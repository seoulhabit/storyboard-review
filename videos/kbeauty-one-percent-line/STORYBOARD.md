---
message: "K-beauty ingredient labels use two legal loopholes (extract dilution, the 1% ordering rule) — here's how to read past them."
audience: "K-beauty-curious skincare shoppers who read ingredient lists but don't know the 1% rule or Hanbang INCI names"
mode: autonomous
format: 1080x1920
duration: 105s
---

Eight frames, fixed script (user-supplied, restructured only for content
accuracy — see `frame.md` § Content corrections), fully faceless. Frames
alternate `data-track-index` 0/1; each scene's clip runs 0.5s past the next
scene's start for a cross-fade overlap (except the final frame). Target
durations below are pre-generation estimates; **boundaries are finalized
from measured real VO length per line** once `assets/voice/*.wav` exist, per
the seoulhabit-launch precedent — this section is updated with final numbers
after generation. Design source: `frame.md`.

## Frame 1 — hook

- status: planned
- src: compositions/frames/01-hook.html
- type: hook
- start: 0.0
- duration target: ~8.0s
- blueprint: kinetic-type-beats (Hook) — rapid stat flash + cross-out, one
  new element every ~2s
- rules: dynamic-content-sequencing, spring-pop-entrance
- beat: Paper ground. Three faint serum-silhouette marks flash top band
  (SFX: cash-register + bass hit). Big Inter-800 kinetic block "80%
  GINSENG?" snaps in center. Ink strikethrough slashes across it (SFX:
  buzzer), "0.5% GINSENG." pops beneath in coral. VO (verbatim): "Does your
  favorite Korean serum claim to be packed with 80% Ginseng? What if the
  actual amount is less than a single drop?"

## Frame 2 — promise

- status: planned
- src: compositions/frames/02-promise.html
- type: branding
- start: ~8.0
- duration target: ~7.0s
- blueprint: titlecard-reveal — kinetic headline build
- rules: dynamic-content-sequencing
- beat: Ink ground. Mono kicker "CRACKING THE CODE" builds letter-by-letter
  (SFX: keyboard typing). Split-frame motif: a beaker icon (left, aqua
  outline) and an ingredient-label rectangle (right) suggest chemist ↔
  label, snapping together with a `--d-snap` scale pop. VO: "Today we are
  cracking the code on K-beauty labels using a trick cosmetic chemists use
  to spot the marketing fluff."

## Frame 3 — the extract loophole

- status: planned
- src: compositions/frames/03-extract-loophole.html
- type: concept
- start: ~15.0
- duration target: ~13.0s
- blueprint: split-screen comparison, dynamic-content-sequencing
- rules: dynamic-content-sequencing, spring-pop-entrance
- beat: Split ground — left half paper (labeled "WESTERN"), right half ink
  (labeled "K-BEAUTY"), aqua rule down the center. Left: mono chip "WATER —
  1st ingredient." Right: mono chip "CENTELLA EXTRACT — 70%" (aqua
  highlight, this frame's one aqua hit). SFX pop on each chip. Then
  "EXTRACT" (Inter-800, center) breaks into two stacked words on ink-weight
  fracture lines (SFX: glass shatter): "WATER" + "TINY BIT OF PLANT." VO:
  "First: The Extract Loophole. Western serums almost always list water
  first. But K-beauty? You'll see seventy percent Centella Extract. Here's
  the secret: an extract is usually just a tiny bit of the plant steeped in
  a water solvent."

## Frame 4 — the 1% line

