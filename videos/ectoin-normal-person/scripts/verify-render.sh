#!/usr/bin/env bash
# One pass over a finished render. Run from the project dir.
#
# setopt -- an unmatched glob is a FATAL error in zsh, which silently aborted
# a render launch twice on this project (`rm -rf renders/work-*` with no work
# dir present killed the whole command line, and a racy pgrep then reported
# "RENDERING" for a process that had never started). bash + nullglob here.
set -uo pipefail
shopt -s nullglob 2>/dev/null || true

RAW="${1:-renders/ectoin-normal-person.raw.mp4}"
T="../../catalog/tooling"

echo "=== 1. safe-area (HARD GATE, streaming to survive memory pressure) ==="
python3 /tmp/sa_stream.py "$RAW" || true

echo
echo "=== 2. cadence (--longform) ==="
python3 "$T/check-cadence.py" . "$RAW" --longform 2>&1 | head -24

echo
echo "=== 3. static-hold (--landscape) ==="
python3 "$T/check-static-hold.py" . "$RAW" --landscape 2>&1 | tail -14

echo
echo "=== 4. continuity audit (source-structural) ==="
python3 "$T/continuity-audit.py" . 2>&1 | sed -n '/VERDICT/,$p' | head -10
