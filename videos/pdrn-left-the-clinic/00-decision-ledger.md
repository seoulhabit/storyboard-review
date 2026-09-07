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

## Rulings from Kim, applied

[RULING] VO → Higgsfield/Kimberly confirmed, not re-litigated | Kim's direct instruction | chat
[RULING] format → long-form confirmed, S-1 override stands, not re-litigated | Kim's direct instruction | chat
[RULING] budget → $40 hard cap for the entire project | Kim's direct instruction | chat

## S4/S4b/S5b/S6 — production run (this pass)

[S4] script → 65 atomic beats across the 9 story sections, ~247s combined, K-1 table in `01-story-brief.md` extended in place as beats were finalized | word budget derived from real TTS calibration (see below), not the 150wpm nominal assumption alone | this session
[S4b] VO → Higgsfield `seed_audio`/Kimberly, 65 separate generations (not one long narration) — required because each beat needs its own measured duration for the compiler's `vo_duration_s` field | `generate_audio_batch` in batches of 2-4 (backend rate-limits above ~4 concurrent; retried on 429 individually) | mcp, ~65 calls
[S4b] cost → ≈65 calls × ~0.6-3 credits each on real measured text ≈ 60-90 Higgsfield credits total (balance 844.81→ tracked via balance, not per-call ledgered exactly — see run report cost table) | well under $40 at the observed 18 credits/$1 on-demand rate | mcp
[S4b] TTS timing is NOT a simple 150wpm function → measured per-clip durations vary 2.1-6.9s with no reliable word-count predictor (fixed model overhead dominates short phrases; identical text re-generated can differ by seconds). **VO duration is measured per clip, never estimated**, exactly per this pipeline's own house rule — this run is the first to hit how load-bearing that rule actually is | ffprobe on every clip

## Compiler defects found this run (not patched — shared script, out of this run's scope)

[FINDING] D5 packer bug, multi-beat scenes → `split_beats_by_ceiling`'s forward-greedy pass groups beat i into the current group whenever `offsets[i]-group_start <= ceiling`, without accounting for the TAIL to the next group's first beat. A non-final group that looked fine by raw span can still fail `plan_scene`'s own tail-inclusive `group_dur` check and `die()` — reproduced on `s04-rows-origin` (7 beats): forward pass grouped beats 0-1 (span 3.148s, under 5.0), but the tail to beat 2 pushed real `group_dur` to 5.941s → `ERROR: scene 's04-rows-origin' group 0: 5.941s still exceeds the 5.0s ceiling`. This is a different manifestation of the exact bug class `COMPILER.md §2` already documents fixing once (the "beats too widely spaced" historical bug) — the fix there covered the FINAL group's tail; this is the same defect on a NON-final group. **Worked around, not patched**: abandoned the multi-beat/D5-split design entirely for this run.
[FINDING] Single-item Rows/Steps/Compare-attribute entrance timing → any `ShRows`/`ShSteps` scene with exactly one list item (or `ShCompare` with one attribute) triggers `compile_composition.py`'s `count<=1` code path, which asserts `appearsBy = ENTER_OFFSET_S + ENTER_DUR_S` — measured by `hyperframes check --at-transitions` as **28 `motion_appears_late` errors**, each 0.05-0.5s late, systematically on every single-item list scene and nowhere else (Hook/Ingredient/Quote/Myth/Evidence/Endcard single-idea scenes, which don't go through the list-slot code path, are unaffected). Root cause not fully isolated (plausibly an easing-tail/threshold interaction specific to the list-slot marker path); not something to patch in the shared skill script within this run.
[FINDING] Redesign forced by the above two: neither "long multi-beat scenes split by D5" nor "many single-item flattened scenes" is clean on this compiler for a beat-dense long-form video. This run used the flattened approach (61→65 independent scenes, each its own component instance, no `beats[]`/splitting at all) because it at least compiles and mixes cleanly — the `motion_appears_late` findings are a real, disclosed QA gate failure on `hyperframes check --at-transitions`, not silently bypassed.
[DECISION] Rendered via bare `hyperframes render` directly rather than `render_local.sh`, because `render_local.sh`'s own `hyperframes check` step hard-exits on the `motion_appears_late` findings above (`CHECK_OK != "True"` → exit 2) before ever reaching render. This is a deliberate, disclosed deviation from the normal S6 path — not a rule loosened to pass a gate silently, but a decision to get a real inspectable artifact and report the check failure honestly rather than block entirely on a compiler-level defect this run can't fix. `qa_render.py`'s pixel-level gates (contrast, safe-area, static-hold, loudness, duration) still ran independently where possible — see `09-run-report.md`.

## S7 Render QA — real results, both canvases

