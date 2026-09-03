#!/usr/bin/env python3
"""Generate a HyperFrames project from 03-beat-sheet.json.

Usage:
    python3 beats_to_composition.py 03-beat-sheet.json <project-dir> [--force]

The beat sheet is the single source of timing. This script emits, from it:

  <project>/index.html                      root composition (scene .clip elements)
  <project>/compositions/frames/NN-<id>.html one sub-composition per scene
  <project>/index.motion.json               motion-intent sidecar for `hyperframes check`

Nothing here is hand-typed timing. Editing a time in the HTML and not in the
beat sheet is the defect this script exists to prevent: re-run it instead.

Engine contract transcribed from the pinned CLI's own shipped docs
(node_modules/hyperframes/dist/...), not from memory:

  #root carries data-composition-id / data-start / data-duration /
        data-width / data-height              docs/compositions.md,
                                              docs/data-attributes.md §Composition,
                                              templates/blank/index.html
  timed elements carry class="clip" + data-start + data-duration
                                              docs/data-attributes.md §Timing,
                                              templates/_shared/AGENTS.md rules 1-2
  data-track-index is a Studio display lane the render never reads
                                              docs/data-attributes.md L9
  sub-compositions mount via a RELATIVE data-composition-src
                                              docs/compositions.md §Nested,
                                              templates/_shared/AGENTS.md rule 5
  timelines are gsap.timeline({paused:true}) registered on
        window.__timelines[<composition-id>]  docs/gsap.md,
                                              templates/_shared/AGENTS.md rule 3
  supported tween methods: set / to / from / fromTo
                                              docs/gsap.md §Key Rules
  no Date.now / Math.random / network fetches  templates/_shared/AGENTS.md rule 6

Cadence enforcement ([S5/C-2]): a scene whose beats leave a still window longer
than the format's cadence cap is a generation ERROR, not a warning. `check`'s
own `motion_frozen` / `sweep_static` would catch it later; catching it here
costs no render.

--------------------------------------------------------------------------
v2.2 — continuity: transitions, idioms, actors
--------------------------------------------------------------------------
Cadence is a floor, not a pass. A piece can measure clean on active-frame
share and still read as a slide deck, because what is missing is CONTINUITY:
a transition system, a camera, persistent actors, and an entrance vocabulary.
Three beat-sheet fields and one derived quantity close that gap.

  scene.transition  {type, direction?, duration?}   [S6/A-8]
        The ENTERING transition (registry convention: a scene names what
        brings it ON). type is one of cut / wipe-left / wipe-up /
        push-slide / blur-crossfade / zoom-through / squeeze / crossfade.
        Omit it and the generator derives one: `short` -> cut everywhere;
        `long` -> wipe-left inside a section and wipe-up at a section
        start, so transition strength
        serves the re-hook. A plain `crossfade` across a ground change is a
        generation ERROR (its midpoint is a muddy blend of two grounds);
        `blur-crossfade` is the sanctioned soft option and its midpoint is
        still extracted. More than 3 distinct non-cut types warns; a `short`
        with any non-cut transition warns. Exit animations are never emitted
        — the transition IS the exit.

  scene.handoff     generated | hand-authored       [S6/A-9]
        `hand-authored` keeps the generator's hands off that scene file (a
        multi-scene merge with persistent actors, a camera leg) while it still
        owns the clip, the transition and the assertions. The hand-authored
        file must honour the id contract `#<scene-id>-b<N>` / `#<scene-id>-stage`.

  beat.idiom        arrive|slam|wipe|count|swap|hold  [S6/A-10]
        Motion by narrative function. `arrive` is the old fade-and-rise, now
        one option of six rather than the house entrance. `slam` is
        kinetic-beat-slam; `wipe` a clip-path reveal with opacity untouched;
        `count` counting-dynamic-scale (proxy + deterministic onUpdate
        formatter, the asr-keyword-glow pattern — no Date.now / Math.random /
        rAF); `swap` scale-swap-transition (transform, don't replace); `hold`
        a multi-phase-camera micro-drift on the stage that emits NO element,
        which is how a deliberate hold is sanctioned by cadence instead of
        padded. `easing`, when present, still overrides the idiom's ease.
        The run prints the top signature's share; over 50% is warned.

  beat.actor        a shared id                      [S6/A-9]
        The same on-screen actor across beats and scenes. An actor in two
        CONSECUTIVE scenes as separate beats warns: that is a diagram being
        redrawn rather than rearranged. Merge the scenes and hand-author.

DERIVED OVERLAP — the beat sheet never contains one.
        Authored scene times still TILE exactly: no gap, no overlap. From
        scene i's own transition the generator derives d_in (its entering
        transition's duration, 0 for a cut and for scene 0) and d_out (which
        is simply scene i+1's d_in). Then, exactly as the injector in
        TRANSITION-REGISTRY.md §"How the injector applies a transition" does:
          clip data-start     = start - d_in        (pull the incoming back)
          clip data-duration  = duration + d_in + d_out
                                                     (extend the outgoing; it
                                                      holds its final frame)
          data-track-index    = i % 2                (ping-pong; DOM order is
                                                      what actually composites)
          root timeline       = registry gsap_template stamped at
                                T = start - d_in, the overlap start
        Inside the sub-composition every beat offset shifts by +d_in and the
        sub-comp's own duration becomes dur + d_in + d_out. Absolute assertion
        times are unchanged by construction, because
        (start - d_in) + (off + d_in) == start + off. Sub-composition
        timelines stay independently driven by the runtime: no double seek.
        One retime of the beat sheet re-derives all of it.

NO TIMELINE `defaults: { ease }`, anywhere. An inherited ease is an UNCOUNTED
ease — the mechanism by which a video reaches 65% of its real tweens sharing
one entrance signature while every explicit-`ease:` grep says otherwise. Every
tween the generator emits, including the duration anchors, names its own.

MOTION SIDECAR — three things MEASURED on hyperframes 0.8.22, 2026-09-02, on
the proof/v2.2-continuity-3scene project. Do not re-derive them from the docs;
the docs do not say any of this.

  1. `keepsMoving.withinSelector` RESOLVES for both `#scene-<cid>` (the root's
     clip wrapper) and `#<cid>-stage` (the mounted sub-composition's own
     stage). Neither produces `motion_selector_missing`, so `check` does see
     the mounted sub-composition's children through the root clip wrapper.
     BUT NEITHER IS USABLE PER SCENE: the static-window scan runs over the
     WHOLE root composition duration and is never bounded to the window in
     which that scene's clip is live, so a per-scene assertion reports the
     scene's own off-screen time as a frozen window and fails by construction:
       #scene-s02 "nothing moves ... between 0s and 2.5s (2.5s static)"
       #scene-s01 "nothing moves ... between 3.5s and 9s (5.5s static)"
       #scene-s03 "nothing moves ... between 0s and 5.65s"
     (identical findings with `#s01-stage` / `#s02-stage` / `#s03-stage`.)
     So the generator emits ONE composition-wide `keepsMoving` on `#root` at
     the format's cadence cap. On tiling scenes that has the same coverage for
     a frozen scene and additionally covers the boundaries. See build_sidecar.
  2. A per-sub-composition sidecar (`compositions/frames/01-s01.motion.json`)
     is NOT discovered: `check`'s reported `specPath` stays the root
     `index.motion.json` and `samples` stays the root's. Writing one is a
     silent no-op — the worst kind of green. The generator does not write one.
  3. `staysInFrame` is INCOMPATIBLE with a transition. A transition translates
     or scales the whole scene wrapper, so every element inside it genuinely
     leaves the canvas during the overlap; the assertion fires
     `motion_off_frame` by design ("#s01-b2 drifts off the 1080x1920 canvas at
     2.7s" under a push-slide LEFT). It is emitted only on a scene that no
     transition touches — which now includes the plate's own `staysInFrame`.

A `wipe` beat gets `appearsBy` but never `before`: it never changes opacity, so
`appearsBy` proves only that the copy element exists and is not hidden (still
worth naming — a typo'd id fires motion_selector_missing), while
`before(prev, wipe)` would actively FAIL, an opacity-1 element "first
appearing" at frame zero. The clip-path reveal itself is outside all four
assertion kinds' vocabulary; the transition-midpoint frame extraction is what
verifies it.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

# [S5/C-2] cadence caps, seconds of permitted stillness. Long-form tolerates a
# longer hold than a Short; both sit at or under `check`'s own maxStaticSec
# default of 2s for keepsMoving, so a pass here implies a pass there.
CADENCE_CAP = {"long": 2.0, "short": 1.5}

DEFAULT_BEAT_DUR = 0.45

# GSAP eases, keyed by the beat sheet's `easing` vocabulary.
EASE = {
    "arrive": "power3.out",
    "camera": "power1.inOut",
    "linear": "none",
    "snap": "power4.out",
}
DEFAULT_EASE = "arrive"

# --------------------------------------------------------------------------
# [S6/A-10] motion idiom by narrative function. `arrive` is the fade-and-rise
# the generator used to emit for every entering beat; it is now ONE option of
# six, and its dominance is a measurable template failure, not a house style.
# Each idiom names its own ease — the timeline no longer carries a
# `defaults: { ease }`, so an unnamed ease would silently be GSAP's own.
# --------------------------------------------------------------------------
IDIOM_EASE = {
    "arrive": "power3.out",   # (unchanged) rules: none — the generic entrance
    "slam": "power4.out",     # rules/kinetic-beat-slam.md
    "wipe": "power2.inOut",   # a clip-path reveal; opacity untouched
    "count": "power2.out",    # rules/counting-dynamic-scale.md
    "swap": "back.out(1.6)",  # rules/scale-swap-transition.md (incoming only)
    "hold": "sine.inOut",     # rules/multi-phase-camera.md micro-drift
}
DEFAULT_IDIOM = "arrive"

# `^(\D*)(\d[\d,.]*)(\D*)$` — a `count` beat's text must contain exactly one
# number, with optional prefix and suffix copy around it.
COUNT_RE = re.compile(r"^(\D*)(\d[\d,.]*)(\D*)$")

# --------------------------------------------------------------------------
# [S6/A-8] transition registry. The `gsap_template` lines and the
# `default_duration_s` values below are transcribed VERBATIM from
# ~/.claude/skills/hyperframes-animation/transitions/TRANSITION-REGISTRY.md
# (§Registry). The generator substitutes only the placeholders that file
# documents in §"Template placeholders"; it never invents a transition tween.
#
# Mechanics, also from that file (§"How the injector applies a transition"):
#   1. outgoing clip data-duration extended by d (it holds its final frame)
#   2. incoming clip data-start pulled earlier by d (this IS the overlap)
#   3. data-track-index ping-pongs 0/1 so the two overlapping wrappers never
#      share a track (a readability convention; DOM order does the compositing)
#   4. the template is stamped on window.__timelines['main'] at T = overlap start
# Sub-composition timelines stay independently driven — no double seek.
# EXIT ANIMATIONS ARE NEVER EMITTED: the transition IS the exit.
# --------------------------------------------------------------------------
TRANSITION_MIN_S = 0.15
TRANSITION_MAX_S = 2.0   # registry `max_duration_s`

TRANSITIONS = {
    "cut": {"default_duration": 0.0, "template": []},
    "crossfade": {
        "default_duration": 0.5,
        "template": [
            'tl.to(__OLD__, { opacity: 0, duration: __DUR__, ease: "power2.inOut" }, __T__);',
            'tl.fromTo(__NEW__, { opacity: 0 }, { opacity: 1, duration: __DUR__, ease: "power2.inOut" }, __T__);',
        ],
    },
    "blur-crossfade": {
        "default_duration": 0.6,
        "template": [
            'tl.to(__OLD__, { filter: "blur(10px)", scale: 1.03, opacity: 0, duration: __DUR__, ease: "power2.inOut" }, __T__);',
            'tl.fromTo(__NEW__, { filter: "blur(10px)", scale: 0.97, opacity: 0 }, { filter: "blur(0px)", scale: 1, opacity: 1, duration: __DUR__, ease: "power2.inOut" }, __T__);',
        ],
    },
    "push-slide": {
        "default_duration": 0.5,
        "default_direction": "LEFT",
        "template_horizontal": [
            'tl.to(__OLD__, { x: __DX__, duration: __DUR__, ease: "power3.inOut" }, __T__);',
            'tl.fromTo(__NEW__, { x: __DXIN__, opacity: 1 }, { x: 0, duration: __DUR__, ease: "power3.inOut" }, __T__);',
        ],
        "template_vertical": [
            'tl.to(__OLD__, { y: __DY__, duration: __DUR__, ease: "power3.inOut" }, __T__);',
            'tl.fromTo(__NEW__, { y: __DYIN__, opacity: 1 }, { y: 0, duration: __DUR__, ease: "power3.inOut" }, __T__);',
        ],
    },
    "zoom-through": {
        "default_duration": 0.4,
        "template": [
            'tl.to(__OLD__, { scale: 2.5, opacity: 0, filter: "blur(8px)", duration: __DUR__, ease: "power3.in" }, __T__);',
            'tl.fromTo(__NEW__, { scale: 0.5, opacity: 0, filter: "blur(8px)" }, { scale: 1, opacity: 1, filter: "blur(0px)", duration: __DUR__, ease: "power3.out" }, __T__);',
        ],
    },
    "squeeze": {
        "default_duration": 0.4,
        "template": [
            'tl.to(__OLD__, { scaleX: 0, transformOrigin: "left center", duration: __DUR__, ease: "power3.inOut" }, __T__);',
            'tl.fromTo(__NEW__, { scaleX: 0, transformOrigin: "right center", opacity: 1 }, { scaleX: 1, transformOrigin: "right center", duration: __DUR__, ease: "power3.inOut" }, __T__);',
        ],
    },
    # The two long-form defaults. NOT in the engine's Tier-B registry: those five
    # all translate or scale a wrapper, and a translating transition drags scene
    # content through the reserved safe-area zones. Measured on a 29-scene
    # 1920x1080 piece, push-slide vs a wipe, same composition, one render each:
    # push failed the hard safe-area gate on 99 frames (real text, up to 6.2%
    # edge density in the top band) against a hard-cut baseline that passed all
    # 1361; the wipe measured 0. Both render correctly and both pass `check`, so
    # nothing before the safe-area scan tells them apart [S6/A-8].
    #
    # A wipe only CLIPS: the incoming scene sits at its own resting position and
    # is progressively revealed, so it cannot put content anywhere a settled
    # frame does not already have it. Only the incoming wrapper is touched --
    # the outgoing needs no tween at all, because later scenes paint above
    # earlier ones and the extended clip simply holds its final frame beneath.
    #
    # Unsafe over a RASTER inside the wiped region (the drawElement capture bug
    # in /hyperframes-cli); validate_transitions() warns when a scene carries a
    # plate and a wipe at once.
    "wipe-left": {
        "default_duration": 0.45,
        "template": [
            'tl.fromTo(__NEW__, { clipPath: "inset(0% 0% 0% 100%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: __DUR__, ease: "power3.inOut" }, __T__);',
        ],
    },
    "wipe-up": {
        "default_duration": 0.60,
        "template": [
            'tl.fromTo(__NEW__, { clipPath: "inset(100% 0% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: __DUR__, ease: "power3.inOut" }, __T__);',
        ],
    },
}
TRANSITION_TYPES = sorted(TRANSITIONS)

ROLE_CLASS = {
    "kicker": "kicker",
    "head": "head",
    "sub": "sub",
    "body": "body",
    "caption": "caption",
    "stat": "stat",
    # A disclosure that an on-screen claim has no source record in the project's
    # tracking system. Deliberately NOT the accent colour: a flag that borrows
    # the accent reads as a citation. See catalog/visual-components/unsourced-flag.
    "flag": "flag",
    # [K-2] the citation chip a SOURCED claim renders with. Human-readable only
    # -- "PMID 35328954", "21 CFR 333.350", "Arch Dermatol - 1995" -- never an
    # internal record id. Deliberately accent-toned so it cannot be mistaken for
    # the muted flag, and vice versa.
    "cite": "cite",
}


WARNINGS: list = []


def die(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def warn(msg: str) -> None:
    """A warning is a ledger line, not a shrug: every one is re-printed in the
    run summary so it lands in the delivery record rather than scrolling away."""
    WARNINGS.append(msg)
    print(f"WARNING: {msg}", file=sys.stderr)


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "-", str(s).lower()).strip("-") or "scene"


def esc(s) -> str:
    return html.escape(str(s), quote=True)


def f(x) -> str:
    """Fixed 3dp — the same string lands in the HTML and in the sidecar."""
    return f"{float(x):.3f}"


# --------------------------------------------------------------------------
# [S6/A-8] transitions: resolution and emission
# --------------------------------------------------------------------------
def resolve_transitions(bs: dict, scenes: list) -> list:
    """One resolved {type, direction, duration} per scene — the ENTERING
    transition, registry convention. Index 0 is always a cut.

    Derived when the scene omits `transition`:
      short -> cut everywhere (cuts on the timing grid are the Shorts default)
      long  -> wipe-left inside a section; wipe-up at a section
               start, where the accent serves the re-hook.
    """
    fmt = bs["format"]
    out = []
    prev_section = None
    for i, sc in enumerate(scenes):
        section = sc.get("section")
        t = sc.get("transition")
        if i == 0:
            if t and t.get("type", "cut") != "cut":
                die(
                    f"scene {sc['id']!r} is the first scene and carries "
                    f"transition {t.get('type')!r} — there is nothing to transition "
                    f"FROM. The first scene's transition must be absent or 'cut'."
                )
            t = {"type": "cut"}
        elif t is None:
            if fmt == "short":
                t = {"type": "cut"}
            elif prev_section is not None and section != prev_section:
                t = {"type": "wipe-up"}
            else:
                t = {"type": "wipe-left"}
        kind = t.get("type", "cut")
        if kind not in TRANSITIONS:
            die(
                f"scene {sc['id']!r} names transition type {kind!r}; the registry "
                f"has {TRANSITION_TYPES}. (No 'wipe', 'match-cut' or 'whip pan' "
                f"exists as a between-scene transition — TRANSITION-REGISTRY.md.)"
            )
        spec = TRANSITIONS[kind]
        dur = float(t.get("duration", spec["default_duration"]))
        direction = t.get("direction", spec.get("default_direction"))
        if kind == "cut":
            dur = 0.0
            direction = None
        else:
            if not (TRANSITION_MIN_S - 1e-9 <= dur <= TRANSITION_MAX_S + 1e-9):
                die(
                    f"scene {sc['id']!r}: transition duration {dur}s is outside the "
                    f"registry's {TRANSITION_MIN_S}-{TRANSITION_MAX_S}s window "
                    f"(typical 0.3-0.6s)."
                )
            if dur > float(sc["duration"]) or (
                i > 0 and dur > float(scenes[i - 1]["duration"])
            ):
                die(
                    f"scene {sc['id']!r}: a {dur}s overlap does not fit between a "
                    f"{scenes[i - 1]['duration']}s scene and a {sc['duration']}s one."
                )
        if kind != "push-slide" and t.get("direction"):
            warn(
                f"scene {sc['id']!r}: `direction` is meaningful only on push-slide; "
                f"ignored for {kind!r}."
            )
            direction = None
        if kind == "push-slide" and direction not in ("LEFT", "RIGHT", "UP", "DOWN"):
            die(f"scene {sc['id']!r}: push-slide direction {direction!r} is not one of LEFT/RIGHT/UP/DOWN")
        # A wipe animates a clip over whatever the incoming scene draws. Over a
        # RASTER that is the drawElement capture bug: the region can render
        # frozen while the DOM reports correct geometry and `check` passes.
        # Browser-drawn scenes are unaffected, which is why this warns rather
        # than dies -- but verify the boundary on an extracted frame.
        if kind.startswith("wipe-") and sc.get("plate"):
            warn(
                f"scene {sc['id']!r}: {kind} reveals a scene carrying a plate "
                f"({sc['plate']}). An animated clip over a raster can capture "
                f"frozen on the drawElement path — extract this boundary's "
                f"midpoint from the render before trusting it, or use `cut` here."
            )
        # A translating transition drags scene content through the reserved
        # safe-area zones; a wipe cannot. Measured: 99 flagged frames vs 0 on
        # the same 29-scene composition [S6/A-8]. Allowed, because a piece whose
        # settled frames leave the zones clear by a wide margin can afford it --
        # but it has to be a choice, and [S7/R-2]'s safe-area gate has to run.
        if kind in ("push-slide", "zoom-through", "squeeze"):
            warn(
                f"scene {sc['id']!r}: {kind!r} translates or scales whole scene "
                f"wrappers, which moves content through the reserved zones. The "
                f"safe-area gate will judge it — prefer wipe-left/wipe-up unless "
                f"you have a reason and have run [S7/R-2] on a real render."
            )
        out.append({"type": kind, "direction": direction, "duration": dur})
        prev_section = section
    return out


def transition_js(kind: str, direction, dur: float, old_sel: str, new_sel: str,
                  t0: float, w: int, h: int) -> list:
    """Substitute the registry's documented placeholders into its own template.
    __DX__/__DY__ are where the OUTGOING travels; __DXIN__/__DYIN__ are the
    side the INCOMING comes from — the opposite sign, one canvas away."""
    spec = TRANSITIONS[kind]
    if kind == "push-slide":
        lines = (spec["template_horizontal"] if direction in ("LEFT", "RIGHT")
                 else spec["template_vertical"])
    else:
        lines = spec["template"]
    dx = {"LEFT": -w, "RIGHT": w}.get(direction, 0)
    dy = {"UP": -h, "DOWN": h}.get(direction, 0)
    sub = {
        "__OLD__": f"'{old_sel}'",
        "__NEW__": f"'{new_sel}'",
        "__DUR__": f(dur),
        "__DXIN__": str(-dx),
        "__DYIN__": str(-dy),
        "__DX__": str(dx),
        "__DY__": str(dy),
        "__ORIGIN_OUT__": '"left center"',
        "__ORIGIN_IN__": '"right center"',
        "__T__": f(t0),
    }
    out = []
    for line in lines:
        for token, value in sub.items():
            line = line.replace(token, value)
        out.append("    " + line)
    return out


def overlap_windows(trans: list) -> tuple:
    """(d_in, d_out) per scene. d_out is simply the NEXT scene's d_in — the
    outgoing clip is extended by exactly the window its successor pulls back
    into. Both are DERIVED; the beat sheet's own times never overlap."""
    d_in = [float(t["duration"]) for t in trans]
    d_out = d_in[1:] + [0.0]
    return d_in, d_out


