---
message: "SeoulHabit does the K-beauty ingredient research for you and turns it into simple, bite-sized insights."
audience: "K-beauty-curious social audience overwhelmed by ingredient lists"
mode: autonomous
format: 1080x1920
duration: 55.7s
---

Six frames, fixed script, fully faceless (no avatar/video footage — kinetic
typography and design-system components only, one locked narrator voice
throughout — **Kimberly**, all six lines, since 2026-08-29; see Notes).
Frames alternate `data-track-index` 0/1; each scene's clip runs 0.5s past
the next scene's start for a cross-fade overlap (except the final frame).
Boundaries are set from measured real VO length per line, not an even
split. **Retimed 2026-08-29** (55.7s total, was 60.0s) when the VO voice
changed to Kimberly, which reads noticeably faster than the original Isla
takes — see Notes for the retiming method. Design source: `frame.md`
(SeoulHabit Video Design System tokens, `assets/tokens/tokens.css`).

## Frame 1 — hook

- status: built
- src: compositions/frames/01-hook.html
- type: hook
- start: 0.0
- duration: 8.0 (visible 0.0–7.5, cross-fade tail to 8.0; retimed 2026-08-29,
  was 10.0/9.5 — see Notes)
- blueprint: kinetic-type-beats (Hook) — two-clause per-word headline over a
  dark ground, adapted from `red-ginseng-two-routes/01-hook.html`'s
  `dynamic-content-sequencing` scheduler
- rules: dynamic-content-sequencing, spring-pop-entrance (chip arrival),
  sine-wave-loop (chip idle drift)
- beat: Muted B-roll ground (`assets/broll/01-hook.mp4` — moody amber
  bottle/dropper macro, brightened 2026-08-29 via `hyperframes
  media-treatment`) under a two-edge Scrim (design system
  `--scrim-top`/`--scrim-bottom`) plus the original dark radial + grain,
  now semi-transparent. Three mono chips — `SNAIL MUCIN` /
  `CENTELLA ASIATICA` / `HEARTLEAF` — scaled +50% 2026-08-29 (mobile
  legibility feedback) — stagger in top-band, drift, then exit (now at
  local 7.0s, was 8.2s) before the cross-fade. Below them, a two-clause EB
  Garamond headline builds word-by-word: "Korean skincare is pure magic,
  but the ingredient lists? An advanced chemistry exam." VO (verbatim):
  "Korean skincare is pure magic, but let's be real, the ingredient lists
  can sometimes look like an advanced chemistry exam." (6.88s, Kimberly —
  was 8.56s/Isla)

## Frame 2 — solution

- status: built
- src: compositions/frames/02-solution.html
- type: branding
- start: 7.5
- duration: 7.0 (visible 7.5–14.0, cross-fade tail to 14.5; retimed
  2026-08-29, was 9.5/18.0/18.5 — see Notes)
- blueprint: titlecard-reveal (Product_Intro) — calm breather, ONE
  restrained slide-up-crossfade move, adapted from
  `red-ginseng-two-routes/06-endcard.html`
- rules: (blueprint's own signature move only)
- beat: Paper ground from t=0 (no avatar phase). The **습 SeoulHabit**
  lockup slides up + crossfades in at 0.35s, holds with a low-amplitude
  breath for the rest of the scene (breath loop trimmed from repeat:5 to
  repeat:3, 2026-08-29). Sub-line: "Your Korean skincare ingredient
  research platform." VO: "Enter SeoulHabit. We are your dedicated Korean
  skincare ingredient research platform." (5.28s, Kimberly — was 6.96s/Isla)

## Frame 3 — process

- status: built
- src: compositions/frames/03-process.html
- type: feature_showcase
- start: 14.0
- duration: 12.2 (visible 14.0–25.7, cross-fade tail to 26.2; retimed
  2026-08-29, was 18.0/30.0/30.5 — see Notes)
- blueprint: typewriter-reveal (composed) — a live caret types each query
  as a human would; full-frame, no split-screen (no avatar to share the
  frame with)
- rules: context-sensitive-cursor, dynamic-content-sequencing
- beat: Centered full-frame search interface: kicker "습 SeoulHabit ·
  Research", a large mist search bar, caret in `--aqua` (the frame's single
  accent). Caret types three queries sequentially: "what does snail mucin
  actually do?" → "centella vs cica — same thing?" → "heartleaf for
  redness?" — per-character reveal sped up ~18% 2026-08-29 (pacing
  feedback); each resolves into "→ simple, bite-sized insights" below. The
  whole block fades clear at local 11.3s (was local 11.3s, unchanged —
  still safely before the new local 11.7 visible-end) before the cross-fade
  into Frame 4 (avoids overlapping Frame 4's plate in the same vertical
  band). VO: "We take the most common questions you have about K-beauty
  ingredients, do the heavy research, and turn them into simple,
  bite-sized insights." (8.72s, Kimberly — was 9.04s/Isla)

