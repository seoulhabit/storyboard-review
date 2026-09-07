# T3 — `catalog-registry.yaml` and the S4.5 caster

**Status: shipped, HALTED AT GATE B.** Per the WO's own gate table
("Gate B | After T3 | The registry: the component vocabulary the channel
will use for every future video"), this session stops here for Kim's
ruling.

**T4 had already run in parallel, out of sequence with the WO's own gate
table — see "Cross-session reconciliation" below before reading anything
else in this report as if T4 were still pending.**

Deliverables:

- [`videos/_system/catalog/catalog-registry.yaml`](../../videos/_system/catalog/catalog-registry.yaml)
  — the registry itself.
- [`~/Desktop/claude-skills-current/makemeavideo/scripts/cast_scenes.py`](/Users/sumitchoudhary/Desktop/claude-skills-current/makemeavideo/scripts/cast_scenes.py)
  — the S4.5 caster (skill repo, `seoulhabit/claude-skills`, not this repo —
  see "Two repos" below).
- [`videos/_system/COMPILER.md`](../../videos/_system/COMPILER.md) §1 —
  documents the new `scene.purpose` field, MANIFEST amended (see below).

---

## Cross-session reconciliation (found mid-task, not part of the original plan)

This repo runs several sessions at once (`CLAUDE.md`'s own standing
warning). Partway through T3, `./worktree.sh status` showed two other live
worktrees already ahead of where the WO's gate table says they should be:

- **`session/fvc-007-t4`** (2 commits) — built its *own*
  `videos/_system/catalog/catalog-registry.yaml`, retrofitted `cta-close`
  and `logo-brand-close`, and **closed the `furniture_lower_third` gap
  with a live Kim ruling** (R-11 option 1 — rewrite the beat: no
  lower-third overlay component exists, so the beat itself becomes a held
  `cta-close` interstitial immediately before the end card, distinct from
  `action_line`'s own use of the same component). T4 is titled
  "channel furniture" in the WO and its own gate table entry
  (`Gate B | After T3`) implies it should not have started before this
  session's registry landed — it started anyway, and structured its own
  file cooperatively: a `furniture:` top-level key, with `purposes:` left
  as an explicit empty placeholder and a comment naming this session by
  branch to fill it in.
- **`session/fvc-007-t5`** (2 commits) — read this session's *in-progress,
  uncommitted* `catalog-registry.yaml` directly off disk (a worktree's
  files are on the same filesystem, so this is possible even with separate
  git checkouts) to confirm `editorial_imagery_broll_wrapper` is the only
  `broll_allowed: true` purpose, then built the G0-3b B-roll style scaffold
  and sourcing-pool draft against that finding. No conflicting file — its
  commits touch `docs/wo/007/broll-manifest.md` and a new
  `broll-style-core-draft.md` only. Left untouched by this session; T5's
  own eventual merge is unaffected by anything below.

**What this session did about it:** merged `session/fvc-007-t4` into this
branch (`git merge --no-ff`, a normal additive merge of their branch into
mine — never touching their branch, worktree, or commits, per `CLAUDE.md`'s
own "prefer merging your own branch over rewriting a shared one") rather
than let both branches land separate, conflicting versions of the same
file on `master`. The one real conflict — both sessions wrote
`catalog-registry.yaml` — resolved by keeping T4's `furniture:` section
verbatim (it carries a real Kim ruling, two real retrofits, and measured
contrast checks — strictly more authoritative than anything this session
could add) and placing this session's `purposes:` list where T4's own
placeholder comment asked for it. **This session's `furniture_end_card` /
`furniture_cta` / `furniture_lower_third` / `furniture_platform_follow`
purpose entries (from the earlier draft of this file, before the merge)
are dropped entirely** — T4's `furniture:` section supersedes them with
real, ruled data, and furniture placement turns out not to be a per-beat
casting problem the way scene content is (fixed placement — final 4s,
penultimate beat — not a ranked pick against beat aspect/content), so it
correctly belongs in its own section the S4.5 caster never reads, not
folded into `purposes:` as this session originally modeled it. `cta-close`,
`logo-brand-close`, their retrofit output, and `retrofit_catalog.py`'s new
`TOKEN_BRIDGE_MAP`/`INTERNAL_VARS` entries (both files, from T4) are now
part of this branch's history via the merge.

**One consequence for the rest of this report:** everywhere below that
still reads as if `furniture_lower_third` is an open Gate B question, that
reflects this session's registry *before* discovering T4 had already run
and Kim had already ruled on it live. It is not still open. The "Gate B —
halting for Kim's ruling" section at the end has been corrected; the
body above it has not been rewritten scene-by-scene to match, since the
corrected registry file itself (not this prose) is the source of truth
going forward.

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

**Purpose grouping** (the four scene systems + B-roll wrapper — furniture
is T4's own `furniture:` section, a different shape, not `purposes:`
entries — see "Cross-session reconciliation" above):

| Purpose | Candidates | broll_allowed |
|---|---|---|
| `claim_vs_evidence` | 6 (comparison-split, before-after-wipe, split-tilt-cards, chart-story, decline-chart, count-up) | false |
| `svg_diagram` | 3 (svg-stroke-trace, svg-mask-reveal, svg-line-draw-loader) | false |
| `checklist` | 2 (marker-checklist-card, grid-card-assemble) | false |
| `editorial_imagery_broll_wrapper` | 5 (push-in, yt-camera-move, device-frame-stage, grade-split-reveal, grain-overlay) | true |

16 candidate entries total across 4 purposes, drawn from the 19 verified
components (`device-frame-stage` is one of them, under
`editorial_imagery_broll_wrapper`). Separately, T4's `furniture:` section
covers `end_card` (`logo-brand-close`), `action_line` (`cta-close`),
`lower_third_subscribe` (resolved onto `cta-close` too, via a live R-11
ruling — see below), and `platform_follow` (left unassigned, per T4's own
scope).

## The furniture gap is already resolved — by T4, live, not by this session

An earlier draft of this registry (before this session discovered T4 had
already run — see "Cross-session reconciliation" above) modeled
`furniture_lower_third` as a `purposes:` entry with zero candidates and
flagged it as an open Gate B question, carrying forward
`wo/FVC-007/GATE-A-RULING.md`'s own "known consequence" note: every
lower-third match in the full 383-item catalog is a `hyperframes:block`
(`yt-lower-third`, `lt-dark-card`, `lt-kicker-name`, the rest of the
`lt-*` family), out of scope after Gate A restricted the registry to
components.

**That's no longer accurate.** T4 ran the R-11 resolution live and Kim
ruled option 1 (rewrite the beat): no lower-third component exists, so the
beat itself stops being a persistent overlay and becomes a held,
full-frame `cta-close` interstitial placed immediately before the end
card — the same component `action_line` uses, with a recorded
`conflicts_with`/`conflict_note` in the registry's `furniture:` section
so a beat sheet never tries to use `cta-close` for both roles in one
video. This is in the merged registry now, not still open.

`platform_follow` remains genuinely unassigned, but that was always T4's
own stated scope ("retrofit but leave unassigned; cross-promo is a
per-video call") — not a blocking gap, and not something this session's
merge changes.

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

5 of the 19 registry candidates have actually been run through
`retrofit_catalog.py`: T2's own 3-item test suite (`focus-swap`,
`caption-highlight`, `device-frame-stage`) plus T4's two furniture
retrofits (`cta-close`, `logo-brand-close`, picked up by this session's
merge — see "Cross-session reconciliation"). The registry's
`retrofitted: false` field is literal for the other 14 `purposes:`
candidates, not a placeholder default. Per R-14, an item is never consumed
raw regardless of what the registry ranks it — running the retrofit on a
candidate before it's used in a real build is T5/T6's job ("future catalog
additions cost minutes," per T2's own report), not speculative work
against all 14 here. This is a deliberate scope boundary, not an
oversight — retrofitting components nobody ends up casting for the pilot
would be wasted work against a registry that's itself still subject to
Kim's Gate B ruling.

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
`catalog-registry.yaml` is — merged, now, with T4's `furniture:` section.
Flagging, not deciding, what's actually still open:

- **The furniture gap is already resolved, by Kim, in the parallel T4
  session — not still open.** See "Cross-session reconciliation" and "The
  furniture gap is already resolved" above. Nothing to rule on here; T4
  has already closed.
- **`svg_diagram` is registered but thin — this is the one real open
  question.** Its three candidates cover a narrower job (single-path
  trace, title reveal, contentless connector) than "diagram" implies.
  Worth deciding now whether that's acceptable for this channel's actual
  content mix, or whether it's worth an upstream contribution before T6
  rather than after a real `BLOCKER-CAST` forces the question mid-build.
- **Process note, not a registry question:** T4 and T5 both started before
  this session's Gate B halt would normally have cleared them to. Nothing
  in either session's actual work looks wrong for it (T4's registry
  section was built defensively, cooperatively, and correctly anticipated
  this merge; T5's B-roll scaffold doesn't depend on the caster's per-beat
  output). Worth deciding, going forward, whether this WO's gate table
  should be read as a hard sequential block or as guidance sessions can
  route around when they can show their own work doesn't depend on the
  gated deliverable — this session took no position and just reconciled
  what happened.

T4 is done. T5 is in progress on its own branch, unaffected by this merge.
The `svg_diagram` thinness is the one item this session is actually
raising for Kim's Gate B ruling.
