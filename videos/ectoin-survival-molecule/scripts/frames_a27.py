"""Scene definitions for ACTS 2-7 (scenes 08-29).

Every scene here is authored to the CORRECTED BEAT VOCABULARY established by the
Act 1 pilot. Measured there: word-scale beats (text fades, 5px strike bars) moved
4-5.8% of 8fps steps past a perceptibility floor, against 11.7-23.1% on the
channel's shipped 9:16 work. Cause is grid share, not size -- on a 1920-wide frame
a headline sits inside a column and changes ~0.7% of the pixels.

So the rule for everything below: A BEAT MOVES A PANEL OR A COLUMN, never a word.
Washes sweeping across a card, whole panels entering and leaving, grounds
inverting, grids filling. Text still animates, but never as a scene's only beat.
"""
from build_storyboard import CHAPTERS

# ---- shared chapter-band component (into 08, 12, 16, 22, 26; see
# scripts/transitions.py KIND["chapter"]) ---------------------------------
# An in-scene overlay carrying the CHAPTERS title as a kicker: washes in
# (moss fill, paper text -- the project's one safe dark-wash pairing) at
# 0.05s, holds through the wipe, then recedes at 1.6s so it never competes
# with the scene's own content, which lands on its own word-bound beats
# underneath. Kept INSIDE the safe box (never full-bleed) -- a full-bleed
# band was the exact shape of failure the hard safe-area gate caught before
# (see _preamble.py's BASE comment on the first render's 81 flagged frames).
CHBAND_CSS = """
    /* top/left/right are offset from #root's own edge (the chband div is a
       sibling of .stage, not nested inside it), so the safe-area tokens are
       spelled out explicitly here -- never 0, which would bleed the wash to
       the true canvas edge. See the hard safe-area gate note above. */
    /* top:calc(safe-top + 3px), not bare var(--safe-top): the hard safe-area
       gate measured this band's own rendered edge 2px into the reserved zone
       (rounded-corner antialiasing/H.264 edge blur softening a couple of
       rows outward beyond the CSS-computed line) -- a small buffer absorbs
       that without being visible. */
    .chband { position:absolute; top:calc(var(--safe-top) + 3px); left:calc(var(--safe-left) + var(--safe-buffer));
              right:calc(var(--safe-right) + var(--safe-buffer)); height:112px;
              display:flex; align-items:center; overflow:hidden;
              border-radius:var(--r-3); z-index:10; padding:0 var(--s-6); }
    .chband .kicker { position:relative; z-index:1; font-size:var(--t-frame);
                       letter-spacing:var(--tr-mono); }
"""


def chband_body(cid):
    return (f'      <div class="chband" id="ch-band">\n'
            f'        <div class="wash moss" id="ch-wash"></div>\n'
            f'        <p class="kicker" id="ch-title">{CHAPTERS[cid]}</p>\n'
            f'      </div>')


CHBAND_TL = """
  // Chapter band: washes in over the wipe, recedes at 1.6s -- see CHBAND_CSS.
  tl.fromTo('#ch-wash', { scaleX:0 }, { scaleX:1, duration:0.45, ease:'power2.inOut' }, 0.05);
  // The band WIPES out, it does not dissolve. A dissolve necessarily spends its
  // whole exit at a contrast the band never has when it is being read: measured
  // 5.42:1 at 1.0s and 1.29:1 at 1.94s, mid-fade, on the same element. Wiping
  // the container (it already has overflow:hidden) removes the band without
  // ever putting translucent type on screen -- and it echoes the wash that
  // brought it in.
  tl.to('#ch-band', { clipPath:'inset(0% 0% 0% 100%)', duration:0.45,
                      ease:'power2.inOut' }, 1.6);
  tl.set('#ch-band', { opacity:0 }, 2.10);
"""

# NOTE (2026-09-02): copy inside a washed container is ALWAYS wrapped in an
# element. `.wash ~ *` can only lift an ELEMENT above the wash, and
# `.wash.moss ~ *` can only recolour one; a bare text node gets neither, so the
# wash paints straight over it and the card renders blank. Scene 28's payoff
# line shipped that way -- struck by its own wash at 1.72:1 instead of reading
# paper-on-moss at 5.42:1. The `.wash:only-child` dashed-outline guard could not
# catch it either, because :only-child counts elements and a text node is not one.

# ---------------------------------------------------------------- 08 humectant
S08 = dict(css="""
    #root { background:var(--paper); color:var(--ink); }
    .g2 { display:grid; grid-template-columns:1fr 1fr; gap:var(--s-6); height:100%; }
    .g2.tilt { grid-template-columns:0.62fr 1.38fr; }
    .g2 .panel { display:flex; flex-direction:column; }
    .drop { position:absolute; border-radius:50%; background:var(--aqua); }
""" + CHBAND_CSS, body=chband_body("08-humectant") + """
    <div class="stage">
      <div class="g2" id="g2-grid">
        <div class="panel" id="p-hum">
          <div class="wash dim" id="w-hum"></div>
          <p class="kicker">A familiar humectant</p>
          <p class="p-title">Glycerin.<br>Hyaluronic acid.</p>
          <p class="p-body">Attracts water and holds onto it.</p>
          <svg viewBox="0 0 400 260" width="100%" height="200" style="margin-top:auto"
               aria-hidden="true"><g id="hum-dots"></g>
            <circle cx="200" cy="130" r="52" fill="#6B6B6B"/></svg>
        </div>
        <div class="panel" id="p-ect">
          <div class="wash aqua" id="w-ect"></div>
          <p class="kicker" style="color:var(--ink)">Ectoin</p>
          <p class="p-title">Works on how water<br>arranges itself.</p>
          <p class="p-body" style="color:var(--ink)">Around proteins and membranes.</p>
          <svg viewBox="0 0 400 260" width="100%" height="200" style="margin-top:auto"
               aria-hidden="true"><g id="ect-dots"></g>
            <circle cx="200" cy="130" r="52" fill="#131516"/></svg>
        </div>
      </div>
    </div>""", tl="""
  // PANEL-SCALE: each panel is ~45% of the frame; its entrance and its colour
  // wash are the beats. The dot behaviour is the explanation on top of them.
  // Chapter opener: first spoken beat bound to @first.
  tl.fromTo('#p-hum', { opacity:0, x:-120 }, { opacity:1, x:0, duration:0.65 }, @first);
  tl.fromTo('#w-hum', { scaleX:0 }, { scaleX:1, duration:0.80, ease:'power2.inOut' }, 2.40);
  var hd = document.getElementById('hum-dots'), ed = document.getElementById('ect-dots');
  for (var i = 0; i < 14; i++) {
    var a = i * (360/14) * Math.PI/180;
    for (var k = 0; k < 2; k++) {
      var g = k ? ed : hd;
      var c = document.createElementNS('http://www.w3.org/2000/svg','circle');
      c.setAttribute('cx', (200 + Math.cos(a)*150).toFixed(1));
      c.setAttribute('cy', (130 + Math.sin(a)*105).toFixed(1));
      c.setAttribute('r', 11); c.setAttribute('fill', '#59B8AE');
      c.id = (k ? 'e' : 'h') + '-' + i; g.appendChild(c);
    }
    // humectant: water is PULLED IN and absorbed
    tl.to('#h-' + i, { x:-Math.cos(a)*95, y:-Math.sin(a)*66, duration:1.3,
                       ease:'power2.in' }, 4.00 + i*0.05);
    // ectoin: water STAYS OUT, but organises into an even shell
    tl.to('#e-' + i, { x:-Math.cos(a)*38, y:-Math.sin(a)*27, duration:1.4,
                       ease:'power2.inOut' }, 10.40 + i*0.05);
  }
  // The second panel is held back to land on the VO's third sentence, which is
  // where it belongs -- and it spreads the beats across all 16.8s instead of
  // stacking them in the first third (measured: a 10.00s frozen stretch).
  tl.fromTo('#p-ect', { opacity:0, x:120 }, { opacity:1, x:0, duration:0.65 }, 8.30);
  tl.fromTo('#w-ect', { scaleX:0 }, { scaleX:1, duration:0.85, ease:'power2.inOut' }, 9.40);
  tl.to('#p-hum', { opacity:0.40, duration:0.80 }, 9.40);
  // closing beat: the organised shell settles, so the back half is not dead air
  // The grid REWEIGHTS toward ectoin in the back half: ~15% of the frame moves,
  // where 14 small dots scaling by 1.06 measured as nothing (per-step 0.1).
  tl.to('#p-hum', { scaleX:0.62, transformOrigin:'0% 50%', duration:1.10,
                    ease:'power2.inOut' }, 11.90);
  tl.to('#p-ect', { scaleX:1.30, x:-150, transformOrigin:'100% 50%', duration:1.10,
                    ease:'power2.inOut' }, 11.90);
  tl.to('#p-hum', { opacity:0.18, duration:1.20 }, 14.30);
""" + CHBAND_TL)

