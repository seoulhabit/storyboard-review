# T1-FINDINGS.md — WO-FVC-005 spike
Criteria written before any tool call, per the WO's own T1 instruction. Verdicts filled in below each, in order, as each finding was actually run — never edited after the fact to match a result.

---

## F1 — Local render parity

**Pass:** `hyperframes check` 0 errors; shader-boundary frame non-black
locally; font/colour match on a pixel diff of ≥ 3 frames within a tolerance
written in advance (±3 on any 8-bit channel, mean absolute error over the
frame ≤ 1.5).
**Fail consequence (pre-written):** shader chains forbidden in local
compositions (hard cuts only) — rule **`C-6`** added; cloud render stays
gated by R-1 regardless.

**Verdict: PARTIAL.** By this session's D2 ruling, zero HeyGen credits are
spent proving the cloud leg — no `import-claude-design-from-url` /
`get_project` cloud-preview pull was attempted, so there is no cloud frame
to diff against. What *was* run and is real:

- `hyperframes check --json` on a real local render (the T0 smoke test):
  `ok: true`, `lint`/`runtime`/`layout`/`motion`/`contrast` all
  `errorCount: 0`.
- The rendered frame at each sampled point is confirmed non-blank (visual
  content present throughout a 10.0s render, 300/300 frames captured).
- No shader-boundary frame exists to check, because the local composition
  used for this smoke test (`blank`) has no shader transition — that is
  exactly the point D2 pre-empts: this WO ships with **no shader path at
  all**, so there is no shader boundary to ever measure in production.

**Consequence, exactly as pre-written:** local render is clean, cloud parity
is unmeasured, so the fail branch fires: **rule `C-6` — hard cuts only, no
contiguous shader chain — is added.** This is not a downgrade decided after
the fact; it is the WO's own stated consequence for exactly this outcome,
applied because D2 chose not to spend the credits that would have let F1
resolve fully.

## F2 — VO cost + fidelity

**Pass:** credits delta recorded; duration returned; ≤ 1 mispronunciation on
a 60-word scene read by the channel voice via `create_speech`.
**Fail consequence (pre-written):** brand glossary entries added
(`create_brand_glossary`) before any production VO.

**Re-run 2026-09-07, connector now authorized. Verdict: BLOCKED-CREDITS**
(new finding — supersedes the earlier BLOCKED-CONNECTOR; the connector
itself is no longer the obstacle). What was actually done, in order:

1. `get_current_user` (before): `plan: pro`, `premium_credits.remaining: 243`
   (resets 2026-10-06), `add_on_credits.remaining: 41`. Both figures
   **correct** the 2026-09-06 record in `providers-measured.md` (`plan:
   creator`, premium `0`, add-on `81`) — the account state is materially
   different now, whether from a plan change or a reset in the interim; not
   assumed, just re-measured.
2. `list_voices(engine=starfish, gender=female, language=English)` —
   succeeded, returned 20 voices with `next_token` for more. Picked
   **"Annie - Lifelike"** (`voice_id 330290724a1b470fb63153f34d4c0183`) as
   the **test** voice for this spike only — **not** a production pick.
   `baseline.yaml`'s `heygen.voice_id` stays `null`; that choice is T2's
   TOUCHPOINT-SETUP, not T1's.
3. Composed the 60-word scene (word-counted, not estimated) with two
   INCI-adjacent terms chosen for pronunciation risk:

   > Centella Asiatica Extract is not just a trend ingredient. It carries
   > decades of wound healing research behind it. Its active compounds,
   > Madecassoside and Asiaticoside, work by stimulating collagen synthesis
   > and calming inflammation at the cellular level. A twenty eleven
   > clinical trial found a four percent concentration performed on par
   > with hydroquinone for reducing redness over eight weeks, without the
   > irritation.

4. `create_speech(text=<above>, voiceId=330290724a1b470fb63153f34d4c0183)`
   → **HTTP 402**, `error_code: insufficient_credit`: *"This operation
   requires 'api' credits. Upgrade your plan at
   https://app.heygen.com/home?upgrade"*.
5. `get_current_user` (after): `premium_credits.remaining: 243`,
   `add_on_credits.remaining: 41` — **unchanged**. The 402 charged nothing;
   confirmed, not assumed.

**What this establishes, precisely:** `create_speech` draws from a third
credit pool — **"api" credits** — that is disjoint from the
`premium_credits` / `add_on_credits` the subscription actually carries and
that `get_current_user` reports (`wallet: null`, `usage_based: null`; no
`api_credits` field anywhere in the response). This account currently holds
**zero** of that pool. No amount of the 243 + 41 credits already on the
account enables a single `create_speech` call. This is a **billing-page
action for Kim** (the 402's own `upgrade` link), not a connector or OAuth
problem, and not fixable from this session.

**Not run, as a direct consequence:** the duration/fidelity half of F2
(mispronunciation count) — no audio was ever generated, so there is nothing
to assess. The WO's pre-written fail consequence ("brand glossary entries
added before any production VO") is a response to a **fidelity** failure
specifically; it does not fire here, because fidelity was never reached —
recorded as not-applicable rather than force-fit to a branch that assumed a
different failure mode. `hyperframes tts` (local Kokoro-82M) remains the
only fidelity-only substitute, still not run this pass (out of scope here;
see the 2026-09-06 note below for its own installation gap on this
machine).

## F3 — Image generation reach + cost

**Pass:** recorded either way (yes with cost + face check, or no).
**Fail consequence (pre-written):** `S5a` uses the library lane; HeyGen
image is out of the run path.

**Re-run 2026-09-07, connector now authorized. Verdict: NOT EXPOSED** — a
final "no," not a block. Answered by tool inventory alone, at zero cost (no
call was needed once the connector question stopped being the obstacle):
the full `mcp__heygen__*` surface was enumerated and contains no
general-purpose text-to-image or image-generation tool. The only
image-producing tools are **avatar-scoped** — `create_photo_avatar`
(photo→avatar), `create_prompt_avatar` (text→avatar face),
`create_digital_twin` (video→avatar) — each produces a person/character
avatar look, not an arbitrary plate (an ingredient hero, a texture). Even
disregarding that mismatch, all three are avatar tools and therefore
forbidden outright by `R-2`'s scope fence and by `H-3` (faceless on
pixels) for this brand, independent of whether they're "exposed." So: **no**
is the honest, final answer to F3's own question, and it does not need
revisiting once account/billing state improves — this is a fact about the
MCP's tool surface, not about credits or auth.

