# Ginseng

Unlike PDRN and snail mucin, there's no homeless design spike to rescue here
— red ginseng's design work already has a proper home in a real, in-progress
HyperFrames project. This entry just points at it rather than duplicating
anything, so there's one copy instead of two that can drift apart (see the
Dawn to Dusk / "Cape Family Medical" mess in
[../../visual-components/dawn-to-dusk-routine/](../../visual-components/dawn-to-dusk-routine/)
for why that matters).

**Project:** `../../../videos/red-ginseng-two-routes/` — "Red Ginseng: Two
Routes." Six-scene, 1080x1920 concept-explainer. Hook: *"The strongest
ginseng study never touched skin. It was swallowed."* The whole video argues
that oral and topical red ginseng aren't interchangeable — each delivery
route is backed by a separate real clinical study (oral: `ING-ginseng-S002`;
topical: `S001`, `S005`, `S006`), with its own sample size, duration, and
claim.

**Rendered:** `renders/video.mp4` — 40.1s, 1080x1920, 5.4MB (confirmed via
`ffprobe`). Finished with a Hanbang/apothecary art-direction pass over the
earlier build: concentric root/ripple ring motifs, sine-wave linework
replacing a jagged wrinkle line, a gold-seal treatment for the 인삼 Hangul,
softer corners throughout. Passed the full lint/layout/motion/contrast
check clean (41/41 contrast).

Scenes: hook (dried-root pan) → botanical identity → oral/systemic route →
topical route → **side-by-side comparison** (the crux — split-screen
framing) → end card. Frames 3→4 deliberately repeat the same layered-depth
camera logic as one continuous move (dermis-deep in Frame 3, rising to the
surface in Frame 4) — a documented exception to the project's usual
never-repeat-framing rule, not an oversight.

Unlike this catalog's spikes, the individual scene files
(`compositions/frames/*.html`) are **not** standalone-previewable — each is
a bare `<template>` fragment meant to be assembled by the project's own
runtime, so opening one directly renders an empty page (confirmed: 0 body
children, inert by how `<template>` works). Even the project's real
`index.html` needs the actual HyperFrames dev/preview tooling to render —
loading it under a plain static file server gets you a registered
`window.__timelines.main` GSAP timeline sitting correctly paused at t=0,
but no visible frame, because it's authored to be scrubbed by that tooling,
not to autoplay standalone. Read the frame packets instead for the actual
content:
- [`.hyperframes/frame-packets/05-comparison.md`](../../../videos/red-ginseng-two-routes/.hyperframes/frame-packets/05-comparison.md) — the oral-vs-topical split-screen, the piece's whole thesis in one frame.
- [`.hyperframes/frame-packets/01-hook.md`](../../../videos/red-ginseng-two-routes/.hyperframes/frame-packets/01-hook.md) — the opening hook.

Full creative direction (palette system, motion grammar, negative list) is
in `../../../videos/red-ginseng-two-routes/STORYBOARD.md`. This project was
adapted from the same "dawn-to-dusk" recipe as the
[Dawn to Dusk](../../visual-components/dawn-to-dusk-routine/) component,
per its own `BRIEF.md` — worth knowing if you're looking for a shared
starting point for a future ingredient video.

An earlier, separately-validated ginseng script also exists
(`storyline_ginseng.html` at the repo root) — generated output, gitignored,
not duplicated here.
