# Request to Claude Design — imagery ruling + long-form runtime, for `pdrn-left-the-clinic`

**From:** `makemeavideo` run, slug `pdrn-left-the-clinic`, 2026-09-07
**To:** the SeoulHabit Video Design System project (`a7945a95-da21-4823-8b16-57c6ffa11558`)
**Why now:** the first brief this pipeline has received whose story cannot be told
by the system as it stands today. Per this project's own `readme.md` —

> "If imagery is ever introduced it will need a ruling... it becomes component
> eleven **with a written spec**, not a one-off."
>
> "If you find yourself changing something in the first list to make a video
> work, the video is wrong, not the system."

This document is that written spec, plus the runtime question the same brief
raises. It asks for two rulings and, if the first is granted, five component
specs to review.

---

## A1 — The imagery ruling

The brief is "The Viral Ingredient That Left the Korean Clinic" (PDRN). Its
story arc is told entirely through *place and object*: a serum bottle in
darkness, a camera push through the bottle into strands of DNA, a Korean
dermatology clinic, an Olive Young retail aisle, a beneath-skin-vs-on-top
diagram, a freeze-frame on marketing imagery with warning labels stamped over
it, a bottle and a syringe side by side.

**None of it is buildable today.** This system's own readme is explicit and
absolute:

> "**No imagery.** The system is typographic by design — cream ground, no
> footage behind the hook, no faces, no illustration."
>
> "There is no photography, no gradient, no texture, no pattern and no video
> underlay anywhere in the system."
>
> "**Never:** ... more than one clay element in a scene." (implicitly: no
> photographic subject at all — the ten shipped components are text, list,
> comparison and card layouts, nothing that holds a drawn or photographic
> object)

This is not a gap this WO's extraction introduced. `EXTRACTION.md` on the
compiler side confirms the same read: every file that could plausibly carry
imagery (`assets/`, `avatar/`, `screenshots/`, `ui_kits/`) was deliberately
left unextracted as "Claude Design authoring/preview infrastructure," not
because it held unused imagery primitives.

**The ask:** rule, explicitly, one of:

1. **Extend the system** — accept the five component specs below (§A2) as
   component eleven onward, each with the same rigor as the shipped ten
   (props contract, clay budget, safe-area behavior, determinism contract).
2. **Decline** — hold the system to its typographic identity. In that case,
   per the readme's own words, *the video is wrong, not the system*: this
   run re-expresses every beat on the nine existing emitters instead (see the
   typographic beat sheet in `videos/pdrn-left-the-clinic/00-decision-ledger.md`
   for exactly how), and this request is filed as a standing, named gap for
   any future brief that needs cinematography rather than as a blocker on
   this one.

Either answer closes this request. What is not sanctioned is a third path —
inventing an imagery workaround inside a single run without this ruling.

---

## A2 — Component specs (only if A1 rules "extend")

Written in the shape of the shipped `.prompt.md` + `.d.ts` pairs, so they can
be reviewed and, if accepted, authored the same way `ShHook` or `ShRows` were.

