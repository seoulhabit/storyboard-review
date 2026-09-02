#!/usr/bin/env python3
"""Measure text contrast from ACTUAL RENDERED PIXELS, not declared CSS colours.

Why this exists. The engine's own contrast pass evaluates the declared
foreground/background colours in the stylesheet. That makes it blind in one
direction (it cannot see what a photographic plate, scrim or blend layer
actually puts behind text) and wrong in the other: it samples an element at a
fixed timestamp regardless of whether that element is currently CLIPPED. On
this project it sampled three reveal-bar spans mid-wipe, while their
overflow:hidden bar was ~15px wide, and reported the text against the page
ground it never actually renders on -- 1:1 and 2.02:1 readings for text that
is 16.1:1 and 8.4:1 once the bar is open.

Method: crop the region, split its pixels into a dark cluster and a light
cluster by Otsu threshold, take each cluster's median colour, and compute the
WCAG ratio between them. That is the contrast a viewer actually sees.
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image


def frame(render, t):
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{t:.3f}",
                        "-i", str(render), "-frames:v", "1", "-f", "image2pipe",
                        "-vcodec", "png", "-"], capture_output=True, check=False)
    if not r.stdout:
        sys.exit(f"FATAL: could not extract frame at t={t}")
    import io
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
    tot = g.size; sm = np.dot(np.arange(256), hist)
    sb = wB = best = thr = 0.0
    for i in range(256):
        wB += hist[i]
        if wB == 0: continue
        wF = tot - wB
        if wF == 0: break
        sb += i * hist[i]
        mB = sb / wB; mF = (sm - sb) / wF
        v = wB * wF * (mB - mF) ** 2
        if v > best: best, thr = v, i
    return thr

def measure(render, t, box, label, floor):
    a = frame(render, t)
    x0, y0, x1, y1 = box
    crop = a[y0:y1, x0:x1]
    g = (crop @ [0.2126, 0.7152, 0.0722])
    thr = otsu(g)
    dark = crop[g <= thr]; light = crop[g > thr]
    if len(dark) < 20 or len(light) < 20:
        print(f"  ? {label}: region is nearly uniform (no text found) at t={t}")
        return None
    cd = np.median(dark, axis=0); cl = np.median(light, axis=0)
    r = ratio(cd, cl)
    ok = r >= floor
    print(f"  {'✓' if ok else '✗'} {label}: {r:.2f}:1 (floor {floor}) at t={t}s  "
          f"ink=({cd[0]:.0f},{cd[1]:.0f},{cd[2]:.0f}) ground=({cl[0]:.0f},{cl[1]:.0f},{cl[2]:.0f})")
    return ok

# Locate each bar by its OWN fill colour rather than a hardcoded box. Two of
# the round-3 probes missed their target with fixed coordinates -- one caught
# the coral bar's edge against the page and reported the bar-vs-page ratio
# instead of the text-vs-bar ratio it was meant to measure, and one landed on
# empty ground and reported "no text found". Anchoring on the fill makes the
# probe follow the element wherever it actually rendered.
TARGETS = [
    # (t, fill rgb, tolerance, label, floor, y-band to search within)
    # The band matters: scene 05 paints its wall channels in the SAME coral as
    # its refusal bar, so an unconstrained search bounded both together and
    # measured coral against the paper between them instead of the bar's own
    # ink text. Each probe is restricted to the band its element occupies.
    # 07-verdict and 08-endcard carry no ink-filled reveal bar (the sign-off
    # became the end card's brand lockup in round 2), so there is nothing for a
    # fill-anchored probe to find there; every filled bar in the piece is below.
    ( 3.20, (19, 21, 22),    26, "01 payoff bar (paper on ink)",              4.5, (380, 700)),
    (19.60, (19, 21, 22),    26, "03a tag bar (paper on ink)",                4.5, (1300, 1545)),
    (23.60, (19, 21, 22),    26, "03b verdict bar (paper on ink)",            4.5, (980, 1420)),
    (47.10, (201, 122, 92),  34, "05b refusal bar (ink on coral)",            4.5, (1000, 1420)),
    # 05a's coral stamp, banded BELOW the wall: that scene paints its puncture
    # channels in the same coral, so an unbanded search would bound both.
    (42.40, (201, 122, 92),  34, "05a barrier-opened stamp (ink on coral)",    4.5, (1380, 1540)),
]

def find_fill(a, rgb, tol, band=None):
    """Largest solid run of a given fill inside `band` -> its bounding box."""
    m = (np.abs(a - np.array(rgb, dtype=float)).max(axis=2) <= tol)
    if band:
        keep = np.zeros(m.shape[0], dtype=bool); keep[band[0]:band[1]] = True
        m = m & keep[:, None]
    rows = np.where(m.sum(1) > 60)[0]
    cols = np.where(m.sum(0) > 20)[0]
    if rows.size < 10 or cols.size < 40:
        return None
    return int(cols.min()), int(rows.min()), int(cols.max()) + 1, int(rows.max()) + 1

def main():
    render = Path(sys.argv[1] if len(sys.argv) > 1 else "renders/exosome-label-problem.mp4")
    if not render.exists(): sys.exit(f"FATAL: render not found: {render}")
    print(f"[contrast] measuring rendered pixels in {render}")
    results = []
    for t, rgb, tol, label, floor, band in TARGETS:
        a = frame(render, t)
        box = find_fill(a, rgb, tol, band)
        if box is None:
            print(f"  ? {label}: fill {rgb} not found at t={t}s -- element may not "
                  f"have rendered, or the probe timestamp is mid-reveal")
            results.append(None); continue
        # inset so the bar's own border/edge is excluded from the two clusters
        x0, y0, x1, y1 = box
        pad = 6
        results.append(measure(render, t, (x0+pad, y0+pad, x1-pad, y1-pad), label, floor))
    bad = [r for r in results if r is False]
    print(f"[contrast] {len(bad)} below floor")
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
