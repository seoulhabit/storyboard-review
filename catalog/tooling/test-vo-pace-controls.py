#!/usr/bin/env python3
"""Self-contained controls for check-vo-pace.py (beside this file).

Run after any change to its WPM/duration math, its manifest normaliser, or its
audio silence calibration:

    python3 catalog/tooling/test-vo-pace-controls.py

  MANIFEST SHAPES  the same two sentences written in BOTH manifest shapes the
                   gate claims to read -- a master manifest with
                   first_word_idx/last_word_idx, and a per-scene manifest with
                   a words array and a top-level `scene` -- must normalise to
                   the same word counts and the same cid. This is the gate's
                   portability boundary, so it is the fixture most worth
                   having: a project whose manifests take the second shape gets
                   silently wrong wpm numbers if this drifts, and wrong numbers
                   look exactly like right ones.

  WPM MATH         a synthetic 7-word, 210wpm sentence right at the floor (must
                   NOT flag) and a 220wpm one just over it (must flag) --
                   proves the >=7-word gate and the 210 threshold are both
                   live, not just one of them.

  SHORT SENTENCE   a synthetic 4-word sentence spanning 0.8s (must flag, sub-
                   1.0s floor) vs one spanning 1.2s (must not).

  SILENCE CALIBRATION  a synthetic WAV: near-silence, then a loud tone, then a
                   short but genuinely silent gap, then more tone -- proves
                   rms_db() actually reads volumedetect's output (this exact
                   mechanism shipped broken once: `-v error` was silently
                   discarding volumedetect's own INFO-level log line, so every
                   call returned None and the whole of Part 3 reported
                   "SKIPPED" without anyone noticing until the numbers were
                   checked by hand) and that the gate's own ceiling correctly
                   classifies a real silent gap as silent.

NOTE ON THAT LAST ONE. It calls the gate's silence_ceiling() and is_silent();
the version this replaced computed `gap <= tone - CALIBRATION_MARGIN_DB` in the
fixture itself, which tests the fixture's arithmetic and would keep passing
while the gate's own classification broke.
"""
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

TOOL = Path(__file__).resolve().parent / "check-vo-pace.py"


