#!/usr/bin/env python3
"""Retention rule on RENDERED pixels: no shot may sit still for too long.

No static period longer than `--open` seconds inside the first `--open-until`
seconds, and none longer than `--rest` after that -- an opening that stalls
loses the viewer outright, a later one merely bores them.

WHAT COUNTS AS MOTION, and why the obvious test is wrong. A step is MOTION when
the frame-average |luma delta| clears `--eps` **or** any cell of a grid clears
`--eps-local`. The frame average alone was the original test and it asks the
wrong question: a sun rising through frame, six fragments drifting apart, a
column of tiles falling -- each is unmistakable on screen and each moves a small
share of the pixels, so they average to 0.14-0.34 against a 0.35 threshold and
read as "static". Measured on a probe render, five spans flagged that way
carried continuous motion in every sample. The truly frozen spans measure a
frame delta of exactly 0.00, which either test catches. Local change is what a
viewer sees, so the grid is what decides.

`--eps-local`'s default was DERIVED, not picked. Across every span one project's
checker flagged, the separation is clean: genuinely identical frames measure a
per-cell max of 0.00-0.16, spans carrying visible motion measure 0.39-1.05. A
threshold of 1.5 rejected the second group; 0.9 sits in the gap.

SIZE THE MOTION AGAINST THIS GATE'S OWN SAMPLING, not by eye. It steps at
`--fps` (default 4, so 0.25s) and thresholds the delta between CONSECUTIVE
steps. A drift that reads fine at half-second intervals is half that per step
and lands under the floor -- authored motion has been added twice, measured at
0.5s spacing, and still failed here.

EXEMPTIONS. A deliberate hold is a design decision, not something the gate
should keep re-discovering, and a gate that reports the design working as a
defect is the fastest way to teach an operator to ignore it. Three ways to say
so, and all three PRINT what they dropped -- an exemption that skips silently
is one nobody can audit:

    --exempt-window START-END   a reviewed hold. Bounded: a run that grows
                                past the window still fails.
    --exempt-last               everything from the last scene's start.
    --exempt-marker STRING      everything from the first scene whose composition
                                HTML contains STRING -- e.g. the end-screen
                                reserve token. More precise than --exempt-last
                                when a project reserves across SEVERAL closing
                                scenes: --exempt-last would catch only the final
                                one and fail the scene before it.

FIELD CONTRACT
    python3 check-motion-gaps.py <render.mp4>
        [--fps 4] [--eps 0.35] [--eps-local 0.9]
        [--open 2.0] [--open-until 31.0] [--rest 4.0]
        [--exempt-window START-END] [--exempt-last] [--exempt-marker STRING]
        [--project-root DIR]        # for --exempt-last/--exempt-marker;
                                    # defaults to the render's grandparent
        [--advisory]

A render that cannot be read is a HARD failure, never a pass. Both source
copies got this wrong in different ways -- one printed
"0 steps ... PASS (0 static runs over limit)" and exited 0 for a path that did
not exist, the other raised a ValueError out of a reshape. A gate that reports
clean on no data is worse than no gate.

Provenance: `videos/collagen-where-did-it-go` (the grid test, --eps-local's
measured default, --exempt-window, --exempt-last) and
`videos/ectoin-survival-molecule` (--exempt-marker, derived from the scene that
declares the end-screen reserve rather than from scene order).
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

W, H = 480, 270          # analysis size
GRID_COLS, GRID_ROWS = 6, 4


def lumas(path, fps):
    cmd = ["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"fps={fps},scale={W}:{H}",
           "-f", "rawvideo", "-pix_fmt", "gray", "-"]
    r = subprocess.run(cmd, capture_output=True, check=False)
    n = len(r.stdout) // (W * H)
    if n < 2:
        err = (r.stderr or b"").decode(errors="replace").strip().splitlines()
        sys.exit(f"FATAL: read {n} frame(s) from {path} -- nothing to measure."
                 + (f"\n  ffmpeg: {err[-1]}" if err else "")
                 + "\n  A missing or unreadable render is a failure, not a pass.")
    return np.frombuffer(r.stdout[: n * W * H], dtype=np.uint8).reshape(n, H, W).astype(np.int16)


def cell_max(diff):
    """Largest per-cell mean |delta| over a GRID_COLS x GRID_ROWS grid."""
    ch, cw = H // GRID_ROWS, W // GRID_COLS
    cells = diff[:, : ch * GRID_ROWS, : cw * GRID_COLS]
    cells = cells.reshape(cells.shape[0], GRID_ROWS, ch, GRID_COLS, cw)
    return cells.mean(axis=(2, 4)).reshape(cells.shape[0], -1).max(axis=1)


def scenes(project_root):
    """[(cid, start)] in document order, from the built index.html.

    Matches on the ATTRIBUTES, never on their order: this repo's preview server
    injects data-hf-id as the first attribute on every tag, and a pattern
    anchored to a tag's opening bytes silently stops matching.
    """
    idx = Path(project_root) / "index.html"
    if not idx.exists():
        return []
    return [(cid, float(t)) for cid, t in re.findall(
        r'data-composition-id="([^"]+)"[^>]*?data-start="([0-9.]+)"', idx.read_text())]


def exempt_start(a):
    root = Path(a.project_root) if a.project_root else Path(a.render).resolve().parent.parent
    sc = scenes(root)
    if not sc:
        if a.exempt_last or a.exempt_marker:
            sys.exit(f"FATAL: --exempt-last/--exempt-marker need {root}/index.html")
        return None
    if a.exempt_marker:
        for cid, t in sc:
            f = root / "compositions" / "frames" / f"{cid}.html"
            if f.exists() and a.exempt_marker in f.read_text():
                print(f"  --exempt-marker {a.exempt_marker!r}: first declared by {cid}; "
                      f"runs from {t:.2f}s are the authored hold")
                return t
        sys.exit(f"FATAL: no scene's composition contains {a.exempt_marker!r}")
    if a.exempt_last:
        cid, t = max(sc, key=lambda x: x[1])
        print(f"  --exempt-last: runs from {t:.2f}s ({cid}) are the authored hold")
        return t
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("render")
    ap.add_argument("--fps", type=float, default=4)
    ap.add_argument("--eps", type=float, default=0.35)
    ap.add_argument("--eps-local", type=float, default=0.9,
                    help="per-cell mean |delta| that counts as motion on its own")
    ap.add_argument("--open", type=float, default=2.0)
    ap.add_argument("--open-until", type=float, default=31.0)
    ap.add_argument("--rest", type=float, default=4.0)
    ap.add_argument("--exempt-window", action="append", default=[], metavar="START-END")
    ap.add_argument("--exempt-last", action="store_true")
    ap.add_argument("--exempt-marker")
    ap.add_argument("--project-root")
    ap.add_argument("--advisory", action="store_true")
    a = ap.parse_args()

    if not Path(a.render).exists():
        sys.exit(f"FATAL: render not found: {a.render}")
    windows = [tuple(float(x) for x in w.split("-")) for w in a.exempt_window]
    frm = exempt_start(a)

    L = lumas(a.render, a.fps)
    diff = np.abs(np.diff(L, axis=0))
    d = diff.mean(axis=(1, 2))
    dl = cell_max(diff)
    step = 1.0 / a.fps

    runs, start = [], None
    for i, v in enumerate(d):
        if v < a.eps and dl[i] < a.eps_local:
            if start is None:
                start = i
        elif start is not None:
            runs.append((start, i))
            start = None
    if start is not None:
        runs.append((start, len(d)))

    fails = 0
    for s, e in runs:
        t0, t1 = s * step, (e + 1) * step
        limit = a.open if t0 < a.open_until else a.rest
        if t1 - t0 <= limit:
            continue
        if frm is not None and t0 >= frm - 0.01:
            print(f"  static {t0:7.2f}-{t1:7.2f}s  ({t1 - t0:4.1f}s) -- inside the "
                  f"authored closing hold, exempt")
            continue
        if any(lo - 0.05 <= t0 and t1 <= hi + 0.05 for lo, hi in windows):
            print(f"  static {t0:7.2f}-{t1:7.2f}s  ({t1 - t0:4.1f}s) -- inside a "
                  f"reviewed window, exempt")
            continue
        fails += 1
        print(f"  static {t0:7.2f}-{t1:7.2f}s  ({t1 - t0:4.1f}s > {limit}s)")

    print(f"{len(d)} steps @ {a.fps}fps, eps {a.eps} frame / {a.eps_local} local: "
          f"{'PASS' if fails == 0 else 'FAIL'} ({fails} static run(s) over limit)")
    return 0 if (fails == 0 or a.advisory) else 1


if __name__ == "__main__":
    sys.exit(main())
