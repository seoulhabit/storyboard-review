#!/usr/bin/env python3
"""The narration script. THIS IS THE ONLY TEXT SENT TO TTS.

One narrator, one master take. The two-voice dialogue (SoulHabit + Jay, 41
lines) that this project shipped with on 2026-09-03 was replaced on
2026-09-04 by a single-narrator rewrite; the reasons and the retention
diagnosis are in DELIVERY.md's changelog. Every downstream file -- the frame
generator, the root composition, captions, SCRIPT.md, STORYBOARD.md, the
motion sidecar -- derives from this table plus the measured word manifest
(assets/voice/master.words.json, written by scripts/gen_vo.py).

TTS-safe copy rules (carried from videos/ectoin-survival-molecule): no
em-dashes and no colons (both read as long pauses or get verbalised); numbers
are SPELLED OUT here and rendered numeric on screen by the frame generator.
Fixing a mispronunciation by editing the visible copy is the wrong half of
that fix -- the spoken form is respelled HERE and the on-screen form is left
alone.

  cid     the beat UNIT (16 units, 15 spoken). Several units share one
          composition file -- see actors.FILES -- but every unit is its own
          timing span and its own row in STORYBOARD.md.
  text    the exact sentence(s) spoken for that unit. A sentence ends in
          . ? or ! and nothing else; gen_vo.py and timing.py rely on that.
"""

# Kimberly is the channel's standing narrator (videos/_channel/baseline.yaml,
# policies [S1/S-3] one presenter, [S1/S-4] never rotate). Higgsfield seed_audio,
# voice_type "element" (a workspace reference element), never a preset.
NARRATOR = ("element", "674b71b8-1d2e-4087-8567-d1f53c0b9f3c")   # Kimberly

SCENES = [
    ("01-hook",
     "Collagen cream does not replace your collagen. "
     "Collagen powder does not travel straight to your face."),
    ("02-promise",
     "So where does it go? Across twenty three trials, it appears to help. "
     "Remove the industry funded studies, and the answer changes."),
    ("03-building",
     "Think of your skin as a building. Collagen is the main structure inside it. "
     "It keeps everything firm and upright."),
    ("04-demolition",
     "As we age, collagen production slows. "
     "And ultraviolet light switches on enzymes that cut collagen apart. "
     "The sun runs a demolition crew. It works weekends."),
    ("05-boundary",
     "Sunscreen is not just about sunburn. It draws a boundary around the building. "
     "Preserving collagen is usually easier than replacing it later."),
    ("06-door",
     "Now, the cream. To pass through skin, a molecule generally needs to be "
     "under five hundred daltons. Collagen is around three hundred thousand. "
     "It is not getting through that door."),
    ("07-film",
     "It may still form a moisturising film on the surface. Skin may feel smoother. "
     "But polishing the windows is not replacing the beams."),
    ("08-digestion",
     "Now, the powder. Swallow collagen, and digestion breaks it into peptides "
     "and amino acids. Your stomach does not offer facial delivery."),
    ("09-dispatch",
     "But your body decides where they go, to skin, joints, tendons, "
     "or wherever repairs are most urgent. "
     "Your face ordered scaffolding. It got spare parts instead. "
     "Trials do point to a modest benefit."),
    ("10-trials",
     "Does the powder work? Trials do report modest improvements in hydration, "
     "elasticity, or wrinkles."),
    ("11-caveat",
     "But many were small, short, and industry funded."),
    ("12-filter",
     "In twenty twenty five, researchers pooled twenty three randomised trials. "
     "All together, a benefit. "
     "Keep only the studies without industry funding, and it is no longer "
     "statistically significant. "
     "Keep only the higher quality studies. Same result. "
     "The effect stops showing up."),
    ("13-uncertain",
     "Do supplements definitely work? We cannot say that. Definitely fail? "
     "We cannot confidently say that either. The independent evidence is uncertain."),
    ("14-hierarchy",
     "What the evidence actually supports. Broad spectrum sunscreen, every day. "
     "Not smoking. Enough protein and vitamin C. "
     "And for suitable users, topical retinoids have considerably stronger evidence "
     "for encouraging collagen production than collagen cream."),
    ("15-verdict",
     "Collagen cream can be a pleasant moisturiser. Collagen powder is optional. "
     "Protect the building before you buy expensive powdered bricks."),
]

