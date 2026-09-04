#!/usr/bin/env python3
"""Download/measure, TRANSCRIBE, VERIFY and CUT the act-level VO blocks into
per-scene WAVs + word manifests.

    python3 scripts/gen_vo.py transcribe [--from-takes]
    python3 scripts/gen_vo.py verify     [--from-takes]
    python3 scripts/gen_vo.py cut        [--from-takes]

Normal mode reads assets/voice/acts/<block>.wav (one per vo_lines.BLOCKS entry,
downloaded from the Higgsfield generate_audio_batch result) and CUTS each into
the scenes it covers.

--from-takes is the validation / fallback mode: it treats each of the 29
EXISTING per-scene takes (assets/voice/NN.wav, one scene per file already) as
its own one-scene "block", so `cut` degenerates to trim + internal-gap
compression + loudness normalise, with no cross-scene alignment needed except
for 09-exclusion, whose "block" is takes 09+10 concatenated -- this is what
proves the merge mechanism (two old takes -> one new scene) without spending
any TTS credit. Running this against real act-level blocks and against
--from-takes exercises the exact same `cut_scene`/`remap_words` code path.

WHY A REAL ALIGNMENT STEP. An act-level block's transcript is Whisper's ASR
output for several scenes' worth of speech end to end; scene boundaries have
to be located inside it. The scripted words (vo_lines.LINES, normalised
through vo_words.norm) are aligned against the ASR words with
difflib.SequenceMatcher, which tolerates the odd ASR insertion/substitution
without losing sync -- the failure mode of a naive index-count split is a
single ASR dropped word silently shifting every later scene's cut point.

FAIL LOUD ON ZERO ALIGNMENT. A scene with no aligned ASR words (block
truncated, or garbled beyond recognition) raises immediately naming the
scene and block, rather than cutting a zero-length or garbage clip -- run
`verify` first; it is designed to catch exactly this before `cut` runs.
"""
import difflib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOICE = ROOT / "assets" / "voice"
ACTS = VOICE / "acts"
TAKES_STAGE = ACTS / "_takes"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vo_lines import LINES, TEXT, BLOCKS, TAKES_MAP, EVIDENCE
from vo_words import script_words, norm

LEAD_KEEP = 0.10   # audio kept before the first word (fade-in finishes before onset)
TAIL = 0.25        # uniform trailing digital silence appended to every scene clip
INTRA_GAP = 0.22   # authored pause between sentences inside a scene, after compression
INTRA_GAP_OVERRIDES = {"20-twelve": 0.45, "21-verdict": 0.40, "19-limits": 0.35}
INTERNAL_SILENCE_MIN = 0.45   # an internal gap has to beat this to be compressed at all
VO_TARGET_LUFS = -20.0
GAIN_CAP, GAIN_WARN = 5.0, 3.0
NOISE = "-45dB"
EXPECT_ECTOIN = {"ectoin", "ectoins"}
RARE = re.compile(r"\b[Ee]ct[a-z]*\b|\b[a-z]*ecto[a-z]*\b")


# ---------------------------------------------------------------- ffmpeg glue

def sh(*a):
    return subprocess.run(a, capture_output=True, text=True)


def dur(p):
    o = sh("ffprobe", "-v", "error", "-show_entries", "format=duration",
           "-of", "csv=p=0", str(p)).stdout.strip()
    return float(o) if o else 0.0


def silences(p, noise=NOISE):
    """[(start, end_or_None)] -- end is None when silence runs to EOF."""
    r = sh("ffmpeg", "-v", "info", "-i", str(p), "-af",
           f"silencedetect=noise={noise}:d=0.04", "-f", "null", "-")
    out, cur = [], None
    for line in r.stderr.splitlines():
        m = re.search(r"silence_start:\s*([\d.]+)", line)
        if m:
            cur = float(m.group(1))
            continue
        m = re.search(r"silence_end:\s*([\d.]+)", line)
        if m and cur is not None:
            out.append((cur, float(m.group(1))))
            cur = None
    if cur is not None:
        out.append((cur, None))
    return out


