"""The dialogue line table. THIS IS THE ONLY TEXT SENT TO TTS.

One .wav per line, not per scene: the scenes alternate between two speakers, so
a per-scene take is impossible. 41 lines -> assets/voice/NN-<who>.wav.

TTS-safe copy rules, carried from videos/ectoin-survival-molecule/scripts/
vo_lines.py: no em-dashes and no colons (both read as long pauses or get
verbalised). Where the spoken form must differ from the ON-SCREEN form, the
spoken form is respelled HERE and the on-screen text is left alone -- fixing a
mispronunciation by editing the visible copy is the wrong half of the fix.

  scene   which composition file the line lands in
  who     "soul" (SoulHabit, voice A) or "jay" (Jay, voice B)
  gap_after  seconds of silence after this line before the next one starts.
             Dialogue needs real turn-taking; a flat gap reads as a list being
             read out. Comic beats before a Jay punchline get more.
"""

# (scene, who, text, gap_after)
LINES = [
    # --- 01-building : S1, the collagen building ---------------------------
    ("01", "soul", "Collagen is one of the main structural proteins keeping your skin firm and supported.", 0.35),
    ("01", "jay",  "So collagen is the scaffolding holding up my face?", 0.30),
    ("01", "soul", "Basically.", 0.45),
    ("01", "jay",  "That explains why gravity keeps sending me renovation notices.", 0.60),
    # --- 01-building : S2, the demolition crew -----------------------------
    ("01", "soul", "As we age, collagen production slows. Ultraviolet exposure also activates enzymes that break existing collagen down.", 0.35),
    ("01", "jay",  "The sun has a demolition company?", 0.25),
    ("01", "soul", "And it works weekends.", 0.55),
    ("01", "jay",  "So sunscreen isn't only preventing sunburn. It is protecting the building?", 0.30),
    ("01", "soul", "Exactly. Preserving collagen is usually easier than trying to replace it later.", 0.50),

    # --- 02-door : S3, the collagen cream problem --------------------------
    ("02", "soul", "Now imagine applying a cream containing intact collagen.", 0.40),
    ("02", "soul", "Collagen is an extremely large molecule. It generally cannot travel through the skin barrier and reach the deeper dermis where your natural collagen lives.", 0.45),
    ("02", "jay",  "Delivery rejected. Package too large.", 0.55),
    ("02", "soul", "Topical collagen may still form a moisturizing film that makes the surface feel smoother.", 0.35),
    ("02", "jay",  "So it can polish the building's windows.", 0.30),
    ("02", "soul", "Yes.", 0.40),
    ("02", "jay",  "But it cannot walk downstairs and replace the support beams.", 0.55),

    # --- 03-digestion : S4, what happens when you drink it -----------------
    ("03", "soul", "When you consume collagen, digestion breaks it into smaller peptides and amino acids.", 0.35),
    ("03", "jay",  "Wait. The collagen does not travel directly from my smoothie to my forehead?", 0.30),
    ("03", "soul", "No. Your stomach does not offer facial delivery.", 0.50),
    ("03", "jay",  "So my face ordered scaffolding, and my digestive system delivered a box of spare parts.", 0.55),
    ("03", "soul", "Some of those parts may be absorbed and used by the body. Certain peptides may also act as biological signals. But the body decides where those resources go.", 0.40),
    ("03", "jay",  "Skin, joints, tendons, or wherever management thinks the repairs are most urgent.", 0.60),

    # --- 04-evidence : S5, the evidence plot twist -------------------------
    ("04", "soul", "Several clinical trials have reported modest improvements in hydration, elasticity or wrinkles after taking hydrolyzed collagen.", 0.40),
    ("04", "soul", "However, many trials were small, short and funded by collagen manufacturers.", 0.45),
    # "2025" and "23" are spelled out so TTS does not read them as digits.
    ("04", "soul", "A twenty twenty five analysis examined twenty three randomized trials. When researchers focused on higher quality and non industry funded studies, the benefits were no longer statistically significant.", 0.55),
    ("04", "jay",  "So collagen supplements definitely work?", 0.30),
    ("04", "soul", "We cannot say that.", 0.35),
    ("04", "jay",  "They definitely don't work?", 0.30),
    ("04", "soul", "We cannot confidently say that either.", 0.45),
    ("04", "jay",  "Science has entered its favourite relationship status. It's complicated.", 0.60),

    # --- 05-verdict : S6, what actually protects collagen ------------------
    ("05", "soul", "The strongest strategy is protecting and supporting the collagen your skin already produces.", 0.35),
    ("05", "soul", "Use broad spectrum sunscreen consistently. Avoid smoking. Eat adequate protein and get enough vitamin C.", 0.45),
    ("05", "soul", "For suitable users, topical retinoids have considerably stronger evidence for encouraging collagen production than collagen cream.", 0.45),
    ("05", "jay",  "So the ingredient with collagen written on the largest bottle may not be doing the most for collagen?", 0.35),
    ("05", "soul", "Welcome to skincare marketing.", 0.60),
    # --- 05-verdict : S7, the SoulHabit verdict ----------------------------
    ("05", "soul", "Collagen cream can be a pleasant moisturizer, but it does not simply replace lost dermal collagen.", 0.40),
    ("05", "soul", "Collagen supplements are optional. Early results are interesting, but the independent evidence remains uncertain.", 0.40),
    ("05", "soul", "Sunscreen, good nutrition and proven actives should come first.", 0.45),
    ("05", "jay",  "Protect the building before buying expensive powdered bricks.", 0.35),
    ("05", "soul", "That is surprisingly accurate.", 0.55),
    ("05", "jay",  "My smoothie has been demoted from contractor to intern.", 0.30),
]

