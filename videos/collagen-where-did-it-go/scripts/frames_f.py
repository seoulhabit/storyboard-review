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
              padding:10px 16px; display:flex; align-items:center; gap:14px; position:relative; }
    .w-card svg { width:56px; height:56px; flex:0 0 auto; }
    .pk-body { fill:var(--paper); stroke:var(--ink); stroke-width:5; }
    .pk-cap  { fill:var(--ink); }
    .w-t { font-family:var(--font-body); font-weight:800; font-size:var(--t-chip); color:var(--ink); margin:0; }
    .brick { fill:var(--coral); stroke:var(--paper); stroke-width:3; }
    #final { padding:var(--s-4) var(--s-6); display:flex; align-items:center; opacity:0; }
    #final-kt { font-size:var(--t-hero); }
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
               abs_(1440, 120, 288, 330))}
        <svg id="bricks" class="abs" viewBox="0 0 300 220" width="300" height="220" style="{abs_(1440, 560)}" aria-hidden="true">
          <rect class="brick" x="0" y="150" width="140" height="60" rx="6"/><rect class="brick" x="150" y="150" width="140" height="60" rx="6"/>
          <rect class="brick" x="75" y="80" width="140" height="60" rx="6"/><rect class="brick" x="225" y="80" width="70" height="60" rx="6"/>
          <rect class="brick" x="0" y="80" width="65" height="60" rx="6"/><rect class="brick" x="150" y="10" width="140" height="60" rx="6"/>
        </svg>
        {cite("cite-smoke", "J Dermatol Sci &middot; 2007", False, abs_(620, 735))}
        {cite("cite-ret", "Arch Dermatol &middot; 2007", False, abs_(1120, 735))}
        {panel("final", "moss", kt("final-kt", "Protect the building first."), abs_(0, 796, 1728, 122))}
       </div>
      </div>
"""
    tl = EASE_JS + HELPERS_JS + BUILDING_JS + """
    var svg = document.getElementById("bldg");
    drawBuilding(svg, { door:true, into:document.getElementById("bwrap") });
    // the building comes back DAMAGED: same beams 04 cut, restated at 0 for cold seeks
    setBeamsCut(tl, CUT_ORDER);
    document.getElementById("bwrap").setAttribute("transform", "translate(40 40) scale(0.9) skewX(-1.4)");
    gsap.set("#bwrap", { skewX:-1.4, y:9 });
    // camera settles in from the invert
    tl.fromTo("#world", { scale:1.06 }, { scale:1, duration:1.2, ease:EASE.camera }, 0);
    // rows are authored in their final slots; frame zero shows them UNSORTED
    ["#rank-1", "#rank-2", "#rank-3", "#rank-4"].forEach(function (id, i) {
      tl.fromTo(id, { y:SHUFFLE[i] }, { y:0, duration:0.7, ease:EASE.swap }, @w(supports) - 0.2 + i * 0.08);
    });
    // each action locks in as it is named; sunscreen locks into the FOUNDATION
    tl.fromTo("#rank-1-wash", { scaleX:0 }, { scaleX:1, duration:0.4, ease:EASE.wipe }, @w(sunscreen));
    // sunscreen LOCKS ACROSS the foundation, left to right, as it is named
    tl.fromTo("#slab-lock", { opacity:1, scaleX:0, transformOrigin:"0% 50%" },
              { scaleX:1, duration:0.38, ease:EASE.slam }, @w(sunscreen) + 0.10);
    tl.to("#shield", { opacity:0.30, duration:0.6, ease:EASE.swap }, @w(sunscreen) + 0.10);
    tl.fromTo("#rank-2-wash", { scaleX:0 }, { scaleX:1, duration:0.4, ease:EASE.wipe }, @w(smoking));
    tl.fromTo("#cite-smoke", { opacity:0, y:16 }, { opacity:1, y:0, duration:0.35, ease:EASE.arrive }, @w(smoking) + 0.3);
    tl.fromTo("#rank-3-wash", { scaleX:0 }, { scaleX:1, duration:0.4, ease:EASE.wipe }, @w(protein));
    // PROTEIN is the building material, so the partial repair rides that line:
    // three of six beams come back and the lean comes out. The damage is not undone.
    ["4a", "3a", "1a"].forEach(function (k, i) {
      tl.to("#beam-" + k, { strokeDashoffset:0, opacity:1, duration:0.55, ease:EASE.wipe }, @w(protein) + 0.25 + i * 0.3);
    });
    tl.to("#bwrap", { skewX:0, y:0, duration:1.1, ease:EASE.swap }, @w(vitamin));
    // the smoking chip steps back so it is not read as sourcing the nutrition line
    tl.to("#cite-smoke", { opacity:0.35, duration:0.35, ease:EASE.exit }, @w(protein) + 0.2);
    tl.fromTo("#rank-4-wash", { scaleX:0 }, { scaleX:1, duration:0.4, ease:EASE.wipe }, @w(retinoids));
    tl.fromTo("#cite-ret", { opacity:0, y:16 }, { opacity:1, y:0, duration:0.35, ease:EASE.arrive }, @w(retinoids) + 0.4);
    // "considerably stronger evidence for encouraging collagen production": ONE
    // more beam draws in, and the camera leans toward the building to watch it.
    // One beam, not six -- the claim is stronger evidence for production, not a
    // rebuilt structure. The push now starts on "stronger" rather than waiting
    // for "encouraging" -- between the retinoid citation settling (~118.7s) and
    // the old @w(encouraging)-0.3 anchor (121.0s) sat ~2.3s of nothing, measured
    // on the render as a pixel-identical t=120-122s freeze, during the section's
    // longest sentence. The camera lean now fills that gap directly; the beam
    // repair keeps its own anchor on "encouraging", the word it depicts.
    tl.to("#world", { scale:1.05, x:120, duration:0.8, ease:EASE.camera }, @w(stronger) - 0.1);
    tl.to("#beam-2b", { strokeDashoffset:0, opacity:1, duration:0.7, ease:EASE.wipe }, @w(encouraging));
    // the whole brace set brightens as production is named, so the claim reads as
    // the building gaining rather than one line quietly redrawing itself
    tl.to(".beam", { opacity:1, duration:1.0, ease:EASE.arrive }, @w(production) - 0.2);
    tl.fromTo("#shield", { opacity:0.30 }, { opacity:0.44, duration:0.9, yoyo:true, repeat:1,
              ease:EASE.hold }, @w(production) + 0.1);

    // ---- unit 15: cream and powder are OPTIONAL, kept apart from the first line
    // the optional column ARRIVES: the camera pans right so cream and powder
    // enter the frame from outside the first-line actions, never sharing their row
    tl.to("#world", { scale:1.06, x:-240, duration:0.9, ease:EASE.camera }, @w(cream,2) - 0.5);
    tl.fromTo("#opt-wash", { scaleX:0 }, { scaleX:1, duration:0.4, ease:EASE.wipe }, @w(cream,2) - 0.2);
    tl.to("#w1", { scale:1.05, duration:0.25, yoyo:true, repeat:1, ease:EASE.slam }, @w(cream,2));
    tl.to("#w2", { scale:1.05, duration:0.25, yoyo:true, repeat:1, ease:EASE.slam }, @w(powder));
    // the two optional cards settle back and dim as the verdict is spoken over
    // them -- 1.9s of still frame sat across "can be a pleasant moisturiser"
    tl.to("#w1", { y:10, opacity:0.62, duration:1.2, ease:EASE.hold }, @w(pleasant) - 0.2);
    tl.to("#w2", { y:10, opacity:0.62, duration:1.2, ease:EASE.hold }, @w(powder) + 0.15);
    tl.fromTo("#opt-chip", { opacity:0, scale:0.8 }, { opacity:1, scale:1, duration:0.3, ease:EASE.slam }, @w(optional));
    tl.to("#world", { scale:1, x:0, duration:0.8, ease:EASE.camera }, @w(protect) - 0.9);
    tl.to("#final", { opacity:1, duration:0.1 }, @w(protect) - 0.1);
    tl.fromTo("#final-wash", { scaleX:0 }, { scaleX:1, duration:0.6, ease:EASE.wipe }, @w(protect) - 0.1);
    kineticWords(tl, "#final-kt", @w(protect) + 0.15, 0.08, "rise");
    // the bricks are already leaving as they are named; the building they were
    // never going to build takes the frame back over the closing words
    tl.to("#bldg", { scale:1.05, transformOrigin:"20% 60%", duration:1.4, ease:EASE.camera }, @w(building) - 0.2);
    tl.to("#bricks", { x:180, duration:0.9, ease:EASE.hold }, @w(before));
    tl.to("#bricks", { x:520, opacity:0.3, duration:0.7, ease:EASE.exit }, @w(bricks));
