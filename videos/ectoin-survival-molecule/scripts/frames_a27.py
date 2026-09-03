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
""", body="""    <div class="stage">
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
  tl.fromTo('#p-hum', { opacity:0, x:-120 }, { opacity:1, x:0, duration:0.65 }, 0.10);
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
""")

# ---------------------------------------------------------------- 09 exclusion
S09 = dict(css="""
    #root { background:var(--paper); color:var(--ink); }
    .g9 { display:grid; grid-template-columns:44fr 56fr; gap:var(--s-8);
          align-items:center; height:100%; }
""", body="""    <div class="stage">
      <div class="g9">
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
                font-family="Inter, sans-serif" font-weight="800" font-size="34"
                opacity="0">PROTEIN</text>
        </svg>
      </div>
    </div>""", tl="""
  // The diagram assembles in three LARGE annular layers -- each one is a big
  // area change, which is the beat. Text rides along; it is not the beat.
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
    tl.to('#x-' + i, { opacity:1, duration:0.35 }, 6.00 + i*0.055);
  }
  tl.fromTo('#e-sub', { opacity:0 }, { opacity:1, duration:0.45 }, 8.20);
  // The hydration shell thickens and saturates -- a large annulus, not 18 dots.
  tl.to('#e-shell', { attr:{ 'stroke-width':78 }, opacity:0.55, duration:1.40,
                      ease:'power2.inOut' }, 6.10);
  tl.to('#e-shell', { attr:{ r:214 }, duration:1.60, ease:'power2.inOut' }, 8.60);
""")

# ---------------------------------------------------------------- 10 messier
S10 = dict(css="""
    #root { background:var(--ink); color:var(--paper); }
    .g10 { display:grid; grid-template-columns:52fr 48fr; gap:var(--s-8);
           align-items:center; height:100%; }
    .swap { position:relative; }
    .swap .old { position:absolute; inset:0; }
    /* A full-width PAPER band on the ink ground: a 225-luma step over ~17% of the
       frame. The ring of 18 small squares it replaces measured as no beat. */
    .m-band { background:var(--paper); border-radius:var(--r-3);
              padding:var(--s-5) var(--s-6); margin-top:var(--s-5);
              transform:scaleY(0); transform-origin:50% 0%; }
