# Delivery — exosome-label-problem (Round 2, 2026-09-02)

A 9:16 narrated Short arguing that "exosome" on a serum label names a particle
*class*, not an ingredient identity — and that the strongest human evidence
comes from procedures that breach the skin barrier, not from daily serums on
intact skin.

Built independently of `videos/exosome-label-decode`, which a separate session
was producing concurrently on the same topic. **No files are shared with it**,
and none of its three cited DOIs were inherited — every source below was
verified against PubMed in this session.

## Renders

| File | Duration | Resolution | Codec | Loudness | True peak |
|---|---|---|---|---|---|
| `renders/exosome-label-problem.mp4` | **67.50s** (2024 frames @ 30fps) | 1080×1920 | h264 / aac 48kHz stereo | **−14.7 LUFS** | **−1.9 dBTP** |
| `renders/exosome-label-problem.raw.mp4` | 67.47s | 1080×1920 | h264 / aac | −24.2 LUFS | −5.5 dBTP |

**Ten scenes** (round 1 shipped seven). See `STORYBOARD.md` for the scene map
and the three split points.

**`exosome-label-problem.mp4` is the publish candidate.** `.raw.mp4` is the
pre-master render, kept only so the mastering step is reproducible.

Mastering: two-pass `ffmpeg loudnorm I=-14:TP=-2.5:LRA=11`, video stream copied
(`-c:v copy`) and **MD5-confirmed unchanged** between input and output.
`TP=-2.5` rather than `-1.5` deliberately: `loudnorm` hits its target on the PCM
it writes, and the AAC encode then raises intersample true peak. A sibling
project in this repo recorded "−1.50 dBTP final" and shipped an MP4 that
measured **+0.5 dBFS** on decode. The figures above are measured with `ebur128`
on the **shipped MP4**, not on the intermediate — see `scripts/master-audio.py`.

## Captions

**Burned-in: none.** This piece is fully type-carried — every spoken claim
renders on screen at 44–86px, above the 42–56px burned-in caption floor — so a
caption band would repeat scenes 06 and 07 close to verbatim and would collide
with the foot zone (citation pills) that every scene already occupies. Recorded
as a decision, not an omission; `scripts/check-static-hold.py` therefore keeps
`CAPTION_BAND_EXCLUDE = False` and its runtime assertion agrees.

| File | Cues | Shortest cue | Longest cue |
|---|---|---|---|
| `captions/exosome-label-problem.srt` | 26 | 1.01s | 4.78s |
| `captions/exosome-label-problem.vtt` | 26 | — | — |

Both built from **one** corrected transcript, so they cannot drift from each
other. Produced by `hyperframes transcribe` (whisper `small.en`) against a VO
mixdown assembled at the composition's own absolute clip timings, so the word
timings are already in video time.

Two corrections applied by hand, both recorded:
- **"prove the other's work" → "prove the others work"** — an ASR mishearing.
  Everything else matched the authoritative script, including the vocabulary
  most likely to be mangled (*exosome*, *extracellular*, *microneedling*,
  *fermentation-derived*).
- **Trailing overrun clamped.** Whisper reported 67.64s against a 67.45s file
  and stretched the word "whole" across 1.37s. Real VO ends at 66.880s; the
  overrunning tail was re-spaced inside the real audio.

Every cue is ≥1.0s, max 2 lines, ≤6 words per line.

## Thumbnail

**`assets/thumbnail/thumbnail-final.png`** — extracted from the render at
**t=3.30s** (the hook fully composed: `EXOSOME` set, payoff bar struck, bottle
at rest), light grade re-derived for this video's own warm-paper palette
(contrast 1.06×, colour 1.04×, sharpness 1.25×) rather than copied from a
sibling with a different ground.

**Five** candidates were pulled at settled moments — `hook-payoff`, `triptych`,
`barrier`, `questions` and the new `endcard` — each written at ~68×120 feed grid
scale plus a 5× re-upscale. `hook-payoff` won on the only test that matters: at
grid size it is the sole candidate whose headline stays fully legible, and
"EXOSOME" is also the search term. The others degrade into blobs and smudges at
that scale; `barrier` reads strongly as graphics (the coral channels survive)
but carries no legible text.

## Imagery

**Five plates, all reused from `catalog/`. Nothing generated.**

| Scene | Source | Role |
|---|---|---|
| 01, 07 | `catalog/product-photography/assets/A01-01.png` | frosted dropper bottle, `세럼 · 30mL` |
| 03 | `catalog/ingredient-photography/sh-pdrn.png` | cell-derived |
| 03 | `catalog/ingredient-photography/02-centella-asiatica.png` | plant-derived |
| 03 | `catalog/ingredient-photography/07-bifida-ferment-lysate.png` | ferment-derived |
| 05 | `catalog/skin-macro-photography/04-base-skin.png` | intact barrier |

