#!/usr/bin/env python3
"""Build captions/<slug>.srt and .vtt from the CUT voiceover manifests.

NO ASR CALL HERE ANY MORE. Timing.walk() already carries every scene's word
list (assets/voice/NN.words.json, produced once by scripts/gen_vo.py cut) with
ASR timing -- re-transcribing to build captions risked a second ASR pass
disagreeing with the one the render's own word-marker bindings are keyed to.

Two disciplines the skill requires and that a naive build gets wrong, both
still true here:

  * ASR mangles exactly the vocabulary this channel depends on. "ectoin" came
    back as Ecton / ectoene / ectoy / echetoin across takes. Captions use the
    SCRIPTED spelling (vo_lines.LINES / TEXT), aligned onto the ASR word
    TIMING via the same difflib alignment gen_vo.py uses to cut scenes --
    never the raw ASR text. vo_words.CORRECTIONS is kept as a fallback for any
    word alignment does not confidently cover.
  * A cue is a glance, not a mirror of the beat schedule. Max 2 lines, ~3-6
    words a line, and a hard 1.0s minimum on screen -- a hand-authored sidecar
    that simply mirrored element entrances produced 10 cues under 0.5s on an
    earlier project, the shortest 0.15s.
"""
import difflib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLUG = "ectoin-survival-molecule"
MIN_CUE_S, MAX_CUE_S, MAX_WORDS = 1.0, 5.5, 11
# The review's line discipline: at most two lines, roughly 32-42 characters each.
# The predecessor capped WORDS only and split at the midpoint, so an 11-word cue
# of long words could produce a 55-character line -- a word count is not a line
# length. Both caps are enforced now, the character one at cue level as well as
# at wrap level, because a wrapper cannot fix a cue that was packed too long.
MAX_LINE_CHARS = 42
MAX_CUE_CHARS = MAX_LINE_CHARS * 2

# Cue placement. Default is the player's own bottom position; scenes listed here
# carry content in the lower third that a bottom caption would sit on top of, so
# their cues move to the top instead. Verified against rendered frames, not
# guessed from the source: each entry names what is actually down there.
# CUE PLACEMENT, MEASURED. The first version of this table was hand-authored
# from reading the scene sources -- "the lower third looks busy here" -- and it
# was wrong for half the piece: 19-limits, 21-verdict, 23-numbers, 24-eleven and
# 29-cta all have a CLEARER bottom band than top, because this is a full-frame
# editorial layout rather than a lower-third one. Several scenes hold a 36px
# kicker just under the safe line, which a top caption lands straight on.
#
# So it is measured instead. For each scene, `scripts/measure_cue_bands.py`
# samples four frames of the render and takes the 99.9th-percentile local
# gradient (text has sharp edges; a photographic plate at this scale does not)
# in the two bands a caption can occupy -- top y162-330, bottom y840-1000, both
# x300-1620. A cue goes top only where the top band is clearly emptier.
#
# Regenerate with:  python3 scripts/measure_cue_bands.py <render.mp4>
#
# Measured 2026-09-05 on ..._a11y-master.mp4 (top / bottom sharpness):
TOP_CUE_SCENES = {
    "02-osmosis":    (45, 185), "03-now":        (73, 173),
    "06-mechanism":  (72, 189), "07-question":   (75, 189),
    "12-load":      (181, 200), "22-whofor":     (25, 196),
    "25-formula":    (70, 186), "26-kbeauty":    (40, 201),
    "27-resilience":(160, 182), "28-remember":   (69, 192),
}


def cue_is_top(cid, local_start=None):
    return cid in TOP_CUE_SCENES


# WebVTT line positions. `line:N%` is the cue box's top edge as a share of frame
# height. 10% is 108px, which lands ON the kicker band -- several scenes set a
# 36px mono label just under the safe line, and a top-placed caption sat on top
# of "ABIB - ECTOIN PANTHENOL 11%" in the burned-in cut. 15% is 162px, clear of
# a kicker at 54-115. The default (no setting) leaves the player's own bottom
# placement alone, which is where a viewer expects captions.
VTT_TOP = "line:15%,align:center"
VTT_BOTTOM = "line:-3,align:center"

sys.path.insert(0, str(ROOT / "scripts"))
from vo_words import CORRECTIONS, caption_text, norm
from vo_lines import TEXT
from timing import walk


