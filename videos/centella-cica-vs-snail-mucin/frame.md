# Frame — centella-cica-vs-snail-mucin

## Canvas

1080×1920, 30fps, 9:16 (Shorts). Safe area: `--safe-top 120 / --safe-bottom
360 / --safe-left 60 / --safe-right 162` (source `tokens.css`).

## Channel audit (reuse basis, not re-derived)

Same audit basis as `glass-skin-5-habits/frame.md` § Channel audit — tokens
and the VO bus exist channel-wide only in `seoulhabit-launch` and
`kbeauty-one-percent-line`; captions ship only in `snail-mucin-truth` /
`snail-mucin-medical-secret`. This project copies from those, not re-derives:

- **Tokens** — `assets/tokens/tokens.css` copied verbatim from
  `seoulhabit-launch`.
- **VO bus** (`<hf-audio-group>`, `data-fx-chain`) — copied verbatim from
  `kbeauty-one-percent-line/index.html`.
- **Captions** — `.caption-group`/`.caption-word` +
  `.is-active`/`.is-spoken` mechanism from
  `videos/snail-mucin-truth/.hyperframes/caption-skin.html`, re-tokened to
  this project's palette (same approach `glass-skin-5-habits` used).

## Palette

Base five, from `tokens.css`: `--paper #F7F5F0`, `--ink #131516`,
`--aqua #59B8AE`, `--leaf #6F8F72`, `--coral #C97A5C`, plus `--highlighter
#E0A32B` for the numeral/data-mark moments. **One aqua-family highlight per
frame** (hard law, inherited) — Frame 4 is the sole exception (see below).

**Coral is the single voltage moment for the whole video** — the "CICA =
CENTELLA ASIATICA" reveal on Frame 4. No aqua in that frame; the equivalence
chip's own accent border, normally aqua on the reused `kbeauty-one-percent-line`
chip, is recolored coral for this one frame only, so the two accents never
compete inside the same composition.

Frames alternate paper/ink, same convention as every prior channel video:

| Frame | Ground |
|---|---|
| 1 hook | paper |
| 2 string test | ink |
| 3 dropper | paper |
| 4 twist | ink |
| 5 cta | paper |

All four boundaries change ground — hard cut at every one (see Motion).

## Type

`--font-display` EB Garamond (verdict headline, Frame 5), `--font-body` Inter
700/800 (verdict-rail words: SNAIL / CENTELLA, GLOW / CALM), `--font-mono`
JetBrains Mono (the Frame 4 INCI qualifier chip, source-style callouts),
`--font-kr` Noto Sans KR 500 (습 SeoulHabit lockup, Frame 5 only). Nothing
under `--t-floor: 20px`.

## Faceless

Presenter is the macro plate/texture, not typography — same deliberate
departure `glass-skin-5-habits` made from this channel's typographic-first
house style, driven here by the user's own script direction that the string
test is the highest-retention hook visual in the category. Type still
performs real work: the persistent two-row verdict rail, the Frame 4
qualifier chip, and wall-to-wall captions.

No talking-head footage, no visible faces at any point. Every plate and video
is hands-below-wrist or texture-only, matching
`catalog/product-photography/`'s no-face constraint, extended here to
generated video.

## Media exception (filed decision record)

`catalog/product-photography/README.md` states the HyperFrames lane is
browser-drawn only and that feeding generative imagery into a composition
"needs its own filed decision record first." `glass-skin-5-habits/frame.md`
filed that record for generated **stills**. This is the record for generated
**video**, one step further:

- **Why**: the user's production rule makes the snail-mucin string test
  mandatory inside the first 10 seconds. A still plate with Ken Burns cannot
  show a substance stretching, sagging, and pinching off between two fingers
  — that motion is the entire hook.
- **Precedent**: `seoulhabit-launch/assets/broll/*.mp4` — muted,
  framework-owned `<video>` with `data-start`/`data-duration`/
  `data-track-index`, added by explicit user direction in that project after
  its original faceless render had already shipped once (see that project's
  own `frame.md` § Faceless / Build history).
- **Scope**: exactly two of five frames (Frame 2 string test, Frame 3
  dropper). Frames 1, 4, 5 stay browser-drawn/photography, matching this
  channel's default.
- **Constraints, extended from `catalog/product-photography/README.md`'s
  hard constraints for stills to generated video**: unbranded, no faces
  (hands cropped below the wrist), no claims on any rendered surface, no
  glow/bloom/lens flare, muted (no autoplaying audio track — any usable foley
  is demuxed and re-placed as a scheduled `<audio>` clip, not left on the
  `<video>` element).
- **Verification against `catalog/ingredient-photography/12-snail-mucin.png`**:
  opened at full resolution before deciding this. It is a top-down pour into
  a glass dish, not a stretch — confirms no existing catalog still can serve
  as the string-test hero, and is used instead as the video model's material/
  lighting reference only.

