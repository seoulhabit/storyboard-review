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
#
# SHOWN is a 1% OVERSHOOT past the frame edge on every side ("inset(-1% ...)"),
# not a bare 0%. All five kinds ease IN and OUT (power*.inOut/power4.inOut),
# meaning the wipe decelerates as it approaches its final state -- for
# "arrive" specifically, the safe-area margins (54px top of 1080, 96px left
# of 1920 -- both exactly 5% of their axis, i.e. 10% of the CENTER-OUT
# reveal's half-dimension) sit at the SAME fractional progress on all four
# edges at once, so the decelerating tail spends real, measurable time with
# the reveal's edge sitting inside the reserved zone before fully covering
# it -- caught by the hard safe-area gate at up to 178030px across both the
# top and bottom zones simultaneously in one sampled frame at the 27->28
# boundary. Overshooting the target by 1% means the reveal has already
# passed fully beyond the visible frame while still decelerating, so no
# sliver of the outgoing scene's ground is ever visible in that tail. A 1%
# overshoot is invisible by construction (clipped by the viewport) on every
# kind, including the ones that were never observed to fail.
#   MEASURED (this project's own render, 28-remember arrive, before this fix):
#   the bottom edge sits at y=854 (a static scene27 element, not the wipe)
#   until t=seam+0.376s, THEN the wipe's bottom edge sweeps 854->1079 in
#   ~90ms -- but crosses into the reserved bottom band (y>=972, the last
#   108px of that sweep) at t=seam+0.40s and does not clear it until
#   t=seam+0.55s: 150ms of real dwell time inside the reserved zone, on a
#   0.70s-total tween, because power4.inOut's velocity approaches ZERO at
#   its own endpoint and 0%/0% (fully-hidden -> fully-shown-with-no-margin)
#   put that endpoint EXACTLY where the margin-crossing had to happen. A 1%
#   overshoot barely moved the crossing point (recomputed: eased_frac 50/51
#   -> 50/51.5, indistinguishable) and the gate still failed, worse than
#   before (up to 166860px, and newly on left/right too, since "arrive" is
#   symmetric on all four sides and the crossing is coincidentally the same
#   fractional progress on every axis -- see the top-of-file note above).
#   FIX: "arrive" overshoots to -50%, matching the +50% starting inset, so
#   the tween covers -50%..+50%. The point where it crosses 0% (fully
#   covering every reserved margin) now falls at eased_frac 50/(50+50) =
#   0.5 -- for a symmetric inOut ease that is the SINGLE FASTEST-MOVING
#   instant of the whole tween, as far from the zero-velocity endpoints as
#   this shape can put it. The slow start (revealing nothing yet) and the
#   slow end (already fully covering, including overshoot) both now sit
#   OFF the visible frame. Re-verify by extracting frames, not by trusting
#   the arithmetic alone -- this is exactly the class of error that
#   produced this bug in the first place.
CLIP_PATH = {
    "continue": ("inset(0% 0% 0% 100%)", "inset(-1% -1% -1% -1%)", "power3.inOut"),
    "carry":    ("inset(0% 0% 0% 100%)", "inset(-1% -1% -1% -1%)", "power3.inOut"),
    "chapter":  ("inset(100% 0% 0% 0%)", "inset(-1% -1% -1% -1%)", "power3.inOut"),
    "arrive":   ("inset(50% 50% 50% 50%)", "inset(-50% -50% -50% -50%)", "power4.inOut"),
    "settle":   ("inset(0% 0% 100% 0%)", "inset(-1% -1% -1% -1%)", "power2.inOut"),
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
