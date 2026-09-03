# WO-FVC-001 §0 — Live inventory

Run at: 2026-09-02, session in `/Users/sumitchoudhary/Desktop/Story Board`.
All values below are live command output, gathered in this run — none carried from the WO doc or from memory.

## 0.1 — Repo / git state

```
$ git rev-parse --show-toplevel
/Users/sumitchoudhary/Desktop/Story Board

$ git branch --show-current
master

$ git status --short
?? outputs/2026-09-01-how-to-repair-skin-barrier/05-composition/snapshots/
?? outputs/2026-09-01-how-to-repair-skin-barrier/06-render/raw.mp4
?? videos/snail-mucin-recut-34s/.backup-pre-rerender-20260831/
?? videos/snail-mucin-recut-34s/renders/snail-mucin-recut-34s_rerender.mp4
```
(All four untracked paths are unrelated render/backup outputs from other in-flight work — not touched by this run.)

## 0.2 — Every copy of the skill on this machine

| Path | Exists | SKILL.md lines | sha256sum | mtime | references |
|---|---|---|---|---|---|
| `.claude/skills/faceless-video-craft/SKILL.md` (repo) | yes | 3247 | `231b63d1548cdc1c9bd95bdc6186c14209fc9e2678980e50a27a60fd98590684` | 2026-09-02 17:33:35 | none (monolithic file, no `references/` dir) |
| `.claude/skills/faceless-video-craft-v2/SKILL.md` (repo) | yes | 247 | `602e3e431737128beeb731a1401f118815d2cf678e491536b6725da0bf292361` | 2026-09-02 17:05:56 | `channel-baseline.TEMPLATE.md`, `channel-baseline.md`, `decision-policy.md`, `hyperframes-engine.md`, `learning-loop.md`, `pipeline-runbook.md`, `restored-v1-rules.md`, `youtube-delivery.md` (8, not the 6 the WO assumed) |
| `~/.claude/skills/faceless-video-craft*` | **no** | — | — | — | — |
| `~/.claude/skills/synced/` | directory absent / empty, no faceless match | — | — | — | — |
| `~/.claude/plugins/cache/*faceless*` | none found | — | — | — | — |
| `.claude/commands/*produce*` or `*video*` (repo) | none found | — | — | — | — |
| `~/.claude/commands/*produce*` or `*video*` | none found | — | — | — | — |

**Finding:** only two copies exist anywhere on this machine, both project-level, both in this repo. There is no personal (`~/.claude/skills`), synced, or plugin-cache copy to reconcile — the "every copy on this machine" search the WO worried about turned up nothing extra.

## 0.3 — What `/faceless-video-craft` resolves to right now

The live skill listing already injected into this session (not re-derived) shows both project skills registered independently and simultaneously:
- `faceless-video-craft` — description matches `.claude/skills/faceless-video-craft/SKILL.md` verbatim (confirmed by diff against file content read in this run).
- `faceless-video-craft-v2` — description matches `.claude/skills/faceless-video-craft-v2/SKILL.md` verbatim.
- `anthropic-skills:faceless-video-craft` — a third, plugin-scoped entry, also present in the same listing, with wording close to `faceless-video-craft-v2`'s description but not byte-identical (not diffed against a file since it isn't on disk in this repo — plugin-sourced).

I did not additionally spawn `claude -p "What skills are available?"` as a nested subprocess — that would open a second billed session just to re-ask a question this session's own harness already answered in-context. If Kim wants the literal subprocess transcript for audit purposes, say so and I'll run it.

**Finding, not in the WO's model:** invocation is not "one skill resolves" — it's three simultaneously-registered candidates (two project, one plugin) with overlapping trigger language (both project skills mention HyperFrames, Ken Burns, `window.__timelines`, 9:16 short). This is worse than "v2 is shadowed by v1" — it's a three-way collision, and the plugin-scoped `anthropic-skills:faceless-video-craft` is a copy this WO's §0.2 machine-scan didn't have a category for (it's neither `~/.claude/skills` nor `~/.claude/plugins/cache` on this machine — it's served from the plugin marketplace, not a local file this repo's mtime/hash comparison can even reach).

## 0.4 — Rule IDs: repo copy vs v2 vs K-rules

