# 07-publish-envelope.md — centella-asiatica

**Draft only. Nothing written to YouTube (`E-1`).** Kim's click is what
publishes this, not this file's existence.

## Title

What human studies say about Centella Asiatica

## Description

A 45-second evidence check on centella asiatica (cica): what the human
studies actually tested, the safety data, and who should patch test first.

Sources: `content/ingredients/centella-asiatica.json` and
`content/findings/centella-asiatica.json`, seoulhabit-learn @ `cacff81`.
Full sourcing: seoulhabit.com/ingredient/centella-asiatica

## Tags

centella asiatica, cica, gotu kola, k-beauty, korean skincare, skincare
science, skincare ingredients, evidence-based skincare

## Chapters

Not applicable — Shorts carry no chapter markers.

## Pinned comment (draft)

"Full sourcing (12 citations, EMA/CIR/peer-reviewed) at
seoulhabit.com/ingredient/centella-asiatica — this isn't medical advice,
patch test if you're sensitive."

## End-screen map

Frame 0 (`ShHook`, "It's in your cream. Is it working?") is both the hook
and the Shorts thumbnail (`P-3`). Last scene (`ShEndcard`) carries the
SeoulHabit wordmark/tagline/CTA per `C-3a` — no separate long↔Shorts
cross-link (`format: short` only this run, no long-form derivative per
`F-2`'s own `format: absent → single format` default read against
`request.yaml`'s explicit `format: short`).

## Format

Short (9:16) only, per `S-1` branch 2 (channel is 95.8% Shorts). No `format:
both` requested.

## Gate state at time of draft (for the record, not a publish blocker per se)

`06-render/9x16/qa.json` verdict: `fail` — `H-3` (faceless) mechanically
fails on 2 Haar-cascade detections, both **visually confirmed as false
positives on bold typography** (no imagery anywhere in this design system;
frames archived at `06-render/9x16/h3-verification/`). `H-4.contrast` fails
(advisory only — the muted citation-chip token, `--chip-opacity: 0.4` by
design, measures low contrast; not yet validated against a corpus per
`policy.md`'s own note on this gate). Every other gate (canvas, safe-area,
static-hold, loudness, duration, type-floor) passes for real, including
`H-2` frame zero. See `09-run-report.md` for the full account before Kim
clicks publish.
