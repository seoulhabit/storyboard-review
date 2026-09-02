#!/usr/bin/env python3
"""Measure state-change CADENCE on a rendered MP4 — a different question from
check-static-hold.py, and one that script cannot answer.

check-static-hold.py asks "is anything frozen?" via a PSNR threshold
(PSNR_FROZEN_DB) that only fires on near-pixel-identical consecutive samples.
A scene can report 0 findings there while carrying no meaningful motion at all,
because sub-perceptual drift — a slow Ken Burns, an easing tail, antialiasing
noise — keeps breaking the "frozen" run before it reaches the cadence ceiling.
"Not frozen" and "adequately paced" are not the same measurement.

So: sample at ~8fps, compute mean |delta luma| per step across the whole frame,
and count what fraction of steps clear a real-but-low threshold. Hard cuts are
excluded from the active count — a cut can measure 100+ and would otherwise let
six cuts stand in for an entire video's cadence.

The burned-in caption band is cropped out before differencing. Its 27 cues
repaint constantly and would register as motion in every scene, which is the
exact masking effect that makes a whole-frame diff read "alive" over a dead
scene.

Advisory (always exits 0) — cadence is a judgement call in a way a safe-area
intrusion is not.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import numpy as np
    from PIL import Image
except ImportError:
    print("check-cadence: needs `python3 -m pip install pillow numpy` — skipping.")
    sys.exit(0)

SAMPLE_FPS = 8
CANVAS_W, CANVAS_H = 1080, 1920

# Caption band, re-derived from THIS project's index.html (.vo-caption
# top:1360px height:160px). Same discipline as check-static-hold.py.
CAPTION_BAND_TOP, CAPTION_BAND_BOTTOM = 1360, 1520

# CALIBRATED 2026-09-02 against this render, after the first version of this
# script produced a FALSE POSITIVE and had to be checked against actual frames.
#
# The first version used mean |dLuma| >= 1.0 (the skill's suggested starting
# point) and reported 4% active with an 11.5s "frozen" run in scene 04 --
# alarming, and wrong. Measuring known authored beats showed why: a gate
# activation (an 8px bar plus a line of text) changes ~4,000-8,000 px out of
# 1.47M, which is a mean |dLuma| of only 0.14-0.28. The 1.0 threshold was
# scoring real beats as dead.
#
# CHANGED-PIXEL COUNT separates cleanly and is scale-invariant:
#     genuinely frozen step -> 0 changed px (exactly zero, not drift)
#     real authored beat    -> 4,000-8,000
# so 800 sits in an empty gap between the two populations rather than inside
# one of them. Re-measure this gap if the design's beat size changes.
ACTIVE_PX = 800           # changed px (|dLuma| > 12) for a step to count as a beat
PIXEL_DELTA = 12          # per-pixel luma change that counts as "changed"
CUT_PX = 300000           # at/above this the step is a hard scene cut, not in-scene motion
LOW_SHARE_WARN = 0.15     # whole-video active-step share below this is worth a second look

# Scene boundaries from index.html (start, end, id) — a per-scene read is what
# actually matters; a healthy whole-video number can hide one dead scene.
SCENES = [
    (0.000,  4.450, "01-hook"),
    (4.450, 15.200, "02-what"),
    (15.200, 28.000, "03-evidence"),
    (28.000, 40.700, "04-questions"),
    (40.700, 48.250, "05-claim"),
    (48.250, 55.800, "06-close"),
    (55.800, 59.000, "07-endcard"),
]


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    render = sys.argv[2] if len(sys.argv) > 2 else None
    if render:
        render = Path(render)
        if not render.is_absolute():
            render = root / render
    else:
        c = sorted(root.glob("renders/*.mp4"))
        render = c[-1] if c else None
    if not render or not render.exists():
        print("check-cadence: no render found — skipping.")
        return 0

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        top_h = CAPTION_BAND_TOP
        bot_h = CANVAS_H - CAPTION_BAND_BOTTOM
        filt = (
            f"[0:v]fps={SAMPLE_FPS},crop={CANVAS_W}:{top_h}:0:0[t];"
            f"[0:v]fps={SAMPLE_FPS},crop={CANVAS_W}:{bot_h}:0:{CAPTION_BAND_BOTTOM}[b];"
            f"[t][b]vstack=inputs=2[out]"
        )
        subprocess.run(
            ["ffmpeg", "-v", "error", "-i", str(render), "-filter_complex", filt,
             "-map", "[out]", "-vsync", "0", str(td / "f-%05d.png")], check=True)
        frames = sorted(td.glob("f-*.png"))
        if len(frames) < 2:
            print("check-cadence: too few frames — skipping.")
            return 0

        arr = [np.asarray(Image.open(f).convert("L")).astype(np.float32) for f in frames]
        steps = []
        for i in range(1, len(arr)):
            d = int((np.abs(arr[i] - arr[i - 1]) > PIXEL_DELTA).sum())
            steps.append((i / SAMPLE_FPS, d))

    print(f"check-cadence: {len(steps)} steps @ {SAMPLE_FPS}fps, caption band "
          f"({CAPTION_BAND_TOP}-{CAPTION_BAND_BOTTOM}px) excluded")
    print(f"  active if >= {ACTIVE_PX} changed px (|dLuma| > {PIXEL_DELTA}); "
          f"cuts (>= {CUT_PX}) excluded\n")
    print(f"  {'scene':<14} {'steps':>7} {'active':>7} {'share':>7}   verdict")

    overall_act = overall_tot = 0
    for s, e, name in SCENES:
        inside = [(t, d) for t, d in steps if s + 0.15 <= t < e - 0.05]
        real = [(t, d) for t, d in inside if d < CUT_PX]
        act = sum(1 for _, d in real if d >= ACTIVE_PX)
        tot = len(real)
        overall_act += act
        overall_tot += tot
        share = act / tot if tot else 0.0
        verdict = "ok" if share >= LOW_SHARE_WARN else "LOW — check for a dead stretch"
        print(f"  {name:<14} {tot:>7d} {act:>7d} {100 * share:>6.0f}%   {verdict}")

        # longest run of consecutive inactive steps inside the scene
        run = best = 0
        best_at = None
        for t, d in real:
            if d < ACTIVE_PX:
                run += 1
                if run > best:
                    best, best_at = run, t
            else:
                run = 0
        if best:
            secs = best / SAMPLE_FPS
            flag = "  <-- over 2.5s ceiling" if secs > 2.5 else ""
            print(f"                 longest quiet run {secs:.2f}s ending ~{best_at:.1f}s{flag}")

    share = overall_act / overall_tot if overall_tot else 0
    print(f"\n  whole video: {overall_act}/{overall_tot} active ({100*share:.0f}%)")
    if share < LOW_SHARE_WARN:
        print(f"  NOTE: under {100*LOW_SHARE_WARN:.0f}% — worth a second look regardless "
              f"of what `hyperframes check` reports (it has no cadence dimension).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
