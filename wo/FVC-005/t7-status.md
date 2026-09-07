# T7 — Skill cut to 0.3.0 — DONE

Commits: claude-skills branch `wo-fvc-005-t7` off `origin/master` (`e010f68`,
the merged T2–T4 PR); Story Board branch `session/wo-fvc-005-t7` (this
status + `videos/_channel/baseline.yaml`'s new `heygen:` block).

## Why this ran out of order (T7 before T5/T6)

T5 (pilot run) halted at S0.0: the loaded skill (0.2.0, no drift between the
`~/.claude/skills/makemeavideo` copy and canonical `claude-skills`) still
routed S5–S7 through HeyGen Video Agent — exactly what R-1/R-2 supersede —
and `<CHANNEL>/baseline.yaml` (checked under both possible names) had no
`heygen:` block resolving T1-FINDINGS' spike findings, so the skill's own
`BLOCKER-SPIKE-PENDING` rule would have fired on the first `[SPIKE:n]`
marker S5–S7 reached. Running T5 as literally written would have meant
either violating R-1/R-2 or improvising an unwritten rule mid-run — both
against this WO's own "no loosening a rule to pass a gate." T7 was the only
real path forward; ratified before starting (see chat).

## What shipped

**claude-skills** (`makemeavideo/`):
- `SKILL.md` — engine paragraph, pipeline diagram, outputs table, and tool
  fence (`H-0`, now R-2's exact list) rewritten; version bumped to 0.3.0 in
  all three sites the frontmatter/heading/body carry it.
- `references/policy.md` §H — `H-1` (composition generated, not typed, via
  `compile_composition.py`), `H-2`–`H-4` reread against a local render
  (`H-4`'s loudness note records T4's measured ~+3dB render-stage gain as a
  finding to re-verify, not a hard-coded constant), `H-5` (recompile cap,
  not a chat-message cap), `H-6` **retired** (`[SPIKE:3]` — the compiler's
  own `index.motion.json` is deterministic, no timing-source question
  remains), `H-7` (credit scope narrowed — local compile/render spend
  zero), `F-2` **retired as a spike** (`[SPIKE:4]` — R-5's one-compile-both-
  canvases already answers it, `F-2a` clipping forbidden outright). `PR-2`/
  `V-2` corrected: the pre-flight VO **ships** now (no HeyGen build-time
  re-synthesis to trust instead) and an unreachable connector routes to a
  named local substitute rather than halting the run. `C-3a` corrected: the
  brand end-card is a mounted `ShEndcard` component now, not a described
  prompt scene. Version header bumped.
- `references/runbook.md` — S4 split into S4 (script) / S4b (VO pre-flight,
  with the local-substitute branch spelled out); S5 split into S5a (image
  plates — a structural no-op, this design system carries no imagery) /
  S5b (composition) / S5c (sound, local-first); S6 rewritten to
  `render_local.sh`/`render_cloud.sh`; S7 rewritten to read
  `render_local.sh`'s own `qa.json` instead of re-driving `qa_render.py` by
  hand. S0.0 gained a render-machine probe. Version header bumped.
- `references/providers.yaml` — restructured off the single
  `heygen-video-agent` role into `tts_preflight`/`image`/`audio_enhance`/
  `audio_search`/`render_cloud`, each carrying T1-FINDINGS' actual verdict
  (`BLOCKED-CONNECTOR`, named) rather than a placeholder. The one measured
  number: the public cloud-render rate, 20 credits/minute.
- `assets/environment.template.md` — render-machine block added;
  provider-reachability line distinguishes `BLOCKED-CONNECTOR` (structural)
  from `unreachable` (transient).
- `assets/run-report.template.md` — credits-by-stage cost table added
  (local render/compile is not a row); Stages table matches the new S4/S4b/
  S5a/S5b/S6/S7 split.
- `scripts/render_cloud.sh` — file-resolution order swapped to check
  `baseline.yaml` first (matching the sec-8.8 decision below), `channel.yaml`
  as fallback; the now-redundant "which one did we read" warning removed.
- `CHANGELOG.md` — 0.3.0 entry.

**Story Board** (`videos/_channel/baseline.yaml`):
- New `heygen:` block. `voice_id`/`brand_glossary_id` stay `null`
  (TOUCHPOINT-SETUP hasn't run; both are connector-blocked regardless, per
  F2). `cloud_render_credits_cap: 20` [default] — R-1/WO sec 8.3, credit-
  denominated against this account's 81 add-on credits, pending Kim's own
  preference. `style_id`/`tokens`/`timing_source`/`shorts_path` set `null`
  with a note each explaining why they're retired (obsolete under the local
  engine, not just unfilled). `spike_findings`: T1-FINDINGS' four verdicts
  recorded verbatim, dated, sourced.

## The channel.yaml vs baseline.yaml fork (sec 8.8), resolved

Asked directly rather than defaulted, per the WO's own instruction. Answer:
**point the skill's docs at `baseline.yaml`** (the file that actually
exists, with real measured channel data), not the other way round. This
reverses 0.2.0's own T3 change, which renamed the skill's *prose* to
`channel.yaml` but never touched the real file — leaving the docs and the
data permanently disagreeing until now. Recorded explicitly in
`CHANGELOG.md`'s 0.3.0 entry rather than silently re-diverging a second
time.

