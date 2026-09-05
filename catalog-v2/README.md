# Catalog V2

Catalog V2 is the reusable ingredient layer for SeoulHabit videos. It begins with **Snail Mucin** and **PDRN**, harvested from work that already exists. The original `catalog/` remains untouched while V2 proves its structure.

Catalog V2 now also contains **story systems**: reusable teaching components that consume ingredient packs without owning their facts, hooks, or complete storyboards. The first system is Label Literacy, harvested from `kbeauty-label-trap`.

## Governing idea

**Harvest first. Generate only after the inventory proves a real gap.**

An ingredient pack owns stable ingredient information and reusable visual actors. A story format owns the hook, pacing, edit, typography, and CTA. This allows the same ingredient to appear in multiple formats without rebuilding its evidence or making every video look identical.

## Structure

```text
catalog-v2/
  governance/
    ingredient-pack.schema.json
    format-contract.json
  ingredients/
    snail-mucin/
      pack.json
      manifest.json
      identity-card.svg
      assets/
    pdrn/
      pack.json
      manifest.json
      identity-card.svg
      assets/
  story-systems/
    label-literacy/
      label-review.schema.json
      registry.json
      components/
        label-compare-stage/
        ingredient-order-map/
        ingredient-identity-map/
        formula-vehicle-journey/
        evidence-distance-map/
        boundary-suitability-card/
      examples/
        snail-mucin.json
        pdrn.json
  HARVEST-LOG.md
  registry.json
```

## Asset statuses

- `approved` — production-safe for the uses listed in the pack.
- `restricted` — usable only when its limitation or attribution is visible.
- `reference_only` — useful direction, but not a production asset.
- `quarantined` — do not use until a source, rights, or design problem is resolved.
- `planned` — confirmed gap, not yet built.

## Harvest gate

Before generating anything new:

1. Search `catalog-v2/registry.json` and the ingredient `manifest.json`.
2. Check the existing `catalog/` and only the relevant finished video folders.
3. Record every candidate in `HARVEST-LOG.md`, including rejected candidates.
4. Generate only when no approved asset fits and the requested visual is likely to recur.
5. Prefer promoting a gap after two separate stories request it.

Story systems follow the same rule: harvest information architecture and proven behaviors first. Source-video artwork remains reference-only until the component is redrawn, stress-tested, and explicitly approved.

## What V2 does not contain

- full storyboards;
- finished video renders;
- voiceover, music, or one-off transitions;
- branded product images presented as generic ingredients;
- unsourced benefit counts;
- automatically interchangeable label terms.

Story systems may assemble ingredient data into a teaching view, but they do not turn uncertainty into a score or invent missing label details.

## Pilot status

- Snail Mucin: ready for use across formats.
- PDRN: ready for identity, topical product, route separation, and scoped evidence stories. Route-comparison is the highest-priority missing component.
- Label Literacy: six-component prototype kit created from `kbeauty-label-trap`; Centella/Cica demonstrates the source story and Snail Mucin/PDRN test reuse. Components require real-label and narration-timed stress testing before approval.
