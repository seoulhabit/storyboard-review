# WO-FVC-004 — HeyGen is the production engine: `makemeavideo` (was: `faceless-video-craft` v3.0.0)
**Status:** DRAFT — awaiting Gate 0 answers + Kim's `approved`
**Ruling that opens this WO (2026-09-05):** *"Everything moves to HeyGen."* Confirmed scope: HeyGen renders too; the local HyperFrames lane is retired. Shorts path: the spike decides.
**Supersedes:** WO-FVC-002 (HeyGen for voice/audio only — its `HG-0` fence is void) and WO-FVC-003 (first story run on HyperFrames; its §0.3 "keep current-vo" is void). What both WOs got right is carried in §2 and named per task. Neither WO-FVC-002 nor WO-FVC-003 exists on this machine, in this repo, or in `claude-skills` — see §8.1.
**Predecessor still in force:** WO-FVC-001 (closed, v2.1.0) — its policy layer is what survives.
**Target on close:** `makemeavideo` **1.0.0** (superseded from `faceless-video-craft` 3.0.0 — see §7).
**Kickoff line (once approved):** `Read docs/wo/WO-FVC-004.md in this repo and work from it, §7 first. The skill under construction is claude-skills/makemeavideo/, seeded from makemeavideo-src-0.1.0.zip. faceless-video-craft is frozen and read-only.`

---

## §0 — What changes, what doesn't, and the one thing that must be proven first

### 0.1 The skill's shape survives; the engine underneath it is swapped

```
S0 Baseline ──► S1 Story ──► S2 Topic gate ──► S3 Packaging ──► S4 Script (+VO pre-flight)
   unchanged      unchanged     unchanged         unchanged        script per K-1..K-5;
   (vidIQ)        (K-1 table)   (vidIQ)           (vidIQ)          create_speech measures
                                                                    per-scene duration
                                                                          │
S9 Readout ◄── S8 Envelope ◄── S7 Render QA ◄── S6 Build ◄──────── S5 Build spec
 unchanged     unchanged;      download MP4 →    create_video_agent  beat sheet → scene-by-scene
 + HeyGen      chapters from   frames → pixel    (chat mode, "no     prompt: type / visual /
 credit line   scene bounds    gates → fix via   avatar", style_id,  VO / duration + style
                               chat, capped      brand tokens)       block + attachments
```

**Unchanged (the value):** vidIQ data layer, `<CHANNEL>/baseline.yaml`, S1 brief with the `[K-1]` claim table and the `K-1..K-5` floor, S2 topic gate, S3 title/thumbnail scoring, S8 envelope, S9 learning loop and its class table, the Decision Ledger, `00-environment.md` / `09-run-report.md` bookends, **two human touchpoints**, and — carried from WO-003 — `request.yaml`, the wrappers (`/produce`, `/improve`, `/video-package`, `/video-readout`), rule `F-2` (one story, both formats) and the `/improve` class→rebuild chain.

**Replaced:** S5 "beat sheet → HTML composition" becomes S5 "beat sheet → **build spec**" (the scene-by-scene Video Agent prompt). S6 "composition + `check`" becomes S6 "**one Video Agent session in chat mode**". S7 keeps every *pixel* gate (contrast, safe-area, frame-0 hook, `K-4` claims read off frames, loudness/true-peak) and drops every *engine* gate (`check`, `sweep_static`, motion sidecars, box-sizing). Fixes are scene regenerations through `send_video_agent_message`, capped.

**Retired from the pipeline:** HyperFrames CLI/MCP, `hyperframes-engine.md`, `/hyperframes-animation`, `/hyperframes-keyframes`, `lint_composition.py`, `beats_to_composition.py`, composition-level rules `A-5`–`A-10`, `R-1`/`R-1b`, the `[S7]` frozen-render class of failure, Higgsfield as image role (Video Agent supplies motion graphics / AI images / stock; project plates become **attachments**), `current-vo`, `gemini-tts`, and the `PR-2` listening test (closed by supersession). Gemini stays for **research only** (`PR-1`), per the Sep 2 ruling that it is available as a provider option.

For the record, not for relitigation: HyperFrames is HeyGen's own engine and, per HeyGen's July 2026 notes, now runs *inside* Video Agent. The ruling retires the **local video-as-code lane** and its toolchain; whatever Video Agent does internally is its business.

### 0.2 The one thing that must be proven before any rewrite: T0

Everything above assumes four things HeyGen's docs say but no run of ours has measured:

1. Video Agent produces a **faceless** video when told "no avatar, voice-over only" — and does not sneak a person in via stock footage.
2. It **follows a scene-by-scene script** closely enough that the beat sheet remains the driver (claims land in their scene; durations roughly hold).
3. **Per-scene timing is retrievable** after render (for chapters, `K-4` frame mapping, and the retention diagnosis) — from `get_video_scenes`, from a caption sidecar, or by scene-cut detection on the MP4.
4. **Shorts**: `create_ai_clipping` on the long yields at least one clip that passes the Shorts gates (single claim, frame-0 hook, 9:16 safe-area) — or it doesn't, and F-2's derivative is a second portrait session.

T0 measures all four on the already-sourced centella brief for a bounded credit spend, with the pass/fail rule for each written **before** the session is created (§3 T0). If (1) fails, this WO halts at Gate 0 and the ruling comes back to Kim with the evidence — it does not get quietly worked around with an avatar.

