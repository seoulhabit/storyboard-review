# RETIRED-transitions.md

Verbatim block `beats_to_composition.py:197-479` from
`claude-skills/faceless-video-craft/scripts/beats_to_composition.py`, moved
here rather than deleted. This is the most carefully measured logic in that
file — a real 99-flagged-safe-area-frames-vs-0 measurement comparing
push-slide against a wipe on a 29-scene 1920×1080 composition, and a proven
overlap invariant for a derived transition window. WO-FVC-005's ruling
**C-6** (hard cuts only, no shader chain — fired by `T1-FINDINGS.md` F1
resolving PARTIAL under this session's zero-HeyGen-spend decision) makes
none of this code path reachable in the current compiler. It is preserved
here, verbatim, so a future reversal of C-6 does not have to re-derive any
of it.

**Do not import this file at compile time.** It is a historical record, not
a module. If C-6 is ever reversed, port from this file back into the
compiler deliberately, re-verifying the safe-area measurement below against
whatever `hyperframes` version is current at that time — engine internals
have already been confirmed to shift between minor versions in unrelated
ways this session (`ENGINE-DIFF-0.8.30.md`), so a multi-version-old
transition measurement should not be trusted blind.

---

```python
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
                f"scene {sc['id']!r} names transition type {kind!r}; this "
                f"generator has {TRANSITION_TYPES}. A bare 'wipe' is not one of "
                f"them — the two wipes are directional, 'wipe-left' and "
                f"'wipe-up', and they are authored here rather than taken from "
                f"the engine's Tier-B set. 'match-cut' and 'whip pan' exist "
                f"nowhere: neither is a named between-scene transition "
                f"(TRANSITION-REGISTRY.md), and whip pan is shader-only with no "
                f"CSS implementation."
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
```
