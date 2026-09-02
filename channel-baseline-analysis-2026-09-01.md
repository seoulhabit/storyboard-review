# channel-baseline — UCzqEGQ9uAU43AgyxGtLT7MA (SeoulHabit)

**Populated 2026-09-01** from a live vidIQ pull (`vidiq_user_videos` n=48,
`vidiq_channel_performance_trends`, `vidiq_video_stats`) plus a filesystem count over
`videos/*`. Ages measured against 2026-09-01T20:54Z.

**Status: ANALYSIS DOCUMENT. Not the canonical baseline.**

> **Reconciled 2026-09-02.** This file was written before the v2 package was installed
> on this machine, and its own header asked for its numbers to be pasted into v2's
> `references/channel-baseline.md` once available. **That paste is done.**
>
> **Canonical for every schema field is now
> `.claude/skills/faceless-video-craft-v2/references/channel-baseline.md`** — that is
> what `[S0/B-1]` and every `[baseline]` rule read. This file is kept for the analysis
> the schema has no slot for: the duration-threshold falsification (§4), the repo-level
> conformance audit (§5), and the still-unbacked inventory (§7).
>
> **Two claims below are superseded — corrected in place and marked.** Do not cite the
> original wording.
>
> **View counts in §2 and §4 are `vidiq_video_stats` (lifetime public).** These are NOT
> interchangeable with `channel_analytics` figures, which are windowed and disagree
> sharply on some videos (`cGbokt_B_vE` 145 vs 32, `Yc1hH5Bz4t8` 162 vs 13). §3's curve
> is built from the same family as §2/§4, so the ratios here are internally consistent —
> a ratio mixing the two sources is not.

Every figure below is measured; nothing is estimated.

---

## 1. Corpus composition

| | Count |
|---|---|
| Total uploads | 48 |
| Shorts (`videoType: "short"`) | **46** |
| Long-form (`videoType: "long"`) | 2 — a 34s clip and a 48s ex-livestream, **both private** |
| Public | 14 |
| Unlisted | 1 |
| Private | 33 |

**Consequence for any ranking step:** there is no long-form corpus. Only the 14 public
uploads carry a distribution signal — private and unlisted view counts reflect no
algorithmic delivery and cannot be ranked against public ones.

## 2. Public view distribution (n=14)

| | Views |
|---|---|
| Min | 4 |
| Median | **58.0** |
| Mean | 211.8 |
| Max | 1,193 |
| Median excluding the two >1,000 outliers (n=12) | **45.0** |
| Mean excluding those outliers | 59.2 |

The mean is 3.6× the median. **Use the median; the mean is not usable on this corpus.**

## 3. Accumulation curve (`vidiq_channel_performance_trends`)

| Age | p30 | median | p70 |
|---|---|---|---|
| 1h | 0.1 | 1 | 1 |
| 2h | 1.1 | 2 | 2.9 |
| 6h | 3.0 | 6 | 8 |
| 12h | 5.0 | 6.5 | 10.5 |
| **24h** | 6.5 | **9.5** | 18.5 |
| **48h** | 7.0 | **15.5** | 31.5 |
| **72h** | 7.0 | **21** | 39.5 |
| 7d | 7.0 | 25 | 64.5 |
| 28d | 8.5 | 28 | 109 |

**Sample-size caveat, and it is load-bearing.** The curve's own `avg` values divide by
6–8 videos, and its 28-day max is 389 — so neither 1,000+ video is in the sample. The
p30–p70 band at 48h spans 7 → 31.5 views. **A gap of a few views at this age is inside
the noise floor**, which is the basis for the `[UNDERPOWERED]` rule now governing the
findings table.

## 4. Duration vs. the 28–45s default and 50s ceiling — tested, age-normalized

**Corrected 2026-09-01.** An earlier version of this section compared raw view counts
across a corpus spanning 7 hours to 48 days of age and concluded "the longer cohort has
the higher median." That was wrong: the >50s cohort simply contained older videos with
more time to accumulate. Normalizing against §3's curve removes the artifact and slightly
**reverses** the direction — which is the evidence that neither direction is real.

