# WO-FVC-001 — faceless-video-craft v2.1
**Single source of truth · reliable invocation · companions as gates · provider registry with cost tracking · run visibility**
Date: 2026-09-02 · Lane: Chat → Code · Origin: Chat "Skill fix plan" (Sep 2) + Chat "Faceless educational video skill optimization" (Sep 1) + REPORT-2026-09-01.md
Status: **DRAFT** until Kim writes `approved` on the line below.
▸ Kim's approval: ___
---
## KICKOFF (paste into Claude Code, opened in the video repo, model **Sonnet / medium**)
> Read `docs/wo/WO-FVC-001.md` in this repo and work from it — do not work from memory. Start with §0 and stop at Gate 0.
Save this file there first. Everything the run produces goes under `wo/FVC-001/` in the repo until T10.
---
## §0 — Live inventory first (re-query, never assume)
Before any edit, write `wo/FVC-001/00-inventory.md` from live commands, not recollection:
1. `git rev-parse --show-toplevel`, current branch, `git status --short`.
2. Every copy of the skill that exists on this machine. For each: path, SKILL.md line count, `sha256sum SKILL.md`, references present (list), mtime.
   - `.claude/skills/faceless-video-craft*` (this repo)
   - `~/.claude/skills/faceless-video-craft*`
   - `~/.claude/skills/synced/`
   - `~/.claude/plugins/cache/` entries matching `faceless`
   - Any `.claude/commands/*produce*` or `*video*`
