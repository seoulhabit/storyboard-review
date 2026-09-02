#!/usr/bin/env python3
"""Scan a rendered MP4 for real content (ink) inside YouTube Shorts' reserved UI
zones, measured on transformed, RENDERED pixels — not on the composition's source.

Why this exists: `faceless-video-craft` SKILL.md's pre-render gate item 7 asks
"are safe-area tokens consumed by every scene" — a source-code question. Every
scene in a project can consume `--safe-*` correctly and still ship ink past the
real line, because a `transform: scale()`/`translate()` applied OUTSIDE a padded
box (a Ken Burns wrapper, most commonly) maps the padded edge outward by the same
factor it scales the box. Confirmed on `peeling-not-progress`'s own 2026-08-31
render: three scenes (03-truth, 04-boundary, 05-reset) each declared and consumed
every `--safe-*` token, and each still overshot the real 20%-bottom/15%-right
line by 5-10px once their own continuous Ken Burns zoom was accounted for — a
class of defect no source-level audit or lint pass can see, because the source
IS correct; only the rendered result isn't. See `frame.md` "Post-render review
fixes" round 6 for the full measured root cause.

This is a HARD GATE, unlike check-blank-frames.py / check-static-hold.py's
advisory (always-exit-0) convention in this project — a rendered pixel inside a
reserved zone is not a judgment call the way a static hold's cadence sometimes
is; it will be covered by the platform's own UI on a real device.

Method: sample the render at a fixed fps, build an ink mask per frame (|luma -
modal background luma| over a threshold, ignoring stray antialiasing by
requiring a minimum run of masked pixels in a row/column before it counts as a
real edge), and flag any frame with ink inside the four reserved zones. Zone
sizes are passed as CLI flags — this script is not project-specific — and
default to this project's own tokens.css values so a bare invocation matches
what the composition actually declares.
"""
import argparse
import glob
import sys
import tempfile
from pathlib import Path

try:
    import numpy as np
    from PIL import Image
except ImportError:
    print("check-safe-area: needs `python3 -m pip install pillow numpy` — skipping (exit 0).")
    sys.exit(0)

import subprocess

SAMPLE_FPS = 4                  # finer than static-hold's 2fps -- a fast Ken Burns
                                 # drift can cross the line between two 2fps samples
CANVAS_W, CANVAS_H = 1080, 1920
INK_THRESHOLD = 28              # |luma - background| above this counts as "ink"
MIN_EDGE_RUN = 8                # a row/col needs >=8 masked px before it's a real
                                 # edge, not antialiasing noise, matching the method
                                 # used to diagnose this project's own round-6 defect
MIN_INTRUSION_PX = 40           # total masked px inside a zone before it's reported --
                                 # tolerates a stray AA sliver at the zone boundary


def most_recent_render(project_root):
    candidates = glob.glob(str(project_root / "renders" / "*.mp4"))
    if not candidates:
        return None
    return Path(max(candidates, key=lambda p: Path(p).stat().st_mtime))


def ink_mask(frame_gray):
    vals, counts = np.unique(frame_gray, return_counts=True)
    bg = int(vals[counts.argmax()])
    diff = np.abs(frame_gray.astype(int) - bg)
    raw = diff > INK_THRESHOLD
    row_ok = raw.sum(axis=1) >= MIN_EDGE_RUN
    col_ok = raw.sum(axis=0) >= MIN_EDGE_RUN
    return raw & row_ok[:, None] & col_ok[None, :]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("project_root", nargs="?", default=".")
    ap.add_argument("render_path", nargs="?", default=None)
    ap.add_argument("--safe-top", type=int, default=192, help="reserved top px (default: skill's 10% of 1920)")
    ap.add_argument("--safe-bottom", type=int, default=384, help="reserved bottom px (default: skill's 20% of 1920)")
    ap.add_argument("--safe-right", type=int, default=162, help="reserved right px (default: skill's 15% of 1080)")
    ap.add_argument("--safe-left", type=int, default=0, help="reserved left px (default: 0 -- no left rail in the skill)")
    args = ap.parse_args()

    project_root = Path(args.project_root).resolve()
    render_path = Path(args.render_path) if args.render_path else most_recent_render(project_root)

    if not render_path or not render_path.exists():
        print("check-safe-area: no render found under renders/*.mp4 — skipping (exit 0).")
        return 0

    y_top, y_bot = args.safe_top, CANVAS_H - args.safe_bottom
    x_left, x_right = args.safe_left, CANVAS_W - args.safe_right

    print(f"Safe-area scan — {render_path.name}, sampling every {1000/SAMPLE_FPS:.0f}ms.")
    print(f"  reserved zones: top<{y_top}  bottom>={y_bot}  right>={x_right}"
          + (f"  left<{x_left}" if x_left else ""))

    with tempfile.TemporaryDirectory() as tmp:
        proc = subprocess.run(
            ["ffmpeg", "-y", "-i", str(render_path), "-vf", f"fps={SAMPLE_FPS}",
             "-q:v", "4", f"{tmp}/f_%06d.png"],
            capture_output=True, check=False,
        )
        frame_paths = sorted(glob.glob(f"{tmp}/f_*.png"))
        if not frame_paths:
            print("  could not extract frames — skipping (exit 0).")
            print(proc.stderr.decode(errors="replace")[-800:])
            return 0

        zones = {"top": [], "bottom": [], "right": [], "left": []}
        for i, p in enumerate(frame_paths):
            t = i / SAMPLE_FPS
            gray = np.asarray(Image.open(p).convert("L"), dtype=np.uint8)
            mask = ink_mask(gray)

            top_px = int(mask[:y_top, :].sum())
            bot_px = int(mask[y_bot:, :].sum())
            right_px = int(mask[:, x_right:].sum())
            left_px = int(mask[:, :x_left].sum()) if x_left else 0

            if top_px > MIN_INTRUSION_PX:
                zones["top"].append((t, top_px))
            if bot_px > MIN_INTRUSION_PX:
                zones["bottom"].append((t, bot_px))
            if right_px > MIN_INTRUSION_PX:
                zones["right"].append((t, right_px))
            if left_px > MIN_INTRUSION_PX:
                zones["left"].append((t, left_px))

    total_findings = sum(len(v) for v in zones.values())
    if not total_findings:
        print(f"  no findings ({len(frame_paths)} frames sampled) — every sampled frame's ink stayed clear of all reserved zones.")
        return 0

    print(f"  FAIL — ink found inside a reserved zone on {total_findings} sampled frame(s):")
    for zone, hits in zones.items():
        if not hits:
            continue
        peak_t, peak_px = max(hits, key=lambda h: h[1])
        first_t = hits[0][0]
        print(f"  - {zone}: first at t={first_t:.2f}s, worst at t={peak_t:.2f}s ({peak_px}px masked in-zone), {len(hits)} frame(s) total")
    print("  This is a hard gate: fix the scene(s) named above before calling the render final.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
