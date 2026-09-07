# T0a/T0b — Catalog clone, inventory, and aspect survivability scan

**Status: HALTED AT GATE A.** Per T0b's own instruction — "Do not begin T2
before Kim rules on Gate A" — this session stops here. T2 has not started.

---

## T0a — Clone and inventory

- **Repo path verified, not assumed.** `npm view hyperframes repository.url` →
  `git+https://github.com/heygen-com/hyperframes.git`. Matches the WO's
  assumption; no fallback needed.
- **Cloned** to `vendor/hyperframes/` (gitignored, per R-14), pinned at
  commit `0d5d3f3eb3aecd9fd64954d2767d3d64e97e58fc`.
- **Installed CLI:** `hyperframes --version` → `0.8.30`.
- **Real catalog size: 383 items** — 219 components, 155 blocks, 9 examples.
  Close to the WO's cited "375" (drift is repo activity between when the WO
  was drafted and now, not a made-up number — confirmed against the live
  registry, not asserted).
- **All 17 component names the WO cited by name are real upstream items** —
  `before-after-wipe`, `mk-specs-list`, `svg-stroke-trace`, `hw-frame`,
  `mk-placeholder-grid`, `yt-lower-third`, `logo-outro`, `logo-brand-close`,
  `cta-close`, `instagram-follow`, `tiktok-follow`, `x-post`,
  `yt-camera-move`, `grain-overlay`, `push-in`, `count-up`,
  `comparison-split`. The prior review (`wo/FVC-007/REVIEW.md` §5) flagged
  these as unverified since they appeared nowhere in this repo — they were
  simply never pulled. All confirmed real.
- **Full inventory written to `docs/wo/007/catalog-inventory.json`** (383
  entries: name, category, title, tags, native dimensions where declared,
  variable/slot list, colour-handling classification, CDN dependencies,
  source path).
- **`videos/_system/catalog/manifest.json` written** per R-14: source repo,
  pinned commit, CLI version. Per-item retrofit entries are T2's output, not
  populated here.

### A structural finding T0a surfaced, load-bearing for T0b and T2

**Only `blocks` (155/383) declare native dimensions.** `components`
(219/383) declare none — they're written to embed inside whatever canvas
hosts them, not to own a canvas. `142/155` blocks are native 1920×1080,
`12/155` native 1080×1920, `1/155` native 1440×2560 (a 9:16-ratio block at a
different absolute resolution — see below). This means "most catalog items
are authored at 1920×1080," the WO's stated T0 risk, is **true for blocks,
not true for components at all** — components have no native aspect to
survive a reframe of in the first place.

**The upstream registry has no formal `slots` field.** T3's own worked
example (`slots: {before: text_block, after: text_block}`) assumes
structured slot metadata that doesn't exist upstream — `before-after-wipe`'s
real schema has `variables` typed `content`/`style`/`layout`/`timing`, and
"slot" is only a tag/description word, not a schema field. T3 will need to
derive slot contracts from variable roles and/or the HTML itself, not read
them off the registry directly. Flagging this now since T3 is next in
sequence after Gate A.

**Colour handling across the real catalog:** 14/383 already token-native,
143/383 fully hardcoded, 224/383 mixed, 2/383 no colour literals at all.
T2's retrofit has real work across nearly the whole catalog, as the WO
assumed — this part of the WO's premise holds.

**CDN usage:** 311/383 items use jsdelivr GSAP (T2 step 3's target is
right for the bulk case); 58/383 use `fonts.googleapis.com`.

---

## T0b — Aspect survivability scan

### Scope: 36 items, not all 383 or all 155 blocks

T0b's own text says "judged over the ~40 items the registry actually needs
rather than all 375" — the WO never says which ~40, since curating that list
is T3's job, done later. To make T0b's pre-written thresholds meaningful
now, this session built a working set from T3's own stated coverage
requirement — "the four scene systems (editorial imagery, SVG diagram,
claim-vs-evidence, checklist), plus B-roll wrappers, plus the channel
furniture in T4" — by real tag/name search against the cloned registry,
plus every item this WO cites by name. **36 items resulted** (19
components, 17 blocks); full list and grouping in `catalog-inventory.json`'s
`t0b_scan` block. This is close enough to the WO's own "~40" figure to judge
the thresholds against, and it's the actual candidate set T3 will draw from
— not a token 12-item sample.

The remaining 347 catalog items were inventoried (T0a) but not individually
aspect-tested — T3 will only ever pull a curated subset, so testing items
nobody will use would have been wasted effort. If T3's later curation reaches
outside this 36-item set, those additions need their own aspect check before
being trusted.

### Method

For each item: loaded the raw registry HTML directly (no host harness —
none exists standalone; these are sub-composition snippets meant to be
seeked by a HyperFrames engine, and GSAP timelines here are constructed
`paused: true` with no autoplay). Forced the composition root (or, for
components with no declared root, `document.body`) to `1080×1920` via
`style.setProperty(..., 'important')`, then measured every descendant
element's `getBoundingClientRect()` relative to that root: flagged as
**off-canvas** anything extending past the new bounds, and separately
flagged **text-clipped** any text-bearing leaf whose `scrollWidth`/
`scrollHeight` exceeds its own box (content overflowing its own container,
not just the canvas).

**Caveat, stated plainly:** this measures the *unplayed initial layout*, not
a seeked frame mid-animation. An element legitimately positioned off-screen
for an intentional slide-in entrance would show as a false "off-canvas" hit
here. To keep the signal honest, every off-canvas hit was also tagged
**has-text** — background/atmospheric elements (a 3D dolly-zoom rig's depth
walls, a full-bleed grain overlay, an entrance-animated cursor icon) bleeding
past the frame is normal design, not a defect, and does **not** by itself
fail an item. Only text-bearing off-canvas content or genuine content
clipping counts against the verdict. This is a deliberate, disclosed choice
about what "survives a reframe" means — not a numbers-only pass.

