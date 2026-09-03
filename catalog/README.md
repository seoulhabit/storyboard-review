# Component catalog

Everything built today, organized so it can be mixed and matched into videos
instead of re-found by scrolling through file names. Five kinds of thing
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
- **[`product-photography/`](product-photography/README.md)** — fictional,
  unbranded K-beauty *packaging* photography (bottles, jars, tubes,
  texture macros) rather than ingredients — 12 scenes for thumbnails,
  channel art, B-roll, and Shorts Studio inputs. Per-asset provenance and
  verification results live in [`manifest.json`](manifest.json).
- **[`skin-macro-photography/`](skin-macro-photography/README.md)** — real-
  looking (model-generated) macro skin/hand photography for tactile-proof
  beats: pilling residue, layered product texture, flaking skin, bare
  comparison skin. Harvested from `pilling-vs-peeling`'s 2026-09-01 recut,
  currently 4 stills.
- **[`tooling/`](tooling/README.md)** — shared verification scripts, not
  imagery or components. Currently two entries: a rendered-pixel safe-area
  scanner harvested from `peeling-not-progress`'s round-6 fix, and a
  static-hold (frozen-content) scanner from `peeling-question-open` —
  both worth reusing the same way a proven component is.

A video is assembled by picking **one ingredient piece + one or more visual
components** — e.g. "PDRN Renewal poster" (ingredient) driving into an
"EvidenceMeter" scene (visual component) that cites `ING-PDRN-S004`.

