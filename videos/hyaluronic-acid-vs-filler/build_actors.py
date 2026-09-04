#!/usr/bin/env python3
"""Emit the ten DIAGRAM scenes -- the ones carrying the morphology actor.

These are marked `handoff: "hand-authored"` in the beat sheet, so the skill's
generator emits their clip, transition and motion assertions but NOT their
markup [S6/A-9]. This writes that markup, still reading every time from
03-beat-sheet.json: no timing is hand-typed here either.

v3 RETENTION CUT (2026-09-04): rewritten from v2's five-scene version for one
reason, found by grepping the shipped v2 composition rather than assumed: v2
had 27 container-level x/y/scale drift tweens and ZERO tweens on any actor
sub-element (no chain, no water dot, no lattice node ever moved on its own).
The three actors were baked static plates the whole video only ever panned or
zoomed. This version keeps the actors themselves static-and-deterministic
(same seeded geometry, so continuity-audit still reports zero rebuilt-actor
pairs) but animates their SUB-ELEMENTS -- individual chains, individual water
dots, individual lattice nodes -- so each diagram scene's motion IS the
mechanism it is narrating, not a camera move over an unchanging picture:

    s01-thesis      three actors composed together, then a "SERUM =/= FILLER"
                    snap-highlight -- the hook's whole argument in one frame
    s02-identities  the same three actors, each named as its lane brightens
    s04-split       free chains (gentle idle drift) beside a mesh that LOCKS
                    into place -- the categorical contrast, before either
                    mechanism scene explains why
    s05-size        big chains decelerate and stop above the skin boundary;
                    small chains cross below it -- literally what "large
                    stays, small may travel" means, not just said over a
                    static picture
    s06-plumping    the same serum actor (reused, not redrawn) -- the
                    near-surface chains swell briefly then settle, because
                    the hedge in the VO is "temporarily"
    s07-binds       water dots translate onto a free chain and bind (kept
                    from v2, which already did this correctly)
    s08-seals       continuing from s07's bound state: without a sealing
                    step, a subset of the bound water detaches and drifts
                    away
    s09-crosslink   loose chains fade as lattice NODES pop in individually,
                    staggered, rather than the whole net cross-fading in as
                    one flat block -- the assembly is the point
    s10-origin      1934 count-up + the eye/flask illustration (kept from
                    v1/v2, already a genuine value-driven animation)
    s13-badges      the SAME lineup actors from s01/s02, brought back
                    (rearranged, never redrawn) for the three-badge recap

DETERMINISM: every coordinate is computed HERE, in Python, with a fixed seed
and baked into static SVG path data. Nothing random, timed or measured runs
inside the composition -- the renderer seeks, it does not play. The seeded
actor geometry (`actor_svg`, seeds 11/23/37) is unchanged from v1/v2 so a
reused actor is pixel-identical wherever it reappears.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
BS = json.load(open(f"{HERE}/03-beat-sheet.json"))
OUT = f"{HERE}/05-composition/compositions/frames"
SCENES = {s["id"]: s for s in BS["scenes"]}
ORDER = [s["id"] for s in BS["scenes"]]
IDIOM_EASE = {"arrive": "power3.out", "slam": "power4.out", "wipe": "power2.inOut",
              "count": "power2.out", "swap": "back.out(1.6)", "hold": "sine.inOut"}
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

def free_coils(rng, n, w, h, length, amp, sw=7, id_prefix=None):
    """Dispersed free chains — the body state. If id_prefix is given, each
    chain gets its own id (id_prefix + index) so a caller can animate chains
    individually rather than only as one group."""
    out = []
    for i in range(n):
        x = rng.uniform(10, max(12, w - length - 10))
        y = rng.uniform(40, h - 40)
        idattr = f' id="{id_prefix}{i}"' if id_prefix else ""
        out.append(f'<path{idattr} d="{coil(x, y, length, amp, 46, rng)}" fill="none" '
                   f'stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" opacity="0.9"/>')
    return "\n      ".join(out)

def water_dots(rng, n, w, h, r=7, id_prefix=None):
    out = []
    for i in range(n):
        idattr = f' id="{id_prefix}{i}"' if id_prefix else ""
        out.append(f'<circle{idattr} cx="{rng.uniform(20, w-20):.1f}" cy="{rng.uniform(20, h-20):.1f}" '
                   f'r="{r}" fill="currentColor" opacity="0.28"/>')
    return "\n      ".join(out)

def lattice(w, h, cols, rows, pad=40, node_id_prefix=None):
    """Cross-linked net — the filler state. Nodes plus the struts between them.
    If node_id_prefix is given, each node circle gets its own id (in row-major
    order) so a caller can stagger them individually instead of only fading
    the whole net group at once."""
    xs = [pad + i * (w - 2*pad) / (cols - 1) for i in range(cols)]
    ys = [pad + j * (h - 2*pad) / (rows - 1) for j in range(rows)]
    seg, nod = [], []
    k = 0
    for j, y in enumerate(ys):
        for i, x in enumerate(xs):
            if i < cols - 1:
                seg.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{xs[i+1]:.1f}" y2="{y:.1f}"/>')
            if j < rows - 1:
                seg.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{ys[j+1]:.1f}"/>')
            if i < cols - 1 and j < rows - 1:   # the cross-links themselves
                seg.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{xs[i+1]:.1f}" y2="{ys[j+1]:.1f}" '
                           f'class="xl"/>')
            idattr = f' id="{node_id_prefix}{k}"' if node_id_prefix else ""
            nod.append(f'<circle{idattr} cx="{x:.1f}" cy="{y:.1f}" r="9"/>')
            k += 1
    return ('<g class="net-seg" fill="none" stroke="currentColor" stroke-width="6" '
            'stroke-linecap="round">\n      ' + "\n      ".join(seg) + "\n      </g>\n"
            '      <g class="net-nod" fill="currentColor">\n      ' + "\n      ".join(nod) + "\n      </g>")

def boundary_panel(rng, w, h, big_id_prefix=None, small_id_prefix=None):
    """Two chain sizes meeting a skin boundary — the serum state. Each big and
    small chain can carry its own id so large/small groups can be animated
    both as a group AND (for size/plumping) with per-chain stagger."""
    by = h * 0.46
    big = []
    for i in range(3):
        idattr = f' id="{big_id_prefix}{i}"' if big_id_prefix else ""
        big.append(f'<path{idattr} d="{coil(rng.uniform(20, w*0.45), rng.uniform(60, by-70), w*0.42, 26, 52, rng)}" '
                   f'fill="none" stroke="currentColor" stroke-width="9" stroke-linecap="round"/>')
    small = []
    for i in range(9):
        x = rng.uniform(20, w - 120); y = rng.uniform(by + 40, h - 40)
        idattr = f' id="{small_id_prefix}{i}"' if small_id_prefix else ""
        small.append(f'<path{idattr} d="{coil(x, y, 92, 11, 22, rng)}" fill="none" '
                     f'stroke="currentColor" stroke-width="6" stroke-linecap="round"/>')
    return (f'<g class="big" id="{big_id_prefix}grp">\n      ' + "\n      ".join(big) + "\n      </g>\n"
            f'      <line class="skin" x1="0" y1="{by:.1f}" x2="{w}" y2="{by:.1f}" '
            f'stroke="currentColor" stroke-width="4" stroke-dasharray="14 10" opacity="0.55"/>\n'
            f'      <g class="small" id="{small_id_prefix}grp">\n      ' + "\n      ".join(small) + "\n      </g>",
            by)

def skin_band(w, h, boundary_frac=0.30):
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
    likeness of a real person or animal in distress."""
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

