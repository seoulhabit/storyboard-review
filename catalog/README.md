# Component catalog

Everything built today, organized so it can be mixed and matched into videos
instead of re-found by scrolling through file names. Four kinds of thing
live here:

- **`ingredients/`** — substance-specific content: posters and explainers
  about one specific active (PDRN, snail mucin). Swap the ingredient, and you
  need a new one of these.
- **`visual-components/`** — reusable presentation patterns that aren't tied
  to any one ingredient (an evidence meter, a graded-scale badge, a
  split-face diagram, an AM/PM routine layout). Any ingredient can be dropped
  into one of these.
- **`marks/`** — standalone identity/logo exploration: flat vector marks
  (primary pick + alternates), not full posters or explainers. Some are
  ingredient-specific (PDRN, ginseng), one is a generic ingredient study,
  one is a brand-level proposal not tied to any ingredient at all.
- **[`ingredient-photography/`](ingredient-photography/README.md)** — raw
  flat-lay product photography, one still per ingredient, for B-roll and
  thumbnails rather than any single poster or card. Currently the 20-item
  Skincare Ingredient Glossary list, numbered to match it 1:1.

A video is assembled by picking **one ingredient piece + one or more visual
components** — e.g. "PDRN Renewal poster" (ingredient) driving into an
"EvidenceMeter" scene (visual component) that cites `ING-PDRN-S004`.

Open [index.html](index.html) for a browsable gallery of all sixteen (click a
card to load its live preview — they're not auto-loaded so the page doesn't
try to run four GSAP timelines and a WebGL scene at once).

## Shared design rules

A few rules repeat verbatim across the rules-based components (evidence-meter,
graded-scale, split-face-protocol) — worth knowing once rather than
rediscovering per file:

- **No success color.** Celadon/aqua marks "confirmed" at *every* level —
  1-of-5 must not read as failing, 5-of-5 must not read as winning.
- **Deterministic, t-driven clocks.** Every animated component is a paused
  GSAP timeline scrubbed by a single `t` value — no autoplay, no wall-clock,
  any `t` reproduces the same frame. This is what makes them scroll-stop and
  seek safe.
- **Locked to its claim/source.** None of these render standalone in the real
  pipeline — always paired with the claim text and its `ING-*` source chip.
- **"Not wired to build.mjs" / "SPIKE".** Three of the four visual components
  say this explicitly in-page. They're validated visual specs, not yet
  plugged into the real HyperFrames composition pipeline — that wiring is
  the next step before any of them can appear in an actual render.

## Ingredients

| Item | File | Format | Status |
|---|---|---|---|
| [PDRN Renewal](ingredients/pdrn/pdrn-poster-spike.html) | `pdrn-poster-spike.html` | Branded hero poster — 4 steps / 7 benefits, Trinity Medical Aesthetics, Traditional Chinese copy | Spike |
| [PDRN Skin Regeneration](ingredients/pdrn/pdrn-skin-regeneration-spike.html) | `pdrn-skin-regeneration-spike.html` | 3-point mechanism explainer (Barrier Repair / Reduces Inflammation / Boosts Cell Renewal) — not a poster, a different scene format entirely | Spike |
| [Snail Mucin Essence](ingredients/snail-mucin/snail-mucin-poster-spike.html) | `snail-mucin-poster-spike.html` | Same poster template family as PDRN Renewal (5 actives / 4 benefits) applied to a different ingredient | Spike — full video since produced at `../videos/snail-mucin-glass-skin/` |
| [Ginseng](ingredients/ginseng/README.md) | *(linked, not duplicated)* | "Red Ginseng: Two Routes" — oral vs. topical delivery aren't interchangeable, split-screen comparison scene is the thesis | Linked to `../videos/red-ginseng-two-routes/` — rendered (40.1s), no spike file, real project already has a proper home |
| [Retinal vs. Retinol](ingredients/retinal-vs-retinol/README.md) | *(no asset yet)* | "What the Research Actually Compared" — validated script exists, but no poster/spike/video project in this repo | Gap — flagged, not fabricated |
| [Skincare Ingredient Glossary](ingredients/skincare-ingredient-glossary/README.md) | *(linked, not duplicated)* | 76s breadth-first pass — 20 ingredients, AHA/BHA through Vitamin C, one "what it is / best for" card each | Linked to `../videos/skincare-ingredient-glossary/` — already rendered, overlaps 3 ingredients with dedicated entries above without duplicating them |

Reference images: [pdrn-poster-bubbles.png](ingredients/pdrn/pdrn-poster-bubbles.png), [pdrn-poster-helix.png](ingredients/pdrn/pdrn-poster-helix.png) — two visual-motif options reviewed side by side (see `storyboard_pdrn-poster.html` at the repo root).

