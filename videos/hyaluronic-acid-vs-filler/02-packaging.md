# Packaging — hyaluronic-acid-vs-filler

**v2 note (2026-09-03):** the video was revised to a 160 s single-narrator cut
(see `01-story-brief.md` §v2 Revision). Nothing below was re-run — the topic,
title and thumbnail scoring all depend on the subject and seed keyword, which
are unchanged, so re-scoring would have spent vidIQ credits to re-derive the
same answer. `07-publish-envelope.md` carries the v2-specific chapters and
description; this file's research stands as the record of how the title and
thumbnail were chosen.

## §Topic — S2

**`[S2/T-1]` seed (initial):** `hyaluronic acid vs filler` — shortest noun phrase
naming the mechanism, 4 words, no brand.

**`[S2/T-2]` search demand → FAIL, then SWAP → PASS**

| Keyword | volume | competition | overall | est. monthly | verdict |
|---|---|---|---|---|---|
| `hyaluronic acid vs filler` (seed) | 0 | null | null | 0 (`<750`, "Very low") | **FAIL** — neither `overall ≥ 50` nor (`volume ≥ 40` ∧ `competition ≤ 60`) |
| **`hyaluronic acid filler`** (adopted) | **54.28** | **14.3** | **66.85** | **4,327** | **PASS on both limbs** |

Swap logged. The rule takes "the highest-`overall` related keyword whose meaning
still matches the brief". Higher-scoring rows were **rejected on meaning, not on
score**, and the rejections are the substance of this decision:

- `botox` 68.75 — different molecule, different mechanism entirely.
- `juvederm` 68.66, `restylane` 61.79 — brand names; `[S2/T-1]` bars brands unless
  the brand is the subject, and it is not.
- `radiesse` 67.54 — **calcium hydroxylapatite, not hyaluronic acid.** Adopting it
  would have pointed the video at the wrong substance.
- `sculptra` 60.57 — poly-L-lactic acid. Same problem.
- `skin care` 64.97, `plastic surgery` 60.41, `fillers` 61.70 — category, not mechanism.

`hyaluronic acid filler` is the highest-scoring row that is actually about this
video's subject, and its competition of **14.3** is the lowest of any row above
volume 50.

**Slug kept as `hyaluronic-acid-vs-filler`, diverging from the seed.** The runbook
derives the slug from the seed, which would give `hyaluronic-acid-filler` — one
character-class away from the existing `videos/hyaluronic-acid-serum/` and
actively misleading, since this video is a three-way comparison, not a filler
explainer. Divergence logged rather than taken silently.

**`[S2/T-3]` browse evidence → PASS in letter, VOID in substance**

Bounds sent, both explicit: `minSubscribers=0`, `maxSubscribers=max(10×8, 10_000)
= 10_000`, `contentType=long`, `publishedWithin=sixMonths`, `sort=breakoutScore`,
`limit=20`.

Three calls were made and the finding is the same each time: **the outlier tool
cannot answer this question at these bounds.** Top 3 returned, on the original seed:

| Video | breakoutScore | subs | Actually about |
|---|---|---|---|
| `FT64rjKdFuA` "How To Clean Yellow Teeth Into White" | 3137.67 | 5060 | teeth whitening |
| `zyaW88AZ5CI` "Gluteal Intramuscular Injection Demonstration" | 706.45 | 1450 | nursing skills |
| `P3-ad5Zvw3o` "Messing around in Roblox 2.5: Filler pt16" | 162.24 | 4240 | a Roblox filler episode |

`hyaluronic acid vs filler` also returned a **billiards player named Joshua
Filler** and a **WIX oil filter** comparison. Re-run on the swapped seed returned
gecko rescues, lofi spa music, and hydrofluoric acid. Run again with
`requireAllTitleTerms=true`: **zero results** — no long-form video from a
≤10k-subscriber channel in the last six months carries all three of
*hyaluronic / acid / filler* in its title.

So the gate **passes literally** (many rows clear `breakoutScore ≥ 3`) while
carrying no browse evidence at all, because "acid", "filler" and "injection" are
each strongly polysemous. Recorded as a literal pass with the set named, not
laundered into a real one. **The topic proceeds on `[S2/T-2]`, which passed on
its own after the swap** — the "if both fail → reframe" branch never opens, and
the run is **not** tagged `experiment`.

**`[S2/T-4]` title shapes → harvest DEGRADED**

Extracting shapes from the top 5 by breakoutScore would extract the shape of
gecko-rescue and nursing-injection titles. `title_shapes[]` is therefore thin —
**one** structurally relevant comparator in the whole set:

