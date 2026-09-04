# BRIEF — Ectoin: Explained by SoulHabit, and Then by a Normal Person

**Slug** `ectoin-normal-person` · **Format** 1920×1080 long-form ·
**Engine** `hyperframes@0.8.22` · **Authoring skill** faceless-video-craft

## Cold-open revision (2026-09-03)

Operator feedback rewrote the opening: the "11% bottle → it's a blend → turn
the bottle around" payoff now opens the video at frame 0; the bacteria-origin
material compresses to one narrated raisin beat; the section closes on
"Skincare borrowed the molecule. Marketing borrowed the drama." Full account
in `SCRIPT.md` §Changes and this file's §Structure, §Claim table below.
Mode: `full (revision)` — S0–S3 skipped (subject/seed unchanged, reused from
the shipped 5:59 cut at commit `406ad4f`); S4–S7 ran; S8 updated in place;
S9 skipped. Runtime: 5:59.01 → 4:57.02. Decisions taken with the operator
before work began: trim CH5's repeat of the same reveal (`12-bottle` keeps
who-it's-for and the INCI payoff, drops the turn itself); ship a generic
illustrative bottle, no brand; revise in place on the working branch rather
than a sibling recut directory. Full run record in `00-decision-ledger.md`,
`00-environment.md`, `09-run-report.md`.

## Format

`data-resolution="landscape"`, 1920×1080, 30fps. Safe areas
`--safe-top:54 --safe-bottom:108 --safe-left:96 --safe-right:96`; end-screen
reserve `--endscreen-right:640 --endscreen-bottom:200` is **scene-scoped to
`18-endscreen` alone** — the Shorts rails bind every frame, the end-screen zone
binds only the last 5–20s, so reserving it globally would waste the right third
of every frame.

**Type scale is unchanged from the Shorts lane.** Both canvases share a 1080px
short edge and type size is a fraction of the short edge, so the scale transfers
one-for-one. Layout gets a landscape variant; type does not. Do not scale it in
either direction.

## Assumptions on record

Two numbers here are **assumptions, not measurements.** Recorded so a later
review knows the difference.

- **Duration ~5:00–5:30.** Derived from 677 spoken words at this channel's
  measured pace, not authored. The script header said 3:30–4:00; that was wrong
  by roughly 40%. Real timing comes from ffprobe'd VO and is written into
  `STORYBOARD.md` by the generator. **Superseded the moment VO exists.**
- **Long-form hook window.** `faceless-video-craft` says ~8s; the v2 package
  says ~15s. Neither is measured on this channel, and this channel's only
  long-form retention comparison is marked `[UNDERPOWERED]`. **This build
  assumes 8s** and puts the payoff at t≈0. Not citable as a cause of anything.

## Voices

Two speakers, no repo precedent — this is the first two-voice piece here.

| | SOULHABIT | JAY |
|---|---|---|
| Role | calm, credible, occasionally too technical | audience rep who translates |
| Voice | **Kimberly**, the standing series voice — Higgsfield `seed_audio`, `voice_type element`, `674b71b8-1d2e-4087-8567-d1f53c0b9f3c` | **TBD — auditioned, awaiting selection** |
| Type | `--font-display` EB Garamond, `--t-hero` | `--font-body` Inter 800, `--t-figure` |
| Mark | `--aqua` rule | `--coral-deep` on paper / `--coral` on ink |
| Bus | `vo-soulhabit`, chain **verbatim** | `vo-jay`, same topology, two deltas |

JAY's chain deviates from the channel's standing chain in exactly two params,
and the reason is stated because deviating needs one: **weight 0.8→0.3** (a
brighter voice muddies with the 150Hz lift) and **de-ess −4→−6** (a brighter
voice sibilates harder through the same limiter). Highpass, compressor, clarity
and ceiling are identical, so the pair reads as one room.

### Attribution is carried by TYPE alone

There are no persistent speaker rails. That was an explicit operator decision
and it has a cost: **no actor spans a cut by default**, which is exactly how the
predecessor passed every per-scene gate and still read as an animated
presentation. Two compensations, both structural:

1. **A serif/grotesque split, not a colour split.** EB Garamond against Inter
   800 survives any ground, any scale, and the 25% phone-scale check. Colour
   would not — see below.
2. **Camera and merged actors carry continuity instead.** See the beat sheet.

### The contrast finding

`--coral` is the channel's accent and the obvious choice for JAY. **Measured, it
is 3.00:1 on paper** — under the 4.5:1 floor. Every JAY line on a paper ground
would have shipped illegible. `scripts/contrast.py` holds the measurement:

```
PASS  5.60:1  --coral      on ink        FAIL  3.00:1  --coral      on paper
PASS  4.60:1  --coral-deep on paper      FAIL  3.66:1  --coral-deep on ink
```

