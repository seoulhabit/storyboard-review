#!/usr/bin/env python3
"""Emit index.html. GENERATED -- edit THIS file, never the output.

Owns three things and nothing else:
  1. the scene divs, with the transition overlap folded into data-duration
  2. the root transition tweens (clip-path wipes on the scene WRAPPERS)
  3. the audio block: the voiceover group, 41 VO clips, and the BGM bed

Everything inside a scene belongs to build_frames.py.

TRANSITIONS. Clip-path wipes, nothing translates, opacity never touched. A
translating push was built on the ectoin project and REJECTED: it failed the
hard safe-area gate on 99 frames because a push drags real text through the
reserved zones on its way in and out, while a wipe only reveals content already
at its resting position. Both render fine and both pass `check`; only the gate
on a real render tells them apart.

  chapter opener   wipe UP    inset(100% 0 0 0) -> inset(0)   0.60s
  within chapter   wipe LEFT  inset(0 0 0 100%) -> inset(0)   0.45s
  one HARD CUT     03 -> 04, deliberate: leaving the body for the abstract
                   evidence space is a register change that earns a cut.

The outgoing clip's data-duration is extended by the overlap so it is still on
screen to be wiped away from; an ended clip holds its final frame. Scene
data-start values are NOT shifted -- the overlap IS the transition window.

Expect `check` to report content_overlap / text_occluded at each wipe. That is a
known false positive: the layout pass tests bounding boxes and does not model
clip-path, so a clipped incoming wrapper still presents a full-canvas opaque
box. Its SEVERITY moves with --samples, not with the composition. Confirm on an
extracted frame; do not restructure to satisfy it.
"""
import json, subprocess
from pathlib import Path
from build_frames import scene_timing
from vo_lines import by_scene

ROOT = Path(__file__).resolve().parent.parent
FPS = 30

# scene id -> (source file, transition INTO this scene)
#   "up"   chapter opener    "left"  within chapter    None  hard cut / first
SCENES = [
    ("00-cold-open", None),
    # within chapter 1: the cold open and the building are the same chapter, so
    # this boundary gets the within-chapter LEFT wipe, not the chapter accent.
    ("01-building",  "left"),
    ("02-door",      "up"),
    ("03-digestion", "up"),
    ("04-evidence",  None),   # deliberate hard cut -- see module docstring
    ("05-verdict",   "up"),
]
WIPE = {"up": (0.60, "inset(100% 0% 0% 0%)"), "left": (0.45, "inset(0% 0% 0% 100%)")}

VO_LEAD, FADE, VO_LEVEL = 0.10, 0.08, 1.0
BGM_LEVEL = 0.12          # the house value: 8 of this channel's projects use it
BGM_FILE = "assets/bgm/bed.mp3"

# The channel's canonical voice chain, byte-identical across six projects
# (md5 555e4fb8cd83882d982816763cf3a12d). Reused verbatim on purpose -- it is
# what makes the narration sound like the same show. Both speakers share it.
FX_CHAIN = {"version": 1, "nodes": [
 {"type":"highpass","id":"n1","label":"Remove Rumble","params":{"frequency":90,"q":0.707,"poles":"2"}},
 {"type":"peaking","id":"n2","label":"Add Weight","params":{"frequency":150,"gain":0.8,"q":1.2}},
 {"type":"compressor","id":"n3","label":"Even Out Loudness","params":{"threshold":-24,"ratio":4,"attack":5,"release":140,"knee":2,"makeup":3,"mix":1}},
 {"type":"peaking","id":"n4","label":"Add Clarity","params":{"frequency":3000,"gain":2.5,"q":1}},
 {"type":"peaking","id":"n5","label":"De-ess (fallback)","params":{"frequency":6500,"gain":-4,"q":3.5}},
 {"type":"limiter","id":"n6","label":"Peak Ceiling","params":{"limit":-9,"attack":0.05,"release":40,"level_out":0}}]}


def j(o):
    return json.dumps(o, separators=(",", ":"))


def automation(dur, level):
    """A volume lane REPLACES data-volume on this engine -- it does not scale it.

    Confirmed by reading hyperframes@0.8.22's own bundled cli.js: any clip
    carrying data-automation is filtered out of the data-volume path entirely.
    So the plateau must be the clip's REAL intended level. Writing a normalised
    1.0 plateau over a data-volume="0.12" bed is silent and renders it ~18dB
    hot -- no lint error, no render warning, nothing.
    """
    if dur <= 2 * FADE:
        return j({"version": 1, "lanes": [{"target": "volume", "points": [
            {"t": 0.0, "v": 0.0}, {"t": round(dur / 2, 3), "v": level},
            {"t": round(dur, 3), "v": 0.0}]}]})
    return j({"version": 1, "lanes": [{"target": "volume", "points": [
        {"t": 0.0, "v": 0.0}, {"t": FADE, "v": level},
        {"t": round(dur - FADE, 3), "v": level}, {"t": round(dur, 3), "v": 0.0}]}]})


