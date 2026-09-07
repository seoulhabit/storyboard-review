#!/usr/bin/env bash
# Local mirror of .github/workflows/ci.yml, for when GitHub Actions itself
# can't be trusted for signal (this repo's CI has been failing at the
# runner-provisioning level -- every job's own step list empty -- on both
# master and every PR, independent of the diff being tested).
#
# Runs the exact same four steps the workflow does, in the same order,
# against every Python version the workflow's matrix names that is
# actually installed on this machine:
#
#   pip install -e ".[dev]"  ->  ruff check .  ->  mypy  ->  pytest -q
#
# This mirrors the workflow's python-version axis (3.9, 3.12). It cannot
# mirror the OS axis (ubuntu, windows) without a VM or Docker per OS, which
# is out of scope for a local script -- named here rather than silently
# pretending this is the full matrix. (macos-latest was dropped from
# ci.yml's own matrix -- its 10x Actions-minute billing multiplier was the
# single biggest driver of a private-repo month's included minutes.)
#
# Each Python version gets its own throwaway venv under .ci-local/, never
# the developer's own .venv/, so this never disturbs an interactive
# environment. Venvs are reused across runs (fast) unless --clean wipes
# them first.
#
# Usage:
#   ./ci-local.sh                 # both 3.9 and 3.12, whichever are found
#   ./ci-local.sh 3.12            # just one version
#   ./ci-local.sh --clean         # wipe .ci-local/ first, then run both
#   ./ci-local.sh --clean 3.9
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

CI_DIR="$REPO_ROOT/.ci-local"
VERSIONS=(3.9 3.12)   # must match .github/workflows/ci.yml's matrix.python-version
CLEAN=false
REQUESTED=()

for arg in "$@"; do
  case "$arg" in
    --clean) CLEAN=true ;;
    -h|--help)
      sed -n '2,29p' "$0"
      exit 0
      ;;
    *) REQUESTED+=("$arg") ;;
  esac
done
if [ "${#REQUESTED[@]}" -gt 0 ]; then
  VERSIONS=("${REQUESTED[@]}")
fi

if [ "$CLEAN" = true ]; then
  find "$CI_DIR" -maxdepth 1 -mindepth 1 -exec rm -rf {} + 2>/dev/null || true
fi
mkdir -p "$CI_DIR"

c_red=$'\033[31m'; c_grn=$'\033[32m'; c_yel=$'\033[33m'; c_dim=$'\033[2m'; c_off=$'\033[0m'

declare -a RESULT_LINES=()
OVERALL_OK=true

run_step() {
  local label="$1"; shift
  echo "${c_dim}\$ $*${c_off}"
  if "$@"; then
    echo "${c_grn}✓${c_off} $label"
    return 0
  else
    echo "${c_red}✗${c_off} $label"
    return 1
  fi
}

for ver in "${VERSIONS[@]}"; do
  echo
  echo "══════════ Python $ver ══════════"

  PYBIN=""
  for candidate in "python$ver" "python${ver%%.*}.${ver##*.}"; do
    if command -v "$candidate" >/dev/null 2>&1; then
      PYBIN="$candidate"
      break
    fi
  done
  if [ -z "$PYBIN" ]; then
    echo "${c_yel}⚠${c_off}  python$ver not found on PATH -- skipping (install it, or pass only the versions you have)"
    RESULT_LINES+=("$ver | ${c_yel}SKIPPED${c_off} (interpreter not found)")
    continue
  fi

  VENV="$CI_DIR/venv-$ver"
  if [ ! -d "$VENV" ]; then
    echo "creating venv: $VENV ($("$PYBIN" --version 2>&1))"
    "$PYBIN" -m venv "$VENV"
    # A fresh venv's bundled pip can be too old to editable-install a
    # pyproject.toml-only project (no setup.py): PEP 660 editable installs
    # need pip >= 21.3. Confirmed on this machine's python3.9 venv, which
    # ensurepip seeds at pip 20.2.3 -- "editable mode currently requires a
    # setup.py based build" is that old-pip error, not a real packaging
    # problem with this project. Upgrade once, at venv-creation time, not
    # on every run.
    "$VENV/bin/python" -m pip install -q --upgrade pip
  fi
  VPY="$VENV/bin/python"

  STEP_OK=true

  if ! run_step "install (pip install -e .[dev])" "$VPY" -m pip install -q -e ".[dev]"; then
    STEP_OK=false
  fi

  if [ "$STEP_OK" = true ]; then
    if ! run_step "lint (ruff check .)" "$VPY" -m ruff check .; then
      STEP_OK=false
    fi
  fi

  if [ "$STEP_OK" = true ]; then
    if ! run_step "typecheck (mypy)" "$VPY" -m mypy; then
      STEP_OK=false
    fi
  fi

  if [ "$STEP_OK" = true ]; then
    if ! run_step "test (pytest -q)" "$VPY" -m pytest -q; then
      STEP_OK=false
    fi
  fi

  if [ "$STEP_OK" = true ]; then
    RESULT_LINES+=("$ver | ${c_grn}PASS${c_off}")
  else
    RESULT_LINES+=("$ver | ${c_red}FAIL${c_off}")
    OVERALL_OK=false
  fi
done

echo
echo "══════════ summary ══════════"
echo "(mirrors ci.yml's python-version axis only -- not the ubuntu/windows OS matrix)"
for line in "${RESULT_LINES[@]}"; do
  echo -e "  $line"
done

if [ "$OVERALL_OK" = true ]; then
  echo "${c_grn}all local CI steps passed${c_off}"
  exit 0
else
  echo "${c_red}one or more local CI steps failed${c_off}"
  exit 1
fi
