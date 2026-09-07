# Gate 0 — WO-FVC-005 answer sheet
Status: **ANSWERED, G0-4 corrected same day** (Kim, 2026-09-07) — the three required slots are resolved; G0-4's plan/rate was corrected from Creator to Pro after a live re-check found the earlier answer stale. Note: T0–T8 already ran and merged to `origin/master` in the interim (see `wo/FVC-005/HANDBACK.md`) on these same defaults; this sheet is being closed out retroactively so the ruling is on record rather than only in chat.
Pre-filled values are defaults or repo-derived facts, not decisions — check them before writing `approved`.

---

## Required, no repo-derivable answer

▸ **G0-1 — Claude Design URL of `seoulhabit-system`** for `claude_design` MCP import. Two projects share this name in the account (see the blocker below) — confirm `a7945a95-da21-4823-8b16-57c6ffa11558` is the intended one before T2 extracts it: **CONFIRMED (Kim, 2026-09-07).** Re-verified directly by reading both projects' `readme.md` via the DesignSync tool: `a7945a95-…`'s readme is titled "SeoulHabit Video Design System" and contains verbatim the exact 10 components (`ShHook`/`ShIngredient`/`ShRows`/`ShSteps`/`ShCompare`/`ShEvidence`/`ShMyth`/`ShQuote`/`ShEndcard`/`ShChip`), the exact 6 templates (T1–T6), and the exact palette this WO ships. `75132ad8-…` is a different, unrelated design system (React/Tailwind, EB Garamond/Inter, aqua/coral/highlighter — the "Ingredient Passport" lane's system, not this one). T2's extraction stands as final.

▸ **G0-4 (½) — HeyGen $/credit**, from the plan page. `get_current_user`-equivalent fills the credit counts for free (see pre-filled below); the price does not resolve from any tool: **CORRECTED (2026-09-07, same day, later in the session).** First recalled as Creator ($29/mo/600 → 0.0483) and written into `providers.yaml`; a live `hyperframes auth status` re-check minutes later (after an OAuth token refresh — the stored token had expired) shows the account is actually on **Pro** ($49/mo for 1000 credits) → `usd_per_credit = 0.049`. Both the pre-filled G0-4 credit-count row below (line 23) and this WO's own T0 probe recorded the plan as `creator` on 2026-09-06/07 — either the account changed plan between that probe and this re-check, or the earlier reads were wrong; not distinguished here, flagged for Kim. Corrected value written into `claude-skills` `providers.yaml` (branch `session/fvc-005-g04-pro-fix`, superseding `session/fvc-005-gate0-pricing`). Applies uniformly across every HeyGen credit row (speech/image/enhance/audio/render) since it's the plan's blended credit price, not a per-tool cost — does not itself unblock F2–F4 or measure credits-per-call.

▸ **G0-8 — Palette conflict** (video cream/indigo/clay vs Nocturne brand sheet). WO default says "whatever `seoulhabit-system` holds" — confirmed the extracted project's palette is cream `#F4EDE3` / ink `#26215C` / clay `#9C3A32` / brass `#C0A265`. Confirm this is the palette to ship, not the Nocturne sheet: **CONFIRMED (Kim, 2026-09-07).** Ship the extracted cream/ink/clay/brass palette — it's already the palette rendered in the real `centella-asiatica` pilot (T5), so this also avoids re-rendering everything produced to date. No Nocturne brand sheet was found anywhere in this repo to compare against; if one exists elsewhere, it was not consulted.

---

## Pre-filled from the repo and live tool calls (confirm or override)

▸ **G0-2 — Videos repo + branch:** `Story Board` repo, fresh branch `session/fvc-005` off `master` `c97201d`, worked in an isolated worktree per `CLAUDE.md`. Override: ___

▸ **G0-3 — `claude-skills` repo path:** `/Users/sumitchoudhary/Desktop/claude-skills` (confirmed live — matches the path recorded in WO-FVC-001 Gate 0 and re-verified via `readlink ~/.claude/skills/makemeavideo`). Branch `fvc-005/makemeavideo`, created off `master` without disturbing another session's 5 uncommitted `faceless-video-craft` files (diffstat verified byte-identical before/after branch creation). Override: ___

▸ **G0-4 (½) — HeyGen credits (measured, free):** `hyperframes auth status` → account `hello@seoulhabit.com`, plan **`creator`**, premium credits **0** (resets 2026-10-06), add-on credits **81**. No free-tier row exists on this plan — R-1's cap is corrected to be denominated in credits, not in a render count (see WO §8.3). **STALE, re-read 2026-09-07 (see line 11):** plan now reads `pro`, premium credits **243** (resets 2026-10-06), add-on credits **41**. The add-on drop from 81→41 isn't explained by this WO's own cost table (T0–T8's HeyGen spend was $0 throughout) — worth Kim checking the account directly. Override: ___

