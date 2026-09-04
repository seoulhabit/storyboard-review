# Before / after — `hyaluronic-acid-vs-filler` retention rewrite

Three cuts of this project exist. **v1** is the original two-hander described in
the brief's "CURRENT PROBLEMS" section, reachable at commit `48c29d9` (no
longer on `master`'s tip — see note at the end). **v2** is a prior single-narrator
revision, commit `dd34015`, used here as the stated starting point. **v3** is
this rewrite.

## Headline numbers

| Metric | v1 (original) | v2 (baseline) | v3 (this rewrite) |
|---|---:|---:|---:|
| Duration | 180.100s | 160.000s | **120.359s** (measured, not stretched) |
| Word count | 421 | 388 | **309** |
| Speaker turns | 25 (13 Kimberly / 12 Grady) | 13 (Kimberly only) | **12 (Kimberly only)** |
| Scenes | 14 | 13 | **14** |
| Longest scene (clip-padded) | 23.034s (s06-serum-size) | 22.281s (s11-do-not-inject) | **13.767s** (s13-badges) |
| Container-drift tweens | not separately counted | **27**, on 0 mechanism tweens | **8** (safety-net only), plus **79** real per-element mechanism/entrance tweens |
| Central answer lands by | ~35s (after two speaker turns and a history detour) | ~14s (end of a 5-sentence opening) | **5.411s**, measured (its own stem) |
| Three identities complete by | not distinctly staged | ~14s | **10.095s**, measured (its own stem) |
| History (1934) position | 17–41s, before the mechanism explanation | 22–28s, before the mechanism explanation | **78.0–84.1s**, after every mechanism scene |
| Analogies retained | 4+ (cousins, forty-dollar serum, houseplant, lifeguard/pool, cow royalties) | 3 (houseplant, lifeguard/pool, resident/moisturiser/construction) | **1** ("a sponge, not a water factory") |

## Longest visually unchanged interval

Measured on the rendered pixels via `catalog/tooling/check-cadence.py --longform`
(8fps sampling, a step counts as a "beat" only if it produces mean\|ΔLuma\|≥1.0
**and** a localized max≥40 — declaring a tween is not enough to count):

- **v3: 5.62s** (worst individual scene, s08-seals), whole-video active share
  **19.1%** of 8fps steps. Every scene is under the format's 6.0s ceiling.
- v1/v2 were not re-measured this way as part of this rewrite (their renders
  were not re-run), but the project's own `policy-change-proposals.md`
  documents specific measured frozen windows in v1's composition before its
  own fixes: **9.03s** on the safety-card scene (three consecutive wipes and
  nothing else) and an **8.43s** frozen window on a scene with three
  identical-target hold beats. v2's composition carried the same 27
  container-drift-only tweens with zero mechanism motion (confirmed by grep,
  not estimate) — its equivalent measurement was not separately re-run here.

Separately, at the authoring level (GSAP tween-start times, before rendering),
`hyperframes keyframes --json` on v3 shows **127 distinct visual-change
events** across the piece, **largest gap anywhere 3.50s**, **largest gap in
the first 30 seconds 3.27s** — both inside the brief's 2–4 second target.

## Per-scene durations, v3 (clip-padded, matching how v1/v2 are reported above)

| Scene | Duration | What it shows |
|---|---:|---|
| s01-thesis | 6.36s | Central myth-correction thesis; three actors present; ends on a "SERUM ≠ FILLER" snap |
| s02-identities | 6.33s | Each of the three identities named as its lane brightens |
| s03-not-filler | 11.91s | "The mix-up is expensive" / "not filler in a bottle" |
| s04-split | 10.44s | Free chains (idle drift) vs. a mesh that locks into place — the categorical contrast |
| s05-size | 12.69s | Large chains stop above the skin boundary; small chains cross below it |
| s06-plumping | 9.03s | Near-surface chains swell then settle — the "temporarily" hedge, animated |
| s07-binds | 9.53s | Water dots translate onto a chain and bind |
| s08-seals | 8.72s | Continuing s07's state: three of eight bound drops detach and drift away |
| s09-crosslink | 11.44s | Loose chains fade as 14 of 42 lattice nodes pop in, staggered |
| s10-origin | 7.29s | 1934 count-up + eye/flask illustration (placed after the mechanism, not before) |
| s11-warning | 7.42s | Decisive full-frame "DO NOT INJECT YOURSELF" |
| s12-risks | 13.77s | FDA wording, risks, provider instruction |
| s13-badges | 13.71s | Three-badge recap, reusing the s01/s02 actors |
| s14-endcard | 4.93s | Closing line, end card |

Mean scene length **9.6s** (clip-padded) / **8.6s** (beat-sheet), against v1's
mean of ~13.5s and v2's ~12.6s.

## What changed, mechanically

- **VO model**: `04-assets/build_vo.py` no longer stretches speech + gaps to a
  fixed target (v1: 180.0, v2: 160.0, via one global scale factor with no
  guard against going negative). It now places stems with fixed absolute
  gaps, so the total is whatever the measured recording comes to — 120.359s,
  landing inside the requested 120–135s band.
- **Animation**: v2's composition had 27 tweens on scene containers/panels
  and zero tweens on any actor sub-element — the three morphology actors were
  static plates the video only ever panned or zoomed. v3 keeps the actors
  themselves static and seed-deterministic (so reused actors stay
  pixel-identical) but animates their own children: chain groups translate
  across the skin boundary, water-dot circles bind and later detach, lattice
  nodes pop in individually with a stagger. Verified empirically via the
  animation map and the rendered-pixel cadence gate above, not asserted.
- **Safety section**: was one scene held 22.3s (v2) / 16.3s (v1). Now two
  scenes, 7.42s + 13.77s = 21.19s total, with the decisive full-frame card
  as its own short beat rather than sharing a scene with the FDA wording.
- **Chapters**: the new 6.1s "history" section would have broken
  `youtube-delivery.md`'s 10-second chapter floor if given its own marker;
  it now folds into the preceding "mechanism" chapter for the public chapter
  list while keeping its own `section` value for scene bookkeeping.

## Known limitation, disclosed rather than hidden

`catalog/tooling/check-static-hold.py` flagged 9 brief (~1.0–1.25s) windows
where a mid-frame band reads as empty right at a same-background scene
transition (e.g. 10.5–11.75s, at the s02→s03 handoff). Spot-checked on
extracted frames: real, not a false positive — the incoming scene's wipe mask
covers the outgoing scene's content fractionally before its own headline has
faded in enough to read. A same-ground transition in v2's own shipped render
(checked directly, s01→s02) does not show this, because that scene's outgoing
text has no exit animation and stays on screen, unfaded, until the wipe
physically covers it — whereas several v3 scenes rely on the incoming beat's
own fade-in without an overlapping-visible outgoing state. This is a
transition-timing characteristic of my new scene set, not of the shared
wipe-transition mechanism itself, and it is brief enough that the pixel-level
cadence gate (the authoritative check) still passes cleanly through every one
of these windows — but it is a real, fixable rough edge, not a false alarm,
and is called out here rather than smoothed over.

## Reference preserved

The original two-hander is at git commit `48c29d9` — note that `master`'s tip
has moved to `dd34015` (v2) during this session (another session's merge,
observed while gathering these numbers, not an action taken here). v1 remains
fully recoverable by commit SHA either way, in this branch's own ancestry and
in `master`'s history. v2's render (`06-render/final.mp4` in this worktree,
160.000s) is untouched on disk. This rewrite's own proof render lives at
`06-render/proof/draft.mp4` and does not overwrite either.
