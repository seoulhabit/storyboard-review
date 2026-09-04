#!/usr/bin/env python3
"""Retention-master scene overrides (2026-09-04, session/ectoin-retention).

Applied over build_frames.FRAME_DEFS. Every override keeps the scene id, its
walk()-derived duration, its VO word markers and its transition kind; what
changes is the PICTURE: photoreal plates (assets/plates/*.jpg|mp4, prepared by
scripts/prep_plates.py) under text that now sits on scrims instead of a flat
page ground.

Plate rules, decided once here:
  - Plates are FULL-BLEED. Text and UI stay inside the safe box. The project's
    safe-area gate assumes a flat page ground and reads a photograph's margins
    as "ink"; it is therefore N/A on plate scenes (RETENTION-PLAN.md).
  - Every conceptual science plate carries the CONCEPTUAL VISUALIZATION chip.
  - Ectoin is never drawn as a shield, a barrier, or attached to a protein --
    the hydration-layer plates show small molecules hovering AWAY from the
    surface, and the honest-version diagram in 09 is kept as authored.
  - A `<video class="clip">` plate is pre-padded to at least its data-duration
    (prep_plates.py tpad-clones the last frame) so a clip never runs out
    under a scene that outlives it.
"""
from frames_a27 import CHBAND_CSS, CHBAND_TL, chband_body

# ---------------------------------------------------------------- shared
PLATE_CSS = """
    #root { color:var(--paper); }
    .plate { position:absolute; inset:0; overflow:hidden; z-index:0; }
    .plate > video, .plate > img { position:absolute; left:0; top:0;
             width:1920px; height:1080px; object-fit:cover; display:block;
             transform-origin:50% 50%; }
    .scrim { position:absolute; inset:0; z-index:1; pointer-events:none; }
    .scrim.l { background:linear-gradient(90deg, rgba(19,21,22,.88) 0%,
               rgba(19,21,22,.72) 36%, rgba(19,21,22,.18) 60%, rgba(19,21,22,0) 74%); }
    .scrim.r { background:linear-gradient(270deg, rgba(19,21,22,.88) 0%,
               rgba(19,21,22,.72) 36%, rgba(19,21,22,.18) 60%, rgba(19,21,22,0) 74%); }
    .scrim.b { background:linear-gradient(0deg, rgba(19,21,22,.90) 0%,
               rgba(19,21,22,.62) 28%, rgba(19,21,22,.10) 52%, rgba(19,21,22,0) 66%); }
    .scrim.t { background:linear-gradient(180deg, rgba(19,21,22,.70) 0%,
               rgba(19,21,22,.20) 22%, rgba(19,21,22,0) 40%); }
    .scrim.full { background:rgba(19,21,22,.58); }
    .scrim.ink { background:rgba(19,21,22,.74); }
    .scrim.paper { background:rgba(247,245,240,.82); }
    .flash { position:absolute; inset:0; z-index:3; background:#DCEFEC; opacity:0;
             pointer-events:none; }
    .stage { position:relative; z-index:2; }
    .chband { z-index:10; }
    /* CONCEPTUAL VISUALIZATION chip -- top-right, inside the safe box. */
    .cv { position:absolute; top:calc(var(--safe-top) + 6px); right:var(--safe-right);
          z-index:4; margin:0; width:max-content;
          font-family:var(--font-mono); font-size:var(--t-caption);
          letter-spacing:var(--tr-mono-wide); text-transform:uppercase;
          color:rgba(247,245,240,.82); background:rgba(19,21,22,.46);
          border:1.5px solid rgba(247,245,240,.38); border-radius:var(--r-pill);
          padding:8px 18px; opacity:0; }
    /* lower-third block: translucent ink card */
    .lt { position:absolute; left:var(--safe-left); bottom:var(--safe-bottom);
          z-index:4; max-width:1040px; background:rgba(19,21,22,.70);
          border-radius:var(--r-3); padding:var(--s-5) var(--s-6);
          display:flex; flex-direction:column; gap:var(--s-3); }
    .lt .kicker { color:var(--ink-3-dark); }
    .lt .line { font-family:var(--font-display); font-size:var(--t-figure);
                line-height:var(--lh-snug); margin:0; color:var(--paper); }
    .lt .line b { font-weight:400; color:var(--coral); }
    .lt .line i { font-style:normal; color:var(--aqua); }
    .pill { display:inline-flex; align-items:center; background:rgba(19,21,22,.78);
            color:var(--paper); border-radius:var(--r-pill); padding:14px 30px;
            font-family:var(--font-body); font-weight:800; font-size:var(--t-body);
            white-space:nowrap; border:2px solid rgba(247,245,240,.16); }
    .pill.coral { background:var(--coral); color:var(--ink); border-color:transparent; }
    .pill.aqua { background:var(--aqua); color:var(--ink); border-color:transparent; }
    .cite.on-plate { color:var(--paper); border-color:rgba(247,245,240,.45);
                     background:rgba(19,21,22,.55); }
    .mark { position:absolute; left:var(--safe-left); bottom:var(--safe-bottom);
            right:auto; width:max-content; margin:0; z-index:4;
            font-family:var(--font-mono); font-size:var(--t-label);
            letter-spacing:0.42em; color:var(--aqua); text-transform:uppercase; }
"""


def pv(pid, src, start, dur, style=""):
    """Full-bleed video plate. start/dur on the SCENE's own clock."""
    return (f'    <div class="plate" id="pl-{pid}"><video class="clip" id="pv-{pid}" '
            f'src="assets/plates/{src}" data-start="{start:.3f}" '
            f'data-duration="{dur:.3f}" muted playsinline'
            f'{(" style=" + chr(34) + style + chr(34)) if style else ""}></video></div>\n')


def pi(pid, src, style="", wrap_style=""):
    """Full-bleed still plate."""
    ws = f' style="{wrap_style}"' if wrap_style else ""
    st = f' style="{style}"' if style else ""
    return (f'    <div class="plate" id="pl-{pid}"{ws}><img id="pi-{pid}" '
            f'src="assets/plates/{src}" alt=""{st}></div>\n')


def scrim(kind, sid="", style=""):
    i = f' id="{sid}"' if sid else ""
    s = f' style="{style}"' if style else ""
    return f'    <div class="scrim {kind}"{i}{s}></div>\n'


CV = '    <p class="cv" id="cv">Conceptual visualization</p>\n'
FLASH = '    <div class="flash" id="flash"></div>\n'


def kb(sel, at, dur, s0=1.0, s1=1.08, x0=0, x1=0, y0=0, y1=0):
    """Ken Burns: one continuous transform on a plate element."""
    return (f"  tl.fromTo('{sel}', {{ scale:{s0}, x:{x0}, y:{y0} }}, "
            f"{{ scale:{s1}, x:{x1}, y:{y1}, duration:{dur:.3f}, ease:'none' }}, {at});\n")


def cv_in(at):
    return f"  tl.fromTo('#cv', {{ opacity:0 }}, {{ opacity:1, duration:0.35 }}, {at});\n"