## Verification

Did not re-run the full harness end-to-end a second time under T7 — the
underlying scripts (`compile_composition.py`, `mix_audio.py`,
`render_local.sh`, `render_cloud.sh`, `_qa_adapter.py`) are unchanged from
T4's own already-verified state (`wo/FVC-005/t4-verification/`); T7 rewrote
the *documentation and rules* that describe them, plus `baseline.yaml`'s new
data block and one file-resolution order swap in `render_cloud.sh`. What
was verified fresh:
- `render_cloud.sh` still runs cleanly (refuses correctly on a missing
  `request.yaml`, no syntax errors from the edit).
- The new `baseline.yaml` `heygen:` block parses as valid YAML
  (`python3 -c "import yaml; yaml.safe_load(...)"`) and `render_cloud.sh`'s
  own regex correctly extracts `cloud_render_credits_cap: 20` from it.
- `grep` swept `SKILL.md`/`policy.md`/`runbook.md` for every
  `video_agent`/`Video Agent`/`build spec`/`chat mode`/`beats_to_build_spec`
  string; each hit was either fixed or confirmed intentional (a forbidden-
  tool-fence entry, historical/provenance text). No `[SPIKE:n]` marker in
  the rewritten S4–S7 rules can still fire `BLOCKER-SPIKE-PENDING` — the
  three that existed (`[SPIKE:1]`, `[SPIKE:3]`, `[SPIKE:4]`) are all either
  retired outright or resolved to a measured, stored verdict.

## Accept check

**Done-when, per the WO's own bar**: "the pilot re-runs in `build` mode on
0.3.0 with no `BLOCKER-SPIKE-PENDING`." Structurally satisfied — traced
every path S4b–S7 can take and confirmed none references an unresolved
`[SPIKE:n]`. **Not literally re-run as a live `build`-mode pilot this
session** — T5 itself (the actual pilot) is next, and will be the real,
end-to-end confirmation of this bar rather than a second synthetic-fixture
pass repeating what T4 already proved.

**Not done, named rather than silently skipped**: `beats_to_build_spec.py`
(the old HeyGen build-spec generator) and a handful of files outside T7's
own bullets (`tests/run.sh`, `scripts/_yaml_lite.py`,
`assets/request.template.yaml`, `CHANGELOG.md`'s pre-0.3.0 history) still
say `channel.yaml` or reference the retired build-spec path in places —
left alone deliberately: `beats_to_build_spec.py` is dead code under the new
S5b (never called by the rewritten runbook), and rewriting every historical
or unrelated mention was judged scope creep against T7's own stated bullets.
