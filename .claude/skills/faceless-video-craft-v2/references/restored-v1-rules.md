# Restored v1 rules — verbatim

Six rules v2 dropped with no replacement. Each caught a real, confirmed defect
in this channel's own shipping history (`REPORT-2026-09-01.md` §4.3). They are
reproduced here **verbatim** from `.claude/skills/faceless-video-craft/SKILL.md`
— the repo copy of v1 — because paraphrasing a rule is how its teeth get filed
off. `decision-policy.md` carries each one as a numbered rule at the stage where
it gates and points back here.

Two of the six are now enforced by a tool rather than by reading. The rule stays
either way: `check` tells you a threshold was crossed, this file tells you why
the threshold is where it is.

| | Rule | Policy id | Gates at | Enforced by |
|---|---|---|---|---|
| R1 | Type floors | `[S6/A-6]` | S6, before type is sized | reading + `check --snapshots` |
| R2 | Contrast 4.5:1 on rendered pixels | `[S6/A-7]` | S6 authoring, S7 gate | `hyperframes check` Contrast pass |
| R3 | `box-sizing: border-box` | `[S6/A-5]` | S6, first CSS rule | generator emits it; read frame 0 |
| R4 | Catalog discover / reuse / contribute | `[S6/A-1]` | S6 entry and run exit | reading |
| R5 | Post-render static-hold / cadence | `[S7/R-2]` | S7, on the muxed file | `check` `sweep_static` + `catalog/tooling/check-static-hold.py` |
| R6 | AAC true-peak headroom | `[S7/R-3]` | S7 audio master | `ffmpeg ebur128` on the shipped file |


---

## R1 · Type floors — `[S6/A-6]`

**Gates at:** S6 — Composition, before any type is sized
**Written for:** Six sub-floor type declarations shipped in the 2026-08-31 target.
**Source:** `.claude/skills/faceless-video-craft/SKILL.md` lines 1309-1323, verbatim.

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


---

## R2 · Contrast floor 4.5:1 on rendered pixels — `[S6/A-7]`

**Gates at:** S6 authoring; gated by `check` at S7
**Written for:** A shipped frame measuring 1.44:1 that the engine's own contrast checker passed 13/13.
**Source:** `.claude/skills/faceless-video-craft/SKILL.md` lines 1324-1370, verbatim.

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


---

## R3 · `box-sizing: border-box` — `[S6/A-5]`

**Gates at:** S6 — first rule in every composition's <style>
**Written for:** A `height:1920px` stage laying out at 2496px, pushing a CTA out of frame.
**Source:** `.claude/skills/faceless-video-craft/SKILL.md` lines 72-96, verbatim.

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


---

## R4 · Catalog lifecycle: discover, reuse, build, contribute — `[S6/A-1]`

**Gates at:** S6 asset+mechanism strategy, and the closing step of a run
**Written for:** The same term/definition card rebuilt five times across five videos; BarrierWall found only on the sixth.
**Source:** `.claude/skills/faceless-video-craft/SKILL.md` lines 738-807 (§*Catalog lifecycle: discover, reuse, build, contribute*), verbatim — the section heading is this rule's title above.

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


---

## R5 · Post-render static-hold / cadence pixel diff — `[S7/R-2]`

**Gates at:** S7 — after the render, on the muxed deliverable
**Written for:** Four of six scenes frozen 2.0-7.5s on a project that passed `check` with 0 errors.
**Source:** `.claude/skills/faceless-video-craft/SKILL.md` lines 1005-1101, verbatim.

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


---

## R6 · AAC intersample true-peak headroom — `[S7/R-3]`

**Gates at:** S7 — the audio master
**Written for:** A two-pass `loudnorm` hit -1.50 dBTP on PCM; the shipped AAC file measured +0.5 dBFS.
**Source:** `.claude/skills/faceless-video-craft/SKILL.md` lines 1536-1550, verbatim.

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
