# Channel baseline — measured numbers (rewritten by S0 and S9)

```yaml
populated: true
updated: 2026-09-01
channel:
  id: UCzqEGQ9uAU43AgyxGtLT7MA
  handle: SeoulHabit
  subs: 8                       # channel created 2026-07-07; 2,693 lifetime views
corpus:                         # merged from the root analysis doc, 2026-09-02
  uploads_total: 48
  shorts: 46
  long: 2                       # a 34s clip and a 48s ex-livestream, BOTH private
  public: 14                    # the only uploads carrying a distribution signal
  unlisted: 1
  private: 33
  # Private/unlisted view counts reflect no algorithmic delivery and must never be
  # ranked against public ones.
  shorts_over_50s: 21           # of 46 — v1 SKILL.md's "14 of 23" is stale on both terms
views:
  # TWO SOURCES, NOT INTERCHANGEABLE. Never build a ratio with a numerator from one
  # and a denominator from the other — see curve.ratio_method below.
  public_median: 58             # n=14, vidiq_video_stats (lifetime public counts)
  public_median_ex_outliers: 45 # n=12, excluding the two >1,000-view videos
  public_mean: 211.8            # 3.6x the median — DO NOT USE on this corpus
formats:                        # window 2026-06-03..2026-09-01 (covers ALL uploads)
  long:  { uploads_90d: 2,  median_views_per_upload: null }   # both private; no public long-form
  short: { uploads_90d: 46, median_views_per_upload: 58 }     # median over the 14 PUBLIC shorts
traffic:                        # share of views, last 90 d, n=4756 views
  browse: 0.925                 # SHORTS feed 88.1% + YT_CHANNEL 3.8% + YT_OTHER_PAGE 0.5%
  suggested: 0.0025             # RELATED_VIDEO
  search: 0.042                 # YT_SEARCH
  external: 0.015               # EXT_URL
  shorts_feed: 0.881            # [S0/B-3] — 88.1% of all views; the four-slot schema had no room
  other: {}                     # no further labels returned
curve:                          # vidiq_channel_performance_trends — SHORTS, not long-form
                                # built from PUBLIC view counts, same family as
                                # vidiq_video_stats — NOT from channel_analytics
  p50_24h: 9.5
  p50_48h: 15.5
  perc30_48h: 7                 # noise-floor band, lower bound
  perc70_48h: 31.5              # was mis-named p75_48h; the tool returns perc70
  p50_7d: 25
  p50_28d: 28
  sample_n: 8                   # uploads the percentiles were computed from
  full:                         # merged from the root analysis doc, 2026-09-02
    #  age    p30   median   p70
    - [  "1h", 0.1,   1,      1  ]
    - [  "2h", 1.1,   2,      2.9]
    - [  "6h", 3.0,   6,      8  ]
    - [ "12h", 5.0,   6.5,   10.5]
    - [ "24h", 6.5,   9.5,   18.5]
    - [ "48h", 7.0,  15.5,   31.5]
    - [ "72h", 7.0,  21,     39.5]
    - [  "7d", 7.0,  25,     64.5]
    - [ "28d", 8.5,  28,    109  ]
  max_28d: 389                  # neither 1,000+ video is in the curve's own sample
  ratio_method: age-matched     # views ÷ the channel median AT THAT VIDEO'S AGE, not
                                # ÷ a fixed p50_7d. A fixed denominator understates a
                                # young video and overstates an old one; on d6DPiORuPO4
                                # the two methods give 0.82 vs 0.28. Use age-matched,
                                # and take the numerator from vidiq_video_stats so it
                                # matches the curve's own source.
retention:
  avg_view_pct_long: 43.07      # n=2, both private — not usable
  avg_view_pct_short: 61.28     # per-video median, n=34
  avg_view_pct_short_weighted: 38.26   # view-weighted, from the SHORTS traffic row
  avg_view_pct_median_per_video: 61.28
  median_duration_top_quartile_avp_s: 19      # LOGGED, NOT USED — see WARNING below
  median_duration_top_quartile_curve_s: 49.0  # [S1/S-2] short target. COMPUTED 2026-09-02
                                              # from the root analysis doc's age-matched
                                              # ratios: top quartile is 4 of 14 public
                                              # (2NGeQYjsR7Y 56s, D4e2xnNQm1M 42s,
                                              # Yc1hH5Bz4t8 42s, cGbokt_B_vE 116s),
                                              # median 49.0s — INSIDE the 30-58s clamp,
                                              # so no baseline-below-clamp fires.
                                              # CAVEAT: the quartile holds 4 videos, below
                                              # [S9/L-2]'s "≥ 8 in the quartile calc" bar
                                              # for replacing a [default]. Treat as
                                              # provisional; it is still measured, where
                                              # the 45s it replaces was not.
  replay_inflated_share: 0.176                # 6 of 34 shorts score >100% avg-view-%; max 603.86%
  first_drop_s: null            # audience_retention returns zero rows for this channel.
                                # This blocks the CURVE only. Per-video averageViewPercentage
                                # IS retrievable via channel_analytics(report=top_videos) —
                                # see the correction note below before recording retention
                                # as unavailable anywhere.
  section_curve:
    top:    []                  # not available via vidIQ
    bottom: []                  # not available via vidIQ
packaging:
  median_ctr: null              # not available via vidIQ (Studio only)
  title_scorer_discriminative: false      # [S3/P-1] — ranked the failing title above every
                                          # rewrite on 2 videos in 2 runs (95 vs 93/90/87;
                                          # 94 vs 83-87). Score is logged, not obeyed.
  median_title_score_top_quartile: null   # not measured; bar held open, see note
  median_thumb_score_top_quartile: null   # n/a — Shorts use frame 0
voice:
  id: null                      # vidiq_voiceover_list_voices not called this run
  words_per_minute: 150         # [default], unmeasured
music:
  track_url: null
best_publish_windows:           # vidiq_subscriber_insights, tz -04:00
  - { day: Friday,   start: 12, end: 15, activity: 63 }
  - { day: Friday,   start: 9,  end: 12, activity: 59 }
  - { day: Saturday, start: 0,  end: 3,  activity: 58 }
overrides:                      # [S9/L-2] write-back; append-only
  - field: duration_threshold_28_45s_with_50s_ceiling
    old: "diagnostic — >50s needs a reason"
    new: "craft budget only; NOT a performance threshold and NOT usable to rank a failure"
    date: 2026-09-01
    evidence: >-
      Age-normalised median ratio 4.38 (≤50s, n=6) vs 3.97 (>50s, n=8), against a
      within-cohort spread of 0.67-49.44 — two orders of magnitude, cohorts overlapping
      across nearly all of it. Raw counts favour the longer cohort, age-normalised
      counts favour the shorter; neither margin survives the spread. The corpus cannot
      distinguish the cohorts at all. This does NOT license the inverse: "shorter
      performs better" is exactly as unbacked. It flags d6DPiORuPO4 (0.82) and
      cGbokt_B_vE (8.85) identically.
    videos: [all 14 public]
```