""", body="""    <div class="stage">
      <div class="g10">
        <div class="col">
          <p class="kicker on-ink">Correction</p>
          <div class="swap" style="min-height:300px">
            <div class="old" id="m-old"><p class="hero" style="color:var(--ink-2-dark)">The tidy version.</p></div>
            <div id="m-new" style="opacity:0"><p class="hero">The honest one<br>is <em style="font-style:normal;color:var(--coral)">messier.</em></p></div>
          </div>
          <div class="m-band" id="m-band">
            <p class="p-body" id="m-note" style="color:var(--ink)">In the simulations ectoin
              also showed some attraction to that surface.</p>
          </div>
        </div>
        <svg viewBox="0 0 620 620" width="100%" height="100%" aria-hidden="true">
          <circle cx="310" cy="310" r="190" fill="none" stroke="#59B8AE"
                  stroke-width="46" opacity="0.22"/>
          <circle cx="310" cy="310" r="112" fill="#F7F5F0"/>
          <g id="m-ring"></g>
        </svg>
      </div>
    </div>""", tl="""
  // Ground is INK -- the whole-frame inversion from scene 09 is itself the
  // largest beat in the piece so far, and it lands on "the honest version".
  tl.to('#m-old', { opacity:0, y:-30, duration:0.50 }, 2.30);
  tl.fromTo('#m-new', { opacity:0, y:40 }, { opacity:1, y:0, duration:0.60 }, 2.55);
  var ring = document.getElementById('m-ring');
  for (var i = 0; i < 18; i++) {
    var a = i * 20 * Math.PI/180;
    var x = 310 + Math.cos(a)*268, y = 310 + Math.sin(a)*268;
    var d = document.createElementNS('http://www.w3.org/2000/svg','rect');
    d.setAttribute('x', x-13); d.setAttribute('y', y-13);
    d.setAttribute('width', 26); d.setAttribute('height', 26);
    d.setAttribute('fill', '#C97A5C');
    d.setAttribute('transform', 'rotate(45 ' + x.toFixed(1) + ' ' + y.toFixed(1) + ')');
    d.id = 'y-' + i; ring.appendChild(d);
    // A THIRD of them break ranks and move to the protein surface -- the actual
    // finding, drawn. Not decoration: this is what the correction says.
    if (i % 3 === 0) {
      tl.to('#y-' + i, { x:-Math.cos(a)*140, y:-Math.sin(a)*140, fill:'#E0A32B',
                         duration:1.5, ease:'power2.inOut' }, 4.60 + (i/3)*0.12);
    }
  }
  tl.fromTo('#m-band', { scaleY:0 }, { scaleY:1, duration:0.60,
                                       ease:'power3.out' }, 5.20);
  // The protein's own shell destabilises -- a full-annulus change in the back half.
  tl.to('#m-ring', { rotation:9, transformOrigin:'310px 310px', duration:3.20,
                     ease:'power1.inOut' }, 7.40);
  // The band recedes and the correction takes the frame -- a second large beat
  // in the back half rather than a 1.04 text scale.
  // RECOLOUR the band, do not scale it. Two earlier versions of this beat were
  // both wrong: retracting to zero left the lower-left sixth at 0.00% ink for
  // 2.5s (a real region void), and retracting to a residual strip squashed the
  // band's own text to 16% height -- illegible, and visibly worse than the void
  // it fixed. A paper->moss recolour is a 140-luma step over ~17% of the frame
  // (per-step ~4.2, comfortably over the floor), keeps the region occupied, and
  // does not deform any type.
  tl.to('#m-band', { backgroundColor:'#4F6B52', duration:0.70,
                     ease:'power2.inOut' }, 10.20);
  tl.to('#m-note', { color:'#F7F5F0', duration:0.70 }, 10.20);
  tl.to('#m-new', { scale:1.10, transformOrigin:'0% 50%', duration:1.30,
                    ease:'power3.out' }, 10.60);
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
  tl.fromTo('#a-star', { opacity:0, scale:0.4, transformOrigin:'310px 280px' },
                       { opacity:1, scale:1, duration:0.60, ease:'back.out(1.6)' }, 1.20);
  var g = document.getElementById('a-guard'), e = document.getElementById('a-ect');
  for (var i = 0; i < 12; i++) {
    var a = i * 30 * Math.PI/180;
    var c = document.createElementNS('http://www.w3.org/2000/svg','circle');
    c.setAttribute('cx', 310 + Math.cos(a)*150); c.setAttribute('cy', 280 + Math.sin(a)*150);
    c.setAttribute('r', 30); c.setAttribute('fill', '#4F6B52'); c.setAttribute('opacity', 0);
    c.id = 'g-' + i; g.appendChild(c);
    tl.to('#g-' + i, { opacity:1, duration:0.30 }, 2.30 + i*0.06);
    var d = document.createElementNS('http://www.w3.org/2000/svg','rect');
    var x = 310 + Math.cos(a+0.26)*250, y = 280 + Math.sin(a+0.26)*250;
    d.setAttribute('x', x-13); d.setAttribute('y', y-13);
    d.setAttribute('width', 26); d.setAttribute('height', 26);
    d.setAttribute('fill', '#C97A5C'); d.setAttribute('opacity', 0);
    d.setAttribute('transform', 'rotate(45 ' + x.toFixed(1) + ' ' + y.toFixed(1) + ')');
    d.id = 'ee-' + i; e.appendChild(d);
    tl.to('#ee-' + i, { opacity:1, duration:0.30 }, 5.60 + i*0.06);
  }
  tl.fromTo('#a-l2', { opacity:0, y:34 }, { opacity:1, y:0, duration:0.55 }, 7.20);
  // the ring visibly TIGHTENS -- a large synchronised move, the scene's last beat
  tl.to('#a-guard', { scale:0.94, transformOrigin:'310px 280px', duration:1.6,
                      ease:'power2.inOut' }, 9.40);
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
""", body="""    <div class="stage">
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
  tl.fromTo('#l-h', { opacity:0, y:34 }, { opacity:1, y:0, duration:0.50 }, 0.15);
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
""")

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
  }
  tl.fromTo('#k-h', { opacity:0, y:36 }, { opacity:1, y:0, duration:0.55 }, 0.20);
  tl.fromTo('#k-s', { opacity:0 }, { opacity:1, duration:0.45 }, 4.60);
  // The strand field arrives as one bundle before it disperses, so the first
  // half of the scene carries a large-area beat too.
  tl.fromTo('#k-strands', { scale:0.55, opacity:0.35, transformOrigin:'310px 260px' },
                          { scale:1, opacity:1, duration:1.60,
                            ease:'power3.out' }, 2.30);
  tl.fromTo('#k-cite', { opacity:0 }, { opacity:1, duration:0.45 }, 8.60);
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
    .cohort i { display:block; width:100%; aspect-ratio:1/1; border-radius:50%;
                background:var(--ink-3); }
""", body="""    <div class="stage">
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
  // The count-up rides it; the GRID is the beat.
  var grid = document.getElementById('t-grid');
  for (var i = 0; i < 104; i++) {
    var d = document.createElement('i'); d.id = 'ct-' + i; grid.appendChild(d);
    tl.set('#ct-' + i, { opacity:0, scale:0.3, transformOrigin:'50% 50%' }, 0);
    tl.to('#ct-' + i, { opacity:1, scale:1, duration:0.30 }, 1.60 + i*0.022);
  }
  var counter = { v:0 }, el = document.getElementById('t-n');
  tl.set('#t-n', { opacity:0 }, 0);   // restates the CSS default, never the sole source
  tl.to('#t-n', { opacity:1, duration:0.30 }, 1.60);
  tl.to(counter, { v:104, duration:2.30, ease:'power1.out',
                   onUpdate:function(){ el.textContent = Math.round(counter.v); } }, 1.60);
  tl.fromTo('#t-h', { opacity:0, y:34 }, { opacity:1, y:0, duration:0.55 }, 4.60);
  // split the cohort into the two arms -- a whole-grid recolour
  for (var j = 0; j < 104; j++) {
    tl.to('#ct-' + j, { backgroundColor: (j % 2 ? '#59B8AE' : '#9C978D'),
                        duration:0.50 }, 6.90 + (j % 13) * 0.05);
  }
  tl.fromTo('#t-cite', { opacity:0 }, { opacity:1, duration:0.45 }, 8.40);
  // The grid physically SPLITS into its two arms -- a whole-column move, where
  // recolouring 104 small dots measured as nothing.
  tl.to('#t-grid', { scaleX:0.92, x:-26, transformOrigin:'50% 50%', duration:1.50,
                     ease:'power2.inOut' }, 9.60);
  tl.to('#t-grid', { scaleY:1.10, duration:1.80, ease:'power2.inOut' }, 12.60);
""")

