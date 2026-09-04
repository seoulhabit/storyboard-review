#!/usr/bin/env python3
"""Two-pass EBU R128 master, then RE-MEASURE THE SHIPPED FILE.

    python3 scripts/master-audio.py . renders/ectoin-full.mp4 renders/<out>.mp4

Targets -14 LUFS integrated (YouTube normalises louder material down anyway).

TP=-5.0, NOT -1.5. AAC encoding raises intersample true peak, and the margin
has to cover the MEASURED overshoot rather than a guessed one. Measured twice
on this project, each time by decoding the shipped file back:

    loudnorm TP    shipped LUFS    shipped dBTP    verdict
       -2.5           -14.6           -0.7        peak fails
       -3.5           -14.5           -0.6        peak fails
       -5.0           -15.3           -3.2        LOUDNESS fails
       -4.0           -14.7           -1.8        passes both   <-- shipped

The overshoot is not a constant, which is why this took four attempts: a lower
loudnorm target applies more limiting, that changes the waveform the encoder
sees, and past about -4 the limiting starts pulling integrated loudness out of
tolerance faster than it buys peak headroom. Both criteria have to be read
together (|I + 14| <= 1.0 AND TP < -1.0) -- optimising either alone walks into
the other. The script refuses to pass either way, which
is what caught both of the attempts above. The video stream is copied through
untouched, and the measurement that counts is taken by decoding the finished MP4
back -- a number from the intermediate is not evidence about the deliverable.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

I, TP, LRA = -14.0, -4.0, 11.0   # see the table above -- measured, not guessed


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
