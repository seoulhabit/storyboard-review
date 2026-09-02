# Story brief — how to repair skin barrier

Source material: `videos/centella-tiger-grass/{BRIEF.md, STORYBOARD.md, frame.md}`.
Format **short** 1080×1920 · target 45 s, actual **44.320 s** (measured VO) ·
presenter **kinetic-type** (S-3 selected moving-diagram; re-fired, see the ledger) ·
voice `SAz9YHcvj6GT2YYXdXww`.

## Spine

| Section | Content | Status |
|---|---|---|
| Hook | Is the viewer's skin sensitive, or is the barrier damaged? Asked, not asserted. | grounded |
| Misconception | Reaching for something gentler while continuing to exfoliate. | grounded |
| Mechanism | Centella identity → four compounds → madecassoside as primary active → inflammation/fibroblast account. | grounded in the input, **entirely unsourced** |
| Proof | — | **`[UNGROUNDED]`** — no Centella source records exist in this system; `[S1/S-5]` drops it rather than fabricate |
| Application | Stop over-exfoliating; cica daily on damp skin. | grounded |
| Recap | Folded into Application (short). | — |

## §Sourcing — the `[K-1]` claim table

Shape borrowed from `videos/peeling-not-progress/frame.md`, the repo's exemplar.
**No claim entered S4 unclassified.** Unclassifiable defaults to `unsourced`.

**Source resolution pass, 2026-09-02** — `sources.json`. Three candidate sources
were fetched directly and all three resolved. A fourth, "the 4-trial PRISMA
review of *topical* centella", **was not found to exist** and may not be cited.

| id | Source | Resolved | Scope |
|---|---|---|---|
| **S1** | PMID 36918311 — "The effect of Centella Asiatica cream on scar development in patients who underwent open carpal tunnel release surgery." | ✅ | 1 % centella cream on the **wrist**, 6 months post-carpal-tunnel-release. Surgical scar outcomes. |
| **S2** | PMID 35328954 — "A Systematic Review of the Effect of [Centella asiatica] on Wound Healing" | ✅ | 4 trials, PRISMA. **"Oral or topical"** — two of the four trials are oral. |
| **S3** | CIR, "Safety Assessment of Centella asiatica-derived Ingredients as Used in Cosmetics" — Status **Final Report**, Release Date **July 10, 2015** | ✅ | Cosmetic **safety** only. Full-text scan: `barrier` 0 hits, `primary active` 0, `sensitive skin` 0, `stinging`/`tightness`/`flaking`/`exfoliat` 0 each. |
| — | "4-trial PRISMA review of *topical* centella" | ❌ **not found** | Two PubMed searches returned no such review. **May not be cited.** |

