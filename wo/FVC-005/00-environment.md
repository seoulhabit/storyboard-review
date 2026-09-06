T0-RENDER-OK

# 00-environment.md — WO-FVC-005 T0
Machine: this session's host. Skill under test: `makemeavideo` 0.2.0 (target
close: 0.3.0, WO §8.1). Drift check and render-machine verification below,
all commands re-run for this file.

## Version and drift check

- `hyperframes --version` → **0.8.30** (WO required ≥ 0.8.23 — pass, and
  three minor versions ahead).
- Resolved path: `hyperframes` is a **global** binary at
  `~/.nvm/versions/node/v24.18.0/bin/hyperframes`. It is **not** invoked via
  `npx` anywhere in this environment. Every `npx hyperframes` instance in the
  WO text is corrected in §8.2 of `docs/wo/WO-FVC-005.md` — worth restating
  here because `hyperframes init`'s own scaffold (confirmed live, see below)
  still writes `npx --yes hyperframes@0.8.30 …` into a fresh project's
  `package.json`. The tool's own default and this repo's convention disagree;
  this repo's convention wins.
- `makemeavideo` resolves at `~/.claude/skills/makemeavideo` →
  `/Users/sumitchoudhary/Desktop/claude-skills/makemeavideo` (readlink
  confirmed). `faceless-video-craft` resolves alongside it, unreleased 2.2.0,
  five uncommitted files (untouched by this session — diffstat verified
  byte-identical before/after this session's branch was created there).
- **`channel.yaml` does not exist anywhere in the repo.** `find "Story Board"
  -name channel.yaml` (repo-wide, all worktrees) returns zero hits. The file
  that exists is `videos/_channel/baseline.yaml`. The skill's 0.2.0 policy
  and runbook read `videos/_channel/channel.yaml` in 43 places (measured by a
  prior exploration pass this session). **This drift is confirmed, not
  assumed, and Gate 0 slot G0-10 asks Kim to rule which name wins** — this
  file does not decide it.
- No `videos/_queue.yaml` exists (`T6` deliverable — greenfield).

## Surface and paths

- Story Board repo: worktree `session/fvc-005` off `master` `c97201d`,
  isolated per `CLAUDE.md`'s worktree convention (`./worktree.sh guard` → 0
  from this tree).
- `claude-skills` repo: `/Users/sumitchoudhary/Desktop/claude-skills`, branch
  `fvc-005/makemeavideo` off `master` `9f66e2c`, created without disturbing
  another session's in-flight `faceless-video-craft` 2.2.0 diff (verified:
  `git diff --stat` identical before and after branch creation — same 5
  files, same `107 insertions(+), 6 deletions(-)`).

## Render machine (G0-5)

`hyperframes doctor`, re-run for this file:

| Check | Result |
|---|---|
| Version | 0.8.30 (latest) |
| Node.js | v24.18.0 (darwin x64) |
| CPU | 8 cores |
| Memory | 16.0 GB total · 5.6 GB available |
| Disk | 363.4 GB free |
| FFmpeg / FFprobe | 8.1.2 |
| Chrome | headless-shell `mac-152.0.7977.30`, cached |
| whisper-cpp | present, `/usr/local/bin/whisper-cli` |
| BGM (MusicGen) | deps installed |
| TTS (Kokoro) | **not installed** — `pip install kokoro-onnx soundfile` |
| Docker / Docker running | **not found** — not a T0 halt; local render uses bundled Puppeteer + system FFmpeg and needs neither. Docker only buys byte-exact determinism (pinned Chrome + fonts), most of which is already closed by the cached headless-shell pin plus font-freezing planned in T2. |

**End-to-end render, this machine, this session** (WO's literal T0 acceptance
— "Fail here = WO halts"):

```
$ hyperframes init t0-check --example blank   # WO names "faceless-explainer";
                                                # no such example exists in this
                                                # CLI's registry (confirmed via
                                                # `hyperframes docs examples` —
                                                # only blank / title-card /
                                                # video-edit are built in, and
                                                # title-card isn't registered
                                                # under that name either — see
                                                # note below). Used `blank`,
                                                # the CLI's own recommendation
                                                # "for offline use".
$ hyperframes check --json
  → ok: true, lint/runtime/layout/motion/contrast errorCount all 0
$ hyperframes render -q draft -o out.mp4
  → 300/300 frames captured, encoded, assembled — 100% Render complete
  → out.mp4: 18.5 KB · 10.0s video · rendered in 24.6s wall time
$ ffprobe out.mp4
  → codec_name=h264, width=1920, height=1080, duration=10.000000, size=18903
```

**Correction found:** the WO's T0 step 2 names *"the package's own
faceless-explainer route"* as the render target. No such bundled example
exists — `hyperframes docs examples` lists only `blank`, `title-card`,
`video-edit` as built-ins, and the live registry (`init --example`) does not
even have `title-card` under that exact name (it has `titlecard-calm` /
`titlecard-lockup`). `faceless-explainer` is a *skill* name in this
environment's skill list, not a hyperframes CLI example. Substituted `blank`,
which the CLI itself recommends for offline verification, and it exercises
the same init → check → render → ffprobe path the WO's acceptance actually
needs proven.

## Provider reachability

- **HeyGen**: `hyperframes auth status` → `hello@seoulhabit.com`, OAuth
  (expired, refreshable), plan **`creator`**, premium credits **0** (resets
  2026-10-06), add-on credits **81**. No connector for the HeyGen *MCP* tools
  (`create_speech` etc.) is authorized in this non-interactive session —
  `T1`'s F2–F4 need Kim present to complete OAuth live, per this session's
  D3 ruling.
- **vidIQ**: not probed this pass (no run yet needs it; `T1`'s findings are
  HeyGen/local-render only per this WO's scope).
- **Gemini**: not probed — not in this WO's tool fence (R-2).

## Budget in force

- HeyGen: 81 add-on credits total, resets 2026-10-06. This session's ruling
  (D2): **zero spend against `F1`'s cloud-parity leg.** `F1` resolves
  PARTIAL; rule `C-6` (hard cuts only) fires per its pre-written fail branch.
- vidIQ: not exercised this pass.

## Channel setup state

`videos/_channel/baseline.yaml` exists and is populated (channel id, corpus,
traffic curve, voice, music, publish windows — see the file itself). The
`heygen:` one-time-picks block the skill's `channel.template.yaml` defines
(voice_id, style_id, brand_glossary_id, tokens, timing_source, shorts_path,
usd_per_credit) is **not yet present** in `baseline.yaml` — it is a `T2`
setup-time pick (`TOUCHPOINT-SETUP`), not a `T0` deliverable.

## Mode and blockers named here

No `BLOCKER-*` raised by `T0` itself. Two items carried forward to `T1`/`T2`
as named, not silent:

- `BLOCKER-CONNECTOR:heygen` — not yet raised; `T1` raises it only if F2–F4
  cannot complete with Kim present.
- The `channel.yaml`/`baseline.yaml` name drift (Gate 0 G0-10) — carried, not
  resolved here.
