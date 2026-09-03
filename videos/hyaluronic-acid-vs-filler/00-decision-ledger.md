# Decision ledger — hyaluronic-acid-vs-filler

Run started: 2026-09-03 00:40 · Channel: SeoulHabit (UCzqEGQ9uAU43AgyxGtLT7MA) · Baseline: refreshed
Credit budget: 200 pre-production · Spent: 35 · Tags: `baseline-partial`, `long-form-override`

Format: `[stage/rule] fork → value | data read (threshold) | tool`
Companion gates: `COMPANION-RESOLVED:<name> (skill-tool|file)` or `COMPANION-MISSING:<name>`

## S0.0 Environment
[S0.0] OUT → `<repo>/videos/hyaluronic-acid-vs-filler/` | `/mnt/user-data/outputs` tested fresh, ABSENT | bash
[S0.0] CHANNEL → `<repo>/videos/_channel/` | existed and was git-tracked (see CONCURRENCY below) | bash
[S0.0] pin → hyperframes 0.8.22 | `npx --yes hyperframes@0.8.22 --version` → 0.8.22; pin from ectoin's package.json and check.json:77, NOT hyaluronic-acid-serum's 0.8.17 | bash
[S0.0] provider vidIQ → ok | 2428 credits (1628/2000 renewable + 800 add-on) | vidiq_balance
[S0.0] provider Higgsfield → ok | 2437.25 credits, plan=free; Kimberly voice id still exists | balance, list_voices
[S0.0] provider Gemini → no-key | `GEMINI_API_KEY` unset | env
[PR-1] research provider → does not fire | Gemini status != ok; claim sourcing ran on PubMed + regulator fetch, which is the project's own source list PR-1 sits behind anyway | —
[PR-2] voice provider → `current-vo` (Higgsfield generate_audio) | Gemini status != ok → stated fallback | providers.yaml §tts
[PR-2] `listening-test pending` → NOT flagged | flag is scoped to gemini-tts runs; this run used current-vo | —
[S0.0] project skill → none | confirmed by search; SKILL.md states the repo has none | —
[S0.0] therefore `K-*` applies as the undiluted floor | decision-policy.md §Claims | —

## S0 Baseline
[S0/B-1] baseline → REFRESH | `videos/_channel/baseline.yaml` was stamped `updated: 2026-09-01`, older than this run | file
[S0/B-2] channel → UCzqEGQ9uAU43AgyxGtLT7MA / SeoulHabit / 8 subs | exactly one authorized channel → no BLOCKER-CHANNEL | vidiq_user_channels, vidiq_channel_stats
[S0/B-3] traffic schema → 10 source labels recorded verbatim | YouTube returned **no browse row and no suggested row at all**; SHORTS alone is 4192/4756 = 88.14 %. The pre-existing `browse: 0.925` is a CONSTRUCTED sum, now labelled as such, and `suggested` is RELATED_VIDEO (0.25 %) standing in for a slot never filled. | vidiq_channel_analytics(traffic_sources)
[S0] retention metric → `averageViewPercentage` IS retrievable | the default top_videos metric set OMITS it silently; a second call with explicit `metrics` returned it for all 39 rows. Recorded so a future run does not mark retention unavailable. | vidiq_channel_analytics(top_videos)
[S0] gate → `baseline-partial` | chosen format is **long**, and `retention.avg_view_pct_long` is not attributable (VOD corpus = 26 views/90 d; no top_videos row resolves to a long-form duration). Proceeding on [default]s for long-form retention, per the gate's own instruction. | —
[S0] `[S1/S-2]`'s own reasoning independently reproduced | ranking the top quartile by avg-view-% gives **18.9 s** on fresh n=39 data, against the 19 s the rule records — below the rule's own 30 s clamp floor. The rule is right to forbid the avp path for shorts. | computed
[S0] superseded method NOT written over the live field | recomputing `median_duration_top_quartile_curve_s` with a fixed p50_7d denominator gives 39.8 s; `curve.ratio_method: age-matched` and baseline-notes.md §Correction 3 say that method is wrong, so the measured **49.0 s** stands and 39.8 is filed as a cross-check only. | computed