Grade: ground-keyed to `--paper` with an additive shift applied only to bright,
low-chroma pixels. **Subject pixels are bit-identical to the catalog
originals** — verified max per-channel delta **0.00** at luma < 190. The three
triptych plates arrived with visibly different grounds (242,235,228 /
245,242,238 / 234,229,220), which side by side would have read as three
different papers and undone the comparison.

No lab, vial, or microneedling imagery exists in the catalog and none was
generated: it would visually assert the very procedure-to-serum transfer the
scope guard forbids.

## Full source list (for the video description)

All eight verified against PubMed in this session.

1. Welsh JA et al. *Minimal information for studies of extracellular vesicles
   (MISEV2023).* J Extracell Vesicles. 2024. `10.1002/jev2.12404`
2. Alzahrani A et al. *Exosomes in Skin Rejuvenation: Systematic Review of
   Anti-Aging Effects and Clinical Applications.* Dermatol Pract Concept. 2026.
   `10.5826/dpc.1601a6462`
3. Liu H et al. *Plant-derived exosome-like nanovesicles: a novel therapeutic
   perspective for skin diseases.* J Nanobiotechnology. 2025.
   `10.1186/s12951-025-03715-1`
4. Wang J et al. *Lactobacillus rhamnosus GG-derived extracellular vesicles
   promote wound healing via miR-21-5p.* J Nanobiotechnology. 2024.
   `10.1186/s12951-024-02893-8`
5. Khalifian S, Shisler J. *Photobiomodulation and Biological Pathways in Skin
   Regeneration and Rejuvenation.* Facial Plast Surg Clin North Am. 2026.
   `10.1016/j.fsc.2026.05.002`
6. Ash M et al. *The Innovative and Evolving Landscape of Topical Exosome and
   Peptide Therapies.* Aesthet Surg J Open Forum. 2024. `10.1093/asjof/ojae017`
7. Flores Rodríguez JC et al. *Efficacy of Exosome-Based Therapies for Skin
   Rejuvenation: A Systematic Review of Human Studies.* Cureus. 2026.
   `10.7759/cureus.104182`
8. Nahm WJ et al. *Exosomes in Dermatology: A Comprehensive Review.* Int J
   Dermatol. 2025. `10.1111/ijd.17903`

On-screen pills carry `Journal · Year` only — no DOI, PMID or internal key ever
renders.

**Two script lines were changed against the supplied draft**, both because the
claim as written could not be sourced and a stronger sourced version existed.
Neither softens a claim. See `BRIEF.md § Script — deviations`.

## Title

**Exosome Skincare Has a Label Problem**

## Description (draft)

> "Exosome" on a serum label names a particle class — not a formula, not a
> dose, not a result.
>
> Three different materials get sold under that one word: cell-derived
> exosomes, plant-derived vesicles, and ferment-derived vesicles. Evidence for
> one doesn't automatically transfer to the others. And "cell-derived" isn't
> one thing either — published work uses vesicles from stem cells, from
> platelets, even from milk.
>
> There's a second problem. Much of the human research pairs exosomes with
> microneedling or laser — devices used precisely because they get past the
> outer barrier. That doesn't tell you how a daily serum behaves on intact skin.
>
> Three questions before you buy:
> 1. What is the source?
> 2. Was the finished formula tested on people?
> 3. Was it tested on intact skin?
>
> The biology is promising. The evidence is still developing.
>
> SeoulHabit — Korean skincare, answered.
>
> ⚠️ Educational content, not medical advice.
>
> SOURCES — (paste the eight citations above)

## Pinned comment (draft)

> Check your own bottle: does the label actually say what the exosomes are
> derived from — cells, plants, or ferment? Most don't. Comment the product and
> we'll decode its label.

## End-screen / next-video target

Shorts carry no end-screen overlay; the equivalent job is the **loop**, which
is engineered here (see below). Natural next video:
`videos/kbeauty-one-percent-line` — the other label-literacy piece on this
channel, and the closest topical neighbour.

## Catalog contribution

- **`MaterialTriptych` → `catalog/visual-components/material-triptych/`**
  (spike + README, registered in `catalog/README.md` and `catalog/index.html`).
  N parallel materials joined by a rail, then having that join struck through.
  A discovery pass found the catalog had **no N-way comparison of any kind**;
  `SplitCompare`/`SplitFaceProtocol` are two-thing bisectors, `ThresholdList`
  is a cutoff ranking, and `FactorConverge` converges on a shared outcome —
  which would have asserted the opposite of this video's claim.
