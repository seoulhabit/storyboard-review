#!/usr/bin/env python3
"""Re-pace already-cut scene voiceover: tempo + authored mid-scene rests.

WHY THIS AND NOT A RE-ROLL. The 2026-09-05 review asked for 125-135 wpm through
the technical and evidence sections, which sit at 143-166 today. Re-voicing them
means new TTS for eleven scenes across three acts while the acts around them keep
their original takes, and the seams between them then have to match on level,
brightness and pace. This operates on the CUT wavs instead: the read is the same
read, so nothing can drift.

WHAT IT DOES, per scene:
  * atempo on each speech segment (pitch-preserving),
  * `anullsrc` silence inserted at authored rest points, which atempo never
    touches -- so a 0.5s rest is 0.5s, not 0.5/T,
  * a rewritten NN.words.json whose times are CONSTRUCTED from the same plan the
    ffmpeg graph executes, never remapped afterwards.

THE SEGMENT PIN is load-bearing and is ported from
videos/collagen-where-did-it-go/scripts/gen_vo.py:829-868. atempo's output is not
exactly input/rate -- it rounds at its own frame boundaries, and on that project
the rounding accumulated to 0.44s across 61 segments. Every word time, caption
cue and @w() anchor here is computed from the PLAN, so a master that runs long
against its plan slides the back half of the scene out of sync with its own
narration. Trimming and padding each segment to the planned length makes the
plan true by construction.

IDEMPOTENT. Originals are snapshotted to assets/voice/_orig/ on first run and
every run reads from there, so the numbers below can be changed and the script
re-run without compounding.

  python3 scripts/repace_vo.py            # apply
  python3 scripts/repace_vo.py --report   # measure only, write nothing
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vo_lines import LINES, TEXT, SLOWED

VOICE = ROOT / "assets" / "voice"
ORIG = VOICE / "_orig"

# atempo below this makes the formants audible. The sibling project measured
# 0.92 as its comfort floor on the same voice; 0.90 is the outer limit worth
# spending, and the authored rests carry whatever the tempo cannot.
# atempo below this makes the formants audible. The sibling project measured
# 0.92 as its comfort floor on the same voice; 0.90 is the outer limit worth
# spending, and the authored rests carry whatever the tempo cannot.
TEMPO_MIN = 0.90
WPM_TARGET_BAND = (123.0, 137.0)
MIN_GAP = 0.03   # a rest is placed at the MIDPOINT of the gap after its anchor

# Scenes the review asked to slow that are NOT held to the band, with the
# reason. This is the only place an exemption can be written down.
EXEMPT = {
    "21-verdict": (
        "reads 102 wpm and cannot reach 123 without undoing the review's own "
        "request for short breaks between bitop, Merck and Kao: the line is "
        "four one-word sentences, so its span is mostly authored pause and a "
        "span-based wpm reads low by construction. Its ARTICULATION is normal; "
        "speeding it to hit a number would remove the breaks that were asked for."),
}

# scene -> (tempo, [(word_index, expected_token, seconds), ...])
#
# Every rest carries the word index AND the word it follows, and the script
# refuses to run if they disagree -- an index that silently slid one word after
# a re-cut would move a beat without anyone noticing. Rests land at the midpoint
# of the gap after the anchor word.
#
# The named rests are the review's, by timecode:
#   01:36  09-exclusion  after "The honest version is messier."
#   02:49  16-trial104   after "...to actual people?"
#   04:10  23-numbers    after "Turn it around."
#   plus a beat between the buying advice and "And tell me..." in 29-cta.
#
# Tempo and rest budget are SOLVED, not guessed: tempo goes to the floor first,
# and the rests make up whatever distance is left to 130 wpm (--plan prints the
# arithmetic). 08-humectant, 19-limits and 20-twelve already read inside the
# band and are left alone -- correcting a scene that is already right is how a
# pass introduces a defect.
PACING = {
    # --- 01:13-02:02 mechanism ---
    "09-exclusion":  (0.92, [(24, "organized.", 0.40), (29, "messier.", 0.75)]),
    "11-analogy":    (0.90, [(8, "security.", 0.55), (14, "celebrity.", 0.60),
                             (24, "shape,", 0.63)]),
    # --- 02:53-03:49 human evidence ---
    "16-trial104":   (0.90, [(7, "people?", 0.85), (12, "study,", 0.50),
                             (19, "2%", 0.35)]),
    "17-preference": (0.90, [(16, "result.", 0.15)]),
    "18-eczema":     (0.90, [(13, "eczema.", 0.36)]),
    # --- 04:12-04:32 reading the label ---
    "23-numbers":    (0.90, [(10, "bottle.", 0.45), (13, "around.", 0.85),
                             (20, "number.", 0.35), (24, "7%.", 0.34)]),
    "24-eleven":     (0.90, [(13, "ingredients.", 0.35), (20, "list.", 0.30),
                             (23, "11th.", 0.25)]),
    # --- close: the instruction and the question get separate beats ---
    "29-cta":        (1.00, [(18, "buy.", 0.50)]),
    # Not one of the review's three sections, but it read 174 wpm against this
    # project's own 140-170 band once the wpm definition was made consistent
    # (gen_vo.py used to measure the whole clip, padding included, and the
    # scene squeaked under 170 on that arithmetic). 4% is inaudible and moves
    # the same direction as everything else in this pass.
    "06-mechanism":  (0.96, []),
}

# A scene too short for a span-based wpm to mean anything. Four words over two
# seconds is a number, not a measurement.
SHORT = {"30-endcard"}


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True)


def dur(p):
    return float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration",
                    "-of", "csv=p=0", str(p)).stdout.strip())


def scene_n(cid):
    return int(cid.split("-")[0])


def snapshot():
    """Copy every scene's cut wav+manifest aside, once. Never overwritten."""
    ORIG.mkdir(parents=True, exist_ok=True)
    for cid, _ in LINES:
        n = scene_n(cid)
        for suffix in (".wav", ".words.json"):
            src, dst = VOICE / f"{n:02d}{suffix}", ORIG / f"{n:02d}{suffix}"
            if src.exists() and not dst.exists():
                shutil.copy2(src, dst)


