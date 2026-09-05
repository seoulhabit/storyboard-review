#!/usr/bin/env python3
"""Self-contained controls for check-motion-gaps.py.

Run after any change to its motion test, its thresholds or its exemptions:

    python3 catalog/tooling/test-motion-gaps-controls.py

Builds throwaway renders with ffmpeg and drives the gate through its CLI, so an
exit code that stops matching the printed verdict is itself caught.

The control that matters most is SMALL-AREA MOTION. The gate's original test was
the frame-average |luma delta| alone, and that is the wrong question: a sun
rising, fragments drifting apart, a column of tiles falling are each obvious on
screen and each move a small share of the pixels, so they average below the
threshold and read as "static". A gate that flags real motion as dead time gets
ignored, and an ignored gate protects nothing. The fixture below reproduces
exactly that shape -- a small moving block on a still ground -- and asserts the
gate accepts it.

Every control is a PAIR: a fixture the gate must reject and one it must accept.
A gate that has been accidentally silenced passes the second and fails the
first, which a one-sided test cannot tell apart from a working gate.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

TOOL = Path(__file__).resolve().parent / "check-motion-gaps.py"
FPS, DUR = 24, 12          # 12s is comfortably past any --rest under test


def render(path, mover):
    """Encode DUR seconds from frames drawn here, not from an ffmpeg filter.

    An earlier version built these with `drawbox` and an `x='t*36'` expression;
    it silently drew nothing at all -- every frame identical, zero white pixels
    -- so two controls "failed" against a gate that was working. A fixture that
    cannot be trusted is worse than no fixture, and PIL frames are checkable.

    `mover(i)` returns the moving block's box for frame i, or None for none.
    """
    frames = Path(path).parent / "frames"
    frames.mkdir(exist_ok=True)
    for f in frames.glob("*.png"):
        f.unlink()
    for i in range(FPS * DUR):
        im = Image.new("RGB", (480, 270), (16, 16, 16))
        d = ImageDraw.Draw(im)
        d.rectangle([40, 40, 440, 100], fill=(90, 90, 90))   # a still element
        box = mover(i)
        if box:
            d.rectangle(box, fill=(245, 245, 245))
        im.save(frames / f"f{i:05d}.png")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS),
                    "-i", str(frames / "f%05d.png"), "-c:v", "libx264",
                    "-preset", "ultrafast", "-pix_fmt", "yuv420p", str(path)],
                   check=True)


def FROZEN(i):
    """Never moves."""
    return [100, 150, 180, 230]


def BIG_MOTION(i):
    """A wide block crossing the frame -- obvious to the frame average."""
    x = 10 + (i * 460 // (FPS * DUR))
    return [x, 130, x + 190, 250]


def SMALL_MOTION(i):
    """A 16px block creeping across an otherwise still frame. THIS is the shape
    the frame-average test gets wrong and the grid test is there to accept.

    The numbers are MEASURED, not chosen to look small: this fixture produces a
    mean frame-average delta of 0.177 against the 0.35 threshold -- invisible to
    that test -- and a mean per-cell max of 3.74 against 0.9, unmistakable to
    the grid. A 26px block travelling 380px, the first version of this fixture,
    measured 0.755 frame-average and cleared BOTH tests, so it demonstrated
    nothing and the control asserting otherwise was wrong rather than the gate.
    """
    x = 30 + (i * 140 // (FPS * DUR))
    return [x, 180, x + 16, 196]


def run(mp4, *flags):
    r = subprocess.run([sys.executable, str(TOOL), str(mp4), *flags],
                       capture_output=True, text=True, check=False)
    return r.returncode, r.stdout + r.stderr


def control(name, expect_fail, mover, *flags, tmp=None):
    mp4 = Path(tmp) / "fixture.mp4"
    render(mp4, mover)
    code, out = run(mp4, *flags)
    rejected = code != 0
    ok = rejected == expect_fail
    print(f"  {'PASS' if ok else 'FAIL'}  must {'reject' if expect_fail else 'accept':6s}  {name}"
          + ("" if ok else f"   <-- exit {code}"))
    if not ok:
        print("".join(f"        {l}\n" for l in out.strip().splitlines()[-4:]))
    return ok


def main():
    if subprocess.run(["ffmpeg", "-version"], capture_output=True,
                      check=False).returncode != 0:
        print("test-motion-gaps-controls: needs ffmpeg on PATH -- skipping (exit 0).")
        return 0
    ok = True
    with tempfile.TemporaryDirectory() as tmp:
        print("\n  FROZEN FRAME (must be caught)")
        ok &= control("12s of an unchanging frame, --rest 4", True, FROZEN,
                      "--open-until", "0", "--rest", "4", tmp=tmp)
        ok &= control("the same frame inside --exempt-window", False, FROZEN,
                      "--open-until", "0", "--rest", "4",
                      "--exempt-window", "0.00-13.00", tmp=tmp)

        print("\n  LARGE-AREA MOTION (must be accepted)")
        ok &= control("a block crossing the frame", False, BIG_MOTION,
                      "--open-until", "0", "--rest", "4", tmp=tmp)

        print("\n  SMALL-AREA MOTION -- the regression --eps-local exists for")
        ok &= control("a small block moving on a still ground", False, SMALL_MOTION,
                      "--open-until", "0", "--rest", "4", tmp=tmp)
        ok &= control("...and the frame-average test alone rejects it", True,
                      SMALL_MOTION, "--open-until", "0", "--rest", "4",
                      "--eps-local", "999", tmp=tmp)

        print("\n  OPENING IS STRICTER THAN THE REST")
        ok &= control("3s frozen at the open, --open 2 --rest 10", True, FROZEN,
                      "--open", "2", "--open-until", "31", "--rest", "10", tmp=tmp)

        print("\n  A RENDER THAT CANNOT BE READ IS A FAILURE, NEVER A PASS")
        code, _ = run(Path(tmp) / "does-not-exist.mp4")
        good = code != 0
        ok &= good
        print(f"  {'PASS' if good else 'FAIL'}  must reject  an absent render"
              + ("" if good else f"   <-- exit {code}"))

        empty = Path(tmp) / "empty.mp4"
        empty.write_bytes(b"")
        code, out = run(empty)
        good = code != 0 and "nothing to measure" in out
        ok &= good
        print(f"  {'PASS' if good else 'FAIL'}  must reject  a zero-byte render"
              + ("" if good else f"   <-- exit {code}"))

    print("\n  All controls behave as expected.\n" if ok else
          "\n  A CONTROL FAILED -- do not trust this gate until it is resolved.\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