## CONCURRENCY — recorded, not a blocker
At run start `videos/_channel/` did not resolve and the exploration pass confirmed it
absent repo-wide. It was in fact **git-tracked**, and this run's first write clobbered
`baseline.yaml`. Detected via `git status` showing ` M`, recovered with
`git show HEAD:...`, and the committed file restored before any further work; the S0
refresh was then applied as a **merge** (+61/-4 lines, the 4 deletions being exactly the
anchors replaced by richer versions). Verified preserved: `overrides[]`,
`curve.ratio_method`, `curve.full`, `corpus`, `views`, `packaging.title_scorer_discriminative`.
Two project directories absent from the run-start listing — `videos/collagen-where-did-it-go/`
and `videos/ectoin-normal-person/` — are present now, so **another session is writing to
this repo concurrently.** Consequence for the rest of this run: re-read
`videos/_channel/*` and `catalog/*` immediately before any write to them; never
overwrite either wholesale. Untouched by this run.

## S1 Story
[S1/S-5] spine → all 6 sections grounded, 0 [UNGROUNDED], 0 fabricated | supplied script fills all six | —
[S1/S-1] format → **long 16:9**, OPERATOR OVERRIDE of branch 2 | overrode 99.45% short by views-90d (4730 vs 26), 95.8% by uploads (46/2), 30-of-31 by repo corpus. Every curve.*/retention.* comparison this run is [UNDERPOWERED]. NOT fully first-of-kind — ectoin-survival-molecule is 1920x1080/340.2s prior art — so the "prove on a vertical slice first" clause is skipped, logged. | baseline + operator
[S1/S-2] target length → **180 s**, `below-clamp` | long clamp is 4:00-12:00. Clamp governs a target DERIVED from baseline; there is no long-form baseline to derive from (avg_view_pct_long unattributable). Operator runtime is a stated input, not a measurement that would defeat its own rule. | —
[S1/S-3] presenter → **moving diagram** | mechanism-heavy: three parallel mechanisms | —
[S1/S-4] voice → two-hander, `[NOT IN SKILL]` | Kimberly (element 674b71b8) NOT rotated, speaks SoulHabit; Grady (preset e2a2d2e6) added for Jay by S-4's own fallback ordering (no "neutral"/"narrator" name returned -> first returned, contrasting gender). Proposal filed. | list_voices
[S1/S-7] route → angle=concept | length=180s | destination=16:9 | VO_MODE=restructure per scene (script supplied but reworded under [K-2]) | —
[S1/S-7] route length divergence → 180 s vs route's 30-90 s "sweet spot" | advice, not a gate; [S1/S-2] wins | —

## Claims — K-*
[K-1] inventory → 12 claims: nominal 1 · **sourced 10** · unsourced **0** · illustration 0 · editorial 1 | every identifier FETCHED AND READ this run, not recalled | PubMed MCP, WebFetch, WebSearch
[K-1] chip vocabulary → `Journal · Year` / `FDA · <page>` ONLY | follows ectoin-survival-molecule's convention (its .cite CSS states it in every frame), NOT peeling-not-progress's older on-screen raw-PMID one. No PMID, no ING-* reaches a frame. | —
[K-2a] hard-prohibited set → CLEAR | the two safety claims are FDA-verbatim; the only on-screen number (1934) is cited; no treats/prevents/cures; no comparative superiority; no absolute language | —
[K-2b] ratio limb → **DOES NOT FIRE** | Mechanism+Proof sourced:unsourced = 8:0. Ships as a normal explainer, not disclosure-forward. No unsourced-flag component emitted. | —
[K-2] reword 1 → "Never inject a topical serum" → **"Do not inject yourself."** | FDA's actual sentence is "Do not inject yourself with dermal fillers." The original narrows the warning to serums and leaves self-injecting a real filler unaddressed — the more dangerous act, and the one the regulator names. | fda.gov
[K-2] reword 2 → "skin, joints and eyes" SPLIT into C3 + C4, separate chips | the skin source (Dermatoendocrinol 2012) does not cover joints; the joints source (Front Vet Sci 2019) is not a dermatology paper. One chip over both would stand on ground it does not have. | PubMed MCP
[K-2] reword 3 → none needed for "plumping" | script already hedged "temporarily"/"appear"; [K-3] pushes the same hedge into the on-screen type | —
[K-1] source NOT used → 21 CFR 878.3540 | eCFR redirected to a bot-block page and could not be read. "An identifier you have not read is not a source" — dropped rather than cited unread. The FDA consumer page sources C10/C11 verbatim on its own. | WebFetch (302 -> unblock.federalregister.gov)

