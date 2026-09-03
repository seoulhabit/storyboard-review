#!/usr/bin/env python3
"""Self-contained controls for check-safe-area.py.

Run after ANY change to its ink mask, its background estimator, or its
whole-band ground-fill exclusion:

    python3 catalog/tooling/test-safe-area-controls.py

Why this exists. check-safe-area.py is the only HARD gate in this directory --
it exits non-zero and is meant to stop a render shipping. That makes a false
positive worse than a miss: a gate that cries wolf gets waved through, and the
next wave-through is the real one. It has now been wrong in both directions on
real renders, each time because its notion of "the page background" was an
assumption rather than a measurement:

  * the whole-frame modal broke on a busy landscape frame (two 45%-of-frame
    panels made the modal a PANEL colour, and all four zones reported 100% ink
    across 136 frames with nothing out of place);
  * the outer-border-ring median that replaced it broke on a TRANSITION frame,
    which legitimately contains two grounds -- the ring goes bimodal and
    whichever ground loses the median reads as 100% ink. Measured on a real
    29-scene wipe render: the entire 54x1920 top band reported as inked at
    t=73.50s where that band is uniformly luma 19 with zero variation.

So the fixtures below pin the three behaviours that matter, and two of them are
NEGATIVE on purpose. A gate that only proves it can fail is not validated.

  POSITIVE     text sitting inside the bottom reserved zone     -> MUST FAIL.
               The thing the gate exists for. If this stops firing, the gate has
               been silenced and every "no findings" it prints is worthless.

  SOLID-BLOCK  a bounded solid rectangle inside the bottom zone -> MUST FAIL.
               Guards the ground-fill exclusion specifically. A structure- or
               edge-density test would suppress this (a solid block has no
               internal detail), which is exactly why the exclusion keys on
               whether a masked row spans the band EDGE TO EDGE rather than on
               how much detail it contains.

  TWO-GROUND   two flat grounds meeting at a straight seam, as a wipe or a cut
               boundary produces                                -> MUST PASS.
               The regression this file was added for. Both sides are flat
               scene ground; neither is content; the frame simply has no single
               page background for the estimator to find.

Fixtures are built with ffmpeg and need no project assets.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

TOOL = Path(__file__).resolve().parent / "check-safe-area.py"
W, H, FPS, DUR = 1920, 1080, 30, 3          # landscape; bottom reserved zone is y>=972
PAPER, INK = "0xF7F5F0", "0x131516"


def build(kind, out):
    """One 3s 1920x1080 clip per fixture.

    drawbox only -- this repo's ffmpeg is built without libfreetype, so
    drawtext is unavailable. A run of small bounded boxes is what the gate
    actually sees in a line of text anyway: many partially-masked rows.
    """
    boxes = []
    if kind == "positive":                   # text-like: a run of glyph-sized boxes
        for i in range(18):
            boxes.append(f"drawbox=x={220 + i * 44}:y=1000:w=26:h=44:color={INK}:t=fill")
    elif kind == "solid-block":              # ONE bounded solid rect, no internal detail
        boxes.append(f"drawbox=x=300:y=1000:w=500:h=60:color={INK}:t=fill")
    elif kind == "two-ground":               # flat ink over flat paper, one straight seam
        boxes.append(f"drawbox=x=0:y=0:w={W}:h=300:color={INK}:t=fill")
    else:
        raise ValueError(kind)
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi",
                    "-i", f"color=c={PAPER}:s={W}x{H}:d={DUR}:r={FPS}",
                    "-vf", ",".join(boxes), "-pix_fmt", "yuv420p", str(out)], check=True)


def run(kind):
    with tempfile.TemporaryDirectory() as d:
        proj = Path(d)
        mp4 = proj / "renders" / f"{kind}.mp4"
        build(kind, mp4)
        p = subprocess.run([sys.executable, str(TOOL), str(proj), str(mp4), "--landscape"],
                           capture_output=True, text=True, check=False)
    out = p.stdout + p.stderr
    m = re.search(r"ink found inside a reserved zone on (\d+) sampled frame", out)
    return (int(m.group(1)) if m else 0), p.returncode, out


def main():
    ok = True

    print("\n  POSITIVE — text inside the bottom reserved zone (must FAIL):")
    n, rc, _ = run("positive")
    good = n > 0 and rc != 0
    ok &= good
    print(f"    {n} flagged frame(s), exit={rc}   {'PASS' if good else 'FAIL <-- the gate has been silenced'}")

    print("\n  SOLID-BLOCK — bounded solid rect in the bottom zone (must FAIL):")
    n, rc, _ = run("solid-block")
    good = n > 0 and rc != 0
    ok &= good
    print(f"    {n} flagged frame(s), exit={rc}   "
          f"{'PASS' if good else 'FAIL <-- ground-fill exclusion is over-suppressing'}")

    print("\n  TWO-GROUND — flat ink over flat paper, straight seam (must PASS):")
    n, rc, _ = run("two-ground")
    good = n == 0 and rc == 0
    ok &= good
    print(f"    {n} flagged frame(s), exit={rc}   "
          f"{'PASS' if good else 'FAIL <-- the estimator is flagging a flat ground again'}")

    print("\n  All controls behave as expected.\n" if ok else
          "\n  A CONTROL FAILED — do not trust this gate until it is resolved.\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
