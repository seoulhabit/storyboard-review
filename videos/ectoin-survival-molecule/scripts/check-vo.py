#!/usr/bin/env python3
"""QC every voiceover take before it drives scene timing.

Three checks, each for a defect measured on this project's own takes:

1. SPEECH RATE. Two takes came back near 110 wpm against a ~155 wpm norm, both on
   comma-heavy enumerations -- this engine slows sharply on comma lists. Slow is
   not automatically wrong (a list of stressors reads well unhurried), but it must
   be a decision, not a surprise, because scene duration is derived from it.

2. TRAILING TAIL. Roughly half the takes end with the last word still live at
   end-of-file. The composition fades each clip out over its final 80ms, and a
   fade applied to audio that is still live just mutes an active word faster --
   it does not smooth anything. Flags takes whose last 250ms is not meaningfully
   quieter than the file average.

3. RARE-WORD PRONUNCIATION. "ectoin" is the video's central term. Take 08
   garbled it twice, DIFFERENTLY each time ("Ecton", then "ectoene"), which is
   the signature of an articulation failure rather than a transcription miss --
   takes 03 and 05 render it cleanly. Transcript-diffing across takes is the only
   way to tell those apart.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Only ectoin-SHAPED tokens. The previous pattern matched any word containing
# "ect", so "protective" and "protects" reported as garbled -- a false positive
# that would have sent two perfectly good takes back for regeneration.
RARE = re.compile(r'\b[Ee]ct[a-z]*\b|\b[a-z]*ecto[a-z]*\b', re.IGNORECASE)
EXPECT = {"ectoin", "ectoins"}
SLOW_WPM, FAST_WPM, TAIL_MARGIN_DB = 130.0, 190.0, 12.0


def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                 "format=duration", "-of", "csv=p=0", str(f)],
                                capture_output=True, text=True).stdout)


def rms(f, ss=None):
    c = ["ffmpeg", "-nostdin"] + (["-ss", str(ss)] if ss is not None else [])
    c += ["-i", str(f), "-af", "astats", "-f", "null", "-"]
    m = re.search(r"RMS level dB:\s*(-?[\d.]+|-inf)",
                  subprocess.run(c, capture_output=True, text=True).stderr)
    if not m or m.group(1) == "-inf":
        return float("-inf")
    return float(m.group(1))


def main():
    sys.path.insert(0, str(ROOT / "scripts"))
    from vo_lines import LINES
    act1 = {1: 26, 2: 22, 3: 25, 4: 25, 5: 27, 6: 26, 7: 26}
    findings = []
    print(f"  {'take':6s} {'dur':>7s} {'wpm':>6s} {'tail dB':>9s}  notes")
    for f in sorted((ROOT / "assets" / "voice").glob("[0-9][0-9].wav")):
        n = int(f.stem)
        words = act1.get(n) if n <= 7 else (len(LINES[n - 8][1].split()) if n - 8 < len(LINES) else None)
        d = dur(f)
        wpm = words / d * 60 if words else 0
        whole, tail = rms(f), rms(f, ss=max(0, d - 0.25))
        notes = []
        if words and wpm < SLOW_WPM:
            notes.append(f"SLOW ({wpm:.0f} wpm)"); findings.append((f.name, "slow"))
        if words and wpm > FAST_WPM:
            notes.append(f"FAST ({wpm:.0f} wpm)"); findings.append((f.name, "fast"))
        if tail > whole - TAIL_MARGIN_DB:
            notes.append("LIVE AT EOF"); findings.append((f.name, "no-tail"))
        print(f"  {f.name:6s} {d:7.2f} {wpm:6.1f} {tail:9.1f}  {', '.join(notes) or 'ok'}")

    print("\n  rare-word check (transcribes every take -- slow, whisper small.en):")
    for f in sorted((ROOT / "assets" / "voice").glob("[0-9][0-9].wav")):
        r = subprocess.run(["npx", "--yes", "hyperframes@0.8.22", "transcribe", str(f),
                            "--engine", "whisper", "--model", "small.en",
                            "--timeout", "300000"],
                           capture_output=True, text=True, cwd=ROOT)
        tp = ROOT / "assets" / "voice" / "transcript.json"
        if not tp.exists():
            continue
        txt = " ".join(w["text"] for w in json.load(open(tp)))
        bad = [w for w in RARE.findall(txt) if w.lower() not in EXPECT]
        if bad:
            print(f"    {f.name}: {bad}   <-- garbled")
            findings.append((f.name, "pronunciation"))
    if not findings:
        print("\n  All takes pass.")
    else:
        print(f"\n  {len(findings)} finding(s). A garbled rare word needs a PHONETIC "
              "RESPELLING in the\n  TTS prompt only -- never in the on-screen text or "
              "the caption.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
