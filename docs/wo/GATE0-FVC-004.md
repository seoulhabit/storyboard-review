# Gate 0 — WO-FVC-004 answer sheet
Status: **DRAFT** — three slots need Kim; the rest are pre-filled from the repo, per WO-FVC-004 §8.4.
Pre-filled values are defaults or repo-derived facts, not decisions — check them before writing `approved`.

---

## Required, no repo-derivable answer

▸ **G0-1 — The story** for the first run (topic, question, script, outline, research note, or URL): ___

▸ **G0-3 — HeyGen plan + credits** — plan name, credits remaining, **$/credit**: ___
  (`get_current_user` fills remaining credits once the connector exists; the price needs your plan page.)

▸ **G0-6 — Brand tokens** — 3 hex colours + font family, or "read from project skill", or "neutral": ___
  Default if left blank: neutral (navy / off-white / one accent, Inter).

---

## Pre-filled from the repo (confirm or override)

▸ **G0-2 — Channel + repo:** `storyboard-review` — channel `@SeoulHabit`, id `UCzqEGQ9uAU43AgyxGtLT7MA`, 8 subs, 17 public videos as of 2026-09-03 (`videos/_channel/baseline.yaml`). Override: ___

▸ **G0-4 — Spike budget** (max HeyGen credits T0 may burn): `60` (WO default). Override: ___

▸ **G0-5 — Format for the first run:** `both` (WO default; F-2, Shorts path per T0 Finding 4). Override: ___

▸ **G0-7 — Project skill in play?** `none` (WO default — `K-1..K-5` still apply as the floor). Override: ___

▸ **G0-8 — Publish surface:** `manual` (WO default — upload private in Studio, paste envelope). Override: ___

▸ **G0-9 — `/improve` dry-run target:** `d6DPiORuPO4` (WO default). Confirmed this resolves to `videos/centella-tiger-grass` — **not** the same artifact T0 spikes against (`outputs/2026-09-01-how-to-repair-skin-barrier/`, see WO §8.2). Override: ___

▸ **G0-10 — Confirm the command name:** `/makemeavideo` (§7 default). Override: ___

---

## What is blocking Gate 0 regardless of these answers

1. **The HeyGen MCP is not connected on this machine.** No `heygen` entry in `~/.claude.json`, not in the connector registry, no `heygen`-prefixed tool in this session. T0 cannot run until an interactive session completes OAuth to `https://mcp.heygen.com/mcp/v1/`.
2. **Prior art says that connection may not be simple.** WO-FVC-001's own Gate 0 found HeyGen sign-in "unavailable from an automation context" (`wo/FVC-001/gate-0-notes.md:20`). T0's first job, before spending any spike credits, should be confirming the remote MCP's OAuth flow actually succeeds — see WO §8.5.
3. **Two claude.ai library skills need removing** — `makemeavideo` and `faceless-video-craft` are both currently enabled there, which is exactly the two-copies drift the new skill's own version check exists to catch. This can only be done from the account's library settings, not from a coding session. Ledgered as `TOUCHPOINT-LIBRARY-REMOVAL` in `wo/FVC-004/HANDBACK.md`.

**STOP. Waiting for G0-1 / G0-3 / G0-6, for the HeyGen MCP connection, and for Kim's `approved` before T0 runs.**
