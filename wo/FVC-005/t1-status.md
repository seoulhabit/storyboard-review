# T1 — Spike: four findings, pass/fail pre-written — Accept: F1 PARTIAL (evidence-based); F2–F4 correctly BLOCKED-CONNECTOR, not guessed
Commits: Story Board branch `session/fvc-005`; no claude-skills changes this task (providers.yaml edit is T7 scope, deferred — see `providers-measured.md`).

## What shipped

1. **`T1-FINDINGS.md`** written with all four pass/fail criteria stated
   **before** any tool call, per the WO's own instruction — verified by the
   file's own structure (criteria first, verdict second, in that order, for
   each finding).
2. **F1 run for real**, at zero HeyGen cost per this session's D2 ruling:
   the T0 smoke-test render was checked for `check --json` cleanliness (0
   errors across all five categories) and frame content (non-blank
   throughout). No cloud leg was attempted, so F1 resolves **PARTIAL**, not
   PASS — reported as such, not rounded up.
3. **F1's pre-written fail consequence applied immediately, not deferred**:
   rule **`C-6`** (hard cuts only, no shader chain) is now in force for
   everything `T2`/`T3` build. This is a direct, traceable consequence of
   D2, not an independent decision made here.
4. **F2–F4 correctly reported as `BLOCKED-CONNECTOR`**, not skipped and not
   guessed. Each names exactly what tool it needs and why this
   non-interactive session cannot reach it (HeyGen MCP OAuth requires an
   interactive session — a hard platform constraint, not a preference).
5. **One substantive finding recorded independent of the connector**: the
   extracted design system's own readme states it carries no imagery
   whatsoever by rule, which means F3's fail-branch question ("does the
   library lane need to serve any scene?") is very likely moot for this
   WO's actual templates — flagged as an observation, not used to fabricate
   an F3 verdict.
6. **`providers-measured.md`** — the numbers T1 actually produced (HeyGen
   balance, the derived ~4-minute monthly cloud-render ceiling, local
   render cost = 0), kept separate from the shipped `providers.yaml` because
   editing that file is `T7`'s job (skill-cut session), not this one's.

## Accept check — what's verified and what isn't

**Verified:**
- `T1-FINDINGS.md` exists with pre-written criteria visible ahead of every
  verdict — checked by reading the file's own order, not by trusting a
  summary of it.
- F1's local half is real: the same `check --json` output T0 already
  captured, re-read for this finding specifically.
- No HeyGen credits were spent this session — `hyperframes auth status`
  read-only, no `create_speech`/`create_video_agent`/render_video call made.

**Not verified, and I'm not claiming otherwise:**
- **F1's cloud half.** No cloud preview was pulled, no pixel diff against a
  cloud frame exists. The PARTIAL verdict is honest about this — it is not
  a PASS with an asterisk.
- **F2, F3, F4 in full.** All three need the HeyGen MCP connector, which
  needs Kim present for OAuth (D3). Nothing here should be read as "probably
  fine" — they are unanswered, named as such.
- **Whether `hyperframes tts` (Kokoro) actually produces acceptable INCI
  pronunciation.** The local substitute for F2 is *available* (one `pip
  install` away) but was not run this pass — F2 stays BLOCKED-CONNECTOR
  rather than partially answered by a substitute that wasn't actually
  exercised.

## Judgment calls made

- **Applied C-6 now, rather than waiting for a later task to notice F1 was
  PARTIAL.** The WO states the consequence in advance for exactly this
  outcome; applying it immediately means `T2`/`T3` never build a shader path
  that would just be deleted later.
- **Did not fabricate a cost number for HeyGen speech/image/enhance.**
  `providers-measured.md` marks each `unmeasured` rather than defaulting to
  0 or to a guessed figure, because a fabricated number in a budget ledger
  is worse than a named gap — a later stage could spend against it as if it
  were real.
- **Did not edit the shipped `providers.yaml`.** That file's HeyGen role
  rows describe the Video Agent engine this WO is retiring; rewriting it
  correctly is `T7`'s job (rewrite `§H`, retarget the tool fence to R-2,
  fold `[SPIKE:n]` findings into the channel file) and doing it piecemeal
  here would leave it half-migrated.

## Not done (blocked, not skipped)

F2, F3, F4 in full — all named `BLOCKER-CONNECTOR:heygen` in effect, though
not yet a literal ledger token since no run past T1 has tried to consume a
forbidden tool. Kim: authorize the HeyGen MCP connector when convenient;
these three re-run for real the moment it's live, with `hyperframes tts`
(after `pip install kokoro-onnx soundfile`) as the named local fallback for
F2's fidelity half if OAuth does not hold — matching the precedent
WO-FVC-001's own Gate 0 recorded for HeyGen sign-in from an automation
context.
