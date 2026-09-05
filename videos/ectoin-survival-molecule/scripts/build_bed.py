#!/usr/bin/env python3
"""Cut assets/music/bed.mp3 to this edit's exact length from the channel's bed.

PORTED from videos/collagen-where-did-it-go/scripts/build_bgm.py. This project
shipped a bed frozen at 338.145s -- exactly the length of the cut that built it,
which is fine until the next cut is longer, and then the music simply stops
while the end card is still on screen. The length is taken from walk() here for
the same reason build_index.py now takes it from walk(): a duration written down
in two places disagrees the first time either one moves.

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
OUT = ROOT / "assets" / "music" / "bed.mp3"

# MEASURED on the source, per 10s RMS: 0-20s is an intro build at -35 to -20 dB,
# 30-158s sits flat at -14 to -18 dB, and the last ~12s is an authored fade to
# digital silence sized for ITS running time, not ours. So only the flat body is
# usable, and it has to be looped: 128s of body under a 6:11 edit is three
# passes, where the sibling project this file came from only ever needed two.
BODY_IN, BODY_OUT = 30.0, 158.0
XFADE = 4.0            # seam crossfade between passes
DECLICK = 0.25         # our own edge fades


def root_duration():
    # ectoin's walk() returns (scenes, total), not the 3-tuple the source
    # project's does.
    return walk()[1]


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

    # n passes crossfaded end to end give body + (n-1)*(body - XFADE).
    n = 1
    while body + (n - 1) * (body - XFADE) < total:
        n += 1
    inputs, filt, prev = [], [], None
    for k in range(n):
        inputs += ["-ss", str(BODY_IN), "-t", str(body), "-i", str(SRC)]
        if k == 0:
            prev = "[0:a]"
            continue
        lbl = f"[x{k}]"
        filt.append(f"{prev}[{k}:a]acrossfade=d={XFADE}:c1=tri:c2=tri{lbl}")
        prev = lbl
    filt.append(f"{prev}atrim=0:{total:.3f},"
                f"afade=t=in:st=0:d={DECLICK},"
                f"afade=t=out:st={total - DECLICK:.3f}:d={DECLICK}[a]")
    cmd = (["ffmpeg", "-y", "-v", "error"] + inputs +
           ["-filter_complex", ";".join(filt), "-map", "[a]",
            "-c:a", "libmp3lame", "-b:a", "192k", str(OUT)])
    subprocess.run(cmd, check=True)

    got = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                "format=duration", "-of", "csv=p=0", str(OUT)],
                               capture_output=True, text=True).stdout)
    print(f"assets/music/bed.mp3  {got:.3f}s (target {total:.3f}s, {n} passes)")
    # The check that matters: the bed must still be LIVE at both ends, or the
    # mix hands the final beat -- and a replay -- to silence.
    head, tail = rms(OUT, 0, 2), rms(OUT, max(0, got - 2), 2)
    print(f"  first 2s RMS {head:7.2f} dB")
    print(f"  last  2s RMS {tail:7.2f} dB")
    if abs(got - total) > 0.05:
        sys.exit(f"FAIL: bed is {got:.3f}s against a {total:.3f}s edit")
    if head < -45 or tail < -45:
        sys.exit("FAIL: bed is not live at both ends")


if __name__ == "__main__":
    main()
