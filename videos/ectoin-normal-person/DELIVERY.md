# DELIVERY — Ectoin: Explained by SoulHabit, and Then by a Normal Person

**Slug** `ectoin-normal-person` · **Branch** `claude/faceless-video-feedback-6c6c24`
**Format** 1920×1080, 30fps, **4:57.02** (cold-open revision; was 5:59.01) · **Engine** `hyperframes@0.8.22`

## Status — COMPLETE (cold-open revision, 2026-09-03)

| Deliverable | State |
|---|---|
| Render | **`renders/ectoin-normal-person.mp4`** — 4:57.02, 1920×1080, h264/AAC, 75.3 MB, 8911 frames |
| Master | **PASS** — −14.7 LUFS integrated, −2.2 dBTP, measured on the decoded shipped file |
| Safe-area (hard gate) | **PASS** — 0 findings across 1188 sampled frames |
| Static-hold (whole-frame) | **PASS** — 0 findings, 594 frames sampled |
| Static-hold (region-aware) | 4 findings, all confirmed benign on extracted frames (empty grid cells with no content in that stretch, or the by-design endscreen right-third reserve) |
| Cadence | 13.7% whole-video active share (>= the shipped 13.0% baseline); 2 scenes over the 6.0s quiet ceiling, one pre-existing/out of scope (`05-skin`), one 0.25s over (`12-bottle`, advisory) |
| Continuity `--gate` | **PASS** — 16/16 boundaries transitioned, 0 hard cuts, 0 crossfade-across-ground violations, top entrance signature 15.5%, 0 timelines with `defaults:{ease}`, 5 merged scenes, 0 rebuilt-actor pairs, 11 camera moves |
| Captions | `captions/ectoin-normal-person.srt` + `.vtt`, 88 cues, none under 1.10s |
| Thumbnail | `assets/thumbnail/final.png`, 1280×720, grid-checked at 120×67 — rebuilt this revision around the new hook |
| Storyboard | `STORYBOARD.md`, generated from real `data-start` values |
| Motion sidecar | `index.motion.json`, 22 assertions, all passing |
| Catalog | unchanged this revision — see the shipped-cut catalog note below |

`renders/*.raw.mp4` is the pre-master intermediate and is gitignored. **The
publish candidate is `ectoin-normal-person.mp4`** — the one without `.raw`.

## Revision — cold-open, 2026-09-03

Operator feedback rewrote the opening: the "11% bottle → it's a blend → turn
the bottle around" reveal moves to frame 0; the bacteria-origin material
compresses to one narrated raisin beat; the section closes on "Skincare
borrowed the molecule. Marketing borrowed the drama." Full account in
`SCRIPT.md` §Changes and `BRIEF.md` §Cold-open revision.

**What changed:** `01-hook`, `02-industry`, `03-cell` retired (12 turns);
two new merged units `01-bottle` / `02-origin` open the video (7 turns, one
reused verbatim: t002/t003); `12-bottle` drops its own repeat of the same
reveal (t051-t054, 4 turns) — keeps who-it's-for and the INCI-list payoff;
`18-endscreen` rebuilt to bookend the bottle instead of the retired brine
hook. Runtime **5:59.01 → 4:57.02**. Turn count 70 → 58.

**Real bugs found during this revision's own `check` pass (not by eye):**
1. `01-bottle` reused `12-bottle`'s bare `#pc`/`#in-10` ids — every
   sub-composition renders into the same document at once, so this made the
   motion sidecar's selectors ambiguous (`motion_selector_ambiguous`, 2
   errors). Fixed by prefixing `01-bottle`'s actor ids (`ob-*`).
2. `01-bottle`'s own hand-authored ambient `#world` drift fought its phase-b
   camera fly on the same x/y properties (`overlapping_gsap_tweens`) — the
   generator already appends an ambient tween to `#drift` on every unit, so
   the custom one was both redundant and the actual cause of ~150-160px of
   real (not bounding-box-false-positive) content overflow measured on the
   plate panel and the INCI list. Removed the custom drift and the 1.28
   baseline camera zoom it was paired with (an "extreme close-up" tried via
   `#world` scale, which pushed the two-column grid off-canvas at rest);
   close framing now comes from layout, not a camera trick.
