#!/usr/bin/env python3
"""Scenes s08-s11: Q3 (vehicle journey), Q4 (evidence tunnel), Q5 (boundary)."""
from build_composition import write, stamp_svg
from catalog_components import evidence_state_chip, illustrative_disclosure, icon_svg


def chain_tweens(sel, start, end, seg, keyframes, ease="sine.inOut"):
    """Build restrained ambient idle motion as a chain of literal tl.to()
    calls on `sel` -- cycling through `keyframes` (a list of {gsap-var: value}
    dicts; duration/ease are supplied here, not per-keyframe), each held for
    `seg` seconds, from `start` up to `end` (the final segment is truncated to
    land exactly on `end`, never overshoots it). Deliberately built as
    explicit chained tweens -- each one starting exactly where the previous
    ends -- rather than GSAP's `repeat`, per this project's paused-timeline
    seek(t) render engine. Used to answer the cadence gate's flagged dead
    windows in s08/s09/s10/s11 with small, secondary, non-narrative motion."""
    GAP = 0.02  # hairline buffer so consecutive segments never touch at the same t
    lines = []
    t = start
    i = 0
    while t < end - GAP:
        dur = min(seg, end - t)
        vars_str = ", ".join(f"{k}: {v}" for k, v in keyframes[i % len(keyframes)].items())
        lines.append(f"  tl.to('{sel}', {{ {vars_str}, duration: {dur:.2f}, ease: '{ease}' }}, {t:.2f});")
        t += dur + GAP
        i += 1
    return "\n".join(lines)


# ---------------------------------------------------------------- s08 -----
# The shared "travel-corridor" pattern (also used at s10) -- camera travels
# through N successive stages with one persistent traveling actor.
style = """
  .corridor { position:relative; height:100%; width:100%; overflow:hidden; }
  .lane { position:absolute; inset:0; display:flex; }
  .leg { flex:1 1 0; display:flex; flex-direction:column; align-items:center; justify-content:center;
    border-right:1px solid var(--rule-strong); }
  .leg:last-child { border-right:none; }
  .leg-fill { position:absolute; inset:0; opacity:0.35; }
  .leg-label { font-family:var(--font-mono); font-size:28px; color:var(--ink-2); letter-spacing:.08em;
    position:relative; z-index:1; margin-top:14px; }
  .passenger { position:absolute; width:30px; height:30px; border-radius:50%;
    background: radial-gradient(circle at 35% 30%, #fff, var(--celadon) 70%);
    box-shadow: 0 0 20px 4px rgba(147,184,150,0.55); top:50%; left:6%; opacity:0; }
  .leg-icon { width:90px; height:90px; position:relative; z-index:1; }
"""
legs = [
    ("WATER PHASE", "#DCEDEB"),
    ("GEL LATTICE", "#C7DED8"),
    ("EMULSION", "#B7CFC3"),
    ("STRATUM CORNEUM", "#E9E1CE"),
]
def leg_svg(kind):
    if kind == "water":
        return '<svg class="leg-icon" viewBox="0 0 90 90"><path d="M20 70 Q30 50 20 30 Q35 45 45 30 Q55 45 70 30 Q60 50 70 70" fill="none" stroke="currentColor" stroke-width="4"/></svg>'
    if kind == "gel":
        return '<svg class="leg-icon" viewBox="0 0 90 90"><g fill="none" stroke="currentColor" stroke-width="3"><path d="M10 20 L30 20 L30 40 L10 40 Z"/><path d="M30 20 L50 20 L50 40 L30 40 Z"/><path d="M50 20 L70 20 L70 40 L50 40 Z"/><path d="M10 40 L30 40 L30 60 L10 60 Z"/><path d="M30 40 L50 40 L50 60 L30 60 Z"/><path d="M50 40 L70 40 L70 60 L50 60 Z"/></g></svg>'
    if kind == "emulsion":
        return '<svg class="leg-icon" viewBox="0 0 90 90"><g fill="currentColor" opacity="0.6"><circle cx="25" cy="30" r="8"/><circle cx="50" cy="45" r="11"/><circle cx="70" cy="25" r="6"/><circle cx="35" cy="65" r="9"/><circle cx="65" cy="65" r="7"/></g></svg>'
    return '<svg class="leg-icon" viewBox="0 0 90 90"><g fill="none" stroke="currentColor" stroke-width="3"><path d="M0 30 Q22 20 45 30 T90 30" /><path d="M0 55 Q22 45 45 55 T90 55" stroke-dasharray="5 6"/></g></svg>'
