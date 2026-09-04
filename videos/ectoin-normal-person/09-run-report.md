# Run report — ectoin-normal-person (cold-open revision)

Written last, every mode, whether or not S9 itself ran.

## Summary

- Mode: `full (revision)` — S0.0 ran; S0-S3 skipped, reused from the shipped 5:59 cut (subject/seed unchanged); S4-S7 ran; S8 updated in place (thumbnail); S9 skipped, nothing published this run.
- Result: complete
- Artifacts: 38 files written or modified under OUT this run (see below)
- Spend: $0.082 of $5.00 cap (1.6%)
- Needs Kim: the publish click

This is a **revision**, not a fresh build. Operator feedback rewrote the
opening: the "11% bottle -> it's a blend -> turn the bottle around" reveal
moves to frame 0; the bacteria-origin material compresses to one narrated
raisin beat; the section closes on "Skincare borrowed the molecule.
Marketing borrowed the drama." Full account: `BRIEF.md` §Cold-open revision,
`SCRIPT.md` §Changes, `DELIVERY.md` §Revision. Runtime 5:59.01 -> 4:57.02.

## Stages

| Stage | Ran / skipped | Gate result | Tool calls | Minutes |
|---|---|---|---|---|
| S0.0 Environment | ran | no gate (records state) | hyperframes --version, higgsfield balance | 2 |
| S0 Baseline | skipped (mode=full, revision) | n/a | n/a | 0 |
| S1 Story | skipped (mode=full, revision) — spine reused, one new claim row set (C9-C11) added to BRIEF.md §Sourcing | n/a | n/a | 0 |
| S2 Topic gate | skipped (mode=full, revision) — seed keyword unchanged | n/a | n/a | 0 |
| S3 Packaging | skipped (mode=full, revision) for title (unchanged) | n/a | 0 | 0 |
| S4 Script + VO | ran | pass, 1 regeneration (t075, cap 2) | Higgsfield generate_audio x6 | 8 |
| S5 Beat sheet | ran (via build_frames.py/build_index.py/build_storyboard.py) | pass | build script passes x4 | 6 |
| S6 Composition | ran | COMPANION-RESOLVED:frontend-design (skill-tool, applied manually — no review mode in the plugin itself); pass after fixing 2 real bugs on the first check pass (id collision across sub-compositions, ambient-drift/camera tween overlap) | frontend-design invocation; 3 build+check cycles | 40 |
| S7 Render QA | ran | check: PASS 0 errors (5 cycles total, 2 more real bugs found by extracting frames — see below). Render: 297.025s, 8911 frames. Master: PASS (-14.7 LUFS, -2.2 dBTP). Postrender: safe-area PASS 0/1188, static-hold whole-frame PASS 0/594, static-hold region-aware 4 benign findings, cadence 13.7% (>= 13.0% shipped baseline), continuity `--gate` PASS. COMPANION-RESOLVED:design-critique (skill-tool) — no blocking findings, one cosmetic note on the disclosure tag's real-device legibility | npx hyperframes render x2 (1 discarded — stale build mid-render), master-audio.py x2, check-*.py x4 explicit, continuity-audit.py x2, ffmpeg frame extraction x2 passes (24 frames total) | 55 |
| S8 Publish envelope | ran (thumbnail only) | rebuilt around the new hook, contrast re-measured, grid-checked | Playwright capture (local, no MCP cost), ffmpeg grid-check | 8 |
| S9 Readout schedule | skipped (mode=full, revision) — nothing published this run | n/a | n/a | 0 |

## Skills and tools invoked

