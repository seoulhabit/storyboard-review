# QA log — hyaluronic-acid-vs-filler

## Gates

| Gate | Result | Measured on |
|---|---|---|
| `hyperframes@0.8.22 check` | **ok: true**, 0 errors across lint / runtime / layout / motion / contrast | the composition under seek, 40 samples |
| `check-safe-area.py --landscape` | **PASS — no findings, 720 frames sampled** | `06-render/final.mp4` |
| `check-static-hold.py --landscape` | advisory (exit 0); content-void regions verified by eye, see below | `final.mp4` |
| `check-cadence.py --longform` | advisory (exit 0); **15.1% whole-video active share** | `final.mp4` |
| `continuity-audit.py` | 13/13 boundaries transitioned · top signature 28.7% · 0 rebuilt actors · 17 camera moves | source |
| `ebur128` | **−14.1 LUFS integrated, −2.5 dBTP, LRA 3.0** | `final.mp4`, not the loudnorm intermediate |
| `ffprobe` duration | video **180.000 s / 5400 frames @ 30 fps** == VO master clock exactly | `final.mp4` |

**Constants confirmed against this project before trusting any "0 findings"**
(`[S7/R-2]` requires this; an inherited caption band has silently excluded real
content three times in this lineage): `CAPTION_BAND_EXCLUDE = False` is correct
here — there is no burned-in caption band, `.caption` is ordinary flow text
inside the stage. `--landscape` rebinds both scripts to 1920×1080 with zones
54/108/96/96, which matches this project's own declared tokens exactly, and both
scripts `ffprobe` the render and refuse on a canvas mismatch.

## Cadence, in context

15.1% of 8fps steps carry a perceptible, localised change. Comparators, all
measured on shipped files rather than quoted from a delivery note:

| Piece | Active share |
|---|---|
| **this run** | **15.1 %** |
| `ectoin-survival-molecule` (the long-form comparator) | 14.0 % |
| shipped 9:16, low end | 11.7 % |
| shipped 9:16, high end | 23.1 % |

Five scenes exceed the 6.0 s long-form quiet ceiling (longest 10.12 s, in
`s06-serum-size`). These are advisory. Each is a scene where a single sourced
claim is being read aloud over a diagram that is already making the argument —
`s06` is the size/boundary panel, which holds while the VO explains it. The
script's own note applies: "does it need a beat, or is it a deliberate hold?"
Judged deliberate, and the whole-video share is above the long-form comparator.

## `[K-4]` — rendered-claim check, on the extracted frames

| Check | Verdict |
|---|---|
| Every unsourced claim shows its flag concurrently | **n/a — there are no unsourced claims.** `[K-2b]` did not fire (Mechanism + Proof are 8 : 0). No flag component is emitted because there is nothing to flag. |
| Flag not in the accent colour / not citation typography | n/a, as above |
| No internal record id (`ING-*`) anywhere | **PASS** — confirmed on all frames |
| No PMID on any frame | **PASS** — chips render `Journal · Year` or `FDA · Dermal Fillers`; PMIDs and DOIs are in the description only, per `ectoin`'s convention |
| On-screen wording hedges at least as far as the VO | **PASS** — verified on the pixels at t=75.0: the frame reads "Smaller ones **may** travel farther into the upper layers", carrying the VO's own hedge into the type. `[K-3]` is satisfied where it matters most, since the muted viewer reads the type. |
| Nothing hard-prohibited appears | **PASS** — the only on-screen number is `1934` (cited); the two safety lines are FDA-verbatim; no *treats/prevents/cures*, no comparative superiority, no absolute language |

**One `[K-4]` finding, fixed rather than logged:** the video shipped **two
different citation treatments** — hand-authored scenes used the bordered mono
pill, generated scenes used accent uppercase sans. Two treatments read as two
different kinds of evidence, and citations are this video's entire credibility
layer. Unified on the pill across all 14 scenes.

## `design-critique` — frame review

`COMPANION-RESOLVED:design-critique (skill-tool)`. Applied to frames extracted
from the muxed deliverable.

### First impression
Frame zero reads as what it is: one name over three visibly different structures.
The three-lane comparison is legible in about a second, before any narration.

### What works
- **The diagram makes the argument the sentence makes.** At t=75.0 the copy says
  large chains stay near the surface and smaller ones may travel farther, and the
  panel shows exactly that — big coils above a dashed boundary, small ones below.
  That alignment is the whole reason the presenter is `moving-diagram`.
- **The payoff frame (t=168) is the strongest in the piece.** Three morphologies,
  three badges, no explanation needed.
- Type hierarchy is doing real work: EB Garamond hero against Inter body against
  a mono chip gives three unmistakable registers.
- Ground alternation (paper → ink) tracks the argument rather than decorating it:
  the dark scenes are the origin story and the filler/safety material.

### Findings

| Finding | Severity | Action |
|---|---|---|
| Frame zero showed only lane 0; lanes 1–2 were hidden until their beats, leaving ~60% of the opening frame empty — close to mandatory rule 5's "a lone title on empty canvas" | 🔴 Critical | **Fixed.** All three lanes composed at t=0 at rest, each brought forward on its own beat. |
| The cross-linked lattice was **invisible** for 16 s on `s10-crosslink`: `.actor` painted with `var(--ink)`, which stays the dark token when only the text colour flips | 🔴 Critical | **Fixed.** Flip the token, not the colour, so actor strokes and badge borders follow. |
| Two citation treatments in one video | 🟡 Moderate | **Fixed.** Unified on the mono pill. |
| Lane scenes are top-heavy; the lower third is reserved for foot copy that enters later, so several frames read bottom-empty | 🟢 Minor | **Accepted.** The space is reserved, not wasted — it fills as the beats land. Recorded for the next long-form piece. |
| Actor stroke weight is light at 1920 width; the free-coil state reads as thin squiggles more than as a dispersed tangle | 🟢 Minor | **Accepted for this cut.** The three states are still distinguishable at a glance, which is the job. Noted in the catalog entry as the thing to redraw per ingredient. |

### Accessibility
- Contrast: `check`'s pass measures WCAG AA on rendered pixels — **0 failures**.
  The citation pill measures 4.29:1 on mist (needs 3:1 at 32 px).
- Text sizes: hero 104 px, body 52 px, caption 44 px, chip 32 px — all at or above
  `[S6/A-6]`'s floors, with 32 px the absolute floor for anything meant to be read.

## Warnings left standing, with reasons

- `lint / overlapping_gsap_tweens` ×1 — two tweens touch one element in an
  overlapping window by design (a `swap` re-states its panel while the copy
  scales in). Intentional.
- `layout / container_overflow` ×3 (+13 info) — a `hold` drift scales the padded
  stage ~1.5%, so its **box** crosses the canvas edge by ~15 px. No **ink** does:
  the safe-area scan on rendered pixels reports no findings across 720 frames,
  and that scan, not a bounding-box test, is the authority here.
