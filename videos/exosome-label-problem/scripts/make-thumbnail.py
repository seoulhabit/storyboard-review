#!/usr/bin/env python3
"""Extract, grade and grid-check thumbnail candidates from the finished render.

Path chosen: EXTRACT-GRADE-FINALIZE. The render already contains frames where
the hero and a legible headline share the frame, so a separately authored
still isn't needed.

Every candidate is pulled at a SETTLED moment -- never mid-wipe, mid-tween or
mid-crossfade, which is the thumbnail form of the transition-midpoint defect.
The grade is re-derived for this video's own paper/ink palette rather than
copied from a sibling: a curve tuned for a different ground reads as a cast.

Each candidate is also written at ~68x120 feed-grid scale and re-upscaled 5x,
because that is the size the click decision is actually made at.
"""
import io
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageEnhance

RENDER = Path(sys.argv[1] if len(sys.argv) > 1 else "renders/exosome-label-problem.mp4")
OUT = Path("assets/thumbnail"); OUT.mkdir(parents=True, exist_ok=True)

# (name, timestamp, what it is testing) -- all settled moments
CANDIDATES = [
    ("hook-payoff",  3.30, "EXOSOME + payoff bar + bottle, the hook fully composed"),
    ("triptych",    19.60, "three materials + 'three different starting materials' tag"),
    ("barrier",     42.60, "breached wall, shards fallen, barrier-opened stamp"),
    ("questions",   57.00, "the three-question checklist, all gates open"),
    ("endcard",     66.60, "습 brand lockup + verdict + hero bottle"),
]

def frame(t):
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{t:.3f}",
                        "-i", str(RENDER), "-frames:v", "1", "-f", "image2pipe",
                        "-vcodec", "png", "-"], capture_output=True, check=False)
    return Image.open(io.BytesIO(r.stdout)).convert("RGB")

def grade(im):
    # Light, palette-specific: this piece is a warm paper ground with near-black
    # ink. It needs separation, not saturation -- pushing colour would tint the
    # paper. Contrast 1.06, colour 1.04, a touch of sharpening.
    im = ImageEnhance.Contrast(im).enhance(1.06)
    im = ImageEnhance.Color(im).enhance(1.04)
    return ImageEnhance.Sharpness(im).enhance(1.25)

for name, t, note in CANDIDATES:
    src = frame(t)
    src.save(OUT / f"candidate-{name}-source.png")
    g = grade(src)
    g.save(OUT / f"candidate-{name}-graded.png")
    grid = g.resize((68, 120), Image.LANCZOS)
    grid.save(OUT / f"candidate-{name}-grid-check.png")
    grid.resize((340, 600), Image.NEAREST).save(OUT / f"candidate-{name}-grid-check-5x.png")
    print(f"  {name:14s} t={t:6.2f}s  {note}")
print(f"\n{len(CANDIDATES)} candidates written to {OUT}/")