kinds = ["water", "gel", "emulsion", "skin"]
legs_html = "\n".join(
    f'<div class="leg" id="s08-leg-{i}" style="background:{color}22;"><div class="leg-fill" style="background:{color};"></div>{leg_svg(k)}<div class="leg-label">{label}</div></div>'
    for i, ((label, color), k) in enumerate(zip(legs, kinds))
)
# Cadence gate: the four legs sit fully static for the whole 18-19s crossing
# (only the passenger itself moves). Give each leg icon a slow, staggered
# scale breathe -- ambient, not a new beat -- spanning nearly the full window.
s08_leg_tweens = "\n".join(
    chain_tweens(f"#s08-leg-{i} .leg-icon", 0.6 + i * 0.35, 18.9, 3.5,
                 [{"scale": 1.035}, {"scale": 0.975}])
    for i in range(4)
)
script = f"""
  gsap.set('#s08-passenger', {{ opacity: 0, x: 0 }});

  var tl = gsap.timeline({{ paused: true }});
  tl.to('#s08-passenger', {{ opacity: 1, duration: 0.4, ease: 'power2.out' }}, 0.2);
  tl.to('#s08-passenger', {{ x: 1450, duration: 18.0, ease: 'power1.inOut' }}, 0.3);
{s08_leg_tweens}
  tl.to({{}}, {{ duration: 19.16, ease: 'none' }}, 0);
  window.__timelines = window.__timelines || {{}};
  window.__timelines['s08-q3-journey'] = tl;
"""
body = f'''
    <div class="corridor">
      <div class="lane">
        {legs_html}
      </div>
      <div class="passenger" id="s08-passenger"></div>
    </div>
'''
write("s08-q3-journey", style, body, script, bg="paper")

