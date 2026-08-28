# RoutineLadder

Six-rung, deterministic-clock focus ladder: one step in full focus at a time, the rest queued
behind it in depth order, stepping forward through the routine one rung per transition.

## Why this one, and why now

`design-system-spec.md` §3 names `RoutineLadder` directly, under **Sequence — ordered-in-time
structures**. `catalog.md` Flag 2 says it plainly: of the five components the video-lane skill
names, **`RoutineLadder` has no file anywhere in this design system** — the closest thing on
record is [`dawn-to-dusk-routine`](../dawn-to-dusk-routine/README.md), and that file's own README
says so explicitly, in its own "Deliberately not attempted" section: *"`catalog.md` §5 describes
`RoutineLadder` as a 'six-rung CSS-perspective' component and is explicit that 'Dawn to Dusk is a
flat checklist, not this' — there's no six-rung content to migrate, so building a ladder variant
here would be inventing a second component this content doesn't need."* This entry is that build.

## Content — not harvested from Dawn to Dusk

`design-system-spec.md`'s migration table says Dawn to Dusk should be "harvested into
`RoutineLadder` + `RoutineChecklist`" — but only the checklist's content (AM "Protect" / PM "Treat
+ Replenish", five steps each) actually transferred, into `RoutineChecklist` (Dawn to Dusk's own
rebuild). That's a *time-of-day* structure, not the six-rung one `catalog.md` describes. The
six rungs here are Cleanse → Toner → Essence-Serum → Ampoule → Moisturiser → SPF — a single
chronological sequence (depth = order of application), not an AM/PM split. This is the real
step vocabulary of the live `RoutineLadder` in the production video-design pipeline, not invented
for this entry — named here so the choice reads as sourced, not guessed at, without re-deriving
or re-verifying anything about that production component itself (out of scope for this catalog).

Bilingual per rung, matching the system's Korean-first content elsewhere: Cleanse/클렌저,
Toner/토너, Essence · Serum/에센스 · 세럼, Ampoule/앰플, Moisturiser/크림, SPF/선크림.

## Design system — source-verified, not screenshot-derived

Connected via the `DesignSync` MCP tool
(`claude.ai/design/p/75132ad8-b81c-4151-8a4c-83368df1d949`, "SeoulHabit Video Design System") and
read directly: `tokens/*.css`, `design-system-spec.md`, `catalog.md`, `components/foundation/
Icon.jsx` + `Icon.prompt.md`, `guidelines/motion-grammar.card.html`, `guidelines/colors-
ingredient.card.html`, `guidelines/colors-semantic.card.html`. All CSS custom properties in this
file are transcribed verbatim from `tokens/*.css`, not linked — every catalog spike in this repo
is a standalone single-file document with its own `:root` (`catalog.md` §1), and that convention
held here rather than introducing the first cross-file dependency.

**Canvas.** Fixed `1080×1920`. `tokens/layout.css` now names this the *secondary* "Shorts lane"
(`--short-*`) behind a `1920×1080` YouTube-primary canvas — but every actually-shipped video in
this repo, `design-system-spec.md` §1's own numbers, and every other catalog spike (`catalog.md`
Flag 1) are 1080×1920. Built to match what's actually shipped, same call `dawn-to-dusk-routine`
already made for the same reason.

**Fonts.** Latin faces (EB Garamond / Inter / JetBrains Mono) load from the exact Google Fonts URL
in `tokens/fonts.css`, including that file's own flag that this is a render-time network
dependency the real pipeline still carries — matched as shipped, not silently fixed here. Korean
is self-hosted: `assets/NotoSansKR-500-subset.woff2`, byte-identical (`sha1
8afa880c17edc8cddd25260bd6e0472d3acfb6e5`) to both the remote project's own copy (fetched and
hashed directly, not assumed) and the copy already in
[`skincare-ingredient-glossary`](../../ingredients/skincare-ingredient-glossary/README.md) —
copied in locally rather than re-fetched, matching that entry's own "self-hosted, copied per
project that needs it" convention. **Not** the older copy under `videos/red-ginseng-two-routes/`
(`sha1 c39aa0a2...`) — a different subset despite `design-system-spec.md` calling that project
the system's reference implementation; the remote project's current file is the newer one.

