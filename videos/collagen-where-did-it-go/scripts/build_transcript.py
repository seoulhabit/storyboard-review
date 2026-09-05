#!/usr/bin/env python3
"""Emit TRANSCRIPT.md + .html: the full narration, plus every fact this video
only conveys visually.

    python3 scripts/build_transcript.py

WHY THIS EXISTS. A caption track (captions/*.srt) carries the same words the
narration says, timed to the render -- it does not carry what is ONLY on
screen: numerals compared by size, the fixed order of a ranked list, a legend
explaining what a colour or a glyph means, or a caveat sitting beside a graphic
rather than spoken aloud. A viewer using a screen reader, or reading only the
transcript, gets none of that from the SRT alone. This is generated from the
same sources everything else in this project is (vo_lines.py for the text,
BRIEF.md's claim table for full citations, master.words.json for timestamps),
never hand-typed, for the same reason captions and SCRIPT.md are generated:
one source of truth, so a text edit cannot silently leave the transcript
behind.

NOT a replacement for the caption track. Captions are timed for a viewer
watching with the sound off; the transcript is read start to finish, at the
reader's own pace, and is the place the video's on-screen-only information
has to live in text form at all.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLUG = "collagen-where-did-it-go"

sys.path.insert(0, str(ROOT / "scripts"))
from vo_lines import SCENES, CITES, CLAIMS, ORDER, TEXT, WORDLESS  # noqa: E402

# Full citation, mirroring BRIEF.md's own "§Sourcing -- the claim table" --
# kept here as a second copy on purpose (the transcript must stand alone even
# if BRIEF.md is reorganised), not parsed from the markdown table. Keep in
# sync with BRIEF.md by hand; a mismatch there is a documentation bug, not a
# build one, since neither file is generated from the other.
CLAIM_SOURCES = {
    "C1": "Definitional -- collagen is a main structural protein of skin.",
    "C2": ("Fisher & Voorhees, J Investig Dermatol Symp Proc 1998;3(1):61-8 "
           "(PMID 9732061); companion Fisher et al., Photochem Photobiol 1999;69(2):154-7."),
    "C3": ("Bos & Meinardi, Exp Dermatol 2000;9(3):165-9 -- the \"500 dalton rule\" "
           "for what can cross the skin barrier."),
    "C3b": ("Definitional/textbook: tropocollagen is approximately 300,000 daltons "
            "(three ~95,000-dalton chains). Stated for scale against the 500-dalton "
            "limit -- Bos & Meinardi source the LIMIT, not collagen's own mass."),
    "C4": "Follows from C3 (too large to cross the barrier); no efficacy claim made.",
    "C5": "Definitional -- digestion breaks collagen into peptides and amino acids.",
    "C6": "Pu et al., Nutrients 2023;15(9):2080 -- 26 RCTs, n=1721.",
    "C7": ("Myung & Park, Am J Med 2025;138(9):1264-77 -- 23 RCTs, n=1474; the "
           "benefit is absent in the non-industry-funded and higher-quality subgroups."),
    "C8": "Morita, J Dermatol Sci 2007;48(3):169-75.",
    "C9": ("Kafi et al., Arch Dermatol 2007;143(5):606-12 -- topical retinol raised "
           "procollagen I and improved fine wrinkles."),
    "C10": ("UNSOURCED, editorial by decision: general dietary-adequacy advice, not "
            "a claim that a supplement has an effect. Carries no on-screen citation "
            "for the same reason."),
}

# Every fact this video conveys ONLY on screen -- the reason this file exists.
# (unit cid, note) -- placed after that unit's spoken text.
VISUAL_ONLY = {
    "02-promise": ('On screen: a field of 23 tiles represents the trials, with '
                   'industry-funded ones marked with a "$" as they are named. '
                   'A note beside the grid reads "tag pattern illustrative" -- '
                   'see the note on 12-filter below for why.'),
    "06-door": ('On screen: two size cards are compared directly -- "~500 daltons, '
                'the size limit" and "~300,000 daltons, one collagen molecule" -- '
                'so the ~600x size gap is a visual comparison as much as a spoken one.'),
    "10-trials": ('On screen: an illustrative effect-size meter (a horizontal bar '
                  'from "NO EFFECT" to "BENEFIT") visualises each stage of the '
                  'evidence; every instance of it carries the on-screen label '
                  '"illustrative scale, not the paper\'s values". The three named '
                  'outcomes (hydration, elasticity, wrinkles) each highlight a '
                  'band of the tile field as they are said.'),
    "12-filter": ('On screen: the trial-tile field is tagged with "$" (industry '
                  'funded) and "?" (lower quality) markers, and those tiles visibly '
                  'drop out of the field as each filter is named. IMPORTANT: Myung '
                  '& Park (2025) report subgroup RESULTS by funding source and '
                  'study quality, but do not publish per-subgroup trial counts -- '
                  'the tag pattern is a FIXED, illustrative set (the same tiles '
                  'flagged in the 02-promise foreshadow drop here), not a reported '
                  'count of how many trials were actually excluded. A permanent '
                  'on-screen note beside the tile grid says "tag pattern '
                  'illustrative" for this reason. The pooled count, 23, IS the '
                  'paper\'s own number. The pooled meter reads "BENEFIT", then '
                  '"NOT SIGNIFICANT" once industry-funded studies are removed, '
                  'then holds at "NOT SIGNIFICANT" once lower-quality studies are '
                  'also removed -- redundantly labelled in text, not colour alone, '
                  'since the two meter states (a coral/orange fill and a celadon/ '
                  'green fill used elsewhere in this scene) measure close enough '
                  'in lightness to be hard to tell apart without color vision.'),
    "14-hierarchy": ('On screen: the four recommendations are shown as a NUMBERED, '
                     'ranked list (1. daily sunscreen, 2. not smoking, 3. protein + '
                     'vitamin C, 4. topical retinoids if suitable) -- the ranking '
                     'itself, strongest evidence first, is a visual structure the '
                     'narration states once but does not repeat per item. Collagen '
                     'cream and powder are shown set apart from this list, under an '
                     '"optional" label, specifically so they are not read as a 5th '
                     'and 6th ranked recommendation.'),
}


def load_words():
    mp = ROOT / "assets" / "voice" / "master.words.json"
    return json.loads(mp.read_text()) if mp.exists() else None


def scene_time(manifest, cid):
    if not manifest:
        return None
    for sc in manifest.get("scenes", []):
        if sc["cid"] == cid:
            return sc["start"], sc["end"]
    return None


def ts(t):
    m, s = divmod(t, 60)
    return f"{int(m)}:{s:05.2f}"


def build_body():
    manifest = load_words()
    parts = []
    for cid in ORDER:
        if cid in WORDLESS:
            continue
        text = TEXT.get(cid, "")
        span = scene_time(manifest, cid)
        header = f"### {cid}"
        if span:
            header += f"  ({ts(span[0])}-{ts(span[1])})"
        block = [header, "", text]
        cite_chips = CITES.get(cid)
        claim_ids = CLAIMS.get(cid)
        if cite_chips or claim_ids:
            block.append("")
            if cite_chips:
                block.append(f"**On-screen citation:** {', '.join(cite_chips)}")
            if claim_ids:
                for c in claim_ids:
                    src = CLAIM_SOURCES.get(c, "(source not recorded)")
                    block.append(f"- **{c}:** {src}")
        note = VISUAL_ONLY.get(cid)
        if note:
            block.append("")
            block.append(f"**Visual-only information:** {note}")
        parts.append("\n".join(block))
    return "\n\n---\n\n".join(parts)


def build_markdown():
    body = build_body()
    return f"""# Transcript -- You Bought Collagen. Where Did It Actually Go?

