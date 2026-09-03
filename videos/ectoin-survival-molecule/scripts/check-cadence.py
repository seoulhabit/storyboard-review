#!/usr/bin/env python3
"""Measure how much of a render actually carries visible motion, per scene.

This is a DIFFERENT question from check-static-hold.py's, and the distinction
is the whole reason this file exists. That script asks "is anything frozen?"
via PSNR between consecutive samples, with a frozen threshold of ~55dB. This
one asks "is anything *perceptible* happening?" — and a scene can answer yes
to the first and no to the second, because sub-perceptual drift keeps breaking
a frozen run before it ever reaches the ceiling.

Confirmed on this project, 2026-09-01 (round 4): 06-fix-pilling's three demo
beats animated 12px strokes inside a 56px glyph — roughly 48px^2 of change on
a 2,073,600px canvas. They fired correctly on every frame, measured
0.0001-0.012 mean |dLuma| per 8fps step, and no viewer could see any of them.
check-static-hold.py reported 0 findings on that scene, truthfully: the
0.003-ish drift is not "frozen," it is just invisible. Only a threshold set at
a real-but-low perceptibility floor separates the two.

ENCODER-ARTIFACT REJECTION, and why a mean-only threshold is not enough.
An h264 keyframe refresh shifts the whole frame by a few luma levels at once.
That registers as a LARGE mean delta with a TINY per-pixel maximum — measured
here at mean 5.208 with maxpix 12.0, which a mean-only test happily counts as
a strong beat. Real motion is the inverse: localised, so a modest mean sits
under a large per-pixel max. Round 3's own record credited 07-fix-peeling with
"8% active steps" on exactly two such artifacts; the scene in fact had no
qualifying beat at all. A step therefore has to clear BOTH thresholds to count.

Scene boundaries come from index.html, via check-static-hold.py's own parser,
so the two scripts always agree about where the scenes are.
"""

import re
import subprocess
import sys
from pathlib import Path

SAMPLE_FPS = 8.0
MEAN_ACTIVE = 1.0      # mean |dLuma| (0-255) for a step to count as a beat
MIN_MAXPIX = 40.0      # ...and it must be LOCALISED, not a global codec shift
QUIET_CEILING_S = 1.6  # longest run of non-active steps tolerated inside a scene.
                       # SHORTS value, against the 1.5-3s shorts cadence target.
                       # --longform raises it to 6.0: the long-form cadence budget is
                       # 8-12s, and 1.6/2.5 = 0.64 of the target, so 0.64 x ~9.5 ~= 6.
                       # Both cadence figures are CRAFT BUDGETS, not measured thresholds
                       # (channel-baseline-analysis-2026-09-01.md section 7 lists both as
                       # unbacked by channel data) -- never cite a finding here as proof
                       # of a performance problem.
CANVAS_CUT_DELTA = 60.0  # steps this large are scene cuts, not internal motion


def sample(render_path, start=None, end=None):
    cmd = ["ffmpeg", "-nostdin", "-hide_banner"]
    if start is not None:
        cmd += ["-ss", str(start), "-to", str(end)]
    cmd += ["-i", str(render_path), "-vf",
            (f"fps={SAMPLE_FPS},format=gray,tblend=all_mode=difference,"
             "signalstats,metadata=print"), "-f", "null", "-"]
    out = subprocess.run(cmd, capture_output=True, text=True, check=False).stderr
    toks = re.findall(r"pts_time:([0-9.]+)|YAVG=([0-9.]+)|YMAX=([0-9.]+)", out)
    rows, cur = [], {}
    for t, avg, mx in toks:
        if t:
            cur = {"t": float(t)}
        elif avg:
            cur["mean"] = float(avg)
        elif mx:
            cur["max"] = float(mx)
            rows.append(cur)
    return rows


def active(r):
    return r["mean"] >= MEAN_ACTIVE and r["max"] >= MIN_MAXPIX


def main():
    global QUIET_CEILING_S
    argv = [a for a in sys.argv[1:] if a != "--longform"]
    if "--longform" in sys.argv:
        QUIET_CEILING_S = 6.0

    project_root = Path(argv[0] if len(argv) > 0 else ".").resolve()
    if len(argv) > 1:
        render_path = Path(argv[1])
    else:
        renders = sorted((project_root / "renders").glob("*.mp4"),
                         key=lambda p: p.stat().st_mtime)
        render_path = renders[-1] if renders else None
    if not render_path or not render_path.exists():
        print("check-cadence: no render found — skipping.")
        return 0

    sys.path.insert(0, str(Path(__file__).parent))
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "csh", Path(__file__).parent / "check-static-hold.py")
    csh = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(csh)
    scenes = csh.scene_boundaries(project_root) or []

    rows = sample(render_path)
    body = [r for r in rows if r["mean"] < CANVAS_CUT_DELTA]
    n_act = sum(1 for r in body if active(r))
    print(f"Cadence scan — {render_path.name}, {SAMPLE_FPS:.0f}fps, "
          f"beat = mean|dLuma| >= {MEAN_ACTIVE} AND maxpix >= {MIN_MAXPIX}.")
    print(f"  whole video: {n_act}/{len(body)} steps carry a visible beat "
          f"({100*n_act/max(len(body),1):.1f}%)")

    findings = []
    if scenes:
        print(f"\n  {'scene':>6}  {'window':>16}  {'beats':>10}  longest quiet run")
        for i, (s, e) in enumerate(scenes, 1):
            seg = [r for r in rows if s + 0.13 < r["t"] < e - 0.001]
            if not seg:
                continue
            a = [r for r in seg if active(r)]
            run = best = 0
            brs = bre = None
            rs = None
            for r in seg:
                if not active(r):
                    if rs is None:
                        rs = r["t"]
                    run += 1
                    if run > best:
                        best, brs, bre = run, rs, r["t"]
                else:
                    run, rs = 0, None
            quiet = best / SAMPLE_FPS
            bad = quiet > QUIET_CEILING_S
            if bad:
                findings.append((i, s, e, quiet, brs, bre))
            print(f"  {i:>6}  {s:6.2f}-{e:5.2f}  {len(a):>3}/{len(seg):<3} "
                  f"{100*len(a)/len(seg):>3.0f}%  {quiet:5.2f}s"
                  f"{'  <-- over ceiling' if bad else ''}")

    if findings:
        print(f"\n  {len(findings)} scene(s) over the {QUIET_CEILING_S}s quiet ceiling:")
        for i, s, e, q, a, b in findings:
            print(f"    scene {i} ({s:.2f}-{e:.2f}s): {q:.2f}s with no visible "
                  f"beat, {a:.2f}-{b:.2f}s")
        print("  Verify each: does it need a beat, or is it a deliberate hold?")
    else:
        print("\n  Overall: clean (no scene exceeds the quiet ceiling).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