3. What `/faceless-video-craft` resolves to right now: run `/skills` (or `claude -p "What skills are available?"`) and record source labels.
4. Rules present in the repo copy but absent from v2: list by rule ID. K-1..K-5 are expected; anything else is a finding.
5. Tooling: `claude --version` · `hyperframes --version` (and the installed npm package version) · `ffmpeg -version | head -1` · `ffprobe -version | head -1` · `python3 --version` · `echo "GEMINI_API_KEY: ${GEMINI_API_KEY:+set}${GEMINI_API_KEY:-unset}"` · vidIQ MCP reachable (one cheap call) · Higgsfield MCP reachable · HyperFrames MCP reachable.
6. Paths of `REPORT.md`, `REPORT-2026-09-01.md`, `videos/centella-tiger-grass/`.
7. The name of the current voiceover path used at S4 (tool + voice id).
**GATE 0 — stop here.** Post the inventory in chat and wait. Kim answers the three slots below on this page, then writes `go`.
▸ Skills repo location (default: new private GitHub repo `claude-skills`, path `faceless-video-craft/` inside it): ___
▸ Higgsfield USD per credit (from current plan), for `providers.yaml`: ___
▸ Current VO provider to register as `current-vo` in `providers.yaml`: ___
---
## §1 — Standing rulings (verbatim, enforce throughout)
1. **Canonical = v2 structure.** Merge in, never drop: K-1..K-5 claim-sourcing (repo copy) · the six v1 rules v2 dropped (type floors · 4.5:1 contrast measured on pixels · box-sizing · catalog reuse loop · static-hold pixel diff · AAC true-peak headroom) · the engine-contract fixes from REPORT-2026-09-01.
2. **K-2b is not loosened.** Zero sourced claims still blocks. Unblocking the centella video is a separate fetch-and-read pass that wires R01 EN-01 (PMID 36918311), EN-06 PRISMA, CIR 2015 Final, and the MFS `/ingredient/centella` passport into the K-1 table. Not this WO.
3. **Gemini is available for ALL roles** — research/claims, image plates, voiceover — as a provider option chosen by rule, **with cost tracking on every call.**
4. **Channel data lives in the project repo, never in the skill.** Policy changes need repeated evidence or Kim's approval; the learning loop *proposes*, it does not rewrite `decision-policy.md`.
5. **No creative-preference questions to the operator.** Legitimate stops only: authentication, channel ambiguity, paid spend above cap, a genuine blocker with a name.
6. **Kim is the only publish gate.** Metadata writes to YouTube need explicit consent every time.
7. **Surface-aware paths.** `/mnt/...` only when the directory exists at run time.
8. **Scope never widens.** Anything discovered but not in §2 goes to §5, not into the diff.
9. **Read-back verification, never mutation echo.** Every "done" in the handback is a command output, not a sentence.
10. **Tier discipline.** T2 (and the policy text of T7 if done in the same stretch) on Opus/High; everything else Sonnet/medium. Announce each switch in chat; switch back down after T2.
---
## §2 — Tasks
Each task: *Do* → *Produces* → *Accept* (a command whose output goes in the handback). Do them in order. A failed Accept stops the task; no auto-retry past one fix attempt — report instead.
### T1 · Repo and version stamp — Sonnet/medium
*Do*
- Create the skills repo per Gate 0 answer. Layout: `faceless-video-craft/` (the skill) · `wrappers/` (thin Code-only command skills) · `archive/` · `dist/` (gitignored) · `scripts/release.sh`.
- Import v2 as-is into `faceless-video-craft/` from whichever copy the inventory identifies as v2 (SKILL.md ≈190 lines + 6 references + scripts + assets). Commit `import v2 baseline`.
- Copy the repo v1 (`.claude/skills/faceless-video-craft/`, ~2,172 lines) to `archive/v1-repo-2026-09-01/`. Commit `archive v1 repo copy for merge`.
- Add `CHANGELOG.md`. Frontmatter gains `metadata: {version: "2.1.0"}`. First body line under the title: `Version 2.1.0 — copy this string verbatim into 00-environment.md and 09-run-report.md.`
- `scripts/release.sh`: asserts frontmatter keys ⊆ {name, description, license, compatibility, metadata, allowed-tools}; runs `claude plugin validate faceless-video-craft` (Claude Code ≥ 2.1.233); zips to `dist/faceless-video-craft-<version>.zip`.
*Accept* — `git log --oneline | head -3` · `scripts/release.sh && ls -la dist/` · validator exit code.
### T2 · Merge and engine fixes — **Opus/High (the one tier switch)**
*Do*
- Write `wo/FVC-001/merge-matrix.md`: one row per rule ID across {v1-repo, v2, K-rules} with a verdict `keep | merge | superseded-by <id> | dropped: <reason>`. Empty cells are not allowed. The six §1.1 rules and K-1..K-5 must be `keep` or `merge`.
- Apply the matrix to `references/decision-policy.md` and the other references.
- Engine contract, verified against the *installed* HyperFrames, not the report text: `#root` with `data-composition-id` / `data-start` / `data-duration`; GSAP paused timelines registered on `window.__timelines`; `assets/composition-skeleton.html` must render with motion.
- Lint parity: run `scripts/lint_composition.py` and `hyperframes check` on three fixtures (clean · banned rAF · lazy image) and reconcile, **recording each delta with its cause rather than eliminating it**. Corrected 2026-09-03: the original wording, "reconcile until findings agree", is not achievable and should not be. `check` has no image-loading rule — verified across all 248 of its lint rule ids on 0.8.26, and its shipped docs carry no image guidance — so it passes `fail_lazy_image` at exit 0 while `lint_composition.py` correctly reports 2 errors. `lint_composition.py` is a deliberate **superset**; deleting its rule to buy agreement would drop a real check. See `hyperframes-engine.md` §10 Provenance.
- Policy defects: S-1 (long-form default on a Shorts-majority channel) · S-2 (top-quartile below the 30 s clamp, replay-inflated) · T-3 (10×subs ceiling) rewritten as rules that read `channel-baseline`, tagged `[default]`.
*Accept* — `merge-matrix.md` grep for empty verdicts returns 0 · `hyperframes check <dir>` exit 0 on the skeleton **scaffolded as a project** · frame diff on the skeleton render shows Δ>0 · lint-vs-check **delta** table for the three fixtures, every delta explained.
*Accept text corrected 2026-09-03, after running it.* Three of the four criteria were unrunnable as written. (1) `check` takes `[DIR] Project directory`; a file path errors `Not a directory`. (2) The bare skeleton cannot pass regardless — it references three `compositions/frames/*.html` sub-compositions that only exist once S6 authors them, so the fixture must be scaffolded with scenes first. (3) `t=0 vs t=1s` samples a window where the skeleton's **root** timeline does nothing: its transitions open at 2.500s and 5.400s, so that pair measures the sub-compositions, not the skeleton's own choreography — diff across a real transition instead. (4) "agreement" is replaced by "delta, explained", per the *Do* above.
Switch back to Sonnet/medium after T2.
### T3 · Invocation: description, mode router, wrappers, paths — Sonnet/medium
*Do*
- Replace the description with §4.1. Hard cap 500 characters. No "trigger even for plain frontend work".
- Mode router at the top of the SKILL.md body (§4.2): `full | render | package | audit | readout`; each mode names the stages it runs and the references it loads. Nothing outside the mode loads.
- Wrappers in `wrappers/<name>/SKILL.md` — `produce`, `video-render`, `video-package`, `video-audit`, `video-readout` — per §4.6. Claude Code only; never uploaded to claude.ai (`argument-hint` is not a spec field).
- Surface-aware paths: `OUT = /mnt/user-data/outputs/<slug>/` if that directory exists, else `<repo>/videos/<slug>/`. `CHANNEL = <repo>/videos/_channel/`. Replace every hardcoded `/mnt` reference.
- Move `references/channel-baseline.md` content to `assets/channel-baseline.template.yaml`; S0 writes `<CHANNEL>/baseline.yaml`; the learning loop writes `<CHANNEL>/policy-change-proposals.md`.
*Accept* — `wc -c` of the description ≤ 500 · `grep -rn "/mnt/" faceless-video-craft/` shows only the guarded pattern · `ls wrappers/` lists five.
### T4 · Companion skills as gates — Sonnet/medium
*Do*
- Replace "Also read `/mnt/skills/public/frontend-design/SKILL.md`" with the resolver: (1) invoke skill `frontend-design` via the Skill tool (plugin `frontend-design@claude-plugins-official`) → (2) read `/mnt/skills/public/frontend-design/SKILL.md` if it exists → (3) else write `COMPANION-MISSING:frontend-design` to the ledger and continue. **Mandatory** at S3 (thumbnail/packaging visuals) and S6 entry.
- Same resolver for `design-critique` (invoked directly via the Skill tool — confirmed 2026-09-03 that it is not sourced from `claude-plugins-official` or any other configured marketplace, and needs no install; see T8's note), **mandatory** at the S7 gate on extracted frames — it was "optional"; it is not any more.
- Every companion invocation is a ledger line and a run-report row.
*Accept* — a dry run of S6 entry in Code shows the Skill tool call in the transcript; `grep -n "COMPANION" 00-decision-ledger.md` on a run with the plugin disabled shows the MISSING line.
### T5 · Validators and lint hardening — Sonnet/medium
*Do*
- `scripts/validate_beat_sheet.py`: six sections in order · non-negative, continuous timings · no overlap or gap · last scene ends at measured VO duration ±50 ms · beat offsets inside their scene · canvas matches format · end scene long-form only · chapters only where the policy allows. Exit 1 with a list.
- `scripts/lint_composition.py`: single- and double-quoted attributes · every image individually · missing `decoding="sync"` and remote render URLs are errors · every image wrapper has a fallback · self-running GSAP / anime.js / CSS animation / Web Animations detected · comments and strings ignored.
- `scripts/extract_frames.sh`: sanitise scene IDs · require ffprobe · real variance/entropy check (ffmpeg `signalstats` or ImageMagick) or delete the "tofu" claim.
- `tests/fixtures/` + `tests/run.sh`, with at least one failing fixture per validator.
*Accept* — `tests/run.sh` exit 0 · each validator run on its failing fixture exits 1 with the finding named.
### T6 · Environment probe and run report — Sonnet/medium
*Do*
- New stage S0.0 writes `00-environment.md` (§4.4) in every mode, including `audit` and `readout`.
- New final artifact `09-run-report.md` (§4.5), mandatory in every mode. The last chat message of a run is the report's **Summary** block verbatim — nothing else after it.
- Runbook and SKILL.md outputs table updated; `08-readout-schedule.md` stays.
*Accept* — a `render` dry run produces both files; the report's Stages table shows S0–S4 and S8–S9 as `skipped (mode=render)`.
### T7 · Provider registry, cost wrapper, rules R-1 / A-1 / V-1 / B-1 — Sonnet/medium (policy text on Opus if still in the T2 stretch)
*Do*
- `references/providers.yaml` per §4.3, dated. Gate 0 answers fill the two `null` prices.
- `scripts/provider_call.py` — subcommands `gemini text|image|tts` (uses `GEMINI_API_KEY` from the environment only; reads `usageMetadata` for tokens) and `log` (for spend that happens MCP-side: vidIQ credits, Higgsfield credits, HyperFrames render minutes). Prices from the yaml. Appends one §4.3 line to `<OUT>/cost-log.jsonl`. `--dry-run` prices without calling. `.gitignore` covers `.env*` and `*.key`.
- `decision-policy.md` gains: **R-1** research provider — Gemini grounded search fires only when K-1 still lacks a source after the project source list is exhausted · **A-1** extended — diagram/illustration plates → Gemini image, photographic → Higgsfield, decided per plate by the asset manifest · **V-1** voice — Gemini TTS default, `current-vo` fallback, flagged `listening-test pending` · **B-1** budget — per-run cap $5 plus credit caps, ledger warning at 80 %, halt with blocker `BUDGET-CAP` at 100 %; replaces the vidIQ-only 200-credit rule. All four carry both providers and a `[default]` tag.
- Run report Spend table (provider × stage, total vs cap). Run total appended to `<CHANNEL>/spend.jsonl` so the 7-day readout can compute cost per 1k views.
- Environment probe records `gemini: ok | no-key | no-network`; R-1/A-1/V-1 fall back automatically on anything but `ok`.
*Accept* — `provider_call.py gemini text --dry-run --in 1000 --out 1000` prints the price the yaml implies · with the key set: one real text call, one 1K image, one 5-second TTS → three lines in `cost-log.jsonl` with `est_usd` · a run report showing the Spend table · a run with `GEMINI_API_KEY` unset shows the fallback provider in the ledger, not an error.
### T8 · Distribution — machine A, machine B, claude.ai (Kim does the parts marked ☐)
*Do*
- Each machine: `git clone` the skills repo → `ln -s <checkout>/faceless-video-craft ~/.claude/skills/faceless-video-craft` → same for each `wrappers/<name>` → ☐ `GEMINI_API_KEY` in the shell profile → ☐ `/plugin install frontend-design@claude-plugins-official`, `skill-creator@claude-plugins-official` (`design@claude-plugins-official` dropped 2026-09-03 — no such plugin exists in that marketplace, checked directly against its source repo; `design-critique` needs no install anywhere, it's already active in-session via a different, non-marketplace mechanism).
- ☐ claude.ai: Customize → Skills → delete the old `faceless-video-craft` entry → upload `dist/faceless-video-craft-2.1.0.zip`. Cowork and cloud sessions load it from there; local Code loads the symlink. No `CLAUDE_CODE_SYNC_SKILLS` run is needed — the synced copy would be skipped in favour of the personal one anyway, which is the intended single winner.
*Accept* — on each machine: `/skills` shows exactly one faceless entry (source: personal) · `/produce` appears in the `/` menu · `claude plugin validate ~/.claude/skills` passes · `readlink ~/.claude/skills/faceless-video-craft`.
### T9 · Evals, blind A/B, description tuning — Sonnet/medium
*Do*
- With the skill-creator plugin: `evals/evals.json` with the seven cases in §4.7. Run with-skill and baseline. Blind A/B v2.1 vs `archive/v1-repo-2026-09-01/` on cases 1 and 3.
- Description optimisation: ≥ 10 should-trigger and ≥ 10 should-not-trigger prompts; "make my landing page hero animate" must be a should-not.
- Case 7 (centella regression) uses `videos/centella-tiger-grass/` as-is. If K-2b still blocks, the assertion is that it **blocks with the named reason** — that is correct behaviour under §1.2.
*Accept* — `benchmark.json` pass rate ≥ v1 on all seven · trigger precision ≥ 0.9 on the should-not set · results in `faceless-video-craft-workspace/` · `evals/evals.json` committed.
### T10 · Cutover — only after T9 passes and Kim writes `cut over` on the handback
*Do* — delete `.claude/skills/faceless-video-craft*` from the video repo (commit `remove shadowing skill copies; canonical is claude-skills`) · tag `v2.1.0` in the skills repo · update `CHANGELOG.md`.
*Accept* — `git tag` · `ls .claude/skills/` in the video repo · `/skills` on machine A after a fresh session.
---
## §3 — Target file map (v2.1)
```
claude-skills/
├── faceless-video-craft/
│   ├── SKILL.md                      (frontmatter: 6 spec fields only; body ≤ 500 lines)
│   ├── CHANGELOG.md
│   ├── references/
│   │   ├── decision-policy.md        (rules incl. K-1..K-5, R-1, A-1, V-1, B-1, restored v1 rules)
│   │   ├── pipeline-runbook.md       (S0.0 probe … S9 report)
│   │   ├── hyperframes-engine.md     (verified contract)
│   │   ├── youtube-delivery.md
│   │   ├── learning-loop.md          (proposes; never rewrites policy)
│   │   └── providers.yaml            (dated rates)
│   ├── scripts/
│   │   ├── provider_call.py · lint_composition.py · validate_beat_sheet.py · extract_frames.sh
│   ├── assets/
│   │   ├── composition-skeleton.html · beat-sheet.schema.json
│   │   ├── decision-ledger.template.md · run-report.template.md · environment.template.md
│   │   └── channel-baseline.template.yaml
│   ├── tests/ (fixtures + run.sh)
│   └── evals/evals.json
├── wrappers/ (produce, video-render, video-package, video-audit, video-readout)
├── archive/v1-repo-2026-09-01/
├── scripts/release.sh
└── dist/ (gitignored)
```
Per-project (video repo): `videos/<slug>/00…09 artifacts + cost-log.jsonl` · `videos/_channel/baseline.yaml · spend.jsonl · policy-change-proposals.md`.
---
## §4 — Specs
### 4.1 Description (≤ 500 chars, front-loaded)
> Faceless educational YouTube video as code: story → beat sheet → HTML/CSS/JS composition rendered through HyperFrames seek(t) → MP4 plus publish envelope, every fork decided by written rule and vidIQ data. Modes: full production, render-only (animate supplied assets or a script), packaging (title, thumbnail, description), performance audit, 48h/7d readout. Use on HyperFrames, seek(t), beat sheet, Shorts or long-form packaging, vidIQ decisions, /produce. Not for ordinary websites, UI animation that will not become a video, or still-image edits.
### 4.2 Mode router (top of SKILL.md body)
| Mode | Runs | Loads |
|---|---|---|
| `full` | S0.0–S9 | all references |
| `render` | S0.0, S5–S7 (+S8 if asked) | hyperframes-engine, youtube-delivery, decision-policy §A/§S |
| `package` | S0.0, S0, S2–S3, S8 | decision-policy §T/§P, youtube-delivery, providers |
| `audit` | S0.0, S0, S9-diagnose | learning-loop, channel baseline |
| `readout` | S0.0, S9 | learning-loop |
Mode comes from the wrapper or from the request; default `full` only when a story is supplied and no narrower intent is stated.
### 4.3 `providers.yaml` skeleton and cost-log line
```yaml
as_of: 2026-09-02
source: https://ai.google.dev/gemini-api/docs/pricing
roles:
  research:
    - {id: gemini-text, provider: gemini, model: gemini-3.8-flash, unit: tokens,
       usd_per_1m_in: 0.75, usd_per_1m_out: 3.75,            # through 2026-12-31; 1.50 / 7.50 from 2027-01-01
       grounding: {free_per_month: 5000, usd_per_1k_after: 14}}
    - {id: claude-native, provider: claude, unit: tokens, usd_per_1m_in: 0, usd_per_1m_out: 0}   # running model; logged, not priced
  image:
    - {id: gemini-image, provider: gemini, model: gemini-3.1-flash-image, unit: image,
       usd_per_image: {"0.5k": 0.045, "1k": 0.067, "2k": 0.101, "4k": 0.151}}
    - {id: gemini-image-lite, provider: gemini, model: gemini-3.1-flash-lite-image, unit: image, usd_per_image: {"1k": 0.0336}}
    - {id: higgsfield, provider: higgsfield, unit: credits, usd_per_credit: null}   # Gate 0
  tts:
    - {id: gemini-tts, provider: gemini, model: gemini-3.1-flash-tts-preview, unit: audio_tokens,
       tokens_per_second: 25, usd_per_1m_out: 20.00, usd_per_1m_in: 1.00}
    - {id: current-vo, provider: null, unit: null}                                   # Gate 0
  render:
    - {id: hyperframes, provider: hyperframes, unit: minutes_rendered, usd_per_unit: null}
  data:
    - {id: vidiq, provider: vidiq, unit: credits, usd_per_credit: null}
budget:
  per_run_usd: 5.00
  warn_at: 0.8
  vidiq_credits: 200
```
`cost-log.jsonl`, one line per paid call:
```json
{"ts":"…","run":"<slug>","stage":"S4","role":"tts","rule":"V-1","provider":"gemini","model":"gemini-3.1-flash-tts-preview","units_in":812,"units_out":9000,"unit":"audio_tokens","est_usd":0.1808,"artifact":"04-assets/vo.wav","note":""}
```
### 4.4 `00-environment.md` headings
Skill version · Surface (claude.ai | cowork | code) · Host · Paths (OUT, CHANNEL) · Companions resolved (name → skill-tool | file | MISSING) · Providers reachable (vidIQ · HyperFrames + version · Higgsfield · Gemini: ok/no-key/no-network) · Project skill in play · Budget in force · Mode.
### 4.5 `09-run-report.md` template
1. **Summary** — five lines: mode · result (complete | halted:<blocker>) · artifact count · total spend vs cap · what needs Kim (publish click or nothing).
2. **Stages** — table: stage · ran/skipped (reason) · gate result (pass | auto-fixed ×n | halt) · tool calls · minutes.
3. **Skills and tools invoked** — companion skills (how resolved) and MCPs, per stage.
4. **Rules fired** — count, the five that changed the outcome, link to `00-decision-ledger.md`.
5. **Spend** — provider × stage, total, % of cap; the line appended to `spend.jsonl`.
6. **Artifacts** — path list with sizes.
7. **Skipped and why.**
8. **`[NOT IN SKILL]` findings** → written to `policy-change-proposals.md`, never to policy.
9. **Next readout** — date and what to compare.
### 4.6 Wrapper example (`wrappers/produce/SKILL.md`)
```yaml
---
name: produce
description: Full faceless-video production run — story in, MP4 plus publish envelope out, via the faceless-video-craft skill.
argument-hint: [topic, script path, or URL] [--short|--long]
disable-model-invocation: true
---
Invoke the `faceless-video-craft` skill in **full** mode with this input: $ARGUMENTS
Do not run stages outside the mode table. End with the 09-run-report Summary block.
```
Same shape for `video-render` (mode render), `video-package` (package), `video-audit` (audit, argument = video id), `video-readout` (readout).
### 4.7 Eval cases (`evals/evals.json`)
1. Six-minute explainer from a topic — full pipeline, all nine artifacts, spend under cap.
2. Animate one supplied image into a 20 s clip — **no** vidIQ calls in the ledger.
3. Diagnose an underperforming published video — **no** render started.
4. Non-English Short — voice and keyword market follow the requested language.
5. vidIQ unreachable — one named blocker, no invented numbers.
6. "Make my landing page hero animate" — skill must not trigger.
7. Centella regression (`videos/centella-tiger-grass/`) — `hyperframes check` 0/0, safe-area pass, K-4 pass, true-peak ≤ −2 dBFS; K-2b outcome asserted as it stands.
---
## §5 — Does NOT close (carried, not in scope)
- Whether to trim `seoulhabit-video-3d` (open since Aug 29).
- Wiring R01 / CIR / MFS sources into the centella K-1 table (§1.2) — separate pass.
- Provider reordering by cost-per-view — needs data from ≥ 3 published runs; the learning loop only proposes.
- Veo / Omni video generation — excluded by design; composition stays code-rendered.
- Listening test Gemini TTS vs `current-vo` — Kim's ears, after T7.
- Multi-channel baselines — one channel only in this WO.
---
## §6 — Handback format (write `wo/FVC-001/HANDBACK.md`, then post it)
1. **Attestation table** — one row per Accept check: task · command · output excerpt. Read-back, never echo.
2. **Refusals on record** — anything declined, skipped, or impossible, with the reason and the §1 rule it protects.
3. **Deploy traps** — what breaks on machine B if only done on A; env vars; plugin installs; symlink targets.
4. **Tier log** — which tasks ran on which model.
5. **Version and hash** — `metadata.version` and `sha256sum faceless-video-craft/SKILL.md` at handback.
6. **§5 carried** — unchanged or with additions, each with a one-line reason.
7. Final line: `Awaiting: Kim writes "cut over" to run T10.`
