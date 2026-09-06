# MOTION.md — sh-timeline.js retirement record and compile-time IR

## Provenance

`templates/_shared/sh-timeline.orig.js` is the SeoulHabit design system's own
runtime, byte-for-byte as extracted from Claude Design project
`a7945a95-da21-4823-8b16-57c6ffa11558` on 2026-09-06 (see `MANIFEST.json` for
its sha256). It builds one paused GSAP timeline on `window.__timelines["main"]`
by reading `[data-scene]` elements and their `data-start`/`data-dur`/
`data-anchor` attributes, applying `autoAlpha` to non-anchors and plain
`opacity` to anchors, and animating five element-level markers:
`data-enter`, `data-float`, `data-sweep`, `data-sh-count`, `data-sh-strike`.

## Why it is not shipped as a render-time runtime

Two engine facts rule it out for this compiler, and one architectural
decision (D5, this WO) rules out its natural home:

1. **`data-dur` is not the HyperFrames engine's attribute.** The contract
   (`hyperframes docs data-attributes`) is `data-start` + `data-duration`.
   A scene using `data-dur` gets one lifetime from `sh-timeline` and a
   different one (or none) from the runtime's own visibility toggling —
   two clocks disagreeing about when a scene is on screen.
2. **It registers on `DOMContentLoaded`, not synchronously.** The runtime's
   readiness gate probes `window.__timelines` and expects it populated
   before the document finishes parsing. Deferred registration risks the
   exact failure other projects in this repo have recorded: the gate reads
   "key present" as "ready" when the timeline is still empty.
3. **This WO's D5 ruling splits any scene over the duration ceiling into a
   deterministic sub-scene sequence**, which turns one design-system scene
   into several. A single-document runtime driving all scenes as siblings
   (which is what `sh-timeline.js` assumes) does not scale past roughly a
   dozen scenes before `hyperframes lint`'s `composition_file_too_large`
   warning becomes permanent — and a beat sheet like `kbeauty-label-trap`'s
   (257s at a 5s cap) compiles to roughly 50 scenes. The compiler instead
   emits one `<template>` sub-composition per scene (see `COMPILER.md`),
   each with its own inline, synchronous, per-scene timeline — the shape
   `beats_to_composition.py` already uses and three shipped projects in
   this repo already pass `check` against.

So `sh-timeline.js` is retired **as a runtime**. It is not deleted — it
survives verbatim at `sh-timeline.orig.js` as the design system's own
authoring aid (it still animates a `.dc.html` artboard inside Claude
Design, where there is no HyperFrames engine and none of the above applies),
and its vocabulary becomes this compiler's **intermediate representation**.

## The IR: what each marker means to the compiler

The compiler's emitters still write these five attributes onto the elements
they animate — not for any runtime to read, but so a human reading a
compiled scene file can see what a tween is *for* without cross-referencing
Python. The actual motion is emitted as explicit `gsap.set()` / `tl.to()`
lines in the scene's own inline `<script>`, following the pattern
`beats_to_composition.py`'s `render_scene()` already uses.

| Marker | Meaning | Compiler's emitted equivalent |
|---|---|---|
| `data-enter` | One entrance: fade + slide up 40px, 0.35s, `power3.out`. `data-enter="row"` staggers 0.8s; any other value staggers 0.12s (characters). | `tl.from(el, {opacity:0, y:40, duration:0.35, ease:'power3.out'}, offset)`, `stagger` set per the row/char distinction |
| `data-float` | Continuous breathing: ±6px, `sine.inOut`, yoyo, over half the scene duration. | `tl.to(el, {y:-6, duration:D/2, yoyo:true, repeat:1, ease:'sine.inOut'}, start)` |
| `data-sweep` | A brass hairline or clay sweep: `scaleX` 0→1, `power2.out`, 0.6s. | `tl.fromTo(el, {scaleX:0}, {scaleX:1, transformOrigin:'left center', duration:0.6, ease:'power2.out'}, start+0.4)` |
| `data-sh-count` | A numeric count-up, `power2.out`, capped at 1.2s or 60% of scene duration. | The proxy-object `onUpdate` counter pattern kept verbatim from `beats_to_composition.py:899-921` (`hfNum`) |
| `data-sh-strike` | A struck-through claim: `scaleX` 0→1 from the left, `power2.out`, 0.4s. | Same `fromTo` `scaleX` pattern as `data-sweep`, different duration |

## Anchors: the one idea worth keeping, for a reason the original never stated

`data-anchor` uses plain `opacity` instead of `autoAlpha`
(`visibility:hidden`) for a reason not in the original file's own comments,
but confirmed this session by reading the engine's own layout-audit source:
`autoAlpha` sets `visibility:hidden`, which removes an element from the
render's visibility/layout accounting *and* from motion-liveness sampling;
plain `opacity:0` leaves it geometrically present while still under the
liveness threshold. Anchors that must stay measurable (the frame-zero hook,
in particular) use `opacity`; everything else uses the runtime's own
`visibility` toggling on `data-start`/`data-duration`, which makes
`autoAlpha` redundant in this architecture — the runtime already hides
inactive scenes, so no compiler-emitted tween needs to.

## Defects fixed, not carried forward

Both are structural, not stylistic, so `sh-timeline.orig.js` is preserved
unmodified as provenance rather than patched in place:

1. `data-dur` → the compiler always computes and emits `data-duration` (on
   the `<template>` root) alongside a `data-dur` annotation (on the inner
   stage element, for Claude Design round-trip) — one computed number,
   two spellings, never two sources of truth.
2. Deferred registration → the compiler's emitted per-scene script builds
   and registers its timeline synchronously, at the point the `<script>`
   tag executes, with no `DOMContentLoaded` listener.
