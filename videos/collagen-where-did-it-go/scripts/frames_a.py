#!/usr/bin/env python3
"""File A1 -- 01-hook (unit 1) and File A2 -- 02-promise (unit 2).

Frame ZERO is the hook: the molecule is already racing at the barrier and
the first word lands at 0.10s. Nothing fades in from black.
"""
from actors import (HELPERS_JS, HELIX_JS, HELIX_CSS, BARRIER_JS, BARRIER_CSS, TILES_JS,
                    EASE_JS, kt, chip, panel, abs_)
from motion import MOTION

# local safe-box coordinates (1728 x 918)
MOL_PARK = (864, 506)          # where the molecule rests between files A1 and A2 (canvas 960,560)


def file_01_hook(fspan, fctx):
    css = HELIX_CSS + BARRIER_CSS + """
    .abs { position:absolute; left:0; top:0; }
    #hook-slam { position:absolute; left:120px; top:120px; width:820px; }
    #hook-slam .kt-word.em { color:var(--coral); }
    .lab { opacity:0; }
    #powder { position:absolute; left:60px; top:560px; width:820px; height:320px;
              background:var(--mist); padding:var(--s-4) var(--s-5); }
    #powder .chip { position:relative; }
    .glass { fill:none; stroke:var(--ink); stroke-width:5; }
    .glass-fill { fill:var(--aqua); opacity:.35; }
    .arrow { fill:none; stroke:var(--ink); stroke-width:5; stroke-dasharray:18 14; opacity:.8; }
    .strike { fill:var(--coral); opacity:0; }
    .hidden-path { fill:none; stroke:none; }
    #epi-wash { position:absolute; left:1067px; top:0; width:177px; height:918px; background:var(--coral); }
"""
    body = f"""
      <div class="stage">
       <div class="world" id="world">
        {panel("powder", "aqua", chip("lab-powder", "POWDER", "lab", "position:absolute;left:32px;top:24px;"), abs_(60, 560, 820, 320), "")}
        <svg id="stageA" class="abs" viewBox="0 0 1728 918" width="1728" height="918" aria-hidden="true">
          <path id="run" class="hidden-path" d="M 320 470 L 790 470"/>
          <path id="drop" class="hidden-path" d="M 470 230 C 470 400 470 520 470 690"/>
          <path class="glass" d="M 400 640 L 540 640 L 522 830 L 418 830 Z"/>
          <rect class="glass-fill" x="412" y="760" width="116" height="66"/>
          <path id="arrow-face" class="arrow" d="M 570 735 L 1000 735"/>
          <rect id="arrow-x" class="strike" x="560" y="722" width="450" height="26" rx="6"/>
        </svg>
        <div id="epi-wash"></div>
        {kt("hook-slam", "does NOT replace", "", em=("NOT",))}
        {chip("lab-cream", "CREAM", "lab", abs_(120, 330))}
       </div>
      </div>
"""
    tl = EASE_JS + HELPERS_JS + HELIX_JS + BARRIER_JS + """
    var svg = document.getElementById("stageA");
    gsap.set("#epi-wash", { scaleX:0, transformOrigin:"0% 50%" });
    // the barrier stands on the right, surface facing the molecule
    drawBarrier(svg, { id:"bar", w:918, h:691, surf:30, boundary:207, brickRows:2,
                       orient:"left", x:1037, hatch:{ n:6 } });
    var mol = drawHelix(svg, { id:"mol", x:40, y:470, w:560, h:140, strokeW:16 });
    var molb = drawHelix(svg, { id:"mol-b", x:330, y:230, w:280, h:70, strokeW:11 });
    molb.style.opacity = "0";
    var run = document.getElementById("run"), drop = document.getElementById("drop");

    // THE RACE: frame zero already has the molecule moving; it reaches the
    // surface exactly as "replace" is spoken.
    var tR = @w(replace);
    var end = pathFollow(tl, mol, run, 0.12, Math.max(0.6, tR - 0.30 - 0.12), "power2.in");
    // IMPACT: the epidermis flashes coral, the wall flexes, the molecule recoils
    tl.fromTo("#epi-wash", { scaleX:0 }, { scaleX:1, duration:0.18, yoyo:true, repeat:1, ease:EASE.slam }, tR - 0.05);
    tl.fromTo("#bar", { scaleX:1, transformOrigin:"100% 50%" },
              { scaleX:0.97, duration:0.16, yoyo:true, repeat:1, ease:EASE.slam }, tR - 0.05);
    tl.fromTo(mol, { x:end.x, y:end.y }, { x:end.x - 70, duration:0.45, ease:EASE.slam }, tR);
    kineticWords(tl, "#hook-slam", @w(not,1) - 0.05, 0.08, "slam");
    tl.fromTo("#lab-cream", { opacity:0, scale:0.8 }, { opacity:1, scale:1, duration:0.3, ease:EASE.slam }, @w(cream));

    // THE SPLIT: the powder route opens below
    tl.fromTo("#powder-wash", { scaleX:0 }, { scaleX:1, duration:0.5, ease:EASE.wipe }, @w(powder) - 0.10);
    tl.fromTo("#lab-powder", { opacity:0, scale:0.8 }, { opacity:1, scale:1, duration:0.3, ease:EASE.slam }, @w(powder));
    // the powder route is the SAME actor splitting off, not a new one fading in
    tl.fromTo(molb, { opacity:1, scale:0.2, transformOrigin:"50% 50%" },
              { scale:1, duration:0.32, ease:EASE.slam }, @w(powder));
    pathFollow(tl, molb, drop, @w(travel), 0.7, "power2.in");
    drawIn(tl, "#arrow-face", @w(travel) + 0.25, 0.5, 0, EASE.wipe);
    // "...to your face": the route is struck out, the panel retracts
    tl.fromTo("#arrow-x", { opacity:1, scaleX:0, transformOrigin:"0% 50%" },
              { scaleX:1, duration:0.25, ease:EASE.wipe }, @w(face));
    tl.to("#powder-wash", { scaleX:0, duration:0.4, ease:EASE.exit }, @w(face) + 0.30);
    tl.to(["#arrow-face", "#arrow-x", molb, "#lab-powder"], { opacity:0, duration:0.3, ease:EASE.exit }, @w(face) + 0.30);
    // converge: the molecule parks at the frame centre, where the iris opens
    tl.fromTo(mol, { x:end.x - 70, y:end.y }, { x:MOLX - 320, y:MOLY - 470, duration:0.55, ease:EASE.camera }, @we(face) - 0.20);
    tl.to("#hook-slam", { opacity:0, duration:0.3, ease:EASE.exit }, @we(face) - 0.20);
""".replace("MOLX", str(MOL_PARK[0])).replace("MOLY", str(MOL_PARK[1]))
    MOTION["01-hook"]["beats"] = [
        {"name": "impact flash",  "at": "@w(replace)-0.05", "area": 0.092, "dl": 103, "dur": 0.36},
        {"name": "powder wash",   "at": "@w(powder)-0.10",  "area": 0.127, "dl": 81,  "dur": 0.50},
        {"name": "powder retract","at": "@w(face)+0.30",    "area": 0.127, "dl": 81,  "dur": 0.40},
    ]
    return body, css, tl


