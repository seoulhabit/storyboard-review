#!/usr/bin/env bash
# Per-session git worktrees for this repo.
#
# WHY THIS EXISTS
# ---------------
# Several Claude sessions work this repo at once. When they share one checked-out
# working tree, one session's checkout/reset/merge moves state under another mid-
# operation. On 2026-09-02/03 that cost, in one evening:
#
#   - two commits orphaned by a `reset --hard` to origin/master
#   - an uncommitted HANDBACK.md destroyed by a merge checkout
#   - two separate sessions' commits landing on a feature branch they did not
#     intend, because the shared tree was switched out from under them
#
# None of those were tool bugs and none were caught by checking git status first:
# the damage happens in the gap between "check state" and "act on state".
# Separate worktrees remove the gap by not sharing the tree at all. History stays
# shared; the checkout does not.
#
# USAGE
#   ./worktree.sh status          what every tree is on, and what is at risk
#   ./worktree.sh new <name>      create an isolated worktree off origin/master
#   ./worktree.sh guard           exit 1 if run from the shared tree (for hooks)
#
# `guard` tests your CURRENT WORKING DIRECTORY, not where this script lives.
# Invoking a worktree's copy while cd'd to the shared tree correctly reports the
# shared tree; that is right for hook use, where cwd is what matters, but it
# reads as a false positive if you expect it to check the script's own path.
#
# This script never deletes a worktree or moves a ref. Stale trees are reported
# with what would be lost; removing them is a human decision.

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WT_DIR="$ROOT/.claude/worktrees"          # already in .git/info/exclude
_common="$(git -C "$ROOT" rev-parse --path-format=absolute --git-common-dir 2>/dev/null)"
MAIN="$(dirname "$_common")"

c_red=$'\033[31m'; c_yel=$'\033[33m'; c_grn=$'\033[32m'; c_dim=$'\033[2m'; c_off=$'\033[0m'

die() { echo "${c_red}error:${c_off} $*" >&2; exit 2; }

git -C "$ROOT" rev-parse --git-dir >/dev/null 2>&1 || die "not a git repo: $ROOT"

# Divergence from origin is invisible to `git status`, and it is where work is
# actually lost: an unpushed commit on a branch someone later resets is gone with
# no reflog entry its author can find. Tonight master sat 2-ahead/2-behind
# unnoticed, on a branch that had been reset --hard twice. Seeing it took an
# explicit rev-list, so status runs it for every tree.
_ahead_behind() {
  local dir="$1" br="$2" pad="$3" counts a b
  if [ "$br" = "HEAD" ] || [ -z "$br" ]; then return 0; fi
  if ! git -C "$dir" rev-parse --verify -q "refs/remotes/origin/$br" >/dev/null 2>&1; then
    local unmerged; unmerged="$(git -C "$dir" rev-list --count master.."$br" 2>/dev/null || echo 0)"
    if [ "${unmerged:-0}" -gt 0 ]; then
      echo "${pad}${c_yel}!${c_off} no origin/$br, and $unmerged commit(s) not on master —"
      echo "${pad}  they exist ONLY in this worktree. Merge or push before anyone removes it."
    else
      echo "${pad}${c_dim}local-only branch, nothing ahead of master${c_off}"
    fi
    return 0
  fi
  counts="$(git -C "$dir" rev-list --left-right --count "origin/$br...$br" 2>/dev/null)" || return 0
  b="${counts%%	*}"; a="${counts##*	}"
  [ "${a:-0}" = 0 ] && [ "${b:-0}" = 0 ] && { echo "${pad}${c_dim}in sync with origin/$br${c_off}"; return 0; }
  echo "${pad}${c_yel}!${c_off} $a ahead / $b behind origin/$br"
  [ "${a:-0}" -gt 0 ] && echo "${pad}  $a unpushed commit(s) — a reset of this branch orphans them"
  [ "${b:-0}" -gt 0 ] && echo "${pad}  $b behind — pull before committing or you diverge further"
  return 0
}

