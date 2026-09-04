# Branch Register (WO-SBR-001, T2)

Captured 2026-09-04, after T1's safety snapshot (4 WIP branches created, 9
branches pushed — see `docs/wo/GATE0-2026-09-04.md` §0 and the T1 report
below). All ahead/behind figures are `origin/master...<branch>` via
`git rev-list --left-right --count`, read as `behind / ahead`. "Already
merged?" is verified via ahead=0 (equivalent to `merge-base --is-ancestor`),
not inferred.

## Cluster 1 — `.claude/skills/faceless-video-craft/SKILL.md` (single-file, 4 branches, same edit at different stages)

| Branch | Last commit | Behind/Ahead | Merged? | Files | Open PR | Artefacts | Disposition |
|---|---|---|---|---|---|---|---|
| `claude/laughing-goldberg-1a051f` | 2026-08-31, sumit | 99 / 1 | No | 1 (SKILL.md) | **#1 (open)** | none new | **MERGE** — confirmed the fullest version (see below) |
| `rescue/34cf30b` | (local only — origin deleted during Gate 0, see GATE0 report §5) | 119 / 1 | No | 1 (SKILL.md) | none | none new | **DROP** — superseded |
| `rescue/f3f95d3` | 2026-08-31, sumit | 105 / 2 | No | 1 (SKILL.md) | none | none new | **DROP** — superseded |
| `claude/eager-cori-d241cf` | 2026-08-31, sumit (4 days stale) | 105 / 1 | No | 1 (SKILL.md) | none | none new | **DROP** — superseded |

**Verified, not assumed:** diffed all three non-PR branches against PR #1's content for this exact file. PR #1's version is a strict superset — it contains two additional edits (a documentation paragraph, and a 72-line section removal) that none of the other three have. All three are earlier snapshots of the same underlying edit, most likely artefacts of the `reset --hard` incident CLAUDE.md documents (two are literally named `rescue/*`). **Disposition rationale: merge PR #1 alone; the other three add nothing PR #1 doesn't already have, and merging them too would just replay an incomplete version over the complete one.** `rescue/34cf30b`'s origin copy was already deleted mid-Gate-0 (unconfirmed whether intentional — see open question in GATE0 report); the other two DROPs are proposed, not deleted (Rule 2 — Kim's call).

## Cluster 2 — `hyaluronic-acid-vs-filler` (triple, heavily overlapping, no two are ancestors of each other)