def correct(w):
    for pat, rep in CORRECTIONS.items():
        if re.fullmatch(pat, w, re.IGNORECASE):
            return rep.capitalize() if w[:1].isupper() and rep[:1].islower() else rep
    return w


def scripted_words(scene):
    """[{'text': scripted spelling, 'start', 'end'}] in absolute time.

    DRIVEN FROM THE SCRIPT, not from the ASR. The predecessor walked the ASR
    token list and mapped each token to at most one scripted word, so wherever
    the recogniser COLLAPSED two spoken words into one token the extra scripted
    word was silently dropped: "Paula's Choice says seven percent" shipped as
    "Paula's Choice says seven", and 24-eleven lost "percent" twice. Whisper
    writes "7%" for "seven percent" and "104" for "a hundred and four", so this
    is not an edge case on this channel, it is the normal case.

    Building from the script instead means every scripted word reaches the
    caption; several words sharing one ASR token split that token's span
    between them, and a scripted word with no token at all borrows the seam
    between its neighbours."""
    script_disp = TEXT[scene.cid].split()
    script_norm = [norm(w) for w in script_disp]
    asr = scene.words
    asr_norm = [norm(w["text"]) for w in asr]
    sm = difflib.SequenceMatcher(None, script_norm, asr_norm, autojunk=False)

    def at(j):
        w = asr[j]
        return (scene.vo_start + w["start"], scene.vo_start + w["end"])

    spans = [None] * len(script_disp)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                spans[i1 + k] = at(j1 + k)
        elif tag in ("replace", "delete") and i2 > i1:
            if j2 > j1:
                # Share the matched ASR span across the scripted words it
                # covers, in order, so none of them is left without a time.
                a, b = at(j1)[0], at(j2 - 1)[1]
                n = i2 - i1
                step = (b - a) / n
                for k in range(n):
                    spans[i1 + k] = (a + k * step, a + (k + 1) * step)
            # tag == "delete" with no ASR span is filled in below.

    # Any word still unplaced sits between its nearest placed neighbours.
    for i, sp in enumerate(spans):
        if sp is not None:
            continue
        prev = next((spans[k] for k in range(i - 1, -1, -1) if spans[k]), None)
        nxt = next((spans[k] for k in range(i + 1, len(spans)) if spans[k]), None)
        if prev and nxt:
            spans[i] = (prev[1], max(prev[1] + 0.05, nxt[0]))
        elif prev:
            spans[i] = (prev[1], prev[1] + 0.20)
        elif nxt:
            spans[i] = (max(0.0, nxt[0] - 0.20), nxt[0])
        else:
            spans[i] = (scene.vo_start, scene.vo_start + 0.20)

    # Monotonic, non-zero-length.
    out, last = [], None
    for disp, (a, b) in zip(script_disp, spans):
        if last is not None and a < last:
            a = last
        b = max(b, a + 0.02)
        last = b
        out.append({"text": correct(disp),
                    "start": round(a, 3), "end": round(b, 3)})
    return out


def group(words):
    """Greedy cue packing: break on sentence end, word count, or duration."""
    cues, cur = [], []
    for w in words:
        cur.append(w)
        span = cur[-1]["end"] - cur[0]["start"]
        chars = sum(len(x["text"]) for x in cur) + len(cur) - 1
        ends_sentence = re.search(r"[.?!]$", cur[-1]["text"])
        ends_clause = re.search(r"[,;:]$", cur[-1]["text"]) and len(cur) >= 5 and span >= 1.6
        if (ends_sentence or ends_clause or len(cur) >= MAX_WORDS
                or chars >= MAX_CUE_CHARS or span >= MAX_CUE_S):
            cues.append(cur)
            cur = []
    if cur:
        cues.append(cur)
    merged = []
    for c in cues:
        if merged and (c[-1]["end"] - c[0]["start"]) < MIN_CUE_S:
            merged[-1].extend(c)
        else:
            merged.append(c)
    return merged


