---
message: "Snail mucin and Centella solve different problems — snail for glow, Centella for redness. 'Cica' is just Centella's K-beauty marketing name."
audience: "Skincare-curious viewers confused by K-beauty ingredient naming"
mode: autonomous
format: 1080x1920
duration: 30.280s (MEASURED — re-derived from index.html after the post-render review fix pass; see note)
---

**Timing below is measured, re-derived from `index.html`'s real `data-start`/
`data-duration` attributes** — it replaced an earlier pre-generation estimate
once the VO was generated, per `faceless-video-craft`'s re-timing cascade
section, the same discipline `glass-skin-5-habits` followed. It was
re-derived a second time after a post-render review pass extended Frame 5's
tail by 1.6s (28.680s → 30.280s total) to fix an abrupt ending — see Frame 5
below. Five frames, fixed script (two lines corrected for claim rigor — see
`frame.md` § Content corrections), fully faceless. All four boundaries
hard-cut (ground alternates paper/ink at every one — see `frame.md` § Motion).

## Frame 1 — hook

- status: shipped
- src: compositions/frames/01-hook.html
- type: hook
- start: 0.000
- duration (scene clip, measured): 5.260s
- ground: paper
- beat: Macro top-down glass palette — a watery, green-gold drop beside a
  thick, clear stretchy blob, both settled and visible at frame zero (the
  cold open, per the mandatory rule: never mid-fade). VO: "Snail mucin or
  Centella? If your skin is red and angry, stop guessing." SFX: soft
  glass-clink, curious chime.
- review fix: title stack nudged down (`top: var(--safe-top) + 130px`) — at
  the original `--safe-top` alone it sat inside YouTube Shorts' ~10% top UI
  zone (search/camera icons).

## Frame 2 — the snail texture

- status: shipped
- src: compositions/frames/02-string-test.html
- type: concept
- start: 5.260
- duration (scene clip, measured): 4.940s
- ground: ink
- beat: **Generated macro video** — two fingers tap-lift the snail-mucin
  blob, strands stretch, sag, and pinch off (the mandatory "string test," see
  `frame.md` § Media exception). Verdict rail's first row builds:
  `SNAIL → GLOW`, aqua accent. VO: "Snail mucin is incredible for deep
  hydration and that glass skin glow." SFX: sticky tack-tack (demuxed from
  the generated clip if usable, else channel fallback).
- review fix: verdict rail re-anchored `top: calc(--cap-band-top - 180px)`
  (was `bottom: 260px`) — the original placement sat inside YouTube Shorts'
  bottom ~20% UI zone (channel name, audio track, subscribe button). Rail
  scrim gradient re-tuned to keep contrast at the new position.

## Frame 3 — the centella texture

- status: shipped
- src: compositions/frames/03-dropper.html
- type: concept
- start: 10.200
- duration (scene clip, measured): 4.780s
- ground: paper
- beat: **Generated macro video** — a glass dropper dispenses a lightweight
  green-gold Centella ampoule onto the back of a hand (cropped at the
  wrist). Verdict rail's second row builds: `CENTELLA → CALM`, aqua accent.
  VO: "But for redness and stinging, Centella Asiatica is the better-studied
  pick." SFX: wet dispense/splash (demuxed if usable, else channel
  fallback).
- review fix: same rail re-anchor and scrim re-tune as Frame 2.

## Frame 4 — the twist

- status: shipped
- src: compositions/frames/04-twist.html
- type: concept
- start: 14.980
- duration (scene clip, measured): 5.660s
- ground: ink
- beat: A cream swipe passes over the reused Centella leaf plate, then the
  `.cta-chip-hb`-derived equivalence chip snaps in: `CICA = CENTELLA
  ASIATICA`, recolored **coral** — the video's one voltage moment, no aqua
  in this frame. A small mono qualifier chip carries the precision the VO no
  longer states: `"Cica" is a marketing word, not an INCI. Check the label.`
  VO (corrected): "Spoiler: K-beauty's Cica is just Centella — same plant,
  different label." SFX: cream-swoosh, reveal chime.
- review fix: the cream swipe (`#f4-cream`) was rebuilt full-bleed with
  feathered mask-image edges — the original hard-edged 45%/26% band only
  showed the flat top of its source image and read as a stray layer rather
  than an intentional wipe. Also given a `tl.set(..., 0)` seek baseline
  (the only element in the project hit by two tweens without one). Verdict
  rail re-anchored, same as Frames 2/3.

## Frame 5 — the CTA

- status: shipped
- src: compositions/frames/05-cta.html
- type: cta
- start: 20.640
- duration (scene clip, measured, post-fix): 9.640s (was 8.040s at first
  render — extended +1.6s by review fix, see below)
- ground: paper
- beat: Adapted SplitFaceProtocol bisector mechanism — left field snail
  (aqua-off, ink-weight), right field Centella (aqua on, the interrogated
  side), verdict rail now holds both completed rows beneath. 습 SeoulHabit
  lockup appears once, bottom-safe. Final held frame composition (paper
  ground, palette-adjacent framing) is the deliberate loop target back to
  Frame 1's cold open. VO: "So: Snail for glow. Centella for repair.
  Subscribe and let's simplify your skincare habits." SFX: chime-triple.
- review fix: the first render's Frame 5 was visually frozen from ~2.3s to
  its end (6.3s with zero pixel change outside captions) and the CTA landed
  with almost no time to register before the loop. Fixed three ways: (1)
  scene extended 8.040s → 9.640s; (2) a continuous Ken Burns
  (`.split-field img`, scale 1.0 → 1.045 across the whole scene) replaces the
  frozen hold; (3) the final caption group now releases at ~27.96s instead
  of holding through the whole tail (`compositions/captions.html`), leaving
  a clean ~2.3s CTA-only window before the loop point.
