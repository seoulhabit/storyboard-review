#!/usr/bin/env python3
"""Scenes s04-s07: Q1 (order/dose) and Q2 (extract standardization)."""
from build_composition import write, stamp_svg
from catalog_components import (
    ingredient_actor_svg, evidence_state_chip, citation_chip, illustrative_disclosure, icon_svg,
    question_seal,
)


def order_map_markup(uid, ingredients, threshold_after, selected_idx):
    """Catalog source: ingredient-order-map. Shared by s04 (full list) and
    s05 (pushed-in state on one row) -- same receipt + analysis structure,
    only the selection/zoom differs, per the brief's reuse requirement."""
    rows = []
    for i, name in enumerate(ingredients):
        cls = " selected" if i == selected_idx else ""
        rows.append(
            f'<div class="om-row{cls}" id="{uid}-row-{i}"><span class="om-rank">{i+1:02d}</span>'
            f'<span class="om-name">{name}</span><span class="om-amount">unknown</span></div>')
        if i == threshold_after:
            rows.append(f'<div class="om-threshold" id="{uid}-threshold"><span>1% teaching line</span></div>')
    return "\n".join(rows)


def order_map_finding(uid, can_value, can_note, verdict_text):
    return f'''<div class="om-finding-grid">
    <article class="om-finding"><div class="om-finding-title">The list can show</div>
      <div class="om-finding-value" id="{uid}-can">{can_value}</div>
      <div class="om-finding-note" id="{uid}-can-note">{can_note}</div></article>
    <article class="om-finding cannot"><div class="om-finding-title">The list cannot show</div>
      <div class="om-finding-value">Exact amount <span class="om-precision">??%</span></div>
      <div class="om-finding-note">Do not reverse-engineer a percentage from rank alone.</div></article>
  </div>
  <div class="om-verdict" id="{uid}-verdict">{verdict_text}</div>'''


ORDER_MAP_CSS = """
  .om-wrap { display:flex; gap:70px; align-items:stretch; }
  .om-receipt { position:relative; width:660px; flex:none; padding:34px 36px; border:1px solid var(--line);
    border-radius:20px; background:rgba(255,255,255,0.6); }
  .om-receipt-title { display:flex; justify-content:space-between; padding-bottom:12px;
    border-bottom:1px solid var(--line); color:var(--ink-soft); font-family:var(--font-mono); font-size:20px; }
  .om-rows { margin-top:6px; }
  .om-row { position:relative; display:grid; grid-template-columns:36px 1fr auto; align-items:center;
    gap:12px; min-height:56px; border-bottom:1px solid rgba(23,35,50,.09); color:var(--ink-soft); font-size:24px; opacity:0; }
  .om-rank { font-family:var(--font-mono); font-size:18px; color:rgb(90,94,99); }
  .om-amount { font-family:var(--font-mono); min-width:70px; padding:4px 8px; border-radius:6px;
    background:repeating-linear-gradient(135deg, rgba(23,35,50,.65) 0 4px, transparent 4px 8px);
    background-clip:text; -webkit-background-clip:text; color:transparent; -webkit-text-fill-color:transparent;
    text-align:center; }
  .om-row.selected { color:var(--ink); font-weight:700; }
  .om-row.selected::after { content:""; position:absolute; inset:5px -8px; border:2px solid var(--assay); border-radius:8px; }
  .om-threshold { display:flex; align-items:center; gap:12px; margin:6px 0; color:#B23D2C;
    font-family:var(--font-mono); font-size:18px; opacity:0; }
  .om-threshold::after { content:""; flex:1; height:2px; background:var(--signal); }
  .om-flexzone { position:absolute; left:8px; right:0; bottom:8px; height:0; background:rgba(217,95,82,.06);
    border-radius:0 0 18px 12px; }
  .om-analysis { flex:1; min-width:0; display:flex; flex-direction:column; justify-content:center; gap:32px; }
  .om-finding-grid { display:grid; grid-template-columns:1fr 1fr; gap:26px; }
  .om-finding { position:relative; min-height:200px; padding:30px; border-top:6px solid var(--celadon);
    background:rgba(255,255,255,0.55); opacity:0; }
  .om-finding.cannot { border-color:var(--signal); }
  .om-finding-title { color:var(--ink-soft); font-size:22px; }
  .om-finding-value { margin-top:26px; font-size:34px; font-weight:700; letter-spacing:-.02em; }
  .om-finding-note { position:absolute; left:30px; right:30px; bottom:24px; color:var(--ink-soft); font-size:20px; line-height:1.35; }
  .om-precision { display:inline-block; margin-left:6px; padding:0 .22em; border-radius:4px;
    background:repeating-linear-gradient(135deg, var(--ink) 0 7px, #334052 7px 12px);
    background-clip:text; -webkit-background-clip:text; color:transparent; -webkit-text-fill-color:transparent; }
  .om-verdict { display:flex; align-items:center; gap:18px; padding:22px 28px; border-radius:14px;
    color:var(--paper); background:var(--ink); font-size:30px; font-weight:600; opacity:0; }
  .om-verdict::before { content:"\\2260"; display:grid; place-items:center; flex:none; width:52px; height:52px;
    border:2px solid var(--signal); border-radius:50%; color:var(--signal); font-size:1.3em; }
"""


