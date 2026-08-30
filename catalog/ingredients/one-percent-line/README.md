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

**Rendered:** `renders/kbeauty-one-percent-line_2026-08-29_21-40-00.mp4` —
115.5s, 1080x1920, mastered -15.0 LUFS / -1.3dBTP (confirmed via
`ffmpeg ebur128`). Passed `npm run check`
(lint/runtime/layout/motion/contrast) clean.

**Status:** in review — the creator has continued past the originally
planned 3 rounds with further feedback. Round 8: creator flagged that the
ingredient photos across a few frames "take majority of the space" —
measured it precisely rather than assuming (photos never exceed ~9% of
the actual canvas area in any frame) and found the real issue was
perceptual: Frame 3's water/leaf equation becomes the *only* content on
screen once the split-comparison content above it fades out, not because
the photos themselves are large. Fixed by adding content, not shrinking
photos (creator's explicit direction) — a "70% CENTELLA EXTRACT" recap
callback now fills the vacated space, closing the loop with the K-BEAUTY
chip shown earlier in the same scene, and the equation zone grew from a
500px island to 900px, using ~62.5% of the safe vertical column instead
of ~35%. Also built the channel's first YouTube thumbnails for this
video (`assets/thumbnail/`), following the same extract-grade-finalize
convention already established in `seoulhabit-launch` — pulled real
frames from the render rather than authoring a separate composition; see
that section below. Round 7, another Studio comments
pass: real ginseng photography added to Frames 1 and 2 (the hook's
"0.5% GINSENG." payoff and the promise diagram's "BEAKER + TEST" icon,
both reusing the already-approved still), Frame 3's water/leaf photos
enlarged 220->300px to use vertical space the equation zone was leaving
unfilled, and Frames 5-6 got a real text-vs-skill audit against the
`faceless-video-craft` skill's 40px reading-text floor — most violations
fixed, one (Frame 5's 4-name ingredient fan) partially bumped with the
trade-off documented, and one (Frame 6's 14-row real INCI list) left
untouched and flagged as needing a deliberate card redesign rather than a
side-effect change. Two image placements needed a follow-up fix after a
first render showed real problems a lint pass didn't catch: Frame 1's
ginseng photo initially overlapped the VO caption text below it, and
Frame 6's enlarged "1% LINE" tag first attempt clipped off the canvas
edge because it sits inside a 1.8x zoom-push beat. Round 6 was driven by
comments
left directly in HyperFrames Studio (`.hyperframes/frame-comments.json`)
rather than chat: Frame 7's three small stacked ingredient cards became
one big flashcard shown one at a time (still timed to each term's real VO
onset), and Frame 8's recap-chip thumbnails were enlarged 64->88px after
confirming with the creator which "better image" reading they meant. Also
fixed a Studio-only display bug — all 9 frames' plan status was
`rendered`, a value outside Studio's actual schema (`outline` / `built` /
`animated`), so the dashboard showed "0 Built / 0 Animated" despite the
project being fully built; corrected to `animated`. Round 5 removed the
`el-sfx-6`
glitch-shatter cue entirely (round 4's gain cut wasn't enough — it was
confirmed as the single loudest moment in the whole video) and seeded the
"1% LINE" concept earlier in Frame 6's reading-scan sweep, after the
creator's screenshot at the concept's mid-sweep point looked like the tag
was missing (it wasn't — the actual reveal is 8s later, on the correct
row; the real gap was that nothing signalled the concept before then).
Round 4 addressed a real audio level complaint (21-24s "harsh blast,"
first attempt was a gain cut, not a full removal) and replaced Frame 3's
hand-drawn SVG beaker/leaf illustration with real catalog photography
(see below). Earlier rounds fixed the video's own craft gaps (all-
crossfade transitions producing muddy near-blank midpoints, ~60s of the
runtime with no authored visual change, several elements landing past
the Shorts safe-bottom line) alongside a companion fix to the
`faceless-video-craft` skill itself, which had drifted from the real
HyperFrames API; round 3 fixed a genuine audio-clipping bug and a GSAP
bleed-through bug (a reused element rendering at its "from" state
seconds before its first scheduled appearance — `tl.set()` inside the
timeline fixed it; a bare `gsap.set()` outside it did not). Full change
log: `STORYBOARD.md`'s "Build history"
section in the project folder.

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
Round-3 feedback asked for the catalog's imagery to be felt through more of
the runtime, not just Frame 1's opening flash — extended to Frame 6's
teardown card (a circular accent near the "GLOW SERUM" header, same
`hook-bottle-photo.png`, reinforcing "this is a real physical product"
during the one scene that's literally about reading a bottle's own label)
and to the CTA endcard's three Hanbang recap chips (reusing the same
already-approved ingredient-photography stills from Frame 7 — zero new
assets). Frame 1's own photo also now recedes to a persistent 0.3-opacity
backdrop by 3s instead of disappearing entirely.

## Frame 3's equation — SVG illustration replaced with real photography

Round 4: the creator flagged Frame 3's hand-drawn beaker/leaf SVG directly
("notice this svg rather use a available pic") after already pushing on
catalog underuse earlier in the same round. The illustrated beaker, its
waterline/ripple animation, and the leaf-drop SVG were removed entirely
and replaced with two bordered photo cards under the labels WATER / TINY
BIT OF PLANT: [`loop-water-droplet.png`](../../product-photography/assets/B01-01.png)
(droplet macro from `product-photography/`, cropped to the droplet) and
[`loop-centella-leaf.png`](../../ingredient-photography/02-centella-asiatica.png)
(the actual named ingredient — this frame's own K-BEAUTY chip already
reads "CENTELLA EXTRACT — 70%", so the leaf photo is a literal, on-topic
pairing rather than decoration). Both copied project-local to
`assets/images/`, matching this project's existing convention. First
render regressed the scene's blank-frame reading (467ms -> 7533ms): both
source photos are shot on this catalog's own near-white house background,
which read as low-contrast against the composition's paper canvas. Fixed
with a solid ink border and a size bump on the photo cards, not by
swapping the source images — confirmed via re-render back to 533ms.

## Thumbnails — extracted from the render, not a separate composition

`assets/thumbnail/` follows the same extract-grade-finalize convention
`seoulhabit-launch` established: pull a real frame from the rendered video
(never a fresh composition built just for the thumbnail), apply a light
grading pass, and save as `<name>-source.png` / `<name>-final.png`.
`thumbnail-final.png` is the currently-selected primary, pulled from the
hook's own resolved payoff (t=2.7s — struck "80% GINSENG?", the
"0.5% GINSENG." reveal, and the round-7 ginseng photo). Unlike
`seoulhabit-launch`'s source frame (a plain product shot needing an added
headline), no title text was layered on top — this frame's own in-video
typography already carries the full hook claim, and stacking another
headline on it would compete rather than help.

First grading attempt copied `seoulhabit-launch`'s exact filter chain
(contrast/saturation boost + vignette) without adjusting for this video's
light paper background — the vignette read as a muddy gray cast instead of
a natural darken, since it was tuned for a dark-ink-background video.
Redone with a lighter touch (contrast 1.06, saturation 1.05, mild unsharp,
no vignette) suited to this project's own palette.

Three additional candidates (`candidate-curiosity-gap`,
`candidate-high-value-promise`, `candidate-visual-equation`) were pulled
from creator-supplied timestamps/descriptions and graded the same way —
not yet chosen as the final. Note: `candidate-visual-equation` (t=26s) was
pulled before round 8's Frame 3 change below and should be re-extracted if
it's still a live candidate — the frame at that timestamp now includes
the "70% CENTELLA EXTRACT" recap headline.

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
