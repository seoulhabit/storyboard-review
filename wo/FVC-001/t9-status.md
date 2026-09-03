# T9 — Evals, blind A/B, description tuning — Authored, blocked on an org-level feature gate

Commit `66c1940` pushed to `github.com/seoulhabit/claude-skills`.

## The blocker, diagnosed cleanly

`claude plugin eval` — the WO's named tool for this task — returns `plugin eval is currently in early access` when actually run (`claude plugin eval init --bare sample-case`, confirmed directly). This is **not** the OAuth contention that affected some of T8's checks — it's an organization-level feature flag Anthropic controls. Researched via the `claude-code-guide` agent:

- **What Kim needs to do**: request plugin-eval early access for this org from Anthropic (account contact or support), then `claude update` and start a fresh session. If this environment can't reach Anthropic's server-side flags at all (self-hosted/Bedrock/Vertex/custom `ANTHROPIC_BASE_URL`, or telemetry-disabling env vars set), an enablement environment variable from Anthropic may be needed instead, set in the shell profile or `~/.claude/settings.json`. **I did not set anything myself** — that needs Kim's actual enablement credential, not a guess on my part.

## What I built anyway

The full suite, in the tool's **real** file format — not the WO's `evals/evals.json` assumption, which doesn't match how `claude plugin eval` actually reads cases (confirmed via `--help` and the research agent: it wants `<case>/prompt.md` + `<case>/graders/*.md`, directory per case). Seven case directories under `faceless-video-craft/evals/`, one per WO §4.7 case, each with a real prompt and graders written against this skill's actual current rules — read `decision-policy.md` and `SKILL.md`'s mode table/failure-modes list for each one rather than paraphrasing from memory. `evals.json` still exists as a summary manifest, clearly labeled as not what the tool consumes.

Grader schema for the `regex` and `tool_used` types is reasonably solid (confirmed via research). Two spots are honest guesses I flagged individually: the `llm`-type grader in case 5, and a `with-only` field in case 6 modeled on the `--ablation` flag's mention of a "plugin-fired indicator." Both need checking against real docs once access lands.

## Three real findings this produced, independent of the tooling gate

1. **Case 7's true-peak grader is not hypothetical — I actually measured it.** `videos/centella-tiger-grass/renders/centella-tiger-grass_delivery.mp4` already exists (ffmpeg is installed here even though HyperFrames isn't), so I ran `ffmpeg -af ebur128=peak=true` on it directly: **-1.6 dBFS**, which **fails** the WO's own asserted expectation of `≤ -2 dBFS`. This is a real, measured gap between what §4.7 assumes as the passing baseline and what the actual shipped file measures — worth your attention regardless of whether the eval framework ever runs.
2. **Case 4 (non-English) may expose a real policy gap**, not just test one: `decision-policy.md` has no rule for how a requested language propagates to voice selection or the vidIQ keyword-market call. `language` is only listed as an accepted override in prose.
3. **The T3 description trim likely cost real trigger recall.** Fitting the WO's own 500-char cap meant cutting the old v2 description's concrete example phrasings (`'animate this image'`, `'turn this script into a video'`, etc.) in favor of an abstract "Modes:" list. The keywords survived; natural-language surface area didn't. Not something I'm undoing unilaterally (T3's char-cap compliance was correct at the time), but worth weighing now that it's visible.

## Manual trigger-precision analysis (in lieu of the gated tool)

`evals/description-trigger-precision.md`: 11 should-trigger + 11 clean should-not-trigger prompts (meets the WO's ≥10/≥10 minimum) plus one prompt deliberately held out as genuinely ambiguous rather than forced into a bucket. **This is reasoned prediction against the live description text, not an executed test** — I tried to get a real answer via a fresh nested session first (same approach that failed twice in T8 with OAuth errors) and didn't force a third attempt. Do not read this table as satisfying the WO's "trigger precision ≥ 0.9" Accept criterion; it's the best substitute available without either blocker clearing.

## Accept check — honest status

- `benchmark.json` pass rate ≥ v1 on all seven — **not produced**; needs the gated tool.
- Trigger precision ≥ 0.9 on the should-not set — **not measured**; manual prediction only (see above).
- Results in `faceless-video-craft-workspace/` — **not produced**; that directory is `claude plugin eval`'s own output location, never created since the tool never ran.
- `evals/evals.json` committed — **done**, though see the format note above (the real deliverable is the seven case directories; `evals.json` is a manifest, not the tool's input).

## What's still needed to actually close T9

1. Kim gets `claude plugin eval` enabled for the org.
2. Run it against this suite — all 7 cases, with `--ablation` for the with/without comparison, and pointed at `archive/v1-repo-2026-09-01/` for the blind A/B on cases 1 and 3.
3. Decide whether the HyperFrames-dependent cases (1, 2, 4, 7) need running on a different machine that actually has the CLI, since this dev machine doesn't.
