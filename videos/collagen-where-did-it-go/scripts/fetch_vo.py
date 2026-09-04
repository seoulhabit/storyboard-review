#!/usr/bin/env python3
"""Download a finished TTS take into assets/voice/raw/<block>.wav.

    python3 scripts/fetch_vo.py master <url>
    python3 scripts/fetch_vo.py A <url> B <url>      # two-block fallback

Block names are validated against vo_lines.BLOCKS so a take can never land
under a name the cutter does not know. Raw takes are immutable: re-running
refuses to overwrite unless --force is given.
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vo_lines import BLOCKS

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "assets" / "voice" / "raw"


def probe(p):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
         "stream=duration,sample_rate,channels", "-of", "csv=p=0", str(p)],
        capture_output=True, text=True).stdout.strip()
    return out


def main(argv):
    force = "--force" in argv
    args = [a for a in argv if a != "--force"]
    if len(args) < 2 or len(args) % 2:
        print(__doc__); return 2
    known = {b for b, _ in BLOCKS}
    RAW.mkdir(parents=True, exist_ok=True)
    for name, url in zip(args[::2], args[1::2]):
        if name not in known:
            raise SystemExit(f"unknown block {name!r}; vo_lines.BLOCKS knows {sorted(known)}")
        dst = RAW / f"{name}.wav"
        if dst.exists() and not force:
            raise SystemExit(f"{dst.relative_to(ROOT)} exists; pass --force to replace it")
        r = subprocess.run(["curl", "-sSL", "-o", str(dst), url])
        if r.returncode or not dst.exists() or dst.stat().st_size < 1000:
            raise SystemExit(f"download failed for {name}")
        print(f"  {dst.relative_to(ROOT)}  {probe(dst)}  (sample_rate,channels,duration)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