## Reconciliation, 2026-09-02

Two `channel-baseline` files existed: this one (written by S0, schema-shaped, read
by the rules) and a 168-line analysis document at the repo root, written in a
separate session **before the v2 package was installed on this machine** — its own
header says its numbers were "ready to paste into v2's `references/channel-baseline.md`
once the package is available." This is that paste, plus three corrections.

**What merged in:** corpus composition, the full 9-row accumulation curve, the public
view distribution, `shorts_over_50s: 21`, the duration-threshold falsification as the
first `overrides[]` entry, and the previously-null
`median_duration_top_quartile_curve_s`.

**Correction 1 — the analysis doc's retention blocker was wrong.** It states, in two
places, that retention is "currently unobtainable via vidIQ" because
`audience_retention` returns zero rows, and rests its cadence and payoff-timing
conclusions on that. The zero rows block the **100-point curve only**;
`channel_analytics(report=top_videos)` returns per-video `averageViewPercentage`, which
is where every retention figure in this file comes from and which was re-measured
independently on 2026-09-02 (n=36). Those rows in the analysis doc are superseded.

**Correction 2 — two view-count sources, not interchangeable.** `vidiq_video_stats`
(lifetime public counts) and `channel_analytics` (a windowed YouTube Analytics figure)
disagree, sometimes hugely: `cGbokt_B_vE` reads 145 vs 32, `Yc1hH5Bz4t8` 162 vs 13.
The accumulation curve is built from the former. **A ratio whose numerator comes from
one source and denominator from the other is invalid** — recorded as
`curve.ratio_method`.

