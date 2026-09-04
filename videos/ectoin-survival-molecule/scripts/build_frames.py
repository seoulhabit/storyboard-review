#!/usr/bin/env python3
"""Generate compositions/frames/*.html for all 28 scenes.

Scene durations, starts and every @w()/@we()/@first/@last/@dur/@sent() marker
are DERIVED from timing.walk(), which itself derives from the CUT, measured
voiceover (scripts/gen_vo.py's output: assets/voice/NN.wav + NN.words.json).
Nothing here authors a duration or an absolute second by hand any more -- see
this project's CLAUDE.md and the plan this implements for why a hand-typed
absolute second is exactly the defect class that put dead air at every seam.

Layouts are landscape-NATIVE, not portrait layouts stretched -- unchanged from
the Act 1 pilot's own framing note.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _preamble import scene
from frames_a27 import SCENES_A27
from timing import walk, Ctx, ORDER

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- scene 01
S1_CSS = """
    #root { background:var(--ink); color:var(--paper); }
    .s1 { display:grid; grid-template-columns:58fr 42fr; gap:var(--s-8);
          align-items:stretch; height:100%; }
    .s1-claim-wrap { display:flex; align-items:center; min-height:0; }
    .s1-claim { font-family:var(--font-display); font-size:var(--t-hero);
                line-height:var(--lh-tight); letter-spacing:var(--tr-display);
                margin:0; }
    .s1-claim em { font-style:normal; color:var(--aqua); }
    .s1-claim span { display:inline; }
    .s1-neg { display:flex; flex-direction:column; gap:var(--s-4);
              min-height:0; height:100%; justify-content:center; }
    .s1-neg-h { flex:0 0 auto; font-family:var(--font-mono); font-size:var(--t-label);
                letter-spacing:var(--tr-mono-wide); color:var(--ink-3-dark);
                text-transform:uppercase; margin:0 0 var(--s-2); }
    /* A CARD that fills the column, not a line of text with a hairline through it.
       Sized against the cadence metric: a flood must move enough FRAME AREA to
       register. Measured at the old size the flood covered 0.67% of the frame and
       the scene read as an 8.6s hold; filling the column takes each card to ~8%. */
    .s1-item { position:relative; flex:1 1 0; min-height:0; max-height:230px;
               display:flex; align-items:center; overflow:hidden;
               background:var(--ink-soft); border-radius:var(--r-3);
               padding:var(--s-5) var(--s-6);
               font-family:var(--font-body); font-weight:800;
               font-size:var(--t-frame); color:var(--ink-2-dark); }
    .s1-item > span:not(.bar) { position:relative; z-index:1; }
    /* scaleX, NOT an animated width: a peer session measured hardware GPU capture
       silently dropping an animated `width` on an overflow:hidden box, and .clip is
       overflow:hidden. A transform composites correctly and is the better mechanism
       regardless. transform-origin pins the wipe to the left edge. */
    .s1-mark { position:absolute; left:var(--safe-left); bottom:var(--safe-bottom);
               right:auto; width:max-content; margin:0;
               font-family:var(--font-mono); font-size:var(--t-label);
               letter-spacing:0.42em; color:var(--aqua); text-transform:uppercase; }
    .s1-item .bar { position:absolute; inset:0; transform:scaleX(0);
                    transform-origin:0% 50%; background:var(--coral); }
