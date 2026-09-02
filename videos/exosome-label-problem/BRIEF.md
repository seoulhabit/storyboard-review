# BRIEF — exosome-label-problem

**Title (working):** Exosome Skincare Has a Label Problem
**Format:** YouTube Short, 9:16, 1080×1920, 30fps
**Audience:** skincare buyers evaluating a trend ingredient at the shelf —
no clinical vocabulary assumed
**Engine:** `hyperframes@0.8.22`
**VO_MODE:** narrated (synthetic) — see § Voice

## Thesis

"Exosome" on a label names a *particle class*, not a formula, a dose, or a
result. The word carries no information about source, characterization, or
whether the finished product was ever tested on people — on intact skin.
Promising ≠ proven.

---

## Relationship to `videos/exosome-label-decode`

A separate session was concurrently building `videos/exosome-label-decode/`
on the same topic. **This project is independent and shares no files with
it.** Nothing here was copied from that project; its BRIEF was read for
context only, and its three cited DOIs were deliberately **not inherited** —
every source below was verified against PubMed in this session (§ Sources).
Assets come from `catalog/` and `videos/pilling-vs-peeling`, not from the
sibling.

---

## Voice

Higgsfield `generate_audio`, model `seed_audio`, voice **Kimberly**
(`voice_id 674b71b8-1d2e-4087-8567-d1f53c0b9f3c`, `voice_type element`) —
the channel's established voice, confirmed live via `list_voices` before the
build rather than assumed from a prior project's record.

**TTS prompt vs. on-screen text diverge deliberately.** Em-dashes in the
source script were replaced with sentence breaks in the *prompt only*, for
prosody. On-screen copy keeps the authored punctuation.

---

## Duration — reason on record

Script nominal is **~65s**; final runtime is VO-derived and recorded in
`STORYBOARD.md` after measurement, never authored up front.

Past 50s needs a reason (production-loop step 2). The reason:

- The operator supplied a script with its own segment timings summing to
  **58s**, and separately approved an added ~6s taxonomy beat. The runtime
  is the brief, not drift.
- The deliverable **is** a three-question decision checklist. Dropping a
  question to reach 45s removes a third of what the viewer came for.
- The channel's own measured baseline finds **no duration→performance
  relationship** (age-normalized median ratio 4.38 for ≤50s vs 3.97 for
  >50s, against a within-cohort spread of 0.67–49.44). It does not license
  the inverse either — so 28–45s is treated here as a **craft budget, not a
  threshold**, and the copy is written tight rather than allowed to sprawl.

Mitigation actually applied: each take's speaking rate is tuned so the
measured take lands near its scripted slot, instead of letting a ~23%
TTS overshoot (measured on `pdrn-cellular-science`) carry the piece to ~75s.

---

## Script — deviations from the supplied text, and why

The operator's script is authoritative. Two lines changed, both because the
claim as written could not be sourced and a **stronger, sourced** version
existed. Nothing was softened to avoid a claim; both edits make the on-screen
assertion more specific.

| Supplied | Shipped | Why |
|---|---|---|
| "many of the strongest-looking results involve exosomes applied after microneedling or laser, when the skin barrier has already been disrupted" | "Much of the clinical work pairs exosomes with microneedling or laser — devices used precisely to get past the barrier." | No source quantifies "many of the strongest results." S5 states the mechanism directly: these devices "overcome the stratum corneum barrier to facilitate substantive dermal penetration." That is a sharper claim, and it is cited. |
| (added beat) "cell-derived exosomes" as one undivided class | "And 'cell-derived' isn't one thing either — stem cells, platelets, even milk." | The operator approved a second taxonomy beat. The sourced source-list (S2) is adipose stem cell / platelet / plant / milk. "Immune cell" was considered and dropped: not sourced. |

---

## Palette — translation record

Channel `tokens.css` is copied verbatim from `videos/pilling-vs-peeling`
(byte-identical across 8 projects). Roles used here:

| Token | Role in this piece |
|---|---|
| `--paper #F7F5F0` | ground, scenes 1 / 3 / 5 / 7 |
| `--ink #131516` | ground, scenes 2 / 4 / 6; primary text on paper |
| `--celadon #93B896` / `--leaf #6F8F72` | vesicles, evidence marks |
| `--aqua #59B8AE` | rules, the "tested" affirmative in scene 6 |
| `--coral #C97A5C` | **spent once**, scene 5 — the refusal beat |

`--coral`'s documented channel role is "a limitation or a refusal," which is
exactly what scene 5's "does not prove" needs. Coral and celadon are used as
**fills and marks behind or beside ink text**, never as read-text colour on
paper — neither clears 4.5:1 as type on `--paper`.

`--ink-2` on paper, `--ink-2-dark` on ink. The token's documented scope is a
constraint, not a comment: a prior project recorded "16/16 passed" while
reusing a paper-scoped token on an ink ground at 3.44:1.

---

## Imagery decision record

- **Why photographic:** the piece needs a real tactile/product anchor early
  (asset-protocol rule 6). The subject is a retail serum and three physically
  distinct source materials — there is something concrete to show, so an
  all-illustrated open would be the weaker call.
- **What, and reused vs. generated:** five plates, **all reused from
  `catalog/`, none generated.**

| Scene | Asset | Role |
|---|---|---|
| 1, 7 | `catalog/product-photography/assets/A01-01.png` | frosted dropper bottle, `세럼 · 30mL` |
| 3 | `catalog/ingredient-photography/sh-pdrn.png` | cell-derived — opalescent biologic serum |
| 3 | `catalog/ingredient-photography/02-centella-asiatica.png` | plant-derived — botanical |
| 3 | `catalog/ingredient-photography/07-bifida-ferment-lysate.png` | ferment-derived — cloudy ferment lysate |
| 5 | `catalog/skin-macro-photography/04-base-skin.png` | intact barrier, deliberately neutral |

- **Why the triptych matters:** three plates in one consistent grade
  (2048², warm cream matte seamless, no baked text) that literally depict the
  three material classes the script names. This is the scene's argument, not
  decoration.
- **Scope:** unbranded, no faces, no claims on any rendered surface. The
  bottle's label carries a category word and a volume only — it asserts
  nothing, which is what lets it sit next to a sourced claim.
- **What stays browser-drawn:** barrier disruption (scene 5). The catalog's
  own rule — don't let a generated plate stand in for a mechanism it wasn't
  built to show — and a photograph of microneedled skin would also import the
  in-office context the piece exists to separate from a daily serum.
- **No lab / vial / microneedling imagery exists in the catalog**, and none
  was generated: it would visually assert the very procedure-to-serum
  transfer the scope guard below forbids.

---

## Sources

Every on-screen citation pill reads `Journal · Year` only. No PMID, no DOI,
no internal key on any frame. Full list with DOIs → `DELIVERY.md`.

**All eight verified against PubMed in this session.** The sibling project's
DOIs were not inherited; one of them (`10.1093/asj/sjaf259`) was not
reproduced by search and is not used here.

| # | Claim carried | Pill | DOI |
|---|---|---|---|
| S1 | Nomenclature and characterization of EVs are still being standardized — "exosome" alone is not a complete identity | `J Extracell Vesicles · 2024` | `10.1002/jev2.12404` |
| S2 | Marketed/studied vesicles derive from adipose stem cells, platelets, plants and milk | `Dermatol Pract Concept · 2026` | `10.5826/dpc.1601a6462` |
| S3 | Plant-derived vesicles are a distinct class ("exosome-**like** nanovesicles") with their own standardization and regulatory gaps | `J Nanobiotechnology · 2025` | `10.1186/s12951-025-03715-1` |
| S4 | Bacteria/ferment-derived vesicles are a distinct class; skin evidence is preclinical | `J Nanobiotechnology · 2024` | `10.1186/s12951-024-02893-8` |
| S5 | Fractional laser and microneedling platforms "overcome the stratum corneum barrier to facilitate substantive dermal penetration" | `Facial Plast Surg Clin N Am · 2026` | `10.1016/j.fsc.2026.05.002` |
| S6 | Topical-only human evidence is small (9 studies met inclusion, 2024) and no topical exosome product is FDA approved | `Aesthet Surg J Open Forum · 2024` | `10.1093/asjof/ojae017` |
| S7 | 19 human studies, most non-randomized; heterogeneity and lack of follow-up; rigorous RCTs required | `Cureus · 2026` | `10.7759/cureus.104182` |
| S8 | Diverse marketed formulations; proper characterization of cargo is necessary for safety and efficacy | `Int J Dermatol · 2025` | `10.1111/ijd.17903` |

