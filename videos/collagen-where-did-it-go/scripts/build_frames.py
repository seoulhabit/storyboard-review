#!/usr/bin/env python3
"""Emit compositions/frames/*.html. GENERATED -- edit THIS file, not the output.

Six files for seven scripted scenes, split by ACTOR CONTINUITY rather than by
narration sentence. That is the rule ectoin violated: its 09-exclusion.html and
10-messier.html draw byte-identical protein geometry because they were split per
sentence, so one actor got drawn twice instead of moved.

  00-cold-open   molecule at a door             (no VO, 5s)
  01-building    THE BUILDING   S1 + S2         phases: intact -> beams cut
  02-door        the building's entrance  S3
  03-digestion   the powder route         S4
  04-evidence    the evidence stack       S5
  05-verdict     THE BUILDING returns  S6 + S7  phases: tools -> verdict -> end

Scene durations are NEVER authored here: they are derived from the real VO takes
by vo_timing.py, which ffprobes each .wav. The VO is the master clock.
"""
import re, subprocess, sys
from pathlib import Path
from _preamble import scene, EASE
from vo_lines import by_scene

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "compositions" / "frames"

TARGET_TOTAL = 189.0   # 3:09.000 exactly
# Was 180.0 (3:00) at atempo 1.265. The tempo was dialled back to 1.20 for a
# calmer read, which costs ~8.3s of runtime; this is the nearest whole second
# above the natural total, so the cold open lands at a comfortable ~4.7s rather
# than clamping at its 3.2s floor. The mechanism is unchanged: every other scene
# is clocked by its VO and the cold open absorbs the remainder.

LEAD = 0.25   # scene opens this long before its first line
TAIL = 0.40   # scene holds this long after its last line ends
# The closing scene holds longer: YouTube draws its end-screen elements over
# the final 5-20s, and that window has to be calm and clear of content.
ENDCARD_HOLD = 5.0   # floor: YouTube's end-screen window is the final 5-20s
# Turn-taking gaps are scaled by this. The authored values were set before
# any take existed and assumed a ~184 wpm read; the real corpus averages
# much slower, so the same gaps read as slack rather than comic timing.
GAP_SCALE = 0.36
# The cold open is WORDLESS, so its exact length is the one duration in the piece
# that costs nothing to move. It is therefore the balancing term: every other
# scene is clocked by its VO, and the cold open absorbs whatever remains to land
# the root on TARGET_TOTAL. Clamped so it can never collapse below a length the
# hook can actually land in. Its own beats scale with it -- see s00.
COLD_OPEN_MIN, COLD_OPEN_MAX = 3.2, 6.0


def wav_dur(p: Path) -> float:
    if not p.exists():
        return 2.4          # placeholder before the VO takes exist
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a:0",
         "-show_entries", "stream=duration", "-of", "csv=p=0", str(p)],
        capture_output=True, text=True).stdout.strip()
    return round(float(out), 3)


def scene_timing():
    """-> {scene: {"dur": s, "lines": [{...,"start","dur"}]}}, scene-relative."""
    grouped, out = by_scene(), {}
    for sc in ["01", "02", "03", "04", "05"]:
        t, lines = LEAD, []
        for ln in grouped[sc]:
            d = wav_dur(ROOT / ln["wav"])
            lines.append({**ln, "start": round(t, 3), "dur": d})
            t += d + ln["gap"] * GAP_SCALE
        dur = round(t - grouped[sc][-1]["gap"] * GAP_SCALE + TAIL
                    + (ENDCARD_HOLD if sc == "05" else 0.0), 3)
        out[sc] = {"dur": dur, "lines": lines}
    # cold open last: it takes whatever is left to hit TARGET_TOTAL exactly
    spoken = sum(v["dur"] for v in out.values())
    cold = round(min(COLD_OPEN_MAX, max(COLD_OPEN_MIN, TARGET_TOTAL - spoken)), 3)
    out = {"00": {"dur": cold, "lines": []}, **out}
    return out


# --------------------------------------------------------------------------
# The dialogue lane stack. One card per spoken line, at most two visible: the
# live line, and the one before it held back at 38% with the ground showing
# through. That gives one PANEL-SCALE beat per line for free -- the thing
# ectoin's Act 1 lacked when it measured 5.8% active steps with word-scale
# motion. At ~4.5s per line it also keeps every scene inside the 6.0s long-form
# quiet ceiling without a single decorative tween.
# --------------------------------------------------------------------------
LANE_CSS = """
    /* Cards are ANCHORED, not scrolled, and nothing here is measured.
       Two earlier versions both failed:
         1. collapsing each spent card's height/margin/padding to make room --
            rejected 31x by `check` as gsap_non_transform_motion, because layout
            properties snap to integer device pixels and stutter under a
            seek-by-frame capture;
         2. translating a tall stack to centre the live card on a MEASURED
            offset -- correct in principle, but it depends on clientHeight, on
            the offsetParent chain (will-change:transform silently makes the
            stack one) and on webfont metrics, and it shipped every active card
            below the fold in the first snapshot pass.
       This version uses yPercent, which GSAP resolves against the ELEMENT'S OWN
       height. The live card's TOP sits on the anchor line; the previous card's
       BOTTOM sits just above it. Correct for any two card heights, with no
       measurement and nothing to go stale when a line is reworded. */
    .lanes { position:absolute; right:0; top:0; bottom:0; width:46%;
             padding-left:var(--s-6); overflow:hidden; }
    .lane { position:absolute; top:50%; opacity:0; }
    .lane-soul { left:0;  right:7%; }
    .lane-jay  { right:0; left:7%;  }
    /* In the FULL-WIDTH band layouts (03-digestion, 04-evidence) the lanes span
       1728px, and BASE's `max-width:1080px` over-constrains a box that has both
       `left` and `right` set -- CSS drops `right` for LTR, so a Jay card was
       laid out from its left offset and simply stopped, leaving the right ~530px
       of the frame unused. It read as a 38.25s content-void in the bottom-right
       across the whole of scene 03. Anchoring each lane to ONE edge lets the
       max-width do what it is for (a readable measure) instead of silently
       cancelling the alignment. */
    .lanes.low  .lane-soul, .lanes.rail .lane-soul { left:0;  right:auto; }
    .lanes.low  .lane-jay,  .lanes.rail .lane-jay  { right:0; left:auto;  }
    .lane .say em { font-style:normal; font-weight:800; }
"""

NAMES = {"soul": "SoulHabit", "jay": "Jay"}


def lanes_html(lines, extra_class=""):
    out = [f'      <div class="lanes {extra_class}">']
    for ln in lines:
        who = ln["who"]
        # Copy is always wrapped in an element. A bare text node under a .wash
        # has nothing to carry z-index, renders overpainted, and the engine's
        # own text_occluded pass cannot see it -- it walks text ELEMENTS.
        out.append(
            f'        <div class="lane lane-{who}" id="L{ln["idx"]}">'
            f'<p class="lane-name">{NAMES[who]}</p>'
            f'<p class="say">{ln["disp"]}</p></div>')
    out.append("      </div>")
    return "\n".join(out)


def lanes_tl(lines):
    """One beat per spoken line: the new card lands, the previous steps back.

    Positions are pure yPercent, so they resolve against each card's own height:
      live      yPercent 0     -> its TOP on the anchor line
      previous  yPercent -100  -> its BOTTOM just above the anchor line
      spent     opacity 0
    No measurement, so nothing here depends on font metrics, container height or
    which element happens to be an offsetParent.

    SoulHabit `arrive` and Jay `slam` are deliberately different tweens with
    different eases. A shared entrance on every beat is the template failure
    this whole build is shaped against.
    """
    t = []
    for i, ln in enumerate(lines):
        at, who, cid = ln["start"], ln["who"], f'L{ln["idx"]}'
        if who == "soul":
            t.append(f'    tl.fromTo("#{cid}", {{ opacity:0, x:-70, yPercent:0 }}, '
                     f'{{ opacity:1, x:0, yPercent:0, duration:0.42, '
                     f'ease:"{EASE["arrive"]}" }}, {at:.3f});')
        else:
            t.append(f'    tl.fromTo("#{cid}", {{ opacity:0, x:70, scale:0.9, yPercent:0 }}, '
                     f'{{ opacity:1, x:0, scale:1, yPercent:0, duration:0.38, '
                     f'ease:"{EASE["slam"]}" }}, {at:.3f});')
        # Both exits FINISH before the entrance begins, and the spent card leaves
        # ahead of the receding one so the two never cross. Clamped at 0 so the
        # first swap of a scene cannot go negative.
        if i:
            ex = max(0.0, at - 0.44)
            t.append(f'    tl.to("#L{lines[i-1]["idx"]}", {{ opacity:0.38, yPercent:-100, '
                     f'y:-18, duration:0.38, ease:"{EASE["swap"]}" }}, {ex:.3f});')
        if i > 1:   # only two cards ever legible
            ex2 = max(0.0, at - 0.56)
            t.append(f'    tl.to("#L{lines[i-2]["idx"]}", {{ opacity:0, yPercent:-200, '
                     f'y:-36, duration:0.44, ease:"{EASE["exit"]}" }}, {ex2:.3f});')
    return "\n".join(t)


