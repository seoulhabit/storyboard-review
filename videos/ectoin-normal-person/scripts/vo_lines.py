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

VERDICT-COMPRESSION REVISION (2026-09-03, second revision). Cuts the
false line ("None of it passed peer review", t048 -- see CLAIMS.md) and
adds the on-screen verdict inside the first ~20s (t076, t077), per an
operator brief that also asked for 35-45 turns / ~430-500 words. New turns
are APPENDED as t076-t082 rather than renumbered, continuing the same
convention the cold-open revision (t071-t075) established: frames_spec.py
has ~180 literal t['tNNN'] lookups, and renumbering would touch every one
of them for no benefit. TURNS list ORDER must equal playback order (see the
assert at the bottom of this file); turn id numbering is NOT required to be
monotonic with it.

Retired this revision: t048 (false, cut per operator decision -- see
CLAIMS.md "Removed this revision"), t019/t020 (merged into t078, the
celebrity analogy), t022/t023/t024 (the "event coordinator" gag and its
own hedge -- cut for length; the hedge survives folded into t017), t027/t028
("translating yourself" exchange), t037 ("Preference, not Cinderella"),
t043/t044 (merged into t079), t049/t050 (merged into t080), t058/t059
(merged into t082), t061, t066's standalone S interjection t067 and the
closing t069 "Fair enough" (t066+t068 merged into one JAY turn, t081, to
keep the dignity-ship joke intact in fewer turns).