def load_orig(cid):
    n = scene_n(cid)
    wav = ORIG / f"{n:02d}.wav"
    man = json.loads((ORIG / f"{n:02d}.words.json").read_text())
    return wav, man


def resolve_rests(cid, words, rests):
    """[(raw_split_time, seconds)] -- a rest lands at the MIDPOINT of the gap
    after the anchor word, so neither that word's release nor the next word's
    onset is cut into. The index and the word must agree: a stale index would
    move a beat to the wrong place and nothing downstream would notice."""
    out = []
    for i, token, secs in rests:
        if i >= len(words) - 1:
            raise SystemExit(f"{cid}: rest anchor {i} ({token!r}) is at or past "
                             f"the last word; scene-end rests belong in "
                             f"transitions.REST_AFTER")
        got = words[i]["text"].strip()
        if got != token:
            raise SystemExit(
                f"{cid}: rest anchor {i} is {got!r}, not {token!r} -- the cut "
                f"read has changed under this table.\n"
                f"  words: " + " ".join(f"{k}:{w['text']}" for k, w in enumerate(words)))
        gap = words[i + 1]["start"] - words[i]["end"]
        out.append((words[i]["end"] + max(0.0, gap) / 2.0, secs))
    return sorted(out)


def plan(cid, wav, man, tempo, rests):
    """-> (ffmpeg filter parts, new word list, planned total).

    The master timeline is CONSTRUCTED here; the filter graph below only
    executes it. Nothing is remapped after the fact."""
    words = man["words"]
    total_raw = dur(wav)
    splits = resolve_rests(cid, words, rests)

    segs, cursor, edges = [], 0.0, []   # edges: (raw_a, raw_b, master_a)
    a = 0.0
    for raw_t, secs in splits + [(total_raw, 0.0)]:
        b = min(raw_t, total_raw)
        if b - a > 0.005:
            edges.append((a, b, cursor))
            segs.append(("seg", a, b))
            cursor += (b - a) / tempo
        if secs > 0:
            segs.append(("sil", secs))
            cursor += secs
        a = b

    def to_master(t):
        for ra, rb, ma in edges:
            if ra - 0.005 <= t <= rb + 0.005:
                return round(ma + (min(max(t, ra), rb) - ra) / tempo, 3)
        return round(edges[-1][2] + (edges[-1][1] - edges[-1][0]) / tempo, 3)

    new_words = [{**w, "start": to_master(w["start"]), "end": to_master(w["end"])}
                 for w in words]
    return segs, new_words, round(cursor, 3)


