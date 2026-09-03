#!/usr/bin/env python3
"""Emit the five DIAGRAM scenes -- the ones carrying the morphology actor.

These are marked `handoff: "hand-authored"` in the beat sheet, so the skill's
generator emits their clip, transition and motion assertions but NOT their
markup [S6/A-9]. This writes that markup, still reading every time from
03-beat-sheet.json: no timing is hand-typed here either.

The actor is one molecule in three physical states, and that IS the video's
argument:
    ha-body    long free coils, dispersed, water caught in the loops
    ha-serum   the same chains in two sizes meeting a skin boundary
    ha-filler  the same chains cross-linked into a lattice that holds shape

DETERMINISM: every coordinate is computed HERE, in Python, with a fixed seed and
baked into static SVG path data. Nothing random, timed or measured runs inside
the composition -- the renderer seeks, it does not play.

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
IDIOM_EASE = {"arrive": "power3.out", "slam": "power4.out", "wipe": "power2.inOut",
              "count": "power2.out", "swap": "back.out(1.6)", "hold": "sine.inOut"}

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

# ------------------------------------------------------------- v2 geometry --
# Added for the v2 revision's ten named visuals. Same discipline as the block
# above: deterministic, seeded, static SVG path data computed here in Python.

def skin_band(w, h, boundary_frac=0.30):
    """A two-layer skin cross-section: a thin epidermis band over a deeper
    dermis, with a gently wavy surface line. Reused by every scene that needs
    an honest (labelled) skin cross-section rather than a flat backdrop."""
    by = h * boundary_frac
    # wavy surface, low-amplitude, deterministic (no rng — it is a fixed motif)
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
    rng = random.Random(1934)
    # the eye: almond outline via two symmetric arcs, iris circle, three
    # short lash strokes -- the "tasteful, elegant" 1930s-plate register
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
    # the flask: Erlenmeyer outline, a liquid fill, and a stopper -- lab
    # glassware, not medical equipment; nothing pierces anything.
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
    rng = random.Random(2024)
    tray = '<rect x="20" y="180" width="480" height="18" rx="9" fill="none" stroke="currentColor" stroke-width="5"/>'
    # capped syringe, lying flat on the tray -- barrel + plunger + a CAPPED tip
    syringe = (
        '<g transform="translate(60,120)">'
        '<rect x="0" y="0" width="220" height="34" rx="8" fill="none" stroke="currentColor" stroke-width="5"/>'
        '<line x1="30" y1="0" x2="30" y2="34" stroke="currentColor" stroke-width="3" opacity="0.5"/>'
        '<line x1="60" y1="0" x2="60" y2="34" stroke="currentColor" stroke-width="3" opacity="0.5"/>'
        '<rect x="-46" y="8" width="46" height="18" rx="6" fill="none" stroke="currentColor" stroke-width="5"/>'
        '<rect x="220" y="10" width="34" height="14" rx="4" fill="currentColor" opacity="0.35"/>'  # cap, sealed
        '</g>'
    )
    vial = ('<g transform="translate(340,90)">'
            '<rect x="0" y="0" width="46" height="72" rx="8" fill="none" stroke="currentColor" stroke-width="5"/>'
            '<rect x="6" y="30" width="34" height="34" fill="currentColor" opacity="0.16"/>'
            '<rect x="10" y="-10" width="26" height="12" rx="3" fill="currentColor" opacity="0.5"/>'
            '</g>')
    # a gloved hand resting beside the tray: a simple rounded mitten shape,
    # never touching the syringe tip -- calm, not mid-procedure.
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

def scene_shell(sid, css_extra, markup, sets, tweens):
    sc = SCENES[sid]; dur = sc["duration"]
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
         f'     data-duration="{dur:.3f}">',
         f'  <div class="clip stage" id="{sid}-stage" data-start="0" data-duration="{dur:.3f}">',
         markup, "  </div>", "</div>", "<script>", "(function () {"]
    for x in sets: s.append("  " + x)
    s.append("  // No timeline `defaults: { ease }` — an inherited ease is an uncounted")
    s.append("  // one, and that is how a project ships a single entrance signature.")
    s.append("  var tl = gsap.timeline({ paused: true });")
    for x in tweens: s.append("  " + x)
    s.append(f"  tl.to({{}}, {{ duration: {dur:.3f}, ease: 'none' }}, 0);   // anchor — last, at 0")
    s.append("  window.__timelines = window.__timelines || {};")
    s.append(f"  window.__timelines['{sid}'] = tl;")
    s += ["})();", "</script>", "</template>", ""]
    return "\n".join(s)

def beats_of(sid):
    return SCENES[sid]["beats"]

def txt(b):
    return esc(b.get("text", b.get("intent", "")))

# ---------------------------------------------------------- lineup / badges --
# Layout is a FLEX COLUMN: title, then the three lanes, then the payoff copy.
# The earlier version floated the copy absolutely over the lanes and produced a
# real `content_overlap` error (#lab0 "IN YOUR BODY" under #k "Same name" at
# 9.0s, 16 occurrences). Nothing here is absolutely positioned.
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
  /* [S7/R-2] measured: 440px + the foot's 76px punchline left only ~20px
     clearance -- check flagged content_overlap between the lane0 label and
     the foot head at their closest approach. 380px restores real clearance. */
  .lane .actor { height:380px; width:auto; max-width:100%; flex:0 0 auto; }
  /* Absolutely positioned so the icon adds ZERO height to the lane's flex
     budget -- v1's proven 440px-actor layout already fills the available
     798px column exactly; anything added in-flow overflows into .foot. */
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

    # Only a beat at offset 0 may be rendered as the composed title. A later
    # beat painted from scene start APPEARS before every earlier beat, which is
    # exactly the motion_out_of_order `check` caught on s13-badges-b3.
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
        # [visual #1] category icon above the molecule actor: a bottle, a body
        # silhouette, a syringe -- the three CATEGORIES, composed at rest
        # alongside the existing molecular-form diagram, not replacing it.
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
    # Frame zero is a DESIGN OBJECT [S6/A-3] and the thumbnail candidate: ALL
    # THREE lanes are composed at t=0, because the lineup is the hook. They rest
    # slightly de-emphasised and each is brought forward on its own beat, so the
    # opening frame is complete and the motion still tracks the narration.
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
        tw.insert(0, f"tl.to('#{sid}-stage', {{ scale: 1.014, y: -7, duration: 1.500, "
                     f"ease: 'sine.inOut' }}, 0.150);")
        tw.insert(1, f"tl.to('#{sid}-stage', {{ scale: 1.0, y: 0, duration: 1.200, "
                     f"ease: 'sine.inOut' }}, 1.700);")
    LDRIFT = [(8, -6, 1.012), (-7, 5, 1.004), (6, 6, 1.009), (-5, -5, 1.006)]
    for n_, b in enumerate([x for x in beats if x["idiom"] == "hold"]):
        dx, dy, ds = LDRIFT[n_ % len(LDRIFT)]
        tw.append(f"tl.to('#{sid}-stage', {{ x: {dx}, y: {dy}, scale: {ds}, "
                  f"duration: {b['dur']:.3f}, ease: 'sine.inOut' }}, {b['offset']:.3f});")
    return scene_shell(sid, LANE_CSS, markup, sets, tw)

def build_lineup():
    return lane_scene("s01-lineup", icons=(icon_body, icon_bottle, icon_syringe))
def build_badges(): return lane_scene("s12-badges", badge_roles=True)

# ------------------------------------------------- 05 / 06 / 10 : two-column --
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
    """Copy left, the morphology actor right. The panel is what MOVES."""
    b = beats_of(sid)
    rows = []
    for i, bt in enumerate(b):
        if bt["idiom"] == "hold":
            continue
        role = bt.get("role", "body")
        cls = {"head": "head", "sub": "sub", "body": "body", "caption": "caption",
               "cite": "cite", "kicker": "kicker", "stat": "stat"}.get(role, "body")
        rows.append(f'        <div class="{cls} beat is-entering" id="{sid}-b{i}">{txt(bt)}</div>')
    markup = ('    <div class="two">\n'
              f'      <div class="col" id="{sid}-col">\n' + "\n".join(rows) + "\n      </div>\n"
              f'      <div class="panel{" on" if panel_on else ""}" id="{sid}-panel">\n'
              f'        {actor_svg(kind)}\n'
              "      </div>\n"
              "    </div>")
    sets, tw, drift = [], [], 0
    DRIFTS = [(10, -7, 1.018), (-9, 6, 1.005), (7, 8, 1.014), (-6, -6, 1.010)]
    sets.append(f"gsap.set('#{sid}-panel', {{ opacity: 0, x: 60, scale: 0.94 }});")
    tw.append(f"tl.to('#{sid}-panel', {{ opacity: 1, x: 0, scale: 1, duration: 1.300, ease: 'power2.inOut' }}, 0.001);")
    for i, bt in enumerate(b):
        if bt["idiom"] == "hold":
            # a hold moves the PANEL, not a text line: panel-scale motion is what
            # actually reads on a 1920-wide frame [ectoin: a text fade is ~0.7%].
            dx, dy, ds = DRIFTS[drift % len(DRIFTS)]; drift += 1
            tw.append(f"tl.to('#{sid}-panel', {{ x: {dx}, y: {dy}, scale: {ds}, "
                      f"duration: {bt['dur']:.3f}, ease: 'sine.inOut' }}, {bt['offset']:.3f});")
            continue
        ease = IDIOM_EASE[bt["idiom"]]
        off, d = bt["offset"], bt["dur"]
        if bt["idiom"] == "wipe":
            sets.append(f"gsap.set('#{sid}-b{i}', {{ clipPath: 'inset(0 100% 0 0)', opacity: 1, y: 22 }});")
            tw.append(f"tl.to('#{sid}-b{i}', {{ clipPath: 'inset(0 0% 0 0)', y: 0, duration: {d:.3f}, ease: '{ease}' }}, {off:.3f});")
        elif bt["idiom"] == "swap":
            sets.append(f"gsap.set('#{sid}-b{i}', {{ opacity: 0, scale: 0.86 }});")
            tw.append(f"tl.to('#{sid}-b{i}', {{ opacity: 1, scale: 1, duration: {d:.3f}, ease: '{ease}' }}, {off:.3f});")
            # a swap also re-states the panel: the same actor, newly emphasised
            tw.append(f"tl.to('#{sid}-panel', {{ scale: 1.05, duration: {d:.3f}, ease: '{ease}' }}, {off:.3f});")
        elif bt["idiom"] == "slam":
            sets.append(f"gsap.set('#{sid}-b{i}', {{ opacity: 0, scale: 1.03, y: -18 }});")
            tw.append(f"tl.to('#{sid}-b{i}', {{ opacity: 1, scale: 1, y: 0, duration: {d:.3f}, ease: '{ease}' }}, {off:.3f});")
        else:
            sets.append(f"gsap.set('#{sid}-b{i}', {{ opacity: 0, y: 30 }});")
            tw.append(f"tl.to('#{sid}-b{i}', {{ opacity: 1, y: 0, duration: {d:.3f}, ease: '{ease}' }}, {off:.3f});")
    return scene_shell(sid, TWOCOL_CSS, markup, sets, tw)


# ------------------------------------------------------- v2 bespoke scenes --
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

def _row_tweens(sid, rows_used):
    """Shared enter-tween pass matching two_col()'s idiom handling, reused by
    every bespoke hero-left/split scene so beats behave identically everywhere."""
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

def _hold_drift(sid, target_sel):
    sets, tw = [], []
    DRIFTS = [(10, -7, 1.018), (-9, 6, 1.005), (7, 8, 1.014), (-6, -6, 1.010)]
    drift = 0
    for bt in beats_of(sid):
        if bt["idiom"] != "hold": continue
        dx, dy, ds = DRIFTS[drift % len(DRIFTS)]; drift += 1
        tw.append(f"tl.to('{target_sel}', {{ x: {dx}, y: {dy}, scale: {ds}, "
                  f"duration: {bt['dur']:.3f}, ease: 'sine.inOut' }}, {bt['offset']:.3f});")
    return sets, tw

HEROSPLIT_CSS = """
  .split2 { display:grid; grid-template-columns: 1fr 560px; gap:80px; width:100%;
            align-items:center; }
  .col { display:flex; flex-direction:column; gap:26px; }
  .panel { position:relative; display:flex; align-items:center; justify-content:center;
           border:2px solid var(--rule-strong); border-radius:16px; padding:18px;
           background:rgba(0,0,0,0.015); }
  .panel .actor { color:var(--ink); }