# ---------------------------------------------------------------- s09 -----
style = """
  .transit { position:relative; height:100%; width:100%; display:flex; flex-direction:column; justify-content:center; }
  .transit-row { display:flex; justify-content:center; gap:70px; }
  .transit-col { width:520px; height:420px; border-radius:20px; border:2px solid var(--rule-strong);
    padding:26px; position:relative; overflow:hidden; opacity:0; }
  .transit-col.b { border-color: var(--celadon); }
  .transit-label { font-family:var(--font-mono); font-size:26px; letter-spacing:.08em; color:var(--ink-2); }
  .map-line { position:absolute; stroke-width:2.5; fill:none; }
  .tag4 { text-align:center; margin-top:44px; opacity:0; }
  .tag4 .sub { font-size:56px; color:var(--vermilion); }
"""
chaotic_lines = "\n".join(
    f'<path class="map-line" id="s09-chaotic-{i}" stroke="var(--ink-3)" d="M {20+i*15} {30+((i*47)%320)} L {200+((i*61)%260)} {60+((i*83)%300)} L {380+((i*29)%100)} {(i*97)%360+30}"/>'
    for i in range(9)
)
orderly_lines = "\n".join(
    f'<path class="map-line" id="s09-orderly-{i}" stroke="var(--celadon)" d="M 20 {60+i*70} L 460 {60+i*70}"/>' for i in range(5)
)
body = f'''
    <div class="transit">
      <div class="transit-row">
        <div class="transit-col a" id="s09-colA">
          <div class="transit-label">BOTTLE A — TRANSPORT MAP</div>
          <svg viewBox="0 0 480 380" width="440" height="330">{chaotic_lines}</svg>
        </div>
        <div class="transit-col b" id="s09-colB">
          <div class="transit-label">BOTTLE B — TRANSIT SYSTEM</div>
          <svg viewBox="0 0 480 380" width="440" height="330">{orderly_lines}</svg>
        </div>
      </div>
      <div class="tag4" id="s09-tag">
        <div class="sub">THE VEHICLE MATTERS.</div>
        <div class="cite" id="s09-cite" style="margin:16px auto 0;">Int J Cosmet Sci · 2009</div>
      </div>
    </div>
'''
# Cadence gate: once both cards + the citation land (~7.7s in), the scene is
# static to the end (~15.5s). Give each map its own idle beat -- Bottle A's
# chaotic lines dimly flicker out of sync (still "rerouting"), Bottle B's
# orderly lines pulse together, calmly, as a contrast. Both stay well under
# the citation's and tag's opacity -- different elements, no shared property.
s09_chaotic_tweens = "\n".join(
    chain_tweens(f"#s09-chaotic-{i}", 1.7, 14.0, 1.8,
                 [{"opacity": 0.55}, {"opacity": 1.0}] if i % 2 == 0
                 else [{"opacity": 1.0}, {"opacity": 0.55}])
    for i in range(9)
)
_s09_orderly_sel = ", ".join(f"#s09-orderly-{i}" for i in range(5))
s09_orderly_tweens = chain_tweens(_s09_orderly_sel, 2.0, 14.5, 2.6,
                                   [{"opacity": 1.0}, {"opacity": 0.8}])
script = f"""
  gsap.set('.transit-col', {{ opacity: 0, y: 24 }});
  gsap.set('#s09-tag', {{ opacity: 0, y: 16 }});
  gsap.set('#s09-cite', {{ opacity: 0 }});

  var tl = gsap.timeline({{ paused: true }});
  tl.to('#s09-colA', {{ opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' }}, 0.3);
  tl.to('#s09-colB', {{ opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' }}, 0.7);
  tl.to('#s09-tag', {{ opacity: 1, y: 0, duration: 0.9, ease: 'power3.out' }}, 6.0);
  tl.to('#s09-cite', {{ opacity: 1, duration: 0.5, ease: 'power2.out' }}, 7.2);
{s09_chaotic_tweens}
{s09_orderly_tweens}
  tl.to({{}}, {{ duration: 15.048, ease: 'none' }}, 0);
  window.__timelines = window.__timelines || {{}};
  window.__timelines['s09-q3-transit'] = tl;
"""
write("s09-q3-transit", style, body, script, bg="paper")