### Result: PARTIAL — 24/36 = 66.7% pass-eligible (native-portrait or reframes-clean)

| Verdict | Count |
|---|---|
| native-portrait | 2 |
| reframes-clean | 22 |
| reframes-with-edits | 10 |
| landscape-only | 2 |

Falls in T0b's own **PARTIAL band (35–70%)**. Per the WO's pre-written rule:
**halt at Gate A. Kim rules: reduced registry, or retarget the pilot to
long-form.**

### The finding does not spread evenly — it clusters exactly where T0b said to look for that

> "if the failures cluster in one area... that is a different and more
> manageable finding than an even spread"

It clusters. Sharply, on one structural axis:

| Category | Pass | Total | Pct |
|---|---|---|---|
| **components** | 19 | 19 | **100%** |
| **blocks** | 5 | 17 | **29%** |

**Every component passed. Blocks fail nearly two-thirds of the time.** This
tracks the structural finding from T0a: components have no native canvas —
they're written to inherit whatever host embeds them, so they have nothing
to "reframe" and nothing hardcoded to a specific width. Blocks are full
standalone scenes authored at a fixed pixel canvas (overwhelmingly 1920×1080)
with element positions frequently hardcoded in absolute pixels tied to that
canvas — `flowchart`'s nodes sit at literal `left: 960px`/`600px`/`1320px`
with a `transform-origin: 960px 300px`, `data-chart`'s title/legend/source
line are centred against a 1920-wide layout with no relative fallback.

By T3's four scene systems + furniture grouping:

| Group | Pass | Total | Pct |
|---|---|---|---|
| editorial_imagery_broll_wrapper | 6 | 7 | 86% |
| claim_vs_evidence | 4 | 4 | 100% |
| channel_furniture | 5 | 8 | 62% |
| svg_diagram | 6 | 11 | 55% |
| checklist | 2 | 4 | 50% |
| misc_wo_named | 1 | 2 | 50% |

`claim_vs_evidence` and `editorial_imagery_broll_wrapper` pass well because
they're component-heavy. `svg_diagram` and `checklist` pull the average down
because they're block-heavy (charts and spec lists are usually authored as
full scenes, not embeddable snippets).

### Specific findings worth Kim's attention

- **`bar-chart-race`** (landscape-only): 31/70 elements off-canvas, 7 with
  text (dollar values, period caption), plus the period label genuinely
  **text-clips**, not just relocates. Heaviest failure in the set.
- **`data-chart`** (reframes-with-edits, borderline): 19/53 off-canvas,
  title/subtitle/legend/source line all affected — centred layout with no
  relative fallback.
- **`mk-specs-list`** (landscape-only): 0 off-canvas but **10 text-clipped**
  spec labels/values — a different failure mode than the others: nothing
  leaves the frame, but fixed-width columns truncate their own content once
  narrower. Worth naming since a naive "count off-canvas elements" check
  would have missed this entirely.
- **`yt-lower-third`**: clean despite native 1920×1080 — a real, working
  portrait-safe furniture candidate for T4.
- **`lt-dark-card`** / **`lt-kicker-name`**: minor text-clip only (a name
  label truncates) — cheap, targeted fixes, not structural problems.
- **`x-post`**: 20/53 off-canvas. Expected and consistent with R-13's own
  pre-existing call that `x-post` is a **foreign-surface** item (kept at
  native colour and, by this finding, arguably native *proportions* too) —
  this scan corroborates that classification rather than contradicting it.
- **`flowchart-vertical`**: native aspect **is** 9:16 (1440×2560 — same
  ratio as 1080×1920, confirmed: 1440/2560 = 1080/1920 = 0.5625) but still
  fails on reframe to the exact 1080×1920 target (6 off-canvas, cursor
  entrance element included). **A matching aspect ratio does not by itself
  guarantee survival** — this item hardcodes absolute pixel values at its
  own 1440-wide native resolution rather than using relative units, so
  forcing it down to 1080 breaks the same way a 1920-wide block does. Worth
  keeping in mind for T0b's own pass criteria if this scan is ever repeated
  at other target resolutions.

---

## Gate A — halting for Kim's ruling

Per the WO: **PARTIAL means halt, and Kim rules between two options** —
reduce the registry, or retarget the pilot to long-form. This session takes
no position between them beyond surfacing what each would actually mean:

- **Reduce the registry:** viable and specifically well-supported by this
  data — components alone already cover 100% of what was tested, and two of
  T3's four scene systems (`claim_vs_evidence`, and most of
  `editorial_imagery_broll_wrapper`) are already component-heavy. A registry
  built preferentially from components, falling back to only the
  already-verified-clean blocks (`yt-lower-third`, `hw-frame` after its
  6-line fix, etc.), would likely clear 70% on its own without touching a
  single upstream file.
- **Retarget to long-form:** also viable — every block that failed here was
  authored natively at 1920×1080 and would need **no reframe fix at all** in
  a 16:9 pilot. This flips the finding entirely: blocks would pass ~100%,
  components (canvas-agnostic) would presumably still pass, since nothing
  about their embed-anywhere design depends on aspect.

Either path is real and inexpensive to pursue given what's now known — this
isn't a "the catalog doesn't work for this channel" finding, it's a "the
catalog splits cleanly along a line the WO didn't know to look for, and one
side of that line already clears the bar" finding.

**T2 does not start until Kim rules here.**
