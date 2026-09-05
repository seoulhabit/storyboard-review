#!/usr/bin/env python3
"""Scenes s08-s11: Q3 (vehicle journey), Q4 (evidence tunnel), Q5 (boundary)."""
from build_composition import write, stamp_svg
from catalog_components import evidence_state_chip, illustrative_disclosure, icon_svg, question_seal


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


def leg_svg(kind):
    if kind == "water":
        return '<svg class="leg-icon" viewBox="0 0 90 90"><path d="M20 70 Q30 50 20 30 Q35 45 45 30 Q55 45 70 30 Q60 50 70 70" fill="none" stroke="currentColor" stroke-width="4"/></svg>'
    if kind == "gel":
        return '<svg class="leg-icon" viewBox="0 0 90 90"><g fill="none" stroke="currentColor" stroke-width="3"><path d="M10 20 L30 20 L30 40 L10 40 Z"/><path d="M30 20 L50 20 L50 40 L30 40 Z"/><path d="M50 20 L70 20 L70 40 L50 40 Z"/><path d="M10 40 L30 40 L30 60 L10 60 Z"/><path d="M30 40 L50 40 L50 60 L30 60 Z"/><path d="M50 40 L70 40 L70 60 L50 60 Z"/></g></svg>'
    if kind == "emulsion":
        return '<svg class="leg-icon" viewBox="0 0 90 90"><g fill="currentColor" opacity="0.6"><circle cx="25" cy="30" r="8"/><circle cx="50" cy="45" r="11"/><circle cx="70" cy="25" r="6"/><circle cx="35" cy="65" r="9"/><circle cx="65" cy="65" r="7"/></g></svg>'
    return '<svg class="leg-icon" viewBox="0 0 90 90"><g fill="none" stroke="currentColor" stroke-width="3"><path d="M0 30 Q22 20 45 30 T90 30" /><path d="M0 55 Q22 45 45 55 T90 55" stroke-dasharray="5 6"/></g></svg>'

VEHICLE_STAGES = [
    ("Water phase", "water", "illustrative"),
    ("Gel network", "gel", "illustrative"),
    ("Complete emulsion", "emulsion", "requires_context"),
    ("Skin surface", "skin", "not_established"),
]

def vehicle_channel(uid, compact=False):
    """Catalog source: formula-vehicle-journey. The ingredient is the
    passenger; the full formula is the vehicle. Shared by s08 (single route)
    and s09 (paired A/B), per the brief's reuse requirement."""
    icon_size = 56 if compact else 90
    size_attr = f'width="{icon_size}" height="{icon_size}"'
    legs = []
    for i, (label, kind, state) in enumerate(VEHICLE_STAGES):
        icon = leg_svg(kind).replace('class="leg-icon"', size_attr)
        chip = "" if compact else evidence_state_chip(f"{uid}-chip-{i}", state)
        legs.append(
            f'<div class="veh-leg" id="{uid}-leg-{i}"><div class="veh-icon">{icon}</div>'
            f'<div class="veh-name">{label}</div>{chip}</div>')
    legs_html = "\n".join(legs)
    return f'''<div class="veh-channel" id="{uid}">
    <div class="veh-route" id="{uid}-route"></div>
    <div class="veh-payload" id="{uid}-payload"></div>
    {legs_html}
  </div>'''

VEHICLE_CSS = """
  .veh-channel { position:relative; display:flex; border:1px solid var(--line); border-radius:24px;
    background:rgba(255,255,255,0.5); overflow:hidden; }
  .veh-leg { flex:1; min-width:0; padding:26px 20px; text-align:center; border-right:1px solid var(--line); }
  .veh-leg:last-child { border-right:none; }
  .veh-icon { color:var(--ink); opacity:0.85; margin-bottom:8px; display:flex; justify-content:center; }
  .veh-name { font-weight:700; font-size:24px; letter-spacing:-.01em; margin-bottom:10px; }
  .veh-route { position:absolute; left:5%; right:5%; top:50%; height:3px; border-radius:999px;
    background:rgba(23,35,50,.1); }
  .veh-payload { position:absolute; left:5%; top:calc(50% - 13px); width:26px; height:26px; border-radius:50%;
    background: radial-gradient(circle at 35% 30%, #fff, var(--celadon) 70%);
    box-shadow: 0 0 16px 3px rgba(127,157,136,0.5); opacity:0; }
"""

