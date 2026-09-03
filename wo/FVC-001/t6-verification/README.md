# T6 Accept verification — evidence

These two files are **T6 Accept evidence, not a production run's artifacts.**

T6 requires that a `render`-mode run write `00-environment.md` (S0.0) and
`09-run-report.md` (final), and that the report's Stages table mark
S0–S4 and S8–S9 as `skipped (mode=render)` rather than omit them. Verifying
that needed an actual render-mode run, so one was executed on 2026-09-03
against an **isolated copy** of `outputs/2026-09-01-how-to-repair-skin-barrier/`
in a scratchpad directory.

## Why they live here and not in that output directory

The copy's source is a tracked, self-describing artifact set: its own
`00-decision-ledger.md` opens "Dry run of `faceless-video-craft` **v2.1**,
stages S1→S7". The report here says `Mode: render` with S5/S6 `ran (reused)`.
Filing it beside that ledger would put two contradictory records of the same
slug in one directory, and a later reader would reasonably take
`09-run-report.md` as that video's own production record. It is not one.
The original was left untouched — 9 entries, `06-render/raw.mp4` mtime
unchanged at Sep 1 21:35.

## Result

PASS, verified by parsing the Stages table rather than reading it:

- both files written, non-empty (37 and 112 lines)
- exact string `skipped (mode=render)` on S0, S1, S2, S3, S4, S8, S9 — all seven
- `ran` on S0.0, S5, S6, S7
- 11 of 11 stage rows present, none omitted
- S8 correctly stayed skipped: the mode table admits it only "+S8 if asked",
  and this run did not ask

Unlike T2, T6's Accept criteria matched the real mode table exactly, so there
is no mis-specification to record against it.

## What was and was not executed

Read the report's own §Skipped and why — it is written to be honest rather
than flattering. In short: S7's real gate (`hyperframes check`) ran and passed
(exit 0, contrast 21/21 WCAG AA, layout clean across 9 samples), but the
render/frame-extract/mux sub-steps reused the copy's existing outputs rather
than re-encoding, and both companion gates are logged
`COMPANION-RESOLVED:<name> (skill-tool)` but **not executed**, because the
stages they hook reused artifacts instead of authoring new ones.

S0.0's provider probe was real: vidIQ ok (2316 credits, via the 0-credit
`vidiq_balance`), Higgsfield ok, HyperFrames 0.8.26, Gemini `no-key`.
Total spend $0.00 of the $5.00 cap.