- status: planned
- src: compositions/frames/04-one-percent-line.html
- type: concept (this video's coral "voltage moment")
- start: ~28.0
- duration target: ~14.0s
- blueprint: scrolling-list-reveal + hard-cut rule slash
- rules: dynamic-content-sequencing
- beat: Ink ground (SFX: alert ping). Mono INCI list scrolls downward
  (Water, Glycerin, Niacinamide, Centella Extract...). A coral rule
  (`--rule-w-strong`, this video's single voltage moment) slams across the
  list at "PHENOXYETHANOL" (SFX: laser-slice). Everything below the rule
  shifts to `--ink-3`, drifts down and fades. Label "THE 1% LINE" in
  EB Garamond sits above, aqua underline. VO: "Next, the holy grail: The 1%
  Line. Ingredients are legally listed by concentration, until the one
  percent mark. After 1%, brands can scramble them in any order."

## Frame 5 — the trick

- status: planned
- src: compositions/frames/05-the-trick.html
- type: concept
- start: ~42.0
- duration target: ~13.0s
- blueprint: highlight + directional-arrow callout
- rules: dynamic-content-sequencing
- beat: Ink ground. "PHENOXYETHANOL" and "ETHYLHEXYLGLYCERIN" mono chips
  highlight aqua (SFX: ding-ding-ding, stagger). A large downward aqua arrow
  (SVG stroke-draw, `--d-fast`) points to a fan of botanical-name chips
  below (fading to `--ink-3`, marked "<1%"). VO (corrected — see `frame.md`
  § Content corrections): "Look for preservatives like Phenoxyethanol or
  Ethylhexylglycerin. Phenoxyethanol has an actual legal cap around 1%.
  Ethylhexylglycerin sits in that same fractions-of-a-percent range. Once
  you spot them, every single ingredient listed after makes up less than 1%
  of the bottle."

## Frame 6 — live teardown

- status: planned
- src: compositions/frames/06-teardown.html
- type: proof / worked-example
- start: ~55.0
- duration target: ~20.0s
- blueprint: label-card teardown, dynamic-content-sequencing
- rules: dynamic-content-sequencing, spring-pop-entrance
- beat: Paper ground (SFX: whoosh + thud). A typographic mono label card
  drops in — "BEAUTY OF JOSEON — GLOW SERUM: PROPOLIS + NIACINAMIDE"
  (generic text card, no brand trade dress/logo). Real published order
  (verified against incidecoder.com/incibeauty.com — see `frame.md`):
  Propolis Extract, Dipropylene Glycol, Glycerin, Butylene Glycol, Water,
  **Niacinamide (2%)**, 1,2-Hexanediol, Melia Azadirachta Extract, Sodium
  Hyaluronate, Centella Asiatica Extract ... **Ethylhexylglycerin** ...
  Dextrin, Pentylene Glycol, Tocopherol, Xanthan Gum, Carbomer. An aqua
  circle-stroke draws around "NIACINAMIDE (2%)" (SFX: marker squeak). A
  coral-adjacent ink strikethrough slashes under "ETHYLHEXYLGLYCERIN" (SFX:
  sharp slash — kept ink-weight, not coral, since coral's one voltage
  moment already spent in Frame 4). Everything below it desaturates to
  `--ink-3` and blurs 2px (design-system-legal focus blur, not a glow). VO
  (corrected): "Let's do a live teardown. Beauty of Joseon Glow Serum. We've
  got Propolis Extract making up the bulk, and our active Niacinamide at
  2%. Perfect. Now, hunt for the 1% line... Boom. Ethylhexylglycerin.
  Everything below it — dextrin, xanthan gum, tocopherol — is basically
  fairy dust."

## Frame 7 — Hanbang rapid fire

- status: planned
- src: compositions/frames/07-hanbang-rapidfire.html
- type: listicle
- start: ~75.0
- duration target: ~20.0s
- blueprint: flashcard-sequence, dynamic-content-sequencing
- rules: dynamic-content-sequencing, spring-pop-entrance
- beat: Ink ground (SFX: camera-shutter cadence, `--d-snap` per card). Three
  flashcards snap in sequence, each a mono INCI name → EB Garamond common
  name + one-line function, Noto Sans KR gloss where relevant: "Snail
  Secretion Filtrate → Snail Mucin (barrier repair)"; "Panax Root → Ginseng
  (firming)"; "Artemisia Princeps → Mugwort · 쑥 (calming)". One aqua
  underline per card on the common name. VO: "Finally, the Hanbang cheat
  sheet. Korean skincare uses traditional herbs with wildly confusing INCI
  names. Snail Secretion Filtrate? That's Snail Mucin for barrier repair.
  Panax Root? Ginseng for firming. Artemisia Princeps? That is just Mugwort
  for calming acne."

## Frame 8 — CTA / endcard

- status: planned
- src: compositions/frames/08-cta-endcard.html
- type: cta
- start: ~95.0
- duration target: ~10.0 (no cross-fade tail — final frame)
- blueprint: titlecard-reveal (freeze-grid) — adapted from
  `red-ginseng-two-routes/06-endcard.html`
- rules: (blueprint's own signature move only — no infinite loop; finite
  pulse ends before frame end)
- beat: Paper ground (SFX: camera flash). Frozen grid of the video's
  cheat-sheet chips (Water-first, 1% line, the 3 Hanbang pairs) settles into
  a clean mono grid. "SCREENSHOT THIS" in Inter-800 pulses 2–3x
  (finite yoyo, `--e-inout`) then holds. 습 SeoulHabit lockup (Noto Sans KR
  500) + disclaimer line below in `--t-caption`: "General label-reading
  guide — not sourced claims, not medical advice." VO: "Screenshot this
  cheat sheet for your next Stylevana haul. Drop the exact name of the
  serum you want me to decode next in the comments!"

## Audio

- BGM: one energetic instrumental bed, `assets/bgm/track.mp3`,
  `data-volume 0.12`, `data-fx-carve` against the `voiceover` group,
  `strength 0.25`.
- VO: 8 lines, `assets/voice/{01..08}.wav`, one locked TTS voice
  (text2speech_v2/elevenlabs — custom element voice "Kimberly",
  user-specified), routed through the shared `voiceover` `hf-audio-group`
  chain (see `frame.md` § Audio mix).
- SFX: one file per named cue in the script (cash register, buzzer,
  keyboard, pop, glass shatter, alert ping, ding-ding-ding, whoosh+thud,
  marker squeak, sharp slash, camera shutter, camera flash) —
  `assets/sfx/`, `data-track-index` 20+, `data-volume ≈0.35`.

## Build history

- 2026-08-28: STORYBOARD drafted from user-supplied script; two content
  corrections applied (fake "seed oils below the line" claim, overstated
  "globally capped" claim for Ethylhexylglycerin) after fact-checking
  Beauty of Joseon's real published INCI list. Frame timings were
  pre-generation targets.
- 2026-08-28: VO generated (text2speech_v2/elevenlabs, custom voice
  "Kimberly", element id `674b71b8-1d2e-4087-8567-d1f53c0b9f3c` — user
  specified mid-build, replacing the initially-generated "Isla" preset).
  Measured durations: 01=7.20s, 02=7.28s, 03=13.76s, 04=11.60s, 05=19.04s,
  06=17.52s, 07=18.96s, 08=6.80s. Final scene boundaries below are set from
  these measured lengths, each with a ~1.0s trailing hold (3.0s on Frame 8,
  the ending hold) before the next scene's cross-fade, per the
  seoulhabit-launch precedent of setting boundaries from real VO length
  rather than an even split.

| Frame | start | duration (incl. 0.5s tail except last) |
|---|---|---|
| 01 hook | 0.00 | 8.70 |
| 02 promise | 8.20 | 8.78 |
| 03 extract-loophole | 16.48 | 15.26 |
| 04 one-percent-line | 31.24 | 13.10 |
| 05 the-trick | 43.84 | 20.54 |
| 06 teardown | 63.88 | 19.02 |
| 07 hanbang-rapidfire | 82.40 | 20.46 |
| 08 cta-endcard | 102.36 | 9.80 (no tail — final frame) |

Total composition length: 112.16s (~1:52) — the script's own 105s estimate
was pre-VO; real spoken pacing plus the CTA's frozen-grid hold lands here,
still well inside the faceless-explainer workflow's ~3-minute hard cap.
