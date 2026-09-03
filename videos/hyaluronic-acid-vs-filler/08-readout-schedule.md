# Readout schedule — hyaluronic-acid-vs-filler

Two readouts, both relative to the **publish moment**, which has not happened —
`[S8/E-1]` leaves the click to Kim. Set the dates from the actual publish time.

| Readout | When | Rule |
|---|---|---|
| R48 | publish + **48 h** | `[S9/R48]` — early-warning line only, **no rule changes** |
| R7D | publish + **7 d** | `[S9/L-1]` classify, then `[S9/L-2]` write-back |

---

## Readout 1 — 48 hours

```
vidiq_video_stats(videoId)
vidiq_channel_analytics(channelId="UCzqEGQ9uAU43AgyxGtLT7MA",
    filters="video==<id>",
    metrics=["views","averageViewPercentage","averageViewDuration","subscribersGained"])
```

Compare `views@48h` against the baseline as it stands **today**:

| Field | Value | Source |
|---|---|---|
| `curve.p50_48h` | **15.5** | measured 2026-09-03 |
| `curve.perc30_48h` | **7** | the noise floor's lower bound |
| `curve.perc70_48h` | **31.5** | upper bound |
| `curve.sample_n` | 8 | 6–8 uploads depending on bucket |

**Compute the band before writing anything.** Any gap narrower than 7→31.5, or
thinner than about 10 views, is inside the noise floor and is written
`[UNDERPOWERED]`, not as a finding. On an 8-subscriber channel this is the
default outcome, not the exception.

Ledger line shape:
```
[S9/R48] views <n> vs p50 15.5 (band 7-31.5) | avg-view <n>% vs median 48.81% | subs +<n> | vidiq_video_stats
```

## Readout 2 — 7 days

```
vidiq_video_stats(videoId)
vidiq_channel_analytics(report="audience_retention", filters="video==<id>")
vidiq_channel_analytics(filters="video==<id>", dimensions=["insightTrafficSourceType"])
```

**Pull `averageViewPercentage` from the `top_videos` path before writing
retention off.** `report=audience_retention` returns zero rows on this channel —
it did again during this run's S0 — and two earlier runs recorded retention as
"not available via vidIQ" on that basis and then *inferred* it from view
velocity, producing a retention diagnosis on a video that retained above median.
The per-video metric IS retrievable; S0 pulled it for all 39 videos this run,
but **only after passing `metrics` explicitly** — the default metric set for
`top_videos` silently omits it.

Impressions CTR is **not exposed via vidIQ**. Take it from Studio or write
`not available via vidIQ`. Do not estimate it.

### Classify before diagnosing — `[S9/L-1]`

Channel medians to compare against (measured 2026-09-03):

| Metric | Median | Note |
|---|---|---|
| avg-view-% per video | **48.81%** | n=39 |
| views (per video, 365 d) | 34.0 | |
| CTR | `null` | not available via vidIQ |

| Condition | Class | Fix lives in |
|---|---|---|
| CTR < median **and** avg-view-% ≥ median | CTR-failure | S3 packaging |
| CTR ≥ median **and** avg-view-% < median | Retention-failure | S5/S6 structure |
| both below | Both — packaging first | S3 then S5 |
| both at/above | Working | none |
| **CTR unavailable, avg-view-% ≥ median, views ≪ curve** | **Distribution failure** | **S2 seed + the first-frame feed signal — NOT packaging, NOT structure** |

**Distribution failure is the likeliest class here and the easiest to
misdiagnose.** CTR is unavailable on this channel, so a video that is simply
never served has no CTR row to fail. The measured precedent: the 2026-09-01
target retained at 67.2% against a 61.28% median while sitting below its own
accumulation curve — people who saw it watched two thirds; almost nobody was
served it. If this class fires, **do not rewrite the title or rebuild the
thumbnail.** The levers are the seed (S2) and what the first second hands the
feed, i.e. frame zero `[S6/A-3]`.

---

## What this run has already loaded into the readout

Two things are **`[UNDERPOWERED]` by construction** and must not be reported as
findings:

1. **Every `curve.*` and `retention.*` comparison for this video.** It is the
   channel's first published long-form piece; the accumulation curve is built
   entirely from Shorts (`baseline-notes.md` says so independently: "This channel
   has no public long-form, so the curve is necessarily built from Shorts. Any
   rule reading `curve.*` as a long-form signal is reading Shorts data"). Ranking
   a 180 s 16:9 video against a Shorts curve is a category error.
2. **Duration has no discriminative power on this channel**, per the standing
   `overrides[]` entry: the age-normalised medians for ≤50 s and >50 s cohorts
   are 4.38 vs 3.97 against a within-cohort spread of 0.67–49.44. Do not cite
   this video's 180 s runtime as a cause of anything.

### Specific things to check, which this run set up deliberately

- **`packaging.title_scorer_discriminative` is `false`** in the baseline, from two
  prior runs where the scorer ranked a failing title above its rewrites. This run
  produced **no inversion** — the top scorer (95) also won on shape rank — so it
  is a **null result**, not evidence the scorer works. `[S9/L-2]` needs a case
  where the scorer and the outcome disagree. Log which way this one went.
- **The title's runner-up is on record.** `[S3/P-1]`'s own default would have
  picked #4 ("Why Hyaluronic Acid Filler and Serum Do Completely Different Jobs",
  93) because its first 40 characters carry the mechanism; the winner's carry
  origin. The winner was chosen on a shape drawn from a **single** comparator at
  breakoutScore 4.37. If this reads as a CTR-failure, #4 is the tested
  alternative, not a fresh guess.
- **`[S2/T-3]` returned no usable browse evidence at all** — the outlier tool
  matched "acid", "filler" and "injection" in unrelated senses (Roblox filler
  episodes, oil filters, a billiards player named Filler, gecko rescues). If this
  video underperforms on distribution, that void is a prior, not a surprise.

### Write-back — `[S9/L-2]`

A `[default]` contradicted **twice in a row** is replaced by the measured value
in `videos/_channel/baseline.yaml`, with the date and the two video ids as
evidence. Append to `overrides[]`; never overwrite it.

Fields this video can legitimately move:
- `formats.long.median_views_per_upload` and `views_90d` — currently `null` /
  26, because there was no public long-form to measure.
- `retention.avg_view_pct_long` — currently `null` and the reason this run is
  tagged `baseline-partial`. **One video does not make a median**; record it as
  n=1 and say so.
- `voice.words_per_minute` — currently the unmeasured `150` [default]. This run
  measured **161.3 wpm** for Kimberly on a long line. Two more long-form VOs and
  that default can be replaced.
