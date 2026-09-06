# Gate 0 — WO-FVC-005 answer sheet
Status: **DRAFT** — most slots pre-filled from the repo and live tool calls this session; three need Kim regardless.
Pre-filled values are defaults or repo-derived facts, not decisions — check them before writing `approved`.

---

## Required, no repo-derivable answer

▸ **G0-1 — Claude Design URL of `seoulhabit-system`** for `claude_design` MCP import. Two projects share this name in the account (see the blocker below) — confirm `a7945a95-da21-4823-8b16-57c6ffa11558` is the intended one before T2 extracts it: ___

▸ **G0-4 (½) — HeyGen $/credit**, from the plan page. `get_current_user`-equivalent fills the credit counts for free (see pre-filled below); the price does not resolve from any tool: ___

▸ **G0-8 — Palette conflict** (video cream/indigo/clay vs Nocturne brand sheet). WO default says "whatever `seoulhabit-system` holds" — confirmed the extracted project's palette is cream `#F4EDE3` / ink `#26215C` / clay `#9C3A32` / brass `#C0A265`. Confirm this is the palette to ship, not the Nocturne sheet: ___

---

## Pre-filled from the repo and live tool calls (confirm or override)

▸ **G0-2 — Videos repo + branch:** `Story Board` repo, fresh branch `session/fvc-005` off `master` `c97201d`, worked in an isolated worktree per `CLAUDE.md`. Override: ___

▸ **G0-3 — `claude-skills` repo path:** `/Users/sumitchoudhary/Desktop/claude-skills` (confirmed live — matches the path recorded in WO-FVC-001 Gate 0 and re-verified via `readlink ~/.claude/skills/makemeavideo`). Branch `fvc-005/makemeavideo`, created off `master` without disturbing another session's 5 uncommitted `faceless-video-craft` files (diffstat verified byte-identical before/after branch creation). Override: ___

▸ **G0-4 (½) — HeyGen credits (measured, free):** `hyperframes auth status` → account `hello@seoulhabit.com`, plan **`creator`**, premium credits **0** (resets 2026-10-06), add-on credits **81**. No free-tier row exists on this plan — R-1's cap is corrected to be denominated in credits, not in a render count (see WO §8.3). Override: ___

▸ **G0-5 — Render machine:** this machine. `hyperframes doctor`: Node v24.18.0, 8 cores, 16 GB RAM (5.6 GB free), 363 GB disk free, Chrome headless-shell cached, FFmpeg/FFprobe 8.1.2, whisper-cpp present, MusicGen deps installed. **Gaps:** Kokoro TTS not installed (`pip install kokoro-onnx soundfile`); Docker absent (not a T0 halt — local render does not need it). `hyperframes` resolves globally at v0.8.30 (**not** via `npx` — see WO §8.2). Override: ___

▸ **G0-6 — `serif-split` vs `serif-everywhere`:** `serif-split` (WO default), and now confirmed against the actual source: the extracted design system's own readme states this exact split verbatim — DejaVu Serif Bold for ingredient names/titles/end cards, Archivo for functional captions and hooks. Override: ___

▸ **G0-7 — Pilot page:** `centella-asiatica`, confirmed by data — 12 citations / 12 findings, the strongest of the 21 published passports on `seoulhabit-learn` (site repo below), and an existing prior video to compare against. Override: ___

---

## New slots this WO needs that WO-FVC-004's sheet had no reason to ask

▸ **G0-9 — Story-source site + pin.** R-3 names no repo. Resolved this session: `~/Desktop/SeoulHabit/seoulhabit-learn`, remote `github.com/seoulhabit/seoulhabit-learn`, clean tree at commit `cacff81`. Route contract `/ingredient/${handle}` (`src/routes/passports.ts`), 21 routed passports, all `published`. Confirm this is the canonical site, and confirm pinning `03-beat-sheet.json`'s `story.sha` to `cacff81` for the centella pilot: ___

▸ **G0-10 — `channel.yaml` vs `baseline.yaml`.** The skill's 0.2.0 pipeline reads `videos/_channel/channel.yaml` in 43 places; the repo has `videos/_channel/baseline.yaml` and no `channel.yaml` anywhere (confirmed via `find`). Rename the file in the repo, or correct the skill's path back to `baseline.yaml`? Default if left blank: **rename the repo file to `channel.yaml`**, since three prior sessions' worth of skill text already assumes that name: ___

---

## What is blocking Gate 0 regardless of these answers

1. **Two Claude Design projects share the name "SeoulHabit Video Design System."** `a7945a95-da21-4823-8b16-57c6ffa11558` (updated today, matches every component/palette/template R-4 names) and `75132ad8-b81c-4151-8a4c-83368df1d949` (Aug 28, a different system — Montserrat, icons, scrims). T2 will extract `a7945a95…` on the strength of the match; G0-1 above asks Kim to confirm that reading before the extraction is treated as final, since picking wrong means re-deriving all of T2.
2. **Neither design-system project carries a version string.** R-4's "v5.0" cannot be verified against the source. T2 will synthesise a version anchor (project UUID + `updatedAt` + a sha256 manifest of what was extracted) — this is disclosed, not hidden, but it means "v5.0" should be dropped from future WO text once Gate 0 clears, in favour of the manifest.
3. **`F1` (local render parity, WO §3 T1) is not being spent against.** Per this session's ruling: zero HeyGen credit spend for the render-parity check. `F1` resolves **PARTIAL** — local render clean, cloud-parity leg unmeasured — which fires the pre-written fail branch: rule **`C-6`, hard cuts only**, no shader chain in the compiler. This is a scoping choice available to Kim to override (spending ~5-8 of the 81 add-on credits would let `F1` resolve fully), but the default going forward is C-6.
4. **`F2`/`F3`/`F4` need the HeyGen MCP connector authorized live**, which this non-interactive pass cannot do. Kim: authorize when convenient; T1 runs those three findings for real once done, with `hyperframes tts` (needs the Kokoro install above) as the named local fallback if OAuth does not hold.

**STOP. Waiting for G0-1 confirmation, G0-4's $/credit, G0-8's palette confirmation, G0-9/G0-10 on the new slots, the HeyGen connector for F2–F4, and Kim's `approved` before T2/T3 land as final (T0/T1's environment and local-only findings may proceed now — they spend nothing and commit nothing irreversible).**
