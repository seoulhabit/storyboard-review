# COMPILER.md — the compiler contract

Written before any compiler code, per this WO's own `T2` acceptance rule: a
reviewer must be able to read this file and predict the output file tree
for a T1 beat sheet without running anything. §6 is that worked example.

## 0. Provenance and what has already changed from the WO's own text

The design system this compiler targets is Claude Design project
`a7945a95-da21-4823-8b16-57c6ffa11558`, extracted 2026-09-06 (`EXTRACTION.md`,
`MANIFEST.json` — 64 files, sha256 per file, zero mismatches on re-check).
It carries no version string; the manifest is the version anchor.

Four corrections to the WO's own T2/`COMPILER.md` spec, found against the
real source and the real engine, all logged in `docs/wo/WO-FVC-005.md` §8:

1. **No shader path.** `T1-FINDINGS.md`'s F1 resolved PARTIAL under this
   session's zero-HeyGen-spend ruling, firing rule **`C-6`**: hard cuts
   only, no contiguous shader chain, anywhere. The WO's original §4.2 named
   a shader rule ("at most one contiguous chain… `cross-warp-morph`
   default"); this compiler implements none of it. See
   `RETIRED-transitions.md` for the preserved mechanism if `C-6` is ever
   reversed.
2. **Fonts are frozen and root-relative by default, not base64-inlined.**
   Base64 is legal per the installed engine (`base64_media_prohibited`
   matches only `data:audio/` and `data:video/`, confirmed against
   `hyperframes@0.8.30`'s own `cli.js`), but this compiler emits
   sub-composition-per-scene, and inlining ~2.4 MB of font payload into
   every one of a ~50-scene compile (kbeauty-scale, see §2) would be pure
   waste. `--inline-fonts` remains available for single-file deliverables.
   See `fonts/SOURCES.md`.
3. **One duration ceiling for every canvas; the compiler splits an
   over-cap scene rather than refusing it or inventing a second ceiling
   for long-form** (this session's ruling `D5`). §2 below is the split
   arithmetic, worked against a real case: `T6.json`'s own steps chapter
   runs 6.0s in the design system's reference cut, over the 5.0s
   non-evidence/compare cap.
4. **Scene visibility is the HyperFrames engine's job, not GSAP's.**
   Confirmed this session by reading the installed engine's own runtime:
   it writes `visibility` on every `[data-start]` element at each seek.
   The compiler never emits a tween that shows or hides a `.clip` element
   — `gsap_animates_clip_element` is a hard lint error for exactly that,
   and the engine's own fix hint prescribes the inner-wrapper split this
   compiler already uses (§3).

## 1. Inputs

Exactly three, all read-only:

- `videos/<slug>/03-beat-sheet.json` — the schema at
  `claude-skills/faceless-video-craft/assets/beat-sheet.schema.json`, plus
  three compiler/caster-only optional fields the frozen schema does not yet
  declare: `scene.component` (one of the twelve `Sh*` names, or explicit
  override) and `scene.slots` (the named props that component's
  `.props.json` contract requires). When `scene.component` is absent, it is
  resolved from `scene.section` against the chosen `templates/T*.json`
  spine. *(WO-FVC-007 T3, 2026-09-07)* The third field, `scene.purpose`, is
  new and belongs to the S4.5 stage, not this compiler directly: a
  `catalog-registry.yaml` purpose key (`claim_vs_evidence`, `svg_diagram`,
  `checklist`, `editorial_imagery_broll_wrapper`, or one of the
  `furniture_*` roles — see `videos/_system/catalog/catalog-registry.yaml`)
  that `scripts/cast_scenes.py` resolves into a real `scene.component` +
  `scene.slots` skeleton *before* this compiler ever runs, by looking the
  purpose up in the registry (R-9: "casting is data"). A beat sheet that
  already sets `scene.component` explicitly (the `Sh*` path above) skips
  S4.5 entirely — `purpose` and an explicit `component` are alternatives,
  never combined. **This compiler's own `CANONICAL_COMPONENTS` gate
  (`compile_composition.py:255-256`) still `die()`s on any component name
  outside the twelve `Sh*` names** — casting a scene against the catalog
  registry does not yet mean this compiler can render it; that gate has not
  been extended to accept a retrofitted catalog component, and doing so is
  not scoped to T3. See `wo/FVC-007/T3-REGISTRY-AND-CASTER-REPORT.md`.
- `videos/_system/` — this design system: tokens, 12 components, 6
  template spines, fonts, vendored GSAP. Checked against `MANIFEST.json`
  at the start of every compile; a hash mismatch on any tracked file halts
  with a named diff, never a silent proceed.
- `videos/<slug>/04-assets/` — VO audio, music bed, and (currently unused —
  the design system forbids imagery by rule) any plate.

## 2. The timing rule, as arithmetic

```
reading_floor(words) = max(1.6, words / (150/60))
  # 1.6s = the design system's own per-element hold floor (tokens/motion.css
  #   --m-hold-min). 150 wpm is this repo's existing channel default
  #   (videos/_channel/baseline.yaml, and makemeavideo's own V-1 rule) —
  #   a CHOICE, stated as one, not a measurement. The nearest measured
  #   neighbour in this repo is catalog/tooling/check-vo-pace.py's
  #   MAX_WPM=210, which is spoken pace, not scan-read pace, and is not
  #   substituted here without a ruling.

D_raw   = max(vo_duration_s + 0.30, reading_floor(slot_words))
ceiling = 8.0 if component in {ShEvidence, ShCompare} else 5.0
```

**If `D_raw <= ceiling`:** the scene compiles as one sub-composition,
`data-duration = D_raw` (rounded to 3dp, the fixed-precision contract kept
from `beats_to_composition.py`'s `f()`).

**If `D_raw > ceiling` (rule D5 — the compiler splits, it does not
refuse):** the beat sheet's own `beats[]` array (each carrying an `offset`
into the scene) is partitioned into the fewest contiguous groups such that
each group's EFFECTIVE duration — from its own first beat to the *next*
group's first beat, or to the scene's own end (`D_raw`) for the final
group — is `<= ceiling`, preserving beat order. This is deliberately not
"each group's own beat span `<= ceiling`": a first implementation did
exactly that and **died on a real compile** with a misleading "beats too
widely spaced" error, because three beats spanning only 4.0s inside a 6.3s
scene fit comfortably as one group *by their own span* while the scene's
trailing hold (the time after the last beat, needed for `vo_duration_s` or
the reading floor) pushed the group's real duration to 6.3s — over the
5.0s ceiling. The fix accounts for the scene's own end explicitly: the
final group is peeled down, one beat at a time from the back, until what
remains actually fits against `D_raw`. Each group becomes its own
sub-composition, id-prefixed `<parent-cid>-<n>` (1-indexed), so a frame
always traces back to one authored scene. Splitting is **deterministic**:
recompiling an unchanged beat sheet always yields identical boundaries —
the partition algorithm has no randomness and no wall-clock input.

**Content, not just timing, must split too.** A scene's `slots` describe
what the component renders; splitting `beats[]` alone does nothing to the
content, and a first implementation shipped exactly that gap — both
compiled halves of a split `ShRows` scene rendered the *identical, full*
row list, discovered by actually inspecting the compiled HTML. Content
splitting is possible **only** for components with a natural per-beat
list slot, where each item corresponds 1:1, in order, with the scene's own
beats: `ShRows.rows` and `ShSteps.steps`. For those, each split group
renders `items[lo:hi]` sliced to its own beat-index range, and `ShRows`'s
`active` row index is relocated to the containing group's local index (or
set to `-1` if the active row fell in a different group). Every other
component — a single hook line, one ingredient card, one figure, one
claim, one comparison — has no defined notion of "half of itself", and the
compiler **refuses** rather than guess: a scene using any component
outside `{ShRows, ShSteps}` that needs a D5 split dies, naming the
component and why.

**Worked example, this exact case, verified against a real compile and
render, not asserted** (a fixture mirroring `templates/T6.json`'s own
reference cut: `ShRows`, three beats at offsets 0.0/2.0/4.0, a scene whose
derived duration is 6.3s against the 5.0s ceiling `ShRows` gets as a
non-evidence/compare component): the partition puts beats 0 and 1 (offsets
0.0, 2.0) in group 1 — its effective duration runs to group 2's first beat
at 4.0s minus... no: to its own end via the tail rule below, landing at
4.000s — and beat 2 (offset 4.0) alone in group 2, whose effective
duration is `D_raw` (6.3) minus its own start (4.0) = 2.300s. Group 1
compiles to `<parent>-1` rendering rows `[0:2]` (both non-active, full
opacity); group 2 compiles to `<parent>-2` rendering `rows[2:3]` with the
scene's own `active: 2` relocated to local index `0`. Compiled, this
passed `hyperframes lint` (0/0), `hyperframes check --at-transitions` on
9x16 (`ok: true`, all five categories `errorCount: 0`), and a real local
render: 6.300s exactly, two visually distinct frames (the first showing
Sebum/Down and Barrier/Repaired in ink; the second showing Pigment/Blocked
correctly in clay) — see `wo/FVC-005/t3-verification/d5-split/`.

**Entrance-stagger interaction, stated rather than glossed over:** the
design system's own 0.8s row stagger cannot hold at the 5.0s ceiling for
more than roughly three rows (a 4-row scene needs D >= 5.70s to have its
last entrance finish by 50% of scene duration, per the arithmetic below).
The compiler **derives** the stagger rather than asserting the source's
0.8s figure, and errors — does not silently clamp — when the derived value
falls under 0.25s:

```
last readable element finishes entering by 0.5 * D
  => enter_offset + (N-1)*stagger + 0.35 <= 0.5*D
  => stagger = (0.5*D - enter_offset - 0.35) / (N-1),  must be >= 0.25
```

This means the compiled artefact's rhythm will sometimes differ from the
design system's own stated 0.8s figure. That is disclosed here and in the
compile report, not hidden — see "Known conflicts" in the WO plan.

## 3. Attribute vocabulary — engine attributes vs. the retired IR

Two vocabularies, on two different elements, per scene, confirmed against
the installed `hyperframes@0.8.30` engine this session (not carried from
memory):

| Element | Attributes | Who reads them | Never |
|---|---|---|---|
| `<template>` sub-composition root, `id="root"`, styled only via `#root` | `data-composition-id`, `data-width`, `data-height`, `data-duration` | **engine** | class-based styling (`subcomposition_root_styled_by_class` is a hard error) |
| Parent's `<div class="clip" data-composition-src="…">` mount point | `data-start`, `data-duration` | **engine** — writes `visibility` on this element every seek | any GSAP tween touching `visibility`/`display`/`opacity`/`autoAlpha` here (`gsap_animates_clip_element`, hard error) |
| Inner non-clip wrapper inside the sub-composition | `data-scene` (annotation only), `data-enter`/`-float`/`-sweep`/`-sh-count`/`-sh-strike` (annotation only — `MOTION.md`'s IR) | nothing at render time; a human reading the file | — |

`data-track-index` is **omitted entirely** — confirmed this session that
`timeline_track_too_dense` skips any element lacking it, and
`hyperframes docs data-attributes` states the render never reads it.

Every sub-composition emits its **own** `@font-face` block for every family
it uses (`font_family_without_font_face` is an error, evaluated per file —
confirmed against the installed engine). GSAP is **not** re-declared per
scene: sub-compositions inherit it from the host, confirmed this session.

## 4. Asset rules

- **Fonts**: root-relative `url("assets/fonts/<name>.woff2")` from each
  sub-composition, copied once per project from `videos/_system/fonts/` —
  never `../fonts/` (a `../` traversal is `invalid_parent_traversal_in_asset_path`,
  a measured trap from `videos/ectoin-normal-person/scripts/_preamble.py`).
  `videos/_system/tokens/fonts.css`'s own `../fonts/` paths are relative to
  *that file's position in the source tree*, not the render output — the
  compiler rewrites them at emit time; this is stated so the source path is
  never mistaken for the final one.
- **GSAP**: vendored once at `videos/<slug>/06-render/<canvas>/vendor/gsap-3.14.2.min.js`
  (byte-identical to `videos/ectoin-normal-person/assets/vendor/gsap-3.14.2.min.js`,
  confirmed this session — sha256 `c174bfce…`), referenced from the root
  only.
- **Audio**: real files, never base64 (`base64_media_prohibited` is a hard
  error on `data:audio/`, confirmed against the installed engine's own
  regex this session). Root-relative from `04-assets/`.
- **Images**: none. The design system forbids imagery by rule
  (`readme.md`: *"no photography, no gradient, no texture, no pattern and
  no video underlay anywhere in the system"*). If a future template
  introduces one, that is a ruling, not a compiler default — the compiler
  refuses an `image_ref` field it does not recognise rather than guessing
  a treatment.
- **Brass is never a text `color`.** Measured this session: `#C0A265` on
  cream is 2.10:1, which fails even the engine's own large-text 3:1 floor
  (`fontSize >= 24` qualifies as large; every SeoulHabit type step does).
  The emitter layer (§6) makes this a codegen invariant, not a lint hope.

## 5. Outputs

Per format (`9x16` and/or `16x9`, per `request.yaml`'s `formats:` — see
`videos/_channel/baseline.yaml` for the channel default):

```
videos/<slug>/06-render/<canvas>/
  index.html                       root composition; scene mounts as .clip
  index.motion.json                one composition-wide keepsMoving + per-scene assertions
  vendor/gsap-3.14.2.min.js
  assets/fonts/*.woff2             copied from videos/_system/fonts/
  assets/vo.wav, assets/bed.mp3    copied/referenced from 04-assets/
  compositions/frames/NN-<id>.html one <template> per compiled scene
                                    (NN-<parent>-<k>.html for a D5 split)
  compile-report.md                every derived duration, every derived
                                    stagger, every D5 split, every warning
```

`compile-report.md` exists because a warning that scrolls past in a
terminal is not a ledger line — this is the same discipline
`beats_to_composition.py`'s own `WARNINGS` list and run-summary reprint
already enforce, kept verbatim.

## 6. Predicting the output tree from a T1 beat sheet — the acceptance test

Given `03-beat-sheet.json` with `format: "short"`, `canvas: 9x16`, and five
scenes whose `section` values are `hook, define, mechanism, evidence, cta`
(matching `templates/T1.json`'s own `sequence`), and assuming none of the
five scenes exceeds the 5.0s/8.0s ceiling (no D5 split fires):

A reviewer reads off, **without running anything**:

- `templates/T1.json`'s sequence resolves `hook -> ShHook`,
  `define -> ShIngredient`, `mechanism -> ShRows`, `evidence -> ShEvidence`
  (anchor), `cta -> ShEndcard` (anchor).
- `06-render/9x16/index.html` contains exactly 5 `<div class="clip"
  data-composition-src="compositions/frames/…">` mounts, `data-start`
  cumulative from 0.0 with no gaps (scenes tile — the one invariant kept
  unconditionally from `beats_to_composition.py`'s `validate()`).
- `compositions/frames/` contains exactly 5 files:
  `01-hook.html`, `02-define.html`, `03-mechanism.html`, `04-evidence.html`,
  `05-cta.html` (the `scene_filename` rule, kept verbatim: 1-indexed,
  zero-padded to 2, slug from the scene id).
- `index.motion.json` contains exactly one `keepsMoving` (composition-wide,
  on `#root` — confirmed this session that a per-scene `withinSelector`
  reports off-screen time as false-frozen) plus one `appearsBy` and one
  `staysInFrame` per scene (5 each), plus one `before`/`after` timing
  assertion per adjacent scene pair (4).
- `01-hook.html` (scene 0) carries **no** `data-enter` on any readable
  element — the frame-zero rule: an entrance with an offset means frame
  zero is blank, which fails both the WO's own "frame zero must be the
  hook, fully dense" line and `catalog/tooling/check-blank-frames.py`'s
  frame-zero tag. Scene 0's motion comes only from `data-float`/`data-sweep`,
  both non-zero at t=0.
- Every file under `compositions/frames/` carries its own `@font-face`
  block for exactly the families it uses (§3) and its own `<script>` tag
  building and registering a paused timeline **synchronously** — no
  `DOMContentLoaded` listener anywhere (`MOTION.md`'s defect-2 fix).
- If any of the above is not predictable from the beat sheet and
  `templates/T1.json` alone, the template is underspecified and the fix is
  in `T1.json`, never a Python special-case.

## 7. Refusals — the compiler dies, it does not warn and proceed

- A beat-sheet timeline that does not tile (gap or overlap between scenes).
- A scene whose derived duration exceeds the ceiling **and** cannot be
  split without a group falling under 0.15s (too few beats to divide).
- A slot's text exceeding its `.props.json` `maxWords` at either canvas
  (checked before rendering, never discovered as `text_box_overflow` later).
- `scene.component` naming anything outside the twelve `Sh*` names.
- Any attempt to set `color` to the brass token on a text element.
- More than one clay element resolved in a single scene.
- More than two type steps resolved in a single scene.
- A `MANIFEST.json` hash mismatch against the live `videos/_system/` tree.
