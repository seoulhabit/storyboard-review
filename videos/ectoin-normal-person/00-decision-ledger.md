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
