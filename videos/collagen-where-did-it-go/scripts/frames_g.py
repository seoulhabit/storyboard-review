#!/usr/bin/env python3
"""File G -- 16-end: the calm end card. Right third and lower-right kept
clear for YouTube's end-screen elements; one slow drift is the only motion."""
from actors import EASE_JS
from motion import MOTION


def file_16_end(fspan, fctx):
    css = """
    .endcard { position:absolute; inset:0; display:flex; flex-direction:column;
               justify-content:center; gap:var(--s-4);
               padding-right:calc(var(--endscreen-right) - var(--s-6));
               padding-bottom:calc(var(--endscreen-bottom) - var(--s-6)); }
    .ec-kicker { font-family:var(--font-mono); font-size:var(--t-label);
                 letter-spacing:var(--tr-mono-wide); text-transform:uppercase;
                 color:var(--ink-2); margin:0; }
    .ec-do { font-family:var(--font-display); font-size:var(--t-hero); line-height:var(--lh-tight);
             letter-spacing:var(--tr-display); color:var(--ink); margin:0; }
    .ec-sub { font-family:var(--font-body); font-weight:800; font-size:var(--t-body);
              color:var(--ink-2); margin:0; }
    .ec-rule { height:6px; width:520px; background:var(--coral); }
"""
    body = """
      <div class="stage">
       <div class="world" id="world">
        <div class="endcard" id="endcard">
          <p class="ec-kicker">SeoulHabit</p>
          <p class="ec-do" id="end-line">Evidence, not hype.</p>
          <div class="ec-rule"></div>
          <p class="ec-sub">Sources in the description.</p>
        </div>
       </div>
      </div>
"""
    tl = EASE_JS + """
    // motion calmed: one slow drift across the whole hold, large enough that
    // the 2fps static gate still sees a change, small enough to read as calm
    tl.fromTo("#endcard", { y:36 }, { y:0, duration:@fown, ease:"power1.out" }, 0);
"""
    MOTION["16-end"]["beats"] = []
    return body, css, tl


FILES = {"16-end": file_16_end}
