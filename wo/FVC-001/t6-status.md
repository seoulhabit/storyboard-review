# T6 — Environment probe and run report — DONE (spec + template); Accept check PASSED for real, 2026-09-03

Commit `cd14057` pushed to `github.com/seoulhabit/claude-skills`.

## What changed

- **New stage S0.0** in `pipeline-runbook.md`, positioned before S0, explicitly "runs first, every mode, no exceptions." Resolves OUT/CHANNEL, probes vidIQ/HyperFrames/Higgsfield/Gemini reachability (never blocks on any of them failing), writes `00-environment.md` from the new `assets/environment.template.md`.
- **New "Run report" section**, appended after "Re-running a stage" at the end of `pipeline-runbook.md`. Explicit about being written last in *every* mode, whether or not S9 itself ran — and explicit that its Stages table always lists all 11 rows (S0.0, S0–S9), marking whatever a mode didn't reach as `skipped (mode=<mode>)` rather than dropping the row. Section 8 restates the WO's own instruction: the run report's Summary is the run's entire final chat message, nothing after it.
- `assets/environment.template.md` and `assets/run-report.template.md` added, matching WO spec §4.4/§4.5 headings exactly.
- `SKILL.md`'s outputs table gains `00-environment.md` and `09-run-report.md`, with a note that both bookend every run regardless of mode.

## Accept check — actually run, 2026-09-03

WO's Accept: *"a `render` dry run produces both files; the report's Stages table shows S0–S4 and S8–S9 as `skipped (mode=render)`."*

Originally hand-traced only (below), because the HyperFrames CLI wasn't installed on this machine. Once `story-board-78` installed it (see `t2-status.md`), they ran the real check against a scratchpad copy — deliberately not the live `outputs/2026-09-01-how-to-repair-skin-barrier/` directory, to avoid overwriting an existing pre-T6 render. **PASS, verified by parsing the output, not eyeballing it:**

- `00-environment.md` (37 lines) and `09-run-report.md` (112 lines) both written under the scratchpad OUT.
- All 11 stage rows present in the Stages table — none omitted.
- Exact-string `skipped (mode=render)` on S0, S1, S2, S3, S4, S8, S9 (S8 correctly skipped since this run didn't ask for it).
- `ran` on S0.0, S5, S6, S7.
- S0.0 probed live tool reachability for real: vidIQ ok (2316 credits via the free `vidiq_balance` call), Higgsfield ok (2362.25 credits), HyperFrames ok 0.8.26, Gemini `no-key`. Total spend $0.00 of the $5.00 cap. `<CHANNEL>` resolved to `videos/_channel/` and found the migrated `baseline.yaml` already populated — confirming that migration (`becfaec`) now feeds a real run, not just sitting unused.
- S7's actual gate ran: `hyperframes check` on the copied `05-composition/` → exit 0, contrast 21/21 WCAG AA, layout clean across 9 samples.
- Original `outputs/2026-09-01-how-to-repair-skin-barrier/` confirmed untouched afterward: same 9 entries, `06-render/raw.mp4` mtime unchanged.

**Two honesty caveats the run itself recorded, worth keeping rather than smoothing over:**
1. S5/S6 are marked `ran (reused)` and S7 `ran (check gate only)` — the scratchpad copy's existing render artifacts weren't re-encoded (that would test ffmpeg, not T6's artifact contract); the gate that actually gates S7 did run for real and passed.
2. Both companion gates logged as `COMPANION-RESOLVED:<name> (skill-tool)` but explicitly **not executed** — S6/S7 reused artifacts rather than producing new markup or extracting new frames, so there was nothing for the gates to act on. Recorded as resolutions, not passes.

Unlike T2, T6's Accept criteria matched the real mode table exactly (`render` = S0.0 + S5–S7, +S8 if asked) — no mis-specification to report here.

Hand-traced table (kept for reference — matches the real run's shape exactly):

| Stage | Ran / skipped |
|---|---|
| S0.0 Environment | ran |
| S0 Baseline | skipped (mode=render) |
| S1 Story | skipped (mode=render) |
| S2 Topic gate | skipped (mode=render) |
| S3 Packaging | skipped (mode=render) |
| S4 Script + VO | skipped (mode=render) |
| S5 Beat sheet | ran |
| S6 Composition | ran |
| S7 Render QA | ran |
| S8 Publish envelope | ran (mode table: "+S8 if asked") — or `skipped (mode=render)` if not asked |
| S9 Readout schedule | skipped (mode=render) |

## Not done (correctly out of scope for T6)

- Actually wiring `providers.yaml`'s budget block into S0.0's "Budget in force" line — T7. S0.0's text already says so ("the 200-credit default until then").
- `provider_call.py` for the Spend section's real numbers — T7.
