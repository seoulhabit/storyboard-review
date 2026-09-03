# T7 — Provider registry, cost wrapper, provider rules — DONE

Commit `5fa27f2` pushed to `github.com/seoulhabit/claude-skills`.

## Same stale-premise problem T2 found — this time in rule IDs

Before writing anything, checked whether the WO's planned rule IDs (`R-1`, `A-1`, `V-1`, `B-1`) were actually free. They weren't, mostly:

- **R-1** was already "The gate is the engine's own `check`" — the S7 render/lint gate, cross-referenced constantly as `[S7/R-1]`. A real collision.
- **V-1** was already "Script length from target length" (S4 word budget) — unrelated to voice *provider* selection. A real collision.
- **B-1** was already "Do we have a channel baseline?" (S0 freshness check). A real collision.
- **A-1** ("Asset and mechanism strategy — check the catalog first") was genuinely the right extension point — its existing text already had a generation-provider decision tree, just without Gemini/Higgsfield named. The WO calling this one "A-1 extended" (vs. flatly new for the other three) turned out to be exactly correct.

Renamed the three colliding ones to **PR-1** (research), **PR-2** (voice), **PR-3** (budget) — a new cross-cutting section, "Providers and budget," parallel to how "Claims — `K-*`" already works. Documented the rename and why, in the section itself, so nobody reading it later wonders why it doesn't match the WO's original R-1/V-1/B-1 text. `A-1` was extended in place as planned; `V-2` (voiceover generation) got one line pointing at PR-2 for which provider actually runs it.

## What shipped

- **`references/providers.yaml`** — dated 2026-09-02, per §4.3. Both Gate-0-supplied prices filled in: Higgsfield $0.02/credit, and `current-vo` resolved to Higgsfield `generate_audio` with the specific voice id from `videos/ectoin-survival-molecule/BRIEF.md` (recorded back in Gate 0).
- **`scripts/provider_call.py`** — `gemini text|image|tts` (dry-run pricing plus a real-call path using only `GEMINI_API_KEY` from the environment and stdlib `urllib`) and `log` (for vidIQ/Higgsfield/HyperFrames spend that happens MCP-side, not through this script). One `cost-log.jsonl` line per paid call, matching §4.3's shape.
- **PR-1 / PR-2 / PR-3** in `decision-policy.md`, each with a `[default]`, both providers named, and an explicit "falls back automatically on anything but `ok`" clause reading the environment probe T6 already wired in.
- **A-1 extended**: diagram/illustration/data-object/kinetic-type generation → Gemini image; photographic generation → Higgsfield; decided per plate in the asset manifest.
- Folded the old untagged "Credit budget (vidIQ)" section into PR-3, which replaces its old graceful degradation (cap-reduced path, no halt) with a hard `HALT: BUDGET-CAP` at 100% of either the $5 or 200-credit cap, warning at 80% — as the WO specified.
- Two more stale-count fixes caught in passing: SKILL.md's Read order item 5 still said "six rules" (T3's earlier fix only caught the mention inside decision-policy.md's own body text, not this one).

## Accept check — what's verified and what isn't

WO's Accept has four parts:

1. **`provider_call.py gemini text --dry-run --in 1000 --out 1000` prints the price the yaml implies** — verified myself, independently of the agent's own report: `est=$0.0045`, matches `1000/1e6*0.75 + 1000/1e6*3.75` by hand.
2. **With the key set: one real text call, one 1K image, one 5-second TTS → three lines in cost-log.jsonl with est_usd** — **not verified; honestly can't be**, `GEMINI_API_KEY` is unset on this machine (confirmed fresh, not assumed). The real-call code path is implemented (stdlib `urllib`, parses `usageMetadata`), but its exact request/response shape is unverified against the live API — flagged as such, not claimed as tested. Same category of gap as T2/T4/T6's HyperFrames-CLI-dependent checks.
3. **A run report showing the Spend table** — the table itself was already built into `assets/run-report.template.md` in T6; nothing new needed here.
4. **A run with `GEMINI_API_KEY` unset shows the fallback provider in the ledger, not an error** — verified for the `provider_call.py` layer myself: calling `gemini text` without `--dry-run` and no key gives a clean one-line message and exit code 3 (distinct from a generic error), not a traceback. The *skill-level* behavior (PR-1/PR-2 actually routing to the fallback provider and writing it to the ledger) needs a real pipeline run to see end-to-end, same blocker as everywhere else — but the piece that's actually new in this task (the script not crashing on a missing key) is genuinely confirmed.

## Independent verification beyond the agent's own report

Re-ran myself rather than trusting the write-up: the dry-run text price, the no-key failure path (with a fresh `echo "${GEMINI_API_KEY:+set}${GEMINI_API_KEY:-unset}"` check first), and the `log` subcommand's `cost-log.jsonl` output (parsed it back with `json.load` to confirm it's valid). Also confirmed the script uses `PR-1`/`A-1`/`PR-2` — not the stale `R-1`/`V-1` — by grepping its own source.

## Judgment calls

- Told the agent to use stdlib-only for the YAML reader per the task's own explicit instruction, even though it flagged that PyYAML is actually importable on this machine — the instruction said "standard library only, full stop," so that's what shipped. Worth knowing if a future task assumes PyYAML is available in this repo: it might be, but nothing here depends on it.
- The agent added `--prompt`/`--prompt-file`/`--text`/`--text-file` flags beyond the WO's literal subcommand spec, since a real (non-dry-run) call needs actual content to send and the spec only described the pricing-relevant flags. Reasonable — flagging it as an addition, not silently absorbed.
