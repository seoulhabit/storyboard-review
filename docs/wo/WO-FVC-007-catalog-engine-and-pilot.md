# WO-FVC-007 — Catalog Engine, Component Release, and Single-Variable Pilot

**Target skill:** `makemeavideo` 0.3.0 → 0.4.0  
*(corrected 2026-09-07: WO-FVC-005 T7 already shipped 0.3.0, merged to `origin/master`. See `wo/FVC-007/REVIEW.md` C6.)*
**Target repo:** `seoulhabit/storyboard-review`
**Pilot subject:** `cGbokt_B_vE` — "The 1% trick K-Beauty brands don't want you to know" (Short, 1:56, 153 views, published 2026-08-30)
**Status:** awaiting Gate 0 answers + `approved`

---

## §0 — Supersession

This WO changes the production engine. Two prior rulings are reversed on the record, not silently:

| Superseded | Was | Now |
|---|---|---|
| Sep 5 ruling, "everything moves to HeyGen" | HeyGen Video Agent is the build engine; HyperFrames retired | HyperFrames CLI is the build engine; Video Agent is removed from `makemeavideo` entirely |
| WO-FVC-006 (Credibility Gap remake) | Live, awaiting its own Gate 0 | Superseded. Its G0-1 palette question and G0-2 lane-change question survive as G0-2 and G0-3 below |
| R-4, browser-drawn lane only | No generative or photographic imagery in compositions | Photographic and generated imagery permitted **as B-roll only**, governed by B-1 |

R-1 (local render default), R-2 (HeyGen fence = voice, images, sound), R-3 (story from a pinned source), R-5 (Shorts = second 9:16 composition) survive unchanged. R-2 is in fact strengthened: with Video Agent gone, the fence is now the whole of HeyGen's role.

Policy layers that survive untouched: S0–S4, S8–S9, `K-1..K-5`, the Decision Ledger, the two human touchpoints, `request.yaml` as the front door.

---

## §1 — Gate 0

Nine slots: one already answered (G0-5), one already executed and awaiting confirmation-to-close (G0-1), three added by this review (G0-6, G0-7, G0-8), four open with no default. The run does not start until every open slot is answered and Kim writes `approved`.

