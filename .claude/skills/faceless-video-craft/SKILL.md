---
name: faceless-video-craft
description: Craft layer for building faceless video as code — HTML/CSS/JS/WebGL compositions rendered deterministically through HyperFrames (HeyGen's HTML-to-video engine), plus motion design, image-driven animation, and YouTube retention and interaction architecture. Use whenever the work involves making video with no presenter on camera — motion graphics, animated explainers, kinetic typography, image-plate animation, parallax and 2.5D, scene maps, shot lists, render pipelines, branching or interactive YouTube pieces, or asks like "make a video", "animate this image", or "add motion". Trigger even when the ask sounds like plain frontend work, because compositions are rendered frame-by-frame by a seeking headless browser and ordinary web animation (rAF, Date.now, autoplaying CSS, GSAP without seek wiring) silently produces frozen or broken video. Also trigger on HyperFrames, hyperframes CLI, data-start, data-composition-src, window.__timelines, Remotion, Ken Burns, displacement map, sprite sequence, end screens, chapters, or 9:16 short.
---

# Faceless video craft

This is the **craft and engine** layer: how to build video out of web code so it
looks authored rather than templated, and how to make it survive a deterministic
renderer.

It is deliberately domain-neutral. Truth rules, claim/source enforcement, brand
palettes, and component rosters belong to a **project skill**, not here. If a
project skill is in play, its constraints win on content; this skill still governs
craft. Never carry one project's constraints into another project's work — a rule
that exists because a specific record set had defects is not a general rule.
**This repo currently has no project skill holding those truth/claim rules** —
don't go looking for one that doesn't exist, and don't treat its absence as
license to skip citation discipline. What this file *does* own, because it's
presentation rather than domain truth, is what form a citation takes on screen
and what must never render at all — see *What must never reach a rendered
frame* below.

## Read order

1. This file — decisions, loop, posture, and the canonical patterns below.
   Everything required to build a correct composition is in this file.
2. `references/` — if `hyperframes-engine.md`, `motion-craft.md`,
   `image-motion.md`, or `interactive-youtube.md` are present alongside this
   file, read the relevant one for depth. **Do not assume they exist.** Check
   with a directory listing first. If they are absent, this file is complete on
   its own — never stall or hand back a partial answer because a reference file
   is missing.

**Before writing markup for a real render, read the installed HyperFrames skills
(`/hyperframes` is the router) and the version's own docs.** The framework is
young and moves; the shipped API wins over anything recalled below. Every
attribute name and API shape in this file was verified against a real shipped
project, but treat it as *the shape to look for*, not a frozen spelling —
confirm with `npx hyperframes docs <topic>` or the project's own `CLAUDE.md`
before a real render, and prefer what the project's own `CLAUDE.md` says over
this file if the two disagree on engine mechanics (this file governs craft; the
project's `CLAUDE.md` and installed HyperFrames skills govern the engine
contract for that specific pinned CLI version).

Also read `/mnt/skills/public/frontend-design/SKILL.md` before visual specs.
Compositions are frontend and inherit its taste rules.

## Mandatory render rules

Non-negotiable. These are operator rules, not preferences, and they override
convenience in every case.

1. **Image rendering.** Never use `loading="lazy"`. A headless renderer will
   skip unpainted images and the frame ships without them. Always
   `loading="eager" decoding="sync"`, always explicit `width`/`height`
   attributes plus an explicit `object-fit`, and always a background colour on
   the parent container. Apply this to *every* `<img>`, including ones added
   late in a build (B-roll inserts, interlude stills) — a missing attribute on
   one image in an otherwise-correct project is the single most common defect
   found in review.
2. **Layout math.** Build spatial relationships inside a clip with CSS Grid or
   Flexbox. `position: absolute` is the correct and sanctioned mechanism for
   **clip/scene stacking** — HyperFrames' own idiom is `.clip { position:
   absolute; inset: 0; }` so multiple timed layers occupy the same canvas and
   the engine toggles which one paints. What must not be absolute is the
   *internal* structure of a clip: the columns, rows, and card layout inside
   it. If two elements' relative position is expressed as two independent
   `top`/`left` values instead of a Grid/Flex relationship, that is the layout
   bug this rule exists to prevent — it will not survive a string-length
   change or an aspect-ratio flip.
3. **`box-sizing: border-box` on every element, always** — `*, *::before,
   *::after { box-sizing: border-box; }` as the first rule in every
   composition's `<style>` block. Any element that combines an explicit
   `height`/`width` with `padding` renders LARGER than declared under the
   CSS default (`content-box`), because padding is added on top of the
   declared size instead of reserved within it. Confirmed as the root
   cause of a genuinely hard-to-diagnose defect: a `.stage { height:
   1920px; padding: 192px ... 384px ...; }` rendered as an actual
   **2496px** box (1920 + 576 top/bottom padding), silently pushing
   bottom-anchored content — citation chips, a CTA — past the real canvas
   edge and into, or entirely out of, the reserved safe zone. This
   reproduced identically across renders regardless of `--safe-*` token
   values, `justify-content` strategy, flex-grow vs. explicit flex-basis,
   or sub-composition nesting depth, and is **invisible from source** — it
   only shows up as a discrepancy between `getComputedStyle(el).height`
   (reports the declared value, e.g. "1920px") and
   `el.getBoundingClientRect().height` (reports the actual laid-out value,
   e.g. 2496) on a real compiled render. A project missing this reset can
   pass `npx hyperframes check`'s lint/runtime/motion/contrast passes
   completely clean while still shipping this defect — check surfaces it
   only as scattered `container_overflow`/`canvas_overflow` **info**-level
   layout findings (non-blocking), not as an error, so a project that
   doesn't investigate its own info findings will ship it. See *Failure
   modes worth naming* below for the second half of this defect
   (`min-height: auto` on flex children) and the fix for both.
4. **Validation mode.** When asked to verify a layout or draft a skeleton, ship
   a debug overlay the operator can toggle without editing anything first (see
   *Layout validation and debug strategy* below for the concrete pattern in
   this engine).

## What must never reach a rendered frame

Distinct from the mandatory rules above, which govern how markup renders —
this governs what content is allowed to render at all. Confirmed shipped
defects, not hypotheticals:

- **Internal record/citation IDs.**
  `videos/pdrn-cellular-science/compositions/frames/03-history.html` renders
  "CITATION — ⌞ ING-pdrn-S003 ⌟" directly on screen — a raw catalog key,
  meaningless to a viewer — in a citation-pill pattern repeated across
  `retinal-clinical-dossier` and others. A citation pill reads `Journal ·
  Year` (or an equivalent human-readable form); it never carries the internal
  ID that looked the source up. The full source name, DOI, or URL belongs in
  the video description (see *The delivery manifest*), not the frame.
- **Placeholder strings, TODO text, and unfinished copy.** The same class of
  defect as a draft-only remote image URL (*Asset protocol* below) or a
  debug overlay left on (*Layout validation* below) — something authored for
  a working session that was never meant to survive to the export.
- **Absolute claim language the source doesn't back.** "...is useless
  without one specific ingredient" renders verbatim in
  `videos/ceramides-barrier-diagnostic/compositions/01-hook.html` — a hook
  line, not a cited claim, but it reads as one to a viewer. Superlatives and
  absolutes ("guaranteed," "instantly," "proven," "always," "useless")
  deserve the same scrutiny a cited efficacy claim gets, citation pill
  attached or not.
- **A drawn mechanism dressed as data.** An illustration of an unmeasured
  process must not borrow chart grammar — axes, gridlines, a plotted line or
  point — that implies a real measurement sits behind it. Label a diagram as
  a diagram when it isn't a rendering of actual study data.
- **An untranslated clinical/technical register in the claim itself.** A
  citation pill (`Journal · Year`, a CFR/regulation code) is a provenance
  stamp, not something the viewer has to parse — that's already covered
  above. This is different: it's the *claim sentence* — the headline,
  qualifier, or instruction the video is actually asking the viewer to walk
  away with — using clinical/regulatory shorthand as if the audience already
  has the vocabulary to decode it (a raw statistic with no plain-language
  frame — "reduced TEWL by 23%" with no gloss for what TEWL is or why 23%
  matters; a mechanism-of-action term dropped in unexplained — "inhibits
  tyrosinase" instead of "slows the enzyme that makes dark spots"; a severity
  or dosing term borrowed straight from a regulatory text without
  translating it into what the viewer should actually do). The test: could
  the target audience (see the project's own `audience:` line) act on the
  on-screen sentence correctly without knowing what the technical term
  means? If not, it needs a plain-language equivalent standing in the
  headline/qualifier position, with the technical term optionally still
  present as backup, not instead of the translation. Citations sitting
  beside an already-plain-language claim are the sanctioned pattern this
  rule doesn't flag — confirmed against `videos/peeling-not-progress`'s full
  copy deck: every claim/instruction ("Severe burning or swelling? Stop and
  ask a doctor.", "In trials, more irritation didn't mean better results.")
  is plain English on its own, with citation pills (`Arch Dermatol · 1995`,
  `21 CFR 333.350`) doing pure provenance work beside it — a real example of
  what passing this check looks like, not just what failing it looks like.

This is the craft half of research integrity: presentation, not whether the
underlying claim is true. Whether a claim is defensible — a real source
exists, the cited population/product-type/route actually matches, injected
clinical treatments are distinguished from topical cosmetics — is
domain-truth work, and as the note above says, no project skill in this repo
currently holds it. Don't let that missing home become an excuse to skip the
presentation half this section does own. The same is true of the
plain-language rule just above: whether the *underlying science* is
correctly simplified (not just readably worded) is domain-truth work outside
this skill's remit; what this section owns is that the on-screen sentence
carrying the claim doesn't require the viewer to already speak clinical.

## The five things that actually break work

**1. Time is seeked, not played.** The renderer opens the page in headless Chrome
and jumps to each frame. Nothing that depends on wall-clock or on having played
the previous frame will work. No `requestAnimationFrame` loops driving your own
clock, no `Date.now()`, no `performance.now()`, no `setInterval`, no physics that
integrates per tick, no CSS `animation` left to run on its own, no autoplaying
`<video>`. Every animated value must be a **pure function of the current time**.
This single constraint reshapes how you write everything and is the number one
cause of "the preview looks great, the MP4 is frozen." In HyperFrames the pure
function is a **paused GSAP timeline the engine seeks by calling `.seek(t)` on
it** (see *The time model* below) — GSAP calls are not banned, an *unseeked*
GSAP call (anything with `.play()`, `.to()` without registering the timeline
paused, or a scroll-trigger) is.

**2. Determinism is environment-scoped.** Same input, same output — on the same
platform. Linux is the reference path; macOS and Windows fall back to an
approximate capture. GPU/driver differences (ANGLE, Metal, SwiftShader) change
antialiasing and WebGL output. Fix the render environment before you build an
acceptance harness on top of it, and re-baseline when you move to CI or cloud.
That reference path is not strictly the safer one, though: Linux's
headless-shell capture defaults to a `beginframe` mode with its own frame-0
and scene-boundary fragility that macOS's screenshot fallback is structurally
immune to — see *Verification loop*'s frame-index-vs-nominal-timestamp check.

**3. Verify by pixels, never by manifest.** A render that reports success can
still contain missing glyphs, clipped text, an unloaded font falling back, a
placeholder string, a still-frozen "settle" frame in the middle of a scene, or
a near-blank transition midpoint. Extract frames on a regular interval — not
just at scene boundaries — and look at them; see *Verification loop* below for
the two checks a manifest cannot substitute for (static-hold and transition
midpoint). Fonts are a classic failure too: a subset webfont that covers the
site does not necessarily cover the video's characters, and the browser will
silently substitute.

**4. Frame zero is a design object.** The first built frame is the scroll-stop
and the thumbnail candidate. It is never blank, never mid-fade, never a lone
title on empty canvas. Compose it as if it were the only frame anyone sees —
concretely, that means the hero visual is already at (or very near) its resting
opacity/position at `t=0`, not mid-tween. A common bug: a headline authored to
fade in over its first 0.3–0.5s reads fine when scrubbed by eye but makes the
literal `t=0` export frame near-blank. Check the export's actual first frame,
not "the frame after things have appeared."

**5. Assets must exist before the composition does.** A composition cannot invent
a missing image. Decide the asset strategy first — browser-drawn (SVG/CSS/canvas/
WebGL), generated plates, licensed stock, or a mix — because it changes the entire
build. Whether generated imagery is permitted is a **project decision**, not a
property of this skill.

## Canonical patterns

Start from the patterns below — they are the shape HyperFrames actually uses in
production. A project may be single-file (`.clip` sections stacked in one
`index.html`) or split into **sub-compositions**: a root `index.html` timeline
that references child files via `data-composition-src`, each child a full
document whose motion is authored independently and coordinated by the parent's
timeline. Prefer sub-compositions once a project has more than ~4-5 scenes —
they keep each scene's markup, tokens, and timeline reviewable in isolation.

### Root composition skeleton

```html
<!DOCTYPE html>
<html lang="en" data-resolution="portrait">
<head>
  <meta charset="UTF-8">
  <title>Render Composition</title>
</head>
<body>
  <div id="root"
       data-composition-id="main"
       data-start="0"
       data-duration="90.00"
       data-width="1080"
       data-height="1920">

    <!-- Each scene is a clip that owns a time window on the canvas. -->
    <div class="scene clip" data-start="0" data-duration="8.0"
         data-composition-src="compositions/frames/01-hook.html"></div>
    <div class="scene clip" data-start="8.0" data-duration="7.5"
         data-composition-src="compositions/frames/02-promise.html"></div>
    <!-- ...one per scene -->
  </div>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.14.2/gsap.min.js"></script>
  <script>
    // The root timeline's own job is scene handoff — see "Cuts, crossfades,
    // and transitions." It does NOT drive content inside a scene; each
    // sub-composition owns that.
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    // Boundary treatment is FORMAT-SCOPED: cuts on the grid for a Short (no
    // tween at all); a 2-3-type transition system for long-form; never a
    // plain crossfade across a ground change, in either. A transition is a
    // timing edit — extend the outgoing clip's data-duration by d, pull the
    // incoming clip's data-start back by d, ping-pong data-track-index —
    // plus one tween stamped here at the overlap start, on the WRAPPERS:
    //   tl.to('#scene-01', { xPercent: -100, duration: 0.5, ease: 'power3.inOut' }, 7.5);
    tl.to({}, { duration: 90.00 }, 0); // anchor: tl.duration() === root duration
    window.__timelines["main"] = tl;
  </script>
</body>
</html>
```

### A sub-composition (one scene, one file)

```html
<!DOCTYPE html>
<html>
<head>
<style>
  /* Tokens: import or paste the project's tokens.css here — see
     "Design tokens across sub-compositions" for why paste-per-file is a trap. */
  #root {
    --paper: #F7F5F0; --ink: #131516; --aqua: #59B8AE;
    /* ...rest of the project's token set */
  }
  .clip { position: absolute; inset: 0; background: var(--paper); overflow: hidden; }

  /* Structure INSIDE the clip is Grid/Flex — never two independent absolute
     top/left pairs standing in for a layout relationship. */
  .content { display: flex; flex-direction: column; justify-content: center;
             height: 100%; padding: 0 90px; }

  .beat { --p: 0; opacity: var(--p);
          transform: translateY(calc((1 - var(--p)) * 24px)); }
</style>
</head>
<body>
  <template id="scene-template">
    <div id="root" class="clip">
      <div class="content">
        <h1 class="beat" id="headline">80% GINSENG?</h1>
      </div>
    </div>
  </template>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.14.2/gsap.min.js"></script>
  <script>
    // Instantiate the template, then build one paused timeline for this scene.
    const root = document.importNode(
      document.getElementById('scene-template').content, true);
    document.body.appendChild(root);

    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    tl.to('#headline', { '--p': 1, duration: 0.4, ease: 'power2.out' }, 0.15);
    tl.to({}, { duration: 8.0 }, 0); // anchor to the parent's declared duration
    window.__timelines["01-hook"] = tl;
  </script>
</body>
</html>
```

Three notes on using it:

- The engine seeks each registered timeline by id; nothing calls `.play()`
  anywhere in a composition. The full-span anchor tween (`tl.to({}, {duration:
  N}, 0)`) is what makes `tl.duration()` match the clip's declared duration —
  add it last in every timeline, root and sub-composition alike.
- `decoding="sync"` and explicit `width`/`height` on every `<img>` are
  additions worth restating: async decode is wall-clock behaviour, and the
  intrinsic size reserves the box before the file resolves.
- Fonts: the engine auto-fetches and injects deterministic `@font-face` rules
  for named Google Fonts at check/render time — you do not need to hand-write
  `@font-face`, but you do need the font *named* consistently across every
  sub-composition, and you should confirm the injection happened by reading
  the `check` log, not by assuming it worked.

The patterns below exist inline because the reference files may not be
installed and a composition must never be blocked on them.

### What a scene and a beat actually are

A **scene** (a `.clip`) is a block of markup with a start time and a duration,
optionally delegated to its own sub-composition file. A **beat** is a single
animated element inside a scene with its own timeline position. Scenes cut;
beats stagger. Nothing plays — the renderer sets a time and the page must
render that time correctly from a cold start.

```html
<div class="clip" data-start="0" data-duration="8.0"
     data-composition-src="compositions/frames/01-hook.html"></div>
<div class="clip" data-start="8.0" data-duration="7.5"
     data-composition-src="compositions/frames/02-promise.html"></div>
```

`data-start` / `data-duration` are the engine's real attributes — confirm the
exact spelling against the installed HyperFrames version's docs before
rendering, since a young framework's API can still drift between versions.

### The time model — one paused timeline per composition

Every animated value is a function of the timeline's local position. There is
exactly one registered timeline per composition (root or sub), it is paused,
and seeking it to the same position twice must produce pixel-identical output.

```js
// The engine seeks this timeline directly — it may jump to 7.2, then 0.4,
// then back to 7.2. All three must match a cold seek to that position.
window.__timelines = window.__timelines || {};
const tl = gsap.timeline({ paused: true });

tl.to('.beat-1', { '--p': 1, duration: 0.4, ease: 'power2.out' }, 0.0);
tl.to('.beat-2', { '--p': 1, duration: 0.4, ease: 'power2.out' }, 0.35);

// Idle motion (a float, a pulse) must be FINITE and resolve inside the beat's
// own duration — never an infinite repeat, which is wall-clock behaviour
// dressed up as a tween:
tl.to('.chip', { y: -6, duration: 0.6, yoyo: true, repeat: 3,
                 ease: 'power1.inOut' }, 1.2);

tl.to({}, { duration: 8.0 }, 0); // anchor — keep this last, always at time 0

window.__timelines["01-hook"] = tl;
```

Banned inside a composition, without exception: any `requestAnimationFrame`
loop that advances its own state, `Date.now()`, `performance.now()` used to
drive a value, `setTimeout`/`setInterval`, CSS `animation` that runs on its
own without being seeked, autoplaying `<video>`, and any GSAP timeline that is
not registered paused on `window.__timelines` and driven purely by the
engine's seek. A paused, registered `gsap.timeline()` — including nested
timelines, `yoyo`/`repeat` with a bounded count, and `ScrollTrigger`-free
scrubbing — is the sanctioned mechanism, not a workaround.

### Consuming `--p` in CSS

Motion lives in CSS custom properties driven by the timeline; the GSAP tween
above sets `--p` directly, and CSS reads it. No CSS `@keyframes`.

```css
.beat {
  --p: 0;
  opacity: var(--p);
  transform: translateY(calc((1 - var(--p)) * 24px));
  will-change: transform, opacity;
}

/* Ken Burns without animation: pure function of a scene-progress custom
   property the timeline also sets. */
.media-plate img {
  transform: scale(calc(1 + var(--progress, 0) * 0.08));
  transform-origin: 50% 40%;
}
```

### Motion idiom by narrative function

The `.beat` above is a **starting shape, not a vocabulary.** It is one
entrance — fade plus rise — that happens to be the one this file writes down,
which is exactly why it ends up on every element in a project. Choose the idiom
from what the beat is *doing narratively*, then implement it with the named
rule. Every name below is a real file in
`~/.claude/skills/hyperframes-animation/rules/`; read it before authoring
rather than reconstructing it from the label.

| What the beat is doing | Idiom | Rule |
|---|---|---|
| Explaining a mechanism or process | Draw it, deform it, assemble it | `svg-path-draw`, `reactive-displacement`, `depth-scatter-assemble` |
| Presenting evidence or data | Let the number, bar, or axis perform | `counting-dynamic-scale`, `stat-bars-and-fills`, `chart-scrub-readout` |
| Investigating something (a label, a list, a document) | Take the camera to the evidence | `coordinate-target-zoom`, `viewport-change` |
| Correcting a myth, delivering a verdict | Transform the wrong thing into the right one | `scale-swap-transition`, `card-morph-anchor` |
| Landing type on a spoken beat | Hit it, or sequence it word by word | `kinetic-beat-slam`, `discrete-text-sequence`, `asr-keyword-glow` |
| Holding, deliberately | Liveness from the hero actor or the camera | `multi-phase-camera` micro-drift |

Three of those rows carry a rule of their own.

- **Evidence: the choreography enacts the study's own structure.** A trial's
  *n* divides into its arms; a Week 0→4 outcome scrubs its own axis; a
  percentage counts to its value. That is the motion form of *Asset protocol*
  rule 8 — a diagram is not a chart unless it plots real data, and data is
  allowed chart grammar — and it is what makes a data beat explanatory rather
  than decorative (*Posture*'s "motion that means something").
- **Correction: transform, don't replace.** Fading card A out and card B in
  tells the viewer two unrelated things happened. `scale-swap-transition` and
  `card-morph-anchor` keep the anchor, so the second state reads as *the first
  one corrected* — the whole point of a myth-versus-fact beat.
- **A hold is not a licence to breathe a text card.** Liveness comes from the
  hero actor or a camera with a reason to move. `sine-wave-loop`'s own
  frontmatter is explicit — "**Reach for this last**… circular breathing as
  'aliveness' is cheap… I'd rather have NO motion than BAD motion" — so it is
  never the default answer to a quiet stretch. Same anti-pattern *Posture* and
  *Failure modes worth naming* already carry: decorative idle motion added to
  make a frozen scene score better on a metric instead of earning a real beat.

**The entrance-signature rule.** Count a tween's signature as **(the set of
properties it animates + its *effective* ease)**, where *effective* is the
load-bearing word: an ease inherited from
`gsap.timeline({ defaults: { ease } })` is as much a signature as one written
on the tween. **A majority of a project's real tweens sharing one signature is
the template failure regardless of how varied the content is** — and counting
only explicit `ease:` strings misses it completely. Confirmed case:
`videos/ectoin-survival-molecule/` declares `defaults: { ease: "power3.out" }`
on **29 of 29** scene timelines; 8 explicit plus 120 inherited is **128 of 196
real tweens (65%)** on one ease, and **69 of 122 opacity tweens also move
x/y** — the canonical fade-and-rise — against 47 pure fades. Grepping that
project for `power3.out` returns 8 hits and would have reported variety.

Unlike cadence, this is a legitimate **source-level** check — entrance variety
genuinely is a property of the source, where a source-level beat map is only
ever a hypothesis about pixels (*Verification loop*). Run it at authoring time,
before the render exists.

### The image plate component

Every image in a composition uses this shape. See the asset protocol below for
why each line is non-optional — and note this applies to every `<img>` added
at any point in the build, including a late B-roll insert; a plate added in a
later review pass is exactly where these attributes get silently dropped.

```html
<figure class="media-plate" style="--ar: 16 / 9;">
  <img src="assets/images/plates/centella-01.jpg"
       alt="" width="1920" height="1080"
       loading="eager" decoding="sync">
