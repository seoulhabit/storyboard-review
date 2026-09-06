#!/usr/bin/env python3
"""The single timing walk. build_frames.py, build_index.py, build_captions.py,
build_motion.py, build_bgm.py, sfx.py and the gates all import walk() from
here -- none of them computes a unit's start/duration/word time on its own,
so they cannot disagree about where anything sits.

Timing is DERIVED from the measured, cut master narration
(assets/voice/master.wav + master.words.json, written by scripts/gen_vo.py),
never authored. The master is ONE audio clip at root t=0, so master time IS
root time; a unit's span is defined by its own words:

    start_1        = 0            first_word_1 = LEAD_KEEP  (0.10s -- the hook
                                  starts speaking before anyone can leave)
    start_N        = last_word_end(N-1) + seam_after(kind_into(N))
    first_word_N   = start_N + d - j          (asserted against the manifest)
    own_N          = start_{N+1} - start_N
    hold_N         = d(kind_into(N+1)) at a file boundary, else 0
    start_end      = last_word_end(15) + seam_after(curtain); own = END_CARD_HOLD

Units are grouped into composition FILES at every visible transition (see
transitions.BOUNDARIES): a file's timeline runs from its first unit's start,
so every marker Ctx resolves is FILE-relative.
"""
import json
import re
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOICE = ROOT / "assets" / "voice"
MASTER = VOICE / "master.wav"
MANIFEST = VOICE / "master.words.json"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vo_lines import ORDER, WORDLESS, TEXT
from vo_words import norm
from transitions import KIND, kind_into, is_file_boundary

LEAD_KEEP = 0.10      # master audio kept before word 1; word 1 starts HERE
TAIL = 0.25           # digital silence after the last word of the master
INTRA_GAP = 0.16      # a sentence pause inside a unit, after compression.
                      # 77 of these in the cut master, so every 10ms here is
                      # 0.8s of runtime; 0.16 still reads as a breath at pace.
END_CARD_HOLD = 5.0   # the wordless end card's own span (brief: a 3-5s calm end screen)
FADE_IN = 0.06        # master clip volume lane; ends before word 1 at 0.10
FADE_OUT = 0.08       # sits inside TAIL

# Composition file that a unit lands in: a new file starts at every unit whose
# incoming transition is visible. Names default to the first unit's cid; the
# evidence file is named for the mode, not its first beat.
FILE_NAMES = {"08-trials": "05-evidence"}


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True)


@lru_cache(maxsize=None)
def master_len():
    out = sh("ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(MASTER)).stdout.strip()
    if not out:
        raise SystemExit(f"cannot probe {MASTER} -- run scripts/gen_vo.py cut (or fake)")
    return float(out)


def load_manifest():
    if not MANIFEST.exists():
        raise SystemExit(f"missing {MANIFEST}\nTiming is derived from the CUT master; "
                         f"run scripts/gen_vo.py cut (or `gen_vo.py fake` to build "
                         f"without audio).")
    return json.loads(MANIFEST.read_text())


class Unit:
    __slots__ = ("cid", "i", "start", "own", "hold", "kind_in", "kind_out",
                 "words", "sentences", "first_word_abs", "last_word_abs",
                 "file", "file_start", "file_index")

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))

    @property
    def dur(self):
        """Emitted span of this unit: own plus the hold under the NEXT wipe."""
        return round(self.own + self.hold, 3)

    @property
    def spoken(self):
        return self.cid not in WORDLESS


class FileSpan:
    __slots__ = ("cid", "units", "start", "own", "hold", "kind_in", "kind_out")

    def __init__(self, cid, units, kind_in):
        self.cid, self.units, self.kind_in = cid, units, kind_in
        self.start = units[0].start
        self.own = round(sum(u.own for u in units), 3)
        self.hold = units[-1].hold
        self.kind_out = units[-1].kind_out

    @property
    def dur(self):
        return round(self.own + self.hold, 3)


def _clean(text):
    return norm(text)


class Ctx:
    """Bound to one Unit; resolves @w/@we/@first/@last/@sent/@ustart/@uend
    tokens to seconds on the unit's FILE timeline (t=0 at file_start)."""

    def __init__(self, unit):
        self.unit = unit

    def _rel(self, t_abs):
        return round(t_abs - self.unit.file_start, 3)

    def _matches(self, word):
        w = norm(word)
        return [x for x in self.unit.words if _clean(x["text"]) == w]

    def _find(self, word, occ):
        m = self._matches(word)
        if len(m) < occ:
            avail = [x["text"] for x in self.unit.words]
            raise SystemExit(
                f"@w({word},{occ}) not found in unit {self.unit.cid} "
                f"(matched {len(m)}x). Words in this unit: {avail}")
        return m[occ - 1]

    def w(self, word, occ=1):      return self._rel(self._find(word, occ)["start"])
    def we(self, word, occ=1):     return self._rel(self._find(word, occ)["end"])
    def w_abs(self, word, occ=1):  return round(self._find(word, occ)["start"], 3)
    def we_abs(self, word, occ=1): return round(self._find(word, occ)["end"], 3)
    def first(self):               return self._rel(self.unit.first_word_abs)
    def last(self):                return self._rel(self.unit.last_word_abs)
    def sent(self, i):             return self._rel(self.unit.sentences[i]["start"])
    def sent_end(self, i):         return self._rel(self.unit.sentences[i]["end"])
    def ustart(self):              return self._rel(self.unit.start)
    def uend(self):                return self._rel(self.unit.start + self.unit.own)
    def own(self):                 return self.unit.own