def _wrap_world(body, cid):
    """Insert the clip layer around the camera layer.

    Done here rather than in each scene's own markup so no scene can be added
    later without it -- the failure it prevents is silent in the source and only
    shows up as ink in a reserved zone on a rendered frame.
    """
    m = re.search(r'( *)<div class="world"([^>]*)>', body)
    assert m, f"{cid}: no .world element to wrap"
    ind = m.group(1)
    body = body[:m.start()] + f'{ind}<div class="worldclip">\n' + \
           f'{ind}<div class="world"{m.group(2)}>' + body[m.end():]
    # close it against the stage's closing tag
    close = "\n      </div>\n"
    assert body.count(close) >= 1, f"{cid}: no stage close to match"
    i = body.rindex(close)
    body = body[:i] + "\n      </div>" + close + body[i + len(close):]
    return body


def emit(cid, dur, body, css, tl):
    # LANE_CSS is appended to EVERY scene, after the scene's own rules, because
    # every scene carries dialogue. It was previously defined and never
    # included: the cards silently fell back to the in-flow .lane rule in BASE,
    # rendered stacked in the flex row, and the first card was pushed off frame
    # entirely. Caught by snapshot extraction, not by `check` -- an unreferenced
    # CSS constant is not a lint error.
    (OUT / f"{cid}.html").write_text(
        scene(cid, dur, _wrap_world(body, cid), css + LANE_CSS, tl))
    return f"  {cid}.html  {dur:7.3f}s"


# ==========================================================================
# THE BUILDING -- the persistent actor.
#
# Drawn by one deterministic builder shared by 01-building and 05-verdict, so
# the closing scene returns to the SAME structure rather than a lookalike. No
# Math.random anywhere: a reseek must reproduce the frame exactly.
#
# The aqua X-braces ARE the collagen. 01 cuts them; 05 restores some of them.
# Every node carries a stable id so a later phase can move it instead of
# redrawing it.
# ==========================================================================
BUILDING_JS = """
    function drawBuilding(svg) {
      var NS = "http://www.w3.org/2000/svg";
      function el(t, a) { var n = document.createElementNS(NS, t);
        for (var k in a) n.setAttribute(k, a[k]); return n; }
      var STOREYS = 5, X0 = 90, X1 = 530, TOP = 150, H = 108;
      svg.appendChild(el("rect", { x:60, y:TOP+STOREYS*H+8, width:500, height:26,
                                   rx:4, class:"b-slab", id:"b-slab" }));
      svg.appendChild(el("rect", { x:X0, y:TOP, width:X1-X0, height:STOREYS*H,
                                   rx:6, class:"b-shell" }));
      for (var s = 0; s < STOREYS; s++) {
        var y = TOP + s*H, yb = y + H;
        svg.appendChild(el("line", { x1:X0, y1:yb, x2:X1, y2:yb, class:"b-floor" }));
        // the collagen: one X-brace per storey, each half independently cuttable
        svg.appendChild(el("line", { x1:X0+16, y1:yb-6, x2:X1-16, y2:y+6,
                                     class:"beam", id:"beam-"+s+"a" }));
        svg.appendChild(el("line", { x1:X1-16, y1:yb-6, x2:X0+16, y2:y+6,
                                     class:"beam", id:"beam-"+s+"b" }));
        for (var w = 0; w < 3; w++)
          svg.appendChild(el("rect", { x:X0+34+w*140, y:y+30, width:74, height:46,
                                       rx:3, class:"b-win", id:"win-"+s+"-"+w }));
      }
    }
"""

BUILDING_CSS = """
    .b-slab  { fill:var(--ink); }
    .b-shell { fill:none; stroke:var(--ink); stroke-width:5; }
    .b-floor { stroke:var(--ink); stroke-width:2.5; opacity:.55; }
    .b-win   { fill:var(--mist); stroke:var(--ink); stroke-width:2; }
    .beam    { stroke:var(--aqua); stroke-width:9; stroke-linecap:round;
               stroke-dasharray:640; stroke-dashoffset:0; }
"""


# ==========================================================================
# 00 -- COLD OPEN.  5s, no VO.
#
# Frame zero IS the hook, so it is COMPOSED IN CSS, not tweened in: the
# molecule is already at the door and the title is already set at t=0. The
# timeline only moves what happens NEXT. A headline authored to fade in over
# its first 0.4s reads fine on a scrub and exports a near-blank first frame.
# ==========================================================================
def s00(dur):
    k = dur / 5.0          # beats were authored against a 5.0s cold open
    css = """
    .co { display:flex; flex-direction:column; justify-content:center;
          align-items:center; height:100%; gap:var(--s-6); }
    .co-title { text-align:center; max-width:1400px; }
    .co-title .l1 { display:block; font-family:var(--font-mono);
                    font-size:var(--t-label); letter-spacing:var(--tr-mono-wide);
                    text-transform:uppercase; color:var(--ink-2); margin-bottom:var(--s-4); }
    .co-title .l2 { display:block; font-family:var(--font-display);
                    font-size:var(--t-hero); line-height:var(--lh-tight);
                    letter-spacing:var(--tr-display); color:var(--ink); }
    .co-row { display:flex; align-items:flex-end; gap:var(--s-5); }
    .co-mol, .co-wall { display:block; }
    .mol-body { fill:none; stroke:var(--coral); stroke-width:14; stroke-linecap:round; }
    .mol-box  { fill:var(--ink); }
    .wall-face { fill:var(--mist); stroke:var(--ink); stroke-width:5; }
    .wall-door { fill:var(--paper); stroke:var(--ink); stroke-width:4; }
    .tag { font-family:var(--font-mono); font-size:var(--t-label);
           letter-spacing:var(--tr-mono); fill:var(--ink-2); opacity:0; }
    .co-rule { height:6px; background:var(--coral); width:520px;
               transform:scaleX(0); transform-origin:50% 50%; }
"""
    body = """
      <div class="stage">
       <div class="world">
        <div class="co">
          <p class="co-title">
            <span class="l1">SeoulHabit &middot; Evidence, not hype</span>
            <span class="l2">You bought collagen.<br>Where did it actually go?</span>
          </p>
          <div class="co-rule" id="co-rule"></div>
          <div class="co-row">
            <svg class="co-mol" id="mol" width="470" height="330" viewBox="0 0 470 330"
                 aria-hidden="true"></svg>
            <svg class="co-wall" width="300" height="330" viewBox="0 0 300 330"
                 aria-hidden="true">
              <rect class="wall-face" x="10" y="10" width="280" height="310" rx="6"/>
              <rect class="wall-door" x="120" y="252" width="60" height="68" rx="3"/>
              <text class="tag" id="tag-door" x="150" y="238" text-anchor="middle">the way in</text>
            </svg>
          </div>
        </div>
       </div>
      </div>
"""
    tl = f"""
    // Deterministic triple-helix ribbon -- no Math.random, so a reseek matches.
    (function () {{
      var NS = "http://www.w3.org/2000/svg", svg = document.getElementById("mol");
      for (var k = 0; k < 3; k++) {{
        var d = "", ph = k * 2.09;
        for (var x = 0; x <= 400; x += 8)
          d += (x ? "L" : "M") + (30 + x) + " " +
               (150 + Math.sin(x / 42 + ph) * 52).toFixed(2) + " ";
        var p = document.createElementNS(NS, "path");
        p.setAttribute("d", d); p.setAttribute("class", "mol-body");
        p.setAttribute("opacity", (0.45 + k * 0.27).toFixed(2));
        svg.appendChild(p);
      }}
      var b = document.createElementNS(NS, "rect");
      b.setAttribute("x", 352); b.setAttribute("y", 214);
      b.setAttribute("width", 84); b.setAttribute("height", 62);
      b.setAttribute("rx", 4); b.setAttribute("class", "mol-box");
      svg.appendChild(b);
      var t = document.createElementNS(NS, "text");
      t.setAttribute("class", "tag"); t.setAttribute("id", "tag-mol");
      t.setAttribute("x", 230); t.setAttribute("y", 318);
      t.setAttribute("text-anchor", "middle");
      t.textContent = "one collagen molecule";
      svg.appendChild(t);
    }})();

    // The nudge: it tries the door and does not fit. ~9% of frame moving.
    // Beat positions are a FRACTION of the scene's own duration, because this
    // scene's length floats -- it absorbs whatever the VO-clocked scenes leave
    // over to land the root on exactly 3:00. Authored against a fixed 5.0s they
    // would run past the end of a shorter timeline and clamp mid-tween.
    tl.to("#mol", {{ x:64, duration:{0.50 * k:.3f}, ease:"{EASE['arrive']}" }}, {0.55 * k:.3f});
    tl.to("#mol", {{ x:18, duration:{0.55 * k:.3f}, ease:"{EASE['slam']}" }}, {1.05 * k:.3f});
    tl.to("#tag-mol",  {{ opacity:1, duration:{0.35 * k:.3f}, ease:"{EASE['arrive']}" }}, {1.70 * k:.3f});
    tl.to("#tag-door", {{ opacity:1, duration:{0.35 * k:.3f}, ease:"{EASE['arrive']}" }}, {2.35 * k:.3f});
    tl.to("#co-rule",  {{ scaleX:1, duration:{0.60 * k:.3f}, ease:"{EASE['wipe']}" }}, {3.05 * k:.3f});
    tl.to("#mol", {{ x:0, duration:{0.70 * k:.3f}, ease:"{EASE['hold']}" }}, {3.85 * k:.3f});
"""
    return emit("00-cold-open", dur, body, css, tl)


