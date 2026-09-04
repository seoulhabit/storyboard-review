# Decision ledger — ectoin-normal-person (cold-open revision)

Run started: 2026-09-03 22:08 · Channel: seoulhabit · Baseline: reused from prior run
Credit budget: 200 pre-production · Spent: 0 (S0–S3 skipped) · Tags: revision

Format: `[stage/rule] fork → value | data read (threshold) | tool`
Companion gates, one line per attempt: `COMPANION-RESOLVED:<name> (skill-tool|file)` or `COMPANION-MISSING:<name>`

**Note:** this project shipped before the numbered-artifact convention and
carries no lines 1..N of prior ledger to append to. This file starts fresh at
the revision; the shipped cut's own record is `BRIEF.md`, `SCRIPT.md`,
`STORYBOARD.md`, `DELIVERY.md` (see `00-environment.md` for the filed
`[NOT IN SKILL]` on this gap).

## re-run — cold-open revision, 2026-09-03

Operator feedback rewrites the opening: the "11% bottle -> it's a blend ->
turn the bottle around" reveal moves to frame 0; the bacteria-origin section
compresses to one narrated raisin beat; closes on "Skincare borrowed the
molecule. Marketing borrowed the drama." Decisions taken with the operator
before work began (AskUserQuestion, this session): trim CH5's repeat of the
bottle-turn reveal (keep t049-t050, t055-t057; drop t051-t054); ship a
generic illustrative bottle, no brand; revise in place on this branch, not a
sibling recut directory (repo precedent exists both ways — see
`hyaluronic-acid-vs-filler`'s `09-run-report.md` §Deviations for the same
fork resolved the same way).

