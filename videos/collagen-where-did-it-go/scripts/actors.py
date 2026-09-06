#!/usr/bin/env python3
"""The continuous actors, as deterministic JS builders (Python strings), plus
the Python-side helpers every file function uses to emit HTML.

Every builder takes an <svg> whose viewBox equals its px size (1:1 user
units), so GSAP x/y on SVG children and getPointAtLength share one coordinate
space. No Math.random anywhere: a re-seek must reproduce the frame exactly.

COORDINATES. Inside .world the safe box is 1728x918 at (0,0) ("local").
Canvas px = local + (96, 54). motion.MOTION["iris_at"] is in canvas px.
"""

SAFE_W, SAFE_H = 1728, 918
SAFE_DX, SAFE_DY = 96, 54


def canvas(x, y):
    return (x + SAFE_DX, y + SAFE_DY)


# ---------------------------------------------------------------- JS helpers

HELPERS_JS = r"""
    var NS = "http://www.w3.org/2000/svg";
    function el(t, a, parent) { var n = document.createElementNS(NS, t);
      for (var k in a) n.setAttribute(k, a[k]); if (parent) parent.appendChild(n); return n; }
    function txt(parent, x, y, s, cls, anchor) {
      var t = el("text", { x:x, y:y, "class":cls || "", "text-anchor":anchor || "start" }, parent);
      t.textContent = s; return t; }

    // pathFollow: move `node` along `pathEl` between progress `from` and `to`
    // WITHOUT MotionPathPlugin and WITHOUT onUpdate. The path is SAMPLED at
    // build time into a chain of short linear x/y (and rotation) tweens, so the
    // pose at any timeline time is a plain property tween -- a pure function of
    // time under any seek. (An onUpdate proxy was tried first: the runtime seeks
    // with callbacks suppressed, and frame zero rendered the molecule at the END
    // of its run.) Convention: the node is DRAWN at the path's start point, so
    // the translation is (q - p0). Returns the end pose for the caller's next
    // fromTo. Easing is applied to the sampled progress, so the motion keeps its
    // curve while every sub-tween stays linear.
    function pathFollow(tl, node, pathEl, at, dur, ease, o) {
      o = o || {}; var from = o.from == null ? 0 : o.from, to = o.to == null ? 1 : o.to;
      var L = pathEl.getTotalLength(), p0 = pathEl.getPointAtLength(0);
      var ox = o.ox == null ? p0.x : o.ox, oy = o.oy == null ? p0.y : o.oy;
      var N = o.samples || Math.max(12, Math.round(dur * 30)), ef = gsap.parseEase(ease || "none");
      function pose(p) {
        var q = pathEl.getPointAtLength(p * L), r = { x:q.x - ox, y:q.y - oy };
        if (o.rotate) { var a = pathEl.getPointAtLength(Math.min(L, p * L + 4)),
                            b = pathEl.getPointAtLength(Math.max(0, p * L - 4));
                        r.rotation = Math.atan2(a.y - b.y, a.x - b.x) * 57.2958; }
        return r;
      }
      var start = pose(from);
      // frame zero, and any cold seek before `at`. A node that is walked by TWO
      // pathFollows (tract, then a branch) must pass { set:false } on the second:
      // two zero-duration sets at t=0 render in insertion order and the LATER
      // one wins every frame before `at` (measured: dispatch dots drawn at the
      // tract exit before "absorbed").
      if (o.set !== false) tl.set(node, start, 0);
      var prev = start;
      for (var i = 1; i <= N; i++) {
        var p = from + (to - from) * ef(i / N), nxt = pose(p);
        var t0 = at + dur * (i - 1) / N;
        tl.fromTo(node, prev, Object.assign({ duration: dur / N, ease: "none" }, nxt), t0);
        prev = nxt;
      }
      return prev;
    }
    // stroke draw-in; dasharray set from the measured length
    function drawIn(tl, sel, at, dur, stagger, ease) {
      gsap.utils.toArray(sel).forEach(function (p, i) {
        var L = p.getTotalLength(); p.style.strokeDasharray = L; p.style.strokeDashoffset = L;
        tl.fromTo(p, { strokeDashoffset: L }, { strokeDashoffset: 0, duration: dur,
                  ease: ease || "power4.inOut" }, at + i * (stagger || 0));
      });
    }
    // numeral count -- ease none, or it lies. A PROPERTY tween on innerText
    // with a modifier (no onUpdate), so any seek renders the right numeral.
    function count(tl, id, from, to, at, dur, fmt) {
      var node = document.getElementById(id);
      var f = fmt || function (n) { return n.toLocaleString("en-GB"); };
      node.textContent = f(from);
      tl.fromTo(node, { innerText: from }, { innerText: to, duration: dur, ease: "none",
                modifiers: { innerText: function (v) { return f(Math.round(parseFloat(v))); } } }, at);
    }
    // a panel that must not leak its copy before its wash: CSS .late holds it at
    // opacity 0; reveal() switches it on right as the wash begins
    function reveal(tl, sel, at) { tl.to(sel, { opacity:1, duration:0.1 }, at); }
    // kinetic words: "rise" (a claim settling) or "slam" (a payoff landing)
    function kineticWords(tl, sel, at, step, mode) {
      var w = gsap.utils.toArray(sel + " .kt-word");
      if (mode === "slam") tl.fromTo(w, { opacity:0, scale:1.6 }, { opacity:1, scale:1,
            duration:0.32, stagger:step, ease:"back.out(1.7)" }, at);
      else tl.fromTo(w, { opacity:0, y:18 }, { opacity:1, y:0, duration:0.34,
            stagger:step, ease:"power2.out" }, at);
    }
    // restrained Ken Burns for a plate()'s own .world layer -- linear, never
    // the file's entrance eases, so a still photo reads as a slow drift, not
    // an arrival. 1.03-1.08 per the brief; keep dur >= ~4s so the per-frame
    // step stays under check-motion-gaps' per-cell ceiling while still
    // clearing its floor (measured against PSNR_FROZEN_DB=55 and eps=0.35).
    function pushPlate(tl, id, fromS, toS, at, dur) {
      tl.fromTo("#" + id + "-world", { scale:fromS }, { scale:toS, duration:dur, ease:"none" }, at);
    }
"""

