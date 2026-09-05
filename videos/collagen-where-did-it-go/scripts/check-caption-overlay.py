#!/usr/bin/env python3
"""Would a real two-line player caption cover anything essential?

    python3 scripts/check-caption-overlay.py .
    python3 scripts/check-caption-overlay.py . renders/collagen-where-did-it-go_final.mp4

This project's own safe-area reserve is --safe-bottom:108px (_preamble.py) --
sized for platform UI chrome (the like/subscribe bar), not for captions. A
real two-line caption in the YouTube/most players' default styling runs
roughly 220-260px tall at 1080p once font size, line-height and the player's
own bottom margin are accounted for -- more than DOUBLE the 108px this
composition actually reserves. So content that clears the shipped safe-area
gate can still sit directly under a viewer's own caption track once they
turn it on, which is exactly the accessibility failure mode a captions-first
review exists to catch: the feature that makes the video usable without
sound can simultaneously make it unreadable.

Method: check-safe-area.py's own ink-detection machinery (multi-ground
clustering, run-length antialiasing filter), invoked as a subprocess with a
--safe-bottom of 240px -- the midpoint of the 220-260px range -- instead of
this project's own 108px. Reusing the tool rather than reimplementing its
detection means a fix to one measurement (e.g. the multi-ground estimator)
benefits both gates without drifting apart.

This is advisory, not a hard gate: the shipped safe-area reserve (108px) is
a deliberate, reviewed platform-chrome budget, and this project ships a
clean captions track rather than assuming every viewer enables the player's
own OS/platform captions -- so a finding here is "worth checking before an
open-caption burn-in," not "this render is broken." Promote to a hard gate
if this project ever ships a variant relying on player-native captions.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
SAFE_AREA = Path(__file__).parent / "check-safe-area.py"
CAPTION_BOTTOM_PX = 240  # midpoint of the review's own 220-260px estimate


def main():
    render_arg = sys.argv[2:3]
    cmd = [sys.executable, str(SAFE_AREA), str(ROOT), *render_arg,
           "--landscape", "--safe-bottom", str(CAPTION_BOTTOM_PX)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = r.stdout + r.stderr
    print(f"Caption-overlay scan -- simulating a {CAPTION_BOTTOM_PX}px player caption band "
          f"(this project's own safe-bottom is 108px).")
    for line in out.splitlines():
        if line.startswith("Safe-area scan") or line.startswith("  reserved zones"):
            continue  # check-safe-area.py's own header, redundant with ours above
        print(f"  {line}" if not line.startswith(" ") else line)
    if r.returncode == 2:
        return 2  # canvas mismatch -- a real configuration error, not advisory
    if "no findings" in out:
        return 0
    print("\n  ADVISORY (does not fail the gate): the shipped 108px safe-area reserve is a")
    print("  deliberate platform-chrome budget, not a caption reserve -- this project ships")
    print("  a clean sidecar caption track rather than relying on player-native captions.")
    print("  Worth a look before any open-caption burn-in variant.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
