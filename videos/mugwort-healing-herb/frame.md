---
version: alpha
name: Mugwort Healing Herb — Frame
description: >
  Canonical SeoulHabit house tokens, paper-dominant register carried over from
  madecassoside-clinical-cut (no dark stage-box anywhere). Portrait only (1080×1920).
unit: the frame — 1080×1920, 9:16 only
principle: one aqua accent per frame · coral is the one voltage moment (beat 04's ✕) ·
  an UNSOURCED flag is never mistaken for a citation · captions from the authoritative
  script, ASR for timing only
colors:
  ink: "#131516"
  paper: "#F7F5F0"
  card: "#FBF9F5"
  aqua: "#59B8AE"
  aqua-text: "#3A7871"       # required whenever aqua colors readable text (3:1 large-text on paper)
  coral: "#C97A5C"
  coral-text: "#9F6149"
  ink-muted: "rgba(19,21,22,0.62)"   # WCAG floor for low-emphasis text — not self-enforcing, apply explicitly
  line: "rgba(19,21,22,0.12)"
typography:
  headline-kinetic: { fontFamily: "Inter", weight: 800, upper: true }
  name-serif: { fontFamily: "EB Garamond", note: "ingredient name + CTA question only" }
  fields-claims: { fontFamily: "Inter", weight: "500-700", note: "24px-equivalent floor" }
---

# Mugwort Healing Herb — Frame

- Safe areas: captions top band y=240 (round 3: nudged from 196 for extra top-UI
  clearance, bounded well short of the content band below); content band y ∈ [384,1440]; diagram field
  640px wide centered (right ~15% rail clear); claim cards 822px at x=129.
- Diagram fields hairline-bordered directly on paper; `[Authored, illustrative — not a
  claim]` tag bottom-left on every illustrative state.
- Mugwort sprig (beats 01/06): hand-authored deterministic SVG path set, identical
  geometry in both frames — the CTA ghosts it back in as the loop's landing pad.
- Citations (beat 03 only): `.uc-cite` pills, Jung et al. 2018 · PMID 29353040 and
  Jung et al. 2017 · PMID 28899779, with explicit scope line "Mouse model · human skin
  cells in vitro — not a human clinical trial". Beats 04/05 carry
  `○ UNSOURCED — no record in this system` instead — the protocol and absorption
  framings are authored guidance.
- Motion: `power3.out` settles; no overshoot anywhere (nothing in this video snaps into
  a structure, so nothing earns back.out). Alarm-ray jitter in beat 03 decays via
  deterministic timeline onUpdate — never rAF.
- Frame zero = beat 01 fully composed (name + underline + sprig + kicker + tag opaque
  at t=0; only sub-pixel settles animate).
- Beat grid from real Kimberly takes: S1=0.000 S2=11.400 S3=21.700 S4=36.500 S5=51.600
  S6=63.600, total 73.900s.
