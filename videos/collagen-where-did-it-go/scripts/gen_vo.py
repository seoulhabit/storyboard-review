#!/usr/bin/env python3
"""Transcribe, VERIFY and CUT the raw narration take(s) into ONE master
(assets/voice/master.wav) plus its word manifest (master.words.json).

    python3 scripts/gen_vo.py transcribe            # raw/<block>.wav -> raw/<block>.asr.json
    python3 scripts/gen_vo.py verify   [--tempo X]  # alignment, garble, rate decision
    python3 scripts/gen_vo.py cut      [--tempo X]  # master.wav + master.words.json
    python3 scripts/gen_vo.py fake                  # synthetic manifest + silent master
    python3 scripts/gen_vo.py plan     [--tempo X]  # print the edit list, no ffmpeg

Ported from videos/ectoin-survival-molecule/scripts/gen_vo.py and reduced to
this project's shape: however many raw blocks vo_lines.BLOCKS names (one, by
the user's confirmed choice; two as the fallback), `cut` concatenates them
into a single master so nothing downstream knows there were blocks at all.

WHAT `cut` DOES, and why every number is where it is:
  * word 1 lands at exactly timing.LEAD_KEEP (0.10s) -- narration starts
    before a viewer can leave; a raw take with a long lead is trimmed, a take
    that starts hot gets silence prepended.
  * at every UNIT seam the pause is REPLACED by transitions.gap_into(next):
    0.30 inside a file, 0.35 under an iris, 0.55 under the invert. This is
    what lets timing.walk() assert the manifest against the grammar instead
    of hoping the TTS paused the right amount.
  * pauses INSIDE a unit longer than INTERNAL_SILENCE_MIN are compressed to
    timing.INTRA_GAP; shorter ones are the narrator's own and are kept.
  * `atempo` (TEMPO) is applied per speech segment, so inserted gaps stay
    exact. The rate decision is printed by `verify`; it is not guessed.
  * the master is normalised to VO_TARGET_LUFS; the composition's FX chain
    and master-audio.py do the rest.

FAIL LOUD ON A BAD ALIGNMENT. A scripted key term (vo_words.KEY_TERMS) that
does not come back from the ASR as itself is a re-roll, never a caption
fix; a unit with no aligned words raises naming the unit.
"""
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOICE = ROOT / "assets" / "voice"
RAW = VOICE / "raw"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vo_lines import BLOCKS, TEXT, ORDER, WORDLESS
from vo_words import norm, merge_phrases, script_words, KEY_TERMS
from transitions import gap_into
from timing import LEAD_KEEP, TAIL, INTRA_GAP, END_CARD_HOLD, MASTER, MANIFEST

INTERNAL_SILENCE_MIN = 0.35   # a pause inside a unit must beat this to be compressed
SIL_KEEP = 0.03               # audio kept on each side of a compressed pause
# Whisper reports a word's END inside the following silence, routinely by
# 0.1-0.2s. The pause test used to require the detected silence to START after
# that reported end, so a real 0.9s pause whose silence began 0.15s "before" the
# word finished did not match and was kept in full. Measured consequence on this
# project's four takes: the cutter reclaimed 7s of 33s of dead air, and the
# piece projected at 2:53 against a 2:30 ceiling -- which would have been paid
# for with atempo on the whole read, or with a third TTS round. The fix is to
# intersect the silence with the inter-word gap instead of nesting it inside.
POST_KEEP = 0.06              # kept after a word when no trailing silence is detected
SNAP_MIN_SIL = 0.15           # a silence this long inside a word span is a real pause
MIN_WORD_S = 0.035            # no spoken word, even one letter, is shorter than this
MIN_MS_PER_CHAR = 8.0         # implied speaking rate above ~125 chars/s is not speech
MAX_MS_PER_CHAR = 175.0       # the mirror-image defect: a word (or run) that absorbs a
# real SILENCE ahead of it reads as impossibly SLOW, not fast -- "the" at 2773ms (07-film,
# this project's own take) and "As"/"we"/"age," together spanning 4.35s for what real audio
# shows is a ~2.3s sentence. Calibrated on this manifest's own legitimate slow endings
# ("upright." 149.6ms/char, "benefit." 133.6ms/char, both real, both plausible sentence-final
# deceleration) against the clear failures starting at 185ms/char and running past 900ms/char.
# Both floors exist because whisper's word-level timestamps can drift a whole run of
# words into a nearby silence gap without moving their SPAN, then snap_words_to_silence
# (correctly) relocates only the first word of the run out of that silence, leaving the
# rest to be squeezed edge-to-edge in ~18ms increments by the monotonic guard below it.
# Measured on this project's own master.words.json before this fix: 56 of 364 words
# (15.4%), in 39 separate runs spread from 0:05 to 1:55, at a CONSTANT ~18-19ms
# regardless of the word's length -- "a" and "getting" and "spectrum" all the same
# duration, which is the signature of a computed artifact, not measured audio. A
# threshold on chars/sec catches it without an absolute duration floor low enough to
# admit it; MIN_MS_PER_CHAR=8 gives a 4-letter word 32ms minimum and an 8-letter word
# 64ms, well under any real narration pace measured elsewhere in this manifest.
TAIL_SLOP = 0.30              # tolerance when locating a take's final silence
TAIL_CLAMP = 0.25             # fallback only: kept after the last word when NO
                              # trailing silence can be found at all
TAIL_MAX = 1.50               # sanity bound when a silence IS found
TAIL_MIN_SIL = 0.25           # a take's tail is a real pause, not a micro-gap
NOISE = "-45dB"
LIVE_AT_EOF_DB = -45.0
VO_TARGET_LUFS = -20.0
GAIN_CAP, GAIN_WARN = 5.0, 3.0
SHELF_FREQ, SHELF_CAP, SHELF_MIN = 3000, 3.0, 0.4   # brightness match across blocks
WPM_TARGET = 170.0
WPM_BAND = (160.0, 185.0)     # a read inside this band is left alone; Kimberly measures ~184
TEMPO_MAX = 1.15              # 1.265 read as hurried on the two-voice cut; 1.20 was its ship value
TEMPO_MIN = 0.92              # slowing further makes the formants audible
TEMPO = 1.08                  # set from `verify`'s printed decision; --tempo overrides.
                              # Measured on the four shipped takes: 1.00 gives 157.3 wpm
                              # and 2:24, 1.15 gives 178.5 wpm and 2:08. 1.08 lands 168.7
                              # wpm and 2:15 -- inside the brief's 165-175 band with the
                              # smallest correction that gets there.
RUNTIME_WINDOW = (120.0, 150.0)   # the brief's 2:00-2:30, measured on the finished root

# Word timing comes from whisper. large-v3 is already cached beside small.en
# (~/.cache/hyperframes/whisper/models) and its recognition is what matters
# here: `verify` REFUSES a take whose KEY_TERMS did not come back as
# themselves, so a model that mishears "daltons" costs a whole re-roll, not a
# caption fix. Timing quality between the two is comparable; recognition is not.
ASR_MODEL = "large-v3"
ASR_LANG = "en"
ASR_TIMEOUT_MS = "1800000"

# Two blocks are two performances. These are the differences an ear hears at the
# seam, in the order they are audible; `verify` measures each and names the
# outlier block rather than leaving the seam to a listening pass alone.
SEAM_MAX_DLUFS = 2.0          # LU, raw (before per-block gain)
SEAM_MAX_DWPM = 0.12          # fraction
SEAM_MAX_DCENTROID = 0.12     # fraction -- brightness
SEAM_MAX_DTILT = 3.0          # dB, low-band minus high-band
SEAM_MAX_DF0 = 0.08           # fraction -- ~1.3 semitones
SPOKEN = [c for c in ORDER if c not in WORDLESS]


# ---------------------------------------------------------------- ffmpeg glue

def sh(*a):
    return subprocess.run(a, capture_output=True, text=True)


