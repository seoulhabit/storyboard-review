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

**Verdict: BLOCKED-CONNECTOR.** The HeyGen MCP tools (`create_speech`,
`list_voices`, `create_brand_glossary`) require an authorized connector this
non-interactive session cannot establish (OAuth needs an interactive
session, per the system prompt's own constraint). Per D3, this finding is
attempted for real once Kim authorizes the connector — not guessed, not
skipped silently.

**Local substitute available, not yet run:** `hyperframes tts` (local
Kokoro-82M) can produce a 60-word sample at zero HeyGen cost the moment
`pip install kokoro-onnx soundfile` is done (`hyperframes doctor` names this
exact command as the only gap). This substitute proves *fidelity* (does the
audio read the words correctly, including INCI-style terms) but not
HeyGen's *cost* — a local TTS engine has no credit ledger. If F2 is answered
via the local substitute rather than the connector, `providers.yaml`'s VO
cost row stays `usd_per_credit: null` / cost-per-call `unmeasured`, named as
such, not defaulted to zero.

## F3 — Image generation reach + cost

**Pass:** recorded either way (yes with cost + face check, or no).
**Fail consequence (pre-written):** `S5a` uses the library lane; HeyGen
image is out of the run path.

**Verdict: BLOCKED-CONNECTOR**, same reason as F2 — `list_video_agent_styles`
/ image-generation tools are behind the same unauthorized connector. Not
answerable locally (there is no local substitute for "does this specific
MCP expose image generation" — that is a fact about the connector, not
about this machine).

**Independent finding, not requiring the connector:** the design system
extracted for `T2` (Claude Design project `a7945a95…`) states its own
imagery rule explicitly: *"There is no photography, no gradient, no
texture, no pattern and no video underlay anywhere in the system… If
imagery is ever introduced it will need a ruling."* So **even once F3 is
answered, the design system as it stands has no scene that would consume a
generated image** — F3's fail branch (library lane) is very likely moot for
this WO's actual templates, T6 possibly excepted. Recorded as an
observation, not a substitute verdict — F3 itself stays BLOCKED-CONNECTOR
until Kim authorizes the connector and the question is actually asked.

## F4 — Enhanced composition retrievability

**Pass:** after one free enhance turn, the enhanced HTML/assets are
retrievable and render locally, still passing `check`.
**Fail consequence (pre-written):** enhance step out of the lane; sound is
local (`S5c` first option).

**Verdict: BLOCKED-CONNECTOR**, same reason. Not locally substitutable —
"enhance" is a HeyGen-side operation on a HeyGen-hosted project with no
local equivalent to test against.

---

## Summary

| # | Finding | Verdict |
|---|---|---|
| F1 | Local render parity | **PARTIAL** — local clean; cloud leg not run (D2). **Consequence: rule `C-6`, hard cuts only, applied now.** |
| F2 | VO cost + fidelity | **BLOCKED-CONNECTOR** — local substitute (`hyperframes tts`) available once Kokoro is installed; does not answer the cost half |
| F3 | Image generation reach | **BLOCKED-CONNECTOR** — likely moot regardless, given the design system's own no-imagery rule |
| F4 | Enhance retrievability | **BLOCKED-CONNECTOR** — no local substitute exists |

**Acceptance, per the WO's own bar** ("all four findings written with their
evidence; Finding 1 = PASS; spend ≤ G0-4"): **not met as literally stated** —
F1 is PARTIAL, not PASS, and F2–F4 are blocked, not found. This is reported
plainly rather than rounded up. It does not halt this session's work: D2/D3
were made *with* this consequence stated in advance, so `T2`/`T3` proceed on
the C-6 ruling and the connector-blocked findings are Kim's to unblock live,
named individually rather than defaulted.

`providers.yaml`: HeyGen VO/image/enhance costs remain **unmeasured**, named
as such — not zero, not guessed. The one number that *is* measured without
spending anything: the public cloud-render rate, 20 credits/rendered
minute, against this account's 81 add-on credits (≈4 minutes of cloud
render for the whole month) — see `docs/wo/WO-FVC-005.md` §8.3.
