#!/usr/bin/env python3
"""Build captions/<slug>.srt and .vtt from the REAL word timings of each take.

One source of truth: the same corrected transcript feeds both files, so they
cannot drift from each other. Timings come from `hyperframes transcribe` on the
shipped takes, offset by each scene's absolute data-start -- never estimated.

Two disciplines the skill requires and that a naive build gets wrong:

  * ASR mangles exactly the vocabulary this channel depends on. "ectoin" came
    back as Ecton / ectoene / ectoy / echetoin across takes. CORRECTIONS below
    fixes the caption text; it does NOT touch the audio, and the TTS prompt is a
    separate concern (the two are allowed to diverge, and here they do).
  * A cue is a glance, not a mirror of the beat schedule. Max 2 lines, ~3-6
    words a line, and a hard 1.0s minimum on screen -- a hand-authored sidecar
    that simply mirrored element entrances produced 10 cues under 0.5s on an
    earlier project, the shortest 0.15s.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLUG = "ectoin-survival-molecule"
MIN_CUE_S, MAX_CUE_S, MAX_WORDS = 1.0, 5.5, 11

# ASR output -> what was actually said. Case-insensitive whole-word.
CORRECTIONS = {
    r"\bect(?:o)?(?:e|y|oy|ene|oene|etoin|oin)?\b": "ectoin",
    r"\bech?etoin\b": "ectoin", r"\becton\b": "ectoin", r"\bectoene\b": "ectoin",
    r"\bectoine\b": "ectoin", r"\bectoy\b": "ectoin",
    r"\bhalomonas\b": "Halomonas", r"\belongata\b": "elongata",
    r"\bbitop\b": "bitop", r"\bpubmed\b": "PubMed", r"\bk beauty\b": "K-beauty",
    r"\bpaula's choice\b": "Paula's Choice", r"\babib'?s?\b": "Abib's",
    r"\bpanthenol\b": "panthenol", r"\bsqualane\b": "squalane",
    # ASR normalises to US spelling; this channel's script is UK. The captions
    # should read as the channel writes, not as the recogniser guessed.
    r"\bfavorite\b": "favourite", r"\bmoisturizer\b": "moisturiser",
    r"\bmoisturizers\b": "moisturisers", r"\bmoisturization\b": "moisturisation",
    r"\brandomized\b": "randomised", r"\borganized\b": "organised",
    r"\bstabilize\b": "stabilise", r"\bstabilise\b": "stabilise",
    r"\bemphasized\b": "emphasised", r"\baging\b": "ageing",
    r"\bbehaviour\b": "behaviour", r"\bbehavior\b": "behaviour",
    r"\bjudgment\b": "judgement",
}


def correct(w):
    for pat, rep in CORRECTIONS.items():
        if re.fullmatch(pat, w, re.IGNORECASE):
            # preserve a leading capital if the original had one
            return rep.capitalize() if w[:1].isupper() and rep[:1].islower() else rep
    return w


def transcribe(wav):
    subprocess.run(["npx", "--yes", "hyperframes@0.8.22", "transcribe", str(wav),
                    "--engine", "whisper", "--model", "small.en", "--timeout", "300000"],
                   capture_output=True, cwd=ROOT)
    tp = ROOT / "assets" / "voice" / "transcript.json"
    return json.load(open(tp)) if tp.exists() else []


def group(words):
    """Greedy cue packing: break on sentence end, word count, or duration."""
    cues, cur = [], []
    for w in words:
        cur.append(w)
        span = cur[-1]["end"] - cur[0]["start"]
        ends_sentence = re.search(r"[.?!]$", cur[-1]["text"])
        # A comma is a legitimate break once the cue is already readable-length;
        # breaking there keeps a clause whole instead of splitting it across cues.
        ends_clause = re.search(r"[,;:]$", cur[-1]["text"]) and len(cur) >= 5 and span >= 1.6
        if ends_sentence or ends_clause or len(cur) >= MAX_WORDS or span >= MAX_CUE_S:
            cues.append(cur); cur = []
    if cur:
        cues.append(cur)
    # Merge any cue shorter than the readability floor into its neighbour.
    merged = []
    for c in cues:
        if merged and (c[-1]["end"] - c[0]["start"]) < MIN_CUE_S:
            merged[-1].extend(c)
        else:
            merged.append(c)
    return merged


def wrap(text):
    """<=2 lines, balanced, 3-6 words a line."""
    ws = text.split()
    if len(ws) <= 6:
        return text
    mid = (len(ws) + 1) // 2
    return " ".join(ws[:mid]) + "\n" + " ".join(ws[mid:])


def ts(t, sep=","):
    h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d}{sep}{int(round((s%1)*1000)):03d}"


def main():
    sys.path.insert(0, str(ROOT / "scripts"))
    from build_index import SCENES, TAIL_PAD, VO_LEAD, dur

    t, cues = 0.0, []
    for cid, n in SCENES:
        wav = ROOT / "assets" / "voice" / f"{n:02d}.wav"
        vlen = dur(wav)
        for g in group([{**w, "text": correct(w["text"])} for w in transcribe(wav)]):
            start = t + VO_LEAD + g[0]["start"]
            end = max(t + VO_LEAD + g[-1]["end"], start + MIN_CUE_S)
            cues.append((start, end, wrap(" ".join(w["text"] for w in g))))
        t = round(t + vlen + TAIL_PAD, 3)

    # No cue may outlast the next one's start.
    for i in range(len(cues) - 1):
        if cues[i][1] > cues[i + 1][0]:
            trimmed = cues[i + 1][0] - 0.02
            # Only trim if the cue stays readable; otherwise push the NEXT cue
            # later instead. Trimming blindly is what left one cue at 0.87s.
            if trimmed - cues[i][0] >= MIN_CUE_S:
                cues[i] = (cues[i][0], trimmed, cues[i][2])
            else:
                end = cues[i][0] + MIN_CUE_S
                cues[i] = (cues[i][0], end, cues[i][2])
                cues[i + 1] = (max(cues[i + 1][0], end + 0.02), cues[i + 1][1], cues[i + 1][2])

    out = ROOT / "captions"; out.mkdir(exist_ok=True)
    srt = "\n".join(f"{i+1}\n{ts(a)} --> {ts(b)}\n{x}\n" for i, (a, b, x) in enumerate(cues))
    vtt = "WEBVTT\n\n" + "\n".join(
        f"{ts(a,'.')} --> {ts(b,'.')}\n{x}\n" for a, b, x in cues)
    (out / f"{SLUG}.srt").write_text(srt)
    (out / f"{SLUG}.vtt").write_text(vtt)

    short = [c for c in cues if c[1] - c[0] < MIN_CUE_S - 0.01]
    print(f"  {len(cues)} cues -> captions/{SLUG}.srt + .vtt")
    print(f"  shortest {min(b-a for a,b,_ in cues):.2f}s, longest {max(b-a for a,b,_ in cues):.2f}s")
    print(f"  cues under the {MIN_CUE_S}s floor: {len(short)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
