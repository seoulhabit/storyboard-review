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
import shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "thumbnail"
RENDER = ROOT / "renders" / "collagen-where-did-it-go_final.mp4"

# (slug, timestamp, what it is testing)
#
# Re-chosen for the 2:14.90 single-narrator cut. The previous set was framed on
# the 3:09 two-voice cut and its winner sat at t=2.60s on a cold open this build
# does not have. The title beside the thumbnail is "You Bought Collagen. Where
# Did It Actually Go?", so a candidate that restates the question spends its one
# frame on something the viewer has already read: every candidate here answers.
CANDIDATES = [
    ("a-not-replace",   4.60, "the contradiction: cream and powder beside a molecule that does NOT replace"),
    ("b-uv-cuts",      29.00, "the cause, in the only black-on-yellow block in the piece: UV cuts collagen"),
    ("c-rejected",     47.80, "the refusal: REJECTED over a coral barrier, with both size numbers"),
    ("d-effect-stops", 101.60, "the verdict, in the largest type in the video: THE EFFECT STOPS SHOWING UP"),
    ("e-protect",     128.60, "the payoff: the ranked list under Protect the building first."),
]

# d's timestamp is pinned inside a 0.8s window and is not a round number by
# accident. The kinetic word "UP" is still grey until 101.10 (it fades to black
# over the preceding beat, and a half-set word reads as a rendering fault in a
# still), and "works?" starts fading in underneath at 101.95. Outside
# 101.15-101.95 the frame carries a visible defect. Measured, not eyeballed.

# The candidate that ships. Naming it here rather than in the README means the
# shipped file cannot drift from the decision: the previous README said
# thumbnail-final.png was "a copy of candidate-b-rejected-1280.png" and left the
# copying to a human to remember.
WINNER = "d-effect-stops"

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
        # 120x67 is the size a thumbnail is actually browsed at. The README
        # claimed the call was made here as well as at 256x144, but no file at
        # this size was ever written. Write it -- it changes the answer.
        run("ffmpeg", "-y", "-v", "error", "-i", str(gra),
            "-vf", "scale=120:67:flags=area", str(OUT / f"candidate-{slug}-feed-check.png"))
        print(f"  {slug:14s} t={t:7.2f}s  {why}")
    # contact sheets at both judging sizes, which is how the pick is made
    def sheet(suffix, zoom, dest):
        ins = []
        for slug, _, _ in CANDIDATES:
            ins += ["-i", str(OUT / f"candidate-{slug}-{suffix}.png")]
        filt = "".join(f"[{i}]" for i in range(len(CANDIDATES))) + \
            f"hstack=inputs={len(CANDIDATES)},scale=iw*{zoom}:ih*{zoom}:flags=neighbor"
        run("ffmpeg", "-y", "-v", "error", *ins, "-filter_complex", filt, str(OUT / dest))

    sheet("grid-check", 2, "grid-check-contact.png")
    sheet("feed-check", 4, "feed-check-contact.png")
    shutil.copyfile(OUT / f"candidate-{WINNER}-1280.png", OUT / "thumbnail-final.png")
    print(f"\n  ships: thumbnail-final.png  <- candidate-{WINNER}-1280.png")
    print(f"  judged on: grid-check-contact.png (256x144) and feed-check-contact.png (120x67)")


if __name__ == "__main__":
    main()
