#!/usr/bin/env python3
"""Measure text contrast from ACTUAL RENDERED PIXELS, not declared CSS colours.

WHY THIS EXISTS. A stylesheet-reading contrast check evaluates the DECLARED
foreground and background colours. That makes it blind in two directions at
once, and both have shipped:

  * it cannot see what a photographic plate, a scrim, an opacity tween or a
    blend layer actually puts behind the type. `videos/ectoin-survival-molecule`
    shipped three scenes at ~1.3:1 -- paper-white type rendering as UA-default
    black, because a wrapper appended `#root { color:inherit }` after each
    scene's own root rule. The declared colour in the source was still correct.
    `hyperframes check` reported 16/16 contrast checks passing on that master.
  * it samples an element regardless of whether that element is currently
    CLIPPED. `videos/exosome-label-problem` had three reveal-bar spans measured
    mid-wipe, while their `overflow:hidden` bar was ~15px wide, and reported the
    text against a page ground it never renders on -- 1:1 and 2.02:1 readings
    for text that is 16.1:1 and 8.4:1 once the bar is open.

Neither is visible by reading the source, and neither is visible to an eye
skimming the render. It takes measuring the pixels.

METHOD. Crop the region, split its pixels into a dark cluster and a light
cluster by Otsu threshold, take each cluster's median colour, and compute the
WCAG ratio between them. That is the contrast a viewer actually sees.

A probe that finds NO TEXT is a failure, not a pass. A stale box that has
drifted off its element is the failure mode this gate is most likely to
develop, and reporting it as "clean" is how it would stop protecting anything.

FIELD CONTRACT
    python3 check-contrast-pixels.py <render.mp4> --probes <probes.json>
                                     [--scene-map <scenes.json> | --project-root <dir>]
                                     [--normal-floor 4.5] [--large-floor 3.0]

probes.json is a list of probe objects. Time is given ONE of two ways:

    {"t": 211.0,                      "box": [96, 330, 1824, 500],
     "label": "19 headline on ink",   "floor": "large"}

    {"cid": "19-limits", "offset": 2.6, "box": [96, 330, 1824, 500],
     "label": "19 headline on ink",   "floor": "large"}

`cid` + `offset` is strongly preferred and is why this gate outlived a re-time
on the project it came from: an absolute second is correct for exactly one cut,
and a probe table pinned to wall-clock silently samples the wrong scene the
first time anything upstream changes length. Scene starts come from
--scene-map (a {cid: start_seconds} JSON) or are parsed out of
<project-root>/index.html, the same source check-static-hold.py reads.

`floor` is "normal" (4.5:1), "large" (3.0:1 -- >=24px bold or >=30px regular),
or a number. Boxes are [x0, y0, x1, y1] in the render's own pixels.

BOXES ARE THE HARD PART, and two lessons are worth stating because both cost a
render cycle to learn:

  * a box that spans a coloured RULE or FILL as well as the type is split by
    Otsu into rule-vs-card, and measures a pair nobody cares about. Band the
    box to rows that hold only the text.
  * a box that extends past a backing panel's edge onto a bright plate is split
    into panel-vs-plate for the same reason. Inset it.

A `?` line (no text found) means one of those, or a probe timed before its
element enters. Fix the probe, do not raise the floor.

Exits non-zero on any probe below its floor or any probe that found no text --
a HARD gate, like check-safe-area.py and unlike the advisory check-*.py here.

Provenance: `videos/exosome-label-problem` (the Otsu/median core and the
fill-anchored box search), `videos/ectoin-survival-molecule` (the cid+offset
probe schema, the no-text-is-a-failure rule, the RGB readout) and
`videos/collagen-where-did-it-go` (the bin-edge fix below, without which a
synthetic control fixture mis-splits).
"""
import argparse
import io
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

NORMAL_FLOOR, LARGE_FLOOR = 4.5, 3.0
MIN_CLUSTER_PX = 20          # below this a "cluster" is noise, not a population


def frame(render, t):
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{t:.3f}",
                        "-i", str(render), "-frames:v", "1", "-f", "image2pipe",
                        "-vcodec", "png", "-"], capture_output=True, check=False)
    if not r.stdout:
        sys.exit(f"FATAL: could not extract a frame at t={t:.3f} from {render}")
    return np.asarray(Image.open(io.BytesIO(r.stdout)).convert("RGB")).astype(float)


def lin(c):
    c = c / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def luminance(rgb):
    r, g, b = lin(np.array(rgb, dtype=float))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio_rgb(c1, c2):
    a, b = luminance(c1), luminance(c2)
    hi, lo = max(a, b), min(a, b)
    return float((hi + 0.05) / (lo + 0.05))


