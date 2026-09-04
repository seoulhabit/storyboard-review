#!/usr/bin/env python3
"""The single timing walk. build_index.py and build_frames.py MUST agree, so
neither computes it -- both import it from here.

Timing is DERIVED from measured audio, never authored. Every duration below
comes from ffprobe on a real take.
"""
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vo_lines import UNITS

VO_LEAD  = 0.10   # a unit cuts this much before its first line
TURN_GAP = 0.28   # between turns INSIDE a unit -- dialogue needs a beat
PHASE_GAP = 0.34  # between PHASES of a merged unit, slightly longer: the actor
                  # is rearranging, and the extra 60ms reads as a thought, not
                  # a stumble. Still well under a cut.
TAIL_PAD = 0.20   # after the last turn, before the unit hands over


@lru_cache(maxsize=None)
def dur(p):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip()
    if not out:
        raise SystemExit(f"cannot probe {p}")
    return float(out)


def walk():
    """[(unit_id, start, own_len, phases, turns)] where
         phases = [(name, rel_start, rel_len)]      -- relative to the unit
         turns  = [(turn_id, abs_start, len)]       -- absolute, for the root
    """
    out, t = [], 0.0
    for cid, phase_defs in UNITS:
        cur = round(t + VO_LEAD, 3)
        phases, turns = [], []
        for pi, (pname, tids) in enumerate(phase_defs):
            p0 = cur
            for ti, tid in enumerate(tids):
                wav = ROOT / "assets" / "voice" / f"{tid}.wav"
                if not wav.exists():
                    raise SystemExit(
                        f"missing {wav}\nTiming is derived from measured audio; "
                        f"generate the VO first (scripts/gen_vo.py).")
                L = dur(wav)
                turns.append((tid, round(cur, 3), round(L, 3)))
                cur = round(cur + L, 3)
                if ti + 1 < len(tids):
                    cur = round(cur + TURN_GAP, 3)
            phases.append((pname, round(p0 - t, 3), round(cur - p0, 3)))
            if pi + 1 < len(phase_defs):
                cur = round(cur + PHASE_GAP, 3)
        own = round(cur - t + TAIL_PAD, 3)
        out.append((cid, round(t, 3), own, phases, turns))
        t = round(t + own, 3)
    return out, round(t, 3)


if __name__ == "__main__":
    units, total = walk()
    print(f"{len(units)} units  total {total:.3f}s  "
          f"({int(total//60)}:{total%60:05.2f})")
    for cid, start, own, phases, _ in units:
        ph = " ".join(f"{n}@{s:.1f}+{l:.1f}" for n, s, l in phases)
        print(f"  {cid:14s} {start:7.3f} +{own:6.3f}   {ph}")
