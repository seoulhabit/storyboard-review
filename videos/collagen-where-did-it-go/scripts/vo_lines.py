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
     "So where does it go? Twenty three trials say the powder works. "
     "Remove the industry funded ones, and watch what happens. "
     "But first, what protects the collagen you already have?"),
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
     "under about five hundred daltons. Collagen is around three hundred thousand. "
     "It is not getting through that door."),
    ("07-film",
     "It may still form a moisturising film on the surface. Skin may feel smoother. "
     "But polishing the windows is not replacing the beams."),
    ("08-digestion",
     "Now, the powder. Swallow collagen, and digestion breaks it into peptides "
     "and amino acids. Your stomach does not offer facial delivery."),
    ("09-dispatch",
     "Some pieces may be absorbed. Certain peptides may even act as signals. "
     "But your body decides where they go. "
     "Skin, joints, tendons, wherever repairs are most urgent. "
     "Your face ordered scaffolding. It got a box of spare parts."),
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
BLOCKS_TWO_EARLY = [("A", ORDER[0:9]), ("B", ORDER[9:15])]   # fallback split
# seed_audio rejects prompts over 2048 chars (measured: our 15-unit master is
# 2323). BLOCKS_ONE is kept for a shorter future script; this build uses the
# two-block split with the seam at 13-uncertain -> 14-hierarchy: the whole
# hook-to-climax run (units 1-13) is ONE continuous performance, and the seam
# falls under the second invert wipe at the "what the evidence supports"
# chapter turn, where a register reset reads as intended. Block A must stay
# under 2048 chars (python3 scripts/vo_lines.py prints it); if the service
# rejects it, fall back to BLOCKS_TWO_EARLY (seam at the first invert).
BLOCKS = BLOCKS_TWO
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
