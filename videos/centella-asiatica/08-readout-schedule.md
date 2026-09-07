# 08-readout-schedule.md — centella-asiatica

Written per S9 (`full` run). Dates computed from a placeholder publish
timestamp — this run does not publish; recompute both dates from Kim's
actual publish timestamp when that happens.

- **48h readout**: publish_time + 48h. Compare against `avg_view_pct_short`
  (channel median, `baseline.yaml`: 61.28 per-video / 38.26 view-weighted)
  and `curve.p50_48h` (15.5) / `curve.perc30_48h`–`perc70_48h` (7–31.5) band,
  age-matched ratio method (`curve.ratio_method: age-matched`).
- **7d readout**: publish_time + 7d. Compare against `curve.p50_7d` (25).

Both against the channel's **own Shorts curve** — this is the channel's
first video with `format: short` produced by this local-compiler pipeline
(prior Shorts in the curve were produced by whatever pipeline preceded
WO-FVC-005), so a first readout round should note the pipeline change
itself as a potential confound, not just a content-quality signal.
