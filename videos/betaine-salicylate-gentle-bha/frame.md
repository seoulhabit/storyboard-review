---
version: alpha
name: Betaine Salicylate — The Gentle Alternative — Frame
description: >
  Canonical SeoulHabit house tokens applied directly, carried forward verbatim from
  videos/pdrn-cellular-science/frame.md (the user's explicit style reference) including
  that project's Round-4 mobile-legibility components and Round-12 safe-zone/caption
  conventions. Portrait only (1080×1920).
unit: the frame — 1080×1920, 9:16 only
principle: one aqua accent per frame · celadon means sourced, never "winning" · coral is
  the one scarce voltage moment · an UNSOURCED flag is never mistaken for a citation ·
  this video contains ZERO real citations, so no coral citation bracket appears anywhere

colors:
  ink: "#131516"
  paper: "#F7F5F0"
  aqua: "#59B8AE"        # the one "interrogated / under comparison" element per frame
  coral: "#C97A5C"       # the one "voltage" accent per frame — decorative use only (underlines, kickers)
  coral-text: "#9F6149"
  celadon: "#6F8F72"
  celadon-bright: "#93B896"
  celadon-deep: "#4F6B52"
  ink-faint: "rgba(19,21,22,0.85)"   # UNSOURCED marker text at PDRN Round-12 strength (raised from 0.62)
  ink-muted: "rgba(19,21,22,0.62)"   # secondary row text
  line: "rgba(19,21,22,0.12)"

borders: { hairline: "1px solid {colors.line}" }
shadows: { card: "0 1px 3px rgba(19,21,22,0.08), 0 4px 16px rgba(19,21,22,0.04)", none: "none" }

typography:
  body:      { fontFamily: "Inter", cqw: 2.8, weight: 500, lineHeight: 1.35 }
  kicker:    { fontFamily: "Inter", cqw: 2.4, weight: 700, tracking: "0.06em", upper: true }
  field-label: { fontFamily: "Inter", cqw: 2.3, weight: 700, upper: true }
  claim:     { fontFamily: "Inter", cqw: 3.3, weight: 600, lineHeight: 1.45 }
  unsourced: { fontFamily: "Inter", cqw: 3.4, weight: 600 }
  frame-line:{ fontFamily: "EB Garamond", cqw: 3.2, weight: 400, italic: true, lineHeight: 1.2 }
  headline:  { fontFamily: "EB Garamond", cqw: 5.6, weight: 400, lineHeight: 1.1 }
  kinetic:   { fontFamily: "Inter", cqw: 4.4, weight: 700, tracking: "-0.01em", upper: true }

components:
  uc-card:
    description: "The one reusable rounded card (PDRN Round 4): background #FBF9F5 (or #F7F5F0 when it doubles as a diagram ground), border 1px solid rgba(19,21,22,.12), radius 28px, two-layer card shadow, position:absolute REQUIRED on the rule (the top/left-without-position bug is documented in the PDRN BRIEF). Used on every paper claim-bearing frame."
  uc-unsourced:
    text: "○ UNSOURCED — no record in this system"
    description: "Inter 600 3.4cqw, ink at 0.85 alpha, hollow-circle prefix, never bracketed, never coral/celadon/aqua/red. Sits in the citation slot on every claim in this video (no real record exists for any of them)."
  illustrative-tag:
    text: "[Authored, illustrative — not a claim]"
    description: "Small subordinate tag on every dimensional/illustrative visual (barrier erosion, molecule dock, pore/hydration diagram). Never competes with the claim row."
  dark-stage:
    description: "Frames 1 and 5 only: the PDRN Round-2 dark glow register (deep #131516 stage, bounded neon accents) — structurally dark-only, an explicit prior style request carried forward. All other frames are paper."

---

# Betaine Salicylate — Frame

## The one rule that governs every frame here

Two layers per beat: an authored FRAME/hook line that asserts nothing, plus a CLAIM that
is compiled from the user's script and never strengthened. Every CLAIM in this video
carries the `○ UNSOURCED` flag — zero Betaine Salicylate records exist in this system,
and no citation id is ever invented. Questions ("LOVE BHA, HATE THE PEELING?") and
engagement CTAs assert nothing and carry no marker.

## Color discipline

- **Aqua** — exactly one interrogated element per frame (the bond point in frame 3, the
  clear pore channel in frame 4).
- **Coral** — at most one voltage moment per frame (a kicker underline). With no real
  citations in this video, coral never appears as a bracket.
- **Red/cyan binary** — frame 1 only (irritated vs calm), reusing PDRN beat-6's
  damaged/healed vocabulary; frame 5's neon-cyan CTA type reuses the same cyan. Nowhere
  else — no other frame has a genuine binary state.
- No green-as-success. No glow outside the two dark frames (1 and 5).

## Material and motion

Matte, unlit, flat-shaded on paper frames; bounded neon glow only inside the two dark
frames (the carried-forward Round-2 exception). `power3.out` long-tail settles; no
bounce/elastic anywhere except nothing — the PDRN Round-2 collagen jiggle is not
carried here (frame 3's dock lands with one precise snap, no overshoot). Frame zero on
every frame is the dense, fully composed pause state (`if (t===0) tl.progress(1)` where
applicable; frame 1 is fully composed at t=0 per the PDRN blank-frame-zero fix).

## Safe area (PDRN Round-12 final convention)

Portrait 1080×1920. Content band: the middle 60% — y ∈ [384, 1440] for anything that
must be read (cards may start at ~300 when stacked rows need height, but their text
stays inside). No ink past x=918 (right ~15% button rail). Bottom 20% (y ≥ 1536)
carries nothing, ever. Burned-in captions live in the top band (y 196–330), ink pill /
paper text, Inter 800 40px — the only strip clear of scene content in all five beats.
Frame zero carries no caption.

## Fonts

EB Garamond (FRAME lines, identity headline) · Inter everywhere else (fields, claims,
markers, kinetic and caption type). Loaded per-composition via Google Fonts, matching
every sibling project.
