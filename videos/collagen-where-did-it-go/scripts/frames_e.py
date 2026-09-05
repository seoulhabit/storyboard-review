#!/usr/bin/env python3
"""File E -- 10-evidence: units 10 (trials), 11 (caveat), 12 (filter), 13
(uncertain). Ink ground; the inversion IS the entrance, so no camera move.

HONEST BY CONSTRUCTION. The only quantitative object is the pooled n = 23,
which the abstract gives. Filtering is shown by TAG (which tiles drop) and by
the RESULT changing (an illustrative effect-size meter whose interval crosses
the no-effect line); no survivor count is ever displayed because the source
gives none. The meter carries a permanent "illustrative" note.
"""
from actors import HELPERS_JS, TILES_JS, EASE_JS, kt, chip, cite, panel, abs_
from motion import MOTION

CORAL = "#C97A5C"; CORAL_DEEP = "#A85A3C"; CELADON = "#93B896"; CELADON_EDGE = "#C3DCC5"
TILE = "#4A453E"; TILE_EDGE = "#6A6459"


def file_10_evidence(fspan, fctx):
    css = """
    #root { background:var(--ink); }
    .abs { position:absolute; }
    .ev-n { font-family:var(--font-display); font-size:96px; line-height:0.95;
            color:var(--paper); margin:0; min-width:160px; opacity:0; }
    .ev-n-l { font-family:var(--font-mono); font-size:var(--t-label); letter-spacing:var(--tr-mono-wide);
              text-transform:uppercase; color:#93989A; margin:0; opacity:0; }   /* 5.64:1 on ink */
    #caveat-panel { background:var(--ink-soft); padding:var(--s-4) var(--s-5); display:flex; align-items:center; opacity:0; }
    #caveat { font-size:var(--t-frame); color:var(--paper); }
    .grid { display:grid; gap:14px; grid-template-columns:repeat(8, 1fr); grid-template-rows:repeat(3, 1fr); }
    .tr { border-radius:var(--r-2); background:#4A453E; border:2px solid #6A6459; position:relative;
          display:flex; align-items:center; justify-content:center; }
    .tr-tag { font-family:var(--font-mono); font-size:var(--t-chip); color:var(--ink); opacity:0; }
    .out { font-family:var(--font-mono); font-size:var(--t-chip); letter-spacing:var(--tr-mono);
           color:var(--ink); background:var(--celadon); border-radius:var(--r-pill);
           padding:9px 24px; opacity:0; white-space:nowrap; }
    .f-pill { font-family:var(--font-mono); font-size:var(--t-chip); letter-spacing:var(--tr-mono);
              color:var(--paper); border:2px solid #93989A; border-radius:var(--r-pill);
              padding:9px 24px; opacity:0; white-space:nowrap; }
    #res { background:var(--ink-soft); padding:var(--s-4) var(--s-5); }
    .res-v { position:absolute; left:32px; top:24px; margin:0; font-family:var(--font-body);
             font-weight:800; font-size:var(--t-frame); opacity:0; }

    .res-note { position:absolute; left:32px; bottom:14px; margin:0; font-family:var(--font-mono);
                font-size:var(--t-chip); line-height:1.2; opacity:.85; }
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
          <p class="ev-n-l" id="ev-n-l" style="position:absolute;left:200px;top:34px;">randomised trials<br>pooled in 2025</p>
          <p class="ev-n-l" id="tag-note" style="position:absolute;left:0;top:132px;opacity:.85;">tag pattern illustrative</p>
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
        <div class="abs" style="{abs_(0, 664, 760, 60)};display:flex;gap:16px;">
          <div class="out" id="out-1">hydration</div><div class="out" id="out-2">elasticity</div><div class="out" id="out-3">wrinkles</div>
        </div>
        <div class="abs" style="{abs_(0, 740, 1728, 60)};display:flex;gap:16px;">
          <div class="f-pill" id="f1">keep only: independent</div><div class="f-pill" id="f2">keep only: higher quality</div>
        </div>
        {cite("c1", "Nutrients &middot; 2023", True, abs_(0, 830))}
        {cite("c2", "Am J Med &middot; 2025", True, "position:absolute;right:0;top:830px;")}
        {panel("stops", "paper", kt("stops-1", "THE EFFECT", "", ) + kt("stops-2", "STOPS", "") + kt("stops-3", "SHOWING UP", "") +
               '<div class="q-void" id="q1-void" style="top:474px;"></div>' + kt("q1", "works?", "q") .replace('class="kt q"', 'class="kt q" style="top:500px;"') +
               '<div class="q-void" id="q2-void" style="top:574px;"></div>' + kt("q2", "fails?", "q").replace('class="kt q"', 'class="kt q" style="top:600px;"'),
               abs_(0, 176, 1040, 742))}
       </div>
      </div>
"""
    # the stops kt blocks need the 132px class
    body = body.replace('class="kt " id="stops-1"', 'class="kt stops-t" id="stops-1"') \
               .replace('class="kt " id="stops-2"', 'class="kt stops-t" id="stops-2"') \
               .replace('class="kt " id="stops-3"', 'class="kt stops-t" id="stops-3"')
    tl = EASE_JS + HELPERS_JS + TILES_JS + """
    // tiles are PRESENT at frame zero (a cut into an empty frame is the one thing a cut must not do)
    var IND = tiles(TAGS.industry), LOWQ = tiles(TAGS.lowq), SMALL = tiles(TAGS.small), SHORT = tiles(TAGS.short);
    tl.fromTo(".tr", { scaleY:0.62 }, { scaleY:1, duration:0.26, stagger:0.026, ease:EASE.arrive }, 0.0);
    // the result panel opens (dim), then the numeral counts to the study's own n
    tl.fromTo("#res-wash", { scaleX:0 }, { scaleX:1, duration:0.5, ease:EASE.wipe }, @w(trials) - 0.5);   // the result panel opens
    // NO count here: this unit's chip is Nutrients 2023 (26 RCTs). The 23 is the
    // 2025 pooled n and lands in unit 12, under its own chip.
    // "Trials DO report modest improvements": the interval grows out of the
    // no-effect line to the benefit side as the sentence says so. The meter is
    // the claim, not a caption arriving after it -- and this is the only
    // bounding-box motion between the panel opening and the outcome pills,
    // which the motion checker found as 2.32s frozen.
    gsap.set("#res-ci", { attr:{ x:235, width:0 } });
    gsap.set("#res-pt", { opacity:0 });
    tl.to("#res-ci", { attr:{ x:330, width:190 }, duration:0.75, ease:EASE.arrive }, @w(improvements) - 0.2);
    // the field acknowledges the claim: a wave across the tiles as "trials do
    // report" is said, before the named outcomes light their own bands
    tl.to(".tr", { scaleY:1.06, duration:0.28, yoyo:true, repeat:1, stagger:{ each:0.02 },
                   ease:EASE.swap }, @w(report) - 0.1);
    tl.fromTo("#res-pt", { opacity:0, scale:0.4, transformOrigin:"50% 50%" },
              { opacity:1, scale:1, duration:0.3, ease:EASE.slam }, @w(improvements) + 0.45);
    // one outcome per named outcome, each lighting the band of trials that measured it
    [["hydration", 0], ["elasticity", 8], ["wrinkles", 16]].forEach(function (o, k) {
      var at = [@w(hydration), @w(elasticity), @w(wrinkles)][k];
      tl.fromTo("#out-" + (k + 1), { opacity:0, scale:0.8 }, { opacity:1, scale:1, duration:0.32, ease:EASE.slam }, at);
      for (var i = o[1]; i < Math.min(o[1] + 8, 23); i++)
        tl.to("#tr-" + i, { backgroundColor:"CELADON", duration:0.34, yoyo:true, repeat:1, ease:EASE.swap }, at + (i % 8) * 0.018);
    });
    tl.fromTo("#c1", { opacity:0, y:16 }, { opacity:1, y:0, duration:0.35, ease:EASE.arrive }, @we(wrinkles) - 0.4);
    // the pooled result: the meter goes moss (a benefit is on the table)
    tl.fromTo("#res-v1", { opacity:0, y:16 }, { opacity:1, y:0, duration:0.3, ease:EASE.slam }, @we(wrinkles) + 0.3);

    // ---- unit 11: the caveat lands on the tiles as it is spoken --------------
    // the field is examined, not just labelled: the caveat pushes the camera in
    // on the trials themselves and it comes back out for the pooled result
    tl.to("#world", { scale:1.07, y:-30, duration:0.8, ease:EASE.camera }, @w(small) - 0.3);
    tl.to("#world", { scale:1, y:0, duration:0.7, ease:EASE.camera }, @w(pooled) - 0.9);
    tl.to("#caveat-panel", { opacity:1, duration:0.1 }, @w(small) - 0.10);
    tl.fromTo("#caveat-panel-wash", { scaleX:0 }, { scaleX:1, duration:0.5, ease:EASE.wipe }, @w(small) - 0.10);
    kineticWords(tl, "#caveat", @w(small), 0.0, "slam");
    tl.to(".out", { opacity:0.25, duration:0.4, stagger:0.06, ease:EASE.exit }, @w(small));
    tl.to(SMALL, { scale:0.8, duration:0.4, stagger:0.02, ease:EASE.swap }, @w(small));
    tl.to(SHORT, { scaleX:0.7, transformOrigin:"0% 50%", duration:0.4, stagger:0.02, ease:EASE.swap }, @w(short));
    tl.to(IND, { backgroundColor:"CORAL", borderColor:"CORAL", duration:0.45, stagger:0.02, ease:EASE.swap }, @w(industry));
    // the flagged tiles sink as they are named -- the field stops being uniform,
    // and 2.8s of identical frames sat between the tag and the pooling
    // the flagged tiles sink AS they are named, one after another, rather than
    // all at once after the sentence: 12 tiles at 45ms apart carry the whole
    // "and industry funded" span, which otherwise held 2.5s of still frames
    tl.to(IND, { y:16, duration:0.9, stagger:{ each:0.045 }, ease:EASE.hold }, @w(industry) + 0.25);
    // "funded." sits for 1.4s before the next sentence starts. The caveat has
    // done its work, so it steps back and hands the frame to the pooling.
    tl.to("#caveat-panel", { y:-26, scale:0.97, transformOrigin:"50% 0%", opacity:0.55,
                             duration:1.0, ease:EASE.exit }, @we(funded) + 0.15);
    TAGS.industry.forEach(function (i) { tl.set("#tag-" + i, { innerText:"$", opacity:1 }, @w(industry) + 0.2); });

    // ---- unit 12: pooled -> filtered, twice; the meter tells the truth ---------
    tl.to(".tr", { backgroundColor:"CELADON", borderColor:"CELADON_EDGE", scale:1, scaleX:1, duration:0.5,
                   stagger:0.012, ease:EASE.swap }, @w(pooled));
    tl.set(".tr-tag", { opacity:0 }, @w(pooled) + 0.2);
    tl.fromTo("#c2", { opacity:0, y:16 }, { opacity:1, y:0, duration:0.35, ease:EASE.arrive }, @w(pooled) - 0.2);
    // the pooled n, under the chip that sources it
    tl.fromTo("#ev-n", { opacity:0, y:20 }, { opacity:1, y:0, duration:0.3, ease:EASE.slam }, @w(three) - 0.3);
    count(tl, "ev-n", 0, 23, @w(three) - 0.2, 1.0);
    tl.fromTo("#ev-n-l", { opacity:0, y:14 }, { opacity:1, y:0, duration:0.35, ease:EASE.arrive }, @w(three) + 0.3);
    // a wave across the field on "randomised trials" -- the tiles are what the
    // numeral is counting, so they answer to it rather than sitting still
    tl.to(".tr", { scaleY:1.08, duration:0.30, yoyo:true, repeat:1,
                   stagger:{ each:0.012 }, ease:EASE.swap }, @w(randomised) + 0.1);
    tl.fromTo("#tag-note", { opacity:0 }, { opacity:0.85, duration:0.3, ease:EASE.arrive }, @w(three) + 0.7);
    // "a benefit": the result panel flashes celadon -- the pooled claim, at panel scale
    tl.to("#res-wash", { backgroundColor:"CELADON", duration:0.3, yoyo:true, repeat:1, ease:EASE.swap }, @w(benefit));
    // every tile rises back to level as they are pooled: "all together" is the
    // field becoming one dataset again
    tl.to(".tr", { y:0, duration:0.9, stagger:{ each:0.015 }, ease:EASE.arrive }, @w(together) - 0.3);
    tl.to("#res", { scale:1.03, duration:0.25, yoyo:true, repeat:1, ease:EASE.slam }, @w(benefit));
    // filter 1: independent only
    // lean in for the filter: the trial field is what is being examined
    tl.to("#world", { scale:1.08, duration:0.9, ease:EASE.camera }, @w(keep,1));
    tl.fromTo("#f1", { opacity:0, x:40 }, { opacity:1, x:0, duration:0.3, ease:EASE.arrive }, @w(keep,1));
    tl.to(IND, { backgroundColor:"CORAL", duration:0.2, ease:EASE.swap }, @w(without));
    TAGS.industry.forEach(function (i) { tl.set("#tag-" + i, { innerText:"$", opacity:1 }, @w(without)); });
    // the tiles FALL OUT of the field, and the result starts moving with them --
    // the meter is not a caption arriving after the fact
    tl.to(IND, { y:64, opacity:0.10, scale:0.86, duration:0.45, stagger:0.012, ease:EASE.wipe }, @w(without) + 0.25);
    tl.to("#res-ci", { attr:{ x:175, width:235 }, duration:1.8, ease:EASE.swap }, @w(without) + 0.25);
    tl.to("#res-pt", { x:292 - 425, duration:1.8, ease:EASE.swap }, @w(without) + 0.25);
    tl.to("#res-wash", { scaleX:0, transformOrigin:"100% 50%", duration:0.5, ease:EASE.wipe }, @w(longer));
    tl.to("#res-v1", { opacity:0, duration:0.25, ease:EASE.exit }, @w(longer));
    tl.to("#res-v2", { opacity:1, y:0, duration:0.3, ease:EASE.slam }, @w(longer) + 0.2);
    tl.to("#res-zero", { attr:{ "stroke-width":9 }, stroke:"CORAL", duration:0.5, ease:EASE.swap }, @w(longer) + 0.3);
    // restore, then filter 2: higher quality only
    tl.to(IND, { y:0, opacity:1, scale:1, backgroundColor:"CELADON", duration:0.4, stagger:0.01, ease:EASE.swap }, @w(keep,2) - 0.30);
    tl.fromTo("#res-wash", { scaleX:0, transformOrigin:"0% 50%" }, { scaleX:1, duration:0.4, ease:EASE.wipe }, @w(keep,2) - 0.30);
    tl.to("#res-v2", { opacity:0, duration:0.2, ease:EASE.exit }, @w(keep,2) - 0.3);
    tl.to("#res-v1", { opacity:1, duration:0.2, ease:EASE.arrive }, @w(keep,2) - 0.1);
    tl.to("#res-ci", { attr:{ x:330, width:190 }, duration:0.4, ease:EASE.swap }, @w(keep,2) - 0.3);
    tl.to("#res-pt", { x:0, duration:0.4, ease:EASE.swap }, @w(keep,2) - 0.3);
    tl.set(".tr-tag", { opacity:0 }, @w(keep,2) - 0.3);
    tl.to("#f1", { opacity:0.35, duration:0.3, ease:EASE.exit }, @w(keep,2));
    tl.fromTo("#f2", { opacity:0, x:40 }, { opacity:1, x:0, duration:0.3, ease:EASE.arrive }, @w(keep,2));
    tl.to(LOWQ, { backgroundColor:"CORAL_DEEP", duration:0.2, ease:EASE.swap }, @w(quality));
    TAGS.lowq.forEach(function (i) { tl.set("#tag-" + i, { innerText:"?", opacity:1 }, @w(quality)); });
    tl.to(LOWQ, { y:64, opacity:0.10, scale:0.86, duration:0.45, stagger:0.012, ease:EASE.wipe }, @w(quality) + 0.25);
    tl.to("#res-ci", { attr:{ x:160, width:225 }, duration:1.4, ease:EASE.swap }, @w(quality) + 0.25);
    tl.to("#res-pt", { x:272 - 425, duration:1.4, ease:EASE.swap }, @w(quality) + 0.25);
    tl.to("#res-wash", { scaleX:0, transformOrigin:"100% 50%", duration:0.4, ease:EASE.wipe }, @w(quality) + 0.5);
    tl.to("#res-v1", { opacity:0, duration:0.2, ease:EASE.exit }, @w(quality) + 0.5);
    tl.to("#res-v2", { opacity:1, y:0, duration:0.3, ease:EASE.slam }, @w(quality) + 0.7);
    tl.to("#res-v2", { scale:1.06, duration:0.25, yoyo:true, repeat:1, ease:EASE.slam }, @w(same) + 0.1);
    // home before the flood: the biggest beat lands on a settled frame
    tl.to("#world", { scale:1, duration:0.8, ease:EASE.camera }, @w(same));
    // THE PAYOFF: the biggest beat in the piece -- a paper flood, then three slams
    tl.to(["#f1", "#f2"], { opacity:0, duration:0.3, ease:EASE.exit }, @w(effect) - 0.35);
    tl.fromTo("#stops-wash", { scaleX:0 }, { scaleX:1, duration:0.8, ease:EASE.wipe }, @w(effect) - 0.15);
    tl.to("#caveat-panel", { opacity:0.35, duration:0.5, ease:EASE.exit }, @w(effect) - 0.15);
    kineticWords(tl, "#stops-1", @w(effect), 0.06, "slam");
    kineticWords(tl, "#stops-2", @w(stops), 0.0, "slam");
    tl.to("#world", { scale:1.03, duration:0.18, yoyo:true, repeat:1, ease:EASE.slam }, @w(stops));
    kineticWords(tl, "#stops-3", @w(showing), 0.10, "slam");

    // ---- unit 13: two questions, two refusals, one honest word ----------------
    // the payoff type settles while it is held, so the frame is not identical
    // for the 2.3s between the last slam and the first question
    tl.to("#stops-1 .kt-word, #stops-2 .kt-word, #stops-3 .kt-word",
          { y:-14, duration:1.0, stagger:{ each:0.03 }, ease:EASE.hold }, @we(up) + 0.25);
    kineticWords(tl, "#q1", @w(definitely,1) - 0.1, 0.08, "rise");
    // "the independent evidence" is literally what is left standing: the paper
    // flood retracts to the survivor field with the low-quality tiles still down
    tl.to("#stops-wash", { scaleX:0, transformOrigin:"100% 50%", duration:0.6, ease:EASE.wipe }, @w(independent) - 0.2);
    tl.to(["#stops-1 .kt-word", "#stops-2 .kt-word", "#stops-3 .kt-word", ".q-void", "#q1 .kt-word", "#q2 .kt-word"],
          { y:-24, opacity:0, duration:0.3, stagger:0.01, ease:EASE.exit }, @w(independent) - 0.1);
    tl.to("#q1-void", { opacity:0.85, duration:0.3, ease:EASE.wipe }, @w(cannot,1));
    tl.to("#q1 .kt-word", { color:"#F7F5F0", duration:0.2 }, @w(cannot,1));
    kineticWords(tl, "#q2", @w(definitely,2) - 0.1, 0.08, "rise");
    tl.to("#q2-void", { opacity:0.85, duration:0.3, ease:EASE.wipe }, @w(cannot,2));
    tl.to("#q2 .kt-word", { color:"#F7F5F0", duration:0.2 }, @w(cannot,2));
    // The act's last word is UNCERTAIN, and it used to land 0.2s before the
    // invert took the frame. The interval widens under "the independent
    // evidence", so the meter has already told the truth by the time the word
    // arrives -- and the word gets the whole tail of the unit rather than a
    // sliver of it.
    tl.to("#res-ci", { attr:{ x:150, width:245 }, duration:0.9, ease:EASE.swap }, @w(independent));
    tl.to("#res-v2", { opacity:0, duration:0.25, ease:EASE.exit }, @w(uncertain) - 0.4);
    tl.fromTo("#res-v3", { opacity:0, y:16 }, { opacity:1, y:0, duration:0.3, ease:EASE.slam }, @w(uncertain) - 0.1);
""".replace("CELADON_EDGE", CELADON_EDGE).replace("CELADON", CELADON).replace("CORAL_DEEP", CORAL_DEEP).replace("CORAL", CORAL)
    MOTION["10-trials"]["beats"] = [
        {"name": "tile field settles", "at": "0.0", "area": 0.30, "dl": 60, "dur": 0.5},
        {"name": "result panel opens", "at": "@w(trials)-0.5", "area": 0.147, "dl": 65, "dur": 0.5},
        {"name": "interval grows", "at": "@w(improvements)-0.2", "area": 0.147, "dl": 65, "dur": 0.75},
        {"name": "tile wave", "at": "@w(report)-0.1", "area": 0.30, "dl": 40, "dur": 0.56},
        {"name": "hydration band", "at": "@w(hydration)", "area": 0.064, "dl": 99, "dur": 0.34},
        {"name": "elasticity band", "at": "@w(elasticity)", "area": 0.064, "dl": 99, "dur": 0.34},
        {"name": "wrinkles band", "at": "@w(wrinkles)", "area": 0.064, "dl": 99, "dur": 0.34},
    ]
    MOTION["11-caveat"]["beats"] = [
        {"name": "camera examines", "at": "@w(small)-0.3", "area": 0.5, "dl": 60, "dur": 0.8},
        {"name": "caveat dim wash", "at": "@w(small)-0.10", "area": 0.080, "dl": 120, "dur": 0.5},
        {"name": "camera back out", "at": "@w(pooled)-0.9", "area": 0.5, "dl": 60, "dur": 0.7},
        {"name": "industry coral", "at": "@w(industry)", "area": 0.096, "dl": 72, "dur": 0.45},
        {"name": "flagged tiles sink", "at": "@w(industry)+0.25", "area": 0.096, "dl": 60, "dur": 1.44},
        {"name": "caveat steps back", "at": "@we(funded)+0.15", "area": 0.080, "dl": 70, "dur": 1.0},
    ]
    MOTION["12-filter"]["beats"] = [
        {"name": "pooled celadon",    "at": "@w(pooled)",        "area": 0.18,  "dl": 99,  "dur": 0.5},
        {"name": "count to 23",       "at": "@w(three)-0.3",     "area": 0.05,  "dl": 200, "dur": 0.3},
        {"name": "field answers the count", "at": "@w(randomised)+0.1", "area": 0.30, "dl": 40, "dur": 0.60},
        {"name": "field levels",      "at": "@w(together)-0.3",  "area": 0.18,  "dl": 55,  "dur": 0.9},
        {"name": "benefit flash",     "at": "@w(benefit)",       "area": 0.147, "dl": 73,  "dur": 0.3},
        {"name": "camera lean-in",    "at": "@w(keep,1)",        "area": 0.5,   "dl": 60,  "dur": 0.9},
        {"name": "industry falls",    "at": "@w(without)+0.25",  "area": 0.096, "dl": 134, "dur": 0.45},
        {"name": "meter retract",     "at": "@w(longer)",        "area": 0.147, "dl": 65,  "dur": 0.5},
        {"name": "industry restore",  "at": "@w(keep,2)-0.30",   "area": 0.096, "dl": 134, "dur": 0.4},
        {"name": "low-quality falls", "at": "@w(quality)+0.25",  "area": 0.104, "dl": 134, "dur": 0.45},
        {"name": "meter retract 2",   "at": "@w(quality)+0.5",   "area": 0.147, "dl": 65,  "dur": 0.4},
        {"name": "camera home",       "at": "@w(same)",          "area": 0.5,   "dl": 60,  "dur": 0.8},
        {"name": "STOPS paper flood", "at": "@w(effect)-0.15",   "area": 0.46,  "dl": 224, "dur": 0.8},
        {"name": "stops slam 3",      "at": "@w(showing)",       "area": 0.067, "dl": 224, "dur": 0.32},
    ]
    MOTION["13-uncertain"]["beats"] = [
        {"name": "payoff settles", "at": "@we(up)+0.25",       "area": 0.20, "dl": 60,  "dur": 1.0},
        {"name": "q1 void",       "at": "@w(cannot,1)",        "area": 0.05, "dl": 103, "dur": 0.3},
        {"name": "q2 void",       "at": "@w(cannot,2)",        "area": 0.05, "dl": 103, "dur": 0.3},
        {"name": "flood retract", "at": "@w(independent)-0.2", "area": 0.46, "dl": 224, "dur": 0.6},
        {"name": "interval widens", "at": "@w(independent)", "area": 0.147, "dl": 65, "dur": 0.9},
    ]
    return body, css, tl


FILES = {"10-evidence": file_10_evidence}
