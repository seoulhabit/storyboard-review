# Gate 0 — decisions and open items

Tracks resolutions to points raised in `00-inventory.md`, kept separate from `docs/wo/WO-FVC-001.md` so the WO document stays a faithful copy of what was drafted.

## Decided

- **Skills repo location.** Kim, 2026-09-02: *"claude-skills, personal GitHub, default layout is fine."*
  → new private GitHub repo `claude-skills` on Kim's personal GitHub account, default layout from §3: `faceless-video-craft/`, `wrappers/`, `archive/`, `dist/` (gitignored), `scripts/release.sh`. Resolves Gate 0 slot 1. T1 creates this repo once Gate 0 clears in full.

- **T2 rescoped.** Kim, 2026-09-02: *"T2 should verify and document what's already merged, not redo it."*
  Applies to T2's *Do* list in the WO as follows:
  - `merge-matrix.md` — still produced, but as a verification pass over the merge already done in commits `d7e07e3` and `6e6c202`, not a new merge. Every rule ID found live (K-1..K-5, A-1..A-9, B-1..B-3, C-1..C-3, E-1..E-2, L-1..L-2, P-1..P-4, R-1/R-1b/R-2/R-3, S-1..S-8, T-1..T-4, V-1..V-3, plus restored R1–R8 in `restored-v1-rules.md`) gets a verdict against what's actually in `decision-policy.md` right now, not a fresh keep/merge/drop decision.
  - The two extra restored rules found beyond the WO's list — **R7** (cuts/crossfades/transitions, `[S6/A-8]`) and **R8** (motion idiom by narrative function, `[S6/A-10]`) — get rows in the matrix too, verified rather than authored.
  - Policy-defect items (S-1, S-2, T-3) — confirm the existing `channel-baseline`-reading, `[default]`-tagged rules already satisfy the WO's intent; document any gap found rather than rewriting rules that already pass.
  - Engine-contract and lint-parity Accept checks (`hyperframes check ...`) are still blocked on the HyperFrames CLI not being installed on this machine (see `00-inventory.md` §0.5) — that blocker is independent of the rescoping and still needs Kim's or an operator's action before T2's Accept can run.
  - Tier stays Opus/High per §1.10 — verification-and-documentation of a large rule set across multiple files still warrants it.

- **Current VO provider.** Kim, 2026-09-02: *"pull the VO id from ectoin-survival-molecule's ledger."*
  That project has no `00-decision-ledger.md` (it predates/sits outside the v2 pipeline's artifact convention) — the equivalent record is `videos/ectoin-survival-molecule/BRIEF.md:66-72`, under `## Voice`:
  > Standing series voice — `voice_id 674b71b8-1d2e-4087-8567-d1f53c0b9f3c`, `voice_type element` — via Higgsfield `generate_audio`. HeyGen/`hyperframes tts` sign-in is unavailable from an automation context; local Kokoro is not installed and Parakeet cannot run on this Intel host.

  → `current-vo` in `providers.yaml` resolves to: **provider `higgsfield`, tool `generate_audio`, `voice_id 674b71b8-1d2e-4087-8567-d1f53c0b9f3c`, `voice_type element`**, unit `credits` (same unit as the image/video Higgsfield rows). Note this is a constraint-driven default, not a chosen-best one — HeyGen TTS sign-in and both local options were ruled out for environment reasons, not quality. Resolves Gate 0 slot 3.

  **This sharpens the still-open Higgsfield $/credit slot**: that single number now prices *two* `providers.yaml` roles (image/video generation *and* the VO fallback), not just one — worth flagging to Kim since it makes that number more load-bearing than the WO's `providers.yaml` skeleton implies.

## Gate 0 — CLEARED

- **Higgsfield USD per credit.** Kim, 2026-09-02: **$0.02/credit.** Prices both the `A-1` image/video role and the `V-1` `current-vo` fallback in `providers.yaml`.
- Kim wrote **`go`**, 2026-09-02.

All three slots resolved:
1. Skills repo: `claude-skills`, Kim's personal GitHub, default layout.
2. Higgsfield: `$0.02/credit`.
3. `current-vo`: Higgsfield `generate_audio`, `voice_id 674b71b8-1d2e-4087-8567-d1f53c0b9f3c`, `voice_type element`.

T1 starts now.
