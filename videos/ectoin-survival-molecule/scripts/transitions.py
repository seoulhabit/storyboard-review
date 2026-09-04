#!/usr/bin/env python3
"""The transition grammar. Five kinds, all clip-path wipes (never a translate,
never an opacity crossfade -- see this project's CLAUDE.md on why). Replaces
the old build_index.py transition_into(), which only knew two kinds (wipe-LEFT
"scene" and wipe-UP "chapter").

  d           wipe duration
  seam_after  gap from the outgoing scene's last word to the seam (the
              incoming scene's data-start / where the wipe begins)
  j           how much of the wipe's tail overlaps the next sentence --
              the incoming scene's first word sounds DURING the wipe's last
              `j` seconds, not after it finishes
  gap         seam_after + d - j: the narration-free span this boundary
              produces, by construction (never authored per-scene, never left
              to chance)

first_word_abs = seam + d - j   -- see scripts/timing.py, which is the only
other file allowed to import KIND directly for the actual walk.
"""

KIND = {
    #            d     seam_after   j     gap
    "continue": (0.40, 0.05,       0.20, 0.25),
    "carry":    (0.50, 0.05,       0.25, 0.30),
    "chapter":  (0.60, 0.10,       0.15, 0.55),
    "arrive":   (0.70, 0.15,       0.25, 0.60),
    "settle":   (0.80, 0.10,       0.30, 0.60),
}

# scene id -> kind of the transition INTO it. Anything not listed is "continue".
BOUNDARIES = {
    "17-preference": "carry",
    "21-verdict":    "carry",
    "24-eleven":     "carry",
    "08-humectant":  "chapter",
    "12-load":       "chapter",
    "16-trial104":   "chapter",
    "22-whofor":     "chapter",
    "26-kbeauty":    "chapter",
    "28-remember":   "arrive",
    "29-cta":        "settle",
}

# Incoming clip-path pair (hidden -> shown) and default ease per kind. Child
# travel during the wipe (the FLIP-carry, the chapter band, the ring rotation,
# etc.) is NOT here -- it lives in each scene's own timeline as an
# `arrival(kind)` snippet (scripts/build_frames.py), because it animates
# elements inside the INCOMING scene, which this module has no handle on.
CLIP_PATH = {
    "continue": ("inset(0% 0% 0% 100%)", "inset(0% 0% 0% 0%)", "power3.inOut"),
    "carry":    ("inset(0% 0% 0% 100%)", "inset(0% 0% 0% 0%)", "power3.inOut"),
    "chapter":  ("inset(100% 0% 0% 0%)", "inset(0% 0% 0% 0%)", "power3.inOut"),
    "arrive":   ("inset(50% 50% 50% 50%)", "inset(0% 0% 0% 0%)", "power4.inOut"),
    "settle":   ("inset(0% 0% 100% 0%)", "inset(0% 0% 0% 0%)", "power2.inOut"),
}


def kind_into(cid):
    """The transition kind entering scene `cid`. Scene 1 has none (returns
    None) -- there is nothing before it to wipe away from."""
    return BOUNDARIES.get(cid, "continue")


def plan(prev_cid, cid):
    """(kind, d, seam_after, j, gap, hidden, shown, ease) for the boundary
    prev_cid -> cid. `prev_cid` is accepted for symmetry with callers that
    already have it in hand; the kind depends only on the INCOMING scene."""
    kind = kind_into(cid)
    d, seam_after, j, gap = KIND[kind]
    hidden, shown, ease = CLIP_PATH[kind]
    return kind, d, seam_after, j, gap, hidden, shown, ease
