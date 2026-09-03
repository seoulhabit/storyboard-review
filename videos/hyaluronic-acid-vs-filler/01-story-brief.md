# Story brief — hyaluronic-acid-vs-filler

**Source:** operator-supplied script, "HYALURONIC ACID HAS THREE DIFFERENT IDENTITIES",
7 scenes, two characters (SoulHabit, Jay), stated runtime ~3 minutes.

| Field | Value | Rule |
|---|---|---|
| Format | **long, 16:9, 1920×1080** | `[S1/S-1]` branch 1, operator-directed — see §Format override |
| Target length | **~180 s** | `[S1/S-2]`, `below-clamp` — see §Length |
| Presenter | **moving diagram** | `[S1/S-3]` mechanism-heavy (three parallel mechanisms) |
| Voice | **two-hander** — Kimberly / Grady | `[S1/S-4]` + `[NOT IN SKILL]`, see §Cast |
| fps | 30 | `[S6/A-4]` — no fast counters |
| Route angle | `concept` | `[S1/S-7]`: six-section spine with a named wrong belief |
| `VO_MODE` | `use it verbatim`→`restructure per scene` | script supplied, but reworded under `[K-2]`; see §Rewordings |

---

## The six-section spine

| § | Content | Script scenes | Time |
|---|---|---|---|
| **Hook** | Three things carry one name. Only one of them can add volume. | 1 (lineup) | 0–14 s |
| **Misconception** | "A hyaluronic-acid serum is basically filler in a bottle." | 1 (title) | 14–32 s |
| **Mechanism** | Where it came from; what your body's version does; what the serum's version does — molecular size as the governing variable. | 2, 3, 4 | 32–99 s |
| **Proof** | It binds water, it does not make water. Filler HA is chemically different: cross-linked into a gel. | 5, 6a | 99–135 s |
| **Application** | Pair a humectant with something that seals. Never inject a topical. Fillers are a medical procedure. | 6b | 135–162 s |
| **Recap + end scene** | Three badges: resident / moisturiser / construction project. End card. | 7 | 162–180 s |

`[S1/S-5]` — all six sections carry distinct content, grounded in the supplied
script. **Nothing is `[UNGROUNDED]`; nothing generated from scratch.** Bridging
sentences added for timing are marked `[GEN]` in `04-assets/script.md`.

---

## Format override — `[S1/S-1]`

Branch 1 fired: the operator directed 16:9 long-form. **This overrode branch 2**,
which would have selected `short`. The share it overrode, stated rather than
implied:

- views, 90 d: shorts **4730** vs videoOnDemand **26** → 99.45 % short
- uploads, 90 d: **46 short / 2 long** (baseline `corpus`) → 95.8 % short
- repo corpus: **30 of 31** built projects are 9:16

Consequences carried, per the first-of-kind clause:

1. **Every `curve.*` and `retention.*` comparison in this run is `[UNDERPOWERED]`.**
   `baseline-notes.md` independently reaches the same conclusion from the other
   direction: "This channel has no public long-form, so the curve is necessarily
   built from Shorts. Any rule reading `curve.*` as a long-form signal is reading
   Shorts data." The 48 h/7 d readout must not rank this video against that curve.
2. **Format-specific gates are re-pointed, not inherited.** Safe areas are
   54/108/96/96, not the Shorts 192/384/162/72. `check-safe-area.py` and
   `check-static-hold.py` take `--landscape`; `check-cadence.py` takes `--longform`.
   A portrait-calibrated gate on a landscape render is confirmed to **report a
   silent clean pass** — the bottom-zone slice runs off the end of a 1080-tall
   array and numpy returns an empty view.
3. `[S3/P-3]` runs the **long-form** branch: a thumbnail is generated and scored.
   The Shorts frame-0 branch does not carry across.
4. **Not fully first-of-kind** — `videos/ectoin-survival-molecule` is 1920×1080 /
   340.2 s / 29 scenes of working repo prior art, with its own landscape token set,
   safe-area reasoning and postrender gate chain. The clause's "prove the format on
   a short vertical slice first" is therefore **skipped, logged**: the slice already
   exists and shipped.

