# Story input — pinned per R-3 (WO-FVC-005)

**Source (R-3):** `https://seoulhabit.com/ingredient/centella-asiatica/`, pinned to
site repo `github.com/seoulhabit/seoulhabit-learn` commit `cacff81` (clean at
that SHA — confirmed this session). Route: `src/routes/passports.ts`'s
`/ingredient/${handle}`. G0-7 default (centella first in line); WO correction
8.9 confirms **12 citations / 12 findings** — the strongest passport on the
site — from `content/ingredients/centella-asiatica.json` and
`content/findings/centella-asiatica.json` at that SHA.

## Plain-English (site's own copy, `plain_english`)

Centella asiatica — also called cica, gotu kola or tiger grass — is a
botanical extract used in formulas aimed at comfort and barrier support.
Studies showing hydration and redness benefits tested finished creams and
gels containing the extract, not the extract on its own, so the results
belong to those formulas rather than to the ingredient in isolation. Its
best-known constituents are madecassoside and asiaticoside.

## Quick facts (site's own copy, `quick_facts`)

- A soothing botanical also known as cica, gotu kola, or tiger grass.
- Calms visible redness and supports the skin barrier.
- Rich in madecassoside and asiaticoside, its active compounds.
- A staple in formulas for sensitive, reactive, or post-blemish skin.
- Rarely, people allergic to the Apiaceae plant family may react — patch-test
  if unsure.

## Misconception the video should correct

The FAQ's own framing (`faq[6]`, "What does the human evidence on cica
show?"): centella is popularly sold as a universal, all-purpose soother —
but the human studies that exist mostly tested **finished creams and gels**,
not the isolated extract, and the safety-review evidence (CIR/IJT) explicitly
does **not** cover isolated compounds like madecassoside on their own
(finding C7, verdict AMBIGUOUS). "It's in this cream, therefore it's
centella doing the work" is not something the evidence, read carefully,
actually says.

## Mechanism / what it's shown to do

- Repeat-insult patch test data (finding C1, 108 subjects, verdict
  PASS-CORRECTED): no skin irritation or sensitization observed at the
  tested concentration.
- A human cosmetic-formulation study (finding C6, 25 volunteers, 4 weeks,
  2.5–5% w/w): increased stratum corneum hydration, reduced transepidermal
  water loss — but explicitly **not an RCT** (no randomization, no control,
  no blinding — the source's own tier note).
- CIR/IJT expert-panel safety review (finding C7): concludes centella-derived
  ingredients are "safe as used in cosmetics... when formulated to be
  non-sensitizing" — but this covers 9 *whole-extract* materials, explicitly
  **not** isolated compounds.

## Proof / the caveat (rare allergy + pregnancy)

- Hausen 1993 characterizes centella as **"a weak sensitizer"** (finding D001-02,
  finding C2/C10) — a small, real, recurring case-report history of allergic
  contact dermatitis across decades and countries (Spain 1996, Portugal-area
  Turkey 2024), some on already-compromised skin.
- EMA's own cutaneous-use herbal monograph (finding D001-03/C3): "use during
  pregnancy and lactation is not recommended" — stated as **insufficient
  data**, not demonstrated harm, and the monograph covers traditional
  herbal preparations, not cosmetic-extract concentrations specifically.
  `videos/_channel/baseline.yaml` has no per-video pregnancy-caution flag
  yet, so this claim is scripted as attributed + concurrently flagged
  (`K-2`), never asserted as fact.

## Application

Per the FAQ (`faq[7]`): the reactions in the literature are allergic, not
breakout-type — no published report of centella causing acne-like breakouts
was located (an absence of evidence, not proof it can't happen). Patch-test
first, especially on a compromised barrier — the site's own `pregnancy_caution:
true` flag and `gentleness: "very gentle"` rating both carry forward here.

## Full findings corpus (for reference, not all scripted)

`content/findings/centella-asiatica.json` in the pinned site repo carries 37
individually-sourced findings (D001-01 through C37) — far more than a
45-second video can use. This brief draws only the passport's own
already-vetted, most load-bearing claims (`quick_facts`, `one_liner`, the
FAQ) rather than re-deriving the full harvest; the `[K-1]` claim table in
`01-story-brief.md` cites specific finding ids for exactly the claims that
made it into the script.
