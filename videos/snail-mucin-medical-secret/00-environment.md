# Environment — snail-mucin-medical-secret

Written by S0.0, first thing, before any other stage.

**Skill version:** 2.1.0
**Surface:** code (Claude Code, desktop app)
**Host:** Darwin 24.6.0 / macOS 15.7.9, x86_64 · node v24.18.0 · Python 3.9.4 · ffmpeg/ffprobe at /usr/local/bin

**Paths** (see SKILL.md §Paths):
- OUT: `<repo>/videos/snail-mucin-medical-secret/`
  — `/mnt/user-data/outputs/` was tested fresh this run and does **not** exist on this host.
- CHANNEL: `<repo>/videos/_channel/` (baseline.yaml, spend.jsonl, policy-change-proposals.md all present)
- `<repo>` = `/Users/sumitchoudhary/Desktop/Story Board/.claude/worktrees/render-review-optimizations-781b9e`
  (a git worktree on branch `claude/render-review-optimizations-781b9e`; the shared checkout was not touched)

**Companions resolved** (SKILL.md §Companion-skill gates):
- frontend-design: see ledger (fired at S6 entry)
- design-critique: see ledger (fired at S7 on extracted frames)

**Providers reachable:**
- vidIQ: `not called` — render mode makes no vidIQ decision; no credits spent.
- HyperFrames: `ok` — project pin **0.8.17** (`package.json` scripts), used for both `check` and `render`.
  A global `hyperframes` 0.8.27 is also on PATH; **not** used, because raising a project's
  engine pin behind its back would change render output and break the project's own
  reproducibility contract (project CLAUDE.md §Pinned CLI version).
- Higgsfield: `not called` (no new plates needed)
- Gemini: `not called` (no new plates needed)

**Project skill in play:** `none`.
There is no `SKILL.md` anywhere in this repo and no `snail-mucin-medical-secret` skill in
`~/.claude/skills/`. `videos/snail-mucin-medical-secret/CLAUDE.md` is the generic HyperFrames
project template (byte-identical to its `AGENTS.md`) and carries no brand palette, roster or
truth rules. So `decision-policy.md` §Claims `K-*` applies as the **floor**, undelegated.

**Budget in force:** no paid provider call in this mode; 0 vidIQ credits.
**Mode:** `render` — S0.0, S5–S7. S1–S4, S8, S9 not run (see 09-run-report.md).