# Voice assignment. SoulHabit keeps the channel's standing voice for continuity;
# Jay is a deliberate second voice -- recorded as a voice-continuity break in
# BRIEF.md, the way videos/ceramides-skin-barrier/BRIEF.md documented the last one.
VOICES = {
    # SoulHabit keeps the channel's standing voice. Measured 184.1 wpm.
    "soul": ("element", "674b71b8-1d2e-4087-8567-d1f53c0b9f3c"),  # Kimberly
    # Jay is a DELIBERATE second voice -- the channel has never run two
    # concurrently. Chosen over Emmett on two measurements: 163.4 wpm vs 150.3
    # (a comic foil wants the snappier read), and a clearly opposite spectral
    # tilt to Kimberly (low-band RMS -26.3 dB vs her -34.9), so the two are
    # separable by ear without any on-screen label doing the work.
    "jay":  ("preset", "b847bc29-f184-583a-8ad9-d1f1e16d1a60"),   # Dylan
}

SCENES = ["00", "01", "02", "03", "04", "05"]


def by_scene():
    """Lines grouped by the composition file they land in, in order."""
    out = {s: [] for s in SCENES}
    for i, (sc, who, text, gap) in enumerate(LINES, start=1):
        out[sc].append({"idx": i, "who": who, "text": text, "gap": gap,
                        "disp": DISPLAY[i],
                        "wav": f"assets/voice/{i:02d}-{who}.wav"})
    return out



