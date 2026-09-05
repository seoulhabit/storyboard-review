#!/usr/bin/env python3
"""The single timing walk. build_frames.py, build_index.py, build_captions.py,
build_motion.py and check-seams.py all import walk() from here -- none of them
computes a scene's start/duration/word times independently, so they cannot
disagree with each other about where a scene sits.

Timing is DERIVED from measured, cut voiceover (scripts/gen_vo.py's output:
assets/voice/NN.wav + NN.words.json), never authored. A dead-tail hole is
impossible by construction: a scene's own span ends at its last word's end
time plus the next boundary's `seam_after`, not at some independently-guessed
clip length.

    seam_N       = last_word_end_abs(N-1) + seam_after(kind_into(N))
    first_word_N = seam_N + d(kind_into(N)) - j(kind_into(N))
    vo_start_N   = first_word_N - LEAD_KEEP
    own_N        = seam_{N+1} - seam_N
    emitted_dur  = own_N + d(kind_into(N+1))     -- 0 hold on the last scene
    gap_N        = seam_after + d - j            -- see transitions.KIND

Scene 1 has no incoming transition: first_word_1 = LEAD_KEEP, start_1 = 0.
The last scene's "next boundary" is synthetic: seam_last+1 = last_word_end +
END_TAIL, so `own` on the closing scene includes the closing hold and no
transition extends it further.
"""
import re
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOICE = ROOT / "assets" / "voice"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vo_lines import LINES
from transitions import KIND, kind_into, rest_after

LEAD_KEEP = 0.10
TAIL = 0.25
INTRA_GAP = 0.22
INTRA_GAP_OVERRIDES = {"20-twelve": 0.45, "21-verdict": 0.40, "19-limits": 0.35}
END_TAIL = 1.50
FADE_IN = 0.06
FADE_OUT = 0.08
# How far a stored sentence span may sit from the word it was cut from before
# Ctx.sent() calls the manifest inconsistent. Both writers round times to 3
# decimals and copy sentence ends verbatim off a word, so agreement is exact;
# 10ms is slack for rounding only, and sits far under this project's ~400ms
# mean word spacing, so it cannot accidentally accept a shifted span.
SENT_TOL = 0.010

ORDER = [cid for cid, _ in LINES]


def scene_n(cid):
    return int(cid.split("-")[0])


@lru_cache(maxsize=None)
def dur(p):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip()
    if not out:
        raise SystemExit(f"cannot probe {p}")
    return float(out)


def _load_manifest(cid):
    p = VOICE / f"{scene_n(cid):02d}.words.json"
    if not p.exists():
        raise SystemExit(
            f"missing {p}\nTiming is derived from CUT voiceover; run "
            f"scripts/gen_vo.py cut (or --from-takes) first.")
    import json
    return json.loads(p.read_text())


class Scene:
    __slots__ = ("cid", "n", "block", "start", "own", "hold", "kind_in",
                 "kind_out", "vo_start", "vo_len", "words", "sentences")

    def __init__(self, cid, n, block, start, own, hold, kind_in, kind_out,
                 vo_start, vo_len, words, sentences):
        self.cid, self.n, self.block = cid, n, block
        self.start, self.own, self.hold = start, own, hold
        self.kind_in, self.kind_out = kind_in, kind_out
        self.vo_start, self.vo_len = vo_start, vo_len
        self.words, self.sentences = words, sentences

    @property
    def dur(self):
        """Emitted duration: own span plus the hold under the NEXT wipe."""
        return round(self.own + self.hold, 3)

    @property
    def frame_offset(self):
        """vo_start expressed relative to this scene's OWN timeline (t=0 at
        `start`) -- what every word marker is actually measured against,
        since a scene's GSAP timeline runs from its own frame's t=0, not from
        the root's absolute clock."""
        return round(self.vo_start - self.start, 3)


