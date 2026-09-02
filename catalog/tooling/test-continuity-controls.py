#!/usr/bin/env python3
"""Self-contained controls for continuity-audit.py.

Run after ANY change to its parsing, its classification, or its heuristics:

    python3 catalog/tooling/test-continuity-controls.py

Why this exists. Every number continuity-audit.py prints comes out of a
hand-written JavaScript scanner, and a scanner that quietly stops matching
does not crash -- it reports a smaller, tidier project. "0 transitions" from a
piece that is all cuts and "0 transitions" from a broken tween scan are the
same string. So the controls are built in opposite directions: one synthetic
project that is deliberately the failure the tool exists to name, one that is
deliberately the fix, and one that is the single hard violation.

  SLIDES     3 contiguous scenes, alternating grounds, every tween
             {opacity,y} inheriting one defaults:{ease}, and the same circle
             redrawn in scenes 2 and 3
             -> 2 cuts, 0 transitions, ONE signature at 100%, 1 rebuilt pair,
                0 camera moves. If any of these drifts, the tool has stopped
                seeing the shape it was written to name.

  FILM       the same three beats built for continuity: authored overlaps with
             root push / blur tweens, six different entrance idioms, a .stage
             camera drift, no shared geometry
             -> 0 cuts, 2 transitions (push then blur), top signature < 50%,
                0 rebuilt pairs, >= 1 camera move. This is the control that
                catches a scanner blinded into always reporting "slides".

  VIOLATION  an opacity-only root tween across a ground change -- the one
             documented muddy-midpoint rule
             -> --gate must exit 2, and a plain run must still exit 0.

No project assets, no render, no ffmpeg: everything is written into a tempdir.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

TOOL = Path(__file__).resolve().parent / "continuity-audit.py"

SCENE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>__CID__</title></head>
<body>
<template>
  <div id="root" data-composition-id="__CID__"
       data-width="1920" data-height="1080" data-duration="__DUR__">
    <style>
      #root {
        --paper:#F7F5F0; --ink:#131516; --aqua:#59B8AE;
      }
      #root { position:absolute; inset:0; overflow:hidden; }
      #root { background:var(__GROUND__); color:var(--ink); }
    </style>
    <div class="stage">
__BODY__
    </div>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    var tl = gsap.timeline({ paused: true, defaults: { ease: "power3.out" } });
__TWEENS__
    tl.to({}, { duration: __DUR__ }, 0);   // full-span anchor -- always last
    window.__timelines["__CID__"] = tl;
  </script>
</template>
</body></html>
"""

INDEX = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"></head>
<body>
  <div id="root" data-composition-id="main" data-width="1920" data-height="1080"
       data-duration="__TOTAL__">
__CLIPS__
  </div>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    var tl = gsap.timeline({ paused: true });
__ROOT__
    tl.to({}, { duration: __TOTAL__ }, 0);
    window.__timelines["main"] = tl;
  </script>
