# Catalog

Inventory of what this repo contains as of 2026-08-30, with emphasis on
what the most recent working session created or changed. Video projects
live under `videos/<slug>/` as self-contained HyperFrames projects
(`index.html`, `compositions/frames/`, `STORYBOARD.md`, `assets/`,
`renders/`). Reusable stock media and components live under `catalog/`.

## 2026-08-30 session

- **New video: `glass-skin-5-habits`** — 41.5s SeoulHabit Short built from a
  user-supplied A/V script ("5-Habit K-Beauty Routine"), the first project on
  this channel where **macro photography is the primary presenter across
  every scene**, not typography (a deliberate departure from the channel's
  usual typographic-first house style, driven by the user's own tactile/ASMR
  brief). Audited the whole channel first for real inheritance (tokens,
  audio bus, caption mechanism) rather than assuming a shared catalog folder
  implied consistency — found real drift (VO bus and tokens.css each exist
  in only 2 of 10 prior projects; the only real caption mechanism lives in
  the snail-mucin projects under an unrelated palette) and copied from the
  right sources rather than the majority pattern. Five reused
  `catalog/product-photography` stills + four newly generated plates (two
  catalog-table assumptions were wrong until the files were actually
  opened — see `assets/MANIFEST.md`). Three real bugs found via pixel-level
  snapshot inspection, not from a clean `check` output: a habit-tracker
  badge that kept its digit instead of showing a checkmark after a
  mid-timeline state change, a blank dark box at Frame 2's own hard-cut
  frame-zero, and a 3.5s flat stretch past the shorts cadence ceiling — all
  fixed and re-verified. Full envelope shipped: real word-level-transcript
  captions (re-tokened from the channel's one existing caption mechanism),
  `.srt`, two-pass loudness mastering (-14 LUFS/-1.5dBTP), and a scored
  thumbnail set. See `videos/glass-skin-5-habits/frame.md` § Verification.
- **New video: `centella-cica-vs-snail-mucin`** — 30.3s SeoulHabit Short
  ("Snail Mucin or Centella?") comparing the two ingredients and correcting
  the K-beauty "Cica = same ingredient" claim to "same plant, different
  label." Built across two sessions: an initial build (five frames, two
  generated `<video>` macro clips for the string-test/dropper hook per a
  filed media-exception record, closing verdict split), then a review-fix
  pass this session against an external QC report. The report's four
  findings were reproduced against actual pixels before fixing anything, not
  applied verbatim — two of the four misdiagnosed the cause: "captions in
  the kill zone" was actually the **verdict rail** buried at 92% down in
  Frame 4 (captions themselves measured clear); a "stray video layer" at
  0:15–0:17 was actually the authored cream-wipe beat, just built as a hard-
  edged opaque panel with no swirl visible — rebuilt full-bleed with
  feathered mask edges instead of deleted. The literal "extend the ending"
  instruction would have made a bigger pre-existing defect worse (Frame 5
  was already frozen 6.3s before the fix); fixed with an extended scene, a
  continuous Ken Burns, and an earlier caption release together. Verified
  by re-measuring the new render at the same pixel level that caught the
  original defects, not by re-running lint. See
  `videos/centella-cica-vs-snail-mucin/frame.md` § Post-render review fixes.
- **SplitCompare harvested into `catalog/visual-components/`** — generalized
  from `centella-cica-vs-snail-mucin`'s closing verdict split: a vertical
  bisector, two independently-targetable fields, a tint flood on the
  interrogated side only (no success color, never both fields at once).
  Mechanism adapted from `SplitFaceProtocol` with the clinical/facial skin
  dropped — applies to any two-thing comparison where one side is the
  "answer" (an ingredient comparison, a before/after, a competitor split).
  See `catalog/visual-components/split-compare/README.md`.
- **SeoulHabitSkin channel branding** — `brand/channel/` now ships real,
  pixel-exact PNG exports (`avatar-800.png`, `banner-2560.png`,
  `watermark-150.png`), not just HTML source — see that folder's own README
  for how they're produced and regenerated. The banner's macro-plate photo
  was generated (`generate_image`, `marketing_studio_image`) and composited
  in as a real `<img>`, replacing an earlier placeholder.
