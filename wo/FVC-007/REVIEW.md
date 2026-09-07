# WO-FVC-007 — Review (2026-09-07)

Reviews `docs/wo/WO-FVC-007-catalog-engine-and-pilot.md` as revised 09:46
2026-09-07 (the version committed alongside this file). Per house convention
(`WO-FVC-004` §8 precedent), this is a dated appendix — the WO's own body
text is not edited to fix what's found here except for the mechanical
corrections listed in §3, applied in a separate commit.

**Verdict on the strategy:** sound. A catalog-as-only-source-of-components
rule (`R-11`), casting as data, a hard B-roll cap tied to the claim register
— this is the right shape for a channel doing 15 Shorts to 2 long-form.

**Verdict on the text as drafted:** not ready to run. Three items below
(§1) block a session that starts at T0a; the rest (§2–§4) would each cost a
session real time discovering them mid-run rather than before.

Every claim below was checked against the repo directly — commands are
included so this is reproducible, not just asserted.

---

## §1 — Blockers

### B1. R-12 breaks the compiler, and T7 archives it after T6 needs it

```
grep -c 'Sh[A-Z]' /Users/sumitchoudhary/Desktop/claude-skills-current/makemeavideo/scripts/compile_composition.py
# 29
```

All twelve `Sh*` component names are hardcoded in the compiler. All six
template spines (`videos/_system/templates/T1–T6.json`) are built from them
— `T1.json`'s `sequence` and `clay_slot_by_component` name `ShHook`,
`ShIngredient`, `ShRows`, `ShEvidence`, `ShEndcard` directly.
`videos/_system/COMPILER.md` §1 defines `scene.component` as "one of the
twelve `Sh*` names."

**R-12** ("The design system is foundations, not components... The ten
`sh-*` components move to `video/system/_archive/`... not referenced by any
composition") retires exactly what the compiler is built on. **T7** is
where that archiving happens — and T7 runs *after* **T6**, the pilot build,
which needs a working compiler. As sequenced, either the pilot builds on
components R-12 has already retired, or something rewrites the compiler to
cast from the catalog registry first — which nothing in the WO scopes.

Compounding it: `compile_composition.py:1090`'s `check_manifest()` halts
with `BLOCKER-SYSTEM` on any hash mismatch against `MANIFEST.json`. Moving
files to `_archive/` is a hash-changing edit; R-12 doesn't mention
re-hashing and adding an `amendments[]` entry, which is R-6's (the
*original* R-6, safe-area) own precedent for exactly this kind of change.

**Needs a ruling — proposed as new Gate 0 slot G0-7 in §4.**

### B2. `catalog-v2/` is unaddressed, and R-11 forbids it retroactively

`catalog-v2/` (committed 2026-09-05, one day before this WO) holds:

```
catalog-v2/story-systems/label-literacy/registry.json   # 9 components, 2 patterns, 9 shared primitives
catalog-v2/story-systems/ingredient-fate/registry.json  # 5 components
catalog-v2/governance/format-contract.json              # required_inputs / format_owned_fields / guardrails
catalog-v2/registry.json                                # 4 ingredient packs + global_rules
```

These are first-party *authored* components — not catalog imports. Each
`component.json` already records a slot contract and, in `ingredient-fate`,
a `layouts` field:

```
catalog-v2/story-systems/ingredient-fate/components/route-fork/component.json:
  "layouts": ["16:9", "9:16-safe"]
```

That is T0b's aspect verdict, already recorded, for a component T0b doesn't
know exists. `format-contract.json`'s `required_inputs` /
`format_owned_fields` / `guardrails` shape is functionally the slot-contract
idea T3 proposes building as `catalog-registry.yaml`.

**R-11** — "The catalog is the only source of components. We do not author
components... no matter how well it would fit" — forbids exactly this kind
of work going forward. **G0-5** explicitly retires `sh-*` but says nothing
about `catalog-v2`. It is a second, larger, two-day-old component library
and the WO does not mention it once.

**Needs a ruling — proposed as new Gate 0 slot G0-6 in §4.**

