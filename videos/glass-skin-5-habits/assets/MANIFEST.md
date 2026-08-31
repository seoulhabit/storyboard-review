# Asset manifest — glass-skin-5-habits

Checked `catalog/product-photography/` and `catalog/visual-components/`
before generating anything new, per `faceless-video-craft`'s production-loop
steps 3-4. Every plate below was opened and inspected at full resolution —
not accepted from the catalog table's description alone; two entries in an
earlier pass of this table were wrong until the pixels were checked (see
Corrections below).

## Images — reused (verified, project-local copy)

| Beat | Source | Verified content | Local path |
|---|---|---|---|
| Frame 2 promise | `catalog/product-photography/assets/C02-01.png` | Hand dispensing serum, cropped at the wrist — already faceless-compliant | `assets/images/promise-hand-dispense.png` |
| Frame 3 cleanse | `catalog/product-photography/assets/B03-01.png` | Balm block melting into a celadon-tinted puddle on white | `assets/images/cleanse-balm-melt.png` |
| Frame 4 treat | `catalog/product-photography/assets/B01-01.png` | One suspended clear droplet above a celadon glass dish | `assets/images/treat-droplet.png` |
| Frame 4 seal | `catalog/product-photography/assets/B02-01.png` | Thick opaque whipped-cream swirl in a dish (attempt 3 — the gloss-free version per that asset's own README) | `assets/images/seal-cream-swirl.png` |
| Frame 6 cta | `catalog/product-photography/assets/C01-01.png` | Six-product shelf lineup, 16:9 — cropped to 5 of 6 products for this video | `assets/images/cta-five-products.png` |

All five: 2048px-class Higgsfield stills, unbranded, no faces, no on-surface
claims (per `catalog/product-photography/README.md`'s hard constraints —
verified glyph-level in that project, not re-verified here since nothing is
composited onto them). Downsampled to ~1400px and copied project-local into
`assets/images/`, matching `kbeauty-one-percent-line`'s Frame 04b precedent
— not referenced cross-project from `catalog/`, the same way fonts and audio
are always project-local in this channel's projects.

## Images — generated (the real gaps)

| Beat | Need | Local path | Verified |
|---|---|---|---|
| Frame 1a hook | Top-down counter, 10+ bottles cluttering frame, two hands entering to sweep | `assets/images/hook-clutter.png` | **Regenerated 2026-08-30** (QC #6) — the original generation had a six-fingered left hand, confirmed on direct inspection. Four `nano_banana_pro` candidates generated with hand anatomy called out explicitly in both prompt and negative prompt; all four inspected full-resolution before picking one. Chosen candidate: densest bottle pile, both hands fully spread and anatomically correct (5+5 digits, confirmed by counting), same white ground/matte lighting as its `hook-swept.png` twin, cropped at the wrist, no face. |
| Frame 1b hook payoff | Same counter, same white ground, swept clear | `assets/images/hook-swept.png` | Same white ground and lighting as 1a (a deliberate before/after pair, generated together for consistency) |
| Frame 3 hydrate | Watery toner pouring into a cupped palm | `assets/images/hydrate-pour.png` | Hand cropped at wrist, no face, natural (non-glossy) specular highlight on the liquid only |
| Frame 5 protect | Two fingers, two thick SPF lines squeezed down their length | `assets/images/protect-fingers.png` | No face, no logos/text; a third finger is faintly visible at the frame's bottom-right edge (minor, doesn't compete with the two-finger subject) |

Model: `nano_banana_2` (Higgsfield), 9:16, generated via this session's
`generate_image_batch` — except Frame 1a's regeneration (`nano_banana_pro`,
2026-08-30, see above). Each verified against
`catalog/product-photography/README.md`'s hard constraints (unbranded, no
faces, no on-surface claims, no gloss/glow) before use, per the process
above — not accepted on the prompt text alone.

## Corrections to my own first pass

- **Frame 1 hook clutter** was initially assigned to
  `catalog/product-photography/assets/C03-01.png` on the strength of the
  catalog README's table description ("overhead flat-lay, 4 products
  labeled"). Opening the file showed a sparse, clean 4-product flat-lay —
  the opposite of "counter covered in 10+ bottles." Reassigned to a new
  generated plate instead of forcing the mismatch.
- **Frame 3 cleanse** was assumed to need a literal hands-under-running-water
  shot per the user's script direction. `B03-01.png` (balm melting into a
  puddle) reads as a stronger "melt" visual than a generated water shot
  would, and is already catalog-verified — reused instead of generating a
  new plate that would have duplicated the intent.

## Fonts

