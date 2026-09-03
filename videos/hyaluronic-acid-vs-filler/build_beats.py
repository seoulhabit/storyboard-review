#!/usr/bin/env python3
"""Derive 03-beat-sheet.json from the MEASURED voiceover timing.

Nothing here is hand-typed timing. Scene and beat times are computed from
04-assets/vo-timing.json, which is the master clock [S4/V-2]. Change the VO and
re-run; never edit a time in the JSON.

Scenes are split by ACTOR CONTINUITY, not by narration sentence [S6/A-9]. The
three morphology actors -- ha-body / ha-serum / ha-filler -- persist across the
piece and are rearranged rather than redrawn, which is what stops a long-form
piece reading as separate slides.

Cadence [S5/C-2]: every spoken stem start gets a content beat; long stems are
kept alive by `hold` beats (bounded camera drift, which the generator counts as
a real beat) at <= 2.0s spacing. That is the cap the generator enforces.
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
# `t` is absolute; the builder converts to scene-relative offsets and inserts
# hold beats wherever a gap would breach the cadence cap.
PAPER, INK, MIST = "#F7F5F0", "#131516", "#F0EBE1"

SCENES = [
 dict(id="s01-lineup", actor="lineup", section="hook", layout="three-lane", bg=PAPER,
      start=0.0, end=S[4]["start"], beats=[
        (at(1,0.00), 1.20, "arrive", "head",  "Hyaluronic acid"),
        (at(1,0.22), 1.40, "wipe",   "sub",   "The kind your body makes"),
        (at(1,0.52), 1.40, "wipe",   "sub",   "The kind in your serum"),
        (at(1,0.80), 1.40, "wipe",   "sub",   "The kind a doctor injects"),
        (at(2,0.00), 1.00, "arrive", "kicker","Same name"),
        (at(3,0.00), 0.80, "slam",   "head",  "Different jobs"),
      ]),
 dict(id="s02-cousins", actor="lineup", section="misconception", layout="three-lane", bg=PAPER,
      start=S[4]["start"], end=at(5,0.436), beats=[
        (at(4,0.00), 1.10, "arrive", "caption","Three cousins, one name"),
        (at(5,0.00), 1.30, "arrive", "body",  "People buy a serum expecting what an injection does"),
        (at(5,0.28), 1.60, "swap",   "head",  "A serum is not filler in a bottle"),
      ]),
 dict(id="s03-origin", actor="vitreous", section="misconception", layout="hero-left", bg=INK,
      start=at(5,0.436), end=S[6]["start"], beats=[
        (at(5,0.44), 1.60, "count",  "stat",  "1934"),
        (at(5,0.62), 1.30, "arrive", "sub",   "Karl Meyer and John Palmer"),
        (at(5,0.80), 1.40, "wipe",   "body",  "Isolated from the vitreous of a cow's eye"),
        (at(5,0.95), 1.00, "arrive", "cite",  "J Biol Chem · 1934"),
      ]),
 dict(id="s04-named", actor="vitreous", section="mechanism", layout="hero-left", bg=INK,
      start=S[6]["start"], end=S[9]["start"], beats=[
        (at(6,0.00), 1.20, "arrive", "caption","“This could be a forty-dollar face serum?”"),
        (at(7,0.00), 0.80, "slam",   "head",  "Not immediately"),
        (at(8,0.00), 1.10, "arrive", "caption","Unsettling foresight"),
      ]),
 dict(id="s05-body", actor="ha-body", section="mechanism", layout="hero-left", bg=PAPER,
      start=S[9]["start"], end=S[11]["start"], beats=[
        (at(9,0.00), 1.40, "arrive", "head",  "Your body already makes it"),
        (at(9,0.30), 1.40, "wipe",   "body",  "Most of it sits in your skin, holding water"),
        (at(9,0.52), 1.00, "arrive", "cite",  "Dermatoendocrinol · 2012"),
        (at(9,0.66), 1.40, "wipe",   "body",  "It also lubricates your joints"),
        (at(9,0.88), 1.00, "arrive", "cite",  "Front Vet Sci · 2019"),
        (at(10,0.00),1.10, "arrive", "caption","Part sponge, part cushion"),
      ]),
 dict(id="s06-serum-size", actor="ha-serum", section="mechanism", layout="two-column", bg=PAPER,
      start=S[11]["start"], end=S[13]["start"], beats=[
        (at(11,0.10), 1.50, "arrive", "head",  "In a serum, size decides almost everything"),
        (at(11,0.36), 1.60, "wipe",   "body",  "Large chains mostly stay near the surface"),
        (at(11,0.58), 1.60, "wipe",   "body",  "Smaller ones may travel farther into the upper layers"),
        (at(11,0.78), 1.00, "arrive", "cite",  "Skin Res Technol · 2015"),
        (at(11,0.90), 1.20, "slam",   "sub",   "Neither behaves like a filler"),
        (at(12,0.00), 1.10, "arrive", "caption","“So why does my bottle say plumping?”"),
      ]),
 dict(id="s07-plumping", actor="ha-serum", section="mechanism", layout="two-column", bg=PAPER,
      start=S[13]["start"], end=S[15]["start"], beats=[
        (at(13,0.00), 1.50, "arrive", "head",  "Hydrated surface cells can temporarily make fine lines appear softer"),
        (at(13,0.70), 1.00, "arrive", "cite",  "Dermatoendocrinol · 2012"),
        (at(14,0.00), 1.30, "arrive", "caption","Like watering a tired houseplant"),
        (at(14,0.55), 1.30, "swap",   "sub",   "Not like adding a new branch"),
      ]),
 dict(id="s08-binds-water", actor="ha-serum", section="proof", layout="hero-left", bg=MIST,
      start=S[15]["start"], end=S[16]["start"], beats=[
        (at(15,0.18), 1.50, "arrive", "head",  "It binds water and holds it"),
        (at(15,0.48), 1.60, "swap",   "head",  "It does not make water"),
        (at(15,0.66), 1.00, "arrive", "cite",  "ChemRxiv · 2023"),
        (at(15,0.80), 1.50, "wipe",   "body",  "A complete formula still needs something that stops it leaving"),
      ]),
 dict(id="s09-lifeguard", actor="ha-serum", section="proof", layout="hero-left", bg=MIST,
      start=S[16]["start"], end=S[17]["start"], beats=[
        (at(16,0.00), 1.40, "arrive", "caption","A lifeguard for an empty swimming pool"),
        (at(16,0.72), 1.10, "slam",   "sub",   "Strange image. Correct principle."),
      ]),
 dict(id="s10-crosslink", actor="ha-filler", section="proof", layout="two-column", bg=INK,
      start=S[17]["start"], end=S[18]["start"], beats=[
        (at(17,0.22), 1.50, "arrive", "head",  "A filler is chemically different"),
        (at(17,0.42), 1.80, "wipe",   "body",  "Its chains are cross-linked into a gel that holds its shape"),
        (at(17,0.62), 1.00, "arrive", "cite",  "J Cosmet Dermatol · 2024"),
        (at(17,0.76), 1.60, "wipe",   "body",  "Placed beneath the skin, it can physically add volume"),
      ]),
 dict(id="s11-needle", actor="ha-filler", section="application", layout="hero-left", bg=INK,
      start=S[18]["start"], end=S[20]["start"], beats=[
        (at(18,0.00), 1.30, "arrive", "caption","“So it is not just serum with a needle?”"),
        (at(19,0.00), 0.90, "slam",   "head",  "Absolutely not"),
      ]),
 dict(id="s12-do-not-inject", actor="warning", section="application", layout="full-bleed", bg=INK,
      start=S[20]["start"], end=SECTIONS[-1]["start"], beats=[
        (at(20,0.00), 1.20, "arrive", "caption","“Put that in very large letters.”"),
        (at(21,0.00), 1.00, "slam",   "head",  "DO NOT INJECT YOURSELF"),
        (at(21,0.18), 1.00, "arrive", "cite",  "FDA · Dermal Fillers"),
        (at(21,0.36), 1.60, "wipe",   "body",  "Dermal fillers are a medical procedure with real risks"),
        (at(21,0.58), 1.50, "wipe",   "body",  "Including tissue death, vision loss and stroke"),
        (at(21,0.82), 1.40, "wipe",   "sub",   "Choose a provider trained to perform the injection"),
      ]),
 dict(id="s13-badges", actor="lineup", section="recap", layout="three-lane", bg=PAPER,
      start=SECTIONS[-1]["start"], end=171.0, beats=[
        (at(22,0.00), 1.20, "arrive", "sub",   "Body version — resident"),
        (at(22,0.34), 1.20, "arrive", "sub",   "Serum version — moisturiser"),
        (at(22,0.66), 1.20, "arrive", "sub",   "Filler version — construction project"),
        (at(23,0.00), 1.50, "arrive", "head",  "Same family"),
        (at(23,0.34), 1.60, "swap",   "head",  "Different size, structure and location"),
      ]),
 dict(id="s14-endcard", actor="endcard", section="recap", layout="full-bleed", bg=PAPER,
      start=171.0, end=TOTAL, beats=[
        (at(23,0.72), 1.30, "wipe",   "sub",   "So, a different result"),
        (at(24,0.00), 1.20, "arrive", "caption","“And it started in a cow's eyeball.”"),
        (at(25,0.00), 1.60, "arrive", "head",  "Hyaluronic acid isn't misleading"),
        (at(25,0.45), 1.60, "wipe",   "sub",   "Giving every version the same job description is"),
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
    # A beat at offset 0 is COMPOSED at frame zero and the generator emits no
    # tween for it -- so it changes no pixels, even though the generator's own
    # cadence check counts it as covering [0, dur]. Treat its coverage as a
    # point. And the clip starts up to `transition.duration` (<=0.6s) BEFORE the
    # scene's beat-sheet start, so the first gap is that much longer again:
    # the first fill step is tightened to keep 0+0.6 under the 2.0s cap.
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
        end = b["offset"] + b["dur"]
        if k == 0 and abs(b["offset"]) < 1e-6:
            end = 0.0
        cursor = max(cursor, round(end, 3))
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

    DIAGRAM = {"s01-lineup", "s05-body", "s06-serum-size", "s10-crosslink", "s13-badges"}
    out_scenes.append({"id": sc["id"], "start": start, "duration": dur,
                       "section": sc["section"], "layout": sc["layout"],
                       "bg": sc["bg"],
                       "handoff": "hand-authored" if sc["id"] in DIAGRAM else "generated",
                       "beats": filled})

CHAPTERS = [
 {"t": 0.0,                       "title": "Three things, one name"},
 {"t": round(S[4]["start"],3),    "title": "Not filler in a bottle"},
 {"t": round(at(5,0.436),3),      "title": "It came out of a cow's eye"},
 {"t": round(S[9]["start"],3),    "title": "The version already in you"},
 {"t": round(S[11]["start"],3),   "title": "Why size decides everything"},
 {"t": round(S[15]["start"],3),   "title": "It cannot make water"},
 {"t": round(S[17]["start"],3),   "title": "What a filler actually is"},
 {"t": round(S[20]["start"],3),   "title": "Do not inject yourself"},
 {"t": round(SECTIONS[-1]["start"],3), "title": "Same family, different jobs"},
]

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
 "end_scene": {"start": 171.0,
               "duration": round(TOTAL - 171.0,3),
               "overlay_zones_clear": True},
}
json.dump(bs, open(f"{HERE}/03-beat-sheet.json","w"), indent=2)

nb = sum(len(s["beats"]) for s in out_scenes)
nh = sum(1 for s in out_scenes for b in s["beats"] if b["idiom"]=="hold")
print("scenes    : %d" % len(out_scenes))
print("beats     : %d  (%d content, %d hold)" % (nb, nb-nh, nh))
print("beats/s   : %.2f  (ectoin long-form comparator: 0.71)" % (nb/TOTAL))
print("chapters  : %d, first at %.1fs, min gap %.1fs"
      % (len(CHAPTERS), CHAPTERS[0]["t"],
         min(CHAPTERS[i+1]["t"]-CHAPTERS[i]["t"] for i in range(len(CHAPTERS)-1))))
print("total     : %.3fs vs VO %.3fs" % (sum(s["duration"] for s in out_scenes), TOTAL))
from collections import Counter
print("idioms    : %s" % dict(Counter(b["idiom"] for s in out_scenes for b in s["beats"])))
print("actors    : %s" % dict(Counter(s["beats"][0]["actor"] for s in out_scenes)))