# ---------------------------------------------------------------- s08 -----
style = VEHICLE_CSS + """
  .journey-stage { position:relative; height:100%; width:100%; display:flex; flex-direction:column; justify-content:center; }
  .journey-head { text-align:center; margin-bottom:30px; opacity:0; }
"""
s08_channel = vehicle_channel("s08-veh", compact=False)
body = f'''
    <div class="journey-stage">
      <div class="journey-head" id="s08-head"><div class="kicker">THE INGREDIENT IS THE PASSENGER</div></div>
      <div style="width:1650px; margin:0 auto;">
        {s08_channel}
        <div style="margin-top:26px;">{illustrative_disclosure("s08-disc", "Authored formula-path illustration — not a product-performance claim.")}</div>
      </div>
    </div>
'''
# Cadence gate: the four legs sit fully static for the whole 18-19s crossing
# (only the passenger itself moves). Give each leg icon a slow, staggered
# scale breathe -- ambient, not a new beat -- spanning nearly the full window.
s08_leg_tweens = "\n".join(
    chain_tweens(f"#s08-veh-leg-{i} .veh-icon", 0.6 + i * 0.35, 18.9, 3.5,
                 [{"scale": 1.035}, {"scale": 0.975}])
    for i in range(4)
)
script = f"""
  gsap.set('#s08-head', {{ opacity: 0, y: -10 }});
  gsap.set('#s08-veh-payload', {{ opacity: 0, x: 0 }});
  gsap.set('.veh-icon', {{ transformOrigin: '50% 50%' }});

  var tl = gsap.timeline({{ paused: true }});
  tl.to('#s08-head', {{ opacity: 1, y: 0, duration: 0.6, ease: 'power3.out' }}, 0.0);
  tl.to('#s08-veh-payload', {{ opacity: 1, duration: 0.4, ease: 'power2.out' }}, 0.2);
  tl.to('#s08-veh-payload', {{ x: 1520, duration: 18.0, ease: 'power1.inOut' }}, 0.3);
{s08_leg_tweens}
  tl.to({{}}, {{ duration: 19.16, ease: 'none' }}, 0);
  window.__timelines = window.__timelines || {{}};
  window.__timelines['s08-q3-journey'] = tl;
"""
write("s08-q3-journey", style, body, script, bg="paper")