# --------------------------------------------------------------------------
# validation
# --------------------------------------------------------------------------
def validate(bs: dict) -> tuple:
    """Return (scenes, resolved transitions), or die with the first structural
    problem."""
    for key in ("slug", "format", "fps", "canvas", "vo_duration_s", "presenter", "scenes"):
        if key not in bs:
            die(f"beat sheet is missing required key {key!r}")
    if bs["format"] not in CADENCE_CAP:
        die(f"format must be one of {sorted(CADENCE_CAP)}, got {bs['format']!r}")
    scenes = bs["scenes"]
    if not scenes:
        die("beat sheet has no scenes")

    cap = CADENCE_CAP[bs["format"]]
    cursor = 0.0
    for i, sc in enumerate(scenes):
        for key in ("id", "start", "duration", "beats"):
            if key not in sc:
                die(f"scene {i} is missing required key {key!r}")
        start, dur = float(sc["start"]), float(sc["duration"])
        if dur <= 0:
            die(f"scene {sc['id']!r} has duration {dur}")
        if abs(start - cursor) > 1e-6:
            die(
                f"scene {sc['id']!r} starts at {start} but the previous scene ends at "
                f"{cursor} — scenes must tile the timeline with no gap and no overlap"
            )
        cursor = start + dur
        if not sc["beats"]:
            die(f"scene {sc['id']!r} has no beats")

        # [S5/C-2] cadence: no still window longer than the cap, measured from
        # scene start, between consecutive beat ends, and to scene end.
        handoff = sc.get("handoff", "generated")
        if handoff not in ("generated", "hand-authored"):
            die(f"scene {sc['id']!r}: handoff must be 'generated' or 'hand-authored', got {handoff!r}")

        marks = []
        for j, b in enumerate(sc["beats"]):
            if "offset" not in b:
                die(f"a beat in scene {sc['id']!r} is missing 'offset'")
            off = float(b["offset"])
            bdur = float(b.get("dur", DEFAULT_BEAT_DUR))
            if off < 0 or off + bdur > dur + 1e-6:
                die(
                    f"beat at offset {off} (dur {bdur}) in scene {sc['id']!r} "
                    f"falls outside the scene's own {dur}s window"
                )
            # [S6/A-10] idiom. A `hold` beat COUNTS as a beat for cadence below:
            # it is camera motion on the stage, which is how a deliberate
            # long-form hold gets sanctioned instead of padded with a crossfade.
            idiom = b.get("idiom", DEFAULT_IDIOM)
            if idiom not in IDIOM_EASE:
                die(
                    f"beat {j} in scene {sc['id']!r} names idiom {idiom!r}; the "
                    f"vocabulary is {sorted(IDIOM_EASE)}"
                )
            if idiom == "count":
                text = b.get("text", b.get("caption", b.get("intent", "")))
                if not COUNT_RE.match(str(text).strip()):
                    die(
                        f"beat {j} in scene {sc['id']!r} has idiom 'count' but its "
                        f"text {text!r} contains no single number to count to. "
                        f"counting-dynamic-scale needs one numeral, optionally "
                        f"wrapped in copy (\"104\", \"up 42%\", \"1,200 people\")."
                    )
            if idiom == "swap" and j == 0:
                die(
                    f"beat 0 in scene {sc['id']!r} has idiom 'swap' but there is no "
                    f"previous beat to swap OUT — scale-swap-transition transforms "
                    f"what is already on screen, it does not introduce."
                )
            marks.append((off, off + bdur))
        marks.sort()
        still_from = 0.0
        for off, end in marks:
            if off - still_from > cap + 1e-6:
                die(
                    f"[S5/C-2] scene {sc['id']!r}: {off - still_from:.2f}s of stillness "
                    f"before the beat at {off}s exceeds the {cap}s {bs['format']} cadence "
                    f"cap. Split the beat or add one — do not pad with a crossfade."
                )
            still_from = max(still_from, end)
        if dur - still_from > cap + 1e-6:
            die(
                f"[S5/C-2] scene {sc['id']!r}: the last beat ends at {still_from:.2f}s "
                f"leaving {dur - still_from:.2f}s of stillness before the scene ends at "
                f"{dur}s (cap {cap}s). This is the frozen-tail defect `check` reports as "
                f"motion_frozen / sweep_static."
            )

    total = cursor
    vo = float(bs["vo_duration_s"])
    if vo > 0 and abs(total - vo) > 0.15:
        die(
            f"scenes total {total:.3f}s but vo_duration_s is {vo:.3f}s — the voiceover's "
            f"measured duration is the master clock ([S4/V-2]); re-derive the beats."
        )

    # ---- [S6/A-8] transitions, resolved and gated -------------------------
    trans = resolve_transitions(bs, scenes)
    default_bg = bs.get("bg", "#101314")
    used = []
    for i, (sc, t) in enumerate(zip(scenes, trans)):
        if t["type"] == "cut":
            continue
        used.append(t["type"])
        if t["type"] == "crossfade":
            bg_now = sc.get("bg", default_bg)
            bg_prev = scenes[i - 1].get("bg", default_bg)
            if str(bg_now).strip().lower() != str(bg_prev).strip().lower():
                die(
                    f"[S6/A-8] scene {sc['id']!r} enters on a plain 'crossfade' but its "
                    f"ground {bg_now} differs from the previous scene's {bg_prev}. The "
                    f"midpoint of that crossfade is a muddy blend of two grounds — the "
                    f"one transition failure this project has already extracted and "
                    f"proven. Use 'blur-crossfade' (the blur masks the clash; extract "
                    f"its midpoint anyway [S7/R-2]) or a 'push-slide' (no frame ever "
                    f"blends two grounds)."
                )
    distinct = sorted(set(used))
    if len(distinct) > 3:
        warn(
            f"[S6/A-8] {len(distinct)} distinct non-cut transition types in one piece "
            f"({', '.join(distinct)}). Pick 2-3 and repeat them — repetition is what "
            f"reads as a system; four types read as a sampler."
        )
    if bs["format"] == "short" and used:
        warn(
            f"[S6/A-8] format is 'short' but {len(used)} scene(s) carry a non-cut "
            f"transition ({', '.join(distinct)}). Hard cuts on the timing grid are the "
            f"Shorts default; a transition spends frames a Short does not have."
        )

    # ---- [S6/A-9] actor continuity ----------------------------------------
    # An actor that appears in two CONSECUTIVE scenes as separate beats is a
    # diagram being REDRAWN rather than rearranged. The fix is a multi-scene
    # merge (hyperframes-core composition-patterns §C) declared as
    # `handoff: "hand-authored"`, which this generator will then not overwrite.
    prev_actors: set = set()
    for sc in scenes:
        actors = {str(b["actor"]) for b in sc["beats"] if b.get("actor")}
        shared = sorted(actors & prev_actors)
        if shared and sc.get("handoff", "generated") != "hand-authored":
            warn(
                f"[S6/A-9] actor(s) {', '.join(shared)} appear in scene {sc['id']!r} and "
                f"in the scene before it as separate beats — the actor is being redrawn, "
                f"not rearranged. Merge those scenes into one hand-authored multi-phase "
                f"sub-composition (`handoff: \"hand-authored\"`) so the same DOM nodes "
                f"move, or accept a rebuilt diagram at the boundary."
            )
        prev_actors = actors

    return scenes, trans


