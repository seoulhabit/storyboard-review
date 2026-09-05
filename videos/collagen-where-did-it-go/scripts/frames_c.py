#!/usr/bin/env python3
"""File C -- 06-door: units 6 (door) and 7 (film). Paper ground.
The barrier close-up: surface low in the frame, a 60px "door" in the brick
course at local (404, 599) -- exactly where file B's building door stood, so
the iris opens ON the door and reveals the door. The molecule fails it three
times, is stamped, then flattens into a surface film."""
from actors import (HELPERS_JS, HELIX_JS, HELIX_CSS, BARRIER_JS, BARRIER_CSS, EASE_JS,
                    kt, chip, cite, panel, abs_)
from motion import MOTION


def file_06_door(fspan, fctx):
    css = HELIX_CSS + BARRIER_CSS + """
    .abs { position:absolute; }
    #stageD, #barSvg { position:absolute; left:0; top:0; }
    #epi-wash { position:absolute; left:47px; top:560px; width:1728px; height:140px; background:var(--aqua); }
    #derm-wash { position:absolute; left:47px; top:700px; width:1728px; height:218px; background:var(--ink-3); opacity:.9; }
    .hidden-path { fill:none; stroke:none; }
    .dot { fill:var(--aqua); }
    .film { fill:var(--aqua); opacity:0; }
    .surf-smooth { fill:none; stroke:var(--ink); stroke-width:4; opacity:0; }
    .shine { stroke:var(--paper); stroke-width:5; stroke-linecap:round; opacity:0; }
    .sz { padding:var(--s-4) var(--s-5); display:flex; flex-direction:column; justify-content:center; gap:6px; }
    .sz-n { font-family:var(--font-display); font-size:var(--t-figure); line-height:1; margin:0; }
    .sz-l { font-family:var(--font-mono); font-size:var(--t-chip); letter-spacing:var(--tr-mono); margin:0; }
    .stamp { position:absolute; left:110px; top:110px; font-family:var(--font-mono); font-weight:500;
             font-size:96px; letter-spacing:.06em; color:var(--coral); border:6px solid var(--coral);
             border-radius:var(--r-3); padding:6px 28px; transform:rotate(-9deg); opacity:0; }
    #verdict7 { padding:var(--s-4) var(--s-5); display:flex; align-items:center; background:transparent; }
    .cite { position:absolute; opacity:0; }
    .note { opacity:0; }
"""
    body = f"""
      <div class="stage">
       <div class="world" id="world">
        <svg id="barSvg" viewBox="0 0 1728 918" width="1728" height="918" aria-hidden="true"></svg>
        <div id="epi-wash"></div>
        <div id="derm-wash"></div>
        <svg id="stageD" viewBox="0 0 1728 918" width="1728" height="918" aria-hidden="true">
          <path id="dot-path" class="hidden-path" d="M 120 330 C 240 330 404 380 404 560 L 404 780"/>
          <rect class="film" id="film" x="60" y="538" width="700" height="24" rx="12"/>
          <line class="surf-smooth" id="surf-smooth" x1="0" y1="560" x2="1728" y2="560"/>
          <g id="shines"><line class="shine" x1="140" y1="546" x2="200" y2="546"/><line class="shine" x1="330" y1="546" x2="410" y2="546"/><line class="shine" x1="560" y1="546" x2="620" y2="546"/></g>
        </svg>
        {panel("sz-a", "dim", '<p class="sz-n" id="n500">~0</p><p class="sz-l">daltons · the size limit</p>', abs_(900, 40, 760, 180), "sz late")}
        {panel("sz-b", "coral", '<p class="sz-n" id="n300k">~0</p><p class="sz-l">daltons · one collagen molecule</p>', abs_(900, 250, 760, 180), "sz late")}
        {chip("sz-note", "labelled, not to scale", "note", abs_(900, 448))}
        {cite("cite-da", "Exp Dermatol &middot; 2000", False, abs_(900, 500))}
        <div class="stamp" id="stamp">REJECTED</div>
        {panel("verdict7", "ink", '<p class="p-title">surface smoothing &ne; structural replacement</p>', abs_(60, 740, 1200, 130), "late")}
       </div>
      </div>
"""
    tl = EASE_JS + HELPERS_JS + HELIX_JS + BARRIER_JS + """
    var svg = document.getElementById("stageD");
    gsap.set(["#epi-wash", "#derm-wash"], { scaleY:0, transformOrigin:"50% 0%" });   // GSAP owns these transforms
    // the barrier lives in its OWN svg below the HTML washes; actors above them
    drawBarrier(document.getElementById("barSvg"), { id:"bar", w:1728, h:918, surf:560, boundary:700,
                brickRows:2, x:47, door:{ col:2 }, hatch:{ n:8, cut:[1,2,4,6] } });
    var mol = drawHelix(svg, { id:"mol", x:189, y:330, w:430, h:110, strokeW:14 });
    var dot = el("circle", { cx:120, cy:330, r:9, "class":"dot", id:"dot500" }, svg);
    // ---- unit 6: the door -----------------------------------------------------
    tl.fromTo("#world", { scale:1.03 }, { scale:1, duration:0.9, ease:EASE.camera }, 0);
    tl.fromTo(mol, { y:0 }, { y:60, duration:0.6, ease:EASE.arrive }, @w(cream));
    // "through skin": the barrier lights up as the subject
    tl.fromTo("#epi-wash", { scaleY:0 }, { scaleY:1, duration:0.5, ease:EASE.wipe }, @w(skin));
    tl.to("#epi-wash", { scaleY:0, duration:0.4, ease:EASE.exit }, @w(skin) + 1.4);
    pathFollow(tl, dot, document.getElementById("dot-path"), @w(pass), 1.6, "power1.inOut");
    reveal(tl, "#sz-a", @w(daltons,1) - 0.5);
    tl.fromTo("#sz-a-wash", { scaleX:0 }, { scaleX:1, duration:0.4, ease:EASE.wipe }, @w(daltons,1) - 0.5);
    count(tl, "n500", 0, 500, @w(daltons,1) - 0.4, 0.6, function (n) { return "~" + n.toLocaleString("en-GB"); });
    reveal(tl, "#sz-b", @w(thousand) - 0.6);
    tl.fromTo("#sz-b-wash", { scaleX:0 }, { scaleX:1, duration:0.4, ease:EASE.wipe }, @w(thousand) - 0.6);
    // the molecule shifts while the size comparison is read out -- the cards
    // themselves are wash reveals inside a fixed panel (no outer bbox change,
    // invisible to a geometry-based motion tracker), so this fills the stretch
    tl.to(mol, { y:80, duration:0.6, ease:EASE.hold }, @w(collagen) - 0.2);
    count(tl, "n300k", 0, 300000, @w(thousand) - 0.5, 1.1, function (n) { return "~" + n.toLocaleString("en-GB"); });
    tl.to("#sz-note", { opacity:1, duration:0.3, ease:EASE.arrive }, @w(thousand) + 0.6);
    tl.to("#cite-da", { opacity:1, duration:0.3, ease:EASE.arrive }, @w(thousand) + 0.8);
    // three tries at the door, three recoils
    [0, 0.55, 1.10].forEach(function (d) {
      tl.to(mol, { y:150, duration:0.20, ease:"power2.in" }, @w(not) - 0.6 + d);
      tl.to(mol, { y:60, duration:0.28, ease:EASE.slam }, @w(not) - 0.4 + d);
    });
    // REJECTED: the epidermis flashes coral, the stamp slams, a micro-push
    tl.to("#epi-wash", { backgroundColor:"#C97A5C", duration:0.1 }, @w(door) - 0.2);
    tl.fromTo("#epi-wash", { scaleY:0 }, { scaleY:1, duration:0.18, yoyo:true, repeat:1, ease:EASE.slam }, @w(door) - 0.05);
    tl.fromTo("#stamp", { opacity:0, scale:1.5, rotate:-9 }, { opacity:1, scale:1, rotate:-9, duration:0.42, ease:EASE.slam }, @w(door));
    tl.to("#world", { scale:1.05, duration:0.25, yoyo:true, repeat:1, ease:EASE.slam }, @w(door));

    // ---- unit 7: the film ---------------------------------------------------------
    tl.to("#stamp", { opacity:0, duration:0.3, ease:EASE.exit }, @w(film) - 0.4);
    // the molecule FLATTENS onto the surface (transform-only morph) and the film appears
    tl.to(mol, { y:190, scaleY:0.15, scaleX:1.6, transformOrigin:"50% 50%", duration:0.7, ease:EASE.swap }, @w(film) - 0.3);
    tl.to("#film", { opacity:0.6, duration:0.5, ease:EASE.arrive }, @w(film));
    tl.to("#epi-wash", { backgroundColor:"#59B8AE", duration:0.1 }, @w(film) - 0.3);
    tl.fromTo("#epi-wash", { scaleY:0 }, { scaleY:1, duration:0.5, ease:EASE.wipe }, @w(film) - 0.2);
    tl.to("#epi-wash", { scaleY:0.08, duration:0.5, ease:EASE.wipe }, @w(smoother) - 0.1);
    tl.to("#bar-surface", { opacity:0, duration:0.4 }, @w(smoother));
    tl.to("#surf-smooth", { opacity:0.7, duration:0.4 }, @w(smoother));
    tl.to(["#sz-a-wash", "#sz-b-wash"], { scaleX:0, transformOrigin:"100% 50%", duration:0.4, stagger:0.08, ease:EASE.exit }, @w(smoother));
    tl.to([".sz-note", "#sz-note", "#cite-da"], { opacity:0.35, duration:0.4, ease:EASE.exit }, @w(smoother));
    tl.fromTo(".shine", { opacity:0, x:-30 }, { opacity:1, x:0, duration:0.3, stagger:0.12, ease:EASE.arrive }, @w(polishing));
    // "...replacing the beams": the dermis dims -- the hatch stays cut
    // "...is NOT replacing the beams": the dermis dims on "not", the verdict lands on "replacing" --
    // both finish before the iris opens on the next file (unit 7 ends 0.05s after its last word)
    tl.fromTo("#derm-wash", { scaleY:0 }, { scaleY:1, duration:0.5, ease:EASE.wipe }, @w(not,2) - 0.1);
    reveal(tl, "#verdict7", @w(replacing));
    tl.fromTo("#verdict7-wash", { scaleX:0 }, { scaleX:1, duration:0.45, ease:EASE.wipe }, @w(replacing));
"""
    MOTION["06-door"]["beats"] = [
        {"name": "camera settle", "at": "0.0", "area": 0.5, "dl": 40, "dur": 0.9},
        {"name": "barrier aqua", "at": "@w(skin)", "area": 0.117, "dl": 81, "dur": 0.5},
        {"name": "barrier aqua out", "at": "@w(skin)+1.4", "area": 0.117, "dl": 81, "dur": 0.4},
        {"name": "size card A", "at": "@w(daltons,1)-0.5", "area": 0.066, "dl": 94, "dur": 0.4},
        {"name": "size card B", "at": "@w(thousand)-0.6", "area": 0.066, "dl": 103, "dur": 0.4},
        {"name": "mol shift", "at": "@w(collagen)-0.2", "area": 0.03, "dl": 60, "dur": 0.6},
        {"name": "rejected flash", "at": "@w(door)-0.05", "area": 0.117, "dl": 103, "dur": 0.36},
    ]
    MOTION["07-film"]["beats"] = [
        {"name": "film wash", "at": "@w(film)-0.2", "area": 0.117, "dl": 81, "dur": 0.5},
        {"name": "cards retract", "at": "@w(smoother)", "area": 0.13, "dl": 98, "dur": 0.48},
        {"name": "dermis dim", "at": "@w(not,2)-0.1", "area": 0.18, "dl": 84, "dur": 0.5},
        {"name": "verdict ink", "at": "@w(replacing)", "area": 0.075, "dl": 215, "dur": 0.45},
    ]
    return body, css, tl


FILES = {"06-door": file_06_door}
