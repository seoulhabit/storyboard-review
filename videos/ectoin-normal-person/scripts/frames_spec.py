#!/usr/bin/env python3
"""Per-unit scene content. The creative layer.

Each SPECS[unit_id] is fn(ctx) -> (css, body_html, timeline_js).

ctx.phases is [(name, rel_start, rel_len)] relative to the unit's own start, so
a phase's beats are stamped against a REAL measured offset, never an estimate.

Conventions enforced throughout, each one a defect this repo has actually shipped:
  * Copy inside a washed container is ALWAYS wrapped in an element. A bare text
    node has nothing to carry z-index, so the wash paints over it and the card
    renders EMPTY -- and the engine's own text_occluded pass cannot see it,
    because the text never became an element.
  * Citation pills are `Journal - Year`. No PMID, no internal id, ever.
  * JAY's colour is ground-scoped: --coral-deep on paper, --coral on ink.
  * Every tween names its own ease.
"""
from dataclasses import dataclass


@dataclass
class Ctx:
    cid: str
    dur: float
    phases: list      # [(name, rel_start, rel_len)]
    turns: list       # [(turn_id, abs_start, len)]
    merged: bool

    def p(self, name):
        """(start, len) of a phase, relative to this unit."""
        for n, s, l in self.phases:
            if n == name:
                return s, l
        raise KeyError(f"{self.cid} has no phase {name}")

    def ps(self, name):
        return self.p(name)[0]

    def pe(self, name):
        s, l = self.p(name)
        return s + l


# ---- shared fragments -----------------------------------------------------

def say(speaker, text, eid, ink=False, size=None):
    """One spoken line. SOULHABIT = display serif; JAY = Inter 800.

    Attribution is TYPE, not colour -- the serif/grotesque split survives any
    ground and the 25% phone-scale check, which a colour difference would not.
    The mark is decorative only, so a wrong-ground colour can never become a
    legibility bug.
    """
    cls = "say-s" if speaker == "S" else "say-j"
    mark = "who-s" if speaker == "S" else "who-j"
    oi = " on-ink" if ink else ""
    st = f' style="font-size:{size}"' if size else ""
    return (f'<div class="line" id="{eid}">'
            f'<i class="who {mark}{oi}"></i>'
            f'<p class="say {cls}{oi}"{st}>{text}</p></div>')


def cite(text, eid, ink=False):
    return f'<p class="cite{" on-ink" if ink else ""}" id="{eid}">{text}</p>'


def stage(inner, ground="paper", world=True):
    """A unit's outer box. .world is the camera target; .stage carries the safe
    padding and .stage > * {overflow:hidden} clips the moving world AT the safe
    line, so no camera leg can push ink into a reserved zone."""
    bg = "var(--paper)" if ground == "paper" else "var(--ink)"
    # data-layout-allow-overflow is correct here and is not a silencer: a
    # camera move NECESSARILY renders its world larger than the frame -- that
    # is what a push IS -- and .ground's overflow:hidden clips it at the safe
    # line. The engine's layout pass tests bounding boxes and cannot model
    # clip geometry, so it reports every leg as a container overflow. Marking
    # it is the documented remedy; restructuring to satisfy it would mean
    # deleting the camera.
    # ORDER IS LOad-BEARING: ground > stage(safe padding) > world > drift.
    #
    # The camera layers sit INSIDE the stage's padding, not outside it. With
    # them outside, `#drift` scaling 1.018 about the frame centre mapped a
    # compliant x=96 to 96*1.018 - 17.3 = 80.4px -- 16px inside the reserved
    # left zone -- and the hard safe-area gate failed on 1205 rendered frames
    # while every --safe-* token was declared and consumed correctly. That is
    # the documented trap: padding constrains the pre-transform box and says
    # nothing about where a transform then puts it.
    #
    # Inside, `.stage > * { overflow: hidden }` clips .world at the CONTENT
    # box, which IS the safe box, so no camera move can push ink into a
    # reserved zone regardless of its amplitude. Structural, not a margin --
    # a margin is sized against today's token and goes stale silently.
    #
    # NOT id="root" either: scene() already opens the composition's #root, and
    # a second one meant the ink background never painted and five units
    # rendered paper-on-paper at 1:1, frame zero included.
    #
    # AND the clip lives on .clipbox, which NEVER transforms. overflow:hidden
    # clips an element's CHILDREN, not itself -- so putting it on .world meant
    # scaling .world scaled its own clip region too, and content escaped the
    # safe line along with it. Measured: at t=77.25s, mid camera leg with
    # #world at scale ~1.09, the EXTREMOLYTE card sat at y=32 against a 54px
    # top line; at rest the same scene's topmost ink is y=87. A static clip
    # ancestor is what makes the containment hold under any transform.
    open_w = '<div class="world" id="world">' if world else ""
    close_w = "</div>" if world else ""
    on_ink = ground != "paper"
    band = (f'<div class="band{" on-ink" if on_ink else ""}" id="band">'
            f'<div class="band-f" id="band-f"></div>'
            f'<span class="band-t" id="band-t"></span></div>')
    return (f'<div class="ground" style="background:{bg}">'
            f'<div class="stage"><div class="clipbox">{open_w}'
            f'<div class="drift" id="drift">{inner}{band}</div>'
            f'{close_w}</div></div></div>')


BASE_SPEC_CSS = """
    .line { display:flex; flex-direction:column; }
    .col-mid { display:flex; flex-direction:column; justify-content:center;
               height:100%; gap:var(--s-6); min-height:0; }
    .two { display:grid; gap:var(--s-8); height:100%; align-items:center;
           min-height:0; }
    .row3 { display:grid; grid-template-columns:repeat(3,1fr); gap:var(--s-5);
            min-height:0; }
    .flood { position:absolute; inset:0; opacity:0; z-index:0; }
    /* A phase is a beat inside a merged unit. It is display:contents so it
       marks structure without introducing a box that would change layout. */
    .phase { display:contents; }
    /* The spoken-beat band. Absolute so it never perturbs a scene's layout;
       inside .clipbox so it cannot reach a reserved zone. Sized against the
       cadence metric, not by eye: 11.3% of frame at 215 luma = 5.5/step. */
    .band { position:absolute; left:0; right:0; bottom:0; height:136px;
            border-radius:var(--r-3); overflow:hidden; opacity:0; z-index:3; }
    .band-f { position:absolute; inset:0; background:var(--ink);
              transform:scaleX(0); transform-origin:0% 50%; }
    .band.alt .band-f { background:var(--moss); }
    /* On an ink ground the fill must go the OTHER way. ink-on-ink is a 0-luma
       step: measured, the two ink-ground bands moved their scene's quiet run
       by exactly 0.00s while every paper-ground band worked. */
    .band.on-ink .band-f     { background:var(--paper); }
    .band.on-ink.alt .band-f { background:var(--celadon); }
    .band.on-ink .band-t     { color:var(--ink); }
    .band-t { position:relative; z-index:1; display:block; padding:0 var(--s-6);
              line-height:136px; font-family:var(--font-body); font-weight:800;
              font-size:46px; color:var(--paper); opacity:0;
              white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
    .plate { position:relative; width:100%; min-height:150px; overflow:hidden;
             border-radius:var(--r-3); background:var(--mist); flex:0 0 auto; }
    .plate-fill { position:absolute; inset:0; background:var(--ink);
                  transform:scaleX(0); transform-origin:0% 50%; }
    .plate-t { position:relative; z-index:1; display:block; padding:var(--s-5);
               font-family:var(--font-body); font-weight:800; font-size:44px;
               color:var(--paper); opacity:0; }
"""

# ---- CAMERA -------------------------------------------------------------
# Continuity in this piece is carried by the CAMERA, because attribution is
# type-only and no actor spans a cut by default. The legs below traverse ONE
# continuous space -- brine -> cell -> protein -> skin -> evidence -> bottle
# -> shelf -> back to brine -- so consecutive units read as framings of one
# world rather than as separate slides. Planned at beat-sheet time (BRIEF.md);
# deciding this in the motion pass would mean re-authoring every unit's markup.
#
# `.stage > * {overflow:hidden}` clips the moving world AT the safe line, so a
# leg physically cannot drag ink into a reserved zone the way a translating
# push transition was measured doing (99 failed frames on the predecessor).

def cam(frm, to, at, dur=1.10, ease="power2.inOut"):
    """One camera leg on the unit's own .world wrapper."""
    def fmt(d):
        return ", ".join(f"{k}: {v}" for k, v in d.items())
    return (f"    tl.fromTo('#world', {{ {fmt(frm)} }},\n"
            f"              {{ {fmt(to)}, duration: {dur:.2f}, "
            f"ease: '{ease}' }}, {at:.3f});\n")


def phase_div(name, inner):
    """An explicit phase container. The merge pattern wants these as real
    divs, not just timeline positions -- it keeps each beat legible in the
    generated file and lets continuity-audit.py actually SEE the merge."""
    return f'<div class="phase" data-phase="{name}">{inner}</div>'


def plate(eid, klass=""):
    """A panel-scale beat surface. NOT decoration: it carries the scene's own
    kicker/label, and it changes state on a spoken turn that would otherwise
    have no visual event.

    It exists because word-scale beats do not register on this canvas. Measured
    with scripts/beat_budget.py: four mist chips on paper is 0.04 per step and
    six 26px ring squares recolouring is 0.01, against a 1.0 floor. A band of
    this size going paper->ink is 6.4. The rule the predecessor already had --
    a beat moves a panel or a column, never a word -- is the same finding.
    """
    return (f'<div class="plate {klass}" id="{eid}">'
            f'<div class="plate-fill" id="{eid}-f"></div>'
            f'<span class="plate-t" id="{eid}-t"></span></div>')


SPECS = {}


def unit(cid):
    def deco(fn):
        SPECS[cid] = fn
        return fn
    return deco


# ---- the running gag: JARGON ALARM -----------------------------------------
# Shared across 04-protein (first fire, this revision -- the retired 03-cell
# used to fire first), 05-skin (reach, no fire) and 12-bottle (retire).

ALARM_CSS = """
    .alarm { position:absolute; top:var(--s-6); left:var(--s-6); z-index:4;
             display:flex; align-items:center; gap:var(--s-3);
             padding:14px 28px; border-radius:var(--r-pill);
             background:var(--highlighter); opacity:0; transform:scale(.82);
             transform-origin:100% 0%; }
    .alarm b { font-family:var(--font-mono); font-weight:500;
               font-size:var(--t-chip); letter-spacing:var(--tr-mono-wide);
               text-transform:uppercase; color:var(--ink); white-space:nowrap; }
    .alarm i { width:18px; height:18px; border-radius:50%; background:var(--ink);
               display:block; }
"""


def alarm(eid, label="JARGON ALARM"):
    return f'<div class="alarm" id="{eid}"><i></i><b>{label}</b></div>'


def alarm_fire(eid, at, n=3):
    """Fire: a hard scale-in then a bounded pulse. The pulse is FINITE --
    repeat:{n} with a real count, never repeat:-1. An infinite repeat is
    wall-clock behaviour wearing a tween's clothes and will not seek."""
    return (f"    tl.fromTo(\'#{eid}\', {{ opacity: 0, scale: 0.82 }},\n"
            f"              {{ opacity: 1, scale: 1, duration: 0.20,\n"
            f"                 ease: \'back.out(3)\' }}, {at:.3f});\n"
            f"    tl.to(\'#{eid}\', {{ scale: 1.07, duration: 0.16, yoyo: true,\n"
            f"                      repeat: {n}, ease: \'power1.inOut\' }}, "
            f"{at + 0.22:.3f});\n")



# ===========================================================================
# CH1 -- Turn the bottle around
# ===========================================================================

