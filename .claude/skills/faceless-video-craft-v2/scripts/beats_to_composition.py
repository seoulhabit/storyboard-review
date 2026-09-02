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


def die(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "-", str(s).lower()).strip("-") or "scene"


def esc(s) -> str:
    return html.escape(str(s), quote=True)


def f(x) -> str:
    """Fixed 3dp — the same string lands in the HTML and in the sidecar."""
    return f"{float(x):.3f}"


# --------------------------------------------------------------------------
# validation
# --------------------------------------------------------------------------
def validate(bs: dict) -> list:
    """Return the scene list, or die with the first structural problem."""
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
        marks = []
        for b in sc["beats"]:
            if "offset" not in b:
                die(f"a beat in scene {sc['id']!r} is missing 'offset'")
            off = float(b["offset"])
            bdur = float(b.get("dur", DEFAULT_BEAT_DUR))
            if off < 0 or off + bdur > dur + 1e-6:
                die(
                    f"beat at offset {off} (dur {bdur}) in scene {sc['id']!r} "
                    f"falls outside the scene's own {dur}s window"
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
    return scenes


# --------------------------------------------------------------------------
# emission
# --------------------------------------------------------------------------
def scene_filename(idx: int, sid: str) -> str:
    return f"{idx + 1:02d}-{slugify(sid)}.html"


def render_root(bs: dict, scenes: list) -> str:
    cv = bs["canvas"]
    w, h = int(cv["w"]), int(cv["h"])
    total = sum(float(s["duration"]) for s in scenes)
    resolution = "portrait" if h > w else "landscape"
    audio = bs.get("audio") or {}

    rows = []
    for i, sc in enumerate(scenes):
        cid = slugify(sc["id"])
        src = f"compositions/frames/{scene_filename(i, sc['id'])}"
        rows.append(
            f'    <div class="scene clip" id="scene-{esc(cid)}" data-composition-id="{esc(cid)}"\n'
            f'         data-composition-src="{esc(src)}"\n'
            f'         data-start="{f(sc["start"])}" data-duration="{f(sc["duration"])}"\n'
            f'         data-track-index="{i % 2}"></div>'
        )

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
    window.__timelines = window.__timelines || {{}};
    var tl = gsap.timeline({{ paused: true }});
    tl.to({{}}, {{ duration: {f(total)} }}, 0);   // anchor: tl.duration() === root duration
    window.__timelines['main'] = tl;
  </script>
</body>
</html>
"""


def render_scene(bs: dict, sc: dict, idx: int):
    """Return (html, assertions). The sidecar is built from the same pass that
    emits the markup, so a selector can never exist in one and not the other."""
    cv = bs["canvas"]
    w, h = int(cv["w"]), int(cv["h"])
    dur = float(sc["duration"])
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
    for j, b in enumerate(sc["beats"]):
        role = b.get("role", "head" if j == 0 else "sub")
        cls = ROLE_CLASS.get(role, "sub")
        eid = f"{cid}-b{j}"
        text = b.get("text", b.get("caption", b.get("intent", "")))
        off = float(b["offset"])
        bdur = float(b.get("dur", DEFAULT_BEAT_DUR))
        ease = EASE.get(b.get("easing", DEFAULT_EASE), EASE[DEFAULT_EASE])

        hide = " is-entering" if off > 0.0001 else ""
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
        if off <= 0.0001:
            # First beat is composed at frame zero: no entrance, it IS the hook.
            entering[eid] = False
        else:
            entering[eid] = True
            pre.append(f"  gsap.set('#{eid}', {{ opacity: 0, y: 20 }});")
            tweens.append(
                f"  tl.to('#{eid}', {{ opacity: 1, y: 0, duration: {f(bdur)}, "
                f"ease: '{ease}' }}, {f(off)});"
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
        if prev_sel:
            assertions.append({"kind": "before", "a": prev_sel, "b": f"#{eid}"})
        prev_sel = f"#{eid}"

    # ---- the plate, when the scene has one -------------------------------
    plate_markup = ""
    if plate:
        plate_markup = (
            f'    <div class="clip plate-wrap" id="{cid}-plate" data-layout-allow-overflow\n'
            f'         data-start="0" data-duration="{f(dur)}">\n'
            f'      <img id="{cid}-img" src="{esc(plate)}" alt=""\n'
            f'           width="{w}" height="{h}" loading="eager" decoding="sync">\n'
            f"    </div>\n"
            f'    <div class="clip scrim" data-start="0" data-duration="{f(dur)}"></div>\n'
        )
        # Ken Burns across the whole hold: a static plate is never left motionless.
        tweens.insert(
            0,
            f"  tl.fromTo('#{cid}-plate', {{ scale: 1.0 }}, {{ scale: 1.09, "
            f"duration: {f(dur)}, ease: 'none', immediateRender: true }}, 0);",
        )
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

  /* Debug overlay lives on #root, never on <body>: a sub-composition's own
     renderable surface IS #root. Confirm it is off by looking at frame zero. */
  #root.debug-layout * {{ outline: 1px solid rgba(255,0,0,.6) !important; }}
  #root.debug-layout .clip {{ outline: 2px solid #00E5FF !important; }}
</style>

<div id="root" data-composition-id="{esc(cid)}" data-width="{w}" data-height="{h}"
     data-duration="{f(dur)}">
{plate_markup}    <div class="clip stage" id="{esc(cid)}-stage" data-start="0" data-duration="{f(dur)}">
{beats_markup}
    </div>
</div>
<script>
(function () {{
  // docs/gsap.md: create paused, register on window.__timelines[compositionId].
  // Supported methods are set / to / from / fromTo — nothing else is emitted.
  // Initial states first, immediate and outside the timeline.
{pre_lines}
  var tl = gsap.timeline({{ paused: true, defaults: {{ ease: 'power3.out' }} }});
{tween_lines}
  tl.to({{}}, {{ duration: {f(dur)} }}, 0);   // anchor — always last, always at 0
  window.__timelines = window.__timelines || {{}};
  window.__timelines['{esc(cid)}'] = tl;
}})();
</script>
</template>
""", assertions


def build_sidecar(bs: dict, scenes: list, per_scene_assertions: dict) -> dict:
    """[S7/R-2] The motion sidecar `check` reads. Assertions are the beat sheet's
    own intent restated in the engine's vocabulary, so `check` verifies the
    render against what the beat sheet asked for, not against itself."""
    total = sum(float(s["duration"]) for s in scenes)
    out = []
    for sc in scenes:
        out.extend(per_scene_assertions[sc["id"]])
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

    scenes = validate(bs)

    proj = Path(args.project_dir)
    frames = proj / "compositions" / "frames"
    index = proj / "index.html"
    if index.exists() and not args.force:
        die(f"{index} exists — pass --force to regenerate")
    frames.mkdir(parents=True, exist_ok=True)

    per_scene_assertions = {}
    written = []
    for i, sc in enumerate(scenes):
        markup, assertions = render_scene(bs, sc, i)
        per_scene_assertions[sc["id"]] = assertions
        path = frames / scene_filename(i, sc["id"])
        path.write_text(markup, encoding="utf-8")
        written.append(path)

    index.write_text(render_root(bs, scenes), encoding="utf-8")
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
    print("\nnext: npx hyperframes check --json --snapshots")


if __name__ == "__main__":
    main()