▸ **G0-5 — Render machine:** this machine. `hyperframes doctor`: Node v24.18.0, 8 cores, 16 GB RAM (5.6 GB free), 363 GB disk free, Chrome headless-shell cached, FFmpeg/FFprobe 8.1.2, whisper-cpp present, MusicGen deps installed. **Gaps:** Kokoro TTS not installed (`pip install kokoro-onnx soundfile`); Docker absent (not a T0 halt — local render does not need it). `hyperframes` resolves globally at v0.8.30 (**not** via `npx` — see WO §8.2). Override: ___

▸ **G0-6 — `serif-split` vs `serif-everywhere`:** `serif-split` (WO default), and now confirmed against the actual source: the extracted design system's own readme states this exact split verbatim — DejaVu Serif Bold for ingredient names/titles/end cards, Archivo for functional captions and hooks. Override: ___

▸ **G0-7 — Pilot page:** `centella-asiatica`, confirmed by data — 12 citations / 12 findings, the strongest of the 21 published passports on `seoulhabit-learn` (site repo below), and an existing prior video to compare against. Override: ___

---

## New slots this WO needs that WO-FVC-004's sheet had no reason to ask

▸ **G0-9 — Story-source site + pin.** R-3 names no repo. Resolved this session: `~/Desktop/SeoulHabit/seoulhabit-learn`, remote `github.com/seoulhabit/seoulhabit-learn`, clean tree at commit `cacff81`. Route contract `/ingredient/${handle}` (`src/routes/passports.ts`), 21 routed passports, all `published`. Confirm this is the canonical site, and confirm pinning `03-beat-sheet.json`'s `story.sha` to `cacff81` for the centella pilot: ___

▸ **G0-10 — `channel.yaml` vs `baseline.yaml`.** The skill's 0.2.0 pipeline reads `videos/_channel/channel.yaml` in 43 places; the repo has `videos/_channel/baseline.yaml` and no `channel.yaml` anywhere (confirmed via `find`). Rename the file in the repo, or correct the skill's path back to `baseline.yaml`? Default if left blank: **rename the repo file to `channel.yaml`**, since three prior sessions' worth of skill text already assumes that name: ___

---

## What is blocking Gate 0 regardless of these answers

1. ~~Two Claude Design projects share the name "SeoulHabit Video Design System."~~ **RESOLVED — see G0-1 above.** `a7945a95-…` confirmed correct by content, not just name/date.
2. **Neither design-system project carries a version string.** R-4's "v5.0" cannot be verified against the source. T2 synthesised a version anchor (project UUID + `updatedAt` + a sha256 manifest of what was extracted) — this is disclosed, not hidden, but it means "v5.0" should be dropped from future WO text in favour of the manifest. Still open — no version string has appeared since.
3. **`F1` (local render parity, WO §3 T1) is not being spent against.** **RULED (Kim, 2026-09-07): no spend.** Declined to spend the ~5-8 add-on credits that would fully resolve F1 — `F1` stays **PARTIAL**, and rule **`C-6`, hard cuts only** (no shader chain in the compiler) stands until this is revisited. Recorded in `providers.yaml`'s `render_cloud` row.
4. **`F2`/`F3`/`F4` need a HeyGen MCP tool surface this Claude Code session doesn't have.** **UPDATED 2026-09-07, same day, later:** the `hyperframes` CLI's own HeyGen OAuth is now live (Kim authorized it; a stale token needed one `hyperframes auth refresh`) — `hyperframes auth status` correctly reads the live account. That did **not** unblock F2–F4: this Claude Code session has no callable tool for HeyGen's `create_speech`/image-gen/enhance endpoints at all. The HyperFrames MCP's own docs disable those for CLI/IDE agents by design (hosted chat clients only), and `hyperframes tts` is a *local* Kokoro-82M fallback, not HeyGen's cloud API — running it just reconfirmed Kokoro still isn't installed here. Kim then registered a dedicated `heygen` MCP server (`claude mcp add --transport http heygen https://mcp.heygen.com/mcp/v1/`); `claude mcp list` shows it added but **`! Needs authentication`** (a separate login from the CLI OAuth above), and a newly-added MCP server's tools don't load into an already-running session regardless. **Still open**: Kim needs to authenticate that server and start a fresh session before F2–F4 can run for real.
5. **NEW (2026-09-07): the shared `~/Desktop/claude-skills` checkout was stuck on stale 0.2.0 content**, 4 merges behind `origin/master`, because its working branch carried another session's uncommitted `faceless-video-craft` files that this session correctly declined to discard (`wo/FVC-005/HANDBACK.md` §3). **RESOLVED**, without touching that checkout at all: `~/.claude/skills/makemeavideo` now symlinks to a fresh clone (`~/Desktop/claude-skills-current`, confirmed at 0.3.0). The old checkout and its in-flight WIP are untouched.

**STOP conditions cleared:** G0-1, G0-4's $/credit (now corrected to Pro), and G0-8's palette are all confirmed above. **Still open:** F2–F4 (item 4) — narrowed from an auth problem to a tool-surface + second-login problem, but still not clearable from this session. Only Kim, authenticating the new `heygen` MCP server and starting a fresh session, can finish this.