"""
S1_BODY = """    <div class="stage">
      <div class="s1">
        <div class="s1-claim-wrap">
          <h1 class="s1-claim" id="s1-claim"><span id="s1-c1">Your next favourite
            skincare ingredient</span><span id="s1-c2"> may have been invented
            by </span><em id="s1-bacteria">bacteria trying not to die.</em></h1>
        </div>
        <div class="s1-neg flexmin">
          <p class="s1-neg-h">Not this</p>
          <div class="s1-item" id="s1-i1"><span class="bar" id="s1-b1"></span><span>Snail mucin</span></div>
          <div class="s1-item" id="s1-i2"><span class="bar" id="s1-b2"></span><span>Salmon DNA</span></div>
          <div class="s1-item" id="s1-i3"><span class="bar" id="s1-b3"></span><span>Hyaluronic acid</span></div>
        </div>
      </div>
      <p class="s1-mark" id="s1-mark">ECTOIN</p>
    </div>"""
S1_TL = """
  // FRAME ZERO IS THE HOOK: chunk 1 of the claim is already at rest at t=0,
  // not mid-fade (a separate still is the thumbnail asset, so the export's
  // literal first frame does not have to carry that job alone). Chunks 2/3
  // reveal on their own words -- real early motion instead of the whole
  // claim landing as one inert block, and keeps #root moving well inside
  // the 6.0s cadence ceiling (previously the first beat was the "Not snail"
  // card at ~5.65s, which the newest take's timing pushed close enough to
  // the ceiling to read as a static hold).
  tl.set('#s1-c1', { opacity: 1, y: 0 }, 0);
  tl.fromTo('#s1-c2', { opacity:0, y:14 }, { opacity:1, y:0, duration:0.45 }, @w(may)-0.10);
  tl.fromTo('#s1-bacteria', { opacity:0, y:14 }, { opacity:1, y:0, duration:0.45 }, @w(bacteria)-0.10);
  // "not to die" is occurrence 1 of "not" -- not one of the three negated
  // items below, which are occurrences 2/3/4 ("not snail" / "not salmon" /
  // "and not another [hyaluronic acid]").
  tl.fromTo('#s1-i1', { opacity:0, x:52 }, { opacity:1, x:0, duration:0.45 }, @w(Not,2)-0.10);
  tl.fromTo('#s1-i2', { opacity:0, x:52 }, { opacity:1, x:0, duration:0.45 }, @w(Not,3)-0.10);
  tl.fromTo('#s1-i3', { opacity:0, x:52 }, { opacity:1, x:0, duration:0.45 }, @w(Not,4)-0.10);
  tl.fromTo('#s1-b1', { scaleX:0 }, { scaleX:1, duration:0.30, ease:'power2.inOut' }, @we(mucin)+0.10);
  tl.to('#s1-i1', { color:'#131516', duration:0.30 }, @we(mucin)+0.10);  // --ink on coral = 5.60:1
  tl.fromTo('#s1-b2', { scaleX:0 }, { scaleX:1, duration:0.30, ease:'power2.inOut' }, @we(DNA)+0.10);
  tl.to('#s1-i2', { color:'#131516', duration:0.30 }, @we(DNA)+0.10);  // --ink on coral = 5.60:1
  tl.fromTo('#s1-b3', { scaleX:0 }, { scaleX:1, duration:0.30, ease:'power2.inOut' }, @we(acid)+0.10);
  tl.to('#s1-i3', { color:'#131516', duration:0.30 }, @we(acid)+0.10);  // --ink on coral = 5.60:1
  // The mark lands late enough to fill the tail rather than the hold going dead.
  // Enters from ABOVE (y:-24 -> 0), not below: #s1-mark rests with its own
  // bottom edge AT the safe-bottom line, so a y:+N->0 entrance would start
  // the whole element N px LOWER than rest, transiently pushing it into the
  // reserved bottom margin while opacity ramps up together with position --
  // caught by the hard safe-area gate at 642px inside the zone at t=10.75s.
  // Sliding down into place from above never crosses that line.
  tl.fromTo('#s1-mark', { opacity:0, y:-24 }, { opacity:1, y:0, duration:0.60 }, @last-0.4);
  tl.fromTo('#s1-claim', { y:0 }, { y:-14, duration:1.60, ease:'power1.inOut' }, @last-0.4);
"""

# ---------------------------------------------------------------- scene 02
S2_CSS = """
    #root { background:var(--paper); color:var(--ink); }
    .s2 { display:grid; grid-template-columns:52fr 48fr; gap:var(--s-8);
          align-items:center; height:100%; }
    .s2-fig { position:relative; width:100%; aspect-ratio:1/1; max-height:100%;
              justify-self:center; }
    .s2-copy { display:flex; flex-direction:column; gap:var(--s-5); min-height:0; }
    .s2-kicker { font-family:var(--font-mono); font-size:var(--t-label);
                 letter-spacing:var(--tr-mono-wide); color:var(--ink-2);
                 text-transform:uppercase; margin:0; }
    .s2-line { font-family:var(--font-display); font-size:var(--t-figure);
               line-height:var(--lh-snug); margin:0; }
    .s2-line b { font-weight:400; color:var(--coral); }
