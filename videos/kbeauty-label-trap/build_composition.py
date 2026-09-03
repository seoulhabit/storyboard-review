#!/usr/bin/env python3
"""Project-local composition builder for kbeauty-label-trap.

Emits compositions/frames/*.html from hand-authored per-scene content below,
using shared CSS tokens + the video's one signature device (the vermilion
ink-stamp). index.html itself is generated separately by the mechanical
transition-formula script (already run) and is NOT touched here.

Each scene function returns (style_extra, body_html, script_js). The wrapper
below assembles the full <template> file with the shared token/safe-area/
type-floor CSS every scene needs, per [S6/A-5]/[S6/A-6]/[S6/A-7].
"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
BS = json.load(open(os.path.join(ROOT, "03-beat-sheet.json")))
SCENES = {s["id"]: s for s in BS["scenes"]}
OUTDIR = os.path.join(ROOT, "05-composition", "compositions", "frames")

SHARED_CSS = """
  *, *::before, *::after { box-sizing: border-box; }
  #root {
    --safe-top:54px; --safe-bottom:108px; --safe-left:96px; --safe-right:96px;
    --paper:#F7F5F0; --ink:#131516; --ink-soft:#211F1B; --mist:#F0EBE1;
    --celadon:#93B896; --moss:#4F6B52; --coral:#C97A5C; --vermilion:#E34234;
    --ink-2:#6B6B6B; --ink-3:#9C978D; --rule-strong:#D9D3C6; --rule-dark:#333333;
    --font-display:"EB Garamond",Georgia,"Times New Roman",serif;
    --font-body:"Inter",system-ui,-apple-system,Helvetica,Arial,sans-serif;
    --font-mono:"JetBrains Mono",ui-monospace,"SF Mono",Consolas,monospace;
    position:relative; width:1920px; height:1080px; overflow:hidden;
    font-family:var(--font-body);
  }
  .clip { position:absolute; inset:0; }
  .stage { padding: calc(var(--safe-top) + 40px) calc(var(--safe-right) + 40px)
                    calc(var(--safe-bottom) + 40px) calc(var(--safe-left) + 40px);
           height:100%; }
  /* Type floors [S6/A-6]: hero 96-160, body 40 min, labels 32 absolute floor. */
  .head  { font-family:var(--font-display); font-weight:600; font-size:104px;
           line-height:1.06; letter-spacing:-.016em; margin:0; }
  .head-lg { font-family:var(--font-display); font-weight:600; font-size:132px;
           line-height:1.02; letter-spacing:-.018em; margin:0; }
  .sub   { font-weight:700; font-size:46px; letter-spacing:.09em; text-transform:uppercase; }
  .body  { font-weight:600; font-size:52px; line-height:1.28; }
  .kicker{ font-weight:700; font-size:36px; letter-spacing:.16em; text-transform:uppercase; }
  .label { font-family:var(--font-mono); font-weight:500; font-size:34px; letter-spacing:.03em; }
  .cite  { font-family:var(--font-mono); font-weight:500; font-size:32px; letter-spacing:.04em;
           border:2px solid var(--rule-strong); border-radius:999px; padding:10px 26px;
           width:max-content; display:inline-block; }
  .uf-badge { display:inline-flex; align-items:center; gap:10px; font-weight:600; font-size:32px;
           border:1px solid rgba(19,21,22,0.28); border-radius:999px; padding:12px 28px;
           background:rgba(19,21,22,0.05); width:max-content; }
  .illus-tag { font-family:var(--font-mono); font-weight:500; font-size:28px; letter-spacing:.03em;
           color:var(--ink-3); font-style:italic; }
  #root.debug-layout * { outline:1px solid rgba(255,0,0,.6) !important; }
