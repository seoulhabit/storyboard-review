#!/usr/bin/env python3
"""Measure how much of a render actually carries visible motion, per scene.

This is a DIFFERENT question from check-static-hold.py's, and the distinction
is the whole reason this file exists. That script asks "is anything frozen?"
via PSNR between consecutive samples, with a frozen threshold of ~55dB. This
one asks "is anything *perceptible* happening?" -- and a scene can answer yes
to the first and no to the second, because sub-perceptual drift keeps breaking
a frozen run before it ever reaches the ceiling.

PROVENANCE. Written in `videos/pilling-vs-peeling` (round 4, 2026-09-01),
copied verbatim into `videos/ectoin-survival-molecule` (which added the
`--longform` ceiling for the channel's first 16:9 piece), harvested into the
catalog 2026-09-02. The inherited docstring opened "Confirmed on this project,
2026-09-01 (round 4): 06-fix-pilling's three demo beats..." -- and `06-fix-
pilling` is a scene that exists only in pilling-vs-peeling. Read inside the
Ectoin copy, that sentence pointed at a file which was not there: provenance
drift, the same copy-the-comment-along-with-the-context failure this catalog's
check-static-hold.py entry documents for caption bands. Every "confirmed on"
below now names the project it was actually confirmed on, and none of them
says "this project".

CONFIRMED ON `videos/pilling-vs-peeling`, 2026-09-01 (round 4): 06-fix-
pilling's three demo beats animated 12px strokes inside a 56px glyph --
roughly 48px^2 of change on a 2,073,600px canvas. They fired correctly on
every frame, measured 0.0001-0.012 mean |dLuma| per 8fps step, and no viewer
could see any of them. check-static-hold.py reported 0 findings on that scene,
truthfully: the 0.003-ish drift is not "frozen," it is just invisible. Only a
threshold set at a real-but-low perceptibility floor separates the two.

ENCODER-ARTIFACT REJECTION, and why a mean-only threshold is not enough.
An h264 keyframe refresh shifts the whole frame by a few luma levels at once.
That registers as a LARGE mean delta with a TINY per-pixel maximum -- measured
on pilling-vs-peeling at mean 5.208 with maxpix 12.0, which a mean-only test
happily counts as a strong beat. Real motion is the inverse: localised, so a
modest mean sits under a large per-pixel max. That project's round-3 record
credited 07-fix-peeling with "8% active steps" on exactly two such artifacts;
the scene in fact had no qualifying beat at all. A step therefore has to clear
BOTH thresholds to count.

Scene boundaries come from index.html, via check-static-hold.py's own parser,
so the two scripts always agree about where the scenes are. In the catalog
that parser is the sibling `check-static-hold.py` in this directory.

SCOPE, and what this script does NOT measure -- see the closing summary, which
names it in the output rather than leaving it in a docstring nobody re-reads.
Advisory: always exits 0. It reports; it does not gate.
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
                       # --longform (alias --landscape) raises it to 6.0: the long-form
                       # cadence budget is 8-12s, and 1.6/2.5 = 0.64 of the target, so
                       # 0.64 x ~9.5 ~= 6.
                       # Both cadence figures are CRAFT BUDGETS, not measured thresholds
                       # (channel-baseline-analysis-2026-09-01.md section 7 lists both as
                       # unbacked by channel data) -- never cite a finding here as proof
                       # of a performance problem.
CANVAS_CUT_DELTA = 60.0  # steps this large are scene cuts, not internal motion
BOUNDARY_SKIP_S = 0.13   # skip this much of each scene after its start before measuring.
                         # The first sampled step inside a scene straddles the cut: its
                         # tblend difference is against the LAST frame of the previous
                         # scene, so at 8fps (0.125s/step) it reports the cut, not the
                         # scene. One step plus a rounding margin is exactly what has to
                         # go. Unnamed in the inherited copy (a bare `s + 0.13`), which
                         # made it look like a tuned fudge rather than one sample period.

LONGFORM_FLAGS = ("--longform", "--landscape")   # --landscape is an alias, matching
                                                 # check-static-hold.py / check-safe-area.py,
                                                 # whose landscape flag is spelled that way.


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


def _flags(argv):
    """--ceiling <s>, --exempt-last and --gate, stripped from argv.

    These were passed by package.json and SILENTLY IGNORED: the old filter kept
    only the profile flag, so `--ceiling` landed in argv[0] and became the
    project root while the ceiling stayed at its profile default. A gate that
    is handed a stricter number and quietly uses a looser one is worse than no
    gate, because its PASS line names the number it was given."""
    out, ceiling, exempt_last, gate = [], None, False, False
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--ceiling":
            ceiling = float(argv[i + 1]); i += 2; continue
        if a == "--exempt-last":
            exempt_last = True; i += 1; continue
        if a == "--gate":
            gate = True; i += 1; continue
        out.append(a); i += 1
    return out, ceiling, exempt_last, gate


def main():
    global QUIET_CEILING_S
    argv = [a for a in sys.argv[1:] if a not in LONGFORM_FLAGS]
    if any(f in sys.argv for f in LONGFORM_FLAGS):
        QUIET_CEILING_S = 6.0
    argv, ceiling, exempt_last, gate = _flags(argv)
    if ceiling is not None:
        QUIET_CEILING_S = ceiling   # AFTER the profile, or the profile wins

    project_root = Path(argv[0] if len(argv) > 0 else ".").resolve()
    if len(argv) > 1:
        render_path = Path(argv[1])
    else:
        renders = sorted((project_root / "renders").glob("*.mp4"),
                         key=lambda p: p.stat().st_mtime)
        render_path = renders[-1] if renders else None
    if not render_path or not render_path.exists():
        print("check-cadence: no render found - skipping.")
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
    print(f"Cadence scan - {render_path.name}, {SAMPLE_FPS:.0f}fps, "
          f"beat = mean|dLuma| >= {MEAN_ACTIVE} AND maxpix >= {MIN_MAXPIX}.")
    print(f"  whole video: {n_act}/{len(body)} steps carry a visible beat "
          f"({100*n_act/max(len(body),1):.1f}%)")

    findings = []
    if scenes:
        print(f"\n  {'scene':>6}  {'window':>16}  {'beats':>10}  longest quiet run")
        for i, (s, e) in enumerate(scenes, 1):
            seg = [r for r in rows if s + BOUNDARY_SKIP_S < r["t"] < e - 0.001]
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
            last = (i == len(scenes))
            bad = quiet > QUIET_CEILING_S and not (exempt_last and last)
            if bad:
                findings.append((i, s, e, quiet, brs, bre))
            print(f"  {i:>6}  {s:6.2f}-{e:5.2f}  {len(a):>3}/{len(seg):<3} "
                  f"{100*len(a)/len(seg):>3.0f}%  {quiet:5.2f}s"
                  f"{'  <-- over ceiling' if bad else ''}")

    # Scope the summary to what was actually MEASURED. The inherited line was
    # "Overall: clean (no scene exceeds the quiet ceiling)", which reads as a
    # verdict on the edit and is not one -- the same defect catalogued for
    # check-static-hold.py's own "Overall: clean" (see this directory's
    # README.md, "the summary line asserted more than it tested"). Two things
    # this pass structurally cannot see are named below rather than left in a
    # docstring, because the summary is what gets pasted into a delivery note.
    print("\n  Measured: per-scene longest run of consecutive 8fps steps with no "
          "perceptible,\n  localised change, and the whole-video share of steps that "
          "do carry one.")
    print("  NOT measured: a region that stays FROZEN while still carrying content "
          "(the\n  same mode-4 blind spot check-static-hold.py documents - a beat "
          "anywhere in\n  the frame keeps this scan alive); and structural sameness - "
          "29 scenes with\n  one enter/wash/hold shape and one entrance ease measure as "
          "'paced' here.\n  That second question belongs to continuity-audit.py, not to "
          "this script.")

    if findings:
        print(f"\n  {len(findings)} scene(s) over the {QUIET_CEILING_S}s quiet ceiling:")
        for i, s, e, q, a, b in findings:
            print(f"    scene {i} ({s:.2f}-{e:.2f}s): {q:.2f}s with no visible "
                  f"beat, {a:.2f}-{b:.2f}s")
        print("  Verify each: does it need a beat, or is it a deliberate hold?")
    else:
        print(f"\n  Result: no scene exceeds the {QUIET_CEILING_S}s quiet ceiling"
              f"{' (last scene exempt)' if exempt_last else ''}.")
    return 1 if (findings and gate) else 0


if __name__ == "__main__":
    sys.exit(main())