# ------------------------------------------------------- 09-exclusion (merged)
# Scenes 09 and 10 merged into one continuous scene/diagram (external review,
# approved cut): the tidy version and the honest correction now share a single
# annular diagram at identical geometry, and the correction arrives as a
# GROUND INVERSION -- a clip-path sweep of the ink layer over the paper one --
# rather than a hard scene cut. Word-bound to the real cut voiceover
# (assets/voice/09.words.json); tokens confirmed against
# `python3 scripts/timing.py --words 09-exclusion` before writing.
S09 = dict(css="""
    #root { background:var(--paper); color:var(--ink); }
    .world.ink { background:var(--ink); color:var(--paper); clip-path:inset(0% 0% 0% 100%); }
    .g9 { display:grid; grid-template-columns:44fr 56fr; gap:var(--s-8);
          align-items:center; height:100%; }
    .g9 .stage { padding:var(--safe-top) var(--safe-right) var(--safe-bottom) var(--safe-left); }
""", body="""    <div class="world" id="w-paper">
      <div class="stage"><div class="g9">
        <div class="col">
          <p class="kicker">The mechanism</p>
          <p class="hero" id="e-term">Preferential<br>exclusion</p>
          <p class="p-body" id="e-sub" style="margin-top:20px">The tidy version.</p>
        </div>
        <svg viewBox="0 0 620 620" width="100%" height="100%" aria-hidden="true">
          <circle id="e-shell" cx="310" cy="310" r="190" fill="none"
                  stroke="#59B8AE" stroke-width="46" opacity="0.30"/>
          <circle id="e-prot" cx="310" cy="310" r="112" fill="#131516"/>
          <g id="e-ring"></g>
          <text id="e-lab" x="310" y="322" text-anchor="middle" fill="#F7F5F0"
                font-family="Inter, sans-serif" font-weight="800" font-size="36"
                opacity="0">PROTEIN</text>
        </svg>
      </div></div>
    </div>
    <div class="world ink" id="w-ink">
      <div class="stage"><div class="g9">
        <div class="col">
          <p class="kicker on-ink">The mechanism</p>
          <p class="hero" id="m-h">The honest version<br>is <em style="font-style:normal;color:var(--coral)">messier.</em></p>
          <p class="p-body on-ink" id="m-note" style="margin-top:20px">In the simulations,
            ectoin also showed some attraction to that surface. And how far it stays back
            depends on how tightly the protein&rsquo;s own water is already arranged.</p>
        </div>
        <svg viewBox="0 0 620 620" width="100%" height="100%" aria-hidden="true">
          <circle cx="310" cy="310" r="190" fill="none" stroke="#59B8AE"
                  stroke-width="46" opacity="0.30"/>
          <circle cx="310" cy="310" r="112" fill="#F7F5F0"/>
          <g id="m-ring"></g>
        </svg>
      </div></div>
    </div>""", tl="""
  // ---- w-paper: the tidy version. Same three-layer diagram build as before. ----
  tl.fromTo('#e-term', { opacity:0, y:40 }, { opacity:1, y:0, duration:0.55 }, 0.15);
  tl.fromTo('#e-prot', { attr:{ r:0 } }, { attr:{ r:112 }, duration:0.75,
                                           ease:'back.out(1.4)' }, 1.30);
  tl.to('#e-lab', { opacity:1, duration:0.40 }, 1.90);
  tl.fromTo('#e-shell', { attr:{ r:112 }, opacity:0 },
                        { attr:{ r:190 }, opacity:0.30, duration:1.00,
                          ease:'power2.out' }, 3.20);
  var ring = document.getElementById('e-ring');
  for (var i = 0; i < 18; i++) {
    var a = i * 20 * Math.PI/180;
    var d = document.createElementNS('http://www.w3.org/2000/svg','rect');
    var x = 310 + Math.cos(a)*268, y = 310 + Math.sin(a)*268;
    d.setAttribute('x', x-13); d.setAttribute('y', y-13);
    d.setAttribute('width', 26); d.setAttribute('height', 26);
    d.setAttribute('fill', '#C97A5C'); d.setAttribute('opacity', 0);
    d.setAttribute('transform', 'rotate(45 ' + x.toFixed(1) + ' ' + y.toFixed(1) + ')');
    d.id = 'x-' + i; ring.appendChild(d);
    tl.to('#x-' + i, { opacity:1, duration:0.35 }, 4.20 + i*0.05);
  }
  tl.fromTo('#e-sub', { opacity:0 }, { opacity:1, duration:0.45 }, @w(version)-0.30);
  tl.to('#e-shell', { attr:{ 'stroke-width':78 }, opacity:0.55, duration:1.40,
                      ease:'power2.inOut' }, 5.20);

  // ---- ground inversion on "the honest version" -- the scene's single largest
  // beat: a full-frame clip-path sweep, paired with a small child travel on
  // the ring (pairs a clipPath-only tween with real motion, per this
  // project's keepsMoving rule) and the headline settling in from y:24. ----
  var inv = @w(honest)-0.45;
  tl.fromTo('#w-ink', { clipPath:'inset(0% 0% 0% 100%)' },
                      { clipPath:'inset(0% 0% 0% 0%)', duration:0.60,
                        ease:'power3.inOut' }, inv);
  tl.fromTo('#m-ring', { rotation:0, transformOrigin:'310px 310px' },
                       { rotation:6, transformOrigin:'310px 310px', duration:1.40,
                         ease:'power2.out' }, inv);
  tl.fromTo('#m-h', { y:24, opacity:0.4 }, { y:0, opacity:1, duration:0.60,
                                             ease:'power2.out' }, inv);

  // ---- w-ink: the honest correction, on the SAME diagram geometry. ----
  // Ring rebuild timed to @w(simulations) -- that is the word that names
  // the evidence backing the correction, not the ground-flip itself.
  var sim = @w(simulations);
  var mring = document.getElementById('m-ring');
  for (var j = 0; j < 18; j++) {
    var aj = j * 20 * Math.PI/180;
    var xj = 310 + Math.cos(aj)*268, yj = 310 + Math.sin(aj)*268;
    var e = document.createElementNS('http://www.w3.org/2000/svg','rect');
    e.setAttribute('x', xj-13); e.setAttribute('y', yj-13);
    e.setAttribute('width', 26); e.setAttribute('height', 26);
    e.setAttribute('fill', '#C97A5C'); e.setAttribute('opacity', 0);
    e.setAttribute('transform', 'rotate(45 ' + xj.toFixed(1) + ' ' + yj.toFixed(1) + ')');
    e.id = 'y-' + j; mring.appendChild(e);
    tl.to('#y-' + j, { opacity:1, duration:0.30 }, sim + j*0.03);
    // a third break ranks toward the protein surface -- @w(attraction), the
    // actual finding named in the VO, drawn as real motion, not decoration.
    if (j % 3 === 0) {
      tl.to('#y-' + j, { x:-Math.cos(aj)*140, y:-Math.sin(aj)*140, fill:'#E0A32B',
                         duration:1.4, ease:'power2.inOut' }, @w(attraction)-0.8);
    }
  }
  // "depends on how tightly ... already arranged" -- the shell itself
  // destabilises, a full-annulus rotation timed to the closing clause.
  tl.to('#m-ring', { rotation:14, transformOrigin:'310px 310px', duration:2.60,
                     ease:'power1.inOut' }, @w(depends));
  tl.to('#m-note', { opacity:0.75, duration:0.60 }, @w(arranged));
""")

# ---------------------------------------------------------------- 11 analogy
S11 = dict(css="""
    #root { background:var(--paper); color:var(--ink); }
    .g11 { display:grid; grid-template-columns:46fr 54fr; gap:var(--s-8);
           align-items:center; height:100%; }
""", body="""    <div class="stage">
      <div class="g11">
        <div class="col">
          <p class="kicker">One way to picture it</p>
          <p class="fig" id="a-l1">A celebrity inside a ring of security.</p>
          <p class="fig" id="a-l2" style="margin-top:24px;opacity:0">Ectoin is not hugging
            the celebrity. It hangs back &mdash; and helps the ring
            <em style="font-style:normal;color:var(--moss)">hold its shape</em>.</p>
        </div>
        <svg viewBox="0 0 620 560" width="100%" height="100%" aria-hidden="true">
          <g id="a-guard"></g>
          <circle id="a-star" cx="310" cy="280" r="76" fill="#E0A32B" opacity="0"/>
          <g id="a-ect"></g>
        </svg>
      </div>
    </div>""", tl="""
  tl.fromTo('#a-l1', { opacity:0, y:40 }, { opacity:1, y:0, duration:0.55 }, 0.15);
  // power3.out, not back.out -- a settling entrance rather than an overshoot,
  // to read as arriving INSIDE the ring rather than bouncing into place.
  tl.fromTo('#a-star', { opacity:0, scale:0.86, transformOrigin:'310px 280px' },
                       { opacity:1, scale:1, duration:0.60, ease:'power3.out' }, 1.20);
  var g = document.getElementById('a-guard'), e = document.getElementById('a-ect');
  for (var i = 0; i < 12; i++) {
    var a = i * 30 * Math.PI/180;
    var c = document.createElementNS('http://www.w3.org/2000/svg','circle');
    c.setAttribute('cx', 310 + Math.cos(a)*150); c.setAttribute('cy', 280 + Math.sin(a)*150);
    c.setAttribute('r', 30); c.setAttribute('fill', '#4F6B52'); c.setAttribute('opacity', 0);
    c.id = 'g-' + i; g.appendChild(c);
    // The guard ring lands on the word that names it.
    tl.to('#g-' + i, { opacity:1, duration:0.30 }, @w(security) + i*0.06);
    var d = document.createElementNS('http://www.w3.org/2000/svg','rect');
    var x = 310 + Math.cos(a+0.26)*250, y = 280 + Math.sin(a+0.26)*250;
    d.setAttribute('x', x-13); d.setAttribute('y', y-13);
    d.setAttribute('width', 26); d.setAttribute('height', 26);
    d.setAttribute('fill', '#C97A5C'); d.setAttribute('opacity', 0);
    d.setAttribute('transform', 'rotate(45 ' + x.toFixed(1) + ' ' + y.toFixed(1) + ')');
    d.id = 'ee-' + i; e.appendChild(d);
    // The ectoin squares land on "hangs" (back) -- the beat that describes them.
    tl.to('#ee-' + i, { opacity:1, duration:0.30 }, @w(hangs) + i*0.06);
  }
  tl.fromTo('#a-l2', { opacity:0, y:34 }, { opacity:1, y:0, duration:0.55 }, @w(hangs)+1.60);
  // the ring visibly TIGHTENS on "hold" -- a large synchronised move, the
  // scene's last beat, landing exactly on the word it illustrates.
  tl.to('#a-guard', { scale:0.94, transformOrigin:'310px 280px', duration:1.6,
                      ease:'power2.inOut' }, @w(hold));
""")

# ---------------------------------------------------------------- 12 load
S12 = dict(css="""
    #root { background:var(--paper); color:var(--ink); }
    .g12 { display:flex; flex-direction:column; justify-content:center;
           gap:var(--s-6); height:100%; }
    .stressors { display:grid; grid-template-columns:repeat(5,1fr); gap:var(--s-4); }
    .st { background:var(--ink); color:var(--paper); border-radius:var(--r-3);
          padding:var(--s-5) var(--s-4); text-align:center;
          font-family:var(--font-body); font-weight:800; font-size:var(--t-body);
          min-height:0; }
    .barrier { position:relative; height:150px; background:var(--mist);
               border-radius:var(--r-3); overflow:hidden; }
    .barrier .brick { position:absolute; background:var(--celadon);
                      border:3px solid var(--paper); }
""" + CHBAND_CSS, body=chband_body("12-load") + """
    <div class="stage">
      <div class="g12">
        <p class="fig" id="l-h">Your outer barrier is under constant load.</p>
        <div class="stressors">
          <div class="st" id="st-0">Dry air</div>
          <div class="st" id="st-1">Cleansing</div>
          <div class="st" id="st-2">Pollution</div>
          <div class="st" id="st-3">Sun</div>
          <div class="st" id="st-4">Strong actives</div>
        </div>
        <div class="barrier" id="l-wall"></div>
        <p class="p-body" id="l-note">Water escapes more easily. Skin can feel tight,
          rough, or unusually reactive.</p>
      </div>
    </div>""", tl="""
  // Five full-height cards, each ~9% of the frame, entering across 5.5s -- the
  // enumeration in the VO is slow (measured 110wpm on the comma list), so the
  // beats are spread to match it rather than clustered at the top.
  for (var i = 0; i < 5; i++) {
    tl.fromTo('#st-' + i, { opacity:0, y:60 },
                          { opacity:1, y:0, duration:0.45 }, 2.20 + i*0.95);
  }
  var wall = document.getElementById('l-wall');
  for (var r = 0; r < 3; r++) for (var c = 0; c < 12; c++) {
    var b = document.createElement('div');
    b.className = 'brick';
    // 12 x 8% = 96%, leaving 4% for the odd-row stagger -- so a staggered row
    // ends exactly at 100% instead of 70px past the container's clip edge.
    b.style.left = (c*8 + (r%2?4:0)) + '%'; b.style.top = (r*50) + 'px';
    b.style.width = '8%'; b.style.height = '50px';
    b.id = 'bk-' + r + '-' + c; wall.appendChild(b);
  }
  // Chapter opener: first spoken beat bound to @first.
  tl.fromTo('#l-h', { opacity:0, y:34 }, { opacity:1, y:0, duration:0.50 }, @first);
  // the wall visibly loosens as the stressors land -- one large synchronised move
  for (var r2 = 0; r2 < 3; r2++) for (var c2 = 0; c2 < 12; c2++) {
    tl.to('#bk-' + r2 + '-' + c2,
          { y: (r2 === 0 ? -10 : r2 === 1 ? 4 : 12) + (c2 % 3) * 3,
            backgroundColor:'#C97A5C', duration:1.8, ease:'power1.inOut' },
          9.60 + c2*0.05);
  }
  tl.fromTo('#l-note', { opacity:0 }, { opacity:1, duration:0.55 }, 12.60);
  // The whole barrier band recolours and opens up -- ~8% of the frame, against
  // brick nudges that measured as no beat at all.
  // Recolour the BRICKS, not the wall's background -- the bricks cover it almost
  // completely, so the previous background tween changed nothing visible. And
  // displace them far enough to register (10px did not).
  for (var r3 = 0; r3 < 3; r3++) for (var c3 = 0; c3 < 12; c3++) {
    tl.to('#bk-' + r3 + '-' + c3,
          // --ink, NOT --coral: celadon->coral is a 27-luma step and measured as
          // no beat at all, despite reading as a big hue change to the eye.
          { backgroundColor:'#131516', duration:0.90 }, 11.80 + c3*0.07);
    tl.to('#bk-' + r3 + '-' + c3,
          { y: (r3 === 0 ? -34 : r3 === 1 ? 8 : 30) + (c3 % 3) * 9,
            rotation: (c3 % 5 - 2) * 3, duration:1.70, ease:'power2.inOut' },
          14.10 + c3*0.05);
  }
""" + CHBAND_TL)

