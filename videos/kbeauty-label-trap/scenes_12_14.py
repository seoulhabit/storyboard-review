#!/usr/bin/env python3
"""Scenes s12-s14: the reveal (exact bench reuse), recap card, end card."""
from build_composition import write, stamp_svg, bottle_svg

# ---------------------------------------------------------------- s12 -----
# [S6/A-9]: reuses s01's exact bench markup/geometry (same bottle_svg calls,
# same layout), NOT a rebuild -- only the liquid_kind data differs, which is
# what actually resolves the mystery (ambiguous -> lattice/water).
style = """
  .bench { position:relative; height:100%; width:100%;
    background: radial-gradient(120% 90% at 50% 15%, #1B1E1F 0%, var(--ink) 55%, #0A0B0B 100%); }
  .bench-surface { position:absolute; left:0; right:0; bottom:0; height:38%;
    background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(0,0,0,0.35));
    border-top:1px solid rgba(255,255,255,0.06); }
  .bottle-pair { position:absolute; left:50%; top:36%; transform:translate(-50%,-50%);
    display:flex; gap:220px; }
  .bottle-label { text-align:center; margin-top:18px; }
  .verdict-row { position:absolute; left:0; right:0; bottom:calc(var(--safe-bottom) + 60px);
    display:flex; justify-content:center; gap:340px; }
  .verdict { text-align:center; opacity:0; }
  .verdict .illus-tag { color:var(--ink-3); }
  .verdict .label { font-size:30px; margin-top:8px; }
  .verdict.a .label { color:var(--ink-3); }
  .verdict.b .label { color:var(--celadon); }
  .seal-row { position:absolute; left:50%; top:14%; transform:translate(-50%,0); display:flex; gap:24px; }
  .card-focus { position:absolute; left:0; right:0; bottom:calc(var(--safe-bottom) + 60px);
    text-align:center; opacity:0; }
  .card-focus .head { font-size:60px; color:var(--paper); }
"""
seal_row = "".join(stamp_svg(f"s12-sealf-{i}", str(i+1), size=80) for i in range(5))
body = f'''
    <div class="bench">
      <div class="bench-surface"></div>
      <div class="seal-row" id="s12-seals">{seal_row}</div>
      <div class="bottle-pair" id="s12-bottles">
        <div class="bottle-label">
          {bottle_svg("s12-bottle-a", 0, 0, 300, 150, "lattice")}
        </div>
        <div class="bottle-label">
          {bottle_svg("s12-bottle-b", 0, 0, 300, 150, "water")}
        </div>
      </div>
      <div class="verdict-row" id="s12-verdicts">
        <div class="verdict a"><div class="illus-tag">[Authored, illustrative — not a claim]</div><div class="label">MORE UNCERTAINTY</div></div>
        <div class="verdict b"><div class="illus-tag">[Authored, illustrative — not a claim]</div><div class="label">MORE DECISION-USEFUL INFORMATION</div></div>
      </div>
      <div class="card-focus" id="s12-card"><div class="head">FIVE QUESTIONS. ONE VERDICT.</div></div>
    </div>
'''
script = """
  gsap.set('#s12-bottles', { opacity: 1 });
  gsap.set('.verdict', { opacity: 0, y: 16 });
  gsap.set('#s12-card', { opacity: 0, y: 16 });
  gsap.set('#s12-seals', { opacity: 0.9 });

  var tl = gsap.timeline({ paused: true });
  tl.to('#s12-bottles', { opacity: 1, duration: 0.6, ease: 'power2.out' }, 0.0);
  tl.to('.verdict.a', { opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' }, 7.0);
  tl.to('.verdict.b', { opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' }, 7.6);
  tl.to('#s12-bottles', { opacity: 0.25, duration: 1.0, ease: 'power2.inOut' }, 17.0);
  tl.to('.verdict', { opacity: 0, duration: 0.6, ease: 'power2.in' }, 17.0);
  tl.to('#s12-card', { opacity: 1, y: 0, duration: 1.0, ease: 'power3.out' }, 18.2);
  tl.to({}, { duration: 25.425, ease: 'none' }, 0);
  window.__timelines = window.__timelines || {};
  window.__timelines['s12-reveal'] = tl;
"""
write("s12-reveal", style, body, script, bg="dark")

