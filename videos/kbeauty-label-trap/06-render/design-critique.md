# Design Critique — kbeauty-label-trap (S7 mandatory gate)

Reviewed: all 16 extracted frames in `06-render/frames-final/` (frame 0, each
scene's settle point, the s01→s02 transition midpoint, last frame).

## Overall Impression

The signature stamp device genuinely earns its "one signature component"
status — it isn't decoration bolted onto separate scenes, it's the same
semantic object (a verification mark) doing the same job every time it
appears. The dark/porcelain register alternation is legible and intentional.
The single weak point is `s05` (Q1's dose beat), which is sparse enough to
read as a generic AI-explainer slide despite passing every mechanical gate.

## Usability

| Finding | Severity | Recommendation |
|---|---|---|
| s01's ingredient-list ribbons are set in vertical (`writing-mode:vertical-rl`) text at a viewing speed the audience can't pause for | 🟡 Moderate | A viewer has ~3s before the scene moves on; vertical text takes longer to parse than horizontal. Consider horizontal micro-columns or dropping to fewer, larger ingredient names if this scene gets revisited. |
| s05 leaves ~65% of the canvas empty (two small elements confined to the upper-left/upper-center) | 🟡 Moderate | Not a safe-area or contrast issue — a genuine composition gap. The scene reads as under-designed relative to the rest of the piece. |

## Visual Hierarchy

- **What draws the eye first**: the vermilion stamp, consistently, everywhere it appears (s02's passport, s03/s12's seal arrays, s14's lock) — correct, since it's the signature device and the throughline of the whole video's argument.
- **Reading flow**: strong in the diagram scenes (s04, s06, s08, s10, s11) — each has a clear top-to-bottom or left-to-right path with the citation/tag as the final beat the eye lands on. s05 has no such path; the two dots don't compose into a sequence the eye is guided through.
- **Emphasis**: correctly weighted — regulatory citations (s04, s06, s09) get the quiet mono-chip treatment, the five memory-anchor phrases get the vermilion sub-headline treatment, nothing competes with the stamp for attention.

## Consistency

| Element | Issue | Recommendation |
|---|---|---|
| Dark/porcelain register | None — s01/s02/s03 (bench, dark) → s04–s11 (mechanism diagrams, porcelain) → s12 (reveal, dark, exact bench reuse) → s13 (recap, porcelain) → s14 (landing, dark) is a legible, motivated alternation, not arbitrary switching. | Keep as-is. |
| Stamp device | Consistent geometry (double-ring, rotated, mono-glyph) across all 5+ uses. | Keep as-is — this is the piece's real strength. |
| Whitespace discipline | s04/s06/s09/s10/s11 all fill their canvas with intent; s05 does not. | See s05 fix above. |

## Accessibility

- **Color contrast**: 23/23 automated checks pass WCAG AA (`hyperframes check`); the below-cutoff canyon rows and the UnsourcedFlag chips were both hand-verified against the tool's own suggested colors.
- **Text readability**: type floors respected throughout (40px+ body, 32px absolute floor on labels/chips) — no readability concerns beyond the vertical-ribbon usability note above.

## What Works Well

- The vermilion stamp as the single signature device, reused with real semantic continuity (identity mark → question seal → final lock) rather than as a repeated decorative badge.
- The bench/bottle reuse between s01 and s12 (identical markup, only the liquid data differs) — the mystery resolves using the same visual object the audience already knows, which is exactly the kind of continuity this format usually lacks.
- Citation chips and UnsourcedFlag badges are visually distinct from each other by design (mono ink-toned pill vs. accent-bordered pill) — a viewer can tell "this is disclosed as uncertain" from "this is cited" without reading either string closely.

## Priority Recommendations

1. **Redesign s05's composition** to fill more of the frame with intent — either scale up the two-dot diagram into a fuller size-comparison visual, or add a third compositional element (e.g., a faint background ingredient-list ghost, echoing s04's canyon) so the scene doesn't read as the odd one out. Not fixed this round — logged as the top follow-up for the next revision pass, alongside the cadence gate's pacing findings.
2. **Reconsider the vertical ribbon text in s01** if this scene is revisited — legibility at real viewing speed is a genuine, if minor, concern.
3. Everything else reviewed holds up — ship as-is on the current findings.
