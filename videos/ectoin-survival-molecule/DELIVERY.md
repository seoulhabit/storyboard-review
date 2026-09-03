# DELIVERY — Ectoin: the survival molecule

**Complete: all 7 acts, 29 scenes, 5:40.2 at 1920×1080.** The channel's first
long-form video and the first 16:9 render in this repo. Nothing has been
published anywhere.

---

## Deliverables

| Item | Path | Notes |
|---|---|---|
| **Publish candidate** | `renders/ectoin-survival-molecule_2026-09-02_final.mp4` | 1920×1080, 30 fps, **5:40.2**, 10,207 frames. Carries the wipe transition system and the scene-28 fix. **Mastered: −14.6 LUFS / −1.9 dBTP**, measured by decoding the shipped file back. |
| Superseded — no transitions | `renders/ectoin-survival-molecule.mp4` | The 28-hard-cut build, mastered. Kept as the before/after reference and as the safe-area gate's clean baseline. |
| Act 1 pilot | `renders/ectoin-act1.mp4` | The 75s risk-retirement render. Superseded — kept only as the cadence baseline the table below compares against. |
| Captions | `captions/ectoin-survival-molecule.srt` / `.vtt` | 217 cues from real word timings, not estimates. Shortest 1.00s, longest 5.26s, **0 under the 1.0s floor**. |
| Voiceover | `assets/voice/01.wav` … `29.wav` | Standing series voice. All normalised to exactly 250ms trailing silence. |
| Storyboard | `STORYBOARD.md` | **Generated** from `index.html` — chapters and timing table cannot drift. |
| Brief + claim table | `BRIEF.md` | The `[K-1]` table for all 13 claims. |
| Script | `SCRIPT.md` | All four corrections applied. |

**Pruned 2026-09-02.** Three renders were removed once the final master existed:
both unmastered pre-masters (`ectoin-full.mp4` and
`ectoin-survival-molecule_2026-09-02_wipes.mp4`) and the rejected translating-push
build (`…_2026-09-02_transitions.mp4`), which failed the safe-area gate on 35
frames because sliding a full-canvas scene drags its content through the reserved
zones. All three were picture-identical to a render still present here and
differed only in audio mastering — verified by frame hash before deletion. They
remain in git history at `4894c0f` if a re-master or the known-dirty gate fixture
is ever wanted again; re-mastering is cheap from either surviving master anyway,
since the video stream is copied through untouched.

**Chapters** (paste-ready, from `STORYBOARD.md`):

```
0:00 A molecule invented by bacteria trying not to die
1:13 Why it is not just another hyaluronic acid
2:07 What it might actually do for skin
2:54 What the human evidence really says
4:03 How to read an ectoin label
4:52 Why K-beauty picked it up
5:15 The verdict
```

## Gates — final render

| Gate | Result |
|---|---|
| `hyperframes check --samples 40` | **Pass.** 0 errors, 0 warnings, 26 info (scenes legitimately clipped mid-wipe). **Sample-density dependent** — see the note below before raising `--samples`. |
| Safe-area (**hard gate**) | **PASS** — 1,361 frames, no ink in any reserved zone. Requires the multi-ground estimator; an older copy of the gate reports 70 false failures on this render. |
| Static-hold, whole-frame | **No findings**, 680 frames. |
| Static-hold, region-aware | 6 content-voids, **all verified false** — the flagged cells carry content throughout (edge density 2.33% inside a "void" against 2.34% just before it). The ink threshold, not the content, is what moves. |
| Audio | **−14.6 LUFS / −1.9 dBTP** on the delivered file, decoded back. |
| Cadence (`--longform`) | **Clean** — no scene exceeds the quiet ceiling. Whole-video active-step share **14.0%**. |

**Both of those gate results depend on tool versions, and a reader re-running
them with older copies will get failures that are not this render's fault.**

*Safe-area.* The gate's page-ground estimator took a single median of the outer
border ring, which is only valid while a frame has one ground. Every wipe
boundary here has two, so the ring goes bimodal and whichever ground loses the
median reads as 100% ink. On this render that produced **70 flagged frames, all
false** — the frame it called worst has a top band of uniform luma 19, min ==
max, zero variation. Fixed upstream in `catalog/tooling/check-safe-area.py`
(commit `cc343e9`, controls added in `78c1460`) by clustering the ring instead
of averaging it. `scripts/check-safe-area.py` here is a copy of the fixed
version. A pre-fix copy will fail this render; the render is fine.