</figure>
```

```css
.media-plate {
  aspect-ratio: var(--ar, 16 / 9);
  width: 100%;
  overflow: hidden;
  background: #1A1A1A;          /* layout holds if the file 404s */
  position: relative;
}
.media-plate img {
  width: 100%;
  height: 100%;
  object-fit: cover;            /* cover or contain — never unset */
  display: block;
}
```

## Asset protocol — images

**Before generating or licensing a single new plate, check whether the
project already has one.** Many projects maintain (or point to) a shared
catalog of previously sourced/generated imagery and reusable components. Find
it via the *Catalog lifecycle* section above — don't stop at a `CLAUDE.md`
that never names the location and conclude one doesn't exist; that specific
silent failure is documented there because it already happened for real.
Search it first: a plate that's already sourced, licensed, and proven in a
prior render is strictly better than a fresh generation — faster, avoids a
second unlicensed near-duplicate of the same subject sitting in two places,
and lets a visual motif recur across a channel's videos on purpose instead of
by luck. Generate a new plate only when the catalog has nothing usable for
the beat; note in the project's own asset manifest which plates were reused
vs. newly made so the next project can find them too. This check belongs at
production-loop step 4 (asset manifest), before any generation call — not as
an afterthought once a new image already exists. A catalog with reusable
*visual components* (not just plates) gets the same treatment, one step
later — see production-loop step 5. The two are easy to do only half of:
checking for reusable imagery while never looking at whether a scene's actual
*mechanism* — its layout pattern, its motion structure — already exists
somewhere reusable too.

Images are the single largest source of renders that "succeed" while looking
broken. Four rules, all mandatory.

1. **Explicit dimensions, always.** Never emit an `<img>` without a constrained
   box: CSS `width` + `height`, or `aspect-ratio` on the container. An
   unconstrained image reflows the layout at the moment it decodes, which lands
   on a different frame each render — the layout pops and deterministic timing
   breaks. Set `width`/`height` attributes on the tag as well so the box is
   reserved before decode.
2. **Always declare `object-fit`.** `cover` when the plate is a background or
   fills a cell, `contain` when the whole subject must stay visible (product
   shots, diagrams, logos). Never leave it unset — the default stretches and the
   distortion is subtle enough to survive a quick preview and ship.
3. **Every image container carries a fallback background.** `background: #1A1A1A;`
   on the wrapper, or the composition's own dark neutral. If a path fails, the
   frame shows a deliberate block in the right place instead of a collapsed
   layout, and the failure is visible in frame extraction rather than silent.
4. **Project-local, resolvable paths.** Use the project's `assets/` root
   (resolved by `hyperframes.json`'s `paths.assets` / `media.autoProxy`) — a
   path like `assets/images/plate_01.jpg`, relative to the composition file or
   the resolved root the project's own docs specify. Do not invent an absolute
   filesystem path (`file:///mnt/...` or similar); it will not exist on the
   machine actually rendering. During drafting, use an explicitly declared
   placeholder and mark it — never leave an invented path that looks real.
   Remote URLs are draft-only: they add network variance to a render that is
   supposed to be deterministic.

Also: `decoding="sync"` and `loading="eager"` on every plate. Lazy loading and
async decode are both wall-clock behaviours in a renderer that does not wait.
Font loading is normally handled by the engine's own injection (see *Canonical
patterns*) — confirm it in the check log rather than hand-rolling `@font-face`.

Beyond the four dimension rules above, four more rules govern content and
treatment, not just markup correctness:

5. **No raw static plate.** Every image gets a restrained treatment — a zoom,
   reframe, depth shift, reveal, or parallax (see the Ken Burns pattern in
   *Consuming `--p` in CSS* above) — never left motionless for its full
   on-screen duration. A still image with zero applied motion is the same
   defect class as a frozen scene, the thing the *Verification loop*'s
   static-hold check exists to catch.
6. **A real tactile/photographic anchor early, not a fixed quota.** At least
   one real photographic or tactile plate — skin, texture, a product, the
   actual ingredient — lands in an early beat, not only in late B-roll. When
   a topic genuinely has nothing to photograph and the video is fully
   illustrated instead, that's a legitimate call, but record the reason in
   the beat sheet; an all-illustrated video that never considered the
   alternative is what makes faceless content read as an animated report
   rather than a video. A fixed percentage-of-beats quota doesn't survive
   contact with a real topic mix — the reason-recorded exception does the
   same job without an arbitrary number.
7. **One mechanism per diagram, three important labels max.** A diagram
   explains a single mechanism per beat and carries at most three important
   labels. A dense, multi-label dossier-style diagram is unreadable at phone
   scale before it's even a content problem — see the *Phone-scale
   legibility check* below.
8. **A diagram is not a chart unless it plots real data.** Chart grammar —
   axes, gridlines, a plotted line or point — implies a measurement behind
   it. An illustrated mechanism borrowing that grammar without real data
   reads as a fabricated result; keep illustrations visually distinct from
   data visualization (see *What must never reach a rendered frame* above).

## Audio is a first-class composition layer

The composition is **not silent by default** — narrated faceless video is the
common case, and HyperFrames renders audio *with* the video, in-markup, not as
a post-render mux step. Treat audio with the same rigor as visual motion:
every clip has a declared position, group, and gain; nothing is dropped in
loose or "figure it out at mix time."

```html
<hf-audio-group id="voiceover"
  data-fx-chain='[
    {"type":"highpass","freq":90},
    {"type":"peaking","freq":150,"gain":1.5},
    {"type":"compressor","threshold":-22,"ratio":3},
    {"type":"peaking","freq":3000,"gain":1.5},
    {"type":"peaking","freq":6500,"gain":-4,"q":3.5}
  ]'>
  <audio src="assets/voice/01.wav" data-start="0.2" data-track-index="10"
         data-audio-group="voiceover"
         data-automation='{"volume":[[0,0],[0.08,1],[6.9,1],[7.0,0]]}'></audio>
  <!-- one <audio> per VO line, same group, same fx-chain -->
</hf-audio-group>

<audio src="assets/bgm/track.mp3" data-start="0" data-track-index="1"
       data-volume="0.35"
       data-fx-carve='{"sources":["voiceover"],"strength":0.25}'></audio>

<audio src="assets/sfx/whoosh.wav" data-start="3.15" data-track-index="20"
       data-volume="0.35"></audio>
```

Rules:

- **Buses, not loose clips.** Group every VO line into one `<hf-audio-group>`
  carrying a shared `data-fx-chain` (a voice-warm EQ/compressor/de-ess chain
  is a reasonable default; confirm the project doesn't already define one to
  reuse). Reusing a bus chain verbatim across a channel's videos is a
  legitimate consistency win, not laziness.
- **Fade every clip's edges.** An 80–120ms `data-automation` volume fade
  in/out on every VO and SFX clip avoids a click at the cut point.
  Un-automated SFX are the most common miss — add the fade even on a
  "one-shot" sound.
- **`data-automation`'s exact JSON shape drifts by pinned version — don't
  trust the snippet above blindly.** Confirmed on `hyperframes@0.8.17`: the
  flat `{"volume":[[t,v],...]}` shape shown above is rejected outright
  (`Unsupported automation version: undefined`), and — worse — only at
  `npm run render` time; `npm run check` accepts it silently on that version,
  so a lint-clean project can still fail to render. That version's real shape
  is `{"version":1,"lanes":[{"target":"volume","points":[{"t":0,"v":0},
  {"t":0.08,"v":1},...]}]}` — versioned, `points` as `{t,v}` objects not
  tuples, and an explicit lane `target`. If `npx hyperframes docs
  data-attributes` doesn't cover automation (it didn't on 0.8.17), grep the
  installed CLI's own bundled output for the exact error string (e.g.
  `grep "Unsupported automation version" $(npm root)/.../hyperframes/dist/cli.js`
  or the equivalent path under the npx cache) to read the real validator
  instead of guessing from this file.
- **A `data-automation` volume lane can REPLACE `data-volume` instead of
  multiplying against it — verify which, per engine version, before shipping
  a fade.** Confirmed on `hyperframes@0.8.17` by reading its own
  gain-resolution code: when a "volume" automation lane exists for a clip,
  its interpolated value *is* the final gain outright; `data-volume` is only
  used as a fallback when no automation exists at all. Writing a fade's
  "full volume" plateau as `v:1` — reasonable if you assume it means "100% of
  `data-volume`," the way a normal envelope-times-fader model would work —
  instead makes the clip play at full unity gain for that entire plateau,
  regardless of its `data-volume`. This is **silent**: no lint error, no
  render warning, nothing — a BGM bed at `data-volume="0.12"` rendered ~10dB
  hotter than intended and only surfaced when a human listened to the file
  and said the music sounded very loud. The fix is to write each clip's real
  intended level as the plateau value (`v:0.12` for that BGM, not `v:1`), not
  a normalized `0`-to-`1` envelope. After adding *any* volume automation,
  A/B the actual rendered loudness (`ffmpeg astats` RMS in a window with no
  other source active) against a same-window render from before the
  automation existed — matching envelope shape on a scrub is not enough
  evidence; the absolute level can be wrong while the shape looks perfect.
- **BGM ducks under VO, not the reverse.** `data-fx-carve` (sidechain-style
  ducking against the voiceover group) is how BGM steps back during
  narration; set the strength low enough that music stays audible as texture.
- **For a short's engineered loop (see *The hook*), the mix must be live at
  both boundaries, not just the picture.** A stock BGM bed's own tail fade is
  authored for that bed's original, longer running time — reused unmodified
  under a shorter cut, its fade-out can land well before the video actually
  ends, so the last second or two plays in near-silence even though the file
  is technically still "the BGM track." Check by measuring RMS across the
  final ~2s of the mix, not by trusting that a bed marked `.loop.` or a
  filename implying it's loop-safe was cropped to this edit's actual length.
  Re-cut the bed to the real duration with a short (~150-250ms) declick fade
  at each end instead of inheriting whatever fade the source file shipped
  with — confirmed necessary on a render where a stock bed's 4.5s tail fade
  left the final 1.6s of a 34s short at true digital silence.
- **SFX spotting is its own pass.** Trim every SFX file to its beat — a stock
  SFX that runs 1.5s longer than its visual beat will audibly drone into the
  next scene; this is caught only by listening past the cue, not by looking
  at its start time. Before adding a "new" SFX from a library, hash-compare it
  against assets already in the project — duplicate files under different
  names are a common and wasteful mistake. After any retiming pass, re-measure
  true peak on the final mix; a clip nudged by 100–200ms can push the mix from
  comfortably under a limiter to clipping.
- **No render-time loudness normalization.** The engine renders the mix as
  authored; it does not apply loudness targets. Master to YouTube's ~-14 LUFS
  integrated / -1.5 dBTP target as a **separate post-render step** (two-pass
  `ffmpeg loudnorm` on the exported MP4, video stream copied through
  unchanged) — do not assume the render already did this.
- **Captions are a separate deliverable, not a mux side-effect.** Full
  workflow — transcript generation, proper-noun correction, burned-in vs.
  `.srt`, competitive research, verification — is in *The captions* below.
  One thing worth flagging here since it's an audio-pipeline gotcha rather
  than a captions-authoring one: Whisper-class transcription models can
  hallucinate a trailing cue past the true end of the audio; check the
  transcript's last timestamp against the file's real duration before
  handing it off to the caption-authoring step.
- **A synthetic voice will mispronounce domain terms.** If TTS says an
  acronym or coined term wrong (a technical acronym spoken as a word, a
  brand name stressed incorrectly), fix it by respelling the *TTS prompt*
  phonetically, not by changing the on-screen text — the two can and should
  diverge (VO says "en-see-eye", on-screen still reads "INCI").
- **A fade cannot fix a clip with no tail.** Before lengthening a fade-out to
  smooth an abrupt cutoff, run `ffmpeg silencedetect` on the raw clip and
  confirm real trailing silence actually exists past the last word. If the
  file's last sample is still mid-word, the take itself needs to be
  re-recorded with room to decay into — a longer automation fade applied to
  audio that's still live at end-of-file just mutes an active word faster,
  which reads as a different flavor of abrupt, not as a fix.

### Re-timing cascade — what one VO change actually touches

Because scene timing is normally derived from measured VO clip durations (not
authored up front and hoped to fit), a single script change — even inserting
one new short scene — cascades further than it looks:

1. Every scene `data-start` after the change point.
2. Every transition overlap window on the root timeline — the extended
   outgoing `data-duration`, the pulled-forward incoming `data-start`, the
   `data-track-index` ping-pong and the stamped `T`. One retime re-derives all
   four; moving the scene start alone leaves the tween firing over the wrong
   pair of wrappers.
3. Every SFX clip's `data-start` in scenes after the change point.
4. The BGM's loop/slot length and its `data-fx-carve` timing if it's phrase-synced.
5. The root `data-duration` and its anchor tween.
6. The project's own storyboard/spec document (STORYBOARD.md or equivalent) —
   re-derive its timing table from the actual `index.html`, don't hand-edit
   estimates. A drifted storyboard stops being useful as a spec the moment one
   real timing changes and the doc isn't re-synced.
7. **The audio master, which a re-render silently resets.** Mastering is a
   post-render step (*Audio mastering*), so a fresh render carries the mix at
   whatever level the composition produced and none of the loudness work.
   Confirmed: a re-render measured **-24.2 LUFS** against the previous
   deliverable's **-14.6**, a 9.6 LU gap, on a file that was otherwise ready
   to ship and was about to be handed over as the publish candidate. Nothing
   in the render output says so; only `ffmpeg ebur128` on the new file does.
   Re-master after every re-render, and re-measure the shipped file rather
   than assuming the pass ran.
8. Any in-scene motion beat hand-timed against a *specific VO word's*
   timestamp — a chip that appears on "because," a stagger that lands on a
   clause. A new take's word timings rarely fall at the same offsets as the
   old ones, even when the scene's own start/duration don't change (a
   re-recorded final line changes nothing upstream but still desyncs every
   beat inside that one scene). Re-derive each beat's trigger time from the
   new transcript; don't assume the old relative offsets still land on the
   same words.

Treat a mid-build script edit as "this touches N files," not "this touches one
line," and budget for it.

**The cascade runs in the other direction too: a motion edit can orphan an
SFX cue.** The list above starts from a script/VO change; the same
dependency exists when a *visual* beat is removed or retimed with no
script change at all — e.g. an entrance stagger deleted to fix a
blank-frame finding. Confirmed case: three card-entrance SFX clicks kept
firing at their original timestamps after the card entrances themselves
were removed (all three cards changed to settle at frame zero instead),
leaving three clicks with no corresponding visual event. Any pass that
deletes, merges, or retimes a visual beat needs the same SFX-spotting
re-check as a VO change — grep the scene's `data-start` audio cues against
what actually still animates at each of those timestamps.

## Is the file you are about to edit generated?

Ask before the first edit, not after the next build. A mature project in this
repo generates its compositions: one script emits `index.html` from a scene
table, another emits every `compositions/frames/*.html` from a spec module.
Editing the output looks like it worked — the change is on disk, the render
shows it, `check` passes — and the next `npm run build` silently discards it.

Confirmed the expensive way: a payoff-line fix and a 28-boundary transition
system were both authored into generated files first. Neither would have
survived. The tell was in `package.json` all along (`"build": "python3
scripts/build_frames.py && python3 scripts/build_index.py"`), and one `grep -n
"write_text\|\.html" scripts/*.py` would have shown which files each script
owns.

Two habits close it:

- **Grep the build scripts for the file you are about to touch** before you
  touch it. If a generator writes it, edit the generator and re-run.
- **Diff the regenerated output against what you verified.** After moving both
  fixes into their generators and re-running the build, the emitted
  `index.html` differed from the hand-edited one only in comment wording, and
  the scene file was byte-identical — which is the check that the generator
  actually reproduces what you looked at, rather than something close to it.

The inverse of this file's find-and-replace rule (*verify against the
generated file, not the generator*) is not its opposite: verify output, edit
source. Both halves are needed, and a project can be generated in one layer
and hand-authored in another — here scenes 01-07 and 08-29 came from two
different generators, and a third script consumed both.

## Layout validation and debug strategy

Layout cannot be verified by looking at the code, so the code has to be built in
a form where correctness is derivable and errors are visible in one screenshot.

**Grid/Flex inside every clip, always.** `.clip { position: absolute; inset: 0 }`
is the sanctioned stacking mechanism (mandatory rule 2) — everything *inside*
one clip's content is Grid or Flex. If the main composition of a scene depends
on two elements each getting an independent absolute `top`/`left`, it is
wrong: it will not survive an aspect-ratio change, a font substitution, or a
longer string, and each of those failures shows up only after a render.

**Spatial chain-of-thought — required before any HTML.** Write three bullets
naming the structural plan, then write markup. No exceptions, including for
"simple" scenes.

> - Scene 2 is a flex column, `justify-content: center`, full-bleed height.
> - Kinetic type stack fills the safe column top-to-bottom with real vertical
>   rhythm — not a single line centered in a mostly-empty canvas.
> - The drifting source chip is the one element that gets its own absolute
>   position, floating over the flex column as a motion layer.

**The debug overlay.** When asked to validate a layout — or any time a layout
is in doubt — ship a togglable debug state on the composition's own root
element so the operator can verify bounding boxes and safe-area zones at a
glance, without editing anything first:

```css
#root.debug-layout * { outline: 1px solid rgba(255, 0, 0, 0.6) !important; }
#root.debug-layout .clip { outline: 2px solid #00E5FF !important; }
#root.debug-layout .media-plate { outline: 2px solid #FFD400 !important; }

/* Shorts safe-area overlay — see "9:16-native composition" for the numbers */
#root.debug-layout::after {
  content: ""; position: absolute; inset: 0; pointer-events: none;
  background:
    linear-gradient(to left,  rgba(255,0,168,.25) 15%, transparent 15%),
    linear-gradient(to top,   rgba(255,0,168,.25) 20%, transparent 20%),
    linear-gradient(to bottom, rgba(255,0,168,.25) 10%, transparent 10%);
}
```

Toggle it with a class on the composition's own `#root` (not `<body>` — a
sub-composition's renderable surface is its `#root`, and that's what an
operator inspecting one scene in isolation will actually see). Confirm the
class is off before the real render by checking frame zero — a debug-tinted
export is a shipped bug, not a style choice.

## Catalog lifecycle: discover, reuse, build, contribute

A shared catalog only compounds in value if the loop actually closes. Three
failure points break it, and each has already happened in a real project
this skill was built against — not hypotheticals, confirmed cases:

1. **Discovery silently fails.** "Check the project's `CLAUDE.md` for where
   the catalog lives" (see *Asset protocol* below) is a real, useful
   instruction — but it's a dead end if `CLAUDE.md` never names the
   location. Confirmed across an entire real repo: the root `CLAUDE.md`
   gestured at "check for existing sourced imagery" without naming a path,
   and not one of ten per-project `CLAUDE.md` files named the catalog
   either. An agent following the instruction literally would reasonably
   conclude no catalog existed. One did — nineteen documented entries.
   **Don't stop at `CLAUDE.md`.** If it doesn't name a location, still check
   for a conventional one — a top-level `catalog/`, `component-library/`, or
   similarly-named directory sibling to the video projects — before
   concluding there isn't one. Its own `README.md`, or a browsable
   `index.html` if it has one, settles the question in one read.
2. **Reuse gets skipped even after discovery succeeds**, when the catalog is
   checked for images but not for *mechanisms*. Confirmed in the same real
   project: a full-frame term/definition card was independently
   reimplemented from scratch five separate times across five different
   videos — identical class names, identical tokens, identical
   choreography — because each build checked for reusable imagery and never
   asked whether the scene's actual *structure* already existed somewhere
   reusable too. Component check (production-loop step 5) exists
   specifically to close this gap; give it the same weight as the image
   check, not treat it as optional.
3. **Nothing closes the loop at the end.** A video can discover the catalog,
   reuse what's there, and build cleanly, and still leave the catalog
   exactly as impoverished as it started if whatever new, genuinely reusable
   mechanism it built never gets harvested back. Catalog contribution
   (production-loop step 12) exists to make this a required closing step,
   not a someday-maybe: the same real project had a second component (a
   ranked list split by a cutoff line) that was built once, never
   generalized, and sat undiscoverable in one video's own folder until a
   dedicated review found it by grepping every composition's class
   names — which should never be the mechanism by which a catalog grows.

**What's worth harvesting.** A mechanism — real choreography, a real data
contract, or both — not every reusable-looking `<div>`. A three-line CSS
chip isn't a catalog entry; a card that cycles through a data array with a
shared animation contract is. A component doesn't need to have been reused
more than once to qualify — a single well-built, genuinely topic-agnostic
mechanism is worth extracting on its own merit.

**How to harvest, if the project doesn't already have its own convention.**
One self-contained entry: the component's markup/CSS/timeline, kept
render-safe per the mandatory rules above (a paused, seekable clock — never
autoplaying CSS, which defeats the entire point of cataloging something
meant for a deterministic render). Document, briefly: why it's here (what
called for extracting it, not a justification invented after the fact), its
field/data contract if it takes one ("swap this array" is worth one line),
and its status (validated reference vs. wired into a real render pipeline).
Use generalized sample content, not the source video's real content
duplicated into the catalog — the point of a shared component is that the
content is exactly the part that changes per use.

**A browsable catalog is worth more than a folder listing**, once a
project's catalog is large enough to need one. Group entries by what kind of
thing they fundamentally are (a data-driven component vs. a static graphic
vs. raw photography vs. a pointer to a project that already has a proper
home) before grouping by topic or status — status alone
("draft"/"final") doesn't tell a reader whether something has a time axis at
all, and that distinction is what actually determines whether it can be
reused or only looked at. For anything with a time axis, surface its
duration and field contract *before* anyone has to open the file, and if
it's gated behind a debug flag to reveal its own scrubber, don't make a
future reader discover that flag by accident — load it pre-applied.

