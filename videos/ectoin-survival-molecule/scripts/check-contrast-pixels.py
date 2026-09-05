#!/usr/bin/env python3
"""Measure text contrast from ACTUAL RENDERED PIXELS, not declared CSS colours.

WHY THIS EXISTS, on this project specifically. `hyperframes check` evaluates the
declared foreground/background colours in the stylesheet and reported 16/16
contrast checks passing on a master that shipped three scenes at ~1.3:1. The
cause was a wrapper appending `#root { color:inherit }` AFTER each scene's own
root rule: the declared colour in the source was still --paper, and the computed
colour in the browser was the UA default black on a near-black ground. No
stylesheet-reading tool can see that, and no eye reading the source would either.
It took extracting frames from the shipped MP4.

Method: crop the region, split its pixels into a dark cluster and a light
cluster by Otsu threshold, take each cluster's median colour, and compute the
WCAG ratio between them. That is the contrast a viewer actually sees.

Core ported from videos/exosome-label-problem/scripts/check-contrast-pixels.py;
TARGETS is this piece's own geometry.

  python3 scripts/check-contrast-pixels.py [render.mp4]
"""
import io
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from timing import walk

AA_NORMAL = 4.5
AA_LARGE = 3.0     # >=24px bold or >=30px regular; every "large" probe here is 48px+


def frame(render, t):
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{t:.3f}",
                        "-i", str(render), "-frames:v", "1", "-f", "image2pipe",
                        "-vcodec", "png", "-"], capture_output=True, check=False)
    if not r.stdout:
        sys.exit(f"FATAL: could not extract frame at t={t}")
    return np.asarray(Image.open(io.BytesIO(r.stdout)).convert("RGB")).astype(float)


def lin(c):
    c = c / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def L(rgb):
    r, g, b = lin(np.array(rgb, dtype=float))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(c1, c2):
    a, b = L(c1), L(c2)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def otsu(g):
    hist, _ = np.histogram(g, bins=256, range=(0, 256))
    tot = g.size
    sm = np.dot(np.arange(256), hist)
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


def measure(a, box, label, floor, t):
    x0, y0, x1, y1 = box
    crop = a[y0:y1, x0:x1]
    g = crop @ [0.2126, 0.7152, 0.0722]
    thr = otsu(g)
    dark, light = crop[g <= thr], crop[g > thr]
    if len(dark) < 40 or len(light) < 40:
        print(f"  ?  {label}: region is nearly uniform at t={t}s -- no text found. "
              f"Either the element has not entered yet or the probe box is wrong.")
        return None
    cd, cl = np.median(dark, axis=0), np.median(light, axis=0)
    r = float(ratio(cd, cl))
    # float(), not the raw numpy scalar. `ok` was an np.bool_ and main()'s
    # `r is False` identity test never matched it, so the gate printed FAIL on
    # four probes and then exited 0. A gate that reports and passes is worse
    # than no gate.
    ok = bool(r >= floor)
    print(f"  {'PASS' if ok else 'FAIL'}  {r:6.2f}:1 (floor {floor})  {label:44s} "
          f"t={t:7.2f}s  ink=({cd[0]:.0f},{cd[1]:.0f},{cd[2]:.0f}) "
          f"ground=({cl[0]:.0f},{cl[1]:.0f},{cl[2]:.0f})")
    return ok


# (scene, offset into the scene, box, label, floor)
#
# Offsets are into the SCENE, not the piece, so the table survives a re-time --
# the whole point of the walk. Every probe here is a state the 2026-09-05 review
# named, plus the states that were dimmed as a signal, sampled while dimmed.
TARGETS = [
    ("01-hook",       5.60, (1100, 175, 1760, 300), "01 NOT THIS label on plate",        AA_NORMAL),
    ("05-halomonas",  4.40, (96, 330, 980, 760),    "05 Halomonas name + note on deck",  AA_LARGE),
    ("07-question",   8.60, (140, 730, 1150, 950),  "07 closing question on deck",       AA_LARGE),
    ("08-humectant", 11.00, (96, 560, 900, 900),    "08 humectant card while dimmed",    AA_NORMAL),
    ("09-exclusion",  6.00, (140, 300, 760, 800),   "09 paper world on deck",            AA_NORMAL),
    ("09-exclusion", 24.00, (96, 300, 900, 830),    "09 ink world note while dimmed",    AA_NORMAL),
    ("19-limits",     2.60, (96, 330, 1824, 500),   "19 headline on ink",                AA_LARGE),
    ("19-limits",     6.80, (96, 470, 1824, 720),   "19 claim cards after the strike",   AA_NORMAL),
    ("21-verdict",    5.00, (96, 230, 1824, 430),   "21 bitop / Merck / Kao tiles",      AA_NORMAL),
    ("21-verdict",    9.20, (200, 480, 1720, 900),  "21 verdict panel on the moss wash", AA_LARGE),
    ("23-numbers",    4.00, (96, 240, 980, 420),    "23 headline serif on plate",        AA_LARGE),
    ("23-numbers",   13.50, (96, 700, 980, 900),     "23 brand card name row",            AA_NORMAL),
    ("24-eleven",     3.20, (96, 100, 1824, 300),   "24 carry row while inactive",       AA_NORMAL),
    ("24-eleven",    12.00, (990, 385, 1800, 700),  "24 ingredient list",                AA_NORMAL),
    # banded to rows 3-10, so the two aqua-filled rows are not what Otsu
    # splits on -- the question is whether the DIMMED list is readable.
    ("24-eleven",    17.50, (990, 385, 1800, 700),  "24 ingredient list while dimmed",   AA_NORMAL),
    # banded to the kicker + label rows: a box spanning the strike itself is
    # split by Otsu into bar-vs-card and measures the wrong pair.
    ("26-kbeauty",    7.50, (170, 400, 1180, 460),  "26 negated claim kicker",           AA_NORMAL),
    ("26-kbeauty",    7.50, (170, 530, 1180, 590),  "26 NOT TRUE label",                 AA_NORMAL),
    ("26-kbeauty",    9.00, (140, 700, 1180, 950),   "26 true claim on ink card",         AA_LARGE),
    ("27-resilience", 14.00, (120, 800, 660, 990),   "27 'from' panel while dimmed",      AA_NORMAL),
    ("28-remember",  10.00, (96, 640, 1400, 980),   "28 closing line on montage",        AA_LARGE),
    ("30-endcard",    2.40, (96, 380, 1180, 700),   "30 end card handle",                AA_LARGE),
]


def main():
    render = Path(sys.argv[1] if len(sys.argv) > 1
                  else "renders/ectoin-survival-molecule_a11y-master.mp4")
    if not render.exists():
        sys.exit(f"FATAL: render not found: {render}")
    starts = {s.cid: s.start for s in walk()[0]}
    print(f"[contrast] measuring rendered pixels in {render.name}")
    results = []
    for cid, off, box, label, floor in TARGETS:
        if cid not in starts:
            sys.exit(f"FATAL: probe names scene {cid}, which is not in the walk")
        t = starts[cid] + off
        results.append(measure(frame(render, t), box, label, floor, t))
    bad = [r for r in results if r is not None and not r]
    miss = [r for r in results if r is None]
    print(f"[contrast] {len(bad)} below floor, {len(miss)} probe(s) found no text")
    return 1 if (bad or miss) else 0


if __name__ == "__main__":
    sys.exit(main())
