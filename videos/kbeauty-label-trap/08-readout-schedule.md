# Readout schedule — kbeauty-label-trap

Readouts are keyed to the operator's actual publish moment (unknown at
render time) — the dates below are offsets, not calendar dates, to be
resolved when `07-publish-envelope.md` is actually used.

| Readout | When | Reads |
|---|---|---|
| R48 | 48h after publish | `vidiq_video_stats`, `vidiq_channel_analytics(filters=video==<id>)` — early CTR, first retention curve |
| R7D | 7 days after publish | Same calls, full-week view; compare against `videos/_channel/baseline.yaml` |

## Why this run matters for the baseline

`videos/_channel/baseline.yaml`'s `retention.avg_view_pct_long` is currently
`43.07 (n=2, both private, "not usable")` — both prior long-form pieces
(`ectoin-survival-molecule`, `hyaluronic-acid-vs-filler`) are unpublished or
private. **This will be the channel's first *public* long-form retention
data point**, assuming the operator publishes it. Until then and until a
second public long-form comparator exists, every retention comparison in
this run's own ledger is tagged `[UNDERPOWERED]` — R48/R7D should update
`baseline.yaml`'s long-form fields with real numbers rather than carrying
the `not usable` flag forward by default.

## What to compare, once real data exists

- CTR against the thumbnail's predicted score (89) — is a self/independent
  vidIQ score of 89 predictive at this channel's actual scale (8 subs)?
- Retention curve against the canonical section boundaries in
  `03-beat-sheet.json` — does viewer drop-off cluster at a specific
  section (Hook exit at 15.8s? Mechanism, the longest section at 101.6s?),
  which would inform a length/pacing correction for the *next* long-form
  video rather than this one.
- Whether the 12.5%-under-target runtime (257.12s vs. the nominal 300s)
  reads as "tight" or "rushed" in viewer feedback/comments — this is the
  first real signal on whether "measured VO is the clock, don't pad" was
  the right call for this channel's audience.