# --------------------------------------------------------------------------
# emission
# --------------------------------------------------------------------------
def scene_filename(idx: int, sid: str) -> str:
    return f"{idx + 1:02d}-{slugify(sid)}.html"


def render_root(bs: dict, scenes: list, trans: list) -> str:
    cv = bs["canvas"]
    w, h = int(cv["w"]), int(cv["h"])
    total = sum(float(s["duration"]) for s in scenes)
    resolution = "portrait" if h > w else "landscape"
    audio = bs.get("audio") or {}
    d_in, d_out = overlap_windows(trans)

    rows = []
    for i, sc in enumerate(scenes):
        cid = slugify(sc["id"])
        src = f"compositions/frames/{scene_filename(i, sc['id'])}"
        # [S6/A-8] the overlap is DERIVED here and nowhere else: the incoming
        # clip's start is pulled back by its own transition's d, the outgoing
        # clip's duration is extended by the NEXT one's d (it holds its final
        # frame through the window). The beat sheet's own times still tile.
        rows.append(
            f'    <div class="scene clip" id="scene-{esc(cid)}" data-composition-id="{esc(cid)}"\n'
            f'         data-composition-src="{esc(src)}"\n'
            f'         data-start="{f(float(sc["start"]) - d_in[i])}"'
            f' data-duration="{f(float(sc["duration"]) + d_in[i] + d_out[i])}"\n'
            f'         data-track-index="{i % 2}"></div>'
        )

    # The registry template, stamped on the ROOT timeline at T = overlap start.
    # Sub-composition timelines are driven independently by the runtime, so
    # there is no double seek. No exit animation is ever emitted: this IS it.
    trans_lines = []
    for i, t in enumerate(trans):
        if i == 0 or t["type"] == "cut":
            continue
        prev_cid = slugify(scenes[i - 1]["id"])
        cid = slugify(scenes[i]["id"])
        t0 = float(scenes[i]["start"]) - d_in[i]
        label = t["type"] + (f" {t['direction']}" if t["direction"] else "")
        trans_lines.append(
            f"    // {label} {f(d_in[i])}s: {prev_cid} -> {cid}, overlap opens at {f(t0)}s"
        )
        trans_lines.extend(
            transition_js(t["type"], t["direction"], d_in[i],
                          f"#scene-{prev_cid}", f"#scene-{cid}", t0, w, h)
        )
    trans_block = ("\n" + "\n".join(trans_lines) + "\n") if trans_lines else ""

    audio_row = ""
    if audio.get("src"):
        # data-volume only. A data-automation volume lane REPLACES data-volume on
        # this engine rather than scaling it, which is how a bed ships hot.
        audio_row = (
            f'\n    <audio id="bgm" src="{esc(audio["src"])}"\n'
            f'           data-start="0.000" data-duration="{f(total)}"\n'
            f'           data-volume="{f(audio.get("volume", 0.30))}"></audio>'
        )

    scene_rows = "\n".join(rows)
    return f"""<!DOCTYPE html>
<html lang="en" data-resolution="{resolution}">
<head>
  <meta charset="UTF-8">
  <title>{esc(bs['slug'])}</title>
  <style>
    /* Mandatory rule: border-box reset first, every composition.
       The shipped blank template carries this same reset
       (templates/blank/index.html). An explicit height plus padding under the
       CSS default renders LARGER than declared and pushes bottom-anchored
       content out of the safe zone. */
    *, *::before, *::after {{ box-sizing: border-box; }}
    html, body {{ margin: 0; padding: 0; }}
    body {{ width: {w}px; height: {h}px; overflow: hidden; background: {esc(bs.get('bg', '#101314'))}; }}
    .scene {{ position: absolute; inset: 0; }}
  </style>
</head>
<body>
  <!-- GENERATED from 03-beat-sheet.json by scripts/beats_to_composition.py.
       Do not hand-edit timing here; edit the beat sheet and re-run. -->
  <div id="root" data-composition-id="main" data-start="0" data-duration="{f(total)}"
       data-width="{w}" data-height="{h}">

{scene_rows}{audio_row}
  </div>

  <!-- GSAP from CDN is the shipped template's own pattern
       (templates/blank/index.html loads gsap from jsdelivr). -->
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    // The root timeline's only job is scene handoff; each sub-composition owns
    // its own beats. docs/gsap.md: paused, registered on window.__timelines.
    // No timeline `defaults: {{ ease }}` anywhere — every tween names its own
    // ease, because an inherited ease is an uncounted one [S6/A-10].
    window.__timelines = window.__timelines || {{}};
    var tl = gsap.timeline({{ paused: true }});
{trans_block}    tl.to({{}}, {{ duration: {f(total)}, ease: 'none' }}, 0);   // anchor: tl.duration() === root duration
    window.__timelines['main'] = tl;
  </script>
</body>
</html>
"""