- **`08-endcard`'s brand lockup** — not harvested. It is one 습 mark in a
  bordered square beside a wordmark; that is a three-line CSS chip, not a
  mechanism, and the skill is explicit that a catalog entry needs real
  choreography or a real data contract.
- **`QuestionGate` — deliberately NOT contributed.** The concurrent
  `exosome-label-decode` session harvested one to
  `catalog/visual-components/question-gate/` at 23:40 while this build was in
  progress. Scene 06 here is an independent, simpler sequential-reveal variant;
  adding a second entry under the same name would be exactly the duplication
  the catalog exists to prevent. **A future build should use the catalog entry,
  or the two should be reconciled into one.**

## What shipped this round that a future round should reuse

- `scripts/check-contrast-pixels.py` — measures contrast from **rendered
  pixels**, colour-anchored to each element's own fill. The engine's contrast
  pass sampled three reveal bars mid-wipe and reported 1:1 / 1:1 / 2.02:1 for
  text that measures **16.88:1 / 16.72:1 / 14.64:1** once the bars are open.
- `scripts/run-checks.py` — runs every post-render check unconditionally. The
  house `&&` chain means the first failing gate silences the rest; on round 2
  the safe-area failure meant `check-cadence` never ran at all.
- `scripts/master-audio.py` — two-pass master that re-measures the **shipped**
  file and MD5-confirms the video stream.
- The **UA margin reset** (`h1,h2,h3,p,figure,… { margin: 0 }`). Round 1 failed
  the safe-area hard gate on four scenes because of default `h1`/`figure`
  margins, *with* the border-box reset already in place.

## Verification record

Round 2 final render, measured against the **shipped MP4** — not the source, not
the intermediate. `npx hyperframes check`: 0 lint / 0 runtime / 0 layout / 0 motion.

| Check | Result |
|---|---|
| **`check-safe-area.py` (HARD GATE)** | **PASS — no findings, 270 frames sampled at 4fps.** Every frame's ink clear of top<192 / bottom≥1536 / right≥918 / left<72 |
| `check-blank-frames.py` | PASS — no near-blank stretches |
| `check-static-hold.py` whole-frame | PASS — no findings |
| `check-static-hold.py` region-aware | Findings reviewed frame-by-frame; all false positives (photographic gradient + legitimate negative space) |
| `check-cadence.py` | Runs clean; **11.4% active steps**, up from 4.0% at round 1 open — see below |
| `check-sfx-durations.py` | PASS — 27 cues across 11 files, none long-without-fade |
| `check-contrast-pixels.py` | PASS — 5/5 measured on rendered pixels: 16.88:1, 16.72:1, 16.88:1, **5.49:1** and **5.44:1** (both ink on coral) |
| Frame zero composed | PASS — luma stddev **35.4** (blank threshold <12); ink rows 276–1495, cols 80–917, entirely inside the safe box |
| Loop, picture | PASS — hero region mean luma **219.0 @ t=0 vs 219.0 @ t=67.40, delta 0.01** — effectively a pixel-identical hand-back |
| Loop, audio | PASS — tail (66.90–67.30) **−24.42 dB** against a mid-video BGM-only reference of −22.66 dB; only the last 150ms is a declick fade |
| Loudness, shipped file | PASS — **−14.7 LUFS / −1.9 dBTP** measured with `ebur128` after the AAC encode |
| Video stream integrity | PASS — MD5 identical pre/post master |

### Cadence across the two rounds

| | whole-video active steps | worst quiet run |
|---|---|---|
| Round 1 open | 4.0% | 7.38s |
| Round 1 close | 5.6% | 6.38s |
| Round 2, after the splits | 9.9% | 5.50s |
| **Round 2 final** | **11.4%** | 5.88s |

Reference: `videos/pilling-vs-peeling`, this channel's most recently shipped and
QC'd project, measures **13.6%**. The gap is now small, and closing it further
would mean adding decoration rather than fixing anything real.

**What actually moved the number was not motion tuning.** Two scenes measured 1%
and 2%, and extracting their frames showed the branch tree and the wall
proof-scaled into a mostly-empty canvas — the skill's named 9:16 under-fill
defect, the one that reads as "small fonts" even when the type clears the floor.
Enlarging them (and fixing the wall's backwards internal contrast, where pale
bricks sat on a *lighter* mortar ground) took `04-source` 1% → 13% and
`05a-barrier` 2% → 12%. A second cause was tween *duration*: a channel driving
over 0.40s spreads its change across ~3.2 sampling steps, so each moved only
~0.44 mean luma; concentrating it into ~1.5 steps clears the floor and reads
sharper anyway.

Two scenes remain soft and are accepted as such: `02-what` (10%) and
`06-questions` (5%) are text-and-diagram scenes whose elements are small by
nature. Raising them further would mean decorative motion, which is explicitly
worse than leaving them calm.
