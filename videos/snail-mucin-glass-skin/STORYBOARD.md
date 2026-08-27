---
format: 1080x1920
duration: 10s
message: Snail mucin's reputation for glass skin comes down to five active compounds and four skin benefits — shown through the ingredient's own glossy secretion trail.
arc: Hook (headline) → Descriptor → CN Subhead → Stat 1 (Active Compounds) → Stat 2 (Skin Benefits) → Resolve
audience: skincare-education viewers learning what's actually in snail mucin and what it does for skin
mode: autonomous
---

All six frames below are beats of the **same** single-composition timeline
(`index.html`, `window.__timelines["main"]`) — not six separate files. Each
`src` points to the one composition; `poster` seeks to a settled moment
inside that beat so the contact sheet shows it correctly. There are no
cross-file transitions: everything is one continuous GSAP timeline over the
locked poster's illustrated bottle + snails + botanical background, so
`transition_in` is omitted throughout — the "transitions" are internal
reveals, not cuts. Nothing that enters ever exits: each beat layers onto the
persistent stage, so by the resolve hold every element from beats 1–5 is
still on screen together.

## Frame 1 — Hook: headline + bottle + snails

- status: animated
- src: index.html
- poster: 1.5
- duration: 1.8s
- scene: "SNAIL" kicks up, "MUCIN" lands with a confident slam; the illustrated dropper bottle draws in and both snails settle onto the glass as their opalescent slime trails stroke-draw down it.

Cold open on the botanical background (sage gradient, ghosted leaves,
bokeh bubbles already in place). The kicker lands at t=0.15s, then "MUCIN"
slams in on a restrained scale+blur entrance settling by ~0.9s — glossy,
not playful. The bottle group and both snails spring-pop in alongside it
(large snail first, small snail ~0.15s behind), and from t=0.4s the twin
seafoam-to-gold-to-lilac slime trails draw themselves onto the glass,
finishing by 1.6s. This stroke-draw is the piece's one dominant motif —
everything else in the piece is built around it.

## Frame 2 — Descriptor: the actives named

- status: animated
- src: index.html
- poster: 2.6
- duration: 1.4s
- scene: "Glycoprotein · Hyaluronic Acid · Allantoin Complex" reveals left to right beneath the headline.

Entering at t=1.9s. The three terms fade/blur in with an even ~0.15–0.2s
stagger and no scale or bounce on any of them — genuinely co-equal weight,
a clinical credentialing beat rather than a showy one.

## Frame 3 — Chinese subhead: the bridge

- status: animated
- src: index.html
- poster: 3.7
- duration: 1.2s
- scene: "蝸牛黏液精華" (Snail Mucin Essence) slides up beneath the descriptor.

Entering at t=3.3s. Deliberately the calmest, most unadorned beat in the
piece — a short breath between the hook's slam/draw-on energy and the
punchier stat pair to come.

## Frame 4 — Stat 1: Key Actives

- status: animated
- src: index.html
- poster: 5.5
- duration: 1.5s
- scene: First glass callout disc pops in; "05" counts up alongside "活性成分 / Key Actives".

Entering at t=4.5s — the piece's one deliberate pattern-interrupt, where
the calm text cascade gives way to a punchier proof rhythm. The disc
scale-pops in, then the numeral counts 00→05 in ~0.5–0.6s with no bounce
on the digits themselves (it's data, not decoration) — the punch comes
from the disc's pop and the count's speed. Labels follow ~0.15s behind.

## Frame 5 — Stat 2: Skin Benefits

- status: animated
- src: index.html
- poster: 7.0
- duration: 1.3s
- scene: Second glass callout disc pops in; "04" counts up alongside "肌膚功效 / Skin Benefits".

Entering at t=6.0s, about a second after Stat 1 so it reads as its own
beat. Deliberately a near-exact mirror of Frame 4's mechanism — a matched
call-and-response pair, not a varied beat.

## Frame 6 — Resolve & hold

- status: animated
- src: index.html
- poster: 8.5
- duration: 2.8s
- scene: Full assembled composition holds — headline, descriptor, CN subhead, both stat discs, and the illustrated bottle all legible together, bubbles breathing gently.

Closing hold from t=7.2s. Nothing new enters and nothing exits — this is
the intentional, screenshot-worthy still that closes the piece. The bokeh
bubbles and the slime trail's shimmer carry a low-amplitude ambient
breathe (bounded sine motion, not a new motif) through to t=10.0s. No
brand mark anywhere, per the locked constraint carried over from the
source poster.
