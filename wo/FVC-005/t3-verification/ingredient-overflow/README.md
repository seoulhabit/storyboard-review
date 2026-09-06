# ShIngredient overflow verification

Proves a class of bug found once already (`ShCompare`'s grid overflow)
recurs in a different emitter through a different CSS mechanism —
prompted by testing `ShIngredient` deliberately with a long, unbreakable
name rather than waiting for it to surface by accident.

## The fixture

`ingredient-overflow.beat-sheet.json`: one scene, `ShIngredient`, `name`
and `inci` both set to `"Polymethylsilsesquioxane"` — a real INCI term (a
silicone elastomer powder used in cosmetics), 24 characters, no spaces or
hyphens, genuinely unbreakable under normal line-wrapping rules. Chosen
deliberately as a worst case: cosmetic-chemistry ingredient names are
frequently long compound words with no natural break point.

## The bug, found on the first compile

`hyperframes check` returned a `canvas_overflow` warning far larger than
the earlier `ShCompare` case: `#define-name`'s box measured **1895.89px
wide — nearly double the 1080px canvas** — overflowing the right edge by
923.89px, held for the scene's entire visible duration (44 occurrences,
0–3.95s).

Root cause, structurally the same defect class as the `ShCompare` bug but
via flexbox instead of grid: `#cid-name` sits inside `#cid-wrap`, a
`display:flex; flex-direction:column` container, which is itself a flex
*item* of `#cid-stage`. Flex items default to `min-width:auto`, which
resolves to the largest descendant's min-content width. `text-wrap:balance`
only balances line lengths **once wrapping already happens** — it does
nothing when a single word has no space or hyphen to wrap at, so the
unbreakable 24-character name's full-width rendering became `#cid-name`'s
(and therefore `#cid-wrap`'s) min-content width, and the flex item refused
to shrink below it regardless of the safe-area bounds around it.

## The fix

Two changes, both necessary — one alone would not have fixed it:

1. `min-width:0` on `#cid-wrap`, so the flex item can actually shrink to
   its container's width.
2. `overflow-wrap:anywhere` (not the legacy `overflow-wrap:break-word`)
   on `#cid-name`/`#cid-inci`/`#cid-fn`. This distinction is real: per the
   CSS Text spec, `anywhere` — unlike `break-word` — changes an element's
   *min-content contribution*, which is what actually lets `min-width:0`
   take effect for a flex/grid sizing calculation. `break-word` alone
   would look identical on an already-sized box but silently fail to
   shrink the box's own computed min-content width in the first place.

## Verified, after the fix

- `hyperframes check --samples 40 --at-transitions --json`: `"ok": true`,
  every one of lint/runtime/layout/motion/contrast at `errorCount: 0` AND
  `warningCount: 0` — `check-9x16.json`, captured verbatim.
- The second static gate, `lint_composition.py`: `0 error(s), 0
  warning(s) across 2 file(s)`.
- Determinism: two independent compiles, `diff -r`, empty.
- **No regression** on any of the three prior fixtures (`synthetic-t1`,
  the D5 split, and the four-emitter fixture), all re-verified clean on
  9x16 after this fix.
- A real local render: exactly 4.000s. `frame.png`, extracted at t=2.0s,
  shows the name correctly broken mid-word into three lines
  ("Polymethyl" / "silsesquiox" / "ane"), fully inside the safe area with
  margin on both sides — not elegant typography for this specific edge
  case, but on-canvas and legible, which is what the gate actually
  requires.

## Worth flagging, not fixed here

This is the **second** emitter found to have the same underlying class of
defect (an unconstrained flex/grid child with no `min-width:0` and no
`overflow-wrap` guard on a text node that could plausibly grow
unboundedly). The other seven emitters (`ShHook`, `ShRows`, `ShSteps`,
`ShMyth`, `ShQuote`, `ShEvidence`, `ShEndcard`) have not been
systematically audited for the same gap — each has only been proven
against the specific slot content used in its own fixture, none of which
happened to include a single unbreakable long word. A worthwhile follow-up
is a deliberate stress pass across all nine components with adversarial
text (very long single words, very long numbers/figures, very long
attribution strings) rather than continuing to find these one at a time.

## Reproduce

```
python3 <claude-skills>/makemeavideo/scripts/compile_composition.py \
  ingredient-overflow.beat-sheet.json /tmp/ingredient-repro \
  --system videos/_system --format 9x16
cd /tmp/ingredient-repro/06-render/9x16
hyperframes check --samples 40 --at-transitions --json
hyperframes render -q draft -o out.mp4
```
