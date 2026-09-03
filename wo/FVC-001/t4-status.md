# T4 — Companion skills as gates — DONE (static wiring); Accept check partially verifiable

Commit `b1d351b` pushed to `github.com/seoulhabit/claude-skills`.

## What changed

- New `SKILL.md` §Companion-skill gates: defines the resolver once — (1) Skill tool (`frontend-design@claude-plugins-official` / `design@claude-plugins-official`), (2) file path if the Skill tool can't resolve it, (3) `COMPANION-MISSING:<name>` to the ledger and continue, never a halt — replacing the old "locate frontend-design rather than assuming a path" paragraph, which described step 2 only and didn't say the skill was mandatory or name where.
- Wired into `pipeline-runbook.md` at the three points the WO names:
  - **S3**, step 0, before thumbnail-concept work — `frontend-design`.
  - **S6**, step 0, before any markup — `frontend-design`.
  - **S7**, step 4b, on the frames the post-render pixel gate (step 4) just extracted — `design-critique`, **no longer optional** (the Companion skills table used to say "Optional review pass on extracted frames, not code" — that line now says mandatory and points at the gate section).
- Ledger token family: `COMPANION-RESOLVED:<name> (skill-tool|file)` / `COMPANION-MISSING:<name>` — matched to the skill's existing flat `BLOCKER-CLAIM`/`BLOCKER-CHECK`-style tokens rather than inventing a new bracketed `[Sx/COMPANION]` syntax (an inconsistency I introduced mid-edit and caught before committing — see below). `assets/decision-ledger.template.md` now shows one example of each of the three states (resolved by skill-tool, resolved by file, missing) at the three gate points.

## Accept check — what's verified and what isn't

WO's Accept: *"a dry run of S6 entry in Code shows the Skill tool call in the transcript; `grep -n "COMPANION" 00-decision-ledger.md` on a run with the plugin disabled shows the MISSING line."*

**Verified:**
- Static wiring is consistent end to end — `grep -rn COMPANION` across the repo shows the same token family used identically in SKILL.md's definition, the runbook's three gate points, and the ledger template's three example lines.
- `frontend-design` and `design:design-critique` both resolve via the Skill tool in this actual session (confirmed against this session's own live skill list) — so the happy path's step 1 is mechanically viable in this environment, not just written down.
- `scripts/release.sh` still validates clean after the edit (frontmatter unaffected).

**Not verified, and I'm not claiming otherwise:** the literal Accept check needs an actual production run — `/produce` or `/video-render` entering S6 for real, with a real `00-decision-ledger.md` being written — which needs a real story input plus the full stack (vidIQ auth, HyperFrames CLI). The CLI still isn't installed on this machine (per `00-inventory.md` §0.5, unchanged since Gate 0). I did not fabricate a ledger file or a transcript to make this check look passed; it's an honest gap, same category as T2's engine-contract blocker, and it closes naturally once T9's eval runs actually execute the pipeline.

## Judgment call

Caught and fixed my own inconsistency before committing: I first wrote the ledger format two different ways in the same edit pass (a bracketed `[Sx/COMPANION] <name> → ...` form in one spot, the flat `COMPANION-MISSING:<name>` form the WO itself specifies in another). Checked how this skill already names comparable events (`BLOCKER-CLAIM`, `BLOCKER-CHECK`, `BLOCKER-CHANNEL` — all flat tokens, never bracketed) and standardized on that instead of leaving two competing conventions in a file T9's evals will read.

## Not done (correctly out of scope for T4)

- Run-report row for companion invocations (§4.5's "Skills and tools invoked" section) — the run-report template itself doesn't exist yet; that's T6. The requirement is already implied by what's wired here, so T6 has what it needs.
