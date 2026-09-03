# Restored v1 rules — verbatim

Eight rules v2 dropped or never had. Each caught a real, confirmed defect
in this channel's own shipping history (`REPORT-2026-09-01.md` §4.3; R7 and R8
were added 2026-09-02 from the `ectoin-survival-molecule` review). They are
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
| R7 | Cuts, crossfades, and transitions | `[S6/A-8]` | S5 beat sheet, S6 emission | generator derives the overlap; `[S7/R-2]` extracts each midpoint |
| R8 | Motion idiom by narrative function | `[S6/A-10]` | S6, per beat | `catalog/tooling/continuity-audit.py` counts signatures |


---

## R1 · Type floors — `[S6/A-6]`

**Gates at:** S6 — Composition, before any type is sized
**Written for:** Six sub-floor type declarations shipped in the 2026-08-31 target.
**Source:** `.claude/skills/faceless-video-craft/SKILL.md` lines 2328-2342, verbatim.

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
**Source:** `.claude/skills/faceless-video-craft/SKILL.md` lines 2343-2389, verbatim.

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
**Source:** `.claude/skills/faceless-video-craft/SKILL.md` lines 845-914 (§*Catalog lifecycle: discover, reuse, build, contribute*), verbatim — the section heading is this rule's title above.

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
**Source:** `.claude/skills/faceless-video-craft/SKILL.md` lines 1180-1484, verbatim.

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


---

## R6 · AAC intersample true-peak headroom — `[S7/R-3]`

**Gates at:** S7 — the audio master
**Written for:** A two-pass `loudnorm` hit -1.50 dBTP on PCM; the shipped AAC file measured +0.5 dBFS.
**Source:** `.claude/skills/faceless-video-craft/SKILL.md` lines 2558-2572, verbatim.

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


---

## R7 · Cuts, crossfades, and transitions — `[S6/A-8]`

**Gates at:** S5 — the beat sheet names each scene's transition; S6 — the generator derives the overlap window
**Written for:** `videos/ectoin-survival-molecule`, 28 of 28 boundaries hard cut on a 340s long-form piece by correct application of v1's Shorts-derived rule. Every gate passed; the review called it "a sequence of separate slides".
**Source:** `.claude/skills/faceless-video-craft/SKILL.md` lines 1813-1968, verbatim.

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

  Three caveats on the wipe. It only clips, so it cannot place content
  anywhere a settled frame does not already have it — that is the whole
  argument, and it holds only if the settled frames are themselves compliant.
  An animated clip over a **raster** is the `drawElement` capture bug above:
  safe on a browser-drawn piece (confirmed by grepping every scene for `<img>`
  and finding none), suspect the moment a plate is inside the wiped region.

  And **the engine's own layout pass reports a wipe boundary as
  `content_overlap` / `text_occluded`, which is a false positive you have to
  expect rather than fix.** That pass tests bounding-box geometry and does not
  model `clip-path`, so a clipped incoming wrapper still presents a full-canvas
  opaque box over the outgoing scene's text. The rendered frames show both
  scenes correctly with a clean seam; nothing is occluded.

  What makes it a trap is that **its severity moves with sampling density, not
  with the composition.** Severity is persistence-aware, so a finding seen in
  one sample demotes to info and one seen in several is an error. Measured on
  the same generated 3-scene proof, wipes versus cuts:

  | | layout errors |
  |---|---|
  | cuts, any `--samples` | 0 |
  | wipes, `--samples 9` | 1 |
  | wipes, `--samples 20` | 3 |
  | wipes, `--samples 60` | 3 |

  A 340s piece with 28 wipes reported **0 errors and 26 info** at `--samples
  40`, because a 0.45s window is rarely hit twice when samples sit 8.5s apart.
  So the same technique passes on the long piece you developed against and
  gates on a short one, or starts gating the moment someone raises
  `--samples`. Confirm the boundary on an extracted frame, record the finding
  with its reason, and do not restructure the composition to satisfy it.

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

---

## R8 · Motion idiom by narrative function — `[S6/A-10]`

**Gates at:** S6 — Composition, per beat, before any entrance is authored
**Written for:** the same render. 29 of 29 scene timelines declared `defaults: { ease: "power3.out" }`; 128 of 196 real tweens (65%) carried it, but grepping for the ease name returns 8 hits and reports variety.
**Source:** `.claude/skills/faceless-video-craft/SKILL.md` lines 417-472, verbatim.

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
