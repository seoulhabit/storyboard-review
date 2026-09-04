#!/usr/bin/env python3
"""Derive assets/voice/NN-who.wav from assets/voice/raw/ at a documented tempo.

WHY. The 41 TTS takes came back at a corpus mean of 126.5 wpm. That is slow for
an explainer -- typical narration sits at 150-170 -- and it pushed the piece to
3:42 against a brief asking for approximately three minutes. The single audition
line that set the original expectation measured 184 wpm and was not
representative of the corpus.

HOW. ffmpeg's atempo is a time-stretch: it changes duration without shifting
pitch, so the voice is unchanged and only the pace moves. Up to about 1.2x is
transparent on speech; TEMPO here is well inside that.

IDEMPOTENT BY CONSTRUCTION. The raw takes are kept untouched in
assets/voice/raw/ and every working take is regenerated FROM them, so running
this twice produces the same output rather than compounding the stretch. Doing
it in place would silently speed the video up on every run.
"""
import shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOICE = ROOT / "assets" / "voice"
RAW = VOICE / "raw"
TEMPO = 1.20          # 126.5 wpm raw -> ~152 wpm
# History, because the number has moved twice and the reasons matter:
#   1.15  the first retime -- the raw takes averaged 126.5 wpm, which is sluggish
#         for an explainer, so this brought them to ~145.
#   1.265 pushed to land the piece on exactly 3:00. It got there, but at 176 wpm
#         for SoulHabit -- above the normal 150-170 explainer band, and audibly
#         hurried on the longer claim sentences.
#   1.20  dialled back on request. ~152 wpm, squarely inside the band, and the
#         most transparent of the three to atempo's time-stretch. The piece runs
#         longer than 3:00 as a result; that was the accepted trade.
# The fixed overhead stays where the 3:00 trim left it (cold open floating,
# end-card hold at its 5.0s floor, lead/tail/gap tightened) -- none of that was
# costing anything audible, so there is no reason to give it back.


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                 "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout)


def main():
    RAW.mkdir(exist_ok=True)
    takes = sorted(VOICE.glob("[0-9][0-9]-*.wav"))
    if not takes and not any(RAW.glob("*.wav")):
        sys.exit("no takes found")
    # first run: the current working takes ARE the raw takes
    for t in takes:
        if not (RAW / t.name).exists():
            shutil.copy2(t, RAW / t.name)

    before = after = 0.0
    for r in sorted(RAW.glob("[0-9][0-9]-*.wav")):
        out = VOICE / r.name
        tmp = VOICE / (r.stem + ".tmp.wav")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(r),
                        "-af", f"atempo={TEMPO}", str(tmp)], check=True)
        tmp.replace(out)
        before += dur(r); after += dur(out)
    n = len(list(RAW.glob("[0-9][0-9]-*.wav")))
    print(f"retimed {n} takes from raw/ at atempo={TEMPO}")
    print(f"  VO total {before:.1f}s -> {after:.1f}s  (saved {before - after:.1f}s)")


if __name__ == "__main__":
    main()