def build():
    t = scene_timing()
    grouped = by_scene()

    # scene starts, then the overlap folded into each OUTGOING duration
    starts, acc = {}, 0.0
    for cid, _ in SCENES:
        starts[cid] = round(acc, 3)
        acc += t[cid.split("-")[0]]["dur"]
    total = round(acc, 3)

    holds = {cid: 0.0 for cid, _ in SCENES}
    for i, (cid, tr) in enumerate(SCENES):
        if tr and i:
            holds[SCENES[i - 1][0]] = WIPE[tr][0]

    divs, tweens = [], []
    for cid, tr in SCENES:
        k = cid.split("-")[0]
        dur = round(t[k]["dur"] + holds[cid], 3)
        divs.append(
            f'    <div id="scene-{cid}" class="scene clip" data-composition-id="{cid}"\n'
            f'         data-composition-src="compositions/frames/{cid}.html"\n'
            f'         data-start="{starts[cid]:.3f}" data-duration="{dur:.3f}"\n'
            f'         data-track-index="0"></div>')
        if tr:
            d, frm = WIPE[tr]
            tweens.append(
                f'    tl.fromTo("#scene-{cid}", {{ clipPath:"{frm}" }},\n'
                f'      {{ clipPath:"inset(0% 0% 0% 0%)", duration:{d:.2f}, '
                f'ease:"power3.inOut" }}, {starts[cid]:.3f});')
        else:
            tweens.append(f'    // {cid}: hard cut, deliberate.')

    # ---- audio -----------------------------------------------------------
    clips = []
    for cid, _ in SCENES:
        k = cid.split("-")[0]
        for ln, tim in zip(grouped[k], t[k]["lines"]):
            at = round(starts[cid] + tim["start"] - VO_LEAD, 3)
            d = tim["dur"]
            clips.append(
                f'      <audio id="vo-{ln["idx"]:02d}" src="{ln["wav"]}"\n'
                f'             data-start="{at:.3f}" data-duration="{d:.3f}"\n'
                f'             data-track-index="10" data-volume="{VO_LEVEL}"\n'
                f'             data-audio-group="voiceover"\n'
                f"             data-automation='{automation(d, VO_LEVEL)}'></audio>")

    bgm = ""
    if (ROOT / BGM_FILE).exists():
        bgm = (
            f'    <audio id="bgm" src="{BGM_FILE}" data-start="0"\n'
            f'           data-duration="{total:.3f}" data-track-index="1"\n'
            f'           data-volume="{BGM_LEVEL}"\n'
            f'           data-fx-carve=\'{j({"sources":["voiceover"],"strength":0.25})}\'\n'
            f"           data-automation='{automation(total, BGM_LEVEL)}'></audio>")
    else:
        bgm = ("    <!-- No BGM bed present. Drop a file at assets/bgm/bed.mp3 and\n"
               "         re-run `npm run build` to wire it with the house 0.12 level\n"
               "         and a 0.25 voiceover carve. -->")

    html = f"""<!DOCTYPE html>
<html lang="en" data-resolution="landscape">
<head>
  <meta charset="UTF-8">
  <title>You Bought Collagen. Where Did It Actually Go?</title>
</head>
<body>
  <!-- ==================================================================
       GENERATED BY scripts/build_index.py -- DO NOT EDIT THIS FILE.
       Any change here is discarded by the next `npm run build`.
       Scene content lives in scripts/build_frames.py; the dialogue and
       its timing live in scripts/vo_lines.py.
       ================================================================== -->
  <div id="root" data-composition-id="main" data-start="0"
       data-duration="{total:.3f}" data-width="1920" data-height="1080"
       data-fps="{FPS}">

{chr(10).join(divs)}

    <hf-audio-group id="voiceover" data-label="Voiceover" data-volume="1"
                    data-fx-chain='{j(FX_CHAIN)}'>
{chr(10).join(clips)}
    </hf-audio-group>

{bgm}
  </div>

  <style>
    *,*::before,*::after {{ box-sizing:border-box; }}
    html,body {{ margin:0; padding:0; background:#F7F5F0; }}
    .scene.clip {{ position:absolute; inset:0; }}
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {{}};
    // No `defaults` on the root either. The root's only job is scene handoff.
    var tl = gsap.timeline({{ paused: true }});
{chr(10).join(tweens)}
    tl.to({{}}, {{ duration: {total:.3f} }}, 0);   // anchor
    window.__timelines["main"] = tl;
  </script>
</body>
</html>
"""
    (ROOT / "index.html").write_text(html)
    return starts, t, total


def main():
    starts, t, total = build()
    print("index.html  (GENERATED -- edit build_index.py)")
    for cid, tr in SCENES:
        k = cid.split("-")[0]
        print(f"  {starts[cid]:8.3f}  {cid:14s} {t[k]['dur']:7.3f}s  "
              f"{'<- ' + tr + ' wipe' if tr else '<- hard cut'}")
    m, s = divmod(total, 60)
    print(f"  total {total:.3f}s  ({int(m)}:{s:05.2f})")


if __name__ == "__main__":
    main()
