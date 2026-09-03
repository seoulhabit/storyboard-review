#!/usr/bin/env python3
"""Scenes s01-s03: the bench hook, the passport thesis, the promise/seal tease."""
from build_composition import write, stamp_svg, bottle_svg

# ---------------------------------------------------------------- s01 -----
style = """
  .bench { position:relative; height:100%; width:100%;
    background: radial-gradient(120% 90% at 50% 15%, #1B1E1F 0%, var(--ink) 55%, #0A0B0B 100%); }
  .bench-surface { position:absolute; left:0; right:0; bottom:0; height:38%;
    background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(0,0,0,0.35));
    border-top:1px solid rgba(255,255,255,0.06); }
  .droplet { position:absolute; left:50%; top:8%; width:14px; height:14px; border-radius:50%;
    background: radial-gradient(circle at 35% 30%, #EAF2F0, var(--celadon) 70%); opacity:0; }
  .ripple { position:absolute; left:50%; top:52%; width:60px; height:16px; border-radius:50%;
    transform:translate(-50%,-50%); border:2px solid var(--celadon); opacity:0; }
  .bottle-pair { position:absolute; left:50%; top:46%; transform:translate(-50%,-40%);
    display:flex; gap:220px; opacity:0; }
  .bottle-label { text-align:center; margin-top:18px; }
  .emboss { font-family:var(--font-mono); font-size:26px; letter-spacing:.22em; color:var(--ink-3); }
  .ribbon { position:absolute; top:14%; width:220px; font-family:var(--font-mono); font-size:19px;
    line-height:1.35; letter-spacing:.02em; color:rgba(247,245,240,0.35); opacity:0; text-align:left; }
  .ribbon .item { margin-bottom:10px; color:rgba(247,245,240,0.35); }
  .ribbon .item:last-child { margin-bottom:0; }
  .ribbon.left { left:calc(50% - 400px); }
  .ribbon.right { left:calc(50% + 180px); }
  .thesis-row { position:absolute; left:0; right:0; bottom:calc(var(--safe-bottom) + 70px);
    text-align:center; opacity:0; }
  .thesis-row .head { font-size:88px; color:var(--paper); }
"""
# [design-critique fix] the two ingredient ribbons were set in rotated
# writing-mode:vertical-rl text -- unreadable at any viewing speed. Same
# ingredient-name lists, now laid out as horizontal micro-columns (one name
# per line) so they're actually parseable at a glance, while staying dim/
# small -- background texture, not the main read.
s01_ribbon_l_names = ["CENTELLA ASIATICA EXTRACT", "WATER", "GLYCERIN", "NIACINAMIDE",
                       "PANTHENOL", "SODIUM HYALURONATE", "ALLANTOIN", "FRAGRANCE"]
s01_ribbon_r_names = ["CENTELLA ASIATICA EXTRACT", "WATER", "BUTYLENE GLYCOL", "NIACINAMIDE",
                       "MADECASSOSIDE", "PANTHENOL", "ALLANTOIN", "FRAGRANCE"]
s01_ribbon_l_html = "\n        ".join(
    f'<div class="item" id="s01-ribbon-l-{i}">{n}</div>' for i, n in enumerate(s01_ribbon_l_names))
s01_ribbon_r_html = "\n        ".join(
    f'<div class="item" id="s01-ribbon-r-{i}">{n}</div>' for i, n in enumerate(s01_ribbon_r_names))