Each video's views divided by the channel's own median at that video's age:

| Video | dur | views | age (h) | expected median | ratio |
|---|---|---|---|---|---|
| `2s2tYIOEpwo` | 31s | 4 | 6.9 | 6.0 | **0.67** |
| `d6DPiORuPO4` | 72s | 13 | 49.8 | 15.9 | **0.82** |
| `1ytTppx1C_s` | 62s | 15 | 27.9 | 10.5 | 1.43 |
| `fqfjSj0p8NY` | 42s | 21 | 44.4 | 14.6 | 1.44 |
| `lhFQzV5_BrA` | 52s | 54 | 69.6 | 20.5 | 2.64 |
| `TFzR62tdxHI` | 63s | 63 | 69.6 | 20.5 | 3.08 |
| `BY10jUsN76c` | 35s | 36 | 19.9 | 8.5 | 4.25 |
| `NUgjmYXI-5A` | 31s | 62 | 40.9 | 13.7 | 4.52 |
| `LPqIuEYOx3s` | 114s | 104 | 81.1 | 21.4 | 4.86 |
| `aQnB7abw8M4` | 51s | 32 | 6.9 | 6.0 | 5.33 |
| `cGbokt_B_vE` | 116s | 145 | 51.9 | 16.4 | 8.85 |
| `Yc1hH5Bz4t8` | 42s | 162 | 44.6 | 14.7 | 11.05 |
| `D4e2xnNQm1M` | 42s | 1193 | 1170.6 | 28.0 * | 42.61 |
| `2NGeQYjsR7Y` | 56s | 1061 | 83.0 | 21.5 | 49.44 |

\* extrapolated — the curve ends at 28 days and this video is 48 days old.

| Cohort | n | Median ratio |
|---|---|---|
| ≤ 50s | 6 | 4.38 |
| > 50s | 8 | 3.97 |
| ≤ 50s, excluding the two >1,000-view videos | 5 | 4.25 |
| > 50s, excluding the two >1,000-view videos | 7 | 3.08 |

**Conclusion: there is no evidence supporting the 50s ceiling.** The cohort medians differ
by less than the spread *within* either cohort — ratios run 0.67 to 49.44, two orders of
magnitude, and the two cohorts overlap across nearly that entire range. Raw counts favour
the longer cohort; age-normalized counts favour the shorter one; neither margin survives
n=6/n=8 against that spread.

**This does not license the inverse.** "Shorter performs better" is exactly as unbacked
here as "longer performs better" was. The finding is that this corpus cannot distinguish
the cohorts at all — so the 28–45s default and the 50s ceiling can stand as a *craft
budget* if the skill wants one, but must not be cited as a performance threshold or used
to rank a failure. It flags `d6DPiORuPO4` (0.82) and `cGbokt_B_vE` (8.85) identically.

**Second by-product, computed 2026-09-02.** `[S1/S-2]`'s short-form target length reads
`median_duration_top_quartile_curve_s`, which sat `null`. The top quartile of this table
by ratio is 4 videos — `2NGeQYjsR7Y` (56s), `D4e2xnNQm1M` (42s), `Yc1hH5Bz4t8` (42s),
`cGbokt_B_vE` (116s) — median duration **49.0s**, inside the rule's 30–58s clamp. Now
populated in the canonical file, flagged provisional: 4 videos is below `[S9/L-2]`'s ≥ 8
bar. Note this does **not** contradict §4's conclusion — "what duration do our
best-performing videos have" is a different question from "does duration predict
performance," and the answer to the second is still no.

**Useful by-product — a cleaner statement of standing than raw views.** Only two public
videos sit below their age-matched median: `2s2tYIOEpwo` (0.67) and `d6DPiORuPO4` (0.82).
Every other public upload is above 1.0. But the target's shortfall is **13 observed vs
15.9 expected = 2.9 views**, which is inside the p30–p70 band and under the 10-view floor
— so this ranks the target without licensing a forensic diagnosis of it.