## S2 Topic gate
[S2/T-1] seed → `hyaluronic acid vs filler` | shortest noun phrase naming the mechanism, 4 words, no brand | —
[S2/T-2] demand → **FAIL then SWAP -> PASS** | seed volume 0 / overall null / `<750`-mo. Adopted `hyaluronic acid filler`: overall **66.85** (>=50) AND volume 54.28 (>=40) with competition 14.3 (<=60) — passes BOTH limbs. | vidiq_keyword_research
[S2/T-2] higher-scoring rows REJECTED ON MEANING | botox 68.75 (different molecule); juvederm 68.66 / restylane 61.79 (brands, barred by T-1); **radiesse 67.54 (calcium hydroxylapatite — not HA at all)**; sculptra 60.57 (poly-L-lactic acid); skin care 64.97 / plastic surgery 60.41 (category, not mechanism) | vidiq_keyword_research
[S2] slug DIVERGES from seed → kept `hyaluronic-acid-vs-filler` | seed-derived `hyaluronic-acid-filler` is one character-class from the existing videos/hyaluronic-acid-serum/ and misdescribes a three-way comparison as a filler explainer | —
[S2/T-3] outliers → **PASS in letter, VOID in substance** | bounds sent explicitly: minSubscribers=0, maxSubscribers=max(10x8, 10_000)=10_000. Top 3: teeth-whitening (breakout 3137.67), gluteal IM injection (706.45), "Roblox 2.5: Filler pt16" (162.24). Also returned a billiards player named Joshua **Filler** and a WIX **oil filter** comparison. Swapped-seed re-run gave gecko rescues, lofi spa music, hydrofluoric acid. `requireAllTitleTerms=true` -> **0 results**. "acid"/"filler"/"injection" are each strongly polysemous. Recorded as a literal pass carrying no browse evidence, not laundered into a real one. | vidiq_outliers x3
[S2/T-3] reframe branch NOT opened | it needs BOTH T-2 and T-3 to fail; T-2 passed on its own after the swap. Run is **not** tagged `experiment`. | —
[S2/T-4] title shapes → **HARVEST DEGRADED**, 1 usable | extracting from the top-5-by-breakout would extract gecko-rescue and nursing-injection shapes. Only structurally relevant comparator: DCHYmELj1LE "The Acid That Eats Through Glass — The History of Hydrofluoric Acid" (breakout 4.37) = substance identity + surprising property + origin. Counter-example recorded, not harvested: LzVw4reocxk "ALOE VERA Erases Deep Wrinkles within 10 Minutes Even at 70!" is exactly the [K-2a] absolute-language pattern. | vidiq_outliers