# ---------------------------------------------------------------- MOL

HELIX_JS = r"""
    // The collagen molecule: three sine ribbons 120deg apart, drawn as `segs`
    // groups (#id-seg-i) so digestion can tween segments apart without a
    // second drawing. o = { id, x, y, w, h, turns, strokeW, segs, cls }
    function drawHelix(svg, o) {
      var STEP = 8, N = Math.round(o.w / STEP), segs = o.segs || 1, turns = o.turns || 1.5;
      var g = el("g", { id:o.id, "class":"mol" }, svg);
      for (var s = 0; s < segs; s++) {
        var sg = el("g", { id:o.id + "-seg-" + s }, g);
        var i0 = Math.floor(N * s / segs), i1 = Math.min(N, Math.floor(N * (s + 1) / segs) + 1);
        for (var k = 0; k < 3; k++) {
          var d = "", ph = k * 2.0944;
          for (var i = i0; i <= i1; i++) {
            var x = i * STEP;
            d += (i === i0 ? "M" : "L") + (o.x + x).toFixed(1) + " " +
                 (o.y + Math.sin(x / o.w * turns * 6.2832 + ph) * o.h / 2).toFixed(2) + " ";
          }
          var p = el("path", { d:d, "class":o.cls || "mol-body", opacity:(0.45 + k * 0.27).toFixed(2) }, sg);
          p.style.strokeWidth = (o.strokeW || 14) + "px";
        }
      }
      return g;
    }
"""

HELIX_CSS = """
    .mol-body { fill:none; stroke:var(--coral); stroke-linecap:round; }
"""

# ---------------------------------------------------------------- BLDG

