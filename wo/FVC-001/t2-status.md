# T2 — Merge and engine fixes — Accept checks actually run, 2026-09-03

At the time T2 itself ran, its Accept checks were recorded as blocked (no HyperFrames CLI on this machine). That changed once `story-board-78` installed the CLI here directly (see `t8-status.md`'s HANDBACK.md addendum). At Kim's request, they ran all four T2 Accept checks for real. I independently re-verified the two most consequential results myself before accepting either. This file is the read-back record; `merge-matrix.md` is unchanged.

## 1. merge-matrix.md empty verdicts — PASS

27 data rows (16 keep, 8 merge, 3 "keep, confirmed correct"), 0 empty. My own recount landed on a different raw number (31, via a looser grep pattern) but the substantive check — zero empty verdict cells — agrees either way.

## 2. `hyperframes check` on the skeleton — PASS, but the WO's literal Accept command doesn't work as written

Two real problems in the Accept text itself, both confirmed:
- `hyperframes check` takes a **project directory**, not a file — `check assets/composition-skeleton.html` errors "Not a directory" on the installed 0.8.26 CLI.
- The bare skeleton references `compositions/frames/*.html` sub-compositions that don't exist until S6 actually authors them — it cannot pass standalone.

Fixed by scaffolding a minimal real project around it (three authored scenes, a silent bgm) and running `check` against that directory: clean across lint/runtime/layout (9 samples)/motion/contrast, exit 0. Engine contract reconfirmed against the real, installed CLI (not just cross-referenced against docs, which is as far as T2 itself got): `#root` with `data-composition-id`/`data-start`/`data-duration`, GSAP paused timelines on `window.__timelines`.

## 3. Frame diff t=0 vs t=1s, Δ>0 — PASS, with a methodological caveat worth keeping

PSNR avg 15.35 (finite = differs; a t=0-vs-itself control gave `inf`, confirming the method detects identity correctly rather than always reporting difference). The caveat: the skeleton's own root-timeline transitions sit at 2.500s and 5.400s — nothing in the root timeline itself moves between 0 and 1s. The measured difference at that pair comes from the authored *sub-composition* scene content, not the skeleton's own choreography. `t=2.5` vs `t=2.73` (inside the actual push-slide transition) is the pair that exercises the root timeline, and gives PSNR 15.76 — also finite, also a genuine difference, just a more honest test of what this Accept item claims to check.

## 4. Lint vs `check` agreement on three fixtures — **FAIL, a real and reproducible disagreement**

- `clean.html`: lint 0 err / exit 0 · `check` 0 findings / exit 0 → agree.
- `fail_banned_raf.html`: lint 1 err / exit 1 · `check` reports `requestanimationframe_in_composition`, exit 1 → agree.
- `fail_lazy_image.html`: lint 2 err (`loading="lazy"`, missing `decoding="sync"`) / exit 1 · **`check` reports 0 findings, exit 0** → **disagree**.

**Independently reproduced myself**, not taken on the report alone: built the same fixture with the missing asset supplied (their setup note — all three initially false-failed on `missing_local_asset` before the asset was added) and ran the real, installed `hyperframes check .` against it directly. Result: `Lint ◇ 0 errors, 0 warnings`, exit 0 — while `scripts/lint_composition.py` on the identical file reports 2 errors and exits 1, exactly as reported.

**This is a genuine contradiction inside the WO itself, not a bug in either script.** `lint_composition.py` does exactly what T5 specified — T5's own text: *"missing `decoding="sync"` and remote render URLs are errors."* The real, shipped `hyperframes check` simply does not enforce `loading`/`decoding` on `<img>` as a lint error. T2's *Do* says "reconcile until findings agree" — as written, that cannot be satisfied without either (a) removing a check `lint_composition.py` was explicitly told to have, contradicting T5, or (b) the actual CLI growing a rule it doesn't have, which isn't something this WO controls.

**Not resolved unilaterally — this is Kim's call**, same as every other WO-vs-reality conflict this engagement has surfaced (T7's rule-ID collisions, T9's `claude plugin eval` gate). Two honest options, not a recommendation:
- Keep `lint_composition.py`'s stricter check (matches T5's literal spec; catches a real headless-renderer failure mode `check` currently misses) and accept that T2's "must agree" Accept criterion is unsatisfiable as written — document the divergence instead of chasing agreement.
- Drop the `loading`/`decoding` check from `lint_composition.py` to match `check`'s current behavior, accepting a real gap in coverage that a previous session (this WO's own T5 write-up) specifically called out as worth catching.

## T6 — still not run, in progress elsewhere

Structural pieces confirmed present (both templates, `S0.0` in `pipeline-runbook.md`, the `skipped (mode=<mode>)` convention in `run-report.template.md`). The behavioral Accept (an actual render-mode run producing `00-environment.md` and `09-run-report.md`) has not been executed yet. `story-board-78` was about to run it against a scratchpad copy — not the real `outputs/2026-09-01-how-to-repair-skin-barrier/` directory, correctly avoiding overwriting an existing pre-T6 render — but hadn't reported results as of this note. Update this file when they do.