# ---------------------------------------------------------------- s13 -----
style = """
  .recap { position:relative; height:100%; width:100%; display:flex; flex-direction:column;
    align-items:center; justify-content:center; }
  .recap-card { width:1500px; border:2px solid var(--rule-strong); border-radius:24px; padding:60px;
    background: var(--mist, #F0EBE1); opacity:0; }
  .recap-row { display:flex; justify-content:space-between; padding:22px 0; border-bottom:1px solid var(--rule-strong); }
  .recap-row:last-child { border-bottom:none; }
  .recap-num { font-family:var(--font-mono); font-size:34px; color:var(--vermilion); width:60px; }
  .recap-q { font-family:var(--font-display); font-size:42px; }
"""
qs = [
    "How much is there?",
    "Which version is it?",
    "What formula carries it?",
    "What evidence matches the claim?",
    "Where does the answer stop?",
]
rows = "\n".join(
    f'<div class="recap-row" id="s13-row-{i}" style="opacity:0"><div class="recap-num">{i+1}</div><div class="recap-q">{q}</div></div>'
    for i, q in enumerate(qs)
)
body = f'''
    <div class="recap">
      <div class="recap-card" id="s13-card">
        {rows}
      </div>
    </div>
'''
row_tweens = "\n".join(
    f"  tl.to('#s13-row-{i}', {{ opacity: 1, duration: 0.5, ease: 'power2.out' }}, {1.2+i*0.9:.2f});"
    for i in range(5)
)
script = f"""
  gsap.set('#s13-card', {{ opacity: 0, y: 20 }});
  gsap.set('.recap-row', {{ opacity: 0 }});

  var tl = gsap.timeline({{ paused: true }});
  tl.to('#s13-card', {{ opacity: 1, y: 0, duration: 0.9, ease: 'power3.out' }}, 0.0);
{row_tweens}
  tl.to({{}}, {{ duration: 11.994, ease: 'none' }}, 0);
  window.__timelines = window.__timelines || {{}};
  window.__timelines['s13-recap-questions'] = tl;
"""
write("s13-recap-questions", style, body, script, bg="paper")

# ---------------------------------------------------------------- s14 -----
style = """
  .endcard { position:relative; height:100%; width:100%;
    background: radial-gradient(120% 90% at 50% 20%, #1B1E1F 0%, var(--ink) 55%, #0A0B0B 100%);
    display:flex; flex-direction:column; align-items:center; justify-content:center; }
  .lock-ring { position:relative; width:340px; height:340px; }
  .mark { position:absolute; inset:0; display:flex; align-items:center; justify-content:center;
    font-family:var(--font-display); font-size:120px; color:var(--celadon); opacity:0; }
  .end-head { text-align:center; margin-top:56px; opacity:0; }
  .end-head .head { color:var(--paper); font-size:64px; max-width:1300px; }
  .footer { margin-top:28px; opacity:0; color:var(--ink-3); font-size:30px; }
"""
seal_lock = "".join(stamp_svg(f"s14-seal-{i}", str(i+1), size=64) for i in range(5))
body = f'''
    <div class="endcard">
      <div class="lock-ring">
        <div id="s14-seals" style="display:flex; gap:14px; position:absolute; inset:0; align-items:center; justify-content:center;">{seal_lock}</div>
        <div class="mark" id="s14-mark">습</div>
      </div>
      <div class="end-head" id="s14-head"><div class="head">DON'T FOLLOW THE HYPE. FOLLOW THE QUESTION.</div></div>
      <div class="footer" id="s14-footer">Educational, not diagnostic.</div>
    </div>
'''
script = """
  gsap.set('#s14-seals', { opacity: 1, scale: 1 });
  gsap.set('#s14-mark', { opacity: 0, scale: 0.6 });
  gsap.set('#s14-head', { opacity: 0, y: 16 });
  gsap.set('#s14-footer', { opacity: 0 });

  var tl = gsap.timeline({ paused: true });
  tl.to('#s14-seals', { scale: 0.7, opacity: 0, duration: 0.8, ease: 'power2.in' }, 3.0);
  tl.to('#s14-mark', { opacity: 1, scale: 1, duration: 0.8, ease: 'back.out(1.6)' }, 3.4);
  tl.to('#s14-head', { opacity: 1, y: 0, duration: 1.0, ease: 'power3.out' }, 5.0);
  tl.to('#s14-footer', { opacity: 1, duration: 0.8, ease: 'power2.out' }, 6.6);
  tl.to({}, { duration: 9.451, ease: 'none' }, 0);
  window.__timelines = window.__timelines || {};
  window.__timelines['s14-landing'] = tl;
"""
write("s14-landing", style, body, script, bg="dark")