*`check` layout findings.* A clip-path wipe trips the engine's layout pass as
`content_overlap` / `text_occluded`, because that pass tests bounding-box
geometry and does not model `clip-path` — a clipped incoming wrapper still
presents a full-canvas opaque box over the outgoing scene's text. The rendered
frames show both scenes with a clean seam. Severity is persistence-aware, so
the verdict tracks **sampling density rather than the composition**: at
`--samples 40` a 0.45s window is rarely hit twice across 340s, so these land as
26 info. Raise the sampling and they become errors without anything about the
video changing. Measured on a 3-scene proof of the same generator: cuts 0
layout errors at any density, wipes 1 at `--samples 9`, 3 at 20, 3 at 60.

## The thing this rebuild was for

Act 1 measured **5.8%** of 8 fps steps clearing a perceptibility floor, against
11.7–23.1% on shipped 9:16 work. The cause was grid share: on a 1920-wide frame
a headline sits in a column, so a text fade moves ~0.7% of the pixels. Acts 2–7
were authored to a **panel-scale** vocabulary — washes sweeping whole cards,
panels entering and leaving, grounds inverting, grids filling:

| Render | Active steps |
|---|---|
| Act 1 pilot (word-scale) | 5.8% |
| Panel-scale rebuild, 28 hard cuts | 12.7% |
| **Final, panel-scale + wipe transitions** | **14.0%** |
| `exosome-label-problem` (shipped 9:16) | 11.7% |
| `pilling-vs-peeling` (shipped 9:16) | 23.1% |

**Correction, 2026-09-02.** This table previously recorded the hard-cut build at
**14.8%**. That figure is wrong and was never measured against the file it
describes: re-running this project's own unmodified `scripts/check-cadence.py`
on `renders/ectoin-survival-molecule.mp4` returns **12.7%** (344 of 2703 steps),
and the doc was written eleven minutes after that render finished. An external
review independently reported 12.7% and was initially dismissed on the strength
of the number above — the review was right. A figure a project has already
written down is a claim, not a measurement.

**Now clean.** Nine scenes were over the ceiling after the first pass, not the
five first reported — a truncated log hid four Act 1 scenes still carrying the
original word-scale vocabulary. All nine are fixed, and the fixes were sized
against the metric rather than by eye:

    per-step mean|dLuma| = (frame-area-fraction x luma-delta) / (duration x 8)

Two earlier attempts failed *because* they were eyeballed, and the arithmetic
says exactly why:

| Attempt | Area | Luma delta | Per-step | |
|---|---|---|---|---|
| s12 bricks celadon→coral | 12% | **27** | 0.45 | under the 1.0 floor |
| s24 proportion bar at 74px | 2.9% | 120 | 0.43 | under the floor |
| s12 bricks celadon→**ink** | 12% | **149** | 2.48 | clears |
| s1 cards filling the column | 8.7% | 107 | 3.88 | clears |

The celadon→coral case is the instructive one: it reads as a dramatic shift to
the eye and is nearly invisible to a luma-difference check, because those two
colours have almost the same luminance. **Pick a beat's colour by luminance, not
by hue.**

Three near-blank stretches (267ms–1.47s) sit at ink↔paper ground changes in the
closing scenes. Short, and consistent with hard cuts between opposite grounds.

## Bugs this build surfaced

Each was caught by a gate and verified against pixels, not assumed:

1. **Sub-composition scripts must live INSIDE `<template>`.** The runtime clones
   only the template's contents and discards everything else — including the
   `<script>`. With them outside, no timeline registered and every scene rendered
   at its static CSS state: t=0.0s and t=8.5s of scene 01 came out
   **pixel-identical**.
2. **An inlined token block that omits one token fails silently.** `--endscreen-*`
   lived in `tokens.css` and never made it into the inlined copy, so scene 29's
   `calc()` was invalid and CSS dropped the padding entirely. The end-screen scene
   ran full-bleed into the reserved right zone — 41 frames, caught by the hard
   gate. `grep -c endscreen` was **3 in `tokens.css`, 0 in the inlined block**.
3. **Entrance transforms overshoot the safe line.** 81 frames of intrusion across
   four scenes, all transients from `x:-90` entrances and decorative `scale:1.03`.
   Fixed structurally with `.stage > * { overflow: hidden; }` — the child fills
   the safe box, so clipping it clips at the line. The two decorative scale-ups
   were **deleted**, not clipped into compliance.
