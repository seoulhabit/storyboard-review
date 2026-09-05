#!/usr/bin/env python3
"""Scenes s01-s03: the bench hook, the passport thesis, the promise/seal tease."""
from build_composition import write, stamp_svg, bottle_svg
from catalog_components import (
    ingredient_actor_svg, neutral_package_shell_svg, five_question_progress,
    question_seal, icon_svg, evidence_state_chip,
)

# ---------------------------------------------------------------- s01 -----
# Catalog source: ingredient-hero-actor + label-compare-stage. Open on the
# Cica actor, not two hero bottles; the actor persists between two neutral
# package shells brought in as supporting specimens (brief's s01 map).
style = """
  .bench { position:relative; height:100%; width:100%;
    background: radial-gradient(120% 90% at 50% 15%, #1B1E1F 0%, var(--ink) 55%, #0A0B0B 100%); }
  .bench-surface { position:absolute; left:0; right:0; bottom:0; height:38%;
    background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(0,0,0,0.35));
    border-top:1px solid rgba(255,255,255,0.06); }
  .droplet { position:absolute; left:50%; top:8%; width:14px; height:14px; border-radius:50%;
    background: radial-gradient(circle at 35% 30%, #EAF2F0, var(--celadon) 70%); opacity:0; }
  .ripple { position:absolute; left:50%; top:44%; width:60px; height:16px; border-radius:50%;
    transform:translate(-50%,-50%); border:2px solid var(--celadon); opacity:0; }
  .actor-row { position:absolute; left:50%; top:34%; transform:translate(-50%,-50%);
    display:flex; align-items:center; justify-content:center; gap:130px; }
  .actor-slot { opacity:0; }
  .bottle-slot { text-align:center; opacity:0; }
  .emboss { font-family:var(--font-mono); font-size:24px; letter-spacing:.2em; color:rgb(150,158,168); margin-top:14px; }
  .decl { margin-top:14px; font-family:var(--font-mono); font-size:16px; line-height:1.35;
    letter-spacing:.01em; color:rgb(150,158,168); text-align:left; width:210px; }
  .decl .item { margin-bottom:6px; color:rgb(150,158,168); }
  .decl .item:last-child { margin-bottom:0; }
  .decl.right { text-align:left; }
  .thesis-row { position:absolute; left:0; right:0; bottom:calc(var(--safe-bottom) + 10px);
    text-align:center; opacity:0; }
  .thesis-row .head { font-size:84px; color:var(--paper); }
"""
s01_ribbon_l_names = ["CENTELLA ASIATICA EXTRACT", "WATER", "NIACINAMIDE", "FRAGRANCE"]
s01_ribbon_r_names = ["CENTELLA ASIATICA EXTRACT", "WATER", "MADECASSOSIDE", "FRAGRANCE"]
s01_ribbon_l_html = "\n        ".join(
    f'<div class="item" id="s01-ribbon-l-{i}">{n}</div>' for i, n in enumerate(s01_ribbon_l_names))
s01_ribbon_r_html = "\n        ".join(
    f'<div class="item" id="s01-ribbon-r-{i}">{n}</div>' for i, n in enumerate(s01_ribbon_r_names))
body = f'''
    <div class="bench">
      <div class="bench-surface"></div>
      <div class="droplet" id="s01-droplet"></div>
      <div class="ripple" id="s01-ripple"></div>
      <div class="actor-row">
        <div class="bottle-slot" id="s01-slot-a">
          {neutral_package_shell_svg("s01-bottle-a", width=180, height=360, variant="a", liquid_state="ambiguous")}
          <div class="emboss">CICA</div>
          <div class="decl" id="s01-decl-l">{s01_ribbon_l_html}</div>
        </div>
        <div class="actor-slot" id="s01-actor-slot">
          {ingredient_actor_svg("s01-actor", size=240)}
        </div>
        <div class="bottle-slot" id="s01-slot-b">
          {neutral_package_shell_svg("s01-bottle-b", width=180, height=360, variant="b", liquid_state="ambiguous")}
          <div class="emboss">CICA</div>
          <div class="decl right" id="s01-decl-r">{s01_ribbon_r_html}</div>
        </div>
      </div>
      <div class="thesis-row" id="s01-thesis">
        <div class="head">SAME HERO. DIFFERENT FORMULA.</div>
      </div>
    </div>
'''
# [cadence] fill the long hold (10.0-15.777) with a slow breathing scale on
# the actor row, plus a paced brightening cascade on the two declaration
# lists (secondary re-emphasis of names already on screen).
_s01_ribbon_order = []
for _i in range(len(s01_ribbon_l_names)):
    _s01_ribbon_order.append(f"s01-ribbon-l-{_i}")
    _s01_ribbon_order.append(f"s01-ribbon-r-{_i}")
