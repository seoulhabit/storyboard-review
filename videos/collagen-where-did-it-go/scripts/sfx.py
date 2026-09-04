#!/usr/bin/env python3
"""The SFX cue table, anchored on WORDS (never on seconds), consumed by
build_index.py. Restrained by design: six physical events only -- impact,
slice, fragmentation, the 23 landing, two filter drops, one lock-in. The
peak of each file lands on its word (offsets from assets/sfx/peaks.json,
written by make_sfx.py), so a hit never trails the thing it punctuates.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SFX_DIR = ROOT / "assets" / "sfx"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from timing import Ctx

# (unit cid, fn, word, occurrence, offset s, file, level, note)
CUES = [
    ("01-hook",       "w",  "replace",   1,  0.00, "impact-bass-2.mp3",         0.34, "molecule hits the barrier"),
    ("04-demolition", "w",  "apart",     1, -0.05, "slice.wav",                 0.30, "UV cuts a beam"),
    ("08-digestion",  "w",  "breaks",    1,  0.00, "fragment.wav",              0.28, "molecule fragments"),
    ("10-trials",     "we", "trials",    1, -0.10, "citation-tick-trimmed.mp3", 0.30, "23 lands"),
    ("12-filter",     "w",  "keep",      1,  0.00, "filter.wav",                0.26, "industry-funded tiles drop"),
    ("12-filter",     "w",  "keep",      2,  0.00, "filter.wav",                0.26, "low-quality tiles drop"),
    ("14-hierarchy",  "w",  "sunscreen", 1,  0.10, "lock.wav",                  0.30, "sunscreen locks into the foundation"),
]


def peaks():
    p = SFX_DIR / "peaks.json"
    if not p.exists():
        raise SystemExit("assets/sfx/peaks.json missing -- run scripts/make_sfx.py")
    return json.loads(p.read_text())


def cues(units):
    """[(at_abs, file, duration, level, note)] sorted by time."""
    pk = peaks()
    by = {u.cid: u for u in units}
    out = []
    for cid, fn, word, occ, off, fname, level, note in CUES:
        ctx = Ctx(by[cid])
        t = (ctx.w_abs if fn == "w" else ctx.we_abs)(word, occ)
        info = pk[fname]
        at = max(0.0, round(t + off - info["peak_offset"], 3))
        out.append((at, fname, info["duration"], level, note))
    return sorted(out)
