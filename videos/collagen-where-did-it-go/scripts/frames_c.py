#!/usr/bin/env python3
"""File C -- 04-barrier + 05-film. The skin cross-section's SECOND appearance
-- same actor, camera-reframed onto the surface/dermis boundary, its mesh
already carrying the damage 03-uv snapped live (restated via skin_opts_js's
`cut`, the same convention the old BUILDING actor used for its cut beams).
The molecule approaches, is sized against the ~500-dalton entry limit,
doesn't get through, and flattens into a surface film."""
from actors import (HELPERS_JS, HELIX_JS, HELIX_CSS, BARRIER_JS, BARRIER_CSS, EASE_JS,
                    kt, chip, cite, panel, abs_, skin_opts_js, MESH_DAMAGED)
from motion import MOTION


def file_04_barrier(fspan, fctx):
    css = HELIX_CSS + BARRIER_CSS + """
    .abs { position:absolute; left:0; top:0; }
    .dot { fill:var(--aqua); }
    .film { fill:var(--aqua); opacity:0; }
    .hidden-path { fill:none; stroke:none; }
    .sz { padding:var(--s-4) var(--s-5); display:flex; flex-direction:column; justify-content:center; gap:6px; }
    .sz-n { font-family:var(--font-display); font-size:var(--t-figure); line-height:1; margin:0; }
    .sz-l { font-family:var(--font-mono); font-size:var(--t-chip); letter-spacing:var(--tr-mono); margin:0; }
    #verdict5 { padding:var(--s-4) var(--s-5); display:flex; flex-direction:column; justify-content:center; gap:4px; }
    .cite { position:absolute; opacity:0; }
    .note { opacity:0; }
"""
    body = f"""
      <div class="stage">
       <div class="world" id="world">
        <svg id="skinSvg" class="abs" viewBox="0 0 1728 918" width="1728" height="918" aria-hidden="true">
          <path id="dot-path" class="hidden-path" d="M 700 60 C 700 140 700 200 700 260"/>
        </svg>
        {panel("sz-a", "dim", '<p class="sz-n" id="n500">~0</p><p class="sz-l">daltons &middot; the entry limit</p>', abs_(60, 60, 620, 160), "sz late")}
        {panel("sz-b", "coral", '<p class="sz-n" id="n300k">~0</p><p class="sz-l">daltons &middot; one collagen molecule</p>', abs_(60, 300, 620, 160), "sz late")}
        {cite("cite-da", "Exp Dermatol &middot; 2000", False, abs_(60, 480))}
        {chip("sz-note", "labelled, not to scale", "note", abs_(60, 566))}
        {panel("verdict5", "ink", '<p class="p-title">Moisturizes the surface.</p><p class="p-body on-ink">Does not replace collagen below.</p>', abs_(1080, 620, 648, 220), "late")}
       </div>
      </div>
"""
    tl = EASE_JS + HELPERS_JS + HELIX_JS + BARRIER_JS + f"""
    var svg = document.getElementById("skinSvg");
    drawBarrier(svg, {skin_opts_js(labels=False, cut=MESH_DAMAGED)});
    var mol = drawHelix(svg, {{ id:"mol", x:640, y:60, w:120, h:40, strokeW:13 }});
    var dot = el("circle", {{ cx:700, cy:60, r:9, "class":"dot", id:"dot500" }}, svg);
    // appended AFTER drawBarrier so it paints ON TOP of the opaque epidermis
    // background and brick course -- static markup placed before the JS call
    // was silently invisible under those layers (same defect as 12-recs'
    // shield). y:18 sits at the true surface line, not near the dermis
    // boundary where a prior draft mistakenly placed it.
    var film = el("rect", {{ "class":"film", id:"film", x:620, y:48, width:220, height:16, rx:8 }}, svg);

    // ---- unit 04-barrier: too large to cross ------------------------------------
    tl.fromTo("#world", {{ scale:1.04 }}, {{ scale:1, duration:0.8, ease:EASE.camera }}, 0);
    // a held beat between the camera settling and the dot's descent starting
    // on @w(be) (late in this unit's own sentence) -- a fixed early bridge
    tl.to(mol, {{ scale:1.09, duration:0.6, yoyo:true, repeat:1, ease:"sine.inOut" }}, 0.9);
    pathFollow(tl, dot, document.getElementById("dot-path"), @w(be) - 0.2, 1.3, "power1.inOut");
    reveal(tl, "#sz-a", @w(daltons) - 0.5);
    tl.fromTo("#sz-a-wash", {{ scaleX:0 }}, {{ scaleX:1, duration:0.4, ease:EASE.wipe }}, @w(daltons) - 0.5);
    count(tl, "n500", 0, 500, @w(daltons) - 0.4, 0.6, function (n) {{ return "~" + n.toLocaleString("en-GB"); }});
    reveal(tl, "#sz-b", @w(collagen) - 0.4);
    tl.fromTo("#sz-b-wash", {{ scaleX:0 }}, {{ scaleX:1, duration:0.4, ease:EASE.wipe }}, @w(collagen) - 0.4);
    tl.to(mol, {{ y:60, scale:1.16, transformOrigin:"50% 50%", duration:0.7, ease:EASE.arrive }}, @w(collagen));
    tl.to("#dot500", {{ scale:0.85, transformOrigin:"50% 50%", duration:0.4, ease:EASE.swap }}, @w(collagen) + 0.2);
    count(tl, "n300k", 0, 300000, @w(thousand) - 0.5, 1.0, function (n) {{ return "~" + n.toLocaleString("en-GB"); }});
    tl.fromTo("#cite-da", {{ opacity:0, y:16 }}, {{ opacity:1, y:0, duration:0.35, ease:EASE.arrive }}, @w(thousand) + 0.4);
    tl.to("#sz-note", {{ opacity:1, duration:0.3, ease:EASE.arrive }}, @w(thousand) + 0.6);
    // one attempt, one stop -- against a shorter unit than the old three-bounce
    tl.to(mol, {{ y:200, duration:0.4, ease:"power2.in" }}, @w(doesn't) - 0.5);
    tl.to(mol, {{ y:150, scale:1.0, duration:0.35, ease:EASE.slam }}, @w(doesn't) - 0.1);
    tl.to("[id^=skin-b-]", {{ fill:"#C97A5C", duration:0.12, yoyo:true, repeat:1, ease:EASE.slam }}, @w(through) - 0.15);
    tl.to("#world", {{ scale:1, x:0, y:0, duration:0.6, ease:EASE.camera }}, @uend(05-film) - 1.0);

    // ---- unit 05-film: flattens into a surface film -----------------------------
    // Measured on the real word manifest: the brick-flash on "through." ends
    // ~9.42s file-relative and nothing else moves until "film" flattens the
    // molecule at ~11.43s -- a genuine ~2s hole, not covered by anchoring off
    // 05-film's own start (10.10s), which is itself well inside that hole.
    tl.to(mol, {{ scale:1.10, duration:0.5, yoyo:true, repeat:1, ease:"sine.inOut" }}, @w(through) + 0.3);
    // flattens back up AT the surface (y:26, matching the film rect's new
    // position) -- not down near the dermis boundary, where a prior draft
    // mistakenly sent it (thematically wrong: a surface film sits ON the
    // skin, not deep in the tissue the molecule was just rejected from).
    tl.to(mol, {{ y:56, scaleY:0.18, scaleX:1.7, transformOrigin:"50% 50%", duration:0.6, ease:EASE.swap }}, @w(film) - 0.3);
    tl.fromTo("#film", {{ opacity:0.6, scaleX:0, transformOrigin:"50% 50%" }},
              {{ scaleX:1, duration:0.5, ease:EASE.wipe }}, @w(film));
    tl.to(["#sz-a-wash", "#sz-b-wash"], {{ scaleX:0, transformOrigin:"100% 50%", duration:0.4, stagger:0.08, ease:EASE.exit }}, @w(smoother) - 0.4);
    tl.to(["#sz-a", "#sz-b", "#sz-note", "#cite-da"], {{ opacity:0, duration:0.3, ease:EASE.exit }}, @w(smoother));
    reveal(tl, "#verdict5", @w(smoother) + 0.2);
    tl.fromTo("#verdict5-wash", {{ scaleX:0 }}, {{ scaleX:1, duration:0.45, ease:EASE.wipe }}, @w(smoother) + 0.2);
    // measured hole: nothing else moves from here to the file's own end
    // (@fown) while "but that's the surface, not structure below it" plays --
    // the verdict card just sits. A held emphasis on "not" is the beat.
    tl.to("#verdict5", {{ scale:1.06, duration:0.35, yoyo:true, repeat:1, ease:EASE.slam }}, @w(not) - 0.1);
    // duration kept short enough that this ends well before @fown (18.628) --
    // the camera-home assert requires every #world tween to settle by then
    tl.to("#world", {{ scale:1.035, duration:0.65, yoyo:true, repeat:1, ease:"sine.inOut" }}, @w(not) + 0.6);
"""
    MOTION["04-barrier"]["beats"] = [
        {"name": "camera settle", "at": "0.0", "area": 0.5, "dl": 40, "dur": 0.8},
        {"name": "size card A",  "at": "@w(daltons)-0.5",   "area": 0.066, "dl": 94, "dur": 0.4},
        {"name": "size card B",  "at": "@w(collagen)-0.4","area": 0.066, "dl": 94, "dur": 0.4},
        {"name": "molecule grows","at": "@w(collagen)",   "area": 0.05,  "dl": 72, "dur": 0.7},
        {"name": "stopped at barrier", "at": "@w(through)-0.15", "area": 0.10, "dl": 103, "dur": 0.35},
        {"name": "camera home",  "at": "@uend(05-film)-1.0","area": 0.5,  "dl": 60, "dur": 0.6},
    ]
    MOTION["05-film"]["beats"] = [
        {"name": "film spreads",  "at": "@w(film)-0.3",   "area": 0.10, "dl": 81,  "dur": 0.6},
        {"name": "cards retract", "at": "@w(smoother)-0.4","area": 0.13, "dl": 98, "dur": 0.4},
        {"name": "verdict ink",   "at": "@w(smoother)+0.2","area": 0.108,"dl": 149,"dur": 0.45},
    ]
    return body, css, tl


FILES = {"04-barrier": file_04_barrier}
