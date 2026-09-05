#!/usr/bin/env python3
"""Emit captions/<slug>.srt and .vtt from the master word manifest.

NO ASR CALL HERE. The manifest (assets/voice/master.words.json) already
carries every scripted word with its MEASURED time -- the same alignment the
frame generator's @w() markers are keyed to -- so a second transcription
could only disagree with the render. Text is the SCRIPTED spelling (UK,
punctuation intact); spoken numeral phrases are shown as numerals
(vo_words.CAPTION_FORM). No speaker prefixes: there is one narrator.

Cue discipline (a cue is a glance, not a mirror of the beat schedule):
  >= MIN_CUE_S on screen, <= MAX_WORDS words, break at sentence ends or
  long clauses, <= 2 balanced lines, <= MAX_LINE_CHARS per line.

Reading-speed rule, added after a review measured 20 of 53 cues over 20
characters/second (worst 36.0, "Sunscreen is not just about sunburn" held
0.74s -- itself later found to be a manifest bug, not the read; see
gen_vo.py's repair_implausible_runs). Two mechanisms, in order:
  1. TAIL EXTENSION: a cue's on-screen END is pushed into whatever silence
     already follows its last word (capped at TAIL_MAX_S, never crossing the
     next cue's start). This is free reading time nobody has to slow down
     for -- the words already finished; the caption just lingers.
  2. GAP-AWARE RE-SPLIT: if a cue is still over MAX_CPS_HARD after tail
     extension, it is split at its own largest internal inter-word gap and
     each half is checked again, recursively -- never re-timed, never
     stretched across silence that isn't there. A residual that survives
     down to a single word is a genuine speech-rate problem, not a caption
     problem, and is reported rather than hidden (matches the project's own
     residual-advisory pattern in gen_vo.py's verify).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLUG = "collagen-where-did-it-go"
MIN_CUE_S, PREF_MIN_CUE_S, MAX_CUE_S, MAX_WORDS = 1.0, 1.5, 5.5, 11
MAX_CPS_HARD, MAX_CPS_PREF = 20.0, 17.0
MAX_LINE_CHARS, MAX_LINES = 42, 2
TAIL_MAX_S = 0.30   # matches this project's own median inter-cue gap (0.22s);
                    # gains beyond this are marginal (measured on the pre-fix
                    # SRT: 0.30s already took cues over 20 CPS from 20 to 9).

sys.path.insert(0, str(ROOT / "scripts"))
from timing import walk
from vo_words import caption_text


def group(words):
    cues, cur = [], []
    for w in words:
        cur.append(w)
        span = cur[-1]["end"] - cur[0]["start"]
        ends_sentence = re.search(r"[.?!]$", cur[-1]["text"])
        ends_clause = re.search(r"[,;:]$", cur[-1]["text"]) and len(cur) >= 5 and span >= 1.6
        if ends_sentence or ends_clause or len(cur) >= MAX_WORDS or span >= MAX_CUE_S:
            cues.append(cur); cur = []
    if cur:
        cues.append(cur)
    return cues


def _cps(cue):
    span = cue[-1]["end"] - cue[0]["start"]
    chars = len(caption_text([w["text"] for w in cue]))
    return chars / span if span > 0 else 999.0


def _split_at_best_gap(cue):
    """Split at the single largest internal inter-word gap. None if the cue
    is one word (nothing left to split) or every word is edge-to-edge."""
    if len(cue) < 2:
        return None
    gaps = sorted(((cue[i + 1]["start"] - cue[i]["end"], i) for i in range(len(cue) - 1)),
                  reverse=True)
    gap, i = gaps[0]
    if gap <= 0:
        return None
    return cue[:i + 1], cue[i + 1:]


def enforce_cps(cue, depth=0):
    """Recursively split a cue at its own largest internal gap until every
    piece is at or under MAX_CPS_HARD. Never invents time that isn't there;
    a piece that can't be split further (or has no internal gap left) is a
    genuine speech-rate residual, not a caption-splitting one, and is kept
    as-is for the caller to report."""
    if _cps(cue) <= MAX_CPS_HARD or depth > 5:
        return [cue]
    split = _split_at_best_gap(cue)
    if split is None:
        return [cue]
    left, right = split
    if not left or not right:
        return [cue]
    return enforce_cps(left, depth + 1) + enforce_cps(right, depth + 1)


def would_fit(a, b):
    """Would merging word-groups a+b still respect the cue ceilings? A merge
    that blows past MAX_CUE_S/MAX_WORDS mashes two unrelated sentences onto
    one card -- worse than a short cue rescued by tail extension instead."""
    words = len(a) + len(b)
    span = b[-1]["end"] - a[0]["start"]
    return words <= MAX_WORDS and span <= MAX_CUE_S


def wrap(text):
    """<= MAX_LINES lines, each <= MAX_LINE_CHARS. Character-aware: a short
    cue stays on one line regardless of word count; a long one is split at
    the space nearest the midpoint that keeps both halves under the limit."""
    if len(text) <= MAX_LINE_CHARS:
        return text
    ws = text.split()
    best_i, best_d = None, None
    cur = ""
    for i in range(len(ws) - 1):
        cur = (cur + " " + ws[i]).strip() if cur else ws[i]
        rest = " ".join(ws[i + 1:])
        if len(cur) <= MAX_LINE_CHARS and len(rest) <= MAX_LINE_CHARS:
            d = abs(len(cur) - len(rest))
            if best_d is None or d < best_d:
                best_d, best_i = d, i
    if best_i is None:
        # No split keeps both halves under the limit (a very long single
        # word, or MAX_LINE_CHARS too tight for this cue's word lengths) --
        # fall back to the old midpoint-by-words split rather than failing.
        mid = (len(ws) + 1) // 2
        return " ".join(ws[:mid]) + "\n" + " ".join(ws[mid:])
    return " ".join(ws[:best_i + 1]) + "\n" + " ".join(ws[best_i + 1:])


def ts(t, sep=","):
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d}{sep}{int(round((s % 1) * 1000)):03d}"


def main():
    units, files, total, manifest = walk()
    raw = []   # (unit_index, word-group) -- pre-extension, pre-merge
    for ui, u in enumerate(units):
        if not u.spoken:
            continue
        for g in group(u.words):
            for piece in enforce_cps(g):
                raw.append((ui, piece))

    # Tail extension FIRST: a cue's natural duration often already reaches
    # MIN_CUE_S once it can borrow the silence before the next cue (which may
    # be in the next unit -- a real pause, often a transition). Extending
    # before deciding what still needs a merge means a rescue-by-merge only
    # ever fires on a cue that's genuinely too short even with that room.
    ext = []
    for i, (ui, g) in enumerate(raw):
        start = g[0]["start"]
        natural_end = g[-1]["end"]
        next_start = raw[i + 1][1][0]["start"] if i + 1 < len(raw) else natural_end + TAIL_MAX_S
        end = min(natural_end + TAIL_MAX_S, next_start - 0.02)
        ext.append([ui, start, max(end, natural_end), g])

    # Floor rescue: a cue still under MIN_CUE_S after ordinary tail extension
    # first tries reaching the floor by borrowing MORE of the real silence
    # ahead of it (the 1.0s floor is a harder requirement than the ordinary
    # TAIL_MAX_S cap) -- and only merges into a same-unit neighbour, and only
    # if the merge keeps both MAX_CUE_S and MAX_WORDS, so two unrelated
    # sentences are never mashed onto one card just to clear the floor.
    cues = []
    i = 0
    while i < len(ext):
        ui, start, end, g = ext[i]
        if end - start < MIN_CUE_S:
            next_start = ext[i + 1][1] if i + 1 < len(ext) else end + (MIN_CUE_S - (end - start))
            reachable = min(next_start - 0.02, start + MIN_CUE_S)
            if reachable - start >= MIN_CUE_S - 0.005:
                end = reachable
            elif i + 1 < len(ext) and ext[i + 1][0] == ui and would_fit(g, ext[i + 1][3]):
                nui, nstart, nend, ng = ext[i + 1]
                cues.append([start, max(nend, start + MIN_CUE_S), g + ng]); i += 2; continue
            elif cues and cues[-1][2][-1]["cid"] == g[0]["cid"] and would_fit(cues[-1][2], g):
                # No forward rescue available -- typically the LAST cue of a
                # unit, with only a transition's fixed gap ahead of it, not
                # real borrowable silence, and no next same-unit cue to merge
                # forward into. Merge BACKWARD into the previous, same-unit
                # cue instead of shipping a sub-floor card (e.g. a single
                # trailing word like "face." before an iris cut).
                cues[-1][1] = max(end, cues[-1][0] + MIN_CUE_S)
                cues[-1][2] = cues[-1][2] + g
                i += 1; continue
            # else: genuinely too short even after every rescue tried above
            # (an isolated short cue at a unit boundary with no same-unit
            # neighbour on either side to merge into) -- kept as-is and
            # reported, rather than merged across a scene change.
        cues.append([start, end, g]); i += 1

    cues = [[a, b, wrap(caption_text([w["text"] for w in g])), g] for a, b, g in cues]

    # Residual overlap repair (tail extension already caps at the next cue's
    # start minus 0.02s; this only catches a genuine floor push or merge
    # crossing into what follows).
    for i in range(len(cues) - 1):
        if cues[i][1] > cues[i + 1][0]:
            trimmed = cues[i + 1][0] - 0.02
            if trimmed - cues[i][0] >= MIN_CUE_S:
                cues[i][1] = trimmed
            else:
                end = cues[i][0] + MIN_CUE_S
                cues[i][1] = end
                cues[i + 1][0] = max(cues[i + 1][0], end + 0.02)

    out = ROOT / "captions"
    out.mkdir(exist_ok=True)
    srt = "\n".join(f"{i+1}\n{ts(a)} --> {ts(b)}\n{x}\n" for i, (a, b, x, _) in enumerate(cues))
    vtt = "WEBVTT\n\n" + "\n".join(f"{ts(a,'.')} --> {ts(b,'.')}\n{x}\n" for a, b, x, _ in cues)
    (out / f"{SLUG}.srt").write_text(srt)
    (out / f"{SLUG}.vtt").write_text(vtt)

    durs = [b - a for a, b, _, _ in cues]
    cps = [len(x.replace("\n", " ")) / (b - a) for a, b, x, _ in cues]
    lines = [ln for _, _, x, _ in cues for ln in x.split("\n")]
    over20 = sum(1 for c in cps if c > MAX_CPS_HARD)
    over17 = sum(1 for c in cps if c > MAX_CPS_PREF)
    short = sum(1 for d in durs if d < MIN_CUE_S - 0.01)
    long_lines = [ln for ln in lines if len(ln) > MAX_LINE_CHARS]
    print(f"  {len(cues)} cues -> captions/{SLUG}.srt + .vtt"
          f"{'  [VO MANIFEST: FAKE]' if manifest.get('source') == 'fake' else ''}")
    print(f"  shortest {min(durs):.2f}s, longest {max(durs):.2f}s, under the floor: {short}")
    print(f"  CPS: worst {max(cps):.1f}, over {MAX_CPS_HARD:.0f}: {over20}, "
          f"over {MAX_CPS_PREF:.0f}: {over17} ({(1 - over17/len(cps)):.0%} at or under {MAX_CPS_PREF:.0f})")
    print(f"  lines over {MAX_LINE_CHARS} chars: {len(long_lines)}"
          + (f"  worst: {max(long_lines, key=len)!r}" if long_lines else ""))
    if over20:
        print(f"  RESIDUAL over {MAX_CPS_HARD:.0f} CPS -- a speech-rate problem, not a caption one:")
        for a, b, x, g in cues:
            c = len(x.replace(chr(10), " ")) / (b - a)
            if c > MAX_CPS_HARD:
                print(f"    {a:6.2f}-{b:6.2f}  {c:5.1f} cps  {x.replace(chr(10), ' / ')!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