# ---------------------------------------------------------------- 17 preference
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
""", body="""    <div class="stage">
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
  tl.fromTo('#pr-a', { opacity:0, y:50 }, { opacity:1, y:0, duration:0.50 }, 0.15);
  tl.fromTo('#pr-b', { opacity:0, y:50 }, { opacity:1, y:0, duration:0.50 }, 0.35);
  tl.fromTo('#pr-h', { opacity:0 }, { opacity:1, duration:0.50 }, 1.20);
  // the winning arm floods with colour -- a whole half-width panel, ~20% of frame
  tl.fromTo('#pr-wa', { scaleX:0 }, { scaleX:1, duration:0.90, ease:'power2.inOut' }, 3.00);
  tl.to('#pr-b', { opacity:0.40, duration:0.70 }, 3.20);
  // the qualifier slides up over the result -- the honest beat, and a big one
  tl.set('#pr-q', { opacity:0, y:90 }, 0);
  tl.to('#pr-q', { opacity:1, y:0, duration:0.65, ease:'power3.out' }, 5.90);
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
  tl.fromTo('#ez-n', { opacity:0 }, { opacity:1, duration:0.50 }, 8.20);
  tl.fromTo('#ez-cite', { opacity:0 }, { opacity:1, duration:0.45 }, 10.40);
  // Both bars converge to exactly level -- the finding, made visible as a
  // large-area move rather than two static columns.
  tl.to('#ez-f1', { scaleY:0.76, backgroundColor:'#59B8AE', duration:2.10,
                    ease:'power2.inOut' }, 7.10);
  tl.to('#ez-f2', { scaleY:0.76, backgroundColor:'#59B8AE', duration:2.10,
                    ease:'power2.inOut' }, 7.10);
  tl.to('#ez-prog', { backgroundColor:'#4F6B52', duration:1.20 }, 10.60);
