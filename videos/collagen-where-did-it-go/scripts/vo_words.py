#!/usr/bin/env python3
"""Word normalisation shared by gen_vo.py (script<->ASR alignment),
build_captions.py (caption text) and check-vo.py.

One source, imported by all three -- two independent copies of the same
alias table is the drift this repo's CLAUDE.md warns about for generated
files. Ported from videos/ectoin-survival-molecule/scripts/vo_words.py and
re-derived for THIS script's vocabulary.
"""
import re

# The script speaks numbers as words (TTS-safe). Whisper usually writes them
# as digits. Both sides are merged to ONE alignment token per phrase so a
# numeral never costs an alignment match. Keys are lower-cased word tuples.
PHRASES = {
    ("twenty", "three"): "23",
    ("twenty", "twenty", "five"): "2025",
    ("five", "hundred"): "500",
    ("three", "hundred", "thousand"): "300000",
    ("vitamin", "c"): "vitaminc",
    ("ultra", "violet"): "ultraviolet",
    ("sun", "screen"): "sunscreen",
}

# ASR digit forms -> the same alignment token.
NUMERALS = {
    "23": "23", "twenty-three": "23",
    "2025": "2025", "2,025": "2025", "twenty-twenty-five": "2025",
    "500": "500", "five-hundred": "500",
    "300000": "300000", "300,000": "300000", "three-hundred-thousand": "300000",
}

# ASR normalises to US spelling; this channel writes UK. Alignment tokens are
# spelling-insensitive via this map; captions use the SCRIPTED spelling anyway.
UK = {
    "moisturizing": "moisturising", "moisturizer": "moisturiser",
    "moisturizers": "moisturisers", "randomized": "randomised",
    "ultra-violet": "ultraviolet", "aging": "ageing",
}

# On-screen / caption form of a spoken numeral phrase (display only; the
# alignment never touches this).
CAPTION_FORM = {
    "twenty twenty five": "2025",
    "twenty three": "23",
    "five hundred": "500",
    "three hundred thousand": "300,000",
}

# Words that MUST come back from the ASR as themselves (aligned `equal`).
# A garble on any of these is a re-roll, not a caption fix.
KEY_TERMS = {"collagen", "daltons", "retinoids", "peptides", "randomised",
             "ultraviolet", "sunscreen", "elasticity", "amino", "moisturising"}


def norm(word):
    """Lowercase, strip edge punctuation and internal apostrophes; map digit
    forms and UK/US spellings to one alignment token. Never used for display."""
    w = word.lower().strip(".,!?;:‘’“”\"'()[]")
    w = w.replace("’", "").replace("'", "")
    w = NUMERALS.get(w, w)
    w = UK.get(w, w)
    return w


def merge_phrases(tokens):
    """Merge PHRASES inside a list of normalised tokens.

    Returns (merged_tokens, spans) where spans[i] = (first_idx, last_idx) of
    the ORIGINAL token positions each merged token covers. Greedy, longest
    phrase first at each position, so "twenty twenty five" is not eaten by a
    shorter match."""
    keys = sorted(PHRASES, key=len, reverse=True)
    out, spans, i = [], [], 0
    while i < len(tokens):
        hit = None
        for k in keys:
            n = len(k)
            if tuple(tokens[i:i + n]) == k:
                hit = (PHRASES[k], n)
                break
        if hit:
            out.append(hit[0]); spans.append((i, i + hit[1] - 1)); i += hit[1]
        else:
            out.append(tokens[i]); spans.append((i, i)); i += 1
    return out, spans


def script_words(text):
    """The scripted text split into display words (keeps punctuation/casing)."""
    return [w for w in text.split() if norm(w)]


def caption_text(words):
    """Display words -> caption string with numeral phrases in display form."""
    s = " ".join(words)
    for spoken, shown in CAPTION_FORM.items():
        s = re.sub(r"\b" + spoken + r"\b", shown, s, flags=re.IGNORECASE)
    return s
