#!/usr/bin/env python3
"""WCAG contrast for a project's declared token pairs. Measured, not eyeballed.

The SOURCE-SIDE half of the contrast pair. Its companion,
check-contrast-pixels.py, measures the render; this one measures the palette,
and each catches a class the other structurally cannot:

  * this file catches a token pair that never clears its floor on the ground it
    actually lands on -- the trap being that a token is usually checked against
    ONE ground and then used on several. `--ink-2` reads 4.89:1 on paper and
    3.44:1 on ink; `--coral` reads 5.03:1 on ink-soft and 2.72:1 on a light
    card. Neither project's palette had a per-ground record before this ran.
  * it CANNOT see anything the compositor does: a photographic plate, a scrim,
    an opacity tween, a blend layer, or a stylesheet rule that overrides the
    declared colour at render time. That is check-contrast-pixels.py's job, and
    the defect that motivated both is exactly of that kind.

Neither replaces the other, and they belong in different stages: this runs
source-side with no render (a project's `gates:source`), the pixel one needs a
finished master (`postrender`).

EXPECTED FAILURES ARE THE POINT. A pair carrying an "expected FAIL" note is
documentation, not aspiration -- it records why a token is ground-scoped, and
it fails the gate if it ever starts PASSING, because that means someone changed
the token and the note is now a lie. A pair list with no expected failures is
usually a pair list that has not been written honestly.

FIELD CONTRACT
    python3 check-contrast-tokens.py <pairs.json>
                                     [--text-floor 4.5] [--graphic-floor 3.0]

pairs.json is {"tokens": {...}, "pairs": [...]}:

    {"tokens": {"paper": "#F7F5F0", "ink": "#131516", "ink-2": "#666666"},
     "pairs": [
       {"label": ".p-body ink-2 on paper", "fg": "ink-2", "bg": "paper"},
       {"label": "ink-3 on paper (superseded, must not ship)",
        "fg": "#9C978D", "bg": "paper",
        "note": "expected FAIL -- .p-body uses --ink-2 instead"},
       {"label": "coral-deep fill on paper", "fg": "coral-deep", "bg": "paper",
        "floor": "graphic"}
     ]}

`fg`/`bg` are either a key in `tokens` or a literal `#rrggbb`. `floor` is
"text" (4.5:1), "graphic" (3.0:1 -- a meaningful non-text mark) or a number.
A `note` containing "expected FAIL" inverts the assertion for that pair.

Exits non-zero when any pair behaves differently from its record -- a real pair
below its floor, or an expected-FAIL pair that now passes.

Provenance: three near-identical copies of this arithmetic existed across
`videos/ectoin-normal-person`, `videos/ectoin-survival-molecule` and
`videos/collagen-where-did-it-go` before this was catalogued. The pair schema
is collagen's (per-pair floor and free-text note, rather than ectoin's bare
boolean and one hardcoded floor, which could not express a graphic-stroke pair).
"""
import argparse
import json
import sys
from pathlib import Path

TEXT_FLOOR, GRAPHIC_FLOOR = 4.5, 3.0


def lin(c):
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def lum(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def resolve(v, tokens):
    if isinstance(v, str) and v.startswith("#"):
        return v
    if v not in tokens:
        sys.exit(f"FATAL: {v!r} is neither a #rrggbb literal nor a key in `tokens`")
    return tokens[v]


def check(pairs, tokens, text_floor, graphic_floor):
    floors = {"text": text_floor, "graphic": graphic_floor}
    bad, expected = 0, 0
    for p in pairs:
        fg, bg = resolve(p["fg"], tokens), resolve(p["bg"], tokens)
        f = p.get("floor", "text")
        floor = float(f) if isinstance(f, (int, float)) else floors.get(f, text_floor)
        r = ratio(fg, bg)
        note = p.get("note")
        expect_fail = bool(note) and "expected FAIL" in note
        expected += expect_fail
        passes = r >= floor
        ok = passes != expect_fail
        bad += not ok
        print(f"  {'PASS' if passes else 'FAIL'}  {r:5.2f}:1 (floor {floor})  "
              f"{p['label']} [{fg} on {bg}]" + (f"  -- {note}" if note else "")
              + ("" if ok else "   <-- UNEXPECTED"))
    return bad, expected


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pairs")
    ap.add_argument("--text-floor", type=float, default=TEXT_FLOOR)
    ap.add_argument("--graphic-floor", type=float, default=GRAPHIC_FLOOR)
    a = ap.parse_args()
    doc = json.loads(Path(a.pairs).read_text())
    pairs, tokens = doc["pairs"], doc.get("tokens", {})
    print(f"[contrast-tokens] {len(pairs)} declared pair(s) from {Path(a.pairs).name}")
    bad, expected = check(pairs, tokens, a.text_floor, a.graphic_floor)
    print(f"[contrast-tokens] {bad} pair(s) behaved differently from their record; "
          f"{expected} deliberate documented failure(s).")
    print("  Covered: a foreground token against a FLAT ground.")
    print("  NOT covered: text over a photo, a gradient, a blend layer, an opacity")
    print("               tween, or a colour overridden at render time --")
    print("               those need check-contrast-pixels.py against a render.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