"""

def _hero_left(sid, panel_markup, panel_setup_sets=None, panel_extra_tweens=None):
    """head/sub/body/caption/cite text in a left column, one illustration
    panel on the right. The shared shape behind s03/s04/s08/s09."""
    rows = _rows(sid)
    markup = ('    <div class="split2">\n'
              f'      <div class="col" id="{sid}-col">\n'
              + "\n".join(r[2] for r in rows) + "\n      </div>\n"
              f'      <div class="panel" id="{sid}-panel">\n'
              f'        {panel_markup}\n'
              "      </div>\n"
              "    </div>")
    sets = [f"gsap.set('#{sid}-panel', {{ opacity: 0, x: 60, scale: 0.94 }});"]
    tw = [f"tl.to('#{sid}-panel', {{ opacity: 1, x: 0, scale: 1, duration: 1.300, ease: 'power2.inOut' }}, 0.001);"]
    if panel_setup_sets: sets += panel_setup_sets
    if panel_extra_tweens: tw += panel_extra_tweens
    rs, rt = _row_tweens(sid, rows); sets += rs; tw += rt
    hs, ht = _hold_drift(sid, f"#{sid}-panel"); sets += hs; tw += ht
    return scene_shell(sid, HEROSPLIT_CSS, markup, sets, tw)

# ---- s03-origin: 1934, cow-eye vitreous, drawn in a tasteful 1930s idiom ---
def build_origin():
    return _hero_left("s03-origin", eye_glassware_svg())

# ---- s04-body: natural HA in a skin cross-section, water molecules --------
BODYCROSS_CSS = HEROSPLIT_CSS + """
  .cross { width:100%; height:100%; }
