# Gate A — ruling (Kim, 2026-09-07)

**Ruling: reduce the registry to components. Proceed to T2.**

Given `wo/FVC-007/T0-GATE-A-REPORT.md`'s finding — components pass 19/19
(100%), blocks pass 5/17 (29%) — the registry is built from
`hyperframes:component`-category items only. No block is retrofitted or
registered, regardless of its individual T0b verdict (this drops even the
blocks that scanned clean or native-portrait: `yt-lower-third`,
`instagram-follow`, `tiktok-follow`, `hw-frame`, `freeze-frame-dressing`).

## Known consequence, flagged per R-11 rather than silently worked around

A real catalog search at the pinned commit (`0d5d3f3`) finds **no
component-category alternative** for two of T4's furniture roles:

- **Lower-third / subscribe furniture.** The only matches for `lower-third`
  in the whole 383-item registry are blocks (`yt-lower-third`, `lt-dark-card`,
  `lt-kicker-name`, and others in the `lt-*` family) — zero components.
- **Platform-specific follow cards.** `instagram-follow` / `tiktok-follow`
  are blocks only. The one component-category follow item,
  `x-follow-card`, is generic (tag `social-overlay`), not IG/TikTok-branded.

`logo-outro`'s furniture role is still covered — `logo-brand-close` is a
component and already scanned clean. `cta-close` is also a component,
already clean.

**Per R-11's own mechanism** ("no viable candidate halts with
`BLOCKER-CAST:<beat_id>`; Kim rules on exactly two options: rewrite the
beat, or contribute the component upstream"): this is exactly that
situation, arriving early via the registry build rather than mid-beat at
T6. Recorded here as a named, tracked gap for T4 rather than resolved by
assumption — T4 will need one of R-11's two paths for the lower-third and
platform-follow roles specifically. Not blocking T2, which does not depend
on furniture coverage.

## What this changes in the WO

- T2's retrofit targets components only (219 of 383 items are eligible
  input; a `hyperframes:block` item is out of scope for this WO's registry,
  full stop — not merely deprioritized).
- T3's registry has no block-authored candidates to rank in any purpose
  group. Every `catalog-registry.yaml` entry is a component.
- T4 furniture is covered for `logo-outro`'s role (via `logo-brand-close`)
  and the CTA role (via `cta-close`); lower-third and platform-follow need
  an R-11 resolution before T4 can close.
