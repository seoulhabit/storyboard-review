#!/usr/bin/env python3
"""The motion registry: one entry per beat unit, authored alongside the unit's
timeline in build_frames.py and read by four generators so the storyboard,
the transitions, the motion sidecar and the cadence assert all agree.

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
        "treatments": ["path-follow race", "barrier impact", "cream/powder split", "kinetic slam"],
        "text": ["does NOT replace", "CREAM", "POWDER"],
        "iris_at": (960, 560),
        "copy": {"#hook-slam-last": ("we", "replace", 1, 0.40)},
    },
    "02-promise": {
        "treatments": ["kinetic question", "data column rise", "$ tag + drop", "shield teaser"],
        "text": ["Where does it actually go?", "23 trials", "$ = industry funded",
                 "what protects it?"],
        "iris_at": (500, 500),   # the molecule, parked where the building's shell will stand
        "copy": {"#promise-q-last": ("we", "go", 1, 0.60)},
    },
    "03-building": {
        "treatments": ["ground-up assembly", "beam draw-in", "camera settle"],
        "text": ["collagen = the beams"],
    },
    "04-demolition": {
        "treatments": ["sky warm", "ray draw", "beam cuts + shards fall", "camera push"],
        "text": ["UV cuts collagen", "works weekends"],
    },
    "05-boundary": {
        "treatments": ["camera pull-back", "shield draw", "ghost repair fails", "preserve pulse"],
        "text": ["preserve > replace"],
        "iris_at": (500, 653),
    },
    "06-door": {
        "treatments": ["scale cards + count-ups", "molecule grows vs the dot", "door hits", "rejected stamp"],
        "text": ["~500 daltons", "the size limit", "~300,000 daltons",
                 "one collagen molecule", "labelled, not to scale", "REJECTED"],
    },
    "07-film": {
        "treatments": ["film spreads", "surface smooth", "dermis push", "verdict wash"],
        "text": ["surface smoothing ≠ structural replacement"],
        "iris_at": (500, 584),
    },
    "08-digestion": {
        "treatments": ["scoop match cut", "tract path-follow", "fragmentation", "no-delivery void"],
        "text": ["peptides + amino acids", "no facial delivery"],
    },
    "09-dispatch": {
        "treatments": ["camera pan", "branch draw", "dot dispatch", "spare-parts crate"],
        "text": ["your body decides", "skin", "joints", "tendons", "other",
                 "scaffolding", "spare parts"],
    },
    "10-trials": {
        "treatments": ["ground inversion", "outcome bands", "result meter"],
        "text": ["hydration", "elasticity", "wrinkles", "BENEFIT"],
    },
    "11-caveat": {
        "treatments": ["head dim wash", "tag shrink", "industry recolour"],
        "text": ["small", "short", "industry funded"],
    },
    "12-filter": {
        "treatments": ["count-up 23 + pooled celadon", "tiles fall + meter moves", "camera lean", "STOPS flood"],
        "text": ["23", "randomised trials · pooled 2025", "keep only: independent",
                 "keep only: higher quality", "NOT SIGNIFICANT", "THE EFFECT", "STOPS SHOWING UP"],
        "copy": {"#ev-n": ("we", "three", 1, 0.60), "#stops-3-last": ("we", "up", 1, 0.50)},
    },
    "13-uncertain": {
        "treatments": ["question strikes", "flood retract", "meter settles"],
        "text": ["works?", "fails?", "UNCERTAIN"],
    },
    "14-hierarchy": {
        "treatments": ["building return", "rank sort", "foundation lock", "protein repairs beams"],
        "text": ["1 daily sunscreen", "2 not smoking", "3 protein + vitamin C",
                 "4 retinoids, if suitable"],
        "copy": {"#rank-1": ("we", "sunscreen", 1, 0.60)},
    },
    "15-verdict": {
        "treatments": ["optional pan", "final band", "bricks exit"],
        "text": ["optional", "collagen cream", "collagen powder",
                 "Protect the building first."],
    },
    "16-end": {
        "treatments": ["curtain", "calm drift"],
        "text": ["SeoulHabit · Evidence, not hype.", "sources in the description"],
    },
}
