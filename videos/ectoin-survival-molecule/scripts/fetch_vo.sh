#!/bin/bash
# fetch_vo.sh <index> <url>  -- download a VO take and report its measured duration
cd "$(dirname "$0")/.." || exit 1
n=$(printf "%02d" "$1")
curl -sS -o "assets/voice/${n}.wav" "$2" || exit 1
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "assets/voice/${n}.wav")
printf "  %s.wav  %6.3fs\n" "$n" "$d"