**§8.2 amends which artifact "the centella brief" names** — the run at `outputs/2026-09-01-how-to-repair-skin-barrier/`, not `videos/centella-tiger-grass/`.

### 0.3 Dependency — repo state (carried from WO-003 §0.4)

`storyboard-review` reconciliation is open. T1 works on a reconciled master **or** a fresh branch `fvc-004/<slug>` from a named known-good commit, recorded in `00-environment.md`. This WO does not reconcile the repo.

**§8.3 amends this: the reconciliation closed on 2026-09-04**, before this WO was drafted. See §8.3 for the evidence; T1 works directly on master (or a worktree of it), no separate reconciliation step needed.

---

## §1 — Gate 0: answer slots

| # | Slot | Kim's answer | Default |
|---|---|---|---|
| G0-1 | **The story** for the first run — paste or path (topic, question, script, outline, research note, URL). | | *(none — required)* |
| G0-2 | **Channel + repo** — YouTube handle; git repo holding `videos/_channel/`. | | `storyboard-review` |
| G0-3 | **HeyGen plan + credits** — plan name, credits remaining, **$/credit** (carried from WO-002 G0; `get_current_user` fills remaining credits, the price needs your plan page). | | *(none — required; it is the `PR-3` budget unit now)* |
| G0-4 | **Spike budget** — max HeyGen credits T0 may burn. | | 60 |
| G0-5 | **Format for the first run** — `long` / `short` / `both`. | | `both` (F-2; Shorts path per T0 finding 4) |
| G0-6 | **Brand tokens** — 3 hex colours + font family for the channel, or "read from project skill", or "neutral". | | read from project skill if one is in play, else neutral (navy / off-white / one accent, Inter) |
| G0-7 | **Project skill in play?** name or `none`. | | `none` (`K-1..K-5` still apply) |
| G0-8 | **Publish surface** — `manual` (upload private in Studio, paste envelope) or `api`. | | `manual` (Publish Desk 80/20 ruling) |
| G0-9 | **`/improve` dry-run target** — video id. | | `d6DPiORuPO4` (centella; class already measured: distribution-failure) |
| G0-10 | **Confirm the command name.** | | `/makemeavideo` |

