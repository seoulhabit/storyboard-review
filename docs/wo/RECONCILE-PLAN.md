# Reconciliation Plan (WO-SBR-001, T4) → Gate 1

Built from `docs/wo/BRANCH-REGISTER.md` (T2). This is a *proposal* — nothing
below executes until Kim rules MERGE / CARRY / DROP per branch. Only ruled
dispositions proceed to T5.

## Proposed merge order (7 branches — the uncontested set only)

Ordered fewest-overlaps-first, oldest-first within ties. Each step names the
test to run immediately after that merge, before moving to the next.

| # | Branch | Why this position | Test after merging |
|---|---|---|---|
| 1 | `claude/laughing-goldberg-1a051f` (PR #1) | Zero overlap with anything else in this list; single file (`.claude/skills/faceless-video-craft/SKILL.md`) | `ruff check . && mypy && pytest -q` (this branch touches no `videos/` content) |
| 2 | `claude/kbeauty-ingredient-video-675976` | Zero overlap with #1; oldest of the remaining branches (2026-09-03 15:42) | `ruff check . && mypy && pytest -q`, then `hyperframes check videos/kbeauty-label-trap` |
| 3 | `claude/snail-mucin-bottle-animation-1d3308` (PR #14) | Zero overlap with #1-#2 | `ruff check . && mypy && pytest -q`, then `hyperframes check` on whichever project this PR's diff touches (confirm exact path at merge time — title references a "bottle animation" scene replacement) |
| 4 | `session/ectoin-normal-person` | Zero overlap with #1-#3; **must precede #5** — it's a verified ancestor of `claude/faceless-video-feedback-6c6c24` (`merge-base --is-ancestor` confirmed true), not an independent line | `ruff check . && mypy && pytest -q`, then `hyperframes check videos/ectoin-normal-person` |
| 5 | `claude/faceless-video-feedback-6c6c24` | Depends on #4 being in first (see above) | **Expect a conflict here** — see below. After resolving: `ruff check . && mypy && pytest -q`, then `hyperframes check videos/ectoin-normal-person` |
| 6 | `wip/storyboard-6a-2026-09-04` | Zero overlap with anything; trivial (1 file, a raw render) | `ruff check . && mypy && pytest -q` (no check script needed for a single binary asset) |

**Expected conflict at step 5:** `claude/faceless-video-feedback-6c6c24` and
`claude/kbeauty-ingredient-video-675976` (merged at step 2) both modify
`videos/_channel/policy-change-proposals.md` and `videos/_channel/spend.jsonl`
— both append-style logs, so the likely correct resolution is keeping both
sides' additions (concatenate) rather than picking one side. **Per Rule 4,
whoever resolves this logs branch/file/which-side-won/why in
`docs/wo/RECONCILE-LOG.md` before continuing to step 6** — these are
JSON-lines and markdown, not binary/media, so Rule 4's "STOP and ask" trigger
doesn't apply, but the log entry is still required.

## Not in the merge order — 6 branches need Kim's ruling first

These are not git conflicts a merge order can route around — they're
genuinely competing, uncoordinated work on the same two video projects. Full
evidence in `docs/wo/BRANCH-REGISTER.md` Clusters 2 and 3; summarized here
only to frame the decision each needs:

**`hyaluronic-acid-vs-filler`** — pick one, blend, or sequence:
- `claude/hyaluronic-acid-video-rerender-8abe8c` (open PR #12) + its WIP
  companion `wip/hyaluronic-acid-video-rerender-8abe8c-2026-09-04`
- `wip/hyaluronic-acid-video-rewrite-1ab509-2026-09-04` (has a measured
  before/after report; also calls itself "v3," colliding with PR #12's own
  "v3" label — OPEN-ITEMS.md #2)
- `wip/main-tree-2026-09-04` (a further WIP round on top of the version
  already on master)

**`ectoin-survival-molecule`** — pick one or reconcile both:
- `claude/ectoin-voice-timing-revision-825e2c`
- `claude/voice-animation-sync-409a0a`
(these are the two agents this session tracked as active and confirmed
finished — neither is a continuation of the other; both are complete,
independent rebuilds forked from the same already-merged starting point)

**Once Kim rules on these six**, whichever are ruled MERGE slot into the
ordered list above whenever convenient (none of them overlap with the 7
already-listed branches — only with each other, within their own cluster).
Whichever are ruled DROP or CARRY follow Rule 2 / T8's carry procedure.

## Proposed for deletion (Rule 2 — proposed only, Kim rules, nothing deleted here)

| Branch | Why |
|---|---|
| `rescue/34cf30b` | Superseded — an earlier, incomplete snapshot of the exact edit PR #1 completes. Origin copy already gone (deleted during Gate 0's inventory pass — separately flagged in OPEN-ITEMS.md #5 for confirmation this was intentional). |
| `rescue/f3f95d3` | Same — superseded by PR #1. |
| `claude/eager-cori-d241cf` | Same — superseded by PR #1; also 4 days stale. |
| `session/story-board-6a` | Zero commits ahead of master — its content (PR #13) is already fully merged. |
| `session/story-board-a1` | Zero commits ahead of master — its content (PR #11) is already fully merged. |

## Test command reference

Per `docs/wo/GATE0-2026-09-04.md` §11: run locally, not via `gh pr checks` —
GitHub Actions has been failing at the infrastructure level (zero steps, ~5s
runs) on every branch including master since ~2026-09-04, so CI status is not
signal right now.

```
ruff check .        # excludes storyline.py, videos/
mypy                 # storyboard.py only
pytest -q            # tests/
hyperframes check <project-dir>   # per touched video project — videos/ is outside the three checks above
```

## After Gate 1

Once Kim rules per branch: T5 creates `integrate/2026-09-04` off
`origin/master`, commits `WO-SBR-001.md`, `OPEN-ITEMS.md`, and `docs/wo/`
together (per the work order's own T5 step — this branch's own commits,
listed in `docs/wo/GATE0-2026-09-04.md`'s revision history, fold in via
`git merge --no-ff session/wo-sbr-001-gate0` rather than being re-typed),
then merges ruled-MERGE branches in the order above, running the test after
each and logging every conflict resolution to `docs/wo/RECONCILE-LOG.md`
before continuing.

---
**STOP. Waiting for Kim's per-branch ruling (Gate 1) before T5 runs.**