BUILDING_JS = r"""
    // The building: 5 storeys, an X-brace pair per storey (the collagen),
    // stable ids so a later phase MOVES a beam instead of redrawing it.
    // o.door adds the ground-floor door; o.into = parent group.
    function drawBuilding(svg, o) {
      o = o || {}; var P = o.into || svg;
      var STOREYS = 5, X0 = 90, X1 = 530, TOP = 150, H = 108;
      el("rect", { x:60, y:TOP+STOREYS*H+8, width:500, height:26, rx:4, "class":"b-slab", id:"b-slab" }, P);
      el("rect", { x:X0, y:TOP, width:X1-X0, height:STOREYS*H, rx:6, "class":"b-shell", id:"b-shell" }, P);
      for (var s = 0; s < STOREYS; s++) {
        var y = TOP + s*H, yb = y + H;
        el("line", { x1:X0, y1:yb, x2:X1, y2:yb, "class":"b-floor", id:"floor-"+s }, P);
        el("line", { x1:X0+16, y1:yb-6, x2:X1-16, y2:y+6, "class":"beam", id:"beam-"+s+"a" }, P);
        el("line", { x1:X1-16, y1:yb-6, x2:X0+16, y2:y+6, "class":"beam", id:"beam-"+s+"b" }, P);
        // one hidden 70px shard along each beam's midpoint: the piece the UV cut
        // knocks loose (04-demolition tweens it away; it never draws otherwise)
        shard(P, "shard-"+s+"a", X0+16, yb-6, X1-16, y+6);
        shard(P, "shard-"+s+"b", X1-16, yb-6, X0+16, y+6);
        for (var w = 0; w < 3; w++)
          el("rect", { x:X0+34+w*140, y:y+30, width:74, height:46, rx:3, "class":"b-win", id:"win-"+s+"-"+w }, P);
      }
      if (o.door) el("rect", { x:280, y:620, width:60, height:70, rx:3, "class":"b-door", id:"b-door" }, P);
    }
    function shard(P, id, x1, y1, x2, y2) {
      var mx = (x1 + x2) / 2, my = (y1 + y2) / 2, L = Math.hypot(x2 - x1, y2 - y1),
          ux = (x2 - x1) / L, uy = (y2 - y1) / L;
      el("line", { x1:(mx - 35 * ux).toFixed(1), y1:(my - 35 * uy).toFixed(1),
                   x2:(mx + 35 * ux).toFixed(1), y2:(my + 35 * uy).toFixed(1),
                   "class":"shard", id:id }, P);
    }
    // the same six beams the demolition cuts, in the order it cuts them
    var CUT_ORDER = ["4a","4b","3a","2b","3b","1a"];
    function setBeamsCut(tl, ids, offset) {
      ids.forEach(function (k) {
        var e = document.getElementById("beam-" + k);
        e.style.strokeDashoffset = "640"; e.style.opacity = "0.25";
        tl.set("#beam-" + k, { strokeDashoffset:640, opacity:0.25 }, 0);
      });
    }
"""

BUILDING_CSS = """
    .b-slab  { fill:var(--ink); }
    .b-shell { fill:none; stroke:var(--ink); stroke-width:5; }
    .b-floor { stroke:var(--ink); stroke-width:2.5; opacity:.55; }
    .b-win   { fill:var(--mist); stroke:var(--ink); stroke-width:2; }
    .b-door  { fill:var(--paper); stroke:var(--ink); stroke-width:4; }
    .beam    { stroke:var(--aqua); stroke-width:9; stroke-linecap:round;
               stroke-dasharray:640; stroke-dashoffset:0; }
    .shard   { stroke:var(--aqua); stroke-width:9; stroke-linecap:round; opacity:0; }
"""

# ---------------------------------------------------------------- BARRIER

