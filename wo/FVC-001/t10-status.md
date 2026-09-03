# T10 — Cutover — DONE

Video repo: commit `519285e` ("remove shadowing skill copies; canonical is claude-skills"), pushed. Skills repo: tagged `v2.1.0` at commit `a1f73ac`, pushed.

This was the most eventful task in the whole WO — three real, independently-caught defects got fixed in the ~30 minutes between Kim writing "cut over" and the actual deletion commit, plus one live scope decision. None of it was routine.

## What happened, in order

1. **Before touching anything**: sent a heads-up to all six `story-board-*` sessions live on this machine (91, 78, b0, 6a, 13, e2), since this is a real deletion in a shared working tree, not an additive change like T8's symlink.
2. **story-board-b0 raised a real scope question**: T10's literal glob (`faceless-video-craft*`) deletes v1 (the craft/engine layer) as well as v2 — but v1 was never fully absorbed into the extracted repo (only 8 sections, as restored rules; the rest — including content peers added *that same evening* — has no home elsewhere). Put this to Kim directly rather than deciding it myself. **Kim's answer: delete both, per the literal text** — a deliberate call, not the glob catching v1 by accident.
3. **story-board-13 found a real bug in my own work**: `claude-skills`' `restored-v1-rules.md` R5 was a stale 96-line excerpt claiming (via a provenance line I'd updated in T8's wipe-correction pass) to be the current 305-line rule. Verified independently, found a second, unrelated error in the same rule (wrong section citation — "Pre-render gate" instead of "Verification loop"), fixed both, and re-ran a **full-body** substring check (not the head/tail-fragment check that let this slip through originally) against all eight restored rules — all eight now pass. Commit `69fe812`, pushed *before* proceeding with the deletion.
4. **story-board-78 had already migrated the real channel data** (`videos/_channel/baseline.yaml` + `baseline-notes.md`, video-repo commit `becfaec`) — closing a gap I'd flagged back in T3 and explicitly deferred rather than resolved. Verified their files directly before treating the gap as closed.
5. **Re-checked git status fresh** on the exact two target paths immediately before deleting (clean), then executed `git rm -r` on both directories and committed with the WO's exact required message plus full context.
6. **Post-cutover, story-board-78 did real verification** (not assumed) and found one more pre-existing defect: `decision-policy.md`/`pipeline-runbook.md` instruct writing a `shorts_feed_share` field, but the actual template (and now the real migrated data) has always used `shorts_feed` — a mismatch that predates this WO, just never caught. Fixed (commit `a1f73ac`) by correcting the prose to match the established field name rather than renaming the template and forcing a second cross-repo coordination.

## Accept check

- **`git tag`** — `v2.1.0` exists in the skills repo, pushed.
- **`ls .claude/skills/` in the video repo** — the directory doesn't exist anymore (both subdirectories it contained are gone; nothing left to list).
- **`/skills` on machine A after a fresh session** — not literally re-verified via a fresh nested session (same OAuth-contention risk as T8's unresolved check), but this session's own live skill list updated the moment the project-level copies were deleted: it now shows exactly one `faceless-video-craft` entry, with the description matching `claude-skills`, not either of the two now-deleted project copies. That's real evidence, not a guess, though it's this session's own system state rather than an independent fresh-session check — worth Kim confirming with an actual `/skills` run when convenient, same recommendation as T8.

## Why this took real care rather than being mechanical

Three genuine defects (the v1-scope question, R5's truncation, the shorts_feed mismatch) surfaced in the final minutes before an action that's expensive to reverse cleanly (not undoable by a simple revert — v1's invocability, once gone, doesn't come back just because the text is in git history). All three got independently verified before being treated as real, and two were fixed *before* the deletion made them harder to cross-check against the source they were supposed to reproduce.

## What's now true

- `github.com/seoulhabit/claude-skills`, tag `v2.1.0`, is the sole canonical copy of `faceless-video-craft`.
- The video repo (`Story Board`) no longer has any project-level skill copy — `~/.claude/skills/faceless-video-craft` (T8's symlink) is the only path that resolves the name on this machine.
- `videos/_channel/baseline.yaml` now holds this channel's real measured data, migrated out of the skill it used to live inside.
- v1 (the craft/engine layer, `.claude/skills/faceless-video-craft`) is no longer invocable as a skill anywhere — recoverable as text from git history (`git show 01e4874:.claude/skills/faceless-video-craft/SKILL.md` in the video repo, or `archive/v1-repo-2026-09-01/SKILL.md` in `claude-skills`), but not as something Claude Code will load by name. This was Kim's explicit, informed choice.

WO-FVC-001 is complete.

## Addendum, 2026-09-03: "canonical is claude-skills" isn't true in every worktree

Post-cutover verification kept going after the commit landed. Net finding, independently confirmed (`git worktree list` + a line-count check in each, run directly, not taken on a peer's word): **T10's `git rm` only touched the `master`-branch working tree.** This repo has four other registered worktrees, each its own checkout on its own branch, and `git rm`/commit on `master` doesn't propagate to them:

```
/Story Board                                cc48804 [master]                                — cutover applied, no faceless-video-craft skill dir
/Story Board/.claude/worktrees/eager-cori-d241cf        f3f95d3 [claude/eager-cori-d241cf]        — .claude/skills/faceless-video-craft/SKILL.md, 1318 lines (pre-cutover v1, Aug 31)
/Story Board/.claude/worktrees/frosty-payne-63d79d      9234403 [claude/infallible-einstein-8d1759] — no faceless-video-craft skill dir
/Story Board/.claude/worktrees/goofy-robinson-23a416    34cf30b [claude/loving-newton-12b8db]       — .claude/skills/faceless-video-craft/SKILL.md, 1317 lines (pre-cutover v1, Aug 31)
/Story Board/.claude/worktrees/laughing-goldberg-1a051f 2d53907 (detached HEAD)                     — .claude/skills/faceless-video-craft/SKILL.md, 1897 lines (pre-cutover v1, Aug 31)
```

A session started with cwd inside any of the three affected worktrees resolves a project-level `faceless-video-craft` skill that is stale v1 from two days before the cutover — not a name collision with anything currently *running* (each worktree is its own isolated checkout), but the one place on this machine where "canonical is claude-skills" isn't actually true on disk.

Also found, lower stakes, same wider search: a byte-identical unzip of `dist/faceless-video-craft-2.1.0.zip` sitting in `~/Downloads/faceless-video-craft/` (harmless — same content as the real one, just a stray extra copy), and a 190-line v2 snapshot inside a review workspace under `~/Documents/Codex/2026-09-02/` (not a skill path, doesn't resolve as anything invocable).

**Not touched.** Pruning a git worktree is destructive (`git worktree remove`), and these are other sessions' own branches — not something to clean up unilaterally. Whether/when to remove the stale worktrees, or just leave them until whatever created them finishes with them, is Kim's call.

(Credit where due: this was surfaced by a peer session's own self-correction — they'd first miscounted "three copies remain" post-cutover, conceded it was wrong when I couldn't independently verify a third, then re-searched properly and found these five instead. Worth recording that the correction process worked, not just the finding.)