## Production loop

Follow this order; skipping ahead is what produces expensive rework.

1. **Catalog discovery.** Before writing a single beat, inventory what the
   project's shared catalog already has — components (with duration, control
   type, and field contract if it documents them), reusable imagery, marks.
   See *Catalog lifecycle* above for how to find it even when `CLAUDE.md`
   doesn't say where it is, and read the catalog's own index/README directly
   rather than re-deriving what exists from memory or a partial grep. This
   pass is what turns steps 4 and 5 below into decisions instead of blind
   searches, and it can genuinely shape the beat sheet itself — a beat built
   from an existing, proven component is a different creative decision than
   one built from nothing.
2. **Beat sheet before markup.** Duration, aspect, fps, and a numbered list of
   beats with a one-line intent each. A beat is a visual state, not a sentence.
   Read the YouTube delivery section first — hook, chapters, end-screen scene,
   cadence targets, and caption timing are beat-sheet inputs. **Default a
   short's duration to 28-45s.** Past 50s, record the storyboard reason in
   this beat sheet — a runaway duration is almost always VO-driven timing
   letting the script sprawl past its own structure (see the *re-timing
   cascade* section above), not a deliberate choice, and 14 of this
   channel's 23 shipped shorts already run past 50s with no such reason on
   record. **A long-form beat sheet carries two more columns: a camera path
   and an actor map.** The camera path assigns each act a zoom level in one
   continuous space; the actor map names every beat's subject and marks the
   runs where consecutive beats share one. Both belong here because the actor
   map *is* the file split (step 7), and deciding it after the markup exists
   means rewriting the markup. See *Long-form structure*.
3. **Choose the presenter.** With no face and (often) live narration, something
   has to carry attention: type, a moving diagram, a photographic plate, or a
   data object. Pick one per video. Videos that switch presenter mid-way read
   as compilations.
4. **Asset manifest.** Cross-check the beat sheet against step 1's discovery
   pass and reuse what already exists before generating anything new (see
   *Asset protocol* below). Every image, font, audio file, and generated
   plate listed with its source and licence status, resolved to
   project-local paths, noting which were reused vs. newly made.
5. **Component check.** Cross-check each scene's planned mechanism against
   step 1's discovery pass, not a fresh search — a catalog that organizes
   reusable presentation patterns separately from raw plates (a confidence
   meter, a graded badge, a split-comparison diagram) is telling you those
   mechanisms are meant to recur, the same way a plate is. Check each
   candidate against the actual beat's content, not just its category
   label — a component built for one specific comparison is not a generic
   "split screen" just because it visually resembles one; read its own
   code/spec before adapting it, and skip it honestly if the content doesn't
   actually match rather than forcing a fit. When nothing fits, that's a
   legitimate outcome — but it has to be the result of checking step 1's
   inventory, not of never having looked. Where a real match exists, adapt
   the component's *mechanism* rather than wiring in its literal skin, and
   note in the manifest which components were reused/adapted vs. built new —
   what gets built new here is exactly what step 12 later asks you to look
   back at.
6. **Spatial plan.** Three bullets per scene naming the Grid/Flex strategy
   before any markup exists. See the layout section. For long-form this is
   also where an actor-continuous run collapses into **one merged
   sub-composition** with internal phase divs rather than one file per
   narration sentence (`hyperframes-core`'s composition-patterns §"C.
   Multi-scene merge") — actors rearranged between phases, not redrawn.
7. **Composition skeleton.** Scenes and timing wired with the engine's real
   timing attributes. Get the structure seeking correctly before any styling.
8. **Layout check with the debug overlay on.** Verify bounding boxes and safe
   areas, then turn it off.
9. **Motion pass.** Add easing, stagger, and camera. One idea at a time. Budget
   beats across the *whole* scene, not just its opening two seconds — a scene
   that lands three beats immediately and then holds for the rest of its
   narration duration fails the cadence target just as hard as a scene with no
   beats at all. See *Cadence* below. **Pick each beat's idiom from what it is
   doing narratively** (*Motion idiom by narrative function*), not from the
   canonical `.beat` shape, and don't set one timeline-wide
   `defaults: { ease }` for every tween to inherit. **Author the
   `*.motion.json` sidecar in this same pass** — assertions on the copy
   elements, one `keepsMoving` per scene with `maxStaticSec` from this
   format's cadence budget. Written later it documents what the composition
   happens to do, not what it was supposed to do.
10. **Lint and preview.** Use the project's real preview/check tooling (e.g.
    `npx hyperframes preview --background`, `npm run check`) and scrub by
    dragging the seek position, not by playing — dragging is what exposes
    non-seekable animation. `check` picks up step 9's sidecar on its own —
    no flag — so confirm the report says a sidecar was found and scale
    `--samples` to the piece's length before reading a clean pass as one.
11. **Render, then extract frames and inspect.** Check frame zero, every
    scene's settle frame, every transition midpoint, and the last frame. See
    *Verification loop* for the two checks a passing lint cannot substitute for.
12. **Catalog contribution.** Look back at what step 5 built new and ask: is
    any of it reusable beyond this video — a mechanism, not just a one-off
    scene? If yes, harvest it into the shared catalog now, following
    *Catalog lifecycle* above, not "eventually" — a component left in one
    video's own folder is invisible to the next video the exact same way an
    uncataloged one already was. Not everything qualifies; harvest a real
    mechanism, not every reusable-looking div. A component reused verbatim
    from the catalog needs no new entry here.
13. **Publish envelope.** Title, thumbnail, captions, chapters, end screen
    targets, pinned comment — see the YouTube delivery section (*The
    thumbnail* and *The captions*). All of these are part of the video, not
    afterthoughts, and none is optional: a finished render with no captions or
    no thumbnail is not a done project, the same way a render with no audio
    mix would not be considered done. Close this step by reporting *The
    delivery manifest* — every asset above, by its real path, not left for
    the operator to go find.

## Pre-render gate

A binary checklist, run before calling a render final. A passing lint/check
and a rendered file are necessary but answer none of these — a clean
`npm run check` and a "no" on any item below is still a reject, not a note
for next time:

1. **Is the hook legible from a single silent frame at ~0:01?** See *The
   hook* below — frame zero is the hook, already composed.
2. **Is every important label readable at phone scale?** Run the
   *Phone-scale legibility check* below, not a full-size eyeball pass.
3. **Does every scene have one dominant focal point?** Not two competing
   ones — see *9:16-native composition*'s depth-roles rule below.
4a. **Does the motion explain something** — a relationship, a
    transformation, a comparison, a cause — rather than decorate? See
    *Posture*'s "motion that means something."