One narrator. Full spoken text, in order, plus every fact this video conveys
ONLY on screen (a numeral comparison, a ranked list's order, a legend for a
graphic) -- not a caption file, and not a substitute for one; captions are
timed to the render for a viewer watching with the sound off, this is meant
to be read start to finish.

Generated from `scripts/vo_lines.py` (narration text), `BRIEF.md`'s claim
table (citations), and `assets/voice/master.words.json` (timestamps) by
`scripts/build_transcript.py` -- never hand-edited.

---

{body}

---

## Full source list

{chr(10).join(f"- **{c}:** {s}" for c, s in CLAIM_SOURCES.items())}
"""


def build_html(markdown_body):
    import html as _html
    import re
    # Minimal, dependency-free markdown-ish rendering: this is a small, fixed
    # document shape (##/### headers, **bold**, `code`, paragraphs, --- rules,
    # blank-line-separated blocks) -- not a general markdown renderer, so
    # blocks are split on BLANK LINES first (matching how markdown actually
    # groups text into paragraphs) rather than emitting one <p> per source
    # line, which would fracture every multi-line paragraph in this file into
    # a separate tag per line.
    def inline(s):
        s = _html.escape(s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        return s

    out = ["<!doctype html>", '<html lang="en"><head><meta charset="utf-8">',
           "<title>Transcript -- You Bought Collagen. Where Did It Actually Go?</title>",
           "<style>body{font-family:system-ui,sans-serif;max-width:720px;margin:40px auto;"
           "line-height:1.5;padding:0 20px;color:#131516;background:#F7F5F0}"
           "h1{font-size:28px}h3{font-size:20px;margin-top:2em}hr{border:none;"
           "border-top:1px solid #D9D3C6;margin:2em 0}li{margin:.3em 0}"
           "code{background:#F0EBE1;padding:1px 5px;border-radius:4px;"
           "font-family:ui-monospace,monospace;font-size:.92em}</style></head><body>"]

    for block in markdown_body.split("\n\n"):
        block = block.strip("\n")
        if not block.strip():
            continue
        block_lines = [ln for ln in block.split("\n") if ln.strip()]
        if block.strip() == "---":
            out.append("<hr>")
        elif block.startswith("### "):
            out.append(f"<h3>{inline(block[4:])}</h3>")
        elif block.startswith("## "):
            out.append(f"<h2>{inline(block[3:])}</h2>")
        elif block.startswith("# "):
            out.append(f"<h1>{inline(block[2:])}</h1>")
        elif all(ln.startswith("- ") for ln in block_lines):
            # A pure list block (the closing "Full source list").
            items = "".join(f"<li>{inline(ln[2:])}</li>" for ln in block_lines)
            out.append(f"<ul>{items}</ul>")
        elif len(block_lines) > 1 and all(ln.startswith("- ") for ln in block_lines[1:]):
            # build_body()'s "**On-screen citation:** ..." line followed by
            # one "- **Cn:** ..." item per claim -- a labelled paragraph
            # plus its own list, not one long run of list items.
            out.append(f"<p>{inline(block_lines[0])}</p>")
            items = "".join(f"<li>{inline(ln[2:])}</li>" for ln in block_lines[1:])
            out.append(f"<ul>{items}</ul>")
        else:
            # A single paragraph, possibly source-wrapped across several
            # raw lines for readability (this file's own intro text) --
            # joined with spaces into ONE <p>, not one <p> per source line
            # (the original bug: five tags for one wrapped paragraph).
            out.append(f"<p>{inline(' '.join(block_lines))}</p>")
    out.append("</body></html>")
    return "\n".join(out)


def main():
    md = build_markdown()
    (ROOT / "TRANSCRIPT.md").write_text(md)
    (ROOT / "TRANSCRIPT.html").write_text(build_html(md))
    n_units = sum(1 for cid in ORDER if cid not in WORDLESS)
    n_visual_notes = len(VISUAL_ONLY)
    print(f"  TRANSCRIPT.md + .html  {n_units} spoken units, "
          f"{n_visual_notes} visual-only annotations, {len(CLAIM_SOURCES)} sourced claims")
    return 0


if __name__ == "__main__":
    sys.exit(main())