"""
def build_body_cross():
    sid = "s04-body"
    rng = random.Random(11)
    inner = (skin_band(480, 560, boundary_frac=0.22)
             + "\n      " + free_coils(rng, 4, 480, 560, 260, 24, sw=6)
             + "\n      " + water_dots(rng, 20, 480, 560, r=6))
    panel = (f'<svg class="actor cross" viewBox="0 0 480 560" width="480" height="560" '
             f'preserveAspectRatio="xMidYMid meet" aria-hidden="true">\n      {inner}\n    </svg>')
    html = _hero_left(sid, panel)
    return html.replace(HEROSPLIT_CSS, BODYCROSS_CSS, 1) if HEROSPLIT_CSS in html else html

# ---- s05-compare: side-by-side cross-section, serum vs filler -------------
COMPARE_CSS = """
  .cmp-wrap { display:flex; flex-direction:column; gap:22px; width:100%; height:100%; }
  .cmp-lanes { display:grid; grid-template-columns:1fr 1fr; gap:56px; flex:1 1 auto; min-height:0; }
  .cmp-col { display:flex; flex-direction:column; align-items:center; justify-content:center;
             gap:14px; border:2px solid var(--rule-strong); border-radius:16px; padding:20px; }
  .cmp-col.on { border-color:var(--aqua); }
  .cmp-label { font-weight:700; font-size:32px; letter-spacing:.12em;
               text-transform:uppercase; color:var(--ink-2); }
  .cmp-col .actor { color:var(--ink); height:340px; width:auto; }
