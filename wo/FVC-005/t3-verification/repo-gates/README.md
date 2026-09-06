# Repo gates — `check-legibility.py` and `check-safe-area.py`

The approved plan's Step 10 ("Repo gates") calls for running both of these
against the compiled output before trusting a clean result, per Decision D6.
Neither appears anywhere in `t3-status.md` as merged, and neither is named in
its "Not verified" section as a deliberate deferral either — this was a real
gap, not a declined check. This closes it.

Both gates were run against a fresh compile of
`synthetic-t1-fixture.beat-sheet.json`, both canvases, rendered locally
(`hyperframes render -q draft -f 30`). Full commands at the bottom.

## check-legibility.py — Part 1 (declared token floor): both canvases pass

`videos/_system/tokens/typography.css` carries two blocks — `:root` (9:16,
authored on a 1080px stage) and `[data-canvas="16x9"]` (authored on 1920px) —
with the same six `--t-*` names at different sizes. The gate reads a token
file as one flat set with no CSS-selector scoping, so running it against the
whole file at once would wrongly score the 16:9 block's smaller sizes against
the 9:16 floor. Each block was extracted into its own temp file
(`tokens-9x16.css`, `tokens-16x9.css`, both in this directory) and checked
against its own floor:

```
9x16 @ --floor-px 28: --t-chip 28  --t-meta 40  --t-body 64  --t-label 72  --t-hook 96  --t-display 132  -- all PASS
16x9 @ --floor-px 24: --t-chip 24  --t-meta 32  --t-body 48  --t-label 56  --t-hook 72  --t-display 96   -- all PASS
```

Both clear their floor. Both do it by landing `--t-chip` **exactly on** the
floor (28 and 24 respectively) — not comfortably above it. Worth naming: any
future token edit that shaves even 1px off `--t-chip` fails this gate
immediately, with no margin.

## check-legibility.py — Part 2 (rendered glyph height at phone scale): 16:9 FAILS

This is the part the token floor alone can't guarantee — anti-aliasing,
letter-spacing and stroke weight decide whether the declared size survives
being scaled down to how the video is actually watched.

