---
workflow: faceless-explainer
flow: automation
storyboard: yes
message: "Cica's tiger-grass legend is a hook; what actually matters is what madecassoside does for a wrecked skin barrier — and this system holds no source records for Centella, so every efficacy/mechanism line renders flagged UNSOURCED"
destination: shorts
aspect: 1080x1920
language: en
audience: "Over-exfoliated / damaged-barrier viewers + K-beauty enthusiasts (same series as pdrn-cellular-science)"
length: nominal 60s script; final runtime set by real Kimberly VO takes (see Notes)
angle: concept
---

## Intent

Build the user-approved seven-beat "Tiger Grass Protocol" script (2026-08-29 session) into a
HyperFrames Short: kinetic tiger-footage hook (0–5s pattern interrupt), then a hard pivot into
the SeoulHabit clinical-minimalist register for the remaining beats. VO wording kept as approved.

**Claim-sourcing posture (explicit, same confirmed posture as pdrn-cellular-science):** exhaustive
repo search (2026-08-29) finds NO Centella source records — `catalog/ingredients/` holds ginseng,
pdrn, retinal-vs-retinol, snail-mucin, and the glossary only. The glossary card
(`catalog/ingredients/skincare-ingredient-glossary/components/02-centella-asiatica.html`) supplies
nominal identity fields only: *Centella Asiatica · 병풀 · Botanical extract*. Therefore:

- Identity beat compiles from nominal fields only (name, Korean name, category, origin).
- Every efficacy/mechanism/protocol claim — madecassoside as primary active, inflammatory-signal
  shutdown, fibroblast activation / collagen rebuild, the stop-acids-start-Cica protocol — renders
  with the `○ UNSOURCED — no record in this system` flag (muted ink, no bracket, never coral).
- No citation id is ever invented. No `CITATION ⌞ ⌟` chip appears anywhere in this video, because
  no real record exists to cite.
- The tiger legend is narrated as legend ("Legend? Maybe.") and is not a claim surface.

This retains the approved script's claims per standing user direction rather than rebuilding the
narrative around sourced material — the same documented deviation from the lane's
claim-enforcement rule as PDRN, carrying the same unsubstantiated-health-claim exposure, flagged
here rather than silently absorbed.

**Audio posture:** full VO, Kimberly (Higgsfield `generate_audio`, model `seed_audio`,
voice_type `element`, voice_id `674b71b8-1d2e-4087-8567-d1f53c0b9f3c`) — the standing series
convention, a documented deviation from the lane's silent/captions-only rule. Burned-in top-band
captions (y 196–330) are a transcript of the real VO. VO text is TTS-clean (no colons, no
ACRONYM—expansion dashes).

**Generated-footage posture (new deviation, explicit):** the hook requires wild-tiger footage.
The lane rule is browser-drawn-only / no generative imagery; the approved script explicitly
demands the tiger hyperframe, so the hook plate is AI-generated video (Higgsfield
`generate_video`), used ONLY as the 0–5s legend visual — never as a claim surface, never as
documentary/clinical proof. All claim-bearing beats remain browser-drawn SVG/CSS.

## Customizations

- Beats 2–7 use the canonical house tokens verbatim (see frame.md) — dark-ground variant for the
  clinical pivot per the approved script ("dark backgrounds, clean white UI boxes"), matching the
  PDRN Round-2 precedent for dark beats, but with the lane's no-glow / one-aqua / matte discipline.
- Jagged-red→smooth-green inflammation line: red appears ONLY inside the beat-4 diagram as the
  literal "inflammation signal" state (PDRN beat-6 red/teal precedent — a genuine binary state),
  never as UI accent. The "calmed" state is celadon-family — but the diagram carries the
  `[Authored, illustrative — not a claim]` tag plus the UNSOURCED flag, and celadon here labels the
  calmed line inside a flagged illustration, not a sourced claim.
- Fibroblast grid: minimalist dot-grid → woven lattice, browser-drawn, illustrative tag + flag.
- Loop: final frame color-matches frame zero (tiger green) for seamless replay.

## Notes

- Scaffolded 2026-08-29 via `hyperframes@0.8.19 init --resolution=portrait
  --skill=faceless-explainer --example blank`; pin 0.8.19 per current workspace convention.
