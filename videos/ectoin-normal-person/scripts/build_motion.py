#!/usr/bin/env python3
"""Generate index.motion.json -- declared motion intent, checked by `check`.

Sits between a source-level beat map and a full render: it is evaluated against
the SAME seeked timeline the renderer drives, so it catches an entrance that
never happens or a hold that goes dead, without paying for an MP4.

Four rules that are easy to get wrong, and are all deliberate here:

  1. ONE sidecar, at the PROJECT ROOT. `check` looks for it beside the root
     composition; one written next to a sub-composition is silently ignored and
     reports a false green.
  2. `keepsMoving` is scoped to #root, NEVER to a scene. Its static-window scan
     runs across the whole root duration and is not bounded to the window in
     which a scene is live, so a per-scene selector reports that scene's
     OFF-SCREEN time as frozen and fails by construction on tiling scenes.
  3. `maxStaticSec` comes from this format's cadence budget (long-form, 6.0s),
     not the 2s Shorts default.
  4. Assertions name COPY ELEMENTS, not their containers. A container can be
     present while the text inside it is overpainted or was never wrapped in an
     element at all -- which is exactly the defect class the engine's own
     text_occluded pass cannot see.

No flag is needed to run it: `check` discovers the file automatically.

SCHEMA, verified against hyperframes@0.8.22's own validator (src/utils/
motionSpec.ts in the bundled dist/cli.js) rather than from memory. It is FLAT
with an explicit `kind`, NOT the nested {"appearsBy": {...}} form:

    {"kind": "appearsBy",    "selector": "#x", "bySec": 12.3}
    {"kind": "before",       "a": "#x", "b": "#y"}
    {"kind": "staysInFrame", "selector": "#x"}
    {"kind": "keepsMoving",  "withinSelector": "#root", "maxStaticSec": 6.0}

The nested form parses as JSON and is rejected at check time with
`unknown assertion kind undefined` for every entry. DEFAULT_MAX_STATIC_SEC in
that same file is 2, confirming the Shorts-scale default this overrides.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from timing import walk


def _prefixed(cid, selector):
    """Rewrite a selector's leading #id to match _preamble._prefix_ids'
    output (c<cid>-<id>) -- the same central id-prefixing pass every scene
    file's own markup goes through. Only the id token is touched; a
    compound selector's tag/class tail ('#term p', '#k-a .say') is left
    alone, since only the id half was ever renamed."""
    return re.sub(r"^#([A-Za-z0-9_-]+)", rf"#c{cid}-\1", selector)

# (unit, phase, copy selector, human note). Selectors point at the <p>/<span>
# carrying the words, never at the card around them.
COPY = [
    ("01-bottle",    "a", "#ob-pc",        "eleven percent, extreme close-up, composed at t=0"),
    ("01-bottle",    "b", "#ob-inci",      "it's a blend -- the INCI list reveal"),
    ("01-bottle",    "c", "#ob-vd-t",      "THE VERDICT -- must appear inside the first 20s"),
    ("02-origin",    "a", "#nm",           "Halomonas elongata, extremely salty water"),
    ("02-origin",    "b", "#raisin",       "the raisin"),
    ("02-origin",    "c", "#sw2-b",       "marketing borrowed the drama"),
    ("04-protein",   "a", "#term p",       "the extremolyte gloss"),
    ("04-protein",   "d", "#sw-b",         "GIVE THE PROTEIN SPACE"),
    ("05-skin",      "a", "#k-a .say",     "keratin and water"),
    ("05-skin",      "d", "#vd span",      "support, not armour"),
    ("06-trial104",  "a", "#num",          "the 104 count-up"),
    ("07-preference","a", "#cl-t",         "THEY LIKED IT BETTER"),
    ("08-eczema",    "a", "#n65",          "the 65 count-up"),
    ("10-notprove",  "a", "#fu-a",          "the funding disclosure"),
    ("11-twelve",    "a", "#n12",          "the twelve count-up"),
    ("12-bottle",    "d", "#in-10",        "ectoin's real INCI position"),
    ("14-notnew",    "a", "#sl span",      "not the new hyaluronic acid"),
    ("15-whatitis",  "a", "#pay span",     "the payoff line -- WRAPPED, never a bare text node"),
    ("16-action",    "a", "#s1 span",      "the closing action, step 1"),
    ("18-endscreen", "a", "#e1 .say",      "the end-screen question"),
]


def main():
    units, total = walk()
    start = {cid: (st, {n: (s, l) for n, s, l in ph})
             for cid, st, own, ph, _t in units}

    asserts = []
    for cid, phase, sel, note in COPY:
        st, phases = start[cid]
        ps, pl = phases[phase]
        # Generous: the copy must be up by the END of its own phase. This
        # asserts the beat HAPPENED, not that it hit a particular frame.
        asserts.append({
            "kind": "appearsBy", "selector": _prefixed(cid, sel),
            "bySec": round(st + ps + pl, 2),
            "note": f"{cid}/{phase}: {note}",
        })

    # Reveal order across the evidence chapter: the study must be on screen
    # before its qualification, or the correction reads as a new claim.
    asserts.append({
        "kind": "before",
        "a": _prefixed("07-preference", "#cl-t"),
        "b": _prefixed("07-preference", "#cl-s"),
        "note": "07-preference: the claim lands before it is qualified",
    })
    asserts.append({
        "kind": "before",
        "a": _prefixed("06-trial104", "#num"),
        "b": _prefixed("08-eczema", "#n65"),
        "note": "the 104 study precedes the 65 study",
    })

    # ONE root-scoped hold check for the whole piece.
    asserts.append({
        "kind": "keepsMoving", "withinSelector": "#root", "maxStaticSec": 6.0,
        "note": "long-form cadence ceiling. Root-scoped on purpose: a per-scene "
                "selector reports a scene's off-screen time as frozen.",
    })

    spec = {
        "$comment": "Generated by scripts/build_motion.py -- do not hand-edit. "
                    "check discovers this automatically; there is no --motion flag.",
        "duration": total,
        "assertions": asserts,
    }
    (ROOT / "index.motion.json").write_text(json.dumps(spec, indent=2) + "\n")
    print(f"index.motion.json: {len(asserts)} assertions "
          f"({len(COPY)} appearsBy on copy elements, 2 before, 1 keepsMoving)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
