# Run report — hyaluronic-acid-vs-filler (v3 revision)

Skill version 2.1.0. Mode: full re-render.

## Summary

Rewrote the voiceover (13 → 24 shorter stems, curiosity-gap hook, natural
pacing, no gap-scaling to a preset runtime), added four photoreal plates of
one consistent female subject at the brief's four named moments, restructured
13 scenes into 17 with a real actor-continuity merge and a three-type
transition system, and re-rendered from scratch. Runtime is a **measured
output**: 165.186s (2:45.2), not a target the audio was stretched or
compressed to fit.

**Two real, previously-unfixed defects were found and fixed this run, both
by direct frame inspection rather than by trusting any automated gate:**

1. **Every hand-authored scene shipped a blank tail** — 0.35 to 1.10 seconds
   of hard, silent blank frame at the end of all 15 hand-authored scenes,
   caused by a root-wrapper/sub-composition duration mismatch that
   `hyperframes check`'s layout pass cannot see. Confirmed on the actual
   rendered MP4 (not just source), fixed centrally, re-rendered, and
   re-verified with the bug gone.
2. **The prior mux recipe under-mastered the audio** — the raw voiceover
   measured -25.9 LUFS with a near-0dBFS peak (a ~26dB crest factor), which
   defeats a plain `amix`+`loudnorm` chain. Fixed with a voice-bus
   (highpass → compressor → limiter) before the mix; shipped file measures
   -14.0 LUFS / -3.3 dBTP, verified on the decoded AAC, not the PCM
   intermediate. Also added `-movflags +faststart`, absent from every prior
   version's deliverable.

One hard gate (`check-safe-area.py --landscape`) reports 261 frames of "ink
in a reserved zone," confirmed by direct pixel inspection to be caused
entirely by the four full-bleed photo plates — a scene type this gate's
flat-background-only detection method was never built to evaluate. Filed as
a verified exception, not silently passed over; see `00-decision-ledger.md`.

Deliverables: rewritten script, voiceover + word-level timing + `.srt`/`.vtt`
captions, the regenerated HTML composition, the final rendered MP4, a
19-frame contact sheet, and the engagement-improvement list below.

## Stages

| Stage | Ran? | Notes |
|---|---|---|
| S0.0 Environment | yes | `00-environment.md` §v3 appended |
| S0 Baseline | skipped | fresh from the prior run, not re-probed |
| S1-S3 Story/Topic/Packaging | skipped | carried forward; no re-scoring |
| S4 Script + VO | yes | full rewrite, see ledger |
| S5 Beat sheet | yes | rebuilt from the new VO, 17 scenes |
| S6 Composition | yes | `build_beats.py` + `build_actors.py` both substantially rewritten |
| S7 Render QA | yes | 2 full render cycles (bug discovery, then the fix) |
| S8 Publish envelope | not touched | v2's envelope's claims/warning text still holds; not re-verified against the new script line-by-line beyond the [K-4] pass below |
| S9 Readout | not due | see Next readout |

## Skills and tools invoked

- `character-sheet` (Higgsfield MCP workflow) — built the shared identity
  description for the 4 plates.
- `design-critique` — `COMPANION-RESOLVED (skill-tool)`, S7, on the contact
  sheet and targeted full-resolution frames.
- `hyperframes transcribe` (local whisper, small.en) — word-level timing.
- `hyperframes snapshot` — contact sheet + targeted defect verification
  (also where the blank-tail bug's tail was first isolated to the
  composition itself, ruling out a render-only artifact).
- `hyperframes check` / `render` — pinned `0.8.22` throughout, never the
  global `0.8.27`.
- `catalog/tooling/{check-safe-area,check-static-hold,check-cadence}.py`,
  `continuity-audit.py` — all four, run independently (never `&&`-chained).
- Higgsfield `generate_audio`/`generate_audio_batch` (model `seed_audio`) —
  24 VO stems.