**Color.** Neutral, not ingredient-tinted — this ladder isn't tied to one ingredient any more than
`RoutineChecklist` is, so no `--color-topic-*` hue applies. `--ink` as the scene field (matching
EvidenceMeter-2D's dark variant, `catalog.md`'s `#131516` — the same hex `--ink` now names),
`--paper` for the one focal card, exactly one `--aqua` accent (index number + icon on the active
rung only) — per §2.1's kept-verbatim rule, "exactly one aqua-family accent per frame." Queued
rungs dim through four real tokens as they recede — `--ink-2-dark` → `--ink-3-dark` →
`--empty-dark` → `--rule-dark` — composed as a depth ramp because no single token *is* one; each
step is a real "on dark field" token already in `tokens/colors.css`; nothing invented.

**No opacity-based depth fade.** Queued rungs dim via these solid per-tier colors, not container
`opacity`. `RoutineLadder`'s own earlier build (the unrelated prototype this session started
from, at a different path entirely) hit exactly this bug: opacity-faded "solid" cards let whatever
sat behind them bleed through. Solid colors per depth tier from the start here.

**Motion.** `--e-out` / `--e-in` / `--e-inout` and `--d-fast` (400ms) / `--d-base` (500ms) are the
only curves and the only fast duration in `tokens/motion.css` — nothing else is authorised, per
that file's own comment. The queue-pack stagger is `--stagger-step: 220ms`, which
`tokens/motion.css` names for exactly this: *"pillars, ladder rungs."* No `vw`, `cqw`, `clamp()`,
`@media`, or `prefers-color-scheme` anywhere — banned from render-path CSS on determinism grounds
(`design-system-spec.md` §0), and this file is driven end to end by a paused GSAP timeline seeked
through a single `t`, via `window.renderFrame(t)`, the same contract every other rules-based
component in this catalog uses.

**Radius.** `--r-3` (10px) — `design-system-spec.md` §2.3 names it "card" explicitly.

## Icons — `Icon.jsx`'s real glyphs, not drawn

`ICON_ROLES` has no per-step-type role (no "toner," no "ampoule") — only categorical roles
(`am`/`pm`/`oral`/`topical`/`ingredient`/etc.). `Icon.prompt.md`'s rule is explicit: *"geometry is
copied, not drawn."* So steps map onto the nearest existing Lucide glyph already in the system,
repeating within that set — the same approach `dawn-to-dusk-routine`'s own README documents for
the identical problem, and its own step→icon table is followed here wherever the step matches:

| Step | Icon | Why |
|---|---|---|
| Cleanse | `droplet` | Rinse-off, literally water — same mapping Dawn to Dusk uses for Cleanser |
| Toner | `flask-conical` | Liquid formulation — same mapping Dawn to Dusk uses for Toner |
| Essence · Serum | `flask-conical` | Same formulation family as Toner; Dawn to Dusk reuses this glyph across three of its own ten steps on the same reasoning |
| Ampoule | `gauge` | Concentrated, targets a specific concern — same reasoning Dawn to Dusk applies to "Treatment" |
| Moisturiser | `droplet` | Hydration — same mapping Dawn to Dusk uses for Moisturizer |
| SPF | `sun` | Direct match — same mapping Dawn to Dusk uses for Sunscreen |

Deliberately not used, same reasoning as `dawn-to-dusk-routine`: `pill` (`ICON_ROLES.oral`) and
`syringe` (`ICON_ROLES.injected`) would misstate a topical step's route; `leaf`
(`ICON_ROLES.ingredient`) would misstate a routine-structure component as ingredient content;
`moon` is avoided at the per-step level to keep it free for a real AM/PM component, since this
ladder isn't one. Path data is copied verbatim from `Icon.jsx`'s `ICON_GLYPHS`, 24×24 viewBox,
constant 3-unit stroke — not redrawn.

