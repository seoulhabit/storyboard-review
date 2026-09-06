#!/usr/bin/env python3
"""The motion registry: one entry per beat unit, authored alongside the unit's
timeline in build_frames.py and read by four generators so the storyboard,
the transitions, the motion sidecar and the cadence assert all agree.

2026-09-05 editorial redesign: 13 spoken units (was 16), one persistent
horizontal skin cross-section actor (drawBarrier in actors.py) replacing both
the standalone building and the old vertical barrier -- reused in 02-mesh,
04-barrier and 12-recs, camera-reframed each time rather than redrawn
(iris_at anchors the handoff between files exactly as it always has).

  treatments  2-4 named motion ideas (STORYBOARD.md)
  text        every on-screen text beat this unit introduces (each <= 10 words,
              asserted by build_frames.py) -- the muted-viewer contract
  iris_at     (x, y) canvas px of the actor the NEXT iris transition expands
              from; required only when the unit closes a file whose outgoing
              transition is an iris
  copy        motion-sidecar anchors: selector -> (fn, word, occurrence, slack)
              -> `appearsBy` at ctx.<fn>_abs(word, occ) + slack
  beats       panel-scale / camera beats the cadence checker can SEE, each
              {"name", "at" (file-relative s, filled by build_frames), "area"
              (fraction of frame), "dl" (luma delta), "dur" (s)}. A beat
              registers when area * dl / (dur * 8) >= 1.0 (beat_budget.py).
              build_frames.py asserts no two consecutive registering beats
              are more than 4.0s apart inside a spoken unit.
"""

MOTION = {
    "01-hook": {
        "treatments": ["path-follow split", "real-skin photo ground", "cream/powder divergence", "kinetic question"],
        "text": ["CREAM", "POWDER", "Where does it actually go?"],
        "iris_at": (960, 560),
        "copy": {"#hook-q-last": ("we", "go", 1, 0.40)},
    },
    "02-mesh": {
        "treatments": ["mesh draw-in", "camera settle"],
        "text": ["a support mesh"],
    },
    "03-uv": {
        "treatments": ["sun rises", "fibre snap", "age dim"],
        "text": ["age slows renewal", "UV breaks it down"],
        "iris_at": (900, 500),
    },
    "04-barrier": {
        "treatments": ["molecule descends", "size-compare count-ups", "barrier stop"],
        "text": ["~500 daltons", "~300,000 daltons", "doesn't get through"],
    },
    "05-film": {
        "treatments": ["film spreads", "verdict wash"],
        "text": ["Moisturizes the surface.", "Does not replace collagen below."],
        "iris_at": (420, 600),
    },
    "06-swallow": {
        "treatments": ["scoop match cut", "tract path-follow", "fragmentation"],
        "text": ["peptides + amino acids"],
    },
    "07-dispatch": {
        "treatments": ["branch draw", "dot dispatch", "no-delivery void"],
        "text": ["skin", "joints", "tendons", "No guaranteed delivery to your face."],
    },
    "08-trials": {
        "treatments": ["ground inversion", "outcome bands", "result meter grows"],
        "text": ["hydration", "elasticity"],
        "copy": {"#ev-n": ("we", "twenty", 1, 0.60)},
    },
    "09-caveat": {
        "treatments": ["tag shrink", "industry recolour"],
        "text": ["small", "short", "industry funded"],
    },
    "10-filter": {
        "treatments": ["tiles fall + meter moves", "STOPS flood", "camera settle"],
        "text": ["NOT SIGNIFICANT", "THE EFFECT", "STOPS SHOWING UP"],
        "copy": {"#stops-3-last": ("we", "up", 1, 0.50)},
    },
    "11-uncertain": {
        "treatments": ["question strikes", "flood retract", "meter settles"],
        "text": ["works?", "fails?", "UNCERTAIN"],
    },
    "12-recs": {
        "treatments": ["shield draws", "mesh repairs", "camera lean"],
        "text": ["sunscreen = shield", "protein + vitamin C", "retinoids act inside skin"],
        "copy": {"#shield": ("we", "sunscreen", 1, 0.60)},
    },
    "13-verdict": {
        "treatments": ["film reappears", "optional note", "final band"],
        "text": ["cream = surface", "powder = optional",
                 "Cream can moisturize. Powder is optional. Protect first."],
    },
    "14-end": {
        "treatments": ["curtain", "calm drift"],
        "text": ["SeoulHabit · Evidence, not hype.", "Sources in the description."],
    },
}
