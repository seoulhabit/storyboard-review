#!/usr/bin/env python3
"""Scenes s04-s07: Q1 (order/dose) and Q2 (extract standardization)."""
from build_composition import write, stamp_svg

# ---------------------------------------------------------------- s04 -----
# Adapts catalog/visual-components/threshold-list (ranked list + cutoff rule
# + below-cutoff desaturate/scramble) restyled as the "paper canyon."
style = """
  .canyon { position:relative; height:100%; width:100%; display:flex; flex-direction:column; }
  .canyon-title { text-align:center; margin-top:10px; }
  .canyon-list { margin:30px auto 0; width:1100px; }
  .canyon-row { font-family:var(--font-mono); font-size:40px; padding:14px 0;
    border-bottom:1px solid var(--rule-strong); opacity:0; }
  .canyon-row.below { color:rgb(146,142,132); } /* check's own suggestedColor for the 0.55-opacity below-cutoff row, replacing var(--ink-3) which measured 2.67:1 against 3:1 */
  .cutoff-rule { width:100%; height:6px; margin:6px 0 12px; background:var(--vermilion);
    transform:scaleX(0); transform-origin:left center; }
  .cutoff-label { font-family:var(--font-mono); font-size:28px; color:var(--vermilion);
    letter-spacing:.1em; opacity:0; }
  .tag-row { position:absolute; left:0; right:0; bottom:calc(var(--safe-bottom) + 40px);
    text-align:center; opacity:0; }
  .tag-row .sub { font-size:56px; color:var(--vermilion); }
"""
above = ["CENTELLA ASIATICA EXTRACT", "WATER", "GLYCERIN", "NIACINAMIDE"]
below = ["PANTHENOL", "ALLANTOIN", "SODIUM HYALURONATE", "FRAGRANCE"]
rows_above = "\n".join(f'<div class="canyon-row" id="s04-above-{i}">{name}</div>' for i, name in enumerate(above))
rows_below = "\n".join(f'<div class="canyon-row below" id="s04-below-{i}">{name}</div>' for i, name in enumerate(below))
body = f'''
    <div class="canyon" id="s04-camera" style="transform-origin:50% 30%;">
      <div class="canyon-title"><div class="kicker">THE INGREDIENT LIST</div></div>
      <div class="canyon-list">
        {rows_above}
        <div class="cutoff-rule" id="s04-cutoff"></div>
        <div class="cutoff-label" id="s04-cutoff-label">1% — ORDER NO LONGER GUARANTEED</div>
        {rows_below}
        <div style="display:flex; gap:20px; margin-top:24px;">
          <div class="cite" id="s04-cite-fda">FDA · 21 CFR 701.3</div>
          <div class="cite" id="s04-cite-eu">EU · Reg. 1223/2009 Art. 19</div>
        </div>
      </div>
      <div class="tag-row" id="s04-tag1"><div class="sub">ORDER ≠ EXACT DOSE</div></div>
    </div>
'''
above_tweens = "\n".join(
    f"  tl.fromTo('#s04-above-{i}', {{opacity:0,y:10}}, {{opacity:1,y:0,duration:0.35,ease:'power3.out'}}, {1.2+i*0.3:.2f});"
    for i in range(len(above))
)
below_tweens = "\n".join(
    f"  tl.fromTo('#s04-below-{i}', {{opacity:0,y:10}}, {{opacity:0.55,y:0,duration:0.35,ease:'power3.out'}}, {4.6+i*0.3:.2f});"
    for i in range(len(below))
)
scramble = "\n".join([
    "  tl.to('#s04-below-2', { x: 22, duration: 0.35, ease: 'power2.inOut' }, 7.4);",
    "  tl.to('#s04-below-3', { x: -22, duration: 0.35, ease: 'power2.inOut' }, 7.4);",
    "  tl.to('#s04-below-2', { x: 0, duration: 0.35, ease: 'power2.inOut' }, 7.8);",
    "  tl.to('#s04-below-3', { x: 0, duration: 0.35, ease: 'power2.inOut' }, 7.8);",
])
script = f"""
  gsap.set('.canyon-row', {{ opacity: 0, y: 10 }});
  gsap.set('#s04-cutoff', {{ scaleX: 0 }});
  gsap.set('#s04-cutoff-label', {{ opacity: 0 }});
  gsap.set('#s04-tag1', {{ opacity: 0, y: 16 }});
  gsap.set('#s04-camera', {{ scale: 1.12, y: 40 }});
  gsap.set('#s04-cite-fda', {{ opacity: 0 }});
  gsap.set('#s04-cite-eu', {{ opacity: 0 }});

  var tl = gsap.timeline({{ paused: true }});
  // Camera dive into the canyon: whole-stage push-in, not an element reveal
  // [S6/A-9]. Settles before the first row lands so the read stays sharp.
  tl.to('#s04-camera', {{ scale: 1.0, y: 0, duration: 1.1, ease: 'power2.out' }}, 0.0);
{above_tweens}
  tl.fromTo('#s04-cutoff', {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.3, ease: 'power2.in' }}, 4.2);
  tl.to('#s04-cutoff-label', {{ opacity: 1, duration: 0.3, ease: 'power2.out' }}, 4.5);
  tl.to('#s04-cite-fda', {{ opacity: 1, duration: 0.4, ease: 'power2.out' }}, 5.0);
  tl.to('#s04-cite-eu', {{ opacity: 1, duration: 0.4, ease: 'power2.out' }}, 5.3);
{below_tweens}
{scramble}
  // The tag sits over the list's own bottom rows at this canvas size --
  // dim the list first so the tag never visually collides with live text
  // underneath it (caught on an extracted frame, not by `check`'s sampling).
  tl.to('.canyon-list', {{ opacity: 0.1, duration: 0.5, ease: 'power2.inOut' }}, 8.5);
  tl.to('#s04-tag1', {{ opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' }}, 9.0);
  tl.to('#s04-tag1', {{ opacity: 0, y: -10, duration: 0.5, ease: 'power2.in' }}, 12.5);
  tl.to({{}}, {{ duration: 20.319, ease: 'none' }}, 0);
  window.__timelines = window.__timelines || {{}};
  window.__timelines['s04-q1-canyon'] = tl;
"""
write("s04-q1-canyon", style, body, script, bg="paper")

