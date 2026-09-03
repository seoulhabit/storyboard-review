#!/usr/bin/env python3
"""Scan a rendered MP4 for real content (ink) inside a platform's reserved UI
zones, measured on transformed, RENDERED pixels — not on the composition's source.

Canvas-aware since 2026-09-02. It was previously hard-coded to a 1080x1920
portrait canvas, and the failure on a landscape render was SILENT AND MIXED,
which is why the canvas is now asserted rather than assumed. Measured on a
fully-inked 1920x1080 frame with the old portrait constants:

    bottom zone  mask[1536:, :]   -> shape (0, 1920)     sum=0        FAIL-OPEN
    right  zone  mask[:, 918:]    -> shape (1080, 1002)  sum=1082160  wrong region

The bottom slice runs past the end of a 1080-tall array, so numpy returns an
empty view and the hard gate reports "no findings" and exits 0. The right slice
silently measures the right 52% of the frame instead of a 162px rail. A gate
that lies in both directions is worse than no gate, so `--canvas-w/--canvas-h`
now exist AND a mismatch against the render's real dimensions is a loud failure
(exit 2), never a silent pass.

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
PAGE GROUND luma, taken from the outer border ring| over a threshold, ignoring stray antialiasing by
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
CANVAS_W, CANVAS_H = 1080, 1920   # portrait default; override with --canvas-w/--canvas-h
INK_THRESHOLD = 28              # |luma - background| above this counts as "ink"
GROUND_MIN_SHARE = 0.15         # a luma cluster holding this much of the border ring
                                 # is a page ground in its own right -- a transition
                                 # frame has two, one per scene
MAX_GROUNDS = 3                 # two scenes plus a letterbox is the realistic ceiling
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


def render_dimensions(render_path):
    """(width, height) of the render via ffprobe, or None if it cannot be determined."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", str(render_path)],
            capture_output=True, check=False, timeout=30,
        ).stdout.decode(errors="replace").strip()
        w, h = out.split("x")[:2]
        return int(w), int(h)
    except Exception:  # noqa: BLE001 - any ffprobe/parse failure means "canvas unknown"
        return None


def page_grounds(frame_gray):
    """Every PAGE GROUND present in the outer border ring, not just one.

    page_ground() used to return a single median, which is correct only while
    the frame HAS a single ground. A transition frame legitimately has two --
    the outgoing scene and the incoming one -- so the ring goes bimodal, the
    median lands on whichever ground holds more of it, and the other ground
    then differs from the reference everywhere it appears. The zone reports
    100% ink with nothing in it. Measured on a real 29-scene wipe render: the
    gate called the entire 54x1920 top band inked (103680px) at t=73.50s, where
    that band is uniformly luma 19 -- a flat scene ground, min == max, zero
    variation. 70 frames flagged, every one of them a transition frame.

    That is the second time this estimator has been wrong in the same
    direction (the whole-frame modal it replaced broke on a busy landscape
    frame), and on a HARD gate a false positive is worse than a miss: it
    blocks a clean render, and the wave-through it earns is what lets the next
    real one through.

    So: cluster the ring instead of averaging it. Any luma level holding at
    least GROUND_MIN_SHARE of the ring is a ground, up to MAX_GROUNDS of them,
    and a pixel is ink only when it differs from ALL of them. A single-ground
    frame yields exactly one cluster and behaves as before.

    History, because this estimator has now been wrong twice and the reason
    matters more than the fix: the whole-frame modal it started as failed as
    soon as content covered more than half the canvas (two 45%-of-frame panels
    made the modal a PANEL colour -- modal 151 against a true ground of 243 --
    and all four zones reported 100% ink across 136 frames with nothing out of
    place). The outer ring replaced it because reserved margins mean the
    extreme edge IS page ground by construction. That reasoning still holds;
    what it missed is that the edge can be page ground for TWO pages at once.

    Returns a list of luma levels, most common first.
    """
    ring = np.concatenate([frame_gray[:4, :].ravel(), frame_gray[-4:, :].ravel(),
                           frame_gray[:, :4].ravel(), frame_gray[:, -4:].ravel()])
    hist = np.bincount(ring, minlength=256).astype(float)
    total = hist.sum()
    grounds = []
    for _ in range(MAX_GROUNDS):
        peak = int(hist.argmax())
        lo, hi = max(0, peak - INK_THRESHOLD), min(255, peak + INK_THRESHOLD)
        share = hist[lo:hi + 1].sum() / total
        if share < GROUND_MIN_SHARE:
            break
        grounds.append(peak)
        hist[lo:hi + 1] = 0                 # absorb this cluster, look for the next
    return grounds or [int(np.median(ring))]


def ink_raw(frame_gray):
    """Pixels belonging to no page ground. No run-filter yet -- see zone_ink()."""
    grounds = page_grounds(frame_gray)
    g = frame_gray.astype(int)
    # ink only where the pixel differs from EVERY ground present in the frame
    diff = np.min([np.abs(g - b) for b in grounds], axis=0)
    return diff > INK_THRESHOLD


