#!/usr/bin/env python3
"""End-screen clearance on the RENDERED pixels: from the closing scenes' start
to the end, the right third (x >= 1280) and the lower-right (x >= 960, y >= 780)
must be EMPTY -- uniform, whatever colour that zone happens to be.

Two things were hardcoded here and both were wrong the moment the edit moved:

  * `--start 325.3`, a constant carried over from the cut that measured it. A
    fixed start on a longer edit samples the wrong scenes and reports a clean
    pass on frames the end screen never touches. It is read from index.html now.
  * a `PAPER` ground. The 2026-09-05 pass added an INK-ground end card, and a
    checker that defines "empty" as "close to paper" reports an entire
    correctly-empty ink zone as 100% ink. Emptiness is UNIFORMITY, not a colour:
    each zone is compared against its own median instead.

    python3 scripts/check-endscreen.py renders/<file>.mp4 [--start 353.9]
"""
import argparse, re, subprocess, sys
from pathlib import Path

import numpy as np

W, H = 1920, 1080
ROOT = Path(__file__).resolve().parent.parent


def closing_start():
    """data-start of the first scene that carries the end-screen reserve.

    Read from the built index.html, so it follows the walk. Falls back to the
    last scene if the reserve marker cannot be found -- never to a constant."""
    html = (ROOT / "index.html").read_text()
    scenes = re.findall(r'data-composition-id="([^"]+)"[^>]*?data-start="([0-9.]+)"', html)
    reserved = [(cid, float(t)) for cid, t in scenes
                if (ROOT / "compositions" / "frames" / f"{cid}.html").exists()
                # the token is DEFINED in every frame's inlined preamble, so the
                # test is whether the scene USES it -- `var(--endscreen-right)`
                and "var(--endscreen-right)" in
                (ROOT / "compositions" / "frames" / f"{cid}.html").read_text()]
    if not reserved:
        sys.exit("check-endscreen: no scene declares the end-screen reserve "
                 "(--endscreen-right); nothing to check against")
    cid, t = reserved[0]
    # plus the settle wipe, so the outgoing scene's ground is never sampled
    # mid-transition
    return cid, t + 0.90


def frames(path, start, step):
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{start:.3f}", "-i", path, "-vf", f"fps=1/{step}",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    n = len(raw) // (W * H * 3)
    return np.frombuffer(raw[: n * W * H * 3], dtype=np.uint8).reshape(n, H, W, 3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("render"); ap.add_argument("--start", type=float, default=None)
    ap.add_argument("--step", type=float, default=0.5); ap.add_argument("--tol", type=int, default=28)
    a = ap.parse_args()
    cid, derived = closing_start()
    if a.start is None:
        a.start = derived
    print(f"[endscreen] reserve begins at {cid} -> sampling from {a.start:.2f}s")
    fr = frames(a.render, a.start, a.step)
    bad = 0
    for i, f in enumerate(fr):
        t = a.start + i * a.step
        right = f[:, 1280:, :]; lower = f[780:, 960:, :]
        for name, zone in (("right-third", right), ("lower-right", lower)):
            z = zone.astype(int)
            ground = np.median(z.reshape(-1, 3), axis=0)
            d = np.abs(z - ground).max(axis=2)
            ink = int((d > a.tol).sum())
            if ink > 40:
                bad += 1
                print(f"  t={t:7.2f}s  {name:12s}  {ink} px off-ground")
    print(f"{len(fr)} frames from {a.start}s; {'PASS' if bad == 0 else 'FAIL'} ({bad} zone hits)")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
