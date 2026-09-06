#!/usr/bin/env python3
"""The narration script. THIS IS THE ONLY TEXT SENT TO TTS.

2026-09-05 EDITORIAL REDESIGN. Replaces the 16-unit / 343-word single-narrator
cut (2:23.8) with a 13-unit / 240-word cut targeting ~95-100s at 145-150 wpm,
per the operator's "editorial science documentary" brief: one continuous
visual journey (a collagen strand through skin and body) instead of narrated
slides. The "building" metaphor and the vertical brick-course barrier are both
retired in favour of one recurring horizontal skin cross-section actor
(epidermis / dermis / collagen mesh) -- see actors.py. Every claim keeps the
exact sourced strength BRIEF.md's own 2026-09-04 audit already settled on
(C1-C10); nothing here asserts further than its citation. Two lines are the
operator's own required wording, verbatim: the "support mesh" line (02-mesh +
03-uv) and the closing line (13-verdict).

One narrator. One master take -- BLOCKS_ONE was already this project's
confirmed preference before the cut got shorter; at 240 words / ~1500
characters this is far under seed_audio's measured danger zone (a
1933-character block drifted off-script at 77.7% alignment), so there is no
reason left to split it.

TTS-safe copy rules (unchanged from the shipped cut): no em-dashes and no
colons (both read as long pauses or get verbalised); no hyphenated compound
numbers ("five hundred dalton", not "five-hundred-dalton") -- a hyphen reads
as one token to some engines and a KEY_TERMS mismatch costs a whole re-roll;
numbers are SPELLED OUT here and rendered numeric on screen by the frame
generator. Fixing a mispronunciation is a respelling HERE, never an edit to
the on-screen copy.

  cid     the beat UNIT (14 units, 13 spoken). Several units share one
          composition file -- see actors.FILES -- but every unit is its own
          timing span and its own row in STORYBOARD.md.
  text    the exact sentence(s) spoken for that unit. A sentence ends in
          . ? or ! and nothing else; gen_vo.py and timing.py rely on that.
"""

# Kimberly is the channel's standing narrator (videos/_channel/baseline.yaml,
# policies [S1/S-3] one presenter, [S1/S-4] never rotate) -- UNCHANGED by this
# redesign. Higgsfield seed_audio, voice_type "element" (a workspace reference
# element), never a preset.
NARRATOR = ("element", "674b71b8-1d2e-4087-8567-d1f53c0b9f3c")   # Kimberly

SCENES = [
    ("01-hook",
     "One strand of collagen. Cream spreads across the skin, and stops at the "
     "surface. Powder takes a different route, breaking apart as it goes. "
     "Where does it actually go?"),
    ("02-mesh",
     "Under the surface, collagen acts like a support mesh."),
    ("03-uv",
     "Age slows its renewal, and ultraviolet light helps break that mesh down."),
    ("04-barrier",
     "Topically, a molecule generally needs to be under five hundred daltons "
     "to cross into skin. Collagen is around three hundred thousand. "
     "It doesn't get through."),
    ("05-film",
     "It can still form a moisturizing film on the surface. Skin may feel "
     "smoother, but that's the surface, not structure below it."),
    ("06-swallow",
     "Swallow the powder, and digestion breaks it into peptides and amino acids."),
    ("07-dispatch",
     "They enter the bloodstream, then go wherever the body decides they're "
     "needed most, skin, joints, tendons. No guaranteed delivery to your face."),
    ("08-trials",
     "Twenty three trials, pooled together, do show modest gains in "
     "hydration and elasticity."),
    ("09-caveat",
     "But many of them were small, short, and industry funded."),
    ("10-filter",
     "Exclude the industry funded studies, and the benefit is no longer "
     "statistically significant. Keep only the higher quality studies, "
     "same result. The effect stops showing up."),
    ("11-uncertain",
     "We can't say collagen definitely works. We can't say it definitely "
     "fails, either."),
    ("12-recs",
     "So, broad spectrum sunscreen, every day, it's your best shield. "
     "Don't smoke. Get enough protein and vitamin C to support the repair. "
     "And for suitable users, topical retinoids have considerably stronger "
     "evidence for encouraging collagen production than collagen cream."),
    ("13-verdict",
     "Cream can moisturize. Powder is optional. Protect first."),
]

TEXT = dict(SCENES)
WORDLESS = {"14-end"}
ORDER = [cid for cid, _ in SCENES] + ["14-end"]

# ONE master take. At 240 words / ~1490 characters this sits well clear of
# seed_audio's measured danger zone (a 1933-char block on the previous, much
# longer script drifted off-script mid-take, verify-scored 77.7% against a 90%
# floor) -- there is no length pressure left to justify splitting into blocks,
# and one take removes the seam-matching problem (level/brightness correction
# across blocks) entirely rather than solving it smaller.
BLOCKS_ONE = [("master", ORDER[0:13])]
BLOCKS = BLOCKS_ONE
SCENE_BLOCK = {cid: block for block, cids in BLOCKS for cid in cids}

# Description chapters (no engine primitive; re-derived from real data-start
# values by build_storyboard.py, which parses index.html).
CHAPTERS = [
    ("01-hook",     "Where does it actually go?"),
    ("02-mesh",     "A support mesh under the surface"),
    ("04-barrier",  "Why the cream can't get in"),
    ("06-swallow",  "No guaranteed delivery to your face"),
    ("08-trials",   "The evidence plot twist"),
    ("12-recs",     "What actually protects it"),
]

# On-screen citation chips: `Journal · Year` ONLY. PMIDs/DOIs live in BRIEF.md's
# claim table and the description, never in a frame. Keyed by the unit whose
# claim the chip supports; the frame generator places each at its claim's word.
CITES = {
    "03-uv":      ["J Invest Dermatol · 1998"],
    "04-barrier": ["Exp Dermatol · 2000"],
    "08-trials":  ["Nutrients · 2023"],
    "10-filter":  ["Am J Med · 2025"],
    "12-recs":    ["J Dermatol Sci · 2007", "Arch Dermatol · 2007"],
}

# Claim ids from BRIEF.md's table -> the unit that carries them. C10 (protein and
# vitamin C) is UNSOURCED editorial advice and carries no chip, by decision;
# its chip-free treatment and the C8 chip's step-back-to-35%-opacity beside it
# both carry forward unchanged from the shipped cut.
CLAIMS = {
    "02-mesh":      ["C1"],
    "03-uv":        ["C2"],
    "04-barrier":   ["C3", "C3b"],
    "05-film":      ["C4"],
    "06-swallow":   ["C5"],
    "07-dispatch":  ["C5"],
    "08-trials":    ["C6"],
    "09-caveat":    ["C7"],
    "10-filter":    ["C7"],
    "11-uncertain": ["C7"],
    "12-recs":      ["C8", "C9", "C10"],
}


def prompt(block):
    """The exact TTS input for one block: its units' text joined by single
    spaces, no newlines (a newline reads as a paragraph pause on some engines)."""
    cids = dict(BLOCKS)[block]
    return " ".join(TEXT[c] for c in cids)


if __name__ == "__main__":
    tot = 0
    for cid, text in SCENES:
        n = len(text.split())
        tot += n
        print(f"  {cid:14s} {n:3d} words  {len(text):4d} chars")
    print(f"  TOTAL {tot} words  ~{tot / 170 * 60:.0f}s of speech at 170 wpm")
    for block, cids in BLOCKS:
        p = prompt(block)
        print(f"\n  block {block}: {len(cids)} units, {len(p.split())} words, {len(p)} chars")
        print("  " + p)