"""
S2_BODY = """    <div class="stage">
      <div class="s2">
        <div class="s2-fig">
          <svg viewBox="0 0 600 600" width="100%" height="100%" aria-hidden="true">
            <g id="s2-salt"></g>
            <circle id="s2-cell" cx="300" cy="300" r="150" fill="#F0EBE1"
                    stroke="#131516" stroke-width="4"/>
            <g id="s2-drops" fill="#59B8AE"></g>
          </svg>
        </div>
        <div class="s2-copy flexmin">
          <p class="s2-kicker" id="s2-k">The problem it solves</p>
          <p class="s2-line" id="s2-l1">Some places are so salty and so dry
            that an ordinary cell <b>loses its water</b></p>
          <p class="s2-line" id="s2-l2">&mdash; and stops working.</p>
        </div>
      </div>
    </div>"""
S2_TL = """
  // Salt field and escaping water are BUILT here, not authored by hand: a
  // deterministic lattice, so the same seek always paints the same frame.
  // No Math.random anywhere -- it is banned and would break re-seek determinism.
  var salt = document.getElementById('s2-salt');
  var saltMade = [];   // only ids actually created -- see the animate loop below
  for (var i = 0; i < 44; i++) {
    var a = (i * 137.508) * Math.PI / 180, rr = 205 + (i % 7) * 26;
    var x = 300 + Math.cos(a) * rr, y = 300 + Math.sin(a) * rr;
    if (x < 12 || x > 588 || y < 12 || y > 588) continue;
    var s = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    s.setAttribute('x', x.toFixed(1)); s.setAttribute('y', y.toFixed(1));
    s.setAttribute('width', 9); s.setAttribute('height', 9);
    s.setAttribute('fill', '#9C978D'); s.setAttribute('opacity', 0);
    s.setAttribute('transform', 'rotate(45 ' + x.toFixed(1) + ' ' + y.toFixed(1) + ')');
    s.id = 'salt-' + i; salt.appendChild(s); saltMade.push(i);
  }
  var drops = document.getElementById('s2-drops');
  for (var j = 0; j < 10; j++) {
    var da = (j * 36) * Math.PI / 180;
    var d = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    d.setAttribute('cx', (300 + Math.cos(da) * 110).toFixed(1));
    d.setAttribute('cy', (300 + Math.sin(da) * 110).toFixed(1));
    d.setAttribute('r', 8); d.setAttribute('opacity', 0);
    d.id = 'drop-' + j; drops.appendChild(d);
    // Baseline registered as a REAL timeline tween at 0, not a bare gsap.set():
    // the engine seeks to arbitrary times without passing through 0 first.
    tl.set('#drop-' + j, { opacity: 0, x: 0, y: 0 }, 0);
    tl.to('#drop-' + j, { opacity: 0.9, duration: 0.25 }, 3.30 + j * 0.06);
    tl.to('#drop-' + j, { x: Math.cos(da) * 150, y: Math.sin(da) * 150,
                          opacity: 0, duration: 1.5, ease: 'power1.in' }, 3.70 + j * 0.06);
  }
  // Iterate saltMade, NOT 0..43: the loop above skips out-of-bounds positions, and
  // animating an id that was never created logs "GSAP target not found" per miss.
  saltMade.forEach(function (k, n) {
    tl.set('#salt-' + k, { opacity: 0 }, 0);
    tl.to('#salt-' + k, { opacity: 0.85, duration: 0.4 }, 1.20 + (n % 11) * 0.11);
  });
  tl.fromTo('#s2-k',  { opacity:0, y:34 }, { opacity:1, y:0, duration:0.40 }, 0.20);
  tl.fromTo('#s2-l1', { opacity:0, y:44 }, { opacity:1, y:0, duration:0.50 }, 0.60);
  tl.fromTo('#s2-l2', { opacity:0, y:44 }, { opacity:1, y:0, duration:0.50 }, @w(stop)-0.35);
  tl.set('#s2-cell', { attr:{ r:150 } }, 0);
  tl.to('#s2-cell', { attr:{ r:112 }, duration:2.6, ease:'power2.inOut' }, 4.20);
  tl.to('#s2-cell', { attr:{ stroke:'#C97A5C' }, duration:0.9 }, @last-0.2);
"""

# ---------------------------------------------------------------- scene 03
S3_CSS = """
    #root { background:var(--paper); color:var(--ink); }
    .s3 { display:flex; flex-direction:column; justify-content:center;
          gap:var(--s-7); height:100%; }
    .s3-row { display:grid; grid-template-columns:repeat(3,1fr); gap:var(--s-7); }
    .s3-card { display:flex; flex-direction:column; align-items:center;
               gap:var(--s-4); min-height:0; }
    .s3-vessel { width:150px; height:230px; border:4px solid var(--ink);
                 border-radius:var(--r-3); position:relative; background:var(--mist); }
    .s3-vessel::before { content:""; position:absolute; left:50%; top:-30px;
                         transform:translateX(-50%); width:56px; height:30px;
                         border:4px solid var(--ink); border-bottom:none;
                         border-radius:var(--r-2) var(--r-2) 0 0; background:var(--mist); }
    .s3-fill { position:absolute; left:0; right:0; bottom:0; height:100%;
               transform:scaleY(0); transform-origin:50% 100%;
               background:var(--aqua); border-radius:0 0 5px 5px; }
    .s3-cap { font-family:var(--font-mono); font-size:var(--t-label);
              letter-spacing:var(--tr-mono-wide); text-transform:uppercase;
              color:var(--ink-2); }
    .s3-lockup { position:relative; background:var(--ink); border-radius:var(--r-3);
                 padding:var(--s-6) var(--s-7); overflow:hidden; }
    .s3-lockup .wash { position:absolute; inset:0; background:var(--aqua);
                       transform:scaleX(0); transform-origin:0% 50%; }
    .s3-lockup > *:not(.wash) { position:relative; z-index:1; }
    .s3-mark { text-align:center; font-family:var(--font-display);
               font-size:var(--t-hero); letter-spacing:0.06em; margin:0;
               color:var(--paper); }
    .s3-rule { height:4px; width:520px; margin:var(--s-4) auto; background:var(--coral);
               transform:scaleX(0); transform-origin:50% 50%; }
    .s3-sub { text-align:center; font-family:var(--font-body); font-weight:800;
              font-size:var(--t-body); color:var(--ink-2-dark); margin:0; }
