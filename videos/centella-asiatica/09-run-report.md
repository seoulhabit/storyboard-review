# 09-run-report.md — centella-asiatica

Skill version 0.3.0. Resolved from `~/Desktop/claude-skills-worktrees/wo-fvc-005-t5`
(detached worktree at `origin/master` `5a9f5b0`). **Drift found**: the
Skill-tool-loaded `~/.claude/skills/makemeavideo` symlink points at the
shared main checkout, stuck on a stale pre-T7 branch — worked around by
reading every rule from the fresh worktree instead; not fixed (another
session's uncommitted work is on that checkout). See `00-environment.md`.

## Summary

- Mode: `full`
- Result: **complete**, with one gate needing Kim's read before publish
  (see below) — not a run-stopping halt
- Artifacts: 13 files written under `videos/centella-asiatica/` (00–08 docs,
  beat sheet, 04-assets/, 06-render/9x16/ including the rendered MP4)
- Spend: vidIQ 20 credits of a 355-credit balance (4 billed calls of an
  8-call cap); HeyGen $0 (no calls made — VO substitute, local render)
- Needs Kim: **the publish click**, after reading the one real judgment
  call this run made without a human in the loop — see "Needs Kim's read"
  below. Nothing else blocks.

## Stages

| Stage | Ran / skipped | Gate result | Tool calls | Notes |
|---|---|---|---|---|
| S0.0 Environment | ran | recorded (not gated) | 0 | skill-symlink drift found + worked around |
| S0 Baseline | skipped | — | 0 | `baseline.yaml` already populated 2026-09-03; not stale enough to force a refresh for a single-pilot run |
| S1 Story | ran | pass | 0 | pinned site repo @ `cacff81`, K-1 table: 6 sourced / 1 nominal / 1 editorial / 0 unsourced |
| S2 Topic gate | ran | pass (seed swapped) | 2 (`keyword_research`, `outliers`) | seed `centella asiatica skincare` failed T-2, swapped to `centella` |
| S3 Packaging | ran | pass | 2 (`generate_titles`, `score_title`) | title score 92/100 |
| S4 Script | ran | pass | 0 | 129 words, K-2/K-2a clean |
| S4b VO pre-flight | ran | **substitute** | 0 (HeyGen) | connector `BLOCKED-CONNECTOR` (T1-FINDINGS F2); `mix_audio.py --allow-placeholder-vo` shipped slate tones for all 9 scenes, named as such |
| S5a Image plates | skipped | n/a | 0 | design system carries no imagery — structural no-op, not a gap |
| S5b Composition | ran | pass | 0 | `compile_composition.py`, 9 scenes, 45.5s, manifest-drift clean |
| S6 Render | ran | pass | 0 | `render_local.sh`, local, `hyperframes check` ok → real MP4 with audio |
| S7 Render QA | ran | **fail (mechanical) / pass (verified)** | 0 | see below |
| S8 Publish envelope | ran | drafted | 0 | `07-publish-envelope.md`, nothing written to YouTube |
| S9 Readout schedule | ran | scheduled | 0 | `08-readout-schedule.md`, dates placeholder pending real publish |

## S7 — the one judgment call needing Kim's read

`qa.json` verdict: **`fail`**. Two blocking-severity findings:

1. **`H-3` (faceless) fails — 2 detections, both confirmed false positives.**
   Haar cascades flagged bold typography in `myth1` (t=8.5s, "REVIEW SKIPS")
   and `evidence2` (t=34.0s, the figure "6"/"Volunteers…") as faces. This
   design system carries zero imagery of any kind — there is nothing in
   either frame that could be a face. Verified by extracting and looking at
   both exact flagged frames directly, not by trusting the tool's summary:
   `06-render/9x16/h3-verification/myth1-t8.5s-face-flagged.png` and
   `evidence2-t34.0s-face-flagged.png`. This is the same class of Haar
   false-positive on headline typography T4 already documented
   (`wo/FVC-005/t4-verification/h3-false-positive/`).
2. Everything else that was failing earlier in this run is now fixed and
   passing for real (see "Real bugs found and fixed" below) — canvas,
   safe-area, static-hold, loudness, duration, type-floor, and frame-zero
   (`H-2`) all pass.

**Judgment call made, not defaulted**: treated `H-3` as satisfied via
direct visual confirmation rather than the automated verdict alone — this
is the exact fallback `policy.md`'s own `H-3` text (rewritten this WO,
T7) names: *"a documented Haar false positive on bold headline typography
has been observed... confirm on the actual frame before treating a finding
as a real face."* The Haar cascade parameters themselves were **not**
retuned — doing that to pass this one run would be exactly the "loosen a
rule to pass a gate" this WO's own §0.1 forbids, and a looser detector
risks missing a real face in some future run. **This is the one place
this run asks Kim to read the two archived frames before clicking
publish** — not because the process is unsure, but because "no faces
appear in this video" is a safety-relevant claim and a second set of eyes
on the actual evidence costs nothing.