## Motion

System eases only: `--e-out` entrances, `--e-in` exits, `--e-inout` holds.
`--d-snap 180ms` impact beats (the coral reveal, the verdict-rail advance),
`--d-fast 400ms` / `--d-base 500ms` word reveals. No bounce/elastic/back
eases, no infinite keyframes.

**Hard cuts only, no crossfades.** All four boundaries change ground; per
`faceless-video-craft`'s cuts-vs-crossfades rule and this channel's own
`kbeauty-one-percent-line` round-1 incident, a crossfade across a ground
change produces a muddy near-blank transition midpoint. Hard cut at all four.

Generated `<video>` clips (Frames 2, 3) are framework-owned and muted —
`data-start`/`data-duration`/`data-track-index` on the `<video>` element
itself, same idiom as `seoulhabit-launch`. Their own internal motion is
whatever the generation produced (real footage, not seeked), which is
acceptable per that same precedent — the seek-safety requirement binds
authored GSAP timelines, not a pre-rendered video asset the engine plays back
as a clip like any other media plate.

The two-row verdict rail (SNAIL → GLOW / CENTELLA → CALM) builds one row per
frame across Frames 2→3 and holds complete through Frames 4→5 — a `t`-driven
focus-advance, adapted from RoutineLadder's mechanism but not the component
itself (see Component reuse).

## Elevation

`--elev-2` on the verdict rail's active row and the Frame 4 equivalence chip
only. **Glow banned outright** — no `box-shadow: 0 0 …` / `drop-shadow(0 0 …)`
anywhere, matching every other project on this channel.

## Brand anchor

습 SeoulHabit text lockup (Noto Sans KR 500) appears once, Frame 5, bottom-
safe — not the Fold & Spark mark.

## Audio mix

`<hf-audio-group id="voiceover">` bus carrying the channel's real chain
verbatim (highpass 90Hz → peaking 150Hz +0.8dB → compressor -24dB/4:1 →
peaking 3kHz +2.5dB → peaking 6.5kHz -4dB Q3.5 de-ess → limiter -9dB), copied
from `kbeauty-one-percent-line/index.html`'s `data-fx-chain`. 80ms automation
fade-in/out on every VO and SFX clip, versioned `{"version":1,"lanes":[...]}`
shape — confirmed on `hyperframes@0.8.17` that the flat-array shape is
silently accepted by `check` but rejected at render (per
`faceless-video-craft`'s documented incident, re-confirmed by
`glass-skin-5-habits`). BGM carries `data-fx-carve {sources:["voiceover"],
strength:0.25}`.

**Volume-automation trap** — a `"volume"` automation lane *replaces*
`data-volume` on this CLI version rather than scaling it. Every clip's
plateau value must be its real intended level, not a normalized `v:1`.