"""
S3_BODY = """    <div class="stage">
      <div class="s3">
        <div class="s3-row">
          <div class="s3-card" id="s3-c1">
            <div class="s3-vessel"><div class="s3-fill" id="s3-f1"></div></div>
            <div class="s3-cap">Serums</div></div>
          <div class="s3-card" id="s3-c2">
            <div class="s3-vessel"><div class="s3-fill" id="s3-f2"></div></div>
            <div class="s3-cap">Creams</div></div>
          <div class="s3-card" id="s3-c3">
            <div class="s3-vessel"><div class="s3-fill" id="s3-f3"></div></div>
            <div class="s3-cap">Sunscreens</div></div>
        </div>
        <div class="s3-lockup" id="s3-lockup">
          <div class="wash" id="s3-wash"></div>
          <p class="s3-mark" id="s3-mark">ECTOIN</p>
          <div class="s3-rule" id="s3-rule"></div>
          <p class="s3-sub" id="s3-sub">the science is stranger than the marketing</p>
        </div>
      </div>
    </div>"""
S3_TL = """
  // A genuine three-across row -- the shape a wide frame affords and a tall one
  // can only fake by stacking. Cards settle at frame zero (no entrance), so the
  // scene opens composed; the FILL is the beat that carries the line.
  tl.set(['#s3-c1','#s3-c2','#s3-c3'], { opacity:1, y:0 }, 0);
  tl.fromTo('#s3-f1', { scaleY:0 }, { scaleY:0.62, duration:0.85, ease:'power2.out' }, 1.30);
  tl.fromTo('#s3-f2', { scaleY:0 }, { scaleY:0.74, duration:0.85, ease:'power2.out' }, 1.75);
  tl.fromTo('#s3-f3', { scaleY:0 }, { scaleY:0.55, duration:0.85, ease:'power2.out' }, 2.20);
  // scaleX, not letterSpacing: layout/text-reflow properties snap to integer
  // device pixels during layout, so the ease-out tail stutters under seek-by-frame
  // capture (`check`: gsap_non_transform_motion). A transform gives the same
  // settling-in read and interpolates smoothly.
  tl.fromTo('#s3-mark', { opacity:0, scaleX:1.16 },
                        { opacity:1, scaleX:1, duration:0.90, ease:'power3.out',
                          transformOrigin:'50% 50%' }, @w(ectoin)-0.35);
  tl.fromTo('#s3-rule', { scaleX:0 }, { scaleX:1, duration:0.70, ease:'power2.inOut' }, @w(stranger)-0.30);
  tl.fromTo('#s3-sub',  { opacity:0, y:36 }, { opacity:1, y:0, duration:0.50 }, @w(marketing)-0.40);
  // Vessels drain back slightly on the closing beat -- a real state change tied to
  // the line ("stranger than the marketing"), across the otherwise-dead tail.
  tl.to(['#s3-f1','#s3-f2','#s3-f3'], { scaleY:0.30, duration:1.70,
                                         ease:'power1.inOut', stagger:0.10 }, @last-0.6);
  // The lockup arrives as a full-width dark band, then floods aqua -- two
  // large-area beats replacing a wordmark fade that measured as nothing.
  tl.fromTo('#s3-lockup', { opacity:0, scaleY:0.4, transformOrigin:'50% 50%' },
                          { opacity:1, scaleY:1, duration:0.55, ease:'power3.out' }, @w(ectoin)-0.60);
  tl.fromTo('#s3-wash', { scaleX:0 }, { scaleX:1, duration:0.90,
                                        ease:'power2.inOut' }, @w(stranger)-0.20);
  tl.to('#s3-mark', { color:'#131516', duration:0.50 }, @w(stranger));
"""

# ---------------------------------------------------------------- scene 04
S4_CSS = """
    #root { background:var(--ink); color:var(--paper); }
    .s4 { display:grid; grid-template-columns:44fr 56fr; gap:var(--s-8);
          align-items:center; height:100%; }
    .s4-l { display:flex; flex-direction:column; gap:var(--s-4); min-height:0; }
    .s4-term { font-family:var(--font-display); font-size:var(--t-hero);
               line-height:var(--lh-tight); margin:0; color:var(--aqua); }
    .s4-pron { font-family:var(--font-mono); font-size:var(--t-label);
               letter-spacing:var(--tr-mono); color:var(--ink-3-dark); margin:0; }
    .s4-r { display:flex; flex-direction:column; gap:var(--s-5); min-height:0;
            border-left:3px solid var(--rule-dark); padding-left:var(--s-7); }
    .s4-def { font-family:var(--font-display); font-size:var(--t-figure);
              line-height:var(--lh-snug); margin:0; }
    .s4-def b { font-weight:400; color:var(--celadon); }
    .s4-strike { position:relative; font-family:var(--font-body); font-weight:800;
                 font-size:var(--t-body); color:var(--ink-2-dark);
                 background:var(--ink-soft); border-radius:var(--r-3);
                 padding:var(--s-4) var(--s-5); overflow:hidden; }
    .s4-strike > span { position:relative; z-index:1; }
    .s4-strike .bar { position:absolute; inset:0; transform:scaleX(0);
                      transform-origin:0% 50%; background:var(--coral); }
    .s4-defbox { position:relative; background:var(--ink-soft); border-radius:var(--r-3);
                 padding:var(--s-6); overflow:hidden; }
    .s4-defbox .wash { position:absolute; inset:0; background:var(--moss);
                       transform:scaleX(0); transform-origin:0% 50%; }
    .s4-defbox > *:not(.wash) { position:relative; z-index:1; }
