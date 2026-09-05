#!/usr/bin/env python3
"""QC narration pace from a voice manifest and the actual audio -- no
re-transcription. Reads the manifest the cut already produced rather than
re-deriving timings from the wav.

THREE CHECKS, and the third is the one worth having.

1. PER-SENTENCE WPM. Sentences of >=--min-words words above --max-wpm. The
   word-count floor is what keeps this from flagging every short punchy beat:
   a short sentence's wpm is dominated by fixed articulation overhead. Measured
   on a real take, "Now, the powder." at 3 words computes to 386 wpm and is not
   rushed to a listener, while "Keep only the studies without industry funding,
   and it is no longer statistically significant." at 16 words computing high
   IS a real speech-rate problem.

2. SUB---min-sentence-s SENTENCES. Flagged regardless of word count -- a
   sentence a viewer cannot finish reading as a caption before it changes state
   is a pace problem even if its wpm number looks unremarkable in isolation.

3. SENTENCE-BOUNDARY SILENCE, MEASURED ON THE AUDIO, NOT THE MANIFEST.
   `videos/collagen-where-did-it-go`'s review found 13 boundaries under 100ms
   in the manifest, of which only 2 were genuine hard joins -- the other 11
   carried 60-190ms of real silence the manifest's word timestamps simply did
   not capture. So the manifest cannot answer this question and the audio has
   to.

   A naive fixed dB gate over-reads on a take whose floor is true digital
   silence rather than room tone, so each boundary is measured against a
   threshold CALIBRATED ON THAT TAKE'S OWN measured speech level, not an
   absolute number carried in from another project's take. With per-scene
   manifests each take calibrates independently, which is the right behaviour
   when scenes were cut and gained separately.

FIELD CONTRACT
    python3 check-vo-pace.py <manifest.words.json> [more.words.json ...]
                             [--wav <path>] [--min-words 7] [--max-wpm 210]
                             [--min-sentence-s 1.0] [--min-boundary-ms 100]
                             [--calibration-margin-db 6.0] [--gate]

Advisory by default -- it reports, it does not gate. Several of the sentences
short enough to flag are deliberate punchy beats in an established style, and a
reviewed hook exception shows up here as an expected, not a surprising,
finding. Pass --gate to make it hard once a project has settled its exemptions.

MANIFEST SCHEMA -- the portability boundary. Each manifest needs `sentences`,
a list of objects carrying at least `start`, `end` and `text`. Two shapes are
handled, both real:

  * ONE MASTER MANIFEST for a continuous take, whose sentences carry their own
    `i`, `cid`, `first_word_idx` and `last_word_idx`
    (collagen-where-did-it-go's `assets/voice/master.words.json`).
  * PER-SCENE MANIFESTS, whose sentences carry only start/end/text and whose
    scene id is the manifest's own top-level `scene`
    (ectoin-survival-molecule's `assets/voice/NN.words.json`).

Word count per sentence comes from `first_word_idx`/`last_word_idx` when the
manifest carries them, otherwise from counting `words[]` entries inside the
sentence's own span. A manifest with neither is a hard, named failure rather
than a silent zero.

Each manifest is paired with `<stem>.wav` beside it (`master.words.json` ->
`master.wav`, `08.words.json` -> `08.wav`); --wav overrides that for a single
manifest. Part 3 only ever compares sentences WITHIN one manifest -- a boundary
between two files is a transition-grammar gap and is not this check's concern.

NOTE for zsh callers: a glob that matches nothing is a fatal error, not an
empty expansion, so `check-vo-pace.py assets/voice/*.words.json` aborts the
whole command on a project that has not cut its voice yet. Pass explicit paths
in a pipeline that must survive that.

Provenance: `videos/collagen-where-did-it-go` (all three checks and the
calibrated-ceiling method); the "read the manifest, don't re-derive it"
principle comes from `videos/ectoin-survival-molecule/scripts/check-vo.py`,
whose per-scene manifest shape this now also reads.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

MIN_WORDS_FOR_WPM_CHECK = 7
MAX_WPM = 210
MIN_SENTENCE_S = 1.0
MIN_BOUNDARY_MS = 100
CALIBRATION_MARGIN_DB = 6.0  # a boundary must be at least this far below the take's
                             # own measured speech level to count as "silent" -- not an
                             # absolute dB number, so it travels to a louder or quieter
                             # take without retuning.


def sh(*a):
    return subprocess.run([str(x) for x in a], capture_output=True, text=True, check=False)


def rms_db(wav, start, end):
    """Mean volume (dB) of [start,end) via ffmpeg's own volumedetect -- one
    process per span, but spans here are ~50-300ms so this stays fast.

    volumedetect logs its result at ffmpeg's INFO level, not error -- `-v error`
    (the usual convention for a quiet subprocess call) silently discards it
    along with everything else, so the call always returns None and Part 3
    reports SKIPPED without anyone noticing. `-v info` is required here
    specifically because the thing being measured IS an info-level log line.
    """
    r = sh("ffmpeg", "-nostdin", "-v", "info", "-ss", f"{start:.3f}", "-to", f"{end:.3f}",
           "-i", wav, "-af", "volumedetect", "-f", "null", "-")
    for line in r.stderr.splitlines():
        if "mean_volume" in line:
            return float(line.split(":")[1].strip().rstrip(" dB"))
    return None


def silence_ceiling(speech_peak_db, margin_db=CALIBRATION_MARGIN_DB):
    """The dB level below which a gap counts as silent, for THIS take.

    Exposed, with is_silent(), so a control fixture exercises the gate's own
    classification instead of recomputing the arithmetic beside it.
    """
    return -40.0 if speech_peak_db is None else speech_peak_db - margin_db


def is_silent(db, ceiling):
    return db is not None and db <= ceiling


def load(path, wav_override=None):
    """-> (normalised sentences, wav Path, label). Both manifest shapes in, one
    shape out: every sentence carries i / cid / start / end / n_words / text."""
    path = Path(path)
    d = json.loads(path.read_text())
    raw = d.get("sentences")
    if not raw:
        sys.exit(f"FATAL: {path} carries no `sentences` -- not a voice manifest, or "
                 f"cut by a pipeline that does not emit sentence spans.")
    words = d.get("words") or []
    default_cid = d.get("scene") or path.stem.replace(".words", "")

    out = []
    for k, s in enumerate(raw):
        if "first_word_idx" in s and "last_word_idx" in s:
            n = s["last_word_idx"] - s["first_word_idx"] + 1
        elif words:
            n = sum(1 for w in words if s["start"] <= w.get("start", -1) < s["end"])
        else:
            sys.exit(f"FATAL: {path} sentence {k} has neither word indices nor a "
                     f"`words` array -- word count cannot be established, and "
                     f"guessing it would make every wpm number here fiction.")
        out.append({"i": s.get("i", k), "cid": s.get("cid", default_cid),
                    "start": float(s["start"]), "end": float(s["end"]),
                    "n_words": n, "text": s.get("text", "")})

    wav = Path(wav_override) if wav_override else path.with_name(
        path.name.replace(".words.json", ".wav"))
    return out, wav, path.name


def part1_and_2(sentences, min_words, max_wpm, min_sentence_s):
    print("PART 1+2 -- per-sentence WPM and minimum duration (from the manifest)")
    findings = []
    for s in sentences:
        dur = s["end"] - s["start"]
        wpm = s["n_words"] / dur * 60 if dur > 0 else 0
        flags = []
        if s["n_words"] >= min_words and wpm > max_wpm:
            flags.append(f"{wpm:.0f}wpm > {max_wpm} ({s['n_words']} words)")
        if dur < min_sentence_s:
            flags.append(f"{dur:.2f}s < {min_sentence_s:.1f}s floor")
        if flags:
            findings.append((s["i"], s["cid"], s["text"], flags))
    if not findings:
        print(f"  . PASS  no sentence of >={min_words} words exceeds {max_wpm} wpm, "
              f"none under {min_sentence_s:.1f}s")
    else:
        for i, cid, text, flags in findings:
            print(f"  ! sentence {i} ({cid}): {', '.join(flags)} -- {text!r}")
    return len(findings)


def part3(sentences, wav, min_boundary_ms, margin_db):
    print(f"\nPART 3 -- sentence-boundary silence, measured on the audio ({wav.name})")
    if not wav.exists():
        print(f"  SKIPPED: {wav} not found")
        return 0

    first_start = sentences[0]["start"]
    calib_floor = rms_db(wav, max(0.0, first_start - 0.5), max(0.05, first_start - 0.05))
    if calib_floor is None:
        print("  SKIPPED: could not measure this take's own silence floor")
        return 0
    print(f"  this take's own pre-speech floor: {calib_floor:.1f} dB "
          f"(measured {max(0.0, first_start - 0.5):.2f}-{max(0.05, first_start - 0.05):.2f}s)")

    ceiling = silence_ceiling(rms_db(wav, first_start, first_start + 2.0), margin_db)

    findings = []
    for a, b in zip(sentences, sentences[1:]):
        if a["cid"] != b["cid"]:
            continue  # a unit boundary has its own transition-grammar gap
        gap = b["start"] - a["end"]
        if gap <= 0:
            continue
        db = rms_db(wav, a["end"], b["start"])
        silent = is_silent(db, ceiling)
        silent_ms = gap * 1000 if silent else 0
        if silent_ms < min_boundary_ms:
            findings.append((a["i"], a["cid"], gap * 1000, db, silent))

    if not findings:
        print(f"  . PASS  every same-unit sentence boundary carries >= {min_boundary_ms}ms "
              f"of measured silence (ceiling {ceiling:.1f} dB)")
    else:
        for i, cid, gap_ms, db, silent in findings:
            db_s = f"{db:.1f} dB" if db is not None else "?"
            reason = (f"silent but only {gap_ms:.0f}ms, under the {min_boundary_ms}ms floor"
                      if silent else "not audibly silent at all -- a hard join")
            print(f"  ! sentence {i} ({cid}) -> next: manifest gap {gap_ms:.0f}ms, "
                  f"measured {db_s} (ceiling {ceiling:.1f} dB) -- {reason}")
    return len(findings)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifests", nargs="+")
    ap.add_argument("--wav", help="override the sibling wav (single manifest only)")
    ap.add_argument("--min-words", type=int, default=MIN_WORDS_FOR_WPM_CHECK)
    ap.add_argument("--max-wpm", type=float, default=MAX_WPM)
    ap.add_argument("--min-sentence-s", type=float, default=MIN_SENTENCE_S)
    ap.add_argument("--min-boundary-ms", type=float, default=MIN_BOUNDARY_MS)
    ap.add_argument("--calibration-margin-db", type=float, default=CALIBRATION_MARGIN_DB)
    ap.add_argument("--gate", action="store_true", help="exit non-zero on findings")
    a = ap.parse_args()

    if a.wav and len(a.manifests) > 1:
        sys.exit("FATAL: --wav overrides one manifest's audio; pass a single manifest "
                 "with it, or let each manifest find its own sibling wav.")
    missing = [m for m in a.manifests if not Path(m).exists()]
    if missing:
        # A named manifest that is not there is a hard failure even in advisory
        # mode: "0 findings" on a file that does not exist is the shape of a
        # gate that has quietly stopped running.
        sys.exit(f"FATAL: manifest(s) not found: {', '.join(missing)}")

    total = 0
    for k, m in enumerate(a.manifests):
        sentences, wav, label = load(m, a.wav)
        if len(a.manifests) > 1:
            print(f"{'' if k == 0 else chr(10)}=== {label} ({len(sentences)} sentence(s))")
        total += part1_and_2(sentences, a.min_words, a.max_wpm, a.min_sentence_s)
        total += part3(sentences, wav, a.min_boundary_ms, a.calibration_margin_db)

    print(f"\n{total} finding(s) across all checks.")
    if total and not a.gate:
        print("  Advisory: exits 0. A short punchy beat is frequently deliberate, and a\n"
              "  reviewed caption-speed exception shows up here too -- a human call. Pass\n"
              "  --gate once the project has settled which of these it accepts.")
    return 1 if (total and a.gate) else 0


if __name__ == "__main__":
    sys.exit(main())
