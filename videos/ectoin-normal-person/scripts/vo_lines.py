#!/usr/bin/env python3
"""Turn table -- the machine-readable half of SCRIPT.md.

TURNS is the source of truth for VO generation and for scene composition.
Each entry is (turn_id, speaker, tts_text). SCENES maps a scene id to the
turns it carries, in order.

TTS-safe rules, inherited from the predecessor (scripts/vo_lines.py there):
no em-dashes and no colons -- both produce odd pauses in this engine. Numerals
are spelled where the engine reads them oddly ("2 percent", not "2%").

`ectoin` is written PLAIN everywhere. The predecessor tried a phonetic
respelling and the result was WORSE ("echetoin"); a plain-spelling retry fixed
it. Do not respell it.

Speaker -> audio group. S = SOULHABIT (standing series voice, ink/display type),
J = JAY (contrasting register, coral/Inter type).

COLD-OPEN REVISION (2026-09-03). New turns are APPENDED as t071-t075 rather
than renumbered -- frames_spec.py has ~180 literal t['tNNN'] lookups and
renumbering would touch every one of them for no benefit. TURNS list ORDER
must equal playback order (see the assert at the bottom of this file); turn
id numbering is NOT required to be monotonic with it, and after this revision
it is not: t071-t075 sit ahead of t002/t003/t016 in list order despite the
higher id. Retired turns (t001, t004-t015, t051-t054 -- 17 total) are removed
outright, not commented out, so SCENES coverage stays exact. t002 and t003
are reused verbatim from the shipped cut, just relocated into 02-origin.
"""

S, J = "S", "J"