# ---------------------------------------------------------------- 01 hook
S01 = dict(css=PLATE_CSS + """
    .s1 { display:grid; grid-template-columns:58fr 42fr; gap:var(--s-8);
          align-items:stretch; height:100%; }
    .s1-claim-wrap { display:flex; align-items:center; min-height:0; }
    .s1-claim { font-family:var(--font-display); font-size:var(--t-hero);
                line-height:var(--lh-tight); letter-spacing:var(--tr-display);
                margin:0; color:var(--paper); text-shadow:0 2px 24px rgba(0,0,0,.35); }
    .s1-claim em { font-style:normal; color:var(--aqua); }
    .s1-neg { display:flex; flex-direction:column; gap:var(--s-4);
              min-height:0; height:100%; justify-content:center; }
    .s1-neg-h { flex:0 0 auto; font-family:var(--font-mono); font-size:var(--t-label);
                letter-spacing:var(--tr-mono-wide); color:rgba(247,245,240,.7);
                text-transform:uppercase; margin:0 0 var(--s-2); }
    .s1-item { position:relative; flex:0 0 auto; height:150px;
               display:flex; align-items:center; overflow:hidden;
               background:rgba(19,21,22,.78); border-radius:var(--r-3);
               padding:var(--s-5) var(--s-6);
               font-family:var(--font-body); font-weight:800;
               font-size:var(--t-frame); color:rgba(247,245,240,.85); }
    .s1-item > span:not(.bar) { position:relative; z-index:1; }
    .s1-item .bar { position:absolute; inset:0; transform:scaleX(0);
                    transform-origin:0% 50%; background:var(--coral); }
""", body=(
    pv("a", "V01-saltlake.mp4", 0.0, 6.2)
    + pi("b", "I02-droplet.jpg", wrap_style="opacity:0")
    + scrim("l")
    + """    <div class="stage">
      <div class="s1">
        <div class="s1-claim-wrap">
          <h1 class="s1-claim" id="s1-claim"><span id="s1-c1">Your next favourite
            skincare ingredient</span><span id="s1-c2"> may have been invented
            by </span><em id="s1-bacteria">bacteria trying not to die.</em></h1>
        </div>
        <div class="s1-neg flexmin">
          <p class="s1-neg-h" id="s1-negh" style="opacity:0">Not this</p>
          <div class="s1-item" id="s1-i1"><span class="bar" id="s1-b1"></span><span>Snail mucin</span></div>
          <div class="s1-item" id="s1-i2"><span class="bar" id="s1-b2"></span><span>Salmon DNA</span></div>
          <div class="s1-item" id="s1-i3"><span class="bar" id="s1-b3"></span><span>Hyaluronic acid</span></div>
        </div>
      </div>
    </div>
"""
    + '    <p class="mark" id="s1-mark">ECTOIN</p>\n'
), tl="""
  // Frame zero is already a moving photoreal salt lake (V01). The claim's first
  // chunk is at rest at t=0; chunks 2/3 land on their own words.
  tl.set('#s1-c1', { opacity:1, y:0 }, 0);
  tl.fromTo('#s1-c2', { opacity:0, y:14 }, { opacity:1, y:0, duration:0.45 }, @w(may)-0.10);
  tl.fromTo('#s1-bacteria', { opacity:0, y:14 }, { opacity:1, y:0, duration:0.45 }, @w(bacteria)-0.10);
""" + kb('#pv-a', 0, 6.2, 1.0, 1.06) + """
  // Cut to the brine-droplet macro on "Not snail" -- the descent from lake to
  // droplet the next scene dives into. 0.35s dissolve, then a push-in.
  tl.fromTo('#pl-b', { opacity:0 }, { opacity:1, duration:0.35 }, @w(Not,2)-0.35);
""" + kb('#pi-b', '@w(Not,2)-0.35', 6.5, 1.0, 1.16) + """
  tl.fromTo('#s1-negh', { opacity:0 }, { opacity:1, duration:0.3 }, @w(Not,2)-0.30);
  tl.fromTo('#s1-i1', { opacity:0, x:52 }, { opacity:1, x:0, duration:0.45 }, @w(Not,2)-0.10);
  tl.fromTo('#s1-i2', { opacity:0, x:52 }, { opacity:1, x:0, duration:0.45 }, @w(Not,3)-0.10);
  tl.fromTo('#s1-i3', { opacity:0, x:52 }, { opacity:1, x:0, duration:0.45 }, @w(Not,4)-0.10);
  tl.fromTo('#s1-b1', { scaleX:0 }, { scaleX:1, duration:0.30, ease:'power2.inOut' }, @we(mucin)+0.10);
  tl.to('#s1-i1', { color:'#131516', duration:0.30 }, @we(mucin)+0.10);
  tl.fromTo('#s1-b2', { scaleX:0 }, { scaleX:1, duration:0.30, ease:'power2.inOut' }, @we(DNA)+0.10);
  tl.to('#s1-i2', { color:'#131516', duration:0.30 }, @we(DNA)+0.10);
  tl.fromTo('#s1-b3', { scaleX:0 }, { scaleX:1, duration:0.30, ease:'power2.inOut' }, @we(acid)+0.10);
  tl.to('#s1-i3', { color:'#131516', duration:0.30 }, @we(acid)+0.10);
  tl.fromTo('#s1-mark', { opacity:0, y:-24 }, { opacity:1, y:0, duration:0.60 }, @last-0.4);
  tl.fromTo('#s1-claim', { y:0 }, { y:-14, duration:1.60, ease:'power1.inOut' }, @last-0.4);
""")

# ---------------------------------------------------------------- 02 osmosis
S02 = dict(css=PLATE_CSS, body=(
    pv("a", "V02-dive.mp4", 0.0, 3.6)
    + pv("b", "V03-orbit.mp4", 3.3, 6.0)
    + scrim("b")
    + FLASH
    + """    <div class="stage"></div>
    <div class="lt" id="lt">
      <p class="kicker" id="s2-k">The problem it solves</p>
      <p class="line" id="s2-l1">Some places are so salty and so dry
        that an ordinary cell <b>loses its water</b></p>
      <p class="line" id="s2-l2">&mdash; and stops working.</p>
    </div>
"""
    + CV
), tl="""
  // Race into the droplet (V02, sped up), flash, and we are inside the brine
  // with the bacterium (V03) -- its membrane puckers as salt pulls water out.
  tl.fromTo('#flash', { opacity:0 }, { opacity:0.9, duration:0.12, ease:'power2.in' }, 3.22);
  tl.to('#flash', { opacity:0, duration:0.40, ease:'power2.out' }, 3.36);
""" + kb('#pv-b', 3.3, 5.9, 1.04, 1.12) + cv_in(3.6) + """
  tl.fromTo('#lt', { opacity:0, y:30 }, { opacity:1, y:0, duration:0.45 }, 0.25);
  tl.set(['#s2-l1','#s2-l2'], { opacity:0 }, 0);
  tl.fromTo('#s2-l1', { opacity:0, y:24 }, { opacity:1, y:0, duration:0.50 }, @w(salty)-0.35);
  tl.fromTo('#s2-l2', { opacity:0, y:24 }, { opacity:1, y:0, duration:0.50 }, @w(stop)-0.35);
""")

# ---------------------------------------------------------------- 03 now
S03 = dict(css=PLATE_CSS + """
    .s3-row { position:absolute; left:var(--safe-left); top:calc(var(--safe-top) + 6px);
              z-index:4; display:flex; gap:var(--s-4); }
    .s3-lock { position:absolute; left:var(--safe-left); right:var(--safe-right);
               bottom:var(--safe-bottom); z-index:4; overflow:hidden;
               background:rgba(19,21,22,.84); border-radius:var(--r-3);
               padding:var(--s-6) var(--s-7); display:grid;
               grid-template-columns:auto 1fr; gap:var(--s-7); align-items:center; }
    .s3-lock .wash { position:absolute; inset:0; background:var(--aqua);
                     transform:scaleX(0); transform-origin:0% 50%; }
    .s3-lock > *:not(.wash) { position:relative; z-index:1; }
    .s3-mark { font-family:var(--font-display); font-size:140px; line-height:1;
               letter-spacing:0.06em; margin:0; color:var(--paper); }
    .s3-sub { font-family:var(--font-body); font-weight:800; font-size:var(--t-frame);
              line-height:var(--lh-snug); color:rgba(247,245,240,.82); margin:0; }
    .s3-sub .rule { display:block; height:4px; width:260px; background:var(--coral);
                    margin-bottom:var(--s-4); transform:scaleX(0); transform-origin:0% 50%; }
""", body=(
    pv("a", "V08-hydration.mp4", 0.0, 3.8)
    + pv("b", "V05-bottle.mp4", 3.5, 7.5)
    + scrim("b", style="opacity:0", sid="sc-b")
    + """    <div class="stage"></div>
    <div class="lt" id="lt" style="max-width:760px">
      <p class="kicker">Inside the cell</p>
      <p class="line">Ectoin, <i>hanging back</i> from the protein</p>
    </div>
    <div class="s3-row">
      <span class="pill" id="s3-p1" style="opacity:0">Serums</span>
      <span class="pill" id="s3-p2" style="opacity:0">Creams</span>
      <span class="pill" id="s3-p3" style="opacity:0">Sunscreens</span>
    </div>
    <div class="s3-lock" id="s3-lock" style="opacity:0">
      <div class="wash" id="s3-wash"></div>
      <p class="s3-mark" id="s3-mark">ECTOIN</p>
      <p class="s3-sub" id="s3-sub"><span class="rule" id="s3-rule"></span>the science is
        stranger than the marketing</p>
    </div>
"""
    + CV
), tl="""
  // 0-3.5s: the payoff of the microbe story (ectoin hovering off the protein,
  // water ordered) -- then a match cut, droplet to droplet, into unbranded
  // packaging on "Korean". The ECTOIN lockup lands on its own word.
""" + kb('#pv-a', 0, 3.8, 1.0, 1.05) + cv_in(0.3) + """
  tl.fromTo('#lt', { opacity:0, y:24 }, { opacity:1, y:0, duration:0.4 }, 0.5);
  tl.to('#lt', { opacity:0, duration:0.25 }, @w(Korean)-0.30);
  tl.to('#cv', { opacity:0, duration:0.25 }, @w(Korean)-0.30);
  tl.fromTo('#pl-b', { opacity:0 }, { opacity:1, duration:0.22 }, @w(Korean)-0.22);
""" + kb('#pv-b', '@w(Korean)-0.22', 7.6, 1.0, 1.07) + """
  tl.fromTo('#s3-p1', { opacity:0, y:-16 }, { opacity:1, y:0, duration:0.35 }, @w(serums)-0.10);
  tl.fromTo('#s3-p2', { opacity:0, y:-16 }, { opacity:1, y:0, duration:0.35 }, @w(creams)-0.10);
  tl.fromTo('#s3-p3', { opacity:0, y:-16 }, { opacity:1, y:0, duration:0.35 }, @w(sunscreens)-0.10);
  tl.to('#sc-b', { opacity:1, duration:0.5 }, @w(ectoin)-0.8);
  tl.fromTo('#s3-lock', { opacity:0, y:60 }, { opacity:1, y:0, duration:0.55, ease:'power3.out' }, @w(ectoin)-0.45);
  tl.fromTo('#s3-mark', { scaleX:1.16, transformOrigin:'0% 50%' }, { scaleX:1, duration:0.9, ease:'power3.out' }, @w(ectoin)-0.35);
  tl.fromTo('#s3-rule', { scaleX:0 }, { scaleX:1, duration:0.6, ease:'power2.inOut' }, @w(stranger)-0.30);
  tl.fromTo('#s3-wash', { scaleX:0 }, { scaleX:1, duration:0.9, ease:'power2.inOut' }, @w(stranger)-0.20);
  tl.to(['#s3-mark','#s3-sub'], { color:'#131516', duration:0.5 }, @w(stranger));
""")