""")

# ---------------------------------------------------------------- 19 limits
S19 = dict(css="""
    #root { background:var(--ink); color:var(--paper); }
    .g19 { display:flex; flex-direction:column; justify-content:center;
           gap:var(--s-6); height:100%; }
    .claims { display:grid; grid-template-columns:repeat(3,1fr); gap:var(--s-5); }
    .cl { position:relative; background:var(--ink-soft); border-radius:var(--r-3);
          padding:var(--s-6); text-align:center; overflow:hidden;
          font-family:var(--font-body); font-weight:800; font-size:var(--t-frame);
          min-height:230px; display:flex; align-items:center; justify-content:center; }
    .cl .x { position:absolute; inset:0; background:var(--coral); opacity:0; }
""", body="""    <div class="stage">
      <div class="g19">
        <p class="hero" id="li-h">Encouraging. Not proof.</p>
        <div class="claims">
          <div class="cl" id="cl-0"><div class="x" id="x-0"></div><span>Cures eczema</span></div>
          <div class="cl" id="cl-1"><div class="x" id="x-1"></div><span>Reverses ageing</span></div>
          <div class="cl" id="cl-2"><div class="x" id="x-2"></div><span>Replaces a prescription</span></div>
        </div>
      </div>
    </div>""", tl="""
  // Three full cards, each ~10% of the frame, and each is VOIDED by a full-card
  // colour flood -- the panel-scale version of a strike-through. This is exactly
  // the beat that read as nothing at 5px in Act 1.
  tl.fromTo('#li-h', { opacity:0, y:40 }, { opacity:1, y:0, duration:0.55 }, 0.15);
  for (var i = 0; i < 3; i++) {
    tl.fromTo('#cl-' + i, { opacity:0, y:56 }, { opacity:1, y:0, duration:0.45 }, 0.80 + i*0.22);
    tl.fromTo('#x-' + i, { opacity:0 }, { opacity:0.88, duration:0.35 }, 2.90 + i*0.75);
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
  var t = document.getElementById('tw-tiles');
  for (var i = 0; i < 12; i++) {
    var d = document.createElement('div'); d.className = 'tile'; d.id = 'tl-' + i;
    t.appendChild(d);
    tl.set('#tl-' + i, { opacity:0, scaleY:0, transformOrigin:'50% 100%' }, 0);
    tl.to('#tl-' + i, { opacity:1, scaleY:1, duration:0.40, ease:'back.out(1.5)' },
          2.60 + i*0.30);
  }
  var c = { v:0 }, el = document.getElementById('tw-n');
  tl.set('#tw-n', { opacity:0 }, 0);   // restates the CSS default, never the sole source
  tl.to('#tw-n', { opacity:1, duration:0.30 }, 2.60);
  tl.to(c, { v:12, duration:3.60, ease:'none',
             onUpdate:function(){ el.textContent = Math.round(c.v); } }, 2.60);
  tl.fromTo('#tw-h', { opacity:0, y:34 }, { opacity:1, y:0, duration:0.50 }, 6.40);
  tl.fromTo('#tw-cite', { opacity:0 }, { opacity:1, duration:0.45 }, 7.60);
""")

# ---------------------------------------------------------------- 21 verdict
S21 = dict(css="""
    #root { background:var(--ink); color:var(--paper); }
    .g21 { display:flex; flex-direction:column; justify-content:center;
           gap:var(--s-6); height:100%; }
    .makers { display:grid; grid-template-columns:repeat(3,1fr); gap:var(--s-5); }
    .mk { background:var(--ink-soft); border-radius:var(--r-3); padding:var(--s-6);
          text-align:center; font-family:var(--font-body); font-weight:800;
          font-size:var(--t-frame); }
    .verdict { position:relative; border-radius:var(--r-3); padding:var(--s-7);
               overflow:hidden; background:var(--ink-soft); text-align:center; }
""", body="""    <div class="stage">
      <div class="g21">
        <p class="kicker on-ink" id="v-k">Some of that research comes from people who sell it</p>
        <div class="makers">
          <div class="mk" id="mk-0">bitop</div>
          <div class="mk" id="mk-1">Merck</div>
          <div class="mk" id="mk-2">Kao</div>
        </div>
        <div class="verdict" id="v-box">
          <div class="wash moss" id="v-wash"></div>
          <p class="hero" id="v-h">Promising supporting ingredient.<br>
            <em style="font-style:normal;color:var(--coral)">Not a miracle molecule.</em></p>
        </div>
      </div>
    </div>""", tl="""
  tl.fromTo('#v-k', { opacity:0 }, { opacity:1, duration:0.40 }, 0.15);
  for (var i = 0; i < 3; i++)
    tl.fromTo('#mk-' + i, { opacity:0, y:52 }, { opacity:1, y:0, duration:0.42 }, 0.70 + i*0.55);
  // The verdict panel enters full-width and then washes -- two large beats on the
  // line the whole act has been building to.
  tl.set('#v-box', { opacity:0, y:70 }, 0);
  tl.to('#v-box', { opacity:1, y:0, duration:0.60, ease:'power3.out' }, 4.10);
  tl.fromTo('#v-wash', { scaleX:0 }, { scaleX:1, duration:1.00, ease:'power2.inOut' }, 5.40);
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
""", body="""    <div class="stage">
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
  tl.fromTo('#wf-h', { opacity:0, y:34 }, { opacity:1, y:0, duration:0.50 }, 0.15);
  for (var i = 0; i < 4; i++) {
    tl.fromTo('#ss-' + i, { opacity:0, y:56 }, { opacity:1, y:0, duration:0.42 }, 0.70 + i*0.42);
    // each card washes as its word is said -- four large area changes, spread
    tl.fromTo('#sw-' + i, { scaleX:0 }, { scaleX:1, duration:0.55,
                                          ease:'power2.inOut' }, 2.70 + i*0.62);
  }
  tl.fromTo('#wf-s', { opacity:0 }, { opacity:1, duration:0.45 }, 8.20);
  for (var j = 0; j < 4; j++)
    tl.fromTo('#fr-' + j, { opacity:0, y:34 }, { opacity:1, y:0, duration:0.40 }, 8.70 + j*0.45);
""")

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
              letter-spacing:var(--tr-mono-wide); color:var(--ink-3-dark);
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
  // two half-width cards, each ~18% of the frame, entering then washing
  tl.fromTo('#bd-0', { opacity:0, x:-90 }, { opacity:1, x:0, duration:0.55 }, 5.20);
  tl.fromTo('#bw-0', { scaleX:0 }, { scaleX:1, duration:0.60, ease:'power2.inOut' }, 5.70);
  tl.fromTo('#bd-1', { opacity:0, x:90 },  { opacity:1, x:0, duration:0.55 }, 7.30);
  tl.fromTo('#bw-1', { scaleX:0 }, { scaleX:1, duration:0.60, ease:'power2.inOut' }, 7.80);
""")

