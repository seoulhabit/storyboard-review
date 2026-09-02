# Learning loop — measured results rewrite the rules

The pipeline is only "data-driven" if what it ships changes what it does next.
This file defines the two readouts, the classification that must happen before
any diagnosis, and the exact write-back into `channel-baseline.md`.

## Readout 1 — 48 hours after publish

Calls:
- `vidiq_video_stats(videoId)` → views, VPH, likes, comments at 48 h.
- `vidiq_channel_analytics(channelId, filters=video==<id>, metrics=[views, averageViewPercentage, averageViewDuration, subscribersGained])`.
- Compare views@48h to `channel-baseline.md → curve.p50_48h` and the band
  `curve.perc30_48h` / `curve.perc70_48h`.

**There is no `p75`.** `vidiq_channel_performance_trends` returns `perc30` and
`perc70`, not a 75th percentile. v2's baseline schema named a field the tool
does not produce; a field name that overstates what a tool returns is how an
invented number gets written down. Use the percentile labels the tool uses.

Write to the ledger:
```
[S9/R48] views 412 vs p50 380 (+8 %) | avg-view 38 % vs median 34 % | subs +6 | vidiq_video_stats
```

No rule changes at 48 h. It is an early-warning line only.

## The noise floor comes before everything

On a small channel most differences are not evidence. Compute the band first:
`vidiq_channel_performance_trends` returns the accumulation curve's percentiles
from a sample of the channel's recent uploads. **Any gap narrower than the
p30–p70 band, or thinner than ~10 views, is inside the noise floor and is
written `[UNDERPOWERED]` — not as a finding.**

Measured on this channel at 8 subscribers: the 48 h p30–p70 band spans 7→31.5
views from a sample of 6–8. A 2.9-view shortfall is a ranking signal and nothing
more. Ranking on it is valid; forensics on it is not.

## Readout 2 — 7 days after publish

Calls:
- `vidiq_video_stats(videoId)`.
- `vidiq_channel_analytics(report=audience_retention, filters=video==<id>)` → 100-point curve.
- `vidiq_channel_analytics(filters=video==<id>, dimensions=[insightTrafficSourceType])` → source shares as the tool labels them, including the Shorts feed (`[S0/B-3]`).
- Impressions CTR: from YouTube Studio if not exposed via vidIQ — write `not available via vidIQ` rather than estimating.

**Per-video `averageViewPercentage` IS retrievable**, via
`channel_analytics(report=top_videos)` or a `video==` filter. Two earlier runs
recorded retention as "not available via vidIQ" after testing only
`report=audience_retention` (which does return zero rows on this channel) and
then *inferred* retention from view velocity — producing a retention diagnosis
on a video that retained above median. Test the top_videos path before writing
the metric off.

### Classification first (`[S9/L-1]`)

| Condition | Class | Where the fix lives |
|---|---|---|
| CTR < channel median **and** avg-view-% ≥ median | **CTR-failure** | S3 packaging (title shape, thumbnail concept) |
| CTR ≥ median **and** avg-view-% < median | **Retention-failure** | S5/S6 structure (hook beat, cadence, section split) |
| both below | **Both** — fix packaging first (it is cheaper and gates the rest) | S3 then S5 |
| both at/above | **Working** — record what fired as a positive signal | none |
| **CTR unavailable **and** avg-view-% ≥ median **and** views ≪ curve** | **Distribution failure** | **S2 (topic/seed) and the first-frame feed signal** |
| CTR unavailable, retention below median | classify as retention-failure; note the CTR gap | S5/S6 |

**The distribution-failure row is the one v2 could not express.** A Short has no
thumbnail-CTR decision to fail, so a Short that is never served has no CTR row
in the table above — v2's version had no branch that applied, and the run
defaulted to diagnosing packaging or structure on a video whose problem was
neither. Measured case: the 2026-09-01 target retained at **67.2 %** against a
per-video channel median of **61.28 %** and a view-weighted Shorts-feed figure
of **38.26 %** — above median — while sitting below its own accumulation curve.
The two most-viewed videos on the channel have its *worst* completion rates.
People who saw it watched two thirds of it; almost nobody was served it.

When this class fires:
- **Do not** rewrite the title or rebuild the thumbnail. There is no CTR
  decision to improve.
- The levers are the topic/seed (S2) and the first-frame feed signal — what the
  first ~1 s hands the feed to decide with. Frame zero, `[S6/A-3]`.
