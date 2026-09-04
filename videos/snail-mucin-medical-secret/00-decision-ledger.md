# Decision ledger — snail-mucin-medical-secret

Run started: 2026-09-03 19:20 · Channel: SeoulHabitSkin · Baseline: read, not rewritten (render mode)
Credit budget: 200 pre-production · Spent: **0** (no vidIQ call in render mode) · Tags: `render-mode`, `retrofit-v2.1`

Format: `[stage/rule] fork → value | data read (threshold) | tool`

Scope: **render mode** on an already-shipped render
(`renders/snail-mucin-medical-secret_2026-08-29_06-52-57.mp4`, 1080×1920, 113.87 s, 30 fps),
re-gated against faceless-video-craft **2.1.0**. S1–S4, S8, S9 not run.

## S0.0 Environment
[S0.0] OUT → `<repo>/videos/snail-mucin-medical-secret/` | `/mnt/user-data/outputs` absent (tested fresh) | test -d
[S0.0] engine → `hyperframes@0.8.17` | project `package.json` pin; global 0.8.27 deliberately NOT used | npx
[S0.0] project skill → **none** | no SKILL.md in repo; project CLAUDE.md is the generic HF template | find
[S0.0] `K-*` floor → applies undelegated | no project skill to be stricter | decision-policy §Claims

## S5 Beat sheet
[S5/C-1] beats → not re-derived | render mode; VO and beat timing unchanged from the 2026-08-29 retime | —
[S5/C-2] cadence → source-level count skipped as non-authoritative; the pixel answer is `[S7/R-2]` | —
[S5/C-3] end scene → n/a (Short) | youtube-delivery §Formats

## S6 Composition
COMPANION-RESOLVED:frontend-design (skill-tool)
[S6/A-1] catalog → `catalog/tooling/`'s four QC scripts **reused, not rebuilt**; `check-static-hold.py`
  was copied to the scratchpad and **re-calibrated** rather than edited in place, so the shared catalog
  is untouched. | catalog/tooling present | find
[S6/A-2] tokens → unchanged; every fix reuses existing `--green-deep` / `--ink-moss` / `--pearl` / `--cream`
  vars. **No new colour introduced.** | project :root | grep
[S6/A-4] fps/canvas → 30 fps, 1080×1920 (Short) | ffprobe | ffprobe

[S6/A-5] box-sizing → **WAS MISSING in 7 of 7 sub-compositions** (root had it; no scene did).
  → added as the first rule of every scene `<style>` + `captions.html`. The 4 registry components
  already had it. | grep 0/7 (threshold: every composition) | grep
[S6/A-6] type floors → **8 sub-floor declarations found and raised.** Two audit passes were needed:
  - pass 1, scene files: `04 .topbar-chip` 22.0px → 29.2px; `04 .topbar-counter` 20.5px → 27.0px;
    `04 .cruelty-chip-text` 20.5px → 27.0px; `02 .sm2-label-eyebrow` 24px → 28px.
  - pass 2, **registry components — missed by pass 1 and caught by the S7 frame gate.** Component type
    is sized against its **mount box**, not the canvas: in a 756×750 mount `grid-card-assemble` resolved
    to label **16.5px** / body **19.5px**, and `split-tilt-cards` in a 756×740 mount to **15.9px** /
    **16.6px**. My own `[S7/R-2]` narrowing (900→756px) had made these *worse*.
    → `split-tilt-cards` static CSS raised to 32.5px / 33.3px.
    → `grid-card-assemble` needed four constants moved, because it **computes `--gca-font` /
      `--gca-body-font` at runtime and `setProperty`s them onto its own `#root`** — a host-level
      custom-property override is dead on arrival, which is exactly how my first attempt at this fix
      silently did nothing and had to be caught on the pixels a second time. Binding terms were the
      2.6/2.2 cqw caps and `rowCap: 15` (labelCqh 25.9px / bodyCqh 21.4px); all four raised
      (stageW 64→84cqw, rowCap 15→34cqh, caps 2.6→6.0 and 2.2→5.0).
      Verified on the shipped frame at t=40: label cap-height **30px ⇒ ≈41px font**, body **25px ⇒ ≈35px**.
  | floor 26–32px chrome / 32px absolute readable (R1) | computed + measured on rendered pixels