```
$ grep rule-ID-like tokens in .claude/skills/faceless-video-craft/ (v1, 3247 lines)
(none — only an incidental "UTF-8" match)

$ grep rule-ID-like tokens in .claude/skills/faceless-video-craft-v2/ (all references)
A-1 A-2 A-3 A-4 A-5 A-6 A-7 A-8 A-9 B-1 B-2 B-3 C-1 C-2 C-3 E-1 E-2
K-1 K-2 K-2a K-2b K-3 K-4 K-5 L-1 L-2 P-1 P-2 P-3 P-4 R-1 R-1b R-2 R-3
S-1 S-2 S-3 S-4 S-5 S-6 S-7 S-8 T-1 T-2 T-3 T-4 V-1 V-2 V-3
```

**This inverts the WO's premise.** The WO assumes the repo v1 copy holds K-1..K-5 and six rules v2 dropped, and that T2's job is to merge them into v2. Live state:

- **v1 (`.claude/skills/faceless-video-craft/SKILL.md`) has zero policy/rule IDs.** It is now an explicitly domain-neutral craft/engine skill — its own text says: *"Truth rules, claim/source enforcement, brand palettes, and component rosters belong to a **project skill**, not here... This repo currently has no project skill holding those truth/claim rules."* That statement is itself stale — `faceless-video-craft-v2` *is* that project skill and already holds every rule.
- **v2 already has the full rule set**, including K-1..K-5 and — per `references/restored-v1-rules.md` (518 lines) — **eight** restored-from-v1 rules (R1–R8), not the six the WO lists. R7 (cuts/crossfades/transitions) and R8 (motion idiom by narrative function) were added 2026-09-02 "from the Ectoin review," i.e. after the WO's own Sep-1/Sep-2 chat origins. `decision-policy.md` cross-references them by tag (e.g. A-5 is annotated "restored, verbatim as R3").
- **S-1, S-2, T-3** — the three policy defects T2 is supposed to fix — already read `channel-baseline.md` fields (`formats.short.uploads_90d`, `retention.avg_view_pct_long`, `curve.p50_7d`, a `10 × subs` ceiling) and already carry `[default]` tags (8 uses of `[default]` found in `decision-policy.md`).
- `assets/composition-skeleton.html` and `assets/beat-sheet.schema.json` already exist in the v2 tree.

**Root cause, found via `git log`:** commit `d7e07e3` ("Rebuild faceless-video-craft as v2.1; add K-* claim rules and the Centella re-cut", 2026-09-01 21:49:09) already did the engine-contract fix and the K-rule addition this WO's T2 describes as still-to-do — its message: *"replaces everything touching the engine with the shipped contract... transcribed from the pinned CLI's own docs with the source file named per line."* Confirmed: `git show d7e07e3^:.claude/skills/faceless-video-craft/SKILL.md | wc -l` → **2172** — exactly the line count the WO cites for "repo v1," proving the WO was drafted against the pre-`d7e07e3` state. The most recent commit on this repo, `6e6c202` ("Add long-form continuity rules to faceless-video-craft, from the Ectoin review", **2026-09-02 17:48:29**), touched both skill copies again, minutes before this inventory was taken.

**This is a named blocker for Gate 0, not a creative-preference question:** the WO's T2 (Opus/High merge task, and its `merge-matrix.md`/Accept criteria) is written against a repo state that two commits have already substantially superseded. Per the memory note that this repo is often worked by 2+ sessions concurrently, and given a commit landed 17 minutes before this inventory, there is a live risk that another session is mid-edit on these exact files right now. Recommend Kim confirm before T2 proceeds: (a) whether T2 should now be "verify and document what's already merged" rather than "do the merge," and (b) whether it's safe to branch/extract into a new repo without colliding with concurrent work on `.claude/skills/faceless-video-craft*`.

## 0.5 — Tooling