- `DCHYmELj1LE` "The Acid That Eats Through Glass — The History of Hydrofluoric
  Acid" (breakoutScore 4.37, 2560 subs) — shape: **substance identity + surprising
  property + origin.** Off-topic but structurally the same move this video makes.

Two skincare-adjacent shapes noted, neither harvested:
- negative-command + number + outcome (`kDMiz7qQ2Mk`, gray hair)
- **`LzVw4reocxk`** "ALOE VERA Erases Deep Wrinkles within 10 Minutes Even at 70!"
  — recorded as a **counter-example**: this is precisely the absolute-language
  pattern `[K-2a]` forbids ("Erases", a hard number, an age promise). Not a shape
  to borrow.

## §Title — `[S3/P-1]`

Five candidates, five distinct shapes, seed in the first 60 characters, all ≤ 70.
**Scored once each — 5 calls, the rule's cap. No second round.**

| # | Shape | Title | chars | Score |
|---|---|---|---|---|
| 1 | contrast | Hyaluronic Acid Filler vs Serum: The Difference Nobody Explains | 62 | 85 |
| 2 | question | Is a Hyaluronic Acid Serum Just Filler in a Bottle? | 50 | 89 |
| 3 | number | Hyaluronic Acid Has 3 Identities: Body, Serum, Filler | 52 | 84 |
| 4 | why-X | Why Hyaluronic Acid Filler and Serum Do Completely Different Jobs | 64 | 93 |
| 5 | **substance + origin** | **Hyaluronic Acid: Found in a Cow's Eye, Sold as Serum and Filler** | **62** | **95** |

**Winner: #5**, by T-4 shape rank — it is the only candidate using the single
structurally relevant shape the outlier set produced.

**No inversion this run.** The highest-scoring candidate also won, so this run
does **not** test `packaging.title_scorer_discriminative` (recorded `false` in the
baseline off two prior runs where the scorer ranked a failing title above its
rewrites). There was no failing control here to rank. Logged as a null result for
`[S9/L-2]`, not as evidence the scorer works.

**Recorded tension:** P-1's *default* — "the candidate whose first 40 characters
carry the mechanism, not the category" — would select **#4** ("Why Hyaluronic Acid
Filler and Serum Do C…"). #5's first 40 characters carry origin, not mechanism.
The default applies only when T-4 yields no shapes, and it yielded one, so shape
rank governs. But that shape rests on a **single comparator at breakoutScore
4.37**, which is thin evidence, and #4 is the honest runner-up if this title
underperforms at readout.

## §Thumbnail — `[S3/P-2]`, `[S3/P-3]`

`COMPANION-RESOLVED:frontend-design (skill-tool)` — fired before concept work.

Two things it changed:

1. **No `01 / 02 / 03` numbering anywhere in this video.** Numbered markers encode
   sequence; this content is three *parallel* identities. Three lanes, not three
   steps. (Would otherwise have been the default move for a "three things" video.)
2. **The signature comes from the subject's own world**, not from a layout trope.

**Signature element — the morphology lineup.** The molecule's own shape is the
differentiator, so it carries the whole piece:

| Identity | Chain form drawn |
|---|---|
| body | long free coils, dispersed, water held in the loops |
| serum | two chain sizes meeting a skin boundary — large stays above, small crosses |
| filler | the same chains **cross-linked** into a rigid 3-D lattice that holds shape |

One visual language, three states of one molecule. This doubles as the `[S6/A-9]`
actor map (`ha-body`, `ha-serum`, `ha-filler` persist across scenes and are
rearranged, never redrawn) and defines the camera path: wide lineup → dive into
one identity's chain structure → pull back out to the lineup for the verdict.

**Palette note, stated rather than drifted into.** `frontend-design` names
"warm cream + high-contrast serif + terracotta accent" as one of three current
AI-default looks — and the SeoulHabit token set (`--paper #F7F5F0`,
EB Garamond, `--coral #C97A5C`) *is* that look. It is kept because the skill's own
rule is that a brief pinning a direction wins, and this direction is pinned by 31
shipped projects and a live design system, not chosen fresh here. `[S6/A-2]`:
project tokens win.

**Concept:** the three chain-forms in three lanes on `--paper`, morphology plainly
different at a glance, overlay text **"THREE JOBS"** — 2 words, and neither word
appears in the winning title (`[S3/P-2]` requires overlay text not in the title).
Exactly one accent (`--aqua` on the serum lane, the one the viewer actually owns).
