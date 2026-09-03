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

### Moving out of the shared checkout

**If your work is untracked, copy it out of the repo before you touch git.**
"Commit first, then move" is wrong for untracked work: committing means either
landing on whatever branch the shared tree happens to be on — likely someone
else's — or running `git checkout -b` in the shared tree, which is the thing
this whole convention exists to stop. There is no safe in-tree commit for
untracked work when the tree is on a branch you did not choose. Copy the files
somewhere outside the repo, make your worktree, copy them in, verify, commit.

That is not hypothetical: a session began on `master`, built ~40 untracked
files, and found the tree had been switched to someone else's feature branch
underneath it with no signal that anything had happened.

If your work is already tracked and committed, just make the worktree.

### What a worktree does NOT protect

A worktree isolates the **checkout**, not the **refs**. Both limits below were
hit within an hour of the worktrees going in, so treat them as live:

- **Ref surgery reaches into any tree.** `reset`, `rebase`, `cherry-pick` and
  `branch -f` run from anywhere move a branch even when another worktree has it
  checked out — a session watched a cherry-pick, a reset and a rebase land on
  the `master` its own worktree was on, mid-operation. The worktree lock only
  stops another tree from *checking out* that branch. **Do not do ref surgery on
  a branch you do not have checked out**, and prefer merging your own branch
  over rewriting a shared one. `./worktree.sh guard` cannot catch this: it tests
  where you are, and this damage comes from ref writes, not from location. A
  `reference-transaction` hook refusing writes to `master` from a tree that does
  not have it checked out would.

- **The index is shared too.** In the shared checkout, `git add -A` and
  `git commit -a` sweep up whatever another session has staged. One session
  watched another's `PUBLISH.md` sit staged in the shared index while it worked;
  had it committed with `-A`, it would have taken that file. **Stage by explicit
  path**, always, and check the branch as well as the diff before committing.

`./worktree.sh` never deletes a worktree or moves a ref. `status` reports stale
trees along with what would be lost, and removing one is a human decision.

## The preview server rewrites your files while it runs

The HyperFrames preview server edits composition files **in place** as it
serves them, injecting `data-hf-id` as the **first attribute on every tag** in
`index.html` and `compositions/frames/*.html`:

```html
<div data-hf-id="hf-6axv" id="root" class="clip">
```

**No generator emits this attribute.** Verified across three projects'
`build_index.py`: zero occurrences in any of them, while their generated
`index.html` files carry between 0 and 22. So `data-hf-id` in a generated file
is always injected from outside, never produced by the build — and its presence
means **that file has silently diverged from its generator.** Re-run the
generator and the attributes disappear.

204 files in this repo carry injected ids **committed**, because copies that had
been through the server were saved. That makes the attribute common, but it does
not make a divergence between a generator and its output normal, and reading it
that way costs an hour of wondering why a freshly built file does not match what
the builder emits.

Two consequences:

- **Generated composition files show as dirty for reasons unrelated to your
  edits.** Stop the preview before you diff or commit, or you cannot tell your
  own change from the server's. If a generator owns the file, re-run the
  generator and diff *that* output rather than trusting the working copy.
- **Anything matching on attribute order breaks.** A parser keyed on
  `<div id="root"` silently stopped matching once `data-hf-id` was inserted
  ahead of `id`. Match on the attribute itself (`id="root"`, a class, a
  `data-*` name) and never on it being first, or on a tag's opening byte
  sequence.

The second one is the expensive kind: it does not error, it just quietly stops
finding things, and a parser that finds nothing looks exactly like a file with
nothing in it. It crashed a storyboard parser on a file that was otherwise
perfectly valid.

**Leave a preview server running and you get both at once**: a generated file
that no longer matches its generator, and tooling that stops matching it. If a
generated file looks wrong, stop the preview and rebuild before debugging
anything else.

### Globs that abort the whole command

In zsh a glob matching nothing is a fatal error, not an empty expansion, so
`rm -rf renders/work-* raw.mp4` deletes **neither** when no work dir exists —
the command aborts before it runs. That cost two wasted 8-minute renders: a
file-existence wait returned immediately against a stale `raw.mp4`, and a
previous render was mastered and gated twice before anyone noticed. Prefer:

```bash
find renders -maxdepth 1 -name 'work-*' -exec rm -rf {} +
```

which cannot fail that way. Applies to any helper in this repo that globs paths
that may legitimately not exist.
