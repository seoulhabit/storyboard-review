#!/usr/bin/env python3
"""Self-contained controls for check-contrast.py (collagen-where-did-it-go).

Run after any change to its ratio math or its Otsu-cluster pixel measurement:

    python3 catalog/tooling/test-contrast-controls.py

check-contrast.py mixes two things that need different fixtures: Part 1 is
pure hex-value math with no rendered asset (a control for it is a numeric
sanity check, not a fixture); Part 2 measures Otsu-split median colours from
an actual image the way exosome-label-problem/scripts/check-contrast-pixels.py
does, and THAT mechanism is what can silently break -- an Otsu threshold that
lands in the wrong place, or a ratio computed on the wrong axis, would still
run and still print a number, just the wrong one. So Part 2 gets image
fixtures; Part 1 gets a numeric check against WCAG's own published reference
ratio (pure black on pure white is exactly 21:1).

  RATIO SANITY   black/white via the hex-pair path             -> MUST be 21:1.
                 If this drifts, every Part-1 pair in check-contrast.py is
                 being measured wrong and its PASS/FAIL lines cannot be trusted.

  POSITIVE       light-grey text on a near-identical light-grey ground,
                 text-like glyph boxes (not a flat block, matching the
                 project's own text_occluded lesson: a checker's fixture
                 should look like the thing it is meant to catch) -> MUST FAIL
                 against the WCAG floor. The case the gate exists to catch.

  NEGATIVE       black text on white, same glyph-box layout      -> MUST PASS.
                 Proves a real, well-contrasted case still measures clean
                 through the same Otsu-split path the positive case used.

Fixtures are single PNG frames built with PIL directly -- Part 2 measures one
extracted frame at a time, so there is no reason to round-trip through ffmpeg
just to produce it.
"""
import importlib.util
import sys
from pathlib import Path

try:
    import numpy as np
    from PIL import Image, ImageDraw
except ImportError:
    print("test-contrast-controls: needs `python3 -m pip install pillow numpy` -- skipping (exit 0).")
    sys.exit(0)

TOOL = (Path(__file__).resolve().parents[1].parent /
        "videos" / "collagen-where-did-it-go" / "scripts" / "check-contrast.py")


def load_tool():
    spec = importlib.util.spec_from_file_location("check_contrast", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def glyph_frame(fg, bg, w=300, h=80):
    """A run of glyph-sized boxes on a ground -- text-like, not a flat block,
    so the Otsu split sees the same bimodal shape real anti-aliased type
    produces (a dark cluster and a light cluster, not one blended average)."""
    im = Image.new("RGB", (w, h), bg)
    d = ImageDraw.Draw(im)
    for i in range(6):
        d.rectangle([20 + i * 42, 20, 20 + i * 42 + 26, 60], fill=fg)
    return np.asarray(im).astype(float)


def main():
    mod = load_tool()
    ok = True

    print("\n  RATIO SANITY -- black/white via the hex-pair path (must be 21.00:1):")
    r = mod.ratio("#000000", "#FFFFFF")
    good = abs(r - 21.0) < 0.02
    ok &= good
    print(f"    {r:.2f}:1   {'PASS' if good else 'FAIL <-- Part 1 ratio math is broken'}")

    print("\n  POSITIVE -- light-grey glyphs on near-identical light-grey ground (must FAIL):")
    frame = glyph_frame(fg=(170, 170, 170), bg=(190, 190, 190))
    result = mod.measure(frame, (0, 0, 300, 80), "control: near-identical greys", mod.TEXT_FLOOR)
    good = result == False
    ok &= good
    print(f"    measure() returned {result!r}   "
          f"{'PASS' if good else 'FAIL <-- the gate has been silenced'}")

    print("\n  NEGATIVE -- black glyphs on white ground (must PASS):")
    frame = glyph_frame(fg=(10, 10, 10), bg=(245, 245, 245))
    result = mod.measure(frame, (0, 0, 300, 80), "control: black on white", mod.TEXT_FLOOR)
    good = result == True
    ok &= good
    print(f"    measure() returned {result!r}   "
          f"{'PASS' if good else 'FAIL <-- a real high-contrast case is being flagged'}")

    print("\n  All controls behave as expected.\n" if ok else
          "\n  A CONTROL FAILED -- do not trust this gate until it is resolved.\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
