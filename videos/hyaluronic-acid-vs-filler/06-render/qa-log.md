# QA log — hyaluronic-acid-vs-filler (v3 revision)

`00-decision-ledger.md`'s v3 section covers narrative/root-cause detail; this file
is the gate table, run fresh against the actual shipped `final.mp4` rather than
carried forward from the v2 log this file replaces.

## Gates

| Gate | Result | Measured on |
|---|---|---|
| `hyperframes@0.8.22 check --json --snapshots` | **ok: false** — 2 errors, 0 warnings, 6 info, both errors confirmed benign (see below) | the composition under seek, 9 samples |
| `check-safe-area.py --landscape` | **FAIL, 261 frames** — confirmed exception, not silently passed (see below) | `final.mp4` |
| `check-static-hold.py --landscape` | advisory (exit 0); whole-frame 0 findings (330 samples); region-aware 15 content-void flags, one spot-checked and confirmed a false positive (sparse line-art on a dark ground) | `final.mp4` |
| `check-cadence.py --longform` | advisory (exit 0); **26.3% whole-video active share**; **3 scenes exceed the 6.0s quiet ceiling** — see "Not fixed this pass" below | `final.mp4` |
| `ebur128` | **−14.0 LUFS integrated, −3.3 dBTP**, LRA 2.2 | `final.mp4`, the shipped file |
| `ffprobe` duration | video **165.186000s** == VO master clock (`vo-timing.json measured_total_s` 165.186) to within 0.00004s | `final.mp4` |
| `moov`/`mdat` order | `moov` at byte 32, before `mdat` at 143,991 — fast-start present | `final.mp4` |

**`hyperframes check` was not re-run against the v3 composition until this
verification pass.** The `check.json` and this file were both still the stale
v2 documents (160s duration, "v2 revision" header) when the v3 render was
already sitting in `06-render/final.mp4` — a real process gap: `[S7/R-1]`
states "the gate is the engine's own `check`... errors gate the run," which
only has force if the gate is actually re-run before the render ships. Filed
to `videos/_channel/policy-change-proposals.md`: this pipeline needs a check
that ships a `check.json` older than `index.html`/the beat sheet it's meant
to have validated.

### `hyperframes check` — the 2 errors, confirmed benign

Both are `content_overlap` at a wipe-transition boundary, both firing for
0.55s exactly across the transition's clip-path travel window:

| Finding | At | Overlapping selectors |
|---|---|---|
| `content_overlap` | t=11.307–11.858s | `#s01-hook-b0` ("SAME ACTIVE INGREDIENT.") vs `#s02-lineup-b0`'s container |
| `content_overlap` | t=134.851–135.403s | `#s14-fda-warning-b0` ("DO NOT INJECT YOURSELF") vs `#s15-badges-b0`'s container |

Both boundaries are `wipe-up 0.600s` (confirmed in `index.html`'s transition
script, not assumed). This matches `[S6/A-8]`'s documented, sanctioned
exception exactly: *"Expect `[S7/R-1]` to report a wipe boundary as
`content_overlap`... A wipe only clips, so it cannot place content anywhere a
settled frame does not already have it."* The rule requires confirming on an
extracted frame before accepting the exception, not accepting it on the
strength of the rule alone — done here: frames pulled from inside both
flagged windows (t=11.6s, t=135.1s) show clean, fully-resolved scenes with
**no visible overlap** at either point. **Confirmed benign, now ledgered**
(this is the first time either boundary has been checked — v2 did not carry
either scene, both are new to v3).

The 6 info-level findings (one more `content_overlap` at a `blur-crossfade`
boundary t=25.65s, four `container_overflow` on hold-drift-padded stages)
match the same accepted class this project's v2 log already carried: box
crosses the edge under a bounded drift transform, ink does not — not
re-verified pixel-by-pixel this pass since none are gating and the pattern
is already established.

## `[S7/R-2]` — safe-area hard-gate exception, re-confirmed on v3

**`check-safe-area.py --landscape`: FAIL — 261 sampled frames**, on all four
edges, first at t=20.50s, occurring only inside the four plate scenes'
windows (s03/s04/s09/s16 — cross-referenced every reported timestamp against
scene boundaries, no non-plate scene contributes a single flagged frame).

