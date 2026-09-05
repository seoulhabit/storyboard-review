#!/usr/bin/env python3
"""Scenes s12-s14: the reveal (exact bench reuse), recap card, end card."""
from build_composition import write, stamp_svg, bottle_svg
from catalog_components import (
    ingredient_actor_svg, neutral_package_shell_svg, five_question_progress,
    question_seal, illustrative_disclosure, brand_mark_svg, QUESTIONS,
    icon_svg, evidence_state_chip,
)

# ---------------------------------------------------------------- s12 -----
# Catalog source: verdict-reveal pattern, reusing s01's exact actor-row
# helper/geometry ([S6/A-9]/reuse requirement) -- only liquid_state changes
# (ambiguous -> plain/structured) to resolve the mystery, plus a five-seal
# readout per bottle. No score, winner badge or checkmark -- ever.
style = """
  .bench { position:relative; height:100%; width:100%;
    background: radial-gradient(120% 90% at 50% 15%, #1B1E1F 0%, var(--ink) 55%, #0A0B0B 100%); }
  .bench-surface { position:absolute; left:0; right:0; bottom:0; height:38%;
    background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(0,0,0,0.35));
    border-top:1px solid rgba(255,255,255,0.06); }
  .actor-row { position:absolute; left:50%; top:26%;
    display:flex; align-items:center; justify-content:center; gap:130px; }
  .bottle-slot { text-align:center; }
  /* Anchored to the SAME bottle centers the actor-row's own flex math
     produces (bottle 150 + gap 130 + actor 190 + gap 130 + bottle 150 =>
     bottle centers sit at +-300px from page center) so the seal readout and
     verdict labels visibly belong to their own bottle, not a separately
     centered block that drifts out of alignment. */
  .seal-col { position:absolute; top:48%; display:flex; gap:12px; opacity:0; }
  .seal-col-a { left:calc(50% - 300px); transform:translateX(-50%); }
  .seal-col-b { left:calc(50% + 300px); transform:translateX(-50%); }
  .verdict-row { position:absolute; left:0; right:0; bottom:calc(var(--safe-bottom) + 70px); }
  .verdict { position:absolute; top:0; text-align:center; opacity:0; width:360px; }
  .verdict.a { left:calc(50% - 300px); }
  .verdict.b { left:calc(50% + 300px); }
  .verdict .label { font-size:28px; margin-top:8px; font-family:var(--font-display); font-weight:800; letter-spacing:-.01em; }
  .verdict.a .label { color:var(--ink-soft); }
  .verdict.b .label { color:var(--celadon); }
  .card-focus { position:absolute; left:0; right:0; bottom:calc(var(--safe-bottom) + 50px);
    text-align:center; opacity:0; }
  .card-focus .head { font-size:58px; color:var(--paper); }
  .card-focus .sub2 { margin-top:16px; font-size:32px; color:var(--ink-soft); font-family:var(--font-mono); }
"""
a_states = ["unknown", "unknown", "unknown", "active", "answered"]
b_states = ["active", "answered", "answered", "answered", "answered"]
seal_col_a = "".join(question_seal(f"s12-a-seal-{i}", i, "unseen", size=58, bg="dark") for i in range(5))
seal_col_b = "".join(question_seal(f"s12-b-seal-{i}", i, "unseen", size=58, bg="dark") for i in range(5))
_S12_COLOR = {"unknown": "#D95F52", "active": "#6358A7", "answered": "#426B50"}

