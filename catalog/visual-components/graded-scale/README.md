# GradedScale

"Component 4/5" in the day's in-page numbering.

- **`gradedscale-spike.html`** — "Strict Enum Badge." Five discrete nodes
  for one attribute (e.g. "Gentleness"), integers 1–5 only — no
  interpolation, no clamping a 0–100 score onto it. `validateGradedScale()`
  refuses anything outside `{1,2,3,4,5}` before a node paints, so a bad
  value fails the build instead of drawing a plausible-looking lie. Same
  "no success color" rule as EvidenceMeter: every active node reads the same
  regardless of score.

Pairs naturally with [EvidenceMeter](../evidence-meter/) when a scene needs
both a per-claim confidence grade and a per-attribute 1–5 rating on screen
together. See [../../README.md](../../README.md) for the full catalog.
