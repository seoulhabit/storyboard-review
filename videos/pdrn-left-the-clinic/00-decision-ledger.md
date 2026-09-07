# Decision ledger — pdrn-left-the-clinic

Run started: 2026-09-07 · Channel: SeoulHabit · Baseline: reused (fresh,
`updated: 2026-09-03`) · Slug: `pdrn-left-the-clinic` (distinct from the
pre-existing `videos/pdrn-cellular-science/`, older-pipeline shape, untouched)

Format: `[stage/rule] fork → value | data read (threshold) | tool`

## S0.0 Environment
[S0.0] skill → v0.3.0, `claude-skills-current` `master` @ `9c14bb9`, symlink clean | prior drift (stale 0.2.0 shared checkout) resolved outside this run | git, ls -la
[S0.0] OUT → `<repo>/videos/pdrn-left-the-clinic/` | fresh worktree `.claude/worktrees/pdrn-clinic`, branch `session/pdrn-clinic` | bash
[S0.0] CHANNEL → `<repo>/videos/_channel/` | `baseline.yaml` present, `updated: 2026-09-03` | file
[S0.0] pin → hyperframes 0.8.30, bare binary | `~/.nvm/.../bin/hyperframes`, never `npx` | bash
[S0.0] provider HeyGen → reachable, `plan: pro`, 243 premium + 41 add-on credits, `wallet: null` | `get_current_user` | mcp
[S0.0] provider vidIQ → ok, 325 credits (0 renewable / 325 add-on) | `vidiq_balance` | mcp
[S0.0] `videos/_system/MANIFEST.json` → clean, 67/67, 0 mismatches | independent sha256 re-derivation, both before and after this run's changes | python3
[S0.0] project skill → none | `request.yaml project_skill: none` | file

## Claim sourcing — queue staleness caught before it mattered
[S1] queue count check → `videos/_queue.yaml` lists pdrn at "citations: 2, findings: 1" — **stale** | file's own header warns counts are enqueue-time snapshots, not live | file
[S1] real corpus at `cacff81` → 17 findings, 15 verified `F-PASS`, 1 `F-UNCHECKED` (C1, unused), 1 no-verdict (C11, unused) | `content/findings/pdrn.json` read in full | git show, python3
[K-1] inventory → 12 claims: nominal 1 · sourced 8 · editorial 4 (2 of which restate already-sourced findings) · unsourced 0 | every finding id read live this session from the pinned SHA | git show
[K-1] correction applied → brief's draft implied zero topical evidence exists; C7 (PLoS One 2026, PMID 42430369) is a real topical RCT and had to be added, sized correctly (one small industry-linked trial, one site) | direct read of `content/findings/pdrn.json` finding C7 | git show
[K-1] regulatory claim (§3, 3:10–3:50) → sourced, not cut | 7 independently corroborating Korean trade-press outlets, all reporting one National Assembly Health & Welfare Committee MFDS-data disclosure (Rep. Seo Young-seok, Sept 2026); numbers cross-checked identical across all 7 before classing `sourced` | WebSearch x2, WebFetch x1
[K-1] no primary government URL found for the regulatory claim | disclosed explicitly in `01-story-brief.md`'s K-1 table rather than treated as fully primary-sourced | —
[K-2a] hard-prohibited set → CLEAR | no treats/cures, no unsourced safety claim, no unsourced quantity, no absolute language | —
[K-2b] ratio limb → does NOT fire | Mechanism + Proof: 5 sourced, 0 unsourced | computed from K-1 table

## S1 Story — format and runtime forks
[S1/S-1] format → long 16:9 + short 9:16 (both, F-2 single compile), **operator override** | branch 2 would select short (46/48 uploads = 95.8% ≥ 60%); brief fixes long at 4:55 | baseline.yaml, brief §Formats
[S1/S-1] override consequences ledgered per the rule's own 5-item note → (1) named as override, share overridden = 95.8%; (2) every `curve.*`/`retention.*` comparison at S9 marked `[UNDERPOWERED]` — this channel has zero public long-form; (3) safe-area/cadence/canvas gates must be re-pointed to 16:9 at S7, not inherited from the Shorts-tuned defaults; (4) `[S3/P-3]` will generate+score a thumbnail for the long cut, Shorts uses frame 0; (5) the rule's own "prove on a vertical slice first" advice is **not** followed — flagged as an open ruling for Kim, not decided by this run | policy.md S-1
[S1/S-2] target length → 4:55, inside the 4:00–12:00 clamp | brief §5 | —
[S1/S-2] runtime-vs-template contract mismatch → `T6.json chapters_max: 6` caps near 3:00–3:30 at the compiler's own per-scene ceilings (5.0s / 8.0s D5); 4:55 exceeds it | not enforced by any gate today — filed to Design as §A3 of the request doc, not resolved unilaterally | videos/_system/templates/T6.json, COMPILER.md §2
[S1/S-3] presenter → kinetic-type, contingent | matches design system's established use for evidence/definition content; re-open if Design's A1 ruling extends the system with place/object components, since the brief's own cinematography is object/place-driven, not vocabulary-driven | T1–T5 precedent
[S1/S-4] voice → Higgsfield, Kimberly (`674b71b8-1d2e-4087-8567-d1f53c0b9f3c`), `seed_audio`, 2.4 credits/60 words — **H-0 fence override**, not a default path | brief §0 closes this choice; HeyGen `create_speech` HTTP 402 `insufficient_credit` against a separate "api" credit pool, re-confirmed this session via `get_current_user` (`wallet: null`) | brief §0/§4, mcp