## Length — `[S1/S-2]`

Target **180 s**, from the operator's stated runtime. The long clamp is 4:00–12:00,
so this is **`below-clamp`** and the divergence is logged rather than obeyed: the
clamp governs a target *derived from baseline*, and there is no long-form baseline
to derive one from (`avg_view_pct_long` is unattributable, `baseline-partial`).
An operator-supplied runtime is a stated input, not a measurement that would defeat
its own rule.

`[S1/S-7]` route length field: 180 s against the route's 30–90 s "sweet spot" —
advice, not a gate; `[S1/S-2]` wins and the divergence is recorded here.

## Cast — `[S1/S-4]` and the two-hander gap

| Character | Voice | id | Type |
|---|---|---|---|
| SoulHabit | Kimberly | `674b71b8-1d2e-4087-8567-d1f53c0b9f3c` | element |
| Jay | Grady | `e2a2d2e6-9ed2-59cd-82af-feaa27f8a678` | preset, male |

Kimberly is the established channel voice (`providers.yaml` §tts `current-vo`;
already carried `pdrn-cellular-science` and `hyaluronic-acid-serum`) and is **not
rotated** — she remains the narrator and speaks SoulHabit. Grady is selected by
`[S1/S-4]`'s own fallback ordering: no returned voice name contains
"neutral"/"narrator", so it takes **the first returned** voice of the contrasting
gender. `[NOT IN SKILL]`: the policy has no rule for a multi-character script —
`[S1/S-3]` says one presenter, `[S1/S-4]` says one voice never rotated, and
`[S4/V-2]`'s two-generation cap assumes a single VO. Proposal filed in
`videos/_channel/policy-change-proposals.md`.

---

## §Sourcing — the `[K-1]` claim table

Every identifier below was **fetched and read during this run**, not recalled.
Chips render as `Journal · Year` or `FDA · <page>`; DOIs and PMIDs live in the
description only. **No PMID and no `ING-*` reaches a frame** — following
`ectoin-survival-molecule`'s convention (`.cite` CSS: "Journal · Year ONLY"),
not `peeling-not-progress`'s older raw-PMID one.

