# HyperFrames engine — the shipped contract

Every line in this file is a transcription of the pinned CLI's **own shipped
docs**, with the file that says it named beside it. Nothing here is recalled.
If a pattern is not in the pinned version's shipped docs, it is not in this
skill.

**Where the docs are.** The CLI ships them inside its own package:

```
node_modules/hyperframes/dist/docs/{data-attributes,gsap,compositions,rendering,troubleshooting,examples}.md
node_modules/hyperframes/dist/skills/hyperframes/**
node_modules/hyperframes/dist/skills/hyperframes-cli/**
node_modules/hyperframes/dist/templates/blank/index.html
node_modules/hyperframes/dist/templates/_shared/AGENTS.md
```

Projects here run the CLI through `npx --yes hyperframes@<pin>`, so the package
lands in the npx cache rather than a project `node_modules/`. Either way, read
the copy for **the pin the project's own `package.json` scripts name**, not
`@latest`. `npx hyperframes docs <topic>` prints the same `dist/docs` pages in
the terminal with no network.

**Pin.** This repo has no root `package.json`; the pin lives per video project
in its `scripts` (`npx --yes hyperframes@0.8.22 check`). Pins in use: 0.8.17,
0.8.19, 0.8.20, 0.8.22. `dist/skills/` and `dist/templates/` are **byte-identical
across all four** (verified by `diff -rq`), so the contract below holds for
every project in the repo. Re-run that diff when a new pin appears; do not
assume it.

---

## 1. Composition structure

```html
<div id="root"
     data-composition-id="main"
     data-start="0"
     data-duration="9.000"
     data-width="1080"
     data-height="1920">
```

- `data-composition-id` — required, unique per composition. *(docs/compositions.md §Structure; docs/data-attributes.md §Composition)*
- `data-width` / `data-height` — composition pixel size. *(docs/data-attributes.md §Composition)*
- `data-start` / `data-duration` — seconds. *(docs/data-attributes.md §Timing)*

The shipped blank template carries all five on `#root`. *(templates/blank/index.html)*

## 2. Timed elements

```html
<div class="scene clip" id="scene-s01" data-composition-id="s01"
     data-composition-src="compositions/frames/01-s01.html"
     data-start="0.000" data-duration="3.000" data-track-index="0"></div>
```

- `class="clip"` on every timed element. The runtime keys visibility off
  `data-start`, **not** the class, but the shared `.clip` rule is what gives a
  scene its full-frame box and `lint` warns without it.
  *(docs/data-attributes.md §Element Visibility; templates/_shared/AGENTS.md rule 2)*
- `data-track-index` is **a Studio timeline lane, display only**. The render
  never reads it. It does not control paint order — use CSS `z-index` — and it
  does not prevent overlap. Optional. *(docs/data-attributes.md L9)*
- Sub-compositions mount through `data-composition-src` with a **project-relative**
  path. *(docs/compositions.md §Nested Compositions; templates/_shared/AGENTS.md rule 5)*
- Give every timeline-visible element a stable `id`, or `lint` raises
  `studio_missing_editable_id`. *(observed from `check`; the fix line it prints)*

## 3. The time model — paused GSAP timelines on `window.__timelines`

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });
  tl.to("#title", { opacity: 1, duration: 0.5 }, 0);
  window.__timelines["main"] = tl;