# A stale copy of this script is most likely to be run by exactly the people it
# is for: the shared tree sits on a feature branch that predates these fixes, so
# `./worktree.sh` there is an older version -- LFS wall, no divergence check.
# Compare the running file against origin's blob and say so.
#
# Bootstrapping limit, stated rather than hidden: a copy older than this check
# cannot perform it. This protects future drift, not the drift that already
# exists. It also reads the LOCAL origin/master ref, so it is as fresh as your
# last fetch.
_self_check() {
  local mine theirs
  mine="$(git -C "$ROOT" hash-object "${BASH_SOURCE[0]}" 2>/dev/null)" || return 0
  theirs="$(git -C "$ROOT" rev-parse -q --verify origin/master:worktree.sh 2>/dev/null)" || return 0
  [ -z "$theirs" ] && return 0
  if [ "$mine" != "$theirs" ]; then
    echo
    echo "  ${c_yel}!${c_off} this copy of worktree.sh differs from origin/master's."
    echo "    Running: ${BASH_SOURCE[0]}"
    echo "    If it is older you may be missing fixes. Compare with:"
    echo "      git show origin/master:worktree.sh | diff - \"${BASH_SOURCE[0]}\""
  fi
  return 0
}

# Untracked work is the most exposed thing in any tree and was invisible here:
# `uncommitted` counts TRACKED changes only, so a session building a new video
# project -- 274 files, 149M in the case that surfaced this -- read as
# "uncommitted 0" and therefore safe, while having neither reflog nor stash to
# fall back on. A checker that reports clean without measuring the thing most at
# risk is the failure this whole script exists to answer, so it was worth fixing
# in the script itself rather than only in the guidance.
#
# -uall counts files rather than collapsed directories: one `??` line can hide
# hundreds of files, which is exactly how 274 of them read as a single entry.
_untracked() {
  local n
  n="$(git -C "$1" status --porcelain -uall 2>/dev/null | grep -c '^??')" || true
  echo "${n:-0}"
}

_untracked_warn() {
  local n="$1" pad="$2"
  [ "${n:-0}" -gt 0 ] || return 0
  echo "${pad}${c_yel}!${c_off} $n untracked file(s) — no reflog, no stash, no recovery."
  echo "${pad}  A stray 'git clean' or checkout takes them silently. Copy them"
  echo "${pad}  OUT of the repo before any git operation, then commit them somewhere."
  return 0
}

# ---------------------------------------------------------------- status

cmd_status() {
  local shared_branch dirty ahead
  echo
  echo "  SHARED TREE  $MAIN"
  shared_branch="$(git -C "$MAIN" rev-parse --abbrev-ref HEAD)"
  dirty="$(git -C "$MAIN" status --porcelain | grep -vc '^??' || true)"
  local untr; untr="$(_untracked "$MAIN")"
  printf '    branch %s   uncommitted %s   untracked %s\n' "$shared_branch" "$dirty" "$untr"
  _untracked_warn "$untr" "    "
  _ahead_behind "$MAIN" "$shared_branch" "    "
  if [ "$shared_branch" != "master" ]; then
    echo "    ${c_yel}!${c_off} shared tree is NOT on master. Any session committing here"
    echo "      right now lands on '$shared_branch' without meaning to."
  fi
  if [ "$dirty" -gt 0 ]; then
    echo "    ${c_yel}!${c_off} $dirty uncommitted tracked file(s) — a checkout or reset by"
    echo "      another session takes these with no reflog entry."
  fi

  echo
  echo "  WORKTREES"
  local any=0
  while IFS= read -r line; do
    local path br
    path="$line"
    [ "$path" = "$MAIN" ] && continue
    any=1
    br="$(git -C "$path" rev-parse --abbrev-ref HEAD 2>/dev/null || echo '?')"
    dirty="$(git -C "$path" status --porcelain 2>/dev/null | grep -vc '^??' || true)"
    ahead="$(git -C "$path" log --oneline master.."$br" 2>/dev/null | wc -l | tr -d ' ')"
    local age; age="$(git -C "$path" log -1 --format='%cr' 2>/dev/null || echo '?')"
    printf '    %-30s %-38s\n' "$(basename "$path")" "$br"
    local untr; untr="$(_untracked "$path")"
    printf '      %slast commit %s   unmerged %s   uncommitted %s   untracked %s%s\n' \
           "$c_dim" "$age" "$ahead" "$dirty" "$untr" "$c_off"
    _untracked_warn "$untr" "      "
    _ahead_behind "$path" "$br" "      "
    if [ "$ahead" -gt 0 ] || [ "$dirty" -gt 0 ]; then
      echo "      ${c_yel}holds work not on master — do not remove without reading it${c_off}"
    else
      echo "      ${c_grn}fully merged and clean — safe to remove${c_off}"
    fi
  done < <(git -C "$ROOT" worktree list --porcelain | sed -n 's/^worktree //p')
  [ "$any" = 0 ] && echo "    ${c_dim}(none)${c_off}"
  echo
}