def spv_station(uid, role, icon_name, title, copy, state, variables=None, actor=False):
    """One station in the Source / Process / Version-in-formula map (s06/s07's
    shared component). `actor=True` swaps the generic icon for the persistent
    ingredient actor itself -- used at the Source station so the same leaf
    that opened the scene visibly becomes "the source", not a redrawn icon."""
    glyph = ingredient_actor_svg(f"{uid}-icon", size=64) if actor else icon_svg(f"{uid}-icon", icon_name, size=48, color="var(--ink)")
    var_html = ""
    if variables:
        chips = "".join(
            f'<span class="spv-var {"unknown" if st != "known" else ""}" style="border:1px solid var(--line);'
            f'border-radius:999px;padding:5px 14px;font-family:var(--font-mono);font-size:20px;'
            f'color:{"var(--signal)" if st != "known" else "var(--ink-soft)"};'
            f'{"border-style:dashed;" if st != "known" else ""}margin-right:8px;">{name}</span>'
            for name, st in variables
        )
        var_html = f'<div style="margin-top:14px;">{chips}</div>'
    return f'''<div class="spv-station" id="{uid}" style="position:relative;flex:1;min-width:0;
      padding:28px 30px;border:1px solid var(--line);border-radius:22px;
      background:rgba(255,255,255,0.55);">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;">
      <span class="label" style="color:var(--ink-soft);font-size:24px;">{role}</span>
      {evidence_state_chip(f"{uid}-state", state)}
    </div>
    <div style="width:68px;height:68px;border-radius:50%;border:1px solid var(--line);
      background:rgba(255,255,255,0.7);display:flex;align-items:center;justify-content:center;margin-bottom:16px;">{glyph}</div>
    <div style="font-weight:800;font-size:36px;letter-spacing:-.02em;margin-bottom:8px;">{title}</div>
    <div style="color:var(--ink-soft);font-size:22px;line-height:1.4;max-width:30ch;">{copy}</div>
    {var_html}
  </div>'''


def spv_connector(uid):
    return (f'<div class="spv-connector" id="{uid}" style="flex:0 0 74px;display:flex;align-items:center;'
            f'justify-content:center;position:relative;">'
            f'<div style="width:100%;height:1px;background:var(--ink);"></div>'
            f'<div style="position:absolute;width:32px;height:32px;border-radius:50%;border:1px solid var(--line);'
            f'background:var(--paper);"></div></div>')

# ---------------------------------------------------------------- s04 -----
# Catalog source: ingredient-order-map, full-list state. Receipt (ranked
# declaration + flexible zone) on the left, analysis panel (can-show /
# cannot-show + verdict) on the right -- s05 reuses this same structure.
style = ORDER_MAP_CSS + """
  .om-stage { position:relative; height:100%; width:100%; display:flex; flex-direction:column; justify-content:center; }
  .om-head { text-align:center; margin-bottom:34px; opacity:0; }
  .om-cites { display:flex; gap:18px; margin-top:22px; opacity:0; }
  .tag-row { margin-top:34px; text-align:center; opacity:0; }
  .tag-row .sub { font-size:52px; color:var(--signal); }
  .tag-row .sub2 { margin-top:10px; font-size:52px; color:var(--ink); }
"""
INGREDIENTS_S04 = ["Centella Asiatica Extract", "Water", "Glycerin", "Niacinamide",
                    "Panthenol", "Allantoin", "Sodium Hyaluronate", "Fragrance"]