_s01_cascade_lines = []
for _idx, _elid in enumerate(_s01_ribbon_order):
    _t0 = 6.6 + _idx * 0.5
    _s01_cascade_lines.append(
        f"  tl.to('#{_elid}', {{ color: 'rgb(226,230,235)', duration: 0.35, ease: 'sine.out' }}, {_t0:.2f});")
    _s01_cascade_lines.append(
        f"  tl.to('#{_elid}', {{ color: 'rgb(150,158,168)', duration: 0.45, ease: 'sine.in' }}, {_t0 + 0.37:.2f});")
s01_extra_tweens = "\n".join(_s01_cascade_lines) + "\n" + (
    "  tl.to('.actor-row', { scale: 1.018, duration: 4.18, ease: 'sine.inOut' }, 6.6);\n"
    "  tl.to('.actor-row', { scale: 0.99, duration: 4.18, ease: 'sine.inOut' }, 10.82);\n"
    "  tl.to('.actor-row', { scale: 1.0, duration: 1.28, ease: 'sine.inOut' }, 15.02);\n"
)
script = """
  // [R-1] frame 0 must never be blank: the droplet starts already visible
  // (this IS the hook), not faded in from opacity 0.
  gsap.set('#s01-droplet', { opacity: 1, y: -20 });
  gsap.set('#s01-ripple', { opacity: 0, scale: 0.3 });
  gsap.set('#s01-actor-slot', { opacity: 0, scale: 0.5, rotation: -12 });
  gsap.set('#s01-slot-a', { opacity: 0, x: -60 });
  gsap.set('#s01-slot-b', { opacity: 0, x: 60 });
  gsap.set('#s01-decl-l', { opacity: 0 });
  gsap.set('#s01-decl-r', { opacity: 0 });
  gsap.set('#s01-thesis', { opacity: 0, y: 16 });
  gsap.set('.actor-row', { transformOrigin: '50% 50%' });

  var tl = gsap.timeline({ paused: true });
  tl.to('#s01-droplet', { opacity: 1, y: 200, duration: 1.6, ease: 'power1.in' }, 0.0);
  tl.to('#s01-droplet', { opacity: 0, duration: 0.15 }, 1.6);
  tl.fromTo('#s01-ripple', { opacity: 0.9, scale: 0.3 }, { opacity: 0, scale: 8, duration: 1.1, ease: 'power2.out' }, 1.6);
  // ripple resolves into the ingredient actor -- the hero of the frame.
  tl.to('#s01-actor-slot', { opacity: 1, scale: 1, rotation: 0, duration: 1.0, ease: 'back.out(1.5)' }, 2.1);
  // bottles slide in from opposing sides once the actor has claimed the center.
  tl.to('#s01-slot-a', { opacity: 1, x: 0, duration: 0.9, ease: 'power2.out' }, 2.9);
  tl.to('#s01-slot-b', { opacity: 1, x: 0, duration: 0.9, ease: 'power2.out' }, 3.1);
  tl.to('#s01-decl-l', { opacity: 1, duration: 0.8, ease: 'power2.out' }, 3.9);
  tl.to('#s01-decl-r', { opacity: 1, duration: 0.8, ease: 'power2.out' }, 4.1);
  tl.to('#s01-thesis', { opacity: 1, y: 0, duration: 1.0, ease: 'power3.out' }, 6.0);
""" + s01_extra_tweens + """
  tl.to({}, { duration: 15.777, ease: 'none' }, 0);
  window.__timelines = window.__timelines || {};
  window.__timelines['s01-bench-hook'] = tl;
"""
write("s01-bench-hook", style, body, script, bg="dark")

