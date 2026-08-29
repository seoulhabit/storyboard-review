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
| 07 hanbang-rapidfire | 82.40 | 21.34 |
| 08 cta-endcard | 103.24 | 9.80 (no tail — final frame) |

Total composition length: 113.04s (~1:53) — the script's own 105s estimate
was pre-VO; real spoken pacing plus the CTA's frozen-grid hold lands here,
still well inside the faceless-explainer workflow's ~3-minute hard cap.

- 2026-08-29: Reviewer feedback — narrator mispronounced "INCI" as "inky"
  in Frame 7's VO (confirmed by transcribing `assets/voice/07.wav` with
  both whisper `small.en` and `large-v3`, which independently produced
  "inky names" both times; every other technical term in the script —
  Phenoxyethanol, Ethylhexylglycerin, Niacinamide, etc. — transcribed
  correctly, isolating the defect to this one acronym). Regenerated line 07
  with the same locked "Kimberly" element voice
  (`674b71b8-1d2e-4087-8567-d1f53c0b9f3c`), respelling the TTS input as
  "I-N-C-I" to force letter-by-letter pronunciation (the on-screen script
  text/captions keep the normal "INCI" spelling — only the TTS prompt was
  respelled). Re-transcription confirms correct pronunciation. New take
  measured 19.84s (+0.88s vs the old 18.96s); retimed Frame 7's internal
  fade-out/hold and the root timeline's Frame 7 duration, Frame 8 start,
  and total duration to absorb the delta. `CARD_STARTS` (the three
  flashcard pop-in beats) were deliberately left at their even 6.4s
  "rapidfire" cadence — that spacing was never word-synced (it's exactly
  1.8/8.2/14.6, a fixed rhythm under the narration, not per original
  design), so it doesn't need to track the new word timings.
