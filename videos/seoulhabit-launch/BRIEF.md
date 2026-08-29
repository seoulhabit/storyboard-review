---
workflow: general-video
flow: automation
storyboard: no
message: "SeoulHabit does the K-beauty ingredient research for you and turns it into simple, bite-sized insights."
destination: reels
aspect: 1080x1920
language: en
audience: "K-beauty-curious social audience overwhelmed by ingredient lists — SeoulHabit's launch/follower audience"
length: 55.7s (was 60s; retimed 2026-08-29 for a faster narrator voice — see Notes)
angle: concept
---

## Intent

A 60-second faceless brand launch video introducing SeoulHabit as a
Korean-skincare ingredient research platform. Six fixed scenes, user-authored
VO (verbatim, do not reword — except the CTA line, revised 2026-08-29 per
client feedback, see Notes): hook (overwhelm at complex ingredient lists) →
solution (SeoulHabit reveal) → process (how it researches and simplifies) →
value (three quick answered-question callouts) → magic (confident close) →
CTA (subscribe). Kinetic typography and design-system components carry every
scene — no talking-head footage. Warm, confident, editorial — the SeoulHabit
Video Design System's established voice, not a generic ad read.

## Assets

- SeoulHabit Video Design System (claude.ai design project
  `75132ad8-b81c-4151-8a4c-83368df1d949`) — authoritative tokens/colors.css,
  tokens/motion.css, tokens/spacing.css, tokens/layout.css (--short-* 9:16
  lane), tokens/legibility.css, tokens/fonts.css, design-system-spec.md
  (canvas/type-scale/rules), component prompts (TextCallout, EndScreen,
  LowerThird, Logo) — transcribed into `assets/tokens/tokens.css`.
- `videos/red-ginseng-two-routes/` — HyperFrames scaffolding reference:
  root/scene structure, per-word kinetic-type scheduler (01-hook.html),
  습 SeoulHabit endcard lockup (06-endcard.html), audio rails.
  `assets/fonts/NotoSansKR-500-subset.woff2`, `assets/bgm/track.mp3`,
  `assets/sfx/*.mp3` copied verbatim.
- Voiceover: 6 narration lines generated via the connected creative-platform
  MCP (text2speech_v2/elevenlabs, one locked preset voice throughout) —
  `assets/voice/{01..06}.wav`.
- B-roll (2026-08-27, later pass): three muted background clips generated
  via the creative-platform MCP (`kling3_0_turbo`, 9:16, 720p) —
  `assets/broll/{01-hook,04-value,05-magic}.mp4`. No faces, no readable
  text/logos. See frame.md's "B-roll (frames 1, 4, 5)" section for the
  legibility treatment.
- Audio mix pass (2026-08-27, `/hyperframes-audio`): all six VO clips grouped
  into an `<hf-audio-group id="voiceover">` bus carrying a shared
  voice-warm-style chain (Remove Rumble → Add Weight → Even Out Loudness →
  Add Clarity → a stated-cost de-ess fallback → Peak Ceiling limiter), plus
  short fade-in/out automation on each clip and a dynamic voiceover carve on
  the BGM (`data-fx-carve` sourced against the `voiceover` group) so the bed
  ducks under narration. See frame.md's "Audio mix (2026-08-27)" section.
- Design-system reconciliation (2026-08-28): read the CURRENT state of the
  claude.ai design project (75132ad8-b81c-4151-8a4c-83368df1d949) live via
  `DesignSync`, not just the locally-transcribed `assets/tokens/tokens.css`.
  Found the earlier transcription was made against `design-system-spec.md`
  — a document explicitly labeled "proposal, awaiting sign-off... nothing
  implemented" — which the project has since superseded with real,
  different token values and sixteen built components. Reconciled the parts
  that matter for a HyperFrames (hand-written HTML/CSS, not React) build.
  See frame.md's "Design-system reconciliation (2026-08-28)" section for
  the full finding-by-finding record.