So `--coral-deep:#A85A3C` was added and **both corals are ground-scoped** — the
same split the token set already uses for `--ink-2` / `--ink-2-dark`, for the
same reason. The speaker *mark* is decorative and never carries legibility, so
a wrong-ground colour can never become a readability bug.

## Structure — 17 units, 28 phases, 58 turns

**Cold-open revision (2026-09-03):** was 18/31/70. `01-hook`, `02-industry`,
`03-cell` retired (12 turns); two new merged units `01-bottle`/`02-origin`
open the video (7 turns, one reused: t002/t003); `12-bottle` drops phases
b/c (4 turns) since their reveal now opens the piece. Net new: t071-t075.

A **unit** is one sub-composition file. A **phase** is a beat inside it. Four
units are **merged**: one actor, several phases, rearranged rather than
redrawn. That converts **13 beats that would have been hard cuts into internal
phase transitions**, which is where this build's continuity comes from.

The predecessor has **0 merged units** and its `09-exclusion.html` /
`10-messier.html` carry byte-identical protein+shell geometry — one actor drawn
twice in two files. Here that whole run is unit `04-protein`: five phases, one
actor, ring rearranging.

### Beat sheet — camera path and actor map

Camera legs are planned here, at beat-sheet time. Decided in the motion pass
they would mean re-authoring every scene's markup.

| # | Unit | Ph | Camera | Actor | Boundary in |
|---|---|---|---|---|---|
| 1 | `01-bottle` **M** | 2 | no baseline camera move -- extreme close-up is a layout choice, not a zoom (a tried 1.28 baseline zoom pushed the two-column grid off-canvas, measured, removed); a brief fly to the real INCI position during the turn | bottle *(persists, 2 phases)* | — (frame 0) |
| 2 | `02-origin` **M** | 3 | **L0→L1→L2** crystal field → push into one cell → push to the molecule | crystal field → cell → molecule *(persists, 3 phases)* | wipe LEFT |
| 4 | `04-protein` **M** | 5 | **L2→L3** to the protein | protein+shell *(persists, ring rearranges)* | **wipe UP · CH2** |
| 5 | `05-skin` **M** | 4 | **L3→L2′** pull out to skin | keratin strands *(persists)* | **wipe UP · CH3** |
| 6 | `06-trial104` | 1 | **L2′→L1′** to the evidence plane | 104-dot cohort | **wipe UP · CH4** |
| 7 | `07-preference` | 1 | L1′ hold | cohort *(persists)* | wipe LEFT |
| 8 | `08-eczema` | 1 | L1′ lateral | two bars | wipe LEFT |
| 9 | `09-miracle` | 1 | L1′ hold | bars *(persists)* | wipe LEFT |
| 10 | `10-notprove` | 1 | L1′ hold | three struck claims | wipe LEFT |
| 11 | `11-twelve` | 1 | L1′ lateral | 12 tiles | wipe LEFT |
| 12 | `12-bottle` **M** | 2 | **L1′→L1″** who it's for → INCI (camera flies to the real position); the front-label/turn phases retired -- that reveal now opens the video | bottle *(persists, already turned; camera does the work)* | **wipe UP · CH5** |
| 13 | `13-kbeauty` | 1 | **L2″→L0′** pull back to the shelf | shelf | wipe LEFT |
| 14 | `14-notnew` | 1 | L0′ hold | shelf *(persists)* | **wipe UP · CH6** |
| 15 | `15-whatitis` | 1 | L0′ hold | verdict panel | wipe LEFT |
| 16 | `16-action` | 1 | L0′ hold | the closing action | wipe LEFT |
| 17 | `17-dignity` | 1 | L0′ hold | — | wipe LEFT |
| 18 | `18-endscreen` | 1 | no camera journey -- both ends are already #world's rest state | bottle **returns** (was brine, retired with 01-hook) | wipe LEFT |

**9 camera legs**, against the predecessor's **0** -- unchanged count this
revision: `01-bottle`'s own fly-to-INCI leg (new) replaces one of the two
legs `12-bottle` lost when its front-label phases retired. One continuous
space: bottle → brine → cell → protein → skin → evidence → bottle → shelf →
back to bottle, so the piece bookends and a replay hands back cleanly.

**Transitions**: 12 wipe-LEFT (within chapter, 0.45s), 5 wipe-UP (chapter
opener, 0.60s). No crossfade anywhere — grounds alternate ink/paper and a plain
crossfade gives a muddy near-blank midpoint. Not a push either: a translating
push failed the predecessor's hard safe-area gate on **99 frames**, because
sliding a full-canvas scene drags its content through the reserved zones. A
wipe moves nothing.

## Claim table

Every on-screen citation is `Journal · Year`. **No PMID, no internal id, ever
renders** — those live here and in the description.