@unit("01-bottle")
def _(c):
    """MERGED, 2 phases. ONE bottle actor: the front label at rest first,
    then the turn IS the bottle's own scaleX-through-zero -- the same idiom
    12-bottle used to carry, lifted here because the reveal now opens the
    video instead of arriving at 3:40.

    #world stays at the SAME rest scale every other unit opens on -- a
    global scale(1.28) baseline was tried for an "extreme close-up" framing
    and measured real (not bounding-box-false-positive) overflow: the
    two-column .bwrap grid, zoomed as a whole, pushed its right-hand panel
    ~150-160px past the canvas edge at rest, in BOTH phases. Close framing
    here comes from the bottle's own size and the hero number, not a camera
    trick -- the discrete fly-in during the turn (below) reuses 12-bottle's
    own proven-safe values (scale 1.22, x:-78, y:-26) rather than the
    untested 1.42 this first drew, which overflowed the same way.

    FRAME ZERO IS COMPOSED, not mid-fade: #ob-btl and #ob-pc are visible at
    their CSS rest state with no timeline entrance -- nothing needs to fade
    in for the payoff to be composed at t=0.

    IDs carry an ob- prefix (ob-btl, ob-pc, ob-illus, ob-inci, ob-in-N) even
    though this actor's shape is lifted from 12-bottle -- both units render
    into the same document at once, so a bare #pc / #in-10 here collided
    with 12-bottle's own ids and made every selector-based tool (this
    project's own motion sidecar included) ambiguous. Caught by `check`:
    motion_selector_ambiguous on #pc and #in-10, ERRORS not warnings.

    Also: no unit-authored ambient drift on #world. build_frames.py already
    appends a full-span ambient tween to #drift on EVERY unit -- adding a
    second one on #world's x/y fought the phase-b camera fly-in/pull-back
    for the same properties (`overlapping_gsap_tweens`, caught by `check`)
    and, worse, whichever tween GSAP resolved last was dragging the whole
    .talk2 column off-canvas at t072+1.7..+3.3 (the panel_out_of_canvas /
    canvas_overflow findings at those exact offsets). One camera driver.
    """
    t = {tid: s - c.turns[0][1] + c.ps("a") for tid, s, _ in c.turns}
    css = BASE_SPEC_CSS + """
    .bwrap { display:grid; grid-template-columns:44fr 56fr; gap:var(--s-8);
             height:100%; align-items:center; min-height:0; }
    .bottle { position:relative; margin:0 auto; width:300px; height:520px;
              border-radius:44px 44px 18px 18px; background:var(--paper);
              border:3px solid var(--rule-strong); display:flex;
              flex-direction:column; align-items:center; justify-content:center;
              gap:var(--s-4); overflow:hidden; }
    .bottle .pc { font-family:var(--font-display); font-size:120px;
                  line-height:1; margin:0; }
    .bottle .nm2 { font-family:var(--font-mono); font-size:var(--t-caption);
                   letter-spacing:var(--tr-mono-wide); color:var(--ink-2); }
    /* Anchored INSIDE .bottle -- as a loose sibling this drifted left of
       centre under the phase-b camera fly and measured off-canvas (161px)
       while the bottle itself, centred via margin:auto, never did. */
    .bottle .illus { font-family:var(--font-mono); font-size:var(--t-chip);
             letter-spacing:var(--tr-mono-wide); text-transform:uppercase;
             color:var(--ink-2); opacity:0; text-align:center; }
    .inci { list-style:none; margin:0; padding:0; display:flex;
            flex-direction:column; gap:6px; }
    .inci li { position:relative; font-family:var(--font-mono);
               font-size:22px; letter-spacing:var(--tr-mono);
               color:var(--ink-2); opacity:0; padding:5px 14px;
               border-radius:var(--r-2); }
    .inci li.hit { color:var(--ink); background:var(--highlighter); }
    .talk2 { display:flex; flex-direction:column; justify-content:center;
             gap:var(--s-4); min-height:0; }
    """
    INCI = ["Water", "Glycerin", "Panthenol", "Butylene Glycol", "Niacinamide",
            "Squalane", "Dimethicone", "Ceramide NP", "Sodium Hyaluronate",
            "Betaine", "Ectoin", "Phenoxyethanol"]
    lis = "".join(
        f'<li id="ob-in-{i}" class="{"hit" if n == "Ectoin" else ""}">'
        f'{i+1}. {n}</li>' for i, n in enumerate(INCI))
    body = stage(
        '<div class="bwrap">'
        '<div><div class="bottle" id="ob-btl">'
        '<p class="pc" id="ob-pc">11%</p>'
        '<span class="nm2">COMPLEX</span>'
        '<span class="illus" id="ob-illus">Illustrative label</span></div></div>'
        '<div class="talk2">'
        + phase_div("a", plate("op"))
        + phase_div("b", f'<ul class="inci" id="ob-inci">{lis}</ul>')
        + '</div></div>')
    tl = f"""
    // PHASE A -- "eleven percent... does that mean eleven percent ectoin?"
    // The number swells on the question; nothing else needs to move, this
    // panel IS the beat (11.3%+ of frame, mist->ink).
    tl.set('#op-t', {{ textContent: 'ELEVEN PERCENT ECTOIN?' }}, 0);
    tl.to('#ob-pc', {{ scale: 1.22, duration: 0.85, ease: 'back.out(1.5)' }},
          {t['t071'] + 0.5:.3f});
    tl.to('#op-f', {{ scaleX: 1, duration: 0.55, ease: 'expo.out' }},
          {t['t071'] + 1.0:.3f});
    tl.to('#op-t', {{ opacity: 1, duration: 0.30, ease: 'none' }},
          {t['t071'] + 1.3:.3f});
    tl.to('#op-f', {{ scaleX: 0, transformOrigin: '100% 50%', duration: 0.45,
                     ease: 'power2.in' }}, {t['t072'] - 0.5:.3f});
    tl.to('#op-t', {{ opacity: 0, duration: 0.25, ease: 'none' }},
          {t['t072'] - 0.6:.3f});
    // Collapse the whole panel, not just its fill/text -- an empty
    // min-height:150px box left sitting in the layout for the rest of the
    // unit measured as a real content-then-empty void (check-static-hold's
    // region-aware pass, 7.75-11.25s). Transform-only (opacity + scaleY) --
    // height/marginTop are layout-reflow properties that snap to integer
    // pixels under the seek-by-frame capture engine (check: gsap_non_
    // transform_motion). The now-empty box is still IN the layout, just
    // invisible, which is what the void checker actually measures.
    tl.to('#op', {{ opacity: 0, scaleY: 0, transformOrigin: '0% 0%',
                   duration: 0.30, ease: 'power2.in' }}, {t['t072'] - 0.3:.3f});

    // PHASE B -- the turn. A scaleX through zero IS the turn: one object
    // rotating, not two images swapped -- the front label recedes as the
    // INCI list (the back) appears in its place.
    tl.to('#ob-btl', {{ scaleX: 0, duration: 0.28, ease: 'power2.in' }},
          {t['t072'] + 0.3:.3f});
    tl.to('#ob-btl', {{ scaleX: 1, duration: 0.34, ease: 'power2.out' }},
          {t['t072'] + 0.60:.3f});
    // The number recedes -- it was never the ectoin percentage.
    tl.to('#ob-pc', {{ scale: 0.42, opacity: 0.45, duration: 0.60,
                      ease: 'back.inOut(1.1)' }}, {t['t072'] + 0.62:.3f});
    tl.fromTo('#ob-illus', {{ opacity: 0 }},
              {{ opacity: 0.7, duration: 0.30, ease: 'none' }},
              {t['t072'] + 0.9:.3f});
    // The list -- clip-path WIPE reveal, a mechanism drawing itself, not a
    // fade. Camera then flies to the real position: coordinate-target-zoom.
    for (var i = 0; i < 12; i++) {{
      tl.fromTo('#ob-in-' + i, {{ opacity: 0, clipPath: 'inset(0 100% 0 0)' }},
                {{ opacity: 1, clipPath: 'inset(0 0% 0 0)', duration: 0.24,
                   ease: 'power1.out' }},
                {t['t072'] + 0.55:.3f} + i * 0.05);
    }}
    tl.to('#world', {{ scale: 1.22, x: -78, y: -26, duration: 1.10,
                      ease: 'power2.inOut' }}, {t['t072'] + 1.5:.3f});
    tl.to('#world', {{ scale: 1, x: 0, y: 0, duration: 0.95,
                      ease: 'power2.inOut' }}, {t['t072'] + 2.8:.3f});
    tl.to('#ob-inci li:not(.hit)', {{ opacity: 0.28, duration: 0.60,
          stagger: 0.02, ease: 'power2.inOut' }}, {t['t072'] + 3.3:.3f});
"""
    return css, body, tl


