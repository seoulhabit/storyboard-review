---
workflow: faceless-explainer
flow: automation
storyboard: yes
message: "Product pilling (crumbs after layering) and true peeling (skin actually flaking) look similar but call for different fixes — a clean-skin flake points to peeling, layering-only crumbs point to pilling."
destination: shorts
aspect: 1080x1920
language: en
audience: "skincare-curious viewers who see white flakes/crumbs after their routine and default to assuming their skin is shedding"
length: 21.1s
angle: differential-explainer
VO_MODE: silent
style_preset: seoulhabit
---

## Intent

Creator-supplied 9-block A/V script (0:00–0:59, ~59s at spoken pace) teaching
the pilling-vs-peeling differential: what each looks like, why pilling
happens, why it isn't automatically the product's fault, what peeling
actually is, the clean-skin-vs-after-layering tell, and a fix for each. Built
via `/faceless-video-craft`.

Two of this channel's most recent shipped videos already own half of this
ground separately: `videos/pilling-not-dead-skin/` (29.8s, the pilling
mechanism + settle-and-press fix, cited to Lua BL et al. 2024) and
`videos/peeling-not-progress/` (30.1s, peeling-as-irritation-not-progress,
cited to Griffiths 1995 + 21 CFR 333.350). Per creator direction, **this
video is still built as a full standalone piece covering all nine of the
brief's blocks** — it does not defer either half to the sibling videos — so
it stands alone for a viewer who has seen neither.

Three decisions made explicitly with the creator before build, via
`AskUserQuestion`:

1. **Coverage vs. brief exactly as written** → build all nine blocks as nine
   scenes, accepting the real content overlap with the two sibling videos
   named above, rather than compressing to a differential-only piece that
   defers the two fix sections to those videos.
2. **Narration: silent / type-carried**, not the brief's literal voiceover
   script. Matches the two most recent shipped shorts (`pilling-not-dead-skin`,
   `peeling-not-progress`) and avoids the VO re-timing cascade entirely since
   scene timing is authored directly from the brief's own beat marks, paced
   for reading rather than speech.
