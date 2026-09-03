# Story brief — kbeauty-label-trap

| Field | Value | Rule |
|---|---|---|
| Format | **long, 16:9, 1920×1080** | `[S1/S-1]` — operator-directed; see §Format override |
| Target length | **~300s nominal script; measured VO is the real clock** | `[S1/S-2]`, within the 4:00–12:00 clamp; operator decision (AskUserQuestion, pre-run): do not pad to hit 5:00 |
| Presenter | **moving diagram** | `[S1/S-3]` — 5 of 6 sections are mechanism explainers |
| Voice | **single narrator** — Kimberly (`674b71b8-1d2e-4087-8567-d1f53c0b9f3c`) | `[S1/S-4]`; already the channel's standing narrator per `baseline.yaml`, and the operator's explicit ask |
| fps | 30 | `[S6/A-4]` — no fast counters |
| Route angle | `concept` | `[S1/S-7]`: six-section spine with a named wrong belief |
| `VO_MODE` | `use it verbatim` **except** the hook/misconception restructure and `[K-3]` rewordings below | script supplied; every deviation logged in §Rewordings |

---

## §Format override — `[S1/S-1]`

Long 16:9 is operator-directed, not derived from the baseline (which is
46-of-48-uploads Shorts, 88.1% of views from the Shorts feed). This channel
does have long-form prior art — `ectoin-survival-molecule` (340.2s) and
`hyaluronic-acid-vs-filler` (160.0s) — so the "prove it on a vertical slice
first" clause does not apply. But both prior long-form pieces are **private**,
so `baseline.retention.avg_view_pct_long: 43.07 (n=2)` is not usable. **Every
retention/curve comparison in this run is `[UNDERPOWERED]`.** This will be the
channel's first *public* long-form retention data point (see `08-readout-schedule.md`).

## §The six-section spine — restructured hook, not a cut

The supplied hook (0:00–0:28, 6 sentences + the passport thesis, 74 words)
runs ~28s at the brief's 138–145 wpm, against `[S4/S-6]`'s **hard 20s Hook
cap**. Operator decision (AskUserQuestion): trim to ≤20s by **restructuring**,
since the passport-thesis sentences are themselves the stated wrong belief
the Misconception section needs and didn't otherwise have an explicit
sentence for — this is a net fix, not a loss.

**Hook (first 6 sentences only, 46 words, ~19–20s at 138–145wpm):**
> These two serums make the same promise. Both put cica on the front. Both
> have almost the same ingredient list. One may be a thoughtful formula. The
> other may be expensive green water. And from the front of the bottle, you
> cannot tell which is which.

On-screen: `SAME HERO. DIFFERENT FORMULA.` HyperFrame direction unchanged
(droplet, ripple, bottles, CICA emboss, ribbon lists, leaderboard fracture).

**Misconception (passport thesis, moved here + original promise beat, 61
words, ~25–26s):**
> Here is the uncomfortable truth: an ingredient list is not a scorecard. It
> is a passport. It tells you who entered the formula — not how well they
> work together. Once you know what a label can — and cannot — prove, you
> stop chasing hero ingredients and start asking better questions. Five
> questions, in fact. At the end, we will put both bottles through the test.

The `IDENTITY ONLY` vermilion stamp and `FIVE QUESTIONS. ONE VERDICT.` moves
land here together — both were already Misconception-adjacent content, now in
the section that structurally owns them. The wrong belief this section states
and corrects: *the list itself is a scorecard you can rank formulas by* →
*it's an identity roster, not a performance measure.* `[S1/S-5]` spine
completeness: **6 of 6 grounded**, 0 `[UNGROUNDED]`, 0 fabricated — this
restructure is what closes the one real gap (Misconception previously had no
explicit wrong-belief sentence, only a seals tease).

Q1–Q5 and the reveal/landing are unchanged from the supplied script; each is
individually well under any section's max, so no further trims needed.

