#!/bin/bash
# Called by "Validate Video.app" on the Desktop. Takes the script.json path
# the user picked as $1, validates it, opens the storyline report.
set -e
export PATH="/usr/local/bin:/opt/homebrew/bin:$PATH"
cd "/Users/sumitchoudhary/Desktop/Story Board"
python3 storyline.py "$1"