def actor_svg(kind, cls="", node_ids=False):
    """Same seeded geometry as v1/v2 (seeds 11/23/37) so a reused actor is
    pixel-identical wherever it reappears -- continuity-audit's whole point.
    node_ids=True additionally tags sub-elements with ids for scenes that
    animate individual chains/nodes rather than the actor as one group."""
    rng = random.Random({"body": 11, "serum": 23, "filler": 37}[kind])
    if kind == "body":
        pfx = "chain" if node_ids else None
        wfx = "drop" if node_ids else None
        inner = free_coils(rng, 5, PW, PH, 330, 30, id_prefix=pfx) + "\n      " + water_dots(rng, 26, PW, PH, id_prefix=wfx)
    elif kind == "serum":
        bp, _by = boundary_panel(rng, PW, PH,
                                  big_id_prefix=("big" if node_ids else None),
                                  small_id_prefix=("small" if node_ids else None))
        inner = bp
    else:
        inner = lattice(PW, PH, 6, 7, node_id_prefix=("node" if node_ids else None))
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
            text-transform:uppercase; color:#4B9B93; }
  .stat { font-family:var(--font-display); font-weight:600; font-size:170px; line-height:1; }
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
  .snap { font-family:var(--font-display); font-weight:700; font-size:96px;
          letter-spacing:-.01em; color:var(--coral); text-align:center; width:100%; }