"""

def stamp_svg(uid, glyph, size=180, ring=None, rotate=-6, filled=False):
    """The one signature device: a double-ring ink stamp. Reused, reskinned,
    for the passport ID mark, all five evidence seals, and the end-card
    passport-lock -- never redrawn as a different idiom per [S6/A-9]."""
    ring = ring or "var(--vermilion)"
    r_outer = size/2 - 6
    r_inner = size/2 - 22
    fill = f'fill="{ring}" fill-opacity="0.08"' if filled else 'fill="none"'
    return f'''<svg class="stamp" id="{uid}" viewBox="0 0 {size} {size}" width="{size}" height="{size}"
     style="overflow:visible" aria-hidden="true">
  <g transform="rotate({rotate} {size/2} {size/2})">
    <circle cx="{size/2}" cy="{size/2}" r="{r_outer}" stroke="{ring}" stroke-width="5" {fill}/>
    <circle cx="{size/2}" cy="{size/2}" r="{r_inner}" stroke="{ring}" stroke-width="2.5" fill="none"/>
    <text x="{size/2}" y="{size/2+9}" text-anchor="middle" font-family="var(--font-mono)"
          font-weight="700" font-size="{size*0.16:.0f}" fill="{ring}" letter-spacing="1">{glyph}</text>
  </g>
</svg>'''

def bottle_svg(uid, cx, top, height, width, liquid_kind, cap_color="#8A9498"):
    """A single glass serum bottle. liquid_kind: 'lattice' | 'water' | 'ambiguous'
    ('ambiguous' = the pre-reveal state, flat uniform fill, no distinguishing
    structure -- s01 uses this for BOTH bottles; s12 reuses this same function
    with 'lattice'/'water' to resolve the mystery, per [S6/A-9] reuse-not-rebuild)."""
    body_top = top + height*0.22
    body_h = height - height*0.22
    if liquid_kind == "ambiguous":
        fill = f'''<clipPath id="{uid}-clip"><rect x="{cx-width/2+6}" y="{body_top+6}" width="{width-12}" height="{body_h-12}" rx="{width*0.12}"/></clipPath>
        <g clip-path="url(#{uid}-clip)">
          <rect x="{cx-width/2}" y="{body_top}" width="{width}" height="{body_h}" fill="url(#{uid}-liquid)" opacity="0.55"/>
        </g>'''
    elif liquid_kind == "lattice":
        fill = f'''<clipPath id="{uid}-clip"><rect x="{cx-width/2+6}" y="{body_top+6}" width="{width-12}" height="{body_h-12}" rx="{width*0.12}"/></clipPath>
        <g clip-path="url(#{uid}-clip)">
          <rect x="{cx-width/2}" y="{body_top}" width="{width}" height="{body_h}" fill="url(#{uid}-liquid)"/>
          <g stroke="var(--celadon)" stroke-width="3" fill="none" opacity="0.85">
            <path d="M {cx-width*0.3} {body_top+body_h*0.85} L {cx-width*0.1} {body_top+body_h*0.55} L {cx+width*0.15} {body_top+body_h*0.7} L {cx+width*0.05} {body_top+body_h*0.3} L {cx+width*0.3} {body_top+body_h*0.2}"/>
            <path d="M {cx-width*0.1} {body_top+body_h*0.55} L {cx-width*0.25} {body_top+body_h*0.25}"/>
            <path d="M {cx+width*0.15} {body_top+body_h*0.7} L {cx+width*0.3} {body_top+body_h*0.5}"/>
          </g>
          <g fill="var(--celadon)" opacity="0.9">
            <circle cx="{cx-width*0.3}" cy="{body_top+body_h*0.85}" r="5"/>
            <circle cx="{cx-width*0.1}" cy="{body_top+body_h*0.55}" r="6"/>
            <circle cx="{cx+width*0.15}" cy="{body_top+body_h*0.7}" r="5"/>
            <circle cx="{cx+width*0.05}" cy="{body_top+body_h*0.3}" r="6"/>
            <circle cx="{cx+width*0.3}" cy="{body_top+body_h*0.2}" r="5"/>
            <circle cx="{cx-width*0.25}" cy="{body_top+body_h*0.25}" r="4"/>
            <circle cx="{cx+width*0.3}" cy="{body_top+body_h*0.5}" r="4"/>
          </g>
        </g>'''
    else:
        fill = f'''<clipPath id="{uid}-clip"><rect x="{cx-width/2+6}" y="{body_top+6}" width="{width-12}" height="{body_h-12}" rx="{width*0.12}"/></clipPath>
        <g clip-path="url(#{uid}-clip)">
          <rect x="{cx-width/2}" y="{body_top+body_h*0.18}" width="{width}" height="{body_h*0.82}" fill="url(#{uid}-liquid)"/>
          <line x1="{cx-width/2}" y1="{body_top+body_h*0.18}" x2="{cx+width/2}" y2="{body_top+body_h*0.18}" stroke="var(--celadon)" stroke-width="2" opacity="0.5"/>
        </g>'''
    return f'''<svg class="bottle" id="{uid}" viewBox="0 0 {width+40} {height+20}" width="{width+40}" height="{height+20}"
     style="overflow:visible" aria-hidden="true">
  <defs>
    <linearGradient id="{uid}-glass" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#DDE6E4" stop-opacity="0.14"/>
      <stop offset="45%" stop-color="#EAF2F0" stop-opacity="0.35"/>
      <stop offset="55%" stop-color="#EAF2F0" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#DDE6E4" stop-opacity="0.14"/>
    </linearGradient>
    <linearGradient id="{uid}-liquid" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="var(--celadon)" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="var(--moss)" stop-opacity="0.7"/>
    </linearGradient>
  </defs>
  <rect x="{cx-width/2}" y="{body_top}" width="{width}" height="{body_h}" rx="{width*0.14}"
        fill="url(#{uid}-glass)" stroke="#C7D2CF" stroke-width="2.5" opacity="0.9"/>
  {fill}
  <rect x="{cx-width*0.16}" y="{top}" width="{width*0.32}" height="{height*0.22}" rx="6"
        fill="{cap_color}" stroke="#5C6568" stroke-width="2"/>
  <rect x="{cx-width*0.05}" y="{body_top+body_h*0.12}" width="{width*0.14}" height="{body_h*0.55}" rx="{width*0.06}"
        fill="#FFFFFF" opacity="0.18"/>
</svg>'''

def wrap(scene_id, style_extra, body_html, script_js, bg="paper"):
    sc = SCENES[scene_id]
    dur = sc["duration"]
    bg_color = "var(--ink)" if bg == "dark" else "var(--paper)"
    fg_color = "var(--paper)" if bg == "dark" else "var(--ink)"
    return f'''<template>
<style>
{SHARED_CSS}
  #root {{ background:{bg_color}; color:{fg_color}; }}
{style_extra}
</style>

<div id="root" data-composition-id="{scene_id}" data-width="1920" data-height="1080" data-duration="{dur:.3f}">
  <div class="clip stage" id="{scene_id}-stage" data-start="0" data-duration="{dur:.3f}">
{body_html}
  </div>
</div>
<script>
(function () {{
{script_js}
}})();
</script>
</template>
'''

def write(scene_id, style_extra, body_html, script_js, bg="paper"):
    html = wrap(scene_id, style_extra, body_html, script_js, bg)
    idx = list(SCENES.keys()).index(scene_id) + 1
    path = os.path.join(OUTDIR, f"{idx:02d}-{scene_id}.html")
    open(path, "w").write(html)
    print("wrote", path)
