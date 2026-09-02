# Decision Ledger — 2026-09-01 · how-to-repair-skin-barrier

Dry run of `faceless-video-craft` **v2.1**, stages S1→S7, on the Centella brief
(`videos/centella-tiger-grass/BRIEF.md` + `STORYBOARD.md` + `frame.md`).
**No question was put to the operator during the run.** Nothing published.

Two halts fired. Both are recorded below at the point they fired, with the
`[NOT IN SKILL]` line each produced.

---

## S0 — Baseline

```
[S0/B-1] baseline fresh (updated 2026-09-01) → skip S0 | channel-baseline.md
[S0/B-2] one authorized channel → UCzqEGQ9uAU43AgyxGtLT7MA (@SeoulHabit) | vidiq_user_channels
```

## S1 — Story

```
[S1/S-1] format → short | branch 1 (run input: BRIEF frontmatter destination=shorts, aspect 1080x1920)
         branch 2 concurs: short = 46 of 48 uploads_90d = 95.8% ≥ 60% | channel-baseline.md
[S1/S-2] target 45 s [default], clamp 30-58 s | retention.median_duration_top_quartile_curve_s
         is null → baseline-field-missing. Measured VO landed 46.24 s, inside the clamp.
[S1/S-3] presenter → moving-diagram (mechanism-heavy: inflammation signal, fibroblast activation)
         → RE-FIRED to kinetic-type, see BLOCKER-TOOLING below
[S1/S-4] voice → SAz9YHcvj6GT2YYXdXww "River - Relaxed, Neutral, Informative"
         chain: no project skill → baseline voice null → first vidIQ voice whose name
         contains "neutral" | vidiq_voiceover_list_voices
         DIVERGENCE, logged not halted: BRIEF.md names Kimberly via Higgsfield as the
         standing series convention. S-4's chain has no run-input branch, although
         SKILL.md's operating contract lists voice as an accepted override.
[S1/S-5] spine → hook ✓ | misconception ✓ | mechanism ✓ (unsourced) | proof [UNGROUNDED]
         | application ✓ | recap folded into application (short). Proof DROPPED.
[S1/S-7] route faceless-explainer → angle=concept | length=45 s | destination=9:16 |
         VO_MODE = restructure per scene (no SCRIPT.md exists in the project)
         angle: the rule and the brief's own frontmatter agree independently.
[S1/S-8] pitch round → winner shape "why X, symptom-first, viewer as grammatical subject"
         (T-4 rank 1, breakoutScore 406.7)
```

### `[K-*]` claims — RESOLVED BY RULE (was `BLOCKER-CLAIM`)

The first pass of this run **halted** here: v2.1 had no rule for whether an
unsourced health claim may render, and the run resumed under an operator
assumption. `decision-policy.md` §Claims (`K-*`) has since been written, and the
run was re-executed under it. There is no assumption left in this ledger.

```
[K-1] claim inventory -> 01-story-brief.md §Sourcing | 11 rows classified
      nominal 2 | sourced 0 | unsourced 4 | editorial 3 | illustration 0
      Proof stays [UNGROUNDED] per [S1/S-5]: no Centella source records exist
      in this system and no citation id may be invented.
[K-2] 4 unsourced claims render, each attributed AND carrying a concurrent flag:
      misc-b | comp-b | mech | apply -- flag beat at offset 0.000 of each scene,
      muted #9B9A97, never the accent, never citation typography.
[K-2a] hard prohibitions -> NONE TRIGGERED. Nothing cut.
      "Cica daily, on damp skin" assessed against the safety bullet: cica is a
      non-active, so this is a low-risk usage instruction, not active dosing.
      It stays an unsourced claim needing attribution + flag, which it has.
[K-2b] ratio limb -> FIRED. Mechanism+Proof: sourced 0, unsourced 4.
      unsourced >= sourced -> disclosure-forward REQUIRED. The narration states
      the absence of sourcing outright; badges do not carry it alone.
[K-3] attribution verbs in BOTH lanes, on-screen hedging at least as far as VO:
      "commonly described as" | "described as" | "said to" | "the usual advice"
[K-4] rendered-claim check -> PASS on extracted frames (see S7 below)
[K-5] envelope carries the posture in the description and pinned comment
```