Root cause (from `00-decision-ledger.md`'s v3 section, independently
re-verified this pass, not just carried forward): the scanner clusters the
outer-border luma to find a "page ground," then flags anything in a reserved
zone that doesn't match. A full-bleed photograph has no single ground color —
every pixel is legitimate image content — so the method cannot evaluate this
scene type at all. **Re-confirmed by direct pixel inspection**: viewed the
misconception plate (t=22s) and the plumping plate (t=79s) directly — both
are genuine full-bleed photography with the caption text safely inside the
reserved margins, nothing foreign encroaching. Filed to `videos/_channel/
policy-change-proposals.md`: `check-safe-area.py` needs a `--allow-photo-bleed`
flag or an exemption keyed off the beat sheet's own `scene.plate` field.

## `[K-4]` — rendered-claim check, on extracted frames

| Check | Verdict |
|---|---|
| Hedges match VO in on-screen type | **PASS** — "Smaller ones **may** travel farther into the upper layers" (s08-serum-size, C5) and "Cells can **temporarily** **appear** softer" (s09-plumping-plate, C6), both confirmed in rendered markup |
| No internal id (`ING-*`) or PMID anywhere | **PASS** — every `class="cite"` chip renders `Journal · Year` or `FDA · Dermal Fillers` only. The string "PMID" appears in 15 scene files, but every instance is inside a CSS comment reminding the author never to render one — confirmed by inspecting the surrounding text, not by the grep hit count alone |
| No chip shares a frame with a plate | **PASS** — checked all 4 plate scenes (s03, s04, s09, s16) for any `cite`-class element: zero |
| FDA passage verbatim | **PASS** — "DO NOT INJECT YOURSELF" full-frame, `FDA · Dermal Fillers` chip, matches the regulator's own sentence |
| Nothing hard-prohibited | **PASS** — no treats/prevents/cures, no unsourced number, no absolute language |
| One citation treatment throughout | **PASS** — unchanged mono pill, 7 distinct chip texts across the piece |

## Subject plates

Exactly 4 photoreal plates (`subject-01-misconception`, `-02-not-filler`,
`-03-plumping`, `-04-takeaway`), used only in their 4 named scenes — confirmed
by file-size fingerprint (the 4 plate-scene frames are the only outsized
extracted stills, ~2.2–2.3MB vs ~40–260KB for every diagram scene) and by
direct viewing of 2 of the 4. Consistent subject, correct hand/finger anatomy
in both viewed plates. `soul_cast` (built for cross-shot identity) was
unavailable on this account's plan tier; the run report discloses the
fallback to `soul_v2` with an image reference — visibly minor styling drift
(earring style) between shots, same person, same grade.

## Not fixed this pass — flagged, not buried

1. **The decision ledger's `[S7/R-2]` line claims `check-cadence.py
   --longform` found "no scene exceeds the 6.0s quiet ceiling." This is
   false, confirmed by re-running the exact script against the exact shipped
   file**: 3 scenes exceed it — scene 1/hook (6.50s quiet, t=0.25–6.62s),
   scene 7/compare (8.38s, t=47.12–55.38s), scene 8/serum-size (8.88s,
   t=61.12–69.88s). Traced to source: beats ARE authored in all three
   windows (a kicker fade, a headline clip-path reveal, a subhead fade in
   the hook's case), but their measured pixel delta falls under the
   scanner's visibility floor — small-text-only tweens, the exact gap this
   skill's own docs describe as "counted ≠ perceptible."
2. **Frame zero is a lone kicker line on an almost-empty canvas** ("SAME
   ACTIVE INGREDIENT." with faint background dots, nothing else) for the
   first ~2s, with the headline not arriving until t=4.12s. This is a
   **Mandatory Rule #5** concern, not just the cadence advisory above:
   *"Frame zero is the hook and the thumbnail candidate. Never blank, never
   mid-fade, never a lone title on empty canvas."* `frames-final/
   frame-000-hook.png` in this commit is the true, unedited t≈0.05s frame —
   shipped as-is rather than substituted with a later, better-looking
   moment, so the record reflects what the render actually does.
3. Closing thesis holds fully-settled for **~3.6–3.8s** before the video
   ends (down from v2's 8s) — clears the ≥3s floor stated in the brief, but
   with much less margin.

Neither (1) nor (2) blocks any hard gate — both are advisory/reading-level
findings. Recorded here rather than corrected silently, since fixing (2) in
particular means re-authoring the hook's entrance timing and re-rendering,
which is a real content change, not a QA-doc correction.
