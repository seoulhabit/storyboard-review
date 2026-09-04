---
format: 1080x1920
duration: 84.88s
arc: story-explainer, evidence-led, reordered for Shorts payoff placement
audience: "skincare-curious social viewers who've seen snail mucin trend but don't know the science"
mode: autonomous
music: "quiet forest-editorial bed under narration, no swell — this video's register is measured, not dramatic"
---

**All timestamps below are measured, not estimated** — cut from the actual mastered VO duration per
chapter (`assets/voice/0N.wav`), the master clock. Total: **84.88s** (7 VO lines: 7.12 / 6.24 /
17.92 / 16.64 / 12.40 / 12.16 / 12.40).

Six sub-composition files carry seven chapters; chapters 3+4 share one file
(`03-mixture.html`) because they share one actor — the composition column — split by actor
continuity, not narration sentence (`[S6/A-9]`).

Every boundary is a hard CUT (Short). No plain crossfade, no push-slide (see v1's decision ledger
for why: a push-slide's worst safe-area intrusion and a crossfade's ~50%-opacity midpoint mud are
both measured defects on that project).

Content box for all scenes: **x 72–918 (846px), y 192–1280 (1088px)** — the caption band occupies
y 1300–1520, tighter than the platform's raw bottom-20% rail, and is the real floor.

---

## Frame 1 — `01-open.html` · 0.00–7.12s · verb: **reveal**

VO: "A 1999 study on radiation-damaged skin sparked today's skincare craze. TikTok skipped the study part."

