#!/usr/bin/env python3
"""Word normalisation shared by gen_vo.py (script<->ASR alignment) and
build_captions.py (caption text correction).

CORRECTIONS lived in build_captions.py; moved here because gen_vo.py's `cut`
step needs the identical mapping to align the SCRIPTED word list (vo_lines.py)
against Whisper's ASR output when locating word boundaries to cut on. Two
independent copies of the same regex table is exactly the kind of drift this
project's CLAUDE.md warns about for generated files -- one source, imported
by both.
"""
import re

# ASR output -> what was actually said. Case-insensitive whole-word.
CORRECTIONS = {
    r"\bect(?:o)?(?:e|y|oy|ene|oene|etoin|oin)?\b": "ectoin",
    r"\bech?etoin\b": "ectoin", r"\becton\b": "ectoin", r"\bectoene\b": "ectoin",
    r"\bectoine\b": "ectoin", r"\bectoy\b": "ectoin",
    r"\bhalomonas\b": "Halomonas", r"\belongata\b": "elongata",
    r"\bbitop\b": "bitop", r"\bpubmed\b": "PubMed", r"\bk beauty\b": "K-beauty",
    r"\bpaula's choice\b": "Paula's Choice",
    r"\bpanthenol\b": "panthenol", r"\bsqualane\b": "squalane",
    # 2026-09-05: the maker names on the re-voiced 21-verdict. small.en returns
    # "BTOP" and "Cow"; whisper large-v3 reads all three correctly, so the audio
    # is right and only the transcript needs mapping back. A caption must never
    # ship the recogniser's guess at a company name.
    r"\bbtop\b": "bitop", r"\bb\.?\s?top\b": "bitop",
    r"\bcow\b": "Kao", r"\bkao\b": "Kao", r"\bmerck\b": "Merck",
    r"\babib'?s?\b": "Abib", r"\bceramides?\b": "ceramides",
    r"\bkeratin\b": "keratin", r"\bglycerin[e]?\b": "glycerin",
    r"\bhumectants?\b": "humectants", r"\bextremolyte\b": "extremolyte",
    r"\batopic\b": "atopic", r"\bdermatitis\b": "dermatitis",
    r"\bsoul\s?habit\b": "SeoulHabit", r"\bseoul\s?habit\b": "SeoulHabit",
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

# CAPTION-ONLY display forms. vo_lines.LINES is TTS-safe -- no em-dashes, no
# colons, and no hyphens where the engine would read one as a pause -- so a few
# words are spelled for the SYNTHESISER there and have to be spelled for the
# READER here. This map is applied to caption text only; it never touches
# alignment, the on-screen copy, or what is spoken.
CAPTION_FORM = {
    "bacteria made": "bacteria-made",
    "double blind": "double-blind",
    "K beauty": "K-beauty",
    "over cleansed": "over-cleansed",
    "fragrance free": "fragrance-free",
}


def caption_text(text):
    for a, b in CAPTION_FORM.items():
        text = re.sub(rf"\b{re.escape(a)}\b", b, text, flags=re.IGNORECASE)
    return text


# Number/percent aliases: how the TTS-safe script text (vo_lines.LINES) SPEAKS
# a numeral versus how Whisper is likely to transcribe it. Used only to align
# the scripted word sequence to the ASR word sequence when cutting a block into
# scenes -- never touches the caption text (build_captions keeps ASR timing but
# scripted SPELLING, so a caption always reads "104", not "a hundred and four").
NUMBER_ALIASES = {
    "104": "hundred and four", "65": "sixty five", "12": "twelve",
    "7%": "seven percent", "7": "seven", "2%": "two percent", "2": "two",
    "11%": "eleven percent", "11": "eleven", "5%": "five percent",
}


def correct(word):
    """Apply CORRECTIONS to one ASR word; preserves a leading capital."""
    for pat, rep in CORRECTIONS.items():
        if re.fullmatch(pat, word, re.IGNORECASE):
            return rep.capitalize() if word[:1].isupper() and rep[:1].islower() else rep
    return word


def norm(word):
    """Lowercase, strip punctuation, for ALIGNMENT matching only (not display)."""
    w = word.lower().strip(".,!?;:‘’“”\"'()")
    return NUMBER_ALIASES.get(w, w)


def script_words(text):
    """The scripted text, split into alignment tokens (lowercased, no punct)."""
    return [norm(w) for w in text.split() if norm(w)]
