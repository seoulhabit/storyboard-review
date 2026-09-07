# T4 — Channel furniture

Status: **PARTIAL.** Two of four roles shipped and registered clean. Two
roles halt on the same gap the Gate A ruling already flagged as a tracked
consequence (`wo/FVC-007/GATE-A-RULING.md`): no `hyperframes:component`
exists for lower-third/subscribe or platform-follow furniture, and Gate A
scoped the registry to components only, no blocks, regardless of T0b
verdict. One of those two is load-bearing (recurs every video) and needs
Kim's ruling before T4 can close; the other was already scoped as
"leave unassigned" and doesn't block anything today.

---

## Shipped

**`end_card` → `logo-brand-close`.** Retrofitted, registered, pinned per
T4's own instruction ("pick one in T4... do not decide per video").
`logo-outro` — the block originally named alongside it — is out of scope
under Gate A and also failed its own T0b scan independently (tagline
off-canvas in portrait). `logo-brand-close` is a component,
`t0b_verdict: reframes-clean`, and its `wordmark`/`tagline`/`url` slots
cover the same identity-close role logo-outro would have.

**`action_line` → `cta-close`.** Retrofitted, registered, left unfixed to a
timecode (per-video: "for videos that carry one," per T4 spec).

Both retrofits required two new `TOKEN_BRIDGE_MAP` / `INTERNAL_VARS`
entries in `retrofit_catalog.py` — the first time T4 has exercised T2's
"future items get checked against these two tables" design, not a script
change made lightly:

- `--brand` and `--accent-2` (`logo-brand-close`, `cta-close`): both items
  offer a green/blue/violet `accent` enum, backed by three host-suppliable
  custom properties (`--brand`=green, `--accent`=blue, `--accent-2`=violet).
  `--accent` already resolves correctly (a real design-token name, skipped
  as self-supplied). `--brand` and `--accent-2` had no bridge. Bridged both
  to `var(--accent)` — this channel ships one accent token (G0-3's
  six-token sheet), so all three enum values collapsing to the same clay
  accent is the correct, deliberate reading: there is nothing else on the
  palette for "blue" or "violet" to mean. The enum becomes a no-op by
  design, not by omission.
- `--lbc-wordmark-size` / `--cc-action-size` / `--cc-button-size`: JS-computed
  chars-aware text-fit sizing (cqw/cqh clamps), not colours — confirmed by
  reading each item's own script before exempting, same bar as the existing
  `--logical-width`/`--logical-height`/`--screen-scale` precedent.
- `--lbc-accent` / `--cc-accent`: JS-set at runtime to a `var()` reference
  into whichever of `--brand`/`--accent`/`--accent-2` the `accent` enum
  picked — a runtime alias, not an independent literal. Resolves correctly
  once those three are bridged; verified below.

### Contrast verification (R-13, rendered pixels)

Per R-13 and the T2 report's own bar ("a 4.5:1 contrast check on rendered
pixels... not on declared CSS values"), both retrofitted outputs were
loaded in the Browser pane inside isolated iframes with the real
`videos/_system/tokens/colors.css` injected, and read via
`getComputedStyle()` — not re-parsed from source. GSAP is unavailable in
this static harness (no vendored-path dev server), so the check reads the
unplayed initial layout, same documented limitation as T0b and T2's own
verification; colour values here don't depend on animation state, only on
the JS that runs before the first GSAP call (letter/word construction,
`root.style.setProperty` for the accent alias) — which does execute.

| Element | Computed | Against | Ratio |
|---|---|---|---|
| `logo-brand-close` wordmark/tagline text | `rgb(38,33,92)` (ink) | `rgb(244,237,227)` (cream, `.lbc-clip` bg) | 12.42:1 |
| `logo-brand-close` url text | `rgba(38,33,92,0.75)` (muted) | cream | 6.01:1 |
| `logo-brand-close` accent period | `rgb(156,58,50)` (clay) | cream | 5.9:1 |
| `cta-close` action line | `rgb(38,33,92)` (ink) | cream | 12.42:1 |
| `cta-close` button label | `rgb(244,237,227)` (cream) | `rgb(156,58,50)` (clay, button bg) | 5.9:1 |

