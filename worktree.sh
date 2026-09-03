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

# ---------------------------------------------------------------- status

cmd_status() {
  local shared_branch dirty ahead
  echo
  echo "  SHARED TREE  $MAIN"
  shared_branch="$(git -C "$MAIN" rev-parse --abbrev-ref HEAD)"
  dirty="$(git -C "$MAIN" status --porcelain | grep -vc '^??' || true)"
  printf '    branch %s   uncommitted %s\n' "$shared_branch" "$dirty"
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
    printf '      %slast commit %s   unmerged %s   uncommitted %s%s\n' \
           "$c_dim" "$age" "$ahead" "$dirty" "$c_off"
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
  git -C "$ROOT" worktree add -q -b "$br" "$path" "$base" || die "worktree add failed"

  echo
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

case "${1:-status}" in
  status) cmd_status ;;
  new)    shift; cmd_new "$@" ;;
  guard)  cmd_guard ;;
  *)      die "unknown command: $1 (status | new <name> | guard)" ;;
esac