def dur(p):
    o = sh("ffprobe", "-v", "error", "-show_entries", "format=duration",
           "-of", "csv=p=0", str(p)).stdout.strip()
    return float(o) if o else 0.0


def fmt(p):
    o = sh("ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
           "stream=sample_rate,channels", "-of", "csv=p=0", str(p)).stdout.strip()
    return o


def silences(p, noise=NOISE):
    """[(start, end_or_None)] -- end is None when silence runs to EOF."""
    r = sh("ffmpeg", "-nostdin", "-v", "info", "-i", str(p), "-af",
           f"silencedetect=noise={noise}:d=0.04", "-f", "null", "-")
    out, cur = [], None
    for line in r.stderr.splitlines():
        m = re.search(r"silence_start:\s*([\d.]+)", line)
        if m:
            cur = float(m.group(1)); continue
        m = re.search(r"silence_end:\s*([\d.]+)", line)
        if m and cur is not None:
            out.append((cur, float(m.group(1)))); cur = None
    if cur is not None:
        out.append((cur, None))
    return out


def eof_level(p, window=0.12):
    r = sh("ffmpeg", "-nostdin", "-sseof", f"-{window}", "-i", str(p), "-af",
           "volumedetect", "-f", "null", "-")
    m = re.search(r"mean_volume:\s*(-?[\d.]+) dB", r.stderr)
    return float(m.group(1)) if m else 0.0


def eof_level_at(p, t, window=0.12):
    """Level of the `window` seconds STARTING at `t` -- the audio the edit is
    about to discard. Measuring the window that ENDS at `t` answers a different
    question: it reads the tail of the final word, which is live by definition
    and says nothing about whether the take was cut short."""
    r = sh("ffmpeg", "-nostdin", "-ss", f"{max(0.0, t):.3f}", "-t", f"{window:.3f}",
           "-i", str(p), "-af", "volumedetect", "-f", "null", "-")
    m = re.search(r"mean_volume:\s*(-?[\d.]+|-inf) dB", r.stderr)
    if not m:
        return 0.0
    return float("-inf") if m.group(1) == "-inf" else float(m.group(1))


def integrated_lufs(p):
    err = sh("ffmpeg", "-nostdin", "-i", str(p), "-af", "ebur128", "-f", "null", "-").stderr
    tail = err[err.rindex("Summary:"):] if "Summary:" in err else err
    m = re.search(r"I:\s*(-?[\d.]+)\s*LUFS", tail)
    return float(m.group(1)) if m else None


def spectral_centroid(p):
    """Mean spectral centroid in Hz -- the single number that tracks how bright
    a take reads. A block recorded brighter than its neighbour is the seam a
    listener notices first, before either level or pace."""
    r = sh("ffmpeg", "-nostdin", "-v", "info", "-i", str(p), "-af",
           "aspectralstats=measure=centroid,ametadata=print:key=lavfi.aspectralstats.1.centroid",
           "-f", "null", "-")
    vals = [float(m) for m in re.findall(r"lavfi\.aspectralstats\.1\.centroid=([\d.]+)", r.stderr)]
    return round(sum(vals) / len(vals), 1) if vals else None


def band_tilt(p):
    """Low-band minus high-band RMS, in dB. Two takes at the same loudness can
    still sit differently in the mix; this is what that difference measures."""
    def rms(af):
        r = sh("ffmpeg", "-nostdin", "-v", "info", "-i", str(p), "-af", af + ",volumedetect",
               "-f", "null", "-")
        m = re.search(r"mean_volume:\s*(-?[\d.]+|-inf) dB", r.stderr)
        return None if not m or m.group(1) == "-inf" else float(m.group(1))
    lo, hi = rms("highpass=f=200,lowpass=f=1000"), rms("highpass=f=2000,lowpass=f=6000")
    return None if lo is None or hi is None else round(lo - hi, 2)


def median_f0(p):
    """Median voiced pitch, by autocorrelation over 40ms frames. numpy only --
    librosa is not installed on this host and one number does not justify it."""
    try:
        import numpy as np
    except ImportError:
        return None
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(p), "-f", "s16le",
                        "-ac", "1", "-ar", "16000", "-"], capture_output=True)
    x = np.frombuffer(r.stdout, dtype=np.int16).astype(np.float64) / 32768.0
    if x.size < 16000:
        return None
    N, sr = 640, 16000                       # 40ms frames
    lo, hi = int(sr / 400), int(sr / 70)     # 70-400 Hz search
    f0 = []
    for i in range(0, x.size - N, N):
        fr = x[i:i + N]
        if 20 * np.log10(max(1e-9, float(np.sqrt((fr ** 2).mean())))) < -35:
            continue                          # unvoiced or silent
        fr = fr - fr.mean()
        ac = np.correlate(fr, fr, mode="full")[N - 1:]
        if ac[0] <= 0:
            continue
        seg = ac[lo:hi]
        if seg.size == 0:
            continue
        lag = lo + int(np.argmax(seg))
        if ac[lag] / ac[0] > 0.3:
            f0.append(sr / lag)
    return round(float(np.median(f0)), 1) if f0 else None


def region_stats(path, start, dur):
    """Timbre of one span of a finished file. A block's whole span is a fair
    window; a four-second clip either side of a seam is not -- two differently
    worded four-second windows of the SAME voice measured 22% apart at the
    centroid here, which is a fact about the sentences, not the speaker."""
    tmp = path.with_suffix(".region.wav")
    r = sh("ffmpeg", "-y", "-nostdin", "-v", "error", "-i", str(path),
           "-af", f"atrim=start={start:.3f}:duration={dur:.3f},asetpts=PTS-STARTPTS",
           "-c:a", "pcm_s16le", str(tmp))
    if r.returncode or not tmp.exists():
        return {}
    out = {"lufs": integrated_lufs(tmp), "centroid": spectral_centroid(tmp),
           "tilt": band_tilt(tmp), "f0": median_f0(tmp)}
    tmp.unlink(missing_ok=True)
    return out


def block_stats(wav, words):
    n = len(words)
    span = (words[-1]["end"] - words[0]["start"]) if n > 1 else 0.0
    return {"lufs": integrated_lufs(wav), "wpm": round(n / max(0.01, span) * 60, 1),
            "centroid": spectral_centroid(wav), "tilt": band_tilt(wav), "f0": median_f0(wav),
            "duration": round(dur(wav), 3)}


def seam_findings(stats, names):
    """Adjacent-block differences that would be audible as a change of speaker
    rather than a change of subject. Returns [(block, message)]."""
    out = []
    for i in range(len(stats) - 1):
        a, b = stats[i], stats[i + 1]
        pair = f"{names[i]}->{names[i+1]}"

        def rel(k):
            va, vb = a.get(k), b.get(k)
            if va in (None, 0) or vb is None:
                return None
            return abs(va - vb) / abs(va)

        far = names[i] if abs(a.get("wpm", 0)) < abs(b.get("wpm", 0)) else names[i + 1]
        if a.get("lufs") is not None and b.get("lufs") is not None:
            d = abs(a["lufs"] - b["lufs"])
            if d > SEAM_MAX_DLUFS:
                out.append((far, f"{pair}: {d:.2f} LU apart before gain (max {SEAM_MAX_DLUFS})"))
        for key, cap, label in (("wpm", SEAM_MAX_DWPM, "pace"), ("centroid", SEAM_MAX_DCENTROID, "brightness"),
                                ("f0", SEAM_MAX_DF0, "pitch")):
            d = rel(key)
            if d is not None and d > cap:
                out.append((far, f"{pair}: {label} differs by {d*100:.1f}% (max {cap*100:.0f}%)"))
        if a.get("tilt") is not None and b.get("tilt") is not None:
            d = abs(a["tilt"] - b["tilt"])
            if d > SEAM_MAX_DTILT:
                out.append((far, f"{pair}: spectral tilt {d:.2f} dB apart (max {SEAM_MAX_DTILT})"))
    return out


