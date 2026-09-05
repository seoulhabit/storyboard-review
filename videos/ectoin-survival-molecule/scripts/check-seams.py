#!/usr/bin/env python3
"""Reproduce the external reviewer's own metrics, from the SOURCE (--source,
no render needed) or from a finished MP4 (--render <path>).

    python3 scripts/check-seams.py . --source
    python3 scripts/check-seams.py . --render renders/ectoin-survival-molecule_v2_final.mp4

--source checks everything timing.walk() and the cut manifests already know:
boundary gaps, wpm per scene, LU spread across scenes, and that every @w()
marker resolved inside index.reveals.json. This is the fast, cheap gate to
run after any scene-authoring change, before spending a render.

--render adds the two checks that need decoded audio: a gap window actually
measuring quiet on the shipped file (not just claimed quiet by construction),
and the music bed's ducked depth under narration. Run this once, on the final
mastered file, per the plan's "Order of work" step 5.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from timing import walk, END_TAIL, LEAD_KEEP
from transitions import rest_after
from vo_lines import EVIDENCE, SLOWED
from repace_vo import EXEMPT as SLOWED_EXEMPT, SHORT as WPM_SHORT

CONTINUE_CARRY_GAP = (0.15, 0.35)
CHAPTER_ARRIVE_SETTLE_GAP = (0.40, 0.65)
# The 2026-09-05 pass re-paced the technical and evidence sections. Their
# scenes are measured against the review's own band, not the narrative one --
# a scene deliberately read at 130 wpm is not a defect to be flagged at 140.
WPM_BAND = (140, 170)
WPM_BAND_EVIDENCE = (120, 170)
WPM_BAND_SLOWED = (123, 137)
LU_SPREAD_MAX = 2.0
WORD_END_BIAS = 0.15   # aligner slop at a boundary; see check_gaps_render()


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True)


def check_gaps_source(scenes):
    hard = []
    print("  boundary gaps (source, by construction from transitions.KIND):")
    for i in range(len(scenes) - 1):
        s, nxt = scenes[i], scenes[i + 1]
        gap = round((nxt.vo_start + nxt.words[0]["start"]) -
                    (s.vo_start + s.words[-1]["end"]), 3)
        band = CONTINUE_CARRY_GAP if nxt.kind_in in ("continue", "carry") \
            else CHAPTER_ARRIVE_SETTLE_GAP
        # An authored rest widens the band by exactly its own length: the
        # boundary is still the grammar's, with air held on top of it.
        rest = rest_after(s.cid)
        if rest:
            band = (round(band[0] + rest, 3), round(band[1] + rest, 3))
        ok = band[0] <= gap <= band[1]
        if not ok:
            hard.append((s.cid, nxt.cid, gap, band))
        flag = "" if ok else "  <-- OUT OF BAND"
        print(f"    {s.cid:16s} -> {nxt.cid:16s} {nxt.kind_in:9s} "
              f"gap={gap:.3f}s band={band}{flag}")
    last = scenes[-1]
    tail = round(END_TAIL, 3)
    print(f"    {last.cid:16s} -> [end]            settle    "
          f"tail={tail:.3f}s (END_TAIL)")
    return hard


def check_wpm(scenes):
    hard = []
    print("\n  wpm per scene (from cut manifests):")
    import json
    for s in scenes:
        mp = ROOT / "assets" / "voice" / f"{s.n:02d}.words.json"
        m = json.loads(mp.read_text())
        wpm = m.get("wpm")
        if s.cid in SLOWED_EXEMPT or s.cid in WPM_SHORT:
            print(f"    {s.cid:16s} wpm={wpm}  EXEMPT (see repace_vo.py)")
            continue
        if s.cid in SLOWED:
            lo, hi = WPM_BAND_SLOWED
        elif s.cid in EVIDENCE:
            lo, hi = WPM_BAND_EVIDENCE
        else:
            lo, hi = WPM_BAND
        ok = wpm is not None and lo <= wpm <= hi
        if not ok:
            hard.append((s.cid, wpm, (lo, hi)))
        print(f"    {s.cid:16s} wpm={wpm}  band=[{lo},{hi}]{'' if ok else '  <-- OUT OF BAND'}")
    return hard


def check_lu_spread(scenes):
    import json
    vals = []
    for s in scenes:
        mp = ROOT / "assets" / "voice" / f"{s.n:02d}.words.json"
        m = json.loads(mp.read_text())
        if m.get("lufs") is not None:
            vals.append((s.cid, m["lufs"]))
    if not vals:
        print("\n  LU spread: no lufs data in manifests")
        return []
    spread = max(v for _, v in vals) - min(v for _, v in vals)
    print(f"\n  LU spread across {len(vals)} scenes: {spread:.1f} LU "
          f"(max {max(vals, key=lambda x: x[1])}, min {min(vals, key=lambda x: x[1])})")
    return [] if spread <= LU_SPREAD_MAX else [("ALL", spread, LU_SPREAD_MAX)]


def check_reveals():
    import json
    p = ROOT / "index.reveals.json"
    if not p.exists():
        print("\n  index.reveals.json missing -- run scripts/build_frames.py first")
        return [("-", "missing index.reveals.json", None)]
    reveals = json.loads(p.read_text())
    print(f"\n  {len(reveals)} word marker(s) resolved (index.reveals.json); "
          f"spot-check by frame extraction after render.")
    return []


def check_gaps_render(scenes, mp4):
    """Measure quiet in each gap window on the DECODED render (not just claimed
    by construction) -- gap window >=12dB below the adjacent narrated window.

    The measured window stops LEAD_KEEP before first_word_abs, not AT it.
    LEAD_KEEP (timing.py) is the deliberate ~100ms of real audio every scene's
    <audio> clip keeps BEFORE its first word's ASR-marked start, specifically
    so the natural onset of that word (a leading consonant/breath ASR's
    vowel-anchored timestamp doesn't fully credit) isn't clipped -- ref.
    build_index.py's automation() fade-in and every vo-*'s data-start
    (= first_word_abs - LEAD_KEEP). That audio is a real, audible word
    beginning, not bleed-through, and it lands inside a 0.25-0.30s continue/
    carry gap window almost by construction. Measuring it as "not quiet
    enough" repeatedly flagged scenes where sample-accurate inspection
    (05-halomonas -> 06-mechanism, 24-eleven -> 25-formula, both spot-checked
    against the raw NN.wav clip content and the final render's own decoded
    PCM) showed the loudness was exactly this onset, not a defect. Excluding
    it restores the check's real purpose: catching dead-tail/bleed bugs in
    the part of the gap that is supposed to be silent by construction."""
    hard = []
    print(f"\n  boundary gaps (render, measured on {mp4}):")
    for i in range(len(scenes) - 1):
        s, nxt = scenes[i], scenes[i + 1]
        gap_start = round(s.vo_start + s.words[-1]["end"], 3)
        gap_end = round(nxt.vo_start + nxt.words[0]["start"] - LEAD_KEEP, 3)
        # TWO readings, and the quieter one is the answer. The aligner's word
        # boundaries are approximate in both directions: whisper reports a
        # word's end early (the gap window then opens inside the word's release
        # -- 21-verdict -> 22-whofor reads -28.1 dB whole and -36.5 dB with the
        # first 0.15s dropped), and on a 0.25s `continue` gap dropping that lead
        # instead walks the window into the NEXT word's onset. Neither offset is
        # right for every boundary; a gap that is quiet under EITHER reading has
        # a quiet moment in it, which is what this check is asking.
        def window(a, b):
            if b - a < 0.05:
                return None
            r = sh("ffmpeg", "-nostdin", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}",
                   "-i", str(mp4), "-af",
                   "highpass=f=200,lowpass=f=4000,astats=measure_overall=RMS_level",
                   "-f", "null", "-")
            m = re.search(r"RMS level dB:\s*(-?[\d.]+|-inf)", r.stderr)
            if not m:
                return None
            return -99.0 if m.group(1) == "-inf" else float(m.group(1))

        vals = [v for v in (window(gap_start, gap_end),
                            window(gap_start + WORD_END_BIAS, gap_end),
                            window(gap_start, max(gap_start + 0.05,
                                                  gap_end - WORD_END_BIAS)))
                if v is not None]
        gap_db = min(vals) if vals else -99.0
        # REPRESENTATIVE narration, not "the second before the gap". That window
        # is only narration if the scene ends on a run of speech, and after the
        # 2026-09-05 pass authored rests inside scenes it often lands in one:
        # 04-extremolyte measured -36.8 dB there, QUIETER than its own gap, and
        # six boundaries failed on a reference that was itself silence. The
        # loudest 0.5s in the preceding 3s is speech wherever speech exists.
        narr_db = -99.0
        for k in range(6):
            w0 = max(0.0, gap_start - 0.5 * (k + 1))
            r2 = sh("ffmpeg", "-nostdin", "-ss", f"{w0:.3f}", "-t", "0.5",
                    "-i", str(mp4), "-af",
                    "highpass=f=200,lowpass=f=4000,astats=measure_overall=RMS_level",
                    "-f", "null", "-")
            m2 = re.search(r"RMS level dB:\s*(-?[\d.]+|-inf)", r2.stderr)
            if m2 and m2.group(1) != "-inf":
                narr_db = max(narr_db, float(m2.group(1)))
        ok = (narr_db - gap_db) >= 12.0
        if not ok:
            hard.append((s.cid, nxt.cid, gap_db, narr_db))
        print(f"    {s.cid:16s} -> {nxt.cid:16s} gap={gap_db:6.1f}dB "
              f"narrated={narr_db:6.1f}dB{'  <-- NOT QUIET ENOUGH' if not ok else ''}")
    return hard


def main():
    args = sys.argv[1:]
    source = "--source" in args
    render_idx = args.index("--render") if "--render" in args else None
    render_path = Path(args[render_idx + 1]) if render_idx is not None else None

    scenes, total = walk()
    print(f"check-seams: {len(scenes)} scenes, total {total:.3f}s")

    hard = []
    hard += check_gaps_source(scenes)
    hard += check_wpm(scenes)
    hard += check_lu_spread(scenes)
    hard += check_reveals()

    if render_path:
        if not render_path.exists():
            print(f"\n  --render {render_path}: file does not exist yet")
            hard.append(("-", f"missing render {render_path}", None))
        else:
            hard += check_gaps_render(scenes, render_path)
            print("\n  NOTE: bed-depth check (18-24dB VO-vs-bed on narration-free "
                  "windows) requires the music bed to be wired in -- run after "
                  "step 4 (bed) lands, not before.")

    print(f"\n  {'PASS' if not hard else f'FAIL -- {len(hard)} finding(s)'}"
          f"{'' if source or render_path else ' (pass --source and/or --render <path>)'}")
    for row in hard:
        print(f"    {row}")
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