## S3 Packaging
COMPANION-RESOLVED:frontend-design (skill-tool)
[S3] frontend-design changed two things | (1) **no 01/02/03 numbering anywhere** — numbered markers encode sequence, this content is three PARALLEL identities, so three lanes not three steps; (2) the signature must come from the subject's own world -> **the molecule's own morphology** (free coils / two sizes at a boundary / cross-linked lattice), which also becomes the [S6/A-9] actor map and camera path | frontend-design
[S3/P-1] title candidates → 5 shapes, 5 scoring calls, ONE round (the cap) | contrast 85 · question 89 · number 84 · why-X 93 · **substance+origin 95** | vidiq_score_title x5
[S3/P-1] winner → **"Hyaluronic Acid: Found in a Cow's Eye, Sold as Serum and Filler"** (62 chars, seed in first 60) | selected by T-4 shape rank — the only candidate using the single structurally relevant shape the outlier set produced | —
[S3/P-1] inversion → **NONE this run** | top scorer also won, so this run does NOT test `packaging.title_scorer_discriminative: false` (set from 2 prior runs). No failing control existed to rank. Logged as a null result for [S9/L-2], not as evidence the scorer works. | —
[S3/P-1] recorded tension | P-1's DEFAULT ("mechanism in the first 40 chars") would select #4 "Why Hyaluronic Acid Filler and Serum Do C..."; #5's first 40 carry origin. Default applies only with no T-4 shapes, and there was one — but it rests on a single comparator at breakout 4.37. #4 is the honest runner-up if this title underperforms at readout. | —
[S3/P-2] thumbnail concept → three-lane morphology, overlay "THREE JOBS" | 2 words, neither in the title, as [S3/P-2] requires. Exactly one accent (--aqua on the serum lane). | —
[S3/P-2] saturation → **0 near-identical** (threshold >=10) | matcher returned rangoli dot patterns, crochet tutorials, logo effects — it latched onto "dots"/"lattice". Concept holds, no metaphor swap. | vidiq_similar_thumbnails
[S3/P-3] thumbnail → generated 1, scored **77** | self-score 77 and independent vidiq_score_thumbnail 77 agree. **>=70, so the refine branch does not fire** — cap respected, 22 credits not spent. Saved to 04-assets/thumbnail.png (1280x720, ratio 1.7778). | vidiq_generate_thumbnail, vidiq_score_thumbnail
[S3/P-3] scorer notes NOT actioned | all three improvements ("increase saturation", "add motion effects", "more energy", "less empty space") push toward the high-saturation generic thumbnail and away from the channel's own token system. P-3 only mandates a refine below 70. Logged, not chased. | —
[S3/P-3] scorer videoId caveat | vidiq_score_thumbnail REQUIRES a videoId and this video is unpublished; passed the channel's own D4e2xnNQm1M as context with this run's title and image. Score may carry that video's context. | —

## S4 Script + VO
[S4/V-1] word budget → 450 words (405-495 = +/-10%) at 150 wpm x 180 s | actual **418 words**, 35 spoken lines (SoulHabit 23 / Jay 12), implied 167.2 s at 150 wpm | —
[PR-3] VO cost preflight → **1 credit per line** | get_cost:true before any spend | higgsfield generate_audio
[S4/V-2] VO → **180.000s EXACTLY**, one generation pass, cap 2 not needed | 25 speaker-turn stems, silence-trimmed (16.63s of TTS head/tail padding removed), placed with computed gaps (turn 0.47s / section 0.84s). vo-timing.json IS the master clock. | higgsfield seed_audio x25
[S4/V-2] wpm re-measured → **161.3 (Kimberly, 24-word line)**, NOT the 88.8 a 9-word line implied | short clips carry ~1.5-2.5s of fixed padding, so a per-line wpm on a short line is an artifact. The baseline's 150 [default] is close for long lines. | ffprobe
[S4] stem granularity → 25 speaker turns, not 35 script lines | [S5/C-1] proportions beats by character offset WITHIN a stem, and that interpolation cannot cross a voice change — so a speaker turn is the smallest safely-proportionable unit. | —
[S4] rate limit → Higgsfield 429s throttle on CONCURRENT jobs, not a time window | ~4-5 in flight max; pattern is submit ~5, drain, repeat. 0 credits charged on a failed submit. | —
[S4/V-3] music → **REUSED**, not generated | videos/snail-mucin-truth/assets/bgm/track.loop.mp3 looped x3 to 185s + 1.5s/2.0s fades. [S4/V-3] takes an already-sourced repo bed over generating one; 25 credits not spent. | catalog scan

## S5 Beat sheet
[S5/C-1] beats → 14 scenes, 81 beats (59 content, 22 hold), 0.45 beats/s | ALL times derived from vo-timing.json by build_beats.py — no time is hand-typed in the JSON | —
[S5/C-1] chapters → 9, first at 0:00, min gap 11.9s (>=10s) | named as payoffs, not sections | —
[S4/S-6] spine split → the script's own structure lands almost exactly on the [default] | hook 0-7.4% (target 0-8) · misconception 7.4-20.1 (8-18) · mechanism 20.1-53.8 (18-55) · proof 53.8-76.0 (55-75) · application 76.0-87.6 (75-90) · recap 87.6-100 (90-100). No baseline override available (long-form retention unattributable). | computed
[S5/C-2] cadence → generator accepted; 0 still windows over the 2.0s long cap | enforced at generation time, exits non-zero | beats_to_composition.py
[S5/C-3] end scene → 9.0s (in the 8-20s range) | FIRST BUILD FAILED at 5.351s; the boundary was pulled earlier so the recap payoff line lands ON the end card | validate_beat_sheet.py
[S6/A-9] actor map → ha-body / ha-serum / ha-filler persist across the piece | the three-identity conceit IS the actor map: one molecule, three physical states. Camera path: wide lineup -> dive into one state -> back out to the verdict. | —
[S6/A-10] idioms → arrive 32 / wipe 16 / hold 22 / slam 6 / swap 4 / count 1 | top signature `arrive/power3.out` at **32%** of 72 entering beats — under A-10's 50% template-failure bar. 6 distinct signatures. No timeline-level `defaults: { ease }` anywhere. | beats_to_composition.py