[S6/A-7] contrast → `check`'s Contrast pass **24/24 AA**, and it missed both real failures, because it
  audits declared colour pairs and these are type sitting directly on a photo:
  - `04 .headline-text` ("LUXURY SPA FOR MOLLUSKS") measured **3.04:1** at t=74.00
  - `02 .sm2-label-eyebrow` ("AS LISTED ON THE BOTTLE") measured **2.95:1** at t=20.00 (found by the
    S7 frame gate, not by the source audit)
  → both given an opaque backing in the file's own existing idiom (`green-deep` 88% panel;
  `--ink-moss` panel matching the label box directly beneath it). | 4.5:1 floor (R2) | pixel sample
[S6/A-8] transitions → **VIOLATION.** Short; the rule is *every boundary is a cut*. Found **4 plain
  crossfades** (13.52 / 27.84 / 52.96 / 98.64 s, opacity 0↔1 both `power2.inOut` — both grounds
  compositing at ~50 % at the midpoint) **+ 1 push-slide** at 74.00 s (`y: ±1920`). The push-slide is
  also where the safe-area scan put its worst right-zone intrusion — the exact failure A-8 names.
  → all five converted to hard cuts; clip windows made contiguous (14.02→13.52, 14.82→14.32,
  25.62→25.12, 21.54→21.04, 25.14→24.64 — each now equal to its own VO length). Checked safe first:
  every scene's last GSAP cue is ≤ its new window (12.79 / 2.95 / 23.37 / 18.46 / 23.10).
  **Verified on pixels**, frame-to-frame mean |Δ| across each boundary:
  | boundary | old | new |
  |---|---|---|
  | 13.52 s | ramped over **6** frames | **1** frame — hard cut |
  | 74.00 s | ramped over **3** frames | **1** frame — hard cut |
  | format=short | index.html + ffmpeg diff
[S6/A-9] continuity → n/a, long-form only | youtube-delivery §Formats
[S6/A-10] entrance idiom → **no timeline declared `defaults: { ease }` anywhere (7/7 clean)** — the
  failure mode A-10 was written for is absent here. Three `hold` idioms added, all bounded drifts on a
  stage/group rather than a breathing loop on a text card, each fixing a measured freeze (below).
  | grep `defaults:` = 0 | grep

## S7 Render QA
[S7/R-1] check → **pass** on `hyperframes@0.8.17`: 0 errors / 26 warnings / 11 info, Contrast 24/24,
  Runtime 0, Motion 0. Fix cycles used: **2 of 3**.
  Warnings left standing, with reason:
  - 26 × `studio_missing_editable_id` — a Studio editing affordance, not a render defect. 5 cleared as a
    side-effect of `[S7/R-1b]` (copy elements needed real ids to be assertable); the rest are containers.
  - 1 × `duplicate_media_discovery_risk` — 01-hook mounts `01a-archival-lab.png` twice by design (the
    snap-cut mechanic re-shows the same plate). Pre-existing and intentional.
  11 info findings left standing: 8 are Ken Burns wrappers overflowing their own clipping mask
  (`#sm2PhotoWrap`, `#sm3PhotoWrap`, `#spa-kb`, `#outro-photo-wrap`), 2 are the 05 ambient glows
  bleeding off-canvas by design, 1 is `content_overlap #cap-a/#cap-b` at t=67.85 s — confirmed on the
  extracted frame as a deliberate caption swap, not an occlusion. All intentional and clipped.
