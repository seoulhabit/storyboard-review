---
workflow: faceless-explainer
flow: automation
storyboard: no
message: "Snail mucin has a wild medical origin story, a genuine biological reason it works, and one easy-to-miss application step — not TikTok magic"
destination: shorts
aspect: 1080x1920
language: en
audience: "skincare-curious social viewers who've seen snail mucin trend but don't know the science"
length: 95s
angle: concept
style_preset: editorial-forest
---

## Intent

Explain the real science behind snail mucin skincare: where it came from (a
1960s Spanish radiation-burn observation), what it actually contains, how it's
produced, and the one common mistake (applying to dry skin) that makes people
think it doesn't work. Tone: "mad science" curiosity with a straight-faced
evidence check — playful hook and visuals, but every efficacy claim held to
the pipeline's evidentiary bar rather than TikTok hype language.

## Customizations

- VO_MODE: **verbatim** (revised — see Notes). The user's script, including
  its direct unhedged claims ("naturally loaded with Glycolic Acid to eat
  away dead skin," "massive doses of Hyaluronic Acid," "zero harm, zero
  stress," "miraculous cure"), is spoken essentially as written, segmented
  into frame-sized cues only for natural TTS phrasing — no rewriting for
  evidentiary hedging.
- Visuals are **photoreal, not invented vector** for every beat the script
  describes as a real shot (archival B/W lab footage, macro slime/spatula,
  skincare-routine hands, snail-on-mesh B-roll, dual sponge test, glowing
  cheekbone) — generated stills via Higgsfield `soul_2`, composited into the
  HyperFrames timeline with camera moves. This departs from the
  faceless-explainer preset's normal "invented graphics only" default,
  per explicit user direction (see Notes).
- Reuse `style_preset: editorial-forest` type ramp (Bricolage Grotesque /
  JetBrains Mono) for on-screen title cards and section labels only — the
  scene content itself is now photographic, not the palette-driven invented
  graphics used in `videos/snail-mucin-truth/`.
- **Voice changed 2026-08-29** (explicit user request) to **Kimberly**
  (creative-platform MCP `text2speech_v2`/elevenlabs, `voice_type: element`,
  `voice_id: 674b71b8-1d2e-4087-8567-d1f53c0b9f3c`) — the same workspace
  reference voice already used in `videos/kbeauty-one-percent-line/` and
  `videos/seoulhabit-launch/`. Replaces the originally-reused HeyGen voice id
  `05f19352e8f74b0392a8f411eba40de1` from
  `videos/snail-mucin-truth/audio_engine_meta.json`. See Notes for the full
  retime this triggered.

## Notes

- **Revision (2026-08-28): rebuilt to match the literal script.** The first
  build evidence-tuned the VO and replaced every described shot with
  invented vector graphics, per this repo's usual evidentiary bar (see
  project memory). The user's `/goal` Stop-hook rejected that build as not
  matching the condition they set — the exact pasted script and its literal
  visual descriptions. This revision honors that explicit, current
  instruction over the inferred house convention: VO is verbatim, visuals
  are photoreal reconstructions of the described shots, and the claim-id /
  citation-chip apparatus from the first build is removed (the script makes
  no citation claims). No publication gate applies to this revision — there
  are no forward-referenced source ids left to reconcile.
- This is a **new, separate project** from `videos/snail-mucin-truth/`
  (different script, different runtime, different title) — not a rebuild or
  replacement of that finished, already-rendered video.
- `storyboard: no` / `flow: automation` / `destination: shorts` /
  `aspect: 1080x1920` / `language: en` are remembered defaults confirmed in
  prior runs (`prefs.mjs`), reused here as the recommended and accepted
  answers rather than re-asked.
- `length` follows the verbatim script's own real spoken duration (measured
  from TTS, not estimated) — inside the faceless-explainer hard cap
  (~3 min).
- **Voice change + full retime (2026-08-29, explicit user request):** "change
  this to Kimberly voice." Kimberly's pacing differs from the original
  HeyGen voice per line, and not uniformly in one direction (line 1 -10.6%,
  line 2 +3.4%, line 3 -1.5%, line 4 -9.2%, line 5 +14.1%, line 6 -16.4%) —
  two lines came in *slower*, which would have truncated their audio against
  the old frame boundaries, so "leave timing as-is" was never a safe option.
  Flagged the full duration/loudness comparison before proceeding; user chose
  **full retime** (re-author every frame's internal choreography) over
  "recut boundaries only." All 6 VO lines re-recorded verbatim (text
  unchanged), loudness-matched (see SCRIPT.md), transcribed word-by-word
  (Parakeet/whisper fallback via the media-use audio engine) to get real per-word
  timestamps for Kimberly's actual delivery — every frame's word reveals, cut
  points, and SFX cues were re-anchored to those real timestamps rather than
  the prior evenly-spaced approximation, which is a net accuracy improvement
  independent of the voice change. Global structure moved from
  (0/15.125/28.97/54.466/77.637/99.24, total 117.421s) to
  (0/13.52/27.84/52.96/74.0/98.64, total 113.84s). Whole-video captions
  regenerated from the same per-word data (2-3 word groups breaking on
  clause punctuation or ≥0.12s pauses, matching this pipeline's established
  caption-pacing convention). Re-rendered and re-verified via snapshot at
  every new scene boundary; `npm run check` clean.
