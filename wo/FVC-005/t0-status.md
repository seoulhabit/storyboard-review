# T0 — Environment and drift — DONE (render machine verified end-to-end; connector state unresolved, correctly so — see T1)
Commits: Story Board branch `session/fvc-005` off `master` `c97201d` (isolated worktree). `claude-skills` branch `fvc-005/makemeavideo` off `master` `9f66e2c`.

## What shipped

1. **Version and drift check**, per `S0.0`: `hyperframes` resolves globally
   at v0.8.30 (≥ 0.8.23 required — pass), `makemeavideo` resolves at
   0.2.0 from `~/Desktop/claude-skills/makemeavideo` via the expected
   symlink, `faceless-video-craft` at an unreleased 2.2.0 was confirmed
   untouched by this session (diffstat identical before/after this
   session's own branch was created in that repo).
2. **Confirmed, not assumed, that `videos/_channel/channel.yaml` does not
   exist.** A repo-wide `find` returns zero hits; the file present is
   `baseline.yaml`. This was reported as a correction in the WO
   (`docs/wo/WO-FVC-005.md` §8.8) and as a new Gate 0 slot (G0-10) rather
   than silently renamed — the skill's 43 read-sites and the resolution are
   Kim's call.
3. **Rendered a real composition, locally, end to end**, on this machine,
   this session: `hyperframes init t0-check --example blank` → `check
   --json` (0 errors across lint/runtime/layout/motion/contrast) → `render
   -q draft -o out.mp4` (300/300 frames, 100% complete, 24.6s wall time) →
   `ffprobe` confirmed h264, 1920×1080, exactly 10.000000s duration. This is
   the WO's literal T0 acceptance line ("Fail here = WO halts") and it
   passed.
4. **Found and corrected a WO inaccuracy in the render target itself**: the
   WO's T0 step 2 names "the package's own faceless-explainer route", which
   does not exist as a bundled hyperframes example (`hyperframes docs
   examples` lists only `blank`/`title-card`/`video-edit`, and the live
   registry doesn't even have `title-card` under that name). Substituted
   `blank`, the CLI's own recommendation for offline verification — same
   init → check → render → ffprobe path, same acceptance bar.
5. Ran `hyperframes doctor` and recorded every row in `00-environment.md`,
   including the two real gaps: Kokoro TTS not installed, Docker absent
   (neither is a T0 halt — see that file for why).

## Accept check — what's verified and what isn't

**Verified:**
- `hyperframes --version` → 0.8.30, live, this command, this session.
- `hyperframes auth status` → real account, real plan, real credit counts
  (`hello@seoulhabit.com`, creator, 0 premium / 81 add-on, resets
  2026-10-06) — not a guess, not carried from a prior WO.
- A composition was actually rendered on this machine to a real MP4 file,
  and that file's codec/dimensions/duration were independently confirmed
  via `ffprobe`, not inferred from the render tool's own success message.
- `git diff --stat` in `claude-skills` before and after this session's
  branch creation is byte-identical — the other session's in-flight work
  was not touched.
- `./worktree.sh guard` exits 0 from this session's Story Board worktree.

**Not verified, and I'm not claiming otherwise:**
- **The HeyGen MCP connector.** OAuth was not run — this is a
  non-interactive pass and D3 requires Kim present for it. `create_speech`,
  `list_voices`, `create_speech`-driven cost data: none of it exists yet.
  This is `T1`'s job, not `T0`'s, and it is named as pending rather than
  assumed to be fine.
- **vidIQ and Gemini reachability.** Not probed — out of this WO's tool
  fence (R-2) for the tasks run so far.
- **Docker-mode determinism.** Not exercised — local (non-Docker) render is
  what the WO's default path (R-1) actually uses, so this is correctly out
  of scope, not a gap in coverage.
- **The second machine.** This session ran on one machine only. Two-machine
  parity is unaddressed, same as it was in WO-FVC-004's T1.

## Judgment calls made

- **Worked in an isolated worktree** for Story Board (`session/fvc-005`)
  and a dedicated branch for claude-skills (`fvc-005/makemeavideo`), per
  `CLAUDE.md`'s convention and the plan's step 0 — verified the branch
  creation didn't disturb another session's uncommitted diff before
  proceeding to anything else.
- **Substituted `blank` for the WO's named (nonexistent) render target**
  rather than halting T0 on a WO typo — the acceptance bar (init → check →
  render → verify) is what matters, and `blank` exercises exactly that.
- **Did not attempt HeyGen OAuth non-interactively.** The system prompt is
  explicit that this session cannot run an OAuth flow; per D3, that step
  waits for Kim.

## Not done (correctly out of scope for T0)

The HeyGen MCP connector, `T1`'s four findings, `T2`'s design-system
extraction, `T3`'s compiler — all named in the plan as the next steps in
this pass, not blocked by anything T0 found.