# ---------------------------------------------------------------- 05 halomonas
S05 = dict(css=PLATE_CSS + """
    .s5 { display:grid; grid-template-columns:50fr 50fr; gap:var(--s-8);
          align-items:center; height:100%; }
    .s5-l { display:flex; flex-direction:column; gap:var(--s-4); min-height:0; }
    .s5-name { font-family:var(--font-display); font-style:italic;
               font-size:var(--t-hero); line-height:var(--lh-tight); margin:0; }
    .s5-note { font-family:var(--font-display); font-size:var(--t-figure);
               line-height:var(--lh-snug); margin:0; }
    .s5-note b { font-weight:400; color:var(--aqua); }
    .tint { position:absolute; inset:0; z-index:1; background:var(--aqua); opacity:0;
            mix-blend-mode:screen; }
""", body=(
    pv("a", "V06-colony.mp4", 0.0, 11.1)
    + '    <div class="tint" id="tint"></div>\n'
    + scrim("l")
    + """    <div class="stage">
      <div class="s5">
        <div class="s5-l flexmin">
          <p class="kicker on-ink" id="s5-k">Where it comes from</p>
          <p class="s5-name" id="s5-name">Halomonas elongata</p>
          <p class="s5-note" id="s5-note">Lives in salt. When the outside gets
            punishing, it <b>floods itself with ectoin</b>.</p>
          <div style="margin-top:20px"><span class="cite on-plate" id="s5-cite">Environ Microbiol &middot; 2010</span></div>
        </div>
        <div></div>
      </div>
    </div>
"""
    + CV
), tl=kb('#pv-a', 0, 11.1, 1.0, 1.08) + cv_in(0.3) + """
  tl.fromTo('#s5-k',    { opacity:0, y:30 }, { opacity:1, y:0, duration:0.40 }, 0.20);
  tl.fromTo('#s5-name', { opacity:0, y:46 }, { opacity:1, y:0, duration:0.55 }, @w(Halomonas)-0.30);
  tl.fromTo('#s5-note', { opacity:0, y:44 }, { opacity:1, y:0, duration:0.55 }, @w(lives)-0.20);
  tl.fromTo('#s5-cite', { opacity:0 },       { opacity:1, duration:0.45 }, @last-1.4);
  // "floods itself with ectoin": the whole plate tints aqua for a beat.
  tl.fromTo('#tint', { opacity:0 }, { opacity:0.22, duration:0.45, ease:'power2.out' }, @w(floods)-0.10);
  tl.to('#tint', { opacity:0.08, duration:1.4, ease:'power1.inOut' }, @w(floods)+0.40);
""")

# ---------------------------------------------------------------- 06 mechanism
S06 = dict(css=PLATE_CSS + """
    .s6-h { position:absolute; left:var(--safe-left); top:calc(var(--safe-top) + 10px);
            z-index:4; margin:0; font-family:var(--font-display); font-size:var(--t-figure);
            line-height:var(--lh-snug); max-width:1100px;
            text-shadow:0 2px 20px rgba(0,0,0,.45); }
    .s6-row { position:absolute; left:var(--safe-left); right:var(--safe-right);
              bottom:var(--safe-bottom); z-index:4; display:grid;
              grid-template-columns:repeat(4,1fr); gap:var(--s-4); }
    .s6-step { position:relative; background:rgba(19,21,22,.80); border-radius:var(--r-3);
               padding:var(--s-4) var(--s-5); overflow:hidden; min-height:150px;
               display:flex; flex-direction:column; gap:var(--s-2); justify-content:center; }
    .s6-step .fill { position:absolute; inset:0; background:var(--celadon);
                     transform:scaleY(0); transform-origin:50% 100%; }
    .s6-step > *:not(.fill) { position:relative; z-index:1; }
    .s6-num { font-family:var(--font-mono); font-size:var(--t-caption);
              letter-spacing:var(--tr-mono-wide); color:rgba(247,245,240,.6); }
    .s6-lab { font-family:var(--font-body); font-weight:800; font-size:34px;
              line-height:var(--lh-snug); margin:0; }
    .s6-step.on .s6-num, .s6-step.on .s6-lab { color:var(--ink); }
""", body=(
    pv("a", "V07-osmosis.mp4", 0.0, 9.7)
    + scrim("b")
    + scrim("t")
    + """    <div class="stage"></div>
    <p class="s6-h" id="s6-h">Salt pulls water out of cells.</p>
    <div class="s6-row">
      <div class="s6-step" id="s6-s1"><div class="fill" id="s6-f1"></div>
        <span class="s6-num">01</span><p class="s6-lab">Water leaves</p></div>
      <div class="s6-step" id="s6-s2"><div class="fill" id="s6-f2"></div>
        <span class="s6-num">02</span><p class="s6-lab">Proteins lose their shape</p></div>
      <div class="s6-step" id="s6-s3"><div class="fill" id="s6-f3"></div>
        <span class="s6-num">03</span><p class="s6-lab">Membranes get unstable</p></div>
      <div class="s6-step" id="s6-s4"><div class="fill" id="s6-f4" style="background:var(--coral)"></div>
        <span class="s6-num">04</span><p class="s6-lab">The cell stops working</p></div>
    </div>
"""
    + CV
), tl=kb('#pv-a', 0, 9.7, 1.02, 1.10) + cv_in(0.3) + """
  tl.fromTo('#s6-h', { opacity:0, y:-20 }, { opacity:1, y:0, duration:0.50 }, @w(Because)-0.20);
  tl.fromTo('#s6-s1', { opacity:0, y:40 }, { opacity:1, y:0, duration:0.45 }, @w(Lose)-0.35);
  tl.fromTo('#s6-f1', { scaleY:0 }, { scaleY:1, duration:0.55, ease:'power2.out' }, @w(Lose)+0.10);
  tl.to('#s6-s1', { color:'#131516', duration:0.3 }, @w(Lose)+0.10);
  tl.fromTo('#s6-s2', { opacity:0, y:40 }, { opacity:1, y:0, duration:0.45 }, @w(proteins)-0.30);
  tl.fromTo('#s6-f2', { scaleY:0 }, { scaleY:1, duration:0.55, ease:'power2.out' }, @w(shape)-0.20);
  tl.to('#s6-s2', { color:'#131516', duration:0.3 }, @w(shape)-0.20);
  tl.fromTo('#s6-s3', { opacity:0, y:40 }, { opacity:1, y:0, duration:0.45 }, @w(membranes)-0.30);
  tl.fromTo('#s6-f3', { scaleY:0 }, { scaleY:1, duration:0.55, ease:'power2.out' }, @w(unstable)-0.10);
  tl.to('#s6-s3', { color:'#131516', duration:0.3 }, @w(unstable)-0.10);
  tl.fromTo('#s6-s4', { opacity:0, y:40 }, { opacity:1, y:0, duration:0.45 }, @w(cell)-0.30);
  tl.fromTo('#s6-f4', { scaleY:0 }, { scaleY:1, duration:0.55, ease:'power2.out' }, @w(stops)-0.10);
  tl.to('#s6-s4', { color:'#131516', duration:0.3 }, @w(stops)-0.10);
""")