4. **Copy written as a bare text node renders blank** under an animated
   background. `.wash ~ *` lifts sibling *elements*; a text node has nothing to
   apply it to. Three cards rendered completely empty — and `check`'s own
   `text_occluded` pass did not see it, because the text never became an element.
   The region-aware content-void check caught it.
5. **A gate's background estimator is an assumption too.** The safe-area check
   took page background as the whole-frame modal luma. On a scene with two
   ~45%-of-frame panels the modal became a *panel* colour (151 vs a true ground
   of 243), so every margin read as ink and **all four reserved zones reported
   100% ink** across 136 frames with nothing out of place. Now derived from the
   median of the outer 4px border ring. On a hard gate a false positive is worse
   than a miss — it blocks a clean render, and once waved through it teaches you
   to wave through the real one.
6. **Voiceover QC is not optional.** `scripts/check-vo.py` found two takes at
   ~110 wpm (this engine slows sharply on comma lists), seven takes ending with
   the last word still live at end-of-file, and four garbling "ectoin"
   *differently each time* — the signature of articulation failure, not
   transcription error. A phonetic respelling made it **worse** ("echetoin"); a
   plain-spelling retry fixed it.

## Sources — ready to paste into the description

All on-screen claims resolve to indexed literature. The frame carries only
`Journal · Year`; no PMID renders.

- Schwibbert et al. 2010, *Environ Microbiol* — https://doi.org/10.1111/j.1462-2920.2010.02336.x
- Lentzen & Schwarz 2006, *Appl Microbiol Biotechnol* — https://doi.org/10.1007/s00253-006-0553-9
- Yu, Jindo & Nagaoka 2007, *J Phys Chem B* — https://doi.org/10.1021/jp068367z
- Sahle et al. 2018, *Phys Chem Chem Phys* — https://doi.org/10.1039/c8cp05308a
- Graf et al. 2008, *Clin Dermatol* — https://doi.org/10.1016/j.clindermatol.2008.01.002
- Bow et al. 2021, *Biochem Biophys Rep* — https://doi.org/10.1016/j.bbrep.2021.101134
- Heinrich, Garbe & Tronnier 2007, *Skin Pharmacol Physiol* — https://doi.org/10.1159/000103204
- Marini et al. 2013, *Skin Pharmacol Physiol* — https://doi.org/10.1159/000351381

Also available, not cited on screen: Alexopoulos et al. 2022, *Pediatr Dermatol* —
https://doi.org/10.1111/pde.15117

**The Abib claim was verified, and by a better route than the retail copy.** The
on-screen beat now rests on **INCI order**, which is checkable from the label
itself: panthenol is listed 2nd, ectoin 11th. An ingredient at position 11 cannot
be 10%. The voiceover says exactly that rather than asserting a split.

## 2026-09-02 — the continuity pass

An external review called the piece "a sequence of separate slides". It passed
every gate this project had, which is the finding: cadence measures how much
changes inside a scene and says nothing about whether anything carries across
the cut. All 28 boundaries were hard cuts, and 11 of them did not even change
ground.

**Transitions.** `scripts/build_index.py` now emits a two-type system: a
clip-path wipe from the right edge, 0.45s, within a chapter, and one from the
bottom edge, 0.60s, into each of the six chapter openers so the strongest
treatment lands on the re-hook. Both are ground-safe by construction — nothing
translates and opacity is never touched, so no frame composites two grounds,
which matters across this video's 17 ink↔paper changes where a crossfade would
go muddy. The outgoing clip's `data-duration` is extended to hold its final
frame under the wipe; **no scene `data-start`, no internal beat timing and no VO
cue moved**, which is the only reason this is safe on a voiceover-locked cut.

A translating push was built first and rejected. It rendered correctly and
passed `check`, but sliding a full-canvas scene drags its content through the
reserved zones: 99 frames failed the safe-area gate against a baseline that
passed all 1,361, measured at up to 6.2% edge density inside the top zone. A
wipe moves nothing, so every scene stays exactly as compliant as it is at rest.
Safe here specifically because the project is 100% browser-drawn — not one
`<img>` in any scene — so the `drawElement` capture bug that hits an animated
clip over a raster cannot apply.