# --- on-screen copy --------------------------------------------------------
# The lane card is NOT a transcript. It carries the load-bearing clause of the
# spoken line, condensed, with <em> on the one word the beat turns on. The full
# sentence is spoken by the VO and written to the .srt; putting all 30 words in
# a 40px card makes an unreadable frame and wastes the beat.
#
# Where a number is spelled out above for TTS ("twenty three"), the on-screen
# form stays numeric ("23"). Fixing a mispronunciation by editing the visible
# copy is the wrong half of that fix.
DISPLAY = {
    1:  "Collagen is a <em>structural protein</em>. It keeps skin firm.",
    2:  "So it's the <em>scaffolding</em> holding up my face?",
    3:  "Basically.",
    4:  "That explains the <em>renovation notices</em> from gravity.",
    5:  "Production slows with age. <em>UV light</em> switches on enzymes that cut collagen apart.",
    6:  "The sun has a <em>demolition company</em>?",
    7:  "And it works weekends.",
    8:  "So sunscreen isn't just about burning. It's <em>protecting the building</em>?",
    9:  "Yes. Keeping collagen is <em>easier than replacing it</em>.",
    10: "Now put <em>whole collagen</em> in a cream.",
    11: "Far too <em>large a molecule</em> to cross the barrier and reach the deep layer.",
    12: "Delivery rejected. <em>Package too large.</em>",
    13: "It can still sit on top as a <em>moisturising film</em>. Skin feels smoother.",
    14: "So it polishes the <em>windows</em>.",
    15: "Yes.",
    16: "But it can't go downstairs and <em>replace the beams</em>.",
    17: "Digestion breaks collagen into <em>peptides and amino acids</em>.",
    18: "It doesn't go straight from smoothie to <em>forehead</em>?",
    19: "No. Your stomach doesn't do <em>facial delivery</em>.",
    20: "My face ordered scaffolding. My gut sent a <em>box of spare parts</em>.",
    21: "Some gets absorbed and reused. But <em>your body picks where it goes</em>.",
    22: "Skin, joints, tendons — <em>wherever repairs are most urgent</em>.",
    23: "Trials do report <em>modest gains</em> in hydration, elasticity and wrinkles.",
    24: "But many were <em>small, short, and paid for by collagen makers</em>.",
    25: "A 2025 review of <em>23 trials</em>. Keep only the independent, higher-quality ones and <em>the effect disappears</em>.",
    26: "So supplements <em>definitely work</em>?",
    27: "We can't say that.",
    28: "They <em>definitely don't</em>?",
    29: "We can't confidently say that either.",
    30: "Science has entered its favourite status: <em>it's complicated</em>.",
    31: "The strongest move is <em>protecting what you already make</em>.",
    32: "Broad-spectrum sunscreen, daily. <em>Don't smoke.</em> Enough protein and vitamin C.",
    33: "For suitable users, <em>topical retinoids</em> have much stronger evidence for collagen than collagen cream.",
    34: "So the bottle with <em>COLLAGEN</em> in the biggest letters isn't doing the most for it?",
    35: "Welcome to skincare marketing.",
    36: "Collagen cream is a fine moisturiser. It <em>doesn't replace</em> deep-layer collagen.",
    37: "Supplements are optional. Interesting early results, <em>uncertain independent evidence</em>.",
    38: "<em>Sunscreen, nutrition and proven actives</em> come first.",
    39: "Protect the building before buying <em>expensive powdered bricks</em>.",
    40: "That is surprisingly accurate.",
    41: "My smoothie has been demoted from contractor to <em>intern</em>.",
}

assert set(DISPLAY) == set(range(1, len(LINES) + 1)), (
    f"DISPLAY must cover every line exactly: "
    f"missing {set(range(1, len(LINES)+1)) - set(DISPLAY)}, "
    f"extra {set(DISPLAY) - set(range(1, len(LINES)+1))}")

if __name__ == "__main__":
    g = by_scene()
    tot_w = 0
    for s in SCENES:
        w = sum(len(l["text"].split()) for l in g[s])
        gaps = sum(l["gap"] for l in g[s])
        tot_w += w
        print(f"  {s}: {len(g[s]):2d} lines, {w:3d} words, {gaps:5.2f}s of gaps"
              f"  -> ~{w/150*60 + gaps:5.1f}s")
    print(f"  TOTAL {len(LINES)} lines, {tot_w} words,"
          f" ~{tot_w/150*60 + sum(l[3] for l in LINES):.1f}s + 5.0s cold open"
          f" = ~{tot_w/150*60 + sum(l[3] for l in LINES) + 5:.1f}s")
