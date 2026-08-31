---
workflow: faceless-explainer
flow: automation
storyboard: yes
message: "Ceramides make up a huge share of your skin's barrier — fix that before layering on more actives."
destination: shorts
aspect: 1080x1920
language: en
audience: "skincare-curious viewers over-investing in actives while under-investing in barrier health"
length: 60s
angle: myth-bust / explainer
VO_MODE: adapted
style_preset: seoulhabit
---

## Intent

The user handed in a creator-style, on-camera storyboard (five timed
segments: person holding a serum bottle, pointing at the camera, scooping
moisturizer, zooming on an ingredient list) for a ceramides / skin-barrier
explainer that opens on a Retinol hook. Per the established SeoulHabit
precedent (`videos/retinol-patch-test`, `videos/kbeauty-one-percent-line`,
`videos/seoulhabit-launch`), this is adapted to a faceless motion-graphics
build rather than shot on camera — the original is preserved verbatim in
`user_script.txt`. Vibe: confident, mildly mythbusting, educational —
undercutting the "everyone talks about Retinol" assumption without
dismissing Retinol itself. Five scenes, matching the original 0:00–0:60
timing; actual scene durations will be set from measured TTS at Build, same
as every prior project in this pipeline.

This is a new, independent video — **not** a fulfillment of the "Retinal vs
Retinol" catalog gap (`catalog/ingredients/retinal-vs-retinol/README.md`).
That entry is a different piece (a retinal-vs-retinol active-ingredient
comparison); this one is a ceramides/barrier-repair explainer that only uses
Retinol as its opening contrast. Flagging this explicitly so the two aren't
conflated later.

## Assets

None supplied by the user. Scene 3's identity facts (what ceramides are,
what they're used for) reuse the checked-in glossary card verbatim —
`catalog/ingredients/skincare-ingredient-glossary/components/09-ceramides.html`
— rather than writing new copy. No photography asset is used for any beat;
the `retinol-patch-test` precedent found `catalog/ingredient-photography/`
isn't checked into git, so this project doesn't depend on it either.

## Customizations

- Design system: tokens/fonts to be copied from a checked-in
  `skincare-glossary-part-*` project's `index.html`, verified via
  `git ls-files` before use at Build — same provenance discipline as
  `retinol-patch-test/frame.md`. Do not hand-roll new token values, and do
  not pull tokens from `seoulhabit-brandshort` (confirmed during planning to
  be a separate, unrelated project with a different palette).
- Voice continuity: reuse HeyGen voice id `05f19352e8f74b0392a8f411eba40de1`,
  same as `red-ginseng-two-routes` and `retinol-patch-test`.