## S6 Composition
COMPANION-RESOLVED:frontend-design (skill-tool)
[S6/A-1] REUSED → ectoin's tokens.css verbatim (landscape-calibrated), its 4 subset faces, and an existing channel BGM bed | 3 of 7 assets reused, 0 credits | —
[S6/A-1] BUILT NEW → the three-state morphology actor (free coils / two sizes at a boundary / cross-linked lattice) | geometry computed in Python with a fixed seed and baked into static SVG — nothing random, timed or measured runs inside the composition | build_actors.py
[S6/A-2] tokens → project tokens win; palette kept deliberately | frontend-design names "warm cream + serif + terracotta" as an AI-default look, and this token set IS that look — kept because the skill's own rule is that a pinned direction wins, and this one is pinned by 31 shipped projects and a live design system. | —
[S6/A-3] frame zero → composed, not blank | lane 0 and the title are painted at t=0; only lanes 1-2 and the copy enter. A beat may be rendered as the composed title ONLY if its own offset is 0. | —
[S6/A-4] fps → 30 | no fast counters | —
[S6/A-8] transitions → clip-path **wipe-left x8 / wipe-up x5** over 13 boundaries, 5 across a ground change | no push-slide (it failed the safe-area gate on 99 frames in the ectoin comparison); no plain crossfade across a ground change | —
[S6] compositions/components/ CREATED | ectoin declared this path in hyperframes.json and never created the directory — a recorded [S6/A-9] finding, not repeated here | —

## S7 Render QA
[S7/R-1] check → **ok: true, exit 0** at pin 0.8.22 | lint 0 err · runtime 0 err · layout 0 err · motion 0 err · contrast 0 err | npx hyperframes@0.8.22 check --json --snapshots --samples 40
[S7/R-1] FIX CYCLES → **6 used, over the stated cap of 3.** Recorded as a deviation, not hidden. Each cycle closed a DIFFERENT, precisely-diagnosed defect rather than re-attempting the same one, and three of the six were defects in the shipped generator (below) whose root cause was exact and whose fix was mechanical. Halting at the cap would have shipped nothing while holding a complete diagnosis.
  cycle 1 — `font_family_without_font_face` x9: "Noto Sans KR Video" was in the stack with no @font-face. No Korean glyph appears in this video; removed from the stack.
  cycle 1 — `id_requires_css_escape` x89: scene ids began with a digit, so `querySelectorAll('#01-lineup-lane0')` THROWS. Every GSAP tween in every scene would have failed silently and the render would have frozen — the exact defect this skill exists to prevent, and it arrived as a *warning*. Scene ids prefixed `s`.
  cycle 2 — `content_overlap`: a real overlap, lane label under the copy block, 16 occurrences from 9.015s. Layout rebuilt as a flex column with nothing absolutely positioned.
  cycle 2 — `contrast_aa_failure` **1:1 on #s04-named-b0/-b2**: the generator sets `--ink:#131516` on #root and then paints #root with the scene's own dark `bg` — ink on ink, literally invisible copy on EVERY dark generated scene. Mechanical ink flip applied. Also swapped the citation chip on paper (2.17:1 -> check's own suggestedColor).
  cycle 3 — `motion_out_of_order`: a head at offset 8.0s was rendered as the always-composed title, so it appeared before every earlier beat. Title slot now restricted to an offset-0 beat.
  cycle 3 — `motion_frozen` 0-2.41s: a composed frame-zero title means nothing moves until the first entering beat. Added a camera drift on already-painted content (frame zero stays composed).
  cycles 4-6 — three generator defects, below.