# ---------------------------------------------------------------- 07 question
S07 = dict(css=PLATE_CSS + """
    .s7-q { position:absolute; left:var(--safe-left); bottom:var(--safe-bottom);
            z-index:4; max-width:1180px; margin:0;
            font-family:var(--font-display); font-size:var(--t-hero);
            line-height:var(--lh-tight); letter-spacing:var(--tr-display);
            text-shadow:0 2px 26px rgba(0,0,0,.45); }
    .s7-q em { font-style:normal; color:var(--aqua); }
    .s7-under { display:inline-block; }
""", body=(
    pv("a", "V08-hydration.mp4", 0.0, 6.6)
    + pi("b", "C-baseskin.jpg", wrap_style="opacity:0")
    + scrim("b", sid="sc-b")
    + """    <div class="stage"></div>
    <div class="lt" id="lt" style="max-width:900px">
      <p class="kicker" id="s7-k">What it does for the microbe</p>
      <p class="line" id="s7-line">Keeps the space around fragile
        structures <i>survivable</i>.</p>
    </div>
    <p class="s7-q" id="s7-q" style="opacity:0">So could it do the same for
      <em>stressed <span class="s7-under" id="s7-under">human skin?</span></em></p>
"""
    + CV
), tl=kb('#pv-a', 0, 6.6, 1.06, 1.0) + cv_in(0.3) + """
  tl.fromTo('#lt', { opacity:0, y:24 }, { opacity:1, y:0, duration:0.45 }, 0.25);
  // The act's hook: cut from the microbe to real skin on "Could".
  tl.to('#lt', { opacity:0, y:-10, duration:0.30 }, @w(Could)-0.55);
  tl.to('#cv', { opacity:0, duration:0.25 }, @w(Could)-0.55);
  tl.fromTo('#pl-b', { opacity:0 }, { opacity:1, duration:0.30 }, @w(Could)-0.35);
""" + kb('#pi-b', '@w(Could)-0.35', 4.5, 1.0, 1.10, 0, -40) + """
  tl.fromTo('#s7-q', { opacity:0, y:58 }, { opacity:1, y:0, duration:0.70 }, @w(Could)-0.05);
  tl.fromTo('#s7-under', { backgroundImage:
      'linear-gradient(#C97A5C,#C97A5C)', backgroundRepeat:'no-repeat',
      backgroundSize:'0% 5px', backgroundPosition:'0% 100%' },
    { backgroundSize:'100% 5px', duration:0.55, ease:'power2.inOut' }, @w(stressed));
""")

# ---------------------------------------------------------------- 08 humectant (chapter)
S08 = dict(css=PLATE_CSS + CHBAND_CSS + """
    .s8-h { position:absolute; left:var(--safe-left); right:var(--safe-right);
            top:230px; z-index:4; margin:0; font-family:var(--font-display);
            font-size:var(--t-hero); line-height:var(--lh-tight); max-width:1300px;
            text-shadow:0 2px 24px rgba(0,0,0,.45); }
    .s8-h em { font-style:normal; color:var(--coral); }
    .g2 { position:absolute; left:var(--safe-left); right:var(--safe-right);
          top:calc(var(--safe-top) + 130px); bottom:var(--safe-bottom); z-index:4;
          display:grid; grid-template-columns:1fr 1fr; gap:var(--s-6); }
    .card { position:relative; border-radius:var(--r-3); overflow:hidden;
            background:var(--ink-soft); }
    .card img { position:absolute; left:0; top:0; width:100%; height:100%;
                object-fit:cover; transform-origin:50% 50%; }
    .card .cap { position:absolute; left:0; right:0; bottom:0; padding:var(--s-5) var(--s-6);
                 background:linear-gradient(0deg, rgba(19,21,22,.92), rgba(19,21,22,.55) 70%, rgba(19,21,22,0));
                 display:flex; flex-direction:column; gap:var(--s-2); }
    .card .p-title { color:var(--paper); }
    .card .p-body { color:rgba(247,245,240,.8); }
    .card .kicker { color:rgba(247,245,240,.65); }
""", body=(
    chband_body("08-humectant")
    + pi("a", "I12-hydration.jpg", style="filter:blur(3px) brightness(.55)")
    + """    <div class="stage"></div>
    <p class="s8-h" id="s8-h">Here is where ectoin stops behaving like a
      <em>normal moisturiser.</em></p>
    <div class="g2">
      <div class="card" id="c-hum" style="opacity:0">
        <img id="ci-hum" src="assets/plates/I23-glycerin.jpg" alt="">
        <div class="cap">
          <p class="kicker">A familiar humectant</p>
          <p class="p-title">Glycerin. Hyaluronic acid.</p>
          <p class="p-body">Attracts water and holds onto it.</p>
        </div>
      </div>
      <div class="card" id="c-ect" style="opacity:0">
        <img id="ci-ect" src="assets/plates/I24-membrane.jpg" alt="">
        <div class="cap">
          <p class="kicker">Ectoin</p>
          <p class="p-title">Works on how water arranges itself.</p>
          <p class="p-body">Around proteins and membranes.</p>
        </div>
      </div>
    </div>
"""
    + CV
), tl=kb('#pi-a', 0, 14.6, 1.0, 1.08) + """
  tl.fromTo('#s8-h', { opacity:0, y:30 }, { opacity:1, y:0, duration:0.55 }, @first);
  tl.to('#s8-h', { opacity:0, y:-20, duration:0.35 }, @w(humectant)-0.55);
  tl.fromTo('#c-hum', { opacity:0, x:-80 }, { opacity:1, x:0, duration:0.55 }, @w(humectant)-0.25);
""" + kb('#ci-hum', '@w(humectant)-0.25', 10.6, 1.0, 1.12) + cv_in('@w(humectant)') + """
  tl.fromTo('#c-ect', { opacity:0, x:80 }, { opacity:1, x:0, duration:0.55 }, @w(Ectoin,2)-0.20);
""" + kb('#ci-ect', '@w(Ectoin,2)-0.20', 5.6, 1.0, 1.12) + """
  tl.to('#c-hum', { opacity:0.45, duration:0.6 }, @w(Ectoin,2)+0.2);
""" + CHBAND_TL)

# ---------------------------------------------------------------- 09 exclusion
S09 = dict(css=PLATE_CSS + """
    #root { background:var(--paper); }
    .world.ink { background:var(--ink); color:var(--paper); clip-path:inset(0% 0% 0% 100%); z-index:5; }
    .world.paper { z-index:2; }
    .g9 { display:grid; grid-template-columns:44fr 56fr; gap:var(--s-8);
          align-items:center; height:100%; }
    .g9 .stage { padding:var(--safe-top) var(--safe-right) var(--safe-bottom) var(--safe-left); }
    .world.paper .col { color:var(--paper); }
    .world.paper .kicker { color:rgba(247,245,240,.7); }
    .world.paper .p-body { color:rgba(247,245,240,.82); }
""", body=(
    pv("a", "V08-hydration.mp4", 0.0, 11.0)
    + scrim("l")
    + """    <div class="world paper" id="w-paper">
      <div class="stage"><div class="g9">
        <div class="col">
          <p class="kicker">The mechanism</p>
          <p class="hero" id="e-term">Preferential<br>exclusion</p>
          <p class="p-body" id="e-sub" style="margin-top:20px">The tidy version: ectoin
            stays off the protein&rsquo;s surface, and the water around it stays organised.</p>
        </div>
        <div></div>
      </div></div>
    </div>
"""
    + CV
    + """    <div class="world ink" id="w-ink">
      <div class="stage"><div class="g9">
        <div class="col">
          <p class="kicker on-ink">The mechanism</p>
          <p class="hero" id="m-h">The honest version<br>is <em style="font-style:normal;color:var(--coral)">messier.</em></p>
          <p class="p-body on-ink" id="m-note" style="margin-top:20px">In the simulations,
            ectoin also showed some attraction to that surface. And how far it stays back
            depends on how tightly the protein&rsquo;s own water is already arranged.</p>
          <div style="margin-top:24px"><span class="cite on-ink">J Phys Chem B &middot; 2007</span></div>
        </div>
        <svg viewBox="0 0 620 620" width="100%" height="100%" aria-hidden="true">
          <circle cx="310" cy="310" r="190" fill="none" stroke="#59B8AE"
                  stroke-width="46" opacity="0.30"/>
          <circle cx="310" cy="310" r="112" fill="#F7F5F0"/>
          <g id="m-ring"></g>
          <text x="310" y="322" text-anchor="middle" fill="#131516"
                font-family="Inter, sans-serif" font-weight="800" font-size="34">PROTEIN</text>
        </svg>
      </div></div>
    </div>
"""
), tl=kb('#pv-a', 0, 11.0, 1.0, 1.08) + cv_in(0.3) + """
  // ---- tidy version, over the hydration-layer plate (ectoin hovering OFF the
  // protein; never drawn attached). ----
  tl.fromTo('#e-term', { opacity:0, y:40 }, { opacity:1, y:0, duration:0.55 }, 0.15);
  tl.fromTo('#e-sub', { opacity:0 }, { opacity:1, duration:0.45 }, @w(version)-0.30);

  // ---- ground inversion on "the honest version" -- kept as authored: the
  // diagram is the only honest way to draw "some attraction". ----
  var inv = @w(honest)-0.45;
  tl.fromTo('#w-ink', { clipPath:'inset(0% 0% 0% 100%)' },
                      { clipPath:'inset(0% 0% 0% 0%)', duration:0.60,
                        ease:'power3.inOut' }, inv);
  tl.fromTo('#m-ring', { rotation:0, transformOrigin:'310px 310px' },
                       { rotation:6, transformOrigin:'310px 310px', duration:1.40,
                         ease:'power2.out' }, inv);
  tl.fromTo('#m-h', { y:24, opacity:0.4 }, { y:0, opacity:1, duration:0.60,
                                             ease:'power2.out' }, inv);
  tl.to('#cv', { opacity:0, duration:0.2 }, inv);
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
    if (j % 3 === 0) {
      tl.to('#y-' + j, { x:-Math.cos(aj)*140, y:-Math.sin(aj)*140, fill:'#E0A32B',
                         duration:1.4, ease:'power2.inOut' }, @w(attraction)-0.8);
    }
  }
  tl.to('#m-ring', { rotation:14, transformOrigin:'310px 310px', duration:2.60,
                     ease:'power1.inOut' }, @w(depends));
  tl.to('#m-note', { opacity:0.75, duration:0.60 }, @w(arranged));
""")