body = f'''
    <div class="bench">
      <div class="bench-surface"></div>
      <div class="droplet" id="s01-droplet"></div>
      <div class="ripple" id="s01-ripple"></div>
      <div class="ribbon left" id="s01-ribbon-l">
        {s01_ribbon_l_html}
      </div>
      <div class="ribbon right" id="s01-ribbon-r">
        {s01_ribbon_r_html}
      </div>
      <div class="bottle-pair" id="s01-bottles">
        <div class="bottle-label">
          {bottle_svg("s01-bottle-a", 0, 0, 380, 190, "ambiguous")}
          <div class="emboss">CICA</div>
        </div>
        <div class="bottle-label">
          {bottle_svg("s01-bottle-b", 0, 0, 380, 190, "ambiguous")}
          <div class="emboss">CICA</div>
        </div>
      </div>
      <div class="thesis-row" id="s01-thesis">
        <div class="head">SAME HERO. DIFFERENT FORMULA.</div>
      </div>
    </div>
'''
# [cadence-gate fix] 8.88s with no visible beat, t=6.50-15.25 scene-local --
# the droplet/ripple/bottles/ribbons/thesis sequence all lands by ~9.4s, then
# holds dead for the rest. Add: (1) a paced brightening cascade stepping down
# both ribbons (secondary re-emphasis of ingredient names already on screen,
# doubling as motion for the now-legible horizontal layout), and (2) a slow
# camera-style breathing scale on the bottle-pair for the beat sheet's own
# "camera holds on the two-bottle mystery, unresolved" -- chained .to() calls,
# not GSAP's repeat, per this project's paused-timeline convention.
_s01_ribbon_order = []
for _i in range(len(s01_ribbon_l_names)):
    _s01_ribbon_order.append(f"s01-ribbon-l-{_i}")
    _s01_ribbon_order.append(f"s01-ribbon-r-{_i}")
_s01_cascade_lines = []
for _idx, _elid in enumerate(_s01_ribbon_order):
    _t0 = 6.6 + _idx * 0.5
    _s01_cascade_lines.append(
        f"  tl.to('#{_elid}', {{ color: 'rgba(247,245,240,0.78)', duration: 0.35, ease: 'sine.out' }}, {_t0:.2f});")
    _s01_cascade_lines.append(
        f"  tl.to('#{_elid}', {{ color: 'rgba(247,245,240,0.35)', duration: 0.45, ease: 'sine.in' }}, {_t0 + 0.37:.2f});")
s01_extra_tweens = "\n".join(_s01_cascade_lines) + "\n" + (
    "  tl.to('#s01-bottles', { scale: 1.018, duration: 4.18, ease: 'sine.inOut' }, 6.6);\n"
    "  tl.to('#s01-bottles', { scale: 0.99, duration: 4.18, ease: 'sine.inOut' }, 10.82);\n"
    "  tl.to('#s01-bottles', { scale: 1.0, duration: 1.28, ease: 'sine.inOut' }, 15.02);\n"
)
script = """
  // [R-1] frame 0 must never be blank: the droplet starts already visible
  // (this IS the hook), not faded in from opacity 0.
  gsap.set('#s01-droplet', { opacity: 1, y: -20 });
  gsap.set('#s01-ripple', { opacity: 0, scale: 0.3 });
  gsap.set('#s01-bottles', { opacity: 0, y: 30, scale: 1 });
  gsap.set('#s01-ribbon-l', { opacity: 0, x: -20 });
  gsap.set('#s01-ribbon-r', { opacity: 0, x: 20 });
  gsap.set('#s01-thesis', { opacity: 0, y: 16 });

  var tl = gsap.timeline({ paused: true });
  tl.to('#s01-droplet', { opacity: 1, y: 240, duration: 1.6, ease: 'power1.in' }, 0.0);
  tl.to('#s01-droplet', { opacity: 0, duration: 0.15 }, 1.6);
  tl.fromTo('#s01-ripple', { opacity: 0.9, scale: 0.3 }, { opacity: 0, scale: 8, duration: 1.1, ease: 'power2.out' }, 1.6);
  tl.to('#s01-bottles', { opacity: 1, y: 0, duration: 1.1, ease: 'power2.out' }, 2.1);
  tl.to('#s01-ribbon-l', { opacity: 1, x: 0, duration: 1.0, ease: 'power2.out' }, 3.4);
  tl.to('#s01-ribbon-r', { opacity: 1, x: 0, duration: 1.0, ease: 'power2.out' }, 3.7);
  tl.to('#s01-thesis', { opacity: 1, y: 0, duration: 1.0, ease: 'power3.out' }, 6.0);
  tl.to('#s01-thesis', { opacity: 1, duration: 1.0 }, 9.0);
""" + s01_extra_tweens + """
  tl.to({}, { duration: 15.777, ease: 'none' }, 0);
  window.__timelines = window.__timelines || {};
  window.__timelines['s01-bench-hook'] = tl;
"""
write("s01-bench-hook", style, body, script, bg="dark")

