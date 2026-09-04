#!/usr/bin/env python3
"""Synthesize the four one-shot SFX this piece needs, deterministically, with
ffmpeg alone -- no library, no licence, no randomness without a seed -- and
measure every file's peak offset so sfx.py can land the PEAK on the word,
not the file start.

    python3 scripts/make_sfx.py        # writes assets/sfx/*.wav + peaks.json + README.md

The two reused files (impact-bass-2.mp3, citation-tick-trimmed.mp3) come from
videos/ectoin-survival-molecule/assets/sfx/ and are measured here too.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SFX = ROOT / "assets" / "sfx"

SYNTH = {
    # name: (duration, lavfi source, extra -af)
    "slice.wav": (0.35, "anoisesrc=color=white:seed=7:r=48000:d=0.35",
                  "highpass=f=1800,lowpass=f=9000,afade=t=in:d=0.005,afade=t=out:st=0.06:d=0.29,volume=-10dB"),
    "fragment.wav": (0.50,
                     "aevalsrc='0.6*sin(2*PI*1400*t)*exp(-40*t)"
                     "+0.5*gt(t,0.09)*sin(2*PI*2100*(t-0.09))*exp(-40*(t-0.09))"
                     "+0.4*gt(t,0.17)*sin(2*PI*2800*(t-0.17))*exp(-40*(t-0.17))':s=48000:d=0.5",
                     "volume=-6dB"),
    "filter.wav": (0.45, "aevalsrc='0.5*sin(2*PI*(520-400*t/0.45)*t)*exp(-6*t)':s=48000:d=0.45",
                   "lowpass=f=3000,volume=-4dB"),
    "lock.wav": (0.30, "aevalsrc='0.7*sin(2*PI*180*t)*exp(-25*t)+0.3*sin(2*PI*2600*t)*exp(-120*t)':s=48000:d=0.3",
                 "volume=-4dB"),
}


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True)


def peak(path):
    """(offset_s, peak_dBFS) of the loudest sample, decoded to mono 48k s16."""
    import numpy as np
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(path), "-f", "s16le",
                        "-ac", "1", "-ar", "48000", "-"], capture_output=True)
    x = np.frombuffer(r.stdout, dtype=np.int16).astype(float)
    if not len(x):
        return 0.0, -99.0
    i = int(np.argmax(np.abs(x)))
    return round(i / 48000, 3), round(20 * np.log10(max(1, abs(x[i])) / 32768), 1)


def main():
    SFX.mkdir(parents=True, exist_ok=True)
    for name, (d, src, af) in SYNTH.items():
        out = SFX / name
        r = sh("ffmpeg", "-y", "-nostdin", "-v", "error", "-f", "lavfi", "-i", src,
               "-t", f"{d}", "-af", af, "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le", str(out))
        if r.returncode:
            raise SystemExit(f"{name}: {r.stderr[:400]}")
    peaks, rows = {}, []
    for p in sorted(SFX.iterdir()):
        if p.suffix.lower() not in (".wav", ".mp3"):
            continue
        off, db = peak(p)
        dur = float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration",
                       "-of", "csv=p=0", str(p)).stdout.strip() or 0)
        peaks[p.name] = {"peak_offset": off, "peak_dbfs": db, "duration": round(dur, 3)}
        rows.append(f"| `{p.name}` | {dur:.3f} | {off:.3f} | {db} | "
                    f"{'synthesized here (make_sfx.py)' if p.name in SYNTH else 'videos/ectoin-survival-molecule/assets/sfx/'} |")
    (SFX / "peaks.json").write_text(json.dumps(peaks, indent=2) + "\n")
    (SFX / "README.md").write_text(
        "# SFX provenance\n\nGenerated/measured by `scripts/make_sfx.py`. Every cue in "
        "`scripts/sfx.py` is placed so the file's PEAK lands on its word.\n\n"
        "| file | duration s | peak offset s | peak dBFS | source |\n|---|---|---|---|---|\n"
        + "\n".join(rows) + "\n\nThe four `.wav` files are pure ffmpeg synthesis "
        "(`anoisesrc` with a fixed seed, `aevalsrc` decays): deterministic, no licence. "
        "The two `.mp3` files are reused from the ectoin project's SFX set.\n")
    print(json.dumps(peaks, indent=1))


if __name__ == "__main__":
    sys.exit(main())
