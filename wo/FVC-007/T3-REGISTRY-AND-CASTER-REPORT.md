# T3 — `catalog-registry.yaml` and the S4.5 caster

**Status: shipped, HALTED AT GATE B.** Per the WO's own gate table
("Gate B | After T3 | The registry: the component vocabulary the channel
will use for every future video"), this session stops here for Kim's
ruling. T4 (channel furniture) has not started.

Deliverables:

- [`videos/_system/catalog/catalog-registry.yaml`](../../videos/_system/catalog/catalog-registry.yaml)
  — the registry itself.
- [`~/Desktop/claude-skills-current/makemeavideo/scripts/cast_scenes.py`](/Users/sumitchoudhary/Desktop/claude-skills-current/makemeavideo/scripts/cast_scenes.py)
  — the S4.5 caster (skill repo, `seoulhabit/claude-skills`, not this repo —
  see "Two repos" below).
- [`videos/_system/COMPILER.md`](../../videos/_system/COMPILER.md) §1 —
  documents the new `scene.purpose` field, MANIFEST amended (see below).

---

## Two repos, one task

`catalog-registry.yaml` is data and lives in `videos/_system/catalog/` in
*this* repo, per R-14. The S4.5 caster is code, and the compiler it feeds
(`compile_composition.py`) lives in the skill package, `~/Desktop/claude-
skills-current` (remote `seoulhabit/claude-skills`) — a **separate git
repo**, not a subdirectory of this one. `cast_scenes.py` was written and
committed there, on its own branch, not in this repo's worktree. This
split is not a new decision — `videos/_system/COMPILER.md` and
`compile_composition.py` already existed on that side before this WO, T3
just adds a sibling script next to `beats_to_build_spec.py`.

## Registry: what's real, what's curated, what's excluded

**Every candidate is grounded in three real sources**, cross-checked
against each other, not asserted from one:

1. `docs/wo/007/catalog-inventory.json` (T0a) — the 383-item inventory and
   the 36-item T0b working set with real aspect verdicts.
2. `vendor/hyperframes/registry/components/<name>/registry-item.json` at
   the pinned commit (`0d5d3f3`) — re-cloned this session (same commit
   T0a recorded; the clone itself doesn't survive between worktrees since
   it's gitignored per R-14, so it's legitimate, cheap, and necessary to
   re-clone at the identical SHA to read real variable schemas rather than
   re-deriving them from `catalog-inventory.json`'s coarser
   `content_slots` list, which — confirmed by reading the actual JSON —
   has no `role`/`type` distinction at all).
3. The item's own HTML, read directly for the handful of cases where
   `registry-item.json` declares zero variables (`animated-bar-chart`,
   `yt-camera-move`, `grain-overlay`, `svg-line-draw-loader`) or where a
   declared slot doesn't tell the whole story (`before-after-wipe` hosts
   real `img`/`video` children per its own HTML comments; that's not in
   any `variables[]` array anywhere upstream).

**Only the 19 T0b-verified components are candidates.** Not the full
219-component catalog. T0-GATE-A-REPORT.md's own words: "If T3's later
curation reaches outside this 36-item set, those additions need their own
aspect check before being trusted." None do here. This is a real
constraint on the registry's breadth, not a corner cut — widening it later
means re-running T0b's render-probe method on the new candidate first, not
adding it because its tags/name look right.

**`animated-bar-chart` is excluded entirely**, not just deprioritized.
Read its HTML: header title, `+42%` value, all seven bar heights, and the
SVG path are hardcoded literals with zero `data-var-*` binding points — a
demo/preview card, not a beat-fillable component under R-9's "casting is
data" model. Including it would have meant either fabricating a slot
contract that doesn't exist or leaving the registry's own discipline
(every candidate has a real, checked slot list) with a silent exception.
`chart-story`, `decline-chart`, and `count-up` already cover the
claim_vs_evidence chart/stat need with real, declared slots.

