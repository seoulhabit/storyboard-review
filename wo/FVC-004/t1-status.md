# T1 — Setup, both machines — Accept: repo-side done on one machine; HeyGen MCP not connected on either
Commits `claude-skills` branch `fvc-004/makemeavideo`: `33277a6`, `f6591da`, `e153bb1`. Story Board branch `session/fvc-004` off master `7fc21c6`.

## What shipped

1. **`makemeavideo` moved from a claude.ai library-only skill to a repo-canonical copy.**
   Before this session the only copy was an enabled claude.ai library skill
   (`skill_01QpzHqVaWfgeEmhBFR4qtYs`), unpacked read-only into a
   session-scoped cache directory — the exact "two copies, nobody knows
   which one ran" failure §7 exists to prevent, made worse by
   `faceless-video-craft` also still being enabled in the library
   (`skill_019Mzn6o1WPy5UrghXRtfheb`). Copied verbatim (16 files) into
   `~/Desktop/claude-skills/makemeavideo/`, symlinked at
   `~/.claude/skills/makemeavideo` matching the five existing symlinks
   already there. Frontmatter verified as a subset of `release.sh`'s
   `ALLOWED_KEYS`.
2. **`faceless-video-craft` was not touched.** Its 5 files, uncommitted on
   another session's checkout (2.2.0 in progress, rule `C-3a`), are
   byte-for-byte the same diff (`107 insertions, 6 deletions`) before and
   after this session's three commits — verified by `git diff --stat`
   before and after.
3. **`docs/wo/WO-FVC-004.md` and `docs/wo/GATE0-FVC-004.md`** written into
   this repo, in `WO-FVC-001.md`'s house format, with a `§8 Corrections on
   receipt` section recording five places the WO's own text didn't match
   the machine (see `docs/wo/WO-FVC-004.md` §8 for the full account:
   WO-002/003 don't exist anywhere; the scaffold has no zip; the
   reconciliation §0.3 calls "open" closed on 2026-09-04; `faceless-video-craft`
   isn't actually frozen; `makemeavideo` isn't actually repo-canonical yet).

## Accept check — what's verified and what isn't

**Verified:**
- `makemeavideo` resolves from `~/.claude/skills/makemeavideo` →
  `~/Desktop/claude-skills/makemeavideo` (readlink confirmed).
- `references/providers.yaml` has the HeyGen roles, Higgsfield/current-vo/
  gemini-tts rows marked `closed by supersession, WO-FVC-004`, Gemini kept
  research-only — this predates this session (shipped in 0.1.0) but is
  confirmed present and correct.
- S0.0's probe in `runbook.md` names HeyGen `get_current_user`, vidIQ
  `vidiq_balance`, Gemini reachability — no HyperFrames row. Also predates
  this session; confirmed, and this session added the QA capability probe
  lines (T4).
- `git status` in `claude-skills` shows the same 5 modified
  `faceless-video-craft` files, same diff stat, as the session's first
  command run.

**Not verified, and I'm not claiming otherwise:**
- **`get_current_user` returning on either machine.** The HeyGen MCP is not
  connected on this machine: absent from `~/.claude.json`'s `mcpServers`
  (global and per-project), absent from the connector registry search, no
  `heygen`-prefixed tool available in this session. Cannot be completed
  non-interactively; needs an interactive session to run HeyGen's OAuth
  flow. This is T1's own step 1 and it did not happen.
- **The second machine.** This session ran on one machine. Two-machine
  parity (WO ruling 9, T1 step 1, T9) is entirely unverified.
- **Removing `makemeavideo` and `faceless-video-craft` from the claude.ai
  library.** Cannot be done from a coding session — it needs the account
  holder's library settings. Ledgered below as `TOUCHPOINT-LIBRARY-REMOVAL`.
- **Skill resolving at version 0.1.0 "as a baseline" per the WO's literal
  T1 step 5 text.** It resolves at **0.2.0** — T3/T4 work landed in the same
  session as the copy, so there was no meaningful moment to checkpoint at
  0.1.0 before advancing it. The version and every change between them is
  in `CHANGELOG.md` and the two commits above.

## `TOUCHPOINT-LIBRARY-REMOVAL`

Two skills need removing from the claude.ai library — `makemeavideo`
(`skill_01QpzHqVaWfgeEmhBFR4qtYs`) and `faceless-video-craft`
(`skill_019Mzn6o1WPy5UrghXRtfheb`) — so the repo copy is the only copy that
can resolve. Kim: Settings → Skills (or the equivalent claude.ai library
management surface) → disable/remove both. Until this happens, a session
with library access enabled will see two `makemeavideo` copies at
different versions and different paths, which is precisely the drift this
WO exists to end.

## Judgment calls made

- **Worked in an isolated worktree** (`session/fvc-004`, off master
  `7fc21c6`), per this repo's own `CLAUDE.md` convention — three prior
  incidents in this repo came from working in the shared checkout.
- **Did not attempt to reconcile or edit `faceless-video-craft`'s in-flight
  2.2.0 diff.** It belongs to another session. `C-3a`'s content was ported
  into `makemeavideo` (T3) with attribution rather than left to be lost to
  the freeze conflict, but the source file itself is untouched.

## Not done (blocked, not skipped)

T0, the rest of T1 (HeyGen connection, second machine), T2, T5–T9 — all
named in `docs/wo/WO-FVC-004.md` §6 Gate status as blocked on the HeyGen
MCP connection and Kim's three required Gate 0 answers (G0-1, G0-3, G0-6).