# ---------------------------------------------------------------- 13 keratin
S13 = dict(css="""
    #root { background:var(--paper); color:var(--ink); }
    .g13 { display:grid; grid-template-columns:46fr 54fr; gap:var(--s-8);
           align-items:center; height:100%; }
""", body="""    <div class="stage">
      <div class="g13">
        <div class="col">
          <p class="kicker">What the lab work shows</p>
          <p class="fig" id="k-h">One study found ectoin changed how
            <em style="font-style:normal;color:var(--moss)">keratin</em> behaves
            with water.</p>
          <p class="p-body" id="k-s" style="margin-top:20px">Keratin is the main protein
            in our outer skin cells.</p>
          <div style="margin-top:28px"><span class="cite" id="k-cite">Biochem Biophys Rep &middot; 2021</span></div>
        </div>
        <svg viewBox="0 0 620 520" width="100%" height="100%" aria-hidden="true">
          <g id="k-strands"></g>
        </svg>
      </div>
    </div>""", tl="""
  // The whole strand field re-arranges from bundled to dispersed. Every strand
  // moves at once -- a large-area transformation, not a label change.
  var g = document.getElementById('k-strands');
  var N = 22;
  for (var i = 0; i < N; i++) {
    var p = document.createElementNS('http://www.w3.org/2000/svg','rect');
    p.setAttribute('x', 250 + (i%4)*22); p.setAttribute('y', 90 + Math.floor(i/4)*54);
    p.setAttribute('width', 16); p.setAttribute('height', 44);
    p.setAttribute('rx', 8); p.setAttribute('fill', '#4F6B52');
    p.id = 'ks-' + i; g.appendChild(p);
    tl.set('#ks-' + i, { opacity:0 }, 0);
    tl.to('#ks-' + i, { opacity:1, duration:0.30 }, 0.60 + i*0.035);
    // disperse: spread across the full width of the figure
    tl.to('#ks-' + i, { x:(i%6)*84 - 210, y:(Math.floor(i/6)%4)*26 - 30,
                        rotation:(i%5-2)*14, transformOrigin:'50% 50%',
                        duration:1.9, ease:'power2.inOut' }, 6.30 + (i%6)*0.07);
    // Second large-area beat, back half of the scene: the field itself is
    // what "keratin, the main protein" refers to on screen, so it pulses on
    // that word rather than sitting inert while the sentence keeps going.
    tl.to('#ks-' + i, { scale:1.14, duration:0.40, ease:'power2.out',
                        transformOrigin:'50% 50%' }, @w(keratin) + i*0.02);
    tl.to('#ks-' + i, { scale:1, duration:0.55, ease:'power2.inOut' },
                        @w(keratin) + i*0.02 + 0.40);
  }
  tl.fromTo('#k-h', { opacity:0, y:36 }, { opacity:1, y:0, duration:0.55 }, 0.20);
  tl.fromTo('#k-s', { opacity:0 }, { opacity:1, duration:0.45 }, 4.60);
  // The strand field arrives as one bundle before it disperses, so the first
  // half of the scene carries a large-area beat too.
  tl.fromTo('#k-strands', { scale:0.55, opacity:0.35, transformOrigin:'310px 260px' },
                          { scale:1, opacity:1, duration:1.60,
                            ease:'power3.out' }, 2.30);
  tl.fromTo('#k-cite', { opacity:0 }, { opacity:1, duration:0.45 }, 8.60);
  // Third beat, spans "behaves with water": the whole field tints toward
  // hydrated blue-green and back, a real colour change across every strand
  // rather than a caption update, carrying the otherwise-dead close of a
  // scene this take reads much slower than the copy was first blocked for.
  tl.to('#k-strands', { filter:'saturate(1.6) hue-rotate(-12deg)',
                        duration:0.55, ease:'power2.inOut' }, @w(water)-0.35);
  tl.to('#k-strands', { filter:'saturate(1) hue-rotate(0deg)',
                        duration:0.80, ease:'power2.inOut' }, @w(water)+0.20);
""")

# ---------------------------------------------------------------- 14 not a force field
S14 = dict(css="""
    #root { background:var(--ink); color:var(--paper); }
    .g14 { display:grid; grid-template-columns:50fr 50fr; gap:var(--s-8);
           align-items:center; height:100%; }
    .meter { position:relative; height:260px; background:var(--ink-soft);
             border-radius:var(--r-3); overflow:hidden; display:flex;
             align-items:flex-end; }
    .meter .fill { width:100%; height:100%; background:var(--coral);
                   transform:scaleY(0); transform-origin:50% 100%; }
    .meter .cap { position:absolute; left:0; right:0; bottom:16px; text-align:center;
                  font-family:var(--font-mono); font-size:var(--t-label);
                  letter-spacing:var(--tr-mono-wide); color:var(--paper); }
""", body="""    <div class="stage">
      <div class="g14">
        <div class="col">
          <p class="kicker on-ink">The same study, the other way</p>
          <p class="fig" id="f-h">Below five percent humidity, one stress measure
            actually got <em style="font-style:normal;color:var(--coral)">worse</em>.</p>
          <p class="hero" id="f-not" style="margin-top:32px;opacity:0">Not a force field.</p>
        </div>
        <div class="meter" id="f-meter">
          <div class="fill" id="f-fill"></div>
          <div class="cap">DRYING STRESS &middot; &lt;5% RH</div>
        </div>
      </div>
    </div>""", tl="""
  // A full-height meter filling is ~12% of the frame changing colour. That is the
  // beat; the headline is the caption on it.
  tl.fromTo('#f-h', { opacity:0, y:36 }, { opacity:1, y:0, duration:0.55 }, 0.15);
  tl.fromTo('#f-fill', { scaleY:0 }, { scaleY:1, duration:1.60, ease:'power2.inOut' }, 2.40);
  tl.fromTo('#f-not', { opacity:0, y:34 }, { opacity:1, y:0, duration:0.55 }, 5.90);
""")

# ---------------------------------------------------------------- 15 framing
S15 = dict(css="""
    #root { background:var(--paper); color:var(--ink); }
    .g15 { display:flex; align-items:center; height:100%; }
    .band { position:relative; width:100%; background:var(--mist);
            border-radius:var(--r-3); padding:var(--s-8) var(--s-7); overflow:hidden; }
""", body="""    <div class="stage">
      <div class="g15">
        <div class="band" id="fr-band">
          <div class="wash aqua" id="fr-wash"></div>
          <p class="kicker" id="fr-k">So where does that leave it</p>
          <p class="hero" id="fr-h" style="margin-top:16px">A supporting ingredient
            &mdash; not a treatment.</p>
        </div>
      </div>
    </div>""", tl="""
  // One full-width band, ~40% of the frame, entering and then washing colour.
  // A 7.2s scene gets three beats rather than one, spread across the hold.
  tl.fromTo('#fr-band', { opacity:0, scaleY:0.7, transformOrigin:'50% 50%' },
                        { opacity:1, scaleY:1, duration:0.70, ease:'power3.out' }, 0.15);
  tl.fromTo('#fr-k', { opacity:0 }, { opacity:1, duration:0.40 }, 0.65);
  tl.fromTo('#fr-h', { opacity:0, y:40 }, { opacity:1, y:0, duration:0.60 }, 1.10);
  tl.fromTo('#fr-wash', { scaleX:0 }, { scaleX:1, duration:1.10,
                                        ease:'power2.inOut' }, 3.60);
  // Replaces a decorative scale-up that overshot the safe line: the headline
  // resolves to its final two-tone state, which is content, not filler.
  tl.to('#fr-h', { color:'#131516', duration:0.80 }, 5.10);
""")

