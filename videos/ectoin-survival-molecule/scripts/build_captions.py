#!/usr/bin/env python3
"""Build captions/<slug>.srt and .vtt from the CUT voiceover manifests.

NO ASR CALL HERE ANY MORE. Timing.walk() already carries every scene's word
list (assets/voice/NN.words.json, produced once by scripts/gen_vo.py cut) with
ASR timing -- re-transcribing to build captions risked a second ASR pass
disagreeing with the one the render's own word-marker bindings are keyed to.

Two disciplines the skill requires and that a naive build gets wrong, both
still true here:

  * ASR mangles exactly the vocabulary this channel depends on. "ectoin" came
    back as Ecton / ectoene / ectoy / echetoin across takes. Captions use the
    SCRIPTED spelling (vo_lines.LINES / TEXT), aligned onto the ASR word
    TIMING via the same difflib alignment gen_vo.py uses to cut scenes --
    never the raw ASR text. vo_words.CORRECTIONS is kept as a fallback for any
    word alignment does not confidently cover.
  * A cue is a glance, not a mirror of the beat schedule. Max 2 lines, ~3-6
    words a line, and a hard 1.0s minimum on screen -- a hand-authored sidecar
    that simply mirrored element entrances produced 10 cues under 0.5s on an
    earlier project, the shortest 0.15s.
"""
import difflib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLUG = "ectoin-survival-molecule"
MIN_CUE_S, MAX_CUE_S, MAX_WORDS = 1.0, 5.5, 11

sys.path.insert(0, str(ROOT / "scripts"))
from vo_words import CORRECTIONS, norm
from vo_lines import TEXT
from timing import walk


def correct(w):
    for pat, rep in CORRECTIONS.items():
        if re.fullmatch(pat, w, re.IGNORECASE):
            return rep.capitalize() if w[:1].isupper() and rep[:1].islower() else rep
    return w


def scripted_words(scene):
    """[{'text': scripted spelling, 'start', 'end'}] -- absolute time,
    aligning the scripted text (real punctuation/casing) onto the manifest's
    ASR word timing. Falls back to corrected ASR text where alignment is not
    confident (an 'insert'/'delete' opcode -- ASR added or dropped a word)."""
    script_disp = TEXT[scene.cid].split()
    script_norm = [norm(w) for w in script_disp]
    asr = scene.words
    asr_norm = [norm(w["text"]) for w in asr]
    sm = difflib.SequenceMatcher(None, script_norm, asr_norm, autojunk=False)
    mapped = [None] * len(asr)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                mapped[j1 + k] = script_disp[i1 + k]
        elif tag == "replace" and i2 > i1:
            n = max(j2 - j1, 1)
            for k in range(j2 - j1):
                ii = min(i1 + (k * (i2 - i1)) // n, i2 - 1)
                mapped[j1 + k] = script_disp[ii]

    out = []
    for idx, w in enumerate(asr):
        text = mapped[idx] if mapped[idx] else correct(w["text"])
        out.append({"text": text,
                    "start": round(scene.vo_start + w["start"], 3),
                    "end": round(scene.vo_start + w["end"], 3)})
    return out


def group(words):
    """Greedy cue packing: break on sentence end, word count, or duration."""
    cues, cur = [], []
    for w in words:
        cur.append(w)
        span = cur[-1]["end"] - cur[0]["start"]
        ends_sentence = re.search(r"[.?!]$", cur[-1]["text"])
        ends_clause = re.search(r"[,;:]$", cur[-1]["text"]) and len(cur) >= 5 and span >= 1.6
        if ends_sentence or ends_clause or len(cur) >= MAX_WORDS or span >= MAX_CUE_S:
            cues.append(cur)
            cur = []
    if cur:
        cues.append(cur)
    merged = []
    for c in cues:
        if merged and (c[-1]["end"] - c[0]["start"]) < MIN_CUE_S:
            merged[-1].extend(c)
        else:
            merged.append(c)
    return merged


def wrap(text):
    """<=2 lines, balanced, 3-6 words a line."""
    ws = text.split()
    if len(ws) <= 6:
        return text
    mid = (len(ws) + 1) // 2
    return " ".join(ws[:mid]) + "\n" + " ".join(ws[mid:])


def ts(t, sep=","):
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d}{sep}{int(round((s % 1) * 1000)):03d}"


def main():
    scenes, _total = walk()
    cues = []
    for s in scenes:
        for g in group(scripted_words(s)):
            start = g[0]["start"]
            end = max(g[-1]["end"], start + MIN_CUE_S)
            cues.append((start, end, wrap(" ".join(w["text"] for w in g))))

    # No cue may outlast the next one's start.
    for i in range(len(cues) - 1):
        if cues[i][1] > cues[i + 1][0]:
            trimmed = cues[i + 1][0] - 0.02
            if trimmed - cues[i][0] >= MIN_CUE_S:
                cues[i] = (cues[i][0], trimmed, cues[i][2])
            else:
                end = cues[i][0] + MIN_CUE_S
                cues[i] = (cues[i][0], end, cues[i][2])
                cues[i + 1] = (max(cues[i + 1][0], end + 0.02), cues[i + 1][1], cues[i + 1][2])

    out = ROOT / "captions"
    out.mkdir(exist_ok=True)
    srt = "\n".join(f"{i+1}\n{ts(a)} --> {ts(b)}\n{x}\n" for i, (a, b, x) in enumerate(cues))
    vtt = "WEBVTT\n\n" + "\n".join(
        f"{ts(a,'.')} --> {ts(b,'.')}\n{x}\n" for a, b, x in cues)
    (out / f"{SLUG}.srt").write_text(srt)
    (out / f"{SLUG}.vtt").write_text(vtt)

    short = [c for c in cues if c[1] - c[0] < MIN_CUE_S - 0.01]
    print(f"  {len(cues)} cues -> captions/{SLUG}.srt + .vtt")
    print(f"  shortest {min(b-a for a,b,_ in cues):.2f}s, longest {max(b-a for a,b,_ in cues):.2f}s")
    print(f"  cues under the {MIN_CUE_S}s floor: {len(short)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