```
claude --version:        2.1.252 (Claude Code)          [meets T1's ≥ 2.1.233 requirement]
hyperframes --version:   command not found — NOT INSTALLED on this machine
npm list -g hyperframes: (empty — not installed globally via npm either)
ffmpeg:                  ffmpeg version 8.1.2
ffprobe:                 ffprobe version 8.1.2
python3:                 Python 3.9.4
GEMINI_API_KEY:          unset  →  environment probe would read "no-key"
vidIQ MCP:                REACHABLE — vidiq_balance: {totalCredits: 2378, renewableCredits: 1628/2000, addOnCredits: 750/750, resets 2026-10-01}
Higgsfield MCP:           no dedicated "Higgsfield MCP" exists. Higgsfield access (hf_mult_motion_control / hf_mult_replace_object) is one feature inside a broader media-generation MCP server (also does images/video/audio/voice/3D/website/TikTok). That server's balance call is REACHABLE: {credits: 2437.25, plan: "free"}. This is a platform-wide credit balance, not a Higgsfield-specific one — it does not tell us the Higgsfield USD/credit rate the WO needs for providers.yaml.
HyperFrames MCP:          NOT FOUND. No MCP server exposes HyperFrames; it's CLI-only, wrapped by the `hyperframes-cli` skill (and sibling hyperframes-* skills) — and the CLI binary itself is not installed/on PATH right now (see above). Any T2 Accept check that runs `hyperframes check ...` cannot execute on this machine until the CLI is installed.
```

**Findings:**
- HyperFrames CLI is not installed on this machine right now. T2's Accept criteria (`hyperframes check assets/composition-skeleton.html` exit 0, lint-vs-check reconciliation) cannot run until it is. This blocks T2, not just slows it.
- "Higgsfield MCP" as a distinct reachability target doesn't exist the way §0.5 assumes; it's a capability of a general-purpose media MCP. Gate 0's "Higgsfield USD per credit" answer will need to come from Kim's actual billing/plan page, not from an MCP balance call.
- `python3` is 3.9.4 — quite old (no `python3 -m venv` issues expected for the validator scripts, but worth flagging if T5's scripts want anything requiring 3.10+ syntax).

## 0.6 — Report and video paths

```
./REPORT.md                          — exists at repo root
./REPORT-2026-09-01.md               — exists at repo root
videos/centella-tiger-grass/         — exists, populated (AGENTS.md, BRIEF.md, CLAUDE.md, STORYBOARD.md, assets/, compositions/, frame.md, hyperframes.json, index.html [+ a .bak], meta.json, package.json, renders/, thumbnail/)
```

## 0.7 — Current voiceover path (S4)

`decision-policy.md` and `pipeline-runbook.md` reference `vidiq_voiceover_list_voices` / a "baseline voice id" at S4 (`pipeline-runbook.md:41` — *"confirm the baseline voice id still exists"*; `decision-policy.md:117` — *"ledger: voice id"*), but **neither file names an actual current tool/voice id** — it's described generically as "the baseline voice," not pinned to a specific vidIQ voice ID or an explicit non-vidIQ TTS provider. This is the fact Gate 0's third answer slot needs from Kim directly (I can't infer a specific voice ID from the skill text) — recommend Kim also check the most recent shipped video's ledger (e.g. `ectoin-survival-molecule` or `videos/_channel/` if a ledger of past voice ids exists) rather than guessing.

---

## Summary for Gate 0

The mechanical inventory (§0.1, 0.2, 0.5, 0.6) matches what the WO expected in shape, with three deviations worth flagging before Kim answers the three slots:

1. **Stale premise on T2.** The repo's `faceless-video-craft-v2` already contains the full rule merge (K-1..K-5, 8 restored v1 rules, the three policy-defect fixes) that T2 is scoped to produce — done via ordinary commits (`d7e07e3`, `6e6c202`) between when the WO's source chats happened and now. T2 needs re-scoping from "do the merge" to "verify, document (`merge-matrix.md`), and account for the 2 extra rules (R7/R8) and the concurrent-edit risk" before Opus/High time is spent on it.
2. **HyperFrames CLI is not installed on this machine.** Several Accept checks across T2/T5 can't run until it is. Flagging as a blocker per §1.5 ("a genuine blocker with a name"), not proceeding past it silently.
3. **Invocation collision is 3-way, not 2-way.** `anthropic-skills:faceless-video-craft` (plugin-scoped) is a third live candidate alongside the two project copies, with a description close to v2's. T3's "single source of truth" work should account for this third source, which the WO's machine-scan (§0.2) has no category for since it isn't a local file.

No edits have been made to `.claude/skills/`, `decision-policy.md`, or any other content file in this run — this is inventory only, per the Gate 0 instruction to stop here.
