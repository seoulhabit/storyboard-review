---
workflow: faceless-video-craft
destination: shorts
aspect: 1080x1920
language: en
audience: "Over-exfoliated / damaged-barrier viewers (same cohort as videos/centella-tiger-grass)"
length: 15.0s (rebuild scope — packaging + first 15s, not a full replacement cut)
VO_MODE: silent
angle: viewer-stake reframe
---

## What this is

A scoped rebuild of the **first 15 seconds and the packaging** of `d6DPiORuPO4`
("Why everyone is obsessed with Centella Asiatica right now", 1:12, 13 views at ~50h),
whose source project is `videos/centella-tiger-grass/`. Nothing in that project is
modified — this is a sibling.

**Not a finished publishable Short.** It is the hook/packaging prototype the diagnosis
called for. See *Known gaps* below.

## The diagnosis it answers

Measured, with `cGbokt_B_vE` (1:56, 145 views) and `Yc1hH5Bz4t8` (162 views) as controls:

- The original's first second-person address lands at **~11.9s** (transcript word 33).
  Both controls put the viewer in the first sentence — "Does **your** favorite Korean
  serum…" (word 2) and "**Stop** doing a 10-step routine" (word 1).
- The on-screen question ("WHY TIGERS ROLL IN THIS PLANT.") is never answered on screen;
  the answer is VO-only, so a muted-first viewer gets a nature clip and an open loop.
- Seconds 5–16.35 — the longest scene — are a dictionary card (INGREDIENT IDENTITY /
  CATEGORY / SOURCE) sitting in the highest-value retention window.
- The loop hand-back was deleted in the source project's Round 6; the seam measured
  **58.7**/255 mean delta, worse than that video's own internal hard cuts (44.7).

Failure type is **retention**, not packaging: the original's title scores 95, and its
initial sample was normal (4 views at 2.5h vs a channel median of 2 at 2h) before
flatlining. YouTube tested it and declined to expand.

## Beat sheet (YouTube delivery constraints read first)

Constraints: 1080×1920; state change every 1.5–3s across the *whole* scene; reserved
zones top 192 / bottom 384 / right 162; frame zero is the hook, already composed; payoff
visible by ~2s; last frame hands back to the first; hero type 96–160px, reading ≥40px,
labels ≥32px.

| # | Scene | Window | Intent |
|---|---|---|---|
| 1 | `01-hook` | 0.000–4.200 | Viewer is the subject of frame zero. "YOUR SKIN ISN'T SENSITIVE." reads complete at t=0; the reframe ("IT'S A BROKEN BARRIER.") lands at **1.30s**. |
| 2 | `02-barrier` | 4.200–8.600 | What actually broke. The wall assembles, the acid wash descends, the top course shards away and drops out. One mechanism, no second idea. |
| 3 | `03-fix` | 8.600–15.000 | The lesson-tied action, moved from 0:50 into the first 15s: STOP the acids two weeks / START cica AM+PM. Identity ("cica = centella = tiger grass") arrives compressed to one line as a byproduct, not as an 11.3s lesson. Last 0.95s crosses back to scene 1's own plate and treatment — the engineered loop. |

**Presenter:** type, carried by one diagram. Picked once and not switched mid-way.

## Asset strategy (decided before any markup)

Reused, nothing generated:

- `assets/plates/03-flaking-skin.png` — from `catalog/skin-macro-photography/`. The real
  tactile anchor, in the *first* beat rather than late B-roll.
- `assets/plates/02-centella-asiatica.png` — from `catalog/ingredient-photography/`.
- `assets/bgm/track-soft.mp3` — the channel's own bed, from `videos/centella-tiger-grass/`.

## Component check

`02-barrier` adapts the **mechanism** of `catalog/visual-components/barrier-wall`
(its SVG course geometry and wash/shard choreography), restyled to this project's tokens
and retimed to 4.4s. The catalog entry records that three separate videos each rebuilt
this mechanism from scratch before it was harvested; this is its fourth use and the first
that did not rebuild it. Nothing new here is a general mechanism, so there is no catalog
contribution to make from this project — except the tooling fix below.

**Tooling fix contributed back:** `scripts/check-static-hold.py`'s scene-boundary regex
required a literal `class="scene"` and silently fell back to whole-render mode on the
canonical `class="scene clip"` markup (printing a false-positive warning instead of an
error). Widened to match either. Worth pushing to `catalog/tooling/`.

## Known gaps — this is a prototype, not a publish candidate

1. **No voiceover.** `VO_MODE: silent`, and the reason is scope: the rebuild covers
   packaging + the first 15s, and the approved script's VO takes belong to a 71s cut whose
   wording this rebuild deliberately replaces. Publishing would need new VO for the new
   copy, which re-triggers the whole re-timing cascade.
2. **Seconds 15–71 are untouched.** The original's remaining beats still carry the
   dictionary-card pacing and the deleted loop.
3. **Claim posture inherited, not re-litigated.** The efficacy/mechanism claims come from
   the source project's approved script, which carries no source records for Centella
   (see `videos/centella-tiger-grass/BRIEF.md`). This rebuild renders **no citation chip**
   rather than inventing one, and keeps every on-screen sentence in plain language, but it
   does not resolve the underlying sourcing question — that is domain-truth work.
4. `02-barrier` measures 8.8% active-step share with a 3.50s max gap — over the 3s shorts
   ceiling. The mechanism visibly completes (verified by frame extraction); the metric
   under-reads a small, low-contrast diagram on a large canvas. Noted rather than papered
   over with decorative motion.