def _clean(text):
    """Lowercased, punctuation-stripped, for case/punctuation-insensitive
    matching against an @w()/@we() marker's argument."""
    return re.sub(r"^[^\w]+|[^\w]+$", "", text).lower()


class Ctx:
    """Bound to one Scene; resolves @w/@we/@first/@last/@dur/@sent tokens to
    seconds on THIS scene's own timeline (see Scene.frame_offset)."""

    def __init__(self, scene):
        self.scene = scene

    def _rel(self, t):
        return round(self.scene.frame_offset + t, 3)

    def _matches(self, word):
        w = word.lower()
        return [x for x in self.scene.words if _clean(x["text"]) == w]

    def w(self, word, occurrence=1):
        m = self._matches(word)
        if len(m) < occurrence:
            avail = [x["text"] for x in self.scene.words]
            raise SystemExit(
                f"@w({word},{occurrence}) not found in scene {self.scene.cid} "
                f"(matched {len(m)}x). Words in this scene: {avail}")
        return self._rel(m[occurrence - 1]["start"])

    def we(self, word, occurrence=1):
        m = self._matches(word)
        if len(m) < occurrence:
            avail = [x["text"] for x in self.scene.words]
            raise SystemExit(
                f"@we({word},{occurrence}) not found in scene {self.scene.cid} "
                f"(matched {len(m)}x). Words in this scene: {avail}")
        return self._rel(m[occurrence - 1]["end"])

    def first(self):
        return self._rel(self.scene.words[0]["start"])

    def last(self):
        return self._rel(self.scene.words[-1]["end"])

    def dur(self):
        return self.scene.dur

    def sent(self, i):
        """The i-th sentence's start, on this scene's own timeline.

        UNLIKE @w/@we/@first/@last, this reads the manifest's `sentences`
        array, which is STORED derived data rather than the words themselves.
        A pass that rewrites `words` and forgets `sentences` leaves spans
        describing audio that no longer exists, and because @sent() is bound
        by no scene spec today, nothing would notice: scripts/repace_vo.py
        time-stretched nine scenes on 2026-09-05 and left their sentence spans
        on the pre-stretch clock, and every gate in the project stayed green.
        The first spec to reach for @sent() would have bound silently to times
        that are not in the audio. So this checks before it answers.

        A sentence is cut out of the word list -- its span IS some word's start
        and some (later) word's end -- so agreement is exact by construction,
        and SENT_TOL only absorbs rounding. Both ends are checked because
        start alone is not enough: in 29-cta, whose single authored rest landed
        on a sentence boundary, every stale sentence still started on a word
        and only the ends gave the staleness away.
        """
        if not 0 <= i < len(self.scene.sentences):
            raise SystemExit(
                f"@sent({i}) is out of range in scene {self.scene.cid}, which "
                f"has {len(self.scene.sentences)} sentence(s): "
                f"{[s['text'] for s in self.scene.sentences]}")
        s = self.scene.sentences[i]
        for field in ("start", "end"):
            t = s[field]
            if not any(abs(w[field] - t) <= SENT_TOL for w in self.scene.words):
                raise SystemExit(
                    f"scene {self.scene.cid}: @sent({i}) reads a sentence span "
                    f"no word matches -- {field}={t:.3f}s is not within "
                    f"{SENT_TOL * 1000:.0f}ms of any word's {field} "
                    f"({self.scene.words[0]['start']:.3f}-"
                    f"{self.scene.words[-1]['end']:.3f}s of speech).\n"
                    f"  sentence {i}: {s['text']!r}\n"
                    f"  assets/voice/{self.scene.n:02d}.words.json has words and "
                    f"sentences on different clocks -- re-run "
                    f"scripts/repace_vo.py (or gen_vo.py cut) to rebuild both "
                    f"together. Do NOT hand-edit the times.")
        return self._rel(s["start"])


