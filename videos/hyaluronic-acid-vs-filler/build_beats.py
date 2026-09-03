#!/usr/bin/env python3
"""Derive 03-beat-sheet.json from the MEASURED voiceover timing.

v2 REVISION 2026-09-03: single narrator, 13 scenes, ~160s (target band
2:20-2:40; trimmed speech alone measures 151.75s, so 160s is the tightest
target that leaves any gap budget at all -- see 04-assets/build_vo.py).

Nothing here is hand-typed timing. Scene and beat times are computed from
04-assets/vo-timing.json, which is the master clock [S4/V-2]. Change the VO and
re-run; never edit a time in the JSON.

Scenes are split by ACTOR CONTINUITY, not by narration sentence [S6/A-9]. The
three morphology actors -- ha-body / ha-serum / ha-filler -- persist across the
piece and are rearranged rather than redrawn.

Cadence [S5/C-2]: every spoken stem start gets a content beat; the fill pass
below inserts `hold` beats (bounded camera drift, which the generator counts as
a real beat) wherever a gap would exceed the format's cap. Content beats only
need to be written here -- the fill pass is unchanged from v1 and applies
uniformly to every scene, hand-authored or generated.
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

# ---- scenes: id, actor, section, layout, bg, and the content beats ---------
PAPER, INK, MIST = "#F7F5F0", "#131516", "#F0EBE1"

SCENES = [
 dict(id="s01-lineup", actor="lineup", section="hook", layout="three-lane", bg=PAPER,
      start=0.0, end=S[2]["start"], beats=[
        (at(1,0.00), 1.40, "arrive", "head",   "Your hyaluronic-acid serum cannot do what filler does."),
        (at(1,0.10), 1.00, "arrive", "kicker", "Same name"),
        (at(1,0.28), 1.30, "slam",   "sub",    "The kind your body makes"),
        (at(1,0.47), 1.30, "wipe",   "sub",    "The kind in your serum"),
        (at(1,0.66), 1.30, "wipe",   "sub",    "The kind a doctor injects"),
        (at(1,0.90), 1.00, "slam",   "head",   "Three completely different jobs"),
      ]),
 dict(id="s02-not-filler", actor="misconception", section="misconception", layout="hero-left", bg=PAPER,
      start=S[2]["start"], end=S[3]["start"], beats=[
        (at(2,0.00), 1.30, "arrive", "head", "And the mix-up is expensive"),
        (at(2,0.30), 1.40, "wipe",   "body", "People buy a serum expecting what an injection does"),
        (at(2,0.62), 1.60, "swap",   "head", "A serum is not filler in a bottle"),
      ]),
 dict(id="s03-origin", actor="vitreous", section="misconception", layout="hero-left", bg=INK,
      start=S[3]["start"], end=S[4]["start"], beats=[
        (at(3,0.00), 1.30, "count",  "stat", "1934"),
        (at(3,0.30), 1.40, "wipe",   "body", "Isolated from the clear jelly inside a cow's eye"),
        (at(3,0.75), 1.00, "arrive", "cite", "J Biol Chem · 1934"),
      ]),
 dict(id="s04-body", actor="ha-body", section="mechanism", layout="hero-left", bg=PAPER,
      start=S[4]["start"], end=S[5]["start"], beats=[
        (at(4,0.00), 1.40, "arrive", "head", "Your body already makes its own"),
        (at(4,0.30), 1.40, "wipe",   "body", "Most of it sits in your skin, holding water"),
        (at(4,0.50), 1.00, "arrive", "cite", "Dermatoendocrinol · 2012"),
        (at(4,0.66), 1.40, "wipe",   "body", "It also lubricates your joints and eye"),
        (at(4,0.86), 1.00, "arrive", "cite", "Front Vet Sci · 2019"),
      ]),
 dict(id="s05-compare", actor="ha-compare", section="mechanism", layout="split", bg=PAPER,
      start=S[5]["start"], end=S[6]["start"], beats=[
        (at(5,0.00), 1.50, "arrive", "head", "Here's where the two versions really split"),
        (at(5,0.22), 1.50, "wipe",   "body", "A serum's version stays mostly at the surface, supporting hydration"),
        (at(5,0.55), 1.00, "arrive", "cite", "Skin Res Technol · 2015"),
        (at(5,0.66), 1.60, "wipe",   "body", "A filler's version is cross-linked into a gel, placed beneath the skin"),
        (at(5,0.90), 1.00, "arrive", "cite", "J Cosmet Dermatol · 2024"),
      ]),
 dict(id="s06-serum-size", actor="ha-serum", section="mechanism", layout="two-column", bg=PAPER,
      start=S[6]["start"], end=S[7]["start"], beats=[
        (at(6,0.05), 1.50, "arrive", "head",   "In a serum, size decides almost everything"),
        (at(6,0.15), 1.00, "arrive", "kicker", "Simplified illustration"),
        (at(6,0.30), 1.60, "wipe",   "body",   "Large chains mostly stay near the surface, forming a hydrating film"),
        (at(6,0.58), 1.60, "wipe",   "body",   "Smaller ones may travel farther into the upper layers of skin"),
        (at(6,0.80), 1.00, "arrive", "cite",   "Skin Res Technol · 2015"),
        (at(6,0.92), 1.20, "slam",   "sub",    "Neither behaves like a filler"),
      ]),
 dict(id="s07-plumping", actor="ha-serum", section="mechanism", layout="two-column", bg=PAPER,
      start=S[7]["start"], end=S[8]["start"], beats=[
        (at(7,0.00), 1.30, "arrive", "head",    "So why does the bottle say plumping?"),
        (at(7,0.25), 1.50, "wipe",   "body",    "Hydrated surface cells can temporarily make fine lines appear softer"),
        (at(7,0.60), 1.30, "arrive", "caption", "Like watering a tired houseplant"),
        (at(7,0.85), 1.30, "swap",   "sub",     "Not like adding a new branch"),
      ]),
 dict(id="s08-binds-water", actor="ha-serum", section="proof", layout="hero-left", bg=MIST,
      start=S[8]["start"], end=S[9]["start"], beats=[
        (at(8,0.05), 1.50, "arrive", "head", "Here's the part the marketing skips"),
        (at(8,0.30), 1.60, "swap",   "head", "It binds water. It does not make water."),
        (at(8,0.55), 1.00, "arrive", "cite", "ChemRxiv · 2023"),
        (at(8,0.72), 1.60, "wipe",   "body", "A complete formula still needs something that stops it leaving"),
      ]),
 dict(id="s09-lifeguard", actor="ha-serum", section="proof", layout="hero-left", bg=MIST,
      start=S[9]["start"], end=S[10]["start"], beats=[
        (at(9,0.00), 1.40, "arrive", "caption", "Skip that step, and you're hiring a lifeguard for an empty swimming pool"),
        (at(9,0.60), 1.10, "slam",   "sub",     "Strange image. Correct principle."),
      ]),
 dict(id="s10-crosslink", actor="ha-filler", section="proof", layout="two-column", bg=INK,
      start=S[10]["start"], end=S[11]["start"], beats=[
        (at(10,0.00), 1.50, "arrive", "head", "A filler is chemically different"),
        (at(10,0.30), 1.80, "swap",   "body", "Cross-linked into a stable, connected grid"),
        (at(10,0.60), 1.00, "arrive", "cite", "J Cosmet Dermatol · 2024"),
        (at(10,0.78), 1.40, "wipe",   "sub",  "Holds its own shape, once placed beneath the skin"),
      ]),
 dict(id="s11-do-not-inject", actor="warning", section="application", layout="full-bleed", bg=INK,
      start=S[11]["start"], end=S[12]["start"], beats=[
        (at(11,0.00), 1.30, "arrive", "caption", "Is a filler just serum with a needle? Not even close."),
        (at(11,0.22), 1.20, "arrive", "kicker",  "Worth putting in very large letters"),
        (at(11,0.30), 1.00, "slam",   "head",    "DO NOT INJECT YOURSELF"),
        (at(11,0.42), 1.00, "arrive", "cite",    "FDA · Dermal Fillers"),
        (at(11,0.50), 1.60, "wipe",   "body",    "Dermal fillers are a medical procedure with real risks"),
        (at(11,0.68), 1.50, "wipe",   "body",    "Including tissue death, vision loss and stroke"),
        (at(11,0.86), 1.40, "wipe",   "sub",     "Choose a provider trained to perform the injection"),
      ]),
 dict(id="s12-badges", actor="lineup", section="recap", layout="three-lane", bg=PAPER,
      start=S[12]["start"], end=S[13]["start"], beats=[
        (at(12,0.00), 1.30, "arrive", "sub",  "Body version — resident"),
        (at(12,0.20), 1.30, "arrive", "sub",  "Serum version — moisturiser"),
        (at(12,0.38), 1.30, "arrive", "sub",  "Filler version — construction project"),
        (at(12,0.60), 1.50, "arrive", "head", "Same family"),
        (at(12,0.75), 1.60, "swap",   "head", "Different size, structure and location"),
      ]),
 dict(id="s13-endcard", actor="endcard", section="recap", layout="full-bleed", bg=PAPER,
      start=S[13]["start"], end=TOTAL, beats=[
        (at(13,0.00), 1.20, "arrive", "kicker", "One more thing — it started in a cow's eye"),
        (at(13,0.18), 1.80, "slam",   "head",   "Serum hydrates. Filler adds volume. Same name, different jobs."),
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

    # insert `hold` beats so no still window breaches the cap
    FIRST_STEP = 1.2
    filled, cursor = [], 0.0
    for k, b in enumerate(beats):
        step = FIRST_STEP if not filled else HOLD_STEP
        while b["offset"] - cursor > CAP - 1e-6:
            cursor = round(cursor + step, 3)
            step = HOLD_STEP
            if b["offset"] - cursor <= 0: break
            filled.append({"offset": cursor, "dur": min(0.9, round(dur - cursor, 3)),
                           "idiom": "hold", "role": "body", "actor": sc["actor"],
                           "intent": f"camera drift on {sc['actor']}"})
            cursor = round(cursor + 0.9, 3)
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

    DIAGRAM = {"s01-lineup", "s03-origin", "s04-body", "s05-compare",
               "s06-serum-size", "s08-binds-water", "s09-lifeguard",
               "s10-crosslink", "s11-do-not-inject", "s12-badges"}
    out_scenes.append({"id": sc["id"], "start": start, "duration": dur,
                       "section": sc["section"], "layout": sc["layout"],
                       "bg": sc["bg"],
                       "handoff": "hand-authored" if sc["id"] in DIAGRAM else "generated",
                       "beats": filled})

# One chapter per spine SECTION, not per scene: three scenes in a row
# (s02/s03, the compressed misconception+origin pair) run 7-8s apiece, well
# under youtube-delivery.md's >=10s chapter floor. Sections are the correct
# grain -- each already runs comfortably over it.
CHAPTER_TITLE = {
  "hook": "Three things, one name",
  "misconception": "Not filler in a bottle",
  "mechanism": "The version already in you",
  "proof": "It cannot make water",
  "application": "Do not inject yourself",
  "recap": "Same family, different jobs",
}
CHAPTERS = [{"t": s["start"], "title": CHAPTER_TITLE[s["name"]]} for s in SECTIONS]

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
 "end_scene": {"start": S[13]["start"],
               "duration": round(TOTAL - S[13]["start"],3),
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