def load_tool():
    spec = importlib.util.spec_from_file_location("check_vo_pace", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def write(d, name, obj):
    p = Path(d) / name
    p.write_text(json.dumps(obj))
    return p


def run_part12(mod, sentences, **kw):
    """part1_and_2 prints rather than returning structured findings; capture the
    output and read the flagged lines directly."""
    import io
    from contextlib import redirect_stdout
    buf = io.StringIO()
    with redirect_stdout(buf):
        n = mod.part1_and_2(sentences, kw.get("min_words", mod.MIN_WORDS_FOR_WPM_CHECK),
                            kw.get("max_wpm", mod.MAX_WPM),
                            kw.get("min_sentence_s", mod.MIN_SENTENCE_S))
    return n, buf.getvalue().splitlines()


def main():
    if not TOOL.exists():
        print(f"test-vo-pace-controls: {TOOL.name} not found beside this fixture -- "
              f"skipping (exit 0).")
        return 0
    mod = load_tool()
    ok = True

    with tempfile.TemporaryDirectory() as d:
        print("\n  MANIFEST SHAPES -- the same two sentences, both supported shapes:")
        # 4 words then 3 words, identical content, written the two ways.
        master = {"words": [{"i": i, "text": "w", "start": i * 0.5, "end": i * 0.5 + 0.4}
                            for i in range(7)],
                  "sentences": [
                      {"i": 0, "cid": "01-hook", "start": 0.0, "end": 2.0,
                       "first_word_idx": 0, "last_word_idx": 3, "text": "a b c d"},
                      {"i": 1, "cid": "01-hook", "start": 2.0, "end": 3.5,
                       "first_word_idx": 4, "last_word_idx": 6, "text": "e f g"}]}
        per_scene = {"scene": "01-hook",
                     "words": [{"text": "w", "start": i * 0.5, "end": i * 0.5 + 0.4}
                               for i in range(7)],
                     "sentences": [
                         {"start": 0.0, "end": 2.0, "text": "a b c d"},
                         {"start": 2.0, "end": 3.5, "text": "e f g"}]}
        a, _, _ = mod.load(write(d, "master.words.json", master))
        b, _, _ = mod.load(write(d, "01.words.json", per_scene))
        counts_a = [(s["cid"], s["n_words"]) for s in a]
        counts_b = [(s["cid"], s["n_words"]) for s in b]
        good = counts_a == counts_b == [("01-hook", 4), ("01-hook", 3)]
        ok &= good
        print(f"    master   -> {counts_a}\n    per-scene -> {counts_b}   "
              f"{'PASS' if good else 'FAIL <-- the two manifest shapes do not normalise alike'}")

        print("\n  MANIFEST SHAPES -- sibling wav resolution for both stems:")
        _, wav_a, _ = mod.load(Path(d) / "master.words.json")
        _, wav_b, _ = mod.load(Path(d) / "01.words.json")
        good = wav_a.name == "master.wav" and wav_b.name == "01.wav"
        ok &= good
        print(f"    master.words.json -> {wav_a.name}   01.words.json -> {wav_b.name}   "
              f"{'PASS' if good else 'FAIL <-- Part 3 would measure the wrong file, or none'}")

    print("\n  WPM MATH -- 7-word sentences at exactly 210wpm and at 220wpm:")
    sentences = [
        {"i": 0, "cid": "u", "start": 0.0, "end": 7 * 60 / 210, "n_words": 7, "text": "x"},
        {"i": 1, "cid": "u", "start": 10.0, "end": 10.0 + 7 * 60 / 220, "n_words": 7, "text": "x"},
    ]
    n, lines = run_part12(mod, sentences)
    flagged_210 = any("sentence 0" in ln for ln in lines)
    flagged_220 = any("sentence 1" in ln for ln in lines)
    good = (not flagged_210) and flagged_220 and n == 1
    ok &= good
    print(f"    210wpm flagged: {flagged_210} (must be False)   220wpm flagged: {flagged_220} "
          f"(must be True)   "
          f"{'PASS' if good else 'FAIL <-- the wpm threshold or the >=7-word gate is broken'}")

    print("\n  WPM MATH -- a 6-word sentence at 220wpm must NOT flag (the word-count gate):")
    sentences = [{"i": 0, "cid": "u", "start": 0.0, "end": 6 * 60 / 220, "n_words": 6, "text": "x"}]
    n, lines = run_part12(mod, sentences)
    good = n == 0
    ok &= good
    print(f"    flagged: {n} finding(s) (must be 0)   "
          f"{'PASS' if good else 'FAIL <-- the word-count floor is not gating short beats'}")

    print("\n  SHORT SENTENCE -- 4-word sentences at 0.8s and 1.2s:")
    sentences = [
        {"i": 0, "cid": "u", "start": 0.0, "end": 0.8, "n_words": 4, "text": "x"},
        {"i": 1, "cid": "u", "start": 10.0, "end": 11.2, "n_words": 4, "text": "x"},
    ]
    n, lines = run_part12(mod, sentences)
    flagged_short = any("sentence 0" in ln for ln in lines)
    flagged_long = any("sentence 1" in ln for ln in lines)
    good = flagged_short and (not flagged_long) and n == 1
    ok &= good
    print(f"    0.8s flagged: {flagged_short} (must be True)   1.2s flagged: {flagged_long} "
          f"(must be False)   {'PASS' if good else 'FAIL <-- the 1.0s floor is broken'}")

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
        mechanism_ok = None not in (floor, tone, gap)
        print(f"    floor={floor}  tone={tone}  gap={gap}   "
              f"{'PASS' if mechanism_ok else 'FAIL <-- rms_db() returned None -- volumedetect output is not being read'}")
        ok &= mechanism_ok
        if mechanism_ok:
            ceiling = mod.silence_ceiling(tone)
            good = mod.is_silent(gap, ceiling) and not mod.is_silent(tone, ceiling)
            ok &= good
            print(f"    gate's ceiling = {ceiling:.1f} dB   gap ({gap:.1f}) silent: "
                  f"{mod.is_silent(gap, ceiling)}   tone ({tone:.1f}) silent: "
                  f"{mod.is_silent(tone, ceiling)} (must be False)   "
                  f"{'PASS' if good else 'FAIL <-- the gate is misclassifying silence'}")

            good = mod.silence_ceiling(None) == -40.0
            ok &= good
            print(f"    unmeasurable speech level falls back to {mod.silence_ceiling(None)} dB   "
                  f"{'PASS' if good else 'FAIL <-- the no-signal fallback is gone'}")

    print("\n  All controls behave as expected.\n" if ok else
          "\n  A CONTROL FAILED -- do not trust this gate until it is resolved.\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