**Scope guard, load-bearing.** S5, S7 and S8 span **injected and in-office**
exosome use alongside topical. This video is about a **retail serum**. That
gap is not glossed — it is the entire point of scene 5 and of question three
("was it tested on intact skin?"). **No frame claims a topical serum inherits
evidence generated by an injected, microneedled, or laser-assisted
protocol.** Where a number is shown, its route and population are shown with
it.

**Plain-language check (gate 9b).** No claim sentence requires clinical
vocabulary. "Extracellular vesicle" never appears as the claim; "microscopic
packages cells use to carry signals" does. "Stratum corneum" is rendered as
"the outer barrier." "Non-randomized" is rendered as "most weren't
randomized" with the plain gloss "no fair comparison group." Citation pills
stay terse because they are provenance, not instruction.

---

## Beat sheet

Presenter: **photographic plate + condensed type**, held across all seven
scenes. Grounds alternate paper/ink → **hard cuts everywhere**; a crossfade
across a ground change produces a muddy midpoint and is structurally unsafe.

| # | Scene | Ground | Intent (one line) | Mechanism | Pill |
|---|---|---|---|---|---|
| 1 | `01-hook` | paper | The word on the bottle is not the evidence | full-bleed plate + Ken Burns; `EXOSOME` set at t=0, payoff ≤2s | — |
| 2 | `02-what` | ink | It's a signal-carrying particle — not an identity | `TermDefinition` lockup + SVG vesicle-release diagram | S1 |
| 3 | `03-materials` | paper | One word, three different materials | **new `MaterialTriptych`** — three plates, then the transfer is struck | S3 |
| 4 | `04-source` | ink | "Cell-derived" isn't one thing either | three source chips + qualifier | S2 |
| 5 | `05-barrier` | paper | The good results got past the barrier first | adapted `BarrierWall` + intact-skin plate; **coral spent here** | S5 |
| 6 | `06-questions` | ink | Three questions before you buy | **new `QuestionGate`** | S6 |
| 7 | `07-verdict` | paper | Promising ≠ proven; one specific action | adapted `SplitCompare` + closing lockup | S7 |

**Hook.** Frame zero is composed, not mid-fade — plate at rest, `EXOSOME`
already set. The payoff ("may not be what you think") lands by ~2s, inside
the retention window; the question is not left hanging for the setup.

**Loop.** Scene 7 returns to scene 1's ground and hero position so a replay
hands back cleanly. The BGM bed is re-cut to true runtime with ~200ms declick
fades at both ends — a stock tail fade authored for a longer bed would leave
the last seconds near-silent and hand the replay a dead beat. Both ends are
checked by frame-diff **and** by RMS, not by picture alone.

