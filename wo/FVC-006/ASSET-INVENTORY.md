# ASSET-INVENTORY.md — WO-FVC-006, run ahead of Gate 0

Run per WO-006 §4, but corrected to (a) include `catalog/` and `catalog-v2/`,
which the WO's own §4 table omits despite `CLAUDE.md`'s mandate to check there
first, and (b) exclude `.claude/worktrees/` from the sweep, which the WO's own
`find` command does not — the shared tree currently holds two other worktrees
(`ingredient-passport`, `pdrn-clinic`) whose assets would otherwise double-count.

Every entry below was opened and read (README + `file`/`identify` on the actual
binary), not inferred from a filename — per this WO's own review note and
WO-FVC-005's Rule 6 (no item carried on a self-report).

## Sweep command used

```
find . -path ./node_modules -prune -o -path './.claude/worktrees' -prune -o \
  -path ./.git -prune -o \
  \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.webp' \) -print
```

## 1. Photographic plates (reusable stills)

| Path | Count | Dims | Provider | Reusable for this video? |
|---|---|---|---|---|
| `catalog/skin-macro-photography/` | 4 | 1200×1200 (verified via `file`) | Higgsfield `nano_banana_pro` — same model G0-4 defaults to | **Yes, directly.** Real skin texture (pilling/layering/flaking/base), no faces, no packaging, no text — already compliant with §3.4's negative list. README: reuse `04-base-skin.png` rather than regenerating a bare-skin plate. Square crop needs a 16:9 composition strategy (card overlay covering the cropped margin, per the WO's own "reserved negative space" rule). |
| `catalog/ingredient-photography/` | 31 | 2048×2048 (per `manifest.json`; 4 legacy alternates at 896×1200) | mixed, tracked per-asset in `catalog/manifest.json` | Ingredient-specific hero shots (glass, serum, ceramic) — usable for scene system 1 (cinematic editorial) where the beat names a specific ingredient. Not usable where the beat has no named ingredient. |
| `catalog/product-photography/assets/` | 12 | 1536×2752 (9:16) | tracked in `catalog/manifest.json` with per-asset `glyph_check`/`claim_check`/`brand_check`/`face_check` | Portrait crop — same centre-safe problem the WO already flags for the Drive assets. Usable only with a 16:9 recompose, and only for beats that want a product bottle, not skin/mechanism. |
| `videos/exosome-label-problem/assets/plates/` | 10 | mixed (serum bottle + crop, 3 material tiles + crops, intact-skin + crop) | — | **Closest existing analogue to this video's subject** (a different "one word covers several unequal things" video). The 3 material tiles are the actual source asset behind `MaterialTriptych` (§1 below) — reusable as-is if this video runs a similar "one term, several evidence tiers" beat. |
| `videos/ectoin-survival-molecule/assets/plates/` | 41 (27 JPG stills + 14 MP4) | mixed | — | Largest existing plate library: barrier calm/stressed, membrane, serum, toner, sunscreen, bottles, flatlay, plus a `C-*` skin-macro reuse set. Generic skincare stills — usable wherever a beat needs an unbranded product/skin plate and doesn't need this video's specific ingredients. |
| `catalog-v2/ingredients/*/assets/` | 9 | — | tracked in each ingredient's `manifest.json`, `catalog-v2/registry.json` (`policy: harvest_first`) | Newer, smaller, ingredient-scoped (snail-mucin, pdrn, centella-cica). Same reuse logic as `ingredient-photography/`. |
| `brand/channel/` | 4 | — | — | End-card and brand furniture only (`avatar-800.png`, `banner-2560.png`, `watermark-150.png`, plus `assets/images/macro-serum-drop.png`). **Note:** the WO's §4 names `seoulhabit-avatar-800.png`, `channel-avatar-800.png`, `ChannelAvatarCard.html` — none of these filenames exist; the real files are `brand/channel/avatar-800.png` / `avatar-800.html`. |

**Total real, non-QA image assets found: ~336** (of 1,386 image files repo-wide;
~1,050 are QA artifacts — `.thumbnails/`, `snapshots/`, `qa*/`, `renders/`,
`frames/` — and out of scope for reuse).

## 2. Visual mechanism components (`catalog/visual-components/`, 21 total)

Mapped against WO-006's own four scene systems. Each entry below was opened —
README read in full, not filename-matched.

### System 2 — native HTML/SVG diagram (mechanism, anatomy, barrier cross-sections)

| Component | Confirmed to be | Canvas | Verdict |
|---|---|---|---|
| **`skin-band`** | Labelled two-layer skin cross-section (epidermis/dermis, dashed boundary at a caller-chosen `boundary_frac`). API: `skin_band(w, h, boundary_frac=0.30)` — canvas-agnostic SVG fragment, `w`/`h` are parameters. Deterministic, no runtime randomness. | agnostic (SVG fragment) | **This is WO-006 style frame #2 already built.** The WO's proposed net-new `sh-mech` component may be building a fourth version of something the catalog already harvested once — the README itself documents three prior uncatalogued one-offs (`centella-tiger-grass`, `betaine-salicylate-gentle-bha`, `pdrn-cellular-science`) before this harvest. |
| `barrier-wall` | Barrier breaking apart / reforming | — | Third independent build of that mechanism per its own README — a reuse candidate for any "barrier compromised" beat. |
| `molecule-states` | One molecule shown in three physical states, static plate, seeded PRNG | **explicitly tested at 1920×1080** (README documents a 1.03 stage-scale edge-shift measured at that canvas) | 16:9-verified — direct evidence this component class works at the WO's target canvas. |
| `split-face-protocol` | Bilateral clinical study diagram (`#control-arm`/`#active-arm`) | — | The WO explicitly wants to avoid clinical-gore framing for its injection-vs-topical frame; this is a fixed clinical-trial diagram, not a fit as-is, but confirms the pattern exists. |

