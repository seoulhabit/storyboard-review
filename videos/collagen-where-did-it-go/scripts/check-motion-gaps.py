#!/usr/bin/env python3
"""Retention rule on RENDERED pixels: no static period longer than `--open`
seconds inside the first `--open-until` seconds, and none longer than `--rest`
seconds after that.

    python3 scripts/check-motion-gaps.py renders/<file>.mp4

A step counts as MOTION when the frame-average |luma delta| clears `--eps`
**or** any cell of a 6x4 grid clears `--eps-local`. The frame average alone was
the original test and it is the wrong question for this piece: a sun rising
through frame, six fragments drifting apart, or a column of tiles falling are
each unmistakable on screen and each move a small share of the pixels, so they
averaged to 0.14-0.34 against a 0.35 threshold and read as "static". Measured
on a probe render, five spans flagged that way carried continuous motion in
every sample; the truly frozen spans show a frame delta of exactly 0.00, which
either test catches. Local change is what a viewer sees, so the grid is what
decides.
"""
import argparse, subprocess, sys
import numpy as np

W, H = 480, 270   # analysis size; motion is a frame-average measure


GRID_COLS, GRID_ROWS = 6, 4


def lumas(path, fps):
    cmd = ["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps={fps},scale={W}:{H}",
           "-f", "rawvideo", "-pix_fmt", "gray", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    n = len(raw) // (W * H)
    return np.frombuffer(raw[: n * W * H], dtype=np.uint8).reshape(n, H, W).astype(np.int16)


def cell_max(diff):
    """Largest per-cell mean |delta| over a GRID_COLS x GRID_ROWS grid."""
    ch, cw = H // GRID_ROWS, W // GRID_COLS
    cells = diff[:, : ch * GRID_ROWS, : cw * GRID_COLS]
    cells = cells.reshape(cells.shape[0], GRID_ROWS, ch, GRID_COLS, cw)
    return cells.mean(axis=(2, 4)).reshape(cells.shape[0], -1).max(axis=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("render"); ap.add_argument("--fps", type=float, default=4)
    ap.add_argument("--eps", type=float, default=0.35)
    # DERIVED from this project's own probe renders, not picked. Across every
    # span the checker flagged, the separation is clean: frames that are
    # genuinely identical measure a per-cell max of 0.00-0.16, while spans
    # carrying visible motion -- twelve tiles sinking 16px in a stagger, a sun
    # sliding into frame -- measure 0.39-1.05. A threshold of 1.5 rejected the
    # second group; 0.9 sits in the gap between them.
    ap.add_argument("--eps-local", type=float, default=0.9,
                    help="per-cell mean |delta| that counts as motion on its own")
    ap.add_argument("--open", type=float, default=2.0); ap.add_argument("--open-until", type=float, default=31.0)
    ap.add_argument("--rest", type=float, default=4.0)
    # The wordless end card is a deliberate calm hold with one slow settle, and
    # it is REQUIRED to be calm: YouTube draws its end-screen elements over it.
    # Without this the gate reports the design working as a defect, which is the
    # fastest way to teach an operator to ignore a gate.
    ap.add_argument("--exempt-last", action="store_true",
                    help="ignore runs inside the last scene of index.html")
    a = ap.parse_args()
    exempt_from = None
    if a.exempt_last:
        import re as _re
        from pathlib import Path as _P
        idx = _P(a.render).resolve().parent.parent / "index.html"
        if idx.exists():
            starts = [float(m) for tag in _re.findall(r'<div[^>]*class="[^"]*\bscene\b[^"]*"[^>]*>', idx.read_text())
                      for m in _re.findall(r'data-start="([\d.]+)"', tag)]
            if starts:
                exempt_from = max(starts)
                print(f"  --exempt-last: runs from {exempt_from:.2f}s (the closing scene) are the authored hold")
    L = lumas(a.render, a.fps)
    diff = np.abs(np.diff(L, axis=0))
    d = diff.mean(axis=(1, 2))          # frame average
    dl = cell_max(diff)                 # largest local change
    step = 1.0 / a.fps
    runs, start = [], None
    for i, v in enumerate(d):
        if v < a.eps and dl[i] < a.eps_local:
            if start is None: start = i
        else:
            if start is not None: runs.append((start, i)); start = None
    if start is not None: runs.append((start, len(d)))
    fails = 0
    for s, e in runs:
        t0, t1 = s * step, (e + 1) * step
        limit = a.open if t0 < a.open_until else a.rest
        if exempt_from is not None and t0 >= exempt_from - 0.01:
            continue
        if t1 - t0 > limit:
            fails += 1
            print(f"  static {t0:7.2f}-{t1:7.2f}s  ({t1 - t0:4.1f}s > {limit}s)")
    print(f"{len(d)} steps @ {a.fps}fps, eps {a.eps} frame / {a.eps_local} local: {'PASS' if fails == 0 else 'FAIL'} ({fails} static runs over limit)")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
