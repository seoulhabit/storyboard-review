# Environment — ectoin-normal-person (2026-09-03 rebuild)

Written by S0.0, first thing, before any other stage.

**Skill version:** 2.1.0
**Surface:** code (Claude Code desktop app), git worktree
**Host:** Darwin x86_64 (24.6.0)

**Paths** (see SKILL.md §Paths):
- OUT: `/Users/sumitchoudhary/Desktop/Story Board/.claude/worktrees/snail-mucin-video-feedback-d3484b/videos/ectoin-normal-person/`
  (`/mnt/user-data/outputs/ectoin-normal-person/` does not exist on this host —
  tested fresh)
- CHANNEL: `/Users/sumitchoudhary/Desktop/Story Board/.claude/worktrees/snail-mucin-video-feedback-d3484b/videos/_channel/`

**Worktree note.** This project's most recent build lived only at commit
`f893e7b` on `claude/faceless-video-feedback-6c6c24`, checked out in a
different, concurrently-active worktree. This run imported the project
(`git checkout f893e7b -- videos/ectoin-normal-person catalog/tooling
catalog/visual-components/running-gag-badge`) onto this worktree's own branch,
`claude/ectoin-explainer-rebuild-ad081f`, and committed immediately as a
checkpoint (`72ab419`). No other branch's ref was read via checkout-into or
written to, per this repo's CLAUDE.md §"What a worktree does NOT protect."

**Companions resolved this run:**
- frontend-design: not yet fired — fires at S6 entry (before markup) and S3
  (thumbnail scoring). Recorded when reached.
- design-critique: not yet fired — fires at S7, on extracted frames.

**Providers reachable:**
- HyperFrames CLI: global bare binary, `hyperframes --version` → **0.8.27**
  (latest — `hyperframes upgrade` reported "Already up to date"). Project
  `package.json` previously pinned `hyperframes@0.8.22` via `npx --yes`; this
  run re-pins to **0.8.27** (operator decision — see `00-decision-ledger.md`)
  and switches every script from `npx --yes hyperframes@<pin>` to the bare
  `hyperframes` binary, removing the npx-cache re-accumulation problem on
  every invocation.
- Higgsfield (`generate_audio`, MCP): available this session for new/rewritten
  VO takes.
- vidIQ: not probed this run — no packaging/title/thumbnail re-score is in
  scope for the rebuild itself (S8 covers that; deferred to the run's later
  stage, see run report).
- Python deps: numpy 2.0.2, Pillow (PIL) 11.3.0, both required by
  `catalog/tooling/check-safe-area.py` / `check-static-hold.py`.
- ffmpeg/ffprobe 8.1.2 — required by `scripts/timing.py` (per-take duration),
  `scripts/gen_vo.py` (trim/pad/QC), `scripts/master-audio.py` (EBU R128).
- `git-lfs` 3.8.0 — `renders/ectoin-normal-person.mp4` (the prior, 4:57.02
  cut) resolved to a real 78,977,924-byte MP4 on import, not an LFS pointer.

**Project skill in play:** none (repo has no channel-specific project skill —
consistent with prior runs' finding).

**Mode:** `full (revision)` — this is a second revision of an existing,
gate-clean build, not a from-scratch S0–S3 run. Subject and cast (SOULHABIT /
JAY) are unchanged from the cold-open revision at `f893e7b`; the operator
brief supplies new requirements (claim ledger, verdict-in-20s, script
compression to ~430–500 words / 35–45 turns, storyboard frame declarations,
render hardening) in place of a new topic pick. S4 (script/storyboard) and
S5–S7 (composition, validation, preview) run in full; S8/S9 (publish
envelope, readout) are out of scope for this request and deferred.

**Note on artifact format** (carried forward from the prior run, still
true): this project predates the v2.1 numbered-artifact convention. Its
record is `BRIEF.md` / `SCRIPT.md` / `STORYBOARD.md` / `DELIVERY.md` plus a
generator pipeline in `scripts/`. This run adds `CLAIMS.md` as the explicit
claim ledger the brief requires (narration · on-screen claim · primary source
· publication date · limitations · industry connection · approval status) —
folding it into `BRIEF.md` §Sourcing, as the prior run did, would bury a
document the brief asks for by name. `00-environment.md` (this file),
`00-decision-ledger.md`, and `09-run-report.md` are maintained per the
"every mode, no exceptions" rule.
