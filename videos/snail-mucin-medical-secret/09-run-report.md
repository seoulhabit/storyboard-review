# Run report — snail-mucin-medical-secret

Skill version 2.1.0. Written last.

## Summary

- Mode: `render`
- Result: `complete`
- Artifacts: `7` written under OUT (2 modified compositions sets + 5 new files; 10 source files edited)
- Spend: `$0 of $0` (0 % — no paid provider call and 0 vidIQ credits in render mode)
- Needs Kim: `the publish click` — and a decision on the two judgement calls in *Left for you* below.

**What this was.** A re-gate of the shipped 2026-08-29 render against v2.1, then the fixes.
Ten rule violations were confirmed on measurements, not inference; all ten are fixed and re-verified
on the shipped pixels. The engine's own `check` passed the original render with **0 errors** — every
one of the ten was invisible to it.

**The one that mattered most.** `captions.html` declared its burned-in caption band at **y 1600–1920**:
the whole band sat inside the Shorts bottom-20 % UI rail, under YouTube's title, channel and audio
attribution. On a channel where **88.1 % of views come from the muted Shorts feed**, the captions are
the content, and they were being drawn under the platform's own chrome for the entire video. Moved to
y 1300–1520, which required shifting six lower-third elements across five scenes to make room.

**Also fixed:** 4 plain crossfades + 1 push-slide on a Short that the rule says must be hard cuts
(verified: boundaries now jump in 1 frame, previously ramped over 6 and 3); `box-sizing: border-box`
missing from 7 of 7 sub-compositions; 8 sub-floor type declarations, the smallest **15.9 px**; two
contrast failures on rendered pixels (**3.04:1** and **2.95:1**) that `check` passed 24/24; a missing
motion sidecar, which on its first run immediately caught a 1.52 s frozen window nothing else saw; and
a shipped true peak of **−0.4 dBFS**, now **−2.3**.

**Two audit passes were needed, and the second one is the lesson.** My first pass scanned scene files
and missed the registry components, whose `cqw`/`cqh` type resolves against the **mount box**, not the
canvas — 15.9–19.5 px inside their 756 px mounts, and my own safe-area narrowing had made them *worse*.
The mandatory `design-critique` frame gate caught it. The fix then failed silently once, because
`grid-card-assemble` overwrites the very custom properties it documents as inputs; that was caught on
the pixels a second time and fixed at its four real binding constants.

**Left for you — two judgement calls I did not make unilaterally:**
1. **Frame zero is a bare archival photo with no claim on it.** It is not blank and not mid-fade, so it
   clears `[S6/A-3]`, but for a Short frame 0 *is* the thumbnail and the scroll-stop, and this one states
   nothing. Fixing it is a packaging decision (S3), which `render` mode does not run.
2. **One 2.50 s static hold remains at 88.0–90.5 s**, sitting exactly on the 2.5 s ceiling (down from
   4.0 s). Scene 5's upper half is also empty for ~10 s there. Both are composition-shape questions, and
   I had used the `[S7/R-2]` re-render budget.

## Stages

| Stage | Ran / skipped | Gate result | Tool calls | Minutes |
|---|---|---|---|---|
| S0.0 Environment | ran | pass | `test -d`, `ffprobe`, `npx hyperframes --version`, `git rev-parse` | 3 |
| S0 Baseline | skipped (mode=render) | — | — | — |
| S1 Story | skipped (mode=render) | — | — | — |
| S2 Topic gate | skipped (mode=render) | — | — | — |
| S3 Packaging | skipped (mode=render) | — | — | — |
| S4 Script + VO | skipped (mode=render) | — | — | — |
| S5 Beat sheet | ran (read-only) | pass — VO/beat timing unchanged | `ffprobe` ×6 on VO | 4 |
| S6 Composition | ran | auto-fixed ×54 | Skill `frontend-design`, 6 patch passes | 62 |
| S7 Render QA | ran | pass (2 of 3 fix cycles; 2 of 2 re-renders) | `hyperframes check` ×4, `render` ×3, `snapshot` ×2, `ffmpeg`/`ffprobe` ×40+, `check-safe-area.py` ×3, `check-static-hold.py` ×3, Skill `design-critique` | 96 |
| S8 Publish envelope | skipped (mode=render) | — | — | — |
| S9 Readout schedule | skipped (mode=render) | — | — | — |

## Skills and tools invoked

| Stage | Invocation | Result |
|---|---|---|
| S6 entry | `COMPANION-RESOLVED:frontend-design (skill-tool)` | Flagged that collapsing the 04 chip and counter to one size flattened a deliberate hierarchy → chip restored to 2.7cqw over the counter's 2.5cqw. |
| S7 | `COMPANION-RESOLVED:design-critique (skill-tool)` | **Found two defects the source audit missed** — component type at 15.9–19.5px, and the 2.95:1 eyebrow. |
| S7 | HyperFrames CLI `check` ×4, `render` ×3 (1 stopped), `snapshot` ×2 | pinned `0.8.17` |
| S7 | `catalog/tooling/check-safe-area.py` ×3, `check-static-hold.py` ×3 (re-calibrated copy) | exit 0 / findings triaged |
| — | vidIQ MCP | **not called** — render mode makes no vidIQ decision |
| — | Higgsfield / Gemini | **not called** — no new plates needed |

