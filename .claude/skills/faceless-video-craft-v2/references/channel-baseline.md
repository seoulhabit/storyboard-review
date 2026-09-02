# Channel baseline — measured numbers (rewritten by S0 and S9)

```yaml
populated: true
updated: 2026-09-01
channel:
  id: UCzqEGQ9uAU43AgyxGtLT7MA
  handle: SeoulHabit
  subs: 8                       # channel created 2026-07-07; 2,693 lifetime views
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
  p50_24h: 9.5
  p50_48h: 15.5
  perc30_48h: 7                 # noise-floor band, lower bound
  perc70_48h: 31.5              # was mis-named p75_48h; the tool returns perc70
  p50_7d: 25
  p50_28d: 28
  sample_n: 8                   # uploads the percentiles were computed from
retention:
  avg_view_pct_long: 43.07      # n=2, both private — not usable
  avg_view_pct_short: 61.28     # per-video median, n=34
  avg_view_pct_short_weighted: 38.26   # view-weighted, from the SHORTS traffic row
  avg_view_pct_median_per_video: 61.28
  median_duration_top_quartile_avp_s: 19      # LOGGED, NOT USED — see WARNING below
  median_duration_top_quartile_curve_s: null  # [S1/S-2] short target; needs views÷p50_7d, not yet computed
  replay_inflated_share: 0.176                # 6 of 34 shorts score >100% avg-view-%; max 603.86%
  first_drop_s: null            # not available via vidIQ — audience_retention returns zero rows
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
overrides: []                   # none yet — S9 write-back has not run
```

## Population notes — read before trusting any field above

**Scale.** 8 subscribers, 14 public videos, channel 8 weeks old. Every median here
is low-n. This baseline supports *ranking* and *falsifying a threshold that points the
wrong way*. It does not support a forensic per-second diagnosis.

**Noise floor.** At 48 h the curve's p30–p70 band spans **7 → 31.5 views**, from a sample
of 6–8 videos. A gap under ~10 views at ≤72 h is inside that band and is not evidence.

**`retention.median_duration_top_quartile_avp_s: 19` — `[S1/S-2]` no longer reads it.**
As of v2.1 the short-form target length reads
`median_duration_top_quartile_curve_s` (top quartile by `views ÷ curve.p50_7d`),
which is replay-free. That field is `null` until an S0 refresh computes it, so
`[S1/S-2]` uses its 45 s [default] and logs the gap. The avp-derived number is
kept below as the record of why the rule changed.
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
