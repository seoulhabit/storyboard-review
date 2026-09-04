# Story brief — hyaluronic-acid-vs-filler

**Source:** operator-supplied script, "HYALURONIC ACID HAS THREE DIFFERENT IDENTITIES",
7 scenes, two characters (SoulHabit, Jay), stated runtime ~3 minutes. Revised
2026-09-03 (operator feedback on the 180 s two-hander, commit `48c29d9`) into
a **single-narrator 160 s cut** — see §v2 Revision below. The two-hander stays
recoverable at `48c29d9`; this file describes the shipped v2.

| Field | Value | Rule |
|---|---|---|
| Format | **long, 16:9, 1920×1080** | `[S1/S-1]` branch 1, operator-directed — see §Format override |
| Target length | **160 s** | `[S1/S-2]`, `below-clamp`; operator asked "approximately 2:20–2:40" (140–160 s) — see §v2 Revision §Length |
| Presenter | **moving diagram** | `[S1/S-3]` mechanism-heavy (three parallel mechanisms) |
| Voice | **single narrator** — Kimberly only | `[S1/S-4]`; the two-hander gap this brief originally logged no longer applies — see §v2 Revision §Cast |
| fps | 30 | `[S6/A-4]` — no fast counters |
| Route angle | `concept` | `[S1/S-7]`: six-section spine with a named wrong belief |
| `VO_MODE` | `use it verbatim`→`restructure per scene` | script supplied, but reworded under `[K-2]`; see §Rewordings |

---

## §v2 Revision — single narrator, 160 s, ten new visuals

Operator feedback asked for a tighter, visually richer film with one female
narrator, landing the serum/filler contrast inside the first minute, and ten
named supporting visuals returning to the three-lane diagram as a backbone.
Nothing about the underlying science changed — every claim below carries the
same backing it did in the 180 s cut; C0 is the only new claim.

### What changed structurally

