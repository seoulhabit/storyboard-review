# Storyboard — Pilling vs. Peeling

**Round 4** (2026-09-01, review against the updated authoring skill).
Scene 07's claim was re-scoped to the regulator it cites, and scenes 06 and
07 were re-choreographed after a pixel measurement showed their authored
beats were firing but sub-perceptual. Durations, scene starts and the BGM
are untouched from round 3 — nothing upstream of a beat moved, so the
re-timing cascade did not fire. **Round 3** (direct creator feedback on
round 2's render: "scene 7 feels rushed"). 21.1s, 1080×1920, 30fps,
silent/type-carried. Re-derived from the built `index.html` /
`variants/index-hook-b.html`, not hand-estimated. Two opening variants share
scenes 02–08 verbatim; only scene 01 and its SFX differ.

All 7 scene-to-scene boundaries are hard cuts — no crossfade anywhere in
this project (a crossfade across a ground change produces the muddy
near-blank midpoint the verification loop's transition-midpoint check
exists to catch). Ground does **not** strictly alternate every scene this
round (01→02 are both ink) — a deliberate visual grouping of the two
"evidence" scenes that share a real macro plate on a dark ground, not an
oversight; still every boundary is a hard cut regardless of ground match.

## Scene map

| # | id | start | dur | ground | plate? | layout |
|---|---|---|---|---|---|---|
| 01 | `01-hook-a` / `01-hook-b` | 0.0 | 2.6 | ink / paper | ✔ | A: bordered macro panel + crossfade-in-place hook copy. B: full-bleed compare band (same base plate, drawn crumb overlay on right half) + single headline |
| 02 | `02-residue` | 2.6 | 2.9 | ink | ✔ | caption zone / macro→diagram match-cut media box / chip zone |
| 03 | `03-factors` | 5.5 | 1.9 | paper | — | headline / FactorConverge diagram (3 nodes travel inward on their own connectors) |
| 04 | `04-flaking` | 7.4 | 2.8 | ink | ✔ | headline / macro→diagram match-cut media box (BarrierWall) / qualifier + chip |
| 05 | `05-test` | 10.2 | 3.0 | paper | ✔ | fixed panel, base plate + wipe-mask reveal (same plate both sides), sub-lines, UnsourcedFlag pill |
| 06 | `06-fix-pilling` | 13.2 | 2.6 | ink | — | label row / 3-card row, each card highlighting while its own tip is demoed / SPF sub-line / UnsourcedFlag pill |
| 07 | `07-fix-peeling` | 15.8 | 3.3 | paper | — | header / 3-icon row (two of three actives cut, moisturizer+SPF activate) / severity line / 3-chip row |
| 08 | `08-close` | 19.1 | 2.0 | ink | ✔ (crop, 0.18 opacity bg) | centered takeaway + lockup + reworked CTA, loop-matched to 01 |

Sum: 2.6+2.9+1.9+2.8+3.0+2.6+3.3+2.0 = **21.1s** exactly, matches both
roots' `data-duration` and anchor tween.

## Per-scene notes

**01-hook-a** — Real macro plate (`01-pilling-macro.png`) in a 700×700
bordered panel (avoids the safe-area checker's full-bleed-photo
false-positive risk). Frame zero: plate settled, "Peeling — or product
pilling?" already at rest. t=0.55 a soft press-highlight blooms over the
residue (SFX-synced). t=1.20 the payoff crossfades in over the question's
slot: "Those white flakes may not be your skin." t=1.95 an aqua rule draws
under it.

**01-hook-b** — Teaser split, deliberately unlabeled (no BARE SKIN/AFTER
LAYERING verdict — scene 05 is where that resolves). Same base plate
(`04-base-skin.png`) full-bleed, a drawn crumb overlay on the right half
only, a divider draw + staggered crumb appearance as the only motion.
Headline "Those flakes may be your skincare." settled at rest.

**02-residue** — Plate (`02-layering-hand.png`) zooms gently for 0.85s, then
a hard **match cut** swaps it for the SPF/MOISTURIZER/SERUM cross-section at
the same box, seated on a labelled **SKIN** substrate (round 5) so the stack
reads as depth, not as an application order. Pills detach in a staggered
sequence, drifting **up and out** toward the outer surface (round 5; they
previously fell downward, which reads as rolling *into* the skin once the
substrate is present). Round 6 resized them from r=7-10 specks to r=28-36
balls formed in two seam clusters (~1.15s and ~1.55s) that lift away at
~1.80s and ~2.30s — the caption promises "rolls into balls," and at the old
size there were no balls to see. Chip
(`Skin Res Technol · 2024`) lands at 2.20s — 1.35s after the plate left
screen, never co-resident with it.

**03-factors** — FactorConverge (harvested to
`catalog/visual-components/factor-converge/`; this is its origin scene).
Headline + 3 outer nodes (SKIN / FORMULA / HOW YOU APPLY) settled at frame
zero; connectors draw 0.15–0.90s; center node arrives and pulses at 1.00s;
1.35–1.85s the three factors travel inward along their own connectors — the
convergence payoff, not decoration. No citation chip (recorded decision,
unchanged from round 1 — this is an elaboration of scene 02's same study,
not a new claim).

**04-flaking** — Plate (`03-flaking-skin.png`) zooms 0.90s, a lifted-flake
overlay hints the match target, then a **match cut** to BarrierWall. Wash
descends, three shards detach and drift through 2.40s. Qualifier
("dryness · tightness · redness · stinging") at 2.10s, chip
(`FDA · 21 CFR 333.350`) at 2.45s — 1.55s after the plate left screen.

**05-test** — The signature moment. One fixed 840×900 panel: a base plate
(bare skin) always visible, and a wipe-mask (px-width, not %, so the reveal
tracks the panel exactly) holding the *same* plate plus a drawn residue
overlay. The wipe travels full-width at 0.35–1.05s (revealing "layered"),
then partially retreats to ~40% at 1.75–2.35s, landing on a genuine
side-by-side. Sub-lines "Flakes? → Peeling." / "Crumbs? → Pilling." at
1.30/1.50s. `UnsourcedFlag` pill "A clue — not a diagnosis." at 2.10s. No
citation chip (the heuristic has no tested source).

**06-fix-pilling** — "TRY THIS" + all three cards settled at frame zero.
Each card **highlights** (background and border lift) while its own tip is
being demonstrated, so the motion encodes *which* tip is on: a line-shrink
(thinner passes, 0.10–0.70s), a clock-hand sweep (let it settle,
0.80–1.45s), a double tap + the coral slash pop (round 5: three discrete
taps for *pat*, one continuous stroke for *rub*, the slash sized to the rub
stroke alone — it was previously a full-glyph ✗ with no pat mark at all, which
reads as negating the whole card — this video's
one coral spend, 1.55–2.20s). **Round 4 reworked this.** The glyphs were
56px and the demos animated 12px strokes inside them — ~48px² of change on
a 2,073,600px canvas, measuring 0.0001–0.012 mean |Δluma| per 8fps step:
tweens that fired correctly and that no viewer could see. Glyphs are now
168px and the card highlight carries the beat. Measured after: 5% → 40% of
steps carrying a visible beat, longest quiet run 2.38s → 0.50s. SPF line reworded to "Same total SPF — just thinner passes."
`UnsourcedFlag` pill at 2.20s, explicitly covering the reworded SPF line
too (still untested as an intervention).

**07-fix-peeling** — **Re-scoped round 4.** Through round 3 this scene read
"Pause actives. Moisturize. Protect." under two chips inherited verbatim
from `peeling-not-progress`, neither of which supports pausing an active —
an unsourced instruction to stop an active, which no flag rescues. It now
reads "One active at a time. Moisturize. Protect.", tracking 21 CFR
§333.350(c)(1)(ii), with (c)(3)(ii)'s severity gate rendered beneath it
("Severe burning or swelling? Stop and ask a doctor.") and a third chip
carrying the regulation. The actives column shows three droplets; two dim
and are struck, one survives — the claim rendered literally. See BRIEF.md
§ Source verification for the full correction.

Its cadence was reworked in the same pass. The two "do this" circles were
`--mist` on `--paper` — **~1.08:1**, so the 1.08× scale pulses authored on
them moved 0.02–0.10 mean |Δluma|, i.e. nothing. They now change *state*
(a persisting aqua activation) rather than size, and the cut column takes
an ink veil. Round 3's recorded "8% active steps" for this scene was an
artifact: both qualifying steps were h264 keyframe refreshes (mean 5.2 at a
per-pixel max of 12 — a global quantization shift, not motion), so the
scene in fact had no real beat at all. **Originally retimed round 3**
(2.1s → 3.3s) per direct creator
feedback on round 2's render — independently consistent with round 2's own
cadence measurement, which had already flagged this as the weakest scene
(0 steps clearing the active-step threshold; see `frame.md` § Verification
— Round 2). Same beat order, more room between each: header + all three
icon columns settled at frame zero; actives dims + strikes through at
0.15/0.20s, moisturizer pulse at 0.85s, SPF pulse at 1.20s, two chips
(`Cutis · 2006`, `FDA guidance · 2005`) at 1.65/2.05s — each now holds on
screen for 1.35s before the cut (was 0.75s). A slow bounded scale-pulse on
the headline at 2.5–3.1s carries the scene's continuous motion through the
extra hold time so it doesn't read as a static freeze.

**08-close** — Loop-locked, so its own motion budget is intentionally
small. A low-opacity (0.18) crop of the hook's own plate sits inset within
the safe content box (not full-bleed — a full-bleed photographic backdrop
reliably fails the safe-area gate even at low opacity) as a slow-zooming
backdrop, doubling as the cadence carrier and the loop hand-back. Takeaway
("BARE SKIN → PEELING" / "AFTER LAYERING → PILLING") settled at frame
zero — this is the loop endpoint, same frame-zero discipline as scene 01's
hero. Lockup pops at 0.55s, CTA "Save this test for your next skincare
routine." at 1.15s, takeaway drifts up 8px at 1.45–2.00s into the exact
position scene 01 opens on.

## What changed from round 1, structurally

- 9 scenes → 8. Old `02-split` (neutral word-card bisector) dropped — its
  setup/payoff role is now played directly by scene 05's wipe. Old
  `04-factors` kept its own scene rather than being absorbed elsewhere.
- Every scene gained either a real macro plate, a match cut, a moving
  wipe, or per-element demoed motion — round 1 measured only 6% of 8fps
  steps carrying meaningful visual change (three scenes internally frozen
  after their entrance); round 2 measures ~11%, with no scene fully frozen
  for its own duration.
- `assets/tokens/tokens.css`'s values are now inlined directly into each
  scene's `#root` (a `<link>` to the external file did not reliably resolve
  custom properties in the render pipeline — confirmed via direct
  measurement, not assumed) rather than copy-pasted ad hoc per scene as in
  round 1.
