# Decision ledger — kbeauty-label-trap

Run started: 2026-09-03 · Channel: SeoulHabit · Baseline: reused (fresh)
Credit budget: 200 pre-production, $5.00 total · Spent: 0 · Tags: `long-form`

Format: `[stage/rule] fork → value | data read (threshold) | tool`
Companion gates: `COMPANION-RESOLVED:<name> (skill-tool|file)` or `COMPANION-MISSING:<name>`

## S0.0 Environment
[S0.0] skill → v2.1.0, commit `6d70e4d` == origin HEAD | "pick up latest skill" already satisfied, nothing to pull | git
[S0.0] OUT → `<repo>/videos/kbeauty-label-trap/` | `/mnt/user-data/outputs` tested fresh, ABSENT | bash
[S0.0] CHANNEL → `<repo>/videos/_channel/` | existed, git-tracked, `updated: 2026-09-03` | bash
[S0.0] pin → hyperframes 0.8.26 | `hyperframes --version` (global CLI, bare invocation per repo convention, not npx) → 0.8.26; diverges from prior runs' 0.8.22 pin | bash
[S0.0] provider vidIQ → ok | 2246 credits (1446/2000 renewable + 800 add-on) | vidiq_balance
[S0.0] provider Higgsfield → ok | 2344.95 credits, plan=free; Kimberly voice id confirmed extant | balance, list_voices
[S0.0] provider Gemini → no-key | `GEMINI_API_KEY` unset | env
[PR-1] research provider → does not fire | Gemini status != ok; claim sourcing runs on the 5 operator anchors + PubMed MCP/WebFetch for gaps | —
[PR-2] voice provider → `current-vo` (Higgsfield generate_audio, Kimberly) | Gemini status != ok → stated fallback; also the operator's explicit ask | providers.yaml §tts
[S0.0] project skill → none | confirmed by search; SKILL.md states the repo has none | —
[S0.0] therefore `K-*` applies as the undiluted floor | decision-policy.md §Claims | —
[S0.0] tokens → inherit `ectoin-survival-molecule/assets/tokens/tokens.css` + new `--vermilion` | canonical landscape set; no vermilion token exists; operator confirmed add-token over alias-coral | AskUserQuestion

## Operator decisions (pre-run, via AskUserQuestion — plan-mode gate)
[OPERATOR] runtime clock → measured VO + authored pauses, not padded to 5:00 | 646 words < 675–825 word budget for 300s; expect real length <5:00, logged as deviation | AskUserQuestion
[OPERATOR] hook length → trim to ≤20s, restructure not cut | `[S4/S-6]` hard cap; passport thesis moves to Misconception, also fixing that section's missing wrong-belief sentence | AskUserQuestion
[OPERATOR] vermilion → new `--vermilion` token, not `--coral` alias | honors brief's named accent over cross-channel palette consistency | AskUserQuestion
[OPERATOR] music → reuse-first, audition existing track-pulse.wav beds before generating | `[S4/V-3]` rule; matches skill's reuse-before-generate default | AskUserQuestion

## S0 Baseline
[S0/B-1] baseline → SKIP (fresh) | `videos/_channel/baseline.yaml` stamped `updated: 2026-09-03`, today | file
[S0] retention → `avg_view_pct_long: 43.07, n=2, both private, "not usable"` | every curve/retention comparison this run is `[UNDERPOWERED]`; real comparators are `ectoin-survival-molecule` (340s) and `hyaluronic-acid-vs-filler` (160s) own run reports | baseline.yaml

## S1 Story
[S1/S-1] format → long 16:9, operator-directed | prior long-form art exists but both private → `[UNDERPOWERED]`, "vertical slice first" clause skipped | baseline
[S1/S-2] target length → nominal 300s, measured VO governs | within 4:00-12:00 clamp; operator decision: no padding | AskUserQuestion
[S1/S-3] presenter → moving diagram | 5/6 sections are mechanism explainers | —
[S1/S-4] voice → Kimberly, single narrator | standing channel voice, confirmed resolvable, operator's explicit ask | list_voices
[S1/S-5] spine → 6/6 grounded, 0 [UNGROUNDED] | hook/misconception restructure supplies Misconception's previously-missing wrong-belief sentence | —
[S4/S-6] hook cap → restructured, not cut | 28s script hook > 20s hard cap; moved passport-thesis sentences (28 words) into Misconception | operator decision
[K-1] inventory → 19 claims: nominal 2 · sourced 7 · unsourced 2 (C6, C15) · illustration 4 · editorial 8 | every identifier fetched and read live this run | WebFetch x3, PubMed MCP x2
[K-1] source rejected → niacinamide-specific PMID hit NOT used for C6 | would source a narrow ingredient-specific claim as if it backed a general one — same overreach class the PR#11 ledger flagged | PubMed MCP search
[K-2a] hard-prohibited set → CLEAR | C15 reworded off absolute language; "80%" renders only as Bottle A's quoted label art, never a video assertion; no real named comparator | —
[K-2b] ratio limb → does NOT fire | Mechanism 6 sourced : 1 unsourced (C6); Proof 0:0 editorial-only | computed
[K-3] reword 1 → "'Gentle' is never universal" → "'Gentle' isn't a fixed property" | drops K-2a absolute language, keeps the point | —
[S4/V-1] word budget → 750±10% (675-825) target vs **646 actual**, 29 words under floor | logged deviation, not padded per operator decision | wc

