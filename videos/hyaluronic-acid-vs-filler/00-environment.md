# Environment — hyaluronic-acid-vs-filler

Written by S0.0, first thing, before any other stage.

**Skill version:** 2.1.0
**Surface:** code (Claude Code CLI; Skill/Bash/MCP tools present, no sandbox output mount)
**Host:** Darwin 24.6.0 arm64 · node v24.18.0 · python 3.9.4 · ffmpeg/ffprobe 8.1.2

**Paths** (see SKILL.md §Paths):
- OUT: `/Users/sumitchoudhary/Desktop/Story Board/videos/hyaluronic-acid-vs-filler/`
  — `/mnt/user-data/outputs/` was tested fresh this run and is **absent**, so the
  repo path applies.
- CHANNEL: `/Users/sumitchoudhary/Desktop/Story Board/videos/_channel/`
  — **did not exist before this run.** Created by S0.

**Companions resolved** (filled in as each gate fires):
- frontend-design: not yet resolved (fires S3, S6)
- design-critique: not yet resolved (fires S7)

**Providers reachable:**
- vidIQ: `ok` — `vidiq_balance` returned 2428 credits (1628 renewable of 2000,
  resets 2026-10-01; 800 add-on). Authorized as `hello@seoulhabit.com`,
  exactly one channel (`UCzqEGQ9uAU43AgyxGtLT7MA`) → `[S0/B-2]` resolves, no
  BLOCKER-CHANNEL.
- HyperFrames: `ok` — `npx --yes hyperframes@0.8.22 --version` → `0.8.22`.
  Pin taken from `videos/ectoin-survival-molecule/package.json` and from the only
  machine-written version record in the repo
  (`outputs/2026-09-01-.../06-render/check.json:77`). **Not** the 0.8.17 that
  `videos/hyaluronic-acid-serum/` pins.
- Higgsfield: `ok` — 2437.25 credits, plan `free`. `list_voices` confirms the
  channel voice **Kimberly** `674b71b8-1d2e-4087-8567-d1f53c0b9f3c`
  (`voice_type: element`) still exists, as `providers.yaml` §tts `current-vo`
  requires.
- Gemini: `no-key` — `GEMINI_API_KEY` unset. Consequences, both by each rule's
  own stated default, neither a halt:
  - `[PR-1]` grounded research never fires. Claim sourcing ran on PubMed +
    regulator fetches instead, which is the project's own source list and is
    what PR-1 is a *last* resort behind anyway.
  - `[PR-2]` selects `current-vo` (Higgsfield `generate_audio`) rather than
    `gemini-tts`. No `listening-test pending` flag applies, since that flag is
    scoped to gemini-tts runs.

**Project skill in play:** none. Confirmed by search — the repo has no
channel-specific skill, and `faceless-video-craft/SKILL.md` says so itself
("This repo currently has no project skill holding those truth/claim rules").
Therefore `decision-policy.md` §Claims (`K-*`) applies as the **floor**, undiluted.
Brand tokens come from `videos/ectoin-survival-molecule/assets/tokens/tokens.css`,
the canonical landscape token set, not from a project skill.

**Budget in force:** `providers.yaml` §budget — **$5.00 per run**, `warn_at` 0.8,
**200 vidIQ credits**. Tracked in `cost-log.jsonl` beside this file.
**Mode:** `full` (story supplied, no narrower intent stated).