| # | Claim | Unit | Source | On-screen pill |
|---|---|---|---|---|
| C1 | *Halomonas elongata* lives in hypersaline conditions and makes ectoin | `02-origin` | Schwibbert 2010, *Environ Microbiol* · `10.1111/j.1462-2920.2010.02336.x` | `Environ Microbiol · 2010` |
| C2 | preferential exclusion / preferential hydration | `04-protein` | Sahle 2018, *Phys Chem Chem Phys* · `10.1039/c8cp05308a` | `Phys Chem Chem Phys · 2018` |
| C3 | the real behaviour is more complicated — exclusion is size/surface dependent | `04-protein` | Yu 2007, *J Phys Chem B* · `10.1021/jp068367z` | `J Phys Chem B · 2007` |
| C4 | keratin in the outer skin layer interacts with water | `05-skin` | Bow 2021, *Biochem Biophys Rep* · `10.1016/j.bbrep.2021.101134` | `Biochem Biophys Rep · 2021` |
| C5 | 104 women, 2% ectoin vs vehicle, **preference** outcome | `06-trial104` | Heinrich 2007, *Skin Pharmacol Physiol* · `10.1159/000103204` | `Skin Pharmacol Physiol · 2007` |
| C6 | 65 patients, mild–moderate AD, 4 weeks, equivalent to comparator, well tolerated | `08-eczema` | Marini 2013, *Skin Pharmacol Physiol* · `10.1159/000351381` | `Skin Pharmacol Physiol · 2013` |
| C7 | twelve clinical trials | `11-twelve` | PubMed `ectoine AND Clinical Trial[pt]`, **retrieved 2026-09-02, count 12** | `PubMed · 2026` |
| C8 | some research is tied to companies that sell it | `10-notprove` | Bilstein (bitop AG) is a named author on C6 and ≥2 others | plain content, not a pill |
| C9 | the bottle's front label reads "11%", turned around it's a blend | `01-bottle` | **illustration** -- an authored prop, not a real product. `[K-2a]` bars an unsourced quantity from rendering as measurement whatever sits beside it; this ships as `[Authored, illustrative -- not a claim]` via a muted `ILLUSTRATIVE LABEL` tag (`--ink-2`, mono, never the accent, never citation typography) inside the bottle, not a pill | none -- illustrative-label tag, not a citation |
| C10 | the salt pulls water out of the cell; ectoin keeps the machinery stable | `02-origin` | reuses C1 (Schwibbert 2010) for the organism/mechanism and C2 (Sahle 2018, preferential exclusion) for the stabilising claim -- both already on file and read for this project | `Environ Microbiol · 2010` / `Phys Chem Chem Phys · 2018` |
| C11 | "Skincare borrowed the molecule. Marketing borrowed the drama." | `02-origin` | editorial -- asserts no outcome, no `K-1` classification needed | none |

**C7 is a live number.** It was verified by query on 2026-09-02, not recalled.
Re-run before publish if that date has drifted; the pill carries the year for
exactly this reason.

## Known-bad line, shipped by operator decision

`t048` — **"None of it passed peer review."**

This is **false**. All twelve trials in C7 are peer-reviewed articles in indexed
journals; that is what PubMed indexes. It also contradicts C5 and C6, which the
video cites approvingly about 30 seconds earlier.

It was raised, and the operator elected to keep it. Exposure is limited as far
as craft allows:

- **VO only.** No on-screen text, no headline, no citation pill, no reinforcement.
- Not used as a section button or a chapter title.
- Recorded here and in `DELIVERY.md` so it is not mistaken for a sourced claim.

## Other script changes

1. **Hook reordered** — payoff at t=0. The draft's opening targeting line was
   deleted; §6 already opened with the same sentence, so this fixed the hook
   and removed a repetition at once.
2. **Unverified claim cut** — "under extremely dry conditions, one stress
   measurement actually became worse" did not surface in PubMed. SOULHABIT now
   answers "No."; JAY's joke lands off the denial.
3. **"Extremolytes" glossed** — the one technical term JAY never translated.

## Motion budget

Landscape, so beats are budgeted by **fraction of frame changed**, not by
counting tweens. *A beat moves a panel or a column, never a word.* Target
**area ≥ 8% and luma delta ≥ 80 within ≤0.8s**; pick beat colour by
**luminance, not hue** (celadon→coral is 27 luma and measures as nothing).

The predecessor's word-scale pilot measured **5.8%** active steps; its
panel-scale rebuild, **12.7%**; its final with wipes, **14.0%**. Shipped 9:16
comparators are 11.7% and 23.1%.

**No timeline-wide `defaults: { ease }`.** That single inherited default gave
the predecessor **65.3% of its tweens one signature** while a grep for `ease:`
returned 8 hits and reported variety. It is removed from `scene()`; every beat
picks its ease from what it is doing narratively.
