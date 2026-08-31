# red-ginseng-glass-glow — BRIEF

New treatment of Red Ginseng, distinct from `red-ginseng-two-routes` (older, evidence-structure
lane). This build follows the user's explicit 2026-08-30 brief verbatim:

- 9:16, 1080×1920, ~60s Short, six beats on the user's supplied timings/script.
- **Photoreal generated plates** (Higgsfield `cinematic_studio_2_5`, 2k, one plate per beat,
  user-supplied prompts + a shared warm-amber grade tail for cross-plate cohesion).
  This is a deliberate, user-directed departure from the browser-drawn-only dimensional lane
  (seoulhabit-video-3d); the craft/render contract still applies in full.
- **VO = Kimberly** via Higgsfield seed_audio (voice_type element,
  voice_id 674b71b8-1d2e-4087-8567-d1f53c0b9f3c). Energetic pacing; enforced micro-pause
  (~0.5s) after "The real magic?" in beat 5 (inserted at the word boundary if the take's
  natural gap is short).
- Burned-in top-band captions (y196–330 band), script-authoritative text with whisper word
  timing, per series convention. Kimberly runs faster than the syllable formula — beats are
  timed to real take lengths after gating, never to estimates.
- Audio gate per series: duration → silence → transcript-diff (medium.en) → adeclick →
  tail-spike scan (expect the seed_audio run-to-edge tail defect on ~1–2 takes; remedy =
  40ms fade + 0.25s pad). Watch "ginsenosides" for the dense-plural articulation failure mode.
- Render `npx hyperframes@0.8.19 render --quality high --workers 1`; verify by extracted
  frames (frame zero dense and fully composed); master to −14 LUFS / ≤−1 dBTP with
  `alimiter ... level=0`; deliver master copy to `~/Desktop/ingredent videos/Ginseng/`.

## Claims discipline (lane-independent truth rules)

Script is user-authored and kept verbatim in VO/captions. On-screen source treatment:

| Beat | Claim in VO | Treatment |
|---|---|---|
| 4 | ginsenosides "neutralizing free radicals" | Chip: **In vitro** — ginseng-root exosome-like nanoparticles (carrying ginsenosides) reduced ROS in UVB-stressed human keratinocytes. J Ginseng Res 2024, PMID 38465216. Route label "IN VITRO" is load-bearing. |
| 5 | "ramping up collagen" | Chip: **Oral RCT** — 3 g/day red-ginseng herbal mixture, 24 wk, n=82: ↑ type I procollagen, improved facial wrinkles. J Med Food 2009, PMID 20041778. Route label "ORAL, 24 WK" printed — the trial is ingestion, not topical; never cite it as topical support. |
| 5 | "boosts blood circulation" | **○ UNSOURCED** — no matching record found; flag renders adjacent per confirmed series posture (flag, don't fabricate, don't silently strip). |
| 2 | "retinol is destroying your skin barrier" | Rhetorical framing of documented retinoid irritation; no ginseng claim; no chip. |
| 6 | "just add a red ginseng serum" | Instruction/CTA, not an efficacy assertion; note the route tension vs the oral RCT is visible via beat 5's printed route label. |

## Structure

index.html = main composition; per-beat sub-compositions in `compositions/frames/`
(01-hook … 06-cta), VO track 10, captions track 5, plates full-bleed with seek-safe
Ken Burns (GSAP paused timelines in `window.__timelines`, no rAF/Date.now).

## Rework round 2 (2026-08-30, pasted review via /goal)

All six items resolved; two notes on judgment calls:

1. **Micro-pause removed** (review BLOCKER #1 heard it as dead air). This reverses the
   original brief's explicit "add a 0.5s micro-pause" note — treated the later directive
   from the same user as superseding; take 05 rebuilt from raw (8.430s), S6 41.897→41.397,
   total 50.282s. Beats 1–4 untouched; beat 5/6 captions + SFX recomputed programmatically.
2. **○ UNSOURCED flag replaced with a real citation, not deleted** (review MAJOR #4 offered
   either). Found honest support: Korean red ginseng oral RCT, 3 g/day, 8 wk, n=80 women —
   significantly higher hand/foot skin temperature, "peripheral vasodilation" (Park KS et al.,
   J Ethnopharmacol 2014, PMID 25284751). Chip prints route + what was measured; the
   never-fabricate posture holds. Beat 5 now carries one combined two-source card
   (circulation PMID 25284751 + collagen PMID 20041778), single aqua border.
3. CTA stack raised exactly 384px (20% of height) per review #2: bottom 520→904.
4. Captions switched to ink cards (white on rgba(22,24,26,.88)) per review #3.
5. Plate 03 regenerated as a hard vertical split, no ghost blend, per review #5
   (old blend kept at assets/plates/_03-blend-v1.png).
6. Review #6 (diversify future videos with real b-roll/human elements) — series-level
   note, no change to this video; recorded in PUBLISH.md.
