# TEMPLATES.md — how T1..T6.json are derived

## Provenance

Each `T*.json` is derived **by hand, once**, from the corresponding `.dc.html`
artboard in `reference/`, extracted verbatim from Claude Design project
`a7945a95-da21-4823-8b16-57c6ffa11558` on 2026-09-06. The artboard is **not**
parsed programmatically — a canvas artboard's DOM is a layout accident
(absolutely-positioned preview boxes, per-scene debug labels, a `<x-dc>`
preview harness), not a contract. Parsing it would encode those accidents as
rules. What the artboard *is* good for: the visual ground truth a reviewer
compares compiled output against, and a sha256 that flags when it has
changed and the derivation needs re-checking.

`artboard_sha256` in each `T*.json` is exactly that check:

```
$ shasum -a 256 videos/_system/templates/reference/T1-ingredient-explainer.dc.html
c38d3db5f4066174e19c05c0c08bee628f9bc358ed09298ca7e8d28e0a0d9fd7  ...
```

If a re-extraction ever produces a different hash, treat the `T*.json` as
stale until re-derived by hand and re-reviewed — never silently regenerated.

## What each `T*.json` actually says

- `sequence` (or `chapter_sequence`/`close_sequence` for T6): the ordered
  spine — which component fills which named section. This is what a beat
  sheet is **checked against**: a beat sheet names a `section`, the compiler
  looks it up in the template, and either finds a `component` to emit or
  fails naming the scene and the template. A beat sheet may also state
  `component` explicitly, which takes precedence — see `COMPILER.md`.
- `clay_slot_by_component`: which prop of each named component carries the
  scene's one clay element (the design system's "one clay element per
  scene" rule, enforced by the compiler as a codegen invariant, not left to
  the caller's judgement).
- `reference_timings_s`: the artboard's **own authored durations**,
  preserved for comparison — explicitly **not prescriptive**. The compiler
  computes every scene's real duration from `03-beat-sheet.json`'s
  `vo_duration_s` and slot word counts per `COMPILER.md`'s timing rule. Two
  of the six artboards' own reference timings already collide with this
  WO's own ceiling rule (D5): T3's mapping scene and T4's compare scene both
  run exactly 5.0s (no headroom), and **T6's steps chapter runs 6.0s**,
  over the 5.0s non-evidence/compare ceiling. T6.json's note works through
  that exact case — it is the one that actually exercises the compiler's
  scene-split logic on real design-system data, not a hypothetical.

## Component inventory confirmed against the six artboards

Every artboard names its components in its own scene-label comments, so the
sequence below is read off the source, not guessed:

| Template | Sequence |
|---|---|
| T1 Ingredient Explainer | ShHook → ShIngredient → ShRows → ShEvidence(anchor) → ShEndcard(anchor) |
| T2 How To Use | ShHook → ShIngredient → ShSteps → ShRows(anchor) → ShEndcard(anchor) |
| T3 What It Solves | ShHook → ShRows → ShIngredient → ShEvidence(anchor) → ShEndcard(anchor) |
| T4 Comparison | ShHook → ShCompare → ShQuote → ShEvidence(anchor) → ShEndcard(anchor) |
| T5 Myth Correction | ShHook → ShMyth → ShIngredient → ShEvidence(anchor) → ShEndcard(anchor) |
| T6 Long-form (per chapter) | ShHook → ShQuote/ShIngredient → ShSteps/ShRows → ShEvidence, closed once by ShEndcard(anchor) |

Every standard template (T1–T5) is exactly **5 scenes over 14.0s** in its own
reference cut, with the final two scenes always anchors (`ShEvidence` then
`ShEndcard`) — this is the design system's own worked convention, not
something this WO invented. `ShCompare`, `ShMyth`, `ShQuote`, `ShSteps` each
appear in exactly one standard template; `ShRows` and `ShIngredient` are the
only components reused across templates (three and three respectively).

## Per-scene chip, not per-video

Every scene in every artboard carries its **own** `chip` value matching
*that scene's own claim* (e.g. T1's rows scene cites `J. Cosmet. Dermatol.
2019` while its evidence scene cites `Br. J. Dermatol. 2011`) — never one
citation for the whole video. `COMPILER.md`'s asset rules and `K-4`'s
frame-to-claim mapping both depend on this: the chip is compiled per scene
from that scene's own beat-sheet source field, not hoisted to the root.

## The shader clause, and why it is not in these files

Every artboard's end-card scene label says *"anchor · … · shader at
11.35"* (or, for T6, *"carries the one shader"*). This WO's `C-6` ruling
(fired by `T1-FINDINGS.md`'s F1 resolving PARTIAL under a zero-HeyGen-spend
decision) forbids shader chains entirely. None of the `T*.json` files above
carry a shader field, and `ShEndcard.prompt.md` documents the deviation
explicitly. If C-6 is ever reversed, `RETIRED-transitions.md` has the
mechanism to restore.
