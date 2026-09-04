#!/usr/bin/env python3
"""Emit captions/*.srt and *.vtt from the authored turns + measured timings.

NO ASR. The predecessor ran `hyperframes transcribe` per take because its
on-screen text and its VO were authored separately. Here the spoken text is
already an authored artifact (scripts/vo_lines.py) and every turn's start and
length is measured (scripts/timing.py), so transcribing the audio back into
text we already have would only introduce errors -- exactly the proper-noun
mangling the correction pass then has to undo. Hand-authoring from the copy
deck is the documented path when the text and timing are both already known.

Two disciplines the beat schedule does NOT give you for free:

  * A MINIMUM CUE DURATION. Mirroring each turn one-for-one is tempting and
    wrong: a 0.4s "Yes." is not a readable cue. Short turns are merged with
    their neighbour so no cue is under MIN_CUE.
  * LINE DISCIPLINE. Two lines maximum, 3-6 words per line. A caption is a
    glance, not a paragraph.

Speaker prefixes are included because this is a two-hander -- a captions user
with no audio cannot otherwise tell who is talking, and the whole premise is
that two people are talking.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLUG = "ectoin-normal-person"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from timing import walk
from vo_lines import TEXT, SPEAKER

MIN_CUE = 1.10      # seconds. Below this a cue cannot be read.
MAX_CUE = 5.00      # split anything longer
MAX_LINE_WORDS = 6
MAX_CUE_WORDS = 12  # 2 lines x 6. The cue splitter, not just the wrapper,
                    # has to respect this or wrap() silently makes long lines.
NAME = {"S": "SOULHABIT", "J": "JAY"}


def ts(t, vtt=False):
    h, r = divmod(max(0.0, t), 3600)
    m, sec = divmod(r, 60)
    sep = "." if vtt else ","
    return f"{int(h):02d}:{int(m):02d}:{sec:06.3f}".replace(".", sep)


def wrap(text):
    """<=2 lines, 3-6 words each. Longer turns are split across cues upstream."""
    w = text.split()
    if len(w) <= MAX_LINE_WORDS:
        return [" ".join(w)]
    mid = (len(w) + 1) // 2
    return [" ".join(w[:mid]), " ".join(w[mid:])]


def main():
    units, total = walk()
    turns = [(tid, st, ln) for _c, _s, _o, _p, ts_ in units for tid, st, ln in ts_]

    # 1. split long turns into readable cues on word count
    cues = []
    for tid, st, ln in turns:
        words = TEXT[tid].split()
        n = max(int(ln / MAX_CUE) + 1,
                -(-len(words) // MAX_CUE_WORDS))   # ceil-div on BOTH limits
        per = -(-len(words) // n)
        chunks = [words[i:i + per] for i in range(0, len(words), per)] or [words]
        span = ln / len(chunks)
        for i, ch in enumerate(chunks):
            cues.append({"spk": SPEAKER[tid], "t0": st + i * span,
                         "t1": st + (i + 1) * span, "text": " ".join(ch),
                         "first": i == 0})

    # 2. enforce the minimum readable duration by extending into the gap that
    #    follows, and only merging when there is genuinely no room.
    out = []
    for i, c in enumerate(cues):
        nxt = cues[i + 1]["t0"] if i + 1 < len(cues) else total
        c["t1"] = min(max(c["t1"], c["t0"] + MIN_CUE), nxt - 0.02)
        # Too short and mergeable -> merge. Too short and NOT mergeable (a
        # different speaker follows immediately) -> borrow from the previous
        # cue's tail rather than shipping an unreadable flash.
        if c["t1"] - c["t0"] < MIN_CUE:
            if out and out[-1]["spk"] == c["spk"] and \
               len((out[-1]["text"] + " " + c["text"]).split()) <= MAX_CUE_WORDS:
                out[-1]["text"] += " " + c["text"]
                out[-1]["t1"] = c["t1"]
                continue
            if out:
                need = MIN_CUE - (c["t1"] - c["t0"])
                room = max(0.0, (out[-1]["t1"] - out[-1]["t0"]) - MIN_CUE)
                give = min(need, room)
                out[-1]["t1"] -= give
                c["t0"] -= give
        out.append(c)

    srt, vtt = [], ["WEBVTT", ""]
    for i, c in enumerate(out, 1):
        lines = wrap(c["text"])
        if c["first"]:
            lines[0] = f"{NAME[c['spk']]}: {lines[0]}"
        body = "\n".join(lines)
        srt += [str(i), f"{ts(c['t0'])} --> {ts(c['t1'])}", body, ""]
        vtt += [f"{ts(c['t0'], True)} --> {ts(c['t1'], True)}", body, ""]

    d = ROOT / "captions"; d.mkdir(exist_ok=True)
    (d / f"{SLUG}.srt").write_text("\n".join(srt))
    (d / f"{SLUG}.vtt").write_text("\n".join(vtt))
    short = [c for c in out if c["t1"] - c["t0"] < MIN_CUE - 1e-6]
    longest = max(len(l) for c in out for l in wrap(c["text"]))
    print(f"{len(out)} cues -> captions/{SLUG}.srt + .vtt")
    print(f"  shortest {min(c['t1']-c['t0'] for c in out):.2f}s  "
          f"longest {max(c['t1']-c['t0'] for c in out):.2f}s  "
          f"cues under {MIN_CUE}s: {len(short)}")
    print(f"  longest rendered line: {longest} chars, max 2 lines per cue")
    return 0


if __name__ == "__main__":
    sys.exit(main())