[S7/R-1b] motion sidecar → **WAS ABSENT.** No `*.motion.json` existed, so `check`'s Motion pass had
  nothing to verify and reported a vacuous 0/0. → wrote `index.motion.json` **at the project root**
  (one beside a sub-composition is silently ignored): 20 `appearsBy`/`before` assertions naming
  **copy elements, never containers** — 5 bare copy spans were given ids for this — plus **one
  root-scoped** `keepsMoving` (`withinSelector: "#root"`, `maxStaticSec: 1.5`, the Short cadence cap
  from `[S5/C-2]`, replacing the engine's 2 s default). Never per-scene.
  **It earned its place on the first run**, returning 2 errors nothing else had caught:
  - `motion_frozen` 94.42–95.95 s (1.52 s static), over the 1.5 s cap — a real defect in the shipped
    render, fixed with an `[S6/A-10]` bounded drift on `#f05sr-steps`.
  - `motion_appears_late` on `#scrim-w1` — **my assertion was wrong** (it lands at 54.83 s, not 53.9 s);
    corrected to 55.10 s. Not a composition defect.
[S7/R-2] pixel gate → constants confirmed against this project before any number was believed; see below.
COMPANION-RESOLVED:design-critique (skill-tool) — found the two pass-2 defects above (`[S6/A-6]`
  component type, `[S6/A-7]` eyebrow) that the source audit had missed.
[S7/R-3] audio → **VIOLATION on the shipped file**, then fixed. `ebur128` on the 2026-08-29 render:
  I = −13.7 LUFS (in tolerance) but true peak **−0.4 dBFS**, over the ≤ −1.0 dBTP ceiling — R6's exact
  AAC-intersample case. → two-pass `loudnorm` at `TP=-2.5`, then **re-measured on the delivered MP4**,
  not the intermediate: **I = −14.2 LUFS, TP = −2.3 dBFS**. Duration 113.90 s vs VO 113.84 s
  (Δ 0.06 s, inside ±0.1 s).

### `[S7/R-2]` — safe area, and why the gate was believed, then bounded
`check-safe-area.py` on the 2026-08-29 render reported **1188 zone-hits / 455 samples** (top 428,
bottom 452, right 308). A near-total failure is the shape of a mis-calibrated checker, so the named
worst frames were extracted and read. **The gate was right:**
- **bottom** — `captions.html` declared `--cap-band-top: 1600px; --cap-band-height: 320px`, putting the
  entire burned-in caption band at **y 1600–1920**, wholly inside the bottom 20 % rail (y ≥ 1536) where
  YouTube draws title, channel and audio attribution. On a channel where **88.1 % of views come from the
  muted Shorts feed**, the captions *are* the content, and they were rendered under the platform's UI.
- **top** — `01 .hk01-sp-badge` top 116px, `05 .f05sr-topbar` top 64px, `04 .topbar-row` top 84px.
- **right** — content crossing x = 918 on 54–90px margins against a 162px rail, including the `04 / 06`
  chapter counter at x ≈ 927–998.
- **root cause:** no scene declared or consumed any `--safe-*` token — the exact pairing failure
  `youtube-delivery.md` names.
→ Fixes: caption band moved to **y 1300–1520**; pill narrowed 78 %→68 % so a centred caption also clears
  the right rail; all top chrome to y ≥ 208; every right-edge margin to 162px; and **six** colliding
  lower-third elements shifted up to make room for the relocated band (`02 .sm2-label-zone` 1160→1030,
  `02 .sm2-tag-zone` 1380→1200, `04 .cap-slot` 25.5→33cqh, `04 .cruelty-chip` 64→57cqh,
  `05 .f05sr-split-perspective` 520→390, `06 .outro-subscribe-pos` 1214→1100). Centred graphics
  (03's three `grid-card-assemble` mounts, 05's `split-tilt-cards`, 06's subscribe card, 04's closing
  card) were narrowed **symmetrically** so they stay centred; left-aligned copy took an asymmetric
  left-80 / right-162 treatment.

**Residual, and why it is not a defect.** The gate still reports **747 zone-hits** (top 315, bottom 238,
right 194). Every text element was re-checked on frames at t = 0 / 3.25 / 12.25 / 20 / 40 / 66 / 76 / 89 /
110 / 113.70 and **all readable content now sits inside the safe zone**. What remains inside the reserved
zones is the **full-bleed photographic plates**, which are supposed to reach the frame edge — the checker
measures ink as luma difference from the border-ring ground and cannot distinguish a background plate from
type. The masked fraction confirms it quantitatively:

| zone | masked px | zone px | share of zone filled |
|---|---|---|---|
| top | 138 736 | 207 360 | **66.9 %** |
| bottom | 197 582 | 414 720 | **47.6 %** |
| right | 69 089 | 311 040 | **22.2 %** |

Chrome or a caption occupies single-digit percent of a band; two-thirds of a band is a photograph.
Logged as a **known false-positive class for full-bleed scenes**, not carried as an open finding.

### `[S7/R-2]` — static holds, and a checker constant that had to be re-derived
`check-static-hold.py` ships with `CAPTION_BAND_EXCLUDE = False` and the comment *"this project has NO
burned-in captions"* — inherited from a different project. **This project does have them**, and with the
band included the constantly-changing karaoke captions keep the whole-frame diff alive and mask a frozen
hero region. Re-derived against this project's own `captions.html` (band 1300–1520) in a scratchpad copy.
That calibration is what surfaced the finding at all:

| window | 2026-08-29 | after fixes | note |
|---|---|---|---|
| 74.5–78.0 s | **3.5 s frozen** (consecutive frames byte-identical, per-0.5 s mean |Δ| = 0.001) | cleared | `.f05sr-stage` drift |
| 80.0–82.5 s | **2.5 s frozen** | cleared | `.f05sr-stage` drift |
| 88.0–90.5 s | **4.0 s frozen** | **2.50 s — at the 2.5 s ceiling** | `#f05sr-steps` drift; see run report |

A fourth candidate at 38.5–41.5 s in 03-chemistry was **confirmed a false positive**: at full resolution
its Ken Burns moves 4.19 % of pixels by >4 levels (mean |Δ| 1.849), invisible only to the 2 fps downscale.

### Mandatory render rules
- rule 1 — no banned non-deterministic API in any composition (the single `Date.now` hit is inside a
  comment saying "no Date.now"); 8/8 timelines registered `paused: true`; no self-running CSS animation.
- rule 2 — 7 of 7 `<img>` carried `object-fit` but **none** carried `loading="eager"`, `decoding="sync"`
  or explicit `width`/`height`. → all three added (natural size 1152×2048).
- rule 8 — `debug-layout` absent everywhere. PASS.

### Delivery
`.srt` / `.vtt` did not exist for this project while five siblings ship them. → both generated.
**First attempt used the wrong source:** `caption_groups.json` is **stale** (129 groups running to
117.42 s), while the authoritative data is the `GROUPS` array inlined in `captions.html` (100 groups,
last ends exactly at 113.84 s). Regenerated from the inlined source; 23 cues, full CTA line intact.

## Halts / blockers
(none — `[S7/R-1]` used 2 of 3 fix cycles; `[S7/R-2]` used its 2 re-renders exactly)

## [NOT IN SKILL]
- **`[S6/A-8]` gives no retiming procedure for converting a crossfade to a cut.** It states the target
  state but not that overlapping clip windows must be made contiguous, nor that the safe check is each
  scene's last cue against the shortened window. Both were needed. Add as a sub-clause of A-8.
- **`[S7/R-2]` assumes there is room to move content out of the reserved zones.** Here the caption band
  could not simply slide up — six lower-third elements had to move first. "Fix the scene(s) named above"
  understates a coupled relayout.
- **`[S6/A-6]` does not say which box component type resolves against.** A `cqw`/`cqh` size inside a
  registry component is relative to its **mount**, so the same component clears the floor in one project
  and fails in another, and a safe-area narrowing can push it under the floor as a side-effect. A-6
  should require the audit to resolve component type against each mount, not only scan scene files.
- **A component may overwrite the very custom properties it documents as inputs.** `grid-card-assemble`
  `setProperty`s `--gca-font` onto its own root at runtime, so a host override silently does nothing.
  Worth a line in A-6 or the engine reference: verify a component override on the pixels, never assume.
- **`hyperframes snapshot` did not apply a mount's `data-variable-values`** — it rendered
  `grid-card-assemble` with its default items rather than the mount's, which makes `snapshot` unsafe as a
  cheap stand-in for a render when verifying anything variable-driven. Observed, not root-caused.
