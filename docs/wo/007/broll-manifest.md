# T5 — B-roll sourcing manifest

**Status: sourcing-pool draft, not final assignment.** T5 works G0-4's
precedence — existing plates → extracted `cGbokt_B_vE` frames → Higgsfield
(under G0-3b) → `vidiq_generate_broll` stock — "for each B-roll slot the
caster opened." T3 (`catalog-registry.yaml` + the S4.5 caster, Gate B) is
running in a parallel session and has not merged as of this pass, so no
beat carries a `BLOCKER-CAST` or a filled slot yet. This document is the
sourcing-pool inventory that lets slot-filling be fast once T3 lands: what
exists, what it costs (already spent vs. still to spend), its licence, and
its B-1 compliance — tier by tier, per G0-4.

Nothing below is wired into `videos/kbeauty-one-percent-line-v2/` yet. That
wiring is T6, after T3's Gate B.

---

## Tier 1 — existing plates (free, zero-cost, per G0-4/T5: "exhausts them
at no cost before falling through")

### `catalog/product-photography/` — 12 stills, cost: $0 (already generated,
committed to the repo)

The strongest tier-1 candidate pool found. Per `catalog/product-photography/README.md`
and `catalog/manifest.json`: fictional/unbranded K-beauty packaging, **generated
via Higgsfield (`nano_banana_pro`)**, verified on rendered pixels for
`claim_check` / `brand_check` / `face_check`, not `claim_check`-adjacent
guesswork. Licence: none needed — first-party generated asset, not licensed
stock.

| Scene | File | Aspect | Depicts | B-1 face check | B-1 claim check | B-1 brand check |
|---|---|---|---|---|---|---|
| A01 | A01-01.png | 9:16 | Frosted glass dropper bottle | pass (no face) | pass (nominal label only) | pass (unbranded) |
| A02 | A02-01.png | 9:16 | Airless pump + refill cartridge | pass | pass | pass |
| A03 | A03-01.png | 9:16 | Hinged toner-pad jar | pass | pass | pass |
| A04 | A04-01.png | 9:16 | Clear tube, gel visible | pass | pass | pass |
| A05 | A05-01.png | 9:16 | Glass vessel + refill sachet | pass | pass | pass |
| A06 | A06-01.png | 9:16 | Open cushion compact | pass | pass | pass |
| B01 | B01-01.png | 9:16 | Droplet on glass (texture macro) | pass | pass | pass |
| B02 | B02-01.png | 9:16 | Whipped-cream swirl (texture macro) | pass | pass | pass |
| B03 | B03-01.png | 9:16 | Balm mid-melt (texture macro) | pass | pass | pass |
| C01 | C01-01.png | **16:9** | Six-product shelf lineup | pass | pass | pass |
| C02 | C02-01.png | 9:16 | Hand dispensing (cropped at wrist) | pass | pass | pass |
| C03 | C03-01.png | **16:9** | Overhead flat-lay, 4 products | pass | pass | pass |

10 of 12 are native 9:16 — no reframe needed for the pilot. All 12 pass B-1's
face/claim/brand bars as shipped; the two 16:9 stills (C01, C03) would need
either a portrait crop (loses the lineup framing) or a role as a long-form
B-roll asset, not this Short.

**Not yet checked here: camera-move wrapping (B-1's "no still-on-still-background"
rule) and the one-third runtime cap** — both are T6/T3 concerns (the caster
picks a camera-move wrapper component per slot; the cap is measured across
the whole assembled composition, not per-plate). Flagging so T3/T6 don't
read this table's "pass" column as covering those two rules.

**Palette note:** this set's own `style-core.md` (paper white / mist grey /
celadon / ink / one muted aqua accent) predates and differs from G0-3b's
ruled art direction (pearl-white / soft blush / restrained clinical-blue).
Per G0-3b's own text — *"Applies to generated imagery only — extracted
frames and existing catalog plates are not re-shot to match it"* — this
does not disqualify the set: it is an existing catalog plate under G0-4's
tier 1, not new tier-3 generation, so it is not held to G0-3b's palette.
Recorded so a later reviewer doesn't flag the aqua/celadon accent as a
G0-3b violation — it predates that ruling and is exempt by its own text.

### `catalog/ingredient-photography/` — 30 stills, cost: $0

