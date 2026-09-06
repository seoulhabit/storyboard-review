#!/usr/bin/env python3
"""File D -- 08-digestion: units 8 (digestion) and 9 (dispatch). Paper ground.
THE most continuous journey in the piece: the molecule leaves the scoop,
follows ONE tract path, fragments in the stomach into peptides and amino-acid
dots, and the dots are dispatched along four branches -- the body decides."""
from actors import (HELPERS_JS, HELIX_JS, HELIX_CSS, BUILDING_JS, BUILDING_CSS, TRACT_JS, TRACT_CSS,
                    PLATE_CSS, EASE_JS, kt, chip, cite, panel, plate, abs_)
from motion import MOTION

DESTS = [("skin", "skin", 120), ("joints", "joints", 300), ("tendons", "tendons", 480), ("other", "other tissue", 660)]


def file_08_digestion(fspan, fctx):
    css = HELIX_CSS + TRACT_CSS + BUILDING_CSS + PLATE_CSS + """
    .abs { position:absolute; }
    #stageE { position:absolute; left:0; top:0; }
    /* the real scoop, as a match-cut entry into the line-drawn tract below --
       gone before the tract itself draws in, never lingering behind the
       abstract journey (BRIEF.md: no organs, no anatomy stand-in). */
    #scoop-plate { position:absolute; left:0; top:0; width:100%; height:100%; }
    .scoop { fill:var(--mist); stroke:var(--ink); stroke-width:5; }
    .fr { fill:var(--coral); opacity:0; }
    .card { padding:var(--s-4); display:flex; align-items:center; gap:var(--s-4); }
    .card .chip { position:relative; }
    .face { fill:none; stroke:var(--ink); stroke-width:5; }
    .void { z-index:2; }
    .dest { padding:var(--s-3) var(--s-4); display:flex; align-items:center; }
    .dest .p-title { margin:0; font-size:var(--t-body); }
    #decides { padding:var(--s-4) var(--s-5); display:flex; align-items:center; }
    #stomach-p { background:transparent; }
    .slat { fill:var(--paper); stroke:var(--ink); stroke-width:4; }
    #bmini .beam { stroke-width:12; }
"""
    # `late`: the four destinations are the ANSWER to "your body decides where
    # they go", and without it they sat fully readable from the file's first
    # frame -- eleven seconds before the line, with the right half of the frame
    # holding them static the whole time. They now build with the branch map.
    dests = "".join(panel(f"d-{k}", "aqua", f'<p class="p-title">{label}</p>', abs_(1340, y, 380, 150), "dest late")
                    for k, label, y in DESTS)
    body = f"""
      <div class="stage">
       <div class="world" id="world">
        {plate("scoop-plate", "assets/images/collagen-powder-scoop.png",
               filt="filter:saturate(.88) contrast(1.02);", scrim="rgba(247,245,240,.30)")}
        {panel("stomach-p", "aqua", "<span></span>", abs_(640, 560, 520, 280))}
        <svg id="stageE" viewBox="0 0 1728 918" width="1728" height="918" aria-hidden="true">
          <g id="scoop"><path class="scoop" d="M 250 535 Q 250 640 404 640 Q 558 640 558 535 Z"/><path class="scoop" d="M 250 540 L 130 500" fill="none"/></g>
        </svg>
        {panel("face", "dim", '<svg viewBox="0 0 200 200" width="180" height="180" aria-hidden="true"><path class="face" d="M 60 30 C 130 20 160 70 150 120 C 145 150 120 160 118 180 M 150 120 L 168 128 L 152 140"/><circle class="face" cx="110" cy="70" r="6"/></svg>' +
               chip("face-chip", "no facial delivery", "") + '<div class="void" id="face-void"></div>', abs_(60, 60, 520, 240), "card")}
        {panel("decides", "dim", '<p class="p-title">your body decides</p>', abs_(640, 40, 700, 130), "late")}
        {dests}
        {panel("scaff", "aqua", '<svg id="bmini" viewBox="0 0 620 720" width="150" height="174" aria-hidden="true"></svg>' + chip("scaff-chip", "scaffolding", ""), abs_(60, 380, 520, 220), "card late")}
        {panel("crate", "coral", '<svg viewBox="0 0 200 160" width="180" height="144" aria-hidden="true"><rect class="slat" x="10" y="40" width="180" height="110" rx="6"/><rect class="slat" id="slat-1" x="10" y="40" width="180" height="26"/><rect class="slat" id="slat-2" x="10" y="82" width="180" height="26"/><rect class="slat" id="slat-3" x="10" y="124" width="180" height="26"/></svg>' + chip("crate-chip", "spare parts", ""), abs_(60, 640, 520, 240), "card late")}
        {panel("benefit-teaser", "aqua", '<svg viewBox="0 0 200 110" width="160" height="88" aria-hidden="true"><path class="face" id="benefit-line" d="M 15 95 L 65 55 L 105 72 L 175 15" fill="none"/><path class="face" id="benefit-head" d="M 175 15 L 148 18 M 175 15 L 172 42" fill="none"/></svg>' + chip("benefit-chip", "modest benefit", ""), abs_(640, 560, 520, 280), "card late")}
       </div>
      </div>
"""
    tl = EASE_JS + HELPERS_JS + HELIX_JS + BUILDING_JS + TRACT_JS + """
    var svg = document.getElementById("stageE");
    drawTract(svg);
    // match-cut: the real photo covers the line-drawn scoop for a beat, then
    // clears before the tract takes the frame. #scoop itself is NEVER
    // hidden -- it keeps its ORIGINAL default-visible state and its own
    // @w(powder) rotation tween untouched. That rotation fires at 0.38s
    // file-relative, inside check-seams' own iris-midpoint/settled-frame
    // sample window (0.275s / 0.6s) -- it is the only visible motion that
    // keeps those two samples looking genuinely different in the shipped
    // master (measured 25.6dB there). An earlier version of this beat hid
    // #scoop until the photo cleared, which silenced that rotation and
    // made the two samples nearly identical (measured 32.3-32.6dB, over
    // the 30.0dB ceiling, regardless of the photo's own fade timing) --
    // the defect was never the photo's opacity curve, it was suppressing
    // the one thing already making that window read as a real wipe.
    gsap.set("#scoop-plate", { opacity:0 });
    pushPlate(tl, "scoop-plate", 1.0, 1.05, 0.65, 0.6);
    tl.fromTo("#scoop-plate", { opacity:0 }, { opacity:1, duration:0.25, ease:EASE.arrive }, 0.65);
    tl.to("#scoop-plate", { opacity:0, duration:0.2, ease:EASE.exit }, 1.05);
    var tract = document.getElementById("tract"), L = tract.getTotalLength();
    // the tract and branches are hidden until drawn
    ["#tract", "#br-skin", "#br-joints", "#br-tendons", "#br-other"].forEach(function (id) {
      var p = document.querySelector(id); var len = p.getTotalLength();
      p.style.strokeDasharray = len; p.style.strokeDashoffset = len;
    });
    var mol = drawHelix(svg, { id:"mol", x:254, y:530, w:300, h:84, strokeW:12, segs:6 });
    var q62 = tract.getPointAtLength(0.62 * L);
    var OFF = [[-46,-30],[-20,-38],[10,-32],[34,-16],[-8,-6],[20,8]];
    var dots = OFF.map(function (o, i) { return el("circle", { cx:q62.x + o[0], cy:q62.y + o[1], r:10, "class":"fr", id:"fr-" + i }, svg); });
    drawBuilding(svg, { into:document.getElementById("bmini") });
    CUT_ORDER.forEach(function (k) { var e = document.getElementById("beam-" + k); e.style.strokeDashoffset = "640"; e.style.opacity = "0.25"; });

    // ---- unit 8: swallow, fragment, no facial delivery ---------------------------
    tl.fromTo("#world", { scale:1.03 }, { scale:1, duration:0.9, ease:EASE.camera }, 0);
    tl.to("#scoop", { rotation:-22, svgOrigin:"250 540", duration:0.5, ease:EASE.swap }, @w(powder));
    drawIn(tl, "#tract", @w(swallow) - 0.2, 1.6, 0, EASE.wipe);
    pathFollow(tl, mol, tract, @w(swallow), 2.2, "power1.inOut", { to:0.62, rotate:true });
    // the stomach: the molecule breaks into six segments, which become dots
    tl.fromTo("#stomach-p-wash", { scaleX:0 }, { scaleX:1, duration:0.5, ease:EASE.wipe }, @w(breaks) - 0.1);
    for (var s = 0; s < 6; s++) {
      tl.fromTo("#mol-seg-" + s, { x:0, y:0, rotation:0 }, { x:(s % 2 ? 1 : -1) * (20 + 8 * s), y:-40 + 14 * s,
                rotation:(s % 2 ? 35 : -35), duration:0.45, ease:EASE.slam }, @w(breaks) + s * 0.05);
      tl.to("#mol-seg-" + s, { scale:0.25, opacity:0, duration:0.3, ease:EASE.swap }, @w(peptides) + s * 0.06);
      // the fragment CONDENSES out of the segment that just flew apart
      tl.fromTo("#fr-" + s, { opacity:1, scale:0, transformOrigin:"50% 50%" },
                { scale:1, duration:0.3, ease:EASE.slam }, @w(peptides) + s * 0.06 + 0.1);
    }
    // the fragments drift apart while "peptides and amino acids" is said: they
    // are loose pieces now, and 2.3s of identical frames sat here otherwise
    var SPREAD = [[-34,-18],[-16,-26],[12,-22],[30,-10],[-6,10],[22,16]];
    dots.forEach(function (d, i) {
      tl.to(d, { x:SPREAD[i][0], y:SPREAD[i][1], duration:1.4, ease:EASE.hold }, @w(amino) - 0.5);
    });
    tl.fromTo("#face", { opacity:0, y:-30 }, { opacity:1, y:0, duration:0.4, ease:EASE.arrive }, @w(stomach) - 0.3);
    tl.fromTo("#face-wash", { scaleX:0 }, { scaleX:1, duration:0.4, ease:EASE.wipe }, @w(stomach) - 0.2);
    tl.to("#face-void", { opacity:0.85, duration:0.3, ease:EASE.wipe }, @w(facial));
    // the struck route leaves the frame: it is closed, and the 1.9s between
    // the strike and the dots setting off held completely still
    tl.to("#face", { x:-120, opacity:0.35, duration:1.1, ease:EASE.exit }, @we(delivery) + 0.15);

    // ---- unit 9: the body decides where the pieces go -----------------------------
    // "some pieces may be absorbed / certain peptides act as signals" was cut
    // from vo_lines.py (trim target: the middle of the piece, per the review);
    // the unit now opens directly on "But your body decides...", so the
    // stomach-to-branch dispatch anchors on the unit's own first/near-first
    // words instead of the removed hedge sentence.
    dots.forEach(function (d, i) {
      pathFollow(tl, d, tract, @w(but) + i * 0.08, 1.1, "power1.inOut", { from:0.62, to:1, ox:q62.x, oy:q62.y });
    });   // this call owns each dot's frame-zero pose; the branches below pass set:false
    tl.to("#stomach-p-wash", { scaleX:0, transformOrigin:"100% 50%", duration:0.4, ease:EASE.exit }, @w(but) + 0.3);
    // reframe onto the distribution map: the branches, not the gut, are the subject now
    tl.to("#world", { scale:1.12, x:-150, y:-30, duration:0.9, ease:EASE.camera }, @w(body));
    drawIn(tl, "#br-skin,#br-joints,#br-tendons,#br-other", @w(body) + 0.2, 0.7, 0.12, EASE.wipe);
    ["skin", "joints", "tendons", "other"].forEach(function (k, i) {
      tl.fromTo("#d-" + k, { opacity:0, x:26 }, { opacity:1, x:0, duration:0.4, ease:EASE.arrive },
                @w(body) + 0.35 + i * 0.12);
    });
    reveal(tl, "#decides", @w(decides));
    tl.fromTo("#decides-wash", { scaleX:0 }, { scaleX:1, duration:0.4, ease:EASE.wipe }, @w(decides));
    // dispatch: fixed assignment -- skin gets ONE dot, joints two, tendons two, other one
    var GO = [["skin", [0], @w(skin)], ["joints", [1, 2], @w(joints)], ["tendons", [3, 4], @w(tendons)], ["other", [5], @w(wherever)]];
    GO.forEach(function (g) {
      var br = document.getElementById("br-" + g[0]);
      g[1].forEach(function (i, k) { pathFollow(tl, dots[i], br, g[2] + k * 0.08, 0.7, "power1.inOut", { ox:q62.x, oy:q62.y, set:false }); });
      tl.fromTo("#d-" + g[0] + "-wash", { scaleX:0 }, { scaleX:1, duration:0.25, ease:EASE.wipe }, g[2] + 0.55);
      // the panel is knocked as the dot lands -- delivery is felt, not labelled
      tl.to("#d-" + g[0], { x:-18, duration:0.18, yoyo:true, repeat:1, ease:EASE.slam }, g[2] + 0.6);
    });
    // was @w(scaffolding)-0.3: the destination dots finish arriving by
    // ~71.9s and "scaffolding." isn't said until 74.2s, leaving ~1.9s of
    // true stillness (measured on the render: t=72.0-74.0s pixel-identical).
    // Starting the camera-home leg on "urgent." fills that gap with the
    // same motion, just earlier, rather than adding a new one.
    tl.to("#world", { scale:1, x:0, y:0, duration:0.8, ease:EASE.camera }, @w(urgent) - 0.3);
    reveal(tl, "#scaff", @w(scaffolding));
    tl.fromTo("#scaff-wash", { scaleX:0 }, { scaleX:1, duration:0.4, ease:EASE.wipe }, @w(scaffolding));
    // "It got A BOX OF spare parts" -> "It got spare parts instead."; the
    // crate payoff now lands on "parts" rather than the removed "box".
    reveal(tl, "#crate", @w(parts));
    tl.fromTo("#crate-wash", { scaleX:0 }, { scaleX:1, duration:0.4, ease:EASE.wipe }, @w(parts));
    tl.fromTo(["#slat-1", "#slat-2", "#slat-3"], { y:-40, opacity:0 }, { y:0, opacity:1, duration:0.3, stagger:0.08, ease:EASE.slam }, @w(parts) + 0.1);
    // "Trials do point to a modest benefit" -- the partial evidence payoff
    // (added in the Phase 1 narration trim) had no visual event of its own,
    // leaving 76.3-78.4s dead (measured: t=76.0-78.5s pixel-identical on the
    // render). The freed-up stomach-p space hosts a small foreshadow of the
    // evidence section this line sets up.
    reveal(tl, "#benefit-teaser", @w(trials));
    tl.fromTo("#benefit-teaser-wash", { scaleX:0 }, { scaleX:1, duration:0.4, ease:EASE.wipe }, @w(trials));
    drawIn(tl, "#benefit-line,#benefit-head", @w(trials) + 0.15, 0.5, 0.1, EASE.wipe);
"""
    MOTION["08-digestion"]["beats"] = [
        {"name": "camera settle", "at": "0.0", "area": 0.5, "dl": 40, "dur": 0.9},
        {"name": "scoop photo crossfade", "at": "0.65", "area": 1.0, "dl": 120, "dur": 0.25},
        {"name": "stomach wash", "at": "@w(breaks)-0.1", "area": 0.07, "dl": 81, "dur": 0.5},
        {"name": "fragments drift", "at": "@w(amino)-0.5", "area": 0.04, "dl": 90, "dur": 1.4},
        {"name": "face card dim", "at": "@w(stomach)-0.2", "area": 0.06, "dl": 84, "dur": 0.4},
        {"name": "face void", "at": "@w(facial)", "area": 0.06, "dl": 103, "dur": 0.3},
        {"name": "struck route leaves", "at": "@we(delivery)+0.15", "area": 0.06, "dl": 90, "dur": 1.1},
    ]
    MOTION["09-dispatch"]["beats"] = [
        {"name": "stomach retract", "at": "@w(but)+0.3", "area": 0.07, "dl": 81, "dur": 0.4},
        {"name": "camera push", "at": "@w(body)", "area": 0.5, "dl": 60, "dur": 0.9},
        {"name": "destinations build", "at": "@w(body)+0.35", "area": 0.13, "dl": 70, "dur": 0.76},
        {"name": "decides wash", "at": "@w(decides)", "area": 0.044, "dl": 94, "dur": 0.4},
        {"name": "skin lands", "at": "@w(skin)+0.55", "area": 0.0275, "dl": 81, "dur": 0.25},
        {"name": "tendons land", "at": "@w(tendons)+0.55", "area": 0.0275, "dl": 81, "dur": 0.25},
        {"name": "camera home", "at": "@w(urgent)-0.3", "area": 0.5, "dl": 60, "dur": 0.8},
        {"name": "crate wash", "at": "@w(parts)", "area": 0.06, "dl": 103, "dur": 0.4},
        {"name": "benefit teaser", "at": "@w(trials)", "area": 0.05, "dl": 81, "dur": 0.4},
    ]
    return body, css, tl


FILES = {"08-digestion": file_08_digestion}