body = f'''
    <div class="bench">
      <div class="bench-surface"></div>
      <div class="actor-row">
        <div class="bottle-slot" id="s12-slot-a">
          {neutral_package_shell_svg("s12-bottle-a", width=150, height=300, variant="a", liquid_state="plain")}
        </div>
        <div class="actor-slot" id="s12-actor-slot">{ingredient_actor_svg("s12-actor", size=190)}</div>
        <div class="bottle-slot" id="s12-slot-b">
          {neutral_package_shell_svg("s12-bottle-b", width=150, height=300, variant="b", liquid_state="structured")}
        </div>
      </div>
      <div class="seal-col seal-col-a" id="s12-seals-a">{seal_col_a}</div>
      <div class="seal-col seal-col-b" id="s12-seals-b">{seal_col_b}</div>
      <div class="verdict-row" id="s12-verdicts">
        <div class="verdict a">{illustrative_disclosure("s12-tag-a")}<div class="label">MORE UNCERTAINTY</div></div>
        <div class="verdict b">{illustrative_disclosure("s12-tag-b")}<div class="label">MORE DECISION-USEFUL INFORMATION</div></div>
      </div>
      <div class="card-focus" id="s12-card">
        <div class="head">FIVE QUESTIONS. ONE VERDICT.</div>
        <div class="sub2">NOT AUTOMATICALLY BETTER</div>
      </div>
    </div>
'''
a_seal_tweens = "\n".join(
    f"  tl.to('#s12-a-seal-{i}-ring', {{ attr: {{ stroke: '{_S12_COLOR[s]}' }}, duration: 0.35, ease: 'power2.out' }}, {1.2 + i*0.7:.2f});\n"
    f"  tl.to('#s12-a-seal-{i}-keyline', {{ attr: {{ stroke: '{_S12_COLOR[s]}' }}, duration: 0.35, ease: 'power2.out' }}, {1.2 + i*0.7:.2f});\n"
    f"  tl.to('#s12-a-seal-{i} .icon', {{ color: '{_S12_COLOR[s]}', scale: 1.08, duration: 0.35, ease: 'back.out(2)' }}, {1.2 + i*0.7:.2f});"
    for i, s in enumerate(a_states)
)
b_seal_tweens = "\n".join(
    f"  tl.to('#s12-b-seal-{i}-ring', {{ attr: {{ stroke: '{_S12_COLOR[s]}' }}, duration: 0.35, ease: 'power2.out' }}, {7.2 + i*0.7:.2f});\n"
    f"  tl.to('#s12-b-seal-{i}-keyline', {{ attr: {{ stroke: '{_S12_COLOR[s]}' }}, duration: 0.35, ease: 'power2.out' }}, {7.2 + i*0.7:.2f});\n"
    f"  tl.to('#s12-b-seal-{i} .icon', {{ color: '{_S12_COLOR[s]}', scale: 1.08, duration: 0.35, ease: 'back.out(2)' }}, {7.2 + i*0.7:.2f});"
    for i, s in enumerate(b_states)
)
script = f"""
  gsap.set('.actor-row', {{ opacity: 0, y: 20, xPercent: -50 }});
  gsap.set('.seal-col', {{ opacity: 0 }});
  gsap.set('.verdict', {{ opacity: 0, y: 16, xPercent: -50 }});
  gsap.set('#s12-card', {{ opacity: 0, y: 16 }});

  var tl = gsap.timeline({{ paused: true }});
  tl.to('.actor-row', {{ opacity: 1, y: 0, duration: 0.8, ease: 'power2.out' }}, 0.0);
  tl.to('#s12-seals-a', {{ opacity: 1, duration: 0.4, ease: 'power2.out' }}, 1.0);
{a_seal_tweens}
  tl.to('#s12-seals-b', {{ opacity: 1, duration: 0.4, ease: 'power2.out' }}, 7.0);
{b_seal_tweens}
  tl.to('.verdict.a', {{ opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' }}, 13.0);
  tl.to('.verdict.b', {{ opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' }}, 13.6);
  // camera chooses no bottle -- both recede together, card-focus takes the frame.
  tl.to('.actor-row', {{ opacity: 0.2, duration: 1.0, ease: 'power2.inOut' }}, 17.0);
  tl.to('.seal-col', {{ opacity: 0.2, duration: 1.0, ease: 'power2.inOut' }}, 17.0);
  tl.to('.verdict', {{ opacity: 0, duration: 0.6, ease: 'power2.in' }}, 17.0);
  tl.to('#s12-card', {{ opacity: 1, y: 0, duration: 1.0, ease: 'power3.out' }}, 18.2);
  tl.to({{}}, {{ duration: 25.425, ease: 'none' }}, 0);
  window.__timelines = window.__timelines || {{}};
  window.__timelines['s12-reveal'] = tl;
"""
write("s12-reveal", style, body, script, bg="dark")