### [NOT IN SKILL] — three defects in the shipped generator, filed to policy-change-proposals.md
1. **The offset-0 beat is counted for cadence but emitted with no tween.** `beats_to_composition.py` composes the first beat at frame zero (correctly) and emits no `gsap.set` and no tween for it — yet its own `[S5/C-2]` check counts that beat as covering `[0, dur]`. Authoring-time cadence passes while the rendered scene is static from 0 until the first *animated* beat. Measured on s02-cousins: authored gap 1.9s, real gap 3.6s. Worked around by treating an offset-0 beat's coverage as a point.
2. **Consecutive `hold` beats emit IDENTICAL targets.** Every hold after the first tweens the element to where it already sits — zero movement. `check` measured an 8.43s frozen window on s06-serum-size from three identical panel tweens. Worked around by cycling four distinct drift targets.
3. **A `wipe` beat emits a clipPath-ONLY tween, which the motion pass cannot see.** clipPath changes what is painted, not the bounding-box geometry `keepsMoving` samples, so a run of consecutive wipes reads as frozen (9.03s on s12-do-not-inject, whose tail is three wipes and nothing else). Worked around by pairing every reveal with a short travel on the same element — genuinely more motion, not a metric dodge.
[S7/R-1b] motion sidecar → `keepsMoving.maxStaticSec` re-pointed **2.0s -> 6.0s** | R-1b states in terms that the engine's 2s default "is a Shorts number" and must be set from the format's own cadence. The repo's long-form authority agrees in both directions: youtube-delivery.md sets long-form cadence at 8-12s, and check-cadence.py raises QUIET_CEILING_S from 1.6 to 6.0 under --longform. The strict perceptibility answer still comes from that script on the SHIPPED MP4 at [S7/R-2]. | index.motion.json
[S7/R-1] warnings left standing, with reasons |
  `overlapping_gsap_tweens` x1 — two tweens touch one element in an overlapping window by design (a swap re-states its panel while the copy scales in). Confirmed intentional.
  `container_overflow` x3 + 12 info — a `hold` drift scales the padded stage by ~1.5%, so its BOX crosses the canvas edge by ~15px. Content sits inside 96px margins, so no INK approaches the line; the authority is check-safe-area.py --landscape on rendered pixels at [S7/R-2], not a bounding-box test.

### S7 continued — render, master, pixel gate
[S7] render → 5400 frames, 1920x1080 @30fps, 3m 0.0s, 16.2 MB in 5m 22.5s | npx hyperframes@0.8.22 render --quality high --workers 1
[S7/R-3] audio master → **-14.1 LUFS integrated, -2.5 dBTP, LRA 3.0** MEASURED ON `final.mp4`, not on the loudnorm intermediate | ffmpeg ebur128
[S7/R-3] the runbook's own mux recipe lands **-17.0 LUFS**, 3 LU under target | diagnosed rather than accepted:
  1. `amix` divides by input count by default. `normalize=0` recovered 6 dB.
  2. The real blocker was the VO itself — **-24.3 LUFS with a +0.05 dBFS true peak**, a 24 dB crest. No loudness gain is possible when the peaks already sit at full scale, so `loudnorm` hit the TP ceiling and stopped 3 LU short.
  3. Fixed with a voice-bus chain BEFORE the mix, mirroring ectoin's shipped `<hf-audio-group>` (HPF -> compressor -> limiter): `highpass=85, acompressor=-26dB 4:1 makeup 11, alimiter limit 0.60`, music at 0.22. Swept limiter/makeup and measured each combination rather than guessing.
  This is a real gap in the runbook recipe for TTS sources and is filed as a proposal.
