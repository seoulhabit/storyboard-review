# Ingredient Photography (flat-lay set)

Twenty individual product-photography stills, one per ingredient in the
[Skincare Ingredient Glossary](../ingredients/skincare-ingredient-glossary/README.md)'s
20-item list — same names, same order, same numbering as that project's
`components/NN-*.html`, so each file matches its glossary card 1:1.

Generated via Higgsfield (`marketing_studio_image` model), 2048×2048 PNG,
each carrying its Higgsfield job ID in an embedded `hf-job-id` text chunk.
Styled to match a user-supplied reference photo of 7 sample ingredients
(glass-dish actives + whole botanicals on cream seamless paper); these 20
extend that same look to the full glossary list. No text is baked into the
images — labels are left to whatever composition uses them, consistent
with how the rest of this repo renders type as real DOM/SVG text rather
than raster.

## The set

| # | Ingredient | File | Depicted as |
|---|---|---|---|
| 1 | AHA/BHA | `01-aha-bha.png` | glass dish of clear exfoliating liquid, willow bark + citrus slice |
| 2 | Centella Asiatica | `02-centella-asiatica.png` | fresh cica leaf sprig |
| 3 | Bamboo Extract | `03-bamboo-extract.png` | bamboo stalk segments + extract dish |
| 4 | Green Tea | `04-green-tea.png` | loose dried leaves + brewed tea dish |
| 5 | Birch Sap | `05-birch-sap.png` | birch bark strip + sap vial |
| 6 | Ginseng | `06-ginseng.png` | whole forked root |
| 7 | Bifida Ferment Lysate | `07-bifida-ferment-lysate.png` | glass dish of cloudy fermented liquid |
| 8 | Hyaluronic Acid | `08-hyaluronic-acid.png` | glass dish of clear viscous gel |
| 9 | Ceramides | `09-ceramides.png` | glass dish of white waxy lipid balm |
| 10 | Niacinamide | `10-niacinamide.png` | glass dish of clear liquid essence |
| 11 | Peptides | `11-peptides.png` | glass dish of blue-tinted serum + microbeads |
| 12 | Snail Mucin | `12-snail-mucin.png` | glass dish of glossy stretching gel |
| 12b | Snail Mucin (source) | `12b-snail-mucin-source.png` | companion shot — the live snail on a leaf, same cream backdrop |
| 13 | Panthenol | `13-panthenol.png` | glass dish of white lotion |
| 14 | Soybean Extract | `14-soybean-extract.png` | soybean pods, one split open |
| 15 | Propolis | `15-propolis.png` | amber resin chunk + honeycomb |
| 16 | Retinol | `16-retinol.png` | amber dropper bottle, golden-orange oil |
| 17 | Royal Jelly | `17-royal-jelly.png` | glass dish of pale creamy jelly + honeycomb |
| 18 | Mugwort | `18-mugwort.png` | fresh silvery-green leaf sprig |
| 19 | Rice Extract | `19-rice-extract.png` | rice grains + rice-water dish |
| 20 | Vitamin C | `20-vitamin-c.png` | halved fresh orange |

## seoulhabit-learn additions (2026-08-30)

Six more entries, added for `seoulhabit-learn` handles the original 20-item glossary set
doesn't cover. Named `sh-<handle>.png` (not `NN-slug.png`) to mark them as this addition, not
members of the numbered glossary set above — see `TREATMENT-SPEC.md` for why. Manifest with
full generation provenance (model, job id, prompt, reference image) at `manifest.json` in this
folder.

| Handle | File | Depicted as | Branded |
|---|---|---|---|
| `pdrn` | `sh-pdrn.png` | glass dish, pale opalescent viscous serum with a pouring stream | No |
| `tea-tree-oil` | `sh-tea-tree-oil.png` | glass dropper bottle, pale essential oil | No |
| `betaine-salicylate` | `sh-betaine-salicylate.png` | glass dish, clear liquid solution | No |
| `madecassoside` | `sh-madecassoside.png` | glass dish, white crystalline powder | No |
| `galactomyces` | `sh-galactomyces.png` | glass dish, cloudy fermented liquid | No |
| `retinal` | `sh-retinal.png` | glass dropper bottle, deep vivid orange-amber oil | No |

**Bottle/dropper-format subjects are branded with SeoulHabit marketing going forward**
(`TREATMENT-SPEC.md`'s 2026-08-30 amendment) — `tea-tree-oil` and `retinal` above predate that
ruling and were kept as generated, not regenerated.

Raw botanicals are shown as the real plant/root/leaf/fruit. Ingredients
with no natural "raw" form of their own (niacinamide, hyaluronic acid,
peptides, ceramides, panthenol, AHA/BHA, bifida ferment lysate) are shown
as a small glass dish holding the liquid/gel/balm form skincare
formulations actually use — matched to each one's "what it is" text in the
glossary source, not invented freehand.

## Superseded concept alternates

Four earlier Higgsfield renders explored a different visual concept for
snail mucin before the team settled on the dish-of-gel + live-snail-on-leaf
pair above (`12-snail-mucin.png` / `12b-snail-mucin-source.png`). Kept here
for provenance, not part of the numbered 20-item set matched to the
glossary — don't drop these into a slot expecting the 2048×2048 square spec
the rest of this directory uses.

| File | Concept | Generated |
|---|---|---|
| `12c-snail-mucin-alt-dropper-moss-1.png` | Dropper bottle, one snail on the shoulder near the cap, mossy stone slab, sage-green bokeh, golden-hour side light | 2026-08-26 |
| `12d-snail-mucin-alt-dropper-moss-2.png` | Same concept, second generation | 2026-08-26 |
| `12e-snail-mucin-alt-dropper-studio-1.png` | Dropper bottle, two snails crawling on the glass, plain light-gray seamless studio background | 2026-08-26 |
| `12f-snail-mucin-alt-dropper-studio-2.png` | Same concept, second generation | 2026-08-26 |

All four are 896×1200 (3:4) — a different aspect ratio from the 2048×2048
square used everywhere else in this set — generated two days before `12` /
`12b` at the correct spec. Neither dropper-bottle concept was chosen;
documented here rather than silently dropped, following this repo's usual
practice for superseded work (see the PDRN Renewal Codex note in the parent
[catalog README](../README.md)).

## What this is for

Raw B-roll / thumbnail stock for future video projects. Not wired into any
composition or build pipeline.

## Independent of the glossary card's icon decision

`skincare-ingredient-glossary/README.md` documents that per-ingredient AI
photography was already tried for the *glossary card component* itself and
deliberately retired in favor of one uniform Lucide `leaf` glyph, because
that's what the real design system's `Icon.jsx` actually specifies for
ingredient labels. This set doesn't reverse that call — it's a separate
photography library for B-roll and thumbnails, not a replacement for the
card icon. Don't wire these into a `TermDefinition`-based card without
re-reading that decision first.

## Caveat

Like the glossary itself, the "commonly used for" framing behind these
depictions isn't a cited claim — these are visual references, not a
sourcing chip. Pair with `ClaimLockup` and a real `ING-*` source if a video
asserts efficacy rather than just showing the ingredient.