`assets/fonts/NotoSansKR-500-subset.woff2` — copied verbatim from
`videos/seoulhabit-launch/assets/fonts/`, not re-fetched (matches that
project's own "self-hosted, copied per project that needs it" convention).

## Voice / SFX / BGM

Pending generation — see `audio_request.json` once written (step 5 of the
build order in the plan).

## Component reuse

- **RoutineLadder** (`catalog/visual-components/routine-ladder/`) — its
  focus-advance mechanism (one item in focus, driven by a single `t`) is
  adapted for the persistent habit-word stack. Its literal ladder skin
  (six-rung depth stack, bilingual labels) is dropped — the macro plates
  carry the frame here, not the stack. Its content is six rungs (Cleanse →
  Toner → Essence·Serum → Ampoule → Moisturiser → SPF); this video's content
  is a five-step subset (Cleanse / Hydrate / Treat / Seal / Protect) matching
  the user's own script — noted as a real content difference, not silently
  merged into the six-rung set.
- **Caption mechanism** — `videos/snail-mucin-truth/.hyperframes/caption-skin.html`'s
  `.caption-group`/`.caption-word` + `.is-active`/`.is-spoken` state machine
  is reused verbatim; its "Editorial Forest" preset tokens are replaced with
  this project's `tokens.css` values (see `frame.md` § Channel audit).

## Voice — generated, measured

Higgsfield `seed_audio`, voice "Kimberly" (`674b71b8-1d2e-4087-8567-d1f53c0b9f3c`,
`voice_type: element`), per `audio_request.json`. Measured with `ffprobe`
(not assumed from the request text):

| Line | File | Duration |
|---|---|---|
| 01 (hook, corrected) | `assets/voice/01.wav` | 6.485s |
| 02 (promise) | `assets/voice/02.wav` | 5.391s |
| 03 (cleanse/hydrate) | `assets/voice/03.wav` | 7.000s |
| 04 (treat/seal) | `assets/voice/04.wav` | 8.600s |
| 05 (protect) | `assets/voice/05.wav` | 5.050s |
| 06 (cta) | `assets/voice/06.wav` | 7.800s (re-recorded 2026-08-30, see below) |

Sum 39.03s (original) — all scene timing in `index.html` is derived from
these measured numbers, not the pre-generation word-count estimates in
`STORYBOARD.md`.

**Line 06 re-recorded 2026-08-30 (QC #2).** The original take's last sample
was mid-word — confirmed via `ffmpeg silencedetect`, zero trailing silence in
the file, so the shipped render's fade had nothing to fade into (a hard
digital cutoff, not a natural decay clipped short). Re-generated via the same
Higgsfield `seed_audio` / Kimberly voice with explicit trailing room in the
prompt. New take: 7.800s file, real speech ends ~6.13s (natural decay
confirmed via `silencedetect`), re-transcribed via `hyperframes transcribe`
(`assets/voice/06.words.json` replaced, not hand-edited). `index.html`'s
`#el-06-voice` uses `data-duration="6.630"` (natural end + 0.5s engineered
tail) with a rewritten multi-point automation lane approximating a 10-frame
exponential fade-out, replacing the original flat 80ms linear ramp.

## SFX / BGM — real tool gap, resolved by channel reuse, not fabrication

This session's available generation tools cover text-to-speech and images
only. The two models capable of generic music/SFX synthesis
(`sonilo_music`, `mirelo_text_to_audio`) are explicitly scoped "game
pipeline only" by the platform itself — not available for this build. No
stock-audio retrieval command exists in the pinned `hyperframes@0.8.17` CLI
either (checked `--help`; no `media`/`sfx` subcommand).

Rather than fabricate SFX from an unauthorized model, or invent silence
where the user's brief explicitly asked for an ASMR layer, every cue is a
**verified, project-local copy of an existing channel SFX file**, matching
`faceless-video-craft`'s own instruction to reuse/hash-compare before adding
"new" library SFX. Renamed to this project's cue vocabulary so the mapping
is self-documenting in `index.html`, not hidden behind an unrelated
filename:

| Cue (this project) | File | Reused from | Native duration | Honest fit |
|---|---|---|---|---|
| hook hit | `hook-hit.mp3` | `retinol-patch-test` | 2.75s | Exact — same cue role |
| buzzer | `buzzer.mp3` | `retinol-patch-test` | 1.73s | Exact — same cue role |
| glass clink | `glass-clink.mp3` | `retinol-patch-test/pop.mp3` | 0.31s | Substitute — no glass/clink asset exists on the channel; closest short percussive hit |
| soft whoosh | `soft-whoosh.mp3` | `retinol-patch-test` | 1.83s | Exact — same cue role |
| chime | `chime.mp3` | `retinol-patch-test` | 0.72s | Exact — same cue role |
| jar unscrew | `jar-unscrew.mp3` | `retinol-patch-test/soft-click.mp3` | 0.26s | Substitute — closest short click texture to a lid twist |
| water pour | `water-pour.mp3` | `retinol-patch-test/soft-whoosh.mp3` | 1.83s | Substitute — no true splash/pour asset exists; reused a second instance of the channel's one continuous-motion texture |
| droplet tick | `droplet-tick.mp3` | `retinol-patch-test/pop.mp3` | 0.31s | Substitute — same reasoning as glass clink; reused a second instance |
| cream swoosh | `cream-swoosh.mp3` | `kbeauty-one-percent-line/whoosh-thud.mp3` | 0.57s | Substitute — fuller swoosh+thud reads better for a cream smoothing motion than the thinner soft-whoosh |
| pump click | `pump-click.mp3` | `retinol-patch-test/soft-click.mp3` | 0.26s | Substitute — reused a second instance, same click category |
| soft squeeze | `soft-squeeze.mp3` | `kbeauty-one-percent-line/marker-squeak.mp3` | 0.37s | Substitute — closest existing friction/squeak texture to a tube squeeze |
| chime triple | `chime-triple.mp3` | `kbeauty-one-percent-line` | 2.50s | Exact — same cue role |

**Real gap, disclosed rather than papered over:** no genuine water-splash,
jar-unscrew, or cream-application texture exists anywhere on this channel
yet. Three cues above (water pour, jar unscrew, cream swoosh) are the
closest available stand-ins, not accurate matches. If dedicated ASMR SFX
become available in a future session (a stock-audio tool, or manual sourcing
by the user), swap these three specifically — everything else already reads
correctly as its literal cue.

## BGM

`assets/bgm/track.mp3` — reused verbatim from `retinol-patch-test/assets/bgm/track.mp3`
(57.0s, native length). Same reasoning as the SFX gap above: this session
has no music-generation or stock-retrieval tool available, and this project's
own `audio_request.json` BGM query is near-identical in mood to
`retinol-patch-test`'s ("calm, warm, aesthetic educational skincare
background bed, gentle and reassuring, low presence under narration") — the
same retrieval query would very plausibly surface the same or a
sibling track. Reused rather than guessed at.