- **G0-1 — Engine reversal. Already executed.** *(Corrected 2026-09-07: this shipped at WO-FVC-005 T7 — `makemeavideo` 0.3.0, merged to `origin/master`, zero `*video_agent*` calls outside the forbidden-tool fence. This slot now confirms the record rather than authorizes a pending change — see REVIEW.md C7.)* Confirm HyperFrames CLI is the build engine and Video Agent stays removed.
- **G0-2 — Imagery lane. This is a scope expansion, not a closure.** *(Corrected 2026-09-07: WO-FVC-006's Gate 0 closed 09:03 today ruling full imagery for that one video only. This slot asks for the same thing permanently, across every future video. Worth ruling on as the expansion it is — see REVIEW.md C9.)* Confirm photographic and generated imagery is permitted in compositions as B-roll, permanently, under B-1.
- **G0-3 — Palette. `[BLOCKS T2]`** With G0-5 answered, the token layer is no longer one part of the design system — it *is* the design system, and the retrofit writes it into every catalog component. *(Corrected 2026-09-07: the live sheet is six tokens, not three — `videos/_system/tokens/colors.css`: `--bg #F4EDE3` cream, `--bg-lift #FAF3E7`, `--ink #26215C` indigo, `--accent #9C3A32` clay, `--rule #C0A265` brass, `--muted rgba(38,33,92,.55)`. Nocturne and the WO-FVC-006 direction are **not live alternatives**: WO-FVC-005 G0-8 already confirmed cream/ink/clay/brass, and recorded that no Nocturne sheet exists anywhere in this repo. R-13's own contrast finding — brass on ivory measures 2.10:1 and fails — already rules out a Nocturne-adjacent pairing under this WO's own floor. See REVIEW.md C8.)* This is now the single highest-consequence open slot: confirm the existing six-token sheet, or name a real alternative and its contrast numbers.
- **G0-4 — B-roll source precedence.** Rank these; T5 consumes the ranking in order and stops at the first that fills the slot:
  - existing plates already in `storyboard-review` (free, unknown coverage)
  - frames extracted from the original `cGbokt_B_vE` composition (free)
  - `seoulhabit-product-imagery` prompt pack rendered via Higgsfield (costs credits, fictional products, no attribution burden)
  - `vidiq_generate_broll` free stock (cheap, **requires on-screen photographer attribution**, landscape-dominant)
- **G0-5 — ANSWERED (2026-09-07).** The `sh-*` component library is retired; the design system is demoted to **foundations only** — colour, type, space, grid, safe areas, motion. All structure comes from the catalog, recoloured into SeoulHabit tokens by the retrofit. See R-12. Recorded rationale: the bespoke component library was commissioned without knowledge that the catalog existed. It is archived rather than deleted, because its token layer is exactly what now gets applied to every catalog item.
- **G0-6 — `catalog-v2` disposition.** `catalog-v2/` (committed 2026-09-05, one day before this WO) is a second, first-party-authored component library — 14 components across `label-literacy` and `ingredient-fate`, plus governance schemas and a `format-contract.json` already shaped like a slot contract. R-11 ("we do not author components") forbids continuing that work but doesn't name it. Options: retire it alongside `sh-*`; keep it as the ingredient/evidence data layer (its facts and provenance, not its presentation, may fall outside R-11's reach); or fold its slot-contract shape into T3's registry. *(Added 2026-09-07, see REVIEW.md B2/G0-6.)*
- **G0-7 — compiler path under R-12. `[BLOCKS T6]`** R-12 archives the twelve `sh-*` components that `compile_composition.py` (29 hardcoded references) and all six template spines are built on — and T7, where the archiving happens, runs after T6, which needs a working compiler. Options: rewrite the compiler to cast from the catalog registry before T6 runs; or keep `sh-*` live through T6 and archive only at T7, after the pilot no longer depends on it. *(Added 2026-09-07, see REVIEW.md B1/G0-7.)*
- **G0-8 — semantic state tokens.** `videos/_system/tokens/colors.css` has six tokens and none of the "positive, warning, info" states T2 step 2 maps to. Under R-12 the token list is the brand, so extending it is a brand call, not a script decision. Options: extend the sheet; or have the retrofit reject any catalog item that needs a state colour it doesn't have. *(Added 2026-09-07, see REVIEW.md B3/G0-8.)*


---

## §2 — Standing rulings

**R-11 — The catalog is the only source of components. We do not author components.** This is the governing rule of this WO and it outranks every other §2 entry. Every scene, overlay, transition, and piece of furniture in every video comes from the HyperFrames catalog. No bespoke component is written for a beat, no matter how well it would fit, and no existing component is forked to make a variant.

When no catalog component fits a beat, the run halts with `BLOCKER-CAST:<beat_id>` and Kim rules on exactly two options:

1. **Rewrite the beat** so an existing component carries it. This is the default and should resolve the large majority of halts.
2. **Contribute the component upstream** to the HyperFrames catalog, per their contribution guide, and consume it back through the normal retrofit path once merged.

There is no third option. "Write one locally just this once" is the failure mode this rule exists to prevent — it is how the design system accumulated ten components and three palettes.

**R-14 — Catalog governance.** *(renumbered from this WO's original `R-6` — that id is taken by WO-FVC-005's merged safe-area ruling, cited in `videos/_system/tokens/spacing.css` and `MANIFEST.json`. See REVIEW.md C2.)* The catalog repo is cloned once, pinned to a SHA, and lives **outside the build path** (`vendor/hyperframes/`, gitignored from the build, SHA recorded in `videos/_system/catalog/manifest.json`). It is a build input, never a runtime dependency, and is never read at render time.

Catalog items are never consumed raw. Every item passes `retrofit_catalog.py` (T2) and is committed to `videos/_system/catalog/` as project source. The retrofitted file is the artifact. Catalog items are not the design system and never edit `videos/_system/` outside `catalog/`.

