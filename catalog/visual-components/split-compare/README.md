# SplitCompare

A vertical bisector dividing the canvas into two independently-targetable
fields, with a tint flood that floods only the *interrogated* side — the
mechanism for "these two things aren't rivals, they solve different
problems" without a figurative face or a clinical protocol attached to it.

## Why this one, and why now

Harvested from `videos/centella-cica-vs-snail-mucin/compositions/frames/05-cta.html`
(`.split-*` classes, IDs prefixed `f5-`) — that video's closing verdict split
(Snail vs. Centella). The mechanism itself was adapted there from
`catalog/visual-components/split-face-protocol/` — a bisector, two
independently-targetable field groups, one paused `t`-driven timeline, tint
flooding one side only, no success color — but SplitFaceProtocol's own
content is fixed to a facial outline and a clinical control/active-arm
protocol. Once the mechanism was pulled free of that skin, it had nothing
face- or clinical-trial-specific left in it: it applies to any two-thing
comparison where one side is the one being interrogated (a claim being
checked, a recommended pick, the "answer" of the two) — an ingredient
comparison, a before/after, a "which settings" pick, a competitor split.
Named for the mechanism, not the source video's ingredients, following this
catalog's own convention (`EvidenceMeter`, `GradedScale`, `ThresholdList`).

**Not independently re-verified against DesignSync this session** — same
disclosure as `threshold-list`'s and `term-definition`'s READMEs.
Transcribed from the one shipped implementation; this is this session's own
generalization of a pattern used exactly once, not a confirmed design-system
component name.

## Field contract

```js
{
  left:  { label: "CONTROL" },
  right: { label: "VARIANT" },
  interrogated: "right"   // "left" | "right" -- which field the tint floods
}
```

Labels are free text (kept short — this is a full-bleed 1080-wide split, not
a card). `interrogated` picks which field is the "answer" side; the flood
never appears on both, and the un-interrogated side stays plain (optionally
desaturated — see Motion) rather than getting a second, competing tint.

Each field is a plain content block in the spike (a flat placeholder panel) —
in real use this is where a photographic plate, a diagram, or any other
media goes. The mechanism doesn't care what's inside a field; it only owns
the bisector, the flood, and the label.

## The motion, and why it's shaped this way

- **Divider first.** A thin vertical rule draws in (`scaleY` 0→1) down the
  canvas center — the claim "these are being split apart" lands before
  either side does anything else.
- **Labels next**, one per field, fading up independently — never a single
  shared label, since the whole point is that the two fields are
  independently targetable.
- **The flood** is the component's one voltage moment: a single accent color
  (aqua in the source video; any one accent color in general use) washed
  over the interrogated field only, `mix-blend-mode: multiply` so it reads as
  a tint on the content rather than a flat color block sitting on top of it.
  Never both fields at once — that would be two accents in one frame, which
  breaks the "no success color, no doubled accent" law this catalog's other
  rules-based components (`evidence-meter`, `graded-scale`,
  `split-face-protocol`) already carry.
- **The un-interrogated field can desaturate slightly** (a mild
  `grayscale()`/`brightness()` filter) to read as "the control," the same
  "before/after" convention `split-face-protocol` itself documents — this is
  optional polish, not the mechanism's core claim.
- No bounce/elastic/back easing, no infinite keyframes, per this system's
  motion law — the flood's entrance is the only sustained tween; everything
  else is a single settle.

## Status

Validated visual spike, generalized from one real shipped frame. **Not wired
to build.mjs** — like this catalog's other spikes, the real HyperFrames
composition pipeline doesn't consume this file directly; a project adopting
it copies the mechanism (markup + timeline shape) and supplies its own
fields, tokens, and duration.
