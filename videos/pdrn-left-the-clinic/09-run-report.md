# 09-run-report.md — pdrn-left-the-clinic

Skill version 0.3.0, resolved from `claude-skills-current` `master` @
`9c14bb9` — symlink clean, no drift to work around this run.

## Summary

- Mode: `new` → `full`, **deliberately stopped after S1** (Phase A/B, per
  this run's own plan). S4b (VO), S5b (compile) and S6 (render) did not run.
- Result: **the two things this run could actually finish, finished** — a
  written build-spec request pushed live to the Claude Design project, and
  the fully-sourced `[K-1]` claim table plus decision ledger. The video
  itself does not exist yet, and should not: the design system this brief
  targets has zero imagery primitives, and every visual named in the brief
  (bottle in darkness, camera through it, DNA transform, clinic, retail
  aisle) is unbuildable on it today. That is a system-level gap, not a
  fixable-in-run problem, and the system's own readme says exactly what to
  do about it — file a written spec and get a ruling, not invent a
  workaround. §A1 of the request does that.
- The claims are in much better shape than the brief assumed:
  `videos/_queue.yaml`'s "citations: 2, findings: 1" for `pdrn` is stale;
  the real corpus at the pinned SHA (`cacff81`) has 17 findings, 15
  verified. The brief's own draft slightly overclaimed the evidence gap
  (implying no topical trial exists) — one does (finding C7), and it had to
  be added to the K-1 table, sized honestly, not omitted or overstated.
- Spend: **$0**. No HeyGen or vidIQ credit-bearing call was made — both
  balances were read (243+41 HeyGen credits, 325 vidIQ credits) but nothing
  was spent against either.
- Needs Kim: **three rulings**, named below and in `00-decision-ledger.md`'s
  "Open" section, plus whatever Design decides on the pushed request. None
  of them are guesses papered over — each is logged as open, not resolved
  by assumption.

## Stages

| Stage | Ran / skipped | Result | Tool calls | Notes |
|---|---|---|---|---|
| S0.0 Environment | ran | clean, no BLOCKER | 2 (`get_current_user`, `vidiq_balance`) | MANIFEST re-derived clean, 67/67, independently of the shipped manifest tooling |
| S0 Baseline | skipped | — | 0 | `baseline.yaml` current (`updated: 2026-09-03`), not stale |
| S1 Story | ran | pass, with one correction | 0 | K-1: 8 sourced / 1 nominal / 4 editorial / 0 unsourced; the C7 correction, and the regulatory beat's cross-outlet corroboration, are this stage's real work |
| Phase A (Design request) | ran | pushed, awaiting Design's ruling | 3 (`list_files`, `finalize_plan`, `write_files`, `get_file` verify) | `videos/_system/REQUESTS/2026-09-07-imagery-and-longform.md`, read back byte-identical from the live project |
| S2 Topic gate | not run | — | 0 | blocked behind Design's ruling — the presenter/visual direction this stage would score depends on it |
| S3 Packaging | not run | — | 0 | same |
| S4 Script | not run | — | 0 | typographic beat map in `00-decision-ledger.md` stands in as the structural spine |
| S4b VO pre-flight | not run | — | 0 | brief's VO choice is a fence override (see below), not re-verified live this run |
| S5b Composition | not run | — | 0 | compiling now would either render the wrong visual direction silently, or require inventing components outside any ruling — both forbidden by this run's own plan |
| S6 Render | not run | — | 0 | — |
| S7/S8/S9 | not run | — | 0 | — |

## What this run found that the brief did not know

1. **The claim counts in `videos/_queue.yaml` are stale**, not a reflection
   of the actual source corpus. Anyone popping this slug from the queue on
   the stated "citations: 2, findings: 1" would have under-scoped the K-1
   pass badly. Worth a general note: the queue file warns its own counts
   don't auto-refresh — this is the first time that warning was load-bearing
   in a real run.
2. **The regulator beat (§3, 3:10–3:50) is sourced with real numbers**, not
   the unsourced-framing fallback the brief pre-authorized cutting to. 106
   MFDS violations over 4 years, 81 of them (76.4%) for making cosmetics
   sound like medicine, driven by the Rejuran injectable boom — confirmed
   across 7 independent Korean trade-press outlets reporting one National
   Assembly disclosure. Do not cut this beat.
3. **The design system has no imagery primitive at all** — confirmed
   directly against the live Claude Design project (`DesignSync
   list_files`/`get_file`), not just the local extraction. This is the
   headline finding of the run: the brief's entire visual direction needs a
   ruling before any of §3 can be built as written.
4. **One correction to the brief's own evidence framing was necessary**:
   finding C7 is a real topical PDRN RCT (31 women, split-face, vs.
   low-dose retinol, ~2× improvement on several measures). The brief's
   draft leaned toward implying topical evidence doesn't exist; it does,
   thinly. K-1 requires stating what's actually there, not the version that
   makes the strongest narrative point.

## Rulings needed from Kim

1. **Design's answer to `REQUESTS/2026-09-07-imagery-and-longform.md`** —
   extend the system with the 5 proposed components, or hold it typographic
   and build from the fallback beat map already proven in
   `00-decision-ledger.md`.
2. **The VO fence override.** The brief's Higgsfield/Kimberly choice is
   reasonable (HeyGen `create_speech` still 402s) but collides with `H-0`'s
   own text ("not a fallback... may not be called"). Recommend blessing it
   as a named policy amendment, not a silent one-off.
3. **The format override + the skipped vertical-slice-first advice.** `S-1`
   would default this channel to short; the brief overrides to long, and
   `S-1`'s own note to prove a first-of-kind format on a short slice before
   committing a full runtime was not followed. Recommend deciding this
   together with Design's A3 answer (the runtime/template mismatch), since
   both bear on what "the video" actually is before more work goes into it.

## Deviations from a normal `full` run

- Stopped after S1 by design, not by a blocker. Documented in
  `00-environment.md`'s scope note and repeated here so it isn't mistaken
  for an incomplete run that simply ran out of steps.
- No render, no publish envelope, no readout schedule — all downstream of
  the stopped stages, not separately skipped.

## [NOT IN SKILL]

- The vidIQ 8-call cap the WO specifies in three places has no
  implementation anywhere in the shipped skill (confirmed again this run —
  not re-litigated, just re-observed). Not exercised this run since S2/S3
  didn't run, but worth folding into `policy-change-proposals.md` before
  the next run that does reach vidIQ calls.