# ==========================================================================
# 01 -- THE BUILDING.  S1 + S2 merged on one actor.
#
# Two phases on ONE timeline, one set of DOM nodes:
#   A (S1)  the building stands, beams intact, real skin plate as its ground
#   B (S2)  the sun arrives and the beams are CUT -- the same <line> elements,
#           dash-offset away and desaturated, never a second drawing
#
# That merge is the point. Ectoin split by sentence and ended up with two files
# drawing byte-identical geometry; the audit calls that a rebuilt actor and a
# viewer calls it two slides.
# ==========================================================================
def s01(dur, lines):
    # phase B opens on line 5 -- the first S2 line
    pb = lines[4]["start"]
    css = BUILDING_CSS + """
    .split { display:flex; height:100%; align-items:center; }
    .actor { flex:0 0 52%; position:relative; height:100%;
             display:flex; align-items:center; justify-content:center; }
    .plate { position:absolute; left:0; right:var(--s-6); bottom:0; height:190px;
             border-radius:var(--r-3); overflow:hidden; background:#1A1A1A; }
    .plate img { width:100%; height:100%; object-fit:cover; display:block;
                 transform:scale(1.02); transform-origin:50% 45%; }
    .plate-cap { position:absolute; left:var(--s-4); bottom:var(--s-3);
                 font-family:var(--font-mono); font-size:var(--t-chip);
                 letter-spacing:var(--tr-mono); color:var(--paper);
                 text-shadow:0 1px 6px rgba(0,0,0,.85); margin:0; }
    .bwrap { position:relative; }
    .sun { position:absolute; top:6%; right:4%; width:150px; height:150px;
           border-radius:50%; background:var(--highlighter); opacity:0;
           transform:scale(0.5); }
    .ray { stroke:var(--highlighter); stroke-width:7; stroke-linecap:round;
           stroke-dasharray:260; stroke-dashoffset:260; }
    .cut-cite { position:absolute; left:0; bottom:214px; opacity:0; }
"""
    body = f"""
      <div class="stage">
       <div class="world" id="world">
        <div class="split">
          <div class="actor">
            <div class="bwrap">
              <svg id="bldg" width="620" height="720" viewBox="0 0 620 720"
                   aria-hidden="true"></svg>
              <svg class="rays" id="rays" width="620" height="720" viewBox="0 0 620 720"
                   style="position:absolute;inset:0" aria-hidden="true">
                <line class="ray" id="ray-0" x1="560" y1="120" x2="330" y2="330"/>
                <line class="ray" id="ray-1" x1="580" y1="210" x2="360" y2="430"/>
                <line class="ray" id="ray-2" x1="590" y1="310" x2="380" y2="520"/>
              </svg>
              <div class="sun" id="sun"></div>
            </div>
            <div class="plate" id="plate">
              <img src="assets/images/skin-base.png" alt=""
                   width="1200" height="1200" loading="eager" decoding="sync">
              <p class="plate-cap">real skin, magnified</p>
            </div>
            <div class="cite cut-cite" id="cite-uv">J Invest Dermatol &middot; 1998</div>
          </div>
{lanes_html(lines)}
        </div>
       </div>
      </div>
"""
    tl = f"""
{BUILDING_JS}
    drawBuilding(document.getElementById("bldg"));

    // --- phase A : the building stands ---------------------------------
    // Slow camera drift across the whole scene. One leg, not a breathing loop.
    tl.fromTo("#world", {{ scale:1.045, y:-16 }},
              {{ scale:1.0, y:0, duration:{dur:.3f}, ease:"{EASE['hold']}" }}, 0);
    tl.fromTo("#plate img", {{ scale:1.02 }},
              {{ scale:1.10, duration:{dur:.3f}, ease:"{EASE['hold']}" }}, 0);
    for (var s = 0; s < 5; s++) {{
      tl.fromTo(["#beam-"+s+"a", "#beam-"+s+"b"],
                {{ strokeDashoffset:640 }},
                {{ strokeDashoffset:0, duration:0.55, ease:"{EASE['wipe']}" }},
                0.30 + s * 0.13);
    }}

    // --- phase B : the demolition crew ---------------------------------
    tl.to("#sun", {{ opacity:1, scale:1, duration:0.55, ease:"{EASE['slam']}" }}, {pb - 0.30:.3f});
    tl.to([".ray"], {{ strokeDashoffset:0, duration:0.60, stagger:0.10,
                       ease:"{EASE['wipe']}" }}, {pb + 0.25:.3f});
    // The SAME beam elements are cut -- not a second set drawn over them.
    // Ordered top-down so the damage reads as spreading, not blinking.
    ["4a","4b","3a","2b","3b","1a"].forEach(function (k, i) {{
      tl.to("#beam-" + k, {{ strokeDashoffset:640, opacity:0.25, duration:0.42,
                             ease:"{EASE['wipe']}" }}, {pb + 1.15:.3f} + i * 0.34);
    }});
    // The building takes the hit: a whole-actor beat, not a word.
    tl.to("#bldg", {{ skewX:-1.4, y:9, duration:0.90, ease:"{EASE['swap']}" }}, {pb + 3.4:.3f});
    tl.to("#cite-uv", {{ opacity:1, duration:0.40, ease:"{EASE['arrive']}" }}, {pb + 1.5:.3f});
    tl.to("#sun", {{ opacity:0.45, duration:0.70, ease:"{EASE['hold']}" }}, {pb + 6.0:.3f});

{lanes_tl(lines)}
"""
    return emit("01-building", dur, body, css, tl)