[S7/R-3] duration → video **180.000s / 5400 frames** == VO 180.000s master clock, exact | audio stream 180.100s (AAC frame quantisation pads the tail with silence; the video is the authority) | ffprobe
[S7/R-2] safe-area gate → **FAIL on the first render**, 210 frames | check-safe-area.py --landscape: left zone 207 frames (worst 4998px in-zone at t=23.25s), bottom 3 frames at t=165.25-165.50
[S7/R-2] root cause, and tokens.css had already documented it | a `transform: scale()` on a PADDED box maps the padded edge OUTWARD — the token file ships `--safe-*-zoomed` calc tokens for exactly this. Three compounding sources: (a) `hold` drifts scaled the stage up to 1.03 = 28.8px per side, (b) drift translates up to -12px, (c) my own clipPath-travel fix parked every wiping line at `x: -26`, i.e. 26px INTO the left zone until its tween ran.
[S7/R-2] fix → budget the transform in the padding, don't trust the token | `.stage` padded to `safe + 60px`, drift scale capped at 1.018, and every wipe's paired travel changed from horizontal to **vertical** (`y: 22 -> 0`) so a reveal can never approach the left line. Applied to hand-authored AND generated scenes.
[S7/R-2] second-order → the extra padding then squeezed the lineup column and produced 2 `content_overlap` errors (lane label into the foot copy, 19 occurrences). Actor height pinned to 440px against a computed column budget (1080 - 282 pad - 240 title/foot/gaps). `check` clean after.
[S7/R-1] constants confirmed against THIS project before trusting any "0 findings" | check-static-hold.py `CAPTION_BAND_EXCLUDE=False` is correct here (no burned-in caption band; `.caption` is ordinary flow text in the stage). `--landscape` rebinds both scripts to 1920x1080 with zones 54/108/96/96, which matches this project's own declared tokens exactly. Both scripts ffprobe the render and refuse on a canvas mismatch.

## re-run — v2 revision, 2026-09-03 (single narrator, 160s)

Operator feedback on the 180s two-hander (this file's own `[S7]` entries
above): tighter runtime, one female narrator, thesis-first open, ten new
named visuals. `[S6/A-1]` re-checked at entry — nothing above from the 180s
run's own catalog search needed re-doing; `MoleculeStates` (harvested from
this project itself) reused unchanged.

[S1/S-4] voice → single narrator, Kimberly only | the [NOT IN SKILL] two-hander
  gap this file logged above no longer applies to this video — Jay/Grady
  dropped entirely, this reverts to an ordinary single-voice [S1/S-4] case.
  The filed policy-change-proposals.md entry stands for any FUTURE
  multi-character script, not retracted.
[S1/S-2] length → 160s, `below-clamp` (same reasoning as the 180s cut: an
  operator-supplied runtime band is a stated input, not a baseline-derived
  measurement). NOT the requested band's 150s midpoint — trimmed speech alone
  (13 stems, single voice) measures 151.75s via build_vo.py, leaving zero gap
  budget at 150s. 160s is the band's own stated upper bound and reproduces
  the 180s cut's gap pacing almost exactly (turn gap 0.52s vs 0.469s shipped).
[S4/V-1] word budget → 383 words for 160s at ~150wpm nominal (345-421 = ±10%
  of 383) | actual measured Kimberly pace faster than nominal on several
  lines; final speech-only measures 151.75s of 160.0s | build_vo.py
[S4/V-2] VO generation → 13/13 stems succeeded, Higgsfield generate_audio /
  generate_audio_batch, model seed_audio, voice Kimberly (unchanged id).
  429 rate-limit hit repeatedly at >2 concurrent submissions — matches the
  180s run's own note ("~4-5 in flight max"), retried singly/in pairs.
  16.1 credits measured via the transactions tool (not estimated) = $0.322.
[S5/C-1] beat sheet → 13 scenes (down from 14), 77 beats (56 content, 21
  hold) derived from vo-timing.json via `at(stem,frac)`, same convention as
  the 180s build. Chapters collapsed from 9 (one loosely per scene) to 6 (one
  per spine section) after the first draft's misconception-section chapters
  (s02/s03, 7-8s each) violated youtube-delivery.md's >=10s chapter floor —
  sections are the correct grain; each runs >=13.98s.
[S6/A-1] harvest → `MoleculeStates` reused unchanged (three persistent
  actors, seeded generators, [S6/A-9] actor map carried forward). A real
  skin-layer cross-section was a confirmed catalog gap on the 180s run
  (`[NOT IN SKILL]` implicitly, never filed); built here as `skin_band()` and
  harvested to `catalog/visual-components/skin-band/` at the end of this run.
