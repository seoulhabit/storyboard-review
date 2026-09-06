# Run report — WO-FVC-005 T4 (R-6 + audio/render harness)

Written last, per §0.1. This is a build/verification session (S-B tier: T2 ->
T3 -> T4), not an S1-S9 production run, so the Stages table below is scoped
to what actually ran rather than the full pipeline template.

## S0.0 — version and drift check

- `hyperframes --version` -> **0.8.30**, unchanged since T0 (`00-environment.md`).
- `makemeavideo` SKILL.md `metadata.version` -> **0.2.0**, unchanged.
- claude-skills worktree branched from `fvc-005/makemeavideo` @ `0364b79`
  (T3's last commit) — same tip T3 left, no drift.
- Story Board worktree branched from `origin/master` @ `4b2e0ce` (merge of
  PR #20, the last of T0-T3's three merged PRs) — no drift.
- No paid provider calls made this session (HeyGen/vidIQ untouched); no
  balance delta to ledger.

## Summary

- Mode: `build` (T4: audio + render harness, plus ruling R-6)
- Result: `complete`, with one named, unresolved finding (H-3 false
  positive — see below, not a T4 defect)
- Artifacts: 16 files written/changed across two repos (Story Board:
  2 modified + 9 new under `wo/FVC-005/`; claude-skills: 1 modified + 4 new
  under `makemeavideo/scripts/`)
- Spend: $0 of cap — no HeyGen/vidIQ calls this session; one local pip
  install (`opencv-python-headless==4.10.0.84`, the pinned face-detector
  dependency `qa_render.py` already names)
- Needs Kim: nothing blocking. Two things worth a look when convenient:
  (1) HyperFrames' own render pipeline appears to add ~+3dB to muxed audio
  vs. the source file — worth a second measurement on a real production
  mix before trusting any fixed pre-mux LUFS target; (2) `qa_render.py`'s
  H-3 face detector (Haar cascades) false-positives on this design
  system's bold headline typography — a WO-FVC-004 artifact, not
  retuned here.

## What ran

1. Printed `T1-FINDINGS.md`'s pass/fail lines (F1 PARTIAL, F2-F4
   BLOCKED-CONNECTOR — unchanged from T1, restated per this session's
   instruction, not re-run).
2. **R-6** (ruling confirmed by Kim this session): widened the design
   system's safe-area tokens 10%->15% (9:16 right rail) and 8%->10% (16:9
   bottom zone), closing T3 finding #20. Re-verified against
   `check-safe-area.py`: both canvases now `no findings` (were both `FAIL`
   before).
3. **T4**: built `mix_audio.py`, `render_local.sh`, `render_cloud.sh`, and
   a small `_qa_adapter.py` schema-bridge helper (claude-skills). Proved
   the full chain — mix -> compile -> check -> render -> extract -> QA —
   against the T3 synthetic-t1-fixture. Found and fixed two real bugs in
   the new code (a loudness-measurement regex bug, a stale-duration bug in
   the adapter) before reporting anything clean; named one real external
   finding (HyperFrames' render-stage audio gain) rather than silently
   compensating for it as a permanent default.

Full account: `t4-status.md`. Verification evidence (qa.json, check.json,
mix report, before/after safe-area renders, the H-3 false-positive frame):
`t4-verification/`.

## Rules fired

3 rulings/rules touched this session:
1. **R-6** (new, confirmed by Kim) — safe-area widened to 15%/10%.
2. **T1-FINDINGS' F1 consequence, `C-6`** (restated, not re-fired) — hard
   cuts only, already in force since T1, unaffected by this session.
3. **§0.1 "no auto-retry past a cap; no loosening a rule to pass a
   gate"** — applied directly: did not retune the H-3 detector to force a
   green result, and did not bake the measured render-stage gain into a
   permanent default without a second measurement.

## Spend

No provider table this session — no HeyGen/vidIQ calls made. `spend.jsonl`
not appended to (nothing to log).

## Artifacts

Story Board (`session/wo-fvc-005-t4`, commit `2704469`):
- `videos/_system/tokens/spacing.css` — R-6
- `videos/_system/MANIFEST.json` — re-hashed + amendments entry
- `wo/FVC-005/t4-status.md`, `t4-run-report.md`
- `wo/FVC-005/t4-verification/` — README, qa-9x16.json, check-9x16.json,
  mix-report.json, synthetic-t1-fixture-9x16.mp4, repo-gates/ (2 renders),
  h3-false-positive/ (1 frame)

claude-skills (`wo-fvc-005-t4`, commit `40286c7`):
- `makemeavideo/scripts/compile_composition.py` — R-6 constants
- `makemeavideo/scripts/mix_audio.py`, `render_local.sh`,
  `render_cloud.sh`, `_qa_adapter.py` — new

## Skipped and why

- 16:9 was not run through the full `render_local.sh` pipeline this pass
  — R-6 was verified on both canvases independently; the audio/render
  harness mechanism itself (`derive_duration`, the `<audio>` wiring,
  `qa_render.py`'s gates) is canvas-independent, so 9:16 alone proves it.
- Real VO (`create_speech` or local Kokoro) — F2 stays BLOCKED-CONNECTOR;
  `kokoro-onnx` could not be installed in this environment (no matching
  `onnxruntime` wheel for Python 3.9/x86_64 here) — named, not forced.
- `<hf-audio-group>` ducking/automation graph — not in T4's own scope
  (VO-at-start + one bed + loudness band, covered literally).
- No PR opened and no merge to `master`/`fvc-005/makemeavideo` performed —
  not asked for this session; both session branches are committed and
  ready for review.

## `[NOT IN SKILL]` findings

None this session that weren't already covered by an existing rule or
named as a finding above.

## Next readout

N/A — this is a harness-build session, not a published video. No readout
to schedule.