# ---------------------------------------------------------------- 16 trial 104
S16 = dict(css="""
    #root { background:var(--paper); color:var(--ink); }
    .g16 { display:grid; grid-template-columns:42fr 58fr; gap:var(--s-8);
           align-items:center; height:100%; }
    .cohort { display:grid; grid-template-columns:repeat(13,1fr); gap:7px; }
    /* 104 dots ARE the datum here, so they are a meaningful graphic and owe
       3:1, not decoration. --ink-3 read 2.67:1 on paper. */
    .cohort i { display:block; width:100%; aspect-ratio:1/1; border-radius:50%;
                background:var(--ink-2); }
""" + CHBAND_CSS, body=chband_body("16-trial104") + """
    <div class="stage">
      <div class="g16">
        <div class="col">
          <p class="kicker">Does it do anything to people?</p>
          <p class="hero" id="t-n" style="opacity:0">104</p>
          <p class="fig" id="t-h" style="margin-top:8px">women. A cream with two percent
            ectoin, against the same cream without it.</p>
          <div style="margin-top:26px"><span class="cite" id="t-cite">Skin Pharmacol Physiol &middot; 2007</span></div>
        </div>
        <div class="cohort" id="t-grid"></div>
      </div>
    </div>""", tl="""
  // 104 dots filling a 58% column is the biggest single area change in the video.
  // The count-up rides it; the GRID is the beat. Chapter opener: first spoken
  // beat bound to @first. Count-up ENDS on the word that names the number, so
  // the counter never finishes before or after "a hundred and four" is said.
  var grid = document.getElementById('t-grid');
  // The stagger RIDES the count-up rather than running at a fixed 22ms. With a
  // fixed step the grid finished in 2.3s while the counter took 9.7s after the
  // re-pace, leaving 7.5s in which the only thing changing was the tail of a
  // power1.out number crawl -- under the motion gate's threshold, and a genuine
  // dead shot. Tied to the count, the grid fills for exactly as long as the
  // number climbs, which is what the beat was always meant to be.
  var fillStep = (@we(104) - @first) / 104;
  for (var i = 0; i < 104; i++) {
    var d = document.createElement('i'); d.id = 'ct-' + i; grid.appendChild(d);
    tl.set('#ct-' + i, { opacity:0, scale:0.3, transformOrigin:'50% 50%' }, 0);
    tl.to('#ct-' + i, { opacity:1, scale:1, duration:0.30 }, @first + i*fillStep);
  }
  var counter = { v:0 }, el = document.getElementById('t-n');
  tl.set('#t-n', { opacity:0 }, 0);   // restates the CSS default, never the sole source
  tl.to('#t-n', { opacity:1, duration:0.30 }, @first);
  tl.to(counter, { v:104, duration:(@we(104) - @first), ease:'power1.out',
                   onUpdate:function(){ el.textContent = Math.round(counter.v); } }, @first);
  tl.fromTo('#t-h', { opacity:0, y:34 }, { opacity:1, y:0, duration:0.55 }, @we(104)+0.70);
  // split the cohort into the two arms -- a whole-grid recolour, on the word
  // that introduces the comparison arm ("against the same cream without it").
  for (var j = 0; j < 104; j++) {
    tl.to('#ct-' + j, { backgroundColor: (j % 2 ? '#59B8AE' : '#9C978D'),
                        duration:0.50 }, @w(against) + (j % 13) * 0.05);
  }
  tl.fromTo('#t-cite', { opacity:0 }, { opacity:1, duration:0.45 }, @w(against)+1.50);
  // The grid physically SPLITS into its two arms -- a whole-column move, where
  // recolouring 104 small dots measured as nothing.
  tl.to('#t-grid', { scaleX:0.92, x:-26, transformOrigin:'50% 50%', duration:1.50,
                     ease:'power2.inOut' }, @w(against)+2.70);
  tl.to('#t-grid', { scaleY:1.10, duration:1.80, ease:'power2.inOut' }, @w(against)+5.70);
""" + CHBAND_TL)

# ---------------------------------------------------------------- 17 preference (carry)
S17 = dict(css="""
    #root { background:var(--paper); color:var(--ink); }
    .g17 { display:flex; flex-direction:column; justify-content:center;
           gap:var(--s-6); height:100%; }
    .arms { display:grid; grid-template-columns:1fr 1fr; gap:var(--s-6); }
    .arm { position:relative; background:var(--mist); border-radius:var(--r-3);
           padding:var(--s-6); overflow:hidden; text-align:center; }
    .arm .lbl { font-family:var(--font-body); font-weight:800; font-size:var(--t-frame); }
    .qual { position:relative; background:var(--ink); color:var(--paper);
            border-radius:var(--r-3); padding:var(--s-6) var(--s-7); }
    /* CARRY from 16-trial104: its cohort grid, same 13-column geometry and
       final split colours, held in the same screen quadrant it ended in --
       pixel-identical at t=0, no entrance fade -- then collapses into the
       ectoin arm on the word that names the finding. */
    .carry16 { position:absolute; top:calc(var(--safe-top) + var(--safe-buffer)); right:calc(var(--safe-right) + var(--safe-buffer));
               width:40%; display:grid; grid-template-columns:repeat(13,1fr);
               gap:7px; z-index:5; }
    .carry16 i { display:block; width:100%; aspect-ratio:1/1; border-radius:50%; }
""", body="""    <div class="stage">
      <div class="carry16" id="carry-grid" data-layout-allow-occlusion="true"></div>
      <div class="g17">
        <div class="arms">
          <div class="arm" id="pr-a"><div class="wash mist" id="pr-wa"
               style="background:var(--aqua)"></div><div class="lbl">With 2% ectoin</div></div>
          <div class="arm" id="pr-b"><div class="lbl">Same cream, without</div></div>
        </div>
        <p class="fig" id="pr-h">On the study&rsquo;s own measure, the women themselves
          preferred the ectoin version.</p>
        <div class="qual" id="pr-q">
          <p class="hero" style="font-size:var(--t-figure)">That is a preference
            &mdash; not a machine reading their skin.</p>
        </div>
      </div>
    </div>""", tl="""
  // CARRY: build the handed-off grid already in its 16-trial104 end state --
  // split two-tone, fully opaque, no entrance -- so frame zero here reads as
  // a continuation of the previous scene, not a fresh one.
  var cg = document.getElementById('carry-grid');
  for (var k = 0; k < 52; k++) {
    var ci = document.createElement('i'); ci.id = 'cg-' + k;
    ci.style.background = k % 2 ? '#59B8AE' : '#9C978D';
    cg.appendChild(ci);
    tl.set('#cg-' + k, { opacity:1, scale:1 }, 0);
  }
  tl.fromTo('#pr-a', { opacity:0, y:50 }, { opacity:1, y:0, duration:0.50 }, 0.15);
  tl.fromTo('#pr-b', { opacity:0, y:50 }, { opacity:1, y:0, duration:0.50 }, 0.35);
  tl.fromTo('#pr-h', { opacity:0 }, { opacity:1, duration:0.50 }, 1.20);
  // BOUND TO WORDS, not to literal seconds. These three beats were authored at
  // 3.00 / 3.20 / 5.90 against an 11.5s read; re-paced to 130 wpm the scene runs
  // 13.1s and the last beat landed at 6.6s, leaving 6.5s in which only a 0.16-
  // opacity blurred ground moved -- a dead shot the motion gate caught. A beat
  // pinned to the word it illustrates follows the read wherever the read goes.
  // the winning arm floods with colour -- a whole half-width panel, ~20% of frame
  tl.fromTo('#pr-wa', { scaleX:0 }, { scaleX:1, duration:0.90, ease:'power2.inOut' }, @w(women));
  tl.to('#pr-b', { opacity:0.65, duration:0.70 }, @w(themselves));
  // The carried grid COLLAPSES into the ectoin arm on "preferred" -- the word
  // that states the finding the grid was standing in for.
  tl.to('#carry-grid', { scale:0.18, x:-360, y:60, opacity:0,
                         transformOrigin:'50% 0%', duration:0.65,
                         ease:'power2.inOut' }, @w(preferred));
  // the qualifier slides up over the result -- the honest beat, and a big one
  tl.set('#pr-q', { opacity:0, y:90 }, 0);
  tl.to('#pr-q', { opacity:1, y:0, duration:0.65, ease:'power3.out' }, @w(preference)-0.35);
  // The arms hold the result while the qualifier is still coming: a slow,
  // continuous settle from the grid collapse to the qualifier's entrance. The
  // re-paced scene left 4.2s in there with nothing above the motion gate's
  // threshold, and a paper-ground scene has no plate drift to fall back on.
  // Sized against the gate's own sampling, not by eye: it samples at 4fps and
   // thresholds the frame-average |luma delta| at 0.35, so a drift has to move
   // enough per 0.25s STEP -- a travel that reads fine at 0.5s intervals is half
   // that per step and lands under the floor.
  tl.to('.arms', { y:-40, scale:1.028, transformOrigin:'50% 50%',
                   duration:@w(preference)-@w(preferred)-0.35, ease:'none' },
        @w(preferred)+0.30);
  // and the qualifier settles across the rest of the line rather than stopping
  // dead on it
  tl.to('#pr-q', { y:-26, duration:@dur-(@w(preference)+0.30), ease:'none' },
        @w(preference)+0.30);
""")

# ---------------------------------------------------------------- 18 eczema trial
S18 = dict(css="""
    #root { background:var(--paper); color:var(--ink); }
    .g18 { display:flex; flex-direction:column; justify-content:center;
           gap:var(--s-5); height:100%; }
    .weeks { position:relative; height:64px; background:var(--mist);
             border-radius:var(--r-pill); overflow:hidden; }
    .weeks .prog { position:absolute; inset:0; background:var(--celadon);
                   transform:scaleX(0); transform-origin:0% 50%; }
    .weeks .t { position:absolute; inset:0; display:flex; align-items:center;
                justify-content:space-between; padding:0 var(--s-5);
                font-family:var(--font-mono); font-size:var(--t-label); }
    .bars { display:grid; grid-template-columns:1fr 1fr; gap:var(--s-6);
            align-items:end; height:250px; }
    /* --ink-soft, not --mist: the label is --paper (it must read on the risen
       moss fill), and on --mist that is 1.06:1 -- invisible until the fill
       arrives. On --ink-soft it is 15.0:1 empty and 5.4:1 filled. */
    .bar { position:relative; background:var(--ink-soft); border-radius:var(--r-3);
           height:100%; display:flex; align-items:flex-end; overflow:hidden; }
    .bar .f { width:100%; background:var(--moss); transform:scaleY(0);
              transform-origin:50% 100%; height:100%; }
    .bar .n { position:absolute; left:0; right:0; bottom:20px; text-align:center;
              color:var(--paper); font-family:var(--font-body); font-weight:800;
              font-size:var(--t-body); }
""", body="""    <div class="stage">
      <div class="g18">
        <p class="fig" id="ez-h">65 people with mild-to-moderate atopic dermatitis
          &mdash; <em style="font-style:normal;color:var(--moss)">eczema</em>.</p>
        <div class="weeks"><div class="prog" id="ez-prog"></div>
          <div class="t"><span>WEEK 0</span><span>WEEK 4</span></div></div>
        <div class="bars">
          <div class="bar"><div class="f" id="ez-f1"></div><div class="n">Ectoin cream</div></div>
          <div class="bar"><div class="f" id="ez-f2"></div><div class="n">Reference barrier cream</div></div>
        </div>
        <p class="p-body" id="ez-n">Performed about as well as the cream it was tested
          against, and was well tolerated.</p>
        <div><span class="cite" id="ez-cite">Skin Pharmacol Physiol &middot; 2013</span></div>
      </div>
    </div>""", tl="""
  tl.fromTo('#ez-h', { opacity:0, y:36 }, { opacity:1, y:0, duration:0.55 }, 0.15);
  // full-width progress sweep = the 4 weeks, ~4% but full-bleed horizontally
  tl.fromTo('#ez-prog', { scaleX:0 }, { scaleX:1, duration:3.20, ease:'none' }, 2.60);
  // two tall bars rising together -- ~23% of the frame, and they END LEVEL,
  // which IS the finding ("performed about as well as")
  // The arms rise to visibly DIFFERENT heights first, so the convergence to level
  // is a real move. Previously both rose to ~0.77 and then "converged" by 2%,
  // which is the finding stated invisibly.
  tl.fromTo('#ez-f1', { scaleY:0 }, { scaleY:0.94, duration:2.90, ease:'power1.inOut' }, 2.80);
  tl.fromTo('#ez-f2', { scaleY:0 }, { scaleY:0.52, duration:2.90, ease:'power1.inOut' }, 2.80);
  // BOUND TO WORDS. Authored at 7.10 / 8.20 / 10.40 against a 15.1s read; at
  // 130 wpm the scene runs 17.6s and every beat had finished by 12.5s, leaving
  // the last five seconds with nothing moving but a blurred 0.16-opacity ground.
  tl.fromTo('#ez-n', { opacity:0 }, { opacity:1, duration:0.50 }, @w(weeks)+0.30);
  tl.fromTo('#ez-cite', { opacity:0 }, { opacity:1, duration:0.45 }, @w(barrier));
  // Both bars converge to exactly level -- the finding, made visible as a
  // large-area move rather than two static columns -- on the words that state it.
  tl.to('#ez-f1', { scaleY:0.76, backgroundColor:'#59B8AE', duration:2.10,
                    ease:'power2.inOut' }, @w(performed)-0.40);
  tl.to('#ez-f2', { scaleY:0.76, backgroundColor:'#59B8AE', duration:2.10,
                    ease:'power2.inOut' }, @w(performed)-0.40);
  // The bars keep rising, slowly, from the moment they converge to the end of
  // the line -- one continuous move rather than a 0.04 scale nudge that the
  // motion gate cannot see. 18-eczema left 5.5s static after the re-pace.
  tl.to(['#ez-f1','#ez-f2'], { scaleY:0.96, duration:@dur-@w(performed)-0.4,
                               ease:'none' }, @w(performed)+1.70);
  tl.to('#ez-prog', { scaleX:1.10, transformOrigin:'0% 50%',
                      duration:@dur-@w(performed)-0.4, ease:'none' },
        @w(performed)+1.70);
  tl.to('#ez-h', { y:-30, duration:@dur-@w(performed)-0.4, ease:'none' },
        @w(performed)+1.70);
  tl.to('#ez-prog', { backgroundColor:'#4F6B52', duration:1.20 }, 10.60);
""")

