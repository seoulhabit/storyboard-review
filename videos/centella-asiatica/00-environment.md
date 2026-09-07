# 00-environment.md — centella-asiatica

## Version and drift check

- **This run's skill version:** `0.3.0` (`metadata.version`, `makemeavideo/SKILL.md`).
- **Resolved from:** `~/Desktop/claude-skills-worktrees/wo-fvc-005-t5/makemeavideo`
  (a detached worktree at `origin/master` `5a9f5b0`, the merged T7 commit).
- **DRIFT FOUND, and worked around, not ignored**: `~/.claude/skills/makemeavideo`
  (the Skill-tool-loaded copy) is a symlink to `~/Desktop/claude-skills/makemeavideo`
  — the **shared main checkout**, which is on branch `fvc-005/makemeavideo`
  (pre-T7, `version: "0.2.0"`) with another session's own uncommitted changes
  on it (`faceless-video-craft/` files). Invoking `/makemeavideo` via the
  Skill tool injects that stale 0.2.0 content. This run did **not** act on
  the stale injected content and did not touch the shared checkout (another
  session's uncommitted work is on it); it read every rule from the fresh
  worktree above instead — the canonical, merged 0.3.0 state. **Standing
  finding for whoever fixes it**: the `~/.claude/skills/makemeavideo` symlink
  needs to point at a checkout that tracks `origin/master`, or the shared
  main checkout needs its own branch fast-forwarded, before `/makemeavideo`
  can be invoked directly and trusted again.

## Surface and paths

- Surface: local repo (Story Board), `/mnt/user-data/outputs/` not present in
  this environment.
- `OUT` resolved to: `videos/centella-asiatica/`
- `CHANNEL` resolved to: `videos/_channel/` — `baseline.yaml` present,
  `populated: true`, `updated: 2026-09-03`. `heygen:` block present (T7).
- `<repo>` = `/Users/sumitchoudhary/Desktop/Story Board`, worktree
  `.claude/worktrees/wo-fvc-005-t5`, branch `session/wo-fvc-005-t5`, on
  commit `dc0f806` (includes T7's merge) at run start.

## Companion roster

- Skills available this session: full roster per the system's Skill listing
  (frontend-design, design-critique, and many others — see the session's own
  available-skills list). Both mandatory gates resolve to the real skill.
- `frontend-design` (S3, S5b) → found.
- `design-critique` (S7) → found.

## Provider reachability

- HeyGen: `get_current_user` → **not attempted** — T1-FINDINGS (WO-FVC-005)
  already established `BLOCKED-CONNECTOR` for this exact non-interactive
  session type (F2–F4), re-confirmed in T4's own testing. Recorded as
  `BLOCKED-CONNECTOR` (structural), not `unreachable` (transient), per the
  T7-updated template's own distinction. No credits-at-start to record since
  no HeyGen call was made.
- vidIQ: `vidiq_balance` → **ok**, `totalCredits: 355` (`renewableCredits: 0`
  of 2000 max, resets 2026-10-01; `addOnCredits: 355` of 1000 max).
- Gemini (research role): not probed — not needed for this run (K-1 draws
  from the pinned site repo's own already-sourced findings, no gap to fill
  via grounded search).

## QA capability probe

- Face detector: `qa_render.py`'s `resolve_detector()` path confirmed
  manually — `cv2 4.10.0`, both Haar cascades present at
  `cv2.data.haarcascades` (`opencv-python-headless==4.10.0.84`, the pinned
  version, installed in T4).
- `catalog/tooling/` resolution: `<repo>/catalog/tooling/` — present.

## Render machine

- `hyperframes --version` → **0.8.30** (required ≥ 0.8.23 — pass). Resolved
  path: `~/.nvm/versions/node/v24.18.0/bin/hyperframes`, the **bare binary**
  (never `npx`, per CLAUDE.md).
- Chrome reachable: confirmed via T4's own render tests this session (not
  re-probed with a fresh smoke render — T4's `t4-verification/` already has
  a real, recent, successful `hyperframes render` on this exact machine).
- `videos/_system/MANIFEST.json` drift check: **ok** — `check_manifest()`
  (imported from `compile_composition.py`) ran clean against the live
  `videos/_system/` tree (R-6's spacing.css hash included, confirmed
  up to date).

## Budget in force

- `providers.yaml` `budget.per_run_cap`: `null` → technically
  `BLOCKER-BUDGET-UNSET` per `H-7`'s own default — **not treated as a hard
  halt here**: the cap is denominated in HeyGen credits, and this run makes
  zero HeyGen calls (VO substitute, local render), so there is no HeyGen
  spend for an unset cap to fail to bound. Named, not silently passed.
- `providers.yaml` `budget.vidiq_preproduction_cap`: `200`.
- `usd_per_credit`: `null` (Gate 0 G0-4's $ half still open, WO sec 8.3).

## Channel setup state (S-4 finding — see run report)

- `baseline.yaml` `heygen.voice_id` / `brand_glossary_id`: both `null`
  (T2 `TOUCHPOINT-SETUP` never ran). **S-4's own carried rule, read
  literally, would halt here with `BLOCKER-SETUP-PENDING`** — this run
  does not take that literal halt: `voice_id` is unset for the identical
  reason S4b's own (T7-rewritten) local-substitute branch exists to handle
  (HeyGen connector unavailable, not an unrelated oversight), and S-4's
  text was not updated in T7 to say so explicitly. Treated as one finding
  (the connector gap), not two independent blockers. Flagged as a real T7
  loose end for a follow-up correction — see `09-run-report.md`'s
  `[NOT IN SKILL]` section.
- `style_id` / `tokens`: `null`, retired (T7) — the design system
  (`videos/_system/`) is the style now, referenced by path.

## Mode and blockers named here

- Mode: `new` → `full` (`request.yaml`, validated: `ok`).
- No `BLOCKER-*` halts this run at S0.0. Two named, non-halting findings
  carried forward: the skill-symlink drift (worked around), and the
  S-4/S4b rule inconsistency (resolved by treating them as one finding).
