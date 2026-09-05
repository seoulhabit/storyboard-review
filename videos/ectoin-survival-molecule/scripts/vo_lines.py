#!/usr/bin/env python3
"""VO text for all 29 scenes, keyed by scene id. Single source for generation.

TTS-safe: no em-dashes, no colons -- both produce odd pauses in this engine.
On-screen text keeps real punctuation and spelling; these diverge deliberately.

Act 1 lines are moved here from SCRIPT.md (previously hard-coded only as
on-screen copy in build_frames.py). Scenes 09 and 10 are merged into a single
scene id, 09-exclusion, carrying both original sentences -- the external
review's approved cut. That takes the deck from 29 scenes to 28.
"""
LINES = [
    # --- ACT 1 (pilot) ---
    ("01-hook",       "Your next favourite skincare ingredient may have been invented by bacteria trying not to die. Not snail mucin. Not salmon DNA. And not another form of hyaluronic acid."),
    ("02-osmosis",    "This tiny molecule helps microorganisms survive places so salty and so dry that an ordinary cell would lose its water and stop functioning."),
    ("03-now",        "And it is now turning up, quietly, in Korean serums, creams and sunscreens. It is called ectoin, and the real science is stranger than the marketing."),
    ("04-extremolyte","Ectoin is what researchers call an extremolyte. That sounds like a superhero. It just means a protective molecule made by microbes living somewhere extreme."),
    ("05-halomonas",  "The bacterium we get most of it from has a name. Halomonas elongata. It lives in salt. When the salt outside gets punishing, it floods itself with ectoin."),
    ("06-mechanism",  "Why? Because salt pulls water out of cells. Lose enough water and proteins start to lose their shape, membranes get unstable, and the cell stops working."),
    ("07-question",   "Ectoin keeps the space around those fragile structures survivable. Which led skincare researchers to an obvious question. Could it do the same for stressed human skin?"),
    # --- ACT 2 (mechanism) ---
    ("08-humectant",  "Here is where ectoin stops behaving like a normal moisturiser. Familiar humectants, such as glycerin and hyaluronic acid, attract water and hold on to it. Ectoin seems to affect how water arranges itself around proteins and membranes."),
    # 09-exclusion carries BOTH the tidy version (formerly scene 09) and the
    # honest correction (formerly scene 10) -- one continuous diagram, one scene.
    ("09-exclusion",  "Scientists call the idea preferential exclusion. The tidy version. Ectoin protects proteins by staying off their surface, which helps the water around them stay organised. The honest version is messier. In the simulations, ectoin also showed some attraction to that surface. And how far it stays back depends on how tightly the protein's own water is already arranged."),
    ("11-analogy",    "Think of a celebrity inside a ring of security. Ectoin is not hugging the celebrity. It hangs back, and helps the ring hold its shape. Which is why calling it another hydrating ingredient misses the interesting part."),
    # --- ACT 3 (what it means for skin) ---
    ("12-load",       "Your outer skin barrier is under constant load. Dry air, cleansing, pollution, sun, strong actives. When it struggles, water escapes more easily, and skin can feel tight, rough, or unusually reactive."),
    ("13-keratin",    "Lab research suggests ectoin can help stabilise biological structures and improve hydration in that outer layer. One study found it changed how keratin, the main protein in our outer skin cells, behaves with water."),
    ("14-notforce",   "Though in that same study, in punishing dryness, below five percent humidity, one stress measure actually got worse. It is not a force field."),
    ("15-framing",    "It is better understood as a supporting ingredient that may help skin handle dehydration and environmental stress more comfortably."),
    # --- ACT 4 (the human evidence) ---
    ("16-trial104",   "So does it do anything to actual people? In one randomised, double blind study, a hundred and four women used a cream with two percent ectoin against the same cream without it."),
    ("17-preference", "On the study's own measure, the women themselves preferred the ectoin version. That is a real result. And it is a preference, not a machine reading their skin."),
    ("18-eczema",     "A second randomised study followed sixty five people with mild to moderate atopic dermatitis, eczema. Over four weeks, an ectoin cream performed about as well as the barrier cream it was tested against, and was well tolerated."),
    ("19-limits",     "Encouraging. Not proof that ectoin cures eczema, reverses ageing, or replaces anything a dermatologist prescribes."),
    ("20-twelve",     "And the evidence base is genuinely small. Search PubMed today and you will find twelve ectoin clinical trials. Twelve."),
    # The three makers get a full stop each, not commas: this engine reads a
    # comma as a beat and a period as a rest, and the review asked for short
    # breaks BETWEEN the names. Phonetic locks live in the TTS prompt only
    # (scripts/gen_vo.py PRONUNCIATION), never in this text -- what is written
    # here is what the captions say.
    ("21-verdict",    "Some of that research comes from companies that sell the ingredient. bitop. Merck. And Kao. So. Promising supporting ingredient, yes. Miracle molecule, no."),
    # --- ACT 5 (how to read a label) ---
    ("22-whofor",     "Ectoin is most interesting if your skin runs dry, sensitive, over cleansed, or irritated by a strong routine. It sits comfortably alongside panthenol, glycerin, squalane and ceramides."),
    ("23-numbers",    "But do not buy it off the front of the bottle. Turn it around. Plenty of brands do print a number. Paula's Choice says seven percent. The Ordinary lists two percent ectoin."),
    # "The brand" is not decoration. Sentence-initial "Abib" came back from the
    # engine as "Abbey", and both phonetic respellings made it worse -- "Ah-beeb"
    # read as "AB" and "A-beeb" as "A.B.", each also dragging ectoin off with it
    # ("ecto-on", "ectoion"). Two words of run-up put the brand mid-phrase, where
    # it is said correctly and ectoin survives. Verified on whisper large-v3.
    ("24-eleven",     "The brand Abib promotes Ectoin Panthenol eleven percent, but that eleven percent combines the two ingredients. Panthenol is second on the ingredient list. Ectoin is eleventh. The big number on the front is not always the ectoin number."),
    ("25-formula",    "The rest is judgement, not evidence. Is it fragrance free, if fragrance bothers you? Does the formula carry other useful moisturisers? One good ingredient cannot rescue a badly built product."),
    # --- ACT 6 (the K-beauty connection) ---
    ("26-kbeauty",    "K beauty did not invent ectoin. What Korean formulators are doing well is pairing it with barrier ingredients in light, wearable textures."),
    ("27-resilience", "That fits the wider move away from aggressive transformation and towards skin that simply stays comfortable. You will already find it in Korean barrier serums, toners and sun products, often in smaller type than the trend suggests."),
    # --- ACT 7 (close) ---
    ("28-remember",   "So next time you see ectoin on an ingredient list, remember what you are looking at. A survival strategy, borrowed from bacteria. Not the new hyaluronic acid. Not a miracle. A genuinely interesting supporting molecule."),
    ("29-cta",        "Here is the one thing worth doing. Turn the bottle around and find the actual percentage before you buy. And tell me, would you put a bacteria made survival molecule on your face?"),
    # --- END CARD (2026-09-05 accessibility pass) ---
    # Spoken, so it walks like any other scene -- no wordless-unit machinery.
    ("30-endcard",    "Follow SeoulHabit for more."),
]

