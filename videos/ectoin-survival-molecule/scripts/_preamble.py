"""Shared CSS/HTML preamble for every scene file in this project.

Tokens are INLINED, not linked. A <link rel="stylesheet"> to the shared
assets/tokens/tokens.css is confirmed not to resolve custom properties through
this render pipeline (measured empty on a compiled render), so the values are
copied with that file as the single source of truth. Grep for a distinguishing
value (e.g. --safe-bottom: 108px) to check a scene is in sync with it.
"""

GSAP = '<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>'

# Fonts are self-hosted woff2 under assets/fonts/. Paths are ROOT-RELATIVE:
# sub-compositions are served with the PROJECT ROOT as their base URL, not the
# compositions/ directory. A "../../assets/..." path traverses above the root and
# 404s in Studio preview even though the renderer rewrites it against the source
# path -- `check` flags it as invalid_parent_traversal_in_asset_path.
FONTS = """
    @font-face { font-family:"EB Garamond"; src:url("assets/fonts/eb-garamond-400.woff2") format("woff2");
                 font-weight:400; font-display:block; }
    @font-face { font-family:"Inter"; src:url("assets/fonts/inter-800.woff2") format("woff2");
                 font-weight:800; font-display:block; }
    @font-face { font-family:"JetBrains Mono"; src:url("assets/fonts/jetbrains-mono-500.woff2") format("woff2");
                 font-weight:500; font-display:block; }
"""

# --- tokens, inlined from assets/tokens/tokens.css -------------------------
# Type scale is UNCHANGED from the Shorts projects: 1080x1920 and 1920x1080
# share a 1080px short edge and type size is a fraction of the short edge, so
# the scale transfers one-for-one. Layout gets a landscape variant; type does not.
TOKENS = """
    --paper:#F7F5F0; --ink:#131516; --ink-soft:#211F1B; --mist:#F0EBE1; --white:#FCFBF9;
    /* --coral is scoped to DARK grounds: 5.03:1 on --ink-soft, but only
       3.00:1 on --paper and 2.72:1 on the light cards 26-kbeauty uses.
       --coral-deep is the same hue for a light ground. It is deeper than the
       4.5:1 arithmetic strictly needs, because the pixel gate measures a
       30px mono glyph's Otsu median, and antialiasing on thin strokes pulls
       that toward the ground -- #9E5236 computes 5.19:1 and MEASURES 4.10:1
       on the render. The number that matters is the measured one. */
    --aqua:#59B8AE; --leaf:#6F8F72; --coral:#C97A5C; --coral-deep:#8E4228;
    --highlighter:#E0A32B;
    --moss:#4F6B52; --celadon:#93B896;
    /* MEASURED against the grounds they actually land on, not against paper
       alone. --ink-2 was 4.49:1 on --mist (the .cite chip, .sh.from) and
       --ink-2-dark 4.78:1 on --ink-soft with no headroom for the retention
       plates behind it; both now clear 4.5:1 with room. --ink-3-dark (4.13:1
       on --ink-soft) is kept for non-text use only -- no text binds to it. */
    --ink-2:#666666; --ink-3:#9C978D; --ink-2-dark:#8E9293; --ink-3-dark:#7C8082;
    --rule:#E3E3E3; --rule-strong:#D9D3C6; --rule-dark:#333333;

    --font-display:"EB Garamond",Georgia,"Times New Roman",serif;
    --font-body:"Inter",system-ui,-apple-system,sans-serif;
    --font-mono:"JetBrains Mono",ui-monospace,"SF Mono",Consolas,monospace;

    /* Raised for the 2026-09-05 accessibility pass: essential informational
       text sits at 48px+ in the 1080p master, chrome and labels at 36px, and
       nothing a viewer is expected to read is under 30px. The display sizes
       (hero/figure/frame) are unchanged -- they were never the problem. */
    --t-hero:96px; --t-figure:60px; --t-frame:50px; --t-body:48px;
    --t-caption:30px; --t-label:36px; --t-chip:36px; --t-floor:20px;
    --lh-tight:1.06; --lh-snug:1.2; --lh-body:1.45;
    --tr-display:-0.018em; --tr-body:0em; --tr-mono:0.04em; --tr-mono-wide:0.1em;

    --e-out:cubic-bezier(0.215,0.61,0.355,1);
    --e-inout:cubic-bezier(0.455,0.03,0.515,0.955);

    --s-2:8px; --s-3:12px; --s-4:20px; --s-5:32px; --s-6:60px; --s-7:96px; --s-8:144px;
    --r-2:6px; --r-3:10px; --r-pill:999px;

    /* landscape canvas + reserved zones -- see tokens.css for the derivation */
    --canvas-w:1920px; --canvas-h:1080px;
    --safe-top:54px; --safe-bottom:108px; --safe-left:96px; --safe-right:96px;
    --safe-margin:6px;
    /* End-screen reserve -- SCENE-SCOPED, consumed by 29-cta alone. Present here
       because an inlined token block that omits a token used by any scene fails
       SILENTLY: the calc() is invalid and the whole declaration is dropped. */
    --endscreen-right:640px; --endscreen-bottom:200px;
"""