| # | Claim (as it will render) | Class | On-screen chip | Backing — verified |
|---|---|---|---|---|
| C1 | Three things share the name "hyaluronic acid": the kind in your body, the kind in a serum, the kind in a filler | nominal | none | Identity. Asserts no effect. |
| C2 | In 1934 it was isolated from the vitreous of a cow's eye and named there | **sourced** | `J Biol Chem · 1934` | Meyer K & Palmer JW, *J Biol Chem* **107**:629–634, `10.1016/S0021-9258(18)75338-6`. Named from *hyalos* (glassy) + uronic acid. Clears `[K-2a]`'s unsourced-number bar — the year is a citation, not a measurement. |
| C3 | Your body makes it; most of it sits in your skin, where it holds water | **sourced** | `Dermatoendocrinol · 2012` | Papakonstantinou et al., PMID 23467280, `10.4161/derm.21923` — "The key molecule involved in skin moisture is hyaluronic acid (HA) that has unique capacity in retaining water." |
| C4 | It also lubricates joints and is found in the eye | **sourced** | `Front Vet Sci · 2019` | Gupta et al., PMID 31294035, `10.3389/fvets.2019.00192` — "naturally found in many tissues and fluids, but more abundantly in articular cartilage and synovial fluid… partially responsible for lubrication and viscoelasticity". Split from C3 deliberately so each chip sits on the claim it actually supports. |
| C5 | In a topical, molecular size governs how far it gets: larger stays at the surface, smaller can reach the upper layers | **sourced** | `Skin Res Technol · 2015` | Essendoubi et al., PMID 25877232, `10.1111/srt.12228` — LMW (20–300 kDa) "passes through the stratum corneum in contrast of the impermeability of high molecular weight HA (1000–1400 kDa)." Corroborated, not chipped: PMID 37004799 (5–8 kDa through SC; HMW "trapped on the SC surface"). |
| C6 | Hydrated surface cells can temporarily make fine lines **appear** softer | **sourced** | `Dermatoendocrinol · 2012` | Same as C3 — a moisture/appearance claim, already correctly hedged in the supplied script. `[K-3]`: "appear" and "temporarily" carry into the on-screen type, not just the VO. |
| C7 | It binds and holds water — it does not create water. A formula also needs to stop that water leaving. | **sourced** | `ChemRxiv · 2023` | Reused: `ING-hyaluronic-acid-S001`, `videos/hyaluronic-acid-serum/BRIEF.md` — *Fallacy of Hyaluronic Acid Binding a Thousand Times Its Weight In Water*, `10.26434/chemrxiv-2023-r728q`. Real capacity ~10–100× by MW. `[S6/A-1]` reuse, not re-research. |
| C8 | Filler HA is **cross-linked** into a gel that holds its shape | **sourced** | `J Cosmet Dermatol · 2024` | Hong et al., PMID 39466959, `10.1111/jocd.16652` — "Uncrosslinked HA degrades rapidly due to endogenous hyaluronidase, while crosslinked HA undergoes slower degradation"; BDDE cross-linking. Corroborated: PMID 39107664. |
| C9 | Placed under the skin, that gel can physically add volume | **sourced** | `J Cosmet Dermatol · 2024` | Same — histology shows collagen capsule formation and autologous tissue replacement post-injection. |
| C10 | **Do not inject yourself.** | **sourced**, REWORDED | `FDA · Dermal Fillers` | FDA, *Dermal Fillers (Soft Tissue Fillers)*, rev. 2023-07-06, verbatim: **"Do not inject yourself with dermal fillers."** Also "Do not purchase dermal filler products online" and "Needle-free devices are not approved by the FDA for the injection of dermal fillers." |
| C11 | Fillers are a medical procedure with real risks, for trained providers only | **sourced** | `FDA · Dermal Fillers` | Same page, verbatim: "Select a health care provider who is trained to perform the dermal filler injection procedure"; "seek a licensed health care provider with experience in the fields of dermatology or plastic surgery"; risks "include necrosis (death of tissue), vision abnormalities including blindness, and stroke." |
| C12 | Jay's analogies (cousins at a wedding, houseplant, lifeguard/empty pool, cow royalties), the title, the end card | editorial | none | Assert no outcome. Subject to the absolute-language ban — no *guaranteed / instantly / proven / always / useless*. |

**Counts.** nominal 1 · **sourced 10** · unsourced **0** · illustration 0 · editorial 1.

`[K-2b]` **ratio limb: does NOT fire.** Across Mechanism (C2–C6) and Proof
(C7–C9), sourced : unsourced is **8 : 0**. The video ships as a normal explainer,
not disclosure-forward. No `unsourced-flag` component is needed and none is
emitted — which is the outcome that rule wants, not an exemption from it.

`[K-2a]` **hard-prohibited set: clear.** No unsourced safety claim (C10/C11 are
FDA-verbatim), no unsourced quantity (the only number on screen is 1934, cited),
no *treats/prevents/cures*, no comparative superiority, no absolute language.
Checked again on pixels at `[K-4]`.

### Rewordings applied before the script is written

Same discipline `videos/peeling-not-progress/frame.md` applied — the point of a
sourcing pass is that it changes the copy.

1. **"Never inject a topical serum" → "Do not inject yourself. Ever."**
   FDA's actual sentence is *"Do not inject yourself with dermal fillers."* The
   original wording narrows the warning to serums and, read literally, leaves
   self-injecting an actual filler unaddressed — the more dangerous act, and the
   one the regulator names. The reworded line tracks the source and is strictly
   safer. Retained as the large-type callout the script asks for.
2. **"skin, joints and eyes" split into two claims (C3, C4)** with separate chips,
   because the skin source does not cover joints and the joints source is not a
   dermatology paper. One chip covering both would have been a chip standing on
   ground it does not have.
3. **"Neither behaves like an injectable filler"** kept — it is a distinction, not
   a comparative-superiority claim, and C8/C9 source the difference.
4. **"plumping"** — the script already says "can temporarily make fine lines
   *appear* softer". No change to the VO; `[K-3]` pushes the same hedge into the
   on-screen type, which is the half most of this channel's audience receives.

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
