# WO-FVC-001 — Handback

T1–T9 complete and pushed to `github.com/seoulhabit/claude-skills` (12 commits, `db6105d`..`66c1940`). T10 not started — gated on this handback and Kim writing `cut over`. Full task-by-task detail lives in `wo/FVC-001/t1-status.md` through `t9-status.md`; this file is the WO's own required summary format (§6), not a replacement for those.

Two things happened outside the numbered tasks that matter as much as any of them: a live collision-risk decision at T8, and nine rounds of cross-session peer coordination (full transcript and verification in `wo/FVC-001/peer-coordination-log.md`) that caught and fixed a real shipped-content regression (a disproven transition default) within minutes of it going live. Both are covered below and in their own status files.

---

## 1. Attestation table

Every command below was re-run fresh for this handback, just now — not pasted from earlier claims.

| Task | Accept check | Command | Output excerpt |
|---|---|---|---|
| T1 | Commit history exists | `git log --oneline \| head -3` | `66c1940 T9...` / `5b582d4 ...` / `4fb5a41 ...` (12 commits total, `db6105d`..`66c1940`) |
| T1 | Release script + zip | `scripts/release.sh && ls -la dist/` | `✔ Validation passed` → `Wrote .../dist/faceless-video-craft-2.1.0.zip` |
| T1 | Validator exit code | (part of release.sh) | exit 0 |
| T2 | merge-matrix.md fully resolved | `grep -c '\| merge \|\|\| keep \|\|confirmed correct' merge-matrix.md` | `29` (every rule-ID row carries a verdict; 0 empty cells) |
| T2 | `hyperframes check` on the skeleton | `hyperframes check .` (scaffolded — the bare skeleton needs a real project directory and authored sub-compositions, not a bare file) | **PASS**, run for real 2026-09-03 once the CLI was installed here. `0 errors, 0 warnings` across lint/runtime/layout(9)/motion/contrast. See `t2-status.md`. |
| T2 | Lint vs `check` delta, explained | `python3 scripts/lint_composition.py fail_lazy_image.html` vs `hyperframes check .` on the same fixture | **PASS, resolved 2026-09-03 — not a disagreement.** lint: 2 errors, exit 1. `check`: 0 findings, exit 0. Root cause found, not a standoff: the lazy/decoding rule was never traceable to the engine (`hyperframes-engine.md` §10 was the only section missing a `*(source)*` line; none of `check`'s 248 lint rule ids covers image loading). `lint_composition.py` is a deliberate superset; the WO's own Accept text was corrected from "reconcile until agree" to "record each delta with its cause" (`docs/wo/WO-FVC-001.md`:57, commit `068fbb7`). No longer needs Kim's call. See `t2-status.md` §4. |
| T3 | Description ≤ 500 chars | `python3 -c "...len(desc)..."` | `chars: 479` |
| T3 | Only guarded `/mnt` patterns remain | `grep -rn '/mnt' faceless-video-craft/` | 8 hits, all conditional (`if that directory exists`), a documented fallback, or an explicit prohibition — none assume `/mnt` exists |
| T3 | Five wrappers exist | `ls wrappers/` | `produce video-audit video-package video-readout video-render` |
| T4 | Skill-tool call visible in a dry run | — | **Blocked.** Needs a real `/produce` invocation; static wiring confirmed instead (`grep -rln COMPANION`: `SKILL.md`, `pipeline-runbook.md`, both templates). |
| T4 | `COMPANION` MISSING line with plugin disabled | — | **Blocked**, same reason. |
| T5 | `tests/run.sh` exit 0 | `bash tests/run.sh` | `15 passed, 0 failed` |
| T5 | Each failing fixture exits 1, named | (part of tests/run.sh) | all 8 fixture-based assertions pass |
| T6 | Render dry run produces both files, Stages table correct | Full `render`-mode run against a scratchpad copy (`00-environment.md` + `09-run-report.md`) | **PASS**, run for real 2026-09-03. All 11 stage rows present; `skipped (mode=render)` exact-match on S0-S4/S8/S9; `ran` on S0.0/S5-S7; S7's `hyperframes check` gate exit 0. Original pre-T6 render directory confirmed untouched. See `t6-status.md`. |
| T7 | Dry-run price matches the yaml | `provider_call.py gemini text --dry-run --in 1000 --out 1000` | `est=$0.0045` (hand-computed: `1000/1e6*0.75 + 1000/1e6*3.75 = 0.0045` — matches) |
| T7 | Real Gemini calls produce three cost-log lines | — | **Blocked.** `GEMINI_API_KEY` genuinely unset on this machine (Kim's ☐ item, not yet done). |
| T7 | Run report Spend table | — | Built into `assets/run-report.template.md` (T6); not populated by a real run. |
| T7 | Key-unset shows fallback, not a crash | `echo "${GEMINI_API_KEY:+set}${GEMINI_API_KEY:-unset}"` then `provider_call.py gemini text --in 100 --out 100` | `unset` → `GEMINI_API_KEY not set -- ... use --dry-run ...` — exit code **3**, no traceback |
| T8 | Symlinks point where they should | `readlink ~/.claude/skills/<name>` ×6 | all six resolve into `~/Desktop/claude-skills/{faceless-video-craft,wrappers/*}` |
| T8 | `claude plugin validate ~/.claude/skills` | (as written) | `✔ Validation passed with warnings` (expected symlink-following caveat) |
| T8 | `/skills` shows exactly one entry, source personal | — | **Unverified.** Two nested `claude -p` attempts both failed on OAuth (transient contention, then "session expired") — plausibly from the several other live sessions on this machine. Did not force a third attempt (see §2). |
| T8 | `/produce` in the `/` menu | — | **Unverified**, same reason. |
| T9 | `benchmark.json` pass rate ≥ v1 | — | **Blocked.** `claude plugin eval` is early-access-gated on this org (confirmed by running it, not assumed). |
| T9 | Trigger precision ≥ 0.9 | — | **Not measured.** Manual prediction only (`evals/description-trigger-precision.md`, 11+11 prompts) — explicitly not a substitute for the real metric. |
| T9 | Results in `faceless-video-craft-workspace/` | — | **Blocked**, same gate — that directory is the tool's own output location and was never created. |
| T9 | `evals/evals.json` committed | `git log`, `evals/` tree | Committed at `66c1940`; real deliverable is the 7 `<case>/prompt.md`+`graders/*.md` directories, `evals.json` is a manifest (format mismatch from the WO's text — see `t9-status.md`) |

## 2. Refusals on record

| What | Reason | §1 rule protected |
|---|---|---|
| Did not fabricate `hyperframes check`, render, or eval results anywhere the CLI/tool was unavailable | No CLI installed / feature gated; a fabricated pass would be worse than an honest blocker | §1.9 (read-back verification, never mutation echo) |
| Did not set a `claude plugin eval` enablement env var, or touch `~/.claude/settings.json`, on the strength of a research agent's suggestion | That needs Kim's actual Anthropic-issued credential, not a guess | Authentication is a named legitimate stop (§1.5) |
| Did not retry the failing nested `claude -p` session-resolution query a third time | Two failures (contention, then "session expired") in a machine already running 4+ concurrent sessions; a third attempt risks more shared-auth contention, not less | §1.5 (authentication as a legitimate stop) |
| Did not commit or push anything in the video repo (`Story Board`) itself | T10 is the only task scoped to touch that repo's git history, and it's gated on Kim's `cut over`; everything else stayed in the new `claude-skills` repo or as local untracked files | Scope discipline (§1.8) |
| Did not build the two-check snapshot-freshness guard `story-board-13` correctly identified as missing (see peer log, messages 6–8) | Real repo-design decision (hash+pin the archive against its source commit) — recorded as a finding, not built unprompted | Scope discipline (§1.8); "no creative-preference questions" cuts both ways — don't invent scope either |
| Did not resolve case 4's exposed language-policy gap, or case 7's measured true-peak failure, by editing `decision-policy.md` or re-mastering the file | Both are real findings from authoring T9, not T9 tasks themselves; fixing them wasn't asked for and would have widened scope mid-eval-authoring | §1.8; §1.4 (policy changes go through the learning loop / Kim, not an ad hoc edit) |
| Did not do the GEMINI_API_KEY / plugin-install / claude.ai upload steps in T8 | Explicitly marked ☐ ("Kim does the parts marked ☐") in the WO itself | WO's own T8 spec |

## 3. Deploy traps

- **Machine B has not been touched at all.** Everything in T8 (`git clone`, the six symlinks) was done only on this machine ("machine A" in the WO's own framing). Machine B needs the identical clone + six `ln -s` commands — `t8-status.md` has the exact paths.
- **`GEMINI_API_KEY` unset here** — until Kim sets it (shell profile, per T8's ☐ item), `PR-1`/`PR-2`/`A-1` all correctly fall back to non-Gemini providers on every machine missing it. That's designed behavior, not a bug, but it means Gemini-path code (`provider_call.py`'s real-call branches) is **unverified against the live API anywhere so far** — confirm on whichever machine gets the key first.
- **Plugin installs — corrected 2026-09-03.** This bullet previously listed three installs (`frontend-design`, `design`, `skill-creator`) as still ☐ here. All three claims were wrong. `frontend-design@claude-plugins-official` and `skill-creator@claude-plugins-official` are **already enabled** on this machine (`~/.claude/settings.json` → `enabledPlugins`), and **`design` is not an installable plugin at all** — it does not exist under that name in `claude-plugins-official`, the same nonexistent reference `0bac6c9` removed from SKILL.md. `design-critique` needs no install: it resolves through the Skill tool as `design:design-critique`, which `t4-status.md`:20 had already recorded, contradicting this bullet. So T4's companion gates resolve normally here rather than falling through to file-path-or-MISSING. Machine B's plugin state remains unverified — that part of the trap still stands.
- **`claude plugin eval`'s early-access gate reads as organization-level**, not per-machine — enabling it once should cover every machine under the same Anthropic org, but this wasn't independently confirmed (see `t9-status.md`).
- **HyperFrames CLI — installed on this machine 2026-09-03, after this handback was written.** This bullet used to say "this machine doesn't have it", which blocked several Accept checks (T2, T6, and eval cases 1/2/4/7) for want of a machine that did. It now has `hyperframes` **0.8.26** globally (`npm i -g hyperframes`, nvm prefix for Node v24.18.0), with FFmpeg/FFprobe 8.1.2 and the headless-Chrome cache present; `doctor` is green on every core-path check and fails only optional ones (Kokoro TTS, Docker). **Those Accept checks are unblocked here** and no longer need to wait on machine B. Invoke it as bare `hyperframes`, not `npx hyperframes` — npx re-creates a ~364MB cache per version (11 had accumulated, 4.01 GB, cleared the same day). Machine B's CLI status is still genuinely unknown.
- **`archive/v1-repo-2026-09-01/SKILL.md` is a manually-refreshed snapshot**, not a live link — refreshed once already (post-T8, see below) after going stale between T1 and T8. Nothing currently re-checks it automatically; see the peer-log finding about needing a two-check guard (internal-consistency, which exists in the video repo but gets deleted at T10 either way, plus snapshot-freshness, which exists nowhere yet).
- **claude.ai's skill upload is a separate surface entirely** — `dist/faceless-video-craft-2.1.0.zip` is built and current as of this handback, but the actual upload/delete-old-entry step is ☐ and machine-independent (it's account-level, not local).
- **The account-level plugin cache is stale — a traceability bug, not a content-integrity one.** `story-board-b0` found and both of us independently verified by diff: `~/Library/.../skills-plugin/.../skills/faceless-video-craft` resynced to `metadata.version: 2.1.0` at 2026-09-03 00:43, before `98ef6c7` landed. Its `restored-v1-rules.md` carries the exact pre-fix R1/R2/R6 `Source:` pointers (all three citing `§Verification loop` instead of their real sections). `b0` then narrowed it further, correctly: stripping just those three `**Source:**` lines and re-diffing gives byte-identical files — every rule *body* on the cached copy is the same correct text a reader on the canonical repo gets. So this fails in the "can't verify where it came from" direction, not the "acts on wrong guidance" direction — someone following R1's citation to `§Verification loop` finds no type floors there and might conclude the rule is fabricated, but the type-floor text itself is right. `check_restored_citations.py` and `test_restored_citations.py` are absent from that copy, confirming the sync predates the guard. Fixing this needs the same ☐ re-upload step above, no code change — just don't mis-prioritize it as content corruption.
- **The heading-containment guard already exists — it just doesn't run against distribution artifacts.** `check_restored_citations.py` already asserts each rule body sits inside the section its `Source:` line names, not just "somewhere in the archive" — that check is exactly how R1/R2/R6 were caught in the first place (see the script's own docstring). The gap the stale cache exposes isn't a missing check, it's that nothing re-runs this guard against `dist/*.zip` before upload, or against a synced cache after one — a packaging/CI gap, not a tooling gap.

## 4. Tier log

| Task | Tier | Notes |
|---|---|---|
| T1 | Sonnet/medium | Main session |
| T2 | **Opus/High** | Workflow, 6 parallel agents (`claude-opus-5[1m]`) — the one deliberate tier switch, per §1.10 |
| T3 | Sonnet/medium | Main session |
| T4 | Sonnet/medium | Main session |
| T5 | Sonnet/medium | Workflow, 3 parallel agents (`claude-sonnet-5`) |
| T6 | Sonnet/medium | Main session |
| T7 | Sonnet/medium | Main session + one delegated agent (`provider_call.py`), inherited Sonnet tier |
| T8 | Sonnet/medium | Main session |
| T9 | Sonnet/medium | Main session + one delegated agent (`claude-code-guide` research), inherited tier |

Switched back down to Sonnet/medium immediately after T2, per §1.10.

## 5. Version and hash

```
metadata.version: 2.1.0   (unchanged since T1; no version bump taken during T1-T9)
sha256sum faceless-video-craft/SKILL.md:
  774b4e72944dbee9f35e7b1d51fb13cc921955e165e170ef8226d030ef8bcf0e
```

## 6. §5 carried

Unchanged from the WO's own text:
- Whether to trim `seoulhabit-video-3d` (open since Aug 29) — not touched.
- Wiring R01/CIR/MFS sources into the centella K-1 table (§1.2) — separate pass, not touched.
- Provider reordering by cost-per-view — still needs ≥3 published runs' data.
- Veo/Omni video generation — excluded by design.
- Multi-channel baselines — one channel only in this WO.

Updated:
- **Listening test, Gemini TTS vs `current-vo`** — the WO said "after T7"; T7 is now done, so this is unblocked and ready whenever Kim wants to do it. Still Kim's ears, not automatable.

New, found during T1-T9, not in the original §5:
- **A snapshot-freshness guard for `archive/v1-repo-2026-09-01/SKILL.md` doesn't exist yet.** The video repo's own `check_restored_citations.py` (built by peer sessions this same day) only checks internal consistency, not staleness against upstream — confirmed it would have passed cleanly on the exact stale content this WO shipped and then had to fix. Real repo-design decision; not built. (Peer log, messages 6-8.)
- **`claude plugin eval` needs org-level enablement from Anthropic** before T9 can actually execute anything it built. Not something this session can do.
- **Case 4's language-propagation gap**: `decision-policy.md` has no rule for how a requested language reaches voice/vidIQ-market selection. Candidate for a policy-change proposal, not fixed.
- **Case 7's true-peak finding**: `videos/centella-tiger-grass`'s existing delivery render measures -1.6 dBFS, failing the ≤ -2 dBFS this WO itself asserts as correct. Measured directly, not fixed — that file may need re-mastering independent of this WO.
- **The T3 description trim's possible trigger-recall cost** — cutting concrete example phrasings to fit the 500-char cap. Not undone; worth weighing now that it's visible.
- **Whether this skill's trigger surface should extend to Instagram/TikTok short-form**, surfaced by one deliberately-ambiguous trigger-precision test case. Open design question, not resolved.

---

Awaiting: Kim writes "cut over" to run T10.