# ---------------------------------------------------------------- addressing

def raw_wav(block):
    return RAW / f"{block}.wav"


def asr_path(block):
    return RAW / f"{block}.asr.json"


# ---------------------------------------------------------------- transcribe

def cmd_transcribe(argv):
    """Transcribe every block that does not already have a transcript. Passing
    --force re-does them all; whisper large-v3 is minutes per block on this
    host, so re-running after fetching ONE new take should cost one block."""
    ok = True
    force = "--force" in argv
    for block, _cids in BLOCKS:
        wav = raw_wav(block)
        if not wav.exists():
            print(f"  MISSING raw take for block {block}: {wav.relative_to(ROOT)}")
            ok = False; continue
        if asr_path(block).exists() and not force:
            print(f"  {block:8s} transcript already present -- skipping (--force to redo)")
            continue
        model = argv[argv.index("--model") + 1] if "--model" in argv else ASR_MODEL
        print(f"  {block:8s} transcribing with whisper {model} (this is CPU-bound; "
              f"pass --model small.en to trade recognition for speed)")
        r = sh("hyperframes", "transcribe", str(wav), "--engine", "whisper",
               "--model", model, "--language", ASR_LANG, "--json",
               "--timeout", ASR_TIMEOUT_MS, "-d", str(ROOT))
        if r.returncode != 0:
            print(f"  transcribe FAILED for {block}: {(r.stderr or r.stdout).strip()[:400]}")
            ok = False; continue
        info = None
        for line in reversed(r.stdout.strip().splitlines()):
            try:
                info = json.loads(line); break
            except Exception:
                continue
        if not info:
            print(f"  transcribe: no JSON summary for {block}: {r.stdout[:300]}")
            ok = False; continue
        src = Path(info.get("transcriptPath", ""))
        if not src.exists():
            print(f"  transcribe: {block} reported {src} but it does not exist")
            ok = False; continue
        data = json.loads(src.read_text())
        words = data["words"] if isinstance(data, dict) and "words" in data else data
        words = [{"text": w["text"], "start": float(w["start"]), "end": float(w["end"])}
                 for w in words if str(w.get("text", "")).strip()]
        src.unlink(missing_ok=True)
        # DEFENSIVE RESCALE (ectoin, confirmed): whisper can report word times
        # running PAST the physical end of the file. Only that impossible case
        # is rescaled; a slight under-run (untimed trailing silence) is normal.
        real = dur(wav)
        last_end = max((w["end"] for w in words), default=0.0)
        if last_end > real + 0.05 and last_end > 0:
            f = real / last_end
            for w in words:
                w["start"] = round(w["start"] * f, 3); w["end"] = round(w["end"] * f, 3)
            print(f"  {block:8s} WARNING: ASR timestamps ran to {last_end:.2f}s past the "
                  f"{real:.2f}s file -- rescaled by {f:.4f}")
        # DROP ASR WORDS THAT SIT IN SILENCE. Whisper fills trailing digital
        # silence with plausible speech: block B's take ends at 25.24s and the
        # transcript carried "Thanks for watching!" at 30.0-31.48s, inside 6.09s
        # of measured silence. Left in, a hallucination pollutes the script<->ASR
        # alignment and can drag a real word's timestamp with it. Anything
        # starting after the file's final trailing silence begins is not speech.
        keep, dropped_at = drop_silent_tail(words, wav)
        if dropped_at is not None:
            print(f"  {block:8s} dropped {len(words) - len(keep)} ASR word(s) inside the "
                  f"trailing silence from {dropped_at:.2f}s: "
                  f"{' '.join(w['text'] for w in words[len(keep):])[:60]!r}")
            words = keep
        asr_path(block).write_text(json.dumps(words))
        print(f"  {block:8s} {len(words):4d} ASR words  file {real:.2f}s  {fmt(wav)}  "
              f"-> {asr_path(block).relative_to(ROOT)}")
    return 0 if ok else 1


# ---------------------------------------------------------------- alignment

