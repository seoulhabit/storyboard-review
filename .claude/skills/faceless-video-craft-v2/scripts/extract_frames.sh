#!/usr/bin/env bash
# Post-render frames — ONLY what `hyperframes check` does not do.
#
# Usage: extract_frames.sh <final.mp4> <out-dir>
#
# `check` already sweeps the COMPOSITION under seek: layout, contrast on
# rendered pixels, motion-sidecar assertions, and sweep_static. What it does
# not see is the artifact that actually ships — the MUXED final, after the
# render and the audio pass. Two things live here and nowhere else:
#
#   1. frame zero and the last frame OF THE MUXED FILE (the thumbnail candidate
#      and the loop hand-back), so the check is against the deliverable rather
#      than against the composition it came from;
#   2. the Shorts safe-zone overlay, for eyeballing the reserved UI bands.
#
# The measured safe-area and static-hold gates are NOT reimplemented here. The
# repo already carries both, and [S6/A-1] says reuse before rebuild:
#
#   catalog/tooling/check-safe-area.py    hard gate; real ink in reserved zones
#   catalog/tooling/check-static-hold.py  whole-frame PSNR + region-aware hero check
#
# Wire those into the project's own package.json `postrender`, as every recent
# project in this repo already does.
set -euo pipefail

VID="${1:?usage: extract_frames.sh <final.mp4> <out-dir>}"
OUT="${2:?usage: extract_frames.sh <final.mp4> <out-dir>}"
mkdir -p "$OUT"
command -v ffmpeg  >/dev/null || { echo "ffmpeg not found";  exit 1; }
command -v ffprobe >/dev/null || { echo "ffprobe not found"; exit 1; }

# Duration MUST come from the VIDEO stream, not from format=duration. On a muxed
# file format=duration is the LONGEST stream — here the audio, which outran the
# video by 33ms. Seeking past the last video frame makes ffmpeg write nothing and
# still exit 0, so the last frame silently goes missing and `set -e` never fires.
# Confirmed on the 2026-09-01 dry run: audio 46.300s vs video 46.267s.
DUR=$(ffprobe -v error -select_streams v:0 -show_entries stream=duration -of csv=p=0 "$VID")
[ -z "$DUR" ] || [ "$DUR" = "N/A" ] && DUR=$(ffprobe -v error -select_streams v:0 \
  -show_entries stream=duration_ts,r_frame_rate -of csv=p=0 "$VID" >/dev/null 2>&1; \
  ffprobe -v error -show_entries format=duration -of csv=p=0 "$VID")
W=$(ffprobe -v error -select_streams v:0 -show_entries stream=width  -of csv=p=0 "$VID")
H=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$VID")
# Back off a comfortable two frames at 30fps, not 50ms.
LAST=$(python3 -c "print(round(max(float('$DUR') - 0.10, 0), 3))")
echo "muxed deliverable: ${W}x${H}, video ${DUR}s"

# A grab that writes no file is a hard failure, not a silent skip.
grab () {
  ffmpeg -v error -y -ss "$1" -i "$VID" -frames:v 1 "$2" </dev/null || true
  if [ ! -s "$2" ]; then echo "ERROR: no frame written at ${1}s -> $2" >&2; exit 1; fi
  echo "  $2 @ ${1}s"
}
grab 0       "$OUT/frame-000-hook.png"
grab "$LAST" "$OUT/frame-last.png"

# Shorts safe-zone overlay — vertical canvases only. Right 15% / bottom 20% /
# top 10%. This is for the eye; catalog/tooling/check-safe-area.py is the gate.
if [ "$H" -gt "$W" ]; then
  for pair in "000-hook" "last"; do
    src="$OUT/frame-${pair}.png"
    [ -f "$src" ] || continue
    ffmpeg -v error -y -i "$src" -vf \
      "drawbox=x=iw*0.85:y=0:w=iw*0.15:h=ih:color=magenta@0.35:t=fill,\
       drawbox=x=0:y=ih*0.80:w=iw:h=ih*0.20:color=magenta@0.35:t=fill,\
       drawbox=x=0:y=0:w=iw:h=ih*0.10:color=magenta@0.25:t=fill" \
      "$OUT/safe-zone-${pair}.png"
    echo "  $OUT/safe-zone-${pair}.png"
  done
fi

# Near-uniform heuristic: a blank or blown frame zero is a hook failure.
for f in "$OUT"/frame-*.png; do
  mean=$(ffprobe -v error -f lavfi -i "movie=$f,signalstats" \
         -show_entries frame_tags=lavfi.signalstats.YAVG -of csv=p=0 | head -1)
  [ -n "${mean:-}" ] && awk -v m="$mean" -v f="$f" \
    'BEGIN{ if (m < 8 || m > 247) print "  WARN near-uniform frame (YAVG=" m "): " f }'
done

echo "done — look at every frame. The manifest is not the proof, the pixels are."
