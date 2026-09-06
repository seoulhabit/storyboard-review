#!/usr/bin/env python3
"""File E -- 05-evidence: units 08-trials, 09-caveat, 10-filter, 11-uncertain.
Ink ground; the inversion IS the entrance, so no camera move.

2026-09-05 redesign: SIMPLIFIED per the brief -- one grid, one meter, minimal
labels. The mechanism (tag-then-drop tiles, an illustrative effect-size meter
whose interval crosses the no-effect line) is unchanged; what's REMOVED is
the pair of "keep only: X" filter-pill captions (redundant with the tile tags
and the spoken caveat, and one of the "repeated... secondary labels" the
brief calls out) and the third (wrinkles) outcome, which the new, shorter
narration doesn't name. HONEST BY CONSTRUCTION, unchanged: the only
quantitative object is the pooled n = 23; no survivor count is ever shown.
"""
from actors import HELPERS_JS, TILES_JS, EASE_JS, kt, chip, cite, panel, abs_
from motion import MOTION

CORAL = "#C97A5C"; CORAL_DEEP = "#A85A3C"; CELADON = "#93B896"; CELADON_EDGE = "#C3DCC5"


def file_08_trials(fspan, fctx):
    css = """
    #root { background:var(--ink); }
    .abs { position:absolute; }
    .ev-n { font-family:var(--font-display); font-size:96px; line-height:0.95;
            color:var(--paper); margin:0; min-width:160px; opacity:0; }
    .ev-n-l { font-family:var(--font-mono); font-size:var(--t-label); letter-spacing:var(--tr-mono-wide);
              text-transform:uppercase; color:#93989A; margin:0; opacity:0; }
    #caveat-panel { background:var(--ink-soft); padding:var(--s-4) var(--s-5); display:flex; align-items:center; opacity:0; }
    #caveat { font-size:var(--t-frame); color:var(--paper); }
    .grid { display:grid; gap:14px; grid-template-columns:repeat(8, 1fr); grid-template-rows:repeat(3, 1fr); }
    .tr { border-radius:var(--r-2); background:#4A453E; border:2px solid #6A6459; position:relative;
          display:flex; align-items:center; justify-content:center; }
    .tr-tag { font-family:var(--font-mono); font-size:var(--t-chip); color:var(--ink); opacity:0; }
    .out { font-family:var(--font-mono); font-size:var(--t-chip); letter-spacing:var(--tr-mono);
           color:var(--ink); background:var(--celadon); border-radius:var(--r-pill);
           padding:9px 24px; opacity:0; white-space:nowrap; }
    #res { background:var(--ink-soft); padding:var(--s-4) var(--s-5); }
    .res-v { position:absolute; left:32px; top:24px; margin:0; font-family:var(--font-body);
             font-weight:800; font-size:var(--t-frame); opacity:0; }
    .res-note { position:absolute; left:32px; bottom:14px; margin:0; font-family:var(--font-mono);
                font-size:var(--t-chip); line-height:1.2; opacity:1; }
    .m-axis { stroke:var(--paper); stroke-width:3; opacity:.6; }
    .m-zero { stroke:var(--paper); stroke-width:4; }
    .m-ci { fill:var(--celadon); stroke:var(--paper); stroke-width:2; }
    .m-pt { fill:var(--paper); }
    .m-lab { font-family:var(--font-mono); font-size:32px; fill:var(--paper); letter-spacing:.06em; }
    .cite.on-ink { opacity:0; }
    #stops { padding:60px 60px; background:transparent; }
    #stops .kt { margin-bottom:4px; }
    .q { position:absolute; left:60px; width:900px; }
    .q .kt-word { color:var(--ink); }
    .q-void { position:absolute; left:40px; height:110px; width:940px; background:var(--coral);
              opacity:0; border-radius:var(--r-3); }
"""
    tags = "".join(f'<div class="tr" id="tr-{i}"><span class="tr-tag" id="tag-{i}"></span></div>' for i in range(23))
    body = f"""
      <div class="stage">
       <div class="world" id="world">
        <div class="abs" style="{abs_(0, 0, 600, 150)}">
          <p class="ev-n" id="ev-n">0</p>
          <p class="ev-n-l" id="ev-n-l" style="position:absolute;left:200px;top:40px;">pooled trials</p>
          <p class="ev-n-l" id="tag-note" style="position:absolute;left:0;top:96px;opacity:.85;">tags illustrative</p>
        </div>
        {panel("caveat-panel", "dim", kt("caveat", "small · short · industry funded", "on-ink"), abs_(620, 0, 1108, 150))}
        <div class="grid abs" id="grid" style="{abs_(0, 176, 1040, 464)}">{tags}</div>
        {panel("res", "moss", '''<p class="res-v" id="res-v1">BENEFIT</p>
          <p class="res-v" id="res-v2">NOT SIGNIFICANT</p>
          <p class="res-v" id="res-v3">UNCERTAIN</p>
          <svg viewBox="0 0 620 300" width="620" height="300" style="position:absolute;left:14px;top:70px;" aria-hidden="true">
            <line class="m-axis" x1="60" y1="170" x2="560" y2="170"/>
            <line class="m-zero" id="res-zero" x1="235" y1="110" x2="235" y2="230"/>
            <rect class="m-ci" id="res-ci" x="330" y="160" width="190" height="20" rx="10"/>
            <path class="m-pt" id="res-pt" d="M 425 154 L 441 170 L 425 186 L 409 170 Z"/>
            <text class="m-lab" x="235" y="266" text-anchor="middle">NO EFFECT</text>
            <text class="m-lab" x="500" y="266" text-anchor="middle">BENEFIT →</text>
          </svg>
          <p class="res-note">illustrative scale ·<br>not the paper's values</p>''', abs_(1080, 176, 648, 464))}
        <div class="abs" style="{abs_(0, 664, 520, 60)};display:flex;gap:16px;">
          <div class="out" id="out-1">hydration</div><div class="out" id="out-2">elasticity</div>
        </div>
        {cite("c1", "Nutrients &middot; 2023", True, abs_(0, 830))}
        {panel("stops", "paper", kt("stops-1", "THE EFFECT", "", ) + kt("stops-2", "STOPS", "") + kt("stops-3", "SHOWING UP", "") +
               '<div class="q-void" id="q1-void" style="top:474px;"></div>' + kt("q1", "works?", "q") .replace('class="kt q"', 'class="kt q" style="top:500px;"') +
               '<div class="q-void" id="q2-void" style="top:574px;"></div>' + kt("q2", "fails?", "q").replace('class="kt q"', 'class="kt q" style="top:600px;"'),
               abs_(0, 176, 1040, 742))}
       </div>
      </div>
"""
    body = body.replace('class="kt " id="stops-1"', 'class="kt stops-t" id="stops-1"') \
               .replace('class="kt " id="stops-2"', 'class="kt stops-t" id="stops-2"') \
               .replace('class="kt " id="stops-3"', 'class="kt stops-t" id="stops-3"')
    tl = EASE_JS + HELPERS_JS + TILES_JS + """
    var IND = tiles(TAGS.industry), LOWQ = tiles(TAGS.lowq), SMALL = tiles(TAGS.small), SHORT = tiles(TAGS.short);
    tl.fromTo(".tr", { scaleY:0.62 }, { scaleY:1, duration:0.26, stagger:0.026, ease:EASE.arrive }, 0.0);
    tl.fromTo("#res-wash", { scaleX:0 }, { scaleX:1, duration:0.5, ease:EASE.wipe }, @w(trials) - 0.3);
    gsap.set("#res-ci", { attr:{ x:235, width:0 } });
    gsap.set("#res-pt", { opacity:0 });

    // ---- 08-trials: 23, pooled, a modest benefit shown across two outcomes ----
    tl.fromTo("#ev-n", { opacity:0, y:20 }, { opacity:1, y:0, duration:0.3, ease:EASE.slam }, @w(twenty) - 0.2);
    count(tl, "ev-n", 0, 23, @w(twenty) - 0.1, 0.8, function (n) { return n; });
    tl.fromTo("#ev-n-l", { opacity:0, y:14 }, { opacity:1, y:0, duration:0.35, ease:EASE.arrive }, @w(trials) + 0.2);
    tl.to(".tr", { backgroundColor:"CELADON", borderColor:"CELADON_EDGE", duration:0.45,
                   stagger:0.012, ease:EASE.swap }, @w(pooled));
    tl.fromTo("#tag-note", { opacity:0 }, { opacity:0.85, duration:0.3, ease:EASE.arrive }, @w(together) + 0.3);
    tl.to("#res-ci", { attr:{ x:330, width:190 }, duration:0.75, ease:EASE.arrive }, @w(show) - 0.1);
    tl.fromTo("#res-pt", { opacity:0, scale:0.4, transformOrigin:"50% 50%" },
              { opacity:1, scale:1, duration:0.3, ease:EASE.slam }, @w(show) + 0.35);
    tl.fromTo("#res-v1", { opacity:0, y:16 }, { opacity:1, y:0, duration:0.3, ease:EASE.slam }, @w(gains) + 0.1);
    [["hydration", 0, 12], ["elasticity", 11, 23]].forEach(function (o) {
      var at = o[0] === "hydration" ? @w(hydration) : @w(elasticity);
      tl.fromTo("#out-" + (o[0] === "hydration" ? 1 : 2), { opacity:0, scale:0.8 },
                { opacity:1, scale:1, duration:0.32, ease:EASE.slam }, at);
      for (var i = o[1]; i < o[2]; i++)
        tl.to("#tr-" + i, { scaleY:1.06, duration:0.30, yoyo:true, repeat:1, ease:EASE.swap }, at + (i % 8) * 0.018);
    });
    tl.fromTo("#c1", { opacity:0, y:16 }, { opacity:1, y:0, duration:0.35, ease:EASE.arrive }, @we(elasticity) - 0.3);

    // ---- 09-caveat: the field is examined, not just labelled ------------------
    tl.to("#grid", { y:-10, duration:0.8, ease:EASE.camera }, @w(many) - 0.3);
    tl.to("#caveat-panel", { opacity:1, duration:0.1 }, @w(small) - 0.10);
    tl.fromTo("#caveat-panel-wash", { scaleX:0 }, { scaleX:1, duration:0.5, ease:EASE.wipe }, @w(small) - 0.10);
    kineticWords(tl, "#caveat", @w(small), 0.0, "slam");
    tl.to(".out", { opacity:0.25, duration:0.4, stagger:0.06, ease:EASE.exit }, @w(small));
    tl.to(SMALL, { scale:0.8, duration:0.4, stagger:0.02, ease:EASE.swap }, @w(small));
    tl.to(SHORT, { scaleX:0.7, transformOrigin:"0% 50%", duration:0.4, stagger:0.02, ease:EASE.swap }, @w(short));
    tl.to(IND, { backgroundColor:"CORAL", borderColor:"CORAL", duration:0.45, stagger:0.02, ease:EASE.swap }, @w(industry,1));
    tl.to(IND, { y:16, duration:0.9, stagger:{ each:0.045 }, ease:EASE.hold }, @w(industry,1) + 0.25);
    TAGS.industry.forEach(function (i) { tl.set("#tag-" + i, { innerText:"$", opacity:1 }, @w(industry,1) + 0.2); });
    tl.to("#caveat-panel", { y:-26, scale:0.97, transformOrigin:"50% 0%", opacity:0.55,
                             duration:1.0, ease:EASE.exit }, @we(funded,1) + 0.15);
    tl.to("#grid", { y:0, duration:0.7, ease:EASE.camera }, @uend(09-caveat) - 0.9);

    // ---- 10-filter: exclude industry funding, then low quality -- twice, the
    // meter tells the truth each time -----------------------------------------
    tl.to("#res", { scale:1.04, transformOrigin:"100% 50%", duration:0.9, ease:EASE.camera }, @w(exclude));
    tl.to(IND, { backgroundColor:"CORAL", duration:0.2, ease:EASE.swap }, @w(exclude) + 0.15);
    tl.to(IND, { y:64, opacity:0.10, scale:0.86, duration:0.45, stagger:0.012, ease:EASE.wipe }, @w(exclude) + 0.4);
    tl.to("#res-ci", { attr:{ x:175, width:235 }, duration:1.6, ease:EASE.swap }, @w(exclude) + 0.4);
    tl.to("#res-pt", { x:292 - 425, duration:1.6, ease:EASE.swap }, @w(exclude) + 0.4);
    tl.to("#res-wash", { scaleX:0, transformOrigin:"100% 50%", duration:0.5, ease:EASE.wipe }, @w(longer));
    tl.to("#res-v1", { opacity:0, duration:0.25, ease:EASE.exit }, @w(longer));
    tl.to("#res-v2", { opacity:1, y:0, duration:0.3, ease:EASE.arrive }, @w(longer) + 0.2);
    tl.to("#res-zero", { attr:{ "stroke-width":9 }, stroke:"CORAL", duration:0.5, ease:EASE.swap }, @w(longer) + 0.3);
    // restore, then filter 2: higher quality only
    tl.to(IND, { y:0, opacity:1, scale:1, backgroundColor:"CELADON", duration:0.4, stagger:0.01, ease:EASE.swap }, @w(keep) - 0.30);
    tl.fromTo("#res-wash", { scaleX:0, transformOrigin:"0% 50%" }, { scaleX:1, duration:0.4, ease:EASE.wipe }, @w(keep) - 0.30);
    tl.to("#res-v2", { opacity:0, duration:0.2, ease:EASE.exit }, @w(keep) - 0.3);
    tl.to("#res-v1", { opacity:1, duration:0.2, ease:EASE.arrive }, @w(keep) - 0.1);
    tl.to("#res-ci", { attr:{ x:330, width:190 }, duration:0.4, ease:EASE.swap }, @w(keep) - 0.3);
    tl.to("#res-pt", { x:0, duration:0.4, ease:EASE.swap }, @w(keep) - 0.3);
    tl.set(".tr-tag", { opacity:0 }, @w(keep) - 0.3);
    tl.to(LOWQ, { backgroundColor:"CORAL_DEEP", duration:0.2, ease:EASE.swap }, @w(quality));
    TAGS.lowq.forEach(function (i) { tl.set("#tag-" + i, { innerText:"?", opacity:1 }, @w(quality)); });
    tl.to(LOWQ, { y:64, opacity:0.10, scale:0.86, duration:0.45, stagger:0.012, ease:EASE.wipe }, @w(quality) + 0.25);
    tl.to("#res-ci", { attr:{ x:160, width:225 }, duration:1.4, ease:EASE.swap }, @w(quality) + 0.25);
    tl.to("#res-pt", { x:272 - 425, duration:1.4, ease:EASE.swap }, @w(quality) + 0.25);
    tl.to("#res-wash", { scaleX:0, transformOrigin:"100% 50%", duration:0.4, ease:EASE.wipe }, @w(quality) + 0.5);
    tl.to("#res-v1", { opacity:0, duration:0.2, ease:EASE.exit }, @w(quality) + 0.5);
    tl.to("#res-v2", { opacity:1, y:0, duration:0.3, ease:EASE.arrive }, @w(quality) + 0.7);
    tl.to("#res-v2", { scale:1.06, duration:0.25, yoyo:true, repeat:1, ease:EASE.arrive }, @w(same) + 0.1);
    tl.to("#res", { scale:1, transformOrigin:"100% 50%", duration:0.8, ease:EASE.camera }, @w(same));
    // THE PAYOFF
    tl.fromTo("#stops-wash", { scaleX:0 }, { scaleX:1, duration:0.8, ease:EASE.wipe }, @w(effect) - 0.15);
    tl.to("#caveat-panel", { opacity:0.35, duration:0.5, ease:EASE.exit }, @w(effect) - 0.15);
    kineticWords(tl, "#stops-1", @w(effect), 0.06, "slam");
    kineticWords(tl, "#stops-2", @w(stops), 0.0, "slam");
    tl.to("#world", { scale:1.03, duration:0.18, yoyo:true, repeat:1, ease:EASE.slam }, @w(stops));
    kineticWords(tl, "#stops-3", @w(showing), 0.10, "slam");

    // ---- 11-uncertain: two questions, two refusals -----------------------------
    tl.to("#stops-1 .kt-word, #stops-2 .kt-word, #stops-3 .kt-word",
          { y:-14, duration:1.0, stagger:{ each:0.03 }, ease:EASE.hold }, @we(up) + 0.25);
    kineticWords(tl, "#q1", @w(definitely,1) - 0.4, 0.08, "rise");
    tl.to("#stops-wash", { scaleX:0, transformOrigin:"100% 50%", duration:0.6, ease:EASE.wipe }, @w(definitely,1) - 0.5);
    tl.to(["#stops-1 .kt-word", "#stops-2 .kt-word", "#stops-3 .kt-word", ".q-void", "#q1 .kt-word", "#q2 .kt-word"],
          { y:-24, opacity:0, duration:0.3, stagger:0.01, ease:EASE.exit }, @w(definitely,1) - 0.4);
    tl.to("#q1-void", { opacity:0.85, duration:0.3, ease:EASE.wipe }, @w(can't,1));
    tl.to("#q1 .kt-word", { color:"#F7F5F0", duration:0.2 }, @w(can't,1));
    kineticWords(tl, "#q2", @w(definitely,2) - 0.1, 0.08, "rise");
    tl.to("#q2-void", { opacity:0.85, duration:0.3, ease:EASE.wipe }, @w(can't,2));
    tl.to("#q2 .kt-word", { color:"#F7F5F0", duration:0.2 }, @w(can't,2));
    tl.to("#res-ci", { attr:{ x:150, width:245 }, duration:0.9, ease:EASE.swap }, @w(fails) - 0.3);
    tl.to("#res-v2", { opacity:0, duration:0.25, ease:EASE.exit }, @we(either) - 0.6);
    tl.fromTo("#res-v3", { opacity:0, y:16 }, { opacity:1, y:0, duration:0.3, ease:EASE.arrive }, @we(either) - 0.3);
""".replace("CELADON_EDGE", CELADON_EDGE).replace("CELADON", CELADON).replace("CORAL_DEEP", CORAL_DEEP).replace("CORAL", CORAL)
    MOTION["08-trials"]["beats"] = [
        {"name": "tile field settles", "at": "0.0", "area": 0.30, "dl": 60, "dur": 0.5},
        {"name": "count to 23",   "at": "@w(twenty)-0.2",  "area": 0.05, "dl": 200, "dur": 0.3},
        {"name": "field pools",   "at": "@w(pooled)",      "area": 0.30, "dl": 55,  "dur": 0.45},
        {"name": "interval grows","at": "@w(show)-0.1",    "area": 0.147,"dl": 65,  "dur": 0.75},
        {"name": "hydration band","at": "@w(hydration)",   "area": 0.064,"dl": 99,  "dur": 0.34},
        {"name": "elasticity band","at": "@w(elasticity)", "area": 0.064,"dl": 99,  "dur": 0.34},
    ]
    MOTION["09-caveat"]["beats"] = [
        {"name": "camera examines", "at": "@w(many)-0.3", "area": 0.5, "dl": 60, "dur": 0.8},
        {"name": "caveat dim wash", "at": "@w(small)-0.10", "area": 0.080, "dl": 120, "dur": 0.5},
        {"name": "industry coral", "at": "@w(industry,1)", "area": 0.096, "dl": 72, "dur": 0.45},
        {"name": "flagged tiles sink", "at": "@w(industry,1)+0.25", "area": 0.096, "dl": 60, "dur": 1.44},
        {"name": "camera back out", "at": "@uend(09-caveat)-0.9", "area": 0.5, "dl": 60, "dur": 0.7},
    ]
    MOTION["10-filter"]["beats"] = [
        {"name": "camera lean-in",    "at": "@w(exclude)",       "area": 0.5,   "dl": 60,  "dur": 0.9},
        {"name": "industry falls",    "at": "@w(exclude)+0.4",   "area": 0.096, "dl": 134, "dur": 0.45},
        {"name": "meter retract",     "at": "@w(longer)",        "area": 0.147, "dl": 65,  "dur": 0.5},
        {"name": "industry restore",  "at": "@w(keep)-0.30",     "area": 0.096, "dl": 134, "dur": 0.4},
        {"name": "low-quality falls", "at": "@w(quality)+0.25",  "area": 0.104, "dl": 134, "dur": 0.45},
        {"name": "meter retract 2",   "at": "@w(quality)+0.5",   "area": 0.147, "dl": 65,  "dur": 0.4},
        {"name": "camera home",       "at": "@w(same)",          "area": 0.5,   "dl": 60,  "dur": 0.8},
        {"name": "STOPS paper flood", "at": "@w(effect)-0.15",   "area": 0.46,  "dl": 224, "dur": 0.8},
        {"name": "stops slam 3",      "at": "@w(showing)",       "area": 0.067, "dl": 224, "dur": 0.32},
    ]
    MOTION["11-uncertain"]["beats"] = [
        {"name": "payoff settles", "at": "@we(up)+0.25",        "area": 0.20, "dl": 60,  "dur": 1.0},
        {"name": "q1 void",       "at": "@w(can't,1)",          "area": 0.05, "dl": 103, "dur": 0.3},
        {"name": "q2 void",       "at": "@w(can't,2)",          "area": 0.05, "dl": 103, "dur": 0.3},
        {"name": "interval settles", "at": "@w(fails)-0.3",     "area": 0.147,"dl": 65,  "dur": 0.9},
        {"name": "uncertain label",  "at": "@we(either)-0.3",   "area": 0.075,"dl": 65,  "dur": 0.3},
    ]
    return body, css, tl


FILES = {"05-evidence": file_08_trials}
