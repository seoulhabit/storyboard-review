# Run report — ectoin-normal-person (verdict-compression revision)

Written last, every mode, whether or not S9 itself ran.
Skill version: 2.1.0.

## Summary

- Mode: `full (revision)` — S0.0 ran; S1 (claims) ran fresh against live
  data; S2 (script) ran; S3 (VO) ran; S4/S5 (storyboard/composition) ran;
  S6 (validation) ran to a clean gate; S7 (preview) opened — **render not
  run, awaiting explicit operator approval per non-negotiable #14**; S8/S9
  out of scope for this request.
- Result: **complete except the render itself**, which is gated on approval
  by design, not by an unresolved defect.
- Artifacts: source restored/located (no `.pyc` problem existed — see
  §Restoration below), `CLAIMS.md` (new), `SCRIPT.md` + `scripts/vo_lines.py`
  rewritten, 16 of 44 VO takes regenerated, `frames_spec.py` rewritten for
  8 units, GSAP vendored, DOM ids prefixed project-wide, music bed + 14 SFX
  cues added, `hyperframes check` clean (`ok: true`), pixel-verified against
  all 17 sub-compositions plus the verdict window, Studio preview opened
  and confirmed live.
- Spend: ~2.1 Higgsfield credits (21 `generate_audio` calls at 0.1 each,
  including retries against a persistent rate limit) against a 2275.25-credit
  balance. Negligible against the $5.00/200-credit per-run cap.
- Needs the operator: **render approval.**

This is a **second revision** of an already-shipped, gate-clean build. The
first (cold-open) revision moved the "11% bottle → blend → turn it around"
reveal to open the video. This one responds to a new brief with four content
requirements the cold-open revision did not carry: a claim ledger, removal
of a knowingly false line, a verdict inside the first 20 seconds, and
compression to 35–45 turns / ~430–500 words. Full account: `BRIEF.md`
§Verdict-compression revision, `SCRIPT.md` §Changes, `CLAIMS.md`,
`00-decision-ledger.md`.

## §Restoration — non-negotiable #1

