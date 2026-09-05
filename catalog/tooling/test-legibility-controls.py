#!/usr/bin/env python3
"""Self-contained controls for check-legibility.py (collagen-where-did-it-go).

Run after any change to its token-floor regex or its glyph_height() pixel
measurement:

    python3 catalog/tooling/test-legibility-controls.py

Two independent mechanisms, two fixtures:

  TOKEN REGEX    a synthetic TOKENS block with one too-small and one
                 acceptable size -> the too-small one MUST be caught, the
                 acceptable one MUST NOT.

  GLYPH HEIGHT   a tall synthetic glyph on a flat ground MUST measure at
                 least its own drawn height; a ground with NOTHING drawn on
                 it (no glyph at all -- the failure mode an empty or fully-
                 occluded phone-scale crop produces) MUST measure 0, so a
                 floor comparison against it fails rather than silently
                 passing on whatever noise crosses the ink threshold.
"""
import importlib.util
import re
import sys
from pathlib import Path

try:
    import numpy as np
except ImportError:
    print("test-legibility-controls: needs `python3 -m pip install numpy` -- skipping (exit 0).")
    sys.exit(0)

TOOL = (Path(__file__).resolve().parents[1].parent /
        "videos" / "collagen-where-did-it-go" / "scripts" / "check-legibility.py")


def load_tool():
    spec = importlib.util.spec_from_file_location("check_legibility", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    mod = load_tool()
    ok = True

    print("\n  TOKEN REGEX -- synthetic TOKENS block, one too-small one acceptable:")
    synthetic = "--t-tiny:22px; --t-fine:44px;"
    sizes = dict(re.findall(r"(--t-[a-z]+):\s*(\d+)px", synthetic))
    tiny_ok = int(sizes["--t-tiny"]) >= mod.FLOOR_PX
    fine_ok = int(sizes["--t-fine"]) >= mod.FLOOR_PX
    good = (not tiny_ok) and fine_ok
    ok &= good
    print(f"    --t-tiny (22px) flagged below floor: {not tiny_ok}   "
          f"--t-fine (44px) passes: {fine_ok}   {'PASS' if good else 'FAIL <-- the floor regex is broken'}")

    print("\n  GLYPH HEIGHT -- a drawn 12px-tall glyph on a flat ground (must measure >= 10px):")
    frame = np.full((60, 60), 230.0)
    frame[20:32, 20:40] = 60.0   # a 12px-tall, 20px-wide solid glyph block
    h = mod.glyph_height(frame, (0, 0, 60, 60), bg_luma=230)
    good = h >= 10
    ok &= good
    print(f"    measured {h}px   {'PASS' if good else 'FAIL <-- glyph_height() is under-measuring a real glyph'}")

    print("\n  GLYPH HEIGHT -- a blank ground, nothing drawn (must measure 0):")
    frame = np.full((60, 60), 230.0)
    h = mod.glyph_height(frame, (0, 0, 60, 60), bg_luma=230)
    good = h == 0
    ok &= good
    print(f"    measured {h}px   {'PASS' if good else 'FAIL <-- noise is being counted as a glyph'}")

    print("\n  All controls behave as expected.\n" if ok else
          "\n  A CONTROL FAILED -- do not trust this gate until it is resolved.\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
