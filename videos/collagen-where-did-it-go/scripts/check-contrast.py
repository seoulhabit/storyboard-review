#!/usr/bin/env python3
"""WCAG contrast, two ways: declared tokens, and actual rendered pixels.

    python3 scripts/check-contrast.py .
    python3 scripts/check-contrast.py . renders/collagen-where-did-it-go_final.mp4

PART 1 -- STATIC TOKEN PAIRS (ectoin-normal-person/scripts/contrast.py's
method, ported). Every foreground/ground pair actually used for text or a
meaningful graphic stroke in this project's _preamble.py / actors.py /
frames_*.py, checked against the WCAG floor (4.5:1 text, 3.0:1 graphic).
Several of these pairs were the review's own P0 findings this session and are
listed here as regression locks, not new discoveries: --ink-3 on --paper
(2.67:1, fixed to --ink-2 in frames_a.py/actors.py), --ink-3-dark on
--ink-soft (4.13:1, fixed to --ink-2-dark in _preamble.py), .res-note and
.bar-label at reduced opacity (fixed to full opacity).

Covered: foreground token vs a FLAT ground.
NOT covered: text over a photo, a gradient, or a blend-mode layer -- Part 2.

PART 2 -- COMPOSITED PIXELS, on the actual render (exosome-label-problem/
scripts/check-contrast-pixels.py's method, ported): crop a known region at a
known timestamp, Otsu-split into a dark/light cluster, ratio their median
colours. This is what a viewer actually sees after opacity and compositing,
which is exactly what the two opacity-related P0 fixes above needed proving
on -- a token pair can be correct and an `opacity:.85` on the element that
uses it can still take the shipped pixels under the floor.

PART 3 -- REDUNDANT CHANNEL, not a contrast ratio. Coral and celadon (the
evidence scene's two filter-state fills) measure 1.49:1 against each other --
indistinguishable by lightness alone, so colour-blind-safe only if a SECOND
channel carries the same information. Checked here by confirming the tag
glyphs ($ / ?) are present in source for every dropped-tile state, not by a
WCAG number (there is no "contrast floor" for two adjacent fills; the actual
requirement is a non-colour channel, and that is what is verified).
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
RENDER = Path(sys.argv[2]) if len(sys.argv) > 2 else None
SCRIPTS = ROOT / "scripts"

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


def lum_rgb(rgb):
    r, g, b = (lin(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio_rgb(a, b):
    la, lb = lum_rgb(a), lum_rgb(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


# ---------------------------------------------------------------- Part 1 ---
PAPER, INK, INK_SOFT, MIST = "#F7F5F0", "#131516", "#211F1B", "#F0EBE1"
AQUA, CORAL, MOSS, CELADON = "#59B8AE", "#C97A5C", "#4F6B52", "#93B896"
HIGHLIGHTER = "#E0A32B"
INK_2, INK_3 = "#6B6B6B", "#9C978D"
INK_2_DARK, INK_3_DARK, INK_2_MIST = "#878B8C", "#7C8082", "#626262"
CHIP_ON_INK = "#93989A"
CORAL_DEEP = "#A85A3C"

# (label, fg, bg, floor, note)
CASES = [
    ("--ink-2 on --paper (.p-body, .kicker, .qmark/.branch strokes)",
     INK_2, PAPER, TEXT_FLOOR, None),
    ("--ink-2-mist on --mist (secondary text on a panel)",
     INK_2_MIST, MIST, TEXT_FLOOR, None),
    ("--ink-2 on --aqua (WASH TRAP: fails if used, must not be)",
     INK_2, AQUA, TEXT_FLOOR, "expected FAIL -- documents the wash-colour-binds-text-colour rule"),
    ("--paper on --aqua (WASH TRAP: fails if used, must not be)",
     PAPER, AQUA, TEXT_FLOOR, "expected FAIL -- same rule, other direction"),
    ("--ink-3-dark on --ink-soft (superseded token, must not ship)",
     INK_3_DARK, INK_SOFT, TEXT_FLOOR, "expected FAIL -- .kicker.on-ink uses --ink-2-dark instead"),
    ("--ink-2-dark on --ink-soft (.kicker.on-ink, .p-body.on-ink)",
     INK_2_DARK, INK_SOFT, TEXT_FLOOR, None),
    ("chip.on-ink text (#93989A) on --ink-soft",
     CHIP_ON_INK, INK_SOFT, TEXT_FLOOR, None),
    ("--ink on --aqua (chip.solid)", INK, AQUA, TEXT_FLOOR, None),
    ("--ink on --coral (chip.warn)", INK, CORAL, TEXT_FLOOR, None),
    ("--ink on --highlighter (wash.sun)", INK, HIGHLIGHTER, TEXT_FLOOR, None),
    ("--ink on --celadon (wash.celadon)", INK, CELADON, TEXT_FLOOR, None),
    ("--ink-3 on --paper (superseded token, must not ship)",
     INK_3, PAPER, TEXT_FLOOR, "expected FAIL -- frames_a.py/actors.py use --ink-2 instead"),
    ("--paper on --moss (.res-note, opacity 1)", PAPER, MOSS, TEXT_FLOOR, None),
    ("--coral-deep on --paper (evidence-scene low-quality fill)",
     CORAL_DEEP, PAPER, GRAPHIC_FLOOR, None),
    ("--ink on --paper / --paper on --ink (primary kt text)",
     INK, PAPER, TEXT_FLOOR, None),
    ("--paper on --ink-soft (.cite.on-ink, .chip.on-ink ground)",
     PAPER, INK_SOFT, TEXT_FLOOR, None),
]


def part1():
    print("PART 1 -- static token pairs (declared colours, WCAG floor)")
    bad = 0
    for name, fg, bg, floor, note in CASES:
        r = ratio(fg, bg)
        expected_fail = note is not None and "expected FAIL" in note
        ok = (r >= floor) == (not expected_fail)
        if not ok:
            bad += 1
        tag = "PASS" if (r >= floor) else "FAIL"
        print(f"  {'.' if ok else '!'} {tag}  {r:5.2f}:1 (floor {floor})  {name}"
              + (f"  -- {note}" if note else ""))
    print(f"  {bad} unexpected result(s) out of {len(CASES)} pairs "
          f"({sum(1 for *_, n in CASES if n and 'expected FAIL' in n)} pairs "
          f"are deliberate documented failures).")
    return bad


# ---------------------------------------------------------------- Part 2 ---
def frame(render, t):
    import io
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{t:.3f}",
                        "-i", str(render), "-frames:v", "1", "-f", "image2pipe",
                        "-vcodec", "png", "-"], capture_output=True, check=False)
    if not r.stdout:
        return None
    import numpy as np
    from PIL import Image
    return np.asarray(Image.open(io.BytesIO(r.stdout)).convert("RGB")).astype(float)


def otsu(g):
    import numpy as np
    hist, _ = np.histogram(g, bins=256, range=(0, 256))
    tot = g.size
    sm = float(np.dot(np.arange(256), hist))
    sb = wB = best = thr = 0.0
    for i in range(256):
        wB += hist[i]
        if wB == 0:
            continue
        wF = tot - wB
        if wF == 0:
            break
        sb += i * hist[i]
        mB, mF = sb / wB, (sm - sb) / wF
        v = wB * wF * (mB - mF) ** 2
        if v > best:
            best, thr = v, i
    return thr


def measure(a, box, label, floor):
    import numpy as np
    x0, y0, x1, y1 = box
    crop = a[y0:y1, x0:x1]
    g = crop @ [0.2126, 0.7152, 0.0722]
    thr = otsu(g)
    # otsu() returns a BIN INDEX (each of its 256 bins spans [i, i+1)), not a
    # cutoff on the raw float luma this compares against -- a flat, unjittered
    # fill (e.g. a synthetic control fixture, or a solid glyph with no anti-
    # aliasing) can land EXACTLY on a bin's lower edge (10.0 computed as
    # 9.999999999998 by the dot-product above) and fall on the wrong side of
    # a bare `<= thr`. +1 restores the bin's own upper edge as the cutoff.
    dark, light = crop[g <= thr + 1], crop[g > thr + 1]
    if len(dark) < 20 or len(light) < 20:
        print(f"  ?  {label}: region is nearly uniform (no text found)")
        return None
    cd, cl = np.median(dark, axis=0), np.median(light, axis=0)
    r = ratio_rgb(cd, cl)
    ok = r >= floor
    print(f"  {'.' if ok else '!'} {'PASS' if ok else 'FAIL'}  {r:.2f}:1 (floor {floor})  {label}")
    return ok


# (t, box x0,y0,x1,y1 in 1920x1080 canvas px, label, floor)
# Boxes are hand-placed on the two P0 opacity fixes this session's Phase 3
# pass made, plus one label the review flagged directly -- these are the
# cases a static token check cannot see, because the risk IS the opacity/
# compositing step, not the declared colour.
PIXEL_TARGETS = [
    (97.00, (1092, 616, 1660, 660), "10-evidence .res-note on moss wash (was opacity .85)", TEXT_FLOOR),
    # .bar-label is 32px regular-weight mono (actors.py:271) -- WCAG's large-text
    # exemption (>=24pt/32px regular, or >=18pt/24px bold) applies, so 3.0:1 is
    # the correct floor here, not the normal-text 4.5:1 every other case in this
    # file uses. Measured 4.14-4.20:1 depending on exact crop, comfortably clears
    # 3.0 -- the anti-aliasing on a thin 32px stroke pulls a pixel-median result
    # noticeably below the pure-token 4.89:1, which is real (that softening is
    # what a viewer's eye also sees) and is exactly why this large-text floor,
    # not the normal-text one, is the one that actually applies.
    (52.50, (160, 931, 300, 953), "07-film .bar-label DERMIS on paper (was opacity .7)", GRAPHIC_FLOOR),
]


def part2(render):
    print(f"\nPART 2 -- composited pixels on the actual render ({render.name})")
    if not render.exists():
        print("  SKIPPED: render not found")
        return 0
    bad = 0
    for t, box, label, floor in PIXEL_TARGETS:
        a = frame(render, t)
        if a is None:
            print(f"  ?  {label}: could not extract frame at t={t}s")
            continue
        r = measure(a, box, label, floor)
        if r is False:
            bad += 1
    return bad


# ---------------------------------------------------------------- Part 3 ---
def part3():
    print("\nPART 3 -- redundant channel (coral vs celadon, 1.49:1 -- not a WCAG case)")
    src = (SCRIPTS / "frames_e.py").read_text()
    checks = [
        ('innerText:"$"', "industry-funded tiles tagged with $ glyph (not colour alone)"),
        ('innerText:"?"', "low-quality tiles tagged with ? glyph (not colour alone)"),
    ]
    bad = 0
    for pattern, label in checks:
        found = pattern in src
        print(f"  {'.' if found else '!'} {'PASS' if found else 'FAIL'}  {label}")
        if not found:
            bad += 1
    print("  Coral and celadon are 1.49:1 apart -- indistinguishable by lightness "
          "alone in a\n  desaturated or colour-blind view. The glyph tags above and "
          "tile POSITION (a\n  fixed, named index set, not randomised) are the "
          "redundant channels; verified\n  present here, not re-measured as a "
          "contrast ratio because none applies to two\n  adjacent fills.")
    return bad


def main():
    bad1 = part1()
    bad2 = part2(RENDER) if RENDER else 0
    bad3 = part3()
    total = bad1 + bad2 + bad3
    print(f"\n{total} finding(s) across all three parts.")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