def walk():
    """(scenes, total) -- scenes is [Scene, ...] in ORDER; total is the root
    composition duration."""
    manifests = {cid: _load_manifest(cid) for cid in ORDER}
    words = {cid: manifests[cid]["words"] for cid in ORDER}
    if any(len(words[cid]) == 0 for cid in ORDER):
        empty = [cid for cid in ORDER if not words[cid]]
        raise SystemExit(f"scene(s) with zero words -- cannot time: {empty}")

    # pass 1: seam (start) and vo_start/first-word-abs per scene, forward,
    # each depending only on the PREVIOUS scene's last word.
    starts, vo_starts, last_word_abs = {}, {}, {}
    seam = 0.0
    for i, cid in enumerate(ORDER):
        kind_in = kind_into(cid) if i > 0 else None
        if i == 0:
            start = 0.0
            first_word_abs = LEAD_KEEP
        else:
            start = seam
            d, _seam_after, j, _gap = KIND[kind_in]
            first_word_abs = round(seam + d - j, 3)
        vo_start = round(first_word_abs - LEAD_KEEP, 3)
        starts[cid] = start
        vo_starts[cid] = vo_start
        last_end = round(vo_start + words[cid][-1]["end"], 3)
        last_word_abs[cid] = last_end

        if i + 1 < len(ORDER):
            next_cid = ORDER[i + 1]
            d2, seam_after2, j2, gap2 = KIND[kind_into(next_cid)]
            # rest_after(cid) is authored air held after THIS scene's last word
            # (transitions.REST_AFTER); 0 for every scene the review did not
            # name, so the grammar is still what sets every other boundary.
            seam = round(last_end + seam_after2 + rest_after(cid), 3)
        else:
            seam = round(last_end + END_TAIL, 3)

    total = seam  # after the loop, `seam` is the synthetic end-of-video seam

    # pass 2: own/hold per scene from consecutive starts (+ vo_len from disk).
    scenes = []
    for i, cid in enumerate(ORDER):
        start = starts[cid]
        next_start = starts[ORDER[i + 1]] if i + 1 < len(ORDER) else total
        own = round(next_start - start, 3)
        kind_out = kind_into(ORDER[i + 1]) if i + 1 < len(ORDER) else None
        hold = KIND[kind_out][0] if kind_out else 0.0
        kind_in = kind_into(cid) if i > 0 else None
        m = manifests[cid]
        vo_len = dur(VOICE / f"{scene_n(cid):02d}.wav")
        # Scene.n is the AUDIO FILE NUMBER (assets/voice/NN.wav), derived from
        # the cid prefix -- NOT the sequential 1..28 position. They diverge
        # after the 09/10 merge (11-analogy is the 10th scene in ORDER but
        # its file is 11.wav): a build that used `i + 1` here wired every
        # scene from 11-analogy on to the WRONG audio file. scene_n(cid) is
        # the single source both gen_vo.py (writing the files) and this
        # walk (reading them) agree on.
        scenes.append(Scene(cid, scene_n(cid), m.get("block", cid), start, own,
                             hold, kind_in, kind_out, vo_starts[cid], vo_len,
                             m["words"], m["sentences"]))
    return scenes, total


def main():
    if "--words" in sys.argv:
        cid = sys.argv[sys.argv.index("--words") + 1]
        m = _load_manifest(cid)
        print(f"{cid}  {len(m['words'])} words  wpm={m.get('wpm')}  lufs={m.get('lufs')}")
        for w in m["words"]:
            print(f"  {w['start']:7.3f} - {w['end']:7.3f}  {w['text']}")
        return 0

    scenes, total = walk()
    print(f"{len(scenes)} scenes  total {total:.3f}s  "
          f"({int(total // 60)}:{total % 60:05.2f})")
    for s in scenes:
        print(f"  {s.cid:16s} start={s.start:8.3f} own={s.own:7.3f} "
              f"dur={s.dur:7.3f} hold={s.hold:.2f} in={s.kind_in or '-':9s} "
              f"vo={s.vo_start:8.3f}+{s.vo_len:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