s04_rows = order_map_markup("s04", INGREDIENTS_S04, threshold_after=3, selected_idx=0)
s04_finding = order_map_finding("s04", "Relative position",
    "Centella Asiatica Extract appears first in this fictional list.",
    "Rank is visible. Quantity remains unknown.")
body = f'''
    <div class="om-stage" id="s04-camera" style="transform-origin:50% 40%;">
      <div class="om-head" id="s04-head"><div class="kicker">THE INGREDIENT DECLARATION</div></div>
      <div class="om-wrap">
        <div class="om-receipt" id="s04-receipt">
          <div class="om-receipt-title"><span>Ingredient declaration</span><span>Exact percentages undisclosed</span></div>
          <div class="om-rows" id="s04-rows">{s04_rows}</div>
          <div class="om-flexzone" id="s04-flexzone"></div>
        </div>
        <div class="om-analysis">
          {s04_finding}
          <div class="om-cites" id="s04-cites">
            {citation_chip("s04-cite-fda", "FDA &middot; 21 CFR 701.3")}
            {citation_chip("s04-cite-eu", "EU &middot; Reg. 1223/2009 Art. 19")}
          </div>
        </div>
      </div>
      <div class="tag-row" id="s04-tag1"><div class="sub">ORDER &ne; EXACT DOSE</div><div class="sub2">RANK, NOT QUANTITY</div></div>
    </div>
'''
row_tweens = "\n".join(
    f"  tl.fromTo('#s04-row-{i}', {{opacity:0,y:10}}, {{opacity:1,y:0,duration:0.32,ease:'power3.out'}}, {1.4+i*0.28:.2f});"
    for i in range(len(INGREDIENTS_S04))
)
scramble = "\n".join([
    "  tl.to('#s04-row-5', { x: 22, duration: 0.35, ease: 'power2.inOut' }, 8.2);",
    "  tl.to('#s04-row-6', { x: -22, duration: 0.35, ease: 'power2.inOut' }, 8.2);",
    "  tl.to('#s04-row-5', { x: 0, duration: 0.35, ease: 'power2.inOut' }, 8.6);",
    "  tl.to('#s04-row-6', { x: 0, duration: 0.35, ease: 'power2.inOut' }, 8.6);",
])
script = f"""
  gsap.set('#s04-head', {{ opacity: 0, y: -10 }});
  gsap.set('.om-row', {{ opacity: 0, y: 10 }});
  gsap.set('#s04-threshold', {{ opacity: 0 }});
  gsap.set('#s04-flexzone', {{ height: 0 }});
  gsap.set('.om-finding', {{ opacity: 0, y: 16 }});
  gsap.set('.om-verdict', {{ opacity: 0, y: 16 }});
  gsap.set('#s04-cites', {{ opacity: 0 }});
  gsap.set('#s04-tag1', {{ opacity: 0, y: 16 }});
  gsap.set('#s04-camera', {{ scale: 1.1, y: 30 }});

  var tl = gsap.timeline({{ paused: true }});
  tl.to('#s04-camera', {{ scale: 1.0, y: 0, duration: 1.1, ease: 'power2.out' }}, 0.0);
  tl.to('#s04-head', {{ opacity: 1, y: 0, duration: 0.7, ease: 'power3.out' }}, 0.6);
{row_tweens}
  tl.to('#s04-threshold', {{ opacity: 1, duration: 0.3, ease: 'power2.out' }}, 4.6);
  tl.to('#s04-flexzone', {{ height: 168, duration: 0.6, ease: 'power2.out' }}, 4.9);
  tl.to('#s04-cites', {{ opacity: 1, duration: 0.4, ease: 'power2.out' }}, 5.4);
{scramble}
  tl.to('.om-finding', {{ opacity: 1, y: 0, duration: 0.6, ease: 'power3.out', stagger: 0.15 }}, 10.6);
  tl.to('.om-verdict', {{ opacity: 1, y: 0, duration: 0.6, ease: 'power3.out' }}, 11.4);
  tl.to('#s04-tag1', {{ opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' }}, 13.0);
  tl.to('#s04-tag1', {{ scale: 1.02, duration: 3.0, ease: 'sine.inOut' }}, 14.0);
  tl.to('#s04-tag1', {{ scale: 1.0, duration: 3.0, ease: 'sine.inOut' }}, 17.0);
  tl.to({{}}, {{ duration: 20.319, ease: 'none' }}, 0);
  window.__timelines = window.__timelines || {{}};
  window.__timelines['s04-q1-canyon'] = tl;
"""
write("s04-q1-canyon", style, body, script, bg="paper")

