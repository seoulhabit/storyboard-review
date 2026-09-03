# Story Board

## Shared catalog

This repo's shared catalog of reusable imagery, marks, and components lives
at [`catalog/`](catalog/) — start with [`catalog/README.md`](catalog/README.md)
(what's in each subfolder) and [`catalog/index.html`](catalog/index.html) (a
browsable gallery, grouped by what kind of thing each entry is and, for
components, how it's driven — clock/select/none).

Before generating or licensing new plates, or building a scene's mechanism
from scratch, check `catalog/` first for something already sourced, proven,
and reusable. This applies to visual components as much as imagery — a
component's own mechanism (its layout, its timeline) is as worth checking for
as a raw plate is.

## Concurrent sessions: work in your own worktree

Several Claude sessions often work this repo at once. **Do not work in the
shared checkout at `~/Desktop/Story Board` — give yourself a worktree:**

```bash
./worktree.sh new <your-session-name>   # isolated tree on its own branch
./worktree.sh status                    # what every tree is on, and what is at risk
./worktree.sh guard                     # exits 1 if you are in the shared tree
```

History stays shared; the checkout does not. Merge back with a normal PR, or
`git merge --no-ff session/<name>`.

**Why, from one evening (2026-09-02/03):** a `reset --hard` orphaned two
commits; a merge checkout destroyed an uncommitted `HANDBACK.md`; and two
different sessions' commits landed on a feature branch neither intended,
because the shared tree was switched under them mid-operation.

None of that was a tool bug, and checking `git status` first would not have
caught any of it — the damage happens in the gap between *checking* state and
*acting* on it. That gap cannot be closed by being careful. It closes by not
sharing the tree.

Two habits for whatever you cannot isolate:

- **Check the branch immediately before you commit**, not just the diff. A
  clean `git status` says nothing about which branch you are on, and the shared
  checkout can move between your check and your commit.
- **Commit early.** Untracked and uncommitted files have no reflog and no
  recovery path. Every irrecoverable loss in the incident above was work that
  had not been committed; everything committed was recovered.

`./worktree.sh` never deletes a worktree or moves a ref. `status` reports stale
trees along with what would be lost, and removing one is a human decision.