# ---------------------------------------------------------------- s05 -----
style = """
  .dose-stage { position:relative; height:100%; width:100%; display:flex; flex-direction:column; justify-content:center; }
  .dose-row { display:flex; align-items:center; justify-content:space-around; padding:0 60px; }
  .dose-item { text-align:center; }
  .dose-dot { width:34px; height:34px; border-radius:50%; margin:0 auto 20px; }
  .dose-dot.small { background: var(--celadon); box-shadow: 0 0 0 0 var(--celadon); }
  .dose-dot.big { width:150px; height:150px; background: var(--ink-3); opacity:0.35; }
  .dose-label { font-family:var(--font-mono); font-size:30px; color:var(--ink-2); max-width:340px; }
  .msg { text-align:center; margin-top:60px; opacity:0; }
  .msg .body { font-size:48px; max-width:1200px; margin:0 auto; }
  .tag2 { position:absolute; left:0; right:0; bottom:calc(var(--safe-bottom) + 40px); text-align:center; opacity:0; }
  .tag2 .sub { font-size:56px; color:var(--vermilion); }
"""
body = '''
    <div class="dose-stage">
      <div class="dose-row">
        <div class="dose-item">
          <div class="dose-dot big" id="s05-bigdot"></div>
          <div class="dose-label">near the top — not automatically effective</div>
        </div>
        <div class="dose-item">
          <div class="dose-dot small" id="s05-smalldot"></div>
          <div class="dose-label">may be active at low levels</div>
          <div class="uf-badge" id="s05-flag" style="margin:14px auto 0;">○ UNSOURCED — no record in this system</div>
        </div>
      </div>
      <div class="msg" id="s05-msg"><div class="body">Unless a brand publishes the percentage — don't invent a number.</div></div>
      <div class="tag2" id="s05-tag2"><div class="sub">RANK, NOT QUANTITY</div></div>
    </div>
'''
script = """
  gsap.set('#s05-bigdot', { opacity: 0.35, scale: 1 });
  gsap.set('#s05-smalldot', { opacity: 0.5, scale: 1 });
  gsap.set('#s05-msg', { opacity: 0, y: 14 });
  gsap.set('#s05-tag2', { opacity: 0, y: 16 });
  gsap.set('#s05-flag', { opacity: 0 });

  var tl = gsap.timeline({ paused: true });
  tl.to('#s05-smalldot', { opacity: 1, scale: 1.3, duration: 0.5, ease: 'power2.out' }, 0.4);
  // [K-2] flag fires CONCURRENTLY with the claim it discloses, per C6 in
  // 01-story-brief.md -- not before, not after.
  tl.to('#s05-flag', { opacity: 1, duration: 0.4, ease: 'power2.out' }, 0.6);
  tl.to('#s05-flag', { opacity: 0, duration: 0.4, ease: 'power2.in' }, 10.5);
  tl.to('#s05-smalldot', { boxShadow: '0 0 0 24px rgba(147,184,150,0)', duration: 1.1, ease: 'power2.out' }, 0.4);
  tl.to('#s05-smalldot', { scale: 1, duration: 0.4, ease: 'power2.inOut' }, 0.9);
  tl.to('#s05-bigdot', { opacity: 0.2, duration: 0.8, ease: 'power2.out' }, 1.2);
  tl.to('#s05-msg', { opacity: 1, y: 0, duration: 1.0, ease: 'power3.out' }, 11.0);
  tl.to('#s05-tag2', { opacity: 1, y: 0, duration: 0.9, ease: 'power3.out' }, 15.5);
  tl.to({}, { duration: 18.762, ease: 'none' }, 0);
  window.__timelines = window.__timelines || {};
  window.__timelines['s05-q1-dose'] = tl;
"""
write("s05-q1-dose", style, body, script, bg="paper")

