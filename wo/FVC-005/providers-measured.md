# providers.yaml — measured numbers, WO-FVC-005 T1

This is **not** an edit to `claude-skills/makemeavideo/references/providers.yaml`
— that file is a `T7` (skill-cut, session S-D) deliverable, out of scope for
this pass. This records what T1 actually measured or could not measure, so
T7 has real numbers to write in rather than re-deriving them.

## Measured without spending anything

| Row | Value | Source |
|---|---|---|
| HeyGen plan | `creator` | `hyperframes auth status`, this session |
| HeyGen premium credits | 0 (resets 2026-10-06) | same |
| HeyGen add-on credits | 81 | same |
| Public cloud-render rate | 20 credits / rendered minute | WO §0, unchanged, not spent against |
| Effective monthly cloud-render ceiling, this account | **~4.05 minutes** (81 ÷ 20) | derived |
| Local render wall time, draft quality, 10s @ 1920×1080 | 24.6s (300 frames, 5 workers) | this session, `hyperframes render -q draft` |
| Local render cost | **0 credits** (machine time only) | same |

## Not measured — blocked on the HeyGen MCP connector (T1-FINDINGS.md F2–F4)

| Row | Status |
|---|---|
| `heygen.speech_per_call` (create_speech, credits) | unmeasured — connector not authorized this pass |
| `heygen.image_per_call` (if exposed) | unmeasured — same; also possibly moot, design system forbids imagery by rule |
| `heygen.enhance_per_turn` | unmeasured — same |
| `usd_per_credit` | unresolved — Gate 0 G0-4, needs Kim's plan page regardless of connector state |

## R-1 cap, corrected (WO §8.3)

The WO's default cloud-render cap ("3, the free-tier allowance") does not
apply to this account — there is no free tier row on the `creator` plan.
Recommend `channel.yaml`/`baseline.yaml` `heygen.cloud_render_credits_cap`
be set in **credits**, not renders, at a small fraction of 81 (e.g. one
20-credit reserve = one rendered minute of cloud fallback per month) —
Kim's call at Gate 0, not defaulted here.
