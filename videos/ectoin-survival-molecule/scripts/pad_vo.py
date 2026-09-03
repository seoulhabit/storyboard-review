#!/usr/bin/env python3
"""Pad every voiceover take with a short silent tail, in place.

Measured on this project: 7 of 28 takes end with the last word still LIVE at
end-of-file (take 13's final 250ms was -24 dB, LOUDER than its own file
average). The composition fades each VO clip out over its final 80ms, and a fade
applied to audio that is still live does not smooth anything -- it just mutes an
active word faster, which reads as a different flavour of abrupt.

The audio itself is fine; there is simply no room for the fade to happen in. So
pad rather than re-record: non-destructive, repeatable, and it gives the mixer
the tail it assumes exists. Idempotent -- a take that already has quiet at the
end is padded to the same target, not stacked.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAD_S = 0.25

# Strip ALL trailing silence, then add exactly PAD_S back. Idempotent by
# CONSTRUCTION -- no marker file, no measurement to get wrong. Two earlier
# attempts stacked pads: a marker-file version broke when the marker was
# cleared, and a silencedetect version failed because ffmpeg emits a
# silence_end at EOF, so "a start with no matching end" never matched.
# areverse + silenceremove(start) + areverse is the standard idiom for
# trimming the END of a stream, since silenceremove only trims from the front.
FILTER = (f"areverse,"
          f"silenceremove=start_periods=1:start_threshold=-50dB:start_duration=0,"
          f"areverse,"
          f"apad=pad_dur={PAD_S}")


def main():
    n = 0
    for f in sorted((ROOT / "assets" / "voice").glob("[0-9][0-9].wav")):
        tmp = f.with_suffix(".norm.wav")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(f),
                        "-af", FILTER, str(tmp)], check=True)
        tmp.replace(f)
        n += 1
    print(f"  normalised {n} take(s) to exactly {PAD_S*1000:.0f}ms trailing silence")
    return 0


if __name__ == "__main__":
    sys.exit(main())