# ---------------------------------------------------------------- s09 -----
# Paired state of the same Formula Vehicle Journey: two structured channels,
# same four stages, different per-stage support variables -- never a
# chaotic-vs-orderly value judgment, per the brief's map for this scene.
style = VEHICLE_CSS + """
  .transit { position:relative; height:100%; width:100%; display:flex; flex-direction:column; justify-content:center; }
  .transit-row { display:flex; flex-direction:column; gap:26px; width:1650px; margin:0 auto; }
  .transit-label { font-family:var(--font-mono); font-size:20px; letter-spacing:.06em; color:var(--ink-soft); margin-bottom:8px; }
  .veh-channel.compact .veh-leg { padding:16px 14px; }
  .veh-channel.compact .veh-name { font-size:19px; margin-bottom:0; }
  .tag4 { text-align:center; margin-top:30px; opacity:0; }
  .tag4 .sub { font-size:50px; color:var(--signal); }
  .seal-lock { position:absolute; right:calc(var(--safe-right) + 40px); bottom:calc(var(--safe-bottom) + 20px);
    opacity:0; transform:scale(0.5); }
"""
s09_channel_a = vehicle_channel("s09-vehA", compact=True)
s09_channel_b = vehicle_channel("s09-vehB", compact=True)
body = f'''
    <div class="transit">
      <div class="transit-row">
        <div id="s09-colA" style="opacity:0;"><div class="transit-label">BOTTLE A — FORMULA VEHICLE</div>
          <div class="veh-channel compact">{s09_channel_a}</div></div>
        <div id="s09-colB" style="opacity:0;"><div class="transit-label">BOTTLE B — FORMULA VEHICLE</div>
          <div class="veh-channel compact">{s09_channel_b}</div></div>
      </div>
      <div class="tag4" id="s09-tag">
        <div class="sub">THE VEHICLE MATTERS.</div>
        <div class="cite" id="s09-cite" style="margin:16px auto 0;">Int J Cosmet Sci &middot; 2009</div>
      </div>
      <div class="seal-lock" id="s09-seal-lock">{question_seal("s09-q3-seal", 2, "active", size=100, bg="paper")}</div>
    </div>
'''
script = """
  gsap.set('#s09-colA', { opacity: 0, y: 20 });
  gsap.set('#s09-colB', { opacity: 0, y: 20 });
  gsap.set('#s09-vehA-payload', { opacity: 0, x: 0 });
  gsap.set('#s09-vehB-payload', { opacity: 0, x: 0 });
  gsap.set('#s09-tag', { opacity: 0, y: 16 });
  gsap.set('#s09-cite', { opacity: 0 });
  gsap.set('#s09-seal-lock', { opacity: 0, scale: 0.5 });

  var tl = gsap.timeline({ paused: true });
  tl.to('#s09-colA', { opacity: 1, y: 0, duration: 0.7, ease: 'power3.out' }, 0.3);
  tl.to('#s09-colB', { opacity: 1, y: 0, duration: 0.7, ease: 'power3.out' }, 0.6);
  tl.to('#s09-vehA-payload', { opacity: 1, duration: 0.3 }, 1.1);
  tl.to('#s09-vehB-payload', { opacity: 1, duration: 0.3 }, 1.2);
  tl.to('#s09-vehA-payload', { x: 1540, duration: 5.0, ease: 'power1.inOut' }, 1.1);
  tl.to('#s09-vehB-payload', { x: 1540, duration: 5.0, ease: 'power1.inOut' }, 1.2);
  tl.to('#s09-tag', { opacity: 1, y: 0, duration: 0.9, ease: 'power3.out' }, 6.5);
  tl.to('#s09-cite', { opacity: 1, duration: 0.5, ease: 'power2.out' }, 7.7);
  // snap, Question 3 seal turns face-up.
  tl.to('#s09-seal-lock', { opacity: 1, scale: 1, duration: 0.3, ease: 'back.out(2)' }, 13.1);
  tl.to('#s09-q3-seal-ring', { attr: { stroke: '#426B50' }, duration: 0.3, ease: 'power2.out' }, 13.2);
  tl.to('#s09-q3-seal-keyline', { attr: { stroke: '#426B50' }, duration: 0.3, ease: 'power2.out' }, 13.2);
  tl.to('#s09-q3-seal .icon', { color: '#426B50', duration: 0.3, ease: 'power2.out' }, 13.2);
  tl.to({}, { duration: 15.048, ease: 'none' }, 0);
  window.__timelines = window.__timelines || {};
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
  .seal-lock { position:absolute; right:calc(var(--safe-right) + 40px); bottom:calc(var(--safe-bottom) + 20px);
    opacity:0; transform:scale(0.5); }
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
      <div class="seal-lock" id="s10-seal-lock">{question_seal("s10-q4-seal", 3, "active", size=100, bg="paper")}</div>
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
  gsap.set('#s10-seal-lock', {{ opacity: 0, scale: 0.5 }});

  var tl = gsap.timeline({{ paused: true }});
  tl.to('#s10-head', {{ opacity: 1, y: 0, duration: 0.7, ease: 'power3.out' }}, 0.4);
{stage_tweens}
{gap_tweens}
{stage_fill_tweens}
  tl.to('#s10-row', {{ x: -40, duration: 1.0, ease: 'power2.inOut' }}, 30.0);
{card_tweens}
  // snap, Question 4 seal turns face-up.
  tl.to('#s10-seal-lock', {{ opacity: 1, scale: 1, duration: 0.3, ease: 'back.out(2)' }}, 39.0);
  tl.to('#s10-q4-seal-ring', {{ attr: {{ stroke: '#426B50' }}, duration: 0.3, ease: 'power2.out' }}, 39.1);
  tl.to('#s10-q4-seal-keyline', {{ attr: {{ stroke: '#426B50' }}, duration: 0.3, ease: 'power2.out' }}, 39.1);
  tl.to('#s10-q4-seal .icon', {{ color: '#426B50', duration: 0.3, ease: 'power2.out' }}, 39.1);
  tl.to({{}}, {{ duration: 39.983, ease: 'none' }}, 0);
  window.__timelines = window.__timelines || {{}};
  window.__timelines['s10-q4-tunnel'] = tl;
"""
write("s10-q4-tunnel", style, body, script, bg="paper")

