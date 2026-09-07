# providers.yaml — measured numbers, WO-FVC-005 T1

This is **not** an edit to `claude-skills/makemeavideo/references/providers.yaml`
— that file is a `T7` (skill-cut, session S-D) deliverable, out of scope for
this pass. This records what T1 actually measured or could not measure, so
T7 has real numbers to write in rather than re-deriving them.

## Measured without spending anything

| Row | Value | Source |
|---|---|---|
| HeyGen plan | `pro` **(corrected 2026-09-07 — was `creator`)** | `get_current_user`, this session |
| HeyGen premium credits | 243 (resets 2026-10-06) **(corrected — was 0)** | same |
| HeyGen add-on credits | 41 **(corrected — was 81)** | same |
| Public cloud-render rate | 20 credits / rendered minute | WO §0, unchanged, not spent against |
| Effective monthly cloud-render ceiling, this account | **~1.4 minutes** on add-on credits alone (41 ÷ 20); premium/add-on credit interchangeability for renders is not confirmed here — re-derive once that's known | derived, 2026-09-07 numbers |
| Local render wall time, draft quality, 10s @ 1920×1080 | 24.6s (300 frames, 5 workers) | 2026-09-06 session, `hyperframes render -q draft` |
| Local render cost | **0 credits** (machine time only) | same |
| `heygen.image_per_call` | **N/A** — no general-purpose image-generation tool exists in the `heygen` MCP surface; only avatar-scoped tools (`create_photo_avatar`, `create_prompt_avatar`, `create_digital_twin`), forbidden outright by `R-2`/`H-3` regardless of cost | T1-FINDINGS.md F3, 2026-09-07, tool-inventory only, zero calls made |

**2026-09-07 note:** the plan/credit figures above changed materially from
the 2026-09-06 record (creator/0/81 → pro/243/41) between sessions — not
explained here, just re-measured and corrected rather than left stale.

## Not measured — newly-diagnosed blockers, not the connector (T1-FINDINGS.md F2, F4; connector authorized 2026-09-07)

| Row | Status |
|---|---|
| `heygen.speech_per_call` (create_speech, credits) | unmeasured — **BLOCKED-CREDITS**, not connector: `create_speech` requires a separate "api" credit pool (`error_code: insufficient_credit`, HTTP 402) that `get_current_user` does not surface at all (`wallet: null`, `usage_based: null`) and this account holds none of. Confirmed the 402 charges nothing (premium/add-on credits identical before and after the call). Needs Kim to add API/usage-based credits at the account's billing page (the 402's own `upgrade` link) — not an OAuth or session-type fix. |
| `heygen.enhance_per_turn` | unmeasured — **BLOCKED-CLIENT-TYPE**: the HyperFrames project MCP's `compose` (the only plausible route to an "enhance" turn — no dedicated enhance tool exists) is refused outright to CLI/IDE clients including Claude Code, confirmed by a real zero-cost probe call. Unreachable from any Code session regardless of account or connector state; would need a hosted chat client (claude.ai web/desktop, ChatGPT, Grok) instead. |
| `usd_per_credit` | unresolved — Gate 0 G0-4, needs Kim's plan page regardless of connector or credit-pool state |

## R-1 cap, corrected (WO §8.3)

The WO's default cloud-render cap ("3, the free-tier allowance") does not
apply to this account — there is no free tier row on the `creator` plan.
Recommend `channel.yaml`/`baseline.yaml` `heygen.cloud_render_credits_cap`
be set in **credits**, not renders, at a small fraction of 81 (e.g. one
20-credit reserve = one rendered minute of cloud fallback per month) —
Kim's call at Gate 0, not defaulted here.
