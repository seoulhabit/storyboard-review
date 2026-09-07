# T2 — `retrofit_catalog.py`

Script: [`videos/_system/catalog/retrofit_catalog.py`](../../videos/_system/catalog/retrofit_catalog.py)
(614 lines). Shipped and tested per the WO's own bar: "tests over at least
three items of different shapes — one token-native component, one hardcoded
block, one media wrapper." Per the Gate A ruling (registry reduced to
components), "hardcoded block" is read as **hardcoded component** — no
block is in scope for this WO's registry at all. The three real items used:

| Item | Shape | Real upstream colour handling |
|---|---|---|
| `focus-swap` | token-native | zero hex/rgb literals — 100% its own `var(--fg)`/`var(--surface)`/etc. vocabulary |
| `caption-highlight` | hardcoded | white text, red gradient fill, red/black shadows — zero CSS variables |
| `device-frame-stage` | media wrapper | mixed — device-chrome material colours *and* host-bridgeable tokens in the same file |

All three run clean end-to-end. Full per-item colour role maps are published
alongside each retrofitted file (`videos/_system/catalog/<name>.colormap.json`)
— per the WO's own instruction, this is "the single most consequential
artifact in this WO," so every substitution decision is there to review, not
just asserted here.

---

## What the script does, in order

1. **Strip remote font links**, inject the design system's real 5-face
   `@font-face` block (DejaVu Serif 400/700, Archivo variable, Noto Serif KR
   400/700 for Hangul) — root-relative, not base64, per the WO's own
   corrected T2 step 1.
2. **Recolour to tokens** — the real engineering centre, three distinct
   mechanisms depending on what the source item actually does (see below).
3. **Pin GSAP** to `../vendor/gsap-3.14.2.min.js`.
4. **Record aspect** — `"n/a-embeds-in-host"` for every component (per T0a's
   structural finding: components declare no native canvas), plus the T0b
   working-set verdict when the item was in that 36-item scan.
5. **Emit a manifest entry** to `videos/_system/catalog/manifest.json`:
   name, upstream commit (the real version anchor — this registry carries no
   per-item version numbers), retrofit script version, aspect, classification,
   colormap path, output hash.

## Recolouring — three real cases, three real mechanisms

The WO's own spec ("parse every colour literal... map it to a design token
by role") describes only one of these. Building against real items surfaced
the other two; all three are load-bearing, not incidental:

**1. Literal substitution** (`caption-highlight`). Every hex/rgb(a) is
classified by HSL distance to the nearest of the nine design tokens (six
foundation + three semantic, per G0-8), with a `color:`-property tie-break
(text can't be classified against `surface`/`surface-raised` — a background
tone as a text colour is never the real intent) and a `box-shadow`/
`text-shadow`/`filter` exemption for low-saturation neutrals (a depth cue,
not a brand hue). Alpha is preserved via `color-mix(in srgb, var(--token)
N%, transparent)`. Anything outside the distance threshold halts loudly,
naming the literal — never guessed.

**2. Token bridging** (`focus-swap`, and half of `device-frame-stage`).
Some items carry zero literals because they already read entirely from
their *own* custom-property vocabulary (`--fg`, `--surface`, `--border`,
`--font-body`...), meant to be supplied by whatever hosts them. The
"recolour" step here isn't substitution — it's aliasing: a `:root` block
mapping the item's own names to the design system's real tokens
(`--fg: var(--ink)`, `--surface: var(--bg-lift)`), injected once, so the
item's own CSS is untouched and simply inherits real values through
properties it already reads.

**3. Foreign-surface protection** (`device-frame-stage`). The source item's
own comment says its device-chrome colours are *"physical-material law...
not brand paint... do not swap in --radius/--space-*."* The script detects
this pattern generically — any custom-property **name** first declared
inside a comment-marked block is protected everywhere it's redeclared
elsewhere in the file (the silver-variant override reuses
`--device-color`/`--device-color-hi`/`--device-color-dark` without repeating
the comment, and is still protected, because the name carries the
documented intent, not the textual proximity to the comment). This is R-13's
`foreign-surface` classification, generalised from the one real example that
prompted it rather than hardcoded to that item's name.

## Two real bugs, caught by actually rendering the output — not asserted from source reading

Per R-13: *"a 4.5:1 contrast check on rendered pixels — not on declared CSS
values."* Both retrofitted test items with text were loaded in the Browser
pane with the real `colors.css` injected (matching how they'll actually be
hosted), and checked with real `getComputedStyle()` reads, not a re-parse of
the source.

