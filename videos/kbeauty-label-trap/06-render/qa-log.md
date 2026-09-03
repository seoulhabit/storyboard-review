# Render QA log — kbeauty-label-trap

## Render

- `hyperframes render --quality high --workers 1` — 1920×1080, 30fps, 7714 frames.
- **Round 1**: 257.133s, 9.0MB, rendered in 9m20s. Superseded — see defects below.
- **Round 2 (final)**: 257.133s, 9.1MB, rendered in 7m57s. Used for `final.mp4`.
- Duration check: 257.133s render vs. `vo_duration_s` 257.120s → Δ0.013s, well
  inside the ±0.15s tolerance.

## Audio master

- Mix bug found and fixed: ffmpeg's `amix` filter defaults `normalize=1`,
  auto-attenuating both inputs on sum — silently dropped the mix ~6 LU below
  the VO's own standalone loudness. Fixed with `normalize=0` (music was
  already manually ducked to 0.12 via a separate `volume` filter; no need for
  amix's own clip protection on top of that).
- Two-pass `loudnorm` (I=-14 TP=-2.5 LRA=11, linear where possible).
  Measured input: -23.72 LUFS / +0.38 dBTP / 5.80 LRA. The VO's true peak
  (+0.38dBTP pre-limiting) relative to its integrated loudness gives a high
  crest factor, so a pure-linear pass to -14 LUFS would exceed the -2.5dBTP
  ceiling — `loudnorm` falls back to dynamic normalization.
- **Final measured: -16.10 LUFS / -1.80 dBTP** (re-measured on `final.mp4`
  itself, not the pre-mux intermediate). Comparable to this pipeline's prior
  shipped master (`kbeauty-one-percent-line`: -15.0 LUFS / -1.3 dBTP) —
  slightly quieter, no clipping, safe for YouTube's own loudness normalization
  on playback.

## Pixel gate — manual frame review (before the landscape tooling gates)

All 14 scene settle points + frame 0 + last frame extracted and read directly
(seek-after-`-i`, frame-accurate). **4 real defects found in round 1, none
caught by `hyperframes check` or the automated tooling gates**:

| # | Defect | Where | Fix |
|---|---|---|---|
| 1 | Frame 0 nearly blank — violates the mandatory "frame zero is the hook" rule | s01 | Droplet starts already visible instead of fading in from opacity 0 |
| 2 | Tag text overlapped live list rows underneath it | s04 | Dim `.canyon-list` to 0.1 opacity before the tag appears |
| 3 | Verdict labels ran through the bottom of both reveal bottles | s12 | Moved bottle-pair up + shrunk it, opening real clearance |
| 4 | **The video's true last ~0.45s rendered solid black** — a structural bug: every scene's own `data-duration` was the beat sheet's nominal duration, while `index.html`'s wrapper keeps each clip mounted for nominal+transition-overlap. Affected **8 of 14 scenes** (every one followed by a non-cut transition), not just the one caught visually | s01,s02,s03,s04,s06,s08,s12,s13 (tail windows) | Fixed centrally in `build_composition.py`: every scene's real on-screen lifetime is now computed once from the same transition formula `index.html` uses, and force-applied as the timeline's registered duration |

Round 2 (final) re-reviewed at the same 16 points plus the s01→s02 transition
midpoint (to visually confirm `check`'s clip-path-unaware overlap warning was
a false positive) — **all 4 defects confirmed fixed, no new defects found.**

## Landscape tooling gates (final.mp4)

| Gate | Result |
|---|---|
| `check-safe-area.py --landscape` | **0 findings**, 1028 frames sampled at 250ms — every sampled frame's ink stayed clear of all four reserved zones (top<54, bottom≥972, right≥1824, left<96). Hard gate, passes clean. |
| `check-static-hold.py --landscape` | Advisory (always exit 0). 24 region-level content-voids found. Most 1s voids are transition-boundary artifacts (a wipe's mid-cut moment reading as briefly empty in one grid cell) — benign. The larger multi-second voids (8–19s, concentrated in s04/s05/s09/s10/s11/s12/s13/s14) reflect scenes whose visual content sits in one screen region while the rest of the 2×3 grid stays empty for a long stretch. Same underlying finding as the cadence gate below, not a second independent problem. |
| `check-cadence.py --longform` | Advisory (always exit 0). 12 of 14 scenes exceed the 6.0s quiet ceiling (longest: s10's evidence tunnel, 30.25s with no visible beat after its entrance animations finish). **Logged as a real, honest craft gap, not silently accepted**: several scenes front-load their motion into the first 20–40% of their duration and then hold static while the VO continues talking. This is common in this format (the viewer needs time to read a diagram/citation while narration continues) but the channel's own posture rule ("motion that encodes meaning," avoiding the generic-explainer register) would be better served by spreading reveals later into each scene or adding subtle ambient motion. **Not fixed in this run** — both gates are advisory, this run is already on its 2nd render (within the pixel-gate's re-render cap but at the point of diminishing return for a 3rd purely-cosmetic pass), and the underlying content/claims/safe-area/transitions are all correct. Flagged in `09-run-report.md` as a named follow-up for the next revision round, with exact per-scene numbers preserved here rather than summarized away. |

`continuity-audit.py` (source-level, re-run on final composition): 8/13
boundaries carried by a transition, top entrance-signature share 37.2%
(under the 50% bar), 0 rebuilt-actor pairs, 7 genuine camera-move tweens.
0 plain-crossfade-across-ground-change violations (the one hard rule this
tool enforces).

## K-4 — rendered-claim check

Verified on the extracted frames (see `01-story-brief.md` §Sourcing for the
claim table this checks against):

- C6 (s05) and C15 (s11): `UNSOURCED` flag visible **concurrently** with the
  claim, ink-toned (not accent-colored), not citation-styled. On-screen
  wording ("may be active at low levels", "'Gentle' isn't a fixed property")
  hedges at least as far as the VO.
- C3/C4 (s04), C8 (s06), C10 (s09): citation chips (`FDA · 21 CFR 701.3`,
  `EU · Reg. 1223/2009 Art. 19`, `J Cosmet Sci · 2020`, `Int J Cosmet Sci ·
  2009`) render plainly, human-readable, no PMID and no internal record id
  anywhere on any frame.
- C17/C18 (s12 reveal): the "80%" Bottle-A claim is **VO-only, never
  rendered on screen** — deliberately, to sidestep any risk of it reading as
  a floating unattributed stat. The two verdict tags (`MORE UNCERTAINTY` /
  `MORE DECISION-USEFUL INFORMATION`) carry no scorecard grammar (no n/5,
  no ticks, no bars) and both sit under an `[Authored, illustrative — not a
  claim]` tag.
- No hard-prohibited claim (`[K-2a]`) appears on any reviewed frame.

**Verdict: K-4 passes.** 0 fix cycles needed against the 2-cycle cap (the
claim-rendering gap was caught and fixed before the first render, at the
composition-source level — see `00-decision-ledger.md`).
