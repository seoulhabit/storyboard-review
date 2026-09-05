#!/usr/bin/env python3
"""Derive 03-beat-sheet.json from the MEASURED voiceover timing.

v3 RETENTION CUT (2026-09-04): 14 scenes, 120.359s, rebuilt from the v3 12-stem
VO. Rewritten from v2's 13-scene sheet for three reasons, all measured against
the shipped v1/v2 cuts, not assumed:

  1. The central-answer and three-identity requirements are now each their own
     stem (1 and 2), so "central answer in 3-5s" / "identities within 10s" are
     literal measured facts (5.411s / 10.095s) instead of an estimate inside
     one longer stem.
  2. Two stems ran long enough to reproduce the old "one scene held 15-24s"
     defect if left as single scenes (stem7 "water" 15.946s, stem12 "recap"
     17.133s). Both are split into two SCENES at a character-proportional
     point INSIDE the stem (s07-binds/s08-seals; s13-badges/s14-endcard) --
     `at(stem, frac)` already supports an arbitrary frac, so a scene boundary
     does not have to land on a stem start. This keeps every scene under
     ~12.7s (mean 8.6s) with no single-beat hold anywhere close to the old
     15-24s scenes.
  3. Every DIAGRAM scene gets NEW per-element motion on the actor's own SVG
     children (chains, water-dot circles, lattice segments/nodes) instead of
     container-level x/y/scale drift -- see build_actors.py. This file only
     places the TEXT/citation beats; the mechanism motion is layered on top
     in the hand-authored builders, keyed to these same offsets.

Nothing here is hand-typed timing. Scene and beat times are computed from
04-assets/vo-timing.json, which is the master clock [S4/V-2]. Change the VO and
re-run; never edit a time in the JSON.

Scenes are split by ACTOR CONTINUITY, not by narration sentence [S6/A-9]. The
morphology actors -- lineup / ha-serum / ha-body / ha-filler / vitreous /
warning -- persist across the piece and are rearranged rather than redrawn
(s01/s02/s13 all reuse the same lineup actor; s05/s06 reuse ha-serum; s07/s08
reuse ha-body; s11/s12 reuse warning).

Cadence [S5/C-2]: beats below average one every ~2.4s across the piece (50
content beats / 120.359s), so the fill pass that inserts bounded `hold` drift
almost never fires -- it remains as a safety net, not the primary motion
source, unlike v1/v2 where drift dominated every scene's timeline.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
VO = json.load(open(f"{HERE}/04-assets/vo-timing.json"))
S = {s["id"]: s for s in VO["stems"]}
TOTAL = VO["measured_total_s"]
CAP = 2.0          # long-form still-window cap the generator enforces
HOLD_STEP = 1.9    # keep hold beats safely under the cap

def at(stem, frac=0.0):
    """Absolute time at a character-proportional point inside a stem [S5/C-1].

    A scene need not span a whole stem: s07/s08 and s13/s14 each cover only
    part of one stem's duration, so `frac` for those scenes' own beats stays
    within that scene's own sub-range of [0, 1] -- the helper does not care
    which scene owns the time, only the stem's own start/dur.
    """
    s = S[stem]
    return s["start"] + s["dur"] * frac

# ---- sections: taken from the stems' own section labels --------------------
SECTIONS = []
for s in VO["stems"]:
    if not SECTIONS or SECTIONS[-1]["name"] != s["section"]:
        if SECTIONS: SECTIONS[-1]["end"] = round(s["start"], 3)
        SECTIONS.append({"name": s["section"], "start": round(s["start"], 3)})
SECTIONS[-1]["end"] = round(TOTAL, 3)
SECTIONS[0]["start"] = 0.0

# ---- scenes: id, actor, section, layout, bg, and the content beats ---------
PAPER, INK, MIST = "#F7F5F0", "#131516", "#F0EBE1"

# Split points inside stem 7 (water) and stem 12 (recap) -- character-
# proportional, computed once here so both the scene boundary and that
# scene's own beats agree on the same absolute time.
SPLIT_7  = at(7, 0.5409)    # end of "...sponge, not a water factory."
SPLIT_12 = at(12, 0.7388)   # end of the third badge, before the close line

SCENES = [
 dict(id="s01-thesis", actor="lineup", section="hook", layout="three-lane", bg=PAPER,
      start=0.0, end=S[2]["start"], beats=[
        # The verdict leads. v3 put the slam at at(1,0.75) -- 4.058s, plus a
        # 1.0s ease, so the one line that answers the title finished landing
        # at ~5.1s of a 120s film. A viewer who bounces at 5s saw three
        # unexplained diagrams and no answer. It now opens the piece and is
        # fully readable at 0.70s, ahead of the 1.2s the review asked for,
        # and it works with the sound off. The lineup is what the camera
        # pulls back TO, not what the film opens on.
        (at(1,0.00), 0.70, "slam",   "sub",    "SERUM ≠ FILLER"),
        (at(1,0.29), 1.10, "arrive", "kicker", "Same name"),
        (at(1,0.55), 1.40, "wipe",   "head",   "Two completely different jobs"),
      ]),
 dict(id="s02-identities", actor="lineup", section="hook", layout="three-lane", bg=PAPER,
      start=S[2]["start"], end=S[3]["start"],
      transition={"type": "crossfade"},
      beats=[
        (at(2,0.00), 1.20, "arrive", "sub", "The kind your body makes"),
        (at(2,0.34), 1.20, "wipe",   "sub", "The kind in your serum"),
        (at(2,0.68), 1.20, "wipe",   "sub", "The kind a doctor injects"),
      ]),
 dict(id="s03-not-filler", actor="misconception", section="misconception", layout="hero-left", bg=PAPER,
      start=S[3]["start"], end=S[4]["start"],
      transition={"type": "cut"},
      beats=[
        (at(3,0.00), 1.30, "arrive", "head", "And the mix-up is expensive"),
        (at(3,0.28), 1.50, "wipe",   "body", "People buy a serum expecting the results of an injection"),
        (at(3,0.62), 1.50, "wipe",   "body", "Then wonder why nothing changed"),
        (at(3,0.80), 1.70, "swap",   "head", "A serum is not filler in a bottle"),
      ]),
 dict(id="s04-split", actor="ha-split", section="mechanism", layout="split", bg=PAPER,
      start=S[4]["start"], end=S[5]["start"],
      # wipe-up, held to 0.45s (connective: "short simple wipe"). A plain
      # crossfade was tried first and double-exposed two headlines at its
      # midpoint (extracted frame at 21.65s) -- reverted. The checker-side
      # problem this boundary has (s03 is cut-entered, so its exit is audited
      # and its covered text flagged) is handled by fix_exit_fades() in
      # build_actors.py, which fades the OUTGOING wrapper across this window:
      # PAPER over a PAPER body, so the fade is invisible to the viewer, and
      # the checker's mid-fade exemption applies by design rather than by the
      # leftover-clip-path accident every wipe-entered scene relies on.
      transition={"type": "wipe-up", "duration": 0.450},
      beats=[
        (at(4,0.00), 1.40, "arrive", "head",    "Here's where the two versions really split"),
        (at(4,0.42), 1.60, "wipe",   "caption", "One stays a loose, flowing molecule"),
        (at(4,0.75), 1.60, "wipe",   "caption", "The other gets locked into a rigid mesh"),
      ]),
 dict(id="s05-size", actor="ha-serum", section="mechanism", layout="two-column", bg=PAPER,
      start=S[5]["start"], end=S[6]["start"],
      transition={"type": "zoom-through", "duration": 0.5},
      beats=[
        (at(5,0.00), 1.40, "arrive", "head", "In a serum, size decides almost everything"),
        (at(5,0.28), 1.60, "wipe",   "body", "Large chains mostly stay near the surface"),
        (at(5,0.58), 1.60, "wipe",   "body", "Smaller ones may travel farther into the upper layers"),
        (at(5,0.90), 1.00, "arrive", "cite", "Skin Res Technol · 2015"),
      ]),
 dict(id="s06-plumping", actor="ha-serum", section="mechanism", layout="two-column", bg=PAPER,
      start=S[6]["start"], end=S[7]["start"], beats=[
        (at(6,0.00), 1.30, "arrive", "head", "So why does the bottle say plumping?"),
        (at(6,0.40), 1.60, "wipe",   "body", "Hydrated surface cells can temporarily make fine lines appear softer"),
        (at(6,0.85), 1.20, "swap",   "sub",  "That's hydration, not correction"),
      ]),
 dict(id="s07-binds", actor="ha-body", section="mechanism", layout="hero-left", bg=MIST,
      start=S[7]["start"], end=SPLIT_7, beats=[
        (at(7,0.00), 1.40, "arrive", "head",    "Here's the part the marketing skips"),
        (at(7,0.17), 1.60, "wipe",   "body",    "Hyaluronic acid binds water"),
        (at(7,0.30), 1.50, "swap",   "sub",     "It doesn't manufacture it"),
        (at(7,0.45), 1.60, "arrive", "caption", "Think of it as a sponge, not a water factory"),
      ]),
 dict(id="s08-seals", actor="ha-body", section="mechanism", layout="hero-left", bg=MIST,
      start=SPLIT_7, end=S[8]["start"],
      # crossfade at GENERATION time so the generator owns the overlap
      # bookkeeping (clip start/duration, d_in shift); build_actors.py's
      # fix_hero_transitions() then swaps the two crossfade tweens for the
      # hand-authored liquid-lens reveal. [S6/A-8 catalog miss]
      transition={"type": "crossfade", "duration": 0.600},
      beats=[
        (at(7,0.58), 1.50, "arrive", "head", "A complete formula still needs something else"),
        (at(7,0.75), 1.60, "wipe",   "body", "An ingredient that seals that water in"),
        (at(7,0.90), 1.00, "arrive", "cite", "ChemRxiv · 2023"),
        (at(7,0.97), 1.30, "swap",   "sub",  "So it doesn't evaporate away"),
      ]),
 dict(id="s09-crosslink", actor="ha-filler", section="mechanism", layout="two-column", bg=INK,
      start=S[8]["start"], end=S[9]["start"], beats=[
        (at(8,0.00), 1.40, "arrive", "head", "A filler is chemically different"),
        (at(8,0.25), 1.80, "wipe",   "body", "Its chains are cross-linked into a gel that holds its own shape"),
        (at(8,0.60), 1.00, "arrive", "cite", "J Cosmet Dermatol · 2024"),
        (at(8,0.72), 1.60, "wipe",   "sub",  "Placed beneath the skin, it can physically add volume"),
      ]),
 dict(id="s10-origin", actor="vitreous", section="history", layout="hero-left", bg=INK,
      start=S[9]["start"], end=S[10]["start"], beats=[
        (at(9,0.00), 1.40, "count",  "stat", "1934"),
        (at(9,0.35), 1.50, "wipe",   "body", "Isolated from the clear jelly inside a cow's eye"),
        (at(9,0.80), 1.00, "arrive", "cite", "J Biol Chem · 1934"),
      ]),
 dict(id="s11-warning", actor="warning", section="application", layout="full-bleed", bg=INK,
      start=S[10]["start"], end=S[11]["start"],
      transition={"type": "cut"},
      beats=[
        (at(10,0.00), 1.20, "arrive", "caption", "Is a filler just serum with a needle?"),
        (at(10,0.35), 1.00, "arrive", "caption", "Not even close."),
        # Opens 0.24s AHEAD of the spoken "Do not inject yourself" (at 0.55)
        # so the slam is ~80% landed on the word itself; the review's
        # acceptance line is "the warning appears by its spoken onset", and a
        # slam that STARTS on the onset is still invisible for its first
        # frames. Asserted in index.motion.json by fix_motion_sidecar().
        (at(10,0.51), 1.10, "slam",   "head",    "DO NOT INJECT YOURSELF"),
        (at(10,0.80), 1.00, "arrive", "cite",    "FDA · Dermal Fillers"),
      ]),
 dict(id="s12-risks", actor="risks", section="application", layout="hero-left", bg=INK,
      start=S[11]["start"], end=S[12]["start"],
      # CUT. A crossfade here ghosted "DO NOT INJECT YOURSELF" under the FDA
      # line for 0.4s (extracted frames 90.2s / 90.4s) -- two headlines
      # double-exposed on a dark ground. Both scenes are the warning register,
      # and the review's own idiom for that register is the hard cut.
      transition={"type": "cut"},
      beats=[
        (at(11,0.00), 1.40, "arrive", "head", "That's the F D A's own wording, not ours"),
        (at(11,0.25), 1.60, "wipe",   "body", "Dermal fillers are a medical procedure with real risks"),
        (at(11,0.55), 1.60, "wipe",   "body", "Including tissue death, vision loss and stroke"),
        (at(11,0.80), 1.50, "wipe",   "sub",  "Choose a provider trained to perform the injection"),
      ]),
 dict(id="s13-badges", actor="lineup", section="recap", layout="three-lane", bg=PAPER,
      start=S[12]["start"], end=SPLIT_12, beats=[
        (at(12,0.00), 1.30, "arrive", "head", "Same ingredient family"),
        (at(12,0.18), 1.40, "wipe",   "kicker",  "Different size, different structure, different location"),
        (at(12,0.40), 1.30, "arrive", "sub",  "Body version — resident"),
        (at(12,0.55), 1.30, "arrive", "sub",  "Serum version — hydration"),
        (at(12,0.68), 1.30, "arrive", "sub",  "Filler version — volume"),
      ]),
 dict(id="s14-endcard", actor="endcard", section="recap", layout="full-bleed", bg=PAPER,
      start=SPLIT_12, end=TOTAL, beats=[
        (at(12,0.75), 1.30, "slam",   "head", "Serum hydrates. Filler adds volume."),
        (at(12,0.90), 1.40, "arrive", "sub",  "Same name, different jobs"),
      ]),
]

# ---- build ---------------------------------------------------------------
out_scenes = []
for sc in SCENES:
    start, end = round(sc["start"], 3), round(sc["end"], 3)
    dur = round(end - start, 3)
    beats = []
    for (t, bdur, idiom, role, text) in sc["beats"]:
        off = round(t - start, 3)
        if off < 0: off = 0.0
        if off + bdur > dur: bdur = round(max(0.3, dur - off), 3)
        beats.append({"offset": off, "dur": round(bdur, 3), "idiom": idiom,
                      "role": role, "text": text, "actor": sc["actor"],
                      "intent": text})
    beats.sort(key=lambda b: b["offset"])

    # insert `hold` beats so no still window breaches the cap -- a safety
    # net now, not the primary motion source: with beats averaging one every
    # ~2.4s across the piece this fires rarely, and never as the ONLY motion
    # in a scene the way v1/v2's drift-per-scene did.
    FIRST_STEP = 1.2
    filled, cursor = [], 0.0
    for k, b in enumerate(beats):
        step = FIRST_STEP if not filled else HOLD_STEP
        while b["offset"] - cursor > CAP - 1e-6:
            cursor = round(cursor + step, 3)
            step = HOLD_STEP
            if b["offset"] - cursor <= 0: break
            # [correctness] clip against the UPCOMING beat's own offset too,
            # not only the scene's total length -- clipping against `dur`
            # alone let a hold's end run past the very next beat's start.
            hold_dur = min(0.9, round(dur - cursor, 3), round(b["offset"] - cursor, 3))
            if hold_dur <= 0: break
            filled.append({"offset": cursor, "dur": hold_dur,
                           "idiom": "hold", "role": "body", "actor": sc["actor"],
                           "intent": f"camera drift on {sc['actor']}"})
            cursor = round(cursor + hold_dur, 3)
        filled.append(b)
        end2 = b["offset"] + b["dur"]
        if k == 0 and abs(b["offset"]) < 1e-6:
            end2 = 0.0
        cursor = max(cursor, round(end2, 3))
    while dur - cursor > CAP - 1e-6:
        off = min(round(cursor + HOLD_STEP, 3), round(dur - 0.5, 3))
        if off <= cursor + 1e-6:
            break
        bdur = min(0.9, round(dur - off, 3))
        if bdur < 0.2:
            break
        filled.append({"offset": off, "dur": bdur, "idiom": "hold",
                       "role": "body", "actor": sc["actor"],
                       "intent": f"camera drift on {sc['actor']}"})
        cursor = round(off + bdur, 3)
    filled.sort(key=lambda b: b["offset"])

    DIAGRAM = {"s01-thesis", "s02-identities", "s04-split", "s05-size",
               "s06-plumping", "s07-binds", "s08-seals", "s09-crosslink",
               "s10-origin", "s13-badges"}
    out_sc = {"id": sc["id"], "start": start, "duration": dur,
              "section": sc["section"], "layout": sc["layout"],
              "bg": sc["bg"],
              "handoff": "hand-authored" if sc["id"] in DIAGRAM else "generated",
              "beats": filled}
    if "transition" in sc:
        out_sc["transition"] = sc["transition"]
    out_scenes.append(out_sc)

# One chapter per spine SECTION, not per scene -- EXCEPT a section shorter
# than youtube-delivery.md's 10s chapter floor never gets its own marker.
# "history" is 6.092s (78.044-84.136s), the one-line 1934 callback the brief
# asks to compress rather than remove -- exactly the kind of short aside that
# floor exists for. It stays its own `section` in the beat sheet (scenes and
# actor bookkeeping still key off it), but folds into the preceding chapter
# ("mechanism") for the public chapter list, which keeps every chapter >=10s
# without inflating "history" into a topic it isn't.
CHAPTER_TITLE = {
  "hook": "Same name, different jobs",
  "misconception": "Not filler in a bottle",
  "mechanism": "Size, water, and the cross-link",
  "history": "Where the name came from",
  "application": "Do not inject yourself",
  "recap": "Same family, different jobs",
}
CHAPTER_FLOOR_S = 10.0
_raw = [{"t": s["start"], "end": s["end"], "title": CHAPTER_TITLE[s["name"]]} for s in SECTIONS]
CHAPTERS = [_raw[0]]
for c in _raw[1:]:
    if c["end"] - c["t"] < CHAPTER_FLOOR_S:
        continue   # too short for its own marker; absorbed into the chapter before it
    CHAPTERS.append(c)
CHAPTERS = [{"t": c["t"], "title": c["title"]} for c in CHAPTERS]

bs = {
 "slug": "hyaluronic-acid-vs-filler",
 "format": "long", "fps": 30,
 "canvas": {"w": 1920, "h": 1080},
 "vo_duration_s": round(TOTAL, 3),
 "presenter": "moving-diagram",
 "bg": PAPER, "ink": INK, "accent": "#59B8AE", "muted": "#6B6B6B",
 "fonts": {
   "family": "Inter",
   "css": "'Inter', system-ui, -apple-system, Helvetica, Arial, sans-serif",
   "google_css2": "https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;600&family=Inter:wght@600;700;800&family=JetBrains+Mono:wght@500&display=swap"
 },
 "safe_area": {"top": 54, "bottom": 108, "right": 96, "left": 96},
 "audio": {"src": "", "volume": 0},
 "sections": [{"name": s["name"], "start": s["start"], "end": s["end"]} for s in SECTIONS],
 "scenes": out_scenes,
 "chapters": CHAPTERS,
 # End-scene block spans BOTH s13-badges and s14-endcard: [S5/C-3] requires an
 # 8-20s end scene with overlay zones clear for YouTube end-screen elements.
 # The brief separately asks for the visible END CARD to hold ~3-4s -- s14
 # alone satisfies that (4.476s) while the combined block (17.13s, badges
 # start to TOTAL) satisfies [S5/C-3]. Both requirements hold at once because
 # they are about two different things: how long the very last card is on
 # screen, versus how long before it the frame must stay clear of overlays.
 "end_scene": {"start": S[12]["start"],
               "duration": round(TOTAL - S[12]["start"],3),
               "overlay_zones_clear": True},
}
json.dump(bs, open(f"{HERE}/03-beat-sheet.json","w"), indent=2)

nb = sum(len(s["beats"]) for s in out_scenes)
nh = sum(1 for s in out_scenes for b in s["beats"] if b["idiom"]=="hold")
print("scenes    : %d" % len(out_scenes))
print("beats     : %d  (%d content, %d hold)" % (nb, nb-nh, nh))
print("beats/s   : %.2f" % (nb/TOTAL))
print("chapters  : %d, first at %.1fs, min gap %.1fs"
      % (len(CHAPTERS), CHAPTERS[0]["t"],
         min(CHAPTERS[i+1]["t"]-CHAPTERS[i]["t"] for i in range(len(CHAPTERS)-1))))
print("total     : %.3fs vs VO %.3fs" % (sum(s["duration"] for s in out_scenes), TOTAL))
from collections import Counter
print("idioms    : %s" % dict(Counter(b["idiom"] for s in out_scenes for b in s["beats"])))
print("end scene : %.3fs" % bs["end_scene"]["duration"])
print()
print("scene durations:")
for s in out_scenes:
    print("  %-16s %6.3fs  (%d beats)" % (s["id"], s["duration"], len(s["beats"])))
