# Frame — Pilling vs. Peeling

## Design system

Inherited verbatim from `videos/pilling-not-dead-skin/assets/tokens/tokens.css`
(the SeoulHabit Video Design System), per *Consistency across a channel's
videos*. No local token overrides.

```css
--paper: #F7F5F0;   /* ground, scenes 02/04/06/08 */
--ink: #131516;      /* ground, scenes 01/03/05/07/09; text on paper */
--ink-2: #6B6B6B;    /* secondary text on paper -- 4.89:1, passes */
--aqua: #59B8AE;      /* accents, dividers, node fill -- never readable text at small size */
--coral: #C97A5C;     /* spent exactly once: scene 07's card-3 ✗ mark */
```

Measured contrast (via `npx hyperframes check`'s own pass, 16/16 checked and
passed — see Verification below): every text element clears 4.5:1 against
its background. No `--aqua-text`/darker-variant workaround was needed here
(unlike `pilling-not-dead-skin/06-protocol.html`) because aqua is never used
as small readable text in this project — only as a divider, a node fill, and
an underline.

## Fonts

`Inter 800` (headlines, labels), `EB Garamond 400` (scene 05/08/09 display
lines), `JetBrains Mono 500` (kickers, captions, citation chips, mono sub
lines), `Noto Sans KR Video 500` (the 습 glyph in scene 09's lockup only).
All four self-hosted from `assets/fonts/`, all reused verbatim from
`pilling-not-dead-skin` and `peeling-not-progress` (the Korean subset).

## Per-scene design notes

**01-hook** — Full-bleed ink, a drawn fingertip pad + skin-texture band with
6 crumbs, already mid-scatter at frame zero (mandatory rule 4). Payoff stamp
lands at t1.25, inside the ~2s shorts hook window. Panel/text-stack sized to
858×858 + 320px text-stack (64% of the full 1920px canvas) after an initial
build measured only 56% and read top-heavy on inspection — see Verification.

**02-split** — `split-compare` mechanism, neutral no-flood mode (introduces
the split; scene 06 pays it off). Labels settle at frame zero after an
initial fade-in build left a 333ms genuinely blank paper frame at the cut —
see Verification.

**03-residue** — Same-family reuse of `pilling-not-dead-skin/04-stack.html`,
extended from 2 bands to 3 (SERUM/MOISTURIZER/SPF). SVG viewBox tightened
from 620px to 500px tall after the first build left ~170px of genuinely dead
space below the diagram — see Verification.

**04-factors** — New mechanism: 3 nodes converge on 1 center node. Harvested
to `catalog/visual-components/factor-converge/` (production-loop step 12 —
see Catalog contribution below).

**05-flaking** — `catalog/visual-components/barrier-wall/` adapted directly
(fourth independent context for this mechanism). Wall + label + h1 settled
at frame zero — the diagram alone measured too low-contrast against ink to
clear the blank-frame scan on its own (subtle fill/stroke by design); see
Verification.

**06-clue** — `split-compare` again, now with a drawn flake icon (left) and
a crumb-cluster icon (right) instead of scene 02's plain words — the
callback pays off with content. `catalog/visual-components/unsourced-flag/`
verbatim for the "clue, not a diagnosis" disclosure.

**07-fix-pilling** — Adapted from `pilling-not-dead-skin/06-protocol.html`'s
numbered-step column, generalized to 3 cards. All 3 cards settle at frame
zero after a staggered-entrance build left a single small card floating in
an otherwise-empty canvas for ~400ms — see Verification. The entrance beat
moved to the card-3 coral ✗ mark (this video's one coral spend) instead.

**08-fix-peeling** — Adapted from `peeling-not-progress/05-reset.html`'s
3-icon row, reframed with a "switch turns off" beat on the actives icon
(strike line draws across it) instead of all three icons presenting equally.
Icon circles bumped to 220px to match that file's own validated proportions.

**09-close** — Loop-matched to scene 01: same ink ground, same centered
flex-column shape. line1 settles at frame zero (it's also the loop
endpoint, so it gets the same frame-zero discipline as scene 01's hero).
`습 SeoulHabit` lockup + underline draw as the closing beat.

## Component reuse

See `BRIEF.md` § Component reuse for the full table and the considered-and-
declined list (StatReveal, TermDefinition, ThresholdList, FrostedPanel).

## Catalog contribution

**`FactorConverge`** harvested to `catalog/visual-components/factor-converge/`
— a several-inputs-converge-on-one-node diagram, confirmed as a genuine gap
(a discovery pass across every existing component found nothing matching
this shape before scene 04 was built). Fixed to exactly 3 nodes; a real
N-node variant is a documented, undelivered limitation, matching
`StatReveal`'s own honest-limitation disclosure pattern.

Scene 03's 3-band extension of `04-stack.html` and scene 08's reframed
`05-reset.html` are same-family/adapted-file reuses, not new catalog
harvests — the mechanisms already exist in the catalog (`04-stack.html`'s
2-band shed is the same shape as `BarrierWall`'s shed-beat; `05-reset.html`'s
3-icon row is a project-to-project file reuse, not a component gap).

## Verification — Round 3 (2026-09-01, scene 07 retimed)

Scoped verification — only `07-fix-peeling` and the cascade it touched
(scene 08's start, both roots' duration/BGM/SFX, all four caption files)
changed this round. Scenes 01–06 untouched and not re-verified beyond the
project-wide checks below, which cover the whole render regardless.

### 1. `npx hyperframes check`

0 errors, 1 pre-existing warning (`duplicate_media_discovery_risk` in
`05-test.html`, unrelated to this round's edit — not present in round 2's
own recorded "0 warnings," so either a version-bump artifact
(`hyperframes@0.8.22`, same pin as round 2 used) or a check round 2 didn't
actually clear; flagged here rather than silently reconciled, not fixed
since it's out of this round's scope), 6 benign info findings, all in
scenes 01/02/04/05/06 — same shapes round 2 already recorded (Ken-Burns
zoom overflow inside an already-clipped panel, one content-overlap at a
crossfade sample instant, one decorative overflow by design).

### 2. Render + `check-blank-frames.py`

**Real bug caught in this round's own pipeline, not the composition:**
`npm run render`'s default output is a timestamped filename
(`pilling-vs-peeling_2026-09-01_14-45-27.mp4`), not an overwrite of
`renders/pilling-vs-peeling.mp4` — `postrender`'s `check-static-hold.py`
and `check-safe-area.py` invocations hardcode that filename as an argument,
so the first `npm run postrender` after this round's render silently
validated the **stale round-2 file** (20.0s) while `check-blank-frames.py`
(which auto-discovers the most recent `renders/*.mp4`) correctly picked up
the new one. Caught by checking `ffprobe` duration on every file in
`renders/` before trusting any postrender output, not by the scripts
themselves — nothing in the pipeline would have surfaced this on its own.
Fixed by promoting the timestamped render to `pilling-vs-peeling.mp4` and
re-running `postrender` against the correct file. Fixed in this round: `package.json`'s `render` script now passes
`-o renders/pilling-vs-peeling.mp4` explicitly, matching `render:b`'s own
convention, so a future re-render can't reproduce this exact gap.

Blank-frame scan on the correct file: 0 findings (317 frames sampled).

### 3. `check-static-hold.py` (whole-frame + region-aware)

Whole-frame: 0 findings (42 samples, 2.5s ceiling — up from round 2's 40
samples, matching the longer 21.1s runtime). Region-aware: still falls
back to whole-render mode (round 2's own note about re-deriving the
script's scene-boundary parser against this project's single-level 8-scene
root remains open — not addressed this round, out of scope for a
single-scene retime).

### 4. `check-safe-area.py` (hard gate)

0 findings, both variants (84 samples each, up from round 2's 80 — longer
runtime, same sampling interval).

### 5. `check-sfx-durations.py`

0 findings, 23/23 checked — the 4 retimed scene-07 cues and 2 shifted
scene-08 cues all still match their declared `data-duration` against the
actual source files (retiming only moved `data-start`, not any cue's own
duration).

### 6. Audio mastering

Pre-master (raw re-render, both variants): **−23.0 to −23.3 LUFS / −6.5 to
−6.7 dBTP** — consistent with round 2's own pre-master range, confirming
the retime didn't change the mix's overall loudness character. Two-pass
`ffmpeg loudnorm` at the same `I=-14:TP=-2.5` target round 2 established,
video stream copied through (confirmed via matching MD5 on the isolated
video stream, both variants). **Re-measured on the final encoded MP4:**

| | Integrated | True peak |
|---|---|---|
| Variant A | −14.3 LUFS | −2.0 dBTP |
| Variant B | −14.2 LUFS | −2.1 dBTP |

Both within 0.1 LUFS of round 2's own numbers — the extra 1.2s changed
scene 07's pacing, not the mix's overall level. Loop-seam RMS (final 2s):
−16.2 dB both variants, genuinely live (not silence).

### 7. Visual spot-check, scene 07's new pacing

Extracted frames at 15.9/16.7/17.5/17.9/18.5/19.0s (variant A). Confirms
the intended beat schedule lands where authored: actives icon still fully
opaque at 15.9s (strike hasn't started), struck through by 16.7s,
`Cutis · 2006` chip fading in at 17.5s, both chips fully settled and held
from ~18.0s through the 19.1s cut — a genuine 1.1s+ hold with both
citations legible, versus round 2's ~0.75s.

---

## Verification — Round 2 (2026-09-01 recut)

The round-1 verification record below this line described a render that no
longer exists — replaced rather than amended, per the skill's own warning
against a stale verification claim surviving a real change.

### 1. `npx hyperframes check`

Clean after a genuinely hard debugging pass (see "The box-sizing defect"
below): 0 lint/runtime/layout errors, 0 warnings, 7 benign info findings
(a few px of Ken-Burns zoom overflow inside an already-clipped panel,
a decorative SVG element overflowing its own viewBox by design — matches
round 1's own confirmed-benign `#wash-group` finding — and one
content-overlap info at the hook's mid-crossfade sample instant, expected
during a 0.30s crossfade).

### 2. The box-sizing defect (found and fixed this round, not present in round 1's simpler layouts)

Every one of round 2's 9 scene files combines an explicit height/flex-basis
with padding on the same element, and none declared `box-sizing`. Under the
CSS default (`content-box`), `.stage`'s `height: 1920px` plus its own
`192px`/`384px` top/bottom padding rendered as an actual **2496px** box —
push­ing bottom-anchored content (citation chips, the CTA) past the real
canvas edge. This was invisible from source, reproduced identically
regardless of `--safe-*` values or nesting depth, and was only caught by
comparing `getBoundingClientRect()` against `getComputedStyle().height` on
a real compiled render. A second, related defect (`min-height:auto`
silently overriding an explicit small `flex-basis` with a flex child's own
content size) surfaced once the first was fixed. Both are now fixed
project-wide: a `*, *::before, *::after { box-sizing: border-box; }` reset
plus `min-height: 0` on every flex child carrying an explicit small basis.
See BRIEF.md § Round 2 and the `faceless-video-craft` SKILL.md update this
round proposes — this defect class is general enough to be worth the
skill's own record, not just this project's.

### 3. `check-blank-frames.py`

Clean: 0 findings (299 frames sampled) on the final mastered render.

### 4. `check-static-hold.py` (whole-frame + region-aware)

Whole-frame: 0 findings (40 samples, 2.5s ceiling). Region-aware: 0 findings
(no `index.html` scene list matched by the script's own parser against this
round's single-level 8-scene root — it fell back to whole-render mode,
flagged in its own output; re-derive the script's scene-boundary regex
against the current `index.html` before trusting a region-aware "clean" on
a future round).

Own cadence measurement (mean `|Δluma|` per 8fps step, the metric this
round's own SKILL.md update proposes as a gate): active-step share rose
from round 1's measured **6%** to **11%**; no scene sits frozen for its
full duration (round 1 had three: medians 0.000/0.010/0.002). `07-fix-peeling`
is the weakest scene by this metric (0 steps clearing the 1.0 threshold,
though real per-element motion is authored throughout) — worth a closer
look in a future pass if cadence is revisited.

### 5. `check-safe-area.py` (hard gate)

**Failed twice before passing.** First failure: the box-sizing defect
above (38 sampled frames in violation, up to 10512px masked in a single
frame). Second, smaller failure after that fix: `08-close`'s full-bleed
low-opacity (0.18) background plate crop still registered as "ink" in the
reserved right-rail zone under the checker's luma-diff mask — confirmed
this project's own instance of the skill's documented "a full-bleed
photographic plate reliably hard-fails the safe-area gate even at low
opacity" risk. Fixed by insetting the plate to the safe content box instead
of full-bleed. **Final state: 0 findings, 80 samples, both variants.**

### 6. `check-sfx-durations.py`

Clean: 23/23 SFX elements checked (10 files, several reused as multiple
cues), no findings.

### 7. Audio mastering

Pre-master (raw render, both variants): **−22.9 to −23.2 LUFS / −6.5 to
−6.7 dBTP** — no mastering pass had been run yet at that point in the
round. Two-pass `ffmpeg loudnorm` targeting `I=-14:TP=-2.5` (extra
pre-encode headroom vs. round 1's `TP=-1.5`, specifically to survive the
AAC re-encode step — round 1's true peak was verified on the PCM
intermediate, not the shipped file, and the shipped file measured +0.5
dBTP as a result). Video stream copied through unchanged (`-c:v copy`).
**Re-measured on the final encoded MP4, not the intermediate:**

| | Integrated | True peak |
|---|---|---|
| Variant A | −14.3 LUFS | −1.8 dBTP |
| Variant B | −14.1 LUFS | −1.5 dBTP |

Both clear the −1.0 dBTP target with room to spare.

### 8. Thumbnail

Extracted from variant A at t=1.6s (the hook's payoff, well-settled — real
macro residue plus "Those white flakes may not be your skin."). Light grade
(contrast 1.08×, saturation 1.05×). Downscaled to 68×120 (grid scale) and
confirmed legible before finalizing — a marked improvement over round 1's
hero panel, which measured 1.05:1 contrast against its own ground and was
effectively invisible at grid scale.

---

## Verification — Round 1 (superseded, kept for history)

Full account, in the order each check actually ran.

### 1. `npx hyperframes check`

Clean on the first pass: 0 lint/runtime errors, 0 warnings. 3 layout `info`
findings, all investigated and confirmed benign against actual rendered
pixels, not dismissed on severity alone:

- **`content_overlap` at t=8.625s** (scenes 03/04's cut boundary, sample
  landing 0.025s into scene 04) — snapshot-extracted at 8.6s/8.65s showed a
  clean hard cut with no visible bleed; the finding is the checker sampling
  DOM geometry across both scenes' (non-visible + visible) elements at a
  boundary instant, not a real render defect.
- **`container_overflow` on `#wash-group`, scene 05, t=13s** — the
  `barrier-wall` component's own wash rect starts above its SVG viewBox by
  design (descends onto the wall from off-frame); snapshot-confirmed it
  never visually intrudes into the headline zone above it. Matches the
  catalog component's own unmodified geometry.

### 2. Snapshot inspection (`npx hyperframes snapshot`)

Full-project snapshot pass at all 9 scene midpoints + the 8.55/8.6/8.65s cut
boundary surfaced two real layout defects the check's own numeric pass
didn't flag (both are taste/fill judgments, not lint-catchable):

- **Scene 01 under-filled the frame** (58% of canvas vs. the 65-80% target)
  and its hero payoff sat below the 96px type floor (84px). Fixed: panel
  858×858 (was 858×760), text-stack 320px (was 260px), payoff font 96px
  (was 84px) — re-verified at 64% canvas fill.
- **Scene 08's icon circles (200px)** read slightly under-scaled next to
  `peeling-not-progress/05-reset.html`'s own validated 220px — matched.

### 3. Render + `check-blank-frames.py`

First render: **5 near-blank stretches** (200–400ms each), all at scene-cut
boundaries (scenes 02, 05, 06, 07, 09's own local frame zero). Each was a
real instance of the skill's own named failure mode — "a headline authored
to fade in over its first 0.3–0.5s... makes the literal t=0 export frame
near-blank" — generalized here to every scene's *own* opening frame, not
just the video's global t=0. Fixed by settling each scene's primary content
(labels, wall diagram, headline, cards, takeaway line) at frame zero and
moving the entrance beat to a secondary element (a divider draw, an
h2 second line, a coral mark pop). Two scenes needed a second round:

- **Scene 05** — settling the wall+label alone wasn't enough; the diagram's
  own subtle fill/stroke measured too low-contrast against ink to clear the
  scan. Fixed by also settling h1 at frame zero.
- **Scene 07** — tightening the card cascade from 0/0.35/0.60 to
  0/0.15/0.30 wasn't enough either; a single small card in an otherwise-
  empty canvas is the skill's "small element in a large canvas" failure
  even at a shortened 200ms. Fixed architecturally: all 3 cards now settle
  at frame zero, and the entrance beat moved to the coral ✗ mark instead.

Re-render after both rounds: **0 findings** (390 frames sampled).

### 4. `check-static-hold.py` (whole-frame + region-aware)

Whole-frame pass: 0 findings (52 samples, 2.5s ceiling) — no scene sits
frozen for the whole-frame check's cadence window.

Region-aware pass: **6 region-level content-voids flagged** across scenes
03, 05, and 06. Per the tool's own documented false-positive classes, each
was verified against extracted frames with the checker's own 3×2 grid
overlaid, not trusted from cell coordinates alone:

- Scene 06's four flagged cells (top-right, mid-left, bottom-left,
  bottom-right) — extracted frame at t=15.5s shows both fields fully
  populated (star + "BARE SKIN" + sub-line on the left, crumb icon +
  "AFTER LAYERING" + sub-line on the right, the flag pill spanning the
  bottom-center). **Confirmed false positive** — real, legible content in
  every flagged cell.
- Scene 05's top-left cell — extracted frame at t=12.5s shows "Peeling is
  different — / actual skin flaking." clearly spanning across the grid's
  center line into the left cell. **Confirmed false positive.**
- Scene 03's bottom-right cell — the citation chip appears there on
  schedule (visually confirmed at t=7.5s) after a brief early window with
  no content; the "empty after carrying content" framing appears to reflect
  the checker's own baseline sensitivity near scene start, not a dead hero
  region. **Confirmed false positive** against the actual pixels.

No fix applied — findings are advisory by design (`check-static-hold.py`
always exits 0) and this project's own re-verification confirmed none of
the six describes a real defect.

### 5. `check-safe-area.py` (hard gate)

Clean: 0 findings across 104 samples at the project's exact token values
(top 192 / bottom 384 / right 162 / left 72). No scene uses a Ken Burns
zoom in this project, so no `--safe-*-zoomed` derivation was needed.

### 6. `check-sfx-durations.py`

Clean: 10/10 SFX elements checked, no findings.

### 7. Audio mastering

Pre-master integrated loudness (raw render): −23.2 LUFS / −6.1 dBTP.
Two-pass `ffmpeg loudnorm` (measure, then linear correction against the
measured values), video stream copied through unchanged — confirmed by
matching MD5 checksums on the isolated video streams before/after mastering.
Independently re-measured after mastering: **−14.1 LUFS integrated / −1.50
dBTP** (target −14/−1.5). Final-2s loop-seam RMS: −25.6 dB (genuinely live,
not silence) — the BGM envelope's 0.15 floor at both ends does what it was
meant to.

### 8. Thumbnail

Extracted at t=2.2s (hook payoff, well-settled). Light grade (contrast
1.08×, saturation 1.15×, unsharp). Downscaled to 120×213 and confirmed
legible at grid scale before finalizing.
