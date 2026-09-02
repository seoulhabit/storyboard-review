#!/usr/bin/env python3
"""Scan a rendered MP4 for near-blank stretches anywhere in the timeline.

Catches the class of bug found in kbeauty-one-percent-line 2026-08-29: a gap
between two sequential reveal beats (or a slow entrance tween) leaves the
canvas essentially empty for a stretch a viewer will perceive as a stutter —
including frame zero itself, the load/poster frame per faceless-video-craft's
"frame zero is a design object" rule, but not limited to it.

Portable across HyperFrames video projects: run with a project root (finds
the most recently modified renders/*.mp4 there), no project-specific paths
hardcoded.

Method: sample frames at a fixed rate, compute each frame's luma standard
deviation (PIL/numpy — a genuinely flat frame has stddev near 0; real content,
even a small headline on a big background, reads meaningfully higher).
Calibrated against this project's own two confirmed bugs: the original blank
frame-zero measured stddev=0.0, the Frame-3 gap measured stddev=4.2, while
ordinary content frames measured 25-90+. Default cutoff sits well above both
confirmed-bad readings and well below confirmed-good ones.

Advisory only (exit 0 always) — some blank stretches are deliberate (a held
freeze-frame, a wordless breather beat). This surfaces candidates for a human
to confirm, the same way hyperframes check's own info-level findings do.
"""
import glob
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import numpy as np
    from PIL import Image
except ImportError:
    print("check-blank-frames: needs `python3 -m pip install pillow numpy` — skipping.")
    sys.exit(0)

STDDEV_CUTOFF = 12.0       # bad readings seen: 0.0, 4.2. good readings seen: 25.3+
SAMPLE_FPS = 15            # ~67ms resolution — catches the 200ms/350ms bugs found so far
MIN_FLAG_DURATION_S = 0.15


def most_recent_render(project_root):
    candidates = glob.glob(str(project_root / "renders" / "*.mp4"))
    if not candidates:
        return None
    return Path(max(candidates, key=lambda p: Path(p).stat().st_mtime))


def main():
    project_root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    render_path = sys.argv[2] if len(sys.argv) > 2 else None
    render_path = Path(render_path) if render_path else most_recent_render(project_root)

    if not render_path or not render_path.exists():
        print("check-blank-frames: no render found under renders/*.mp4 — skipping.")
        return 0

    print(f"Blank-frame scan — {render_path.name}, sampling every {1000/SAMPLE_FPS:.0f}ms.")

    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(render_path), "-vf", f"fps={SAMPLE_FPS}",
             "-q:v", "4", f"{tmp}/f_%06d.png"],
            capture_output=True, check=True,
        )
        frame_paths = sorted(glob.glob(f"{tmp}/f_*.png"))
        if not frame_paths:
            print("  could not extract frames — skipping.")
            return 0

        stddevs = []
        for p in frame_paths:
            arr = np.asarray(Image.open(p).convert("L"), dtype=np.float32)
            stddevs.append(float(arr.std()))

    findings = []
    run_start = None
    for i, sd in enumerate(stddevs):
        t = i / SAMPLE_FPS
        if sd < STDDEV_CUTOFF:
            if run_start is None:
                run_start = t
        else:
            if run_start is not None:
                duration = t - run_start
                if duration >= MIN_FLAG_DURATION_S:
                    findings.append((run_start, t, duration))
                run_start = None
    if run_start is not None:
        t_end = len(stddevs) / SAMPLE_FPS
        duration = t_end - run_start
        if duration >= MIN_FLAG_DURATION_S:
            findings.append((run_start, t_end, duration))

    if not findings:
        print(f"  no findings ({len(frame_paths)} frames sampled).")
        return 0

    print(f"  {len(findings)} near-blank stretch(es) found ({len(frame_paths)} frames sampled):")
    for start, end, duration in findings:
        tag = " <- includes frame zero (poster/load frame)" if start <= 0.01 else ""
        print(f"  - t={start:.2f}s to t={end:.2f}s  ({duration*1000:.0f}ms){tag}")
    print("  Verify each: a real gap between reveal beats, or a deliberate hold/freeze?")
    return 0


if __name__ == "__main__":
    sys.exit(main())