""".replace("SHUFFLE", str(SHUFFLE))
    MOTION["14-hierarchy"]["beats"] = [
        {"name": "camera settle",  "at": "0.0",               "area": 0.5,   "dl": 60,  "dur": 1.2},
        {"name": "rows sort in",   "at": "@w(supports)-0.2",  "area": 0.22,  "dl": 70,  "dur": 0.7},
        {"name": "row 1 wash",     "at": "@w(sunscreen)",     "area": 0.047, "dl": 91,  "dur": 0.4},
        {"name": "foundation lock", "at": "@w(sunscreen)+0.1", "area": 0.05, "dl": 120, "dur": 0.38},
        {"name": "row 2 wash",     "at": "@w(smoking)",       "area": 0.047, "dl": 91,  "dur": 0.4},
        {"name": "row 3 wash",     "at": "@w(protein)",       "area": 0.047, "dl": 91,  "dur": 0.4},
        {"name": "building straightens", "at": "@w(vitamin)", "area": 0.17,  "dl": 60,  "dur": 1.1},
        {"name": "row 4 wash",     "at": "@w(retinoids)",     "area": 0.047, "dl": 91,  "dur": 0.4},
        {"name": "retinoid beam",  "at": "@w(stronger)-0.1", "area": 0.5,  "dl": 60,  "dur": 0.8},
        {"name": "braces brighten", "at": "@w(production)-0.2",  "area": 0.17, "dl": 55,  "dur": 1.0},
    ]
    MOTION["15-verdict"]["beats"] = [
        {"name": "camera pans right", "at": "@w(cream,2)-0.5", "area": 0.5,   "dl": 60,  "dur": 0.9},
        {"name": "optional dim",      "at": "@w(cream,2)-0.2", "area": 0.05,  "dl": 94,  "dur": 0.4},
        {"name": "camera home",       "at": "@w(protect)-0.9", "area": 0.5,   "dl": 60,  "dur": 0.8},
        {"name": "final moss band",   "at": "@w(protect)-0.1", "area": 0.108, "dl": 149, "dur": 0.6},
        {"name": "cards settle",      "at": "@w(pleasant)-0.2", "area": 0.05,  "dl": 70,  "dur": 1.2},
        {"name": "building retakes",  "at": "@w(building)-0.2", "area": 0.20, "dl": 55,  "dur": 1.4},
        {"name": "bricks drift",      "at": "@w(before)",      "area": 0.064, "dl": 70,  "dur": 0.9},
        {"name": "bricks exit",       "at": "@w(bricks)",      "area": 0.064, "dl": 103, "dur": 0.7},
    ]
    return body, css, tl


FILES = {"14-hierarchy": file_14_hierarchy}
