# T0 (review pass) — Gate 0 review + asset inventory — DONE
Commits: `Story Board` branch `session/wo-fvc-006-gate0` off `master` `76af03e`, isolated worktree per `CLAUDE.md`.

## Scope of this pass

Not a WO-006 task execution. This is the review pass requested before any
T1+ work starts: fact-check the WO against the repo state it was drafted
against, correct what's stale, and produce a Gate 0 sheet answerable from
the record where possible. No generation spend, no renders, no T1+ artifacts.

## What shipped

1. **Moved the WO out of the shared tree.** It was untracked on `master`
   at session start (`CLAUDE.md`'s highest-risk state — no reflog, no
   recovery). Copied to `/tmp`, then into this worktree, diffed identical,
   committed (`bd63e34`), then removed the now-redundant untracked copy from
   the shared tree. `./worktree.sh status` confirms the shared tree is back
   to 0 untracked.

2. **Fact-checked the WO against the live repo** via three parallel Explore
   agents (repo/WO history, design system/assets, tooling/source file) plus
   direct verification of the highest-load-bearing claims. Found:
   - 3 of 6 Gate 0 questions already ruled by Kim under WO-FVC-005, dated
     the same day this WO is dated (`docs/wo/GATE0-FVC-005.md`).
   - A beat-sheet compiler (`videos/_system/COMPILER.md`) merged under
     WO-005 that the WO never mentions and that would refuse the build as
     specified (imagery, duration ceilings, font inlining, component
     naming).
   - Higgsfield defaults into G0-4 silently while two standing WOs
     (FVC-004, FVC-005) retire it out of lane.
   - The asset sweep (§4) omits `catalog/` entirely, despite `CLAUDE.md`'s
     first section mandating it be checked first.
   - Three source-file facts the WO states incorrectly or not at all: 720p
     (not 1080p), +1.0 dBTP already-clipping audio, single mono stream.
   - Several "carried verbatim" rulings (R-1, R-2, K-2b) that are misquoted
     or, in R-SRC's case, net-new.

3. **Ran the asset inventory** (`wo/FVC-006/ASSET-INVENTORY.md`), ahead of
   ruling on G0-2/G0-4 rather than after, since it's free and changes what
   those rulings are decided against. Opened and read every candidate
   (README + `file`/`identify` on the binary, not filename-matched).
   Headline: `catalog/visual-components/skin-band/` may already be style
   frame #2's mechanism; `material-triptych/` is close to this video's
   actual thesis; `unsourced-flag/` is a ready-made K-2b disclosure
   treatment. Net-new generation still looks needed for scene system 1 and
   ingredient-specific beats — the WO's 85–95%-net-new estimate does not
   survive contact with `catalog/`, but this doesn't fully resolve G0-2.

4. **Appended `docs/wo/WO-FVC-006-credibility-gap-remake.md` §7**
   (corrections, dated, per house convention — WO-FVC-004 §8 / WO-FVC-005
   §8 precedent). §0–§6 left untouched. 10 numbered subsections, each with
   file:line citations.

5. **Wrote `wo/FVC-006/GATE0-FVC-006.md`** — closes G0-1/G0-5/G0-6 from
   citation, restates G0-2/G0-3/G0-4 at their real scope, and adds two new
   gates this review surfaced: G0-7 (prove one T6 chapter before all six)
   and G0-8 (compile vs. hand-author, largely downstream of G0-2).

## Refusals on record

- **Did not rule on G0-2/G0-3/G0-4/G0-7/G0-8 myself.** These are Kim's
  calls per the WO's own Gate 0 discipline ("no default" on G0-2; G0-4
  promoted to required by this review). Presented the asset-inventory
  evidence so they can be answered with real numbers, not guessed at.
- **Did not edit the WO's own §0–§6 body** to fix the errors found. House
  convention (WO-FVC-004 §8 precedent, WO-FVC-005's explicit refusal to
  edit its own body for the same reason): corrections land as a dated
  appendix.
- **Did not start T1** (audio extraction/transcript) or any task requiring
  Gate 0 to be closed. This pass is upstream of T0 as the WO defines it.
- **Did not spend any generation credits or touch Higgsfield/HeyGen.**

## Verification performed

- `videos/_system/MANIFEST.json` — re-verified the design-system extraction
  is what it claims to be (component/token files read directly, not
  assumed from the manifest's own description).
- `catalog/manifest.json`'s `approved_surfaces` field — read directly, not
  paraphrased from a README, since it's the strongest evidence for G0-2's
  real scope.
- Every asset-inventory reuse candidate — README read in full, binary
  checked with `file`/`identify` for actual dimensions, not inferred from
  filename or prose claim.
- `ffprobe`/`ffmpeg -af ebur128` run directly against the source file in
  `~/Downloads/` for §7.7's source-facts corrections.
- `git branch --show-current` and `git log --oneline -1` checked
  immediately before each commit.

## Next step — UPDATED 2026-09-07

Kim ruled directly on G0-2, G0-3, G0-4, and G0-8 this session (G0-7 was
already ruled earlier); recorded in `wo/FVC-006/GATE0-FVC-006.md` with full
citations. Two rulings (G0-2 full imagery, G0-4 re-authorize Higgsfield)
are deliberate reversals of WO-FVC-004/WO-FVC-005 decisions, flagged as
such rather than silently overwritten. Gate 0 is now fully closed.

T0–T4 are unblocked and can start. G0-8's compiler extension is now fully
scoped as **T4.5** in `wo/FVC-006/T4.5-compiler-image-ref-scope.md` —
grounded directly in the real `compile_composition.py` (exact staging
pattern to mirror, exact line the image attaches to), a `ShScene`-level
design recommendation, and a correction to this file's original G0-4 text
(no dormant Higgsfield row exists to un-retire; a new one gets added).
T5 (style frames) is gated on T4.5 landing. Who owns T4.5 — a sub-task of
this WO, or a separate prerequisite WO — is still open (T4.5 §6); doesn't
block T0–T4 from starting now.
