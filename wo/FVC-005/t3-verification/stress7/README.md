# Seven-emitter stress test — ShHook, ShRows, ShSteps, ShEvidence, ShMyth, ShQuote, ShEndcard

Systematic adversarial-text stress test of the seven emitters not yet
individually torture-tested (`ShCompare` and `ShIngredient` were already
fixed for the same defect class in prior passes). One combined 7-scene
fixture, deliberately loading every slot with either a genuinely
unbreakable long word (the same real 24-character INCI term used for
`ShIngredient`, `"Polymethylsilsesquioxane"`) or a long unbreakable
citation-style token, so every emitter is stressed in one coherent
composition rather than seven disconnected fragments.

## Seven real defects found, all fixed

**Six overflow bugs, the same defect class already found twice
(`ShCompare`, `ShIngredient`), now confirmed in the remaining
components** — every one is a flex or grid child missing `min-width:0`
and/or its text missing `overflow-wrap:anywhere`:

1. **`ShHook`** — the accent `<span>` overflowed. Root cause was actually
   structural, not just missing properties: the wrapping `display:
   inline-block` div shrink-to-fits its content, which makes
   `max-width:100%` on the `<h1>` inside it circular (100% of a box that
   sizes to fit that same content is not a real constraint). Fixed by
   switching the wrapper to `display:block` (so it takes its parent's
   real width) plus `min-width:0` and `overflow-wrap:anywhere` on the h1.
2. **`ShRows`** — left/right terms already had `min-width:0` from the
   start (this component was written carefully) but no
   `overflow-wrap:anywhere`, so an unbreakable term still overflowed its
   own grid cell. Added the missing property.
3. **`ShSteps`** — the action-label wrapper is a grid item in a
   `minmax(0,1fr)` track but had no `min-width:0` of its own (a track's
   `minmax(0,…)` does not override its items' default `min-width:auto`).
   Fixed with `min-width:0` on the wrapper plus `overflow-wrap:anywhere`
   on both the action label and the note.
4. **`ShEvidence`** — the outer wrap is a flex item of `#cid-stage` (same
   position `ShIngredient`'s `#cid-wrap` was in) with no `min-width:0`,
   and its caption (already `max-width:90%`) and source had no
   `overflow-wrap`. Fixed both.
5. **`ShMyth`** — same flex-item gap on the outer wrap, plus the claim's
   wrapper had the identical `inline-block` shrink-to-fit issue as
   `ShHook`. Fixed with `min-width:0` throughout, `display:block` on the
   claim wrapper, and `overflow-wrap:anywhere` on claim and correction.
6. **`ShQuote`** — same flex-item gap on the outer wrap; `line` grew to
   1516.72px (wider than the 1080px canvas). Fixed with `min-width:0` on
   the wrap and `overflow-wrap:anywhere` on `line`/`attribution`.

`ShEndcard`'s `cta` was fixed defensively too (its test text happened to
have spaces, so it did not fail this specific fixture, but the same
structural gap was there and a genuinely unbreakable CTA would have hit
it).

**One much more serious, structurally different bug: every compiled
video's closing scene opened with a ~0.17s completely blank cream
flash.** Not an overflow — a real dead hold, confirmed by exact-frame
extraction (frames 702–706 of 774, t=23.400–23.533, pixel-uniform, zero
variance) immediately after the hard cut into the endcard scene. Root
cause: `ShEndcard`'s three elements (mark/word/cta) all use the standard
delayed entrance (cold-seek `opacity:0`, fade in starting at local
t=0.15s) — which is fine for every OTHER scene, because every other scene
also has a citation chip that renders immediately, unconditionally,
bridging the gap. Confirmed across all six of the design system's own
extracted templates (`templates/reference/T1..T6`) that the closing
scene is the *only* one that structurally never has a chip — so this was
not a rare edge case, it would have been present at the end of **every
single video this compiler ever produces**, with zero exceptions,
until this fixture happened to test a full composition all the way
through to its own ending rather than stopping at whichever scene was
the subject of the test.

Fixed by extending the same "compose immediately, no entrance" rule the
compiler already applies to the video's overall frame zero to *any*
scene with no chip to bridge the entrance gap — not by hand-tuning
`ShEndcard` specifically, since the underlying condition (nothing visible
during the entrance offset) could in principle recur for any future
chip-less scene.

## One finding investigated and ruled a check-tool artifact, not a defect

After the fix, `check --at-transitions` still reports `content_overlap`
and `text_occluded` on `#quote-line`/`#quote-attr`/`#quote-chip`, all at
exactly `time: 23.4` — the precise instant of the hard cut from `quote`
into `cta`. Investigated rather than dismissed:

- A frame extracted well inside the quote scene (t=22.0, no boundary
  nearby) shows the layout is genuinely clean — `frame-quote-mid-scene.png`.
- The actual rendered frame at the exact boundary (frame 702,
  `frame-boundary-702.png`) shows the endcard content alone, fully
  correct, with **no trace of the quote scene's content** — no overlap,
  no occlusion, nothing wrong.
- The same finding does **not** appear at any of the other five hard-cut
  boundaries in the same 7-scene composition, so it is not a universal
  "every hard cut trips this" artifact.

Conclusion at the time: a check-tool artifact, not a defect, on the
strength of these two frames. **The precise mechanism was later confirmed**
by reading `hyperframes@0.8.30`'s own source
(`collectTweenBoundaries`/`toTimelineTime`/`seekCompositionTimeline` in
`dist/cli.js`) and verifying it live against a running instance of this
exact fixture: `--at-transitions`'s generic scrub-seek path
(`window.__player.renderSeek`, the same API the interactive Studio preview
uses) leaves the outgoing scene's `.clip` visible for one extra frame
(~33ms) past its own `data-duration` end when the *incoming* scene is
`ShEndcard` specifically — but the actual frame-capture render pipeline
does not share that lag, confirmed by inspecting the real rendered PNG at
the exact reported time. Full chain of evidence, with the source citations
and the decisive rendered frames, in
`../artifact-mechanism/README.md`.

## Verified, after all seven fixes

- `hyperframes lint`: `0 errors, 0 warnings` across all 8 files.
- `hyperframes check --samples 40 --at-transitions --json`: `"ok": true`.
  All five categories `errorCount: 0`; the only remaining findings are
  the two `layout` warnings above, investigated and accounted for.
- The second static gate, `lint_composition.py`: `0 error(s), 0
  warning(s) across 8 file(s)`.
- A real local render: exactly 25.800s, 774 frames — confirmed
  frame-by-frame (not sampled) that no frame in the composition is blank
  and the transition into the endcard is clean.
- **No regression** on any of the four prior fixtures (`synthetic-t1`,
  the D5 split, the four-emitter fixture, the `ShIngredient` overflow
  fixture), all re-verified clean after these fixes.

## Reproduce

```
python3 <claude-skills>/makemeavideo/scripts/compile_composition.py \
  stress7.beat-sheet.json /tmp/stress7-repro \
  --system videos/_system --format 9x16
cd /tmp/stress7-repro/06-render/9x16
hyperframes check --samples 40 --at-transitions --json
hyperframes render -q draft -o out.mp4
# Confirm no blank frame at the endcard boundary (frame 702 at 30fps for
# this exact fixture; recompute as start_of_last_scene * fps for others):
ffmpeg -i out.mp4 -vf "select='between(n\,698,712)'" -vsync 0 frame_%03d.png
```