"""

def lane_scene(sid, kinds=("body","serum","filler"), badge_roles=False, icons=None,
               node_ids=False):
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
        if badge_roles and bi is not None:
            lab = (f'<div class="badge beat is-entering" id="{sid}-b{bi}">'
                   f'{txt(beats[bi])}</div>')
        icon = f'<div class="lane-icon">{icons[n]()}</div>' if icons else ""
        lanes.append(f'        <div class="lane" id="{sid}-lane{n}">\n'
                     f'          {icon}\n'
                     f'          {actor_svg(kind, node_ids=node_ids)}\n'
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
        tw.insert(0, f"tl.to('#{sid}-stage', {{ scale: 1.014, y: -7, duration: 1.500, "
                     f"ease: 'sine.inOut' }}, 0.150);")
        tw.insert(1, f"tl.to('#{sid}-stage', {{ scale: 1.0, y: 0, duration: 1.200, "
                     f"ease: 'sine.inOut' }}, 1.700);")
    LDRIFT = [(8, -6, 1.012), (-7, 5, 1.004), (6, 6, 1.009), (-5, -5, 1.006)]
    for n_, b in enumerate([x for x in beats if x["idiom"] == "hold"]):
        dx, dy, ds = LDRIFT[n_ % len(LDRIFT)]
        tw.append(f"tl.to('#{sid}-stage', {{ x: {dx}, y: {dy}, scale: {ds}, "
                  f"duration: {b['dur']:.3f}, ease: 'sine.inOut' }}, {b['offset']:.3f});")
    return sets, tw, markup, lanes

# ---- s01-thesis: all three actors together, then a SERUM =/= FILLER snap --
def build_thesis():
    sid = "s01-thesis"
    beats = beats_of(sid)
    idx = [i for i, b in enumerate(beats) if b["idiom"] != "hold"]
    kick_i = next((i for i in idx if beats[i].get("role") == "kicker"), None)
    head_i = next((i for i in idx if beats[i].get("role") == "head"), None)
    slam_i = next((i for i in idx if beats[i]["idiom"] == "slam"), None)

    lanes = []
    for n, kind in enumerate(("body", "serum", "filler")):
        lanes.append(f'        <div class="lane" id="{sid}-lane{n}">\n'
                     f'          {actor_svg(kind)}\n'
                     f'        </div>')
    kick_md = (f'      <div class="kicker beat is-entering" id="{sid}-b{kick_i}" '
              f'style="text-align:center">{txt(beats[kick_i])}</div>' if kick_i is not None else "")
    head_md = (f'      <h1 class="head beat is-entering" id="{sid}-b{head_i}" '
              f'style="font-size:76px;text-align:center">{txt(beats[head_i])}</h1>' if head_i is not None else "")
    slam_md = (f'      <div class="snap beat is-entering" id="{sid}-b{slam_i}">'
              f'{txt(beats[slam_i])}</div>' if slam_i is not None else "")
    markup = ('    <div class="col-wrap">\n' + kick_md + '\n'
              '      <div class="lanes">\n' + "\n".join(lanes) + '\n      </div>\n'
              '      <div class="foot" style="justify-content:center;width:100%;flex-direction:column;'
              'align-items:center;gap:20px">\n' + head_md + '\n' + slam_md + '\n      </div>\n    </div>')

    sets, tw = [], []
    # Frame zero: all three forms present together, at rest -- the hook's
    # whole argument composed in one frame before a word plays [S6/A-3].
    for n in (0, 1, 2):
        sets.append(f"gsap.set('#{sid}-lane{n}', {{ opacity: 0.55, scale: 0.97 }});")
        tw.append(f"tl.to('#{sid}-lane{n}', {{ opacity: 1, scale: 1, duration: 1.100, "
                  f"ease: 'power2.inOut' }}, {0.10 + n*0.12:.3f});")
    if kick_i is not None:
        sets.append(f"gsap.set('#{sid}-b{kick_i}', {{ opacity: 0, y: 26 }});")
        tw.append(f"tl.to('#{sid}-b{kick_i}', {{ opacity: 1, y: 0, duration: {beats[kick_i]['dur']:.3f}, "
                  f"ease: 'power3.out' }}, {beats[kick_i]['offset']:.3f});")
    if head_i is not None:
        sets.append(f"gsap.set('#{sid}-b{head_i}', {{ clipPath: 'inset(0 100% 0 0)', opacity: 1, y: 22 }});")
        tw.append(f"tl.to('#{sid}-b{head_i}', {{ clipPath: 'inset(0 0% 0 0)', y: 0, "
                  f"duration: {beats[head_i]['dur']:.3f}, ease: 'power2.inOut' }}, {beats[head_i]['offset']:.3f});")
    if slam_i is not None:
        # the snap-highlight: the whole lineup steps back a touch as the
        # verdict lands, so the motion READS as a reveal, not a caption fading in.
        off, d = beats[slam_i]["offset"], beats[slam_i]["dur"]
        sets.append(f"gsap.set('#{sid}-b{slam_i}', {{ opacity: 0, scale: 0.7 }});")
        tw.append(f"tl.to('#{sid}-b{slam_i}', {{ opacity: 1, scale: 1, duration: {d:.3f}, "
                  f"ease: 'back.out(1.8)' }}, {off:.3f});")
        for n in (0, 1, 2):
            tw.append(f"tl.to('#{sid}-lane{n}', {{ scale: 0.90, opacity: 0.5, duration: {d:.3f}, "
                      f"ease: 'power2.out' }}, {off:.3f});")
    return scene_shell(sid, LANE_CSS, markup, sets, tw)

def build_identities():
    sets, tw, markup, _ = lane_scene("s02-identities", icons=(icon_body, icon_bottle, icon_syringe))
    return scene_shell("s02-identities", LANE_CSS, markup, sets, tw)

def build_badges():
    sets, tw, markup, _ = lane_scene("s13-badges", badge_roles=True)
    return scene_shell("s13-badges", LANE_CSS, markup, sets, tw)

# --------------------------------------------------------- shared text col --
ROLE_CLASS_MAP = {"head":"head","sub":"sub","body":"body","caption":"caption",
                   "cite":"cite","kicker":"kicker","stat":"stat"}

def _rows(sid, skip_roles=()):
    out = []
    for i, bt in enumerate(beats_of(sid)):
        if bt["idiom"] == "hold" or bt.get("role") in skip_roles:
            continue
        cls = ROLE_CLASS_MAP.get(bt.get("role","body"), "body")
        out.append((i, bt, f'        <div class="{cls} beat is-entering" id="{sid}-b{i}">{txt(bt)}</div>'))
    return out

def _row_tweens(sid, rows_used):
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
    sets, tw = [], []
    DRIFTS = drifts or DEFAULT_DRIFTS
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

def _hero_left(sid, panel_markup, panel_setup_sets=None, panel_extra_tweens=None, css_extra=""):
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
    return scene_shell(sid, HEROSPLIT_CSS + css_extra, markup, sets, tw)

# ---- s04-split: free chains (idle drift) beside a mesh that LOCKS in -------
SPLIT_CSS = """
  .split-two { display:grid; grid-template-columns: 1fr 1fr; gap:56px; width:100%; height:100%;
               align-items:center; }
  .split-panel { position:relative; display:flex; flex-direction:column; align-items:center;
                 gap:18px; border:2px solid var(--rule-strong); border-radius:16px; padding:24px; }
  .split-panel .actor { color:var(--ink); height:420px; width:auto; }
  .split-panel .caption { font-size:38px; text-align:center; }
  .split-title { grid-column:1/-1; }
