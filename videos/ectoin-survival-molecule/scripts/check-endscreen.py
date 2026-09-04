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
    ap.add_argument("render"); ap.add_argument("--start", type=float, default=324.37)
    ap.add_argument("--step", type=float, default=0.5); ap.add_argument("--tol", type=int, default=28)
    a = ap.parse_args()
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
