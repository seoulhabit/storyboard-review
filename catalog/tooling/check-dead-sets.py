#!/usr/bin/env python3
"""Find tl.set() values that NEVER reach the screen.

The failure this catches, from 03-cell: a band stamped its text with
`tl.set(..., 0)` while a SECOND band in the same unit stamped different text at
16.95s. Seeking to the first band's cue at 39.7s replays both sets in order, so
it showed the other band's line. The video shipped with one caption repeated
and one that never appeared at all.

Detection needs no knowledge of intent: for each element, resolve which set is
in force at each moment the element is REVEALED (opacity -> 1). A set whose
value is in force at no reveal is dead -- it was authored and never seen.

An ordering check does NOT catch this and reports a clean 0 -- the two sets are
in ascending time order. It is the gap between a set and its use that matters,
not the order of the sets.
"""
import collections
import glob
import re
import sys
from pathlib import Path

SET = re.compile(r"tl\.set\('(#[\w-]+)',\s*\{\s*(textContent|className|innerHTML)\s*:\s*"
                 r"('(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\")[^}]*\}\s*,\s*([\d.]+)\s*\)")
# opacity -> 1 on the same element, however the tween is spelled/wrapped
REVEAL = re.compile(r"tl\.(?:to|fromTo)\('(#[\w-]+)',[^;]*?opacity:\s*1[^;]*?,\s*([\d.]+)\s*\)",
                    re.DOTALL)

def audit(path):
    src = Path(path).read_text()
    sets = collections.defaultdict(list)
    for m in SET.finditer(src):
        sets[m.group(1)].append((float(m.group(4)), m.group(2), m.group(3)))
    reveals = collections.defaultdict(list)
    for m in REVEAL.finditer(src):
        reveals[m.group(1)].append(float(m.group(2)))
    out = []
    for el, ss in sets.items():
        if len(ss) < 2:
            continue
        rv = sorted(reveals.get(el, []))
        seen = set()
        for t in rv:
            eff = [s for s in ss if s[0] <= t]
            if eff:
                seen.add(id(max(eff, key=lambda s: s[0])))
        for s in ss:
            if id(s) not in seen:
                out.append((el, s[0], s[1], s[2], len(rv)))
    return out

if __name__ == "__main__":
    files = sys.argv[1:] or sorted(glob.glob("compositions/frames/*.html"))
    total = 0
    for f in files:
        for el, t, prop, val, nrv in audit(f):
            print(f"  DEAD SET  {f.split('/')[-1]:16s} {el}.{prop}@{t:.2f} "
                  f"= {val[:46]}  (never in force at any of {nrv} reveal(s))")
            total += 1
    print(f"\n{total} dead set(s) across {len(files)} file(s)")
    sys.exit(1 if total else 0)
