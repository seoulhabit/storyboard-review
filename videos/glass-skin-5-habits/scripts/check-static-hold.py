#!/usr/bin/env python3
"""Scan a rendered MP4 for a static-hold: real content that stops changing for
longer than a short's cadence ceiling, even though it is never blank.

This is the gap check-blank-frames.py cannot close. That script measures
per-frame luma stddev (blankness) — a frozen but fully-populated frame reads
identically to a healthy one on that metric, so a scene that lands all its
beats early and then sits frozen for the rest of its narration sails through
it clean. Confirmed on this exact project 2026-08-30: Frame 6 (the
CTA/endcard) measured ~5.0s frozen from local ~2.06s to its own end — the
only static-hold violation in the video, invisible to check-blank-frames.py
and to `hyperframes check` alike (neither measures frame-to-frame change),
and previously reported in frame.md as "re-verified clean" on the strength of
a tool that could not have established that.

Caption-band exclusion matters: this project's burned-in captions repaint
words continuously, and cropping them back IN would mask every frozen scene
underneath them — precisely how the Frame 6 freeze passed review the first
time (a human scrubbing the render sees the caption band changing and reads
the whole frame as "alive"). CAPTION_BAND_TOP/BOTTOM below match this
project's own caption-stage position (scripts/gen/build_captions_html.py);
adjust per project if this script is copied elsewhere before it has a real
config path — see the QC fix pass that added it (CATALOG.md, 2026-08-30) for
why it isn't fully generic yet.

Method: sample at a fixed low fps, crop out the caption band (top+bottom
strips vstacked back together), compute PSNR between consecutive sampled
frames. A genuinely frozen region reads as very high PSNR (identical or
near-identical pixels); real motion — even a slow Ken Burns drift — keeps
PSNR well below the cutoff. Flag any run longer than the project's cadence
ceiling.

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
CAPTION_BAND_TOP = 960          # this project's caption-stage top (build_captions_html.py)
CAPTION_BAND_BOTTOM = 1110      # top + height (150)
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

    print(f"Static-hold scan — {render_path.name}, sampling every {1000/SAMPLE_FPS:.0f}ms, "
          f"caption band ({CAPTION_BAND_TOP}-{CAPTION_BAND_BOTTOM}px) excluded.")

    top_h = CAPTION_BAND_TOP
    bot_h = CANVAS_H - CAPTION_BAND_BOTTOM
    filt = (
        f"[0:v]fps={SAMPLE_FPS},crop={CANVAS_W}:{top_h}:0:0[top];"
        f"[0:v]fps={SAMPLE_FPS},crop={CANVAS_W}:{bot_h}:0:{CAPTION_BAND_BOTTOM}[bot];"
        f"[top][bot]vstack=inputs=2[out]"
    )
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