- Coral discipline: none of this script's five beats carries the
  safety-warning intensity that earned coral in `retinol-patch-test` (Frame
  5's "STOP" moment). Coral may go unspent in this video — consistent with
  the one-voltage-moment rule, not a gap to force.
- On-screen text beats preserved from the user's script: "What are they?"
  (Scene 3), "Plant-based & Bio-identical" (Scene 4).
- The original script's "point down for a subscribe CTA" beat is dropped as
  composition content — subscribe/follow prompts are platform-native UI in
  every other video in this pipeline, never drawn into the composition
  itself. "Subscribe for more skincare science" stays in the spoken VO only;
  the visual closes on the standard seoulhabit.com endcard instead (see
  STORYBOARD.md Frame 5).

## Notes

- **Sourcing — explicit decision, not an oversight.** This script's precise
  stats and absolute claims ("fifty percent of your skin's outer layer," "by
  age 30, you've lost about 40% of them," "they lock moisture in and block
  irritants out," "lab-made to perfectly match your skin") have no `ING-*`
  source record anywhere in this codebase — the existing Ceramides glossary
  card itself carries no source id either. The fourth of these ("perfectly
  match your skin") was caught during storyboard review, after the original
  sourcing decision — it falls under the same ship-as-written call, listed
  here for a complete record rather than left implicit. Per the user's
  explicit choice, these ship as written, with no citation chips (matching
  the glossary card's own current sourcing state). This is a deliberate
  departure from `retinol-patch-test`'s precedent, which softened its one
  unsourced overclaim rather than shipping it — flagged here so a future
  pass can find and revisit this decision if real sources surface.
- Run scoped to Setup only (`BRIEF.md`/`STORYBOARD.md`/`frame.md`/
  `user_script.txt`). `storyboard: yes` — unlike `retinol-patch-test`'s `no`,
  this project's frame-by-frame plan has not yet been reviewed, so the
  live-board review gate stays on for Build/Render.
- Build/Render did subsequently happen (captions ended up on the
  `caption_groups.json`/`captions.html` system, not the simpler `caption.txt`
  pattern `frame.md` had called for — a Build-time deviation from this doc,
  noted here rather than silently left inconsistent). First render:
  `renders/video.mp4`, 2026-08-29 13:12.

## Revision (2026-08-29) — stronger-hook cinematic cut

A second, explicit user request replaced this video's entire visual and audio
language, on top of the already-rendered v1 above. Recorded here rather than
silently overwriting the Setup-phase record, per this file's own practice.

**What changed and why:**

- **Visual language: flat paper/ink motion graphics → photoreal cinematic
  stills with Ken Burns motion.** This is a deliberate departure from
  `frame.md`'s explicit "no photorealism, no generative imagery" rule and this
  pipeline's established flat/restrained convention (shared with
  `retinol-patch-test`, `kbeauty-one-percent-line`, `seoulhabit-launch`, etc.).
  It was not my call to make silently — flagging it here so it's a visible,
  reversible decision rather than quiet drift. The user supplied 6 pre-generated
  image job IDs (Higgsfield `text2image_soul_v2` ×2, `marketing_studio_image`
  ×2, `cinematic_studio_2_5` ×1, `nano_banana_2` ×1), all verified real and
  `completed` via `show_generation_by_ids` before use, downloaded to
  `assets/images/`. If a future pass wants the original flat register back,
  `renders/video.mp4` + the git-free file history is the fallback — nothing
  from v1 was deleted, only the 3 frame files whose content was fully
  superseded (`02-evaporation.html`, `03-identity.html`, `04-the-catch.html`)
  were removed; `05-sourcing.html`/`06-outro.html`/`01-hook.html` were
  overwritten in place (same filenames, new content).
- **New hook.** "Everyone talks about Retinol…" (curiosity-gap open) →
  "Stop using Retinol until you do this one thing…" (pattern-interrupt/warning
  open). The "50%" stat moved from the hook into Scene 4's Ceramides
  explanation, since the new hook doesn't carry it.
- **Scene count/timing: 6 frames (~53.6s measured) → 6 scenes locked to a
  60s nominal grid** (0:00/0:05/0:15/0:35/0:50/1:00 per the user's exact
  brief), with scenes 2–3 sharing one continuous VO block cut on the "serums,"
  comma — not yet measured from real TTS (see TTS blocker below).
- **Captions: bottom pill / karaoke-highlight → full-screen center, true
  word-by-word.** Used the registry's `caption-kinetic-slam` component
  (`npx hyperframes add caption-kinetic-slam`), adapted from its 1920×1080 demo
  shape to this project's 1080×1920 canvas and `#captions-root` id, per the
  user's explicit "center-screen, word-by-word" instruction — a deliberate
  departure from `captions/authoring.md`'s generic portrait-caption position
  guidance (lower-middle), justified by that same explicit instruction.
- **New BGM prompt, explicit ducking, new SFX cue sheet** — see
  `audio_request.json` / `audio_meta.json` for the exact values in force.

**Voiceover — resolved via Higgsfield, not HeyGen.** HeyGen free-tier TTS
minutes were exhausted (`HTTP 402 insufficient_credit`) when first attempting
to regenerate voice for the new 5-line script — confirmed via
`npx hyperframes auth status` (`hello@seoulhabit.com`, plan: free). Per
`media-use/audio/references/tts.md`'s Preflight rule this was flagged rather
than silently routed around (a local-Kokoro fallback would have broken this
video's voice continuity with `red-ginseng-two-routes` / `retinol-patch-test`,
which reuse the same HeyGen voice). The user then explicitly directed a
provider switch: **Higgsfield `seed_audio`, voice element "Kimberly"**
(`voice_id: 674b71b8-1d2e-4087-8567-d1f53c0b9f3c`, `voice_type: element` — a
custom voice in this workspace, found via `list_voices`). This is therefore a
**second, deliberate voice-continuity break** on top of the visual-language
one above — Kimberly is a different voice from every other video in this
pipeline. Recorded here for the same reason as the visual change: a visible,
reversible decision, not silent drift. Generated via `generate_audio_batch`
(5 lines, `use_unlim: false`), downloaded to `assets/voice/01–05.wav`.

**Real timing supersedes the nominal 60s grid.** Real Kimberly VO measured
**~39.9s total** (`01`=5.240s, `02`=6.981s, `03`=11.557s, `04`=8.560s,
`05`=7.522s) — significantly faster than the brief's nominal sketch. Per this
pipeline's own standing convention ("nominal timing is a Setup-phase
scaffold, retimed from real TTS at Build" — see `frame.md`), scenes were cut
to the **real** measured audio rather than padded to force the nominal 60s:
final composition duration is **~40.26s** (a 0.4s hold added after the last
word). The scene2/scene3 visual cut (bathroom counter → cracked
desert/skin) lands on the real "serums," word boundary inside line 02's
audio, same mechanism as before, new absolute timestamp (~7.76s).
SFX/CERAMIDES-stamp sync points moved with their scenes (still exactly
aligned to the same narrative beats — "Enter Ceramides" / "Subscribe" — just
at new absolute seconds).

**Second revision pass — caption redesign + audio glitch + BGM provider swap.**
User feedback on the first Kimberly render drove four changes:

1. **Captions moved center-screen → lower third** (`top:1380px`, 240px band,
   ~72% down the 1920px canvas) — center placement blocked the split-screen
   face comparison and the 3D cell infographic, the two shots the captions
   were sitting on top of.
2. **Word-by-word → grouped 3-5 word phrases.** Re-authored the caption
   grouping algorithm to close a phrase at 5 words, or at 3+ words on
   sentence-ending punctuation or a >150ms pause — never across a script-line
   boundary. 25 groups total, all 3-5 words except 2 short trailing remainders
   at line ends (unavoidable without merging across sentences, which would
   have been worse). **Real bug found and fixed in the same pass:** the first
   attempt made each word its own CSS flex item for layout, which trims a
   span's own trailing space at the end of its inline formatting context —
   every phrase rendered as one run-together word ("DOTHISONETHING."). Fixed
   by moving the word spans into a plain (non-flex) inner block so normal
   text flow handles spacing and line-wrap natively.
3. **Removed the opaque scrim bar**, per explicit instruction, in favor of a
   stroke-only treatment: 4px 8-directional black outline + a couple of
   diagonal reinforcement shadows + soft ambient drop shadow. Verified via
   `hyperframes check`'s Contrast audit rather than assumed — the stroke
   alone cleared WCAG AA on every group (21/21) once strong enough; one
   borderline word (2.92:1) needed the stroke bumped from 3px to 4px to
   clear 3:1. No background bar needed in the end.
4. **The reported "0:04 scratch" was real** — diagnosed with an
   `ffmpeg showwavespic` waveform render (not audible to me directly) rather
   than guessed at. It was NOT an edit-seam issue at a clip boundary (the
   user's suggested fix assumed one); it was a sharp synthesis-artifact click
   baked into the raw `voice/01.wav` file itself, in the trailing silence
   after "barrier." finishes (~4.95-4.98s absolute in the first cut). Fixed
   at the root — trimmed `voice/01.wav` from 5.240s to 4.950s with a short
   fade-out — rather than masked with a crossfade/punch-in on a "second
   clip" that doesn't actually exist at that point in the timeline. This
   shifted line 1's duration and cascaded through every downstream scene
   start; full composition is now 39.970s (was 40.260s).

**BGM: local MusicGen stalled, switched to HeyGen retrieval.** The local
generation from the first pass (see below) ran for 53+ minutes of wall clock
while accumulating only ~9.5 minutes of actual CPU time (~17% utilization) —
not simply slow, something was stuck. Killed it and retrieved from HeyGen's
catalog instead (`bgm.mode: "retrieve"`, query "lo-fi chill upbeat electronic
synth beauty skincare focus"), then crossfade-looped the 24s result up to the
full composition length with `ffmpeg acrossfade` + fade in/out. This is a
mood-matched catalog track, not a prompt-generated one — a further, smaller
fidelity trade-off from the user's exact music brief, recorded for the same
reason as the others.

**Render-output naming — the v1 flat cut was overwritten, not preserved as
earlier stated.** `npx hyperframes render . -o renders/video.mp4` was used
for these iterations, same filename the original flat-design render occupied
(5.3MB, ~53.6s, described here as "untouched" when this revision started).
It is gone; overwritten by this cut's render. What survives from v1 on disk:
`assets/voice/06.wav` (untouched — v2's script only needed 5 lines),
`assets/bgm/track.loop.mp3` (untouched — v2's BGM file is `track.loop.wav`,
a different name), and all 9 of v1's original SFX files (untouched — v2's 4
new cues use different filenames). Not recoverable as rendered: v1's
`index.html`/`captions.html`/`01-hook.html` were overwritten (the exact prior
content is quoted verbatim earlier in this session's transcript and could be
reconstructed on request), `02-evaporation.html`/`03-identity.html`/
`04-the-catch.html` were deleted outright, and — the actual blocker to a
byte-exact restoration — v1's `voice/01-05.wav` (original HeyGen TTS) cannot
be regenerated without HeyGen credit, which is still exhausted.

Word timestamps: `npx hyperframes transcribe --language en --json`
(whisper `small.en`, since Kimberly/seed_audio doesn't return provider
timestamps the way HeyGen does). One manual correction: whisper dropped the
leading "Stop" in line 01 (merged into "using"'s span) — confirmed via
`ffmpeg silencedetect` showing continuous speech audio from t=0–0.869s (too
long for "using" alone) — re-inserted from that acoustic evidence rather than
trusted blindly. Caption exit timing also hardened after `hyperframes check`
briefly flagged `content_overlap` on a few tight real-speech word pairs: each
word's fade-out now always completes before the next word's entrance is
constructed geometrically (`min(word.end, nextWord.start - 0.02)`), not just
tuned by duration — holds regardless of how tight real ASR timestamps get.