| Branch | Last commit | Behind/Ahead | Merged? | Files | Open PR | Artefacts | Disposition |
|---|---|---|---|---|---|---|---|
| `claude/hyaluronic-acid-video-rerender-8abe8c` | 2026-09-04 05:59, sumit | 16 / 1 | No | 103 | **#12 (open)** "v3: conversational rewrite, human subject, 17-scene restructure" | none new | **ASK** |
| `wip/hyaluronic-acid-video-rerender-8abe8c-2026-09-04` | 2026-09-04 (T1, this session) | 16 / 2 | No | 145 (103 + 42 QC files) | none (companion to #12) | none new | **ASK**, same call as #12 — these 42 untracked render-verification files (contact sheets, frame captures, loudnorm log) belong to PR #12's work; fold in if #12 is taken |
| `wip/hyaluronic-acid-video-rewrite-1ab509-2026-09-04` | 2026-09-04 (T1, this session) | 7 / 1 | No (tip was already on master before T1's WIP commit) | 83 | none | **`BEFORE-AFTER-REPORT.md`** — see OPEN-ITEMS.md #1-#3 | **ASK** |
| `wip/main-tree-2026-09-04` | 2026-09-04 (T1, this session) | 49 / 1 | No (tip was already on master before T1's WIP commit) | 64 | none | none new | **ASK** |

**Verified, not assumed:** pairwise `diff --name-only` shows all three genuinely overlap on the SAME core files — `03-beat-sheet.json`, every `04-assets/vo/*.wav`, `build_vo.py`, `script.md`, `build_actors.py`, `build_beats.py`, `05-composition/index.html`/`index.motion.json` — not just "same project, different scenes." This is one video with three independent, uncoordinated rewrites in flight:

- **#12** calls itself "v3... 17-scene restructure, human subject" (conversational format).
- **wip/hyaluronic-acid-video-rewrite-1ab509** *also* calls itself "v3" in its own `BEFORE-AFTER-REPORT.md` (120.359s, 14 scenes, 12 VO turns, single narrator) — **a direct naming collision with #12**, see OPEN-ITEMS.md #2.
- **wip/main-tree** sits on top of the version already on master (v2/PR #11, "single-narrator, 2:40") with a further, different WIP round ("single-narrator 160s cut" per its own commit message) — a *fourth* distinct point in this video's history if counted separately from the other three.

None of these three can be merged blindly — a git merge would produce extensive conflicts on the exact same files, and even a clean auto-merge would silently interleave three different creative directions into one file. **This needs Kim's explicit call on which version (or which parts of which) ships**, not a git operation. Proposed as `ASK` for all three, not `MERGE`/`DROP`/`CARRY`.

## Cluster 3 — `ectoin-survival-molecule` (two independent, diverged, full rebuilds)

| Branch | Last commit | Behind/Ahead | Merged? | Files | Open PR | Artefacts | Disposition |
|---|---|---|---|---|---|---|---|
| `claude/ectoin-voice-timing-revision-825e2c` | 2026-09-04 09:24, sumit (finished agent #1) | 7 / 5 | No | 172 | none | none new | **ASK** |
| `claude/voice-animation-sync-409a0a` | 2026-09-04 12:07, sumit (finished agent #2) | 7 / 6 | No | 134 | none | none new | **ASK** |

**Verified, not assumed:** these are the two worktrees confirmed live during this session (see GATE0 report). Diffed against each other directly: overlap is **near-total** — nearly every file in `videos/ectoin-survival-molecule/` (all 29 VO tracks, all 29 scene frames, captions, scripts, `index.html`) appears in both diffs. `merge-base --is-ancestor` checked both directions: **neither contains the other** — they forked from the same already-on-master commit (`1d38a897`) and diverged independently. Commit messages suggest they may have been *intended* as sequential ("Step 1: build and validate the mechanism" vs. "rebuild scene timing... for retention"), but git history shows two parallel, complete rebuilds, not a sequence. **Proposed `ASK`** — Kim needs to determine which (if either) is the intended continuation, or whether they need manual reconciliation of two independently-finished builds of the same video.

## Cluster 4 — clean, independent work (no overlap found)

| Branch | Last commit | Behind/Ahead | Merged? | Files | Open PR | Artefacts | Disposition |
|---|---|---|---|---|---|---|---|
| `claude/snail-mucin-bottle-animation-1d3308` | 2026-09-04 07:08, sumit | 1 / 3 | No | 81 | **#14 (open)** | none new | **MERGE** |
| `session/ectoin-normal-person` | 2026-09-03 16:22, sumit | 32 / 10 | No | 233 | none | none new | **MERGE first** (see below) |
| `claude/faceless-video-feedback-6c6c24` | 2026-09-03 19:38, sumit | 16 / 12 | No | 245 | none | none new | **MERGE after** `session/ectoin-normal-person` |
| `claude/kbeauty-ingredient-video-675976` | 2026-09-03 15:42, sumit | 16 / 12 | No | 84 | none | none new | **MERGE**, expect a small conflict (see below) |
| `wip/storyboard-6a-2026-09-04` | 2026-09-04 (T1, this session) | 14 / 1 | No (tip was already on master before T1's WIP commit) | 1 | none | none new | **MERGE** — trivial, one raw render file, no overlap |
| `session/story-board-6a` | 2026-09-04 05:57, sumit | 14 / 0 | **Yes** | — | (was PR #13, merged) | none new | **DROP** — nothing left to merge |
| `session/story-board-a1` | 2026-09-03 09:16, sumit | 29 / 0 | **Yes** | — | (was PR #11, merged) | none new | **DROP** — nothing left to merge |

**Ordering note, verified not assumed:** `git merge-base --is-ancestor origin/session/ectoin-normal-person origin/claude/faceless-video-feedback-6c6c24` → true. `faceless-video-feedback-6c6c24` already contains every commit from `session/ectoin-normal-person` — it's a linear descendant, not a competing line. Merging `session/ectoin-normal-person` first and `faceless-video-feedback-6c6c24` second should be conflict-free (the second branch already carries everything the first contributes).

**Expected conflict, verified not assumed:** `kbeauty-ingredient-video-675976` and `faceless-video-feedback-6c6c24` both modify two shared channel-level files — `videos/_channel/policy-change-proposals.md` and `videos/_channel/spend.jsonl`. Both look like append-style logs; a real but likely mechanical conflict (concatenate rather than pick-a-side), not a design disagreement.

## Not covered here (infrastructure, not content)

- `session/wo-sbr-001-gate0` — this WO's own working branch (Gate 0 report, branch register, open-items register, this file). Not part of the video/content reconciliation; folds into the `integrate/2026-09-04` branch at T5 per the work order's own design, or can be merged directly to master earlier as pure documentation — Kim's call, lower stakes either way.

## Summary

| Disposition | Branches |
|---|---|
| **MERGE** | `claude/laughing-goldberg-1a051f` (#1), `claude/snail-mucin-bottle-animation-1d3308` (#14), `session/ectoin-normal-person` → `claude/faceless-video-feedback-6c6c24` (in that order), `claude/kbeauty-ingredient-video-675976`, `wip/storyboard-6a-2026-09-04` |
| **DROP** (proposed, not executed — Rule 2) | `rescue/34cf30b`, `rescue/f3f95d3`, `claude/eager-cori-d241cf`, `session/story-board-6a`, `session/story-board-a1` |
| **ASK** (Kim's creative/product call, not a git decision) | `claude/hyaluronic-acid-video-rerender-8abe8c` (#12) + its WIP companion, `wip/hyaluronic-acid-video-rewrite-1ab509-2026-09-04`, `wip/main-tree-2026-09-04`, `claude/ectoin-voice-timing-revision-825e2c`, `claude/voice-animation-sync-409a0a` |

7 of 18 branches are ready to merge with a clear, verified rationale. 5 are safe, verified-redundant drops. **6 branches, across two video projects, need Kim's judgment before any merge** — these are not git conflicts to resolve mechanically, they're genuinely competing creative directions on the same content.