**Scene 28's payoff line.** `A genuinely interesting supporting molecule` was a
bare text node under `.wash.moss`. `.wash ~ *` can only lift an *element* above
the wash and `.wash.moss ~ *` can only recolour one, so the wash painted over it
and the card rendered blank at 1.72:1 — the affirmation the two strike-outs
exist to set up. Wrapped in a `<span>`, it now reads paper-on-moss at **5.42:1**.
Fixed in `scripts/frames_a27.py`, the generator, not the generated file:
`npm run build` regenerates all 29 scenes and would have silently discarded a
downstream edit.

**What the gate got wrong.** The final render still tripped the safe-area gate on
70 frames, all inside wipe windows, all false. Its page-ground estimator took a
single median of the border ring, which is only valid while the frame has one
ground; a transition frame has two. Fixed upstream in
`catalog/tooling/check-safe-area.py` (commit `cc343e9`) and mirrored into
`scripts/`. The rejected push build is kept as the known-dirty fixture that fix
was validated against.

**Still open** from the review, each needing per-beat authoring rather than a
mechanical edit: 65.3% of real tweens still share one `power3.out` inherited
from a timeline default; scenes 09 and 10 still draw byte-identical protein and
water-shell geometry instead of merging into one sub-composition; there are
still zero camera moves.

## Still outstanding

- **Thumbnail.** Produced 2026-09-03 — see *Packaging* below. The CTR score
  (`[S3/P-3]`) is still outstanding: `vidiq_score_thumbnail` needs a published
  `videoId` or a hosted image URL, and this video is unpublished.
- **BGM and SFX.** The mix is voiceover only. Mastering is correct for that mix
  and must be re-run if a music bed is added.
- **Description, tags, pinned comment, end-screen targets.**
- **`brand/channel/watermark-150.png`** — built and contrast-verified for
  long-form, still unused. This video is its intended first outing.

## Reproducing

```bash
python3 scripts/pad_vo.py && npm run build && npm run check
npx --yes hyperframes@0.8.22 render --quality high --workers 1 -o renders/<raw>.mp4
python3 scripts/master-audio.py . renders/<raw>.mp4 renders/<final>.mp4
```

Gates need their profile flags — `--landscape` for safe-area and static-hold,
`--longform` for cadence. Without them the portrait defaults produce a **silent
false pass**: the bottom-zone slice `mask[1536:, :]` on a 1080-tall frame is an
empty numpy view.


## Packaging — 2026-09-03

**Title (scored, `[S3/P-1]`).** `Ectoin: How Salt Lake Bacteria Made a Skin
Barrier Ingredient` — 61 chars (limit 70), seed keyword `Ectoin` at position 1
(must be inside the first 60). Chosen by measurement, not preference; four
candidates scored against the channel via `vidiq_score_title`:

| Title | Score |
|---|---|
| Ectoin: How Salt Lake Bacteria Made a Skin Barrier Ingredient | **93** |
| Ectoin: How Desert Bacteria Made a Skin Barrier Ingredient | 89 |
| Ectoin: The Skin Barrier Molecule Bacteria Invented to Survive | 82 |
| Ectoin: The Survival Molecule Behind Skin Barrier Repair | 73 |

The 20-point spread runs along one axis: the origin-story framing beats the
benefit framing every time. That matches the packaging research — both ranking
competitors are product roundups, and nobody owns the origin/mechanism angle,
which is exactly this script's.

**Thumbnail.** `thumbnail/thumb-1280x720.{html,png,jpg}`, browser-drawn per the
PDRN/betaine precedent and rendered through headless Chrome at exactly
1280x720.

- Overlay text is **WHERE NOTHING LIVES** — three words (`[S3/P-2]` ceiling)
  sharing no word with the title, so the pair carries two different hooks
  rather than one repeated twice.
- **No ingredient pill**, which departs from house style deliberately: the pill
  would take total overlay text to four words, and at feed size the chip costs
  more legibility than naming the ingredient buys when the title already opens
  with it.
- The salt-flat ground and horizon were added after the first render, where a
  bare gradient carried no place at all. Verified by downscaling the real PNG
  to 168px (mobile feed width): headline still reads, molecule holds as a
  glowing form, horizon survives.
- The art is the mechanism, not decoration — a molecule inside its own ordered
  water shell, which is the video's actual claim.

**Still open.** Thumbnail CTR score, description, tags, pinned comment,
end-screen targets, and the first outing for `brand/channel/watermark-150.png`.