# ---------------------------------------------------------------- s02 -----
style = """
  .pass-stage { position:relative; height:100%; width:100%;
    background: radial-gradient(120% 90% at 50% 15%, #1B1E1F 0%, var(--ink) 55%, #0A0B0B 100%);
    display:flex; align-items:center; justify-content:center; }
  .leaderboard { position:absolute; left:50%; top:26%; transform:translate(-50%,-50%);
    display:flex; gap:90px; opacity:0; }
  .lb-col { width:280px; font-family:var(--font-mono); font-size:26px; color:rgba(247,245,240,0.55); }
  .lb-row { display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.08); }
  .passport { position:relative; width:640px; height:420px; border-radius:14px;
    background: linear-gradient(160deg, #F7F5F0, #E9E4D8); opacity:0; transform:scale(0.85);
    box-shadow: 0 40px 80px rgba(0,0,0,0.5); padding:44px; }
  .passport-title { font-family:var(--font-mono); font-size:24px; letter-spacing:.18em; color:var(--ink-2); }
  .passport-name { font-family:var(--font-display); font-size:52px; color:var(--ink); margin-top:14px; }
  .passport-sub { font-family:var(--font-body); font-size:28px; color:var(--ink-2); margin-top:22px; line-height:1.4; }
  .passport-stamp-wrap { position:absolute; right:36px; bottom:36px; opacity:0; transform:scale(0.5); }
  .thesis { position:absolute; left:0; right:0; bottom:calc(var(--safe-bottom) + 50px); text-align:center; opacity:0; }
"""
body = f'''
    <div class="pass-stage">
      <div class="leaderboard" id="s02-leaderboard">
        <div class="lb-col"><div class="lb-row"><span>1</span><span>CENTELLA EXTRACT</span></div><div class="lb-row"><span>2</span><span>NIACINAMIDE</span></div><div class="lb-row"><span>3</span><span>PANTHENOL</span></div></div>
        <div class="lb-col"><div class="lb-row"><span>1</span><span>CENTELLA EXTRACT</span></div><div class="lb-row"><span>2</span><span>MADECASSOSIDE</span></div><div class="lb-row"><span>3</span><span>NIACINAMIDE</span></div></div>
      </div>
      <div class="passport" id="s02-passport">
        <div class="passport-title">INGREDIENT PASSPORT</div>
        <div class="passport-name">Centella Asiatica Extract</div>
        <div class="passport-sub">This document certifies identity only.<br>It does not certify performance.</div>
        <div class="passport-stamp-wrap" id="s02-stamp-wrap">
          {stamp_svg("s02-stamp", "ID ONLY", size=170)}
        </div>
      </div>
      <div class="thesis" id="s02-thesis">
        <div class="head" style="color:var(--paper); font-size:76px;">A LIST IS A PASSPORT — NOT A SCORECARD</div>
      </div>
    </div>
'''
script = """
  gsap.set('#s02-leaderboard', { opacity: 0 });
  gsap.set('#s02-passport', { opacity: 0, scale: 0.85 });
  gsap.set('#s02-stamp-wrap', { opacity: 0, scale: 0.5, rotation: -18 });
  gsap.set('#s02-thesis', { opacity: 0, y: 16 });

  var tl = gsap.timeline({ paused: true });
  tl.to('#s02-leaderboard', { opacity: 1, duration: 0.8, ease: 'power2.out' }, 0.0);
  tl.to('#s02-leaderboard', { opacity: 0, y: -20, duration: 0.6, ease: 'power2.in' }, 1.9);
  tl.to('#s02-passport', { opacity: 1, scale: 1, duration: 1.0, ease: 'back.out(1.4)' }, 2.4);
  tl.to('#s02-stamp-wrap', { opacity: 1, scale: 1, rotation: -6, duration: 0.6, ease: 'back.out(2.2)' }, 4.6);
  tl.to('#s02-thesis', { opacity: 1, y: 0, duration: 1.0, ease: 'power3.out' }, 6.6);
  tl.to({}, { duration: 12.257, ease: 'none' }, 0);
  window.__timelines = window.__timelines || {};
  window.__timelines['s02-scorecard-passport'] = tl;
"""
write("s02-scorecard-passport", style, body, script, bg="dark")