- `npm run render` carries `--quality high --workers 1` from day one (PDRN's static-frame-dedup
  defect fix + lane determinism rule) — not left to be rediscovered.
- All inner `.clip` `data-duration` values are authored against REAL measured VO durations, never
  nominal script timings (PDRN inner/outer duration defect, class of bug avoided at authoring time).
- Audio gate per convention: duration → silence → transcript-diff → adeclick → tail-spike scan.
  Delivery master −14 LUFS / ≤−1 dBTP, copied to `~/Desktop/ingredent videos/Centella/`.

## Round 5 — QC revision pass (2026-08-30, explicit direction)

Five fixes applied per QC review: header "ACTIVE COMPOUNDS · 4" → "INSIDE TIGER GRASS:";
protocol boxes made pixel-identical (390×290, flex-centered); intercut-2 aligned to S3's
first frame with 10-frame (0.333s) background cross-dissolves on all intercuts; out point
trimmed 73.0 → 72.0s (loop-out retimed to land the leaf-on-green by 72.0).

**Posture change, explicit and user-directed:** the four on-screen
`○ UNSOURCED — no record in this system` flags (beats 3/4/5/6) were REMOVED at the
requester's direction, with the underlying efficacy/mechanism/protocol claims retained
unchanged. This reverses the disclosure layer documented in the Intent section above and
was flagged to the requester (QC report + this pass) as increasing unsubstantiated-
health-claim exposure — the claims now render with no citation AND no flag. The
`[Authored, illustrative — not a claim]` tags and "· CLAIMED" kickers remain.

## Round 6 — silent cut (2026-08-30, explicit QC direction)

Out point set to exactly 71.0s; the loop-out (green sweep + leaf) DELETED as a perceived
stray asset — the video now ends on the CTA scene, and the seamless-replay hand-back to
frame zero no longer exists. Caption pills removed. The voiceover was briefly removed on a literal reading of
"remove the text pills and their associated narration entirely," then RESTORED same day
at the requester's correction (Round 6.1) — VO07 trimmed to end inside the 71.0 out
point, BGM back at 0.045 under the voice. VO takes remain in assets/voice/; the narrated composition is backed up as
index.html.rev5-with-vo.bak + compositions/frames/07-cta.html.rev5.bak. Illustrative
tags centered over the card column; fibroblast grid re-gridded perfectly uniform
(viewBox 710×310, dx=114, dy=72.7); mechanism marker now tracks the calm wipe's leading
edge in two eased segments. BGM raised 0.045→0.25 (it is now the foreground audio),
master −14.0 LUFS / −1.6 dBTP.

## Round 7 (2026-08-30)

QC item claiming missing CTA VO was stale (reviewer had the Round-6 silent cut) — verified
by transcribing the delivered master's 60–71s: full CTA narration present; no trim applied.
Applied: "Centella Asiatica" subtitle in the hook headline (frame-zero visible); master UI
anchor — every primary card top at y470 (identity 440→470, protocol split 492→470, CTA
560→470, killing the 0:58 drop); illustrative tags centered full-width and tucked under
their cards (1020/1075); mechanism red line now draws from its measured getTotalLength
(no dead-zone jump) with power1.out and a faster card entry; identity underlay gains
blur(5px) + card scales 0.9→1.0 over ~5 frames on entry.

## Round 8 (2026-08-30) — glassmorphism pass

QC items 1 (VO clipped at 0:59) and 3 (left-aligned disclaimers) were stale against the
current cut — verified by transcript ("...serum or cream. Morning and night." complete)
and by frame extraction (tags centered since Round 7); a 0.3s silence pad was added to
06.wav as margin anyway. Applied: glassmorphism on every card surface per explicit
direction (rgba(251,249,245,.6) fill, backdrop-blur 25 + saturate, 1px white edge,
Helvetica Neue-first type stack) — a deliberate departure from the matte/unlit house
style; active fibroblast label −17% to fit the card; PRIMARY ACTIVE label became a glass
pill tucked under the chips (y1046); follow pill raised 100px to y1130. Glass fill cost
contrast on four text elements — dimmed chips 0.4→0.58, symptom dim 0.38→0.52, calm/active
labels #4F6B52→#3E5641, red label #C2504A→#993F3A — restoring 0 contrast failures.
