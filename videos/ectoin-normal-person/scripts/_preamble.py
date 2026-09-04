"""Shared CSS/HTML preamble for every scene file in this project.

Tokens are INLINED, not linked. A <link rel="stylesheet"> to the shared
assets/tokens/tokens.css is confirmed not to resolve custom properties through
this render pipeline (measured empty on a compiled render), so the values are
copied with that file as the single source of truth. Grep for a distinguishing
value (e.g. --safe-bottom: 108px) to check a scene is in sync with it.
"""
import re

# VERDICT-COMPRESSION REVISION: vendored locally, not loaded from a CDN.
# assets/vendor/gsap-3.14.2.min.js is a one-time fetch of the exact same
# pinned version every scene file already used, frozen the same way fonts
# under assets/fonts/ are -- project-relative, no live network dependency at
# render time. Path convention matches FONTS below (root-relative, no "../..").
GSAP = '<script src="assets/vendor/gsap-3.14.2.min.js"></script>'

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
    --aqua:#59B8AE; --leaf:#6F8F72; --coral:#C97A5C; --highlighter:#E0A32B;
    --moss:#4F6B52; --celadon:#93B896;
    /* JAY's accent is GROUND-SCOPED. Measured (scripts/contrast.py):
       --coral on ink 5.60:1 PASS, on paper 3.00:1 FAIL.
       --coral-deep on paper 4.60:1 PASS, on ink 3.66:1 FAIL.
       Use the variant matching the ground under the text, never by name. */
    --coral-deep:#A85A3C;
    --ink-2:#6B6B6B; --ink-3:#9C978D; --ink-2-dark:#878B8C; --ink-3-dark:#7C8082;
    --rule:#E3E3E3; --rule-strong:#D9D3C6; --rule-dark:#333333;

    --font-display:"EB Garamond",Georgia,"Times New Roman",serif;
    --font-body:"Inter",system-ui,-apple-system,sans-serif;
    --font-mono:"JetBrains Mono",ui-monospace,"SF Mono",Consolas,monospace;

    --t-hero:96px; --t-figure:60px; --t-frame:50px; --t-body:40px;
    --t-caption:24px; --t-label:32px; --t-chip:32px; --t-floor:20px;
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
    /* The static clip ancestor. NOTHING may transform this element: it is the
       box that turns "the safe area" into a hard boundary, and overflow:hidden
       only clips an element's children, so a transform applied HERE would move
       the boundary along with the content it is meant to contain. */
    .clipbox { position:relative; width:100%; height:100%; min-height:0;
               overflow:hidden; }
    /* The scene's ground plane. A sibling of nothing -- it fills #root and
       carries the paper/ink background. It is a CLASS, not a second #root:
       duplicate ids meant the background never painted and five ink-ground
       units shipped paper-on-paper text at 1:1. */
    .ground { position:absolute; inset:0; overflow:hidden; }
    /* The camera-spine layer. Separate from .world so an authored leg and the
       slow drift compose instead of overwriting each other's transform. */
    .drift { position:relative; width:100%; height:100%; min-height:0;
             transform-origin:50% 50%; will-change:transform; }
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
    /* A full-panel colour wash. scaleX from the left = a large area changing.
       No CSS transform initializer here -- non-negotiable #11. Every .wash
       reveal is driven by tl.fromTo(el, {{scaleX:0}}, {{scaleX:1,...}}), so
       GSAP already declares its own start state; a CSS one would just be a
       second, driftable copy of the same value. transform-origin stays --
       GSAP's fromTo does not set it, so CSS is the only declared source. */
    .wash { position:absolute; inset:0; transform-origin:0% 50%;
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

    /* A panel-sized strike: covers the whole card, not a 5px line through a word. */
    .void { position:absolute; inset:0; background:var(--coral); opacity:0;
            border-radius:inherit; }
    .p-title { font-family:var(--font-body); font-weight:800; font-size:var(--t-frame);
               line-height:var(--lh-snug); margin:0 0 var(--s-3); }
    .p-body { font-family:var(--font-display); font-size:var(--t-body);
              line-height:var(--lh-body); margin:0; color:var(--ink-2); }
    .p-body.on-ink { color:var(--ink-2-dark); }
    .kicker { font-family:var(--font-mono); font-size:var(--t-label);
              letter-spacing:var(--tr-mono-wide); text-transform:uppercase;
              color:var(--ink-2); margin:0; }
    .kicker.on-ink { color:var(--ink-3-dark); }
    .hero { font-family:var(--font-display); font-size:var(--t-hero);
            line-height:var(--lh-tight); letter-spacing:var(--tr-display); margin:0; }
    .fig { font-family:var(--font-display); font-size:var(--t-figure);
           line-height:var(--lh-snug); margin:0; }
    .col { display:flex; flex-direction:column; min-height:0; }
    .grow { flex:1 1 0; min-height:0; }

    /* ---- SPEAKER ATTRIBUTION, carried by TYPE alone ----------------------
       This project has NO persistent speaker rails, so nothing but the
       typography tells a viewer who is talking. The two roles are therefore
       built on the largest contrast this design system owns -- a display
       SERIF against a grotesque at weight 800. That survives any ground, any
       scale, and the 25% phone-scale downscale check. A colour difference
       alone would not, and colour is the half that breaks: see --coral-deep.
         SOULHABIT  EB Garamond, larger, ground-neutral. The authored voice.
         JAY        Inter 800, tighter, coral mark. The interruption.
       --font-mono stays reserved for citations and chrome. Do not spend it. */
    .say { margin:0; }
    .say-s { font-family:var(--font-display); font-size:var(--t-hero);
             line-height:var(--lh-tight); letter-spacing:var(--tr-display);
             color:var(--ink); }
    .say-j { font-family:var(--font-body); font-weight:800; font-size:var(--t-figure);
             line-height:var(--lh-snug); color:var(--ink); }
    .say-s.on-ink, .say-j.on-ink { color:var(--paper); }

    /* The speaker mark is DECORATIVE -- it never carries legibility, so the
       ground-scoped coral can never become a readability bug. Colour marks the
       turn; the typeface is what actually identifies the speaker. */
    .who { display:block; width:88px; height:6px; border-radius:var(--r-pill);
           margin:0 0 var(--s-4); }
    .who-s { background:var(--aqua); }
    .who-j { background:var(--coral-deep); }
    .who-j.on-ink { background:var(--coral); }

    /* ---- CAMERA ----------------------------------------------------------
       One .world per scene, driven by a single cam {scale,x,y}. Continuity
       here is carried by the CAMERA, because attribution is type-only and so
       no actor spans a cut by default. `.stage > * {overflow:hidden}` above
       already clips the moving world at the safe line, which is why a camera
       leg cannot drag content into a reserved zone the way a translating push
       transition was measured doing (99 failed frames on the predecessor). */
    /* The camera layers are children of .stage, so they fill its CONTENT box
       (the safe box) rather than its padding box. An abspos inset:0 would
       resolve against the padding box and defeat the whole arrangement, so
       these are in-flow and sized 100%. */
    .world { position:relative; width:100%; height:100%; min-height:0;
             transform-origin:50% 50%; will-change:transform; }

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


def _prefix_ids(cid, body, css, timeline):
    """Prefix every DOM id assembled for this composition with the
    composition id -- non-negotiable #10 of the rebuild brief.

    WHY THIS EXISTS AS A CENTRAL PASS, not a per-unit convention: 01-bottle
    already needed a hand-applied `ob-` prefix because two units render into
    the same document at once during a wipe, and a bare `#pc` / `#in-10`
    there collided with 12-bottle's own ids -- caught by `check` as
    `motion_selector_ambiguous`, an ERROR, not a warning. Doing this once,
    centrally, at emit time removes the whole class of bug instead of
    requiring the next unit author to remember it.

    Discovers every id from the STATIC `id="X"` markup already assembled
    into body/css/timeline (by this point build_frames.py has already
    appended its own band-beat and ambient-drift tweens, so those are
    covered too), then rewrites every reference to each one: the HTML
    attribute, any '#X'/"#X" selector (CSS rule or JS string, either quote
    style), and any getElementById('X')/("X") call. #root is exempt -- the
    render engine mounts against it by a fixed contract; it is never
    scene-owned and must not be touched.

    NOT covered: ids assigned dynamically at runtime via `el.id = 'x-' + i`
    (the ring/strand per-node ids in 04-protein/05-skin). None of those are
    ever selected individually by id -- only as '#ring rect' / '#strands
    path' compound selectors targeting the STATIC parent id, which IS
    covered -- so there is no collision risk left uncovered, only ids that
    were never collision-prone to begin with.

    IS covered, and had to be added after the first version of this function
    shipped 156 "GSAP target not found" runtime warnings across the piece --
    two distinct dynamic-selector idioms, neither a static id="X" match:

      1. `['x1','x3'].forEach(function (id) { tl.to('#' + id, ...) })` --
         a bare id string sitting in an array literal, concatenated with
         '#' at call time. Matched positionally: 'X' immediately after '['
         or ',' and immediately before ',' or ']', so an unrelated string
         that happens to equal a short id name elsewhere in the same
         unit's JS (plain text content, a CSS value) is not touched.
      2. `'#ob-in-' + i` -- a STEM shared by a whole family of real,
         statically-declared ids (ob-in-0 .. ob-in-11, each a real
         id="ob-in-N" in the markup), concatenated with a loop counter.
         The stem itself is never a complete id, so the exact-match id
         regex above cannot see it; every id ending in digits contributes
         its non-digit prefix as a stem, and every '#stem' string (as a
         complete quoted literal, not a substring) gets prefixed too.
    """
    combined = body + css + timeline
    ids = sorted(set(re.findall(r'id="([^"]+)"', combined)) - {"root"})

    # A second dynamic-selector idiom, distinct from the array-literal one
    # above: a static list of ids (like the INCI list's ob-in-0..ob-in-11,
    # each a real id="..." in the markup) selected in a loop by
    # concatenating a STEM string with a counter -- '#ob-in-' + i, not a
    # bare array. The stem itself is never a complete id, so the exact-
    # match #{old} regex above cannot see it. Derive every stem as the
    # non-digit prefix of any id ending in digits, longest first so a
    # shorter stem (e.g. a hypothetical "tl-" vs "tl-0") never shadows a
    # more specific one.
    stems = sorted({re.match(r"^(.*?)(\d+)$", i).group(1)
                     for i in ids if re.match(r"^.*\d+$", i)},
                    key=len, reverse=True)

    def sub(part):
        for old in ids:
            new = f"c{cid}-{old}"
            part = part.replace(f'id="{old}"', f'id="{new}"')
            part = re.sub(rf'#{re.escape(old)}(?![A-Za-z0-9_-])', f'#{new}', part)
            part = part.replace(f"getElementById('{old}')", f"getElementById('{new}')")
            part = part.replace(f'getElementById("{old}")', f'getElementById("{new}")')
            part = re.sub(rf"(?<=[\[,])(\s*)'{re.escape(old)}'(\s*)(?=[,\]])",
                           rf"\1'{new}'\2", part)
            part = re.sub(rf'(?<=[\[,])(\s*)"{re.escape(old)}"(\s*)(?=[,\]])',
                           rf'\1"{new}"\2', part)
        for stem in stems:
            part = part.replace(f"'#{stem}'", f"'#c{cid}-{stem}'")
            part = part.replace(f'"#{stem}"', f'"#c{cid}-{stem}"')
        return part

    return sub(body), sub(css), sub(timeline)


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
    body, css, timeline = _prefix_ids(cid, body, css, timeline)
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
    var tl = gsap.timeline({{ paused: true }});
{timeline}
    tl.to({{}}, {{ duration: {duration:.3f} }}, 0);   // full-span anchor -- always last
    window.__timelines["{cid}"] = tl;
  </script>
</template>
</body>
</html>
"""
