# UnsourcedFlag

A small pill/badge that discloses authored usage guidance with no record in a project's
source-tracking system — the on-screen counterpart to this channel's truth-discipline rule
that a claim/instruction with no real source is flagged, never given a fabricated citation id.

- **`unsourcedflag-spike.html`** — the component (`.uf-badge`), shown beside its sibling
  `.uf-cite` real-citation pill for contrast, a live-context demo, and a `t`-driven debug
  scrubber. Start here.

## Why this one, and why now — a different shape of harvest than usual

Most entries in this catalog exist because the *same* component was independently rebuilt
byte-identically several times (`TermDefinition`'s story: five projects, one component, never
cataloged). This one is the opposite risk: the *concept* — an "○ UNSOURCED — no record in this
system"-style disclosure flag — converged independently across at least **six** shipped
videos (`pdrn-cellular-science`, `madecassoside-flat-matrix`, `centella-tiger-grass`,
`retinal-clinical-dossier`, `mugwort-healing-herb`, and `red-ginseng-glass-glow` before that
project later replaced its flag with a real citation) — but the *visual treatment* never did.
Confirmed by reading the actual shipped CSS in each:

| Project | Treatment |
|---|---|
| `pdrn-cellular-science` | `.uc-unsourced` — bare text, no border/fill/shape |
| `madecassoside-flat-matrix` | `.uc-unsourced` — bare text, no border/fill/shape |
| `retinal-clinical-dossier` | `.flag-unsourced` — `JetBrains Mono`, no pill |
| `centella-tiger-grass` | has an explicit color-discipline comment ("never coral/celadon/aqua/red") but no pill either |
| **`mugwort-healing-herb`** | **`.uc-unsourced` — bordered pill, subtle fill, `border-radius:999px`** |

`mugwort-healing-herb` only reached the pill treatment in its round 3.1 fix, *after* a review
correctly flagged the bare-text version as "genuinely plausible to misread as leftover
template output" — the same defect class the other four/five projects above still ship. This
entry harvests that fixed version as the **recommended** shared treatment, not as a
description of an existing consensus: as of this writing, five of the six projects above do
not use it and would need updating to match.

## What the badge must never be confused with

Its sibling is a real citation pill (`.uc-cite` in the shipped projects): coral-toned, carries
an author/year/PMID or similar. `.uf-badge` is deliberately ink-toned with a plain circular
glyph prefix — never coral, never journal-style typography — so a viewer can tell which is
which without reading either string closely. This is the same rule `faceless-video-craft`
`SKILL.md`'s own "never mistaken for a citation" note states for this exact pattern.

## Field contract

```js
{
  text: "○ UNSOURCED — no record in this system",  // shipped default — swap wording/glyph per
                                                     // project convention, keep ink/border/pill
  fadeInAt: 0.6,       // seconds into the scene's local timeline
  fadeInDuration: 0.4  // opacity 0 -> 1
}
```

No other fields — intentionally a single string in a fixed shell, not a multi-field
data-driven component. The one real per-use decision is timing: fire it while the unsourced
claim is actually being said or shown on screen, not before or after.

## Status

**SPIKE — not wired to a build pipeline.** Matches this catalog's existing convention: a
validated, self-contained visual reference (deterministic `t`-driven clock, seek-safe, no
`animation`/rAF), ready to paste into a real HyperFrames composition. Markup/CSS transcribed
verbatim from `mugwort-healing-herb`'s shipped `.uc-unsourced` (round 3.1).

**How to use it in a new video:** drop `.uf-badge`'s markup/CSS into the scene, set
`fadeInAt` to the moment the unsourced claim lands, and check here first — six shipped
projects each independently reached for this concept and five of them still ship a
treatment worth replacing.
