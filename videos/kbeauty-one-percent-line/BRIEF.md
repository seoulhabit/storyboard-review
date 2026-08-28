---
workflow: faceless-explainer
flow: automation
storyboard: no
message: "K-beauty ingredient labels use two legal loopholes (the extract dilution and the 1% ordering rule) that make marketing hero-ingredients look bigger than they are — here's how to read past them."
destination: shorts
aspect: 1080x1920
language: en
audience: "K-beauty-curious skincare shoppers who read ingredient lists but don't know the 1% rule or Hanbang INCI names — general skincare/beauty YouTube Shorts audience"
length: 105s
angle: how-to
VO_MODE: verbatim
---

## Intent

A ~1:45 fast-paced "hyperframe" faceless explainer teaching viewers to
decode K-beauty ingredient labels: the extract-dilution loophole, the legal
1% ordering rule, a live label teardown, and a Hanbang (traditional Korean
herbal) INCI-to-common-name cheat sheet. User supplied a complete verbatim
A/V script (8 timed segments, SFX + VO columns) — used as-is, restructured
only where content accuracy required it (see `frame.md` § Content
corrections). Aggressive, high-energy, ~130 wpm pacing; a new kinetic beat
every ~2s (word pop, mask reveal, list scroll, card snap) per the user's own
hyperframe-editing brief.

## Assets

- SeoulHabit Video Design System — `assets/tokens/tokens.css` (copied
  verbatim from `videos/seoulhabit-launch/assets/tokens/tokens.css`, the
  local authoritative transcription), `assets/fonts/NotoSansKR-500-subset.woff2`.
- `videos/seoulhabit-launch/` — HyperFrames scaffolding + audio-mix
  reference (root/scene contract, VO bus chain, BGM carve).
- `videos/skincare-ingredient-glossary/` — reference for the JS-generated
  fast-card pattern and the "not sourced claims, not medical advice"
  disclaimer convention (this video ships the same disclaimer; it has no
  locked `ING-*` source record).
- Voiceover: 8 narration lines via the creative-platform MCP
  (text2speech_v2/elevenlabs), one locked custom voice, "Kimberly"
  (user-specified, voice_type element) — `assets/voice/{01..08}.wav`.
- SFX: sourced/generated per beat — `assets/sfx/`.
- BGM: one energetic instrumental bed — `assets/bgm/track.mp3`.

## Customizations

**User's literal visual brief (Montserrat/Impact, pitch-black + neon green
#39FF14 + alert red #FF3131, glow effects) is translated into SeoulHabit
Video Design System tokens, not used literally** — confirmed by the user
when asked directly. See `frame.md` § Design translation for the full
mapping. 9:16 vertical confirmed by the user over 16:9.

## Notes

No locked `ING-*` source record exists for this topic (general label-reading
literacy, not a single ingredient's evidence record) — ships the sanctioned
disclaimer instead of citation chips. The live teardown (Beauty of Joseon
Glow Serum) is fact-checked against the brand's actual published INCI list
during build; the on-screen list follows reality even where it differs from
the user's script draft (see `frame.md` § Content corrections).
