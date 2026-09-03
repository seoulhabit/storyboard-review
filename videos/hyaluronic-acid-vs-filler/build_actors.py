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
  .kicker { font-weight:700; font-size:34px; letter-spacing:.16em;
            text-transform:uppercase; color:var(--aqua); }
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
              justify-content:space-between; gap:18px; }
  .lanes { display:grid; grid-template-columns:1fr 1fr 1fr; gap:0;
           width:100%; flex:0 1 auto; min-height:0; align-items:center;
           overflow:hidden; }
  .lane { display:flex; flex-direction:column; align-items:center; gap:16px;
          padding:0 26px; position:relative; height:100%; justify-content:center; }
  .lane + .lane::before { content:""; position:absolute; left:0; top:8%;
          bottom:8%; width:2px; background:var(--rule-strong); }
  .lane .actor { height:440px; width:auto; max-width:100%; flex:0 0 auto; }
  .lane-copy { font-weight:700; font-size:34px; letter-spacing:.12em;
               text-transform:uppercase; color:var(--ink-2); text-align:center; }
  .badge { font-weight:700; font-size:34px; letter-spacing:.10em;
           text-transform:uppercase; color:var(--ink); border:2px solid var(--ink);
           border-radius:999px; padding:8px 22px; text-align:center; }
  .foot { display:flex; align-items:baseline; gap:28px; flex-wrap:wrap; }
"""

def lane_scene(sid, kinds=("body","serum","filler"), badge_roles=False):
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
        lanes.append(f'        <div class="lane" id="{sid}-lane{n}">\n'
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

def build_lineup(): return lane_scene("s01-lineup")
def build_badges(): return lane_scene("s13-badges", badge_roles=True)

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

BUILD = {
  "s01-lineup":     build_lineup,
  "s13-badges":     build_badges,
  "s05-body":       lambda: two_col("s05-body", "body"),
  "s06-serum-size": lambda: two_col("s06-serum-size", "serum", panel_on=True),
  "s10-crosslink":  lambda: two_col("s10-crosslink", "filler"),
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
            css = pad + "\n  /* [K-4] one citation treatment for the whole video. */\n" + """  .cite { font-family:"JetBrains Mono",ui-monospace,"SF Mono",Consolas,monospace;\n          font-weight:500; font-size:32px; letter-spacing:.04em;\n          text-transform:none; color:#6B6B6B; border:2px solid #D9D3C6;\n          border-radius:999px; padding:10px 26px; width:max-content;\n          background:#F0EBE1; display:inline-block; }\n""" + ("\n  /* [S6/A-7] superseded by the pill above; kept for the record:\n"
                   "     this is check's own suggestedColor. */\n"
                   "")
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
