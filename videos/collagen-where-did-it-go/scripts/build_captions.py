#!/usr/bin/env python3
"""Emit captions/<slug>.srt and .vtt from the line table + real clip timings.

NO ASR. Every other project on this channel runs `hyperframes transcribe` over a
mixed VO and then hand-corrects the proper nouns back to what was actually said.
Here the spoken text is an authored artifact -- vo_lines.LINES IS the script
sent to TTS -- so transcribing it would only introduce errors into text already
known verbatim, and then spend a correction pass undoing them.

What is NOT free is the timing. Cue starts come from the composition's real
audio placement (scene start + line offset - VO_LEAD) and cue ends from each
take's ffprobed duration, so a re-recorded line moves its cue on the next build.
Word-level positions WITHIN a cue are apportioned by word count, which is an
approximation and is labelled as one here rather than presented as measured.

Cue discipline, which a mechanical one-cue-per-line split does not give you:
  * >= MIN_CUE seconds on screen. Deriving cues straight from element entrance
    times produced a sidecar with 10 of 29 cues under 0.5s on a sibling project,
    the shortest at 0.15s -- nowhere near readable.
  * <= MAX_WORDS words, split at clause boundaries, so a 26-word line becomes
    two or three readable cues instead of one wall.
  * <= 2 lines on screen, ~3-6 words per line.

This project burns in NO caption track: the on-screen language is the two-lane
dialogue card system, and a caption band would restate words already in frame.
The sidecar is the caption deliverable, which is the right split for long-form --
it is watched in a player that surfaces an uploaded track.
"""
import re
from pathlib import Path
from build_frames import scene_timing, LEAD
from build_index import SCENES, VO_LEAD
from vo_lines import by_scene

ROOT = Path(__file__).resolve().parent.parent
SLUG = "collagen-where-did-it-go"
MIN_CUE, MAX_CUE, MAX_WORDS, MAX_LINE = 1.0, 5.5, 12, 6
SPEAKER = {"soul": "SoulHabit", "jay": "Jay"}


def chunks(text):
    """Split a spoken line into cue-sized pieces at clause boundaries."""
    parts = [p for p in re.split(r"(?<=[.?!,])\s+", text.strip()) if p]
    out, cur = [], ""
    for p in parts:
        cand = (cur + " " + p).strip()
        if cur and len(cand.split()) > MAX_WORDS:
            out.append(cur); cur = p
        else:
            cur = cand
    if cur:
        out.append(cur)
    # a clause can still exceed MAX_WORDS on its own -- hard-wrap it
    final = []
    for c in out:
        w = c.split()
        while len(w) > MAX_WORDS:
            final.append(" ".join(w[:MAX_WORDS])); w = w[MAX_WORDS:]
        if w:
            final.append(" ".join(w))
    return final


def wrap(text):
    """<= 2 lines, ~3-6 words each. A caption is a glance, not a paragraph."""
    w = text.split()
    if len(w) <= MAX_LINE:
        return text
    mid = (len(w) + 1) // 2
    return " ".join(w[:mid]) + "\n" + " ".join(w[mid:])


def cues():
    """Chunks are MERGED up to the readability floor, never clamped down to it.

    The first version apportioned each line into chunks and then clamped any cue
    that ran short -- which produced 10 of 61 cues under 1.0s (shortest 0.43s),
    because the de-overlap pass pulled each cue's end back to the next cue's
    start and undid the floor it had just applied. Merging first means the floor
    holds by construction and no clamp is needed.
    """
    t, grouped, out = scene_timing(), by_scene(), []
    starts, acc = {}, 0.0
    for cid, _ in SCENES:
        starts[cid] = acc
        acc += t[cid.split("-")[0]]["dur"]

    for cid, _ in SCENES:
        k = cid.split("-")[0]
        for ln, tim in zip(grouped[k], t[k]["lines"]):
            a, dur = starts[cid] + tim["start"] - VO_LEAD, tim["dur"]
            cs = chunks(ln["text"])
            nw = sum(len(c.split()) for c in cs) or 1
            # proportional share per chunk -- an approximation, not a measurement
            sized = [[c, dur * len(c.split()) / nw] for c in cs]
            # merge forward until every piece clears the floor
            merged = []
            for c, d in sized:
                if merged and (merged[-1][1] < MIN_CUE or d < MIN_CUE) and \
                        len((merged[-1][0] + " " + c).split()) <= MAX_WORDS + 6:
                    merged[-1][0] += " " + c
                    merged[-1][1] += d
                else:
                    merged.append([c, d])
            # a single piece can still be shorter than the floor if the whole
            # TAKE is (e.g. "Yes."); let it run past the take rather than sit
            # on screen for 0.4s, since the next line's gap absorbs it
            pos = a
            for c, d in merged:
                out.append({"a": pos, "b": pos + max(d, MIN_CUE), "who": ln["who"],
                            "text": c})
                pos += d

    out.sort(key=lambda c: c["a"])
    for i in range(len(out) - 1):
        # never two cues on screen at once; a 20ms guard between them
        out[i]["b"] = min(out[i]["b"], out[i + 1]["a"] - 0.02, out[i]["a"] + MAX_CUE)
    return out


def ts(t, sep=","):
    h, r = divmod(max(t, 0.0), 3600)
    m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d}{sep}{int(round((s % 1) * 1000)):03d}"


def main():
    cs = cues()
    srt, vtt = [], ["WEBVTT", ""]
    prev = None
    for i, c in enumerate(cs, 1):
        # Speaker prefix only when the speaker CHANGES. With two voices and no
        # burned-in track a captions user cannot otherwise tell who is talking --
        # which is most of the joke -- but prefixing every cue is noise.
        body = wrap(f"{SPEAKER[c['who']]}: {c['text']}" if c["who"] != prev else c["text"])
        prev = c["who"]
        srt += [str(i), f"{ts(c['a'])} --> {ts(c['b'])}", body, ""]
        vtt += [f"{ts(c['a'], '.')} --> {ts(c['b'], '.')}", body, ""]
    (ROOT / "captions").mkdir(exist_ok=True)
    (ROOT / "captions" / f"{SLUG}.srt").write_text("\n".join(srt))
    (ROOT / "captions" / f"{SLUG}.vtt").write_text("\n".join(vtt))
    d = [c["b"] - c["a"] for c in cs]
    print(f"captions/{SLUG}.srt + .vtt  {len(cs)} cues, "
          f"shortest {min(d):.2f}s, longest {max(d):.2f}s, "
          f"under {MIN_CUE}s: {sum(1 for x in d if x < MIN_CUE - 1e-6)}")


if __name__ == "__main__":
    main()
