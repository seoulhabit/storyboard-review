#!/usr/bin/env python3
"""Scan a rendered MP4 for a static-hold: real content that stops changing for
longer than a short's cadence ceiling, even though it is never blank.

This is the gap check-blank-frames.py cannot close. That script measures
per-frame luma stddev (blankness) — a frozen but fully-populated frame reads
identically to a healthy one on that metric, so a scene that lands all its
beats early and then sits frozen for the rest of its narration sails through
it clean. Confirmed on `videos/peeling-not-progress`'s own sibling channel
project, `videos/glass-skin-5-habits`, 2026-08-30: a CTA/endcard scene
measured several seconds frozen — invisible to check-blank-frames.py and to
`hyperframes check` alike (neither measures frame-to-frame change).

CORRECTED 2026-08-31 (peeling-not-progress): that project's copy of this
script inherited a hardcoded CAPTION_BAND_TOP/BOTTOM (960-1110) from a
different project's caption geometry while itself having no burned-in
captions at all — the crop was cutting a real content strip out of every
scene it scanned. See that project's own copy for the full story if reusing
this file again.

RE-DERIVED 2026-08-31 (this project, mugwort-healing-herb): this video DOES
carry burned-in captions — `.vo-caption` in index.html, `top:240px`, up to
two lines at 46px/1.3 line-height plus 12px vertical padding each side (worst
case ≈240 to ≈384). CAPTION_BAND_EXCLUDE is ON below with that project's own
real numbers (215-350, a few px of margin either side of the measured worst
case), not copied from a sibling — re-derive again for any other project
before trusting this file's "zero findings" as evidence of anything.

Method: sample at a fixed low fps, optionally crop out a caption band
(top+bottom strips vstacked back together) when one exists, compute PSNR
between consecutive sampled frames. A genuinely frozen region reads as very
high PSNR (identical or near-identical pixels); real motion — even a slow Ken
Burns drift — keeps PSNR well below the cutoff. Flag any run longer than the
project's cadence ceiling.

Advisory only (exit 0 always), matching check-blank-frames.py's convention —
a held freeze-frame can be a deliberate choice; this surfaces candidates for
a human to confirm, not a hard gate.
"""
import glob
import subprocess
import sys
from pathlib import Path

try:
    import numpy as np
    from PIL import Image
except ImportError:
    print("check-static-hold: needs `python3 -m pip install pillow numpy` — skipping.")
    sys.exit(0)

SAMPLE_FPS = 2                  # coarse is fine -- a static hold is measured in seconds
CANVAS_W, CANVAS_H = 1080, 1920
CAPTION_BAND_EXCLUDE = True     # this project DOES burn in captions (.vo-caption,
                                 # top:240px in index.html) -- re-derived for this project's
                                 # own geometry, not copied from a sibling. See docstring.
CAPTION_BAND_TOP = 215          # a few px above the caption's own top:240px
CAPTION_BAND_BOTTOM = 350       # covers the worst case: 2-line caption at 46px/1.3 lh + 24px pad
PSNR_FROZEN_DB = 55.0           # above this between consecutive samples reads as "no change"
CADENCE_CEILING_S = 2.5         # shorts target: a state change at least every 1.5-3s


def most_recent_render(project_root):
    candidates = glob.glob(str(project_root / "renders" / "*.mp4"))
    if not candidates:
        return None
    return Path(max(candidates, key=lambda p: Path(p).stat().st_mtime))


def psnr(a, b):
    mse = np.mean((a.astype(np.float64) - b.astype(np.float64)) ** 2)
    if mse <= 1e-9:
        return 99.0
    return 10.0 * np.log10((255.0 ** 2) / mse)


def main():
    project_root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    render_path = sys.argv[2] if len(sys.argv) > 2 else None
    render_path = Path(render_path) if render_path else most_recent_render(project_root)

    if not render_path or not render_path.exists():
        print("check-static-hold: no render found under renders/*.mp4 — skipping.")
        return 0

    if CAPTION_BAND_EXCLUDE:
        print(f"Static-hold scan — {render_path.name}, sampling every {1000/SAMPLE_FPS:.0f}ms, "
              f"caption band ({CAPTION_BAND_TOP}-{CAPTION_BAND_BOTTOM}px) excluded.")
        top_h = CAPTION_BAND_TOP
        bot_h = CANVAS_H - CAPTION_BAND_BOTTOM
        filt = (
            f"[0:v]fps={SAMPLE_FPS},crop={CANVAS_W}:{top_h}:0:0[top];"
            f"[0:v]fps={SAMPLE_FPS},crop={CANVAS_W}:{bot_h}:0:{CAPTION_BAND_BOTTOM}[bot];"
            f"[top][bot]vstack=inputs=2[out]"
        )
    else:
        print(f"Static-hold scan — {render_path.name}, sampling every {1000/SAMPLE_FPS:.0f}ms, "
              f"full frame (no caption band to exclude).")
        filt = f"[0:v]fps={SAMPLE_FPS}[out]"
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        proc = subprocess.run(
            ["ffmpeg", "-y", "-i", str(render_path), "-filter_complex", filt,
             "-map", "[out]", "-q:v", "4", f"{tmp}/f_%06d.png"],
            capture_output=True, check=False,
        )
        frame_paths = sorted(glob.glob(f"{tmp}/f_*.png"))
        if not frame_paths:
            print("  could not extract frames — skipping.")
            print(proc.stderr.decode(errors="replace")[-800:])
            return 0

        arrays = [np.asarray(Image.open(p).convert("L"), dtype=np.uint8) for p in frame_paths]

    findings = []
    run_start = None
    for i in range(1, len(arrays)):
        t = i / SAMPLE_FPS
        p = psnr(arrays[i - 1], arrays[i])
        if p > PSNR_FROZEN_DB:
            if run_start is None:
                run_start = t - (1.0 / SAMPLE_FPS)
        else:
            if run_start is not None:
                duration = t - run_start
                if duration >= CADENCE_CEILING_S:
                    findings.append((run_start, t, duration))
                run_start = None
    if run_start is not None:
        t_end = (len(arrays) - 1) / SAMPLE_FPS
        duration = t_end - run_start
        if duration >= CADENCE_CEILING_S:
            findings.append((run_start, t_end, duration))

    if not findings:
        print(f"  no findings ({len(arrays)} frames sampled, {CADENCE_CEILING_S}s ceiling).")
        return 0

    print(f"  {len(findings)} static-hold(s) found, over the {CADENCE_CEILING_S}s cadence ceiling:")
    for start, end, duration in findings:
        print(f"  - t={start:.2f}s to t={end:.2f}s  ({duration:.2f}s frozen, imagery excluding captions)")
    print("  Verify each: does this scene need a beat, or is it a deliberate hold?")
    return 0


if __name__ == "__main__":
    sys.exit(main())