TURNS = [
    # ---- new cold open -----------------------------------------------
    ("t071", S, "This bottle says eleven percent. Does that mean eleven percent ectoin?"),
    ("t072", S, "No. It's a blend. Which is why the most useful thing you can do with an ectoin product is turn the bottle around."),
    ("t073", S, "But before skincare marketing found it, ectoin belonged to a bacterium living in extremely salty water."),
    ("t002", J, "Bacteria invented skincare?"),
    ("t003", S, "Not intentionally."),
    ("t074", S, "The salt is constantly trying to pull water out of the cell, basically turning it into a microscopic raisin. Ectoin helps keep the delicate machinery inside stable."),
    ("t075", S, "Skincare borrowed the molecule. Marketing borrowed the drama."),
    # ---- CH2 -- give the protein some space (unchanged) ---------------
    ("t016", S, "Ectoin belongs to a group of protective molecules sometimes called extremolytes."),
    ("t017", S, "Its proposed effects involve how water arranges itself around proteins and membranes. One part of the explanation is called preferential exclusion."),
    ("t018", J, "Even the alarm wants you to stop."),
    ("t019", S, "Fine. Imagine a protein is a celebrity surrounded by security."),
    ("t020", S, "Ectoin may help the surrounding water remain organised without simply clinging directly to the protein."),
    ("t021", J, "So ectoin gives proteins personal space."),
    ("t022", S, "That is the simplified explanation. The actual molecular behaviour is more complicated."),
    ("t023", J, "Understood. Ectoin is a hydration event coordinator with excellent boundaries."),
    ("t024", S, "I immediately regret simplifying this."),
    # ---- CH3 -- what this means for skin (unchanged) -------------------
    ("t025", S, "Laboratory research suggests ectoin may help stabilise biological structures and influence how keratin in the outer skin layer interacts with water."),
    ("t026", S, "It may help dry or stressed skin cope more comfortably."),
    ("t027", J, "Look at you translating yourself."),
    ("t028", S, "I am learning."),
    ("t029", J, "Does ectoin create an invisible protective force field around my face?"),
    ("t030", S, "No."),
    ("t031", J, "Finally, a skincare ingredient with realistic boundaries."),
    ("t032", S, "Think of ectoin as support for the skin barrier, not body armour."),
    # ---- CH4 -- does it work on people (unchanged) ----------------------
    ("t033", S, "In one study, 104 women compared a cream containing 2 percent ectoin with the same cream without it."),
    ("t034", S, "The women preferred the ectoin version."),
    ("t035", J, "So it worked?"),
    ("t036", S, "They liked it better. That is a real result, but it is not the same as a machine proving that their skin transformed."),
    ("t037", J, "Preference, not Cinderella."),
    ("t038", S, "Another study followed 65 people with mild to moderate eczema. Over four weeks, the ectoin cream performed about as well as the comparison barrier cream and was well tolerated."),
    ("t039", J, "Promising?"),
    ("t040", S, "Yes."),
    ("t041", J, "Miracle?"),
    ("t042", S, "No."),
    ("t043", S, "It does not prove that ectoin cures eczema, reverses ageing or replaces medical treatment."),
    ("t044", S, "The clinical evidence is still limited, and some research is connected to companies that sell the ingredient."),
    ("t045", J, "How limited?"),
    ("t046", S, "A PubMed search found twelve clinical trials."),
    ("t047", J, "Twelve? My group chat has produced more research on whether someone should text their ex."),
    # t048 is retained by operator decision and is factually wrong -- all twelve
    # are peer-reviewed indexed articles. Shipped VO-only, with NO on-screen
    # reinforcement and no citation pill. See SCRIPT.md change 3 and DELIVERY.md.
    ("t048", S, "None of it passed peer review."),
    # ---- CH5 -- how to read the bottle. t051-t054 RETIRED this revision:
    # the "turn the bottle around" / "group project" reveal now lives in the
    # cold open (t072). 12-bottle keeps only who-it's-for (t049-t050) and the
    # INCI-list payoff (t055-t057), which the open only glimpsed. -----------
    ("t049", S, "Ectoin may be most interesting if your skin is dry, sensitive, over-cleansed or irritated by a demanding routine."),
    ("t050", S, "It can be paired with ingredients such as panthenol, glycerin, squalane and ceramides."),
    ("t055", S, "Exactly. Check the actual percentage when it is disclosed, read the ingredient list and judge the complete formula."),
    ("t056", J, "One fashionable ingredient cannot rescue a badly built product."),
    ("t057", S, "You may deactivate the Jargon Alarm now."),
    ("t058", S, "K-beauty did not invent ectoin. Bacteria developed the survival strategy."),
    ("t059", S, "Korean formulators are using it alongside familiar barrier-supporting ingredients in lightweight serums, toners and sun products."),
    ("t060", J, "So bacteria invented it, and Korea gave it better packaging."),
    ("t061", S, "Aggressively simplified, but acceptable."),
    # ---- CH6 -- the honest verdict (unchanged) --------------------------
    ("t062", S, "Ectoin is not the new hyaluronic acid. It is not a miracle, and the evidence is not strong enough for dramatic promises."),
    ("t063", S, "It is a genuinely interesting supporting ingredient that may help dry or stressed skin."),
    ("t064", J, "Supporting actor, not superhero."),
    ("t065", S, "Exactly. Look for the actual percentage, then judge the whole formula."),
    ("t066", J, "And would I put a bacteria-made survival molecule on my face?"),
    ("t067", S, "Would you?"),
    ("t068", J, "I have already purchased snail mucus. The dignity ship sailed years ago."),
    ("t069", S, "Fair enough."),
    ("t070", J, "What questionable skincare ingredient are we investigating next?"),
]

