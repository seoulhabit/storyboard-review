#!/usr/bin/env python3
"""Self-contained controls for check-vo-pace.py (collagen-where-did-it-go).

Run after any change to its WPM/duration math or its audio silence
calibration:

    python3 catalog/tooling/test-vo-pace-controls.py

  WPM MATH        a synthetic 7-word, 210wpm sentence is right at the floor
                  (must NOT flag) and a 220wpm one just over it (must flag) --
                  proves the >=7-word gate and the 210 threshold are both
                  live, not just one of them.

  SHORT SENTENCE  a synthetic 4-word sentence spanning 0.8s (must flag, sub-
                  1.0s floor) vs one spanning 1.2s (must not).

  SILENCE CALIBRATION  a synthetic WAV: near-silence, then a loud tone, then a
                  short but genuinely silent gap, then more tone -- proves
                  rms_db() actually reads volumedetect's output (this exact
                  mechanism shipped broken once already this session: `-v
                  error` was silently discarding volumedetect's own INFO-level
                  log line, so every call returned None and the whole of Part
                  3 reported "SKIPPED" without anyone noticing until the
                  numbers were checked by hand) and that the calibrated
                  ceiling correctly classifies a real silent gap as silent.
"""
import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

TOOL = (Path(__file__).resolve().parents[1].parent /
        "videos" / "collagen-where-did-it-go" / "scripts" / "check-vo-pace.py")


def load_tool():
    spec = importlib.util.spec_from_file_location("check_vo_pace", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sentence(i, cid, first, last, start, end, n_words):
    return {"i": i, "cid": cid, "start": start, "end": end,
            "first_word_idx": first, "last_word_idx": last,
            "text": " ".join(["word"] * n_words)}


def main():
    mod = load_tool()
    ok = True

    print("\n  WPM MATH -- 7-word sentences at exactly 210wpm and at 220wpm:")
    manifest = {"sentences": [
        sentence(0, "u", 0, 6, 0.0, 7 * 60 / 210, 7),   # exactly 210wpm
        sentence(1, "u", 7, 13, 10.0, 10.0 + 7 * 60 / 220, 7),  # 220wpm
    ]}
    # part1_and_2 prints rather than returning structured findings; call it and
    # look for the printed lines directly instead of parsing return semantics.
    import io
    from contextlib import redirect_stdout
    buf = io.StringIO()
    with redirect_stdout(buf):
        n = mod.part1_and_2(manifest)
    lines = buf.getvalue().splitlines()
    flagged_210 = any("sentence 0" in ln for ln in lines)
    flagged_220 = any("sentence 1" in ln for ln in lines)
    good = (not flagged_210) and flagged_220 and n == 1
    ok &= good
    print(f"    210wpm flagged: {flagged_210} (must be False)   220wpm flagged: {flagged_220} (must be True)"
          f"   {'PASS' if good else 'FAIL <-- the wpm threshold or the >=7-word gate is broken'}")

    print("\n  SHORT SENTENCE -- 4-word sentences at 0.8s and 1.2s:")
    manifest = {"sentences": [
        sentence(0, "u", 0, 3, 0.0, 0.8, 4),
        sentence(1, "u", 4, 7, 10.0, 11.2, 4),
    ]}
    buf = io.StringIO()
    with redirect_stdout(buf):
        n = mod.part1_and_2(manifest)
    lines = buf.getvalue().splitlines()
    flagged_short = any("sentence 0" in ln for ln in lines)
    flagged_long = any("sentence 1" in ln for ln in lines)
    good = flagged_short and (not flagged_long) and n == 1
    ok &= good
    print(f"    0.8s flagged: {flagged_short} (must be True)   1.2s flagged: {flagged_long} (must be False)"
          f"   {'PASS' if good else 'FAIL <-- the 1.0s floor is broken'}")

    print("\n  SILENCE CALIBRATION -- synthetic WAV, a real 300ms silent gap between two tones:")
    with tempfile.TemporaryDirectory() as d:
        wav = Path(d) / "test.wav"
        # 0.3s near-silence, 1.0s tone, 0.3s TRUE silence, 1.0s tone
        subprocess.run([
            "ffmpeg", "-y", "-v", "error",
            "-f", "lavfi", "-i", "anoisesrc=d=0.3:c=white:a=0.0001",
            "-f", "lavfi", "-i", "sine=frequency=440:d=1.0",
            "-f", "lavfi", "-i", "anullsrc=d=0.3",
            "-f", "lavfi", "-i", "sine=frequency=440:d=1.0",
            "-filter_complex", "[0][1][2][3]concat=n=4:v=0:a=1",
            "-ar", "48000", "-ac", "1", str(wav),
        ], check=True, capture_output=True)

        floor = mod.rms_db(wav, 0.0, 0.25)
        tone = mod.rms_db(wav, 0.5, 1.0)
        gap = mod.rms_db(wav, 1.35, 1.55)
        mechanism_ok = floor is not None and tone is not None and gap is not None
        print(f"    floor={floor}  tone={tone}  gap={gap}   "
              f"{'PASS' if mechanism_ok else 'FAIL <-- rms_db() returned None -- volumedetect output is not being read'}")
        ok &= mechanism_ok
        if mechanism_ok:
            ceiling = tone - mod.CALIBRATION_MARGIN_DB
            gap_is_silent = gap <= ceiling
            print(f"    ceiling (tone - {mod.CALIBRATION_MARGIN_DB}dB) = {ceiling:.1f} dB   "
                  f"gap ({gap:.1f} dB) classified silent: {gap_is_silent}   "
                  f"{'PASS' if gap_is_silent else 'FAIL <-- a real silent gap is not being classified as silent'}")
            ok &= gap_is_silent

    print("\n  All controls behave as expected.\n" if ok else
          "\n  A CONTROL FAILED -- do not trust this gate until it is resolved.\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
