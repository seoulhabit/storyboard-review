# Director's Notes — HA video v4 (retention cut)

Producer pass over the v3 clinical draft. Aesthetic untouched (paper + dark
panels + neon, boxed citations); pacing, script register, and CTA rebuilt for
short-form retention. Runtime 64.5s → **51.7s**. All five flagged issues
fixed and implemented in the composition (not just proposed).

## 1 · The hook (was: 7s of orb before the name)

- **Cut the orb prelude entirely.** The glowing polymer chain is lit at
  frame zero — the scroll-stop frame is already the subject.
- **"HYALURONIC ACID" is the headline at t=0** (snap-settle, no scale-in —
  a scale entrance visually jammed the two words on the thumbnail frame).
- Benefit subline "YOUR SKIN'S BIGGEST DRINK OF WATER" lands at **0.35s**;
  spoken name lands ~0.9s, spoken benefit by ~2.2s. Name + benefit on
  screen inside 2 seconds. ✔
- The five water dots dock on the chain exactly on the spoken phrase
  "drink of water" (1.3–1.9s) — first state change inside the 1.5–3s
  cadence window.
- Coral underline now fires at 3.95s on "…is a myth." Hook scene total:
  **5.4s** (was 7.3s).

## 2 · Identity screen (was: fields loading out of order)

- Reveal order is now **strictly top-to-bottom**: INCI (1.5s) → MOLECULAR
  WEIGHT (2.4s) → SOURCE (3.2s). Nothing ever pops in above an
  already-visible row. (Root cause: v3 revealed rows on VO cues while the
  DOM stacked them in dossier order; v4 makes screen order == reveal
  order.)
- Cadence tightened: card 0.1s → name 0.85s → one field every ~0.9s →
  claim 4.0s → citation 5.25s. Scene total **6.7s** (was 11.5s).

## 3 · Information density (was: kDa ranges + "fibroblasts" in VO)

- VO now carries zero dalton figures and zero cell-biology nouns. The
  numbers live **on screen only**, demoted to fine print:
  - MW row reads "Light → heavy chains (10 kDa – 2 MDa)" — plain words
    first, precise range in parens for the science-literate pause-readers.
  - Claim row: "how much it holds depends on chain size."
  - The FIBROBLAST label stays inside the diagram (screen-only authority);
    VO says "your skin makes its own."
- Authority is preserved by the *frame*, not the vocabulary: boxed
  `CITATION — ⌞ ING-hyaluronic-acid-S00N ⌟` pills stay on every sourced
  claim, measured figures stay on the dark data panel.

## 4 · CTA (was: tiny unspoken gray text)

- **Spoken, verbatim, in the last 4 seconds:** "…tell me in the comments —
  and hit follow for the next ingredient."
- **Burned in neon** (the video's highest-salience treatment), inside the
  dark panel where the eye already is: "TELL ME BELOW ↓" (5.8s) then
  "+ FOLLOW — INGREDIENT SERIES" (7.15s). The old 30px gray line is
  deleted as redundant; the disclaimer stays small beneath the citation.
- "Ingredient series" seeds the follow with a reason (next episode), and
  the closing beat hands back cleanly for a Shorts loop.

## 5 · Voiceover energy (was: monotone academic read)

- Same Kimberly voice (brand continuity), rewritten register: direct
  address ("here's why you care", "here's the catch"), short contrasting
  clauses on em-dashes, one idea per breath. The em-dash-over-period rule
  is the voice's own fitted pacing model (each period costs ~1.6s of dead
  pause — the monotone feel was largely punctuation-driven).
- Net: 47.1s of narration vs 57.7s, with more addressed-to-you turns.

## Pacing outline (as built)

| # | Scene | In | Dur | State changes (target: one every 1.5–3s) |
|---|---|---|---|---|
| 1 | Hook | cut | 5.37s | name t0 · benefit 0.35 · dots 1.3–1.9 · coral strike 3.95 |
| 2 | Identity card | cut | 6.74s | card 0.1 · name 0.85 · INCI 1.5 · MW 2.4 · SOURCE 3.2 · claim 4.0 · pill 5.25 |
| 3 | Myth vs measured | xfade | 12.71s | row-1k 1.5 · row-6k 4.7 · red strikes 5.95/6.2 · neon 10–100× 7.0 · axis label 9.45 · pill 10.3 |
| 4 | Why you care | xfade | 9.14s | rods 1.05 · coils 1.55–3.1 · water dots 3.05 ("plump") · decline row 4.45 · sparkline 5.6–7.1 · pill 7.9 |
| 5 | The catch | xfade | 7.01s | surface 0.45 · HMW 1.05 · aqua in-arrow 2.3 · air dims 3.7 · coral out-arrow 3.95 · claim 4.9 · pill 5.6 |
| 6 | Protocol + CTA | cut | 10.72s | rows 1.2/1.9/2.55 · dim+divider 4.45 · neon CTA 5.8 + 7.15 · pill 8.55 · disclaimer 9.05 · still hold 9.5→end |

