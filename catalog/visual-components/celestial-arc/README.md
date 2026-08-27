# Celestial Arc

- **`celestial-arc-spike.html`** — a day/night sky motif: a dashed arc from
  sunrise to sunset with a dot that travels it (color-shifting AM&rarr;PM), a
  pulsing/radiating CSS sun on one end, and a crescent moon with twinkling
  stars on the other. No ingredient copy, no routine steps — just the motif.

Extracted from [Dawn to Dusk
Skincare](../dawn-to-dusk-routine/am-pm-skincare-spike.html), where it's the
hero backdrop above the AM/PM routine cards. Pulled out on its own because
the motif is reusable anywhere a video needs to say "morning vs. evening" or
"over the course of a day" — not just for skincare routines.

**SPIKE — not wired to build.mjs**, same as the other visual components (see
[../../README.md](../../README.md)). It also inherits its parent's gap: the
sun/moon/star animations run on plain CSS `infinite` keyframes (wall-clock),
not the deterministic `t`-driven GSAP clock the rules-based components use —
so it isn't seek-safe yet. Re-driving `glow-pulse` / `spin-slow` / `twinkle`
/ the arc-dot's `<animateMotion>` from a scrubbed timeline is the next step
before this can appear in a real render.