# ---------------------------------------------------------------- s10 -----
# Catalog source: evidence-distance-map. Same four stages the original
# tunnel used, now built as a proper evidence chain -- each node states its
# relation to the finished-product target, connectors are dashed (no
# automatic transfer), and the sideways camera pull exposes the full chain
# plus the forensic question cards.
style = """
  .tunnel { position:relative; height:100%; width:100%; display:flex; flex-direction:column; justify-content:center; }
  .tunnel-head { text-align:center; opacity:0; margin-bottom:34px; }
  .tunnel-row { display:flex; justify-content:center; align-items:stretch; gap:0; position:relative; width:1740px; margin:0 auto; }
  .tstage { width:360px; text-align:left; opacity:0; position:relative; padding:26px 26px;
    border:1px solid var(--line); border-radius:20px; background:rgba(255,255,255,0.55); }
  .tstage-icon-wrap { width:70px; height:70px; border-radius:50%; border:1px solid var(--line);
    background:rgba(255,255,255,0.7); display:flex; align-items:center; justify-content:center; margin-bottom:14px; }
  .tstage-label { font-family:var(--font-mono); font-size:20px; color:var(--ink-soft); letter-spacing:.05em; }
  .tstage-title { font-weight:800; font-size:30px; letter-spacing:-.02em; margin-top:6px; }
  .tgap { flex:0 0 58px; position:relative; align-self:center; opacity:0; }
  .tgap .line { position:absolute; left:0; right:0; top:50%; height:0; border-top:2px dashed var(--ink-soft); }
  .cards { display:flex; justify-content:center; gap:40px; margin-top:52px; }
  .card { font-family:var(--font-mono); font-size:30px; color:var(--ink); border:2px solid var(--ink);
    border-radius:10px; padding:14px 22px; opacity:0; }
"""
tstages = [
    ("STAGE 1", "Cell study", "ingredient-source", "different"),
    ("STAGE 2", "Isolated ingredient, human", "quantity", "requires_context"),
    ("STAGE 3", "Human ingredient study", "identity-version", "requires_context"),
    ("STAGE 4", "Finished product test", "boundary", "known"),
]
stages_html = []
for i, (role, title, icon_name, state) in enumerate(tstages):
    icon = icon_svg(f"s10-stage-{i}-icon", icon_name, size=38, color="var(--ink)")
    chip = evidence_state_chip(f"s10-stage-{i}-chip", state,
                                text={"different": "Furthest", "requires_context": "Context required", "known": "Target"}[state])
    stages_html.append(f'''<div class="tstage" id="s10-stage-{i}">
      <div class="tstage-icon-wrap" id="s10-stage-{i}-fill">{icon}</div>
      <div class="tstage-label">{role}</div>
      <div class="tstage-title">{title}</div>
      <div style="margin-top:14px;">{chip}</div>
    </div>''')
    if i < len(tstages) - 1:
        stages_html.append(f'<div class="tgap" id="s10-gap-{i}"><div class="line"></div></div>')
body = f'''
    <div class="tunnel">
      <div class="tunnel-head" id="s10-head"><div class="kicker">EVIDENCE DISTANCE — HOW FAR FROM THE FINISHED PRODUCT</div></div>
      <div class="tunnel-row" id="s10-row">
        {"".join(stages_html)}
      </div>
      <div class="cards" id="s10-cards">
        <div class="card">TESTED WHAT?</div><div class="card">PEOPLE?</div>
        <div class="card">HOW LONG?</div><div class="card">MEASURED?</div>
      </div>
    </div>
'''
stage_tweens = "\n".join(
    f"  tl.to('#s10-stage-{i}', {{ opacity: 1, y: 0, duration: 0.7, ease: 'power3.out' }}, {2.0+i*2.0:.2f});"
    for i in range(4)
)
gap_tweens = "\n".join(
    f"  tl.to('#s10-gap-{i}', {{ opacity: 1, duration: 0.4, ease: 'power2.out' }}, {4.0+i*2.0:.2f});"
    for i in range(3)
)
card_tweens = "\n".join(
    f"  tl.to('.card:nth-child({i+1})', {{ opacity: 1, y: 0, duration: 0.5, ease: 'power3.out' }}, {24.5+i*0.35:.2f});"
    for i in range(4)
)
# Cadence gate: this is the longest dead window in the video (30s) -- the four
# stages land 8s apart and then just sit there. Give each stage's icon medal
# a slow pulse once it lands, continuing well past the last stage reveal (up
# to just before the sideways camera pull at t=30). Does not touch the
# forensic cards or their timing.
_s10_land = [2.0, 4.0, 6.0, 8.0]
stage_fill_tweens = "\n".join(
    chain_tweens(f"#s10-stage-{i}-fill", _s10_land[i] + 1.0, 35.0, 4.0,
                 [{"scale": 1.08}, {"scale": 0.96}])
    for i in range(4)
)
script = f"""
  gsap.set('#s10-head', {{ opacity: 0, y: -10 }});
  gsap.set('.tstage', {{ opacity: 0, y: 20, transformOrigin: '50% 50%' }});
  gsap.set('.tgap', {{ opacity: 0 }});
  gsap.set('.card', {{ opacity: 0, y: 14 }});

  var tl = gsap.timeline({{ paused: true }});
  tl.to('#s10-head', {{ opacity: 1, y: 0, duration: 0.7, ease: 'power3.out' }}, 0.4);
{stage_tweens}
{gap_tweens}
{stage_fill_tweens}
  tl.to('#s10-row', {{ x: -40, duration: 1.0, ease: 'power2.inOut' }}, 30.0);
{card_tweens}
  tl.to({{}}, {{ duration: 39.983, ease: 'none' }}, 0);
  window.__timelines = window.__timelines || {{}};
  window.__timelines['s10-q4-tunnel'] = tl;
"""
write("s10-q4-tunnel", style, body, script, bg="paper")