## Frame 4 — value

- status: built
- src: compositions/frames/04-value.html
- type: benefit_highlight
- start: 25.7
- duration: 13.5 (visible 25.7–38.7, cross-fade tail to 39.2; start shifted
  2026-08-29 by the retime above — this frame's own 13.5s span is
  deliberately unchanged, since its three-plate relay has its own fixed
  internal schedule through local 13.5s, independent of VO length. See
  Notes.)
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
  trends are total myths? We answer all of it." (9.52s, Kimberly — was
  10.8s/Isla)

## Frame 5 — magic

- status: built
- src: compositions/frames/05-magic.html
- type: benefit_highlight
- start: 38.7
- duration: 8.5 (visible 38.7–46.7, cross-fade tail to 47.2; retimed
  2026-08-29, was 43.0/52.5/53.0 — see Notes)
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
  (6.96s, Kimberly — was 8.4s/Isla)

## Frame 6 — cta

- status: built
- src: compositions/frames/06-cta.html
- type: cta
- start: 46.7
- duration: 9.0 (visible 46.7–55.7, no cross-fade tail — final frame;
  retimed 2026-08-29, was 52.5/60.0 — see Notes. The lockup/pill/cursor
  beats stay at their original local timings — only the final held
  duration grew, from a 5.6s hold to a deliberately more generous 7.1s
  hold, matching this frame's existing "pause-and-study, never blank"
  design intent rather than the pacing complaint that drove the other
  frames' retiming.)
- blueprint: titlecard-reveal (CTA) — monochrome end-card, one restrained
  move, held to the final frame; adapted from
  `red-ginseng-two-routes/06-endcard.html`
- rules: spring-pop-entrance (Subscribe pill emphasis beat only)
- beat: EndCard on paper: "Build Your SeoulHabit." slides up + crossfades
  in at 0.3s with the compact **습 SeoulHabit** lockup beneath it; a
  **Subscribe** pill (renamed from Follow 2026-08-29, YouTube-native CTA
  language) in `--color-brand-accent` (gochujang — the frame's one
  voltage moment) pops with a 180ms scale 0.92→1 emphasis at 1.5s and
  holds — frame-zero-safe final state. VO: "Ready to truly understand your
  skin? Subscribe, and let's build your SeoulHabit." (4.64s, Kimberly —
  re-recorded 2026-08-29 — see BRIEF.md Assets/Notes)

## Audio

- BGM `assets/bgm/track.mp3` — modern lo-fi/chill R&B instrumental
  (replaced 2026-08-29, see BRIEF.md Notes; sourced via `/media-use`,
  crossfade-looped to 67s from a 15s catalog clip — still comfortably
  covers the retimed 55.7s composition), 0–55.7s, `data-volume="0.12"`
  (unchanged).
- VO: `assets/voice/{01..06}.wav`, one locked ElevenLabs voice
  (**Kimberly**, all six lines since 2026-08-29 — was Isla for lines 1-5,
  Kimberly for line 6 only, on the previous pass; see Notes) via
  `text2speech_v2`.
