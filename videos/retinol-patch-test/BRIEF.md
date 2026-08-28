---
workflow: faceless-explainer
flow: automation
storyboard: no
message: "Patch test retinol behind your ear or jawline before your face — wait 48 hours, and stop at the first sign of a bad reaction."
destination: shorts
aspect: 1080x1920
language: en
audience: "skincare beginners who just bought their first retinol"
length: 55s
angle: how-to
VO_MODE: adapted
style_preset: seoulhabit
---

## Intent

The user handed in a creator-style, on-camera storyboard (six timed segments,
person holding the serum, pointing to their jawline, etc.) for a retinol
patch-testing how-to. Per the established SeoulHabit precedent
(`videos/kbeauty-one-percent-line`, `videos/seoulhabit-launch`), this is adapted
to a faceless motion-graphics build rather than shot on camera — the original is
preserved verbatim in `user_script.txt`. Vibe: cautious but encouraging,
educational, aesthetic — never alarmist. Six scenes, one VO line each, ~9s per
scene, timed from measured TTS.

## Assets

None supplied by the user. Scene 2's original photo hero
(`catalog/ingredient-photography/16-retinol.png`) was dropped — that asset
isn't checked into git — in favor of the checked-in glossary's own generic
ingredient icon (see `frame.md` § Provenance validation).

## Customizations

- Design system: tokens inlined per file, copied from the checked-in
  `videos/skincare-glossary-part-4-texture-anti-aging/index.html` (verified
  via `git ls-files` — see `frame.md` § Provenance validation, 2026-08-28).
  Noto Sans KR self-hosted font sourced from that same tracked project. Plain
  `<audio data-volume>` wiring, matching the tracked
  `videos/red-ginseng-two-routes/index.html` — no voiceover-bus/fx-chain
  machinery (that only ever existed in uncommitted sibling projects).
- Voice continuity: reuse HeyGen voice id `05f19352e8f74b0392a8f411eba40de1`,
  confirmed in the tracked `videos/red-ginseng-two-routes/audio_engine_meta.json`.
- Coral discipline: exactly one "voltage moment" — the Scene 5 "STOP — wash it
  off" symptom branch. The hook's "Stop!" is carried by ink strikethrough +
  highlighter instead, so coral isn't spent twice.
- On-screen text beats to preserve from the user's script: "Retinol = Powerful"
  (Scene 2), "Wait 48 Hours" (Scene 5), "seoulhabit.com" (Scene 6).

## Notes

- No `ING-*` evidence record exists for patch-testing in this pipeline, so no
  citation chips are used anywhere. The outro instead carries the sanctioned
  disclaimer microcopy: "General patch-testing guide — not sourced claims, not
  medical advice" (pattern from `videos/kbeauty-one-percent-line/frame.md`).
- One rigor edit to the user's script: Scene 3's line "This mimics the skin on
  your face perfectly" is an unsourced overclaim and is softened to "...the
  spots that behave most like the skin on your face." All other lines are kept
  faithful to the user's wording.
- Fold & Spark logo is banned from SeoulHabit videos; the outro uses the
  "습 SeoulHabit" Noto Sans KR text lockup instead (see
  `videos/seoulhabit-launch/frame.md` § Brand anchor).
- Run executed autonomously from an already-approved plan (no live-board review
  loop) — `storyboard: no`. `STORYBOARD.md` is still authored as the project's
  frame-by-frame plan document; it's the deliverable of Setup, not a review gate.
