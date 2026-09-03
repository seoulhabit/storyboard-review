# T1 — Repo and version stamp — DONE

Skills repo: **https://github.com/seoulhabit/claude-skills** (private), local checkout at `~/Desktop/claude-skills`.

## Attestation (Accept checks, read-back)

**`git log --oneline | head -3`**
```
f0fe0a9 add CHANGELOG, version 2.1.0 stamp, and scripts/release.sh
973a7c3 archive v1 repo copy for merge
db6105d import v2 baseline
```

**`scripts/release.sh && ls -la dist/`**
```
== release.sh: validating frontmatter keys ==
OK: frontmatter keys (name description metadata) are a subset of {name description license compatibility metadata allowed-tools}
Version: 2.1.0
== release.sh: claude plugin validate ==
claude --version: 2.1.252 (release.sh requires >= 2.1.233)
✔ Validation passed
== release.sh: zipping dist ==
Wrote /Users/sumitchoudhary/Desktop/claude-skills/dist/faceless-video-craft-2.1.0.zip

dist/faceless-video-craft-2.1.0.zip   105909 bytes
```

**Validator exit code:** `0` (clean pass, no warnings, on an isolated scratch copy)

## Decisions made during T1 (not blank in the WO, but needed a call)

1. **`claude plugin validate faceless-video-craft` doesn't work as literally written.** Tested directly: pointing `claude plugin validate` at a bare skill directory (SKILL.md at its root — tried this repo's `faceless-video-craft/`, the repo root, and `~/.claude/skills/hyperframes-cli` as a known-good control) always demands a `.claude-plugin/plugin.json` manifest. The manifest-free "skills-dir" validation path only activates when the target is a directory *containing* skill directories (confirmed against the real `~/.claude/skills` and against synthetic dirs named `.claude/skills` or plain `skills`). This repo deliberately has no plugin manifest — T8 distributes this as a **skill** (symlink into `~/.claude/skills/`, or a skill zip uploaded to claude.ai), never as an installed plugin. `release.sh` now copies `faceless-video-craft/` into a throwaway `<tmp>/skills/` directory and validates that, which exercises the same manifest-free skill-validation path with an exit code `release.sh` can check — same intent as the WO's literal command, adapted to how the CLI actually behaves at `2.1.252`.
2. **Archive source for `archive/v1-repo-2026-09-01/`.** Per `wo/FVC-001/00-inventory.md`, the WO's "~2,172 lines" description of repo v1 matches an earlier state (before commit `d7e07e3`), not the current 3,247-line file at `.claude/skills/faceless-video-craft/SKILL.md`. T1's instruction points at the live path, so the *current* content is what's archived; a `NOTE.md` alongside it in the skills repo explains the discrepancy and tells T2 where to get the actual pre-rebuild snapshot (`git show d7e07e3^:...` in this repo) if it needs to check `restored-v1-rules.md`'s line-number citations against source.
3. **`wrappers/` is an empty directory** in the pushed repo (git doesn't track empty dirs — it exists locally, won't appear in `git ls-tree` until T3 adds wrapper skills into it). Not a defect, just noting it so a `ls` on the pushed repo isn't mistaken for a missed layout item.

## Known gap surfaced after the fact (real, deferred to T3 — not a T1 defect)

A peer session grepped the pushed repo and found 35 dangling references to paths outside `faceless-video-craft/`: 9 to `.claude/skills/faceless-video-craft/SKILL.md` (v1, cited by exact line number in `restored-v1-rules.md`'s R7/R8), 18 to `catalog/tooling/*.py`, 9 to `skills/hyperframes-*` companion-skill paths. Verified independently — confirmed, and confirmed T1 did not vendor any of the referenced tooling scripts (nothing to go stale, just dangling path strings). v2 was designed to run inside the video repo, where these are all real sibling paths; extracting it into its own repo is what surfaces the assumption. Worst instance: the R7/R8 `Source:` line-number citations point at a file that doesn't exist in this repo at all, so drift there can no longer even be detected from inside `claude-skills`. This is T3's "surface-aware paths" mandate, not a T1 fix — full detail and a peer-suggested remedy (commit-pin the v1 reference, or drop line numbers for a heading pointer) in `wo/FVC-001/peer-coordination-log.md`.

## Not done (correctly out of scope for T1)

- `wrappers/<name>/SKILL.md` contents — T3.
- Anything inside `faceless-video-craft/references/` or `decision-policy.md` — T2 (rescoped to verify/document per `gate-0-notes.md`), not T1.

No files under `.claude/skills/` in the video repo were modified or deleted — only read from, to build the copy in the new `claude-skills` repo.