# ---------------------------------------------------------------- 19 limits
S19 = dict(css="""
    #root { background:var(--ink); color:var(--paper); }
    .g19 { display:flex; flex-direction:column; justify-content:center;
           gap:var(--s-6); height:100%; }
    .claims { display:grid; grid-template-columns:repeat(3,1fr); gap:var(--s-5); }
    /* NOT-SUPPORTED CARD. The predecessor voided each claim with a full-card
       coral flood at opacity 0.88. `.x` is absolutely positioned and is NOT a
       `.wash`, so the _preamble rule that lifts washed siblings to z-index 1
       never applied and the flood painted OVER the copy -- measured 1.03:1 on
       the render, i.e. the claim was erased rather than struck. It also carried
       the whole meaning in one colour. Three cues now, none of them colour
       alone: an explicit `NOT SUPPORTED` label, a rule struck through the
       claim, and a coral edge. The copy stays --paper on --ink-soft, 15.1:1,
       readable for the whole scene. */
    .cl { position:relative; background:var(--ink-soft); border-radius:var(--r-3);
          padding:var(--s-6); text-align:center; overflow:hidden;
          border-left:10px solid var(--ink-soft);
          font-family:var(--font-body); font-weight:800; font-size:var(--t-frame);
          min-height:230px; display:flex; flex-direction:column; gap:var(--s-4);
          align-items:center; justify-content:center; }
    .cl .claim { position:relative; z-index:1; display:inline-block; }
    .cl .strike { position:absolute; left:-6px; right:-6px; top:50%; height:6px;
                  background:var(--coral); transform:scaleX(0);
                  transform-origin:0% 50%; z-index:2; }
    .cl .tag { font-family:var(--font-mono); font-weight:500;
               font-size:var(--t-caption); letter-spacing:var(--tr-mono-wide);
               text-transform:uppercase; color:var(--coral); opacity:0; }
""", body="""    <div class="stage">
      <div class="g19">
        <p class="hero" id="li-h">Encouraging. Not proof.</p>
        <div class="claims">
          <div class="cl" id="cl-0"><span class="claim">Cures eczema<span class="strike" id="x-0"></span></span><span class="tag" id="tg-0">Not supported</span></div>
          <div class="cl" id="cl-1"><span class="claim">Reverses ageing<span class="strike" id="x-1"></span></span><span class="tag" id="tg-1">Not supported</span></div>
          <div class="cl" id="cl-2"><span class="claim">Replaces a prescription<span class="strike" id="x-2"></span></span><span class="tag" id="tg-2">Not supported</span></div>
        </div>
      </div>
    </div>""", tl="""
  // Three full cards, each ~10% of the frame, each REFUSED on the beat: a coral
  // rule drawn through the claim, a coral edge, and the words "Not supported".
  // Motion still carries it at 5px; meaning no longer depends on the colour.
  tl.fromTo('#li-h', { opacity:0, y:40 }, { opacity:1, y:0, duration:0.55 }, 0.15);
  for (var i = 0; i < 3; i++) {
    tl.fromTo('#cl-' + i, { opacity:0, y:56 }, { opacity:1, y:0, duration:0.45 }, 0.80 + i*0.22);
    tl.fromTo('#x-' + i, { scaleX:0 }, { scaleX:1, duration:0.35, ease:'power2.inOut' }, 2.90 + i*0.75);
    tl.to('#cl-' + i, { borderLeftColor:'#C97A5C', duration:0.35 }, 2.90 + i*0.75);
    tl.fromTo('#tg-' + i, { opacity:0, y:10 }, { opacity:1, y:0, duration:0.30 }, 3.05 + i*0.75);
  }
""")

# ---------------------------------------------------------------- 20 twelve
S20 = dict(css="""
    #root { background:var(--paper); color:var(--ink); }
    .g20 { display:grid; grid-template-columns:44fr 56fr; gap:var(--s-8);
           align-items:center; height:100%; }
    .tiles { display:grid; grid-template-columns:repeat(4,1fr); gap:var(--s-4); }
    .tile { background:var(--ink); border-radius:var(--r-2); aspect-ratio:3/2; }
""", body="""    <div class="stage">
      <div class="g20">
        <div class="col">
          <p class="kicker">How much evidence is there</p>
          <p class="hero" id="tw-n" style="font-size:180px;line-height:1;opacity:0">12</p>
          <p class="fig" id="tw-h">ectoin clinical trials indexed on PubMed. Total.</p>
          <div style="margin-top:26px"><span class="cite" id="tw-cite">PubMed &middot; 2026</span></div>
        </div>
        <div class="tiles" id="tw-tiles"></div>
      </div>
    </div>""", tl="""
  // Count reaches 12 exactly on the word that first names the number; the
  // second "Twelve." (the standalone sentence) instead PULSES the tiles --
  // a distinct beat, not a repeat of the same reveal.
  var t = document.getElementById('tw-tiles');
  for (var i = 0; i < 12; i++) {
    var d = document.createElement('div'); d.className = 'tile'; d.id = 'tl-' + i;
    t.appendChild(d);
    tl.set('#tl-' + i, { opacity:0, scaleY:0, transformOrigin:'50% 100%' }, 0);
    tl.to('#tl-' + i, { opacity:1, scaleY:1, duration:0.40, ease:'back.out(1.5)' },
          @first + i*0.30);
  }
  var c = { v:0 }, el = document.getElementById('tw-n');
  tl.set('#tw-n', { opacity:0 }, 0);   // restates the CSS default, never the sole source
  tl.to('#tw-n', { opacity:1, duration:0.30 }, @first);
  tl.to(c, { v:12, duration:(@w(12,1) - @first), ease:'none',
             onUpdate:function(){ el.textContent = Math.round(c.v); } }, @first);
  tl.fromTo('#tw-h', { opacity:0, y:34 }, { opacity:1, y:0, duration:0.50 }, @w(12,1)+0.20);
  tl.fromTo('#tw-cite', { opacity:0 }, { opacity:1, duration:0.45 }, @w(12,1)+1.40);
  // The standalone second "Twelve." pulses the whole tile grid -- the tiles
  // are already there; this is emphasis, a large-area beat, not a re-entrance.
  tl.to('.tile', { scale:1.14, duration:0.22, yoyo:true, repeat:1,
                   ease:'power1.inOut', transformOrigin:'50% 50%' }, @w(12,2));
""")