@unit("02-origin")
def _(c):
    """MERGED, 3 phases. ONE continuous space: brine/crystal field (the
    origin) -> one cell dehydrating (the raisin) -> the molecule that
    answers it, handed to 04-protein as the same actor. Camera legs
    L0->L1->L2 across it -- the idiom the retired 03-cell used to carry,
    compressed from four phases into three because the new open only
    budgets one turn per beat.

    The salt/crystal field is the SAME group of nodes across phase a (where
    it assembles) and phase b (where it closes in on the cell) -- reused,
    not redrawn, so the actor persists exactly like [S6/A-9] asks.
    """
    a, b, cc = (c.ps(x) for x in "abc")
    t = {tid: s - c.turns[0][1] + c.ps("a") for tid, s, _ in c.turns}
    css = BASE_SPEC_CSS + """
    .cellwrap { display:grid; grid-template-columns:46fr 54fr; gap:var(--s-8);
                height:100%; align-items:center; min-height:0; }
    .cellbox { position:relative; height:100%; min-height:0;
               display:flex; align-items:center; justify-content:center; }
    .talk2 { display:flex; flex-direction:column; justify-content:center;
             gap:var(--s-4); min-height:0; }
    .nm { font-family:var(--font-display); font-style:italic;
          font-size:var(--t-frame); color:var(--paper); margin:0; opacity:0;
          line-height:var(--lh-snug); }
    .swap2 { position:relative; font-family:var(--font-mono);
             font-size:var(--t-label); letter-spacing:var(--tr-mono-wide);
             text-transform:uppercase; }
    #sw2-a { color:var(--celadon); }
    #sw2-b { color:var(--paper); position:absolute; inset:0; opacity:0; }
    """
    body = stage(
        '<div class="cellwrap">'
        '<div class="cellbox">'
        '<svg viewBox="0 0 620 620" width="100%" height="100%" aria-hidden="true">'
        '<g id="salt"></g>'
        '<ellipse id="cell" cx="310" cy="310" rx="176" ry="176" fill="#59B8AE"'
        ' opacity="0"/>'
        '<ellipse id="cyto" cx="310" cy="310" rx="132" ry="132" fill="#1B1917"'
        ' opacity="0"/>'
        '<g id="water2"></g>'
        '<text id="raisin" x="310" y="470" text-anchor="middle" fill="#C97A5C"'
        ' font-family="JetBrains Mono, monospace" font-size="30"'
        ' letter-spacing="3" opacity="0">RAISIN</text>'
        '<g id="ect" opacity="0"></g>'
        '</svg></div>'
        '<div class="talk2">'
        + phase_div("a", '<p class="nm" id="nm">Halomonas elongata</p>'
                    + say("S", "Belonged to a bacterium in extremely salty water.", "o-a", ink=True, size="52px")
                    + say("J", "Bacteria invented skincare?", "o-j", ink=True, size="46px")
                    + say("S", "Not intentionally.", "o-s2", ink=True, size="46px")
                    + cite("Environ Microbiol · 2010", "o-cite1", ink=True))
        + phase_div("b", say("S", "The salt pulls water out. A microscopic raisin.", "o-b", ink=True, size="50px")
                    + cite("Phys Chem Chem Phys · 2018", "o-cite2", ink=True))
        + phase_div("c", '<div class="swap2">'
                    '<span id="sw2-a">SKINCARE BORROWED THE MOLECULE</span>'
                    '<span id="sw2-b">MARKETING BORROWED THE DRAMA</span></div>')
        + '</div></div>', ground="ink")
    tl = f"""
    (function () {{
      // Deterministic crystal field -- golden angle, no RNG. Same group
      // persists into phase b as the antagonist closing in on the cell.
      var g = document.getElementById('salt');
      for (var i = 0; i < 40; i++) {{
        var a = i * 137.508 * Math.PI / 180, r = 200 + (i % 7) * 22;
        var s = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        var x = 310 + Math.cos(a) * r, y = 310 + Math.sin(a) * r;
        s.setAttribute('x', x - 7); s.setAttribute('y', y - 7);
        s.setAttribute('width', 14); s.setAttribute('height', 14);
        s.setAttribute('fill', '#59B8AE'); s.setAttribute('opacity', '0');
        s.setAttribute('transform', 'rotate(45 ' + x.toFixed(1) + ' ' + y.toFixed(1) + ')');
        s.id = 'sx-' + i; g.appendChild(s);
      }}
      var w2 = document.getElementById('water2');
      for (var q = 0; q < 16; q++) {{
        var aq = q * 137.508 * Math.PI / 180, rq = 24 * Math.sqrt(q);
        var cw = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        cw.setAttribute('cx', 310 + Math.cos(aq) * rq);
        cw.setAttribute('cy', 310 + Math.sin(aq) * rq);
        cw.setAttribute('r', 10); cw.setAttribute('fill', '#59B8AE');
        cw.setAttribute('opacity', '0.75'); w2.appendChild(cw);
      }}
      var e = document.getElementById('ect');
      for (var j = 0; j < 14; j++) {{
        var b2 = j * 137.508 * Math.PI / 180, r2 = 26 * Math.sqrt(j);
        var d2 = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        d2.setAttribute('cx', 310 + Math.cos(b2) * r2);
        d2.setAttribute('cy', 310 + Math.sin(b2) * r2);
        d2.setAttribute('r', 11); d2.setAttribute('fill', '#4F6B52');
        e.appendChild(d2);
      }}
    }})();

    // PHASE A -- the crystal field ASSEMBLES: 40 marks entering on a
    // sequential wavefront (index order stands in for the diagonal a real
    // grid would use -- the golden-angle placement has no rows/cols), each
    // a hard back.out(2) settle. This is the beat: 40 marks across ~30% of
    // the plate, not a word fading.
    for (var i = 0; i < 40; i++) {{
      tl.fromTo('#sx-' + i, {{ opacity: 0, scale: 0.3 }},
                {{ opacity: 0.55, scale: 1, duration: 0.30, ease: 'back.out(2)',
                   transformOrigin: 'center' }},
                {a + 0.10:.3f} + i * 0.028);
    }}
    tl.fromTo('#nm', {{ opacity: 0, y: 18 }},
              {{ opacity: 1, y: 0, duration: 0.40, ease: 'circ.out' }}, {t['t073']:.3f});
    tl.fromTo('#o-a', {{ opacity: 0, y: 22 }},
              {{ opacity: 1, y: 0, duration: 0.40, ease: 'circ.out' }},
              {t['t073'] + 0.18:.3f});
    tl.fromTo('#o-cite1', {{ opacity: 0 }},
              {{ opacity: 1, duration: 0.30, ease: 'none' }}, {t['t073'] + 1.2:.3f});
    // t002/t003 -- the two-line exchange callback, same slam idiom the
    // retired hook used for its own replies.
    tl.fromTo('#o-j', {{ opacity: 0, scale: 1.10, y: 8 }},
              {{ opacity: 1, scale: 1, y: 0, duration: 0.34,
                 ease: 'power4.out' }}, {t['t002']:.3f});
    tl.fromTo('#o-s2', {{ opacity: 0, scale: 1.10, y: 8 }},
              {{ opacity: 1, scale: 1, y: 0, duration: 0.30,
                 ease: 'power4.out' }}, {t['t003']:.3f});

    // Handover: phase A's lines leave as B's deformation begins.
    tl.to(['#nm', '#o-a', '#o-j', '#o-s2', '#o-cite1'],
          {{ opacity: 0, y: -18, duration: 0.34, ease: 'power2.in' }},
          {t['t074'] - 0.2:.3f});

    // CAMERA L0->L1 -- close on the single cell as the salt arrives.
    tl.fromTo('#world', {{ scale: 1, x: 0 }},
              {{ scale: 1.08, x: -18, duration: 2.20, ease: 'power2.inOut' }},
              {a:.3f});

    // PHASE B -- the cell DEFORMS. reactive-displacement: the actor reacts
    // to the salt rather than being replaced by a picture of a shrunken
    // cell. Salt closes in on the cell across the whole phase.
    tl.fromTo('#cell', {{ opacity: 0 }}, {{ opacity: 0.30, duration: 0.30,
              ease: 'none' }}, {b:.3f});
    tl.fromTo('#cyto', {{ opacity: 0 }}, {{ opacity: 1, duration: 0.30,
              ease: 'none' }}, {b:.3f});
    tl.fromTo('#salt', {{ scale: 1.34, transformOrigin: '310px 310px' }},
              {{ scale: 1.0, duration: {cc - b + 1.0:.3f}, ease: 'power1.inOut' }},
              {b:.3f});
    tl.to('#cell', {{ attr: {{ rx: 150, ry: 118 }}, duration: 1.10,
                     ease: 'power2.inOut' }}, {t['t074'] + 0.5:.3f});
    tl.to('#cyto', {{ attr: {{ rx: 104, ry: 82 }}, duration: 1.10,
                     ease: 'power2.inOut' }}, {t['t074'] + 0.5:.3f});
    tl.to('#water2 circle', {{ attr: {{ r: 0 }}, duration: 0.55,
                              stagger: {{ each: 0.30, from: 'random' }},
                              ease: 'power2.in' }}, {t['t074'] + 1.2:.3f});
    tl.fromTo('#raisin', {{ opacity: 0, scale: 0.7 }},
              {{ opacity: 1, scale: 1, duration: 0.38, ease: 'back.out(2.2)' }},
              {t['t074'] + 2.4:.3f});
    tl.fromTo('#o-b', {{ opacity: 0, x: -24 }},
              {{ opacity: 1, x: 0, duration: 0.34, ease: 'expo.out' }},
              {t['t074']:.3f});
    // Ectoin appears INSIDE the same cell and it recovers -- same nodes,
    // rearranged, so the recovery reads as the answer to the deformation.
    tl.to('#ect', {{ opacity: 1, duration: 0.42, ease: 'sine.out' }},
          {t['t074'] + 4.6:.3f});
    tl.to('#cell', {{ attr: {{ rx: 176, ry: 176 }}, duration: 1.25,
                     ease: 'elastic.out(1, 0.7)' }}, {t['t074'] + 4.9:.3f});
    tl.to('#cyto', {{ attr: {{ rx: 132, ry: 132 }}, duration: 1.25,
                     ease: 'elastic.out(1, 0.7)' }}, {t['t074'] + 4.9:.3f});
    tl.to('#raisin', {{ opacity: 0.25, duration: 0.60, ease: 'power1.inOut' }},
          {t['t074'] + 5.2:.3f});
    tl.fromTo('#o-cite2', {{ opacity: 0 }},
              {{ opacity: 1, duration: 0.30, ease: 'none' }}, {t['t074'] + 5.6:.3f});
    tl.to('#ect circle', {{ attr: {{ r: 15 }}, duration: 0.60, stagger: 0.05,
                           ease: 'back.out(2)' }}, {t['t074'] + 5.9:.3f});

    tl.to(['#o-b', '#o-cite2'], {{ opacity: 0, y: -18, duration: 0.32,
                                  ease: 'power2.in' }}, {t['t075'] - 0.3:.3f});

    // CAMERA L1->L2 -- push inside for the handoff to 04-protein, which
    // continues this exact leg (04-protein opens at L2->L3, x:-30).
    tl.to('#world', {{ scale: 1.16, x: -30, duration: 1.60,
                      ease: 'power2.inOut' }}, {cc:.3f});

    // PHASE C -- the close. A myth TRANSFORMS into its correction: skincare
    // borrowed the molecule fades up, then marketing borrowed the drama
    // replaces it in place -- the swap idiom, not a fade to a new card.
    tl.fromTo('#sw2-a', {{ opacity: 0, y: 20 }},
              {{ opacity: 1, y: 0, duration: 0.36, ease: 'expo.out' }},
              {t['t075']:.3f});
    tl.to('#sw2-a', {{ opacity: 0, yPercent: -60, duration: 0.30,
                      ease: 'power3.inOut' }}, {t['t075'] + 2.6:.3f});
    tl.fromTo('#sw2-b', {{ opacity: 0, yPercent: 60 }},
              {{ opacity: 1, yPercent: 0, duration: 0.30, ease: 'power3.inOut' }},
              {t['t075'] + 2.6:.3f});
    tl.to('#cell', {{ opacity: 0.46, duration: 0.80, ease: 'sine.inOut' }},
          {t['t075'] + 2.6:.3f});
"""
    return css, body, tl


