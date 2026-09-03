# Verification tooling

Not imagery, not a component — a shared script, catalogued for the same
reason a component is: it was built once for a real project and is worth
finding before the next project rebuilds the same check from scratch.

| Item | File | What it is |
|---|---|---|
| [check-safe-area.py](check-safe-area.py) | `check-safe-area.py` | Scans a rendered MP4 for real content inside YouTube Shorts' reserved UI zones, measured on transformed, rendered pixels — catches a class of defect a source-level "are the `--safe-*` tokens consumed" audit structurally cannot see (a `transform: scale()`/`translate()` between a safe-padded box and the canvas moves ink past a compliant padding value without the source ever being wrong). |
| [check-static-hold.py](check-static-hold.py) | `check-static-hold.py` | Scans a rendered MP4 for a static-hold two different ways: a whole-frame PSNR check (the original, project-portable form already in use across this channel), plus a region-aware check that grids the safe content box and flags a cell that goes from carrying real content to essentially empty and stays there — catching a scene's own HERO element sitting dead while unrelated motion elsewhere in the same frame keeps the whole-frame check clean. Advisory (exits 0), like the other `check-*.py` scripts here except `check-safe-area.py`. |

**Provenance.** Built for `videos/peeling-not-progress`'s round-6 safe-area
fix (2026-08-31) — an external QC report flagged content near the Shorts UI
overlap, and a pixel-level audit found three scenes silently overshooting
the real line via exactly this mechanism (a scene-wide Ken Burns wrapper) and
a fourth via a related one (an entrance transform's own transient). See that
project's `frame.md` "Post-render review fixes" round 6 for the full measured
root cause, and `.claude/skills/faceless-video-craft/SKILL.md`'s
*Verification loop* → "Safe-area intrusion scan" and pre-render gate item 7b
for the rule this script exists to enforce.

**Field contract.** `python3 check-safe-area.py <project_root> [render_path]
--safe-top <px> --safe-bottom <px> --safe-right <px> [--safe-left <px>]` —
zone sizes are CLI flags, not hardcoded, so this is drop-in across projects;
pass the calling project's own real reserved-zone pixel values (its tokens,
or the skill's 192/384/162 defaults if the project has no deviation on
record). Samples the render at 4fps, builds an antialiasing-tolerant ink
mask per frame, and exits non-zero if any sampled frame has real content
inside a reserved zone — a **hard gate**, unlike this repo's other
`check-*.py` scripts, which are advisory (always exit 0). Wire it into a
project's own `package.json` `postrender` script alongside
`check-blank-frames.py` / `check-static-hold.py`.

**Fix, 2026-09-01 (`videos/centella-barrier-recut-15s`).**
`check-static-hold.py`'s scene-boundary regex required a literal `class="scene"`
and therefore did not match the canonical `class="scene clip"` markup the
HyperFrames skeleton actually ships (`.clip` is what gives a scene its
full-frame box, so the two-class form is the normal case, not an edge case).
On a non-matching project it silently fell back to treating the whole render
as one scene and printed a "cross-cut false positives are possible" note
rather than an error — which is exactly how a project reads a degraded run as
a clean one. Widened to `class="[^"]*\bscene\b[^"]*"`. Verified both ways on
a real render: whole-render fallback reported 2 region voids, the corrected
scene-aware run reported 1, and the difference was a false positive spanning
a hard cut.

**Status: validated reference, not yet wired into every project.** Confirmed
working against a real render (`peeling-not-progress`'s round-6 mastered
file, before and after the fix) but copied per-project rather than imported —
matches this repo's existing convention for `check-blank-frames.py` /
`check-static-hold.py`, which are also per-project copies, not a shared
module. Copy this file into a new project's `scripts/` directory and wire it
into `postrender` rather than re-authoring an equivalent script from scratch.

---

## check-static-hold.py

**Provenance.** The whole-frame PSNR half of this script already existed
per-project across the channel (`peeling-not-progress`, `mugwort-healing-
herb`, others) — each copy carrying a `CAPTION_BAND_EXCLUDE` flag and a
caption-band crop hand-derived for ITS OWN project. `peeling-not-progress`'s
own copy documented, in its own docstring, a real defect it had already
caused once: inheriting a sibling project's caption-band crop verbatim,
silently cutting real content out of every diff it ran. That documented
warning did not stop the same defect from recurring one project later
(`peeling-question-open`, 2026-09-01): its copy of this script still carried
`mugwort-healing-herb`'s crop and `True` flag despite `peeling-question-open`
having **no burned-in captions at all** — the crop was masking scene 5's own
"THE BOUNDARY" kicker from every scan. Caught only because an external QC
report's one real (if misdiagnosed) finding prompted a full pixel-level
re-verification, not because this script itself flagged anything wrong with
its own configuration — a comment warning about a trap is not the same as
the tool enforcing against it.

