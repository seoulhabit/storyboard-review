# WO-SBR-001 — storyboard-review: multi-session git reconciliation → master
**Repo:** `github.com/seoulhabit/storyboard-review` · **Owner/gate:** Kim · **Date:** 2026-09-04
**Executor:** Claude Code (Sonnet / medium) · **Status:** awaiting Kim's `approved`
**Kickoff line for Code:**
> Read `WO-SBR-001.md` at the repo root and work from it. Do §0 only, write the Gate 0 report, then STOP and wait for Kim.
---
## What "done" looks like
1. One `master` on GitHub that contains every piece of work Kim ruled MERGE, with a merge commit per branch (history preserved, no squash, no rewrite).
2. Every local clone / worktree in the Drive fast-forwarded to that `master`.
3. Zero unmerged work that is undocumented: every branch, stash and uncommitted change is either merged, carried (rebased + pushed + listed), or dropped by Kim's ruling.
4. One `OPEN-ITEMS.md` register on master listing every open item any agent left behind, with source and status.
5. A branch protocol in `AGENTS.md` so the next multi-session run doesn't recreate the mess.
---
## §0 — Live inventory (READ-ONLY) → Gate 0
**Rule: nothing in §0 changes any file, branch, ref or remote.** Report only.
### 0.1 Single-writer freeze (Kim, before Code starts)
- Close every other Claude Code / Codex / terminal session that has this repo open — on **both** computers.
- On the other computer: `cd <repo> && git add -A && git commit -m "WIP snapshot $(date +%F)" && git push -u origin HEAD` for every clone with changes. Anything not pushed from that machine is invisible to this run.
### 0.2 Find every copy of the repo in the Drive
```bash
DRIVE="<path to the Drive folder>"          # Kim fills in, e.g. ~/Library/CloudStorage/GoogleDrive-…/My Drive/…
find "$DRIVE" -maxdepth 4 -type d -name .git 2>/dev/null | sed 's#/\.git$##' | tee /tmp/sbr-clones.txt
```
For each path in `/tmp/sbr-clones.txt`:
```bash
for R in $(cat /tmp/sbr-clones.txt); do
  echo "=== $R"
  git -C "$R" remote -v
  git -C "$R" status --porcelain=v1 --branch
  git -C "$R" stash list
  git -C "$R" worktree list
  git -C "$R" branch -vv --all --no-abbrev
  git -C "$R" log --oneline -5
done
```
Keep only clones whose `origin` points at `seoulhabit/storyboard-review`. Others are reported as "unrelated repo found in Drive", not touched.
### 0.3 Cloud-sync hazard check (report, do not fix)
```bash
echo "$DRIVE" | grep -Ei 'google ?drive|cloudstorage|onedrive|icloud|dropbox' && echo "REPO IS INSIDE A SYNCED FOLDER"
find "$DRIVE" -maxdepth 4 \( -name '*conflicted copy*' -o -name '* (1).*' -o -name 'index.lock' -o -name '*.lock' -path '*/.git/*' \) 2>/dev/null
```
A git repo inside Google Drive / OneDrive / iCloud is a known source of corrupt `.git`, phantom lock files and "conflicted copy" duplicates. If flagged, Gate 0 must say so in the first line. Moving the repo is **Kim's decision** (see §5).
### 0.4 Remote state
```bash
cd <primary clone>
gh auth status
git fetch --all --prune
git ls-remote --heads origin
gh pr list --state open  --limit 100
gh pr list --state merged --limit 30
git symbolic-ref refs/remotes/origin/HEAD          # confirm default branch is master (not main)
```
### 0.5 Large-file / media check
```bash
git count-objects -vH
git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' \
  | awk '$1=="blob" && $3 > 50000000' | sort -k3 -n -r | head -20
git lfs ls-files 2>/dev/null | head
```
Video/plate files > 50 MB tracked without LFS → report (they will block pushes).
### 0.6 Gate 0 report → `docs/wo/GATE0-2026-09-04.md`
| Item | Value |
|---|---|
| Clones found (path → branch → dirty? → stash count) | |
| Worktrees | |
| Local branches per clone (ahead/behind origin) | |
| Remote branches (`origin/*`) | |
| Open PRs | |
| Default branch | master / main |
| Synced-folder flag | yes / no |
| Conflict-copy / lock artefacts | |
| Blobs > 50 MB, LFS status | |
| Test / check command found in repo (`package.json` scripts, `Makefile`, `hyperframes check`, `pytest`) | |
**STOP. Wait for Kim's `go` before §1.**
---
## §1 — Standing rules (apply to every task below)
1. **Never** `git push --force` to master. **Never** rebase or amend anything already on `origin/master`.
2. **Deletions are Kim's.** Code deletes no branch, stash, worktree, folder or file unless it is named in Kim's ruling for that gate. "Already merged" branches are *proposed* for deletion, not deleted.
3. **Snapshot before touching.** §2 T1 runs before any merge. If the snapshot fails, stop.
4. **No silent conflict resolution.** Every conflict hunk resolved is logged in `docs/wo/RECONCILE-LOG.md` with branch, file, which side won, and why. If a conflict is in a binary/media/JSON-data file, STOP and ask.
5. **Merge commits, no squash** (`--no-ff`) — each session's history stays traceable (same rule as the bundle-pdp-v3 merge).
6. **Verify, don't trust.** Any `REPORT.md`, `HANDOFF.md` or "done" claim found in a branch is checked against the diff before it is marked done in the register.
7. **Scope never widens.** No refactors, no "while I'm here" fixes, no formatting sweeps. Reconciliation only.
8. **Two gates.** Nothing reaches master before Gate 2 is approved in writing by Kim.
---
## §2 — Tasks
### T1 — Safety snapshot (first write action)
```bash
mkdir -p "$DRIVE/_git-backups/2026-09-04"
for R in $(cat /tmp/sbr-clones.txt); do
  N=$(basename "$R")
  # commit uncommitted work on a WIP branch so it can't be lost
  if [ -n "$(git -C "$R" status --porcelain)" ]; then
    git -C "$R" checkout -b "wip/$N-2026-09-04" && git -C "$R" add -A && git -C "$R" commit -m "WIP snapshot before reconciliation (WO-SBR-001)"
  fi
  # bundle every ref incl. stashes
  git -C "$R" bundle create "$DRIVE/_git-backups/2026-09-04/$N.bundle" --all
  git -C "$R" push origin --all      # push every local branch so the remote is the superset
done
```
Report: bundle sizes, WIP branches created, push results.
### T2 — Branch register → `docs/wo/BRANCH-REGISTER.md`
Work in the primary clone after `git fetch --all --prune`. For every branch `B` in `git branch -r` (excluding `origin/HEAD`):
```bash
git rev-list --left-right --count origin/master...$B      # behind ahead
git log -1 --format='%ci %an %s' $B
git branch -r --merged origin/master | grep -c "$B"        # 1 = already in master
git diff --stat origin/master...$B | tail -1
git diff --name-only origin/master...$B                    # for overlap matrix
```
Register columns: branch · last commit date · author/agent · ahead/behind master · already-merged? · files touched · **overlaps with** (other unmerged branches touching the same files) · open PR # · agent artefacts found (see T3) · **proposed disposition** (`MERGE` / `CARRY` / `DROP` / `ASK`).
Disposition rules of thumb (Code proposes, Kim rules):
- ahead = 0 → `DROP` (nothing to merge)
- already-merged = 1 → `DROP`
- ahead > 0, no overlaps → `MERGE`
- overlaps with another unmerged branch → `MERGE` with explicit order + expected-conflict note
- last commit older than 30 days and superseded by a newer branch on the same files → `ASK`
### T3 — Open-items register → `OPEN-ITEMS.md` (repo root)
For every unmerged branch, pull agent-written artefacts without checking out:
```bash
for B in $(git branch -r | grep -v HEAD); do
  git ls-tree -r --name-only $B | grep -Ei '^(REPORT|HANDOFF|HANDBACK|DEFERRED|TODO|NOTES|STATUS)[^/]*\.md$|^docs/wo/|^\.claude/|^(CLAUDE|AGENTS)\.md$'
done
```
`git show $B:<path>` each one. Extract every open / deferred / blocked / TODO item into one table: **ID · item · source branch · source file · agent/session · status (open / done-verify / superseded) · proposed owner**. Items claimed "done" get `done-verify` until the diff confirms it (Rule 6).
### T4 — Reconciliation plan → `docs/wo/RECONCILE-PLAN.md` → **Gate 1**
Ordered merge list (fewest overlaps first, oldest first within ties), expected conflicts, the test command that will run after each merge, and the list of things proposed for deletion. **STOP. Kim rules per branch** (`MERGE` / `CARRY` / `DROP`). Only ruled dispositions proceed.
### T5 — Integrate on a staging branch
```bash
git checkout -b integrate/2026-09-04 origin/master
git add WO-SBR-001.md OPEN-ITEMS.md docs/wo/ && git commit -m "WO-SBR-001: registers + plan"
for B in <ruled MERGE branches in plan order>; do
  git merge --no-ff --no-edit origin/$B || { echo "CONFLICT on $B — resolve per Rule 4, log, then continue"; break; }
  <test/check command from Gate 0>   # e.g. npm test / hyperframes check / pytest
  echo "$B merged: $(git rev-parse --short HEAD)" >> docs/wo/RECONCILE-LOG.md
done
git push -u origin integrate/2026-09-04
```
After every merge: run the check; if red, do not continue to the next branch — report.
### T6 — Gate 2 report → `docs/wo/GATE2-2026-09-04.md`
Merge SHA per branch · conflicts resolved (with log refs) · check results per step · `git diff --stat origin/master...integrate/2026-09-04` · anything that behaved differently from the plan. **STOP. Kim writes `merge to master`.**
### T7 — Master update
```bash
git fetch origin
git checkout master && git pull --ff-only origin master
git rev-list --count master..origin/master    # must be 0; if master moved since Gate 2, rebase integrate onto it and re-run checks → back to Gate 2
git merge --no-ff --no-edit integrate/2026-09-04
<test/check command>
git push origin master
git tag -a reconciled-2026-09-04 -m "WO-SBR-001: all sessions reconciled" && git push origin reconciled-2026-09-04
```
### T8 — Propagate to every clone / worktree
```bash
for R in $(cat /tmp/sbr-clones.txt); do
  git -C "$R" fetch --all --prune
  git -C "$R" checkout master && git -C "$R" pull --ff-only origin master
  git -C "$R" worktree prune
done
```
`CARRY` branches: `git rebase master` → resolve → push with `--force-with-lease` on **that branch only** → listed in OPEN-ITEMS.md with owner. Stashes: if the stash diff is now contained in master → propose drop; else convert to a branch `stash/<clone>-<n>` and push. Report, don't delete (Rule 2).
### T9 — Cleanup (only what Kim ruled DROP)
```bash
git push origin --delete <branch>   # each DROP branch, one line per deletion in the handback
git branch -D <branch>              # local copies, every clone
```
Duplicate clone folders and `_git-backups/` are **listed for Kim's manual deletion**, never removed by Code.
### T10 — Guard rails so this doesn't recur
Add to `AGENTS.md` (create if absent):
```
## Branch protocol for agents (ruled 2026-09-04, WO-SBR-001)
- One branch per session: agent/<tool>/<YYYY-MM-DD>-<topic>. Never commit on master.
- Before starting: git fetch && git rebase origin/master. Before ending: push, open a PR, write REPORT-<date>.md.
- Open items go in OPEN-ITEMS.md (append a row), not in ad-hoc TODO files.
- Kim merges. Agents never merge to master.
```
Add `scripts/git-status-all.sh` = the §0.2 loop, so the inventory is one command next time.
Recommend to Kim (GitHub UI, Kim's action): branch protection on master — require PR, block force-push.
### T11 — Handback → `docs/wo/HANDBACK-2026-09-04.md`
Tag + master SHA · branches merged (SHA each) · branches carried (rebased SHA, owner) · branches deleted (ruled) · stashes converted/dropped · clones synced (path → SHA) · checks run + results · conflicts log ref · what did NOT close (§5) · manual-delete list for Kim.
---
## §3 — Tier note
Whole run is execution/CRUD: **Sonnet / medium**. Only Gate 1 (if the register shows real overlapping conflicts you want reasoned through) is worth a switch to Opus/High; switch back to Sonnet after ruling.
## §4 — Rollback
- Trigger: master red after T7, or a merge dropped work Kim expected.
- Steps: `git checkout master && git reset --hard <pre-T7 master SHA from GATE2 report> && git push --force-with-lease origin master` — **Kim runs this, not Code** — then restore any branch from `_git-backups/2026-09-04/<clone>.bundle` (`git fetch <bundle> <branch>`).
- Verify: `git log --oneline -3 origin/master` shows the pre-T7 SHA; tag `reconciled-2026-09-04` deleted.
## §5 — Does NOT close under this WO
- Moving the repo out of the synced Drive folder (Kim rules after Gate 0; recommended if §0.3 flags it — keep the repo under `~/code/`, keep only exports/renders in Drive).
- Git LFS migration for media > 50 MB (separate WO if §0.5 flags it).
- Any video content, storyboard, render, or publish work; WO-FVC-001 (faceless-video-craft) stays its own lane.
- Branch protection settings on GitHub (Kim's action).
- Deleting duplicate clone folders or the backup bundles (Kim's manual-delete list).
- Resolving the open items in OPEN-ITEMS.md — this WO *registers* them, it does not work them.