@unit("04-protein")
def _(c):
    """MERGED, 5 phases. ONE protein+shell+ring actor. CH2 opener.

    This unit exists because of a specific defect in the predecessor:
    09-exclusion.html and 10-messier.html carry byte-identical geometry
    (viewBox 0 0 620 620, r 190 and 112, stroke-width 46) plus a duplicated
    ring-builder loop -- one actor drawn twice in two files, which is why that
    piece read as a sequence of resembling diagrams rather than one subject.

    Here the ring is built ONCE and REARRANGED: it closes ranks in phase c
    (the security detail), then holds a standoff gap in phase d (the actual
    point -- exclusion), then relaxes in phase e. Same nodes throughout.
    """
    t = {tid: s - c.turns[0][1] + c.ps("a") for tid, s, _ in c.turns}
    css = BASE_SPEC_CSS + ALARM_CSS + """
    .pwrap { display:grid; grid-template-columns:54fr 46fr; gap:var(--s-8);
             height:100%; align-items:center; min-height:0; }
    .pbox { position:relative; height:100%; min-height:0; display:flex;
            align-items:center; justify-content:center; }
    .talk2 { display:flex; flex-direction:column; justify-content:center;
             gap:var(--s-4); min-height:0; }
    .term { position:relative; background:var(--mist); border-radius:var(--r-3);
            padding:var(--s-6); opacity:0; }
    .term h4 { position:relative; z-index:1; margin:0 0 var(--s-2);
               font-family:var(--font-body); font-weight:800;
               font-size:var(--t-frame); letter-spacing:var(--tr-mono); }
    .term em { position:relative; z-index:1; display:block;
               font-family:var(--font-mono); font-size:var(--t-caption);
               color:var(--ink-2); letter-spacing:var(--tr-mono);
               margin-bottom:var(--s-3); font-style:normal; }
    .term p { position:relative; z-index:1; margin:0;
              font-family:var(--font-display); font-size:var(--t-body);
              line-height:var(--lh-body); }
    .swap { position:relative; font-family:var(--font-mono);
            font-size:var(--t-label); letter-spacing:var(--tr-mono-wide);
            text-transform:uppercase; }
    #sw-a { color:var(--ink-2); }
    #sw-b { color:var(--ink); position:absolute; inset:0; opacity:0; }
    """
    body = stage(
        alarm("alarm2") +
        '<div class="pwrap">'
        '<div class="pbox">'
        '<svg viewBox="0 0 620 620" width="100%" height="100%" aria-hidden="true">'
        '<circle id="shell" cx="310" cy="310" r="190" fill="none" stroke="#59B8AE"'
        ' stroke-width="46" opacity="0.30"/>'
        '<circle id="prot" cx="310" cy="310" r="112" fill="#131516"/>'
        '<g id="ring"></g>'
        '<text id="plab" x="310" y="322" text-anchor="middle" fill="#F7F5F0"'
        ' font-family="Inter, sans-serif" font-weight="800" font-size="34"'
        ' opacity="0">PROTEIN</text>'
        '</svg></div>'
        '<div class="talk2">'
        # ONE protein+shell+ring above, five phases here. The ring REARRANGES
        # between them; it is never rebuilt.
        + phase_div("a", '<div class="term" id="term">'
                    '<div class="wash aqua" id="tw"></div>'
                    '<h4>EXTREMOLYTE</h4><em>noun</em>'
                    '<p>A molecule that keeps a cell stable in conditions '
                    'that should destroy it.</p></div>')
        + phase_div("b", '<div class="swap">'
                    '<span id="sw-a">PREFERENTIAL EXCLUSION</span>'
                    '<span id="sw-b">GIVE THE PROTEIN SPACE</span></div>')
        + phase_div("c", say("S", "A celebrity, surrounded<br>by security.", "p-c", size="46px"))
        + phase_div("d", say("J", "So ectoin gives proteins<br>personal space.", "p-d", size="42px")
                    + cite("Phys Chem Chem Phys · 2018", "p-cite"))
        + phase_div("e", "")
        + '</div></div>')
    tl = f"""
    (function () {{
      // ONE ring, built once. Every later phase MOVES these same nodes.
      var g = document.getElementById('ring');
      for (var i = 0; i < 18; i++) {{
        var a = i * 20 * Math.PI / 180;
        var x = 310 + Math.cos(a) * 268, y = 310 + Math.sin(a) * 268;
        var s = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        s.setAttribute('x', x - 13); s.setAttribute('y', y - 13);
        s.setAttribute('width', 26); s.setAttribute('height', 26);
        s.setAttribute('fill', '#C97A5C'); s.setAttribute('opacity', '0');
        s.setAttribute('transform', 'rotate(45 ' + x.toFixed(1) + ' ' + y.toFixed(1) + ')');
        s.id = 'r-' + i; g.appendChild(s);
      }}
    }})();

    // PHASE A -- the gloss. This card is change 4 from SCRIPT.md: extremolyte
    // was the one technical term JAY never translated.
    tl.fromTo('#term', {{ opacity: 0, y: 28 }},
              {{ opacity: 1, y: 0, duration: 0.44, ease: 'power2.out' }}, {t['t016']:.3f});

    // CAMERA L2->L3 -- the deepest framing in the piece. Arrives on the
    // protein just as the exclusion beat lands.
    tl.fromTo('#world', {{ scale: 1.16, x: -30 }},
              {{ scale: 1.0, x: 0, duration: 1.40, ease: 'power2.inOut' }}, 0);
    tl.to('#world', {{ scale: 1.12, x: 34, duration: 1.60,
                      ease: 'power2.inOut' }}, {t['t019']:.3f});
    tl.fromTo('#tw', {{ scaleX: 0 }},
              {{ scaleX: 1, duration: 0.52, ease: 'expo.out' }}, {t['t016'] + 0.20:.3f});

    // PHASE B -- the jargon lands, the alarm fires, the ring arrives.
{alarm_fire('alarm2', t['t017'] + 4.4)}
    tl.to('#term', {{ opacity: 0, y: -20, duration: 0.34, ease: 'power2.in' }},
          {t['t017'] + 0.2:.3f});
    tl.fromTo('#ring rect', {{ opacity: 0 }},
              {{ opacity: 1, duration: 0.30, stagger: 0.035, ease: 'none' }},
              {t['t017'] + 0.6:.3f});
    tl.to('#alarm2', {{ opacity: 0, duration: 0.24, ease: 'power2.in' }},
          {t['t018'] + 0.9:.3f});

    // PHASE C -- security CLOSES RANKS. The ring moves inward toward the
    // protein: same 18 nodes, new radius. depth-scatter-assemble.
    tl.fromTo('#plab', {{ opacity: 0 }},
              {{ opacity: 1, duration: 0.30, ease: 'none' }}, {t['t019'] + 0.3:.3f});
    tl.fromTo('#p-c', {{ opacity: 0, y: 20 }},
              {{ opacity: 1, y: 0, duration: 0.36, ease: 'expo.out' }}, {t['t019']:.3f});
    tl.to('#p-c', {{ opacity: 0, y: -16, duration: 0.30, ease: 'power2.in' }},
          {t['t021'] - 0.2:.3f});
    tl.to('#ring', {{ scale: 0.72, transformOrigin: '310px 310px',
                     duration: 0.70, ease: 'back.out(1.4)' }}, {t['t019'] + 0.7:.3f});

    // t020 -- THE HYDRATION SHELL FILLS IN. This is the one genuine cadence
    // outlier left in the piece: check-cadence measured 9.12s with no visible
    // beat across 98.25-107.25s, which is t019 plus the whole of t020 -- and
    // t020 is the six-second line that explains the actual mechanism ("water
    // remains organised without clinging directly to the protein").
    //
    // Everything already in that window is word-scale and measures as nothing:
    // the ring closing ranks is 18 squares of 26px, 0.2% of frame, 0.01/step.
    // The shell is the only element here big enough to carry a beat, and
    // thickening it IS the line's content rather than decoration over it.
    //
    // Sized with scripts/beat_budget.py before authoring, not after a render:
    //   before  r190 sw46  @0.30  -> luma 218, 5.0% of frame
    //   after   r160 sw120 @0.78  -> luma 174, 11.1% of frame
    //   changed area 11.1% at mean delta ~58 over 0.65s = 1.24/step (floor 1.0)
    tl.to('#shell', {{ attr: {{ r: 160, 'stroke-width': 120 }}, opacity: 0.78,
                      duration: 0.65, ease: 'power2.inOut' }}, {t['t020'] + 0.45:.3f});
    // Settle back before t021's own shell beat so the two do not fight.
    tl.to('#shell', {{ attr: {{ r: 190, 'stroke-width': 46 }}, opacity: 0.30,
                      duration: 0.80, ease: 'power2.inOut' }}, {t['t020'] + 3.6:.3f});

    // PHASE D -- THE POINT. The ring pulls BACK to a standoff and the shell
    // thickens into the gap: ectoin is excluded from the surface and the
    // ordered water fills the space. Same nodes, third arrangement.
    tl.to('#ring', {{ scale: 0.94, duration: 0.85, ease: 'power2.inOut' }},
          {t['t021']:.3f});
    tl.to('#shell', {{ attr: {{ 'stroke-width': 78, r: 214 }}, opacity: 0.42,
                      duration: 0.90, ease: 'power2.inOut' }}, {t['t021']:.3f});
    tl.fromTo('#p-d', {{ opacity: 0, y: 20 }},
              {{ opacity: 1, y: 0, duration: 0.34, ease: 'expo.out' }}, {t['t021']:.3f});
    // The on-screen term TRANSFORMS rather than being replaced -- the second
    // state must read as the first one corrected, which a fade-out/fade-in of
    // two unrelated strings does not.
    tl.to('#sw-a', {{ opacity: 0, yPercent: -60, duration: 0.30,
                     ease: 'power3.inOut' }}, {t['t021'] + 0.5:.3f});
    tl.fromTo('#sw-b', {{ opacity: 0, yPercent: 60 }},
              {{ opacity: 1, yPercent: 0, duration: 0.30, ease: 'power3.inOut' }},
              {t['t021'] + 0.5:.3f});
    tl.fromTo('#p-cite', {{ opacity: 0 }},
              {{ opacity: 1, duration: 0.28, ease: 'none' }}, {t['t022'] + 0.3:.3f});

    // t022 -- "the actual molecular behaviour is more complicated". The tidy
    // ring DISORDERS: a third of it breaks rank inward and recolours. This is
    // the line's own content, and it was previously 6.7s of speech over a
    // still frame.
    (function () {{
      for (var i = 0; i < 18; i++) {{
        if (i % 3 !== 0) continue;
        var a = i * 20 * Math.PI / 180;
        tl.to('#r-' + i, {{ attr: {{ x: 310 + Math.cos(a) * 196 - 13,
                                    y: 310 + Math.sin(a) * 196 - 13 }},
                           fill: '#E0A32B', duration: 0.80,
                           ease: 'power2.inOut' }}, {t['t022'] + 0.6:.3f} + i * 0.045);
      }}
    }})();
    tl.to('#shell', {{ opacity: 0.16, duration: 0.80, ease: 'power2.inOut' }},
          {t['t022'] + 1.2:.3f});
    // The protein itself inverts -- 3.5% of frame at 225 luma = 1.40/step.
    // The 18 ring squares recolouring alongside it measure 0.01 and are
    // detail, not the beat.
    tl.to('#prot', {{ attr: {{ fill: '#F7F5F0' }}, duration: 0.70,
                     ease: 'power2.inOut' }}, {t['t022'] + 0.9:.3f});
    tl.to('#plab', {{ attr: {{ fill: '#131516' }}, duration: 0.70,
                     ease: 'power2.inOut' }}, {t['t022'] + 0.9:.3f});
    tl.to('#prot', {{ attr: {{ fill: '#131516' }}, duration: 0.70,
                     ease: 'power2.inOut' }}, {t['t023'] + 1.6:.3f});
    tl.to('#plab', {{ attr: {{ fill: '#F7F5F0' }}, duration: 0.70,
                     ease: 'power2.inOut' }}, {t['t023'] + 1.6:.3f});

    // PHASE E -- t023: the whole actor recomposes on JAY's summary. A rotation
    // of the ring plus the shell returning is a full-plate change, not a settle.
    tl.to('#ring', {{ scale: 1.0, rotation: 14, transformOrigin: '310px 310px',
                     duration: 1.30, ease: 'power2.inOut' }}, {t['t023']:.3f});
    tl.to('#shell', {{ opacity: 0.30, duration: 1.0, ease: 'sine.inOut' }}, {t['t023']:.3f});
    // t024 -- "I immediately regret simplifying this": the protein swells and
    // the ring scatters outward. The last turn had no beat at all before.
    tl.to('#prot', {{ attr: {{ r: 150 }}, duration: 0.70,
                     ease: 'back.out(1.6)' }}, {t['t024'] + 0.4:.3f});
    tl.to('#ring', {{ scale: 1.14, rotation: 0, duration: 0.90,
                     ease: 'power2.out' }}, {t['t024'] + 0.4:.3f});
"""
    return css, body, tl


@unit("05-skin")
def _(c):
    """MERGED, 4 phases. CH3 opener. Keratin strands + water, one actor.

    Phase c is the FORCE FIELD beat: the claim is drawn, then struck. A strike
    at PANEL scale (a full flood over the plate), not a 5px line through a
    word -- the word-scale version measures as nothing on this canvas.
    """
    t = {tid: s - c.turns[0][1] + c.ps("a") for tid, s, _ in c.turns}
    css = BASE_SPEC_CSS + ALARM_CSS + """
    .swrap { display:grid; grid-template-columns:52fr 48fr; gap:var(--s-8);
             height:100%; align-items:center; min-height:0; }
    .sbox { position:relative; height:100%; min-height:0; }
    .talk2 { display:flex; flex-direction:column; justify-content:center;
             gap:var(--s-4); min-height:0; }
    .ff { position:relative; background:var(--mist); border-radius:var(--r-3);
          padding:var(--s-4) var(--s-5); opacity:0; overflow:hidden; }
    .ff span { position:relative; z-index:1; font-family:var(--font-body);
               font-weight:800; font-size:var(--t-frame); }
    .verdict { position:relative; background:var(--mist);
               border-radius:var(--r-3); padding:var(--s-5); opacity:0; }
    .verdict span { position:relative; z-index:1;
                    font-family:var(--font-display); font-size:var(--t-frame);
                    line-height:var(--lh-snug); }
    """
    body = stage(
        alarm("alarm3") +
        '<div class="swrap">'
        '<div class="sbox">'
        '<svg viewBox="0 0 620 620" width="100%" height="100%" aria-hidden="true">'
        '<g id="strands"></g><g id="water"></g></svg></div>'
        '<div class="talk2">'
        + phase_div("a", say("S", "Keratin, and how it<br>holds water.", "k-a", size="48px")
                    + cite("Biochem Biophys Rep · 2021", "k-cite"))
        + phase_div("b", "")
        + phase_div("c", '<div class="ff" id="ff"><div class="void" id="ffx"></div>'
                    '<span>AN INVISIBLE FORCE FIELD</span></div>'
                    + say("J", "Finally, realistic boundaries.", "k-c", size="42px"))
        + phase_div("d", '<div class="verdict" id="vd">'
                    '<div class="wash aqua" id="vw"></div>'
                    '<span>Support for the barrier. Not body armour.</span></div>')
        + '</div></div>')
    tl = f"""
    (function () {{
      var g = document.getElementById('strands'), w = document.getElementById('water');
      for (var i = 0; i < 22; i++) {{
        var y = 70 + i * 22;
        var p = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        p.setAttribute('d', 'M 40 ' + y + ' Q 310 ' + (y - 16) + ' 580 ' + y);
        p.setAttribute('stroke', '#6F8F72'); p.setAttribute('stroke-width', '7');
        p.setAttribute('fill', 'none'); p.setAttribute('stroke-linecap', 'round');
        p.id = 'st-' + i; g.appendChild(p);
      }}
      for (var j = 0; j < 26; j++) {{
        var a = j * 137.508 * Math.PI / 180, r = 30 * Math.sqrt(j);
        var d = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        d.setAttribute('cx', 310 + Math.cos(a) * r * 1.5);
        d.setAttribute('cy', 310 + Math.sin(a) * r);
        d.setAttribute('r', 9); d.setAttribute('fill', '#59B8AE');
        d.setAttribute('opacity', '0'); w.appendChild(d);
      }}
      // svg-path-draw: dash the strands so they can be DRAWN, not faded.
      var ps = g.querySelectorAll('path');
      for (var k = 0; k < ps.length; k++) {{
        var L = ps[k].getTotalLength();
        ps[k].style.strokeDasharray = L; ps[k].style.strokeDashoffset = L;
      }}
    }})();

    // PHASE A -- draw the strands. ease 'none' is correct for a draw: a path
    // revealing at constant rate reads as being drawn; an eased one reads as
    // sliding.
    tl.to('#strands path', {{ strokeDashoffset: 0, duration: 0.90,
                             stagger: 0.026, ease: 'none' }}, {t['t025']:.3f});

    // CAMERA L3->L2' -- pull back out of the molecule to the skin surface.
    tl.fromTo('#world', {{ scale: 1.12, x: 34 }},
              {{ scale: 1.0, x: 0, duration: 1.80, ease: 'power2.inOut' }}, 0);
    tl.to('#water circle', {{ opacity: 0.85, duration: 0.40, stagger: 0.018,
                             ease: 'sine.out' }}, {t['t025'] + 1.4:.3f});
    tl.fromTo('#k-a', {{ opacity: 0, y: 20 }},
              {{ opacity: 1, y: 0, duration: 0.38, ease: 'power2.out' }}, {t['t025']:.3f});
    tl.fromTo('#k-cite', {{ opacity: 0 }},
              {{ opacity: 1, duration: 0.28, ease: 'none' }}, {t['t025'] + 2.2:.3f});
    // t025 runs 8.65s and previously spent ~7 of them on a still frame. The
    // strands now MOVE through the rest of the line -- water working into the
    // keratin, which is what the sentence describes.
    tl.to('#strands path', {{ attr: {{ 'stroke-width': 11 }}, duration: 1.20,
          stagger: 0.035, ease: 'sine.inOut' }}, {t['t025'] + 3.4:.3f});
    tl.to('#water circle', {{ attr: {{ r: 14 }}, duration: 1.10, stagger: 0.03,
          ease: 'back.out(1.8)' }}, {t['t025'] + 5.2:.3f});
    // t026/t027/t028 -- the exchange where SOULHABIT self-translates. The
    // field settles to a calmer state on the plain-language version.
    tl.to('#strands path', {{ attr: {{ 'stroke-width': 7 }}, duration: 1.00,
          stagger: 0.03, ease: 'power2.inOut' }}, {t['t026'] + 0.4:.3f});
    tl.to('#water circle', {{ attr: {{ r: 11 }}, opacity: 0.9, duration: 0.90,
          stagger: 0.02, ease: 'power2.inOut' }}, {t['t027'] + 0.2:.3f});
    tl.to('#strands path', {{ attr: {{ stroke: '#4F6B52' }}, duration: 0.80,
          stagger: 0.025, ease: 'none' }}, {t['t028'] + 0.1:.3f});
    // JAY reaches for the alarm; SOULHABIT self-corrects before it fires. The
    // gag is that it ALMOST goes off -- it appears, then retreats.
    tl.fromTo('#alarm3', {{ opacity: 0, scale: 0.82, x: 40 }},
              {{ opacity: 0.75, scale: 0.94, x: 0, duration: 0.30,
                 ease: 'power2.out' }}, {t['t025'] + 3.4:.3f});
    tl.to('#alarm3', {{ opacity: 0, x: 40, duration: 0.34, ease: 'power2.in' }},
          {t['t026'] + 0.2:.3f});

    // PHASE C -- the claim is drawn, then STRUCK at panel scale.
    tl.fromTo('#ff', {{ opacity: 0, y: 22 }},
              {{ opacity: 1, y: 0, duration: 0.34, ease: 'power2.out' }}, {t['t029']:.3f});
    tl.to('#ffx', {{ opacity: 0.90, duration: 0.24, ease: 'power3.in' }}, {t['t030']:.3f});
    tl.to('#water circle', {{ opacity: 0.25, duration: 0.50, ease: 'power2.in' }},
          {t['t030']:.3f});
    tl.fromTo('#k-c', {{ opacity: 0, y: 18 }},
              {{ opacity: 1, y: 0, duration: 0.32, ease: 'expo.out' }}, {t['t031']:.3f});

    // PHASE D -- the honest framing, on a wash. aqua + --ink is 7.76:1.
    tl.to(['#ff', '#k-c'], {{ opacity: 0, y: -16, duration: 0.32,
                             ease: 'power2.in' }}, {t['t032'] - 0.2:.3f});
    tl.fromTo('#vd', {{ opacity: 0, y: 24 }},
              {{ opacity: 1, y: 0, duration: 0.38, ease: 'power2.out' }}, {t['t032']:.3f});
    tl.fromTo('#vw', {{ scaleX: 0 }},
              {{ scaleX: 1, duration: 0.55, ease: 'expo.out' }}, {t['t032'] + 0.18:.3f});
    tl.to('#water circle', {{ opacity: 0.85, duration: 0.60, ease: 'sine.out' }},
          {t['t032'] + 0.3:.3f});
"""
    return css, body, tl