# ---------------------------------------------------------------- 21 verdict (carry)
S21 = dict(css="""
    #root { background:var(--ink); color:var(--paper); }
    .g21 { display:flex; flex-direction:column; justify-content:center;
           gap:var(--s-6); height:100%; }
    .makers { display:grid; grid-template-columns:repeat(3,1fr); gap:var(--s-5); }
    /* Colour stated, never inherited. These three tiles shipped BLACK on
       near-black (1.28:1 measured at t=229.6s) because a wrapper's trailing
       `#root { color:inherit }` outranked the scene's own root rule. An
       explicit colour here cannot be reached by that class of bug. */
    .mk { background:var(--ink-soft); color:var(--paper); border-radius:var(--r-3);
          padding:var(--s-6); text-align:center; font-family:var(--font-body);
          font-weight:800; font-size:var(--t-frame); }
    .verdict { position:relative; border-radius:var(--r-3); padding:var(--s-7);
               overflow:hidden; background:var(--ink-soft); text-align:center; }
    /* CARRY from 20-twelve: the same hero "12", same size, same corner it
       held at t=0 -- pixel-identical, no entrance -- then shrinks into the
       kicker it becomes part of. */
    .ghost12 { position:absolute; top:calc(var(--safe-top) + var(--safe-buffer)); left:calc(var(--safe-left) + var(--safe-buffer));
               font-family:var(--font-display); font-size:180px; line-height:1;
               color:var(--paper); margin:0; z-index:5; }
    /* VERDICT HALVES. "No." used to be inline coral, which lands at 5.03:1 on
       --ink-soft but collapses to 1.72:1 once the moss wash sweeps under it,
       and it carried the whole yes/no distinction in hue alone. Both halves
       now read in --paper (15.1:1 / 5.4:1 on the wash) and are distinguished
       by a drawn underline AND a word: moss + SUPPORTED, coral + NOT
       SUPPORTED. The colour is confirmation, not the message. */
    .v-line { margin:0; }
    /* The panel washes MOSS mid-scene, so a moss or coral marker on it is a
       1.1-1.7:1 mark that simply disappears -- which is what the original
       moss "Yes." underline and coral "No." flash both did. The verdict is
       carried instead by a glyph plus a word inside a currentColor pill, and
       both underlines are --paper so they read on ink-soft AND on the wash. */
    .v-tag { display:inline-block; margin:10px 0 var(--s-5);
             font-family:var(--font-mono); font-weight:500;
             font-size:var(--t-caption); letter-spacing:var(--tr-mono-wide);
             text-transform:uppercase; color:var(--paper); opacity:0;
             border:2px solid currentColor; border-radius:var(--r-pill);
             padding:6px 22px; }
    .v-tag .g { margin-right:12px; font-size:1.1em; vertical-align:-0.04em; }
""", body="""    <div class="stage">
      <div class="ghost12" id="ghost-12">12</div>
      <div class="g21">
        <p class="kicker on-ink" id="v-k">Some of that research comes from people who sell it</p>
        <div class="makers">
          <div class="mk" id="mk-0">bitop</div>
          <div class="mk" id="mk-1">Merck</div>
          <div class="mk" id="mk-2">Kao</div>
        </div>
        <div class="verdict" id="v-box">
          <div class="wash moss" id="v-wash"></div>
          <p class="hero v-line" id="v-h">Promising supporting ingredient. <span id="v-yes"
            style="position:relative">Yes.</span></p>
          <span class="v-tag yes" id="v-tag-yes"><span class="g">&#10003;</span>Supported by the trials</span>
          <p class="hero v-line">Miracle molecule. <span id="v-no"
            style="position:relative">No.</span></p>
          <span class="v-tag no" id="v-tag-no"><span class="g">&#10005;</span>Not supported</span>
        </div>
      </div>
    </div>""", tl="""
  // CARRY: the ghost 12 shrinks into the kicker it becomes part of, on "Some".
  tl.set('#ghost-12', { opacity:1, scale:1, x:0, y:0 }, 0);
  tl.fromTo('#v-k', { opacity:0 }, { opacity:1, duration:0.40 }, @w(Some));
  tl.to('#ghost-12', { scale:0.16, x:40, y:-30, opacity:0, transformOrigin:'0% 0%',
                       duration:0.55, ease:'power2.inOut' }, @w(Some));
  // ASR on this take still mis-hears two of the three brand names ("Bitop"
  // as "BTOP", "Kao" as "Cow"); Merck now comes back correctly. Markers bind
  // to what is in the manifest, same as any other scene. The SPOKEN audio is
  // right -- verified on whisper large-v3, which reads all three -- so this is
  // a small.en miss on proper nouns, not a TTS defect. vo_words.CORRECTIONS
  // maps them back for the captions.
  tl.fromTo('#mk-0', { opacity:0, y:52 }, { opacity:1, y:0, duration:0.42 }, @w(BTOP));
  tl.fromTo('#mk-1', { opacity:0, y:52 }, { opacity:1, y:0, duration:0.42 }, @w(Merck));
  tl.fromTo('#mk-2', { opacity:0, y:52 }, { opacity:1, y:0, duration:0.42 }, @w(Cow));
  // The verdict panel enters full-width and then washes -- two large beats on the
  // line the whole act has been building to.
  tl.set('#v-box', { opacity:0, y:70 }, 0);
  tl.to('#v-box', { opacity:1, y:0, duration:0.60, ease:'power3.out' }, @w(Promising));
  // "yes" gets an underline highlight -- the affirming half of the verdict.
  tl.fromTo('#v-yes', { backgroundImage:'linear-gradient(#F7F5F0,#F7F5F0)',
      backgroundRepeat:'no-repeat', backgroundSize:'0% 4px',
      backgroundPosition:'0% 100%' },
    { backgroundSize:'100% 4px', duration:0.45, ease:'power2.inOut' }, @w(yes));
  // "Miracle" is where the panel washes moss -- the coral line + wash beat.
  tl.fromTo('#v-wash', { scaleX:0 }, { scaleX:1, duration:1.00, ease:'power2.inOut' }, @w(Miracle));
  tl.fromTo('#v-tag-yes', { opacity:0, y:14 }, { opacity:1, y:0, duration:0.30 }, @w(yes)+0.25);
  // "no" is underlined in coral -- the same gesture as "yes", opposite hue --
  // and the two words SUPPORTED / NOT SUPPORTED land under the halves they
  // label, so the verdict survives without colour vision.
  tl.fromTo('#v-no', { backgroundImage:'linear-gradient(#F7F5F0,#F7F5F0)',
      backgroundRepeat:'no-repeat', backgroundSize:'0% 4px',
      backgroundPosition:'0% 100%' },
    { backgroundSize:'100% 4px', duration:0.45, ease:'power2.inOut' }, @w(no));
  tl.fromTo('#v-tag-no', { opacity:0, y:14 }, { opacity:1, y:0, duration:0.30 }, @w(no)+0.25);
""")

# ---------------------------------------------------------------- 22 who it suits
S22 = dict(css="""
    #root { background:var(--paper); color:var(--ink); }
    .g22 { display:flex; flex-direction:column; justify-content:center;
           gap:var(--s-6); height:100%; }
    .states { display:grid; grid-template-columns:repeat(4,1fr); gap:var(--s-5); }
    .stt { position:relative; background:var(--mist); border-radius:var(--r-3);
           padding:var(--s-6) var(--s-5); text-align:center; overflow:hidden;
           font-family:var(--font-body); font-weight:800; font-size:var(--t-frame);
           min-height:190px; display:flex; align-items:center; justify-content:center; }
    .friends { display:grid; grid-template-columns:repeat(4,1fr); gap:var(--s-4); }
    .fr { background:var(--ink); color:var(--paper); border-radius:var(--r-pill);
          padding:var(--s-4) var(--s-3); text-align:center;
          font-family:var(--font-mono); font-size:var(--t-label); }
""" + CHBAND_CSS, body=chband_body("22-whofor") + """
    <div class="stage">
      <div class="g22">
        <p class="fig" id="wf-h">Most interesting if your skin runs&hellip;</p>
        <div class="states">
          <div class="stt" id="ss-0"><div class="wash aqua" id="sw-0"></div><span>Dry</span></div>
          <div class="stt" id="ss-1"><div class="wash aqua" id="sw-1"></div><span>Sensitive</span></div>
          <div class="stt" id="ss-2"><div class="wash aqua" id="sw-2"></div><span>Over-cleansed</span></div>
          <div class="stt" id="ss-3"><div class="wash aqua" id="sw-3"></div><span>Irritated</span></div>
        </div>
        <p class="p-body" id="wf-s">It sits comfortably alongside&hellip;</p>
        <div class="friends">
          <div class="fr" id="fr-0">Panthenol</div><div class="fr" id="fr-1">Glycerin</div>
          <div class="fr" id="fr-2">Squalane</div><div class="fr" id="fr-3">Ceramides</div>
        </div>
      </div>
    </div>""", tl="""
  // Chapter opener: first spoken beat bound to @first.
  tl.fromTo('#wf-h', { opacity:0, y:34 }, { opacity:1, y:0, duration:0.50 }, @first);
  for (var i = 0; i < 4; i++) {
    tl.fromTo('#ss-' + i, { opacity:0, y:56 }, { opacity:1, y:0, duration:0.42 }, @first+0.55 + i*0.42);
    // each card washes as its word is said -- four large area changes, spread
    tl.fromTo('#sw-' + i, { scaleX:0 }, { scaleX:1, duration:0.55,
                                          ease:'power2.inOut' }, @first+2.55 + i*0.62);
  }
  tl.fromTo('#wf-s', { opacity:0 }, { opacity:1, duration:0.45 }, 8.20);
  for (var j = 0; j < 4; j++)
    tl.fromTo('#fr-' + j, { opacity:0, y:34 }, { opacity:1, y:0, duration:0.40 }, 8.70 + j*0.45);
""" + CHBAND_TL)

# ---------------------------------------------------------------- 23 the numbers
S23 = dict(css="""
    #root { background:var(--paper); color:var(--ink); }
    .g23 { display:flex; flex-direction:column; justify-content:center;
           gap:var(--s-6); height:100%; }
    .brands { display:grid; grid-template-columns:1fr 1fr; gap:var(--s-6); }
    .bd { position:relative; background:var(--ink); color:var(--paper);
          border-radius:var(--r-3); padding:var(--s-7); overflow:hidden; }
    .bd .pc { font-family:var(--font-display); font-size:120px; line-height:1;
              color:var(--aqua); }
    .bd .nm { font-family:var(--font-mono); font-size:var(--t-label);
              letter-spacing:var(--tr-mono-wide); color:var(--ink-2-dark);
              margin-top:var(--s-3); }
""", body="""    <div class="stage">
      <div class="g23">
        <p class="hero" id="nb-h">Do not buy it off the front of the bottle.</p>
        <p class="fig" id="nb-s">Plenty of brands do print a number.</p>
        <div class="brands">
          <div class="bd" id="bd-0"><div class="wash moss" id="bw-0"></div>
            <div class="pc">7%</div><div class="nm">PAULA&rsquo;S CHOICE</div></div>
          <div class="bd" id="bd-1"><div class="wash moss" id="bw-1"></div>
            <div class="pc">2%</div><div class="nm">THE ORDINARY</div></div>
        </div>
      </div>
    </div>""", tl="""
  tl.fromTo('#nb-h', { opacity:0, y:40 }, { opacity:1, y:0, duration:0.55 }, 0.15);
  tl.fromTo('#nb-s', { opacity:0 }, { opacity:1, duration:0.45 }, 3.40);
  // two half-width cards, each ~18% of the frame, entering on the brand's own
  // name, then washing
  tl.fromTo('#bd-0', { opacity:0, x:-90 }, { opacity:1, x:0, duration:0.55 }, @w(Paula's));
  tl.fromTo('#bw-0', { scaleX:0 }, { scaleX:1, duration:0.60, ease:'power2.inOut' }, @w(Paula's)+0.50);
  tl.fromTo('#bd-1', { opacity:0, x:90 },  { opacity:1, x:0, duration:0.55 }, @w(Ordinary));
  tl.fromTo('#bw-1', { scaleX:0 }, { scaleX:1, duration:0.60, ease:'power2.inOut' }, @w(Ordinary)+0.50);
""")

