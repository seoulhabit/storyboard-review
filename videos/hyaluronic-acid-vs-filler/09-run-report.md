# Run report — hyaluronic-acid-vs-filler (v2 revision)

## Summary

- Mode: `full` (revision) — S0.0 ran; S0–S3 skipped, reused from the 180s
  cut (subject and seed keyword unchanged); S4–S7 ran; S8 updated in place;
  S9 skipped, nothing published
- Result: `complete`
- Artifacts: 10 files under OUT changed, plus 2 new files in `catalog/`
- Spend: `$0.32 of $5.00` (`6.4%`) · vidIQ `0 of 200` credits this run (`0%`)
- Needs Kim: the publish click — `vidiq_update_video` was never called

Rendered **`06-render/final.mp4`** — 1920×1080, 30 fps, **160.000 s / 4800
frames**, 27.4 MB. Every gate measured on the shipped file, not an
intermediate: `hyperframes check` **ok: true** (0 errors across lint /
runtime / layout / motion / contrast, 3 accepted warnings), safe-area
**no findings across 640 sampled frames**, **−14.5 LUFS / −2.3 dBTP**, cadence
**16.5%** active share against the long-form comparators' 14.0-15.1%. This
is the fourth render: a `/code-review high` pass on the opened PR (#11)
found 10 real issues in the generator scripts before merge, all fixed and
re-verified — see "Post-review fix pass" below.

This is a **revision**, not a fresh build: operator feedback on the shipped
180 s two-hander (commit `48c29d9`) asked for one female narrator, a tighter
runtime, the thesis stated in the opening line, and ten named supporting
visuals returning to the existing three-lane diagram as a backbone. The
underlying claims and their sourcing are unchanged; C0 (the opening thesis)
is the only new claim, backed by the same C5/C7/C8/C9 evidence already on
file. Full account of what changed and why: `01-story-brief.md` §v2 Revision.

**Three things worth your attention before publishing.** First, **three
renders were needed for this revision**, not one — two cleared real
safe-area violations the pixel gate caught that `hyperframes check`'s
layout pass could not see (a genuinely-too-tall panel forcing ink into the
reserved bottom zone at t≈51.5s; a hold-drift pushing already-tight content
over the same line at t≈132s). Second, **two visual bugs were caught only by
looking at extracted frames**, not by any gate — a duplicated skin-cross-
section label from calling one helper twice, and text clipped off the
bottom of the canvas from an under-budgeted column. Third, **this run
carries forward, not re-verifies, the topic/title/thumbnail research** from
the 180 s cut — nothing about the subject or seed keyword changed, so
re-scoring would have spent credits to re-derive the same answer.

## Stages

| Stage | Ran / skipped | Gate result | Tool calls | Minutes |
|---|---|---|---|---|
| S0.0 Environment | ran | pass (no gate) | `hf transactions`, `npx hyperframes --version` | 2 |
| S0 Baseline | **skipped** | — | reused `videos/_channel/baseline.yaml` as of the 180s run; not re-fetched, no new data changes the revision's decisions | 0 |
| S1 Story | **skipped** | — | subject unchanged; claim table (`01-story-brief.md` §Sourcing) carried forward with one addition (C0) | 0 |
| S2 Topic gate | **skipped** | — | seed keyword unchanged (`hyaluronic acid filler`) | 0 |
| S3 Packaging | **skipped** | — | title/thumbnail already scored (95 / 77) and still accurate to the revised content; `02-packaging.md` v2 note explains why not re-run | 0 |
| S4 Script + VO | ran | **pass, 1 generation pass** | `hf generate_audio` ×1 + `generate_audio_batch` ×5, `jobs_wait` ×9 (13 stems total; repeated 429 rate-limit retries at >2 concurrent) | 22 |
| S5 Beat sheet | ran | pass after 1 revision (chapter floor) | `build_beats.py` ×2 | 4 |
| S6 Composition | ran | pass | `beats_to_composition.py` ×4, `build_actors.py` ×5, `continuity-audit.py` | 41 |
| S7 Render QA | ran | **pass after 4 renders / 4 check-fix cycles** (4th render is the post-code-review fix pass, below) | `check` ×7, `render` ×4, `ffmpeg` ×9, `check-safe-area.py` ×4, `check-static-hold.py` ×2, `check-cadence.py` ×2, `continuity-audit.py` ×1 | 65 |
| S8 Publish envelope | ran — **updated in place** | pass — no write calls | manual edit: chapters, description opening, `[K-5]` count, end-screen scene ref | 5 |
| S9 Readout schedule | **skipped** | — | nothing published; `08-readout-schedule.md` unchanged, still valid (relative to publish moment, not to cut version) | 0 |

## Skills and tools invoked

| Stage | Companion / tool | Result |
|---|---|---|
| S6 entry | `frontend-design` | `COMPANION-RESOLVED:frontend-design (skill-tool)` — self-critique against the skill's framework on the ten new hand-authored scenes; no changes needed, token discipline holds (no new hues or fonts, only scoped sizes where layout math required them) |
| S7 | `design-critique` | `COMPANION-RESOLVED:design-critique (skill-tool)` — 2 findings fixed (both confirmed real by the pixel gate), 2 accepted (unchanged from the 180s cut's own accepted findings) |

MCP/tool calls in stage order: `hf transactions`, Higgsfield `generate_audio`
×1 + `generate_audio_batch` ×5 + `jobs_wait` ×9, `ffmpeg` (trim/concat/mux/
loudnorm ×2-pass/ebur128) ×8, `npx hyperframes check` ×6, `npx hyperframes
render` ×3, `check-safe-area.py --landscape` ×3, `check-static-hold.py
--landscape` ×1, `check-cadence.py --longform` ×1, `continuity-audit.py` ×1.

## Rules fired

The five that changed what got produced (full list carried in
`00-decision-ledger.md`'s `## re-run` section, appended not overwritten):

1. **`[S1/S-4]` reverts to ordinary single-voice.** Dropping Jay/Grady
   retired the `[NOT IN SKILL]` two-hander gap the 180s brief logged —
   this video no longer exercises that policy question, though the filed
   proposal stands for any future multi-character script.
2. **`[S1/S-2]` length, band upper bound, not midpoint.** Trimmed speech
   alone (13 single-voice stems) measured 151.75s — already over the
   requested 150s midpoint before a single gap was added. 160s (the band's
   own stated top) was the tightest target leaving any pause budget at all;
   the alternative was cutting real content (the FDA safety passage) to
   force a lower number.
3. **`[S6/A-1]` reuse, twice over.** `MoleculeStates` — itself harvested
   from this project's own 180s cut — reused unchanged for all three
   persistent actors. A confirmed gap (no cataloged skin cross-section
   despite three uncataloged one-offs elsewhere in the repo) was filled and
   harvested back as `SkinBand` before this run ended, not left as a
   fourth one-off.
4. **`[S7/R-2]` post-render pixel gate, twice.** Caught what `check`'s
   layout pass structurally cannot: real ink in the reserved safe-area zone
   on two different scenes, on two different full renders, both times with
   `check` reporting 0 layout errors. The gate exists because the layout
   pass checks declared containers, not the canvas edge a flex column can
   silently exceed.
5. **`[S6/A-9]` continuity, deliberately scoped down.** The full text
   describes merged multi-phase sub-compositions with true camera legs;
   this run kept the SAME proven separate-scene-file idiom the 180s cut
   shipped clean with (shared deterministic actor-drawing functions, not
   duplicated logic) rather than building true camera-leg dives — a
   scope decision for ten new scenes' worth of novel geometry in one pass,
   logged rather than silently substituted. `continuity-audit.py` still
   measured 0 rebuilt-actor pairs.

## Post-review fix pass

Operator requested a code review of PR #11 before merging. `/code-review
high` ran 8 finder angles against the diff plus independent 1-vote
verification on every surviving candidate: **10 findings, all CONFIRMED**,
all in `build_beats.py`/`build_actors.py` (the generator scripts, not
`01-story-brief.md` or any claim/sourcing content). Full list with root
causes: `00-decision-ledger.md`'s `## re-run — code-review fix pass`
section. Operator then asked to fix before merging rather than file as
follow-up.

Four correctness bugs (a hold-beat/next-beat overlap miscalculation, two
scenes bypassing the shared `_row_tweens()` entrance helper via hand-rolled
loops, one scene's `layout` metadata label not matching how it actually
renders) and six cleanup findings (a success counter that could report
success on a silently-failed regex substitution, one string-replace hack
replaced with a proper parameter, a triplicated constant hoisted to one
definition, three unread seeded RNGs removed, one dead list removed, one
undocumented recurring hand-tuning pattern documented). Two of the ten
(the `_row_tweens()` fixes) changed rendered pixels; the rest were
generator-code-only with no visual effect.

Fixed, committed (`8b41964`), and the full pipeline re-run from
`build_beats.py` through render: beat sheet still totals exactly 160.000s
with 0 hold-beat overlaps, `check --json` still `ok: true` with the same 3
accepted warnings, and all three pixel gates (safe-area, static-hold,
cadence) re-verified clean on the new `final.mp4` rather than assumed
carried-over. Cadence moved 18.1% → 16.5% (see `06-render/qa-log.md`) —
the two `_row_tweens()` fixes changed *which* tween ran, not whether the
scene reads as active; still above the 180s cut's 15.1%. Extracted frames
at both fix sites confirmed no visual regression.

## Spend

| Provider | Stage | Measured |
|---|---|---|
| Higgsfield `generate_audio` (seed_audio, Kimberly) | S4 | **16.1 credits = $0.322** — measured via the `transactions` tool, not estimated |
| vidIQ | — | 0 credits (S0–S3 all reused, not re-fetched) |
| HyperFrames render | S7 | 24 render-minutes across the first 3 renders, plus 1 more render for the post-review fix pass (not separately timed); `providers.yaml` has no per-minute rate, minutes logged not priced |

Total **$0.32 of $5.00 (6.4%)**. `BUDGET-WARN` and `BUDGET-CAP` did not fire.
Appended to `videos/_channel/spend.jsonl`.

## Artifacts

```
00-decision-ledger.md (appended, ## re-run section)   01-story-brief.md (rewritten, §v2 Revision)
02-packaging.md (v2 note)                              07-publish-envelope.md (chapters/desc/K-5 updated)
03-beat-sheet.json (regenerated)                       cost-log.jsonl (VO entry appended)
build_beats.py (13-scene SCENES list)                  build_actors.py (7 new scene builders + fixes)
04-assets/  script.md (rewritten) · vo-stems.json (13 single-voice stems) ·
            vo-timing.json/vo.mp3 (re-measured, 160.000s) ·
            vo/ (13 new stems, old 25 replaced) · build_vo.py (TARGET=160.0)
05-composition/  index.html · index.motion.json · compositions/frames/ (13,
                 was 14) — regenerated from scratch each fix cycle
06-render/  final.mp4 (160.000s) · raw.mp4 · check.json · qa-log.md
            (rewritten) · loudnorm-pass1.json (two-pass measured values) ·
            frames/, frames-final/ (extracted for review)
```

Outside OUT:
- `catalog/visual-components/skin-band/` — **new**, the `[S6/A-1]` contribute
  half (README.md + skinband-spike.html), registered in `catalog/README.md`
  and `catalog/index.html`
- `videos/_channel/spend.jsonl` — this run's line appended
- `videos/_channel/baseline.yaml` — **not touched** (S0 skipped, reused as-is)

## Skipped and why

- **S0/S1/S2/S3 all skipped** — this is a revision of an already-fully-
  packaged video. Re-running baseline/topic/title/thumbnail research would
  have spent vidIQ credits to re-derive answers the subject change doesn't
  affect. See `02-packaging.md`'s v2 note for the explicit reasoning.
- **S9 readout skipped** — nothing is published; unchanged from the 180s
  cut's own state. `08-readout-schedule.md` was not touched because it is
  relative to the publish moment, not to which cut is live at that moment.
- **True camera-leg continuity (`[S6/A-9]`'s full mechanism) not built** —
  see Rules fired #5. Logged as a scope decision, not an oversight.

## `[NOT IN SKILL]` findings

None new this run. The five findings the 180s run filed to
`videos/_channel/policy-change-proposals.md` (multi-character script gap,
three generator motion defects, dark-ground ink-on-ink, digit-leading-id
severity, ambiguous long-form `maxStaticSec`) all still apply to the shipped
generator and were worked around here the same way they were worked around
there — none were re-discovered as new, none were silently no longer true.

## Deviations, stated rather than buried

- **This revision overwrote the 180s cut in place** rather than landing as a
  sibling recut directory (the repo's own precedent —
  `snail-mucin-recut-34s`, `centella-barrier-recut-15s`). Operator's explicit
  choice this session, recorded in the plan approved before work began. The
  180s two-hander stays fully recoverable at commit `48c29d9`.
- **Target length landed at the requested band's upper bound (160s), not the
  midpoint (150s).** See Rules fired #2 — a measured constraint, not a
  preference.
- **Two full-render cycles were spent on defects `hyperframes check` reported
  as completely clean (0 errors) both times.** Real ink in the reserved
  safe-area zone, caught only by the pixel-level gate. Recorded because it's
  the sharpest evidence in this run for why that gate is authoritative and
  the bounding-box layout pass is not a substitute for it.

## Next readout

Not scheduled by this run — nothing is published, and this revision doesn't
change that. `08-readout-schedule.md` (unchanged from the 180s cut) holds
both readouts with the exact calls and the medians to compare against.
**What would trigger one: the publish click.**

Compare against `curve.p50_48h` **15.5** (band 7–31.5) and
`retention.avg_view_pct_short` **48.81%** — and mark every one of those
comparisons `[UNDERPOWERED]`, because the curve is built entirely from
Shorts and this is the channel's first long-form piece.
