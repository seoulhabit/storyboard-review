#!/usr/bin/env python3
"""Gate the shipped SRT/VTT for reading speed and line length.

    python3 scripts/check-captions.py .

Reads captions/<slug>.srt directly -- the shipped deliverable, not the
generator's own internal state -- so this catches a hand-edit or a stale
file as readily as a real regression. build_captions.py's own summary line
(CPS/line-length counts) is a build-time echo of the same numbers; this is
the independent, fail-closed version meant for `npm run gates`.

Acceptance (the review's own numbers):
  - zero cues above MAX_CPS_HARD (20 characters/second)
  - at least MIN_PREF_FRACTION (95%) of cues at or below MAX_CPS_PREF (17)
  - zero lines above MAX_LINE_CHARS (42)
  - zero cues below MIN_CUE_S (1.0s)
  - zero overlapping cues
"""
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
SLUG = "collagen-where-did-it-go"
MAX_CPS_HARD, MAX_CPS_PREF = 20.0, 17.0
MIN_PREF_FRACTION = 0.95
MAX_LINE_CHARS = 42
MIN_CUE_S = 1.0


def ts(s):
    h, m, rest = s.split(":")
    sec, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000


def parse_srt(path):
    raw = path.read_text().strip()
    cues = []
    for block in re.split(r"\n\s*\n", raw):
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue
        a, b = lines[1].split(" --> ")
        cues.append((ts(a), ts(b), lines[2:]))
    return cues


def main():
    srt = ROOT / "captions" / f"{SLUG}.srt"
    if not srt.exists():
        print(f"  MISSING: {srt.relative_to(ROOT)}")
        return 1

    cues = parse_srt(srt)
    if not cues:
        print("  SRT has no cues")
        return 1

    findings = []
    cps_values = []
    for i, (a, b, lines) in enumerate(cues):
        dur = b - a
        chars = len(" ".join(lines))
        cps = chars / dur if dur > 0 else 999.0
        cps_values.append(cps)
        if dur < MIN_CUE_S - 0.005:
            findings.append(f"cue {i+1} ({a:.2f}-{b:.2f}s): {dur:.2f}s, under the {MIN_CUE_S:.1f}s floor")
        if cps > MAX_CPS_HARD:
            findings.append(f"cue {i+1} ({a:.2f}-{b:.2f}s): {cps:.1f} CPS, over the {MAX_CPS_HARD:.0f} hard ceiling -- {' / '.join(lines)!r}")
        for ln in lines:
            if len(ln) > MAX_LINE_CHARS:
                findings.append(f"cue {i+1} ({a:.2f}-{b:.2f}s): line is {len(ln)} chars (max {MAX_LINE_CHARS}) -- {ln!r}")
        if i + 1 < len(cues) and b > cues[i + 1][0] + 0.001:
            findings.append(f"cue {i+1} overlaps cue {i+2}: ends {b:.3f}s, next starts {cues[i+1][0]:.3f}s")

    pref_ok = sum(1 for c in cps_values if c <= MAX_CPS_PREF)
    pref_fraction = pref_ok / len(cps_values)
    if pref_fraction < MIN_PREF_FRACTION:
        findings.append(f"only {pref_fraction:.0%} of cues at or under {MAX_CPS_PREF:.0f} CPS "
                         f"(want >= {MIN_PREF_FRACTION:.0%})")

    print(f"  {len(cues)} cues, worst {max(cps_values):.1f} CPS, "
          f"{pref_fraction:.0%} at or under {MAX_CPS_PREF:.0f} CPS")
    if findings:
        print(f"  {len(findings)} finding(s):")
        for f in findings:
            print(f"    - {f}")
        return 1
    print("  all cues pass: CPS, line length, minimum duration, no overlaps")
    return 0


if __name__ == "__main__":
    sys.exit(main())
