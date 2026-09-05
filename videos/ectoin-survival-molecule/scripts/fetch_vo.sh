#!/bin/bash
# fetch_vo.sh <index> <url>  -- download a VO take and report its measured duration
cd "$(dirname "$0")/.." || exit 1
n=$(printf "%02d" "$1")
# CloudFront rejects curl's default user agent with a 403 on these result URLs.
# The failure is silent with -sS -o: you get a 403 body written to the .wav and
# an ffprobe error two steps later, so the UA is not optional.
curl -sSL -A "Mozilla/5.0" -o "assets/voice/${n}.wav" "$2" || exit 1
case "$(head -c 4 "assets/voice/${n}.wav")" in
  RIFF) ;;
  *) echo "  NOT a WAV -- the download returned an error page, not audio" >&2; exit 1 ;;
esac
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "assets/voice/${n}.wav")
printf "  %s.wav  %6.3fs\n" "$n" "$d"