BARRIER_JS = r"""
    // Skin cross-section: wavy surface, a brick-course stratum corneum, a
    // dashed epidermis/dermis boundary, an optional dermis hatch (aqua braces
    // = the collagen under the surface) and 32px labels. Geometry is a pure
    // function of o.w / o.h -- no PRNG. Adapted from catalog skin-band +
    // barrier-wall.
    //   o = { id, w, h, surf, boundary, brickRows, door:{col}, hatch:{n, cut:[i]},
    //         orient:"top"|"left", x, y, labels:true }
    // "left": drawn horizontally then rotated so the SURFACE faces left and the
    // band stands vertically at o.x with width o.h and height o.w.
    function drawBarrier(svg, o) {
      var g = el("g", { id:o.id, "class":"barrier" }, svg);
      var inner = g;
      if (o.orient === "left") {
        inner = el("g", { transform:"translate(" + o.x + " 0) rotate(-90) translate(-" + o.w + " 0)" }, g);
      } else if (o.x || o.y) {
        inner = el("g", { transform:"translate(" + (o.x||0) + " " + (o.y||0) + ")" }, g);
      }
      var w = o.w, h = o.h, surf = o.surf, bnd = o.boundary;
      // washes FIRST so everything paints above them
      el("rect", { x:0, y:surf, width:w, height:bnd - surf, "class":"bar-band", id:o.id + "-epi" }, inner);
      el("rect", { x:0, y:bnd, width:w, height:h - bnd, "class":"bar-band", id:o.id + "-derm" }, inner);
      // NO wash rects here: transform-scaling an SVG rect inside a translated group
      // rendered around the SVG origin, not the rect's edge. Washes are HTML divs
      // laid over the band by the file that owns it (see frames_c.py).
      // dermis hatch
      if (o.hatch) {
        var n = o.hatch.n || Math.max(2, Math.round(w / 150)), hx = w / n;
        for (var i = 0; i < n; i++) {
          var x0 = i * hx + 14, x1 = (i + 1) * hx - 14;
          var a = el("line", { x1:x0, y1:h - 14, x2:x1, y2:bnd + 14, "class":"bar-h", id:o.id + "-h-" + i }, inner);
          var b = el("line", { x1:x1, y1:h - 14, x2:x0, y2:bnd + 14, "class":"bar-h", id:o.id + "-hb-" + i }, inner);
          [a, b].forEach(function (L) { var len = Math.hypot(x1 - x0, h - bnd - 28);
            L.style.strokeDasharray = len; L.style.strokeDashoffset = 0; L.setAttribute("data-len", len); });
        }
        (o.hatch.cut || []).forEach(function (i) {
          ["-h-", "-hb-"].forEach(function (s) {
            var L = document.getElementById(o.id + s + i);
            L.style.strokeDashoffset = L.getAttribute("data-len"); L.style.opacity = "0.25"; });
        });
      }
      // brick courses (running bond)
      var BW = 130, BH = 58, J = 16, rows = o.brickRows == null ? 2 : o.brickRows;
      for (var r = 0; r < rows; r++) {
        var yb = surf + 10 + r * (BH + J), off = (r % 2) ? -73 : 0, c = 0;
        for (var xb = off; xb < w; xb += BW + J, c++) {
          if (o.door && r === 0 && c === o.door.col) {
            el("line", { x1:xb + 20, y1:yb, x2:xb + 20, y2:yb + BH, "class":"bar-jamb" }, inner);
            el("line", { x1:xb + BW - 20, y1:yb, x2:xb + BW - 20, y2:yb + BH, "class":"bar-jamb" }, inner);
            el("rect", { x:xb + 20, y:yb, width:BW - 40, height:BH, "class":"bar-doorgap", id:o.id + "-door" }, inner);
            continue;
          }
          el("rect", { x:Math.max(0, xb), y:yb, width:Math.min(w, xb + BW) - Math.max(0, xb), height:BH, rx:9,
                       "class":"bar-brick", id:o.id + "-b-" + r + "-" + c }, inner);
        }
      }
      // surface wave and boundary
      var d = "";
      for (var k = 0; k <= 24; k++) {
        var x = w * k / 24, y = surf + 7 * Math.sin(2.2 * 6.2832 * x / w) + 3 * Math.sin(5.1 * 6.2832 * x / w);
        d += (k ? "L" : "M") + x.toFixed(1) + " " + y.toFixed(1) + " ";
      }
      el("path", { d:d, "class":"bar-surface", id:o.id + "-surface" }, inner);
      el("line", { x1:0, y1:bnd, x2:w, y2:bnd, "class":"bar-boundary", id:o.id + "-boundary" }, inner);
      if (o.labels !== false) {
        if (o.orient === "left") {
          txt(g, o.x + surf + 22, 52, "EPIDERMIS", "bar-label");
          txt(g, o.x + h - 22, 52, "DERMIS", "bar-label", "end");
        } else {
          txt(inner, 22, surf - 16, "EPIDERMIS", "bar-label");
          txt(inner, 22, h - 18, "DERMIS", "bar-label");
        }
      }
      return g;
    }
"""