**What the rule changed about the video.** The first pass opened on
"Your skin isn't sensitive. It's a broken barrier." — an unsourced diagnostic
claim asserted as fact at frame zero. `[K-2]` does not permit that, and the fix
is the question form: "Is your skin actually sensitive? / Or is the barrier
damaged?" That form is independently supported — it is T-4 shape rank 3
(breakoutScore 271.05), the second-highest-scoring relevant shape in the
channel's own outlier set. The rule and the data pointed the same way.

Three further sentences moved from asserted to attributed, and four scenes
gained a concurrent flag they did not have.

### BLOCKER-TOOLING — fired between `[S1/S-3]` and `[S6/A-1]`

```
[NOT IN SKILL] scripts/beats_to_composition.py emits two of the four presenters
S-3 can select: kinetic-type and photographic-plate. moving-diagram and
data-object have no emitter, so S-3's own output cannot be built by the
generator. [S6/A-1]'s fallback clause ("re-fire S-3 with presenter = kinetic
type") is scoped to PLATES being unobtainable, not to a tooling gap.
```

Resolution taken: re-fired S-3 to **kinetic-type**, the nearest rule-consistent
action, so the composition stays fully generated from the beat sheet rather than
hand-authored. Logged as a fallback. The cost is visible in the render — see
§What this did not achieve in the report.

## S2 — Topic gate

```
[S2/T-1] seed → "centella damaged skin barrier"
[S2/T-2] FAIL → SWAP → "how to repair skin barrier" | vidiq_keyword_research(mode=research, US)
         seed: volume 0, overall null, monthly searches <750 ("Very low") — fails both limbs.
         Highest-overall related was "skin1004 centella ampoule" (67.85) — REJECTED under
         T-1 (brand name, and the brand is not the subject).
         Adopted: "how to repair skin barrier" volume 54.9, competition 24.4, overall 63.18,
         est. 4,762/mo. PASS on overall ≥ 50.
[S2/T-3] PASS | minSubscribers=0, maxSubscribers=max(10 × 8, 10_000)=10_000 — both bounds logged
         top 3: gmRACLKgG9g breakout 406.7 (2,730 subs, 54,905 views, 109 s short)
                l3mwJaD9dIk breakout 302.64 (off-topic)
                Vq2Vu2yFOxE breakout 271.05 (610 subs, 50,148 views, 30 s short)
         NOTE: 10 × subs alone would have been 80. The floor is what made this call answer.
[S2/T-4] title_shapes[] → 1 why-X symptom-first, viewer as subject (406.7)
                          2 superlative + fix (302.6, off-topic)
                          3 second-person question accusing a routine step (271.1)
                          4 number/price + second person (226.6)
                          5 experiment/consequence (165.2, off-topic)
         Shapes 1 and 3 both put the VIEWER in the opening words. Convergent with the
         2026-09-01 audit's finding 1 on the original video.
```

## S3 — Packaging

```
[S3/P-1] winner → "Why your skincare stings: how to repair skin barrier" (51 chars)
         selected by T-4 shape rank 1; score 87 logged, not obeyed | vidiq_score_title ×5
         | 92  "4 compounds in tiger grass: how to repair skin barrier"     shape rank 4
         | 88  "Is your exfoliant the problem? How to repair skin barrier"  shape rank 3
         | 87  "Why your skincare stings: how to repair skin barrier"       shape rank 1  ← WINNER
         | 83  "Over-exfoliated? How to repair skin barrier with cica"      shape rank 5
         | 82  "Sensitive skin vs damaged: how to repair skin barrier"      no T-4 shape
         SCORER INVERSION #3: the top score went to shape rank 4. Two prior instances
         (2026-08-31 and 2026-09-01) are why P-1 logs the score instead of obeying it.
         Evidence for [S9/L-2]; packaging.title_scorer_discriminative stays false.
[S3/P-2] concept → frame zero: the claim "Your skin isn't sensitive." set as the whole frame
[S3/P-3] n/a — Shorts use frame 0 as the thumbnail. No generation, no score. 0 credits.
[S3/P-4] tags → seed + related with overall ≥ 30 (7 qualify); description in 07-publish-envelope.md
```

## S4 — Script and voiceover