- SFX (track 20+, ~0.35 volume) — retimed 2026-08-29, each cue's offset
  *within its own scene* is unchanged, only the global clock shifted:
  0.0 glitch-3 (chip flurry) · 7.5 whoosh-short (into solution) · 8.5
  chime (logo settles) · 14.0/14.8/19.2/23.4 click-soft (search opens +
  each query begins typing) · 25.7 click-soft ("How to use?") · 30.0
  sparkle ("When to use?") · 34.3 impact-bass-1 ("Myth Busted!") · 38.7
  sparkle (magic begins) · 46.7 chime (CTA lockup).

## Build history

An earlier pass built this same script with HeyGen-style avatar footage
(Seedance 2.5 omni_reference clips, one locked creator identity) for
Frames 1/2/3/5, using the avatar's native lip-synced audio as VO for those
scenes and TTS only for Frames 4/6. That version rendered successfully
(60.0s) but was explicitly reversed mid-session in favor of this fully
faceless cut — the avatar clips, `assets/avatar/`, and the avatar-native
voice extracts were deleted; all six VO lines now come from one TTS voice.

## Voice change + full retime (2026-08-29)

Explicit user direction: re-record all six VO lines in **Kimberly**
(`voice_type: element`) for narrator consistency, after an earlier pass had
put only the Frame 6 CTA line in Kimberly (client feedback drove that
first change; the follow-up request extended it to the whole video). Text
is unchanged (verbatim) on all six lines.

Kimberly reads noticeably faster than the original Isla takes — every line
came back shorter (line 2 by 24%, line 1 by 20%, down to line 3's 3.5%) —
so the fixed 60.0s cut, whose scene boundaries were originally set from
Isla's measured pacing per line, no longer fit. Retimed from scratch:

- **Frames 1, 2, 5** (VO-paced kinetic type / title-card): each scene's
  outer duration shrunk to the new VO length plus that scene's own
  already-authored buffer (preserved as a ratio, not re-invented) — e.g.
  Frame 1's chip-exit point moved from local 8.2s to 7.0s so it still
  finishes with room to spare inside the new 8.0s scene. Entrance beats
  (chip pop-in, headline word timing, lockup fade) were left at their
  authored local times — only the flexible hold/exit tail was trimmed.
- **Frame 3** (typewriter sequence): outer duration recomputed the same
  way (VO + buffer), but its internal typing/result/clear schedule was
  never VO-length-driven in the first place (fixed local timings, already
  well inside the old buffer), so nothing internal needed to change.
- **Frame 4** (three-plate relay): deliberately **not** shrunk. Its plate
  schedule runs to a fixed local 13.5s regardless of VO length — that's
  now the binding constraint, not the (now much shorter) VO, which fits
  with far more room than before. Only its global start time moved.
- **Frame 6** (CTA end-card): kept its quick, fixed entrance beats
  (lockup 0.3s, pill tap 1.5s, cursor clear 1.9s) and grew its final hold
  moderately (9.0s total, was 7.5s) rather than mechanically via the same
  VO+buffer formula (which would have given only a marginal bump) or by
  dumping the full ~7.5s saved elsewhere in the cut onto it (which would
  have produced a ~9s dead-static tail — its own pacing problem). This
  frame's hold is deliberately generous by design already (see "Frame
  zero" in frame.md); the new hold is a considered middle point, not
  either formula's mechanical output.

New global structure: 0 / 7.5 / 14.0 / 25.7 / 38.7 / 46.7 / 55.7 (was 0 /
9.5 / 18.0 / 30.0 / 43.0 / 52.5 / 60.0). SFX cues moved with their owning
scene, preserving each cue's local offset exactly (verified — every cue
that was tied to a frame's own fixed internal schedule, e.g. Frame 3's
click-softs and Frame 4's sparkle/impact-bass hits, landed on the same
local time after the shift). Voiceover carve re-run against the fully
changed VO track. `npm run check`: 0 lint/runtime/layout/motion errors,
22/22 WCAG AA. Verified via snapshot at every scene boundary and settled
state across the new timeline — no truncated animation, no premature cuts.
Final duration 55.7s (was 60.0s) — shorter, driven honestly by the new
voice's faster pacing rather than forced back to a round number.