3. `12-bottle`'s trimmed phase-a states/pairs chips were never cleared —
   their exit tween was tied to the now-retired t051 turn — so they stayed
   on screen through the INCI reveal (`panel_out_of_canvas` on `#pr2`/`#pr4`/
   `#bpl`). Added an explicit clear before phase D.
4. The illustrative-label disclosure tag (new this revision, see `[K-2a]`
   note below) measured off-canvas during both units' own camera moves when
   authored as a loose sibling of `.bottle`; anchoring it as a child of
   `.bottle` (inheriting the same centred, proven-safe positioning) fixed it
   in both places.

**`[K-2a]` note:** the bottle's "11%" is an authored illustrative prop, not a
real product — `K-2a` bars an unsourced quantity from rendering as
measurement whatever sits beside it, so it ships tagged
`[Authored, illustrative — not a claim]` via a muted `ILLUSTRATIVE LABEL`
caption (`--ink-2`, mono, never the accent, never citation typography) on
the bottle itself, in both `01-bottle` and `12-bottle`.

**Two more real bugs found only by extracting frames — `check` cannot see
either class:**
5. `02-origin`'s `stage()` call omitted `ground="ink"` (defaulted to
   `paper`) while every dialogue line was authored `ink=True`
   (`color:var(--paper)`) for contrast against a dark ground. Result: paper
   text on a paper background — every spoken line in the unit's first two
   phases was **invisible**, confirmed at full 1920×1080 resolution (not a
   downscaled screenshot artifact). The citation pill still read correctly
   because `.cite.on-ink` sets its own dark background unconditionally,
   which is exactly why it looked fine in isolation while the plain text
   next to it was gone. `check`'s Contrast pass did not flag this. Fixed:
   added `ground="ink"`.
6. The two plate-collapse fixes below (item 3 in the earlier list) first
   used `height`/`minHeight`/`marginTop` to shrink the empty panel — `check`
   correctly rejected this as `gsap_non_transform_motion` (layout-reflow
   properties snap to integer device pixels under the seek-by-frame capture
   engine). Switched to `opacity`+`scaleY` (transform-only).

**npm gotcha, not a content bug, worth recording anyway:** `package.json`
names a script literally `postrender`, so `npm run render` silently
auto-triggers it as an npm lifecycle hook — and the first time this run hit
that, `postrender`'s gate chain scanned the **stale, unmastered**
`ectoin-normal-person.mp4` (still the shipped 5:59 file, since mastering is
a separate step run after render). All of that gate output was meaningless.
Caught by checking the file's mtime before trusting it. From here on,
`render` was invoked directly via `npx hyperframes render` rather than
`npm run render`, and `npm run postrender` was called explicitly and only
after `npm run master`.

**Gates on this revision's render — see the Status table above.** All pass:
safe-area 0/1188, static-hold whole-frame 0/594, continuity `--gate` pass,
cadence 13.7% (>= the 13.0% shipped baseline). Full per-rule detail in
`00-decision-ledger.md` §S7.

## Verification

**Historical record of the original 5:59.01 ship** — superseded by the
Status table above for this revision's own gate numbers.

`npx hyperframes@0.8.22 check --samples 60` — **0 errors** across lint, layout,
motion and contrast. One lint warning remains: `04-protein.html` is 408 lines,
which is a five-phase merged unit and is deliberate.

### Continuity audit — the gate this build exists to pass

`python3 catalog/tooling/continuity-audit.py videos/ectoin-normal-person`

| Count | `ectoin-survival-molecule` | This build |
|---|---|---|
| Boundaries carried by a transition | — | **17/17**, 0 hard cuts |
| Top entrance signature | 26.0% | **15.6%** |
| Top *effective* ease | **65.3%** | **16.2%** |
| Timelines declaring `defaults:{ease}` | 29 of 29 | **0 of 18** |
| Merged multi-phase scenes | **0** | **4** |
| Rebuilt-actor pairs | 1 | **0** |
| Camera moves | **0** | **12** |

The predecessor passed every per-frame gate it had and still read as an animated
presentation. The single change that moves the ease number is deleting
`defaults: { ease: "power3.out" }` from the `scene()` emitter — a grep for
`ease:` on that project returns 8 hits and reports variety while 128 tweens
actually carry one signature.

### Render-level gates — all run against the shipped file