# ---------------------------------------------------------------- s11 -----
style = """
  .barrier { position:relative; height:100%; width:100%; display:flex; flex-direction:column; justify-content:center; align-items:center; }
  .skin-band { width:1400px; height:280px; position:relative; }
  .fissure { position:absolute; top:40%; stroke:var(--rule-dark); stroke-width:2; opacity:0; fill:none; }
  .boundary-ring { position:absolute; left:50%; top:38%; width:900px; height:220px; transform:translate(-50%,-50%);
    border:4px solid var(--celadon); border-radius:200px; opacity:0; }
  .icon-row { display:flex; gap:80px; margin-top:56px; }
  .icon-item { text-align:center; opacity:0; }
  .icon-item .label { margin-top:12px; }
  .tag5 { text-align:center; margin-top:40px; opacity:0; }
  .tag5 .sub { font-size:56px; color:var(--vermilion); }
  .gentle-row { position:absolute; left:0; right:0; top:calc(var(--safe-top) + 30px); text-align:center; opacity:0; }
  .gentle-row .body { font-size:44px; margin-bottom:14px; }
"""
icons = [
    ("PATCH", '<svg width="70" height="70" viewBox="0 0 70 70"><rect x="14" y="14" width="42" height="42" rx="8" fill="none" stroke="currentColor" stroke-width="4"/><path d="M24 35 L32 43 L48 27" fill="none" stroke="var(--celadon)" stroke-width="4"/></svg>'),
    ("ROUTINE", '<svg width="70" height="70" viewBox="0 0 70 70"><circle cx="35" cy="35" r="24" fill="none" stroke="currentColor" stroke-width="4"/><path d="M35 20 L35 35 L46 42" stroke="currentColor" stroke-width="4" fill="none"/></svg>'),
    ("STOP", '<svg width="70" height="70" viewBox="0 0 70 70"><polygon points="22,10 48,10 60,22 60,48 48,60 22,60 10,48 10,22" fill="none" stroke="currentColor" stroke-width="4"/><line x1="24" y1="24" x2="46" y2="46" stroke="currentColor" stroke-width="4"/></svg>'),
    ("CLINICIAN", '<svg width="70" height="70" viewBox="0 0 70 70"><circle cx="35" cy="24" r="12" fill="none" stroke="currentColor" stroke-width="4"/><path d="M15 58 Q35 38 55 58" fill="none" stroke="currentColor" stroke-width="4"/></svg>'),
]
icon_html = "\n".join(
    f'<div class="icon-item" id="s11-icon-{i}">{svg}<div class="label">{label}</div></div>'
    for i, (label, svg) in enumerate(icons)
)
fissures = "\n".join(
    f'<path class="fissure" id="s11-fissure-{i}" d="M {150+i*220} 60 L {170+i*220} 120 L {140+i*220} 180"/>'
    for i in range(6)
)
body = f'''
    <div class="barrier" id="s11-camera" style="transform-origin:50% 40%;">
      <div class="gentle-row" id="s11-gentle">
        <div class="body">"Gentle" isn't a fixed property</div>
        <div class="uf-badge" id="s11-flag" style="margin:0 auto;">○ UNSOURCED — no record in this system</div>
      </div>
      <div class="skin-band">
        <svg width="1400" height="280" viewBox="0 0 1400 280">
          <path d="M0 90 Q175 70 350 90 T700 90 T1050 90 T1400 90" fill="none" stroke="var(--ink)" stroke-width="4" opacity="0.7"/>
          <line x1="0" y1="150" x2="1400" y2="150" stroke="var(--ink)" stroke-width="2" stroke-dasharray="14 10" opacity="0.4"/>
          {fissures}
        </svg>
      </div>
      <div class="boundary-ring" id="s11-ring"></div>
      <div class="icon-row" id="s11-icons">
        {icon_html}
      </div>
      <div class="tag5" id="s11-tag"><div class="sub">THE BOUNDARY IS THE ANSWER.</div></div>
    </div>
'''
fissure_tweens = "\n".join(
    f"  tl.to('#s11-fissure-{i}', {{ opacity: 0.7, duration: 0.3, ease: 'power2.out' }}, {2.0+i*0.5:.2f});"
    for i in range(6)
)
icon_tweens = "\n".join(
    f"  tl.to('#s11-icon-{i}', {{ opacity: 1, y: 0, duration: 0.5, ease: 'power3.out' }}, {12.0+i*0.3:.2f});"
    for i in range(4)
)
# Cadence gate: after the ring/icons finish landing (~21s) the scene holds
# static to the end. The ring is the scene's central metaphor, so give it a
# slow scale+opacity breathe spanning the dead window -- starting after its
# own arrival tween finishes (7.9s) and ending before the scene's own close
# (25.242s). Does not touch #s11-flag or #s11-camera.
s11_ring_tweens = chain_tweens("#s11-ring", 8.2, 25.0, 2.8,
                                [{"scale": 1.035, "opacity": 1.0},
                                 {"scale": 0.975, "opacity": 0.88}])