**Fail branch fires as pre-written:** `S5a` uses the library lane; HeyGen
image generation is out of the run path. This is now the **resolved**
state, not a placeholder — it agrees with, and firms up, the independent
observation already on record: the extracted design system (`T2`, Claude
Design project `a7945a95…`) states its own no-imagery rule (*"There is no
photography, no gradient, no texture, no pattern and no video underlay
anywhere in the system"*), so the library lane itself is very likely a
structural no-op for this WO's actual templates too.

## F4 — Enhanced composition retrievability

**Pass:** after one free enhance turn, the enhanced HTML/assets are
retrievable and render locally, still passing `check`.
**Fail consequence (pre-written):** enhance step out of the lane; sound is
local (`S5c` first option).

**Re-run 2026-09-07, connector now authorized. Verdict: BLOCKED-CLIENT-TYPE**
(new finding — also supersedes BLOCKED-CONNECTOR, but for a reason that
does **not** go away when Kim authorizes anything further). Probed for
real: called `mcp__…__compose` on the HyperFrames project MCP with a
no-op prompt explicitly asking only to observe availability, no project
created. It was rejected outright, before any credit or project check:

> Hosted HyperFrames compose/render is disabled for local CLI/IDE agents
> (Claude Code, Cursor, Codex, and similar). These environments have a
> local filesystem, so author HyperFrames with the local HyperFrames
> skills instead… This hosted MCP remains the path for chat clients with
> no local filesystem (Claude.ai web/desktop, ChatGPT, Grok).

No project was created (no `project_id` returned), so this cost nothing.
**"Enhance" has no dedicated tool anywhere in either MCP surface** (the
`heygen` server or this HyperFrames-project server) — the closest
candidate is an edit turn via `compose` on an already-imported project,
and `compose` is exactly what this client type is refused. This means F4
is **not answerable from a Claude Code / CLI session at all, regardless of
account state or connector authorization** — it would need to run from a
hosted chat client (claude.ai web/desktop, ChatGPT, Grok) with no local
filesystem, which is a different operating context than every other task
in this WO (T0–T8 have all run from Code). This is an architectural fact
about where this WO's tooling runs, not a to-do that clears with a billing
or OAuth fix.

**Fail branch fires, unconditionally for this client type:** `S5c` stays
local-first; HeyGen enhance is out of the lane for any CLI-run production
under this WO, not just for this account today.

---

## Summary

| # | Finding | Verdict |
|---|---|---|
| F1 | Local render parity | **PARTIAL** — local clean; cloud leg not run (D2). **Consequence: rule `C-6`, hard cuts only, applied now.** |
| F2 | VO cost + fidelity | **BLOCKED-CREDITS** (2026-09-07, connector live) — `create_speech` needs a separate "api" credit pool this account has none of; a billing-page action for Kim, confirmed to charge nothing on the 402 |
| F3 | Image generation reach | **NOT EXPOSED** (2026-09-07, resolved) — no general-purpose image-generation tool in the `heygen` MCP; only avatar-scoped tools exist, and those are forbidden outright by `R-2`/`H-3` regardless. `S5a` fail branch (library lane) is final |
| F4 | Enhance retrievability | **BLOCKED-CLIENT-TYPE** (2026-09-07) — `compose`/enhance is refused outright to CLI/IDE clients by the MCP server itself; unreachable from any Code session regardless of account or auth state |

**Acceptance, per the WO's own bar** ("all four findings written with their
evidence; Finding 1 = PASS; spend ≤ G0-4"): **still not met as literally
stated** — F1 is PARTIAL, F2 is now blocked on billing rather than auth, F3
is finally resolved (a real "no"), and F4 is blocked for architectural
reasons this session cannot change. Reported plainly, not rounded up.
Authorizing the connector (D3's ask) genuinely moved F3 to done and
reclassified F2/F4 from a vague "connector" block to two distinct, more
actionable ones — one a billing-page click, one a client-type limit that
needs a different session type entirely, not another authorization.

`providers-measured.md` (this repo's working record; the shipped skill's
`claude-skills/…/references/providers.yaml` remains out of scope here, per
T7): HeyGen VO/enhance costs remain **unmeasured**, named as such with the
*new, narrower* reason each is unmeasured. Image cost is now **N/A** (no
tool exists to price). The public cloud-render rate, 20 credits/rendered
minute, stays the only HeyGen cost number actually priced without spending
anything — see `docs/wo/WO-FVC-005.md` §8.3.
