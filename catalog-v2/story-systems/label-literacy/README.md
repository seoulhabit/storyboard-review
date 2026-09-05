# K-Beauty Label Trap component system

This system turns governed ingredient-pack data into repeatable label-reading visuals. It owns the visual explanation; ingredient packs remain the factual source.

## Status

Version: `0.3.0`

Stage: complete source-story prototype kit
Harvest source: `videos/kbeauty-label-trap`

No visual from the source video is automatically production-approved. The source scenes are treated as behavior and information-architecture references.

## Component kit

Open `kit-preview.html` to review all nine components and two assembly patterns in one interface.

`components/label-compare-stage/preview.html` now implements an ingredient-anchored A/B comparison:

- two neutral, replaceable product specimens;
- a paired front-claim to exact-label reveal;
- explicit known, unknown, and not-established states;
- a persistent ingredient actor between the products;
- Snail Mucin and PDRN fixtures;
- 16:9 and narrow-screen layouts;
- keyboard focus and reduced-motion support.

Open the preview and switch among the Centella/Cica source-story demonstration and the governed Snail Mucin and PDRN fixtures. The preview does not represent a real commercial product and does not invent a percentage or ingredient list.

## System components

| Component | Status | Purpose |
|---|---|---|
| Ingredient Hero Actor | prototype | Keep the ingredient recognizable across every story context |
| Ingredient-on-Label Compare | prototype | Compare two packaging claims around one ingredient and reveal exact label evidence |
| Five-Question Progress | prototype | Carry quantity, identity, vehicle, evidence, and boundary through the story |
| Ingredient Order Map | prototype | Explain ingredient rank without implying exact concentration |
| Ingredient Identity Map | prototype | Separate consumer name, exact declaration, and studied-material match |
| Source, Process and Version Map | prototype | Separate origin, transformation, and the preparation that reaches a formula |
| Formula Vehicle Journey | prototype | Show an ingredient inside the complete formula |
| Evidence Distance Map | prototype | Show the distance between a study and a finished-product claim |
| Boundary and Suitability Card | prototype | Express practical and evidence boundaries |

## Assembly patterns

| Pattern | Status | Purpose |
|---|---|---|
| Ingredient Verdict Reveal | prototype | Return to the opening A/B labels after all five questions without declaring a universal winner |
| Five-Question Recap | prototype | Compress the five answers into the closing memory aid and vertical short |

Components own reusable behavior. Patterns arrange components for specific story beats. Hook copy, scene timing, narration, and the final brand landing remain story-owned.

## Rules

1. Render missing information as missing; never manufacture label facts.
2. A front claim and an exact ingredient declaration are different fields.
3. Medical-route evidence cannot silently support a topical product.
4. Evidence strength is described through provenance and distance, not a numerical score.
5. Story timing, hook, CTA, and transitions stay outside this system.

## Data

- `label-review.schema.json` defines the reusable input.
- `evidence-distance.schema.json` defines study-to-product mapping.
- `system-tokens.css` defines the shared visual language and responsive baseline for new components.
- `examples/centella-label-demo.json` is the declared fictional source-story fixture; `examples/snail-mucin.json` and `examples/pdrn.json` are governed pack fixtures.
- `registry.json` records component maturity and harvest provenance.
- `source-map.md` records what was harvested and what remains story-specific.

## Next gate

The source story is fully covered, but the kit moves from `prototype` to `approved` component by component only after:

- real-label stress testing with a photographed product;
- 16:9 and 9:16 rendered-frame review;
- long-INCI overflow review;
- light and dark background review;
- animation timing review at actual narration speed.
