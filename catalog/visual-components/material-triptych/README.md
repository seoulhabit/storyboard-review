# MaterialTriptych

**N parallel materials shown side by side, joined by a rail, then having that
join struck through.** The component's subject is not the items — it is the
*relationship between them being withdrawn*. Use it when several things share
a name or a category label but do not share the evidence, the origin, or the
outcome behind it.

- **Duration** 13.5s (authored; every beat derives from `items.length`)
- **Control** clock — one paused GSAP timeline, seeked. Scrubber loads
  **pre-applied**, no `?debug=1` to discover.
- **Canvas** 1080×1920, safe-area padding 192/162/384/72 baked in
- **Status** validated reference spike; the mechanism ships in
  `videos/exosome-label-problem/compositions/frames/03-materials.html`

## Why this one, and why now

Harvested from `videos/exosome-label-problem` scene 03 — "One word. Three
materials." (cell-derived vs. plant-derived vs. ferment-derived vesicles, all
sold under the word *exosome*).

A discovery pass across every existing `catalog/visual-components/` entry
before that scene was built found **no N-way comparison of any kind**, and
three near-misses worth recording so the next build doesn't repeat the
comparison:

| Considered | Why it doesn't fit |
|---|---|
| `SplitCompare` | A **two-thing** bisector. Three parallel materials are not a binary, and forcing a third into a bisector misrepresents the relationship. |
| `SplitFaceProtocol` | Also two-armed, and specifically a *clinical study* diagram (control vs. active). These items are not arms of a trial. |
| `FactorConverge` | Three nodes, but **many-to-one convergence** on a shared outcome, with fixed triangle geometry. These items converge on nothing — the entire point is that they *don't* share an outcome. Using it would assert the opposite of the claim. |
| `ThresholdList` | A ranked list split by a **cutoff**. No ranking here, no cutoff; the items are peers. |

The distinguishing property is the **join-then-withdraw beat**. A plain
three-up grid is not this component: what makes it a mechanism is that the
rail is drawn *first*, proposing a relationship the viewer is invited to
assume, and only then struck through and dimmed. Nothing else in the catalog
animates a proposition and its retraction as two ordered beats.

## Field contract

Swap the `DATA` object. `items` accepts **2–4** entries; the grid is
`repeat(var(--n),1fr)` and every stagger derives from `items.length`, so
nothing else needs editing.

```js
var DATA = {
  headline: "One word.<br>Three materials.",   // innerHTML, <br> allowed
  sub:      "All sold under the same name",
  items: [                                      // 2-4
    { name: "Cell-derived", sub: "stem cell<br>platelet<br>milk", plate: null },
    { name: "Plant",        sub: "leaf, root<br>extract",         plate: null },
    { name: "Ferment",      sub: "bacteria<br>derived",           plate: null }
  ],
  verdict:  "Evidence does not transfer",       // the struck-through bar
  close:    "Proof for one is not<br>proof for the others.",
  citation: "Journal · Year"                    // human-readable form ONLY
};
```

`plate: null` renders a labelled placeholder tile. Pass a project-relative
path to use a real image; the spike emits `loading="eager" decoding="sync"`
with explicit `width`/`height` and `object-fit: cover`, because a headless
renderer skips unpainted images and an unconstrained one reflows mid-render.

## Beat map

| t | beat |
|---|---|
| 0.00 | N independent Ken Burns drifts start — different scale and ease per tile |
| 0.18 | sub-label |
| 0.55 + 1.5·i | item *i* arrives on a scale-pop |
| ~5.3 | celadon rail draws across, joining every column |
| ~5.4 + 0.28·i | node cap *i* lands |
| ~7.3 | **ink bar strikes across; the rail dims to 0.22** |
| ~8.9 | plain-language restatement |
| ~10.3 | citation pill |
| ~11.3 | settle push on the verdict bar |

## Notes for reuse

- **The tiles want one consistent grade.** Three plates from different shoots
  read as three different papers side by side and undo the comparison. The
  source project ground-keyed all three to `--paper` with an additive shift
  applied only to bright, low-chroma pixels, leaving subject pixels
  bit-identical (verified: max per-channel delta 0.00 at luma < 190).
- **Each tile's drift is clipped by its own tile box**, so no zoom can reach
  the safe area and this component needs no zoom-aware safe-area math.
- **Reset UA margins.** The source project's round-1 render failed the
  safe-area hard gate because `h1`/`p`/`figure` default margins inflated a
  fixed-height flex stack by 64–75px. This spike carries
  `h1,h2,h3,p,figure,… { margin: 0 }`; keep it if you lift the markup.
- **No success colour.** Celadon marks the proposed join, not an endorsement;
  the strike is plain ink, not red. The source project reserved its one coral
  spend for a different scene.
- **Citations render as `Journal · Year` only** — never a DOI, PMID, or
  internal catalog key on a frame.
