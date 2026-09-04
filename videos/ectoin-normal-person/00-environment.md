# Environment — ectoin-normal-person (cold-open revision)

Written by S0.0, first thing, every mode, before any other stage.

**Skill version:** 2.1.0
**Surface:** code (Claude Code desktop app, this worktree)
**Host:** Darwin x86_64

**Paths** (see SKILL.md §Paths):
- OUT: `/Users/sumitchoudhary/Desktop/Story Board/.claude/worktrees/faceless-video-feedback-6c6c24/videos/ectoin-normal-person/`
  (`/mnt/user-data/outputs/ectoin-normal-person/` does not exist on this host —
  tested fresh, not assumed)
- CHANNEL: `/Users/sumitchoudhary/Desktop/Story Board/.claude/worktrees/faceless-video-feedback-6c6c24/videos/_channel/`

**Companions resolved** (filled in as each gate fired during the run):
- frontend-design: skill-tool (S6 entry)
- design-critique: skill-tool (S7, on 5 extracted frames)

**Providers reachable:**
- vidIQ: not probed — S0–S3 skipped this run (subject/seed unchanged, revision only)
- HyperFrames: ok, global CLI 0.8.27; project pins `hyperframes@0.8.22` in every
  `package.json` script — every CLI call this run uses `npx --yes hyperframes@0.8.22`
  to match the pin, not the global version
- Higgsfield: ok — `balance` measured 2275.25 credits, free plan
- Gemini: no-key — `GEMINI_API_KEY` unset; PR-1/PR-2 fall to `current-vo` (Higgsfield)
  wherever the policy would otherwise reach for Gemini

**Project skill in play:** none (repo has no channel-specific project skill;
confirmed by `hyaluronic-acid-vs-filler/00-environment.md`'s same finding)
**Budget in force:** $5.00 per-run cap (`providers.yaml`), 200 vidIQ credits
(not spent this run — S0–S3 skipped)
**Mode:** `full (revision)` — S0.0 runs; S0–S3 skipped (subject and seed
keyword unchanged, reused from the shipped 5:59 cut at commit `406ad4f`);
S4–S7 run; S8 updated in place (chapters, thumbnail); S9 skipped, nothing
published this run.

**Note on artifact format:** this project predates the v2.1 numbered-artifact
convention — its record is `BRIEF.md` / `SCRIPT.md` / `STORYBOARD.md` /
`DELIVERY.md` plus a 17-script `scripts/` generator pipeline, the same shape
as its sibling `ectoin-survival-molecule`. There is no written mapping from
that format to the nine numbered artifacts, and no exemption from writing
them either. This run writes `00-environment.md` (this file),
`00-decision-ledger.md`, and `09-run-report.md` as required "every mode, no
exceptions," and folds `01-story-brief.md`'s required content (the K-1 claim
table) into `BRIEF.md` §Sourcing rather than duplicating it — logged as a
`[NOT IN SKILL]` finding.
