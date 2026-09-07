# Ingredient actor contract

An ingredient actor is the repeatable visual identity of an ingredient. It is neither a product packshot nor scientific proof.

Each actor ships as an editable transparent SVG plus a JSON motion and usage contract. The SVG contains stable, ingredient-prefixed layer IDs so a story format can animate it without redrawing it.

## Required states

- `hero` — full recognition view;
- `compact` — small persistent marker;
- `source` — paired with origin or identity context;
- `formula` — contained inside a vehicle or product context;
- `evidence` — reduced visual presence beside evidence;
- `unknown-version` — desaturated or interrupted when specification is missing;
- `recap` — simplified closing state.

## Host rule

Copy or inline the SVG into the consuming HyperFrames composition when internal layer animation is needed. Prefix any host-created IDs with the scene ID. Use one paused, seek-safe timeline; do not add infinite SVG or CSS animation inside the actor asset.

The actor communicates category recognition only. Claims, evidence, routes, processes, and suitability remain separate governed components.

## Long-form roles

The seven visual states become six editorial jobs in a long-form story:

- `chapter_open` uses `hero` for the full introduction or a meaningful chapter return;
- `continuity_anchor` uses `compact` as a quiet reminder while another visual leads;
- `diagram_node` uses `source` or `formula` inside route, process and format diagrams;
- `evidence_companion` uses `evidence` at reduced hierarchy beside study details;
- `recap_token` uses `recap` as a closing memory callback;
- `unknown_version` uses `unknown-version` when a missing specification must remain visibly unresolved.

Use the full entrance only on the first appearance. Later appearances should use a short match-position return or state resolve. Keep orientation, signature colors and distinguishing endpoints stable across chapters. Never shrink below the actor contract's `minimum_width_px`; switch to its `small_size_mode` before reducing detail further.
