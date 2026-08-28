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
- Reuse the HeyGen voice id `05f19352e8f74b0392a8f411eba40de1` from
  `videos/snail-mucin-truth/audio_engine_meta.json` for narration continuity.

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