20-item numbered set (`01-aha-bha.png` … `20-vitamin-c.png`, 2048×2048)
plus 4 `sh-*` identity-slot additions (2048×2048) plus 2 snail-mucin
alternates (`12c`–`12f`, 896×1200) plus the original `12`/`12b` (2048×2048).
All square or near-square — **none are native 9:16**. A 2048×2048 square
center-cropped to 9:16 keeps only the middle ~56% of width; whether that
survives per-ingredient (most are flat-lay single-object shots, likely
tolerant of a crop; a few may not be) is an aspect-survivability question
in T0b's own spirit, not decided here. Relevant only if a beat needs a
named-ingredient plate specifically (ginseng, mugwort, snail mucin — all
three also appear in `kbeauty-one-percent-line/assets/images/`, see below)
rather than generic packaging/texture B-roll, which `product-photography`
already covers in native portrait.

### `catalog/skin-macro-photography/` — 4 stills, cost: $0

`01-pilling-macro.png`, `02-layering-hand.png`, `03-flaking-skin.png`,
`04-base-skin.png` — all 1200×1200 square. Harvested from
`pilling-vs-peeling`'s 2026-09-01 recut per this folder's README. Same
square-crop caveat as ingredient-photography. Topically about
pilling/layering/flaking — not an obvious fit for the "1% trick" pilot's
likely beats (labeling-claim deception, not texture demonstration), but
recorded for completeness since G0-4 says exhaust tier 1 fully before
falling through.

### `videos/kbeauty-one-percent-line/assets/images/` — 6 stills, cost: $0
(already spent, original video)

| File | Size | Note |
|---|---|---|
| `hook-bottle-photo.png` | 1080×1935 | Near-9:16 (off by 15px vs. 1080×1920), from the original render |
| `ingredient-ginseng.png` | 1400×1400 | square |
| `ingredient-mugwort.png` | 1400×1400 | square |
| `ingredient-snail-mucin.png` | 1400×1400 | square |
| `loop-centella-leaf.png` | 700×700 | square, small |
| `loop-water-droplet.png` | 700×700 | square, small |

**Flag, not a ruling:** these are the *original* `cGbokt_B_vE`'s own source
images. R-10 frames the pilot as a single-variable experiment — "only the
visual system changes." Reusing these verbatim as B-roll in the v2 build is
defensible (T1 item 1 explicitly directs sweeping "already-rendered plates
from the centella and PDRN runs," and this project *is* the pilot source,
not a different run) but it's close enough to R-10's boundary that T6/Gate C
should say explicitly whether any of these six were reused, so the readout
(T9) can account for it if asked.

**Update: T1 has now run** (`session/fvc-007-t1`, merged into this branch —
see `wo/FVC-007/T1-ASSET-SWEEP-REPORT.md` and `docs/wo/007/asset-inventory.md`).
It confirms and extends the manual sweep above:

