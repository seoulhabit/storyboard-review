---
format: 1080x1920
duration: 34.0s
message: "You're probably using snail mucin wrong. Mist first, then apply — or it pulls moisture out of your skin instead of in."
arc: mistake -> mechanism -> fix -> payload -> credibility -> loop
audience: "Same TikTok/Shorts skincare audience as the source video"
mode: skill-audit rebuild, packaging + structure only — see REPORT.md
---

## Why this exists

Rebuild of `LPqIuEYOx3s` (source: `videos/snail-mucin-medical-secret/`, 113.84s, 100 views)
against the revised `faceless-video-craft` skill. Diagnosis (full findings table in
`REPORT.md`): retention failure, not packaging — title scored 94 vs the channel's 10.4x
winner's 90. Root cause is structural: scene length ~2x the winner's, payoff delayed to
13.5s in a 2s-window format, 60.5% of runtime inside a >3s cadence gap, closing beat is a
generic subscribe card with no engineered loop.

Scope (user-confirmed, wider than the brief's default "first 15s"): full re-cut to 30-40s,
because rebuilding the opening of a 114s short does not fix a 114s short.

## Catalog discovery (production-loop step 1)

Checked `catalog/README.md` + `catalog/index.html` before beats were written.

- **`catalog/visual-components/split-compare/`** — bisector + one-side tint-flood mechanism
  for "these two things aren't rivals" comparisons. Matches Scene 02 (dry vs. misted sponge)
  exactly — the source video's own content already IS a two-field comparison, just never
  built as one. Adapted (not copied verbatim): fields are `{left: DRY SPONGE, right: MISTED
  SPONGE, interrogated: "right"}`. Component's own resolve time (~1.15s: divider -> labels ->
  flood) leaves room inside the 6s scene for the PANICS/ABSORBS reversal beat.
- **`catalog/visual-components/term-definition/`** — checked against Scene 04 (3 ingredient
  cards in 8s). **Rejected, not adapted**: TermDefinition is a full-frame single-term cycle
  with a continuous progress rail, built for a slow glossary sweep of many terms — its own
  choreography assumes settle time per term that a 3-card/8s burst doesn't have. Per the
  skill's own component-check rule ("skip it honestly if the content doesn't actually match
  rather than forcing a fit"), Scene 04 uses a lighter native 3-card stagger instead.
- **`catalog/ingredients/snail-mucin/`** and **`catalog/ingredient-photography/12-*`** —
  reviewed; not used. Both are static poster/photography assets for a different beat shape
  (a full ingredient-profile card), not the fast payload burst this scene needs.

## Asset manifest (production-loop step 4) — everything reused, nothing generated

| Asset | Source | Used in |
|---|---|---|
| `06-cheekbone-glow.png` | `videos/snail-mucin-medical-secret/public/` | Scene 01 (mistake) AND Scene 06 (loop close) — same plate both ends, deliberately, to close the loop |
| `05a-dry-sponge.png` | same | Scene 02, left field |
| `05b-wet-sponge.png` | same | Scene 02, right field |
| `03-macro-droplet.png` | same | Scene 04 (payload) background |
| `01a-archival-lab.png` | same | Scene 05 (credibility), compressed from the source's 14s treatment to 6s |
| `01b-macro-slime-spatula.png` | same | Scene 03 (fix), MIST step texture |
| 3x woff2 fonts | same | all scenes |

Not reused: `02-routine-montage.png`, `04-snail-mesh.png`, `snail-mucin-bottle.png` — no beat
in the tighter 34s cut needs them. Nothing new was generated; the source project's own plates
covered every beat.

## Component check (production-loop step 5)

`split-compare` reused/adapted (Scene 02). `spring-pop` and `yt-camera-move` installed via
`npx hyperframes add` (same registry items the source project itself uses) for entrance pops
and the Ken Burns drift on Scene 05's archival plate. `term-definition` checked, rejected —
see Catalog discovery above.

## Beat sheet

Duration 34.0s. Cadence contract: state change at least every ≤2.5s, no gap >3s anywhere —
measured from the actual timeline source before render, not estimated (see
`REPORT.md`'s cadence-audit script for the source project's own false-positive/negative
history on this exact measurement).

| # | Scene | Window | Len | Beats (~every ≤2.5s) |
|---|---|---|---|---|
| 01 | mistake | 0.0-2.0 | 2.0s | t0: plate + headline both at rest (frame zero = payoff, not setup) · t0.9: sub-line lands |
| 02 | why (SplitCompare) | 2.0-8.0 | 6.0s | t0: cut-in · t0.25/0.35: labels · t0.7: flood · t2.1: PANICS/ABSORBS reversal swap · t4.2: "moisture magnet" line |
| 03 | fix | 8.0-16.0 | 8.0s | t0: 01 MIST · t2.6: 02 PAT — NEVER RUB · t5.2: 03 SEAL IT IN · t7.3: all three settle, hold |
| 04 | payload | 16.0-24.0 | 8.0s | t0: droplet cut-in · t0.8: GLYCOLIC ACID · t3.1: ALLANTOIN · t5.4: HYALURONIC ACID · t7.0: "engineered by nature" |
| 05 | credibility | 24.0-30.0 | 6.0s | t0: archival cut, Ken Burns starts · t0.6: "1960s, Spain" tag · t2.8: "the same goo is now skincare's biggest obsession" · t5.0: dim for handoff |
| 06 | close + loop | 30.0-34.0 | 4.0s | t0: cut back to Scene 01's exact plate/position, camera creep eases scale back to 1.0 by t4.0 to preserve the loop match · t0.5: hero reads "Damp skin. Every time." (caption pill carries the literal VO line, "Mist first. Then apply." — kept distinct after QC found the two stacked verbatim) · t2.4: hold — last frame matches frame zero (ground colour + hero position) for a seamless replay |

