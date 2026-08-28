# Skincare Ingredient Glossary

A rendered reference glossary, not a single-ingredient piece like the other
entries in this folder — catalogued here as one entry rather than split
across twenty mostly-empty ingredient folders.

**Project:** `../../../videos/skincare-ingredient-glossary/` — rendered
(`renders/skincare-ingredient-glossary_2026-08-27_23-40-26.mp4`, 76s,
1080×1920, confirmed via `ffprobe`). Twenty ingredients, in order: AHA/BHA,
Centella Asiatica, Bamboo Extract, Green Tea, Birch Sap, Ginseng, Bifida
Ferment Lysate, Hyaluronic Acid, Ceramides, Niacinamide, Peptides, Snail
Mucin, Panthenol, Soybean Extract, Propolis, Retinol, Royal Jelly, Mugwort,
Rice Extract, Vitamin C. Each gets a name / Korean gloss / category / "what
it is" / "commonly used for" card.

## Design system

Restyled against the **SeoulHabit Video Design System**. Two passes:

**Pass 1 (visual, screenshot-derived):** colors, type, spacing, radii, and
motion curves transcribed by eye from the Claude Design canvas — flat ink
`#131516` field (no gradients, no glow), `--color-topic-ingredient` →
perilla green, EB Garamond / Inter / JetBrains Mono / Noto Sans KR, the
`--e-out`/`--e-in`/`--e-inout` cubic-beziers. Mostly right, but a
screenshot can't be diffed against a source file.

**Pass 2 (source-verified):** the design project connected via the
`DesignSync` MCP tool (`claude.ai/design/p/75132ad8-b81c-4151-8a4c-83368df1d949`)
and read directly — `tokens/*.css`, `_ds_manifest.json`, and the real
`TermDefinition`/`Icon` component source, not a rendering of them. That
surfaced real gaps pass 1 missed:

- **The Korean font was loading from Google Fonts at render time.** The
  system self-hosts a video-specific subset (`assets/fonts/NotoSansKR-500-subset.woff2`)
  specifically because the CDN face is missing glyphs the video needs, and
  because a deterministic render pipeline shouldn't fetch fonts over the
  network. Copied in as `assets/NotoSansKR-500-subset.woff2` in every
  project that needs it.
- **The on-ink text hierarchy was fabricated.** `--on-ink-secondary` /
  `--on-ink-tertiary` were opacity steps on `--paper` I made up because they
  looked right. The real tokens are solid, measured hex —
  `--ink-2-dark #878B8C`, `--ink-3-dark #7C8082`, the latter explicitly
  documented as sitting at the 4.59:1 AA floor. Swapped in verbatim.
  `TermDefinition`'s own definition text renders in `--ink-2-dark`
  (secondary), not full paper-white — matched.
- **The safe-area padding was hand-guessed.** `tokens/layout.css` has an
  actual `--short-safe-*` set for the 9:16 lane (`120px` / `162px` /
  `360px` / `60px`, top/right/bottom/left) that doesn't match what was
  eyeballed before. Swapped in verbatim.
- **The card's fill, border, and elevation didn't match `TermDefinition.jsx`.**
  The real component uses `--capsule-dark` (`rgba(19,21,22,.8)`, not a
  faint paper tint), a solid `--rule-dark` border, and `--elev-2` — no
  shadow was applied before.
- **Name and Korean gloss render inline,** baseline-aligned, the Korean
  gloss in `--aqua` — not stacked in a muted secondary color, which is what
  this card did before.
- **Type-line motion ran at 400ms; the real grammar (`motion-grammar.card.html`)
  specifies 500ms** (rise 48px + fade, e-out, 80ms stagger) for that
  element class. Fixed across all five compositions.
- **The icon.** `Icon.jsx`'s actual `ICON_ROLES.ingredient` maps to exactly
  one glyph — Lucide `leaf`, outline, `currentColor`, a constant 3-viewBox-unit
  stroke that scales with size. Not a per-ingredient illustration: the
  component's own comment is explicit that a standard, repeated glyph
  reads as a label rather than getting mistaken for bespoke channel
  artwork, "until the finished mark lands." Two earlier passes (an AI photo
  model, then a hand-built HyperFrames illustration sheet) gave each
  ingredient its own bottle-and-props scene — neither matches how the real
  system actually labels "ingredient" content, so both are retired in favor
  of the one real glyph, verbatim path data, correct stroke ratio, uniform
  across all twenty terms.

**Where this card knowingly extends past `TermDefinition.jsx`, not just
approximates it**, because the real component and this use case solve
different problems — it's a left-aligned lower-third/overlay for footage,
this is a full-frame hero card in a sequence with nothing behind it:

- **A second body line** ("Commonly used for") that the real component's
  field list doesn't have — `TermDefinition.prompt.md` is explicit that
  nominal fields only belong here, and an efficacy/usage sentence needs a
  `ClaimLockup` with a source chip instead. This glossary's "commonly used
  for" text isn't cited (see the caveat below), so routing it through
  `ClaimLockup` would fabricate a sourcing rigor it doesn't have; kept as a
  visually-subordinate (`--ink-3-dark`, tertiary) extension instead of
  silently dropping content the user asked for.
- **Centered, not left-aligned.** `TermDefinition.jsx`'s root has no
  `items-center` — by design, since it's meant to sit in a corner over
  moving footage. Twenty sequential full-frame cards read better centered;
  kept centered.
- **The category line isn't labeled `INCI ·`.** The real field is
  literally an INCI/formal name (`inci` in `TermDefinition.d.ts`); this
  glossary's category values ("Botanical extract," "Vitamin B3") are
  categorical, not verified INCI nomenclature, so they keep the chip
  styling without the `INCI ·` prefix — that label would assert something
  not actually true of this data.
- **No `Logo` component.** `Logo.jsx`'s own prompt file calls it "a
  placeholder monogram, not a delivered brand mark" and flags its
  Montserrat file as unfit for a long render. Not worth building against a
  spec its own author hasn't signed off on; the plain mono wordmark stands.

**Content caveat, unchanged:** the design system's core rule is that any
on-screen claim of efficacy carries a source id or does not render. This
glossary's "commonly used for" lines come from a general ingredient chart,
not cited studies, so they're kept descriptive rather than phrased as
sourced claims, and the outro card carries an explicit disclaimer
("General ingredient overview — not sourced claims, not medical advice").

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
