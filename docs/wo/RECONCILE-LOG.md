# Reconciliation Log (WO-SBR-001, T5)

## Conflict 1 — `claude/laughing-goldberg-1a051f` (PR #1)

- **File:** `.claude/skills/faceless-video-craft/SKILL.md`
- **Type:** modify/delete (PR #1 modifies it; `integrate/2026-09-04` — inherited
  from `origin/master` — has it deleted)
- **Which side won:** deletion. The file was removed.
- **Why:** verified via `git log --diff-filter=D` that master deleted this file
  (and the entire `.claude/skills/` directory) in commit `519285e`, "remove
  shadowing skill copies; canonical is claude-skills", dated 2026-09-03 —
  *after* PR #1 forked from an earlier point. PR #1's fix targets a file that
  has since been deliberately removed as a duplicate; resurrecting it would
  undo that cleanup.
- **Consequence for `docs/wo/BRANCH-REGISTER.md`'s Cluster 1:** this changes
  PR #1's own disposition, not just the three branches it was proposed to
  supersede. PR #1 no longer contributes anything mergeable — every branch in
  that cluster (`claude/laughing-goldberg-1a051f`, `rescue/34cf30b`,
  `rescue/f3f95d3`, `claude/eager-cori-d241cf`) is now moot, not just the
  three non-PR ones. **Correction, not silently absorbed**: flagged back to
  the user/Kim rather than merging PR #1 as originally planned. PR #1 itself
  should likely be closed on GitHub with this explanation, not merged — that
  action (closing a PR) wasn't taken here, only proposed.

## Merge 1 — `claude/snail-mucin-bottle-animation-1d3308` (PR #14)

- **Result:** `b3cbede`, clean merge, no conflicts.
- **Checks:** ruff/mypy/pytest all pass; `hyperframes check videos/snail-mucin-medical-secret-v2` → 0 errors (7 info-level layout-overflow advisories, pre-existing style notes, not merge-introduced).

## Blocked — `claude/kbeauty-ingredient-video-675976`

- **File:** `videos/_channel/spend.jsonl` — JSON-data. Per Rule 4, stopping to
  ask rather than resolving. `videos/_channel/policy-change-proposals.md`
  auto-merged cleanly on the same attempt (no conflict).
- **What the conflict actually is:** both sides independently *appended*
  distinct, non-overlapping log entries at the same point in the file (master
  added 2 snail-mucin-medical-secret entries; this branch adds 1
  kbeauty-label-trap entry). Not a real disagreement — a concatenate-both
  resolution looks safe — but per Rule 4 this needs a yes, not an assumption.
- **Status:** merge attempted then aborted, worktree left clean. Not yet
  resolved.

## Major correction — `session/ectoin-normal-person` and `claude/faceless-video-feedback-6c6c24` are superseded, not mergeable

- Attempting to merge `session/ectoin-normal-person` produced ~40 add/add
  conflicts across nearly every file in `videos/ectoin-normal-person/` —
  contradicting `docs/wo/BRANCH-REGISTER.md`'s "zero overlap" finding for
  this branch. Aborted immediately to investigate rather than resolve blind.
- **Root cause, found in the project's own decision ledger
  (`00-decision-ledger.md`, already on master):** master's copy of this
  project was not produced by merging either branch. Commit `72ab419`
  ("Import ectoin-normal-person from f893e7b, plus newer catalog tooling")
  did `git checkout f893e7b -- videos/ectoin-normal-person ...` — a content
  import from `claude/faceless-video-feedback-6c6c24`'s tip, done deliberately
  to avoid ref surgery on a branch that worktree didn't have checked out (the
  ledger cites CLAUDE.md's own guidance for this). That import breaks git's
  ancestry tracking for these paths even though the content lineage is real,
  which is exactly why a normal `git merge` now sees "independently added"
  files with no common history instead of a clean fast-forward.
- **Master then continued past that import** with three more commits
  (`80c55c1`, `5c13bc9`, `1d38a897` — the last already confirmed on master
  and already accounted for elsewhere in the register) doing real work: VO
  generation, a claim-ledger correction pass (reversing an earlier wrong
  claim-verification call, tightening an authorship claim), script
  compression, and a final render/gate pass.
- **Conclusion: master's `videos/ectoin-normal-person/` is strictly more
  advanced than both `session/ectoin-normal-person` (the pre-import state)
  and `claude/faceless-video-feedback-6c6c24` (the exact commit that got
  imported and then superseded).** Merging either now would not add new
  work — it would overwrite master's more-evolved content with an older
  snapshot. **Revised disposition for both: DROP (superseded), not MERGE.**
  Neither was merged. `docs/wo/BRANCH-REGISTER.md` Cluster 4 needs updating
  to reflect this — not done automatically here, flagged for the user.

## Merge 2 — `wip/storyboard-6a-2026-09-04`

- **Result:** `b1753ed`, clean merge, no conflicts (confirmed clean ancestry
  from the already-merged `session/story-board-6a` first via
  `merge-base --is-ancestor`, unlike the ectoin-normal-person case above).
- **Checks:** ruff/mypy/pytest all pass. No `hyperframes check` run — single
  binary media file, no composition logic touched.