# ---------------------------------------------------------------- s11 -----
# Catalog source: boundary-suitability-card. Replaces the skin-fissure
# illustration with a calm inside/outside-the-evidence split and explicit
# actions (check / contextualize / stop / escalate) -- no universal
# gentle/safe language, per the brief's map and the exclude-list in
# source-map.md.
style = """
  .barrier { position:relative; height:100%; width:100%; display:flex; flex-direction:column; justify-content:center; align-items:center; }
  .bd-wrap { position:relative; width:1650px; }
  .bd-zones { display:flex; align-items:stretch; gap:80px; }
  .bd-zone { flex:1; min-width:0; padding:34px 38px; border-top:6px solid var(--celadon); border-radius:4px 4px 20px 20px;
    background:rgba(255,255,255,0.55); opacity:0; }
  .bd-zone.outside { border-top-color:var(--signal); }
  .bd-zone-name { color:var(--ink-soft); font-size:22px; margin-bottom:16px; }
  .bd-zone-value { font-size:30px; font-weight:700; letter-spacing:-.02em; line-height:1.3; margin-bottom:14px; }
  .bd-zone-copy { color:var(--ink-soft); font-size:20px; line-height:1.4; }
  .bd-badge { position:absolute; left:50%; top:50%; transform:translate(-50%,-50%) rotate(-6deg); width:150px; height:150px;
    border-radius:50%; border:6px solid var(--signal); background:var(--paper); display:flex; align-items:center;
    justify-content:center; text-align:center; font-weight:700; font-size:24px; color:var(--signal); opacity:0; }
  .bd-actions { display:flex; margin-top:40px; border-radius:14px; overflow:hidden; opacity:0; }
  .bd-action { flex:1; display:flex; align-items:center; gap:16px; padding:22px 24px; background:var(--ink);
    border-right:1px solid rgba(255,255,255,.14); }
  .bd-action:last-child { border-right:none; }
  .bd-action .mark { width:44px; height:44px; flex:none; border-radius:50%; border:2px solid var(--ink-mark, var(--celadon));
    color:var(--ink-mark, var(--celadon)); display:flex; align-items:center; justify-content:center; font-weight:700; }
  .bd-action .name { color:var(--paper); font-size:20px; font-weight:650; }
  .bd-action .copy { color:rgba(247,245,240,0.62); font-size:16px; margin-top:4px; }
  .tag5 { text-align:center; margin-top:34px; opacity:0; }
  .tag5 .sub { font-size:50px; color:var(--signal); }
  .gentle-row { position:absolute; left:0; right:0; top:calc(var(--safe-top) + 30px); text-align:center; opacity:0; }
  .gentle-row .body { font-size:44px; margin-bottom:14px; }
  .seal-lock { position:absolute; right:calc(var(--safe-right) + 40px); bottom:calc(var(--safe-bottom) + 20px);
    opacity:0; transform:scale(0.5); }
"""
actions = [
    ("1", "Check the product", "Use its actual label and directions.", "#7F9D88"),
    ("2", "Check the context", "Formula, route, routine and skin state matter.", "#5F9294"),
    ("3", "Stop the inference", "Do not extend the evidence past this line.", "#D95F52"),
    ("4", "Escalate the question", "Personal medical decisions belong with a qualified clinician.", "#6358A7"),
]
action_html = "\n".join(
    f'<div class="bd-action" id="s11-action-{i}"><div class="mark" style="--ink-mark:{color};">{n}</div>'
    f'<div><div class="name">{name}</div><div class="copy">{copy}</div></div></div>'
    for i, (n, name, copy, color) in enumerate(actions)
)
body = f'''
    <div class="barrier" id="s11-camera" style="transform-origin:50% 42%;">
      <div class="gentle-row" id="s11-gentle">
        <div class="body">"Gentle" isn't a fixed property</div>
        <div class="uf-badge" id="s11-flag" style="margin:0 auto;">○ UNSOURCED — no record in this system</div>
      </div>
      <div class="bd-wrap">
        <div class="bd-zones">
          <div class="bd-zone inside" id="s11-inside">
            <div class="bd-zone-name">INSIDE THE EVIDENCE</div>
            <div class="bd-zone-value">The label may identify Centella Asiatica Extract.</div>
            <div class="bd-zone-copy">That identity can support a focused product question when the declaration is visible.</div>
          </div>
          <div class="bd-zone outside" id="s11-outside">
            <div class="bd-zone-name">OUTSIDE THE EVIDENCE</div>
            <div class="bd-zone-value">It does not certify performance or personal suitability.</div>
            <div class="bd-zone-copy">Exact extract, amount, vehicle, evidence match and individual context remain separate questions.</div>
          </div>
        </div>
        <div class="bd-badge" id="s11-badge">BOUNDARY</div>
        <div class="bd-actions" id="s11-actions">{action_html}</div>
      </div>
      <div class="tag5" id="s11-tag"><div class="sub">THE BOUNDARY IS THE ANSWER.</div></div>
      <div class="seal-lock" id="s11-seal-lock">{question_seal("s11-q5-seal", 4, "active", size=100, bg="paper")}</div>
    </div>
'''
action_tweens = "\n".join(
    f"  tl.to('#s11-action-{i}', {{ opacity: 1, duration: 0.4, ease: 'power2.out' }}, {12.0+i*0.25:.2f});"
    for i in range(4)
)
# Cadence gate: after the actions land (~13s) the scene holds fairly static
# to the end. The boundary badge is the scene's central metaphor, so give it
# a slow scale breathe spanning that stretch, ending before the scene closes.
s11_badge_tweens = chain_tweens("#s11-badge", 8.9, 24.6, 2.8,
                                 [{"scale": 1.04}, {"scale": 0.97}])