def render_scene(bs: dict, sc: dict, idx: int, d_in: float = 0.0, d_out: float = 0.0):
    """Return (html, assertions). The sidecar is built from the same pass that
    emits the markup, so a selector can never exist in one and not the other.

    `d_in` / `d_out` are the DERIVED transition overlap windows either side of
    this scene ([S6/A-8]). The clip starts d_in early and runs d_in + d_out
    longer, so every beat offset inside the sub-composition shifts by +d_in and
    the sub-comp's own duration is dur + d_in + d_out. Absolute assertion times
    are unaffected: (start - d_in) + (off + d_in) == start + off."""
    cv = bs["canvas"]
    w, h = int(cv["w"]), int(cv["h"])
    dur = float(sc["duration"])
    total_dur = dur + d_in + d_out
    cid = slugify(sc["id"])
    safe = bs.get("safe_area") or {}
    st = int(safe.get("top", 192 if h > w else 80))
    sb = int(safe.get("bottom", 384 if h > w else 80))
    sr = int(safe.get("right", 162 if h > w else 120))
    sl = int(safe.get("left", 72 if h > w else 120))
    fonts = bs.get("fonts") or {}
    css_family = fonts.get("css", "'Inter', system-ui, sans-serif")
    gfont = fonts.get("google_css2")

    plate = sc.get("plate")
    bg = sc.get("bg", bs.get("bg", "#101314"))
    accent = sc.get("accent", bs.get("accent", "#93B896"))
    ink = bs.get("ink", "#F7F5F0")
    muted = bs.get("muted", "#9B9A97")

    # ---- markup for the beats -------------------------------------------
    els, tweens, assertions = [], [], []
    pre, entering = [], {}
    prev_sel = None
    prev_eid = None
    hold_n = 0
    n_count = 0
    uses = {"wipe": False, "swap": False, "count": False, "hold": False}
    arrive_y = 20 if h > w else 32   # [v1] landscape gets the longer travel
    # VERIFIED 2026-09-02, hyperframes 0.8.22: a transition translates or scales
    # the WHOLE scene wrapper, so every element inside it leaves the canvas
    # during the overlap and `staysInFrame` fires motion_off_frame by design
    # (observed: "#s01-b2 drifts off the 1080x1920 canvas at 2.7s" under a
    # push-slide LEFT). `staysInFrame` is therefore only asserted on a scene no
    # transition touches; inside a transition, staying in frame is not true.
    moved = d_in > 1e-9 or d_out > 1e-9
    for j, b in enumerate(sc["beats"]):
        role = b.get("role", "head" if j == 0 else "sub")
        cls = ROLE_CLASS.get(role, "sub")
        eid = f"{cid}-b{j}"
        text = b.get("text", b.get("caption", b.get("intent", "")))
        off = float(b["offset"])
        bdur = float(b.get("dur", DEFAULT_BEAT_DUR))
        idiom = b.get("idiom", DEFAULT_IDIOM)
        # `easing` still wins when the beat sheet names one; otherwise the idiom
        # supplies its own. Nothing is inherited from a timeline default.
        ease = (EASE.get(b["easing"], EASE[DEFAULT_EASE]) if "easing" in b
                else IDIOM_EASE[idiom])
        pos = f(off + d_in)          # [S6/A-8] every offset shifts by the overlap
        composed = off <= 0.0001     # composed at frame zero: it IS the hook

        # `hold` emits NO element: it is the camera staying alive over a
        # deliberate hold (rules/multi-phase-camera.md micro-drift), bounded and
        # finite, and it resolves. Never a breathing loop on a text card —
        # sine-wave-loop.md's own frontmatter says "reach for this last".
        if idiom == "hold":
            uses["hold"] = True
            sx, sy = (6, -4) if hold_n % 2 == 0 else (-6, 4)
            hold_n += 1
            tweens.append(
                f"  tl.to('#{cid}-stage', {{ x: {sx}, y: {sy}, scale: 1.01, "
                f"duration: {f(bdur)}, ease: '{ease}' }}, {pos});"
            )
            continue

        hide = ""
        if not composed:
            hide = " is-wiping" if idiom == "wipe" else " is-entering"

        if idiom == "count":
            # rules/counting-dynamic-scale.md. `count` owns the `stat` role: it
            # is a number, and the stat type scale is the one built for numbers.
            m = COUNT_RE.match(str(text).strip())
            prefix, number, suffix = m.group(1), m.group(2), m.group(3)
            while number and number[-1] in ".,":       # trailing punctuation is copy
                suffix, number = number[-1] + suffix, number[:-1]
            grouped = "," in number
            digits = number.replace(",", "")
            decimals = len(digits.split(".")[1]) if "." in digits else 0
            zero = "0" if decimals == 0 else "0." + "0" * decimals
            els.append(
                f'      <div class="beat stat{hide}" id="{eid}">{esc(prefix)}'
                f'<span class="cnt" data-from="0" data-to="{esc(number)}">{zero}</span>'
                f"{esc(suffix)}</div>"
            )
        elif idiom == "swap":
            # rules/scale-swap-transition.md — transform, don't replace. The two
            # states share one grid cell so the swap reads as one thing changing.
            prev_markup = els.pop() if els else ""
            els.append(
                '      <div class="slot">\n'
                + (f"  {prev_markup}\n" if prev_markup else "")
                + f'        <div class="beat {cls}{hide}" id="{eid}">{esc(text)}</div>\n'
                + "      </div>"
            )
        else:
            els.append(
                f'      <div class="beat {cls}{hide}" id="{eid}">{esc(text)}</div>'
            )

        # Two traps, one on each side, both confirmed by the engine's own lint:
        #   fromTo + immediateRender:false leaves the element at its CSS resting
        #     state until the tween STARTS, then snaps to the "from" value — the
        #     beat is visible at frame zero, blanks, then fades back in.
        #   tl.set(...) at position 0 is worse the other way: a zero-duration set
        #     at 0 does not render while the playhead sits exactly at 0, so frame
        #     zero shows the UN-hidden state (lint: gsap_timeline_set_initial_hide).
        # The state that survives a cold seek to 0 is one authored OUTSIDE the
        # timeline — in CSS, and re-stated with gsap.set() so the transform cache
        # agrees — with the timeline only ever tweening toward the visible state.
        if composed and idiom in ("arrive", "slam", "wipe", "swap"):
            # First beat is composed at frame zero: no entrance, it IS the hook.
            entering[eid] = False
        elif idiom == "slam":
            # rules/kinetic-beat-slam.md — a percussive hit on a spoken beat.
            entering[eid] = True
            pre.append(f"  gsap.set('#{eid}', {{ opacity: 0, scale: 1.12 }});")
            tweens.append(
                f"  tl.to('#{eid}', {{ opacity: 1, scale: 1, duration: {f(bdur)}, "
                f"ease: '{ease}' }}, {pos});"
            )
        elif idiom == "wipe":
            # A geometric reveal: opacity is deliberately untouched, so the CSS
            # resting state is the CLIP, not a zero alpha.
            uses["wipe"] = True
            entering[eid] = False
            pre.append(f"  gsap.set('#{eid}', {{ clipPath: 'inset(0 100% 0 0)' }});")
            tweens.append(
                f"  tl.to('#{eid}', {{ clipPath: 'inset(0 0% 0 0)', "
                f"duration: {f(bdur)}, ease: '{ease}' }}, {pos});"
            )
        elif idiom == "count":
            uses["count"] = True
            entering[eid] = not composed
            if composed:
                pre.append(f"  gsap.set('#{eid}', {{ scale: 0.86 }});")
                tweens.append(
                    f"  tl.to('#{eid}', {{ scale: 1, duration: {f(bdur)}, "
                    f"ease: '{ease}' }}, {pos});"
                )
            else:
                pre.append(f"  gsap.set('#{eid}', {{ opacity: 0, scale: 0.86 }});")
                tweens.append(
                    f"  tl.to('#{eid}', {{ opacity: 1, scale: 1, duration: {f(bdur)}, "
                    f"ease: '{ease}' }}, {pos});"
                )
            # The value itself rides a proxy object with a deterministic
            # onUpdate formatter — the sanctioned pattern (asr-keyword-glow uses
            # the same shape). No Date.now, no Math.random, no rAF: the writer
            # is the seeked timeline, so frame N always renders the same digits.
            pre.append(f"  var cntEl{n_count} = document.querySelector('#{eid} .cnt');")
            pre.append(f"  var cntPx{n_count} = {{ v: 0 }};")
            tweens.append(
                f"  tl.to(cntPx{n_count}, {{ v: {digits}, duration: {f(bdur)}, "
                f"ease: '{ease}',\n"
                f"    onUpdate: function () {{ cntEl{n_count}.textContent = hfNum("
                f"cntPx{n_count}.v, {decimals}, {'true' if grouped else 'false'}); }} }}, "
                f"{pos});"
            )
            n_count += 1
        elif idiom == "swap":
            uses["swap"] = True
            entering[eid] = True
            if prev_eid:
                # Outgoing rushes away on power2.in; only the INCOMING gets the
                # bouncy ease, or the swap reads mechanical.
                tweens.append(
                    f"  tl.to('#{prev_eid}', {{ scale: 0.6, opacity: 0, duration: 0.250, "
                    f"ease: 'power2.in' }}, {pos});"
                )
            pre.append(f"  gsap.set('#{eid}', {{ opacity: 0, scale: 0.6 }});")
            tweens.append(
                f"  tl.to('#{eid}', {{ opacity: 1, scale: 1, duration: {f(bdur)}, "
                f"ease: '{ease}' }}, {f(off + d_in + 0.12)});"
            )
        else:
            entering[eid] = True
            pre.append(f"  gsap.set('#{eid}', {{ opacity: 0, y: {arrive_y} }});")
            tweens.append(
                f"  tl.to('#{eid}', {{ opacity: 1, y: 0, duration: {f(bdur)}, "
                f"ease: '{ease}' }}, {pos});"
            )

        assertions.append(
            {
                "kind": "appearsBy",
                "selector": f"#{eid}",
                # absolute: `check` seeks the ROOT timeline, so a sub-composition
                # beat's assertion time is scene start + its own offset.
                "bySec": round(float(sc["start"]) + off + bdur + 0.25, 3),
            }
        )
        if idiom == "wipe":
            # A wipe never changes opacity, so `appearsBy` on it only proves the
            # copy element exists and is not hidden — the clip-path reveal itself
            # is outside all four assertion kinds' vocabulary. It is still worth
            # naming: a typo'd id fires motion_selector_missing, loudly. What it
            # must NOT get is `before`: an opacity-1 element "first appears" at
            # frame zero, so `before(prev, wipe)` reports motion_out_of_order.
            # When no transition moves the scene, staysInFrame is the one honest
            # geometric assertion available, so add it there.
            if not moved:
                assertions.append({"kind": "staysInFrame", "selector": f"#{eid}"})
        else:
            if prev_sel and entering[eid]:
                assertions.append({"kind": "before", "a": prev_sel, "b": f"#{eid}"})
            prev_sel = f"#{eid}"
        prev_eid = eid

    # ---- the plate, when the scene has one -------------------------------
    plate_markup = ""
    if plate:
        plate_markup = (
            f'    <div class="clip plate-wrap" id="{cid}-plate" data-layout-allow-overflow\n'
            f'         data-start="0" data-duration="{f(total_dur)}">\n'
            f'      <img id="{cid}-img" src="{esc(plate)}" alt=""\n'
            f'           width="{w}" height="{h}" loading="eager" decoding="sync">\n'
            f"    </div>\n"
            f'    <div class="clip scrim" data-start="0" data-duration="{f(total_dur)}"></div>\n'
        )
        # Ken Burns across the whole hold: a static plate is never left motionless.
        tweens.insert(
            0,
            f"  tl.fromTo('#{cid}-plate', {{ scale: 1.0 }}, {{ scale: 1.09, "
            f"duration: {f(total_dur)}, ease: 'none', immediateRender: true }}, 0);",
        )
        if not moved:
            assertions.append({"kind": "staysInFrame", "selector": f"#{cid}-b0"})

    gfont_link = ""
    if gfont:
        # The compiler fetches named Google Fonts and injects deterministic
        # @font-face at render time (observed: "Injected deterministic @font-face
        # rules"), so the CDN link is the shipped-supported path, not a hazard.
        gfont_link = (
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="">\n'
            f'<link href="{esc(gfont)}" rel="stylesheet">\n'
        )

    beats_markup = "\n".join(els)
    tween_lines = "\n".join(tweens)
    pre_lines = "\n".join(pre)
    plate_css = (
        """
  .plate-wrap { overflow: hidden; background: #1A1A1A; }
  .plate-wrap img { width: 100%; height: 100%; object-fit: cover; display: block;
    transform-origin: 50% 45%; }
  .scrim { background: linear-gradient(to bottom,
      rgba(0,0,0,0.82) 0%, rgba(0,0,0,0.60) 40%, rgba(0,0,0,0.78) 100%);
    pointer-events: none; }
"""
        if plate
        else ""
    )

    # [S6/A-10] idiom CSS is emitted ONLY for idioms this scene actually uses:
    # a scene of plain `arrive` beats emits exactly what it emitted before this
    # feature existed, which is what makes the back-compat diff readable.
    idiom_css = ""
    if uses["wipe"]:
        idiom_css += (
            "  /* `wipe` resting state: clipped, not transparent. Authored in CSS so a\n"
            "     cold seek to 0 paints the clip, and re-stated with gsap.set(). */\n"
            "  .beat.is-wiping { clip-path: inset(0 100% 0 0); }\n"
        )
    if uses["swap"]:
        idiom_css += (
            "  /* `swap`: both states share one grid cell and one transform-origin, so\n"
            "     the exchange reads as one thing changing rather than two things. */\n"
            "  .slot { display: grid; }\n"
            "  .slot > * { grid-area: 1 / 1; }\n"
        )
    if uses["count"]:
        idiom_css += (
            "  /* tabular-nums is MANDATORY on a counter: proportional digits reflow the\n"
            "     line on every frame. Size is static; only the transform scales. */\n"
            "  .cnt { font-variant-numeric: tabular-nums; display: inline-block; }\n"
        )
    idiom_css = idiom_css.rstrip("\n")

    count_helper = ""
    if uses["count"]:
        count_helper = (
            "  // Deterministic number formatting — no toLocaleString, whose grouping\n"
            "  // depends on the renderer's ICU data. Same input, same digits, always.\n"
            "  function hfNum(v, dp, grp) {\n"
            "    var s = dp > 0 ? v.toFixed(dp) : String(Math.round(v));\n"
            "    if (grp) { var p = s.split('.');\n"
            "      p[0] = p[0].replace(/\\B(?=(\\d{3})+(?!\\d))/g, ',');\n"
            "      s = p.join('.'); }\n"
            "    return s;\n"
            "  }\n"
        )

    return f"""<template>
{gfont_link}<style>
  /* GENERATED from 03-beat-sheet.json — edit the beat sheet, re-run the generator. */
  *, *::before, *::after {{ box-sizing: border-box; }}

  #root {{
    --safe-top: {st}px; --safe-bottom: {sb}px; --safe-right: {sr}px; --safe-left: {sl}px;
    --ink: {esc(ink)}; --accent: {esc(accent)}; --muted: {esc(muted)};
    position: relative; width: {w}px; height: {h}px; overflow: hidden;
    background: {esc(bg)}; font-family: {css_family};
  }}
  .clip {{ position: absolute; inset: 0; }}
{plate_css}
  /* Structural layout is Flex. position:absolute is scene/clip stacking only. */
  .stage {{ display: flex; flex-direction: column; justify-content: center;
    gap: 28px;
    padding: var(--safe-top) var(--safe-right) var(--safe-bottom) var(--safe-left); }}

  /* [restored from v1] Type floors for phone viewing: hero 96-160px,
     body 40px min, captions 42-56px, labels 26-32px with 32px the absolute
     floor for anything meant to be read. */
  .beat   {{ opacity: 1; overflow-wrap: anywhere; }}
  /* Authored OUTSIDE the timeline so a cold seek to t=0 paints the composed
     hook and nothing else. See the note beside the tweens below. */
  .beat.is-entering {{ opacity: 0; }}
  .kicker {{ font-weight: 700; font-size: 34px; letter-spacing: .16em;
            text-transform: uppercase; color: var(--accent); }}
  .head   {{ font-weight: 800; font-size: 112px; line-height: 1.03;
            letter-spacing: -.015em; text-transform: uppercase; color: var(--ink);
            margin: 0; }}
  .sub    {{ font-weight: 700; font-size: 46px; letter-spacing: .12em;
            text-transform: uppercase; color: var(--ink); }}
  /* Sentence-case size for lines too long to set as a hero without wrapping
     past the safe box. Still above the 40px reading-text floor [S6/A-6]. */
  .body   {{ font-weight: 600; font-size: 58px; line-height: 1.22;
            letter-spacing: -.005em; color: var(--ink); }}
  .flag   {{ font-weight: 600; font-size: 34px; letter-spacing: .06em;
            color: var(--muted); }}
  .cite   {{ font-weight: 700; font-size: 34px; letter-spacing: .10em;
            text-transform: uppercase; color: var(--accent); }}
  .stat   {{ font-weight: 800; font-size: 150px; line-height: 1; color: var(--accent); }}
  .caption{{ font-weight: 600; font-size: 44px; line-height: 1.25; color: var(--ink); }}
{idiom_css}
  /* Debug overlay lives on #root, never on <body>: a sub-composition's own
     renderable surface IS #root. Confirm it is off by looking at frame zero. */
  #root.debug-layout * {{ outline: 1px solid rgba(255,0,0,.6) !important; }}
  #root.debug-layout .clip {{ outline: 2px solid #00E5FF !important; }}
</style>

<div id="root" data-composition-id="{esc(cid)}" data-width="{w}" data-height="{h}"
     data-duration="{f(total_dur)}">
{plate_markup}    <div class="clip stage" id="{esc(cid)}-stage" data-start="0" data-duration="{f(total_dur)}">
{beats_markup}
    </div>
</div>
<script>
(function () {{
  // docs/gsap.md: create paused, register on window.__timelines[compositionId].
  // Supported methods are set / to / from / fromTo — nothing else is emitted.
  // Initial states first, immediate and outside the timeline.
{count_helper}{pre_lines}
  // NO `defaults: {{ ease }}` on this timeline. An inherited ease is an
  // UNCOUNTED ease: it is how a video ends up with 65% of its real tweens
  // sharing one entrance signature while every explicit-ease grep says
  // otherwise. Each tween below names the ease its idiom asked for [S6/A-10].
  var tl = gsap.timeline({{ paused: true }});
{tween_lines}
  tl.to({{}}, {{ duration: {f(total_dur)}, ease: 'none' }}, 0);   // anchor — always last, always at 0
  window.__timelines = window.__timelines || {{}};
  window.__timelines['{esc(cid)}'] = tl;
}})();
</script>
</template>
""", assertions