# ---------------------------------------------------------------- s05 -----
# Same Ingredient Order Map, pushed into a closer state on one below-the-
# line row -- s04 and s05 are two states of one component, not unrelated
# illustrations, per the brief's reuse requirement. UnsourcedFlag (#s05-flag)
# keeps its exact content/timing; closes with the Q1 seal turning face-up.
style = ORDER_MAP_CSS + """
  .om-stage { position:relative; height:100%; width:100%; display:flex; flex-direction:column; justify-content:center; }
  .om-push { transform-origin:36% 45%; }
  .msg { text-align:center; margin-top:36px; opacity:0; }
  .msg .body { font-size:44px; max-width:1300px; margin:0 auto; }
  .tag2 { position:absolute; left:0; right:0; bottom:calc(var(--safe-bottom) + 30px); text-align:center; opacity:0; }
  .tag2 .sub { font-size:52px; color:var(--signal); }
  .seal-lock { position:absolute; right:calc(var(--safe-right) + 40px); bottom:calc(var(--safe-bottom) + 30px);
    opacity:0; transform:scale(0.5); }
"""
INGREDIENTS_S05 = INGREDIENTS_S04
s05_rows = order_map_markup("s05", INGREDIENTS_S05, threshold_after=3, selected_idx=4)
s05_finding = order_map_finding("s05", "A flexible zone",
    "Panthenol appears inside the story's flexible-order teaching zone.",
    "Position below the line still does not reveal the dose.")