- Higgsfield `generate_image`/`generate_image_batch` (model `soul_v2`,
  internally `text2image_soul_v2`) — 7 image generations across 4 plates
  (`soul_cast` was attempted first; unavailable on this account's plan tier).

## Rules fired

`[S4/V-2]` VO is the master clock, measured not targeted — the central fix
this run. `[K-1]`-`[K-4]` claim table carried forward unchanged in
substance, re-verified against the new on-screen text — PASS, one disclosed
(not fixed) consideration on C0's chip timing. `[S6/A-1]` catalog-first for
imagery — Higgsfield routing per `providers.yaml`, `soul_cast` unavailable,
fell back correctly. `[S6/A-3]` frame-zero composed-not-faded — a real v2
gap, fixed and applied uniformly via `_compose_first()`. `[S6/A-7]` contrast
on rendered pixels — 13/13 pass. `[S6/A-8]` transition system — 3 types + 3
cuts, 0 crossfade-across-ground violations. `[S6/A-9]` actor continuity — one
real merge replacing a confirmed redraw, 0 rebuilt-actor pairs project-wide.
`[S6/A-10]` entrance signature — 18.2% top share, well under the 50%
template-failure line. `[S7/R-1]` `check` gates the run — 0 errors (2
accepted wipe-boundary findings, explicitly the documented exception class).
`[S7/R-2]` pixel gates — static-hold and cadence clean; safe-area hard-gate
failed and was overridden on verified evidence (see ledger). `[S7/R-3]`
audio mastering — voice-bus chain required again, faststart added.

## Spend

~21 Higgsfield credits on voiceover (24 generations) + ~0.84 credits on
imagery (7 generations) ≈ 22 credits ≈ **$0.44**, against a $5.00/run cap.
0 vidIQ credits (no S0-S3 re-run).

## Artifacts

| File | What |
|---|---|
| `04-assets/vo-stems.json` | rewritten script, 24 stems |
| `04-assets/vo.wav` / `vo.mp3` | the voiceover, 165.186s |
| `04-assets/transcript.json` / `captions.srt` / `captions.vtt` | word-level timing + caption sidecars, new this run |
| `04-assets/transcript-provenance.json` | source-wav hash/mtime the transcript was run against |
| `04-assets/manifest.json` | rewritten, every v3 asset with provenance |
| `05-composition/**` | fully regenerated, 17 scenes |
| `05-composition/assets/images/subject-0{1..4}-*.png` | the 4 photoreal plates |
| `06-render/final.mp4` | the deliverable, 165.186s, faststart, -14.0 LUFS |
| `06-render/contact-sheet-src/` | 19 frames + 3 grid contact sheets |
| `00-environment.md`, `00-decision-ledger.md`, `01-story-brief.md` | all appended with §v3 sections |

## Skipped and why

- S0/S1/S2/S3: baseline still fresh from the prior run; this was a targeted
  re-render on an already-scoped project, not a new topic.
- S8 publish envelope: not re-verified line-by-line against the new script
  text beyond confirming the [K-4] claim/hedge/citation set still holds —
  worth a pass before the actual publish click if the description or pinned
  comment quotes the old script verbatim anywhere.
- `frontend-design` companion: not re-invoked — no new token or component
  system introduced, existing S6 resolution from the prior run still applies.

## `[NOT IN SKILL]` findings, filed to `videos/_channel/policy-change-proposals.md`

1. `check-safe-area.py` has no way to evaluate a full-bleed photographic
   plate scene — its ground-detection method assumes a flat background.
   Needs either a `--allow-photo-bleed` flag or an exemption keyed off the
   beat sheet's own `scene.plate` field.
2. A hand-authored scene's own `scene_shell()`-equivalent must independently
   replicate the shared generator's wrapper-padding math (`dur + d_in +
   d_out`, every tween shifted by `+d_in`) or it ships a blank tail — this
   skill's own reference docs describe the padding for GENERATED scenes but
   never flag that a hand-authored one needs the identical treatment.
3. `hyperframes snapshot` does not correctly composite the outgoing scene
   during an active cross-scene transition window (confirmed: a real,
   correctly-compositing mid-wipe frame on the actual render read as fully
   blank in `snapshot` at the same timestamp) — verify a transition midpoint
   on the rendered MP4, never on `snapshot`, when the two disagree.
4. VO assembly must never scale silence gaps to hit a preset target runtime
   — the runtime is the VO's measured output, always.
5. The runbook's mux recipe is missing `-movflags +faststart`.
6. A voice-bus chain (highpass → compressor → limiter) before the mix is
   required whenever the source TTS measures a large loudness/peak crest
   factor (confirmed twice now on this same project, different VO takes) —
   the plain `amix`+`loudnorm` recipe should not be the default for a TTS
   source without checking this first.

## Deviations, stated rather than buried

- C0's citation chip does not appear until ~46s into the video (was
  chip-adjacent at frame zero in v2) — a deliberate trade for the new
  minimal curiosity-gap hook, disclosed in the ledger, not a rule violation
  (the claim remains sourced and its chip does appear later in the video).
- The safe-area hard gate reports a failure that is a confirmed tool
  limitation, not a composition defect — overridden on direct pixel
  evidence, filed as a proposal rather than silently ignored.
- `soul_cast` (the model built for cross-shot character consistency) was
  unavailable on this account's plan tier; consistency was achieved instead
  via `soul_v2` with an explicit image reference to an already-accepted
  shot. Works, but is a fallback, not the intended primary path.

## Next readout

48h and 7d per `learning-loop.md`, same as any publish — not scheduled
here, since the publish click has not happened. This run report is the
handoff point.
