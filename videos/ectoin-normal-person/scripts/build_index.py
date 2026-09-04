#!/usr/bin/env python3
"""Generate index.html -- root timeline: flat scene clips + ALL audio.

Inherits two hard engine constraints from the predecessor, both confirmed:

  1. SINGLE-LEVEL NESTING, root->frame. Double nesting silently breaks a
     scene's inner layout -- invisible in the MP4, not a lint finding.
  2. ALL AUDIO ON THE ROOT. Nested <audio data-start> is unverified against
     the pinned CLI.

WHAT IS NEW HERE: this is a TWO-VOICE piece, so audio is wired per TURN, not
per scene. A scene holds 2-5 turns; each turn is its own clip in its own
speaker group. Scene duration is therefore derived from the SUM of its turns
plus the inter-turn gaps, not from a single take's length.

data-automation is the VERSIONED lane form. The flat {"volume":[[t,v],...]}
form is rejected at RENDER time while `check` passes it, so a lint-clean
project can still fail to render. AND a volume lane REPLACES data-volume
rather than scaling it, so every plateau below is the clip's REAL level.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLUG = "ectoin-normal-person"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vo_lines import SCENES, SPEAKER
from build_storyboard import CHAPTERS

# Timing comes from the SHARED walk, never a local copy. An earlier version of
# this file carried its own scene_timing() that predated scripts/timing.py and
# did not know about PHASE_GAP; it reported 358.229s against the frame
# generator's 359.008s. A 0.78s disagreement between the root's scene starts
# and each frame's internal phase offsets is an audio/visual desync inside
# every merged unit, and nothing in the render pipeline would have said so.
from timing import walk
FADE     = 0.08   # 80ms edge fade on every clip -- avoids a click at the cut
VO_LEVEL = 1.0    # VO is the reference level; the plateau IS this

GROUP = {"S": "vo-soulhabit", "J": "vo-jay"}

# ---- music bed + local SFX (non-negotiable #12) ----------------------------
# The bed is ONE frozen, finite file (assets/music/bed.mp3, 241.262s, built
# once via `ffmpeg -stream_loop` from a loop-prepared source and committed --
# not a runtime loop, per the render-safety ban on infinite loops) carved
# against BOTH voice groups (see hyperframes-audio skill: "sources" is a
# list, summed onto the bed's own clock -- a bed under a two-voice dialogue
# ducks under either speaker, dynamically, never a fixed depth). Every SFX
# cue is a short local one-shot, sourced from this channel's own existing
# kit (catalog convention: reuse before generating) rather than a fresh
# license. Timestamps below are read directly off scripts/timing.py's walk,
# not estimated -- re-derive them (see the __main__ block at the bottom of
# this file) if the script changes again.
BED = ("assets/music/bed.mp3", 241.262, 0.30)

# (at_seconds, file, duration, volume, note)
SFX_CUES = [
    (4.25,   "cream-swoosh-short.mp3",                 0.350, 0.40, "t072: the bottle turns"),
    (6.62,   "chime-trimmed.mp3",                       1.100, 0.38, "t076: the verdict lands"),
    (44.40,  "whoosh-soft-split-reveal.mp3",             1.056, 0.40, "CH1->CH2 chapter wipe"),
    (55.86,  "ui-toggle-trimmed.mp3",                    0.350, 0.42, "04-protein: Jargon Alarm fires"),
    (79.93,  "whoosh-soft-split-reveal.mp3",             1.056, 0.40, "CH2->CH3 chapter wipe"),
    (110.82, "whoosh-soft-split-reveal.mp3",             1.056, 0.40, "CH3->CH4 chapter wipe"),
    (141.51, "glass-clink.mp3",                          0.312, 0.38, "09-miracle: Yes"),
    (144.38, "sharp-text-stamp-impact-hit.trimmed.mp3",  1.100, 0.42, "09-miracle: No"),
    (146.70, "sharp-text-stamp-impact-hit.trimmed.mp3",  1.100, 0.40, "10-notprove: the claims struck"),
    (154.13, "citation-tick-trimmed.mp3",                0.500, 0.36, "11-twelve: the count lands"),
    (163.23, "whoosh-soft-split-reveal.mp3",             1.056, 0.40, "CH4->CH5 chapter wipe"),
    (185.05, "click-soft-chip-pair-lands.mp3",           0.264, 0.36, "12-bottle: Jargon Alarm retires"),
    (202.74, "whoosh-soft-split-reveal.mp3",             1.056, 0.40, "CH5->CH6 chapter wipe"),
    (237.06, "chime.mp3",                                2.500, 0.34, "18-endscreen: the close"),
]

# ---- transition system (harvested; see the predecessor's build_index.py) ----
# Two types, both CLIP-PATH WIPES. Nothing translates and opacity is never
# touched, so no frame composites two grounds -- which is what makes this safe
# across every ink<->paper change here, where a plain crossfade gives a muddy
# near-blank midpoint. A translating push was built there first and FAILED the
# hard safe-area gate on 99 frames; a wipe moves no content, so every scene
# stays exactly as compliant at the seam as it is at rest.
#   primary  wipe from the RIGHT edge leftward 0.45s -- within a chapter
#   accent   wipe from the BOTTOM edge upward  0.60s -- into a chapter opener
T_WITHIN, T_CHAPTER = 0.45, 0.60


def transition_into(cid):
    if cid in CHAPTERS:
        return T_CHAPTER, "inset(100% 0% 0% 0%)", "inset(0% 0% 0% 0%)", "UP"
    return T_WITHIN, "inset(0% 0% 0% 100%)", "inset(0% 0% 0% 0%)", "LEFT"


def automation(clip_len, level):
    return json.dumps({"version": 1, "lanes": [{"target": "volume", "points": [
        {"t": 0.0, "v": 0.0},
        {"t": FADE, "v": level},
        {"t": round(clip_len - FADE, 3), "v": level},
        {"t": round(clip_len, 3), "v": 0.0},
    ]}]}, separators=(",", ":"))


def fx_chain(kind):
    """The channel's standing VO chain. SOULHABIT takes it VERBATIM -- it is
    what makes the narration sound like the same show across projects.

    JAY runs the same topology with two deltas, and only two, so the pair reads
    as one room rather than two shows: less low-mid weight (a brighter voice
    does not need the 150Hz lift and muddies with it) and a deeper de-ess (a
    brighter voice sibilates harder through the same limiter). Everything else
    -- highpass, compressor, clarity, ceiling -- is identical by intent.
    """
    weight = 0.8 if kind == "S" else 0.3
    deess = -4 if kind == "S" else -6
    return json.dumps({"version": 1, "nodes": [
        {"type": "highpass",   "id": "n1", "label": "Remove Rumble",     "params": {"frequency": 90, "q": 0.707, "poles": "2"}},
        {"type": "peaking",    "id": "n2", "label": "Add Weight",        "params": {"frequency": 150, "gain": weight, "q": 1.2}},
        {"type": "compressor", "id": "n3", "label": "Even Out Loudness", "params": {"threshold": -24, "ratio": 4, "attack": 5, "release": 140, "knee": 2, "makeup": 3, "mix": 1}},
        {"type": "peaking",    "id": "n4", "label": "Add Clarity",       "params": {"frequency": 3000, "gain": 2.5, "q": 1}},
        {"type": "peaking",    "id": "n5", "label": "De-ess (fallback)", "params": {"frequency": 6500, "gain": deess, "q": 3.5}},
        {"type": "limiter",    "id": "n6", "label": "Peak Ceiling",      "params": {"limit": -9, "attack": 0.05, "release": 40, "level_out": 0}},
    ]}, separators=(",", ":"))



def main():
    walked, total = walk()
    timing = [(cid, st, own, turns) for cid, st, own, _ph, turns in walked]
    scene_divs, audio_divs, xitions = [], [], []

    for i, (cid, start, own, placed) in enumerate(timing):
        hold = 0.0
        if i + 1 < len(timing):
            nxt = timing[i + 1][0]
            d, hidden, shown, label = transition_into(nxt)
            hold = d
            T = round(start + own, 3)   # the next scene's start IS the seam
            kind = "chapter" if nxt in CHAPTERS else "scene"
            xitions.append(
                f'    // {kind} boundary: {cid} -> {nxt}, wipe {label} {d:.2f}s\n'
                f'    tl.fromTo("#scene-{nxt}", {{ clipPath: "{hidden}" }}, '
                f'{{ clipPath: "{shown}", duration: {d:.2f}, '
                f'ease: "power3.inOut" }}, {T:.3f});')

        scene_divs.append(
            f'    <div id="scene-{cid}" class="scene clip" data-composition-id="{cid}"\n'
            f'         data-composition-src="compositions/frames/{cid}.html"\n'
            f'         data-start="{start:.3f}" data-duration="{own + hold:.3f}" '
            f'data-track-index="0"></div>')

        for tid, astart, alen in placed:
            spk = SPEAKER[tid]
            audio_divs.append(
                f'    <audio id="a-{tid}" src="assets/voice/{tid}.wav"\n'
                f'           data-start="{astart:.3f}" data-duration="{alen:.3f}"\n'
                f'           data-track-index="{10 if spk == "S" else 11}" '
                f'data-volume="{VO_LEVEL}" data-audio-group="{GROUP[spk]}"\n'
                f"           data-automation='{automation(alen, VO_LEVEL)}'></audio>")

    bed_src, bed_dur, bed_vol = BED
    sfx_divs = [
        f'    <audio id="sfx-{i}" src="assets/sfx/{fname}"\n'
        f'           data-start="{at:.3f}" data-duration="{dur:.3f}"\n'
        f'           data-track-index="21" data-volume="{vol}"></audio>'
        f'  <!-- {note} -->'
        for i, (at, fname, dur, vol, note) in enumerate(SFX_CUES)
    ]

    html = f'''<!DOCTYPE html>
<html lang="en" data-resolution="landscape">
<head>
  <meta charset="UTF-8">
  <title>Ectoin, explained twice</title>
</head>
<body>
  <div id="root" data-composition-id="main" data-start="0" data-duration="{total:.3f}"
       data-width="1920" data-height="1080" data-fps="30">

    <!-- {len(timing)} scenes, flat root->frame (one level -- double nesting is
         confirmed to break inner layout silently). -->
{chr(10).join(scene_divs)}

    <!-- Audio. Two speaker buses. Per-TURN clips, not per-scene: this is a
         dialogue, so a scene carries 2-5 takes from alternating voices. -->
    <hf-audio-group id="vo-soulhabit" data-label="SOULHABIT" data-volume="1"
                    data-fx-chain='{fx_chain("S")}'>
    </hf-audio-group>
    <hf-audio-group id="vo-jay" data-label="JAY" data-volume="1"
                    data-fx-chain='{fx_chain("J")}'>
    </hf-audio-group>
{chr(10).join(audio_divs)}

    <!-- Music bed, carved against BOTH voice groups (hyperframes-audio:
         "sources" is a list, summed onto the bed's own clock -- one analysis
         covers a two-speaker dialogue). strength 0.25 is the documented
         default: audible room for the voice without reading as a hole. -->
    <audio id="bed-music" src="{bed_src}"
           data-start="0.000" data-duration="{bed_dur:.3f}"
           data-track-index="20" data-volume="{bed_vol}"
           data-fx-carve='{{"enabled":true,"sources":["vo-soulhabit","vo-jay"],"strength":0.25,"dynamic":true}}'></audio>

    <!-- Local one-shot SFX. Own track, no carve of their own -- each is a
         short transient at a transition or reveal beat, not a bed. -->
{chr(10).join(sfx_divs)}
  </div>

  <style>
    *,*::before,*::after {{ box-sizing:border-box; }}
    html,body {{ margin:0; padding:0; background:#F7F5F0; }}
    .scene.clip {{ position:absolute; inset:0; }}
  </style>

  <script src="assets/vendor/gsap-3.14.2.min.js"></script>
  <script>
    // The root timeline's only job is scene handoff. A plain crossfade stays
    // banned -- grounds alternate ink/paper and blending two gives a muddy
    // near-blank midpoint -- but a clip-path wipe reveals the incoming scene at
    // its own resting position without translating anything and without
    // touching opacity, so no frame composites two grounds AND no content is
    // dragged through a reserved safe-area zone.
    window.__timelines = window.__timelines || {{}};
    var tl = gsap.timeline({{ paused: true }});
{chr(10).join(xitions)}
    tl.to({{}}, {{ duration: {total:.3f} }}, 0);   // anchor: tl.duration() === root
    window.__timelines["main"] = tl;
  </script>
</body>
</html>
'''
    (ROOT / "index.html").write_text(html)
    nch = sum(1 for cid, _, _, _ in timing[1:] if cid in CHAPTERS)
    print(f"index.html: {len(timing)} scenes, {len(audio_divs)} VO clips, "
          f"total {total:.3f}s ({int(total//60)}:{total%60:05.2f})")
    print(f"  transitions: {len(xitions)} ({nch} chapter wipe-UP, "
          f"{len(xitions)-nch} within-chapter wipe-LEFT)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
