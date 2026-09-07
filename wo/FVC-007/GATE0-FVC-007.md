# Gate 0 — WO-FVC-007 answer sheet

Status: **ANSWERED (Kim, 2026-09-07).** All nine slots are closed — one
already executed at WO-FVC-005 (G0-1), one already answered in the WO's own
09:46 revision (G0-5), and seven ruled directly by Kim this session
(G0-2, G0-3, G0-3b, G0-4, G0-6, G0-7, G0-8). `approved`.

Two of these rulings deliberately expand scope beyond what was previously
ruled elsewhere — flagged explicitly below per this repo's own convention
that a supersession or expansion is recorded, not silently adopted.

Full evidence for every finding referenced below is in `wo/FVC-007/REVIEW.md`.

---

## Already resolved — no ruling needed

▸ **G0-1 — Engine reversal.** **CLOSED**, already executed. `makemeavideo`
0.3.0 shipped at WO-FVC-005 T7, merged to `origin/master`: zero
`*video_agent*` calls outside the forbidden-tool fence. This slot confirms
the record.

▸ **G0-5 — `sh-*` retirement.** **CLOSED**, answered in the WO's own
09:46 2026-09-07 revision, before this Gate 0 pass. The bespoke `sh-*`
component library is retired; the design system is demoted to foundations
only. See R-12.

---

## Ruled directly by Kim, this session (2026-09-07)

▸ **G0-2 — Imagery lane.** **RULED: permanent, channel-wide, as drafted.**

Photographic and generated imagery is permitted in compositions as B-roll,
for every future video, not only this pilot.

**This is a scope expansion, recorded as such:** WO-FVC-006's own closed
Gate 0 (`wo/FVC-006/GATE0-FVC-006.md`, 09:03 today) ruled full imagery for
that one video only — *"Scope: this video only… unless Kim rules broader."*
This ruling is that broader call. The design-system rule this reverses
(`videos/_system/COMPILER.md`: "the design system forbids imagery by rule")
now no longer holds for any video, not just Credibility Gap.

▸ **G0-3 — UI/component token sheet.** **RULED: the existing six-token
sheet — cream `#F4EDE3` / bg-lift `#FAF3E7` / ink `#26215C` / clay `#9C3A32`
/ brass `#C0A265` / muted `rgba(38,33,92,0.75)`.**

This confirms what WO-FVC-005 G0-8 and WO-FVC-006's own G0-1 already ruled
— *"ship cream/ink/clay/brass… the same palette already live in the
`centella-asiatica` pilot render… no Nocturne sheet exists anywhere in this
repo."* No new palette is built. Note the `--muted` value is `0.75`, not
the `0.55` this WO's draft cited — amended 2026-09-07 by the PDRN pilot
(`1aeccba`, endcard contrast fix) after a real H-4.contrast failure;
confirm against `videos/_system/tokens/colors.css` directly before citing
this value elsewhere, since it is now a second amendment on the same file.

**Correction on the record:** this WO's draft G0-3 listed "the pearl-white
/ blush / clinical-blue direction from WO-FVC-006" as a third *competing UI
palette*. It is not one — see G0-3b.

▸ **G0-3b — B-roll photographic art direction. (New this session, split
out of G0-3's conflation.)** **RULED: the pearl-white / soft blush /
restrained clinical-blue art-direction spec (WO-FVC-006 §3.4 — "editorial
medical-beauty still… physically plausible materials… shallow depth of
field…") extends channel-wide to every video's generated B-roll,
consistent with G0-2.**

This governs *what generated photographs look like*, not the UI token
sheet — a different system from G0-3, wrongly merged into one slot in the
WO's draft. Previously scoped to Credibility Gap's plates only
(`wo/FVC-006/GATE0-FVC-006.md` G0-2); this ruling extends that same visual
treatment to any B-roll this WO's own T5 or any future video generates via
Higgsfield. Applies to *generated* imagery only — extracted frames and
existing catalog plates are not re-shot to match it.

▸ **G0-4 — B-roll source precedence.** **RULED: keep the ranking as
drafted** — existing plates, then extracted `cGbokt_B_vE` frames, then
Higgsfield `nano_banana_pro` (under G0-3b's art direction), then
`vidiq_generate_broll` stock. Confirmed knowing the first two tiers cover
very little true 9:16 inventory (2 of 58 catalog plates) — T5 exhausts them
quickly at no cost and falls through to Higgsfield rather than skipping
ahead.

▸ **G0-6 — `catalog-v2` disposition.** **RULED: retire entirely, alongside
`sh-*`.**

The 4 ingredient packs (centella-cica, snail-mucin, PDRN, collagen — their
evidence records, provenance, approved/restricted asset tracking) and the
14 authored story-system components (`label-literacy`, `ingredient-fate`)
are archived together, not split. R-11 now applies without an unstated
carve-out for `catalog-v2`. See T7 for the archiving mechanics, added
alongside the `sh-*` move.

**Consequence, not yet resolved:** `catalog-v2`'s ingredient-evidence model
(citation IDs, approved/restricted status per asset) has no direct
replacement named in this WO. Claim sourcing still runs through K-1/R-3 (the
pinned website source) independently of `catalog-v2`, so this does not block
the catalog engine — but any future video that leaned on `catalog-v2`'s
provenance tracking specifically will need that need re-stated once
`catalog-v2` is gone. Not scoped here; flag if it recurs.

▸ **G0-7 — Compiler path under R-12.** **RULED: keep `sh-*` live through
T6, archive at T7.**

**Reading adopted, stated explicitly since the literal answer supports more
than one implementation:** `sh-*` stays on disk and importable through T6 —
`check_manifest()` never fires `BLOCKER-SYSTEM` mid-pipeline, since nothing
is moved to `_archive/` before Gate C. The compiler still gains
catalog-registry casting support as T3 already scopes (T6's own text: "cast
by S4.5 from the retrofitted library"), and casts primarily from the
catalog registry; `sh-*` remains available as an explicit fallback for any
beat the registry doesn't yet cover, not as the pilot's primary path.
Physical archiving — the move to `videos/_system/_archive/` — happens only
at T7, once Gate C has passed and no composition still references an
`sh-*` component.

**Why this reading, not the narrower one:** the alternative reading — T6
built entirely on the existing `sh-*` compiler, catalog-registry casting
left unproven until after Gate C — would mean the pilot doesn't exercise
the visual system this WO exists to build, undercutting R-10's own premise
("Only the visual system changes… any delta is attributable to the visual
system"). If that narrower reading was actually intended, say so before T2
starts — it changes what T9's readout can honestly claim.

▸ **G0-8 — Semantic state tokens.** **RULED: extend the token sheet now.**

`videos/_system/tokens/colors.css` gains `positive`/`warning`/`info`
tokens as part of this WO. **Not yet specified: the actual hex/rgba
values.** That is real design-system work — picking colours, checking them
against R-13's 4.5:1 contrast floor on the current cream background,
re-hashing `MANIFEST.json` with an `amendments[]` entry per the R-6/R-14
precedent — and belongs inside **T2** (the Opus/High retrofit task), not
this ruling pass. T2's spec is amended to carry this as an explicit first
sub-step, ahead of the recolour-mapping work that depends on it.

---

## Sequencing after this Gate 0 close

T0a and T0b may now start. G0-7's ruling means T2 is not blocked waiting on
a compiler rewrite — but T2 itself now carries two prerequisites before its
recolour-mapping step can run: the G0-8 token additions above, and
confirming the compiler's catalog-registry casting path (needed for T6 to
cast primarily from the registry, per G0-7) is real before T6 is attempted.
Neither changes T0a/T0b's own scope.
