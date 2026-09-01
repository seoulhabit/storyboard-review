---
workflow: faceless-explainer
flow: automation
storyboard: yes
message: "Peeling is a reaction, not proof a product is working — the useful question is what changed (ingredient, strength, frequency, or combination), not whether skin is flaking."
destination: shorts
aspect: 1080x1920
language: en
audience: "skincare-curious viewers stacking actives (retinol, AHA/BHA, exfoliating toners) who read visible peeling as evidence of progress"
length: 25s
angle: format-pilot / claim-audit
VO_MODE: silent
style_preset: seoulhabit-evidence-green
series: "A Question We Marked Open"

## Intent

Creator-supplied, second-by-second brief for the pilot of a new recurring format,
**"A Question We Marked Open"**: pose a claim as a question, stamp a short answer,
separate the folk reasoning from the evidence, name the evidence's real tier, draw
the actual safety boundary, and hand the viewer a better question instead of a
subscribe card. This video's specific question is "Is peeling proof that skincare
is working?" — the same conclusion `videos/peeling-not-progress/` already shipped
(30.1s, ink/paper/aqua palette, barrier-wall diagram), but this build is a
**different treatment in a new visual language**, not a rebuild. `peeling-not-progress`
is untouched by this project.

Four decisions were made explicitly with the creator before build, via
`AskUserQuestion`, because the repo had real precedent and real constraints
pointing in different directions on each:

1. **Scope: new project alongside, not a rebuild.** `videos/peeling-question-open/`
   is a separate folder. The existing 30.1s video stays as-is; this is the format's
   pilot, reusing the same verified sources rather than re-deriving them.
2. **Narration: silent**, matching the predecessor's precedent — on-screen kinetic
   type carries the language, BGM + stamp/glass SFX carry pacing. No `<hf-audio-group
   id="voiceover">` bus, no `data-fx-carve` duck.
3. **Imagery: browser-drawn only (CSS/SVG), no generated plates.**
   `catalog/product-photography/README.md` blocks generative imagery from HyperFrames
   compositions without a filed decision record; staying browser-drawn avoids needing
   one. The frosted-glass panel is a proven pattern (`videos/centella-tiger-grass`,
   `backdrop-filter: blur(25px) saturate(1.15)`, shipped across 7 renders) — not a new
   render-safety risk, just a new use of an existing one.
4. **Duration: hold 25s as briefed**, under the channel's own 28–45s standard
   (`REPORT.md`). Recorded here rather than silently padded: the brief's six beats
   are tight and specific; adding runway would mean either slowing the format's own
   pacing (working against the "stamp, don't linger" register the brief asks for) or
   padding with decorative motion, which the skill explicitly treats as a defect
   class of its own. A sub-28s short with a hard loop is a legitimate shape for a
   pilot; if the format continues past this pilot, later entries can re-open the
   duration question with real audience-retention data behind it.

## Sourcing

Two citations, both verified live before build (not carried over from the
predecessor without a check, even though the underlying facts overlap):

- **Griffiths CE et al., 1995, *Archives of Dermatology*** (PMID 7544967) — 48-week
  double-blind trial (n=99): more visible irritation from a retinoid did not
  correlate with better clinical outcomes. Reused verbatim from
  `peeling-not-progress/frame.md`'s sourcing log, where it was already vetted.
  Rendered on screen as `Arch Dermatol · 1995`.
- **American Academy of Dermatology**, "How to maximize results from anti-aging
  skin care products" —
  https://www.aad.org/public/everyday-care/skin-care-secrets/anti-aging/maximize-anti-aging-products
  — fetched and read directly for this build. Exact sentence: *"Stop using a
  product that stings, burns, or tingles. These sensations mean that the product
  irritates your skin."* with the caveat *"If you are using a product prescribed
  by your dermatologist, ask if this should be happening before you stop using
  it."* Both the stop-instruction and the prescription caveat are represented on
  screen in scene 5. Rendered as `AAD guidance`.

## Evidence-vocabulary note

The brief's scene 4 asks for "EVIDENCE LABEL: Established." The shared catalog's
existing evidence vocabulary is `catalog/visual-components/evidence-meter/`'s
`QUALIFIED` and `catalog/visual-components/graded-scale/`'s strict 1–5 integer
enum — introducing a third tier word risks the channel-level vocabulary drift the
skill warns about. Kept the brief's word (it is the client's actual language for
this format) but rendered it as a stamped ink-on-frosted-glass mono label with a
`--leaf` rule beneath, not a filled green success badge — honoring GradedScale's
"no success color" rule even though this component doesn't use GradedScale
itself. Flagged for the catalog entry as a reconciliation follow-up, not silently
decided.

## What this reuses vs. builds new

Reused verbatim: 4 fonts, BGM bed, 4 QC scripts (the `mugwort-healing-herb`
evolved set), 6 SFX cues — see `frame.md` for exact source paths. Adapted
mechanism, not skin: the `04-boundary.html` two-card verdict pair (source for
scene 5), the `06-payoff.html` loop-endpoint pattern (source for scene 6), the
`centella-tiger-grass` frosted-glass card (source for every panel in this
project), the catalog's `tl.set(..., 0)` seek-safety baseline, and the
`threshold-list` stamp-impact ease. Built new: the peeling-film mechanism
(nothing like it exists in the repo — the nearest neighbor, BarrierWall's
wash-descends-and-shards-detach, is SVG and a different subject), the
green-ground evidence-card treatment, and the format's own beat structure.