def eof_level(p, window=0.12):
    r = sh("ffmpeg", "-sseof", f"-{window}", "-i", str(p), "-af",
           "volumedetect", "-f", "null", "-")
    m = re.search(r"mean_volume:\s*(-?[\d.]+) dB", r.stderr)
    return float(m.group(1)) if m else 0.0


LIVE_AT_EOF_DB = -45.0


def analyse(p):
    total = dur(p)
    sil = silences(p)
    is_silent = any(s <= 0.01 and (e is None or e >= total - 0.01) for s, e in sil)
    lead = 0.0
    if sil and sil[0][0] <= 0.01 and sil[0][1] is not None:
        lead = sil[0][1]
    return lead, eof_level(p), is_silent


def integrated_lufs(p):
    err = sh("ffmpeg", "-nostdin", "-i", str(p), "-af", "ebur128", "-f", "null", "-").stderr
    tail = err[err.rindex("Summary:"):] if "Summary:" in err else err
    m = re.search(r"I:\s*(-?[\d.]+)\s*LUFS", tail)
    return float(m.group(1)) if m else None


# ---------------------------------------------------------------- addressing

def blocks_for(from_takes):
    """[(block_name, [scene_cid, ...])]. --from-takes: one pseudo-block per
    scene, so `cut` never has to split across scenes except for 09-exclusion."""
    if from_takes:
        return [(cid, [cid]) for cid, _ in LINES]
    return BLOCKS


def _concat_takes(cid, nums):
    if len(nums) == 1:
        return VOICE / f"{nums[0]:02d}.wav"
    # Cached: once staged, reused even after `cut` has overwritten the scene's
    # OWN output slot (assets/voice/NN.wav for its lead take number) on a later
    # run -- without this cache a re-run would try to re-source from a take
    # file that `cut` had already replaced with the merged, trimmed clip.
    TAKES_STAGE.mkdir(parents=True, exist_ok=True)
    out = TAKES_STAGE / f"{cid}.wav"
    if out.exists():
        return out
    listfile = TAKES_STAGE / f"{cid}.concat.txt"
    listfile.write_text("".join(f"file '{(VOICE / f'{n:02d}.wav').resolve()}'\n" for n in nums))
    r = sh("ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
           "-i", str(listfile), "-ac", "1", "-ar", "48000", str(out))
    if r.returncode != 0 or not out.exists():
        raise SystemExit(f"concat of takes {nums} for {cid} failed: {r.stderr[:400]}")
    return out


def source_wav(block_name, from_takes):
    if from_takes:
        return _concat_takes(block_name, TAKES_MAP[block_name])
    return ACTS / f"{block_name}.wav"


def transcript_path(block_name, from_takes):
    d = TAKES_STAGE if from_takes else ACTS
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{block_name}.words.json"


def scene_n(cid):
    return int(cid.split("-")[0])


def scene_wav(cid):
    return VOICE / f"{scene_n(cid):02d}.wav"


def scene_words_path(cid):
    return VOICE / f"{scene_n(cid):02d}.words.json"


# ---------------------------------------------------------------- transcribe

