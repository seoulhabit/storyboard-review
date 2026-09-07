# Asset inventory — T1

Sweep of already-rendered plates from the centella and PDRN family of
projects (per T1's own scope), plus the extraction pass over the pilot's
own `cGbokt_B_vE` composition (`videos/kbeauty-one-percent-line/`). Full
narrative, decisions, and the voiceover ledger are in
[`wo/FVC-007/T1-ASSET-SWEEP-REPORT.md`](../../wo/FVC-007/T1-ASSET-SWEEP-REPORT.md);
this file is the per-plate table T1 asks for.

Columns follow T1's own spec: path, dimensions, aspect, depicts, face
present, reusable as B-roll under B-1. "Reusable" here means the plate
itself clears B-1's face/brand/claim bars — it does **not** mean a slot
has been assigned; that's T3/T6's job once a real per-beat cast list
exists (see `docs/wo/007/broll-manifest.md`, T5).

## 1. Centella / PDRN family — already-rendered plates

| Path | Dimensions | Aspect | Depicts | Face? | B-1 reusable? |
|---|---|---|---|---|---|
| `videos/centella-cica-vs-snail-mucin/assets/images/f1-palette.png` | 1536×2752 | 9:16 native | Two texture swatches (clear gel + pale-yellow serum) on a frosted glass dish | No | **Yes** — no face, no brand, no text, native portrait |
| `videos/centella-cica-vs-snail-mucin/assets/images/f2-string-start.png` | 1536×2752 | 9:16 native | Hand (cropped above wrist) pinching cream in a white dish | Hand only, no face | **Yes** — B-1 permits a hand cropped short of the face (same treatment as `catalog/product-photography`'s C02) |
| `videos/centella-cica-vs-snail-mucin/assets/images/f3-dropper-start.png` | 1536×2752 | 9:16 native | Dropper releasing a droplet onto the back of a hand/forearm | Hand/forearm only, no face | **Yes** |
| `videos/centella-cica-vs-snail-mucin/assets/images/twist-centella-leaf.png` | 1400×1400 | square | Centella asiatica leaf sprig on white paper | No | Content clears B-1; needs a reframe call for 9:16 (not decided here, see T0b's own aspect-survivability logic) |
| `videos/centella-cica-vs-snail-mucin/assets/images/twist-cream-swirl.png` | 781×1400 | ~9:16-ish (0.558, vs 0.5625 target) | Whipped green-tinted cream swirl, overhead, filling frame | No | **Yes** — no face, no brand, no text; near-9:16, a minor crop away from exact |
| `videos/centella-cica-vs-snail-mucin/assets/images/cta-snail-pour.png` | 1400×1400 | square | Dropper pouring clear liquid into a glass dish, overhead | No | Content clears B-1; square, same reframe caveat as the leaf plate above |
| `videos/centella-cica-vs-snail-mucin/assets/thumbnail/*.png` (3 files) | 1080×1920 | 9:16 native | YouTube thumbnail compositions with baked-in headline text ("SNAIL MUCIN OR CENTELLA?", etc.) | No | **No** — claim/headline text is baked into the pixels; these are thumbnails, not B-roll, regardless of aspect |
| `videos/centella-cica-vs-snail-mucin/assets/broll/02-string-test.mp4` | 1076×1928 | ~9:16 (0.558) | 6.04s clip, string/texture test (same family as f2-string-start.png) | Not checked frame-by-frame | Likely yes, same content family as f2; not individually verified |
| `videos/centella-cica-vs-snail-mucin/assets/broll/03-dropper.mp4` | 1076×1928 | ~9:16 (0.558) | 6.04s clip, dropper (same family as f3-dropper-start.png) | Not checked frame-by-frame | Likely yes, same content family as f3; not individually verified |
| `videos/centella-barrier-recut-15s/assets/plates/02-centella-asiatica.png` | 2048×2048 | square | Duplicate of `catalog/ingredient-photography/02-centella-asiatica.png` | No | Already catalogued — no new source |
| `videos/centella-barrier-recut-15s/assets/plates/03-flaking-skin.png` | 1200×1200 | square | Duplicate of `catalog/skin-macro-photography/03-flaking-skin.png` | No | Already catalogued — no new source |
| `videos/centella-barrier-recut-15s/assets/thumbnail/*.jpg` (3 files) | 1080×1920 | 9:16 native | YouTube thumbnail candidates/finals, headline text baked in | Not checked | **No** — thumbnails, same reasoning as centella-cica-vs-snail-mucin's |
| `videos/centella-tiger-grass/assets/plates/broll-{1..6}.mp4` | 720×1280 | 9:16 native | 5.04s each; real (not generated) nature/plant footage — dew on a leaf confirmed by frame-sampling `broll-1.mp4` | No (sampled) | Content clears B-1, **but provenance/licence is unconfirmed** — see note below |
| `videos/centella-tiger-grass/assets/plates/tiger.mp4` / `tiger-2k.mp4` | 720×1280 / 1440×2560 | 9:16 native | Real tiger footage (a tiger rolling in vegetation) — confirmed by frame sample | No | Content clears B-1 (no face — animal, not human; no brand/claim), **same unconfirmed-licence flag** |
| `videos/centella-tiger-grass/assets/plates/under-{1,2,2b,3,6}.mp4` | 720×1280 | 9:16 native | 8.8–14.4s each; `under-1.mp4` sampled — leaf/dew macro, same family as `broll-*` | No (sampled) | Same content family, same licence flag |

**Provenance flag — `centella-tiger-grass/assets/plates/`:** no README, manifest,
or licence note exists anywhere in that project directory (checked). Real
wildlife and macro-nature footage at this quality is very unlikely to be
first-party generated or shot in-house — it reads as licensed stock. Per
T5's own cost/licence table, this cannot be marked "$0, no licence" the way
the Higgsfield-generated catalog plates can. **Do not reuse without
confirming the licence first** — an unattributed or unlicensed stock clip
in a finished video is exactly the kind of liability B-1's own attribution
concern (for the tier-4 stock path) is written to prevent, even though this
plate didn't arrive through that tier.

## 2. Other centella/PDRN-family projects — audio only, no visual plates

`videos/centella-asiatica/`, `videos/madecassoside-clinical-cut/`,
`videos/madecassoside-flat-matrix/`, `videos/pdrn-cellular-science/`,
`videos/pdrn-left-the-clinic/` all have `assets/` trees containing only
voice/BGM/SFX audio and font files — no images or B-roll video plates were
found in any of them. Confirmed by directory listing, not by name alone.

## 3. Extracted `cGbokt_B_vE` frames (T1 item 2)

Nine frames extracted from the actual rendered MP4
(`videos/kbeauty-one-percent-line/renders/kbeauty-one-percent-line_2026-08-29_21-40-00.mp4`,
115.60s), one per scene, sampled ~1s into each scene (past the cross-fade)
per `STORYBOARD.md`'s own frame-start table:

| Frame | Sampled at | Content | B-1 reusable as raw B-roll? |
|---|---|---|---|
| 01 hook | 1.00s | Bottle photo with "80% GINSENG?" headline baked into the frame | **No** — claim text baked into pixels |
| 02 promise | 9.20s | Pure typography on black, no imagery | **No** |
| 03 extract-loophole | 17.48s | Two-column comparison-split UI ("WESTERN" / "K-BEAUTY"), no photography | **No** |
| 04 one-percent-line | 32.24s | Not separately graded — same design-system family as 03/05/06 | Not graded (typographic pattern already confirmed) |
| 04b ingredient-showcase | 44.84s | Ginseng root photo inside a card, with "GINSENG" caption + progress dots baked into the frame | **No, as this composite frame** — but the underlying plate is already available clean, without the card chrome, as `videos/kbeauty-one-percent-line/assets/images/ingredient-ginseng.png` (already inventoried by T5, square, no face) |
| 05 the-trick | 47.34s | Two ingredient-name pill badges on black, no photography | **No** |
| 06 teardown | 67.38s | "GLOW SERUM" ingredient-list card, typography only | **No** |
| 07 hanbang-rapidfire | 85.90s | "THE HANBANG CHEAT SHEET" title card, typography only | **No** |
| 08 cta-endcard | 106.74s | Recap card with tiny ingredient thumbnail icons + "SCREENSHOT THIS", typography-dominant | **No** |

**Grading result: 0 of 9 sampled frames are usable as raw B-roll.** This is
stronger than T1's own text predicted ("most will be typographic and
unusable") — in this composition, every sampled frame is either pure
typography or a design-system card with claim/label text baked directly
into the pixels, which is disqualifying regardless of what photography sits
underneath it. Where a clean underlying plate exists (04b's ginseng root),
it's already catalogued separately without the card chrome — extracting
the composited frame adds nothing tier-2 didn't already have via tier 1.

Tier 2 (extracted frames) is therefore **exhausted at zero usable plates**,
confirming the WO's own expectation about this tier being thin, and
matching G0-4's own framing that tiers 1–2 together cover very little true
9:16 inventory.

## 4. Voiceover extraction (T1 items 3–4)

See `wo/FVC-007/T1-ASSET-SWEEP-REPORT.md` for the full ledger. Summary:
`videos/kbeauty-one-percent-line-v2/vo/source-vo.wav` built from the 8
per-scene WAVs at `videos/kbeauty-one-percent-line/assets/voice/{01..08}.wav`,
placed at the composition's own start offsets per `STORYBOARD.md`'s frame
table, padded to the rendered MP4's actual total duration (115.60s, probed
directly — not the STORYBOARD's rounded 115.54s). SHA-256:
`ea4dc2823f21cf6601302725d23794564e73272c65c9e456b1d6092b17ce78a9`.