| Section | Content | Nominal window |
|---|---|---|
| Hook | Two-bottle mystery (trimmed) | 0:00–~0:20 |
| Misconception | Scorecard→passport thesis + 5-question promise | ~0:20–~0:46 |
| Mechanism | Q1 order · Q2 extract version · Q3 vehicle | ~0:46–~2:54 |
| Proof | Q4 evidence distance | ~2:54–~3:38 |
| Application | Q5 boundary | ~3:38–~4:14 |
| Recap + end | Reveal callback + brand landing (end scene 8–20s) | ~4:14–~4:41 |

All times above are **nominal** — `[S5/C-1]` re-derives every real boundary
from `vo-timing.json` at S5; nothing here is hand-typed into the beat sheet.

---

## §Sourcing — the `[K-1]` claim table

Every identifier below was **fetched and read live this run** (FDA, EU Article
19, MFDS via WebFetch; the two PubMed reviews via PubMed MCP `get_article_metadata`,
abstracts read in full) — "an identifier you have not read is not a source."
Chips render `FDA · 21 CFR 701.3` / `EU · Reg. 1223/2009 Art. 19` / `Journal ·
Year`. No PMID and no internal record id reaches a frame.

| # | Claim (as it will render) | Class | On-screen chip | Backing — verified |
|---|---|---|---|---|
| C1 | Two serums, same promise, near-identical lists, can't tell from the front | **illustration** + editorial | `[Authored, illustrative — not a claim]` on bench scenes | Fictional bottles, stated hypothetical throughout; no real brand named. Cleared against `[K-2a]`'s comparative-superiority bar below. |
| C2 | A list is not a scorecard; it is a passport — who entered, not how well they work together | editorial | none | Metaphor/framing, asserts no measurable outcome. |
| C3 | US: ingredients >1% listed descending by predominance; ≤1% may be in any order | **sourced** | `FDA · 21 CFR 701.3` | Verbatim, fetched fda.gov: *"Ingredients present at a concentration not exceeding 1% may be listed in any order after the listing of the ingredients present at more than 1% in descending order of predominance."* [21 CFR 701.3(f)(2)] |
| C4 | EU: same descending-by-weight rule, same 1% flex zone | **sourced** | `EU · Reg. 1223/2009 Art. 19` | Verbatim, fetched eur-lex: *"listed in descending order of weight... Ingredients in concentrations of less than 1% may be listed in any order after those in concentrations of more than 1%."* [Art. 19(1)(g)] |
| C5 | So the bottom of the list is not a precise concentration chart; rank, not dose | sourced (direct inference from C3/C4) | reuse C3/C4 chips | Both regs confirm order flexibility below the 1% line — the chart-not-precise claim follows directly, no separate source needed. |
| C6 | "Some ingredients work at low levels" | **unsourced** | `UnsourcedFlag` | Searched PubMed for a generic (non-ingredient-specific) source; none returned. A niacinamide-specific hit (4 results) was **rejected** — it would source a specific-ingredient claim, not the general one the script makes, the same overreach the `hyaluronic-acid-vs-filler` ledger flagged when a source didn't cover its full claim. Ships attributed ("some ingredients *are described as* active at low levels") + flag, per `[K-2]`'s three-part unsourced test — not `[K-2a]` hard-prohibited (no specific number, no named ingredient). |
| C7 | "Unless a brand publishes the percentage or meaningful finished-product testing, do not invent a number" | editorial | none | Instructional framing, asserts no outcome. |
| C8 | One INCI name can hide plant part / extraction process / standardization; a study can test one extract while your bottle holds another | **sourced** | `J Cosmet Sci · 2020` | Kongkaew et al., PMID 33413787, *J Cosmet Sci* 71(6):439–454 — systematic review/network meta-analysis of *Centella asiatica* on wrinkles: *"lack of [Centella asiatica] standardization prevents general application."* Read in full via PubMed MCP. |
| C9 | Same passport name, different traveler; "contains cica" is a beginning, not a conclusion | editorial | none | Restates C8's finding as metaphor, no new assertion. |
| C10 | Vehicle (water/gel/cream/emulsion), pH, solvents, emulsifiers, stability, packaging influence what stays intact and reaches the skin | **sourced** | `Int J Cosmet Sci · 2009` | Otto, du Plessis & Wiechers, PMID 19134123, *Int J Cosmet Sci* 31(1):1–19 — *"the vehicle in which a permeant is applied to the skin has a distinctive effect on the dermal and transdermal delivery of active ingredients"*; covers emulsion type, droplet size, emollient, emulsifier, surfactant organization. Read in full. **Coverage caveat**: the review is about *delivery*, not sensory *tolerability* — "what feels tolerable" in the script's own sentence is not literally in this abstract. The sentence is already hedged ("can influence"), so this ships as sourced-with-caveat rather than needing a separate flag; caveat logged here per the same discipline `hyaluronic-acid-vs-filler` applied to a source that didn't cover its whole claim. |
| C11 | Humectants/emollients/occlusives/preservatives/fragrance are part of the formula | nominal | none | Identity/definition, asserts no effect. |
| C12 | Same hero ingredient, different behaviour across two products | sourced via C10 | C10 chip | "Can" behave differently — hedged, follows from C10. |
| C13 | Cell study → mechanism; ingredient human study → potential; neither automatically proves this finished serum works | nominal/editorial | none | Methodological framing (how evidence hierarchies work), not a claim about any specific study or ingredient — "can reveal", "can suggest", "neither automatically proves" are all correctly hedged already. |
| C14 | Evidence has distance; the four forensic questions (tested what / people / how long / measured) | editorial | none | Framing device, asserts no outcome. |
| C15 | "'Gentle' is never universal" — barrier, allergies, routine, frequency all matter | **unsourced**, `[K-3]` reword required | `UnsourcedFlag` | No PubMed source returned for a generic individual-variability claim. `"never"` is absolute-language territory even though the underlying idea (tolerance varies by person) is mundane and non-quantified — **reworded** to *"'Gentle' isn't a fixed property"* (drops the absolute, keeps the point). Not `[K-2a]` hard-prohibited: no specific active, no dose, no named condition. Ships attributed + flagged. |
| C16 | A trustworthy answer names its boundary: patch-test, caution, stop, clinician | editorial | none | Icons are labels ("clinician"), never instructions ("stop using X") — verified at `[K-4]` on rendered pixels. |
| C17 | Reveal: Bottle A's own label claims "eighty percent cica water", no standardization shown, no finished-formula evidence, fragrance a hypothetical reactive-skin viewer avoids; Bottle B: quieter claim, explains formula, publishes a human test, names limits | **illustration** | `[Authored, illustrative — not a claim]` | The "80%" renders **only as Bottle A's own quoted label text inside the scene** (e.g. in quote marks / on the prop bottle itself), never as a video assertion — verified at `[K-4]`. Not comparative superiority (`[K-2a]`): no real named alternative, explicitly hypothetical throughout. |
| C18 | `MORE UNCERTAINTY` (A) / `MORE DECISION-USEFUL INFORMATION` (B) | illustration | same tag as C17 | **No scorecard grammar** — the five seals never render as n/5, ticks, or a graded bar; that would smuggle an unsourced quantity into a fictional device, per `[K-2]`'s chart-grammar ban on illustrations. Verified at `[K-4]`. |
| C19 | Landing copy: "Don't follow the hype, follow the question", "Educational, not diagnostic" | editorial | none | Brand framing, asserts no outcome. |
| — | MFDS: all ingredients used in manufacture must be listed | not narrated | description-only source | Fetched mfds.go.kr: confirms all-ingredient disclosure is required, but **explicitly states no ordering requirement** is specified — do not narrate MFDS as if it shares the FDA/EU ordering rule. Cited in the publish-envelope description only, alongside C3/C4, as the third jurisdiction's disclosure requirement (not an ordering rule). |

