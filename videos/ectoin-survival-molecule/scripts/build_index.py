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

Music bed + local SFX (plan step 3/"Music bed and cues"). The bed is ONE
frozen, finite file (assets/music/bed.mp3, built once via `ffmpeg
-stream_loop` from the sibling's loop-prepared source and committed, never a
runtime loop) carved against the single VO group ("voiceover") this project
uses -- no `dynamic` key (see this project's CLAUDE.md: data-fx-carve names
the GROUP, and that key does not belong here). Every SFX cue is a short local
one-shot pulled from an existing kit (catalog convention: reuse before
generating), never carved. Timestamps below are read off index.seams.json /
timing.walk() (chapter seams, the 27->28 arrive completion, the 28->29
settle completion, and scene 20's second spoken "12" -- Whisper transcribes
the digit, not the word "twelve"), not estimated.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLUG = "ectoin-survival-molecule"
FADE = 0.08         # 80ms edge fade on every clip -- avoids a click at the cut
VO_LEVEL = 1.0       # VO is the reference level; plateau IS this, not a scaled 1.0

# Bed measures -14.3 LUFS (verified: scripts/gen bed build, ffmpeg ebur128).
# In-engine VO reads ~-17 LUFS after the standing fx chain's makeup gain
# below. 18-24dB under VO is the target depth -> 0.08 is the middle of that
# band as a starting data-volume; adjust 0.06-0.10 from the measured render
# per the plan (`check-seams.py --render`'s bed-depth check, once wired).
# Duration comes from the walk. It used to be the literal 338.145 -- correct
# for the cut that wrote it and silently wrong for the next one, which is
# how a longer edit runs out of bed at the exact moment the end card needs
# music under it. scripts/build_bed.py cuts the file itself to the same
# number, so the two cannot disagree.
BED_SRC, BED_VOL = "assets/music/bed.mp3", 0.08
# The bed holds, then resolves ACROSS the end card rather than stopping
# with the last word -- the review asked for the music to resolve, not cut.
BED_RESOLVE = 3.2

# (at_seconds, file, duration, volume, note). Duration/volume verified by
# ffprobe against the actual files in assets/sfx/, not guessed.
# DERIVED, not frozen. These were eight literal timestamps, correct for the cut
# that measured them and silently wrong for every cut after it -- a re-paced
# scene moves its seam and the chime then lands mid-sentence. Each cue below
# says WHERE it belongs in the grammar; walk() says when that is.
#
# (file, duration, volume) per cue kind. Durations/volumes are ffprobe'd facts
# about the files in assets/sfx/, not guesses.
SFX_CHIME = ("chime-trimmed.mp3", 1.100, 0.30)
SFX_CHIME_LONG = ("chime.mp3", 2.500, 0.28)
SFX_TICK = ("citation-tick-trimmed.mp3", 0.500, 0.36)
SFX_IMPACT = ("impact-bass-2.mp3", 2.592, 0.34)
# impact-bass-2.mp3's own peak sits ~0.403s into the file (measured via astats
# per-frame peak scan), so its cue starts that far BEFORE the beat it is meant
# to land on -- otherwise the thump arrives late by the file's silent lead-in.
IMPACT_PRE_ROLL = 0.403


def sfx_cues(scenes):
    """[(at, file, dur, vol, note)] -- every cue anchored to a boundary."""
    by_cid = {s.cid: s for s in scenes}
    cues = []

    def seam_completion(cid):
        """When the wipe INTO `cid` finishes: its own start plus the kind's d."""
        s = by_cid[cid]
        return s.start + KIND[s.kind_in][0]

    for cid in ("08-humectant", "12-load", "16-trial104", "22-whofor", "26-kbeauty"):
        s = by_cid[cid]
        # The chime marks the chapter seam itself, +0.10 so it reads as arriving
        # with the wipe rather than under the outgoing scene's last syllable.
        f, d, v = SFX_CHIME
        cues.append((round(s.start + 0.10, 3), f, d, v, f"chapter seam into {cid}"))

    # 20-twelve's second spoken "12" -- the standalone "Twelve." Whisper
    # transcribes the digit, not the word, hence the marker text.
    tw = by_cid["20-twelve"]
    hits = [w for w in tw.words if w["text"].strip().strip(".,") == "12"]
    if len(hits) < 2:
        raise SystemExit("20-twelve: expected two spoken \"12\"s for the citation "
                         "tick; found " + repr([w["text"] for w in tw.words]))
    f, d, v = SFX_TICK
    cues.append((round(tw.vo_start + hits[1]["start"], 3), f, d, v,
                 '20-twelve: second spoken "12"'))

    f, d, v = SFX_IMPACT
    cues.append((round(seam_completion("28-remember") - IMPACT_PRE_ROLL, 3), f, d, v,
                 "27->28 arrive completion (peak-aligned)"))
    f, d, v = SFX_CHIME_LONG
    cues.append((round(seam_completion("29-cta"), 3), f, d, v,
                 "28->29 settle completion"))
    return sorted(cues)


sys.path.insert(0, str(Path(__file__).resolve().parent))
from timing import walk
from transitions import plan, KIND


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

    bed_src, bed_vol = BED_SRC, BED_VOL
    bed_dur = total
    sfx = sfx_cues(scenes)
    # The bed holds at level until the end card is on screen, then resolves to
    # zero across it. build_bed.py's own 0.25s declick is an anti-click measure,
    # not a musical ending -- on its own it reads as the track being switched
    # off, which is the "do not cut it abruptly" note.
    bed_lane = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": [
        {"t": 0.0, "v": 0.0},
        {"t": 0.6, "v": bed_vol},
        {"t": round(max(0.6, bed_dur - BED_RESOLVE), 3), "v": bed_vol},
        {"t": round(bed_dur, 3), "v": 0.0},
    ]}]}, separators=(",", ":"))
    sfx_divs = [
        f'    <audio id="sfx-{i}" src="assets/sfx/{fname}"\n'
        f'           data-start="{at:.3f}" data-duration="{dur:.3f}"\n'
        f'           data-track-index="21" data-volume="{vol}"></audio>  <!-- {note} -->'
        for i, (at, fname, dur, vol, note) in enumerate(sfx)
    ]

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

    <!-- Music bed, carved against the single voiceover group (hyperframes-audio:
         "sources" is a list of group/audio ids, summed onto the bed's own clock).
         No `dynamic` key -- see this project's CLAUDE.md. -->
    <audio id="bed-music" src="{bed_src}"
           data-start="0.000" data-duration="{bed_dur:.3f}"
           data-track-index="20" data-volume="{bed_vol}"
           data-automation='{bed_lane}'
           data-fx-carve='{{"enabled":true,"sources":["voiceover"],"strength":0.25}}'></audio>

    <!-- Local one-shot SFX. Own track, no carve of their own -- each is a
         short transient at a transition or reveal beat, not a bed. -->
{chr(10).join(sfx_divs)}
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
