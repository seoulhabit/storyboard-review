#!/usr/bin/env python3
"""File F -- 14-hierarchy (unit 14) + 15-verdict (unit 15). Paper ground.
THE BUILDING RETURNS -- same builder, damaged state carried (beams cut, skew,
the shield's held tint), so the ending comes back to a place, not a lookalike.
"""
from actors import HELPERS_JS, BUILDING_JS, BUILDING_CSS, EASE_JS, kt, chip, cite, panel, abs_
from motion import MOTION

ROWS = [("rank-1", "1 · daily sunscreen"), ("rank-2", "2 · not smoking"),
        ("rank-3", "3 · protein + vitamin C"), ("rank-4", "4 · retinoids, if suitable")]
SHUFFLE = [300, -150, 150, -300]     # fixed, never Math.random


def file_14_hierarchy(fspan, fctx):
    css = BUILDING_CSS + """
    .abs { position:absolute; }
    #bldg { position:absolute; left:0; top:0; }
    .shield { fill:var(--aqua); opacity:.12; }
    .slab-lock { fill:var(--aqua); opacity:0; }
    .rank-row { padding:var(--s-4) var(--s-5); display:flex; align-items:center; }
    .rank-row .p-title { margin:0; }
    #opt { background:var(--mist); padding:var(--s-4); display:flex; flex-direction:column; gap:12px; }
    .w-card { border-radius:var(--r-3); background:var(--paper); border:3px solid var(--rule-strong);
              padding:10px 14px; display:flex; align-items:center; gap:14px; position:relative; }
    .w-card svg { width:70px; height:70px; flex:0 0 auto; }
    .pk-body { fill:var(--paper); stroke:var(--ink); stroke-width:5; }
    .pk-cap  { fill:var(--ink); }
    .w-t { font-family:var(--font-body); font-weight:800; font-size:var(--t-chip); color:var(--ink); margin:0; }
    .brick { fill:var(--coral); stroke:var(--paper); stroke-width:3; }
    #final { padding:var(--s-4) var(--s-5); display:flex; align-items:center; opacity:0; }
    .cite { opacity:0; position:absolute; }
"""
    rows = "".join(panel(rid, "aqua", f'<p class="p-title">{label}</p>',
                         abs_(740, 120 + i * 160, 700, 130), "rank-row")
                   for i, (rid, label) in enumerate(ROWS))
    body = f"""
      <div class="stage">
       <div class="world" id="world">
        <svg id="bldg" viewBox="0 0 700 918" width="700" height="918" aria-hidden="true">
          <g id="bwrap" transform="translate(40 40) scale(0.9)"></g>
          <rect class="shield" id="shield" x="90" y="150" width="520" height="560" rx="18"/>
          <rect class="slab-lock" id="slab-lock" x="80" y="686" width="490" height="34" rx="6"/>
        </svg>
        {rows}
        {panel("opt", "dim", chip("opt-chip", "optional", "", "opacity:0;") +
               '''<div class="w-card" id="w1"><svg viewBox="0 0 200 200"><rect class="pk-body" x="46" y="74" width="108" height="96" rx="8"/><rect class="pk-cap" x="60" y="46" width="80" height="30" rx="5"/></svg><p class="w-t">collagen cream</p></div>
               <div class="w-card" id="w2"><svg viewBox="0 0 200 200"><path class="pk-body" d="M58 46 L142 46 L152 172 L48 172 Z"/><rect class="pk-cap" x="58" y="36" width="84" height="16" rx="4"/></svg><p class="w-t">collagen powder</p></div>''',
               abs_(1460, 120, 268, 330))}
        <svg id="bricks" class="abs" viewBox="0 0 300 220" width="300" height="220" style="{abs_(1440, 560)}" aria-hidden="true">
          <rect class="brick" x="0" y="150" width="140" height="60" rx="6"/><rect class="brick" x="150" y="150" width="140" height="60" rx="6"/>
          <rect class="brick" x="75" y="80" width="140" height="60" rx="6"/><rect class="brick" x="225" y="80" width="70" height="60" rx="6"/>
          <rect class="brick" x="0" y="80" width="65" height="60" rx="6"/><rect class="brick" x="150" y="10" width="140" height="60" rx="6"/>
        </svg>
        {cite("cite-smoke", "J Dermatol Sci &middot; 2007", False, abs_(740, 800))}
        {cite("cite-ret", "Arch Dermatol &middot; 2007", False, abs_(1200, 800))}
        {panel("final", "moss", '<p class="p-title">Protect the building first.</p>', abs_(0, 760, 700, 130))}
       </div>
      </div>
"""
    tl = EASE_JS + HELPERS_JS + BUILDING_JS + """
    var svg = document.getElementById("bldg");
    drawBuilding(svg, { door:true, into:document.getElementById("bwrap") });
    // the building comes back DAMAGED: same beams 04 cut, restated at 0 for cold seeks
    setBeamsCut(tl, CUT_ORDER);
    document.getElementById("bwrap").setAttribute("transform", "translate(40 40) scale(0.9) skewX(-1.4)");
    tl.set("#bwrap", { skewX:-1.4, y:9 }, 0);
    // camera settles in from the invert
    tl.fromTo("#world", { scale:1.06 }, { scale:1, duration:1.2, ease:EASE.camera }, 0);
    // rows are authored in their final slots; frame zero shows them UNSORTED
    ["#rank-1", "#rank-2", "#rank-3", "#rank-4"].forEach(function (id, i) {
      tl.fromTo(id, { y:SHUFFLE[i] }, { y:0, duration:0.7, ease:EASE.swap }, @w(supports) - 0.2 + i * 0.08);
    });
    // each action locks in as it is named; sunscreen locks into the FOUNDATION
    tl.fromTo("#rank-1-wash", { scaleX:0 }, { scaleX:1, duration:0.4, ease:EASE.wipe }, @w(sunscreen));
    tl.to("#slab-lock", { opacity:1, duration:0.3, ease:EASE.slam }, @w(sunscreen) + 0.10);
    tl.to("#shield", { opacity:0.30, duration:0.6, ease:EASE.swap }, @w(sunscreen) + 0.10);
    tl.fromTo("#rank-2-wash", { scaleX:0 }, { scaleX:1, duration:0.4, ease:EASE.wipe }, @w(smoking));
    tl.to("#cite-smoke", { opacity:1, duration:0.3, ease:EASE.arrive }, @w(smoking) + 0.3);
    // the repair: SOME beams come back and the building straightens -- protecting
    // beats replacing; the damage is not undone
    ["4a", "3a", "1a"].forEach(function (k, i) {
      tl.to("#beam-" + k, { strokeDashoffset:0, opacity:1, duration:0.55, ease:EASE.wipe }, @w(smoking) + 0.4 + i * 0.3);
    });
    tl.to("#bwrap", { skewX:0, y:0, duration:1.1, ease:EASE.swap }, @w(smoking) + 0.6);
    tl.fromTo("#rank-3-wash", { scaleX:0 }, { scaleX:1, duration:0.4, ease:EASE.wipe }, @w(protein));
    tl.fromTo("#rank-4-wash", { scaleX:0 }, { scaleX:1, duration:0.4, ease:EASE.wipe }, @w(retinoids));
    tl.to("#cite-ret", { opacity:1, duration:0.3, ease:EASE.arrive }, @w(retinoids) + 0.4);

    // ---- unit 15: cream and powder are OPTIONAL, kept apart from the first line
    tl.fromTo("#opt-wash", { scaleX:0 }, { scaleX:1, duration:0.4, ease:EASE.wipe }, @w(cream,2) - 0.2);
    tl.to("#w1", { scale:1.05, duration:0.25, yoyo:true, repeat:1, ease:EASE.slam }, @w(cream,2));
    tl.to("#w2", { scale:1.05, duration:0.25, yoyo:true, repeat:1, ease:EASE.slam }, @w(powder));
    tl.fromTo("#opt-chip", { opacity:0, scale:0.8 }, { opacity:1, scale:1, duration:0.3, ease:EASE.slam }, @w(optional));
    tl.to("#final", { opacity:1, duration:0.1 }, @w(protect) - 0.1);
    tl.fromTo("#final-wash", { scaleX:0 }, { scaleX:1, duration:0.6, ease:EASE.wipe }, @w(protect) - 0.1);
    tl.to("#bricks", { x:420, duration:0.6, ease:EASE.exit }, @w(bricks));
""".replace("SHUFFLE", str(SHUFFLE))
    MOTION["14-hierarchy"]["beats"] = [
        {"name": "camera settle", "at": "0.0", "area": 0.5, "dl": 60, "dur": 1.2},
        {"name": "row 1 wash", "at": "@w(sunscreen)", "area": 0.047, "dl": 91, "dur": 0.4},
        {"name": "row 2 wash", "at": "@w(smoking)", "area": 0.047, "dl": 91, "dur": 0.4},
        {"name": "row 3 wash", "at": "@w(protein)", "area": 0.047, "dl": 91, "dur": 0.4},
        {"name": "row 4 wash", "at": "@w(retinoids)", "area": 0.047, "dl": 91, "dur": 0.4},
    ]
    MOTION["15-verdict"]["beats"] = [
        {"name": "optional dim", "at": "@w(cream,2)-0.2", "area": 0.05, "dl": 94, "dur": 0.4},
        {"name": "final moss", "at": "@w(protect)-0.1", "area": 0.044, "dl": 149, "dur": 0.6},
        {"name": "bricks exit", "at": "@w(bricks)", "area": 0.064, "dl": 103, "dur": 0.6},
    ]
    return body, css, tl


FILES = {"14-hierarchy": file_14_hierarchy}
