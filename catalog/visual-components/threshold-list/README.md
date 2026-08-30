# ThresholdList

A ranked list split by a cutoff line: rows above the line are in meaningful
order, rows below are not — visualized with a "rule slam" landing at the
cutoff and a lateral scramble beat on the below-cutoff rows that makes "order
stops mattering here" a visual claim, not just a spoken one.

## Why this one, and why now

Harvested from `videos/kbeauty-one-percent-line/compositions/frames/04-one-percent-line.html`
(`.opl-*` classes, IDs prefixed `opl-`) — the scene that *is* that video's
whole thesis: "ingredients are listed by concentration only until the 1%
mark; after that, order means nothing" (`caption.txt`, point 2). It was
built once, for that exact claim, and never generalized — but the mechanism
underneath (a ranked list, a threshold, a visual "this side counts / this
side doesn't" split) has nothing INCI-label-specific about it. It applies to
any "top N vs. the rest," "before/after a legal or clinical cutoff," or
"counted vs. cosmetic ordering" beat — this catalog's naming convention
(`EvidenceMeter`, `GradedScale` — mechanism-first, not campaign-first) is
followed here rather than keeping the source's `OnePercentLine` framing.

**Not independently re-verified against DesignSync this session** — same
disclosure as `term-definition`'s README. Transcribed from the one shipped
implementation; unlike TermDefinition this pattern has not been proven by
repeated independent reimplementation, so treat the generalization (the
`above`/`below` field contract below) as this session's extraction, not a
confirmed design-system component name.

## Field contract

```js
{
  title: "THE 1% LINE",          // the threshold's name/claim
  above: ["WATER", "GLYCERIN", "NIACINAMIDE", "CENTELLA ASIATICA EXTRACT"],
  below: ["PHENOXYETHANOL", "FRAGRANCE", "TOCOPHEROL"]
}
```

Row counts in each group are not fixed — the spike builds `.tl-row` elements
from `above.length` / `below.length` rather than the source's hardcoded 4/3
split. The scramble beat (see below) targets the **last two** below-cutoff
rows specifically, not a fixed pair — it degrades gracefully to a single
jitter or no scramble at all if `below` has fewer than two entries.

## The motion, and why it's shaped this way

- **Above-cutoff rows** rise+fade in first, individually staggered — this is
  the "list you're meant to actually read."
- **The rule slam** (`--coral`, this component's one voltage moment — never
  doubled with `--aqua` in the same frame, per this design system's
  one-accent-per-frame rule) lands in normal document flow directly above the
  first below-cutoff row, timed to the claim's payoff beat.
- **Dynamic zoom-pan-zoom** on the list container (`transform-origin: 0 0`)
  pushes in on the above-cutoff cluster while it's explained, pans down to
  land on the rule slam, then pulls back out — because the full list read too
  small on a 1080-wide mobile canvas at flat scale in the source build.
- **Below-cutoff rows desaturate and drift** once the rule lands — a visual
  demotion, not just a color difference.
- **The scramble beat** exists to fill a specific problem: a flat multi-second
  freeze between the rule landing and the camera pulling back, during VO that
  is *actively describing* disorder ("after this, they can be in any order").
  A vertical position-swap was tried first in the source and lint-flagged for
  `content_overlap` (two text boxes crossing through the same space
  mid-transition) — the shipped fix is lateral opposite-direction jitter,
  which has no shared space to cross. Keep this fix if reusing the beat;
  don't reintroduce a vertical swap.

## What's genuinely reused vs. generalized in this spike

- Every token, timing constant, and the rule-slam/zoom/scramble choreography
  are transcribed unchanged from the shipped scene.
- The `above`/`below` arrays, and building `N` + `M` rows instead of a fixed
  4 + 3, are this session's generalization — the source hardcodes seven
  specific INCI terms.
- The demo content ("THE CUTOFF" / generic label set) is invented for this
  spike; the real "THE 1% LINE" / INCI-ingredient content stays in
  `videos/kbeauty-one-percent-line/`, not duplicated here.

## Status

**SPIKE — not wired to `build.mjs`.** Debug scrubber behind `?debug=1`
(`t=0` / `t=end`, a range input driving `window.renderFrame(t)`), matching
every other timed spike in this catalog.
