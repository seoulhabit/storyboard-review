# The 1% K-Beauty Secret Brands Are Hiding

A rendered label-literacy explainer, not a single-ingredient piece like the
other entries in this folder — catalogued here as one entry, the same way
[Skincare Ingredient Glossary](../skincare-ingredient-glossary/README.md) is.

**Project:** `../../../videos/kbeauty-one-percent-line/` — 8 (+1) frame,
1080x1920, ~1:56 Shorts explainer teaching two label-reading loopholes: the
extract-dilution trick ("70% Centella Extract" usually means a tiny bit of
plant steeped in mostly water) and the legal 1%-ordering rule (ingredients
are listed by concentration only until the 1% mark; after that, order means
nothing). A live teardown of the Beauty of Joseon Glow Serum's real
published INCI list, then a Hanbang (traditional Korean herbal) INCI-to-
common-name cheat sheet — Snail Secretion Filtrate = Snail Mucin, Panax Root
= Ginseng, Artemisia Princeps = Mugwort.

**Rendered:** `renders/kbeauty-one-percent-line_2026-08-29_17-13-53.mp4` —
115.5s, 1080x1920 (confirmed via `ffprobe`). Passed `npm run check`
(lint/runtime/layout/motion/contrast) clean.

**Status:** in review — round 2 of a planned 3 feedback passes with the
creator, following a skill-review pass (2026-08-29) that fixed the video's
own craft gaps (all-crossfade transitions producing muddy near-blank
midpoints, ~60s of the runtime with no authored visual change, several
elements landing past the Shorts safe-bottom line) alongside a companion fix
to the `faceless-video-craft` skill itself, which had drifted from the real
HyperFrames API. Full change log: `STORYBOARD.md`'s "Build history" section
in the project folder.

## Ingredient photography — reused, not duplicated

Frame 4b ("Beyond the Label," a 3s wordless B-roll interlude — the one
photographic beat in an otherwise fully typographic/vector video) uses
three stills from [`ingredient-photography/`](../../ingredient-photography/README.md):
[`06-ginseng.png`](../../ingredient-photography/06-ginseng.png),
[`12-snail-mucin.png`](../../ingredient-photography/12-snail-mucin.png), and
[`18-mugwort.png`](../../ingredient-photography/18-mugwort.png) — the same
three ingredients Frame 7 later Hanbang-translates, in the same order, so
the beat also primes that reveal. Downsampled to 1400px and copied into the
project's own `assets/images/` (project-local paths, matching how fonts and
audio are always project-local in this catalog's video conventions) rather
than referenced from this shared path directly. Confirmed pixel-identical
to the source catalog files (accounting for the resize) during the
2026-08-29 skill-review pass — logged here as a working example of the
"check the catalog before generating a new plate" rule, not a gap: this
project got it right the first time.

No new imagery was generated for this project.

## Product photography — one authorized exception, filed here

Frame 1's hook uses [`product-photography/A01-01.png`](../../product-photography/assets/A01-01.png)
(unbranded frosted celadon dropper bottle, manifest-verified) as a blurred,
scrim-tinted background layer, per round-2 creator feedback asking for a
recognizable physical product to open the hook on. This is a real
exception to two standing rules, both checked before acting rather than
assumed past: `product-photography/README.md` states these assets are
"not HyperFrames assets... needs its own filed decision record first,"
and the `seoulhabit-video-3d` skill states "Browser-drawn only... No
generative imagery, ever." The creator explicitly authorized full catalog
use for this project in-session, which is what unlocked this — logged
here as that authorization's filed record, since the chat lane that
granted it can't write to `docs/decisions/` directly. Copied
project-local to `assets/images/hook-bottle-photo.png` (1080px, downsampled
from the catalog's 1536x2752 original), matching how every other asset in
this project is referenced locally rather than from the shared path.

## Visual components — checked, none applicable

Prompted by creator feedback asking whether the catalog's `visual-components/`
library was checked before building each scene's mechanism (it hadn't been —
the skill's reuse rule only covered plates until this pass, now fixed in
`faceless-video-craft` production-loop step 4). Checked each of the five
existing components against this video's actual content, not just their
category label: `SplitFaceProtocol` reads like a fit for Frame 3's
split-screen but is a literal clinical bilateral-face SVG (control-arm/
active-arm treatment zones), not a generic two-column layout; `EvidenceMeter`
requires an `ING-*` source citation, which this topic explicitly has none of
(general label-reading literacy, not a single ingredient's evidence record —
see the project's own `frame.md`); `GradedScale`, `RoutineLadder`, and
`Dawn-to-Dusk`/`CelestialArc` are confidence-scale, routine-sequence, and
AM/PM-specific. None apply — a real finding from checking, not an assumption
from skipping the check.
