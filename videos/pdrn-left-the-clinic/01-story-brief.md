# 01-story-brief.md — pdrn-left-the-clinic

Source: `https://seoulhabit.com/ingredient/pdrn/`, pinned to `seoulhabit-learn`
@ `cacff81`. `content/ingredients/pdrn.json` + `content/findings/pdrn.json`
at that SHA. `videos/_queue.yaml`'s "citations: 2, findings: 1" for this slug
is stale (the queue file's own header: counts are not auto-refreshed) — the
real corpus at the pinned SHA carries 17 findings, 15 verified `F-PASS`.

## Objective

Answer the brief's own core question: how did PDRN — DNA fragments
associated with injectable Korean skin treatments — become an ordinary
serum ingredient, and can the cosmetic version produce the same result?

## Misconception

That "PDRN" on a label means the injectable evidence transfers to a bottle.
It doesn't automatically, and the brief's own draft came close to
overcorrecting the other way — implying *no* topical evidence exists. One
genuine topical RCT exists (finding C7) and must be represented, sized
correctly: one small, industry-linked trial, one body site (periocular),
one active comparator. Thin evidence is not absent evidence, and the script
must say which.

## Mechanism

Commercially, PDRN is salmon-derived (C13); the INCI is registered as
`Sodium DNA` with origins spanning animal/synthetic/**plant** (C12) — one
label can cover chemically different materials. Nearly all rejuvenation
trial evidence uses injected/microneedled delivery, not leave-on cosmetic
use (C8) — the review that found this explicitly states no leave-on-design
trial was included. A plant (peony)-derived alternative has its own small
study (C3) that explicitly does not transfer to salmon-derived PDRN, the
dominant commercial form.

## Proof

The one topical cosmetic RCT that exists (C2/C5/C6/C7/C15, PLoS One 2026,
PMID 42430369): 31 women, split-face, PDRN eye cream vs. low-dose retinol —
well tolerated (C2), ~2× greater improvement on several periocular measures
than the retinol arm (C7). Real, but the trial's own authors flag possible
transient plumping over durable remodeling, and it is one small
industry-linked trial on one site.

## Application

Four checks a buyer can run without lab access: the actual listed name
(Sodium DNA / salmon DNA / a named plant source), whether the source is
disclosed at all, whether concentration/delivery tech is disclosed, and
whether the specific finished topical product — not the injectable
literature — was tested on people (C8's own finding: for skin-rejuvenation
claims, "borrowed from injectable" is still the norm, not the exception).

## Format decision (S-1) — operator override, ledgered per the WO's own rule

Branch 2 would select **short**: `baseline.yaml formats.short.uploads_90d` =
46 of `corpus.uploads_total` = 48 → 95.8% ≥ 60%. **The brief overrides this
to long** (4:55 target, both formats via F-2's single dual-canvas compile).
Per `S-1`'s own first-of-kind-override note:

1. Ledgered as an override: long, operator override; branch 2 would have
   selected short on 46/48 = 95.8% Shorts.
2. This channel's `curve.*`/`retention.*` figures were all built from Shorts.
   Any comparison of this video's long-form performance against those
   figures is `[UNDERPOWERED]` and must be marked as such at S9, not treated
   as a real benchmark.
3. Format-specific gates (safe-area zones, cadence ceilings, canvas
   constants) must be re-pointed to the 16:9 long-form set at S7, not
   inherited from the channel's Shorts-tuned defaults — "a portrait
   gate against a landscape render reports a silent clean pass" is the
   named failure mode to avoid.
4. `[S3/P-3]` changes: long-form generates and scores a thumbnail at S3,
   where Shorts use frame 0 — both apply once both canvases compile.
5. `S-1`'s own advice ("prove the format on a short vertical slice before
   committing a full runtime") is **not** followed by this run — flagged as
   an open ruling for Kim (see `00-decision-ledger.md`), not decided here.

## Target length (S-2)

Long clamp is 4:00–12:00 [default 6:30]; the brief's 4:55 sits inside it.
**Contract mismatch, not a rule failure**: `templates/T6.json` declares
`chapters_min: 4, chapters_max: 6`, which at the compiler's own per-scene
ceilings (5.0s; 8.0s for `ShEvidence`/`ShCompare`) lands near 3:00–3:30 even
with D5 splitting — short of 4:55. Filed to Design as §A3 of
`videos/_system/REQUESTS/2026-09-07-imagery-and-longform.md`, not resolved
by this run.

## Presenter (S-3)

Kinetic type, matching the design system's established presenter for
vocabulary/definition-and-evidence content (same as the T3/T4 synthetic-
fixture precedent and the `centella-asiatica` pilot) — **contingent on
Design's A1 ruling**. If Design declines to extend the system, this is the
only presenter option available regardless; if Design extends it, the
brief's own cinematography (place/object-driven) may warrant a different
presenter choice, to be re-decided once the new components exist.

## Voice (S-4) — brief closes this, logged as a fence override

Per the brief's own §0, VO = Higgsfield, voice **Kimberly**
(`674b71b8-1d2e-4087-8567-d1f53c0b9f3c`, `voice_type=element`), model
`seed_audio`, measured at 2.4 credits per 60-word block, already generated
live for the reference block in §4. **This is a `H-0` tool-fence override,
not a default path** — the skill's own fence lists Higgsfield `generate_audio`
among providers that "are not fallbacks and may not be called," with "a gate
that cannot be passed with a permitted tool halts." The override is
justified in this instance (HeyGen `create_speech` returns HTTP 402
`insufficient_credit` against a separate, unfunded "api" credit pool,
confirmed again this run via `get_current_user`) but is Kim's call to bless
as a standing fence amendment, not this run's to assume silently. Logged to
`videos/_channel/policy-change-proposals.md` — see `00-decision-ledger.md`.

## §Sourcing — the [K-1] claim table

| On-screen chip | Backing | What it actually supports |
|---|---|---|
| "One of Korea's most talked-about skincare ingredients is made from fragments of DNA." | Passport's own `plain_english`/`one_liner` (SeoulHabit Editorial, `last_reviewed: 2026-08-09`) | **nominal** — identity/definition, inherited from the site's own reviewed copy. |
| "If PDRN became famous because it was injected into the skin, what happens when you spread it on top?" | Hook framing | **editorial** — asserts no outcome, poses the video's own question. |
| "Traditionally derived from purified salmon or trout DNA." | Finding C13 — *Int J Biol Macromol* 2024, PMID 39486723. Quote: "extracted mainly from salmon." | **sourced** — direct restatement; "trout" not independently found in this corpus, narrowed to salmon per the source. |
| "Registered under the INCI name Sodium DNA — a label that can legally cover animal, synthetic, or plant sources." | Finding C12 — COSMILE Europe INCI directory. Quote: "Origin/Source Categories 'animal/synthetic/plant'." | **sourced** — regulatory/industry nomenclature listing, directly read. |
| "Nearly all of the clinical evidence for PDRN skin rejuvenation comes from injections or microneedling — not from a cream or serum sitting on top of skin." | Finding C8 — *Cureus* 2026 systematic review of RCTs, PMID 42572627. Quote: "no trial meeting a leave-on cosmetic design was included in this review." | **sourced** — systematic review, directly read; this is the load-bearing evidence-boundary claim. |
| "'Vegan PDRN' — from roses, green tea, or seaweed — is a real, studied category, not just a marketing label." | Finding C13 (alt-source versions proposed) + Finding C3 — *Int J Mol Sci* 2025, PMID 41516097, peony-derived PDRN, Korean participants, no irritation reported | **sourced** — real study exists; C3's own `does_not_establish`: results do not transfer to salmon-derived PDRN, the dominant commercial form. Scripted with that limit stated, not implied as equivalence. |
| "Two materials from different organisms can share the name PDRN and not behave the same way." | Finding C14 — *Biomolecules* 2025, PMID 39858543. Quote: "the interchangeable use of the terms 'PDRN' and 'PN' ... has led to considerable confusion within the medical and [cosmetic] communities." | **sourced** — single author group's proposed naming distinction, not an adopted standard; scripted as "researchers argue," not as settled fact. |
| "There is one real human trial of a topical PDRN cosmetic — and it found a real effect." | Findings C2 (tolerability), C7 (efficacy vs. retinol) — PLoS One 2026, PMID 42430369, RCT, split-face, n=31 | **sourced** — the correction this run's own review made to the brief's draft framing (see Misconception, above). Scripted with its own limits: one small industry-linked trial, one body site, one comparator dose. |
| "Korean regulators have logged 106 cosmetic-advertising violations tied to PDRN in the last four years — 81 of them for making the product sound like a medicine." | Korean trade press (7 independently corroborating outlets — 약사공론, 헬스경향, 지디넷코리아, 의학신문, 포커스경제, 저널25, 기호일보/다음뉴스), all reporting a National Assembly Health & Welfare Committee disclosure of MFDS inspection data (Rep. Seo Young-seok/서영석, Sept 2026): 2023: 7 → 2024: 19 → 2025: 39 → H1 2026: 41; 81/106 (76.4%) "advertising liable to be mistaken for a medicine"; 11 administrative actions. | **sourced** — read directly across multiple independent outlets reporting the identical dataset (not a single unread press link); no primary MFDS/National Assembly URL located, disclosed as such. Survives K-1's "an identifier you have not read is not a source" test because the actual figures were read and cross-checked, not copied from one unverified chip. |
| "The question isn't whether PDRN has biological potential — it's whether this specific topical formula has shown a benefit on intact skin." | Restates C8 + C7's own scope limits together | **editorial**, directly supported by two already-sourced findings above — no new factual claim introduced. |
| Four-question buying checklist (name / source / concentration disclosed / topical-vs-injectable evidence) | Restates C8's own finding in checklist form | **editorial/application** — no new claim, a reframing of C8 and C12 as consumer actions. |
| "It's also been studied for an inflammatory genital skin disease — injected, alongside a steroid, under medical supervision." | Finding C9 — *Dermatol Res Pract* 2013, PMID 24489537. Quote: "intradermal administration of PDRN, associated with CP 0.05% cream, seemed to be associated with a clinical improvement of lichen sclerosus better than CP used in single th[erapy]." | **sourced** — small, non-blinded comparison in diseased genital skin under medical supervision; does not establish anything about cosmetic or topical-only use, stated as such in the script. |
| "In rats, injected PDRN sped healing after laser resurfacing." | Finding C10 — *J Cosmet Laser Ther* 2016, PMID 27762652 | **sourced** — animal (rat) study only; does not establish human outcomes, not applicable to leave-on skincare. |
| "A field-wide review of 'regenerative aesthetics' — PDRN, stem cells, exosomes together — found the science still lacks rigor." | Finding C11 — *Aesthetic Plastic Surgery* 2024, PMID 39198280 (PRISMA systematic review). Quote: "lacks the necessary scientific rigour and regulatory compliance to be recognized as a legitimate medical specialty." | **sourced** — pooled judgment across many interventions, not broken out by ingredient; scripted as a general-caution finding, not a PDRN-specific verdict. |
| "In animals, a PDRN blend reduced UV pigmentation — but three actives were combined, not PDRN alone." | Finding C16 — *Molecules* 2022, PMID 35209068 | **sourced** — animal model, multi-ingredient combination (PDRN + vitamin C + niacinamide) via microneedling; does not isolate PDRN's own effect or apply to a leave-on serum. |
| "PDRN isn't on the EU's fragrance-allergen disclosure list — expected, since it isn't marketed as a fragrance ingredient." | Finding C17 — Official Journal of the EU, Reg. (EU) 2023/1545, primary regulatory text directly checked (search for "Sodium DNA," "DNA," "polydeoxyribonucleotide," "PDRN" — none appear) | **sourced** — primary regulatory absence check; does not establish absence from any other EU regulatory annex or list, only this specific amendment. |
| "PDRN did not become meaningless when it left the clinic. It became a different question." | Verdict framing | **editorial** — asserts no outcome, closing statement. |

**Ledger:** 13 sourced, 1 nominal, 4 editorial (2 of which restate already-
sourced findings, introducing no unsourced claim). **0 unsourced.**
Sourced:total ratio across Mechanism + Proof = 5/5 = 100%. Every finding id
above was read directly from `content/findings/pdrn.json` at `cacff81` this
session (not assumed from the queue file's stale chip counts), and the
regulatory claim was corroborated across seven independent outlets before
being classed `sourced` rather than `unsourced`.

## K-2a hard-prohibition check

No *treats / prevents / cures* language. No unsourced safety claim — the
allergy/pregnancy material in the source corpus (C6's `does_not_establish`)
is deliberately **not** scripted as a safety claim in either direction; this
brief's own script stays on the efficacy-evidence question, not safety. No
unsourced quantity — every number on screen (106, 81, 76.4%, "~2×", 31, 17)
traces to a finding or the regulatory reporting above. No comparative
superiority claim beyond the C7 finding's own stated comparison (PDRN vs.
retinol, as measured in that one trial, not generalized). No absolute
language (*guaranteed, proven, always*).

## K-2b ratio check

Unsourced = 0 in both Mechanism and Proof. Sourced ≫ unsourced. **Does not
fire** — this video presents as a real explainer of how the evidence stands,
not disclosure-forward.

## Script — not written this pass

Per this run's own scope (`00-environment.md`), S4 (script) does not run
until Design's A1/A3 rulings land — the presenter and available components
depend on that answer, and a script written against components that may not
exist would need a full rewrite either way. The typographic beat mapping in
`00-decision-ledger.md` stands in for S4 as the structural argument this
run is prepared to build from, whichever way Design rules.