# ---------------------------------------------------------------- 24 the eleven (carry)
S24 = dict(css="""
    #root { background:var(--ink); color:var(--paper); }
    .g24 { display:grid; grid-template-columns:48fr 52fr; gap:var(--s-8);
           align-items:center; height:100%; }
    /* CARRY from 23-numbers: its two brand cards (7%/2%), same dark-card
       styling, pixel-identical at t=0 -- PLUS the 11% card the act's payoff
       needs, in the same row, so the row reads as one continuous lineup
       rather than a fresh scene. */
    /* The active card scales to 1.14 on its beat, and it now carries a 3px
       border as well, so the row needs room for the overshoot. The room is
       PADDING, not a negative margin: pulling the box out past the safe lines
       put the cards 18px into the top reserve and 44px into the right one, which
       is exactly what the hard safe-area gate is for. */
    .carry23 { position:absolute; top:calc(var(--safe-top) + var(--safe-buffer)); left:calc(var(--safe-left) + var(--safe-buffer));
               right:calc(var(--safe-right) + var(--safe-buffer)); display:grid;
               grid-template-columns:1fr 1fr 1fr; gap:var(--s-5); z-index:5;
               padding:18px 44px; }
    /* CARRY ROW. The two superseded brands used to drop to opacity 0.30 --
       2.58:1 as authored, 1.08:1 as it actually shipped -- with the live one
       marked only by an aqua fill. Inactive is now 0.60 plus a dashed edge,
       active is a solid aqua edge plus a marker glyph, so "which one are we
       talking about" survives greyscale and a 5px thumbnail alike. */
    .c23-card { position:relative; background:var(--ink-soft); color:var(--paper);
                border:3px dashed rgba(247,245,240,.38); border-radius:var(--r-3);
                padding:var(--s-5); text-align:center; }
    .c23-card .mark { position:absolute; top:8px; left:14px; opacity:0;
                      font-family:var(--font-mono); font-size:var(--t-caption);
                      color:var(--ink); }
    .c23-card .pc { font-family:var(--font-display); font-size:64px; line-height:1;
                     color:var(--aqua); }
    .c23-card .nm { font-family:var(--font-mono); font-size:var(--t-caption);
                     letter-spacing:var(--tr-mono-wide); color:var(--ink-2-dark);
                     margin-top:var(--s-2); }
    .c23-card.eleven { background:var(--aqua); color:var(--ink);
                       border:3px solid var(--ink); }
    .c23-card.eleven .pc { color:var(--ink); }
    .c23-card.eleven .nm { color:var(--ink); }
    .c23-card.eleven .mark { opacity:1; }
    .split { display:flex; gap:var(--s-4); }
    .half { position:relative; flex:1 1 0; min-width:0; border-radius:var(--r-3);
            padding:var(--s-6); text-align:center; }
    .half.p { background:var(--ink-soft); color:var(--paper); }
    .half.e { background:var(--aqua); color:var(--ink); }
    .half .v { font-family:var(--font-display); font-size:78px; line-height:1; }
    .half .k { font-family:var(--font-mono); font-size:var(--t-caption);
               letter-spacing:var(--tr-mono-wide); margin-top:var(--s-2); }
    /* 26px was the smallest type in the piece, under the project's own 32px
       "meant to be read" floor, in --ink-3-dark (4.13:1 on --ink-soft) -- and
       the whole list then dimmed to opacity 0.40, i.e. 1.75:1. Bigger, in the
       colour that clears AA, and dimmed only to 0.75. The full list is also in
       the description, per the accessible source list in PUBLISH.md. */
    .inci { font-family:var(--font-mono); font-size:32px; line-height:1.75;
            color:var(--ink-2-dark); white-space:nowrap; }
    .inci b { color:var(--paper); font-weight:500; background:var(--ink-soft);
              padding:3px 10px; border-radius:var(--r-2);
              border:2px solid transparent; }
    /* Active INCI entries get weight + a border + a marker glyph on top of the
       aqua fill; the fill alone was a colour-only state signal. */
    .inci b.hit { background:var(--aqua); color:var(--ink); font-weight:700;
                  border-color:var(--ink); }
    .inci b .mk { opacity:0; }
    /* The 10:1 split drawn TO SCALE across the full column -- the scene's
       largest beat, and a clearer statement of the point than two chips. */
    /* 260px, not 74px: at 74 the bar was 2.9% of the frame and its draw measured
       per-step 0.43, under the 1.0 floor. At 260 it is ~10.4% -> 2.2. */
    .prop { display:flex; height:260px; border-radius:var(--r-2); overflow:hidden;
            margin-top:20px; }
    .prop-p, .prop-e { display:flex; align-items:center; justify-content:center;
                       font-family:var(--font-mono); font-size:var(--t-caption);
                       letter-spacing:var(--tr-mono); transform:scaleX(0);
                       transform-origin:0% 50%; }
    .prop-p { flex:10 1 0; background:var(--paper); color:var(--ink); }
    .prop-e { flex:1 1 0; background:var(--aqua); color:var(--ink); }
""", body="""    <div class="stage">
      <div class="carry23" id="carry-row">
        <div class="c23-card" id="c23-0"><span class="mark">&#9656;</span><div class="pc">7%</div><div class="nm">PAULA&rsquo;S CHOICE</div></div>
        <div class="c23-card" id="c23-1"><span class="mark">&#9656;</span><div class="pc">2%</div><div class="nm">THE ORDINARY</div></div>
        <div class="c23-card eleven" id="c23-2"><span class="mark">&#9656;</span><div class="pc">11%</div><div class="nm">ABIB</div></div>
      </div>
      <div class="g24">
        <div class="col">
          <p class="kicker on-ink">Abib &middot; Ectoin Panthenol 11%</p>
          <p class="hero" id="el-n" style="opacity:0">11%</p>
          <div class="split" id="el-split" style="margin-top:24px;opacity:0">
            <div class="half p"><div class="v">10%</div><div class="k">PANTHENOL</div></div>
            <div class="half e"><div class="v">1%</div><div class="k">ECTOIN</div></div>
          </div>
          <div class="prop" id="el-prop" style="opacity:0">
            <div class="prop-p" id="el-pp"><span>10% PANTHENOL</span></div>
            <div class="prop-e" id="el-pe"><span>1%</span></div>
          </div>
          <p class="p-body on-ink" id="el-note" style="margin-top:20px;opacity:0">
            The big number on the front is not always the ectoin number.</p>
        </div>
        <div class="col">
          <p class="kicker on-ink" style="margin-bottom:14px">On the ingredient list</p>
          <div class="inci" id="el-inci">
            1. Water &nbsp; <b id="in-p"><span class="mk" id="mk-p">&#9656;</span> 2. Panthenol</b><br>
            3. Propanediol &nbsp; 4. Cetyl Ethylhexanoate<br>
            5. Squalane &nbsp; 6. Diisobutyl Adipate<br>
            7. Vinyl Dimethicone<br>
            8. Propylheptyl Caprylate<br>
            9. Cetearyl Alcohol<br>
            10. Glyceryl Glucoside<br>
            <b id="in-e"><span class="mk" id="mk-e">&#9656;</span> 11. Ectoin</b>
          </div>
        </div>
      </div>
    </div>""", tl="""
  // CARRY: the row is already there at t=0, pixel-identical to how 23-numbers
  // ended (plus the 11% card). On "eleven" the two brand cards dim and the
  // 11% card scales up into the hero position -- the hand-off beat.
  tl.set(['#c23-0','#c23-1','#c23-2'], { opacity:1, y:0, scale:1 }, 0);
  tl.to(['#c23-0','#c23-1'], { opacity:0.60, duration:0.50 }, @w(11));
  tl.to('#c23-2', { scale:1.14, duration:0.45, ease:'power2.out' }, @w(11));
  tl.to('#c23-2', { opacity:0, scale:1.6, duration:0.45, ease:'power2.in' }, @w(11)+0.55);
  tl.fromTo('#el-n', { opacity:0, scale:0.7, transformOrigin:'0% 50%' },
                     { opacity:1, scale:1, duration:0.60, ease:'back.out(1.4)' }, @w(11)+0.55);
  tl.to('#carry-row', { opacity:0, duration:0.01 }, @w(11)+1.05);
  tl.to('#el-n', { opacity:0.60, scale:0.72, transformOrigin:'0% 50%', duration:0.55 }, @w(11)+2.85);
  // "That eleven is the two of them added together" -- the split reveals on "added".
  tl.fromTo('#el-split', { opacity:0, y:44 }, { opacity:1, y:0, duration:0.60 }, @w(combines));
  tl.fromTo('#el-inci', { opacity:0, x:60 }, { opacity:1, x:0, duration:0.60 }, @w(combines)+2.20);
  // "panthenol is second" / "Ectoin is eleventh" -- each highlight lands on its own word.
  // Fill + weight + border + marker, all on the same beat. The fill alone was
  // a colour-only signal for "this is the entry we are talking about".
  tl.fromTo('#in-p', { backgroundColor:'#211F1B' },
                     { backgroundColor:'#59B8AE', color:'#131516', duration:0.45 }, @w(second));
  tl.to('#in-p', { fontWeight:700, borderColor:'#131516', duration:0.45 }, @w(second));
  tl.to('#mk-p', { opacity:1, duration:0.30 }, @w(second));
  tl.fromTo('#in-e', { backgroundColor:'#211F1B' },
                     { backgroundColor:'#59B8AE', color:'#131516', duration:0.45 }, @w(11th));
  tl.to('#in-e', { fontWeight:700, borderColor:'#131516', duration:0.45 }, @w(11th));
  tl.to('#mk-e', { opacity:1, duration:0.30 }, @w(11th));
  tl.fromTo('#el-note', { opacity:0, y:30 }, { opacity:1, y:0, duration:0.55 }, @w(big)-0.20);
  // The two halves of the 11% resolve at panel scale in the back half.
  tl.to('#el-prop', { opacity:1, duration:0.30 }, @w(big)+0.80);
  tl.fromTo('#el-pp', { scaleX:0 }, { scaleX:1, duration:1.05, ease:'power2.out' }, @w(big)+0.90);
  tl.fromTo('#el-pe', { scaleX:0 }, { scaleX:1, duration:0.45, ease:'power2.out' }, @w(big)+2.00);
  tl.to('#el-inci', { opacity:0.88, duration:1.10 }, @w(big)+3.00);
""")

# ---------------------------------------------------------------- 25 formula (UNSOURCED)
S25 = dict(css="""
    #root { background:var(--paper); color:var(--ink); }
    .g25 { display:flex; flex-direction:column; justify-content:center;
           gap:var(--s-6); height:100%; }
    .flag { display:inline-flex; align-items:center; gap:var(--s-3);
            font-family:var(--font-mono); font-size:var(--t-chip);
            letter-spacing:var(--tr-mono); color:var(--ink-2);
            border:2px dashed var(--rule-strong); border-radius:var(--r-pill);
            padding:10px 26px; width:max-content; background:transparent; }
    .qs { display:grid; grid-template-columns:repeat(3,1fr); gap:var(--s-5); }
    .q { position:relative; background:var(--mist); border-radius:var(--r-3);
         padding:var(--s-6); overflow:hidden; min-height:260px;
         font-family:var(--font-display); font-size:var(--t-figure);
         line-height:var(--lh-snug); }
""", body="""    <div class="stage">
      <div class="g25">
        <span class="flag" id="u-flag">JUDGEMENT &mdash; NO SOURCE RECORD</span>
        <div class="qs">
          <div class="q" id="q-0"><div class="wash mist" id="qw-0"></div><span>Fragrance-free,
            if fragrance bothers you?</span></div>
          <div class="q" id="q-1"><div class="wash mist" id="qw-1"></div><span>Does it carry other
            useful moisturisers?</span></div>
          <div class="q" id="q-2"><div class="wash mist" id="qw-2"></div><span>Is the rest of the
            formula built well?</span></div>
        </div>
        <p class="hero" id="u-h" style="font-size:var(--t-figure)">One good ingredient cannot
          rescue a badly built product.</p>
      </div>
    </div>""", tl="""
  // This beat is EDITORIAL, not evidence. It renders with the dashed unsourced
  // flag and NO citation chip -- the two must never be mistakable for each other.
  tl.fromTo('#u-flag', { opacity:0 }, { opacity:1, duration:0.45 }, 0.20);
  for (var i = 0; i < 3; i++) {
    tl.fromTo('#q-' + i, { opacity:0, y:58 }, { opacity:1, y:0, duration:0.45 }, 1.10 + i*0.60);
    tl.fromTo('#qw-' + i, { scaleX:0 }, { scaleX:1, duration:0.55,
                                          ease:'power2.inOut' }, 3.40 + i*0.85);
  }
  tl.fromTo('#u-h', { opacity:0, y:40 }, { opacity:1, y:0, duration:0.60 }, 8.30);
""")

