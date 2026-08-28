# frame.md — retinol-patch-test

## Provenance validation (2026-08-28)

Everything below the first build cited `videos/kbeauty-one-percent-line` and
`videos/seoulhabit-launch` as "the" SeoulHabit design system. `git ls-files`
shows both are **fully untracked** (0 files in git) — uncommitted working-tree
content from another session, not checked-in ground truth. So was
`catalog/ingredient-photography/16-retinol.png`, the product photo Frame 2
used. The project was rebuilt against what's actually tracked:

- **Tokens/fonts** — `videos/skincare-glossary-part-4-texture-anti-aging/index.html`
  (and the identical block in `skincare-ingredient-glossary`, `-part-2`,
  `-part-3`), a real committed SeoulHabit video with the tokens inlined per
  file, doc-commented as read verbatim via DesignSync from the same source
  Claude Design project — same hex values, different (and now-adopted)
  variable names (`--short-safe-*`, `--ink-2-dark`/`--ink-3-dark`). Its
  `assets/NotoSansKR-500-subset.woff2` replaces the copy that came from the
  untracked project (checksums differ).
- **Audio wiring** — `videos/red-ginseng-two-routes/index.html` (tracked,
  rendered, `renders/video.mp4` committed): plain `<audio data-volume>`
  elements. No `hf-audio-group`/fx-chain/carve precedent exists in any
  checked-in project — that machinery is dropped.
- **Frame 2's icon** — the exact generic leaf-stroke SVG path and card copy
  (`"A gold-standard anti-aging compound that promotes cell turnover."`,
  category `"Vitamin A"`) from that same glossary project's own tracked
  **Retinol** card (`skincare-glossary-part-4-texture-anti-aging/index.html`
  line ~317) — reused instead of the untracked photo.
- **Frame 6's lockup** — the "습 SeoulHabit" wordmark + slide-up-and-breathe
  move is genuinely checked in: `videos/red-ginseng-two-routes/compositions/frames/06-endcard.html`.
