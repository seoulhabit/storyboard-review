#!/usr/bin/env python3
"""Gate the shipped caption sidecars against the 2026-09-05 review.

The build prints its own line/floor numbers, but a build that is never re-run
prints nothing, and the .srt/.vtt are what actually ship. This reads the FILES.

  * <=2 lines, <=42 characters a line
  * >=1.0s on screen, no cue outlasting the next one's start
  * every term the review listed by name, spelled the way it asked
  * VTT cue settings present, and present on the scenes that need them
  * non-speech cues only where they carry information

Term spelling is checked case-SENSITIVELY. "bitop" is the company's own
styling and "Bitop" is wrong even at the start of a sentence; "Ectoin" mid-
sentence is a product name and "ectoin" is the molecule. A case-insensitive
check would pass both and catch neither.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLUG = "ectoin-survival-molecule"
MAX_LINE_CHARS, MAX_LINES, MIN_CUE_S = 42, 2, 1.0

sys.path.insert(0, str(ROOT / "scripts"))
from build_captions import VTT_TOP   # one source for what "placed top" means

# The review's list, verbatim, plus the closing caption's hyphen.
REQUIRED = [
    "Ectoin", "Halomonas elongata", "extremolyte", "humectants",
    "preferential exclusion", "glycerin", "hyaluronic acid", "keratin",
    "atopic dermatitis", "bitop", "Merck", "Kao", "Paula's Choice",
    "The Ordinary", "Abib", "panthenol", "squalane", "ceramides",
    "bacteria-made survival molecule",
]
# Spellings that must NOT appear -- the ASR's guesses and the TTS-safe forms.
FORBIDDEN = [
    "Bitop", "BTOP", "Cow.", "Abbey", "ectoene", "Ecton", "ectoy",
    "bacteria made survival", "double blind", "K beauty",
]


def parse_vtt(text):
    cues, block = [], []
    for line in text.splitlines():
        if line.strip() == "":
            if block:
                cues.append(block)
                block = []
        elif line.strip() != "WEBVTT":
            block.append(line)
    if block:
        cues.append(block)
    out = []
    for b in cues:
        m = re.match(r"([\d:.]+)\s+-->\s+([\d:.]+)(.*)$", b[0])
        if not m:
            continue
        out.append((secs(m.group(1)), secs(m.group(2)),
                    m.group(3).strip(), "\n".join(b[1:])))
    return out


def secs(t):
    h, m, s = t.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def main():
    vtt_p = ROOT / "captions" / f"{SLUG}.vtt"
    srt_p = ROOT / "captions" / f"{SLUG}.srt"
    for p in (vtt_p, srt_p):
        if not p.exists():
            sys.exit(f"FATAL: missing {p}")
    vtt = vtt_p.read_text()
    cues = parse_vtt(vtt)
    bad = []
    print(f"[captions] {len(cues)} cues in {vtt_p.name}")

    for a, b, setting, text in cues:
        lines = text.split("\n")
        if len(lines) > MAX_LINES:
            bad.append(f"{a:.2f}s: {len(lines)} lines -- {text!r}")
        for l in lines:
            if len(l) > MAX_LINE_CHARS:
                bad.append(f"{a:.2f}s: line of {len(l)} chars -- {l!r}")
        if b - a < MIN_CUE_S - 0.01:
            bad.append(f"{a:.2f}s: on screen {b-a:.2f}s, under the {MIN_CUE_S}s floor")
        if not setting:
            bad.append(f"{a:.2f}s: no VTT cue setting -- placement is the player's guess")
    for i in range(len(cues) - 1):
        if cues[i][1] > cues[i + 1][0] + 0.001:
            bad.append(f"{cues[i][0]:.2f}s: outlasts the next cue's start")

    body = "\n".join(c[3] for c in cues)
    for term in REQUIRED:
        if term not in body:
            bad.append(f"required term missing or misspelled: {term!r}")
    for term in FORBIDDEN:
        if term in body:
            bad.append(f"forbidden spelling present: {term!r}")

    ns = [c for c in cues if c[3].startswith("[")]
    print(f"  {sum(1 for c in cues if c[2] == VTT_TOP)} cue(s) placed top, "
          f"{len(ns)} non-speech cue(s): {[c[3] for c in ns]}")
    if len(ns) > 3:
        bad.append(f"{len(ns)} non-speech cues -- decorative transitions should not "
                   f"be captioned individually")

    longest = max(len(l) for c in cues for l in c[3].split("\n"))
    print(f"  longest line {longest} chars (cap {MAX_LINE_CHARS}); "
          f"shortest cue {min(b-a for a,b,_,_ in cues):.2f}s")
    if bad:
        print(f"\n[captions] {len(bad)} finding(s):")
        for x in bad:
            print(f"  - {x}")
        return 1
    print("[captions] PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