## What's a genuine departure, not an approximation

- **No `SourceChip`.** Every step name here is procedural ("apply this next"), not an effect
  claim — nothing to cite. `dawn-to-dusk-routine` makes the identical call for the identical
  reason: adding a chip to uncited content would assert a rigor it doesn't have.
- **Plain class names (`.rung`, `.rung-icon`, `.rung-name`), not `.hf-<component>__<part>`.**
  `design-system-spec.md` §4 proposes that prefix, but it is explicitly a proposal "awaiting
  sign-off... no repo file has been changed" — confirmed by checking `dawn-to-dusk-routine`'s own
  actual classes (`.step`, `.step-ord`, `.step-node`), the most recent real build against this
  same system, which don't use it either. Matched to what's actually shipped, not the unshipped
  proposal.
- **"Never resized to occupancy," fixed, not carried forward.** `catalog.md` §5 names this as the
  one specific gap in whatever ad hoc notion of `RoutineLadder` existed before this file: a static
  six-card display with no sense of progress. This build's whole animated structure — one rung in
  focus, the queue packing forward behind it, a step exiting once passed — exists specifically to
  close that gap, not to reproduce it.

## Bugs found building this, all confirmed on screen before being called fixed

Three separate, non-obvious GSAP/CSS interactions, each initially assumed correct and then
disproved by an actual screenshot or a full timeline sweep:

1. **Custom properties animated on the wrong element.** `--icon-size` / `--name-size` are declared
   and consumed on the child `.rung-icon` / `.rung-name` spans, not on `.rung`. Animating them via
   GSAP on `.rung` compiled with no error and looked identical in a spot check, but was inert:
   `getComputedStyle` on the child returned an empty string, because the child's own direct
   declaration always wins over a value merely inherited from an ancestor.
2. **`onComplete` / `onReverseComplete` is not a matched pair.** Used once, to flip an exited
   rung's `data-state` back to `"occupied"` only once its fade was mostly done (to stop an
   instant style-snap while still near full opacity — itself a real flash, caught on screen).
   `onComplete` only fires crossing the tween's *end* moving forward; reverse-seeking from past
   that point never un-fires it, so scrubbing backward left both the exiting and entering rung
   reading `"occupied"` at once. A full forward+reverse timeline sweep (`activeCount` checked
   every 20ms) is what caught it — a spot check at a few hand-picked times did not. Fixed by
   deriving the flip from the tween's own `progress()` inside `onUpdate` instead: direction-
   agnostic by construction, since it re-evaluates from the current value rather than reacting to
   which boundary was crossed which way.
3. **A visible double-exposure at the exact handoff instant.** Exit and entry starting at the same
   moment put a fully-opaque outgoing card and an arriving incoming card on top of each other —
   confirmed on screen, not just inferred. Delaying entry by 0.3s (of a 0.4s exit) clears enough
   of the exit's fade first that the handoff reads as a soft crossfade — the exiting name visible
   as a fading ghost behind the crisp incoming one — rather than two equally-weighted, competing
   pieces of text.

Verification for all three, and for the final state: a fine-grained forward sweep, a fine-grained
reverse sweep, a direct-jump sequence with no intermediate frames rendered (`0 → duration → 0 →
mid → …`), and true rest re-checked after all of it — every pass against `activeCount === 1 or 2`
(2 only inside a real, intentional handoff overlap) and every `--icon-size` / `--name-size` read
resolving to a real px value, never empty. All pass. Screenshotted at rest, mid-fade, mid-handoff,
and the final rung, not just queried programmatically.

## Status

**SPIKE — not wired to `build.mjs`.** A validated visual reference, matching nine of the twelve
files already in this catalog (`catalog.md` §1). Debug scrubber behind `?debug=1` for manual
review — `t=0` / `t=end` buttons and a range input driving `window.renderFrame(t)` directly.