def build_sidecar(bs: dict, scenes: list, per_scene_assertions: dict) -> dict:
    """[S7/R-2] The motion sidecar `check` reads. Assertions are the beat sheet's
    own intent restated in the engine's vocabulary, so `check` verifies the
    render against what the beat sheet asked for, not against itself.

    There is now also a `keepsMoving` [S6/A-10, R-1b]: `appearsBy` and `before`
    can all pass on a piece whose every scene enters, washes and then sits — the
    frozen window is exactly what they do not see. `maxStaticSec` is the format's
    own cadence cap, not the assertion default of 2s, which is Shorts-scale.

    It is ONE composition-wide assertion, not one per scene, and that is an
    engine fact rather than a preference. MEASURED 2026-09-02 on hyperframes
    0.8.22 (see the module docstring): `keepsMoving`'s static-window scan runs
    over the WHOLE root composition duration, never bounded to the window in
    which the named scene's clip is live. A per-scene `withinSelector` therefore
    reports the scene's own OFF-SCREEN time as a frozen window and fails by
    construction — `#scene-s02` "static between 0s and 2.5s", `#scene-s01`
    "static between 3.5s and 9s" — with `#<cid>-stage` behaving identically.
    On a composition whose scenes tile, the composition-wide form has the same
    coverage for a frozen scene (nothing else is moving during that window
    either) and additionally covers the transition boundaries, which a
    scene-scoped selector skips."""
    total = sum(float(s["duration"]) for s in scenes)
    cap = CADENCE_CAP[bs["format"]]
    out = []
    for sc in scenes:
        out.extend(per_scene_assertions[sc["id"]])
    out.append({"kind": "keepsMoving", "withinSelector": "#root", "maxStaticSec": cap})
    return {"duration": round(total, 3), "assertions": out}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("beat_sheet")
    ap.add_argument("project_dir")
    ap.add_argument("--force", action="store_true",
                    help="overwrite index.html / compositions/frames if present")
    args = ap.parse_args()

    bs_path = Path(args.beat_sheet)
    if not bs_path.exists():
        die(f"beat sheet not found: {bs_path}")
    try:
        bs = json.loads(bs_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        die(f"beat sheet is not valid JSON: {e}")

    scenes, trans = validate(bs)
    d_in, d_out = overlap_windows(trans)

    proj = Path(args.project_dir)
    frames = proj / "compositions" / "frames"
    index = proj / "index.html"
    if index.exists() and not args.force:
        die(f"{index} exists — pass --force to regenerate")
    frames.mkdir(parents=True, exist_ok=True)

    per_scene_assertions = {}
    written = []
    for i, sc in enumerate(scenes):
        markup, assertions = render_scene(bs, sc, i, d_in[i], d_out[i])
        per_scene_assertions[sc["id"]] = assertions
        path = frames / scene_filename(i, sc["id"])
        if sc.get("handoff", "generated") == "hand-authored":
            # [S6/A-9] the file is a hand-authored multi-scene merge. The
            # generator still owns the clip, the derived transition and the
            # assertions; it must not overwrite the actors.
            if not path.exists():
                warn(
                    f"scene {sc['id']!r} is handoff='hand-authored' but {path} does not "
                    f"exist. Write it, honouring the id contract the assertions name: "
                    f"#{slugify(sc['id'])}-b<N> per beat and #{slugify(sc['id'])}-stage "
                    f"for the stage, or `check` reports motion_selector_missing."
                )
            else:
                print(f"  (kept hand-authored) {path}")
            continue
        path.write_text(markup, encoding="utf-8")
        written.append(path)

    index.write_text(render_root(bs, scenes, trans), encoding="utf-8")
    written.append(index)

    sidecar = proj / "index.motion.json"
    sidecar.write_text(json.dumps(build_sidecar(bs, scenes, per_scene_assertions), indent=2) + "\n",
                       encoding="utf-8")
    written.append(sidecar)

    total = sum(float(s["duration"]) for s in scenes)
    print(f"generated {len(scenes)} scene(s), {total:.3f}s, "
          f"{sum(len(s['beats']) for s in scenes)} beats")
    for p in written:
        print(f"  {p}")

    # [S6/A-8] transition ledger: types used, count per type, ground-change
    # boundaries. This is the line the delivery record copies.
    kinds: dict = {}
    ground_changes = 0
    default_bg = bs.get("bg", "#101314")
    for i, t in enumerate(trans):
        if i:
            if str(scenes[i].get("bg", default_bg)).lower() != str(
                scenes[i - 1].get("bg", default_bg)
            ).lower():
                ground_changes += 1
            label = t["type"] + (f" {t['direction']}" if t["direction"] else "")
            kinds[label] = kinds.get(label, 0) + 1
    # [S6/A-10] entrance-signature share: (property set + EFFECTIVE ease). The
    # inherited-default trap is why the ease is counted per tween, not grepped.
    sig: dict = {}
    for sc in scenes:
        for j, b in enumerate(sc["beats"]):
            if float(b["offset"]) <= 0.0001 and b.get("idiom", DEFAULT_IDIOM) in (
                "arrive", "slam", "wipe", "swap"
            ):
                continue                       # composed at frame zero — no entrance
            idiom = b.get("idiom", DEFAULT_IDIOM)
            ease = (EASE.get(b["easing"], EASE[DEFAULT_EASE]) if "easing" in b
                    else IDIOM_EASE[idiom])
            key = f"{idiom}/{ease}"
            sig[key] = sig.get(key, 0) + 1
    n_sig = sum(sig.values()) or 1
    top = max(sig.items(), key=lambda kv: kv[1]) if sig else ("-", 0)
    share = 100.0 * top[1] / n_sig
    print(
        f"\n[S6/A-8] boundaries: {len(scenes) - 1}, "
        f"{ground_changes} across a ground change; transitions: "
        + (", ".join(f"{k} x{v}" for k, v in sorted(kinds.items())) or "none (all cuts)")
    )
    print(
        f"[S6/A-10] entrance signatures: {len(sig)} distinct over {n_sig} entering "
        f"beat(s); top {top[0]} at {share:.0f}%"
    )
    if share > 50.0 and n_sig > 2:
        warn(
            f"[S6/A-10] {share:.0f}% of entering beats share the signature {top[0]!r}. "
            f"A majority sharing one entrance is the template failure regardless of "
            f"what the beats say — vary the idiom by narrative function [R8]."
        )
    if WARNINGS:
        print(f"\n{len(WARNINGS)} warning(s):", file=sys.stderr)
        for m in WARNINGS:
            print(f"  - {m}", file=sys.stderr)
    print("\nnext: npx hyperframes check --json --snapshots")


if __name__ == "__main__":
    main()