Open [index.html](index.html) for a browsable gallery — redesigned 2026-08-30
to stop treating every entry as an image. Cards are grouped by **kind**
(component / static composition / mark / photography / linked / tooling) and,
for components specifically, by **control** — `⏱ clock` (deterministic,
seekable, safe for a real render), `◧ select` (a discrete prop, no time
axis), or `⚠ none` (no scrub interface yet, or — flagged per-card — running
on its own autoplaying clock and *not* render-safe, like Celestial Arc's
CSS `@keyframes`). Every clock/select component shows its duration and a
short field contract on the card face, before you load anything — the point
of harvesting a component is knowing what you can pass it without reading
its source. Loading a `debug`-gated clock component auto-appends `?debug=1`
so its scrubber is visible immediately, not just to whoever already knew
that flag existed. Photography (37 stills across the two photo catalogs)
renders as real inline thumbnails, not a "load preview" button, since
there's no timeline to scrub. Cards aren't auto-loaded on page open so the
page doesn't try to run several GSAP timelines and a WebGL scene at once.

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
| [The 1% K-Beauty Secret](ingredients/one-percent-line/README.md) | *(linked, not duplicated)* | Label-literacy explainer, not a single-ingredient piece — the extract-dilution loophole, the legal 1%-ordering rule, a live Beauty of Joseon teardown, a Hanbang INCI cheat sheet (reuses the Ginseng/Snail Mucin/Mugwort stills below rather than generating new ones) | Linked to `../videos/kbeauty-one-percent-line/` — rendered, in review (round 1/3 with the creator) |

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
| [TermDefinition](visual-components/term-definition/termdefinition-spike.html) | `termdefinition-spike.html` | Full-frame hero card — icon, name (+ optional Korean), category, definition, "commonly used for" line, cycling through a data array with a shared progress rail | Unnumbered — the design system's own name, harvested from **five** independent shipped reimplementations (the four `skincare-glossary-part-*` videos + `skincare-ingredient-glossary`), none of which knew about the others |
| [MoleculeStates](visual-components/molecule-states/moleculestates-spike.html) | `moleculestates-spike.html` | One molecule in **three physical states**, side by side, so the difference is carried by geometry rather than a caption — free chains (in the body), two sizes meeting a dashed boundary (in a serum), a cross-linked lattice (in a filler). A **static plate by design**: geometry is baked to SVG from a seeded PRNG in the generator, so there is no `Math.random`, no wall-clock, no autoplay, and it drops into a seeked composition safely — the host scene's paused timeline animates it. Carries two hard-won notes: scaling it inside a padded stage maps the padded edge *outward* (207 frames of ink in a reserved zone before the pad was budgeted), and a `clipPath` reveal is invisible to `hyperframes check`'s motion pass. | Unnumbered — harvested from `hyaluronic-acid-vs-filler`, whose three-identity argument *is* this component. The three lanes are that video's `[S6/A-9]` actor map: the same actors persist across 14 scenes and are rearranged rather than redrawn (`continuity-audit.py`: 0 rebuilt-actor pairs). Portable to any ingredient whose behaviour changes with **size, cross-linking, or placement** — peptides, silicones and polymer thickeners are the obvious next candidates |
| [DialogueLanes](visual-components/dialogue-lanes/dialoguelanes-spike.html) | `dialoguelanes-spike.html` | Two named speakers in dialogue, rendered **faceless** — no avatar, no portrait, no glyph standing in for a person. Identity is carried by which lane a card lands in, its colour and weight, and a distinct entrance per speaker (`arrive` vs `slam`, different eases). Cards are PANELS, not lines of type: on a 1920-wide frame a text fade moves ~0.7% of the pixels and a card moves 15–30%. The stack is anchored with `yPercent` — resolved against each card's own height — so it needs no measurement and cannot go stale when a line is reworded. Ink-ground variants included, each ratio re-measured against the new ground. | Unnumbered — confirmed catalog gap: a discovery pass before the build found **no two-speaker treatment of any kind** in the repo, no character sheet, no speaker-attribution component, and no prior video with named speakers. `SplitCompare` and `SplitFaceProtocol` are two-*thing* bisectors, not two *voices*. Harvested from `collagen-where-did-it-go` (41 turns across 5 scenes); wired into a real render pipeline, not spike-only |
| [ThresholdList](visual-components/threshold-list/thresholdlist-spike.html) | `thresholdlist-spike.html` | Ranked list split by a cutoff line — a "rule slam" lands at the threshold, below-cutoff rows desaturate and scramble to visualize "order stops meaning anything here" | Unnumbered — generalized from `kbeauty-one-percent-line`'s "1% Line" scene into a reusable above/below-cutoff mechanism |
| [SplitCompare](visual-components/split-compare/splitcompare-spike.html) | `splitcompare-spike.html` | Vertical bisector, two independently-targetable fields, tint flood on the interrogated side only — no success color, never both fields floods at once | Unnumbered — generalized from `centella-cica-vs-snail-mucin`'s closing verdict split; mechanism adapted from `SplitFaceProtocol` with the clinical/facial skin dropped |
| [BarrierWall](visual-components/barrier-wall/barrierwall-spike.html) | `barrierwall-spike.html` | Pure-SVG brick-course wall; an acid-wash rect descends and three shards detach/drift as the top course dims — the skin barrier "breaking apart" | Unnumbered — this is the **third** independent build of this mechanism found in this repo (`betaine-salicylate-gentle-bha`'s SVG original, `ceramides-barrier-diagnostic`'s CSS-grid variant, then `peeling-not-progress`'s adaptation); harvested here so a fourth video doesn't rebuild it again |
| [UnsourcedFlag](visual-components/unsourced-flag/unsourcedflag-spike.html) | `unsourcedflag-spike.html` | Ink-toned pill badge disclosing authored/usage guidance with no record in the source system — deliberately never coral, never citation-pill typography, so it can't be mistaken for a real source | Unnumbered — the *concept* independently recurs across **six** shipped videos (`pdrn-cellular-science`, `madecassoside-flat-matrix`, `centella-tiger-grass`, `retinal-clinical-dossier`, `mugwort-healing-herb`, `red-ginseng-glass-glow` before it was replaced with a real citation), but only `mugwort-healing-herb` (round 3.1) resolved the *treatment* past bare unstyled text — this harvests that fixed version as the recommended shared shape, not a description of an existing consensus |
| [FrostedPanel](visual-components/frosted-panel/frostedpanel-spike.html) | `frostedpanel-spike.html` | Translucent `backdrop-filter` glass card + an optional counter-translated peeling-film overlay (clip boundary and sheet move opposite directions so the sheet reads as stationary while it's "eaten away") | Unnumbered — the **second** independent implementation of the frosted-panel primitive in this repo (after `centella-tiger-grass`), harvested from `peeling-question-open` before a third rebuild happened; render-safety (a GPU-dependent CSS property) confirmed on two independent shipped projects now |
| [StatReveal](visual-components/stat-reveal/statreveal-spike.html) | `statreveal-spike.html` | Single-statistic hero beat — numeral counts up (seek-safe, driven by tween progress via `onUpdate`), plain-language qualifier, human-readable citation chip, and a 100-unit tick-grid pictogram (never chart grammar) showing the same fraction as discrete units | Unnumbered — confirmed catalog gap: a discovery pass found no stat/percent/count-up component anywhere in this directory despite several prior videos (`kbeauty-one-percent-line`, `ceramides-barrier-diagnostic`, `hyaluronic-acid-serum`, others) each building one from scratch; harvested from `pilling-not-dead-skin` after its own implementation was fixed for a real layout-overlap defect and fully post-render-verified |
| [QuestionGate](visual-components/question-gate/README.md) | *(documented; lives in `../videos/exosome-label-decode/compositions/frames/04-questions.html`)* | Ordered checklist of independent questions a viewer applies in sequence — N numbered cards, each activating as its question is asked, with optional second sub-beats inside a card when the narration splits that question into two clauses; answered cards step back via border only, no success colour | Unnumbered — confirmed catalog gap: a discovery pass before the build checked `FactorConverge` (many-to-one convergence), `ThresholdList` (cutoff ranking) and `SplitCompare` (two-thing bisector) and none carries the distinguishing property, **per-item activation state over time**. First entry here harvested from a scene that shipped and was post-render verified rather than from a standalone spike |
| [FactorConverge](visual-components/factor-converge/factorconverge-spike.html) | `factorconverge-spike.html` | Several-inputs-converge-on-one-node diagram — 3 outer nodes each draw a connector line inward to a center node, which pulses once all three land; no node reads as more important than another | Unnumbered — confirmed catalog gap: a discovery pass across every existing component before build found nothing matching this shape (a many-to-one causal diagram, distinct from a comparison or a ranked list); harvested from `pilling-vs-peeling`'s SKIN/FORMULA/APPLICATION beat, fixed to exactly 3 nodes (a real N-node variant this spike doesn't build) |
| [MaterialTriptych](visual-components/material-triptych/materialtriptych-spike.html) | `materialtriptych-spike.html` | N parallel materials (2–4) side by side, joined by a celadon rail that draws across all of them — then an ink bar strikes across and the rail dims. The subject is the *relationship being withdrawn*, not the items: use it when several things share a name but not the evidence behind it. 9:16 canvas with safe-area padding baked in; scrubber loads pre-applied | Unnumbered — confirmed catalog gap: a discovery pass before build found **no N-way comparison of any kind** here. `SplitCompare` and `SplitFaceProtocol` are two-thing bisectors; `ThresholdList` is a cutoff ranking; `FactorConverge` is 3-node but converges on a shared outcome, which would have asserted the *opposite* of this claim. Harvested from `exosome-label-problem`'s "one word, three materials" scene |

The in-page numbering (3/5, 4/5) is the components' own — slots 1, 2, and 5
don't appear among today's files, so treat that as a hint about a larger
plan rather than a complete series. `TermDefinition` and `ThresholdList` are
outside that numbering; see each entry's own README for provenance.

**Considered and not harvested, 2026-08-30 review** — checked against the
same bar the two entries above cleared, and didn't:
- `.cta-chip` (`kbeauty-one-percent-line/08-cta-endcard.html`) — a labeled
  pill, optionally with a thumbnail image (`cta-chip-hb` variant, "X = Y"
  equivalence text). Already an established design-system-level pattern
  (pill chips, `--r-pill`) rather than a distinct component with its own
  choreography — see `seoulhabit-launch/frame.md`'s own notes on this.
- `.trick-fan-chip` (`kbeauty-one-percent-line/05-the-trick.html`) — a fanned
  cluster of ingredient-name chips. Single use, lower generality than
  ThresholdList's mechanism; not harvested this pass.
- `.htu-word` (`snail-mucin-truth/05-how-to-use.html`) — word-by-word kinetic
  type reveal. Already documented as a general motion technique ("type as
  the performer") rather than a discrete component with its own state/data
  contract — nothing to harvest beyond what's already written down.
- The `hook-bottle-*` SVGs (`kbeauty-one-percent-line/01-hook.html`) — a
  decorative dropper-bottle icon, not a data-driven component. Closer to
  `marks/` than `visual-components/`; not harvested.

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

## Verification tooling

Not imagery or a design component — a shared script, catalogued for the
same reason a component is: built once for a real project, worth finding
before the next project rebuilds the same check from scratch. Full
provenance and field contract in [`tooling/README.md`](tooling/README.md).

| Item | File | What it is |
|---|---|---|
| [check-safe-area.py](tooling/check-safe-area.py) | `check-safe-area.py` | The one **hard gate** here: scans a rendered MP4 for content inside the platform's reserved UI zones on transformed, rendered pixels — catches an overshoot a source-level "are the tokens consumed" audit can't see. Portrait by default, `--landscape` for the 16:9 zones, and it refuses to run on a canvas it wasn't configured for rather than failing open. Its page-ground estimator reads the border ring as a *set* of grounds, not one median, so a transition frame showing two scenes at once no longer reports a flat scene background as 100% ink. Harvested from `peeling-not-progress`'s round-6 safe-area fix; the multi-ground estimator came from `ectoin-survival-molecule`, where it flagged 70 clean wipe frames. |
| [check-static-hold.py](tooling/check-static-hold.py) | `check-static-hold.py` | Scans a rendered MP4 for a static-hold whole-frame AND region-aware (a scene's own hero element going empty while unrelated motion elsewhere keeps the whole-frame check clean). Harvested from `peeling-question-open`'s QC-verification round after that project's own copy was found still carrying a sibling project's caption-band crop — see `tooling/README.md` for the recurring-defect history this entry exists to break. |
| [check-cadence.py](tooling/check-cadence.py) | `check-cadence.py` | Scans a rendered MP4 for *perceptible* motion, which is a different question from "is anything frozen?" — a step counts as a beat only if its mean absolute luma delta **and** its per-pixel max both clear a floor, so an h264 keyframe refresh (large mean, tiny max) can no longer be counted as animation. Reports the per-scene longest quiet run and the whole-video active-step share; advisory, exits 0. Harvested from `pilling-vs-peeling` via `ectoin-survival-molecule`, whose docstring had drifted to cite a scene that only existed in the first project. |
| [continuity-audit.py](tooling/continuity-audit.py) | `continuity-audit.py` | Source-level, no render: counts what makes a long-form piece one continuous space rather than a stack of slides — boundaries by type and whether the ground changes across each, entrance-signature shares including eases *inherited* from `defaults:{ease}`, diagrams rebuilt in consecutive scenes, and camera moves. Written after `ectoin-survival-molecule` passed every existing gate and still read as an animated presentation (28/28 hard cuts, 65 % of tweens on one inherited ease, 0 camera moves). Advisory; `--gate` exits 2 on one rule only, a plain crossfade across a ground change. |

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
