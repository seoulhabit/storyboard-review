#!/usr/bin/env python3
"""Master the retention render: two-pass EBU R128 loudnorm (same targets as
master-audio.py: -14 LUFS / -4.0 dBTP / LRA 11), AAC stereo 48 kHz, video
stream copied through untouched (already H.264 High / BT.709 / 30 fps /
10 Mbps from `hyperframes render --video-bitrate 10M`). Then RE-MEASURE the
shipped file and print the stream facts the delivery spec asks for.

    python3 scripts/master-retention.py renders/<raw>.mp4 renders/<master>.mp4
"""
import json, re, subprocess, sys
from pathlib import Path

I, TP, LRA = -14.0, -4.0, 11.0


def measure(path):
    err = subprocess.run(["ffmpeg", "-nostdin", "-i", str(path), "-af", "ebur128=peak=true",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    tail = err[err.rindex("Summary:"):] if "Summary:" in err else err
    i = float(re.search(r"I:\s*(-?[\d.]+)\s*LUFS", tail).group(1))
    tp = float(re.search(r"Peak:\s*(-?[\d.]+)\s*dBFS", tail).group(1))
    return i, tp


def main():
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    if dst.exists():
        print(f"refusing to overwrite {dst}"); return 2
    err = subprocess.run(["ffmpeg", "-nostdin", "-i", str(src), "-af",
                          f"loudnorm=I={I}:TP={TP}:LRA={LRA}:print_format=json", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    m = json.loads(re.search(r"\{[^{}]*\}", err[err.rindex("{") - 1:]).group(0))
    print(f"  measured I={m['input_i']} LUFS, TP={m['input_tp']} dBTP")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-c:v", "copy",
                    "-af", (f"loudnorm=I={I}:TP={TP}:LRA={LRA}:measured_I={m['input_i']}"
                            f":measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
                            f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}"
                            f":linear=true:print_format=summary"),
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                    "-movflags", "+faststart", str(dst)], check=True)
    i, tp = measure(dst)
    print(f"  SHIPPED: {i:.2f} LUFS / {tp:.2f} dBTP  ({'PASS' if abs(i - I) <= 1.0 and tp < -1.0 else 'FAIL'})")
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "format=duration,bit_rate:stream=codec_name,profile,width,height,r_frame_rate,"
                          "color_primaries,color_transfer,color_space,sample_rate,channels,bit_rate",
                          "-of", "default=nw=1", str(dst)], capture_output=True, text=True).stdout
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
