#!/usr/bin/env python3
"""Emit index.html -- the root composition. GENERATED; edit THIS file.

Owns exactly three things: one scene clip per composition FILE, the root
transition tweens between them, and the audio block. Everything inside a
file belongs to build_frames.py.

Timing comes from timing.walk() (measured words), transitions from
transitions.py, iris centres from motion.MOTION, SFX cues from sfx.py.

AUDIO -- three tracks:
  10  ONE narration clip: assets/voice/master.wav at data-start 0, inside the
      single <hf-audio-group id="voiceover"> carrying the channel's canonical
      6-node voice chain (md5 555e4fb8cd83882d982816763cf3a12d, byte-identical
      across seven projects now).
  20  the music bed, carved against the voiceover GROUP (data-fx-carve).
  21  one-shot SFX, own track, never carved.

data-automation: the VERSIONED lane form. A volume lane REPLACES data-volume
on this engine (confirmed on 0.8.22 by reading its bundled cli.js; re-verified
on 0.8.27 -- see DELIVERY.md), so every plateau below is the clip's REAL level.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from timing import walk, master_len, FADE_IN, FADE_OUT
from transitions import plan
from motion import MOTION
from sfx import cues as sfx_cues

FPS = 30
VO_LEVEL = 1.0
BGM_LEVEL = 0.12          # the house value: 8 of this channel's projects use it
BGM_FILE = "assets/bgm/bed.mp3"
SAFE_CENTRE = (960.0, 513.0)   # centre of the safe box: the outgoing push pivots here

FX_CHAIN = {"version": 1, "nodes": [
 {"type":"highpass","id":"n1","label":"Remove Rumble","params":{"frequency":90,"q":0.707,"poles":"2"}},
 {"type":"peaking","id":"n2","label":"Add Weight","params":{"frequency":150,"gain":0.8,"q":1.2}},
 {"type":"compressor","id":"n3","label":"Even Out Loudness","params":{"threshold":-24,"ratio":4,"attack":5,"release":140,"knee":2,"makeup":3,"mix":1}},
 {"type":"peaking","id":"n4","label":"Add Clarity","params":{"frequency":3000,"gain":2.5,"q":1}},
 {"type":"peaking","id":"n5","label":"De-ess (fallback)","params":{"frequency":6500,"gain":-4,"q":3.5}},
 {"type":"limiter","id":"n6","label":"Peak Ceiling","params":{"limit":-9,"attack":0.05,"release":40,"level_out":0}}]}


def j(o):
    return json.dumps(o, separators=(",", ":"))


def lane(points):
    return j({"version": 1, "lanes": [{"target": "volume",
              "points": [{"t": round(t, 3), "v": v} for t, v in points]}]})


def build():
    units, files, total, manifest = walk()
    fake = manifest.get("source") == "fake"
    divs, tweens, seams = [], [], []
    for i, f in enumerate(files):
        divs.append(
            f'    <div id="scene-{f.cid}" class="scene clip" data-composition-id="{f.cid}"\n'
            f'         data-composition-src="compositions/frames/{f.cid}.html"\n'
            f'         data-start="{f.start:.3f}" data-duration="{f.dur:.3f}"\n'
            f'         data-track-index="0"></div>')
        if i == 0:
            continue
        prev = files[i - 1]
        iris_at = None
        if f.kind_in == "iris":
            p = MOTION[prev.units[-1].cid].get("iris_at")
            assert p, f"{prev.cid}: closes with an iris but its last unit declares no iris_at"
            # the outgoing file pushes to 1.06 under the wipe; at the midpoint (~1.03)
            # the actor has drifted from p to c + (p - c) * 1.03
            cx, cy = SAFE_CENTRE
            iris_at = (cx + (p[0] - cx) * 1.03, cy + (p[1] - cy) * 1.03)
        kind, d, sa, jj, gap, hidden, shown, ease = plan(f.units[0].cid, iris_at)
        tweens.append(f'    tl.fromTo("#scene-{f.cid}", {{ clipPath:"{hidden}" }},\n'
                      f'      {{ clipPath:"{shown}", duration:{d:.2f}, ease:"{ease}" }}, '
                      f'{f.start:.3f});   // {kind}: {prev.cid} -> {f.cid}')
        seams.append({"from": prev.cid, "into": f.cid, "kind": kind, "seam": f.start,
                      "d": d, "gap": gap, "iris_at": iris_at,
                      "first_word": f.units[0].first_word_abs})

    L = master_len()
    vo = (f'      <audio id="vo-master" src="assets/voice/master.wav"\n'
          f'             data-start="0.000" data-duration="{L:.3f}"\n'
          f'             data-track-index="10" data-volume="{VO_LEVEL}"\n'
          f'             data-audio-group="voiceover"\n'
          f"             data-automation='{lane([(0, 0), (FADE_IN, VO_LEVEL), (L - FADE_OUT, VO_LEVEL), (L, 0)])}'></audio>")

    bgm = ""
    if (ROOT / BGM_FILE).exists():
        bgm = (f'    <!-- Music bed, carved against the voiceover GROUP. -->\n'
               f'    <audio id="bgm" src="{BGM_FILE}" data-start="0" data-duration="{total:.3f}"\n'
               f'           data-track-index="20" data-volume="{BGM_LEVEL}"\n'
               f"           data-automation='{lane([(0, 0), (0.25, BGM_LEVEL), (total - 1.5, BGM_LEVEL), (total, 0)])}'\n"
               f"           data-fx-carve='{j({'sources': ['voiceover'], 'strength': 0.25})}'></audio>")

    sfx = []
    for k, (at, fname, dur, vol, note) in enumerate(sfx_cues(units)):
        sfx.append(f'    <audio id="sfx-{k}" src="assets/sfx/{fname}" data-start="{at:.3f}" '
                   f'data-duration="{dur:.3f}" data-track-index="21" data-volume="{vol}"></audio>'
                   f'  <!-- {note} -->')

    html = f"""<!DOCTYPE html>