def cmd_transcribe(from_takes):
    ok = True
    for block_name, _cids in blocks_for(from_takes):
        wav = source_wav(block_name, from_takes)
        if not wav.exists():
            print(f"  MISSING audio for block {block_name}: {wav}")
            ok = False
            continue
        r = sh("hyperframes", "transcribe", str(wav), "--engine", "whisper",
               "--model", "small.en", "--json", "--timeout", "300000", "-d", str(ROOT))
        if r.returncode != 0:
            print(f"  transcribe FAILED for {block_name}: {(r.stderr or r.stdout).strip()[:300]}")
            ok = False
            continue
        try:
            info = json.loads(r.stdout.strip().splitlines()[-1])
        except Exception:
            print(f"  transcribe: could not parse JSON summary for {block_name}: {r.stdout[:300]}")
            ok = False
            continue
        src = Path(info["transcriptPath"])
        if not src.exists():
            print(f"  transcribe: {block_name} reported {src} but it does not exist")
            ok = False
            continue
        words = json.loads(src.read_text())
        src.unlink(missing_ok=True)

        # DEFENSIVE RESCALE. Confirmed on the 09-exclusion concat (48kHz mono,
        # ffmpeg-reencoded from two 24kHz stereo takes): hyperframes/whisper
        # reported durationSeconds 25.56s and a last word ending at 25.56s for
        # a file ffprobe measures at 23.871s -- word timestamps extending
        # PAST the physical end of the audio, a ~7% uniform stretch. A normal
        # take instead under-reports slightly (trailing silence the ASR does
        # not timestamp), which is expected and left alone. Only the
        # impossible case -- a word ending after the file does -- is rescaled.
        real_dur = dur(wav)
        last_end = max((w["end"] for w in words), default=0.0)
        if last_end > real_dur + 0.05 and last_end > 0:
            factor = real_dur / last_end
            for w in words:
                w["start"] = round(w["start"] * factor, 3)
                w["end"] = round(w["end"] * factor, 3)
            print(f"  {block_name:16s} WARNING: ASR timestamps ran to {last_end:.2f}s "
                  f"past the {real_dur:.2f}s file -- rescaled by {factor:.4f}")

        dst = transcript_path(block_name, from_takes)
        dst.write_text(json.dumps(words))
        print(f"  {block_name:16s} {info['wordCount']:3d} words  "
              f"{info['durationSeconds']:6.2f}s (file {real_dur:.2f}s) -> {dst.relative_to(ROOT)}")
    return 0 if ok else 1


# ---------------------------------------------------------------- verify

def cmd_verify(from_takes):
    findings = []
    for block_name, cids in blocks_for(from_takes):
        wav = source_wav(block_name, from_takes)
        tp = transcript_path(block_name, from_takes)
        if not wav.exists() or not tp.exists():
            findings.append((block_name, "missing audio or transcript -- run transcribe first"))
            continue
        lead, eof_db, is_silent = analyse(wav)
        block_bad = []
        if is_silent:
            block_bad.append("SILENT")
        if eof_db > LIVE_AT_EOF_DB:
            block_bad.append(f"ends mid-word (eof {eof_db:.1f}dB)")
        words = json.loads(tp.read_text())
        text = " ".join(w["text"] for w in words)
        bad_terms = sorted({w for w in RARE.findall(text) if w.lower() not in EXPECT_ECTOIN})
        if bad_terms:
            block_bad.append(f"garbled ectoin: {bad_terms}")
        script_n = sum(len(script_words(TEXT[c])) for c in cids)
        if len(words) < 0.6 * script_n:
            block_bad.append(f"looks truncated: {len(words)} ASR words vs {script_n} scripted")
        status = "FLAGGED" if block_bad else "ok"
        print(f"  {block_name:16s} {status:8s} words={len(words):4d}/{script_n:<4d} "
              f"eof={eof_db:6.1f}dB lead={lead:.2f}s  {'; '.join(block_bad)}")
        for msg in block_bad:
            findings.append((block_name, msg))
    if findings:
        print(f"\n  {len(findings)} finding(s) across "
              f"{len({b for b, _ in findings})} block(s) -- re-roll only those:")
        for b, msg in findings:
            print(f"    {b}: {msg}")
        return 1
    print("\n  All blocks pass.")
    return 0


# ---------------------------------------------------------------- cut

