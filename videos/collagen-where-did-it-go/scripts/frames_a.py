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
    #epi-wash { position:absolute; left:1067px; top:0; width:177px; height:918px; background:var(--coral);
                transform:scaleX(0); transform-origin:0% 50%; }
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
    tl.to(molb, { opacity:1, duration:0.2, ease:EASE.arrive }, @w(powder));
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
    css = HELIX_CSS + """
    .abs { position:absolute; }
    #stageB { position:absolute; left:0; top:0; }
    #promise-q { position:absolute; left:0; top:60px; width:1000px; }
    .qmark { font-family:var(--font-display); font-size:200px; line-height:1; fill:var(--ink-3); }
    #twist { padding:var(--s-3) var(--s-5); display:flex; align-items:center; }
    #twist .kicker { margin:0; }
    #minitiles { background:var(--mist); padding:var(--s-4); }
    .mini-grid { display:grid; grid-template-columns:repeat(8, 1fr); grid-template-rows:repeat(3, 1fr);
                 gap:10px; height:210px; }
    .tr.mini { border-radius:var(--r-2); background:#4A453E; border:2px solid #6A6459; }
    .mini-cap { position:absolute; left:20px; bottom:14px; }
    #protect { padding:var(--s-4) var(--s-5); display:flex; align-items:center; }
"""
    body = f"""
      <div class="stage">
       <div class="world" id="world">
        {kt("promise-q", "Where does it actually go?", "serif")}
        <svg id="stageB" viewBox="0 0 1728 918" width="1728" height="918" aria-hidden="true">
          <text class="qmark" x="1000" y="640">?</text>
        </svg>
        {panel("twist", "coral", '<p class="kicker">stay for the twist</p>', abs_(1100, 60, 628, 100), "late")}
        {panel("minitiles", "ink", '<div class="mini-grid" id="mini-grid"></div>' + chip("mini-cap", "23 trials", "on-ink mini-cap"), abs_(1100, 190, 628, 330), "late")}
        {panel("protect", "aqua", '<p class="p-title">&hellip;and what protects it?</p>', abs_(0, 720, 1000, 140), "late")}
       </div>
      </div>
"""
    tl = EASE_JS + HELPERS_JS + HELIX_JS + TILES_JS + """
    var svg = document.getElementById("stageB");
    // the molecule is parked at the frame centre -- exactly where the iris opened
    drawHelix(svg, { id:"mol", x:654, y:506, w:420, h:110, strokeW:14 });
    drawTiles(document.getElementById("mini-grid"), 23, { size:"mini" });
    tl.set(".tr.mini", { scaleY:0.6, opacity:0 }, 0);
    kineticWords(tl, "#promise-q", @w(where) - 0.1, 0.09, "rise");
    reveal(tl, "#twist", @w(twist) - 0.2);
    tl.fromTo("#twist-wash", { scaleX:0 }, { scaleX:1, duration:0.45, ease:EASE.wipe }, @w(twist) - 0.2);
    // the FORESHADOW: 23 mini tiles, about half of them flagged
    reveal(tl, "#minitiles", @w(trials) - 0.4);
    tl.fromTo("#minitiles-wash", { scaleX:0 }, { scaleX:1, duration:0.5, ease:EASE.wipe }, @w(trials) - 0.4);
    tl.to(".tr.mini", { scaleY:1, opacity:1, duration:0.3, stagger:0.02, ease:EASE.arrive }, @w(trials) - 0.1);
    tl.fromTo("#mini-cap", { opacity:0 }, { opacity:1, duration:0.3, ease:EASE.arrive }, @w(trials) + 0.3);
    tl.to(tiles(TAGS.industry), { backgroundColor:"#C97A5C", duration:0.25, yoyo:true, repeat:5, stagger:0.01, ease:EASE.swap }, @w(remove));
    tl.to(tiles(TAGS.industry), { opacity:0.12, duration:0.5, stagger:0.01, ease:EASE.exit }, @w(industry) + 0.4);
    tl.to("#minitiles-wash", { backgroundColor:"#9C978D", duration:0.5, ease:EASE.swap }, @w(industry) + 0.4);
    tl.to("#mini-cap", { color:"#131516", backgroundColor:"#F0EBE1", duration:0.4 }, @w(industry) + 0.4);
    reveal(tl, "#protect", @w(first) - 0.1);
    tl.fromTo("#protect-wash", { scaleX:0 }, { scaleX:1, duration:0.5, ease:EASE.wipe }, @w(first) - 0.1);
    tl.to("#mol", { y:-24, duration:0.6, yoyo:true, repeat:1, ease:EASE.hold }, @w(protects));
"""
    MOTION["02-promise"]["beats"] = [
        {"name": "hero rise", "at": "@w(where)-0.1", "area": 0.065, "dl": 224, "dur": 0.34},
        {"name": "twist coral", "at": "@w(twist)-0.2", "area": 0.033, "dl": 103, "dur": 0.45},
        {"name": "mini tiles ink", "at": "@w(trials)-0.4", "area": 0.10, "dl": 224, "dur": 0.5},
        {"name": "industry dim", "at": "@w(industry)+0.4", "area": 0.10, "dl": 131, "dur": 0.5},
        {"name": "protect wash", "at": "@w(first)-0.1", "area": 0.068, "dl": 91, "dur": 0.5},
    ]
    return body, css, tl


FILES["02-promise"] = file_02_promise
