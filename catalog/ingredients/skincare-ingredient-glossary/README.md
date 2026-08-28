# Skincare Ingredient Glossary

A rendered reference glossary, not a single-ingredient piece like the other
entries in this folder — catalogued here as one entry rather than split
across twenty mostly-empty ingredient folders.

**Project:** `../../../videos/skincare-ingredient-glossary/` — rendered
(`renders/skincare-ingredient-glossary_2026-08-27_21-23-54.mp4`, 76s,
1080×1920, confirmed via `ffprobe`). Twenty ingredients, in order: AHA/BHA,
Centella Asiatica, Bamboo Extract, Green Tea, Birch Sap, Ginseng, Bifida
Ferment Lysate, Hyaluronic Acid, Ceramides, Niacinamide, Peptides, Snail
Mucin, Panthenol, Soybean Extract, Propolis, Retinol, Royal Jelly, Mugwort,
Rice Extract, Vitamin C. Each gets a name / Korean gloss / category / "what
it is" / "commonly used for" card.

## Design system

Restyled against the **SeoulHabit Video Design System** (shared Claude
Design canvas), replacing the original standalone palette: flat ink
`#131516` field (no gradients, no glow — the system bans both), the
`--color-topic-ingredient` → perilla green identity, EB Garamond display /
Inter body / JetBrains Mono technical / Noto Sans KR for Hangul, the
system's own type scale, spacing steps, radii, and the exact
`--e-out`/`--e-in`/`--e-inout` cubic-bezier motion curves at token durations
(`--d-snap`, `--d-fast`, `--d-base`, `--stagger-line`). Icons are
hand-approximated in Lucide's outline style (24×24, `currentColor`, no
per-ingredient accent) — not literally copied from the `lucide-icons/lucide`
package, since that wasn't available to fetch here; flagged rather than
silently claimed as verbatim.

**Content caveat, stated plainly:** the design system's core rule is that
any on-screen claim of efficacy carries a source id or does not render. This
glossary's "commonly used for" lines come from a general ingredient chart,
not cited studies, so they're kept descriptive rather than phrased as
sourced claims, and the outro card carries an explicit disclaimer
("General ingredient overview — not sourced claims, not medical advice").
They do not meet the system's sourcing bar the way an `ING-*`-cited claim
would — this is a breadth-first pass across twenty terms, not twenty
fact-checked claims.

## Components

`components/` holds all twenty ingredient cards as individual, standalone
HTML files — the same TermDefinition-pattern card as the video, extracted
one-per-file for reuse outside the render (static layout, a one-time CSS
rise-in on load, no GSAP/HyperFrames dependency, matching this catalog's
existing `-spike.html` convention of self-contained reference files):

| # | File | Ingredient |
|---|---|---|
| 01 | `components/01-aha-bha.html` | AHA / BHA |
| 02 | `components/02-centella-asiatica.html` | Centella Asiatica |
| 03 | `components/03-bamboo-extract.html` | Bamboo Extract |
| 04 | `components/04-green-tea.html` | Green Tea |
| 05 | `components/05-birch-sap.html` | Birch Sap |
| 06 | `components/06-ginseng.html` | Ginseng |
| 07 | `components/07-bifida-ferment-lysate.html` | Bifida Ferment Lysate |
| 08 | `components/08-hyaluronic-acid.html` | Hyaluronic Acid |
| 09 | `components/09-ceramides.html` | Ceramides |
| 10 | `components/10-niacinamide.html` | Niacinamide |
| 11 | `components/11-peptides.html` | Peptides |
| 12 | `components/12-snail-mucin.html` | Snail Mucin |
| 13 | `components/13-panthenol.html` | Panthenol |
| 14 | `components/14-soybean-extract.html` | Soybean Extract |
| 15 | `components/15-propolis.html` | Propolis |
| 16 | `components/16-retinol.html` | Retinol |
| 17 | `components/17-royal-jelly.html` | Royal Jelly |
| 18 | `components/18-mugwort.html` | Mugwort |
| 19 | `components/19-rice-extract.html` | Rice Extract |
| 20 | `components/20-vitamin-c.html` | Vitamin C |

Three of the twenty overlap with dedicated entries elsewhere in this
catalog — [Ginseng](../ginseng/README.md), [Snail Mucin
Essence](../snail-mucin/snail-mucin-poster-spike.html), and this project's
own Retinol card (not to be confused with [Retinal vs.
Retinol](../retinal-vs-retinol/README.md), which is specifically about the
retinal/retinol distinction — a different piece with a different job, not
a duplicate). Those dedicated entries are full bespoke posters; these
components are the uniform, design-system-token glossary card — a
deliberately different, consistent format, not a redundant copy.

No `STORYBOARD.md` in this project (unlike PDRN, snail mucin, or red
ginseng), so the ingredient order and card copy above come straight from
`index.html`, the rendered video, and `components/`, not a design-plan
document.