def build(wav, segs, tempo, out):
    parts, labels = [], []
    for k, item in enumerate(segs):
        if item[0] == "sil":
            parts.append(f"anullsrc=r=48000:cl=mono:d={item[1]:.3f},"
                         f"aformat=sample_fmts=s16:sample_rates=48000:"
                         f"channel_layouts=mono[p{k}]")
        else:
            _, a, b = item
            chain = [f"[0:a]atrim=start={a:.3f}:end={b:.3f}", "asetpts=PTS-STARTPTS",
                     "aformat=sample_fmts=s16:sample_rates=48000:channel_layouts=mono"]
            if abs(tempo - 1.0) > 1e-6:
                chain.append(f"atempo={tempo:.4f}")
            # PIN each segment to its planned length -- see the module docstring.
            want = (b - a) / tempo
            chain += [f"atrim=start=0:duration={want:.4f}", "asetpts=PTS-STARTPTS",
                      f"apad=whole_dur={want:.4f}", f"atrim=start=0:duration={want:.4f}",
                      "asetpts=PTS-STARTPTS"]
            parts.append(",".join(chain) + f"[p{k}]")
        labels.append(f"[p{k}]")
    graph = ";".join(parts) + f";{''.join(labels)}concat=n={len(labels)}:v=0:a=1[out]"
    r = sh("ffmpeg", "-y", "-v", "error", "-i", str(wav), "-filter_complex", graph,
           "-map", "[out]", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "1", str(out))
    if r.returncode != 0:
        raise SystemExit(f"ffmpeg failed:\n{r.stderr[:800]}")


def wpm_of(cid, words):
    """Scripted words over the spoken span -- the SAME definition gen_vo.py and
    check-vo.py use. Counting ASR tokens instead would disagree with every other
    number in the project by a few per cent."""
    span = words[-1]["end"] - words[0]["start"]
    return round(len(TEXT[cid].split()) / max(0.01, span) * 60, 1)


def main():
    report = "--report" in sys.argv
    snapshot()
    bad = []
    print(f"  {'scene':16s} {'tempo':>5s} {'rests':>5s}  {'wpm':>6s} -> {'wpm':>6s}   "
          f"{'len':>6s} -> {'len':>6s}")
    for cid, _ in LINES:
        wav, man = load_orig(cid)
        tempo, rests = PACING.get(cid, (1.0, []))
        if tempo < TEMPO_MIN:
            raise SystemExit(f"{cid}: tempo {tempo} is below TEMPO_MIN {TEMPO_MIN}")
        was = wpm_of(cid, man["words"])
        if tempo == 1.0 and not rests:
            # Untouched, but its manifest's stored `wpm` may predate the single
            # definition (gen_vo.py used to measure the padded clip). Every
            # consumer reads that field, so it is refreshed here whether or not
            # the audio moved -- a stale number in a manifest fails a gate on a
            # scene that is actually fine, which is worse than no number.
            n = scene_n(cid)
            cur = json.loads((VOICE / f"{n:02d}.words.json").read_text())
            if cur.get("wpm") != was and not report:
                cur["wpm"] = was
                (VOICE / f"{n:02d}.words.json").write_text(json.dumps(cur, indent=1))
            print(f"  {cid:16s} {'--':>5s} {'--':>5s}  {was:6.1f}    (unchanged)")
            continue
        segs, new_words, total = plan(cid, wav, man, tempo, rests)
        now = wpm_of(cid, new_words)
        n = scene_n(cid)
        if not report:
            build(wav, segs, tempo, VOICE / f"{n:02d}.wav")
            out = dict(man, words=new_words, wpm=now,
                       repaced={"tempo": tempo, "rests": rests})
            (VOICE / f"{n:02d}.words.json").write_text(json.dumps(out, indent=1))
        print(f"  {cid:16s} {tempo:5.2f} {len(rests):5d}  {was:6.1f} -> {now:6.1f}   "
              f"{dur(wav):6.2f} -> {total:6.2f}")
        if cid in SLOWED and cid not in EXEMPT and \
                not (WPM_TARGET_BAND[0] <= now <= WPM_TARGET_BAND[1]):
            bad.append((cid, now))

    # A slowed scene with no PACING entry is checked on its RESULT, not on
    # whether it was touched -- one that already reads inside the band needs no
    # correction, and "correcting" it is how a pass introduces a defect.
    for cid, _ in LINES:
        if cid in SLOWED and cid not in PACING and cid not in EXEMPT:
            _, man = load_orig(cid)
            w = wpm_of(cid, man["words"])
            if not (WPM_TARGET_BAND[0] <= w <= WPM_TARGET_BAND[1]):
                bad.append((cid, f"{w} (no pacing entry)"))
    for cid, why in EXEMPT.items():
        print(f"\n  EXEMPT {cid}: {why}")
    if bad:
        print(f"\n  {len(bad)} slowed scene(s) outside {WPM_TARGET_BAND}:")
        for cid, v in bad:
            print(f"    {cid:16s} {v}")
        return 1
    print(f"\n  all slowed scenes inside {WPM_TARGET_BAND} wpm"
          f"{' (report only, nothing written)' if report else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
