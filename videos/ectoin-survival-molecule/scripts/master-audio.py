#!/usr/bin/env python3
"""Two-pass EBU R128 master, then RE-MEASURE THE SHIPPED FILE.

    python3 scripts/master-audio.py . renders/ectoin-full.mp4 renders/<out>.mp4

Targets -14 LUFS integrated (YouTube normalises louder material down anyway).

TP=-4.0, NOT -2.5. This project's first master (VO only, no bed) shipped at
TP=-2.5 and measured -1.9 dBTP on the decoded deliverable -- inside spec on
the number the old script reported, but the true peak that matters (the
DELIVERED, AAC-encoded file, decoded back) was already eating most of its
-1.0 dBTP margin before a music bed and SFX cues stack on top of the VO. AAC
encoding raises intersample true peak regardless of source TP, and adding a
bed raises the source TP itself (two signals summing). -4.0 is the plan's
adopted margin for a mixed VO+bed+SFX master, per the sibling project
ectoin-normal-person's build (see that project's own master-audio.py and
DELIVERY.md for its measured numbers) -- RE-MEASURE this project's own
decoded deliverable below rather than trusting either project's number by
analogy; that is what this script's final assertion is for.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

I, TP, LRA = -14.0, -4.0, 11.0


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