# ---------------------------------------------------------------- 12 load (chapter)
S12 = dict(css=PLATE_CSS + CHBAND_CSS + """
    .l-h { position:absolute; left:var(--safe-left); top:calc(var(--safe-top) + 150px);
           z-index:4; margin:0; max-width:1100px; font-family:var(--font-display);
           font-size:var(--t-figure); line-height:var(--lh-snug);
           text-shadow:0 2px 20px rgba(0,0,0,.45); }
    .stressors { position:absolute; left:var(--safe-left); right:var(--safe-right);
                 bottom:var(--safe-bottom); z-index:4; display:grid;
                 grid-template-columns:repeat(5,1fr); gap:var(--s-4); }
    .st { background:rgba(19,21,22,.82); color:var(--paper); border-radius:var(--r-3);
          padding:var(--s-5) var(--s-4); text-align:center;
          font-family:var(--font-body); font-weight:800; font-size:var(--t-body); }
    .l-note { position:absolute; left:var(--safe-left); bottom:var(--safe-bottom);
              z-index:4; margin:0; max-width:1000px; background:rgba(19,21,22,.72);
              border-radius:var(--r-3); padding:var(--s-5) var(--s-6);
              font-family:var(--font-display); font-size:var(--t-figure);
              line-height:var(--lh-snug); }
    .l-note b { font-weight:400; color:var(--coral); }
""", body=(
    chband_body("12-load")
    + pi("a", "I16-barrier-calm.jpg")
    + pv("b", "V10-escape.mp4", 6.1, 7.5)
    + scrim("b")
    + """    <div class="stage"></div>
    <p class="l-h" id="l-h">Your outer barrier is under constant load.</p>
    <div class="stressors" id="l-st">
      <div class="st" id="st-0">Dry air</div>
      <div class="st" id="st-1">Cleansing</div>
      <div class="st" id="st-2">Pollution</div>
      <div class="st" id="st-3">Sun</div>
      <div class="st" id="st-4">Strong actives</div>
    </div>
    <p class="l-note" id="l-note" style="opacity:0">Water <b>escapes</b> more easily. Skin can feel
      <b id="l-w1">tight</b>, <b id="l-w2">rough</b>, or <b id="l-w3">unusually reactive</b>.</p>
"""
    + CV
), tl=kb('#pi-a', 0, 6.4, 1.0, 1.10, 0, 0, 0, -30) + cv_in(2.2) + """
  tl.fromTo('#l-h', { opacity:0, y:34 }, { opacity:1, y:0, duration:0.50 }, @first);
  tl.fromTo('#st-0', { opacity:0, y:60 }, { opacity:1, y:0, duration:0.40 }, @w(dry)-0.15);
  tl.fromTo('#st-1', { opacity:0, y:60 }, { opacity:1, y:0, duration:0.40 }, @w(cleansing)-0.15);
  tl.fromTo('#st-2', { opacity:0, y:60 }, { opacity:1, y:0, duration:0.40 }, @w(pollution)-0.15);
  tl.fromTo('#st-3', { opacity:0, y:60 }, { opacity:1, y:0, duration:0.40 }, @w(sun)-0.15);
  tl.fromTo('#st-4', { opacity:0, y:60 }, { opacity:1, y:0, duration:0.40 }, @w(strong)-0.15);
  // "When it struggles": cut to the stressed barrier -- water visibly escaping.
  tl.to('#l-h', { opacity:0, duration:0.3 }, @w(struggles)-0.3);
  tl.to('#l-st', { opacity:0, y:30, duration:0.35 }, @w(struggles)-0.3);
  tl.fromTo('#pl-b', { opacity:0 }, { opacity:1, duration:0.30 }, @w(struggles)-0.25);
""" + kb('#pv-b', 6.1, 7.4, 1.0, 1.08) + """
  tl.fromTo('#l-note', { opacity:0, y:30 }, { opacity:1, y:0, duration:0.5 }, @w(escapes)-0.3);
  tl.set(['#l-w1','#l-w2','#l-w3'], { color:'#F7F5F0' }, 0);
  tl.to('#l-w1', { color:'#C97A5C', duration:0.25 }, @w(tight));
  tl.to('#l-w2', { color:'#C97A5C', duration:0.25 }, @w(rough));
  tl.to('#l-w3', { color:'#C97A5C', duration:0.25 }, @w(unusually));
""" + CHBAND_TL)

# ---------------------------------------------------------------- 13 keratin
S13 = dict(css=PLATE_CSS + """
    .g13 { display:grid; grid-template-columns:50fr 50fr; gap:var(--s-8);
           align-items:center; height:100%; }
    .g13 .kicker { color:rgba(247,245,240,.7); }
    .g13 .p-body { color:rgba(247,245,240,.82); }
    .g13 .fig em { font-style:normal; color:var(--aqua); }
""", body=(
    pv("a", "V11-stabilise.mp4", 0.0, 17.4)
    + scrim("l")
    + """    <div class="stage">
      <div class="g13">
        <div class="col">
          <p class="kicker">What the lab work shows</p>
          <p class="fig" id="k-h0">Lab research suggests ectoin can help <em>stabilise</em>
            structures and improve hydration in that outer layer.</p>
          <p class="fig" id="k-h" style="opacity:0;margin-top:28px">One study found ectoin changed how
            <em>keratin</em> behaves with water.</p>
          <p class="p-body" id="k-s" style="margin-top:20px;opacity:0">Keratin is the main protein
            in our outer skin cells.</p>
          <div style="margin-top:28px"><span class="cite on-plate" id="k-cite" style="opacity:0">Biochem Biophys Rep &middot; 2021</span></div>
        </div>
        <div></div>
      </div>
    </div>
"""
    + CV
), tl=kb('#pv-a', 0, 17.4, 1.0, 1.09) + cv_in(0.3) + """
  tl.fromTo('#k-h0', { opacity:0, y:36 }, { opacity:1, y:0, duration:0.55 }, @w(suggests)-0.30);
  tl.to('#k-h0', { opacity:0.45, duration:0.5 }, @w(One)-0.2);
  tl.fromTo('#k-h', { opacity:0, y:36 }, { opacity:1, y:0, duration:0.55 }, @w(One)-0.10);
  tl.fromTo('#k-s', { opacity:0 }, { opacity:1, duration:0.45 }, @w(main)-0.20);
  tl.fromTo('#k-cite', { opacity:0 }, { opacity:1, duration:0.45 }, @w(behaves)-0.20);
""")

