#!/usr/bin/env python3
"""File A -- 01-hook (unit 1). File B -- 02-mesh + 03-uv (units 2-3).

2026-09-05 editorial redesign. 01-hook opens on real skin (a graded macro
photo, CSS background-image -- never <img>, which build_frames.py's own
_static_asserts bans for the clip-path/fast-capture hazard) with one collagen
strand splitting into its two routes: cream stops at the photo's own surface
edge, powder passes through it and starts to fragment. File B introduces the
video's one persistent actor -- a horizontal skin cross-section, epidermis
over dermis, a woven collagen mesh inside the dermis -- and immediately shows
it weakening (age + UV). This same actor returns, camera-reframed and never
redrawn, in 04-barrier and 12-recs (see actors.skin_opts_js).
"""
from actors import (HELPERS_JS, HELIX_JS, HELIX_CSS, BARRIER_JS, BARRIER_CSS,
                    EASE_JS, kt, chip, panel, abs_, skin_opts_js, MESH_DAMAGED)
from motion import MOTION


def file_01_hook(fspan, fctx):
    css = HELIX_CSS + """
    .abs { position:absolute; left:0; top:0; }
    #photo { position:absolute; left:0; top:485px; width:1728px; height:433px;
             background-image:url("assets/images/skin-base.png");
             background-size:cover; background-position:center 30%;
             background-color:#DCC9AE;
             -webkit-mask-image:linear-gradient(to bottom, transparent 0%, black 14%);
             mask-image:linear-gradient(to bottom, transparent 0%, black 14%); }
    .surf { fill:none; stroke:var(--ink); stroke-width:4; opacity:.55; }
    .hidden-path { fill:none; stroke:none; }
    #hook-q { position:absolute; left:280px; top:700px; width:1160px; text-align:center; justify-content:center; }
    .lab { opacity:0; }
"""
    body = f"""
      <div class="stage">
       <div class="world" id="world">
        <div id="photo"></div>
        <svg id="stageA" class="abs" viewBox="0 0 1728 918" width="1728" height="918" aria-hidden="true">
          <path id="surf-line" class="surf" d="M 0 485 Q 220 465 440 485 T 880 485 T 1320 485 T 1728 485"/>
          <path id="drop" class="hidden-path" d="M 780 470 C 820 620 860 760 900 900"/>
        </svg>
        {chip("lab-cream", "CREAM", "lab", abs_(560, 340))}
        {chip("lab-powder", "POWDER", "lab", abs_(900, 560))}
        {kt("hook-q", "Where does it actually go?", "serif")}
       </div>
      </div>
"""
    tl = EASE_JS + HELPERS_JS + HELIX_JS + """
    var svg = document.getElementById("stageA");
    var mol = drawHelix(svg, { id:"mol", x:520, y:280, w:340, h:90, strokeW:15 });
    var molb = drawHelix(svg, { id:"mol-b", x:640, y:420, w:280, h:70, strokeW:11, segs:3 });
    molb.style.opacity = "0";
    var drop = document.getElementById("drop");

    // frame zero: the strand is already in frame, already moving -- nothing
    // fades in from black
    tl.fromTo(mol, { y:-40 }, { y:0, duration:1.0, ease:"power1.out" }, 0);
    tl.fromTo("#lab-cream", { opacity:0, y:10 }, { opacity:1, y:0, duration:0.3, ease:EASE.arrive }, @w(cream));
    // CREAM: settles right at the photo's own surface edge and stops
    tl.to(mol, { y:52, duration:0.6, ease:EASE.arrive }, @w(cream) + 0.1);
    tl.to(mol, { scale:1.05, duration:0.16, yoyo:true, repeat:1, ease:EASE.slam }, @w(stops));
    tl.to("#surf-line", { stroke:"#59B8AE", strokeWidth:6, duration:0.3, yoyo:true, repeat:1 }, @w(stops));

    // POWDER: the SAME actor splits off, not a new one fading in
    tl.fromTo("#lab-powder", { opacity:0, y:10 }, { opacity:1, y:0, duration:0.3, ease:EASE.arrive }, @w(powder));
    tl.fromTo(molb, { opacity:1, scale:0.2, transformOrigin:"50% 50%" },
              { scale:1, duration:0.3, ease:EASE.slam }, @w(powder));
    var end = pathFollow(tl, molb, drop, @w(different), 1.3, "power1.in");
    // BREAKING APART: passes through the surface photo and starts to fragment --
    // the foreshadow digestion pays off in full
    for (var s = 0; s < 3; s++) {
      tl.to("#mol-b-seg-" + s, { x:(s - 1) * (26 + 10 * s), y:14 * s, rotation:(s - 1) * 30,
             opacity:0.75, duration:0.5, ease:EASE.slam }, @w(apart) + s * 0.08);
    }
    tl.to(molb, { opacity:0.35, duration:0.6, ease:EASE.exit }, @w(goes) - 0.1);

    // ONE question, stated plainly once both routes have played out
    kineticWords(tl, "#hook-q", @w(where) - 0.1, 0.08, "rise");
    // converge: both actors settle where the next iris opens
    tl.to(mol, { x:344, y:226, duration:0.6, ease:EASE.camera }, @we(go) - 0.5);
    tl.to(molb, { opacity:0, duration:0.4, ease:EASE.exit }, @we(go) - 0.5);
"""
    MOTION["01-hook"]["beats"] = [
        {"name": "cream settles",   "at": "@w(cream)+0.1",   "area": 0.06,  "dl": 80,  "dur": 0.6},
        {"name": "surface flash",   "at": "@w(stops)",       "area": 0.10,  "dl": 60,  "dur": 0.3},
        {"name": "powder splits",   "at": "@w(powder)",      "area": 0.05,  "dl": 90,  "dur": 0.3},
        {"name": "powder fragments","at": "@w(apart)",       "area": 0.06,  "dl": 90,  "dur": 0.5},
        {"name": "question rises",  "at": "@w(where)-0.1",   "area": 0.09,  "dl": 224, "dur": 0.34},
        {"name": "converge",        "at": "@we(go)-0.5",     "area": 0.06,  "dl": 60,  "dur": 0.6},
    ]
    return body, css, tl


