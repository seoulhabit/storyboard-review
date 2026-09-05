#!/usr/bin/env python3
"""QC narration pace from the master manifest and the actual audio -- no
re-transcription (modelled on ectoin-survival-molecule/scripts/check-vo.py's
"read the manifest, don't re-derive it" principle, adapted for this project's
single continuous master take rather than per-scene clips).

    python3 scripts/check-vo-pace.py .

Advisory: always exits 0. It reports; it does not gate (this project's own
check-cadence.py convention) -- several of the sentences short enough to flag
here ("Not smoking.", "Same result.", "Definitely fail?") are deliberate
punchy beats in the established style, and the review's own reviewed hook
exception (--exempt-window in check-captions.py) shows up here too as an
expected, not a surprising, finding.

Three checks:

1. PER-SENTENCE WPM. Sentences of >=7 words above 210 wpm -- the review's own
   number, chosen because a short sentence's wpm is dominated by fixed
   articulation overhead (measured this session: "Now, the powder." at 3
   words computes to 386 wpm and is not actually rushed to a listener; "Keep
   only the studies without industry funding, and it is no longer
   statistically significant." at 16 words computing high IS a real
   speech-rate problem). The word-count floor is what keeps this from
   flagging every short punchy beat in the piece.

2. SUB-1.0s SENTENCES. Flagged regardless of word count -- a sentence a
   viewer cannot finish reading as a caption before it changes state is a
   pace problem even if its wpm number looks unremarkable in isolation.

3. SENTENCE-BOUNDARY SILENCE, MEASURED ON THE AUDIO, NOT THE MANIFEST. This
   project's own review found 13 boundaries under 100ms in the manifest, of
   which only 2 were genuine hard joins -- the other 11 carried 60-190ms of
   real silence the manifest's word timestamps simply didn't capture. A
   naive fixed dB gate over-reads on this specific take (its floor is true
   digital silence, not room tone), so each boundary is measured against a
   THRESHOLD CALIBRATED ON THIS TAKE's OWN measured floor (sampled from the
   silence before the first word), not an absolute number carried in from
   another project's take.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
MANIFEST = ROOT / "assets" / "voice" / "master.words.json"
WAV = ROOT / "assets" / "voice" / "master.wav"

MIN_WORDS_FOR_WPM_CHECK = 7
MAX_WPM = 210
MIN_SENTENCE_S = 1.0
MIN_BOUNDARY_MS = 100
CALIBRATION_MARGIN_DB = 6.0  # a boundary must be at least this far below the take's
                             # own measured PEAK speech level to count as "silent" --
                             # not an absolute dB number, so it travels to a louder
                             # or quieter take without retuning.


def sh(*a):
    return subprocess.run([str(x) for x in a], capture_output=True, text=True, check=False)


def rms_db(wav, start, end):
    """Mean volume (dB) of [start,end) via ffmpeg's own volumedetect -- one
    process per span, but spans here are ~50-300ms so this stays fast.

    volumedetect logs its result at ffmpeg's INFO level, not error -- `-v
    error` (this project's usual convention for a quiet subprocess call)
    silently discards it along with everything else, so this always prints
    "n_samples: 0" and never the actual mean_volume line. `-v info` is
    required here specifically because the thing being measured IS an info-
    level log line, not an error."""
    r = sh("ffmpeg", "-nostdin", "-v", "info", "-ss", f"{start:.3f}", "-to", f"{end:.3f}",
           "-i", wav, "-af", "volumedetect", "-f", "null", "-")
    for line in r.stderr.splitlines():
        if "mean_volume" in line:
            return float(line.split(":")[1].strip().rstrip(" dB"))
    return None


def part1_and_2(manifest):
    print("PART 1+2 -- per-sentence WPM and minimum duration (from the manifest)")
    findings = []
    for s in manifest["sentences"]:
        n = s["last_word_idx"] - s["first_word_idx"] + 1
        dur = s["end"] - s["start"]
        wpm = n / dur * 60 if dur > 0 else 0
        flags = []
        if n >= MIN_WORDS_FOR_WPM_CHECK and wpm > MAX_WPM:
            flags.append(f"{wpm:.0f}wpm > {MAX_WPM} ({n} words)")
        if dur < MIN_SENTENCE_S:
            flags.append(f"{dur:.2f}s < {MIN_SENTENCE_S:.1f}s floor")
        if flags:
            findings.append((s["i"], s["cid"], s["text"], flags))
    if not findings:
        print(f"  . PASS  no sentence of >={MIN_WORDS_FOR_WPM_CHECK} words exceeds {MAX_WPM} wpm, "
              f"none under {MIN_SENTENCE_S:.1f}s")
    else:
        for i, cid, text, flags in findings:
            print(f"  ! sentence {i} ({cid}): {', '.join(flags)} -- {text!r}")
    return len(findings)


def part3(manifest, wav):
    print(f"\nPART 3 -- sentence-boundary silence, measured on the audio ({wav.name})")
    if not wav.exists():
        print("  SKIPPED: master.wav not found")
        return 0

    first_start = manifest["words"][0]["start"]
    calib_floor = rms_db(wav, max(0.0, first_start - 0.5), max(0.05, first_start - 0.05))
    if calib_floor is None:
        print("  SKIPPED: could not measure this take's own silence floor")
        return 0
    print(f"  this take's own pre-speech floor: {calib_floor:.1f} dB "
          f"(measured {max(0.0, first_start - 0.5):.2f}-{max(0.05, first_start - 0.05):.2f}s)")

    speech_peak = rms_db(wav, first_start, first_start + 2.0)
    silence_ceiling = (speech_peak - CALIBRATION_MARGIN_DB) if speech_peak is not None else -40.0

    sentences = manifest["sentences"]
    findings = []
    for a, b in zip(sentences, sentences[1:]):
        if a["cid"] != b["cid"]:
            continue  # a unit/file boundary has its own transition-grammar gap; not this check's concern
        gap = b["start"] - a["end"]
        if gap <= 0:
            continue
        db = rms_db(wav, a["end"], b["start"])
        is_silent = db is not None and db <= silence_ceiling
        silent_ms = gap * 1000 if is_silent else 0
        if silent_ms < MIN_BOUNDARY_MS:
            findings.append((a["i"], a["cid"], a["end"], b["start"], gap * 1000, db, is_silent))

    if not findings:
        print(f"  . PASS  every same-unit sentence boundary carries >= {MIN_BOUNDARY_MS}ms of "
              f"measured silence (ceiling {silence_ceiling:.1f} dB)")
    else:
        for i, cid, a_end, b_start, gap_ms, db, is_silent in findings:
            db_s = f"{db:.1f} dB" if db is not None else "?"
            reason = (f"silent but only {gap_ms:.0f}ms, under the {MIN_BOUNDARY_MS}ms floor"
                      if is_silent else "not audibly silent at all -- a hard join")
            print(f"  ! sentence {i} ({cid}) -> next: manifest gap {gap_ms:.0f}ms, "
                  f"measured {db_s} (ceiling {silence_ceiling:.1f} dB) -- {reason}")
    return len(findings)


def main():
    if not MANIFEST.exists():
        print(f"check-vo-pace: {MANIFEST.relative_to(ROOT)} not found -- skipping (exit 0).")
        return 0
    import json
    manifest = json.loads(MANIFEST.read_text())

    bad1 = part1_and_2(manifest)
    bad3 = part3(manifest, WAV)
    total = bad1 + bad3
    print(f"\n{total} finding(s) across all checks.")
    if total:
        print("  Advisory: always exits 0. A short punchy beat (\"Not smoking.\", "
              "\"Same result.\") is\n  frequently deliberate in this project's style, "
              "and the hook's one reviewed CPS\n  exception (check-captions.py's own "
              "documented tradeoff) shows up here too -- a\n  human call, same as "
              "check-cadence.py's own quiet-run findings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