# ---------------------------------------------------------------- s03 -----
style = """
  .promise-stage { position:relative; height:100%; width:100%;
    background: radial-gradient(120% 90% at 50% 15%, #1B1E1F 0%, var(--ink) 55%, #0A0B0B 100%); }
  .bottle-pair-sm { position:absolute; left:50%; top:44%; transform:translate(-50%,-50%);
    display:flex; gap:260px; opacity:1; }
  .seal-ring { position:absolute; left:50%; top:44%; width:900px; height:520px;
    transform:translate(-50%,-50%); }
  .seal-slot { position:absolute; opacity:0; transform:scale(0.4) rotate(-30deg); }
  .promise-head { position:absolute; left:0; right:0; top:calc(var(--safe-top) + 20px); text-align:center; opacity:0; }
  .scanner-line { position:absolute; left:0; right:0; top:0; height:4px; background:var(--celadon);
    box-shadow:0 0 30px 6px var(--celadon); opacity:0; }
"""
seal_positions = [
    (-380, -170), (-190, 220), (0, -260), (190, 220), (380, -170),
]
seals_html = "\n".join(
    f'<div class="seal-slot" id="s03-seal-{i}" style="left:calc(50% + {dx}px); top:calc(44% + {dy}px);">'
    f'{stamp_svg(f"s03-seal-svg-{i}", str(i+1), size=110)}</div>'
    for i, (dx, dy) in enumerate(seal_positions)
)
body = f'''
    <div class="promise-stage">
      <div class="scanner-line" id="s03-scanner"></div>
      <div class="bottle-pair-sm" id="s03-bottles">
        {bottle_svg("s03-bottle-a", 0, 0, 300, 150, "ambiguous")}
        {bottle_svg("s03-bottle-b", 0, 0, 300, 150, "ambiguous")}
      </div>
      <div class="seal-ring">
        {seals_html}
      </div>
      <div class="promise-head" id="s03-head">
        <div class="head" style="color:var(--paper); font-size:80px;">FIVE QUESTIONS. ONE VERDICT.</div>
      </div>
    </div>
'''
seal_tweens = "\n".join(
    f"  tl.to('#s03-seal-{i}', {{ opacity: 1, scale: 1, rotation: 0, duration: 0.35, ease: 'back.out(2)' }}, {6.5 + i*0.22:.2f});"
    for i in range(5)
)
seal_sets = "\n".join(
    f"  gsap.set('#s03-seal-{i}', {{ opacity: 0, scale: 0.4, rotation: -30 }});"
    for i in range(5)
)
# [cadence-gate fix] 6.25s with no visible beat, roughly local t=2.4-8.5 --
# the scanner sweep and the five small seal pop-ins are individually too
# subtle to read as a "beat"; add one bigger, tasteful camera-style breathing
# scale on the bottle-pair spanning that stretch, matching s01's identical
# treatment of its own "hold on the mystery" beat. Settles just before the
# headline arrives at 8.5.
s03_extra_tweens = (
    "  tl.to('#s03-bottles', { scale: 1.02, duration: 2.98, ease: 'sine.inOut' }, 2.6);\n"
    "  tl.to('#s03-bottles', { scale: 1.0, duration: 2.7, ease: 'sine.inOut' }, 5.62);\n"
)
script = f"""
  gsap.set('#s03-scanner', {{ opacity: 0, y: -10 }});
  gsap.set('#s03-bottles', {{ opacity: 0.9, scale: 1 }});
  gsap.set('#s03-head', {{ opacity: 0, y: 16 }});
{seal_sets}
  var tl = gsap.timeline({{ paused: true }});
  tl.fromTo('#s03-scanner', {{ opacity: 1, y: -10 }}, {{ opacity: 1, y: 1090, duration: 3.0, ease: 'power1.inOut' }}, 0.0);
  tl.to('#s03-scanner', {{ opacity: 0, duration: 0.3 }}, 3.0);
{seal_tweens}
{s03_extra_tweens}
  tl.to('#s03-head', {{ opacity: 1, y: 0, duration: 1.0, ease: 'power3.out' }}, 8.5);
  tl.to({{}}, {{ duration: 15.136, ease: 'none' }}, 0);
  window.__timelines = window.__timelines || {{}};
  window.__timelines['s03-promise-seals'] = tl;
"""
write("s03-promise-seals", style, body, script, bg="dark")
