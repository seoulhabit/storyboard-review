# Channel baseline — measured numbers (rewritten by S0 and S9)

```yaml
populated: false          # S0 sets true
updated: null             # YYYY-MM-DD
channel:
  id: null
  handle: null
  subs: null
formats:
  long:  { uploads_90d: null, median_views_per_upload: null }
  short: { uploads_90d: null, median_views_per_upload: null }
traffic:                  # share of views, last 90 d — [S0/B-3]
  # Record EVERY source insightTrafficSourceType returns, with its own label.
  # These four cannot describe a Shorts channel on their own.
  shorts_feed: null       # the one the four-slot schema had no room for
  browse: null
  suggested: null
  search: null
  external: null
  other: {}               # any further labels the tool returns, verbatim
curve:                    # from vidiq_channel_performance_trends
  # The tool returns perc30 / perc70, NOT a p75. Do not name a field the tool
  # does not produce. perc30..perc70 is the run's noise floor.
  p50_24h: null
  p50_48h: null
  perc30_48h: null
  perc70_48h: null
  p50_7d: null
  p50_28d: null
  sample_n: null          # how many uploads the percentiles were computed from
retention:
  # Per-video averageViewPercentage IS retrievable via report=top_videos.
  # audience_retention returning zero rows is not evidence the metric is absent.
  avg_view_pct_long: null
  avg_view_pct_short: null
  avg_view_pct_median_per_video: null
  median_duration_top_quartile_avp_s: null    # long-form target length [S1/S-2]
  median_duration_top_quartile_curve_s: null  # short target length; views ÷ p50_7d
  replay_inflated_share: null   # fraction of shorts with avg-view-% > 100 %
  first_drop_s: null      # where the aggregated curve first loses ≥ 10 points
  section_curve:          # 10-bucket aggregate, top-3 vs bottom-3 videos
    top:    []
    bottom: []
packaging:
  median_ctr: null        # from Studio if not via vidIQ; else null
  title_scorer_discriminative: null   # [S3/P-1] — false while it ranks failures first
  median_title_score_top_quartile: null
  median_thumb_score_top_quartile: null
voice:
  id: null
  words_per_minute: 150   # measured after the first VO: chars/5 ÷ minutes
music:
  track_url: null
best_publish_windows: []  # from vidiq_subscriber_insights
overrides:                # [default]s replaced by measured values, with evidence
  # - field: spine_split.mechanism
  #   old: "18-55%"  new: "18-62%"  date: 2026-10-14  videos: [id1, id2]
```

Rules for editing this file:
- Only S0 (full refresh) and S9 (`[S9/L-2]` write-back) write here.
- A field that a call could not fill stays `null` and the ledger records
  `not available via vidIQ` — never a guessed number.
- `overrides` is append-only; it is the audit trail of every rule that changed.