**Counts.** nominal 2 · **sourced 7** (C3–C5, C8, C10, C12, +MFDS as description-only) · unsourced **2** (C6, C15) · illustration 4 (C1, C17, C18, +C1's editorial half) · editorial 8.

`[K-2b]` **ratio limb — does NOT fire.** Mechanism (C3–C12) is sourced 6 :
unsourced 1 (C6 only). Proof (C13–C14) is sourced 0 : unsourced 0 — a purely
editorial/nominal section, no claims requiring sourcing at all. Combined
Mechanism+Proof: 6 sourced : 1 unsourced — sourced-dominant. Ships as a normal
sourced explainer with two flagged asides (C6, C15), **not disclosure-forward**.

`[K-2a]` **hard-prohibited set: clear.** No unsourced safety claim (C15 is
reworded off the absolute and carries no dose/active/condition), no
treats/prevents/cures, no unsourced quantity as a video assertion (the one
number that appears, "80%," is quoted *inside* the fictional Bottle A's own
label art, not asserted by the narration or a floating stat), no comparative
superiority (Bottle A/B is explicitly hypothetical, no real alternative
named), no absolute language after the C15 reword. Re-checked on pixels at
`[K-4]` — see `06-render/qa-log.md`.

### §Rewordings applied before the script is otherwise used verbatim

1. **Hook/Misconception restructure** (see above) — moves the passport-thesis
   sentences from Hook into Misconception to satisfy `[S4/S-6]`'s 20s Hook
   cap and to give Misconception its previously-missing wrong-belief sentence.
2. **C15**: *"'Gentle' is never universal"* → **"'Gentle' isn't a fixed
   property"** — drops absolute language (`[K-2a]`), keeps the point that
   tolerance varies by person, barrier state, and routine.
3. **C6** on-screen/VO attribution verb: *"some ingredients work at low
   levels"* stays in narration as the script's own hedge ("some... not
   automatically useless"), but the **on-screen chip/type** carries an
   explicit `UnsourcedFlag` per `[K-2]`/`[K-3]` — the caption must hedge at
   least as far as the VO, so on-screen wording uses "may be active at low
   levels," not a flat "work at low levels."

### §Evidentiary limits, recorded rather than left implicit

- C8's source (Kongkaew et al. 2020) is a wrinkle-efficacy systematic review;
  it supports "extract standardization varies and limits generalization" —
  it does **not** support any claim about a specific finished serum's
  efficacy, which the script never makes at this point anyway.
- C10's source (Otto et al. 2009) is a delivery/absorption review; it does
  **not** cover sensory tolerability ("feels tolerable") — see the caveat in
  the table above. The claim ships hedged, not flagged separately.
- MFDS's page confirms full-ingredient disclosure is mandatory in Korea but
  is **silent on ordering** — this is a real three-jurisdiction asymmetry
  (US/EU regulate order; Korea regulates completeness, not order) worth
  stating plainly in the publish-envelope description rather than implying
  MFDS shares the same ordering rule.

---

## §Cast — `[S1/S-4]`

Single narrator, Kimberly (Higgsfield `674b71b8-1d2e-4087-8567-d1f53c0b9f3c`,
`voice_type: element`) — already the channel's standing voice per
`baseline.yaml`, confirmed still resolvable via `list_voices` this run, and
the operator's explicit request. No two-hander gap to log (unlike the
`hyaluronic-acid-vs-filler` v1 cut).

## §Word budget — `[S4/V-1]`

300s × 150wpm / 60 = 750 words target, ±10% band = 675–825. **Actual: 646
words** (unchanged by the hook/misconception restructure — words moved, none
added or cut) — **29 words under the floor**, logged as a deviation per the
operator's pre-run decision: the measured VO is the real clock, not padded to
hit the word/time target.

**Measured at S4: 257.120s (4:17.12)** — 42.88s (12.5%) under the nominal 5:00
target, consistent with the word-budget shortfall above. Not padded, per the
operator's decision. Sits between the channel's two long-form precedents
(`hyaluronic-acid-vs-filler` 2:40, `ectoin-survival-molecule` 5:40), closer to
the latter. See `04-assets/vo-timing.json` and `04-assets/script.md`.
