# SkinBand

A labelled two-layer skin cross-section — epidermis over dermis, a gently
wavy surface line, a dashed boundary between them — that other actors
compose within or beneath.

- **`skinband-spike.html`** — the band alone, then combined with a free-chain
  actor (natural HA), a boundary-panel actor (serum), and a lattice actor
  (filler beneath the skin), demonstrating the three compositions it was
  actually used for.

## Why this exists

`videos/hyaluronic-acid-vs-filler` v2 needed to *place* each molecular form
relative to real skin structure — "at the surface" and "beneath the skin" are
claims about depth, and a viewer reads depth off a cross-section, not off a
caption. This was a **confirmed catalog gap**: three uncatalogued one-off
skin cross-sections already existed in the repo before this
(`videos/centella-tiger-grass/…/05-fibroblast.html`,
`videos/betaine-salicylate-gentle-bha/…/04-power.html`,
`videos/pdrn-cellular-science/…/04-mechanism.html`), none harvested — the
same "built five times, reused once, on the fourth try" pattern `[S6/A-1]`
names for `BarrierWall`. This entry is the harvest, not the fifth one-off.

## API

```python
skin_band(w, h, boundary_frac=0.30)
```

Returns one SVG fragment: a low-amplitude wavy surface path, a dashed
horizontal boundary line at `h * boundary_frac`, and two `EPIDERMIS` /
`DERMIS` labels (22px, 55% opacity, plain `<text>` — never citation-chip
typography). Compose other actors above the boundary (near the surface) or
below it (in the dermis) depending on what the beat claims:

| Composition | `boundary_frac` | What's above / below |
|---|---|---|
| Natural HA in skin | 0.22 | free coils + water dots spread through the dermis |
| Serum at the surface | — (uses `boundary_panel()` instead, its own dashed line) | large chains above, small chains crossing below |
| Filler beneath the skin | 0.20 | a cross-linked lattice, shifted down, sitting entirely beneath the line |

## Control: **none** (static plate)

Same discipline as `MoleculeStates`: no runtime randomness, no clock, no
autoplay. `free_coils()` / `water_dots()` take a seeded `random.Random`;
`skin_band()` itself has no randomness at all — the wavy line is a fixed
deterministic function of `w`, computed the same way every time.

## Two things to carry with it

1. **Compose the lattice or chains BEFORE the band in document order when they
   share one `viewBox`**, so the band's labels paint on top and stay legible
   over dense geometry. Getting this backwards, or calling `skin_band()` twice
   for one panel (once inside a transform group, once again unshifted), was
   a real authoring bug: it produced two overlapping `EPIDERMIS` labels at
   different y-offsets, caught only on an extracted frame — `hyperframes
   check` has no notion of "the same label drawn twice" and passed it clean.
2. **`boundary_frac` is a claim, not a decoration.** A panel asserting
   "stays near the surface" wants a high boundary (small dermis band below);
   one asserting "placed beneath the skin" wants the reverse. Match it to
   what the beat's text actually says, every time — there is no default that
   is right for more than one claim.

## Status

**SPIKE** — harvested from one project (`hyaluronic-acid-vs-filler` v2,
2026-09-03), used across four scenes there. The band itself is fully generic;
what will want redrawing per ingredient is whatever's composed on top of it.

See [../../README.md](../../README.md) for the full catalog.
