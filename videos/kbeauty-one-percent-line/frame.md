# Frame — kbeauty-one-percent-line

## Canvas

1080×1920, 30fps, 9:16 (Shorts). Safe area: `--safe-top 120 / --safe-bottom 360 /
--safe-left 60 / --safe-right 162` (source tokens.css).

## Palette

Base five only: `--paper #F7F5F0`, `--ink #131516`, `--aqua #59B8AE`,
`--leaf #6F8F72`, `--coral #C97A5C`, plus `--highlighter #E0A32B` for a
secondary data-mark and `--ink-3 #9C978D` for de-emphasized/"below the line"
text. **One aqua-family highlight per frame** (hard law). **Coral is the
single voltage moment for the whole video** — the 1% red-line slash in Frame
04 (`04-one-percent-line`) is that moment; every other "alert" beat in the
script (hook buzzer cross-out, teardown slash) uses ink-weight strikethrough
or highlighter instead of a second coral hit, per catalog/README.md's rule
that coral never doubles with aqua in-frame and never repeats as a second
voltage moment.

Frames alternate paper (`--paper`) and ink (`--ink`) backgrounds scene to
scene for hyperframe contrast pops — the paper-first system explicitly
sanctions dark frames; this video leans on that instead of glow (banned) to
get the aggressive tech feel the user's script asked for.

| Frame | Background |
|---|---|
| 01 hook | paper |
| 02 promise | ink |
| 03 extract-loophole | split paper/ink (two columns) |
| 04 one-percent-line | ink |
| 05 the-trick | ink |
| 06 teardown | paper |
| 07 hanbang-rapidfire | ink |
| 08 cta-endcard | paper |

## Type

`--font-display` EB Garamond (hero/question lines), `--font-body` Inter
700/800 (kinetic block words, the closest system-legal analog to the user's
requested Montserrat/Impact blockiness), `--font-mono` JetBrains Mono (INCI
names, percentages, chips, citations-style labels), `--font-kr` Noto Sans KR
500 (습 SeoulHabit lockup only). Nothing under `--t-floor: 20px`. Track
tight on mono (`--tr-mono 0.04em`), centered kinetic blocks per the user's
brief.

## Motion

System eases only: `--e-out` for entrances, `--e-in` for exits, `--e-inout`
for holds/attention loops. Durations `--d-snap 180ms` for hit/impact beats
(flashcards, slashes, chip pops), `--d-fast 400ms` / `--d-base 500ms` for
word reveals, `--stagger-line 80ms` / `--stagger-node 120ms` for lists.
**No bounce/elastic/back eases, no infinite keyframes** — any idle motion
(chip float, pulse) is a finite bounded yoyo (repeat: 2-3) that resolves by
the frame's last authored beat, matching `01-hook.html`'s chip-float
precedent in seoulhabit-launch. Motion blur is not a HyperFrames primitive;
the "aggressive crash zoom" feel is achieved with fast scale+opacity snaps
on `--d-snap` timing instead, never CSS blur filters (which read as
low-fidelity, not cinematic).

## Elevation

`--elev-2` / `--elev-3` shadows on popped cards/chips only. **Glow banned**
outright — no `box-shadow: 0 0 …`, no `drop-shadow(0 0 …)` — matching the
banned pattern the user's own script literally asked for ("neon glow");
translated to elevation + scale instead.

## Faceless

No talking-head footage, no stock photo people. Typographic/vector treatment
still carries every INCI/data frame, consistent with the JS-generated-card
precedent in `skincare-ingredient-glossary`. One exception: Frame 04b (see
B-roll) uses three flat-lay PNGs from `catalog/ingredient-photography/` as a
deliberate sensory counterweight to the text-heavy frames around it — not a
reversal of the house style, a controlled exception to it.

## B-roll

None captured (no product/site to film, per the faceless-explainer contract).
Frame 04b ("BEYOND THE LABEL") is the one photographic beat in the video: a
2.5s rapid-fire interlude between Frame 4 (the 1%-line breakdown) and Frame
5, showing three `catalog/ingredient-photography/` stills — snail mucin,
ginseng, mugwort — each with a quick snap-in, a brief Ken-Burns push+drift
while held, and a whip-out into the next (the same three ingredients Frame 7
later Hanbang-translates, in the same order, so the beat also primes that
reveal). Cut down from an initial 5.8s pass after review flagged it as
dragging against the rest of the video's pacing.
Paper background, not ink, so it reads as a breather rather than another
data frame — the two adjacent ink frames (04, 05) make the paper pop land on
both sides. No VO: this is the one wordless beat in an otherwise wall-to-wall
narrated video, letting BGM alone carry it. Source images are 2048x2048
Higgsfield stills shot on cream seamless paper (see the catalog's own
README); downsampled to 1400px and copied into `assets/images/` rather than
referenced from the shared catalog path, matching how fonts/audio are always
project-local.

