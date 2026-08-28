---
message: "SeoulHabit does the K-beauty ingredient research for you and turns it into simple, bite-sized insights."
audience: "K-beauty-curious social audience overwhelmed by ingredient lists"
mode: autonomous
format: 1080x1920
duration: 60s
---

Six frames, fixed script, exactly 60.0s, fully faceless (no avatar/video
footage — kinetic typography and design-system components only, one locked
narrator voice throughout). Frames alternate `data-track-index` 0/1; each
scene's clip runs 0.5s past the next scene's start for a cross-fade overlap
(except the final frame). Boundaries are set from measured real VO length
per line, not an even split. Design source: `frame.md` (SeoulHabit Video
Design System tokens, `assets/tokens/tokens.css`).

## Frame 1 — hook

- status: built
- src: compositions/frames/01-hook.html
- type: hook
- start: 0.0
- duration: 10.0 (visible 0.0–9.5, cross-fade tail to 10.0)
- blueprint: kinetic-type-beats (Hook) — two-clause per-word headline over a
  dark ground, adapted from `red-ginseng-two-routes/01-hook.html`'s
  `dynamic-content-sequencing` scheduler
- rules: dynamic-content-sequencing, spring-pop-entrance (chip arrival),
  sine-wave-loop (chip idle drift)
- beat: Muted B-roll ground (`assets/broll/01-hook.mp4` — moody amber
  bottle/dropper macro) under a two-edge Scrim (design system
  `--scrim-top`/`--scrim-bottom`) plus the original dark radial + grain,
  now semi-transparent. Three mono chips — `SNAIL MUCIN` /
  `CENTELLA ASIATICA` / `HEARTLEAF` — stagger in top-band, drift, then exit
  before the cross-fade. Below them, a two-clause EB Garamond headline
  builds word-by-word: "Korean skincare is pure magic, but the ingredient
  lists? An advanced chemistry exam." VO (verbatim):
  "Korean skincare is pure magic, but let's be real, the ingredient lists
  can sometimes look like an advanced chemistry exam." (8.56s)

## Frame 2 — solution

- status: built
- src: compositions/frames/02-solution.html
- type: branding
- start: 9.5
- duration: 9.0 (visible 9.5–18.0, cross-fade tail to 18.5)
- blueprint: titlecard-reveal (Product_Intro) — calm breather, ONE
  restrained slide-up-crossfade move, adapted from
  `red-ginseng-two-routes/06-endcard.html`