**Closing beat** is one specific, lesson-tied action ("check your bottle for
the source — comment it and we'll decode the label"), not a generic
subscribe card.

**Layout variety.** 2-col grid → stacked lockup+diagram → 3-col triptych →
chip row → split wall/plate → vertical gate list → bisector. No two
consecutive scenes share a structure.

---

## Component check

Cross-checked against the catalog inventory read at discovery, not a fresh
search. Reused/adapted vs. built new:

| Scene | Catalog entry | Verdict |
|---|---|---|
| 2 | `TermDefinition` | **adapt** — lockup structure (name / category / definition) for the text half. Single entry, no cycling; the array-cycling half of its contract is unused. |
| 3 | — | **build new → `MaterialTriptych`** |
| 5 | `BarrierWall` | **adapt** — keep the 3-course wall + shard mechanism; replace the acid-wash descent with puncture channels, which is the actual mechanism here. |
| 6 | — | **build new → `QuestionGate`** |
| 7 | `SplitCompare` | **adapt** — bisector, two independently-targetable fields, tint floods the interrogated side only, no success colour. |
| all | `.uf-cite` pill (from `unsourced-flag`) | **copy** — `Journal · Year` only |

**`FactorConverge` rejected, deliberately.** It was the near-miss for scene 3
and is a many-to-one causal diagram (3 inputs converging on 1 outcome, fixed
triangle geometry). Scene 3's three materials are **parallel and
non-converging** — the whole point is that they do *not* share an outcome.
`ThresholdList` (ranked list split by a cutoff) and `SplitCompare` (two-thing
bisector) don't fit a 3-way parallel comparison either. Forcing any of them
would be a category error, so scene 3 is built new.

**`Dawn-to-Dusk` rejected for scene 6.** It is the catalog's only checklist
and its least-mature entry — static, no clock, no data contract, and
deprecation-recommended by the design system's own notes. Scene 6 needs a
timed sequential gate, so it is built new.

Both new components are harvested back to `catalog/visual-components/` per
production-loop step 12.

**Reused imagery:** 5 plates. **Newly generated imagery:** none.

---

## Type & legibility

Channel floors, from `assets/tokens/tokens.css`: hero 96px, figure 60px,
frame 50px, body 40px (reading floor), label/chip 32px (absolute floor for
anything meant to be read), `--t-floor` 20px. **Nothing below 32px carries
content.**

Contrast is verified per **ground**, against actual rendered pixels — not
tokens, and not the engine's own contrast pass, which evaluates declared
stylesheet colours and structurally cannot see what a plate puts behind text.
Any text over a photographic plate gets an opaque backing (pill or scrim)
rather than relying on a colour choice holding across the plate.

Diagrams: one mechanism per beat, **three important labels max**.

---

## Safe areas

`--safe-top 192` / `--safe-bottom 384` / `--safe-right 162` / `--safe-left 72`,
`--safe-margin 6`. Every scene consumes the tokens; **no scene hardcodes an
offset.** Any scene whose Ken Burns scale sits *outside* a clipped panel uses
the **derived** `--safe-*-zoomed` values (already in `tokens.css`, including
the top/left inversion for an off-centre origin) rather than a hand-tuned
`+Npx` allowance, which goes stale the moment the token or the scene's scale
changes. Where the zoom wrapper is *inside* a panel with `overflow: hidden`,
no zoomed math is needed and the spatial-plan comment says so explicitly.

Verified against the render, not the source — a source-level audit
structurally cannot see a transform-induced overshoot.

---

## Round 1 — post-render verification fixes

Every item below was found by measuring the **actual render**, not by reading
the source. `npx hyperframes check` reported **0 errors** while several of them
were live, which is the whole reason the pixel-level gate exists.

### 1. UA margins broke the safe area (hard gate, 4 scenes)

`check-safe-area.py` failed with ink 64–75px below the reserved bottom line and
39px inside the right rail, on every scene carrying a `<figure>` panel.

Root cause was **not** `box-sizing` (the border-box reset was present from the
start). It was the browser's own default margins, never reset: `h1` carries
`margin: 0.67em` — **100px** at this piece's 150px display size — `p` carries
`1em`, and `figure` carries `1em 40px`. Those inflated each fixed-height flex
stack until the bottom-anchored plate panel was pushed past the line, and the
figure's 40px inline margin pushed it past the right line.

Fix: `h1, h2, h3, p, figure, blockquote, ul, ol, dl { margin: 0; }` in every
scene, alongside the border-box reset. `gap` on the flex column was already
doing all the spacing, so every one of those margins was unwanted.

Worth recording because the skill's own note on this failure mode names
`box-sizing` as the cause — this render had the border-box reset and still
failed the same gate for a sibling reason.

### 2. Transform-induced overshoots (hard gate, 3 scenes)

With the margins fixed, the gate still failed on 19 frames:

- **`back.out()` entrance overshoot on edge-anchored elements.** A
  `back.out(1.6)` scale tween passes *through* ~1.06 before settling at 1.0. On
  the triptych's first column (left edge) and on right-aligned citation pills,
  that walked the element 5–8px into the reserved zone for the length of the
  tween. Fixed by anchoring `transform-origin` to the touched edge so the
  overshoot grows inward — the pop survives, the geometry risk doesn't.
- **A slide entrance on a left-anchored row.** `06-questions`' gate rows
  entered from `x: -26`, i.e. at x=46 for the whole tween. Per the skill: fix
  the mechanism, don't add margin. The row now cross-fades in place and the
  slide moved to an inner text block that starts at x=200.
- **A citation pill that was too wide at rest.** `02-what`'s note + pill in one
  `space-between` row measured 875px against an 846px content box, putting the
  pill's *resting* right edge 29px inside the rail. No transform fix could
  reach this one — it was static layout. Both such rows are now stacked.

### 3. Cadence was 3.4× below the channel's shipped reference

`check-cadence.py` flagged **all seven** scenes over the quiet ceiling, at
**4.0%** active steps whole-video with a worst quiet run of 7.38s.

Before acting, the metric was calibrated against `videos/pilling-vs-peeling`'s
shipped, QC'd round-4 render: **13.6%** active, worst quiet run 2.88s. So the
threshold was not mis-tuned — this piece really was that much softer. Its beats
were authored and visible but gentle: medium-sized elements on 0.44–0.52s
fades, clustered in each scene's first half.

Fix was a real motion pass, not decoration added to move a number:

- entrances shortened (0.52 → 0.32–0.34) and travel increased (y:18 → y:40–64,
  scale 0.92 → 0.72–0.78)
- **real state changes added in each scene's quiet stretch**: the triptych's
  tiles desaturate in sequence *after* the strike; `02`'s vesicles scatter and
  the membrane contracts under "not an ingredient identity"; `04`'s parent chip
  answers each child landing; `06`'s answered gates step back and then all
  three return; `07`'s emphasis moves from the promising half to the
  developing half
- **`05` gained `BarrierWall`'s shard mechanism**, which the component check
  said was being adapted but the first build had dropped: three brick fragments
  detach and fall after the channels drive through

### 4. Findings deliberately NOT acted on

- **Six region-aware "content-voids."** All six extracted and inspected; all
  six are false positives. Two are the photographic plate itself (a smooth
  gradient reading as empty — exactly the class that script's own docstring
  warns about), one is legitimate negative space beside a left-aligned
  headline, and three carry full headline text. The whole-frame static-hold
  scan reported no findings, and no scene is frozen.
- **Three engine contrast warnings** (1:1, 1:1, 2.02:1). All three sample a
  reveal bar **mid-wipe**, while its `overflow:hidden` window is ~15px wide, and
  measure the clipped text against the page ground it never actually renders
  on. Measured on real pixels once the bars are open: **16.88:1** and
  **14.15:1**. `scripts/check-contrast-pixels.py` was written to do that
  measurement properly and is now part of `postrender`.

### 5. `postrender` no longer hides its own findings

The house `postrender` chains checks with `&&`, so the first failing gate
silences every check after it. On round 2 the safe-area gate failed and
`check-cadence` therefore **never ran** — a reader skimming that output would
reasonably have concluded cadence was fine when it had simply not been
measured. `scripts/run-checks.py` now runs every check unconditionally and only
the aggregate decides the exit code.

---

## Round 2 — scene splits, the end card, and the under-fill defect

Round 1 shipped seven scenes and closed with cadence at 5.6% against the
channel's shipped reference of 13.6%, with a recommendation to split the long
scenes rather than keep tweaking motion. Round 2 does that, plus two things the
operator asked for directly.

### 1. Three scenes split (7 → 10)

Cut points were chosen at **real silence gaps between caption cues**, so no cut
lands mid-phrase and the VO clips stay untouched:

| old | cut at | halves |
|---|---|---|
| `03-materials` 13.5s | 20.880 | `03a-materials` 7.83s + `03b-transfer` 5.67s |
| `05-barrier` 12.8s | 44.480 | `05a-barrier` 8.38s + `05b-intact` 4.42s |
| `07-verdict` 8.25s | 63.120 | `07-verdict` 3.92s + `08-endcard` 4.33s |

Each pair shares its ground, so **structure carries the cut**: a tile grid
against a name stack, a breached wall against an intact-wall/skin compare, pure
type against a brand lockup with the hero plate. Mean scene length 9.64s → 6.75s.

### 2. The end card was missing — added as its own scene

The operator flagged that the video had no end card and no SeoulHabit logo.
Round 1 had only a text sign-off bar tucked inside the verdict scene, and no
brand mark anywhere.

`08-endcard` is now a scene in its own right carrying the channel's **습 mark**,
set as **type rather than an image**: the glyph is present in this project's own
`NotoSansKR-500-subset` (verified U+C2B5), so it renders crisp at any size and
takes `--ink` directly. It sits in a 132px bordered square beside the SeoulHabit
wordmark — the same relationship the channel avatar uses.

The **coral watermark variant was not used**: coral is spent once per video and
this piece spends it on the barrier refusal.

**Font-subset finding, worth recording.** Checking the subset for 습 revealed
that `세럼` (scene 01) and `엑소좀` (scene 02) are **not in it** — the 49-glyph
subset covers only the 습 family. Those strings render correctly only because
the engine auto-fetches and injects Google Fonts for the named family at
check/render time. Not currently a defect, but the local subset does not stand
on its own and an offline render would show tofu.

### 3. The real reason cadence was low: under-filled frames

Chasing the cadence number surfaced a genuine craft defect rather than a metric
artifact. `04-source` measured **1%** active steps and `05a-barrier` **2%**, and
extracting their frames showed why: the branch tree and the wall were
proof-scaled into a mostly-empty canvas, occupying roughly a third of the safe
column with large dead bands above and below. That is the skill's named 9:16
under-fill failure — the one that reads as "small fonts" even when the type
clears the floor.

Fixes were to the composition, not the motion:

- **`04-source`** chips 34→46px, kid chips 32→40px with celadon borders instead
  of near-invisible `--rule-dark` on ink, drop rails 62→128px. **1% → 13%.**
- **`05a-barrier`** wall 540→780px, and its internal contrast was **backwards**:
  bricks (#DCD5C6, luma 217) sat on a *lighter* mist ground (236), so the mortar
  gaps read as highlights and the whole wall washed out. Dark mortar (#8C8371),
  light bricks. **2% → 5%.**
- **`02-what`** diagram viewBox 430→620px with vesicles roughly doubled.
  **6% → 10%.**
- **`03a-materials`** tiles given 4px ink borders and elevation — cream plates on
  a cream ground changed only ~13 luma per pixel and barely registered.

A second, subtler cause: **tween duration, not size**. A channel driving through
the wall over 0.40s spreads its change across ~3.2 sampling steps at 8fps, so
each step moved only ~0.44 mean luma — under the floor despite the channel being
5% of the canvas. Concentrating the same motion into ~1.5 steps clears it, and a
0.18s puncture reads sharper than a 0.40s slide anyway.

Whole-video cadence across the round: **5.6% → 7.1% → 9.9% → 10.9%**.

### 4. Safe-area regressions, all self-inflicted, all fixed at the mechanism

Every new scene introduced its own edge violation, and each was an entrance
transform on an element already sitting on a safe line — the same class round 1
documented, now with three more instances:

- `03a` transform-origin was set on `.cell` while the scale tween targeted
  `.plate-wrap`, so it did nothing and the first tile's back.out() overshoot put
  ink at x=70.
- `03a`'s index chip was outdented `right: -10px`, putting the third tile's chip
  10px inside the reserved engagement rail.
- `05a`'s foot label entered with `y: 20` from a block whose bottom is the 1536
  line, and its coral stamp's back.out() overshoot pushed 1px past.
- `08-endcard`'s brand row entered with `y: -22` from the top safe line, and the
  mark's centre-origin scale pushed it past the left line — 560px in both zones.
- `02-what`'s citation pill, now last in a stacked foot, overshot the bottom line
  by ~6px.

None was fixed with margin. Each was fixed by removing the offending translation
or by anchoring `transform-origin` to the edge the element actually sits on, so
the overshoot grows inward.