Result: 58 turns/595 words (prior revision) -> 44 turns/489 words this
revision. Both the turn-count band (35-45) and word band (430-500) in the
brief are met. Real timing, as always, comes from ffprobe'd VO via
scripts/timing.py and supersedes any word-count-based runtime estimate the
moment takes exist -- see 00-decision-ledger.md for the runtime arithmetic
this revision was planned against.
"""

S, J = "S", "J"

TURNS = [
    # ---- CH1: the reveal, the VERDICT (within ~20s), then the origin -----
    ("t071", S, "This bottle says eleven percent. Does that mean eleven percent ectoin?"),
    ("t072", S, "No. It's a blend."),
    ("t076", S, "Ectoin itself may genuinely help dry or stressed skin feel more comfortable."),
    ("t077", S, "But the evidence is limited, and it is not a miracle or a replacement for treatment."),
    ("t073", S, "Before skincare marketing found it, ectoin belonged to a bacterium in extremely salty water."),
    ("t002", J, "Bacteria invented skincare?"),
    ("t003", S, "Not intentionally."),
    ("t074", S, "The salt pulls water out of the cell, turning it into a microscopic raisin. Ectoin helps keep the machinery stable."),
    ("t075", S, "Skincare borrowed the molecule. Marketing borrowed the drama."),
    # ---- CH2: give the protein some space (mechanism, compressed hardest) -
    ("t016", S, "Ectoin belongs to a group of protective molecules sometimes called extremolytes."),
    ("t017", S, "Its effects involve how water arranges around proteins. Scientists call part of it preferential exclusion, though the real picture is messier."),
    ("t018", J, "Even the alarm wants you to stop."),
    ("t078", S, "Picture a protein as a celebrity with security. Ectoin may help that water stay organised without touching the protein directly."),
    ("t021", J, "So ectoin gives proteins personal space."),
    # ---- CH3: what this means for skin -------------------------------------
    ("t025", S, "Laboratory research suggests ectoin may help stabilise structures and change how keratin in the outer skin layer interacts with water."),
    ("t026", S, "It may help dry or stressed skin cope more comfortably."),
    ("t029", J, "Does ectoin create an invisible protective force field around my face?"),
    ("t030", S, "No."),
    ("t031", J, "Finally, a skincare ingredient with realistic boundaries."),
    ("t032", S, "Think of ectoin as support for the skin barrier, not body armour."),
    # ---- CH4: does it work on people ----------------------------------------
    ("t033", S, "In one study, 104 women compared a cream containing 2 percent ectoin with the same cream without it."),
    ("t034", S, "The women preferred the ectoin version."),
    ("t035", J, "So it worked?"),
    ("t036", S, "They liked it better. That is real, but not the same as a machine proving their skin changed."),
    ("t038", S, "Another study followed 65 people with mild to moderate eczema. Over four weeks the ectoin cream matched the comparison and was well tolerated."),
    ("t039", J, "Promising?"),
    ("t040", S, "Yes."),
    ("t041", J, "Miracle?"),
    ("t042", S, "No."),
    ("t079", S, "It does not prove ectoin cures eczema or replaces treatment. The evidence is limited, and some research comes from companies that sell it."),
    ("t046", S, "A PubMed search found twelve clinical trials."),
    ("t047", J, "Twelve? My group chat has produced more research on whether someone should text their ex."),
    # t048 REMOVED this revision -- false, contradicted C5/C6. See CLAIMS.md.
    # ---- CH5: how to read the bottle -----------------------------------------
    ("t080", S, "Ectoin suits dry, sensitive or irritated skin, and pairs with panthenol, glycerin, squalane and ceramides."),
    ("t055", S, "Exactly. Check the actual percentage when it is disclosed, read the ingredient list and judge the complete formula."),
    ("t056", J, "One fashionable ingredient cannot rescue a badly built product."),
    ("t057", S, "You may deactivate the Jargon Alarm now."),
    ("t082", S, "K-beauty did not invent ectoin. Bacteria developed the survival strategy. Korean formulators pair it with barrier ingredients in light textures."),
    ("t060", J, "So bacteria invented it, and Korea gave it better packaging."),
    # ---- CH6: the honest verdict ----------------------------------------------
    ("t062", S, "Ectoin is not the new hyaluronic acid, not a miracle, and the evidence does not support dramatic promises."),
    ("t063", S, "It is a genuinely interesting supporting ingredient that may help dry or stressed skin."),
    ("t064", J, "Supporting actor, not superhero."),
    ("t065", S, "Exactly. Look for the actual percentage, then judge the whole formula."),
    ("t081", J, "And would I put a bacteria-made survival molecule on my face? I already bought snail mucus. The dignity ship sailed years ago."),
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
# THIS REVISION: 01-bottle gains a third phase (c) carrying the verdict,
# t076/t077, so the payoff lands inside the same extreme-close-up actor as
# the reveal -- no new cut needed for it. 04-protein drops from 5 phases to
# 4 (phase e, the event-coordinator gag, is gone; its former phase d turn
# t022 is folded into t017's text in phase b, so phase d now carries only
# t021). 05-skin's phase b drops to a single turn (t027/t028 cut). 07-
# preference keeps its 2-turn shape (t037 cut, not the whole exchange).
# 09-miracle through 11-twelve are unchanged in structure (11-twelve loses
# only t048 from its turn list). 12-bottle's phase a collapses to the merged
# t080. 13-kbeauty's phase a collapses from 4 turns to 2 (t058+t059 merged
# into t082, t061 cut). 17-dignity's phase a collapses from 4 turns to 1
# (t066+t068 merged into t081; t067's "Would you?" and t069's "Fair enough"
# are cut rather than kept as separate turns bracketing a single-line reply).
UNITS = [
    # MERGED -- one bottle actor, three phases. Extreme close-up on the front
    # label; the turn IS the label's own scaleX-through-zero, not a cut.
    # Phase c (the verdict) stays on the SAME actor -- no new visual beat
    # needed to justify it landing inside the first 20s.
    ("01-bottle",    [("a", ["t071"]),
                      ("b", ["t072"]),
                      ("c", ["t076", "t077"])]),
    # MERGED -- one continuous space, three phases: brine field (the origin)
    # -> one cell dehydrating (the raisin) -> the molecule that answers it.
    ("02-origin",    [("a", ["t073", "t002", "t003"]),
                      ("b", ["t074"]),
                      ("c", ["t075"])]),
    # MERGED -- ONE protein+shell actor, now FOUR phases (was five). The
    # ring rearranges between phases; it is never rebuilt.
    ("04-protein",   [("a", ["t016"]),
                      ("b", ["t017", "t018"]),
                      ("c", ["t078"]),
                      ("d", ["t021"])]),
    # MERGED -- keratin strands + water, four phases (phase b now one turn).
    ("05-skin",      [("a", ["t025"]),
                      ("b", ["t026"]),
                      ("c", ["t029", "t030", "t031"]),
                      ("d", ["t032"])]),
    ("06-trial104",  [("a", ["t033", "t034"])]),
    ("07-preference", [("a", ["t035", "t036"])]),
    ("08-eczema",    [("a", ["t038"])]),
    ("09-miracle",   [("a", ["t039", "t040", "t041", "t042"])]),
    ("10-notprove",  [("a", ["t079"])]),
    ("11-twelve",    [("a", ["t046", "t047"])]),
    # MERGED -- one bottle, two phases (unchanged from the cold-open
    # revision). Phase a is now the merged who-it's-for turn.
    ("12-bottle",    [("a", ["t080"]),
                      ("d", ["t055", "t056", "t057"])]),
    ("13-kbeauty",   [("a", ["t082", "t060"])]),
    ("14-notnew",    [("a", ["t062"])]),
    ("15-whatitis",  [("a", ["t063", "t064"])]),
    ("16-action",    [("a", ["t065"])]),
    ("17-dignity",   [("a", ["t081"])]),
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
