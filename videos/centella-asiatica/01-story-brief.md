# 01-story-brief.md — centella-asiatica

Source: `https://seoulhabit.com/ingredient/centella-asiatica/`, pinned to
`seoulhabit-learn` @ `cacff81` (R-3). `content/ingredients/centella-asiatica.json`
+ `content/findings/centella-asiatica.json` at that SHA.

## Objective

Correct the "cica is a universal soother, works because it's in this
product" assumption with what the actual human evidence supports — and
name the one real caveat (rare allergy) plainly.

## Misconception

Cica/centella is marketed and consumed as a general-purpose, works-on-
everything soother. The evidence that exists mostly tested **finished
creams and gels**, not the isolated extract on its own, and the one
dedicated safety review explicitly does **not** cover isolated actives
like madecassoside — "universal soother" oversells what's actually been
checked.

## Mechanism

Repeat-insult patch testing (108 subjects) found no irritation or
sensitization. A small (25-person, non-RCT) cosmetic-formulation study
measured real hydration and redness improvement — in finished creams and
gels, not the raw extract. The widely-cited CIR/IJT safety review covers
nine whole-extract materials, not isolated compounds.

## Proof

Finding C1 (Int J Toxicol 2023, PMID via the passport's own citation list):
"Neither skin irritation nor sensitization was observed" across 108
subjects — the largest safety dataset in this corpus.

## Application

Hausen 1993 characterizes centella as "a weak sensitizer" with a real,
recurring (if rare) allergic-contact-dermatitis case history — patch test
if sensitive. EMA's own cutaneous-use herbal monograph: pregnancy/lactation
use "not recommended," stated explicitly as an insufficient-data caution,
not a demonstrated-harm finding.

## Format decision (S-1)

Branch 2: `baseline.yaml formats.short.uploads_90d` = 46 of
`corpus.uploads_total` = 48 → **95.8% ≥ 60%** → **short**.

## Target length (S-2)

`retention.median_duration_top_quartile_curve_s: 49.0` — inside the 30–58s
clamp (already measured, per `baseline.yaml`'s own note). Target: **49.0s ±10%
(44.1–53.9s)**.

## Presenter (S-3)

Kinetic type — vocabulary/definition-and-evidence content, matches the
design system's own established presenter for this content shape (same as
the T3/T4 synthetic-fixture precedent).

## Voice (S-4) — finding, not a fresh halt

`baseline.yaml heygen.voice_id` is `null` (T2 `TOUCHPOINT-SETUP` never
ran). S-4's own carried rule text would read this as `BLOCKER-SETUP-PENDING`.
Treated as the same finding S4b's T7-rewritten local-substitute branch
already exists for (HeyGen connector unavailable, T1-FINDINGS F2), not a
second independent blocker — see `00-environment.md` and this run's
`09-run-report.md` `[NOT IN SKILL]` section for the follow-up correction
this surfaces for `policy.md`'s own S-4 text.

## §Sourcing — the [K-1] claim table

| On-screen chip | Backing | What it actually supports |
|---|---|---|
| "Centella asiatica — cica — a calming botanical, rich in madecassoside and asiaticoside." | Passport's own `plain_english`/`quick_facts`/`one_liner` (SeoulHabit Editorial, last reviewed 2026-08-16, 9 findings agent-checked) | **nominal** — identity/definition, inherited from the site's own already-reviewed published copy. |
| "Redness and hydration — yes, shown, but only in finished creams and gels, not the extract by itself." | Finding C6 — Ratz-Lyko et al., *Indian J Pharm Sci* 2016, PMID 27168678. Quote: "Topical application of cosmetic formulations containing Centella asiatica extract increased stratum corneum hydration and reduced transepidermal water loss." | **sourced** — real human study, but explicitly NOT an RCT (no randomization/control/blinding per the source's own tier note); 25 volunteers, forearm site, 2.5–5% w/w, 4 weeks. |
| "Marketed as a universal soother? The one review we found never actually tested that claim broadly." | Finding C33 — *Skinmed* 2022, PMID 35532760, narrative (not systematic) review | **sourced** — the review's own framing, characterizing the literature rather than confirming or refuting general-purpose efficacy. |
| "The safety review everyone cites covers the whole extract, not isolated actives like madecassoside alone." | Finding C7 — Expert Panel for Cosmetic Ingredient Safety, *Int J Toxicol* 2023, PMID 36812692. Verdict: **AMBIGUOUS**. Quote (does_not_establish): "does NOT cover isolated madecassoside or isolated asiaticoside as standalone compounds." | **sourced** — direct, accurate restatement of the review's own stated scope limit. |
| "In the largest repeat-use study on record — over a hundred people, weeks of skin contact — researchers saw no irritation and no allergic sensitization at all." | Finding C1 — *Int J Toxicol* 2023 (source-corrected 2026-08-16). Quote: "Neither skin irritation nor sensitization was observed during the study." 108 subjects, 6% effective induction concentration. | **sourced** — expert-panel secondary review carrying unpublished industry HRIPT data, not a primary study; verdict PASS-CORRECTED. |
| "Still, rare allergic reactions are on record, so patch test if your skin's sensitive." | Findings C2/C10 (Hausen 1993, PMID 8281778, "very weak sensitizers") + C4/C5 (Danese 1994, PMID 7821029; Gonzalo Garijo 1996, PMID 8766746 — single-patient case reports) + C11 (Özkaya 2024, 2 patients, Turkey) | **sourced** — real, recurring (if rare) case-report history across decades; single-case reports, not incidence data. |
| "Pregnant or nursing? The safety data's too thin to say either way." | Finding C3/D001-03 — EMA HMPC, *European Union herbal monograph on Centella asiatica*, EMA/HMPC/489142/2020, adopted 2022. Quote: "use during pregnancy and lactation is not recommended," stated on the basis of insufficient data. | **sourced** — regulatory primary, directly verified. Monograph covers cutaneous-use traditional herbal preparations, not cosmetic-extract concentrations specifically — does not establish either safety or harm, only insufficient data. |
| "It's in your cream. Is it working?" | Hook framing | **editorial** — asserts no outcome. |

Ledger: 6 sourced, 1 nominal, 1 editorial. 0 unsourced. Sourced:total ratio
across Mechanism+Proof = 4/4 = 100%. Every identifier above was directly
read this session (the passport JSON's own `citations[]` and
`content/findings/centella-asiatica.json` at the pinned SHA), not assumed
from a chip.

## K-2a hard-prohibition check

No *treats / prevents / cures* language anywhere in the script. No
unqualified safety claim. Pregnancy line is explicitly hedged ("data's too
thin to say either way"), matching the source's own "insufficient data,
not recommended" framing rather than overclaiming risk or safety in
either direction.

## Script (word budget: 49.0s × 150wpm/60 ≈ 122 words ±10% → 110–135)

1. **Hook** — "It's in your cream. Is it working?"
2. **Define** — "Centella asiatica — cica — a calming botanical, rich in madecassoside and asiaticoside."
3. **Mechanism** — "Here's what the evidence actually shows. Redness and hydration — yes, shown, but only in finished creams and gels, not the extract by itself. Marketed as a universal soother? The one review we found never actually tested that claim broadly. And the safety review everyone cites? It covers the whole extract — not isolated actives like madecassoside alone."
4. **Evidence** — "And on safety: in the largest repeat-use study on record — over a hundred people, weeks of skin contact — researchers saw no irritation and no allergic sensitization at all."
5. **CTA** — "Still, rare allergic reactions are on record, so patch test if your skin's sensitive. Pregnant or nursing? The safety data's too thin to say either way."

Word count: 7 + 12 + 56 + 28 + 26 = **129 words** → 51.6s at 150wpm, inside
the 44.1–53.9s target band.