- Goal-alignment pass (2026-08-27): four elements named explicitly in the
  original goal script but missing from the built frames were added —
  Frame 1's "Wait, what is this?!" reaction callout, Frame 4's ink-bordered
  rotated stamp badge on the "Myth Busted!" plate (standing in for the
  script's "red stamp graphic" — gochujang is reserved for Frame 6, so this
  stays monochrome rather than doubling an accent color into a frame that
  already uses aqua), Frame 5's 3-item minimalist checklist ("Researched" /
  "Verified" / "Simplified", ticking off sequentially), and Frame 6's cursor
  that arrives and taps the Follow pill (renamed Subscribe 2026-08-29, see
  Notes) in sync with its existing emphasis
  beat, then clears before the frame's final held state. See frame.md's
  "Goal-alignment additions (2026-08-27)" section for exact timings.
- CTA voiceover re-recorded (2026-08-29, YouTube-optimization feedback):
  `assets/voice/06.wav` replaced — text changed from "Hit follow" to
  "Subscribe" (see Notes for the full rationale). Voice changed to
  **Kimberly** (a workspace reference voice, `voice_type: element`) for this
  one line only, per explicit user direction given mid-session — breaking
  from the other five lines' locked **Isla** preset (`text2speech_v2`/
  elevenlabs for both) *at the time this bullet was written*. A same-day
  follow-up request extended Kimberly to all six lines — see the "Voice
  change + full retime" bullet below; this entry is left intact as the
  historical record of the first, CTA-only step. The raw Kimberly take
  measured 8.6dB quieter than its Isla siblings (-19.19 LUFS vs. their
  -11.10 to -10.17 LUFS band, per the Audio mix pass above); two-pass
  loudness-matched (`ffmpeg loudnorm`, measured→apply) to -14.3 LUFS /
  -1.0 dBTP before placing — the -1.0 dBTP safety ceiling capped how far
  it could reach the sibling band without risking clipping, given the raw
  take's peak already sat at -0.97 dBTP. New duration 4.64s (was 5.76s);
  `data-duration` and the fade-in/out automation on `el-06-cta-voice`
  updated to match.
