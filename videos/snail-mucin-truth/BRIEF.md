---
workflow: faceless-explainer
flow: automation
storyboard: no
message: "Snail mucin is a legitimately useful hydrator with modest real evidence behind it — here's what it is, what it does, and how to use it right"
destination: shorts
aspect: 1080x1920
language: en
audience: "SeoulHabit's evidence-conscious skincare audience (same as pdrn-skin-regeneration / red-ginseng-two-routes / snail-mucin-glass-skin series)"
length: 65s
angle: concept
---

## Intent

Answer "is snail mucin actually worth it?" with a confident, slightly cheeky
but evidence-held-to-rigor tone — SeoulHabit's house voice. Six scenes,
following the user's own script structure: hook (macro goo → glass skin) →
intro ("Snail Mucin 101") → what is it (snail on leaf → INCI infographic) →
benefits (hydration / barrier support / post-acne marks) → how to use
(damp skin, pat don't rub, seal with moisturizer) → outro (bottle shot +
subscribe CTA). `VO_MODE: evidence-tuned` — the user's script sets scene
order, visuals, and voice, but every efficacy line is hedged and tagged
against a locked source-id set; see Customizations.

No product being marketed, no site capture — arbitrary topic explainer, so
`/faceless-explainer` is correct. Sibling `videos/snail-mucin-glass-skin/`
is a separate, already-finished 10s silent kinetic-type piece; it stays
untouched and is only an asset/motif donor here (palette, typography,
no-brand-mark constraint).

## Customizations

- **Evidence-tuning pass (required, not optional style polish).** Full raw
  script preserved verbatim in `user_script.txt`. The tuned VO in
  `SCRIPT.md` softens absolute/superlative claims and tags every
  efficacy-asserting line with a locked source id:
  - `ING-snail-mucin-S001` — composition (glycoproteins, allantoin, glycolic
    acid, HA-like mucopolysaccharides)
  - `ING-snail-mucin-S002` — hydration / barrier-support evidence
  - `ING-snail-mucin-S003` — post-acne-mark fading evidence
  - `ING-snail-mucin-S004` — collection-practice reporting (cruelty claim
    attribution, not assertion)
  - INCI name "snail secretion filtrate" and technique guidance (damp skin,
    pat don't rub, seal with moisturizer) are non-efficacy / mechanical —
    no id needed.
  - VO ban list: incredible, instantly, must, proven, cures, erases,
    guaranteed, miracle. "Acne scars" → "post-acne marks" (evidence is for
    marks/hyperpigmentation, not true scarring).
  - Cruelty-free claim is attributed to producers, not asserted as fact
    ("producers say... a common industry claim, though practices vary").
  - These four ids are **forward references** — the underlying source
    record lives in a sibling repo not present here (see PDRN/ginseng
    precedent). `STORYBOARD.md` carries a local Claims Inventory mapping
    every efficacy line to its id; ids must be reconciled against the real
    source record before this video is published anywhere.
- **Design system**: reuse the locked palette, typography, and motion
  language already established for this ingredient rather than inventing a
  new one — source: `../snail-mucin-glass-skin/shot-plan.json` (13-color
  eyedropped palette, Bricolage Grotesque + Noto Serif TC, slime-trail
  svg-path-draw motif, `no_brand_mark: true`) and
  `../../catalog/ingredients/snail-mucin/snail-mucin-poster-spike.html`
  (5 actives / 4 benefits content for the "what is" infographic beat).
  Re-author these as this project's own vector assets — do not iframe or
  embed the donor files.
- **No brand mark anywhere** — inherited constraint from the locked poster
  and the sibling 10s piece. Outro CTA is a generic "subscribe", no logo or
  URL lockup.
- **Success-color law**: this repo's `catalog/README.md` rule is
  celadon/aqua = "confirmed, no success color at any level." This
  ingredient's donor palette includes a seafoam trail color used purely as
  a decorative slime-trail motif — `frame.md` must explicitly declare that
  distinction (motif vs. status color) so the rule stays checkable.
- **Frame 6 photo asset**: `../../catalog/ingredient-photography/12-snail-mucin.png`
  (4.7MB flat-lay) — reframe to 9:16 and compress into this project's own
  `assets/` via `/media-use`; do not ship the original file size.
- Frame 5 (how-to-use) is illustrated-first (vector hands/steps); AI
  photoreal hands b-roll is an optional upgrade only, not the plan of
  record — hands are the highest-artifact-risk AI subject.

## Notes

- Voice/audio provider: resolve via `/media-use` at the audio step; do not
  default silently — confirm sign-in status or local engine availability
  first, matching the pattern already hit in `red-ginseng-two-routes/BRIEF.md`.
- Word budget: keep total VO to roughly 150-190 words across six lines so
  the 60-75s target holds without speed-warping.
- Optional CJK subhead (蝸牛黏液精華) may appear in Scene 2 title card if it
  strengthens the "Snail Mucin 101" beat — if kept, verify full glyph
  rendering at native resolution per this repo's established Korean/CJK
  glyph-check convention before final render.
