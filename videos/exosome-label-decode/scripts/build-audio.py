#!/usr/bin/env python3
"""Emit the root composition's audio block.

Two things this exists to get right, both of them silent-failure traps on the
pinned engine version:

1. `data-automation` shape. The flat {"volume":[[t,v],...]} form is rejected at
   RENDER time (`Unsupported automation version`) while `check` passes it, so a
   lint-clean project can still fail to render. The versioned lane form is
   emitted here instead.

2. A volume lane REPLACES `data-volume` -- it does not scale it. Writing a
   fade's plateau as v:1 makes the clip play at full unity gain for the whole
   plateau regardless of its data-volume, which is inaudible in the source and
   only shows up when someone listens. So every plateau below is written as the
   clip's REAL intended level, and `data-volume` is kept only as the
   no-automation fallback.
"""
import json
import subprocess
from pathlib import Path

SFX_DIR = Path("assets/sfx")

# (id, file, start_abs, volume, note)
SFX = [
    # --- scene 1 (0.000 - 4.450) ---
    ("s1-annot",  "click-soft.mp3",                             0.450, 0.22, "annotation row lands"),
    ("s1-stamp",  "paper-stamp-thump-the-myth-stamp-landing.mp3", 1.450, 0.42, "coral payoff bar strikes"),
    ("s1-rule",   "whoosh-soft-photo-reveal.mp3",               2.550, 0.25, "celadon rule draws"),

    # --- scene 2 (4.450 - 15.200) --- 3 of 7 vesicles get a tick, not all 7
    ("s2-v1",     "droplet-tick.mp3",                           5.900, 0.22, "vesicle release"),
    ("s2-v2",     "droplet-tick.mp3",                           6.500, 0.20, "vesicle release"),
    ("s2-v3",     "droplet-tick.mp3",                           7.100, 0.18, "vesicle release"),
    ("s2-src1",   "click-soft.mp3",                             9.800, 0.26, "source chip"),
    ("s2-src2",   "click-soft.mp3",                            10.170, 0.26, "source chip"),
    ("s2-src3",   "click-soft.mp3",                            10.540, 0.26, "source chip"),
    ("s2-cite",   "click-soft.mp3",                            13.000, 0.18, "citation pill"),

    # --- scene 3 (15.200 - 28.000) ---
    ("s3-stamp",  "paper-stamp-thump-the-myth-stamp-landing.mp3", 15.750, 0.50, "LIMITED stamp -- the bold beat"),
    ("s3-n1",     "click-soft.mp3",                            17.050, 0.28, "evidence node fills"),
    ("s3-n2",     "click-soft.mp3",                            17.350, 0.28, "evidence node fills"),
    ("s3-strike", "whoosh-soft-photo-reveal.mp3",              22.800, 0.34, "coral strike across the pair"),
    ("s3-cite",   "click-soft.mp3",                            24.650, 0.18, "citation pill"),

    # --- scene 4 (28.000 - 40.700) --- one toggle per gate, ticks for sub-beats
    ("s4-g1",     "ui-toggle-trimmed.mp3",                     31.950, 0.30, "gate 01 activates"),
    ("s4-g2",     "ui-toggle-trimmed.mp3",                     33.280, 0.30, "gate 02 activates"),
    ("s4-s2b",    "click-soft.mp3",                            35.550, 0.22, "gate 02 second clause"),
    ("s4-g3",     "ui-toggle-trimmed.mp3",                     37.180, 0.30, "gate 03 activates"),
    ("s4-s3b",    "click-soft.mp3",                            39.100, 0.22, "gate 03 second clause"),
    ("s4-cite",   "click-soft.mp3",                            39.850, 0.18, "citation pill"),

    # --- scene 5 (40.700 - 48.250) ---
    ("s5-bis",    "whoosh-split-reveal-short.mp3",             42.250, 0.34, "bisector draws down"),
    ("s5-flood",  "whoosh-soft-photo-reveal.mp3",              43.600, 0.26, "interrogated side floods"),
    ("s5-neq",    "paper-stamp-thump-the-myth-stamp-landing.mp3", 44.250, 0.38, "the not-equals punches in"),

    # --- scene 6 (48.250 - 55.800) ---
    ("s6-v2",     "click-soft.mp3",                            50.080, 0.24, "second verdict line"),
    ("s6-rule",   "whoosh-soft-photo-reveal.mp3",              52.150, 0.26, "celadon rule draws"),
    ("s6-lock",   "bright-glass-chime.mp3",                    54.200, 0.40, "SeoulHabit lockup"),

    # --- scene 7 end card (55.800 - 59.000) --- one soft cue only; the
    # chime already landed at 54.20 and a second would crowd the sign-off.
    ("s7-bar",    "click-soft.mp3",                            56.250, 0.22, "end-card rule draws"),
]

VO = [  # (index, start_abs, duration) -- durations MEASURED from the final takes
    (1, 0.100,  4.156),
    (2, 4.550, 10.438),
    (3, 15.300, 12.482),
    (4, 28.100, 12.399),
    (5, 40.800,  7.217),
    (6, 48.350,  7.109),
]

VIDEO_END = 59.000
BGM_VOL = 0.30