def zone_ink(raw_zone):
    """Masked px in one reserved zone, run-filtered WITHIN that zone.

    MIN_EDGE_RUN exists to drop antialiasing: a real edge puts several masked
    pixels in a row, a resampling fringe puts one. That test used to be
    computed across the FULL FRAME, which quietly defeats it at a zone
    boundary -- a row crossing a scene seam carries one masked pixel inside a
    96px rail, but the same row has real content elsewhere in the 1920px
    frame, so the row passes and the lone fringe pixel survives into the zone.

    Measured: the multi-ground estimator took a 29-scene wipe render from 70
    flagged frames to 8, and those 8 were the seam's own antialiasing -- worst
    case 1184px inside a 103680px rail, about one pixel per row. Scoping the
    run test to the zone removes them without touching anything bounded: real
    content in a rail spans many pixels per row, and the smallest genuine
    finding on the known-dirty push build was 12636px.
    """
    if not raw_zone.size:
        return 0
    row_ok = raw_zone.sum(axis=1) >= MIN_EDGE_RUN
    col_ok = raw_zone.sum(axis=0) >= MIN_EDGE_RUN
    return int((raw_zone & row_ok[:, None] & col_ok[None, :]).sum())


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("project_root", nargs="?", default=".")
    ap.add_argument("render_path", nargs="?", default=None)
    ap.add_argument("--safe-top", type=int, default=192, help="reserved top px (default: skill's 10%% of 1920)")
    ap.add_argument("--safe-bottom", type=int, default=384, help="reserved bottom px (default: skill's 20%% of 1920)")
    ap.add_argument("--safe-right", type=int, default=162, help="reserved right px (default: skill's 15%% of 1080)")
    ap.add_argument("--safe-left", type=int, default=0, help="reserved left px (default: 0 -- no left rail in the skill)")
    ap.add_argument("--canvas-w", type=int, default=CANVAS_W, help=f"canvas width px (default: {CANVAS_W})")
    ap.add_argument("--canvas-h", type=int, default=CANVAS_H, help=f"canvas height px (default: {CANVAS_H})")
    ap.add_argument("--landscape", action="store_true",
                    help="16:9 long-form profile: canvas 1920x1080 and the landscape reserved "
                         "zones (top 54 / bottom 108 / left 96 / right 96). Any explicit "
                         "--canvas-* or --safe-* flag still wins over the profile.")
    args = ap.parse_args()

    # Landscape profile: apply only where the operator left the portrait default in place,
    # so an explicit flag is never silently overridden.
    if args.landscape:
        supplied = {a.split("=")[0] for a in sys.argv[1:]}
        def _default(flag, cur, portrait_default):
            return cur if f"--{flag}" in supplied else portrait_default
        args.canvas_w    = _default("canvas-w",    args.canvas_w,    1920)
        args.canvas_h    = _default("canvas-h",    args.canvas_h,    1080)
        args.safe_top    = _default("safe-top",    args.safe_top,    54)
        args.safe_bottom = _default("safe-bottom", args.safe_bottom, 108)
        args.safe_right  = _default("safe-right",  args.safe_right,  96)
        args.safe_left   = _default("safe-left",   args.safe_left,   96)

    project_root = Path(args.project_root).resolve()
    render_path = Path(args.render_path) if args.render_path else most_recent_render(project_root)

    if not render_path or not render_path.exists():
        print("check-safe-area: no render found under renders/*.mp4 — skipping (exit 0).")
        return 0

    canvas_w, canvas_h = args.canvas_w, args.canvas_h

    # Fail LOUD on a canvas mismatch. The whole reason this assert exists is that the
    # old portrait-only version returned an empty numpy slice on a landscape render and
    # reported a clean pass -- see the module docstring for the measured numbers.
    real = render_dimensions(render_path)
    if real and real != (canvas_w, canvas_h):
        print(f"check-safe-area: CANVAS MISMATCH — {render_path.name} is "
              f"{real[0]}x{real[1]} but the zones are configured for {canvas_w}x{canvas_h}.")
        print("  Refusing to run: the reserved-zone slices would address the wrong region "
              "(and a bottom zone past the frame height reports a silent false pass).")
        print(f"  Fix: pass --canvas-w {real[0]} --canvas-h {real[1]}"
              + ("  (or just --landscape)" if real == (1920, 1080) else "")
              + " with the matching --safe-* values for that platform.")
        return 2

    y_top, y_bot = args.safe_top, canvas_h - args.safe_bottom
    x_left, x_right = args.safe_left, canvas_w - args.safe_right

    print(f"Safe-area scan — {render_path.name}, {canvas_w}x{canvas_h}, "
          f"sampling every {1000/SAMPLE_FPS:.0f}ms.")
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
            raw = ink_raw(gray)

            top_px = zone_ink(raw[:y_top, :])
            bot_px = zone_ink(raw[y_bot:, :])
            right_px = zone_ink(raw[:, x_right:])
            left_px = zone_ink(raw[:, :x_left]) if x_left else 0

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