"""
def build_split():
    sid = "s04-split"
    beats = beats_of(sid)
    idx = [i for i, b in enumerate(beats) if b["idiom"] != "hold"]
    head_i = next((i for i in idx if beats[i].get("role") == "head"), None)
    cap_i = [i for i in idx if beats[i].get("role") == "caption"]
    left_cap_i = cap_i[0] if len(cap_i) > 0 else None
    right_cap_i = cap_i[1] if len(cap_i) > 1 else None

    rng_l = random.Random(11)
    left_actor = (f'<svg class="actor" viewBox="0 0 420 420" width="420" height="420" '
                  f'preserveAspectRatio="xMidYMid meet" aria-hidden="true">\n      '
                  f'{free_coils(rng_l, 3, 420, 420, 300, 34, sw=9, id_prefix=f"{sid}-lchain")}'
                  f'\n    </svg>')
    net = lattice(420, 420, 5, 6, pad=36, node_id_prefix=f"{sid}-rnode")
    right_actor = (f'<svg class="actor" id="{sid}-rmesh" viewBox="0 0 420 420" width="420" height="420" '
                   f'preserveAspectRatio="xMidYMid meet" aria-hidden="true">\n      {net}\n    </svg>')

    title = (f'      <h1 class="head beat is-entering split-title" id="{sid}-b{head_i}">'
             f'{txt(beats[head_i])}</h1>' if head_i is not None else "")
    left_cap = (f'<div class="caption beat is-entering" id="{sid}-b{left_cap_i}">'
               f'{txt(beats[left_cap_i])}</div>' if left_cap_i is not None else "")
    right_cap = (f'<div class="caption beat is-entering" id="{sid}-b{right_cap_i}">'
                f'{txt(beats[right_cap_i])}</div>' if right_cap_i is not None else "")

    markup = ('    <div class="split-two">\n' + title + '\n'
              f'      <div class="split-panel" id="{sid}-left">\n        {left_actor}\n        {left_cap}\n      </div>\n'
              f'      <div class="split-panel" id="{sid}-right">\n        {right_actor}\n        {right_cap}\n      </div>\n'
              '    </div>')

    sets, tw = [], []
    if head_i is not None:
        sets.append(f"gsap.set('#{sid}-b{head_i}', {{ opacity: 0, y: 30 }});")
        tw.append(f"tl.to('#{sid}-b{head_i}', {{ opacity: 1, y: 0, duration: {beats[head_i]['dur']:.3f}, "
                  f"ease: 'power3.out' }}, {beats[head_i]['offset']:.3f});")
    sets += [f"gsap.set('#{sid}-left', {{ opacity: 0, x: -40 }});",
             f"gsap.set('#{sid}-right', {{ opacity: 0, x: 40 }});",
             f"gsap.set('#{sid}-rmesh', {{ opacity: 0.35, scale: 0.90 }});"]
    tw += [f"tl.to('#{sid}-left', {{ opacity: 1, x: 0, duration: 1.100, ease: 'power2.inOut' }}, 0.001);",
           f"tl.to('#{sid}-right', {{ opacity: 1, x: 0, duration: 1.100, ease: 'power2.inOut' }}, 0.001);"]
    # LEFT: "one stays a loose, flowing molecule" -- each chain gets its own
    # slow, offset undulation, so it reads as flowing rather than a static
    # picture merely fading in. Three chains, three slightly different
    # periods, deliberately not synchronized.
    if left_cap_i is not None:
        off, d = beats[left_cap_i]["offset"], beats[left_cap_i]["dur"]
        sets.append(f"gsap.set('#{sid}-b{left_cap_i}', {{ opacity: 0, y: 24 }});")
        tw.append(f"tl.to('#{sid}-b{left_cap_i}', {{ opacity: 1, y: 0, duration: {d:.3f}, "
                  f"ease: 'power3.out' }}, {off:.3f});")
        for n, (dy1, dy2, dur1) in enumerate([(10, -8, 1.6), (-9, 7, 1.9), (8, -10, 1.7)]):
            tw.append(f"tl.to('#{sid}-lchain{n}', {{ y: {dy1}, rotation: {1 if n%2==0 else -1}, "
                      f"transformOrigin: 'center', duration: {dur1:.3f}, ease: 'sine.inOut' }}, {off:.3f});")
            tw.append(f"tl.to('#{sid}-lchain{n}', {{ y: {dy2}, duration: {dur1+0.3:.3f}, "
                      f"ease: 'sine.inOut' }}, {off+dur1:.3f});")
    # RIGHT: "the other gets locked into a rigid mesh" -- the mesh nodes pop
    # in with a staggered scale-up, a visible ASSEMBLY rather than a fade.
    if right_cap_i is not None:
        off, d = beats[right_cap_i]["offset"], beats[right_cap_i]["dur"]
        sets.append(f"gsap.set('#{sid}-b{right_cap_i}', {{ opacity: 0, y: 24 }});")
        tw.append(f"tl.to('#{sid}-b{right_cap_i}', {{ opacity: 1, y: 0, duration: {d:.3f}, "
                  f"ease: 'power3.out' }}, {off:.3f});")
        tw.append(f"tl.to('#{sid}-rmesh', {{ opacity: 1, scale: 1, duration: 0.700, "
                  f"ease: 'power2.out' }}, {off:.3f});")
        n_nodes = 5 * 6
        stagger_n = 10
        step = list(range(0, n_nodes, max(1, n_nodes // stagger_n)))[:stagger_n]
        for k, node_i in enumerate(step):
            t = off + 0.10 + k * 0.045
            tw.append(f"gsap.set('#{sid}-rnode{node_i}', {{ transformOrigin: 'center', scale: 0.3 }});")
            tw.append(f"tl.to('#{sid}-rnode{node_i}', {{ scale: 1, duration: 0.500, "
                      f"ease: 'back.out(2.2)' }}, {t:.3f});")
    hs, ht = _hold_drift(sid, f"#{sid}-stage"); sets += hs; tw += ht
    return scene_shell(sid, SPLIT_CSS, markup, sets, tw)

# ---- s05-size: big chains stop above the boundary, small cross below it ---
def build_size():
    sid = "s05-size"
    beats = beats_of(sid)
    idx = [i for i, b in enumerate(beats) if b["idiom"] != "hold"]
    body_i = [i for i in idx if beats[i].get("role") == "body"]
    rng = random.Random(23)
    bp, by = boundary_panel(rng, 480, 560, big_id_prefix=f"{sid}-big", small_id_prefix=f"{sid}-small")
    panel = (f'<svg class="actor" viewBox="0 0 480 560" width="480" height="560" '
             f'preserveAspectRatio="xMidYMid meet" aria-hidden="true">\n      {bp}\n    </svg>')

    sets = [f"gsap.set('#{sid}-biggrp', {{ y: -34 }});",
            f"gsap.set('#{sid}-smallgrp', {{ y: -8, opacity: 0.55 }});"]
    tw = []
    # "Large chains mostly stay near the surface" -- the big-chain group
    # eases DOWN toward the boundary and visibly DECELERATES as it arrives,
    # rather than a static picture: motion that IS the claim "stays near".
    if len(body_i) > 0:
        off, d = beats[body_i[0]]["offset"], beats[body_i[0]]["dur"]
        tw.append(f"tl.to('#{sid}-biggrp', {{ y: 0, duration: {d+0.4:.3f}, "
                  f"ease: 'power2.out' }}, {off:.3f});")
    # "Smaller ones may travel farther into the upper layers" -- the small-
    # chain group continues PAST the boundary, further than the big group
    # ever moves -- the size comparison plays out as a literal distance.
    if len(body_i) > 1:
        off, d = beats[body_i[1]]["offset"], beats[body_i[1]]["dur"]
        tw.append(f"tl.to('#{sid}-smallgrp', {{ y: 46, opacity: 1, duration: {d+0.3:.3f}, "
                  f"ease: 'power1.inOut' }}, {off:.3f});")
    rows = _rows(sid)
    rs, rt = _row_tweens(sid, rows); sets += rs; tw += rt
    hs, ht = _hold_drift(sid, f"#{sid}-panel"); sets += hs; tw += ht
    sets.insert(0, f"gsap.set('#{sid}-panel', {{ opacity: 0, x: 60, scale: 0.94 }});")
    tw.insert(0, f"tl.to('#{sid}-panel', {{ opacity: 1, x: 0, scale: 1, duration: 1.300, ease: 'power2.inOut' }}, 0.001);")
    markup = ('    <div class="split2">\n'
              f'      <div class="col" id="{sid}-col">\n' + "\n".join(r[2] for r in rows) + "\n      </div>\n"
              f'      <div class="panel" id="{sid}-panel">\n        {panel}\n      </div>\n    </div>')
    return scene_shell(sid, HEROSPLIT_CSS, markup, sets, tw)

# ---- s06-plumping: same serum actor, near-surface chains swell then settle-
def build_plumping():
    sid = "s06-plumping"
    beats = beats_of(sid)
    rng = random.Random(23)   # SAME seed as s05 -- the actor is REUSED, not redrawn
    bp, by = boundary_panel(rng, 480, 560, small_id_prefix=f"{sid}-small")
    panel = (f'<svg class="actor" viewBox="0 0 480 560" width="480" height="560" '
             f'preserveAspectRatio="xMidYMid meet" aria-hidden="true">\n      {bp}\n    </svg>')

    body_i = [i for i, b in enumerate(beats) if b["idiom"] != "hold" and b.get("role") == "body"]
    sets = [f"gsap.set('#{sid}-smallgrp', {{ transformOrigin: 'center' }});"]
    tw = []
    # "can TEMPORARILY make fine lines appear softer" -- the near-surface
    # chains swell (scale up) and then visibly SETTLE BACK, because the
    # motion itself is the hedge: temporary, not a correction.
    if body_i:
        off, d = beats[body_i[0]]["offset"], beats[body_i[0]]["dur"]
        tw.append(f"tl.to('#{sid}-smallgrp', {{ scale: 1.12, duration: {d*0.55:.3f}, "
                  f"ease: 'power2.out' }}, {off:.3f});")
        tw.append(f"tl.to('#{sid}-smallgrp', {{ scale: 1.0, duration: {d*0.7:.3f}, "
                  f"ease: 'power2.inOut' }}, {off+d*0.55:.3f});")
    rows = _rows(sid)
    rs, rt = _row_tweens(sid, rows); sets += rs; tw += rt
    hs, ht = _hold_drift(sid, f"#{sid}-panel"); sets += hs; tw += ht
    sets.insert(0, f"gsap.set('#{sid}-panel', {{ opacity: 0, x: 60, scale: 0.94 }});")
    tw.insert(0, f"tl.to('#{sid}-panel', {{ opacity: 1, x: 0, scale: 1, duration: 1.300, ease: 'power2.inOut' }}, 0.001);")
    markup = ('    <div class="split2">\n'
              f'      <div class="col" id="{sid}-col">\n' + "\n".join(r[2] for r in rows) + "\n      </div>\n"
              f'      <div class="panel" id="{sid}-panel">\n        {panel}\n      </div>\n    </div>')
    return scene_shell(sid, HEROSPLIT_CSS, markup, sets, tw)

# ---- s07-binds: water dots translate onto a free chain and bind -----------
def build_binds():
    sid = "s07-binds"
    rng = random.Random(23)
    chain = f'<path id="{sid}-chain" d="{coil(30, 260, 380, 30, 50, rng)}" fill="none" stroke="currentColor" stroke-width="10" stroke-linecap="round"/>'
    starts = [(60,60),(380,50),(420,180),(40,420),(400,430),(220,40),(60,340),(430,300)]
    ends   = [(70,230),(150,230),(280,250),(120,300),(320,280),(200,220),(90,270),(340,240)]
    drops = [water_drop(sx, sy, r=9, eid=f"{sid}-drop{i}") for i, (sx, sy) in enumerate(starts)]
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

# ---- s08-seals: continuing the bound state, water leaves without a seal ---
def build_seals():
    sid = "s08-seals"
    rng = random.Random(23)   # SAME seed as s07 -- the chain is the SAME actor
    chain = f'<path id="{sid}-chain" d="{coil(30, 260, 380, 30, 50, rng)}" fill="none" stroke="currentColor" stroke-width="10" stroke-linecap="round"/>'
    # These are the s07 END positions -- water already bound to the chain
    # when this scene opens, so the two scenes read as one continuous event
    # rather than two independent illustrations.
    bound = [(70,230),(150,230),(280,250),(120,300),(320,280),(200,220),(90,270),(340,240)]
    leave = [(30,110),(210,90),(360,150)]   # where three of the eight go
    drops = [water_drop(x, y, r=9, eid=f"{sid}-drop{i}") for i, (x, y) in enumerate(bound)]
    panel = (f'<svg class="actor" viewBox="0 0 460 460" width="460" height="460" '
             f'preserveAspectRatio="xMidYMid meet" aria-hidden="true">\n'
             f'      {chain}\n      ' + "\n      ".join(drops) + '\n    </svg>')

    beats = beats_of(sid)
    idx = [i for i, b in enumerate(beats) if b["idiom"] != "hold"]
    swap_i = [i for i in idx if beats[i]["idiom"] == "swap"]
    off = beats[swap_i[-1]]["offset"] if swap_i else beats[idx[-1]]["offset"]

    sets = [f"gsap.set('#{sid}-drop{i}', {{ opacity: 1 }});" for i in range(len(bound))]
    tw = []
    # "So it doesn't evaporate away" -- WITHOUT a sealing ingredient, three of
    # the eight bound drops detach and drift up and out, fading as they go.
    # The other five stay put: the point is that SOME water is still lost,
    # not that binding does nothing.
    detach_idx = [0, 3, 6]
    for n, di in enumerate(detach_idx):
        sx, sy = bound[di]; ex, ey = leave[n]
        tw.append(f"tl.to('#{sid}-drop{di}', {{ x: {ex-sx}, y: {ey-sy}, opacity: 0, scale: 0.6, "
                  f"duration: 1.500, ease: 'power1.in' }}, {off + n*0.12:.3f});")
    rows = _rows(sid)
    rs, rt = _row_tweens(sid, rows); sets += rs; tw += rt
    hs, ht = _hold_drift(sid, f"#{sid}-panel"); sets += hs; tw += ht
    sets.insert(0, f"gsap.set('#{sid}-panel', {{ opacity: 0, x: 60, scale: 0.94 }});")
    tw.insert(0, f"tl.to('#{sid}-panel', {{ opacity: 1, x: 0, scale: 1, duration: 1.300, ease: 'power2.inOut' }}, 0.001);")
    markup = ('    <div class="split2">\n'
              f'      <div class="col" id="{sid}-col">\n' + "\n".join(r[2] for r in rows) + "\n      </div>\n"
              f'      <div class="panel" id="{sid}-panel">\n        {panel}\n      </div>\n    </div>')
    return scene_shell(sid, HEROSPLIT_CSS, markup, sets, tw)

# ---- s09-crosslink: loose chains fade as lattice NODES pop in, staggered --
def build_crosslink():
    sid = "s09-crosslink"
    rng = random.Random(37)
    loose = free_coils(rng, 5, 480, 560, 300, 28, sw=8)
    net = lattice(480, 560, 6, 7, node_id_prefix=f"{sid}-node")
    panel = (f'<svg class="actor" viewBox="0 0 480 560" width="480" height="560" '
             f'preserveAspectRatio="xMidYMid meet" aria-hidden="true">\n'
             f'      <g class="loose-state" id="{sid}-loose">{loose}</g>\n'
             f'      <g class="net-state" id="{sid}-net" opacity="0" transform="scale(0.92)" '
             f'transform-origin="240 280">{net}</g>\n    </svg>')

    beats = beats_of(sid)
    idx = [i for i, b in enumerate(beats) if b["idiom"] != "hold"]
    swap_i = [i for i in idx if beats[i]["idiom"] == "wipe" or beats[i]["idiom"] == "swap"]
    off = beats[swap_i[0]]["offset"] if swap_i else 1.0
    d = beats[swap_i[0]]["dur"] if swap_i else 1.5

    xform_sets = [f"gsap.set('#{sid}-net', {{ opacity: 0, scale: 0.92 }});"]
    xform_tw = [
        f"tl.to('#{sid}-loose', {{ opacity: 0, scale: 0.94, duration: {d:.3f}, ease: 'power2.inOut' }}, {off:.3f});",
        f"tl.to('#{sid}-net', {{ opacity: 1, scale: 1, duration: {d:.3f}, ease: 'power2.inOut' }}, {off:.3f});",
    ]
    # The assembly is the point: instead of the whole net cross-fading in as
    # one flat block, a representative spread of NODES individually pop from
    # 0 scale with a stagger and an overshoot -- segments and nodes visibly
    # arriving one after another, not a state-swap of a static picture.
    n_nodes = 6 * 7
    stagger_n = 14
    step = list(range(0, n_nodes, max(1, n_nodes // stagger_n)))[:stagger_n]
    for k, node_i in enumerate(step):
        xform_sets.append(f"gsap.set('#{sid}-node{node_i}', {{ transformOrigin: 'center', scale: 0 }});")
        t = off + 0.15 + k * 0.06
        xform_tw.append(f"tl.to('#{sid}-node{node_i}', {{ scale: 1, duration: 0.450, "
                        f"ease: 'back.out(2.4)' }}, {t:.3f});")
    return _hero_left(sid, panel, panel_setup_sets=xform_sets, panel_extra_tweens=xform_tw)

# ---- s10-origin: 1934, cow-eye vitreous, tasteful 1930s idiom --------------
def build_origin():
    return _hero_left("s10-origin", eye_glassware_svg())

BUILD = {
  "s01-thesis":       build_thesis,
  "s02-identities":   build_identities,
  "s04-split":        build_split,
  "s05-size":         build_size,
  "s06-plumping":     build_plumping,
  "s07-binds":        build_binds,
  "s08-seals":        build_seals,
  "s09-crosslink":    build_crosslink,
  "s10-origin":       build_origin,
  "s13-badges":       build_badges,
}

def fix_generated_grounds():
    """Mechanical [S7/R-1] fix on the GENERATED scenes (s03, s11, s12, s14).

    Unchanged from v1/v2: dark-ground ink flip so text is never ink-on-ink,
    the citation-chip contrast swap, pairing every clipPath wipe with a real
    y-travel (a clipPath change is invisible to the motion pass on its own),
    and cycling hold-drift targets so consecutive holds don't tween an
    element to where it already sits.
    """
    fixed = 0
    total_subs = 0
    for i, sid in enumerate(ORDER, start=1):
        sc = SCENES[sid]
        if sc["handoff"] != "generated":
            continue
        path = f"{OUT}/{i:02d}-{sid}.html"
        html = open(path).read()
        scene_subs = 0
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
        html, n = html.replace("</style>", css + "</style>", 1), ("</style>" in html)
        scene_subs += int(n)

        html, n = re.subn(
            r"(gsap\.set\('#[^']+', \{ clipPath: 'inset\(0 100% 0 0\)')( \}\);)",
            r"\1, y: 22\2", html)
        scene_subs += n
        html, n = re.subn(r"(gsap\.set\('#[^']+', \{ opacity: 0, scale: )1\.12( \}\);)",
                      r"\g<1>1.03, y: -18\2", html)
        scene_subs += n
        html, n = re.subn(r"(tl\.to\('#[^']+', \{ opacity: 1, scale: 1)(, duration[^}]*ease: 'power4\.out')",
                      r"\1, y: 0\2", html)
        scene_subs += n
        html, n = re.subn(
            r"(tl\.to\('#[^']+', \{ clipPath: 'inset\(0 0% 0 0\)')(, duration)",
            r"\1, y: 0\2", html)
        scene_subs += n

        cnt = [0]
        def _drift(m):
            dx, dy, ds = DEFAULT_DRIFTS[cnt[0] % len(DEFAULT_DRIFTS)]; cnt[0] += 1
            return "%sx: %d, y: %d, scale: %s%s" % (m.group(1), dx, dy, ds, m.group(3))
        html, n = re.subn(r"(tl\.to\('#[^']+-stage', \{ )(x: -?[\d.]+, y: -?[\d.]+, scale: [\d.]+)(, duration)",
                      _drift, html)
        scene_subs += n

        open(path, "w").write(html)
        fixed += 1
        total_subs += scene_subs
        if scene_subs == 0:
            print("  WARNING: fix_generated_grounds made 0 substitutions on %s -- "
                  "the external generator's output format may have changed "
                  "under this fixer's regexes" % sid)
    print("  ground/contrast fix applied to %d generated scene(s), %d substitution(s) made"
          % (fixed, total_subs))


def fix_motion_sidecar():
    """[S7/R-1b]: set root `keepsMoving.maxStaticSec` from the FORMAT's cadence.

    v1/v2 both re-pointed this 2.0 -> 6.0, matched to a video whose real
    motion source was a handful of container drifts. This cut's 50 content
    beats average one every ~2.4s (see build_beats.py), so the honest ceiling
    is close to the brief's own "every 2-4 seconds" ask, not the loosest
    number the long-form format would tolerate. 3.0s keeps a small margin
    over that average without re-licensing the old drift-dominated pacing.
    """
    p = f"{HERE}/05-composition/index.motion.json"
    m = json.load(open(p))
    n = 0
    for a in m.get("assertions", []):
        if a.get("kind") == "keepsMoving" and a.get("maxStaticSec") == 2.0:
            a["maxStaticSec"] = 3.0
            a["_note"] = ("re-pointed from the engine's 2s Shorts default; kept close to "
                          "the piece's own measured ~2.4s beat cadence rather than "
                          "loosened to the long-form ceiling, since drift is no longer "
                          "the primary motion source")
            n += 1
    json.dump(m, open(p, "w"), indent=2)
    print("  motion sidecar: %d keepsMoving assertion(s) re-pointed 2.0s -> 3.0s" % n)


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
