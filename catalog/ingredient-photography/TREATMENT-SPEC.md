# Ingredient photography — treatment spec

Extracted from the 20 existing entries in this folder (5 sampled directly at full resolution —
`02-centella-asiatica`, `06-ginseng`, `08-hyaluronic-acid`, `09-ceramides`, `20-vitamin-c` —
background color measured by pixel sampling, not estimated). Committed here so a new entry can
be generated to match the set without re-deriving the look from scratch or drifting from it.
Adopted 2026-08-30 as the sole identity-slot image source for `seoulhabit-learn`'s ingredient
passports (site repo ruling, folded into that repo's `IMAGE-RENDER-CONTRACT.md` rule 3
amendment — see that repo's `DEC-072`).

## Framing

- **Aspect ratio: 1:1 square, 2048×2048px.** Every existing entry matches this exactly (verified
  via the GitHub Contents API's own reported file dimensions, not assumed).
- **Single subject, centered with generous negative space.** The subject (or subject + its
  vessel) occupies roughly the middle third to middle half of the frame; every side carries
  visible breathing room — no edge-to-edge crops, no subject touching the frame border.
- **Orientation follows the subject's natural form**, not a fixed angle: a leaf sprig or root is
  laid flat and photographed top-down (true overhead); a glass dish or jar is shot from a
  near-overhead angle shallow enough to show the vessel's rim and depth (roughly 75–85° from
  horizontal, not a flat top-down that would flatten the glass to a circle with no visible wall).
- **No crop variation, no dramatic angle, no macro extreme close-up** — every sampled entry
  keeps the full subject in frame with a consistent, moderate camera distance.

## Background

- **Warm off-white / cream matte seamless**, not pure white and not a color background.
  Measured corner pixel values across the 5 sampled entries cluster in the `#E8E3DC`–`#F9F7F5`
  range (warm, R ≥ G ≥ B) — closer to unbleached paper or a warm gallery wall than a clinical
  white studio sweep.
- **Visible paper/surface texture at full resolution** — a subtle grain, not a flat digital
  gradient. Present on every sampled entry.
- **No props, no second surface, no gradient backdrop, no color block.** The background is one
  continuous plane behind and (for the top-down shots) beneath the subject.

## Lighting

- **Soft, diffused, single dominant direction** — every sampled entry casts one soft-edged
  shadow, not multiple hard shadows from multiple sources. Shadow direction varies per shot
  (not a fixed light position), but is always soft-edged and low-contrast, never a hard graphic
  shadow.
- **No specular hotspots, no glare, no visible light source in frame.** Glass/liquid subjects
  (hyaluronic acid, vitamin-c's citrus flesh) show gentle sheen and internal light play, never a
  blown-out highlight.
- **Even overall exposure** — background stays legible and textured across the frame; corners
  are allowed a natural, soft vignette-style falloff (measured up to roughly 15% darker than
  the lit background area — see `09-ceramides`) but never a hard vignette or crushed shadow.

## Subject treatment

- **Botanicals** (leaf, root, sprig): shown as the real, whole raw material — fresh and
  slightly dewy where that's true to the plant (`centella-asiatica`), dried and fibrous where
  that's true to the material as sold (`ginseng`'s root). Never a stylized illustration, never
  a cut cross-section unless the real ingredient is naturally shown that way (`vitamin-c`'s
  orange half — chosen because ascorbic acid itself has no raw "whole form" of its own; the
  fruit source stands in, per this folder's own stated rule for ingredients "with no natural
  raw form of their own").
- **Formulated / liquid / cream materials** (hyaluronic acid, ceramides): shown as a small
  glass dish or jar holding the actual liquid/gel/cream form a skincare formulation would use —
  never the raw powder or an invented "pure active" visual with no real-world analog.
- **No text, no logo, no brand mark, no wordmark anywhere in frame.**
- **No human hand, no face, no body part** — every sampled entry is the material alone.

## Naming (for `seoulhabit-learn` additions)

The existing 20 files use `NN-slug.png`, numbered against a *different* 20-item glossary list
unrelated to `seoulhabit-learn`'s own 13 ingredient handles (confirmed: only 7 of those 13
handles resolve to an existing numbered entry by name — see that repo's `scripts/resolve-
catalog-image.mjs`). A `seoulhabit-learn` addition should **not** claim the next free number in
that sequence, which would misleadingly imply membership in the original glossary's own
list. Proposed convention: `sh-<handle>.png` (e.g. `sh-pdrn.png`, `sh-tea-tree-oil.png`),
`sh-` marking it as this repo's own addition, `<handle>` matching `seoulhabit-learn`'s exact
route handle so the mapping never needs a translation table.

## What this spec does not cover

Per-ingredient art direction (which vessel, which cut, whether dewy or dry) is a judgment call
made per subject from what the record actually says the ingredient is — matching this folder's
own stated practice ("matched to each one's 'what it is' text ... not invented freehand"), not
a fixed rule this spec can state in advance. The founder confirms each new subject's proposed
treatment before generation, same as any other identity-slot image.

## Generation mechanics (discovered 2026-08-30, for whoever runs generation next)

Higgsfield's `marketing_studio_image` model (the tool this folder's own README already
credits, and the standing generation tool per `seoulhabit-learn`'s `DEC-072`) takes a required
`medias` reference-image input, not a text prompt alone — confirmed via `models_explore` on
this model id. This matches the folder's own README ("styled to match a user-supplied
reference photo of 7 sample ingredients"). A new generation should pass one of the existing 20
entries (or the original 7-sample reference, if still available) as the reference image, not
attempt a from-scratch text-only prompt against this spec's written description alone.

Cost, preflighted via `get_cost: true` (no charge): **2 credits per generation at 2k
resolution**, 1:1 aspect ratio.

## Amendment 2026-08-30 — bottle/dropper-format subjects carry SeoulHabit branding

**Founder ruling, live in chat, seoulhabit-learn session:** bottle/dropper-format subjects
(essential oils, tinctures — anything shown in an upright glass dropper bottle, per this spec's
own Subject Treatment section) are branded with SeoulHabit marketing going forward. This is a
**deliberate departure** from the "no text, no logo, no brand mark" rule stated earlier in this
document — that rule is unchanged for every other format (dish, powder, mound) and for the
original 20 entries, none of which carry any mark.

**Scope, precisely:** applies to *future* generations of bottle/dropper-format subjects only.
The two bottle-format entries generated the same day this ruling landed (`sh-tea-tree-oil.png`,
`sh-retinal.png`) were made under the prior no-branding rule and were explicitly kept as
generated, not regenerated — see `seoulhabit-learn`'s own decision record for this cycle.

**Open, not resolved here:** whether a *branded* bottle image may be adopted into
`seoulhabit-learn`'s passport identity slot once one exists — that site's own `CLAUDE.md`
carries a standing "no commerce" constraint for ingredient content. This spec governs the
catalog's own generation convention; it does not itself authorize what a consuming site adopts.

## Amendment 2026-08-30 (second) — the open question above is now resolved: two variants required

**Founder ruling, live in chat, `seoulhabit-learn` session, resolving the "open, not resolved
here" paragraph directly above:** a branded bottle image is **never** adopted into a consuming
site's own identity slot — not `seoulhabit-learn`'s, not any future one. The identity slot
answers "what is this material"; a branded bottle answers "which product to buy," a claim the
record can't source and most consuming sites have no commerce to back. It also dates instantly
against a real label or formula change.

**The split is by destination, not by subject.** Bottle/dropper-format subjects still carry
SeoulHabit branding in this catalog, per the amendment above — that's for this catalog's own
video/marketing use, unchanged. But **from this ruling forward, a bottle/dropper-format
generation produces two variants**, not one:

1. **Branded** — this catalog's own convention (the amendment above), filed under this folder's
   normal `sh-<handle>.png` naming, for video and marketing use.
2. **Unbranded** — the only variant any consuming site's identity slot may ever adopt. Suggested
   naming: `sh-<handle>-unbranded.png`, so the pair is unambiguous at a glance and neither file
   can be mistaken for the other by a script matching on the bare handle.

If only a branded variant exists for a bottle-format handle, it does not get adopted anywhere
outside this catalog — the consuming site's identity slot keeps whatever unbranded asset it
already has (which may be nothing, rendering as text) rather than showing a branded image.

Recorded in full, with rendered evidence and the founder's ruling text verbatim, in
`seoulhabit-learn`'s own decision record for this cycle (`DEC-075`) — this amendment mirrors
that record's ruling into the catalog's own generation convention, since a future generation
cycle may run from this folder without seeing `seoulhabit-learn`'s decision log at all.