def ratio(hex1, hex2):
    """WCAG ratio between two #rrggbb strings. Exposed for control fixtures."""
    def rgb(h):
        h = h.lstrip("#")
        return [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    return ratio_rgb(rgb(hex1), rgb(hex2))


def otsu(g):
    """Otsu threshold as a BIN INDEX over 256 bins spanning [i, i+1)."""
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


def measure(a, box, label, floor, t=None):
    """-> True (pass) / False (below floor) / None (no text found)."""
    x0, y0, x1, y1 = box
    crop = a[y0:y1, x0:x1]
    if crop.size == 0:
        print(f"  ?  {label}: box {box} is empty for this frame size {a.shape[1]}x{a.shape[0]}")
        return None
    g = crop @ [0.2126, 0.7152, 0.0722]
    thr = otsu(g)
    # otsu() returns a BIN INDEX, not a cutoff on the raw float luma this
    # compares against. A flat, unjittered fill -- a synthetic control fixture,
    # or a solid glyph with no antialiasing -- can land EXACTLY on a bin's lower
    # edge (10.0 computed as 9.999999999998 by the dot product above) and fall
    # on the wrong side of a bare `<= thr`. +1 restores the bin's upper edge.
    dark, light = crop[g <= thr + 1], crop[g > thr + 1]
    if len(dark) < MIN_CLUSTER_PX or len(light) < MIN_CLUSTER_PX:
        at = "" if t is None else f" at t={t:.2f}s"
        print(f"  ?  {label}: region is nearly uniform{at} -- no text found. Either "
              f"the element has not entered yet or the box has drifted off it.")
        return None
    cd, cl = np.median(dark, axis=0), np.median(light, axis=0)
    # float(), not the raw numpy scalar: an np.bool_ fails an `is False`
    # identity test, which is how a caller once printed FAIL and exited 0.
    r = float(ratio_rgb(cd, cl))
    ok = bool(r >= floor)
    at = "" if t is None else f"  t={t:7.2f}s"
    print(f"  {'PASS' if ok else 'FAIL'}  {r:6.2f}:1 (floor {floor})  {label:44s}{at}  "
          f"ink=({cd[0]:.0f},{cd[1]:.0f},{cd[2]:.0f}) "
          f"ground=({cl[0]:.0f},{cl[1]:.0f},{cl[2]:.0f})")
    return ok


def scene_starts(scene_map, project_root):
    if scene_map:
        return {k: float(v) for k, v in json.loads(Path(scene_map).read_text()).items()}
    if not project_root:
        return {}
    html = (Path(project_root) / "index.html").read_text()
    # Match on the ATTRIBUTES, never on their order: this repo's preview server
    # injects data-hf-id as the first attribute on every tag, and a pattern
    # anchored to the tag's opening bytes silently stops matching.
    return {cid: float(t) for cid, t in re.findall(
        r'data-composition-id="([^"]+)"[^>]*?data-start="([0-9.]+)"', html)}


def resolve_floor(v, normal, large):
    if isinstance(v, (int, float)):
        return float(v)
    return {"normal": normal, "large": large}.get(str(v).lower(), normal)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("render")
    ap.add_argument("--probes", required=True)
    ap.add_argument("--scene-map")
    ap.add_argument("--project-root")
    ap.add_argument("--normal-floor", type=float, default=NORMAL_FLOOR)
    ap.add_argument("--large-floor", type=float, default=LARGE_FLOOR)
    a = ap.parse_args()

    render = Path(a.render)
    if not render.exists():
        sys.exit(f"FATAL: render not found: {render}")
    probes = json.loads(Path(a.probes).read_text())
    starts = scene_starts(a.scene_map, a.project_root)

    print(f"[contrast] measuring rendered pixels in {render.name} "
          f"({len(probes)} probe(s))")
    results = []
    for p in probes:
        if "t" in p:
            t = float(p["t"])
        else:
            cid = p["cid"]
            if cid not in starts:
                sys.exit(f"FATAL: probe names scene {cid!r}, which is not in the "
                         f"scene map. Pass --scene-map or --project-root.")
            t = starts[cid] + float(p.get("offset", 0.0))
        floor = resolve_floor(p.get("floor", "normal"), a.normal_floor, a.large_floor)
        results.append(measure(frame(render, t), p["box"], p["label"], floor, t))

    bad = [r for r in results if r is not None and not r]
    miss = [r for r in results if r is None]
    print(f"[contrast] {len(bad)} below floor, {len(miss)} probe(s) found no text")
    return 1 if (bad or miss) else 0


if __name__ == "__main__":
    sys.exit(main())