@unit("06-trial104")
def _(c):
    """CH4 opener. counting-dynamic-scale + a real 104-unit cohort grid.

    The choreography enacts the study's own structure: 104 dots, because n=104;
    they split into the two arms the trial actually had. That is what makes an
    evidence beat explanatory rather than decorative.
    """
    t = {tid: s - c.turns[0][1] for tid, s, _ in c.turns}
    css = BASE_SPEC_CSS + """
    .twrap { display:grid; grid-template-rows:auto 1fr auto; height:100%;
             gap:var(--s-6); min-height:0; }
    .big { font-family:var(--font-display); font-size:200px; line-height:1;
           letter-spacing:var(--tr-display); margin:0; }
    .cohort { display:grid; grid-template-columns:repeat(26,1fr); gap:10px;
              align-content:center; min-height:0; }
    .cohort i { display:block; width:100%; aspect-ratio:1; border-radius:50%;
                background:var(--ink-3); opacity:0; }
    .cohort i.on { background:var(--aqua); }
    .foot { display:flex; align-items:flex-end; justify-content:space-between;
            gap:var(--s-6); }
    """
    body = stage(
        '<div class="twrap">'
        '<div><p class="kicker" id="tk">ONE STUDY</p>'
        '<p class="big" id="num">0</p></div>'
        '<div class="cohort" id="coh"></div>'
        '<div class="foot">'
        + say("S", "They preferred the 2% version.", "e-a", size="54px")
        + cite("Skin Pharmacol Physiol · 2007", "e-cite")
        + '</div></div>')
    tl = f"""
    (function () {{
      var g = document.getElementById('coh');
      for (var i = 0; i < 104; i++) {{
        var e = document.createElement('i');
        e.id = 'c-' + i; g.appendChild(e);
      }}
    }})();
    tl.fromTo('#tk', {{ opacity: 0 }}, {{ opacity: 1, duration: 0.26, ease: 'none' }}, {t['t033']:.3f});

    // CAMERA L2'->L1' -- widen onto the evidence plane. A chapter opener,
    // so the leg carries the boundary as well as the wipe.
    tl.fromTo('#world', {{ scale: 1.10 }},
              {{ scale: 1.0, duration: 1.50, ease: 'power2.out' }}, 0);
    // Seek-safe count-up: a tween on a proxy object with onUpdate writing the
    // numeral. Any seek reproduces the same frame; a setInterval would not.
    (function () {{
      var o = {{ v: 0 }}, el = document.getElementById('num');
      tl.to(o, {{ v: 104, duration: 1.15, ease: 'power1.out',
                 onUpdate: function () {{ el.textContent = Math.round(o.v); }} }},
            {t['t033'] + 0.25:.3f});
    }})();
    // 104 dots arrive as ONE field -- a 26-wide grid crossing most of the
    // frame, which is the beat. Individually they are invisible to any metric.
    tl.to('#coh i', {{ opacity: 1, duration: 0.30, stagger: 0.006,
                      ease: 'none' }}, {t['t033'] + 0.35:.3f});
    // Then the arms separate: this is the trial's own structure, not decoration.
    (function () {{
      for (var i = 0; i < 104; i++) {{
        if (i % 2 === 0) document.getElementById('c-' + i).classList.add('on');
      }}
    }})();
    tl.fromTo('#coh i.on', {{ scale: 1 }},
              {{ scale: 1.32, duration: 0.55, stagger: 0.004,
                 ease: 'back.out(2)' }}, {t['t034']:.3f});
    tl.fromTo('#e-a', {{ opacity: 0, y: 20 }},
              {{ opacity: 1, y: 0, duration: 0.36, ease: 'power2.out' }}, {t['t034']:.3f});
    tl.fromTo('#e-cite', {{ opacity: 0 }},
              {{ opacity: 1, duration: 0.28, ease: 'none' }}, {t['t034'] + 0.6:.3f});
"""
    return css, body, tl


@unit("07-preference")
def _(c):
    """LIKED IT BETTER != MEASURED CHANGE. A card-morph, not a replace.

    Two states of ONE card. Fading card A out and card B in would tell the
    viewer two unrelated things happened; keeping the anchor makes the second
    state read as the first one qualified, which is the whole beat.
    """
    t = {tid: s - c.turns[0][1] for tid, s, _ in c.turns}
    css = BASE_SPEC_CSS + """
    .pcol { display:flex; flex-direction:column; justify-content:center;
            height:100%; gap:var(--s-6); min-height:0; }
    .claim { position:relative; background:var(--mist); border-radius:var(--r-3);
             padding:var(--s-7); overflow:hidden; }
    .claim span { position:relative; z-index:1; display:block;
                  font-family:var(--font-body); font-weight:800;
                  font-size:74px; line-height:var(--lh-snug); }
    .claim small { position:relative; z-index:1; display:block;
                   margin-top:var(--s-4); font-family:var(--font-display);
                   font-size:var(--t-body); color:var(--ink-2); opacity:0; }
    """
    body = stage(
        '<div class="pcol">'
        '<div class="claim" id="cl"><div class="wash aqua" id="cw"></div>'
        '<span id="cl-t">THEY LIKED IT BETTER</span>'
        '<small id="cl-s">That is a real result. It is not a machine measuring '
        'a change in their skin.</small></div>'
        + say("J", "Preference, not Cinderella.", "pr-j", size="56px")
        + '</div>')
    tl = f"""
    tl.fromTo('#cl', {{ opacity: 0, y: 30 }},
              {{ opacity: 1, y: 0, duration: 0.40, ease: 'power2.out' }}, {t['t035']:.3f});
    // The wash sweeps the WHOLE card -- mist 240 -> aqua 178 across ~22% of
    // frame. That is the beat; the text arriving is not.
    tl.fromTo('#cw', {{ scaleX: 0 }},
              {{ scaleX: 1, duration: 0.58, ease: 'expo.out' }}, {t['t036']:.3f});
    // Same card, qualified. The anchor stays, so this reads as a correction.
    tl.to('#cl-t', {{ scale: 0.72, transformOrigin: '0% 50%', duration: 0.45,
                     ease: 'back.inOut(1.2)' }}, {t['t036'] + 0.5:.3f});
    tl.to('#cl-s', {{ opacity: 1, duration: 0.40, ease: 'sine.out' }},
          {t['t036'] + 0.7:.3f});
    tl.fromTo('#pr-j', {{ opacity: 0, x: -30 }},
              {{ opacity: 1, x: 0, duration: 0.34, ease: 'circ.out' }}, {t['t037']:.3f});
"""
    return css, body, tl


@unit("08-eczema")
def _(c):
    """stat-bars-and-fills. Two arms, level -- because the finding IS level."""
    t = {tid: s - c.turns[0][1] for tid, s, _ in c.turns}
    css = BASE_SPEC_CSS + """
    .ewrap { display:grid; grid-template-rows:auto 1fr auto; height:100%;
             gap:var(--s-6); min-height:0; }
    .bars { display:grid; grid-template-columns:1fr 1fr; gap:var(--s-6);
            align-items:end; min-height:0; }
    .bar { position:relative; display:flex; flex-direction:column;
           justify-content:flex-end; height:100%; min-height:0; }
    .bar .f { transform:scaleY(0); transform-origin:50% 100%;
              border-radius:var(--r-3) var(--r-3) 0 0; }
    .bar .f.a { background:var(--aqua); height:62%; }
    .bar .f.b { background:var(--ink-3); height:62%; }
    .bar b { display:block; margin-top:var(--s-4); font-family:var(--font-mono);
             font-size:var(--t-chip); letter-spacing:var(--tr-mono);
             text-transform:uppercase; color:var(--ink-2); opacity:0; }
    .head { display:flex; align-items:baseline; gap:var(--s-5); }
    .head p.big { font-family:var(--font-display); font-size:150px;
                  line-height:1; margin:0; }
    """
    body = stage(
        '<div class="ewrap">'
        '<div class="head"><p class="big" id="n65">65</p>'
        '<p class="kicker" id="wk">PEOPLE · MILD TO MODERATE ECZEMA · 4 WEEKS</p></div>'
        '<div class="bars">'
        '<div class="bar"><div class="f a" id="fa"></div><b id="la">ECTOIN CREAM</b></div>'
        '<div class="bar"><div class="f b" id="fb"></div><b id="lb">BARRIER CREAM</b></div>'
        '</div>'
        '<div class="head" style="justify-content:space-between">'
        + say("S", "About as well. And well tolerated.", "ez", size="50px")
        + cite("Skin Pharmacol Physiol · 2013", "ez-cite")
        + '</div>' + plate("epl") + '</div>')
    tl = f"""
    (function () {{
      var o = {{ v: 0 }}, el = document.getElementById('n65');
      tl.to(o, {{ v: 65, duration: 0.85, ease: 'power1.out',
                 onUpdate: function () {{ el.textContent = Math.round(o.v); }} }},
            {t['t038']:.3f});
    }})();
    tl.fromTo('#wk', {{ opacity: 0 }}, {{ opacity: 1, duration: 0.26, ease: 'none' }},
              {t['t038'] + 0.5:.3f});
    // Both bars rise TOGETHER and land level. The choreography is the finding:
    // an equivalence result should not animate as a race one side wins.
    tl.to('#fa', {{ scaleY: 1, duration: 0.95, ease: 'power2.inOut' }}, {t['t038'] + 1.5:.3f});
    tl.to('#fb', {{ scaleY: 1, duration: 0.95, ease: 'power2.inOut' }}, {t['t038'] + 1.5:.3f});
    tl.to('#la', {{ opacity: 1, duration: 0.30, ease: 'none' }}, {t['t038'] + 2.3:.3f});
    tl.to('#lb', {{ opacity: 1, duration: 0.30, ease: 'none' }}, {t['t038'] + 2.3:.3f});
    tl.fromTo('#ez', {{ opacity: 0, y: 18 }},
              {{ opacity: 1, y: 0, duration: 0.34, ease: 'power2.out' }}, {t['t038'] + 3.2:.3f});
    tl.fromTo('#ez-cite', {{ opacity: 0 }},
              {{ opacity: 1, duration: 0.26, ease: 'none' }}, {t['t038'] + 3.6:.3f});
    // t038 runs 14.5s; everything above lands in its first 4. This carries the
    // clause that actually matters -- equivalence, not superiority.
    tl.set('#epl-t', {{ textContent: 'ABOUT AS WELL. WELL TOLERATED.' }}, 0);
    tl.to('#epl-f', {{ scaleX: 1, duration: 0.60, ease: 'expo.out' }}, {t['t038'] + 6.2:.3f});
    tl.to('#epl-t', {{ opacity: 1, duration: 0.30, ease: 'none' }}, {t['t038'] + 6.5:.3f});
"""
    return css, body, tl