[S0/B-1] baseline -> not refreshed | reused, subject/seed unchanged (revision, not a fresh build) | n/a
[S1/S-5] spine -> reused, one new claim row set added (C9-C11) | BRIEF.md §Sourcing carries the K-1 table for this project (no separate 01-story-brief.md; see [NOT IN SKILL] below) | n/a
[S4/V-2] VO -> 5 new turns generated (t071-t075), SOULHABIT/Kimberly (element 674b71b8), 1 regeneration on t075 (first take ended mid-word at -17.7dB EOF; regenerated take measured -37.1dB with a smoothly decaying tail to -47.7dB at the tightest 0.03s window, read as a natural word-ending and accepted at the 2-generation cap) | measured via ffprobe+ffmpeg volumedetect/silencedetect (scripts/gen_vo.py's own analyse()) | Higgsfield generate_audio x6 (5 new + 1 regen)
  t071 3.51s 202wpm · t072 6.69s 214wpm · t073 6.53s 153wpm · t074 10.60s 156wpm · t075 4.40s 116wpm -- all within/near the 110-230wpm band. New speech total 31.73s.
[PR-3] spend -> 4.10 Higgsfield credits ($0.082 @ $0.02/credit) for 6 generations | providers.yaml tts rate | well under $5.00 per-run cap and 80% warn line

## S6 Composition
COMPANION-RESOLVED:frontend-design (skill-tool)
[S6/A-1] assets -> browser-drawn (SVG/CSS/canvas), same as the rest of the project; the two new units reuse existing proven mechanisms (12-bottle's bottle/turn/INCI actor, 03-cell's crystal-field/cell/raisin/ectoin actor, 04-protein's swap-panel idiom) rather than generating new plates | catalog/ has no bottle/brine/cell/molecule entry (checked, see the run's own catalog survey); mechanism reuse from within-project is the higher-priority match per A-1's own "mechanisms, not only imagery" clause | n/a
[S6/A-2] tokens -> clean; both new units' CSS is var()-based, no ad-hoc colors. Two raw px font-sizes (120px hero number, 22px INCI list) are inherited verbatim from 12-bottle's already-shipped markup, not new choices. New illustrative-label tag set at --t-chip (32px), clearing the labels/chrome floor | manual review (frontend-design's own skill content is for greenfield pages, not review; applied its token/type-floor/contrast lens directly against the built compositions/frames/*.html) | grep + contrast.py-style WCAG calc
[S6/A-7] contrast -> swap2 panel: celadon-on-ink 8.32:1, paper-on-ink 16.81:1, both clear 4.5:1 with room | scripts/contrast.py method | manual calc
[S6/A-9] camera/actor map -> 01-bottle carries the label/turn/list actor into 02-origin's brine field into the cell/ectoin actor (reused verbatim from 03-cell) into 04-protein's protein+shell (unchanged handoff, L2->L3 continues). 5 merged units total (was 4): 01-bottle, 02-origin, 04-protein, 05-skin, 12-bottle | continuity-audit.py, run post-render at S7 | n/a
[S6/A-10] entrance idioms -> arrive/slam/swap/wipe used across the two new units (no single idiom repeated as the unit's whole vocabulary); no timeline-wide defaults:{ease} declared anywhere in frames_spec.py | grep for 'defaults:' returns 0 hits | n/a

## S7 Render QA
[S7/R-1] check -> PASS, 0 errors across Lint/Runtime/Layout/Motion/Contrast (--samples 60), 3 fix cycles used. 2 real bugs found and fixed: (1) motion_selector_ambiguous on #pc/#in-10 -- 01-bottle reused 12-bottle's bare ids while both render into the same document; fixed by prefixing 01-bottle's actor ids with ob-. (2) 01-bottle's own ambient #world drift tween overlapped its phase-b camera fly on the same x/y properties (overlapping_gsap_tweens) and was dragging content off-canvas real (not bounding-box-false-positive) overflow measured on #op/#ob-illus/#ob-in-10 up to 161px; root cause was a redundant hand-authored drift -- build_frames.py already appends one to #drift on every unit. Removed the custom drift and the 1.28 baseline #world zoom it needed, reused 12-bottle's proven fly-in values (1.22/-78/-26) instead of an untested 1.42. Also found and fixed: 12-bottle's new illustrative-label tag and its own phase-a states/pairs chips were not anchored/cleared correctly (chips never faded before phase D since their clear tween was tied to the now-retired t051 -- overlapping real content through the INCI reveal). All fixed; verified by rebuild+re-check, not assumed. | hyperframes@0.8.22 check --samples 60, 3 passes | npx hyperframes check
  Remaining findings, all info/warning (0 errors): container_overflow on #world during camera legs (5 instances, including one new one in 01-bottle/02-origin's own legs) -- the documented bounding-box-vs-clip-path false positive [S6/A-8]/[S6/A-3] names; one panel_out_of_canvas on #bpl (12-bottle) during its own phase-d camera fly, an opacity:0 (invisible) element's resting geometry, not visible content. Both classes accepted per policy; confirm on extracted frames below, not blocked on.
[S7/R-2] pixels -> 2 more real bugs found by extracting frames (not by check, which never flags this class): (1) 02-origin's stage() call omitted ground="ink" (defaulted to paper) while every dialogue line was authored ink=True (color:var(--paper)) for contrast against a dark ground -- paper text on paper background, invisible for the whole unit's dialogue (t073/t002/t003/t074/o-cite pill still worked, it sets its own dark background unconditionally). Confirmed at full resolution, not from a downscaled screenshot. Fixed: added ground="ink". (2) The two plate-collapse fixes (below) initially used height/minHeight/marginTop, which `check` correctly flagged as gsap_non_transform_motion (layout-reflow properties snap to integer pixels under seek-by-frame capture) -- switched to opacity+scaleY (transform-only). | ffmpeg frame extraction at 18 timestamps spanning frame 0, both units' quiet windows, and the flagged void/overflow moments; PIL crop for full-resolution close inspection | ffmpeg, PIL
[S6/A-1] leftover-panel fix -> 01-bottle's #op and 12-bottle's #bpl plate panels retracted their fill/text but left an empty min-height:150px box visible for the rest of the unit -- measured by check-static-hold's region-aware pass as real content-then-empty voids (7.75-11.25s and 212.25-228.75s) and, for #bpl, as real panel overflow once the phase-d camera zoomed in around the empty box. Fixed: collapse the whole panel (opacity+scaleY, not layout properties) right after its own retract.

## S7 Render QA (cont.)
COMPANION-RESOLVED:design-critique (skill-tool)
[S7/R-2] frame review -> 5 frames reviewed (frame 0, INCI payoff x2, ink-ground dialogue post-fix, endscreen bookend). No blocking findings. One cosmetic note filed: the ILLUSTRATIVE LABEL disclosure tag is legible at 1920x1080 desktop but small/muted enough to warrant a real-device check before publish -- not gating, K-2's own floor (--t-chip, 32px) is met. | design-critique skill, applied against extracted frames | n/a
[S7/R-2] render -> final render 297.025s, 1920x1080, 8911 frames. Master: -14.7 LUFS (target -14.0), -2.2 dBTP (must be <-1.0), PASS. Safe-area (HARD GATE): PASS, 0 findings/1188 frames. Static-hold whole-frame: PASS, 0 findings. Static-hold region-aware: 4 findings, all confirmed benign on extracted frames (empty grid cells with no content in that stretch, or the by-design endscreen right-third reserve) -- down from 8 before the plate-collapse fixes. Cadence: 13.7% whole-video (>= shipped 13.0% baseline). 2 scenes over the 6.0s quiet ceiling: 05-skin (7.75s, pre-existing/unchanged code, out of this revision's scope) and 12-bottle (6.25s, 0.25s over, advisory). Continuity --gate: PASS, 16/16 boundaries transitioned, 0 hard cuts, 0 crossfade-across-ground violations, top entrance signature 15.5% (well under any warning threshold), 0 timelines with defaults:{ease}, 5 merged scenes, 0 rebuilt-actor pairs, 11 camera moves. | full postrender gate chain run explicitly (not via npm's postrender lifecycle hook) against the mastered file | check-static-hold.py, check-safe-area.py, check-cadence.py, continuity-audit.py

## re-run — verdict-compression revision, 2026-09-03 (second)

Operator brief: rebuild as a scientifically responsible 16:9 explainer,
preserving the SoulHabit/Jay dialogue, dry humour, Jargon Alarm, and
"supporting actor, not superhero" close. Four content requirements beyond
the cold-open revision: a claim ledger, removal of the known-false `t048`
line, a viewer-facing verdict inside the first 20s, and compression to
35–45 turns / ~430–500 words, mechanism and bottle sections first.

**Import note.** This project's most recent build (the cold-open revision
above) existed only at commit `f893e7b` on a different, concurrently-active
worktree's branch (`claude/faceless-video-feedback-6c6c24`). Imported via
`git checkout f893e7b -- videos/ectoin-normal-person catalog/tooling
catalog/visual-components/running-gag-badge` onto this worktree's own
branch and committed immediately (`72ab419`) before any edits — no ref
surgery on a branch this worktree does not have checked out, per this
repo's CLAUDE.md.

[S0/pin] hyperframes -> re-pinned 0.8.22 -> 0.8.27 | global CLI reports
0.8.27, `hyperframes upgrade` reports "Already up to date" | operator
decision (put via AskUserQuestion): validate on the newer pin rather than
the stale one; every project script switched from `npx --yes
hyperframes@<pin>` to the bare binary
[S0/catalog] hyperframes catalog searched for count-up, transition, ducking
and two-speaker primitives (`hyperframes catalog --query ...`) -> nothing
adopted. The project's own count-up (06-trial104, 11-twelve) and dialogue
system (type-only attribution, `_preamble.py`) are already built, gate-clean
on the prior render, and match or exceed what the registry offers | n/a

### [K-1]/[K-4] claim ledger — CLAIMS.md, new this revision

Every claim re-verified live against PubMed E-utilities on 2026-09-03, not
copied from either prior ectoin project's brief. Two real corrections
surfaced:
- **C4 (Bow 2021).** The prior revision's `SCRIPT.md` said the dry-condition
  stress-worsening claim "did not surface in PubMed" and cut it on that
  basis. The live abstract states plainly: "Peak stresses were increased in
  harsh drying environments of <5% RH." The prior reasoning was wrong. Not
  restored to the script (this run is compressing); logged as a correction
  to the record.
- **C6 (Marini 2013).** Verified **two** bitop AG-affiliated authors
  (Reinelt AND Bilstein), not "Bilstein and ≥2 others" as the prior brief
  had it. The industry-connection claim is stronger than previously stated.
- PubMed count for C7 re-queried live: `ectoine AND Clinical Trial[pt]` = 12,
  unchanged from the 2026-09-02 count.
- `t048` ("None of it passed peer review") **removed** — false, contradicts
  C5/C6. The prior revision retained it by explicit operator decision; this
  brief reverses that decision (item 3, non-negotiable).

### [S5] script compression

The brief's two length constraints (35–45 turns, ~430–500 words) and its
runtime constraint (~3:00–3:30) are arithmetically incompatible once
verified against this project's own measured cost model. Regressing all 58
turns of the PRIOR revision's shipped takes (duration vs word count, least
squares): `speech ≈ 1.45s/turn + 0.329s/word`; measured non-speech pad on
that same render was 5.8%, so `runtime ≈ speech × 1.058`. At that rate,
465 words alone (ignoring turn-count overhead) already runs to ~3:52; 500
words to ~4:09. There is no point in the stated word band that fits inside
3:30.

Put to the operator via AskUserQuestion: **word count wins.** Target ~465
words / ~41–44 turns, log the runtime overshoot rather than under-cutting
the word floor to force-fit a runtime that the brief's own two numeric
constraints do not simultaneously allow.

Landed: **44 turns, 489 words** (both within the required bands) — see
`scripts/vo_lines.py`'s docstring and `SCRIPT.md` §Changes for the
turn-by-turn reasoning. Mechanism (CH2, 9t/97w → 5t/65w — the largest single
cut) and the bottle sections (CH1, CH5) compressed hardest, per the brief's
explicit priority order.

**The viewer-facing verdict now lands inside the first 20 seconds, measured,
not estimated.** Two new turns (`t076`, `t077`) follow the "it's a blend"
reveal. Real timing walk (`scripts/timing.py`, driven by ffprobe on the
actual generated takes): `t077` ends speaking at **t=18.552s** — see the
`01-bottle` phase table below. 1.45s of measured margin inside the 20s
window.

### [S4/V-2] VO regeneration

16 of 44 turns needed new audio (text changed or brand-new): `t017 t025
t030 t036 t038 t062 t072 t073 t074 t076 t077 t078 t079 t080 t081 t082`.
28 turns reused their existing, already-gate-clean takes unchanged.

`t030` ("No.") — the prior revision's own `DELIVERY.md` documents this
exact take as PURE SILENCE and names padding the TTS prompt to "No. Not at
all." as an accepted fix, while SCREEN stays plain "No." (VO/SCREEN
divergence is this project's own stated, pre-existing rule). Applied.
Regenerated clean, first take.

Higgsfield `generate_audio` (`seed_audio`, SOULHABIT = Kimberly `element
674b71b8-…`, JAY = Juno `preset a3ce02fe-…`) rate-limited heavily on
submission (`429 rate_limit_reached`) — batches of up to 12 routinely
partial-failed and needed 2–4 retry rounds each; all 16 first-pass
generations eventually succeeded. **5 of the first-pass takes failed this
project's own mid-word QC** (`scripts/gen_vo.py`'s `eof_level()`, threshold
-45dB): `t017` (-37.5dB), `t072` (-15.5dB), `t074` (-43.6dB), `t079`
(-14.3dB), `t080` (-34.8dB). Regenerated; `t072` took 3 rounds total (a
short two-sentence line, "No. It's a blend.", consistently truncating —
not a bare monosyllable like `t030`'s known issue, but short lines
generally seem to stress this engine's tail decay). Final regen: t017 clean
(-91.0dB), t074 clean (-91.0dB) on round 2, t079 clean (-91.0dB) on round 1
of the retry, t080 clean (-91.0dB) on round 1 of the retry, t072 clean
(-91.0dB) on round 3.

Zero dead takes, zero mid-word takes, in the final 44/44 set —
`python3 scripts/gen_vo.py --report-only` exits 0. 12 short/punchy lines
flagged outside the 110–230 wpm QC band (all reused, unchanged turns —
short single-clause lines reading slow by nature, e.g. `t002`
"Bacteria invented skincare?" at 66 wpm); the tool's own guidance is to
check by ear only if one sounds wrong, not to regenerate on the flag alone.

[PR-3] spend -> 21 Higgsfield `generate_audio` calls total (16 first-pass +
5 regenerations) at 0.1 credits each = 2.1 credits, against a 2275.25-credit
balance (`00-environment.md`). Negligible against the $5.00/200-credit
per-run cap.

### Measured result

`scripts/timing.py` walk over the real generated takes:

```
Total duration: 241.262s = 4:01.26   (was 297.025s = 4:57.02)
```

Against the brief's stated 3:00–3:30 band, this is a ~31–61s overshoot —
**logged as a deliberate consequence of the word-count-wins decision above,
not a miss.** Against the operator's own informal ~3:45–3:50 planning
estimate (made before real VO existed), it lands ~11–16s over — the
estimate underweighted this project's per-turn fixed cost (`1.45s/turn`),
which real dialogue with short interjecting turns pays more of than the
regression's aggregate fit suggested. The 44-turn / 489-word count itself
is exact, not estimated, and sits inside both required bands.

[01-bottle] phase table, from the real timing walk:
```
phase a (t071):        0.100 - 3.611   (the reveal, "eleven percent")
phase b (t072):         3.951 - 6.283   (the blend line)
phase c (t076,t077):    6.623 - 18.552  (THE VERDICT — completes at 18.552s)
```

S5 (composition markup: vendor GSAP, prefix DOM ids, strip CSS transform
initialisers on properties GSAP owns, music bed + SFX) and S6/S7
(validation, preview, render) are separate, subsequent stages — not yet
run as of this ledger entry.

### [S5] composition markup, [S6] validation — completed

**S5.** `frames_spec.py` rewritten for every unit whose turn/phase structure
changed (01-bottle, 04-protein, 05-skin, 07-preference, 10-notprove,
12-bottle, 13-kbeauty, 17-dignity — see the S2 script-compression commit for
the full per-unit account). Render-hardening, verified against actual GSAP
call sites before touching anything, not assumed:
- GSAP 3.14.2 vendored locally (`assets/vendor/`) — was a CDN `<script>` tag
  in every scene file AND a separately hardcoded one in `build_index.py`.
- Every DOM id prefixed with its composition id, applied centrally in
  `_preamble.scene()` via a new `_prefix_ids()` pass — discovers every
  `id="X"` already assembled (including what `build_frames.py` itself
  appends), rewrites the HTML attribute, `'#X'`/`"#X"` selectors, and
  `getElementById()` calls. Two dynamic-selector idioms needed a second
  pass after the first version shipped 156 spurious runtime warnings:
  bare id strings in `forEach` array literals concatenated with `'#'`, and
  loop-generated id STEMS (`'#ob-in-' + i`) shared by a family of real,
  statically-declared ids. `02-origin`'s fully-dynamic crystal-field ids
  (never a static `id="X"`) needed a hand fix using the unit's own `c.cid`.
- 3 genuinely redundant CSS transform initializers removed (`.wash`,
  `.band-f`, `.alarm`) where GSAP's own `fromTo()` already declares the
  same start state — verified each call site first; left `.plate-fill` and
  `.bar .f` alone, since those use bare `.to()` with CSS as their sole
  initial-state source, not a duplicate of one GSAP owns.
- Music bed + 14 local SFX cues added (`00-decision-ledger.md`'s own commit
  message has the full cue table); carved against both voice groups at the
  hyperframes-audio skill's documented default (strength 0.25, dynamic).

**S6.** `check-tokens.py`, `contrast.py`, `check-dead-sets.py` all clean.
`hyperframes check --samples 60 --json --snapshots`: **ok: true**, 0 errors
across lint/runtime/layout/motion/contrast, after fixing 3 real bugs found
by the check itself (a Python-style `#` comment left inside a JS timeline
string from an earlier edit; the two dynamic-selector id-prefixing gaps
above; a `content_overlap` layout error in 10-notprove's funding-disclosure
card caused by 5 sibling inline elements each carrying `position:relative`
wrapping to 2 lines — restructured to one wrapping element with the `<b>`
tags nested rather than sibling). `continuity-audit.py --gate`: pass —
16/16 boundaries transitioned, 0 hard cuts, top entrance signature 16.7%,
0 timelines with `defaults:{ease}`, 5 merged scenes, 11 camera moves.

**Verified by pixels** (this project's own R-2 rule), not by manifest:
midpoint snapshot captured for all 17 sub-compositions
(`snapshots/midpoints-verdict-revision/`) plus frame 0 and the full verdict
window (`snapshots/verify-open/`). Confirms: frame 0 composed, not blank;
the verdict text renders exactly as scripted at the measured 18.55s mark;
10-notprove shows exactly 2 claim cards; 17-dignity shows the merged
two-line JAY turn with no stray S interjection; every scene's on-screen
copy matches `SCRIPT.md` turn for turn. Phone-scale legibility (25%
downscale of three text-dense frames) confirmed readable, matching the
design system's own stated type-floor guarantee.

**Studio preview** opened (`hyperframes preview`, port 5677) and confirmed
functional: timeline populated with all 17 scenes, live scrubbing/playback
verified (paused at 00:07, matches the pixel-verified verdict window),
Studio's own lint panel flags 4 findings — all four are
`assets/thumbnail/cand-a.html`, a standalone Playwright-capture thumbnail
source file that is never part of the render timeline (no
`data-composition-id`, never referenced by `index.html`), pre-existing and
unchanged by this revision. The authoritative gate is `hyperframes check`
on the actual composition, which is 0 errors.

**S7 — STOPPING HERE per non-negotiable #14.** No render has been run.
Awaiting explicit operator approval before `hyperframes render`.
