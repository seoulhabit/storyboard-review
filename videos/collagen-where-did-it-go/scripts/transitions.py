#!/usr/bin/env python3
"""The transition grammar: three visible kinds plus the invisible unit seam.

  d           wipe duration (0 for a phase seam inside one file)
  seam_after  gap from the outgoing unit's last word to the seam (= the
              incoming unit's start)
  j           how much of the wipe's tail the incoming unit's first word
              overlaps -- the word sounds DURING the wipe's last `j` seconds
  gap         seam_after + d - j: the narration-free span this boundary
              produces. gen_vo.py `cut` INSERTS exactly this much silence at
              every unit seam, and timing.walk() asserts the manifest agrees,
              so a change here without a re-cut fails loudly instead of
              drifting.

Grammar ([S6/A-8]: two-to-three kinds, never a plain crossfade):
  iris     PRIMARY. The incoming file is revealed by a circle expanding from
           the outgoing file's declared actor position (the molecule, the
           door, the film) -- "following the molecule / moving through a
           layer". Literal px so the overshoot is explicit.
  invert   SECONDARY, x2. Wipe UP into / out of the ink-ground evidence mode.
  curtain  CLOSING, x1. Slow wipe LEFT into the end card; reveals the empty
           right third (the end-screen reserve) first, so it is calm by
           construction.
  phase    a unit seam inside one composition file: no wipe, just the
           authored pause.

Nothing translates and opacity is never touched (BRIEF.md: a translating
push failed the hard safe-area gate on 99 frames on ectoin).
"""

KIND = {
    #            d     seam_after   j     gap
    "phase":   (0.00, 0.30,       0.00, 0.30),
    "iris":    (0.55, 0.05,       0.25, 0.35),
    "invert":  (0.60, 0.10,       0.15, 0.55),
    "curtain": (0.90, 0.20,       0.00, 1.10),   # no VO follows; gap is moot
}
for _k, (_d, _s, _j, _g) in KIND.items():
    assert abs(_s + _d - _j - _g) < 1e-9, f"KIND[{_k}] gap is not seam_after + d - j"

# unit cid -> kind of the transition INTO it. Unlisted units are "phase" seams
# inside their file. Unit 1 has no incoming transition.
BOUNDARIES = {
    "02-promise":   "iris",
    "03-building":  "iris",
    "06-door":      "iris",
    "08-digestion": "iris",
    "10-trials":    "invert",
    "14-hierarchy": "invert",
    "16-end":       "curtain",
}

# Incoming clip-path pair (hidden -> shown) and ease. Iris strings are
# formatted with the centre in canvas px by build_index.py.
#
# OVERSHOOT (ported from ectoin's measured note): every inset kind ends at
# -1%, past the frame edge, so the eased tail of the tween -- where velocity
# approaches zero -- spends its time OFF the visible frame rather than with a
# sliver of the outgoing ground sitting inside a reserved zone. For the circle,
# 2400px exceeds the farthest possible corner distance (sqrt(1920^2+1080^2) =
# 2203px) from any centre, so the reveal has fully covered the frame while
# still decelerating.
CLIP_PATH = {
    "iris":    ("circle(0px at {x}px {y}px)", "circle(2400px at {x}px {y}px)", "power2.inOut"),
    "invert":  ("inset(100% 0% 0% 0%)",       "inset(-1% -1% -1% -1%)",       "power3.inOut"),
    "curtain": ("inset(0% 0% 0% 100%)",       "inset(-1% -1% -1% -1%)",       "power2.inOut"),
}


def kind_into(cid):
    """Transition kind entering unit `cid`; "phase" for an in-file seam."""
    return BOUNDARIES.get(cid, "phase")


def gap_into(cid):
    """Narration-free seconds that precede unit `cid`'s first word."""
    return KIND[kind_into(cid)][3]


def is_file_boundary(cid):
    return kind_into(cid) != "phase"


def plan(cid, iris_at=None):
    """(kind, d, seam_after, j, gap, hidden, shown, ease) for the boundary
    INTO `cid`. `iris_at` = (x, y) canvas px, required for an iris."""
    kind = kind_into(cid)
    d, seam_after, j, gap = KIND[kind]
    if kind == "phase":
        return kind, d, seam_after, j, gap, None, None, None
    hidden, shown, ease = CLIP_PATH[kind]
    if kind == "iris":
        assert iris_at, f"{cid}: iris boundary needs an iris_at centre"
        x, y = int(round(iris_at[0])), int(round(iris_at[1]))
        hidden, shown = hidden.format(x=x, y=y), shown.format(x=x, y=y)
    return kind, d, seam_after, j, gap, hidden, shown, ease