Graphics speed-ups vs v3: F5's diagram build compressed ~2.4× (coil draw
1.55s→0.9s, whole schematic done by 2.7s instead of 5.5s); F4's lattice
build ~1.5× faster; F3 unchanged in feel but strikes land as a pair
(0.25s apart) right on the "measured" turn.

## Claim safety (unchanged discipline)

Every spoken assertion still maps to S001/S002/S003; "biggest drink of
water" is hook framing for the humectant identity (carried by the S001-
sourced claim row on screen); 6,000× remains struck marketing copy;
mechanism schematics keep the [Authored, illustrative — not a claim] tag.

---

# v5 — external QA pass (safe areas, audio master, hook trim) · 2026-08-29

Response to the four-issue QA report on `hyaluronicacidserumv4.mp4`. All fixes
applied at the composition/stem level and re-rendered — not patched in an NLE.

## 1 · BLOCKER — lower text inside the Shorts bottom-overlay zone

Verified by frame extraction: citation pills sat at y≈1432–1519 and the
disclaimer at y≈1486–1512 — under the Shorts title/channel/audio UI, and
outside this project's own frame.md content window (y ∈ [288, 1440]).
Fixed by reclaiming dead panel space instead of crowding the top:

- F3: panel 416→380, height 1000→900 (had ~150px empty bottom), pill 1432→1296.
- F4: claim row 1186→1170, pill 1338→1310.
- F5: claim 1245→1210, pill row 1382→1340.
- F6: panel 300→288, height 980→920, pill 1316→1224, disclaimer 1486→1356.

Every readable element now bottoms out ≤ ~1430 (bottom-20% line is 1536).
Disclaimer KEPT on screen (house rule, per BRIEF) — now actually readable.
Also add it to the description/pinned comment at publish time.

## 2 · MAJOR — "hiss / high noise floor"

Diagnosed before treating: stems measure -57 to -70 dB RMS in pauses and the
BGM bed has no content above 6 kHz — there is no literal hiss source. The real
defect was the master level: **-21.4 LUFS integrated**, 7.4 LU under the -14
target, so playback gain-up surfaces breath/floor as perceived hiss.
Fix: light afftdn (nr=12, nf=-42) on all six VO stems (originals in
`assets/voice/_v4-stems-backup/`), then a two-pass loudnorm master of the
render to **-14.7 LUFS / -1.0 dBTP** (video stream copied, AAC 256k).

## 3 · MINOR — hook pacing

No leading dead air exists in stem 01 (speech starts at t=0), so no head-trim.
Instead: stem 01 runs through atempo=1.08 (pitch-preserving, 4.77s→4.43s),
frame 01 duration 5.37→4.78s, VO-synced cues ÷1.08 (dots 1.20, underline 3.66),
and the tail hold tightened. Identity card now arrives at 4.78s (was 5.37s).
Full downstream ripple −0.59s; total runtime 51.7s → **51.1s**.

## Delivery specs (verified, closes the "could not verify" list)

1080×1920 · 30fps CFR · yuv420p · Rec.709 (bt709 primaries/transfer/matrix) ·
AAC 48 kHz stereo · -14.7 LUFS integrated · -1.0 dBTP · moov faststart.
`npm run check` clean (lint/runtime/layout/motion 0 issues, 33/33 AA contrast).

---

# v6 — second external QA pass (CTA arrow) · 2026-08-29

Three-issue report; two were already resolved by v5 and re-verified on this
render, one new fix applied:

1. **Safe areas** — verified against the stricter "above the 80% vertical
   line" bar (y=1536): every citation pill and the disclaimer bottoms out
   ≤ ~1430. No element is anywhere near the lower 15% (y ≥ 1632). No change.
2. **CTA arrow (fixed)** — "TELL ME BELOW ↓" pointed at the Shorts
   description strip, not the comments button (which sits mid-right). Per the
   report's own recommended option, the arrow is removed and the neon copy now
   reads "TELL ME IN THE COMMENTS / + FOLLOW — INGREDIENT SERIES", matching
   the spoken VO verbatim. Word-stagger reveal timing unchanged.
3. **Hiss** — stems already run through afftdn (v5); this render reuses them
   and is mastered to -14.7 LUFS / -1.0 dBTP. No further treatment.