def wrap(text):
    """<=2 lines, each <=MAX_LINE_CHARS, broken as late as the cap allows.

    Balanced-at-the-midpoint reads better than ragged ONLY while both halves
    fit; past the cap it just makes two long lines instead of one. So: fill the
    first line as far as the cap, then prefer the balanced split when that also
    fits, because a phrase break beats an arbitrary one."""
    if len(text) <= MAX_LINE_CHARS:
        return text
    ws = text.split()
    # latest word index whose prefix still fits the cap
    cut, run = 0, 0
    for i, w in enumerate(ws):
        add = len(w) + (1 if run else 0)
        if run + add > MAX_LINE_CHARS:
            break
        run += add
        cut = i + 1
    cut = max(1, cut)
    mid = (len(ws) + 1) // 2
    if mid <= cut and len(" ".join(ws[mid:])) <= MAX_LINE_CHARS:
        cut = mid
    return " ".join(ws[:cut]) + "\n" + " ".join(ws[cut:])


def ts(t, sep=","):
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d}{sep}{int(round((s % 1) * 1000)):03d}"


def main():
    scenes, total = walk()
    cues = []
    for s in scenes:
        for g in group(scripted_words(s)):
            start = g[0]["start"]
            end = max(g[-1]["end"], start + MIN_CUE_S)
            # caption_text is PHRASE-level ("bacteria made" -> "bacteria-made"),
            # so it runs on the assembled cue. Applied per word it silently
            # matches nothing, which is how the hyphens went missing.
            text = caption_text(" ".join(w["text"] for w in g))
            cues.append([start, end, wrap(text), s.cid])

    # Non-speech cues, and ONLY where they carry information. The bed opens the
    # piece under no narration and resolves under the end card; the transition
    # chimes and the impact hit are decorative punctuation on beats the picture
    # already makes, and captioning each one would bury the dialogue.
    first_word = cues[0][0]
    if first_word >= 1.2:
        cues.insert(0, [0.20, round(min(first_word - 0.10, 2.20), 3),
                        "[soft music]", "01-hook"])
    # After the last word, not at a fixed offset from the end -- anchored to
    # `total` it collided with the end card's own line and the overlap fixer
    # then clipped the spoken cue to the 1.0s floor.
    last_end = max(c[1] for c in cues)
    if total - last_end >= MIN_CUE_S + 0.3:
        cues.append([round(last_end + 0.25, 3), round(total - 0.20, 3),
                     "[soft music fades]", "30-endcard"])
    cues.sort(key=lambda c: c[0])

    # No cue may outlast the next one's start.
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
    # SRT carries no positioning: cue placement is not portably supported there
    # and players disagree about the coordinate space, so a positioned SRT is a
    # guess. The VTT is the positioned deliverable; the SRT is the plain one.
    srt = "\n".join(f"{i+1}\n{ts(a)} --> {ts(b)}\n{x}\n"
                    for i, (a, b, x, _cid) in enumerate(cues))
    vtt_lines = ["WEBVTT", ""]
    starts = {s.cid: s.start for s in scenes}
    for a, b, x, cid in cues:
        setting = VTT_TOP if cue_is_top(cid, a - starts[cid]) else VTT_BOTTOM
        vtt_lines.append(f"{ts(a,'.')} --> {ts(b,'.')} {setting}")
        vtt_lines.append(x)
        vtt_lines.append("")
    (out / f"{SLUG}.srt").write_text(srt)
    (out / f"{SLUG}.vtt").write_text("\n".join(vtt_lines))

    short = [c for c in cues if c[1] - c[0] < MIN_CUE_S - 0.01]
    longest_line = max(len(l) for _a, _b, x, _c in cues for l in x.split("\n"))
    over = [x for _a, _b, x, _c in cues
            if any(len(l) > MAX_LINE_CHARS for l in x.split("\n"))
            or x.count("\n") > 1]
    moved = sum(1 for c in cues if cue_is_top(c[3], c[0] - starts[c[3]]))
    print(f"  {len(cues)} cues -> captions/{SLUG}.srt + .vtt")
    print(f"  shortest {min(b-a for a,b,_,_ in cues):.2f}s, "
          f"longest {max(b-a for a,b,_,_ in cues):.2f}s")
    print(f"  cues under the {MIN_CUE_S}s floor: {len(short)}")
    print(f"  longest line {longest_line} chars (cap {MAX_LINE_CHARS}); "
          f"over cap or >2 lines: {len(over)}")
    print(f"  {moved} cue(s) moved to the top over lower-third content")
    return 1 if (short or over) else 0


if __name__ == "__main__":
    sys.exit(main())