### B3. T2 step 2 maps to tokens that don't exist

```
grep -iE 'positive|warning|info|success|danger|error' videos/_system/tokens/colors.css
# (no output)
```

T2 step 2 requires the retrofit to map catalog colour literals to "surface,
raised surface, ink, muted ink, accent, hairline, and the semantic states
(positive, warning, info)." `videos/_system/tokens/colors.css` has six
tokens total — `--bg`, `--bg-lift`, `--ink`, `--accent`, `--rule`,
`--muted` — and its own comment: "the six fixed tokens. Nothing outside
this list ships." No semantic state tokens exist anywhere in the file.

Combined with step 2's "fail loudly on any literal the mapper cannot
classify, never guess" — the first catalog item carrying a green/red status
colour halts T2. Under R-12 (the token layer *is* the brand now), extending
the sheet is a brand decision, not something the retrofit script can decide
for itself.

**Needs a ruling — proposed as new Gate 0 slot G0-8 in §4.**

---

## §2 — Corrections (mechanical, applied to the WO text in a follow-up commit)

| # | Where | Issue | Fix |
|---|---|---|---|
| C1 | R-6, R-12, T2 (×2), T4, T7 | `video/system/` doesn't exist — the design system is `videos/_system/` (plural, leading underscore) | path corrected throughout |
| C2 | R-6 | R-6 is already taken — WO-FVC-005 minted it for safe-area widening (merged, cited in `tokens/spacing.css` and `MANIFEST.json`'s `amendments[]`, and in `H-4`) | renumbered R-14 |
| C3 | R-6 vs R-12 | contradiction: R-6 says retrofits commit to `.../catalog/`; R-12 says the system dir holds foundations, "Nothing else" | resolved once R-6/R-14 and R-12 use the corrected path and R-12 is read as governing the parent dir, R-6/R-14 the `catalog/` subdir under it |
| C4 | T2 step 1 | base64-inlining fonts reverses a documented ruling (`fonts/SOURCES.md`, "Why root-relative, not base64-inlined, by default"; ≈2.4 MB × ~50 sub-compositions) — and names only 2 of the 5 real faces, dropping Noto Serif KR (Hangul, under a `unicode-range` on the DejaVu family) — **this drops Korean coverage for 서울의 습관, the channel's own name** | step rewritten: keep root-relative `@font-face`, reference all 5 faces |
| C5 | T2 step 3 | scopes only "the jsdelivr GSAP CDN reference" — repo actually has 2 CDN hosts (jsdelivr + cdnjs), 3 GSAP versions (3.14.2/3.12.5/3.12.2), plus `three@0.128.0` and `pretendard` CSS; `fonts.googleapis.com` in 657 files incl. `catalog/` itself | step scope widened; vendored target `videos/_system/vendor/gsap-3.14.2.min.js` confirmed correct |
| C6 | header, T7 | targets `makemeavideo` 0.2.0 — shipped 0.3.0 on 2026-09-06 (`WO-FVC-005` T7, merged). 6 of T7's 8 items are already done: S5–S7 rewritten, all 4 `[SPIKE:n]` resolved, `H-5` already a per-scene cap (2/scene, 4/run), `providers.yaml` narrowed (`usd_per_credit: 0.049`), CHANGELOG's 0.3.0 entry records the reversal, 0.2.0-vs-0.3.0 drift closed | header retargeted to 0.3.0→0.4.0; T7 struck down to only the genuinely new items: S4.5, B-1, new R-numbers, the `sh-*` archive (pending G0-7) |
| C7 | G0-1 | asks Kim to approve a reversal already merged — 0.3.0 has zero `*video_agent*` calls outside the forbidden-tool fence | marked "already executed at WO-FVC-005 T7; confirm to close, not to authorize" |
| C8 | G0-3 | names 3 of 6 live tokens (omits `--bg-lift`, `--rule` brass, `--muted`); offers Nocturne and pearl-white as live alternatives when WO-FVC-005 G0-8 already confirmed cream/ink/clay/brass and recorded **no Nocturne sheet exists anywhere in the repo** — R-13 itself notes brass-on-ivory measures 2.10:1, i.e. a Nocturne-adjacent pairing already known to fail R-13's own floor | option list corrected; full 6-token set quoted |
| C9 | G0-2 | WO-FVC-006's Gate 0 (closed 09:03 today) ruled full imagery **scoped to that one video**; G0-2 here asks for the same thing **permanently** without naming it as an expansion | reworded to state the expansion explicitly |
| C10 | §5 | all three "does not close" items are stale: `STORY-pdrn-left-the-clinic.md` doesn't exist and the actual project is *not* Video-Agent (built + rendered both aspects on `session/pdrn-clinic`, skill 0.3.0, HeyGen only as a rejected VO provider, HTTP 402); safe-margin was closed by R-6 at WO-FVC-005 T4; Higgsfield is not "already authorized" — `providers.yaml` has no Higgsfield row (removed by WO-FVC-004); it was re-authorized only on WO-FVC-006's branch, which this WO supersedes | all three corrected or removed |
| C11 | R-13 | closing paragraph runs directly into R-9 with no line break | paragraph break inserted |

---

## §3 — Pilot-specific (R-10's single-variable premise)

**P1 — VO source.** `videos/kbeauty-one-percent-line/assets/voice/` holds 8
per-scene `NN-raw.mp3`/`NN.wav` pairs already on disk. What T1.3's
`vidiq_edit_media extract_audio` would pull from the published YouTube URL
is the **finished mix** — VO + BGM + SFX — not isolated voiceover. Calling
that `source-vo.wav` bakes the original's music bed into the "single
variable that changes." Recommend using the local per-scene files,
re-placed at the composition's own offsets, and dropping the YouTube
extraction step.

**P2 — no beat sheet exists to carry over.** `kbeauty-one-percent-line`
predates the staged project layout; there is no `03-beat-sheet.json`. The
script lives inside `STORYBOARD.md`. T6's "carried over from the original,
unchanged" needs a machine-readable original first — deriving one from
`STORYBOARD.md` + the SRT is itself a step, and itself a place the
"single variable" premise can leak.

**P3 — T8 breaks single-variable.** A new title and thumbnail are CTR
variables larger than the visual system. Recommend reusing the original's
packaging for the remake, or explicitly scoping T9's readout to
retention-past-3s and saying why. Separately: 153 baseline views is a thin
sample for any curve comparison to clear noise — T9 should state a minimum
sample size before drawing a conclusion either way.

**P4 — B-1's two limbs may leave near-zero B-roll budget.** ≤⅓ runtime,
*and* forbidden on claim/evidence beats, on a claims-discipline channel.
Recommend computing the actual surviving seconds from the K-1 register as
part of T1, before T5 spends anything sourcing plates for a budget that may
not exist.

**P5 — G0-4's free tiers are thinner than they read.**

```
# from prior inventory pass:
# 58 catalog plates total: 35 square, 21 portrait, 2 true 9:16
# none of the centella/PDRN plates is 9:16
```

Options 1–2 of G0-4's precedence may yield close to nothing for a portrait
pilot. Worth stating before the ranking is finalized, since it changes
which option actually governs spend.

**P6 — naming/paths.** Source project is `videos/kbeauty-one-percent-line/`
— already 1080×1920, 115.54s, matching the published 1:56 runtime.
`videos/1-percent-trick-r2/` breaks two repo conventions at once: the
`-r2` suffix has no precedent (`-v2`, `-recut-Ns` do), and it drops the
topic anchor every other slug keeps. `kbeauty-one-percent-line-v2` matches
existing naming exactly. `vo/` as a subpath matches neither the flat layout
(`assets/voice/`) nor the staged layout (`04-assets/`).

**P7 — R-7's invocation.** `npx hyperframes render`, unpinned, matches
neither convention in use: version-pinned `npx --yes hyperframes@X.Y.Z` (in
most `package.json` scripts) or bare `hyperframes` (2 projects, and this
repo's own `CLAUDE.md` flags `npx hyperframes` as silently re-accumulating
large caches). Recommend bare `hyperframes render`, globally installed.

---

## §4 — Gate 0 additions

Three new slots, evidence attached, left unanswered for Kim:

- **G0-6 — `catalog-v2` disposition.** Retire it alongside `sh-*` under
  R-11 (consistent, but discards two days of authored work and its
  ingredient-provenance data model, which nothing else replaces); keep it
  as the ingredient/evidence layer since its `format-contract.json` is data
  and provenance more than presentation (R-11 arguably doesn't reach it);
  or fold its slot-contract shape into the catalog registry T3 builds. See
  B2.

- **G0-7 — compiler path under R-12.** R-12 archives the twelve components
  the compiler and all six templates are built on. Options: rewrite the
  compiler to cast from the catalog registry before T6 runs (correct order,
  adds real scope not currently budgeted anywhere); or keep `sh-*` live
  through T6 and archive only at T7, after the pilot no longer needs it
  (matches current task order, but the pilot then isn't proving the new
  system it's meant to validate). See B1.

- **G0-8 — semantic state tokens.** The token sheet has six tokens and no
  positive/warning/info. Options: extend the sheet with semantic tokens
  (a brand decision, since R-12 makes the token list the brand); or have
  the retrofit reject any catalog item that needs one, shrinking the usable
  catalog. See B3.

Existing slots amended for accuracy rather than answered:

- **G0-1** — mark as "already executed at WO-FVC-005 T7 (0.3.0, merged);
  confirm to close the record, not to authorize a pending change." (C7)
- **G0-2** — reworded to name the this-video→permanent expansion from
  WO-FVC-006's closed Gate 0 explicitly, so it's ruled on as a scope
  expansion rather than read as closing an open question. (C9)
- **G0-3** — corrected to the full 6-token set; Nocturne and pearl-white
  flagged as not live options (no Nocturne sheet exists in the repo; R-13's
  own contrast floor already fails a brass-on-ivory-class pairing). (C8)

---

## §5 — Process hazards

- **The WO itself was untracked** at the start of this review — the exact
  state `CLAUDE.md` names as highest-risk, and the state WO-FVC-006 had to
  be rescued from earlier this morning (09:03). Rescued into
  `session/fvc-007-review` per the documented copy-out-first procedure
  before any git operation touched it.
- **`session/wo-fvc-006-gate0`** is a live worktree whose Gate 0 is fully
  closed with five of Kim's own rulings on record (including the imagery
  reversal and Higgsfield re-authorization). §0 supersedes it; per Kim's
  standing instruction, those closed rulings should be carried forward
  rather than re-asked (reflected in G0-2's rewording above, C9).
- **Six broken symlinks** in `~/.claude/skills` (`faceless-video-craft`,
  `produce`, `video-audit`, `video-package`, `video-readout`,
  `video-render`) after `~/Desktop/claude-skills` was deleted. Out of scope
  for this review; flagged since T7 touches the same skill tree.
- **T0a's "375 items" / "~40 the registry needs"** have no source in this
  repo as far as this review found. Only 5 registry items have ever been
  installed here: `yt-camera-move`, `spring-pop`, `split-tilt-cards`,
  `grid-card-assemble`, `caption-kinetic-slam`. 12 of the 17 component
  names the WO cites (`before-after-wipe`, `mk-specs-list`,
  `svg-stroke-trace`, `hw-frame`, `mk-placeholder-grid`, `yt-lower-third`,
  `logo-outro`, `logo-brand-close`, `cta-close`, `instagram-follow`,
  `tiktok-follow`, `x-post`) appear nowhere in this repo except the WO
  text itself — not a defect in the WO (T0a's own job is to establish the
  real inventory), but worth naming so T0a isn't read as confirming a list
  that was never verified.

---

## What this review does not resolve

Per Kim's instruction, this session reviewed and corrected the WO text; it
did not run T0a or T0b, did not rule on G0-1 through G0-8, and did not
decide `catalog-v2`'s or `session/wo-fvc-006-gate0`'s disposition. Those
remain Kim's calls, recorded above with the evidence attached rather than
answered by assumption.