Presenter (production-loop step 3): **type + photographic plate together**, one per scene,
consistent with the source project — not switched mid-video.

## Audio (added after the initial silent-first build)

Real VO recorded for all 6 lines — voice **Kimberly** (`voice_id: 674b71b8-1d2e-4087-8567-d1f53c0b9f3c`,
`voice_type: element`, via `text2speech_v2`/elevenlabs), the same voice already used in
`kbeauty-one-percent-line` and `seoulhabit-launch` on this channel (see
`../snail-mucin-medical-secret/SCRIPT.md`) — reused for channel-voice consistency, not
picked fresh. Raw takes measured -17.8 to -20.8 LUFS (real spread across a single-session
batch); two-pass `ffmpeg loudnorm` (measure -> apply, linear mode) brought every clip to
-16.6 to -17.0 LUFS / -1.0 to -1.2 dBTP, matching the -16.6 LUFS band this exact voice was
already normalized to on this channel (source project's `SCRIPT.md`) rather than an
arbitrary target. Raw pre-normalize takes kept at `assets/voice/{01..06}-raw.mp3` for
provenance, same convention the source project uses.

Every line fit its scene's window with real headroom (no scene needed retiming): 1.12s/2.0s,
4.88s/6.0s, 4.72s/8.0s, 4.88s/8.0s, 4.16s/6.0s, 2.16s/4.0s. Each clip carries a 100ms
fade-in/out via `data-automation` in the real `{version:1, lanes:[{target:"volume",
points:[{t,v}]}]}` shape — confirmed against this project's pinned `hyperframes@0.8.17`
by reading the installed CLI's own bundled validator (`dist/cli.js`), not assumed from the
skill's documentation, per the skill's own instruction to verify engine mechanics against
the shipped code before writing markup for a real render.

BGM reuses the exact same bed (`../snail-mucin-medical-secret/assets/bgm/track.loop.mp3`)
the source video ships, cropped to 34.0s with head/tail fades baked in, at the source
project's own `data-volume=0.12` — no `data-fx-carve` ducking added, matching the real,
confirmed convention the source project itself uses (inspected directly: no
`hf-audio-group`, no fx-carve anywhere in its `index.html`), not the skill's more
elaborate idealized bus/duck pattern, which this specific project has never actually shipped.

Pre-render gate item 12 ("does it make sense with the sound off?") still holds: every beat
was authored silent-first and the on-screen type carries the full meaning independent of
narration.

## Captions sidecar

`renders/snail-mucin-recut-34s.srt` — 10 cues, exported from the actual recorded VO, not
retyped from the script. Per *The captions* production order: each of the 6 clips was
transcribed individually with `npx hyperframes transcribe` (word-level timestamps), not as
one composite pass — an initial attempt at transcribing a single 32s composite of all 6
clips let Whisper collapse a real ~3s cross-scene silence gap into one word's reported
duration ("Glycolic" showed as 13.0-16.22s, spanning the actual gap between scenes 03 and
04). Per-clip transcription avoids that failure mode entirely. One ASR mishearing was
hand-corrected against the known-correct script: "Missed first, then apply." -> "Mist
first, then apply." (scene 06). Each clip's local word timestamps were shifted by its real
`data-start` offset from `index.html` (0.15/2.15/8.15/16.15/24.15/30.2s) to build one
globally-timed cue list, then split at natural clause boundaries to the 2-line/3-6-word
discipline. Verified against the actual mastered render's audio (not the pre-mix clips) by
sampling `ffmpeg volumedetect` at every cue's start timestamp — 9 of 10 showed strong
signal (-0.9 to -5.6 dB); the tenth (-12.5 dB, a fast quiet "and") was confirmed as real
speech, not a timing miss, against a wider window. No cue's end timestamp exceeds its
clip's real duration (checked per clip, per the skill's Whisper-hallucination-past-end-of-
audio warning).
- **No chapters, no end-screen scene.** Both are long-form-only per the skill's own Formats
  table. A Short's equivalent mechanism is the engineered loop, built into Scene 06.
- **No .srt sidecar produced this pass** — no final mixed VO exists yet to transcribe from
  (see *The captions* production order, step 1: transcript is generated from the *final
  mixed* VO, not before it exists).