- **`faceless-video-craft` skill** — added a dedicated *The captions*
  section (previously three sentences buried in an audio-mixing bullet),
  a *Consistency across a channel's videos* section, and a publish-envelope
  completeness check in the verification loop. See
  `.claude/skills/faceless-video-craft/SKILL.md`'s own diff for the full
  reasoning — it was driven by gaps found in this repo's own video catalog.
- **Two visual components harvested into `catalog/visual-components/`**,
  found by reviewing every shipped composition's HTML for recurring
  patterns never added to the shared catalog:
  - **TermDefinition** — a full-frame term/definition hero card, built
    independently five separate times (four `skincare-glossary-part-*`
    videos + `skincare-ingredient-glossary`) with identical class names and
    tokens, never once shared. The single strongest harvest candidate found.
  - **ThresholdList** — generalized from `kbeauty-one-percent-line`'s "1%
    Line" scene (a ranked list split by a cutoff line) into a reusable
    above/below-threshold mechanism.
  - A real bug was found and fixed in the TermDefinition spike during
    verification (two cards' index labels visible simultaneously — a
    missing `t=0` timeline baseline, the same root cause the
    faceless-video-craft skill's own failure-modes list already names for a
    different case) — see that component's own file comments.
  - See `catalog/README.md`'s "Considered and not harvested" note for
    patterns reviewed and declined (`.cta-chip`, `.trick-fan-chip`,
    `.htu-word`, the `hook-bottle-*` icon), with reasoning.
- **`catalog/index.html` redesigned** — the gallery previously treated every
  entry as a uniform "card + load-preview button," which hid the thing that
  actually matters now that the catalog holds real components, not just
  images: whether an entry has a data contract and a time axis at all.
  Cards now carry two explicit axes — **kind** (component / static
  composition / mark / photography / linked) and, for components, **control**
  (`⏱ clock` deterministic-and-seekable, `◧ select` a discrete prop,
  `⚠ none` no scrub interface — flagged per-card when that's because the
  component isn't render-safe, e.g. Celestial Arc's autoplaying CSS
  `@keyframes`, not just because it's early-stage). Duration and a short
  field contract are shown before loading anything. Loading a
  `debug`-gated component now auto-appends `?debug=1` — previously
  RoutineLadder's scrubber was invisible in the gallery unless you already
  knew that query param existed, so the component looked like a frozen
  image even though it's fully seekable. Photography (the 25-still
  ingredient set + 12-scene product set, 37 total) is now in the gallery at
  all — it wasn't before — rendered as real inline thumbnails rather than
  an iframe-loading button, since there's nothing to scrub. One real bug was
  found and fixed while verifying the rebuild: an unescaped literal
  `<select>` in a description string got parsed as a real HTML tag, silently
  nesting the next two cards inside GradedScale's card instead of as
  siblings — caught by comparing `grid.children.length` against the actual
  title count, not by eyeballing the render.

## Active video projects

| Project | Current render | This session |
|---|---|---|
| [peeling-not-progress](videos/peeling-not-progress/) | `renders/peeling-not-progress_FINAL_mastered.mp4` | New project — first genuinely silent (no VO) video on the channel; 30s claim-audit short (peeling ≠ progress), real PubMed/CFR/FDA sourcing corrected two lines that said the opposite of the regulator, barrier-wall SVG harvested to `catalog/visual-components/barrier-wall/` as its third independent build in this repo, real `--p`-custom-property render bug found and fixed via frame-exact pixel verification |
| [kbeauty-one-percent-line](videos/kbeauty-one-percent-line/) | `renders/kbeauty-one-percent-line_2026-08-29_21-40-00.mp4` | Hard-cut scene transitions, VO-synced cadence fixes across Frames 4-8, retimed hook payoff, ingredient macro-shot interlude (Frame 4b), first YouTube thumbnail set |
| [retinol-patch-test](videos/retinol-patch-test/) | `renders/retinol-patch-test_2026-08-29_23-00-57.mp4` | YouTube feedback round 2 (bottle bounce-in, camera-punch on "Stop!", spring-pop callouts, compressed ladder draw), frame-zero + img-attribute skill-compliance fixes, YouTube thumbnail set |
| [seoulhabit-launch](videos/seoulhabit-launch/) | (render unchanged this session) | YouTube thumbnail set; QA verification snapshots from retiming/hook-check rounds kept as working history |
| [snail-mucin-truth](videos/snail-mucin-truth/) | `renders/snail-mucin-truth_2026-08-29_07-21-10.mp4` | Retimed SFX cues across the caption/frame tracks to match real VO pacing |
| [snail-mucin-medical-secret](videos/snail-mucin-medical-secret/) | (render unchanged this session) | Three YouTube thumbnail concepts explored (medical-secret / yuck-factor / mad-science), not yet chosen |