- **New tier-1 stills**, all from `videos/centella-cica-vs-snail-mucin/assets/images/`:
  `f1-palette.png`, `f2-string-start.png`, `f3-dropper-start.png` (native
  9:16, 1536×2752 — same dimensions as `catalog/product-photography`'s set),
  `twist-cream-swirl.png` (781×1400, near-9:16), and two square stills
  (`twist-centella-leaf.png`, `cta-snail-pour.png`) pending a reframe call.
  All five/six clear B-1 (no face, no brand, no baked-in text) by direct
  visual inspection.
- **A real footage pool with a licence flag, not a clean tier-1 source**:
  `videos/centella-tiger-grass/assets/plates/` — 14 clips, native 9:16,
  confirmed by frame-sampling to be real wildlife/nature footage (not
  generated). Content clears B-1 but the project has no README, manifest, or
  licence note anywhere — T1 flags this as **unconfirmed provenance, do not
  cast until resolved**, unlike the Higgsfield-generated catalog plates
  which are provably first-party and free.
- **Tier 2 (extracted `cGbokt_B_vE` frames) is confirmed empty, not thin.**
  T1 extracted and visually graded 9 frames (one per scene) from the actual
  render: 0 are usable raw B-roll — every frame is either pure typography or
  a design-system card with claim text baked into the same pixels as any
  photography underneath. This updates tier 2's entry below from "not done"
  to "done, zero yield."

The five other centella/madecassoside/pdrn projects T1 checked turned out
audio-only — no further tier-1 stills expected from that family beyond what's
recorded here and in the manual sweep above.

---

## Tier 2 — extracted `cGbokt_B_vE` frames

**Done, zero yield.** T1 extracted 9 frames (one per scene) from the actual
rendered MP4 and visually graded each: every one is either pure typography
or a design-system card with claim/label text baked into the same pixels as
any photography underneath (see `wo/FVC-007/T1-ASSET-SWEEP-REPORT.md` §2).
This tier contributes nothing to the sourcing pool — stronger than "thin,"
it's empty for this pilot. One overlap noted: the 04b scene's ginseng-root
photo is the same source image already available clean, without card
chrome, as `videos/kbeauty-one-percent-line/assets/images/ingredient-ginseng.png`
— already in tier 1, so nothing is lost by tier 2 being empty.

---

## Tier 3 — Higgsfield generation under G0-3b

**Finding: the ~100-image generation history already in this workspace's
Higgsfield/nano-banana media library does not qualify as G0-3b-compliant
tier-3 B-roll, and none of it is proposed for use here.**

Reviewed via `show_generations` (type=image, ~100 items spanning
2026-09-05 through 2026-09-07). The pool breaks into three groups, none of
which clear the bar:

1. **A propolis/amber/honeycomb ingredient narrative** (thorn sealed in
   amber, bees working resin onto bark, a mouse decaying vs. one preserved
   in amber, amber "shield" cross-sections of skin) — the large majority of
   the pool. This reads as B-roll for a different ingredient story (propolis
   or a PDRN-adjacent "preservation" metaphor), not this pilot's "1% trick"
   labeling-claims Short. Palette is warm amber/gold on near-black or dark
   charcoal — the opposite of G0-3b's pearl-white/blush/clinical-blue
   direction. Aspect is mixed (mostly 16:9, some 9:16).
2. **Face-forward portraits** (a dermatologist finger-to-lips "shh" gesture,
   a smiling woman with "radiant glowing skin," a doctor nodding
   reassuringly, a woman touching a melasma patch in a mirror) — these fail
   B-1's "no faces in frame" rule outright, regardless of aspect or palette.
3. **A small `cinematic_studio_2_5` batch, 2026-09-05, native 9:16** (hand
   holding a bottle "no face visible," cream being scooped, hands being
   sanitized in a clinical setting, a droplet on skin) — the closest
   structural match to what B-1/G0-3b actually want (no faces, portrait,
   product/texture macro), but still off-palette: "dark charcoal
   background," "crimson and deep red gel lighting," "cool clinical
   fluorescent" — not pearl-white/blush/clinical-blue.

None of the three groups is recommended for this pilot's B-roll. Group 1 is
off-topic and off-brief; group 2 is a hard B-1 violation; group 3 is
on-structure but off-palette, and reskinning an already-generated image
after the fact isn't how G0-3b's spec gets satisfied — it has to be the
generation prompt.

**Consequence:** tier 3, when actually reached, still needs fresh
generation against G0-3b's spec (pearl-white seamless environment, soft
blush bounce light, restrained clinical-blue rim, physically plausible
materials, shallow depth of field, no lettering/logos/UI/watermarks) —
written the way `catalog/product-photography/prompts/style-core.md` writes
its own shared look, so it can be reused per-scene the same way. That
prompt work is not done here because it depends on knowing which beats
actually fall through tiers 1–2, which is T3's output. Building G0-3b's
`style-core.md` equivalent now, ahead of T3, is a reasonable next step and
is *not* gated — it doesn't require a specific beat, only the ruled palette
— but assigning it to specific slots is.

---

## Tier 4 — `vidiq_generate_broll` stock

**Not reached.** Per T5's own text: if this tier is reached, portrait
orientation is mandatory and the attribution string must be composed into
the frame — **surface the attribution burden to Kim before spending**,
since an on-screen photo credit is a visible cost on a claims-discipline
channel. No stock has been sourced or costed. Flagging the halt condition
here so whoever picks this back up doesn't spend before that conversation
happens.

---

## Cost table (running)

| Source | Plates | Cost | Licence |
|---|---|---|---|
| `catalog/product-photography/` | 12 (10× 9:16) | $0 — already generated, committed | None (first-party generated, unbranded, fictional) |
| `catalog/ingredient-photography/` | 30 (square) | $0 — already generated, committed | None |
| `catalog/skin-macro-photography/` | 4 (square) | $0 — already generated, committed | None |
| `kbeauty-one-percent-line/assets/images/` | 6 (mixed) | $0 — already generated, committed | None (original pilot's own assets) |
| Extracted `cGbokt_B_vE` frames | 0 extracted yet | $0 when done | N/A |
| New Higgsfield (G0-3b spec) | 0 generated yet | TBD — priced per generation at spend time | None (first-party) |
| `vidiq_generate_broll` stock | 0 | TBD, **halt for Kim before spending** | Attribution required, burned into frame |

---

## What T5 has NOT done (explicit, not silently skipped)

- No B-roll slot has been filled, because T3's registry/caster (parallel
  session, unmerged as of this pass) hasn't opened any slots yet to fill.
- T1's own asset-inventory sweep hasn't run as a named task; tier 1 above is
  a best-effort manual sweep for this pass, not a substitute for it.
- Tier 2 (frame extraction) hasn't run.
- No new Higgsfield generation has been requested under G0-3b — the existing
  ~100-image pool was reviewed and rejected for this purpose (see Tier 3),
  not spent against.
