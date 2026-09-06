#!/usr/bin/env python3
"""The SFX cue table, anchored on WORDS (never on seconds), consumed by
build_index.py. Restrained by design: nine physical events -- two opening
impacts (cream stopping, powder starting to fragment), a UV mesh-snap, the
cream's rejection at the barrier, digestion fragmenting, the 23 landing, two
filter drops, one lock-in. The
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
    ("01-hook",    "w", "stops",     1,  0.00, "impact-bass-2.mp3",         0.34, "cream stops at the surface"),
    ("01-hook",    "w", "apart",     1, -0.05, "fragment.wav",              0.22, "powder breaking apart (preview)"),
    ("03-uv",      "w", "down",      1, -0.05, "slice.wav",                 0.30, "UV snaps a mesh fibre"),
    ("04-barrier", "w", "through",   1, -0.05, "impact-bass-2.mp3",         0.22, "molecule rejected, doesn't get through"),
    ("06-swallow", "w", "breaks",    1,  0.00, "fragment.wav",              0.28, "molecule fragments in digestion"),
    ("08-trials",  "w", "three",     1,  0.00, "citation-tick-trimmed.mp3", 0.30, "23 lands (the 2025 pooled n)"),
    ("10-filter",  "w", "exclude",   1,  0.00, "filter.wav",                0.26, "industry-funded tiles drop"),
    ("10-filter",  "w", "keep",      1,  0.00, "filter.wav",                0.26, "low-quality tiles drop"),
    ("12-recs",    "w", "sunscreen", 1,  0.10, "lock.wav",                  0.30, "sunscreen locks in as a shield"),
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