FILES = {"01-hook": file_01_hook}


# ---------------------------------------------------------------- File B -- 02-mesh + 03-uv

def file_02_mesh(fspan, fctx):
    """The one persistent actor's first appearance -- introduced in full, then
    immediately weakened. Labels appear ONCE, here; every later reframing of
    this same actor (04-barrier, 12-recs) passes labels:false."""
    css = BARRIER_CSS + """
    .abs { position:absolute; left:0; top:0; }
    .sun { fill:var(--highlighter); }
    .ray { stroke:var(--highlighter); stroke-width:5; stroke-linecap:round; opacity:0; }
    /* #mesh-kt had no explicit position and fell into normal document flow at
       .world's top-left origin -- directly over the epidermis brick course
       (confirmed on the rough-preview render: the kinetic text rendered
       interleaved with the brick rects, illegible). Centered in the open
       dermis space instead, where the mesh lines have room around them. */
    #mesh-kt { position:absolute; left:0; top:520px; width:1728px;
               text-align:center; justify-content:center; }
"""
    body = f"""
      <div class="stage">
       <div class="world" id="world">
        <svg id="skinSvg" class="abs" viewBox="0 0 1728 918" width="1728" height="918" aria-hidden="true">
          <circle class="sun" id="sun" cx="1560" cy="70" r="0"/>
          <g id="rays">
            <line class="ray" x1="1560" y1="20" x2="1560" y2="0"/>
            <line class="ray" x1="1610" y1="45" x2="1630" y2="28"/>
            <line class="ray" x1="1610" y1="95" x2="1630" y2="112"/>
          </g>
        </svg>
        {kt("mesh-kt", "a support mesh", "serif")}
       </div>
      </div>
"""
    tl = EASE_JS + HELPERS_JS + BARRIER_JS + f"""
    var svg = document.getElementById("skinSvg");
    drawBarrier(svg, {skin_opts_js(labels=True)});
    // the whole mesh starts undrawn -- it draws IN as "support mesh" is said,
    // never sitting pre-formed before the claim is made
    var fibres = [];
    for (var i = 0; i < 10; i++) {{ fibres.push("#skin-h-" + i); fibres.push("#skin-hb-" + i); }}
    fibres.forEach(function (sel) {{
      var L = document.querySelector(sel); L.style.strokeDashoffset = L.getAttribute("data-len");
    }});
    tl.fromTo("#world", {{ scale:1.05 }}, {{ scale:1, duration:1.0, ease:EASE.camera }}, 0);
    drawIn(tl, "#skin-surface", 0.1, 0.7, 0, EASE.wipe);
    // stratum-corneum brick course settles in behind the surface line
    tl.fromTo("[id^=skin-b-]", {{ opacity:0, y:-10 }}, {{ opacity:1, y:0, duration:0.4, stagger:0.008, ease:EASE.arrive }}, 0.3);
    drawIn(tl, fibres.join(","), @w(support) - 0.5, 0.7, 0.02, EASE.wipe);
    kineticWords(tl, "#mesh-kt", @w(under) - 0.1, 0.08, "rise");
    // a held beat between the brick course settling (~0.7s) and the mesh
    // draw-in beginning (@w(support)-0.5, itself late in a short unit) -- a
    // fixed early anchor, not word-relative, since the gap sits BEFORE
    // "support" is even spoken. A bounded camera micro-drift keeps it alive.
    tl.to("#world", {{ scale:1.035, duration:1.0, yoyo:true, repeat:1, ease:"sine.inOut" }}, 0.9);
    tl.to("#mesh-kt", {{ opacity:0, duration:0.3, ease:EASE.exit }}, @uend(03-uv) - 2.4);

    // ---- 03-uv: age + ultraviolet weaken the mesh, live ------------------------
    tl.fromTo("#sun", {{ attr:{{ r:0 }} }}, {{ attr:{{ r:34 }}, duration:0.6, ease:EASE.arrive }}, @w(age));
    tl.to(".ray", {{ opacity:0.85, duration:0.4, stagger:0.06, ease:EASE.arrive }}, @w(age) + 0.2);
    var DAMAGED = {MESH_DAMAGED};
    DAMAGED.forEach(function (i, k) {{
      snapMeshFibers("skin", [i], tl, @w(break) + k * 0.22, 0);
    }});
    tl.to(["#sun", "#rays"], {{ opacity:0.5, duration:0.5, ease:EASE.hold }}, @w(down) - 0.3);
    // camera settles home before the next iris opens ON this actor's own state
    tl.to("#world", {{ scale:1, x:0, y:0, duration:0.7, ease:EASE.camera }}, @uend(03-uv) - 0.8);
"""
    MOTION["02-mesh"]["beats"] = [
        {"name": "camera settle", "at": "0.0", "area": 0.5, "dl": 60, "dur": 1.0},
        {"name": "surface draws", "at": "0.1", "area": 0.15, "dl": 70, "dur": 0.7},
        {"name": "mesh draws in", "at": "@w(support)-0.5", "area": 0.20, "dl": 65, "dur": 0.7},
    ]
    MOTION["03-uv"]["beats"] = [
        {"name": "sun rises",    "at": "@w(age)",       "area": 0.05, "dl": 90,  "dur": 0.6},
        {"name": "fibre snap 1", "at": "@w(break)",     "area": 0.04, "dl": 103, "dur": 0.42},
        {"name": "fibre snap 3", "at": "@w(break)+0.44","area": 0.04, "dl": 103, "dur": 0.42},
        {"name": "camera home",  "at": "@uend(03-uv)-0.8", "area": 0.5, "dl": 60, "dur": 0.7},
    ]
    return body, css, tl


FILES["02-mesh"] = file_02_mesh
