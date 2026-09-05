#!/usr/bin/env python3
"""Retention rule on RENDERED pixels: no static period longer than
`--open` seconds inside the first `--open-until` seconds, and none longer
than `--rest` seconds after that. "Static" = consecutive 4 fps samples whose
mean |luma delta| stays under `--eps` (frame-average, 0-255 scale).

    python3 scripts/check-motion-gaps.py renders/<file>.mp4
"""
import argparse, subprocess, sys
import numpy as np

W, H = 480, 270   # analysis size; motion is a frame-average measure
ROOT = __import__("pathlib").Path(__file__).resolve().parent.parent


def endscreen_start():
    """data-start of the first scene that carries the end-screen reserve."""
    import re
    html = (ROOT / "index.html").read_text()
    for cid, t in re.findall(
            r'data-composition-id="([^"]+)"[^>]*?data-start="([0-9.]+)"', html):
        f = ROOT / "compositions" / "frames" / f"{cid}.html"
        if f.exists() and "var(--endscreen-right)" in f.read_text():
            return float(t)
    return None


def lumas(path, fps):
    cmd = ["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps={fps},scale={W}:{H}",
           "-f", "rawvideo", "-pix_fmt", "gray", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    n = len(raw) // (W * H)
    return np.frombuffer(raw[: n * W * H], dtype=np.uint8).reshape(n, H, W).astype(np.int16)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("render"); ap.add_argument("--fps", type=float, default=4)
    ap.add_argument("--eps", type=float, default=0.35)
    ap.add_argument("--open", type=float, default=2.0); ap.add_argument("--open-until", type=float, default=31.0)
    ap.add_argument("--rest", type=float, default=4.0)
    # The end-screen scenes are calm on purpose: YouTube draws its own overlay
    # cards over the final 5-20s and competing movement under them reads as
    # clutter (frames_a27.py S29). Derived from index.html rather than typed,
    # so it follows the walk instead of freezing a timestamp.
    ap.add_argument("--exempt-endscreen", action="store_true", default=True)
    ap.add_argument("--no-exempt-endscreen", dest="exempt_endscreen",
                    action="store_false")
    a = ap.parse_args()
    exempt_from = endscreen_start() if a.exempt_endscreen else None
    L = lumas(a.render, a.fps)
    d = np.abs(np.diff(L, axis=0)).mean(axis=(1, 2))   # d[i] = change between sample i and i+1
    step = 1.0 / a.fps
    runs, start = [], None
    for i, v in enumerate(d):
        if v < a.eps:
            if start is None: start = i
        else:
            if start is not None: runs.append((start, i)); start = None
    if start is not None: runs.append((start, len(d)))
    fails = 0
    for s, e in runs:
        t0, t1 = s * step, (e + 1) * step
        limit = a.open if t0 < a.open_until else a.rest
        if exempt_from is not None and t0 >= exempt_from:
            print(f"  static {t0:7.2f}-{t1:7.2f}s  ({t1 - t0:4.1f}s) -- end-screen "
                  f"scene, calm by design, exempt")
            continue
        if t1 - t0 > limit:
            fails += 1
            print(f"  static {t0:7.2f}-{t1:7.2f}s  ({t1 - t0:4.1f}s > {limit}s)")
    print(f"{len(d)} steps @ {a.fps}fps, eps {a.eps}: {'PASS' if fails == 0 else 'FAIL'} ({fails} static runs over limit)")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
