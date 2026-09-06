#!/usr/bin/env python3
"""File B -- 03-building: units 3 (building), 4 (demolition), 5 (boundary).
Paper ground. THE BUILDING assembles from the slab up; the sun cuts its beams;
the shield draws a boundary. One set of DOM nodes, three phases; the camera
pushes INTO the damage and comes home on "sunscreen"."""
from actors import (HELPERS_JS, BUILDING_JS, BUILDING_CSS, PLATE_CSS, EASE_JS,
                    kt, chip, cite, panel, plate, abs_)
from motion import MOTION

# building placed so its door centre lands at local (404, 599) = canvas (500, 653)
BX, BY = 94, -56


def file_03_building(fspan, fctx):
    css = BUILDING_CSS + PLATE_CSS + """
    .abs { position:absolute; }
    #stageC { position:absolute; left:0; top:0; }
    /* real-skin ground the building grows out of -- BRIEF.md's own imagery
       plan for this scene, never wired in until now. b-shell is a hollow
       stroke (fill:none) and .b-floor/.b-win start at opacity 0, so the
       photo shows clearly through the whole building silhouette until the
       storeys and windows draw in over it: a masked reveal for free, not an
       extra transition to author. */
    /* a quick fade rather than an instant full-opacity pop -- purely
       cosmetic. CONFIRMED (hyperframes check --at-transitions against the
       unmodified master, no photo present) that the text_occluded warning
       at t=13.94-14.03s on this seam is a PRE-EXISTING characteristic of
       this iris transition itself (03-building's own paper ground
       compositing over 02-promise's tail text), not caused by this photo --
       identical with or without it. Out of scope for this redesign. */
    #ground { position:absolute; left:0; top:0; width:100%; height:100%; opacity:0; }
    .ray { stroke:var(--highlighter); stroke-width:7; stroke-linecap:round; opacity:.9; }
    .sun { fill:var(--coral); stroke:var(--paper); stroke-width:5; }
    #rays { opacity:0; }
    .shield-line { fill:none; stroke:var(--aqua); stroke-width:7; }
    .shield-fill { fill:var(--aqua); opacity:0; }
    #sky { background:transparent; }
    #uv { background:var(--mist); padding:var(--s-4) var(--s-5); display:flex; flex-direction:column;
          justify-content:center; gap:8px; }
    #uv .kt { font-size:var(--t-frame); }
    #chip-beams, #preserve { padding:var(--s-4) var(--s-5); display:flex; align-items:center; }
    .cite { position:absolute; opacity:0; }
"""
    body = f"""
      <div class="stage">
       <div class="world" id="world">
        {plate("ground", "assets/images/skin-base.png", filt="filter:saturate(.82) contrast(1.02);",
               scrim="rgba(247,245,240,.30)")}
        {panel("sky", "sun", "<span></span>", abs_(700, 0, 1028, 240))}
        <svg id="stageC" viewBox="0 0 1728 918" width="1728" height="918" aria-hidden="true">
          <g id="bwrap" transform="translate({BX} {BY})"></g>
          <circle class="sun" id="sun" cx="1520" cy="130" r="72"/>
          <g id="rays">
            <line class="ray" x1="1455" y1="165" x2="640" y2="250"/>
            <line class="ray" x1="1470" y1="185" x2="640" y2="400"/>
            <line class="ray" x1="1485" y1="200" x2="650" y2="530"/>
          </g>
          <rect class="shield-fill" id="shield-fill" x="150" y="30" width="510" height="630" rx="30"/>
          <rect class="shield-line" id="shield" x="150" y="30" width="510" height="630" rx="30"/>
        </svg>
        {panel("chip-beams", "aqua", '<p class="p-title">collagen = the beams</p>', abs_(760, 660, 760, 130), "late")}
        {panel("uv", "ink", kt("uv-1", "UV cuts collagen") + kt("uv-2", "works weekends"), abs_(760, 300, 760, 240), "late")}
        {panel("preserve", "aqua", '<p class="p-title">preserve &gt; replace</p>', abs_(760, 790, 900, 110), "late")}
        {cite("cite-uv", "J Invest Dermatol &middot; 1998", False, abs_(170, 700))}
       </div>
      </div>
"""
    tl = EASE_JS + HELPERS_JS + BUILDING_JS + f"""
    // the ground photo drifts almost imperceptibly for the WHOLE file -- it is
    // covered progressively as the building fills in, but stays real motion
    // (not a frozen plate) in whatever margin remains visible throughout.
    pushPlate(tl, "ground", 1.0, 1.05, 0, {fspan.dur:.3f});
    tl.fromTo("#ground", {{ opacity:0 }}, {{ opacity:1, duration:0.5, ease:EASE.arrive }}, 0);
""" + """
    var svg = document.getElementById("stageC"), bwrap = document.getElementById("bwrap");
    drawBuilding(svg, { door:true, into:bwrap });
    // ---- unit 3: the building assembles from the slab up ----------------------
    tl.fromTo("#world", { scale:1.04 }, { scale:1, duration:1.2, ease:EASE.camera }, 0);
    gsap.set(["#b-door", ".b-floor", ".b-win"], { opacity:0 });
    gsap.set(".beam", { strokeDashoffset:640 });
    // frame zero already shows the slab and the shell: the iris opens on a site, not a void
    tl.fromTo("#b-shell", { scaleY:0.94, transformOrigin:"50% 100%" }, { scaleY:1, duration:0.6, ease:EASE.arrive }, @w(building) - 0.2);
    // GROUND UP: floors are laid bottom-first (stagger from:"end" -- DOM order is
    // top-down), each drawn across rather than faded in; the door is hung last
    tl.fromTo(".b-floor", { scaleX:0, transformOrigin:"0% 50%" },
              { scaleX:1, opacity:0.55, duration:0.32, stagger:{ each:0.07, from:"end" }, ease:EASE.arrive }, @w(building) + 0.15);
    tl.fromTo(".b-win", { opacity:0, scale:0.6 }, { opacity:1, scale:1, duration:0.3,
              stagger:{ each:0.03, from:"end" }, ease:EASE.arrive }, @w(building) + 0.45);
    tl.fromTo("#b-door", { scaleY:0, opacity:1, transformOrigin:"50% 100%" },
              { scaleY:1, duration:0.35, ease:EASE.arrive }, @w(building) + 0.9);
    // the collagen: beams DRAW in with the word
    tl.to(".beam", { strokeDashoffset:0, duration:0.55, stagger:{ each:0.10, from:"end" }, ease:EASE.wipe }, @w(structure) - 0.1);
    reveal(tl, "#chip-beams", @w(structure) + 0.2);
    tl.fromTo("#chip-beams-wash", { scaleX:0 }, { scaleX:1, duration:0.4, ease:EASE.wipe }, @w(structure) + 0.2);
    // "the structure INSIDE it": the camera goes in, and comes back out as the
    // building is described holding. The beams drawing between these two words
    // is a stroke-dashoffset reveal -- real motion that a bounding-box tracker
    // cannot see at all, which is why 2.25s here read as frozen.
    tl.to("#world", { scale:1.07, y:18, duration:1.0, ease:EASE.camera }, @w(inside) - 0.15);
    tl.to("#world", { scale:1, y:0, duration:0.6, ease:EASE.camera }, @w(firm));

    // ---- unit 4: the demolition crew --------------------------------------------
    // "As we age, collagen production slows" -- the braces dim, and the agent of
    // the next sentence RISES into frame while it is still being said. A dim on
    // six thin lines is a real pixel change but moves no bounding box, so this
    // stretch read as 2.25s frozen; the sun arriving is both the missing motion
    // and the cause of everything that follows it.
    tl.to(".beam", { opacity:0.6, duration:0.6, ease:EASE.hold }, @w(age));
    tl.fromTo("#sun", { y:-300, scale:1, opacity:1, transformOrigin:"50% 50%" },
              { y:0, duration:1.9, ease:EASE.arrive }, @w(age) + 0.2);
    tl.to("#sun", { scale:1.12, duration:0.28, yoyo:true, repeat:1, ease:EASE.slam }, @w(ultraviolet) - 0.1);
    tl.fromTo("#sky-wash", { scaleX:0 }, { scaleX:1, duration:0.5, ease:EASE.wipe }, @w(ultraviolet) - 0.1);
    tl.to("#rays", { opacity:1, duration:0.1 }, @w(enzymes));
    drawIn(tl, ".ray", @w(enzymes), 0.5, 0.10, EASE.wipe);
    // camera pushes INTO the storeys being cut, then comes home on "sunscreen"
    // Animation item 6 (review): routine camera scale kept near 1.03-1.08.
    // Was 1.18 (x:83, y:23); pan scaled down with it (0.18->0.08 extra zoom)
    // to keep the same framing on the beam being cut.
    tl.to("#world", { scale:1.08, x:37, y:10, duration:1.1, ease:EASE.camera }, @w(cut) - 0.2);
    // each cut: the beam flashes at the cut point, retracts, and a SHARD of it
    // falls away -- UV is a cutting force, not an eraser
    CUT_ORDER.forEach(function (k, i) {
      var at = @w(cut) + i * 0.34;
      tl.to("#beam-" + k, { stroke:"#C97A5C", duration:0.10, ease:EASE.slam }, at);
      tl.to("#beam-" + k, { strokeDashoffset:640, opacity:0.25, duration:0.42, ease:EASE.wipe }, at + 0.04);
      tl.fromTo("#shard-" + k, { opacity:1, y:0, rotation:0 },
                { y:110, rotation:(i % 2 ? 26 : -22), opacity:0, duration:0.6,
                  transformOrigin:"50% 50%", ease:EASE.exit }, at + 0.08);
    });
    tl.to("#bwrap", { skewX:-1.4, y:9, duration:0.6, ease:EASE.swap }, @w(apart) + 0.3);
    reveal(tl, "#uv", @w(demolition) - 0.1);
    tl.fromTo("#uv-wash", { scaleX:0 }, { scaleX:1, duration:0.5, ease:EASE.wipe }, @w(demolition) - 0.1);
    kineticWords(tl, "#uv-1", @w(demolition), 0.08, "slam");
    kineticWords(tl, "#uv-2", @w(weekends), 0.08, "slam");
    tl.to("#sun", { scale:1.12, duration:0.25, yoyo:true, repeat:1, ease:EASE.slam }, @w(weekends));
    tl.fromTo("#cite-uv", { opacity:0, y:16 }, { opacity:1, y:0, duration:0.35, ease:EASE.arrive }, @w(enzymes) + 0.3);

    // ---- unit 5: the boundary ----------------------------------------------------
    tl.to("#world", { scale:1, x:0, y:0, duration:1.0, ease:EASE.camera }, @w(sunscreen) - 0.1);
    drawIn(tl, "#shield", @w(draws) - 0.1, 0.9, 0, EASE.wipe);
    tl.to("#shield-fill", { opacity:0.30, duration:0.7, ease:EASE.wipe }, @w(boundary));
    // the boundary CLOSES around the building as it is named -- 2.2s of
    // identical frames sat here while the shield was merely present
    tl.fromTo(["#shield", "#shield-fill"], { scale:1.09, transformOrigin:"50% 50%" },
              { scale:1, duration:1.1, ease:EASE.arrive }, @w(around) - 0.2);
    // the rays STOP at the boundary; the sun band cools
    gsap.utils.toArray(".ray").forEach(function (r) {
      var L = r.getTotalLength();
      tl.to(r, { strokeDashoffset:L * 0.45, duration:0.6, ease:EASE.swap }, @w(boundary) + 0.1);
    });
    // the sky cools as the boundary is drawn (the only transform in a stretch of
    // stroke-dashoffset reveals, which a bounding-box motion tracker cannot see)
    tl.to("#sky-wash", { scaleX:0, transformOrigin:"100% 50%", duration:0.6, ease:EASE.exit }, @w(draws) - 0.1);
    tl.to("#uv", { opacity:0.35, duration:0.5, ease:EASE.exit }, @w(boundary) + 0.1);
    reveal(tl, "#preserve", @w(preserving));
    tl.fromTo("#preserve-wash", { scaleX:0 }, { scaleX:1, duration:0.45, ease:EASE.wipe }, @w(preserving));
    tl.to("#chip-beams", { opacity:0.35, duration:0.4, ease:EASE.exit }, @w(preserving));
    // PRESERVING holds: the shield takes one pulse as it is named, and the camera
    // pulls back to take in the whole protected building -- the reframe the line
    // asks for, and the only bounding-box motion in a stretch whose other beats
    // are all stroke-dashoffset (invisible to the motion checker, which found
    // 2.32s frozen here before this leg existed).
    tl.to("#shield-fill", { opacity:0.42, duration:0.3, yoyo:true, repeat:1, ease:EASE.slam }, @w(preserving) + 0.1);
    tl.to("#world", { scale:0.955, duration:1.0, ease:EASE.camera }, @w(preserving) + 0.4);
    // REPLACING is tried, and fails: a cut beam starts to redraw and falls back.
    // The tail of the file is this attempt, not an idle drift.
    tl.fromTo("#beam-4a", { strokeDashoffset:640 }, { strokeDashoffset:430, duration:0.45, ease:EASE.arrive }, @w(replacing) - 0.1);
    tl.to("#beam-4a", { strokeDashoffset:640, duration:0.35, ease:EASE.exit }, @w(replacing) + 0.3);
    tl.to("#bwrap", { y:14, duration:0.45, ease:EASE.swap }, @w(replacing) + 0.3);
    tl.to("#world", { scale:1, duration:0.55, ease:EASE.camera }, @w(replacing) + 0.4);
    tl.to("#bwrap", { y:9, duration:0.4, ease:EASE.arrive }, @w(later));
"""
    MOTION["03-building"]["beats"] = [
        {"name": "camera settle",   "at": "0.0",              "area": 0.5,   "dl": 60,  "dur": 1.2},
        {"name": "storeys lay in",  "at": "@w(building)+0.15", "area": 0.17, "dl": 74,  "dur": 0.6},
        {"name": "beams chip wash", "at": "@w(structure)+0.2", "area": 0.048, "dl": 91, "dur": 0.4},
        {"name": "camera goes in",  "at": "@w(inside)-0.15",  "area": 0.5,   "dl": 60,  "dur": 1.0},
        {"name": "firm settle",     "at": "@w(firm)",         "area": 0.5,   "dl": 60,  "dur": 0.6},
    ]
    MOTION["04-demolition"]["beats"] = [
        {"name": "the sun rises", "at": "@w(age)+0.2",         "area": 0.09,  "dl": 96,  "dur": 1.9},
        {"name": "sky warm",     "at": "@w(ultraviolet)-0.1", "area": 0.119, "dl": 77,  "dur": 0.5},
        {"name": "camera push",  "at": "@w(cut)-0.2",         "area": 0.5,   "dl": 60,  "dur": 1.1},
        {"name": "shards fall",  "at": "@w(apart)+0.08",      "area": 0.02,  "dl": 80,  "dur": 0.6},
        {"name": "UV panel ink", "at": "@w(demolition)-0.1",  "area": 0.088, "dl": 215, "dur": 0.5},
    ]
    MOTION["05-boundary"]["beats"] = [
        {"name": "camera home",    "at": "@w(sunscreen)-0.1", "area": 0.5,   "dl": 60, "dur": 1.0},
        {"name": "sky cools",      "at": "@w(draws)-0.1",     "area": 0.119, "dl": 77, "dur": 0.6},
        {"name": "shield fills",   "at": "@w(boundary)",      "area": 0.19,  "dl": 44, "dur": 0.7},
        {"name": "boundary closes", "at": "@w(around)-0.2",   "area": 0.19,  "dl": 60, "dur": 1.1},
        {"name": "preserve wash",  "at": "@w(preserving)",     "area": 0.048, "dl": 91, "dur": 0.45},
        {"name": "camera pulls back", "at": "@w(preserving)+0.4", "area": 0.5, "dl": 60, "dur": 1.0},
        {"name": "building sinks", "at": "@w(replacing)+0.3",  "area": 0.17,  "dl": 60, "dur": 0.45},
        {"name": "camera home",    "at": "@w(replacing)+0.4",  "area": 0.5,   "dl": 60, "dur": 0.55},
    ]
    return body, css, tl


FILES = {"03-building": file_03_building}
