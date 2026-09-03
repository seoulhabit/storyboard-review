#!/usr/bin/env python3
"""Generate compositions/frames/*.html for ACT 1.

Scene durations are read from the MEASURED voiceover takes in assets/voice/,
never authored by hand -- the VO is the master clock. Re-run after any new take.

Layouts are landscape-NATIVE, not portrait layouts stretched. The 9:16 failure
mode is a small element marooned in a tall empty column; the 16:9 failure mode is
a full-width band of text with no depth behind it. Each scene below uses a shape a
wide frame actually affords: two-column, three-across, or a left-to-right process.
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _preamble import scene
from frames_a27 import SCENES_A27

ROOT = Path(__file__).resolve().parent.parent
TAIL_PAD = 0.15   # scene breath BEYOND the 250ms silent tail pad_vo.py adds to
                  # every take (total ~0.40s after the last word, as before)


def vo_duration(n):
    p = ROOT / "assets" / "voice" / f"{n:02d}.wav"
    if not p.exists():
        return None
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip()
    return float(out)


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
          <h1 class="s1-claim" id="s1-claim">Your next favourite skincare
            ingredient may have been invented by <em>bacteria trying not to die.</em></h1>
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
  // FRAME ZERO IS THE HOOK: the claim is already at rest at t=0, not mid-fade.
  // Only the strike-throughs are animated, so the export's literal first frame
  // is the composed hook and a viable thumbnail candidate.
  tl.set('#s1-claim', { opacity: 1, y: 0 }, 0);
  tl.fromTo('#s1-i1', { opacity:0, x:52 }, { opacity:1, x:0, duration:0.45 }, 3.10);
  tl.fromTo('#s1-i2', { opacity:0, x:52 }, { opacity:1, x:0, duration:0.45 }, 3.45);
  tl.fromTo('#s1-i3', { opacity:0, x:52 }, { opacity:1, x:0, duration:0.45 }, 3.80);
  tl.fromTo('#s1-b1', { scaleX:0 }, { scaleX:1, duration:0.30, ease:'power2.inOut' }, 5.05);
  tl.to('#s1-i1', { color:'#131516', duration:0.30 }, 5.05);  // --ink on coral = 5.60:1
  tl.fromTo('#s1-b2', { scaleX:0 }, { scaleX:1, duration:0.30, ease:'power2.inOut' }, 6.45);
  tl.to('#s1-i2', { color:'#131516', duration:0.30 }, 6.45);  // --ink on coral = 5.60:1
  tl.fromTo('#s1-b3', { scaleX:0 }, { scaleX:1, duration:0.30, ease:'power2.inOut' }, 7.95);
  tl.to('#s1-i3', { color:'#131516', duration:0.30 }, 7.95);  // --ink on coral = 5.60:1
  // Fills the dead 8.25-10.49 tail with the scene's actual payoff, not filler.
  tl.fromTo('#s1-mark', { opacity:0, y:52 }, { opacity:1, y:0, duration:0.60 }, 8.60);
  tl.fromTo('#s1-claim', { y:0 }, { y:-14, duration:1.60, ease:'power1.inOut' }, 8.60);
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
  tl.fromTo('#s2-l2', { opacity:0, y:44 }, { opacity:1, y:0, duration:0.50 }, 6.30);
  tl.set('#s2-cell', { attr:{ r:150 } }, 0);
  tl.to('#s2-cell', { attr:{ r:112 }, duration:2.6, ease:'power2.inOut' }, 4.20);
  tl.to('#s2-cell', { attr:{ stroke:'#C97A5C' }, duration:0.9 }, 6.85);  // after the radius tween ends at 6.80, not inside it
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
                          transformOrigin:'50% 50%' }, 5.40);
  tl.fromTo('#s3-rule', { scaleX:0 }, { scaleX:1, duration:0.70, ease:'power2.inOut' }, 6.50);
  tl.fromTo('#s3-sub',  { opacity:0, y:36 }, { opacity:1, y:0, duration:0.50 }, 7.20);
  // Vessels drain back slightly on the closing beat -- a real state change tied to
  // the line ("stranger than the marketing"), across the otherwise-dead tail.
  tl.to(['#s3-f1','#s3-f2','#s3-f3'], { scaleY:0.30, duration:1.70,
                                         ease:'power1.inOut', stagger:0.10 }, 8.20);
  // The lockup arrives as a full-width dark band, then floods aqua -- two
  // large-area beats replacing a wordmark fade that measured as nothing.
  tl.fromTo('#s3-lockup', { opacity:0, scaleY:0.4, transformOrigin:'50% 50%' },
                          { opacity:1, scaleY:1, duration:0.55, ease:'power3.out' }, 5.10);
  tl.fromTo('#s3-wash', { scaleX:0 }, { scaleX:1, duration:0.90,
                                        ease:'power2.inOut' }, 6.90);
  tl.to('#s3-mark', { color:'#131516', duration:0.50 }, 7.10);
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
  tl.fromTo('#s4-sx',   { opacity:0, x:44 }, { opacity:1, x:0, duration:0.45 }, 3.90);
  tl.fromTo('#s4-sb', { scaleX:0 }, { scaleX:1, duration:0.32, ease:'power2.inOut' }, 5.60);
  tl.to('#s4-sx', { color:'#131516', duration:0.32 }, 5.60);  // --ink on coral = 5.60:1
  tl.fromTo('#s4-d1', { opacity:0, y:44 }, { opacity:1, y:0, duration:0.55 }, 6.60);
  // The definition panel floods on "extreme" -- a real large-area beat in the
  // back half, where the scene previously held for 6.6s on a 1.04 text scale.
  tl.fromTo('#s4-defbox', { opacity:0, y:44 }, { opacity:1, y:0, duration:0.55 }, 6.50);
  tl.fromTo('#s4-defwash', { scaleX:0 }, { scaleX:1, duration:0.95,
                                           ease:'power2.inOut' }, 8.60);
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
  tl.fromTo('#s5-note', { opacity:0, y:44 }, { opacity:1, y:0, duration:0.55 }, 4.60);
  tl.fromTo('#s5-cite', { opacity:0 },       { opacity:1, duration:0.45 }, 6.20);
  tl.to('#s5-crystals', { rotation:2.2, transformOrigin:'50% 50%',
                          duration:5.0, ease:'none' }, 5.60);
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
                       ease: 'power1.in' }, 4.30 + i * 0.11);
    // Second wave: refill, then leave again. Without it the middle column is
    // genuinely empty for the back half of the scene -- caught by the
    // region-aware content-void check, not by the whole-frame one.
    tl.to('#w-' + i, { x: 0, y: 0, opacity: 0.55, duration: 0.01 }, 7.30 + i * 0.04);
    tl.to('#w-' + i, { x: 150, y: -22, opacity: 0, duration: 1.30,
                       ease: 'power1.in' }, 7.90 + i * 0.09);
  }
  // The vessel outline persists for the whole scene, so the step never goes blank.
  // Hidden state is authored in the SVG attribute, NOT tl.set(...,0): a zero-duration
  // set at position 0 does not render while the playhead sits exactly at 0, so frame 0
  // would show it un-hidden (engine lint: gsap_timeline_set_initial_hide).
  tl.to('#s6-vessel', { opacity: 1, duration: 0.45 }, 3.70);
  tl.fromTo('#s6-h',  { opacity:0, y:20 }, { opacity:1, y:0, duration:0.50 }, 0.15);
  tl.fromTo('#s6-s1', { opacity:0, y:52 }, { opacity:1, y:0, duration:0.50 }, 1.30);
  tl.fromTo('#s6-s2', { opacity:0, y:52 }, { opacity:1, y:0, duration:0.50 }, 3.60);
  tl.fromTo('#s6-s3', { opacity:0, y:52 }, { opacity:1, y:0, duration:0.50 }, 7.10);
  // Each card's ground fills as its step becomes active -- three ~11%-of-frame
  // beats spread across the hold, where the SVG strokes alone were invisible.
  tl.fromTo('#s6-fill1', { scaleY:0 }, { scaleY:1, duration:0.60, ease:'power2.out' }, 2.20);
  tl.fromTo('#s6-fill2', { scaleY:0 }, { scaleY:1, duration:0.60, ease:'power2.out' }, 4.60);
  tl.to('#s6-fill1', { scaleY:0.14, duration:0.60, ease:'power2.inOut' }, 4.60);
  tl.fromTo('#s6-fill3', { scaleY:0 }, { scaleY:1, duration:0.60, ease:'power2.out',
                                         backgroundColor:'#C97A5C' }, 7.90);
  tl.to('#s6-fill2', { scaleY:0.14, duration:0.60, ease:'power2.inOut' }, 7.90);
  // The protein visibly loses its fold -- the claim the label makes, drawn.
  tl.fromTo('#s6-p3', { attr:{ d:'M40,150 C70,60 110,60 150,105 C190,150 230,150 260,60' } },
                      { attr:{ d:'M40,150 C86,128 96,168 150,138 C206,108 214,166 260,132' },
                        duration:1.60, ease:'power2.inOut' }, 7.70);
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
            <em>stressed human skin?</em></p>
        </div>
      </div>
    </div>"""
