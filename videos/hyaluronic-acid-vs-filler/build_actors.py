#!/usr/bin/env python3
"""Emit the hand-authored scenes -- the ones carrying a diagram, a photoreal
plate, or the morphology actor.

v3 REWRITE 2026-09-03: 15 hand-authored scenes (was 10), covering a hook type
card, the three-lane lineup (x2, hook + recap), four photoreal plates of one
consistent subject, five diagram scenes reused near-unchanged from v2, one
genuine two-phase actor merge (s11-binds-and-seal, replacing two scenes that
redrew the same chain object -- see build_binds_and_seal()), and a warning
pair split from v2's single 21s do-not-inject scene. Still marked
`handoff: "hand-authored"` in the beat sheet, so the skill's generator emits
each one's clip, transition and motion assertions but NOT their markup
[S6/A-9]. Still reads every time from 03-beat-sheet.json: no timing is
hand-typed here either.

The actor is one molecule in three physical states, and that IS the video's
argument:
    ha-body    long free coils, dispersed, water caught in the loops
    ha-serum   the same chains in two sizes meeting a skin boundary
    ha-filler  the same chains cross-linked into a lattice that holds shape

DETERMINISM: every coordinate is computed HERE, in Python, with a fixed seed and
baked into static SVG path data. Nothing random, timed or measured runs inside
the composition -- the renderer seeks, it does not play.

FRAME-ZERO DISCIPLINE (new in v3): every scene's first beat is authored in
build_beats.py at offset 0, and every builder that runs through _hero_left(),
two_col() or plate_scene() now composes that first row at frame zero instead
of fading it in -- see _compose_first() below. v2 shipped this as a real,
uncaught gap: a wipe or a hard cut into a scene whose first beat still had an
entrance tween would reveal an empty ground for the tween's own duration.
lane_scene() and build_compare() already had this fix; it is now shared.

PANEL-SCALE MOTION: on a 1920-wide frame a headline sits in a grid cell, so a
text fade moves ~0.7% of the pixels. ectoin measured 4-5.8% active steps in its
first act for exactly that reason. The beats here move whole panels and whole
lanes.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
BS = json.load(open(f"{HERE}/03-beat-sheet.json"))
OUT = f"{HERE}/05-composition/compositions/frames"
SCENES = {s["id"]: s for s in BS["scenes"]}
ORDER = [s["id"] for s in BS["scenes"]]

# [correctness] every scene id must be a clean slug: build_actors.py names
# files from the RAW id (f"{idx:02d}-{sid}.html"), while the skill's own
# generator names them from a SLUGIFIED id (scene_filename() in
# beats_to_composition.py). Today every id is already slug-clean so the two
# never diverge, but nothing enforced that -- one capital letter or
# underscore would split the pipeline into two silently-disagreeing file
# namespaces. Enforced here rather than assumed.
for _sid in ORDER:
    assert re.fullmatch(r"[a-z0-9-]+", _sid), \
        f"scene id {_sid!r} is not a clean slug ([a-z0-9-]+) -- it will name " \
        f"one file for this script and a DIFFERENT file for the shared " \
        f"generator's own slugify()"

# [correctness] CRITICAL FIX, confirmed on the actual render, not just in
# source: beats_to_composition.py's render_scene() extends a GENERATED
# scene's own wrapper by d_in+d_out and shifts every beat offset by +d_in
# so its internal timeline lines up with the padded root-level wrapper
# window [S6/A-8] ("every offset inside the sub-composition shifts by
# +d_in ... the sub-comp's own duration is dur + d_in + d_out"). Nothing
# ever did that for a HAND-AUTHORED scene file -- confirmed by comparing
# every wrapper's declared data-duration in index.html against each
# sub-composition's own declared data-duration: every one of the 15
# hand-authored scenes here mismatched by exactly its own d_in+d_out.
# The runtime keys a sub-composition's visibility off ITS OWN declared
# duration, not the wrapper's, so the trailing `mismatch` seconds of
# EVERY hand-authored scene rendered as a hard, silent, fully blank
# frame -- measured directly on the rendered MP4: s08-serum-size (whose
# only mismatch is its own 0.350s incoming wipe) went completely blank
# from t=75.7s to its 76.049s cut into s09, reproduced identically via
# `hyperframes snapshot` on the live composition, ruling out a render-
# capture artifact. `hyperframes check`'s layout pass never saw it --
# it has no notion of "does this sub-composition go invisible before its
# wrapper's own window closes," the same class of blind spot as the
# padded-.stage drift bug this file already works around elsewhere.
# Fixed once, centrally, in scene_shell() and plate_scene() below, via
# _shift_tweens() -- not by hand-deriving a shift in all 15 builders.
def _transition_dur(sid):
    t = SCENES[sid].get("transition") or {"type": "cut"}
    return 0.0 if t.get("type") == "cut" else float(t.get("duration", 0.0))

D_IN, D_OUT = {}, {}
for _i, _sid in enumerate(ORDER):
    D_IN[_sid] = 0.0 if _i == 0 else _transition_dur(_sid)
    D_OUT[_sid] = 0.0 if _i == len(ORDER) - 1 else _transition_dur(ORDER[_i + 1])

_TWEEN_POS_RE = re.compile(r"(tl\.(?:to|fromTo)\([^;]*?,\s*)(-?\d+(?:\.\d+)?)(\);)")

def _shift_tweens(tweens, shift):
    """Shift every tl.to/tl.fromTo POSITION argument (never gsap.set, which is
    immediate and runs outside the timeline regardless of playhead) forward
    by `shift` seconds -- see the D_IN/D_OUT block above for why this exists.
    The anchor tween (`tl.to({}, {duration: ...}, 0)`) is authored directly
    by scene_shell() with the correct padded duration and is never passed
    through this function."""
    if shift <= 1e-9:
        return tweens
    out = []
    for line in tweens:
        m = _TWEEN_POS_RE.search(line)
        if not m:
            out.append(line)
            continue
        pos = float(m.group(2)) + shift
        out.append(_TWEEN_POS_RE.sub(
            lambda mm, _p=pos: f"{mm.group(1)}{_p:.3f}{mm.group(3)}", line, count=1))
    return out

IDIOM_EASE = {"arrive": "power3.out", "slam": "power4.out", "wipe": "power2.inOut",
              "count": "power2.out", "swap": "back.out(1.6)", "hold": "sine.inOut"}
# [simplification] shared default hold-drift magnitude -- was duplicated
# verbatim in two_col() and _hold_drift(), with nothing enforcing they stay
# in sync. s14-fda-warning already needs a scene-specific override
# (S14_DRIFTS, see build_warning_fullbleed()) after this exact default pushed
# content into a reserved safe-area zone in v2 (same defect, same fix,
# carried forward under the new scene id). That pattern will recur, and a
# future tune of the magnitude should only need to happen in one place.
DEFAULT_DRIFTS = [(10, -7, 1.018), (-9, 6, 1.005), (7, 8, 1.014), (-6, -6, 1.010)]

def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

# ---------------------------------------------------------------- geometry --
def coil(x0, y0, length, amp, wl, rng, wobble=0.35):
    """A sinuous polymer chain as one cubic-bezier path. Deterministic."""
    pts, x, y = [], x0, y0
    n = max(3, int(length / wl))
    for i in range(n + 1):
        t = i / n
        x = x0 + length * t
        y = y0 + math.sin(t * math.pi * 2 * (length / wl) / 2) * amp \
              + rng.uniform(-amp * wobble, amp * wobble)
        pts.append((x, y))
    d = f"M {pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(1, len(pts)):
        px, py = pts[i - 1]; cx, cy = pts[i]
        d += f" C {px+(cx-px)*0.4:.1f} {py:.1f} {px+(cx-px)*0.6:.1f} {cy:.1f} {cx:.1f} {cy:.1f}"
    return d

def free_coils(rng, n, w, h, length, amp, sw=7):
    """Dispersed free chains — the body state."""
    out = []
    for i in range(n):
        x = rng.uniform(10, max(12, w - length - 10))
        y = rng.uniform(40, h - 40)
        out.append(f'<path d="{coil(x, y, length, amp, 46, rng)}" fill="none" '
                   f'stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" opacity="0.9"/>')
    return "\n      ".join(out)

def water_dots(rng, n, w, h, r=7):
    return "\n      ".join(
        f'<circle cx="{rng.uniform(20, w-20):.1f}" cy="{rng.uniform(20, h-20):.1f}" '
        f'r="{r}" fill="currentColor" opacity="0.28"/>' for _ in range(n))

def lattice(w, h, cols, rows, pad=40):
    """Cross-linked net — the filler state. Nodes plus the struts between them."""
    xs = [pad + i * (w - 2*pad) / (cols - 1) for i in range(cols)]
    ys = [pad + j * (h - 2*pad) / (rows - 1) for j in range(rows)]
    seg, nod = [], []
    for j, y in enumerate(ys):
        for i, x in enumerate(xs):
            if i < cols - 1:
                seg.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{xs[i+1]:.1f}" y2="{y:.1f}"/>')
            if j < rows - 1:
                seg.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{ys[j+1]:.1f}"/>')
            if i < cols - 1 and j < rows - 1:   # the cross-links themselves
                seg.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{xs[i+1]:.1f}" y2="{ys[j+1]:.1f}" '
                           f'class="xl"/>')
            nod.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9"/>')
    return ('<g class="net-seg" fill="none" stroke="currentColor" stroke-width="6" '
            'stroke-linecap="round">\n      ' + "\n      ".join(seg) + "\n      </g>\n"
            '      <g class="net-nod" fill="currentColor">\n      ' + "\n      ".join(nod) + "\n      </g>")

def boundary_panel(rng, w, h):
    """Two chain sizes meeting a skin boundary — the serum state."""
    by = h * 0.46
    big = [f'<path d="{coil(rng.uniform(20, w*0.45), rng.uniform(60, by-70), w*0.42, 26, 52, rng)}" '
           f'fill="none" stroke="currentColor" stroke-width="9" stroke-linecap="round"/>'
           for _ in range(3)]
    small = []
    for _ in range(9):
        x = rng.uniform(20, w - 120); y = rng.uniform(by + 40, h - 40)
        small.append(f'<path d="{coil(x, y, 92, 11, 22, rng)}" fill="none" '
                     f'stroke="currentColor" stroke-width="6" stroke-linecap="round"/>')
    return (f'<g class="big">\n      ' + "\n      ".join(big) + "\n      </g>\n"
            f'      <line class="skin" x1="0" y1="{by:.1f}" x2="{w}" y2="{by:.1f}" '
            f'stroke="currentColor" stroke-width="4" stroke-dasharray="14 10" opacity="0.55"/>\n'
            f'      <g class="small">\n      ' + "\n      ".join(small) + "\n      </g>")

def skin_band(w, h, boundary_frac=0.30):
    """A two-layer skin cross-section: a thin epidermis band over a deeper
    dermis, with a gently wavy surface line. Reused by every scene that needs
    an honest (labelled) skin cross-section rather than a flat backdrop."""
    by = h * boundary_frac
    pts = []
    n = 10
    for i in range(n + 1):
        x = w * i / n
        y = 26 + math.sin(i * 0.9) * 8
        pts.append((x, y))
    top = f"M {pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(1, len(pts)):
        px, py = pts[i-1]; cx, cy = pts[i]
        top += f" L {cx:.1f} {cy:.1f}"
    return (f'<path d="{top}" fill="none" stroke="currentColor" stroke-width="4" opacity="0.7"/>\n'
            f'      <line class="skin" x1="0" y1="{by:.1f}" x2="{w}" y2="{by:.1f}" '
            f'stroke="currentColor" stroke-width="4" stroke-dasharray="14 10" opacity="0.55"/>\n'
            f'      <text x="16" y="{by-16:.1f}" font-size="22" fill="currentColor" '
            f'opacity="0.55" style="font-family:var(--font-mono)">EPIDERMIS</text>\n'
            f'      <text x="16" y="{h-20:.1f}" font-size="22" fill="currentColor" '
            f'opacity="0.55" style="font-family:var(--font-mono)">DERMIS</text>')

def eye_glassware_svg():
    """A tasteful, non-photorealistic 1930s-style illustration: an almond eye
    (outline + iris) beside a simple Erlenmeyer flask. Elegant, no gore, no
    likeness of a real person or animal in distress -- pure line art in the
    house idiom, the same restraint the channel uses everywhere else."""
    eye = (
        '<g transform="translate(40,120)">'
        '<path d="M0 90 C 60 10, 220 10, 280 90 C 220 170, 60 170, 0 90 Z" '
        'fill="none" stroke="currentColor" stroke-width="6"/>'
        '<circle cx="140" cy="90" r="46" fill="none" stroke="currentColor" stroke-width="6"/>'
        '<circle cx="140" cy="90" r="16" fill="currentColor" opacity="0.85"/>'
        + "".join(f'<path d="M {20+i*18} 24 q 6 -18 14 -22" fill="none" '
                  f'stroke="currentColor" stroke-width="4" stroke-linecap="round" opacity="0.6"/>'
                  for i in range(4))
        + '</g>'
    )
    flask = (
        '<g transform="translate(330,60)">'
        '<path d="M60 0 L60 60 L20 220 Q20 250 60 250 L140 250 Q180 250 180 220 L140 60 L140 0" '
        'fill="none" stroke="currentColor" stroke-width="6" stroke-linejoin="round"/>'
        '<path d="M30 190 Q100 210 170 190 L 140 220 Q 180 250 140 250 L 60 250 Q 20 250 60 220 Z" '
        'fill="currentColor" opacity="0.18"/>'
        '<rect x="50" y="-14" width="20" height="16" rx="3" fill="none" stroke="currentColor" stroke-width="6"/>'
        '<rect x="130" y="-14" width="20" height="16" rx="3" fill="none" stroke="currentColor" stroke-width="6"/>'
        + "".join(f'<line x1="{34+i*10}" y1="{170-i*4}" x2="{50+i*10}" y2="{170-i*4}" '
                  f'stroke="currentColor" stroke-width="3" opacity="0.35"/>' for i in range(6))
        + '</g>'
    )
    return (f'<svg class="actor" viewBox="0 0 560 320" width="560" height="320" '
            f'preserveAspectRatio="xMidYMid meet" aria-hidden="true">\n      {eye}\n      {flask}\n    </svg>')

def water_drop(cx, cy, r=8, eid=""):
    idattr = f' id="{eid}"' if eid else ""
    return f'<circle{idattr} cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="currentColor" opacity="0.85"/>'

def clinical_vignette_svg():
    """Calm, professional, non-graphic: a prepared tray, a capped/sealed
    syringe lying flat (never entering skin), a small vial, a gloved hand
    resting beside the tray. No face, no needle piercing anything."""
    tray = '<rect x="20" y="180" width="480" height="18" rx="9" fill="none" stroke="currentColor" stroke-width="5"/>'
    syringe = (
        '<g transform="translate(60,120)">'
        '<rect x="0" y="0" width="220" height="34" rx="8" fill="none" stroke="currentColor" stroke-width="5"/>'
        '<line x1="30" y1="0" x2="30" y2="34" stroke="currentColor" stroke-width="3" opacity="0.5"/>'
        '<line x1="60" y1="0" x2="60" y2="34" stroke="currentColor" stroke-width="3" opacity="0.5"/>'
        '<rect x="-46" y="8" width="46" height="18" rx="6" fill="none" stroke="currentColor" stroke-width="5"/>'
        '<rect x="220" y="10" width="34" height="14" rx="4" fill="currentColor" opacity="0.35"/>'
        '</g>'
    )
    vial = ('<g transform="translate(340,90)">'
            '<rect x="0" y="0" width="46" height="72" rx="8" fill="none" stroke="currentColor" stroke-width="5"/>'
            '<rect x="6" y="30" width="34" height="34" fill="currentColor" opacity="0.16"/>'
            '<rect x="10" y="-10" width="26" height="12" rx="3" fill="currentColor" opacity="0.5"/>'
            '</g>')
    glove = ('<g transform="translate(420,150)">'
             '<path d="M0 60 Q-10 10 30 6 Q34 -6 46 4 Q52 -6 62 6 Q70 -4 76 8 Q92 10 86 40 '
             'Q90 70 60 76 L10 76 Q0 74 0 60 Z" fill="none" stroke="currentColor" stroke-width="5" '
             'stroke-linejoin="round"/></g>')
    return (f'<svg class="actor" viewBox="0 0 520 260" width="520" height="260" '
            f'preserveAspectRatio="xMidYMid meet" aria-hidden="true">\n'
            f'      {tray}\n      {syringe}\n      {vial}\n      {glove}\n    </svg>')

def icon_body(size=96):
    return (f'<svg class="icon" viewBox="0 0 96 96" width="{size}" height="{size}" aria-hidden="true">'
            '<circle cx="48" cy="18" r="14" fill="none" stroke="currentColor" stroke-width="5"/>'
            '<path d="M48 32 L48 62 M48 40 L26 56 M48 40 L70 56 M48 62 L32 92 M48 62 L64 92" '
            'fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round"/></svg>')

def icon_bottle(size=96):
    return (f'<svg class="icon" viewBox="0 0 96 96" width="{size}" height="{size}" aria-hidden="true">'
            '<rect x="30" y="4" width="16" height="12" rx="2" fill="none" stroke="currentColor" stroke-width="5"/>'
            '<path d="M32 16 L32 30 L22 46 L22 88 Q22 92 26 92 L70 92 Q74 92 74 88 L74 46 L64 30 L64 16" '
            'fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round"/>'
            '<rect x="26" y="58" width="44" height="26" fill="currentColor" opacity="0.14"/></svg>')

def icon_syringe(size=96):
    return (f'<svg class="icon" viewBox="0 0 96 96" width="{size}" height="{size}" aria-hidden="true">'
            '<g transform="translate(6,40) rotate(-28 42 8)">'
            '<rect x="0" y="0" width="60" height="16" rx="4" fill="none" stroke="currentColor" stroke-width="5"/>'
            '<rect x="-14" y="3" width="14" height="10" rx="2" fill="none" stroke="currentColor" stroke-width="5"/>'
            '<line x1="60" y1="8" x2="82" y2="8" stroke="currentColor" stroke-width="4"/>'
            '</g></svg>')

# --------------------------------------------------------------- the actors --
PW, PH = 520, 620          # actor panel viewBox

def actor_svg(kind, cls=""):
    rng = random.Random({"body": 11, "serum": 23, "filler": 37}[kind])
    if kind == "body":
        inner = free_coils(rng, 5, PW, PH, 330, 30) + "\n      " + water_dots(rng, 26, PW, PH)
    elif kind == "serum":
        inner = boundary_panel(rng, PW, PH)
    else:
        inner = lattice(PW, PH, 6, 7)
    return (f'<svg class="actor {cls}" viewBox="0 0 {PW} {PH}" width="{PW}" height="{PH}" '
            f'preserveAspectRatio="xMidYMid meet" aria-hidden="true">\n      {inner}\n    </svg>')

# ------------------------------------------------------------------ scenes --
BASE_CSS = """
  *, *::before, *::after { box-sizing: border-box; }
  #root {
    --safe-top:54px; --safe-bottom:108px; --safe-left:96px; --safe-right:96px;
    --paper:#F7F5F0; --ink:#131516; --mist:#F0EBE1; --ink-soft:#211F1B;
    --aqua:#59B8AE; --moss:#4F6B52; --coral:#C97A5C; --ink-2:#6B6B6B;
    --ink-2-dark:#878B8C; --rule-strong:#D9D3C6; --rule-dark:#333333;
    --font-display:"EB Garamond",Georgia,"Times New Roman",serif;
    --font-body:"Inter",system-ui,-apple-system,Helvetica,Arial,sans-serif;
    --font-mono:"JetBrains Mono",ui-monospace,"SF Mono",Consolas,monospace;
    position:relative; width:1920px; height:1080px; overflow:hidden;
    font-family:var(--font-body); background:%(bg)s; color:%(ink)s;
  }
  .clip { position:absolute; inset:0; }
  /* DRIFT BUDGET, not decoration: a transform on a padded box moves the padded
     edge outward, so the pad must absorb (max scale - 1)/2 * canvas + max
     translate. 1.03 scale = 28.8px/side horizontally, 16.2px vertically. */
  .stage { padding: calc(var(--safe-top) + 60px) calc(var(--safe-right) + 60px)
                   calc(var(--safe-bottom) + 60px) calc(var(--safe-left) + 60px);
           height:100%%; display:flex; }
  .stage > * { min-width:0; }
  /* Type floors [S6/A-6]: hero 96-160, body 40 min, labels 32 absolute floor. */
  .head { font-family:var(--font-display); font-weight:600; font-size:104px;
          line-height:1.04; letter-spacing:-.018em; margin:0; }
  .sub  { font-weight:700; font-size:46px; letter-spacing:.10em;
          text-transform:uppercase; }
  .body { font-weight:600; font-size:52px; line-height:1.24; }
  .caption { font-weight:600; font-size:44px; line-height:1.26; }
  /* [S6/A-7] --aqua on paper measures 2.17:1 against the 3:1 floor for large
     bold text -- rgb(75,155,147) is `check`'s own suggestedColor in the same
     palette direction. The dark-ground branch below restates full --aqua,
     which measures well clear of the floor against --ink. */
  .kicker { font-weight:700; font-size:34px; letter-spacing:.16em;
            text-transform:uppercase; color:#4B9B93; }
  .stat { font-family:var(--font-display); font-weight:600; font-size:170px; line-height:1; }
  /* Citation chip: `Journal · Year` ONLY. Never a PMID, never an internal id --
     those live in the brief's claim table and the video description. */
  .cite { font-family:var(--font-mono); font-weight:500; font-size:32px;
          letter-spacing:.04em; color:var(--ink-2); border:2px solid var(--rule-strong);
          border-radius:999px; padding:10px 26px; width:max-content;
          background:var(--mist); display:inline-block; }
  .actor { color:var(--ink); display:block; }
  .lane-label { font-weight:700; font-size:34px; letter-spacing:.14em;
                text-transform:uppercase; color:var(--ink-2); }
  .beat { transform-origin: left center; }
  .beat.is-entering { opacity:0; }
  .beat.is-wiping { clip-path: inset(0 100%% 0 0); }
  #root.debug-layout * { outline:1px solid rgba(255,0,0,.6) !important; }
"""

def dark(bg): return str(bg).strip().lower() in ("#131516", "#211f1b")

def scene_shell(sid, css_extra, markup, sets, tweens, pre_stage=""):
    """pre_stage (new in v3): raw markup emitted as a SIBLING of .stage, inside
    #root but before it -- for full-bleed layers like a photoreal plate that
    must not inherit .stage's safe-area padding. "" is a no-op, so every
    existing caller's output is byte-identical to before this parameter
    existed (verified: re-running build_actors.py on the 7 scenes that don't
    pass it produces the same files it always did)."""
    sc = SCENES[sid]; dur = sc["duration"]
    # See the D_IN/D_OUT block above main content: the root-level wrapper for
    # this scene is dur+d_in+d_out wide, and the runtime keys this sub-
    # composition's own visibility off ITS OWN declared duration -- so it
    # must declare the PADDED width, not the raw content width, or its last
    # d_in+d_out seconds render as a hard blank (confirmed on-render).
    d_in, d_out = D_IN[sid], D_OUT[sid]
    dur_padded = round(dur + d_in + d_out, 3)
    ink = "#F7F5F0" if dark(sc["bg"]) else "#131516"
    css = (BASE_CSS % {"bg": sc["bg"], "ink": ink}) + css_extra
    if dark(sc["bg"]):
        css += ("\n  /* Flip the TOKEN, not just #root's colour: .actor strokes and\n"
                "     .badge borders read var(--ink) and would stay dark-on-dark. */\n"
                "  #root { --ink: #F7F5F0; --ink-2: #878B8C; }\n"
                "  .cite { color:var(--ink-2-dark); border-color:var(--rule-dark);"
                " background:var(--ink-soft); }\n  .kicker { color:var(--aqua); }\n")
    s = ["<template>", "<style>", css, "</style>", "",
         f'<div id="root" data-composition-id="{sid}" data-width="1920" data-height="1080"',
         f'     data-duration="{dur_padded:.3f}">']
    if pre_stage:
        s.append(pre_stage)
    s += [f'  <div class="clip stage" id="{sid}-stage" data-start="0" data-duration="{dur_padded:.3f}">',
         markup, "  </div>", "</div>", "<script>", "(function () {"]
    for x in sets: s.append("  " + x)
    s.append("  // No timeline `defaults: { ease }` — an inherited ease is an uncounted")
    s.append("  // one, and that is how a project ships a single entrance signature.")
    s.append("  var tl = gsap.timeline({ paused: true });")
    # Every content tween shifts by +d_in so it fires when the padded
    # wrapper's OWN reveal completes, not d_in seconds before it -- see
    # _shift_tweens()'s own docstring for the full reasoning and the
    # confirmed-on-render defect this fixes.
    for x in _shift_tweens(tweens, d_in): s.append("  " + x)
    s.append(f"  tl.to({{}}, {{ duration: {dur_padded:.3f}, ease: 'none' }}, 0);   // anchor — last, at 0")
    s.append("  window.__timelines = window.__timelines || {};")
    s.append(f"  window.__timelines['{sid}'] = tl;")
    s += ["})();", "</script>", "</template>", ""]
    return "\n".join(s)

def beats_of(sid):
    return SCENES[sid]["beats"]

def txt(b):
    return esc(b.get("text", b.get("intent", "")))

# ---------------------------------------------------------- lineup / badges --
LANE_CSS = """
  .col-wrap { display:flex; flex-direction:column; width:100%; height:100%;
              justify-content:space-between; gap:32px; }
  .lanes { display:grid; grid-template-columns:1fr 1fr 1fr; gap:0;
           width:100%; flex:0 1 auto; min-height:0; align-items:center;
           overflow:hidden; }
  .lane { display:flex; flex-direction:column; align-items:center; gap:16px;
          padding:0 26px; position:relative; height:100%; justify-content:center; }
  .lane + .lane::before { content:""; position:absolute; left:0; top:8%;
          bottom:8%; width:2px; background:var(--rule-strong); }
  .lane .actor { height:380px; width:auto; max-width:100%; flex:0 0 auto; }
  .lane-icon { position:absolute; top:6px; left:50%; transform:translateX(-50%);
               color:var(--kicker-color, #4B9B93); opacity:0.85; z-index:1; }
  .lane-icon svg { display:block; width:52px; height:52px; }
  .lane-copy { font-weight:700; font-size:34px; letter-spacing:.12em;
               text-transform:uppercase; color:var(--ink-2); text-align:center; }
  .badge { font-weight:700; font-size:34px; letter-spacing:.10em;
           text-transform:uppercase; color:var(--ink); border:2px solid var(--ink);
           border-radius:999px; padding:8px 22px; text-align:center; }
  .foot { display:flex; align-items:baseline; gap:28px; flex-wrap:wrap; }
"""

def lane_scene(sid, kinds=("body","serum","filler"), badge_roles=False, icons=None):
    """Three lanes of the SAME molecule in three states, plus title and payoff.

    Beat -> element mapping is by ORDER of the non-hold beats, so the ids match
    the generator's motion sidecar exactly (#<sid>-b<i>).
    """
    sc = SCENES[sid]; beats = sc["beats"]
    idx = [i for i, b in enumerate(beats) if b["idiom"] != "hold"]
    lane_i = [i for i in idx if beats[i].get("role") == "sub"][:3]
    head_i = [i for i in idx if beats[i].get("role") == "head"]
    kick_i = [i for i in idx if beats[i].get("role") == "kicker"]

    title, titled = "", None
    if head_i and abs(beats[head_i[0]]["offset"]) < 1e-6:
        titled = head_i[0]
        title = (f'      <h1 class="head beat" id="{sid}-b{titled}">'
                 f'{txt(beats[titled])}</h1>')
    lanes = []
    for n, kind in enumerate(kinds):
        bi = lane_i[n] if n < len(lane_i) else None
        lab = (f'<div class="lane-copy beat is-entering" id="{sid}-b{bi}">'
               f'{txt(beats[bi])}</div>') if bi is not None else ""
        cls = "badge" if badge_roles else "lane-copy"
        if badge_roles and bi is not None:
            lab = (f'<div class="badge beat is-entering" id="{sid}-b{bi}">'
                   f'{txt(beats[bi])}</div>')
        icon = f'<div class="lane-icon">{icons[n]()}</div>' if icons else ""
        lanes.append(f'        <div class="lane" id="{sid}-lane{n}">\n'
                     f'          {icon}\n'
                     f'          {actor_svg(kind)}\n'
                     f'          {lab}\n'
                     f'        </div>')
    foot = []
    for i in kick_i:
        foot.append(f'        <div class="kicker beat is-entering" id="{sid}-b{i}">'
                    f'{txt(beats[i])}</div>')
    for i in [h for h in head_i if h != titled]:
        foot.append(f'        <div class="head beat is-entering" id="{sid}-b{i}" '
                    f'style="font-size:76px;color:var(--aqua)">{txt(beats[i])}</div>')
    markup = ('    <div class="col-wrap">\n' + title + '\n'
              '      <div class="lanes">\n' + "\n".join(lanes) + '\n      </div>\n'
              '      <div class="foot">\n' + "\n".join(foot) + '\n      </div>\n'
              '    </div>')

    sets, tw = [], []
    for n in (0, 1, 2):
        sets.append(f"gsap.set('#{sid}-lane{n}', {{ opacity: 0.42, scale: 0.965 }});")
    for i in idx:
        if i == titled: continue
        sets.append(f"gsap.set('#{sid}-b{i}', {{ opacity: 0, y: 26 }});")
    for n, i in enumerate(lane_i):
        b = beats[i]; off = b["offset"]
        tw.append(f"tl.to('#{sid}-lane{n}', {{ opacity: 1, scale: 1, duration: 1.300, "
                  f"ease: 'power2.inOut' }}, {off:.3f});")
        tw.append(f"tl.to('#{sid}-b{i}', {{ opacity: 1, y: 0, duration: {b['dur']:.3f}, "
                  f"ease: '{IDIOM_EASE[b['idiom']]}' }}, {off:.3f});")
    for i in kick_i + [h for h in head_i if h != titled]:
        b = beats[i]
        tw.append(f"tl.to('#{sid}-b{i}', {{ opacity: 1, y: 0, duration: {b['dur']:.3f}, "
                  f"ease: '{IDIOM_EASE[b['idiom']]}' }}, {b['offset']:.3f});")
    if titled is not None:
        # [correctness] this used to run 0.150 -> 2.900 (push 1.500s, return
        # 1.200s), which `check` flags on s02-lineup and s15-badges: a hold
        # beat's own stage-drift tween can start as early as 1.900s (its
        # start is bounded by the beat fill pass, not by this fixed window),
        # so the two tweens fought over #stage's scale/y for up to 0.9s.
        # Tightened to finish by 1.800s -- clear of any observed hold start
        # in this project -- while keeping the same push-then-settle shape.
        tw.insert(0, f"tl.to('#{sid}-stage', {{ scale: 1.014, y: -7, duration: 1.000, "
                     f"ease: 'sine.inOut' }}, 0.150);")
        tw.insert(1, f"tl.to('#{sid}-stage', {{ scale: 1.0, y: 0, duration: 0.650, "
                     f"ease: 'sine.inOut' }}, 1.150);")
    LDRIFT = [(8, -6, 1.012), (-7, 5, 1.004), (6, 6, 1.009), (-5, -5, 1.006)]
    for n_, b in enumerate([x for x in beats if x["idiom"] == "hold"]):
        dx, dy, ds = LDRIFT[n_ % len(LDRIFT)]
        tw.append(f"tl.to('#{sid}-stage', {{ x: {dx}, y: {dy}, scale: {ds}, "
                  f"duration: {b['dur']:.3f}, ease: 'sine.inOut' }}, {b['offset']:.3f});")
    return scene_shell(sid, LANE_CSS, markup, sets, tw)

def build_lineup():
    return lane_scene("s02-lineup", icons=(icon_body, icon_bottle, icon_syringe))
def build_badges(): return lane_scene("s15-badges", badge_roles=True)

# --------------------------------------------------------- shared row logic --
ROLE_CLASS_MAP = {"head":"head","sub":"sub","body":"body","caption":"caption",
                   "cite":"cite","kicker":"kicker","stat":"stat"}

def _rows(sid, skip_roles=()):
    """Shared beat->row-markup pass used by every text column below."""
    out = []
    for i, bt in enumerate(beats_of(sid)):
        if bt["idiom"] == "hold" or bt.get("role") in skip_roles:
            continue
        cls = ROLE_CLASS_MAP.get(bt.get("role","body"), "body")
        out.append((i, bt, f'        <div class="{cls} beat is-entering" id="{sid}-b{i}">{txt(bt)}</div>'))
    return out

def _compose_first(sid, rows):
    """If rows[0] sits at offset 0, render it COMPOSED (no is-entering class,
    no entrance tween) and return (composed_markup, remaining_rows) -- the
    same treatment lane_scene() and build_compare() already gave their own
    titled beat. Everything downstream of _hero_left()/two_col()/plate_scene()
    gets this for free: a wipe or a hard cut into a scene never again reveals
    an empty ground while its first beat is still fading in (a real, shipped
    v2 defect on every _hero_left/two_col scene -- only lane_scene and
    build_compare had already special-cased it)."""
    if not rows or abs(rows[0][1]["offset"]) > 1e-6:
        return "", rows
    i, bt, markup = rows[0]
    cls = ROLE_CLASS_MAP.get(bt.get("role", "body"), "body")
    composed = f'        <div class="{cls} beat" id="{sid}-b{i}">{txt(bt)}</div>'
    return composed, rows[1:]

def _row_tweens(sid, rows_used):
    """Shared enter-tween pass matching two_col()'s idiom handling, reused by
    every bespoke hero-left/split/plate scene so beats behave identically
    everywhere. rows_used must already have any composed (frame-zero) row
    excluded -- see _compose_first()."""
    sets, tw = [], []
    for i, bt, _ in rows_used:
        ease = IDIOM_EASE[bt["idiom"]]; off, d = bt["offset"], bt["dur"]
        if bt["idiom"] == "wipe":
            sets.append(f"gsap.set('#{sid}-b{i}', {{ clipPath: 'inset(0 100% 0 0)', opacity: 1, y: 22 }});")
            tw.append(f"tl.to('#{sid}-b{i}', {{ clipPath: 'inset(0 0% 0 0)', y: 0, duration: {d:.3f}, ease: '{ease}' }}, {off:.3f});")
        elif bt["idiom"] == "swap":
            sets.append(f"gsap.set('#{sid}-b{i}', {{ opacity: 0, scale: 0.86 }});")
            tw.append(f"tl.to('#{sid}-b{i}', {{ opacity: 1, scale: 1, duration: {d:.3f}, ease: '{ease}' }}, {off:.3f});")
        elif bt["idiom"] == "slam":
            sets.append(f"gsap.set('#{sid}-b{i}', {{ opacity: 0, scale: 1.03, y: -18 }});")
            tw.append(f"tl.to('#{sid}-b{i}', {{ opacity: 1, scale: 1, y: 0, duration: {d:.3f}, ease: '{ease}' }}, {off:.3f});")
        elif bt["idiom"] == "count":
            sets.append(f"gsap.set('#{sid}-b{i}', {{ opacity: 0, scale: 0.86 }});")
            tw.append(f"tl.to('#{sid}-b{i}', {{ opacity: 1, scale: 1, duration: {d:.3f}, ease: '{ease}' }}, {off:.3f});")
        else:
            sets.append(f"gsap.set('#{sid}-b{i}', {{ opacity: 0, y: 30 }});")
            tw.append(f"tl.to('#{sid}-b{i}', {{ opacity: 1, y: 0, duration: {d:.3f}, ease: '{ease}' }}, {off:.3f});")
    return sets, tw

def _hold_drift(sid, target_sel, drifts=None):
    """drifts=None uses the shared default magnitude. Pass a smaller custom
    list for a scene whose content already sits close to a safe-area edge."""
    sets, tw = [], []
    DRIFTS = drifts or DEFAULT_DRIFTS
    drift = 0
    for bt in beats_of(sid):
        if bt["idiom"] != "hold": continue
        dx, dy, ds = DRIFTS[drift % len(DRIFTS)]; drift += 1
        tw.append(f"tl.to('{target_sel}', {{ x: {dx}, y: {dy}, scale: {ds}, "
                  f"duration: {bt['dur']:.3f}, ease: 'sine.inOut' }}, {bt['offset']:.3f});")
    return sets, tw

# ------------------------------------------------------------------- hook --
HOOK_CSS = """
  .hook-wrap { display:flex; flex-direction:column; justify-content:center; gap:26px;
               width:100%; height:100%; position:relative; z-index:1; }
  .hook-bg { position:absolute; inset:0; opacity:0.14; pointer-events:none; z-index:0; }
  .hook-wrap .head { font-size:136px; }
  .hook-wrap .sub  { font-size:52px; font-weight:600; letter-spacing:0;
                     text-transform:none; color:var(--ink-2); }
"""
def build_hook():
    """Frame zero, the thumbnail candidate, and the curiosity-gap hook: no
    diagram, no plate -- type as the performer, with a field of drifting
    water-dot texture behind it (the hydration motif, established before any
    diagram explains it) [S6/A-3]."""
    sid = "s01-hook"
    rng = random.Random(41)
    bg_dots = water_dots(rng, 30, 1920, 1080, r=5)
    bg_svg = (f'<svg class="hook-bg" viewBox="0 0 1920 1080" width="1920" height="1080" '
              f'preserveAspectRatio="xMidYMid slice" aria-hidden="true">\n      {bg_dots}\n    </svg>')
    rows = _rows(sid)
    composed, tween_rows = _compose_first(sid, rows)
    body = (composed + "\n" if composed else "") + "\n".join(r[2] for r in tween_rows)
    markup = ('    <div class="hook-wrap">\n' + bg_svg + "\n" + body + "\n    </div>")
    sets, tw = _row_tweens(sid, tween_rows)
    hs, ht = _hold_drift(sid, f"#{sid}-stage"); sets += hs; tw += ht
    return scene_shell(sid, HOOK_CSS, markup, sets, tw)

# ------------------------------------------------------------- two-column --
TWOCOL_CSS = """
  .two { display:grid; grid-template-columns: 1fr 560px; gap:80px; width:100%;
         align-items:center; }
  .col { display:flex; flex-direction:column; gap:26px; }
  .panel { position:relative; display:flex; align-items:center; justify-content:center;
           border:2px solid var(--rule-strong); border-radius:16px; padding:18px;
           background:rgba(0,0,0,0.015); }
  .panel.on { border-color:var(--aqua); }
  .panel .actor { color:var(--ink); }
"""

def two_col(sid, kind, panel_on=False):
    """Copy left, the morphology actor right. The panel is what MOVES.

    [simplification] v3: this used to duplicate _row_tweens()'s exact
    idiom-handling logic inline (same four branches, same shape) rather than
    calling it -- the two had drifted to be identical in every way that
    mattered, so this now shares the one implementation instead of two
    copies that could silently diverge. Also picks up _compose_first() for
    free, which the old inline version never had."""
    rows = _rows(sid)
    composed, tween_rows = _compose_first(sid, rows)
    col_body = (composed + "\n" if composed else "") + "\n".join(r[2] for r in tween_rows)
    markup = ('    <div class="two">\n'
              f'      <div class="col" id="{sid}-col">\n' + col_body + "\n      </div>\n"
              f'      <div class="panel{" on" if panel_on else ""}" id="{sid}-panel">\n'
              f'        {actor_svg(kind)}\n'
              "      </div>\n"
              "    </div>")
    sets = [f"gsap.set('#{sid}-panel', {{ opacity: 0, x: 60, scale: 0.94 }});"]
    tw = [f"tl.to('#{sid}-panel', {{ opacity: 1, x: 0, scale: 1, duration: 1.300, ease: 'power2.inOut' }}, 0.001);"]
    rs, rt = _row_tweens(sid, tween_rows); sets += rs; tw += rt
    hs, ht = _hold_drift(sid, f"#{sid}-panel"); sets += hs; tw += ht
    return scene_shell(sid, TWOCOL_CSS, markup, sets, tw)

# ------------------------------------------------------------- hero-left --
HEROSPLIT_CSS = """
  .split2 { display:grid; grid-template-columns: 1fr 560px; gap:80px; width:100%;
            align-items:center; }
  .col { display:flex; flex-direction:column; gap:26px; }
  .panel { position:relative; display:flex; align-items:center; justify-content:center;
           border:2px solid var(--rule-strong); border-radius:16px; padding:18px;
           background:rgba(0,0,0,0.015); }
  .panel .actor { color:var(--ink); }
"""

def _hero_left(sid, panel_markup, panel_setup_sets=None, panel_extra_tweens=None, css_extra=""):
    """head/sub/body/caption/cite text in a left column, one illustration
    panel on the right. The shared shape behind s05/s06/s11/s12/s13."""
    rows = _rows(sid)
    composed, tween_rows = _compose_first(sid, rows)
    col_body = (composed + "\n" if composed else "") + "\n".join(r[2] for r in tween_rows)
    markup = ('    <div class="split2">\n'
              f'      <div class="col" id="{sid}-col">\n'
              + col_body + "\n      </div>\n"
              f'      <div class="panel" id="{sid}-panel">\n'
              f'        {panel_markup}\n'
              "      </div>\n"
              "    </div>")
    sets = [f"gsap.set('#{sid}-panel', {{ opacity: 0, x: 60, scale: 0.94 }});"]
    tw = [f"tl.to('#{sid}-panel', {{ opacity: 1, x: 0, scale: 1, duration: 1.300, ease: 'power2.inOut' }}, 0.001);"]
    if panel_setup_sets: sets += panel_setup_sets
    if panel_extra_tweens: tw += panel_extra_tweens
    rs, rt = _row_tweens(sid, tween_rows); sets += rs; tw += rt
    hs, ht = _hold_drift(sid, f"#{sid}-panel"); sets += hs; tw += ht
    return scene_shell(sid, HEROSPLIT_CSS + css_extra, markup, sets, tw)

# ---- s05-origin: 1934, cow-eye vitreous, drawn in a tasteful 1930s idiom ---
def build_origin():
    return _hero_left("s05-origin", eye_glassware_svg())

# ---- s06-body: natural HA in a skin cross-section, water molecules --------
def build_body_cross():
    sid = "s06-body"
    rng = random.Random(11)
    inner = (skin_band(480, 560, boundary_frac=0.22)
             + "\n      " + free_coils(rng, 4, 480, 560, 260, 24, sw=6)
             + "\n      " + water_dots(rng, 20, 480, 560, r=6))
    panel = (f'<svg class="actor cross" viewBox="0 0 480 560" width="480" height="560" '
             f'preserveAspectRatio="xMidYMid meet" aria-hidden="true">\n      {inner}\n    </svg>')
    return _hero_left(sid, panel, css_extra="\n  .cross { width:100%; height:100%; }\n")

# ---- s07-compare: side-by-side cross-section, serum vs filler -------------
COMPARE_CSS = """
  .cmp-wrap { display:flex; flex-direction:column; gap:20px; width:100%; height:100%; }
  .cmp-title { font-family:var(--font-display); font-weight:600; font-size:64px;
               line-height:1.08; letter-spacing:-.012em; margin:0; }
  .cmp-lanes { display:grid; grid-template-columns:1fr 1fr; gap:56px; flex:1 1 auto; min-height:0; }
  .cmp-col { display:flex; flex-direction:column; align-items:center; justify-content:center;
             gap:14px; border:2px solid var(--rule-strong); border-radius:16px; padding:20px;
             overflow:hidden; }
  .cmp-col.on { border-color:var(--aqua); }
  .cmp-label { font-weight:700; font-size:32px; letter-spacing:.12em;
               text-transform:uppercase; color:var(--ink-2); }
  .cmp-col .actor { color:var(--ink); height:260px; width:auto; }
  .cmp-col .body { font-size:40px; line-height:1.18; }
"""
def build_compare():
    sid = "s07-compare"
    beats = beats_of(sid)
    idx = [i for i, b in enumerate(beats) if b["idiom"] != "hold"]
    head_i = [i for i in idx if beats[i].get("role") == "head"]
    body_i = [i for i in idx if beats[i].get("role") == "body"]
    cite_i = [i for i in idx if beats[i].get("role") == "cite"]

    rng_s = random.Random(23)
    serum_inner = boundary_panel(rng_s, 420, 460)
    serum_svg = (f'<svg class="actor" viewBox="0 0 420 460" width="420" height="460" '
                 f'preserveAspectRatio="xMidYMid meet" aria-hidden="true">\n      {serum_inner}\n    </svg>')
    filler_svg = (f'<svg class="actor" viewBox="0 0 420 460" width="420" height="460" '
                  f'preserveAspectRatio="xMidYMid meet" aria-hidden="true">\n'
                  f'      <g transform="translate(0,120)">{lattice(420, 460 - 120, 5, 5, pad=30)}</g>\n'
                  f'      {skin_band(420, 460, boundary_frac=0.20)}\n    </svg>')

    title = ""
    titled = None
    if head_i and abs(beats[head_i[0]]["offset"]) < 1e-6:
        titled = head_i[0]
        title = f'      <h1 class="cmp-title beat" id="{sid}-b{titled}">{txt(beats[titled])}</h1>'

    left_body = (f'<div class="body beat is-entering" id="{sid}-b{body_i[0]}">{txt(beats[body_i[0]])}</div>'
                 if len(body_i) > 0 else "")
    left_cite = (f'<div class="cite beat is-entering" id="{sid}-b{cite_i[0]}">{txt(beats[cite_i[0]])}</div>'
                 if len(cite_i) > 0 else "")
    right_body = (f'<div class="body beat is-entering" id="{sid}-b{body_i[1]}">{txt(beats[body_i[1]])}</div>'
                  if len(body_i) > 1 else "")
    right_cite = (f'<div class="cite beat is-entering" id="{sid}-b{cite_i[1]}">{txt(beats[cite_i[1]])}</div>'
                  if len(cite_i) > 1 else "")

    markup = (
        '    <div class="cmp-wrap">\n' + title + '\n'
        '      <div class="cmp-lanes">\n'
        f'        <div class="cmp-col" id="{sid}-colL">\n'
        '          <div class="cmp-label">Serum — surface</div>\n'
        f'          {serum_svg}\n          {left_body}\n          {left_cite}\n'
        '        </div>\n'
        f'        <div class="cmp-col" id="{sid}-colR">\n'
        '          <div class="cmp-label">Filler — beneath the skin</div>\n'
        f'          {filler_svg}\n          {right_body}\n          {right_cite}\n'
        '        </div>\n'
        '      </div>\n    </div>'
    )

    sets, tw = [], []
    for n, colsel in enumerate((f"#{sid}-colL", f"#{sid}-colR")):
        sets.append(f"gsap.set('{colsel}', {{ opacity: 0, y: 40, scale: 0.96 }});")
        tw.append(f"tl.to('{colsel}', {{ opacity: 1, y: 0, scale: 1, duration: 1.200, "
                  f"ease: 'power2.inOut' }}, {0.20 + n*0.35:.3f});")
    rows_used = [(i, beats[i], None) for i in idx if i != titled]
    rs, rt = _row_tweens(sid, rows_used); sets += rs; tw += rt
    hs, ht = _hold_drift(sid, f"#{sid}-colR" ); sets += hs; tw += ht
    return scene_shell(sid, COMPARE_CSS, markup, sets, tw)

# ---- s11-binds-and-seal: TWO-PHASE actor merge [S6/A-9] --------------------
# The old v2 cut drew this same "ha-serum" chain across TWO separate files
# (s08-binds-water, s09-lifeguard) with the same random seed and near-
# identical geometry -- coil(30,260,380,...) vs coil(30,260,340,...). That is
# the exact defect [S6/A-9] names: an actor redrawn instead of rearranged.
# Fixed here as one sub-composition: ONE chain path, drawn once. Phase 1
# pulls water droplets toward it (unchanged from the old build_binds_water);
# phase 2 fades those down and fades UP a moisturiser-seal band drawn onto
# the SAME path (unchanged mechanism from the old build_lifeguard). The actor
# is rearranged, never redrawn.
BINDS_SEAL_CSS = """
  /* [correctness] this scene merges two v2 scenes' worth of beats (6 text
     rows) into one file for [S6/A-9] -- _hero_left()'s plain flex column
     stacks all of them permanently and the sixth row ran 30-50px past the
     canvas bottom, confirmed on an extracted frame at t=99.5s (check's
     layout pass never caught it -- it has no notion of the canvas edge,
     same documented gap as the padded-.stage drift class of bug). Fixed by
     giving the TEXT column the same two-phase treatment the panel already
     has: phase 1's four rows and phase 2's two rows occupy the SAME grid
     cell (the `swap` idiom's own .slot pattern) and cross-fade at the
     phase boundary, so at most 4 rows are ever laid out at once. */
  .col-slot { display:grid; }
  .col-slot > .col-phase { grid-area: 1/1; display:flex; flex-direction:column; gap:26px; }
"""

def build_binds_and_seal():
    sid = "s11-binds-and-seal"
    rng = random.Random(23)
    chain_d = coil(30, 260, 360, 26, 48, rng)
    chain = f'<path d="{chain_d}" fill="none" stroke="currentColor" stroke-width="10" stroke-linecap="round"/>'

    starts = [(60,60),(380,50),(420,180),(40,420),(400,430),(220,40),(60,340),(430,300)]
    ends   = [(70,230),(150,230),(280,250),(120,300),(320,280),(200,220),(90,270),(340,240)]
    drops = [water_drop(sx, sy, r=9, eid=f"{sid}-drop{i}") for i, (sx, sy) in enumerate(starts)]

    seal = (f'<g id="{sid}-seal" opacity="0">'
            '<path d="M10 210 Q230 165 450 210 L450 236 Q230 200 10 236 Z" '
            'fill="currentColor" opacity="0.14"/>'
            '<text x="10" y="188" font-size="20" fill="currentColor" opacity="0.6" '
            'style="font-family:var(--font-mono)">MOISTURISER — SLOWS WATER LOSS</text>'
            '</g>')

    panel = (f'<svg class="actor" viewBox="0 0 460 460" width="460" height="460" '
             f'preserveAspectRatio="xMidYMid meet" aria-hidden="true">\n'
             f'      {chain}\n      ' + "\n      ".join(drops) + f'\n      {seal}\n    </svg>')

    beats = beats_of(sid)
    idx = [i for i, b in enumerate(beats) if b["idiom"] != "hold"]
    swap_i = [i for i in idx if beats[i]["idiom"] == "swap"]
    phase1_off = beats[swap_i[0]]["offset"] if swap_i else 2.0
    cap_i = [i for i in idx if beats[i].get("role") == "caption"]
    phase2_off = beats[cap_i[0]]["offset"] if cap_i else SCENES[sid]["duration"] * 0.55

    drop_sets, drop_tw = [], []
    for i, ((sx, sy), (ex, ey)) in enumerate(zip(starts, ends)):
        drop_sets.append(f"gsap.set('#{sid}-drop{i}', {{ opacity: 0.35 }});")
        drop_tw.append(f"tl.to('#{sid}-drop{i}', {{ x: {ex-sx}, y: {ey-sy}, opacity: 1, scale: 1.15, "
                       f"duration: 1.400, ease: 'power2.inOut' }}, {phase1_off + i*0.05:.3f});")
        # Phase 2: the droplets settle back rather than vanish -- rearranged.
        drop_tw.append(f"tl.to('#{sid}-drop{i}', {{ opacity: 0.25, scale: 0.9, "
                       f"duration: 1.000, ease: 'power2.inOut' }}, {phase2_off:.3f});")
    seal_sets = [f"gsap.set('#{sid}-seal', {{ opacity: 0 }});"]
    seal_tw = [f"tl.to('#{sid}-seal', {{ opacity: 1, duration: 1.200, ease: 'power2.out' }}, {phase2_off:.3f});"]

    # --- the text column: two phase groups sharing one grid cell ----------
    rows = _rows(sid)
    composed, tween_rows = _compose_first(sid, rows)
    phase1_rows = [r for r in tween_rows if r[1]["offset"] < phase2_off - 1e-6]
    phase2_rows = [r for r in tween_rows if r[1]["offset"] >= phase2_off - 1e-6]
    phase1_body = (composed + "\n" if composed else "") + "\n".join(r[2] for r in phase1_rows)
    phase2_body = "\n".join(r[2] for r in phase2_rows)

    markup = ('    <div class="split2">\n'
              f'      <div class="col-slot" id="{sid}-col">\n'
              f'        <div class="col-phase" id="{sid}-colphase1">\n{phase1_body}\n        </div>\n'
              f'        <div class="col-phase" id="{sid}-colphase2">\n{phase2_body}\n        </div>\n'
              '      </div>\n'
              f'      <div class="panel" id="{sid}-panel">\n'
              f'        {panel}\n'
              "      </div>\n"
              "    </div>")

    sets = [f"gsap.set('#{sid}-panel', {{ opacity: 0, x: 60, scale: 0.94 }});",
            f"gsap.set('#{sid}-colphase2', {{ opacity: 0 }});"] + drop_sets + seal_sets
    tw = [f"tl.to('#{sid}-panel', {{ opacity: 1, x: 0, scale: 1, duration: 1.300, ease: 'power2.inOut' }}, 0.001);"]
    # Cross-fade the phase groups at the same boundary the panel itself
    # transforms on -- text and diagram change together, one moment.
    fade_at = max(0.0, phase2_off - 0.30)
    tw.append(f"tl.to('#{sid}-colphase1', {{ opacity: 0, duration: 0.500, ease: 'power2.inOut' }}, {fade_at:.3f});")
    tw.append(f"tl.to('#{sid}-colphase2', {{ opacity: 1, duration: 0.500, ease: 'power2.inOut' }}, {phase2_off:.3f});")
    tw += drop_tw + seal_tw
    rs, rt = _row_tweens(sid, tween_rows); sets += rs; tw += rt
    hs, ht = _hold_drift(sid, f"#{sid}-panel"); sets += hs; tw += ht
    return scene_shell(sid, HEROSPLIT_CSS + BINDS_SEAL_CSS, markup, sets, tw)

# ---- s12-crosslink: loose chains TRANSFORM into a connected grid ----------
def build_crosslink_transform():
    sid = "s12-crosslink"
    rng = random.Random(37)
    loose = free_coils(rng, 5, 480, 560, 300, 28, sw=8)
    net = lattice(480, 560, 6, 7)
    panel = (f'<svg class="actor" viewBox="0 0 480 560" width="480" height="560" '
             f'preserveAspectRatio="xMidYMid meet" aria-hidden="true">\n'
             f'      <g class="loose-state" id="{sid}-loose">{loose}</g>\n'
             f'      <g class="net-state" id="{sid}-net" opacity="0" transform="scale(0.92)" '
             f'transform-origin="240 280">{net}</g>\n    </svg>')

    beats = beats_of(sid)
    idx = [i for i, b in enumerate(beats) if b["idiom"] != "hold"]
    swap_i = [i for i in idx if beats[i]["idiom"] == "swap"]
    off = beats[swap_i[0]]["offset"] if swap_i else 1.0
    d = beats[swap_i[0]]["dur"] if swap_i else 1.5

    xform_sets = [f"gsap.set('#{sid}-net', {{ opacity: 0, scale: 0.92 }});"]
    xform_tw = [
        f"tl.to('#{sid}-loose', {{ opacity: 0, scale: 0.94, duration: {d:.3f}, ease: 'power2.inOut' }}, {off:.3f});",
        f"tl.to('#{sid}-net', {{ opacity: 1, scale: 1, duration: {d:.3f}, ease: 'power2.inOut' }}, {off:.3f});",
    ]
    return _hero_left(sid, panel, panel_setup_sets=xform_sets, panel_extra_tweens=xform_tw)

# ---- s13-warning-question: the clinical vignette + the rhetorical question -
def build_warning_question():
    return _hero_left("s13-warning-question", clinical_vignette_svg())

# ---- s14-fda-warning: full-bleed, composed at frame 0 (lands on a CUT) ----
WARNING_FULLBLEED_CSS = """
  .warn-wrap { display:flex; flex-direction:column; gap:30px; width:100%; height:100%;
               justify-content:center; }
  .warn-head { font-family:var(--font-display); font-weight:600; font-size:148px;
               line-height:0.98; letter-spacing:-.01em; color:var(--coral); margin:0; }
"""
def build_warning_fullbleed():
    """This scene is ENTERED BY A HARD CUT [S6/A-8] -- the ALL-CAPS headline
    must already be on screen the instant the cut lands, or the cut reveals
    an empty frame for the length of an entrance tween. Composed at frame 0,
    same discipline as _compose_first(), applied by hand here because the
    coral .warn-head treatment is bespoke to this scene, not the shared
    ROLE_CLASS_MAP path _rows() uses."""
    sid = "s14-fda-warning"
    beats = beats_of(sid)
    idx = [i for i, b in enumerate(beats) if b["idiom"] != "hold"]
    by_role = {r: [i for i in idx if beats[i].get("role") == r]
               for r in ("head", "cite", "body", "sub")}
    head_i = by_role["head"][0] if by_role["head"] else None
    cite_i = by_role["cite"][0] if by_role["cite"] else None
    head_composed = head_i is not None and abs(beats[head_i]["offset"]) < 1e-6

    head_md = ""
    if head_i is not None:
        cls = "warn-head beat" if head_composed else "warn-head beat is-entering"
        head_md = f'      <h1 class="{cls}" id="{sid}-b{head_i}">{txt(beats[head_i])}</h1>'
    cite_md = (f'      <div class="cite beat is-entering" id="{sid}-b{cite_i}">{txt(beats[cite_i])}</div>'
              if cite_i is not None else "")
    body_rows = "\n".join(f'      <div class="body beat is-entering" id="{sid}-b{i}">{txt(beats[i])}</div>'
                          for i in by_role["body"])
    sub_rows = "\n".join(f'      <div class="sub beat is-entering" id="{sid}-b{i}">{txt(beats[i])}</div>'
                         for i in by_role["sub"])
    markup = ('    <div class="warn-wrap">\n' + head_md + '\n' + cite_md
              + '\n' + body_rows + '\n' + sub_rows + '\n    </div>')

    rows_used = [(i, beats[i], None) for i in idx if not (i == head_i and head_composed)]
    sets, tw = _row_tweens(sid, rows_used)
    # s14's own content already reaches close to the bottom safe-area edge by
    # design (the full-bleed warning look, carried over from v2's s11) -- cap
    # drift well below the shared default so a hold can never push it over.
    S14_DRIFTS = [(6, 0, 1.006), (-5, 0, 1.004), (4, 0, 1.005), (-4, 0, 1.003)]
    hs, ht = _hold_drift(sid, f"#{sid}-stage", drifts=S14_DRIFTS); sets += hs; tw += ht
    return scene_shell(sid, HEROSPLIT_CSS + WARNING_FULLBLEED_CSS, markup, sets, tw)

# ---------------------------------------------------------- photoreal plate --
PLATE_CSS = """
  .plate-wrap { position:absolute; inset:0; overflow:hidden; background:var(--ink-soft); }
  .plate-wrap img { width:100%; height:100%; object-fit:cover;
                    object-position:var(--plate-focus, 50% 38%);
                    display:block; transform-origin:50% 50%; will-change:transform; }
  .scrim { position:absolute; inset:0; pointer-events:none;
           background:linear-gradient(180deg,
             rgba(19,21,22,0.30) 0%,  rgba(19,21,22,0.05) 24%,
             rgba(19,21,22,0.08) 50%, rgba(19,21,22,0.70) 80%,
             rgba(19,21,22,0.92) 100%); }
  .stage { flex-direction:column; justify-content:flex-end; }
  .plate-copy { display:flex; flex-direction:column; gap:20px; max-width:1200px;
                position:relative; z-index:1; }
  .plate-copy .head { font-size:88px; color:#F7F5F0; }
  .plate-copy .kicker { color:#8FD6CC; }
  .plate-copy .sub { color:#F7F5F0; font-size:44px; letter-spacing:0.06em; }
"""
# One camera leg per plate -- four DIFFERENT moves (this repo's own
# ceramides-skin-barrier/compositions/frames/01-hook.html convention: the Ken
# Burns rides the IMG inside a fixed crop box, never the WRAPPER -- a wrapper
# scale maps the crop edge outward, the exact class of defect
# check-safe-area.py caught on this project's own padded .stage before).
# (x,y,scale) -> (x,y,scale), applied to the <img>, not the wrapper.
PLATE_MOVES = {
  "s03-misconception-plate": ((0, 0, 1.00), (0, -22, 1.085)),
  "s04-not-filler-plate":    ((-14, 0, 1.06), (0, 0, 1.00)),
  "s09-plumping-plate":      ((0, 14, 1.02), (12, -14, 1.09)),
  "s16-takeaway-plate":      ((10, -10, 1.05), (-10, 8, 1.01)),
}
PLATE_DRIFTS = [(6, 0, 1.005), (-5, 0, 1.004), (4, 0, 1.005), (-4, 0, 1.003)]

# Filled in after the plates are generated -- see PLATE_DIMS_NOTE at the
# bottom of this file. Placeholder native dims match the requested 16:9
# generation aspect; corrected to the real PNG dimensions once shipped.
PLATE_DIMS = {
  "s03-misconception-plate": (1920, 1080),
  "s04-not-filler-plate":    (1920, 1080),
  "s09-plumping-plate":      (1920, 1080),
  "s16-takeaway-plate":      (1920, 1080),
}
PLATE_ALT = {
  "s03-misconception-plate": "Woman looking at a serum bottle with a thoughtful, questioning expression",
  "s04-not-filler-plate":    "Close-up of a woman's hands holding a dropper of serum near her cheek",
  "s09-plumping-plate":      "Woman touching her cheek, checking her skin in soft natural light",
  "s16-takeaway-plate":      "Woman applying serum to her face in a calm, editorial skincare moment",
}

def plate_scene(sid, src):
    """A photoreal 16:9 plate under a text scrim -- the four moments the
    revision brief names: the opening misconception, "a serum is not filler
    in a bottle", the temporary surface-plumping explanation, and the final
    practical takeaway. Ken Burns rides the <img>, never the wrapper; the
    crop box (.plate-wrap) stays pinned to the canvas throughout."""
    (x0, y0, s0), (x1, y1, s1) = PLATE_MOVES[sid]
    nat_w, nat_h = PLATE_DIMS[sid]
    dur = SCENES[sid]["duration"]
    # pre_stage markup is built here, BEFORE scene_shell() runs, so it must
    # independently use the PADDED duration for any full-window .clip layer
    # (plate-wrap, scrim) -- see the D_IN/D_OUT block near the top of this
    # file. Left at raw `dur` these two layers would go invisible during the
    # trailing d_out seconds even after scene_shell()'s own #root/.stage fix,
    # since a .clip's visibility is keyed off ITS OWN data-duration.
    d_in, d_out = D_IN[sid], D_OUT[sid]
    dur_padded = round(dur + d_in + d_out, 3)
    rows = _rows(sid)
    composed, tween_rows = _compose_first(sid, rows)
    body = (composed + "\n" if composed else "") + "\n".join(r[2] for r in tween_rows)

    pre_stage = (
        f'  <div class="clip plate-wrap" id="{sid}-plate" data-layout-allow-overflow\n'
        f'       data-start="0" data-duration="{dur_padded:.3f}">\n'
        f'    <img id="{sid}-img" src="{esc(src)}" alt="{esc(PLATE_ALT[sid])}"\n'
        f'         width="{nat_w}" height="{nat_h}" loading="eager" decoding="sync">\n'
        f'  </div>\n'
        f'  <div class="clip scrim" id="{sid}-scrim" data-start="0" data-duration="{dur_padded:.3f}"></div>')

    markup = '    <div class="plate-copy">\n' + body + '\n    </div>'

    # Authored at position 0 for duration (dur + d_out): scene_shell()'s
    # uniform +d_in shift (applied to every tl.to/fromTo, this one included)
    # moves it to start at d_in and run through dur_padded exactly -- the
    # Ken Burns fills the padded window edge to edge with no gap, no
    # overshoot, using the same one mechanism as every other tween here.
    sets = [f"gsap.set('#{sid}-img', {{ x: {x0}, y: {y0}, scale: {s0} }});"]
    tw = [f"tl.fromTo('#{sid}-img', {{ x: {x0}, y: {y0}, scale: {s0} }}, "
          f"{{ x: {x1}, y: {y1}, scale: {s1}, duration: {(dur + d_out):.3f}, "
          f"ease: 'none', immediateRender: true }}, 0);"]

    rs, rt = _row_tweens(sid, tween_rows); sets += rs; tw += rt
    hs, ht = _hold_drift(sid, f"#{sid}-stage", drifts=PLATE_DRIFTS); sets += hs; tw += ht
    return scene_shell(sid, PLATE_CSS, markup, sets, tw, pre_stage=pre_stage)

PLATE_SRC = {
  "s03-misconception-plate": "assets/images/subject-01-misconception.png",
  "s04-not-filler-plate":    "assets/images/subject-02-not-filler.png",
  "s09-plumping-plate":      "assets/images/subject-03-plumping.png",
  "s16-takeaway-plate":      "assets/images/subject-04-takeaway.png",
}

BUILD = {
  "s01-hook":                 build_hook,
  "s02-lineup":                build_lineup,
  "s03-misconception-plate":   lambda: plate_scene("s03-misconception-plate", PLATE_SRC["s03-misconception-plate"]),
  "s04-not-filler-plate":      lambda: plate_scene("s04-not-filler-plate", PLATE_SRC["s04-not-filler-plate"]),
  "s05-origin":                build_origin,
  "s06-body":                  build_body_cross,
  "s07-compare":               build_compare,
  "s08-serum-size":            lambda: two_col("s08-serum-size", "serum", panel_on=True),
  "s09-plumping-plate":        lambda: plate_scene("s09-plumping-plate", PLATE_SRC["s09-plumping-plate"]),
  "s11-binds-and-seal":        build_binds_and_seal,
  "s12-crosslink":             build_crosslink_transform,
  "s13-warning-question":      build_warning_question,
  "s14-fda-warning":           build_warning_fullbleed,
  "s15-badges":                build_badges,
  "s16-takeaway-plate":        lambda: plate_scene("s16-takeaway-plate", PLATE_SRC["s16-takeaway-plate"]),
}

def fix_generated_grounds():
    """Mechanical [S7/R-1] fix on the GENERATED scenes (s10-houseplant,
    s17-endcard in v3).

    The generator sets `--ink: #131516` on #root and then paints #root with the
    scene's own `bg`. On a dark ground that is ink text on ink -- literally
    invisible copy, not merely low-contrast. Every dark generated scene has it.

    Also swaps the citation chip's accent on light grounds: #59B8AE on #F7F5F0
    measured 2.17:1 against a 3:1 requirement, and rgb(75,155,147) is `check`'s
    own suggestedColor in the same palette direction [S6/A-7].
    """
    fixed = 0
    css_subs = 0
    motion_subs = 0
    for i, sid in enumerate(ORDER, start=1):
        sc = SCENES[sid]
        if sc["handoff"] != "generated":
            continue
        path = f"{OUT}/{i:02d}-{sid}.html"
        html = open(path).read()
        # [correctness] idempotency guard: this fixer is NOT safe to run twice
        # on the same file -- running it a second time (e.g. re-invoking
        # build_actors.py without first regenerating compositions/frames/ from
        # the beat sheet) duplicated this CSS block verbatim into both
        # generated scenes, confirmed on this exact project. The project-wide
        # convention is "always regenerate from scratch"; this makes it safe
        # even when that convention slips.
        if "[S7/R-2] a slam parked at scale 1.12" in html:
            print(f"  {sid}: already ground/contrast-fixed (re-run without regenerating "
                  f"compositions/frames/ first) -- skipping to avoid duplicating the CSS block")
            continue
        pad = ("\n  /* [S7/R-2] a slam parked at scale 1.12 on a full-width block\n"
               "     grows 6% past each edge -- 370px of ink inside left<96 at\n"
               "     t=117.75s. Origin-left pins the edge; the punch goes vertical. */\n"
               "  .beat { transform-origin: left center; }\n"
               "\n  /* [S7/R-2] drift budget: a transform on a padded box maps the\n"
               "     padded edge OUTWARD. Measured 207 frames of ink inside left<96\n"
               "     before this. Pad to safe+60 so scale+translate stay clear. */\n"
               "  .stage { padding: calc(var(--safe-top) + 60px) calc(var(--safe-right) + 60px)\n"
               "                   calc(var(--safe-bottom) + 60px) calc(var(--safe-left) + 60px); }\n")
        if dark(sc["bg"]):
            css = pad + "\n  /* [K-4] one citation treatment for the whole video. */\n" + """  .cite { font-family:"JetBrains Mono",ui-monospace,"SF Mono",Consolas,monospace;\n          font-weight:500; font-size:32px; letter-spacing:.04em;\n          text-transform:none; color:#878B8C; border:2px solid #333333;\n          border-radius:999px; padding:10px 26px; width:max-content;\n          background:#211F1B; display:inline-block; }\n""" + ("\n  /* [S7/R-1] dark-ground ink flip: the generator leaves --ink at\n"
                   "     #131516 on a #131516 ground -> 1:1, invisible text. */\n"
                   "  #root { --ink: #F7F5F0; --muted: #878B8C; }\n")
        else:
            css = pad + "\n  /* [K-4] one citation treatment for the whole video. */\n" + """  .cite { font-family:"JetBrains Mono",ui-monospace,"SF Mono",Consolas,monospace;\n          font-weight:500; font-size:32px; letter-spacing:.04em;\n          text-transform:none; color:#6B6B6B; border:2px solid #D9D3C6;\n          border-radius:999px; padding:10px 26px; width:max-content;\n          background:#F0EBE1; display:inline-block; }\n""" + ("\n  /* [S6/A-7] same defect as .cite: --accent (#59B8AE) on a light\n"
                   "     generated ground measures 2.17:1 against the 3:1 floor. Same\n"
                   "     suggestedColor as the hand-authored .kicker fix. */\n"
                   "  .kicker { color:#4B9B93; }\n")
        n_css = int("</style>" in html)
        html = html.replace("</style>", css + "</style>", 1)
        css_subs += n_css

        html, n = re.subn(
            r"(gsap\.set\('#[^']+', \{ clipPath: 'inset\(0 100% 0 0\)')( \}\);)",
            r"\1, y: 22\2", html)
        motion_subs += n
        html, n = re.subn(r"(gsap\.set\('#[^']+', \{ opacity: 0, scale: )1\.12( \}\);)",
                      r"\g<1>1.03, y: -18\2", html)
        motion_subs += n
        html, n = re.subn(r"(tl\.to\('#[^']+', \{ opacity: 1, scale: 1)(, duration[^}]*ease: 'power4\.out')",
                      r"\1, y: 0\2", html)
        motion_subs += n
        html, n = re.subn(
            r"(tl\.to\('#[^']+', \{ clipPath: 'inset\(0 0% 0 0\)')(, duration)",
            r"\1, y: 0\2", html)
        motion_subs += n

        cnt = [0]
        def _drift(m):
            dx, dy, ds = DEFAULT_DRIFTS[cnt[0] % len(DEFAULT_DRIFTS)]; cnt[0] += 1
            return "%sx: %d, y: %d, scale: %s%s" % (m.group(1), dx, dy, ds, m.group(3))
        html, n = re.subn(r"(tl\.to\('#[^']+-stage', \{ )(x: -?[\d.]+, y: -?[\d.]+, scale: [\d.]+)(, duration)",
                      _drift, html)
        motion_subs += n

        open(path, "w").write(html)
        fixed += 1
        # [correctness] v2's zero-substitution guard counted the ALWAYS-
        # succeeding CSS insert alongside the four motion regexes, so it
        # could never actually report 0 even if every motion regex silently
        # stopped matching. Split here: the CSS insert is asserted outright
        # (it is not optional -- every generated scene needs its ground fix),
        # and the motion-regex count is its own separate, honestly-zeroable
        # number, checked against how many wipe/slam/hold beats this scene's
        # own beat sheet actually declares.
        assert n_css == 1, f"{sid}: ground/contrast CSS insert failed -- </style> not found"
        idioms = [b["idiom"] for b in sc["beats"]]
        expected_min = sum(1 for x in idioms if x in ("wipe", "slam", "hold"))
        if expected_min > 0 and motion_subs == 0:
            print(f"  WARNING: fix_generated_grounds made 0 MOTION substitutions on {sid} "
                  f"but its beat sheet declares {expected_min} wipe/slam/hold beat(s) -- "
                  f"the external generator's output format may have changed under this "
                  f"fixer's regexes")
    print("  ground/contrast fix applied to %d generated scene(s), %d CSS + %d motion substitution(s)"
          % (fixed, css_subs, motion_subs))


def fix_motion_sidecar():
    """[S7/R-1b]: set root `keepsMoving.maxStaticSec` from the FORMAT's cadence.
    6.0s for long-form (this repo's own check-cadence.py --longform ceiling),
    not the engine's 2.0s Shorts default."""
    p = f"{HERE}/05-composition/index.motion.json"
    m = json.load(open(p))
    n = 0
    for a in m.get("assertions", []):
        if a.get("kind") == "keepsMoving" and a.get("maxStaticSec") == 2.0:
            a["maxStaticSec"] = 6.0
            a["_note"] = ("re-pointed from the engine's 2s Shorts default per "
                          "[S7/R-1b]; long-form ceiling from check-cadence.py --longform")
            n += 1
    json.dump(m, open(p, "w"), indent=2)
    print("  motion sidecar: %d keepsMoving assertion(s) re-pointed 2.0s -> 6.0s (long-form)" % n)


def main():
    # [correctness] mirror assertion: the old code only asserted BUILD subset
    # DIAGRAM (a BUILD entry not marked hand-authored). It never caught the
    # OTHER direction -- a DIAGRAM id with no BUILD function, which falls
    # through to the generator's own warning or, worse, an untouched stale
    # file. Both directions checked now.
    diagram_ids = {sid for sid in ORDER if SCENES[sid]["handoff"] == "hand-authored"}
    missing_builders = diagram_ids - set(BUILD)
    extra_builders = set(BUILD) - diagram_ids
    assert not missing_builders, f"hand-authored in beat sheet but no BUILD function: {missing_builders}"
    assert not extra_builders, f"BUILD function exists but not hand-authored in beat sheet: {extra_builders}"

    n = 0
    written = set()
    for sid, fn in BUILD.items():
        idx = ORDER.index(sid) + 1
        path = f"{OUT}/{idx:02d}-{sid}.html"
        open(path, "w").write(fn())
        written.add(os.path.basename(path))
        n += 1
        print("  wrote %-40s  %5.1fs  %2d beats"
              % (os.path.basename(path), SCENES[sid]["duration"], len(SCENES[sid]["beats"])))
    print("%d hand-authored scenes emitted" % n)
    fix_generated_grounds()
    fix_motion_sidecar()

    # Stale-file guard: neither generator deletes anything from
    # compositions/frames/. A scene id that changed between runs (as every
    # id in this project did, going from 13 scenes to 17) leaves its old file
    # behind, un-referenced by index.html but sitting on disk. `main()` here
    # only WROTE the hand-authored ones above; add the two generated ones the
    # shared generator itself wrote, then compare against everything present.
    generated = {f"{ORDER.index(sid)+1:02d}-{sid}.html"
                 for sid in ORDER if SCENES[sid]["handoff"] == "generated"}
    expected = written | generated
    present = {f for f in os.listdir(OUT) if f.endswith(".html")}
    stale = present - expected
    if stale:
        print(f"  WARNING: {len(stale)} stale file(s) in {OUT}, not part of this run: "
              f"{sorted(stale)} -- delete them (a prior run's scene ids no longer used)")

if __name__ == "__main__":
    main()
