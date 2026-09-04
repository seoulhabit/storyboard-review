#!/usr/bin/env python3
"""Emit captions/<slug>.srt and .vtt from the master word manifest.

NO ASR CALL HERE. The manifest (assets/voice/master.words.json) already
carries every scripted word with its MEASURED time -- the same alignment the
frame generator's @w() markers are keyed to -- so a second transcription
could only disagree with the render. Text is the SCRIPTED spelling (UK,
punctuation intact); spoken numeral phrases are shown as numerals
(vo_words.CAPTION_FORM). No speaker prefixes: there is one narrator.

Cue discipline (a cue is a glance, not a mirror of the beat schedule):
  >= MIN_CUE_S on screen, <= MAX_WORDS words, break at sentence ends or
  long clauses, <= 2 balanced lines. No cue outlasts the next one's start.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLUG = "collagen-where-did-it-go"
MIN_CUE_S, MAX_CUE_S, MAX_WORDS = 1.0, 5.5, 11

sys.path.insert(0, str(ROOT / "scripts"))
from timing import walk
from vo_words import caption_text


def group(words):
    cues, cur = [], []
    for w in words:
        cur.append(w)
        span = cur[-1]["end"] - cur[0]["start"]
        ends_sentence = re.search(r"[.?!]$", cur[-1]["text"])
        ends_clause = re.search(r"[,;:]$", cur[-1]["text"]) and len(cur) >= 5 and span >= 1.6
        if ends_sentence or ends_clause or len(cur) >= MAX_WORDS or span >= MAX_CUE_S:
            cues.append(cur); cur = []
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
    units, files, total, manifest = walk()
    cues = []
    for u in units:
        if not u.spoken:
            continue
        for g in group(u.words):
            start = g[0]["start"]
            end = max(g[-1]["end"], start + MIN_CUE_S)
            cues.append((start, end, wrap(caption_text([w["text"] for w in g]))))
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
    vtt = "WEBVTT\n\n" + "\n".join(f"{ts(a,'.')} --> {ts(b,'.')}\n{x}\n" for a, b, x in cues)
    (out / f"{SLUG}.srt").write_text(srt)
    (out / f"{SLUG}.vtt").write_text(vtt)
    short = [c for c in cues if c[1] - c[0] < MIN_CUE_S - 0.01]
    print(f"  {len(cues)} cues -> captions/{SLUG}.srt + .vtt"
          f"{'  [VO MANIFEST: FAKE]' if manifest.get('source') == 'fake' else ''}")
    print(f"  shortest {min(b-a for a,b,_ in cues):.2f}s, longest {max(b-a for a,b,_ in cues):.2f}s, "
          f"under the floor: {len(short)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
