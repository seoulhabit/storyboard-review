# Run report — kbeauty-label-trap

Skill version 2.1.0.

## Summary

- Mode: `full` — S0.0 ran; S0 baseline reused (fresh as of today); S1–S8 ran; S9 scheduled but not executed (nothing published); **plus one post-report revision round** addressing both design-critique follow-ups and the cadence gate's flagged pacing gap
- Result: `complete`
- Artifacts: 10 numbered outputs under `videos/kbeauty-label-trap/`, plus 3 files appended/updated in `videos/_channel/` and 4 findings filed to `policy-change-proposals.md`
- Spend: `$0.48 of $5.00` (`9.6%`) · vidIQ `62 of 200` credits (`31%`) — unchanged by the revision round (no vidIQ/Higgsfield calls, render compute only)
- Needs the operator: the publish click — `vidiq_update_video` was never called

Rendered **`06-render/final.mp4`** — 1920×1080, 30fps, **257.133s / 7714
frames**, 14.9MB. Every gate measured on the shipped file, not an
intermediate: `hyperframes check` **ok: true** (0 errors across lint /
runtime / layout / motion / contrast; 6 warnings + 18 info, all one
transition's clip-path-unaware false positive, visually confirmed clean),
`check-safe-area.py --landscape` **0 findings across 1028 sampled frames**,
**-16.10 LUFS / -1.80 dBTP**. This is the **third render**: the first was
check-clean but a manual review of every extracted frame found 4 real
defects (fixed in render 2); render 2 fully re-verified clean; render 3
addressed the two design-critique follow-ups plus the cadence gate's
flagged 12-scene pacing gap (see "Revision round," below).

**Revision round (post-report).** The operator said "continue" after the
original run report named the design-critique's two follow-up findings and
the cadence gate's pacing gap as the natural next targets. Both design
findings are now substantially fixed and pixel-verified: s05's composition
was rebuilt from two dots in a corner into a vertical concentration-axis
diagram using the full canvas with intent (independently corroborated by
`check-static-hold.py`'s before/after diff — an 8.5s content-void in that
scene's region is now gone entirely), and s01's vertical ribbon text was
converted to legible horizontal micro-columns. The cadence fix is more
qualified: real, verified motion was added to all 12 flagged scenes
(confirmed by direct pixel-diff at the tool's own 0.125s comparison
granularity — mean |dLuma| 0.042 but max pixel delta 86 in the tested
window), but `check-cadence.py`'s own summary numbers are unchanged,
because its `mean|dLuma|>=1.0 AND maxpix>=40` gate is diluted by whole-frame
averaging for motion confined to small icons — a genuine tool-methodology
limitation, filed as `policy-change-proposals.md` P9, not an unfixed
defect. Not chased with a fourth render: the gate is advisory, the motion
is confirmed real and human-visible, and enlarging it purely to move a
metric would trade away the "restrained, subtle" brief the fix was built
to satisfy. Full account: `06-render/qa-log.md` §Revision round.

This is the channel's **third long-form video**, not its first (the two
priors, `ectoin-survival-molecule` and `hyaluronic-acid-vs-filler`, are both
private/unpublished) — and will be the first one this run's own operator
could choose to make public, which would make it the channel's first *public*
long-form retention data point.

**Three things worth your attention before publishing.**

First, **a full-render, check-clean video can still fail on frames no gate
looks at.** `hyperframes check` reported 0 errors on the first render; a
manual review of all 16 extracted frames (frame 0, each scene's settle
point, the video's true last frame) found the video's real final ~0.45
seconds rendered **solid black** — a structural bug where every scene's own
`data-duration` used the beat sheet's nominal duration while `index.html`'s
wrapper keeps each clip mounted longer (the transition-overlap formula).
This affected the tail window of **8 of 14 scenes**, not just the one
caught visually; it's fixed centrally in `build_composition.py`, not
patched per-scene. Two more real defects (a blank-reading frame 0, two
separate text/graphic overlaps) came from the same manual pass. See
`06-render/qa-log.md` for the full account and `videos/_channel/
policy-change-proposals.md` P6 for the filed generalization.

Second, **two advisory gates found a real, unaddressed craft gap.**
`check-cadence.py` and `check-static-hold.py` (both always-exit-0 by
convention) agree: 12 of 14 scenes hold static for well past their 6-second
quiet ceiling — up to 30 seconds in the evidence-tunnel scene — while
narration continues. This is logged, not fixed, in this run: both gates are
advisory, the video is already on its second full render, and the
underlying content, claims, and safe-area compliance are all correct. It's
the clearest single target for a revision round if one happens.

Third, **the claim-sourcing chips were built into the shared CSS but never
wired to an actual claim** until this was caught reading the generated HTML
directly, before the first render. All five fact-check anchors were fetched
and read live (not recalled) before any claim table entry could cite them —
see `01-story-brief.md` §Sourcing for the full accounting of what's sourced,
what's flagged unsourced, and why the fictional two-bottle comparison is
illustration rather than a claim needing either treatment.

## Stages

| Stage | Ran / skipped | Gate result | Tool calls | Notes |
|---|---|---|---|---|
| S0.0 Environment | ran | pass (no gate) | `vidiq_balance`, `hyperframes --version`, Higgsfield `balance`+`list_voices` | Skill confirmed already at latest (`6d70e4d` == origin HEAD). HyperFrames CLI version bumped 0.8.26→0.8.27 mid-run from a concurrent session's global upgrade — a transient hiccup, not this run's action. |
| S0 Baseline | **skipped (reused)** | — | none | `baseline.yaml` stamped `updated: 2026-09-03` (today) |
| S1 Story | ran | pass — 6/6 sections grounded | WebFetch ×3, PubMed MCP ×2 | Hook restructured (passport-thesis lines moved to Misconception) to clear the 20s hook cap **and** supply Misconception's previously-missing wrong-belief sentence — one fix, two gaps closed |
| S2 Topic gate | ran | pass after 1 seed swap | `vidiq_keyword_research` ×1, `vidiq_outliers` ×1 | Seed `k-beauty ingredient label` had 0 measurable demand; swapped to `k beauty`, specificity loss logged plainly |
| S3 Packaging | ran | pass | `vidiq_score_title` ×5, `vidiq_similar_thumbnails` ×1, `vidiq_generate_thumbnail` ×1, `vidiq_score_thumbnail` ×1 | Title 96/100 (= operator's own primary); thumbnail self/independent score 89/89, no refine needed |
| S4 Script + VO | ran | pass, 1 generation pass | Higgsfield `generate_audio` ×9 | 646 words, 29 under the 675 floor — not padded, per operator decision. Concurrency-throttled to one-stem-at-a-time (see Deviations) |
| S5 Beat sheet | ran | pass | none (computed from `vo-timing.json`) | 14 scenes, tiling 0–257.12s exactly; end-scene split required to clear the 20s cap |
| S6 Composition | ran | pass, 2 fix cycles | `hyperframes check` ×3, `continuity-audit.py` ×2 | GSAP/CSS transform conflicts, a non-transform-motion warning, a contrast floor miss, a layout overflow — all fixed |
| S7 Render QA | ran | pass, 3 renders (2 original + 1 revision round) | `hyperframes render` ×3, `ffmpeg` ×~18, `check-safe-area.py` ×3, `check-static-hold.py` ×2, `check-cadence.py` ×2, `continuity-audit.py` ×2 | 4 real defects found by manual frame review in round 1, not by any gate; round 3 (revision) added verified cadence motion + 2 design fixes — see Summary |
| S8 Publish envelope | ran | pass — no write calls | none | Draft only; end-screen "watch next" slot has no public long-form video to point to yet |
| S9 Readout schedule | **scheduled, not executed** | — | none | Nothing published this run; `08-readout-schedule.md` written with both readout calls ready |

## Skills and tools invoked

| Stage | Companion / tool | Result |
|---|---|---|
| S3 entry | `frontend-design` | `COMPANION-RESOLVED:frontend-design (skill-tool)` — 2 corrections: locked porcelain as the default ground (vs. the AI-default near-black+accent look), moved the vermilion stamp onto the bottle itself in the thumbnail |
| S6 entry | `frontend-design` | `COMPANION-RESOLVED:frontend-design (skill-tool)` — identified the vermilion ink-stamp as the video's one signature device (passport ID, all 5 evidence seals, end-card lock — one component reused, not five invented) |
| S7 | `design-critique` | `COMPANION-RESOLVED:design-critique (skill-tool)` — signature device and dark/porcelain register both confirmed intentional; 2 follow-up findings logged, then both fixed in the post-report revision round (see Summary) |

MCP/tool calls in stage order: `vidiq_balance`, `hyperframes --version`,
Higgsfield `balance`+`list_voices`, `vidiq_keyword_research` ×1,
`vidiq_outliers` ×1, `vidiq_score_title` ×5, `vidiq_similar_thumbnails` ×1,
`vidiq_generate_thumbnail`+`vidiq_job_poll`+`vidiq_score_thumbnail` ×1 each,
Higgsfield `generate_audio` ×9 + `jobs_wait` ×~15 (concurrency retries),
`ffmpeg` (silencedetect/trim/concat/mix/mux/loudnorm ×2-pass/ebur128/
volumedetect) ×~20, `hyperframes check` ×3, `hyperframes render` ×2,
`check-safe-area.py --landscape` ×2, `check-static-hold.py --landscape` ×1,
`check-cadence.py --longform` ×1, `continuity-audit.py` ×3, WebFetch ×3,
PubMed MCP `search_articles`+`get_article_metadata` ×2 each.

## Rules fired

The ones that changed what got produced (full account in
`00-decision-ledger.md`):

1. **`[S1/S-1]` long 16:9, operator-directed, not first-of-kind.** Two
   prior long-form pieces exist but both are private — every
   retention/curve comparison this run makes is `[UNDERPOWERED]`, and the
   "prove on a vertical slice first" clause was skipped since prior art
   exists in letter even though it can't be measured against.
2. **`[S4/S-6]` hook cap forced a restructure, not a cut.** The supplied
   script's hook ran 28s against a 20s hard cap; the fix moved content
   already destined for Misconception rather than deleting anything,
   closing a second gap (Misconception's missing wrong-belief sentence) in
   the same move.
3. **`[S1/S-2]`/word budget: measured VO is the clock, not padded.** 646
   words is 29 under the 675-word floor for a 300s nominal target;
   operator decision (pre-run) was to let the real runtime land at 257.12s
   (12.5% under nominal) rather than invent narration to fill time.
4. **`[K-1]`/`[K-2]` claim table drove real content changes.** C6 ("some
   ingredients work at low levels") was reworded on-screen to "may be
   active at low levels" and flagged; C15 ("'Gentle' is never universal")
   was reworded to drop the absolute language before it ever reached a
   frame. A niacinamide-specific PubMed hit was found and **rejected** as a
   source for the general low-levels claim — the same claim-scope
   discipline `hyaluronic-acid-vs-filler`'s own C3/C4 split established.
5. **`[S6/A-9]` actor reuse, verified not asserted.** The hook and reveal
   scenes share identical bottle/bench markup; only the liquid-fill data
   differs between "ambiguous" (hook) and "resolved" (reveal) states.
   `continuity-audit.py` confirms 0 rebuilt-actor pairs across all 14
   scenes, not just these two.
6. **`[S6/A-8]` transition system lands at hard-cut 38% / wipe-left 46% /
   wipe-up 15%**, diverging from the plan's sketched 60/30/10 — the
   hard-cut is a deliberate repeated "return home to the bench" device
   (5 of its 5 uses are the bench snap-back), not per-scene fatigue.

## Spend

| Provider | Stage | Measured |
|---|---|---|
| vidIQ | S2, S3 | **62 credits** (5 outliers + 25×5 title scores + 5 similar-thumbnails + 22 generate-thumbnail + 5 score-thumbnail); `keyword_research` cost not itemized (no disclosed per-call rate) |
| Higgsfield `generate_audio` (seed_audio, Kimberly) | S4 | **~23.9 credits ≈ $0.48**, estimated from the `get_cost` preflight rate (1.7 credits/46 words) scaled to the full 646-word script — no per-call cost readout was returned by the actual generation calls |
| HyperFrames render | S7 | 2 full renders, ~17.2 wall-clock minutes combined; `providers.yaml` has no per-minute rate, minutes logged not priced |
| Gemini | — | not used, `no-key` |

Total **$0.48 of $5.00 (9.6%)**, **62 of 200 vidIQ credits (31%)**.
`BUDGET-WARN` and `BUDGET-CAP` did not fire. Appended to
`videos/_channel/spend.jsonl`.

## Artifacts

```
00-environment.md          00-decision-ledger.md        01-story-brief.md
02-packaging.md            03-beat-sheet.json           07-publish-envelope.md
08-readout-schedule.md     09-run-report.md (this file)
build_composition.py       scenes_01_03.py / scenes_04_07.py /
                            scenes_08_11.py / scenes_12_14.py
04-assets/  script.md · manifest.json · thumbnail.png · vo.wav/vo.mp3 ·
            vo-timing.json · vo/s00.wav..s08.wav (+ silence_report.json,
            trims.json) · music.wav · tokens/tokens.css (+ --vermilion) ·
            fonts/
05-composition/  index.html · hyperframes.json · package.json ·
                 compositions/frames/*.html (14) · assets/
06-render/  final.mp4 · check.json · qa-log.md · design-critique.md ·
            loudnorm-pass1.json · frames-final/ (19 extracted PNGs)
scenes_01_03.py / scenes_04_07.py / scenes_08_11.py / scenes_12_14.py
            (revision round: cadence fixes + design-critique follow-ups)
```

Outside OUT:
- `videos/_channel/spend.jsonl` — this run's line appended
- `videos/_channel/policy-change-proposals.md` — 4 findings filed (P6: a
  sub-composition's own duration must match its wrapper's transition-
  extended window, not the beat sheet's nominal value; P7: `check`'s
  overlap detector isn't clip-path-aware; P8: ffmpeg `amix`'s default
  `normalize=1` silently drops mixed-audio loudness when one input is
  already deliberately gain-staged; P9, filed in the revision round:
  `check-cadence.py`'s whole-frame mean threshold structurally under-counts
  real motion confined to small icons)
- `videos/_channel/baseline.yaml` — **not touched** (S0 skipped, reused as-is)

## Skipped and why

- **S9 readout not executed** — nothing is published yet. The schedule
  (`08-readout-schedule.md`) is written and ready; it fires from the
  operator's actual publish moment, which this run cannot supply.

## `[NOT IN SKILL]` findings

Four, all newly filed this run (see Artifacts, above, and
`videos/_channel/policy-change-proposals.md` for full text): a sub-comp
duration/wrapper-duration mismatch that renders as black rather than a
frozen frame; `check`'s clip-path-blind overlap detector; ffmpeg `amix`'s
default auto-attenuation fighting a manually gain-staged mix; and (filed in
the revision round) `check-cadence.py`'s whole-frame mean threshold
structurally under-counting real motion confined to small icons. All four
are generalizable beyond this project — filed as proposals, not worked
around silently.

## Deviations, stated rather than buried

- **Runtime landed at 257.12s against a 300s nominal target (12.5% under),
  not padded to match.** Operator decision, pre-run — see Rules fired #3.
- **A full render cycle was spent on defects `hyperframes check` reported
  as completely clean.** The blank frame 0, the s04/s12 overlaps, and the
  8-scene black-dead-zone bug were all found by manually reading every
  extracted PNG, not by any automated gate. Recorded because it's the
  sharpest evidence in this run for why "verify by pixels, never by
  manifest" is a mandatory rule and not a suggestion.
- **Both design-critique findings were addressed in a revision round**
  (s05 redesign, s01 ribbon legibility) — see Summary and
  `06-render/qa-log.md` §Revision round for the full account and
  pixel-level verification of each.
- **The cadence gate's finding was acted on but its own metric didn't
  move** — real motion was added and verified by direct pixel-diff at the
  tool's own comparison granularity, but `check-cadence.py`'s summary
  numbers are unchanged because of a diagnosed tool-methodology limitation
  (filed as P9), not because nothing was done. Not chased with a fourth
  render — see Summary for the reasoning.
- **`check-static-hold.py`'s findings were partially, verifiably improved**
  (the s05 redesign eliminated one region's 8.5s content-void entirely,
  confirmed by diffing the gate's own before/after output) but its total
  finding count is unchanged (24 voids both times) since content
  redistributed rather than disappeared — not claimed as a full fix.
- **Higgsfield spend is an estimate, not a measured figure** — the actual
  `generate_audio` calls this run used didn't return a per-call cost the
  way the `get_cost` preflight did; the $0.48 figure scales the preflight's
  rate by word count rather than summing real per-call charges.

## Next readout

Not scheduled by this run — nothing is published. `08-readout-schedule.md`
holds both the 48h and 7-day readout calls, ready to fire from the actual
publish moment. **What would trigger one: the publish click.**

Compare against `baseline.yaml`'s `retention.avg_view_pct_long: 43.07`
(n=2, both private, "not usable") and mark that comparison
`[UNDERPOWERED]` — this run's readout, once it happens, would be the
channel's **first usable public long-form retention data point**, not a
comparison against an existing curve.
