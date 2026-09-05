#!/usr/bin/env python3
"""QC every scene's CUT voiceover from its manifest -- no re-transcription.

Previously this re-ran whisper on every take to get wpm/tail/pronunciation.
That work is now done once, per block, by `scripts/gen_vo.py verify` (garble/
truncation/silence) and `scripts/gen_vo.py cut` (which writes wpm/lufs/gain
straight into assets/voice/NN.words.json as it cuts). Re-deriving any of that
here by re-transcribing would risk disagreeing with the manifest the render
actually uses -- one source, read here, not recomputed.

Three checks, read from the manifest:

1. WPM per scene against vo_lines.EVIDENCE's two bands (120-170 for citation-
   heavy scenes, 140-170 otherwise) -- see scripts/timing.py's docstring for
   why a hand-typed absolute second used to make this drift silently; wpm now
   comes straight from the cut clip's own measured speech span.
2. LUFS spread across scenes -- flags anything gen_vo.py's gain cap (+-5dB)
   could not fully correct, i.e. still far from VO_TARGET_LUFS.
3. RARE-WORD PRONUNCIATION -- re-reads the same manifest text gen_vo.py verify
   already checked at the BLOCK level; reported again here per-scene so a
   scene inheriting a flagged block is easy to spot without re-running verify.
"""
import json
import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

# Every rare term the 2026-09-05 review asked to have verified by ear, matched
# loosely enough to catch the way the recogniser garbles it. A hit that is not
# in EXPECT means the ASR did not hear the word as itself, which is a re-roll or
# a PRONUNCIATION LOCK in the TTS prompt -- never a caption fix (see the closing
# note below).
RARE = re.compile(
    r'\b[Ee]ct[a-z]*\b|\b[a-z]*ecto[a-z]*\b'
    r'|\bhalo[a-z]*\b|\belonga[a-z]*\b|\bextremo[a-z]*\b'
    r'|\bpanthe[a-z]*\b|\bsqual[a-z]*\b|\bceram[a-z]*\b'
    r'|\bkerat[a-z]*\b|\batop[a-z]*\b|\bdermat[a-z]*\b'
    r'|\bhumect[a-z]*\b|\bglycer[a-z]*\b|\bhyalur[a-z]*\b'
    r'|\\bbitop\\b|\\bbtop\\b|\\bmerck\\b|\\bkao\\b|\\babib[a-z]*\\b',
    re.IGNORECASE)
EXPECT = {
    "ectoin", "ectoins", "halomonas", "elongata", "extremolyte", "extremolytes",
    "extremolite",   # ASR spelling of the same sound; captions use the script

    "panthenol", "squalane", "ceramides", "ceramide", "keratin", "atopic",
    "dermatitis", "dermatologist", "humectant", "humectants", "glycerin",
    "hyaluronic", "hyaluronic acid",
    "bitop", "merck", "kao", "abib", "abib's",
    # small.en's known misses on this voice. The AUDIO is correct -- verified on
    # whisper large-v3, which reads all three -- and vo_words.CORRECTIONS maps
    # them back for the captions, so these are recorded as accepted, not fixed.
    "btop", "cow",
}
VO_TARGET_LUFS = -20.0
LUFS_WARN = 2.0


def main():
    from vo_lines import LINES, EVIDENCE, SLOWED, TEXT
    from repace_vo import EXEMPT as SLOWED_EXEMPT, SHORT as WPM_SHORT

    findings = []
    print(f"  {'scene':16s} {'dur':>7s} {'wpm':>6s} {'lufs':>7s} {'gain':>6s}  notes")
    rows = []
    for cid, _text in LINES:
        n = int(cid.split("-")[0])
        wav = ROOT / "assets" / "voice" / f"{n:02d}.wav"
        mp = ROOT / "assets" / "voice" / f"{n:02d}.words.json"
        if not wav.exists() or not mp.exists():
            print(f"  {cid:16s} MISSING -- run scripts/gen_vo.py cut first")
            findings.append((cid, "missing"))
            continue
        m = json.loads(mp.read_text())
        # COMPUTED, not read. `wpm` in the manifest is written by whichever
        # tool last touched that scene -- gen_vo.py cut for most, repace_vo.py
        # for the re-paced ones -- and a scene neither has rewritten still
        # carries the number from the cut BEFORE the re-pace. One definition,
        # applied to the words that are actually on disk: scripted words over
        # the spoken span, the same as gen_vo.py:476.
        words = m["words"]
        span = words[-1]["end"] - words[0]["start"]
        wpm = round(len(TEXT[cid].split()) / max(0.01, span) * 60, 1)
        lufs = m.get("lufs")
        gain = m.get("gain_db")
        if cid in SLOWED_EXEMPT or cid in WPM_SHORT:
            lo = hi = None           # exempt with a written reason; see repace_vo.EXEMPT
        elif cid in SLOWED:
            lo, hi = (123, 137)      # the review's re-paced sections
        elif cid in EVIDENCE:
            lo, hi = (120, 170)
        else:
            lo, hi = (140, 170)
        notes = []
        if lo is not None and wpm is not None and not (lo <= wpm <= hi):
            notes.append(f"wpm outside [{lo},{hi}]")
            findings.append((cid, "wpm"))
        if lufs is not None and abs(lufs - VO_TARGET_LUFS) > LUFS_WARN:
            notes.append(f"lufs {LUFS_WARN}+ off target ({VO_TARGET_LUFS})")
            findings.append((cid, "lufs"))
        text = " ".join(w["text"] for w in m.get("words", []))
        bad = sorted({w for w in RARE.findall(text) if w.lower() not in EXPECT})
        if bad:
            notes.append(f"garbled: {bad}")
            findings.append((cid, "pronunciation"))
        dur_s = m["cut"]["end"] - m["cut"]["start"] if "cut" in m else None
        print(f"  {cid:16s} {str(round(dur_s,2)) if dur_s else '?':>7s} "
              f"{str(wpm):>6s} {str(lufs):>7s} {str(gain):>6s}  {', '.join(notes) or 'ok'}")
        rows.append((cid, wpm, lufs))

    lufs_vals = [l for _, _, l in rows if l is not None]
    if lufs_vals:
        spread = max(lufs_vals) - min(lufs_vals)
        print(f"\n  LU spread across {len(lufs_vals)} scenes: {spread:.1f} LU "
              f"(max {max(lufs_vals):.1f}, min {min(lufs_vals):.1f})")

    if not findings:
        print("\n  All scenes pass.")
    else:
        by_kind = {}
        for _, k in findings:
            by_kind[k] = by_kind.get(k, 0) + 1
        print(f"\n  {len(findings)} finding(s): "
              f"{', '.join(f'{k}={n}' for k, n in by_kind.items())}")
        print("  A garbled rare word needs a PHONETIC RESPELLING in the TTS prompt "
              "only -- never in the on-screen text or the caption.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
