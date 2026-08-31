# Asset manifest — centella-cica-vs-snail-mucin

Catalog checked first, per `faceless-video-craft`'s production-loop steps 3-4
— `catalog/product-photography/`, `catalog/ingredient-photography/`, and
`catalog/visual-components/`. Two catalog entries opened at full resolution
turned out not to match their own README description (see Corrections
below); nothing was accepted on the table description alone.

## Images — reused (verified, project-local copy)

| Beat | Source | Verified content | Local path |
|---|---|---|---|
| Frame 4 twist / Frame 5 cta | `catalog/ingredient-photography/02-centella-asiatica.png` | Three round centella leaves on one stem, top-down on cream paper — accurate to its README, but native green (HSL ~85°, 49% sat) is far more saturated than the system's `--leaf #6F8F72` (HSL ~126°, 12.6% sat) | `assets/images/twist-centella-leaf.png` — graded (`ffmpeg hue=h=42:s=0.28,eq=brightness=0.02:contrast=0.98`) to HSL (128.8°, 9.8% sat, 48.6% light), a close match to the token. Sampled with a Python/PIL patch average before and after grading to confirm, not eyeballed. |
| Frame 4 twist (cream swipe) | `catalog/product-photography/assets/B02-01.png` | Thick opaque whipped-cream swirl, gloss-free (that asset's own attempt-3 fix for the banned glossy look) | `assets/images/twist-cream-swirl.png` |
| Frame 5 cta (left panel, material reference) | `catalog/ingredient-photography/12-snail-mucin.png` | **README said** "glass dish of glossy stretching gel." **Actually is** a top-down pour of a clear stream into a glass dish — no stretch, no fingers. Confirms this still cannot serve as the string-test start frame; used instead as a material/lighting reference and the Frame 5 left-panel still. | `assets/images/cta-snail-pour.png` |

All three downsampled to 1400px and copied project-local, not referenced
cross-project — matching `glass-skin-5-habits`'s own convention.

## Images — generated (the real gaps)

| Beat | Need | Model | Verified against hard constraints |
|---|---|---|---|
| Frame 1 hook | Glass palette, top-down, watery green-gold drop beside a thick clear stretchy blob | `nano_banana_pro`, 2k, 9:16 | Unbranded, no hands/face, no text/labels/claims, no bloom/glow. Pass. |
| Frame 2 string-test start frame | Two bare fingertips pressing into a clear translucent gel | `nano_banana_pro`, 2k, 9:16, `image_references` = Frame 1's own palette still (for consistent gel translucency) | First attempt rendered opaque/lotion-white — rejected, regenerated referencing Frame 1's blob for translucency. Second attempt: hands below wrist, no face, no jewelry, no claims. Pass. |
| Frame 3 dropper start frame | Glass dropper above the back of a hand, one bead of pale green-gold liquid | `nano_banana_pro`, 2k, 9:16 | Hand cropped at wrist, no face, no claims, no glow. Pass on first attempt. |

## Video — generated (the media exception, see `frame.md` § Media exception)

| Beat | Model | Params | Verified |
|---|---|---|---|
| Frame 2 string test | `kling3_0` | `mode: pro`, `duration: 6`, `aspect_ratio: 9:16`, `sound: on`, seeded from the Frame 2 start-frame still (`start_image`) | Extracted frames at 0.5s intervals: two fingers press in, lift, and produce visible glossy strands stretching and thinning between fingertip and pool — the mandatory string-test beat. No face, no jewelry, hands below wrist throughout. `assets/broll/02-string-test.mp4`, 1076×1928, 6.04s native. |
| Frame 3 dropper | `kling3_0` | same params, seeded from the Frame 3 start-frame still | Extracted frames: dropper squeezes, bead falls, lands and spreads on the back of the hand. No face, no jewelry. `assets/broll/03-dropper.mp4`, 1076×1928, 6.04s native. |

Both `<video>` elements are muted and framework-owned (`data-start`/
`data-duration`/`data-media-start`), the same idiom as
`seoulhabit-launch/assets/broll/*.mp4` — the engine seeks `currentTime`
directly rather than playing them, so they stay deterministic under a cold
seek the same as everything else in this pipeline (confirmed via
`npx hyperframes docs data-attributes`, which documents `data-media-start`
as a real trim/offset attribute, not a play-from-here signal).

## SFX

Both generated videos carry a real (non-silent) `generate_audio: true` audio
track — confirmed via `ffmpeg astats` (peak ≈ -3dB, RMS ≈ -34dB, real
transient structure, not silence). Demuxed and kept as candidates at
`assets/sfx/candidates/{string-test,dropper}-generated-foley.aac`.

**Not wired into the shipped mix.** This session has no way to listen to
audio content — only to measure it numerically. "Sticky tack-tack" and "wet
dispense" are specific *qualitative* textures, and shipping an unheard track
under a specific descriptive claim would be exactly the kind of unverified
claim this channel's other rules exist to prevent. The honest choice is the
channel's own verified cue library instead, same reasoning
`glass-skin-5-habits` used for its own SFX gap:

| Cue (this project) | File | Reused from | Native duration | Fit |
|---|---|---|---|---|
| curious chime | `chime.mp3` | `glass-skin-5-habits` | 0.72s | Exact — same cue role |
| glass clink | `glass-clink.mp3` | `glass-skin-5-habits` | 0.31s | Exact — same cue role |
| sticky tack-tack | `droplet-tick.mp3` (×2) | `glass-skin-5-habits` | 0.31s each | Substitute — no true tacky/sticky-stretch asset exists on the channel; closest short percussive hit, used twice for a "tack-tack" rhythm |
| wet dispense | `water-pour.mp3` | `glass-skin-5-habits` (itself reused from `retinol-patch-test/soft-whoosh.mp3`) | 1.83s (trimmed to ~0.6s via `data-duration`) | Substitute — no true drop/splash asset exists on the channel |
| cream swoosh | `cream-swoosh.mp3` | `glass-skin-5-habits` | 0.57s | Exact — same cue role |
| reveal chime | `chime.mp3` | `glass-skin-5-habits` | 0.72s | Exact — same cue role, reused a second instance |
| chime triple | `chime-triple.mp3` | `glass-skin-5-habits` | 2.50s | Exact — same cue role |

**Real gap, disclosed rather than papered over:** no genuine sticky-stretch
or wet-dispense SFX exists anywhere on this channel, and this session cannot
qualitatively verify whether the two generated foley candidates would have
filled it. If a future session can listen to
`assets/sfx/candidates/*-generated-foley.aac` and confirms either is usable,
swap it in for `droplet-tick.mp3`×2 or `water-pour.mp3` respectively —
until then, shipping the unheard track would be a claim this manifest can't
back up.

## BGM

`assets/bgm/track.mp3` — reused verbatim from
`retinol-patch-test/assets/bgm/track.mp3` (57.0s native, confirmed via
`ffprobe`). Same channel-reuse reasoning as `glass-skin-5-habits`: no
music-generation tool available this session, same calm/warm/educational
mood brief.

## Voice — generated, measured

Higgsfield `text2speech_v2`/elevenlabs, voice "Kimberly"
(`674b71b8-1d2e-4087-8567-d1f53c0b9f3c`, `voice_type: element`) — the
channel's established voice. Measured with `ffprobe` after generation, not
assumed from script word count:

| Line | File | Duration |
|---|---|---|
| 01 (hook) | `assets/voice/01.wav` | 4.960s |
| 02 (snail texture) | `assets/voice/02.wav` | 4.640s |
| 03 (centella texture, corrected) | `assets/voice/03.wav` | 4.480s |
| 04 (twist, corrected) | `assets/voice/04.wav` | 5.360s |
| 05 (cta) | `assets/voice/05.wav` | 7.040s |

Sum 26.48s. All scene timing in `index.html` is derived from these measured
numbers (+0.3s inter-scene hold, +1.0s loop-hold tail on Frame 5), not the
`STORYBOARD.md` pre-generation estimate — total runtime 28.680s.

## Fonts

`assets/fonts/{eb-garamond-400,inter-800,jetbrains-mono-500,NotoSansKR-500-subset}.woff2`
— copied verbatim from `glass-skin-5-habits/assets/fonts/` (itself sourced
from `seoulhabit-launch`), not re-fetched.

## Component reuse

See `frame.md` § Component reuse for the full reasoning. Summary: the
`.cta-chip-hb`/`.cta-chip-eq` equivalence chip is reused directly from
`kbeauty-one-percent-line`; SplitFaceProtocol's bisector mechanism is
adapted (skin dropped) for Frame 5; RoutineLadder's focus-advance idea (not
the component) drives the verdict rail; the caption mechanism is reused
verbatim from `snail-mucin-truth`, re-tokened.
