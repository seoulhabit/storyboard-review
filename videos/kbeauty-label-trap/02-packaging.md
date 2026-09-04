# Packaging — kbeauty-label-trap

## §Topic — `[S2]`

[S2/T-1] seed → `k-beauty ingredient label` (shortest noun phrase naming the video's actual mechanism — evaluating an ingredient list — no brand name, 4 words).

[S2/T-2] demand → **FAIL then SWAP → PASS.** Seed volume 0, `estimatedMonthlySearch: <750`, no `overall` score (unattributable). `vidiq_keyword_research(mode=research, keyword="k-beauty ingredient label", country=US)` returned 13 related suggestions, **none of which retain "ingredient" or "label"** — the related-keyword engine drifted entirely to category terms (skincare, k beauty, korean skincare routine, glass skin). Adopted **`k beauty`**: overall **65.96** (≥50) with volume **69.74** (≥40) and competition **39.7** (≤60) — passes both limbs.

[S2/T-2] specificity loss, logged plainly → the swap keeps the channel's own category identity (K-beauty) but drops the "how to read a label" mechanism entirely; no related keyword scored measurably while retaining it. This is a real gap in the seed's own searchability, not a laundering of the swap into something it isn't — recorded rather than presented as a clean pass.

[S2] slug DIVERGES from seed → kept `kbeauty-label-trap` (fixed at S0.0, before T-1/T-2 ran). `k-beauty-ingredient-label` (seed-derived) is longer and less distinctive than the operator's own title; no existing project collides with either.

[S2/T-3] outliers → **PASS in letter, degraded in substance.** `vidiq_outliers(keyword="k beauty ingredients", contentType=long, publishedWithin=sixMonths, minSubscribers=0, maxSubscribers=10000, sort=breakoutScore, limit=20)`. Top by breakout: a Punjabi lyric video (4177.71 — pure keyword-overlap noise, "ingredients" nowhere in it), a Tyler Perry review, several ASMR/ingredient-name-for-kids/DIY-face-mask videos. **Only one structurally relevant comparator**: `uGjGjKhoEKw` — "10 Hair Dye Brands Women Need To Drop Immediately (And 4 Safer Choices)" (Skinvestigation, breakout 120.49, vph 297.27, tags include "beauty industry exposed", "skincare dupes") — an investigative consumer-literacy channel in the same register as this video's "the label can't tell you everything" premise. **Counter-example, not harvested**: `zS6_DoLoCJA` "5 CHEAP Makeup Brands EVERYONE IGNORES (But They're Goldmines)" — bargain-hunting framing, opposite intent (buy more vs. evaluate better), rejected as a shape.

[S2/T-3] reframe branch NOT opened → needs both T-2 and T-3 to fail; T-2 passed after its swap. Run is **not** tagged `experiment`.

[S2/T-4] title shape harvested → **N-items + red-flag/safer-choice investigative frame** (from Skinvestigation's video: "[N] things to drop + [N] safer alternatives"). Adapted, not copied: this video's actual shape is *N questions*, not *N red flags* — the operator's own title/alt-title already carry that shape. T-4's harvest confirms the investigative-literacy register is a real, if thin, comparator class rather than validating any specific phrasing.

## §Packaging — `[S3]`

COMPANION-RESOLVED:frontend-design (skill-tool)

[S3] frontend-design findings → two corrections, both applied | (1) the brief's own "ink-black lab + one vermilion accent" description sits close to the skill's documented AI-default cluster #2 ("near-black background, single bright accent") unless the two-register split is explicit: **porcelain stays the video's default ground** (matches all 31 prior channel videos), **ink-black is reserved specifically for the lab-bench/forensic scenes** (s01–s03, s12), not the whole piece — locked into `03-beat-sheet.json`'s per-scene `bg`, not left implicit. (2) the thumbnail's molecular-ecosystem-vs-green-water split risked reading as a generic "real vs. fake" trope; corrected by putting the vermilion evidence stamp **physically on one bottle's glass**, tying the accent color to the video's own passport/stamp signature motif rather than functioning as an arbitrary "pick one bright color" default. Five-seal numbering is legitimate here (not the generic 01/02/03 the skill warns against) — the five questions are a genuine build-on-each-other sequence, not a decorative label. | frontend-design

[S3/P-1] title candidates → 5 shapes, 5 scoring calls, one round (cap) | problem+negative-capability **96** · myth-bust reframe 85 · question 92 · exposé/hiding 87 · actionable-listicle 77 | vidiq_score_title x5
[S3/P-1] winner → **"The K-Beauty Label Trap: 5 Things Your Ingredient List Can't Tell You"** (69 chars, seed "k beauty" in first 13) | top score AND the operator's own stated primary title — no conflict to resolve. T-4's harvest is too thin (one weak comparator) to override a clear 96 by shape-rank the way `hyaluronic-acid-vs-filler`'s did; recorded as top-score selection, not shape-rank selection. | —
[S3/P-1] runner-up on file → "Can You Actually Read a Skincare Ingredient List?" (92) — the honest fallback if this title underperforms at readout | —

[S3/P-2] thumbnail concept → two bottles, forensic scanner split, vermilion stamp on the left bottle's glass (not headline-only), overlay `THE LABEL ≠ THE FORMULA` (4 words incl. symbol, not in title) | frontend-design's stamp-placement correction applied | —
[S3/P-2] saturation → **0 near-identical** (threshold ≥10) | top match score 1.36 (noise floor — tarot cards, fake-LV-bottle spotting, DNS encryption); concept holds, no metaphor swap | vidiq_similar_thumbnails
[S3/P-3] thumbnail → generated 1, self-score **89**, independent `vidiq_score_thumbnail` **89** (agree) | **≥70, refine branch does not fire** — cap respected, one generation only, 22 credits spent | vidiq_generate_thumbnail, vidiq_job_poll, vidiq_score_thumbnail
[S3/P-3] result → 1280×720 (16:9, ratio 1.7778), saved `04-assets/thumbnail.png` | stamp glyphs on the bottle are AI-generated decorative seal-chop texture, not real characters — acceptable for a thumbnail; the in-composition passport stamp built fresh at S6 uses real designed typography (`IDENTITY ONLY`), not this placeholder art | —
[S3/P-3] scorer videoId caveat → `vidiq_score_thumbnail` requires a videoId; passed the channel's own `D4e2xnNQm1M` as context (same channel this run's title/image belong to), matching `hyaluronic-acid-vs-filler`'s precedent for an unpublished video | —

[S3/P-4] description skeleton + tags → drafted at `07-publish-envelope.md` (S8), sources rendered human-readable (FDA · 21 CFR 701.3, EU · Reg. 1223/2009 Art. 19, MFDS, two journal citations), chapters filled once S5 measures real timestamps.

## §Chapters — filled from `03-beat-sheet.json` at S5

| Time | Chapter |
|---|---|
| 0:00 | Two Bottles, One Question |
| 0:16 | The List Is a Passport, Not a Scorecard |
| 0:43 | Why Order Isn't Random |
| 1:22 | Same Name, Different Extract |
| 1:51 | What Carries the Ingredient In |
| 2:25 | How Far Is the Evidence, Really |
| 3:05 | Where the Claim Stops |
| 3:30 | Back to the Two Bottles |
| 4:08 | What to Actually Check |

Min gap 15.777s (≥10s floor), first at 0:00, 9 chapters (≥3 floor) — payoff-named, derived from beat-sheet section/sub-section starts, not hand-written.

## §Thumbnail concept image
See `04-assets/thumbnail.png`.
