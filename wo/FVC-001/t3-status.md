# T3 — Invocation: description, mode router, wrappers, paths — DONE

Two commits pushed to `github.com/seoulhabit/claude-skills`: `357fcb1` (description/mode-router/paths/channel-baseline) and `ee833c9` (five wrappers).

## Attestation (Accept checks, read-back)

**`wc -c` / char count of the description**
```
chars: 479   (<= 500 — PASS)
```
Note: the WO's own §4.1 text is 549 characters, already over its own stated 500-char cap. Trimmed the parenthetical mode descriptions out of the "Modes:" sentence (they're redundant with the new Mode table in the body) to bring it to 479 — same trigger words, same scope statement, under cap.

**`grep -rn "/mnt/" faceless-video-craft/`**
```
SKILL.md:51   OUT definition — "if that directory exists at run time"
SKILL.md:104  frontend-design discovery — one of three checked locations, "If it is absent, proceed"
SKILL.md:166  prohibition — "No file://, no /mnt"
references/pipeline-runbook.md:8    OUT definition, same guard
references/hyperframes-engine.md:170  prohibition, unchanged (already guarded)
references/decision-policy.md:818   OUT definition, same guard
references/decision-policy.md:821   historical/explanatory ("v2 once wrote... a hardcoded /mnt path that turned out not to exist")
```
All seven are conditional, a documented fallback, a prohibition, or explanatory — none assume `/mnt` exists. PASS.

**`ls wrappers/`**
```
produce  video-audit  video-package  video-readout  video-render
```
Five. PASS.

## What changed, beyond the three Accept checks

- **Mode router** added (`full | render | package | audit | readout`) with a runs/loads table, inserted before "Read order"; Read order's own two channel-baseline items were rewritten to point at the new `<CHANNEL>/baseline.yaml` convention instead.
- **A real bug found and fixed, not just documented**: `references/channel-baseline.md`, which T1's straight copy had pulled into the skill, turned out to hold the *actual* SeoulHabit channel's measured data (real subscriber count, view stats, channel id) — not a template. That's exactly what §1.4 says must never live in the skill. Removed it from `claude-skills`; the null-valued `channel-baseline.TEMPLATE.md` becomes `assets/channel-baseline.template.yaml`, and every reference to `channel-baseline.md` across `decision-policy.md`, `pipeline-runbook.md`, `learning-loop.md`, `youtube-delivery.md`, and `SKILL.md` (18 occurrences) now points at `<CHANNEL>/baseline.yaml` instead. **The video repo's own copy of the skill was not touched** — its `channel-baseline.md` still has this data; nothing was lost, it's just correctly excluded from what gets shipped as the reusable skill going forward.
- **Fixed the dangling-citation bug a peer session found** (see `peer-coordination-log.md`, message 3): `restored-v1-rules.md`'s 8 `Source:` lines cited the video repo's live v1 file by exact line number — a path that doesn't exist in this standalone repo at all, so drift there could never even be detected. Rewrote all 8 to cite `archive/v1-repo-2026-09-01/SKILL.md` (already in this repo from T1) by section heading instead — survives reflow, and the target actually exists here. Two "six rules" mentions that had gone stale (restored-v1-rules.md already said eight; two other spots hadn't caught up) corrected while in the file for the same reason.
- **catalog/tooling/*.py and hyperframes-* skill references**: added one clear paragraph in SKILL.md stating these are project-owned paths, not vendored, with a ledger-and-continue fallback if absent. Did not rewrite the ~27 individual mention sites (decision-policy.md, pipeline-runbook.md, youtube-delivery.md, restored-v1-rules.md, the generator script, the composition skeleton) — checked `scripts/extract_frames.sh`'s actual behavior first and confirmed it already just *documents* these paths for the invoking project to wire into its own `postrender` step rather than executing them itself, so the risk here is much lower than the v1-citation bug was. Flagging this boundary explicitly rather than silently claiming a full fix.

## Judgment calls made (not blank in the WO, but needed a decision)

1. Trimmed §4.1's description text to fit its own cap (above) rather than exceeding the literal Accept check.
2. Removed live channel-baseline data from the extracted repo without migrating it into `videos/_channel/baseline.yaml` in the video repo. That's a data-seeding/operational action, not a skill-shape one — S0 will populate it fresh (or someone can migrate it by hand) whenever `/produce` next runs for this channel. Flagging so it isn't assumed already done.
3. Fixed the v1-citation dangling-reference bug in full (all 8), since it was a real, already-diagnosed defect in what T1 shipped. Only partially addressed the catalog/tooling and hyperframes-skill references (one general clarifying paragraph, not a rewrite of every site) — judged the remaining risk as low after checking actual runtime behavior, per above.
4. Staged both commits explicitly by path rather than `git add -A`, per the peer-coordination note about broad-add commits sweeping in unrelated work-in-progress in a concurrently-edited repo (not a risk in *this* repo since I'm the only one touching it, but keeping the habit consistent).

## Not done (correctly out of scope for T3)

- Actually wiring the `providers.yaml`/T7 dependency the Mode table's `package` row names, or the `S0.0` stage T6 adds — both referenced by name in the router table as forward declarations, built by their own later tasks.
- `wrappers/*/SKILL.md` distribution (symlinking, claude.ai upload) — T8.