# ---------------------------------------------------------------- new

cmd_new() {
  local name="${1:-}"
  [ -n "$name" ] || die "usage: ./worktree.sh new <name>"
  [[ "$name" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || die "name must be alnum/._- : $name"

  local br="session/$name" path="$WT_DIR/$name"
  [ -e "$path" ] && die "already exists: $path"
  git -C "$ROOT" show-ref --verify --quiet "refs/heads/$br" && die "branch exists: $br"

  git -C "$ROOT" fetch -q origin 2>/dev/null || true
  local base; base="$(git -C "$ROOT" rev-parse --verify -q origin/master || git -C "$ROOT" rev-parse master)"

  mkdir -p "$WT_DIR"
  # git-lfs prints a long "Encountered N files that should have been pointers"
  # block here for blobs predating .gitattributes. It is pre-existing, it is not
  # an error, and printed raw it buries the success message -- a session read it
  # as a failure and nearly backed out of a step that had worked. Capture, then
  # summarise.
  local out
  if ! out="$(git -C "$ROOT" worktree add -q -b "$br" "$path" "$base" 2>&1)"; then
    echo "$out" >&2
    die "worktree add failed"
  fi
  local lfs_n
  lfs_n="$(grep -c "should have been pointers" <<<"$out" || true)"

  echo
  if [ "${lfs_n:-0}" -gt 0 ]; then
    echo "  ${c_dim}(git-lfs pointer warning suppressed — pre-existing, not an error)${c_off}"
  fi
  echo "  ${c_grn}created${c_off}  $path"
  echo "  branch   $br  (from $(git -C "$ROOT" rev-parse --short "$base"))"
  echo
  echo "  Work here instead of the shared tree:"
  echo "    cd \"$path\""
  echo
  echo "  When done, merge back with a normal PR or:"
  echo "    git -C \"$MAIN\" merge --no-ff $br"
  echo
}

# ---------------------------------------------------------------- guard

cmd_guard() {
  local here; here="$(git rev-parse --path-format=absolute --show-toplevel 2>/dev/null)"
  if [ "$here" = "$MAIN" ]; then
    echo "${c_red}guard:${c_off} you are in the SHARED tree ($MAIN)." >&2
    echo "  Other sessions can move this checkout under you. Use:" >&2
    echo "    ./worktree.sh new <your-session-name>" >&2
    return 1
  fi
  echo "${c_grn}guard:${c_off} isolated worktree ($here) — safe."
  return 0
}

# _self_check runs for `new` as well as `status`, because `new` is the command
# the people most likely to hold a stale copy actually run. The check's own
# comment says a stale copy "is most likely to be run by exactly the people it
# is for" -- and those people are mid-migration, so they type `new`, not
# `status`. Wiring it only to `status` put the warning on the one path that
# audience had no reason to take.
#
# Deliberately NOT wired to `guard`: guard is documented as hook-usable, its
# contract is an exit code, and a hook that starts emitting an extra paragraph
# on every invocation is a hook someone silences. Its answer -- am I in the
# shared tree -- also barely depends on script version.
case "${1:-status}" in
  status) _self_check; cmd_status ;;
  new)    _self_check; shift; cmd_new "$@" ;;
  guard)  cmd_guard ;;
  *)      die "unknown command: $1 (status | new <name> | guard)" ;;
esac
