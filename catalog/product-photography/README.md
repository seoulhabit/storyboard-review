# Product Photography (fictional K-beauty packaging)

Twelve studio product-photography stills of **fictional** Korean skincare
packaging — unbranded, built to 2026 K-beauty conventions (skinimalism,
mono-material glass/aluminium, refill systems, transparent walls, hinged
pad jars, 2nd-gen airless cushions). For thumbnails, channel art, NLE-cut
B-roll, Shorts Studio inputs, and website use.

**Not HyperFrames assets.** The HyperFrames video lane is browser-drawn
only (SVG/CSS/canvas/WebGL) and takes no generative imagery — see
`seoulhabit-video-3d`'s SKILL.md. Feeding any of these into a composition
needs its own filed decision record first.

Generated via Higgsfield (`nano_banana_pro`), 2k resolution, PNG. Per-asset
provenance (model, prompt hash, job id, verification results) lives in
[`../manifest.json`](../manifest.json), one record per surviving asset.

## Prompt structure

Three files under [`prompts/`](prompts/): [`style-core.md`](prompts/style-core.md)
(shared look — palette, material, lighting, hard exclusions),
[`negatives.md`](prompts/negatives.md) (exclusion list), and
[`scenes.json`](prompts/scenes.json) (per-scene bodies, 12 scenes). Final
prompt = style-core + scene body + negatives. Change the look in
style-core once rather than editing every scene.

## The set

| Scene | File | Depicted as | Aspect |
|---|---|---|---|
| A01 | `A01-01.png` | Frosted glass dropper bottle, 세럼 · 30mL | 9:16 |
| A02 | `A02-01.png` | Aluminium airless pump, refill cartridge lifted out, 로션 · 50mL | 9:16 |
| A03 | `A03-01.png` | Hinged toner-pad jar with integrated tweezers, 토너패드 · 70매 | 9:16 |
| A04 | `A04-01.png` | Clear tube, gel visible through the wall, 젤 · 80mL | 9:16 |
| A05 | `A05-01.png` | Glass vessel + paperboard refill sachet, 에센스 · 100mL | 9:16 |
| A06 | `A06-01.png` | Open cushion compact, 쿠션 · 15g | 9:16 |
| B01 | `B01-01.png` | Droplet on glass (texture macro, no label) | 9:16 |
| B02 | `B02-01.png` | Whipped-cream swirl in a dish (texture macro, no label) | 9:16 |
| B03 | `B03-01.png` | Balm mid-melt (texture macro, no label) | 9:16 |
| C01 | `C01-01.png` | Six-product shelf lineup, all 6 labeled | 16:9 |
| C02 | `C02-01.png` | Hand dispensing serum, framed below the wrist, 세럼 · 30mL | 9:16 |
| C03 | `C03-01.png` | Overhead flat-lay, 4 products labeled | 16:9 |

Every asset in this table survived verification and is catalogued in
`manifest.json`. Nothing here was retouched — a frame that failed
verification was discarded and regenerated from an adjusted prompt, never
patched after the fact.

## Hard constraints (all 12 verified against these)

- **Unbranded, no faces.** No real brand names, logos, or recognizable
  trade dress. No human faces; C02's hand is cropped at the wrist.
- **No claims on any rendered surface.** Labels carry nominal fields
  only — Korean category word + volume/count (e.g. `세럼 · 30mL`). No
  percentages, no durations, no efficacy words, no badges or seals. A
  generated image can't carry a source chip, so it asserts nothing.
- **No glow, no bloom, no lens flare.** Matte, unlit, flat-shaded, high-key
  lighting. Palette: paper white, mist grey, celadon, ink, one muted aqua
  accent maximum per frame. The glossy wet-glass K-beauty default look is
  explicitly excluded.

## Verification method

Every frame was verified from the rendered pixels, never from the prompt
text — a model can render text adjacent to what was asked for (a volume
marking drifting into something else), so each Hangul label was inspected
glyph-by-glyph at 100% crop before being accepted. `claim_check` /
`brand_check` / `face_check` ran on every frame regardless of scene type.
A frame that failed any check was discarded and regenerated from an
adjusted prompt — never retouched.

### Discards (not catalogued, kept here for provenance)

- **B02, attempt 1:** cream swirl rendered with real specular gloss —
  the explicitly-banned glossy wet-glass K-beauty look, not the softer
  refraction judgment call made for B01's droplet.
- **B02, attempt 2:** still glossy, plus unintended blue marbling running
  through the cream — more than the one-accent rule allows. Fixed on
  attempt 3 by reframing the product as a thick opaque whipped cream
  instead of a translucent gel; `scenes.json` updated to match.
- **C03, attempt 1:** a malformed glyph — the lotion pump's label read
  `로선` (dropping the 션 y-glide) instead of `로션`. Caught only by
  zooming into pixels, not by trusting the prompt.
- **C03, attempt 2:** fixed the glyph but introduced a duplicated,
  floating copy of the `토너패드 · 70매` label disconnected from any
  object. Fixed on attempt 3 by explicitly forbidding duplicate/floating
  label text; `scenes.json` updated to match.

### Judgment calls (catalogued, flagged rather than silently passed)

- **A04:** tiny illegible embossed numerals on the tube's crimp-seal
  pull-tab — non-Hangul, no claim or brand content, read as generic
  manufacturing batch-code texture rather than an asserted claim.
- **B01:** the droplet carries necessary internal light/dark modeling to
  read as a transparent liquid at all — refraction, not a beauty-lighting
  specular highlight. The plate and background stay flat matte.
- **C02:** renders two hands (one tilting the bottle, one receiving the
  drop) rather than the single hand the scene body asked for — that
  instruction was physically self-contradictory (a dropper can't be
  tipped and caught in the same hand's own palm). Both hands are cropped
  at the wrist with no face or body, so the hard constraints hold.

## What this is for

Raw B-roll / thumbnail / texture-plate stock for SeoulHabit video
projects. Not wired into any composition or build pipeline — approved
surfaces are thumbnails, channel art, NLE-cut B-roll, Shorts Studio
inputs, and the website only.
