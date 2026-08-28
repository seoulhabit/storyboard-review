# Dawn to Dusk routine

- **`am-pm-skincare-spike.html`** — "Dawn to Dusk Skincare." Two 5-step
  checklists: Morning ("Protect" — cleanser, toner, antioxidant serum,
  moisturizer, sunscreen) and Night ("Treat + Replenish" — cleanser, toner,
  treatment, serum/booster, night cream).

This is the "day and night" component. It's ingredient-agnostic — any
ingredient can be slotted into a routine step — which is why it lives here
under visual components rather than under a specific ingredient folder.

## Design system

Restyled against the **SeoulHabit Video Design System**
(`claude.ai/design/p/75132ad8-b81c-4151-8a4c-83368df1d949`), connected via the
`DesignSync` tool and read directly — `tokens/*.css`, `design-system-spec.md`,
`catalog.md`, and `components/foundation/Icon.jsx` — not eyeballed from a
screenshot.

`catalog.md` (the system's own audit of this repo, read 2026-08-27) and
`design-system-spec.md` (the migration proposal derived from it) both name
this file specifically. The verdict for it is explicit, not inferred:

> **Dawn to Dusk Routine** — Deprecate as a component; harvest into
> `RoutineLadder` + `RoutineChecklist`. Its content structure is good; its
> implementation is the least render-safe thing here (`vw`, `clamp`,
> `@media`, `prefers-color-scheme`, infinite keyframes, `color-mix`).
> Nothing survives the rewrite except the AM/PM step content.

So this was rebuilt from the token layer up, not restyled in place. What
actually carried over from the previous version: the ten step names and
one-line descriptions, and the "Morning = Protect" / "Night = Treat +
Replenish" taglines. Everything else — the palette, the layout mechanics,
the backdrop — is new.

### What was dropped, and why

- **The bespoke 22-token palette** (`--page-bg`, `--panel-am`, `--panel-pm`,
  ten unique per-step hues `--am-1..5`/`--pm-1..5`, a full
  `prefers-color-scheme` dark-mode override block). `design-system-spec.md`
  §2.1 names this palette directly — "dawn-to-dusk amber/violet" — in its
  list of five ingredient-specific art directions to deprecate: "none carried
  into a rendered video except as copied CSS." The real token layer has no
  per-routine or per-step accent slot; introducing one here would just be a
  sixth incompatible palette.
- **Instrument Serif and Karla**, loaded from Google Fonts. Not in the
  system's four-family stack (EB Garamond / Inter / JetBrains Mono / Noto
  Sans KR) and not flagged anywhere as a considered addition.
- **The inline Celestial Arc backdrop** (`.arc-strip`, `.celestial`, the
  sun/moon orbit SVG). `catalog.md` §2 flags it as a duplicate — "extracted
  verbatim from Dawn to Dusk... both copies exist" — and
  `design-system-spec.md` deprecates Celestial Arc on its own terms: three
  infinite CSS loops, `drop-shadow` glow, `animateMotion`, `clamp()` sizing.
  If the motif is wanted back it returns as a `Backdrop`, driven by seek
  time, from [`../celestial-arc/`](../celestial-arc/README.md) — not
  re-duplicated into this file.
- **Every viewport-relative unit**: `clamp()`, `vw`, `max-width` fluid
  containers, the `@media (min-width:760px)` two-column breakpoint, the
  `@media (prefers-color-scheme: dark)` theme override, `color-mix()`. The
  spec bans all of these from render-path CSS on determinism grounds — "a
  non-deterministic component cannot be built out of compliant tokens."
- **The `calc(var(--i) * 90ms)` scroll-triggered stagger** and its
  `IntersectionObserver`. Named directly in `design-system-spec.md` §2.4 as
  one of two reasons ("Celestial Arc and Dawn to Dusk") the originals aren't
  seek-safe.

### What replaced it