**Bug 1 — self-referencing token bridge.** `focus-swap`'s own local
vocabulary happens to use `--bg` and `--muted` — names that are *themselves*
real design-system tokens, not aliases needing one. The first version of the
bridge logic wrote `:root { --muted: var(--muted); }` after `colors.css`'s
own `:root { --muted: rgba(...) }` — a self-reference, which CSS treats as
invalid, silently reverting the property to whatever it would otherwise
inherit. Caught by rendering `.fs-status` (`color: var(--muted)`) and
finding it resolved to fully-opaque ink instead of the intended 0.75-alpha
muted tone. **Fixed**: any local var name that collides with a real design
token name is now skipped entirely — colors.css already supplies it, and
writing a bridge for it is actively harmful, not redundant. Re-verified:
`.fs-status` now resolves `rgba(38,33,92,0.75)` correctly, blended contrast
6.18:1 against its actual background — real number, alpha correctly
accounted for, not the naive 13.09:1 an unblended read would have shown.

**Bug 2 — foreign-surface marker scoped by text proximity, not property
identity.** The first version only set a whole-item classification flag
*after* every literal was already substituted — it didn't actually stop
`device-frame-stage`'s graphite trio (`#1b1d22`/`#343740`/`#111318`) from
being silently forced into `var(--ink)` and friends by nearest-colour
distance. The silver-variant override (`#c9cdd3`/`#eef1f4`/`#9a9ea6`,
declared in a *separate* rule block with no repeated comment) correctly
failed loudly as unclassifiable, but only by accident — it happened to fall
outside the distance threshold. **Fixed**: protection is now keyed to the
custom-property *name*, scanned once for every declaration of that name
anywhere in the file. Re-verified: `--device-color` still resolves
`#1b1d22` unchanged in the retrofitted output; `.device-screen`'s `background:
var(--surface, #f5f6f8)` correctly resolves to `rgb(250,243,231)` (`--bg-lift`)
— the *bridgeable* token in the same file, correctly distinguished from the
*protected* one three lines away.

Both bugs would have shipped invisibly if verification had stopped at "the
script runs and produces plausible-looking output" — the first only shows up
in rendered alpha compositing, the second only shows up when the same
property name is legitimately reused in two different rule blocks. Neither
is visible from reading `colormap.json` alone.

## Known limitations, stated rather than hidden

- **Global string replace, not an AST rewrite.** Substitution matches by
  literal string value across the whole file. If an identical literal
  appears in both a protected and a substitutable context in the same item,
  both move together. Not a risk for the three test items (checked
  directly); worth a real fix (position-scoped replacement) before running
  at full-catalog scale if it ever bites.
- **Raw-DOM contrast check, not a seeked-frame check.** Verification reads
  computed styles from the unplayed initial layout, same caveat as T0b.
  Colour/contrast values are static regardless of animation state for every
  item checked here, so this doesn't change the result — but it's a real
  scope limit, not a guarantee for every future item.
- **`TOKEN_BRIDGE_MAP` and `INTERNAL_VARS` are hand-curated, not inferred.**
  Every future item's local vocabulary gets checked against these two
  tables; an unrecognised name halts rather than guesses (by design — see
  `--logical-width`/`--logical-height`/`--screen-scale`, confirmed by
  reading `device-frame-stage`'s own script before exempting them, not
  assumed safe).
- **The Browser pane can't load a relatively-pathed local script.** Files
  outside a live dev server render as disconnected snapshots; verification
  swapped the vendored GSAP path for jsdelivr's CDN copy in throwaway test
  copies only (never in the committed retrofitted output, which correctly
  keeps the relative vendored path per spec). GSAP path substitution itself
  was verified by direct string inspection, not by this workaround.

## Semantic tokens (G0-8) — now real, not placeholder

`videos/_system/tokens/colors.css` gained three tokens as this task's own
first sub-step, per the WO's amended T2 spec:

- `--positive: #2F5940` (6.89:1 against `--bg`)
- `--warning: #7A5A0F` (5.48:1)
- `--info: #2E5C6E` (6.29:1)

All three clear R-13's 4.5:1 floor with real margin. `MANIFEST.json`
re-hashed and amended (67/67 tracked files re-verified clean —
`check_manifest()` will pass).
