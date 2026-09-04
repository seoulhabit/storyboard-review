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

---

## v3 revision — 2026-09-04

**Worktree:** `.claude/worktrees/hyaluronic-acid-video-rerender-8abe8c`,
branch `claude/hyaluronic-acid-video-rerender-8abe8c`, HEAD `cc41fac` (merge
of PR #11) at run start, clean tree.

**Host:** Darwin 24.6.0 x86_64 (this machine differs from the prior run's
arm64 host — same repo, different worktree checkout) · node v24.18.0 ·
python 3.9.4 · ffmpeg/ffprobe 8.1.2.

**Provenance check (pre-render, per the request's own explicit ask):**
`index.html` verified byte-identical (`sha1 77cc2be2…`) across 7 of 8
checked worktrees; the one divergent copy (`~/Desktop/storyboard-master`)
was OLDER, not newer. mtime alone would have been misleading (ranged
06:47-19:20 across identical-content copies) — see `00-decision-ledger.md`'s
new provenance section for the full reasoning. Nothing under
`05-composition/` is hand-written regardless; it was regenerated from
scratch (not trusted from any checkout) via `beats_to_composition.py --force`
after `rm -rf compositions/frames index.html index.motion.json`.

**Providers reachable (re-checked this run):**
- Higgsfield: `ok` — 2271.15 credits at run start (free plan). Kimberly
  voice id confirmed still live. `soul_cast` (the purpose-built consistent-
  character model) returned `Requires basic plan or higher` — not available
  on this account; fell back to `soul_v2` (`text2image_soul_v2`) per
  `providers.yaml`'s own fallback ordering.
- vidIQ: not re-probed this run (S0-S3 not re-run; baseline still fresh from
  the prior run's S0.0 check).
- HyperFrames: global install is now `0.8.27` (was `0.8.22` last run); this
  project's pin STAYS at `0.8.22` for every command touching the
  composition (`check`/`snapshot`/`render`) — `build_actors.py`'s
  regex-based ground/contrast fixer is calibrated to this exact generator's
  output shape, and a contact sheet drawn by a different renderer than the
  one that renders the film is not evidence about the film. Only
  `transcribe` (pure local ASR, never opens the composition) runs on the
  bare global `0.8.27` binary.
- Gemini: `no-key`, unchanged — `PR-2` falls to `current-vo` again.

**Companions resolved:**
- `design-critique`: `COMPANION-RESOLVED:design-critique (skill-tool)` — S7,
  applied to the 19-frame contact sheet plus targeted full-resolution
  extractions from the mastered render.
- `frontend-design`: not separately invoked this revision — the S6 gate was
  already satisfied by v2's original resolution and no new component
  system was introduced (the new plate/hook/binds-and-seal builders reuse
  the existing token set and type scale unchanged).

**Skill version:** 2.1.0, unchanged.
