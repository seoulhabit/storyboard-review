# BarrierWall

- **`barrierwall-spike.html`** — "Skin Barrier Diagram." A pure-SVG
  brick-course wall standing in for the stratum corneum's lipid barrier —
  no photography, no medical illustration license needed. Three courses
  (`#course-top`, `#course-mid`, `#course-bot`) assemble on entrance, then
  an acid-wash rect + dashed waterline (`#wash`, `#wash-line`) descends onto
  the top course while three hand-authored shard paths (`#shard-1/2/3`)
  detach, drift, and rotate away as that course dims — the barrier
  "breaking apart" under repeated irritation. Same deterministic, paused
  GSAP clock as the other components — see [../../README.md](../../README.md).

  This is the **third independent build** of this exact mechanism in this
  repo — `videos/betaine-salicylate-gentle-bha/compositions/frames/02-harsh.html`
  (the pure-SVG original this entry is sourced from) and
  `videos/ceramides-barrier-diagnostic/compositions/03-crumble.html` (a
  CSS-grid variant with a hardcoded, non-random 12-brick collapse array) both
  built it from scratch before this one adapted the SVG version for
  `videos/peeling-not-progress`. Harvested here so a fourth video doesn't
  rebuild it again.

  **Field contract:** swap the two text nodes (`#claim-line-1`/`#claim-line-2`
  or your own headline element, and the mono qualifier under the diagram) and
  the `#source-chip` text for your own claim + a human-readable citation —
  `Journal · Year` or equivalent, never a raw lookup ID (a PMID, an `ING-*`
  key). faceless-video-craft SKILL.md bans internal record IDs from rendered
  frames; the ID that looked the source up belongs in the consuming video's
  own description, not this chip — corrected here 2026-08-31 after
  `videos/peeling-not-progress` shipped this exact defect in its first use of
  the mechanism. Wash color
  defaults to a neutral ink tint — recolor `.wash`/`.wash-line` to spend a
  video's coral moment here *only* if the wash beat is that video's one
  voltage moment; most videos will want it to stay neutral (see
  `peeling-not-progress/frame.md` § Component reuse for why that project's
  own adaptation dropped coral from this mechanism — its coral was already
  spent elsewhere).

Use this wherever a claim is literally about barrier damage, over-exfoliation,
or irritation from actives — the wall reads as "protective layers" generically
enough to generalize past skincare if a future project needs the same
break-apart mechanism for an unrelated barrier metaphor.