body = f'''
    <div class="om-stage">
      <div class="om-wrap om-push" id="s05-push">
        <div class="om-receipt" id="s05-receipt">
          <div class="om-receipt-title"><span>Ingredient declaration</span><span>Exact percentages undisclosed</span></div>
          <div class="om-rows" id="s05-rows">{s05_rows}</div>
          <div class="om-flexzone" id="s05-flexzone" style="height:168px;"></div>
        </div>
        <div class="om-analysis">
          {s05_finding}
          <div class="uf-badge" id="s05-flag" style="width:max-content;">&#9675; UNSOURCED — no record in this system</div>
        </div>
      </div>
      <div class="msg" id="s05-msg"><div class="body">Unless a brand publishes the percentage — don't invent a number.</div></div>
      <div class="tag2" id="s05-tag2"><div class="sub">RANK, NOT QUANTITY</div></div>
      <div class="seal-lock" id="s05-seal-lock">{question_seal("s05-q1-seal", 0, "active", size=110, bg="paper")}</div>
    </div>
'''
script = """
  gsap.set('.om-row', { opacity: 1 });
  gsap.set('#s05-push', { scale: 1.16, x: 60 });
  gsap.set('.om-finding', { opacity: 0, y: 16 });
  gsap.set('.om-verdict', { opacity: 0 });
  gsap.set('#s05-flag', { opacity: 0 });
  gsap.set('#s05-msg', { opacity: 0, y: 14 });
  gsap.set('#s05-tag2', { opacity: 0, y: 16 });
  gsap.set('#s05-seal-lock', { opacity: 0, scale: 0.5 });

  var tl = gsap.timeline({ paused: true });
  // camera pushes into the selected row -- whole-stage move, matching the
  // camera-dive convention already used at s04/s06/s11.
  tl.to('#s05-push', { scale: 1.0, x: 0, duration: 1.4, ease: 'power2.out' }, 0.0);
  tl.to('.om-finding', { opacity: 1, y: 0, duration: 0.6, ease: 'power3.out', stagger: 0.15 }, 1.6);
  tl.to('.om-verdict', { opacity: 1, duration: 0.6, ease: 'power2.out' }, 2.4);
  // [K-2] flag fires CONCURRENTLY with the claim it discloses, per C6 in
  // 01-story-brief.md -- not before, not after.
  tl.to('#s05-flag', { opacity: 1, duration: 0.4, ease: 'power2.out' }, 2.6);
  tl.to('#s05-flag', { opacity: 0, duration: 0.4, ease: 'power2.in' }, 10.5);
  tl.to('#s05-msg', { opacity: 1, y: 0, duration: 1.0, ease: 'power3.out' }, 11.0);
  tl.to('#s05-msg', { opacity: 0, duration: 0.5, ease: 'power2.in' }, 15.0);
  tl.to('#s05-tag2', { opacity: 1, y: 0, duration: 0.9, ease: 'power3.out' }, 15.5);
  // snap back to the bottles' own question rail -- Question 1 seal turns
  // face-up (active -> answered) in the beat sheet's own final 1s window.
  tl.to('#s05-seal-lock', { opacity: 1, scale: 1, duration: 0.35, ease: 'back.out(2)' }, 17.76);
  tl.to('#s05-q1-seal-ring', { attr: { stroke: '#426B50' }, duration: 0.35, ease: 'power2.out' }, 17.9);
  tl.to('#s05-q1-seal-keyline', { attr: { stroke: '#426B50' }, duration: 0.35, ease: 'power2.out' }, 17.9);
  tl.to('#s05-q1-seal .icon', { color: '#426B50', duration: 0.35, ease: 'power2.out' }, 17.9);
  tl.to({}, { duration: 18.762, ease: 'none' }, 0);
  window.__timelines = window.__timelines || {};
  window.__timelines['s05-q1-dose'] = tl;
"""
write("s05-q1-dose", style, body, script, bg="paper")

# ---------------------------------------------------------------- s06 -----
# Catalog source: source-process-version-map, single_path variant. Opens on
# the same ingredient actor from s01/s03, which becomes the Source station
# itself -- not a redrawn icon -- then Process and Version stations reveal
# what the familiar name does and does not disclose.
style = """
  .spv-stage { position:relative; height:100%; width:100%; display:flex; flex-direction:column; justify-content:center; }
  .spv-open { position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); opacity:1; }
  .spv-map { display:flex; align-items:stretch; gap:0; opacity:0; }
  .not-equal { text-align:center; margin-top:28px; opacity:0; color:var(--ink-soft); font-size:26px; }
  .not-equal b { color:var(--signal); margin-right:10px; }
"""
station_source = spv_station("s06-source", "SOURCE", "ingredient-source",
    "Centella asiatica", "The botanical source can be named without proving the extract specification.",
    "known", actor=True)
station_process = spv_station("s06-process", "PROCESS", "formula-vehicle",
    "Extraction process", "Solvent, ratio and standardization are not disclosed by the familiar name.",
    "not_disclosed")
station_version = spv_station("s06-version", "VERSION IN FORMULA", "identity-version",
    "Centella Asiatica Extract", "The exact declaration identifies the ingredient, not every process variable.",
    "requires_context",
    variables=[("botanical", "known"), ("solvent", "unknown"), ("standardization", "unknown")])