### System 3 — split-screen claim vs evidence ("the spine of this video")

| Component | Confirmed to be | Canvas | Verdict |
|---|---|---|---|
| **`material-triptych`** | N (2–4) parallel items shown side by side, joined by a rail, then the join struck through — "these share a name but not the evidence behind it." Harvested from `exosome-label-problem` scene 03. | **1080×1920 (9:16), safe-area padding baked in** | **This is this video's thesis, already built as a component** — but authored portrait. Using it in a 16:9 long-form chapter needs either a canvas port or a deliberate portrait-insert treatment; flag as a design decision, not a blocker. |
| `split-compare` | Vertical bisector, tint flood on the interrogated side only, no success color. Generalized from `split-face-protocol` — explicitly for "these two things aren't rivals" or "claim being checked vs. the answer." | full-bleed, ~1080 wide | Directly fits a two-thing claim-vs-evidence beat; the N=3+ case is `material-triptych`, not this one. |
| `evidence-meter` | Claim → instrument → source footnote, 4-level confidence scale (open/inferred/qualified/known). Flat 2D and Three.js variants. Cites real ingredient source IDs, not placeholder text. | — | Direct fit for K-rule sourcing display per claim. |
| `graded-scale` | Hard-enum 1–5 badge, `validateGradedScale()` | — | Usable for a coarser evidence-strength readout than `evidence-meter`. |
| **`unsourced-flag`** | Disclosure badge for guidance/claims with no record in the source-tracking system — the exact visual counterpart to K-2b's disclosure-forward path. Confirmed converged independently across 6 shipped videos before being cataloged once. | — | **Ready-made resolution for the WO's own T2 "UNSOURCED" bucket** — the WO proposes handling this in prose (`FLAGS.md`) with no on-screen treatment specified; this component already exists for exactly that gap. |

### Not yet needed but confirmed present

`celestial-arc`, `dawn-to-dusk-routine`, `dialogue-lanes`, `factor-converge`,
`frosted-panel`, `question-gate`, `routine-ladder`, `running-gag-badge`,
`seoulhabit-endcard`, `stat-reveal`, `term-definition`, `threshold-list` — not
mapped to this video's beats yet; listed so a later beat-mapping pass (T4) checks
here before inventing anything.

**All 21 are marked "Spike" status** — validated visual specs with a real
`README.md` + `*-spike.html`, not wired to any build pipeline (`build.mjs` or the
WO-005 compiler). Reuse means porting the mechanism, not importing a module.

## 3. QA tooling already built (relevant to T10)

| Tool | What it does | Status |
|---|---|---|
| `catalog/tooling/check-safe-area.py` | Rendered-pixel safe-area gate; **has a `--landscape` flag** for 16:9 | exists, not run this session |
| `catalog/tooling/check-static-hold.py` | Detects frozen scenes (Δ=0.00) | exists |
| `catalog/tooling/check-cadence.py` | Cut-pacing gate | exists |
| `catalog/tooling/continuity-audit.py` | Cross-scene continuity check | exists |

T10 as written proposes extracting contact sheets and inspecting "by hand" for
several of the things these scripts already automate. Recommend running them
rather than rebuilding the checks manually.

## 4. Net coverage estimate

WO-006 §4 predicted: **30–40 net-new plates, 85–95% of the visual load net-new.**

Against what's actually cataloged:

- **Scene system 2** (mechanism/cross-section): `skin-band` alone may cover the
  named style-frame #2 mechanism without any new generation — pending a design
  review of whether its exact visual treatment matches this video's tone.
- **Scene system 3** (claim vs. evidence — the spine): `split-compare`,
  `evidence-meter`, `graded-scale`, `material-triptych`, `unsourced-flag` cover
  the *mechanism* for every beat type this scene system needs. What's still
  net-new per beat is the *content* (which claim, which source, which two/three
  things), not the visual machinery.
- **Scene system 1** (cinematic editorial) and any beat needing a specific named
  ingredient plate not already in `catalog/ingredient-photography/` or
  `catalog-v2/` — this is where genuine net-new generation is most likely needed,
  and where the WO's estimate is probably closest to right.
- **Scene system 4** (consumer checklist) — the WO's own §3.2 already specifies
  "flat, no photographic plate," so this system needs zero plates regardless.

**This does not fully dissolve G0-2 or G0-4** — scene system 1 and any
ingredient-specific beat in system 2/3 will likely still want new photographic
generation, so a provider ruling is still needed. But the *scale* of that need is
materially smaller than "85–95% of the visual load," and the *mechanism* need for
systems 2–4 may be close to zero net-new. This inventory is offered as the
evidence G0-2/G0-4 should be decided against, not as a resolution of either.