S7_TL = """
  // Act hook: the scene ENDS on the open question the next act answers, rather
  // than summarising this one. A chapter boundary is where a viewer leaves.
  tl.fromTo('#s7-k',    { opacity:0, y:30 }, { opacity:1, y:0, duration:0.40 }, 0.20);
  tl.fromTo('#s7-line', { opacity:0, y:44 }, { opacity:1, y:0, duration:0.55 }, 0.55);
  tl.fromTo('#s7-q',    { opacity:0, y:58 }, { opacity:1, y:0, duration:0.70 }, 4.40);
  tl.to('#s7-line', { opacity:0.42, duration:0.80 }, 4.60);
  tl.fromTo('#s7-q', { scale:1 }, { scale:1.03, duration:3.0, ease:'none',
                                    transformOrigin:'0% 50%' }, 6.60);
"""

SCENES = [
    # ACT 1 (pilot, already validated)
    ("01-hook",       1, S1_BODY, S1_CSS, S1_TL),
    ("02-osmosis",    2, S2_BODY, S2_CSS, S2_TL),
    ("03-now",        3, S3_BODY, S3_CSS, S3_TL),
    ("04-extremolyte",4, S4_BODY, S4_CSS, S4_TL),
    ("05-halomonas",  5, S5_BODY, S5_CSS, S5_TL),
    ("06-mechanism",  6, S6_BODY, S6_CSS, S6_TL),
    ("07-question",   7, S7_BODY, S7_CSS, S7_TL),
] + [
    # ACTS 2-7 -- authored to the corrected (panel-scale) beat vocabulary.
    (cid, vo, spec["body"], spec["css"], spec["tl"]) for cid, spec, vo in SCENES_A27
]


def main():
    out = ROOT / "compositions" / "frames"
    out.mkdir(parents=True, exist_ok=True)
    rows, missing = [], []
    for cid, vo_n, body, css, tlj in SCENES:
        d = vo_duration(vo_n)
        if d is None:
            missing.append(vo_n); continue
        dur = round(d + TAIL_PAD, 3)
        (out / f"{cid}.html").write_text(scene(cid, dur, body, css, tlj))
        rows.append((cid, vo_n, d, dur))
    print(f"{'scene':16s} {'vo':>4s} {'vo_dur':>8s} {'scene_dur':>10s}")
    total = 0.0
    for cid, n, d, dur in rows:
        print(f"{cid:16s} {n:4d} {d:8.3f} {dur:10.3f}")
        total += dur
    print(f"{'TOTAL':16s} {'':4s} {'':8s} {total:10.3f}")
    if missing:
        print(f"\nMISSING VO takes (scenes not written): {missing}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