## S2 Topic gate
[S2/T-1] seed → `k-beauty ingredient label` | shortest phrase naming the mechanism, no brand | —
[S2/T-2] demand → FAIL then SWAP → PASS | seed volume 0/<750mo/no overall; swapped to `k beauty` (overall 65.96, volume 69.74, competition 39.7) — passes both limbs, specificity loss logged plainly | vidiq_keyword_research
[S2] slug DIVERGES from seed → kept `kbeauty-label-trap` (fixed at S0.0) | shorter, more distinctive than seed-derived form | —
[S2/T-3] outliers → PASS in letter, degraded in substance | top breakout results are noise (lyric video, Tyler Perry review); one real comparator (Skinvestigation "beauty industry exposed" investigative format, breakout 120.49) | vidiq_outliers
[S2/T-3] reframe → NOT opened | T-2 passed after swap; run not tagged `experiment` | —
[S2/T-4] title shape → N-red-flags/safer-choice investigative frame, adapted not copied (this video's shape is N-questions) | —

## S3 Packaging
COMPANION-RESOLVED:frontend-design (skill-tool)
[S3] frontend-design → 2 corrections applied: (1) porcelain locked as default ground, ink-black reserved for bench-only scenes (avoids AI-default cluster #2); (2) vermilion stamp moved onto the bottle itself in the thumbnail, tying accent to the passport-motif signature rather than arbitrary color | frontend-design
[S3/P-1] titles → 5 shapes scored, one round: negative-capability **96** (winner, = operator's primary) · question 92 · exposé 87 · myth-bust 85 · listicle 77 | vidiq_score_title x5
[S3/P-2] concept → two bottles, scanner split, vermilion stamp on glass, `THE LABEL ≠ THE FORMULA` overlay | saturation 0/10 near-identical | vidiq_similar_thumbnails
[S3/P-3] thumbnail → generated 1, self-score 89, independent score 89 (agree), ≥70 → no refine | 1280×720 saved `04-assets/thumbnail.png` | vidiq_generate_thumbnail, vidiq_score_thumbnail

## S4 Script + VO
[PR-3] VO cost preflight → 1.7 credits per ~46-word stem, roughly proportional to length | get_cost:true before any spend | generate_audio
[S4/V-1] word budget → 646 actual vs 675-825 target (300s@150wpm±10%), 29 words under floor | logged deviation, operator decision not to pad | wc
[S4/V-2] VO → **257.120s exactly** (speech 251.470s + 4.45s authored gaps + 1.20s room-tone tail), one generation pass, cap 2 not needed | 9 speaker-turn stems, silence-trimmed via ffmpeg silencedetect (noise=-35dB, d=0.15) + 0.03s safety pad; `vo-timing.json` IS the master clock | higgsfield generate_audio x9
[S4] rate limit → Higgsfield 429s on concurrent submission (batch-of-9 and batch-of-4 both failed instantly, single-at-a-time succeeded after one retry) — likely shared account throttling from other concurrent worktree sessions this repo runs, not a per-run cap | matches PR#11's documented "~4-5 in flight max, submit/drain/repeat" pattern, though ceiling was lower this run (effectively 1 in flight) | —
[S4] stem granularity → 9 speaker-turns = 9 script paragraphs (single narrator, no voice-change constraint) | matches PR#11's precedent that a speaker turn is the smallest safely-proportionable unit for [S5/C-1] | —
[S4/V-3] music → **REUSED**, not generated | the three candidate `track-pulse.wav` beds (centella-tiger-grass, retinal-clinical-dossier, madecassoside-clinical-cut) are byte-identical (md5 confirmed) — one house pulse-percussion bed, not three auditions. Looped x5 + trimmed to 257.12s, 1.5s/2.0s fades. Per-question acceleration and the warm reveal resolve deferred to mix automation at S6/S7 (hyperframes-audio's domain), not a new generation — ~25 credits not spent. | catalog scan, md5
[S6/A-1] tokens → REUSED `ectoin-survival-molecule/assets/tokens/tokens.css` verbatim (confirmed genuinely landscape-calibrated: 1920x1080 canvas block, safe-area 54/108/96/96, end-screen reserve 640/200 all present and matching this plan — the file's own header comment about "canvas IS 1080x1920" describes the type scale's historical provenance, not the file's target canvas) | file
[S6/A-1] tokens → ADDED `--vermilion: #E34234` as a project-local accent (kbeauty-label-trap only) | operator decision, pre-run; `--coral` stays unused to keep "one accent per frame" | —

## Model tier
[MODEL-TIER] S5 onward → flagged, stronger-tier work begins (spatial/structural reasoning: beat sheet, composition, pixel QA) | decision-policy.md's model-tier protocol | —

## S5 Beat sheet
[S5/C-1] beats → **14 scenes**, all times derived from `vo-timing.json` — section boundaries at gap midpoints, sub-scene splits within a stem by character-offset proportioning (same method PR#11 used for cross-voice beats, applied here within a single voice). No time is hand-typed independent of that source. | computed from vo-timing.json
[S4/S-6] spine split (actual, vs. canonical @300s nominal, informational only — no baseline to enforce against) → hook 6.1% (target 0-8) · misconception 10.7% (8-18) · mechanism 39.5% (18-55) · proof 15.6% (55-75, a bit under) · application 9.8% (75-90, a bit under) · recap 18.4% (90-100, over — driven by the reveal+landing payoff both being genuinely substantial, not padding). No baseline override applies (long-form retention unattributable); logged as measured, not corrected. | computed
[S5/C-3] end scene → **9.451s** (8-20s band) | FIRST split attempt (whole s08 landing stem, 20.245s+1.2s pad=21.445s) exceeded the 20s cap by 1.445s; resolved by character-proportion-splitting s08 into s13-recap-questions (the five-question card, not yet reserved-zone) and s14-landing (seals→passport→SeoulHabit mark, the true reserved-zone end card) at the "That is how you turn..." sentence boundary | computed
[S6/A-9] actor map → `bench` persists s01/s02/s03 (born) and returns s05/s07/s09/s10/s11 (snap-backs) and s12 (exact reveal reuse, same sub-comp not a rebuild); `passport` persists s02→s07; `evidence-seal-array` persists s03→s12 (6 consecutive scenes, full merge treatment per plan) | —
[S6/A-8] transitions → **hard-cut ×5 (38%) / wipe-left ×6 (46%) / wipe-up ×2 (15%)**, 3 types, 13 boundaries | diverges from the plan's sketched 60/30/10 split — hard-cut is used at every "snap to bench + seal flip" beat (5 of them), which is a deliberate repeated structural device (the bench-as-home actor anchor), not per-scene transition fatigue. No `push-slide`, no plain crossfade across the dark/paper ground change (all 5 dark↔paper crossings — s01↔s02 wipe-up, s03↔s04 wipe-up, s09↔s10/s10↔s11/s11↔s12 hard-cut — use a transition, never a crossfade). Logged as a real deviation from the plan's sketch, not silently forced to match it. | computed
[S5/C-1] chapters → 9, first at 0:00, min gap **15.777s** (≥10s floor) | chapters = section/sub-section starts, distinct from scene boundaries (min scene duration 8.01s at s07 is a separate, unrelated number — not a chapter-gap violation) | computed

## S6 Composition
COMPANION-RESOLVED:frontend-design (skill-tool)
[S6] frontend-design entry gate → **signature device identified**: the vermilion ink-stamp circle (not the bench, not a generic seal badge) is the one signature component per video posture rule. Reused verbatim as: the passport ID stamp (s02), all 5 evidence seals (s03/s12/s14), and the end-card passport-lock (s14) — one SVG generator function, reskinned by glyph/size, never redrawn as a different idiom. | frontend-design
[S6/A-1] discovery → ThresholdList adapted for s04 canyon (ranked list + cutoff rule + below-cutoff desaturate/scramble, restyled); MaterialTriptych-style N-parallel-lanes pattern adapted for s06 chambers; travel-corridor pattern built once, reused at s08 (vehicle journey) and s10 (evidence tunnel); bench+bottle-pair markup identical between s01 and s12, only the `liquid_kind` data differs (ambiguous→lattice/water), resolving the mystery without a rebuild [S6/A-9]. | —
[S6] check cycle 1 → 12 missing-file errors (scenes not yet authored) | expected, not a defect | hyperframes check
[S6] check cycle 2 → 2 real defects fixed: `gsap_css_transform_conflict` (5 occurrences — CSS `transform:translateY(Npx)` fighting GSAP's own y-management, stripped from CSS since gsap.set() already establishes the same initial offset) and `gsap_non_transform_motion` (#s08-passenger animated via `left`, snaps to integer device pixels under frame-seek capture — switched to transform `x`) | hyperframes check
[S6] check cycle 3 → 2 real defects fixed: layout `container_overflow` (s09's two SVGs overflowed their card by 23px, shrunk from 480×380 to 440×330) and `contrast_aa_failure` (below-cutoff canyon rows at 0.55 opacity measured 2.67:1 against the 3:1 large-text floor — replaced `var(--ink-3)` with check's own suggested `rgb(146,142,132)`) | hyperframes check
[S6] check → **clean**: 0 errors, 0 warnings, 19/19 contrast checks pass WCAG AA. 2 real fix cycles used, within the 3-cycle cap. | hyperframes check --samples 40
[S6/A-8] transitions → confirmed at build time: hard-cut ×5 / wipe-left ×6 / wipe-up ×2, 3 types, **0 plain-crossfade-across-ground violations** (continuity-audit.py) | continuity-audit.py
[S6/A-10] entrance signatures → top signature `{opacity,y}+power3.out` at **40.6%** of 101 tweens — under the 50% template-failure bar. No timeline declares `defaults:{ease}` anywhere (0/14). | continuity-audit.py
[S6/A-9] actors → **0 rebuilt-actor pairs** (bench/passport/seal markup genuinely reused, not redrawn) | continuity-audit.py
[S6] camera continuity → **real gap found and partly closed**: first audit pass found 0 genuine camera-move tweens (a 4-count "hit" on s10 was a heuristic false-positive matching element-level opacity/y reveals, not a whole-stage move) — despite the plan's own stated intent to "dive into" each mechanism via camera push. Added 3 genuine whole-stage scale+y push-in tweens (s04 canyon, s06 chambers, s11 boundary) reusing one consistent camera-dive pattern; re-audit confirms 3 real camera moves. **Logged honestly as a partial retrofit** — s07/s08/s09/s12/s13/s14 still read via element-level reveals only, not a full camera treatment across all 14 scenes; the three added are the plan's clearest "dive into a mechanism" beats, not exhaustive coverage. | continuity-audit.py

## S7 Render QA — round 1 (pre-fix)
[S7/R-1] check → clean, 0 errors/0 warnings, 23/23 contrast | hyperframes check --samples 40
[S7/R-3] render 1 → 1920x1080/30fps/257.133s, 9.0MB, rendered in 9m20s | hyperframes render
[S7] audio mix bug found and fixed → ffmpeg's `amix` filter defaults `normalize=1`, auto-attenuating every input to prevent clipping on sum — this silently dropped the mix ~6 LU below the VO's own standalone loudness (-29.75 vs -23.60 LUFS measured). Fixed with `normalize=0` (music was already manually ducked to 0.12, no need for amix's own protection). | ffmpeg volumedetect + loudnorm
[S7/R-3] final master (round 1) → -16.10 LUFS / -1.80 dBTP, 257.20s | ffmpeg loudnorm two-pass (linear, falls back to dynamic — the source's high crest factor makes a pure-linear -14 LUFS impossible without exceeding the -2.5dBTP ceiling)
[S7/R-2] pixel gate, manual frame review (14 settle points + frame0 + last, before running the landscape tooling gates) → **4 real defects found**, none caught by `hyperframes check` or `check-safe-area.py`:
  1. **frame 0 nearly blank** — violates the mandatory "frame zero is the hook" rule. s01's droplet faded in from opacity 0; fixed to start already visible (matches the brief's own "single droplet falls" hook).
  2. **s04 tag overlaps live list text** — "ORDER ≠ EXACT DOSE" sat directly over the below-cutoff ingredient rows. Not caught by `check`'s 40-sample layout pass (missed the exact overlap window). Fixed by dimming `.canyon-list` to 0.1 opacity before the tag appears.
  3. **s12 verdict labels overlap the bottle graphics** — "[Authored, illustrative — not a claim]" text ran through the lower body of both bottles. Fixed by moving the bottle-pair up (top 46%→36%, translateY -40%→-50%) and shrinking the bottles (380×190→300×150), opening real clearance.
  4. **the video's real last ~0.45s rendered solid black** (a structural bug, not cosmetic) — every sub-composition's own `data-duration` was set to the beat sheet's NOMINAL scene duration, while `index.html`'s wrapper keeps each clip mounted for nominal+d_in+d_out (the transition-overlap formula, `[S6]`'s own math). Once a scene's internal timeline "finished" before its wrapper unmounted it, the dead zone rendered black instead of holding the last frame. **Affects 8 of 14 scenes** (every one followed by a non-cut transition — s01,s02,s03,s04,s06,s08,s12,s13), not just the visually-checked final scene; only the video's true end frame happened to land in one of these windows during manual review. Fixed centrally in `build_composition.py`'s `write()`: every scene's `data-duration` and forced timeline-length anchor now use the transition-extended duration, computed once and shared with the same formula `index.html`'s own generator uses — not duplicated per scene. | manual PNG review of all 16 extracted frames
[S7/R-1] re-check after fixes → clean, 0 errors, 3 warnings + 4 info, 23/23 contrast | all warnings/info are the s01→s02 wipe transition's overlap window (`check`'s DOM-bounding-box overlap detector isn't clip-path-aware — during a wipe, only the unmasked region of each element is actually visible on screen; the tool sees two boxes at the same coordinates and can't tell one is 90% clipped away). Flagged for visual confirmation on the re-render's extracted frames, not assumed safe from the warning text alone. | hyperframes check --samples 40
[S7/R-3] render 2 (post-fix) → 1920x1080/30fps/257.133s, 9.1MB, 7m57s — all 4 defects confirmed fixed via re-review of the same 16 extraction points + the s01-s02 transition midpoint | hyperframes render
[S7] gates on final.mp4 → check-safe-area.py **0 findings** (1028 samples); check-static-hold.py and check-cadence.py both advisory-pass with real findings preserved (12/14 scenes exceed the 6s quiet ceiling, concentrated where a diagram/citation needs reading time) — logged as a named follow-up in `09-run-report.md`, not fixed this round (both gates are advisory; this run is already on render 2 of the pixel-gate's 2-cap, past the point of diminishing return for a purely-cosmetic 3rd pass) | catalog/tooling
[K-4] rendered-claim check on final frames → **passes**. Flags concurrent+muted for C6/C15, citation chips plain+human-readable for C3/C4/C8/C10, no ING-* ids, "80%" (C17) never rendered on screen at all (VO-only, sidesteps the floating-stat risk entirely), no scorecard grammar on the verdict tags, no hard-prohibited claim on any reviewed frame. 0 fix cycles needed (caught pre-render). | manual frame review
COMPANION-RESOLVED:design-critique (skill-tool)
[S7] design-critique → signature stamp device confirmed as genuine continuity, not decoration; dark/porcelain register alternation confirmed intentional. **2 follow-up findings, not fixed this round**: (1) s05 leaves ~65% of canvas empty, reads as the one templated/generic-feeling frame in the piece; (2) s01's vertical ribbon text may not be legible at real viewing speed. Both logged in `06-render/design-critique.md` and `09-run-report.md` as next-round items — same scope-deferral reasoning as the cadence/static-hold advisories, not silently dropped. | design-critique

[K-4-PRE] **rendered-claim gap found before render, fixed at source** — pre-render inspection of the composition source found the `.uf-badge`/`.cite` CSS existed (baked into SHARED_CSS) but was **never wired to any actual claim**: C6 and C15 (the two unsourced claims) had no on-screen flag at all, and C3/C4/C8/C10 (the four sourced claims) had no citation chip anywhere in 14 scenes, despite `01-story-brief.md`'s §Sourcing table promising both. Fixed at the composition-source level (a render would only have shown this at frame-extraction time, wasting a full render cycle — caught first by reading the generated HTML directly): s05 gets a concurrent `UNSOURCED` flag + reworded on-screen text ("may be active at low levels", matching the story-brief's own K-3 wording) for C6; s11 gets a concurrent `UNSOURCED` flag + explicit on-screen line ("'Gentle' isn't a fixed property") for C15; s04 gets `FDA · 21 CFR 701.3` + `EU · Reg. 1223/2009 Art. 19` chips for C3/C4; s06 gets `J Cosmet Sci · 2020` for C8; s09 gets `Int J Cosmet Sci · 2009` for C10. The "80%" Bottle-A claim (C17) is deliberately **not** rendered as on-screen text anywhere — VO-only — which trivially satisfies K-2a's no-floating-unattributed-stat rule rather than requiring careful quote-mark handling. Re-checked clean: 23/23 contrast (up from 19, the new chips all pass). | manual source review + hyperframes check