"""
def build_compare():
    sid = "s05-compare"
    beats = beats_of(sid)
    idx = [i for i, b in enumerate(beats) if b["idiom"] != "hold"]
    head_i = [i for i in idx if beats[i].get("role") == "head"]
    body_i = [i for i in idx if beats[i].get("role") == "body"]
    cite_i = [i for i in idx if beats[i].get("role") == "cite"]

    rng_s, rng_f = random.Random(23), random.Random(37)
    serum_inner = boundary_panel(rng_s, 420, 460)
    serum_svg = (f'<svg class="actor" viewBox="0 0 420 460" width="420" height="460" '
                 f'preserveAspectRatio="xMidYMid meet" aria-hidden="true">\n      {serum_inner}\n    </svg>')
    filler_inner = skin_band(420, 460, boundary_frac=0.20) + "\n      " + lattice(420, 460 - 120, 5, 5, pad=30)
    filler_svg = (f'<svg class="actor" viewBox="0 0 420 460" width="420" height="460" '
                  f'preserveAspectRatio="xMidYMid meet" aria-hidden="true">\n'
                  f'      <g transform="translate(0,120)">{filler_inner}</g>\n'
                  f'      {skin_band(420, 460, boundary_frac=0.20)}\n    </svg>')

    title = ""
    titled = None
    if head_i and abs(beats[head_i[0]]["offset"]) < 1e-6:
        titled = head_i[0]
        title = f'      <h1 class="head beat" id="{sid}-b{titled}">{txt(beats[titled])}</h1>'

    body_rows = []
    for n, i in enumerate(body_i[:1]):
        pass  # left column gets the first body line, right gets the second
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
    for i in idx:
        if i == titled: continue
        b = beats[i]
        sets.append(f"gsap.set('#{sid}-b{i}', {{ opacity: 0, y: 26 }});")
        tw.append(f"tl.to('#{sid}-b{i}', {{ opacity: 1, y: 0, duration: {b['dur']:.3f}, "
                  f"ease: '{IDIOM_EASE[b['idiom']]}' }}, {b['offset']:.3f});")
    hs, ht = _hold_drift(sid, f"#{sid}-colR" ); sets += hs; tw += ht
    return scene_shell(sid, COMPARE_CSS, markup, sets, tw)

# ---- s08-binds-water: HA attracting/holding water, animated droplets ------
def build_binds_water():
    sid = "s08-binds-water"
    rng = random.Random(23)
    chain = f'<path d="{coil(30, 260, 380, 30, 50, rng)}" fill="none" stroke="currentColor" stroke-width="10" stroke-linecap="round"/>'
    # droplets start scattered AWAY from the chain and are pulled toward it
    # on the "It binds water" swap beat -- genuine x/y motion, not a static
    # illustration standing in for the mechanism.
    starts = [(60,60),(380,50),(420,180),(40,420),(400,430),(220,40),(60,340),(430,300)]
    ends   = [(70,230),(150,230),(280,250),(120,300),(320,280),(200,220),(90,270),(340,240)]
    drops = []
    for i, (sx, sy) in enumerate(starts):
        drops.append(water_drop(sx, sy, r=9, eid=f"{sid}-drop{i}"))
    panel = (f'<svg class="actor" viewBox="0 0 460 460" width="460" height="460" '
             f'preserveAspectRatio="xMidYMid meet" aria-hidden="true">\n'
             f'      {chain}\n      ' + "\n      ".join(drops) + '\n    </svg>')

    beats = beats_of(sid)
    idx = [i for i, b in enumerate(beats) if b["idiom"] != "hold"]
    swap_i = [i for i in idx if beats[i]["idiom"] == "swap"]
    swap_off = beats[swap_i[0]]["offset"] if swap_i else 2.0

    drop_sets, drop_tw = [], []
    for i, ((sx, sy), (ex, ey)) in enumerate(zip(starts, ends)):
        drop_sets.append(f"gsap.set('#{sid}-drop{i}', {{ opacity: 0.35 }});")
        drop_tw.append(f"tl.to('#{sid}-drop{i}', {{ x: {ex-sx}, y: {ey-sy}, opacity: 1, scale: 1.15, "
                       f"duration: 1.400, ease: 'power2.inOut' }}, {swap_off + i*0.05:.3f});")
    return _hero_left(sid, panel, panel_setup_sets=drop_sets, panel_extra_tweens=drop_tw)

# ---- s09-lifeguard: moisturiser seal slowing water loss --------------------
def build_lifeguard():
    sid = "s09-lifeguard"
    rng = random.Random(23)
    band = skin_band(460, 420, boundary_frac=0.55)
    chain = f'<path d="{coil(30, 260, 340, 22, 46, rng)}" fill="none" stroke="currentColor" stroke-width="8" stroke-linecap="round"/>'
    seal = ('<path d="M20 150 Q230 110 440 150 L440 175 Q230 140 20 175 Z" '
            'fill="currentColor" opacity="0.14"/>'
            '<text x="20" y="130" font-size="22" fill="currentColor" opacity="0.6" '
            'style="font-family:var(--font-mono)">MOISTURISER — SLOWS WATER LOSS</text>')
    panel = (f'<svg class="actor" viewBox="0 0 460 420" width="460" height="420" '
             f'preserveAspectRatio="xMidYMid meet" aria-hidden="true">\n'
             f'      {band}\n      {chain}\n      {seal}\n    </svg>')
    return _hero_left(sid, panel)

# ---- s10-crosslink: loose chains TRANSFORM into a connected grid ----------
def build_crosslink_transform():
    sid = "s10-crosslink"
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

# ---- s11-do-not-inject: clinical vignette, then the full-bleed warning ----
WARNING_CSS = """
  .warn-wrap { display:flex; flex-direction:column; gap:34px; width:100%; height:100%;
               justify-content:center; }
  .warn-top { display:flex; align-items:center; gap:48px; }
  .warn-top .actor { color:var(--ink); height:220px; width:auto; opacity:0.9; }
  .warn-head { font-family:var(--font-display); font-weight:600; font-size:132px;
               line-height:0.98; letter-spacing:-.01em; color:var(--coral); margin:0; }
