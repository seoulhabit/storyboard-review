#!/usr/bin/env python3
"""Which caption band is emptier, per scene, measured on the render.

build_captions.TOP_CUE_SCENES started as a hand-authored guess from reading the
scene sources, and it was wrong for half the piece -- this is a full-frame
editorial layout, not a lower-third one, and several scenes hold a 36px kicker
just under the safe line where a top caption lands straight on it.

Method: four frames per scene; in each of the two bands a caption can occupy,
take the 99.9th-percentile local luma gradient. Text has sharp edges at this
scale and a photographic plate does not, so the gradient separates "there is
type here" from "there is a photograph here" -- which is the question, since a
caption over a plate is fine and a caption over a label is not.

    python3 scripts/measure_cue_bands.py renders/<file>.mp4

Paste the printed table into build_captions.TOP_CUE_SCENES.
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

TOP_BAND = (162, 330)      # matches build_captions.VTT_TOP (line:15%)
BOTTOM_BAND = (840, 1000)  # matches build_open_captions.SAFE_BOTTOM
X0, X1 = 300, 1620         # ignore the outer columns; a caption is centred
MARGIN = 12                # top must be clearly emptier, not marginally


def frame(render, t):
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{t:.3f}",
                        "-i", str(render), "-frames:v", "1", "-f", "image2pipe",
                        "-vcodec", "png", "-"], capture_output=True)
    if not r.stdout:
        sys.exit(f"FATAL: could not extract frame at t={t}")
    return np.asarray(Image.open(io.BytesIO(r.stdout)).convert("RGB")).astype(float)


def sharpness(a):
    g = a @ [0.2126, 0.7152, 0.0722]
    return max(float(np.percentile(np.abs(np.diff(g, axis=1)), 99.9)),
               float(np.percentile(np.abs(np.diff(g, axis=0)), 99.9)))


def main():
    render = Path(sys.argv[1] if len(sys.argv) > 1
                  else "renders/ectoin-survival-molecule_a11y-master.mp4")
    if not render.exists():
        sys.exit(f"FATAL: render not found: {render}")
    rows = []
    print(f"  {'scene':16s} {'top':>6s} {'bottom':>7s}   place")
    for s in walk()[0]:
        t_vals, b_vals = [], []
        for f in (0.25, 0.45, 0.65, 0.85):
            a = frame(render, s.start + s.dur * f)
            t_vals.append(sharpness(a[TOP_BAND[0]:TOP_BAND[1], X0:X1]))
            b_vals.append(sharpness(a[BOTTOM_BAND[0]:BOTTOM_BAND[1], X0:X1]))
        t, b = max(t_vals), max(b_vals)
        top = t + MARGIN < b
        rows.append((s.cid, round(t), round(b), top))
        print(f"  {s.cid:16s} {t:6.1f} {b:7.1f}   {'top' if top else 'bottom'}")
    print("\nTOP_CUE_SCENES = {")
    for cid, t, b, top in rows:
        if top:
            print(f'    "{cid}": ({t}, {b}),')
    print("}")


if __name__ == "__main__":
    main()
