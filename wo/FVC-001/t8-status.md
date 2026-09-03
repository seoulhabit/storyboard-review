# T8 — Distribution (machine A) — symlinks done; live resolution unverified; one real regression caught and fixed along the way

This task turned out to be the highest-stakes one in the WO so far, not because of its own mechanics but because it made the repo live account-wide, which immediately surfaced a real defect. Full peer exchange in `wo/FVC-001/peer-coordination-log.md` (messages 5-6).

## Gate 0 for T8 itself

Before touching `~/.claude/skills/`, flagged to Kim that this machine currently has 4+ other live Claude Code sessions, two of them actively editing this exact repo's two project-level `faceless-video-craft*` copies, plus a plugin-cache-served third copy already resolving as `anthropic-skills:faceless-video-craft`. Creating the personal symlink now (rather than at T10, when the project copies get deleted) means a 4-way collision window that wouldn't otherwise exist. **Kim chose to proceed now**, with the condition that I message the other sessions first.

## What was done

1. Sent a heads-up to all four live `story-board-*` sessions before touching anything (message text and IDs in the peer log).
2. Created six symlinks:
   ```
   ~/.claude/skills/faceless-video-craft -> ~/Desktop/claude-skills/faceless-video-craft
   ~/.claude/skills/produce              -> ~/Desktop/claude-skills/wrappers/produce
   ~/.claude/skills/video-render         -> ~/Desktop/claude-skills/wrappers/video-render
   ~/.claude/skills/video-package        -> ~/Desktop/claude-skills/wrappers/video-package
   ~/.claude/skills/video-audit          -> ~/Desktop/claude-skills/wrappers/video-audit
   ~/.claude/skills/video-readout        -> ~/Desktop/claude-skills/wrappers/video-readout
   ```
   Confirmed no pre-existing entry of any of these names in `~/.claude/skills/` before creating them (only an unrelated, real, pre-existing `faceless-explainer` skill was there).
3. `git clone`-equivalent: already satisfied since T1 — the local checkout at `~/Desktop/claude-skills` has been tracking `origin` (`github.com/seoulhabit/claude-skills`) since it was created.

## Accept check — what's verified and what isn't

- **`claude plugin validate ~/.claude/skills`** — ran it: `✔ Validation passed with warnings` (the warning is the expected "symlinks aren't followed by validate, but are followed by a real session" caveat — present before my changes too, on a pre-existing symlink). **PASS.**
- **`readlink ~/.claude/skills/<name>`** — ran all six, all point where they should. **PASS.**
- **`/skills` shows exactly one faceless entry (source: personal)`** — **attempted, could not verify.** Tried querying a fresh `claude -p` session twice to see actual runtime resolution (exactly the question the Gate-0 collision risk was about). First attempt failed with a transient OAuth-refresh contention error (plausible given how many concurrent sessions are running); the second, after other work had passed some time, failed with "OAuth session expired and could not be refreshed" — a different, more serious failure. I did not retry further or attempt to fix the auth state myself: per the WO's own §1.5, authentication issues are a named legitimate stop, and repeatedly hammering a shared OAuth token from a nested process in a machine already running 4+ concurrent Claude sessions seemed likely to cause more contention, not resolve it. **This Accept item is genuinely unverified** — I'm not claiming the personal symlink wins over the project copies, only that I created it correctly and `claude plugin validate` is satisfied with it in isolation.
- **`/produce` appears in the `/` menu** — same limitation; not independently verifiable from a non-interactive shell without the same live-session query that just failed.

## The regression this surfaced

Within minutes of creating the symlink, `story-board-b0` flagged that the extracted repo's long-form transition default (`push-slide`) had been **disproved**, not just superseded, by video-repo commits `e97da4b`/`606cb45` (a wipe measures 0 failed safe-area frames vs. push-slide's 99, on the same real composition) — content this repo hadn't picked up since T1's extraction. Since the symlink had just made this account-wide, I verified the claim against the video repo's actual git history and ported the full correction (schema, generator, policy, and the restored-rule text) rather than treating it as a later-cleanup item. Commit `4fb5a41`, full detail in the peer log. `tests/run.sh` (15/15) and `release.sh` both still pass after the port.

A second peer (`story-board-13`) then flagged that T10's cutover (which deletes `.claude/skills/faceless-video-craft*` — both v1 **and** v2, on the literal glob) will also delete a citation-drift guard they'd just built for the video repo's own copies. Clarified the scope precisely (their message assumed v1 alone gets deleted; it's both) and initially recommended porting an equivalent guard into `claude-skills`. They then corrected that recommendation themselves, sharply: their guard only checks **internal consistency** (does the archive agree with `restored-v1-rules.md`) — it has no notion of whether the archive is *current*. Pointed at my stale snapshot, it would have returned a clean 8/8 on the exact defect that just shipped, since the archive and `restored-v1-rules.md` agreed with each other the whole time, both wrong the same way. **A real fix needs two checks**: the existing internal-consistency one, plus a new snapshot-freshness one (hash the archive, pin it to the upstream commit it came from, report "N commits behind" as a state instead of something a person has to notice by re-diffing by hand — which is what I did, twice, today). Not building either check now; flagging as a real gap for T9 or a deliberate follow-up, with the corrected (two-check) shape recorded so a future pass doesn't stop at the incomplete first version of this idea.

One more round: `story-board-b0` independently caught and fixed, upstream, the exact stale-error-message bug I'd flagged (confirmed it was a real bug in their own commit, not a port artifact) — their fix (commit `01e4874`) was more thorough than my quick edit, so I adopted their exact wording (commit `5b582d4`) rather than keep my shorter version.

## What's still Kim's (☐ per the WO)

- `GEMINI_API_KEY` in the shell profile.
- `/plugin install frontend-design@claude-plugins-official`, `design@claude-plugins-official`, `skill-creator@claude-plugins-official`.
- claude.ai: delete the old `faceless-video-craft` entry under Customize → Skills, upload `dist/faceless-video-craft-2.1.0.zip`.

## Recommendation

Given the live-resolution Accept check is unverified and this session can't safely re-attempt it right now, it would be worth Kim (or a fresh, unburdened session) running `/skills` directly in an interactive Claude Code window on this machine to see what actually shows for "faceless-video-craft" — that's a one-second check with the actual REPL that I can't safely reproduce from here.
