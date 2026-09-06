# WO-FVC-005 — HeyGen placement, local render, design-system compiler
**Target:** `makemeavideo` 0.1.0 → **0.2.0** (canonical copy = `claude-skills` repo, never the claude.ai library)
**Supersedes:** WO-FVC-004 §T0 (Video Agent spike) and §H-0 tool fence — *pending R-1 below*. Policy layers S0–S4, S8–S9, K-1..K-5, ledger, two touchpoints, `request.yaml` + wrappers survive unchanged.
**Status:** DRAFT — awaiting Gate 0 answers + Kim's `approved`.
**Kickoff line (paste into Code):** `Read docs/wo/WO-FVC-005.md in this repo and work from it. Fetch, don't work from memory.`
---
## §0 Why this WO exists
Three facts set the design:
1. **HeyGen pricing is asymmetric.** Import of a composition is free, enhance turns are free, **render is the paid step** (free tier 3/month; paid 20 credits per rendered minute). Voice (`create_speech`) and image generation are priced per asset, not per minute of output.
2. **The composition is portable.** What Claude Design emits for "Send to HyperFrames" — one self-contained HTML, paused GSAP timeline on `window.__timelines["main"]`, base64 fonts, scenes tiled by `data-start`/`data-duration` — is the same contract the open `hyperframes` CLI (`npx hyperframes check` / `render`) consumes on a laptop with Chrome. One artifact, two render paths.
3. **The website is canonical (MFS rule).** A published ingredient passport already carries its evidence graph. A video derived from a pinned published page inherits its `[K-1]` claim table instead of starting from zero — which is exactly what blocked the centella re-cut under `K-2b`.
So: **research → website publish → video**, with HeyGen spent only on what local tooling cannot produce (voice, images, optionally sound design), and every render local by default.
## §0.1 Standing rulings carried verbatim
- Two human touchpoints: the story in, the publish click out. Nothing else asks the operator.
- `K-1..K-5` claim floor. `H-3` faceless on pixels. `E-1` no metadata write without consent.
- `S0.0` version + drift check first, every run. Rules live in the skill; data and one-time picks live in `<repo>/videos/_channel/channel.yaml`. Never vendor one into the other.
- No auto-retry past a cap; no loosening a rule to pass a gate. A halt returns to Kim with its three lines.
- Run report written last, every mode; its §Summary is the final chat message verbatim.
## §0.2 Rulings this WO requires (Kim writes `approved`, or amends inline)
| ID | Ruling | Supersedes |
|---|---|---|
| **R-1 Render locality** | Default render = `npx hyperframes render` on Kim's machine. HeyGen `render_video` fires only when `request.yaml render: cloud` **and** `channel.yaml heygen.cloud_renders_this_month < cap` (default cap = 3, the free-tier allowance). Cloud render is a fallback, never the path. | Sep 5 "HeyGen renders too, HyperFrames retired" |
| **R-2 HeyGen scope fence** (replaces `H-0`) | **Permitted in a run:** `create_speech`, `list_voices`, `design_voice` (setup only), image generation *if exposed by the MCP* (T1 discovers), `search_audio_sounds`, `create_asset_upload`/`complete_asset_upload`, `get_current_user` / balance. **T1-only:** `import-claude-design-from-url`, `get_project`, `get-send-to-hyperframes-guide`. **Forbidden in a production run:** every `*video_agent*` call, `create_video`, `render_video` (outside R-1's gate), `create_ai_clipping`, avatars, templates, lipsync, translation, `delete_*`. | `H-0` |
| **R-3 Story source** | `request.yaml story.kind: url` pointing at a published `seoulhabit.com` page, pinned to the site repo commit SHA that produced it. `story.kind: text` is allowed only with `override_reason`. The `[K-1]` table is seeded from the page's evidence records; the run may add sources, never drop the page's. | WO-FVC-003 free-text front door |
| **R-4 Design-system source** | `SEOULHABIT-VIDEO-DESIGN-SYSTEM-v5.0` as implemented in Claude Design (`seoulhabit-system`). Code extracts it into `video/system/` once per design-system version and never hand-edits tokens, fonts, or component shapes. A change goes Claude Design → re-extract → version bump. | — |
| **R-5 Shorts path** | `F-2b` fixed: Shorts are a second 9:16 composition compiled from the same beat sheet, rendered locally. AI clipping is out (it needs a HeyGen-hosted render). | WO-FVC-004 "let the spike decide" |
## §1 Gate 0 — answer slots
Every slot has a `[default]` except the ones marked **required**. An unanswered slot runs on its default and the ledger says so.
| Slot | Question | Default |
|---|---|---|
| **G0-1 (required)** | Claude Design URL of `seoulhabit-system` (the v5.0 implementation) for `claude_design` MCP import in Code. | none — WO halts at T2 without it |
| G0-2 | Videos repo: root path + branch to work on. | `storyboard-review`, **fresh branch `wo-fvc-005`** off `master` (repo history is messy — no work on `master` directly) |
| G0-3 | `claude-skills` repo path on the machine running Code. | the path recorded in WO-FVC-001 Gate 0 |
| G0-4 | HeyGen plan and $ per credit. | credits only; $ column left blank in `providers.yaml` until answered |
| G0-5 | Render machine: which of the two computers, Chrome/Chromium installed? | the machine running this Code session; `T0` verifies `npx hyperframes render` end-to-end before anything else |
| G0-6 | `serif-split` vs `serif-everywhere`. | `serif-split` — DejaVu Serif Bold for ingredient names / titles / end cards; Archivo 800 for functional captions (legibility at 9:16 safe-area sizes) |
| G0-7 | Pilot page. | Code's `S2` picks among live `/ingredient/*` routes whose evidence records resolved in the Aug 13 verification; **centella** is first in line (13/13 sources verified, and an existing video to compare against) |
| G0-8 | Palette conflict (video cream/indigo/clay vs Nocturne brand sheet). | whatever `seoulhabit-system` holds — the design system is the single source; this is a Claude Design decision, not a code one |
## §2 Where HeyGen sits — the placement table
| Stage | Producer | Why here and not elsewhere | Cost class | Cap per run |
|---|---|---|---|---|
| S1 Story | Website page @ SHA | Canonical; carries sourced claims | free | — |
| S2 Topic gate, S3 Packaging, S9 Readout | vidIQ | Every quantitative fork | credits — see §4.5 budget | 8 calls |
| S4 Script | Claude (this session) | Free inside the session; `K-*` applied | free | — |
| **S4b VO pre-flight** | **HeyGen `create_speech`** | Per-scene audio + measured duration drives beat timing; cheap per asset | credits/asset | 1 per scene + 2 regens |
| **S5a Image plates** | **HeyGen image gen** (if MCP exposes it; else library lane) | Ingredient hero / texture plates the components need; **cache-first** in `video/library/images/` keyed `ingredient+component+aspect` so cost amortises across videos | credits/asset | ≤ 4 new per video |
| S5b Composition | **Compiler** (`video/system/` + beat sheet) | Generated, never typed (`H-1`); design system is code | free | — |
| S5c Sound | Local royalty-free folder, or HeyGen `search_audio_sounds`; **HeyGen enhance only if T1-F4 passes** | Enhance is free but only useful if the enhanced HTML can come back for local render | free / credits | 1 enhance turn |
| **S6 Render** | **`npx hyperframes render` locally** | The metered step, moved off the meter | machine time | cloud = 0 unless R-1 gate |
| S7 Render QA | `npx hyperframes check` + `H-2..H-4` frame gates | Unchanged | free | — |
| S8 Envelope | Existing (`E-1`) | Unchanged | free | — |
**Not in the lane:** HeyGen Video Agent (parked, not deleted — it re-enters only by a new ruling), AI clipping, avatars, Higgsfield for anything faceless (Sunny lane untouched, see §6).
Interpretation note: "AI image and text generation" is read as **image generation + text-to-speech**. If Kim meant script/caption text generation through HeyGen, say so at Gate 0 — the WO keeps script writing in-session because it is free there.
## §3 Tasks
Tier: **Sonnet/medium** unless marked. Only T2 earns **Opus/High**.
### T0 — Environment and drift (S-A)
- `S0.0` as written in the skill: version, resolved path, every other copy found, roster of skills + MCP tools, HeyGen credits at start, vidIQ credits at start.
- Verify on the render machine: `npx hyperframes --version` (≥ 0.8.23), Chrome reachable, `npx hyperframes render` succeeds on the package's own `faceless-explainer` route. **Fail here = WO halts** (G0-5 back to Kim). Nothing else runs on a machine that cannot render.
- Install vendor agent skills: `npx skills add https://github.com/heygen-com/hyperframes`.
- Done when `00-environment.md` exists with all of the above and `T0-RENDER-OK` in its first lines.
### T1 — Spike: four findings, pass/fail pre-written (S-A)
Write the four criteria to `T1-FINDINGS.md` **before** running anything.
| # | Finding | Pass | Fail consequence |
|---|---|---|---|
| F1 | **Local render parity.** Import the G0-1 composition into HyperFrames (free), pull the cloud preview frames via `get_project`; render the same HTML locally; extract frames at t = 0, each scene start, and the shader boundary. | `check` 0 errors; shader boundary frame non-black locally; font/colour match on a pixel diff of ≥ 3 frames within tolerance written in advance | Shader chains forbidden in local compositions (hard cuts only, rule `C-6` added); cloud render remains gated by R-1 |
| F2 | **VO cost + fidelity.** One `create_speech` on a 60-word scene with the channel voice; credits before/after; INCI names read correctly (glossary). | Credits delta recorded; duration returned; ≤ 1 mispronunciation | Brand glossary entries added (`create_brand_glossary`) before any production VO |
| F3 | **Image generation reach + cost.** Does the HeyGen MCP expose image generation? If yes: one faceless plate, credits delta, face check. | Recorded either way | If not exposed: `S5a` uses the library lane (existing `seoulhabit-product-imagery` prompt pack seeds the cache); HeyGen image is out of the run path |
| F4 | **Enhanced composition retrievability.** After one free enhance turn, can the enhanced HTML/assets be retrieved and rendered locally? | Yes, and it still passes `check` | Enhance step out of the lane; sound is local (`S5c` first option) |
Done when `T1-FINDINGS.md` has a pass/fail line per finding **and** `providers.yaml` has measured credit costs for VO, image (if any), and one cloud-render-minute (from the public rate, not spent).
### T2 — Design-system extraction + compiler design **[Opus/High]** (S-B)
- Pull `seoulhabit-system` via `claude_design` MCP (G0-1). Extract to `video/system/`:
  - `tokens.css` (`:root` vars only — colours, type scale, spacing, safe areas per format)
  - `fonts/` as base64 `@font-face` fragments (DejaVu Serif Bold, Archivo 800/600 — no Google Fonts `<link>`, per the import contract)
  - `components/sh-*.html` + `components/sh-*.motion.js` — the 10 components (chip, hook, ingredient, rows, steps, compare, evidence, myth, quote, endcard), each with its entrance + ≥ 2 mid-scene patterns and ≥ 3 eases
  - `templates/T1..T6.json` — scene maps (component sequence, slot names, duration budgets from the reading-time table)
  - `SYSTEM-VERSION` file = the Claude Design version string
- Design the compiler contract (§4.2) and write it as `video/system/COMPILER.md` before any code.
- Done when a reviewer can read `COMPILER.md` and predict the output file tree for a T1 beat sheet. **Flag "back to Sonnet/medium" at the end of this task.**
### T3 — Compiler build (S-B)
- `scripts/compile_composition.py` (or `.mjs`): `03-beat-sheet.json` + `video/system/` + `04-assets/` → `06-render/<format>/index.html` valid to the Send-to contract (one live root, base64 fonts/images, paused synchronous GSAP timeline registered on `window.__timelines["main"]`, scenes tiled, ≤ 1 contiguous shader chain, `autoAlpha` toggles on non-anchors, no `Date.now`/`Math.random`/`setTimeout`/`repeat:-1`).
- Hash the output and ledger it (`H-1`).
- Run `npx hyperframes check` on a synthetic T1 beat sheet for both formats. Done when 0/0 on both.
### T4 — Audio and render harness (S-B)
- `scripts/mix_audio.py`: VO files placed at beat starts, music bed under, loudness to the `H-4` band, true-peak ≤ −1 dBTP, output `06-render/<format>/audio.wav` referenced from the composition (muted `<video>`/separate `<audio>` per contract).
- `scripts/render_local.sh <slug> <format>`: check → render → extract frames → `qa.json`. Cloud path exists only as `render_cloud.sh` and refuses to run unless R-1's gate passes.
- Done when the synthetic T1 renders locally to MP4 with audio and passes `H-2..H-4`.
### T5 — Pilot run, full mode (S-C)
- `request.yaml` v2 (§4.1) with `story.kind: url` for the G0-7 page at its pinned SHA.
- S0 → S9 on 0.2.0 rules. Two formats per `R-5` if `T6` long-form triggers; otherwise one 9:16 T1–T5.
- `[K-1]` table seeded from the page's evidence records; `K-2b` must pass on the page's own sources — if it cannot, that is a **website-content finding**, not a video finding: halt, report, no loosening.
- Ends at the envelope. Kim clicks publish. Done when `09-run-report.md` §Summary is the last message.
### T6 — Recurrence (S-C)
- `scripts/enqueue_from_site.py`: diff the site repo's published ingredient routes between two SHAs → append `videos/_queue.yaml` entries (`slug`, `url`, `sha`, `content_type` → template). `/makemeavideo next` pops the head. The website release gate **is** touchpoint 1 from now on.
- `08-readout-schedule.md` 48 h / 7 d for the pilot; `learning-loop.md` unchanged.
- Done when the queue is populated from the current live routes and the pilot's readout is scheduled.
### T7 — Skill cut to 0.2.0 (S-D)
- `SKILL.md`: engine paragraph rewritten (compiler + local render; HeyGen = voice/images/sound only), pipeline diagram S4b/S5a-c/S6 updated, tool fence → R-2, `[SPIKE:n]` markers resolved from `T1-FINDINGS.md` into `channel.yaml`.
- `policy.md`: `§H` rewritten; new `C-6` if F1 failed; `F-2b` fixed per R-5; `PR-3` caps in measured credits.
- `runbook.md`: stage-by-stage calls for the new S4b–S6. `providers.yaml`: measured numbers.
- `00-environment.md` template gains a `render_machine` block. `09-run-report.md` template gains a **cost table** (credits per stage, vidIQ calls used vs cap).
- Version string bumped in one place; drift check passes on both machines. Done when the pilot re-runs in `build` mode on 0.2.0 with no `BLOCKER-SPIKE-PENDING`.
### T8 — Handback (S-D)
Per §7.
## §4 Specs
### 4.1 `request.yaml` v2 (additions only)
```yaml
story:
  kind: url            # url | text
  url: https://seoulhabit.com/ingredient/<slug>/
  sha: <site repo commit that published this page>
  override_reason: ""  # required when kind: text
template: auto         # auto | T1..T6 ; auto = rule §4.4
formats: [short]       # [short] | [long] | [long, short]
render: local          # local | cloud (cloud needs R-1 gate)
budget:
  heygen_credits_max: <from providers.yaml PR-3>
  vidiq_calls_max: 8
```
### 4.2 Compiler contract (write to `video/system/COMPILER.md` in T2)
- **Input:** `03-beat-sheet.json` (existing schema + per beat `component`, `slots{}`, `vo_file`, `vo_duration_s`, `image_ref`), `template`, `format`.
- **Timing rule:** scene `data-duration` = max(`vo_duration_s` + 0.3 s tail, reading-time floor for the slot word count). Hard ceiling 5 s except `sh-evidence` and `sh-compare` (8 s). Last readable element finishes entering by 50 % of the scene.
- **Shader rule:** at most one contiguous chain, placed only at the `sh-hook → sh-ingredient` reveal or `→ sh-endcard`; `cross-warp-morph` default; disabled entirely if F1 failed.
- **Assets:** fonts and images inlined base64; music/VO as `<audio>`; nothing relative, nothing on an expiring host.
- **Output:** `06-render/<format>/index.html`, `composition.hash`, `scene-map.json` (for chapters and the Shorts derivative).
- **Frame zero** = the hook, fully dense (`H-2`).
### 4.3 QA gates (unchanged set, local source)
`npx hyperframes check` 0 errors → frames extracted at mobile width → `H-2` frame zero, `H-3` face detection, `H-4` contrast 4.5:1 on text pixels / safe areas / type floor / static-hold / loudness / true-peak / duration within `S-2` tolerance → `K-4` reads finished frames. Source chips per claim, adjacent, secondary weight, legible.
### 4.4 Template routing (Code decides, ledgered)
| Page signal | Template |
|---|---|
| Ingredient passport | T1 Ingredient Explainer |
| Page has a "how to use / routine" section as primary | T2 How To Use |
| Page organised by concern/problem | T3 What It Solves |
| Two ingredients compared | T4 Comparison |
| Page carries a flagged misconception with a sourced correction | T5 Myth Correction |
| ≥ 4 sourced sections **and** vidIQ long-form demand above the `S-1` threshold in `channel.yaml` | T6 long + Shorts derivative |
### 4.5 vidIQ call budget (tool efficiency)
- Channel baseline (`vidiq_channel_analytics`, `vidiq_channel_performance_trends`, `vidiq_channel_stats`): **once per 7 days**, cached in `channel.yaml` with `fetched_at`; a run inside the window reads the cache.
- S2: `vidiq_keyword_research` ≤ 2 per run; `vidiq_outliers` 1 per run, niche-scoped.
- S3: `vidiq_generate_titles` 1 (returns a scored list — no re-calls to "try another"); `vidiq_score_thumbnail` 1 on the final concept only.
- S9: `vidiq_video_stats` 1 per video per readout.
- **Hard cap 8 calls per full run**; `vidiq_balance` before and after; every call ledgered with what decision it fed. A call that feeds no rule is a defect.
### 4.6 HeyGen budget
- Balance read before and after every session (`H-7` kept).
- VO: 1 `create_speech` per scene + ≤ 2 regenerations per run. Images: cache-first, ≤ 4 new per video. Cloud renders: 0 unless R-1 gate. Enhance: ≤ 1 turn, only if F4 passed.
- `providers.yaml` rows: `heygen.speech_per_call`, `heygen.image_per_call`, `heygen.render_per_minute = 20`, `vidiq.*` — all **measured in T1** except the public render rate.
### 4.7 Cost log line (appended per stage to `00-decision-ledger.md`)
`COST | <stage> | <provider> | <tool> | credits_before → credits_after | Δ | cap_remaining`
## §5 Session plan
| Session | Tasks | Tier | Est. | Exit artifact |
|---|---|---|---|---|
| **S-A Ground truth** | T0, T1 | Sonnet/medium | ~2 h | `00-environment.md`, `T1-FINDINGS.md`, `providers.yaml` measured |
| **S-B Compiler** | T2 → T3, T4 | **Opus/High for T2 (~45 min)**, then Sonnet/medium | ~3 h | `video/system/`, compiler, synthetic T1 rendered locally 0/0 |
| **S-C Pilot** | T5, T6 | Sonnet/medium | ~2 h + Kim's publish click | envelope, run report, queue populated |
| **S-D Skill cut** | T7, T8 | Sonnet/medium | ~1.5 h | `makemeavideo` 0.2.0 on both machines, handback |
Tier switches are flagged by Code at the S-B start (up) and end of T2 (down) — not every turn. Each session opens with `S0.0` and closes with a run-report §Summary even when no video was produced.
## §6 Does NOT close
- The Sunny / Higgsfield character lane, Glass Skin film, Descript assembly, Habi format test.
- Publish Desk automation (metadata still pasted by hand; `E-1`).
- The Nocturne-vs-video palette question (G0-8 defers it to Claude Design).
- MFS gate 13 / evidence-completion work on the website — a `K-2b` halt in T5 reports it, does not fix it.
- HeyGen Video Agent as an engine (parked). Localisation. Long-form beyond T6 routing.
- `faceless-video-craft` 2.1.0 archive step (WO-FVC-004 T9) — carried, not redone here.
## §7 Handback
1. `09-run-report.md` §Summary verbatim as the final message of each session.
2. Cost table: credits per stage per provider, vidIQ calls used vs cap, cloud renders used (should be 0).
3. `T1-FINDINGS.md` pass/fail with the pre-written criteria visible.
4. Rulings needed from Kim, three lines each: what halted, what it read, what the two options cost.
5. Refusals on record (anything the session declined to do and why).
6. Attestation: which skill version ran, from which path, on which machine, drift check result.
---
*Scope never widens inside this WO. Anything discovered that is not a task above is a line in §6 or a new WO.*

## §8 Corrections on receipt (2026-09-06, this implementation pass)

Per house convention (`WO-FVC-004.md` §8), factual corrections to this WO's
own text are appended here, dated, and never silently edited into §0–§7. Each
item names what the WO says, what the machine or the sources actually show,
and the amendment. Evidence for every line below is in
`wo/FVC-005/00-environment.md` and `wo/FVC-005/GATE0-answers-evidence.md`.

**8.1 — Target version.** §Target says `0.1.0 → 0.2.0`. `makemeavideo` is
**already at 0.2.0** (`SKILL.md:5`; `CHANGELOG.md`'s `0.2.0 — 2026-09-05 (T3
policy surgery + T4 scripts) — WO-FVC-004 §7` entry; claude-skills HEAD
`9f66e2c "…land makemeavideo 0.2.0 as the canonical copy"`). **Amends Target
to: `makemeavideo` 0.2.0 → 0.3.0.** Every task in §3/§7 that reads "0.2.0" as
the close target reads 0.3.0 instead. The version string lives in three
places in `SKILL.md` (lines 5, 8, 10), and `references/policy.md:1` and
`references/runbook.md:1` still carry a stale `v0.1.0` header — T7 corrects
all five sites, not one.

**8.2 — `npx` throughout.** Every command in §0.2, §3 (T0, T3, T4) and the
kickoff line is written `npx hyperframes …`. This repo's standing rule
(`CLAUDE.md`, confirmed live: `hyperframes` resolves globally at v0.8.30 via
`~/.nvm/versions/node/v24.18.0/bin/hyperframes`) is the opposite — invoke the
bare binary. `npx` silently re-accumulates caches; a prior incident cleared
4.01 GB of `npx`-only cache on 2026-09-03. **Amends every `npx hyperframes`
instance in this WO to the bare `hyperframes` invocation.**

**8.3 — R-1's cloud-render cap.** R-1 and §2 cap cloud renders at "3, the
free-tier allowance". `hyperframes auth status` on the render machine shows
account `hello@seoulhabit.com`, plan **`creator`**, **premium credits 0**
(resets 2026-10-06), **add-on credits 81** — no free-tier row at all. At the
public rate of 20 credits/rendered minute that is **~4 minutes of cloud
render for the entire month**. **Amends R-1's cap to be denominated in
credits** (`channel.yaml heygen.cloud_render_credits_cap`, default a small
fraction of the 81 on hand), not in a render count that assumes a tier this
account does not have. This also answers G0-4's credit half without
spending anything: 0 premium / 81 add-on / resets 2026-10-06. The $/credit
half remains open — Kim's plan page.

**8.4 — R-3/R-4 have no precedent in this corpus.** `seoulhabit.com`,
"site repo", and `SEOULHABIT-VIDEO-DESIGN-SYSTEM` return **zero hits**
anywhere in `docs/wo/` or `wo/` prior to this WO. R-3 and R-4 are new
ground, not a supersession of anything on record — noted so a reader does
not go looking for a prior ruling that doesn't exist. This WO is also where
**MFS** — carried open and undefined across WO-FVC-001 (§1 ruling 2, §5) and
WO-FVC-004 (§5) as *"the MFS `/ingredient/centella` passport"* — resolves:
MFS is `seoulhabit-learn` (below), and R-3 is what turns that long-deferred
`K-2b` unblock from a manual fetch-and-read pass into a mechanical one.

**8.5 — G0-1, the design-system source, resolved with a caveat.** Claude
Design holds **two projects named "SeoulHabit Video Design System"**:
`a7945a95-da21-4823-8b16-57c6ffa11558` (updated 2026-09-06) and
`75132ad8-b81c-4151-8a4c-83368df1d949` (updated 2026-08-28). They are not
versions of one system — the first is cream/ink/clay/brass, DejaVu Serif +
Archivo, no icons/shadows/imagery by rule, with exactly the ten components
and `T1`–`T6` templates R-4 and T2 describe; the second is Montserrat/Noto
Sans KR with an icon set, logo marks, scrims and a dataviz/evidence
component family — a different system entirely, not the `v5.0` implementation
named in R-4. **`a7945a95…` is the one T2 must extract.** Neither project
carries a version string (§8.6), so "v5.0" in R-4 cannot be verified against
the source and should be read as this WO's own label, not the project's.

**8.6 — T2's extraction assumptions, three corrections.**
(a) *No `SYSTEM-VERSION` file exists to extract* — the project carries no
version string anywhere. T2 synthesises one instead: project UUID +
`updatedAt` + a sha256 manifest of the extracted tree.
(b) *No font binaries are in the project* — `tokens/fonts.css` loads four
faces from the jsdelivr Fontsource CDN and says so in its own comment
(*"no font binaries were supplied with the brief… HyperFrames requires the
fonts base64-inlined"*); `assets/` is empty by design. T2's font step is
fetch-and-freeze from four named pinned URLs, not extraction.
(c) *The components are not `sh-*.html` + `sh-*.motion.js` pairs* — they are
twelve small React `.jsx` files (`ShHook.jsx` is 25 lines, `ShScene.jsx` is
33), pure presentational and styled entirely through CSS custom properties,
each with a sibling `.d.ts` and `.prompt.md`; and the templates are Claude
Design `.dc.html` canvas artboards, not JSON scene maps. **Amends T2** to:
port the twelve components to Python HTML emitters (cheap — no React build
belongs in the render path) and derive `templates/T1..T6.json` by hand from
the artboards as a checked-against spine, never generated from them.

**8.7 — The compiler is a port, not a new build.**
`claude-skills/faceless-video-craft/scripts/beats_to_composition.py`
(1,273 lines) is an existing, contract-verified beat-sheet → HyperFrames
generator — the exact mechanism T3 asks for. WO-FVC-004 *replaced* it with
`beats_to_build_spec.py` (a HeyGen prompt writer) when it moved the pipeline
to HeyGen Video Agent; this WO reverses that decision. **Amends T3's
estimate**: it is a port (measured this pass at roughly 35% verbatim, 40%
adapted, 25% new — see `wo/FVC-005/t3-status.md`), not a from-scratch build.
`claude-skills/makemeavideo/scripts/qa_render.py` (907 lines) already
implements most of T4's `H-2`/`H-3`/`H-4` gates against a rendered MP4, and
`catalog/tooling/` in this repo holds 12 further QA gates with control
fixtures — T4 should reuse both rather than re-authoring the QA layer.

**8.8 — `channel.yaml` does not exist.** §0.1 and the pipeline (43 sites in
the 0.2.0 skill) read `videos/_channel/channel.yaml`. The repo has
`videos/_channel/baseline.yaml`; `find` over the whole tree returns zero
`channel.yaml`. WO-FVC-004's T3 renamed the path in the skill's *prose* only
— its own `channel.template.yaml:3,5` still says `baseline.yaml` too. T0
confirms this drift before T1 trusts any channel-derived value; T7 either
renames the file in the repo or corrects the skill's path — Kim's call, not
defaulted here.

**8.9 — Story-source data, resolved.** Site repo is
`~/Desktop/SeoulHabit/seoulhabit-learn`
(`github.com/seoulhabit/seoulhabit-learn`), clean at `cacff81`. Route is
literally `/ingredient/${handle}` (`src/routes/passports.ts`), 21 routed
passports, all `passport_status: published`. Evidence counts vary sharply:
**centella-asiatica carries 12 citations / 12 findings** — the strongest
passport on the site and the one G0-7's default already names by
preference, now confirmed by data rather than by preference alone. **Nine
of the 21 passports carry zero citations and zero findings**
(collagen, exosomes, galactomyces, mugwort, panthenol, rice, retinol,
spicules, tranexamic-acid). Any of those nine chosen as a pilot or queue
entry (T6) will fail `K-2b` on the **website's** content — a finding for
§6, never a rule to loosen.

**8.10 — Scope carried, not touched.** WO-FVC-004 §7's own retarget to
`makemeavideo` **1.0.0** (with `faceless-video-craft` archived) never
shipped — the skill is 0.2.0 and `faceless-video-craft` is at an
**unreleased 2.2.0 with five uncommitted files**, not "frozen at 2.1.0" as
its own changelog claims. This WO does not resolve that; it stays open in
§6 for whichever WO finally does the 1.0.0/archive close.