### New per-project assets this session

- **kbeauty-one-percent-line** — source photography (`assets/images/hook-bottle-photo.png`, `loop-centella-leaf.png`, `loop-water-droplet.png`); thumbnail set (`assets/thumbnail/`: hook-frame source+graded, 3 candidates each with source+final, `thumbnail-final.png`)
- **retinol-patch-test** — thumbnail set (`hook-stop.png`, `powerful-stakes.png`, `safety-stop-card.png`, `thumbnail-final.png`); regenerated voice word-timing sidecars + transcript
- **seoulhabit-launch** — thumbnail set (`hook-frame-source.png`, `hook-frame-graded.png`, `thumbnail-final.png`)
- **snail-mucin-medical-secret** — 3 thumbnail options, each an HTML source + rendered PNG

## Removed this session

Per creator instruction — no longer needed:

- `videos/pdrn-skin-regeneration/`
- `videos/red-ginseng-two-routes/`
- `videos/snail-mucin-glass-skin/`

(Full history remains recoverable from git — e.g. `git log --all -- videos/pdrn-skin-regeneration`.)

## Other video projects in this repo (untouched this session)

- `skincare-ingredient-glossary` (created 2026-08-27)
- `skincare-glossary-part-1-barrier-repair` (created 2026-08-28)
- `skincare-glossary-part-2-hydration-boosters` (created 2026-08-28)
- `skincare-glossary-part-3-glow-brightening` (created 2026-08-28)
- `skincare-glossary-part-4-texture-anti-aging` (created 2026-08-28)

## Shared catalog library (`catalog/`)

Reusable, pre-vetted assets referenced across video projects — check here
before generating or licensing new plates (see root [CLAUDE.md](CLAUDE.md)):

- `ingredient-photography/` — macro ingredient stills, tracked in `manifest.json`
- `product-photography/` — fictional K-beauty product photography (see that folder's own manifest + README for the generation/verification log)
- `visual-components/` — reusable HyperFrames components: `evidence-meter/`,
  `graded-scale/`, `split-face-protocol/`, `dawn-to-dusk-routine/`,
  `routine-ladder/`, `celestial-arc/`, `term-definition/`, `threshold-list/`,
  `split-compare/` — see `catalog/README.md` for what each one is and its
  provenance
- `marks/` — standalone graphic marks
- `ingredients/one-percent-line/` — production record for the kbeauty-one-percent-line video (render history, catalog-imagery usage, authorizations)

## Channel branding (`brand/`)

- `brand/channel/` — SeoulHabitSkin YouTube channel branding kit (avatar,
  banner, watermark, About-section copy), built from VidIQ competitor/keyword
  research and extending the existing SeoulHabit Video Design System rather
  than a new identity. See that folder's own README for the asset list, the
  QA harnesses kept as working history, and two real contrast/layout bugs
  found and fixed during verification.

## Tooling / config added this session

- `.claude/skills/faceless-video-craft/SKILL.md` — repo copy of the video-authoring skill, kept in sync with the active session copy
- `CLAUDE.md` — instructs future sessions to check `seoulhabit/storyboard-review` (this repo) for existing sourced imagery before generating or licensing new plates