- BGM replaced (2026-08-29, YouTube-optimization feedback): see Notes for
  the full rationale. Sourced a fresh "modern lo-fi chill R&B instrumental"
  bed via `/media-use`'s HeyGen catalog retrieval
  (`audio/scripts/audio.mjs --only bgm`). The returned catalog clip was only
  15s; crossfade-looped (5×15s copies, 2s triangular crossfades via ffmpeg
  `acrossfade`) to 67s so it comfortably covers the 60s composition.
  `data-volume` kept at `0.12` (the audio engine's own bed-under-narration
  default, and the feedback's explicit "low-volume" ask). Voiceover carve
  re-run (`hyperframes-audio/scripts/carve.mjs`) against the new bed and the
  updated line 6 — new bands `160Hz -6dB / 250Hz -3.62dB / 1600Hz -5.16dB`,
  same `strength: 0.25`.

## Customizations

- Faceless kinetic-type build per the approved plan
  (`/Users/sumitchoudhary/.claude/plans/typed-exploring-sun.md`).
- B-roll added to frames 1, 4, 5 (2026-08-27) per the approved plan
  (`/Users/sumitchoudhary/.claude/plans/reflective-gliding-kurzweil.md`) —
  explicit user direction after the faceless-only cut had already rendered
  and shipped once. Scenes 2, 3, 6 unchanged. Timing, VO, BGM, and SFX are
  untouched.

## Notes

- `storyboard: no` — the approved plan already serves as the frame-by-frame
  storyboard; `STORYBOARD.md` still records one `## Frame N` block per scene
  as the build's dispatch record.
- Brand anchor is the 습 SeoulHabit text lockup (Noto Sans KR), not the
  design system's `assets/marks/brand/` SVG (Fold & Spark) — that mark's own
  README flags it as unconfirmed for SeoulHabit; explicitly excluded per
  user direction.
- Fixed 60.0s duration, 1080×1920, 30fps. Scene boundaries were set from
  measured real VO length per line (0, 9.5, 18.0, 30.0, 43.0, 52.5, 60.0),
  not the original avatar-driven plan's even split.
- **Pivoted mid-build from an avatar-led cut to fully faceless** (explicit
  user direction after the avatar version had already rendered once). All
  four avatar-carrying scenes (hook, solution, process, magic) were rebuilt
  as kinetic-type / design-system treatments; the avatar clips and their
  native-speech audio extracts were deleted and replaced with narrator VO
  for all six lines from one locked voice.
- **B-roll generation, two attempts (2026-08-27):** the first batch
  (`seedance_2_5`, 1080p) stalled at `in_progress` for ~19 minutes with no
  progress across five polls; the user chose to ship the faceless-only cut
  rather than keep waiting, and that render was delivered. A follow-up
  request to implement the design system prompted a retry, bounded to 5
  minutes, with a faster model (`kling3_0_turbo`, 720p) — all three clips
  completed within that window and were integrated as documented above.
  Re-rendered `renders/seoulhabit-launch_2026-08-27_21-42-38.mp4` (60.0s,
  1080×1920, 30fps) supersedes the earlier faceless-only render as current.
- CLI pin bumped 0.8.16 → 0.8.17 before this pass (`npm run check` verified
  clean on the new version before any composition edits).
- **Audio mix, real clipping caught and fixed (2026-08-27):** the first mix
  pass (VO bus with Add Weight/Add Clarity at +2.5dB each, compressor
  makeup +3dB, limiter ceiling -1dB) rendered with a genuine digital sample
  peak at +3.84 dBTP (confirmed via raw-PCM analysis, not just an
  inter-sample-peak estimate — the sample and true peak matched almost
  exactly, at t=36.4s in the value scene). The previous B-roll-only render
  had measured a safe -0.16 dBTP, so this was a regression introduced by
  the VO chain. Root cause: the limiter's default 5ms attack let a fast
  transient through before gain reduction engaged; lowering the ceiling
  alone (-1 → -6 → -10dB) barely moved the measured peak (0.54 → 0.53 dBTP),
  confirming the ceiling wasn't the limiting factor. Fix: limiter attack
  dropped to 0.1ms (near-instant), Add Weight/Add Clarity trimmed to
  +1.5dB each, compressor threshold tightened to -22dB. Final measured
  true peak: -3.33 dBTP (safely under the -1 dBTP delivery standard),
  integrated loudness -16.6 LUFS. Verified by extracting raw PCM and
  4x-oversampling (scipy `resample_poly`) rather than trusting a single
  summary number — `@hyperframes/core` was installed as a devDependency to
  run the skill's `carve.mjs` script for this pass.
  Re-rendered `renders/seoulhabit-launch_2026-08-27_22-11-21.mp4` (60.0s,
  1080×1920, 30fps) supersedes the B-roll-only render as current.
- **YouTube-optimization feedback pass (2026-08-29):** an external
  reviewer's five-point YouTube-specific note actioned end to end.
  Full per-item rationale is in `frame.md`'s "YouTube-optimization feedback
  pass (2026-08-29)" section; asset-level specifics (new VO take, new BGM
  track, re-run carve) are in this file's Assets section above. Summary:
  (1) CTA copy+voice "Hit follow"→"Subscribe" (on-screen pill and VO;
  VO voice deviates to Kimberly for this one line only, per explicit
  mid-session user direction — see Assets); (2) confirmed the existing
  1080×1920 format is already correct for YouTube Shorts, no composition
  change, just a publishing note (upload via the Shorts surface, not a
  standard 16:9 slot); (3) BGM swapped for a genre-matched lo-fi/chill R&B
  bed, same 0.12 volume; (4) Frame 3 typing sped up ~18%
  (`compositions/frames/03-process.html`'s `CHAR_DUR`); (5) Frame 1 chips
  scaled +50% (local override, design-system floor untouched) and
  `#hook-video` brightened via `hyperframes media-treatment` (measured
  correction, escalated once past the tool's first bounded suggestion after
  a snapshot showed it was imperceptible under the existing dark ground/
  scrim layers — see frame.md for the exact values and why). `npm run check`
  clean throughout (0 lint/runtime/layout/motion errors, 18/18 WCAG AA
  contrast, matching the pre-change baseline).
  **Audio re-verified post-render** (raw PCM, matching this project's
  established method): full mix -16.67 LUFS / -2.85 dBTP true peak (safely
  under the -1 dBTP standard, consistent with the -16.6 LUFS / -3.33 dBTP
  prior baseline — no clipping introduced by the new BGM bed or CTA take).
  BGM audibility during a narration gap (8.6-9.4s) measured -48.9dB RMS on
  the prior render vs. **-36.0dB RMS on this one** — a real ~13dB
  improvement, confirming the "dead silence" complaint was measurable and is
  now fixed rather than just reportedly fixed. CTA line 6 (Kimberly) reads
  -22.9dB RMS mid-sentence in the final mix vs. -20.1/-21.9dB for two Isla
  lines elsewhere — within normal per-take variation once through the
  shared VO bus, not a jarring level mismatch despite the raw 8.6dB gap.
  Re-rendered `renders/seoulhabit-launch_2026-08-29_04-59-18.mp4` (60.0s,
  1080×1920, 30fps) supersedes the 2026-08-27 22:11 render as current.
- **Voice change + full retime (2026-08-29, same day, explicit follow-up
  request):** "redo all six lines in Kimberly for consistency." Lines 1-5
  re-recorded (`assets/voice/{01..05}.wav`, `{01..05}-raw.mp3`) in
  Kimberly, verbatim text unchanged. All five raw takes measured -17.36 to
  -20.20 LUFS — confirming line 6's earlier -19.19 LUFS wasn't a fluke but
  a real characteristic of this voice — so all five (not just six) got the
  same two-pass peak-safe loudness match used for line 6
  (`I=-10.6:TP=-1.0`, dynamic); final six lines cluster tightly at -14.71
  to -13.82 LUFS, all ≤-0.97 dBTP.

  Kimberly reads 3.5-24% faster than Isla per line (new durations: 6.88 /
  5.28 / 8.72 / 9.52 / 6.96 / 4.64s, was 8.56 / 6.96 / 9.04 / 10.8 / 8.4 /
  5.76s) — flagged to the user before proceeding, since the fixed 60.0s
  cut's scene boundaries were originally set from Isla's measured pacing
  and would no longer fit. User chose "full retime" over "leave timing
  as-is" or "recut boundaries only" from three offered options. Full
  retiming mechanics, per-frame reasoning, and the new global structure (0
  / 7.5 / 14.0 / 25.7 / 38.7 / 46.7 / 55.7) are in `STORYBOARD.md`'s
  "Voice change + full retime" section — not duplicated here. Voiceover
  carve re-run against the fully changed track (bands now 1000/1600/2500Hz,
  strength unchanged at 0.25). `npm run check` clean (0 lint/runtime/
  layout/motion errors, 22/22 WCAG AA — up from 18/18, more text samples
  land in the new frame durations). Verified via snapshot at all 6 scene
  boundaries plus each scene's settled state (18 frames total) — no
  truncated animation anywhere, including the two frames flagged as risk
  during planning (Frame 1's chip-exit, now at local 7.0s, finishes with
  0.4s to spare in the new 8.0s scene; Frame 5's checklist, unchanged,
  finishes with ~1.0s to spare in the new 8.5s scene). Total duration
  55.7s (down from 60.0s) — not forced back to 60s, since doing that by
  padding the CTA hold alone would have produced a ~9s dead-static tail on
  the exact kind of over-lingering pacing this whole feedback pass was
  about fixing elsewhere.

  Re-rendered and re-verified (raw PCM): full mix -17.62 LUFS / -3.25 dBTP
  true peak (safely under the -1 dBTP standard). VO consistency check
  across all six lines (1s mid-sentence RMS sample per scene) landed at
  -20.5 / -20.3 / -20.8 / -23.2 / -21.9 / -22.5 dB — a ~2.9dB spread, and
  the first three within 0.5dB of each other, a real improvement in
  narrator consistency over the mixed Isla/Kimberly state (which had
  clips varying by up to ~9dB raw). BGM remains clearly audible at the new
  frame boundaries (-29.2dB RMS at the Frame 1→2 gap, vs. the original
  -48.9dB "dead silence" baseline). `renders/seoulhabit-launch_2026-08-29_05-24-17.mp4`
  (55.7s, 1080×1920, 30fps) supersedes the 04:59 same-day render as
  current.