# ---------------------------------------------------------------- s06 -----
# Adapts catalog/visual-components/material-triptych (N materials, one celadon rail)
style = """
  .leaf-stage { position:relative; height:100%; width:100%; display:flex; flex-direction:column; justify-content:center; }
  .leaf-head { text-align:center; margin-bottom:40px; opacity:0; }
  .chambers { display:flex; justify-content:center; gap:64px; }
  .chamber { width:420px; border:2px solid var(--rule-strong); border-radius:20px; padding:32px;
    text-align:center; opacity:0; }
  .chamber-vial { width:120px; height:180px; margin:0 auto 20px; border-radius:16px;
    border:3px solid var(--ink-3); position:relative; overflow:hidden; }
  .chamber-fill { position:absolute; left:0; right:0; bottom:0; }
  .chamber-label { font-family:var(--font-mono); font-size:26px; color:var(--ink-2); letter-spacing:.06em; }
  .collapse-label { text-align:center; margin-top:44px; opacity:0; }
  .collapse-label .head { font-size:64px; }
  .rail { position:absolute; left:50%; bottom:calc(var(--safe-bottom) + 30px); width:0; height:5px;
    background:var(--celadon); transform:translateX(-50%); }
"""
chambers = [
    ("WATER EXTRACT", "#93B896", 0.55),
    ("SOLVENT EXTRACT", "#4F6B52", 0.72),
    ("PURIFIED COMPOUND", "#131516", 0.30),
]
chamber_html = "\n".join(
    f'''<div class="chamber" id="s06-chamber-{i}">
      <div class="chamber-vial"><div class="chamber-fill" style="height:{h*100:.0f}%; background:{c};"></div></div>
      <div class="chamber-label">{label}</div>
    </div>''' for i, (label, c, h) in enumerate(chambers)
)
body = f'''
    <div class="leaf-stage" id="s06-camera" style="transform-origin:50% 45%;">
      <div class="leaf-head" id="s06-head"><div class="kicker">CENTELLA ASIATICA EXTRACT — ONE NAME, THREE PROCESSES</div></div>
      <div class="chambers">
        {chamber_html}
      </div>
      <div class="rail" id="s06-rail"></div>
      <div class="collapse-label" id="s06-collapse">
        <div class="head">CENTELLA ASIATICA EXTRACT</div>
        <div class="cite" id="s06-cite" style="margin:20px auto 0;">J Cosmet Sci · 2020</div>
      </div>
    </div>
'''
chamber_tweens = "\n".join(
    f"  tl.to('#s06-chamber-{i}', {{ opacity: 1, y: 0, duration: 0.7, ease: 'power3.out' }}, {2.0+i*0.5:.2f});"
    for i in range(3)
)
script = f"""
  gsap.set('.chamber', {{ opacity: 0, y: 30 }});
  gsap.set('#s06-head', {{ opacity: 0, y: -10 }});
  gsap.set('#s06-camera', {{ scale: 1.10, y: -30 }});
  gsap.set('#s06-rail', {{ width: 0 }});
  gsap.set('#s06-collapse', {{ opacity: 0, scale: 0.9 }});
  gsap.set('#s06-cite', {{ opacity: 0 }});

  var tl = gsap.timeline({{ paused: true }});
  tl.to('#s06-camera', {{ scale: 1.0, y: 0, duration: 1.1, ease: 'power2.out' }}, 0.0);
  tl.to('#s06-head', {{ opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' }}, 0.3);
{chamber_tweens}
  tl.to('#s06-rail', {{ width: 900, duration: 0.9, ease: 'power2.inOut' }}, 14.5);
  tl.to('.chamber', {{ opacity: 0.25, duration: 0.6, ease: 'power2.inOut' }}, 15.6);
  tl.to('#s06-collapse', {{ opacity: 1, scale: 1, duration: 0.8, ease: 'back.out(1.5)' }}, 16.2);
  tl.to('#s06-cite', {{ opacity: 1, duration: 0.5, ease: 'power2.out' }}, 17.4);
  tl.to({{}}, {{ duration: 20.554, ease: 'none' }}, 0);
  window.__timelines = window.__timelines || {{}};
  window.__timelines['s06-q2-leaf-chambers'] = tl;
"""
write("s06-q2-leaf-chambers", style, body, script, bg="paper")