### `ShPlate` — a held subject
A single subject (bottle, syringe, sealed serum pack) held in frame on the
cream ground, lit as a product photograph would be but rendered as flat
illustration/vector, never a photographic asset (`readme.md`'s "no
photography... anywhere" stays true; this is a drawn plate, not a plate).
- Props: `subject` (name, for the a11y layer), `orientation`, `accent`
  (whether the plate itself carries the scene's one clay element, e.g. a
  clay cap or clay label swatch)
- Clay budget: the plate may carry the scene's one clay element, or none —
  never two
- Safe area: same reserved zones as every other component (9:16 15% right
  rail / 18% top / 24% bottom; 16:9 6%/8%/10%)
- Determinism: static geometry, no procedural generation — a `data-start`
  seek must render pixel-identical output every time, same as every
  existing component

### `ShTransform` — one subject becoming another
The bottle-to-DNA beat: subject A morphs into subject B along a single
deterministic path (scale, opacity crossfade, or a path-morph if SVG-based).
- Props: `from`, `to`, `holdStart`, `holdEnd` (seconds each subject holds
  static before/after the transform)
- Explicitly **not** `--m-shader`/`cross-warp-morph` — ruling `C-6` in this
  WO forbids the one shader the source design ever specified, hard cuts only.
  This is a plain, deterministic GSAP-timeline crossfade/morph, not a shader.
- Clay budget: one element, same rule
- Determinism: seek to any `t` mid-transform must render the correct
  interpolated frame, not a snap to the nearest keyframe

### `ShPlace` — an establishing interior/context scene
The clinic interior, the Olive Young aisle. A flat, typographic-illustration
establishing shot — walls, a counter, a shelf silhouette — never a
photograph, never a face (this system's "no faces" rule is absolute and
crosses over unchanged).
- Props: `place` (name), `depthCue` (a simple layered-plane parallax, or none)
- Clay budget: one element (e.g. one product silhouette picked out in clay)
- Safe area / determinism: as above

### `ShDiagram` — the beneath-skin vs on-top boundary
The single most important visual in the brief: PDRN delivered beneath an
intact skin barrier vs. sitting on top of it. This is the evidence-boundary
beat the whole video turns on.
- Props: `layers` (named, e.g. `["stratum corneum", "epidermis", "dermis"]`),
  `deliveryPoint` (which layer), `intact` (boolean — draws the barrier as
  continuous or breached)
- **Must not borrow chart grammar.** `K-2`'s illustration rule is explicit:
  "it may not borrow chart grammar — no axes, gridlines, or plotted points
  implying a measurement that does not exist." This is a cross-section
  drawing, not a data visualization — no axis labels, no numeric scale
- Renders with the `[Authored, illustrative — not a claim]` tag per `K-2`
- Clay budget: one element (e.g. the delivery point marker)

### `ShAnnotate` — the freeze-and-label marketing sequence
The 3:10–3:50 beat: an animated marketing sequence freezes, and warning-style
labels stamp over the frozen frame.
- Props: `frozenAt` (seconds into the parent scene where the freeze happens),
  `labels` (array of `{text, position}`)
- The label styling reuses `ShChip`'s existing "unsourced flag" visual
  grammar (muted ink, never the accent colour, per `K-2`(2)) rather than
  inventing a second warning-label language
- This component **wraps** another component's frozen final frame rather
  than rendering its own subject — needs a ruling on whether that
  composition pattern (component-wrapping-component) fits the system's
  existing `ShScene`-wraps-everything convention, or needs its own contract

**Every spec above inherits, unchanged:** the six fixed colour tokens, the
two type families, "no shadows... no transparency or blur," "no icon font...
no emoji, ever," the one-clay-element-per-scene rule, and the safe-area
zones. None of the five specs proposes touching anything in the system's own
"fixed, changes only by explicit ruling" list.

---

## A3 — The long-form runtime question

Separate from imagery: `templates/T6.json` (Long-form Explainer) declares
`chapters_min: 4`, `chapters_max: 6`. At the compiler's own per-scene
ceilings — 5.0s standard, 8.0s for `ShEvidence`/`ShCompare` (rule D5) — six
chapters plus one close sequence lands near **3:00–3:30** even with D5's
scene-splitting arithmetic applied generously. The pipeline's own `S-2` rule
targets long-form at **4:00–12:00**, and this brief's runtime (4:55) sits
inside that clamp and outside T6's own declared chapter ceiling.

`chapters_max` is enforced by no gate today — this is a live contract
mismatch, not yet a hard failure, which is exactly why it should be ruled
rather than silently exceeded or silently truncated.

**The ask:** what does this system need to carry a 4:55 runtime cleanly?
Options, not a recommendation — this is Design's call, not the compiler's:

1. Raise `chapters_max` (say, to 9–10) if the six-artboard reference cut was
   a starting point rather than a hard ceiling
2. Add a longer chapter variant/template for stories with more beats than
   T6's four-slot chapter sequence (`hook → quote_or_define → steps_or_rows
   → evidence`) comfortably carries
3. Rule that 4:55 is itself wrong for this system and the story should be
   cut to fit six chapters (~3:00–3:30) instead

Whichever is ruled, the compiler-side artifact (`00-decision-ledger.md` in
this run) will record it as an amendment to `T6.json`, the same way ruling
`R-6` was recorded as an `amendments[]` entry against the safe-area tokens.

---

## A4 — Drift found while preparing this request (reported, not actioned here)

- The brief's file list (`_ds_manifest.json`, `_ds_bundle.js`, `styles.css`,
  `SKILL.md`, `_adherence.oxlintrc.json`, `thumbnail.html`, `avatar/`) is
  real — every one of those files exists in this project. But the compiler's
  own `EXTRACTION.md` records each as **deliberately not extracted**,
  because none of it is consumed by `compile_composition.py` — they are
  Claude Design's own authoring/preview infrastructure. Nothing is missing;
  the brief and the extraction disagree on purpose, and the extraction's
  reasoning is sound (a prototyping-skill SKILL.md and a lint config for
  *this* project are not inputs the video compiler should read).
- The brief names this system "v5.0." No version string exists anywhere in
  this project — confirmed again this pass. `MANIFEST.json`
  (project id + `updatedAt` + a sha256 per extracted file) remains the only
  version anchor; "v5.0" should not be repeated in future briefs.
- G0-1 (which of the two identically-named Design projects is canonical) is
  **confirmed**, not open — `a7945a95-…` matches this brief's own URL and
  every component/palette/template name the compiler's Gate 0 sheet expects.
