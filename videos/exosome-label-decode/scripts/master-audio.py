#!/usr/bin/env python3
"""Two-pass loudnorm master, then RE-MEASURE the shipped file.

Two things this gets right that a one-liner does not:

1. TARGET_TP is -2.5, not -1.5. `loudnorm` measures its own PCM output, but the
   deliverable is AAC, and lossy encoding raises intersample true peak. A prior
   project on this channel recorded -1.50 dBTP from loudnorm and shipped an MP4
   whose AAC encode actually measured +0.5 dBFS — reproduced by decoding the
   shipped file back to PCM. The extra 1 dB of headroom absorbs that.

2. The final measurement is taken by decoding the SHIPPED MP4, not by trusting
   the loudnorm pass's own report. A measurement of the intermediate is not
   evidence about the deliverable.

Video is stream-copied through untouched.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

TARGET_I = -14.0     # YouTube normalization target
TARGET_LRA = 11.0
TARGET_TP = -2.5     # deliberately below -1.5; see docstring


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def measure(path):
    r = run(["ffmpeg", "-v", "info", "-i", str(path), "-af", "ebur128=peak=true",
             "-f", "null", "-"])
    err = r.stderr
    tail = err[err.rfind("Summary:"):] if "Summary:" in err else err[-1500:]
    def grab(label):
        m = re.search(rf"{label}:\s*(-?[\d.]+|-inf)", tail)
        return m.group(1) if m else "?"
    return {"I": grab("I"), "LRA": grab("LRA"), "TP": grab("Peak")}


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    src = Path(sys.argv[2]) if len(sys.argv) > 2 else root / "renders/exosome-label-decode.raw.mp4"
    dst = Path(sys.argv[3]) if len(sys.argv) > 3 else root / "renders/exosome-label-decode.mp4"
    if not src.is_absolute():
        src = root / src
    if not dst.is_absolute():
        dst = root / dst
    if not src.exists():
        sys.exit(f"master-audio: source not found: {src}")

    print(f"master-audio: {src.name} -> {dst.name}")
    before = measure(src)
    print(f"  before        I={before['I']} LUFS  LRA={before['LRA']}  TP={before['TP']} dBTP")

    # pass 1 — analyse
    r = run(["ffmpeg", "-v", "info", "-i", str(src), "-af",
             f"loudnorm=I={TARGET_I}:LRA={TARGET_LRA}:TP={TARGET_TP}:print_format=json",
             "-f", "null", "-"])
    m = re.search(r"\{[^{}]*input_i[^{}]*\}", r.stderr, re.DOTALL)
    if not m:
        sys.exit("master-audio: could not parse loudnorm pass-1 JSON")
    st = json.loads(m.group(0))
    print(f"  pass 1        measured_I={st['input_i']}  measured_TP={st['input_tp']}")

    # pass 2 — apply, video copied through untouched
    af = (f"loudnorm=I={TARGET_I}:LRA={TARGET_LRA}:TP={TARGET_TP}"
          f":measured_I={st['input_i']}:measured_LRA={st['input_lra']}"
          f":measured_TP={st['input_tp']}:measured_thresh={st['input_thresh']}"
          f":offset={st['target_offset']}:linear=true:print_format=summary")
    # Cap the output at the VIDEO stream's exact duration. AAC encoder padding
    # otherwise runs ~100ms past the last frame (measured: video 55.800 / audio
    # 55.900), leaving a tail with no picture under it -- which for a Short is
    # precisely at the loop seam.
    vdur = run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                "-show_entries", "stream=duration", "-of", "csv=p=0", str(src)]).stdout.strip()
    dst.parent.mkdir(parents=True, exist_ok=True)
    r2 = run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-af", af,
              "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
              "-t", vdur, str(dst)])
    if r2.returncode != 0:
        sys.exit(f"master-audio: pass 2 failed\n{r2.stderr[-1200:]}")

    # RE-MEASURE the shipped deliverable, not the intermediate
    after = measure(dst)
    print("  after (SHIPPED FILE, AAC-decoded)")
    print(f"                I={after['I']} LUFS  LRA={after['LRA']}  TP={after['TP']} dBTP")

    try:
        tp = float(after["TP"])
        if tp > -1.0:
            print(f"  WARNING: shipped true peak {tp} dBTP is above -1.0 — lower TARGET_TP.")
        else:
            print(f"  OK: shipped true peak {tp} dBTP is under the -1.0 ceiling.")
    except ValueError:
        print("  WARNING: could not parse shipped true peak.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
