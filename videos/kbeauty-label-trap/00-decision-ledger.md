# Decision ledger — kbeauty-label-trap

Run started: 2026-09-03 · Channel: SeoulHabit · Baseline: reused (fresh)
Credit budget: 200 pre-production, $5.00 total · Spent: 0 · Tags: `long-form`

Format: `[stage/rule] fork → value | data read (threshold) | tool`
Companion gates: `COMPANION-RESOLVED:<name> (skill-tool|file)` or `COMPANION-MISSING:<name>`

## S0.0 Environment
[S0.0] skill → v2.1.0, commit `6d70e4d` == origin HEAD | "pick up latest skill" already satisfied, nothing to pull | git
[S0.0] OUT → `<repo>/videos/kbeauty-label-trap/` | `/mnt/user-data/outputs` tested fresh, ABSENT | bash
[S0.0] CHANNEL → `<repo>/videos/_channel/` | existed, git-tracked, `updated: 2026-09-03` | bash
[S0.0] pin → hyperframes 0.8.26 | `hyperframes --version` (global CLI, bare invocation per repo convention, not npx) → 0.8.26; diverges from prior runs' 0.8.22 pin | bash
[S0.0] provider vidIQ → ok | 2246 credits (1446/2000 renewable + 800 add-on) | vidiq_balance
[S0.0] provider Higgsfield → ok | 2344.95 credits, plan=free; Kimberly voice id confirmed extant | balance, list_voices
[S0.0] provider Gemini → no-key | `GEMINI_API_KEY` unset | env
[PR-1] research provider → does not fire | Gemini status != ok; claim sourcing runs on the 5 operator anchors + PubMed MCP/WebFetch for gaps | —
[PR-2] voice provider → `current-vo` (Higgsfield generate_audio, Kimberly) | Gemini status != ok → stated fallback; also the operator's explicit ask | providers.yaml §tts
[S0.0] project skill → none | confirmed by search; SKILL.md states the repo has none | —
[S0.0] therefore `K-*` applies as the undiluted floor | decision-policy.md §Claims | —
[S0.0] tokens → inherit `ectoin-survival-molecule/assets/tokens/tokens.css` + new `--vermilion` | canonical landscape set; no vermilion token exists; operator confirmed add-token over alias-coral | AskUserQuestion

## Operator decisions (pre-run, via AskUserQuestion — plan-mode gate)
[OPERATOR] runtime clock → measured VO + authored pauses, not padded to 5:00 | 646 words < 675–825 word budget for 300s; expect real length <5:00, logged as deviation | AskUserQuestion
[OPERATOR] hook length → trim to ≤20s, restructure not cut | `[S4/S-6]` hard cap; passport thesis moves to Misconception, also fixing that section's missing wrong-belief sentence | AskUserQuestion
[OPERATOR] vermilion → new `--vermilion` token, not `--coral` alias | honors brief's named accent over cross-channel palette consistency | AskUserQuestion
[OPERATOR] music → reuse-first, audition existing track-pulse.wav beds before generating | `[S4/V-3]` rule; matches skill's reuse-before-generate default | AskUserQuestion

## S0 Baseline
[S0/B-1] baseline → SKIP (fresh) | `videos/_channel/baseline.yaml` stamped `updated: 2026-09-03`, today | file
[S0] retention → `avg_view_pct_long: 43.07, n=2, both private, "not usable"` | every curve/retention comparison this run is `[UNDERPOWERED]`; real comparators are `ectoin-survival-molecule` (340s) and `hyaluronic-acid-vs-filler` (160s) own run reports | baseline.yaml

## S1 Story
[S1/S-1] format → long 16:9, operator-directed | prior long-form art exists but both private → `[UNDERPOWERED]`, "vertical slice first" clause skipped | baseline
[S1/S-2] target length → nominal 300s, measured VO governs | within 4:00-12:00 clamp; operator decision: no padding | AskUserQuestion
[S1/S-3] presenter → moving diagram | 5/6 sections are mechanism explainers | —
[S1/S-4] voice → Kimberly, single narrator | standing channel voice, confirmed resolvable, operator's explicit ask | list_voices
[S1/S-5] spine → 6/6 grounded, 0 [UNGROUNDED] | hook/misconception restructure supplies Misconception's previously-missing wrong-belief sentence | —
[S4/S-6] hook cap → restructured, not cut | 28s script hook > 20s hard cap; moved passport-thesis sentences (28 words) into Misconception | operator decision
[K-1] inventory → 19 claims: nominal 2 · sourced 7 · unsourced 2 (C6, C15) · illustration 4 · editorial 8 | every identifier fetched and read live this run | WebFetch x3, PubMed MCP x2
[K-1] source rejected → niacinamide-specific PMID hit NOT used for C6 | would source a narrow ingredient-specific claim as if it backed a general one — same overreach class the PR#11 ledger flagged | PubMed MCP search
[K-2a] hard-prohibited set → CLEAR | C15 reworded off absolute language; "80%" renders only as Bottle A's quoted label art, never a video assertion; no real named comparator | —
[K-2b] ratio limb → does NOT fire | Mechanism 6 sourced : 1 unsourced (C6); Proof 0:0 editorial-only | computed
[K-3] reword 1 → "'Gentle' is never universal" → "'Gentle' isn't a fixed property" | drops K-2a absolute language, keeps the point | —
[S4/V-1] word budget → 750±10% (675-825) target vs **646 actual**, 29 words under floor | logged deviation, not padded per operator decision | wc
