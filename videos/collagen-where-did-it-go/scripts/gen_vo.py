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

INTERNAL_SILENCE_MIN = 0.45   # a pause inside a unit must beat this to be compressed
SIL_KEEP = 0.03               # audio kept on each side of a compressed pause
POST_KEEP = 0.06              # kept after a word when no trailing silence is detected
TAIL_CLAMP = 0.25             # never keep more than this after a unit's last word
NOISE = "-45dB"
LIVE_AT_EOF_DB = -45.0
VO_TARGET_LUFS = -20.0
GAIN_CAP, GAIN_WARN = 5.0, 3.0
WPM_TARGET = 170.0
WPM_BAND = (160.0, 185.0)     # a read inside this band is left alone; Kimberly measures ~184
TEMPO_MAX = 1.15              # 1.265 read as hurried on the two-voice cut; 1.20 was its ship value
TEMPO_MIN = 0.92              # slowing further makes the formants audible
TEMPO = 1.00                  # set from `verify`'s printed decision; --tempo overrides
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
        sil = silences(wav)
        trailing = next((a for a, b in sil if b is None), None)
        if trailing is not None:
            keep = [w for w in words if w["start"] < trailing - 0.02]
            if len(keep) != len(words):
                dropped = [w["text"] for w in words if w not in keep]
                print(f"  {block:8s} dropped {len(words) - len(keep)} ASR word(s) inside the "
                      f"trailing silence from {trailing:.2f}s: {' '.join(dropped)[:60]!r}")
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
    ASR's digit form cost nothing."""
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


def load_blocks(require_asr=True):
    blocks = []
    for name, cids in BLOCKS:
        wav = raw_wav(name)
        if not wav.exists():
            raise SystemExit(f"missing raw take {wav.relative_to(ROOT)} -- fetch_vo.py first")
        if require_asr and not asr_path(name).exists():
            raise SystemExit(f"missing {asr_path(name).relative_to(ROOT)} -- run transcribe first")
        asr = json.loads(asr_path(name).read_text()) if asr_path(name).exists() else []
        blocks.append({"name": name, "cids": cids, "wav": wav, "dur": dur(wav),
                       "sil": silences(wav), "asr": asr,
                       "words": align_block(cids, asr) if asr else []})
    return blocks


# ---------------------------------------------------------------- the edit plan

def tail_cut(sil, last_end):
    """Raw time to stop keeping audio after a word ending at `last_end`."""
    for s, _e in sil:
        if s >= last_end - 0.02:
            return min(s, last_end + TAIL_CLAMP)
    return last_end + POST_KEEP


def plan_edit(blocks, tempo):
    """-> (seq, master_words) where seq is the ordered edit list of
    ("seg", block_idx, a, b) | ("sil", seconds) and master_words carries
    master-relative times for every scripted word."""
    T = tempo
    per_unit = []  # (block_idx, [words])
    for bi, b in enumerate(blocks):
        for cid in b["cids"]:
            ws = [w for w in b["words"] if w["cid"] == cid]
            if not ws:
                raise SystemExit(f"plan: unit {cid} has no aligned words in block "
                                 f"{b['name']} -- run `verify`")
            per_unit.append((bi, cid, ws))

    seq, open_seg, prev = [], None, None   # open_seg = [bi, a]; prev = (bi, last_end)

    def add_sil(s):
        if s > 0.004:
            seq.append(("sil", round(s, 3)))

    def close(bi, b):
        nonlocal open_seg
        if open_seg and b - open_seg[1] > 0.01:
            seq.append(("seg", open_seg[0], round(open_seg[1], 3), round(b, 3)))
        open_seg = None

    for bi, cid, ws in per_unit:
        first, last = ws[0], ws[-1]
        sil = blocks[bi]["sil"]
        if prev is None:
            head = first["start"] - LEAD_KEEP * T
            if head < 0:
                add_sil(LEAD_KEEP - first["start"] / T); start = 0.0
            else:
                start = head
        else:
            pbi, pend = prev
            gap = gap_into(cid)
            cut_a = tail_cut(blocks[pbi]["sil"], pend)
            ins = gap - LEAD_KEEP - (cut_a - pend) / T
            if ins < 0:
                cut_a = pend + max(POST_KEEP, (gap - LEAD_KEEP) * T)
                ins = max(0.0, gap - LEAD_KEEP - (cut_a - pend) / T)
            close(pbi, cut_a)
            add_sil(ins)
            start = first["start"] - LEAD_KEEP * T
            if bi == pbi:
                start = max(start, cut_a)
            start = max(start, 0.0)
        open_seg = [bi, start]
        # compress long pauses INSIDE the unit
        for w0, w1 in zip(ws, ws[1:]):
            for s, e in sil:
                if e is None:
                    continue
                if s >= w0["end"] - 0.02 and e <= w1["start"] + 0.02 and (e - s) > INTERNAL_SILENCE_MIN:
                    close(bi, s + SIL_KEEP)
                    add_sil(INTRA_GAP)
                    open_seg = [bi, e - SIL_KEEP]
        prev = (bi, last["end"])
    pbi, pend = prev
    close(pbi, tail_cut(blocks[pbi]["sil"], pend))

    # remap raw -> master
    cursor, bounds = 0.0, []
    for item in seq:
        if item[0] == "sil":
            cursor += item[1]
        else:
            _, bi, a, b = item
            bounds.append((bi, a, b, cursor))
            cursor += (b - a) / T

    def remap(bi, t):
        best = None
        for bbi, a, b, base in bounds:
            if bbi != bi:
                continue
            if a - 0.01 <= t <= b + 0.01:
                return round(base + (min(max(t, a), b) - a) / T, 3)
            edge = base if t < a else base + (b - a) / T
            d = abs(t - (a if t < a else b))
            if best is None or d < best[0]:
                best = (d, edge)
        return round(best[1], 3) if best else round(cursor, 3)

    master_words = []
    for bi, cid, ws in per_unit:
        for w in ws:
            master_words.append({**w, "start": remap(bi, w["start"]), "end": remap(bi, w["end"])})
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
        eof = eof_level(wav)
        if eof > LIVE_AT_EOF_DB:
            bad.append(f"ends mid-word (eof {eof:.1f} dB)")
        ws = b["words"]
        eq = sum(1 for w in ws if w["how"] == "equal")
        cov = eq / max(1, len(ws))
        if cov < 0.90:
            bad.append(f"alignment coverage {cov:.0%} < 90%")
        for w in ws:
            if w["norm"] in KEY_TERMS and w["how"] != "equal":
                bad.append(f"key term {w['text']!r} ({w['cid']}, ~{w['start']:.1f}s raw) not "
                           f"recognised by the ASR ({w['how']}) -- garble, re-roll")
        last_asr = max((w["end"] for w in b["asr"]), default=0.0)
        trailing = next((s for s, e in sil if e is None), b["dur"])
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
        for blk, msg in seam_findings(stats, names):
            print(f"      - SEAM: {msg}")
            findings.append((blk, msg))

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


def build_master(blocks, seq, tempo, gains, out):
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
    tmp = MASTER.with_suffix(".cut.wav")
    build_master(blocks, seq, tempo, gains, tmp)
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