</body></html>
"""

CLIP = ('    <div id="scene-__CID__" class="scene clip" data-composition-id="__CID__"\n'
        '         data-composition-src="compositions/frames/__CID__.html"\n'
        '         data-start="__START__" data-duration="__DUR__" '
        'data-track-index="__TRACK__"></div>')

CIRCLE = ('      <svg viewBox="0 0 620 620"><circle id="__ID__" cx="310" cy="310" '
          'r="__R__" fill="#131516"/></svg>')


def fill(tpl, **kw):
    for k, v in kw.items():
        tpl = tpl.replace(f"__{k}__", str(v))
    return tpl


def write_project(root, scenes, root_tweens=""):
    (root / "compositions" / "frames").mkdir(parents=True)
    clips, total = [], 0.0
    for s in scenes:
        clips.append(fill(CLIP, CID=s["cid"], START=f'{s["start"]:.3f}',
                          DUR=f'{s["dur"]:.3f}', TRACK=s.get("track", 0)))
        total = max(total, s["start"] + s["dur"])
        (root / "compositions" / "frames" / f'{s["cid"]}.html').write_text(
            fill(SCENE, CID=s["cid"], DUR=f'{s["dur"]:.3f}', GROUND=s["ground"],
                 BODY=s["body"], TWEENS=s["tweens"]))
    (root / "index.html").write_text(
        fill(INDEX, TOTAL=f"{total:.3f}", CLIPS="\n".join(clips), ROOT=root_tweens))


# ------------------------------------------------------------------ fixtures
ARRIVE = ("  tl.fromTo('#__ID__', {{ opacity:0, y:20 }},\n"
          "                       {{ opacity:1, y:0, duration:0.55 }}, {t});")


def arrive(i, t):
    return ARRIVE.replace("__ID__", f"a{i}").format(t=t)


def slides_scenes():
    return [
        {"cid": "s1", "start": 0.0, "dur": 5.0, "ground": "--ink",
         "body": '      <p id="a1">one</p>\n      <p id="a2">two</p>',
         "tweens": arrive(1, 0.2) + "\n" + arrive(2, 1.2)},
        {"cid": "s2", "start": 5.0, "dur": 5.0, "ground": "--paper",
         "body": '      <p id="a3">three</p>\n' + fill(CIRCLE, ID="c1", R="112"),
         "tweens": arrive(3, 0.2) + "\n" + arrive(4, 1.2)},
        {"cid": "s3", "start": 10.0, "dur": 5.0, "ground": "--ink",
         "body": '      <p id="a5">five</p>\n' + fill(CIRCLE, ID="c2", R="112"),
         "tweens": arrive(5, 0.2) + "\n" + arrive(6, 1.2)},
    ]


FILM_ROOT = """    tl.fromTo('#scene-f1', { xPercent: 0 },
                            { xPercent: -100, duration: 0.5, ease: 'power2.inOut' }, 5.0);
    tl.fromTo('#scene-f2', { xPercent: 100 },
                            { xPercent: 0, duration: 0.5, ease: 'power2.inOut' }, 5.0);
    tl.fromTo('#scene-f3', { opacity: 0, filter: 'blur(20px)' },
                            { opacity: 1, filter: 'blur(0px)', duration: 0.6,
                              ease: 'power1.inOut' }, 10.0);"""


def film_scenes():
    return [
        {"cid": "f1", "start": 0.0, "dur": 5.5, "ground": "--ink", "track": 0,
         "body": '      <p id="b1">one</p>\n' + fill(CIRCLE, ID="d1", R="90"),
         "tweens": ("  tl.fromTo('#b1', { opacity:0, scale:1.12 },\n"
                    "                   { opacity:1, scale:1, duration:0.40,\n"
                    "                     ease:'power4.out' }, 0.20);\n"
                    "  tl.fromTo('#d1', { clipPath:'inset(0 100% 0 0)' },\n"
                    "                   { clipPath:'inset(0 0% 0 0)', duration:0.50,\n"
                    "                     ease:'power2.inOut' }, 0.90);")},
        {"cid": "f2", "start": 5.0, "dur": 5.6, "ground": "--paper", "track": 1,
         "body": '      <p id="b2">two</p>\n' + fill(CIRCLE, ID="d2", R="140"),
         "tweens": ("  tl.to('.stage', { x:6, y:-4, scale:1.01, duration:3.00,\n"
                    "                    ease:'sine.inOut' }, 0.40);\n"
                    "  tl.to('#b2', { scaleY:1.0, duration:0.60, ease:'back.out(1.6)' }, 0.30);")},
        {"cid": "f3", "start": 10.0, "dur": 5.0, "ground": "--ink", "track": 0,
         "body": '      <p id="b3">three</p>\n' + fill(CIRCLE, ID="d3", R="200"),
         "tweens": ("  tl.fromTo('#b3', { opacity:0, y:20 },\n"
                    "                   { opacity:1, y:0, duration:0.55 }, 0.20);\n"
                    "  tl.to('#d3', { rotation:180, duration:0.80, ease:'power1.out' }, 1.10);")},
    ]


VIOLATION_ROOT = """    tl.fromTo('#scene-v2', { opacity: 0 },
                            { opacity: 1, duration: 0.5, ease: 'power1.inOut' }, 5.0);"""


def violation_scenes():
    return [
        {"cid": "v1", "start": 0.0, "dur": 5.5, "ground": "--ink",
         "body": '      <p id="g1">one</p>', "tweens": arrive(1, 0.2)},
        {"cid": "v2", "start": 5.0, "dur": 5.0, "ground": "--paper",
         "body": '      <p id="g2">two</p>', "tweens": arrive(2, 0.2)},
    ]


# ------------------------------------------------------------------- measure
PATTERNS = {
    "cuts": r"transitions: \d+ of \d+\s+hard cuts: (\d+)",
    "transitions": r"transitions: (\d+) of \d+",
    "boundaries": r"transitions: \d+ of (\d+)",
    "ground_changes": r"ground changes \(\*\): (\d+) of",
    "violations": r"plain-crossfade-across-ground violations: (\d+)",
    "top_sig": r"top entrance signature share\s+: ([\d.]+)%",
    "pairs": r"rebuilt-actor pairs / merged scenes: (\d+) /",
    "merged": r"rebuilt-actor pairs / merged scenes: \d+ / (\d+)",
    "camera": r"camera moves\s+: (\d+)",
}


def measure(out):
    got = {}
    for k, pat in PATTERNS.items():
        m = re.search(pat, out)
        got[k] = (float(m.group(1)) if k == "top_sig" else int(m.group(1))) if m else None
    return got


def run(kind, scenes, root_tweens="", gate=False):
    with tempfile.TemporaryDirectory() as tmp:
        proj = Path(tmp) / kind
        proj.mkdir()
        write_project(proj, scenes, root_tweens)
        cmd = [sys.executable, str(TOOL), str(proj)] + (["--gate"] if gate else [])
        p = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return measure(p.stdout), p.returncode, p.stdout


def check(label, got, expected):
    ok = True
    for k, want in expected.items():
        have = got.get(k)
        hit = have is not None and (want(have) if callable(want) else have == want)
        if not hit:
            ok = False
        print(f"      {'ok ' if hit else 'BAD'}  {k:<15} = {have}"
              f"{'' if hit else '   expected ' + (getattr(want, '__doc__', None) or str(want))}")
    print(f"    {'PASS' if ok else 'FAIL'}  {label}")
    return ok


def lt50(v):
    """< 50"""
    return v < 50.0


def ge1(v):
    """>= 1"""
    return v >= 1


def main():
    ok = True

    print("  SLIDES fixture (the failure this tool exists to name):")
    got, rc, out = run("slides", slides_scenes())
    ok &= check("slides", got, {"boundaries": 2, "cuts": 2, "transitions": 0,
                                "ground_changes": 2, "violations": 0,
                                "top_sig": 100.0, "pairs": 1, "merged": 0,
                                "camera": 0})
    if rc != 0:
        ok = False
        print(f"    FAIL  slides exited {rc}; advisory runs must exit 0.")

    print("\n  FILM fixture (the fix -- catches a scanner blinded to 'always slides'):")
    got, rc, out = run("film", film_scenes(), FILM_ROOT)
    ok &= check("film", got, {"boundaries": 2, "cuts": 0, "transitions": 2,
                              "violations": 0, "top_sig": lt50, "pairs": 0,
                              "camera": ge1})
    types = re.search(r"    types: (.+)", out)
    print(f"      boundary types: {types.group(1) if types else '(not printed)'}")
    if not (types and "push" in types.group(1) and "blur" in types.group(1)):
        ok = False
        print("    FAIL  film: expected one push and one blur boundary "
              "(prop-based classification is broken).")
    if rc != 0:
        ok = False
        print(f"    FAIL  film exited {rc}; advisory runs must exit 0.")

    print("\n  VIOLATION fixture (the one hard rule):")
    got, rc_plain, _ = run("violation", violation_scenes(), VIOLATION_ROOT)
    _, rc_gate, _ = run("violation", violation_scenes(), VIOLATION_ROOT, gate=True)
    ok &= check("violation", got, {"violations": 1, "transitions": 1, "cuts": 0,
                                   "ground_changes": 1})
    print(f"      exit codes: plain={rc_plain}, --gate={rc_gate}")
    if rc_gate != 2:
        ok = False
        print(f"    FAIL  --gate exited {rc_gate}, expected 2 on a crossfade across "
              "a ground change.")
    if rc_plain != 0:
        ok = False
        print(f"    FAIL  plain run exited {rc_plain}; without --gate this tool is "
              "advisory and must exit 0.")

    print("\n  " + ("All three controls behave as expected." if ok else
                    "CONTROLS FAILED -- continuity-audit.py's counts are not evidence "
                    "right now."))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
