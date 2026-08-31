---
workflow: faceless-explainer
flow: automation
storyboard: yes
message: "Snail mucin and Centella (Cica) aren't rivals with one winner — they solve different problems: snail for hydration/glow, Centella for redness/repair. And 'Cica' is just K-beauty's marketing name for Centella, not a separate ingredient."
destination: shorts
aspect: 1080x1920
language: en
audience: "Skincare-curious viewers confused by K-beauty ingredient naming — general beauty/skincare YouTube Shorts audience"
length: 30s
angle: comparison
VO_MODE: verbatim-with-two-corrections
---

## Intent

A ~30s tactile, macro-photography-led Short built from a user-supplied 5-beat
A/V script: the "Concern → Ingredient" comparison framework this channel has
already run once (`kbeauty-one-percent-line`), applied to two specific actives
instead of a label-literacy sweep. Presenter is the macro plate/texture, same
faceless departure `glass-skin-5-habits` made from this channel's usual
typographic-first house style — the user's own script direction says the
"string test" stretch is a mandatory, highest-retention hook visual, which a
still image cannot deliver.

## Assets

- SeoulHabit Video Design System — `assets/tokens/tokens.css` +
  `assets/fonts/NotoSansKR-500-subset.woff2`, both copied verbatim from
  `videos/seoulhabit-launch/assets/` (channel source of truth, see `frame.md`
  § Channel audit).
- `videos/kbeauty-one-percent-line/` — VO bus `data-fx-chain`, and the
  `.cta-chip-hb`/`.cta-chip-eq` equivalence-chip pattern reused for Frame 4's
  "CICA = CENTELLA ASIATICA" reveal.
- `videos/snail-mucin-truth/.hyperframes/caption-skin.html` — caption
  mechanism, reused and re-tokened (channel's only real caption
  implementation, per `glass-skin-5-habits/frame.md`'s own audit).
- `catalog/visual-components/split-face-protocol/` — bisector +
  independently-targetable-field *mechanism* adapted for Frame 5's
  snail-vs-centella verdict split. Literal skin (facial outline, clinical
  arms) dropped — see `frame.md` § Component reuse.
- `catalog/ingredient-photography/12-snail-mucin.png` — used as a material/
  lighting reference for the generated string-test video, NOT as its start
  frame; opening the file showed a pour into a dish, not a stretch (see
  `frame.md` § Corrections).
- `catalog/ingredient-photography/02-centella-asiatica.png` — reused for
  Frame 4/5, graded down from its native saturation toward `--leaf`.
- `catalog/product-photography/assets/B02-01.png` — reused cream-swirl plate
  for Frame 4's swipe beat.
- Generated: F1 palette still; F2 string-test video; F3 dropper video — see
  `frame.md` § Media exception for why video is permitted here.
- Voiceover: 5 narration lines via Higgsfield, voice "Kimberly"
  (`674b71b8-1d2e-4087-8567-d1f53c0b9f3c`, `voice_type: element`) — same
  voice as `kbeauty-one-percent-line`, `retinol-patch-test`,
  `glass-skin-5-habits`.
- SFX: demux foley from the two generated videos where usable; fall back to
  the channel's existing cue library — see `assets/MANIFEST.md`.
- BGM: reused verbatim from `retinol-patch-test/assets/bgm/track.mp3`.

## Customizations

**Two VO corrections** (user asked, chose to soften — see `SCRIPT.md` and
`frame.md` § Content corrections):
- Line 3: "you need Centella Asiatica" (exclusivity + treatment claim) →
  "Centella Asiatica is the better-studied pick" (comparative, not a cure claim).
- Line 4: "They are the exact same ingredient" ("Cica" is an unregulated
  marketing word, not a guaranteed 1:1 INCI identity) → "same plant, different
  label" — the precision moves to an on-screen mono qualifier chip on Frame 4.

**Media**: the mandatory string-test hook is generated macro `<video>`, not a
still — the channel's second use of generated video B-roll after
`seoulhabit-launch`'s precedent, and its own filed decision record (see
`frame.md` § Media exception).

**Duration**: VO-driven, not the script's own 30s beat grid — five beats kept
fixed, boundaries re-derived from measured `assets/voice/*.wav` durations
after generation, same method `glass-skin-5-habits` used.

## Notes

General-guidance disclaimer ships per channel convention — this is routine/
label literacy comparing two actives, not a locked `ING-*` source record for
either one, same status as `kbeauty-one-percent-line`.
