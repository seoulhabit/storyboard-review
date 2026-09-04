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

Every scene's start/duration and every transition's timing come from
timing.walk() + transitions.plan() -- see those two files. This generator no
longer computes a seam or a wipe duration itself; it only emits markup for
numbers it is handed.

data-automation shape: the VERSIONED lane form. The flat {"volume":[[t,v],...]}
form is rejected at RENDER time ("Unsupported automation version") while `check`
passes it, so a lint-clean project can still fail to render.

AND: a volume lane REPLACES data-volume, it does not scale it. So each plateau
below is written as the clip's REAL intended level, never a normalised 1.0.

Music bed and SFX cues are wired by a later pass once `total` is final (see
the plan's "Order of work" step 4) -- this generator emits the VO-only root
so the timing/transition mechanism can be validated on its own first.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLUG = "ectoin-survival-molecule"
FADE = 0.08         # 80ms edge fade on every clip -- avoids a click at the cut
VO_LEVEL = 1.0       # VO is the reference level; plateau IS this, not a scaled 1.0

sys.path.insert(0, str(Path(__file__).resolve().parent))
from timing import walk
from transitions import plan


def automation(clip_len, level):
    """Versioned volume lane with an 80ms fade at each edge."""
    return json.dumps({"version": 1, "lanes": [{"target": "volume", "points": [
        {"t": 0.0, "v": 0.0},
        {"t": FADE, "v": level},
        {"t": round(max(FADE, clip_len - FADE), 3), "v": level},
        {"t": round(clip_len, 3), "v": 0.0},
    ]}]}, separators=(",", ":"))


def main():
    scenes, total = walk()
    scene_divs, audio_divs, xitions, seams = [], [], [], []

    for i, s in enumerate(scenes):
        scene_divs.append(
            f'    <div id="scene-{s.cid}" class="scene clip" data-composition-id="{s.cid}"\n'
            f'         data-composition-src="compositions/frames/{s.cid}.html"\n'
            f'         data-start="{s.start:.3f}" data-duration="{s.dur:.3f}" '
            f'data-track-index="0"></div>')
        # The transition grammar OVERLAPS adjacent VO clips by design: a
        # boundary's `j` is the wipe-tail seconds during which the NEXT
        # scene's first word already sounds, so clip N+1 starts before clip
        # N's own TAIL padding finishes playing. Both sides of that overlap
        # are silence (padding vs. lead-in), so it is inaudible, but two
        # <audio> elements with overlapping windows on the SAME track index
        # is flagged by `check` as duplicate_audio_track (layered playback is
        # undefined). Alternating even/odd scenes across two VO tracks keeps
        # every ADJACENT pair on different tracks without changing any timing.
        vo_track = 10 if i % 2 == 0 else 11
        audio_divs.append(
            f'    <audio id="vo-{s.cid}" src="assets/voice/{s.n:02d}.wav"\n'
            f'           data-start="{s.vo_start:.3f}" data-duration="{s.vo_len:.3f}"\n'
            f'           data-track-index="{vo_track}" data-volume="{VO_LEVEL}" '
            f'data-audio-group="voiceover"\n'
            f"           data-automation='{automation(s.vo_len, VO_LEVEL)}'></audio>")

        if i + 1 < len(scenes):
            nxt = scenes[i + 1]
            kind, d, seam_after, j, gap, hidden, shown, ease = plan(s.cid, nxt.cid)
            xitions.append(
                f'    // {kind} boundary: {s.cid} -> {nxt.cid}, {d:.2f}s, gap {gap:.2f}s\n'
                f'    tl.fromTo("#scene-{nxt.cid}", {{ clipPath: "{hidden}" }}, '
                f'{{ clipPath: "{shown}", duration: {d:.2f}, '
                f'ease: "{ease}" }}, {nxt.start:.3f});')
            seams.append({
                "from": s.cid, "to": nxt.cid, "kind": kind, "seam": nxt.start,
                "d": d, "seam_after": seam_after, "j": j, "gap": gap,
                "last_word_abs": round(s.vo_start + s.words[-1]["end"], 3),
                "first_word_abs": round(nxt.vo_start + nxt.words[0]["start"], 3),
            })

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
  <div id="root" data-composition-id="main" data-start="0" data-duration="{total:.3f}"
       data-width="1920" data-height="1080" data-fps="30">

    <!-- Scenes 01-29 minus the 09/10 merge (28 total), flat root->frame. -->
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
    // The root timeline's only job is scene handoff -- five clip-path wipe
    // kinds (scripts/transitions.py), never a translate, never an opacity
    // crossfade. See that file and this project's CLAUDE.md for why.
    window.__timelines = window.__timelines || {{}};
    var tl = gsap.timeline({{ paused: true }});
{chr(10).join(xitions)}
    tl.to({{}}, {{ duration: {total:.3f} }}, 0);   // anchor: tl.duration() === root duration
    window.__timelines["main"] = tl;
  </script>
</body>
</html>
'''
    (ROOT / "index.html").write_text(html)
    (ROOT / "index.seams.json").write_text(json.dumps(seams, indent=2) + "\n")

    by_kind = {}
    for s in seams:
        by_kind[s["kind"]] = by_kind.get(s["kind"], 0) + 1
    print(f"index.html: {len(scenes)} scenes, {len(scenes)} VO clips, "
          f"total {total:.3f}s ({int(total // 60)}:{total % 60:05.2f})")
    print(f"  transitions: {len(seams)} ({', '.join(f'{k} {n}' for k, n in by_kind.items())})")
    print(f"  index.seams.json written ({len(seams)} boundaries)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
