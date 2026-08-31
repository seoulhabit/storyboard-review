# Ceramides / skin barrier — design notes

## Canvas

1080×1920, 30fps. Safe areas: top 120px, bottom 360px, left 60px, right
162px (`--short-safe-top/-bottom/-left/-right`), matching every other
project in this pipeline. Nothing load-bearing sits outside them.

## Provenance validation (do before Build, not yet done in Setup)

Design tokens and fonts are not yet copied into this project. Per
`retinol-patch-test/frame.md`'s own provenance-check pattern: before Build
starts, confirm which `skincare-glossary-part-*` project's `index.html` is
actually checked into git (`git ls-files`) and copy tokens/fonts from that
file. Do **not** pull tokens from `seoulhabit-brandshort` — confirmed during
planning to be a separate, unrelated project (a different, already-rendered
video about INCI-label transparency) with its own different palette
(`--paper:#F6F4F0`, `--ink:#232A5E`, `--aqua:#1F7A7A`, etc.) that doesn't
belong to this pipeline's design system.

Ceramides identity content (name, Korean name, category, body copy) is
reused verbatim from the checked-in
`catalog/ingredients/skincare-ingredient-glossary/components/09-ceramides.html`
rather than authored fresh. Confirmed real token values from that file:
`--paper:#f7f5f0`, `--ink:#131516`, `--aqua:#59b8ae`, `--ink-2-dark:#878b8c`,
`--ink-3-dark:#7c8082`, `--rule-dark:#333333`, `--highlighter:#e0a32b`
(confirmed in `retinol-patch-test/compositions/frames/01-hook.html`),
`--coral:#c97a5c` (confirmed identically in `kbeauty-one-percent-line`,
`retinol-patch-test`, and `red-ginseng-two-routes` — coral is not currently
planned for use in this video, see BRIEF.md § Customizations, but the real
value is recorded here in case a later revision wants it). Fonts: EB Garamond
(display), Inter (body), JetBrains Mono (mono/labels), Noto Sans KR (Korean
glyphs, self-hosted subset woff2, copied into this project at
`assets/fonts/NotoSansKR-500-subset.woff2` — required for Frame 3's "세라마이드"
and Frame 6's "습 SeoulHabit" lockup; any frame using Korean glyphs must
declare a matching `@font-face` pointing at this real file, never name
Noto Sans KR without it).

## Palette & motion

Same restraint rules as every other project in this pipeline: shadow-only
elevation (no glow), crossfade-only scene transitions (0.5s, power2.inOut),
no infinite keyframes, no `Date.now()` / `Math.random()` / network fetches.
Coral reserved for a single voltage moment if one is genuinely warranted —
see `BRIEF.md` § Customizations for why this video may not spend it at all.

## Open items for Build

- Confirm exact token source file via `git ls-files` (not yet done — Setup
  phase only covered planning docs).
- Measure real scene durations from TTS output; the nominal ~5/10/13/7/15/10s
  splits in `STORYBOARD.md` are carried over from the user's original
  script timing (Frame 3's original ~20s span, now split across Frames 3-4),
  not yet validated against actual voice timing.
- Design the brick/grout SVG for Frame 3. No existing component in this
  system's catalog covers this metaphor — checked `catalog/visual-components/`:
  `evidence-meter`, `graded-scale`, `split-face-protocol`, `routine-ladder`,
  `celestial-arc`, `dawn-to-dusk-routine` — none is a barrier/brick-wall
  diagram. This will be a new, bespoke composition, built in the same
  flat/unlit/restrained visual language as the rest (no photorealism, no
  generative imagery). Single ground throughout (paper) — do not reintroduce
  a mid-scene ground change.
- Frame 3's reused identity content is nominal fields only (name/Korean
  name/category) — do not pull in the glossary card's "commonly used for"
  line; that's a separate unsourced claim outside what was reviewed.
- Frame 4 ("the catch," the −40% stat) must stay pure typography. Do not
  size any fill, wipe, or wall-removal animation to the 40% figure — that
  would encode an unsourced effect size in geometry on top of the spoken
  claim, which this pipeline's own render-discipline notes flag as its own
  assertion. Numeral reveal + sound only.
- Design the wheat/flask icon pairing for Frame 5 in the glossary's existing
  icon style (24x24 viewBox, stroke-based, matching `09-ceramides.html`'s
  own icon).
- Decide whether Frame 2's "cost" cue needs its own small component or can
  reuse an existing pattern from another project — not checked yet.
- Frame 1's nominal ~5s is tight for a 20-word line (240wpm at nominal).
  `retinol-patch-test`'s similarly-sized hook line measured ~190wpm/6.8s
  actual — expect Frame 1 to stretch a couple seconds at real TTS, and the
  total runtime to land a bit past the nominal 60s. Normal for this
  pipeline, not a defect.
- The "no proportional geometry" guardrail applies to **both** stat beats —
  Frame 1's "50%" and Frame 4's "−40%" — not just Frame 4. Both are already
  specified as pure typographic reveals in `STORYBOARD.md`; keep it that way
  at Build, don't let either grow a bar/fill/wipe tied to the number.
- Captions: follow `retinol-patch-test`'s simpler `caption.txt` pattern, not
  the `caption_groups.json`/`captions.html` system some other projects in
  this repo use (e.g. `snail-mucin-medical-secret`). Generate from final VO
  timing at Build.