- rules: (blueprint's own signature move only)
- beat: Paper ground from t=0 (no avatar phase). The **습 SeoulHabit**
  lockup slides up + crossfades in at 0.35s, holds with a low-amplitude
  breath for the rest of the scene. Sub-line: "Your Korean skincare
  ingredient research platform." VO: "Enter SeoulHabit. We are your
  dedicated Korean skincare ingredient research platform." (6.96s)

## Frame 3 — process

- status: built
- src: compositions/frames/03-process.html
- type: feature_showcase
- start: 18.0
- duration: 12.5 (visible 18.0–30.0, cross-fade tail to 30.5)
- blueprint: typewriter-reveal (composed) — a live caret types each query
  as a human would; full-frame, no split-screen (no avatar to share the
  frame with)
- rules: context-sensitive-cursor, dynamic-content-sequencing
- beat: Centered full-frame search interface: kicker "습 SeoulHabit ·
  Research", a large mist search bar, caret in `--aqua` (the frame's single
  accent). Caret types three queries sequentially: "what does snail mucin
  actually do?" → "centella vs cica — same thing?" → "heartleaf for
  redness?"; each resolves into "→ simple, bite-sized insights" below. The
  whole block fades clear before the cross-fade into Frame 4 (avoids
  overlapping Frame 4's plate in the same vertical band). VO: "We take the
  most common questions you have about K-beauty ingredients, do the heavy
  research, and turn them into simple, bite-sized insights." (9.04s)

## Frame 4 — value

- status: built
- src: compositions/frames/04-value.html
- type: benefit_highlight
- start: 30.0
- duration: 13.5 (visible 30.0–43.0, cross-fade tail to 43.5)
- blueprint: kinetic-type-beats (Benefits) — 3-statement relay, composed as
  TextCallout plates per the design system's `TextCallout.prompt.md`
- rules: dynamic-content-sequencing, spring-pop-entrance
- beat: Muted B-roll ground (`assets/broll/04-value.mp4` — slow-motion
  serum-drop-into-pool macro) under a flat 62% paper wash (composed from
  `--paper`, not a source-design-system token — see frame.md). Three
  sequential TextCallout plates (0–3.9s / 4.3–8.2s / 8.6–13.5s local), one
  on screen at a time, opaque `--mist` card + `--elev-2` elevation, `--aqua`
  highlighter on the interrogated phrase: "How to use?" / Mugwort · barrier
  support — "When to use?" / Niacinamide · AM or PM — "Myth Busted!" /
  viral trends, checked. VO: "Want to know exactly how Mugwort helps your
  barrier? When you should actually apply Niacinamide? Or which viral
  trends are total myths? We answer all of it." (10.8s)

## Frame 5 — magic

- status: built
- src: compositions/frames/05-magic.html
- type: benefit_highlight
- start: 43.0
- duration: 10.0 (visible 43.0–52.5, cross-fade tail to 53.0)
- blueprint: kinetic-type-beats (composed) — two-clause per-word headline
  on paper, mirroring Frame 1's engine but light-ground for the tonal
  shift into the close
- rules: dynamic-content-sequencing
- beat: Muted B-roll ground (`assets/broll/05-magic.mp4` — dewy gel-texture
  macro) under a graduated paper wash (composed from `--paper`, mirroring
  `--scrim-bottom`'s gradient shape — see frame.md) plus the original grain.
  EB Garamond two-clause headline builds word-by-word:
  "We bust the myths and uncover the **science.**" (aqua accent, the
  frame's one interrogated word) / "Skincare, made effortless." VO: "We
  bust the myths and uncover the science, making it effortless to
  incorporate the magic of these ingredients into your daily routine."
  (8.4s)

## Frame 6 — cta

- status: built
- src: compositions/frames/06-cta.html
- type: cta
- start: 52.5
- duration: 7.5 (visible 52.5–60.0, no cross-fade tail — final frame)
- blueprint: titlecard-reveal (CTA) — monochrome end-card, one restrained
  move, held to the final frame; adapted from
  `red-ginseng-two-routes/06-endcard.html`
- rules: spring-pop-entrance (Follow pill emphasis beat only)
- beat: EndCard on paper: "Build Your SeoulHabit." slides up + crossfades
  in at 0.3s with the compact **습 SeoulHabit** lockup beneath it; a
  **Follow** pill in `--color-brand-accent` (gochujang — the frame's one
  voltage moment) pops with a 180ms scale 0.92→1 emphasis at 1.5s and
  holds — frame-zero-safe final state. VO: "Ready to truly understand your
  skin? Hit follow, and let's build your SeoulHabit." (5.76s)

## Audio

- BGM `assets/bgm/track.mp3`, 0–60s, `data-volume="0.12"`.
- VO: `assets/voice/{01..06}.wav`, one locked ElevenLabs preset voice
  (Isla) across all six lines via `text2speech_v2`.
- SFX (track 20+, ~0.35 volume): 0.0 glitch-3 (chip flurry) · 9.5
  whoosh-short (into solution) · 10.5 chime (logo settles) · 18.0/18.8/
  23.2/27.4 click-soft (search opens + each query begins typing) · 30.0
  click-soft ("How to use?") · 34.3 sparkle ("When to use?") · 38.6
  impact-bass-1 ("Myth Busted!") · 43.0 sparkle (magic begins) · 52.5
  chime (CTA lockup).

## Build history

An earlier pass built this same script with HeyGen-style avatar footage
(Seedance 2.5 omni_reference clips, one locked creator identity) for
Frames 1/2/3/5, using the avatar's native lip-synced audio as VO for those
scenes and TTS only for Frames 4/6. That version rendered successfully
(60.0s) but was explicitly reversed mid-session in favor of this fully
faceless cut — the avatar clips, `assets/avatar/`, and the avatar-native
voice extracts were deleted; all six VO lines now come from one TTS voice.
