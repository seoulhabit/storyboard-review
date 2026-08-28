# Skincare Ingredient Glossary

A rendered reference glossary, not a single-ingredient piece like the other
entries in this folder — catalogued here as one entry rather than split
across twenty mostly-empty ingredient folders.

**Project:** `../../../videos/skincare-ingredient-glossary/` — rendered
(`renders/skincare-ingredient-glossary_2026-08-27_23-15-09.mp4`, 76s,
1080×1920, confirmed via `ffprobe`). Twenty ingredients, in order: AHA/BHA,
Centella Asiatica, Bamboo Extract, Green Tea, Birch Sap, Ginseng, Bifida
Ferment Lysate, Hyaluronic Acid, Ceramides, Niacinamide, Peptides, Snail
Mucin, Panthenol, Soybean Extract, Propolis, Retinol, Royal Jelly, Mugwort,
Rice Extract, Vitamin C. Each gets a name / Korean gloss / category / "what
it is" / "commonly used for" card.

## Design system

Restyled against the **SeoulHabit Video Design System** (shared Claude
Design canvas), replacing the original standalone palette: flat ink
`#131516` field (no gradients, no glow — the system bans both), the
`--color-topic-ingredient` → perilla green identity, EB Garamond display /
Inter body / JetBrains Mono technical / Noto Sans KR for Hangul, the
system's own type scale, spacing steps, radii, and the exact
`--e-out`/`--e-in`/`--e-inout` cubic-bezier motion curves at token durations
(`--d-snap`, `--d-fast`, `--d-base`, `--stagger-line`). Each card's icon has
since been replaced by a full illustration — see **Images** below.

**Content caveat, stated plainly:** the design system's core rule is that
any on-screen claim of efficacy carries a source id or does not render. This
glossary's "commonly used for" lines come from a general ingredient chart,
not cited studies, so they're kept descriptive rather than phrased as
sourced claims, and the outro card carries an explicit disclaimer
("General ingredient overview — not sourced claims, not medical advice").
They do not meet the system's sourcing bar the way an `ING-*`-cited claim
would — this is a breadth-first pass across twenty terms, not twenty
fact-checked claims.

## Images

