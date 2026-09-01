# Storyboard — Pilling vs. Peeling

**Round 2** (2026-09-01 creator-feedback recut). 19.9s, 1080×1920, 30fps,
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
| 06 | `06-fix-pilling` | 13.2 | 2.6 | ink | — | label row / 3-card row, each card demoing its own tip / SPF sub-line / UnsourcedFlag pill |
| 07 | `07-fix-peeling` | 15.8 | 2.1 | paper | — | header / 3-icon row (actives switch-off, moisturizer+SPF pulse) / 2-chip row |
| 08 | `08-close` | 17.9 | 2.0 | ink | ✔ (crop, 0.18 opacity bg) | centered takeaway + lockup + reworked CTA, loop-matched to 01 |

Sum: 2.6+2.9+1.9+2.8+3.0+2.6+2.1+2.0 = **19.9s** exactly, matches both
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
a hard **match cut** swaps it for the 3-band SPF/MOISTURIZER/SERUM diagram
at the same box. Pills detach in a staggered sequence through 2.55s. Chip
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

**06-fix-pilling** — "TRY THIS" + all three cards settled at frame zero;
each demo *is* its own card's entrance: a line-shrink (thinner passes,
0.10–0.60s), a clock-hand sweep (let it settle, 0.75–1.30s), a double tap +
the coral ✗ pop (pat don't rub — this video's one coral spend,
1.35–1.90s). SPF line reworded to "Same total SPF — just thinner passes."
`UnsourcedFlag` pill at 2.20s, explicitly covering the reworded SPF line
too (still untested as an intervention).

**07-fix-peeling** — Densest scene per second. Header + all three icon
columns settled at frame zero; actives dims + strikes through at 0.10s,
moisturizer/SPF pulse at 0.55/0.75s, two chips (`Cutis · 2006`,
`FDA guidance · 2005`) at 1.10/1.35s.

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