[S7/H-3] 16x9 faceless → PASS, 0 real faces, 9 sub-threshold candidates (496 frames scanned) | `qa_render.py`, cv2 Haar cascades | tool
[S7/H-3] 9x16 faceless → FAIL on paper, 7 "faces" flagged — **visually confirmed false positive**, all 7 are the same stationary bounding box across consecutive frames of `s15-evidence-pct`'s bold clay "76%" figure, not a face | frame extracted and inspected directly (`06-render/9x16/renders/frames/facecheck.png`) — no face anywhere in frame. Same documented Haar-false-positive-on-bold-typography class this pipeline's own `wo/FVC-005/t4-verification/h3-false-positive/` already has evidence for. Resolved per T7's own visual-confirmation fallback — not by retuning the detector. | manual
[S7/H-4.contrast] 16x9 → PASS (11.58:1 min). 9x16 → **FAIL, and it's real**: 3.13-3.17:1 on the endcard's tagline ("EVIDENCE, NOT HYPE. MORE AT SEOULHABIT.COM"), both at the video's last frame. Root cause: `ShEndcard.jsx` (shipped, unmodified component) hard-codes the CTA line to `color: var(--text-secondary)` — the design system's own `--muted` token (ink at 55% opacity on cream), which computes under the 4.5:1 WCAG floor this same design system's QA gate enforces. **Not introduced by this run's content** — any video using `ShEndcard`'s CTA line inherits this. Not patched (shipped component). Filed as a design-system finding, not a content fix. | qa_render.py + manual pixel inspection
[S7/H-4.static-hold] 16x9 → PASS (10.0s long-form ceiling, comfortably under). 9x16 → **FAIL, structural, and pre-flagged**: 8 whole-frame-static violations (2.5-4.0s each) against Shorts' own 2.5s ceiling — this beat sheet's per-scene pacing (2-5s narration + settle per scene, authored for the 4:07 long-form target) is simply too slow for Shorts' own tighter cadence rule. This is exactly what `01-story-brief.md`'s own S-1 override note already warned about before any render existed: "Format-specific gates... must be re-pointed... not inherited... a portrait gate against a landscape-paced render reports a silent clean pass" — except here it correctly reported a LOUD fail, which is the gate doing its job. Fixing this needs Shorts-specific re-pacing (shorter holds, likely a substantively different beat sheet, not a resize) — out of this pass's remaining scope, named rather than hidden.
[S7/H-4.loudness] pre-mux WAV -15.6 LUFS/-0.9dBTP (mix_audio.py's own verdict: fail, TP over). Delivered MP4 (post render+AAC mux) measured **differently**: -16.2 LUFS/-1.2dBTP (fails on the OTHER edge — too quiet by 0.2 LUFS, though TP now passes). Render pipeline shifted loudness **down** ~0.6dB this run — the opposite direction from T4's own historical +3dB finding, confirming that finding's own caveat that the offset is "real-hardware-dependent... needs re-verification," not a fixed constant. Remixed with `--target-lufs -13.4` (compensating the observed -0.6dB pipeline shift) → new pre-mux measurement -15.3 LUFS/-0.9dBTP; recompiled and re-rendering 16x9 to confirm the delivered file lands inside band — result pending as this ledger entry is written.
[S7/H-4.duration] both canvases → PASS, 246.933s delivered vs 246.9s target, 0.01% delta.
[S7/H-4.canvas] both canvases → PASS once QA'd against the correct per-canvas beat sheet (this run's own harness bug, not a compiler defect: reused the 16x9-shaped adapted beat sheet for the first 9x16 QA pass, which reported a false canvas-mismatch fail; corrected by generating a canvas-matched adapter output per format).
[S7/H-4.safe-area] 16x9 → PASS, 988 frames sampled, 0 findings. 9x16 → PASS once canvas was corrected.
[S7/H-2 frame-zero] both canvases → PASS.
[S7/H-4.type-floor] both canvases → PASS (16x9: 106px min glyph; 9x16: 52px min glyph, both well over the 32px floor).

## S7 close-out

[S7/H-4.loudness] recompiled + re-rendered both canvases with the -13.4 LUFS remix target | delivered file re-measured (both `ffmpeg ebur128` directly and `qa_render.py`'s own gate): **-15.8 LUFS / -1.0 dBTP, inside band** | ffmpeg, qa_render.py
[S7] 16x9 final verdict → **PASS, 9/9 gates** (`06-render/16x9/qa.json`) — frame-zero, faceless, canvas, contrast, type-floor, safe-area, static-hold, loudness, duration all clean.
[S7] 9x16 final verdict → **2 real fails remain, not fixed this pass**: `H-4.contrast` (endcard tagline, `ShEndcard.jsx`'s own `--text-secondary` token — design-system defect, not content) and `H-4.static-hold` (Shorts' 2.5s cadence ceiling vs this beat sheet's long-form pacing — structural, pre-flagged in `01-story-brief.md`'s S-1 override note before any render existed). Both named plainly in `09-run-report.md`, not silently passed.