- **Coral** `#C97A5C` — grounded in `videos/red-ginseng-two-routes/capture/extracted/tokens.json`
  (that project's own tracked pre-remix capture) plus the "limitation /
  refusal" role documented in `catalog/README.md` and the tracked
  `catalog/visual-components/evidence-meter` component.
- **Frames 3 & 4** — already correct: `split-face-protocol` and
  `celestial-arc` are genuinely tracked catalog components (`git log` shows
  real commits). No change needed beyond the token-name alignment below.

## Canvas

1080×1920, 30fps. Safe areas: top 120px, bottom 360px, left 60px, right 162px
(`--short-safe-top/-bottom/-left/-right`, matching the checked-in glossary
projects' names). Nothing load-bearing sits outside them.

## Palette

Tokens inlined per file (no shared `tokens.css` — no checked-in project uses
one), copied from `videos/skincare-glossary-part-4-texture-anti-aging/index.html`.
Paper `#f7f5f0` / ink `#131516` alternate as scene grounds. Aqua `#59b8ae` is
the recurring highlight — **exactly one aqua moment per frame**. Highlighter
`#e0a32b` carries the hook's "STOP" beat. Coral `#c97a5c` (see Provenance
above) is spent **once in the whole video** — Frame 5's "wash it off" symptom
branch, coral's system role of "a limitation or a refusal." No success color;
glow is banned.

## Type

`--font-display` EB Garamond for display headlines, `--font-body` Inter for
narration-adjacent body copy, `--font-mono` JetBrains Mono for labels/chips,
`--font-kr` Noto Sans KR for the 습 SeoulHabit lockup — loaded via the Google
Fonts `<link>` each checked-in frame file uses, not a separately self-hosted
tokens file. Nothing ships smaller than the 20px floor.

## Motion

No bounce/elastic/back easing, no infinite keyframes — every animation
resolves to a held final state. Scene-to-scene: 0.5s opacity crossfade,
`power2.inOut` (matches every checked-in project's `index.html`).

## Elevation

Shadow only (`--elev-1/-2/-3`), never glow, per token file.

## Content corrections (evidence rigor)

The user's Step 1 line — "This mimics the skin on your face perfectly" — is an
unsourced overclaim; no `ING-*` record exists to support "perfectly." Softened
to "...the spots that behave most like the skin on your face" (see `SCRIPT.md`
Line 3, `BRIEF.md` § Notes). No citation chips are used anywhere in this video —
patch-testing guidance is procedural, not an efficacy claim. The outro instead
carries the sanctioned disclaimer microcopy: "General patch-testing guide — not
sourced claims, not medical advice," mono, `--ink-3`, ≥ `--t-floor`.

## Brand anchor

습 SeoulHabit Noto Sans KR text lockup (Frame 6) — genuinely checked in, see
Provenance above. The Fold & Spark logo mark is explicitly banned from
SeoulHabit videos (documented in the untracked `seoulhabit-launch/frame.md`;
no checked-in project uses that mark either, consistent with the ban).

## Audio mix

Plain `<audio data-volume>` elements, matching the tracked
`videos/red-ginseng-two-routes/index.html` — no voiceover bus, fx-chain, or
carve ducking automation (that machinery only ever existed in the untracked
kbeauty/seoulhabit-launch projects). BGM at `data-volume="0.12"`, retrieved
bed ("calm, warm, aesthetic educational skincare background, gentle and
reassuring, low presence under narration"), 57s — ends a few seconds before
the video's ~60.7s total, which is fine; no loop needed. SFX at
`data-volume≈0.35`, resolved via HeyGen retrieval (`audio_meta.json`):
hook-hit + buzzer (Frame 1), soft-whoosh + soft-click (Frame 2), soft-click
×2 (Frame 3, both test-site markers), pop + soft-click ×3 (Frame 4, pea dot +
rule chips), tick (as a ticking-clock texture under the 0h→24h→48h ladder) +
alert-ping truncated to ~1.3s (Frame 5's coral beat), chime (Frame 6 lockup).

## Design-system reconciliation

Any off-token color introduced while porting the split-face-protocol SVG
geometry (Frame 3) or the celestial-arc night motif (Frame 4) is normalized
to the palette above before shipping.

Frame 3 was rebuilt post-ship, twice. First pass hand-drew an anatomical side
profile (nose/lips), which read as amateurish. Second pass replaced it with a
hand-drawn front-view head+shoulders bust — cleaner, but still invented
geometry, not an existing component. Final pass reuses the catalog's own
`split-face-protocol` component verbatim: its `#control-arm`/`#active-arm`
cranial bezier paths, mirrored into one closed outline, with the two test
sites marked as rounded-rect zone chips matching that component's
`.sfp-zone-wire` convention (recolored to this project's aqua). That second
rebuild also surfaced a real layout bug worth carrying forward as a rule for
this project: a `.zone` class that sets `top` without also setting
`bottom: auto` inherits `bottom: 0` from the shared `.clip { inset: 0 }` base,
so its box silently stretches to the canvas bottom — invisible for plain-text
children, but it turns bordered/backgrounded children (chips, cards) into
stretched shapes under default flex `align-items: stretch`. Any new zone
built on `.clip` should set the unused side to `auto` explicitly.

Frame 4's night motif had the same problem: the first pass hand-drew a simple
moon + 3 dots instead of reusing `catalog/visual-components/celestial-arc`.
Rebuilt to port the source's actual arc path, sun, and moon geometry
(deterministic and glow-free, since the source runs on CSS `infinite`
keyframes and a blurred box-shadow — neither allowed here). The first
crescent-moon attempt (a hand-tuned two-arc SVG path) silently rendered
nothing — caught with `hyperframes snapshot`, not the Studio preview, which
was unreliable for scrubbing in this session. Fixed with an SVG mask (a
circle cut by an offset circle), a more reliable technique and, incidentally,
a closer port of the source's own inset-box-shadow "subtract an offset
shape" trick than the arc-path attempt was.

**Process note:** when a hand-authored SVG element might not be rendering as
expected, `npx hyperframes snapshot . --at <seconds> --no-end -o <dir>` (then
read the resulting `contact-sheet.jpg`) is faster and more reliable than
scrubbing the interactive Studio preview.

## Frame zero

Frame 1 opens on paper ground with the retinol-bottle silhouette mark faint in
the background — the video's visual signature carried through to Frame 2's
large leaf-icon treatment (the checked-in glossary's own Retinol-card icon,
not a product photo — see Provenance above).

## Measured timing (from generated TTS, `assets/voice/0N.wav`)

Scene start = previous start + previous VO duration. Scene duration = own VO
duration + 0.5s crossfade tail (final scene: no tail). All values below are
measured (`ffprobe`), not estimated.

| # | Frame | VO start | VO duration | Scene duration |
|---|---|---|---|---|
| 1 | 01-hook | 0.000 | 6.296 | 6.796 |
| 2 | 02-power | 6.296 | 12.147 | 12.647 |
| 3 | 03-test-site | 18.443 | 8.620 | 9.120 |
| 4 | 04-night-dose | 27.063 | 10.162 | 10.662 |
| 5 | 05-wait-48 | 37.225 | 12.904 | 13.404 |
| 6 | 06-outro | 50.129 | 10.553 | 10.553 (no tail) |

**Total duration: 60.682s.** This runs longer than the 55s the user's on-camera
timing implied, because the adapted VO reads a little slower than the
creator-storyboard's silent stopwatch cues. Per pipeline convention, measured
truth wins over the estimate — 60.7s is comfortably inside the faceless-explainer
route's 30–90s sweet spot (hard cap ~3min).
