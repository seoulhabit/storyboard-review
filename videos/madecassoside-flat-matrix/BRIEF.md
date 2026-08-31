---
workflow: faceless-explainer
flow: automation
storyboard: yes
message: "Madecassoside pitched as a scar-structure 'biological architect' — with every mechanism/efficacy line rendered flagged UNSOURCED, because this system holds no Centella/madecassoside records"
destination: reels
aspect: 1080x1920
language: en
audience: "SeoulHabit's evidence-conscious skincare audience (same series as pdrn-cellular-science / centella-tiger-grass)"
length: 50.400s (script was written to a 60s target; Kimberly's real pace ran faster — see Notes)
angle: concept
---

## Intent

Build the user's approved 60-second, seven-beat "Hyperframe" Madecassoside script
(hook → wound setup → hypertrophic-scar problem → identity/solution → mechanism snap →
flat-matrix result → loop) as a HyperFrames composition to the pdrn-cellular-science
standard. Full production blueprint (frame specs, claim audit, timing, sound map) at the
session artifact "Madecassoside Blueprint"; this BRIEF records what was actually built.

**Claim-sourcing posture (same explicitly confirmed deviation as PDRN/centella):** repo
search during centella-tiger-grass (2026-08-29) found NO Centella or madecassoside source
records — so every efficacy/mechanism sentence (chaotic-collagen dump, hypertrophic
formation, occlusion-vs-structure, soothe-plus-structure, signal interception / parallel
realignment, flat-surface result) renders with the `○ UNSOURCED — no record in this system`
flag, never a citation. VO keeps the user's wording as written. The identity beat compiles
from nominal fields only (INCI Madecassoside · Source Centella asiatica · What it is: one
purified triterpenoid molecule). No citation id appears anywhere in this video — none exists
to cite. Carries the same unsubstantiated-health-claim exposure documented on the two
sibling projects.

## Customizations (translations from the user's literal brief)

- **No Midjourney/Runway assets** — the lane is browser-drawn SVG/CSS/canvas only; every
  visual is authored geometry. Same call as PDRN's declined photographic before/after.
- **One persistent presenter** — a deterministic seeded collagen fiber-field (LCG seed
  20260829, identical across frames 02/03/04/05 so the knot is literally the same object)
  on a persistent dark stage panel: red tangle → labeled scar → aqua blueprint projected
  over it → snap-to-parallel → flat surface → void. The dark stage is promoted from
  hook-only (PDRN grammar) to the standing presenter surface — deliberate, documented here.
- **Descending glowing molecule replaced** by the paper identity uc-card + aqua blueprint
  projection (the lane bans the rotating/floating hero molecule).
- **"Red emergency HUD" translated**: damaged-red #E4574D lives only on the dark stage;
  corner ticks + one uppercase micro-label are the whole HUD; glitch is an audio event
  (glitch-3.mp3); glow is one bounded bloom per beat. "Cica jars + red X" became three
  generic unlabeled jar silhouettes killed by a single coral hairline strike (no brand
  evocation, no red X on a claim surface).
- **Beat 5 snap** reuses PDRN's licensed overshoot: back.out(1.4) + bounded residual
  jiggle that settles — the video's single signature moment.
- **Loop engineering**: beat 7's last frames ghost the beat-1 scar silhouette up behind the
  aqua "?" and the B7 SFX mirrors B1's impact+glitch pairing, so replay lands seamlessly on
  frame zero (which is the fully composed hook — never blank).

## Notes

- Pinned `hyperframes@0.8.19` (current series pin). Scaffolded by hand from sibling
  project structure (centella-tiger-grass), not `hyperframes init`.
- **VO**: Kimberly (voice_id `674b71b8-1d2e-4087-8567-d1f53c0b9f3c`, voice_type `element`)
  via Higgsfield `generate_audio`, model `seed_audio`. All seven takes passed the gate
  first try: duration → silence scan → whisper medium.en transcript-diff → adeclick →
  tail-spike scan. "metacassicide" in the transcript is the known same-way madecassoside
  ASR bias (established on centella-tiger-grass), not a TTS failure; "hypertrophic" and
  "collagen fibers" (the flagged plural-cluster risk) both came through clean. Takes 05/07
  ran speech to the file edge (tail peak −8.7 dB) — given a 40 ms fade + 0.25 s pad before
  installation. `_pre-declick/` holds the raw takes.
- **Timing**: the 60s script runs 43.8s of actual narration at Kimberly's pace — total
  runtime 50.400s with settle tails (S1=0 S2=3.400 S3=12.000 S4=21.300 S5=31.400 S6=39.400
  S7=47.200). Frames were authored directly against the real take lengths and word-level
  whisper timings, so the PDRN inner/outer `data-duration` rescale defect cannot occur —
  nothing was rescaled.
- **Captions**: 25 top-band (y=196) cues, whisper word-timed, each extended to the next
  cue's start. Same visual treatment as pdrn-cellular-science.
- Render via `npm run render` = `--quality high --workers 1` baked into package.json
  (PDRN's static-frame-dedup defect precedent).
