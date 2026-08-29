# frame.md — SeoulHabit Launch Video

Design source: the **SeoulHabit Video Design System**
(claude.ai design project `75132ad8-b81c-4151-8a4c-83368df1d949`). Tokens are
transcribed verbatim into `assets/tokens/tokens.css` — every frame links that
file and uses its custom properties only. Do not hardcode a hex, px, or
easing curve that has a token.

## Canvas

1080×1920, 30fps. Safe areas (the design system's `--short-*` 9:16 lane):
`--safe-top 120px` / `--safe-bottom 360px` (caption band) / `--safe-left
60px` / `--safe-right 162px`. Keep all primary content inside them.

## Palette

`--paper` (#F7F5F0) ground · `--ink` (#131516) primary text · `--mist`
raised surface · `--aqua` (#59B8AE) the single interrogated-element accent —
**exactly one aqua-family highlight per frame** · `--coral`/`--color-brand-accent`
(gochujang, #C97A5C) the "one voltage moment" — reserved for the Frame 6
Subscribe pill (renamed from Follow 2026-08-29, see Notes below — same
component, same color role), never doubled up with aqua in the same frame · `--electric-blue`/
`--brand-mark` reserved for brand-mark moments only, not used as a generic
accent · `--leaf`/`--moss`/`--celadon` the confirmed-state ramp (not used in
this video — no evidence-meter content) · **no success color** rule carries
over even though this video makes no evidence claims.

## Type

`--font-display` (EB Garamond) for headlines/lockup titles · `--font-body`
(Inter, falls through to the self-hosted Noto Sans KR for Hangul) for body
copy · `--font-mono` (JetBrains Mono) for chips, labels, the search-bar
query text · `--font-kr` for `습 SeoulHabit`. Scale (this project's own
1080-wide tokens, see `assets/tokens/tokens.css`): `--t-hero 96` /
`--t-figure 60` / `--t-frame 50` / `--t-body 32` / `--t-caption 24` /
`--t-label 20` / `--t-chip 18` (floor — never smaller). EB Garamond, Inter,
and JetBrains Mono are referenced by family name only (no `@import`) — they
are in HyperFrames' pre-bundled font set, same as `red-ginseng-two-routes`.
Noto Sans KR is self-hosted (`assets/fonts/NotoSansKR-500-subset.woff2`,
`@font-face` in `tokens.css`).

## Motion

Only the two named SceneTransitions between frames — **cross-fade**
(`--e-inout`, 0.5s) and **punch-through** is available but this video uses
cross-fade at every boundary (no scene calls for the more aggressive scale-
blur punch). Within a frame: `--e-out`/`--e-in`/`--e-inout`, durations
`--d-snap 180 / --d-fast 400 / --d-base 500 / --d-fill 600`, staggers
`--stagger-line 80 / --stagger-node 120 / --stagger-step 220`, travel
`--travel-in 48px`. No bounce/elastic/back easing. No infinite keyframes —
idle motion (chip drift, endcard breath) is a finite sine yoyo with a
bounded repeat, resolving to rest at the frame's last authored beat.

## Elevation

`--elev-1` hairline seat, `--elev-2` lift (TextCallout plates). No glow —
`filter: drop-shadow(0 0 …)` and `box-shadow: 0 0 …` are banned outright.

## Faceless (no talking-head footage)

No avatar or talking-head footage anywhere — the ban that was reversed
mid-build (see Build history) still stands: do not reintroduce a
lip-synced/native-speech `<video>` element or an `assets/avatar/` directory.
Frames 1, 4, and 5 (2026-08-27, later pass) carry non-human B-roll — product
macros and texture footage, muted `<video>` under the existing kinetic type —
added by explicit user direction after the original faceless render had
already shipped once. Frames 1 and 5 still run the per-word kinetic-type
scheduler (adapted from
`red-ginseng-two-routes/compositions/frames/01-hook.html`'s
`dynamic-content-sequencing` pattern), now on video grounds instead of flat
dark/paper ones; Frame 3 is unchanged (full-frame search interface,
typewriter reveal); Frames 2, 4, 6 are the EndCard / TextCallout / EndCard
treatments, Frame 4 also now backed by video.

### B-roll (frames 1, 4, 5)

Generated via the creative-platform MCP, `kling3_0_turbo`, 9:16, 720p,
`assets/broll/{01-hook,04-value,05-magic}.mp4` — moody amber-bottle macro,
slow-motion serum-drop-into-pool macro, and dewy gel-texture macro
respectively. No faces, no readable text/logos in any clip (per prompt and
visual spot-check). Muted in the DOM per the framework's video rule; no
generated audio track is used — VO/BGM/SFX stay exactly as authored.

Legibility treatment, composed from the SeoulHabit Video Design System
(claude.ai design project `75132ad8-b81c-4151-8a4c-83368df1d949`,
`components/foundation/Scrim.jsx` + `tokens/legibility.css`):

- **Frame 1** — the system's actual `--scrim-top` / `--scrim-bottom` tokens,
  applied as two edge scrims (top band behind the ingredient chips, bottom
  band behind the headline) rather than one flat wash, so the footage reads
  clearly through the middle of frame. This is a direct, unmodified use of
  the canonical Scrim primitive — it was authored for exactly this case
  (white/light text over unpredictable footage).
- **Frames 4 & 5** — the design system has no inverse primitive for
  dark-ink-on-paper text over footage (its Scrim/legibility tokens are all
  ink-toned, built for the avatar-footage case). Composed a paper-toned wash
  from the existing `--paper` token instead: Frame 4 is a flat 62% wash
  behind the whole frame (the value-plate copy already sits on an opaque
  `--mist` card, so this only keeps the visible margins on-brand); Frame 5
  is a graduated wash mirroring `--scrim-bottom`'s gradient shape/floor logic
  but built from `--paper`, since its headline sits directly on paper with
  no card underneath. Neither is a new named design-system token — both are
  documented, bounded, source-consistent extensions of the one that exists.
  `npm run check` contrast pass: 18/18 WCAG AA after this treatment.

## Brand anchor

The **습 SeoulHabit** text lockup (Noto Sans KR 500, from
`red-ginseng-two-routes/compositions/frames/06-endcard.html`), not the
design system's `assets/marks/brand/logo-primary.svg` ("Fold & Spark") —
that mark's own README flags it unconfirmed for SeoulHabit. Do not use it
anywhere in this project.

## Audio mix (2026-08-27)

All six VO clips (`assets/voice/{01..06}.wav`) carry `data-audio-group="voiceover"`
and are summed onto an `<hf-audio-group id="voiceover">` bus in `index.html`,
per `/hyperframes-audio`. Content/takes are untouched — this is mix/polish only.

- **Shared chain** (voice-warm-style): highpass 90Hz (Remove Rumble) → peaking
  150Hz +1.5dB (Add Weight) → compressor threshold -22dB ratio 3 makeup +2dB
  (Even Out Loudness) → peaking 3000Hz +1.5dB (Add Clarity) → peaking 6500Hz
  -4dB Q3.5 (De-ess — a stated-cost fallback; no true de-esser is shipped by
  the skill) → limiter -10dB ceiling, 0.1ms attack (Peak Ceiling).
- **Fades**: each clip has an 80ms fade-in/out via `data-automation` on
  `volume`, so no boundary click.
- **BGM duck**: `el-bgm` carries `data-fx-carve` with `sources:["voiceover"]`
  — the group id, not six individual clip ids (the CLI's `--voice` flag
  needed clip ids to run the analysis, but the tool recognized the shared
  `data-audio-group` and wrote the group form on its own) — `strength: 0.25`,
  written by `hyperframes-audio`'s `carve.mjs`: a dynamic spectral duck
  (peaking cuts at 160/250/1600Hz plus a level-match gain) that follows the
  speech.
- **Per-clip loudness measured before mixing**: all six raw clips sat within
  ~1dB of each other (-11.10 to -10.17 LUFS) — already consistent from the
  single locked TTS voice, so no individual per-clip gain trim was needed
  beyond the shared bus treatment.
- **Clipping found and fixed**: the first version of this chain (stronger
  boosts, slower limiter attack) produced a genuine +3.84 dBTP digital peak
  at the value scene — see BRIEF.md's Notes for the full diagnosis. Final
  chain (above) measures -3.33 dBTP. Verify any future change to this chain
  by extracting raw PCM and checking true peak directly (sample-peak tools
  alone can miss it) — sample and true peak matched exactly here, so this
  was real clipping, not an inter-sample-peak artifact.

## Goal-alignment additions (2026-08-27)

The original goal script named several concrete visual beats that the built
frames (design-system components, adapted rather than shot-for-shot) didn't
carry. Closed four of them, additively, without touching audio, timing, or
the other frames:

- **Frame 1** — `#hook-reaction` ("Wait, what is this?!") pops in the gap
  between the two headline clauses (1.95–2.95s local) in `--aqua` mono type,
  positioned between the chip band and the headline zone. Clears before
  clause 2 begins at 3.0s.
- **Frame 4** — `.val-eyebrow--stamp` turns the "Myth Busted!" eyebrow on the
  third plate into an ink-bordered, rotated (-6deg) badge with a "thump"
  entrance (oversized start settling on `power3.out` — no bounce/elastic
  easing per house rule) at 8.85s local. Monochrome by design: gochujang is
  reserved for Frame 6, and this frame's one accent (`--aqua`) is already
  spent on "Viral trends."
- **Frame 5** — `.magic-checklist`, three rows ("Researched" / "Verified" /
  "Simplified") in ink-on-paper, each with a filled ink circle + paper
  checkmark that pops in shortly after its row slides in. Starts 5.6s local
  (after the headline settles), rows staggered 0.7s apart, holds to the
  frame's end.
- **Frame 6** — `#cta-cursor`, a small ink dot that travels in and taps the
  Subscribe pill (named Follow at the time this beat was authored; renamed
  2026-08-29, see Notes) exactly at 1.5s (matching the pill's own existing
  emphasis beat), then clears by 2.15s so the frame's final held state stays
  frame-zero-safe with no cursor on screen.

## Design-system reconciliation (2026-08-28)

Read the SeoulHabit Video Design System's CURRENT state live via `DesignSync`
against the same claude.ai project id this build's tokens were originally
transcribed from — not from memory of the earlier transcription. Findings:

- **The source had moved on.** `assets/tokens/tokens.css`'s header claimed
  values from `design-system-spec.md` §2.2 — but that file opens "Part 2 —
  Design system spec (proposal, awaiting sign-off)... Nothing here has been
  implemented." The project has since built past that proposal: real
  `tokens/*.css`, sixteen real components (`.jsx`+`.d.ts`+`.prompt.md`),
  `guidelines/*.card.html` reference cards, a `readme.md`, and `SKILL.md`.
  That current state is the real source of truth now, not the proposal doc.
- **Type scale was stale below the floor.** The real scale
  (`guidelines/type-scale.card.html`, matches `tokens/typography.css`
  exactly) sets `--t-label: 24px` ("data label, kicker"), `--t-chip: 22px`
  ("source chip, citation"), and an explicit `--t-floor: 20px` — "absolute
  floor, nothing smaller ships." This build had shipped 18px chips (Frame 1)
  and 20–22px labels (Frames 3/4) — under the real floor or short of the
  named role size. Bumped: Frame 1 chips 18→22px, Frame 3 label 22→24px,
  Frame 4 label 20→24px, `tokens.css` to match. (This independently
  confirms the same gap the earlier "check against the YouTube standard"
  pass found from the outside.)
- **Canvas primacy is an open question in the source system itself** — its
  own `readme.md` flags: "16:9 is treated as primary here on the strength
  of this brief... every shipped video in the repo is 9:16... if the
  channel is Shorts-first, the ratios swap and the type scale comes down."
  There is no confirmed 9:16-specific scale yet. So the larger display
  roles (`--t-hero`/`--t-figure`/`--t-frame`, 58–96px) were left as this
  project's own calibration from the system's named reference
  implementation (`red-ginseng-two-routes`) rather than force-derived by
  scaling the 1920-canvas numbers — `design-system-spec.md` itself warns
  scaling doesn't work ("each component needs an explicit layout variant;
  none can be derived by scaling"), and proportional scaling would in fact
  push `--t-body` under the floor.
- **Font-family naming.** The real `tokens/fonts.css` names the self-hosted
  Hangul face `"Noto Sans KR Video"` (with plain `"Noto Sans KR"` as a
  fallback for a CDN-loaded copy). This build's `@font-face` declared only
  `"Noto Sans KR"`. Added a second identical `@font-face` under the real
  name in every frame that references Korean type, and led the font stacks
  with it — both names now resolve locally, no CDN dependency either way.
- **Color token naming.** Frame 6 invented a local `--gochujang` variable.
  The real system's name for that role is `--color-brand-accent`
  (`tokens/colors.css`'s video-editor semantic layer), same hex (`#C97A5C`).
  Renamed. **Flagged, not silently resolved:** the system's `readme.md`
  defines core-palette coral's role narrowly — "marks a limitation or a
  refusal" — which doesn't describe a Follow-button active state. Kept the
  color via the semantic layer's own broader reading ("primary marks,
  active states, limit callouts"), documented in both `tokens.css` and
  `06-cta.html` rather than either silently keeping or silently changing it.
- **TextCallout and Scrim were already well-aligned**, verified against the
  real specs: TextCallout's rule ("aqua highlighter... one highlight per
  frame, on the phrase being interrogated") matches Frame 4's plates
  exactly. The hand-written B-roll scrim gradients in Frames 1/4/5 matched
  `tokens/legibility.css`'s `--scrim-bottom`/`--scrim-top` byte-for-byte.
- **EndScreen does not apply to this video and was never really "used."**
  The real `EndScreen` component is YouTube-16:9-specific — pixel-exact
  boxes reserved for YouTube's own subscribe circle and video cards
  (`560×315` at fixed coordinates), held 15s. This project is 9:16 Shorts;
  Frame 6 actually followed the informal "EndCard" pattern from
  `red-ginseng-two-routes/06-endcard.html` (which the system's own
  `catalog.md` calls a not-yet-formalized "candidate" component), not the
  real EndScreen. Corrected the record — earlier notes conflated the two.
- **Logo (SH monogram) exists and was not adopted — a separate finding from
  the earlier Fold & Spark exclusion.** `components/brand/Logo.jsx` is a
  declared placeholder: "SH" in self-hosted Montserrat ExtraBold, electric
  blue `#0B6BF5`, explicitly "not a delivered brand mark." This is a
  different object from the previously-excluded `assets/marks/brand/`
  SVG ("Fold & Spark"). Flagging rather than adopting: introducing an
  actual new brand mark into a finished, delivered video is a creative
  decision beyond a token/spec-alignment pass.
- **The checklist's checkmark glyph has no compliant equivalent in the real
  system.** The real icon set is 17 Lucide SVGs (`assets/icons/`), and the
  system's content rules say "Unicode as icon: only `·` `–` `✕`" — no
  checkmark. `RoutineChecklist` is named in the taxonomy but not built.
  Frame 5's ✓-in-a-circle (added in the prior goal-alignment pass, per
  explicit user direction to add a checklist graphic) is a documented,
  deliberate off-system improvisation, not a system component — left as-is
  since no compliant alternative exists and removing it would undo that
  explicit direction.
- **Not changed:** motion timings/easings (already power2/power3 only, no
  bounce/elastic/back, matching `guidelines/motion-grammar.card.html`'s
  banned list), elevation/shadow values, spacing/radii, the B-roll scrim
  treatment, and the chip's `border-radius: 999px` (pill chips are an
  established pattern in the system's own reference video and `--r-pill`
  is itself a real token — the "no pill on a data node" rule targets data
  nodes specifically, not ingredient-name chips).

## Frame zero

Frame 6 (the final frame) is the dense pause-and-study state: EndCard
lockup + Subscribe pill fully settled, no motion in progress. Never blank,
never mid-fade.

## YouTube-optimization feedback pass (2026-08-29)

Five client notes, actioned:

- **CTA copy.** "Hit follow" read as TikTok/Instagram-native; YouTube viewers
  are primed for "Subscribe." Renamed the Frame 6 pill (`#cta-pill`, was
  "Follow") and re-recorded its VO line to match — see BRIEF.md's Assets
  section for the voiceover-swap details (this pass put only the Frame 6
  line in a different voice, "Kimberly"; a same-day follow-up request
  extended that to all six lines for narrator consistency, which also
  forced a full retime — see the "Voice change + full retime" note below
  and STORYBOARD.md's matching section for the mechanics).
- **Publishing format.** Already 1080×1920 (9:16) — correct for YouTube
  Shorts as delivered. No composition change; this must be uploaded via
  YouTube's Shorts surface specifically, not as a standard 16:9 video (which
  would letterbox).
- **BGM.** The `red-ginseng-two-routes` track this video inherited (see
  Assets, original build) was never genre-matched to this video and read as
  near-silent at 0.12 volume. Replaced with a freshly sourced "modern lo-fi
  chill R&B instrumental" bed (`/media-use`, HeyGen catalog retrieval) —
  full detail in BRIEF.md's Assets section. `data-volume` unchanged at 0.12
  (the "low-volume" ask, and the audio engine's own bed-under-narration
  default) — the fix was the track itself, not its level. Voiceover carve
  re-run against the new bed.
- **Frame 3 typing pace.** `CHAR_DUR` 0.045 → 0.037 (≈18% faster per-character
  reveal) in `compositions/frames/03-process.html`. `TYPE_START` and the
  result-label/SFX cue timings were left untouched — the feedback named the
  typing animation specifically, and touching the query-start beats would
  have meant re-syncing the `click-soft` SFX cues in `index.html` for a
  scope the feedback didn't ask for.
- **Frame 1 hook.** Two independent fixes:
  - Ingredient chips: `--t-chip` 22px → 33px (+50%) and `.hook-chip` padding
    10px/18px → 15px/27px, scaled proportionally. This is a **local override
    inside `01-hook.html` only** — the shared design-system floor recorded in
    `assets/tokens/tokens.css` (22px, from the 2026-08-28 reconciliation
    pass) is untouched. Chips now wrap to two rows at this frame's content
    width; verified via snapshot, still holds inside the `--safe-top`
    chip band and `npm run check`'s 18/18 WCAG AA contrast pass.
  - Brightness: measured `#hook-video` via
    `hyperframes media-treatment --analyze` (yAvg 70/255, no clipping risk,
    yMax already at 238 — a highlight near the dropper glass close to
    ceiling). The tool's own bounded auto-suggestion (exposure +0.054) was
    visually imperceptible once composited under the existing dark
    `.hook-ground` gradient and the two Scrim layers, so escalated within
    the same correction lane to a shadows-focused lift — `exposure 0.15,
    shadows 0.3, blacks 0.05, contrast 0.06, temperature -0.02` — applied via
    `hyperframes media-treatment --apply` (not a hand-rolled CSS filter).
    Confirmed clearly brighter via before/after snapshots without blowing
    the existing near-ceiling highlight or touching the Scrim primitives'
    own legibility contrast.

## Voice change + full retime (2026-08-29)

Same-day follow-up to the pass above: all six VO lines re-recorded in
**Kimberly** (was Isla for lines 1-5, Kimberly for line 6 only). Kimberly
reads faster than Isla, so every scene's duration — originally cut from
Isla's measured pacing — needed recomputing. This was a mechanical retime,
not a design change: no palette, type-scale, motion-token, or layout rule
above was touched. Full mechanics (per-frame before/after numbers, which
constants moved vs. stayed, why Frame 4 didn't shrink) are in
`STORYBOARD.md`'s matching section — this note exists so a reader of
*this* file isn't left thinking the design spec and the built composition
disagree on total duration (55.7s now, not 60.0s).