# ---------------------------------------------------------------- s02 -----
# Catalog source: ingredient-identity-map. Racing leaderboard fractures into
# an identity dossier -- five separate fields, not a ranked score -- with
# the passport reduced to a secondary corner motif per the brief's map.
style = """
  .pass-stage { position:relative; height:100%; width:100%;
    background: radial-gradient(120% 90% at 50% 15%, #1B1E1F 0%, var(--ink) 55%, #0A0B0B 100%); }
  .leaderboard { position:absolute; left:50%; top:32%; transform:translate(-50%,-50%);
    display:flex; gap:90px; opacity:0; }
  .lb-col { width:280px; font-family:var(--font-mono); font-size:26px; color:rgba(247,245,240,0.55); }
  .lb-row { display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.08); }
  .dossier { position:absolute; left:50%; top:30%; transform:translate(-50%,-50%);
    width:1560px; opacity:0; }
  .dossier-name { text-align:center; font-family:var(--font-display); font-weight:800; font-size:64px;
    color:var(--paper); letter-spacing:-.03em; margin-bottom:30px; }
  .dossier-fields { display:flex; gap:0; border-top:1px solid rgba(255,255,255,0.18); }
  .field { flex:1; min-width:0; padding:20px 22px; border-right:1px solid rgba(255,255,255,0.18); }
  .field:last-child { border-right:none; }
  .field-name { font-family:var(--font-mono); font-size:20px; color:rgba(247,245,240,0.5); margin-bottom:10px; }
  .field-value { font-weight:700; font-size:26px; color:var(--paper); line-height:1.25; margin-bottom:12px; min-height:64px; }
  .id-seal-wrap { position:absolute; right:-10px; top:-40px; opacity:0; transform:scale(0.5) rotate(-14deg); }
  .id-tag { font-family:var(--font-mono); font-size:22px; color:var(--assay); letter-spacing:.1em; margin-top:6px; text-align:center; }
  .thesis { position:absolute; left:0; right:0; bottom:calc(var(--safe-bottom) + 40px); text-align:center; opacity:0; }
"""
fields = [
    ("CONSUMER NAME", "Cica", "known"),
    ("LABEL DECLARATION", "Centella Asiatica Extract", "requires_context"),
    ("SOURCE", "Centella asiatica plant", "requires_context"),
    ("PROCESS OR FORM", "Not disclosed", "not_disclosed"),
    ("STUDIED-MATERIAL MATCH", "Not established", "not_established"),
]
field_html = "\n".join(
    f'<div class="field" id="s02-field-{i}"><div class="field-name">{name}</div>'
    f'<div class="field-value">{val}</div>{evidence_state_chip(f"s02-chip-{i}", state)}</div>'
    for i, (name, val, state) in enumerate(fields)
)
body = f'''
    <div class="pass-stage">
      <div class="leaderboard" id="s02-leaderboard">
        <div class="lb-col"><div class="lb-row"><span>1</span><span>CENTELLA EXTRACT</span></div><div class="lb-row"><span>2</span><span>NIACINAMIDE</span></div><div class="lb-row"><span>3</span><span>PANTHENOL</span></div></div>
        <div class="lb-col"><div class="lb-row"><span>1</span><span>CENTELLA EXTRACT</span></div><div class="lb-row"><span>2</span><span>MADECASSOSIDE</span></div><div class="lb-row"><span>3</span><span>NIACINAMIDE</span></div></div>
      </div>
      <div class="dossier" id="s02-dossier">
        <div class="dossier-name">Cica — Ingredient Identity Record</div>
        <div class="dossier-fields">{field_html}</div>
        <div class="id-seal-wrap" id="s02-seal-wrap">
          {question_seal("s02-seal", 1, "answered", size=110, bg="dark")}
          <div class="id-tag">IDENTITY ONLY</div>
        </div>
      </div>
      <div class="thesis" id="s02-thesis">
        <div class="head" style="color:var(--paper); font-size:72px;">A LIST IS A PASSPORT — NOT A SCORECARD</div>
      </div>
    </div>
'''
field_tweens = "\n".join(
    f"  tl.to('#s02-field-{i}', {{ opacity: 1, y: 0, duration: 0.4, ease: 'power2.out' }}, {4.5 + i*0.18:.2f});"
    for i in range(5)
)
script = f"""
  gsap.set('#s02-leaderboard', {{ opacity: 0 }});
  gsap.set('#s02-dossier', {{ opacity: 0, scale: 0.92 }});
  gsap.set('.field', {{ opacity: 0, y: 12 }});
  gsap.set('#s02-seal-wrap', {{ opacity: 0, scale: 0.5, rotation: -14 }});
  gsap.set('#s02-thesis', {{ opacity: 0, y: 16 }});

  var tl = gsap.timeline({{ paused: true }});
  tl.to('#s02-leaderboard', {{ opacity: 1, duration: 0.8, ease: 'power2.out' }}, 0.0);
  tl.to('#s02-leaderboard', {{ opacity: 0, y: -20, duration: 0.6, ease: 'power2.in' }}, 1.9);
  tl.to('#s02-dossier', {{ opacity: 1, scale: 1, duration: 0.9, ease: 'power3.out' }}, 4.3);
{field_tweens}
  tl.to('#s02-seal-wrap', {{ opacity: 1, scale: 1, rotation: -6, duration: 0.6, ease: 'back.out(2.2)' }}, 5.6);
  tl.to('#s02-thesis', {{ opacity: 1, y: 0, duration: 1.0, ease: 'power3.out' }}, 7.5);
  tl.to({{}}, {{ duration: 12.257, ease: 'none' }}, 0);
  window.__timelines = window.__timelines || {{}};
  window.__timelines['s02-scorecard-passport'] = tl;
"""
write("s02-scorecard-passport", style, body, script, bg="dark")