# ---------------------------------------------------------------- s07 -----
style = """
  .gate-stage { position:relative; height:100%; width:100%; display:flex; align-items:center; justify-content:center; flex-direction:column; }
  .gate-wrap { position:relative; width:900px; height:420px; display:flex; align-items:center; justify-content:center; }
  .traveler { position:absolute; width:26px; height:26px; border-radius:50%; opacity:0; }
  .gate-arch { width:6px; height:340px; background:var(--rule-strong); border-radius:4px; }
  .tag3 { text-align:center; margin-top:50px; opacity:0; }
  .tag3 .sub { font-size:56px; color:var(--vermilion); }
"""
travelers = [("#93B896", -260), ("#4F6B52", 0), ("#131516", 260)]
trav_html = "\n".join(
    f'<div class="traveler" id="s07-trav-{i}" style="background:{c}; left:calc(50% + {x-350}px); top:50%;"></div>'
    for i, (c, x) in enumerate(travelers)
)
script = """
  gsap.set('.traveler', { opacity: 0, x: -400 });
  gsap.set('#s07-tag', { opacity: 0, y: 16 });

  var tl = gsap.timeline({ paused: true });
  tl.to('#s07-trav-0', { opacity: 1, x: 700, duration: 3.0, ease: 'power1.inOut' }, 0.3);
  tl.to('#s07-trav-1', { opacity: 1, x: 700, duration: 3.0, ease: 'power1.inOut' }, 0.7);
  tl.to('#s07-trav-2', { opacity: 1, x: 700, duration: 3.0, ease: 'power1.inOut' }, 1.1);
  tl.to('.traveler', { opacity: 0, duration: 0.4 }, 4.4);
  tl.to('#s07-tag', { opacity: 1, y: 0, duration: 0.9, ease: 'power3.out' }, 4.9);
  tl.to({}, { duration: 8.012, ease: 'none' }, 0);
  window.__timelines = window.__timelines || {};
  window.__timelines['s07-q2-travelers'] = tl;
"""
body = f'''
    <div class="gate-stage">
      <div class="gate-wrap">
        <div class="gate-arch"></div>
        {trav_html}
      </div>
      <div class="tag3" id="s07-tag"><div class="sub">ONE NAME. MANY EXTRACTS.</div></div>
    </div>
'''
write("s07-q2-travelers", style, body, script, bg="paper")
