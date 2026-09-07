# 00-environment.md — pdrn-left-the-clinic

## Version and drift check

- **This run's skill version:** `0.3.0` (`metadata.version`,
  `makemeavideo/SKILL.md`).
- **Resolved from:** `/Users/sumitchoudhary/Desktop/claude-skills-current/makemeavideo`
  — a fresh clone on branch `master`, commit `9c14bb9`.
- **Drift check: clean, no workaround needed this run.** `~/.claude/skills/makemeavideo`
  resolves via symlink to the path above, which tracks `origin/master` directly
  (no other session's uncommitted work on it). This closes the drift finding
  `videos/centella-asiatica/00-environment.md` carried — the old shared
  `~/Desktop/claude-skills` checkout no longer exists; it was replaced by
  `claude-skills-current`, cleanly.
- Registry description drift still open, not load-bearing for this run: the
  `anthropic-skills:makemeavideo` listing text is 0.1/0.2-era ("built by
  HeyGen Video Agent"); the on-disk skill invoked here is 0.3.0. Named for
  whoever next reconciles the skill listing metadata.

## Surface and paths

- Surface: local repo (Story Board), in an isolated worktree per
  `CLAUDE.md`'s concurrent-sessions convention (`./worktree.sh new pdrn-clinic`,
  branch `session/pdrn-clinic`) — not the shared checkout.
- `OUT` resolved to: `videos/pdrn-left-the-clinic/`
- `CHANNEL` resolved to: `videos/_channel/` — `baseline.yaml` present,
  `populated: true`, `updated: 2026-09-03`.
- `<repo>` = `/Users/sumitchoudhary/Desktop/Story Board`, worktree
  `.claude/worktrees/pdrn-clinic`, branch `session/pdrn-clinic`, forked from
  `master` `76af03e`.

## Companion roster

- `frontend-design` (S3, S5b) → found (listed skill).
- `design-critique` (S7) → not found as a standalone listed skill this
  session; S7's read-the-words checks (K-4's two non-mechanical items) will
  be done directly against the extracted frames instead, named as a
  substitute rather than silently skipped.

## Provider reachability

- **HeyGen** (`get_current_user`): reachable. `plan: pro`,
  `premium_credits.remaining: 243`, `add_on_credits.remaining: 41`,
  `wallet: null`. Matches the brief's own note: `create_speech` still returns
  HTTP 402 `insufficient_credit` against a **separate "api" credit pool**
  this endpoint doesn't expose — confirmed structurally the same shape T1
  found (`wallet: null`), not re-attempted here since the brief already
  closes this question (§0: use Higgsfield for VO, do not top up HeyGen).
- **vidIQ** (`vidiq_balance`): reachable. `totalCredits: 325`
  (`renewableCredits: 0` of 2000, resets 2026-10-01; `addOnCredits: 325` of
  1000). Down from the handback's `335` — some spend happened between
  T8 and now, outside this run.
- **Higgsfield** (VO, per brief §0): not re-probed this run — the brief
  states the VO reference block (§4) was already preflighted and generated
  live on 2026-09-07, 2.4 credits/60-word block, and closes T1/F2. Treated
  as a closed finding, not re-verified live, per the brief's own "do not
  re-ask" instruction.

## QA capability probe

- Face detector: not re-verified this run (no render attempted — see
  "What this run does not do," below). Prior confirmation:
  `opencv-python-headless==4.10.0.84`, both Haar cascades present
  (`videos/centella-asiatica/00-environment.md`, same machine).
- `catalog/tooling/` resolution: `<repo>/catalog/tooling/` — present.

## Render machine

- `hyperframes --version` → **0.8.30** (required ≥ 0.8.23 — pass). Resolved
  path: `~/.nvm/versions/node/v24.18.0/bin/hyperframes`, the bare binary
  (never `npx`).
- `videos/_system/MANIFEST.json` drift check: **ok, re-verified this run**
  — independent sha256 check against all 67 files in the live
  `videos/_system/` tree: `missing: []`, `mismatches: []`. Design-system
  tree is exactly what `MANIFEST.json` says it is, before this run touches
  anything.
- No render attempted this run — see below.

## Budget in force

- `providers.yaml` `budget.per_run_cap`: `null` → `BLOCKER-BUDGET-UNSET`
  per `H-7`'s own default. **Not a hard halt yet**: no HeyGen-credit-bearing
  call has been made or is planned before Phase A's Design ruling lands.
  Will bite for real at S2/S3 (vidIQ) if this run continues past the K-1
  brief — named now so it isn't a surprise later.
- `providers.yaml` `budget.vidiq_preproduction_cap`: `200` (credits, not the
  WO's own specified-but-unimplemented 8-call cap — see decision ledger).
- No vidIQ or HeyGen credit-bearing call made in this run to date. `325`
  vidIQ / `243`+`41` HeyGen credits confirmed at start, unchanged.

## What this run does and does not do (scope note)

Per this run's own plan: **Phase A** (a written build-spec request pushed to
the Claude Design project, since the design system has no imagery primitive
this brief's cinematography needs) and **Phase B** (every production
artifact not blocked on Design's ruling: this file, `01-story-brief.md`'s
full `[K-1]` table, `00-decision-ledger.md`, and a typographic beat-sheet
mapping every story beat to an existing emitter). **S4b (VO), S5b
(composition/compile) and S6 (render) do not run this pass** — compiling
against `videos/_system/` before Design answers the imagery ruling would
either (a) render a video visually unlike the brief's own intent, silently,
or (b) require inventing components outside any ruling, which this run's
own plan explicitly forbids. Resuming past this point is a `build`-mode
call once Design's ruling lands.

## Mode and blockers named here

- Mode: `new` → `full`, but **intentionally stopped after S1** (see scope
  note above). `request.yaml` validated: `ok mode=new slug=pdrn-left-the-clinic
  format=both language=en attachments=0` (`validate_request.py`, run
  directly, not simulated).
- No `BLOCKER-*` token fires. The stop point is a scope decision recorded in
  `00-decision-ledger.md`, not a rule failure.