# ---------------------------------------------------------------- s13 -----
# Catalog source: five-question-recap pattern. The ingredient actor stays
# visible on the left -- this is a recap of ingredient literacy, not a bare
# checklist -- while five compact rows carry each question's own glyph,
# short label, and the Cica-specific answer state already established
# across s03-s11. No full-sentence captions.
style = """
  .recap { position:relative; height:100%; width:100%; display:flex; align-items:center; justify-content:center; gap:120px; }
  .recap-actor { text-align:center; opacity:0; }
  .recap-actor .name { margin-top:18px; font-weight:800; font-size:34px; letter-spacing:-.02em; }
  .recap-rows { display:flex; flex-direction:column; width:1080px; }
  .recap-row { display:grid; grid-template-columns:70px 260px 1fr auto; align-items:center; gap:22px;
    padding:20px 0; border-bottom:1px solid var(--line); opacity:0; }
  .recap-row:last-child { border-bottom:none; }
  .recap-q { font-weight:700; font-size:28px; letter-spacing:-.01em; }
  .recap-a { color:var(--ink-soft); font-size:22px; }
"""
QS = [
    ("quantity", "How much?", "Rank, not exact amount", "requires_context"),
    ("identity-version", "Which version?", "Process undisclosed", "unknown"),
    ("formula-vehicle", "What carries it?", "Formula-specific", "unknown"),
    ("evidence", "What evidence?", "Material match required", "requires_context"),
    ("boundary", "Where does it stop?", "Identity &ne; performance", "known"),
]
rows = "\n".join(
    f'<div class="recap-row" id="s13-row-{i}">{icon_svg(f"s13-icon-{i}", icon, size=44, color="var(--ink-soft)")}'
    f'<div class="recap-q">{q}</div><div class="recap-a">{a}</div>{evidence_state_chip(f"s13-chip-{i}", state)}</div>'
    for i, (icon, q, a, state) in enumerate(QS)
)
body = f'''
    <div class="recap">
      <div class="recap-actor" id="s13-actor">{ingredient_actor_svg("s13-actor-svg", size=260)}<div class="name">CICA</div></div>
      <div class="recap-rows" id="s13-rows">{rows}</div>
    </div>
'''
row_tweens = "\n".join(
    f"  tl.to('#s13-row-{i}', {{ opacity: 1, duration: 0.5, ease: 'power2.out' }}, {1.4+i*0.7:.2f});"
    for i in range(5)
)
# Idle beat for the hold after all five rows land (~6.5s) through the scene's
# own end (11.994s): a soft, slow pulse across the icon glyphs, in sequence.
ICON_SELECTORS = [f"#s13-icon-{i}" for i in range(5)]
_pulse_lines = []
for _ws in [7.0, 9.6]:
    for _i, _sel in enumerate(ICON_SELECTORS):
        _t0 = _ws + _i * 0.35
        _t1 = _t0 + 0.4 + 0.02
        _pulse_lines.append(f"  tl.to('{_sel}', {{ scale: 1.15, duration: 0.4, ease: 'sine.inOut' }}, {_t0:.2f});")
        _pulse_lines.append(f"  tl.to('{_sel}', {{ scale: 1.0, duration: 0.4, ease: 'sine.inOut' }}, {_t1:.2f});")
icon_pulse_js = "\n".join(_pulse_lines)

script = f"""
  gsap.set('#s13-actor', {{ opacity: 0, x: -20 }});
  gsap.set('.recap-row', {{ opacity: 0, x: 14 }});
  gsap.set('.icon', {{ transformOrigin: '50% 50%' }});

  var tl = gsap.timeline({{ paused: true }});
  tl.to('#s13-actor', {{ opacity: 1, x: 0, duration: 0.8, ease: 'power2.out' }}, 0.0);
{row_tweens}
{icon_pulse_js}
  tl.to({{}}, {{ duration: 11.994, ease: 'none' }}, 0);
  window.__timelines = window.__timelines || {{}};
  window.__timelines['s13-recap-questions'] = tl;
"""
write("s13-recap-questions", style, body, script, bg="paper")

