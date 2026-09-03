# MoleculeStates

One molecule drawn in **three physical states**, side by side, so the difference
between them is carried by geometry rather than by a caption.

- **`moleculestates-spike.html`** — the three states as static SVG, on the house
  paper ground with the aqua accent on one lane.

| State | Drawn as | Reads as |
|---|---|---|
| free chains | long loose coils, dispersed, water dots caught in the loops | the version already in the body |
| two sizes at a boundary | large coils above a dashed line, small ones crossing below | the version in a topical serum |
| cross-linked lattice | the same chains rigidly netted into a shape-holding 3-D grid | the version in an injectable filler |

## Why this exists

Harvested from `videos/hyaluronic-acid-vs-filler` (2026-09-03), whose entire
argument is that three things sharing one name do different jobs. A label can
assert that; only the geometry can *show* it. The three lanes are the video's
`[S6/A-9]` actor map — the same actors persist from the opening lineup, through
one scene each, to the closing badge payoff, and are rearranged rather than
redrawn (`continuity-audit.py`: **0 rebuilt-actor pairs** across 14 scenes).

Generic enough to port: any ingredient whose behaviour changes with **molecular
size, cross-linking, or where it is placed** can use the same three-lane frame —
swap the geometry, keep the structure. Peptides, silicones and polymer thickeners
are the obvious next candidates.

## Control: **none** (static plate)

Deliberately. There is no runtime randomness, no clock, no autoplay and no
self-running CSS animation, so it drops straight into a seeked composition
without violating determinism. **Animate it from the host scene's own paused
timeline**; do not add motion to this file.

Coordinates come from a seeded PRNG in the *generator*
(`random.Random(11 / 23 / 37)` in the source project's `build_actors.py`), never
from `Math.random` at runtime. Re-running the generator reproduces these exact
paths.

## Two things to carry with it

1. **Scaling it inside a padded stage moves the padded edge outward.** On
   1920×1080 a 1.03 stage scale shifts the edge 28.8px per side; that put **207
   frames** of ink inside the reserved left zone before the padding was budgeted
   for the transform. Give a drifting stage `safe + 60px`, and anchor any `scale`
   entrance with `transform-origin: left center` so the left edge cannot move.
   `tokens.css` ships `--safe-*-zoomed` calc tokens for the same trap.
2. **A `clipPath` reveal is invisible to `hyperframes check`'s motion pass**,
   which samples bounding-box geometry. A run of consecutive wipes reads as
   frozen (measured: 9.03s). Pair every reveal with a short travel on the same
   element — vertical, so it never approaches a side zone.

## Status

**SPIKE** — shipped once, in one project. The three-lane frame and the
determinism contract are the reusable parts; the specific chain geometry is
hyaluronic-acid-shaped and will want redrawing per ingredient.

See [../../README.md](../../README.md) for the full catalog.