**Purpose grouping** (four scene systems + B-roll wrapper + two of T4's
four furniture roles — the WO's own stated coverage):

| Purpose | Candidates | broll_allowed |
|---|---|---|
| `claim_vs_evidence` | 6 (comparison-split, before-after-wipe, split-tilt-cards, chart-story, decline-chart, count-up) | false |
| `svg_diagram` | 3 (svg-stroke-trace, svg-mask-reveal, svg-line-draw-loader) | false |
| `checklist` | 2 (marker-checklist-card, grid-card-assemble) | false |
| `editorial_imagery_broll_wrapper` | 5 (push-in, yt-camera-move, device-frame-stage, grade-split-reveal, grain-overlay) | true |
| `furniture_end_card` | 1 (logo-brand-close) | false |
| `furniture_cta` | 1 (cta-close) | false |
| `furniture_lower_third` | 0 — gap, see below | false |
| `furniture_platform_follow` | 0 — gap, see below | false |

18 candidate entries total across 8 purposes, drawn from the 19 verified
components (`device-frame-stage` is the 19th; it appears once, under
`editorial_imagery_broll_wrapper`).

## The two furniture gaps are carried forward, not newly found

`furniture_lower_third` and `furniture_platform_follow` have zero
candidates. This is not a new discovery — `wo/FVC-007/GATE-A-RULING.md`'s
own "Known consequence" section already named it: every lower-third match
in the full 383-item catalog is a `hyperframes:block`
(`yt-lower-third`, `lt-dark-card`, `lt-kicker-name`, the rest of the
`lt-*` family), out of scope after Gate A restricted the registry to
components. Same for `instagram-follow`/`tiktok-follow`. T3's registry
just makes the gap machine-readable (an empty `candidates: []` the caster
can actually halt on) instead of leaving it as prose in a ruling doc.
`furniture_lower_third` blocks T4 the way Gate A predicted;
`furniture_platform_follow` doesn't, since T4 leaves that role unassigned
regardless (cross-promo is a per-video call).

## A gap this session found, not carried forward: `svg_diagram` is thin

None of the 19 verified components is a true multi-node/edge diagram. The
three `svg_diagram` candidates are a single-path tracer, a wordmark-reveal
effect wrongly adjacent to "diagram" by tag only, and a contentless motion
primitive. The catalog's real diagram items — `flowchart`,
`flowchart-vertical`, `data-chart` — are all blocks, excluded by Gate A,
and `flowchart-vertical` specifically **failed its own T0b reframe despite
matching aspect ratio** (1440×2560 = 1080×1920's ratio exactly, still 6
off-canvas elements — per T0-GATE-A-REPORT.md, absolute-pixel authoring at
the wrong native width breaks the same way a 1920-wide block does, aspect
match alone doesn't save it). A beat that genuinely needs a structural
diagram will likely hit `BLOCKER-CAST` even though the purpose has
non-empty candidates — recorded in the registry's own `_gaps` block, not
silently left to surface mid-beat at T6.

## The caster: what it does, what it deliberately doesn't

`cast_scenes.py` implements exactly the WO's own spec: filter by output
aspect and `broll_allowed`, pick the highest-ranked candidate the beat can
fill, ledger every pick and every rejection with a reason, halt
`BLOCKER-CAST:<scene_id>` with no fallback when nothing clears.

Two design decisions worth stating rather than leaving implicit:

- **`scene.purpose` is a new required field for any scene going through
  S4.5 — never inferred from `intent`/`layout` prose.** This is the same
  "fail loudly, never guess" discipline T2's colour mapper already
  established for this WO. A scene's purpose is an authoring decision
  (what job is this beat doing), not a text-classification problem for
  S4.5 to solve by keyword-matching a caption. It's declared alongside
  `beats_to_build_spec.py`'s existing `beat-sheet.schema.json`, following
  the exact precedent `COMPILER.md` already set for `scene.component`/
  `scene.slots` — a compiler/caster-only optional field the frozen schema
  doesn't declare, documented in `COMPILER.md` rather than editing the
  shared schema file.
- **B-1's two limbs are both enforced, and their interaction is checked,
  not assumed non-contradictory.** A purpose's own `broll_allowed` flag is
  one gate; a scene's claim-table match (reusing `beats_to_build_spec.py`'s
  own `parse_claim_table`/`beat_text`/`normalize` — imported, not
  reimplemented) is the other. If a scene is claim-marked *and* its
  declared purpose allows B-roll, that's a real authoring contradiction —
  the caster halts and names it rather than picking a side.

**Tested, not just written to run once:**

- Registry syntax: round-tripped through `_yaml_lite.parse_yaml_subset`
  (the actual shared parser both this script and `beats_to_build_spec.py`
  use) before committing. Caught a real bug this way — every `note`/
  `summary`/`resolution` field was first drafted as a YAML folded (`>`)
  block scalar, which `_yaml_lite` doesn't support (documented in its own
  module docstring); it silently truncated every multi-line note to the
  literal string `">"`. Fixed by converting every one to a single-line
  quoted string and re-verifying the full parse, not just the fields that
  looked short enough to have been safe.
