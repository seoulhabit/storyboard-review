# Catalog V2

Catalog V2 is the reusable ingredient layer for SeoulHabit videos. Its first ingredient family is **Centella / Cica**, **Snail Mucin**, **PDRN**, and **Collagen**, harvested from work that already exists. The original `catalog/` remains untouched while V2 proves its structure.

Catalog V2 now also contains **story systems**: reusable teaching components that consume ingredient packs without owning their facts, hooks, or complete storyboards. The first system is Label Literacy, harvested from `kbeauty-label-trap`.

The second system is **Ingredient Fate**, harvested from `collagen-where-did-it-go`. It separates identity, form, route, physical destination and structural effect before evidence or recommendations are introduced.

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
    _shared/
      README.md
    ingredient-actors-preview.html
    centella-cica/
      pack.json
      manifest.json
      identity-card.svg
      components/
        ingredient-actor.svg
        ingredient-actor.json
      assets/
    snail-mucin/
      pack.json
      manifest.json
      identity-card.svg
      components/
        ingredient-actor.svg
        ingredient-actor.json
      assets/
    pdrn/
      pack.json
      manifest.json
      identity-card.svg
      components/
        ingredient-actor.svg
        ingredient-actor.json
      assets/
    collagen/
      pack.json
      manifest.json
      identity-card.svg
      components/
        ingredient-actor.svg
        ingredient-actor.json
        identity-format-map.svg
  story-systems/
    label-literacy/
      label-review.schema.json
      registry.json
      components/
        ingredient-hero-actor/
        label-compare-stage/
        five-question-progress/
        ingredient-order-map/
        ingredient-identity-map/
        source-process-version-map/
        formula-vehicle-journey/
        evidence-distance-map/
        boundary-suitability-card/
      patterns/
        verdict-reveal/
        five-question-recap/
      examples/
        snail-mucin.json
        pdrn.json
    ingredient-fate/
      registry.json
      kit-preview.html
      components/
        format-vessel-pair/
        route-fork/
        structure-scaffold/
        skin-entry-gate/
        surface-vs-structure/
      examples/
        collagen.json
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

## Ingredient actors

Open `ingredients/ingredient-actors-preview.html` to rehearse the first actor family inside a real 16:9 long-form frame. The review surface covers six editorial roles: chapter open, continuity anchor, diagram node, evidence companion, recap token, and unknown-version boundary. It also exposes scale, placement, entry timing, label policy, light/dark contrast, and a sample appearance map.

Each actor is a transparent SVG with stable layer IDs plus a JSON motion and usage contract. Version 1.1 of that contract includes long-form recurrence and minimum-recognition rules. Story systems consume these actors; they should not redraw ingredient substitutes inside individual scenes. The actors communicate recognition, not efficacy or proof.

Story systems may assemble ingredient data into a teaching view, but they do not turn uncertainty into a score or invent missing label details.

## Pilot status

- Centella / Cica: reusable actor, botanical source asset, and identity card are ready; the pack remains draft until evidence records are reviewed.
- Snail Mucin: ready for use across formats, now with a standalone ingredient actor.
- PDRN: ready for identity, topical product, route separation, and scoped evidence stories, now with the harvested short-fragment actor extracted as a standalone asset.
- Collagen: draft visual-ready pack with a dimensional fibre actor, identity card, form map and traceable evidence boundaries; photographic media and real-product label fixtures remain gaps.
- K-Beauty Label Trap: complete nine-component, two-pattern prototype kit covering all 14 source scenes; the four governed ingredient packs now provide the first reusable actor family. Components require real-label and narration-timed stress testing before approval.
- Ingredient Fate: first five-component prototype slice covering neutral vessels, route separation, structural state, skin entry and surface-versus-structure; the oral-distribution and evidence modules are planned next.