| gate | result |
|---|---|
| `check --samples 60` | **0 errors** — lint, runtime, layout, motion, contrast |
| Dead sets (source) | **0 across 18 units** — `check-dead-sets.py`, wired into `npm run check` |
| Safe-area (HARD GATE) | **PASS — 0 of 1436 frames** with ink in a reserved zone |
| Static-hold, whole-frame | **no findings**, 718 frames, 10.0s ceiling |
| Static-hold, region-aware | 5 findings, **all verified as non-defects** (below) |
| Cadence | **13.0%** whole-video; 5 of 18 scenes over the 6.0s ceiling, all 6.25–7.25s |
| Continuity audit | 17/17 transitions · ease **16.2%** · 4 merged · 12 camera moves · 0 rebuilt actors |
| Transition midpoints | 17 of 17 extracted and scored; **none muddy** |
| Master | **PASS** on the decoded shipped file |

**Safe-area took three attempts** and the middle one is the lesson:

| build | flagged frames |
|---|---|
| camera outside the safe padding | **1205** |
| `overflow:hidden` on the moving `.world` | still failing, 22 of 27 sampled |
| static `.clipbox` ancestor | **0 of 1436** |

`overflow:hidden` clips an element's *children*, not itself, so scaling
`.world` scaled its own clip region along with the content it was meant to
contain. The clip has to live on an ancestor that never transforms. A 5-frame
spot check on the failing build came back clean and was luck — the full sweep
showed 22 of 27 still failing. **Five frames is not a sample.**

