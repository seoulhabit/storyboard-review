# Component catalog

Everything built today, organized so it can be mixed and matched into videos
instead of re-found by scrolling through file names. Two kinds of thing live
here:

- **`ingredients/`** — substance-specific content: posters and explainers
  about one specific active (PDRN, snail mucin). Swap the ingredient, and you
  need a new one of these.
- **`visual-components/`** — reusable presentation patterns that aren't tied
  to any one ingredient (an evidence meter, a graded-scale badge, a
  split-face diagram, an AM/PM routine layout). Any ingredient can be dropped
  into one of these.

A video is assembled by picking **one ingredient piece + one or more visual
components** — e.g. "PDRN Renewal poster" (ingredient) driving into an
"EvidenceMeter" scene (visual component) that cites `ING-PDRN-S004`.

Open [index.html](index.html) for a browsable gallery of all ten (click a
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
| [PDRN Renewal Codex](ingredients/pdrn/pdrn-poster-variation-spike.html) | `pdrn-poster-variation-spike.html` | DNA-helix variation of PDRN Renewal — dark biotech-lab palette, spec-sheet step index (04/07) instead of bubble callouts, Trinity credit pulled back to a quiet line | Spike |
| [PDRN Skin Regeneration](ingredients/pdrn/pdrn-skin-regeneration-spike.html) | `pdrn-skin-regeneration-spike.html` | 3-point mechanism explainer (Barrier Repair / Reduces Inflammation / Boosts Cell Renewal) — not a poster, a different scene format entirely | Spike |
| [Snail Mucin Essence](ingredients/snail-mucin/snail-mucin-poster-spike.html) | `snail-mucin-poster-spike.html` | Same poster template family as PDRN Renewal (5 actives / 4 benefits) applied to a different ingredient | Spike — mid-edit (brand lockup just removed) |

Reference images: [pdrn-poster-bubbles.png](ingredients/pdrn/pdrn-poster-bubbles.png), [pdrn-poster-helix.png](ingredients/pdrn/pdrn-poster-helix.png) — two visual-motif options reviewed side by side (see `storyboard_pdrn-poster.html` at the repo root); `pdrn-poster-spike.html` and `pdrn-poster-variation-spike.html` above are the posters each one fed into.

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

The in-page numbering (3/5, 4/5) is the components' own — slots 1, 2, and 5
don't appear among today's files, so treat that as a hint about a larger
plan rather than a complete series.

## Status legend

- **Spike** — a validated, self-contained visual reference. Explicitly
  "not wired to build.mjs": the real HyperFrames composition pipeline
  doesn't consume these yet.
- **Earlier-stage** — a layout sketch without the rules-based framing
  (no design-law callouts, no deterministic clock, no `ING-*` sourcing) the
  other components carry.
