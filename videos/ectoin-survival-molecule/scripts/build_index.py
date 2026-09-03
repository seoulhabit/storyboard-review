#!/usr/bin/env python3
"""Generate index.html -- the root timeline: flat scene clips + ALL audio.

Two engine constraints force this shape, both confirmed in this repo:

  1. SINGLE-LEVEL NESTING. videos/pilling-vs-peeling/index.html records an
     isolated test where root->body->frame double-nesting silently broke a
     scene's inner layout, pushing content off-canvas -- invisible in the
     rendered MP4, not a lint finding. So no act/chapter grouping: root->frame.
  2. ALL AUDIO ON THE ROOT. Nested <audio data-start> is unverified against the
     pinned CLI, so every cue is wired here even though it would read better
     alongside its scene.

Consequently the root is GENERATED, never hand-maintained -- at full length this
file carries ~40 scenes plus ~40 VO clips plus SFX.

data-automation shape: the VERSIONED lane form. The flat {"volume":[[t,v],...]}
form is rejected at RENDER time ("Unsupported automation version") while `check`
passes it, so a lint-clean project can still fail to render.

AND: a volume lane REPLACES data-volume, it does not scale it. So each plateau
below is written as the clip's REAL intended level, never a normalised 1.0.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLUG = "ectoin-survival-molecule"
TAIL_PAD = 0.15   # see build_frames.py -- pad_vo.py adds 250ms inside each take
VO_LEAD = 0.10      # scene cuts this much before its line starts
FADE = 0.08         # 80ms edge fade on every clip -- avoids a click at the cut
VO_LEVEL = 1.0      # VO is the reference level; plateau IS this, not a scaled 1.0

import sys as _sys

_sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_storyboard import CHAPTERS
from frames_a27 import SCENES_A27

SCENES = [
    ("01-hook",        1), ("02-osmosis",   2), ("03-now",       3),
    ("04-extremolyte", 4), ("05-halomonas", 5), ("06-mechanism", 6),
    ("07-question",    7),
] + [(cid, vo) for cid, _spec, vo in SCENES_A27]


# ---- transition system ---------------------------------------------------
# Two types, both CLIP-PATH WIPES. Nothing translates: the incoming scene sits
# at its own resting position and is progressively revealed, while the outgoing
# holds its final frame underneath (later scenes paint above earlier ones, so
# no z-index juggling is needed). Opacity is never touched either, so no frame
# ever composites two grounds -- which is what makes this safe across the 17
# ink<->paper ground changes here, where a plain crossfade would give the muddy
# near-blank midpoint.
#   primary  wipe from the RIGHT edge leftward 0.45s -- within a chapter
#   accent   wipe from the BOTTOM edge upward  0.60s -- into a chapter opener,
#                               so the strongest treatment lands on the re-hook
#
# WHY A WIPE AND NOT A PUSH. A translating push was built first and rendered
# correctly, but it FAILED the hard safe-area gate on 99 sampled frames: sliding
# a full-canvas scene drags its content through the reserved zones on the way in
# and out (measured up to 6.2% edge density inside the top zone, i.e. real text,
# not just a flat ground). The pre-transition render passed that gate on all
# 1361 sampled frames, so the push was a real regression, not a gate artifact --
# checked by measuring the frames, because this gate's border-ring background
# estimator does also mis-read a legitimately two-ground transition frame.
# A wipe moves no content, so every scene stays exactly as compliant as it is
# at rest. Safe here specifically because this project is 100% browser-drawn:
# there is not one <img> in any scene, so the drawElement capture bug that hits
# an animated clip over a RASTER cannot apply.
#
# The OUTGOING clip's emitted data-duration is extended by the transition
# duration so it holds its final frame while the wipe runs. Scene data-start,
# every scene's internal beat timing, and every VO cue are untouched -- which is
# the whole reason the overlap is built this way round on a VO-locked cut.
T_WITHIN, T_CHAPTER = 0.45, 0.60


def transition_into(cid):
    """(duration, hidden-inset, shown-inset, human label) entering `cid`."""
    if cid in CHAPTERS:
        return T_CHAPTER, "inset(100% 0% 0% 0%)", "inset(0% 0% 0% 0%)", "UP"
    return T_WITHIN, "inset(0% 0% 0% 100%)", "inset(0% 0% 0% 0%)", "LEFT"


def dur(p):
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
        capture_output=True, text=True).stdout.strip())


def automation(clip_len, level):
    """Versioned volume lane with an 80ms fade at each edge."""
    return json.dumps({"version": 1, "lanes": [{"target": "volume", "points": [
        {"t": 0.0, "v": 0.0},
        {"t": FADE, "v": level},
        {"t": round(clip_len - FADE, 3), "v": level},
        {"t": round(clip_len, 3), "v": 0.0},
    ]}]}, separators=(",", ":"))


def main():
    t = 0.0
    scene_divs, audio_divs, xitions = [], [], []
    for i, (cid, n) in enumerate(SCENES):
        vo = ROOT / "assets" / "voice" / f"{n:02d}.wav"
        vlen = dur(vo)
        slen = round(vlen + TAIL_PAD, 3)

        # this scene is the OUTGOING side of the boundary into the next one;
        # hold its final frame for that transition's duration
        hold = 0.0
        if i + 1 < len(SCENES):
            nxt = SCENES[i + 1][0]
            d, hidden, shown, label = transition_into(nxt)
            hold = d
            T = round(t + slen, 3)          # the next scene's start = the seam
            kind = "chapter" if nxt in CHAPTERS else "scene"
            xitions.append(
                f'    // {kind} boundary: {cid} -> {nxt}, wipe {label} {d:.2f}s\n'
                f'    tl.fromTo("#scene-{nxt}", {{ clipPath: "{hidden}" }}, '
                f'{{ clipPath: "{shown}", duration: {d:.2f}, '
                f'ease: "power3.inOut" }}, {T:.3f});')

        scene_divs.append(
            f'    <div id="scene-{cid}" class="scene clip" data-composition-id="{cid}"\n'
            f'         data-composition-src="compositions/frames/{cid}.html"\n'
            f'         data-start="{t:.3f}" data-duration="{slen + hold:.3f}" data-track-index="0"></div>')
        audio_divs.append(
            f'    <audio id="vo-{n:02d}" src="assets/voice/{n:02d}.wav"\n'
            f'           data-start="{t + VO_LEAD:.3f}" data-duration="{vlen:.3f}"\n'
            f'           data-track-index="10" data-volume="{VO_LEVEL}" data-audio-group="voiceover"\n'
            f"           data-automation='{automation(vlen, VO_LEVEL)}'></audio>")
        t = round(t + slen, 3)

    # The channel's standing VO chain, reused verbatim across projects -- it is what
    # makes the narration sound like the same show. Deviating needs a stated reason.
    fx = json.dumps({"version": 1, "nodes": [
        {"type": "highpass",   "id": "n1", "label": "Remove Rumble",     "params": {"frequency": 90, "q": 0.707, "poles": "2"}},
        {"type": "peaking",    "id": "n2", "label": "Add Weight",        "params": {"frequency": 150, "gain": 0.8, "q": 1.2}},
        {"type": "compressor", "id": "n3", "label": "Even Out Loudness", "params": {"threshold": -24, "ratio": 4, "attack": 5, "release": 140, "knee": 2, "makeup": 3, "mix": 1}},
        {"type": "peaking",    "id": "n4", "label": "Add Clarity",       "params": {"frequency": 3000, "gain": 2.5, "q": 1}},
        {"type": "peaking",    "id": "n5", "label": "De-ess (fallback)", "params": {"frequency": 6500, "gain": -4, "q": 3.5}},
        {"type": "limiter",    "id": "n6", "label": "Peak Ceiling",      "params": {"limit": -9, "attack": 0.05, "release": 40, "level_out": 0}},
    ]}, separators=(",", ":"))

    html = f'''<!DOCTYPE html>
<html lang="en" data-resolution="landscape">
<head>
  <meta charset="UTF-8">
  <title>Ectoin: the survival molecule</title>
</head>
<body>
  <div id="root" data-composition-id="main" data-start="0" data-duration="{t:.3f}"
       data-width="1920" data-height="1080" data-fps="30">

    <!-- Scenes 01-29, flat root->frame (one level deep -- double nesting is
         confirmed to break layout silently). Acts 2-7 use panel-scale beats. -->
{chr(10).join(scene_divs)}

    <!-- Audio. All on the root; see this file's generator for why. -->
    <hf-audio-group id="voiceover" data-label="Voiceover" data-volume="1"
                    data-fx-chain='{fx}'>
    </hf-audio-group>
{chr(10).join(audio_divs)}
  </div>

  <style>
    *,*::before,*::after {{ box-sizing:border-box; }}
    html,body {{ margin:0; padding:0; background:#F7F5F0; }}
    .scene.clip {{ position:absolute; inset:0; }}
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    // The root timeline's only job is scene handoff. A plain crossfade is still
    // banned here -- grounds alternate ink/paper and blending two of them gives a
    // muddy near-blank midpoint -- but a hard cut is no longer the only option:
    // a clip-path wipe reveals the incoming scene at its own resting position
    // without translating anything and without touching opacity, so no frame
    // composites two grounds AND no content is dragged through a reserved
    // safe-area zone. See build_index.py for why a push was rejected.
    window.__timelines = window.__timelines || {{}};
    var tl = gsap.timeline({{ paused: true }});
{chr(10).join(xitions)}
    tl.to({{}}, {{ duration: {t:.3f} }}, 0);   // anchor: tl.duration() === root duration
    window.__timelines["main"] = tl;
  </script>
</body>
</html>
'''
    (ROOT / "index.html").write_text(html)
    nch = sum(1 for cid, _ in SCENES[1:] if cid in CHAPTERS)
    print(f"index.html: {len(SCENES)} scenes, {len(SCENES)} VO clips, total {t:.3f}s")
    print(f"  transitions: {len(xitions)} ({nch} chapter wipe-UP, "
          f"{len(xitions) - nch} within-chapter wipe-LEFT)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