# ==========================================================================
# 02 -- THE DOOR.  S3.  Camera pushed in to the building's entrance, which is
# what the cold open was looking at. Same space, closer framing: that rhyme is
# what makes the piece read as one place rather than six slides.
# ==========================================================================
def s02(dur, lines):
    css = """
    .split { display:flex; height:100%; align-items:center; }
    .actor { flex:0 0 54%; position:relative; height:100%;
             display:flex; flex-direction:column; justify-content:center;
             gap:var(--s-5); padding-right:var(--s-6); }
    .door-row { display:flex; align-items:flex-end; gap:var(--s-4); }
    .mol2 { fill:none; stroke:var(--coral); stroke-width:12; stroke-linecap:round; }
    .mol2-box { fill:var(--ink); }
    .wall2 { fill:var(--mist); stroke:var(--ink); stroke-width:5; }
    .door2 { fill:var(--paper); stroke:var(--ink); stroke-width:4; }
    /* The film that CAN sit on top -- a sheet, not a molecule getting through. */
    .film { fill:var(--aqua); opacity:0; }
    .shine { stroke:var(--paper); stroke-width:5; opacity:0; stroke-linecap:round; }
    /* Size comparison. Deliberately NOT chart grammar -- no axis, no gridline,
       no plotted point. Two labelled blocks and an explicit not-to-scale note,
       because an illustrated comparison that borrows chart furniture reads as a
       measurement it is not. */
    .sz { display:flex; gap:var(--s-4); align-items:stretch; }
    .sz-card { flex:1 1 0; min-width:0; border-radius:var(--r-3); position:relative;
               padding:var(--s-4) var(--s-5); background:var(--mist);
               border:3px solid var(--rule-strong); opacity:0; overflow:hidden; }
    .sz-card.big { border-color:var(--coral); }
    /* --mist on --paper is a 9.7-luma step: invisible to a viewer and to the
       cadence check alike. The wash is what makes each card a real beat --
       paper->aqua is 90.6 and paper->coral is 102.8. */
    .sz-card .wash { z-index:0; }
    .sz-card .sz-n, .sz-card .sz-l { position:relative; z-index:1; }
    .sz-n { font-family:var(--font-display); font-size:var(--t-figure);
            line-height:1; margin:0 0 6px; color:var(--ink); }
    .sz-l { font-family:var(--font-mono); font-size:var(--t-chip);
            letter-spacing:var(--tr-mono); color:var(--ink-2-mist); margin:0; }
    .sz-note { font-family:var(--font-mono); font-size:var(--t-chip);
               color:var(--ink-2-mist); margin:var(--s-3) 0 0; opacity:0; }
    .stamp { position:absolute; left:8%; top:22%; padding:14px 34px;
             border:6px solid var(--coral); border-radius:var(--r-2);
             font-family:var(--font-body); font-weight:800; font-size:var(--t-frame);
             color:var(--coral); transform:rotate(-9deg) scale(1.5); opacity:0; }
    .cite-abs { position:absolute; left:0; bottom:2%; opacity:0; }
"""
    body = f"""
      <div class="stage">
       <div class="world" id="world">
        <div class="split">
          <div class="actor">
            <div class="door-row" id="doorrow">
              <svg id="mol2" width="430" height="300" viewBox="0 0 430 300" aria-hidden="true"></svg>
              <svg width="330" height="380" viewBox="0 0 330 380" aria-hidden="true">
                <rect class="wall2" x="8" y="8" width="314" height="364" rx="6"/>
                <rect class="film" id="film" x="8" y="8" width="314" height="364" rx="6"/>
                <line class="shine" id="sh1" x1="60"  y1="70"  x2="110" y2="120"/>
                <line class="shine" id="sh2" x1="110" y1="60"  x2="150" y2="100"/>
                <rect class="door2" x="132" y="304" width="66" height="68" rx="3"/>
              </svg>
              <div class="stamp" id="stamp">REJECTED</div>
            </div>
            <div class="sz">
              <div class="sz-card" id="sz-a">
                <div class="wash aqua" id="wash-a"></div>
                <p class="sz-n">~500</p>
                <p class="sz-l">daltons &mdash; the size limit for getting through</p>
              </div>
              <div class="sz-card big" id="sz-b">
                <div class="wash coral" id="wash-b"></div>
                <p class="sz-n">~300,000</p>
                <p class="sz-l">daltons &mdash; one collagen molecule</p>
              </div>
            </div>
            <p class="sz-note" id="sz-note">Blocks are labelled, not drawn to scale.</p>
            <div class="cite cite-abs" id="cite-da">Exp Dermatol &middot; 2000</div>
          </div>
{lanes_html(lines)}
        </div>
       </div>
      </div>
"""
    tl = f"""
    (function () {{
      var NS = "http://www.w3.org/2000/svg", svg = document.getElementById("mol2");
      for (var k = 0; k < 3; k++) {{
        var d = "", ph = k * 2.09;
        for (var x = 0; x <= 360; x += 8)
          d += (x ? "L" : "M") + (24 + x) + " " +
               (140 + Math.sin(x / 38 + ph) * 46).toFixed(2) + " ";
        var p = document.createElementNS(NS, "path");
        p.setAttribute("d", d); p.setAttribute("class", "mol2");
        p.setAttribute("opacity", (0.45 + k * 0.27).toFixed(2));
        svg.appendChild(p);
      }}
      var b = document.createElementNS(NS, "rect");
      b.setAttribute("x", 316); b.setAttribute("y", 196); b.setAttribute("width", 78);
      b.setAttribute("height", 58); b.setAttribute("rx", 4);
      b.setAttribute("class", "mol2-box"); svg.appendChild(b);
    }})();

    // Camera: this scene starts already pushed in and eases back a little, so
    // the cut from the cold open reads as the same space at a closer framing.
    tl.fromTo("#world", {{ scale:1.14, x:60 }},
              {{ scale:1.0, x:0, duration:2.60, ease:"{EASE['camera']}" }}, 0);

    tl.to("#mol2", {{ x:70, duration:0.55, ease:"{EASE['arrive']}" }}, {lines[1]['start'] - 0.4:.3f});
    tl.to("#mol2", {{ x:26, duration:0.50, ease:"{EASE['slam']}" }}, {lines[1]['start'] + 0.2:.3f});
    tl.to("#sz-a", {{ opacity:1, duration:0.40, ease:"{EASE['arrive']}" }}, {lines[1]['start'] + 1.1:.3f});
    tl.fromTo("#wash-a", {{ scaleX:0 }}, {{ scaleX:1, duration:0.55,
              ease:"{EASE['wipe']}" }}, {lines[1]['start'] + 1.3:.3f});
    tl.to("#sz-b", {{ opacity:1, duration:0.40, ease:"{EASE['arrive']}" }}, {lines[1]['start'] + 2.4:.3f});
    tl.fromTo("#wash-b", {{ scaleX:0 }}, {{ scaleX:1, duration:0.55,
              ease:"{EASE['wipe']}" }}, {lines[1]['start'] + 2.6:.3f});
    tl.to("#sz-note", {{ opacity:1, duration:0.35, ease:"{EASE['arrive']}" }}, {lines[1]['start'] + 3.9:.3f});
    tl.to("#cite-da", {{ opacity:1, duration:0.35, ease:"{EASE['arrive']}" }}, {lines[1]['start'] + 4.4:.3f});
    // the wall darkens as the point lands -- a whole-panel step, not a chip
    tl.to("#doorrow", {{ y:-26, duration:0.90, ease:"{EASE['swap']}" }}, {lines[1]['start'] + 5.4:.3f});
    tl.to("#sz-b", {{ scale:1.05, duration:0.50, yoyo:true, repeat:1,
                      ease:"{EASE['slam']}" }}, {lines[1]['start'] + 6.4:.3f});
    tl.fromTo("#stamp", {{ opacity:0, scale:1.5, rotate:-9 }},
              {{ opacity:1, scale:1, rotate:-9, duration:0.42, ease:"{EASE['slam']}" }},
              {lines[2]['start']:.3f});

    // The correction: it cannot get IN, but it can lie ON. Same wall, new state.
    tl.to("#stamp", {{ opacity:0, duration:0.35, ease:"{EASE['swap']}" }}, {lines[3]['start'] - 0.2:.3f});
    tl.to("#film", {{ opacity:0.55, duration:0.70, ease:"{EASE['swap']}" }}, {lines[3]['start'] + 0.3:.3f});
    tl.to([".shine"], {{ opacity:1, duration:0.30, stagger:0.12, ease:"{EASE['arrive']}" }},
          {lines[4]['start']:.3f});
    // ...and the beams below are still cut. The callback that makes the joke land.
    tl.to("#sz-b", {{ borderColor:"#C97A5C", scale:1.03, duration:0.45,
                      ease:"{EASE['slam']}" }}, {lines[6]['start']:.3f});
    tl.to("#sz-b", {{ scale:1, duration:0.60, ease:"{EASE['hold']}" }}, {lines[6]['start'] + 0.5:.3f});

{lanes_tl(lines)}
"""
    return emit("02-door", dur, body, css, tl)