# `box-sizing` first rule in EVERY composition -- a project missing it passes
# `check` completely clean and still lays a stage out taller than declared.
# `min-height:0` on flex children with an explicit small basis, for the same reason.
BASE = """
    *,*::before,*::after { box-sizing:border-box; }
    html,body { margin:0; padding:0; width:1920px; height:1080px; overflow:hidden; }
    #root { position:absolute; inset:0; overflow:hidden; }
    .stage { position:relative; width:100%; height:100%;
             padding:var(--safe-top) var(--safe-right) var(--safe-bottom) var(--safe-left); }
    /* The stage's single child fills the SAFE BOX exactly, so clipping it clips
       at the safe line. Confirmed necessary: on the first full render the hard
       safe-area gate found 81 frames with ink in a reserved zone, all of them
       entrance-transform transients (a panel offset x:-90 from a resting edge
       that IS the safe line) or scale-up transients. Containment beats a bigger
       margin -- a margin is sized against today's token and goes stale silently. */
    .stage > * { overflow: hidden; }
    .flexmin { min-height:0; }

    /* Citation chip: `Journal · Year` ONLY. Never an internal id or a PMID --
       those live in BRIEF.md's claim table and the video description. */
    .cite { font-family:var(--font-mono); font-weight:500; font-size:var(--t-chip);
            letter-spacing:var(--tr-mono); color:var(--ink-2);
            border:2px solid var(--rule-strong); border-radius:var(--r-pill);
            padding:10px 26px; right:auto; width:max-content; bottom:auto;
            background:var(--mist); }
    .cite.on-ink { color:var(--ink-2-dark); border-color:var(--rule-dark);
                   background:var(--ink-soft); }

    /* ---- panel-scale beat primitives -------------------------------------
       Act 1 measured 4-5.8% active steps against 11.7-23.1% on shipped 9:16
       projects. Cause: on a 1920-wide frame a headline sits in a grid cell, so
       a text fade changes ~0.7% of the pixels. These move a whole panel or
       column instead -- 15-50% per beat -- which is what actually reads. */
    .panel { position:relative; background:var(--mist); border-radius:var(--r-3);
             padding:var(--s-6); min-height:0; overflow:hidden; }
    .panel.on-ink { background:var(--ink-soft); }
    /* A full-panel colour wash. scaleX from the left = a large area changing. */
    .wash { position:absolute; inset:0; transform:scaleX(0); transform-origin:0% 50%;
            border-radius:inherit; z-index:0; }
    /* Every following sibling of a wash sits ABOVE it. The earlier rule was
       scoped to .panel children only, so .arm/.stt/.action labels rendered
       UNDER their own wash (check: text_occluded, a hard error).
       CAVEAT this rule cannot cover: a BARE TEXT NODE has no element to carry
       position/z-index, so a wash paints straight over it and the card renders
       EMPTY -- confirmed on three cards, caught by the region-aware content-void
       check and verified by frame extraction. Always wrap copy in an element
       inside a washed container; the `:empty` guard below makes a stray case
       visible in review instead of silently blank. */
    .wash ~ * { position:relative; z-index:1; }
    .wash:only-child { outline:3px dashed #C97A5C; }   /* a wash with no sibling
                                                          content is authoring error */
    .wash.aqua { background:var(--aqua); } .wash.coral { background:var(--coral); }
    .wash.moss { background:var(--moss); } .wash.mist { background:var(--mist); }
    /* --rule-strong, for washing a panel that is ALREADY --mist. `.wash.mist` on
       a --mist panel is the same colour on the same colour: it renders nothing,
       and a scene relying on it as a beat holds silently. Measured on scene 08. */
    /* Full-canvas layer, for a scene that stacks TWO complete grounds and
       reveals one over the other (09-exclusion: paper "tidy version" under
       an ink "honest correction", swept in by clip-path). Each .world fills
       its own .stage internally -- this class only pins position/overflow so
       stacking two of them under #root does not double the safe-area padding. */
    .world { position:absolute; inset:0; overflow:hidden; }
    .wash.dim  { background:var(--ink-3); }   /* 82-luma step off --mist; a
       --rule-strong wash was only 20 luma and barely registered as a beat */
    /* WASH COLOUR IS BOUND TO TEXT COLOUR. A wash replaces what sits behind the
       text, so the token that passed against the panel's ORIGINAL ground can fail
       against the wash -- measured: --ink-2 on aqua is 2.26:1, and --paper on aqua
       is ~1.9:1. Two safe pairings only:
         light ground -> .wash.aqua    + --ink text   (7.76:1)
         dark  ground -> .wash.moss    + --paper text (5.42:1)
       Anything else must be re-measured against the wash, not the panel. */
    .wash.aqua ~ *, .wash.coral ~ *, .washed-light { color:var(--ink) !important; }
    .wash.moss ~ *, .washed-dark  { color:var(--paper) !important; }
    .wash.dim ~ *  { color:var(--ink) !important; }

    /* A panel-sized strike -- but a STRIKE, not a cover. This used to be a
       full-card coral flood at inset:0. It is absolutely positioned and is not
       a `.wash`, so the rule below that lifts washed siblings to z-index 1 never
       applied to it, and at 0.85 it painted straight over the copy: measured
       1.03:1 on 19-limits and unreadable on 26-kbeauty in the shipped master.
       A bar through the middle of the card is the same panel-scale gesture and
       leaves the words legible; the copy still has to be lifted above it. */
    .void { position:absolute; left:-8px; right:-8px; top:50%;
            height:10px; margin-top:-5px; background:var(--coral); opacity:0;
            transform:scaleX(0); transform-origin:0% 50%; z-index:2; }
    .void ~ * { position:relative; z-index:3; }
    /* The label that says in WORDS what the strike says in colour. */
    /* The strike is on a LIGHT card wherever .void is used, so the label takes
       the light-ground coral: --coral would read 2.72:1 there. */
    .void-tag { display:inline-block; margin-top:var(--s-3);
                font-family:var(--font-mono); font-weight:500;
                font-size:var(--t-caption); letter-spacing:var(--tr-mono-wide);
                text-transform:uppercase; color:var(--coral-deep); opacity:0; }
    .p-title { font-family:var(--font-body); font-weight:800; font-size:var(--t-frame);
               line-height:var(--lh-snug); margin:0 0 var(--s-3); }
    .p-body { font-family:var(--font-display); font-size:var(--t-body);
              line-height:var(--lh-body); margin:0; color:var(--ink-2); }
    .p-body.on-ink { color:var(--ink-2-dark); }
    .kicker { font-family:var(--font-mono); font-size:var(--t-label);
              letter-spacing:var(--tr-mono-wide); text-transform:uppercase;
              color:var(--ink-2); margin:0; }
    .kicker.on-ink { color:var(--ink-2-dark); }
    .hero { font-family:var(--font-display); font-size:var(--t-hero);
            line-height:var(--lh-tight); letter-spacing:var(--tr-display); margin:0; }
    .fig { font-family:var(--font-display); font-size:var(--t-figure);
           line-height:var(--lh-snug); margin:0; }
    .col { display:flex; flex-direction:column; min-height:0; }
    .grow { flex:1 1 0; min-height:0; }

    /* Debug overlay -- toggled by a class on #root, never on <body>.
       Confirm it is OFF by checking frame zero before any real render. */
    #root.debug-layout * { outline:1px solid rgba(255,0,0,.55) !important; }
    #root.debug-layout::after {
      content:""; position:absolute; inset:0; pointer-events:none; z-index:99;
      background:
        linear-gradient(to bottom, rgba(255,0,168,.22) var(--safe-top), transparent var(--safe-top)),
        linear-gradient(to top,    rgba(255,0,168,.22) var(--safe-bottom), transparent var(--safe-bottom)),
        linear-gradient(to right,  rgba(255,0,168,.22) var(--safe-left), transparent var(--safe-left)),
        linear-gradient(to left,   rgba(255,0,168,.22) var(--safe-right), transparent var(--safe-right));
    }
"""