def align_block(cids, asr):
    """Align every SCRIPTED word of `cids` (in order) onto ASR word times.

    Returns [{"cid","text","norm","start","end","how","sent"}] with block-
    relative times; `how` is "equal" | "replace" | "interp". Both sides are
    merged through vo_words.PHRASES first so a spoken numeral phrase and the
    ASR's digit form cost nothing.

    A physically implausible span here (an "equal" match whisper simply
    mistimed) is NOT filtered in this function -- see
    repair_implausible_runs, run once on the finished block after
    snap_words_to_silence. Filtering it here and marking it "interp" was
    tried and reverted: it corrupts verify's alignment-coverage and
    end-drift gates, which must keep measuring whether the ASR matched the
    right WORD, not whether whisper's TIMING for that word was trustworthy
    -- a different question, answered later and without touching `how`."""
    disp, owner, sent_ix = [], [], []
    for cid in cids:
        ws = script_words(TEXT[cid])
        si = 0
        for w in ws:
            disp.append(w); owner.append(cid); sent_ix.append(si)
            if re.search(r"[.?!]$", w):
                si += 1
    toks = [norm(w) for w in disp]
    merged_s, spans_s = merge_phrases(toks)
    asr_toks = [norm(w["text"]) for w in asr]
    merged_a, spans_a = merge_phrases(asr_toks)
    a_span = [(asr[i0]["start"], asr[i1]["end"]) for i0, i1 in spans_a]

    sm = difflib.SequenceMatcher(None, merged_s, merged_a, autojunk=False)
    got = {}   # merged script idx -> (start, end, how)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                got[i1 + k] = (*a_span[j1 + k], "equal")
        elif tag == "replace" and j2 > j1:
            n = max(i2 - i1, 1)
            for k in range(i2 - i1):
                jj = min(j1 + (k * (j2 - j1)) // n, j2 - 1)
                got[i1 + k] = (*a_span[jj], "replace")

    out = [None] * len(disp)
    for mi, (i0, i1) in enumerate(spans_s):
        if mi not in got:
            continue
        s, e, how = got[mi]
        n = i1 - i0 + 1
        if n == 1:
            out[i0] = [s, e, how]
        else:
            lens = [max(1, len(norm(disp[i]))) for i in range(i0, i1 + 1)]
            tot, cur = sum(lens), s
            for i, L in zip(range(i0, i1 + 1), lens):
                nxt = cur + (e - s) * L / tot
                out[i] = [cur, nxt, how]; cur = nxt
    # interpolate anything the ASR dropped, by character length between neighbours
    i = 0
    while i < len(out):
        if out[i] is not None:
            i += 1; continue
        j = i
        while j < len(out) and out[j] is None:
            j += 1
        prev_end = out[i - 1][1] if i > 0 else None
        next_start = out[j][0] if j < len(out) else None
        lens = [max(1, len(norm(disp[k]))) for k in range(i, j)]
        if prev_end is None and next_start is None:
            raise SystemExit("align: no ASR words aligned at all -- is this the right take?")
        if prev_end is None:
            est = sum(lens) * 0.075
            prev_end = max(0.0, next_start - est)
        if next_start is None:
            next_start = prev_end + sum(lens) * 0.075
        span, tot, cur = next_start - prev_end, sum(lens), prev_end
        for k, L in zip(range(i, j), lens):
            nxt = cur + span * L / tot
            out[k] = [cur, nxt, "interp"]; cur = nxt
        i = j
    words = []
    for k, w in enumerate(disp):
        s, e, how = out[k]
        words.append({"cid": owner[k], "text": w, "norm": norm(w), "sent": sent_ix[k],
                      "start": round(s, 3), "end": round(max(e, s + 0.02), 3), "how": how})
    # monotonic guard: a replace/interp can never run backwards
    for a, b in zip(words, words[1:]):
        if b["start"] < a["end"] - 0.005:
            b["start"] = a["end"]
            b["end"] = max(b["end"], b["start"] + 0.02)
    return words


def snap_words_to_silence(words, sil):
    """Move each word's start/end to where the audio actually starts and stops.

    Whisper reports a word's END inside the following silence -- measured at up
    to 0.69s on these takes. Every downstream number is derived from these
    times: which pauses are long enough to compress, where a block is cut, and
    what timing.walk() asserts the seam grammar against. Left uncorrected they
    caused, in order: a cutter that reclaimed 7s of 33s of dead air, then a
    compression that removed a region the manifest still had a word inside, so
    the word "So" was cut from the audio while its time survived in the
    manifest. Snapping to measured silence makes the ASR gaps equal the real
    pauses, after which the compression can stay strictly inside them.

    Only silences of at least SNAP_MIN_SIL count, so a stop consonant inside a
    word is never mistaken for the end of it.

    This is per-word and does not know about its neighbours -- when a RUN of
    consecutive words is each independently mistimed into the SAME silence
    (whisper put both "Think" and "of" inside one gap, not just "Think"), this
    pass alone snaps them to the identical instant, and the overrun guard
    below then drags every FOLLOWING word forward too, one at a time --
    including a word the silence never touched at all ("building." moved from
    19.540 to 19.636 here even though it never overlapped the silence, purely
    because the guard chased it down the chain). A dragged word can still
    have a perfectly plausible-looking duration, so a duration check alone
    (`repair_implausible_runs`, after this) cannot tell it apart from a
    genuinely correct one -- it isn't wrong in LENGTH, it's wrong in
    POSITION. So only a word the GUARD had to push is marked `_snapped`
    (stripped before the manifest is written) -- a clean, non-colliding
    single-word relocation earlier in this function is not, by itself,
    evidence of anything wrong. The guard only ever fires on an actual
    overlap, which is exactly the collision signature: "Think" (a lone,
    isolated relocation) is never touched by it here and stays trusted;
    every word from "of" through "building." is, because each one only
    moved by being shoved off whatever collided into it. The repair pass
    treats a `_snapped` neighbour as untrustworthy, not just an
    implausibly-short one."""
    moved = 0
    for w in words:
        for a, b in sil:
            if b is None:
                b = w["end"]
            if b - a < SNAP_MIN_SIL:
                continue
            if a <= w["start"] and w["end"] <= b:
                # The whole word sits inside measured silence, so its time is
                # simply wrong -- the aligner put "Think" at 18.100-18.530
                # inside a silence running 18.098-19.106, a second before the
                # word is actually spoken. Move it, keeping its length.
                d = w["end"] - w["start"]
                w["start"] = round(b, 3); w["end"] = round(b + d, 3); moved += 1
            elif w["start"] < a < w["end"]:        # audio stops inside this word
                w["end"] = round(a, 3); moved += 1
            elif a <= w["start"] < b < w["end"]:   # audio starts late in this word
                w["start"] = round(b, 3); moved += 1
        if w["end"] <= w["start"]:
            w["end"] = round(w["start"] + 0.02, 3)
    # a moved word must not overrun the one after it -- and THIS is the
    # collision signature: only a word the guard actually had to push away
    # from something is marked, see the docstring above.
    for x, y in zip(words, words[1:]):
        if y["start"] < x["end"]:
            y["start"] = x["end"]
            y["end"] = max(y["end"], round(y["start"] + 0.02, 3))
            y["_snapped"] = True
    return moved


def drop_silent_tail(words, wav):
    """Remove ASR words that begin inside the take's trailing silence.

    Whisper fills digital silence with plausible speech: block B's take ends at
    25.24s and the transcript carried "Thanks for watching!" at 30.0-31.5s. The
    first version of this guard looked for a silence running to EOF and missed
    it, because that file has a click on its final 60ms -- so the silence ended
    at 31.44s of a 31.50s file and did not match. A trailing silence is one that
    reaches the END OF THE FILE, not one that reaches the last sample."""
    if not words:
        return words, None
    total = dur(wav)
    trailing = None
    for a, b in silences(wav):
        if b is None or b >= total - 0.25:
            trailing = a if trailing is None else min(trailing, a)
    if trailing is None:
        return words, None
    keep = [w for w in words if w["start"] < trailing - 0.02]
    return keep, (trailing if len(keep) != len(words) else None)


def repair_implausible_runs(words, sil=None):
    """Re-time any run of words whose measured span implies an impossible
    speaking rate -- too FAST (MIN_WORD_S / MIN_MS_PER_CHAR) or too SLOW
    (MAX_MS_PER_CHAR) -- using the same character-weighted interpolation
    already used for a word ASR never found at all.

    Run this AFTER alignment and after snap_words_to_silence, on the FINISHED
    block, because either stage can produce the defect on its own: alignment
    can trust a genuinely too-fast "equal" ASR match, and snapping a run of
    words that are each independently mistimed into the SAME silence gap
    pins every one of them to the identical instant, which the overrun guard
    then packs into slivers regardless of how many words were stuck there --
    "Think of your skin as a" collapsed to five ~18ms words this way.
    Checking the physical plausibility of the RESULT, not which mechanism
    produced it, catches both in one place. Measured before this existed:
    56 of 364 words (15.4%) in 39 runs, spread from 0:05 to 1:55.

    The MAX side is the mirror image: a word (or run) that absorbs a real
    SILENCE ahead of it reads as impossibly slow, not fast -- 24 of 350 words
    on this project's own re-recorded take, "As"/"we"/"age," together
    spanning 4.35s where the real audio holds a ~2.3s sentence after a
    genuine pause. Blindly character-weighting a bad run's WHOLE anchor-to-
    anchor window would just relocate the same error: the pause is real and
    belongs to nobody's word. So when `sil` is available, any qualifying
    silence found inside [prev_end, next_start] moves prev_end to its end
    first -- the run is redistributed only across what's left, the same
    principle tail_cut() uses to find a take's true trailing silence."""
    n = len(words)

    def implausible(w):
        chars = max(1, len(w["norm"]))
        dur = w["end"] - w["start"]
        return (dur < max(MIN_WORD_S, chars * MIN_MS_PER_CHAR / 1000)
                or dur > chars * MAX_MS_PER_CHAR / 1000)

    # A word snap_words_to_silence moved -- for ANY reason, including being
    # dragged forward by its overrun guard -- is not a trustworthy anchor
    # even when its own duration looks plausible: it isn't wrong in LENGTH,
    # it's wrong in POSITION, and a duration check alone cannot see that.
    # "building." passed the duration check at 754ms/8 chars and was still
    # 96ms later than it should have been, purely from chasing the collision
    # in front of it. A run is therefore bounded by a word that is BOTH
    # plausible AND untouched by snapping -- the only kind whose position is
    # still exactly what alignment originally (and correctly) computed.
    def untrustworthy(w):
        return implausible(w) or w.get("_snapped", False)

    fixed = 0
    i = 0
    while i < n:
        if not untrustworthy(words[i]):
            i += 1; continue
        j = i
        while j < n and untrustworthy(words[j]):
            j += 1
        prev_end = words[i - 1]["end"] if i > 0 else None
        next_start = words[j]["start"] if j < n else None
        lens = [max(1, len(words[k]["norm"])) for k in range(i, j)]
        if prev_end is None and next_start is None:
            i = j; continue   # nothing to anchor on -- leave rather than guess
        if prev_end is None:
            prev_end = max(0.0, next_start - sum(lens) * 0.075)
        if next_start is None:
            next_start = prev_end + sum(lens) * 0.075
        if sil and next_start is not None:
            for a, b in sil:
                if b is None:
                    continue
                if prev_end <= a and b <= next_start and (b - a) >= SNAP_MIN_SIL:
                    prev_end = max(prev_end, b)
        span = max(next_start - prev_end, 0.02 * len(lens))
        tot, cur = sum(lens), prev_end
        for k, L in zip(range(i, j), lens):
            nxt = cur + span * L / tot
            words[k]["start"] = round(cur, 3); words[k]["end"] = round(nxt, 3)
            # `how` is left as ASR reported it -- this repairs TIMING, not
            # whether the ASR recognised the right WORD. Overwriting it to
            # "interp" here once corrupted verify's alignment-coverage and
            # end-drift gates, which exist to catch a take that drifted
            # off-script and must keep measuring text match, not timing
            # confidence -- a different question this pass has no opinion on.
            cur = nxt
        fixed += (j - i)
        i = j
    if fixed:
        for x, y in zip(words, words[1:]):
            if y["start"] < x["end"]:
                y["start"] = x["end"]
                y["end"] = max(y["end"], round(y["start"] + 0.02, 3))
    for w in words:
        w.pop("_snapped", None)
    return fixed


def load_blocks(require_asr=True):
    blocks = []
    for name, cids in BLOCKS:
        wav = raw_wav(name)
        if not wav.exists():
            raise SystemExit(f"missing raw take {wav.relative_to(ROOT)} -- fetch_vo.py first")
        if require_asr and not asr_path(name).exists():
            raise SystemExit(f"missing {asr_path(name).relative_to(ROOT)} -- run transcribe first")
        asr = json.loads(asr_path(name).read_text()) if asr_path(name).exists() else []
        sil_b = silences(wav)
        asr, dropped_at = drop_silent_tail(asr, wav)
        if dropped_at is not None:
            print(f"  {name:8s} ignoring ASR words after the trailing silence at {dropped_at:.2f}s "
                  f"(whisper hallucinates into digital silence)")
        words = align_block(cids, asr) if asr else []
        snapped = snap_words_to_silence(words, sil_b)
        if snapped:
            print(f"  {name:8s} snapped {snapped} word boundary/ies to the measured silence")
        repaired = repair_implausible_runs(words, sil_b) if words else 0
        if repaired:
            print(f"  {name:8s} re-timed {repaired} word(s) with an impossible speaking "
                  f"rate (see repair_implausible_runs)")
        blocks.append({"name": name, "cids": cids, "wav": wav, "dur": dur(wav),
                       "sil": sil_b, "asr": asr, "words": words})
    return blocks


# ---------------------------------------------------------------- the edit plan

def tail_cut(sil, last_end, last_start=None):
    """Raw time to stop keeping audio after a word ending at `last_end`.

    The ASR reports a word's END inside the following silence -- measured at up
    to 0.69s on this project's takes, where the audio is below -45 dB from
    49.99s while whisper puts the last word's end at 50.68s. Requiring the
    silence to begin after the reported end therefore kept most of a second of
    dead air on every block, and made the take look as though it ended live.
    The search starts at last_end - TAIL_SLOP but never before the word's own
    start, so a pause BEFORE the final word can never be mistaken for its tail."""
    floor = last_end - TAIL_SLOP
    if last_start is not None:
        floor = max(floor, last_start)
    for s, _e in sil:
        # A micro-gap between two syllables is not the end of the take. Without
        # this, the search caught a 40ms gap inside the final word and cut there.
        if _e is not None and _e - s < TAIL_MIN_SIL:
            continue
        if s >= floor:
            # SEARCH from floor (the ASR overruns a word's end into the silence,
            # so the silence that belongs to this word can start "before" it),
            # but never RETURN a point before the word's reported end. Cutting
            # earlier is acoustically free -- the audio is already below -45 dB --
            # but it moves the word's end in the manifest, and every seam start
            # downstream is computed from that end. Measured: the first iris
            # then wanted a first word at 5.950s and got 5.634s, and
            # timing.walk() refused the build. Clamping to last_end + 0.25
            # instead was the opposite error: it truncated A3's "uncertain.",
            # which really does run to 40.87s.
            return min(max(s, last_end), last_end + TAIL_MAX)
    return last_end + POST_KEEP


def plan_edit(blocks, tempo):
    """-> (seq, master_words, speech_end).

    CONSTRUCTED, not remapped. The old form laid out the edit in RAW time and
    mapped each word through it afterwards, so the master's seam gaps were
    whatever the arithmetic happened to produce -- and with an aligner whose
    word times disagree with the audio by up to a second, that was repeatedly
    not the gap the grammar asked for. timing.walk() then refused the build,
    correctly.

    Here the MASTER timeline is the thing being built. A running cursor tracks
    master time; each unit's first word is placed at exactly
    `previous last word + gap_into(unit)`, and the silence inserted before it is
    whatever makes that true. The grammar holds by construction, so the assert
    downstream can only fail if the audio itself cannot supply the gap.

    seq is ("seg", block_idx, raw_a, raw_b) | ("sil", seconds); master_words
    carries master-relative times for every scripted word.
    """
    T = tempo
    per_unit = []
    for bi, blk in enumerate(blocks):
        for cid in blk["cids"]:
            ws = [w for w in blk["words"] if w["cid"] == cid]
            if not ws:
                raise SystemExit(f"plan: unit {cid} has no aligned words in block "
                                 f"{blk['name']} -- run `verify`")
            per_unit.append((bi, cid, ws))

    seq, master_words = [], []
    cursor = 0.0     # master time
    prev = None      # (block, raw_last_end, raw_last_start, master_last_end, raw_closed_at)

    def emit_sil(sec):
        nonlocal cursor
        if sec > 0.004:
            seq.append(("sil", round(sec, 3)))
            cursor += sec

    def emit_seg(bi, ra, rb):
        """Keep raw [ra, rb] of block bi. Returns (ra, rb, raw->master fn)."""
        nonlocal cursor
        base = cursor
        if rb - ra <= 0.01:
            return None
        seq.append(("seg", bi, round(ra, 3), round(rb, 3)))
        cursor += (rb - ra) / T
        return (ra, rb, lambda t: round(base + (min(max(t, ra), rb) - ra) / T, 3))

    for ui, (bi, cid, ws) in enumerate(per_unit):
        first, last = ws[0], ws[-1]
        sil = blocks[bi]["sil"]
        # where the NEXT unit's audio begins, when it shares this take: this
        # unit's tail may not run into it, or the next unit's first word ends up
        # inside a segment that was already emitted and its master time is
        # whatever the clamp produced.
        nxt = per_unit[ui + 1] if ui + 1 < len(per_unit) else None
        next_first = nxt[2][0]["start"] if (nxt and nxt[0] == bi) else None

        if prev is None:
            open_a = max(0.0, first["start"] - LEAD_KEEP * T)
            emit_sil(LEAD_KEEP - (first["start"] - open_a) / T)
        else:
            pbi, pend, pstart, pmaster_end, pclosed = prev
            want_first = pmaster_end + gap_into(cid)
            open_a = first["start"] - LEAD_KEEP * T
            if bi == pbi:
                open_a = max(open_a, pclosed)
            open_a = max(open_a, 0.0)
            lead = max(0.0, (first["start"] - open_a) / T)
            if cursor + lead > want_first:      # more lead-in audio than the gap allows
                keep = max(0.0, want_first - cursor)
                open_a = max(first["start"] - keep * T, pclosed if bi == pbi else 0.0)
                open_a = max(open_a, 0.0)
                lead = max(0.0, (first["start"] - open_a) / T)
            emit_sil(want_first - lead - cursor)

        # the unit's audio, with its long internal pauses compressed
        maps = []
        for w0, w1 in zip(ws, ws[1:]):
            for sa, sb in sil:
                if sb is None:
                    continue
                lo, hi = max(sa, w0["end"]), min(sb, w1["start"])
                if hi - lo > INTERNAL_SILENCE_MIN and lo + SIL_KEEP > open_a + 0.02:
                    m = emit_seg(bi, open_a, lo + SIL_KEEP)
                    if m:
                        maps.append(m)
                    emit_sil(INTRA_GAP)
                    open_a = hi - SIL_KEEP
        closed_at = max(tail_cut(sil, last["end"], last["start"]), last["end"])
        if next_first is not None:
            closed_at = min(closed_at, max(last["end"], next_first - LEAD_KEEP * T))
        m = emit_seg(bi, open_a, closed_at)
        if m:
            maps.append(m)
        if not maps:
            raise SystemExit(f"plan: unit {cid} produced no audio segment")

        def to_master(t):
            for ra, rb, fn in maps:
                if ra - 0.01 <= t <= rb + 0.01:
                    return fn(t)
            return maps[0][2](t) if t < maps[0][0] else maps[-1][2](t)

        for w in ws:
            master_words.append({**w, "start": to_master(w["start"]), "end": to_master(w["end"])})
        prev = (bi, last["end"], last["start"], master_words[-1]["end"], closed_at)

    return seq, master_words, round(cursor, 3)


def summarise(master_words, speech_end):
    n = len(master_words)
    first, last = master_words[0]["start"], master_words[-1]["end"]
    wpm = n / max(0.01, last - first) * 60
    return n, first, last, round(wpm, 1)


def rate_decision(wpm, projected_total=None):
    """Pace AND runtime. A take inside the natural band is left alone even when
    a nominal target would nudge it, because atempo on a good read costs more
    than the seconds it buys -- but a projected runtime outside the brief's
    window overrides that, since the window is the deliverable."""
    lo, hi = WPM_BAND
    runtime_ok = projected_total is None or RUNTIME_WINDOW[0] <= projected_total <= RUNTIME_WINDOW[1]
    note = "" if projected_total is None else f" projected runtime {projected_total:.1f}s"
    if lo <= wpm <= hi and runtime_ok:
        return 1.00, f"TEMPO = 1.00 ({wpm:.1f} wpm inside the {lo:.0f}-{hi:.0f} band;{note})"
    if not runtime_ok and projected_total is not None:
        want = RUNTIME_WINDOW[1] if projected_total > RUNTIME_WINDOW[1] else RUNTIME_WINDOW[0]
        need = projected_total / want
        if TEMPO_MIN <= need <= TEMPO_MAX:
            return round(need, 3), (f"TEMPO = {need:.3f} to land {projected_total:.1f}s inside "
                                    f"{RUNTIME_WINDOW[0]:.0f}-{RUNTIME_WINDOW[1]:.0f}s ({wpm:.1f} wpm)")
    need = WPM_TARGET / max(1.0, wpm)
    if need < TEMPO_MIN:
        return None, (f"need {need:.3f} < {TEMPO_MIN}: the take is far too fast to slow "
                      f"transparently. Round 2: regenerate with a negative speech_rate.")
    if need <= TEMPO_MAX:
        return round(need, 2), f"TEMPO = {need:.2f} (atempo; inside the {TEMPO_MAX} cap)"
    sr = int(min(40, max(5, round((need - 1) * 100))))
    return None, (f"need {need:.3f} > {TEMPO_MAX}: do NOT stretch this far. Round 2: regenerate "
                  f"with speech_rate={sr} (linear assumption; re-measure), then TEMPO in "
                  f"[{TEMPO_MIN}, {TEMPO_MAX}].")


def projected_runtime(speech_end, tempo=1.0):
    """What the ROOT will measure once this master is cut: the last word, plus
    the tail, plus the curtain's own seam gap, plus the end card."""
    from transitions import KIND
    return speech_end + TAIL + KIND["curtain"][1] + END_CARD_HOLD


# ---------------------------------------------------------------- verify

def cmd_verify(argv):
    tempo = _tempo(argv)
    blocks = load_blocks()
    findings = []
    for b in blocks:
        bad = []
        wav = b["wav"]
        sil = b["sil"]
        if any(s <= 0.01 and (e is None or e >= b["dur"] - 0.01) for s, e in sil):
            bad.append("SILENT take")
        # Measure at the point the CUTTER will end this block, not at the end of
        # the delivered file. A take with six seconds of trailing silence and a
        # click on its final frame is not "cut off mid-word": tail_cut lands the
        # edit at the silence and the click never reaches the master. Checking
        # the file's last 120ms answers a question nobody asked.
        ws = b["words"]
        cut_at = tail_cut(b["sil"], ws[-1]["end"], ws[-1]["start"]) if ws else b["dur"]
        eof = eof_level_at(wav, cut_at)
        if eof > LIVE_AT_EOF_DB:
            bad.append(f"still live where the cut lands ({eof:.1f} dB at {cut_at:.2f}s) -- "
                       f"the take ran out before the sentence did")
        eq = sum(1 for w in ws if w["how"] == "equal")
        cov = eq / max(1, len(ws))
        if cov < 0.90:
            bad.append(f"alignment coverage {cov:.0%} < 90%")
        # Advisory, not a finding: repair_implausible_runs fixes what it can
        # anchor confidently, but a residual case can be genuinely ambiguous
        # from the waveform alone (a fast, unstressed phrase right after a
        # real pause, where the pause boundary itself is uncertain) -- surface
        # it for a human ear rather than silently guessing further or, worse,
        # silently shipping it unlisted the way the original bug did.
        residual = [w for w in ws if (w["end"] - w["start"])
                    < max(MIN_WORD_S, max(1, len(w["norm"])) * MIN_MS_PER_CHAR / 1000)]
        if residual:
            print(f"  {b['name']:8s} ADVISORY: {len(residual)} word(s) still imply an "
                  f"implausible speaking rate after repair -- listen: "
                  + ", ".join(f"{w['text']!r}@{w['start']:.2f}s" for w in residual))
        for w in ws:
            if w["norm"] in KEY_TERMS and w["how"] != "equal":
                bad.append(f"key term {w['text']!r} ({w['cid']}, ~{w['start']:.1f}s raw) not "
                           f"recognised by the ASR ({w['how']}) -- garble, re-roll")
        # Where the audio really stops: the trailing silence, by the same
        # definition drop_silent_tail uses (reaches the end of the FILE, not the
        # last sample). Comparing against b["dur"] flagged every take whose
        # hallucinated tail had just been trimmed.
        last_asr = max((w["end"] for w in b["asr"]), default=0.0)
        total_b = b["dur"]
        trailing = total_b
        for a, e in sil:
            if e is None or e >= total_b - 0.25:
                trailing = min(trailing, a)
        if last_asr < trailing - 0.5:
            bad.append(f"ASR under-run: last ASR word ends {last_asr:.2f}s, audio runs to {trailing:.2f}s")
        # A DRIFT AT THE END is the dangerous shape: a take can score acceptable
        # coverage overall and still be missing the payoff. Measured on this
        # project: a 1933-char block was faithful for 241 of 310 words and then
        # improvised 25 seconds of generic copy, taking the entire climax with
        # it. Check the tail separately from the whole.
        tail = ws[-12:]
        tail_eq = sum(1 for w in tail if w["how"] == "equal") / max(1, len(tail))
        if tail_eq < 0.75:
            bad.append(f"take drifts off-script at the END: only {tail_eq:.0%} of the last "
                       f"{len(tail)} words aligned (script tail: "
                       f"{' '.join(w['text'] for w in tail[-6:])!r}) -- re-roll, and shorten the block")
        interp = sum(1 for w in ws if w["how"] == "interp")
        print(f"  {b['name']:8s} {'FLAGGED' if bad else 'ok':8s} words={len(ws)} equal={cov:.0%} "
              f"interp={interp} eof={eof:.1f}dB dur={b['dur']:.2f}s {fmt(wav)}")
        for msg in bad:
            print(f"      - {msg}")
            findings.append((b["name"], msg))
    # SEAM CONTINUITY. Two blocks are two performances; these are the four
    # differences an ear reads as a change of speaker rather than of subject.
    if len(blocks) > 1:
        stats = [block_stats(b["wav"], b["words"]) for b in blocks]
        names = [b["name"] for b in blocks]
        print(f"\n  {'block':8s} {'LUFS':>7s} {'wpm':>7s} {'centroid':>9s} {'tilt dB':>8s} {'F0 Hz':>7s}")
        for nm, st in zip(names, stats):
            print(f"  {nm:8s} {st['lufs'] if st['lufs'] is not None else float('nan'):7.1f} "
                  f"{st['wpm']:7.1f} {st['centroid'] or 0:9.1f} {st['tilt'] or 0:8.2f} {st['f0'] or 0:7.1f}")
        seams = seam_findings(stats, names)
        for blk, msg in seams:
            print(f"      - SEAM: {msg}")
        if seams:
            print("        `cut` applies a per-block level AND brightness match; these are the\n"
                  "        RAW takes. The corrected values are measured on the master and\n"
                  "        asserted by check-final.py, so this is a heads-up, not a re-roll.")

    seq, mw, speech_end = plan_edit(blocks, 1.0)
    n, first, last, wpm = summarise(mw, speech_end)
    proj = projected_runtime(speech_end)
    print(f"\n  dry run at TEMPO 1.00: {n} words, first {first:.3f}s, last {last:.3f}s, "
          f"master ~{speech_end + TAIL:.1f}s, {wpm} wpm, projected runtime {proj:.1f}s "
          f"({int(proj // 60)}:{proj % 60:05.2f})")
    t, msg = rate_decision(wpm, proj)
    print(f"  rate decision: {msg}")
    if tempo != 1.0:
        seq, mw, speech_end = plan_edit(blocks, tempo)
        n, first, last, wpm2 = summarise(mw, speech_end)
        print(f"  at --tempo {tempo}: last {last:.3f}s, master ~{speech_end + TAIL:.1f}s, {wpm2} wpm, "
              f"projected runtime {projected_runtime(speech_end):.1f}s")
    if findings:
        print(f"\n  {len(findings)} finding(s) -- re-roll the flagged block(s):")
        for b, m in findings:
            print(f"    {b}: {m}")
        return 1
    print("\n  All blocks pass.")
    return 0


# ---------------------------------------------------------------- cut

def _tempo(argv):
    if "--tempo" in argv:
        return float(argv[argv.index("--tempo") + 1])
    return TEMPO


def build_master(blocks, seq, tempo, gains, out, shelves=None):
    inputs = []
    for b in blocks:
        inputs += ["-i", str(b["wav"])]
    parts, labels = [], []
    for k, item in enumerate(seq):
        if item[0] == "sil":
            parts.append(f"anullsrc=r=48000:cl=mono:d={item[1]:.3f},"
                         f"aformat=sample_fmts=s16:sample_rates=48000:channel_layouts=mono[p{k}]")
        else:
            _, bi, a, b = item
            chain = [f"[{bi}:a]atrim=start={a:.3f}:end={b:.3f}", "asetpts=PTS-STARTPTS",
                     "aformat=sample_fmts=s16:sample_rates=48000:channel_layouts=mono"]
            if abs(tempo - 1.0) > 1e-6:
                chain.append(f"atempo={tempo:.4f}")
            # PIN the segment to its planned length. atempo's output is not
            # exactly input/rate -- it rounds at its own frame boundaries, and
            # across 61 segments that rounding accumulated to 0.44s by the end
            # of the master. Every word time, caption cue and @w() anchor is
            # computed from the PLAN, so a master that runs long against the
            # plan silently slides the whole back half of the piece out of sync
            # with its own narration. Trimming and padding each segment to the
            # planned duration makes the plan true by construction.
            want = (b - a) / tempo
            chain += [f"atrim=start=0:duration={want:.4f}", "asetpts=PTS-STARTPTS",
                      f"apad=whole_dur={want:.4f}", f"atrim=start=0:duration={want:.4f}",
                      "asetpts=PTS-STARTPTS"]
            if shelves and abs(shelves[bi]) >= SHELF_MIN:
                chain.append(f"highshelf=f={SHELF_FREQ}:g={shelves[bi]:.2f}")
            if abs(gains[bi]) > 0.05:
                chain.append(f"volume={gains[bi]:.2f}dB")
            parts.append(",".join(chain) + f"[p{k}]")
        labels.append(f"[p{k}]")
    parts.append(f"{''.join(labels)}concat=n={len(labels)}:v=0:a=1[cat];"
                 f"[cat]apad=pad_dur={TAIL}[out]")
    r = sh("ffmpeg", "-y", "-nostdin", "-v", "error", *inputs,
           "-filter_complex", ";".join(parts), "-map", "[out]",
           "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le", str(out))
    if r.returncode != 0 or not out.exists():
        raise SystemExit(f"ffmpeg master build failed: {r.stderr[:800]}")


def write_manifest(master_words, tempo, source, blocks_meta, lufs):
    sents, cur = [], []
    for w in master_words:
        if cur and (w["cid"] != cur[0]["cid"] or w["sent"] != cur[0]["sent"]):
            sents.append(cur); cur = []
        cur.append(w)
    if cur:
        sents.append(cur)
    sentences = [{"i": i, "cid": s[0]["cid"], "start": s[0]["start"], "end": s[-1]["end"],
                  "first_word_idx": master_words.index(s[0]),
                  "last_word_idx": master_words.index(s[-1]),
                  "text": " ".join(x["text"] for x in s)} for i, s in enumerate(sents)]
    scenes = []
    for k, cid in enumerate(SPOKEN):
        idx = [i for i, w in enumerate(master_words) if w["cid"] == cid]
        ws = [master_words[i] for i in idx]
        nxt = SPOKEN[k + 1] if k + 1 < len(SPOKEN) else None
        scenes.append({"cid": cid, "first_word_idx": idx[0], "last_word_idx": idx[-1],
                       "first_sent_idx": min(s["i"] for s in sentences if s["cid"] == cid),
                       "last_sent_idx": max(s["i"] for s in sentences if s["cid"] == cid),
                       "start": ws[0]["start"], "end": ws[-1]["end"],
                       "gap_after": gap_into(nxt) if nxt else None,
                       "wpm": round(len(ws) / max(0.01, ws[-1]["end"] - ws[0]["start"]) * 60, 1)})
    n, first, last, wpm = summarise(master_words, None)
    words = [{"i": i, "text": w["text"], "norm": w["norm"], "start": w["start"], "end": w["end"],
              "cid": w["cid"], "sent": w["sent"], "interp": w["how"] == "interp", "how": w["how"]}
             for i, w in enumerate(master_words)]
    manifest = {"version": 1, "source": source, "tempo": tempo, "lead_keep": LEAD_KEEP,
                "tail": TAIL, "duration": round(dur(MASTER), 3), "sample_rate": 48000,
                "channels": 1, "lufs": lufs, "wpm": wpm, "blocks": blocks_meta,
                "words": words, "sentences": sentences, "scenes": scenes}
    MANIFEST.write_text(json.dumps(manifest, indent=1))
    return manifest


def cmd_cut(argv):
    tempo = _tempo(argv)
    blocks = load_blocks()
    seq, master_words, speech_end = plan_edit(blocks, tempo)
    # per-block gain equalises blocks to each other; the final pass lands the master
    raw_lufs = [integrated_lufs(b["wav"]) for b in blocks]
    mean = sum(x for x in raw_lufs if x is not None) / max(1, len(raw_lufs))
    gains = [max(-GAIN_CAP, min(GAIN_CAP, mean - (x if x is not None else mean))) for x in raw_lufs]
    # SPECTRAL match, for the same reason as the level match. Four takes are four
    # performances; block B came back 22% brighter at the centroid than its
    # neighbours, which reads as a different voice at the seam even when the
    # loudness matches. A shelf toward the group's median tilt is the smallest
    # correction that addresses it, and it is measured afterwards rather than
    # assumed (see the table `cut` prints).
    tilts = [band_tilt(b["wav"]) for b in blocks]
    known = sorted(t for t in tilts if t is not None)
    med = known[len(known) // 2] if known else None
    shelves = []
    for t in tilts:
        g = 0.0 if (t is None or med is None) else max(-SHELF_CAP, min(SHELF_CAP, -(med - t)))
        shelves.append(round(g, 2) if abs(g) >= SHELF_MIN else 0.0)
    print(f"  {'block':8s} {'raw LUFS':>9s} {'gain dB':>8s} {'tilt dB':>8s} {'shelf dB':>9s}")
    for i, b in enumerate(blocks):
        print(f"  {b['name']:8s} {raw_lufs[i] if raw_lufs[i] is not None else float('nan'):9.1f} "
              f"{gains[i]:8.2f} {tilts[i] if tilts[i] is not None else float('nan'):8.2f} {shelves[i]:9.2f}")
    tmp = MASTER.with_suffix(".cut.wav")
    build_master(blocks, seq, tempo, gains, tmp, shelves)
    I = integrated_lufs(tmp)
    g = max(-GAIN_CAP, min(GAIN_CAP, VO_TARGET_LUFS - I)) if I is not None else 0.0
    if abs(g) > 0.05:
        r = sh("ffmpeg", "-y", "-nostdin", "-v", "error", "-i", str(tmp), "-af",
               f"volume={g:.2f}dB", "-c:a", "pcm_s16le", str(MASTER))
        if r.returncode:
            raise SystemExit(r.stderr[:400])
        tmp.unlink()
    else:
        tmp.replace(MASTER)
    lufs = integrated_lufs(MASTER)
    meta = [{"name": b["name"], "raw": str(b["wav"].relative_to(ROOT)), "cids": b["cids"],
             "raw_lufs": raw_lufs[i], "gain_db": round(gains[i] + g, 2),
             "asr_words": len(b["asr"]),
             "stats": block_stats(b["wav"], b["words"])} for i, b in enumerate(blocks)]
    # where the two performances meet, in MASTER time, plus a listening excerpt.
    # A measurement can say the blocks match; only an ear can say the seam does
    # not sound like a second narrator.
    if len(blocks) > 1:
        qc = ROOT / "renders" / "qc"
        qc.mkdir(parents=True, exist_ok=True)
        for i in range(1, len(blocks)):
            seam_at = next((w["start"] for w in master_words
                            if w["cid"] == blocks[i]["cids"][0]), None)
            if not seam_at:
                continue
            meta[i]["master_seam"] = round(seam_at, 3)
            name = f"seam-{blocks[i-1]['name']}-{blocks[i]['name']}.wav"
            sh("ffmpeg", "-y", "-nostdin", "-v", "error", "-ss", f"{max(0, seam_at - 3):.3f}",
               "-t", "6", "-i", str(MASTER), str(qc / name))
            print(f"  block seam {blocks[i-1]['name']} -> {blocks[i]['name']} at {seam_at:.3f}s "
                  f"-> renders/qc/{name} (listen before shipping)")
    # The numbers check-final asserts are measured on the MASTER, after the level
    # and brightness match -- the raw-take numbers describe what was corrected,
    # not what ships. Each block's own span is the window.
    bounds = []
    for i, b in enumerate(blocks):
        first = next((w["start"] for w in master_words if w["cid"] == b["cids"][0]), None)
        last = max((w["end"] for w in master_words if w["cid"] in b["cids"]), default=None)
        bounds.append((first, last))
    for i, (a, z) in enumerate(bounds):
        if a is not None and z is not None and z - a > 2.0:
            meta[i]["stats_master"] = region_stats(MASTER, a, z - a)
            meta[i]["span"] = [round(a, 3), round(z, 3)]
    print(f"  {'block':8s} {'master span':>16s} {'LUFS':>7s} {'centroid':>9s} {'tilt dB':>8s} {'F0 Hz':>7s}")
    for i, b in enumerate(blocks):
        st = meta[i].get("stats_master") or {}
        sp = meta[i].get("span") or [0, 0]
        print(f"  {b['name']:8s} {sp[0]:7.2f}-{sp[1]:7.2f} {st.get('lufs') or 0:7.1f} "
              f"{st.get('centroid') or 0:9.1f} {st.get('tilt') or 0:8.2f} {st.get('f0') or 0:7.1f}")
    m = write_manifest(master_words, tempo, "blocks" if len(blocks) > 1 else "master", meta,
                       round(lufs, 1) if lufs is not None else None)
    _report(m, seq)
    return 0


def _report(m, seq=None):
    print(f"  master.wav  {m['duration']:.3f}s  {m['lufs']} LUFS  tempo {m['tempo']}  "
          f"source={m['source']}  {len(m['words'])} words  {m['wpm']} wpm overall")
    print(f"  word 1 at {m['words'][0]['start']:.3f}s (LEAD_KEEP {LEAD_KEEP})")
    if seq:
        print(f"  edit list: {sum(1 for s in seq if s[0]=='seg')} segments, "
              f"{sum(1 for s in seq if s[0]=='sil')} inserted gaps")
    print(f"  {'unit':14s} {'start':>8s} {'end':>8s} {'words':>5s} {'wpm':>6s}  gap_after")
    for s in m["scenes"]:
        print(f"  {s['cid']:14s} {s['start']:8.3f} {s['end']:8.3f} "
              f"{s['last_word_idx']-s['first_word_idx']+1:5d} {s['wpm']:6.1f}  {s['gap_after']}")


def cmd_plan(argv):
    tempo = _tempo(argv)
    blocks = load_blocks()
    seq, mw, speech_end = plan_edit(blocks, tempo)
    for item in seq:
        print("  ", item)
    n, first, last, wpm = summarise(mw, speech_end)
    print(f"  {n} words, first {first:.3f}, last {last:.3f}, master ~{speech_end + TAIL:.2f}s, {wpm} wpm")
    return 0


# ---------------------------------------------------------------- fake

def cmd_fake(argv):
    """A synthetic manifest at WPM_TARGET so every generator and `hyperframes
    check` can run before any TTS credit is spent. The silent master carries a
    banner in every generated file; the gates refuse to pass it."""
    VOICE.mkdir(parents=True, exist_ok=True)
    words, t = [], LEAD_KEEP
    for k, cid in enumerate(SPOKEN):
        disp = script_words(TEXT[cid])
        n_sent = sum(1 for w in disp if re.search(r"[.?!]$", w)) or 1
        weights = [0.5 + len(norm(w)) / 10 for w in disp]
        speech = len(disp) * 60 / WPM_TARGET - (n_sent - 1) * INTRA_GAP
        kf = speech / sum(weights)
        si = 0
        for w, wt in zip(disp, weights):
            d = kf * wt
            words.append({"cid": cid, "text": w, "norm": norm(w), "sent": si,
                          "start": round(t, 3), "end": round(t + d, 3), "how": "fake"})
            t += d
            if re.search(r"[.?!]$", w):
                si += 1; t += INTRA_GAP
        t -= INTRA_GAP   # the last sentence's pause is replaced by the seam gap
        nxt = SPOKEN[k + 1] if k + 1 < len(SPOKEN) else None
        if nxt:
            t += gap_into(nxt)
    total = round(t + TAIL, 3)
    r = sh("ffmpeg", "-y", "-nostdin", "-v", "error", "-f", "lavfi",
           "-i", "anullsrc=r=48000:cl=mono", "-t", f"{total:.3f}",
           "-c:a", "pcm_s16le", str(MASTER))
    if r.returncode:
        raise SystemExit(r.stderr[:400])
    m = write_manifest(words, 1.0, "fake", [{"name": "fake", "cids": SPOKEN}], None)
    print("  FAKE manifest -- not for delivery. Generated files will carry a banner.")
    _report(m)
    return 0


def main():
    cmds = {"transcribe": cmd_transcribe, "verify": cmd_verify, "cut": cmd_cut,
            "fake": cmd_fake, "plan": cmd_plan}
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        print(__doc__); return 2
    return cmds[sys.argv[1]](sys.argv[2:])


if __name__ == "__main__":
    sys.exit(main())