script = f"""
  gsap.set('#s11-camera', {{ scale: 1.09, y: 26 }});
  gsap.set('.bd-zone', {{ opacity: 0, y: 24 }});
  gsap.set('#s11-badge', {{ opacity: 0, scale: 0.7, transformOrigin: '50% 50%' }});
  gsap.set('.bd-action', {{ opacity: 0 }});
  gsap.set('#s11-tag', {{ opacity: 0, y: 16 }});
  gsap.set('#s11-gentle', {{ opacity: 0, y: -10 }});
  gsap.set('#s11-seal-lock', {{ opacity: 0, scale: 0.5 }});

  var tl = gsap.timeline({{ paused: true }});
  tl.to('#s11-camera', {{ scale: 1.0, y: 0, duration: 1.2, ease: 'power2.out' }}, 0.0);
  // [K-2] flag fires CONCURRENTLY with the C15 claim per 01-story-brief.md --
  // narrated right after "where does the answer stop applying?", ~0.9-6s in.
  tl.to('#s11-gentle', {{ opacity: 1, y: 0, duration: 0.6, ease: 'power3.out' }}, 0.9);
  tl.to('#s11-gentle', {{ opacity: 0, y: -10, duration: 0.5, ease: 'power2.in' }}, 5.8);
  tl.to('#s11-inside', {{ opacity: 1, y: 0, duration: 0.7, ease: 'power3.out' }}, 7.0);
  tl.to('#s11-outside', {{ opacity: 1, y: 0, duration: 0.7, ease: 'power3.out' }}, 7.5);
  tl.to('#s11-badge', {{ opacity: 1, scale: 1, duration: 0.7, ease: 'back.out(1.8)' }}, 8.2);
{s11_badge_tweens}
{action_tweens}
  tl.to('#s11-tag', {{ opacity: 1, y: 0, duration: 0.9, ease: 'power3.out' }}, 17.0);
  // snap, Question 5 seal turns face-up -- the last of the five.
  tl.to('#s11-seal-lock', {{ opacity: 1, scale: 1, duration: 0.3, ease: 'back.out(2)' }}, 24.24);
  tl.to('#s11-q5-seal-ring', {{ attr: {{ stroke: '#426B50' }}, duration: 0.3, ease: 'power2.out' }}, 24.34);
  tl.to('#s11-q5-seal-keyline', {{ attr: {{ stroke: '#426B50' }}, duration: 0.3, ease: 'power2.out' }}, 24.34);
  tl.to('#s11-q5-seal .icon', {{ color: '#426B50', duration: 0.3, ease: 'power2.out' }}, 24.34);
  tl.to({{}}, {{ duration: 25.242, ease: 'none' }}, 0);
  window.__timelines = window.__timelines || {{}};
  window.__timelines['s11-q5-boundary'] = tl;
"""
write("s11-q5-boundary", style, body, script, bg="paper")
