#!/usr/bin/env python3
"""Two-pass EBU R128 master for a finished HyperFrames render.

Why TP=-2.5 and not -1.5. loudnorm's true-peak target applies to the PCM it
writes. Re-encoding that PCM to AAC RAISES intersample true peak, so a pass
that correctly hits -1.50 dBTP on its own output can still ship an MP4whose
decoded audio measures ABOVE 0 dBFS -- confirmed on a sibling project in this
repo, where a recorded "-1.50 dBTP final" shipped at +0.5 dBFS. Targeting
-2.5 leaves the headroom the encoder eats, and the verification pass below
re-measures the SHIPPED file rather than the intermediate.

The video stream is copied, never re-encoded, and its MD5 is compared before
and after so "audio-only change" is a measured fact rather than an assumption.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

I_TARGET, TP_TARGET, LRA_TARGET = -14.0, -2.5, 11.0

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=False)

def video_md5(path):
    r = run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(path),
             "-map", "0:v:0", "-c", "copy", "-f", "md5", "-"])
    return r.stdout.strip()

def measure(path):
    r = run(["ffmpeg", "-nostdin", "-hide_banner", "-i", str(path),
             "-af", "ebur128=peak=true", "-f", "null", "-"])
    txt = r.stderr
    tail = txt[txt.rfind("Summary"):] if "Summary" in txt else txt
    def g(label):
        m = re.search(rf"{label}:\s*(-?[\d.]+|-inf)", tail)
        return float(m.group(1)) if m and m.group(1) != "-inf" else None
    return {"I": g("I"), "LRA": g("LRA"), "TP": g("Peak")}

def main():
    # argv[1] is the project root, kept for call-signature parity with the
    # other scripts in this folder; the render paths below are what this one uses.
    src  = Path(sys.argv[2]); dst = Path(sys.argv[3])
    if not src.exists():
        sys.exit(f"FATAL: source render not found: {src}")

    print(f"[master] source : {src}")
    before_v = video_md5(src)
    before_a = measure(src)
    print(f"[master] before : I={before_a['I']} LUFS  TP={before_a['TP']} dBTP  LRA={before_a['LRA']}")

    # ---- pass 1: analyse ---------------------------------------------------
    r = run(["ffmpeg", "-nostdin", "-hide_banner", "-i", str(src), "-af",
             f"loudnorm=I={I_TARGET}:TP={TP_TARGET}:LRA={LRA_TARGET}:print_format=json",
             "-f", "null", "-"])
    blob = r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1]
    m = json.loads(blob)
    print(f"[master] pass1  : measured_I={m['input_i']} measured_TP={m['input_tp']}")

    # ---- pass 2: apply, video copied through untouched ---------------------
    af = (f"loudnorm=I={I_TARGET}:TP={TP_TARGET}:LRA={LRA_TARGET}"
          f":measured_I={m['input_i']}:measured_TP={m['input_tp']}"
          f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}"
          f":offset={m['target_offset']}:linear=true:print_format=summary")
    dst.parent.mkdir(parents=True, exist_ok=True)
    r = run(["ffmpeg", "-nostdin", "-hide_banner", "-y", "-i", str(src),
             "-af", af, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
             "-movflags", "+faststart", str(dst)])
    if r.returncode != 0 or not dst.exists():
        sys.exit(f"FATAL: pass 2 failed\n{r.stderr[-2000:]}")

    # ---- verify the SHIPPED file, not the intermediate ---------------------
    after_v = video_md5(dst)
    after_a = measure(dst)
    print(f"[master] output : {dst}")
    print(f"[master] after  : I={after_a['I']} LUFS  TP={after_a['TP']} dBTP  LRA={after_a['LRA']}")
    print(f"[master] video stream md5 {'UNCHANGED' if before_v == after_v else 'CHANGED'}")

    ok = True
    if before_v != after_v:
        print("  ✗ video stream changed -- it must be copied, not re-encoded"); ok = False
    if after_a["TP"] is not None and after_a["TP"] > -1.0:
        print(f"  ✗ shipped true peak {after_a['TP']} dBTP is above -1.0"); ok = False
    if after_a["I"] is not None and abs(after_a["I"] - I_TARGET) > 1.0:
        print(f"  ✗ shipped integrated {after_a['I']} LUFS is >1 LU from {I_TARGET}"); ok = False
    print("[master] " + ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