Also re-counted: **21 of 46 shorts run past 50s** (v1's SKILL.md asserts "14 of this
channel's 23 shipped shorts"). Both the numerator and the corpus size in that sentence are
stale.

## 5. Repo-level conformance (28 projects under `videos/`)

| Check | Count | v1 SKILL.md's stated figure |
|---|---|---|
| References `--safe-*` tokens | **10 / 28** | "only 6 of 24 shipped projects" |
| Ships a real `.srt`/`.vtt` sidecar | **10 / 28** | "only 4 of 24 shipped projects" |
| Has a thumbnail file | 19 / 28 | — |
| Has a `box-sizing` reset in at least one composition | 22 / 28 | — |

Two caveats on my own measurement, recorded so the next reader does not over-trust it:

- `box-sizing` is measured as **project-level presence, not per-file coverage**, and that
  overstates conformance: `centella-tiger-grass` counts as "yes" while carrying the reset
  in only 2 of its 7 scene files.
- An earlier version of this count reported `0/28` for both `--safe-*` and `box-sizing`.
  That was a bug in my own shell loop (`grep -ql` — `-q` suppresses the output `-l`
  produces, so every project silently read as "no"). Corrected and re-verified against two
  projects whose answer I already knew.

## 6. Thresholds this baseline can now replace

| v1 threshold | Replace with |
|---|---|
| "28–45s default, >50s needs a reason" *(as a diagnostic)* | **No evidence either way.** Age-normalized median ratio 4.38 (≤50s) vs 3.97 (>50s), against a within-cohort spread of 0.67–49.44. Keep as a craft budget; **do not use it to rank a failure, and do not assert the inverse.** |
| "14 of this channel's 23 shipped shorts run past 50s" | **21 of 46** |
| "only 6 of 24 shipped projects reference `--safe-*`" | **10 of 28** |
| "only 4 of 24 shipped projects ship a sidecar" | **10 of 28** |
| Implicit "views" as a performance measure | **Median 58 (n=14), or 45 excluding two outliers.** Against the age curve, not raw. |
| Absent: a noise floor for "below expected" | **A gap under ~10 views at ≤72h is inside the p30–p70 band and is not evidence.** |

## 7. Still unbacked by channel data — do not present these as measured

| Threshold | What it rests on now | What would back it |
|---|---|---|
| Cadence 1.5–3s (shorts), 8–12s (long) | Asserted, no channel evidence | ~~Per-video retention curves — `audience_retention` returns zero rows, so this is currently unobtainable via vidIQ~~ **SUPERSEDED 2026-09-02:** the zero rows block the 100-point *curve* only. Per-video `averageViewPercentage` **is** retrievable via `channel_analytics(report=top_videos)` — measured n=36. A per-second cadence correlation still needs the curve, but retention is not wholesale unavailable, and nothing should be recorded as such. |
| Safe zones 192 / 384 / 162 px | Platform observation, not channel data | A current-device screenshot measurement |
| Type floors (hero 96–160, body 40, caption 42–56, label ≥32) | Asserted, explicitly set *above* an outside review's numbers | A legibility test, or retention correlated against type size |
| −14 LUFS / −1.5 dBTP | Platform spec — legitimately not channel data | n/a, keep as-is |
| "65–80% vertical safe-column fill" | Asserted, and has **no stated measurement method** | A method that separates authored content from a full-bleed plate |
| Payoff by ~2s | Asserted; consistent with this channel's hook evidence but **not independently measured here** | Retention curves — same *curve* blocker as cadence, but see the correction there: per-video avg-view-% is available and is what the 2026-09-01 distribution-vs-retention classification was actually built on |

## 8. What this baseline does *not* license

~~The channel's retention data is unavailable (`audience_retention`: zero rows)~~ —
**SUPERSEDED 2026-09-02: the 100-point curve is unavailable; per-video
`averageViewPercentage` is not, and measures 61.28 % median across 34 shorts.** The rest
of this paragraph stands: the public corpus is 14 videos, and the accumulation curve is
built from 6–8. Every conclusion drawn
from this baseline is a **view-count conclusion at low n**. It supports ranking and it
supports falsifying a threshold that points the wrong way. It does not support a forensic
per-second diagnosis, and any finding whose whole evidence is a single-digit view
difference must be marked `[UNDERPOWERED]`.