BARRIER_CSS = """
    .bar-band { fill:var(--mist); }
    .bar-brick { fill:var(--paper); stroke:var(--ink); stroke-width:3; }
    .bar-jamb { stroke:var(--ink); stroke-width:4; }
    .bar-doorgap { fill:var(--paper); }
    .bar-surface { fill:none; stroke:var(--ink); stroke-width:4; opacity:.7; }
    .bar-boundary { stroke:var(--ink); stroke-width:4; stroke-dasharray:14 10; opacity:.55; }
    .bar-h { stroke:var(--aqua); stroke-width:7; stroke-linecap:round; opacity:.55; }
    .bar-label { font-family:var(--font-mono); font-size:32px; letter-spacing:.1em;
                 fill:var(--ink-2); opacity:1; }
    /* was opacity:.7 -- composites to 2.78:1 on paper, failing the 4.5 text
       floor; full opacity measures 4.89:1. The dim was cosmetic, not
       load-bearing (EPIDERMIS/DERMIS are the only text on these labels). */
"""

# ---------------------------------------------------------------- TRACT

TRACT_JS = r"""
    // The powder route: one path from the scoop tip through the mouth, down
    // the oesophagus, round the stomach and along the intestine to ORIGIN,
    // plus four branch paths from ORIGIN to the destination panels.
    var TRACT_D = "M 404 530 C 470 510 560 500 600 545 C 640 595 700 625 700 685 " +
                  "C 700 785 780 825 880 815 C 980 805 1000 725 950 685 " +
                  "C 900 645 860 725 900 765 C 960 815 1060 805 1120 745 C 1180 685 1200 620 1250 560";
    var ORIGIN = { x:1250, y:560 };
    var BRANCHES = {
      skin:    "M 1250 560 C 1330 560 1380 300 1520 300",
      joints:  "M 1250 560 C 1340 560 1380 460 1520 460",
      tendons: "M 1250 560 C 1340 560 1380 620 1520 620",
      other:   "M 1250 560 C 1330 560 1380 780 1520 780"
    };
    function drawTract(svg) {
      el("path", { d:TRACT_D, "class":"tract", id:"tract" }, svg);
      for (var k in BRANCHES) el("path", { d:BRANCHES[k], "class":"branch", id:"br-" + k }, svg);
    }
"""

TRACT_CSS = """
    .tract { fill:none; stroke:var(--ink); stroke-width:6; stroke-linecap:round; opacity:.8; }
    .branch { fill:none; stroke:var(--ink-2); stroke-width:5; stroke-linecap:round; } /* was --ink-3 (2.67:1 on paper, fails 3:1 graphic floor); --ink-2 measures 4.89:1 */
"""

# ---------------------------------------------------------------- TILES

TILES_JS = r"""
    // 23 trial tiles. FIXED index sets, so the industry-tagged tiles that dim
    // in the promise are the ones that fall out in the payoff. No survivor
    // count is ever displayed -- the source gives none.
    var TAGS = { industry:[0,2,3,5,8,9,11,13,14,16,19,21],
                 lowq:    [1,2,4,5,7,9,10,12,15,16,18,20,22],
                 small:   [1,4,7,10,12,15,18,20,22],
                 short:   [3,5,9,13,14,16] };
    function drawTiles(container, n, o) {
      for (var i = 0; i < n; i++) {
        var d = document.createElement("div"); d.className = "tr " + ((o && o.size) || "full"); d.id = "tr-" + i;
        d.style.opacity = "1";
        var t = document.createElement("span"); t.className = "tr-tag"; t.id = "tag-" + i;
        d.appendChild(t); container.appendChild(d);
      }
    }
    function tiles(ids) { return ids.map(function (i) { return "#tr-" + i; }); }
"""