- Five scenarios run end-to-end against synthetic beat sheets: (1) a clean
  cast (claim-marked scene → `comparison-split`, ledgered with its
  `claim_ids`), (2) missing `purpose` → `BLOCKER-CAST`, (3) the B-1
  contradiction (broll-purpose scene matching a claim) → `BLOCKER-CAST`,
  (4) `furniture_lower_third`'s empty-candidate gap → `BLOCKER-CAST`, (5)
  the rank-cascade fallback: a scene with empty VO/caption/intent text
  correctly skips `svg-stroke-trace` (needs `path`) and `svg-mask-reveal`
  (needs `text`+`revealProgress`), landing on `svg-line-draw-loader` (zero
  content slots) with both rejections ledgered and reasoned.

**What it does not do, stated rather than assumed solved:**

- **Does not populate real slot values.** Output `slots` is a
  `{slot_name: null}` skeleton — the real names, so H-1 knows exactly what
  to fill — not text pulled from the beat. Binding beat content to a
  specific component's specific slots by role is T7's own scoped item
  ("H-1 needs to generate against the catalog registry specifically —
  genuinely new").
- **Does not touch `compile_composition.py`, and that script cannot yet
  render what this caster picks.** Read the source directly:
  `CANONICAL_COMPONENTS` gate at `compile_composition.py:255-256` calls
  `die()` on any `scene.component` value outside the twelve `Sh*` names.
  A beat sheet this script casts against the catalog registry will **not**
  compile against the installed compiler today. This is the concrete,
  checked version of G0-7's own flagged prerequisite — "confirming the
  compiler's catalog-registry casting path... is real before T6 is
  attempted" — and it is **not yet real**. Extending or bypassing that
  gate is separate compiler work, not scoped to T3, and needs to happen
  before T6 can literally cast-and-render a scene.
- **"Can fill" is presence-of-text, not per-slot content matching.** A
  2-word caption technically "fills" `marker-checklist-card`'s 10 slots by
  this script's own check. A real per-slot match is the same T7 H-1 work
  named above; this check exists only to stop an obviously-content-empty
  scene from picking a content-heavy candidate over a same-purpose lighter
  one, not to guarantee good content fit.

## `videos/_system/` amendment (R-14/R-6 precedent)

`COMPILER.md` §1 gained the `scene.purpose` documentation above.
`MANIFEST.json` re-hashed and amended (67/67 tracked files re-verified
clean — `check_manifest()` passes) with a fourth `amendments[]` entry,
following the same convention T2's G0-8 token addition and the two prior
entries (`R-6` safe-area, `--muted` contrast fix) already used.

## Retrofit status — real, not glossed over

Only 3 of the 19 registry candidates (`focus-swap`, `caption-highlight`,
`device-frame-stage`) have actually been run through `retrofit_catalog.py`
— T2's own 3-item test suite. The registry's `retrofitted: false` field is
literal for the other 16, not a placeholder default. Per R-14, an item is
never consumed raw regardless of what the registry ranks it — running the
retrofit on a candidate before it's used in a real build is T5/T6's job
("future catalog additions cost minutes," per T2's own report), not
speculative work against all 16 here. This is a deliberate scope boundary,
not an oversight — retrofitting components nobody ends up casting for the
pilot would be wasted work against a registry that's itself still subject
to Kim's Gate B ruling.

## An incidental finding, flagged not fixed

`COMPILER.md` §1's third bullet still reads "currently unused — the design
system forbids imagery by rule" for `videos/<slug>/04-assets/`'s plate
input. That's stale against G0-2 (imagery permitted channel-wide as B-roll
now, ruled at this WO's own Gate 0) — a leftover from the pre-WO-FVC-007
compiler doc. Not fixed here: it's outside T3's scope (registry + caster),
touching it would be a second, unrelated `MANIFEST.json` amendment in the
same commit, and T5/T6 will need to update that line for real once B-roll
plates actually flow through `04-assets/` — better done with real sourcing
data in hand than as a word-swap now.

## Gate B — halting for Kim's ruling

Per the WO's own gate table: Gate B is "the registry: the component
vocabulary the channel will use for every future video." That's what
`catalog-registry.yaml` is. Flagging, not deciding, the two things Kim's
ruling should weigh:

- **The furniture gap is real and blocks T4 as drafted.** `furniture_
  lower_third` has zero candidates. R-11's two options apply: rewrite
  every video's beat sheet to carry no lower-third furniture, or
  contribute a component-category lower-third upstream and consume it
  back through the retrofit path. Neither is decided here.
- **`svg_diagram` is registered but thin.** Its three candidates cover a
  narrower job (single-path trace, title reveal, contentless connector)
  than "diagram" implies. Worth deciding now whether that's acceptable for
  this channel's actual content mix, or whether it's worth an upstream
  contribution before T6 rather than after a real `BLOCKER-CAST` forces
  the question mid-build.

T4 does not start until Kim rules here.