| t | Development | Type |
|---|---|---|
| 0.00–1.60 | Frame 0 already carries the claim (v1's defect: bare photo, no claim in frame 0). Archival lab plate (`public/01a-archival-lab.png`, reused, grayscale-graded), hero clause slams in over it: "A 1999 STUDY" | photoreal + drawn type |
| 1.60–2.80 | In-scene hard cut to macro secretion plate (`public/01b-macro-slime-spatula.png`, reused). Punch-in on the spatula, via the `cut-wrap > punch-wrap > kb-wrap` nesting from v1's `01-hook.html` (keeps type off the moving/zoomed wrapper) | photoreal |
| 2.80–7.12 | Mono chip "TIKTOK SKIPPED THE STUDY PART" spring-pops in (overshoot spend 1 of 2), plate holds a slow drift under it | drawn chip over photoreal |

Citation: none needed — this chapter states no claim requiring a chip; "1999" is restated visually,
not asserted as a number beyond what SRC-1 supports (a real, dated trial).

## Frame 2 — `02-name.html` · 7.12–13.36s · verb: **name**

VO: "One specific extract has been studied in small clinical trials. Most snail-mucin products haven't."

| t | Development | Type |
|---|---|---|
| 7.12–8.60 | Hard cut, ground flips archival→paper. "SNAIL SECRETION FILTRATE" — the INCI name — lands at hero scale | drawn |
| 8.60–10.60 | Two outlines: "ONE STUDIED EXTRACT" (left) vs "MOST OTHERS" (right), sourced/unsourced framing (`CLAIM-LEDGER.md` C2/C3) | drawn |
| 10.60–13.36 | Left fills solid (citation chip `J Drugs Dermatol · 2013` + `J Clin Aesthet Dermatol · 2020`); right stays outline-only, no chip | drawn |

Citation chips: `J Drugs Dermatol · 2013`, `J Clin Aesthet Dermatol · 2020` (C2). Never an `ING-*` id.

## Frame 3+4 — `03-mixture.html` · 13.36–47.92s (two phases, one actor: the composition column)

### Phase `#ph-composition` (ch3) · 13.36–31.28s (17.92s) · verb: **separate**

VO: "Snail secretion is over 97 percent water. The rest — proteins, glycolic acid, allantoin — varies by product. A 2024 lab comparison found the exact mix changes with how it's collected. Same species. Different product, every time."

Every beat is cut to the **measured word clock** in `assets/voice/03.transcript.json`, not to
round numbers — the graphic and its word resolve together instead of the graphic chasing the VO.

| t (abs) | Development | Type |
|---|---|---|
| 13.46–14.56 | Kicker "COMPOSITION" sets the frame; the empty 100% measure draws left→right | drawn |
| 14.66–16.36 | On "97%" (15.30) the numeral lands at 260px beside a mono "WATER"; the green fill then sweeps the measure under it. This lockup is the scene's dominant read | drawn |
| 16.46–17.21 | On "The rest," (16.88) the remaining **3% arrives as the one contrasting bronze segment** on that same measure, and a bronze thread runs tag → segment → the list below | drawn |
| 17.48–19.81 | The remainder opens into its three named parts, one per spoken name: proteins (17.55), glycolic acid (18.27), allantoin (19.38). Each row settles 14px, no overshoot | drawn |
| 20.46–21.21 | "varies by product." — same three names, different amounts. **Only the measure fills move**; rows never travel, so nothing can collide | drawn |
| 21.96–24.02 | "A 2024 lab comparison found" — the observed range appears behind each fill, and the `Sci Rep · 2024` chip lands **on its own claim** rather than trailing the scene | drawn |
| 24.96–28.31 | "the exact mix changes with how it's collected" — two further draws inside that range, then the range itself opens wider | drawn |
| 28.46–31.28 | "VARIABLE" lands at hero scale beside the citation; the fills settle to a final spread | drawn |

Citation chip: `Sci Rep · 2024` (C4, C6).

**Why this is not the v1 column vessel.** The original built this phase around a 300×640 vessel that
filled to a water line, with the three ingredient rows sliding **laterally** underneath it. Measured
on extracted frames, that arrangement had three defects: "97% WATER" was a 30px label inside a pale
box rather than the dominant read; the rows crossed the vessel outline and, by 29.5s, drifted past
the x=72 content edge; and the lateral re-deal read as cartoonish rather than editorial. The
replacement states the whole as one measure, gives the 3% its own contrasting segment on that
measure, and carries variance in bar **length inside a fixed track** — which cannot collide with
anything by construction. A 260px numeral's ink box is 1.2em (312px) tall and overhangs its 0.82
line box by ~49px top and bottom, so the numeral and its label are placed side by side; a stacked
lockup at this size cannot clear both the kicker and the measure inside the y 192–1280 content box,
which `hyperframes check` reported as a real `content_overlap`, not a transient one.

### Phase `#ph-evidence` (ch4) · 31.28–47.92s (16.64s) · verb: **compare**

VO: "Two small trials tested that one specific patented extract — not snail mucin generally. In the smaller trial, twenty-five women, fine lines improved. In the larger trial, fifty women, the placebo cream worked almost as well as the real one."

| t (abs) | Development | Type |
|---|---|---|
| 31.28–33.0 | Hard cut (in-scene phase swap). The ch3 column **reframes** into a left tile — never redrawn | drawn |
| 33.0–36.0 | Two more tiles arrive: "Trial 1 · n=25" and "Trial 2 · n=50" | drawn |
| 36.0–40.5 | Evidence-card rows inside the active tile: solid dot = measured outcome present (fine lines, split-face); hollow ring = absent (no large-N, no long follow-up, one arm shared a maker) | drawn |
| 40.5–44.0 | The honest retraction: "placebo worked almost as well" — a bar visually narrows the gap between the two trial outcomes | drawn |
| 44.0–47.92 | Plain-language restatement + citation pills | drawn |

Citation chips: `J Drugs Dermatol · 2013`, `J Clin Aesthet Dermatol · 2020` (C7–C9). Small-print note
on the second: co-author affiliated with the product's manufacturer (C10) — on screen, not just in
the description, because a claim this specific needs its caveat visible where the claim is made.

## Frame 5 — `04-method.html` · 47.92–60.32s (12.40s) · verb: **inspect**

VO: "Collection methods vary too. Some brands stimulate snails by hand, others use acid sprays. Companies call it cruelty-free. That claim comes from the companies — not an independent study."

| t (abs) | Development | Type |
|---|---|---|
| 47.92–49.92 | Hard cut to mesh plate (`public/04-snail-mesh.png`, reused) full-bleed; camera punch + 2–3° tilt, type outside the moving wrapper | photoreal |
| 49.92–51.92 | Mono chip "METHODS VARY" over the plate | drawn over photoreal |
| 51.92–54.42 | Plate reframes to a third-width tile; two drawn method tiles slide in beside it: "BY HAND" / "ACID SPRAY" | photoreal + drawn |
| 54.42–56.92 | "CRUELTY-FREE" label appears — deliberately in the **same muted ink as the unsourced-flag pill**, never the accent colour, never citation typography | drawn |
| 56.92–60.32 | Unsourced-flag pill: "Company claim — not independently verified" (C12), ink-toned, concurrent with the label | drawn |

No citation chip on "cruelty-free" — by design, because none exists (`CLAIM-LEDGER.md` explicitly:
the paper *relays*, does not verify, this claim).

## Frame 6 — `05-use.html` · 60.32–72.48s (12.16s) · verb: **demonstrate**

VO: "Follow the product's own directions. Some people prefer damp skin first, for texture — a preference, not a proven rule. No study backs the "it pulls your hydration out" warning."

| t (abs) | Development | Type |
|---|---|---|
| 60.32–62.32 | Hard cut. Directions card (drawn): "FOLLOW THE PRODUCT'S DIRECTIONS" | drawn |
| 62.32–64.32 | Cut to photoreal application close-up (`public/02-routine-montage.png` reused for the wide cutaway; new macro-cheek plate for the close application shot — see `ASSET-SPECS.md` S4) | photoreal |
| 64.32–67.32 | Split-compare divider draws down centre; left = damp application, right = neutral base. Labels fade up independently: "PREFERENCE" (left) / "NOT A LAW" (right) | photoreal + drawn |
| 67.32–70.32 | Flood — one accent, multiply blend, on the **left** (interrogated) field only; right stays plain | photoreal + drawn |
| 70.32–72.48 | Unsourced-flag pill: "No study confirms this" — lands directly beside the field it corrects | drawn |

This is the direct correction of v1's most consequential unsourced claim
(`CLAIM-LEDGER.md` — the humectant-harm mechanism, cut and actively corrected, not merely dropped).

## Frame 7 — `06-verdict.html` · 72.48–84.88s (12.40s) · verb: **decide**

VO: "So: an interesting ingredient, with real evidence behind one specific version. Not medicine, not magic. Would you try an animal-derived ingredient? Say so below."

| t (abs) | Development | Type |
|---|---|---|
| 72.48–74.48 | Hard cut to paper ground. Verdict lockup at hero scale | drawn |
| 74.48–76.48 | Two rows: what the evidence supports / what it doesn't | drawn |
| 76.48–78.48 | Ch1's macro plate returns at the **opposite framing** (wide where ch1 was tight) — actor-continuity payoff, not a repeat | photoreal |
| 78.48–84.88 | CTA lands (overshoot spend 2 of 2); ≤1.6s of quiet before the end, inside the cadence ceiling | drawn |

---

## Cadence and continuity notes

- **Cadence ceiling is 1.6s**, not the 2.5–3s window this storyboard's own beats might suggest at a
  glance — `catalog/tooling/check-cadence.py`'s `QUIET_CEILING_S = 1.6` for Shorts is the real gate.
  Every beat above bridges to the next with a sustained tween, not a static landing-then-wait.
- **Actor map:** A-PLATE (ch1, ch7 callback — not consecutive, separate files, same plate at
  different framing) · A-MIX (ch3+ch4 — consecutive, one merged file) · A-RIG (ch5) · A-HAND (ch6)
  · A-VERDICT (ch7). No actor is redrawn across a boundary where it persists.
- **Camera-move safe-area trap:** any `ytCameraMove`-style zoom on a photoreal plate must keep type
  on a sibling wrapper that does *not* scale with the punch — a scaled stage maps its own padded
  edge outward by the same factor (confirmed defect class in this catalog, `molecule-states`
  README).