@unit("09-miracle")
def _(c):
    """Promising? Yes. Miracle? No. Four slams on an ink ground.

    The two answers get OPPOSITE treatments -- aqua flood for yes, coral void
    for no -- so the beat carries the meaning rather than repeating a shape.
    """
    t = {tid: s - c.turns[0][1] for tid, s, _ in c.turns}
    css = BASE_SPEC_CSS + """
    .qa { display:grid; grid-template-columns:1fr 1fr; gap:var(--s-8);
          height:100%; align-items:center; min-height:0; }
    .card { position:relative; border-radius:var(--r-3); padding:var(--s-7);
            background:var(--ink-soft); overflow:hidden; opacity:0;
            min-height:340px; display:flex; flex-direction:column;
            justify-content:center; gap:var(--s-4); }
    .card q { position:relative; z-index:1; font-family:var(--font-body);
              font-weight:800; font-size:var(--t-frame); color:var(--coral);
              quotes:none; }
    .card strong { position:relative; z-index:1; font-family:var(--font-display);
                   font-size:130px; line-height:1; color:var(--paper); }
    """
    body = stage(
        '<div class="qa">'
        '<div class="card" id="q1"><div class="wash moss" id="w1"></div>'
        '<q>Promising?</q><strong>Yes.</strong></div>'
        '<div class="card" id="q2"><div class="void" id="v2"></div>'
        '<q>Miracle?</q><strong>No.</strong></div>'
        '</div>', ground="ink")
    tl = f"""
    tl.fromTo('#q1', {{ opacity: 0, scale: 1.06 }},
              {{ opacity: 1, scale: 1, duration: 0.30, ease: 'power4.out' }}, {t['t039']:.3f});
    // YES gets a moss wash -- paper on moss is 5.42:1, one of the two safe
    // pairings. Full card, so it clears the area floor.
    tl.fromTo('#w1', {{ scaleX: 0 }},
              {{ scaleX: 1, duration: 0.44, ease: 'expo.out' }}, {t['t040']:.3f});
    tl.fromTo('#q2', {{ opacity: 0, scale: 1.06 }},
              {{ opacity: 1, scale: 1, duration: 0.30, ease: 'power4.out' }}, {t['t041']:.3f});
    // NO gets a coral void -- the strike, not a wash. Opposite treatment for
    // the opposite answer.
    tl.to('#v2', {{ opacity: 0.92, duration: 0.22, ease: 'power3.in' }}, {t['t042']:.3f});
"""
    return css, body, tl


@unit("10-notprove")
def _(c):
    """Three claims struck at panel scale, then the funding disclosure.

    bitop AG renders as PLAIN CONTENT, never as a citation pill -- it is an
    author affiliation being reported, not a source vouching for the claim.
    """
    t = {tid: s - c.turns[0][1] for tid, s, _ in c.turns}
    css = BASE_SPEC_CSS + """
    .nwrap { display:grid; grid-template-rows:auto 1fr auto; height:100%;
             gap:var(--s-6); min-height:0; }
    .claims { display:grid; grid-template-columns:repeat(3,1fr); gap:var(--s-5);
              min-height:0; }
    .cx { position:relative; background:var(--mist); border-radius:var(--r-3);
          padding:var(--s-6); display:flex; align-items:center;
          justify-content:center; overflow:hidden; opacity:0; }
    .cx span { position:relative; z-index:1; text-align:center;
               font-family:var(--font-body); font-weight:800;
               font-size:var(--t-frame); line-height:var(--lh-snug); }
    .fund { position:relative; border-radius:var(--r-3); padding:var(--s-6);
            background:var(--mist); overflow:hidden; opacity:0; }
    .fund span { position:relative; z-index:1; font-family:var(--font-display);
                 font-size:var(--t-body); line-height:var(--lh-body); }
    .fund b { position:relative; z-index:1; font-family:var(--font-mono);
              font-size:var(--t-chip); letter-spacing:var(--tr-mono); }
    """
    body = stage(
        '<div class="nwrap">'
        '<p class="kicker" id="nk">IT DOES NOT PROVE</p>'
        '<div class="claims">'
        '<div class="cx" id="x1"><div class="void" id="xv1"></div><span>CURES<br>ECZEMA</span></div>'
        '<div class="cx" id="x2"><div class="void" id="xv2"></div><span>REVERSES<br>AGEING</span></div>'
        '<div class="cx" id="x3"><div class="void" id="xv3"></div><span>REPLACES<br>TREATMENT</span></div>'
        '</div>'
        '<div class="fund" id="fu"><div class="wash dim" id="fw"></div>'
        '<span id="fu-a">The evidence is limited, and some of it is authored by </span>'
        '<b>bitop AG</b><span> &mdash; a company that sells the ingredient.</span>'
        '</div></div>')
    tl = f"""
    // COMPOSED AT t=0 -- same reason as 13-kbeauty. data-start IS the seam, so
    // this scene's t=0 is the first frame of its own reveal. The kicker plus a
    // 0.25/0.47/0.69 card stagger against a 0.45s wipe uncovered empty paper:
    // the midpoint frame measured 1.30% ink, 0.24x the median and the second
    // thinnest in the piece. A LEFT wipe reveals from the right, so #x3 -- the
    // card that entered LAST -- is the one uncovered FIRST.
    //
    // The stagger is not missed. It was three --mist cards on --paper, a ~5
    // luma step that carries no beat, and the scene's real beat is the STRIKE
    // sequence below, which is untouched. Three claims standing and then struck
    // reads better than three arriving and then struck.
    tl.set('#nk', {{ opacity: 1 }}, 0);
    ['x1','x2','x3'].forEach(function (id) {{
      tl.set('#' + id, {{ opacity: 1, y: 0 }}, 0);
    }});
    // Struck in sequence, each a full card. power3.in makes the strike land
    // rather than drift -- a strike that eases out reads as an appearance.
    ['xv1','xv2','xv3'].forEach(function (id, i) {{
      tl.to('#' + id, {{ opacity: 0.90, duration: 0.20, ease: 'power3.in' }},
            {t['t043'] + 1.5:.3f} + i * 0.26);
    }});
    tl.fromTo('#fu', {{ opacity: 0, y: 24 }},
              {{ opacity: 1, y: 0, duration: 0.36, ease: 'power2.out' }}, {t['t044']:.3f});
    tl.fromTo('#fw', {{ scaleX: 0 }},
              {{ scaleX: 1, duration: 0.60, ease: 'expo.out' }}, {t['t044'] + 0.3:.3f});
"""
    return css, body, tl


@unit("11-twelve")
def _(c):
    """Twelve trials. The tiles are the count, and they SORT by what they study.

    Verified 2026-09-02: PubMed `ectoine AND Clinical Trial[pt]` returns 12.
    Four of the twelve are not skin studies at all (eye spray, nasal spray,
    throat lozenges, an inhaled formulation), which is why the tiles carry a
    subject and can separate. The number on screen is the query's count, and
    the pill carries the year because it is a LIVE number.

    NOTE t048 ("none of it passed peer review") is retained by operator
    decision and is FALSE. It gets no on-screen treatment at all -- no text,
    no pill, no card. See BRIEF.md.
    """
    t = {tid: s - c.turns[0][1] for tid, s, _ in c.turns}
    css = BASE_SPEC_CSS + """
    .twrap { display:grid; grid-template-rows:auto 1fr auto; height:100%;
             gap:var(--s-6); min-height:0; }
    .tiles { display:grid; grid-template-columns:repeat(4,1fr);
             grid-template-rows:repeat(3,1fr); gap:var(--s-4); min-height:0; }
    .tile { position:relative; background:var(--mist); border-radius:var(--r-2);
            display:flex; align-items:center; justify-content:center;
            opacity:0; overflow:hidden; }
    .tile span { position:relative; z-index:1; font-family:var(--font-mono);
                 font-size:var(--t-caption); letter-spacing:var(--tr-mono);
                 text-transform:uppercase; color:var(--ink-2);
                 text-align:center; padding:0 var(--s-3); }
    .head2 { display:flex; align-items:baseline; gap:var(--s-5); }
    .head2 .big { font-family:var(--font-display); font-size:170px;
                  line-height:1; margin:0; }
    """
    SUBJ = ["SKIN", "SKIN", "SKIN", "SKIN", "SKIN", "SKIN", "SKIN", "SKIN",
            "EYES", "NOSE", "THROAT", "LUNGS"]
    tiles = "".join(
        f'<div class="tile" id="tl-{i}"><div class="wash dim" id="tw-{i}"></div>'
        f'<span>{s}</span></div>' for i, s in enumerate(SUBJ))
    body = stage(
        '<div class="twrap">'
        '<div class="head2"><p class="big" id="n12">0</p>'
        '<p class="kicker" id="tk2">CLINICAL TRIALS, ALL YEARS</p></div>'
        f'<div class="tiles">{tiles}</div>'
        '<div class="head2" style="justify-content:space-between">'
        + say("S", "Twelve. Four of them are not about skin.", "tw-s", size="50px")
        + cite("PubMed · 2026", "tw-cite")
        + '</div></div>')
    tl = f"""
    (function () {{
      var o = {{ v: 0 }}, el = document.getElementById('n12');
      tl.to(o, {{ v: 12, duration: 0.70, ease: 'power1.out',
                 onUpdate: function () {{ el.textContent = Math.round(o.v); }} }},
            {t['t046']:.3f});
    }})();
    tl.fromTo('#tk2', {{ opacity: 0 }}, {{ opacity: 1, duration: 0.24, ease: 'none' }},
              {t['t046'] + 0.3:.3f});
    for (var i = 0; i < 12; i++) {{
      tl.fromTo('#tl-' + i, {{ opacity: 0, scale: 0.86 }},
                {{ opacity: 1, scale: 1, duration: 0.26, ease: 'back.out(2)' }},
                {t['t046'] + 0.35:.3f} + i * 0.055);
    }}
    // The four non-skin trials wash out. This is the honest limitation beat
    // and it is a real measurement, not a rhetorical flourish: four of the
    // twelve study the eyes, nose, throat and lungs.
    for (var j = 8; j < 12; j++) {{
      tl.fromTo('#tw-' + j, {{ scaleX: 0 }},
                {{ scaleX: 1, duration: 0.34, ease: 'expo.out' }},
                {t['t047'] + 0.9:.3f} + (j - 8) * 0.13);
    }}
    tl.fromTo('#tw-s', {{ opacity: 0, y: 18 }},
              {{ opacity: 1, y: 0, duration: 0.32, ease: 'power2.out' }},
              {t['t047'] + 0.9:.3f});
    tl.fromTo('#tw-cite', {{ opacity: 0 }},
              {{ opacity: 1, duration: 0.26, ease: 'none' }}, {t['t046'] + 1.4:.3f});
"""
    return css, body, tl


