---
workflow: general-video
flow: automation
storyboard: no
message: "SeoulHabit does the K-beauty ingredient research for you and turns it into simple, bite-sized insights."
destination: reels
aspect: 1080x1920
language: en
audience: "K-beauty-curious social audience overwhelmed by ingredient lists — SeoulHabit's launch/follower audience"
length: 60s
angle: concept
---

## Intent

A 60-second faceless brand launch video introducing SeoulHabit as a
Korean-skincare ingredient research platform. Six fixed scenes, user-authored
VO (verbatim, do not reword): hook (overwhelm at complex ingredient lists) →
solution (SeoulHabit reveal) → process (how it researches and simplifies) →
value (three quick answered-question callouts) → magic (confident close) →
CTA (follow). Kinetic typography and design-system components carry every
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
  that arrives and taps the Follow pill in sync with its existing emphasis
  beat, then clears before the frame's final held state. See frame.md's
  "Goal-alignment additions (2026-08-27)" section for exact timings.

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