All five clear the 4.5:1 floor with real margin. Both items classified
`recolourable` in `videos/_system/catalog/manifest.json`. Verification
harness was a throwaway page (not committed — matches T2's own precedent
of not shipping test scaffolding in the retrofitted output).

---

## Halted — `lower_third_subscribe`

**No `hyperframes:component` covers this role**, confirmed by a fresh
tag/name search this session across all 219 components
(`subscribe`/`lower`/`kicker`/`identity`/`channel`/`follow`/`social`/
`badge`/`watermark`/`bug`/`nametag`), independent of Gate A's own earlier
finding. The only real matches in the 383-item catalog are blocks
(`yt-lower-third`, the `lt-*` family) — zero components. This is the exact
consequence `GATE-A-RULING.md` already named as a tracked gap: *"T4 will
need one of R-11's two paths... before T4 can close."*

This role is load-bearing, not deferrable like platform-follow: T4's own
spec frames it as recurring "in every video," and R-14/R-12 mean the
channel's whole visual identity is supposed to route through the catalog +
token layer, not a bespoke build.

**R-11 gives exactly two options; there is no third.** As put to Kim:

1. **Rewrite the beat.** Drop the "persistent overlay while content plays,
   with the channel avatar" mechanism specifically, and carry the subscribe
   ask a different way with an existing component — most plausibly
   `cta-close` again, doing double duty as a dedicated few-second subscribe
   interstitial (`action_line: "Subscribe for the next one"` or similar)
   rather than a lower-third overlay. This is a real creative trade-off,
   not a cosmetic substitution: no avatar, not persistent, appears once as
   its own beat instead of layered over other content. Every other
   component checked (`social-proof-card`, `avatar-cloud`, `testimonial-card`,
   `testimonial-proof-card`, `x-follow-card`) was ruled out — either no
   avatar-image slot, wrong semantic (community/proof, not
   subscribe-specifically), or (`x-follow-card`) zero declared variables,
   meaning using it at all without forking would violate R-11 directly.
2. **Contribute upstream.** Write a subscribe lower-third component
   (avatar-image slot wired to `brand/channel/avatar-800.png`, persistent
   overlay profile) and submit it to the hyperframes catalog per their
   contribution guide, consuming it back through the normal retrofit path
   once merged. Real work; §5 of the WO already flags "the upstream
   contribution backlog... is not scoped in this WO" as an open item, so
   this option likely means T4 ships partial now and closes later.

`catalog-registry.yaml`'s `furniture.lower_third_subscribe` entry is
written with `status: BLOCKER-CAST` and `component: null`, matching R-11's
own mechanism, pending this ruling.

---

## Left unassigned — `platform_follow`

`instagram-follow`/`tiktok-follow` hit the identical component-scope gap
(both are blocks). `x-follow-card` is the one component-category
follow item, but it's X/Twitter-branded and hardcoded (zero declared
variables) — reusing it doesn't carry an Instagram/TikTok role, it
promotes a different platform outright, and reskinning it without
variables would mean forking, which R-11 forbids.

T4's own spec already scopes this role as "leave unassigned; cross-promo is
a per-video call" — no beat currently needs it filled, so this isn't
forced into an R-11 ruling today. Recorded in the registry as
`status: unassigned` rather than `BLOCKER-CAST`, to keep it distinguishable
from the load-bearing gap above. Revisit if and when cross-promo is
requested for a specific video — at that point it becomes a real
R-11 halt too, with the same two options.

---

## Files touched this session

- `videos/_system/catalog/logo-brand-close.html` (+ `.colormap.json`) — new
- `videos/_system/catalog/cta-close.html` (+ `.colormap.json`) — new
- `videos/_system/catalog/manifest.json` — two entries appended
- `videos/_system/catalog/retrofit_catalog.py` — `TOKEN_BRIDGE_MAP` +2,
  `INTERNAL_VARS` +5 (see above; both tables extended per their own
  documented pattern, not redesigned)
- `videos/_system/catalog/catalog-registry.yaml` — new, `furniture:`
  section only (see file header — `purposes:` is T3's, deliberately left
  for that session to fill, to keep the two sessions' edits non-overlapping)
- `vendor/hyperframes/` — re-cloned into this worktree, pinned to the same
  `0d5d3f3` the manifest already records (gitignored per R-14; each
  worktree needs its own clone, it does not travel with the shared index)
