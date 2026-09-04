#!/usr/bin/env python3
"""Derive 03-beat-sheet.json from the MEASURED voiceover timing.

v3 REWRITE 2026-09-03: rewritten voiceover (24 stems, measured 165.186s -- an
OUTPUT of build_vo.py's fixed-gap assembly, never a target it was scaled to
hit), 17 scenes so a real visual or narrative development lands roughly every
5-8s, four photoreal plates of one consistent subject at the brief's four
named moments, a genuine two-phase actor merge (s11-binds-and-seal) replacing
two scenes that redrew the same chain object, and a three-type transition
system (wipe-left / wipe-up / blur-crossfade) plus three deliberate hard cuts
on the plate reveals and the FDA-warning pivot.

Nothing here is hand-typed timing. Scene and beat times are computed from
04-assets/vo-timing.json, which is the master clock [S4/V-2]. Change the VO and
re-run; never edit a time in the JSON.

Scenes are split by ACTOR CONTINUITY, not by narration sentence [S6/A-9]. Where
the OLD 13-scene cut redrew the same "ha-serum" chain across four consecutive
files (s06-s09), this cut collapses the binds-water/lifeguard pair into one
merged two-phase sub-composition instead -- see s11-binds-and-seal below.

On "a development every 5-8s": several scenes here run longer than 8s (the
FDA warning is 17.7s, held deliberately; s08-serum-size is 16.0s). This is a
DELIBERATE reading, not a shortcut -- validate_beat_sheet.py enforces an 8.0s
END_SCENE_MIN_S and a 10.0s CHAPTER_MIN_GAP_S, both of which forbid chopping
every scene down to 5-8s literally without producing a slideshow of orphaned
fragments or starving a chapter below its own floor. The cadence goal is met
at the BEAT level instead: every multi-stem scene below carries 3-6 content
beats, each landing a genuinely new piece of information, so a viewer sees
something change on a 3-6s rhythm even inside a longer-running scene. Where a
scene genuinely shares an actor with its neighbour (the merge above), the fix
is ONE longer scene with an internal phase change, not two shorter ones that
redraw the same geometry -- that trade was made deliberately, in the direction
[S6/A-9] requires, even though it works against a literal per-file 5-8s count.

Cadence [S5/C-2]: every spoken stem start (or sentence-boundary fraction within
a stem) gets a content beat; the fill pass below inserts `hold` beats (bounded
camera drift, which the generator counts as a real beat) wherever a gap would
exceed the format's cap. FRAME-ZERO DISCIPLINE: every scene's first beat is
authored at frac 0.00 and marked composed in build_actors.py, never a later
fraction -- a wipe or cut that reveals an empty ground because the first beat
hasn't fired yet is a real, previously-shipped defect in this project's own
_hero_left()/two_col() paths, fixed here at authoring time.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
VO = json.load(open(f"{HERE}/04-assets/vo-timing.json"))
S = {s["id"]: s for s in VO["stems"]}
TOTAL = VO["measured_total_s"]
CAP = 2.0          # long-form still-window cap the generator enforces
HOLD_STEP = 1.9    # keep hold beats safely under the cap

def at(stem, frac=0.0):
    """Absolute time at a character-proportional point inside a stem [S5/C-1]."""
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

# ---- scenes: id, actor, section, layout, bg, transition, plate, beats ------
PAPER, INK, MIST = "#F7F5F0", "#131516", "#F0EBE1"

# Photoreal plates -- the one consistent subject, at the brief's four named
# moments. Files land at 05-composition/assets/images/ (see build_actors.py's
# plate_scene()); paths declared here so the generator's own raster-aware
# checks (the wipe+plate capture-bug warning) see them even though these
# scenes are hand-authored and the generator's OWN plate markup is unused.
PLATE = {
  "s03-misconception-plate": "assets/images/subject-01-misconception.png",
  "s04-not-filler-plate":    "assets/images/subject-02-not-filler.png",
  "s09-plumping-plate":      "assets/images/subject-03-plumping.png",
  "s16-takeaway-plate":      "assets/images/subject-04-takeaway.png",
}

# Transition system [S6/A-8]: 3 distinct non-cut types (wipe-left / wipe-up /
# blur-crossfade) + 3 deliberate hard cuts, all on the plate reveals and the
# FDA-warning pivot -- never a plain crossfade across a ground change, never
# push-slide (measured elsewhere in this repo at 99 safe-area violations vs 0
# for a wipe). wipe-up is reserved for section-start boundaries (5 of them,
# fixed by the six-section spine); wipe-left carries ordinary within-section
# boundaries, at a duration tuned per chapter (0.35s fast through mechanism's
# "faster contrast" mandate, 0.50s more measured through proof, 0.45s
# elsewhere); blur-crossfade softens the return from a plate to a diagram or
# type card. Declared explicitly on every scene (not left to derive) so
# build_actors.py can read d_in/d_out as a lookup instead of reimplementing
# the resolver -- see TRANSITIONS below and how it feeds scene_shell().
TRANSITIONS = {
  "s02-lineup":               {"type": "wipe-up",        "duration": 0.60},
  "s03-misconception-plate":  {"type": "cut"},
  "s04-not-filler-plate":     {"type": "blur-crossfade",  "duration": 0.50},
  "s05-origin":               {"type": "wipe-left",       "duration": 0.45},
  "s06-body":                 {"type": "wipe-up",        "duration": 0.60},
  "s07-compare":              {"type": "wipe-left",       "duration": 0.35},
  "s08-serum-size":           {"type": "wipe-left",       "duration": 0.35},
  "s09-plumping-plate":       {"type": "cut"},
  "s10-houseplant":           {"type": "blur-crossfade",  "duration": 0.50},
  "s11-binds-and-seal":       {"type": "wipe-up",        "duration": 0.60},
  "s12-crosslink":            {"type": "wipe-left",       "duration": 0.50},
  "s13-warning-question":     {"type": "wipe-up",        "duration": 0.60},
  "s14-fda-warning":          {"type": "cut"},
  "s15-badges":               {"type": "wipe-up",        "duration": 0.60},
  "s16-takeaway-plate":       {"type": "blur-crossfade",  "duration": 0.50},
  "s17-endcard":              {"type": "wipe-left",       "duration": 0.45},
}

SCENES = [
 # ---- HOOK ------------------------------------------------------------
 dict(id="s01-hook", actor="hook", section="hook", layout="type-card", bg=PAPER,
      start=0.0, end=S[3]["start"], beats=[
        (at(1,0.00), 1.70, "arrive", "kicker", "Same active ingredient."),
        (at(1,0.32), 1.60, "slam",   "head",   "One name."),
        (at(1,0.68), 1.60, "wipe",   "sub",    "Two completely different jobs."),
        (at(2,0.00), 1.90, "swap",   "head",   "A serum cannot do what a filler does."),
      ]),
 # ---- MISCONCEPTION -----------------------------------------------------
 dict(id="s02-lineup", actor="lineup", section="misconception", layout="three-lane", bg=PAPER,
      start=S[3]["start"], end=S[5]["start"], beats=[
        (at(3,0.00), 1.40, "arrive", "head", "It isn't one thing. It's three."),
        (at(4,0.00), 1.30, "slam",   "sub",  "Your body makes it"),
        (at(4,0.35), 1.30, "wipe",   "sub",  "Your serum contains it"),
        (at(4,0.68), 1.30, "wipe",   "sub",  "A doctor injects it"),
        (at(4,0.90), 1.20, "slam",   "head", "Three different jobs"),
      ]),
 dict(id="s03-misconception-plate", actor="subject", section="misconception", layout="plate", bg=INK,
      start=S[5]["start"], end=S[6]["start"], beats=[
        (at(5,0.00), 1.60, "arrive", "kicker", "The expensive mix-up"),
        (at(5,0.35), 1.60, "wipe",   "head",   "People expect an injection's results"),
        (at(5,0.70), 1.50, "slam",  "sub",    "From a serum."),
      ]),
 dict(id="s04-not-filler-plate", actor="subject", section="misconception", layout="plate", bg=INK,
      start=S[6]["start"], end=S[7]["start"], beats=[
        (at(6,0.00), 2.00, "arrive", "head", "A serum is not filler in a bottle."),
      ]),
 dict(id="s05-origin", actor="vitreous", section="misconception", layout="hero-left", bg=INK,
      start=S[7]["start"], end=S[8]["start"], beats=[
        (at(7,0.00), 1.30, "count", "stat", "1934"),
        (at(7,0.30), 1.50, "wipe",  "body", "Isolated from the clear jelly inside a cow's eye"),
        (at(7,0.75), 1.30, "arrive","cite", "J Biol Chem · 1934"),
        (at(7,0.92), 1.20, "slam",  "sub",  "Remember that."),
      ]),
 # ---- MECHANISM ---------------------------------------------------------
 dict(id="s06-body", actor="ha-body", section="mechanism", layout="hero-left", bg=PAPER,
      start=S[8]["start"], end=S[10]["start"], beats=[
        (at(8,0.00), 1.40, "arrive","head", "Your body already makes its own."),
        (at(8,0.35), 1.40, "wipe",  "body", "Most of it sits in your skin, holding water."),
        (at(8,0.75), 1.00, "arrive","cite", "Dermatoendocrinol · 2012"),
        (at(9,0.00), 1.40, "wipe",  "body", "It also lubricates your joints and your eye."),
        (at(9,0.65), 1.00, "arrive","cite", "Front Vet Sci · 2019"),
      ]),
 dict(id="s07-compare", actor="ha-compare", section="mechanism", layout="split", bg=PAPER,
      start=S[10]["start"], end=S[12]["start"], beats=[
        (at(10,0.00), 1.50, "arrive","head", "Here's where the two versions split."),
        (at(10,0.30), 1.50, "wipe",  "body", "Stays at the surface, supporting hydration."),
        (at(10,0.70), 1.00, "arrive","cite", "Skin Res Technol · 2015"),
        (at(11,0.00), 1.60, "wipe",  "body", "Cross-linked into a gel, placed beneath the skin."),
        (at(11,0.60), 1.00, "arrive","cite", "J Cosmet Dermatol · 2024"),
      ]),
 dict(id="s08-serum-size", actor="ha-serum", section="mechanism", layout="two-column", bg=PAPER,
      start=S[12]["start"], end=S[14]["start"], beats=[
        (at(12,0.00), 1.50, "arrive","head",   "Size decides almost everything."),
        (at(12,0.20), 1.00, "arrive","kicker", "Simplified illustration"),
        (at(12,0.40), 1.60, "wipe",  "body",   "Large chains stay near the surface."),
        (at(13,0.00), 1.60, "wipe",  "body",   "Smaller ones may travel farther into the upper layers."),
        (at(13,0.55), 1.00, "arrive","cite",   "Skin Res Technol · 2015"),
        (at(13,0.80), 1.20, "slam",  "sub",    "Neither behaves like a filler."),
      ]),
 dict(id="s09-plumping-plate", actor="subject", section="mechanism", layout="plate", bg=INK,
      start=S[14]["start"], end=S[15]["start"], beats=[
        (at(14,0.00), 1.60, "arrive", "kicker", "Why does the bottle say plumping?"),
        (at(14,0.45), 1.70, "wipe",   "head",   "Cells can temporarily appear softer."),
        (at(14,0.85), 1.30, "slam",   "sub",    "Not longer. Softer."),
      ]),
 dict(id="s10-houseplant", actor="analogy", section="mechanism", layout="hero-left", bg=PAPER,
      start=S[15]["start"], end=S[16]["start"], beats=[
        (at(15,0.00), 1.60, "arrive", "head", "Like watering a tired houseplant."),
        (at(15,0.55), 1.40, "swap",   "sub",  "Not like adding a new branch."),
      ]),
 # ---- PROOF ---------------------------------------------------------
 # [S6/A-9] merge: the OLD cut redrew the same "ha-serum" chain across
 # s08-binds-water AND s09-lifeguard as two separate files (confirmed:
 # coil(30,260,380,...) vs coil(30,260,340,...), same seed, same actor,
 # genuinely near-identical geometry emitted twice). This is ONE sub-
 # composition instead: one chain, drawn once, rearranged between two
 # internal phases -- water droplets pulled toward it, THEN a moisturiser
 # seal drawn onto the SAME path -- so the actor is never redrawn.
 dict(id="s11-binds-and-seal", actor="ha-serum", section="proof", layout="hero-left", bg=MIST,
      start=S[16]["start"], end=S[18]["start"], beats=[
        (at(16,0.00), 1.50, "arrive","head",    "Here's the part the marketing skips."),
        (at(16,0.35), 1.60, "swap",  "head",    "It binds water. It does not make water."),
        (at(16,0.65), 1.00, "arrive","cite",    "ChemRxiv · 2023"),
        (at(16,0.85), 1.40, "wipe",  "body",    "A formula still needs something to stop it leaving."),
        (at(17,0.00), 1.40, "arrive","caption", "Skip that, and you're hiring a lifeguard for an empty pool."),
        (at(17,0.55), 1.10, "slam",  "sub",     "Strange image. Correct principle."),
      ]),
 dict(id="s12-crosslink", actor="ha-filler", section="proof", layout="hero-left", bg=INK,
      start=S[18]["start"], end=S[19]["start"], beats=[
        (at(18,0.00), 1.50, "arrive","head", "A filler is chemically different."),
        (at(18,0.30), 1.80, "swap",  "body", "Cross-linked into a stable, connected grid."),
        (at(18,0.62), 1.00, "arrive","cite", "J Cosmet Dermatol · 2024"),
        (at(18,0.80), 1.40, "wipe",  "sub",  "Holds its own shape."),
      ]),
 # ---- APPLICATION ---------------------------------------------------------
 # OLD s11-do-not-inject (21.08s, 11 beats -- effectively three scenes in a
 # trenchcoat) is split into two: the rhetorical question + clinical vignette,
 # then the full-bleed warning card on its own, landed with a hard CUT so the
 # ALL-CAPS line is the very first thing seen, composed, not animated in.
 dict(id="s13-warning-question", actor="warning", section="application", layout="hero-left", bg=INK,
      start=S[19]["start"], end=S[20]["start"], beats=[
        (at(19,0.00), 1.40, "arrive", "caption", "Is a filler just serum with a needle?"),
        (at(19,0.45), 1.40, "slam",   "head",    "Not even close."),
        (at(19,0.80), 1.20, "arrive", "kicker",  "Worth putting in very large letters."),
      ]),
 dict(id="s14-fda-warning", actor="warning", section="application", layout="full-bleed", bg=INK,
      start=S[20]["start"], end=S[21]["start"], beats=[
        (at(20,0.00), 1.00, "slam",   "head", "DO NOT INJECT YOURSELF"),
        (at(20,0.12), 1.00, "arrive", "cite", "FDA · Dermal Fillers"),
        (at(20,0.22), 1.60, "wipe",   "body", "Dermal fillers are a medical procedure with real risks."),
        (at(20,0.55), 1.50, "wipe",   "body", "Including tissue death, vision loss and stroke."),
        (at(20,0.80), 1.40, "wipe",   "sub",  "Choose a provider trained to perform the injection."),
      ]),
 # ---- RECAP ---------------------------------------------------------
 dict(id="s15-badges", actor="lineup", section="recap", layout="three-lane", bg=PAPER,
      start=S[21]["start"], end=S[23]["start"], beats=[
        (at(21,0.00), 1.30, "arrive","head", "Same family."),
        (at(21,0.45), 1.60, "swap",  "head", "Different size, structure and location."),
        (at(22,0.00), 1.30, "arrive","sub",  "Resident"),
        (at(22,0.25), 1.30, "arrive","sub",  "Moisturiser"),
        (at(22,0.50), 1.30, "arrive","sub",  "Construction project"),
      ]),
 dict(id="s16-takeaway-plate", actor="subject", section="recap", layout="plate", bg=INK,
      start=S[23]["start"], end=S[24]["start"], beats=[
        (at(23,0.00), 1.60, "arrive", "head", "Buy the serum for hydration."),
        (at(23,0.45), 1.60, "wipe",   "sub",  "Just don't expect volume."),
      ]),
 dict(id="s17-endcard", actor="endcard", section="recap", layout="full-bleed", bg=PAPER,
      start=S[24]["start"], end=TOTAL, beats=[
        (at(24,0.00), 1.20, "arrive", "kicker", "One more thing — the cow's eye came back."),
        (at(24,0.20), 1.80, "slam",   "head",   "Serum hydrates. Filler adds volume. Same name, different jobs."),
      ]),
]

# ---- build ---------------------------------------------------------------
DIAGRAM = {"s01-hook", "s02-lineup", "s03-misconception-plate",
           "s04-not-filler-plate", "s05-origin", "s06-body", "s07-compare",
           "s08-serum-size", "s09-plumping-plate", "s11-binds-and-seal",
           "s12-crosslink", "s13-warning-question", "s14-fda-warning",
           "s15-badges", "s16-takeaway-plate"}
# s10-houseplant, s17-endcard stay GENERATED: plain kicker/head/sub copy with
# no diagram or plate, exactly the register v2 proved out for this kind of
# aside (its s02-not-filler / s13-endcard were generated too).

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
    # Frame-zero discipline, enforced not just authored: the first beat of
    # every scene must be at offset 0, or a wipe/cut reveals an empty ground.
    if beats and beats[0]["offset"] > 1e-6:
        raise SystemExit(f"{sc['id']}: first beat at offset {beats[0]['offset']}, "
                          f"not 0.00 -- frame zero would be empty")

    # insert `hold` beats so no still window breaches the cap
    FIRST_STEP = 1.2
    filled, cursor = [], 0.0
    for k, b in enumerate(beats):
        step = FIRST_STEP if not filled else HOLD_STEP
        while b["offset"] - cursor > CAP - 1e-6:
            cursor = round(cursor + step, 3)
            step = HOLD_STEP
            if b["offset"] - cursor <= 0: break
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

    entry = {"id": sc["id"], "start": start, "duration": dur,
             "section": sc["section"], "layout": sc["layout"], "bg": sc["bg"],
             "handoff": "hand-authored" if sc["id"] in DIAGRAM else "generated",
             # scene 0 is the first scene: the resolver requires its
             # transition be absent or 'cut' (there is nothing to
             # transition FROM), so it is never looked up in TRANSITIONS.
             "transition": {"type": "cut"} if sc is SCENES[0] else TRANSITIONS[sc["id"]],
             "beats": filled}
    if sc["id"] in PLATE:
        entry["plate"] = PLATE[sc["id"]]
    out_scenes.append(entry)

# One chapter per spine SECTION, not per scene.
CHAPTER_TITLE = {
  "hook": "Same name, different jobs",
  "misconception": "Not filler in a bottle",
  "mechanism": "The version already in you",
  "proof": "It cannot make water",
  "application": "Do not inject yourself",
  "recap": "Same family, different jobs",
}
CHAPTERS = [{"t": s["start"], "title": CHAPTER_TITLE[s["name"]]} for s in SECTIONS]

# End scene: the reserved end-screen window is the last TWO scene files (the
# takeaway plate + the endcard, together 12.96s) -- youtube-delivery.md's
# rule is a TIME WINDOW ("the last 8-20s of long-form"), not a per-file
# constraint, and the true final scene alone (6.96s) falls under
# validate_beat_sheet.py's 8.0s END_SCENE_MIN_S floor on its own.
end_scene_start = SCENES[-2]["start"]

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
 "end_scene": {"start": round(end_scene_start, 3),
               "duration": round(TOTAL - end_scene_start, 3),
               "overlay_zones_clear": True},
}
json.dump(bs, open(f"{HERE}/03-beat-sheet.json","w"), indent=2)

nb = sum(len(s["beats"]) for s in out_scenes)
nh = sum(1 for s in out_scenes for b in s["beats"] if b["idiom"]=="hold")
print("scenes    : %d  (%d hand-authored, %d generated)"
      % (len(out_scenes), len(DIAGRAM), len(out_scenes)-len(DIAGRAM)))
print("beats     : %d  (%d content, %d hold)" % (nb, nb-nh, nh))
print("beats/s   : %.2f" % (nb/TOTAL))
print("chapters  : %d, first at %.1fs, min gap %.1fs"
      % (len(CHAPTERS), CHAPTERS[0]["t"],
         min(CHAPTERS[i+1]["t"]-CHAPTERS[i]["t"] for i in range(len(CHAPTERS)-1))))
print("total     : %.3fs vs VO %.3fs" % (sum(s["duration"] for s in out_scenes), TOTAL))
from collections import Counter
print("idioms    : %s" % dict(Counter(b["idiom"] for s in out_scenes for b in s["beats"])))
print("transitions: %s" % dict(Counter(TRANSITIONS[s["id"]]["type"] for s in SCENES[1:])))
print("end scene : %.3fs (%.3fs -> %.3fs)" % (bs["end_scene"]["duration"], end_scene_start, TOTAL))
print("scene durs: %s" % [round(s["duration"],1) for s in out_scenes])