- **Two-hander → single narrator.** All 12 Jay turns dropped. Three of his
  strongest lines survive as rhetorical asides in Kimberly's own voice — she
  poses the question, then answers it (see `04-assets/script.md`'s table).
- **14 scenes → 13.** The "three cousins named Rahul" misconception scene is
  cut outright; the two origin scenes (1934 / cow's-eye) compress into one
  7-second sentence, preserving the cow-eye reference as a closing callback
  per the feedback's explicit instruction.
- **180 s → 160 s.** Not the requested 150 s midpoint: trimmed speech alone
  (13 stems, single voice) measures 151.75 s, leaving no gap budget at a 150 s
  target. 160 s is the top of the requested 2:20–2:40 band and reproduces the
  180 s cut's own gap pacing almost exactly (turn gap 0.52 s vs. the shipped
  cut's 0.469 s) — see `04-assets/build_vo.py` and §Length below.
- **Ten new hand-authored visuals**, all browser-drawn SVG (no generated
  imagery — `catalog/manifest.json` excludes HyperFrames composition surfaces
  from generative imagery, and the shipped cut had zero raster in-frame
  images; that stays true). Mapped to scenes:

| # | Visual (as briefed) | Scene |
|---|---|---|
| 1 | Serum bottle / body silhouette / syringe as three categories | `s01-lineup` |
| 2 | Skin cross-section, natural HA among structures + water molecules | `s04-body` |
| 3 | 1930s scientific illustration, eye + lab glassware | `s03-origin` |
| 4 | Skin-layer diagram, large vs. small HA chains, labelled "simplified illustration" | `s06-serum-size` |
| 5 | HA molecules attracting/holding water droplets (animated, not implying creation) | `s08-binds-water` |
| 6 | Moisturiser layer slowing water loss + brief lifeguard/pool caption | `s09-lifeguard` |
| 7 | Side-by-side cross-section: serum at surface vs. filler beneath | `s05-compare` |
| 8 | Loose chains transforming into a connected grid | `s10-crosslink` |
| 9 | Calm clinical environment (no needle entering skin) | `s11-do-not-inject` |
| 10 | Final recap: resident / moisturiser / construction project | `s12-badges` |

The engine supports only `opacity, x, y, scale, scaleX, scaleY, rotation,
width, height, visibility` on a paused timeline (`hyperframes-engine.md` §3) —
no path-attribute morphing. Visual #8's "transform" is therefore a scale-swap
crossfade between two pre-drawn states (loose chains fading out, lattice
fading in), the same idiom `[S6/A-10]`'s `swap` already names for "a myth
transforming into its correction rather than being replaced by it." Verified
on the extracted frame at t≈107s (loose) and t≈112s (lattice, settled).

`catalog/` checked per `[S6/A-1]` before drawing anything: `MoleculeStates`
(harvested from this project's own 180 s cut) reused unchanged for the three
persistent actors; a real skin-layer cross-section was a confirmed catalog
gap, built here and harvested back to `catalog/visual-components/skin-band/`
at the end of this run.

### §Length

Target **160 s**. Long clamp is 4:00–12:00, so this remains `below-clamp` —
same reasoning the 180 s cut recorded: the clamp governs a target *derived
from baseline*, and there is no long-form baseline to derive one from. An
operator-supplied runtime band is a stated input, not a measurement that
would defeat its own rule. 160 s sits at the requested band's own stated
upper bound, chosen over 150 s because the alternative was cutting real
content (the FDA safety passage, primarily) to force a lower number.

### §Cast

| Character | Voice | id | Type |
|---|---|---|---|
| Narrator | Kimberly | `674b71b8-1d2e-4087-8567-d1f53c0b9f3c` | element |

Kimberly is unchanged from the 180 s cut — the established channel voice,
not rotated. Jay/Grady is dropped entirely; the `[NOT IN SKILL]` two-hander
gap the original brief logged (`[S1/S-3]` one presenter, `[S1/S-4]` one voice
never rotated, `[S4/V-2]`'s cap assumes one VO) **no longer applies to this
video** — it returns to being a standard single-voice `[S1/S-4]` case. The
filed policy proposal in `videos/_channel/policy-change-proposals.md` stands
for any future multi-character script, not retracted, just not exercised here.

### Pacing direction

"Warm, intelligent, confident — conversational, lightly playful, never
salesy, breathy, robotic or dramatic," with short pauses after contrasts, is
carried by line construction and `GAP_SECTION` placement (1.8× the turn gap,
landing after the thesis, after the serum/filler split, and before the FDA
line), not a synthesis style parameter — this provider/voice combination
doesn't expose one. Kimberly's own documented pacing hazards (no colons in
any spoken line — one silently killed a take previously; full stops cost
~1.6 s each; numerals and acronyms spelled out) carried over unchanged.

---

## The six-section spine (v2 scene numbers and measured times)

| § | Content | Scenes | Time (measured) |
|---|---|---|---|
| **Hook** | Your serum cannot do what filler does — three things, one name. | `s01-lineup` | 0–14.7 s |
| **Misconception** | A serum is not filler in a bottle; the name goes back to 1934. | `s02-not-filler`, `s03-origin` | 14.7–28.7 s |
| **Mechanism** | Your body's version; where the two forms split; molecular size; plumping. | `s04-body`…`s07-plumping` | 28.7–80.3 s |
| **Proof** | It binds water, it does not make water; cross-linking is the structural difference. | `s08-binds-water`…`s10-crosslink` | 80.3–114.9 s |
| **Application** | Do not inject yourself — the FDA's own wording, not ours. | `s11-do-not-inject` | 114.9–136.0 s |
| **Recap + end scene** | Three badges; the final message, held; the cow-eye callback. | `s12-badges`, `s13-endcard` | 136.0–160.0 s |

`[S1/S-5]` — all six sections still carry distinct content, grounded in the
original supplied script plus the operator's revision feedback. Nothing is
`[UNGROUNDED]`. `[GEN]` bridging lines are marked in `04-assets/script.md`.

Serum-vs-filler side-by-side (`s05-compare`) lands at 39–53 s, comfortably
inside the "first minute" the feedback asked for. Three versions introduced
by 9.9 s inside `s01-lineup`, inside the requested "first 10 seconds."

---

## Format override — `[S1/S-1]`

Unchanged from the 180 s cut — branch 1 fired: the operator directed 16:9
long-form, overriding branch 2 (which would have selected `short`). The
share it overrode, stated rather than implied:

- views, 90 d: shorts **4730** vs videoOnDemand **26** → 99.45 % short
- uploads, 90 d: **46 short / 2 long** (baseline `corpus`) → 95.8 % short
- repo corpus: **30 of 31** built projects are 9:16

Consequences carried, per the first-of-kind clause:

1. **Every `curve.*` and `retention.*` comparison in this run is `[UNDERPOWERED]`.**
   `baseline-notes.md` independently reaches the same conclusion from the other
   direction: "This channel has no public long-form, so the curve is necessarily
   built from Shorts. Any rule reading `curve.*` as a long-form signal is reading
   Shorts data." No readout may rank this video against that curve.
2. **Format-specific gates are re-pointed, not inherited.** Safe areas are
   54/108/96/96, not the Shorts 192/384/162/72. `check-safe-area.py` and
   `check-static-hold.py` take `--landscape`; `check-cadence.py` takes `--longform`.
   A portrait-calibrated gate on a landscape render is confirmed to **report a
   silent clean pass** — the bottom-zone slice runs off the end of a 1080-tall
   array and numpy returns an empty view.
3. `[S3/P-3]` runs the **long-form** branch: a thumbnail is generated and scored.
4. **Not fully first-of-kind** — `videos/ectoin-survival-molecule` and this
   video's own 180 s predecessor are working repo prior art at this format.

## Cast — `[S1/S-4]`

See §v2 Revision §Cast above — this section is superseded there.

---

## §Sourcing — the `[K-1]` claim table

Every identifier below was **fetched and read during the original run**, not
recalled, and carries unchanged into v2. Chips render as `Journal · Year` or
`FDA · <page>`; DOIs and PMIDs live in the description only. **No PMID and no
`ING-*` reaches a frame.**

| # | Claim (as it will render) | Class | On-screen chip | Backing — verified |
|---|---|---|---|---|
| C0 | A hyaluronic-acid serum cannot do what a filler does | **sourced** | `J Cosmet Dermatol · 2024` | The v2 opening thesis. A distinction, not comparative superiority — same reasoning that cleared "Neither behaves like an injectable filler" below. Backed by C5/C7 for the serum half and C8/C9 for the filler half; the chip renders on `s01-lineup` and again on `s05-compare` so the thesis is not chip-less through the hook. |
| C1 | Three things share the name "hyaluronic acid": the kind in your body, the kind in a serum, the kind in a filler | nominal | none | Identity. Asserts no effect. |
| C2 | In 1934 it was isolated from the vitreous of a cow's eye and named there | **sourced** | `J Biol Chem · 1934` | Meyer K & Palmer JW, *J Biol Chem* **107**:629–634, `10.1016/S0021-9258(18)75338-6`. Named from *hyalos* (glassy) + uronic acid. Clears `[K-2a]`'s unsourced-number bar — the year is a citation, not a measurement. |
| C3 | Your body makes it; most of it sits in your skin, where it holds water | **sourced** | `Dermatoendocrinol · 2012` | Papakonstantinou et al., PMID 23467280, `10.4161/derm.21923` — "The key molecule involved in skin moisture is hyaluronic acid (HA) that has unique capacity in retaining water." |
| C4 | It also lubricates joints and is found in the eye | **sourced** | `Front Vet Sci · 2019` | Gupta et al., PMID 31294035, `10.3389/fvets.2019.00192` — "naturally found in many tissues and fluids, but more abundantly in articular cartilage and synovial fluid… partially responsible for lubrication and viscoelasticity". Split from C3 deliberately so each chip sits on the claim it actually supports. |
| C5 | In a topical, molecular size governs how far it gets: larger stays at the surface, smaller can reach the upper layers | **sourced** | `Skin Res Technol · 2015` | Essendoubi et al., PMID 25877232, `10.1111/srt.12228` — LMW (20–300 kDa) "passes through the stratum corneum in contrast of the impermeability of high molecular weight HA (1000–1400 kDa)." Corroborated, not chipped: PMID 37004799 (5–8 kDa through SC; HMW "trapped on the SC surface"). |
| C6 | Hydrated surface cells can temporarily make fine lines **appear** softer | **sourced** | `Dermatoendocrinol · 2012` | Same as C3 — a moisture/appearance claim, correctly hedged. `[K-3]`: "appear" and "temporarily" carry into the on-screen type, not just the VO — verified on the extracted frame. |
| C7 | It binds and holds water — it does not create water. A formula also needs to stop that water leaving. | **sourced** | `ChemRxiv · 2023` | Reused: `ING-hyaluronic-acid-S001`, `videos/hyaluronic-acid-serum/BRIEF.md` — *Fallacy of Hyaluronic Acid Binding a Thousand Times Its Weight In Water*, `10.26434/chemrxiv-2023-r728q`. Real capacity ~10–100× by MW. `[S6/A-1]` reuse, not re-research. |
| C8 | Filler HA is **cross-linked** into a gel that holds its shape | **sourced** | `J Cosmet Dermatol · 2024` | Hong et al., PMID 39466959, `10.1111/jocd.16652` — "Uncrosslinked HA degrades rapidly due to endogenous hyaluronidase, while crosslinked HA undergoes slower degradation"; BDDE cross-linking. Corroborated: PMID 39107664. |
| C9 | Placed under the skin, that gel can physically add volume | **sourced** | `J Cosmet Dermatol · 2024` | Same — histology shows collagen capsule formation and autologous tissue replacement post-injection. Nothing here is a claim about how long it lasts, which varies by product and is deliberately not asserted. |
| C10 | **Do not inject yourself.** | **sourced**, REWORDED | `FDA · Dermal Fillers` | FDA, *Dermal Fillers (Soft Tissue Fillers)*, rev. 2023-07-06, verbatim: **"Do not inject yourself with dermal fillers."** |
| C11 | Fillers are a medical procedure with real risks, for trained providers only | **sourced** | `FDA · Dermal Fillers` | Same page, verbatim: "Select a health care provider who is trained to perform the dermal filler injection procedure"; risks "include necrosis (death of tissue), vision abnormalities including blindness, and stroke." |
| C12 | The three surviving analogies (tired houseplant, empty-pool lifeguard, construction project), the title, and the end card | editorial | none | Narrowed from the 180 s cut's C12: the "cousins at a wedding" scene is cut and "cow royalties" was never in the shipped VO. Asserts no outcome. Subject to the absolute-language ban — no *guaranteed / instantly / proven / always / useless*. |

**Counts.** nominal 1 · **sourced 11** · unsourced **0** · illustration 0 · editorial 1.

`[K-2b]` **ratio limb: does NOT fire.** Across Mechanism (C0, C5–C6) and Proof
(C7–C9), sourced : unsourced is **6 : 0**. The video ships as a normal explainer,
not disclosure-forward. No `unsourced-flag` component is needed and none is
emitted — recounted for v2 rather than assumed to carry from the 180 s cut.

`[K-2a]` **hard-prohibited set: clear.** No unsourced safety claim (C10/C11 are
FDA-verbatim), no unsourced quantity (the only number on screen is 1934, cited),
no *treats/prevents/cures*, no comparative superiority, no absolute language.
Checked again on pixels at `[K-4]` — see `06-render/qa-log.md`.

### Rewordings applied before the script is written

Carried unchanged from the 180 s cut, plus one new v2 entry:

1. **"Never inject a topical serum" → "Do not inject yourself."** FDA's actual
   sentence is *"Do not inject yourself with dermal fillers."* The original
   wording narrows the warning to serums and, read literally, leaves
   self-injecting an actual filler unaddressed — the more dangerous act, and
   the one the regulator names. Retained as the large-type callout.
2. **"skin, joints and eyes" split into two claims (C3, C4)** with separate
   chips, because the skin source does not cover joints and the joints source
   is not a dermatology paper.
3. **"Neither behaves like an injectable filler"** kept, and **C0 extends the
   same reasoning to the opening thesis** — a distinction, not a
   comparative-superiority claim.
4. **"plumping"** — "can temporarily make fine lines *appear* softer" carries
   through unchanged; `[K-3]` pushes the same hedge into the on-screen type.

### Evidentiary limits, recorded rather than left implicit

- C5 is measured **ex vivo / in vitro** (Raman micro-imaging on skin sections;
  Franz-cell and ELISA tape-strip work). It supports "smaller forms can travel
  farther into the upper layers"; it does **not** support any claim about a
  clinical outcome from that travel. The script's own "may" is doing real work.
- C9 says a filler gel "can physically add volume" — sourced for the mechanism.
  Nothing here is a claim about how long it lasts, which varies by product and is
  deliberately not asserted.
- C4's source is a comparative-physiology review spanning species. It is cited for
  where HA sits in the body and what it does there, which is what it establishes.

## §v3 Revision — voiceover rewrite, photoreal plates, 165.186s

Full detail in `00-decision-ledger.md`'s `## re-run — v3 revision` section.
Summary of what changed from v2 and why:

- **Voiceover fully rewritten**: 13 stems → 24, shorter sentences, a
  curiosity-gap hook replacing the thesis-first open, natural fixed-second
  pauses replacing v2's gap-scaled-to-a-target assembly. Every claim (C0-C12)
  and every citation below survives unchanged in substance; only the
  surrounding sentences changed. Runtime is now a **measured output**
  (165.186s), not a number the script was built to hit.
- **13 scenes → 17**, so a real development lands roughly every 5-8s at the
  beat level (validated against `validate_beat_sheet.py`'s own 8.0s
  END_SCENE_MIN_S / 10.0s CHAPTER_MIN_GAP_S floors, which forbid chopping
  every scene to a literal 5-8s without starving a chapter or the end scene).
- **A genuine `[S6/A-9]` actor merge** replacing two scenes that redrew the
  same molecule chain (see ledger).
- **A three-type transition system** (wipe-left / wipe-up / blur-crossfade)
  plus three deliberate hard cuts, replacing two flat wipe types across
  every boundary.

### §v3 Imagery — the face-rule override

**This is the one deliberate departure from every prior revision's own
stated rule, made on explicit operator instruction, not silent drift.**

v2's own text above (§v2 Revision) states: *"no generated imagery... the
shipped cut had zero raster in-frame images; that stays true."* It is no
longer true. This channel's `frame.md` convention, confirmed identical
across roughly ten sibling projects, bans a visible face in any plate:
*"No talking-head footage, no visible faces at any point — every plate is
hands-below-wrist or texture-only."*

Asked directly whether to honor that rule with a face-free treatment or
override it for a full photorealistic subject, the operator chose to
**override it** (`AskUserQuestion`, this run). Four photoreal plates of one
consistent adult female subject — natural skin texture, minimal makeup, dark
hair, neutral cream clothing, Korean-skincare-editorial register, realistic
hands — now appear at exactly the four moments the revision brief named: the
opening misconception, "a serum is not filler in a bottle," the temporary
surface-plumping explanation, and the final practical takeaway. She is never
shown self-injecting, and no shot implies a topical serum reproduces a
filler's result — both explicit constraints from the brief, held throughout.

**This is not unprecedented on the channel** — `videos/ceramides-skin-
barrier` already ships full photoreal female faces in a HyperFrames
composition, filed in its own `BRIEF.md` as *"a visible, reversible decision
rather than quiet drift."* Same standard applied here: named, dated, and
attributed to an explicit instruction rather than left for a future reader
to wonder whether it was an oversight.

**What did not change:** the underlying scientific claims, every citation
below, the FDA warning's wording, and the rule that no citation chip ever
shares a frame with a generated plate (adopted from `videos/pilling-vs-
peeling`'s own filed convention, so a photo is never dressed as cited
evidence).

**Provenance and defects found in generation are logged in
`04-assets/manifest.json`**, not repeated here — two of the four plates
needed one regeneration each (a subject-consistency miss and garbled
prop-bottle text on one; an unrequested split-screen framing on another),
both caught by direct visual inspection before acceptance, not assumed clean
from a first pass.