```
[S4/V-1] word budget 45 × 150 / 60 = 112.5, ±10% → 101-124. Actual 108 words / 672 chars.
[S4/S-6] split, Proof dropped: hook 0-10% (max 3 s) | misconception 10-25% |
         mechanism 25-85% | application 85-100%
         Proof's 65-85% band reallocated to Mechanism. INFERRED from S-6's own baseline-
         override direction ("lengthen Mechanism"); S-5 does not say how to reallocate a
         dropped section's time. Flagged, minor.
[S4/V-2] VO 44.320 s measured on the file (tool reported 44.356 s), 667 chars,
         1 generation. Target 45 s ±15% = 38.25-51.75 s → PASS. 46.24 s IS THE MASTER CLOCK.
         | vidiq_voiceover_generate → vidiq_job_poll | 14 credits ×2 (the K-3 rewrite
         required a second generation; the first is superseded, not kept)
[S4/V-3] music → REUSED, 0 credits | videos/madecassoside-flat-matrix/assets/bgm/track-pulse.wav
         62.16 s house bed, in use across 4 prior projects. [S6/A-1] reuse-before-rebuild
         applied to audio, not only imagery. No vidiq_generate_music call (saved ~25 credits).
```

## S5 — Beat sheet

```
[S5/C-1] 9 scenes, 34 beats. Beat and scene times = proportional character offset × 44.320 s.
         Hook beat starts at 0.00. Scenes tile the timeline exactly; total 46.240 s.
[S5/C-2] cadence enforced by the generator at generation time. 0 scenes rejected.
         Hook section runs 0-3.372 s against S-6's "max 3 s" — a 0.372 s overrun the VO's
         own pacing produced. The VO is the master clock; logged, not corrected.
[S5/C-3] n/a — short. Last scene hands back to frame zero's ground (both #101314).
```

## S6 — Composition

```
[S6/A-1] catalog searched: catalog/visual-components/{barrier-wall, unsourced-flag,
         term-definition, split-compare, factor-converge, stat-reveal, frosted-panel, …}
         and catalog/tooling/. Also every videos/*/assets/bgm/.
         REUSED: the house BGM bed (see V-3); catalog/tooling/check-safe-area.py and
                 check-static-hold.py as the S7/R-2 gates rather than rebuilding them.
         NOT USED: BarrierWall — the presenter is kinetic-type, not a diagram.
         HARVESTED BACK: UnsourcedFlag's convention is now a first-class `flag` beat role
                 in scripts/beats_to_composition.py, rendered in muted ink and explicitly
                 never the accent colour — a flag borrowing the accent reads as a citation.
                 Available to every future run instead of being re-derived per project.
[S6/A-2] tokens from videos/centella-tiger-grass/frame.md (project spec wins):
         ground #101314, ink #F7F5F0, aqua #59B8AE, celadon-bright #93B896, coral #C97A5C,
         muted #9B9A97. One accent per frame; coral spent once (the application scene).
[S6/A-3] spatial plan: every scene is one flex column, centred, inside the safe box
         (192/384/162/72). Frame zero verified by extraction, not by reading.
[S6/A-4] 30 fps, 1080×1920
[S6/A-5] box-sizing: border-box emitted as the first rule in the root + all 12 scenes
[S6/A-6] smallest declared type 34 px (kicker, flag) ≥ the 32 px absolute floor.
         Body 58 px ≥ the 40 px reading floor. Hero 112 px inside 96-160 px.
[S6/A-7] see S7/R-1 contrast pass. Hero-visual clause n/a — no hero visual in this cut.
```

## S7 — Render QA