"""
S4_BODY = """    <div class="stage">
      <div class="s4">
        <div class="s4-l flexmin">
          <p class="s4-term" id="s4-term">Extremolyte</p>
          <p class="s4-pron" id="s4-pron">ek-STREE-mo-lyte &middot; noun</p>
        </div>
        <div class="s4-r flexmin">
          <div class="s4-strike" id="s4-sx"><span class="bar" id="s4-sb"></span><span>Sounds like a superhero</span></div>
          <div class="s4-defbox" id="s4-defbox">
            <div class="wash" id="s4-defwash"></div>
            <p class="s4-def" id="s4-d1">A protective molecule made by microbes
              that live somewhere <b>extreme</b>.</p>
          </div>
        </div>
      </div>
    </div>"""
S4_TL = """
  // 12s is a long hold, so the beats are spread across the WHOLE duration --
  // landing them all in the first two seconds and freezing is the cadence
  // failure the static-hold check exists to catch.
  tl.fromTo('#s4-term', { opacity:0, y:52 }, { opacity:1, y:0, duration:0.55 }, 0.15);
  tl.fromTo('#s4-pron', { opacity:0 },       { opacity:1, duration:0.45 }, 0.75);
  tl.fromTo('#s4-sx',   { opacity:0, x:44 }, { opacity:1, x:0, duration:0.45 }, @w(superhero)-0.50);
  tl.fromTo('#s4-sb', { scaleX:0 }, { scaleX:1, duration:0.32, ease:'power2.inOut' }, @we(superhero)+0.60);
  tl.to('#s4-sx', { color:'#131516', duration:0.32 }, @we(superhero)+0.60);  // --ink on coral = 5.60:1
  tl.fromTo('#s4-d1', { opacity:0, y:44 }, { opacity:1, y:0, duration:0.55 }, @w(protective)-0.30);
  // The definition panel floods on "extreme" -- a real large-area beat in the
  // back half, where the scene previously held for 6.6s on a 1.04 text scale.
  tl.fromTo('#s4-defbox', { opacity:0, y:44 }, { opacity:1, y:0, duration:0.55 }, @w(protective)-0.40);
  tl.fromTo('#s4-defwash', { scaleX:0 }, { scaleX:1, duration:0.95,
                                           ease:'power2.inOut' }, @w(extreme)-0.20);
"""

# ---------------------------------------------------------------- scene 05
S5_CSS = """
    #root { background:var(--paper); color:var(--ink); }
    .s5 { display:grid; grid-template-columns:56fr 44fr; gap:var(--s-8);
          align-items:center; height:100%; }
    .s5-l { display:flex; flex-direction:column; gap:var(--s-4); min-height:0; }
    .s5-k { font-family:var(--font-mono); font-size:var(--t-label);
            letter-spacing:var(--tr-mono-wide); text-transform:uppercase;
            color:var(--ink-2); margin:0; }
    .s5-name { font-family:var(--font-display); font-style:italic;
               font-size:var(--t-hero); line-height:var(--lh-tight); margin:0; }
    .s5-note { font-family:var(--font-display); font-size:var(--t-figure);
               line-height:var(--lh-snug); color:var(--ink); margin:0; }
    .s5-note b { font-weight:400; color:var(--coral); }
    .s5-cite-wrap { margin-top:var(--s-4); }
    .s5-fig { position:relative; width:100%; aspect-ratio:1/1; max-height:100%;
              justify-self:center; }
"""
S5_BODY = """    <div class="stage">
      <div class="s5">
        <div class="s5-l flexmin">
          <p class="s5-k" id="s5-k">Where it comes from</p>
          <p class="s5-name" id="s5-name">Halomonas elongata</p>
          <p class="s5-note" id="s5-note">Lives in salt. When the outside gets
            punishing, it <b>floods itself with ectoin</b>.</p>
          <div class="s5-cite-wrap"><span class="cite" id="s5-cite">Environ Microbiol &middot; 2010</span></div>
        </div>
        <div class="s5-fig">
          <svg viewBox="0 0 600 600" width="100%" height="100%" aria-hidden="true">
            <g id="s5-crystals"></g>
          </svg>
        </div>
      </div>
    </div>"""
S5_TL = """
  // Deterministic crystal lattice -- index-derived, no randomness.
  var cg = document.getElementById('s5-crystals');
  for (var i = 0; i < 64; i++) {
    var col = i % 8, row = Math.floor(i / 8);
    var cx = 60 + col * 68, cy = 60 + row * 68;
    var sz = 20 + ((i * 7) % 5) * 6;
    var r = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    r.setAttribute('x', (cx - sz/2).toFixed(1)); r.setAttribute('y', (cy - sz/2).toFixed(1));
    r.setAttribute('width', sz); r.setAttribute('height', sz);
    r.setAttribute('fill', (i % 5 === 0) ? '#59B8AE' : '#D9D3C6');
    r.setAttribute('transform', 'rotate(45 ' + cx + ' ' + cy + ')');
    r.id = 'x-' + i; cg.appendChild(r);
    tl.set('#x-' + i, { opacity: 0, scale: 0.4, transformOrigin: '50% 50%' }, 0);
    tl.to('#x-' + i, { opacity: 1, scale: 1, duration: 0.45, ease: 'back.out(2)' },
          0.30 + (col + row) * 0.16);
  }
  tl.fromTo('#s5-k',    { opacity:0, y:30 }, { opacity:1, y:0, duration:0.40 }, 0.20);
  tl.fromTo('#s5-name', { opacity:0, y:46 }, { opacity:1, y:0, duration:0.55 }, 0.55);
  tl.fromTo('#s5-note', { opacity:0, y:44 }, { opacity:1, y:0, duration:0.55 }, @w(Lives)-0.20);
  tl.fromTo('#s5-cite', { opacity:0 },       { opacity:1, duration:0.45 }, @last-1.4);
  tl.to('#s5-crystals', { rotation:2.2, transformOrigin:'50% 50%',
                          duration:5.0, ease:'none' }, @w(floods)-0.30);