| # | On-screen | Class | Backing | supporting_sentence_verbatim |
|---|---|---|---|---|
| R1 | "Is your skin actually sensitive?" / "Or is the barrier damaged?" / "TWO DIFFERENT PROBLEMS" | **editorial** | — | A question asserts nothing. |
| R2 | "You reach for something gentler and keep exfoliating anyway." | **editorial** | — | Describes viewer behaviour; asserts no outcome. |
| R3 | "Stinging, tightness, flaking / are commonly described as / barrier damage. / Not a skin type." | **unsourced** | none | No sentence in S1/S2/S3 addresses what these symptoms indicate. S3 scan: `stinging` 0, `tightness` 0, `flaking` 0, `sensitive skin` 0, `barrier` 0. |
| R4 | "Centella asiatica" / "병풀 · tiger grass" / "BOTANICAL EXTRACT" | **nominal** | **S2** (partial) | "[Centella asiatica], also known as Gotu Kola, Bua-bok, Tiger grass, or Indian Pennywort [,], is an herbaceous perennial plant member of the[Apiaceae] family, also known as[Umbelliferae]." The Korean name 병풀 is not in any of the three sources; nominal identity, renders plainly. |
| R5 | "Asiatic acid · Asiaticoside · Madecassoside · Madecassic acid" / "FOUR MAIN TRITERPENES" | **nominal** | **S2** | "The main triterpenes found in[Centella asiatica], also known as centelloids, are asiatic acid (AA), asiaticoside (AS), madecassoside (MS) or brahminoside, and madecassic acid (MA) or brahmic acid [,,]." Re-ordered on screen to the source's own order; no compound is ranked. |
| ~~R6~~ | ~~"Madecassoside" / "DESCRIBED AS PRIMARY ACTIVE"~~ | **CUT** | — | **Cut by operator instruction.** No source ranks madecassoside first, and both efficacy-bearing sources name a different compound (S2 → asiaticoside "one of its more active compounds"; S3 → asiatic acid "one of the active constituents", `primary active` 0 hits). Cut rather than corrected: correcting it to name another compound would be a new claim, not a sourcing act. |
| R7 | "PMID 35328954" / "A 4-trial review reports / an anti-inflammatory effect — / reduced IL-1β, IL-6, TNF-α" / "IN WOUND HEALING" | **sourced** | **S2** | "[Centella asiatica] has shown an anti-inflammatory effect observed by the reduction in Interleukin-1β (IL-1β), Interleukin-6 (IL-6) and Tumour Necrosis Factor α (TNFα) [,,], as well as prostaglandin E2 (PGE2) [,], and cyclooxygenase-2 (COX-2) []." **Re-scoped by operator instruction.** The fibroblast and barrier limbs were **removed, not softened** — S2's only fibroblast sentence is proliferation after asiaticoside, S3's has asiatic acid *inhibiting* collagen in keloid fibroblasts, and `barrier` is 0 hits in S3. Trial count "4-trial" is itself sourced: "Four studies [,,,] on[Centella asiatica] were included in the systematic review ()." |
| R8 | "That review is about wound healing, / not daily skincare. / The routine advice below / has no source record here." / "SCOPE NOTE" | **editorial** | — | **Rewritten.** The previous wording ("No source record exists in this system") became **false** the moment R7 gained a citation. It now states the true position: one claim is sourced but out of context, the rest are not. |
| R9 | "The usual advice: / stop over-exfoliating. / Cica daily, on damp skin." | **unsourced** | none | None of the three addresses exfoliation, routine placement, or damp-skin application. S1 is a 6-month post-surgical wrist protocol; S2's topical arms are burn and acne trials; S3 is safety. |

**Counts after cut + source.** nominal 2 · **sourced 1** · unsourced 2 · editorial 3 · illustration 0.

**`[K-2a]` — none triggered.** Nothing cut on prohibition grounds. (R6 was cut on
operator instruction, not by `K-2a`.)

**`[K-2b]` CLEARS.** Mechanism + Proof: **sourced 1, unsourced 0** → `unsourced ≥
sourced` is `0 ≥ 1` = false. The disclosure-forward requirement lifts. R3 and R9
remain unsourced and flagged, but they sit in Misconception and Application, which
`K-2b` does not count.

**ESCALATE — recorded, not substituted:**
1. **S1 is off-topic for every row.** Post-operative carpal tunnel release,
   wrist and hand, surgical scar scales. Nothing on facial skin, barrier,
   inflammation signalling, constituent ranking, or a routine.
2. **S2's scope does not match the brief.** Asked for a *topical* 4-trial PRISMA
   review; S2's inclusion criterion is "Oral or topical treatment", and two of
   its four trials are oral. Recorded with its true scope.
3. **The topical-only 4-trial PRISMA review does not exist** under either search.
4. **R6 may be positively wrong, not merely unsourced.** Both efficacy-bearing
   sources that name a leading constituent name one other than madecassoside
   (S2 → asiaticoside; S3 → asiatic acid). Correcting it to match would be
   changing the claim to fit a source, which `K-1` forbids without a re-cut.
