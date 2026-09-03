#!/usr/bin/env python3
"""Scenes s08-s11: Q3 (vehicle journey), Q4 (evidence tunnel), Q5 (boundary)."""
from build_composition import write, stamp_svg

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
    f'<div class="leg" style="background:{color}22;"><div class="leg-fill" style="background:{color};"></div>{leg_svg(k)}<div class="leg-label">{label}</div></div>'
    for (label, color), k in zip(legs, kinds)
)
script = """
  gsap.set('#s08-passenger', { opacity: 0, x: 0 });

  var tl = gsap.timeline({ paused: true });
  tl.to('#s08-passenger', { opacity: 1, duration: 0.4, ease: 'power2.out' }, 0.2);
  tl.to('#s08-passenger', { x: 1450, duration: 18.0, ease: 'power1.inOut' }, 0.3);
  tl.to({}, { duration: 19.16, ease: 'none' }, 0);
  window.__timelines = window.__timelines || {};
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
    f'<path class="map-line" stroke="var(--ink-3)" d="M {20+i*15} {30+((i*47)%320)} L {200+((i*61)%260)} {60+((i*83)%300)} L {380+((i*29)%100)} {(i*97)%360+30}"/>'
    for i in range(9)
)
orderly_lines = "\n".join(
    f'<path class="map-line" stroke="var(--celadon)" d="M 20 {60+i*70} L 460 {60+i*70}"/>' for i in range(5)
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
      <div class="tag4" id="s09-tag"><div class="sub">THE VEHICLE MATTERS.</div></div>
    </div>
'''
script = """
  gsap.set('.transit-col', { opacity: 0, y: 24 });
  gsap.set('#s09-tag', { opacity: 0, y: 16 });

  var tl = gsap.timeline({ paused: true });
  tl.to('#s09-colA', { opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' }, 0.3);
  tl.to('#s09-colB', { opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' }, 0.7);
  tl.to('#s09-tag', { opacity: 1, y: 0, duration: 0.9, ease: 'power3.out' }, 6.0);
  tl.to({}, { duration: 15.048, ease: 'none' }, 0);
  window.__timelines = window.__timelines || {};
  window.__timelines['s09-q3-transit'] = tl;
"""
write("s09-q3-transit", style, body, script, bg="paper")

# ---------------------------------------------------------------- s10 -----
# Second travel-corridor instance: petri dish -> isolated ingredient -> human
# study -> finished product. Camera pulls sideways at the end to reveal gaps.
style = """
  .tunnel { position:relative; height:100%; width:100%; display:flex; flex-direction:column; justify-content:center; }
  .tunnel-head { text-align:center; opacity:0; margin-bottom:10px; }
  .tunnel-row { display:flex; justify-content:center; align-items:flex-end; gap:0; position:relative; }
  .tstage { width:380px; text-align:center; opacity:0; position:relative; }
  .tstage-icon { width:110px; height:110px; margin:0 auto 18px; }
  .tstage-label { font-family:var(--font-mono); font-size:26px; color:var(--ink-2); }
  .tgap { width:60px; height:3px; background:var(--rule-strong); align-self:center; opacity:0; }
  .cards { display:flex; justify-content:center; gap:40px; margin-top:56px; }
  .card { font-family:var(--font-mono); font-size:30px; color:var(--ink); border:2px solid var(--ink);
    border-radius:10px; padding:14px 22px; opacity:0; }
"""
tstages = [
    ("PETRI DISH", '<svg class="tstage-icon" viewBox="0 0 110 110"><ellipse cx="55" cy="55" rx="45" ry="45" fill="none" stroke="currentColor" stroke-width="4"/><ellipse cx="55" cy="55" rx="35" ry="35" fill="var(--celadon)" opacity="0.25"/></svg>'),
    ("ISOLATED INGREDIENT", '<svg class="tstage-icon" viewBox="0 0 110 110"><circle cx="55" cy="55" r="18" fill="var(--celadon)"/><circle cx="55" cy="55" r="30" fill="none" stroke="currentColor" stroke-width="2" opacity="0.5"/></svg>'),
    ("HUMAN SKIN STUDY", '<svg class="tstage-icon" viewBox="0 0 110 110"><path d="M20 70 Q55 20 90 70" fill="none" stroke="currentColor" stroke-width="4"/><circle cx="55" cy="55" r="8" fill="var(--celadon)"/></svg>'),
    ("FINISHED PRODUCT TEST", '<svg class="tstage-icon" viewBox="0 0 110 110"><rect x="35" y="20" width="40" height="70" rx="8" fill="none" stroke="currentColor" stroke-width="4"/><rect x="42" y="30" width="26" height="45" fill="var(--celadon)" opacity="0.4"/></svg>'),
]
stages_html = []
for i, (label, icon) in enumerate(tstages):
    stages_html.append(f'<div class="tstage" id="s10-stage-{i}">{icon}<div class="tstage-label">{label}</div></div>')
    if i < len(tstages) - 1:
        stages_html.append(f'<div class="tgap" id="s10-gap-{i}"></div>')
body = f'''
    <div class="tunnel">
      <div class="tunnel-head" id="s10-head"><div class="kicker">THE EVIDENCE TUNNEL</div></div>
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
script = f"""
  gsap.set('#s10-head', {{ opacity: 0, y: -10 }});
  gsap.set('.tstage', {{ opacity: 0, y: 20 }});
  gsap.set('.tgap', {{ opacity: 0 }});
  gsap.set('.card', {{ opacity: 0, y: 14 }});

  var tl = gsap.timeline({{ paused: true }});
  tl.to('#s10-head', {{ opacity: 1, y: 0, duration: 0.7, ease: 'power3.out' }}, 0.4);
{stage_tweens}
{gap_tweens}
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
script = f"""
  gsap.set('.fissure', {{ opacity: 0 }});
  gsap.set('#s11-camera', {{ scale: 1.09, y: 26 }});
  gsap.set('#s11-ring', {{ opacity: 0, scale: 0.9 }});
  gsap.set('.icon-item', {{ opacity: 0, y: 16 }});
  gsap.set('#s11-tag', {{ opacity: 0, y: 16 }});

  var tl = gsap.timeline({{ paused: true }});
  tl.to('#s11-camera', {{ scale: 1.0, y: 0, duration: 1.2, ease: 'power2.out' }}, 0.0);
{fissure_tweens}
  tl.to('#s11-ring', {{ opacity: 1, scale: 1, duration: 0.9, ease: 'power2.out' }}, 7.0);
{icon_tweens}
  tl.to('#s11-tag', {{ opacity: 1, y: 0, duration: 0.9, ease: 'power3.out' }}, 17.0);
  tl.to({{}}, {{ duration: 25.242, ease: 'none' }}, 0);
  window.__timelines = window.__timelines || {{}};
  window.__timelines['s11-q5-boundary'] = tl;
"""
write("s11-q5-boundary", style, body, script, bg="paper")