## Brand anchor

습 SeoulHabit text lockup (Noto Sans KR 500) appears once, in Frame 08's
endcard — not the Fold & Spark mark (explicitly not approved for
SeoulHabit).

## Audio mix

Shared `<hf-audio-group id="voiceover">` bus carrying the seoulhabit-launch
voice-warm-style chain verbatim: highpass 90Hz → peaking 150Hz +1.5dB →
compressor -22dB/3:1 → peaking 3kHz +1.5dB → peaking 6.5kHz -4dB Q3.5
(de-ess fallback) → limiter -10dB. 80ms automation fade-in/out on every VO
clip. BGM (`el-bgm`) carries `data-fx-carve {sources:["voiceover"],
strength:0.25}` to ledge under narration. One SFX lane per hit
(`data-track-index` 20+), `data-volume ≈0.35`.

## Goal-alignment additions

The user's script is fast/punchy/high-energy — those qualities are
preserved through beat density (new kinetic element every ~2s inside each
frame) and short VO sentences, not through off-system colors or fonts. The
"cha-ching," buzzer, keyboard-typing, glass-shatter, alert-ping,
ding-ding-ding, whoosh-thud, marker-squeak, camera-shutter, and
camera-flash SFX cues from the script are all kept — they carry the energy
without touching the visual system.

## Design-system reconciliation

Same reconciliation basis as `seoulhabit-launch/frame.md`: `assets/tokens/tokens.css`
copied verbatim from that project (itself reconciled 2026-08-28 against the
live claude.ai design project via DesignSync). No new tokens invented here.

## Content corrections (fact-check against the user's script)

The user's script draft contains two claims that don't hold up against the
real Beauty of Joseon Glow Serum: Propolis+Niacinamide INCI list (verified
via incidecoder.com / incibeauty.com — full list: Propolis Extract [~60%],
Dipropylene Glycol, Glycerin, Butylene Glycol, Water, Niacinamide [2%],
1,2-Hexanediol, Melia Azadirachta Flower/Leaf Extract, Sodium Hyaluronate,
Curcuma Longa Root Extract, Ocimum Sanctum Leaf Extract, Theobroma Cacao
Seed Extract, Melaleuca Alternifolia Extract, Centella Asiatica Extract,
Corallina Officinalis Extract, Lotus Corniculatus Seed Extract, Calophyllum
Inophyllum Seed Oil, Betaine Salicylate [0.5%], Sodium Polyacryloyldimethyl
Taurate, Tham, Polyglyceryl-10 Laurate, Caprylyl Glycol, Ethylhexylglycerin,
Dextrin, Pentylene Glycol, Octanediol, Tocopherol, Xanthan Gum, Carbomer):

1. **"Fancy seed oils below it"** — false for this product. Calophyllum
   Inophyllum Seed Oil sits *above* Ethylhexylglycerin in the real list, not
   below. What's actually below the Ethylhexylglycerin line is Dextrin,
   Pentylene Glycol, Octanediol, Tocopherol, Xanthan Gum, Carbomer —
   texture/preservation aids, not botanical oils. **Fix:** teardown card
   (Frame 06) shows the real trailing ingredients; VO line 6 changed to
   "Everything below it — dextrin, xanthan gum, tocopherol — is basically
   fairy dust," dropping "seed oils."
2. **"Globally capped around 1%" for both preservatives named** —
   Phenoxyethanol does carry a hard EU/ASEAN regulatory cap (1% in leave-on
   and rinse-off products). Ethylhexylglycerin does not carry an equivalent
   formal cap — it's a preservative-booster/deodorant conventionally used at
   well under 1%, but the claim "globally capped" overstates it as
   regulation. **Fix:** Frame 05 VO softened to "Phenoxyethanol has an
   actual legal cap around 1%. Ethylhexylglycerin sits in that same
   fractions-of-a-percent range" — keeps the visual mechanic (both are
   reliable "you've crossed the 1% line" landmarks) without asserting a
   false regulatory fact for the second one.

No `ING-*` source ids exist for this topic (general label-literacy content,
not a single-ingredient evidence record) — endcard carries the sanctioned
disclaimer from `skincare-ingredient-glossary`: "General label-reading
guide — not sourced claims, not medical advice." The hook's "80%" figure is
kept as the script's own rhetorical hypothetical ("What if...?"), not
attributed to any named brand.