# The channel's voiceover bus, reused verbatim across projects -- this chain is
# what makes the channel's narration sound like the same show.
FX_CHAIN = {
    "version": 1,
    "nodes": [
        {"type": "highpass",   "id": "n1", "label": "Remove Rumble",     "params": {"frequency": 90, "q": 0.707, "poles": "2"}},
        {"type": "peaking",    "id": "n2", "label": "Add Weight",        "params": {"frequency": 150, "gain": 0.8, "q": 1.2}},
        {"type": "compressor", "id": "n3", "label": "Even Out Loudness", "params": {"threshold": -24, "ratio": 4, "attack": 5, "release": 140, "knee": 2, "makeup": 3, "mix": 1}},
        {"type": "peaking",    "id": "n4", "label": "Add Clarity",       "params": {"frequency": 3000, "gain": 2.5, "q": 1}},
        {"type": "peaking",    "id": "n5", "label": "De-ess (fallback)", "params": {"frequency": 6500, "gain": -4, "q": 3.5}},
        {"type": "limiter",    "id": "n6", "label": "Peak Ceiling",      "params": {"limit": -9, "attack": 0.05, "release": 40, "level_out": 0}},
    ],
}


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;")


def automation(dur, level, fade=0.06):
    """Versioned volume lane. Plateau is the clip's REAL level, never 1."""
    f = min(fade, dur / 3.0)
    pts = [{"t": 0.0, "v": 0.0},
           {"t": round(f, 3), "v": level},
           {"t": round(dur - f, 3), "v": level},
           {"t": round(dur, 3), "v": 0.0}]
    return {"version": 1, "lanes": [{"target": "volume", "points": pts}]}


def dur_of(p):
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
        capture_output=True, text=True, check=False).stdout.strip())


def main():
    out = []
    errs = []

    out.append("    <!-- BGM: the channel's most-used bed (shared by 5 projects), re-cut")
    out.append("         from its LIVE region only. The 180s master fades out from ~48s and")
    out.append("         is true digital silence past 60s, so a naive 0-55.8s crop would have")
    out.append("         faded the last 6s to nothing and handed the replay a dead beat.")
    out.append("         Declick fades (200ms) are baked into the file, so no volume lane is")
    out.append("         needed here -- which also keeps it clear of the lane-replaces-volume trap. -->")
    out.append(f'    <audio id="bgm" src="assets/bgm/bed-59.0s.wav" data-start="0" '
               f'data-duration="{VIDEO_END:.3f}" data-track-index="1" data-volume="{BGM_VOL}"\n'
               f'           data-fx-carve=\'{{"sources":["voiceover"],"strength":0.28}}\'></audio>')
    out.append("")

    out.append('    <hf-audio-group id="voiceover" data-label="Voiceover" data-volume="1"')
    out.append(f'      data-fx-chain="{esc(json.dumps(FX_CHAIN, separators=(chr(44), chr(58))))}">')
    for i, st, d in VO:
        au = automation(d, 1.0, 0.08)
        out.append(f'      <audio id="vo-{i:02d}" src="assets/voice/{i:02d}.wav" data-start="{st:.3f}" '
                   f'data-duration="{d:.3f}" data-track-index="10" data-volume="1" data-audio-group="voiceover"')
        out.append(f'             data-automation="{esc(json.dumps(au, separators=(chr(44), chr(58))))}"></audio>')
    out.append("    </hf-audio-group>")
    out.append("")

    # Track assignment is COMPUTED, not hand-written: two SFX whose windows
    # overlap are pushed onto separate track indices. A hand-set constant track
    # produced a real `duplicate_audio_track` error here (two 0.366s clicks
    # 0.30s apart), and hand-fixing one instance would not stop the next
    # retime from reintroducing it.
    placed = []          # (start, end, track)
    resolved = []
    for sid, fn, st, vol, note in SFX:
        p = SFX_DIR / fn
        if not p.exists():
            errs.append(f"missing sfx: {fn}")
            continue
        d = dur_of(p)
        end = st + d
        if end > VIDEO_END:
            errs.append(f"{sid}: {fn} runs to {end:.3f}s, past video end {VIDEO_END}")
        track = 20
        while any(t == track and st < pe and ps < end for ps, pe, t in placed):
            track += 1
        placed.append((st, end, track))
        resolved.append((sid, fn, st, d, vol, note, track))

    for sid, fn, st, d, vol, note, track in resolved:
        au = automation(d, vol, 0.05)
        out.append(f'    <!-- {note} -->')
        out.append(f'    <audio id="sfx-{sid}" src="assets/sfx/{fn}" data-start="{st:.3f}" '
                   f'data-duration="{d:.3f}" data-track-index="{track}" data-volume="{vol}"')
        out.append(f'           data-automation="{esc(json.dumps(au, separators=(chr(44), chr(58))))}"></audio>')

    tracks_used = sorted({t for _, _, _, _, _, _, t in resolved})
    print(f"  SFX tracks used: {tracks_used}")

    if errs:
        print("build-audio: FAILED")
        for e in errs:
            print("  -", e)
        raise SystemExit(1)

    Path("captions/_audio.partial.html").write_text("\n".join(out) + "\n")
    print(f"build-audio: {len(VO)} VO + 1 BGM + {len(SFX)} SFX")
    print("  every SFX ends inside the video; every plateau is the clip's real level")
    print("  wrote captions/_audio.partial.html")


if __name__ == "__main__":
    main()
