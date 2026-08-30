# TermDefinition

A full-frame hero card that presents one term at a time — icon, name (+
optional Korean), category, a primary definition, and a secondary "commonly
used for" line — cycling through a data array with identical choreography per
entry, alongside a continuous linear progress rail.

## Why this one, and why now

This is the strongest harvest candidate found in a review of every shipped
composition in this repo, by a wide margin: **the exact same component,
built independently five separate times, was never once added to this
catalog.** Confirmed by grepping every `videos/*/index.html` and
`videos/*/compositions/frames/*.html` for class-name frequency —
`.term-name`, `.term-category`, `.term-body`, `.term-rule`, `.term-label-2`,
`.term-body-2`, `.term-index`, and `.card-inner` each appear 19–21 times,
identically named, identically styled, across five separate video projects:

- `videos/skincare-ingredient-glossary/index.html` (20 terms)
- `videos/skincare-glossary-part-1-barrier-repair/index.html`
- `videos/skincare-glossary-part-2-hydration-boosters/index.html`
- `videos/skincare-glossary-part-3-glow-brightening/index.html`
- `videos/skincare-glossary-part-4-texture-anti-aging/index.html`

The shipped code's own in-line comment names it directly: *"ingredient card
— **TermDefinition**, adapted for a full-frame centered hero use rather than
TermDefinition's native lower-third/overlay placement."* So this isn't a
pattern this session is naming for the first time — it's a real design-system
component (from the same claude.ai project, `75132ad8-b81c-4151-8a4c-83368df1d949`,
other catalog entries cite) that five different builds each independently
reimplemented from scratch instead of reusing, because nothing pointed a
future build at a shared source. This entry is that shared source.

**Not independently re-verified against DesignSync this session** —
unavailable in a non-interactive session (same limitation `routine-ladder`'s
README flags when it can't re-check live). What's here is transcribed
verbatim from the five shipped implementations, which agree with each other
byte-for-byte on every token and class name — a stronger signal than a single
spec read would be, but still worth a live DesignSync confirmation before
treating the *native* lower-third/overlay placement (only the full-frame
adaptation shipped in this repo) as fully specified.

## Field contract

```js
{ name: "Retinal", kr: "레티날", category: "Vitamin A derivative",
  what: "…primary definition, ~1-2 sentences…",
  used: "…commonly-used-for line, ~1 sentence…" }
```

`kr` is optional — omit it and the Korean-name line is skipped entirely (not
rendered empty), exactly as the shipped code does for ingredients with no
common Korean name (e.g. "AHA / BHA", "Bifida Ferment Lysate" in the real
glossary data).

## Icon

`.term-icon` renders one glyph from the design system's real `Icon.jsx` —
copied path data, not drawn, 24×24 viewBox, constant 3-unit stroke (never
scaled by container size). All five shipped uses render the same role
(`ingredient` → Lucide "leaf"), so that's what this spike ships. Swapping the
icon per `category` (a root extract vs. a vitamin vs. a ferment) is a natural
extension the field contract already supports structurally, but the other
`Icon.jsx` roles weren't available to read this session — implement by
extending `TERMS[i]` with an `icon` field and branching the glyph string,
following the exact copy-not-draw rule `routine-ladder`'s README also states.

## The companion progress rail

`.progress-wrap` / `.progress-fill` — a thin `--aqua` bar spanning the full
safe-width at the top of frame, filling **linearly** (`ease: "none"`, a
direct temporal readout, not an eased entrance) across the *entire* video's
runtime, not just one card's. All five shipped videos pair it with
TermDefinition specifically — this is a "how far through the list am I" cue,
not a generic loading bar. Harvested together because no shipped use has ever
run one without the other.

## What's genuinely reused vs. demo-only in this spike

- Every token, class name, dimension, and animation timing below is
  transcribed from the shipped code, unchanged.
- The three demo terms (Retinal, PDRN, Azelaic Acid) are invented for this
  spike and are **not** the real glossary content — the 20 real ingredients
  stay in `videos/skincare-ingredient-glossary/`, not duplicated here.
- The per-card build-and-choreograph loop (`TERMS.forEach` building
  `.clip` sections, then a second `TERMS.forEach` scheduling identical
  staggered tweens per card) is the real shipped pattern, generalized only by
  extracting it from one project's hardcoded 20-item array into this spike's
  swappable 3-item one.

## Status

**SPIKE — not wired to `build.mjs`.** Matches this catalog's existing
convention (`catalog.md` §1) — a validated, self-contained visual reference,
not yet plugged into the real HyperFrames composition pipeline. Debug
scrubber behind `?debug=1` (`t=0` / `t=end` buttons, a range input driving
`window.renderFrame(t)`), same harness every other timed spike in this
catalog uses.

**How to use it in a new video:** replace the `TERMS` array with real data,
adjust `CARD_DUR` per card to match the beat sheet, and — this is the whole
point of harvesting it — don't reimplement `.term-*`/`.card-inner`/the
choreography loop from scratch the way the five prior videos each did.
