# Environment — snail-mucin-medical-secret-v2

Written by S0.0, first thing.

**Skill version:** 2.1.0
**Surface:** code (Claude Code, desktop app)
**Host:** Darwin 24.6.0 / macOS 15.7.9, x86_64 · node v24.18.0 · Python 3.9.4

**Paths:**
- OUT: `<repo>/videos/snail-mucin-medical-secret-v2/` — `/mnt/user-data/outputs/` tested fresh, absent.
- CHANNEL: `<repo>/videos/_channel/`
- `<repo>` = `/Users/sumitchoudhary/Desktop/Story Board/.claude/worktrees/render-review-optimizations-781b9e`,
  a git worktree on `claude/render-review-optimizations-781b9e`.

**Companions resolved:**
- frontend-design: not re-invoked this pass — the v1 render-mode pass already resolved it and its
  guidance (restrained hierarchy, one accent, no seafoam-on-claims) is carried into this rebuild's
  tokens directly.
- design-critique: not re-invoked — see §Skipped in the run report; the pixel-by-pixel verification
  this build required (18+ frame extractions across 6 render attempts) already exceeded what a
  single design pass would add, and the mandatory pixel gate (`[S7/R-2]`) was exhaustively applied.

**Providers reachable:**
- vidIQ: not called — this is a story-level rebuild of an existing topic, not a new topic gate.
- HyperFrames: ok — pin `0.8.27` (this project only; v1 stays at `0.8.17`). Verified via
  `hyperframes upgrade --project . --check` on the v1 project: "would bump 0.8.17 → 0.8.27."
- Higgsfield: not reachable/not used — Gemini (`nano_banana_pro`) used instead, logged as a
  substitution per `[S6/A-1]`.
- Biomedical literature (PubMed MCP): ok — used to actually read all 4 sources in `CLAIM-LEDGER.md`,
  not just cite them.

**Project skill in play:** none (same finding as v1 — this repo carries no project-specific truth
rules; `decision-policy.md` §Claims applies as the floor, undelegated).

**Budget in force:** ~4 credits spent on VO (13 generations incl. rate-limit retries and one
trim/retrim pass) + 2 credits on the one new image (2 candidates) ≈ $0.12 total, well inside the
$5.00/run cap. No vidIQ credits spent.

**Mode:** full story-level rebuild (claim ledger → script → storyboard → assets → composition →
render → verify), triggered by user-supplied engagement review, not the standard `/produce` pipeline
entry point — S0/S2 topic-gate and S8/S9 publish/readout stages are out of scope for this pass; see
the run report for what ran and why.