body = f'''
    <div class="spv-stage" id="s06-camera" style="transform-origin:50% 45%;">
      <div class="spv-open" id="s06-open">{ingredient_actor_svg("s06-open-actor", size=280)}</div>
      <div class="spv-map" id="s06-map" style="width:1560px; margin:0 auto;">
        {station_source}
        {spv_connector("s06-conn-1")}
        {station_process}
        {spv_connector("s06-conn-2")}
        {station_version}
      </div>
      <div class="not-equal" id="s06-noteq"><b>&ne;</b>Same familiar name does not guarantee the same preparation.</div>
      <div style="text-align:center;margin-top:18px;opacity:0;" id="s06-cite-wrap">{citation_chip("s06-cite", "J Cosmet Sci &middot; 2020")}</div>
    </div>
'''
# Idle ambient: each station keeps a very slow scale breathe once landed, so
# the long stretch between the process/version reveals and the final slam
# never sits fully static.
_station_idle = []
_IDLE_SEG, _IDLE_GAP = 2.6, 0.02
# #s06-version deliberately excluded: it gets its own dedicated emphasis
# pulse at 16.0-16.9 for the "collapse into one name" beat, and an idle
# tween landing in that window would overlap the same property (scale).
for _i, (_sel, _t0, _t_end) in enumerate([("#s06-source", 4.4, 20.0), ("#s06-process", 8.4, 15.8)]):
    for _j, _scale in enumerate((1.012, 1.0, 1.01, 1.0)):
        _t = _t0 + _j * (_IDLE_SEG + _IDLE_GAP)
        if _t < _t_end:
            _station_idle.append(f"  tl.to('{_sel}', {{ scale: {_scale}, duration: {_IDLE_SEG}, ease: 'sine.inOut' }}, {_t:.2f});")
station_idle_tweens = "\n".join(_station_idle)
script = f"""
  gsap.set('#s06-open', {{ opacity: 1, scale: 1 }});
  gsap.set('#s06-map', {{ opacity: 0, y: 20 }});
  gsap.set('.spv-station', {{ transformOrigin: '50% 50%' }});
  gsap.set('#s06-process', {{ opacity: 0.15 }});
  gsap.set('#s06-version', {{ opacity: 0.15 }});
  gsap.set('#s06-noteq', {{ opacity: 0 }});
  gsap.set('#s06-cite-wrap', {{ opacity: 0 }});
  gsap.set('#s06-camera', {{ scale: 1.08, y: -24 }});

  var tl = gsap.timeline({{ paused: true }});
  tl.to('#s06-camera', {{ scale: 1.0, y: 0, duration: 1.1, ease: 'power2.out' }}, 0.0);
  // leaf actor opens the scene, veins glowing, before the map assembles.
  tl.fromTo('#s06-open-actor', {{ scale: 0.85 }}, {{ scale: 1.05, duration: 1.6, ease: 'sine.inOut' }}, 0.0);
  tl.to('#s06-open', {{ scale: 0.4, x: -640, y: -70, duration: 1.0, ease: 'power2.inOut' }}, 3.2);
  tl.to('#s06-open', {{ opacity: 0, duration: 0.3 }}, 4.0);
  // the leaf settles as the Source station's own icon -- same element idiom, not a rebuild.
  tl.to('#s06-map', {{ opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' }}, 4.0);
  tl.to('#s06-process', {{ opacity: 1, duration: 0.7, ease: 'power2.out' }}, 6.2);
  tl.to('#s06-version', {{ opacity: 1, duration: 0.7, ease: 'power2.out' }}, 11.0);
{station_idle_tweens}
  tl.to('#s06-noteq', {{ opacity: 1, duration: 0.6, ease: 'power2.out' }}, 16.4);
  tl.fromTo('#s06-version', {{ scale: 1 }}, {{ scale: 1.03, duration: 0.4, ease: 'power2.out' }}, 16.0);
  tl.to('#s06-version', {{ scale: 1.0, duration: 0.5, ease: 'power2.inOut' }}, 16.4);
  tl.to('#s06-cite-wrap', {{ opacity: 1, duration: 0.5, ease: 'power2.out' }}, 17.6);
  tl.to({{}}, {{ duration: 20.554, ease: 'none' }}, 0);
  window.__timelines = window.__timelines || {{}};
  window.__timelines['s06-q2-leaf-chambers'] = tl;
"""
write("s06-q2-leaf-chambers", style, body, script, bg="paper")

