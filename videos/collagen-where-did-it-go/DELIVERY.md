# DELIVERY — You Bought Collagen. Where Did It Actually Go?

**1920×1080 landscape · 30fps · RUNTIME_PLACEHOLDER · 8 composition files · 16 beat units · one narrator**

> The 3:09 two-character cut this project shipped on 2026-09-03 was withdrawn by
> the operator on 2026-09-04. This document delivers its single-narrator
> replacement and diagnoses what the first cut got wrong; `BRIEF.md` records the
> override itself.

---

## Retention diagnosis — what was wrong, and what replaced it

The first cut passed every per-frame gate it had and still read as a
presentation. The gates were not lying; they were answering a different
question. Each row below is the question that actually mattered.

| | Two-voice cut (2026-09-03) | This build | Why it matters |
|---|---|---|---|
| Runtime · words | 3:09.0 · 449 | RUNTIME_SHORT · 364 | 449 words of dialogue is a transcript with pictures |
| Voices · turns | 2 · 41 alternating | 1 · 15 spoken units | speaker switching was carrying the pacing; nothing else was |
| First word | **4.92s** | **FIRSTWORD_PLACEHOLDER** | five near-static seconds before anyone speaks is the whole hook budget |
| Curiosity loop opened | never (the twist arrives at 1:40 unannounced) | LOOP_PLACEHOLDER | the industry-funding reversal is the piece's best asset and was unadvertised |
| Composition files | 6, averaging 31.5s | 8, carrying 16 units | a 31s page is four beats pretending to be one |
| Longest quiet span | 5.62s (the gate's own measure) | see the gates table | measured on pixels, not on tween counts |
| On-screen language | two-lane dialogue cards; every spoken sentence also printed | ≤10-word beats, ~10 kinetic phrases, one deliberate duplicate | printing what is being said gives the viewer nothing to do |
| Transitions | 4 near-identical wipes + 1 hard cut | iris ×4, invert ×2, curtain ×1, each meaning something | one transition repeated is a slide deck's page turn |
| Climax | the 23-trial line held **6.6s** on a single beat | tiles tagged, dropped in two visible stages, result moving with them, then a 132px flood | the reversal is the reason to watch and it was a caption |
| Audio | 41 clips in one group | 1 master clip in one group, same 6-node chain | 41 clips is 41 chances for a level to drift |

**207 authored tweens is not the metric.** The first cut had them; the beat that
mattered still held for 6.6 seconds. What replaced tween-counting here is a
build-time assert (a *registering* beat — area × luma-delta ÷ duration — at least
every 4.0s inside every spoken file) plus two gates measured on rendered pixels.

---

## Changelog — what changed from the 3:09 two-voice cut

### Removed
- **The second speaker.** Jay (Dylan `b847bc29-…`, preset) and every trace of him: the `who` field on each line, the two-entry `VOICES` map, the per-speaker wav naming, the caption speaker prefixes, and the `NAMES` dicts in three generators.
- **The two-lane dialogue card system** — `LANE_CSS`, `lanes_html()`, `lanes_tl()`, the `.lane-soul`/`.lane-jay`/`.lane-name` block in `_preamble.BASE`, the per-scene ink-ground lane overrides, and the layout rows shaped around a dialogue band. Harvested to `catalog/visual-components/dialogue-lanes/` before deletion.
- **41 per-line audio clips** and the `retime_vo.py` / `pad_vo.py` conditioning they needed. One master clip replaces them.
- **The wordless cold open** (4.67s before the first word).
- **"Stay for the twist."** — spoken and printed at once, which the brief forbids, and the loop itself is the better tease.
- **`scripts/check-vo.py`** — the ectoin copy, importing a `LINES` table this pipeline no longer has and globbing a filename pattern that matched nothing. It reported "0 takes" as though the job were done.
- The `#mol` 6-cycle bob, the 5-cycle tile flicker and the `#world` y-drift added to satisfy a bounding-box motion tracker. Every one is replaced by a beat that says something.

### Condensed
- 41 dialogue turns → **15 spoken beat units**; 449 → **364 words**.
- Six ~30s scenes → **8 composition files carrying 16 units**, each file boundary a visible transition.
- The on-screen language stopped being a transcript: every text beat is ≤10 words (asserted at build time), with ~10 kinetic phrases carrying the moments that matter.

### Reordered
Contradiction (0.10s) → promise + the industry-funding curiosity loop (inside the first 10s) → skin as a building → the cream at the door → the powder through digestion → the evidence reversal → the practical hierarchy → the verdict, back at the building.

The loop the opening opens is paid off in `12-filter`, and only there.

### Redesigned, file by file
- **`01-hook`** — the powder molecule now splits off the racing one by scale instead of fading in; both files draw the helix at the same size, so the iris hands off one actor rather than two lookalikes.
- **`02-promise`** — rebuilt as three compositions on one set of nodes: the question drawn around the parked molecule, an ink data column that rises from the floor and shoves it aside, tags the industry-funded trials `$` and drops them **without showing a result**, then the column leaves and a shield draws around the molecule. The iris now opens from the molecule at (500,500) straight onto the building's shell.
- **`03-building`** — the building assembles from the ground up (floors drawn across bottom-first, door hung last, beams from the bottom storey); each UV cut flashes the beam coral and throws a shard off it; "replacing" is visibly attempted and fails (a beam starts to redraw, falls back, the building sinks) while "preserving" holds, with a camera pull-back that takes in the whole protected structure.
- **`06-door`** — the molecule grows against the 500-dalton dot while its own number counts; the three door attempts now reach the brick course and flash the jambs; the film spreads from where the molecule flattened; and the camera drops **below** the polished surface while "smoother" is still being said, to the hatch that is still cut. The animation makes the "not structural" case before the card states it.
- **`08-digestion`** — the dispatch dots were rendering at the tract exit from frame zero: `pathFollow` always wrote a frame-zero pose, and each dot's second call (its branch) overrode its first. The frame-zero write is now opt-out. Fragments condense by scale, and each destination panel is knocked as its dot lands.
- **`10-evidence`** — the climax. Tiles fall out of the field rather than dimming in place, and the result meter moves **with** them rather than after; the camera leans in for the filter and homes before the flood; the paper flood retracts on "the independent evidence" to reveal the survivor field beside the widened interval. The count-up to 23 moved from unit 10 to unit 12: unit 10's chip is Nutrients 2023, which pooled **26** trials.
- **`14-hierarchy`** — sunscreen locks **across** the foundation; the partial beam repair rides the protein line rather than the smoking line; the optional column is panned into frame instead of sitting there from t=0; the closing line is a full-width band with kinetic type.
- **`16-end`** — unchanged, held to 5.0s.

### Gates that were not gating
- `--ceiling`, `--exempt-last` and `--gate` were passed by `package.json` and **silently ignored** by both cadence checks: the argument filter kept only the profile flag, so `--ceiling` became the project root and the ceiling stayed at its default. Worse, `check-static-hold` set its ceiling *before* the landscape profile that overwrites it. Both now parse the flags, apply them after the profile, and exit non-zero under `--gate`.
- `package.json` named three gate scripts that **did not exist on any branch** — the chain died at the sixth command. `check-sfx-durations.py`, `check-motion-gaps.py` and `check-endscreen.py` are ported from `ectoin-survival-molecule`; `check-seams.py` and `check-final.py` are written for this project's shape.
- `build_frames.py` now refuses infinite repeats, cycled yoyos and `Math.random`, and asserts on the real manifest that the curiosity loop lands inside the first ten seconds.

---

## Verification

GATES_PLACEHOLDER

---

## Known findings, verified rather than suppressed

FALSEPOS_PLACEHOLDER

---

## Reproducing

```bash
python3 scripts/vo_lines.py          # print the two TTS prompts; both must be < 2048 chars
# generate both blocks with Higgsfield seed_audio, voice_type element,
# voice_id 674b71b8-1d2e-4087-8567-d1f53c0b9f3c, format wav, sample_rate 48000
python3 scripts/fetch_vo.py A <urlA> B <urlB>
npm run vo        # transcribe (whisper large-v3) -> verify -> cut -> walk -> seams
npm run build     # frames, bed, index, motion sidecar, captions, SCRIPT, STORYBOARD
npm run check     # hyperframes check, motion sidecar included
npm run render && npm run master
npm run gates     # safe-area, static-hold, cadence, continuity, blank, motion-gaps, sfx, seams, final
npm run qc        # contact sheets, phone-scale sheet, seam sheet
```

`index.html`, `compositions/frames/*.html`, `SCRIPT.md`, `STORYBOARD.md` and
`captions/*` are **generated**. Editing them directly survives a render and is
discarded by the next build — edit the generator. Every one carries a header
saying so.

**Stop any preview server before diffing or committing.** It rewrites
composition files in place, injecting `data-hf-id` as the first attribute on
every tag, so a generated file shows as dirty for reasons that have nothing to
do with your edit. `check-final.py` counts those attributes and fails on any.

---

## Still outstanding

OUTSTANDING_PLACEHOLDER
