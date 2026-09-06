# Decision ledger — photo-led visual redesign

Follows the pattern set by `videos/ectoin-survival-molecule`,
`videos/ceramides-skin-barrier`, and the Ingredient Passport benchmark
(`.claude/worktrees/ingredient-passport/videos/ingredient-passport/00-decision-ledger.md`
[D-2]) for overriding `catalog/product-photography/README.md`'s "not
HyperFrames assets" note. Unlike that benchmark's ledger, this one keeps the
full asset list here rather than pointing at a separate manifest file — the
benchmark's own `04-manifest.md` reference is dangling on disk; this project
does not repeat that.

## [D-1] Photographic plates cleared for this composition

**Context.** The review that produced this redesign found the video in one
flat vector register for its full 2:24 runtime (0 hard scene breaks above
ffmpeg `scene>0.3`, versus 25 in the benchmark) and asked for 5–7 photo-led
beats reusing existing catalog assets wherever possible. Every photographic
lane in `catalog/` is model-generated (Higgsfield `nano_banana_pro` /
`marketing_studio_image`); there is no licensed-stock tier, so "reuse over
generate" here is a vetting decision, not a real-vs-AI one.

**Governance conflict.** `catalog/product-photography/README.md`: *"Not
HyperFrames assets. The HyperFrames video lane is browser-drawn only
(SVG/CSS/canvas/WebGL) and takes no generative imagery... Feeding any of
these into a composition needs its own filed decision record first."* Three
other projects have already overridden this note with exactly that kind of
record:

- `videos/ectoin-survival-molecule/DELIVERY.md` ("2026-09-04 — retention
  master"): *"The 'no generative imagery in the HyperFrames lane' note ... is
  overridden for this master by the operator's brief; this section is that
  decision record."*
- `videos/ceramides-skin-barrier/BRIEF.md` (~lines 95–125): *"This is a
  deliberate departure from `frame.md`'s explicit 'no photorealism, no
  generative imagery' rule."*
- Ingredient Passport benchmark `00-decision-ledger.md` [D-2], clearing
  `B02-01` among others for exactly this kind of use.

This is that same kind of record for `videos/collagen-where-did-it-go`.

**Decision.** Cleared for use inside this composition, subject to the
constraint every prior override kept: a generated plate carries the
*tactile/evidentiary* role only, never the *explanatory* one — mechanism
diagrams (the barrier, the tract, the trial grid) stay browser-drawn.

## Asset ledger

| Asset (`assets/images/`) | Source | px | Provenance | Beat |
|---|---|---|---|---|
| `skin-base.png` | `catalog/skin-macro-photography/04-base-skin.png` (byte-identical, md5 `67cc7df6…`) | 1200×1200 | Higgsfield `nano_banana_pro`; that folder's own README already approves this exact plate for a composition's tactile role, shipped once before (`pilling-vs-peeling`) | 03-building ground |
| `cream-swirl.png` | `catalog/product-photography/assets/B02-01.png` | 1536×2752 | Higgsfield `nano_banana_pro`, job `2b3795d0-176a-4d58-947a-77832978e8e0`, `catalog/manifest.json`; `claim_check`/`brand_check`/`face_check` all pass | 06-door film beat (paired w/ layering-hand) |
| `layering-hand.png` | `catalog/skin-macro-photography/02-layering-hand.png` | 1200×1200 | Higgsfield `nano_banana_pro`; composition-approved lane | 06-door film beat |
| `sunscreen.jpg` | `videos/ectoin-survival-molecule/assets/plates/I22-sunscreen.jpg` | 1920×1080 | pre-normalized for 1920×1080 delivery in that project; provenance in its own `DELIVERY.md` | 14-hierarchy row 1 |
| `retinol.png` | `catalog/ingredient-photography/16-retinol.png` | 2048×2048 | Higgsfield, numbered set (no per-asset manifest — see `catalog/ingredient-photography/README.md`); surface approval recorded here | 14-hierarchy row 4 |
| `vitamin-c.png` | `catalog/ingredient-photography/20-vitamin-c.png` | 2048×2048 | Higgsfield; a halved orange, i.e. dietary vitamin C — matches the script's actual "protein + vitamin C" claim, not a topical-ascorbic-acid image | 14-hierarchy row 3 |
| `collagen-powder-scoop.png` | **generated this session** | 1024×1024 | `marketing_studio_image`, job `7f243a6d-b869-481c-a3af-ac4ce2eb7b9b`; see gap statement below | 01-hook powder panel, 08-digestion scoop entry |

### Rejected candidates

- `catalog/ingredient-photography/sh-madecassoside.png` — a glass dish of
  white crystalline powder, but it is madecassoside, not collagen. The brief
  names this exact substitution as the trap to avoid ("a madecassoside
  powder image is not a collagen-powder image").
- `catalog/ingredient-photography/11-peptides.png` — off-palette (blue
  tint), and peptide imagery sitting next to an oral-delivery claim is the
  highest-risk frame in the video; safer to keep that beat fully diagrammatic
  (it already is).
- `catalog/skin-macro-photography/01-pilling-macro.png`,
  `03-flaking-skin.png` — depict pilling and flaking, neither of which is
  collagen loss.

## Gap statement — the one generated asset

No collagen powder, scoop, capsule, or supplement plate exists anywhere in
this repo's catalog or shipped projects. `catalog-v2/ingredients/collagen/pack.json`
independently records this as a live gap: `"shared neutral cream and powder
vessel pair"` at priority `now`, noting *"the source video's line-drawn cup
and scoop are too crude, while current V2 containers are ingredient-specific."*
Generating one unbranded plate fills a gap the catalog itself already flagged,
rather than opening a new one.

Constraints applied: unbranded, no readable text, no efficacy claim, warm
ivory seamless ground matching `catalog/ingredient-photography/TREATMENT-SPEC.md`,
single soft-edged shadow, no props beyond the scoop. The same plate is reused
at two different crops (01-hook, 08-digestion) rather than generating a
second — net-new imagery stays at 1, inside the brief's 0–2 budget.

`catalog-v2/registry.json` sets policy `harvest_first`: *"No new generation
during the initial harvest phase."* Generating this plate is a deliberate,
logged exception to that policy for the one asset the catalog cannot
currently supply.

## Claim-safety check

On-screen copy for the new beats was checked against
`catalog-v2/ingredients/collagen/pack.json`'s `claim_rules.prohibited_default`
(forbids "goes straight to your face", "replaces lost collagen", "rebuilds
the dermis"). No new on-screen text was introduced by this redesign — every
new beat is a photographic plate behind or beside the existing, already-
approved kinetic-type copy — so no new claim-safety surface was created.

## [D-2] The `<img>` build guard: ban replaced with validation

`scripts/build_frames.py`'s `_static_asserts` previously rejected any
composition containing the substring `"<img"`, advisory-only (collected into
`FAILURES`, only raised with `--strict-cadence`, which `npm run build` does
not pass), and blind to `<image>`, `background-image`, `data:` URIs, and
JS-injected media nodes. Its own stated reason was a safe-area / clip-path
engineering hazard, not a content policy — confirmed by `BRIEF.md`'s own
(never-implemented) imagery plan for this exact composition.

Replaced with `_media_asserts()`: every `<img>` must be emitted by the new
`actors.plate()` helper (the `.plate > .worldclip > .world` nesting every
`.world` camera already needs), must carry `decoding="sync"`/`loading="eager"`
for a seek-based renderer, must use `object-fit:cover|contain`, and its `src`
must resolve to a real local file under `assets/` — no remote URL, no `data:`
URI, no parent-traversal path. This check is now **hard**: a bad plate fails
`npm run build` immediately, rather than printing an advisory a busy operator
can skip past.