**Canvas.** Fixed `1080×1920`, matching `design-system-spec.md` §1's primary
canvas and every actually-shipped video in `catalog.md` §4 — the file no
longer reflows; it's one composed frame, the same convention the ingredient
glossary's `components/*.html` already use.

**The AM/PM duality moved from color to surface.** With the amber/violet
palette gone, morning and night needed a different way to read as distinct
at a glance. The system already has exactly one light surface (`--paper`)
and one dark surface (`--ink`) — so Morning sits directly on the page
(`--paper`, `--ink` text) and Night is a raised dark card (`--ink` fill,
`--elev-2`, `--r-4`) inset into it. Day is the page; night is a window cut
into it. No new hue anywhere — the light/dark split *is* the AM/PM content,
not a decoration on top of it.

**Chrome.** `SeoulHabit` wordmark (top-left) / `Routine Checklist` doc-tag
(top-right), both `--font-mono`, matching the catalog-reference convention
already established by the ingredient glossary's cards.

**Icons.** Routine-header badges use `Icon.jsx`'s own `ICON_ROLES.am`
(`sun`) and `ICON_ROLES.pm` (`moon`) verbatim — an exact match already in
the system, not a choice. Per-step icons are a harder case: `ICON_ROLES` has
no role for cleanser, toner, moisturizer, etc., and the system's entire
icon vocabulary is the 17 Lucide glyphs in `assets/icons/`. Rather than
invent new path data — banned by `Icon.prompt.md` ("geometry is copied, not
drawn") — steps are mapped to the closest existing glyph, repeating within
the shape the system already accepts (the ingredient glossary reuses one
glyph across all twenty ingredient cards on the same reasoning):

| Step | Icon | Why |
|---|---|---|
| Cleanser | `droplet` | Rinse-off, literally water |
| Toner | `flask-conical` | Liquid formulation |
| Antioxidant Serum | `flask-conical` | Same formulation family as Toner |
| Moisturizer | `droplet` | Hydration |
| Sunscreen | `sun` | Direct match, and echoes the AM badge |
| Treatment | `gauge` | Targeting a specific concern |
| Serum or Booster | `flask-conical` | Formulation family |
| Night Cream | `moon` | Direct match, echoes the PM badge |

Deliberately not used: `syringe` (the system's `injected` role elsewhere —
reusing it here would misstate a topical step as an injection route) and
`leaf` (the system's `ingredient` role — this component is explicitly
ingredient-agnostic, so borrowing the ingredient glyph would misstate that).
Text still carries the actual meaning (step name + description); the icon
only labels the kind of thing on screen, per `Icon.prompt.md`'s own rule
that removing every icon must not change what the frame asserts.

**Motion.** One-time rise-in on load — `--e-out`, `--d-base` (500ms),
per-step stagger — instead of the scroll-triggered version. No infinite
loops anywhere in the file.

**Ordinal marks.** The old per-step leader-line-and-number was specific to
this file, not a system pattern. Replaced with a plain `--font-mono` index
column (`01`–`05`) to the left of each icon, closer to how the ginseng
card's own `06 · 20` index reads.

### Deliberately not attempted

`design-system-spec.md` names two target components, **`RoutineLadder`**
and **`RoutineChecklist`**. Only the second is built here.
`catalog.md` §5 describes `RoutineLadder` as a "six-rung CSS-perspective"
component and is explicit that "Dawn to Dusk is a flat checklist, not
this" — there's no six-rung content to migrate, so building a ladder
variant here would be inventing a second component this content doesn't
need. Neither component has a file anywhere in the design system yet
(no `components/sequence/` directory exists) — this file is the first
implementation of `RoutineChecklist`, not a consumer of an existing one.

Efficacy claims still need a citation or a `SourceChip` to render under this
system's core rule. Nothing here makes one — all ten lines are procedural
("what this step does"), not effect claims — so no chip was added; adding
one would assert a rigor this content doesn't have.

**Status.** No longer "no stated design laws" — the laws are now the ones
above, inherited from the design system rather than invented locally. Still
a catalog reference, not wired into `build.mjs` or a `videos/` project.