`images/` holds twenty flat illustrations, one per ingredient (`01-aha-bha.png`
through `20-vitamin-c.png`, 1200×1200, transparent background, ~25KB each) —
the component-image library the cards now draw on in place of the original
64px line icons. Each is a bottle (or jar/vial/beaker, matched to the
ingredient's form) styled with 1-3 category-appropriate props — leaves and
roots for botanicals, a honeycomb and dripping honey for Propolis, a
ball-and-stick model for Peptides and Retinol, citrus slices for Vitamin C,
and so on — built entirely from flat SVG shapes in the design system's own
token colors (perilla, highlighter, coral, aqua, paper), no gradients, no
photography.

They're generated *by* HyperFrames, not by an image model: authored as SVG
in a throwaway 20-cell composition, then captured to PNG with
`hyperframes snapshot --zoom "x,y,w,h"` (one crop per cell). An earlier pass
tried an actual AI photo model instead — HyperFrames itself has no
image-generation capability, only a render/capture pipeline, so a photoreal
look would have had to come from an external model — but the photos were
dropped in favor of this HyperFrames-native illustration approach per
explicit direction, keeping the whole pipeline (art + composition + render)
inside one framework and strictly on the design system's token palette
rather than naturalistic photo color.

Used via `<img>` in the card's old icon slot, sized 400×400 in the two video
formats (`object-fit: contain`, no cropping) and 360×360 in the static
components below. Wired into: this project's `index.html` (own `assets/`),
each of the four Part 1–4 projects below (own `assets/`, just the five
images each part uses), and all twenty `components/*.html` files (referenced
directly via `../images/`, no per-file copies needed since those are static
reference pages, not renderable projects).

## Components

`components/` holds all twenty ingredient cards as individual, standalone
HTML files — the same TermDefinition-pattern card as the video, extracted
one-per-file for reuse outside the render (static layout, a one-time CSS
rise-in on load, no GSAP/HyperFrames dependency, matching this catalog's
existing `-spike.html` convention of self-contained reference files):

| # | File | Ingredient |
|---|---|---|
| 01 | `components/01-aha-bha.html` | AHA / BHA |
| 02 | `components/02-centella-asiatica.html` | Centella Asiatica |
| 03 | `components/03-bamboo-extract.html` | Bamboo Extract |
| 04 | `components/04-green-tea.html` | Green Tea |
| 05 | `components/05-birch-sap.html` | Birch Sap |
| 06 | `components/06-ginseng.html` | Ginseng |
| 07 | `components/07-bifida-ferment-lysate.html` | Bifida Ferment Lysate |
| 08 | `components/08-hyaluronic-acid.html` | Hyaluronic Acid |
| 09 | `components/09-ceramides.html` | Ceramides |
| 10 | `components/10-niacinamide.html` | Niacinamide |
| 11 | `components/11-peptides.html` | Peptides |
| 12 | `components/12-snail-mucin.html` | Snail Mucin |
| 13 | `components/13-panthenol.html` | Panthenol |
| 14 | `components/14-soybean-extract.html` | Soybean Extract |
| 15 | `components/15-propolis.html` | Propolis |
| 16 | `components/16-retinol.html` | Retinol |
| 17 | `components/17-royal-jelly.html` | Royal Jelly |
| 18 | `components/18-mugwort.html` | Mugwort |
| 19 | `components/19-rice-extract.html` | Rice Extract |
| 20 | `components/20-vitamin-c.html` | Vitamin C |

## Short-form cuts (Parts 1–4)

Four standalone short-form videos, each a themed 5-ingredient cut of the
glossary above, grouped by skin concern per a supplied content brief (a
hook, five ingredients with punchier one-line descriptions, and a
caption/CTA). Same design-system tokens, TermDefinition card, and easing as
the full glossary — just five cards instead of twenty, ~24s instead of 76s.
Each is its own HyperFrames project (own `index.html` / `renders/` /
`meta.json`), not nested under this one, matching how every other video in
this repo is its own top-level `videos/` folder.

| Part | Folder | Theme | Ingredients |
|---|---|---|---|
| 1 | [`videos/skincare-glossary-part-1-barrier-repair/`](../../../videos/skincare-glossary-part-1-barrier-repair/) | The Barrier Repair Heroes — for redness and sensitivity | Centella Asiatica, Ceramides, Panthenol, Mugwort, Green Tea |
| 2 | [`videos/skincare-glossary-part-2-hydration-boosters/`](../../../videos/skincare-glossary-part-2-hydration-boosters/) | The Ultimate Hydration Boosters — for dehydrated skin | Hyaluronic Acid, Snail Mucin, Birch Sap, Bamboo Extract, Bifida Ferment Lysate |
| 3 | [`videos/skincare-glossary-part-3-glow-brightening/`](../../../videos/skincare-glossary-part-3-glow-brightening/) | The Glow & Brightening Edit — for dullness and dark spots | Vitamin C, Niacinamide, Rice Extract, Propolis, Soybean Extract |
| 4 | [`videos/skincare-glossary-part-4-texture-anti-aging/`](../../../videos/skincare-glossary-part-4-texture-anti-aging/) | The Texture & Anti-Aging Powerhouses — for breakouts and fine lines | Retinol, AHA/BHA, Peptides, Ginseng, Royal Jelly |

Parts 1–4 fully account for all twenty glossary ingredients (5 × 4 = 20) —
the source brief said "5 Parts" but only supplied hook/ingredient/CTA
content for four groupings, which already exhaust the ingredient set.
Rather than invent a fifth theme and ingredient list that wasn't specified,
this delivers exactly the four parts that were, reading "5" as the brief's
own per-part ingredient count, not a parts-total.

Each folder's `caption.txt` holds the hook, ingredient list, and the
caption/CTA exactly as written — including its emoji (👇 💧 🛒✨ ⏳). The
design system's content rules ban emoji from anything rendered ("Emoji:
never. Not in titles, not in thumbnails, not in captions.") — so none
appear in the video frames themselves — but `caption.txt` is social-post
copy that ships beside the video, not pixels the system renders, so the
emoji are kept there rather than silently dropped.

Three of the twenty overlap with dedicated entries elsewhere in this
catalog — [Ginseng](../ginseng/README.md), [Snail Mucin
Essence](../snail-mucin/snail-mucin-poster-spike.html), and this project's
own Retinol card (not to be confused with [Retinal vs.
Retinol](../retinal-vs-retinol/README.md), which is specifically about the
retinal/retinol distinction — a different piece with a different job, not
a duplicate). Those dedicated entries are full bespoke posters; these
components are the uniform, design-system-token glossary card — a
deliberately different, consistent format, not a redundant copy.

No `STORYBOARD.md` in this project (unlike PDRN, snail mucin, or red
ginseng), so the ingredient order and card copy above come straight from
`index.html`, the rendered video, and `components/`, not a design-plan
document.