# ---------------------------------------------------------------- 23 numbers
S23 = dict(css=PLATE_CSS + """
    .g23 { display:flex; flex-direction:column; justify-content:center;
           gap:var(--s-5); height:100%; max-width:860px; }
    .g23 .hero { font-size:84px; text-shadow:0 2px 24px rgba(0,0,0,.45); }
    .g23 .fig { text-shadow:0 2px 20px rgba(0,0,0,.45); }
    .g23 .turn { color:var(--coral); }
    .brands { display:grid; grid-template-columns:1fr 1fr; gap:var(--s-5); }
    .bd { position:relative; background:rgba(19,21,22,.82); color:var(--paper);
          border-radius:var(--r-3); padding:var(--s-6); overflow:hidden; }
    .bd .pc { font-family:var(--font-display); font-size:100px; line-height:1;
              color:var(--aqua); }
    .bd .nm { font-family:var(--font-mono); font-size:var(--t-caption);
              letter-spacing:var(--tr-mono-wide); color:var(--ink-3-dark);
              margin-top:var(--s-3); }
""", body=(
    pi("a", "I18-bottle-front.jpg")
    + pv("b", "V12-turn.mp4", 3.6, 9.2)
    + scrim("l")
    + """    <div class="stage">
      <div class="g23">
        <p class="hero" id="nb-h">Do not buy it off the front of the bottle.</p>
        <p class="hero turn" id="nb-t" style="opacity:0">Turn it around.</p>
        <p class="fig" id="nb-s" style="opacity:0">Plenty of brands do print a number.</p>
        <div class="brands">
          <div class="bd" id="bd-0" style="opacity:0"><div class="wash moss" id="bw-0"></div>
            <div class="pc">7%</div><div class="nm">PAULA&rsquo;S CHOICE</div></div>
          <div class="bd" id="bd-1" style="opacity:0"><div class="wash moss" id="bw-1"></div>
            <div class="pc">2%</div><div class="nm">THE ORDINARY</div></div>
        </div>
      </div>
    </div>
"""
), tl="""
  // The bottle sits in the right half (plate shifted +300px) and turns on
  // "Turn it around" -- front label to ingredient list.
""" + kb('#pi-a', 0, 3.9, 1.12, 1.16, 300, 300) + """
  tl.fromTo('#pl-b', { opacity:0 }, { opacity:1, duration:0.30 }, 3.6);
""" + kb('#pv-b', 3.6, 9.2, 1.12, 1.06, 300, 300) + """
  tl.fromTo('#nb-h', { opacity:0, y:40 }, { opacity:1, y:0, duration:0.55 }, 0.15);
  tl.fromTo('#nb-t', { opacity:0, y:30 }, { opacity:1, y:0, duration:0.45 }, @w(Turn)-0.10);
  tl.fromTo('#nb-s', { opacity:0 }, { opacity:1, duration:0.45 }, @w(Plenty)-0.20);
  tl.fromTo('#bd-0', { opacity:0, x:-90 }, { opacity:1, x:0, duration:0.55 }, @w(Paula's));
  tl.fromTo('#bw-0', { scaleX:0 }, { scaleX:1, duration:0.60, ease:'power2.inOut' }, @w(Paula's)+0.50);
  tl.fromTo('#bd-1', { opacity:0, x:90 },  { opacity:1, x:0, duration:0.55 }, @w(ordinary));
  tl.fromTo('#bw-1', { scaleX:0 }, { scaleX:1, duration:0.60, ease:'power2.inOut' }, @w(ordinary)+0.50);
""")

# ---------------------------------------------------------------- 26 kbeauty (chapter)
S26 = dict(css=PLATE_CSS + CHBAND_CSS + """
    .g26 { position:absolute; left:var(--safe-left); bottom:var(--safe-bottom);
           z-index:4; display:flex; flex-direction:column; gap:var(--s-5); max-width:1120px; }
    .neg { position:relative; background:rgba(240,235,225,.92); color:var(--ink);
           border-radius:var(--r-3); padding:var(--s-6) var(--s-7); overflow:hidden; }
    .pos { position:relative; background:rgba(19,21,22,.86); color:var(--paper);
           border-radius:var(--r-3); padding:var(--s-6) var(--s-7); overflow:hidden; }
    .neg .hero, .pos .hero { font-size:var(--t-figure); margin-top:8px; }
""", body=(
    chband_body("26-kbeauty")
    + pv("a", "V13-serum.mp4", 0.0, 5.4)
    + pv("b", "V14-toner.mp4", 5.1, 5.0)
    + scrim("b")
    + """    <div class="stage"></div>
    <div class="g26">
      <div class="neg" id="kb-neg" style="opacity:0">
        <div class="void" id="kb-void"></div>
        <p class="kicker">The easy story</p>
        <p class="hero">K-beauty invented ectoin.</p>
      </div>
      <div class="pos" id="kb-pos" style="opacity:0">
        <div class="wash moss" id="kb-wash"></div>
        <p class="kicker on-ink">What is actually true</p>
        <p class="hero">Korean formulators pair it with barrier ingredients,
          in light wearable textures.</p>
      </div>
    </div>
"""
), tl=kb('#pv-a', 0, 5.4, 1.0, 1.08) + """
  tl.fromTo('#kb-neg', { opacity:0, x:-90 }, { opacity:1, x:0, duration:0.55 }, @first);
  tl.fromTo('#kb-void', { opacity:0 }, { opacity:0.85, duration:0.45 }, @w(not)-0.05);
  tl.fromTo('#kb-pos', { opacity:0, x:90 }, { opacity:1, x:0, duration:0.55 }, @w(Korean)-0.20);
  tl.fromTo('#kb-wash', { scaleX:0 }, { scaleX:1, duration:0.90, ease:'power2.inOut' }, @w(pairing)-0.20);
  tl.to('#kb-neg', { opacity:0.35, duration:0.70 }, @w(pairing)-0.20);
  // texture change on "light wearable textures"
  tl.fromTo('#pl-b', { opacity:0 }, { opacity:1, duration:0.35 }, 5.1);
""" + kb('#pv-b', 5.1, 5.0, 1.0, 1.08) + CHBAND_TL)

# ---------------------------------------------------------------- 27 resilience
S27 = dict(css=PLATE_CSS + """
    .shift { position:absolute; left:var(--safe-left); right:var(--safe-right);
             bottom:var(--safe-bottom); z-index:4; display:grid;
             grid-template-columns:1fr auto 1fr; gap:var(--s-6); align-items:center; }
    .sh { position:relative; border-radius:var(--r-3); padding:var(--s-6);
          text-align:center; overflow:hidden;
          font-family:var(--font-body); font-weight:800; font-size:var(--t-frame); }
    .sh.from { background:rgba(240,235,225,.90); color:var(--ink-2); }
    .sh.to { background:rgba(19,21,22,.86); color:var(--paper); }
    .arrow { font-family:var(--font-mono); font-size:var(--t-hero); color:var(--paper); }
    .where { position:absolute; left:var(--safe-left); right:var(--safe-right);
             top:var(--safe-top); bottom:var(--safe-bottom); z-index:4;
             display:grid; grid-template-columns:repeat(3,1fr); gap:var(--s-5);
             align-items:stretch; }
    .wh { position:relative; border-radius:var(--r-3); overflow:hidden; background:var(--ink-soft); }
    .wh img { position:absolute; left:0; top:0; width:100%; height:100%; object-fit:cover;
              transform-origin:50% 50%; }
    .wh .cap { position:absolute; left:0; right:0; bottom:0; padding:var(--s-5);
               background:linear-gradient(0deg, rgba(19,21,22,.9), rgba(19,21,22,0));
               font-family:var(--font-mono); font-size:var(--t-label); color:var(--paper);
               text-align:center; }
    .wh-h { position:absolute; left:var(--safe-left); top:calc(var(--safe-top) + 8px);
            z-index:5; margin:0; font-family:var(--font-display); font-size:var(--t-figure);
            text-shadow:0 2px 20px rgba(0,0,0,.5); }
    .wh-note { position:absolute; left:var(--safe-left); bottom:var(--safe-bottom);
               z-index:5; margin:0; background:rgba(19,21,22,.8); border-radius:var(--r-pill);
               padding:12px 26px; font-family:var(--font-mono); font-size:var(--t-caption);
               letter-spacing:var(--tr-mono-wide); text-transform:uppercase; }
""", body=(
    pv("a", "V15-sunscreen.mp4", 0.0, 8.0)
    + scrim("b", sid="sc-b")
    + '    <div class="scrim ink" id="sc-ink" style="opacity:0"></div>\n'
    + """    <div class="stage"></div>
    <div class="shift" id="shift">
      <div class="sh from" id="sh-a">Aggressive transformation</div>
      <div class="arrow" id="sh-ar">&rarr;</div>
      <div class="sh to" id="sh-b"><div class="wash moss" id="sh-w"></div><span>Skin that simply stays comfortable</span></div>
    </div>
    <p class="wh-h" id="wh-h" style="opacity:0">You will already find it in&hellip;</p>
    <div class="where" id="where">
      <div class="wh" id="wh-0" style="opacity:0"><img id="wi-0" src="assets/plates/C-serum.jpg" alt=""><div class="cap">Barrier serums</div></div>
      <div class="wh" id="wh-1" style="opacity:0"><img id="wi-1" src="assets/plates/C-tonerpad.jpg" alt=""><div class="cap">Toners</div></div>
      <div class="wh" id="wh-2" style="opacity:0"><img id="wi-2" src="assets/plates/I25-suntube.jpg" alt=""><div class="cap">Sun products</div></div>
    </div>
    <p class="wh-note" id="wh-note" style="opacity:0">Often in smaller type than the trend suggests</p>
"""
), tl=kb('#pv-a', 0, 8.0, 1.0, 1.08) + """
  tl.fromTo('#sh-a', { opacity:0, x:-70 }, { opacity:1, x:0, duration:0.50 }, 0.20);
  tl.fromTo('#sh-ar', { opacity:0 }, { opacity:1, duration:0.35 }, 1.10);
  tl.fromTo('#sh-b', { opacity:0, x:70 }, { opacity:1, x:0, duration:0.50 }, 1.45);
  tl.fromTo('#sh-w', { scaleX:0 }, { scaleX:1, duration:0.80, ease:'power2.inOut' }, @w(comfortable));
  tl.to('#sh-a', { opacity:0.40, duration:0.60 }, @w(comfortable));
  // "You will already find it in": the texture gives way to three product cards.
  tl.to('#shift', { opacity:0, y:30, duration:0.35 }, @w(find)-0.5);
  tl.to('#sc-ink', { opacity:1, duration:0.4 }, @w(find)-0.5);
  tl.fromTo('#wh-h', { opacity:0, y:-16 }, { opacity:1, y:0, duration:0.4 }, @w(find)-0.2);
  tl.fromTo('#wh-0', { opacity:0, y:52 }, { opacity:1, y:0, duration:0.45 }, @w(serums)-0.15);
  tl.fromTo('#wh-1', { opacity:0, y:52 }, { opacity:1, y:0, duration:0.45 }, @w(toners)-0.15);
  tl.fromTo('#wh-2', { opacity:0, y:52 }, { opacity:1, y:0, duration:0.45 }, @w(sun)-0.15);
""" + kb('#wi-0', '@w(serums)-0.15', 6.5, 1.0, 1.10) + kb('#wi-1', '@w(toners)-0.15', 5.8, 1.0, 1.10)
   + kb('#wi-2', '@w(sun)-0.15', 5.0, 1.0, 1.10) + """
  tl.fromTo('#wh-note', { opacity:0, y:20 }, { opacity:1, y:0, duration:0.4 }, @w(smaller)-0.15);
""")