**R-7 — Engine.** `hyperframes render` locally (bare, globally installed — not `npx`, which silently re-accumulates large caches; see `CLAUDE.md` and REVIEW.md P7). HeyGen supplies voice, images, and sound only. No `render_video`, no Video Agent, no avatars, no templates.

**R-8 — B-1, the B-roll rule.** In full:
- B-roll occupies **no more than one third of runtime**, measured in seconds across the finished composition.
- B-roll is **forbidden on any beat carrying a claim or its evidence**. Those beats are carried by a catalog component with text slots only, skinned by the design tokens. The claim register (`K-1`) marks them; the caster reads the mark.
- Every B-roll still is wrapped in a camera-move component. A still on a still background renders as a frozen frame with a progress bar — this is a known HyperFrames failure, not a style note.
- No faces in frame. Crops at the jaw or above the shoulder. `H-3` face detection stays on and stays unchanged.
- No real branded products. Fictional or unbranded only. The channel's position is claims discipline; showing a competitor's bottle while discussing label deception is a liability, not an illustration.

**R-12 — The design system is foundations, not components.** `videos/_system/` (excluding its `catalog/` subdirectory, which R-14 governs separately) holds colour tokens, the two type families and their steps, the space scale, grid, safe areas, and motion tokens. Nothing else. *(Clarified 2026-09-07: R-14 — drafted in this WO as R-6 — commits retrofits to `videos/_system/catalog/`, which otherwise reads as contradicting this rule's "nothing else." See REVIEW.md C3.)* The ten `sh-*` components move to `videos/_system/_archive/` with a dated note recording why; they are not deleted and not referenced by any composition. Recolouring the catalog into these tokens is how the channel keeps its identity — the brand now lives entirely in the token layer, which makes G0-3 load-bearing for every frame the channel ever renders.

**R-13 — Recolouring has a floor, and some components refuse it.** Swapping a component's palette can destroy the contrast it was designed around. Brass on ivory measures 2.10:1 and fails as text; that finding is already on record and it will recur across the library.

- Every component, after recolouring, passes a **4.5:1 contrast check on rendered pixels** — not on declared CSS values. This reinstates a rule that was dropped once already. A component that fails is rejected from the registry, not shipped with a warning.
- Some components' identity *is* their colour: `x-post` (platform navy), the terminal and VS Code themes, the liquid-glass aurora backgrounds, `halftone-field`. Recolouring these produces something that reads as broken rather than branded. The retrofit classifies each item as `recolourable`, `foreign-surface` (kept at native colour, used deliberately as a foreign object — this is the correct treatment for a social-post card inside an editorial video), or `reject`. The classification is recorded in the manifest and reviewed at Gate B.

**R-9 — Casting is data.** Scene selection is a lookup in `catalog-registry.yaml`, not a per-run judgement. The caster picks the highest-ranked candidate whose slot contract the beat can fill. Every pick and every rejection is one Decision Ledger line with the reason.

**R-10 — The pilot is a single-variable experiment.** Same script, same voiceover audio, same beat sheet. Only the visual system changes. The original video is **not** replaced, unlisted, or edited — the 153-view baseline must stay intact and accumulating for the readout to mean anything.

---

## §3 — Tasks

### T0a — Clone and pin the catalog

Clone `https://github.com/heygen-com/hyperframes` into `vendor/hyperframes/`, pinned to a SHA, recorded in `videos/_system/catalog/manifest.json` alongside the CLI version in use.

Verify the path before assuming it. If that org/repo 404s, resolve the real one from the `hyperframes` npm package metadata (`npm view hyperframes repository.url`) rather than guessing, and record whichever path was used.

Then inventory what was cloned: every catalog item, its category, its native `data-width`/`data-height`, its declared slots, and whether the source hardcodes colour or reads CSS variables. Write it to `docs/wo/007/catalog-inventory.json`. This file is the input to both T0b and T3 — with the repo local, the registry is **generated from real metadata and then curated**, never hand-transcribed from the docs site.

Sonnet/medium.

### T0b — Aspect survivability scan `[GATE A]`

**This is the load-bearing risk in the whole WO and it runs immediately after the clone.**

The channel is 15 Shorts to 2 long-form. The pilot is 9:16. Most catalog items are authored at 1920×1080. If the catalog does not survive a portrait reframe, its value to this channel is a fraction of what §3 assumes.

With the repo local this is a programmatic sweep, not a twelve-item sample. For every item in the inventory: set the root to 1080×1920, render a probe frame, and check that no element leaves the safe area, no text clips, and no absolutely-positioned element lands off-canvas. Record a verdict per item — `native-portrait`, `reframes-clean`, `reframes-with-edits` (with line count), or `landscape-only` — and write it back into the inventory.

Pre-written pass/fail, judged over the ~40 items the registry actually needs rather than all 375:

- **PASS** — 70% or more are `native-portrait` or `reframes-clean`. Proceed as written.
- **PARTIAL** — 35–70%. Halt at Gate A. Kim rules: reduced registry, or retarget the pilot to long-form.
- **FAIL** — under 35%. Halt at Gate A. The catalog is a long-form asset for this channel and the WO is rescoped before further work.

Report the verdict split by category — if the failures cluster in one area (say, data and charts) that is a different and more manageable finding than an even spread.

Do not begin T2 before Kim rules on Gate A. Sonnet/medium.

### T1 — Asset sweep and voiceover extraction

1. Sweep `storyboard-review` for every already-rendered plate from the centella and PDRN runs. Produce `docs/wo/007/asset-inventory.md`: path, dimensions, aspect, what it depicts, whether it contains a face, whether it is reusable as B-roll under B-1.
2. Extract frames from the original `cGbokt_B_vE` composition. These are design-system frames rather than photography, so grade them honestly — most will be typographic and unusable as B-roll. Record what is genuinely reusable.
3. Voiceover. *(Corrected 2026-09-07: the source project is `videos/kbeauty-one-percent-line/` — already 9:16, 1080×1920, 115.54s — and its per-scene voiceover is already on disk at `videos/kbeauty-one-percent-line/assets/voice/` as 8 `NN-raw.mp3`/`NN.wav` pairs. Re-extracting audio from the published YouTube URL would pull the finished mix — VO plus BGM plus SFX — not isolated voiceover, and would bake the original's music bed into what R-10 calls "the fixed variable." Use the local per-scene WAVs, re-placed at the composition's own offsets, instead of a YouTube extraction. See REVIEW.md P1.)* Store as `videos/kbeauty-one-percent-line-v2/vo/source-vo.wav`, hash it, and ledger the hash. **This file is the fixed variable of the whole experiment — it is never regenerated, re-synthesized, or re-levelled beyond a true-peak pass.**
4. Probe its exact duration. The rebuilt composition's total duration must match it to within 100 ms.

Sonnet/medium.

### T2 — `retrofit_catalog.py` `[Opus/High]`

The creative centre of this WO. Rather than hand-editing each catalog item — which does not scale and drifts immediately — build the retrofit as a script so the library is reproducible and future catalog additions cost minutes.

Input: a catalog item's HTML as written by `npx hyperframes add`.
Output: a token-native, brand-safe component in `videos/_system/catalog/`.

The script must:

1. **Strip remote font links.** Delete every `fonts.googleapis.com` / `fonts.gstatic.com` link and replace with root-relative `@font-face` references to `videos/_system/fonts/` — matching `videos/_system/tokens/fonts.css`, not base64. *(Corrected 2026-09-07: base64-by-default was already investigated and rejected — see `videos/_system/fonts/SOURCES.md`, "Why root-relative, not base64-inlined, by default"; ~2.4 MB duplicated per sub-composition across a ~50-scene compile. `--inline-fonts` remains an optional compiler flag for single-file deliverables.)* Reference all **five** faces, not two: DejaVu Serif 400/700, Archivo variable (100–900), and Noto Serif KR 400/700 layered onto the DejaVu family under a Hangul `unicode-range` — dropping the Noto pair silently loses Korean coverage for 서울의 습관, the channel's own name. A Google Fonts link previews correctly and silently falls back in the renderer — this is the documented brand-breaking failure and the reason this step is mechanical rather than optional.
2. **Recolour to tokens — this is now the brand application, not a tidy-up.** Parse every colour literal in the item's `<style>` block and map it to a design token by role: surface, raised surface, ink, muted ink, accent, hairline, and the semantic states (positive, warning, info). Publish the role map as a reviewable file — it is the single most consequential artifact in this WO, because it decides what every catalog component looks like on this channel.
   - **Fail loudly on any literal the mapper cannot classify.** Never guess a mapping.
   - After recolouring, render a probe frame and run a **4.5:1 contrast check on the pixels** per R-13. A failing component is rejected from the registry, not shipped with a warning.
   - Classify the item `recolourable`, `foreign-surface`, or `reject` per R-13 and record it in the manifest.
   - Watch the derived-colour components specifically — aurora fields, glows, halftone, and anything the catalog describes as "accent-derived" compute their palette from a base. Recolouring those changes their entire character rather than their trim, so they need visual review at Gate B, not just a contrast pass.
3. **Pin the runtime.** Replace every GSAP CDN reference — the repo carries both jsdelivr and cdnjs hosts and three shipped versions (3.14.2 / 3.12.5 / 3.12.2) — with `videos/_system/vendor/gsap-3.14.2.min.js`. Watch also for `three@0.128.0` and `pretendard` CSS on items that use them; neither has a vendored copy yet, so an item depending on either halts for a sourcing decision rather than silently keeping a live CDN reference. No build-time network dependency.
4. **Record aspect.** Write the item's native dimensions and its T0 reframe verdict into the manifest.
5. **Emit a manifest entry** in `videos/_system/catalog/manifest.json`: item name, upstream version, retrofit script version, aspect, slots, and the hash of the retrofitted file.

Ship it with tests over at least three items of different shapes — one token-native component, one hardcoded block, one media wrapper.

### T3 — `catalog-registry.yaml` and the S4.5 caster `[Opus/High]`

Scene casting becomes a new stage between the beat sheet (S4) and the build (S5).

Generate the registry skeleton from `catalog-inventory.json` — every item, its real slots, its real aspect verdict — then curate: rank the candidates per purpose and delete what the channel will never use. Authoring it by hand from the docs site is forbidden; the metadata is local now and hand-transcription is how drift starts.

The registry maps **beat purpose** to a ranked list of component candidates, each with a slot contract:

```yaml
- purpose: claim_vs_evidence
  broll_allowed: false          # B-1: claim beats are design-system only
  candidates:
    - component: comparison-split
      slots: {before: text_block, after: text_block}
      aspect: [16:9, 9:16]
    - component: before-after-wipe
      slots: {before: media_or_text, after: media_or_text}
      aspect: [16:9]
```

The caster reads each beat, filters candidates by output aspect and by `broll_allowed` against the claim register, picks the highest-ranked candidate whose slots the beat can fill, and writes one ledger line per pick — including the rejected candidates and why. A beat with no viable candidate halts with `BLOCKER-CAST:<beat_id>`; it never falls back to a generic card.

Registry coverage for this WO: the four scene systems (editorial imagery, SVG diagram, claim-vs-evidence, checklist), plus B-roll wrappers, plus the channel furniture in T4.

### T4 — Channel furniture

Retrofit and release the follow/subscribe and identity components, since they recur in every video and should be picked once:

- `yt-lower-third` — subscribe lower third, wired to the existing channel avatar PNG from the design system
- `logo-outro` or `logo-brand-close` — end card. Pick one in T4 and pin it; do not decide per video.
- `cta-close` — action line, for videos that carry one
- `instagram-follow` / `tiktok-follow` — retrofit but leave unassigned; cross-promo is a per-video call

These land in `videos/_system/catalog/` like everything else and get registry entries with fixed placement rules (lower third at first third, end card at final 4 seconds).

### T5 — B-roll sourcing

Work G0-4's precedence in order. For each B-roll slot the caster opened, take the first source that fills it and stop. Record source, cost, and licence per plate in `docs/wo/007/broll-manifest.md`.

If the stock path is reached, portrait orientation is mandatory and the attribution string must be composed into the frame — surface the attribution burden to Kim before spending, because on a claims-discipline channel an on-screen photo credit is a visible cost.

Every plate is checked against B-1 before it enters the build: no face, no real brand, camera move attached.

### T6 — Pilot build `[GATE C]`

Rebuild `cGbokt_B_vE` as `videos/kbeauty-one-percent-line-v2/`. *(Corrected 2026-09-07: matches this repo's own naming convention — `-v2`/`-recut-Ns` suffixes are in use, `-r2` has no precedent, and every existing slug keeps its topic anchor. See REVIEW.md P6.)*

- Beat sheet: carried over from the original, unchanged. **Do not re-write the script.** *(Note: no `03-beat-sheet.json` exists for the source project — it predates the staged layout; the script lives in `STORYBOARD.md`. "Carried over unchanged" means deriving one from `STORYBOARD.md` + the SRT, which is itself a step worth naming rather than treating as a mechanical carry-over. See REVIEW.md P2.)*
- Voiceover: `source-vo.wav` from T1, unmodified.
- Scenes: cast by S4.5 from the retrofitted library.
- B-roll: T5 plates, under the B-1 cap.
- Render: `hyperframes render`, locally, 1080×1920 (bare, not `npx` — see R-7).

Then `hyperframes check` (lint, runtime, layout, motion, contrast, static sweep), `H-3` face detection over extracted frames, `K-4` over the finished frames, safe-area, and true peak no higher than −1 dBTP.

Present extracted frames and the render for Kim's review at Gate C. Nothing publishes without it.

### T7 — Skill update to 0.4.0

Only after the pilot passes Gate C — the skill is updated from what actually worked, never from what was planned.

*(Corrected 2026-09-07: `makemeavideo` already shipped 0.3.0 at WO-FVC-005 T7, merged. The items struck below are already done and re-verify only; do not redo them. See REVIEW.md C6.)*

- ~~S5–S7 rewritten against the HyperFrames CLI. Every `[SPIKE:n]` marker tied to Video Agent is removed, not left dangling.~~ *(done at 0.3.0 — re-verify, don't redo)*
- New S4.5 stage documented in `runbook.md`. **(genuinely new)**
- ~~`§H` rules: `H-1` (build spec generated, never typed) survives and now generates against the registry.~~ `H-1` needs to generate against the **catalog registry** specifically (0.3.0 generates against `videos/_system/` templates) — this part is new, pending G0-7. ~~`H-5` (per-scene chat fixes, capped) is deleted — it described a Video Agent affordance that no longer exists. Its replacement is a per-scene re-render cap.~~ *(done at 0.3.0: cap 2/scene, 4/run — re-verify, don't redo)*
- `B-1` added to `policy.md`. **(genuinely new)**
- `R-14` (was drafted as R-6 — renumbered, see C2), `R-7`, `R-9`, `R-10`, `R-11`, `R-12`, `R-13` added. **(genuinely new)**
- ~~`providers.yaml` updated: HeyGen roles narrowed to voice/image/sound.~~ *(done at 0.3.0 — `usd_per_credit: 0.049` already recorded; re-verify, don't redo)*
- ~~`CHANGELOG.md` records the engine reversal in plain terms.~~ *(done — 0.3.0 entry opens with exactly this. Add a 0.4.0 entry for this WO's own changes instead.)*
- `sh-*` components moved to `videos/_system/_archive/` per R-12, with a dated note. `videos/_system/` is left holding foundations only. Verify no composition still references an archived component before closing. **(genuinely new — pending G0-7; do not run before G0-7 is ruled, see B1)**
- ~~Canonical install is the `claude-skills` repo. Resolve the 0.2.0-vs-0.3.0 shared-checkout drift as part of this task, and verify both machines resolve the same version before closing.~~ *(that drift is closed. A different drift is live: a 0.1.0 Video-Agent-era copy is loadable this session as `anthropic-skills:makemeavideo`, and `~/Desktop/claude-skills` was deleted, leaving six broken symlinks in `~/.claude/skills`. Resolve **that** drift as part of this task instead — see REVIEW.md §5.)*

### T8 — Publish envelope (held)

Paste-ready title, description, tags, thumbnail. Published as a **new** video. Publish is Kim's click, not Code's.

### T9 — Readout

48-hour and 7-day pull against the original's baseline. The comparison is retention curve first, then views. Since VO and script are constant, any delta is attributable to the visual system — that is the entire point of the design, and the readout should say so or say why it cannot.

---

## §4 — Gates

| Gate | After | Kim rules on |
|---|---|---|
| A | T0b | Aspect verdict — proceed, reduce registry, or rescope |
| B | T3 | The registry: the component vocabulary the channel will use for every future video |
| C | T6 | Pilot frames and render |
| D | T8 | Publish |

---

## §5 — What this WO does NOT close

- The Credibility Gap remake. WO-FVC-006 is superseded; if that video is still wanted it comes back as a new WO built on this engine.
- ~~The PDRN story (`STORY-pdrn-left-the-clinic.md`). Currently written against Video Agent.~~ *(Corrected 2026-09-07: no file by that name exists; the actual project is `pdrn-left-the-clinic` on `session/pdrn-clinic`, already built and rendered in both aspects, resolved skill 0.3.0. HeyGen appears only as a rejected VO provider, HTTP 402. Not written against Video Agent, and not open. See REVIEW.md C10.)*
- ~~Design-system safe-margin question, still open from WO-FVC-005.~~ *(Corrected: closed by R-6 at WO-FVC-005 T4 — "both canvases now no findings." See REVIEW.md C10.)*
- HeyGen connector authorization and the credit cap. *(Note: T5's Higgsfield path does not need connector auth — Higgsfield is separate from the `heygen` MCP. But "already authorized" is wrong as stated: `providers.yaml` carries no Higgsfield row, removed at WO-FVC-004. It was re-authorized only on WO-FVC-006's branch, `session/wo-fvc-006-gate0`, which this WO supersedes — see REVIEW.md C10 and G0-6.)*
- Long-form catalog coverage. This WO proves the path on a Short.
- **Upstream sync cadence.** The clone is pinned at one SHA. When and how often to re-pull, and who reviews the diff before the retrofit re-runs, is not decided here. Propose a cadence in the handback; do not adopt one unilaterally.
- **The upstream contribution backlog.** Every `BLOCKER-CAST` that R-11 resolves by option 2 is a component someone has to write and submit. That queue is real work and is not scoped in this WO.

---

## §6 — Handback

`docs/wo/007/HANDBACK.md`: what shipped, the T0 spike table, the retrofit report per component, the registry, the cost table by provider, every open item, and the version + resolved path the skill loaded from on the final run.

---

## §7 — Tier map

| Task | Tier |
|---|---|
| T0a clone and inventory | Sonnet / medium |
| T0b aspect scan | Sonnet / medium |
| T1 sweep and VO extraction | Sonnet / medium |
| T2 `retrofit_catalog.py` | **Opus / High** |
| T3 registry and caster | **Opus / High** |
| T4 furniture | Sonnet / medium |
| T5 sourcing | Sonnet / medium |
| T6 pilot build | Sonnet / medium |
| T7 skill update | **Opus / High** |
| T8–T9 | Sonnet / medium |

Drop back to Sonnet after each Opus stretch so the next session does not default high.

---

## Kickoff line

> Read `docs/wo/WO-FVC-007-catalog-engine-and-pilot.md` in this repo (and `wo/FVC-007/REVIEW.md` alongside it) and work from it. Do not start T0a until G0-1 through G0-8 are ruled — G0-6 and G0-7 in particular block T2/T3/T7 and the pilot's compiler path. Once ruled, run T0a and T0b only, then stop for Kim's Gate A ruling.
