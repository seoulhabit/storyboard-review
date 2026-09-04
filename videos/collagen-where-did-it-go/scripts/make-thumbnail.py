#!/usr/bin/env python3
"""Extract, grade and finalise the thumbnail from the finished render.

Extract-grade-finalize, which is the house path (see
videos/exosome-label-decode/assets/thumbnail/README.md): the composition already
puts the hero object and a legible line in one frame, so a separately authored
asset is not needed.

Two rules this enforces rather than trusting:
  * candidates are judged at GRID scale (a 5x downscale), not at full size --
    a thumbnail is browsed at ~120x67 before anyone opens it;
  * the grade is re-derived for THIS video's palette. A prior video's
    vignette-and-curve chain reads as a muddy cast on a different ground.
"""
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "thumbnail"
RENDER = ROOT / "renders" / "collagen-where-did-it-go_final.mp4"

# (slug, timestamp, what it is testing)
CANDIDATES = [
    ("a-cold-open",  2.60,   "the title question, literally: an oversized molecule at a door too small for it"),
    ("b-rejected",   48.74,  "the strongest single claim -- REJECTED, with both size numbers on screen"),
    ("c-four-left",  118.82, "the evidence payoff, on the inverted ground: 23 -> 4"),
]
# Light grade, re-derived for this palette: flat warm ivory, one coral accent.
# No vignette -- the ground is deliberately flat and a vignette muddies it.
GRADE = "eq=contrast=1.06:saturation=1.10,unsharp=5:5:0.45:5:5:0.0"


def run(*a):
    subprocess.run(list(a), check=True, capture_output=True)


def main():
    if not RENDER.exists():
        sys.exit(f"render not found: {RENDER}")
    OUT.mkdir(parents=True, exist_ok=True)
    for slug, t, why in CANDIDATES:
        src = OUT / f"candidate-{slug}-source.png"
        gra = OUT / f"candidate-{slug}-graded.png"
        grd = OUT / f"candidate-{slug}-grid-check.png"
        run("ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", str(RENDER),
            "-frames:v", "1", str(src))
        run("ffmpeg", "-y", "-v", "error", "-i", str(src), "-vf", GRADE, str(gra))
        # 1280x720 is the upload size; the grid check is what the decision is made on
        run("ffmpeg", "-y", "-v", "error", "-i", str(gra),
            "-vf", "scale=1280:720", str(OUT / f"candidate-{slug}-1280.png"))
        run("ffmpeg", "-y", "-v", "error", "-i", str(gra),
            "-vf", "scale=256:144:flags=area", str(grd))
        print(f"  {slug:14s} t={t:7.2f}s  {why}")
    # contact sheet of the three grid-scale checks, which is how the pick is made
    run("ffmpeg", "-y", "-v", "error",
        "-i", str(OUT / "candidate-a-cold-open-grid-check.png"),
        "-i", str(OUT / "candidate-b-rejected-grid-check.png"),
        "-i", str(OUT / "candidate-c-four-left-grid-check.png"),
        "-filter_complex", "[0][1][2]hstack=inputs=3,scale=iw*2:ih*2:flags=neighbor",
        str(OUT / "grid-check-contact.png"))
    print(f"\n  grid-scale contact sheet: {OUT / 'grid-check-contact.png'}")


if __name__ == "__main__":
    main()
