---
version: alpha
name: PDRN Cellular Science — Frame
description: >
  Canonical SeoulHabit house tokens (the values both catalog visual-components and the
  captions tool default to) applied directly, not remixed — chosen over red-ginseng-two-routes'
  one-off hanbang palette so EvidenceMeter and SplitFaceProtocol port with zero color
  remapping. Portrait only (1080×1920).
unit: the frame — 1080×1920, 9:16 only
principle: one aqua accent per frame · celadon means sourced, never "winning" · coral is the
  one scarce voltage moment · an UNSOURCED flag is never mistaken for a citation

colors:
  ink: "#131516"
  paper: "#F7F5F0"
  aqua: "#59B8AE"        # the one "interrogated / under comparison" element per frame
  coral: "#C97A5C"       # the one "voltage" accent per frame — decorative use only (underlines, fills)
  coral-text: "#9F6149"  # coral darkened to clear WCAG AA on paper — required for citation-bracket text
  celadon: "#6F8F72"
  celadon-bright: "#93B896"
  celadon-deep: "#4F6B52"
  ink-faint: "rgba(19,21,22,0.62)"   # UNSOURCED marker text — never coral/celadon/aqua/red. Raised from an initial 0.45 after `hyperframes check` flagged it below WCAG AA (4.5:1) on paper; 0.62 clears it with margin.
  ink-muted: "rgba(19,21,22,0.62)"   # Note/secondary row text — same value as ink-faint; the UNSOURCED marker stays legible while reading as "quieter" via the ○ prefix, no-bracket, and ink (not coral) hue, not via extra transparency
  line: "rgba(19,21,22,0.12)"        # hairline borders/rules

borders: { hairline: "1px solid {colors.line}" }
shadows: { card: "0 1px 3px rgba(19,21,22,0.08), 0 4px 16px rgba(19,21,22,0.04)", none: "none" }

typography:
  body:      { fontFamily: "Inter", cqw: 2.2, weight: 400, lineHeight: 1.45 }
  label:     { fontFamily: "JetBrains Mono", cqw: 1.8, weight: 500, tracking: "0.05em" }
  kicker:    { fontFamily: "JetBrains Mono", cqw: 1.46, weight: 500, tracking: "0.16em", upper: true }
  citation:  { fontFamily: "JetBrains Mono", cqw: 2.0, weight: 500 }
  frame-line:{ fontFamily: "EB Garamond", cqw: 3.2, weight: 400, italic: true, lineHeight: 1.2, tracking: "-0.012em" }
  headline:  { fontFamily: "EB Garamond", cqw: 5.0, weight: 400, lineHeight: 1.08, tracking: "-0.015em" }
  kinetic:   { fontFamily: "Inter", cqw: 4.4, weight: 700, tracking: "-0.01em", upper: true }

components:
  claim-panel:
    backgroundColor: "{colors.paper}"
    border: "{borders.hairline}"
    rounded: "30px"
    shadow: "{shadows.card}"
    description: "The FRAME → CLAIM → ROUTE → STUDY → Note → CITATION card, ported structurally from red-ginseng-two-routes/compositions/frames/03-route-oral.html. FRAME is EB Garamond italic and asserts nothing; CLAIM is the compiled, sourced (or flagged) assertion; ROUTE/STUDY carry route+concentration+population+duration; Note carries the limitation. Never truncate a hedge, route, or population to save time."
  citation-chip:
    typography: "{typography.citation}"
    mark: "coral bracket ⌞ ⌟"
    description: "CITATION — ⌞ ING-pdrn-S00N ⌟. Coral, JetBrains Mono. Reserved exclusively for a real, verified source id. Never invented."
  unsourced-flag:
    typography: "{typography.citation}"
    mark: "○ prefix, no bracket, ever"
    color: "{colors.ink-faint}"
    description: >
      "○ UNSOURCED — no record in this system." Sits in the same slot as citation-chip but is
      never bracketed and never coral/celadon/aqua/red. The hollow-circle prefix reuses
      EvidenceMeter's own "checkpoint not passed" grammar rather than inventing new vocabulary.
      Bracket-vs-no-bracket is the instant tell between a real source and a flagged one.
  evidence-lockup:
    description: "Ported verbatim from catalog/visual-components/evidence-meter/evidencemeter-spike.html — lockup mode (claim + 4 checkpoint nodes + footnote) for ING-pdrn-S001; design mode (route + 4 attribute rows + chip row) for ING-pdrn-S003's real INJECTED data. Frame-zero always resolved (t===0 -> progress(1))."
  split-face-diagram:
    description: "Ported verbatim from catalog/visual-components/split-face-protocol/splitfaceprotocol-spike.html — #control-arm / #active-arm periorbital diagram, grounded in ING-pdrn-S004. Never a figurative face."
  illustrative-tag:
    text: "[Authored, illustrative — not a claim]"
    description: "Red-ginseng's own convention (Frame 1) for a dimensional/illustrative visual that dramatizes a mechanism without asserting it as fact. Applied to the DNA-fragment, lock-and-key, and cellular-factory visuals in this project — none of which are backed by a source record."
