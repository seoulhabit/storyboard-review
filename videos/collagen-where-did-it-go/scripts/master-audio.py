#!/usr/bin/env python3
"""Two-pass EBU R128 master, then RE-MEASURE THE SHIPPED FILE.

    python3 scripts/master-audio.py . renders/ectoin-full.mp4 renders/<out>.mp4

Targets -14 LUFS integrated (YouTube normalises louder material down anyway).

TP=-2.5, NOT -1.5. AAC encoding raises intersample true peak: a file measured at
-1.50 dBTP on the PCM intermediate has shipped at +0.5 dBFS. The margin is there
so the DELIVERED file lands under -1.0. The video stream is copied through
untouched, and the measurement that counts is taken by decoding the finished MP4
back -- a number from the intermediate is not evidence about the deliverable.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

I, TP, LRA = -14.0, -2.5, 11.0


def measure(path):
    """Read the SUMMARY block only.

    ebur128 prints a per-frame `I:` line for the whole file before the summary,
    so a bare `re.search(r"I:")` returns an early momentary value -- it reported
    -70.0 LUFS (the silence before the first word) for a file that was actually
    fine. Anchor on the Summary section instead.
    """
    err = subprocess.run(["ffmpeg", "-nostdin", "-i", str(path), "-af",
                          "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    tail = err[err.rindex("Summary:"):] if "Summary:" in err else err
    i = float(re.search(r"I:\s*(-?[\d.]+)\s*LUFS", tail).group(1))
    tp = float(re.search(r"Peak:\s*(-?[\d.]+)\s*dBFS", tail).group(1))
    return i, tp


def main():
    root, src, dst = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])

    print("  pass 1 — analysing…")
    err = subprocess.run(
        ["ffmpeg", "-nostdin", "-i", str(src), "-af",
         f"loudnorm=I={I}:TP={TP}:LRA={LRA}:print_format=json", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    m = json.loads(re.search(r"\{[^{}]*\}", err[err.rindex("{") - 1:]).group(0)) \
        if "{" in err else None
    if m is None:
        print("  could not parse loudnorm JSON"); return 1

    print(f"    measured I={m['input_i']} LUFS, TP={m['input_tp']} dBTP")
    print("  pass 2 — applying, video stream copied…")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(src), "-c:v", "copy",
         "-af", (f"loudnorm=I={I}:TP={TP}:LRA={LRA}"
                 f":measured_I={m['input_i']}:measured_TP={m['input_tp']}"
                 f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}"
                 f":offset={m['target_offset']}:linear=true:print_format=summary"),
         "-c:a", "aac", "-b:a", "192k", str(dst)], check=True)

    # The only measurement that counts: the DELIVERED file, decoded back.
    i, tp = measure(dst)
    print("\n  SHIPPED FILE (decoded back, not the PCM intermediate):")
    print(f"    integrated : {i:.1f} LUFS   (target {I})")
    print(f"    true peak  : {tp:.1f} dBTP  (must be under -1.0)")
    ok = abs(i - I) <= 1.0 and tp < -1.0
    print(f"    {'PASS' if ok else 'FAIL — do not ship'}")

    vsrc = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                           "-show_entries", "stream=nb_frames,width,height",
                           "-of", "csv=p=0", str(dst)], capture_output=True,
                          text=True).stdout.strip()
    print(f"    video      : {vsrc} (stream copied, not re-encoded)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
