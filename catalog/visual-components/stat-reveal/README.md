# StatReveal

A single-statistic hero beat — a large numeral counting up to its final
value, a plain-language qualifier, a human-readable citation chip, and a
tick-grid pictogram that shows the same fraction as 100 discrete unit
squares. The mechanism for "here's the one number this claim rests on,"
without borrowing chart grammar (an axis, a gridline, a plotted point) that
would imply a real measurement sits behind an illustration rather than
behind the numeral itself.

## Why this one, and why now

Harvested from `videos/pilling-not-dead-skin/compositions/frames/03-study.html`
(`#numeral3`, `#qual3`, `#chip3`, the `.tick` grid) — that video's stat beat
("41% of 528 women, ages 20–49"). Built as a new component because a
catalog-discovery pass (production-loop step 1) found no stat/big-number
reveal anywhere in `catalog/visual-components/` — grepped every spike for
stat/percent/count-up markup and came up empty, despite at least four prior
videos (`kbeauty-one-percent-line`, `ceramides-barrier-diagnostic`,
`hyaluronic-acid-serum`, and others) each building some version of a numeral
callout from scratch. This is that shared source, following this catalog's
naming convention (`EvidenceMeter`, `SplitCompare`, `ThresholdList`) rather
than the source video's own ingredient/topic.

**Not independently re-verified against DesignSync this session** — same
disclosure as `split-compare`'s and `term-definition`'s READMEs. Transcribed
from the one shipped, fully post-render-verified implementation (frame
extraction confirmed: no numeral/qualifier overlap after a fix, the tick
grid reaches its full lit count by the scene's own end, safe-area and
static-hold checks both pass on the source video's real render).

## Field contract

```js
{
  percent: 58,                          // drives BOTH the numeral count-up and the
                                         // tick-fraction (percent of 100 ticks lit)
  qualifier: "of 300 survey respondents",
  citation: "Consumer Study · 2024",    // Journal/source · year only -- never a raw
                                         // internal ID or DOI (see the parent skill's
                                         // "what must never reach a rendered frame")
  tickCaption: "58 OF 100 RESPONDENTS"
}
```

The `percent`-driven tick fraction only reads cleanly when the stat genuinely
is a percentage out of a sensible base. For a raw count instead (e.g. "3 of
4 dermatologists"), light `tickLit` ticks directly against a smaller total
grid rather than reusing the 100-unit percent coupling — that's a real
variant this spike doesn't build, not a limitation to paper over.

## The motion, and why it's shaped this way

- **The numeral counts up, not fades in.** `0% → percent%` over 0.6s, driven
  by a plain tween on a `{v:0}` object with `onUpdate` writing
  `textContent` — a pure function of tween progress, seek-safe, no `--p`
  custom property involved (this catalog's `term-definition` and others
  document why a `--p`-driven *opacity* specifically is unsafe; a numeric
  count-up via `onUpdate` doesn't have that failure mode, since it's driven
  by the timeline's own progress value each seek, not a CSS custom property
  read at an arbitrary time).
- **Qualifier, then citation, staggered** — the population/sample-size
  context lands before the source, so a viewer reads "58% of 300
  respondents" as one clause before the provenance stamp arrives.
- **The tick grid is the scene's continuous back-half motion**, lighting one
  unit at a time in reading order across roughly the scene's last 1.3s —
  this is what keeps a stat scene from reading as "done" the instant the
  numeral finishes counting, and it's the component's only sustained tween.
- **Never chart grammar.** No axis, no gridline, no plotted line/point
  anywhere in this component — the tick grid is a pictogram (isotype-style
  discrete units), which counts without implying an instrument measured
  anything. See the parent skill's "a diagram is not a chart unless it
  plots real data" rule.

## Status

Validated visual spike, generalized from one real shipped, fully
post-render-verified frame (not just a design-time spike this time — the
source scene's overlap defect was caught by `npx hyperframes check`'s layout
pass, fixed, and the fix confirmed against the actual render before this
harvest). **Not wired to build.mjs** — like this catalog's other spikes, a
project adopting it copies the mechanism (markup + timeline shape) and
supplies its own `DATA`, tokens, and duration.
