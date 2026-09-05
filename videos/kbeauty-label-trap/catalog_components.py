#!/usr/bin/env python3
"""Reusable production helpers translating the Catalog V2 Label Literacy
system (catalog-v2/story-systems/label-literacy) into render-native
HyperFrames markup for kbeauty-label-trap.

Every function returns a plain HTML string (SVG or div markup) meant to be
embedded inside a scene's body_html, using CSS custom properties from
build_composition.SHARED_CSS (--paper, --ink, --celadon, --celadon-deep,
--assay, --aqua, --amber, --signal, --brand-coral, --font-*). Nothing here
owns timing -- callers gsap.set()/gsap.to() the ids these functions emit.
"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "05-composition", "assets")

# --------------------------------------------------------------- icons -----
_ICON_CACHE = {}

def _load_icon(name):
    """Read an icon/mark asset once and cache its (viewBox, inner-markup).
    Keeps 05-composition/assets/{icons,brand}/*.svg as the real, editable
    source of truth -- scenes inline the parsed content so GSAP can still
    target sub-ids and no runtime file fetch is needed during render."""
    if name in _ICON_CACHE:
        return _ICON_CACHE[name]
    path = (os.path.join(ASSETS, "brand", "seoulhabit-mark.svg") if name == "seoulhabit-mark"
            else os.path.join(ASSETS, "icons", f"{name}.svg"))
    raw = open(path, encoding="utf-8").read()
    m = re.search(r'<svg[^>]*viewBox="([^"]+)"[^>]*>(.*)</svg>', raw, re.S)
    view_box, inner = m.group(1), m.group(2).strip()
    _ICON_CACHE[name] = (view_box, inner)
    return _ICON_CACHE[name]

ICON_NAMES = ["ingredient-source", "quantity", "identity-version",
              "formula-vehicle", "evidence", "boundary", "reference"]

def icon_svg(uid, name, size=64, color="currentColor", opacity=1):
    """One semantic icon (see 05-composition/assets/icons/) sized for inline
    use. `color` sets the ring+glyph currentColor; each icon keeps exactly
    one fixed-palette accent baked into its file, per the icon-family rule."""
    view_box, inner = _load_icon(name)
    return (f'<svg class="icon icon-{name}" id="{uid}" viewBox="{view_box}" '
            f'width="{size}" height="{size}" style="overflow:visible;color:{color};opacity:{opacity}" '
            f'aria-hidden="true">{inner}</svg>')

def brand_mark_svg(uid, size=64):
    """The canonical SeoulHabit signet (coral disc + paper ring + 습), for
    brand touchpoints and the final landing ONLY -- never a per-scene
    watermark and never used to stand in for a semantic icon."""
    view_box, inner = _load_icon("seoulhabit-mark")
    return (f'<svg class="brand-mark" id="{uid}" viewBox="{view_box}" '
            f'width="{size}" height="{size}" style="overflow:visible" aria-hidden="true">{inner}</svg>')


# ------------------------------------------------------- ingredient actor --
def ingredient_actor_svg(uid, size=420):
    """The persistent Cica / Centella asiatica leaf actor. One recognizable
    shape reused across s01/s02/s06/s07/s08/s12/s13/s14 -- only its
    container, scale and surrounding state change, never its own geometry."""
    return f'''<svg class="ingredient-actor" id="{uid}" viewBox="0 0 200 200" width="{size}" height="{size}"
     style="overflow:visible" aria-hidden="true">
  <defs>
    <linearGradient id="{uid}-leaf" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#B7CDBD"/>
      <stop offset="100%" stop-color="#3F6B4E"/>
    </linearGradient>
  </defs>
  <path id="{uid}-body" d="M100 164C86 140 63 125 50 98C35 65 58 34 94 42C108 22 143 32 149 62
    C172 74 165 113 138 125C127 137 113 151 100 164Z"
    fill="url(#{uid}-leaf)" stroke="#426B50" stroke-width="2.6"/>
  <g fill="none" stroke="#F1F2ED" stroke-opacity=".85" stroke-width="1.8">
    <path d="M100 162V49M100 92L62 66M100 110L140 68M100 128L61 103M100 140L138 112"/>
  </g>
  <circle cx="100" cy="49" r="5" fill="#F1F2ED" stroke="#426B50" stroke-width="1.6"/>
</svg>'''


# ------------------------------------------------------ neutral packaging --
def neutral_package_shell_svg(uid, width=210, height=420, variant="a", liquid_state="ambiguous"):
    """A/B neutral product specimen -- same helper/geometry for s01 and s12,
    only `liquid_state` changes to resolve the mystery. variant 'a' reads as
    a rounder apothecary silhouette, 'b' a squarer clinical one; neither is
    ever styled as the hero. liquid_state: 'ambiguous' (pre-reveal, flat,
    both bottles identical) | 'plain' (sparse/thin fill -- fewer visible
    facts) | 'structured' (lattice detail -- more visible facts)."""
    cap_r = 8 if variant == "a" else 4
    body_r = width * 0.16 if variant == "a" else width * 0.07
    body_top = height * 0.22
    body_h = height - body_top
    cx = width / 2

    if liquid_state == "ambiguous":
        liquid = f'<rect x="{cx-width*0.42}" y="{body_top+8}" width="{width*0.84}" height="{body_h-16}" ' \
                 f'rx="{body_r*0.7}" fill="url(#{uid}-liq)" opacity="0.5"/>'
    elif liquid_state == "structured":
        liquid = f'''<rect x="{cx-width*0.42}" y="{body_top+8}" width="{width*0.84}" height="{body_h-16}"
          rx="{body_r*0.7}" fill="url(#{uid}-liq)"/>
        <g stroke="#7F9D88" stroke-width="2.4" fill="none" opacity="0.85">
          <path d="M {cx-width*0.28} {body_top+body_h*0.82} L {cx-width*0.08} {body_top+body_h*0.52}
                   L {cx+width*0.15} {body_top+body_h*0.66} L {cx+width*0.04} {body_top+body_h*0.28}
                   L {cx+width*0.30} {body_top+body_h*0.18}"/>
        </g>
        <g fill="#7F9D88">
          <circle cx="{cx-width*0.28}" cy="{body_top+body_h*0.82}" r="4.5"/>
          <circle cx="{cx-width*0.08}" cy="{body_top+body_h*0.52}" r="5.5"/>
          <circle cx="{cx+width*0.15}" cy="{body_top+body_h*0.66}" r="4.5"/>
          <circle cx="{cx+width*0.04}" cy="{body_top+body_h*0.28}" r="5.5"/>
          <circle cx="{cx+width*0.30}" cy="{body_top+body_h*0.18}" r="4.5"/>
        </g>'''
    else:  # 'plain'
        liquid = f'''<rect x="{cx-width*0.42}" y="{body_top+body_h*0.22}" width="{width*0.84}"
          height="{body_h*0.7}" rx="{body_r*0.5}" fill="url(#{uid}-liq)"/>
        <line x1="{cx-width*0.42}" y1="{body_top+body_h*0.22}" x2="{cx+width*0.42}" y2="{body_top+body_h*0.22}"
          stroke="#426B50" stroke-width="2" opacity="0.4"/>'''

    return f'''<svg class="package-shell package-{variant}" id="{uid}" viewBox="0 0 {width} {height}"
     width="{width}" height="{height}" style="overflow:visible" aria-hidden="true">
  <defs>
    <linearGradient id="{uid}-glass" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#F1F2ED" stop-opacity="0.12"/>
      <stop offset="46%" stop-color="#FFFFFF" stop-opacity="0.32"/>
      <stop offset="54%" stop-color="#FFFFFF" stop-opacity="0.32"/>
      <stop offset="100%" stop-color="#F1F2ED" stop-opacity="0.12"/>
    </linearGradient>
    <linearGradient id="{uid}-liq" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#7F9D88" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#426B50" stop-opacity="0.72"/>
    </linearGradient>
  </defs>
  <rect x="{cx-width*0.16}" y="0" width="{width*0.32}" height="{height*0.20}" rx="{cap_r}"
        fill="#8A9498" stroke="#5C6568" stroke-width="2"/>
  <rect x="{cx-width*0.46}" y="{body_top}" width="{width*0.92}" height="{body_h}" rx="{body_r}"
        fill="url(#{uid}-glass)" stroke="#C7D2CF" stroke-width="2.5" opacity="0.92"/>
  {liquid}
  <rect x="{cx-width*0.30}" y="{body_top+body_h*0.10}" width="{width*0.10}" height="{body_h*0.5}"
        rx="{width*0.05}" fill="#FFFFFF" opacity="0.16"/>
</svg>'''


# ------------------------------------------------------------- evidence ----
_STATE_COLOR = {
    "known": "#426B50", "not_disclosed": "#D95F52", "not_established": "#7D8791",
    "requires_context": "#6358A7", "unknown": "#D95F52", "illustrative": "#8A6738",
    "different": "#D95F52", "partial": "#C5944D", "matches": "#426B50",
}
_STATE_LABEL = {
    "known": "Known", "not_disclosed": "Not disclosed", "not_established": "Not established",
    "requires_context": "Context required", "unknown": "Unknown", "illustrative": "Illustrative",
    "different": "Different", "partial": "Partial match", "matches": "Matches",
}

def evidence_state_chip(uid, state, text=None, mono=True):
    """A field-state pill (known / not_disclosed / not_established /
    requires_context / unknown / illustrative) -- the same five-and-a-half
    states used everywhere a field's certainty needs to be shown, never a
    pass/fail badge."""
    color = _STATE_COLOR[state]
    label = text or _STATE_LABEL[state]
    font = "var(--font-mono)" if mono else "var(--font-body)"
    dash = "stroke-dasharray:3 4;" if state in ("unknown", "not_disclosed") else ""
    return (f'<span class="ev-chip" id="{uid}" style="display:inline-flex;align-items:center;gap:10px;'
            f'border:2px solid {color};border-radius:999px;padding:8px 22px;color:{color};'
            f'font-family:{font};font-weight:600;font-size:28px;letter-spacing:.02em;width:max-content;">'
            f'<svg width="12" height="12" style="flex:none"><circle cx="6" cy="6" r="5" fill="none" '
            f'stroke="{color}" stroke-width="1.6" style="{dash}"/></svg>{label}</span>')

def citation_chip(uid, text):
    """Plain mono citation pill -- regulatory or journal source, quietly
    weighted, never competing with the vermilion-successor seal system."""
    return (f'<div class="cite" id="{uid}">{text}</div>')

def illustrative_disclosure(uid, text="Authored, illustrative — not a claim."):
    """Small italic mono disclosure line -- the catalog's ll-disclosure role."""
    return f'<div class="illus-tag" id="{uid}">{text}</div>'


# --------------------------------------------------- five-question system --
QUESTIONS = [
    ("quantity", "How much?"),
    ("identity-version", "Which version?"),
    ("formula-vehicle", "What carries it?"),
    ("evidence", "What evidence?"),
    ("boundary", "Where does it stop?"),
]
_SEAL_STATE_COLOR = {
    "unseen": "#8B95A3", "active": "#6358A7", "answered": "#426B50", "unknown": "#D95F52",
}

def question_seal(uid, question_index, state="unseen", size=170, bg="paper"):
    """One seal in the five-question system: a ring + dashed inner keyline +
    the question's own semantic icon, colored by investigation state. This
    -- not a stamp motif -- is the video's persistent signature device."""
    icon_name = QUESTIONS[question_index][0]
    color = _SEAL_STATE_COLOR.get(state, _SEAL_STATE_COLOR["unseen"])
    disc_fill = "rgba(255,255,255,0.05)" if bg == "dark" else "rgba(255,255,255,0.55)"
    icon = icon_svg(f"{uid}-glyph", icon_name, size=size * 0.42, color=color)
    return f'''<div class="q-seal" id="{uid}" style="position:relative;width:{size}px;height:{size}px;flex:none;">
  <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" style="position:absolute;inset:0;overflow:visible">
    <circle id="{uid}-ring" cx="{size/2}" cy="{size/2}" r="{size/2-4}" fill="{disc_fill}" stroke="{color}" stroke-width="3"/>
    <circle id="{uid}-keyline" cx="{size/2}" cy="{size/2}" r="{size*0.37}" fill="none" stroke="{color}" stroke-width="1.5"
            stroke-dasharray="3 5" opacity="0.5"/>
  </svg>
  <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;">{icon}</div>
</div>'''

def five_question_progress(uid_prefix, states=None, size=140, gap=48, bg="paper", rail=True):
    """The persistent five-seal rail (or cluster). `states` is a list of 5
    of unseen/active/answered/unknown; defaults to all-unseen. Reused
    verbatim s03 -> s13 with only `states` changing per scene."""
    states = states or ["unseen"] * 5
    seals = []
    for i in range(5):
        seal_id = f"{uid_prefix}-{i}"
        seals.append(question_seal(seal_id, i, states[i], size=size, bg=bg))
    rail_html = ""
    if rail:
        rail_w = gap * 4 + size * 5
        rail_html = (f'<div class="q-rail" id="{uid_prefix}-rail" style="position:absolute;left:{size/2}px;'
                     f'right:{size/2}px;top:50%;height:2px;background:var(--line);z-index:-1;"></div>')
    return (f'<div class="q-progress" id="{uid_prefix}-wrap" style="position:relative;display:flex;'
            f'gap:{gap}px;align-items:center;">{rail_html}{"".join(seals)}</div>')