TEXT = dict(SCENES)
WORDLESS = {"16-end"}
ORDER = [cid for cid, _ in SCENES] + ["16-end"]

# TTS blocks. The user's confirmed choice (2026-09-04) is ONE master take;
# gen_vo.py concatenates however many blocks exist into assets/voice/master.wav
# so nothing downstream knows or cares. Switch to BLOCKS_TWO only if the
# service rejects the full prompt or `gen_vo.py verify` fails on the master
# (round 2 of the channel's two-round cap, [S4/V-2]).
BLOCKS_ONE = [("master", ORDER[0:15])]
BLOCKS_TWO = [("A", ORDER[0:13]), ("B", ORDER[13:15])]
BLOCKS_FOUR = [("A1", ORDER[0:5]), ("A2", ORDER[5:9]), ("A3", ORDER[9:13]), ("B", ORDER[13:15])]

# MEASURED, not assumed. seed_audio's hard limit is 2048 characters, and a
# 1933-character block came back UNDER it and still failed: the take was
# faithful for 241 of 310 words and then abandoned the script entirely,
# improvising ~25 seconds of generic skincare copy in Kimberly's voice over
# live audio (not silence, so no level check would have caught it). The whole
# climax -- "the effect stops showing up", both refusals, "the independent
# evidence is uncertain" -- was simply absent. `gen_vo.py verify` catches this
# by alignment coverage (77.7% against a 90% floor), which is exactly what that
# floor is for.
#
# So the limit that matters is not the documented one. These four blocks are
# 400-700 characters each, and every seam falls on a VISIBLE transition:
#   A1 -> A2  the iris into 06-door
#   A2 -> A3  the invert into the evidence ground
#   A3 -> B   the invert out of it
# A block seam is a change of performance; putting each one where the edit is
# already changing register is the cheapest place to spend it.
BLOCKS = BLOCKS_FOUR
SCENE_BLOCK = {cid: block for block, cids in BLOCKS for cid in cids}

# Description chapters (no engine primitive; re-derived from real data-start
# values by build_storyboard.py, which parses index.html).
CHAPTERS = [
    ("01-hook",      "Where does it actually go?"),
    ("03-building",  "Your skin is a building"),
    ("06-door",      "Why the cream can't get in"),
    ("08-digestion", "Your stomach doesn't do facial delivery"),
    ("10-trials",    "The evidence plot twist"),
    ("14-hierarchy", "What actually protects it"),
]

# On-screen citation chips: `Journal · Year` ONLY. PMIDs/DOIs live in BRIEF.md's
# claim table and the description, never in a frame. Keyed by the unit whose
# claim the chip supports; the frame generator places each at its claim's word.
CITES = {
    "04-demolition": ["J Invest Dermatol · 1998"],
    "06-door":       ["Exp Dermatol · 2000"],
    "10-trials":     ["Nutrients · 2023"],
    "12-filter":     ["Am J Med · 2025"],
    "14-hierarchy":  ["J Dermatol Sci · 2007", "Arch Dermatol · 2007"],
}

# Claim ids from BRIEF.md's table -> the unit that carries them. C10 (protein and
# vitamin C) is UNSOURCED editorial advice and carries no chip, by decision.
CLAIMS = {
    "03-building":  ["C1"],
    "04-demolition": ["C2"],
    "06-door":      ["C3"],
    "07-film":      ["C4"],
    "08-digestion": ["C5"],
    "09-dispatch":  ["C5"],
    "10-trials":    ["C6"],
    "11-caveat":    ["C7"],
    "12-filter":    ["C7"],
    "13-uncertain": ["C7"],
    "14-hierarchy": ["C8", "C9", "C10"],
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
