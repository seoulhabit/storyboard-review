# Label Literacy story system

This system turns governed ingredient-pack data into repeatable label-reading visuals. It owns the visual explanation; ingredient packs remain the factual source.

## Status

Version: `0.1.0`  
Stage: first working prototype  
Harvest source: `videos/kbeauty-label-trap`

No visual from the source video is automatically production-approved. The source scenes are treated as behavior and information-architecture references.

## First component

`components/label-compare-stage/preview.html` implements the first reusable component:

- approved package media from the ingredient pack;
- a front-claim to exact-label reveal;
- explicit known, unknown, and not-established states;
- a five-question inspection rail;
- Snail Mucin and PDRN fixtures;
- 16:9 and narrow-screen layouts;
- keyboard focus and reduced-motion support.

Open the preview and switch between the two fixtures. The preview does not represent a real commercial product and does not invent a percentage or ingredient list.

## System components

| Component | Status | Purpose |
|---|---|---|
| Label Compare Stage | prototype | Connect packaging claims to exact label evidence and unknowns |
| Ingredient Order Map | planned | Explain ingredient rank without implying exact concentration |
| Ingredient Identity Map | planned | Separate consumer name, INCI, source, process, and material specification |
| Formula Vehicle Journey | planned | Show an ingredient inside the complete formula |
| Evidence Distance Map | planned | Show the distance between a study and a finished-product claim |
| Boundary and Suitability Card | planned | Express practical and evidence boundaries |

## Rules

1. Render missing information as missing; never manufacture label facts.
2. A front claim and an exact ingredient declaration are different fields.
3. Medical-route evidence cannot silently support a topical product.
4. Evidence strength is described through provenance and distance, not a numerical score.
5. Story timing, hook, CTA, and transitions stay outside this system.

## Data

- `label-review.schema.json` defines the reusable input.
- `examples/snail-mucin.json` and `examples/pdrn.json` are governed test fixtures.
- `registry.json` records component maturity and harvest provenance.
- `source-map.md` records what was harvested and what remains story-specific.

## Next gate

The Label Compare Stage can move from `prototype` to `approved` only after:

- real-label stress testing with a photographed product;
- 16:9 and 9:16 rendered-frame review;
- long-INCI overflow review;
- light and dark background review;
- animation timing review at actual narration speed.