<html lang="en" data-resolution="landscape">
<head>
  <meta charset="UTF-8">
  <title>You Bought Collagen. Where Did It Actually Go?</title>
</head>
<body>
  <!-- ==================================================================
       GENERATED BY scripts/build_index.py -- DO NOT EDIT THIS FILE.
       Timing: timing.walk() over assets/voice/master.words.json.
       Transitions: scripts/transitions.py. Audio: one narrator clip.
       ================================================================== -->
  {"<!-- VO MANIFEST: FAKE -- synthetic timing, silent master. NOT FOR DELIVERY. -->" if fake else ""}
  <div id="root" data-composition-id="main" data-start="0"
       data-duration="{total:.3f}" data-width="1920" data-height="1080"
       data-fps="{FPS}">

{chr(10).join(divs)}

    <hf-audio-group id="voiceover" data-label="Voiceover" data-volume="1"
                    data-fx-chain='{j(FX_CHAIN)}'>
{vo}
    </hf-audio-group>

{bgm}

    <!-- one-shot SFX, own track, no carve -->
{chr(10).join(sfx)}
  </div>

  <style>
    *,*::before,*::after {{ box-sizing:border-box; }}
    html,body {{ margin:0; padding:0; background:#F7F5F0; }}
    .scene.clip {{ position:absolute; inset:0; }}
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {{}};
    // No `defaults` on the root. Its only job is file handoff.
    var tl = gsap.timeline({{ paused: true }});
{chr(10).join(tweens)}
    tl.to({{}}, {{ duration: {total:.3f} }}, 0);   // anchor
    window.__timelines["main"] = tl;
  </script>
</body>
</html>
"""
    (ROOT / "index.html").write_text(html)
    (ROOT / "index.seams.json").write_text(json.dumps(seams, indent=1) + "\n")
    return files, total, len(sfx), fake


def main():
    files, total, nsfx, fake = build()
    print(f"index.html: {len(files)} file clips, {len(files) - 1} transitions, 1 VO clip, "
          f"{nsfx} SFX cues, total {total:.3f}s{'  [VO MANIFEST: FAKE]' if fake else ''}")
    for f in files:
        print(f"  {f.cid:14s} start={f.start:8.3f} dur={f.dur:7.3f} in={f.kind_in or '-'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
