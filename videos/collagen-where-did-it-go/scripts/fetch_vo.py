#!/usr/bin/env python3
"""Download finished TTS takes into assets/voice/NN-<who>.wav.

Usage:  python3 scripts/fetch_vo.py <idx> <url> [<idx> <url> ...]

The filename's speaker suffix is read from vo_lines.LINES, so a take can never
land under the wrong speaker's name by a typo at the call site.
"""
import subprocess, sys
from pathlib import Path
from vo_lines import LINES

ROOT = Path(__file__).resolve().parent.parent

def main(argv):
    if len(argv) < 2 or len(argv) % 2:
        sys.exit(__doc__)
    for i in range(0, len(argv), 2):
        idx, url = int(argv[i]), argv[i + 1]
        who = LINES[idx - 1][1]
        out = ROOT / "assets" / "voice" / f"{idx:02d}-{who}.wav"
        subprocess.run(["curl", "-sfL", "-o", str(out), url], check=True)
        d = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                            "format=duration", "-of", "csv=p=0", str(out)],
                           capture_output=True, text=True).stdout.strip()
        print(f"  {out.name:16s} {float(d):6.2f}s")

if __name__ == "__main__":
    main(sys.argv[1:])