`pdrn-poster-variation-spike.html` ("PDRN Renewal Codex") has been dropped
from the catalog twice now — once here, once by a separate session that then
re-added it on a mistaken git-history assumption. Recoverable from git
history if it's ever wanted back, but it's not part of the active catalog.

A real HyperFrames project scaffold for PDRN skin regeneration already exists
separately at `../videos/pdrn-skin-regeneration/` — that's the production
side; this folder is the design-reference side.

## Visual components

| Item | File | What it is | Series slot |
|---|---|---|---|
| [EvidenceMeter — Lockup + Design Modes](visual-components/evidence-meter/evidencemeter-spike.html) | `evidencemeter-spike.html` | Flat 2D instrument: hero claim → meter → source footnote, 4-level confidence scale, 5 color-mode options, plus a "design mode" for present/absent attributes | Component 3/5 |
| [EvidenceMeter — Volumetric Monolith](visual-components/evidence-meter/evidencemeter-3d-spike.html) | `evidencemeter-3d-spike.html` | Same component, Three.js 3D take | Component 3/5 (alt) |
| [GradedScale — Strict Enum Badge](visual-components/graded-scale/gradedscale-spike.html) | `gradedscale-spike.html` | 5-node hard-enum badge (integers 1–5 only); `validateGradedScale()` fails loud on anything else | Component 4/5 |
| [SplitFaceProtocol — Clinical Vector Map](visual-components/split-face-protocol/splitfaceprotocol-spike.html) | `splitfaceprotocol-spike.html` | Pure-SVG bilateral study diagram — `#control-arm` / `#active-arm`, independently targetable, no photography | Unnumbered |
| [Dawn to Dusk Skincare](visual-components/dawn-to-dusk-routine/am-pm-skincare-spike.html) | `am-pm-skincare-spike.html` | AM ("Protect", 5 steps) vs PM ("Treat + Replenish", 5 steps) routine checklist | Unnumbered, earlier-stage — no design-law framing or deterministic clock yet |
| [RoutineLadder](visual-components/routine-ladder/routineladder-spike.html) | `routineladder-spike.html` | Six-rung focus ladder, one step at a time in a deterministic-clock 3D depth stack — Cleanse → Toner → Essence-Serum → Ampoule → Moisturiser → SPF | Unnumbered — `catalog.md` Flag 3 guesses this is one of the design system's own unfilled "3/5" series slots (1, 2, or 5) but doesn't confirm which |
| [Celestial Arc](visual-components/celestial-arc/celestial-arc-spike.html) | `celestial-arc-spike.html` | Day/night sky motif — dashed sunrise-to-sunset arc, traveling color-shift dot, pulsing CSS sun, crescent moon + twinkling stars | Unnumbered — extracted from Dawn to Dusk Skincare's hero backdrop so the motif is reusable on its own |

The in-page numbering (3/5, 4/5) is the components' own — slots 1, 2, and 5
don't appear among today's files, so treat that as a hint about a larger
plan rather than a complete series.

## Marks

Standalone identity/logo exploration — a primary pick plus alternates per
folder, generated via Recraft AI (provenance embedded in each SVG's own
C2PA metadata). Not posters, not reusable UI patterns — just marks.

| Item | Files | What it is |
|---|---|---|
| [PDRN Mark](marks/pdrn/README.md) | `pdrn-primary.svg` + 8 alts | Double-helix abstraction, clinical teal with a coral accent strand |
| [Ginseng Mark](marks/ginseng/README.md) | `ginseng-primary.svg` + 3 alts | Abstract root mark matched to a real reference photo — ringed neck, tapering body, root-hair tendrils |
| [Ingredient Mark (generic)](marks/ingredient-generic/README.md) | `ingredient-primary.svg` + 3 alts | Generic study preceding the named marks — leaf/droplet silhouette in jade, not tied to one ingredient |
| [Fold & Spark Brand Mark](marks/brand-education/README.md) | `logo-primary.svg` + 3 alts | Brand-level proposal, not ingredient-specific — angular fan/pages symbol with a spark facet, on deep slate navy |

`Fold & Spark` doesn't appear anywhere else in this repo yet — flagged in
its own README as worth confirming with whoever's driving brand strategy
before the name spreads further.

## Status legend

- **Spike** — a validated, self-contained visual reference. Explicitly
  "not wired to build.mjs": the real HyperFrames composition pipeline
  doesn't consume these yet.
- **Earlier-stage** — a layout sketch without the rules-based framing
  (no design-law callouts, no deterministic clock, no `ING-*` sourcing) the
  other components carry.
- **Linked** — no file lives under `catalog/`; the entry points at a real
  project elsewhere in the repo instead of duplicating it. Used when the
  content already has a proper home (a `videos/` project), unlike a spike
  that was otherwise homeless at the repo root.
- **Gap** — no design asset exists in this repo at all yet. Documented
  honestly rather than backfilled with a placeholder, so it reads as
  "nothing built yet," not "something built badly."
