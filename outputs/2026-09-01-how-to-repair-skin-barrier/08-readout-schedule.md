# Readout schedule

This cut is a dry-run artifact. If it is published, the readouts are:

| When | Calls | Compare against |
|---|---|---|
| **+48 h** | `vidiq_video_stats`; `vidiq_channel_analytics(filters=video==<id>)` | `curve.p50_48h` = 15.5, band `perc30_48h` 7 → `perc70_48h` 31.5. Early warning only, no rule changes. |
| **+7 d** | the above, plus `report=audience_retention`, plus `dimensions=[insightTrafficSourceType]` | `curve.p50_7d` = 25; `retention.avg_view_pct_short` median 61.28 % |

**Classify before diagnosing (`[S9/L-1]`).** On this channel CTR is not
available via vidIQ and a Short has no thumbnail-CTR decision, so the live rows
are retention-vs-median and views-vs-curve. If retention lands ≥ 61.28 % and
views land well under 25, the class is **distribution failure** and the fix
lives in S2 and the first frame — not in packaging, not in a structural rebuild.

**The noise floor comes first.** The 48 h p30–p70 band spans 7 → 31.5 views from
a sample of 8. Any gap thinner than that band is `[UNDERPOWERED]` and is not
written up as a finding.

**What this run already owes `[S9/L-2]`:** a third consecutive `vidiq_score_title`
inversion (top score went to T-4 shape rank 4). Two were already on record.
`packaging.title_scorer_discriminative` stays `false` and the title score bar
stays held open.