# ---------------------------------------------------------------- s07 -----
# Reuses s06's Source/Process/Version component in version_compare state:
# one actor branches into three distinct preparation signatures under one
# common identity gate. Complete Question 2 (identity-version seal locks).
style = """
  .gate-stage { position:relative; height:100%; width:100%; display:flex; flex-direction:column; align-items:center; justify-content:center; }
  .gate-actor { opacity:0; margin-bottom:18px; }
  .gate-lines { position:relative; width:900px; height:70px; }
  .gate-line { position:absolute; top:0; left:50%; width:2px; height:100%; background:var(--line);
    transform-origin:top center; transform:scaleY(0); }
  .gate-row { display:flex; gap:44px; }
  .gate-card { width:270px; padding:22px 24px; border:1px solid var(--line); border-radius:16px;
    background:rgba(255,255,255,0.6); text-align:left; opacity:0; }
  .gate-card .name { font-weight:800; font-size:24px; letter-spacing:-.02em; margin-bottom:8px; }
  .gate-card .note { color:var(--ink-soft); font-size:18px; line-height:1.35; }
  .tag3 { text-align:center; margin-top:36px; opacity:0; }
  .tag3 .sub { font-size:50px; color:var(--signal); }
  .seal-lock { position:absolute; right:calc(var(--safe-right) + 40px); bottom:calc(var(--safe-bottom) + 20px);
    opacity:0; transform:scale(0.5); }
"""
variants = [
    ("Water extract", "Mild, water-soluble fraction"),
    ("Solvent extract", "Different compound profile"),
    ("Standardized compound", "Purified, quantified active"),
]
gate_cards = "".join(
    f'<div class="gate-card" id="s07-card-{i}"><div class="name">{name}</div><div class="note">{note}</div></div>'
    for i, (name, note) in enumerate(variants)
)
gate_lines = "".join(
    f'<div class="gate-line" id="s07-line-{i}" style="left:{p}%;"></div>' for i, p in enumerate([18, 50, 82])
)
body = f'''
    <div class="gate-stage">
      <div class="gate-actor" id="s07-actor">{ingredient_actor_svg("s07-actor-svg", size=140)}</div>
      <div class="gate-lines">{gate_lines}</div>
      <div class="gate-row">{gate_cards}</div>
      <div class="tag3" id="s07-tag"><div class="sub">ONE NAME. MANY EXTRACTS.</div></div>
      <div class="seal-lock" id="s07-seal-lock">{question_seal("s07-q2-seal", 1, "active", size=100, bg="paper")}</div>
    </div>
'''
line_tweens = "\n".join(
    f"  tl.to('#s07-line-{i}', {{ scaleY: 1, duration: 0.4, ease: 'power2.out' }}, {1.4 + i*0.15:.2f});"
    for i in range(3)
)
card_tweens = "\n".join(
    f"  tl.to('#s07-card-{i}', {{ opacity: 1, y: 0, duration: 0.5, ease: 'power3.out' }}, {1.9 + i*0.2:.2f});"
    for i in range(3)
)
script = f"""
  gsap.set('#s07-actor', {{ opacity: 0, y: -10 }});
  gsap.set('.gate-card', {{ opacity: 0, y: 14 }});
  gsap.set('#s07-tag', {{ opacity: 0, y: 16 }});
  gsap.set('#s07-seal-lock', {{ opacity: 0, scale: 0.5 }});

  var tl = gsap.timeline({{ paused: true }});
  tl.to('#s07-actor', {{ opacity: 1, y: 0, duration: 0.6, ease: 'power2.out' }}, 0.0);
{line_tweens}
{card_tweens}
  tl.to('#s07-tag', {{ opacity: 1, y: 0, duration: 0.7, ease: 'power3.out' }}, 3.2);
  // snap, Question 2 seal turns face-up.
  tl.to('#s07-seal-lock', {{ opacity: 1, scale: 1, duration: 0.3, ease: 'back.out(2)' }}, 6.0);
  tl.to('#s07-q2-seal-ring', {{ attr: {{ stroke: '#426B50' }}, duration: 0.3, ease: 'power2.out' }}, 6.1);
  tl.to('#s07-q2-seal-keyline', {{ attr: {{ stroke: '#426B50' }}, duration: 0.3, ease: 'power2.out' }}, 6.1);
  tl.to('#s07-q2-seal .icon', {{ color: '#426B50', duration: 0.3, ease: 'power2.out' }}, 6.1);
  tl.to({{}}, {{ duration: 8.012, ease: 'none' }}, 0);
  window.__timelines = window.__timelines || {{}};
  window.__timelines['s07-q2-travelers'] = tl;
"""
write("s07-q2-travelers", style, body, script, bg="paper")