4b. **Does every scene show measurable pixel change at the cadence target
    across its WHOLE duration**, not just somewhere in it — checked with any
    burned-in caption layer cropped out of the diff (see *Verification
    loop*'s static-hold check)? Item 4a asks whether the motion that exists
    means something; this asks whether motion exists for the full hold, not
    just its opening beats. A source-level beat map or a clean
    `npx hyperframes check` cannot answer this — an authored tween is not a
    pixel change, and layout/motion linting has no cadence dimension.
    Confirmed case: `videos/snail-mucin-recut-34s` passed `check` with 0
    errors while 4 of its 6 scenes sat frozen for 2.0-7.5s at a stretch —
    one scene (a 3-item list) was static for 7.5 of its 8 seconds, and the
    project's own report had separately (and wrongly) claimed clean cadence
    based on the source-level beat map alone. Run the render-level diff
    before checking this item off; a passing 4a on an early beat says
    nothing about second 6 of an 8-second scene. **"Not frozen" and
    "adequately paced" are different questions, and a project's own
    `check-static-hold.py` copy typically only answers the first** — its
    `PSNR_FROZEN_DB` threshold (a project-specific value, commonly ~55dB)
    only fires on near-pixel-identical consecutive samples; a scene can
    report "0 findings" while 94% of its frame-to-frame steps carry no
    meaningful change, because sub-perceptual drift keeps breaking the
    "frozen" run before it reaches the cadence ceiling. Add a real cadence
    check as a second, distinct metric: sample at ~8fps, compute mean
    `|Δluma|` per step across the whole frame, and count what fraction of
    steps clear a real-but-low threshold (~1.0 on a 0-255 scale is a
    reasonable starting point — tune per project, but confirm it separates
    real beats from hard cuts, since cuts alone can measure 100+ per step
    and swamp a threshold set too low). A whole-video active-step share
    under ~10-15% is worth a second look regardless of what `check`
    reports; three consecutive scenes with near-zero internal motion is
    the pattern that produced this rule. **Two limits on that share.** It
    is *portrait-derived* — both comparators behind it are 9:16 (11.7%,
    23.1%), while the same beat vocabulary in landscape measured 4.0%
    before a fix pass and 5.8% after (*16:9-native composition*). And it
    is **structurally blind**: `videos/ectoin-survival-molecule/` measures
    **12.7%** (344 of 2703 steps) on the shipped render — above one shipped
    9:16 comparator and well under the other — and still read as slides,
    because all 29 of its scenes had the same enter → wash → hold shape.
    The share says how much changed, never whether it changed differently
    from the last scene; that question is item 14. **Measure this on the
    file you are shipping, and do not trust a number the project already
    wrote down**: that project's own `DELIVERY.md:53-58` records 14.8%,
    written eleven minutes *after* the render it describes, and re-running
    the project's own unmodified script against the shipped MP4 returns
    12.7%. A stale recorded figure is indistinguishable from a fresh one.
5. **Is there a real photographic, tactile, or product-specific visual
   early in the video**, rather than a fully illustrated/typographic open
   by default? See the tactile-anchor rule in *Asset protocol* above.
6. **Are palette, type, captions, and any channel mark consistent** with
   the rest of the channel? See *Consistency across a channel's videos*.
7a. **Are safe-area tokens actually consumed by every scene**, not declared
    in one file and hardcoded elsewhere? Measured gap on this channel: only
    6 of 24 shipped projects reference `--safe-*` tokens at all. See
    *9:16-native composition* below.
7b. **Is there no RENDERED pixel inside a reserved zone**, measured against
    the actual output rather than inferred from 7a? A scene can pass 7a in
    full — every token declared, consumed, individually correct — and still
    ship ink past the real line once a transform (a Ken Burns scale, an
    entrance transform's transient) sits between the padded box and the
    canvas; 7a is a source-code question and structurally cannot see this.
    Run the *Verification loop*'s safe-area intrusion scan against the real
    render, not a visual scrub — the confirmed case that made this its own
    gate item overshot by only 5-10px, well under what a human eyeballing
    the preview reliably catches.
8. **Does a real sidecar caption file exist** — not a same-named but
   unrelated file (see *The captions*' naming note below) — alongside the
   burned-in track? Measured gap: only 4 of 24 shipped projects ship one.
9a. **Are all on-screen citations real and human-readable, with no internal
    IDs?** See *What must never reach a rendered frame* above.
9b. **Does every on-screen claim/instruction stand on its own in plain
    language, independent of whether its citation is understood?** Distinct
    from 9a, which checks the citation's own format — this checks the
    *claim sentence* next to it. Read each headline/qualifier/instruction
    against the project's own stated audience and ask whether it requires
    clinical vocabulary to act on correctly; a citation pill is allowed to
    stay terse (`Journal · Year`, a regulation code) exactly because it's
    provenance, not the instruction itself. See *What must never reach a
    rendered frame*'s "untranslated clinical/technical register" entry.
10. **Are there no placeholders, unfinished text, or debug-overlay
    artifacts in frame?** Same section as above.
11. **Is the closing beat one specific, lesson-tied action**, not a
    generic subscribe card? See *The hook* below and production-loop
    step 2.
12. **Does the video still make sense with the sound off?**
13. **If the piece isn't a recorded silent-by-design exception (see
    *Posture*'s "Silence is a genuine choice" below), does an actual mix
    exist and hit the mastering target** — not "the render has an audio
    track," but a real measured level? One `ffmpeg astats`/`ebur128` pass
    against the actual file settles this in one command; don't infer it from
    a manifest, a `data-volume` attribute in the source, or the render tool
    reporting success. This is the single cheapest disproof available for an
    external QC report's "completely silent" claim — cheaper than the
    frame-by-frame pixel work most of this section's other items need, and
    exactly the kind of claim the *Verification loop*'s fabricated-findings
    note already warns can be asserted without being true. Confirmed
    necessary: an external QC report claimed `videos/peeling-question-open`
    was "completely silent" when every one-second window across the render
    measured −19 to −14 dB RMS and the file was already mastered to −14.1
    LUFS / −1.5 dBTP — one command would have settled it before any deeper
    verification pass began.
14. **(Long-form) Does the piece pass a continuity audit** — four counts,
    all properties of the source, so run them before the render:
    (a) **boundaries by type** and how many change ground;
    (b) **entrance-signature share**, reported as two separate numbers
    because they answer different questions — the top *(properties +
    effective ease)* signature, and the top *effective ease* on its own,
    counting any inherited from `defaults: { ease }` (*Motion idiom by
    narrative function*); (c) an **actor-persistence map** — which
    subjects span consecutive scenes, and whether each is one merged
    sub-composition or two redrawings; (d) a **camera-move count**.
    `catalog/tooling/continuity-audit.py` keeps this check; (c) and (d)
    are heuristics, so confirm a finding on frames. Confirmed case:
    `videos/ectoin-survival-molecule/` fails all four — 28/28 cuts; a top
    signature of 26.0% but a top effective ease of **65.3%** across 29 of
    29 timelines; one rebuilt-actor pair and 0 merged scenes; 0 camera
    moves — while passing every other item here. Report both signature
    numbers: the ease share is the one that exposes a house template, and
    it is invisible if you only count explicit `ease:` strings (8 here). Item 4b measures *how much* changed; this measures whether
    it changed *differently from the last scene*, which is what "reads as
    slides" means.
15. **Is there one `*.motion.json` sidecar at the project root** — not one
    per scene, which is read by nothing — with assertions naming the **copy
    elements** rather than their containers, `keepsMoving` scoped to `#root`
    rather than to a scene, `maxStaticSec` set from this format's cadence
    budget rather than the 2s default, and `check --samples` scaled to the
    piece's length? `motion.enabled: false` means no sidecar was written,
    not that verification was switched off — see *Verification loop*.
16. **Is there no plain crossfade across a ground change, and has every
    transition midpoint been extracted and looked at** — `blur-crossfade`
    included, since it blends exactly as hard and only masks the clash?
17. **(Long-form) The slides test.** Is every *within-chapter* boundary
    carried by at least one of the three continuity mechanisms — a
    transition, camera continuity, or an actor persisting across it — and
    does every *chapter* boundary open on the next act's payoff rather
    than its setup? A boundary carried by none of the three is a slide
    change, however well-paced the scenes either side of it are.

## Verification loop

A lint/check pass and a rendered file are necessary, not sufficient. Four
specific failure classes survive a clean check and a manifest that says
"success" — the first two require actually looking at extracted frames, the
other two require checking things nothing in the render pipeline verifies on
its own: the publish envelope, and whether anything genuinely new got fed
back into the shared catalog.

**Static-hold detection.** A frozen-but-fully-populated frame looks identical
to a healthy one on any brightness/contrast/luma-variance metric — a scanner
that measures blankness cannot see it. Extract frames at a fixed interval
(~0.5-1s) across the whole render, diff consecutive frames, and flag any run
longer than the project's cadence ceiling (shorts: >2-3s with no measurable
pixel change) as a defect, not just a stylistic choice. This is what catches a
scene that lands all its beats in the first two seconds and then sits frozen
for the rest of its VO — a very common failure mode once VO-driven timing
makes scenes longer than their choreography.

A blankness scanner (luma stddev, catches an *empty* frame) and a static-hold
scanner (frame-to-frame diff or PSNR, catches a *frozen* one) are two
different tools that happen to sound alike — confirm which one a project's
own checker script actually implements before citing its clean output as
evidence in a doc. A project shipped with only the blankness variant can
truthfully report "0 findings" on a scene that's been frozen for five
seconds, because that's a defect class the tool was never built to see.

If the composition burns in captions or any other always-repainting overlay,
**crop that layer out before diffing.** A caption track's own word changes
register as constant motion and will mask a completely frozen scene
underneath it — the diff reads "alive" because *something* in the frame
changed, even though the actual content (the hero plate, the graphic, the
thing the scene is about) has been static the whole time. This is exactly
how a static-hold bug survives a human scrubbing the render, too: a person
watching sees the captions updating and reads the whole frame as in motion.

**The masking risk isn't limited to a caption track — any second on-screen
element can hide a dead hero region the same way, whole-frame diffing alone
cannot see it, and a per-scene checker script inheriting another project's
crop geometry is its own separate, confirmed failure mode.** Two distinct,
confirmed cases:

- A scene's own dominant/hero element (the thing gate item 3's "one dominant
  focal point" is actually about) can go fully **empty** — not just static,
  genuinely carrying zero content — while a *different, legitimate* element
  elsewhere in the same frame keeps animating and keeps the whole-frame diff
  "alive." Confirmed on `videos/peeling-question-open`'s `06-open.html`: the
  hero glass-panel sat empty for 1.30s between a word-grid's exit and a
  closing lockup's arrival, invisible to a whole-frame check because a
  closing headline couplet, in a different region of the same frame, kept
  animating throughout that exact window. This is a **third case**, distinct
  from both halves of the blankness-vs-static-hold split above: not an empty
  *frame* (blankness scanner's job) and not a frozen *frame* (whole-frame
  static-hold's job), but an empty *region inside an otherwise-alive frame*.
  Closing it needs a check that is region-aware — grid the safe content box
  and evaluate each cell's own content-then-empty transition, not just the
  frame as a whole; see `catalog/tooling/check-static-hold.py`'s region-aware
  half for a working (if still heuristic and imperfect — see its own
  documented false-positive classes) reference implementation.
- **A per-project copy of a static-hold checker script inheriting a SIBLING
  project's caption-band crop is a recurring, not a one-time, failure.**
  Confirmed twice in the same lineage: `peeling-not-progress`'s copy of this
  script originally inherited a different project's caption geometry while
  having no burned-in captions of its own — documented as CORRECTED in that
  script's own docstring. One project later, `peeling-question-open`'s copy
  of the *same file* still carried `mugwort-healing-herb`'s caption-band crop
  (`CAPTION_BAND_EXCLUDE = True`, specific pixel numbers) despite
  `peeling-question-open` having no burned-in captions at all — silently
  excluding a real scene's own kicker text from every diff it ran. The
  documented warning did not stop the recurrence: a comment describing a past
  bug is not the same as a check enforcing against it. Before trusting *any*
  project's "0 findings" from a copied static-hold script, confirm its
  `CAPTION_BAND_EXCLUDE`/crop constants against that project's own
  `index.html` — does a burned-in caption element actually exist at those
  coordinates? — rather than trusting the file's own inherited comment.
  **This has now recurred a third time in the same lineage**, confirming
  the pattern rather than being a one-off: a later project's own copy of
  the file carried a docstring literally naming a *different* project
  ("this project, peeling-question-open") even though the constants
  themselves (`CAPTION_BAND_EXCLUDE = False`) happened to be correctly
  re-derived for the new project. The provenance comment drifted; only
  luck kept the actual constant right. Since a comment demonstrably does
  not stop this, prefer a runtime assertion over documentation: have the
  script check, at the top of its own run, whether an element actually
  exists in the calling project's `index.html` at the configured caption-
  band coordinates when `CAPTION_BAND_EXCLUDE` is `True` (and conversely
  warn if a burned-in caption composition exists but the flag is `False`)
  — fail loud rather than silently trusting inherited constants.

**A QC script calibrated for one canvas does not merely mis-measure another —
it can report a clean pass on a defect it structurally cannot see.** Confirmed,
and worse than the caption-band inheritance bug above because no comment
anywhere would have caught it: `catalog/tooling/check-safe-area.py` and
`check-static-hold.py` both hard-coded `CANVAS_W, CANVAS_H = 1080, 1920` as
module constants with no override. Run against a 1920×1080 render they did not
error. Measured, on a fully-inked landscape frame:

```
bottom zone  mask[1536:, :]   -> shape (0, 1920)     sum=0        FAIL-OPEN
right  zone  mask[:, 918:]    -> shape (1080, 1002)  sum=1082160  wrong region
```

The bottom slice runs past the end of a 1080-tall array, so numpy returns an
**empty view** — the *hard gate* printed "no findings" and exited 0. The right
slice silently measured the right 52% of the frame instead of a 162px rail, so
the same run would fire spuriously on the other axis. A gate that fails open on
one edge and fails loud-but-wrong on another is worse than no gate, because its
clean exit is read as evidence.

Note what did **not** prevent this: the script's own docstring already said it
assumed a portrait canvas. Documentation of an assumption is not enforcement of
it — the same lesson the caption-band constants taught one section above, which
is why the fix here is an `ffprobe` dimension probe that **refuses to run**
(exit 2) on a mismatch, not a louder comment. Before trusting any gate's clean
result, confirm it actually measured the canvas you rendered.

A second, independent bug surfaced while testing that one, and it is worth
naming separately because it is the kind that hides inside a passing run: the
scene-boundary regex required a literal attribute order
(`data-composition-src` → `data-start` → `data-duration`). The repo's newest
project writes `data-start` first, so the scene list came back **empty** and the
region-aware check silently degraded to "treat the whole render as one scene" —
the exact mode whose own warning text says cross-cut false positives are
possible. Parse the tag, then pull each attribute out of it independently; never
assume authored attribute order, since nothing enforces it. Note a project's own
copy of a shared script may already carry an independent fix — this one's did —
so a bug in the shared copy does not automatically discredit that project's
published numbers. Check the copy in front of you before crediting or
discrediting a specific past measurement.

**A third bug, found by a reviewer asking why one finding crossed a cut, and the
most damaging of the three: a per-scene check can manufacture a false positive at
almost every boundary through nothing worse than integer truncation.** The
windowing read:

```python
i0 = max(1, int(scene_start * REGION_FPS))     # 13.200 * 4 = 52.8 -> 52 -> t=13.00s
```

`int()` truncates, so whenever a scene start did not land exactly on the sampling
grid the window opened **one sample early**, on a frame still showing the
*previous* scene. That frame set the run's "has content" flag, and the new
scene's legitimately-empty cell then read as "content, then empty" — a defect
invented by the measurement, at exactly the boundary the per-scene windowing
existed to respect. **711 of 936 `data-start` values across the repo (76 %) are
off the 4 fps grid**, so it fired at roughly three cuts in four; fixing it cut
one project's findings from 10 to 3 and removed another's entirely, with no real
finding lost. Use half-open `[start, end)` semantics — `math.ceil` on both
bounds — so a window holds only frames whose timestamp is genuinely inside the
scene.

Two lessons generalise past this script:

- **Check the arithmetic at the boundaries of a windowed measurement, not just
  its thresholds.** Threshold tuning gets all the attention; an off-by-one in
  frame-index conversion is invisible in the output, survives every threshold
  change, and produces findings indistinguishable from real ones.
- **A finding that spans a boundary the tool claims to respect is itself evidence
  of a tool bug**, and is worth chasing before explaining it away as content.

Corollary for reading history: an "N content-voids" count from before such a fix
is not comparable to one after it. Re-run rather than compare.

**And a third class, which no threshold tuning can reach: binary ink presence is
the wrong primitive for an element whose ALPHA is animated.** A card whose
background sits at `rgba(247,245,240,0.06)` at rest and `rgba(...,0.18)` while
highlighted straddles any fixed ink threshold, so its entire area enters and
leaves the ink mask on a legitimate highlight-then-release cycle while the
element never moves. Measured on a synthetic card: ink swings **26,576 →
111,044 (4.2×)** between those two alphas while edge density stays **flat at
6,116**; only genuine removal collapses both to zero. Hysteresis between
enter/exit ink thresholds does not save this — the swing dwarfs any sane gap.

Borders and glyph strokes survive an alpha change, so **require a structural
signal as well**: a cell counts as empty only when its ink delta is low *and*
its edge density has fallen to a small fraction of that scene's own peak. This
class fires on anything that dims, highlights, or pulls focus — an opacity
1 → 0.45 focus pull is the same shape as a card highlight — so a project using
any of those idioms will see it.

**And the payoff for keeping the region-aware check honest rather than deleting
it: it caught a real defect the ENGINE'S OWN auditor missed.** After two rounds
of fixing its false positives it flagged three cards as content-then-empty; frame
extraction showed they were rendering **completely blank**. The cause was a bare
text node — copy written directly inside a container rather than wrapped in an
element:

```html
<!-- wrong: the copy is a TEXT NODE, so `.wash ~ *` has nothing to match -->
<div class="card"><div class="wash"></div>Fragrance-free?</div>
<!-- right -->
<div class="card"><div class="wash"></div><span>Fragrance-free?</span></div>
```

A sibling selector that lifts content above an animated background can only
raise **elements**. A text node has nothing to carry `position`/`z-index`, so the
background paints over it and the card renders empty. `check`'s own
`text_occluded` pass caught the same mistake where the copy *was* wrapped, and
did not catch it here — which is the general lesson: **a layout auditor that
walks text elements is blind to text that never became one.**

Two things follow. Wrap copy in an element inside any container with an animated
background, always. And treat a content-void finding as worth one frame
extraction even after a run of false positives — the run is exactly what makes
the real one easy to wave away.

**A gate's own background estimator is an assumption, and on a hard gate a false
positive is worse than a miss.** The safe-area check took "page background" as
the whole-frame modal luma — fine while the ground is most of the canvas, wrong
the moment it is not. On a landscape scene with two ~45%-of-frame panels the
modal became a *panel* colour (151 against a true ground of 243), every margin
differed from "background" by 92 luma, and **all four reserved zones reported
100% ink** across 136 frames with nothing actually out of place. Deriving the
ground from the **median of the outer 4px border ring** fixes it, and is the
right reference precisely because reserved margins exist: the extreme edge is
page ground by construction in any composition that respects them.

Why this matters more than an equivalent miss: a hard gate that cries wolf gets
waved through, and the next wave-through is the real one. When a gate fails,
**check its assumptions against the frame before changing the composition** — the
first instinct here was to go hunting for the offending element, and there wasn't
one.

That was the fourth distinct defect found in one checker family in a single day
— attribute-order parsing, `int()` window truncation, ink-presence as the wrong
primitive for animated alpha, and the background estimator. The common thread is
worth more than any of them individually: **each assumption held for the portrait
Shorts the tool was written against, and broke on the first composition with
different geometry or a different colour distribution.** A checker inherited from
another format is not validated for yours until something in yours has actually
violated its premises.

**A hard gate's background assumption will break a second time, in the same
place, unless you fix the CLASS rather than the instance.** `check-safe-area.py`
derives "page ground" so it can call everything else ink. That estimator has now
been wrong twice, both times blocking a clean render:

1. the whole-frame modal, broken by a busy landscape frame (two 45%-of-frame
   panels made the modal a *panel* colour; all four zones reported 100% ink
   across 136 frames with nothing out of place);
2. the outer-border-ring median that replaced it, broken by a **transition
   frame** — which legitimately contains two grounds, so the ring goes bimodal,
   the median lands on whichever ground holds more of it, and the other ground
   differs from the reference everywhere it appears. Measured: the entire
   54×1920 top band reported as 103680px of ink at a timestamp where that band
   is uniformly luma 19, min == max, zero variation. 70 frames, all clean.

Both fixes were locally correct. What carried the bug forward was the shape of
the assumption — *there is one background* — surviving the rewrite. The third
version clusters the ring and treats a pixel as ink only when it matches no
ground, which is the first version that does not assume a count.

**On a hard gate, a false positive is worse than a miss**, because the
wave-through it earns is what lets a real one through later. So when a gate
fails, check its assumption against the frame before changing the composition:
here the first instinct was to go hunting for the offending element twice, and
both times there wasn't one.

**Two negative controls, not one, for anything that exits non-zero.** A gate
that only proves it can fail is not validated; neither is one that only proves
it can pass. The safe-area controls pin three behaviours: text in a reserved
zone must fail (the gate still works), **a bounded solid block must fail** (the
fix did not over-suppress), and two flat grounds meeting at a straight seam must
pass (the regression). The middle one is the one that catches a plausible wrong
fix — an edge-density or "does this region have internal detail" test passes
every synthetic case and silently waves through a solid graphic sitting in the
zone. A first attempt here excluded masked rows spanning the band edge-to-edge;
it read as principled, worked on the bands parallel to the seam, and failed on
the rails crossing it, where a flat ground bounded by the seam is
indistinguishable from content. The control caught it in one run.

**A checker's summary line is part of the checker, and it is where a coverage
gap ships as a false all-clear.** `check-static-hold.py` used to end with
*"Overall: clean (whole-frame and region-aware checks both clean)"* — which
reads as a verdict on the **render**, not on the two passes that ran. A region
that stays frozen while still *carrying* content is invisible to both: the
whole-frame diff stays alive on any other moving element, and the region pass
only looks for content-then-**empty**, which never happens. So a render with an
entirely dead scene printed "Overall: clean". Confirmed on a synthetic (a
populated region frozen for a whole clip beside an animating one) and
independently on another project's real known-broken repro.

The logic was right and the sentence was wrong, which is the general shape:
**state what was covered and what was not, and never let the absence of findings
render as a verdict.** A scope line costs nothing and is the difference between
"these two checks found nothing" and an all-clear the tool was never entitled to
give. Name the uncovered mode explicitly, so the next reader can go look for it
by hand instead of trusting the banner.

**Then validate the fix in both directions, and treat the negative result as the
weaker half.** After adding the structural signal, two real projects went to
zero findings; that is only trustworthy because a synthetic control — a
structured block genuinely removed at t=5.0 of a 12 s clip — was **still
flagged**, at the right time and in the right cells. A scanner reporting nothing
is exactly as suspect as one crying wolf, and the discipline this file already
demands of external QC reports applies with equal force to a checker
immediately after it has been "fixed."

**Source-level cadence measurement is an authoring-time aid, never a
substitute for the check above.** Extracting every GSAP tween position from a
scene's own `<script>` block is the fast way to get a rough cadence read
*before* a render exists — but it measures authored beats, not pixels, and an
authored beat is not the same thing as a pixel changing. A naive extraction
also silently under-counts anything authored as a multi-line `fromTo()` call
or via a named helper function (`ytCameraMove(tl, target, at, {...})`,
`ytDefocusPulse(...)`) if it only pattern-matches single-line `tl.to()` calls.
Confirmed doubly wrong in one real render (`videos/snail-mucin-recut-34s`):
a source-level beat map reported "no gap over 3s anywhere," which was false
in both directions — a `tl.to(el, {opacity: 0.85}, 5.6)` counted as a
qualifying beat while moving 0.00 rendered pixels, and the same measurement
separately missed real gaps by only matching single-line `tl.to()` syntax.
If this kind of pre-render estimate is used at all, treat its output as a
hypothesis to check, not a result to report — the post-render pixel diff
above is the only thing that actually answers the static-hold question.

**Motion sidecars (`*.motion.json`) — declared intent, checked against the
same seeked timeline the renderer uses.** This sits between a source-level beat
map and a full render, and is the closest automated proxy for "render the MP4
and watch it". Drop a `*.motion.json` beside the composition, matching the HTML
basename when several share a directory; `check` **discovers it
automatically — there is no flag**, and `check --help` has no `--motion`. Its
`assertions[]` array takes exactly four kinds
(`~/.claude/skills/hyperframes-cli/references/lint-validate-inspect.md:74-99`):

| Assertion | Fires when | Code |
|---|---|---|
| `appearsBy {selector, bySec}` | not visible (opacity ≥ 0.5) by `bySec` | `motion_appears_late` |
| `before {a, b}` | `a` does not first appear strictly before `b` | `motion_out_of_order` |
| `staysInFrame {selector}` | once visible, its box leaves the canvas | `motion_off_frame` |
| `keepsMoving {withinSelector?, maxStaticSec?}` | a fully-static window exceeds `maxStaticSec` (default 2s) | `motion_frozen` |

Findings are errors by default, and a selector matching nothing fails loudly
as `motion_selector_missing` rather than passing silently. Five things follow
that are easy to get wrong, the last two of them measured on
`hyperframes@0.8.22` rather than reasoned from the docs:

- **`motion.enabled: false` in a `check --json` report means "no sidecar was
  found", not "motion verification was disabled."** Nothing was switched off;
  nothing was ever written. Read it as an adoption number — measured across
  this repo on 2026-09-02, **0 of 31 `videos/*` projects had one.** With no
  sidecar the fallback is the far coarser `sweep_static` failure.
- **The default `maxStaticSec` of 2s is Shorts-scale.** Set it per format from
  the cadence budget in the *Formats* table, and **scale `--samples`** with the
  piece — the 9-sample default on a multi-minute render is no coverage.
- **Scope `keepsMoving` to `#root`, never to one scene.** Its static-window
  scan runs across the **whole root composition duration** and is never
  bounded to the window in which that scene's clip is actually live, so a
  per-scene `withinSelector` reports the scene's own *off-screen* time as a
  frozen window and fails by construction on any composition whose scenes
  tile. Measured on a 3-scene, 9s proof where scene 2 runs 2.5-6.6s:
  `#scene-s02` → "nothing moves … between 0s and 2.5s", `#scene-s03` → "between
  0s and 5.65s", `#scene-s01` → "between 3.5s and 9s" — three errors, all of
  them the clip being off screen, none of them a real defect.
  `#<cid>-stage` behaves identically. The selector is not the problem: both
  forms resolve, so neither reports `motion_selector_missing`. On tiling
  scenes a single root-scoped `keepsMoving` loses nothing — a genuinely frozen
  scene still exceeds the window — and additionally covers the boundaries a
  scene-scoped assertion skips.
- **A sidecar beside a sub-composition file is silently ignored, and that is a
  false green.** `check` looks for the sidecar in the **project directory**
  next to the root composition; one written to `compositions/frames/` is never
  read. Confirmed by planting a deliberately impossible assertion
  (`appearsBy` on a selector matching nothing, which is the one thing
  guaranteed to fail loudly) in `compositions/frames/01-s01.motion.json`:
  `check` returned `ok: true`, `motion.errorCount: 0`, with `specPath` still
  the root `index.motion.json`. So per-scene sidecars do not shard the way
  per-scene compositions do — **one sidecar at the root, with every scene's
  selectors in it.**

What it sees is geometry and opacity on the seeked timeline, so it complements
a pixel diff rather than replacing it: it cannot see a colour wash, a clipped
raster going frozen (the `drawElement` failure above), or a text node
overpainted by an animated background — **unless the assertions name the copy
element itself.** That is the whole argument for asserting on the text rather
than its container. In `videos/ectoin-survival-molecule/`,
`compositions/frames/28-remember.html:167` puts the payoff line "A genuinely
interesting supporting molecule" as a **bare text node** under a `.wash.moss`
div, rendering it overpainted at **1.72:1**; an `appearsBy` on `#nt-2 p` would
have failed at check time as `motion_selector_missing`, because there is no
`p` to match.

An external review's language maps onto the four kinds almost directly — the
cheap way to turn a QC report into a re-runnable assertion rather than an
argument: "the reveal order is wrong" → `before`; "the entrance never happens"
→ `appearsBy`; "the hold is dead" → `keepsMoving`; "it drifts off" →
`staysInFrame`.

**Transition midpoint check.** Extract a frame at the exact midpoint of every
scene-to-scene transition, not just before and after it. A crossfade between
two different background colours produces a genuinely muddy, near-blank frame
at 50% — invisible if you only ever look at settled frames. `blur-crossfade`
is **not** exempt: its opacity pair and ease are identical to a plain
crossfade's, so it blends exactly as hard and the 10px blur only masks the
clash. `zoom-through` blends mildly (both wrappers at 0.875 at the midpoint —
worth the frame, rarely muddy). Only `push-slide` and `squeeze` genuinely
cannot blend: their midpoints must show both scenes side by side or
compressed, never mixed. See *Cuts, crossfades, and transitions* below for
which boundary gets which.

Also always check: frame zero (must be composed, not mid-fade — see mandatory
rule 4), and, for a short, that the last frame hands back toward the first if
a loop was promised (see *The hook* below).

**Frame-index-to-timestamp check, `beginframe` capture mode.** The frame-zero
check above assumes frame index and nominal timeline time line up — on a
Linux/cloud render they can silently diverge, in a way a clean local render
gives no warning of. HyperFrames' Linux headless-shell path defaults to a
`beginframe` capture mode (confirmed in `hyperframes@0.8.17`'s and `0.8.20`'s
bundled `dist/cli.js`, identical in both: `captureMode` is `"beginframe"` only
when `headlessShell && process.platform === "linux"`; every other platform
gets plain `"screenshot"` capture). In `beginframe` mode, a CDP
`HeadlessExperimental.beginFrame` response with `hasDamage: false` makes the
engine reuse the *previous* captured buffer instead of re-screenshotting
(`beginFrameCapture`) — and the composite-pending force-repaint workaround
that plain `screenshot` mode gets before every capture
(`prepareFrameForCapture`'s 1×1 `Page.captureScreenshot` flush) is explicitly
skipped when `captureMode === "beginframe"`. At frame 0 there is no previous
buffer to reuse, so a `hasDamage:false` first frame — the likely state right
after a `data-composition-src` sub-composition mount, before its content has
actually painted — can ship with the entrance element missing entirely, not
just under-tweened, even though the composition source has no bug. Confirmed
on `videos/snail-mucin-recut-34s`: its Linux/`beginframe`-mode master had a
frame 0 missing its title text outright (first appearing ~3 frames later),
though the composition's own entrance is a scale-only settle (0.98→1.0, no
opacity animation) with no reason to produce that. A clean local render is
not evidence this is fine — macOS/Windows never take the `beginframe` path at
all, so the identical composition renders a fully composed frame 0 locally;
checked against `madecassoside-clinical-cut`, `madecassoside-flat-matrix`,
`red-ginseng-glass-glow`, and `retinal-clinical-dossier`'s locally-rendered
masters, which all use the same `data-composition-src` + scale-only-settle
entrance pattern and all had a correctly composed frame 0. Treat any
Linux/cloud-rendered master (`hyperframes cloud`/`cloudrun`/`lambda`, or CI)
as needing its own frame-0 and scene-boundary extraction — don't infer safety
from a clean local render or from reading the composition source, since the
defect lives in the capture pipeline, not the markup. If it reproduces,
`PRODUCER_FORCE_SCREENSHOT=true` forces the same `screenshot` path macOS
uses — an internal env var found in the bundled source, not a published or
stable CLI flag, so test it before depending on it, and expect a render-speed
cost. A related symptom — two adjacent scenes at a cut each reading as a
different, internally-inconsistent point in time within one captured frame —
is consistent with the same stale-buffer-reuse mechanism firing mid-transition
rather than at frame 0, but that specific mechanism is inferred, not
source-confirmed the way the frame-0 case is: verify a suspect cut the same
way, by extracting and eyeballing the boundary frame, rather than assuming
the cause.

**Phone-scale legibility check.** Downscale an extracted frame to roughly 25%
size — the same "phone-viewing-simulation habit" *The thumbnail* section
already invokes for judging grid-size legibility. That habit is what
pre-render gate item 2 above actually runs: any headline, caption, label, or
citation that stops being legible at that scale is a reject, not a style
note. See *9:16-native composition* below for the type floors and *Asset
protocol* above for the diagram label budget — the thresholds it's checking
against.

**Safe-area intrusion scan.** A source-level audit ("does every scene consume
`--safe-*`?" — pre-render gate item 7a below) cannot see this class of defect,
because the source is genuinely correct; only the transformed, rendered pixel
isn't (see *9:16-native composition*'s safe-areas bullet for the mechanism
and the derived-token fix). Sample the actual render at a fixed fps (4fps —
finer than the static-hold check's 2fps, since a fast Ken Burns drift or an
entrance-transform transient can cross the line between two coarser samples
and self-correct before the next one), build an ink mask per frame
(`|luma - background| ` over a threshold, requiring a minimum run of masked
pixels in a row/column so stray antialiasing doesn't count as an edge), and
flag any frame with ink inside a reserved zone. This is a **hard gate**, not
advisory like the static-hold/blank-frame checks — a rendered pixel inside a
reserved zone will be covered by the platform's own UI on a real device,
which isn't a judgment call the way a static hold's cadence sometimes is.
Confirmed necessary, not theoretical: on `videos/peeling-not-progress`'s
round-6 render, three scenes passed gate item 7a (tokens declared and
consumed everywhere) while overshooting the real line by 5-10px once each
scene's own Ken Burns scale was accounted for, and a fourth scene's overshoot
existed only for a ~150ms entrance transient a 1-2fps spot-check reliably
lands outside of — a defect an external QC report and this project's own
prior single-frame checks both missed, and only a full-render, fixed-interval
pixel scan catches. See `scripts/check-safe-area.py` (harvested to the shared
catalog) for a reference implementation.

**Publish-envelope completeness check.** A clean render says nothing about
whether captions or a thumbnail exist — those are separate files a check
script has no reason to look for. Before calling a project done, confirm by
listing the project's own directory, not by recalling whether the step was
done: a burned-in caption composition or a real `.srt` (not a same-named but
unrelated file — see *The captions*' naming note), and a finalized thumbnail
(not just candidates — see *The thumbnail*'s file convention). This is the
check that catches a project with a complete word-level transcript and zero
caption output built from it.

**Catalog-contribution check.** Re-read production-loop step 5's own notes on
what got built new, not reused — if anything on that list is a genuine
mechanism (not a one-off scene), confirm it actually landed in the shared
catalog per step 12, not just that the step was considered. This is the check
that catches a component built cleanly, used correctly in this one video, and
then left invisible to the next one — the same failure mode that produced
five independent rebuilds of the same card before anyone thought to check.

**An external QC report is a claim, not a diagnosis — verify its fix against
the actual pixels before applying it.** A report can correctly name a real
symptom while misdiagnosing the cause, and its proposed fix can be wrong even
when the underlying complaint is legitimate. Two shapes this takes in
practice: a report calling two chips "low-contrast" and "too small" when
pixel inspection shows one CSS bug (an unboxed capsule stretched into a
1000px+ slab by an inherited `inset:0`) producing both symptoms — the
colour/size tweak the report asks for is real and worth doing, but it isn't
*the* fix; and a report prescribing "trim the outro to 2s" for a static-hold
complaint when the outro's full duration carries narration that a literal
trim would cut off mid-sentence — the complaint (frozen imagery) is real, the
literal instruction (shorten the scene) would have broken something the
report never looked at. Reproduce every finding against the render before
building a fix plan from the report's own wording, and where the report's
named fix and the measured root cause diverge, fix the root cause and say so
— don't silently apply the literal instruction because it's what was asked.

**A report can also name a symptom that does not exist at all — a distinct
failure class from misdiagnosis, because there the reproduction step above
finds nothing to fix rather than the wrong fix.** Confirmed in one QC pass
where three of four findings were fabricated, all consistent with a
vision/OCR-based reviewer's characteristic failure modes: a claimed on-screen
typo that a native-resolution frame crop showed wasn't there (film grain
under a letterform read as a different character to OCR); a claimed BLOCKER
safe-area violation that row-measuring the actual caption band's pixels
showed cleared the reserved zone by 48px (a downscaled or letterboxed
preview made a mid-frame band look bottom-anchored); and a claimed 8s dead-air
gap that per-250ms RMS measurement showed was actually two real ~3s
narration-light spans with BGM present throughout, not silence. Each class
has a cheap, specific disproof — don't reach for a full frame-by-frame
re-render to check a single claim: a text claim gets a native-resolution crop
of the specific timestamp; a safe-area or position claim gets a pixel-row
measurement against the actual token/canvas math, not an eyeballed preview;
an audio claim gets RMS-vs-time across the disputed window, not a listen-
through. Treat a report's fourth, true finding with full weight even when
the other three are fabricated — a report being wrong on magnitude or
existence for most of its claims doesn't mean the one real finding isn't
real; verify each claim independently rather than discounting the whole
report once a couple of claims fail to reproduce.

**A clipped raster can render as a DEAD REGION while the DOM, the lint pass
and the engine's own capture guard all report it fine.** This is a capture-path
defect, not a composition bug, and it is the one failure in this file that a
correct source cannot prevent.

The engine's default capture path on this platform is `drawElement`, not a
screenshot (`captureMode: "drawelement"` in the render trace). It is faster and
usually pixel-exact, but it can silently produce wrong pixels for one specific
shape: **a raster image inside a container whose own `width` is being
animated** — a wipe mask, a reveal panel, any `overflow: hidden` box that grows.
Confirmed by bisection on `hyperframes@0.8.22`, four renders, one variable at a
time:

| clip content, identical geometry otherwise | result |
|---|---|
| text on a solid fill | **passes**, `psnrDb: "inf"` (pixel-identical) |
| 1200×1200 raster + scrim at `inset: 0` | **fails**, 22.6 dB |
| same, SVG overlay removed | **fails**, 22.6 dB — the SVG is not the trigger |
| same, image removed, text control only | **passes**, `inf` |

So the trigger is the raster, not the animated `width` itself. **Scale matters
too** — the same content at 846×300 passed where 840×900 failed, so a small
clipped image is not evidence the pattern is safe. A text or solid-colour
reveal bar is fine; do not read this as "never animate width".

`0.8.22` ships a guard: it captures a few ground-truth screenshots, compares
them against the fast path, and re-renders the whole video via screenshot when
they disagree (`drawElement self-verify failed at frame N: 22.6dB < 32dB`,
followed by `re-rendering via screenshot`). **Do not treat that guard as
protection.** It samples ~4 instants across the entire render and scores each
against a fixed threshold, which makes it weakest exactly where this defect
lives — an animation that ramps in from nothing. Measured on a real broken
project: the guard armed, sampled *inside* the broken scene, and **passed at
40.4 dB**, because at that instant the wipe was 2.8% open — about 23px of 840,
roughly 1% of the canvas. The same defect was catastrophic twenty frames later.
The render shipped broken with a clean log.

Read the render log as triage, never as proof:

- **no `self-verify` line at all** — the guard never armed; you have no signal.
- **`failed`** — the fast path was wrong and the fallback saved you. The output
  is correct; the composition still has the shape that triggers it.
- **`passed` with `psnrDb: "inf"`** — pixel-identical, genuinely clean.
- **`passed` with a *finite* psnrDb** — a real divergence was measured and
  judged small. Not a bug on its own (a benign value can repeat identically in
  a known-good build), but worth a look when a comparable frame reads `inf`, or
  when the number drifts toward 32.

**This is a FOURTH failure mode, and nothing in `catalog/tooling/` currently
catches it.** That matters, because "we already have a region-aware static-hold
check" is exactly the reasoning that gets the right detector dropped as
duplicative — it was the first assumption on the project where this was
confirmed, and it was wrong. The four are distinct:

| # | defect | caught by |
|---|---|---|
| 1 | blank *frame* | blankness scanner (luma stddev) |
| 2 | frozen *frame* | whole-frame static-hold (PSNR) |
| 3 | *empty region* inside an alive frame | region-aware content-then-empty |
| 4 | **frozen region that still carries content** | **nothing we ship** |

Measured against a render known to ship a dead panel,
`catalog/tooling/check-static-hold.py` missed it in **both** modes:
whole-frame reported no findings across 42 samples, because the scene's labels
and badges animated on schedule and the frame was therefore never frozen — the
same masking problem this file already documents for burned-in captions, with
ordinary scene furniture doing the masking. Region-aware reported three
content-voids, **none of them the frozen panel**, because it detects a cell
going content-then-*empty* and that panel always had content in it. It was
frozen, never emptied, so there was no transition to fire on.

**The check that actually decides it is per-region and per-scene**, because it
does not inherit the guard's sampled-instant blind spot:

```
for each element that CLIPS A RASTER (Ken Burns panel, wipe mask, tile)
        AND has an authored tween inside this scene's window:
    sample N frames ACROSS THAT ELEMENT'S OWN SCENE WINDOW
    count adjacent pairs where the region is byte-identical
    any long identical run = dead region
```

**Both halves of that scope are load-bearing.** A deliberately static plate is
byte-identical too, so raw identity flags calm design as dead — a held product
shot would fail every time. Scoping to elements that clip a raster *and* carry
authored motion in that window is what keeps the false-positive rate sane, and
it is the operational form of "should be animating".

That catches the confirmed case by construction — its panel was byte-identical
between mask-closed and mask-open, a window where it should have been moving.
A healthy panel looks like this (5 clipped rasters, 10 samples across each
one's own scene): **0/9 identical pairs, max frame-to-frame delta 179–235**.

Two corollaries worth carrying:

- **A frame diff reporting ZERO change in a region across a whole scene is
  evidence of a broken render, not slow pacing.** On the confirmed case it was
  misread as a cadence number for two rounds, and two plausible diagnoses were
  wrong first (too-subtle contrast; duplicate media nodes — both real issues,
  neither the cause).
- **`snapshot` and a plain browser drawing the scene correctly while `render`
  does not is the tell**, and `--no-browser-gpu` confirms it. But fix the
  mechanism, not the flag: a `clip-path` driven by a custom property is
  compositor-safe and keeps the fast hardware path.

## Cuts, crossfades, and transitions

**The hard rule first, because it is the one part a frame can settle: a plain
crossfade across a ground change produces a muddy midpoint.** Both layers sit
at ~50% opacity over an unrelated canvas colour at once, so the 50% frame is
washed and near-blank — invisible if you only look at settled frames. A design
that alternates background colour scene-to-scene for contrast (a legitimate
technique) makes plain crossfades structurally unsafe at every boundary that
changes ground. The arbiter is not an argument but the *Verification loop*'s
transition-midpoint extraction: pull the frame at the exact midpoint and look.
Same-ground softness (a very short ≤150-200ms fade) was always allowed.

**Everything past that rule is format-scoped, and this file used to state it
format-blind.**

- **Shorts.** Hard cuts on a timing grid stay the default. A 30-45s piece cut
  to a grid has no room for a transition system, and softness at a boundary
  reads as slack against the format's own cadence.
- **Long-form.** Plan a *transition system*, not a per-boundary decision:
  **2-3 types**, one primary carrying ~60-70% of boundaries plus 1-2 accents
  (`hyperframes-animation`'s `transitions/overview.md` sets that budget —
  "Pick ONE primary … + 1-2 accents. Never use a different transition for
  every scene."). For an editorial explainer the primary is a **clip-path
  wipe** — `inset()` opened along one axis on the incoming clip wrapper, one
  direction held per chapter — with a longer wipe on the other axis as the
  accent. Give the accent to **chapter boundaries** so transition strength
  serves the re-hook (*Long-form structure* below) rather than decorating an
  arbitrary scene change — or let a camera leg land on the next act's payoff
  and carry the boundary that way. Hard cuts survive as **deliberate
  emphasis**: a few per piece, chosen, not defaulted.

  **Not `push-slide`, and this corrects an earlier version of this section.**
  A wipe reveals the incoming scene at its own resting position; a push
  *translates* whole scenes, which drags their content through the reserved
  safe-area zones on the way in and out. Confirmed by building both on the
  same 29-scene 1920×1080 piece and rendering each: the push failed the hard
  safe-area gate on **99 frames** — real text, up to 6.2% edge density inside
  the top band — against a hard-cut baseline that passed all 1361. The wipe
  build measured **0**. Both render correctly, both pass `check`, and both are
  equally safe on grounds; the difference is invisible until the safe-area
  gate runs on a real render, which is why it survived a clean preview and a
  clean `check` before being caught.

  Two caveats on the wipe. It only clips, so it cannot place content anywhere
  a settled frame does not already have it — that is the whole argument, and
  it holds only if the settled frames are themselves compliant. And an
  animated clip over a **raster** is the `drawElement` capture bug above: safe
  on a browser-drawn piece (confirmed by grepping every scene for `<img>` and
  finding none), suspect the moment a plate is inside the wiped region.

The registry holds exactly five — `crossfade`, `blur-crossfade`, `push-slide`,
`zoom-through`, `squeeze` — and **which of them can cross a ground change is a
property of their GSAP templates, not of their names**, computed at the
midpoint (`p = 0.5`) from the registry's own `gsap_template` lines:

**Ground-blending and safe-area transit are independent axes, and a
transition can be clean on one and dirty on the other.** `push-slide` is the
worked example: it never composites two grounds *and* it drags content through
every reserved zone. Only the first column below was measured from the GSAP
templates; the second was measured on rendered frames, and only for the two
marked, so treat the rest as suspect until checked — all three translate or
scale their wrappers, which is the mechanism.

| Transition | Both wrappers at midpoint | Blends grounds? |
|---|---|---|
| `push-slide` | `opacity: 1` pinned; only `x`/`y` move | **No** — never composites two grounds |
| `squeeze` | `opacity: 1` pinned; only `scaleX` moves | **No** — never composites two grounds |
| `zoom-through` | 0.875 / 0.875 (asymmetric `power3.in` out, `power3.out` in) | Mildly — ~11% outgoing ground, ~2% raw canvas |
| `blur-crossfade` | 0.500 / 0.500 (`power2.inOut`) | **Yes, fully** — the 10px blur masks it, nothing more |
| `crossfade` | 0.500 / 0.500 (`power2.inOut`) | **Yes, fully** — this is the muddy case |

| Transition | Drags content into reserved zones? |
|---|---|
| clip-path wipe (authored, not in the registry) | **No** — measured, 0 flagged frames. Nothing moves. |
| `push-slide` | **Yes** — measured, 99 flagged frames on a full-canvas scene |
| `zoom-through`, `squeeze`, `blur-crossfade` | Unmeasured. All three translate or scale a wrapper, so assume yes until a render says otherwise. |

`push-slide` takes a `direction` of `LEFT`/`RIGHT`/`UP`/`DOWN` ("vertical
push" is a direction, not a separate transition); there is no named `cut`,
`match-cut` or `wipe`, a cut being the absence of a transition. And the
registry's note on `blur-crossfade` ("Default when the two scenes' #root
backgrounds differ a lot — the blur masks the background-color clash a plain
crossfade would expose") means what it says: **masks**, not removes. Extract
its midpoint like any other.

**Record the disagreement rather than resolving it silently.** This file has
said hard cuts beat transitions on retention; `transitions/overview.md` says
"Every composition uses transitions. No exceptions… Scenes without transitions
feel like jump cuts." **Neither claim is measured**, and the one long-form
project this channel has shipped marks every retention comparison available to
it `[UNDERPOWERED]` in its own brief
(`videos/ectoin-survival-molecule/BRIEF.md:23-25`), the baseline being
Shorts-derived and the piece not. The format split above therefore has the
same status as the hook window in *Long-form structure*: a craft budget,
usable for authoring, never citable as the cause of a failure, superseded the
moment a channel has retention data on a piece that used transitions.

**The mechanics, so a transition is a timing edit and not a hand-drawn
effect.** `transitions/TRANSITION-REGISTRY.md` (§"How the injector applies a
transition") defines the whole move as four edits at a boundary of duration
`d`:

1. Extend the **outgoing** clip's `data-duration` by `d`. An ended clip holds
   its final frame, so it is still on screen to be transitioned away from.
2. Pull the **incoming** clip's `data-start` earlier by `d`. That overlap *is*
   the transition window; no other authored time moves.
3. Alternate `data-track-index` 0/1 so two overlapping wrappers never share a
   track. The higher track composites on top.
4. Stamp the tween on `window.__timelines["main"]` at `T = overlap start`,
   targeting the two clip **wrappers** — not their contents.

Each sub-composition's own paused timeline keeps being driven independently, so
the root tween moving the wrappers introduces no double seek. Two constraints
travel with the mechanism: **exit animations are banned except on the final
scene** ("The transition IS the exit" — fading the outgoing scene out and then
running the next scene's entrance is a jump cut with a dip), and the registry's
`max_duration_s` is **2.0s**, with 0.3-0.6s the working range.

**Confirmed case — the rule worked exactly as written and the video still read
as slides.** `videos/ectoin-survival-molecule/` (340s, 1920×1080, 29 scenes)
has **28 of 28 boundaries as hard cuts**, and not by neglect: its root timeline
is a single empty anchor tween (`index.html:230-238`) and the reasoning is
written out immediately above it (`index.html:231-233`), citing the
muddy-midpoint rule this section opens with. 17 of the 28 do change ground
(ink↔paper) — but **11 of 28 are paper→paper** and could have carried a
same-ground transition even under the old, format-blind rule. Every gate this
skill had came back green and an external review still called the piece an
animated presentation. A cuts-only rule written for Shorts and applied to
long-form is one of the three ways a piece passes its cadence gate and reads as
slides; see *Long-form structure* for the other two.

## YouTube delivery

The platform layer. Everything here shapes the beat sheet, so it is read
*before* beats are written, not at publish time. Platform numbers drift —
treat limits and safe-area percentages as current-as-written and verify
anything load-bearing before a real publish.

### Formats

| | Long-form | Short |
|---|---|---|
| Canvas | 1920×1080 (16:9) | 1080×1920 (9:16) |
| `data-resolution` on `<html>` | `landscape` | `portrait` |
| Length | any (but see the ~3 min workflow cap below) | ≤ 3:00 (limit raised Oct 2024) |
| State-change cadence | every 8–12 s | every 1.5–3 s, **for the entire scene** |
| Reserved zones | bottom 108 / top 54 / sides 96 | bottom 384 / top 192 / right 162 |
| End-screen reserve | final 5–20 s only, right third + lower-right | n/a |
| End screens / cards | yes | no — one related-video link |
| Chapters | yes (≥ 3, first at 0:00, each ≥ 10 s) | no |
| Thumbnail | authored or extracted + scored | frame 0 |
| Replay mechanism | end-screen handoff | engineered loop |

Both canvases share a **1080px short edge**, so the type floors below are the
same for each — see *16:9-native composition* for why, and for why scaling the
scale is the error.

The cadence target is not "at least one beat somewhere in the scene" — a scene
that is 15s long with narration needs roughly 5-10 authored state changes
spread across its full duration, not 2-3 clustered at the start. See
*Verification loop*'s static-hold check for how this actually gets caught.

**For long-form the cadence row above is a floor, not a pass.** A piece can
clear it on every scene and still read as slides; it must also satisfy
*Long-form structure*'s continuity mechanisms and gate items 14-17.

### 16:9-native composition

The 9:16 section below is the one this skill grew up on, because every project it
was written against was a Short. **This section is its sibling, not its
afterthought** — and the first thing to know is that landscape is the engine's
*native* canvas, not a port away from portrait. HyperFrames' `CANVAS_DIMENSIONS`
defines `landscape: {1920, 1080}`; `init --help` calls 1920×1080 the template
default; `1080p` and `hd` both alias to it; `data-attributes.md` lists `1920x1080`
first; and `storyboard-format.md`'s own worked example is `format: 1920x1080`.
The vertical work is the deviation. Approach a 16:9 build as returning to the
default, not as porting away from a norm.

- **Declaration is two coordinated places**, and both must agree:

  ```html
  <html lang="en" data-resolution="landscape">
    ...
    <div id="root" data-composition-id="main"
         data-width="1920" data-height="1080" data-duration="...">
  ```

  `data-resolution` goes on `<html>`, not on the root, and accepts exactly six
  preset strings (`landscape`, `portrait`, `landscape-4k`, `portrait-4k`,
  `square`, `square-4k`). **`render --resolution` is a supersampler, not an
  aspect converter** — it raises Chrome's device scale factor so the capture
  lands at a larger size, and it requires the aspect to already match and the
  scale to be an integer multiple. You cannot render a portrait composition as
  landscape, and passing mismatched `--width`/`--height` silently renders at the
  authored size instead of erroring.

- **The type scale transfers unchanged. Do not re-derive it, and above all do
  not scale it.** This is counter-intuitive enough to state plainly: **1080×1920
  and 1920×1080 have the same 1080px short edge.** Type size is a fraction of
  the short edge, because the short edge is what governs how much of a viewer's
  visual field a glyph occupies for a full-frame video at a given distance. So
  the floors below carry over one-for-one, and a project's existing `--t-*`
  scale needs no landscape variant.

  A design system may even record that its canonical scale was specced on
  1920×1080 in the first place, with the 9:16 numbers as the improvised
  reinterpretation — in which case a 16:9 build is returning the scale to its
  home canvas. What *does* need an explicit variant is **layout**, per the rule
  such a system states directly: "each component needs an explicit layout
  variant; none can be derived by scaling." Scaling by 0.5625 or 1.78 is the
  error in both directions — one pushes body copy under the floor, the other
  inflates a headline into the frame edge.

- **Reserved zones, and they are a different shape from Shorts — not merely
  different numbers.** There is no action rail and no title strip in 16:9;
  reserving 162px on the right is *semantically* wrong there, not just
  numerically. Verify against a current device or Studio before a real publish;
  these are current-as-written:

  - **Bottom 108px (10%)** — the player progress bar and controls. Persistent on
    mobile, on-hover on desktop. This is the only zone that binds every frame
    hard.
  - **Top 54px, left/right 96px (5%)** — general title-safe margin, the
    broadcast 5% action-safe convention. Looser than the bottom because nothing
    is reliably drawn there.

  So a reasonable landscape token set is `--safe-top: 54px; --safe-right: 96px;
  --safe-bottom: 108px; --safe-left: 96px` — and, exactly as in 9:16, **the
  tokens must be consumed by every scene, not declared in one file and
  hardcoded elsewhere.**

- **The end-screen reserve is scene-scoped, which is the structural difference
  from Shorts.** The Shorts rails bind all 1920 frames of a 60-second short.
  The end-screen zone binds only the final 5–20s, and is *unreserved* for the
  rest of the piece — so applying it globally wastes the right third of every
  frame in the video. Reserve it on the final scene alone (see *The end screen
  is a scene*): at most 4 elements, all inside the inner 80% (192px left/right,
  108px top/bottom), video/playlist elements ≈613×343, subscribe/channel circles
  ≈298px diameter. In practice: keep the **right third (~640px) and the
  lower-right** clear of anything that must be read.

- **Clip at the safe box, and entrance transients stop being a safe-area problem
  at all.** The zoom-derived `--safe-*-zoomed` tokens elsewhere in this file solve
  a *scene-wide* transform; they do nothing for the far more common case of an
  individual element's entrance. A panel that rests against the safe line and
  enters from `x:-90` sits 90px inside the reserved zone for its whole entrance,
  and so does anything given a `scale:1.03` "breath" near an edge. Measured on a
  real 29-scene landscape build: the hard safe-area gate found **81 frames with
  ink in a reserved zone**, every one of them an entrance or scale transient, in
  four different scenes — and the composition's padding was correct throughout.

  Per-element fixes are whack-a-mole. One rule fixes the whole project:

  ```css
  .stage { padding: var(--safe-top) var(--safe-right)
                    var(--safe-bottom) var(--safe-left); }
  .stage > * { overflow: hidden; }   /* the child fills the safe box exactly */
  ```

  The stage's single child fills the safe box, so clipping it clips at the safe
  line by construction — no element can render outside it regardless of what its
  transform does. It also *reads* better: a slide-in becomes a masked reveal
  rather than a panel flying in over the margin. Prefer this to widening a
  margin, which is sized against whatever the token happened to be that day and
  goes stale silently the moment it changes.

  Containment is not a licence to keep decorative motion, though. Two of the four
  offending scenes were only moving because a `scale:1.03` had been added to keep
  a quiet scene alive on a metric — the exact idle-motion anti-pattern named
  above. Those were **removed and replaced with a real content beat**, not
  clipped into compliance. Clip the transients you actually want; delete the ones
  that were filler.

- **The layout failure mode inverts, and this is the part most likely to be got
  wrong by someone carrying 9:16 habits across.** A vertical canvas fails as a
  small element marooned in a tall empty column — hence 9:16's "fill the safe
  column" rule. A wide canvas fails the opposite way: as a **full-width band of
  text with no depth**, a single centered line stretched across 1728px of safe
  width with nothing behind it. Advice tuned for the vertical case ("structure
  scenes as rows, not columns") is actively wrong here.

  The native 16:9 shapes are the ones a wide frame affords and a tall one
  doesn't: **two-column** (claim left, evidence right), **hero-left /
  diagram-right**, **full-bleed plate with a caption rail**, and a genuine
  **three-across** row that portrait can only fake vertically. Hero copy still
  occupies 60–80% of *available* width — but in landscape "available" should
  usually mean a column of the grid, not the whole 1728px. A headline set across
  the full safe width reads as a slide, not a frame.

- **The type scale transfers, but the MOTION budget does not — and this is the
  trap, because the two feel like the same question.** Measured on this repo's
  first landscape build: a composition authored with the channel's normal beat
  vocabulary (text fades, thin strike-through wipes, staggered entrances) came
  out at **4.0 % of 8fps steps clearing a perceptibility floor, median
  frame-to-frame |Δluma| 0.027**, against **11.7 %/0.162** and **23.1 %/0.451**
  for two shipped 9:16 projects on the same channel. Same pixel count, same type
  scale, roughly six times less perceived motion.

  The mechanism is grid share, not size. On a 1080-wide portrait frame a
  `--t-hero` headline spans most of the frame's width, so animating it changes a
  large fraction of the pixels. On a 1920-wide landscape frame that same
  headline sits inside a two-column grid cell and changes roughly half the
  share — the beat is identical in the source and materially weaker on screen.
  Thin elements suffer worst: a 5px strike-through bar is ~0.07 % of a 1920×1080
  frame and is essentially invisible to any frame-difference metric, and nearly
  so to a viewer.

  So budget landscape motion by **fraction of frame changed**, not by counting
  authored tweens. In practice: give entrances noticeably longer travel than the
  portrait equivalent, prefer beats that move a whole column or panel over ones
  that move a word, and treat any scene whose only motion is a text fade as
  having no beat at all. A targeted pass adding real content beats to dead tails
  moved the number above from 4.0 % to only 5.8 % — widening travel and adding
  end-of-scene payoffs is not enough on its own, which is worth knowing before
  budgeting a landscape build's motion pass as an afterthought.

- **Size a beat against the metric, and the metric is LUMA area — not how
  different the colours look.** A frame-difference check sees
  `mean |Δluma| per step ≈ (frame-area-fraction × luma-delta) / (duration × 8)`,
  so a beat clears a 1.0 floor only when area and *luminance* change together.
  Two traps, both measured on a real build:

  - **Hue change is not luma change.** Recolouring a 12%-of-frame element from
    celadon `#93B896` to coral `#C97A5C` reads as a dramatic shift to the eye and
    is a **27-luma step** — per-step 0.45, under the floor, invisible to the
    check. The same element to `#131516` is a **149-luma step** — per-step 2.48.
    When a beat needs to register, pick the colour by luminance, not by hue.
  - **Small elements do not add up.** 104 dots recolouring, 18 ring squares
    rotating, an 18px strand field dispersing — each measured at ~0.1–0.4 per
    step. A single panel at 8–17% of the frame clears comfortably. Rough
    working rule for 1920×1080: **area ≥ 8% and luma delta ≥ 80, inside ≤ 0.8s.**

  Compute it before authoring rather than after rendering. Two of the fixes in
  that build failed *because they were sized by eye*, and each cost a full render
  to discover.

- **Depth roles and the one-dominant-focal-point rule are unchanged**, and
  landscape makes them easier to satisfy, not harder: there is room for a hero
  and a genuinely separated supporting layer side by side, rather than stacked.
  Use it. Two competing focal points is still the failure.

- **Vertical occupancy still matters, it is just less scarce.** A 1080-tall safe
  box is short enough that a centered single line with 400px of dead space above
  and below reads as an unfinished layout, the same as it would in portrait.

- **The contrast floor is universal, not a portrait rule** — it sits in the
  9:16 section below only because that is where this file grew up. 4.5:1 for
  any text meant to be read, **measured on rendered pixels rather than declared
  tokens**, and landscape makes its worst shape *more* likely: a wide frame has
  room for large tinted washes behind copy. Two findings from the one long-form
  piece this repo has, pointing opposite ways — a coral strike-out held at 0.85
  to rhyme with the opening scene measured 4.78:1 and an external review flagged
  it anyway (deliberate, not a defect), while the real defect in that same scene
  was a **bare text node under a `.wash`** at 1.72:1 that no declared-colour
  check caught. Sample the pixels, and check the copy's *markup* too.

### Long-form structure

Everything above is per-frame. This is the shape of the whole piece, and the
skill had almost nothing on it because it had never built one.

- **Know that you are outside the specialized workflows.** `/hyperframes`'s
  routes cap the specialized narrative workflows (`faceless-explainer`,
  `product-launch-video`, `pr-to-video`) at **about 3 minutes**, are strongest
  at 30–90s, and explicitly route anything longer to `/general-video`. A 5-minute
  piece is outside all of them. That is not a prohibition — it means the
  scene-count, asset, and render assumptions those routes bake in do not apply,
  and you own them yourself.
- **Act structure, not a long Short.** Group beats into acts that each deliver
  one payoff, and give every act its own small arc. The rule that every beat past
  the value delivery must earn its place applies *per act*, not once for the
  whole video — a five-minute piece has five or six chances to lose the viewer,
  not one.
- **Re-hook at every chapter boundary.** This is long-form's equivalent of the
  Short's engineered loop, and it is the single highest-leverage structural move
  the format has. A chapter boundary is precisely where a viewer decides to
  leave; it is also where most compositions relax — a summary beat, a calm
  transition, a breath. Design a hook *into* each boundary: end the act on an
  open question the next one answers, and open the next act on its payoff rather
  than its setup. If the beat sheet's chapter boundaries all read as "and now,
  the next topic," the structure is wrong.
- **Cadence 8–12s, recorded as a craft budget and not a measured threshold.**
  Treat it the way a channel baseline treats any unbacked number: usable for
  authoring, never citable as the cause of a failure. If a project's own
  measured channel data says otherwise, that data wins.
- **The hook window is genuinely unresolved — do not pick one silently.** This
  file has said ~8s for long-form; the v2 package says ~15s; neither is measured
  on any real channel, and the two disagree by nearly 2×. Where a channel has
  its own retention data, use it and record that you did. Where it doesn't, say
  the number is an assumption in the beat sheet rather than inheriting one from
  whichever document was read most recently. What is *not* in dispute: frame
  zero is still the hook, still composed, still never a fade-from-black or a
  title card, and the payoff still lands early rather than after a setup.
- **Chapters are a YouTube metadata feature with no engine primitive behind
  them.** There is no chapter attribute, no chapter element, nothing in the CLI.
  They exist only as timestamps in the description — which means nothing in the
  render pipeline will ever tell you they drifted after a re-time. Re-derive the
  chapter list from the composition's real `data-start` values as the last step
  before publish, exactly as the re-timing cascade requires for the storyboard.
- **Cadence is necessary and not sufficient — the failure mode long-form has
  and Shorts don't is CONTINUITY.** The confirmed case is the one in *Cuts,
  crossfades, and transitions*, and its numbers are the point:
  `videos/ectoin-survival-molecule/` measures **12.7% active steps** on the
  shipped render against its own Act 1 pilot at 5.8% and shipped 9:16
  comparators at 11.7% and 23.1%, with a per-scene longest quiet run whose
  median is **5.0s** and which never crosses the project's own 6.0s long-form
  ceiling — scene 28 reaches exactly 6.00s. It passed on cadence and still
  read as slides, and no gate here could say why:
  all of them are per-frame or per-scene, and the defect was *between* scenes.
  Three continuity mechanisms, in priority order — the **transition system**,
  a **camera path**, **persistent actors**. The fix is continuity, not
  spectacle: not Three.js, WebGPU or a shader pass, which is *Posture*'s
  "spend boldness once" on the wrong problem.
- **Camera as the spine, planned at beat-sheet time and not in the motion
  pass.** Map the information hierarchy onto zoom levels so consecutive scenes
  read as *framings of one space* rather than separate slides: salt crystal →
  bacterium → hydration layer; front label → INCI list → verdict. Decided at
  step 2 it is free; decided at step 9 it means re-authoring every scene's
  markup. The rules: `viewport-change` (one `.world` wrapper, one
  `cam {scale, x, y}` state object — everything else follows),
  `coordinate-target-zoom` (*measure* the element you fly to, never hand-derive
  its coordinates), `multi-phase-camera`; the multi-leg shapes are the
  `camera-journey` and `zoom-out-workspace-reveal` blueprints, and
  `hyperframes-keyframes` covers a punch-in on an untimed wrapper. Two rules
  already here are exactly what a camera move needs: a scene-wide transform is
  what the `--safe-*-zoomed` tokens exist for, and
  `.stage > * { overflow: hidden }` keeps the moving world clipped at the safe
  line. `motion-blur-streak` goes on the fast leg only, sharp at each landing,
  and is hand-authored SVG/CSS — **there is no render-level motion blur.**
- **Persistent actors: rearrange them, don't redraw them.** Consecutive beats
  sharing a subject should share **one sub-composition** — the multi-scene
  merge in `hyperframes-core`'s `references/composition-patterns.md` §"C.
  Multi-scene merge": internal phase divs, one timeline, phases as timeline
  positions. Actors are then *rearranged* between phases (the same DOM nodes
  moving, FLIP-style) rather than rebuilt — the difference between a diagram
  that evolves and two that resemble each other. So **split composition files
  by actor continuity, not by narration sentence**, the same instinct as the
  one-evolving-diagram rule in *Asset protocol*. This does not conflict with
  the "stay one level" nesting warning below: a merged file *is* the
  sub-composition, its phases positions on that file's own timeline, not a
  second `data-composition-src` hop. A merged sub-comp can run 30-60s+, so
  scale `check --samples` with it. Confirmed case:
  `videos/ectoin-survival-molecule/`'s `09-exclusion.html` and
  `10-messier.html` carry **byte-identical protein+shell SVG geometry**
  (`viewBox 0 0 620 620`, r 190 and 112, `stroke-width` 46) plus a duplicated
  ring-builder loop — one actor drawn twice instead of moved. Its
  `hyperframes.json` even declares a `compositions/components` directory that
  **does not exist**, and the shared catalog had no molecule actor: the miss
  was a *creation* (production-loop step 12), not just a lookup.
- **Narration sync at word level, not just scene level.** Long-form has enough
  narration for beats to fire *on* the spoken word rather than near it: a claim
  revealed phrase by phrase on its own onsets, three alternatives each reacting
  to a spoken "not", a counter running while the number is said. Word timings
  come from `hyperframes transcribe` (which writes `transcript.json`) or
  `media-use`'s TTS `--words`; the per-word visual rule is `asr-keyword-glow`.
  Two traps: **`hyperframes beats` is MUSIC beat detection, not narration**,
  and captions stay a separate authoring decision from the visual beat schedule
  (*The captions*), so a word-synced beat sheet does not license deriving
  caption cues from it. The re-timing cascade's item 7 and its stale-transcript
  warning apply at full force — a re-recorded line desyncs every word-timed
  beat in its scene even when the scene's own start and duration never move.

### 9:16-native composition

A vertical canvas fails differently than a horizontal one, and "flip the grid
axis" is not sufficient guidance — the actual failure mode this format
produces is content anchored to the top of a 1920px-tall column with the
bottom half empty, which reads to a viewer as "small fonts" even when the type
size itself is reasonable.

- **Depth roles, every designed scene.** Background, midground, and
  foreground each carry a distinct role rather than everything painted flat
  on one plane. In practice: a hero visual (a photographic plate, a product,
  a dominant graphic) plus at least one clearly separated supporting layer
  (a headline, a data point, a caption band). This is the concrete version
  of "one dominant focal point" (pre-render gate above) — the hero reads
  first, the supporting layer reads second, and nothing competes for first
  read.
- **Anchor to an edge or a structural grid.** A small card floating centered
  in open canvas is the failure this rule names — anchor content to a grid
  column, a full-bleed edge, or a safe-area boundary instead of letting it
  drift free in empty space.
- **Fill the safe column.** Active content — not incidental background — should
  occupy roughly 65-80% of the vertical safe area's height in a settled frame,
  not a single centered line floating in a mostly-empty canvas. If a scene's
  content is naturally short (a single stat, one word), give it real scale and
  supporting motion layers rather than leaving negative space unaddressed —
  negative space should be a composed choice (breathing room around a
  deliberately minimal beat), not a byproduct of not filling the frame.
- **Type floor for phone viewing.** Hero/headline text: roughly 96-160px at
  1080 width depending on line count. Reading/body text: 40px minimum.
  Burned-in captions: 42-56px. Labels and secondary chrome (a citation pill,
  a source tag): 26-32px, and 32px is the absolute floor for anything a
  viewer is meant to actually read — smaller than that is decoration, not
  content. These floors sit intentionally higher than some outside guidance
  for the format (one external production review set the headline floor at
  72-110px and body at 34-48px) — real scenes across 14 of this channel's 24
  shipped projects already run type as small as 18-33px, which is a
  legibility failure, not evidence the lower floor is workable. Keep the
  tighter numbers above rather than relaxing them to match a looser outside
  spec. This is higher than a 16:9 desktop-first floor because the
  composition is watched at arm's length, often at partial screen
  brightness, often with the platform's own UI cropping into the frame
  edges.
- **Contrast floor: 4.5:1 for any text meant to be read, measured against
  the actual pixels behind it, not the design token alone.** The type-size
  floors above have no teeth without this — a headline can clear every size
  rule and still be functionally invisible if its declared colour sits
  close to the plate colour behind it. This is a real, confirmed gap: a
  render shipped with pink (`#b9835a`) text directly over a light plate,
  measuring 1.44:1 on the rendered frame (WCAG AA's own large-text floor is
  3:1; this skill's bar is higher because the format's variable backgrounds
  make a marginal pass on one frame a likely fail on the next), and the
  engine's own automated contrast checker reported "13/13 checks pass" on
  that exact render — an automated contrast pass evaluates the *declared*
  foreground/background colours in the stylesheet, not what a plate, scrim,
  or blend-mode layer actually puts behind the text at render time, so it
  cannot see this class of failure either. When text sits over a photo or a
  variable plate rather than a flat token colour, give it an opaque backing
  (a pill, a scrim) rather than trusting a colour choice to stay legible
  across whatever the plate turns out to be — verify by sampling the actual
  rendered pixels at that timestamp, not the CSS.
- **A colour token's own definition can carry a scope; using it off that
  scope is a contrast bug an audit can miss.** When a secondary-ink token
  is documented against one specific ground ("secondary text on paper —
  4.89:1, passes"), that scope is a constraint, not just a comment — using
  the same token on a *different* ground can fail outright while a
  project's own record claims a clean pass. Confirmed case: a token
  defined and scoped to paper (`#6B6B6B` at 4.89:1) was reused on an ink
  ground at **3.44:1**, while the project's own verification notes said
  "16/16 checked and passed" — the check had evaluated the token's
  declared value in isolation, not against the specific ground each usage
  site actually sat on. Contrast has to be re-evaluated per ground, per
  usage site, not assumed to transfer because the token passed once
  somewhere else. If a project's token set has both a light-ground and a
  dark-ground variant of the same semantic role (e.g. `--ink-2` /
  `--ink-2-dark`), that split exists for exactly this reason — use the
  variant matching the actual ground under the text, not whichever name is
  more familiar.
- **Contrast applies to the hero visual, not only to text.** The rule above
  is written around text-over-a-plate, but a purely decorative hero
  element (an illustrated panel, a diagram's own background shape) can
  fail the same way and is easy to miss because no contrast checker
  evaluates it at all. Confirmed case: a hook scene's hero illustration sat
  at **1.05:1** against its own ground (`#1A1A1A` panel on `#131516`
  canvas) — technically present, but visually indistinguishable from its
  background at any viewing size, and completely invisible once downscaled
  to thumbnail/grid scale. This is a hook-legibility failure (gate item 1)
  as much as a contrast failure — a hero visual with no real separation
  from its ground reads as an empty frame, no matter how carefully its
  *content* was drawn.
- **Hero copy occupies 60-80% of the available width.** Distinct from the
  vertical-fill rule above — this is a horizontal-occupancy check on the
  headline/hero text block itself, not the scene's overall vertical fill.
  Copy set narrow in a wide safe column reads as under-scaled even when the
  font size technically clears the type floor.
- **Layout variety.** A vertical canvas still supports asymmetry — a split
  background, an off-center hero element, a full-bleed image with an
  overlaid caption band, a two-tier stack. Nine scenes that are all "one
  centered flex column on a flat background" reads as the single most
  common and most avoidable faceless-video defect (see *Posture* below);
  budget at least one structurally different frame per 3-4 scenes.
- **Safe areas, and they must be consumed, not just documented.** The
  Shorts player overlays UI on the composition. A project should declare
  these as CSS custom properties (`--safe-top`, `--safe-bottom`,
  `--safe-left`, `--safe-right`) *and every scene must actually read them* in
  its layout — declaring the tokens in one file while eight others hardcode
  raw pixel offsets is the gap that lets content drift into a reserved zone
  unnoticed. Approximate reserved zones, given both as a percentage and as
  the literal pixel value at the canonical 1080×1920 canvas — a project's
  tokens should equal the pixel figures below, or the deviation should be
  recorded with a reason (verify the percentages themselves against a
  current device):
  - **Right edge ~15% (162px)** — like/dislike/comment/share rail.
  - **Bottom ~20% (384px)** — title, channel, audio attribution.
  - **Top ~10% (192px)** — search and camera icons.

  The center-left column is the only zone guaranteed clear. Debug-overlay the
  zones (see *Layout validation* above) rather than eyeballing pixel math per
  scene — and re-check every scene after any late change to a block's height
  or `justify-content`, since a spacing fix in one scene silently regressing a
  *different* scene's safe-area compliance is the single most common way
  a violation ships (fixed elsewhere, never re-verified where it originated).

  **The safe area binds transformed, rendered pixels — not the CSS box the
  padding was written against.** `padding` constrains a box's *layout*; it
  says nothing about where that box ends up once a `transform:
  scale()`/`translate()` sits between it and the canvas. A Ken Burns wrapper
  around a safe-padded `.stage` (`.frame-zoom { transform-origin: 50% 40%; }`
  scaling toward 1.045 over the scene) maps the padded edge outward by the
  same factor it scales the box — a scene where every token is declared,
  consumed, and individually correct can still ship ink past the real line,
  because the *source* is correct and only the *rendered result* isn't.
  Confirmed on `videos/peeling-not-progress`'s 2026-08-31 round-6 render:
  three zoomed scenes each overshot the real line by 5-10px this way despite
  passing gate item 7a below, and a fourth, non-zoomed scene overshot by a
  different mechanism — a text element's own entrance `transform:
  translateY()` pushing it past the line for a ~150ms transient before
  easing back to a compliant resting position. Two fixes, matched to the
  mechanism: for a scene-wide zoom, derive the padded edge from the scene's
  own max scale and origin rather than reserving a flat token —

  ```css
  /* Neutral defaults so an unzoomed scene's math reduces to the plain token. */
  --zoom-max: 1; --zoom-origin-x: 540px; --zoom-origin-y: 960px;
  --safe-margin: 4px;  /* guard band for antialiasing / subpixel rounding */

  --safe-bottom-zoomed: calc(1920px - (var(--zoom-origin-y)
    + (1920px - var(--safe-bottom) - var(--safe-margin) - var(--zoom-origin-y)) / var(--zoom-max)));
  --safe-right-zoomed: calc(1080px - (var(--zoom-origin-x)
    + (1080px - var(--safe-right) - var(--safe-margin) - var(--zoom-origin-x)) / var(--zoom-max)));

  /* The two above only cover the edges FARTHER from the zoom origin than
     the origin itself (bottom/right, for the common case of an origin at
     or below/right of canvas center). A zoom whose origin sits off-center
     toward the top (e.g. 50% 40%, a common framing for a hero plate) maps
     the NEARER edges -- top and left -- outward too, by the same inversion
     in the other direction. Add these two whenever the origin isn't
     centered, or a top/left overshoot ships silently the same way a
     missing bottom/right derivation would have. */
  --safe-top-zoomed: calc(var(--zoom-origin-y)
    - (var(--zoom-origin-y) - var(--safe-top) - var(--safe-margin)) / var(--zoom-max));
  --safe-left-zoomed: calc(var(--zoom-origin-x)
    - (var(--zoom-origin-x) - var(--safe-left) - var(--safe-margin)) / var(--zoom-max));
  ```

  Use the `-zoomed` value in `.stage`'s padding in place of the flat token,
  with `--zoom-max`/`--zoom-origin-*` set to the scene's own `fromTo('#zoom',
  {scale:1}, {scale:N, ...})` values. This *replaces* a hand-tuned `+Npx`
  allowance, which is sized against whatever `--safe-bottom` happened to be
  when it was measured and goes silently wrong the moment the token or the
  scene's own scale/origin changes later — exactly what happened here (an
  allowance computed against a pre-correction token undershot the corrected
  line by 5-10px, with nothing to flag it). For a transient caused by an
  element's own entrance transform, don't paper over it with more margin —
  fix the mechanism: drop the position-changing part of the entrance (keep an
  opacity-only cross-fade) so there is no transient offset to overshoot with
  in the first place. A margin increase hides the symptom on this render and
  reappears the next time the settled position happens to sit close to the
  line.

### The hook

Retention is decided in the first ~2 s of a short. The long-form window is
**genuinely unresolved** — this file has said ~8s, the v2 package ~15s, neither
measured on a real channel; see *Long-form structure*'s hook-window bullet, and
record which number a beat sheet assumed rather than inheriting one silently.
Structural consequences, which hold either way:

- **Cold open.** No logo, no fade-from-black, no title card. Frame zero *is*
  the hook — the strongest visual claim of the piece, already composed (see
  mandatory rule 4).
- **The payoff itself must land inside that window, not just the setup.** A
  hook that poses a question at t=0 and doesn't resolve it (a reveal, a
  number, a twist) until t=3s has burned the entire retention window on setup.
  For a short, target the payoff visible by ~2s — if the beat sheet can't get
  there, the hook concept is wrong, not just its timing.
- In shorts, engineer the loop: design the last frame to hand back toward the
  first — matched background colour, matched hero position — so a replay
  feels seamless rather than requiring the viewer to notice a hard reset.
  Replays count as retention; a static, unrelated endcard as the true final
  frame wastes this for free. **The loop is an audio event as much as a
  visual one** — a mix that fades to silence before the cut (a BGM tail fade
  left at its default length instead of trimmed for this shorter edit) hands
  the replay a dead beat even when the picture matches perfectly. Check both
  ends the same way: matched frame-diff for the picture (*Verification
  loop*), matched RMS-vs-time for the mix (see *Audio is a first-class
  composition layer*'s loop-boundary note) — confirmed necessary on a real
  render where a frozen final scene and a BGM tail fading to true silence by
  the last second combined into a loop that handed back nothing at all.
- **Every beat past the value delivery earns its place.** Once the second
  beat has delivered the central value, each later beat must carry
  evidence, explanation, or an action supporting it — not runtime filler.
- **The closing beat is one specific, lesson-tied action** — "patch-test
  before you use retinal," "check the label for the real percentage" —
  never a generic subscribe/like card. A generic close is the default this
  whole category falls into; see *Posture* below for the same principle
  applied to motion and layout.

### Chapters map to the beat sheet

Chapters are the beat sheet made public. Group beats into 3+ chapters, first
timestamp at 0:00, each ≥ 10 s. Name chapters as payoffs ("Why the label
lies"), not sections ("Part 2"). If the beat sheet can't produce coherent
chapters, the beat sheet is wrong — fix it there.

### The end screen is a scene

The last 5–20 s of long-form carry end-screen elements (video/playlist/
subscribe overlays) that YouTube draws *on top of* the composition. So the
final scene is designed as a frame for them: reserved negative space where the
elements land, motion calmed, no text in the overlay zones. Its job is the
next-video handoff — a composition that ends on its content peak wastes the
highest-intent moment the video has. (For a short, the equivalent job is the
loop, above — there is no end-screen overlay.)

### What "interactive" can actually be

No true in-player branching exists. The real inventory:

- **End screens + cards** → chained-video branching ("choose path A or B"
  as two end-screen elements pointing at two videos).
- **Chapters + pinned comment / description timestamps** → viewer-seekable
  structure ("skip to your skin type at 2:14").
- **Pinned comment and polls** → the feedback channel that scripts the next
  video.
- **Shorts** → one related-video link; branching happens across shorts, not
  inside one.

Design branching as a *graph of videos* with the composition treated as one
node — never promise in-video interactivity the player cannot deliver.

### Audio mastering

- Narration and music are normal, in-composition citizens — see *Audio is a
  first-class composition layer* above for the mechanics. What stays banned is
  wall-clock-driven audio (an autoplaying `<video>`'s own audio track, an
  `<audio>` element left to free-run instead of being scheduled by
  `data-start`).
- Master audio to YouTube's ~-14 LUFS integrated / -1.5 dBTP normalization
  target as a **post-render** step; louder than that is simply turned down by
  the platform.
- **Measure true peak on the final encoded deliverable, not the PCM
  intermediate `loudnorm` ran against.** Lossy encoding (AAC in particular)
  raises intersample true peak — confirmed case: a two-pass `loudnorm`
  correctly hit -1.50 dBTP on its PCM output, the project recorded that as
  final, and the shipped MP4's AAC encode had actually pushed true peak up
  to **+0.5 dBFS** — decoding the shipped file back to PCM and re-measuring
  reproduced the overshoot exactly. Leave headroom for this: target
  something like `TP=-2.5` (not `-1.5`) on the `loudnorm` pass specifically
  so the post-encode file still lands under -1.0 dBTP, then re-measure
  `ebur128` on the actual shipped file before calling mastering done — a
  measurement against the intermediate is not evidence about the
  deliverable.

Captions are their own deliverable, with the same weight as the mix — see
*The captions* below, not a bullet point here.

### The captions

Captions carry the same status as the thumbnail: produced and checked before
publish, not improvised from whatever transcript data happens to already
exist. **The raw material existing is not the same as the caption existing.**
A project can have a full set of per-clip word-level transcripts and still
ship with no on-screen captions and no sidecar file, because nothing turned
that data into either — a real, observed gap in this project's own catalog
(see *Consistency across a channel's videos* below), not a hypothetical.

**A silent, type-carried video still ships a sidecar.** The production order
below (steps 1-5) is entirely transcript-predicated — it starts from ASR on a
mixed VO, which is the right call for the common case but leaves a gap for a
project with no voiceover at all, where 100% of the video's language is
already on-screen kinetic type (a legitimate, deliberate choice — see
*Audio is a first-class composition layer*'s note on silence). "No speech to
transcribe" correctly rules out ASR; it does not rule out the caption
deliverable itself, because a captions or screen-reader user watching that
video gets nothing without one. Hand-author the sidecar `.srt`/`.vtt`
directly from the storyboard's copy deck and the composition's own scene
timings (`data-start` + each beat's entrance offset) instead — no transcript
step needed, since the text and its exact timing are already authored
artifacts, not something that has to be extracted from audio. `videos/
peeling-not-progress` shipped with zero captions under a defensible reading
of the transcript-predicated rule above (correctly no VO, incorrectly
concluded therefore no captions) until this gap was named; the fix took one
hand-authored `.srt`/`.vtt` pair, no ASR involved.

Two outputs, and most projects need both:

- **Burned-in, beat-timed typography.** The primary deliverable for anything
  vertical/muted-first (a short). Word-synced on-screen text inside the safe
  zone, built as its own sub-composition included on the root timeline like
  any other scene, driven by the same time model as everything else in this
  file — no separate rendering path, no library that plays on its own clock.
  Check the project's shared catalog for an existing caption-skin component
  (type treatment, highlight colour, entrance/exit beat) before authoring a
  new one — a caption skin is exactly the reusable component *Consistency
  across a channel's videos* names, and a working precedent is worth reusing
  rather than reinventing per video.
- **Sidecar `.srt`.** Required for long-form (YouTube's own caption track,
  searchable, accessible) and cheap once the transcript exists. Not a
  substitute for burned-in type on a short — a short is watched muted inside
  the platform's own UI chrome, which does not surface an uploaded `.srt` the
  way the desktop player does.

**Line and word discipline, regardless of skin.** Maximum two lines on
screen at once, roughly 3-6 words per line — a caption is a glance, not a
paragraph. Don't let a caption repeat verbatim what a decorative on-screen
label already says in the same beat unless the repetition changes meaning
(the label names a category, the caption carries the actual sentence);
otherwise it's the same phrase read twice for no reason, spending the one
frame that could have carried new information. A `.vtt` export is an
accepted alternative or addition to `.srt` where the publish target wants
one.

**A hand-authored sidecar needs its own minimum cue duration — mirroring
every on-screen element's own entrance timestamp is not the same as
authoring readable cues.** When there's no VO to anchor cue timing against,
it's tempting to derive each cue directly from the composition's own beat
schedule (one cue per element, starting exactly when that element enters).
Confirmed failure mode: doing this mechanically produced a sidecar where 10
of 29 cues ran under 0.5 seconds, the shortest at 0.15s — nowhere near
readable, let alone accessible. Enforce a real floor (~1.0s minimum
on-screen time per cue) and merge co-occurring on-screen copy into one cue
rather than one cue per element; a caption track's pacing is a distinct
authoring decision from the visual beat schedule, not a direct mirror of
it, even when both are hand-authored from the same source material.

Production order:

1. Generate a word-level transcript of the **final mixed VO**, not a draft
   take, using the project's transcribe tooling (e.g. `hyperframes
   transcribe`). Re-generate after any voice swap or retime — a transcript
   from an earlier take silently desyncs from the shipped audio, the same
   stale-sidecar risk that already applies to `.words.json` files generally
   (see the re-timing cascade section above).
2. Hand-correct proper nouns, ingredient names, and coined/technical terms —
   a generic ASR pass will mangle exactly the vocabulary a skincare-education
   video depends on getting right. This is the audio section's TTS-
   mispronunciation correction pass run in the other direction: there the fix
   is respelling the *TTS prompt*; here the fix is correcting the
   *transcript text* against what was actually said.
3. Build caption beats from the corrected transcript, reusing the catalog's
   caption-skin component where one exists.
4. Export the `.srt` from the same corrected transcript — one source of
   truth for both outputs, not two independently-timed passes that can drift
   from each other.
5. Proofread every caption line for broken fragments and transcription
   errors — a hand-corrected proper noun (step 2) doesn't guarantee the rest
   of the sentence around it reads cleanly.

**Competitive research, the same way the thumbnail section uses one.** Before
committing to a caption style, `vidiq_video_transcript` against a handful of
outlier videos in the niche — the same outlier set the beat sheet's own
pre-production research already pulled — shows real caption pacing and
phrase-grouping conventions that are currently winning. Feed that into the
beat-timed grouping decision the same way `vidiq_similar_thumbnails` feeds the
thumbnail's competitive check.

**Verification, same discipline as everything else in this skill.** Extract a
frame at a caption's mid-hold, not just its entrance beat, and confirm the
text is legible inside the safe zone at the target canvas size (see *9:16-
native composition*'s type floor). Play the `.srt` back against the actual
rendered audio, not the pre-mix draft, to catch timing drift introduced by a
late retime.

**Naming note, from a real defect found in this project's own catalog:** a
file literally named `caption.txt` turned out, on inspection, to be the
video's YouTube *description/CTA copy* — not a caption/subtitle file at all.
Its presence across most of a catalog's projects can look, at a glance, like
the caption requirement is satisfied when it is an entirely different
deliverable. Don't infer caption status from a filename; check for an actual
burned-in caption composition or a real `.srt`.

### The thumbnail

The thumbnail is a deliverable, not a by-product of rendering — it is the
other half of the click decision alongside the title, and a video with
flawless cadence and a lazy thumbnail still doesn't get watched. Produce and
score it before publish, the same way chapters and end-screen targets are
produced before publish, not improvised from whatever frame is on screen when
someone remembers.

Two legitimate production paths, chosen by what the best candidate moment
actually needs:

- **Extract, grade, finalize.** Pull a real frame from the finished render at
  a genuine peak moment — the hook's payoff, the highest-value promise, a
  curiosity-gap beat — apply a light, video-specific grading pass
  (contrast/saturation/sharpen), and ship that. No separately authored
  composition. This is the default when the render already contains a frame
  that reads as a thumbnail on its own.
- **Authored or generated.** When no single rendered frame carries enough on
  its own (the payoff is inherently a motion beat, or the composition never
  puts the hero element and a legible headline in the same frame), build a
  dedicated thumbnail image instead — a small authored composition/still, a
  generated plate via the project's image tooling, or vidIQ's own generator
  (`vidiq_generate_thumbnail`) composited with the video's real title text.
  Don't force the first path just to avoid a second asset.

Rules that apply to either path:

- **Same frame-zero discipline, applied to a still.** A candidate pulled
  mid-crossfade, mid-strike, or mid-tween is the exact static-hold/
  transition-midpoint failure from *Verification loop*, just cropped to one
  frame — check it the same way, not by eye at full size.
- **Legible at grid size, not just at 1080p.** A thumbnail is browsed in a
  scroll grid around 120×67px before anyone opens it full-size. Downscale the
  candidate to that scale (the same phone-viewing-simulation habit used for
  body-text validation) before judging whether the subject or any text on it
  still reads.
- **A prior video's grade is not portable by default.** A filter chain
  (vignette, contrast curve) tuned for one video's palette can read as a
  muddy cast on a different video's background — re-derive the grade from the
  current video's own palette rather than copying values across videos with
  different grounds.
- **Title and thumbnail are one decision, not two.** Score them together —
  `vidiq_score_title` alongside `vidiq_score_thumbnail` — and check
  `vidiq_similar_thumbnails` for what's already crowding the result page
  before committing, the same competitive pass the pre-beat-sheet research
  step already runs for topic/title. Iterate a chosen candidate with
  `vidiq_refine_thumbnail` rather than re-generating from zero each round.
- **File convention.** Keep candidates and the shipped choice together and
  named — e.g. `assets/thumbnail/`, each candidate labeled by what it's
  testing (a moment, a crop, a grade) plus one clear final — so a later round
  can see what was already tried instead of starting over.

### The delivery manifest

The publish envelope isn't done when every asset exists on disk — it's done
when whoever asked for the video can find each one without going and
listing the project directory themselves. A rendered MP4 sitting next to an
`.srt` sitting next to three thumbnail candidates is not a *delivered* video
if the response that ships it just says "done."

Before calling a project done, report a manifest — in the handoff message
itself, or as a `DELIVERY.md` alongside the project for anything with more
than a couple of scenes — naming every deliverable by its **real path**, not
a description of what it is:

- **Render.** The exact filename and folder (`renders/<name>.mp4` or
  equivalent), duration, resolution, and which mastering pass it carries
  (loudness-normalized? to what target?). If more than one render sits in
  the folder — iterations, a pre-mastered pass — say which one is the
  publish candidate; don't make the reader infer it from timestamps.
- **Captions.** Confirm the burned-in composition shipped inside the render
  (nothing separate to attach) *and* give the sidecar `.srt`'s path.
  Produce the `.srt` even for a short once the transcript exists — it's
  cheap, and gives the operator something to paste into YouTube's upload
  flow regardless of whether the platform surfaces it in-player the same
  way it does for long-form. See *The captions* above for why it must carry
  the corrected transcript's real word timing, never an estimate.
- **Thumbnail.** The finalized file's path (see *The thumbnail*'s file
  convention above) — not "candidates exist in `assets/thumbnail/`."
- **Full source list.** Journal names, DOIs, or URLs for every on-screen
  citation, ready to paste into the description — see *What must never
  reach a rendered frame* above for why the frame itself only ever carries
  the short human-readable form.
- **Chapters** (long-form) — the actual timestamp list, ready to paste into
  the description, not "derived from the beat sheet, see STORYBOARD.md."
- **Pinned comment / description copy**, if drafted this session.
- **End-screen / next-video target**, if this piece is part of a branching
  set (see *What "interactive" can actually be*).

This is a reporting discipline, not new production work — every item above
should already exist by the time production-loop step 13 is reached. What a
missing manifest costs isn't the asset; it's the ten minutes the person on
the other end spends re-deriving where everything is, or publishing without
one of them because they didn't know to look.

## Posture: what makes faceless content not look generic

The default output of this whole category — AI voice, stock B-roll, centered sans
type, slow zoom, ambient pad — is the thing to design against. The levers that
actually differentiate:

- **A single consistent grade and grain across every plate.** Mixed-source imagery
  reads as scraped. One grade, one grain, one edge treatment unifies it more than
  any transition.
- **Motion that means something.** Depth encoding sequence, size encoding
  magnitude, position encoding time. Decorative motion is free to make and free to
  ignore — and decorative motion added to make a static scene *measure* better on
  a blankness scanner without actually adding a beat is worse than no motion: it
  hides the real cadence problem instead of fixing it.
- **Type as the performer.** Typography carries the performance even when there
  is narration — weight, rhythm, and when a word arrives are doing real work
  alongside the voice, not just captioning it.
- **Not every element gets the same entrance.** A shared fade-and-rise on
  every beat in every scene reads as one template no matter how varied the
  content is. This file's own canonical `.beat` pattern (*Consuming `--p` in
  CSS* above) is a starting shape to build variants from — a scale pop, a
  wipe, a stagger on a different curve — not the one entrance every element
  in a project should use. Pick the variant from what the beat is doing —
  *Motion idiom by narrative function* is the vocabulary. And **the trap is the
  inherited default**: a timeline-wide `defaults: { ease }` gives every tween in
  the file one signature while the source shows almost no explicit eases, so a
  grep says "varied" and the render says "template".
- **Boundary treatment is format-scoped.** Hard cuts on a timing grid for a
  Short; a 2-3-type transition system for long-form; never a plain crossfade
  across a ground change in either. The retention argument runs unmeasured in
  both directions — see *Cuts, crossfades, and transitions*.
- **Layout variety, not just palette variety.** Alternating background colour
  scene-to-scene is not the same as alternating structure. Nine scenes that are
  all a single centered flex column — differing only in background colour and
  word count — read as one template repeated, even with perfect color discipline.
  Vary the actual composition: a split layout, an asymmetric hero, a full-bleed
  plate, a grid of cards — at some deliberate cadence across the piece.
- **Spend boldness once.** One signature component per video. A spec where
  everything is dimensional reads as a demo reel, not a piece. This does not
  mean *no* component should be bold — a video with no signature moment at all
  is the opposite failure, equally generic.
- **Fill the frame you were given.** Especially in 9:16: a well-designed small
  element in a large empty canvas is not restraint, it's an unfinished layout.
  See *9:16-native composition* above.
- **When a brief asks for energy, make it measurable.** "High-energy,"
  "aggressive," "punchy" are directions with concrete correlates: cut rate
  (cuts, not crossfades), state-change cadence, scale contrast between hero and
  support elements, and canvas occupancy. A design-system translation is
  allowed to swap the brief's literal colors/fonts for an on-brand palette, but
  it must preserve those measurable qualities — translating "neon glow,
  Impact type, aggressive" into a calm, low-cadence, low-occupancy composition
  is not a style translation, it's a content miss. Check the brief's own
  adjectives against the finished cadence/occupancy numbers at review time,
  the same way you'd check a claim against a source.
- **Silence is a genuine choice, not the default.** Some beats (a B-roll
  interlude, a breather) can and should run with no VO, letting motion and
  music carry pacing alone — but that is an authored exception inside an
  otherwise-narrated piece, not the assumed baseline for the format. **A
  whole video with no VO needs the reason recorded**, the same way a >50s
  duration (production-loop step 2) and an all-illustrated video (*Asset
  protocol* rule 6) both require one — `BRIEF.md`'s `VO_MODE: silent` line
  in `videos/peeling-question-open` is the shape this takes: a one-line,
  checkable record, not something inferred after the fact from the absence
  of a voiceover file. This still requires a real mix (BGM/SFX, mastered —
  see pre-render gate item 13) and, for a short watched muted-first, the
  hand-authored sidecar captions *The captions* section requires even
  without ASR to drive them — "silent" describes the VO track, never the
  whole audio layer or the caption deliverable.

## Companion skills

| Skill | Use it for |
|---|---|
| `frontend-design` | Read before any visual spec. Taste and token discipline. |
| `web-artifacts-builder` | Interactive HTML deliverables and preview harnesses — not for render compositions. |
| `design:design-system` | Extending the component/token library. Never draw a one-off glyph into a composition. |
| `design:design-handoff` | The format for handing a spec to a build lane. |
| `design:design-critique` | Review pass on rendered frames, not on code. |
| `theme-factory` / `canvas-design` | Palette and static key-art exploration before motion. |
| `marketing:draft-content` | Titles, descriptions, hooks — the publish envelope. |
| `searchfit-seo:*`, vidIQ tools | Topic/title/outlier research **before** the beat sheet (it changes the beats); competitive caption-pacing research via `vidiq_video_transcript` before the caption pass — see *The captions*; thumbnail generation, scoring, and refinement **after** the render — see *The thumbnail*. |
| Higgsfield / HyperFrames MCP | Plate generation and cloud render. Both are asset/infra tools, not design authorities. |
| `hyperframes-animation` | The implementation library behind this file's motion vocabulary: atomic rules in `rules/`, multi-phase scene blueprints in `blueprints/`, and the scene-transition registry in `transitions/`. *Motion idiom by narrative function* and *Long-form structure* name its files exactly — read the rule, don't reconstruct it from the label. |
| `hyperframes-keyframes` | Punch-ins, reframes, and camera moves on a wrapper that is not itself a timed clip. |
| `hyperframes-core` | The composition contract, and `references/composition-patterns.md` §"C. Multi-scene merge" — the pattern behind persistent actors and phase-based scenes. |
| `hyperframes-cli` | The dev loop, and `references/lint-validate-inspect.md:74-99` — the `*.motion.json` sidecar's four assertion kinds and failure codes. |

**Names that do not exist** — each was reached for and found absent, so don't
spend a round trip rediscovering them: no `hyperframes docs motion` topic, no
`check --motion` flag (the sidecar is auto-discovered), no render-level motion
blur (`motion-blur-streak` is hand-authored SVG/CSS), no "chapter composition"
primitive (the pattern is the multi-scene merge; nesting `data-composition-src`
two levels deep is a confirmed defect). `hyperframes beats` exists but is
**music** beat detection; narration word timings come from `hyperframes
transcribe` (`transcript.json`) or `media-use`'s `--words`.

## Design tokens across sub-compositions

Once a project has more than one composition file, hand-pasting the same
`#root { --paper: … }` token block, `@font-face` declarations, and GSAP
`<script>` tag into every sub-composition is a real trap: it works, and it
means a single palette change becomes an N-file edit with N chances to drift.
Prefer a single source-of-truth `tokens.css` the project actually imports or
inlines-by-build-step into each sub-composition, and check for tokens that are
declared but never referenced anywhere (a dead accent color, an unused
elevation level) — that's a sign the token file and the compositions have
already started to diverge.

**An inlined token block that OMITS one token fails silently, and the failure
looks like a layout bug rather than a token bug.** This is the paste-per-file
trap's sharpest form: the shared `tokens.css` is correct, the scene's CSS is
correct, and the inlined copy is simply missing one custom property the scene
uses. CSS then discards the whole declaration as invalid — `padding-right:
calc(var(--safe-right) + var(--endscreen-right))` with `--endscreen-right`
undefined does not fall back to `--safe-right`, it drops the padding entirely.
Confirmed on a real render: an end-screen scene ran full-bleed into the reserved
right zone, and the **hard safe-area gate caught it on 41 frames** while both
the token file and the scene source read as correct. `grep -c endscreen` was
**3 in `tokens.css` and 0 in the inlined block** — a one-command diagnosis that
is invisible from reading either file alone.

So when a scene's own CSS looks right and its rendered geometry does not, diff
the inlined token block against the source of truth *before* debugging layout.
And prefer a build step that copies the token block mechanically over one that
copies it by hand: every token added to `tokens.css` after the paste is a latent
version of this.

**A `tokens.css` that exists and is correct but is never actually loaded by
anything is a worse version of the same trap, not a milder one** — it
passes an "does a token file exist" audit while doing nothing. Confirmed
case: a project's `tokens.css` had the correct type scale, the correct
per-ground contrast-safe secondary-ink variants, and the derived
Ken-Burns-aware safe-area math already worked out — and no scene actually
referenced it; a `<link rel="stylesheet">` pointing at it did not reliably
resolve custom properties through the render pipeline (confirmed by
measuring `--safe-top` etc. as empty on a compiled render), so every scene
had silently fallen back to re-declaring its own values inline, some of
them wrong. Two fixes, in order of preference: (1) confirm a `<link>` or
`@import` to the shared file actually resolves on a real compiled render
(measure a token's value, don't assume the reference worked because
`check` didn't complain), or (2) inline the token file's *values* into
each composition's own `#root` block as the reliable fallback — the
discipline that matters is having one source of truth to copy from, not
necessarily a live runtime fetch. Either way, grep the compositions for the
token file's own filename or its distinguishing values, not just for the
file's presence on disk, before trusting a "tokens are centralized" claim.

## Consistency across a channel's videos

*Design tokens across sub-compositions* (above) covers drift **within** one
project's multiple scene files. The same trap exists one level up, **across**
a channel's separate video projects, and is easier to miss because each
project looks complete in isolation — it only becomes visible when the whole
catalog is compared side by side, project by project, not assumed from the
existence of a shared catalog folder.

What should be inherited channel-wide, and how to check whether it actually
is:

- **Palette and type tokens.** One canonical `tokens.css`, referenced (or
  deliberately copied with a comment naming the source of truth) by every
  project on the channel — not re-derived from memory per video. Audit by
  grepping every project's token file for the same handful of hex values; if
  two projects define `--ink` differently with no stated reason, that's
  drift, not a deliberate palette evolution.
- **The audio mastering chain.** The EQ/compressor/de-ess/limiter chain (see
  *Audio mastering*) is a channel-level decision, not a per-video one — it's
  what makes a channel's narration sound like the same show. Reuse the
  `data-fx-chain` verbatim across projects unless there's a specific reason
  (a different mic, a different VO voice with different spectral problems) to
  deviate, and note the reason when it happens.
- **The caption skin.** The type treatment, highlight colour, and
  entrance/exit beat for burned-in captions — see *The captions* above. This
  is the clearest case of a component that should exist exactly once and be
  referenced everywhere, checked for the same way the production loop's
  Component-check step already checks for a reusable visual component.
- **The thumbnail's structural template, not its grade.** *The thumbnail*
  section already establishes that a colour grade doesn't port between videos
  with different backgrounds — that rule stands. What *should* stay
  consistent is the structural template underneath the grade: where the
  headline sits, how much of the frame the hero subject occupies, whether a
  source/credibility chip appears in the same corner every time. A channel
  where every thumbnail is instantly recognizable as "that channel" before
  the title is even read is doing this on purpose, not by accident.
- **The shared catalog location itself.** If a project keeps a shared catalog
  for imagery and components (see *Asset protocol* and the Component-check
  production-loop step), tokens, audio chains, and caption skins belong in
  that same catalog as first-class citizens — not scattered as one-off files
  duplicated into each project's own `assets/`. A catalog that indexes plates
  and components while palette and audio-chain files are silently
  copy-pasted per project carries the exact drift risk the plate-catalog rule
  exists to prevent, just for a different asset type.

**Audit method — check a real catalog before assuming consistency; don't infer
it from a shared catalog folder existing.** Enumerate every video project and
check, per project: does a tokens file exist and do its values match the
others; does an audio fx-chain exist and is it the same chain; does a caption
mechanism exist and is it the same mechanism; does a thumbnail exist. A
catalog where a few projects fully agree and the rest have none of the above
is not "mostly consistent" — it's one working precedent that never got
applied, which reads identically to no precedent at all from a new project's
starting point. Confirmed in this exact shape in one real project catalog: two
projects shared identical palette tokens and an audio chain, two others
independently built the same burned-in-caption mechanism (a dedicated
`captions.html` sub-composition plus a shared caption-skin file) — but no
project combined captions with a thumbnail, no convention document named
either pattern as "the" approach, and the majority of projects had neither.

## Failure modes worth naming

- **Missing `box-sizing: border-box` combined with a flex child's explicit
  small `flex-basis`.** Two defects that compound: (1) without the
  border-box reset (mandatory rule 3 above), an element with both an
  explicit height and padding renders larger than declared, by exactly the
  padding total — invisible from source, caught only by comparing
  `getBoundingClientRect()` against `getComputedStyle().height` on a real
  render. (2) Even after fixing (1), a flex child given a small explicit
  `flex-basis` (e.g. `flex: 0 0 220px`) to keep a zone's size independent of
  its content can still render far taller than that basis — confirmed at
  332px against a declared 220px — because `min-height: auto` (the flex
  item default) resolves to the content's min-content size and silently
  overrides a smaller explicit basis unless `min-height: 0` is also set on
  that child. Both defects reproduce identically across renders, don't
  depend on `--safe-*` token values, and surface only as scattered
  `info`-level (non-blocking) `container_overflow`/`canvas_overflow`
  findings in `npx hyperframes check` — a project can ship with citation
  chips or a CTA silently pushed into, or entirely out of, the reserved
  safe zone while reporting a clean check. Fix both at once, project-wide:
  `*, *::before, *::after { box-sizing: border-box; }` as the first rule in
  every composition, plus `min-height: 0` on every flex child carrying an
  explicit small basis.
- Building the composition before the beat sheet, then re-timing everything.
- Proof-scaling a component into a big empty canvas and calling it a scene —
  especially in 9:16, where the failure reads as "small fonts" even when the
  type itself is a reasonable size (see *9:16-native composition*).
- Landing every beat in a scene's opening two seconds, then freezing for the
  rest of its narration — passes a blankness scanner, fails the actual cadence
  target (see *Verification loop*'s static-hold check).
- Adding decorative idle motion to make a frozen scene score better on a
  metric, instead of fixing the underlying lack of beats.
- Using a generic easing on everything, which reads as PowerPoint.
- More than one accent colour competing for the eye in a single frame.
- Nine scenes that are all the same centered single-column layout — palette
  variety without structural variety.
- Crossfading between two scenes with different background colours, producing
  a muddy near-blank transition midpoint that only shows up in a frame
  extracted at the exact midpoint — when `push-slide` and `squeeze` cross a
  ground change without blending at all, and `blur-crossfade` at least masks
  the clash.
- Applying the Shorts cuts-only rule to long-form: every boundary a hard cut,
  every per-scene gate green, and a video that reads as slides.
- An exit animation before a transition fires — the transition IS the exit, so
  fading out first makes it a jump cut with a dip.
- Rebuilding the same diagram in consecutive scenes instead of merging them and
  rearranging the actors: two files that resemble each other, not one subject
  that evolves.
- A chapter transition that is *bigger* but lands the next act on its setup.
- Reading `motion.enabled: false` as "motion verification was disabled." No
  sidecar was ever written; nothing was switched off.
- `*.motion.json` assertions aimed at containers rather than copy elements, so
  an overpainted or never-wrapped text node passes clean.
- `sine-wave-loop` as the default answer to a quiet stretch, when its own rule
  file says reach for it last and would rather have no motion than bad motion.
- `hyperframes beats` for narration timings (it is music beat detection), or a
  render-level motion-blur flag (there isn't one).
- Counting ease variety by grepping explicit `ease:` strings while a
  timeline-wide `defaults: { ease }` supplies the rest — 8 explicit hits over
  128 tweens actually carrying it.
- Reading a healthy whole-video active-step share as "well paced" on a piece
  whose every scene has the same enter → wash → hold shape.
- **Disproving an external report's magnitude with a source-level number, or
  with a figure the project already wrote down.** This is the sharpest
  confirmed case in this file, because the disproof was the error. In this
  channel's one long-form review, every structural claim reproduced ("28
  boundaries, all hard cuts"; "fade + slide + `power3.out` everywhere") and
  both magnitudes were called false — wrongly, twice, in the two specific ways
  this file already warns about. "12.7% visible motion" was rejected against
  the project's own `DELIVERY.md` figure of 14.8%; re-running that project's
  unmodified cadence script on the shipped MP4 returns **12.7%**, and the
  recorded 14.8% is stale despite being written after the render. "Holds of
  four to six seconds" was rejected on a **median trailing hold of 2.14s** —
  but that measures the gap from a scene's last *authored tween* to its end,
  not perceived stillness; the pixel measurement gives a median longest quiet
  run of **5.0s** with 21 of 29 scenes inside the reported 4-6s band. A
  reviewer describing what a viewer sees is making a claim about pixels, and
  only pixels answer it. Verifying a report is not the same as reaching for
  the nearest available number, and a project's own delivery doc is a claim
  too. **The rule binds when you CITE a number, not only when you measure
  it** — the same session that wrote this bullet then sent a peer a line
  range for one of its own cross-references that was four hours stale, quoted
  from working notes rather than re-read from the file, and was corrected by
  the peer. A measurement decays the moment anything upstream of it changes;
  re-read before repeating, including your own.
- Authoring a fix into a generated file. The change is on disk, the render
  shows it, `check` passes, and the next `npm run build` discards it — grep the
  build scripts for the filename before the first edit, not after.
- Choosing a transition on its ground behaviour alone. Ground-blending and
  safe-area transit are independent: a translating push never composites two
  grounds and still drags text through every reserved zone.
- Handing over a fresh render as a publish candidate. Mastering is a
  post-render step, so a re-render silently reverts it — measured at 9.6 LU
  below the previous deliverable on a file otherwise ready to ship.
- Re-fixing a gate's broken assumption in the same shape it broke in. Twice
  here the estimator was rewritten and the premise "there is one background"
  survived; only the version that stopped assuming a count held.
- Shipping a hard-gate fix behind a single negative control. Two are needed:
  one proving it still fires, one proving the fix did not over-suppress.
- Glow used to create hierarchy. Use elevation, weight, and contrast instead.
- Rendering at 60fps for content that has no fast motion — doubles cost, changes
  nothing a viewer can see.
- Treating the end screen (or, for a short, the loop) as decoration rather
  than as the next-video/replay mechanism.
- An `<img>` with no constrained box, which pops the layout mid-render — check
  every image, including ones added in a late review pass.
- Inventing an absolute filesystem path for an asset instead of using the
  project's resolved asset root; it will not exist on the render machine.
- Two elements positioned with independent absolute `top`/`left` standing in
  for a layout relationship, which collapses on any aspect or string-length
  change.
- A clip that only redeclares `top`/`left`/`width` off the mandatory-rule-2
  skeleton (`.clip { position: absolute; inset: 0; }`) silently keeps
  `bottom: 0` from that `inset` shorthand. Harmless on a plain block, but on
  a `display:flex; flex-wrap:wrap` container it gives the box a huge
  computed height (top-to-canvas-bottom), and `align-items: stretch`
  blows every wrapped child up to fill it — small label chips render as
  giant ovals with text pinned to one edge. Redeclare `bottom: auto` (or an
  explicit height) on any clip-derived element that wraps flex children.
- The same `inset:0` inheritance has a second, more common shape: a plain
  (non-flex) `.clip`-derived element that sets `top` and `left` but never an
  explicit `width` — a one-off label chip, a badge, a pill. `left` being set
  doesn't neutralize the inherited `right: 0` the way it does when `width`
  is *also* explicit (over-constraint only kicks in when both are given);
  with only `left` set, the box's width resolves by stretching from `left`
  to the container's right edge. On an element with a background this reads
  as a full-width slab with the text pinned to its top-left corner — easy to
  misdiagnose as a colour or font-size problem (that's genuinely what it
  looks like from outside the box) rather than the layout bug it is. Fix:
  `right: auto; width: max-content;` (or an explicit width) on any
  `.clip`-derived element carrying its own background that isn't meant to
  span the full canvas.
- Making a text container `display:flex` purely to vertically-center its
  content, when that content mixes raw text with a child element (an inline
  `<span>` accent, an icon). Flex splits mixed inline content into separate
  anonymous flex items at each element boundary and collapses the
  whitespace between them — "Root " + "=" + " Ginseng" runs together as
  "Root=Ginseng" with no space at all. Wrap the full content in one inner
  element first so the flex container has a single child and the mixed
  content keeps normal (non-flex) text flow inside it.
- Reusing one element across several `fromTo()` calls at different timeline
  positions (a repeating burst — ripples, ticks, a countdown ring) without
  registering its state at `t=0` as an actual timeline tween. The element's
  base CSS may say `opacity: 0`, but the render engine seeks this timeline
  directly to arbitrary times without necessarily passing through `t=0`
  first — the element can render at the first `fromTo`'s own "from" value
  (half-opaque, mid-scale) for the entire stretch *before* its first
  scheduled burst, not just during it. Caught via a paused-frame screenshot
  several seconds before a countdown ring's first scheduled appearance,
  visibly bleeding through. **A bare `gsap.set()` call outside the timeline
  does not fix this** — confirmed by testing it first and seeing the bleed
  persist unchanged in a re-render. It's not part of what the timeline
  itself evaluates on a seek, so it doesn't take precedence. The fix that
  actually worked: `tl.set(target, {...}, 0)` — inside the timeline, at
  position 0 — which registers the baseline as a real timeline tween in the
  same sequence GSAP evaluates on every seek. Any element hit by more than
  one `fromTo()` at different timeline positions needs this.
- Treating `tl.set(target, {...}, 0)` as the SOLE source of an element's initial
  state. Two sources in this codebase disagree about whether it holds: the
  multiple-`fromTo` entry above records that it is what survives a cold seek,
  while the engine's own lint (`gsap_timeline_set_initial_hide`) reports that
  *"a zero-duration set at 0 does not render while the playhead sits exactly at
  0, so frame 0 shows the un-hidden state"* and recommends `gsap.set()` outside
  the timeline, or CSS/markup. They were established against different engine
  versions and **neither has been adjudicated on a real render** — an attempt to
  do so found that every position-0 set in the test project was redundant with a
  CSS or markup default, so a silent no-op would have looked identical.

  **Correct practice makes the disagreement moot, which is better than picking a
  winner: let CSS or a markup attribute carry the initial state, and treat
  `tl.set(..., 0)` as a restatement of it, never the sole source.** That is safe
  under both claims — the CSS holds frame 0 either way — and it still fixes the
  original defect the `fromTo` entry was written for, since an element hit by
  several `fromTo`s gets a CSS baseline *plus* a restating `tl.set`. If a project
  ever does depend on the timeline form alone, confirm frame 0 by extraction
  rather than trusting either rule.
- Shipping a render with the debug overlay still toggled on.
- Using `loading="lazy"`, which the renderer will simply skip.
- Diagnosing a missing asset while the debug overlay is tinting every container.
- Translating a brief's explicit energy adjectives ("aggressive," "punchy")
  into a calm, low-cadence composition during a design-system pass, without
  checking the result against those adjectives.
- Opening on a logo, title card, or fade-from-black instead of the hook.
- A hook that poses its question at t=0 but doesn't pay it off until several
  seconds in, burning the whole shorts retention window on setup.
- A short with type parked under the engagement rail or the title strip — and
  a safe-area fix made in one scene that was never re-checked in the others.
- An end-screen scene with content where YouTube will draw its overlays, or a
  short with no engineered loop at its final frame.
- Treating the thumbnail as a screenshot grabbed at the last minute instead of
  a scored, composed deliverable — see *The thumbnail*.
- Copying a prior video's thumbnail grade/filter chain onto a new video with a
  different background palette, producing a muddy cast instead of a clean grade.
- An SFX clip that runs longer than its visual beat and drones into the next
  scene, caught only by listening past the cue.
- A storyboard/spec document whose timing table wasn't re-derived after a real
  timing change, so it stops being trustworthy as a reference.
- Shipping a project with a complete word-level transcript and no caption
  output built from it — the raw material existing is not the same as the
  deliverable existing.
- Two incompatible caption mechanisms coexisting across a channel's projects
  with no documented convention for which one is current.
- Mistaking a file named for what it contains (a `caption.txt` that is
  actually a video description) for the deliverable its name suggests.
- Reinventing a channel's palette, audio-mastering chain, or caption skin from
  scratch per video instead of pulling the channel's own established one — see
  *Consistency across a channel's videos*.
- Concluding a project has no shared catalog because `CLAUDE.md` doesn't name
  one, without checking for a conventional `catalog/`-style directory first —
  see *Catalog lifecycle*.
- Checking the catalog for reusable imagery but never for a reusable
  mechanism, which is exactly how the same component gets independently
  rebuilt across several videos without anyone noticing.
- Building a genuinely reusable component and never harvesting it back into
  the shared catalog — treating catalog contribution as optional cleanup
  instead of a required closing step, the same way a finished render with no
  captions isn't actually a finished project.
- Applying an external QC/bug report's literally-worded fix without first
  reproducing its finding against the actual render — a report's named
  symptom can be real while its diagnosis and proposed fix are wrong (see
  *Verification loop*'s own note on this).
- Trusting an external QC report's finding count instead of reproducing each
  one individually — a report can be right about magnitude on zero of its
  four findings and still be worth reading in full, because the fabricated
  ones and the real one require the same per-claim verification either way
  (see *Verification loop*'s note on fabricated findings, distinct from
  misdiagnosis).
- Calling a project "delivered" without a manifest of what shipped and
  where — a render, an `.srt`, and a thumbnail sitting in three different
  folders is not the same as the person who asked for them being able to
  find them (see *The delivery manifest*).
- An internal record/citation ID rendered on screen instead of a
  human-readable citation — a raw catalog key means nothing to a viewer and
  belongs in the description, not the frame.
- Every beat using the identical fade-and-rise entrance regardless of
  content — see *Posture*'s note on this file's own canonical example.
- A diagram carrying more than three important labels, or explaining more
  than one mechanism per beat — unreadable at phone scale before it's even
  a content problem.
- A caption repeating a decorative label's exact phrase in the same beat
  with no change in meaning — the same words read twice instead of one new
  piece of information.
- A static plate left with zero applied motion for its full on-screen
  duration — the same defect class as a frozen scene, just on an image
  instead of a whole frame.
- A generic subscribe/like card as the closing beat instead of one
  specific, lesson-tied action.
- A short running past 50s with no storyboard reason recorded — almost
  always VO-driven timing left unchecked, not a deliberate call.
- Safe-area padding computed against the pre-transform box instead of the
  scene's own final rendered position — every scene consumes `--safe-*`
  correctly and the render still ships ink past the line, because a Ken
  Burns `transform: scale()` (or an entrance transform's own transient) sits
  between the padded box and the canvas and the padding math never accounted
  for it. See *9:16-native composition*'s safe-areas bullet for the fix.
- A hand-tuned `+Npx` safe-area allowance sized against whatever the token
  happened to be at measurement time, instead of derived from the scene's
  own scale/origin — it silently goes wrong the moment the token or the
  scene's zoom changes later, with nothing to flag it (confirmed: a
  correction to `--safe-bottom` left two scenes' own allowances undershooting
  the new line by 5-10px, computed correctly against a boundary that no
  longer applied).
- A QC report whose named symptom is real but whose prescribed fix is off by
  an order of magnitude from the measured overshoot, or whose top-severity
  finding doesn't reproduce at all — applying either literally would have
  moved a compliant element out of compliance (see *Verification loop*'s
  note on this same failure shape, and reproduce every finding against
  actual pixels before building a fix plan from a report's wording).
- Trying to fix a rendered-pixel safe-area overshoot by adding margin instead
  of fixing what actually pushed the content past the line — an entrance
  transform's transient overshoot needs the transform removed (or bounded),
  not a bigger padding number that only shifts where the same bug resurfaces
  next time a scene's resting position happens to sit close to the line.
- Cleaning up a citation pill's *format* (converting an internal ID to
  `Journal · Year`) and treating that as having handled the video's clinical
  language, when the check that actually matters is whether the *claim
  sentence itself* — not its footnote — requires the viewer to already know
  clinical or regulatory vocabulary to act on it correctly. The two are
  independent: a pill can be perfectly formatted next to a headline the
  target audience can't parse.
- Copying a project's static-hold checker script into a new project without
  re-deriving its `CAPTION_BAND_EXCLUDE`/crop constants against that new
  project's own `index.html` — a comment in the file documenting a past
  instance of this exact mistake does not stop it recurring one project
  later; confirmed happening twice in the same file's own lineage (see
  *Verification loop*'s static-hold section).
- Trusting a whole-frame static-hold check's "clean" result as proof a
  scene's own hero element is alive, when a different, legitimate element
  elsewhere in the same frame is what kept the diff moving — the hero region
  can be genuinely empty (not merely static) for the whole window and never
  register. Needs a region-aware check, not a frame-wide one.
- Diagnosing "the final beats drag" as the ENTRANCE stagger being too slow
  and widening it, when the actual measured gap is a scene's own EXIT-to-
  next-beat handoff — the entrance can already be tighter than the report's
  own suggestion. Reproduce the specific dead window against the render
  before picking which half of the scene to retime.
- Adding a Ken Burns cadence-floor zoom to every scene a QC round touches,
  without checking whether that specific scene's own file already documents
  a reason to have none — a scene built as a loop's byte-identical shell to
  its own opening scene can have "no zoom, on either end" as the deliberate
  mechanism keeping the loop seam matched, not an oversight to fix.
- Trusting an external QC report's "completely silent" claim (or any binary
  presence/absence claim about audio) without running the one-line
  `ffmpeg astats`/`ebur128` check first — this is the cheapest disproof
  available in this entire skill and is worth reaching for before any
  frame-by-frame pixel work, not after.
- Running a QC gate calibrated for one canvas against a render in another and
  reading its silent zero-findings as a pass — confirmed to fail open on the
  bottom zone (an empty numpy slice) while simultaneously measuring the wrong
  region on the right. The script's own docstring naming the assumption does
  not prevent it; only an assert that refuses to run does.
- Editing a generated composition with a find-and-replace that is not asserted.
  A no-match `str.replace` silently does nothing, so a CSS change can appear to
  land while the generated file keeps the old rule — and the next render looks
  like a layout mystery rather than an edit that never happened. Confirmed:
  a card-conversion edit no-oped because an earlier edit had already changed the
  matched text, the flood stayed at 0.67% of frame instead of 8%, and it cost a
  full render cycle. Assert every match, and verify against the GENERATED file,
  not the generator.
- Sizing a beat by how different the colours look rather than by luma delta ×
  frame area — a hue-only change (celadon → coral, 27 luma) is invisible to a
  frame-difference check that a much duller-looking change to near-black (149
  luma) clears easily.
- Writing copy as a bare text node inside a container with an animated
  background. A `.wash ~ *`-style rule lifts sibling ELEMENTS above the
  background; a text node has nothing to apply it to, so the card renders
  blank — and an engine layout auditor that walks text elements will not see it,
  because the text never became one. **One instance survived in the very
  project that documented this failure mode** —
  `videos/ectoin-survival-molecule/compositions/frames/28-remember.html:167`,
  the payoff line, overpainted at 1.72:1, with the file's own comment block
  predicting it and the delivery doc recording it as fixed. The two checks that
  catch it: a source grep for a text node immediately after a `.wash` div, and
  a look for the `.wash:only-child` outline in an extracted frame. **A comment
  predicting a bug is not a check for it.**
- Printing "clean" or "passed" as a checker's summary when only some failure
  modes were tested — the sentence is where a documented coverage gap ships as a
  false all-clear. Scope the line to what actually ran and name what did not.
- Keeping a checker's controls in a session scratch directory instead of a
  runnable script beside the tool. A control that cannot be re-run after the
  next threshold change is not a control.
- Converting a scene start time to a frame index with `int()` instead of
  `ceil()`, so any window whose start is off the sampling grid opens one frame
  early on the previous scene's content — manufacturing a "content then empty"
  finding at most hard cuts. Measured at 76 % of scene starts in one repo.
- A scene-parsing regex that assumes authored attribute order, so a project
  writing the same attributes in a different sequence silently yields zero
  scenes and degrades a per-scene check into a whole-render one.
- Carrying 9:16 layout instincts into a 16:9 frame — "fill the safe column" and
  "structure scenes as rows, not columns" are corrections for the *vertical*
  failure mode, and applying them to a wide canvas produces the landscape
  failure mode instead: a full-width band of text with no depth behind it.
- Re-deriving or scaling the type scale for a 16:9 flip. Both canvases share a
  1080px short edge, so the scale transfers unchanged; scaling by 0.5625 pushes
  body copy under the floor and scaling by 1.78 inflates a headline off the
  frame. Layout gets an explicit variant; type does not.
- Leaving the element that fills the safe box unclipped, so an entrance
  transform's transient (or a decorative `scale:1.0x`) renders inside a reserved
  zone even though every `--safe-*` token is consumed correctly. `.stage > * {
  overflow: hidden; }` makes it structurally impossible; a bigger margin does not.
- Reserving the end-screen zone across the whole video instead of on the final
  scene, wasting the right third of every frame — the Shorts rails bind every
  frame, the end-screen zone binds only the last 5–20 s.
- Assuming `render --resolution` can change aspect ratio. It is a supersampler:
  it requires the aspect to already match and the scale to be an integer
  multiple, and a mismatched `--width`/`--height` renders at the authored size
  rather than erroring.
- Treating a catalog spike that exports `window.renderFrame` plus a bespoke
  global as a drop-in sub-composition. The engine drives
  `window.__timelines[<id>]`; a spike built for a review harness needs real
  adaptation, not a CSS flip.
- Nesting `data-composition-src` two levels deep (root → chapter → frame).
  Confirmed by isolated test to silently break a scene's inner layout, pushing
  content off-canvas — invisible in the rendered MP4, not a lint finding. Stay
  one level: root → frame.
- Running `check` at its 9-sample default on a multi-minute piece — on a 300 s
  render that is one sample every 33 s, which is effectively no coverage while
  reporting a clean pass.
- Building a new region-aware or content-detection scanner and trusting its
  own first clean/dirty result without re-verifying that result against
  actual extracted frames — a heuristic image-analysis script is exactly as
  capable of a false positive (a textured plate reading as "content," a
  weaker second content state reading as "still empty" against a baseline
  calibrated to an earlier, stronger state in the same cell) as an external
  QC report is, and earns the same "verify by pixels" discipline turned back
  on itself, including immediately after fixing the defect it was built to
  catch.
- Animating `width` on an `overflow: hidden` box that clips a RASTER — the
  engine's default `drawElement` capture path can silently render that region
  as frozen while the DOM reports correct geometry and `check` passes clean.
  Text or a solid fill in the same clip is pixel-identical and fine; the
  raster is the trigger, and a small one is not proof of safety (846×300
  passed where 840×900 failed). See *Verification loop*.
- Treating the engine's `drawElement self-verify passed` line as proof the
  render is clean. It samples ~4 instants across the whole render against a
  fixed 32 dB threshold, so it is weakest exactly where this defect lives — an
  animation ramping in from nothing. Measured: it armed, sampled INSIDE the
  broken scene, and passed at 40.4 dB because the wipe was 2.8% open at that
  instant. The video shipped broken with a clean log.
- Assuming `check-static-hold.py`'s region-aware mode already covers a frozen
  panel. It detects a cell going content-then-EMPTY; a panel that stays full
  of content while frozen never makes that transition, and whole-frame mode is
  masked by any other element still animating. Confirmed missed in both modes
  on a render known to be broken — this is a fourth failure mode, not a
  variant of the three above it.
- Flagging a deliberately static plate as a dead region. Raw byte-identity
  cannot tell a held product shot from a broken one; scope the scan to
  elements that clip a raster AND carry an authored tween in that scene's
  window, or the check cries wolf on calm design.
