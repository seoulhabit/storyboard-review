---
version: alpha
name: Centella Tiger Grass — Frame
description: >
  Canonical SeoulHabit house tokens applied on a dark clinical ground for beats 2–7 (the
  approved script demands "dark backgrounds, clean white Ingredient Identity UI boxes"),
  with the tiger hook as the single photographic plate. Portrait only (1080×1920).
unit: the frame — 1080×1920, 9:16 only
principle: one aqua accent per frame · celadon means sourced-or-calmed-inside-a-flagged-diagram,
  never "winning" · coral is the one scarce voltage moment · an UNSOURCED flag is never mistaken
  for a citation · red exists only inside the beat-4 inflammation diagram as a literal state

colors:
  ink: "#131516"
  paper: "#F7F5F0"
  dark-ground: "#101314"      # clinical-pivot background (beats 2–7)
  card: "#FBF9F5"             # the white "Ingredient Identity" UI card on dark ground
  aqua: "#59B8AE"
  coral: "#C97A5C"
  coral-text: "#9F6149"
  celadon: "#6F8F72"
  celadon-bright: "#93B896"
  signal-red: "#C2504A"       # ONLY the beat-4 "inflammation signal" line state
  paper-faint: "rgba(247,245,240,0.62)"  # UNSOURCED marker + muted text on dark ground
  ink-faint: "rgba(19,21,22,0.62)"       # UNSOURCED marker + muted text on card
  line-dark: "rgba(247,245,240,0.14)"    # hairlines on dark ground
  line: "rgba(19,21,22,0.12)"            # hairlines on card

typography:
  headline:  { fontFamily: "EB Garamond", weight: 400, lineHeight: 1.08, tracking: "-0.015em" }
  kinetic:   { fontFamily: "Inter", weight: 800, tracking: "-0.01em", upper: true }
  body:      { fontFamily: "Inter", weight: 500, lineHeight: 1.4 }
  label:     { fontFamily: "Inter", weight: 700, upper: true, tracking: "0.08em" }
  caption:   { fontFamily: "Inter", weight: 700 }

components:
  uc-card:
    backgroundColor: "{colors.card}"
    border: "1px solid {colors.line}"
    rounded: "28px"
    positionRule: "position:absolute REQUIRED on the rule (PDRN Round-4 bug class)"
    description: "The one reusable rounded card. Identity fields, compound chips, protocol rows."
  unsourced-flag:
    text: "○ UNSOURCED — no record in this system"
    mark: "○ prefix, no bracket, ever"
    description: "Muted (paper-faint on dark, ink-faint on card). Never coral/celadon/aqua/red.
      Sits adjacent to every efficacy/mechanism/protocol claim in this video — there are no
      citations here because no Centella record exists."
  illustrative-tag:
    text: "[Authored, illustrative — not a claim]"
    description: "On the inflammation-line diagram (beat 4) and fibroblast lattice (beat 5)."

## Safe area & caption band (series convention, supersedes PDRN's bottom band)
- Captions: TOP band, y ∈ [196, 330], Inter 700, word-timed to real VO.
- Content: y ∈ [384, 1440]; keep readable content x < 918 (clear of right button rail).
- Nothing readable below y ≈ 1440 (bottom UI strip) or above y ≈ 196.

## Motion grammar
power3.out long-tail settles for all clinical beats; no bounce/elastic. Hook beat (tiger) is the
one kinetic exception: hard cuts + scale snaps inside 0–5s, then the pivot cut lands the register
change. Frame zero = fully-built hook frame with headline caption already composed (scroll-stop).
No glow anywhere; elevation shadows only. One aqua per frame. Coral spent once per frame max.

## Material
Matte, flat. The tiger plate carries a single unified grade (slight green-lift LUT feel via CSS
filter kept constant across its cuts). All diagrams SVG/CSS, stroke-first, no fills-with-specular.

## Fonts
EB Garamond · Inter, via Google Fonts (series convention; caption + label mono is dropped per
PDRN Round 4 — Inter everywhere except EB Garamond display).
---
