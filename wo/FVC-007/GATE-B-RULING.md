# Gate B — ruling (Kim, 2026-09-07)

**Ruling: `svg_diagram` acceptable as-is. Proceed to T5/T6.**

Per the WO's own gate table (`docs/wo/WO-FVC-007-catalog-engine-and-pilot.md`
§4: "Gate B | After T3 | The registry: the component vocabulary the channel
will use for every future video"), `catalog-registry.yaml` — merged from
`session/fvc-007-t3` and `session/fvc-007-t4` at `2361302` — is the
deliverable under review. `wo/FVC-007/T3-REGISTRY-AND-CASTER-REPORT.md`
raised one real open question and one already-closed item:

- **`furniture_lower_third` — already resolved, not open.** Closed by Kim's
  live R-11 ruling during T4 (`wo/FVC-007/T4-FURNITURE-REPORT.md`); T3's
  report only flagged it because a stale trace of the pre-merge gap
  lingered in its own draft. No ruling needed here.
- **`svg_diagram` thinness — the actual ask.** Three registered candidates
  (single-path trace, title reveal, contentless connector) cover a
  narrower job than "diagram" implies for general content. **RULED:
  acceptable as-is.** Not rescoped, not sent upstream for a contribution
  before T6. If T6's real beat sheet hits a diagram job none of the three
  candidates can carry, that surfaces the normal way — `BLOCKER-CAST` at
  cast time, per R-11 — rather than being pre-empted by widening the
  registry against a hypothetical need now.

## Consequence

- Gate B is **CLOSED**. `catalog-registry.yaml` (`purposes:` + `furniture:`,
  merged) is the component vocabulary for this WO, unchanged by this
  ruling.
- T5 (B-roll sourcing) and T6 (pilot build, itself Gate C) may proceed.
  T5's own worktree (`session/fvc-007-t5`) was already in progress before
  this ruling — per T3's own report, its B-roll scaffold doesn't depend on
  the caster's per-beat output, so nothing it already did needs redoing.
- The one live, unresolved technical note from the T3/T4 merge —
  `_yaml_lite.py` silently truncating `>` folded blocks, currently only
  affecting `furniture:`'s own (uncast) notes — is not part of this ruling
  and stays open for whichever task first needs to read `furniture:`
  programmatically through that parser.