# ---------------------------------------------------------------- 28 remember (arrive)
S28 = dict(css=PLATE_CSS + """
    #root { background:var(--ink); }
    .mont img { position:absolute; left:0; top:0; width:1920px; height:1080px;
                object-fit:cover; opacity:0; transform-origin:50% 50%; }
    .rm-h { position:absolute; left:var(--safe-left); bottom:var(--safe-bottom);
            z-index:4; margin:0; max-width:1100px; font-family:var(--font-display);
            font-size:var(--t-hero); line-height:var(--lh-tight); letter-spacing:var(--tr-display);
            text-shadow:0 2px 26px rgba(0,0,0,.5); }
    .rm-h em { font-style:normal; color:var(--aqua); }
    .rm-k { position:absolute; left:var(--safe-left); top:calc(var(--safe-top) + 8px);
            z-index:4; margin:0; }
    .nots { position:absolute; right:var(--safe-right); top:var(--safe-top);
            bottom:var(--safe-bottom); width:720px; z-index:4;
            display:flex; flex-direction:column; gap:var(--s-5); justify-content:center; }
    .nt { position:relative; background:rgba(33,31,27,.92); border-radius:var(--r-3);
          padding:var(--s-5) var(--s-6); overflow:hidden;
          font-family:var(--font-body); font-weight:800; font-size:var(--t-frame);
          color:var(--ink-2-dark); }
    .nt .x { position:absolute; inset:0; background:var(--coral); opacity:0; }
""", body=(
    '    <div class="plate mont" id="mont">\n'
    '      <img id="mo-0" src="assets/plates/I19-bottle-back.jpg" alt="">\n'
    '      <img id="mo-1" src="assets/plates/I01-saltlake.jpg" alt="">\n'
    '      <img id="mo-2" src="assets/plates/I03-bacterium.jpg" alt="">\n'
    '      <img id="mo-3" src="assets/plates/I12-hydration.jpg" alt="">\n'
    '      <img id="mo-4" src="assets/plates/I16-barrier-calm.jpg" alt="">\n'
    '      <img id="mo-5" src="assets/plates/I13-droplet-bottle.jpg" alt="">\n'
    '    </div>\n'
    + scrim("b", sid="sc-b")
    + '    <div class="scrim ink" id="sc-ink" style="opacity:0"></div>\n'
    + """    <div class="stage"></div>
    <p class="kicker on-ink rm-k" id="rm-k">What you are actually looking at</p>
    <p class="rm-h" id="rm-h" style="opacity:0">A survival strategy,<br>borrowed from
      <em>bacteria.</em></p>
    <div class="nots">
      <div class="nt" id="nt-0" style="opacity:0"><div class="x" id="nx-0"></div>The new hyaluronic acid</div>
      <div class="nt" id="nt-1" style="opacity:0"><div class="x" id="nx-1"></div>A miracle</div>
      <div class="nt" id="nt-2" style="opacity:0"><div class="wash moss" id="nx-2"></div><span>A genuinely interesting supporting molecule</span></div>
    </div>
"""
), tl="""
  // Callback montage on "remember what you are looking at / a survival
  // strategy borrowed from bacteria": ingredient list -> salt lake ->
  // bacterium -> hydration shell -> skin barrier -> serum droplet.
  var cuts = [0, @w(remember)-0.1, @w(looking)+0.25, @w(survival)+0.25, @w(borrowed)+0.15, @w(bacteria)-0.05];
  for (var i = 0; i < 6; i++) {
    tl.set('#mo-' + i, { opacity:(i === 0 ? 1 : 0) }, 0);
    if (i > 0) tl.to('#mo-' + i, { opacity:1, duration:0.12 }, cuts[i]);
    tl.fromTo('#mo-' + i, { scale:1.0 }, { scale:1.09, duration:3.2, ease:'none' }, cuts[i]);
  }
  tl.fromTo('#rm-h', { opacity:0, y:44 }, { opacity:1, y:0, duration:0.60 }, @w(survival));
  // The negations land on a dimmed ground so the cards read; the last cut
  // (serum droplet) stays under them.
  tl.to('#sc-ink', { opacity:0.72, duration:0.5 }, @w(not,1)-0.35);
  for (var k = 0; k < 3; k++)
    tl.fromTo('#nt-' + k, { opacity:0, x:70 }, { opacity:0.55, x:0, duration:0.45 }, @w(not,1)-0.35+k*0.25);
  tl.fromTo('#nx-0', { opacity:0 }, { opacity:0.85, duration:0.38 }, @w(not,1));
  tl.to('#nt-0', { opacity:1, duration:0.30 }, "<");
  tl.fromTo('#nx-1', { opacity:0 }, { opacity:0.85, duration:0.38 }, @w(Not,2));
  tl.to('#nt-1', { opacity:1, duration:0.30 }, "<");
  tl.fromTo('#nx-2', { scaleX:0 }, { scaleX:1, duration:0.75, ease:'power2.inOut' }, @w(genuinely));
  tl.to('#nt-2', { opacity:1, duration:0.30 }, "<");
""")


# ---------------------------------------------------------------- 22 whofor (chapter)
S22 = dict(css=PLATE_CSS + CHBAND_CSS + """
    .g22 { position:absolute; left:var(--safe-left); right:var(--safe-right);
           bottom:var(--safe-bottom); z-index:4; display:flex; flex-direction:column;
           gap:var(--s-5); }
    .wf-h { margin:0; font-family:var(--font-display); font-size:var(--t-figure);
            text-shadow:0 2px 20px rgba(0,0,0,.5); }
    .states { display:grid; grid-template-columns:repeat(4,1fr); gap:var(--s-4); }
    .stt { position:relative; background:rgba(19,21,22,.80); border-radius:var(--r-3);
           padding:var(--s-5) var(--s-4); text-align:center; overflow:hidden;
           font-family:var(--font-body); font-weight:800; font-size:var(--t-frame);
           min-height:130px; display:flex; align-items:center; justify-content:center; }
    .friends { display:grid; grid-template-columns:repeat(4,1fr); gap:var(--s-4); }
    .fr { background:rgba(247,245,240,.92); color:var(--ink); border-radius:var(--r-pill);
          padding:var(--s-4) var(--s-3); text-align:center;
          font-family:var(--font-mono); font-size:var(--t-label); }
""", body=(
    chband_body("22-whofor")
    + pi("a", "C-baseskin.jpg")
    + pi("b", "C-layering.jpg", wrap_style="opacity:0")
    + scrim("b")
    + """    <div class="stage"></div>
    <div class="g22">
      <p class="wf-h" id="wf-h">Most interesting if your skin runs&hellip;</p>
      <div class="states">
        <div class="stt" id="ss-0" style="opacity:0"><div class="wash aqua" id="sw-0"></div><span>Dry</span></div>
        <div class="stt" id="ss-1" style="opacity:0"><div class="wash aqua" id="sw-1"></div><span>Sensitive</span></div>
        <div class="stt" id="ss-2" style="opacity:0"><div class="wash aqua" id="sw-2"></div><span>Over-cleansed</span></div>
        <div class="stt" id="ss-3" style="opacity:0"><div class="wash aqua" id="sw-3"></div><span>Irritated</span></div>
      </div>
      <p class="wf-h" id="wf-s" style="opacity:0;font-size:var(--t-body)">It sits comfortably alongside&hellip;</p>
      <div class="friends">
        <div class="fr" id="fr-0" style="opacity:0">Panthenol</div><div class="fr" id="fr-1" style="opacity:0">Glycerin</div>
        <div class="fr" id="fr-2" style="opacity:0">Squalane</div><div class="fr" id="fr-3" style="opacity:0">Ceramides</div>
      </div>
    </div>
"""
), tl=kb('#pi-a', 0, 7.0, 1.0, 1.10, 0, 0, 0, -30) + """
  tl.fromTo('#wf-h', { opacity:0, y:34 }, { opacity:1, y:0, duration:0.50 }, @first);
  tl.fromTo('#ss-0', { opacity:0, y:56 }, { opacity:1, y:0, duration:0.42 }, @w(dry)-0.20);
  tl.fromTo('#ss-1', { opacity:0, y:56 }, { opacity:1, y:0, duration:0.42 }, @w(sensitive)-0.20);
  tl.fromTo('#ss-2', { opacity:0, y:56 }, { opacity:1, y:0, duration:0.42 }, @w(over)-0.20);
  tl.fromTo('#ss-3', { opacity:0, y:56 }, { opacity:1, y:0, duration:0.42 }, @w(irritated)-0.20);
  for (var i = 0; i < 4; i++)
    tl.fromTo('#sw-' + i, { scaleX:0 }, { scaleX:1, duration:0.55, ease:'power2.inOut' }, @w(strong)-0.3 + i*0.18);
  // "It sits comfortably alongside": cut to product layered on skin.
  tl.fromTo('#pl-b', { opacity:0 }, { opacity:1, duration:0.35 }, @w(sits)-0.30);
""" + kb('#pi-b', '@w(sits)-0.30', 5.6, 1.0, 1.10) + """
  tl.to('.states', { opacity:0, y:20, duration:0.35 }, @w(sits)-0.30);
  tl.to('#wf-h', { opacity:0, duration:0.3 }, @w(sits)-0.30);
  tl.fromTo('#wf-s', { opacity:0 }, { opacity:1, duration:0.45 }, @w(sits)-0.10);
  tl.fromTo('#fr-0', { opacity:0, y:34 }, { opacity:1, y:0, duration:0.40 }, @w(panthenol)-0.15);
  tl.fromTo('#fr-1', { opacity:0, y:34 }, { opacity:1, y:0, duration:0.40 }, @w(glycerin)-0.15);
  tl.fromTo('#fr-2', { opacity:0, y:34 }, { opacity:1, y:0, duration:0.40 }, @w(squalane)-0.15);
  tl.fromTo('#fr-3', { opacity:0, y:34 }, { opacity:1, y:0, duration:0.40 }, @w(ceramides)-0.15);
""" + CHBAND_TL)