- Say plainly in the readout that the hypothesis is untested until the rebuild
  is published in a comparable slot. A distribution diagnosis is a claim about
  what the feed did, and only a second upload tests it.

Only after the class is written may a diagnosis be attempted. A "bad video"
with no class is a list of everything and fixes nothing.

### Retention diagnosis (when class includes retention)

Map the 100-point curve onto the six spine sections using the beat sheet's
section boundaries. Report:
- the section with the deepest drop (percentage points lost inside it);
- whether the drop begins within 3 s of a section boundary (structure) or
  mid-section (content/pacing);
- any relative-retention spike (the thing to do more of).

### Packaging diagnosis (when class includes CTR)

- Compare the winning title's shape to `title_shapes[]` from that run's T-4;
  if the winner used the *lowest-ranked* shape, mark shape as suspect.
- Re-run `vidiq_score_thumbnail` on the shipped thumbnail; if the score
  differs from the one at ship time by > 10, the scorer moved — log, don't act.
- **Do not treat `vidiq_score_title` as the arbiter.** See `[S3/P-1]`: it has
  scored the failing video above every diagnosis-driven rewrite on two separate
  videos in two separate runs. Log it; keep watching it; do not act on it.

## What may not be cited as a cause

Findings that this channel's own data has already falsified. Each is logged if
observed and then set aside, not written up:

- **Duration outside `[S1/S-2]`'s clamp.** 72 s target vs 116 s control, and the
  control outperforms 10×. No discriminative power.
- **A single-digit view gap.** Inside the noise floor; `[UNDERPOWERED]`.
- **Anything equally true of the controls.** Pull the two best videos as
  controls before diagnosing; a finding that also describes them is discarded.

## Write-back (`[S9/L-2]`)

A **[default]** in `decision-policy.md` is replaced by a measured value in
`channel-baseline.md` when **two consecutive readouts** point the same way:

| Default | Replaced by | Evidence needed |
|---|---|---|
| target length, long (S-2) | median duration of top-quartile videos by avg-view-% | 2 readouts + ≥ 8 videos in the quartile calc |
| target length, short (S-2) | median duration of top-quartile videos by `views ÷ curve.p50_7d` | 2 readouts + ≥ 8 videos; never by avg-view-% (replay-inflated) |
| spine split (S-6) | shifted split per the aggregated retention curve | 2 retention-failure readouts with the same deepest-drop section |
| title score bar (P-1) | — | **held open.** The scorer has inverted twice; a bar cannot be set from a metric that ranks the failure first. Revisit only if a readout shows it ranking correctly. |
| thumbnail score bar 70 (P-3) | the median score of the channel's top-quartile CTR thumbnails | 2 readouts with CTR available |
| cadence caps (C-2) | measured from the two best-retaining videos' beat sheets | 2 "Working" readouts |
| breakout bar 3 (T-3) | the median breakoutScore of the channel's own top 5 | 5 videos with 7-d readouts |
| format default (S-1) | the dominant format by `uploads_90d` | already measured; refresh each S0 |

Each replacement writes: field, old value, new value, date, the two video ids.
Never overwrite a measured value with a default again.

## Running the "worst video" audit

When asked to diagnose an existing underperformer:

1. Define "worst" **relative to the channel curve** (`views@7d ÷ curve.p50_7d`),
   not raw views — otherwise the oldest upload always wins. Confirmed: v1 picked
   its 2026-08-31 target by raw views (100, against two 1,000+ outliers); by
   curve ratio that video scores **4.86**, mid-pack, 9th of 14 from the bottom
   and 6× better than the channel's actual worst.
2. Pull the two best videos as controls. Any finding equally true of the
   controls is discarded.
3. Compute the noise floor (above). Mark everything inside it `[UNDERPOWERED]`
   before looking at it.
4. **Classify** (table above) — including the distribution-failure row. Then,
   and only then, scope the rebuild:
   - CTR-failure → S3 packaging.
   - Retention-failure → S5→S7 on the section carrying the deepest drop.
   - **Distribution failure → S2 seed and the first ~1 s. Not packaging, not a
     structural rebuild of the body.**
5. Every finding the skill could not explain is a `[NOT IN SKILL]` line and must
   land as a new rule in `decision-policy.md` before the session ends — or be
   listed as rejected with one line of reason. Silently dropping one is how a
   rulebook stops matching the channel.