- 2026-08-29: Reviewer feedback — "extreme small fonts." Visually confirmed
  by extracting and inspecting render frames (not just reading CSS
  numbers): Frame 7's three Hanbang cards and Frame 8's recap-chip grid
  were both top-anchored with `justify-content`/`align-content` defaulting
  to the start edge, leaving 40-60% of the 1920px-tall canvas empty below
  the content — which read as "small" even though the raw font-size values
  weren't wildly out of line with the rest of the design system. Fixed by
  centering/distributing each block's content across its full allotted
  height (`justify-content: space-evenly` on Frame 7's card stack,
  `align-content: center` + a taller box on Frame 8's chip grid) and
  bumping the smallest sizes in those two scenes (Frame 7: `--t-label`
  24→28px, `.hb-inci` 26→30px, `.hb-common` 46→56px; Frame 8: `.cta-chip`
  22→26px). Also added the 3rd Hanbang pair ("Artemisia Princeps =
  Mugwort") to Frame 8's recap grid — the STORYBOARD called for all 3 pairs
  there but only 2 existed in the shipped HTML. Other scenes (01, 02, 04,
  05, 06) were screenshotted and checked too; their text was legible at
  actual render resolution, so left unchanged rather than relayout the
  whole video beyond what the reviewer actually flagged.
- 2026-08-29: Parity pass against `snail-mucin-medical-secret` (rendered
  video / fonts / design lessons). Two fixes, both confirmed against actual
  rendered frames, not just source values:
  - **Safe-zone violations.** `06-teardown.html`'s `.tear-disclaimer` sat at
    `top: 1720px` — 160px inside the reserved bottom-360px Shorts safe zone
    (boundary is y:1560 on the 1920px canvas) — and `08-cta-endcard.html`'s
    `.cta-disclaimer` sat exactly on that boundary (`top: 1560px`) with no
    margin. The teardown card's actual ingredient-row content only needs
    ~975px of its declared 1440px height, so `.tear-card` height was cut to
    1200px and `.tear-disclaimer` moved to `top: 1480px`, clearing the
    boundary with ~50px to spare. On the endcard, `.cta-lockup` moved
    1350→1240px and `.cta-disclaimer` moved 1560→1440px, giving both
    elements room well inside the safe area. Re-rendered and confirmed both
    disclaimers now sit clear of the bottom band with visible margin.
  - **Fonts not self-hosted.** Of the four typefaces this project names
    (`--font-display` EB Garamond, `--font-body` Inter, `--font-mono`
    JetBrains Mono, `--font-kr` Noto Sans KR), only Noto Sans KR had a real
    `@font-face` backing it — the other three were pure CSS fallback chains
    with no committed font file, unlike `snail-mucin-medical-secret`'s
    fully self-hosted Bricolage Grotesque + JetBrains Mono. Fixed by adding
    real woff2 files to `assets/fonts/` and matching `@font-face` blocks
    (`font-display: block`, mirroring the existing Noto Sans KR pattern) to
    every frame that names each family: `eb-garamond-400.woff2` (the only
    weight ever used — every `--font-display` element is weight 400,
    explicit or default), `inter-800.woff2` (the only weight ever used —
    every `--font-body` element is weight 800), and `jetbrains-mono-500.woff2`
    (copied directly from `snail-mucin-medical-secret/assets/fonts/`, the
    exact same asset already verified there). Because JetBrains Mono is
    requested at three different weights against this one physical file
    (400 default, 500 on a few chips/parts, 700 on `.tear-row.tear-hero`),
    its `@font-face` declares `font-weight: 100 900` — a range spanning all
    three — rather than an exact `500`, so the browser treats the single
    file as covering that whole span instead of synthesizing fake-bold on
    the 700 request (the same technique `snail-mucin-medical-secret` uses,
    applied consistently here rather than per-frame). Note: hyperframes'
    own compiler already auto-fetches and injects deterministic
    `@font-face` rules for named Google Fonts at `check`/`render` time (seen
    in the `check` log: "Injected deterministic @font-face rules for 6
    requested font families") — a byte-for-byte comparison of the old and
    new renders at the same timestamp (t=2s, Frame 1's headline + VO line)
    showed identical output, confirming the fonts were already resolving
    correctly via that live-fetch path even before this fix. Self-hosting
    them explicitly matches the reference project's convention and removes
    the render's dependency on a live Google Fonts fetch at render time,
    consistent with this project's own pinned-CLI goal of rendering
    identically over time — it is a determinism/fidelity improvement, not a
    correction of a visibly wrong render.
  - Re-rendered: `renders/kbeauty-one-percent-line_2026-08-29_10-29-59.mp4`,
    113.07s, h264 1080x1920 30fps (unchanged from before), ~188kbps video
    bitrate (unchanged from the prior render's ~185kbps — confirming the
    video's small file size is a function of its flat typographic content,
    not a render-settings gap versus the reference project's photographic,
    Ken-Burns-heavy footage).
- 2026-08-29: External reviewer feedback (5 items) after watching the
  rendered video. Voice/VO left unchanged by explicit user decision — real
  human narration and further TTS-voice changes are both out of scope here
  (Kimberly is the locked, consistent narrator across the whole SeoulHabit
  series; swapping her for just this video would break that consistency,
  and recording real human VO is outside what this pipeline can do). Four
  items were implemented, each verified against the actual re-rendered
  frames:
  - **Mobile legibility.** Frame 4's 7-row INCI list and Frame 6's 14-row
    teardown card were unreadable at native size on a phone screen.
    Transcribed both VO lines word-by-word (`hyperframes transcribe`) to
    sync a digital push-in to the actual narration rather than guessing:
    Frame 6 now pushes in on "Niacinamide (2%)" at the exact word onset
    (6.28s local), holds through its aqua-circle mark, then pans down to
    land on "Ethylhexylglycerin" right as "Boom," is spoken (10.34s),
    holding through its ink-strike, before pulling back out. Frame 4's VO
    never names individual ingredients, so its zoom instead follows
    narration *structure*: push in on the above-the-line cluster during
    "legally listed by concentration," then pan down to land on
    `PHENOXYETHANOL` exactly as the coral rule slams (6.4s). Both use a
    `transform-origin: 0 0` wrapper (`#tear-card`, `#opl-list`) with
    pre-computed `scale`/`x`/`y` constants derived from each element's real
    layout (row heights, card padding) — not measured at tween time, and
    verified against actual rendered pixels afterward rather than trusted
    from the arithmetic alone (an initial Frame 4 anchor choice would have
    clipped the left edge of "CENTELLA ASIATICA EXTRACT" off-screen; caught
    by re-deriving the anchor at the text's left edge instead of the
    padded-column center before rendering).
  - **Sound design.** Added two SFX. Checked whether the bundled 19-file
    SFX library actually offered a distinct "highlighter" texture before
    picking one — its "whoosh/impact" and "quick pop" candidates turned out
    to be byte-identical (verified by hash) to `whip-slash.mp3` and
    `pop.mp3` already in this project, so resolving them fresh would have
    been a no-op or a needless duplicate. Instead: swapped Frame 4's
    1%-line rule-slam SFX from `whip-slash.mp3` to `marker-squeak.mp3` (a
    literal felt-tip sound, closer to "highlighter" than a generic
    whoosh, and already established in Frame 6 for the Niacinamide circle
    — now a deliberate marker/emphasis motif across both frames). Added
    `pop.mp3` (already used in Frame 3) to Frame 7 at each of the three
    Hanbang common-name underline reveals (84.45s / 90.85s / 97.25s).
  - **Visual scaffolding.** Frame 3's "EXTRACT = WATER + TINY BIT OF PLANT"
    equation relied on text alone. Added a small inline-SVG beaker + a
    single leaf that drops in and settles with a brief ripple, landing
    right as "TINY BIT OF PLANT" appears (8.85-9.3s) — ink-stroke outline,
    `--ink-2` leaf fill, no fill color that would compete with the frame's
    one aqua highlight (already spent on the K-beauty chip).
  - **Cheat-sheet redesign.** Frame 8's 5-chip recap grid was restyled from
    uniform gray chips into two color-blocked, kicker-labeled sections:
    "THE RECAP" over two solid `--ink` blocks (paper text) for the core
    truths, "HANBANG, TRANSLATED" over three `--aqua`-left-accented
    paper chips for the ingredient translations — a callback to Frame 7's
    aqua-underline treatment. First pass put the kickers at 0.7 opacity and
    the "=" signs in raw `--aqua`; `hyperframes check`'s contrast audit
    caught both as sub-3:1 failures (aqua reads fine as a large underline
    but fails as small text against a light background) — fixed by using
    full opacity with the checker's suggested darker kicker color and
    dropping the "=" tint back to plain ink, letting the border/background
    tint alone carry the color-blocking.
  - **Scope note:** the "highlighter swoosh" and generic bundled "pop"
    candidates being literal duplicates of existing project assets was
    confirmed by SHA-1 hash comparison, not by filename or description
    alone.
  - Re-rendered: `renders/kbeauty-one-percent-line_2026-08-29_11-33-47.mp4`,
    113.07s, same specs as before (h264 1080x1920 30fps, ~258kbps video
    bitrate — the small increase from ~188kbps is consistent with the new
    zoom/pan motion and beaker graphic adding real per-frame delta rather
    than a settings change).
- 2026-08-29: `/goal` directive to integrate "hyper-framed" sensory visuals —
  macro ingredient shots with dynamic keyframing, used as a visual breaker
  after a dense technical explanation — while using existing components
  first. Checked two places before authoring anything new:
  - **Assets**: `catalog/ingredient-photography/` (a shared, project-external
    library, not this project's own) turned out to hold 2048x2048 Higgsfield
    stills for every ingredient this video actually discusses, including the
    exact three Frame 7 later Hanbang-translates — `12-snail-mucin.png`
    ("glossy stretching gel"), `06-ginseng.png` ("whole forked root"), and
    `18-mugwort.png` ("fresh silvery-green leaf sprig"), per the catalog's
    own README — a near-verbatim match to the goal's own example language
    ("glistening snail mucin," "vibrant mugwort leaves," "highly textured
    ginseng roots"). Downsampled 2048px to 1400px (`sips -Z`, still >1.5x
    the 920px display size for headroom under the push-in) and copied into
    this project's own `assets/images/`, matching how fonts/audio are
    always project-local rather than referenced from the shared path.
  - **Registry**: `npx hyperframes catalog --query` surfaced `push-in`
    (single-subject camera push, holdable) and `scroll-camera-story`
    (multi-section forced-scroll pass with depth-rate parallax and
    decelerating arrival cues) as the closest existing components. Installed
    and read both. `push-in` hardcodes its timeline key to the literal id
    `"push-in"`, so three instances in one frame would collide — a
    single-subject primitive, not a sequence one. `scroll-camera-story`'s
    visual skin (dashboard chips, rings, skeleton bars) is built for a
    product-feature-tour, not ingredient photography, but its underlying
    *mechanism* — one `cam.t` progress value driving a percent-based world
    translate, non-overlapping arrival-cue tweens, per-layer parallax rates
    — is exactly the disciplined "hyperlapse through sections" engine this
    beat needed. Adapted that mechanism (a simplified two-layer version:
    photo + label, not four depth layers) into a bespoke frame rather than
    wiring the block in verbatim; removed the two installed component files
    and the `hyperframes.json` registry bookkeeping afterward since nothing
    ended up literally wired in, to avoid leaving unreferenced files in the
    project.
  - **New frame**: `compositions/frames/04b-ingredient-showcase.html`,
    inserted between Frame 4 (`one-percent-line`) and Frame 5 (`the-trick`)
    — the goal's own example placement ("like the 1% line breakdown"). Three
    slides (snail mucin, ginseng, mugwort, in Frame 7/8's own Hanbang order
    — a deliberate callback that primes that later reveal), each a quick
    snap-in from 1.14x scale (the "hyperlapse" cut), a brief held Ken-Burns
    push to ~1.07-1.09x with a small directional drift (2 layers of motion
    at once — push-in and parallax together per the goal's own menu, not a
    plain crossfade sequence), then a quick whip-out except the final slide,
    which just holds into the frame's own crossfade. Paper background,
    against ink on both neighboring frames (04, 05 are already back-to-back
    ink per `frame.md`'s table) — a deliberate second contrast pop so the
    beat reads as a breather, not another data frame. No new VO: the one
    wordless beat in an otherwise wall-to-wall-narrated video, letting BGM
    carry it alone — in scope per the goal (a visual/motion addition, not a
    script change) and consistent with the user's earlier decision to leave
    narration alone. Three `pop.mp3` hits (already this project's "reveal"
    SFX, used five times elsewhere) mark each slide's settle point. One
    aqua highlight per `frame.md`'s hard rule, spent on a 3-dot progress
    indicator rather than a second on-image accent.
  - **First pass ran long, cut after review**: the initial cut dwelled
    ~1.9s per image (5.8s visible span) — technically correct, but the one
    wordless, slow-push beat in an otherwise ~2s-per-kinetic-element video
    read as a drag once actually watched, and undershot the goal's own
    "rapid hyper-lapse" language. Compressed each slide to ~0.8s
    (0.12s snap-in, ~0.6s push, 0.12s whip-out) for a 2.5s visible span
    (3.0s comp duration) — a true rapid-fire pass rather than a showcase,
    while keeping all three ingredients and the Frame 7/8 ordering callback
    intact.
  - **Retime**: the interlude's visible span (2.5s, 3.0s comp duration incl.
    the standard 0.5s crossfade tail) is inserted at the existing Frame 4→5
    boundary (43.84s), cascading a uniform +2.5s to every element from
    Frame 5 onward — comp/VO/SFX starts, the main timeline's crossfade
    pairs, the root and BGM `data-duration`, and the final-anchor tween.
    Root duration: 113.04s to 115.54s.
  - **BGM caught by the runtime audit, not by ear**: extending `el-bgm`'s
    slot triggered `clip_media_fit` — the underlying `track.mp3` is only
    111.70s of real audio, so hyperframes silently truncates an oversized
    slot back to the media's actual length at render time. Left as just a
    longer slot number, the fix would have silently reverted itself,
    cutting music under most of the (now-later) Frame 8 endcard instead of
    extending it. Real fix: crossfade-looped the track with ffmpeg
    (`acrossfade`, `d=2`, triangular curves) blending its own tail back
    into its own opening, saved as `assets/bgm/track-extended.mp3` (levels
    at the seam checked with `volumedetect`: -16.9dB mean / -0.6dB max, in
    line with the rest of the track — no clipping, no dead spot) and its
    slot set to 114.2s, preserving the original's ~1.3s fade-before-end
    ratio against the new root duration. The extended file itself runs to
    117.5s — more than the 114.2s the second (shortened) pass actually
    needs — so it was reused as-is rather than re-cut a second time.
  - Verified in two passes, once per cut: `npx hyperframes check` (0
    lint/runtime/motion errors or warnings both times; contrast 57/59 pass;
    remaining info-level layout notes are unrelated, on Frames 4/6, from
    the prior entry's zoom work) and Studio snapshots at each internal beat
    — then re-verified against the actual rendered MP4 (not just Studio) by
    extracting frames at the new interlude and at every downstream frame
    boundary, confirming the retime landed correctly frame-for-frame.
  - Re-rendered: `renders/kbeauty-one-percent-line_2026-08-29_12-26-27.mp4`,
    115.57s, h264 1080x1920 30fps, 353kbps video bitrate (up from 258kbps —
    expected: photographic PNG content compresses heavier than this
    project's otherwise-flat typography, the same relationship noted
    against the reference project earlier in this log).
