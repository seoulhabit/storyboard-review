# Claim ledger — snail-mucin-medical-secret-v2

Written before the script, per `[K-1]`. **This project has no project-skill truth rules** (see
`00-environment.md` of the v1 run — `snail-mucin-medical-secret/CLAUDE.md` is the generic
HyperFrames template), so `decision-policy.md` §Claims (`K-*`) applies as the **floor**,
undelegated — and, per this run's explicit brief, is no longer overridden by a `VO_MODE: verbatim`
instruction the way it was in v1.

**Why this document exists at all.** v1's `BRIEF.md` (lines 54–64) records that an earlier,
evidence-tuned build of this same story was rejected by a `/goal` Stop-hook for not matching the
user's exact pasted script — and the rebuild that followed deleted the citation apparatus wholesale
rather than keeping it alongside verbatim narration. The result shipped with **zero** citation
identifiers anywhere in the project and six `[K-2a]`-hard-prohibited claims on screen. This
document is the correction, and it is written under an explicit instruction from the current user
to prioritize evidentiary rigor over the original wording.

## Sources actually read (not just cited)

PMC and PubMed are not fetchable over plain HTTP from this session (reCAPTCHA / cookie gate). All
four sources below were retrieved and read via the PubMed MCP (`get_article_metadata`,
`get_full_text_article`) or, for the one non-PubMed document, `WebFetch` directly against its host.
**According to PubMed** for the three PubMed-indexed sources.

