---
format: 1080x1920
duration: 9s
message: PDRN supports skin regeneration through three key functions — barrier repair, reduced inflammation, and cell renewal.
arc: Title → Function 1 → Function 2 → Function 3 → Synthesis
audience: skincare/aesthetics viewers learning what a PDRN treatment actually does at the cellular level
mode: autonomous
---

All five frames below are beats of the **same** single-composition timeline
(`index.html`, `window.__timelines["main"]`) — not five separate files. Each
`src` points to the one composition; `poster` seeks to a settled moment
inside that beat so the contact sheet shows it correctly. There are no
cross-file transitions: everything is one continuous GSAP timeline over a
static background (DNA helix + drifting bubbles + leaf), so `transition_in`
is omitted throughout — the "transitions" are internal reveals, not cuts.

## Frame 1 — Title card

- status: animated
- src: index.html
- poster: 0.85
- duration: 1.05s
- scene: Title and "Three Key Functions" eyebrow fade up over the established background.

Cold open on the background (helix, bubbles, leaf already in place), then the
headline settles in one restrained move at t=0.15s. No panels yet — this is
the calm establishing beat before the three functions arrive one at a time.

## Frame 2 — Function 1: Barrier Repair

- status: animated
- src: index.html
- poster: 1.8
- duration: 1.1s
- scene: First circle pops in — shield + checkmark, falling droplets, "Barrier Repair" and its line of copy.

Event 1 of the sequence, entering at t=1.05s. Badge and illustration pop in
together (power3.out, no bounce — clinical tone), heading/description follow
~0.2s behind.

## Frame 3 — Function 2: Reduces Inflammation

- status: animated
- src: index.html
- poster: 2.9
- duration: 1.1s
- scene: Second circle pops in — red arrows into an inflamed bulge, "Reduces Inflammation" and its line of copy.

Event 2, entering at t=2.15s — about a second after Function 1 so it reads
as its own beat rather than a cascade.

## Frame 4 — Function 3: Boosts Cell Renewal

- status: animated
- src: index.html
- poster: 4.0
- duration: 1.1s
- scene: Third circle pops in — upward arrows and sparkles, "Boosts Cell Renewal" and its line of copy.

Event 3, entering at t=3.25s. All three panels are now visible and the
"sequence of three events" is complete.

## Frame 5 — Synthesis & hold

- status: animated
- src: index.html
- poster: 6.0
- duration: 4.65s
- scene: Summary card ("PDRN works at the cellular level…") fades in beneath the panels; the frame holds with a faint ambient float on the background bubbles.

Closing book-end at t=4.35s, settled by ~5.0s. The remaining ~4s is an
intentional near-static hold so the assembled infographic is legible (and
screenshot-worthy) before the clip ends at t=9.0s.
