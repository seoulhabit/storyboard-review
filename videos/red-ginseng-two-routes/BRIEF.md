---
workflow: faceless-explainer
flow: automation
storyboard: yes
message: "Oral and topical red ginseng aren't interchangeable — each route is backed by a different study, for a different result"
destination: reels
aspect: 1080x1920
language: en
audience: "SeoulHabit's evidence-conscious skincare audience (same as the pdrn-skin-regeneration / snail-mucin-glass-skin / am-pm-skincare series)"
length: 40s
angle: concept
---

## Intent

Explain that oral and topical red ginseng are not interchangeable: each
delivery route is backed by a separate real clinical study, with its own
sample size, duration, and claim. Confident, clinical-but-warm dossier tone —
SeoulHabit's established "evidence held to rigor" house voice. Six scenes,
tightly paced: hook → botanical identity → oral/systemic route → topical
route → side-by-side comparison → end card. Adopted from the "dawn-to-dusk"
recipe (source: am-pm-skincare), with narration, angle, and length reset for
this script since the recipe's saved defaults (no narration, how-to, 45s)
didn't fit a VO-driven ~40s piece.

## Customizations

- Scene 3 (oral/systemic) key visual — "The Dermal Matrix": futuristic
  voxel-grid 3D render, camera plunges from just under the skin surface down
  into the dark dermis, looking up at the epidermis far above. Reveals a
  weak/collapsed collagen-elastin scaffold; pulsing red capillaries release
  glowing amber extract particles that attach to broken strands, which
  tighten and glow vibrant amber (a "REBUILD" transformation). Glowing white
  "BLOODSTREAM" / "SYSTEMIC" labels, small heart/vessel icon, matching
  UI scan-line framing. User-labeled illustrative/conceptual — not a literal
  claim.
- Scene 4 (topical) key visual — "The Epidermal Scan": same Hyperframe
  voxel-grid aesthetic, semi-transparent cross-section of upper skin strata,
  cool blue + amber/red + glowing white. An amber serum droplet impacts the
  surface from above; blue glow radiates only in the uppermost strata (deep
  dermis stays dark) and visibly smooths glowing jagged "wrinkle" lines
  ("SMOOTH" graphic). Small timer icon + glowing "8 WEEKS" near the smoothed
  wrinkle graphic, explicitly illustrative, not a restated claim. Steady
  illustrative tilt/zoom, gentle depth of field. Continuous camera logic with
  Scene 3: Scene 4 is the surface view Scene 3's plunge starts from.
- Scene 5 comparison: bring both route markers onto one block with an aqua
  accent; EvidenceMeter lockup (claim + chips + meter) weighting oral (78
  people, 24 weeks) against topical (23 people, 8 weeks) side by side.
- Reuse this repo's existing established visual system (EvidenceMeter,
  moss/teal/aqua accent, "no success color at any level" rule, deterministic
  t-driven clocks) documented in `../../catalog/README.md` — this is the
  fourth video in that same house style (siblings: PDRN, snail mucin, AM/PM
  routine). Resolved at Step 2 as the `code-editorial` frame preset (structural
  fit: hairline cards, JetBrains-Mono kicker/citation chrome, a warm-navy
  "code surface" repurposed as the citation/source-tracker surface, a
  serif-figure + mono-unit number lockup for the 78/24wk vs 23/8wk stats),
  remixed onto this project's own extracted brand tokens rather than the
  preset's stock palette — ink `#131516`, paper `#F7F5F0`, aqua `#59B8AE`,
  coral `#C97A5C` (near-exact match to the preset's own terracotta), celadon
  family `#4F6B52`/`#6F8F72`/`#93B896` for the "confirmed, no success color"
  role. See `frame.md`.

## Notes

- Full V4 script (VO + on-screen text, all 6 scenes) was pasted verbatim by
  the user and approved before this brief was written; `VO_MODE: verbatim` —
  use the exact wording scene-by-scene, do not restructure or reword. Saved
  to `capture/extracted/visible-text.txt` / `user_script.txt` in Step 1.
- Citations ING-ginseng-S001, S002, S005, S006 were already verified against
  a source record in an earlier review pass in this repo (see root-level
  `storyline_ginseng.html` and `storyline_ginseng.feedback.json`) — the study
  numbers in the script (78 randomized / 24wk / S002 for oral; 23 subjects /
  8wk / S001·S005·S006 for topical) match that prior verification exactly.
  Treat those four ids as the only sourced claims; the two Customizations
  render specs above are explicitly illustrative and must not be presented as
  additional citations.
- Integration-check flag from intake: Scenes 3 and 4 each carry six on-screen
  text fields (FRAME/CLAIM/ROUTE/STUDY/Note/CITATION) plus a camera-moving 3D
  render in ~10–12s. Sequence the text as beats (FRAME → CLAIM → ROUTE/STUDY
  → CITATION) synced to the camera move — do not reveal all six at once.
- A prior feedback note in this repo (`storyline_ginseng.feedback.json`)
  describes a flat 2D "DepthOfAction" diagram with a RouteIcon
  predicate.mjs/render.mjs component; those files could not be located
  anywhere in the current tree. Not a blocker — the two voxel-render
  Customizations above supersede that flat-diagram approach for this video.
- The adopted "dawn-to-dusk" recipe's own `frame.md` (AM/PM amber/violet
  system, copied in automatically on recipe adoption) was overridden at Step
  2: its hard rule ("nothing here carries a source-id citation") directly
  conflicts with this video's citation-driven premise, and its two-register
  day/night palette has no bearing on an oral-vs-topical concept. Replaced
  with `code-editorial` remixed onto real repo brand tokens (see
  Customizations above) instead of keeping the recipe's design system.
- Korean-glyph exception: two on-screen moments (`인삼 · Panax ginseng` in
  Scene 2, `습 SeoulHabit` in Scene 6) need a CJK-capable face — confirmed as
  a real defect, not a hypothetical: the sketch pass's server-rendered poster
  for Frame 6 showed a tofu/fallback glyph for `습` under the generic
  `sans-serif` stack. Fix applied to both sketch files:
  `font-family: "Noto Sans KR", sans-serif` scoped to just those two text
  nodes (`.identity-hero`, `.endcard-brand`) — not a blanket type-system
  swap. Per `hyperframes-creative/references/typography.md`, a real Google
  Fonts family outside the 18 pre-bundled ones is auto-fetched and embedded
  by the actual compiler at build/render time (with a lint warning, and
  fail-closed only on distributed/cloud renders — we're rendering locally).
  **Confirmed working** — re-checked both sketch posters after the initial
  Google Fonts fetch completed (took a few seconds the first time): `인삼` and
  `습` both render correctly now. No further action needed unless a real
  `npx hyperframes check`/render later regresses this.
- Voice/audio provider undecided: not signed in to HeyGen; local engines
  (Kokoro TTS, MusicGen) are installed but missing Python deps
  (`kokoro-onnx`, `soundfile`, `transformers`, `torch`, `numpy`). Ask the user
  to sign in (`npx hyperframes auth login`) or explicitly approve installing
  the local offline deps before Step 3.1 (audio) runs — do not default
  silently to either.