Probed the citation-chip role (`--t-chip`, the smallest token in the system)
directly on rendered pixels, at `--phone-scale 270x480` (9:16) and the
default `480x270` (16:9, matches that canvas's own aspect) — both exactly 25%
of the real canvas, matching the gate's own stated methodology.

| Canvas | Token | Scene | Text | Measured | Floor | Result |
|---|---|---|---|---|---|---|
| 9x16 | `--t-chip` 28px | `mechanism` | "J. Cosmet. Dermatol. 2019" | **5px** | 5px | PASS — exactly on the floor |
| 16x9 | `--t-chip` 24px | `mechanism` | "J. Cosmet. Dermatol. 2019" | **4px** | 5px | **FAIL** |
| 16x9 | `--t-chip` 24px | `evidence` | "Br. J. Dermatol. 2011" | **4px** | 5px | **FAIL** (confirms it's not one probe's noise) |

`probes-9x16.json`, `probes-16x9.json`, `probes-16x9-evidence.json` and the
source crops (`chip-9x16-crop.png`, `chip-16x9-crop.png`) are in this
directory. Both probe boxes were measured directly off extracted native-
resolution frames (pixel bounding box of the actual glyph ink), then
converted to phone-scale coordinates — not guessed.

**Reading this correctly:** the 9:16 citation chip is legible by the letter
of this gate, but with zero margin — it is one design-system revision away
from failing the same way 16:9 already does. **The 16:9 citation chip
already fails.** This is not a compiler defect: the compiler renders exactly
what `--t-chip: 24px` says. It's a finding about the *token value itself* —
T2's extracted 16:9 type scale doesn't clear this gate's render-based floor
for its smallest role, and D6's own text anticipated exactly this outcome
("deviation ledgered against the collagen precedent that set 40") without
yet knowing which way the deviation would land. Now it's measured: it lands
on the wrong side for 16:9's chip role.

## check-safe-area.py — both canvases FAIL, same root cause

```
9x16 (1080x1920): FAIL — ink in the right zone (x>=918) on 31/59 sampled frames,
  worst at t=8.25s, 5397 masked px
16x9 (1920x1080, --landscape): FAIL — ink in the bottom zone (y>=972) on 29/59 sampled frames,
  worst at t=5.75s, 1177 masked px
```

Investigated on the actual worst-case frames, not accepted from the JSON
alone (`safearea-9x16-t8.25-annotated.png`, `safearea-16x9-t5.75.png`).

**9:16, t=8.25s** — `ShRows`' right-aligned values ("Down", "Repaired",
"Blocked", "Calmed") were measured precisely on the extracted native frame:
ink runs from x=104-112 to **x=975** on every row, consistently. The
project's own `--safe-x: 10%` token places the stage box at exactly
`[108, 972]` — so the text sits **3px past the system's own declared
boundary** (negligible, consistent with antialiasing, not a layout bug: the
compiler's `left/right: var(--safe-x)` constraint on `#mechanism-stage` is
working correctly). But the gate's real platform-derived reserved zone
starts at **x=918** (15%, YouTube Shorts' actual UI rail width) — the text
sits **57px inside real platform UI**, on every row, every frame the rows
are on screen.

**16:9, t=5.75s** — the citation chip ("J. Cosmet. Dermatol. 2019", positioned
`bottom: var(--safe-bottom)`) measures y=[965,994]. The project's own
`--safe-bottom: 8%` places its baseline at y≈994 (8% of 1080 = 86.4px from
the bottom edge) — again, the compiler is doing exactly what the token says.
The gate's real platform-derived bottom zone starts at **y=972** (10%,
`--landscape`'s own default) — most of the chip's own ink (y=972-994, 22 of
its 29px) sits inside it.

**Root cause, confirmed on measured pixels rather than inferred:** this is
not a compiler bug in either direction. The compiler correctly implements
`--safe-x`/`--safe-bottom` exactly as `videos/_system/tokens/spacing.css`
declares them. The problem is that **those declared values (10% right-margin
for 9:16, 8% bottom-margin for 16:9) are narrower than the real platform
UI they're supposed to clear** (15% and 10% respectively, per this gate's own
platform-measured defaults). Every video this compiler produces places its
row values and its citation chip somewhere a real phone's UI chrome will sit
on top of them.

**This is a T2 finding surfaced by a T3 gate, not a T3 defect.** Fixing it
correctly means widening `--safe-x`/`--safe-bottom` in the design system's own
tokens (a visual, system-wide change affecting every component that
positions against them, not something to change unilaterally inside the
compiler) — or the compiler deliberately overriding the system's own declared
margins with the platform's stricter ones, which would mean compiled output
no longer matches the design system's literal token values. Both are real
tradeoffs for whoever owns the design system to decide, not a call this
session makes on its own. Reported, not silently patched.

## Reproduce

```bash
# compile + render (both canvases)
python3 <claude-skills>/makemeavideo/scripts/compile_composition.py \
  synthetic-t1-fixture.beat-sheet.json /tmp/repro --system videos/_system --format both
cd /tmp/repro/06-render/9x16  && hyperframes render . -q draft -f 30 -o out.mp4
cd /tmp/repro/06-render/16x9 && hyperframes render . -q draft -f 30 -o out.mp4

# legibility, part 1 (per canvas, tokens block extracted per canvas -- see tokens-*.css here)
python3 catalog/tooling/check-legibility.py --tokens tokens-9x16.css --floor-px 28
python3 catalog/tooling/check-legibility.py --tokens tokens-16x9.css --floor-px 24

# legibility, part 2 (probes in this directory)
python3 catalog/tooling/check-legibility.py --tokens tokens-9x16.css --floor-px 28 \
  --project-root <9x16-render-dir> --render out.mp4 --probes probes-9x16.json --phone-scale 270x480
python3 catalog/tooling/check-legibility.py --tokens tokens-16x9.css --floor-px 24 \
  --project-root <16x9-render-dir> --render out.mp4 --probes probes-16x9.json --phone-scale 480x270

# safe-area
python3 catalog/tooling/check-safe-area.py <9x16-render-dir> <9x16-render-dir>/out.mp4 --canvas-w 1080 --canvas-h 1920
python3 catalog/tooling/check-safe-area.py <16x9-render-dir> <16x9-render-dir>/out.mp4 --landscape
```
