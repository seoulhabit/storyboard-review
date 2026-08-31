---
workflow: faceless-explainer
flow: automation
storyboard: yes
message: "Visible peeling is an irritation side effect, not a scorecard for whether an active is working — go slow, buffer the barrier, and protect it."
destination: shorts
aspect: 1080x1920
language: en
audience: "skincare-curious viewers stacking actives (retinol, AHA/BHA, exfoliating toners) and reading peeling as proof of progress"
length: 30s
angle: myth-bust / claim-audit
VO_MODE: silent
style_preset: seoulhabit
---

## Intent

Creator-supplied, second-by-second brief (six timed beats, 0–30s) for a claim-audit
short: peeling from actives is a side effect, not evidence a product is working. This
is a new content lane for the channel — the 23 prior `videos/` projects are ingredient
profiles (ceramides, PDRN, centella, retinal, betaine salicylate…); this one audits a
*behaviour/claim*, not an ingredient.

Three creative decisions were made explicitly with the creator before build, via
`AskUserQuestion`, because the repo has real precedent pointing in different directions
on each:

1. **Narration: silent** — on-screen type + BGM + SFX, no voiceover. The creator chose
   this over adding VO to the brief's beats.
2. **Visual register: flat paper/ink kinetic typography** — the house default, over the
   `retinal-clinical-dossier` alternating-dark/light dossier look or the
   `ceramides-barrier-diagnostic` clinical-UI-dashboard treatment.
3. **Sourcing: real, verified citations** — over the house `○ UNSOURCED` marker
   (used by `pdrn-cellular-science`, `betaine-salicylate-gentle-bha`,
   `retinal-clinical-dossier` for claims with no record) or dropping flags entirely as
   general safety guidance.

**Correction on the record.** The silent option was originally presented to the creator
citing `videos/retinal-clinical-dossier` as an existing silent precedent. That was
wrong: `ffprobe` on its shipped render shows an AAC stereo audio stream, and the project
ships `assets/voice/01–06.wav` plus 22 `.vo-caption` clips — the project's own "silent
short" framing in its BRIEF.md is stale build history from an earlier revision. **Every
one of the 18 real, narrated video projects in this repo has a voiceover; this is the
channel's first genuinely narration-free video.** The choice is still fully sanctioned —
`faceless-video-craft` SKILL.md states "Silence is a genuine choice, not the default,"
and flat kinetic typography is the register named as the one that carries it — but it
is a first, not a precedent-follow. Flagged here rather than left implicit.

Because there is no VO, the on-screen type **is** the caption layer, and the timing grid
is authored directly from the brief's own 0/3/8/14/20/26/30 second marks rather than
derived from measured TTS — this removes the pipeline's usual re-timing cascade for this
project only.

## Assets

No photography or generated imagery is used for any beat — everything is browser-drawn
SVG/CSS, honouring the `seoulhabit-video-3d` rule quoted throughout this repo
("Browser-drawn only… No generative imagery, ever" —
`catalog/ingredients/one-percent-line/README.md:113`). This means **no filed decision
record is required** (contrast `ceramides-skin-barrier` and `glass-skin-5-habits`, both
of which needed one for generated stills/video).

Two scenes reuse proven mechanisms from prior projects rather than building from
scratch, per the skill's component-check step:

- **Scene 3 (barrier diagram)** adapts `videos/betaine-salicylate-gentle-bha/compositions/frames/02-harsh.html`'s
  inline-SVG brick-wall mechanism (`#hd-wall`, the acid-wash rect + shard paths). That
  scene's own headline — "Clear skin shouldn't cost you your barrier" — is this video's
  thesis.
- **Scene 4 (two-card boundary)** adapts `videos/retinol-patch-test/compositions/frames/05-wait-48.html`'s
  `.split-normal` / `.split-stop` two-column mechanism.