**Correction 3 — age-match the denominator.** The analysis doc divides each video's
views by the channel median **at that video's age**; a later run divided by a fixed
`curve.p50_7d`. On `d6DPiORuPO4` those give 0.82 and 0.28. The age-matched method is
correct and is now the recorded one. The *classification* is unaffected — the video is
below its curve either way, and its retention figure comes from a third source — but
the magnitude is not, and the analysis doc's "2.9 views short" framing is the honest one.

## Population notes — read before trusting any field above

**Scale.** 8 subscribers, 14 public videos, channel 8 weeks old. Every median here
is low-n. This baseline supports *ranking* and *falsifying a threshold that points the
wrong way*. It does not support a forensic per-second diagnosis.

**Noise floor.** At 48 h the curve's p30–p70 band spans **7 → 31.5 views**, from a sample
of 6–8 videos. A gap under ~10 views at ≤72 h is inside that band and is not evidence.

**`retention.median_duration_top_quartile_avp_s: 19` — `[S1/S-2]` no longer reads it.**
As of v2.1 the short-form target length reads
`median_duration_top_quartile_curve_s`, which is replay-free. **That field is now
populated: 49.0 s**, computed 2026-09-02 during the baseline reconciliation from
the age-matched ratios in the analysis doc. It sits inside the 30–58 s clamp, so
no `baseline-below-clamp` fires — unlike the avp-derived 19 s, which fell below
the rule's own floor and is kept only as the record of why the rule changed.
The quartile holds 4 of 14 public videos, below `[S9/L-2]`'s ≥ 8 bar, so treat it
as provisional. It is still measured, where the 45 s it replaces was not.
`[S1/S-2]`'s baseline override sets short target length from this field, but the field is
measured by `averageViewPercentage`, which **counts replays**: 6 of 34 shorts score above
100 %, topping out at 603.86 %. Shorter videos loop more readily, so the metric is
partly a function of duration rather than an independent measure of it
(`r(duration, avgViewPct) = −0.25`, n=34 — weak, but in the direction that inflates short
videos). Taken literally the override would set target length to 19 s, below `[S1/S-2]`'s
own 30 s clamp floor, and would ratchet downward on every readout. **Conflict logged; the
rule needs a replay-corrected metric before its override is safe to fire.**

**Curve provenance mismatch.** The schema comments say the curve is long-form. This
channel has no public long-form, so the curve is necessarily built from Shorts. Any rule
reading `curve.*` as a long-form signal is reading Shorts data.

**`p75_48h` renamed.** `vidiq_channel_performance_trends` returns
min/max/avg/median/perc30/perc70 — there is no p75. The field is now
`perc70_48h`, with `perc30_48h` recorded beside it so the noise-floor band is
readable straight off the schema instead of out of a prose note.

**Traffic schema gap.** `browse/suggested/search/external` cannot represent this channel:
**88.1 % of views come from the Shorts feed**, which is not any of those four. Rolled into
`browse` above and also recorded separately as `shorts_feed`, because a rule reading
`traffic.browse` would otherwise silently conflate two different surfaces.

**Retention is inversely related to views on this channel.** The two highest-view videos
have the *lowest* completion (`D4e2xnNQm1M` 1,189 views / 32.74 %; `2NGeQYjsR7Y` 1,027 /
25.63 %), while several videos nobody saw complete above 100 %. Any rule that treats
low avg-view-% as the failure signal will point at the winners.

**Correction to an earlier claim in this run.** Per-video retention was previously
recorded as "not available via vidIQ". That was wrong: `audience_retention` (the 100-point
curve) does return zero rows, but `channel_analytics(report=top_videos)` returns
`averageViewPercentage` **per video**, which is what S0 step 2 calls. The curve is
unavailable; the per-video average is not.
