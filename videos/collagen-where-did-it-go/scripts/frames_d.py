#!/usr/bin/env python3
"""File D -- 06-swallow + 07-dispatch. THE most continuous journey in the
piece, kept almost exactly as before: the molecule leaves the scoop, follows
ONE tract path, fragments in the stomach into peptides and amino-acid dots,
and the dots are dispatched along four branches. 2026-09-05 redesign removes
the floating scaffolding card, spare-parts crate and evidence-teaser panel --
the brief's one spatial pathway needs no cards anchored beside it, and its
one message is "no guaranteed delivery to your face."."""
from actors import (HELPERS_JS, HELIX_JS, HELIX_CSS, TRACT_JS, TRACT_CSS,
                    EASE_JS, kt, chip, panel, abs_)
from motion import MOTION

DESTS = [("skin", "skin", 120), ("joints", "joints", 300), ("tendons", "tendons", 480), ("other", "other tissue", 660)]


def file_06_swallow(fspan, fctx):
    css = HELIX_CSS + TRACT_CSS + """
    .abs { position:absolute; left:0; top:0; }
    .scoop { fill:var(--mist); stroke:var(--ink); stroke-width:5; }
    .fr { fill:var(--coral); opacity:0; }
    .face { fill:none; stroke:var(--ink); stroke-width:5; }
    .void { z-index:2; }
    .dest { padding:var(--s-3) var(--s-4); display:flex; align-items:center; }
    .dest .p-title { margin:0; font-size:var(--t-body); }
    #stomach-p { background:transparent; }
"""
    dests = "".join(panel(f"d-{k}", "aqua", f'<p class="p-title">{label}</p>', abs_(1340, y, 380, 150), "dest late")
                    for k, label, y in DESTS)
    body = f"""
      <div class="stage">
       <div class="world" id="world">
        {panel("stomach-p", "aqua", "<span></span>", abs_(640, 560, 520, 280))}
        <svg id="stageE" viewBox="0 0 1728 918" width="1728" height="918" aria-hidden="true">
          <g id="scoop"><path class="scoop" d="M 250 535 Q 250 640 404 640 Q 558 640 558 535 Z"/><path class="scoop" d="M 250 540 L 130 500" fill="none"/></g>
        </svg>
        {panel("face", "dim", '<svg viewBox="0 0 200 200" width="180" height="180" aria-hidden="true"><path class="face" d="M 60 30 C 130 20 160 70 150 120 C 145 150 120 160 118 180 M 150 120 L 168 128 L 152 140"/><circle class="face" cx="110" cy="70" r="6"/></svg>' +
               chip("face-chip", "no guaranteed delivery", "") + '<div class="void" id="face-void"></div>', abs_(60, 60, 520, 240), "card late")}
        {dests}
       </div>
      </div>
"""
    tl = EASE_JS + HELPERS_JS + HELIX_JS + TRACT_JS + """
    var svg = document.getElementById("stageE");
    drawTract(svg);
    var tract = document.getElementById("tract"), L = tract.getTotalLength();
    ["#tract", "#br-skin", "#br-joints", "#br-tendons", "#br-other"].forEach(function (id) {
      var p = document.querySelector(id); var len = p.getTotalLength();
      p.style.strokeDasharray = len; p.style.strokeDashoffset = len;
    });
    var mol = drawHelix(svg, { id:"mol", x:254, y:530, w:300, h:84, strokeW:12, segs:6 });
    var q62 = tract.getPointAtLength(0.62 * L);
    var OFF = [[-46,-30],[-20,-38],[10,-32],[34,-16],[-8,-6],[20,8]];
    var dots = OFF.map(function (o, i) { return el("circle", { cx:q62.x + o[0], cy:q62.y + o[1], r:10, "class":"fr", id:"fr-" + i }, svg); });

    // ---- unit 06-swallow: swallow, fragment ----------------------------------
    tl.fromTo("#world", { scale:1.03 }, { scale:1, duration:0.9, ease:EASE.camera }, 0);
    // bridge between the tract drawing in and the fragmentation beat
    tl.to("#scoop", { y:-6, duration:0.6, yoyo:true, repeat:1, ease:"sine.inOut" }, 2.1);
    tl.to("#scoop", { rotation:-22, svgOrigin:"250 540", duration:0.5, ease:EASE.swap }, @w(powder));
    drawIn(tl, "#tract", @w(swallow) - 0.2, 1.5, 0, EASE.wipe);
    pathFollow(tl, mol, tract, @w(swallow), 2.0, "power1.inOut", { to:0.62, rotate:true });
    tl.fromTo("#stomach-p-wash", { scaleX:0 }, { scaleX:1, duration:0.5, ease:EASE.wipe }, @w(breaks) - 0.1);
    for (var s = 0; s < 6; s++) {
      tl.fromTo("#mol-seg-" + s, { x:0, y:0, rotation:0 }, { x:(s % 2 ? 1 : -1) * (20 + 8 * s), y:-40 + 14 * s,
                rotation:(s % 2 ? 35 : -35), duration:0.4, ease:EASE.slam }, @w(breaks) + s * 0.05);
      tl.to("#mol-seg-" + s, { scale:0.25, opacity:0, duration:0.28, ease:EASE.swap }, @w(peptides) + s * 0.05);
      tl.fromTo("#fr-" + s, { opacity:1, scale:0, transformOrigin:"50% 50%" },
                { scale:1, duration:0.28, ease:EASE.slam }, @w(peptides) + s * 0.05 + 0.1);
    }
    var SPREAD = [[-34,-18],[-16,-26],[12,-22],[30,-10],[-6,10],[22,16]];
    dots.forEach(function (d, i) {
      tl.to(d, { x:SPREAD[i][0], y:SPREAD[i][1], duration:1.0, ease:EASE.hold }, @w(amino) - 0.3);
    });

    // ---- unit 07-dispatch: the body decides where the pieces go --------------
    // bridge between the fragments settling and the face-card reveal
    tl.to(dots, { scale:1.06, duration:0.7, yoyo:true, repeat:1, stagger:0.03, ease:"sine.inOut" }, @ustart(07-dispatch) + 0.6);
    tl.fromTo("#face", { opacity:0, y:-30 }, { opacity:1, y:0, duration:0.4, ease:EASE.arrive }, @w(they) - 0.2);
    tl.fromTo("#face-wash", { scaleX:0 }, { scaleX:1, duration:0.4, ease:EASE.wipe }, @w(they) - 0.1);
    dots.forEach(function (d, i) {
      pathFollow(tl, d, tract, @w(enter) + i * 0.08, 1.0, "power1.inOut", { from:0.62, to:1, ox:q62.x, oy:q62.y });
    });   // owns each dot's frame-zero pose; the branches below pass set:false
    tl.to("#stomach-p-wash", { scaleX:0, transformOrigin:"100% 50%", duration:0.4, ease:EASE.exit }, @w(enter) + 0.3);
    // measured hole: "wherever the body decides they're needed most" carries
    // nothing visual between the destination cards settling (~7.5s) and the
    // first dispatch landing on "skin," (~10.0s) -- a ~2.5s gap otherwise
    tl.to(dots, { scale:1.05, duration:0.7, yoyo:true, repeat:1, stagger:0.02, ease:"sine.inOut" }, @w(wherever) - 0.2);
    tl.to("#world", { scale:1.12, x:-150, y:-30, duration:0.9, ease:EASE.camera }, @w(bloodstream));
    drawIn(tl, "#br-skin,#br-joints,#br-tendons,#br-other", @w(bloodstream) + 0.2, 0.7, 0.12, EASE.wipe);
    ["skin", "joints", "tendons", "other"].forEach(function (k, i) {
      tl.fromTo("#d-" + k, { opacity:0, x:26 }, { opacity:1, x:0, duration:0.4, ease:EASE.arrive },
                @w(bloodstream) + 0.35 + i * 0.12);
    });
    // no explicit word names the fourth ("other tissue") destination -- one
    // possible destination among several, per the brief -- so it dispatches
    // just after "tendons", where the sentence's own list runs out
    var GO = [["skin", [0], @w(skin)], ["joints", [1, 2], @w(joints)], ["tendons", [3, 4], @w(tendons)],
              ["other", [5], @w(tendons) + 0.5]];
    GO.forEach(function (g) {
      var br = document.getElementById("br-" + g[0]);
      g[1].forEach(function (i, k) { pathFollow(tl, dots[i], br, g[2] + k * 0.08, 0.65, "power1.inOut", { ox:q62.x, oy:q62.y, set:false }); });
      tl.fromTo("#d-" + g[0] + "-wash", { scaleX:0 }, { scaleX:1, duration:0.25, ease:EASE.wipe }, g[2] + 0.5);
      tl.to("#d-" + g[0], { x:-18, duration:0.18, yoyo:true, repeat:1, ease:EASE.slam }, g[2] + 0.55);
    });
    // "No guaranteed delivery to your face": the struck route is named at last
    tl.to("#face-void", { opacity:0.85, duration:0.3, ease:EASE.wipe }, @w(guaranteed));
    tl.to("#world", { scale:1, x:0, y:0, duration:0.7, ease:EASE.camera }, @uend(07-dispatch) - 0.8);
"""
    MOTION["06-swallow"]["beats"] = [
        {"name": "camera settle", "at": "0.0", "area": 0.5, "dl": 40, "dur": 0.9},
        {"name": "stomach wash", "at": "@w(breaks)-0.1", "area": 0.07, "dl": 81, "dur": 0.5},
        {"name": "fragments drift", "at": "@w(amino)-0.3", "area": 0.04, "dl": 90, "dur": 1.0},
    ]
    MOTION["07-dispatch"]["beats"] = [
        {"name": "face card",   "at": "@w(they)-0.2",   "area": 0.06, "dl": 84,  "dur": 0.4},
        {"name": "stomach retract", "at": "@w(enter)+0.3", "area": 0.07, "dl": 81, "dur": 0.4},
        {"name": "camera push", "at": "@w(bloodstream)", "area": 0.5, "dl": 60, "dur": 0.9},
        {"name": "destinations build", "at": "@w(bloodstream)+0.35", "area": 0.13, "dl": 70, "dur": 0.76},
        {"name": "skin lands",   "at": "@w(skin)+0.5",    "area": 0.0275, "dl": 81, "dur": 0.25},
        {"name": "tendons land", "at": "@w(tendons)+0.5",  "area": 0.0275, "dl": 81, "dur": 0.25},
        {"name": "no delivery void", "at": "@w(guaranteed)", "area": 0.06, "dl": 103, "dur": 0.3},
        {"name": "camera home", "at": "@uend(07-dispatch)-0.8", "area": 0.5, "dl": 60, "dur": 0.7},
    ]
    return body, css, tl


FILES = {"06-swallow": file_06_swallow}