"""
def build_warning():
    sid = "s11-do-not-inject"
    beats = beats_of(sid)
    idx = [i for i, b in enumerate(beats) if b["idiom"] != "hold"]
    by_role = {r: [i for i in idx if beats[i].get("role") == r]
               for r in ("caption","kicker","head","cite","body","sub")}

    vign = clinical_vignette_svg()
    cap_i = by_role["caption"][0] if by_role["caption"] else None
    kick_i = by_role["kicker"][0] if by_role["kicker"] else None
    top = (f'      <div class="warn-top" id="{sid}-top">\n'
           f'        {vign}\n'
           '        <div class="col" style="gap:18px">\n'
           + (f'          <div class="caption beat is-entering" id="{sid}-b{cap_i}">{txt(beats[cap_i])}</div>\n' if cap_i is not None else '')
           + (f'          <div class="kicker beat is-entering" id="{sid}-b{kick_i}">{txt(beats[kick_i])}</div>\n' if kick_i is not None else '')
           + '        </div>\n      </div>')

    head_i = by_role["head"][0] if by_role["head"] else None
    cite_i = by_role["cite"][0] if by_role["cite"] else None
    body_rows = "\n".join(f'      <div class="body beat is-entering" id="{sid}-b{i}">{txt(beats[i])}</div>'
                          for i in by_role["body"])
    sub_rows = "\n".join(f'      <div class="sub beat is-entering" id="{sid}-b{i}">{txt(beats[i])}</div>'
                         for i in by_role["sub"])
    head_md = (f'      <h1 class="warn-head beat is-entering" id="{sid}-b{head_i}">{txt(beats[head_i])}</h1>'
              if head_i is not None else "")
    cite_md = (f'      <div class="cite beat is-entering" id="{sid}-b{cite_i}">{txt(beats[cite_i])}</div>'
              if cite_i is not None else "")

    markup = ('    <div class="warn-wrap">\n' + top + '\n' + head_md + '\n' + cite_md
              + '\n' + body_rows + '\n' + sub_rows + '\n    </div>')

    # #top itself is static (always opacity 1) -- only the vignette
    # illustration it wraps; the caption/kicker inside it get their own
    # tweens below like every other beat, so each keeps its own timing.
    sets, tw = [], []
    for i in idx:
        b = beats[i]
        ease = IDIOM_EASE[b["idiom"]]; off, d = b["offset"], b["dur"]
        if b["idiom"] == "slam":
            sets.append(f"gsap.set('#{sid}-b{i}', {{ opacity: 0, scale: 1.06, y: -18 }});")
            tw.append(f"tl.to('#{sid}-b{i}', {{ opacity: 1, scale: 1, y: 0, duration: {d:.3f}, ease: '{ease}' }}, {off:.3f});")
        elif b["idiom"] == "wipe":
            sets.append(f"gsap.set('#{sid}-b{i}', {{ clipPath: 'inset(0 100% 0 0)', opacity: 1, y: 22 }});")
            tw.append(f"tl.to('#{sid}-b{i}', {{ clipPath: 'inset(0 0% 0 0)', y: 0, duration: {d:.3f}, ease: '{ease}' }}, {off:.3f});")
        else:
            sets.append(f"gsap.set('#{sid}-b{i}', {{ opacity: 0, y: 30 }});")
            tw.append(f"tl.to('#{sid}-b{i}', {{ opacity: 1, y: 0, duration: {d:.3f}, ease: '{ease}' }}, {off:.3f});")
    hs, ht = _hold_drift(sid, f"#{sid}-stage"); sets += hs; tw += ht
    return scene_shell(sid, HEROSPLIT_CSS + WARNING_CSS, markup, sets, tw)

BUILD = {
  "s01-lineup":       build_lineup,
  "s12-badges":       build_badges,
  "s03-origin":       build_origin,
  "s04-body":         build_body_cross,
  "s05-compare":       build_compare,
  "s06-serum-size":   lambda: two_col("s06-serum-size", "serum", panel_on=True),
  "s08-binds-water":  build_binds_water,
  "s09-lifeguard":    build_lifeguard,
  "s10-crosslink":    build_crosslink_transform,
  "s11-do-not-inject":build_warning,
}

def fix_generated_grounds():
    """Mechanical [S7/R-1] fix on the GENERATED scenes.

    The generator sets `--ink: #131516` on #root and then paints #root with the
    scene's own `bg`. On a dark ground that is ink text on ink: `check` measured
    1:1 on #s04-named-b0 and -b2 -- literally invisible copy, not merely
    low-contrast. Every dark generated scene has it.

    Also swaps the citation chip's accent on light grounds: #59B8AE on #F7F5F0
    measured 2.17:1 against a 3:1 requirement, and rgb(75,155,147) is `check`'s
    own suggestedColor in the same palette direction [S6/A-7].
    """
    fixed = 0
    for i, sid in enumerate(ORDER, start=1):
        sc = SCENES[sid]
        if sc["handoff"] != "generated":
            continue
        path = f"{OUT}/{i:02d}-{sid}.html"
        html = open(path).read()
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
        html = html.replace("</style>", css + "</style>", 1)

        # A `wipe` beat emits a clipPath-ONLY tween. clipPath changes what is
        # painted but NOT the bounding-box geometry the motion pass samples, so
        # a stretch of consecutive wipes reads as frozen: `check` measured 9.03s
        # static across s12-do-not-inject, whose tail is three wipes and nothing
        # else. Pair every reveal with a short travel on the same element -- it
        # satisfies the gate because it is genuinely more motion, not less.
        html = re.sub(
            r"(gsap\.set\('#[^']+', \{ clipPath: 'inset\(0 100% 0 0\)')( \}\);)",
            r"\1, y: 22\2", html)
        # slam: scale 1.12 -> 1.03 plus a vertical drop
        html = re.sub(r"(gsap\.set\('#[^']+', \{ opacity: 0, scale: )1\.12( \}\);)",
                      r"\g<1>1.03, y: -18\2", html)
        html = re.sub(r"(tl\.to\('#[^']+', \{ opacity: 1, scale: 1)(, duration[^}]*ease: 'power4\.out')",
                      r"\1, y: 0\2", html)
        html = re.sub(
            r"(tl\.to\('#[^']+', \{ clipPath: 'inset\(0 0% 0 0\)')(, duration)",
            r"\1, y: 0\2", html)

        # And alternate the `hold` drift: identical targets mean every hold after
        # the first tweens to where the element already sits -- zero movement.
        drifts = [(10, -7, 1.018), (-9, 6, 1.005), (7, 8, 1.014), (-6, -6, 1.010)]
        cnt = [0]
        def _drift(m):
            dx, dy, ds = drifts[cnt[0] % len(drifts)]; cnt[0] += 1
            return "%sx: %d, y: %d, scale: %s%s" % (m.group(1), dx, dy, ds, m.group(3))
        html = re.sub(r"(tl\.to\('#[^']+-stage', \{ )(x: -?[\d.]+, y: -?[\d.]+, scale: [\d.]+)(, duration)",
                      _drift, html)

        open(path, "w").write(html)
        fixed += 1
    print("  ground/contrast fix applied to %d generated scene(s)" % fixed)


def fix_motion_sidecar():
    """[S7/R-1b]: set root `keepsMoving.maxStaticSec` from the FORMAT's cadence.

    R-1b is explicit that the engine's 2s default "is a Shorts number" and must
    be re-pointed per format. The generator emits 2.0, which asks a 180s
    long-form piece for a geometric change every two seconds -- a Shorts
    cadence. The repo's own long-form authority disagrees with 2.0 in both
    directions: youtube-delivery.md sets long-form cadence at "every 8-12s",
    and catalog/tooling/check-cadence.py raises QUIET_CEILING_S from 1.6 to
    **6.0** under --longform.

    So: 6.0 here, and the strict perceptibility answer still comes from
    check-cadence.py --longform on the SHIPPED MP4 at [S7/R-2], which is the
    rule's own stated authority ("a source-level cadence measurement is an
    authoring-time aid, never a substitute for the post-render pixel diff").
    Loosening the authoring proxy does not loosen the gate that actually counts.
    """
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
    n = 0
    for sid, fn in BUILD.items():
        assert SCENES[sid]["handoff"] == "hand-authored", \
            f"{sid} is not marked hand-authored in the beat sheet"
        idx = ORDER.index(sid) + 1
        path = f"{OUT}/{idx:02d}-{sid}.html"
        open(path, "w").write(fn())
        n += 1
        print("  wrote %-34s  %5.1fs  %2d beats"
              % (os.path.basename(path), SCENES[sid]["duration"], len(SCENES[sid]["beats"])))
    print("%d diagram scenes emitted (morphology actor: body / serum / filler)" % n)
    fix_generated_grounds()
    fix_motion_sidecar()

if __name__ == "__main__":
    main()
