# FactorConverge

A several-inputs-converge-on-one-node diagram: 3 outer nodes each draw a
connector line inward to a single center node, which arrives and pulses once
all three lines land — "several distinct things are what actually produce
this one outcome," without implying causation order or relative weight
between the inputs.

## Why this one, and why now

Harvested from `videos/pilling-vs-peeling/compositions/frames/04-factors.html`
(SKIN / FORMULA / APPLICATION converging on why a skincare pilling event
happens). A discovery pass across every existing `catalog/visual-components/`
entry before that scene was built found nothing matching this mechanism —
`ThresholdList` is a ranked list split by a cutoff, `SplitCompare` is a
two-thing bisector, `TermDefinition` is a single-term hero card — none of
them is "several inputs converge on one thing," which is a distinct enough
shape (a many-to-one causal diagram, not a comparison or a list) to earn its
own entry rather than being forced into an existing one.

## Field contract

```js
{
  headline: "Not automatically the product's fault.",
  nodes: [
    { label: "SKIN" },
    { label: "FORMULA" },
    { label: "APPLICATION" }
  ],
  caption: "Doesn't mean the product is bad."
}
```

**Exactly 3 nodes.** The geometry (two upper corners + one lower corner, all
three converging on a center node) is a fixed triangle, not an N-node array —
a real variant (4+ inputs, arranged in a circle around the center) is
something a future project would need to build, the same honest limitation
`StatReveal`'s own README discloses for its 100-tick coupling. Swap
`headline`, each node's `label`, and `caption`; the geometry itself is not
parameterized.

## The motion, and why it's shaped this way

- **Outer nodes settle first, staggered** — each a small scale-and-fade
  arrival (`back.out` ease), establishing the three inputs before anything
  connects them.
- **Connector lines draw in toward the center, staggered** — a
  `strokeDashoffset` reveal per line, each starting after the previous, so
  the convergence reads as three separate causes arriving rather than one
  simultaneous flash.
- **The center node is the payoff** — it fades in only once the first line
  has begun drawing, then pulses once (`scale` yoyo, bounded, never
  `repeat:-1`) the moment all three have connected. This is the component's
  one voltage moment; nothing else pulses.
- **No node is drawn as more important than another** — same radius, same
  stroke weight, same entrance timing shape (just staggered in sequence, not
  staggered in size or weight). The mechanism only asserts "these converge,"
  not "one of these matters more."

## Status

**SPIKE — not wired to a build pipeline.** Matches this catalog's existing
convention: a validated, self-contained visual reference (deterministic
`t`-driven clock, seek-safe, no `animation`/rAF, debug scrubber behind
`?debug=1`), ready to paste into a real HyperFrames composition. Verified
against the actual render before harvesting (`npx hyperframes check` clean,
frame-extracted and eyeballed at multiple timestamps) — see
`videos/pilling-vs-peeling/frame.md` § Verification for the record.