- The one-third runtime cap (B-1) can't be checked until there's an assembled
  beat sheet with slots filled — not yet.

## Next step

Once T3 merges and the caster opens B-roll slots (with each slot's purpose,
`broll_allowed` status, and aspect contract), return to this manifest: walk
G0-4's precedence per slot against the tier-1 pool above first (product-photography's
9:16 set is the fastest fill for anything generic-packaging or texture-macro),
extract tier-2 frames for anything tier 1 can't cover, and only then write
G0-3b-spec generation prompts for what's left.

**Update, T3 merged to master (`2361302`, includes a T4 reconciliation —
see `wo/FVC-007/T3-REGISTRY-AND-CASTER-REPORT.md` "Cross-session
reconciliation"):** `videos/_system/catalog/catalog-registry.yaml` is now
real, committed, on disk. Confirms what was visible mid-flight:
`editorial_imagery_broll_wrapper` is the only `broll_allowed: true` purpose,
5 candidates (`push-in` default, `yt-camera-move`, `device-frame-stage`
foreign-surface/screenshot-only, `grade-split-reveal`, `grain-overlay`
non-standalone), zero content slots on any of them — unchanged by the T4
merge, which only touched the registry's separate `furniture:` section.
That answers "what is a B-roll slot" in registry terms without needing a
real per-beat caster run.

Per T3's own correction: **there is still no real per-beat cast list**, and
producing one isn't just T3's remaining work. Two more things block it,
per `T3-REGISTRY-AND-CASTER-REPORT.md`:

1. **T1 hasn't produced a machine-readable beat sheet.** `cast_scenes.py`
   (the S4.5 caster, skill repo `seoulhabit/claude-skills`, tested only
   against synthetic beat sheets) needs one; `kbeauty-one-percent-line` has
   no `03-beat-sheet.json` — T6's own text already flagged this needs
   deriving from `STORYBOARD.md` + the SRT (REVIEW.md P2), and that
   derivation hasn't happened.
2. **The compiler can't render a cast pick yet even once one exists.**
   `compile_composition.py`'s `CANONICAL_COMPONENTS` gate
   (`compile_composition.py:255-256`) still hard-rejects any non-`Sh*`
   component name — flagged in `videos/_system/MANIFEST.json`'s amendments
   and `videos/_system/COMPILER.md` §1, not fixed. Separate, unscoped
   compiler work.

So T5's own "next step" below is gated on T1 + that compiler fix, not on
T3 alone — holding per-scene assignment is still correct, just for a wider
reason than originally understood.

Per the coordination split below, the palette side of tier 3 is drafted
ahead of the real cast list — see `broll-style-core-draft.md` — since it
depends only on G0-3b's ruling, not on beat-specific content.

## Coordination with T3

T3 (`session/fvc-007-t3`, registry + S4.5 caster, Gate B) was a parallel
session; its work is now merged to master (`2361302`). Coordination
happened by direct message before either side touched a shared file — its
reply confirmed the split below and corrected one assumption (see previous
section: the real blocker is T1 + the compiler's `CANONICAL_COMPONENTS`
gate, not T3 itself, which is done).

- **T3 delivered:** `catalog-registry.yaml` (Gate B, halted per its own
  report), the S4.5 caster (`cast_scenes.py`, tested against synthetic beat
  sheets only), and — via a live cross-session reconciliation with T4's
  independently-built `furniture:` section — the lower-third `BLOCKER-CAST`
  resolved onto `cta-close` by Kim's R-11 ruling. None of that changes this
  manifest's tiers; `editorial_imagery_broll_wrapper` is unchanged by the
  T4 merge.
- **T5 owns, in the meantime:** the tier-1/tier-2 sourcing pool (done, this
  file) and the G0-3b palette scaffold (done, `broll-style-core-draft.md`).
  Holding off on per-scene generation bodies or assigning specific plates to
  specific beats until a real cast list exists — writing those against
  guessed content would repeat the mistake T0b's programmatic sweep was
  built to avoid, and per T3's correction there's a real one to wait for now
  (not just an in-progress one).
- **Not T5's job, flagged for whoever picks it up:** deriving
  `03-beat-sheet.json` for `kbeauty-one-percent-line` from `STORYBOARD.md` +
  the SRT (T1/T6's work, per REVIEW.md P2), and extending
  `CANONICAL_COMPONENTS` in `compile_composition.py` to accept registry
  components (unscoped compiler work, flagged but not fixed by T3).
- **Handoff:** once a real per-beat cast list exists and the compiler gate
  is extended, T5 resumes here: walk each `editorial_imagery_broll_wrapper`
  pick against tier 1 first, tier 2 next, and only write new G0-3b scene
  bodies for what's left unfilled.