The same verification round found a SECOND, independent gap the whole-frame
check cannot see even with a correct caption-band setting: a scene's own
dominant hero element (a `.glass-panel` in this case) went fully empty for
~1.1s — text had exited, a closing lockup hadn't arrived yet — while a
different on-screen element (a closing headline couplet) kept the whole-
frame PSNR comparison alive throughout. The region-aware half of this script
was added specifically to close that gap: it grids the safe content box and
flags a cell that goes from a real content peak to essentially empty and
stays there past a (tighter) per-region ceiling, scoped to one scene at a
time using the project's own `index.html` scene list so a hard cut between
scenes never misreads as "content vanished."

**Known limitations, confirmed, not hypothetical — two classes.** The
region-aware check's "is there real content in this cell" signal is
spatial-variance-based (pixels differing from a per-cell background
estimate), which can misfire two ways, both confirmed on this same project:

1. A textured or gradient plate that isn't real UI content — scene 1's
   frosted-glass card, whose subtle embossed watermark produced a false
   content-then-empty read even after threshold tuning.
2. A weaker SECOND content transition in the same scene/cell reading as
   still-empty relative to an earlier, stronger beat in that same cell —
   confirmed AFTER fixing the source defect this script was built to catch
   (06-open.html's panel-empty gap): the per-scene baseline sits between the
   word-grid's strong peak and the SeoulHabit lockup's weaker one (in the
   specific column the glyph mostly doesn't reach), so the fix's own arrival
   still read as "empty." Direct frame extraction at the flagged timestamps
   (this skill's own mandated verification method) confirmed the true empty
   window shrank from 1.30s to 0.40s — the fix is real; the tool's own
   continued flag on it is the false positive, not the other way around.

Both are why the check stays advisory (exits 0) and prints a standing
reminder to confirm each candidate against the actual extracted frame, not
trust the cell coordinates alone — including trusting THIS script's own
output, which is exactly the "verify by pixels" discipline the skill asks of
an external QC report applied reflexively to this script's own claims too.
A future improvement worth trying before re-deriving this from scratch: a
per-cell threshold scaled to that cell's own observed ink range (not one
fixed delta shared across every content state in a scene) — not yet
implemented here.

**Field contract.** No CLI flags (unlike `check-safe-area.py`) — the
per-project constants at the top of the file (`CAPTION_BAND_EXCLUDE`,
`SAFE_TOP`/`SAFE_BOTTOM`/`SAFE_RIGHT`/`SAFE_LEFT`, the grid size, all four
threshold constants) are meant to be hand-re-derived per project, matching
this repo's existing per-project-copy convention for this file (see the
`peeling-not-progress` → `mugwort-healing-herb` → `peeling-question-open`
caption-band history above for exactly why copying without re-deriving is
the recurring failure mode this entry exists to break). Reads scene
boundaries from the calling project's own `index.html`
(`data-start`/`data-duration` on each `.scene[data-composition-src]`); falls
back to treating the whole render as one scene if that file or pattern isn't
found. `python3 check-static-hold.py <project_root> [render_path]`.

---

## 2026-09-02 — canvas awareness (both scripts)

Both scripts hard-coded `CANVAS_W, CANVAS_H = 1080, 1920` as module constants with
no override. Run against a 1920×1080 render they did not error — they **lied**, in
two different directions at once. Measured on a fully-inked landscape frame with the
old constants:

```
bottom zone  mask[1536:, :]   -> shape (0, 1920)     sum=0        FAIL-OPEN
right  zone  mask[:, 918:]    -> shape (1080, 1002)  sum=1082160  wrong region
```

The bottom slice runs past the end of a 1080-tall array, so numpy returns an empty
view: the **hard gate** reported "no findings" and exited 0. The right slice measured
the right 52% of the frame instead of a 162px rail.

**Fix.** Both scripts now probe the render with `ffprobe` and **refuse (exit 2)** on a
canvas mismatch rather than running against the wrong geometry. `check-safe-area.py`
gains `--canvas-w` / `--canvas-h` / `--landscape`; `check-static-hold.py` gains
`--landscape`.

A comment saying "this assumes portrait" would not have prevented this — the file
already said so, in its own docstring, and the gate still passed. The assert is the fix.

### The landscape profile

| | Portrait (Shorts) | Landscape (long-form) |
|---|---|---|
| Canvas | 1080×1920 | 1920×1080 |
| Reserved top / bottom | 192 / 384 | 54 / 108 |
| Reserved left / right | 0 / 162 | 96 / 96 |
| `CADENCE_CEILING_S` | 2.5 | 10.0 |
| Grid rows × cols | 3×2 | 2×3 |
| `ACTIVE` / `EMPTY_DELTA_PX` | 1200 / 300 | 1542 / 386 |

There is no action rail in 16:9, so 162px on the right is *semantically* wrong there,
not just numerically. The bottom 108px is the player progress bar and controls.
End-screen elements occupy the right third and lower-right for the final 5–20s only —
that is a **scene-scoped** reserve, unlike the Shorts rails which bind every frame, so
it is not in this table; check it on the final scene alone.

`ACTIVE`/`EMPTY_DELTA_PX` are absolute ink-pixel counts and therefore scale with cell
area: the portrait safe box is 918×1344 = 1,233,792px over 6 cells = 205,632 px/cell,
where `ACTIVE_DELTA_PX` 1200 is 0.583% of a cell. The landscape safe box is 1728×918
= 1,586,304px over 6 cells = 264,384 px/cell; holding the same 0.583% gives 1542/386.

**`CADENCE_CEILING_S` 10.0 is a craft budget, not a measured threshold.**
`channel-baseline-analysis-2026-09-01.md` §7 lists both the 1.5–3s and 8–12s cadence
numbers as unbacked by channel data. Do not cite a finding from it as evidence of a
performance problem.

## 2026-09-02 — `scene_boundaries()` was attribute-order dependent

Separate latent bug, found while testing the above. The single regex required the
literal attribute order `data-composition-src` → `data-start` → `data-duration`.
`videos/pilling-vs-peeling/index.html` writes `data-start`/`data-duration` **first**,
so the scene list came back empty and the region-aware check silently degraded to
"treat the whole render as one scene" — the exact mode whose own warning text says
cross-cut false positives are possible.

Now matches the tag first and extracts each attribute independently. Across the repo
this recovers **8 scenes, all in `pilling-vs-peeling`** (142 → 150 detected): the bug
was latent everywhere and had only just started biting on the newest markup. Six
projects still report zero scenes — `retinal-clinical-dossier` and the four
`skincare-glossary-part-*` plus `skincare-ingredient-glossary` — and that is correct:
they contain zero `data-composition-src` occurrences and have no sub-composition
scenes to find.

## 2026-09-02 — the region check was manufacturing a false positive at most cuts

Found by a peer session eyeballing a single advisory finding on
`videos/pilling-vs-peeling` and asking why a run crossed a scene boundary that
per-scene windowing was supposed to prevent. It was right that the finding was
spurious, and right that the cause was systematic. The mechanism turned out to be
neither of its two candidates — `had_content` **is** reset per scene, and the
window is assembled after boundaries are applied. It was integer truncation:

```python
i0 = max(1, int(scene_start * REGION_FPS))       # 13.200 * 4 = 52.8 -> 52 -> t=13.00s
```

`int()` truncates, so whenever a scene start did not land exactly on the
1/`REGION_FPS` grid the window opened **one sample early** — on a frame still
showing the *previous* scene. That frame flipped `had_content` True, and the new
scene's legitimately-empty cell then read as "content, then empty."

**Scale of it.** 711 of 936 `data-start` values across `videos/*` (**76 %**) are
off the 4 fps grid, so this fired at roughly three boundaries in four. Confirmed
on `pilling-vs-peeling` scene 06 (starts 13.200 s): the leading frame at t=13.00 s
is still scene 05 and carried 27.1 % ink in the flagged cell.

**Fix:** `math.ceil` on both bounds, giving half-open `[start, end)` frame
semantics so a window holds only frames whose timestamp is actually inside the
scene.

**Measured effect** — false positives removed, real findings kept:

| Project | Before | After |
|---|---|---|
| `ectoin-survival-molecule` (1920×1080) | 10 content-voids | **3**, all within-scene |
| `pilling-vs-peeling` (1080×1920) | the cross-cut finding at t=13.00–15.75 | **gone**; one unrelated within-scene finding remains |

So roughly 70 % of this check's output was an artefact of its own windowing. A
gate that cries wolf at three of four cuts trains its reader to ignore it, which
is worse than not shipping it — worth knowing before trusting any historical
"N content-voids" number produced by this script before today.

**Note on per-project copies.** `videos/pilling-vs-peeling/scripts/`'s own copy had
already been fixed independently for the *attribute-order* bug, so that project's
published scene counts were never degraded. Per the copy-inheritance warning
above: check the copy in front of you, not this file, before trusting or
distrusting a specific project's past results.

## 2026-09-02 (later) — ink presence was the wrong primitive for animated alpha

A third false-positive class, distinct from the `ceil()` windowing one above and
found the same way — a peer session measuring the one advisory finding that
survived that fix, and asking what was actually moving in the cell.

Nothing was leaving. The cell held cards whose background animates between
`rgba(247,245,240,0.06)` at rest and `rgba(...,0.18)` while each card's tip is
demonstrated. `INK_THRESHOLD` sits *between* those two alphas, so the card's
entire area enters and leaves the ink mask on a highlight-then-release cycle
while the element is fully present throughout. Measured on a synthetic card:

```
a=0.06 (at rest)      ink  26,576   edges 6,116
a=0.18 (highlighted)  ink 111,044   edges 6,116     <- 4.2x ink swing, edges flat
genuinely removed     ink       0   edges     0
```

**Binary ink presence cannot distinguish "dimmed" from "gone", and no amount of
hysteresis on a single ink threshold fixes that** — the swing is 4.2×, far larger
than any sane enter/exit gap. Borders and glyph strokes, however, survive an
alpha change untouched: only real removal collapses edge density too.

**Fix:** a cell now counts as empty only when its ink delta is low **and** its
edge density has fallen to ≤ `EDGE_EMPTY_FRACTION` (0.25) of that scene's own
90th-percentile edge peak. New constants `EDGE_THRESHOLD`, `EDGE_EMPTY_FRACTION`.

This will matter to any project that dims, highlights, or pulls focus — a
focus-pull from opacity 1 → 0.45 is the same shape as the card highlight.

**Measured, and validated in both directions:**

| Project | Before | After |
|---|---|---|
| `pilling-vs-peeling` | 1 (the highlight/dim cell) | **0** |
| `ectoin-survival-molecule` | 3 (vertical-centring) | **0** |
| Synthetic control: structured block genuinely removed at t=5.0 of 12 s | — | **still flagged**, t=4.75–11.75, correct cells |

The control matters more than the two zeroes. A checker that reports nothing is
exactly as suspect as one that cries wolf, and this file's own guidance is to
re-verify a scanner immediately after fixing the defect it was built to catch.
Re-run the control (a block that truly disappears mid-scene) after any future
change to these thresholds.

## 2026-09-02 (later still) — the summary line asserted more than it tested

`check-static-hold.py` used to end with:

```
Overall: clean (whole-frame and region-aware checks both clean).
```

That reads as a verdict on the **render**, and it is not. A region that stays
frozen while still *carrying* content is invisible to both passes: the
whole-frame diff stays alive on any other moving element, and the region pass
only looks for content-then-**empty**, which never happens. So a render with an
entirely dead scene printed "Overall: clean".

Confirmed on a synthetic — a populated left region frozen for all 12 s beside a
right region stepping every second — and independently on a peer session's real
known-broken repro, which also came back clean. Neither is a regression from the
edge-density work; the old version missed this identically. **The logic was
right; the sentence was wrong.**

The summary now names its own scope, and states the gap:

```
Covered: near-blank frames, frozen whole frames, and regions that carry content
and then go empty.
NOT covered: a region that stays FROZEN while still carrying content. Neither
pass can see it -- verify a suspect scene by extracting its own frames and
diffing them, not by trusting this summary.

Result: no findings in the two checks above.
```

## Controls — `test-static-hold-controls.py`

```bash
python3 catalog/tooling/test-static-hold-controls.py
```

Run it after **any** change to this checker's thresholds or primitives. Two
fixtures, built with ffmpeg, no project assets needed:

- **Positive** — a structured block genuinely removed mid-clip → **must be
  flagged**. Guards against a "fix" that quietly blinds the check. This is the
  one that matters: after the edge-density change two real projects both went to
  zero findings, which is indistinguishable from having broken the tool until
  something still fires.
- **Negative** — a populated region frozen for the whole clip beside an
  animating one (mode 4) → **must stay silent**, because that is a documented
  coverage boundary, not a bug in this pass.

If anyone later implements a frozen-region byte-identity scan, the negative
control is the ready-made case that must flip from silent to flagged, and its
assertion should be inverted deliberately at that point rather than deleted.

## 2026-09-02 (later still) — the safe-area gate's background estimator broke on a busy frame

`ink_mask()` took the page background as the **whole-frame modal luma**. That holds
while the page ground is the majority of the canvas, and fails the moment it is
not. On a landscape scene with two ~45%-of-frame panels, the modal became a
*panel* colour:

```
whole-frame modal luma : 151   <- what the checker used
outer 4px ring median  : 243   <- the actual page ground
```

Every margin then differed from "background" by 92 luma, so **all four reserved
zones reported 100% ink** — 103,680 px in a 96×1080 left zone is exactly the whole
zone. 136 frames flagged, nothing actually in a reserved zone.

On a **hard gate** a false positive is worse than a miss: it blocks a clean render
and, if waved through once, teaches the reader to wave through the next one.

**Fix:** derive the ground from the **median of the outer 4px border ring**. That
is the right reference precisely *because* reserved margins exist — the extreme
edge of the canvas is page ground by construction in any composition that
respects them. Median rather than modal so a few stray edge pixels cannot move it.

Verified in three directions, not just the one that was failing:

| Check | Result |
|---|---|
| `pilling-vs-peeling` portrait regression | unchanged — 84 frames, no findings |
| Synthetic positive (ink in a reserved zone) | still **FAILS** correctly |
| Synthetic negative (clean landscape) | still passes |
| The busy landscape render that triggered it | **no findings**, 1,361 frames |

This is the fourth distinct defect found in this checker family in one day
(attribute-order parsing, `int()` window truncation, ink-vs-alpha primitive, and
now the background estimator). The pattern in all four: **the measurement's own
assumptions were never checked against a case that violated them.** Each held for
the portrait Shorts it was written against and broke on the first composition
with different geometry or a different colour distribution.

---

## check-cadence.py

**What it measures — two quantities, not a verdict.** Per scene, the *longest
quiet run*: consecutive 8 fps steps carrying no perceptible, localised change.
Whole video, the *active-step share*: the fraction of steps that do carry one.
A step counts as a beat only if it clears **both** `MEAN_ACTIVE` (mean |ΔLuma|
≥ 1.0) **and** `MIN_MAXPIX` (per-pixel max ≥ 40). The second half is not a
refinement, it is the check: an h264 keyframe refresh shifts the whole frame a
few luma levels at once, which reads as a *large* mean with a *tiny* per-pixel
max. `videos/pilling-vs-peeling`'s round-3 record credited a scene with "8%
active steps" that were two such artifacts and no animation at all. Steps whose
mean exceeds `CANVAS_CUT_DELTA` (60) are dropped as scene cuts rather than
counted as motion, and each scene's measuring window opens `BOUNDARY_SKIP_S`
(0.13 s — one 8 fps sample plus a rounding margin) after its `data-start`,
because the first step inside a scene differences against the *last frame of
the previous one*.

**Thresholds, and what they are worth.** `QUIET_CEILING_S` is 1.6 s, raised to
6.0 s by `--longform` (alias `--landscape`). Both are **craft budgets, not
measured thresholds** — `channel-baseline-analysis-2026-09-01.md` §7 lists the
1.5–3 s and 8–12 s cadence targets as unbacked by channel data. Never cite a
finding from this script as evidence of a performance problem.

**What it cannot see.** Two things, and the script now prints both in its own
summary rather than leaving them in a docstring nobody re-reads: (1) a region
that stays **frozen while still carrying content** — a beat anywhere else in
the frame keeps this scan alive, the same mode-4 blind spot documented above
for `check-static-hold.py`; (2) **structural sameness** — 29 scenes with one
enter/wash/hold shape and one entrance ease measure as "paced" here. That
second question belongs to `continuity-audit.py`, not to this script.

**Exit code: always 0.** Advisory, like every `check-*.py` in this directory
except `check-safe-area.py`. It reports; it does not gate.

**Field contract.** `python3 check-cadence.py <project_root> [render_path]
[--longform|--landscape]`. With no render path it takes the most recently
modified `renders/*.mp4`. Scene boundaries come from the sibling
`check-static-hold.py`'s `scene_boundaries()`, so the two scripts cannot
disagree about where the scenes are.

**Provenance, and the drift fixed on harvest.** Written in
`videos/pilling-vs-peeling` (round 4, 2026-09-01); copied verbatim into
`videos/ectoin-survival-molecule`, which added the `--longform` ceiling for the
channel's first 16:9 piece; harvested here 2026-09-02. The inherited docstring
opened *"Confirmed on this project… 06-fix-pilling's three demo beats"* — and
`06-fix-pilling` is a scene that exists only in `pilling-vs-peeling`. Read
inside the Ectoin copy, that sentence pointed at a file which was not there:
the same shape as the caption-band history above, a comment travelling with the
code and quietly ceasing to be true. Six changes on harvest: (1) provenance
rewritten so every "confirmed on" names its own project and nothing says "this
project"; (2) the summary line scoped, per *"the summary line asserted more
than it tested"* above; (3) `--landscape` accepted as an alias of `--longform`,
matching how the other two scripts here spell their landscape flag; (4) the
bare `s + 0.13` named `BOUNDARY_SKIP_S`, with the reason; (5) exit 0 kept and
documented as deliberate; (6) `test-cadence-controls.py` added.

**Behaviour verified unchanged by the harvest.** The catalog copy and
`videos/ectoin-survival-molecule/scripts/check-cadence.py` were both run
against `renders/ectoin-survival-molecule.mp4`: identical whole-video count
(344/2703) and an identical 29-row per-scene table. The only diff is the new
summary text.

**A recorded number that did not reproduce — worth knowing before citing it.**
`videos/ectoin-survival-molecule/DELIVERY.md:53-58` records the final render at
**14.8 %** active steps. Measured 2026-09-02 with both copies of this script,
on both `renders/ectoin-survival-molecule.mp4` (the publish candidate) and
`renders/ectoin-full.mp4` (the same picture, pre-master): **12.7 %**
(344/2703). The longest quiet run is **6.00 s on scene 28**, not 6.15 s on
scene 12. The picture was re-rendered at 14:14 and DELIVERY.md written at
14:26, so 14.8 % appears to describe an earlier round rather than the file that
shipped. Two things follow: re-run the scan against the artefact you are about
to publish, not the one you measured while authoring — and note that scene 28's
6.00 s run clears the 6.0 s long-form ceiling by *exactly zero* margin.

## continuity-audit.py

**What it measures.** Four source-structural counts — pre-render gate item 14 —
and no pixels at all:

| Count | How | Exact or heuristic |
|---|---|---|
| Boundaries by type, and whether the ground changes across each | authored overlap and/or a root-timeline tween targeting `#scene-<id>`, classified by animated props (opacity-only → crossfade, `x`/`y` → push, `scale` → zoom, `filter` → blur); ground = the **last** `#root { … background … }` block in each scene file, with `var(--x)` resolved from that file's own declaration | exact |
| Entrance-signature shares | every real `tl.to` / `tl.from` / `tl.fromTo` as (animated props + **effective** ease — explicit *or* inherited from the timeline's `defaults:{ease}`); top-3 signatures, top-3 effective eases, fade-and-slide share | exact |
| Rebuilt actors, merged scenes | consecutive scene files sharing a normalised SVG shape — geometry kept (`cx cy r d x y width height viewBox stroke-width`), styling dropped (**H3**); scenes with ≥ 2 `.phase` divs (**H3b**) | heuristic |
| Camera moves | tweens whose target matches `/(world\|zoom\|stage\|cam\|frame)/i` with props ∩ `{scale,x,y,xPercent,yPercent}` (**H4**); CSS Ken Burns (`transform: scale(calc(1 + var(--progress`) counted **separately** as *plate* motion, because it moves a plate inside a frame, not the frame | heuristic |

**Why source-level is legitimate here when source-level cadence is not.**
Cadence has to be measured on rendered pixels because a tween can fire
correctly and still be invisible. Variety is the opposite kind of property: it
*is* a property of the source — two tweens with the same props and the same
effective ease are the same entrance whatever they render to.

**The tween scanner is paren-balanced and multi-line by construction.**
Measured on the calibration project: 196 real tweens, of which **47 (24 %) do
not close on the line they open on**. A line-oriented regex does not half-work
on that input; it silently returns a smaller, tidier population and a share
computed over the wrong denominator. `tl.to({}, …)` full-span anchors (29 of
them, one per scene) are skipped, `tl.set` is not a tween, and a `gsap.to(…)`
outside the timeline is counted separately and named — it is not seek-safe
either.

**What it cannot see.** Anything about how the piece looks. It cannot tell a
good transition from a bad one, cannot see a diagram rebuilt with different
numbers (H3 compares geometry), cannot see a camera wrapper named outside its
regex (H4), and has no opinion on whether a given hard cut was right. The
verdict block says so in the output; it never prints "clean".

**Exit codes.** 0 by default. `--gate` exits **2 on one finding only** — a
plain opacity-only crossfade across a ground change, the documented
muddy-midpoint defect. Everything above it is a craft reading, not a rule, and
gating on a craft reading is how a gate gets waved through.

**Calibrated on `videos/ectoin-survival-molecule`** (2026-09-02) — the piece
this gate was written for, and one that passed every other gate the skill had:

| | Measured |
|---|---|
| Boundaries | **28, all hard cuts**, 0 transitions |
| Ground changes | **17 of 28** — all 17 cut; the other **11 are paper→paper** and could have carried a same-ground transition even under the old rule |
| Real tweens | **196** across 29 scene files (47 multi-line; 29 anchors skipped) |
| Top signature (props + ease) | `{opacity,y}` + `power3.out` — **26.0 %**; next `{opacity}` + `power3.out`, 20.9 % |
| Top **effective ease** | `power3.out` **128/196 = 65.3 %** — only **8 explicit**, 120 inherited, from `defaults:{ease}` declared by **29 of 29** timelines |
| Fade-and-slide (opacity + x\|y) | 69 (35.2 %) |
| Rebuilt-actor pairs | **1** — `09-exclusion → 10-messier`, two circles identical in normalised geometry |
| Merged scenes / camera moves / Ken Burns | 0 / 0 / 0 |
| `--gate` | pass — there is no crossfade across a ground change, because there is no crossfade at all |

**Read the two "65 %"s carefully; they are different numbers.** The
inherited-ease share is 65.3 %, and it is the one worth acting on: 120 of 196
tweens never name an ease, so counting eases by explicit hits alone reports
**8** and misses the template entirely. The top (props + ease) *signature* is
26.0 %. A brief that says "top signature ≈ 65 %" has conflated the two — this
tool prints both, labelled, for exactly that reason.

**Field contract.** `python3 continuity-audit.py <project_root> [--gate]
[--verbose]`. Reads `index.html` and the scene files it names; no render, no
ffmpeg, no dependency outside the standard library. Scene parsing is
attribute-order-independent — the same fix `check-static-hold.py` needed above.

## Controls — `test-cadence-controls.py`, `test-continuity-controls.py`

```bash
python3 catalog/tooling/test-cadence-controls.py
python3 catalog/tooling/test-continuity-controls.py
```

Same discipline as `test-static-hold-controls.py` above, for the same reason: a
checker broken into silence and a clean project produce the same output.

`test-cadence-controls.py` — two ffmpeg fixtures, no project assets:

- **Positive** — a 200×200 high-contrast block jumping every 0.5 s for 2 s then
  static for 4 s → must report a quiet run over the 1.6 s ceiling **and** more
  than zero active steps. Two deliberately opposed assertions: a tool tuned
  until nothing registers would pass the first and fail the second.
- **Negative** — the whole frame stepping +6 luma once a second with nothing
  moving, a codec-refresh look-alike (mean ≈ 5, maxpix < 40) → must count
  **exactly 0** active steps. This is the assertion that fails first if the
  beat test is ever "simplified" down to the mean.
- **Alias** — `--landscape` and `--longform` must produce identical output at
  the 6.0 s ceiling, so the same 4 s hold is a finding under the shorts ceiling
  and not under the long-form one.

`test-continuity-controls.py` — three synthetic projects written into a
tempdir; no ffmpeg, no assets:

- **slides** — 3 contiguous scenes, alternating grounds, every tween
  `{opacity,y}` inheriting one `defaults:{ease}`, the same circle redrawn in
  scenes 2 and 3 → 2 cuts, 0 transitions, one signature at **100 %**, 1 rebuilt
  pair, 0 camera moves. The failure the tool exists to name.
- **film** — the same three beats built for continuity: authored overlaps with
  root push and blur tweens, six different idioms, a `.stage` drift, no shared
  geometry → 0 cuts, 2 transitions (push then blur), top signature < 50 %, 0
  pairs, ≥ 1 camera move. This is the control that catches a scanner blinded
  into reporting "slides" for everything — the one that matters most here, the
  way the positive control is the one that matters for `check-static-hold.py`.
- **violation** — an opacity-only root tween across a ground change → `--gate`
  must exit **2**, and the plain run must still exit 0.

All three control scripts in this directory pass as of 2026-09-02.

## 2026-09-02 (later still) — the safe-area gate's background estimator broke on a TRANSITION frame

Same estimator, second failure, opposite trigger — and worth reading next to the
busy-frame entry above, because the fix for that one is what set this one up.

The outer-border-ring median assumes the frame has **one** page ground. A
transition frame legitimately has two: the outgoing scene and the incoming one
are both on screen. The ring goes bimodal, the median lands on whichever ground
holds more of it, and the other ground then differs from the reference
everywhere it appears — so a reserved zone that contains nothing but flat scene
background reports as 100% ink.

Measured on a real 29-scene 1920x1080 render whose 28 boundaries all carry a
clip-path wipe:

```
gate says: top zone, worst at t=73.50s, 103680px masked in-zone  (= 54 x 1920, the WHOLE band)
actual   : top zone luma min 19, max 19, std 0.0 — a flat ground, zero variation
           rows in 0-53 containing any horizontal edge: 0
```

70 frames flagged, every one inside a wipe window, nothing out of place in any
of them. On a hard gate that is the expensive kind of wrong: it blocks a clean
render, and the wave-through it earns is what lets a real one through later.

**Fix: cluster the ring instead of averaging it.** Any luma level holding at
least `GROUND_MIN_SHARE` (0.15) of the border ring is a page ground in its own
right, up to `MAX_GROUNDS` (3), and a pixel counts as ink only when it differs
from **every** ground present. A single-ground frame yields exactly one cluster
and behaves precisely as before, so nothing about the existing pass changes.

**Second half of the fix: scope the antialiasing run-filter to the zone.**
`MIN_EDGE_RUN` exists to drop a resampling fringe — a real edge puts several
masked pixels in a row, antialiasing puts one. It was computed across the FULL
FRAME, which quietly defeats it at a zone boundary: a row crossing a scene seam
carries one masked pixel inside a 96px rail, but that same row has real content
elsewhere in the 1920px frame, so the row passes and the lone fringe pixel
survives into the zone. The clustering fix alone took the wipe render from 70
flagged frames to 8, and those 8 were exactly this — worst case 1184px inside a
103680px rail, about one pixel per row. Applying the run test within each zone
removes them and touches nothing bounded.

**Validated in both directions, on three renders of the same composition:**

| render | expected | result |
|---|---|---|
| baseline, 28 hard cuts | clean before the fix, must stay clean | 0 findings |
| translating push, genuinely dragged text through the zones | **must still FAIL** | 35 frames, smallest real finding 12636px |
| clip-path wipe, clean by independent measurement | should now pass | 0 findings |

The middle row is the one that matters. A gate that has just been "fixed" is
exactly as suspect as a scanner reporting nothing, and the only thing that
makes the two clean rows evidence is that the dirty one still fires.

A first attempt fixed the symptom instead and is worth recording as a wrong
turn: excluding masked rows/columns that span the band edge-to-edge. That works
for the bands parallel to the seam and silently fails for the rails crossing it,
where a flat ground is bounded by the seam and so looks exactly like content.
The `two-ground` control below is what caught it — the fix was written, looked
right, and the control failed it in one run.

## Controls — `test-safe-area-controls.py`

```bash
python3 catalog/tooling/test-safe-area-controls.py
```

Run after **any** change to the ink mask, the background estimator, or the
thresholds. This is the only hard gate in this directory, so it carries two
NEGATIVE controls, not one — a gate that only proves it can fail is not
validated.

- **positive** — text-like glyph boxes inside the bottom reserved zone → **must
  FAIL**. The thing the gate exists for; if it stops firing, every "no findings"
  it prints is worthless.
- **solid-block** — one bounded solid rectangle in the bottom zone → **must
  FAIL**. Guards the estimator against over-suppressing. A structure- or
  edge-density test would wave this through, since a solid block has no internal
  detail, which is exactly why the fix keys on ground membership rather than on
  how much detail a region contains.
- **two-ground** — two flat grounds meeting at a straight seam, as a wipe or a
  cut boundary produces → **must PASS**. The regression above.

Fixtures are `drawbox` only: this repo's ffmpeg is built without libfreetype, so
`drawtext` is unavailable. A run of glyph-sized boxes is what the gate sees in a
line of text anyway — many partially-masked rows.

All four control scripts in this directory pass as of 2026-09-02.