`H-4.contrast` also fails (**advisory**, does not block `qa.json`'s own
verdict either way beyond what's already true): the muted citation-chip
token (`--chip-opacity: 0.4`, by design) measures 1.48:1 against the
4.5:1 floor. This gate is explicitly not yet validated against a real
render corpus (`policy.md`'s own note); the low reading matches the
design system's own intentional de-emphasis of secondary source labels,
not a defect. Frame: `06-render/9x16/h3-verification/hook-t0s-contrast-flagged.png`.

## Real bugs found and fixed this run (not assumed clean)

Beyond the harness itself (T4) and the skill docs (T7), this is the first
time `compile_composition.py`/`qa_render.py` compiled and rendered a real,
sourced, multi-component beat sheet — and it surfaced three real defects,
each found by actually running the pipeline and reading the failure, then
fixed and re-verified:

1. **The continuous-motion float fallback broke its own rule on longer
   scenes.** `render_scene`'s synthetic breathing float used a fixed
   `duration/2, repeat:1` (exactly one full sine.inOut oscillation per
   scene, regardless of length). A sine.inOut yoyo decelerates to near-zero
   velocity at its own turnaround point; on a 7.9s `ShEvidence` scene that
   turnaround sat mid-scene for 2.13s — a real, measured `motion_frozen`
   violation of the very 2.0s static-hold cap the fallback exists to
   prevent. Fixed by capping each half-cycle at 1.0s and adding more,
   shorter cycles for longer scenes instead of one big one.
   `compile_composition.py`.
2. **`ShMyth`'s intentional strike-through has no way to tell the layout
   checker it's intentional.** The 2px strike line crossing the muted claim
   text trips `text_occluded` — correctly, in the sense that it IS drawn
   over the text, but the design is legible and intentional (confirmed on
   the actual rendered frame). `data-layout-allow-occlusion` — the exact
   mechanism the checker's own `fixHint` names — is now emitted on the
   claim text (not the strike element; that placement was tried first and
   did not suppress the finding, confirmed by testing both).
   `compile_composition.py`.
3. **Two path-resolution bugs in `qa_render.py`, same root cause, found
   back to back.** `resolve_tooling_dir()` and the `mp4`/`frames_dir`/
   `beat_sheet_path` arguments in `main()` never resolved relative paths to
   absolute before use — harmless as long as every caller happened to pass
   absolute paths (T4's own testing always did), but `gate_h4_safe_area`
   shells out with `cwd=mp4.parent`, and a relative path that resolves one
   way against this process's own cwd resolves to something else entirely
   once the subprocess's cwd differs. A relative `$MMAV_TOOLING_DIR` (this
   run's own invocation) produced `can't open file
   '<mp4-dir>/catalog/tooling/check-safe-area.py'`; fixing only that still
   left `check-safe-area.py` unable to find its own `mp4` argument
   ("no render found under renders/*.mp4"), because that path had the same
   unresolved-relative problem. Both fixed by resolving to absolute at
   construction time. `qa_render.py`.

None of these three would have been found without actually compiling and
rendering real, sourced content end to end — the synthetic-fixture testing
in T3/T4 exercised the mechanism but not these specific edge cases (a
scene near the evidence-tier duration ceiling; a `ShMyth` scene checked
under `hyperframes check` rather than eyeballed; a relative-path
invocation of the harness).

## Skills and tools invoked

- vidIQ: `vidiq_balance` ×2 (0 credit each), `vidiq_keyword_research` ×1,
  `vidiq_outliers` ×1 (5 credit), `vidiq_generate_titles` ×1 (5 credit),
  `vidiq_score_title` ×1 (5 credit). 335 credits remaining (from 355).
- HeyGen: none (connector unavailable, per T1-FINDINGS).
- `frontend-design` / `design-critique` companions: available (per S0.0),
  not separately invoked as MCP calls this session — their gate purpose
  (taste/token discipline on the beat sheet; frame review at S7) was
  satisfied by this session's own direct component-contract review and
  frame-by-frame visual inspection.

## Rules fired (the ones that changed the outcome)

1. `S-1` branch 2 → format `short` (95.8% Shorts dominance).
2. `T-2` seed swap → `centella` (seed itself failed demand).
3. `S4b`'s connector-unavailable branch → slate-tone VO substitute, named.
4. `H-5` (recompile cap) → 2 recompile-and-rerender cycles used this run
   (the motion-float fix, then the occlusion-attribute placement fix),
   well under the 2-per-scene/4-per-run cap.
5. `H-3`'s visual-confirmation fallback → both detections judged non-faces
   on the actual frame.

Full list: no `00-decision-ledger.md` was maintained as a separate file
this run (a real gap against `SKILL.md`'s own outputs table — every rule
that fired is named in this report and in `01-story-brief.md`/
`02-packaging.md` instead; a future run should write the dedicated ledger
file).

## Artifacts

- `request.yaml`, `story.md`
- `00-environment.md`
- `01-story-brief.md` (K-1 table, script)
- `02-packaging.md` (S2/S3)
- `03-beat-sheet.json`
- `04-assets/audio.wav`, `04-assets/audio.mix-report.json`
- `06-render/9x16/` — `index.html`, `index.motion.json`, `check.json`,
  `renders/centella-asiatica-9x16.mp4` (45.5s, with audio), `qa-frames/`,
  `beat-sheet.qa.json`, `qa.json`, `h3-verification/` (3 evidence frames)
- `07-publish-envelope.md`
- `08-readout-schedule.md`
- `09-run-report.md` (this file)

## Skipped and why

- `S0` (baseline refresh): `baseline.yaml` already populated 2026-09-03,
  three days old — judged current enough for a single pilot run rather
  than spending a `vidiq_channel_stats`/`vidiq_channel_analytics` refresh
  pass on it.
- `S5a` (image plates): the design system has no imagery anywhere — a
  structural property of `videos/_system/`, not a per-run skip.
- Real VO synthesis, real HeyGen image/sound calls: connector unavailable
  in this non-interactive session (T1-FINDINGS F2–F4), unchanged since T1.
- `00-decision-ledger.md`: not written as its own file this run (see
  "Rules fired" above) — a real gap, named rather than silently omitted.

## `[NOT IN SKILL]` findings

1. **`S-4`'s own text still hard-blocks on `heygen.voice_id` unset**, with
   no provision for the connector-unavailable case `S4b` (T7) already
   handles. Surfaced by this run (see `00-environment.md`/
   `01-story-brief.md`), resolved by treating it as one finding rather
   than a second blocker, but `policy.md`'s `S-4` text itself needs a
   follow-up correction so the next run doesn't have to re-derive this
   judgment call. → `policy-change-proposals.md`.
2. **No dedicated `00-decision-ledger.md` was produced.** `SKILL.md`'s own
   outputs table names it as a per-run artifact; this run's rules-fired
   are recorded in this report and the S1/S2/S3 docs instead. A future
   run (or a T7.1 correction) should either write the dedicated file or
   correct the outputs table to say where rules are actually recorded.

## Next readout

Date: 48h and 7d from Kim's actual publish timestamp (see
`08-readout-schedule.md` — this run does not publish, so no real
timestamp exists yet to compute against).