def align_block(cids, words):
    """cid -> (first_asr_idx, last_asr_idx) covering that scene's script."""
    script_tokens, owner = [], []
    for cid in cids:
        toks = script_words(TEXT[cid])
        script_tokens += toks
        owner += [cid] * len(toks)
    asr_norm = [norm(w["text"]) for w in words]
    sm = difflib.SequenceMatcher(None, script_tokens, asr_norm, autojunk=False)
    mapping = {}
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                mapping[i1 + k] = j1 + k
        elif tag == "replace" and j2 > j1:
            n = max(i2 - i1, 1)
            for k in range(i2 - i1):
                mapping[i1 + k] = min(j1 + (k * (j2 - j1)) // n, j2 - 1)
    per_scene = {}
    for cid in cids:
        idxs = [i for i, o in enumerate(owner) if o == cid]
        asr_idxs = sorted({mapping[i] for i in idxs if i in mapping})
        if not asr_idxs:
            raise SystemExit(
                f"cut: scene {cid} has no aligned ASR words in its block -- "
                f"truncated or garbled. Run `gen_vo.py verify` first.")
        per_scene[cid] = (asr_idxs[0], asr_idxs[-1])
    return per_scene


def scene_bounds(cids, words, per_scene, sil):
    """cid -> (cut_start, cut_end), block-relative, clamped against neighbours."""
    bounds = {}
    for i, cid in enumerate(cids):
        a0, a1 = per_scene[cid]
        first_w, last_w = words[a0], words[a1]
        raw_start = max(0.0, first_w["start"] - LEAD_KEEP)
        tail_end = last_w["end"]
        for s, _e in sil:
            if s >= last_w["end"] - 0.02:
                tail_end = s
                break
        if i > 0:
            prev_last = words[per_scene[cids[i - 1]][1]]["end"]
            raw_start = max(raw_start, prev_last + 0.05)
        if i + 1 < len(cids):
            next_first = words[per_scene[cids[i + 1]][0]]["start"]
            tail_end = min(tail_end, next_first - 0.05)
        bounds[cid] = (round(raw_start, 3), round(max(tail_end, raw_start + 0.05), 3))
    return bounds


def internal_gaps(sil, start, end, min_gap):
    gaps = [(s, e) for s, e in sil
            if e is not None and s > start + 0.02 and e < end - 0.02 and (e - s) > min_gap]
    return sorted(gaps)


def cut_scene(cid, block_wav, span, sil, out_wav):
    """Extract, compress internal gaps, pad, gain-normalise. Returns
    (segs, gap_target, gain_db, final_lufs) for word remapping / reporting."""
    start, end = span
    gap_target = INTRA_GAP_OVERRIDES.get(cid, INTRA_GAP)
    gaps = internal_gaps(sil, start, end, INTERNAL_SILENCE_MIN)

    segs, cur = [], start
    for gs, ge in gaps:
        segs.append((cur, gs))
        cur = ge
    segs.append((cur, end))
    segs = [(round(a, 3), round(b, 3)) for a, b in segs if b - a > 0.01]
    if not segs:
        segs = [(start, end)]

    # ALWAYS write to a staging path, never the final out_wav directly: for
    # every single-take scene (--from-takes, no concat) block_wav IS out_wav,
    # and ffmpeg reading and writing the same file in one invocation fails
    # (or silently corrupts) -- confirmed on scene 01, which shares 01.wav as
    # both its take source and its cut destination.
    tmp = out_wav.with_suffix(".cut.wav")
    if len(segs) == 1:
        r = sh("ffmpeg", "-y", "-v", "error", "-i", str(block_wav),
               "-ss", f"{segs[0][0]:.3f}", "-to", f"{segs[0][1]:.3f}",
               "-af", f"apad=pad_dur={TAIL}", "-ac", "1", "-ar", "48000", str(tmp))
    else:
        filt, parts = [], []
        for k, (a, b) in enumerate(segs):
            filt.append(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS[s{k}]")
            parts.append(f"[s{k}]")
            if k < len(segs) - 1:
                filt.append(f"anullsrc=r=48000:cl=mono:d={gap_target:.3f}[g{k}]")
                parts.append(f"[g{k}]")
        # apad has to live INSIDE the filtergraph, not as a trailing -af: ffmpeg
        # rejects a simple filter chained onto a stream that is fed from a
        # complex filtergraph ("Simple and complex filtering cannot be used
        # together for the same stream") -- confirmed on scene 09-exclusion,
        # the only scene whose internal gap actually triggers this branch.
        filt.append(f"{''.join(parts)}concat=n={len(parts)}:v=0:a=1[cat];"
                    f"[cat]apad=pad_dur={TAIL}[out]")
        r = sh("ffmpeg", "-y", "-v", "error", "-i", str(block_wav),
               "-filter_complex", ";".join(filt), "-map", "[out]",
               "-ac", "1", "-ar", "48000", str(tmp))
    if r.returncode != 0 or not tmp.exists():
        raise SystemExit(f"cut_scene({cid}) ffmpeg failed: {r.stderr[:600]}")
    tmp.replace(out_wav)

    I = integrated_lufs(out_wav)
    gain_db = 0.0
    if I is not None:
        gain_db = max(-GAIN_CAP, min(GAIN_CAP, VO_TARGET_LUFS - I))
        if abs(gain_db) > 0.05:
            tmp = out_wav.with_suffix(".g.wav")
            sh("ffmpeg", "-y", "-v", "error", "-i", str(out_wav),
               "-af", f"volume={gain_db:.2f}dB", str(tmp))
            tmp.replace(out_wav)
    final_lufs = integrated_lufs(out_wav)
    return segs, gap_target, round(gain_db, 2), final_lufs


def remap_words(words, a0, a1, segs, gap_target):
    """Map block-relative word times through the edit list to scene-relative."""
    bounds, cum = [], 0.0
    for a, b in segs:
        bounds.append((a, b, cum))
        cum += (b - a) + gap_target

    def remap(t):
        for a, b, base in bounds:
            if a - 0.01 <= t <= b + 0.01:
                return round(base + max(0.0, min(t, b) - a), 3)
        for a, b, base in bounds:
            if t < a:
                return round(base, 3)
        return round(cum, 3)

    return [{"text": w["text"], "start": remap(w["start"]), "end": remap(w["end"])}
            for w in words[a0:a1 + 1]]


def sentences_from(words_rel):
    sents, cur = [], []
    for w in words_rel:
        cur.append(w)
        if re.search(r"[.?!]$", w["text"]):
            sents.append({"start": cur[0]["start"], "end": cur[-1]["end"],
                          "text": " ".join(x["text"] for x in cur)})
            cur = []
    if cur:
        sents.append({"start": cur[0]["start"], "end": cur[-1]["end"],
                      "text": " ".join(x["text"] for x in cur)})
    return sents


def cmd_cut(from_takes):
    rows = []
    for block_name, cids in blocks_for(from_takes):
        wav = source_wav(block_name, from_takes)
        tp = transcript_path(block_name, from_takes)
        if not wav.exists() or not tp.exists():
            raise SystemExit(f"cut: missing {wav} or {tp} -- run transcribe first")
        words = json.loads(tp.read_text())
        per_scene = align_block(cids, words)
        sil = silences(wav)
        bounds = scene_bounds(cids, words, per_scene, sil)
        for cid in cids:
            a0, a1 = per_scene[cid]
            out_wav = scene_wav(cid)
            segs, gap_target, gain_db, lufs = cut_scene(cid, wav, bounds[cid], sil, out_wav)
            words_rel = remap_words(words, a0, a1, segs, gap_target)
            sents = sentences_from(words_rel)
            L = dur(out_wav)
            speech = max(0.01, L - TAIL)
            wpm = round(len(TEXT[cid].split()) / (speech / 60), 1)
            manifest = {
                "scene": cid, "block": block_name,
                "cut": {"start": bounds[cid][0], "end": bounds[cid][1]},
                "gain_db": gain_db, "lufs": round(lufs, 1) if lufs is not None else None,
                "wpm": wpm, "words": words_rel, "sentences": sents,
            }
            scene_words_path(cid).write_text(json.dumps(manifest, indent=2))
            rows.append((cid, L, wpm, manifest["lufs"], len(segs) - 1,
                         abs(gain_db) > GAIN_WARN))

    print(f"  {'scene':16s} {'dur':>7s} {'wpm':>6s} {'lufs':>7s}  gaps  notes")
    for cid, L, wpm, lufs, ngaps, warn in rows:
        lo, hi = (120, 170) if cid in EVIDENCE else (140, 170)
        notes = []
        if not (lo <= wpm <= hi):
            notes.append(f"wpm outside [{lo},{hi}]")
        if warn:
            notes.append("gain > 3dB")
        print(f"  {cid:16s} {L:7.2f} {wpm:6.1f} {str(lufs):>7s}  {ngaps:4d}  {', '.join(notes)}")
    return 0


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("transcribe", "verify", "cut"):
        print(__doc__)
        return 2
    from_takes = "--from-takes" in sys.argv
    return {"transcribe": cmd_transcribe, "verify": cmd_verify,
            "cut": cmd_cut}[sys.argv[1]](from_takes)


if __name__ == "__main__":
    sys.exit(main())