"""

# ---------------------------------------------------------------- scene 06
S6_CSS = """
    #root { background:var(--paper); color:var(--ink); }
    .s6 { display:flex; flex-direction:column; justify-content:center;
          gap:var(--s-6); height:100%; }
    .s6-h { font-family:var(--font-display); font-size:var(--t-figure);
            line-height:var(--lh-snug); margin:0; }
    .s6-row { display:grid; grid-template-columns:repeat(3,1fr); gap:var(--s-7);
              align-items:start; }
    .s6-step { position:relative; display:flex; flex-direction:column; gap:var(--s-4);
               min-height:0; background:var(--mist); border-radius:var(--r-3);
               padding:var(--s-5); overflow:hidden; }
    .s6-step .fill { position:absolute; inset:0; background:var(--celadon);
                     transform:scaleY(0); transform-origin:50% 100%; }
    .s6-step > *:not(.fill) { position:relative; z-index:1; }
    /* --ink-2 (4.89:1 on paper), NOT --ink-3 (2.67:1 -- below even the 3:1
       large-text floor). The step numbers are content meant to be read, so the
       tertiary ink is the wrong token for this ground. Ground-scoped: --ink-3-dark
       is the variant for the ink-ground scenes, and is used there. */
    .s6-num { font-family:var(--font-mono); font-size:var(--t-label);
              letter-spacing:var(--tr-mono-wide); color:var(--ink-2); }
    .s6-svg { width:100%; height:210px; }
    .s6-lab { font-family:var(--font-body); font-weight:800; font-size:var(--t-body);
              line-height:var(--lh-snug); margin:0; }
    .s6-lab.bad { color:var(--coral); }
"""
S6_BODY = """    <div class="stage">
      <div class="s6">
        <p class="s6-h" id="s6-h">Salt pulls water out of cells.</p>
        <div class="s6-row">
          <div class="s6-step" id="s6-s1">
            <div class="fill" id="s6-fill1"></div>
            <span class="s6-num">01</span>
            <svg class="s6-svg" viewBox="0 0 300 210" aria-hidden="true">
              <path id="s6-p1" d="M40,150 C70,60 110,60 150,105 C190,150 230,150 260,60"
                    fill="none" stroke="#131516" stroke-width="9" stroke-linecap="round"/>
            </svg>
            <p class="s6-lab">A protein holds its shape</p></div>
          <div class="s6-step" id="s6-s2">
            <div class="fill" id="s6-fill2"></div>
            <span class="s6-num">02</span>
            <svg class="s6-svg" viewBox="0 0 300 210" aria-hidden="true">
              <rect id="s6-vessel" x="26" y="42" width="150" height="126" rx="16"
                    fill="none" stroke="#131516" stroke-width="5" opacity="0"/>
              <g id="s6-w"></g>
            </svg>
            <p class="s6-lab">Water leaves</p></div>
          <div class="s6-step" id="s6-s3">
            <div class="fill" id="s6-fill3"></div>
            <span class="s6-num">03</span>
            <svg class="s6-svg" viewBox="0 0 300 210" aria-hidden="true">
              <path id="s6-p3" d="M40,150 C70,60 110,60 150,105 C190,150 230,150 260,60"
                    fill="none" stroke="#C97A5C" stroke-width="9" stroke-linecap="round"/>
            </svg>
            <p class="s6-lab bad">It loses it &mdash; and the cell stops working</p></div>
        </div>
      </div>
    </div>"""
S6_TL = """
  // The core mechanism, read LEFT TO RIGHT across the wide frame. This is the
  // shape 16:9 gives you for free and portrait has to stack vertically.
  var wg = document.getElementById('s6-w');
  for (var i = 0; i < 9; i++) {
    var wx = 45 + (i % 3) * 55, wy = 70 + Math.floor(i / 3) * 45;
    var c = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    c.setAttribute('cx', wx); c.setAttribute('cy', wy);
    c.setAttribute('r', 13); c.setAttribute('fill', '#59B8AE');
    c.id = 'w-' + i; wg.appendChild(c);
    tl.set('#w-' + i, { opacity: 1, x: 0, y: 0 }, 0);
    tl.to('#w-' + i, { x: 150, y: -22, opacity: 0, duration: 1.25,
                       ease: 'power1.in' }, @w(Lose)+0.30 + i * 0.11);
    // Second wave: refill, then leave again. Without it the middle column is
    // genuinely empty for the back half of the scene -- caught by the
    // region-aware content-void check, not by the whole-frame one.
    tl.to('#w-' + i, { x: 0, y: 0, opacity: 0.55, duration: 0.01 }, @w(membranes)-0.20 + i * 0.04);
    tl.to('#w-' + i, { x: 150, y: -22, opacity: 0, duration: 1.30,
                       ease: 'power1.in' }, @w(unstable)+0.20 + i * 0.09);
  }
  // The vessel outline persists for the whole scene, so the step never goes blank.
  // Hidden state is authored in the SVG attribute, NOT tl.set(...,0): a zero-duration
  // set at position 0 does not render while the playhead sits exactly at 0, so frame 0
  // would show it un-hidden (engine lint: gsap_timeline_set_initial_hide).
  tl.to('#s6-vessel', { opacity: 1, duration: 0.45 }, @w(Lose)-0.30);
  tl.fromTo('#s6-h',  { opacity:0, y:20 }, { opacity:1, y:0, duration:0.50 }, 0.15);
  tl.fromTo('#s6-s1', { opacity:0, y:52 }, { opacity:1, y:0, duration:0.50 }, 1.30);
  tl.fromTo('#s6-s2', { opacity:0, y:52 }, { opacity:1, y:0, duration:0.50 }, @w(Lose)-0.60);
  tl.fromTo('#s6-s3', { opacity:0, y:52 }, { opacity:1, y:0, duration:0.50 }, @w(stops)-0.50);
  // Each card's ground fills as its step becomes active -- three ~11%-of-frame
  // beats spread across the hold, where the SVG strokes alone were invisible.
  tl.fromTo('#s6-fill1', { scaleY:0 }, { scaleY:1, duration:0.60, ease:'power2.out' }, 2.20);
  tl.fromTo('#s6-fill2', { scaleY:0 }, { scaleY:1, duration:0.60, ease:'power2.out' }, @w(Lose)-0.40);
  tl.to('#s6-fill1', { scaleY:0.14, duration:0.60, ease:'power2.inOut' }, @w(Lose)-0.40);
  tl.fromTo('#s6-fill3', { scaleY:0 }, { scaleY:1, duration:0.60, ease:'power2.out',
                                         backgroundColor:'#C97A5C' }, @w(stops)-0.30);
  tl.to('#s6-fill2', { scaleY:0.14, duration:0.60, ease:'power2.inOut' }, @w(stops)-0.30);
  // The protein visibly loses its fold -- the claim the label makes, drawn.
  tl.fromTo('#s6-p3', { attr:{ d:'M40,150 C70,60 110,60 150,105 C190,150 230,150 260,60' } },
                      { attr:{ d:'M40,150 C86,128 96,168 150,138 C206,108 214,166 260,132' },
                        duration:1.60, ease:'power2.inOut' }, @w(stops)-0.50);