---

# PDRN Cellular Science — Frame

## Brand adaptation

This project builds directly on the canonical house tokens (see frontmatter) rather than
inventing or remixing a new palette — both catalog components (`evidencemeter-spike.html`,
`splitfaceprotocol-spike.html`) and the captions tool's own default (`data-brand-tokens` in
`red-ginseng-two-routes/compositions/captions.html`) already agree on these exact hex values.
Building on this set means both ported components need zero color remapping.

## The one rule that governs every frame here

Two layers per beat: an authored **FRAME** line that asserts nothing, plus a **CLAIM** that is
compiled and never strengthened or softened. A CLAIM either carries a real `CITATION` (coral
bracket, a verified `ING-pdrn-S00N` id) or an `UNSOURCED` flag (muted ink, no bracket) — never
neither, never both implied at once. See STORYBOARD.md for the exact per-line mapping.

## Material direction

Matte, unlit, flat-shaded — no specular, no rim light, no depth-of-field, no glow beyond a single
bounded `ambient-glow-bloom` moment per beat marking a claim landing (never a decorative glow).
Illustrative/dimensional visuals (DNA fragments, the A2A lock-and-key, the fibroblast factory) are
browser-drawn SVG/CSS/canvas only — no generative imagery — and always carry the
`[Authored, illustrative — not a claim]` tag, small and subordinate, never competing with the
claim panel below it.

## Color discipline

- **Aqua** — exactly one "interrogated / under comparison" element per frame. Never a plain accent.
- **Coral** — exactly one "voltage" moment per frame — the citation bracket, or a kicker mark. Never two.
- **Celadon** family — "sourced, at every evidence level," never a success/failing-grade read. A
  2-of-4 EvidenceMeter reads exactly as honestly as a 4-of-4 — never a win/loss color.
- **No red, no green-as-success, no glow-as-decoration.**

## Motion grammar

`power3.out` long-tail settles; no bounce, no overshoot, no elastic ease anywhere. Frame zero is
always the dense, fully-built pause state on every component (ported components already guard
this: `if (t === 0) tl.progress(1)`). Ambient loops (a slow phase-driven breathe, a subtle jitter)
are bounded and settle — never an unbounded yoyo.

## Safe area

Portrait 1080×1920. Keep bottom-anchored chips/citations above **y ≈ 1580px** (clear of the
caption band, which starts at 1600px per `captions.html`) and clear of the right **~162px**
(15%) button rail. `slide-pad` ~80px on every edge otherwise.

## Fonts

EB Garamond (FRAME lines, headlines) · Inter (CLAIM/ROUTE/STUDY body text, kinetic hook type) ·
JetBrains Mono (labels, citation/unsourced-flag chips, kickers). Loaded per-composition via
Google Fonts — matches every sibling project's own approach (no bundled WOFF2 in this project).

## Round 4 — mobile-legibility / safe-zone / component-reuse pass

