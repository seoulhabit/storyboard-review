#!/usr/bin/env python3
"""Cut assets/bgm/bed.mp3 to this edit's exact length from the channel's bed.

Source: videos/centella-barrier-recut-15s/assets/bgm/track-soft.mp3
(md5 8cc9c49b..., 180.0s), already shared by three projects. Reusing the
channel's established bed is the consistency win; what is NOT reusable is its
envelope.

MEASURED on the source, per 2s RMS over its last 12 seconds:

    t=168.0s  -41.0 dB      t=174.0s  -87.1 dB
    t=170.0s  -59.9 dB      t=176.0s  -96.0 dB
    t=172.0s  -82.5 dB      t=178.0s  -82.7 dB

So the file's last ~12s is an authored fade-out to effectively digital silence,
sized for ITS original running time. Dropped in unmodified under a longer edit
it would leave a dead stretch; under a shorter one the fade lands before the
video ends and hands a replay a dead beat. Either way the fix is the same: use
only the LIVE BODY, loop it to this edit's real length, and author our own short
declick fades at both ends.

LENGTH comes from timing.walk() -- the same walk build_index.py writes into
the root's data-duration -- so this can run in any order relative to it.
"""
import re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from timing import walk
SRC = ROOT.parent / "centella-barrier-recut-15s" / "assets" / "bgm" / "track-soft.mp3"
OUT = ROOT / "assets" / "bgm" / "bed.mp3"

BODY_IN, BODY_OUT = 4.0, 166.0    # live music only -- excludes the authored fade
# The bed also has an INTRO BUILD, and it is a second version of the same trap.
# Measured RMS per 10s on the source: 0s -33.6, 10s -29.9, 20s -19.2, then full
# at -13 to -14 from 30s through 158s. Looping the body from BODY_IN therefore
# re-uses the quietest 25 seconds in the file -- and the loop lands them at the
# END of the video, which is where a bed most needs to still be there. The
# second pass starts at a full-level point instead. (Pass ONE may start quiet;
# that suits a cold open, so BODY_IN stays where it is.)
LOOP_IN = 120.0
XFADE = 4.0                        # seam crossfade when the body must repeat
DECLICK = 0.25                     # our own edge fades


def root_duration():
    return walk()[2]


def rms(path, start, dur):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-f", "lavfi",
         f"amovie={path},atrim=start={start}:duration={dur},astats=metadata=1:reset=0",
         "-show_entries", "frame_tags=lavfi.astats.Overall.RMS_level",
         "-of", "csv=p=0"], capture_output=True, text=True).stdout.strip().splitlines()
    return float(out[-1]) if out and out[-1] not in ("", "-inf") else -99.0


def main():
    if not SRC.exists():
        sys.exit(f"source bed missing: {SRC}")
    total = root_duration()
    body = BODY_OUT - BODY_IN
    OUT.parent.mkdir(parents=True, exist_ok=True)

    if total <= body:
        cmd = ["ffmpeg", "-y", "-v", "error", "-ss", str(BODY_IN), "-t", str(total),
               "-i", str(SRC), "-af",
               f"afade=t=in:st=0:d={DECLICK},"
               f"afade=t=out:st={total - DECLICK:.3f}:d={DECLICK}",
               "-c:a", "libmp3lame", "-b:a", "192k", str(OUT)]
    else:
        need = total - body + XFADE      # second pass length, allowing for the seam
        if LOOP_IN + need > BODY_OUT:
            sys.exit(f"loop pass of {need:.1f}s from {LOOP_IN}s runs into the "
                     f"source's own fade at {BODY_OUT}s -- pick an earlier LOOP_IN")
        cmd = ["ffmpeg", "-y", "-v", "error",
               "-ss", str(BODY_IN), "-t", str(body), "-i", str(SRC),
               "-ss", str(LOOP_IN), "-t", str(need), "-i", str(SRC),
               "-filter_complex",
               f"[0:a][1:a]acrossfade=d={XFADE}:c1=tri:c2=tri[x];"
               f"[x]atrim=0:{total:.3f},"
               f"afade=t=in:st=0:d={DECLICK},"
               f"afade=t=out:st={total - DECLICK:.3f}:d={DECLICK}[a]",
               "-map", "[a]", "-c:a", "libmp3lame", "-b:a", "192k", str(OUT)]
    subprocess.run(cmd, check=True)

    got = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                "format=duration", "-of", "csv=p=0", str(OUT)],
                               capture_output=True, text=True).stdout)
    print(f"assets/bgm/bed.mp3  {got:.3f}s (target {total:.3f}s)")
    # The check that matters: the bed must still be LIVE at both ends, or the
    # mix hands the final beat -- and a replay -- to silence.
    print(f"  first 2s RMS {rms(OUT, 0, 2):7.2f} dB")
    print(f"  last  2s RMS {rms(OUT, max(0, got - 2), 2):7.2f} dB")
    print(f"  source last 2s for comparison: {rms(SRC, 178, 2):7.2f} dB")


if __name__ == "__main__":
    main()
