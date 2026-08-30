# Catalog

Inventory of what this repo contains as of 2026-08-29, with emphasis on
what the most recent working session created or changed. Video projects
live under `videos/<slug>/` as self-contained HyperFrames projects
(`index.html`, `compositions/frames/`, `STORYBOARD.md`, `assets/`,
`renders/`). Reusable stock media and components live under `catalog/`.

## Active video projects

| Project | Current render | This session |
|---|---|---|
| [kbeauty-one-percent-line](videos/kbeauty-one-percent-line/) | `renders/kbeauty-one-percent-line_2026-08-29_21-40-00.mp4` | Hard-cut scene transitions, VO-synced cadence fixes across Frames 4-8, retimed hook payoff, ingredient macro-shot interlude (Frame 4b), first YouTube thumbnail set |
| [retinol-patch-test](videos/retinol-patch-test/) | `renders/retinol-patch-test_2026-08-29_23-00-57.mp4` | YouTube feedback round 2 (bottle bounce-in, camera-punch on "Stop!", spring-pop callouts, compressed ladder draw), frame-zero + img-attribute skill-compliance fixes, YouTube thumbnail set |
| [seoulhabit-launch](videos/seoulhabit-launch/) | (render unchanged this session) | YouTube thumbnail set; QA verification snapshots from retiming/hook-check rounds kept as working history |
| [snail-mucin-truth](videos/snail-mucin-truth/) | `renders/snail-mucin-truth_2026-08-29_07-21-10.mp4` | Retimed SFX cues across the caption/frame tracks to match real VO pacing |
| [snail-mucin-medical-secret](videos/snail-mucin-medical-secret/) | (render unchanged this session) | Three YouTube thumbnail concepts explored (medical-secret / yuck-factor / mad-science), not yet chosen |

### New per-project assets this session

- **kbeauty-one-percent-line** — source photography (`assets/images/hook-bottle-photo.png`, `loop-centella-leaf.png`, `loop-water-droplet.png`); thumbnail set (`assets/thumbnail/`: hook-frame source+graded, 3 candidates each with source+final, `thumbnail-final.png`)
- **retinol-patch-test** — thumbnail set (`hook-stop.png`, `powerful-stakes.png`, `safety-stop-card.png`, `thumbnail-final.png`); regenerated voice word-timing sidecars + transcript
- **seoulhabit-launch** — thumbnail set (`hook-frame-source.png`, `hook-frame-graded.png`, `thumbnail-final.png`)
- **snail-mucin-medical-secret** — 3 thumbnail options, each an HTML source + rendered PNG

## Removed this session

Per creator instruction — no longer needed:

- `videos/pdrn-skin-regeneration/`
- `videos/red-ginseng-two-routes/`
- `videos/snail-mucin-glass-skin/`

(Full history remains recoverable from git — e.g. `git log --all -- videos/pdrn-skin-regeneration`.)

## Other video projects in this repo (untouched this session)

- `skincare-ingredient-glossary` (created 2026-08-27)
- `skincare-glossary-part-1-barrier-repair` (created 2026-08-28)
- `skincare-glossary-part-2-hydration-boosters` (created 2026-08-28)
- `skincare-glossary-part-3-glow-brightening` (created 2026-08-28)
- `skincare-glossary-part-4-texture-anti-aging` (created 2026-08-28)

## Shared catalog library (`catalog/`)

Reusable, pre-vetted assets referenced across video projects — check here
before generating or licensing new plates (see root [CLAUDE.md](CLAUDE.md)):

- `ingredient-photography/` — macro ingredient stills, tracked in `manifest.json`
- `product-photography/` — fictional K-beauty product photography (see that folder's own manifest + README for the generation/verification log)
- `visual-components/` — reusable HyperFrames components (e.g. `routine-ladder/`)
- `marks/` — standalone graphic marks
- `ingredients/one-percent-line/` — production record for the kbeauty-one-percent-line video (render history, catalog-imagery usage, authorizations)

## Tooling / config added this session

- `.claude/skills/faceless-video-craft/SKILL.md` — repo copy of the video-authoring skill, kept in sync with the active session copy
- `CLAUDE.md` — instructs future sessions to check `seoulhabit/storyboard-review` (this repo) for existing sourced imagery before generating or licensing new plates
