#!/usr/bin/env python3
"""VO text for ACTS 2-7, keyed by scene id. Single source for generation.

TTS-safe: no em-dashes, no colons -- both produce odd pauses in this engine.
On-screen text keeps real punctuation and spelling; these diverge deliberately.
"""
LINES = [
    # --- ACT 2 (mechanism) ---
    ("08-humectant", "Here is where ectoin stops behaving like a normal moisturiser. A familiar humectant, glycerin, hyaluronic acid, attracts water and holds onto it. Ectoin seems to work on how water arranges itself around proteins and membranes."),
    ("09-exclusion", "Scientists call the idea preferential exclusion. The tidy version. Ectoin protects proteins by staying off their surface, which helps the water around them stay organised."),
    ("10-messier",   "The honest version is messier. In the simulations, ectoin also showed some attraction to that surface. And how far it stays back depends on how tightly the protein's own water is already arranged."),
    ("11-analogy",   "Think of a celebrity inside a ring of security. Ectoin is not hugging the celebrity. It hangs back, and helps the ring hold its shape. Which is why calling it another hydrating ingredient misses the interesting part."),
    # --- ACT 3 (what it means for skin) ---
    ("12-load",      "Your outer skin barrier is under constant load. Dry air, cleansing, pollution, sun, strong actives. When it struggles, water escapes more easily, and skin can feel tight, rough, or unusually reactive."),
    ("13-keratin",   "Lab research suggests ectoin can help stabilise biological structures and improve hydration in that outer layer. One study found it changed how keratin, the main protein in our outer skin cells, behaves with water."),
    ("14-notforce",  "Though in that same study, in punishing dryness, below five percent humidity, one stress measure actually got worse. It is not a force field."),
    ("15-framing",   "It is better understood as a supporting ingredient that may help skin handle dehydration and environmental stress more comfortably."),
    # --- ACT 4 (the human evidence) ---
    ("16-trial104",  "So does it do anything to actual people? In one randomised, double blind study, a hundred and four women used a cream with two percent ectoin against the same cream without it."),
    ("17-preference","On the study's own measure, the women themselves preferred the ectoin version. That is a real result. And it is a preference, not a machine reading their skin."),
    ("18-eczema",    "A second randomised study followed sixty five people with mild to moderate atopic dermatitis, eczema. Over four weeks, an ectoin cream performed about as well as the barrier cream it was tested against, and was well tolerated."),
    ("19-limits",    "Encouraging. Not proof that ectoin cures eczema, reverses ageing, or replaces anything a dermatologist prescribes."),
    ("20-twelve",    "And the evidence base is genuinely small. Search PubMed today and you will find twelve ectoin clinical trials. Twelve."),
    ("21-verdict",   "Some of that research also comes from people who sell the ingredient. Bitop, Merck, Kao. So. Promising supporting ingredient, yes. Miracle molecule, no."),
    # --- ACT 5 (how to read a label) ---
    ("22-whofor",    "Ectoin is most interesting if your skin runs dry, sensitive, over cleansed, or irritated by a strong routine. It sits comfortably alongside panthenol, glycerin, squalane and ceramides."),
    ("23-numbers",   "But do not buy it off the front of the bottle. Turn it around. Plenty of brands do print a number. Paula's Choice says seven percent. The Ordinary says two."),
    ("24-eleven",    "And Abib's Ectoin Panthenol eleven percent? That eleven is the two of them added together. On the ingredient list, panthenol is second. Ectoin is eleventh. The big number on the front is not always the ectoin number."),
    ("25-formula",   "The rest is judgement, not evidence. Is it fragrance free, if fragrance bothers you? Does the formula carry other useful moisturisers? One good ingredient cannot rescue a badly built product."),
    # --- ACT 6 (the K-beauty connection) ---
    ("26-kbeauty",   "K beauty did not invent ectoin. What Korean formulators are doing well is pairing it with barrier ingredients in light, wearable textures."),
    ("27-resilience","That fits the wider move away from aggressive transformation and towards skin that simply stays comfortable. You will already find it in Korean barrier serums, toners and sun products, often in smaller type than the trend suggests."),
    # --- ACT 7 (close) ---
    ("28-remember",  "So next time you see ectoin on an ingredient list, remember what you are looking at. A survival strategy, borrowed from bacteria. Not the new hyaluronic acid. Not a miracle. A genuinely interesting supporting molecule."),
    ("29-cta",       "Here is the one thing worth doing. Turn the bottle around and find the actual percentage before you buy. And tell me, would you put a bacteria made survival molecule on your face?"),
]