@unit("12-bottle")
def _(c):
    """MERGED, 2 phases this revision (was 4). CH5 opener. ONE bottle, ALREADY
    turned -- the front-label reveal (11% -> it's a blend -> turn it around)
    now opens the video at 01-bottle, so this unit does not repeat it. What's
    left: who ectoin is for (phase a), then the CAMERA doing the work to find
    ectoin's real INCI position (phase d) -- the wide shot the open only
    glimpsed close up. Phases b/c (the turn itself) are retired; #pc renders
    at rest already-shrunk, because we are looking at the SAME bottle from
    the open, now turned around for the rest of this section.
    """
    t = {tid: s - c.turns[0][1] + c.ps("a") for tid, s, _ in c.turns}
    css = BASE_SPEC_CSS + ALARM_CSS + """
    .bwrap { display:grid; grid-template-columns:44fr 56fr; gap:var(--s-8);
             height:100%; align-items:center; min-height:0; }
    .bottle { position:relative; margin:0 auto; width:300px; height:520px;
              border-radius:44px 44px 18px 18px; background:var(--paper);
              border:3px solid var(--rule-strong); display:flex;
              flex-direction:column; align-items:center; justify-content:center;
              gap:var(--s-4); overflow:hidden; }
    .bottle .pc { font-family:var(--font-display); font-size:120px;
                  line-height:1; margin:0; transform:scale(.42); opacity:.45; }
    .bottle .nm2 { font-family:var(--font-mono); font-size:var(--t-caption);
                   letter-spacing:var(--tr-mono-wide); color:var(--ink-2); }
    /* Anchored INSIDE .bottle -- as a loose sibling it drifted off-centre
       under this unit's own phase-d camera fly and measured off-canvas
       (up to 183px) while the bottle itself, centred via margin:auto,
       never did. Same fix as 01-bottle. */
    .bottle .illus { font-family:var(--font-mono); font-size:var(--t-chip);
             letter-spacing:var(--tr-mono-wide); text-transform:uppercase;
             color:var(--ink-2); opacity:.7; text-align:center; }
    .inci { list-style:none; margin:0; padding:0; display:flex;
            flex-direction:column; gap:6px; }
    .states, .pairs { display:grid; grid-template-columns:repeat(2,1fr);
                      gap:var(--s-3); }
    .st, .pr { opacity:0; text-align:center; padding:var(--s-4) var(--s-3);
               border-radius:var(--r-2); font-family:var(--font-mono);
               font-size:var(--t-chip); letter-spacing:var(--tr-mono);
               color:var(--ink); background:var(--mist); }
    .pr { border-radius:var(--r-pill); }
    .inci li { position:relative; font-family:var(--font-mono);
               font-size:22px; letter-spacing:var(--tr-mono);
               color:var(--ink-2); opacity:0; padding:5px 14px;
               border-radius:var(--r-2); }
    .inci li.hit { color:var(--ink); background:var(--highlighter); }
    .talk2 { display:flex; flex-direction:column; justify-content:center;
             gap:var(--s-4); min-height:0; }
    """
    INCI = ["Water", "Glycerin", "Panthenol", "Butylene Glycol", "Niacinamide",
            "Squalane", "Dimethicone", "Ceramide NP", "Sodium Hyaluronate",
            "Betaine", "Ectoin", "Phenoxyethanol"]
    lis = "".join(
        f'<li id="in-{i}" class="{"hit" if n == "Ectoin" else ""}">'
        f'{i+1}. {n}</li>' for i, n in enumerate(INCI))
    body = stage(
        alarm("alarm4") +
        '<div class="bwrap">'
        '<div><div class="bottle" id="btl">'
        '<p class="pc" id="pc">11%</p>'
        '<span class="nm2">COMPLEX</span>'
        '<span class="illus">Illustrative label</span></div></div>'
        '<div class="talk2">'
        # ONE bottle above, already turned; the CAMERA does the work across
        # these two remaining phases.
        + phase_div("a", '<div class="states">'
                    '<span class="st" id="st1">DRY</span>'
                    '<span class="st" id="st2">SENSITIVE</span>'
                    '<span class="st" id="st3">OVER-CLEANSED</span>'
                    '<span class="st" id="st4">IRRITATED</span></div>'
                    '<div class="pairs">'
                    '<span class="pr" id="pr1">PANTHENOL</span>'
                    '<span class="pr" id="pr2">GLYCERIN</span>'
                    '<span class="pr" id="pr3">SQUALANE</span>'
                    '<span class="pr" id="pr4">CERAMIDES</span></div>'
                    + plate("bpl"))
        + phase_div("d", f'<ul class="inci" id="inci">{lis}</ul>')
        + '</div></div>')
    tl = f"""
    // PHASE A -- the front label already sits shrunk (#pc rest state); this
    // bottle is the SAME one from the open, turned around. Who it's for.
    tl.fromTo('#btl', {{ opacity: 0, y: 30 }},
              {{ opacity: 1, y: 0, duration: 0.42, ease: 'power2.out' }}, {t['t049']:.3f});
    // t049 -- the four states arrive across the line, not all at its start.
    ['st1','st2','st3','st4'].forEach(function (id, i) {{
      tl.fromTo('#' + id, {{ opacity: 0, y: 26 }},
                {{ opacity: 1, y: 0, duration: 0.34, ease: 'back.out(1.6)' }},
                {t['t049'] + 1.4:.3f} + i * 1.30);
    }});
    // t050 -- the pairings.
    ['pr1','pr2','pr3','pr4'].forEach(function (id, i) {{
      tl.fromTo('#' + id, {{ opacity: 0, scale: 0.8 }},
                {{ opacity: 1, scale: 1, duration: 0.30, ease: 'back.out(2.2)' }},
                {t['t050'] + 0.5:.3f} + i * 1.15);
    }});
    // One panel-scale beat across phase a. The chips above are detail
    // (0.04/step); this is the beat -- was two cycles when phase a/b ran
    // into the turn; the second cycle ("TURN IT AROUND") retired with b/c.
    tl.set('#bpl-t', {{ textContent: 'DRY. SENSITIVE. OVER-CLEANSED.' }}, 0);
    tl.to('#bpl-f', {{ scaleX: 1, duration: 0.60, ease: 'expo.out' }}, {t['t049'] + 4.4:.3f});
    tl.to('#bpl-t', {{ opacity: 1, duration: 0.30, ease: 'none' }}, {t['t049'] + 4.7:.3f});
    tl.to('#bpl-f', {{ scaleX: 0, transformOrigin: '100% 50%', duration: 0.50,
                      ease: 'power2.in' }}, {t['t050'] + 3.4:.3f});
    tl.to('#bpl-t', {{ opacity: 0, duration: 0.25, ease: 'none' }}, {t['t050'] + 3.3:.3f});
    // Collapse the whole panel, not just its fill/text -- an empty
    // min-height:150px box left sitting in the layout for the rest of the
    // unit (through the entire INCI reveal) measured as a real
    // content-then-empty void (check-static-hold, 212.25-228.75s) and as
    // real overflow once the phase-d camera zoomed in around it
    // (panel_out_of_canvas #bpl at t=215.34s). Transform-only, same reason
    // as 01-bottle's #op above.
    tl.to('#bpl', {{ opacity: 0, scaleY: 0, transformOrigin: '0% 0%',
                    duration: 0.30, ease: 'power2.in' }}, {t['t050'] + 3.6:.3f});
    // Clear the states/pairs before phase D -- this used to happen on t051's
    // own beat (the turn, now retired). Without it they stayed on screen
    // through the INCI reveal and measured as real overlapping/overflowing
    // content (check: panel_out_of_canvas on #pr2/#pr4/#bpl at t=215.34s,
    // 16s into this unit -- long after both chip rows had appeared and
    // never left).
    tl.to(['#st1','#st2','#st3','#st4'], {{ opacity: 0, y: -18, duration: 0.40,
          stagger: 0.06, ease: 'power2.in' }}, {t['t050'] + 4.6:.3f});
    tl.to(['#pr1','#pr2','#pr3','#pr4'], {{ opacity: 0, y: -18, duration: 0.40,
          stagger: 0.06, ease: 'power2.in' }}, {t['t050'] + 5.0:.3f});

    // PHASE D -- the list, then the CAMERA flies to the real position. The
    // world scales and translates; the list itself does not move, which is
    // what makes this read as looking closer rather than as a layout change.
    for (var i = 0; i < 12; i++) {{
      tl.fromTo('#in-' + i, {{ opacity: 0, x: 18 }},
                {{ opacity: 1, x: 0, duration: 0.22, ease: 'power1.out' }},
                {t['t055']:.3f} + i * 0.05);
    }}
    tl.to('#world', {{ scale: 1.22, x: -78, y: -26, duration: 1.10,
                      ease: 'power2.inOut' }}, {t['t055'] + 1.1:.3f});
    tl.to('#world', {{ scale: 1, x: 0, y: 0, duration: 0.95,
                      ease: 'power2.inOut' }}, {t['t056'] + 0.4:.3f});
    // t056 -- "one ingredient cannot rescue a badly built product": the whole
    // list dims and only the highlighted row survives. Column-scale, so it
    // registers where dimming one row would not.
    tl.to('#inci li:not(.hit)', {{ opacity: 0.28, duration: 0.70,
          stagger: 0.02, ease: 'power2.inOut' }}, {t['t056'] + 1.5:.3f});
    // The alarm is RETIRED here -- the running gag closes. It appears greyed
    // and powers down; this is its last appearance in the piece.
    tl.fromTo('#alarm4', {{ opacity: 0, scale: 0.9 }},
              {{ opacity: 1, scale: 1, duration: 0.24, ease: 'back.out(2)' }},
              {t['t057']:.3f});
    // Powers down by TWEENING the colour, not by toggling a class in a
    // callback. onStart/onComplete/tl.call do NOT fire reliably on a seek --
    // the engine jumps to arbitrary times, so a callback-set class leaves the
    // element in whatever state the last executed callback happened to set.
    tl.to('#alarm4', {{ backgroundColor: '#E3E3E3', opacity: 0.4, scale: 0.92,
                       duration: 0.50, ease: 'power2.inOut' }}, {t['t057'] + 0.7:.3f});
    tl.to('#alarm4 b', {{ color: '#6B6B6B', duration: 0.50,
                         ease: 'power2.inOut' }}, {t['t057'] + 0.7:.3f});
    tl.to('#alarm4 i', {{ scale: 0.5, opacity: 0.4, duration: 0.40,
                         ease: 'power2.in' }}, {t['t057'] + 0.7:.3f});
"""
    return css, body, tl


@unit("13-kbeauty")
def _(c):
    """K-beauty didn't invent it. A scale-swap: one claim corrected in place."""
    t = {tid: s - c.turns[0][1] for tid, s, _ in c.turns}
    css = BASE_SPEC_CSS + """
    .kcol { display:flex; flex-direction:column; justify-content:center;
            height:100%; gap:var(--s-6); min-height:0; }
    .pair { display:grid; grid-template-columns:1fr 1fr; gap:var(--s-6);
            min-height:0; }
    .kx { position:relative; background:var(--mist); border-radius:var(--r-3);
          padding:var(--s-7); overflow:hidden; opacity:0; text-align:center; }
    .kx span { position:relative; z-index:1; display:block;
               font-family:var(--font-body); font-weight:800; font-size:66px;
               line-height:var(--lh-snug); }
    .fmts { display:grid; grid-template-columns:repeat(3,1fr); gap:var(--s-4); }
    .fmt { opacity:0; text-align:center; padding:var(--s-4) var(--s-3);
           border-radius:var(--r-pill); background:var(--mist);
           font-family:var(--font-mono); font-size:var(--t-chip);
           letter-spacing:var(--tr-mono); color:var(--ink-2); }
    .kx small { position:relative; z-index:1; display:block;
                margin-top:var(--s-3); font-family:var(--font-mono);
                font-size:var(--t-chip); letter-spacing:var(--tr-mono);
                color:var(--ink-2); }
    """
    body = stage(
        '<div class="kcol">'
        '<p class="kicker" id="kk">WHO INVENTED IT</p>'
        '<div class="pair">'
        '<div class="kx" id="k1"><div class="void" id="kv1"></div>'
        '<span>K-BEAUTY</span><small>DID NOT</small></div>'
        '<div class="kx" id="k2"><div class="wash aqua" id="kw2"></div>'
        '<span>BACTERIA</span><small>DID</small></div>'
        '</div>'
        + '<div class="fmts">'
          '<span class="fmt" id="f1">LIGHTWEIGHT SERUMS</span>'
          '<span class="fmt" id="f2">TONERS</span>'
          '<span class="fmt" id="f3">SUN PRODUCTS</span></div>'
        + say("J", "Bacteria invented it. Korea gave it better packaging.", "kb-j", size="48px")
        + plate("kpl") + '</div>')
    tl = f"""
    // COMPOSED AT t=0. A scene's data-start IS the seam it is wiped in on, so
    // its t=0 is the first frame of its own reveal, not the first frame after
    // it. These three entered at +0.00/+0.20/+0.34 against a 0.45s wipe, so the
    // wipe uncovered a scene that had not arrived: the midpoint frame measured
    // 1.15% ink, 0.22x the median frame and the thinnest in the piece. The
    // reveal is the entrance -- there is no second one to author.
    tl.set('#kk', {{ opacity: 1 }}, 0);
    tl.set('#k1', {{ opacity: 1, x: 0 }}, 0);
    tl.set('#k2', {{ opacity: 1, x: 0 }}, 0);

    // CAMERA L2''->L0' -- pull all the way back out to the shelf. This is the
    // scene's entrance now, and it is the right one: it runs unclipped through
    // the wipe and past it, where a per-card tween would have played behind the
    // clip on the half that is revealed last.
    tl.fromTo('#world', {{ scale: 1.14, y: -16 }},
              {{ scale: 1.0, y: 0, duration: 1.90, ease: 'power2.inOut' }}, 0);
    tl.to('#kv1', {{ opacity: 0.88, duration: 0.22, ease: 'power3.in' }}, {t['t058'] + 1.3:.3f});
    tl.fromTo('#kw2', {{ scaleX: 0 }},
              {{ scaleX: 1, duration: 0.46, ease: 'expo.out' }}, {t['t058'] + 1.5:.3f});
    // The corrected side grows as the struck side recedes -- one comparison
    // resolving, not two cards appearing.
    tl.to('#k1', {{ scale: 0.90, opacity: 0.5, duration: 0.55, ease: 'power2.inOut' }},
          {t['t059']:.3f});
    tl.to('#k2', {{ scale: 1.06, duration: 0.55, ease: 'power2.inOut' }}, {t['t059']:.3f});
    tl.fromTo('#kb-j', {{ opacity: 0, y: 18 }},
              {{ opacity: 1, y: 0, duration: 0.32, ease: 'circ.out' }}, {t['t060']:.3f});
    tl.set('#kpl-t', {{ textContent: 'BACTERIA BUILT IT. KOREA PACKAGED IT.' }}, 0);
    tl.to('#kpl-f', {{ scaleX: 1, duration: 0.60, ease: 'expo.out' }}, {t['t060'] + 1.6:.3f});
    tl.to('#kpl-t', {{ opacity: 1, duration: 0.30, ease: 'none' }}, {t['t060'] + 1.9:.3f});
    // t059 lists the product formats Korean formulators actually use -- three
    // chips arriving on the clause, then the pair re-balancing on t061. Both
    // are panel-scale and both sit in what was otherwise a 20s hold.
    ['f1','f2','f3'].forEach(function (id, i) {{
      tl.fromTo('#' + id, {{ opacity: 0, y: 26 }},
                {{ opacity: 1, y: 0, duration: 0.34, ease: 'back.out(1.6)' }},
                {t['t059'] + 1.2:.3f} + i * 0.85);
    }});
    tl.to('#k1', {{ opacity: 0.34, duration: 0.70, ease: 'sine.inOut' }},
          {t['t061']:.3f});
    tl.to('#k2', {{ scale: 1.10, duration: 0.70, ease: 'sine.inOut' }},
          {t['t061']:.3f});
"""
    return css, body, tl