Two picks are made **once, at setup, by you** and then never asked again (T2): the narrator voice (from three `design_voice` candidates) and the Video Agent style (from T0's shortlist). They are channel-level settings, not per-run decisions — the "no open questions" rule is about runs.

**§8.4 reports the pre-filled state of these slots** as of this WO's landing — see `docs/wo/GATE0-FVC-004.md`, the companion answer sheet.

---

## §2 — Standing rulings (verbatim; nothing here may loosen)

1. **Two human touchpoints per run:** the story in; the publish click out. Never "which do you prefer." Missing input with no default → halt with a named `BLOCKER-*`.
2. **`K-1..K-5` is a floor.** Unsourced safety claim, unsourced number, *treats / prevents / cures* never render. `[K-4]` reads the finished frames — engine-agnostic, so it survives unchanged.
3. **Faceless means no human face on screen.** Enforced on pixels (`H-3`, T3), not by trusting the prompt. A project skill may allow a specific exception; absence of a project skill is not permission.
4. **Frame zero is the hook and, for Shorts, the thumbnail** (`[S6/A-3]` carried as `[S7/H-2]`). Never blank, never mid-fade, never a lone title.
5. **Every fork is a written rule with data, a threshold, a default and a ledger line.** The engine changing does not change how decisions are made.
6. **Budget is enforced in HeyGen credits** (`PR-3` re-denominated). Credits before and after every session are ledgered from `get_current_user`.
7. **Publish = manual upload + envelope paste** unless G0-8 says `api`, and then every metadata write asks consent individually.
8. **Scope never widens.** New findings → §5 or a new WO.
9. **Two-machine parity.** The HeyGen MCP connector is per-machine (OAuth). T1 and T9 verify both. **§8.5 records that on this machine, that connection does not exist and OAuth cannot run non-interactively.**
10. **Lane docs are Google Docs;** WO doc-in-place; supersessions as dated §-sections appended.
11. **No auto-retry past a cap; no loosening a rule to pass a gate.** A halt goes to Kim with its three lines.

---

## §3 — Tasks

Tiers: data pulls / MCP calls / CRUD on Sonnet/Med; policy authoring and frame judgement on Opus/High. Times exclude HeyGen render waits.

### T0 — Spike: prove the four assumptions · Sonnet/Med, frame review on **Opus/High** · ~2 h · ≤ G0-4 credits

Pass/fail rules are fixed here, before the first call. Code records each finding with its evidence in `wo/FVC-004/spike.md`.

**Not run in this session — see §6 Gate 0.** The HeyGen MCP is not connected on this machine (confirmed absent from `.claude.json`, the connector registry, and this session's tool list). This task is fully specified and ready; it requires an interactive session to complete HeyGen OAuth first.

1. Connect `https://mcp.heygen.com/mcp/v1/` (OAuth) on the machine running the spike. `get_current_user` → credits **before**.
2. `list_video_agent_styles` → shortlist styles whose description does not imply a presenter; record ids and tags. **Finding 0:** shortlist of ≥ 1 style, or "no avatar-free style listed; relying on prompt only".
3. Build the spike prompt from the centella run's existing `03-beat-sheet.json` and `01-story-brief.md` §Sourcing, by hand this once (T4 automates it): the scene-by-scene block (Scene N: type · Visual · VO · Duration), a style block (G0-6 tokens, "no avatar, voice-over only", motion graphics for mechanism scenes, stock only for establishing shots, no people), and the pinned duration/aspect from the original run. **§8.2: this is `outputs/2026-09-01-how-to-repair-skin-barrier/`Short, 9:16, 45.28 s, 8 scenes — not the 71–72 s figure attached to `videos/centella-tiger-grass` in earlier drafts.**
4. `create_video_agent` in **chat** mode. Poll `get_video_agent_session` to completion. Ledger `session_id`, `video_id`, wall time.
5. `get_video` → download the MP4. Extract frame 0, one settle frame per scene, last frame (`extract_frames.sh` — it already takes an MP4).
6. **Finding 1 — faceless:** face detection on every extracted frame (OpenCV Haar or equivalent, ≥ 60 px face box). PASS = zero faces. FAIL = any face → try **one** `send_video_agent_message` ("remove all people; motion graphics only") and re-measure. Still failing → `BLOCKER-FACELESS-UNACHIEVABLE`, WO halts at Gate 0.
7. **Finding 2 — script fidelity:** for each scene in the prompt, does the rendered scene carry that scene's VO text (via `get_video_scenes` `script`, or by reading the caption sidecar / transcript) and its named claim? PASS = ≥ 80 % of scenes in order with their claim; duration drift ≤ 30 % per scene. FAIL → note whether the drift is in order (re-promptable) or in content (beat sheet not honoured) — the latter means S5/S6 become "prompt then accept", and T3 must say so.
8. **Finding 3 — timing:** does `get_video_scenes` return per-scene start/duration? If not, does a caption/transcript sidecar carry timestamps? If not, does `ffmpeg` scene-cut detection recover the boundaries within ±1 s? Record which of the three works; that is the chapters + `K-4` mapping source for T3.
9. **Finding 4 — Shorts path:** `create_ai_clipping` on the spike output (or, if the spike is already 9:16, on the centella *long* if one exists — else run one extra 16:9 session only if G0-4 allows). Inspect every clip against: single claim, frame-0 hook present, 9:16 safe-area, no face, 15–60 s. **PASS = ≥ 1 clip meets all** → F-2 derivative = clipping (`F-2a`). FAIL → F-2 derivative = second portrait session (`F-2b`). This is the decision Kim delegated to the spike; Code writes it, with the clip evidence, and does not re-open it.
10. `get_current_user` → credits **after**. Ledger the delta per call.
11. Gate 0 evidence pack: `spike.md` with Findings 0–4, the frames, the credit ledger, and the **style shortlist + three `design_voice` candidates** for T2.

**Acceptance:** all four findings written with their evidence; Finding 1 = PASS; spend ≤ G0-4. Anything else halts here.

**Prior art `T0` should read before running (§8.5):** `wo/FVC-001/gate-0-notes.md` and `videos/ectoin-survival-molecule/BRIEF.md:66-72` record that HeyGen/`hyperframes tts` sign-in was **already found unavailable from an automation context** during WO-FVC-001's own Gate 0 — which is why `current-vo` (Higgsfield) was chosen instead. This WO's entire premise depends on the *remote MCP's* OAuth succeeding where that local sign-in failed; that is untested, and the spike should record whether it does before spending credits on anything else.

### T1 — Setup, both machines · Sonnet/Med · ~40 min

1. HeyGen MCP connected and `get_current_user` returning on **both** machines. **Not completed here (§6).**
2. `references/providers.yaml`: new `heygen` provider with roles `video_agent`, `tts` (`create_speech`), `audio` (`search_audio_sounds`), `clipping`, `translation` (stub); rates in credits with `as_of` and G0-3's $/credit; `budget` block re-denominated. Higgsfield rows marked `retired: 2026-09-05 (WO-FVC-004)`; `gemini` keeps `research` only. **Done — see the shipped `makemeavideo/references/providers.yaml`.**
3. S0.0 probe rewritten: HeyGen (`get_current_user` → credits), vidIQ, Gemini (research). HyperFrames row **removed**, not left as `not installed`. **Done in `runbook.md` §S0.0.**
4. Repo per §0.3; `00-environment.md` records branch/commit and the connector's account email. **This session: branch `session/fvc-004` off master `7fc21c6`, isolated worktree per repo convention.**
5. Skill resolves to the target version on both machines *before* T9 touches it. **Done for one machine this session (§7 T1); the second machine and the HeyGen connector both remain for whoever runs T0.**

### T2 — One-time channel picks · Kim + Sonnet/Med · ~30 min · `TOUCHPOINT-SETUP`

The only setup-time human choices, made once and written to `<CHANNEL>/baseline.yaml` under `heygen:`:

- **Voice:** T0's three `design_voice` candidates (each a short sample via `create_speech`, same 20-word test line, ~1 credit each). Kim picks one → `heygen.voice_id`. `list_voices` confirms `engine=starfish` so TTS and Video Agent share it.
- **Style:** from T0's shortlist → `heygen.style_id`.
- **Brand glossary:** `create_brand_glossary` "<channel> INCI" with pronunciations for the ingredient/INCI terms already in R01/R02 (centella, niacinamide, etc. — Code seeds from the ingredient files in the repo). → `heygen.brand_glossary_id`. Carried from WO-002 T3/T4.
- **Brand tokens:** G0-6 → `heygen.tokens` (hex + font), used verbatim in every style block.

Ledger: `TOUCHPOINT-SETUP voice=<id> style=<id> glossary=<id>`. After this, no run asks for any of them. **Blocked on T0 (needs the style shortlist and voice candidates it produces).**

### T3 — Policy rewrite · **Opus/High** · ~3 h

`references/decision-policy.md` → **shipped as `makemeavideo/references/policy.md`** per §7. Retire §A composition rules and §R engine rules; add **§H (HeyGen build & QA)**. Each rule in the house shape (reads / rule / default / ledger). Gist to encode:

| Rule | What it decides |
|---|---|
| `H-0` **Tool fence** (replaces WO-002 `HG-0`) | Permitted: `create_video_agent` (chat mode only), `get_video_agent_session`, `send_video_agent_message`, `stop_video_agent_session`, `get_video`, `get_video_scenes`, `list_video_agent_styles`, `create_speech`, `list_voices`, `design_voice` (T2 only), `search_audio_sounds`, brand glossary tools, `create_ai_clipping`/`get_ai_clipping` (if F-2a), `create_asset_upload`/`complete_asset_upload` (attachments), `get_current_user`. **Forbidden in a run:** every avatar tool, `create_video` (avatar/image lipsync), templates, lipsync, filler-word removal, `delete_*`, batches (until a scale WO), `create_video_translation` (stub, §5). |
| `H-1` **Build spec shape** | The prompt is generated, never free-typed: header (format, aspect, target length, "no avatar — voice-over only", "no people in stock footage"), style block (tokens verbatim, media-type matrix per scene type: mechanism/proof → motion graphics; application → AI image or stock-without-people; hook/end → motion graphics), one `Scene N` block per beat with Visual / VO (script verbatim) / Duration from S4's `create_speech` measurement, attachments list. Ledger the prompt's hash. |
| `H-2` **Frame zero** | carried `[S6/A-3]`: hook visible, not blank/mid-fade; Shorts thumbnail = frame 0; long thumbnail still from `[S3/P-3]`. |
| `H-3` **Faceless on pixels** | face detection on every extracted frame; any face → regenerate that scene (`H-5` cap); still failing → `BLOCKER-FACE`. |
| `H-4` **Pixel gates carried** | 4.5:1 contrast on text pixels, per-format safe-area zones, type floor by pixel height, static-hold detector (no scene frozen > policy seconds), `K-4` claims on frames, ebur128 loudness band + true-peak ≤ −1 dBTP, delivered duration within `S-2` tolerance. |
| `H-5` **Fix loop cap** | per failing scene: one `send_video_agent_message` naming the exact defect and the scene number, re-download, re-gate. Cap **2 per scene, 4 per run**, then `BLOCKER-QA:<scene>:<gate>`. Never a whole-video regenerate to chase one scene. |
| `H-6` **Timing source** | from T0 Finding 3, in the order that worked; chapters and the retention diagnosis map read it. |
| `H-7` **Credits** | `get_current_user` before/after every session and clipping job; `PR-3` cap in credits; the F-2 derivative halts on `BLOCKER-BUDGET` if the long consumed it. |
| `F-2` (carried) | `F-2a` clipping or `F-2b` second portrait session — **fixed by T0 Finding 4**, written as a constant not a fork. Under `F-2a`, every clip runs the full `H-2..H-4` gate set and must carry a single `[K-1]`-sourced claim; clips that fail are dropped, not fixed. Under `F-2b`, the derivative inherits the brief and claim table (WO-003 T4 text). |
| `I-1` (carried) | `/improve` chain: class → stages. Retention → S5–S7 with the rebuild done by **re-prompting the named scenes in a new session** seeded with the original build spec; CTR → S3+S8; distribution → S2 seed + frame-0 redesign then S5–S7; working → halt. New slug `-r2`. |

Also: `S-1` and `S-2` re-pointed (aspect ratio and duration now go into the build spec, and Video Agent treats duration as soft — `H-4` measures what came back); `learning-loop.md` adds the HeyGen credit line to the readout and reads scene timing via `H-6`; `restored-v1-rules.md` keeps the four pixel rules and marks the four engine rules retired with the WO id. **§8.6 amends this last clause — see below.**

**Acceptance:** no rule in the policy references `check`, `seek`, GSAP, `#root`, `.motion.json` or Higgsfield; every §H rule has all four fields; the retire list is explicit.

**§8.6 — this WO's own text is inconsistent about `A-6`/`A-7`/`R-2`/`R-3`.** §3 T3 above says `restored-v1-rules.md` "keeps the four pixel rules"; the shipped `H-4` (policy.md) instead says H-4 itself "carries" them. `restored-v1-rules.md` is not shipped in the `makemeavideo` scaffold, so those four rules cannot be preserved by reference — they exist nowhere on disk if left as citations. **Resolution recorded in `wo/FVC-004/t3-status.md`: fold their measured numbers and doctrine inline into `H-4`'s own text, keep the rule ids as provenance tags on ledger lines, do not carry them as separate rule bodies.**

### T4 — Runbook + scripts + front door · Sonnet/Med · ~3 h

- `pipeline-runbook.md` rewritten S4–S7 with exact tool calls, poll cadence, artifacts, gates. **Shipped as `makemeavideo/references/runbook.md`.**
- `scripts/beats_to_build_spec.py` — `03-beat-sheet.json` + brief + tokens → `05-build-spec.md` (`H-1` shape). Replaces `beats_to_composition.py`. **Written this session — see `wo/FVC-004/t4-status.md`.**
- `scripts/qa_render.py` — MP4 in → frames out + a JSON gate envelope (`H-2..H-4`), same envelope shape the run report reads today. Uses `extract_frames.sh`; adds face detection, static-hold, duration check. **Written this session, orchestrating five `catalog/tooling/` gates by path plus new text-region detection for contrast/type-floor and a new face-detection gate — see `wo/FVC-004/t4-status.md`.**
- `scripts/provider_call.py` — HeyGen branch with credit before/after. **Written this session.**
- `scripts/validate_request.py`, `assets/request.template.yaml` (carried from WO-003 T2; `vo_provider` field dropped — there is one engine now; `attachments:` list added). **Shipped in the 0.1.0 scaffold, tested this session.**
- Wrappers `/produce`, `/improve`, `/video-package`, `/video-readout` (carried from WO-003 T3; `/video-render` becomes `/video-build` = S5–S7 on an existing beat sheet). **§7 supersedes this — one command, `/makemeavideo`, with sub-commands. Not five slash entries.**
- `tests/run.sh` green with fixtures for request validation and the QA envelope. **Written this session.**

### T5 — First story run · Sonnet/Med S0–S4, S8 · **Opus/High S5–S7** · ~3 h + render waits

`/produce <slug>` on G0-1. **Not run this session (§6) — blocked on G0-1 and the HeyGen connection.**

### T6 — Shorts per T0 · Sonnet/Med · ~1 h + waits

`F-2a` or `F-2b` exactly as T0 fixed it. **Not run — blocked on T0.**

### T7 — `/improve` dry run · Sonnet/Med, Opus/High on the class call · ~1 h

`/improve <G0-9>`. **Not run — blocked on T0/T5.**

### T8 — Publish handoff + readout schedule · Sonnet/Med · ~20 min · `TOUCHPOINT-PUBLISH`

**Not run — blocked on T5.**

### T9 — Skill release 1.0.0 · Sonnet/Med · ~1.5 h

Per §7's retarget. **Not run this session** — the scaffold is 0.1.0 and this session's T3/T4 work advances it, but a 1.0.0 release needs T0's findings folded in (the four `[SPIKE:n]` markers) and both machines' HeyGen connection verified (§2 r9). See `wo/FVC-004/t4-status.md` for exactly what shipped and what remains.

### T10 — Handback · Sonnet/Med · ~30 min

`wo/FVC-004/HANDBACK.md` per `/handback`: attestation, every halt and Kim's decision, deploy traps (per-machine OAuth, the credit price used, the repo branch), the §5 list, and the readout dates as next action. **This session's handback covers T1(partial)/T3/T4 only — see `wo/FVC-004/HANDBACK.md`.**

---

## §4 — Specs

### 4.1 `request.yaml` (carried, amended)

```yaml
mode: new                    # new | improve
slug: niacinamide-barrier
story: story.md               # required for new
video_id: null                # required for improve
format: both                  # long | short | both
language: en
project_skill: none
attachments: []                # optional: images/PDFs uploaded via create_asset_upload and referenced in the build spec
overrides: {}                  # target_length_s, style_id, voice_id — each ledgered as an operator override
```

### 4.2 `05-build-spec.md` — the generated Video Agent prompt (`H-1`)

```
FORMAT: long 16:9 · target 6:10 · no avatar — voice-over only · no people in any footage
STYLE: colours #0B1F3A #F6F3EE #E4572E · font Inter · minimal clean motion graphics ·
       mechanism/proof scenes = motion graphics · application scenes = AI image or stock without people ·
       hook and end = motion graphics · fade-through transitions · captions on
VOICE: <heygen.voice_id> · glossary <heygen.brand_glossary_id>
ATTACHMENTS: plates/01.png "use as B-roll in Scene 4" · sources/EN-01.pdf "reference for the numbers in Scene 5"
Scene 1: Hook (Motion Graphics)      Visual: … VO: "…" Duration: 4s
Scene 2: Mechanism (Motion Graphics) Visual: … VO: "…" [K-1 #3] Duration: 12s
…
Scene N: End card (Motion Graphics)  Visual: channel mark, next-video pointer Duration: 4s
```

`[K-1 #n]` markers stay in the spec file for `K-4`; they are stripped from the VO text sent to HeyGen.

### 4.3 Ledger lines added

`[S6/H-1] spec=<sha> session=<id> style=<id> voice=<id>` · `[S7/H-3] faces=0 frames=<n>` · `[S7/H-5] regen scene=<n> gate=<g> attempt=<k>/2` · `[S7/H-7] credits before=<a> after=<b> delta=<d>` · `[S1/F-2a] clips_kept=<n>/<m>` or `[S1/F-2b] derivative-of=<slug>` · `BLOCKER-FACELESS-UNACHIEVABLE` · `BLOCKER-FACE` · `BLOCKER-QA:<scene>:<gate>` · `TOUCHPOINT-SETUP` · `TOUCHPOINT-PUBLISH`

### 4.4 `09-run-report.md` rows added

`HeyGen session(s)`, `Regenerations used (n/4)`, `Credits (before/after/delta, $ at G0-3 rate)`, `Shorts path (F-2a/F-2b)`, `Timing source (H-6)`.

---

## §5 — Does NOT close

- **Video translation derivatives** — `H-0` stubs `create_video_translation`; a language WO decides when and how (closes the 2.1.0 T9 language gap only when written).
- **Batches / scale** — one session per run until a scale WO.
- **`storyboard-review` reconciliation** — §8.3 corrects this: closed 2026-09-04, not open.
- **Publish Desk API path** — G0-8 `api` allowed per-write; not built out.
- **TikTok and 1:1** — not produced.
- **`seoulhabit-video-3d` trim** (Aug 29 open ruling) — still open; no `videos/seoulhabit-video-3d/` directory exists on disk (it is referenced only from other projects' briefs), which is likely why it has stayed open this long.
- **HyperFrames-inside-Video-Agent** — not evaluated; not a fallback (ruling).
- **Captions** — `youtube-delivery.md` requires shipped `.srt`/`.vtt`; no stage in the shipped scaffold produces or gates them, and `catalog/tooling/check-captions.py` sits unwired. New finding this session, not in original WO scope — flagged here per ruling 8.
- **Closed by supersession, for the record:** WO-002 `HG-0` fence; WO-002 Gate 0 questions 2 and 3; WO-003 §0.3 sequencing; `PR-2` listening test; Higgsfield image role.

---

## §6 — Gate status

| Gate | Condition | Status |
|---|---|---|
| Gate 0 | §1 slots filled; **T0 Findings 0–4 written, Finding 1 = PASS, spend ≤ G0-4**; Kim writes `approved` | ☐ **BLOCKED — HeyGen MCP not connected on this machine; G0-1/G0-3/G0-6 unanswered. See `docs/wo/GATE0-FVC-004.md`.** |
| Gate 1 (mid) | T1–T4 status files; T3 acceptance (no engine references left); slash list on both machines | ☐ **T3/T4 done this session on one machine; T1's HeyGen probe and second-machine parity remain.** |
| Gate 2 (close) | T5 acceptance for every slug; T6 per T0; T7 dry run written up; T8 halted at `TOUCHPOINT-PUBLISH`; T9 both machines on 1.0.0; T10 HANDBACK.md | ☐ |

Kim's close signal: `close` on the handback. The 48 h readout runs after close via `/video-readout`.

---

## §7 — Supersession, 2026-09-05 (same day): the target is a NEW skill, `makemeavideo`

**Ruling:** "Start with a new skill for this, call it MakeMeaVideo — multiple issues with the past skill."

What changes in this WO, item by item. Everything not listed stands as written above.

| Where | Was | Now |
|---|---|---|
| Header — target | `faceless-video-craft` 3.0.0 | **`makemeavideo` 1.0.0** (scaffold 0.1.0 delivered with this section; T9 releases 1.0.0) |
| Header — kickoff line | as above | `Read docs/wo/WO-FVC-004.md in this repo and work from it, §7 first. The skill under construction is claude-skills/makemeavideo/, seeded from makemeavideo-src-0.1.0.zip. faceless-video-craft is frozen and read-only.` |
| §0.1 "Retired" | rules/scripts retired *inside* the skill | `faceless-video-craft` **frozen at 2.1.0** — not edited, not deleted, not installed alongside on the two machines (so the drift that hurt v2 cannot recur). Its engine-free parts are already ported verbatim into `makemeavideo/references/policy.md`, `learning-loop.md`, `youtube-delivery.md`, `extract_frames.sh`, `validate_beat_sheet.py`, and the beat-sheet/ledger/report templates — same rule ids. **§8.7: this machine's `faceless-video-craft` working tree is currently mid-edit to 2.2.0 by another session — not touched by this WO; see §8.7.** |
| §1 Gate 0 | slots G0-1..G0-9 | unchanged; **plus G0-10: confirm the command name** `/makemeavideo` (default) |
| §2 ruling 9 | two-machine parity of the skill | unchanged, and adds: `faceless-video-craft` must **not** resolve as an installed skill on either machine after T9 (archived in the repo only) |
| T1 step 5 | skill resolves to 2.1.0 as baseline | → both machines resolve `makemeavideo` 0.1.0 from the repo symlink; **no** claude.ai library install (§Version and drift check in the new SKILL.md). **§8.8: on this machine, `makemeavideo` is currently installed as an enabled claude.ai library skill — the inverse of this rule. See §8.8.** |
| T3 | rewrite `decision-policy.md` in place | → **finish `makemeavideo/references/policy.md`**: (a) strip every retired-engine cross-reference from the carried block (`grep -n -i "hyperframes\|seek\|gsap\|check\b\|composition\|motion.json"` → 22 hits at scaffold time) replacing each with the `H-*` id of the same purpose; (b) re-denominate `PR-*` in HeyGen credits; (c) strip the composition-era lines from `youtube-delivery.md` (21, 89, 125, 135–143 at scaffold time); (d) write T0's findings into `H-6`, `F-2` as constants and remove the `[SPIKE:n]` markers. Acceptance unchanged. |
| T4 | scripts into the old skill | → into `makemeavideo/scripts/`: `qa_render.py`, `beats_to_build_spec.py`; `validate_request.py` ships in 0.1.0 (tested); wrappers become the **sub-commands of one command** (`/makemeavideo`, `/makemeavideo improve|build|package|readout`) — one entry in the slash list, not five. |
| T9 "Skill release 3.0.0" | archive 2.1.0 inside the skill, rewrite SKILL.md | → **release `makemeavideo` 1.0.0**: CHANGELOG from 0.1.0 forward; evals authored fresh in the tool's real format (carry the *ideas* of 03/05/06/07 and 08/09/10 from §3 T9, not the files); `faceless-video-craft` moved to `claude-skills/archive/faceless-video-craft-2.1.0/` with a NOTE naming this WO; description optimised with `skill-creator`'s `improve_description.py` before release. |
| §5 | — | adds: **`faceless-video-craft` trim / cleanup** — closed by supersession; it is archived whole. **`seoulhabit-video-3d`** — its *content* rules (brand palette, product truth) are a candidate project skill for `makemeavideo`; a separate one-task WO decides. |
| §6 Gate 2 | "T9 both machines on 3.0.0" | → "both machines resolve `makemeavideo` 1.0.0; neither resolves `faceless-video-craft`" |

**What the scaffold already is (0.1.0), so Code does not redo it:** SKILL.md (195 lines: front door, paths, read order with `BLOCKER-SKILL-FILE`, version + drift check, companion discovery, ten mandatory rules, pipeline, outputs, tool fence); `policy.md` (§H-0..H-7, F-2a/b, I-1, then 609 lines carried verbatim); `runbook.md`; `providers.yaml`; templates; `validate_request.py`. **What it is not:** `qa_render.py` and `beats_to_build_spec.py` are not written (T4 — **done this session**); the carried block still has engine cross-refs (T3 — **done this session**); no evals (T9).

**Why a new skill instead of 3.0.0, on record:** the past skill's failures were structural — two live copies with different contents, references pointed at but not shipped, mode chosen by phrasing, channel data vendored into the skill, five wrappers that never appeared in the slash list. A major version keeps the name and the install paths, which is exactly where those failures lived. A new name with one command, one canonical location and a drift check on every run removes the surface they lived on.

---

## §8 — Corrections on receipt (2026-09-05, this implementation pass)

Five factual corrections to this WO's own text, found while landing it, plus one dependency note. None change the ruling; all change what a reader should believe about the starting state. Recorded here rather than silently edited into §0–§7, per house convention (dated §-sections appended, never silent edits).

### 8.1 — WO-FVC-002 and WO-FVC-003 do not exist on this machine

This WO's header claims to supersede two prior work orders. Neither exists: `docs/wo/` in this repo holds only `WO-FVC-001.md` and `WO-SBR-001.md`; a full-history search (`git log --all`, `git rev-list --all --reflog --objects`) across every local branch, every worktree, and `origin` finds no commit ever touching a `WO-FVC-002.md` or `WO-FVC-003.md` path; the `claude-skills` repo has no `docs/wo/` at all. If they exist, they exist only on another machine or as chat history not yet committed anywhere. This WO is therefore the **second** FVC work order and the **third** WO overall in this repo's own record — there is no 002/003 artifact to reconcile against, only this text's own paraphrase of what they ruled.

### 8.2 — "The centella brief" names two different artifacts; §0.2/T0/step 3 meant the shorter one

`docs/wo/WO-FVC-001.md`, `videos/_channel/baseline.yaml` and this WO's earlier draft (T0 step 3, "pinned duration/aspect... Short, 9:16, ~72 s") all point loosely at "centella." Two artifacts answer to that name:

- `videos/centella-tiger-grass/` (legacy composition shape) — resolves to YouTube id `d6DPiORuPO4` per `videos/centella-barrier-recut-15s/index.html:14`, ~71–72 s.
- `outputs/2026-09-01-how-to-repair-skin-barrier/` — the actual nine-artifact-shaped run with a real `03-beat-sheet.json` (8 scenes, 45.28 s, 1080×1920, `presenter: kinetic-type`) and `01-story-brief.md` §Sourcing carrying a 9-row `[K-1]` table (R1–R9, R6 struck `CUT`; its own `sources.json` states verbatim "K-1 source resolution for the centella re-cut").

T0 step 3's own instruction — "Build the spike prompt from the centella run's existing `03-beat-sheet.json` and `01-story-brief.md` §Sourcing" — can only mean the second one; the first has no `03-beat-sheet.json` in that shape. The ~72 s duration in the earlier draft belongs to the *other* artifact and does not describe the spike's actual input. T0 must state which artifact it ran against, in its own `spike.md`, rather than leaving "the centella brief" ambiguous between a 45 s and a 72 s source.

### 8.3 — The `storyboard-review` reconciliation named in §0.3 and §5 is closed, not open

§0.3 and §5 both carry forward WO-003's "reconciliation is open" as a live dependency. It closed on **2026-09-04**, the day before this WO: `docs/wo/HANDBACK-2026-09-04.md` records master at `2b9b1e1` ("Merge remote-tracking branch 'origin/integrate/2026-09-04'"), five branches merged, six deleted. Verified directly against this checkout: `git merge-base --is-ancestor 2b9b1e1 HEAD` succeeds, so that merge is an ancestor of the branch this WO is being implemented on. `docs/wo/RECONCILE-PLAN.md` and `GATE2-2026-09-04.md` still end on their own "STOP, waiting for approval" lines and read as open in isolation — they were never updated after the handback superseded them; only `HANDBACK-2026-09-04.md` is authoritative. T1 does not need a separate reconciliation step; it works on master (or a worktree of it) directly. Residue from that closure — 6 branches proposed-drop but not deleted, 2 untouched stashes, no `reconciled-2026-09-04` tag — is tracked in `OPEN-ITEMS.md` and is this WO's dependency only in that a stale branch could still collide with `fvc-004/*` work; it does not block T1.

### 8.4 — Gate 0's ten slots: what is answerable from the repo today

Of G0-1 through G0-10, three are answerable without Kim and are pre-filled in the companion sheet `docs/wo/GATE0-FVC-004.md`: **G0-2** (`storyboard-review`; channel `@SeoulHabit` / `UCzqEGQ9uAU43AgyxGtLT7MA`, from `videos/_channel/baseline.yaml`), **G0-9** (`d6DPiORuPO4`, the WO's own default, confirmed to resolve to `videos/centella-tiger-grass` — see §8.2 on why that is a *different* artifact from T0's actual input), and **G0-10** (`/makemeavideo`, §7's own default). G0-4/G0-5/G0-7/G0-8 carry forward the WO's stated defaults unless Kim overrides them. **G0-1 (the story), G0-3 (HeyGen plan/credits/$-per-credit) and G0-6 (brand tokens, if not reading from a project skill) have no repo-derivable answer and are left blank, marked required.**

### 8.5 — The HeyGen MCP connector does not exist on this machine, and there is prior art that it may not connect at all

Checked directly: no `heygen` entry in `~/.claude.json`'s `mcpServers` (global or per-project), no `heygen` result from the MCP connector registry search, and no `heygen`-prefixed tool available in this session. OAuth to a remote MCP needs an interactive session and cannot be completed from here. T0, and therefore Gate 0, cannot run in this implementation pass.

This is not merely "not yet connected" — it has a specific prior failure attached. `wo/FVC-001/gate-0-notes.md:20`, quoting `videos/ectoin-survival-molecule/BRIEF.md:66-72`, records that during WO-FVC-001's own Gate 0, **"HeyGen/`hyperframes tts` sign-in is unavailable from an automation context"** — which is the reason `current-vo` (Higgsfield `generate_audio`) was chosen as the channel's voice provider instead, and why `videos/_channel/baseline.yaml:161-174` records Higgsfield as the live voice today. This WO's entire premise is that the *remote* HeyGen MCP's OAuth flow succeeds where that *local* sign-in failed. That may well be true — a remote MCP with its own OAuth callback is architecturally different from a CLI sign-in prompt — but it is an assumption, not a measured fact, and it belongs in T0's evidence rather than being discovered only after the rest of the pipeline is rebuilt around it.

### 8.6 — `H-4` vs. `restored-v1-rules.md`: resolved by folding, not carrying

Flagged inline at T3 above. `references/restored-v1-rules.md` (the file A-6, A-7, R-2 and R-3 all cite as "full text lives here") is not part of the shipped `makemeavideo` scaffold. Carrying those four rule ids as separate bodies would create four `BLOCKER-SKILL-FILE` conditions inside the rulebook itself. This session's T3 work folds their measured numbers and doctrine directly into `H-4`'s own text and treats the four ids as provenance tags on ledger lines only (so an `improve` chain reading an old `faceless-video-craft` run's ledger still resolves the citation). Recorded in full in `wo/FVC-004/t3-status.md`.

### 8.7 — `faceless-video-craft` is not actually frozen on this machine right now

§7's freeze ruling ("not edited, not deleted... so the drift that hurt v2 cannot recur") does not hold as of this session: `~/Desktop/claude-skills` has five uncommitted modified files (`faceless-video-craft/SKILL.md` and four `references/*.md`) bumping the skill to an unreleased **2.2.0** and adding rule `C-3a` (a shared brand end-card, every video, every format). Matching in-flight worktrees exist in the Story Board repo: `session/seoulhabit-endcard`, `session/snail-mucin-endcard`. This implementation pass does **not** touch that working tree — it belongs to another session — but flags the freeze violation here rather than silently working around it. `C-3a` is engine-independent content (a build-spec instruction, not a composition mechanism), so it is ported into `makemeavideo/references/policy.md` as a carried rule, credited to its origin, so the ruling is not lost to the freeze conflict. See `wo/FVC-004/t3-status.md`.

### 8.8 — `makemeavideo` is currently a claude.ai library skill, not a repo-canonical copy

§7's T1 rule ("no claude.ai library install... canonical copy = the `claude-skills` repo") is inverted today: the only copy of the `makemeavideo` 0.1.0 scaffold this session found is an *enabled claude.ai library skill* (`skill_01QpzHqVaWfgeEmhBFR4qtYs`), unpacked read-only into a session-scoped cache directory — not a zip, and not present anywhere in `~/Desktop/claude-skills`. `faceless-video-craft` is *also* still enabled in the library (`skill_019Mzn6o1WPy5UrghXRtfheb`), so both the old and new engine can resolve simultaneously — precisely the two-copies failure §7 exists to prevent. This session copies the scaffold verbatim into `claude-skills/makemeavideo/` and symlinks it into `~/.claude/skills/`, making the repo the canonical copy going forward (§7 T1). **Removing both skills from the claude.ai library itself cannot be done from this session** — it requires the account holder's library settings — and is handed to Kim as `TOUCHPOINT-LIBRARY-REMOVAL` in the handback.

---

**STOP. Waiting for Kim's `approved`, the HeyGen MCP connection, and the three required Gate 0 slots (G0-1, G0-3, G0-6) before T0 runs.**