| id | Full citation | What it actually is |
|---|---|---|
| **SRC-1** | Ledo E, de las Heras ME, Ledo A. "Treatment of acute radiodermatitis with Cryptomphalus Aspersa Secretion." *Radioprotection* 23(VII), July 1999, pp. 34–38. | Controlled clinical trial, n=100 (50 treatment / 50 excipient-only control), acute radiodermatitis. "Statistically significant clinical improvement in erythema, itching and burning pain... at first week and one month." Single trial, 1999, not independently replicated since (none found in this search). Does **not** establish long-term efficacy beyond the follow-up window, mechanism, or comparison to standard treatment. |
| **SRC-2** | Fabi SG, Cohen JL, Peterson JD, Kiripolsky MG, Goldman MP. "The Effects of Filtrate of the Secretion of the Cryptomphalus Aspersa on Photoaged Skin." *J Drugs Dermatol* 12(4):453-7, 2013. PMID [23652894](https://pubmed.ncbi.nlm.nih.gov/23652894/). | 2-centre, double-blind, randomized, **split-face**, 14-week trial, n=25, moderate-severe facial photodamage. 8% SCA emulsion + 40% SCA serum vs placebo, contralateral sides. Periocular rhytides improved significantly (P=.03) at 12 wk. Authors' own text: patients "did not report a significant difference in the quality of their skin." Tests one specific branded filtrate (SCA®), not snail mucin generically. |
| **SRC-3** | Lim VZ, Yong AA, Tan WPM, Zhao X, Vitale M, Goh CL. "Efficacy and Safety of a New Cosmeceutical Regimen Based on the Combination of Snail Secretion Filtrate and Snail Egg Extract to Improve Signs of Skin Aging." *J Clin Aesthet Dermatol* 13(3):31-36, 2020. PMID [32308795](https://pubmed.ncbi.nlm.nih.gov/32308795/) / PMC7159309. | Single-centre, double-blind, randomized, **vehicle-controlled**, 3-month trial, n=50 (30 active / 20 vehicle), women 45–65. **Both** groups showed significant improvement in fine lines and wrinkles; active group additionally improved roughness, firmness, elasticity, TEWL. One co-author (Vitale M) is affiliated with Cantabria Labs (Madrid) — a manufacturer, not an independent academic site. Authors' own conclusion: "Larger randomized, controlled studies are needed to confirm our results." |
| **SRC-4** | Di Filippo MF, Dolci LS, Bonvicini F, Sparla F, Gentilomi GA, Panzavolta S, Passerini N, Albertini B. "Influence of the extraction method on functional properties of commercial snail secretion filtrates." *Scientific Reports* 14:22053, 2024. PMID [39333225](https://pubmed.ncbi.nlm.nih.gov/39333225/) / PMC11437072, DOI [10.1038/s41598-024-72733-0](https://doi.org/10.1038/s41598-024-72733-0). | Lab comparison of **four commercial snail secretion filtrates** from three Italian retailers, differing by extraction method (manual / citric-acid stimulation / lactic-acid stimulation). Measured composition directly: dry residue 0.8–2.48% by weight (i.e. **97.5–99.2% water**), protein content varying 0.81–1.80 mg/mL depending on method, distinct SDS-PAGE protein profiles per method. States plainly that "all these methods **are claimed to be** cruelty free for the animal" — the paper is relaying a retailer/industry claim, not independently verifying animal welfare. Also: glycolic acid and allantoin were "believed to be the essential component" historically, but "it has been recently demonstrated that slime has a greater effect than that of the individual molecules" — i.e. the paper does not support attributing a specific cosmetic mechanism to either molecule in isolation. Cytotoxicity/antibacterial assays are **in vitro on Vero cells only**, not human skin. |

No source was found — after an explicit search — for the "humectant on dry skin pulls hydration out
of deeper layers" mechanism the original script asserted, or for the second pipeline's
lymosine/cryptosine molecule split (that split traces to a single non-DOI'd secondary source,
`Wargala et al.`, per `seoulhabit-video/content/r03-snail/script.json`, and is **not used here**).

## Claim table

Classification per `[K-1]`: **nominal** (identity, no effect) · **sourced** (real identifier,
actually read) · **unsourced** · **illustration** (drawn, unmeasured) · **editorial** (opinion,
no outcome asserted). `[K-2]` governs what may render and how; `[K-2a]` lists what may never
render regardless of flag.

| # | On-screen / VO chip | Backing | What it actually supports | Class | Renders as |
|---|---|---|---|---|---|
| C1 | "A 1999 study on radiation-damaged skin" | SRC-1 | A real, single, unreplicated controlled trial on symptom relief in radiodermatitis — not a general healing claim | sourced | `Radioprotection · 1999` chip |
| C2 | "One specific extract... tested in small clinical trials" | SRC-2, SRC-3 | Two real small RCTs of one branded filtrate exist | sourced | `J Drugs Dermatol · 2013` / `J Clin Aesthet Dermatol · 2020` chips |
| C3 | "Most snail-mucin products on the shelf have not [been tested]" | absence, confirmed by search | No RCT found testing a generic/unbranded consumer snail-mucin product | sourced (the claim is about an *absence* of evidence, itself verified) | plainly, no flag needed — this is the honest gap, stated as such |
| C4 | "Snail secretion is over 97% water" | SRC-4 Table 1 (dry residue 0.8–2.48% as received) | Directly computed from the paper's own measured dry-residue range | sourced | `Sci Rep · 2024` chip |
| C5 | "The rest — proteins, glycolic acid, allantoin" | SRC-4 | Composition identity; no effect asserted | nominal | plainly, no chip |
| C6 | "The mix changes with how it's collected" | SRC-4 | The paper's central, directly measured finding (SDS-PAGE, protein content, pH all differ by method) | sourced | `Sci Rep · 2024` chip |
| C7 | "Two small trials tested that one specific patented extract — not snail mucin generally" | SRC-2, SRC-3 | Both trials test SCA®, a named branded filtrate | sourced | plainly, restates C2 |
| C8 | "In the smaller trial, fine lines improved" | SRC-2 | P=.03 on periocular rhytides at 12 wk | sourced | chip as C2 |
| C9 | "In the larger one, the placebo cream worked almost as well" | SRC-3 | Both arms improved on fine lines/wrinkles; only some secondary measures (roughness, firmness, TEWL) differed | sourced | chip as C2 |
| C10 | (on screen, small print) manufacturer-affiliated co-author note | SRC-3 author affiliations | Verifiable directly from the paper's own author list | sourced | small end-card/description note, not mid-frame |
| C11 | "Collection methods vary — hand stimulation or acid sprays" | SRC-4 (methods section) | The paper's own described methods across its four samples | nominal | plainly |
| C12 | "Companies call the process cruelty-free. That claim comes from the companies, not an independent study" | SRC-4's own framing ("are claimed to be cruelty free") | The paper explicitly relays this as an industry claim it did not test | sourced (about the *evidence*, not the animals) — and satisfies `[K-2a]`'s test (harm from getting it wrong) by asserting **nothing** about actual welfare either way | plainly, editorial framing |
| C13 | "Follow the product's own directions" | n/a | Instructional, no efficacy asserted | editorial | plainly |
| C14 | "Some people prefer damp skin first, for texture" | none found | A texture preference with no located study | unsourced | **only** under `[K-2]`'s three conditions: attributed ("some people prefer"), flagged concurrently (`UNSOURCED` pill, muted ink), and not hard-prohibited (it is a low-risk usage preference for a non-active, not a safety claim — matches the `K-2a` carve-out for "apply the moisturiser daily"-class instructions) |
| C15 | "No study backs the 'it pulls your hydration out' warning" | absence, confirmed by search | The claim's absence, not its presence — stated as a correction, not hedged as if it might be true | sourced (about the *absence* of evidence) | plainly, as the explicit myth-correction beat |
| C16 | "An interesting ingredient, not medicine, not magic" | n/a | Editorial verdict, asserts no outcome | editorial | plainly |
| C17 | CTA — "Would you try an animal-derived skincare ingredient?" | n/a | Opinion prompt | editorial | plainly |

### `[K-2b]` ratio check — Mechanism (ch3) + Proof (ch4)

Mechanism (C4–C6): 2 sourced (C4, C6), 1 nominal (C5), 0 unsourced.
Proof (C7–C10): 4 sourced, 0 unsourced.
**Sourced ≥ unsourced in both sections** — `disclosure-forward` does **not** fire. This video
presents as a real (if narrow) explainer, because doing the sourcing work found real evidence to
report, rather than as a video about the absence of evidence.

### `[K-2a]` hard prohibitions — cut, not hedged

None of the retained claims above trip a hard prohibition. For the record, everything v1 shipped
that would have:

| v1 wording | Prohibition | Disposition in v2 |
|---|---|---|
| "a bizarre, miraculous cure" | absolute language | cut — SRC-1 restated as "statistically significant improvement," never "cure" |
| "instantly heal their own bodies" | absolute + rate claim | cut — not used; the biological self-repair framing is dropped entirely, not hedged |
| "massive doses of Hyaluronic Acid" | unsourced quantity | cut — no quantity asserted for any named component |
| "Allantoin to heal wounds" | treats a named condition | cut — allantoin appears only nominally (C5), no effect claimed |
| "Zero harm, zero stress" | unsourced absolute safety claim | cut — replaced with C12, which asserts nothing about actual welfare |
| "it panics and pulls hydration out of the deep layers of your skin" | unsourced adverse-effect mechanism | cut, and actively corrected (C15) rather than merely dropped |
| on-screen "CRUELTY-FREE" chip (v1, no VO backing at all) | unsourced safety/welfare claim, and STORYBOARD.md's own note flagged it as stronger than the VO | cut entirely |

## `[K-5]` — envelope carries the sourcing posture

The publish envelope (not produced by this `render`-adjacent build pass, but noted for whoever
writes it) must state in its first three lines that C1 is a single 1999 trial, C8/C9 test one
named branded extract rather than snail mucin generically, and C10's manufacturer affiliation.
