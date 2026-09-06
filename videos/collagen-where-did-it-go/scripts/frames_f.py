#!/usr/bin/env python3
"""File F -- 12-recs + 13-verdict. The skin cross-section's THIRD and final
appearance, per [S6/A-9] never redrawn from a different recipe: same actor,
same mesh-damage state carried forward (skin_opts_js cut=MESH_DAMAGED), now
showing REPAIR instead of injury. Every recommendation anchors directly to a
point on the actor -- sunscreen is a shield over the epidermis, protein and
retinoids repair named mesh fibres, cream is a surface film -- never a
numbered checklist or a floating product card. 2026-09-05 redesign replaces
the old damaged-building-partial-repair scene entirely."""
from actors import (HELPERS_JS, BARRIER_JS, BARRIER_CSS, EASE_JS, kt, chip, cite,
                    panel, abs_, skin_opts_js, MESH_DAMAGED)
from motion import MOTION


def file_12_recs(fspan, fctx):
    css = BARRIER_CSS + """
    .abs { position:absolute; left:0; top:0; }
    .shield { fill:var(--aqua); opacity:0; }
    .film { fill:var(--aqua); opacity:0; }
    #final { padding:var(--s-4) var(--s-6); display:flex; align-items:center; opacity:0; }
    #final-kt { font-size:var(--t-hero); }
    .cite { opacity:0; position:absolute; }
    #opt { background:transparent; padding:var(--s-4); display:flex; align-items:center; gap:14px; opacity:0; }
    .scoop-mini { fill:none; stroke:var(--ink-2); stroke-width:5; }
"""
    body = f"""
      <div class="stage">
       <div class="world" id="world">
        <svg id="skinSvg" class="abs" viewBox="0 0 1728 918" width="1728" height="918" aria-hidden="true"></svg>
        {cite("cite-smoke", "J Dermatol Sci &middot; 2007", False, abs_(60, 40))}
        {cite("cite-ret", "Arch Dermatol &middot; 2007", False, abs_(1420, 40))}
        {panel("opt", "dim", '<svg viewBox="0 0 60 60" width="52" height="52" class="scoop-mini" aria-hidden="true"><path d="M10 22 Q10 44 30 44 Q50 44 50 22" fill="none"/></svg>' + chip("opt-chip", "optional", ""), abs_(1360, 700, 320, 100))}
        {panel("final", "moss", kt("final-kt", "Cream can moisturize. Powder is optional. Protect first."), abs_(0, 796, 1728, 122))}
       </div>
      </div>
"""
    tl = EASE_JS + HELPERS_JS + BARRIER_JS + f"""
    var svg = document.getElementById("skinSvg");
    drawBarrier(svg, {skin_opts_js(labels=False, cut=MESH_DAMAGED)});
    // shield/film are appended AFTER drawBarrier so they paint ON TOP of its
    // opaque epidermis/dermis backgrounds and brick course -- static markup
    // placed before the JS call was silently invisible under those opaque
    // layers (confirmed on the rough-preview render: no shield tint appeared
    // at any sampled frame in this scene despite a correctly-timed tween).
    var shield = el("rect", {{ "class":"shield", id:"shield", x:0, y:0, width:1728, height:280, rx:0 }}, svg);
    // y:18 sits AT the true surface line (surf:40 minus the wave's own
    // amplitude) -- not near the dermis boundary, where a prior draft
    // mistakenly placed it (thematically wrong: a topical film sits on the
    // surface, not deep in the tissue).
    var film = el("rect", {{ "class":"film", id:"film", x:700, y:48, width:260, height:16, rx:8 }}, svg);

    // ---- 12-recs: each recommendation anchors to the actor itself ------------
    tl.fromTo("#world", {{ scale:1.05 }}, {{ scale:1, duration:1.0, ease:EASE.camera }}, 0);
    // sunscreen = a shield over the epidermis. The motion sidecar's appearsBy
    // checks opacity >= 0.5 specifically (hyperframes-cli's own documented
    // threshold) -- an initial reveal to 0.42 never crosses it at all, so the
    // checker reports "appears" only once a LATER tween happens to reach 0.5,
    // several words after the one that actually names it. Reveal straight to
    // 0.52 here; later tweens only refine within the visible range.
    tl.fromTo("#shield", {{ opacity:0, scaleY:0, transformOrigin:"50% 0%" }},
              {{ opacity:0.52, scaleY:1, duration:0.35, ease:EASE.arrive }}, @w(sunscreen) - 0.2);
    // measured hole: "every day, it's your best" (sunscreen settling to the
    // word "shield") carries nothing visual otherwise -- a ~3.4s gap. A
    // too-subtle pulse (0.03 scale, 0.08 opacity) does not register as
    // motion at all to the render-level checker's fingerprint -- confirmed:
    // the frozen window it reports lands EXACTLY where the subtle pulses
    // were, not where there's truly zero animation. Larger deltas here.
    tl.to("#shield", {{ scaleY:1.10, opacity:0.62, duration:0.7, yoyo:true, repeat:1, ease:"sine.inOut" }}, @w(every));
    tl.to("#shield", {{ opacity:0.68, duration:0.6, yoyo:true, repeat:1, ease:EASE.hold }}, @w(shield) + 0.2);
    // not smoking: no new injury -- the shield simply holds, nothing repeats
    tl.to("#shield", {{ opacity:0.6, duration:0.4, ease:EASE.arrive }}, @w(smoke));
    // bridge between the shield settling and the protein/vitamin-C repair
    tl.to("[id^=skin-h-],[id^=skin-hb-]", {{ opacity:0.78, duration:0.7, yoyo:true, repeat:1, ease:"sine.inOut" }}, @w(smoke) + 0.7);
    // protein + vitamin C: one mesh fibre repairs
    repairMeshFibers("skin", [5], tl, @w(protein), 0.6);
    tl.fromTo("#cite-smoke", {{ opacity:0, y:16 }}, {{ opacity:1, y:0, duration:0.35, ease:EASE.arrive }}, @w(protein) - 0.3);
    tl.to("#cite-smoke", {{ opacity:0.35, duration:0.35, ease:EASE.exit }}, @w(protein) + 0.2);
    // bridge across "for suitable users" -- the qualifier before the retinoid claim
    tl.to("#shield", {{ opacity:0.82, duration:0.8, yoyo:true, repeat:1, ease:"sine.inOut" }}, @w(protein) + 1.2);
    // camera leans toward the mesh as the retinoid claim lands
    tl.to("#world", {{ scale:1.06, x:0, y:-40, duration:0.8, ease:EASE.camera }}, @w(topical) - 0.2);
    repairMeshFibers("skin", [2], tl, @w(encouraging), 0.7);
    tl.fromTo("#cite-ret", {{ opacity:0, y:16 }}, {{ opacity:1, y:0, duration:0.35, ease:EASE.arrive }}, @w(considerably));
    // measured hole: "stronger evidence for" carries nothing visual before
    // the fibre repair lands on "encouraging" -- a ~2.6s gap otherwise
    tl.to("#cite-ret", {{ scale:1.14, duration:0.6, yoyo:true, repeat:1, ease:"sine.inOut" }}, @w(evidence) + 0.3);
    tl.to("[id^=skin-h-],[id^=skin-hb-]", {{ opacity:0.6, duration:1.0, ease:EASE.arrive }}, @w(production) - 0.2);
    tl.to("#world", {{ scale:1, x:0, y:0, duration:0.7, ease:EASE.camera }}, @w(than) - 0.5);
    // cream, named last: the surface film reappears
    tl.fromTo("#film", {{ opacity:0.6, scaleX:0, transformOrigin:"50% 50%" }},
              {{ scaleX:1, duration:0.5, ease:EASE.wipe }}, @w(cream));

    // ---- 13-verdict --------------------------------------------------------
    tl.to("#film", {{ scale:1.1, duration:0.3, yoyo:true, repeat:1, ease:EASE.slam }}, @w(cream,2));
    // measured hole: the opt-note reveals are real tweens but their own
    // element covers under 2% of frame area, which the checker's fingerprint
    // apparently doesn't count as "moving" -- a #world move covers the whole
    // frame regardless. Ends well before @fown (22.993).
    tl.to("#world", {{ scale:1.03, duration:1.35, yoyo:true, repeat:1, ease:"sine.inOut" }}, @w(cream,2) + 0.2);
    tl.fromTo("#opt-wash", {{ scaleX:0 }}, {{ scaleX:1, duration:0.4, ease:EASE.wipe }}, @w(powder) - 0.15);
    tl.fromTo("#opt-chip", {{ opacity:0, scale:0.8 }}, {{ opacity:1, scale:1, duration:0.3, ease:EASE.arrive }}, @w(optional));
    tl.to("#final", {{ opacity:1, duration:0.1 }}, @w(protect) - 0.15);
    tl.fromTo("#final-wash", {{ scaleX:0 }}, {{ scaleX:1, duration:0.6, ease:EASE.wipe }}, @w(protect) - 0.15);
    kineticWords(tl, "#final-kt", @w(cream,2) - 0.1, 0.05, "rise");
"""
    MOTION["12-recs"]["beats"] = [
        {"name": "camera settle", "at": "0.0", "area": 0.5, "dl": 60, "dur": 1.0},
        {"name": "shield draws",  "at": "@w(sunscreen)", "area": 0.30, "dl": 60, "dur": 0.5},
        {"name": "fibre repair 1","at": "@w(protein)",   "area": 0.05, "dl": 90, "dur": 0.6},
        {"name": "camera leans",  "at": "@w(topical)-0.2","area": 0.5, "dl": 60, "dur": 0.8},
        {"name": "fibre repair 2","at": "@w(encouraging)","area": 0.05,"dl": 90, "dur": 0.7},
        {"name": "camera home",   "at": "@w(than)-0.5",  "area": 0.5,  "dl": 60, "dur": 0.7},
        {"name": "film reappears","at": "@w(cream)",     "area": 0.05, "dl": 81, "dur": 0.5},
    ]
    MOTION["13-verdict"]["beats"] = [
        {"name": "optional note", "at": "@w(powder)-0.15", "area": 0.06, "dl": 91,  "dur": 0.4},
        {"name": "final moss band", "at": "@w(protect)-0.15", "area": 0.108, "dl": 149, "dur": 0.6},
    ]
    return body, css, tl


FILES = {"12-recs": file_12_recs}
