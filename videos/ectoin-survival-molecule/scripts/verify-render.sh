#!/usr/bin/env bash
# One pass over a finished render. Run from the project dir
# (videos/ectoin-survival-molecule).
#
# setopt -- an unmatched glob is a FATAL error in zsh, which has silently
# skipped cleanup and caused double-renders in this repo before. bash +
# nullglob here, per this project's CLAUDE.md.
set -uo pipefail
shopt -s nullglob 2>/dev/null || true

RAW="${1:-renders/ectoin-survival-molecule_v2_final.mp4}"
T="../../catalog/tooling"

echo "=== 1. safe-area (HARD GATE) ==="
python3 scripts/check-safe-area.py . "$RAW" --landscape

echo
echo "=== 2. cadence (--longform) ==="
python3 scripts/check-cadence.py . "$RAW" --longform 2>&1 | head -24

echo
echo "=== 3. static-hold (--landscape) ==="
python3 scripts/check-static-hold.py . "$RAW" --landscape 2>&1 | tail -14

echo
echo "=== 4. continuity audit (source-structural, --gate) ==="
python3 "$T/continuity-audit.py" . --gate 2>&1 | sed -n '/VERDICT/,$p' | head -10

echo
echo "=== 5. check-seams (--render) ==="
python3 scripts/check-seams.py . --render "$RAW"

echo
echo "=== 6. sfx durations ==="
python3 scripts/check-sfx-durations.py . 2>&1 | tail -20