Coral is spent exactly once, in Scene 2's strike — the brief's own request ("a sharp red
line cuts through the claim") — which means Scene 4 carries its boundary on rule weight
and ink rather than the coral border `05-wait-48.html` used, since house rule allows
coral only once per video. Documented as a deliberate mechanism-not-skin adaptation.

Design tokens, fonts, the audio-bus pattern, and QA scripts are inherited verbatim from
channel sources of truth (`seoulhabit-launch`, `centella-cica-vs-snail-mucin`,
`glass-skin-5-habits`) per `faceless-video-craft`'s "Consistency across a channel's
videos" — see `frame.md § Channel audit`.

## Customizations

- No `<hf-audio-group>` VO bus and no `data-fx-carve` — there is no voiceover to duck
  music under. Audio is a BGM bed (reused, `retinol-patch-test/assets/bgm/track.mp3`)
  plus SFX cues, all reused from existing channel assets (see `frame.md § Audio mix`).
- BGM plateau raised well above the channel's usual `0.12` (tuned for sitting under a
  voice) since here it is the only sustained audio in the mix — set by measuring the
  mastered render, not copied by convention. See `frame.md § Audio mix` for the
  measured value.
- No `SCRIPT.md` (nothing was spoken), no `assets/voice/`, no
  `compositions/captions.html`, no `caption-overrides.json` — the on-screen kinetic
  type is the only text layer and was authored directly, not derived from a transcript.
- No sidecar `.srt`. There is no speech, so there is no transcript to export one from.
  A deliberate, recorded departure from the skill's "produce the `.srt` even for a
  short" line, which presumes a transcript exists.

## Notes

- **Sourcing — explicit research pass, not left to the model's judgement.** A dedicated
  research pass checked all five on-screen claims against PubMed and regulatory text
  (FDA, 21 CFR), fetching and confirming every citation URL live. Two lines in the
  original brief were found to say the **opposite** of the regulator's own text and were
  corrected before build:
  - "Burning, swelling or pain is not the goal" contradicted 21 CFR §333.350(c)(4)(ii),
    which lists burning and swelling as *expected, labeled* local irritation, not signs
    something has gone wrong. Corrected to "Severe burning or swelling? Stop and ask a
    doctor" — tracking §333.350(c)(3)(ii)'s actual severity-based instruction.
  - "More actives. More results?" answered flatly "no" contradicts the 2024 AAD acne
    guideline (PMID 38300170), which lists combining topical therapies with multiple
    mechanisms as a *good practice statement* for medically directed treatment. Narrowed
    to "More exfoliants. More results?" — true only for unsupervised stacking of
    exfoliating actives, which is what the brief's surrounding beats (retinol, acid,
    toner bottles) actually depict.
  - "Temporary dryness can happen" needed no change — already correctly hedged.
  Full citation list, verdicts, and the two identifier caveats (no DOI exists in PubMed
  for three of the five PMIDs; the FDA's 2014 acne-hypersensitivity safety communication
  is 404 on fda.gov, archive-only) are recorded in `frame.md § Sourcing`.
- **A stated evidentiary limit, not left implicit.** Scene 3's headline ("Peeling is a
  side effect — not a scorecard") is evidenced by two double-blind trials
  (PMID 7544967, PMID 22538278) **for retinoids in photoaging** specifically. No
  equivalent study was found dissociating peeling from efficacy for AHA/BHA exfoliants
  or for acne endpoints, and the strongest source is a dose-comparison of group means,
  not a per-patient correlation of an individual's peeling against their own outcome.
  Ships as the video's title claim regardless — it is the strongest available evidence
  and the claim is a real one — but the limit is recorded here so a future pass can
  revisit it if better sourcing surfaces, matching how `ceramides-skin-barrier` and
  `betaine-salicylate-gentle-bha` record their own sourcing postures rather than
  leaving them implicit.
- Citation chips carry **PMIDs and CFR/FDA document identifiers**, not `ING-*` ids — no
  `ING-*` record exists for behavioural/regulatory claims, and house rule bans inventing
  one. This is a new chip vocabulary for the channel; recorded in `frame.md § Sourcing`
  for the next project that needs a non-ingredient citation.
- Run scoped to Setup + Build in one pass. `storyboard: yes` — this project's
  frame-by-frame plan has not yet been reviewed by the creator.