@unit("14-notnew")
def _(c):
    """CH6 opener. NOT THE NEW HYALURONIC ACID -- struck at full-panel scale."""
    t = {tid: s - c.turns[0][1] for tid, s, _ in c.turns}
    css = BASE_SPEC_CSS + """
    .vcol { display:flex; flex-direction:column; justify-content:center;
            height:100%; gap:var(--s-6); min-height:0; }
    .slab { position:relative; border-radius:var(--r-3); padding:var(--s-8);
            background:var(--ink-soft); overflow:hidden; opacity:0; }
    .slab span { position:relative; z-index:1; display:block;
                 font-family:var(--font-display); font-size:104px;
                 line-height:var(--lh-tight); letter-spacing:var(--tr-display);
                 color:var(--paper); }
    """
    body = stage(
        '<div class="vcol">'
        '<div class="slab" id="sl"><div class="void" id="slv"></div>'
        '<span>Not the new<br>hyaluronic acid.</span></div>'
        + say("S", "And not strong enough evidence for dramatic promises.", "nn", ink=True, size="48px")
        + '</div>', ground="ink")
    tl = f"""
    tl.fromTo('#sl', {{ opacity: 0, y: 34 }},
              {{ opacity: 1, y: 0, duration: 0.44, ease: 'power3.out' }}, {t['t062']:.3f});
    // A full-slab strike: ~34% of the frame, ink-soft(33 luma) -> coral(146).
    // That is a 113-luma step over a third of the canvas -- comfortably past
    // the floor, where a line through the words would measure as nothing.
    tl.to('#slv', {{ opacity: 0.85, duration: 0.26, ease: 'power3.in' }}, {t['t062'] + 1.5:.3f});
    tl.fromTo('#nn', {{ opacity: 0, y: 20 }},
              {{ opacity: 1, y: 0, duration: 0.34, ease: 'power2.out' }}, {t['t062'] + 2.1:.3f});
"""
    return css, body, tl


@unit("15-whatitis")
def _(c):
    """The payoff line. WRAPPED IN AN ELEMENT -- the predecessor shipped this
    exact beat as a BARE TEXT NODE under a .wash and it rendered at 1.72:1,
    invisible to the engine's own text_occluded pass because the text never
    became an element. The <span> below is the fix, and it is load-bearing."""
    t = {tid: s - c.turns[0][1] for tid, s, _ in c.turns}
    css = BASE_SPEC_CSS + """
    .wcol { display:flex; flex-direction:column; justify-content:center;
            height:100%; gap:var(--s-6); min-height:0; }
    .pay { position:relative; border-radius:var(--r-3); padding:var(--s-8);
           background:var(--mist); overflow:hidden; opacity:0; }
    .pay span { position:relative; z-index:1; display:block;
                font-family:var(--font-display); font-size:96px;
                line-height:var(--lh-tight); letter-spacing:var(--tr-display); }
    """
    body = stage(
        '<div class="wcol">'
        '<div class="pay" id="pay"><div class="wash moss" id="payw"></div>'
        '<span>A genuinely interesting<br>supporting ingredient.</span></div>'
        + say("J", "Supporting actor. Not superhero.", "wj", size="54px")
        + '</div>')
    tl = f"""
    tl.fromTo('#pay', {{ opacity: 0, y: 30 }},
              {{ opacity: 1, y: 0, duration: 0.42, ease: 'power2.out' }}, {t['t063']:.3f});
    // moss wash + --paper text = 5.42:1, one of the two verified safe pairings.
    tl.fromTo('#payw', {{ scaleX: 0 }},
              {{ scaleX: 1, duration: 0.62, ease: 'expo.out' }}, {t['t063'] + 0.3:.3f});
    tl.fromTo('#wj', {{ opacity: 0, x: -28 }},
              {{ opacity: 1, x: 0, duration: 0.32, ease: 'circ.out' }}, {t['t064']:.3f});
"""
    return css, body, tl


@unit("16-action")
def _(c):
    """The closing ACTION -- specific and lesson-tied, never a subscribe card."""
    t = {tid: s - c.turns[0][1] for tid, s, _ in c.turns}
    css = BASE_SPEC_CSS + """
    .acol { display:flex; flex-direction:column; justify-content:center;
            height:100%; gap:var(--s-5); min-height:0; }
    .step { position:relative; background:var(--mist); border-radius:var(--r-3);
            padding:var(--s-6) var(--s-7); overflow:hidden; opacity:0;
            display:flex; align-items:center; gap:var(--s-6); }
    .step b { position:relative; z-index:1; font-family:var(--font-mono);
              font-size:56px; color:var(--ink-3); }
    .step span { position:relative; z-index:1; font-family:var(--font-body);
                 font-weight:800; font-size:64px; line-height:var(--lh-snug); }
    """
    body = stage(
        '<div class="acol">'
        '<p class="kicker" id="ak">WHAT TO ACTUALLY DO</p>'
        '<div class="step" id="s1"><div class="wash aqua" id="sw1"></div>'
        '<b>01</b><span>Find the real percentage.</span></div>'
        '<div class="step" id="s2"><div class="wash aqua" id="sw2"></div>'
        '<b>02</b><span>Then judge the whole formula.</span></div>'
        '</div>')
    tl = f"""
    tl.fromTo('#ak', {{ opacity: 0 }}, {{ opacity: 1, duration: 0.24, ease: 'none' }},
              {t['t065']:.3f});
    tl.fromTo('#s1', {{ opacity: 0, x: -40 }},
              {{ opacity: 1, x: 0, duration: 0.38, ease: 'power4.out' }}, {t['t065'] + 0.25:.3f});
    tl.fromTo('#sw1', {{ scaleX: 0 }},
              {{ scaleX: 1, duration: 0.50, ease: 'expo.out' }}, {t['t065'] + 0.45:.3f});
    tl.fromTo('#s2', {{ opacity: 0, x: -40 }},
              {{ opacity: 1, x: 0, duration: 0.38, ease: 'power4.out' }}, {t['t065'] + 1.15:.3f});
    tl.fromTo('#sw2', {{ scaleX: 0 }},
              {{ scaleX: 1, duration: 0.50, ease: 'expo.out' }}, {t['t065'] + 1.35:.3f});
"""
    return css, body, tl


@unit("17-dignity")
def _(c):
    """The button. Four turns, ink ground, calm -- the piece has landed."""
    t = {tid: s - c.turns[0][1] for tid, s, _ in c.turns}
    css = BASE_SPEC_CSS + """
    .dcol { display:flex; flex-direction:column; justify-content:center;
            height:100%; gap:var(--s-6); min-height:0; }
    """
    body = stage(
        '<div class="dcol">'
        + say("J", "Would I put a bacteria-made survival molecule on my face?", "d1", ink=True, size="62px")
        + say("S", "Would you?", "d2", ink=True, size="54px")
        + say("J", "I have already purchased snail mucus.<br>The dignity ship sailed years ago.", "d3", ink=True, size="62px")
        + '</div>', ground="ink")
    tl = f"""
    tl.fromTo('#d1', {{ opacity: 0, y: 22 }},
              {{ opacity: 1, y: 0, duration: 0.38, ease: 'sine.out' }}, {t['t066']:.3f});
    tl.fromTo('#d2', {{ opacity: 0, y: 22 }},
              {{ opacity: 1, y: 0, duration: 0.34, ease: 'sine.out' }}, {t['t067']:.3f});
    tl.to('#d1', {{ opacity: 0.32, duration: 0.40, ease: 'sine.inOut' }}, {t['t067']:.3f});
    tl.fromTo('#d3', {{ opacity: 0, y: 26 }},
              {{ opacity: 1, y: 0, duration: 0.42, ease: 'power3.out' }}, {t['t068']:.3f});
    tl.to('#d2', {{ opacity: 0.32, duration: 0.40, ease: 'sine.inOut' }}, {t['t068']:.3f});
"""
    return css, body, tl


@unit("18-endscreen")
def _(c):
    """END SCREEN. The final 5-20s carry YouTube's own overlays, drawn ON TOP.

    So this scene is a FRAME for them: the right third and lower-right are
    reserved via --endscreen-*, motion is calmed, and no text enters the
    overlay zone.

    COLD-OPEN REVISION: the bookend now returns to the BOTTLE, not the
    brine field -- 01-hook (and its brine) is retired; the piece opens on
    01-bottle now, so a bookend showing brine no longer matches frame 0.
    ids carry an es- prefix (es-btl, es-pc) for the same reason 01-bottle's
    do: every sub-composition renders into the same document at once, and a
    bare #btl/#pc would collide with 01-bottle.html's and 12-bottle.html's.
    No camera journey to bookend either -- 01-bottle has no baseline #world
    transform (the tried close-up zoom overflowed and was removed), so both
    ends are already the same rest state; #world needs no tween here.
    """
    t = {tid: s - c.turns[0][1] for tid, s, _ in c.turns}
    css = BASE_SPEC_CSS + """
    /* Scene-scoped end-screen reserve. NOT global: the Shorts rails bind every
       frame, but this zone binds only the final scene, so reserving it across
       the piece would waste the right third of all 1920 frames. */
    .stage { padding-right:calc(var(--safe-right) + var(--endscreen-right));
             padding-bottom:calc(var(--safe-bottom) + var(--endscreen-bottom)); }
    .ewrap { display:grid; grid-template-columns:38fr 62fr; gap:var(--s-8);
             height:100%; align-items:center; min-height:0; }
    .bottle { position:relative; margin:0 auto; width:220px; height:380px;
              border-radius:34px 34px 14px 14px; background:var(--ink-soft);
              border:3px solid var(--rule-dark); display:flex;
              flex-direction:column; align-items:center; justify-content:center;
              gap:var(--s-3); overflow:hidden; opacity:0; }
    .bottle .pc { font-family:var(--font-display); font-size:88px;
                  line-height:1; margin:0; color:var(--paper); }
    .bottle .nm2 { font-family:var(--font-mono); font-size:var(--t-caption);
                   letter-spacing:var(--tr-mono-wide); color:var(--ink-3); }
    .ecol { position:relative; z-index:1; display:flex; flex-direction:column;
            justify-content:center; height:100%; gap:var(--s-5); }
    """
    body = stage(
        '<div class="ewrap">'
        '<div class="bottle" id="es-btl">'
        '<p class="pc" id="es-pc">11%</p>'
        '<span class="nm2">COMPLEX</span></div>'
        '<div class="ecol">'
        + say("J", "What questionable ingredient<br>are we investigating next?", "e1", ink=True, size="76px")
        + '</div></div>', ground="ink")
    tl = f"""
    // The bottle returns -- same prop, at rest, the piece's actual opening
    // framing now. A gentle settle-in rather than a hard cut so the bookend
    // reads as arrival, not a fresh entrance.
    tl.fromTo('#es-btl', {{ opacity: 0, scale: 0.92 }},
              {{ opacity: 1, scale: 1, duration: 0.60, ease: 'power2.out' }}, 0);
    tl.fromTo('#e1', {{ opacity: 0, y: 24 }},
              {{ opacity: 1, y: 0, duration: 0.44, ease: 'power2.out' }}, {t['t070']:.3f});
"""
    return css, body, tl