# scene id -> text, for O(1) lookup elsewhere
TEXT = dict(LINES)

# Act-level blocks for real TTS generation: one request per act, later CUT into
# the per-scene WAVs above by scripts/gen_vo.py. Order matches LINES.
BLOCKS = [
    ("act1", ["01-hook", "02-osmosis", "03-now", "04-extremolyte", "05-halomonas",
              "06-mechanism", "07-question"]),
    ("act2", ["08-humectant", "09-exclusion", "11-analogy"]),
    ("act3", ["12-load", "13-keratin", "14-notforce", "15-framing"]),
    ("act4", ["16-trial104", "17-preference", "18-eczema", "19-limits",
              "20-twelve", "21-verdict"]),
    ("act5", ["22-whofor", "23-numbers", "24-eleven", "25-formula"]),
    ("act6", ["26-kbeauty", "27-resilience"]),
    ("act7", ["28-remember", "29-cta"]),
    ("act8", ["30-endcard"]),
]
SCENE_BLOCK = {cid: block for block, cids in BLOCKS for cid in cids}

# Scenes carrying citation-backed clinical/lab evidence read slower by nature
# (a number, a qualifier, a study design) -- allowed a lower wpm floor than the
# narrative scenes around them.
EVIDENCE = {"13-keratin", "14-notforce", "16-trial104", "17-preference",
            "18-eczema", "19-limits", "21-verdict"}

# The three passages the 2026-09-05 accessibility review asked to be read at
# 125-135 wpm: the mechanism section (01:13-02:02), the human-evidence section
# (02:53-03:49) and the label-reading section (04:12-04:32). Timecodes are the
# review's, against the 5:38 retention master; the scene ids are what they
# resolve to in that cut and are what the pacing is actually applied to.
SLOWED = {
    "08-humectant", "09-exclusion", "11-analogy",
    "16-trial104", "17-preference", "18-eczema", "19-limits", "20-twelve",
    "21-verdict",
    "23-numbers", "24-eleven",
}

# --from-takes validation (scripts/gen_vo.py): maps each scene id to the take
# number(s) already recorded under the OLD 29-scene numbering, in
# assets/voice/NN.wav. 09-exclusion draws on both takes 09 and 10 -- exactly
# the audio the merge combines -- concatenated into one synthetic "block" so
# the cut/walk/bind mechanism is proven against the real merge case before any
# new TTS credit is spent.
TAKES_MAP = {
    "01-hook": [1], "02-osmosis": [2], "03-now": [3], "04-extremolyte": [4],
    "05-halomonas": [5], "06-mechanism": [6], "07-question": [7],
    "08-humectant": [8], "09-exclusion": [9, 10], "11-analogy": [11],
    "12-load": [12], "13-keratin": [13], "14-notforce": [14], "15-framing": [15],
    "16-trial104": [16], "17-preference": [17], "18-eczema": [18], "19-limits": [19],
    "20-twelve": [20], "21-verdict": [21],
    "22-whofor": [22], "23-numbers": [23], "24-eleven": [24], "25-formula": [25],
    "26-kbeauty": [26], "27-resilience": [27],
    "28-remember": [28], "29-cta": [29], "30-endcard": [30],
}
