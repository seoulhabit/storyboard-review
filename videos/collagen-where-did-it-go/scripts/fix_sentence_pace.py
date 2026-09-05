#!/usr/bin/env python3
"""Slow one spoken sentence in the ALREADY-CUT master, without a re-roll.

    python3 scripts/fix_sentence_pace.py <sentence-i> [<sentence-i> ...] [--wpm 180] [--dry-run]

Use when `gen_vo.py verify`'s per-sentence measurement (or STORYBOARD.md)
shows a sentence at an implausible pace that survived a real take -- not a
manifest bug (see gen_vo.py's repair_implausible_runs for that), a genuine
fast read. Re-rolling the whole block for one line risks the SAME line
landing fast again (TTS pacing is stochastic) and burns a round of the
channel's two-round cap for an uncertain fix. This is deterministic instead:
atempo-stretch exactly that sentence's audio span to a target words-per-
minute, splice it back into master.wav, and shift every word/sentence/scene/
block boundary AFTER it by the resulting delta.

Why a uniform post-cut shift is safe: `timing.walk()`'s seam-grammar assert
(`first_word == start + d - j`) and every transition gap in transitions.KIND
are RELATIVE -- a gap between two absolute times. Shifting everything after
the edit point by the same constant delta changes no gap anywhere, so nothing
downstream needs to know an edit happened at all. This is NOT true of a
proportional retime of the whole take (which is what changing plan_edit's
global TEMPO does) -- that's why this script edits ONE sentence's audio and
uniformly translates the rest, rather than touching gen_vo.py's cut() at all.

Scene 'wpm' is recomputed for any scene whose span changed. Block audio stats
(stats_master: lufs/centroid/tilt/f0) are NOT re-derived -- they go slightly
stale after a local edit, but nothing downstream reads them for a gate;
check-final.py measures loudness/etc. on the actual rendered MP4, not this
field. Re-run `npm run build` after this to regenerate frames/captions/index
from the corrected manifest.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WAV = ROOT / "assets" / "voice" / "master.wav"
MANIFEST = ROOT / "assets" / "voice" / "master.words.json"


def sh(*a):
    r = subprocess.run([str(x) for x in a], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"cmd failed: {a}\n{r.stderr}")
    return r


def probe_dur(p):
    r = sh("ffprobe", "-v", "error", "-show_entries", "format=duration",
           "-of", "default=nk=1:nw=1", p)
    return float(r.stdout.strip())


def atempo_chain(factor):
    """ffmpeg's atempo is valid only in [0.5, 2.0] per filter instance;
    chain instances to reach a factor outside that range. factor < 1 slows
    down (output is longer than input)."""
    parts, f = [], factor
    while f < 0.5:
        parts.append(0.5); f /= 0.5
    while f > 2.0:
        parts.append(2.0); f /= 2.0
    parts.append(f)
    return ",".join(f"atempo={p:.6f}" for p in parts)


def apply_shift(manifest, edit_start, edit_end, new_dur):
    """Rescale the edited span's own words in place (same relative
    proportions, uniformly slower -- exactly what atempo did to the audio),
    then translate every word/sentence/scene/block boundary strictly after
    the edit by the same constant delta."""
    delta = new_dur - (edit_end - edit_start)
    scale = new_dur / (edit_end - edit_start)

    for w in manifest["words"]:
        if edit_start - 0.001 <= w["start"] < edit_end - 0.001:
            w["start"] = round(edit_start + (w["start"] - edit_start) * scale, 3)
            w["end"] = round(edit_start + (w["end"] - edit_start) * scale, 3)
        elif w["start"] >= edit_end - 0.001:
            w["start"] = round(w["start"] + delta, 3)
            w["end"] = round(w["end"] + delta, 3)

    for s in manifest["sentences"]:
        if abs(s["start"] - edit_start) < 0.005 and abs(s["end"] - edit_end) < 0.005:
            s["end"] = round(edit_start + new_dur, 3)
        elif s["start"] >= edit_end - 0.001:
            s["start"] = round(s["start"] + delta, 3)
            s["end"] = round(s["end"] + delta, 3)

    # Read both old boundaries ONCE before any mutation: an end-matches-the-
    # edit case and a shift-because-it's-after case must never both fire on
    # the same (already-mutated) field in one pass -- that double-applies
    # the shift to any scene whose end happens to equal the edit boundary.
    for sc in manifest["scenes"]:
        old_start, old_end = sc["start"], sc["end"]
        new_start, new_end = old_start, old_end
        if abs(old_end - edit_end) < 0.005 and old_start < edit_end:
            new_end = round(edit_start + new_dur, 3)
        elif old_end >= edit_end - 0.001:
            new_end = round(old_end + delta, 3)
        if old_start >= edit_end - 0.001:
            new_start = round(old_start + delta, 3)
        if (new_start, new_end) != (old_start, old_end):
            sc["start"], sc["end"] = new_start, new_end
            n = sc["last_word_idx"] - sc["first_word_idx"] + 1
            sc["wpm"] = round(n / max(0.01, sc["end"] - sc["start"]) * 60, 1)

    for b in manifest["blocks"]:
        if b["span"][1] >= edit_end - 0.001:
            b["span"][1] = round(b["span"][1] + delta, 3)

    manifest["duration"] = round(manifest["duration"] + delta, 3)
    manifest["wpm"] = round(len(manifest["words"]) /
                             max(0.01, manifest["words"][-1]["end"] - manifest["words"][0]["start"]) * 60, 1)
    return delta


def fix_one(manifest, sent_i, target_wpm, dry_run):
    s = next((x for x in manifest["sentences"] if x["i"] == sent_i), None)
    if s is None:
        print(f"  sentence {sent_i}: not found, skipped"); return
    n = s["last_word_idx"] - s["first_word_idx"] + 1
    old_start, old_end = s["start"], s["end"]
    old_dur = old_end - old_start
    old_wpm = n / old_dur * 60
    target_dur = n * 60 / target_wpm
    # Works in both directions: target_wpm below the current pace SLOWS the
    # sentence (the original use case -- a genuinely-too-fast read survived
    # a real take); target_wpm above it COMPRESSES instead, e.g. to buy back
    # a few hundred ms elsewhere in the timeline (a curiosity-loop deadline
    # a few seconds later, missed by milliseconds) without re-recording.
    if abs(target_dur - old_dur) < 0.01:
        print(f"  sentence {sent_i} ({s['cid']!r} {s['text']!r}): "
              f"{old_wpm:.1f}wpm already at the {target_wpm:.0f}wpm target, skipped")
        return
    if dry_run:
        print(f"  sentence {sent_i} ({s['cid']!r} {s['text']!r}): "
              f"{old_dur:.3f}s ({old_wpm:.1f}wpm) -> would become "
              f"{target_dur:.3f}s ({target_wpm:.0f}wpm), delta ~{target_dur - old_dur:+.3f}s")
        return

    tag = f"{sent_i}"
    clip, stretched = Path(f"/tmp/tempo_clip_{tag}.wav"), Path(f"/tmp/tempo_stretched_{tag}.wav")
    before, after = Path(f"/tmp/tempo_before_{tag}.wav"), Path(f"/tmp/tempo_after_{tag}.wav")
    listfile, newwav = Path(f"/tmp/tempo_concat_{tag}.txt"), Path(f"/tmp/tempo_new_{tag}.wav")

    sh("ffmpeg", "-y", "-v", "error", "-i", WAV, "-ss", f"{old_start:.3f}", "-to", f"{old_end:.3f}", clip)
    factor = old_dur / target_dur
    sh("ffmpeg", "-y", "-v", "error", "-i", clip, "-filter:a", atempo_chain(factor), stretched)
    actual_new_dur = probe_dur(stretched)

    sh("ffmpeg", "-y", "-v", "error", "-i", WAV, "-to", f"{old_start:.3f}", before)
    sh("ffmpeg", "-y", "-v", "error", "-i", WAV, "-ss", f"{old_end:.3f}", after)
    listfile.write_text(f"file '{before}'\nfile '{stretched}'\nfile '{after}'\n")
    sh("ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", listfile, "-c", "copy", newwav)

    delta = apply_shift(manifest, old_start, old_end, actual_new_dur)
    sh("cp", newwav, WAV)
    print(f"  sentence {sent_i} ({s['cid']!r} {s['text']!r}): "
          f"{old_dur:.3f}s ({old_wpm:.1f}wpm) -> {actual_new_dur:.3f}s "
          f"({n / actual_new_dur * 60:.1f}wpm), delta={delta:+.3f}s")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sentences", nargs="+", type=int, help="sentence 'i' index/indices from master.words.json")
    ap.add_argument("--wpm", type=float, default=180.0, help="target words/minute (default 180)")
    ap.add_argument("--dry-run", action="store_true", help="report the change without writing anything")
    args = ap.parse_args()

    manifest = json.loads(MANIFEST.read_text())
    for sent_i in sorted(set(args.sentences)):
        fix_one(manifest, sent_i, args.wpm, args.dry_run)

    if not args.dry_run:
        MANIFEST.write_text(json.dumps(manifest, indent=1))
        print(f"\nnew total duration: {manifest['duration']:.3f}s -- run `npm run build` next")
    return 0


if __name__ == "__main__":
    sys.exit(main())
