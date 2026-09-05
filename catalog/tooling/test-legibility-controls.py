#!/usr/bin/env python3
"""Self-contained controls for check-legibility.py (beside this file).

Run after any change to its token parser or its glyph_height() pixel
measurement:

    python3 catalog/tooling/test-legibility-controls.py

Four fixtures across the gate's two mechanisms:

  TOKEN PARSER   a synthetic token block with one too-small and one acceptable
                 size -> the too-small one MUST be caught, the acceptable one
                 MUST NOT.

  TOKEN SOURCES  the same sizes written two ways -- inside a
                 `TOKENS = \"\"\"...\"\"\"` python block, and as a bare
                 stylesheet -> both MUST parse to the same dict. That
                 either-shape claim is what lets one gate read a project's
                 `scripts/_preamble.py` and another's `assets/tokens/
                 tokens.css`, so it is worth a control rather than a comment.

  GLYPH HEIGHT   a tall synthetic glyph on a flat ground MUST measure at least
                 its own drawn height; a ground with NOTHING drawn on it (no
                 glyph at all -- the failure mode an empty or fully-occluded
                 phone-scale crop produces) MUST measure 0, so a floor
                 comparison against it fails rather than silently passing on
                 whatever noise crosses the ink threshold.

NOTE ON THE FIRST CONTROL. It calls the gate's own token_sizes(); the version
this replaced re-implemented the regex inline, so the headline claim it printed
("the floor regex is broken") was one the fixture structurally could not
detect -- it was testing a copy of the regex, not the one that ships. A control
that re-implements the thing it checks is not a control.
"""
import importlib.util
import sys
from pathlib import Path

try:
    import numpy as np
except ImportError:
    print("test-legibility-controls: needs `python3 -m pip install numpy` -- skipping (exit 0).")
    sys.exit(0)

TOOL = Path(__file__).resolve().parent / "check-legibility.py"


def load_tool():
    spec = importlib.util.spec_from_file_location("check_legibility", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    if not TOOL.exists():
        print(f"test-legibility-controls: {TOOL.name} not found beside this fixture -- "
              f"skipping (exit 0).")
        return 0
    mod = load_tool()
    ok = True

    print("\n  TOKEN PARSER -- one too-small size and one acceptable, through the gate's own parser:")
    sizes = mod.token_sizes("--t-tiny:22px; --t-fine:44px;")
    tiny_ok = sizes.get("--t-tiny", 0) >= mod.FLOOR_PX
    fine_ok = sizes.get("--t-fine", 0) >= mod.FLOOR_PX
    good = (not tiny_ok) and fine_ok and len(sizes) == 2
    ok &= good
    print(f"    parsed {sizes}   --t-tiny below floor: {not tiny_ok}   --t-fine passes: {fine_ok}"
          f"   {'PASS' if good else 'FAIL <-- token_sizes() or the floor is broken'}")

    print("\n  TOKEN SOURCES -- a python TOKENS block and a bare stylesheet must parse identically:")
    as_python = 'JUNK = "--t-decoy:11px"\nTOKENS = """\n  --t-body:48px; --t-hero:96px;\n"""\n'
    as_css = ":root { --t-body:48px; --t-hero:96px; }"
    a, b = mod.token_sizes(as_python), mod.token_sizes(as_css)
    # The decoy proves the python form reads ONLY the TOKENS block: a gate that
    # scanned the whole file would pick up --t-decoy and fail a project for a
    # size that is not a live token at all.
    good = a == b == {"--t-body": 48, "--t-hero": 96}
    ok &= good
    print(f"    python block -> {a}\n    stylesheet   -> {b}   "
          f"{'PASS' if good else 'FAIL <-- the two source shapes disagree, or the decoy leaked in'}")

    print("\n  GLYPH HEIGHT -- a drawn 12px-tall glyph on a flat ground (must measure >= 10px):")
    frame = np.full((60, 60), 230.0)
    frame[20:32, 20:40] = 60.0   # a 12px-tall, 20px-wide solid glyph block
    h = mod.glyph_height(frame, (0, 0, 60, 60), bg_luma=230)
    good = h >= 10
    ok &= good
    print(f"    measured {h}px   "
          f"{'PASS' if good else 'FAIL <-- glyph_height() is under-measuring a real glyph'}")

    print("\n  GLYPH HEIGHT -- a blank ground, nothing drawn (must measure 0):")
    frame = np.full((60, 60), 230.0)
    h = mod.glyph_height(frame, (0, 0, 60, 60), bg_luma=230)
    good = h == 0
    ok &= good
    print(f"    measured {h}px   "
          f"{'PASS' if good else 'FAIL <-- noise is being counted as a glyph'}")

    print("\n  All controls behave as expected.\n" if ok else
          "\n  A CONTROL FAILED -- do not trust this gate until it is resolved.\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
