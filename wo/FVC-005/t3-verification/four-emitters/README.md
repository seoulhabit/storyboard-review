# Four-emitter verification — ShCompare, ShMyth, ShQuote, ShSteps

Proves the emitters T3's own status file named as "implemented but not yet
exercised against a real render": the four of nine that the original
synthetic-t1-fixture didn't use.

## The fixture

`four-emitter.beat-sheet.json`: a 7-scene, 23.1s composition —
`ShHook -> ShCompare -> ShQuote -> ShMyth -> ShSteps -> ShEvidence ->
ShEndcard` — exercising all four target emitters alongside the three
already proven, in one coherent piece rather than four disconnected
fragments. Content is drawn from the design system's own worked examples
(`templates/reference/T4-comparison.dc.html`'s ascorbic-acid-vs-THD
comparison and verdict quote; `T5-myth-correction.dc.html`'s vitamin
C/niacinamide myth; `T2-how-to-use.dc.html`'s three-step routine).

## Two real bugs found and fixed

**Bug 1 — `ShCompare` grid overflow.** First compile passed `lint` but
`check` returned a real `canvas_overflow` warning: `"THD ascorbate"`
extended 94.6px past the right edge of the canvas, 16 occurrences across
the scene's full visible window. Root cause: `emit_sh_compare`'s
`grid-template-columns:1fr 1fr` container never set `min-width:0` on its
children — a standard CSS grid trap where a bare `1fr` track still
respects each item's default `min-width:auto`, refusing to shrink below
the unwrapped text's own width. `ShRows` already avoided this (its own
grid uses `minmax(0,auto)` tracks); `ShCompare`'s source JSX has neither,
so this would have hit the same overflow on a real render of the design
system's own component, not just this compiler's port of it. Fixed by
adding `min-width:0` and `overflow-wrap:break-word` to every grid child
(`#cid-a`, `#cid-b`, each attribute wrapper).

**Bug 2 — the continuous-motion fallback trusted one-shot markers.** The
`ShQuote` scene (3.2s, one hairline sweep + two entrances) tripped
`motion_frozen`: `"nothing moves within #root between 8.73s and 10.97s
(2.24s static)"`. The fallback added in the earlier D5 session's testing
checked `if not (float or sweep or count)`, treating any of the three as
equally sufficient — but `sweep`/`count`/`strike` are one-shot: they play
once early in a scene and then stop, so their presence says nothing about
whether motion continues for the rest of an arbitrarily long scene. Only
`float` (a yoyo+repeat tween spanning the *entire* scene duration by
construction) reliably prevents `motion_frozen` regardless of duration.
The bug had been latent since the first D5-fix session — it happened to
pass on `ShHook`'s 2.4s scene by coincidence (a 0.6s one-shot sweep leaves
only 1.4s of subsequent stillness, under the 2.0s ceiling) and only
surfaced here because `ShQuote`'s longer 3.2s scene pushed the same
one-shot-sweep pattern's residual stillness (2.24s) over that ceiling.
Fixed by changing the check to `if not float` — sweep/count no longer
suppress the fallback.

## Verified, after both fixes

- `hyperframes lint`: `0 errors, 0 warnings` across all 8 files.
- `hyperframes check --samples 40 --at-transitions --json`: `"ok": true`,
  every one of lint/runtime/layout/motion/contrast at `errorCount: 0` AND
  `warningCount: 0` — `check-9x16.json`, captured verbatim.
- The second static gate, `lint_composition.py`: `0 error(s), 0
  warning(s) across 8 file(s)`.
- Determinism: two independent compiles, `diff -r`, empty.
- **No regression** on either prior fixture (`synthetic-t1-fixture` and
  the D5 split fixture), both re-verified clean on 9x16 after these fixes.
- A real local render: exactly 23.100s, 693 frames. Four frames extracted
  (one per target emitter) and visually confirmed: `f_compare.png` shows
  `THD ASCORBATE` wrapped cleanly onto three lines, fully inside the
  canvas; `f_quote.png` shows the brass hairline, serif quote, and
  attribution; `f_myth.png` shows the struck-through muted claim and the
  correction with `DON'T` correctly in clay; `f_steps.png` shows three
  numbered steps with clay serif numerals and a brass connector, plus a
  muted note under step 1.

## Reproduce

```
python3 <claude-skills>/makemeavideo/scripts/compile_composition.py \
  four-emitter.beat-sheet.json /tmp/four-repro \
  --system videos/_system --format 9x16
cd /tmp/four-repro/06-render/9x16
hyperframes check --samples 40 --at-transitions --json
hyperframes render -q draft -o out.mp4
```