A later brief asked for this specific project to maximize mobile legibility, enforce a stricter
platform safe zone, and standardize component reuse across all six beats. Applied project-wide;
supersedes the type scale and per-beat card treatments above where they conflict.

**Safe zone (explicit, not left to coincidental centering):** every beat's content band is
`y ∈ [288px, 1440px]` — 15% padding from the top, 25% from the bottom, on the 1920-tall canvas.
Horizontal margins (96px sides, clearing the right ~15% button rail) are unchanged from the
original convention above.

**Type scale (Inter replaces JetBrains Mono for every label, field, citation, and flag — mono is
dropped project-wide, not just for one component):**
- `uc-kicker` / small tags: Inter 600-700, 2.3–2.4cqw (~25px)
- `uc-field-label` / row labels: Inter 700 uppercase, 2.3cqw
- `uc-field-value` / row text: Inter 500, 2.8cqw
- `uc-claim`: Inter 600, 3.3cqw
- `uc-citation-pill` text: Inter 700, 2.8–2.9cqw
- `uc-unsourced`: Inter 600, 2.6cqw

Every size clears a ~24px-equivalent floor (2.22cqw at this canvas width) with margin. Headline/
kinetic type (EB Garamond names, kinetic hooks) was left at its original scale — already far
above the floor — except beat 6's CTA, bumped for hero presence.

**`.uc-card`** — the one reusable rounded card, used in beats 2, 3, 4, and 5 (identity, clinical
history, mechanism, fibroblast summary): `background:#FBF9F5` (or `#F7F5F0` where the card
doubles as the diagram's own ground, as in beat 4); `border:1px solid rgba(19,21,22,.12)`;
`border-radius:28px`; the same two-layer shadow as before. **Must include `position:absolute`
directly on the rule** — a real bug this round: three of the four cards initially set `top`/`left`
with no `position`, which silently no-ops on a plain div and pins the card to (0,0). Caught by
rendering and visually inspecting actual frames, not by `npm run check` (its layout inspector
checks for overflow/off-canvas issues, not this project's specific 15%/25% rule — that still needs
a human/visual pass).

**`.uc-citation-pill`** — the one reusable citation badge, replacing the old plain bracket text
line: celadon-tinted pill (`rgba(111,143,114,.12)` fill, `#6F8F72` border, full `border-radius:
999px`), ink lead text + coral-text bracketed id, Inter 700. Used everywhere a real citation
appears (beats 3 ×2, beat 6). The celadon tint is deliberate, not decorative — it's the same token
that already means "sourced" everywhere else in this system, so the badge's own color now carries
that meaning too, rather than introducing an unrelated new accent.

**Two deliberate exceptions, not oversights:**
- **No literal green/red status-pill binary.** The requesting brief asked for reusable "green/red
  circular indicator pills." Beat 3's EvidenceMeter checkpoints stay celadon-only (filled when
  verified, empty when not) — never red — because a 2-of-4 must read exactly as honestly as a 4-of-4,
  never as a partial failure. Beat 6's existing red(damaged)/teal(healed) pills (an explicit prior
  request, not this rule) are kept and reused as-is; that red/teal pairing was not extended to any
  other frame, since nowhere else in this script has a genuine binary state to represent.
- **Beats 1 and 6 stay dark, not white cards.** Both carry glow/neon treatments (also explicit
  prior requests) that read correctly only against a dark ground. They still comply with the
  bigger-type and safe-zone rules; only the card-color standardization was scoped to the four
  claim-bearing frames where a white card doesn't fight an existing effect.

## Known gaps

- No `DepthOfAction` component exists anywhere in this repo (confirmed by grep) — the mechanism
  beat (04) uses a bespoke flat lock-and-key illustration instead, exactly as red-ginseng
  substituted its own voxel dives for the same missing dependency.
- This frame.md is written fresh for this project rather than adapted from red-ginseng's — that
  file documents a different, one-off remix lineage (the "code-editorial"/hanbang palette) that
  doesn't apply here.