3. **Runtime: ~26s, not the brief's 50–60s** — `REPORT.md`'s own channel
   analytics (27 videos with real `averageViewPercentage`) measure 19–22s
   shorts at ~78% median AVP vs. ~32% for the 34s–1:27 cohort. All nine
   blocks survive as scenes; only *dwell* is compressed (~2.9s/scene reading
   pace vs. `pilling-not-dead-skin`'s 3.7s). The single place this trades
   hardest against the brief's own pacing is the three-card pilling-fix
   block (brief: 0:38–0:47, 9s) → 3.2s here with a fast three-card stagger
   instead of each card given room.

## Two content decisions flagged rather than buried

- **The brief's close ("SAVE THIS GUIDE") is a generic save/subscribe card**,
  which the skill's pre-render gate explicitly rejects ("the closing beat is
  one specific, lesson-tied action, not a generic subscribe card"). Resolved
  by making the final frame restate the test itself as the take-away —
  `BARE SKIN → PEELING` / `AFTER LAYERING → PILLING` — with "SAVE THIS"
  demoted to a secondary line under it. Keeps the brief's own words while
  making the lesson, not the ask, the thing the frame carries.
- **The brief's differential clue** ("flakes on clean, bare skin point
  toward peeling; crumbs that appear only after layering point toward
  pilling") **has no tested source** — it is a reasonable heuristic the
  brief itself already hedges ("A clue—not a diagnosis"), not a diagnostic
  criterion from either cited study. Scene 06 carries
  `catalog/visual-components/unsourced-flag/`'s pill and **no citation
  chip**. Scene 07's pilling-fix protocol ("let it settle, press instead of
  rub," "SPF in two thin passes") is likewise untested as an intervention —
  Lua BL 2024 measured which *existing* application methods correlated with
  more pilling, not whether a settle-then-press technique reduces it — so it
  gets the same `UnsourcedFlag` treatment, matching
  `pilling-not-dead-skin`'s scene 06 call on the identical protocol claim.

## Source verification (production-loop step: claim check before beat sheet)

Both citations re-verified live against PubMed for this build (not
inherited without checking), via `get_article_metadata`:

**According to PubMed:** Lua BL, Ruan L, Lyu Y, Liu S. *Understanding the
causes of skincare product pilling.* Skin Res Technol. 2024
Aug;30(8):e13828. PMID 39092468. [DOI](https://doi.org/10.1111/srt.13828).

**According to PubMed:** Griffiths CE, Kang S, Ellis CN, et al. *Two
concentrations of topical tretinoin (retinoic acid) cause similar
improvement of photoaging but different degrees of irritation.* Arch
Dermatol. 1995 Sep;131(9):1037-44. PMID 7544967.

**Scene numbers below are the SHIPPED 8-scene map** (re-keyed round 4 — they
had been left on the pre-recut 9-scene numbering since round 2, so every row
pointed one scene later than the render it describes).

| Scene | Brief claim | What the source actually reports | On-screen resolution |
|---|---|---|---|
| 02 | "Pilling is product rolling into tiny balls... usually appears while layering or rubbing" | Confirmed verbatim — 217/528 (41%) volunteers experienced pilling; mechanically it's product balling on the surface during/after layering | Used as-is, chip `Skin Res Technol · 2024` |
| 03 | "Doesn't automatically mean the product is bad. Skin, formulas, and application can all play a role" | Confirmed — abstract states pilling correlates with skin physiology (drier, smoother, higher-pH skin), which product is layered (655 pilling events after sunscreen vs. 35 with foundation — a formula difference), and application method (circular/linear rubbing produced the most events) | Used as-is. **No separate chip** — this is an elaboration of scene 03's same study 2.6s later, not a new claim; repeating an identical chip that soon adds no information |
| 04 | "Peeling is different... actual skin flaking... dryness, tightness, redness or stinging" | 21 CFR §333.350(c)(4)(ii) lists burning, itching, **peeling**, and swelling as expected, *labeled* local irritation from topical acne drug products — the regulatory vocabulary this claim describes in plain language | Used as-is, chip `FDA · 21 CFR 333.350` (same on-screen form `peeling-not-progress` scene 02 already ships) |
| 05 | "Flakes on bare skin → peeling; crumbs only after layering → pilling" | **Not tested by either source.** A reasonable clinical heuristic, not a diagnostic finding | **No chip** — `UnsourcedFlag`: "A clue — not a diagnosis" (the brief's own hedge, kept verbatim) |
| 06 | "Thinner layers, let it settle, pat don't rub, SPF in two thin passes" | Lua BL 2024 measured which *existing* rubbing motions correlated with pilling; it never tested a settle-then-press technique or two-pass SPF application as an intervention | Kept as reasonable advice, **no chip** — `UnsourcedFlag`, matching `pilling-not-dead-skin` scene 06's identical call |
| 07 | "One active at a time. Moisturize. Protect." + "Severe burning or swelling? Stop and ask a doctor." | 21 CFR §333.350(c)(1)(ii): "only use one topical acne medication at a time" if irritation occurs — the textual basis for the first limb. (c)(3)(ii): the severity-gated stop-and-ask-a-doctor instruction. Draelos et al. 2006, *Cutis* (PMID 17121065): barrier moisturizer **before and during** retinoid therapy "facilitates the early phase of facial retinization" — the moisturize limb. FDA AHA labeling guidance, Jan 2005 (FDA-2000-P-0063): the sunscreen-during-exfoliation advisory — the protect limb | Chips `21 CFR §333.350` · `Cutis · 2006` · `FDA guidance · 2005`. **Rewritten round 4 — see below.** |

**Round 4 correction (the reason this row changed).** Through round 3 this
scene rendered **"Pause actives. Moisturize. Protect."** with the ACTIVES
icon struck through, under the two chips carried over verbatim from
`peeling-not-progress/05-reset.html`. Neither chip says anything about
pausing an active: Cutis 2006 backs a moisturizer applied *before and
during* therapy — which points the other way — and FDA-2000-P-0063 backs
the sunscreen limb. The pause limb had no backing row anywhere in this
table, which makes it an **unsourced instruction to stop using an active**,
rendered plainly beside citations that implied it was sourced, with no
`UnsourcedFlag` in the scene. An unsourced claim about starting or stopping
an active is hard-prohibited — a flag does not rescue it — so it was
re-scoped rather than badged.

It also contradicted a regulator this video itself cites: scene 04 uses
`FDA · 21 CFR 333.350` to establish peeling as *expected, labeled*
irritation, and §333.350(c)(3)(ii) gates "stop and ask a doctor" on
**severity**. The video was instructing an unconditional pause three scenes
after citing the rule that says otherwise. `peeling-not-progress` reworded
two of its own claims for exactly this reason ("the brief's original wording
said the opposite of the cited regulator"); this is the same correction,
found one project later.

The fix keeps the beat and the strike animation but changes what they mean:
three actives are shown, two are dimmed and struck, one survives — "one at
a time," not "stop." The severity gate renders beside it.

## Component reuse (production-loop step 5 — checked against catalog/ first)

| Scene | Catalog source | What's reused | What's new |
|---|---|---|---|
| 05 | `catalog/visual-components/barrier-wall/` | Full mechanism — flat wall lifting into detached shards. Fourth independent context for this mechanism in the repo | Claim copy, mono qualifier, citation chip |
| 06 | `catalog/visual-components/split-compare/` | Bisector + two independently-targetable fields | Used in its **neutral, no-flood** mode (like scene 02) since neither condition is "the answer" being interrogated — both are equally real; content is a small drawn flake icon (left) vs. crumb icon (right), not scene 02's plain word labels, so the callback pays off rather than repeats |
| 06 | `catalog/visual-components/unsourced-flag/` | Full component, verbatim treatment | Wording: "A clue — not a diagnosis" |
| 02 | `split-compare`, **mechanism only** | The bisector, in the same neutral no-flood mode | Plain word labels `PILLING` / `PEELING`, introducing the split scene 06 pays off |
| 03 | `videos/pilling-not-dead-skin/compositions/frames/04-stack.html` | Same-family reuse — two stacked bands shedding round pills at the seam | Re-labeled SERUM / MOISTURIZER / SPF (three bands, not two) |
| 07 | `videos/pilling-not-dead-skin/compositions/frames/06-protocol.html` | Numbered-step column layout, `TRY THIS`-style label, no-citation convention | Three cards instead of two numbered steps (brief's own "three rapid cards"), added SPF two-pass line |
| 08 | `videos/peeling-not-progress/compositions/frames/05-reset.html` | Three-icon row + two-chip mechanism (actives/moisturizer/SPF) | Reversed framing — a "switch turns off" animation on the actives icon (brief's own direction) rather than all three simply presented equal |
| 01, 04, 09 | — none | Full builds |

**Considered and declined:** `StatReveal` (no percentage/count stat anywhere
in this brief), `TermDefinition` (the brief calls for a split/comparison,
not a single-term hero card), `ThresholdList` (a ranked list with a cutoff —
doesn't match any of these nine beats), `FrostedPanel` (a peel-away reveal
was considered for scene 05, but `BarrierWall`'s shed-mechanism is the
closer content match and is already this channel's standard for exactly
this claim).

## Imagery

**Superseded by Round 2, below.** The original build was fully
browser-drawn (see the reasoning this paragraph used to carry). Round 2
overturns that call for four beats where the creator review asked for real
visual proof; the diagrams below stayed browser-drawn wherever the beat is
explaining a *mechanism* rather than proving what a viewer should look for.
See "Round 2 § Imagery decision record."

## Round 2 — creator feedback recut (2026-09-01)

A creator review of the round-1 26.1s render asked for eight changes. Every
measurable claim in that review was verified against the actual render
before any change was made (`ffprobe`/`ebur128`/pixel measurement), per
`faceless-video-craft` SKILL.md's "an external QC report is a claim, not a
diagnosis" rule — every checkable claim reproduced exactly, and the
verification pass surfaced five further defects the review didn't mention
(a 3.44:1 contrast failure on ink ground, a 1.05:1 hero-panel/ground
separation making the hook's subject invisible at thumbnail scale, true
peak measured on the wrong artifact, three orphaned SFX cues, and
`tokens.css` never actually being loaded by any scene).

**Runtime: 26.1s → 19.9s, 9 scenes → 8.** Old `02-split` (the neutral
PILLING|PEELING word card) is dropped — its setup/payoff callback role is
now played by the wipe-comparison scene directly. Old `04-factors`
(FactorConverge) keeps its own scene rather than being absorbed into a
neighbor, so the three named factors (skin/formula/how you apply) and the
mechanism they explain survive intact.

**New scene map** (see STORYBOARD.md for the full table): `01-hook-a`
(2.6s, real macro) → `02-residue` (2.9s, macro→diagram match cut) →
`03-factors` (1.9s, FactorConverge) → `04-flaking` (2.8s, macro→diagram
match cut) → `05-test` (3.0s, moving wipe comparison — the signature
moment) → `06-fix-pilling` (2.6s, three demoed tips) → `07-fix-peeling`
(2.1s, the reset) → `08-close` (2.0s, takeaway + reworked CTA, loop-matched
to 01).

**Two opening variants**, per the review's explicit A/B ask:
- **A** (`index.html`, this project's primary/default) — real macro pilling
  residue + "Peeling — or product pilling?"
- **B** (`variants/index-hook-b.html`) — a *teaser* split (deliberately
  unlabeled — no BARE SKIN/AFTER LAYERING verdict, since scene 05 is where
  that comparison actually resolves) + "Those flakes may be your
  skincare."

Both share scenes 02–08 verbatim (`compositions/frames/02-*.html` through
`08-close.html`); only the hook scene and its two SFX cues differ per
variant. Mechanically: two thin-ish root files, each with all 8 scenes
declared directly (not a nested `body.html` sub-composition — an earlier
attempt at that indirection produced a confirmed, reproducible layout
defect on double-nested compositions; reverted in favor of the proven
single-level root→frame pattern this project's own predecessor used).
YouTube has no native Shorts A/B test — these are two separate uploads, a
quasi-experiment at best; match posting day-of-week/time before comparing
retention.

### Imagery decision record

Per `catalog/product-photography/README.md`, the HyperFrames composition
lane is browser-drawn only; generative imagery needs its own filed
decision, following the format `centella-cica-vs-snail-mucin/frame.md`'s
own media exception used.

- **Why:** the review's core complaint was that the hook "lacks visual
  proof" — confirmed independently: the original hook's hero panel
  measured **1.05:1** contrast against its own ground, meaning the crumbs
  (the actual subject) were invisible at thumbnail/grid scale. A drawn
  illustration cannot serve as photographic evidence of what pilling
  residue or flaking skin actually look like; the reviewer's ask for "real
  macro footage" is specifically an evidentiary requirement a diagram
  can't satisfy.
- **Precedent:** `catalog/ingredient-photography/` and
  `catalog/product-photography/` — both Higgsfield-generated (`nano_banana_pro`
  / `nano_banana_2`), both filed under this same clause. There is no
  camera-shot photography anywhere in this repo; every photoreal asset on
  the channel is model-generated. The macro plates here follow the same
  convention: no faces, hands/forearms cropped tight, no product bottles,
  no text/logos/claims in-frame, one consistent grade applied across the
  set (`eq=saturation=0.62:contrast=1.06`, desaturated warm-grey/ivory
  palette matching the channel's ink/paper editorial look).
- **Scope:** four plates
  (`assets/plates/01-pilling-macro.png`, `02-layering-hand.png`,
  `03-flaking-skin.png`, `04-base-skin.png`), used in exactly four scenes
  (01-hook-a, 02-residue, 04-flaking, 05-test) via a real
  `<img loading="eager" decoding="sync">` with explicit width/height and a
  background-colored wrapper, per the mandatory image-plate rules. **Plates
  carry the tactile/evidentiary role only — diagrams keep the explanatory
  role.** No plate ever shares a frame with a citation chip (verified: the
  chip in 02/04 lands 1.35s/1.55s after the plate has already left screen
  via the match cut), so a generated image is never dressed as cited
  evidence. Scene 05's bare-vs-layered comparison uses **one** base plate
  on both sides of the wipe (F1: identity-by-construction) with the
  "layered" state composited as a browser-drawn SVG overlay (residue dots +
  a faint scrim) — not a second generation — so the two states are
  guaranteed to be the same skin, same light, same angle, which two
  independent generations could not reliably guarantee.

### Copy changes

- **Hook A:** "Peeling — or product pilling?" (t=0) → "Those white flakes
  may not be your skin." (t≈1.2s).
- **SPF instruction (accuracy fix, not just a copy trim):** the original
  card read "LESS PER LAYER," which can be misread as "use less sunscreen
  overall" — a real safety issue the reviewer correctly flagged. Reworded
  to **"THIN PASSES"** with the supporting line **"Same total SPF — just
  thinner passes."** — same total product, applied in more, thinner
  passes, never less product.
- **Close CTA:** "Save this." → **"Save this test for your next skincare
  routine."** The memorable rule (`BARE SKIN → PEELING` / `AFTER LAYERING →
  PILLING`) stays the hero of the closing frame, as it already was in
  round 1; the CTA underneath it is what changed.

### Audio

Stayed `VO_MODE: silent` (the review's "add voiceover if music-led" ask was
weighed against staying silent to match the channel's `pilling-not-dead-skin`
/ `peeling-not-progress` / `peeling-question-open` lineage and the tighter
19.9s target — richer tactile SFX chosen instead). BGM re-cut from 26.0s to
19.9s with 200ms declick fades at both ends (not the source file's own tail
fade — that lineage's confirmed loop-boundary trap). Added tactile cues for
the rubbing/press beat, the two macro→diagram match cuts, the wipe (forward
and return), and each of the three demoed tips — sourced by reuse from
`snail-mucin-medical-secret`, `centella-cica-vs-snail-mucin`,
`peeling-not-progress`, `ceramides-barrier-diagnostic`, and
`hyaluronic-acid-serum` (hash-checked against this project's own existing
six before reuse), trimmed to their beat where the source file ran long.

**True peak — measured on the wrong artifact in round 1.** `frame.md` and
`DELIVERY.md` recorded "−1.50 dBTP" after round 1's `loudnorm` pass —
correct on the PCM intermediate, but the AAC encode step afterward pushed
true peak up to the reviewer's measured **+0.5 dBFS**, confirmed by decoding
the shipped round-1 MP4 back to PCM and re-measuring. Round 2's master
targets `TP=-2.5` pre-encode specifically to leave AAC headroom; the
**encoded** deliverable measures **−14.1 to −14.3 LUFS integrated / −1.5 to
−1.8 dBTP** on both variants (see DELIVERY.md's verification table) —
verified on the actual shipped file, not the intermediate.

### A structural bug worth recording for future rounds

Every one of this recut's 9 scene files combines an explicit
height/flex-basis with padding, and none declared `box-sizing`. Under the
CSS default (`content-box`), padding is added *on top of* a declared
height rather than being reserved *within* it — `.stage`'s
`height: 1920px` plus `192px`/`384px` top/bottom padding rendered as an
actual **2496px** box (1920+576), silently pushing bottom-anchored content
(citation chips, CTA lines) past the real canvas edge and into — or
entirely out of — the reserved safe zone. This reproduced identically
across renders regardless of `--safe-*` token values, `justify-content`
strategy, or nesting depth, and took a `getBoundingClientRect()` vs.
`getComputedStyle().height` comparison on a real compiled render to catch —
the discrepancy is invisible from source alone. Fixed with a project-wide
`*, *::before, *::after { box-sizing: border-box; }` reset, plus
`min-height: 0` on every flex child carrying an explicit small flex-basis
(the flexbox "automatic minimum size" default otherwise lets a child's
own content silently grow it past a smaller declared basis). See the
faceless-video-craft SKILL.md update this round proposes.

## Round 3 — scene 07 retimed for pacing (2026-09-01)

Direct creator feedback while reviewing round 2's render, live: "scene 7
feels rushed." Not a re-review of the whole cut — a single, specific
pacing note on one scene.

**This corroborates round 2's own cadence measurement rather than
contradicting it.** `frame.md` § Verification — Round 2 had already
flagged `07-fix-peeling` as the weakest scene by its own active-step
metric (0 steps clearing the 1.0 threshold) and recorded it as "worth a
closer look in a future pass if cadence is revisited" — that future pass
is this one.

**Fix:** `07-fix-peeling`'s own duration 2.1s → 3.3s (+1.2s), same beat
order, more room between each beat. Both citation chips now hold on screen
for 1.35s before the cut, up from 0.75s. A bounded scale-pulse on the
headline (2.5–3.1s) was added so the extra hold time carries real motion
rather than reading as a static freeze once both chips have landed.

**Cascade this triggered** (per the skill's own re-timing-cascade warning —
a single scene's duration change touches more than it looks):

1. `08-close`'s `data-start` in both `index.html` and
   `variants/index-hook-b.html`: 17.9 → 19.1.
2. Root `data-duration` and anchor tween in both files: 19.9 → 21.1.
3. `07-fix-peeling`'s own 4 SFX cues, retimed to the new beat schedule
   (15.95/16.65/17.45/17.85, was 15.90/16.35/16.90/17.15).
4. `08-close`'s 2 SFX cues, shifted +1.2s (19.65/20.00, was 18.45/18.80).
5. BGM: re-cut from the 26.0s source bed to 21.1s (was 19.9s), same 200ms
   declick fades; automation tail points moved to 20.5/21.1.
6. Captions: every cue at or after the old 17.9s mark shifted +1.2s, in
   all four caption files (`pilling-vs-peeling.{srt,vtt}` and
   `_hookB.{srt,vtt}`) — both variants share this cue range, so both
   needed the identical shift.
7. `STORYBOARD.md`'s scene map, duration sum, and the `07-fix-peeling`
   per-scene note.

**Not touched:** scenes 01–06 and their SFX/captions (all before the
15.8s boundary this change starts at), the imagery decision record, the
copy changes, the box-sizing fix, and both variants' hook scenes — this
round is scoped to the one scene named in the feedback.

## Round 5 — external QC pass on the round-4 render (2026-09-01)

Three "visual and educational polish" items were raised against
`renders/pilling-vs-peeling.mp4`. Each was reproduced against actual pixels
before any fix was planned, per the craft skill's rule that a QC report is a
claim, not a diagnosis. **Two reproduced; one did not.** In both real cases the
named symptom was legitimate and the prescribed fix was wrong.

| # | Claim | Verdict | Measured |
|---|---|---|---|
| 1 | SPF/Moisturizer/Serum stack + "connecting dots" reads as application order | Real misread risk, mechanism misdescribed | It is a physical cross-section (SPF outermost, serum against skin) — correct. The "dots" are not sequence connectors; they are the `.pill` residue balls detaching from the seams, which is the scene's entire subject. No descending line exists. |
| 2 | Red ✗ over "Pat, don't rub" is contradictory | Real, and worse than reported | Card 3's glyph was *only* a coral ✗. Cards 1–2 each carry an affirmative glyph; card 3 had **no "pat" mark at all**. |
| 3 | Citations too small / low-contrast | **Did not reproduce** | Nothing on screen is below 32px (the floor); smallest is exactly 32px. Scene 04 chip measured **12.23:1**, scene 07 chips **5.09:1** — both clear 4.5:1. Legible at 25% phone scale. |

### What was changed, and where this diverges from the report

- **Scene 02.** The report asked for bullet points. Rejected — that destroys the
  cross-section and the pills-from-the-seams animation. Instead the stack now
  sits on a labelled **SKIN** substrate (flat higher-opacity fill, square
  corners, deliberately not a fourth `.band`), which makes it read as depth
  rather than order. The residue pills were reversed to drift **upward**: with a
  substrate present, falling downward reads as rolling *into* the skin. Same
  durations, stagger and easing, so no beat or SFX moved.
- **Scene 06.** The report asked for a green check plus a red ✗ on "Rub".
  Rejected on the colour half — coral is this video's single accent spend, and a
  second accent competing in one frame is its own defect. The split was achieved
  in-palette instead: **three discrete taps** (pat, full-brightness paper,
  untouched) above **one continuous stroke** (rub) carrying a coral slash sized
  to that stroke alone. Discrete-vs-continuous now carries the instruction, so
  the two marks differ in kind rather than only in label. An intermediate pass
  that dimmed the rub stroke to 0.4 was rejected on inspection — the coral read
  as free-floating negation again, because the thing it crossed had become
  invisible underneath it.
- **Chips (elective).** 32px → 34px across scenes 02/04/07, and scene 07's chips
  moved to a scoped `--ink-2-strong` (#565656) with a firmer border:
  **5.09:1 → 6.91:1** measured on the render. Scene 04's chip colour was left
  alone at 12.23:1. `--ink-2` itself was not touched — `.kicker` also consumes it
  and it is correctly scoped to paper at 4.89:1.

### A regression this round caught, and the reason it was catchable

The 34px chip bump pushed scene 07's two wrapped chip rows to ~148px against
`.chips-zone`'s fixed `flex: 0 0 140px` basis. The zone does not grow
(`min-height: 0`), so the overflow painted **below the stage's content box and
4px into the reserved bottom zone**. `npx hyperframes check` reported **0 errors**
on that state — this is a rendered-pixel defect, not a source defect, and only
`check-safe-area.py` on the actual render saw it. Fixed by tightening the zone's
own vertical rhythm (chip padding 8→6px, row gap 12→10px, zone padding-top 8→4px)
to fit the larger type inside the existing basis, rather than reverting the type
or widening a zone whose bottom edge *is* the safe line. Ink now ends at row 1527
against a 1536 boundary.

### Mastering had to be re-applied

Re-rendering discarded round 3's `loudnorm` master — the fresh renders measured
**−23.0 / −23.3 LUFS**, ~9 dB under target. The documented two-pass
`I=-14:TP=-2.5` chain was re-run and both variants land back on their previously
recorded values (A −14.3 LUFS / −2.0 dBTP, B −14.2 / −2.1), video streams
MD5-identical through the mastering pass. **Any future round that re-renders must
re-master**; the render step does not carry it.

### Pre-existing, not addressed this round

`check-cadence.py` reports 4 scenes over the 1.6s quiet ceiling (2, 4, 5, 7;
whole-video 13.6% active steps). Scene 5 — 0/23 beats, 2.88s quiet — was not
touched this round, which confirms these predate it. Out of scope for a QC pass
that raised no cadence finding, but it is the largest open item on this video.


## Round 6 — cadence gaps in scenes 2, 4, 5, 7 (2026-09-02)

Round 5 left `check-cadence.py` reporting four scenes over the 1.6s quiet
ceiling. All four are now clean.

| Scene | Before | After |
|---|---|---|
| 2 `02-residue` | 2/22 beats, 1.75s quiet | 6/22, **1.00s** |
| 4 `04-flaking` | 1/21 beats, 1.75s quiet | 4/21, **1.25s** |
| 5 `05-test` | **0/23 beats, 2.88s quiet** | 7/23, **0.88s** |
| 7 `07-fix-peeling` | 2/25 beats, 1.75s quiet | 3/25, **1.12s** |

Whole video: 13.6% → **22.8%** active steps. `Overall: clean.`

The gate is the longest quiet *run*, not a beat percentage, so each dead window
needed one or two genuinely large changes rather than continuous motion. In every
case the fix was to make the thing the scene is already about actually visible,
not to add idle motion to move a metric.

- **Scene 2.** The pills were r=7-10 specks — about 0.09% of canvas — while the
  caption promised "rolls into balls." They are now real balls (r=28-36) seated
  in the two seams, forming in two clusters and lifting **up and away** from the
  SKIN substrate. A cluster is large enough to register; a 0.16s-staggered speck
  never was.
- **Scene 4.** The top course was mostly *outline* (fill 0.07), so round 4's
  opacity dim moved ~900px per brick. The course now loosens (fills, `--bf`) and
  then sheds — which is what "actual skin flaking" means — and shards were
  enlarged.
- **Scene 7.** Removed the `scale: 1.015` headline pulse; this file already
  records that even a 1.08 pulse on a 1.08:1 ground measured 0.02-0.10 mean
  |dLuma|. Replaced with a focus pull: once the routine and its citations have
  landed, the icon row dims to 0.45 and the severity line comes to full ink.
  That is an editorial beat — attention moving to the safety exception.

### Scene 5 was not a pacing problem — it never rendered at all

Worth recording in full, because two plausible explanations were wrong before
the real one was found.

`05-test` measured **0 beats in 23 steps** across three separate renders, and
frames at t=10.25 / 11.40 / 12.95 were **byte-identical inside the panel** while
the rest of the frame animated normally. The wipe had no visual effect in any
shipped render — this scene has never worked, in any round.

1. **First hypothesis — the comparison was too subtle.** Partly true and worth
   fixing on its own: the scrim was 0.08 (~14 luma on a light plate) and the
   crumbs were r=7-11, so the "after layering" side was, to both a viewer and a
   frame diff, the same picture as the bare side. Fixed (bigger clumped crumbs,
   scrim to 0.13, its own dulled plate). **Did not change the measurement.**
2. **Second hypothesis — duplicate media nodes.** Both `<img>`s pointed at
   `04-base-skin.png`; lint had flagged `duplicate_media_discovery_risk` for
   rounds and it had been repeatedly waved through as benign. Clearing it got
   the project to 0 warnings for the first time. **Also did not change the
   measurement** — so the warning, while real, was not the cause.
3. **Actual cause — GPU compositing.** The reveal animated `width` on an
   `overflow: hidden` box. Under hardware capture (ANGLE/Metal on this Mac) the
   compositor never updated that clip, so the entire layered subtree was absent
   from every captured frame — while the DOM reported correct geometry the whole
   time (the engine's own layout pass even reported `layered-content overflowed
   #s5-wipe right 504px`, i.e. mask = 336, at t=12.89).

**What isolated it:** `hyperframes snapshot --at 11.40` drew the scene
*correctly* from identical source, and so did a plain browser. Render and
snapshot disagreeing pointed at the capture path, and re-rendering with
`--no-browser-gpu` (SwiftShader) produced the correct picture. The fix is the
mechanism, not the flag: the reveal is now `clip-path: inset()` driven by a
`--wipe` custom property — compositor-safe, and the same custom-property pattern
this project already uses for `--hl` / `--act` / `--bf`. It renders correctly
under the normal hardware path, so the render stays fast.

**Generalisation checked:** three other scenes animate `width`
(`01-hook-a` #h1a-rule, `06-fix-pilling` #s6-labelRule, `08-close`
#s8-underline). All are solid rules whose own painted box grows — not clips over
other content — and all verified present in the render. No further change.

**Lesson worth carrying:** a frame diff that reports *zero* change in a region
across a whole scene is evidence of a broken render, not of slow pacing. It was
read as a pacing number for two rounds.

### Mastering, again

The render discards the `loudnorm` master every time (raw: −23.0 / −23.3 LUFS).
Re-applied; both variants back on target (A −14.3 LUFS / −2.0 dBTP, B −14.1 /
−1.8), video streams MD5-identical through the pass.


## Assets

| Asset | Source | Reused / new | Used in |
|---|---|---|---|
| `assets/fonts/{inter-800,eb-garamond-400,jetbrains-mono-500}.woff2` | `videos/pilling-not-dead-skin/assets/fonts/` | reused | all scenes |
| `assets/tokens/tokens.css` | `videos/pilling-not-dead-skin/assets/tokens/` | reused verbatim | all scenes |
| `assets/bgm/track.mp3` | `videos/pilling-not-dead-skin/assets/bgm/track.mp3` (re-cut a third time in this lineage) | reused, **re-cut to exactly 26.0s** with 200ms declick fades baked in, floor raised to 0.15 at both ends for the loop seam (peeling-question-open's trick) | full runtime |
| `assets/sfx/click-soft-chip-pair-lands.mp3` | `videos/pilling-not-dead-skin/assets/sfx/` | reused | citation chip / card lands |
| `assets/sfx/sharp-text-stamp-impact-hit.trimmed.mp3` | `videos/pilling-not-dead-skin/assets/sfx/` | reused | 01 hook stamp |
| `assets/sfx/whoosh-soft-question-to-headline-wipe.mp3` | `videos/pilling-not-dead-skin/assets/sfx/` | reused | 01→02 cut |
| `assets/sfx/glass-clink.mp3` | `videos/pilling-not-dead-skin/assets/sfx/` | reused | scene 06 clue payoff |
| `assets/sfx/chime.mp3` | `videos/pilling-not-dead-skin/assets/sfx/` | reused | 09 loop settle |
| `assets/sfx/crumb-scatter-soft-granular-tick.mp3` | new (see note) | new | 01 reveal, the brief's own "one subtle crumb sound" cue |

**No SFX-generation tool is available in this environment** (the connected
media-generation server's audio tool is text-to-speech only and explicitly
declines general sound-effect requests). The closest existing candidate —
`peeling-not-progress/assets/sfx/click-soft-3-each-step-arrives.mp3`
(0.240s, three soft clicks in quick succession — already authored for
several small things landing in sequence) — is reused and renamed for this
cue rather than left unaddressed; it is a distinct file from `glass-clink`
(hash-checked: not a duplicate), so the two cues don't collide on the same
underlying sound under different names. If a real crumb/scatter foley
source becomes available later, swap it in without retiming (same cue,
same duration).

## Coral spend

Coral (`--accent-limit`) is spent exactly once, on the small ✗ mark inside
scene 07's "PAT, DON'T RUB" card — the one moment this video identifies a
behavior to avoid, matching `pilling-not-dead-skin`'s identical convention
on its own rub-avoidance beat. It does not appear in scene 06's
`UnsourcedFlag`, scene 08's actives-off icon, or anywhere else.

## Notes

- Safe areas: **192 / 384 / 72 / 162** (top/bottom/left/right), margin 6px —
  the tokens.css default, matching `pilling-not-dead-skin`,
  `mugwort-healing-herb`, and `peeling-question-open`.
- The brief's closing "Caption:" paragraph ("Pilling and peeling can look
  similar...") is **YouTube description copy, not a subtitle/caption
  file** — it is not a sidecar `.srt`/`.vtt`. Recorded here so it isn't
  mistaken for the caption deliverable; it lands in `DELIVERY.md`'s
  description copy instead. The actual sidecar captions are hand-authored
  from this project's own on-screen copy deck.
- Catalog-contribution candidate: scene 04's three-factor
  (skin/formula/application) convergence-on-one-node diagram — nothing in
  `catalog/visual-components/` currently does a several-inputs-converge
  mechanism. Decided honestly after the scene is built and verified, per
  production-loop step 12 — not assumed in advance.