- S6: `frontend-design` — COMPANION-RESOLVED (skill-tool). The plugin's own content is authoring guidance for a fresh page, not a review capability, so its token/type-floor/contrast lens was applied manually against the built `compositions/frames/01-bottle.html` and `02-origin.html`. Findings: token discipline clean; illustrative-label tag correctly set at the `--t-chip` (32px) floor; swap-panel contrast 8.32:1 and 16.81:1.
- S7: `design-critique` — COMPANION-RESOLVED (skill-tool), applied against 5 extracted frames (frame 0, INCI payoff, ink-ground dialogue post-fix, endscreen bookend). No blocking findings; one cosmetic note (disclosure-tag legibility at real-device scale, not gating).
- S4: Higgsfield MCP `generate_audio` x6 (5 new turns + 1 regeneration on t075, accepted at the cap on tail-decay evidence).
- S7: `npx hyperframes@0.8.22 check --samples 60` x5 (1 initial + 4 fix cycles across the whole revision); `npx hyperframes@0.8.22 render` x2 (1 discarded before completion — a stale build was mid-render when a real bug was found in the source, restarted after rebuilding); `catalog/tooling/check-dead-sets.py` x5; `check-static-hold.py`/`check-safe-area.py`/`check-cadence.py`/`continuity-audit.py`, run explicitly (not via npm's `postrender` lifecycle hook, which auto-fires on `npm run render` and the first time scanned a stale unmastered file — see `DELIVERY.md` §Revision for the full account).

## Rules fired

24 ledger lines this run (`00-decision-ledger.md`). The five that changed the outcome:
1. `[S4/V-2]` VO duration/regeneration cap — t075 regenerated once, accepted at the cap on tail-decay evidence (0.03s window already below the silence threshold) rather than a third generation.
2. `[S6/A-9]` camera/actor persistence — drove the two-unit merge (01-bottle, 02-origin) reusing 03-cell's and 12-bottle's actors rather than redrawing, and the endscreen bookend rebuild once the retired hook's brine field was found to no longer match frame 0.
3. `[S6/A-1]` catalog-first — no bottle/brine/cell/molecule catalog entry existed (confirmed by survey); reused within-project mechanisms instead of generating new plates.
4. `[K-2a]` unsourced-quantity prohibition — governed the bottle's "11%" as an illustrative prop with a disclosure tag, not a bare claim, in both units that show it.
5. `[S7/R-1]`/`[S7/R-2]` errors-gate-the-run and verify-by-pixels — 2 errors blocked the first check pass (id collision, tween overlap), and 2 more real bugs (invisible text from a missing `ground="ink"`, a layout-property lint violation) were found only by extracting and inspecting frames at full resolution, exactly the failure class `[S7/R-2]` exists to catch.

Full list: `00-decision-ledger.md`.

## Spend

| Provider | Stage | Est. USD |
|---|---|---|
| Higgsfield | S4 (VO: 5 new turns + 1 regeneration) | $0.082 (4.10 credits) |
| — | S6/S7 (render, no published per-minute rate) | ~35 min logged, not estimated |
| — | S8 (thumbnail capture, local Playwright) | $0 |

Total: $0.082 of $5.00 cap (1.6%). Appended to `../_channel/spend.jsonl`.

## Artifacts

Full diff footprint under `videos/ectoin-normal-person/` this run:
- `scripts/vo_lines.py`, `scripts/frames_spec.py`, `scripts/build_frames.py`, `scripts/build_motion.py`, `scripts/build_storyboard.py` — 92K frames_spec.py (largest edit), rest mechanical
- `compositions/frames/*.html` — all 17 regenerated (VO timing shifted every downstream scene)
- `index.html` (32K), `index.motion.json` (4K), `STORYBOARD.md` (4K)
- `assets/voice/{t071,t072,t073,t074,t075}.wav` (5 new, ~1.5MB total) + `_takes.json`
- `captions/ectoin-normal-person.{srt,vtt}` — 88 cues (was 105)
- `assets/thumbnail/{cand-a.html,final.png,grid-check.png,grid-check-magnified.png,README.md}` — rebuilt
- `renders/ectoin-normal-person.mp4` — 80MB, 4:57.02, the publish candidate (`.raw.mp4` is gitignored)
- `BRIEF.md` (16K), `SCRIPT.md` (12K), `DELIVERY.md` (36K) — all updated with the revision's account
- `00-environment.md` (2.5K), `00-decision-ledger.md` (12K), `09-run-report.md` (this file) — new this run, this project predates the numbered-artifact convention
- `../_channel/spend.jsonl`, `../_channel/policy-change-proposals.md` — appended

## Skipped and why

- S0 Baseline: revision reuses the channel baseline as of the shipped 5:59 cut; nothing about this run's decisions depends on re-fetching it.
- S1-S2: subject and seed keyword unchanged from the shipped cut.
- S3 title/description scoring: unchanged claims and thesis; only the thumbnail needed rebuilding since the hook line it hard-coded was retired. Not vidIQ-scored this run — see `assets/thumbnail/README.md`.
- S9: nothing published this run; readout is scheduled from the eventual publish moment, not this cut.

## `[NOT IN SKILL]` findings

Appended to `../_channel/policy-change-proposals.md` (P6-P8):
1. No `revision` mode exists in the skill's mode table, and no written rule governs re-running S1-S4 on a partial script rewrite. This run followed the `hyaluronic-acid-vs-filler` v2 precedent (`full (revision)`, S0-S3 skipped and logged why).
2. No mapping exists from this project's pre-2.1 four-file format (BRIEF/SCRIPT/STORYBOARD/DELIVERY) to the nine numbered artifacts, and no exemption from writing the numbered ones either. Wrote `00-environment.md`, `00-decision-ledger.md` and `09-run-report.md` (mandatory, every mode) and folded `01-story-brief.md`'s required K-1 claim table into `BRIEF.md` §Sourcing.
3. In-place revision vs. a sibling recut directory has no written rule, and this repo has precedent both ways. Asked the operator before starting; recorded the answer (in place) in the approved plan.

## Next readout

Date: not scheduled — nothing published this run. Would trigger 48h/7d from
the eventual publish moment, compared against `curve.p50_48h` and
`retention.avg_view_pct_long` in `../_channel/baseline.yaml`.