```
[S7/R-1]  npx hyperframes@0.8.22 check --json --snapshots → ok: true
          lint 0/0 · runtime 0/0 · layout 0/0 · motion 0/0 · contrast 0/0
          FIX CYCLES USED: 0 of 3.  Envelope: 06-render/check.json
[S7/R-1b] motion sidecar index.motion.json, 44 assertions (31 appearsBy + 13 before),
          emitted by the generator in the same pass as the markup. Motion pass 0 errors.
[S7/R-2]  render -> 06-render/raw.mp4 (44.3 s, high, 1 worker)
          catalog/tooling/check-safe-area.py  -> PASS, 177 frames, no reserved-zone ink
          catalog/tooling/check-static-hold.py -> whole-frame: no findings, 89 frames
                                               -> region-aware: 3 content-voids, verified
                                                  FALSE POSITIVE by extraction (centred
                                                  column; top/bottom cells empty by design)
          CONSTANTS CONFIRMED: CAPTION_BAND_EXCLUDE = False is correct -- no beat uses the
          caption role, so this project has no burned-in caption band.
          FRAME ZERO -- REGRESSION FOUND AND FIXED. The first re-cut split the hook question
          across two scenes, so frame zero read "IS YOUR SKIN" alone: not a complete thought,
          and a breach of mandatory rule 5. Caught by extracting the frame, not by reading the
          beat sheet -- check passed 0/0 on the broken version. Hook merged into one scene;
          frame zero now carries the complete question.
          Hangul 병풀 renders with no tofu. Flags render muted and distinct from their claims.
[K-4]     rendered-claim check on the same frames -> PASS
          every unsourced claim shows its flag concurrently (flag at scene-local 0.000);
          flag is var(--muted) #9B9A97, never var(--accent); no internal record id anywhere
          (grep ING- across 05-composition: none); on-screen wording hedges at least as far
          as the VO at every checked timestamp; nothing hard-prohibited appears.
          Frames: 12.5 s (misc-b), 26.0 s (comp-b), 33.0 s (mech), 43.5 s (apply).
[S7/R-3]  two-pass loudnorm, TP=-2.5 (not -1.5), measured on the SHIPPED file:
          integrated -15.2 LUFS · true peak -2.2 dBFS
          The headroom rule works: v1's confirmed defect was TP=-1.5 shipping at +0.5 dBFS.
          duration: video 44.333 s vs VO 44.320 s → Δ 0.013 s, inside ±0.1 s. PASS.
```

### Defect found in `scripts/extract_frames.sh` — found by pixels, fixed

The script derived duration from `format=duration`, which on a muxed file is the
**longest stream**. Here audio ran 46.300 s against video 46.267 s, so the
last-frame seek landed 33 ms past the final video frame: ffmpeg wrote nothing and
**still exited 0**, so `set -e` never fired and `frame-last.png` was silently
absent. Fixed to read `stream=duration` from the video stream, back off 0.10 s,
and treat a zero-byte output as a hard failure. Re-run produced the frame.

This is the skill's own rule turning on the skill's own tool: the manifest said
the frames were extracted; the directory listing said otherwise.

### `[NOT IN SKILL]` — R-3's two targets can conflict

```
[NOT IN SKILL] [S7/R-3] states both "-14 LUFS integrated" and "TP=-2.5 headroom"
without saying which wins when they conflict. This mix cannot reach -14 LUFS
under a -2.5 dBTP ceiling: input integrated -25.55 with true peak -7.14 needs
+11.55 dB, which would put the peak at +4.41. loudnorm therefore lands at
-15.4 LUFS. Resolution taken: HEADROOM WINS — a file 1.4 LU quiet is left alone
by the platform, a file at +0.5 dBFS clips. Needs to be written as a rule, with
the alternative (compress before limiting) named.
```

## Credits spent

| Call | Count | Credits |
|---|---|---|
| `vidiq_user_channels` (preflight) | 1 | 0 |
| `vidiq_balance` | 1 | 0 |
| `vidiq_keyword_research` | 1 | 5 |
| `vidiq_outliers` | 1 | 5 |
| `vidiq_score_title` | 5 | 25 |
| `vidiq_voiceover_list_voices` | 1 | 0 |
| `vidiq_voiceover_generate` (672 / 667 chars) | 2 | 28 |
| `vidiq_job_poll` | 3 | 0 |
| **Total** | | **63** |

Ceiling is 200 pre-production. No `budget-reduced` path taken. S0 skipped
(baseline fresh) saved ~30; music reuse saved ~25; Shorts-use-frame-0 saved the
thumbnail generation and both thumbnail scores; P-1's cut from ~10 title scores
to 5 saved ~25.

## Standing-rule compliance

Nothing published. No `vidiq_update_video`, no metadata write, no upload. No
invented numbers — every unavailable metric is written `not available via vidIQ`
or `null`. `videos/centella-tiger-grass/` was read and not modified. Two halts
were reported at the point they fired rather than improvised past; one was
resumed under an explicitly labelled operator assumption, which is recorded as an
assumption and not as a rule.