# ---------------------------------------------------------------- 26 k-beauty
S26 = dict(css="""
    #root { background:var(--paper); color:var(--ink); }
    .g26 { display:grid; grid-template-columns:50fr 50fr; gap:var(--s-8);
           align-items:center; height:100%; }
    .neg { position:relative; background:var(--mist); border-radius:var(--r-3);
           padding:var(--s-7); overflow:hidden; }
    .pos { position:relative; background:var(--ink); color:var(--paper);
           border-radius:var(--r-3); padding:var(--s-7); overflow:hidden; }
""" + CHBAND_CSS, body=chband_body("26-kbeauty") + """
    <div class="stage">
      <div class="g26">
        <div class="neg" id="kb-neg">
          <div class="void" id="kb-void"></div>
          <p class="kicker">The easy story</p>
          <p class="hero" style="font-size:var(--t-figure);margin-top:12px">K-beauty
            invented ectoin.</p>
        </div>
        <div class="pos" id="kb-pos">
          <div class="wash moss" id="kb-wash"></div>
          <p class="kicker on-ink">What is actually true</p>
          <p class="hero" style="font-size:var(--t-figure);margin-top:12px">Korean
            formulators pair it with barrier ingredients, in light wearable textures.</p>
        </div>
      </div>
    </div>""", tl="""
  // Half-frame panel voided, half-frame panel washed. Two ~22% area beats.
  // Chapter opener: first spoken beat bound to @first.
  tl.fromTo('#kb-neg', { opacity:0, x:-90 }, { opacity:1, x:0, duration:0.55 }, @first);
  tl.fromTo('#kb-void', { opacity:0 }, { opacity:0.85, duration:0.45 }, @first+2.15);
  tl.fromTo('#kb-pos', { opacity:0, x:90 }, { opacity:1, x:0, duration:0.55 }, @first+3.45);
  tl.fromTo('#kb-wash', { scaleX:0 }, { scaleX:1, duration:0.90, ease:'power2.inOut' }, @first+4.25);
  tl.to('#kb-neg', { opacity:0.35, duration:0.70 }, @first+4.25);
""" + CHBAND_TL)

# ---------------------------------------------------------------- 27 resilience
S27 = dict(css="""
    #root { background:var(--paper); color:var(--ink); }
    .g27 { display:flex; flex-direction:column; justify-content:center;
           gap:var(--s-7); height:100%; }
    .shift { display:grid; grid-template-columns:1fr auto 1fr; gap:var(--s-6);
             align-items:center; }
    .sh { position:relative; border-radius:var(--r-3); padding:var(--s-7);
          text-align:center; overflow:hidden;
          font-family:var(--font-body); font-weight:800; font-size:var(--t-frame); }
    .sh.from { background:var(--mist); color:var(--ink-2); }
    .sh.to { background:var(--moss); color:var(--paper); }
    .arrow { font-family:var(--font-mono); font-size:var(--t-hero); color:var(--ink-2); }
    .where { display:grid; grid-template-columns:repeat(3,1fr); gap:var(--s-5); }
    .wh { background:var(--ink); color:var(--paper); border-radius:var(--r-3);
          padding:var(--s-5); text-align:center;
          font-family:var(--font-mono); font-size:var(--t-label); }
""", body="""    <div class="stage">
      <div class="g27">
        <div class="shift">
          <div class="sh from" id="sh-a">Aggressive transformation</div>
          <div class="arrow" id="sh-ar">&rarr;</div>
          <div class="sh to" id="sh-b"><div class="wash moss" id="sh-w"></div><span>Skin that simply stays comfortable</span></div>
        </div>
        <p class="fig" id="wh-h">You will already find it in&hellip;</p>
        <div class="where">
          <div class="wh" id="wh-0">Barrier serums</div>
          <div class="wh" id="wh-1">Toners</div>
          <div class="wh" id="wh-2">Sun products</div>
        </div>
      </div>
    </div>""", tl="""
  tl.fromTo('#sh-a', { opacity:0, x:-70 }, { opacity:1, x:0, duration:0.50 }, 0.20);
  tl.fromTo('#sh-ar', { opacity:0 }, { opacity:1, duration:0.35 }, 1.10);
  tl.fromTo('#sh-b', { opacity:0, x:70 }, { opacity:1, x:0, duration:0.50 }, 1.45);
  // The wash lands on the word that names the destination state.
  tl.fromTo('#sh-w', { scaleX:0 }, { scaleX:1, duration:0.80, ease:'power2.inOut' }, @w(comfortable));
  tl.to('#sh-a', { opacity:0.40, duration:0.60 }, @w(comfortable));
  tl.fromTo('#wh-h', { opacity:0 }, { opacity:1, duration:0.45 }, @w(comfortable)+2.60);
  // Each "where you'll find it" card lands on its own named product category.
  tl.fromTo('#wh-0', { opacity:0, y:52 }, { opacity:1, y:0, duration:0.45 }, @w(serums));
  tl.fromTo('#wh-1', { opacity:0, y:52 }, { opacity:1, y:0, duration:0.45 }, @w(toners));
  tl.fromTo('#wh-2', { opacity:0, y:52 }, { opacity:1, y:0, duration:0.45 }, @w(sun));
""")

# ---------------------------------------------------------------- 28 remember (callback)
S28 = dict(css="""
    #root { background:var(--ink); color:var(--paper); }
    .g28 { display:grid; grid-template-columns:58fr 42fr; gap:var(--s-8);
           align-items:center; height:100%; }
    .nots { display:flex; flex-direction:column; gap:var(--s-5); }
    .nt { position:relative; background:var(--ink-soft); border-radius:var(--r-3);
          padding:var(--s-5) var(--s-6); overflow:hidden;
          font-family:var(--font-body); font-weight:800; font-size:var(--t-frame);
          color:var(--ink-2-dark); }
    .nt .x { position:absolute; inset:0; background:var(--coral); opacity:0; }
""", body="""    <div class="stage">
      <div class="g28">
        <div class="col">
          <p class="kicker on-ink">What you are actually looking at</p>
          <p class="hero" id="rm-h">A survival strategy,<br>borrowed from
            <em style="font-style:normal;color:var(--aqua)">bacteria.</em></p>
        </div>
        <div class="nots">
          <div class="nt" id="nt-0"><div class="x" id="nx-0"></div>The new hyaluronic acid</div>
          <div class="nt" id="nt-1"><div class="x" id="nx-1"></div>A miracle</div>
          <div class="nt" id="nt-2"><div class="wash moss" id="nx-2"></div><span>A genuinely interesting supporting molecule</span></div>
        </div>
      </div>
    </div>""", tl="""
  // Deliberate callback to scene 01: same ink ground, same left-column claim
  // structure, same aqua accent. The two negations are VOIDED at panel scale
  // (scene 01 used 5px bars, which measured as no beat at all); the third is
  // affirmed with a wash instead.
  tl.fromTo('#rm-h', { opacity:0, y:44 }, { opacity:1, y:0, duration:0.60 }, @w(survival));
  // The three cards enter DIM on "remember" -- not yet resolved -- each then
  // lights fully to opacity 1 exactly when its own void/wash beat lands.
  for (var i = 0; i < 3; i++)
    tl.fromTo('#nt-' + i, { opacity:0, x:70 }, { opacity:0.55, x:0, duration:0.45 }, @w(remember)+i*0.45);
  tl.fromTo('#nx-0', { opacity:0 }, { opacity:0.85, duration:0.38 }, @w(Not,1));
  tl.to('#nt-0', { opacity:1, duration:0.30 }, "<");
  tl.fromTo('#nx-1', { opacity:0 }, { opacity:0.85, duration:0.38 }, @w(Not,2));
  tl.to('#nt-1', { opacity:1, duration:0.30 }, "<");
  tl.fromTo('#nx-2', { scaleX:0 }, { scaleX:1, duration:0.75, ease:'power2.inOut' }, @w(genuinely));
  tl.to('#nt-2', { opacity:1, duration:0.30 }, "<");
""")

# ---------------------------------------------------------------- 29 CTA / end screen
S29 = dict(css="""
    #root { background:var(--paper); color:var(--ink); }
    /* END-SCREEN SCENE. The right third and lower-right are reserved for YouTube's
       own overlay elements, so the stage's padding is widened on those two edges
       ONLY here -- the reserve is scene-scoped, not global. Applying it to every
       scene would waste the right third of the whole video. */
    .stage { padding-right: calc(var(--safe-right) + var(--endscreen-right));
             padding-bottom: calc(var(--safe-bottom) + var(--endscreen-bottom)); }
    .g29 { display:flex; flex-direction:column; justify-content:center;
           gap:var(--s-6); height:100%; }
    .action { position:relative; background:var(--ink); color:var(--paper);
              border-radius:var(--r-3); padding:var(--s-7); overflow:hidden; }
""", body="""    <div class="stage">
      <div class="g29">
        <p class="kicker" id="c-k">One thing worth doing</p>
        <div class="action" id="c-act">
          <div class="wash moss" id="c-wash"></div>
          <p class="hero" style="font-size:var(--t-figure)">Turn the bottle around and
            find the actual percentage &mdash; before you buy.</p>
        </div>
        <p class="fig" id="c-q">Would you put a bacteria-made survival molecule
          on your face?</p>
      </div>
    </div>""", tl="""
  // Calm motion by design: YouTube draws its end-screen elements over this scene,
  // and competing movement under them reads as clutter. Three beats, no more.
  tl.fromTo('#c-k', { opacity:0 }, { opacity:1, duration:0.45 }, @first);
  tl.fromTo('#c-act', { opacity:0, y:54 }, { opacity:1, y:0, duration:0.65 }, @first+0.50);
  tl.fromTo('#c-wash', { scaleX:0 }, { scaleX:1, duration:1.00, ease:'power2.inOut' }, @w(percentage));
  tl.fromTo('#c-q', { opacity:0, y:36 }, { opacity:1, y:0, duration:0.60 }, @w(would)-0.10);
""")

# scene id -> module-level spec. Scene NUMBERING and duration are no longer
# carried here at all -- both come from scripts/timing.py's walk(), which
# derives them from the cut, measured voiceover (assets/voice/NN.wav +
# NN.words.json). 09-exclusion absorbs what used to be scenes 09 AND 10 (see
# S09 above); there is no separate 10-messier entry any more.
SCENES_A27 = [
    ("08-humectant", S08),  ("09-exclusion", S09),  ("11-analogy",    S11),
    ("12-load",      S12),  ("13-keratin",   S13),  ("14-notforce",   S14),
    ("15-framing",   S15),  ("16-trial104",  S16),  ("17-preference", S17),
    ("18-eczema",    S18),  ("19-limits",    S19),  ("20-twelve",     S20),
    ("21-verdict",   S21),  ("22-whofor",    S22),  ("23-numbers",    S23),
    ("24-eleven",    S24),  ("25-formula",   S25),  ("26-kbeauty",    S26),
    ("27-resilience",S27),  ("28-remember",  S28),  ("29-cta",        S29),
]