def scene(cid, duration, body, css, timeline):
    """Emit one sub-composition file.

    THE <template> IS THE TRANSPORT CONTAINER, and this is the detail that bites:
    the runtime fetches the file, parses it, and clones ONLY the template's
    CONTENTS into the host slot. Everything outside it -- the whole <head>
    included -- is DISCARDED.

    So the <style>, the root div, the GSAP tag AND the timeline script must all
    live INSIDE the template. Putting the scripts after </template> (the natural
    place, and what a standalone HTML file wants) means they are thrown away: the
    scene then renders at its static CSS state with no timeline at all. Measured
    here before the fix -- t=0.0s and t=8.5s of scene 01 came out PIXEL-IDENTICAL,
    and the render logged `sub_timeline_readiness_timeout` because no
    window.__timelines entry was ever registered.

    There is also no importNode/appendChild bootstrap: the runtime does the
    cloning. Adding one is what makes the file look right when opened standalone
    and wrong when rendered.
    """
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>{cid}</title></head>
<body>
<template>
  <div id="root" data-composition-id="{cid}"
       data-width="1920" data-height="1080" data-duration="{duration:.3f}">
    <style>
      #root {{{TOKENS}}}
{FONTS}
{BASE}
{css}
    </style>
{body}
  </div>
  {GSAP}
  <script>
    window.__timelines = window.__timelines || {{}};
    var tl = gsap.timeline({{ paused: true, defaults: {{ ease: "power3.out" }} }});
{timeline}
    tl.to({{}}, {{ duration: {duration:.3f} }}, 0);   // full-span anchor -- always last
    window.__timelines["{cid}"] = tl;
  </script>
</template>
</body>
</html>
"""
