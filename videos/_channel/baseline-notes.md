# Channel baseline — provenance and caveats

Companion to `baseline.yaml` in this directory. Migrated 2026-09-03 from the v2
skill's `references/channel-baseline.md`, which was removed when
faceless-video-craft moved to its standalone repo. The prose below is carried
over **verbatim** from that file; only this header is new.

Read this before relying on any field in `baseline.yaml` marked CAVEAT, and
before recording any metric here as unavailable.

> Note on one path reference below: "this one" and "`references/channel-baseline.md`"
> refer to the pre-migration file, whose measured half is now `baseline.yaml`
> beside this document.

---

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
