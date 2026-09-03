# Environment — kbeauty-label-trap

Written by S0.0, first thing, before any other stage.

**Skill version:** 2.1.0 (`~/.claude/skills/faceless-video-craft` → symlink →
`~/Desktop/claude-skills/faceless-video-craft`, local HEAD `6d70e4d`, verified
== `origin` HEAD this run — "pick up latest skill" is satisfied, nothing to pull).
**Surface:** code (Claude Code CLI; Skill/Bash/MCP tools present, no sandbox
output mount).
**Host:** Darwin 24.6.0 arm64 · node v24.18.0 · python 3.9.4 · ffmpeg/ffprobe 8.1.2.
**Worktree:** `.claude/worktrees/kbeauty-ingredient-video-675976`, branch
`claude/kbeauty-ingredient-video-675976` (isolated per this repo's own
CLAUDE.md concurrency convention — not the shared checkout).

**Paths** (see SKILL.md §Paths):
- OUT: `/Users/sumitchoudhary/Desktop/Story Board/videos/kbeauty-label-trap/`
  — `/mnt/user-data/outputs/` tested fresh this run, **absent**, so the repo
  path applies.
- CHANNEL: `/Users/sumitchoudhary/Desktop/Story Board/videos/_channel/`
  — exists, git-tracked, `updated: 2026-09-03` (today).

**Companions resolved** (filled in as each gate fires):
- frontend-design: not yet resolved (fires S3, S6)
- design-critique: not yet resolved (fires S7)

**Providers reachable:**
- vidIQ: `ok` — `vidiq_balance` → 2246 credits (1446/2000 renewable, resets
  2026-10-01; 800 add-on).
- HyperFrames: `ok` — global CLI on PATH, `hyperframes --version` → **0.8.26**.
  This diverges from the two prior long-form runs' pin (`0.8.22`, taken from
  `ectoin-survival-molecule/package.json` and a machine-written `check.json`).
  Per this repo's own memory (`project-hyperframes-cli-global`), the CLI is
  invoked bare, never via `npx hyperframes@<pin>` — `npx` re-accumulates a
  ~364MB cache per run. This run pins **0.8.26** (the actually-installed
  version) and reads `hyperframes docs <topic>` for 0.8.26 before any markup,
  rather than carrying the stale 0.8.22 pin forward unverified. Logged as a
  `[NOT IN SKILL]` divergence from `pipeline-runbook.md`'s literal `npx
  hyperframes@<pin>` wording — see `videos/_channel/policy-change-proposals.md`.
- Higgsfield: `ok` — 2344.95 credits, plan `free`. `list_voices` confirms
  **Kimberly** `674b71b8-1d2e-4087-8567-d1f53c0b9f3c` (`voice_type: element`)
  still exists, as `providers.yaml` §tts `current-vo` requires and as the
  operator explicitly asked for.
- Gemini: `no-key` — `GEMINI_API_KEY` unset. Consequences (neither a halt):
  - `[PR-1]` grounded research never fires. Claim sourcing runs on the 5
    operator-supplied anchors (FDA, EU 1223/2009, MFDS, 2 PubMed reviews),
    each fetched and read live this run, plus PubMed MCP / WebFetch for any
    gap claim (Q4 evidence-hierarchy framing, the "low levels" and "gentle
    isn't universal" claims) — the project's own source list, which is what
    PR-1 sits behind anyway.
  - `[PR-2]` selects `current-vo` (Higgsfield `generate_audio`, Kimberly)
    rather than `gemini-tts`. No `listening-test pending` flag (scoped to
    gemini-tts runs only).

**Project skill in play:** none — confirmed by search; `faceless-video-craft`
states the repo has none. `decision-policy.md` §Claims (`K-*`) applies as the
undiluted floor. Brand tokens inherit from
`videos/ectoin-survival-molecule/assets/tokens/tokens.css` (the canonical
landscape/16:9 set), with one project-local addition: `--vermilion` (no
existing token covers the brief's "one vermilion evidence mark" — operator
confirmed adding it over aliasing `--coral`).

**Budget in force:** `providers.yaml` §budget — **$5.00/run**, `warn_at` 0.8,
**200 vidIQ credits**. Tracked in `cost-log.jsonl` beside this file. Comparators
from `videos/_channel/spend.jsonl`: `hyaluronic-acid-vs-filler` fresh run
$0.884/112 credits; its v2 revision (S0–S3 reused) $0.322/0 credits.

**Mode:** `full` (story supplied, no narrower intent stated; no `wrappers/`
directory exists in this skill to infer mode from, so stated explicitly here).

**Operator decisions on record, made via AskUserQuestion before this run
started** (all four route a genuine judgment call the skill has no default
for, per the skill's "never invent, never guess" rule):
1. **Runtime**: measured VO + the brief's own authored pauses is the master
   clock; the nominal 5:00 target is not padded to match. 646 words of
   narration is below the S4 word budget (675–825 words for 300s); expect a
   real run length below 5:00, logged as a deviation not a defect.
2. **Hook length**: trim the two-bottle mystery to ≤20s (the `[S4/S-6]` hard
   cap), restructuring rather than cutting content — the "not a scorecard,
   it is a passport" thesis moves into the Misconception section, which also
   supplies that section's previously-missing explicit wrong-belief sentence.
3. **Vermilion**: add a project-local `--vermilion` token rather than alias
   the existing `--coral`.
4. **Music**: reuse-first — audition the three existing `track-pulse.wav` beds
   before generating a bespoke one.