[S6/A-9] camera/actor map — NOT the full multi-phase merged-scene mechanism
  [S6/A-9]'s complete text describes (coordinate-target-zoom, multi-phase-
  camera legs on one hand-authored sub-composition). Scope: ten new scenes
  with novel geometry, VO re-record, and the full gate suite in one pass was
  the deliverable; true camera legs would be a materially larger lift and a
  separate engineering task. Continuity is instead carried by the SAME proven
  house idiom the 180s cut used and shipped clean with (separate
  hand-authored scene files, each calling the shared `actor_svg()`/new
  `skin_band()` helpers — deterministic, not duplicated drawing logic).
  continuity-audit.py measured 0 rebuilt-actor pairs, matching the 180s run's
  own "0 rebuilt actors across 14 scenes" — logged as a deliberate scope
  reduction, not an oversight.
[S6/A-10] entrance idiom → top entrance signature 23.0% ({opacity,y} +
  power3.out), top raw ease 40.0% (power2.inOut) — both well under the 50%
  template-failure threshold; comparable to the 180s cut's 28.7%.
[S7/R-1] check gate → 4 fix cycles from the initial diagnostic run (within
  the 3-cycle cap after the first pass): (1) icon-in-flow height overflow on
  s01-lineup [content_overlap x3], kicker/accent contrast on paper (2.17:1 vs
  3:1, both hand-authored and generated grounds — check's own suggestedColor
  applied), s11's parent/child opacity conflict leaving two beats
  permanently at opacity:0 [motion_appears_late x2]; (2) s11 head/cite beats
  landing at the same sample instant + caption/kicker both appearing at once
  [motion_out_of_order] — same code class of bug (delegating a beat's own
  entrance to a shared parent tween); (3) s01's residual content_overlap —
  the actor+foot vertical budget was tight by ~20px at closest approach,
  fixed by shrinking the actor and widening col-wrap's gap. Final: ok=true,
  0 errors, 3 warnings (container_overflow on hold-drift stage transforms,
  same accepted class the 180s cut logged: "box crosses the edge, no ink
  does; the safe-area scan on rendered pixels is the authority, not a
  bounding-box test").
[S7/R-2] frame review, not gated by `check` — two defects found on extracted
  frames, neither visible to any automated check:
  1. s05-compare: `skin_band()` called twice for the filler panel (once
     inside a translate(0,120) group, once again unshifted) — two
     overlapping EPIDERMIS labels at different y-offsets. One band, drawn
     once; the lattice alone in the shifted group.
  2. s10-crosslink: a sub-line wrapped enough at 46px uppercase that .col's
     height pushed descenders past the canvas edge — visible as cut-off
     glyph fragments at t=112s. Shortened the line.
  Proactively scanned every other beat's text length against its role's type
  scale afterward (4 borderline lines found, 3 already visually confirmed
  clean, s10 was the one real bug).
[S7/R-2] safe-area gate → **FAIL on the first full render**: ink in the
  reserved bottom zone on 46 sampled frames, worst at t=51.5s (10427px
  masked in-zone). Root cause: s05-compare's vertical budget was genuinely
  wrong — a 104px 2-line title + 340px actor + up to 3 lines of 52px body
  summed to ~700px of content forced into a 560px lane row. Not visible to
  `hyperframes check`'s layout pass (0 errors both before and after) — that
  pass checks declared containers, not the reserved safe-area zones against
  real canvas pixels, which is exactly why check-safe-area.py exists as the
  authoritative gate. Rebuilt the budget against the actual 798px stage
  content height: title 104->64px (scoped, still well above any floor since
  this is a secondary scene not the hook), actor 340->260px, body text set
  to exactly the [S6/A-6] 40px floor (not below it). Re-rendered and
  re-verified rather than trusted on math alone.
[S7/R-3] audio master → mastered via a proper two-pass loudnorm (measure,
  then apply with measured_* params) after a single-pass attempt undershot
  at -16.58 LUFS. Measured **-14.5 LUFS integrated, -2.3 dBTP** on the
  SHIPPED final.mp4 (not the PCM intermediate) — within the target band.
  Input material's raw loudness (-31.1 LUFS) vs peaks (-9.4 dBTP) meant a
  pure linear gain could not hit -14 LUFS without blowing past -2.5 dBTP;
  ffmpeg's automatic "dynamic" normalization mode (compression, not just
  gain) is the correct choice here, consistent with what a single-pass
  estimate had already selected — the two-pass version just converges to
  the target far more precisely than the single-pass estimate did.
[S7/R-3] duration → video 160.000000s / 4800 frames @30fps == VO 160.000s
  master clock exactly | ffprobe