## Phase A — Design build spec
[A] gap found → design system (`videos/_system/` and the source Claude Design project, both checked directly) has zero imagery primitives: no photo, plate, illustration, diagram, or camera-move component of any kind | `EXTRACTION.md`, project `readme.md` ("No imagery... typographic by design"), `DesignSync list_files`/`get_file` against `a7945a95-…` directly | file read, DesignSync
[A] request written → `videos/_system/REQUESTS/2026-09-07-imagery-and-longform.md` — A1 imagery ruling (extend vs. decline), A2 five component specs (`ShPlate`, `ShTransform`, `ShPlace`, `ShDiagram`, `ShAnnotate`), A3 the T6 chapter-ceiling question, A4 drift report | this run | Write
[A] pushed to Design → `DesignSync finalize_plan` → `write_files` → `get_file` read back byte-identical | project `a7945a95-da21-4823-8b16-57c6ffa11558` | DesignSync
[A] fallback path named, not silently taken → if Design declines A1, every beat below re-expresses on the nine existing emitters per the readme's own rule ("the video is wrong, not the system") | this ledger's own beat map, below | —

## Typographic beat map (the fallback path, and the working spine either way)

Each story beat mapped to an existing `videos/_system` emitter — proves the
brief is buildable today on the current system, even before Design answers
A1, and gives Design a real alternative to judge the new components against.

| Beat (brief §3) | Emitter | Notes |
|---|---|---|
| 0:00–0:30 hook — bottle/DNA | `ShHook` | Accent word: "DNA" or "top". No bottle/DNA visual without A1; hook line carries the whole beat typographically. |
| 0:30–1:05 clinic authority | `ShIngredient` | Name: "PDRN", INCI "Sodium DNA", function line drawn from C13/C8. |
| 1:05–1:45 leaves the clinic | `ShRows` | Rows: `Clinic → Injection` / `Shelf → Serum`, active on the shelf row. |
| 1:45–2:25 salmon vs plant split | `ShCompare` | `a`: "Salmon DNA", `b`: "Plant/algae DNA", one attribute row: source, favours neither (per C13/C14 — no head-to-head exists). |
| 2:25–3:10 evidence boundary | `ShEvidence` (anchor) | Figure: "0" (leave-on trials in C8's review), caption from C8's own quote, source `Cureus · 2026`. Second `ShEvidence` for C7's real trial if the D5 split budget allows: figure "31", caption "one small trial, one site". |
| 3:10–3:50 marketing vs regulator | `ShMyth` | Claim (struck): the animated-DNA marketing promise; correction: "81 of 106 MFDS violations were this exact overreach." |
| 3:50–4:30 four questions | `ShSteps` | 4 steps: name / source / concentration / topical-vs-injectable, per the Application section. |
| 4:30–4:55 verdict + 3 labels | `ShQuote` then `ShRows` (3 rows: WHAT WE KNOW / DON'T / CHECK) then `ShEndcard` (anchor) | Quote: the brief's own closing line, attribution `SEOULHABIT.COM`. |

Chapter count if built exactly this way: **8** against T6's declared
`chapters_max: 6` — the runtime/template mismatch named at `[S1/S-2]` above,
concretely.

## Open — not decided by this run, flagged for Kim

[OPEN] H-0 fence vs. brief's VO choice → recommend logging as an explicit operator override + a proposed fence amendment to `policy-change-proposals.md`, not silently normalizing Higgsfield as a permitted provider | ruling needed
[OPEN] S-1 format override, vertical-slice-first not followed → recommend Design's A3 answer and Kim's format call be resolved together, since both bear on whether 4:55/long is even the right target | ruling needed
[OPEN] budget → `providers.yaml budget.per_run_cap: null`; the WO's specified 8-call vidIQ cap is implemented nowhere. Zero vidIQ/HeyGen spend so far this run — will bite at S2/S3 if this run resumes past Phase A/B | ruling needed