## Rules fired

30 rules fired. The five that changed the outcome:

1. **`[S7/R-2]` safe area** — moved the entire caption band out of the Shorts bottom rail, plus all top
   chrome and every right-edge margin. The single highest-impact fix in the run.
2. **`[S6/A-8]` transition system** — 4 crossfades + 1 push-slide → 5 hard cuts, verified on frame diffs.
3. **`[S7/R-1b]` motion sidecar** — created from nothing; caught a real 1.52 s freeze on its first run.
4. **`[S6/A-6]` type floors** — 8 sub-floor declarations raised, including the component-mount class of
   defect that needed a second audit pass and a second fix attempt.
5. **`[S7/R-3]` AAC headroom** — shipped true peak −0.4 → −2.3 dBFS, re-measured on the delivered MP4.

Full list: `00-decision-ledger.md`.

## Spend

| Provider | Stage | Est. USD |
|---|---|---|
| vidIQ | — | $0.00 (0 credits — no call) |
| Higgsfield | — | $0.00 (no call) |
| Gemini | — | $0.00 (no call) |
| Local render (CPU) | S7 | $0.00 |

Total: **$0.00** of cap (0 %). Logged to `<CHANNEL>/spend.jsonl`.

## Artifacts

```
00-environment.md                                            2.0 KB   new
00-decision-ledger.md                                       14.7 KB   new
09-run-report.md                                             this      new
index.motion.json                                            2.2 KB   new  (R-1b sidecar)
renders/snail-mucin-medical-secret_2026-09-03_v2.1.mp4      94.1 MB   new  (shipped deliverable)
renders/snail-mucin-medical-secret_2026-09-03_v2.1.raw.mp4  94.1 MB   new  (pre-master)
renders/snail-mucin-medical-secret.srt                       2.4 KB   new
renders/snail-mucin-medical-secret.vtt                       2.4 KB   new
```

Source modified (10 files): `index.html`, `compositions/captions.html`,
`compositions/frames/{01-hook,02-intro,03-chemistry,04-snail-spa,05-sponge-rule,06-outro}.html`,
`compositions/components/{grid-card-assemble,split-tilt-cards}.html`.

The 2026-08-29 render is **kept**, not overwritten, so the before/after is reproducible.

## Skipped and why

- **S0, S1–S4, S8, S9** — not in `render` mode. No story, packaging or envelope work was requested or done.
- **vidIQ entirely** — render mode makes no data-gated decision, so no credits were spent. The channel
  baseline was read for context, not rewritten.
- **`[S6/A-9]` continuity (camera path / actor map)** — long-form only; this is a Short.
- **`[K-1]`–`[K-5]` claim classification** — the `K-*` floor applies undelegated, but re-deriving a claim
  table is S1/S4 work that `render` mode does not run, and no claim wording was changed by this run. The
  rendered-claim check `[K-4]` was **not** performed. If this video's claims have never been classified,
  that is a real gap and it needs a `full` or targeted pass, not this one.
- **A third re-render** — `[S7/R-2]` allows 2, and both were used. The residual 2.50 s hold is reported
  rather than fixed.
- **`hyperframes snapshot` as a cheap verification path** — abandoned: it rendered a component with its
  default variables instead of the mount's, so it cannot stand in for a render on variable-driven content.

## `[NOT IN SKILL]` findings

Five, all appended to `<CHANNEL>/policy-change-proposals.md` (never edited into `decision-policy.md`):

1. `[S6/A-8]` gives no retiming procedure for converting a crossfade to a cut.
2. `[S7/R-2]` assumes there is room to move content out of the reserved zones.
3. `[S6/A-6]` does not say which box component type resolves against (mount, not canvas).
4. A component may overwrite the custom properties it documents as inputs — verify on pixels.
5. `hyperframes snapshot` does not apply a mount's `data-variable-values`.

Plus one calibration note worth carrying: `catalog/tooling/check-static-hold.py` ships with
`CAPTION_BAND_EXCLUDE = False` and a comment asserting the project has no burned-in captions. That is
false for this project, and with the band included the moving captions mask a frozen hero region. It
must be re-derived per project — which is what surfaced two of the three static holds.

## Next readout

**No readout is scheduled by this run** — S9 did not run, and nothing has been published. A readout is
triggered by the publish click; at that point run `video-readout` at 48 h and 7 d and compare against
`curve.p50_48h`, `avg_view_pct_short` and `ctr_short` in `<CHANNEL>/baseline.yaml`.

Because this run changed caption placement, cut structure and type size but **not** the title, thumbnail
or hook, a retention delta would be attributable to the render changes; a CTR delta would not.