# ---- COMPOSITION UNITS ----------------------------------------------------
# A UNIT is one sub-composition file. A PHASE is a named beat inside it.
#
# WHY UNITS AND NOT ONE FILE PER EXCHANGE. This piece carries no persistent
# speaker actors -- attribution is type-only -- so nothing spans a cut by
# default, which is precisely how the predecessor passed every per-scene gate
# and still read as slides. The counter-move is to merge every ACTOR-CONTINUOUS
# run into ONE file whose phases rearrange the same DOM nodes instead of
# redrawing them in a sibling file.
#
# COLD-OPEN REVISION: 01-hook, 02-industry, 03-cell are gone. In their place,
# two new merged units carry the camera path bottle -> brine -> cell ->
# molecule that used to open at 03-cell's midpoint. 12-bottle drops its
# "turn the bottle around" phases (b, c) -- that reveal now lives in
# 01-bottle -- and keeps only phase a (who it's for) and phase d (the INCI
# list payoff), so a viewer who saw the close-up at frame 0 gets the wide
# shot here rather than the same beat twice.
UNITS = [
    # MERGED -- one bottle actor, two phases. Extreme close-up on the front
    # label; the turn IS the label's own scaleX-through-zero, not a cut.
    ("01-bottle",    [("a", ["t071"]),
                      ("b", ["t072"])]),
    # MERGED -- one continuous space, three phases: brine field (the origin)
    # -> one cell dehydrating (the raisin) -> the molecule that answers it.
    # Camera legs L0->L1->L2 across it, same idiom 03-cell used to carry.
    ("02-origin",    [("a", ["t073", "t002", "t003"]),
                      ("b", ["t074"]),
                      ("c", ["t075"])]),
    # MERGED -- ONE protein+shell actor, five phases. The ring REARRANGES
    # between phases (guards close, then a third break rank); it is never
    # rebuilt. This is the unit that answers the predecessor's 09/10 duplication.
    ("04-protein",   [("a", ["t016"]),
                      ("b", ["t017", "t018"]),
                      ("c", ["t019", "t020"]),
                      ("d", ["t021", "t022"]),
                      ("e", ["t023", "t024"])]),
    # MERGED -- keratin strands + water, four phases.
    ("05-skin",      [("a", ["t025"]),
                      ("b", ["t026", "t027", "t028"]),
                      ("c", ["t029", "t030", "t031"]),
                      ("d", ["t032"])]),
    ("06-trial104",  [("a", ["t033", "t034"])]),
    ("07-preference", [("a", ["t035", "t036", "t037"])]),
    ("08-eczema",    [("a", ["t038"])]),
    ("09-miracle",   [("a", ["t039", "t040", "t041", "t042"])]),
    ("10-notprove",  [("a", ["t043", "t044"])]),
    ("11-twelve",    [("a", ["t045", "t046", "t047", "t048"])]),
    # MERGED -- one bottle, TWO phases this revision (was four). Phases b/c
    # (the turn + the blend split) are retired -- that reveal now opens the
    # video. This keeps who-it's-for (a) and the INCI-list payoff (d), camera
    # flying to the real Ectoin position -- the wide shot the open only glimpsed.
    ("12-bottle",    [("a", ["t049", "t050"]),
                      ("d", ["t055", "t056", "t057"])]),
    ("13-kbeauty",   [("a", ["t058", "t059", "t060", "t061"])]),
    ("14-notnew",    [("a", ["t062"])]),
    ("15-whatitis",  [("a", ["t063", "t064"])]),
    ("16-action",    [("a", ["t065"])]),
    ("17-dignity",   [("a", ["t066", "t067", "t068", "t069"])]),
    ("18-endscreen", [("a", ["t070"])]),
]

MERGED = {"01-bottle", "02-origin", "04-protein", "05-skin", "12-bottle"}

# Flat (unit, [turns]) view for the timing walk.
SCENES = [(cid, [t for _, ts in phases for t in ts]) for cid, phases in UNITS]

SPEAKER = {tid: spk for tid, spk, _ in TURNS}
TEXT = {tid: txt for tid, _, txt in TURNS}

if __name__ == "__main__":
    words = sum(len(t.split()) for _, _, t in TURNS)
    ns = sum(1 for _, s, _ in TURNS if s == S)
    print(f"{len(TURNS)} turns / {len(SCENES)} scenes / {words} words")
    print(f"  SOULHABIT {ns}  JAY {len(TURNS)-ns}")
    seen = [t for _, ts in SCENES for t in ts]
    assert seen == [t for t, _, _ in TURNS], "SCENES must cover every turn in order"
    print("  turn coverage OK")