"""

# ---------------------------------------------------------------- scene 07
S7_CSS = """
    #root { background:var(--ink); color:var(--paper); }
    .s7 { display:grid; grid-template-columns:50fr 50fr; gap:var(--s-8);
          align-items:center; height:100%; }
    .s7-l { display:flex; flex-direction:column; gap:var(--s-5); min-height:0; }
    .s7-k { font-family:var(--font-mono); font-size:var(--t-label);
            letter-spacing:var(--tr-mono-wide); text-transform:uppercase;
            color:var(--ink-3-dark); margin:0; }
    .s7-line { font-family:var(--font-display); font-size:var(--t-figure);
               line-height:var(--lh-snug); margin:0; color:var(--celadon); }
    .s7-q { font-family:var(--font-display); font-size:var(--t-hero);
            line-height:var(--lh-tight); letter-spacing:var(--tr-display); margin:0; }
    .s7-q em { font-style:normal; color:var(--aqua); }
    .s7-line-under { display:inline-block; }
"""
S7_BODY = """    <div class="stage">
      <div class="s7">
        <div class="s7-l flexmin">
          <p class="s7-k" id="s7-k">What it does for the microbe</p>
          <p class="s7-line" id="s7-line">Keeps the space around fragile
            structures survivable.</p>
        </div>
        <div class="s7-l flexmin">
          <p class="s7-q" id="s7-q">So could it do the same for
            <em>stressed <span class="s7-line-under" id="s7-under">human skin?</span></em></p>
        </div>
      </div>
    </div>"""
S7_TL = """
  // Act hook: the scene ENDS on the open question the next act answers, rather
  // than summarising this one. A chapter boundary is where a viewer leaves.
  // No more 3s scale-drift filler -- the closing beat is now the coral
  // underline landing under "stressed human skin?" on its own word.
  tl.fromTo('#s7-k',    { opacity:0, y:30 }, { opacity:1, y:0, duration:0.40 }, 0.20);
  tl.fromTo('#s7-line', { opacity:0, y:44 }, { opacity:1, y:0, duration:0.55 }, 0.55);
  tl.fromTo('#s7-q',    { opacity:0, y:58 }, { opacity:1, y:0, duration:0.70 }, @w(Could)-0.05);
  // "Could" lands late in this take (this scene's own gap before it runs
  // ~6.3s, past the 6.0s cadence ceiling on its own) -- a slow, continuous
  // dim on #s7-line spans the wait instead of one beat landing right before
  // #s7-q, so nothing on #root sits frozen for the whole gap.
  tl.to('#s7-line', { opacity:0.42, duration:@w(Could)-1.6 }, 1.6);
  tl.fromTo('#s7-under', { backgroundImage:
      'linear-gradient(#C97A5C,#C97A5C)', backgroundRepeat:'no-repeat',
      backgroundSize:'0% 4px', backgroundPosition:'0% 100%' },
    { backgroundSize:'100% 4px', duration:0.55, ease:'power2.inOut' }, @w(stressed));