# ---------------------------------------------------------------- s14 -----
# Reuses the ingredient actor and five-question seals one final time; the
# 습 mark is the one allowed brand touchpoint (final landing) -- the real
# seoulhabit-mark.svg asset, not a plain-text glyph.
style = """
  .endcard { position:relative; height:100%; width:100%;
    background: radial-gradient(120% 90% at 50% 20%, #1B1E1F 0%, var(--ink) 55%, #0A0B0B 100%);
    display:flex; flex-direction:column; align-items:center; justify-content:center; }
  .lock-ring { position:relative; width:340px; height:340px; }
  .actor-recede { position:absolute; inset:0; display:flex; align-items:center; justify-content:center; }
  .mark-wrap { position:absolute; inset:0; display:flex; align-items:center; justify-content:center; opacity:0; }
  .end-head { text-align:center; margin-top:56px; opacity:0; }
  .end-head .head { color:var(--paper); font-size:64px; max-width:1300px; }
  .footer { margin-top:28px; opacity:0; color:var(--ink-3); font-size:30px; font-family:var(--font-mono); }
"""
final_states = ["answered", "answered", "answered", "answered", "answered"]
seal_lock = "".join(question_seal(f"s14-seal-{i}", i, "answered", size=68, bg="dark") for i in range(5))
seal_ids = [f"s14-seal-{i}" for i in range(5)]
body = f'''
    <div class="endcard">
      <div class="lock-ring">
        <div class="actor-recede" id="s14-actor-wrap">{ingredient_actor_svg("s14-actor", size=170)}</div>
        <div id="s14-seals" style="display:flex; gap:12px; position:absolute; inset:0; align-items:center; justify-content:center;">{seal_lock}</div>
        <div class="mark-wrap" id="s14-mark-wrap">{brand_mark_svg("s14-mark", size=210)}</div>
      </div>
      <div class="end-head" id="s14-head"><div class="head">DON'T FOLLOW THE HYPE. FOLLOW THE QUESTION.</div></div>
      <div class="footer" id="s14-footer">Educational, not diagnostic.</div>
    </div>
'''
converge_tweens = "\n".join(
    f"  tl.to('#{sid}', {{ x: 0, y: 0, scale: 0.6, duration: 0.9, ease: 'power2.inOut' }}, 0.6);"
    for sid in seal_ids
)
script = f"""
  gsap.set('#s14-actor-wrap', {{ opacity: 0.5, scale: 0.9 }});
  gsap.set('#s14-seals', {{ opacity: 1 }});
  gsap.set('#s14-mark-wrap', {{ opacity: 0, scale: 0.6 }});
  gsap.set('#s14-head', {{ opacity: 0, y: 16 }});
  gsap.set('#s14-footer', {{ opacity: 0 }});

  var tl = gsap.timeline({{ paused: true }});
  // five seals converge into a single decision boundary; the actor recedes
  // but stays visible underneath so the mark reads as ITS resolution.
{converge_tweens}
  tl.to('#s14-actor-wrap', {{ opacity: 0.15, scale: 0.75, duration: 0.9, ease: 'power2.inOut' }}, 0.6);
  tl.to('#s14-seals', {{ scale: 0.7, opacity: 0, duration: 0.8, ease: 'power2.in' }}, 3.0);
  // match-cut: the seal cluster's own circular field becomes the mark's disc.
  tl.to('#s14-mark-wrap', {{ opacity: 1, scale: 1, duration: 0.8, ease: 'back.out(1.6)' }}, 3.4);
  tl.to('#s14-head', {{ opacity: 1, y: 0, duration: 1.0, ease: 'power3.out' }}, 5.0);
  tl.to('#s14-footer', {{ opacity: 1, duration: 0.8, ease: 'power2.out' }}, 6.6);
  tl.to({{}}, {{ duration: 9.451, ease: 'none' }}, 0);
  window.__timelines = window.__timelines || {{}};
  window.__timelines['s14-landing'] = tl;
"""
write("s14-landing", style, body, script, bg="dark")
