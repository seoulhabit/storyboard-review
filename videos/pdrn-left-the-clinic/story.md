# Story input — pinned per R-3 (WO-FVC-005)

**Source (R-3):** `https://seoulhabit.com/ingredient/pdrn/`, pinned to
site repo `github.com/seoulhabit/seoulhabit-learn` commit `cacff81` (clean at
that SHA — confirmed this session). Route: `src/routes/passports.ts`'s
`/ingredient/${handle}`. `videos/_queue.yaml` lists this slug with
"citations: 2, findings: 1" — **stale**, per the queue file's own header
warning that counts are not auto-refreshed. Read fresh at `cacff81`:
`content/ingredients/pdrn.json` + `content/findings/pdrn.json` actually carry
**17 findings, 15 verified `F-PASS`**.

## Plain-English (site's own copy, `plain_english`)

PDRN (polydeoxyribonucleotide) is a repair-focused ingredient made from
purified salmon DNA fragments. In skincare it's used to support hydration,
skin recovery, and a smoother, firmer-looking surface. It's often paired
with hyaluronic acid and peptides in "booster" toners and serums.

## Quick facts (site's own copy, `quick_facts`)

- A repair ingredient derived from purified salmon DNA fragments.
- Supports hydration, recovery, and a firmer-looking surface.
- Often paired with hyaluronic acid and peptides in booster toners.
- Not vegan — it is animal (fish) derived.
- Those with a known fish allergy may prefer to patch-test, though topical
  PDRN is highly purified.
- No verified topical safety assessment is on file for this ingredient yet
  on the site's own record — that reflects verification status, not a
  formal all-clear.

## The story this video tells (brief's own arc)

Fascination → suspicion → measured verdict. PDRN is neither a miracle nor a
scam; the investigation is into what changed when the ingredient moved from
an injection to a bottle. Opening question: "If PDRN became famous because
it was injected into the skin, what happens when you simply spread it on
top?"

## Mechanism / what the evidence actually shows

- **Origin.** Commercially available PDRN is typically extracted from salmon
  reproductive tissue (finding C13, *Int J Biol Macromol* 2024, PMID
  39486723): "extracted mainly from salmon." The registered INCI name is
  `Sodium DNA` (finding C12, COSMILE Europe directory), with listed origins
  spanning animal, synthetic **and plant** — one INCI label can legitimately
  cover chemically different materials.
- **Clinical/injectable route.** A systematic review of RCTs on
  polynucleotide/PDRN skin treatments (finding C8, *Cureus* 2026, PMID
  42572627) found nearly all "skin rejuvenation" trial evidence used
  **injected or microneedled delivery**, not leave-on application to intact
  skin — and explicitly: "no trial meeting a leave-on cosmetic design was
  included in this review." Injected PDRN has also been studied for wound
  healing (finding C4, graft donor-site wounds, high risk of bias per the
  review) and, combined with a topical steroid, for an inflammatory skin
  disease (finding C9, *Dermatol Res Pract* 2013).
- **"Vegan PDRN" is real, not marketing invention.** A small open-label study
  of a **peony (plant)-derived** PDRN alternative (finding C3, *Int J Mol
  Sci* 2025, PMID 41516097, Korean participants) reported no irritation —
  but the study explicitly does not establish "anything about salmon-derived
  PDRN, the dominant commercial form — this plant fraction is chemically
  distinct." A separate review (finding C14, *Biomolecules* 2025, PMID
  39858543) notes "PDRN" and "PN" are used interchangeably in the literature
  for fragments of different molecular weights, "confusion within the
  medical and [cosmetic] communities" the source itself names.
- **One real topical cosmetic trial exists, and it is genuinely informative.**
  A randomized, double-blind, split-face RCT (finding C2/C5/C6/C7/C15,
  PLoS One 2026, PMID 42430369) tested a low-concentration salmon-derived
  PDRN **eye cream** against low-dose retinol in 31 Chinese women aged
  35–55 with self-reported sensitive periocular skin. It was well tolerated
  (C2) and produced **~2× greater improvement** in periocular dermal
  thickness, density, wrinkle appearance and firmness than the retinol
  comparator (C7) — the trial's own authors flag this as possibly transient
  hydration/plumping rather than durable remodeling, and the retinol dose
  used was atypically low. **This is the one topical result that exists —
  the video must not claim topical evidence is absent, only that it is
  thin: one small industry-linked trial, one body site, one comparator.**

## The regulatory beat (brief §3, 3:10–3:50) — sourced, keep it

Korean trade press (7 independent outlets, all reporting the same National
Assembly Health & Welfare Committee disclosure of MFDS data, Rep. Seo
Young-seok/서영석, Sept 2026) reports: **106 PDRN-cosmetic-advertising
violations found by MFDS inspections over the last 4 years** — 2023: 7,
2024: 19, 2025: 39, first half of 2026 alone: 41. **81 of the 106 (76.4%)
were for "advertising liable to be mistaken for a medicine"**; 7 were for
claiming functional effects not from an approved functional ingredient; 18
were general consumer-deception risk. 11 led to formal administrative
action. Named driver: the boom around the injectable "Rejuran" (리쥬란)
treatment. No PDRN-specific finding in the site's own passport corpus covers
this directly — it is sourced from the trade-press reporting above, read
directly, not from an internal record.

## Application — what a buyer can actually check

1. What is the actual ingredient name on the full ingredient list — `Sodium
   DNA`, salmon DNA, or a plant-source name?
2. Is the source identified (salmon vs. plant vs. unspecified)?
3. Does the brand disclose concentration or formulation/delivery technology?
4. Was the *finished topical product* tested on people, or are the claims
   borrowed from injectable research? (Per finding C8: for skin
   rejuvenation claims specifically, borrowed-injectable is still the norm.)

## Proof / the caveat

- The one topical RCT (C5, C6) excluded pregnancy/lactation and known
  PDRN/retinol allergy as screening criteria — evidence that trial
  designers treated both as real possibilities to control for, not evidence
  of actual incidence (C6's own `does_not_establish`: "How common PDRN
  allergy is, or that any confirmed case exists").
- This ingredient does not appear on the EU's fragrance-allergen disclosure
  list (finding C17, Reg. (EU) 2023/1545, directly checked) — expected,
  since it isn't used as a fragrance ingredient; this does not extend to any
  other regulatory list.
- A 2024 systematic review of "regenerative aesthetics" broadly (PDRN among
  several other actives, finding C11, PMID 39198280) concludes the field
  overall "lacks the necessary scientific rigour... to be recognized as a
  legitimate medical specialty" — a field-wide judgment, not broken out by
  ingredient, so it supports caution in general rather than a PDRN-specific
  verdict.

## Full findings corpus (for reference, not all scripted)

`content/findings/pdrn.json` at `cacff81` carries 17 findings (C1–C17). This
brief draws the load-bearing ones for the topical-vs-injectable argument;
the `[K-1]` claim table in `01-story-brief.md` cites specific finding ids
for every claim that made it into the script.