"""

# scene id -> spec dict, act 1 in the same shape as frames_a27's SCENES_A27
FRAME_DEFS = {
    "01-hook":        dict(body=S1_BODY, css=S1_CSS, tl=S1_TL),
    "02-osmosis":     dict(body=S2_BODY, css=S2_CSS, tl=S2_TL),
    "03-now":         dict(body=S3_BODY, css=S3_CSS, tl=S3_TL),
    "04-extremolyte": dict(body=S4_BODY, css=S4_CSS, tl=S4_TL),
    "05-halomonas":   dict(body=S5_BODY, css=S5_CSS, tl=S5_TL),
    "06-mechanism":   dict(body=S6_BODY, css=S6_CSS, tl=S6_TL),
    "07-question":    dict(body=S7_BODY, css=S7_CSS, tl=S7_TL),
}
FRAME_DEFS.update({cid: spec for cid, spec in SCENES_A27})

assert set(FRAME_DEFS) == set(ORDER), (
    f"FRAME_DEFS/vo_lines.LINES mismatch: "
    f"missing frames {set(ORDER) - set(FRAME_DEFS)}, "
    f"orphaned frames {set(FRAME_DEFS) - set(ORDER)}")


# ---- word-marker binding --------------------------------------------------
# @w(word[,occurrence]), @we(word[,occurrence]) -> a plain number (seconds on
# THIS scene's own timeline). @first / @last / @dur -> bare tokens, no parens.
# @sent(i) -> the i-th sentence's start. Arithmetic around a resolved token
# (`@w(Bitop)-0.10`) is left as literal JS text for the browser to evaluate --
# only the marker itself is substituted.
TOKEN_RE = re.compile(
    r"@(w|we)\(\s*([A-Za-z0-9']+)\s*(?:,\s*(\d+)\s*)?\)"
    r"|@(first|last|dur)\b"
    r"|@sent\(\s*(\d+)\s*\)")


def bind(tl_src, ctx, cid, reveals):
    def repl(m):
        if m.group(1):
            fn, word = m.group(1), m.group(2)
            occ = int(m.group(3)) if m.group(3) else 1
            val = (ctx.w if fn == "w" else ctx.we)(word, occ)
            reveals.append({"scene": cid, "kind": fn, "word": word,
                             "occurrence": occ, "seconds": val})
            return f"{val:.3f}"
        if m.group(4):
            return f"{getattr(ctx, m.group(4))():.3f}"
        if m.group(5) is not None:
            return f"{ctx.sent(int(m.group(5))):.3f}"
        return m.group(0)

    out = TOKEN_RE.sub(repl, tl_src)
    if "@" in out:
        leftover = re.findall(r"@[A-Za-z0-9_(),]*", out)
        raise SystemExit(
            f"scene {cid}: unresolved marker token(s) after bind(): {leftover}\n"
            f"Run `python3 scripts/timing.py --words {cid}` to see this scene's "
            f"real words and fix the marker.")
    return out


def arrival(kind):
    """Child-travel snippet appended to the INCOMING scene's own timeline for
    a transition of this `kind`, on top of the root-level clip-path wipe
    (scripts/build_index.py). Each carry/chapter/arrive/settle scene's actual
    travel is bespoke and lives in that scene's own tl string in
    frames_a27.py (see 09-exclusion's ground-inversion beat for the pattern);
    this hook returns nothing by default and is the extension point for
    scenes not yet given a bespoke arrival."""
    return ""


def main():
    scenes, total = walk()
    out = ROOT / "compositions" / "frames"
    out.mkdir(parents=True, exist_ok=True)
    reveals = []
    rows = []
    for s in scenes:
        spec = FRAME_DEFS[s.cid]
        ctx = Ctx(s)
        tl_bound = bind(spec["tl"], ctx, s.cid, reveals) + arrival(s.kind_in)
        (out / f"{s.cid}.html").write_text(
            scene(s.cid, s.dur, spec["body"], spec["css"], tl_bound))
        rows.append((s.cid, s.start, s.own, s.dur, s.kind_in or "-"))

    (ROOT / "index.reveals.json").write_text(json.dumps(reveals, indent=2) + "\n")

    print(f"{'scene':16s} {'start':>8s} {'own':>7s} {'dur':>7s}  in")
    for cid, start, own, dur, kind in rows:
        print(f"{cid:16s} {start:8.3f} {own:7.3f} {dur:7.3f}  {kind}")
    print(f"{'TOTAL':16s} {'':8s} {'':7s} {total:7.3f}")
    print(f"  {len(reveals)} word marker(s) resolved -> index.reveals.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