Run safe-area streaming (`/tmp/sa_stream.py`, which imports the shared
script's own scoring functions and only swaps the frame source). The shared
script extracts all 1436 PNGs to a temp dir first and gets OOM-killed when
another session is rendering.

`CAPTION_BAND_EXCLUDE = False` is **correct for this project** — it ships
sidecar captions, not burned-in, and `index.html` has zero caption elements.
That constant has been wrongly inherited three times in this repo's history.

### The five region-aware findings, each verified

Three in scene 11 (`11-twelve`, t=222.5–237.5, top row) are **false
positives**: the cells carry 8134 / 2884 / 641 ink px and hold that through
t=226, 230 and 235. The heuristic fires because the 12 tiles animate in with a
high edge-density peak and the held state reads as "fallen" against it.

Two at t=353.5–358.75 in the right-hand cells are **by design**: that is the
`--endscreen-right: 640px` reserve, cleared for YouTube's own overlays. Zero
ink there is the requirement, not a defect. The left column carries 46,652 px.

### Cadence — 7.5% to 13.1%, and how

| render | share | worst hold | over ceiling |
|---|---|---|---|
| 3 baseline | 7.5% | 29.1s | 13 of 18 |
| 4 beats sized by eye | 8.0% | 20.9s | 13 |
| 5 panel plates, computed | 9.1% | 13.4s | 11 |
| 6 bands in 12 measured windows | 11.5% | 9.1s | 7 |
| 7 bands ground-scoped | 12.5% | 9.1s | 5 |
| 8 shell fill on t020 | 12.7% | 7.25s | 5 |
| 9 band idioms + 03-cell fix | 13.1% | 7.25s | 5 |
| **10 two wipes composed at t=0** | **13.0%** | **7.25s** | **5** |

13.0% is above this channel's shipped 9:16 comparator (11.7%) and above the
predecessor's panel-scale rebuild (12.7%) — in a 6-minute landscape piece, where
the same beat covers three times the wall-clock a Short's does.

**The 0.1pp drop from render 9 is the price of the two wipe fixes, and it is the
right trade.** Composing a scene at `t=0` deletes its entrance tweens, so
`10-notprove` went 22% -> 18% of steps carrying a beat. Nothing regressed where
it matters: **no scene's longest quiet run got worse**, the set of five scenes
over the ceiling is unchanged, and the deleted entrances were `--mist` cards on
`--paper` — a ~5-luma step that was never carrying a beat in the first place.
Four beats of credit for a metric, traded for two boundaries that no longer
reveal an empty scene.

**Every beat sized by eye contributed nothing; every beat sized by the
arithmetic worked.** `scripts/beat_budget.py` computes
`(area_fraction × luma_delta) / (duration × 8)` before anything is authored:

    4 mist chips on paper, 380x64     1.2% x  10 luma  ->  0.04/step
    6 ring squares 26x26              0.2% x  25       ->  0.01/step
    22 strands, stroke-width          4.0% x 110       ->  0.69/step
    lower-third band 1728x136        11.3% x 215       ->  5.53/step

`--mist` on `--paper` is a **10-luma step**. It reads as a real card to a
viewer and is nothing to the metric.

**The band was then wrong in the same way `--coral` had been**: it filled with
`--ink` unconditionally, a 0-luma step on the five ink-ground units. The
measurement named them without ambiguity — `14-notnew` and `17-dignity` were
the only two bands that moved their scene's quiet run by 0.00s. Ground-scoping
the fill took them to 3.75s and 4.12s. Twice a colour was chosen without
reference to what sits behind it; *which colour* and *on what ground* are one
decision that kept getting made as two.

### The 04-protein outlier — FIXED

It was 9.12s and is now **6.62s**, in line with the rest. The dead stretch was
`t019` plus the whole of `t020` — and `t020` is the six-second line that
explains the actual mechanism, *"water remains organised without clinging
directly to the protein"*. Everything already in that window was word-scale:
the ring closing ranks is 18 squares of 26px, 0.2% of frame, **0.01/step**.

The shell is the only element in that scene large enough to carry a beat, and
thickening it *is* the line's content. Computed before authoring:

| | before | after |
|---|---|---|
| geometry | r190, stroke 46 | r160, stroke 120 |
| opacity | 0.30 | 0.78 |
| luma | 218 | 174 |
| frame area | 5.0% | 11.1% |

11.1% at mean delta ~58 over 0.65s = **1.24/step** against a 1.0 floor.

**A near-miss worth recording.** The first attempt at this fix targeted rel
13.7s — a window read from **render 5**, three renders stale. Render 7's real
window was rel 21.47s. Checking whether the existing band actually registered
there (it did: 6 beat steps, peaking at 16.47 mean|dLuma|) is what exposed the
stale number. A measurement decays the moment anything upstream of it changes;
re-read before repeating, including your own.

### Remaining holds — 5 scenes, all marginal

| scene | longest quiet run | window |
|---|---|---|
| `03-cell` | 7.25s | 28.00–35.12s |
| `13-kbeauty` | 7.25s | 307.75–314.88s |
| `05-skin` | 6.88s | 147.12–153.88s |
| `04-protein` | 6.62s | 83.88–90.38s |
| `12-bottle` | 6.25s | 241.88–248.00s |

All five are within 1.25s of a 6.0s craft ceiling, in a dialogue where someone
is speaking throughout. There is no longer an outlier.

### The cost of the bands — paid down

Adding twelve band beats had raised the top entrance-signature share from
**18.9% to 22.4%**, because all of them shared one signature (opacity +
`expo.out`). That was a real cost of a repeated mechanism, recorded rather than
buried, with the note that a further pass should vary the eases rather than add
a thirteenth band. This is that pass.

| | before | after |
|---|---|---|
| Top entrance signature | 22.4% | **16.0%** |
| Top effective ease | 23.0% | **16.6%** |
| `{scaleX} + expo.out` | 30 | **18** |
| Whole-video cadence | 12.7% | **13.1%** |

**The variation is keyed to something, not sprinkled on.** This piece attributes
speakers by TYPE only, with no persistent speaker zone, so the band is the one
chrome element that recurs often enough to carry the same distinction in motion:

- **SOULHABIT** — settles in *with* the reading direction and passes out the far
  side. `power2.out` / `circ.out` / `sine.out`, 0.62–0.70s.
- **JAY** — cuts in *against* it and snaps back the way it came. `expo.out` /
  `power4.out`, 0.40–0.46s.

Ease and duration rotate inside each register, so no two consecutive bands share
a variant. The register is **derived** at build time from `timing.walk()` — which
speaker actually holds the line the band sits under — never hand-assigned. I
assigned all fifteen by reading the band text first and was **wrong on four**:
`07-preference` and `14-notnew` read as JAY punchlines and are SOULHABIT;
`11-twelve` and `03-cell`'s second band read as SOULHABIT and are JAY.

Measured on the render, so the two idioms are physically different and not just
different strings in the source — the fill's leading edge in `03-cell`:

| | edge travel | at +0.05s |
|---|---|---|
| J band @17.0s | left edge 941 → 292 → 96, right pinned at 1823 | 67% wide — snaps |
| S band @39.7s | right edge 554 → 1004 → 1480 → 1820, left pinned at 96 | 24% wide — settles |

**Sizing came before authoring, again.** Every variant was checked against
`beat_budget.py` first. The model's `area x dLuma / (dur x 8)` assumes a LINEAR
ramp, which is the worst case for a wipe, so any out-family ease lands at or
above its modelled number. All fifteen clear the 1.0 floor by **3.0x–7.9x**, and
the render confirmed it: every per-scene quiet run is unchanged from render 8.
Widening a wipe from 0.55s to 0.70s cannot starve a beat here, and now that is a
computed statement rather than a hope.

**What is honest about the 22.4 -> 16.0 drop:** all of it comes from the ten
SOULHABIT bands' *text* fades moving off `none`. A 0.28s text fade is barely
perceptible either way, and on its own that change would be decoration. It earns
its place only because a linear text fade under a decelerating slab is the one
part of the S idiom that contradicted itself. What a viewer will actually notice
is the direction, the 0.40–0.70s duration spread, and the retract-versus-pass-
through exits — none of which move the signature number much.

### A caption that never appeared, found while varying the eases

`03-cell` carries two bands. Each stamped its own text with `tl.set()` — one at
`t=0`, one at `t=16.95`. HyperFrames renders by **seeking a paused timeline**, so
every `set` at or before `t` replays in declaration order on the way there.
Seeking to the second band's cue at **39.7s** replayed both, and the band
displayed the *16.95s* band's line.

One caption played twice; the other — *"ECTOIN IS THE ANSWER IT EVOLVED"* —
**never appeared in the video at all.** Verified on the shipped render before
changing anything: the frame at 67.29s reads `...TER LEAVES - PROTEINS
DESTABILISE`, 23 seconds after those words had already played. The `alt` class
was clobbered the same way, so the two bands were also the same colour.

A `tl.set(..., 0)` is **not "the initial value."** It is a value that any later
`set` on the same element silently overwrites, including for a cue that has not
fired yet. Every set now lands 0.06s before its own band, and the two emitters
that had drifted apart — pass 1 stamping at 0, pass 2 at its own offset — are one
function. Confirmed on render 9: the 39.7s band reads `ECTOIN IS THE ANSWER IT
EVOLVED` in moss, the 17.0s band `WATER LEAVES - PROTEINS DESTABILISE` in ink.

Nothing else caught it. `check` passed, the motion sidecar passed, and the
cadence gate scored the band as a beat because the slab moves whatever text it
happens to carry.

**`catalog/tooling/check-dead-sets.py`** is the gate for it, wired into
`npm run check`. Swept across all 25 projects in this repo with generated frames
(189 files): **0 findings** — so this was local to this piece's two-pass band
emitter, not a repo-wide pattern.

**The obvious implementation of that gate is the wrong one.** The first version
looked for sets declared out of time order, ran against the real defect, and
printed a clean `0` — those two sets *are* in ascending order. What matters is
the gap between a `set` and its use, not the order of the sets. That mistake is
now the control suite's `ordering` fixture, which the broken version flags and
the correct version passes.

### The 12-bottle wipe — FIXED

`12-bottle → 13-kbeauty` was the **thinnest frame in the piece**: 1.15% ink at
the wipe midpoint, **0.22x** the 5.35% median of ordinary frames and below the
10th percentile of every non-seam frame sampled.

**The mechanism, which is general.** A scene's `data-start` *is* the seam it is
wiped in on — `build_index.py` stamps the clip-path tween at the incoming
scene's own start. So a scene's `t=0` is the first frame of its own reveal, not
the first frame after it. `13-kbeauty` entered its kicker at `+0.00` and its two
cards at `+0.20` / `+0.34` against a **0.45s** wipe, so the wipe uncovered a
scene that had not arrived.

This boundary was the worst case because of what sits on each side: the LEFT
wipe covers the outgoing scene from the right, and `12-bottle`'s content-dense
half *is* its right column (the INCI list). So the wipe hid the only dense part
of the outgoing frame and revealed the empty part of the incoming one.

**The fix.** `#kk`, `#k1`, `#k2` are now `tl.set()` at `t=0` — composed before
the reveal begins. The three entrance tweens are gone and nothing replaces them,
because the reveal *is* the entrance. The scene keeps a real entrance regardless:
the camera pull (`scale 1.14 -> 1.0` over 1.90s) runs unclipped through the wipe
and past it, which a per-card tween could not — `#k1` is the left card, and a
LEFT wipe reveals it last, so its entrance would have played behind the clip.

| at the wipe midpoint | before | after |
|---|---|---|
| revealed region | two blank mist rectangles | `BACTERIA` / `DID` at 66px |
| whole-frame ink | 1.15%  (0.22x median) | **2.14%  (0.40x median)** |

**Measured on render 10, and this one is a PARTIAL win — stated as such.** The
ink nearly doubled and it is no longer an outlier against the other wipes, but
at 2.14% it is still under the 2.66% 10th percentile. The residual cause is the
`--mist` on `--paper` contrast below, not the timing: what the wipe now reveals
is composed, but the things it reveals are low-contrast panels, and the
outgoing half it leaves visible is the near-invisible mist bottle. Composing the
scene was the whole of the transition fix and it is done; the rest of this frame
is a contrast problem and will not move until that is addressed.

Verified as a true before/after: both frames captured with `hyperframes
snapshot --at 290.612` off the same build pipeline, rather than comparing a
snapshot against an ffmpeg-extracted render frame. `snapshots/wipe12_before/`
and `snapshots/wipe12/`.

**A measurement I got wrong first.** The obvious metric — ink in the *revealed
region* at the midpoint — reported **8 of 17** boundaries at or near zero and
would have sent me rewriting eight scenes. It is the wrong question: an empty
incoming region is normal and unavoidable for a wipe, because content enters on
the VO. `04-protein → 05-skin` scores 0.00 on it and looks completely fine — the
outgoing half is full and the incoming is calm paper. What the eye objects to is
a thin **composite** frame, so the metric is whole-frame ink at the midpoint
against the piece's own median. On that metric only three boundaries fall below
the 10th percentile, and the two worst are the two that look wrong.

### `09-miracle -> 10-notprove` — FIXED, same cause

The runner-up at **1.30%** (0.24x median), and the identical failure:
`10-notprove` revealed as empty paper while `09-miracle` held "Promising? /
Yes." on the left. Its kicker faded in over 0.26s and its three claim cards
staggered at `+0.25` / `+0.47` / `+0.69` against the same 0.45s wipe. Because a
LEFT wipe reveals from the right, `#x3` — the card that entered **last** — is the
one uncovered **first**.

Kicker and all three cards are now `tl.set()` at `t=0`. The midpoint now carries
`REPLACES TREATMENT` and half of `REVERSES AGEING`.

| at the wipe midpoint | before | after |
|---|---|---|
| whole-frame ink | 1.30%  (0.24x median) | **3.54%  (0.66x median)** |

Measured on render 10. This one clears the 10th percentile outright — it works
better than the 12-bottle fix because `10-notprove`'s cards carry `--t-frame`
ink text against an ink-ground outgoing scene, so both halves of the composite
frame have real contrast.

**Control:** `04-protein -> 05-skin`, deliberately untouched, measured
**2.50% before and 2.50% after** — confirming these two edits changed the two
boundaries they were meant to and nothing else.

**The stagger is not missed, and that is measurable rather than a matter of
taste.** Those are `--mist` cards on `--paper`, a ~5-luma step that carries no
beat at all; the scene's real beat is the STRIKE sequence at `+1.5`, which is
untouched. Three claims standing and then struck also reads better than three
arriving and then struck.

**Both scenes had the same shape on each side.** A LEFT wipe covers the outgoing
scene's right half, and in both cases that is where the outgoing scene's dense
content sits — `12-bottle`'s INCI list, `09-miracle`'s coral-struck "No." card.
The wipe hid the dense half and revealed the empty one. That pairing, not the
wipe itself, is what made these two the thinnest frames in the piece.

The third below the 10th percentile, `04-protein -> 05-skin` (2.50%, 0.47x), is
**not** the same thing and was deliberately left alone: it is a chapter UP wipe
with a full outgoing half and a calm paper incoming ground, and it reads
correctly. Fixing it would have been the metric leading the craft.

### Still open: `--mist` on `--paper`

Visible in the same frame and untouched by the wipe fix. The bottle panel, the
`.kx` cards and `.plate` are all `--mist` on `--paper` — the same ~10-luma
invisibility diagnosed in the chips, sitting in the *design* rather than in a
beat. It is why even a correctly composed frame measures thin here. Fixing it
changes how ~25s of the piece looks at rest, not just at a seam, so it is a
contrast pass of its own and not part of a transition fix.

### The remaining gates

```bash
python3 catalog/tooling/check-safe-area.py . renders/<file>.mp4 --landscape
```
```bash
python3 catalog/tooling/check-cadence.py . renders/<file>.mp4 --longform
```
```bash
python3 catalog/tooling/check-static-hold.py . renders/<file>.mp4 --landscape
```

`--landscape` / `--longform` are **not optional**. Without them the portrait
defaults give a silent false pass: `mask[1536:, :]` on a 1080-tall frame is an
empty numpy view, so the hard gate exits 0 having measured nothing.

`check-static-hold.py`'s `CAPTION_BAND_EXCLUDE` must stay **False** here — this
project ships sidecar captions, not burned-in ones. That constant has been
wrongly inherited from a sibling project three times in this repo's history.

## Three defects caught by measurement

1. **`--coral` is 3.00:1 on paper.** It is the channel accent and the obvious
   choice for JAY's speaker colour; every JAY line on a paper ground would have
   shipped under the contrast floor. Fixed with a ground-scoped pair —
   `--coral` on ink (5.60:1), `--coral-deep` on paper (4.60:1). Neither is a
   drop-in for the other. `scripts/contrast.py` holds the measurement.
2. **A duplicate `id="root"`.** `stage()` emitted a second one inside the one
   `scene()` opens, so the ink background never painted and five units —
   `01-hook`, `09-miracle`, `14-notnew`, `17-dignity`, `18-endscreen`, about 45
   seconds including **frame zero** — rendered paper text on a paper ground at
   1:1. `check`'s contrast pass reported it correctly and it was nearly
   dismissed as a mid-transition false positive. A snapshot settled it.
3. **33.5s of leading silence across 62 VO takes** (worst 1.93s), plus `t030`
   returned as 1.88s of pure digital silence. Scene timing is derived from
   measured audio, so untrimmed this would have put roughly a second of dead
   air in front of most of the 70 turns.

The motion sidecar then caught two dead holds — **6.0s** in `02-industry` and
**8.4s** in `03-cell` — that no source-level beat map would have shown, because
an authored tween is not a pixel changing.

**One honest note on the fix for those.** Each unit now carries a slow full-span
camera drift (`#drift`, 1.8% scale over the unit). Camera is this piece's
declared primary continuity mechanism, so it is defensible on its own terms —
but it was added *in response to* the motion gate, and it is doing part of the
work of keeping long holds alive. The per-phase content beats added alongside it
(the water leaving the cell, the RAISIN label, the naming argument, the K-beauty
format chips) are the real fix; the drift is a floor under them.

## Known-bad line, shipped by operator decision

`t048` — **"None of it passed peer review."**

**This is false.** All twelve trials in C7 are peer-reviewed articles in indexed
journals; that is what PubMed indexes. It also contradicts C5 and C6, which the
video cites approvingly about thirty seconds earlier.

It was raised, and the operator elected to keep it. Exposure is limited as far
as craft allows: **VO only** — no on-screen text, no headline, no citation pill,
not a section button or chapter title.

## Sources — paste into the description

All verified against PubMed on **2026-09-02**. On-screen pills carry
`Journal · Year` only; no PMID or internal id ever renders.

- Schwibbert et al. 2010, *Environ Microbiol* — https://doi.org/10.1111/j.1462-2920.2010.02336.x
- Sahle et al. 2018, *Phys Chem Chem Phys* — https://doi.org/10.1039/c8cp05308a
- Yu, Jindo & Nagaoka 2007, *J Phys Chem B* — https://doi.org/10.1021/jp068367z
- Bow et al. 2021, *Biochem Biophys Rep* — https://doi.org/10.1016/j.bbrep.2021.101134
- Heinrich, Garbe & Tronnier 2007, *Skin Pharmacol Physiol* — https://doi.org/10.1159/000103204
- Marini et al. 2013, *Skin Pharmacol Physiol* — https://doi.org/10.1159/000351381
- Trial count: PubMed `ectoine AND Clinical Trial[Publication Type]`, **12**,
  retrieved 2026-09-02. **A live number** — re-run before publish.
- Industry ties: Andreas Bilstein (bitop AG) is a named author on the 2013
  eczema trial and at least two others.

## Chapters — paste into the description

```
0:00 The bacteria that invented skincare
1:16 Give the protein some space
2:09 What this actually means for skin
2:46 Does it work on people?
3:56 How to read the bottle
5:14 The honest verdict
```

## Outstanding

1. **Render + master — done for render 9, and a standing rule.** Master is a
   **post-render** step and a re-render silently reverts it; the predecessor
   measured 9.6 LU below its previous deliverable on a file otherwise ready to
   ship. It has now been re-run after every one of the nine renders. After any
   future re-render, run
   `python3 scripts/master-audio.py . renders/<raw>.mp4 renders/<final>.mp4`,
   then `ffmpeg ebur128` on the **shipped MP4**, not the PCM intermediate:
   AAC raises intersample true peak, which is why the pass targets `TP=-4.0`
   (the overshoot is not constant — see the mastering table above).
2. **Thumbnail scoring.** `assets/thumbnail/final.png` exists and is
   grid-checked, but `vidiq_score_thumbnail` / `vidiq_similar_thumbnails` were
   not run — it has not been scored against the current results page, and
   title+thumbnail should be scored together.
3. **Description / tags / pinned comment / end-screen target.**
4. **`t030` needs an operator decision.** The original take was pure silence.
   The re-roll used the prompt *"No. Not at all."* rather than the script's
   *"No."* — a bare monosyllable gives this engine no room to decay into.
   Either accept the added words or re-roll the original text.
5. **Seven takes end marginally hot** (−45 to −35 dB at EOF): `t008 t013 t016
   t025 t026 t032 t055`. Below the regeneration threshold; listed so a listen
   pass knows where to look.
6. **Catalog contribution — partly done.** The Jargon Alarm is harvested as
   `catalog/visual-components/running-gag-badge/` (spike + README + index and
   README entries), carrying the two render-safety lessons that made it worth
   cataloguing: a bounded repeat count, and retirement as a tweened colour
   rather than a callback-set class. The merged-actor phase pattern is **not**
   harvested — it is a structural convention rather than a component, and it
   belongs in a skill or a `hyperframes-core` note, not in `catalog/`.

7. **Note for channel consistency.** Another session added
   `catalog/visual-components/dialogue-lanes/` at 06:42 today — a two-speaker
   component carrying identity by LANE plus colour and entrance, already wired
   into `videos/collagen-where-did-it-go` (41 turns). That is essentially the
   "two rails + centre stage" treatment this piece declined in favour of
   type-only attribution. Both now exist on the channel. **If a convention is
   wanted, this is the decision to make** — two incompatible two-speaker
   treatments with no documented default is the same drift the caption-mechanism
   note in `faceless-video-craft` warns about. This piece's choice was
   deliberate and is recorded in BRIEF.md; it is not an oversight.

## A correction on file handling

An earlier note in this file and a message to a peer session said renders were
gitignored and that this branch carried no mp4. That was wrong. Only the render
SCRATCH is ignored (`renders/work-*/`, `.hf-transaction-*`); the mp4 itself is
tracked, which matches the repo -- 160 mp4 are already carried through LFS,
including other projects' `.raw.mp4`.

What was genuinely avoidable: a `git add -A` committed a STALE raw render (91 MB)
that was already being superseded by the next render. The branch should carry the
mastered deliverable, not an intermediate that is mid-replacement. The stale raw
is removed in the final commit.

## Where things are

This work is on branch **`session/ectoin-normal-person`** in
`.claude/worktrees/ectoin-normal-person/`, not the shared checkout — the shared
tree was switched to `video/hyaluronic-acid-vs-filler-v2` by another session
mid-build, with 45 dirty tracked files belonging to someone else. To bring it
onto master:

```bash
git -C "$(git rev-parse --show-toplevel)" merge --no-ff session/ectoin-normal-person
```