# ---------------------------------------------------------------- 24 the eleven
S24 = dict(css="""
    #root { background:var(--ink); color:var(--paper); }
    .g24 { display:grid; grid-template-columns:48fr 52fr; gap:var(--s-8);
           align-items:center; height:100%; }
    .split { display:flex; gap:var(--s-4); }
    .half { position:relative; flex:1 1 0; min-width:0; border-radius:var(--r-3);
            padding:var(--s-6); text-align:center; }
    .half.p { background:var(--ink-soft); } .half.e { background:var(--aqua); color:var(--ink); }
    .half .v { font-family:var(--font-display); font-size:78px; line-height:1; }
    .half .k { font-family:var(--font-mono); font-size:var(--t-caption);
               letter-spacing:var(--tr-mono-wide); margin-top:var(--s-2); }
    .inci { font-family:var(--font-mono); font-size:26px; line-height:2.0;
            color:var(--ink-3-dark); }
    .inci b { color:var(--paper); font-weight:500; background:var(--ink-soft);
              padding:3px 10px; border-radius:var(--r-2); }
    .inci b.hit { background:var(--aqua); color:var(--ink); }
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
      <div class="g24">
        <div class="col">
          <p class="kicker on-ink">Abib &middot; Ectoin Panthenol 11%</p>
          <p class="hero" id="el-n">11%</p>
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
            1. Water &nbsp; <b id="in-p">2. Panthenol</b> &nbsp; 3. Propanediol<br>
            4. Cetyl Ethylhexanoate &nbsp; 5. Squalane<br>
            6. Diisobutyl Adipate &nbsp; 7. Vinyl Dimethicone<br>
            8. Propylheptyl Caprylate &nbsp; 9. Cetearyl Alcohol<br>
            10. Glyceryl Glucoside &nbsp; <b id="in-e">11. Ectoin</b>
          </div>
        </div>
      </div>
    </div>""", tl="""
  // The 11% SPLITTING into its two parts is the act's payoff, and it is a
  // panel-scale move: a hero number replaced by two filled cards.
  tl.fromTo('#el-n', { opacity:0, scale:0.7, transformOrigin:'0% 50%' },
                     { opacity:1, scale:1, duration:0.60, ease:'back.out(1.4)' }, 0.30);
  tl.to('#el-n', { opacity:0.25, scale:0.72, transformOrigin:'0% 50%', duration:0.55 }, 3.60);
  tl.fromTo('#el-split', { opacity:0, y:44 }, { opacity:1, y:0, duration:0.60 }, 3.80);
  tl.fromTo('#el-inci', { opacity:0, x:60 }, { opacity:1, x:0, duration:0.60 }, 6.00);
  tl.fromTo('#in-p', { backgroundColor:'#211F1B' },
                     { backgroundColor:'#59B8AE', color:'#131516', duration:0.45 }, 7.60);
  tl.fromTo('#in-e', { backgroundColor:'#211F1B' },
                     { backgroundColor:'#59B8AE', color:'#131516', duration:0.45 }, 9.00);
  tl.fromTo('#el-note', { opacity:0, y:30 }, { opacity:1, y:0, duration:0.55 }, 10.40);
  // The two halves of the 11% resolve at panel scale in the back half.
  // The proportion bar draws across the full column in the back half, where the
  // scene previously held for 7.25s on two small chip highlights.
  tl.to('#el-prop', { opacity:1, duration:0.30 }, 9.40);
  tl.fromTo('#el-pp', { scaleX:0 }, { scaleX:1, duration:1.05, ease:'power2.out' }, 9.50);
  tl.fromTo('#el-pe', { scaleX:0 }, { scaleX:1, duration:0.45, ease:'power2.out' }, 10.60);
  tl.to('#el-inci', { opacity:0.40, duration:1.10 }, 11.60);
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
""", body="""    <div class="stage">
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
  tl.fromTo('#kb-neg', { opacity:0, x:-90 }, { opacity:1, x:0, duration:0.55 }, 0.15);
  tl.fromTo('#kb-void', { opacity:0 }, { opacity:0.85, duration:0.45 }, 2.30);
  tl.fromTo('#kb-pos', { opacity:0, x:90 }, { opacity:1, x:0, duration:0.55 }, 3.60);
  tl.fromTo('#kb-wash', { scaleX:0 }, { scaleX:1, duration:0.90, ease:'power2.inOut' }, 4.40);
  tl.to('#kb-neg', { opacity:0.35, duration:0.70 }, 4.40);
""")

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
    .arrow { font-family:var(--font-mono); font-size:var(--t-hero); color:var(--ink-3); }
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
  tl.fromTo('#sh-w', { scaleX:0 }, { scaleX:1, duration:0.80, ease:'power2.inOut' }, 2.90);
  tl.to('#sh-a', { opacity:0.40, duration:0.60 }, 2.90);
  tl.fromTo('#wh-h', { opacity:0 }, { opacity:1, duration:0.45 }, 6.60);
  for (var i = 0; i < 3; i++)
    tl.fromTo('#wh-' + i, { opacity:0, y:52 }, { opacity:1, y:0, duration:0.45 }, 7.20 + i*0.75);
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
  tl.fromTo('#rm-h', { opacity:0, y:44 }, { opacity:1, y:0, duration:0.60 }, 0.20);
  for (var i = 0; i < 3; i++)
    tl.fromTo('#nt-' + i, { opacity:0, x:70 }, { opacity:1, x:0, duration:0.45 }, 1.30 + i*0.45);
  tl.fromTo('#nx-0', { opacity:0 }, { opacity:0.85, duration:0.38 }, 5.20);
  tl.fromTo('#nx-1', { opacity:0 }, { opacity:0.85, duration:0.38 }, 6.30);
  tl.fromTo('#nx-2', { scaleX:0 }, { scaleX:1, duration:0.75, ease:'power2.inOut' }, 7.60);
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
  tl.fromTo('#c-k', { opacity:0 }, { opacity:1, duration:0.45 }, 0.20);
  tl.fromTo('#c-act', { opacity:0, y:54 }, { opacity:1, y:0, duration:0.65 }, 0.70);
  tl.fromTo('#c-wash', { scaleX:0 }, { scaleX:1, duration:1.00, ease:'power2.inOut' }, 2.30);
  tl.fromTo('#c-q', { opacity:0, y:36 }, { opacity:1, y:0, duration:0.60 }, 5.20);
""")

# scene id -> (module-level spec, VO take number)
SCENES_A27 = [
    ("08-humectant", S08, 8),  ("09-exclusion", S09, 9),  ("10-messier", S10, 10),
    ("11-analogy",   S11, 11), ("12-load",      S12, 12), ("13-keratin", S13, 13),
    ("14-notforce",  S14, 14), ("15-framing",   S15, 15), ("16-trial104", S16, 16),
    ("17-preference",S17, 17), ("18-eczema",    S18, 18), ("19-limits",  S19, 19),
    ("20-twelve",    S20, 20), ("21-verdict",   S21, 21), ("22-whofor",  S22, 22),
    ("23-numbers",   S23, 23), ("24-eleven",    S24, 24), ("25-formula", S25, 25),
    ("26-kbeauty",   S26, 26), ("27-resilience",S27, 27), ("28-remember",S28, 28),
    ("29-cta",       S29, 29),
]