**Verified against the volume-automation trap, not just written to avoid it.**
Confirmed via an isolated test render (all non-BGM `<audio>` elements removed,
BGM's own authoring left untouched): BGM measured -33.4dB RMS in a
BGM-only window, matching the -14.8dB native-track RMS at that point minus
the expected -18.4dB for its authored `data-volume="0.12"` almost exactly —
the plateau value is genuinely being read as the real gain, not replaced by
an unintended `v:1`. The full mix's same window measured ~8.7dB hotter than
that isolated baseline; isolating confirmed the difference is residual
room-tone in the final VO take, lifted by the shared voiceover chain's
compressor makeup gain (+3dB) and limiter during the wordless loop-hold —
not a BGM level bug. Left as authored: it sits under Frame 5's own VO level
throughout, is confined to a low-attention 1s wordless tail, and fixing it
would mean touching the channel-level shared fx-chain for one minor artifact,
which the channel's own consistency rule reserves for a specific, deliberate
reason, not a single video's tail hiss.

**SFX sourcing** — generate Frames 2/3 video with `generate_audio: true` and
demux for a genuine sticky-tap and wet-dispense cue (a real gap on this
channel until now — see `glass-skin-5-habits/assets/MANIFEST.md`'s own
documented absence of true ASMR foley). Fall back to the channel's existing
cue library for hits/chimes/whooshes where no usable generated cue exists,
logged honestly (`Exact` / `Substitute`) in `assets/MANIFEST.md` — never
fabricated from an unauthorized model.

## Content corrections

Both corrections below follow the precedent set in
`glass-skin-5-habits/frame.md` § Content corrections: user asked, user chose
to soften rather than ship verbatim or add only a spoken qualifier. Full
before/after text lives in `SCRIPT.md`.

**Line 3** — "you need Centella Asiatica" (exclusivity claim) + "fix …
active breakouts" (treatment claim) → "Centella Asiatica is the
better-studied pick" (comparative framing, no cure claim, no exclusivity).

**Line 4** — "They are the exact same ingredient" → "same plant, different
label." "Cica" is an unregulated K-beauty marketing shorthand, not an INCI
ingredient name. It is near-universally built on Centella Asiatica or its
purified triterpenes (madecassoside, asiaticoside, TECA), so "same plant" is
defensible — but "the exact same ingredient" asserts a 1:1 identity the label
does not guarantee. The corrected VO keeps the twist and near-identical word
count; the dropped precision moves to an on-screen mono qualifier chip on
Frame 4 (`"Cica" is a marketing word, not an INCI. Check the label.`) rather
than being cut entirely.

Video carries the channel's standard "general guidance, not medical advice"
disclaimer — routine/label literacy comparing two actives, not a locked
`ING-*` source record for either, same status as `kbeauty-one-percent-line`
and `glass-skin-5-habits`.

## Component reuse

- **`.cta-chip-hb` / `.cta-chip-eq`**
  (`kbeauty-one-percent-line/compositions/frames/08-cta-endcard.html:115,185`)
  — reused directly for Frame 4's "CICA = CENTELLA ASIATICA" reveal. Already
  shipped on this channel as an "X = Y" equivalence chip with a thumbnail
  ("Snail Secretion Filtrate = Snail Mucin"); this is the same pattern, same
  content shape. The catalog documents this as a design-system-level pattern
  rather than a harvestable component, so reuse here adds no new catalog
  entry.
- **SplitFaceProtocol**
  (`catalog/visual-components/split-face-protocol/splitfaceprotocol-spike.html`)
  — mechanism adapted, skin dropped. Its real mechanism (a bisector, two
  independently-targetable field groups `#control-arm`/`#active-arm`, one
  paused `t`-driven timeline, tint flooding one side only, no success color)
  maps directly onto Frame 5's snail-vs-centella split. Its literal content —
  a facial outline, a clinical control/active-arm protocol — is neither
  present nor implied here; adapted, not wired in verbatim. If this holds up
  in the render it is the candidate for catalog contribution as a new,
  named, generalized `split-compare` component (see Catalog contribution
  below) — distinct from SplitFaceProtocol itself, which stays a clinical-
  diagram-specific component.
- **RoutineLadder** — focus-advance *idea* only (one row in focus, driven by
  a single `t`) for the verdict rail. Not the component: RoutineLadder's own
  spec fixes it at six rungs and forbids resizing to occupancy, and this
  video's rail is a two-row verdict, not a routine sequence. Same honest
  framing `glass-skin-5-habits` used for its five-of-six habit-stack reuse.
- **Caption mechanism** — reused verbatim from
  `videos/snail-mucin-truth/.hyperframes/caption-skin.html`, re-tokened to
  this project's palette.

## Catalog contribution (planned, pending render)

If Frame 5's bisector/split mechanism renders cleanly and holds up under
verification, harvest it to `catalog/visual-components/split-compare/` — a
generalized two-field, one-timeline comparison mechanism distinct from
SplitFaceProtocol's clinical-diagram-specific skin — following the
`ThresholdList` precedent for how a mechanism gets generalized out of one
video's specific content. Nothing else from this build is a genuine new
mechanism: the equivalence chip and caption skin are pure reuse, and the
verdict rail is a two-row instance of an idea already documented under
RoutineLadder's own entry, not a new component in its own right.

## Corrections to the catalog's own README (found by opening the files, not the table)

Both flagged in `assets/MANIFEST.md`, and worth fixing at
`catalog/ingredient-photography/README.md`'s source so a later project
doesn't repeat the same misread:

- `12-snail-mucin.png` is described as "glass dish of glossy stretching
  gel." It is actually a top-down macro of a clear stream being **poured**
  into a glass dish — no stretch, no fingers. Confirmed the string test
  cannot be built from this catalog still.
- `02-centella-asiatica.png` ("fresh cica leaf sprig") is accurate as a
  description, but its green is well outside the system's matte `--leaf
  #6F8F72` — usable only after grading, not as a drop-in system color.

## Post-render review fixes

A review of the first shipped render (`renders/centella-cica-vs-snail-mucin_2026-08-30_16-57-00.mp4`)
flagged four issues. Pixel-measuring the actual render (not the composition
source) showed two of the four diagnoses named the wrong element; fixed
per the diagnosis that survived measurement, not the one as originally
reported.

- **Verdict rail in the Shorts UI kill zone (was reported as "captions"; the
  captions were fine).** Measured: `.caption-stage` sits at y1360–1510
  (78.6% down), clear of YouTube's bottom ~20% zone and this project's own
  `--safe-bottom` (y1560). What *was* buried: the verdict rail, y1546–1660
  in Frames 2/3 and **y1660–1780 (92% down)** in Frame 4 — all three used a
  hardcoded `bottom: 260px` / `bottom: 140px` that pre-dated the caption
  band's final position. `05-cta.html` had already solved this for itself
  (`top: 960px`, with a comment naming the caption-band collision) but the
  fix was never carried to Frames 2/3/4 — the exact channel failure mode
  `faceless-video-craft` names: *"a safe-area fix made in one scene that was
  never re-checked in the others."* Root cause: `--safe-bottom: 360px` was
  declared in six files and consumed in zero — every bottom-region Y was a
  hand-tuned pixel. Fix: all four bottom-region scenes now share a
  `--cap-band-top: 1360px` token (mirroring `captions.html`'s own value) and
  express their rail/CTA offsets as `calc(var(--cap-band-top) - Npx)`, so the
  coupling is stated rather than re-derived by eye. Frames 2/3's
  `.rail-scrim` gradient stops were re-tuned to keep contrast at the rail's
  new, higher position. `npm run check`'s layout pass cannot catch this class
  of defect — it validates box overlap, and the old rail sat *below* the
  caption band rather than overlapping it, so it never registered as an
  error.
- **Cream wipe misread as a stray layer (04-twist.html, `#f4-cream`).** Not
  a stray video layer — it is the authored "cream swipes over" beat this
  file's own beat sheet calls for. It read as an accident because the
  original box was a hard-edged, 45%-top/26%-height, fully opaque band, and
  `object-fit: cover` on its 781×1400 portrait source showed only the flat
  top of the bowl — no visible swirl. Rebuilt full-bleed with a feathered
  `mask-image` on both leading and trailing edges and dropped to 0.88
  opacity, so it reads as a soft pass of cream over the leaf rather than a
  panel. Also given a `tl.set("#f4-cream", { x: "-110%" }, 0)` seek baseline
  — it was the only element in the project hit by two tweens at different
  timeline positions with no `t=0` registration, the documented
  multi-`fromTo()` bleed-through class of bug (`faceless-video-craft`
  SKILL.md's *Failure modes worth naming*), applying the same fix
  `03-dropper.html` already uses for `#f3-row-centella`.
- **Abrupt ending (05-cta.html + captions.html).** True as reported, but the
  literal fix ("extend the final clip 1.5–2s") would have made a
  pre-existing, larger defect worse: Frame 5 was already frozen from ~2.3s
  (its last authored beat) to its 8.040s end — 6.3s with zero pixel change
  outside the caption layer — and the final caption group held on screen
  through the *entire* tail (`captions.html`'s `isLast ? DURATION` release
  rule), so extra silent time alone would not have let the CTA breathe.
  Fixed three ways together: scene extended 8.040s → 9.640s (root
  composition 28.680s → 30.280s, BGM `data-duration` and fade-out automation
  shifted to match); a continuous Ken Burns added to `.split-field img`
  (scale 1.0 → 1.045 across the full scene) so the extended tail is live
  motion, not a longer freeze; and the final caption group's release rule
  changed to `Math.min(DURATION, group.end + 0.3)` instead of holding to
  `DURATION`, so it clears at ~27.96s and leaves a clean ~2.3s CTA-only
  window before the loop point.
- **Title inside the top UI zone (01-hook.html).** True as reported.
  "SNAIL MUCIN"'s cap-top measured y133 — inside YouTube Shorts' ~10% top
  zone (192px on a 1920px canvas) — while clearing this project's own
  `--safe-top` (120px) easily; the channel token is simply more permissive
  than the platform. Fixed with a scene-local `top: calc(var(--safe-top) +
  130px)` on `.headline-zone` rather than raising `--safe-top` itself, since
  that token is identical across all four channel projects and raising it
  channel-wide is a separate decision, not one scene's call to make.

Not fixed, flagged for a separate decision: `assets/tokens/tokens.css` is
never linked or imported by any composition in this project — every frame
re-declares its own inline token copy, so the "canonical" file is
documentation, not a live stylesheet; `--safe-top: 120px` is more permissive
than YouTube's own ~10% top zone across all four channel projects, not just
this one; `03-dropper.html`'s `.v-row` CSS default is `--p: 1` (visible) with
`#f3-row-centella` relying entirely on its `fromTo`'s "from" value to stay
hidden before 0.3s — the same latent seek-bleed class as the `#f4-cream` bug
above, just failing visible instead of invisible.

## Design-system reconciliation

Same reconciliation basis as `seoulhabit-launch/frame.md`,
`kbeauty-one-percent-line/frame.md`, and `glass-skin-5-habits/frame.md`:
`assets/tokens/tokens.css` copied verbatim from `seoulhabit-launch`. No new
tokens invented here.