</script>
```

*(docs/gsap.md §Setup; templates/blank/index.html; templates/_shared/AGENTS.md rule 3)*

Rules, verbatim from `docs/gsap.md §Key Rules`:

- Always create timelines with `{ paused: true }`.
- Register timelines on `window.__timelines` with the composition ID as key.
- Position parameter (3rd arg) sets absolute time: `tl.to(el, vars, 1.5)`.
- Supported methods: `set`, `to`, `from`, `fromTo`.
- Supported properties: `opacity, x, y, scale, scaleX, scaleY, rotation, width,
  height, visibility`.

One registered timeline per composition — root and each sub-composition. The
root timeline's only job is scene handoff; a sub-composition owns its own beats.
Keep an anchor tween last so `tl.duration()` equals the declared duration:

```js
tl.to({}, { duration: 9.000 }, 0);   // anchor — always last, always at 0
```

There is **no `seek(t)` entry point.** A hand-written `window.seek` is never
called by this engine; a composition built on one renders as a single flat
colour for its whole duration. That failure is what the 2026-09-01 audit
measured (mean |Δ| = 0.00 across five extracted frames) and it is why this file
exists.

**Determinism.** No `Date.now()`, no `Math.random()`, no network fetches inside
a composition. *(templates/_shared/AGENTS.md rule 6)* Nothing plays: the
renderer seeks. An out-of-order seek to the same position must be
pixel-identical to a cold seek there.

## 4. Initial state — the two-sided trap

Both halves are confirmed by the engine's own lint and by extracted frames:

| Pattern | What actually renders |
|---|---|
| `fromTo(..., {immediateRender:false})` | Element sits at its CSS resting state until the tween **starts**, then snaps to the `from` value — visible at frame zero, blanks mid-scene, fades back in. |
| `tl.set(el, {opacity:0}, 0)` | A zero-duration set at position 0 **does not render while the playhead sits exactly at 0**, so frame zero shows the *un-hidden* state. Lint code: `gsap_timeline_set_initial_hide`. |

The state that survives a cold seek to 0 is authored **outside the timeline** —
in CSS, restated with `gsap.set()` so GSAP's transform cache agrees — with the
timeline only ever tweening toward the visible state:

```css
.beat.is-entering { opacity: 0; }
```
```js
gsap.set('#s01-b1', { opacity: 0, y: 20 });          // immediate, outside tl
var tl = gsap.timeline({ paused: true });
tl.to('#s01-b1', { opacity: 1, y: 0, duration: 0.4 }, 1.0);
```

`scripts/beats_to_composition.py` emits exactly this shape. Verified in pixels:
frame at 0.2 s shows the hook line alone; the second beat is absent until 1.0 s.

## 5. The beat sheet generates the timeline

`03-beat-sheet.json` is the single source of timing. `scripts/beats_to_composition.py`
turns it into `index.html`, `compositions/frames/NN-<id>.html`, and
`index.motion.json`. Timing is never hand-typed into the HTML; edit the beat
sheet and re-run.

The CLI's own `hyperframes beats` is **not** this. It is a Studio utility that
analyses a local music `<audio>` source in headless Chrome and writes a
beat-grid at `beats/<audio-relative-path>.json`. It needs a music track, it
fails and writes nothing when no beats are detected, and it has nothing to do
with a story beat sheet. *(skills/hyperframes-cli/references/beats.md)*

The generator also enforces `[S5/C-2]` cadence at generation time: a scene whose
beats leave a still window longer than the format's cap is an error before a
render is ever attempted.

## 6. Paths

Project-relative, everywhere:

```html
<div data-composition-src="compositions/frames/01-hook.html"></div>
<img src="assets/plates/03-flaking-skin.png" ...>
<audio src="assets/bgm/track-soft.mp3" ...>
```

`hyperframes.json` declares where those roots are:

```json
{ "paths": { "blocks": "compositions", "components": "compositions/components", "assets": "assets" } }
```

No `file:///ABS/PATH`, no `/mnt/...`. The bundler resolves relative paths; the
2026-09-01 audit confirmed a relative plate path loading correctly in a render
that v2's own lint had failed for being relative.

## 7. Fonts

A named Google Fonts stylesheet link is the **supported** path. The compiler
fetches the faces, caches them, and injects deterministic `@font-face` rules at
render time — observed on every run in this repo:

```
[Compiler] Fetched 11 font face(s) for "Inter" from Google Fonts (cached to ~/.cache/hyperframes/fonts/inter)
[Compiler] Injected deterministic @font-face rules for 2 requested font families
```

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@600;700;800&display=swap" rel="stylesheet">
```

For byte-identical output across hosts use `render --docker`, which pins the
Chrome version and the fonts. *(docs/rendering.md §Docker Mode;
docs/troubleshooting.md L29)* Unicode outside Latin (Korean, CJK) still needs a
family that covers it — frame extraction is the check.

## 8. `box-sizing: border-box` — first rule, every composition

`*, *::before, *::after { box-sizing: border-box; }`. The shipped blank template
carries this reset. *(templates/blank/index.html L8-12)* Restored here as a
mandatory rule because its absence caused a confirmed, hard-to-diagnose defect —
see `decision-policy.md [S6/A-5]`.

## 9. Media

- `data-media-start` — playback offset / trim point in seconds.
- `data-volume` — `1` is 0 dB, `0` silence, up to `3.98` (+12 dB).
- `data-has-audio="true"` — the video carries an audio track.
- Videos use `muted` with a separate `<audio>` element for the audio.
*(docs/data-attributes.md §Media; templates/_shared/AGENTS.md rule 4)*

`<video>`/`<audio>` work at any nesting depth — the runtime discovers media with
a flat DOM query. *(skills/hyperframes-cli/references/lint-validate-inspect.md)*

On this engine a `data-automation` volume lane **replaces** `data-volume` rather
than scaling it, which is how a bed ships ~10 dB hot. Use plain `data-volume`
and handle the tail in the post-render master.

## 10. Images

- `loading="eager"` + `decoding="sync"`, always. Never `loading="lazy"` — a
  headless renderer skips unpainted images.
- Explicit `width`/`height` attributes: reserve the box before decode.
- Explicit `object-fit` (`cover` for backgrounds, `contain` for products,
  diagrams, logos).
- A fallback background colour on the wrapper.

## 11. Layout

Structural relationships inside a clip are Grid or Flex. `position: absolute` is
the sanctioned mechanism for **clip/scene stacking** — HyperFrames' own idiom is
`.clip { position: absolute; inset: 0; }`. What must not be absolute is the
*internal* structure of a clip: its columns, rows and card layout. Two elements
whose relative position is expressed as two independent `top`/`left` values is
the bug this rule prevents; it does not survive a string-length change or an
aspect-ratio flip.

Debug overlay goes on **`#root`**, never on `<body>`: a sub-composition's own
renderable surface *is* `#root`, so a debug class on `<body>` is invisible to
any check that only inspects the body tag. Confirm it is off by looking at
frame zero.

## 12. Media treatments and seek-safe motion

Do not improvise equivalent CSS/SVG filters, grades, or reveal effects. Load
`/media-use` and read its `references/media-treatments.md` before changing how
footage or images look or reveal — including when the ask only says "dark",
"flat", "boring", "retro", or "make the reveal cooler". *(templates/_shared/AGENTS.md)*

For motion vocabulary — atomic rules, scene blueprints, the 24 named
text-animation effects, and the runtime adapters — use `/hyperframes-animation`.
For punch-ins, camera moves, Ken Burns and match cuts, `/hyperframes-keyframes`.
This file does not restate them.

**Scene-to-scene transitions are a root-timeline mechanism, and the machine
source of truth is `skills/hyperframes-animation/transitions/TRANSITION-REGISTRY.md`**
— read it rather than deriving the GSAP by hand. Its five Tier-B entries
(`crossfade`, `blur-crossfade`, `push-slide` with a LEFT/RIGHT/UP/DOWN
direction, `zoom-through`, `squeeze`) act purely on the two scene **clip
wrappers**, so no per-scene cooperation and no injected overlay DOM is needed.
The shape, which `scripts/beats_to_composition.py` emits from a scene's
`transition` field `[S6/A-8]`: extend the outgoing wrapper's `data-duration` by
the transition duration so it holds its final frame; pull the incoming
wrapper's `data-start` earlier by the same amount to create the overlap; keep
`data-track-index` ping-ponging 0/1 so the two overlapping wrappers never share
a track; and stamp the registry's `gsap_template` on
`window.__timelines["main"]` at the overlap start. The sub-compositions' own
paused timelines are still driven independently by the runtime — this is not a
nested timeline and does not double-seek. Cap 2.0s. Exit animations are never
authored: the transition *is* the exit.

## 13. The `faceless-explainer` route

v2.1 runs through the shipped `/faceless-explainer` route. Its interview asks
for **angle**, **length**, **destination**, and conditionally **`VO_MODE`**.
Those four are pre-answered from the brief and the baseline by
`decision-policy.md [S1/S-7]` and `[S1/S-8]`, so the route runs without putting
a question to the operator. *(skills/hyperframes/references/routes/faceless-explainer.md)*

## 14. Commands

```bash
npx hyperframes check --json --snapshots    # the gate; see decision-policy [S7/R-1]
npx hyperframes render --quality high --workers 1 -o renders/<slug>.mp4
npx hyperframes preview --background        # Studio handoff; --stop when done
npx hyperframes docs <topic>                # local docs, no network
```

`check` runs the linter first and skips the browser entirely when lint reports
errors. Full flag set and finding semantics:
`skills/hyperframes-cli/references/lint-validate-inspect.md`.