# ---------------------------------------------------------------- Python helpers

def kt(id_, text, cls="", em=()):
    """A kinetic-type block: one span per word (opacity 0 until its beat).
    The LAST word carries its own id ({id_}-last) so a motion-sidecar
    assertion can target exactly one element -- a bare .kt-word class
    selector matches every word and is rejected as ambiguous."""
    words = text.split()
    spans = []
    for i, w in enumerate(words):
        c = "kt-word" + (" em" if w.strip("?.!,") in em else "")
        idattr = (' id="' + id_ + '-last"') if i == len(words) - 1 else ""
        spans.append('<span class="' + c + '"' + idattr + '>' + w + '</span>')
    return '<p class="kt ' + cls + '" id="' + id_ + '">' + " ".join(spans) + '</p>'


def chip(id_, text, cls="", style=""):
    return f'<p class="chip {cls}" id="{id_}" style="{style}">{text}</p>'


def cite(id_, text, on_ink=False, style=""):
    return f'<div class="cite{" on-ink" if on_ink else ""}" id="{id_}" style="{style}">{text}</div>'


def panel(id_, wash, inner, style="", cls=""):
    """A washed panel. Copy MUST be wrapped in an element (never a bare text
    node) so it sits above the wash -- the :only-child guard makes a stray
    case visible."""
    return (f'<div class="panel {cls}" id="{id_}" style="{style}">'
            f'<div class="wash {wash}" id="{id_}-wash"></div>{inner}</div>')


def abs_(x, y, w=None, h=None):
    s = f"position:absolute;left:{x}px;top:{y}px;"
    if w is not None:
        s += f"width:{w}px;"
    if h is not None:
        s += f"height:{h}px;"
    return s


def plate(id_, src, style="", fit="cover", scrim=None, filt=""):
    """A validated photographic plate: .plate (positioned box, clips) >
    .worldclip (overflow:hidden, content box) > .world (the ONLY element a
    camera push may transform) > <img>. Mirrors the .stage/.worldclip/.world
    split every scene already uses for its own camera, so a plate survives the
    file's outer camera AND carries its own independent Ken Burns leg on
    `#{id_}-world` without either transform fighting the other's clip edge.

    `scrim` is an optional CSS background (e.g. "linear-gradient(...)") on a
    div ABOVE the image so caption-weight text can sit on a photo without a
    second measured contrast case; build_frames.py's media assert requires
    every <img> to be wrapped exactly this way. decoding/loading are set for
    a seek-based renderer: the frame must never be captured mid-decode.
    """
    scrim_html = f'<div class="plate-scrim" id="{id_}-scrim" style="background:{scrim};"></div>' if scrim else ""
    # data-layout-allow-overflow: a Ken Burns push on -world legitimately
    # exceeds its own box (that is what "zoomed in" means); .worldclip's
    # overflow:hidden already clips it with no visible defect -- this only
    # silences hyperframes check's geometry-only container_overflow warning.
    return (f'<div class="plate" id="{id_}" style="{style}">'
            f'<div class="worldclip"><div class="world" id="{id_}-world" data-layout-allow-overflow="true">'
            f'<img src="{src}" alt="" decoding="sync" loading="eager" '
            f'style="width:100%;height:100%;object-fit:{fit};{filt}"></div></div>'
            f'{scrim_html}</div>')


PLATE_CSS = """
    /* position:relative by default so .worldclip's inset:0 resolves against
       THIS box, not whatever ancestor happens to be positioned (a bounded
       thumbnail relies on this); a full-bleed usage overrides to absolute
       via its own inline style, which wins on specificity. */
    .plate { position:relative; overflow:hidden; }
    .plate .worldclip { position:absolute; inset:0; overflow:hidden; }
    .plate .world { position:relative; width:100%; height:100%;
                    transform-origin:50% 50%; will-change:transform; }
    .plate-scrim { position:absolute; inset:0; }
"""


# ---------------------------------------------------------------- ease vocabulary as JS
import json as _json
from _preamble import EASE as _EASE
EASE_JS = "    var EASE = " + _json.dumps(_EASE) + ";\n"