# ---------------------------------------------------------------- 25 formula (UNSOURCED)
S25 = dict(css=PLATE_CSS + """
    .g25 { position:absolute; left:var(--safe-left); right:var(--safe-right);
           bottom:var(--safe-bottom); z-index:4; display:flex; flex-direction:column;
           gap:var(--s-5); }
    .uns { width:max-content; font-family:var(--font-mono); font-size:var(--t-caption);
           letter-spacing:var(--tr-mono-wide); text-transform:uppercase;
           color:rgba(247,245,240,.85); background:rgba(19,21,22,.6);
           border:1.5px solid rgba(247,245,240,.35); border-radius:var(--r-pill);
           padding:8px 18px; margin:0; }
    .f-h { margin:0; font-family:var(--font-display); font-size:var(--t-figure);
           text-shadow:0 2px 20px rgba(0,0,0,.5); }
    .qs { display:grid; grid-template-columns:repeat(3,1fr); gap:var(--s-4); }
    .q { position:relative; background:rgba(19,21,22,.80); border-radius:var(--r-3);
         padding:var(--s-5) var(--s-6); overflow:hidden; min-height:170px;
         font-family:var(--font-display); font-size:var(--t-body);
         line-height:var(--lh-snug); display:flex; align-items:center; }
    .q.last { font-family:var(--font-body); font-weight:800; }
""", body=(
    pi("a", "C-flatlay.jpg")
    + scrim("b")
    + """    <div class="stage"></div>
    <div class="g25">
      <p class="uns" id="f-uns">Judgement &middot; no source record</p>
      <p class="f-h" id="f-h">The rest is judgement, not evidence.</p>
      <div class="qs">
        <div class="q" id="q-0" style="opacity:0"><span>Fragrance-free, if fragrance bothers you?</span></div>
        <div class="q" id="q-1" style="opacity:0"><span>Does the formula carry other useful moisturisers?</span></div>
        <div class="q last" id="q-2" style="opacity:0"><div class="wash coral" id="q-w"></div><span>One good ingredient cannot rescue a badly built product.</span></div>
      </div>
    </div>
"""
), tl=kb('#pi-a', 0, 13.6, 1.0, 1.12, 0, -30, 0, 20) + """
  tl.fromTo('#f-uns', { opacity:0 }, { opacity:1, duration:0.3 }, 0.2);
  tl.fromTo('#f-h', { opacity:0, y:30 }, { opacity:1, y:0, duration:0.5 }, @w(judgment)-0.35);
  tl.fromTo('#q-0', { opacity:0, y:50 }, { opacity:1, y:0, duration:0.45 }, @w(fragrance)-0.25);
  tl.fromTo('#q-1', { opacity:0, y:50 }, { opacity:1, y:0, duration:0.45 }, @w(formula)-0.35);
  tl.fromTo('#q-2', { opacity:0, y:50 }, { opacity:1, y:0, duration:0.45 }, @w(One)-0.25);
  tl.fromTo('#q-w', { scaleX:0 }, { scaleX:1, duration:0.7, ease:'power2.inOut' }, @w(rescue)-0.1);
""")

# ---------------------------------------------------------------- wrappers
GROUND_CSS = PLATE_CSS + """
    .ground { position:absolute; inset:0; overflow:hidden; z-index:0; }
    .ground img { position:absolute; left:0; top:0; width:1920px; height:1080px;
                  object-fit:cover; transform-origin:50% 50%; }
"""


def with_ground(spec, src, opacity=0.14, dur=12.0, blur=8, extra_css=""):
    """Editorial scene, kept as authored, over a slowly drifting, blurred,
    low-opacity photographic ground -- parallax without moving the text
    (which would put ink in the safe margins)."""
    body = (f'    <div class="ground" id="gnd"><img id="gi" src="assets/plates/{src}" alt="" '
            f'style="opacity:{opacity}; filter:blur({blur}px) saturate(.6)"></div>\n'
            + spec["body"])
    css = spec["css"] + GROUND_CSS + extra_css + """
    #root { color:inherit; }
    """
    tl = spec["tl"] + kb('#gi', 0, dur, 1.08, 1.0, 40, -40)
    return dict(css=css, body=body, tl=tl)


def with_plate_img(spec, src, scrim_kind="ink", dur=12.0, s0=1.0, s1=1.08, extra_css=""):
    """Existing scene body over a full-bleed still + scrim. Text colours are
    the scene's own ink-ground tokens, so only ink-ground scenes use this."""
    body = pi("g", src) + scrim(scrim_kind) + spec["body"]
    css = spec["css"] + PLATE_CSS + extra_css + "\n    #root { color:inherit; }\n"
    tl = spec["tl"] + kb('#pi-g', 0, dur, s0, s1)
    return dict(css=css, body=body, tl=tl)


def apply(defs):
    """Return a new FRAME_DEFS with the retention overrides applied."""
    out = dict(defs)
    out.update({
        "01-hook": S01, "02-osmosis": S02, "03-now": S03, "05-halomonas": S05,
        "06-mechanism": S06, "07-question": S07, "08-humectant": S08,
        "09-exclusion": S09, "12-load": S12, "13-keratin": S13, "23-numbers": S23,
        "26-kbeauty": S26, "27-resilience": S27, "28-remember": S28,
        "22-whofor": S22, "25-formula": S25,
    })
    # ink-ground editorial scenes: a dimmed plate + scrim behind the authored copy
    out["04-extremolyte"] = with_plate_img(defs["04-extremolyte"], "I14-pinkpond.jpg", "ink", 9.9, 1.10, 1.0)
    out["14-notforce"] = with_plate_img(defs["14-notforce"], "I02-droplet.jpg", "ink", 10.6, 1.0, 1.08)
    out["24-eleven"] = with_plate_img(defs["24-eleven"], "I19-bottle-back.jpg", "ink", 15.1, 1.06, 1.0)
    # paper-ground editorial scenes: a faint drifting ground
    for cid, src, d in [("11-analogy", "I12-hydration.jpg", 14.6), ("15-framing", "I16-barrier-calm.jpg", 8.7),
                        ("16-trial104", "C-baseskin.jpg", 12.7), ("17-preference", "C-baseskin.jpg", 12.1),
                        ("18-eczema", "C-flaking.jpg", 15.7), ("19-limits", "I14-pinkpond.jpg", 7.8),
                        ("20-twelve", "I15-colony.jpg", 9.1), ("21-verdict", "I14-pinkpond.jpg", 9.7),
                        ]:
        out[cid] = with_ground(defs[cid], src, 0.12, d)
    return out
