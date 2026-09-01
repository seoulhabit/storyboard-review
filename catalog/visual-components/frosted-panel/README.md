# FrostedPanel

A translucent, backdrop-blurred glass card — plus an optional peeling-film
overlay — built entirely from CSS/SVG. Harvested because this project
(`videos/peeling-question-open/compositions/frames/01-question.html`) would
otherwise have been the **second independent implementation** of the frosted
panel itself, and the catalog exists specifically to stop that pattern before
it repeats a third time (`TermDefinition`'s own story: five independent
rebuilds before anyone cataloged it).

- **`frostedpanel-spike.html`** — the component (`.glass-panel` +
  `.panel-texture`), the optional peeling-film overlay
  (`.film-clip`/`.film-sheet`/`.curl`), a live demo, and a GSAP-driven
  `t`-scrubber matching the render-gate contract. Start here.

## Why this one, and why now

`videos/centella-tiger-grass/compositions/frames/02-identity.html` is the
**only** other place in this repo using `backdrop-filter`, and it does so
without ever being cataloged — seven shipped renders proved it survives the
headless renderer, but nothing recorded that proof anywhere a second project
could find it. `peeling-question-open` needed the exact same primitive
(confirmed live on this project's own render, not assumed from
`centella-tiger-grass`'s success alone — see *Verification* below) and would
have re-derived it from scratch had this not been checked for first.

## The component

```css
.glass-panel {
  background: rgba(251,249,245,0.16);
  backdrop-filter: blur(25px) saturate(1.15);
  -webkit-backdrop-filter: blur(25px) saturate(1.15);
  border: 1px solid rgba(255,255,255,0.30);
  border-radius: 32px;
  overflow: hidden;
}
```

Sits on a mid-value ground (tested on `--moss #4F6B52`; `centella-tiger-grass`
uses it over a lighter paper-adjacent tone). Text placed *inside* the panel
should stay ink-toned for contrast against the lightened, blurred backdrop;
text placed *outside/below* it (on the raw ground colour) needs its own
contrast check against that ground directly — the panel's translucency does
not extend outward.

**Render-safety note.** `backdrop-filter` is GPU-dependent and this skill's
own determinism guarantee is environment-scoped (see
`faceless-video-craft/SKILL.md`'s "Determinism is environment-scoped"). It is
proven on macOS across two independent projects now (7 `centella-tiger-grass`
renders + this project's own render, both `screenshot`-capture-mode). It has
**not** been verified on a Linux/cloud render target — re-baseline before
trusting it there, per the skill's own guidance on capture-mode drift.

## The optional peeling-film overlay

A translucent sheet that appears to detach from the panel, revealing the
panel's own texture beneath — built from three elements sharing one timeline
position, no `clip-path` string-tweening trick required:

```css
.film-clip  { position:absolute; inset:0; overflow:hidden; }   /* the clipping boundary */
.film-sheet { position:absolute; inset:0; }                     /* the sheet artwork */
.curl       { position:absolute; left:0; right:0; }             /* rides the peel line */
```

```js
// #film-clip translates DOWN by d; #film-sheet translates UP by d, same
// duration/ease -- the two cancel exactly, so the sheet artwork appears
// stationary while the clipping boundary (film-clip's own top edge) descends,
// "eating away" the sheet from the top down. #curl shares the same d/ease and
// sits above both in z-index, so it always rides exactly on the peel line.
tl.to('#film-clip',  { y: d, duration, ease }, t);
tl.to('#film-sheet', { y: -d, duration, ease }, t);
tl.to('#curl',       { y: d, duration, ease }, t);
```

A static (never tweened) `mask-image` gradient on `.film-sheet` fades its
trailing edge to translucent, so the curl reads as thin film rather than an
opaque flap — the same technique
`centella-cica-vs-snail-mucin/04-twist.html` uses for a swipe-fade edge.

`peeling-question-open`'s actual scene additionally tweens `rotationX` on
`.curl` for a 3D lift and a `filter: drop-shadow(...)` for contact shadow —
both proven GSAP-tweened properties in this repo's own shipped renders
(`madecassoside-clinical-cut`, `mugwort-healing-herb`,
`snail-mucin-medical-secret`), included here for completeness but not load-
bearing to the core mechanism.

## Field contract

Not a data-driven component in the `TermDefinition`/`GradedScale` sense —
there's no props array. The real per-use decisions:

```js
{
  panelBg: "rgba(251,249,245,0.16)",   // panel fill over the chosen ground
  peelEnabled: true,                    // false = a static frosted card, no film
  peelDuration: 1.45,                   // seconds, film-clip/sheet/curl travel
  peelEase: "power1.in"                 // adhesion-releases-then-accelerates
}
```

## Verification

Confirmed on the actual render, not assumed from `centella-tiger-grass`'s own
history: `check-safe-area.py`, `check-static-hold.py`, and
`check-blank-frames.py` all pass clean on `peeling-question-open`'s
`01-question` scene, and the peel's `clip-path`/`rotationX` sweep was
confirmed via a 3-frame extraction (t=0, mid, end) to show real, correctly-
progressing pixel motion — not a static frame with a moving label.

## Status

**SPIKE — not wired to a build pipeline.** Deterministic `t`-driven clock via
a paused GSAP timeline, seek-safe (matches this catalog's convention for
anything with a time axis). Transcribed from
`peeling-question-open/compositions/frames/01-question.html`'s shipped,
rendered scene — the panel shell also matches
`centella-tiger-grass/compositions/frames/02-identity.html`'s independently-
arrived-at version closely enough that either project can be treated as
having proven this primitive.