# ==========================================================================
# 03 -- DIGESTION.  S4.  The one scene that genuinely LEAVES the building.
# Layout is deliberately different from 01/02: the actor runs as a horizontal
# pipeline across the top and the dialogue sits under it, so the piece does not
# become nine variations of one two-column frame.
# ==========================================================================
def s03(dur, lines):
    css = """
    .stack { display:flex; flex-direction:column; height:100%; gap:var(--s-5); }
    .pipe { flex:0 0 46%; display:flex; align-items:center;
            justify-content:space-between; gap:var(--s-4); min-height:0; }
    .node { flex:1 1 0; min-width:0; min-height:0; height:100%;
            border-radius:var(--r-3); background:var(--mist);
            display:flex; flex-direction:column; align-items:center;
            justify-content:center; gap:var(--s-3); padding:var(--s-4);
            opacity:0; position:relative; overflow:hidden; }
    /* NO `.node > * { position:relative }` here. It has the same specificity as
       `.wash` in BASE and comes later in the cascade, so it overrode
       `position:absolute` on the wash itself -- which then collapsed to zero
       height in the flex column and rendered nothing at all. BASE's
       `.wash ~ *` already lifts every FOLLOWING sibling, which is exactly the
       set that needs lifting and excludes the wash. The authored beats were
       present in the source the whole time and moved zero pixels; the cadence
       check on the render is what caught it. */
    .node-l { font-family:var(--font-mono); font-size:var(--t-chip);
              letter-spacing:var(--tr-mono); color:var(--ink-2-mist);
              text-transform:uppercase; margin:0; text-align:center; }
    .arrow { flex:0 0 54px; height:6px; background:var(--ink); opacity:0;
             transform:scaleX(0); transform-origin:0% 50%; }
    .fibre { fill:none; stroke:var(--coral); stroke-width:10; stroke-linecap:round; }
    .bit { fill:var(--coral); }
    .dest { display:flex; gap:var(--s-3); width:100%; }
    .dest span { flex:1 1 0; text-align:center; border-radius:var(--r-2);
                 background:var(--paper); border:2px solid var(--rule-strong);
                 font-family:var(--font-mono); font-size:var(--t-chip);
                 color:var(--ink); padding:8px 4px; }
    /* .lanes stays RELATIVE so the cards' top:44% resolves against it. */
    .lanes.low { position:relative; width:100%; flex:1 1 0; padding-left:0; }
"""
    body = f"""
      <div class="stage">
       <div class="world" id="world">
        <div class="stack">
          <div class="pipe">
            <div class="node" id="n1"><div class="wash aqua" id="w-n1"></div>
              <svg width="150" height="130" viewBox="0 0 150 130" aria-hidden="true">
                <path d="M30 96 L120 96 L104 40 L46 40 Z" fill="none"
                      stroke="#131516" stroke-width="5"/>
                <circle cx="62" cy="66" r="7" class="bit"/>
                <circle cx="86" cy="74" r="7" class="bit"/>
                <circle cx="74" cy="86" r="7" class="bit"/>
              </svg>
              <p class="node-l">a scoop of powder</p>
            </div>
            <div class="arrow" id="a1"></div>
            <div class="node" id="n2"><div class="wash aqua" id="w-n2"></div>
              <svg id="chop" width="230" height="130" viewBox="0 0 230 130" aria-hidden="true"></svg>
              <p class="node-l">digestion cuts it up</p>
            </div>
            <div class="arrow" id="a2"></div>
            <div class="node" id="n3"><div class="wash aqua" id="w-n3"></div>
              <div class="dest">
                <span id="d1">skin</span><span id="d2">joints</span><span id="d3">tendons</span>
              </div>
              <p class="node-l">your body decides where</p>
            </div>
          </div>
{lanes_html(lines, "low")}
        </div>
       </div>
      </div>
"""
    tl = f"""
    (function () {{
      var NS = "http://www.w3.org/2000/svg", svg = document.getElementById("chop");
      // one long fibre, then the pieces it becomes -- both drawn up front, the
      // timeline swaps which is visible. Deterministic offsets, no randomness.
      var d = "";
      for (var x = 0; x <= 200; x += 6)
        d += (x ? "L" : "M") + (14 + x) + " " + (66 + Math.sin(x / 26) * 22).toFixed(2) + " ";
      var p = document.createElementNS(NS, "path");
      p.setAttribute("d", d); p.setAttribute("class", "fibre");
      p.setAttribute("id", "fibre"); svg.appendChild(p);
      var g = document.createElementNS(NS, "g");
      g.setAttribute("id", "bits"); g.setAttribute("opacity", "0");
      for (var i = 0; i < 12; i++) {{
        var c = document.createElementNS(NS, "circle");
        c.setAttribute("cx", 22 + (i % 6) * 34);
        c.setAttribute("cy", 46 + Math.floor(i / 6) * 40);
        c.setAttribute("r", 9); c.setAttribute("class", "bit");
        g.appendChild(c);
      }}
      svg.appendChild(g);
    }})();

    tl.fromTo("#world", {{ scale:1.035, y:-12 }},
              {{ scale:1.0, y:0, duration:{dur:.3f}, ease:"{EASE['hold']}" }}, 0);
    tl.to("#n1", {{ opacity:1, duration:0.40, ease:"{EASE['arrive']}" }}, 0.30);
    tl.to("#a1", {{ opacity:1, scaleX:1, duration:0.35, ease:"{EASE['wipe']}" }}, 0.70);
    tl.to("#n2", {{ opacity:1, duration:0.40, ease:"{EASE['arrive']}" }}, 0.95);

    // the cut: one long fibre becomes many small pieces
    tl.to("#fibre", {{ opacity:0, duration:0.35, ease:"{EASE['swap']}" }}, {lines[0]['start'] + 1.5:.3f});
    tl.to("#bits",  {{ opacity:1, duration:0.35, ease:"{EASE['swap']}" }}, {lines[0]['start'] + 1.55:.3f});

    tl.to("#a2", {{ opacity:1, scaleX:1, duration:0.35, ease:"{EASE['wipe']}" }}, {lines[2]['start']:.3f});
    tl.to("#n3", {{ opacity:1, duration:0.40, ease:"{EASE['arrive']}" }}, {lines[2]['start'] + 0.3:.3f});

    // the dispatch board: the destination keeps changing, because the body picks
    // Direct colour tweens, not className swaps: a className tween diffs
    // computed style and is not dependable under an out-of-order seek, which is
    // exactly how the renderer drives this timeline.
    ["#d1", "#d3", "#d2", "#d1", "#d2"].forEach(function (id, i) {{
      var at = {lines[4]['start']:.3f} + i * 0.85;
      // One bounded yoyo per pulse rather than an on-tween plus an
      // off-tween: half the tweens, and a bounded repeat is the sanctioned
      // idiom for finite idle motion (an INFINITE repeat would be wall-clock
      // behaviour wearing a tween's clothes).
      tl.fromTo(id, {{ backgroundColor:"#F7F5F0", borderColor:"#D9D3C6" }},
                {{ backgroundColor:"#59B8AE", borderColor:"#59B8AE",
                   duration:0.30, yoyo:true, repeat:1,
                   ease:"{EASE['slam']}" }}, at);
    }});
    // Each node washes in turn across L21 -- a whole-node colour step
    // (--mist -> --aqua is 80.9 luma) instead of chip-sized pulses that
    // measured near zero on a 1920-wide frame and left a 10s quiet run.
    [["#w-n1", 0.0], ["#w-n2", 2.1], ["#w-n3", 4.2]].forEach(function (p) {{
      tl.fromTo(p[0], {{ scaleX:0 }}, {{ scaleX:1, duration:0.70,
                ease:"{EASE['wipe']}" }}, {lines[4]['start'] + 1.2:.3f} + p[1]);
      tl.to(p[0], {{ scaleX:0, duration:0.55,
                ease:"{EASE['wipe']}" }}, {lines[4]['start'] + 2.6:.3f} + p[1]);
    }});
    tl.to("#n3", {{ scale:1.03, duration:0.40, ease:"{EASE['slam']}" }}, {lines[5]['start']:.3f});
    tl.to("#n3", {{ scale:1, duration:0.60, ease:"{EASE['hold']}" }}, {lines[5]['start'] + 0.45:.3f});

{lanes_tl(lines)}
"""
    return emit("03-digestion", dur, body, css, tl)