**There was no `.pyc` problem.** Zero `.pyc` files and zero `__pycache__`
directories exist anywhere in this repository — checked directly, not
assumed. Two distinct ectoin projects exist: `videos/ectoin-survival-
molecule` (a single-narrator monologue with no SoulHabit/Jay dialogue, not
the target) and `videos/ectoin-normal-person` (the SoulHabit/Jay two-hander
this brief describes), both with complete, readable Python source. The
latter's most recent build existed only at commit `f893e7b` on a different,
concurrently-active worktree's branch — imported via `git checkout f893e7b
-- <paths>` onto this worktree's own branch and committed immediately as a
checkpoint before any edits, per this repo's own concurrency convention
(CLAUDE.md §"What a worktree does NOT protect" — no ref surgery on a branch
not checked out here).

## Stages

| Stage | Ran / skipped | Gate result |
|---|---|---|
| S0.0 Environment | ran | `00-environment.md` written fresh; CLI re-pinned 0.8.22→0.8.27 |
| S0/catalog | ran | searched for count-up/transition/ducking/dialogue primitives — nothing adopted, project's own mechanisms already superior |
| S1 Claims | ran | `CLAIMS.md` written from live PubMed queries (2026-09-03), not copied forward. 2 corrections found: Bow 2021's dry-condition finding does surface in PubMed (prior revision's record was wrong); Marini 2013 has 2 bitop-affiliated authors, not 1. `t048` flagged for removal |
| S2 Script | ran | 58 turns/595w → 44 turns/489w. Both required bands met. Runtime overshoot vs the brief's 3:00–3:30 logged as a deliberate consequence of the operator's "word count wins" decision |
| S3 VO | ran | 16/44 turns regenerated (Higgsfield `generate_audio`); 5 first-pass takes failed this project's own mid-word QC and were re-rolled clean; 0 dead takes, 0 mid-word takes in the final set |
| S4/S5 Storyboard + composition | ran | `frames_spec.py` rewritten for 8 units; GSAP vendored; DOM ids prefixed centrally (2 dynamic-selector bugs found and fixed after the first pass shipped 156 runtime warnings); 3 redundant CSS transform initializers removed; music bed + 14 SFX cues added |
| S6 Validation | ran | `check-tokens.py`/`contrast.py`/`check-dead-sets.py` clean; `hyperframes check --samples 60`: **ok: true**, 0 errors (3 real bugs found and fixed by the check itself, not assumed clean); `continuity-audit.py --gate`: pass; pixel-verified against all 17 sub-compositions + frame 0 + the verdict window; phone-scale (25%) legibility confirmed |
| S7 Preview | ran | Studio opened (`hyperframes preview`, port 5677), live playback/scrubbing confirmed, matches pixel verification. **Render not run — awaiting approval** |
| S8 Publish envelope | not run this request | out of scope |
| S9 Readout | not run this request | out of scope |

## Companion-skill gates

- `frontend-design`: not re-invoked this revision — the token/type-floor/
  contrast lens was already applied and passed in the prior (cold-open)
  revision, and this revision's changes are structural (turn/phase counts,
  id prefixing, audio) rather than new visual design. `COMPANION-MISSING`
  is not the right token here since it was resolved previously on the same
  project; noting the gap explicitly rather than silently skipping it.
- `design-critique`: **not yet run** — this gate fires at S7 on extracted
  render frames; since no render has been produced this revision (S7 opened
  the live preview only, per the approval gate), there are no fresh render
  frames to critique yet. Will run against the actual render output once
  approved, before delivery is considered complete.

## Tools invoked

- Higgsfield MCP `generate_audio` / `generate_audio_batch`: 21 calls (16
  first-pass + 5 re-rolls), 0.1 credits each.
- `hyperframes` CLI 0.8.27: `upgrade`, `catalog --query` (x3), `check
  --samples 60 --json --snapshots` (x5, iterating to clean), `snapshot`
  (x3, midpoints/frame-0/verdict-window), `preview`.
- WebFetch against NCBI E-utilities: ~15 calls verifying every claim in
  `CLAIMS.md` live.
- `python3` build pipeline: `build_frames.py`/`build_index.py`/
  `build_storyboard.py`/`build_captions.py`/`build_motion.py`, run in
  sequence after every source change (~10 full cycles across the revision).
- `ffmpeg`: VO trim/pad/QC (`gen_vo.py`), music-bed loop construction,
  phone-scale downscale renders for the legibility check.
- `catalog/tooling/`: `check-tokens.py`, `contrast.py`, `check-dead-sets.py`,
  `continuity-audit.py --gate`.

## Rules that fired

- `[K-1]`/`[K-2]`/`[K-2a]`/`[K-4]`: every claim classified and verified
  before rendering; no `treats`/`prevents`/`cures` language anywhere; the
  one unsourced claim (the illustrative "11%" bottle) ships with a muted
  `ILLUSTRATIVE LABEL` tag, never a citation pill.
- Non-negotiable #3 (this rebuild's brief): a knowingly false line does not
  ship for humour or operator preference — reverses the prior revision's
  own operator decision on `t048`.
- `[S6/A-8]`: no plain crossfade across a ground change — confirmed by
  `continuity-audit.py --gate`, unchanged from the prior revision (16
  wipe-based transitions, 0 hard cuts, 0 violations).
- `[S6/A-10]`: no timeline-wide `defaults:{ease}` — confirmed, 0 of 17.
- `[S7/R-1]`: `check` is the render gate; its errors gate the run — 3 real
  bugs (a JS syntax error, 2 id-prefixing gaps, 1 layout overlap) were
  found and fixed this way, not assumed away.
- `[S7/R-2]`: verify by pixels, never by manifest — every claim above about
  what renders is backed by an extracted frame in `snapshots/`.

## Next readout

Not scheduled — S9 is out of scope for this request, and nothing publishes
until the render is approved, mastered, gated, and a publish envelope is
separately requested.