script = f"""
  gsap.set('.fissure', {{ opacity: 0 }});
  gsap.set('#s11-camera', {{ scale: 1.09, y: 26 }});
  gsap.set('#s11-ring', {{ opacity: 0, scale: 0.9 }});
  gsap.set('.icon-item', {{ opacity: 0, y: 16 }});
  gsap.set('#s11-tag', {{ opacity: 0, y: 16 }});
  gsap.set('#s11-gentle', {{ opacity: 0, y: -10 }});

  var tl = gsap.timeline({{ paused: true }});
  tl.to('#s11-camera', {{ scale: 1.0, y: 0, duration: 1.2, ease: 'power2.out' }}, 0.0);
  // [K-2] flag fires CONCURRENTLY with the C15 claim per 01-story-brief.md --
  // narrated right after "where does the answer stop applying?", ~0.9-6s in.
  tl.to('#s11-gentle', {{ opacity: 1, y: 0, duration: 0.6, ease: 'power3.out' }}, 0.9);
  tl.to('#s11-gentle', {{ opacity: 0, y: -10, duration: 0.5, ease: 'power2.in' }}, 5.8);
{fissure_tweens}
  tl.to('#s11-ring', {{ opacity: 1, scale: 1, duration: 0.9, ease: 'power2.out' }}, 7.0);
{s11_ring_tweens}
{icon_tweens}
  tl.to('#s11-tag', {{ opacity: 1, y: 0, duration: 0.9, ease: 'power3.out' }}, 17.0);
  tl.to({{}}, {{ duration: 25.242, ease: 'none' }}, 0);
  window.__timelines = window.__timelines || {{}};
  window.__timelines['s11-q5-boundary'] = tl;
"""
write("s11-q5-boundary", style, body, script, bg="paper")
