#!/usr/bin/env python3
"""End-screen clearance on the RENDERED pixels: from `start` seconds to the
end, the right third (x >= 1280) and the lower-right (x >= 960, y >= 780)
must carry no ink -- every pixel within `tol` of the page ground.

    python3 scripts/check-endscreen.py renders/<file>.mp4 [--start 324.37]
"""
import argparse, subprocess, sys
import numpy as np

W, H = 1920, 1080
PAPER = np.array([247, 245, 240])


def frames(path, start, step):
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{start:.3f}", "-i", path, "-vf", f"fps=1/{step}",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    n = len(raw) // (W * H * 3)
    return np.frombuffer(raw[: n * W * H * 3], dtype=np.uint8).reshape(n, H, W, 3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("render")
    # DERIVED, not carried over. This default was 325.3 -- a constant from the
    # project this file came from. A hardcoded start on a different edit samples
    # the wrong scene and reports a clean pass on frames the end screen never
    # touches. The closing scene's own data-start is read from index.html, plus
    # the curtain wipe so the outgoing ground is never sampled mid-transition.
    ap.add_argument("--start", type=float, default=None)
    ap.add_argument("--curtain", type=float, default=0.9,
                    help="closing wipe duration, skipped before sampling")
    ap.add_argument("--step", type=float, default=0.5); ap.add_argument("--tol", type=int, default=28)
    a = ap.parse_args()
    if a.start is None:
        import re as _re
        from pathlib import Path as _P
        idx = _P(a.render).resolve().parent.parent / "index.html"
        if not idx.exists():
            print(f"check-endscreen: no index.html beside {a.render}; pass --start explicitly")
            return 2
        starts = [float(m) for tag in _re.findall(r'<div[^>]*class="[^"]*\bscene\b[^"]*"[^>]*>', idx.read_text())
                  for m in _re.findall(r'data-start="([\d.]+)"', tag)]
        if not starts:
            print("check-endscreen: index.html has no scene clips; pass --start explicitly")
            return 2
        a.start = max(starts) + a.curtain + 0.2
        print(f"  closing scene starts {max(starts):.2f}s; sampling the reserve from {a.start:.2f}s")
    fr = frames(a.render, a.start, a.step)
    bad = 0
    for i, f in enumerate(fr):
        t = a.start + i * a.step
        right = f[:, 1280:, :]; lower = f[780:, 960:, :]
        for name, zone in (("right-third", right), ("lower-right", lower)):
            d = np.abs(zone.astype(int) - PAPER).max(axis=2)
            ink = int((d > a.tol).sum())
            if ink > 40:
                bad += 1
                print(f"  t={t:7.2f}s  {name:12s}  {ink} px off-ground")
    print(f"{len(fr)} frames from {a.start}s; {'PASS' if bad == 0 else 'FAIL'} ({bad} zone hits)")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