FILES = {"01-hook": file_01_hook}


# ---------------------------------------------------------------- File A2 -- 02-promise

def file_02_promise(fspan, fctx):
    """The promise, and the curiosity loop the evidence act pays off.

    Two compositions on one set of nodes: the question drawn AROUND the
    parked molecule; an ink data column that rises and shoves it aside, tags
    the industry-funded trials and drops them WITHOUT showing a result (the
    loop stays open) -- then HOLDS there, unresolved, into the iris. There is
    no second curiosity loop here: the withdrawn draft's separate "what
    protects it?" shield teaser is gone (review Animation item 4, and the
    text that carried it -- "But first, what protects the collagen you
    already have?" -- was cut from vo_lines.py for the same reason: one open
    question, not two).

    The tile TAG PATTERN is illustrative: Myung & Park 2025 report 23 RCTs and
    subgroup results by funding source and quality, but no per-subgroup trial
    counts, so a chip says so on screen rather than letting 12 dropped tiles
    assert a number the source does not give.
    """
    css = HELIX_CSS + """
    .abs { position:absolute; }
    #stageB { position:absolute; left:0; top:0; }
    #promise-q { position:absolute; left:0; top:70px; width:940px; }
    .qmark { fill:none; stroke:var(--ink-3); stroke-width:16; stroke-linecap:round; }
    #data { background:transparent; padding:var(--s-5); display:flex; flex-direction:column;
            justify-content:center; gap:var(--s-4); }
    .mini-grid { display:grid; grid-template-columns:repeat(6, 1fr); gap:12px; height:392px; }
    .tr.mini { border-radius:var(--r-2); background:#4A453E; border:2px solid #6A6459;
               display:flex; align-items:center; justify-content:center; }
    .tr.mini .tr-tag { font-family:var(--font-mono); font-size:44px; font-weight:500;
                       color:var(--ink); opacity:0; }
    #data .chip { position:relative; }
"""
    body = f"""
      <div class="stage">
       <div class="world" id="world">
        <svg id="stageB" viewBox="0 0 1728 918" width="1728" height="918" aria-hidden="true">
          <path class="qmark" id="qmark" d="M 1206 372 C 1206 316 1250 288 1290 300 C 1332 313 1338 362 1308 392 C 1282 418 1268 436 1268 470"/>
          <circle class="qmark" id="qmark-dot" cx="1268" cy="524" r="3"/>
        </svg>
        {kt("promise-q", "Where does it actually go?", "serif")}
        {panel("data", "ink", '<div class="mini-grid" id="mini-grid"></div>'
               + chip("mini-cap", "23 trials", "on-ink")
               + chip("mini-leg", "$ = industry funded", "on-ink")
               + chip("mini-note", "tag pattern illustrative", "on-ink"),
               abs_(1000, 0, 728, 918), "late")}
       </div>
      </div>
"""
    tl = EASE_JS + HELPERS_JS + HELIX_JS + TILES_JS + """
    var svg = document.getElementById("stageB");
    // the SAME helix 01-hook parked here: identical geometry, so the iris hands
    // off one actor rather than two lookalikes
    var mol = drawHelix(svg, { id:"mol", x:584, y:506, w:560, h:140, strokeW:16 });
    drawTiles(document.getElementById("mini-grid"), 23, { size:"mini" });
    gsap.set(".tr.mini", { y:70, opacity:0 });
    gsap.set(["#mini-cap", "#mini-leg", "#mini-note"], { y:16, opacity:0 });
    gsap.set("#data-wash", { scaleX:1, scaleY:0, transformOrigin:"50% 100%" });
    kineticWords(tl, "#promise-q", @w(where) - 0.1, 0.09, "rise");
    // the question is DRAWN around the molecule, not typeset beside it
    drawIn(tl, "#qmark", @w(go) - 0.25, 0.55, 0, EASE.wipe);
    tl.fromTo("#qmark-dot", { attr:{ r:3 } }, { attr:{ r:9 }, duration:0.2, ease:EASE.slam }, @we(go));

    // ---- the data column rises and takes the frame -------------------------
    reveal(tl, "#data", @w(twenty) - 0.45);
    tl.to(["#qmark", "#qmark-dot"], { opacity:0, duration:0.25, ease:EASE.exit }, @w(twenty) - 0.55);
    tl.to("#data-wash", { scaleY:1, duration:0.5, ease:EASE.wipe }, @w(twenty) - 0.45);
    tl.to(mol, { x:-300, duration:0.6, ease:EASE.camera }, @w(twenty) - 0.35);
    tl.to("#promise-q", { y:-26, opacity:0.5, duration:0.5, ease:EASE.exit }, @w(twenty) - 0.35);
    tl.to(".tr.mini", { y:0, opacity:1, duration:0.3, stagger:0.02, ease:EASE.arrive }, @w(trials) - 0.1);
    tl.to("#mini-cap", { y:0, opacity:1, duration:0.3, ease:EASE.arrive }, @w(trials) + 0.3);
    // TAG, then DROP: the loop's object is named and removed, and no result is
    // shown -- 12-filter is where the answer lands
    tl.to(tiles(TAGS.industry), { backgroundColor:"#C97A5C", borderColor:"#C97A5C",
          duration:0.25, stagger:0.012, ease:EASE.swap }, @w(remove));
    TAGS.industry.forEach(function (i) { tl.set("#tag-" + i, { innerText:"$" }, @w(remove) + 0.1); });
    tl.fromTo(TAGS.industry.map(function (i) { return "#tag-" + i; }),
              { opacity:1, scale:0 }, { scale:1, duration:0.25, stagger:0.012, ease:EASE.slam }, @w(remove) + 0.1);
    tl.to(["#mini-leg", "#mini-note"], { y:0, opacity:1, duration:0.3, stagger:0.08, ease:EASE.arrive }, @w(industry));
    // the tags have done their work by the time the tiles leave; they fade with
    // the fall rather than riding it down over the row below and the caption
    tl.to(TAGS.industry.map(function (i) { return "#tag-" + i; }),
          { opacity:0, duration:0.2, stagger:0.015, ease:EASE.exit }, @w(changes));
    tl.to(tiles(TAGS.industry), { y:88, opacity:0.12, duration:0.45, stagger:0.015, ease:EASE.exit }, @w(changes));
    // ---- HOLD, unresolved: the loop is open and stays open into the iris ----
    // review Animation item 4: at least 700ms of settled, unresolved state
    // before the transition -- one curiosity loop, not answered here.
"""
    MOTION["02-promise"]["beats"] = [
        {"name": "hero rise",      "at": "@w(where)-0.1",   "area": 0.065, "dl": 224, "dur": 0.34},
        {"name": "data column up", "at": "@w(twenty)-0.45", "area": 0.32,  "dl": 224, "dur": 0.5},
        {"name": "tiles rise",     "at": "@w(trials)-0.1",  "area": 0.10,  "dl": 100, "dur": 0.46},
        {"name": "industry tags",  "at": "@w(remove)",      "area": 0.05,  "dl": 72,  "dur": 0.25},
        {"name": "tiles fall",     "at": "@w(changes)",     "area": 0.10,  "dl": 131, "dur": 0.45},
    ]
    return body, css, tl


FILES["02-promise"] = file_02_promise