# ==========================================================================
# 04 -- THE EVIDENCE.  S5.  The payoff scene, and the only one that leaves the
# building metaphor entirely -- correctly, because it is about evidence
# QUALITY, not mechanism.
#
# Ground is INVERTED to ink. That is a real structural variety beat (the piece
# is otherwise all paper) and it makes the strip-away read as a filter being
# applied to the whole field, not a list being edited.
#
# Mechanism adapted from catalog/visual-components/threshold-list (ranked list
# split by a cutoff, below-cutoff rows stripped) and .../stat-reveal (count-up
# numeral + citation chip, explicitly never chart grammar). Adapted, not
# skinned: both are 9:16 with safe area baked in, and the design system is
# explicit that layout needs a real landscape variant rather than a scale.
# ==========================================================================
def s04(dur, lines):
    css = """
    #root { background:var(--ink); }
    /* Two full-width bands, which no other scene uses -- that IS the structural
       variety here, together with the inverted ground. The first attempt put the
       dialogue in a 300px rail under a five-child flex column: the grid squashed
       to 8px bars and every card was guillotined mid-sentence by the rail's own
       overflow. Caught on extracted frames, after `check` flagged it as
       content_overlap / text_occluded / container_overflow. */
    /* GRID, not flex column: grid rows cannot overlap, and an explicit
       `minmax(0, ...)` stops a child's content min-size from blowing the row
       out. With flex the verdict bar pushed past its band and sat on top of the
       dialogue card underneath -- visible on an extracted frame, and reported by
       `check` as content_overlap. */
    /* THREE explicit rows: evidence field / verdict bar / dialogue. The verdict
       bar gets `auto` so it always takes its natural height -- inside the first
       row it was squeezed out and clipped to a 9px sliver with the dialogue card
       drawn over it, which is what the content_overlap finding actually was. */
    .ev { display:grid; grid-template-rows:minmax(0,1fr) auto auto 34%;
          gap:var(--s-3); height:100%; }
    /* Explicit rows here too. As a flex column the head and the tile field took
       their content height and the pill/citation row -- the LAST child -- was
       the one that got clipped. `minmax(0,1fr)` on the field is what makes it
       the part that gives way instead. */
    /* The TILE FIELD is the flexible row -- with a floor, so it can neither be
       crushed to hairlines (minmax(0,1fr) did that: 12px rows) nor overflow its
       band (a fixed height did that: it pushed the pill/citation row out of
       frame and let the verdict bar paint over the tiles). overflow:hidden is
       the safety net -- it was dropped in the flex->grid conversion, which is
       what let the overflow reach the neighbouring row at all. */
    .ev-top { min-height:0; display:grid; overflow:hidden;
              grid-template-rows:auto auto minmax(120px,1fr); gap:var(--s-3); }
    .outrow { display:flex; gap:var(--s-3); }
    .out { font-family:var(--font-mono); font-size:var(--t-chip);
           letter-spacing:var(--tr-mono); color:var(--ink); background:var(--celadon);
           border-radius:var(--r-pill); padding:8px 22px; opacity:0; }
    .ev-head { display:flex; align-items:flex-start; gap:var(--s-5); flex:0 0 auto; }
    .ev-n { font-family:var(--font-display); font-size:96px; line-height:0.95;
            color:var(--paper); margin:0; min-width:150px; }
    .ev-n-l { font-family:var(--font-mono); font-size:var(--t-label);
              letter-spacing:var(--tr-mono-wide); text-transform:uppercase;
              color:#93989A; margin:0; }   /* 5.64:1 on --ink; --ink-3-dark is 4.13 */
    .ev-n-l.hi { opacity:0; color:var(--celadon); }
    .grid { min-height:0; height:100%; display:grid; gap:14px;
            grid-template-columns:repeat(8, 1fr); grid-template-rows:repeat(3, 1fr); }
    /* #2C2A26 on the #131516 ground is only a 21-luma step, which left the
       scene's opening frame reading as near-blank right after a hard cut.
       #4A453E is a 45-luma step and gives the field real presence. */
    .tr { border-radius:var(--r-2); background:#4A453E; border:2px solid #6A6459; }
    /* Tile-state colours are chosen by LUMA, not hue. idle->industry is a
       35.6-luma step and idle->keep(celadon) is 126.9; the first pair tried
       (moss for keep) measured 53.6 and would have read as almost nothing. */
    .midrow { display:flex; align-items:center; gap:var(--s-3);
              flex-wrap:nowrap; min-width:0; }
    .midrow > * { flex:0 0 auto; }
    .f-pill { font-family:var(--font-mono); font-size:var(--t-chip);
              letter-spacing:var(--tr-mono); color:var(--paper);
              border:2px solid #93989A; border-radius:var(--r-pill);
              padding:9px 22px; opacity:0; white-space:nowrap; }
    .midrow .spacer { flex:1 1 auto; }
    /* Measured at x=1823 against a safe line of 1824 with the default chip
       padding -- inside, but by ONE pixel, which is not clearance, it is luck.
       Tightening the horizontal padding here (the type size is untouched, since
       32px is the chrome floor) buys ~32px of real margin. */
    .midrow .cite { opacity:0; padding:10px 18px; }
    .verdict-bar { border-radius:var(--r-3); background:var(--ink-soft);
                   padding:var(--s-4) var(--s-5); opacity:0; position:relative;
                   overflow:hidden; }
    .verdict-bar .vb { font-family:var(--font-body); font-weight:800;
                       font-size:var(--t-frame); color:var(--paper); margin:0; }
    /* the dialogue band: a real 42% of the safe box, not a 300px sliver */
    .lanes.rail { position:relative; width:100%; padding-left:0; min-height:0; }
    /* live card grows DOWN from the band's top edge, so a long line has the whole
       band to use instead of being cut in half by a centre anchor */
    .lanes.rail .lane { top:0; }
    /* On the ink ground both lanes need a variant, each re-measured against the
       new ground rather than assumed to transfer. */
    .lane-soul { background:var(--ink-soft); border-left-color:var(--paper); }
    .lane-soul .say { color:var(--paper); }            /* 15.10:1 */
    .lane-soul .lane-name { color:#93989A; }           /* 5.64:1 on --ink-soft;
       --ink-3-dark measures 4.13:1 here and does NOT clear the floor. */
    .lane-jay { background:#33251F; border-right-color:var(--coral); }
    .lane-jay .say { color:#F0D9CE; }                  /* 10.89:1 */
    .lane-jay .lane-name { color:#C98F76; }            /*  5.38:1 */
"""
    body = f"""
      <div class="stage">
       <div class="world" id="world">
        <div class="ev">
          <div class="ev-top">
            <div class="ev-head">
              <p class="ev-n" id="ev-n">0</p>
              <div>
                <p class="ev-n-l" id="ev-n-l0">randomised trials<br>reviewed in 2025</p>
                <p class="ev-n-l hi" id="ev-n-l">&hellip; still standing once you keep</p>
                <p class="ev-n-l hi" id="ev-n-l2">only the independent, higher-quality ones</p>
              </div>
            </div>
            <div class="outrow">
              <div class="out" id="out-1">hydration</div>
              <div class="out" id="out-2">elasticity</div>
              <div class="out" id="out-3">wrinkles</div>
            </div>
            <div class="grid" id="grid"></div>
          </div>
          <div class="midrow">
            <div class="f-pill" id="f1">&check; independently funded</div>
            <div class="f-pill" id="f2">&check; higher quality</div>
            <div class="spacer"></div>
            <div class="cite on-ink" id="c1">Nutrients &middot; 2023</div>
            <div class="cite on-ink" id="c2">Am J Med &middot; 2025</div>
          </div>
          <div class="verdict-bar" id="vb">
            <div class="wash paper" id="vb-wash"></div>
            <p class="vb">Once you keep only those, the effect stops showing up.</p>
          </div>
{lanes_html(lines, "rail")}
        </div>
       </div>
      </div>
"""
    tl = f"""
    (function () {{
      var g = document.getElementById("grid");
      for (var i = 0; i < 23; i++) {{
        var d = document.createElement("div");
        // present, NOT absent: the field is composed at this scene's frame zero.
        // A hard cut into an empty frame is the one thing a cut must not do.
        d.className = "tr"; d.id = "tr-" + i; d.style.opacity = "1";
        g.appendChild(d);
      }}
    }})();

    // NO camera move in this scene. `.worldclip` clips at the safe line, so a
    // scale that starts zoomed cuts whatever sits against the left edge -- here
    // the count numeral, which rendered as a half-glyph for the first ~2s. The
    // ground inversion IS this scene's entrance; it does not need a second one,
    // and a camera move that costs a legible numeral is not worth its count.

    // 23 tiles arrive as a field, then the numeral counts to match it. The
    // numeral is the study's own n, so it is data performing; the tiles are a
    // pictogram, not a chart -- no axis, no gridline, nothing plotted.
    tl.fromTo(".tr", {{ scaleY:0.62 }}, {{ scaleY:1, duration:0.26, stagger:0.026,
              ease:"{EASE['arrive']}" }}, 0.0);
    tl.to({{ n:0 }}, {{ n:23, duration:1.30, ease:"{EASE['count']}",
        onUpdate: function () {{
          document.getElementById("ev-n").textContent = Math.round(this.targets()[0].n);
        }} }}, 0.45);
    tl.to("#c1", {{ opacity:1, duration:0.35, ease:"{EASE['arrive']}" }}, {lines[0]['start'] + 1.2:.3f});
    // one outcome per named outcome, each lighting the band of trials that
    // measured it -- 8 tiles is a third of the field, so it reads as a beat
    [1, 2, 3].forEach(function (k) {{
      var at = {lines[0]['start'] + 2.2:.3f} + (k - 1) * 1.55;
      tl.to("#out-" + k, {{ opacity:1, duration:0.32, ease:"{EASE['slam']}" }}, at);
      for (var i = (k - 1) * 8; i < Math.min(k * 8, 23); i++) {{
        tl.to("#tr-" + i, {{ backgroundColor:"#93B896", duration:0.34, yoyo:true,
                             repeat:1, ease:"{EASE['swap']}" }}, at + (i % 8) * 0.018);
      }}
    }});
    // the outcomes clear as the funding caveat lands -- they were the claim
    tl.to([".out"], {{ opacity:0.25, duration:0.40, stagger:0.06,
                       ease:"{EASE['exit']}" }}, {lines[1]['start'] + 0.2:.3f});

    // L24 is "small, short, and paid for by collagen makers" and used to carry ONE
    // beat, leaving a 6.2s frozen window the motion sidecar caught. The three
    // weaknesses now land as they are spoken, in thirds across the line.
    tl.to([".tr"], {{ backgroundColor:"#6B4433", borderColor:"#8A5943",
                      duration:0.50, stagger:0.02, ease:"{EASE['swap']}" }},
          {lines[1]['start'] + 0.3:.3f});
    ["#tr-3", "#tr-9", "#tr-14", "#tr-20"].forEach(function (id, i) {{
      tl.to(id, {{ scale:0.80, duration:0.40, ease:"{EASE['swap']}" }},
            {lines[1]['start'] + 1.9:.3f} + i * 0.55);
    }});
    tl.to("#ev-n", {{ color:"#C98F76", duration:0.60, ease:"{EASE['swap']}" }},
          {lines[1]['start'] + 4.1:.3f});

    // THE FILTER. Two pills, then the field is stripped.
    tl.to("#f1", {{ opacity:1, duration:0.30, ease:"{EASE['arrive']}" }}, {lines[2]['start'] + 0.5:.3f});
    tl.to("#f2", {{ opacity:1, duration:0.30, ease:"{EASE['arrive']}" }}, {lines[2]['start'] + 1.0:.3f});
    (function () {{
      var KEEP = {{ 2:1, 7:1, 11:1, 18:1 }};   // fixed indices, never Math.random
      for (var i = 0; i < 23; i++) {{
        if (KEEP[i]) {{
          tl.to("#tr-" + i, {{ backgroundColor:"#93B896", borderColor:"#C3DCC5",
                               scale:1, duration:0.40, ease:"{EASE['swap']}" }},
                {lines[2]['start'] + 1.6:.3f} + i * 0.012);
        }} else {{
          tl.to("#tr-" + i, {{ opacity:0.10, scale:0.86, duration:0.45,
                               ease:"{EASE['wipe']}" }},
                {lines[2]['start'] + 1.6:.3f} + i * 0.012);
        }}
      }}
    }})();
    tl.to("#c2", {{ opacity:1, duration:0.35, ease:"{EASE['arrive']}" }},
          {lines[2]['start'] + 2.6:.3f});
    // The numeral does not just dim -- it COUNTS DOWN to what survived, which is
    // the actual finding.
    tl.to("#ev-n-l0", {{ opacity:0, duration:0.35, ease:"{EASE['swap']}" }},
          {lines[2]['start'] + 3.1:.3f});
    tl.to({{ n:23 }}, {{ n:4, duration:1.40, ease:"{EASE['count']}",
        onUpdate: function () {{
          document.getElementById("ev-n").textContent = Math.round(this.targets()[0].n);
        }} }}, {lines[2]['start'] + 3.1:.3f});
    tl.to("#ev-n", {{ color:"#93B896", duration:0.80, ease:"{EASE['swap']}" }},
          {lines[2]['start'] + 3.1:.3f});
    tl.to("#ev-n-l", {{ opacity:1, duration:0.40, ease:"{EASE['arrive']}" }},
          {lines[2]['start'] + 3.4:.3f});
    tl.to("#ev-n-l2", {{ opacity:1, duration:0.40, ease:"{EASE['arrive']}" }},
          {lines[2]['start'] + 4.6:.3f});
    ["#tr-2", "#tr-7", "#tr-11", "#tr-18"].forEach(function (id, i) {{
      tl.to(id, {{ scale:1.30, duration:0.34, yoyo:true, repeat:1,
                   ease:"{EASE['slam']}" }}, {lines[2]['start'] + 5.4:.3f} + i * 0.44);
    }});
    tl.to("#vb", {{ opacity:1, duration:0.35, ease:"{EASE['arrive']}" }},
          {lines[2]['start'] + 7.2:.3f});
    tl.fromTo("#vb-wash", {{ scaleX:0 }},
              {{ scaleX:1, duration:0.80, ease:"{EASE['wipe']}" }},
              {lines[2]['start'] + 7.3:.3f});

{lanes_tl(lines)}
"""
    return emit("04-evidence", dur, body, css, tl)


