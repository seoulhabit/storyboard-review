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
3. **Validation mode.** When asked to verify a layout or draft a skeleton, ship
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

This is the craft half of research integrity: presentation, not whether the
underlying claim is true. Whether a claim is defensible — a real source
exists, the cited population/product-type/route actually matches, injected
clinical treatments are distinguished from topical cosmetics — is
domain-truth work, and as the note above says, no project skill in this repo
currently holds it. Don't let that missing home become an excuse to skip the
presentation half this section does own.

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
    // The root timeline's own job is scene handoff — see "Cuts vs crossfades."
    // It does NOT drive content inside a scene; each sub-composition owns that.
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    // Prefer a hard cut (no tween) between same-family scenes; only tween
    // opacity across a boundary that stays on the same background colour.
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
2. Every crossfade/cut pairing on the root timeline that references those times.
3. Every SFX clip's `data-start` in scenes after the change point.
4. The BGM's loop/slot length and its `data-fx-carve` timing if it's phrase-synced.
5. The root `data-duration` and its anchor tween.
6. The project's own storyboard/spec document (STORYBOARD.md or equivalent) —
   re-derive its timing table from the actual `index.html`, don't hand-edit
   estimates. A drifted storyboard stops being useful as a spec the moment one
   real timing changes and the doc isn't re-synced.
7. Any in-scene motion beat hand-timed against a *specific VO word's*
   timestamp — a chip that appears on "because," a stagger that lands on a
   clause. A new take's word timings rarely fall at the same offsets as the
   old ones, even when the scene's own start/duration don't change (a
   re-recorded final line changes nothing upstream but still desyncs every
   beat inside that one scene). Re-derive each beat's trigger time from the
   new transcript; don't assume the old relative offsets still land on the
   same words.

Treat a mid-build script edit as "this touches N files," not "this touches one
line," and budget for it.

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
   record.
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
   before any markup exists. See the layout section.
7. **Composition skeleton.** Scenes and timing wired with the engine's real
   timing attributes. Get the structure seeking correctly before any styling.
8. **Layout check with the debug overlay on.** Verify bounding boxes and safe
   areas, then turn it off.
9. **Motion pass.** Add easing, stagger, and camera. One idea at a time. Budget
   beats across the *whole* scene, not just its opening two seconds — a scene
   that lands three beats immediately and then holds for the rest of its
   narration duration fails the cadence target just as hard as a scene with no
   beats at all. See *Cadence* below.
10. **Lint and preview.** Use the project's real preview/check tooling (e.g.
    `npx hyperframes preview --background`, `npm run check`) and scrub by
    dragging the seek position, not by playing — dragging is what exposes
    non-seekable animation.
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
4. **Does the motion explain something** — a relationship, a
   transformation, a comparison, a cause — rather than decorate? See
   *Posture*'s "motion that means something."
5. **Is there a real photographic, tactile, or product-specific visual
   early in the video**, rather than a fully illustrated/typographic open
   by default? See the tactile-anchor rule in *Asset protocol* above.
6. **Are palette, type, captions, and any channel mark consistent** with
   the rest of the channel? See *Consistency across a channel's videos*.
7. **Are safe-area tokens actually consumed by every scene**, not declared
   in one file and hardcoded elsewhere? Measured gap on this channel: only
   6 of 24 shipped projects reference `--safe-*` tokens at all. See
   *9:16-native composition* below.
8. **Does a real sidecar caption file exist** — not a same-named but
   unrelated file (see *The captions*' naming note below) — alongside the
   burned-in track? Measured gap: only 4 of 24 shipped projects ship one.
9. **Are all on-screen citations real and human-readable, with no internal
   IDs?** See *What must never reach a rendered frame* above.
10. **Are there no placeholders, unfinished text, or debug-overlay
    artifacts in frame?** Same section as above.
11. **Is the closing beat one specific, lesson-tied action**, not a
    generic subscribe card? See *The hook* below and production-loop
    step 2.
12. **Does the video still make sense with the sound off?**

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

**Transition midpoint check.** Extract a frame at the exact midpoint of every
scene-to-scene transition, not just before and after it. A crossfade between
two different background colours produces a genuinely muddy, near-blank frame
at 50% — invisible if you only ever look at settled frames. See *Cuts vs
crossfades* below for when a crossfade is and isn't safe.

Also always check: frame zero (must be composed, not mid-fade — see mandatory
rule 4), and, for a short, that the last frame hands back toward the first if
a loop was promised (see *The hook* below).

**Phone-scale legibility check.** Downscale an extracted frame to roughly 25%
size — the same "phone-viewing-simulation habit" *The thumbnail* section
already invokes for judging grid-size legibility. That habit is what
pre-render gate item 2 above actually runs: any headline, caption, label, or
citation that stops being legible at that scale is a reject, not a style
note. See *9:16-native composition* below for the type floors and *Asset
protocol* above for the diagram label budget — the thresholds it's checking
against.

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

## Cuts vs crossfades

Hard cuts on a timing grid are the default and outperform transitions on
retention — this is a real, not merely aesthetic, preference. A crossfade is
only safe **between two scenes that share the same background/ground colour**;
crossfading between a light and a dark scene produces a washed, near-blank
midpoint frame (the transition-midpoint failure above) because both layers sit
at ~50% opacity over an unrelated canvas colour at once. If a project's design
alternates background colour scene-to-scene for contrast (a legitimate
technique), that same alternation makes crossfades structurally unsafe for
every boundary that changes ground — use a hard cut there, and reserve any
softness (a very short, ≤150-200ms same-ground fade) for boundaries that don't
change background.

## YouTube delivery

The platform layer. Everything here shapes the beat sheet, so it is read
*before* beats are written, not at publish time. Platform numbers drift —
treat limits and safe-area percentages as current-as-written and verify
anything load-bearing before a real publish.

### Formats

| | Long-form | Short |
|---|---|---|
| Canvas | 1920×1080 (16:9) | 1080×1920 (9:16) |
| Length | any | ≤ 3:00 (limit raised Oct 2024) |
| State-change cadence | every 8–12 s | every 1.5–3 s, **for the entire scene** |
| End screens / cards | yes | no — one related-video link |
| Chapters | yes | no |

The cadence target is not "at least one beat somewhere in the scene" — a scene
that is 15s long with narration needs roughly 5-10 authored state changes
spread across its full duration, not 2-3 clustered at the start. See
*Verification loop*'s static-hold check for how this actually gets caught.

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
  unnoticed. Approximate reserved zones (verify against a current device):
  - **Right edge ~15%** — like/dislike/comment/share rail.
  - **Bottom ~20%** — title, channel, audio attribution.
  - **Top ~10%** — search and camera icons.

  The center-left column is the only zone guaranteed clear. Debug-overlay the
  zones (see *Layout validation* above) rather than eyeballing pixel math per
  scene — and re-check every scene after any late change to a block's height
  or `justify-content`, since a spacing fix in one scene silently regressing a
  *different* scene's safe-area compliance is the single most common way
  a violation ships (fixed elsewhere, never re-verified where it originated).

### The hook

Retention is decided in the first ~2 s of a short and ~8 s of long-form.
Structural consequences:

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
  frame wastes this for free.
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
  in a project should use.
- **Cuts over transitions.** Hard cuts on a timing grid outperform crossfades in
  retention and are far cheaper to render — see *Cuts vs crossfades* for exactly
  when a crossfade is still safe.
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
  otherwise-narrated piece, not the assumed baseline for the format.

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
  extracted at the exact midpoint.
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