def walk():
    """(units, files, total, manifest)."""
    m = load_manifest()
    words_all = m["words"]
    by_cid = {}
    for w in words_all:
        by_cid.setdefault(w["cid"], []).append(w)
    sents_by_cid = {}
    for s in m["sentences"]:
        sents_by_cid.setdefault(s["cid"], []).append(s)
    for cid in ORDER:
        if cid in WORDLESS:
            continue
        if not by_cid.get(cid):
            raise SystemExit(f"unit {cid} has zero words in {MANIFEST.name} -- cannot time")

    # pass 1: starts, forward, each depending only on the previous unit's last word
    starts, last_abs, first_abs = {}, {}, {}
    prev = None
    for i, cid in enumerate(ORDER):
        kind = kind_into(cid) if i else None
        if i == 0:
            start = 0.0
        else:
            d, sa, j, gap = KIND[kind]
            start = round(last_abs[prev] + sa, 3)
        starts[cid] = start
        if cid in WORDLESS:
            first_abs[cid] = None
            last_abs[cid] = round(start + END_CARD_HOLD, 3)
        else:
            ws = by_cid[cid]
            first_abs[cid] = ws[0]["start"]
            last_abs[cid] = ws[-1]["end"]
            expected = LEAD_KEEP if i == 0 else round(start + KIND[kind][0] - KIND[kind][2], 3)
            if abs(first_abs[cid] - expected) > 0.02:
                raise SystemExit(
                    f"{cid}: first word at {first_abs[cid]:.3f}s but the seam grammar "
                    f"expects {expected:.3f}s ({kind or 'start'}). The manifest and "
                    f"transitions.KIND disagree -- re-run `scripts/gen_vo.py cut`.")
        prev = cid
    total = last_abs[ORDER[-1]]   # the end card's own span closes the piece

    # pass 2: own / hold / files
    units = []
    for i, cid in enumerate(ORDER):
        nxt = ORDER[i + 1] if i + 1 < len(ORDER) else None
        own = round((starts[nxt] if nxt else total) - starts[cid], 3)
        kind_out = kind_into(nxt) if nxt else None
        hold = KIND[kind_out][0] if (nxt and is_file_boundary(nxt)) else 0.0
        units.append(Unit(cid=cid, i=i, start=starts[cid], own=own, hold=hold,
                          kind_in=(kind_into(cid) if i else None), kind_out=kind_out,
                          words=by_cid.get(cid, []), sentences=sents_by_cid.get(cid, []),
                          first_word_abs=first_abs[cid], last_word_abs=last_abs[cid]))
    files, cur = [], []
    for u in units:
        if cur and is_file_boundary(u.cid):
            files.append(cur); cur = []
        cur.append(u)
    files.append(cur)
    spans = []
    for fi, group in enumerate(files):
        fcid = FILE_NAMES.get(group[0].cid, group[0].cid)
        for u in group:
            u.file, u.file_start, u.file_index = fcid, group[0].start, fi
        spans.append(FileSpan(fcid, group, group[0].kind_in))
    return units, spans, round(total, 3), m


def main():
    if "--words" in sys.argv:
        cid = sys.argv[sys.argv.index("--words") + 1]
        units, _, _, _ = walk()
        u = next(x for x in units if x.cid == cid)
        print(f"{cid}  file {u.file} (file t0 = {u.file_start:.3f})  {len(u.words)} words")
        for w in u.words:
            print(f"  {w['start']:8.3f} - {w['end']:8.3f}  ({w['start']-u.file_start:7.3f} file)  {w['text']}")
        return 0
    units, files, total, m = walk()
    print(f"{len(units)} units in {len(files)} files  total {total:.3f}s "
          f"({int(total // 60)}:{total % 60:05.2f})  manifest source={m.get('source')}")
    for f in files:
        print(f"  FILE {f.cid:14s} start={f.start:8.3f} own={f.own:7.3f} dur={f.dur:7.3f} in={f.kind_in or '-'}")
        for u in f.units:
            fw = f"{u.first_word_abs:8.3f}" if u.first_word_abs is not None else "       -"
            print(f"     {u.cid:14s} start={u.start:8.3f} own={u.own:7.3f} hold={u.hold:.2f} "
                  f"in={u.kind_in or '-':7s} first={fw} last={u.last_word_abs:8.3f} "
                  f"words={len(u.words)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