# ==========================================================================
# 05 -- THE VERDICT.  S6 + S7 merged, and the BUILDING RETURNS.
#
# Three phases on one timeline and one set of nodes:
#   A (S6)  three tools converge on the damaged building; beams partly restore
#   B (S7)  the verdict -- three products weighed, sunscreen slides UNDER the
#           building and becomes its foundation slab
#   C       end card, motion calmed, end-screen zone cleared
#
# The building is the SAME structure drawn by the same builder as 01, so the
# return reads as coming back to a place rather than arriving at a lookalike.
# Convergence adapted from catalog/visual-components/factor-converge (three
# outer nodes drawing inward, none more important than the others); the weighing
# from .../material-triptych, re-laid-out for landscape rather than scaled.
#
# END-SCREEN RESERVE IS SCENE-SCOPED. YouTube draws its overlays on the last
# 5-20s only, so reserving the right third across the whole video would waste it
# on every other frame.
# ==========================================================================
def s05(dur, lines):
    pb = lines[5]["start"]          # S7 opens on line 36
    # The end card opens after the LAST line finishes, not on line 40 -- YouTube
    # draws its end-screen overlays across the final 5-20s and needs a calm,
    # cleared frame to sit on. ENDCARD_HOLD (added to this scene's duration by
    # scene_timing) is what buys that window.
    pc = lines[-1]["start"] + lines[-1]["dur"] + 0.25
    css = BUILDING_CSS + """
    /* The actor column and the weigh row share the LEFT region and swap; the
       dialogue lanes sit outside both and persist for the whole scene. */
    .actorwrap { position:absolute; left:0; top:0; bottom:0; width:52%; }
    .actor { position:relative; width:100%; height:100%;
             display:flex; align-items:center; justify-content:center; }
    /* SPF shield -- a real panel over the building, ~9% of frame at a 90-luma
       step against --paper, so it reads as a beat instead of measuring nothing. */
    .shield { position:absolute; left:6%; right:6%; top:8%; bottom:6%;
              border-radius:18px; background:var(--aqua); opacity:0;
              transform:scaleY(0); transform-origin:50% 0%; }
    .shield-edge { position:absolute; left:6%; right:6%; top:8%; bottom:6%;
                   border-radius:18px; border:5px solid var(--aqua); opacity:0; }
    .tool { position:absolute; width:190px; padding:var(--s-3) var(--s-4);
            border-radius:var(--r-3); background:var(--mist);
            border:3px solid var(--ink); text-align:center; opacity:0; }
    .tool p { margin:0; font-family:var(--font-mono); font-size:var(--t-chip);
              letter-spacing:var(--tr-mono); color:var(--ink); }
    #t1 { left:0; top:6%; } #t2 { right:0; top:6%; } #t3 { right:2%; bottom:30%; }
    #t4 { left:2%; bottom:34%; }
    /* coral marks a limitation or a refusal -- which is exactly what this one is,
       and the only place coral is used as a fill in this scene. --ink on --coral
       measures 5.60:1. */
    .tool.no { background:var(--coral); border-color:var(--coral); }
    /* the verdict row -- three products weighed against each other */
    .weigh { position:absolute; left:0; top:0; bottom:0; width:52%;
             display:flex; align-items:center; gap:var(--s-4); opacity:0; }
    .w-card { flex:1 1 0; min-width:0; border-radius:var(--r-3); background:var(--mist);
              border:3px solid var(--rule-strong); padding:var(--s-4);
              display:flex; flex-direction:column; gap:var(--s-3);
              align-items:center; position:relative; overflow:hidden; }
    /* Products are DRAWN, not photographed. catalog/manifest.json's
       approved_surfaces for product-photography excludes HyperFrames
       compositions outright -- "that lane is browser-drawn only (SVG/CSS/
       canvas/WebGL), no generative imagery". Those plates are approved for the
       thumbnail, and that is where they are used. The skin-macro plate in
       01-building is a different catalog with the opposite note: its README
       puts those plates in a composition's tactile/evidentiary role. */
    .w-card svg { width:100%; height:210px; display:block; }
    .pk-body { fill:var(--paper); stroke:var(--ink); stroke-width:5; }
    .pk-cap  { fill:var(--ink); }
    .pk-mark { fill:var(--ink-3); }
    .w-card.base .pk-body { stroke:var(--aqua); }
    .w-card.base .pk-cap  { fill:var(--aqua); }
    .w-t { font-family:var(--font-body); font-weight:800; font-size:var(--t-chip);
           color:var(--ink); margin:0; text-align:center; }
    .w-v { font-family:var(--font-mono); font-size:var(--t-chip);
           color:var(--ink-2-mist); margin:0; text-align:center; }
    .w-card.base { border-color:var(--aqua); }
    /* end card: motion calmed, and the right third + lower right kept clear for
       YouTube's own end-screen elements. */
    .endcard { position:absolute; inset:0; display:flex; flex-direction:column;
               justify-content:center; gap:var(--s-4); opacity:0;
               padding-right:calc(var(--endscreen-right) - var(--s-6));
               padding-bottom:calc(var(--endscreen-bottom) - var(--s-6)); }
    .ec-do { font-family:var(--font-body); font-weight:800; font-size:var(--t-figure);
             line-height:var(--lh-snug); color:var(--ink); margin:0; }
    .ec-sub { font-family:var(--font-display); font-size:var(--t-body);
              color:var(--ink-2); margin:0; max-width:900px; }
    .ec-mark { font-family:var(--font-mono); font-size:var(--t-label);
               letter-spacing:var(--tr-mono-wide); color:var(--ink-2-mist); margin:0; }
    .cite-abs2 { position:absolute; left:0; bottom:1%; opacity:0; }
"""
    body = f"""
      <div class="stage">
       <div class="world" id="world">
        <div class="actorwrap" id="scenewrap">
          <div class="actor">
            <svg id="bldg" width="620" height="720" viewBox="0 0 620 720" aria-hidden="true"></svg>
            <div class="shield" id="shield"></div>
            <div class="shield-edge" id="shield-edge"></div>
            <div class="tool" id="t1"><p>broad-spectrum SPF</p></div>
            <div class="tool" id="t2"><p>topical retinoid</p></div>
            <div class="tool" id="t3"><p>protein &amp; vitamin C</p></div>
            <div class="tool no" id="t4"><p>no smoking</p></div>
            <div class="cite cite-abs2" id="cite-ret">Arch Dermatol &middot; 2007</div>
          </div>
        </div>
{lanes_html(lines)}

        <div class="weigh" id="weigh">
          <div class="w-card" id="w1">
            <svg viewBox="0 0 200 200" aria-hidden="true">
              <rect class="pk-body" x="46" y="74" width="108" height="96" rx="8"/>
              <rect class="pk-cap"  x="60" y="46" width="80" height="30" rx="5"/>
              <rect class="pk-mark" x="66" y="110" width="68" height="9" rx="4"/>
              <rect class="pk-mark" x="66" y="128" width="44" height="9" rx="4"/>
            </svg>
            <p class="w-t">Collagen cream</p>
            <p class="w-v">a decent moisturiser</p>
          </div>
          <div class="w-card" id="w2">
            <svg viewBox="0 0 200 200" aria-hidden="true">
              <path class="pk-body" d="M58 46 L142 46 L152 172 L48 172 Z"/>
              <rect class="pk-cap"  x="58" y="36" width="84" height="16" rx="4"/>
              <rect class="pk-mark" x="72" y="96"  width="56" height="9" rx="4"/>
              <rect class="pk-mark" x="72" y="114" width="36" height="9" rx="4"/>
            </svg>
            <p class="w-t">Collagen powder</p>
            <p class="w-v">optional, evidence uncertain</p>
          </div>
          <div class="w-card base" id="w3">
            <svg viewBox="0 0 200 200" aria-hidden="true">
              <path class="pk-body" d="M74 62 L126 62 L138 172 L62 172 Z"/>
              <rect class="pk-cap"  x="84" y="30" width="32" height="34" rx="4"/>
              <rect class="pk-mark" x="80" y="106" width="40" height="9" rx="4"/>
              <rect class="pk-mark" x="80" y="124" width="26" height="9" rx="4"/>
            </svg>
            <p class="w-t">Sunscreen</p>
            <p class="w-v">the foundation</p>
          </div>
        </div>

        <div class="endcard" id="endcard">
          <p class="ec-do">Tomorrow morning:<br>put the sunscreen on.</p>
          <p class="ec-sub">Then decide whether the powder is worth it. Collagen isn't a
             scam or a miracle &mdash; what matters is how it reaches you, and what the
             independent evidence actually shows.</p>
          <p class="ec-mark">SeoulHabit &middot; sources in the description</p>
        </div>
       </div>
      </div>
"""
    tl = f"""
{BUILDING_JS}
    drawBuilding(document.getElementById("bldg"));
    // The building comes back DAMAGED -- the same beams 01 cut are still cut.
    // Set in the timeline at 0 AND restated here so frame 0 of this scene is
    // correct even on a cold seek that never passes through 0.
    ["4a","4b","3a","2b","3b","1a"].forEach(function (k) {{
      var e = document.getElementById("beam-" + k);
      e.style.strokeDashoffset = "640"; e.style.opacity = "0.25";
    }});
    ["4a","4b","3a","2b","3b","1a"].forEach(function (k) {{
      tl.set("#beam-" + k, {{ strokeDashoffset:640, opacity:0.25 }}, 0);
    }});
    tl.set("#bldg", {{ skewX:-1.4, y:9 }}, 0);

    // --- phase A : three tools converge --------------------------------
    tl.fromTo("#world", {{ scale:1.06 }},
              {{ scale:1.0, duration:2.4, ease:"{EASE['camera']}" }}, 0);
    tl.to("#t1", {{ opacity:1, duration:0.36, ease:"{EASE['arrive']}" }}, {lines[1]['start'] + 0.3:.3f});
    // the shield sweeps down over the building as the sunscreen line lands
    tl.fromTo("#shield", {{ scaleY:0, opacity:0.30 }},
              {{ scaleY:1, opacity:0.30, duration:0.72, ease:"{EASE['wipe']}" }},
              {lines[1]['start'] + 0.75:.3f});
    tl.to("#shield-edge", {{ opacity:1, duration:0.40, ease:"{EASE['arrive']}" }},
          {lines[1]['start'] + 1.35:.3f});
    // and eases back to a held tint once the point is made, so it does not sit
    // as a flat block over the rest of the scene
    tl.to("#shield", {{ opacity:0.12, duration:0.80, ease:"{EASE['hold']}" }},
          {lines[1]['start'] + 3.6:.3f});
    tl.to("#shield-edge", {{ opacity:0.45, duration:0.80, ease:"{EASE['hold']}" }},
          {lines[1]['start'] + 3.6:.3f});
    tl.fromTo("#t4", {{ opacity:0, scale:0.8 }},
              {{ opacity:1, scale:1, duration:0.40, ease:"{EASE['slam']}" }},
              {lines[1]['start'] + 2.7:.3f});
    tl.to("#t3", {{ opacity:1, duration:0.36, ease:"{EASE['arrive']}" }}, {lines[1]['start'] + 4.6:.3f});
    tl.to("#t2", {{ opacity:1, duration:0.36, ease:"{EASE['arrive']}" }}, {lines[2]['start'] + 0.2:.3f});
    tl.to("#cite-ret", {{ opacity:1, duration:0.35, ease:"{EASE['arrive']}" }},
          {lines[2]['start'] + 1.3:.3f});
    // the repair: SOME beams come back, and the building straightens. Not all --
    // the claim is that protecting beats replacing, not that damage is undone.
    ["4a","3a","1a"].forEach(function (k, i) {{
      tl.to("#beam-" + k, {{ strokeDashoffset:0, opacity:1, duration:0.55,
                             ease:"{EASE['wipe']}" }}, {lines[2]['start'] + 1.9:.3f} + i * 0.30);
    }});
    tl.to("#bldg", {{ skewX:0, y:0, duration:1.10, ease:"{EASE['swap']}" }},
          {lines[2]['start'] + 2.2:.3f});

    // --- phase B : the verdict ------------------------------------------
    tl.to("#scenewrap", {{ opacity:0, duration:0.45, ease:"{EASE['swap']}" }}, {pb - 0.55:.3f});
    tl.to("#weigh", {{ opacity:1, duration:0.45, ease:"{EASE['swap']}" }}, {pb - 0.45:.3f});
    tl.fromTo("#w1", {{ y:60, opacity:0 }}, {{ y:0, opacity:1, duration:0.45,
              ease:"{EASE['arrive']}" }}, {pb - 0.35:.3f});
    tl.fromTo("#w2", {{ y:60, opacity:0 }}, {{ y:0, opacity:1, duration:0.45,
              ease:"{EASE['arrive']}" }}, {lines[6]['start'] - 0.2:.3f});
    tl.fromTo("#w3", {{ y:60, opacity:0 }}, {{ y:0, opacity:1, duration:0.45,
              ease:"{EASE['arrive']}" }}, {lines[7]['start'] - 0.2:.3f});
    // sunscreen becomes the FOUNDATION: it drops out of the row and the other
    // two settle on top of it. The metaphor closing, as a layout change.
    tl.to("#w1", {{ opacity:0.45, scale:0.94, duration:0.55, ease:"{EASE['swap']}" }},
          {lines[7]['start'] + 1.1:.3f});
    tl.to("#w2", {{ opacity:0.45, scale:0.94, duration:0.55, ease:"{EASE['swap']}" }},
          {lines[7]['start'] + 1.2:.3f});
    tl.to("#w3", {{ scale:1.06, duration:0.55, ease:"{EASE['slam']}" }},
          {lines[7]['start'] + 1.3:.3f});

    // --- phase C : end card ---------------------------------------------
    tl.to("#weigh", {{ opacity:0, duration:0.50, ease:"{EASE['swap']}" }}, {pc - 0.30:.3f});
    // The lanes occupy the right 46%, which is exactly where YouTube draws its
    // end-screen elements. They clear BEFORE the end card, not with it.
    tl.to(".lanes", {{ opacity:0, duration:0.50, ease:"{EASE['swap']}" }}, {pc - 0.40:.3f});
    tl.to("#endcard", {{ opacity:1, duration:0.55, ease:"{EASE['arrive']}" }}, {pc - 0.20:.3f});
    // Motion calmed for the end screen: one slow drift, nothing competing with
    // the overlays YouTube is about to draw on the right third.
    tl.fromTo("#endcard", {{ y:14 }}, {{ y:0, duration:2.4, ease:"{EASE['hold']}" }}, {pc:.3f});

{lanes_tl(lines)}
"""
    return emit("05-verdict", dur, body, css, tl)


# --------------------------------------------------------------------------
def main():
    OUT.mkdir(parents=True, exist_ok=True)
    t = scene_timing()
    print("emitting compositions/frames/ (GENERATED -- edit build_frames.py):")
    print(s00(t["00"]["dur"]))
    print(s01(t["01"]["dur"], t["01"]["lines"]))
    print(s02(t["02"]["dur"], t["02"]["lines"]))
    print(s03(t["03"]["dur"], t["03"]["lines"]))
    print(s04(t["04"]["dur"], t["04"]["lines"]))
    print(s05(t["05"]["dur"], t["05"]["lines"]))
    print(f"  total {sum(v['dur'] for v in t.values()):.3f}s")


if __name__ == "__main__":
    main()