# ---------------------------------------------------------------- s03 -----
# Catalog source: five-question-progress. All five seals introduced unseen,
# in the brief's fixed order (quantity, identity, vehicle, evidence,
# boundary); Question 1 goes active at the very end -- not answered yet.
style = """
  .promise-stage { position:relative; height:100%; width:100%;
    background: radial-gradient(120% 90% at 50% 15%, #1B1E1F 0%, var(--ink) 55%, #0A0B0B 100%); }
  .bottle-pair-sm { position:absolute; left:50%; top:66%; transform:translate(-50%,-50%);
    display:flex; gap:220px; opacity:0.55; }
  .q-progress { position:absolute; left:50%; top:38%; transform:translate(-50%,-50%); }
  .promise-head { position:absolute; left:0; right:0; top:calc(var(--safe-top) + 20px); text-align:center; opacity:0; }
  .scanner-line { position:absolute; left:0; right:0; top:0; height:4px; background:var(--celadon);
    box-shadow:0 0 30px 6px var(--celadon); opacity:0; }
"""
seals_html = five_question_progress("s03-seal", states=["unseen"] * 5, size=150, gap=54, bg="dark")
body = f'''
    <div class="promise-stage">
      <div class="scanner-line" id="s03-scanner"></div>
      <div class="bottle-pair-sm" id="s03-bottles">
        {neutral_package_shell_svg("s03-bottle-a", width=140, height=280, variant="a", liquid_state="ambiguous")}
        {neutral_package_shell_svg("s03-bottle-b", width=140, height=280, variant="b", liquid_state="ambiguous")}
      </div>
      {seals_html}
      <div class="promise-head" id="s03-head">
        <div class="head" style="color:var(--paper); font-size:78px;">FIVE QUESTIONS. ONE VERDICT.</div>
      </div>
    </div>
'''
seal_ids = [f"s03-seal-{i}" for i in range(5)]
seal_sets = "\n".join(f"  gsap.set('#{sid}', {{ opacity: 0, scale: 0.4, rotation: -30 }});" for sid in seal_ids)
seal_tweens = "\n".join(
    f"  tl.to('#{sid}', {{ opacity: 1, scale: 1, rotation: 0, duration: 0.4, ease: 'back.out(2)' }}, {3.0 + i*0.5:.2f});"
    for i, sid in enumerate(seal_ids)
)
# "1 2 3 4 5 flash, wording withheld" beat: a quick sequential pulse across
# the seals' own numeral-free glyphs, four frames each at 30fps (~0.13s).
count_tweens = "\n".join(
    f"  tl.to('#{sid}', {{ scale: 1.16, duration: 0.13, ease: 'power2.out' }}, {6.5 + i*0.3:.2f});\n"
    f"  tl.to('#{sid}', {{ scale: 1.0, duration: 0.13, ease: 'power2.in' }}, {6.63 + i*0.3:.2f});"
    for i, sid in enumerate(seal_ids)
)
# [cadence] one tasteful camera-style breathing scale on the bottle pair
# spanning the quiet stretch before the headline lands.
s03_extra_tweens = (
    "  tl.to('#s03-bottles', { scale: 1.02, duration: 2.98, ease: 'sine.inOut' }, 2.6);\n"
    "  tl.to('#s03-bottles', { scale: 1.0, duration: 2.7, ease: 'sine.inOut' }, 5.62);\n"
)
script = f"""
  gsap.set('#s03-scanner', {{ opacity: 0, y: -10 }});
  gsap.set('#s03-bottles', {{ scale: 1 }});
  gsap.set('#s03-head', {{ opacity: 0, y: 16 }});
{seal_sets}
  var tl = gsap.timeline({{ paused: true }});
  tl.fromTo('#s03-scanner', {{ opacity: 1, y: -10 }}, {{ opacity: 1, y: 1090, duration: 3.0, ease: 'power1.inOut' }}, 0.0);
  tl.to('#s03-scanner', {{ opacity: 0, duration: 0.3 }}, 3.0);
{seal_tweens}
{s03_extra_tweens}
{count_tweens}
  tl.to('#s03-head', {{ opacity: 1, y: 0, duration: 1.0, ease: 'power3.out' }}, 8.5);
  // half-second silence, then Question 1 (quantity) goes active -- not answered.
  tl.to('#s03-seal-0-ring', {{ attr: {{ stroke: '#6358A7' }}, duration: 0.4, ease: 'power2.out' }}, 14.6);
  tl.to('#s03-seal-0-keyline', {{ attr: {{ stroke: '#6358A7' }}, duration: 0.4, ease: 'power2.out' }}, 14.6);
  tl.to('#s03-seal-0 .icon', {{ color: '#6358A7', scale: 1.08, duration: 0.4, ease: 'back.out(2)' }}, 14.6);
  tl.to({{}}, {{ duration: 15.136, ease: 'none' }}, 0);
  window.__timelines = window.__timelines || {{}};
  window.__timelines['s03-promise-seals'] = tl;
"""
write("s03-promise-seals", style, body, script, bg="dark")
