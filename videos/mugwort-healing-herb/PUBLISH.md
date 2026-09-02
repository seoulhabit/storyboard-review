# Publish envelope — Mugwort

**Delivery master (round 4, pixel-verified re-cut):**
`renders/mugwort-healing-herb_delivery.mp4` — this is the current publish candidate,
superseding every prior round below. Not yet copied to
`/Users/korswedie/Desktop/ingredent videos/Mugwort/` — do that only after this round is
approved, since round 3's copy there is now stale (pre-photography, pre-safe-area-fix).
- **Duration 57.70s** (unchanged — VO and every `index.html` `data-start`/`data-duration`
  were frozen for this whole round; only scene CSS/JS and the audio automation layer changed)
- MP4 container · H.264 video, 1080×1920, 30fps · AAC 48kHz stereo 256kbps
- **−14.23 LUFS integrated · −1.50 dBTP** (two-pass `ffmpeg loudnorm`, measured then applied
  with `linear=true`; video stream copied through unchanged from the render)
- Rendered `hyperframes@0.8.20 --quality high --workers 1`; `npm run check` clean (0 errors,
  35/35 contrast checks pass — up from 33 with the new photo captions/labels). QA this round
  was pixel-based, not a source read: `scripts/check-safe-area.py` (0 findings across 231
  sampled frames, was FAIL on 172 frames pre-fix), `scripts/check-static-hold.py` (0 findings
  at a 2.5s ceiling, was ~31.5s of the 57.7s runtime frozen pre-fix), plus frame-zero and
  every scene-boundary frame extracted and inspected directly (see frame.md's Round 4 section
  for the full measured breakdown and why).

**What changed this round, in one line each:** safe-area tokens now actually sized into every
scene's content column (was 33px past the right rail); photographic plates in 3 of 6 beats,
sourced from this repo's own shared catalog (was zero anywhere); continuous motion for each
scene's full duration (was frozen for over half the runtime); type raised to this project's
own stated floor; `.srt` and a finalized thumbnail now exist (were missing).

**Captions, 2026-09-01:** `captions/mugwort-healing-herb.srt` and `.vtt` (44 cues
each, word-for-word identical, timestamps verified against the raw per-clip
`assets/voice/0N.words.json` ASR transcripts — every cue start matches exactly;
end times are deliberately snapped to the next cue's start for gapless
continuous coverage within a VO clip, with real, SFX-covered pauses preserved
at the 5 clip-to-clip boundaries). Both files moved from `renders/` into a
dedicated `captions/` folder, matching `peeling-question-open`'s convention;
no other project doc hardcoded the old `renders/` path. `.vtt` was previously
missing — `peeling-question-open` already shipped both formats, this project
only had the `.srt`.

**Superseded — delivery master (round 3, pasted-review pass):** same 57.70s duration,
−13.81 LUFS / −1.91 dBTP, no photography, the safe-area/static-hold defects above unfixed.
**Superseded — round 2 (tightened):** −13.96 LUFS / −1.93 dBTP, pre-round-3 caption position.

**Title:** Mugwort: The Korean Healing Herb Your Routine Is Missing
**Description:**
The thousand-year Korean herb, and the one molecule inside it researchers actually study.
Lab findings on eupatilin: Jung et al. 2018 (PMID 29353040), Jung et al. 2017
(PMID 28899779) — mouse model and in-vitro evidence, not human clinical trials.
Usage guidance in this video is general education, not medical advice.
#skincare #kbeauty #mugwort #skinbarrier

**Pinned comment:** 🍃 = your skin turns red at everything. Which ingredient should we
break down next?

**Compliance note:** mechanism claim carries on-screen PMID pills + explicit
"not a human clinical trial" scope line; protocol and layer-zero beats carry
`○ UNSOURCED — no record in this system` flags, styled as a bordered badge (round 3.1,
unchanged this round). Beat 2/5 usage framing is authored guidance.

**Imagery, corrected:** round 3's claim of "no photographic/generated imagery anywhere —
browser-drawn only" was a description of an oversight presented as a design decision, not an
actual decision — two finished mugwort plates already existed in this repo's own shared
catalog (`catalog/ingredient-photography/18-mugwort.png`, plus an essence-bottle plate in
`catalog/product-photography/`) and were never discovered because the project's own
`BRIEF.md` asset manifest never listed an image line and catalog discovery never ran. See
`assets/plates/` and frame.md's Round 4 section for what was added and where.

**Published link:** https://hyperframes.dev/p/07acee27-53ed-429d-92d5-873788c12e9c — this
link points at round 3's content and is now stale. Re-publish only with the user's explicit
go-ahead (per this skill's action-category rules, publishing is not something to run
speculatively); until then this is a record of the prior link, not a live one for round 4.
