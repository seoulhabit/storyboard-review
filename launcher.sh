#!/bin/bash
# Called by "New Storyboard.app" on the Desktop. Takes the folder the user
# picked as $1, builds a board from it, refreshes the landing page, opens it.
set -e
export PATH="/usr/local/bin:/opt/homebrew/bin:$PATH"
cd "/Users/sumitchoudhary/Desktop/Story Board"

folder="$1"
name=$(basename "$folder")
out="storyboard_${name}.html"

python3 storyboard.py "$folder" -o "$out"
python3 storyboard.py --index
open "$out"
