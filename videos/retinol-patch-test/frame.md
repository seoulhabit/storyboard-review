# frame.md — retinol-patch-test

## Provenance validation (2026-08-28)

Everything below the first build cited `videos/kbeauty-one-percent-line` and
`videos/seoulhabit-launch` as "the" SeoulHabit design system. `git ls-files`
shows both are **fully untracked** (0 files in git) — uncommitted working-tree
content from another session, not checked-in ground truth. So was
`catalog/ingredient-photography/16-retinol.png`, the product photo Frame 2
used. The project was rebuilt against what's actually tracked:

- **Tokens/fonts** — `videos/skincare-glossary-part-4-texture-anti-aging/index.html`
  (and the identical block in `skincare-ingredient-glossary`, `-part-2`,
  `-part-3`), a real committed SeoulHabit video with the tokens inlined per
  file, doc-commented as read verbatim via DesignSync from the same source
  Claude Design project — same hex values, different (and now-adopted)
  variable names (`--short-safe-*`, `--ink-2-dark`/`--ink-3-dark`). Its
  `assets/NotoSansKR-500-subset.woff2` replaces the copy that came from the
  untracked project (checksums differ).
- **Audio wiring** — `videos/red-ginseng-two-routes/index.html` (tracked,
  rendered, `renders/video.mp4` committed): plain `<audio data-volume>`
  elements. No `hf-audio-group`/fx-chain/carve precedent exists in any
  checked-in project — that machinery is dropped.
- **Frame 2's icon** — the exact generic leaf-stroke SVG path and card copy
  (`"A gold-standard anti-aging compound that promotes cell turnover."`,
  category `"Vitamin A"`) from that same glossary project's own tracked
  **Retinol** card (`skincare-glossary-part-4-texture-anti-aging/index.html`
  line ~317) — reused instead of the untracked photo.
- **Frame 6's lockup** — the "습 SeoulHabit" wordmark + slide-up-and-breathe
  move is genuinely checked in: `videos/red-ginseng-two-routes/compositions/frames/06-endcard.html`.
- **Coral** `#C97A5C` — grounded in `videos/red-ginseng-two-routes/capture/extracted/tokens.json`
  (that project's own tracked pre-remix capture) plus the "limitation /
  refusal" role documented in `catalog/README.md` and the tracked
  `catalog/visual-components/evidence-meter` component.
- **Frames 3 & 4** — already correct: `split-face-protocol` and
  `celestial-arc` are genuinely tracked catalog components (`git log` shows
  real commits). No change needed beyond the token-name alignment below.

## Canvas

1080×1920, 30fps. Safe areas: top 120px, bottom 360px, left 60px, right 162px
(`--short-safe-top/-bottom/-left/-right`, matching the checked-in glossary
projects' names). Nothing load-bearing sits outside them.

## Palette

Tokens inlined per file (no shared `tokens.css` — no checked-in project uses
one), copied from `videos/skincare-glossary-part-4-texture-anti-aging/index.html`.
Paper `#f7f5f0` / ink `#131516` alternate as scene grounds. Aqua `#59b8ae` is
the recurring highlight — **exactly one aqua moment per frame**. Highlighter
`#e0a32b` carries the hook's "STOP" beat. Coral `#c97a5c` (see Provenance
above) is spent **once in the whole video** — Frame 5's "wash it off" symptom
branch, coral's system role of "a limitation or a refusal." No success color;
glow is banned.

## Type

`--font-display` EB Garamond for display headlines, `--font-body` Inter for
narration-adjacent body copy, `--font-mono` JetBrains Mono for labels/chips,
`--font-kr` Noto Sans KR for the 습 SeoulHabit lockup — loaded via the Google
Fonts `<link>` each checked-in frame file uses, not a separately self-hosted
tokens file. Nothing ships smaller than the 20px floor.

## Motion

No bounce/elastic/back easing, no infinite keyframes — every animation
resolves to a held final state. Scene-to-scene: 0.5s opacity crossfade,
`power2.inOut` (matches every checked-in project's `index.html`).

## Elevation

Shadow only (`--elev-1/-2/-3`), never glow, per token file.

## Content corrections (evidence rigor)

The user's Step 1 line — "This mimics the skin on your face perfectly" — is an
unsourced overclaim; no `ING-*` record exists to support "perfectly." Softened
to "...the spots that behave most like the skin on your face" (see `SCRIPT.md`
Line 3, `BRIEF.md` § Notes). No citation chips are used anywhere in this video —
patch-testing guidance is procedural, not an efficacy claim. The outro instead
carries the sanctioned disclaimer microcopy: "General patch-testing guide — not
sourced claims, not medical advice," mono, `--ink-3`, ≥ `--t-floor`.

## Brand anchor

습 SeoulHabit Noto Sans KR text lockup (Frame 6) — genuinely checked in, see
Provenance above. The Fold & Spark logo mark is explicitly banned from
SeoulHabit videos (documented in the untracked `seoulhabit-launch/frame.md`;
no checked-in project uses that mark either, consistent with the ban).

## Audio mix

Plain `<audio data-volume>` elements, matching the tracked
`videos/red-ginseng-two-routes/index.html` — no voiceover bus, fx-chain, or
carve ducking automation (that machinery only ever existed in the untracked
kbeauty/seoulhabit-launch projects). BGM at `data-volume="0.12"`, retrieved
bed ("calm, warm, aesthetic educational skincare background, gentle and
reassuring, low presence under narration"), 57s — ends a few seconds before
the video's ~60.7s total, which is fine; no loop needed. SFX at
`data-volume≈0.35`, resolved via HeyGen retrieval (`audio_meta.json`):
hook-hit + buzzer (Frame 1), soft-whoosh + soft-click (Frame 2), soft-click
×2 (Frame 3, both test-site markers), pop + soft-click ×3 (Frame 4, pea dot +
rule chips), tick (as a ticking-clock texture under the 0h→24h→48h ladder) +
alert-ping truncated to ~1.3s (Frame 5's coral beat), chime (Frame 6 lockup).

## Design-system reconciliation

Any off-token color introduced while porting the split-face-protocol SVG
geometry (Frame 3) or the celestial-arc night motif (Frame 4) is normalized
to the palette above before shipping.

Frame 3 was rebuilt post-ship, twice. First pass hand-drew an anatomical side
profile (nose/lips), which read as amateurish. Second pass replaced it with a
hand-drawn front-view head+shoulders bust — cleaner, but still invented
geometry, not an existing component. Final pass reuses the catalog's own
`split-face-protocol` component verbatim: its `#control-arm`/`#active-arm`
cranial bezier paths, mirrored into one closed outline, with the two test
sites marked as rounded-rect zone chips matching that component's
`.sfp-zone-wire` convention (recolored to this project's aqua). That second
rebuild also surfaced a real layout bug worth carrying forward as a rule for
this project: a `.zone` class that sets `top` without also setting
`bottom: auto` inherits `bottom: 0` from the shared `.clip { inset: 0 }` base,
so its box silently stretches to the canvas bottom — invisible for plain-text
children, but it turns bordered/backgrounded children (chips, cards) into
stretched shapes under default flex `align-items: stretch`. Any new zone
built on `.clip` should set the unused side to `auto` explicitly.

Frame 4's night motif had the same problem: the first pass hand-drew a simple
moon + 3 dots instead of reusing `catalog/visual-components/celestial-arc`.
Rebuilt to port the source's actual arc path, sun, and moon geometry
(deterministic and glow-free, since the source runs on CSS `infinite`
keyframes and a blurred box-shadow — neither allowed here). The first
crescent-moon attempt (a hand-tuned two-arc SVG path) silently rendered
nothing — caught with `hyperframes snapshot`, not the Studio preview, which
was unreliable for scrubbing in this session. Fixed with an SVG mask (a
circle cut by an offset circle), a more reliable technique and, incidentally,
a closer port of the source's own inset-box-shadow "subtract an offset
shape" trick than the arc-path attempt was.

**Process note:** when a hand-authored SVG element might not be rendering as
expected, `npx hyperframes snapshot . --at <seconds> --no-end -o <dir>` (then
read the resulting `contact-sheet.jpg`) is faster and more reliable than
scrubbing the interactive Studio preview.

## Shorts safe-zone audit (post-ship)

Prompted by feedback that on-screen text felt off for Shorts. Checked all 6
frames' peak-text moments by rendering snapshots, overlaying this project's
own declared safe lines (top 120 / bottom 1560 / left 60 / right 918 on the
1080x1920 canvas -- top status area, bottom title/caption/audio strip,
right-side like/comment/share column) at exact pixel positions via a
numpy bounding-box script, and cropping in on anything close.

**Process note:** a quick eyeballed pass over a full-height thumbnail is not
reliable in either direction -- it produced two false positives (Frame 3's
marker, Frame 4's rule chip both looked like they crossed the right line at
a glance; tight pixel crops showed they don't) and missed one real violation
entirely (Frame 6's disclaimer, hardcoded to `bottom: 240px` against this
file's own `--short-safe-bottom: 360px`). Render, overlay the actual token
values as guide lines, and measure pixels -- don't trust a glance at any
resolution.

Three real, confirmed violations, all the same family of bug (a symmetric
~960px-wide centered zone that only honors the left safe margin, or a
`top`-without-`bottom:auto` zone stretching past where it reads as
centered):

- **Frame 1**: the hook's strikethrough + "OVER YOUR FACE?" text crossed
  both the left and right safe lines. `.hook-text-zone` was 960px wide
  (left safe-left, right symmetric) instead of respecting both margins;
  changed width to `calc(100% - var(--short-safe-left) - var(--short-safe-right))`.
- **Frame 5**: the coral STOP block (this video's one safety boundary)
  crossed both the right and bottom lines. `.split-zone` set `top` without
  `bottom: auto`, inheriting `bottom: 0` from `.clip { inset: 0 }` and
  stretching past where `align-items: center` reads as centered -- the
  exact bug already documented and fixed on Frame 3's `.legend-zone`, never
  carried over here. Fixed the same way: added `bottom: auto`, changed
  width to the same `calc()` pattern.
- **Frame 6**: the disclaimer sat entirely below the safe-bottom line
  (hardcoded `bottom: 240px` vs. this file's own 360px token) and also
  crossed the right line (`left: 80px; width: 920px` put its right edge 82px
  past `--short-safe-right`). This file never declared
  `--short-safe-left`/`--short-safe-right` at all, unlike every other frame
  in the project -- added both tokens and switched to `bottom: var(--short-safe-bottom)`
  plus the same `calc()` width pattern.
- **Frame 4** (round 2, caught by re-sweeping with pixel measurement instead
  of trusting the round-1 glance): the day-to-night arc's moon+stars sat at
  the edge of their own viewBox, and `.night-zone` centered the whole SVG in
  the full 1080px width rather than the safe box, pushing the moon ~12px
  past the right line. Low severity (decorative, not text) but real; fixed
  by moving `.night-zone` to the same safe-box `calc()` pattern.

Frames 2, 3 (aside from the moon note above) and the rest of Frame 6 were
confirmed clean and left untouched.

## Font-size validation (post-ship, two rounds)

**Round 1:** checked whether 20-26px labels were a defect or house style by
grepping the tracked `seoulhabit-launch` and `kbeauty-one-percent-line`
sibling videos -- both use 18-28px for label-tier text, so this project's
small text matches an established series convention, not a mistake. Confirmed
with a phone-viewing simulation (downscale the 1080px render to a real 390px
logical width, the way it actually appears on a phone, rather than judging it
at full size on a desktop monitor): most labels held up fine at that scale;
only Frame 6's 20px disclaimer -- this file's own stated absolute floor --
read as genuinely hard to make out. Bumped to 24px. Separately fixed a real
hierarchy bug independent of house style: Frame 5's `.split-kicker`
("NORMAL"/"STOP") was smaller (24px) than its own body text (26px), the only
kicker/body pairing in the project where that was true, on the one word
carrying the video's actual safety directive. Bumped to 28px.

**Round 2:** user still felt text read small after round 1 shipped. This
pass prioritizes that direct read over series-consistency precedent: bumped
every label/body tier across all 6 frames by roughly 4px, keeping the large
display headlines (64-84px) untouched. Frame 2's category/body/chip
(24/30/26 -> 28/34/30), Frame 3's kicker/legend/tagline/marker-labels
(24/26/24/24 -> 28/30/28/26) and legend-num (20 -> 22), Frame 4's night-pm/
rule-chip/dose-label (24/28/32 -> 28/32/34), Frame 5's rung-label/split-body
(36/26 -> 38/30) plus `.split-kicker` pushed further (28 -> 32, keeping it
ahead of split-body's new 30 so the round-1 hierarchy fix doesn't regress),
Frame 6's brand/pill/subline/disclaimer (32/30/24/24 -> 34/32/28/26).

## Why Frame 4's day/night motif isn't the catalog component verbatim

Asked directly: the catalog's own README
(`catalog/visual-components/celestial-arc/README.md`) says the component is
a **"SPIKE -- not wired to build.mjs"** and explicitly **"not seek-safe
yet"** -- its sun/rays/stars/arc-dot animations run on wall-clock CSS
`infinite` keyframes and SMIL `<animateMotion repeatCount="indefinite">`,
not a paused, seek-scrubbable GSAP clock, and it leans on blurred glow
(`box-shadow`/`drop-shadow`) this project's own design system bans ("shadow
only, never glow"). Using it as-is would produce non-deterministic renders
(a render must be able to jump to any timestamp and get a correct frame,
which `infinite` keyframes can't guarantee) and break the no-glow rule. So
Frame 4 **ports** the component instead of embedding it: same arc path
(`M 70 150 Q 500 -30 930 150`), same crescent-moon masking idea, same
sun/moon/star layout, reimplemented as static elements on the composition's
own paused timeline with the glow stripped out. See the SVG comment in
`compositions/frames/04-night-dose.html` for the exact port details.

## Re-voice, image swap, and full retime (post-ship, explicit user request)

Three changes landed together because the first forced the other two to
touch every file anyway:

1. **Voice swap.** User asked for the Higgsfield voice element `Kimberly`
   (`voice_id: 674b71b8-1d2e-4087-8567-d1f53c0b9f3c`, `voice_type: element`),
   confirmed by listing this workspace's `list_voices` catalog -- not a
   HeyGen voice, despite the name superficially fitting that catalog's
   naming style (searched all 1,635 HeyGen starfish voices first and found
   no match before the user clarified "Kimberly in Higgsfield"). This
   deliberately breaks the HeyGen-Marcia voice-continuity convention
   documented in BRIEF.md/SCRIPT.md for the rest of the SeoulHabit run --
   that's the point of an explicit request, not an oversight.
2. **Frame 2 hero image.** `catalog/ingredient-photography/16-retinol.png`
   (amber dropper bottle, golden-orange oil; Higgsfield
   `marketing_studio_image`, 2048x2048, tracked in git as of commit
   `b307235`) replaces the generic leaf-stroke icon. The original build (see
   Provenance section above) dropped this exact photo for not being checked
   into git; it's since been committed as part of a proper 20-item
   ingredient-photography set, and that set's own README explicitly scopes
   it as "B-roll / thumbnail stock for future video projects" independent of
   the (unrelated) glossary-card icon decision -- so using it here doesn't
   reverse anything. Rendered at 360x360, `object-fit: cover`, 28px rounded
   corners, soft shadow (`0 16px 40px rgba(0,0,0,0.45)`).
3. **Full retime.** A new voice means new takes with different durations and
   different word timing -- every scene boundary, crossfade point, SFX
   offset, and word-synced animation beat was keyed to the Marcia takes'
   exact timing, so swapping voices meant recomputing all of it.

### This generative voice has real run-to-run pacing variance

Generated the 6 lines twice over the course of this work (once, then again
after an unrelated incident required rebuilding the project from scratch --
see below) and the two generations differ substantially, not just by normal
TTS jitter: Frame 1's line alone went from 5.36s to 9.50s between takes, with
a dramatically longer pause inserted before "immediately? Stop!" the second
time. The whole-video total happened to land close to both the original
Marcia take (60.682s) and this take (60.668s), which is coincidence, not a
sign the voice is consistent -- Frame-by-frame the two Kimberly generations
distribute that time very differently. **Practical consequence: word-sync
timestamps and scene durations are only valid for the specific audio file
they were measured from.** If these voice files are ever regenerated, the
whole retime below needs to be redone from fresh transcription, not reused.

### Methodology (measured, not estimated or scaled)

Generated all 6 lines via `generate_audio` (model `seed_audio`, the voice
above), downloaded each result, transcoded to this project's established
mono/44.1kHz format (the Higgsfield takes came back stereo/24kHz), and
measured each with `ffprobe`. Then ran `hyperframes transcribe` (whisper
`small.en`) on each new file to get real word-level timestamps, **one file
at a time** -- the command writes a single shared `assets/voice/transcript.json`
sidecar regardless of which input file was given, so running all 6
back-to-back silently overwrites 5 of the 6 results (caught this after a
first pass actually did exactly that; redid it saving each result before the
next transcription started).

Word-synced beats were retimed to the real measured timestamps of the audio
actually shipped in `assets/voice/`, not scaled proportionally from any
other take -- spoken emphasis and pauses don't scale linearly with overall
clip duration:

- Frame 1: the hook's word-by-word reveal was previously driven by an
  estimated per-character formula (`WORD_BASE`/`WORD_PER_CHAR`), not real
  timestamps, even in the original Marcia build -- replaced with actual
  measured word starts. The strikethrough + "WAIT." payoff trigger on the
  real "Stop!" word (8.96s in the shipped take).
- Frame 3: the two test-site markers retimed to "behind"/"ear" (3.21-4.00s)
  and "along"/"jawline" (4.13-5.28s).
- Frame 4: the dose-dot/label retimed to "pea"/"sized" (1.71-2.43s); the
  three rule chips to "clean" (3.19s), "Rub" (4.64s), "No" (7.14s) --
  keeping the original's 0.3s chip-to-strike gap for "NOTHING ON TOP".
- Frame 5: the ladder's 0H->24H->48H draw compressed/expanded to fit
  whatever runway precedes the coral reveal, preserving the original's
  non-literal pacing (the "48H" rung is a suspense beat, not synced to when
  "48 hours" is actually said at ~2.8s). The coral STOP reveal -- this
  video's one safety-boundary moment -- triggers on the real word "wash"
  (9.27s in the shipped take) instead of a fixed late-scene offset.
- Frame 6: the "seoulhabit.com" pill's underline emphasis and the subline
  reveal land on the actual words "soulhabit.com" (6.20s) and "for our full
  guide on layering retinol" (7.46s) -- the original design never claimed
  word-sync here, so this is a genuine improvement.

Every frame's tail fadeout (where one exists) is computed as
`VO_duration - 0.36s` rather than ratio-scaled from scene duration -- that
0.36s gap is what the original build's own numbers implied across all four
frames that have a fadeout tween, so it's the more faithful constant to
carry forward regardless of how long any given take runs.

### Mid-work incident: concurrent-session file collision

While this rework was in progress, a separate concurrent Claude Code session
sharing this same git working tree performed a git operation (unrelated to
this project -- its own commit only touched `videos/seoulhabit-launch`) that
reverted this project's uncommitted working-tree changes back to the
pre-session committed state, including the first-generation Kimberly audio
files. Recovered by moving the work into an isolated git worktree
(`.claude/worktrees/retinol-patch-test-rework`) and rebuilding from scratch,
which is why the shipped Kimberly audio is the *second* generation, not the
first -- see the pacing-variance note above for why that mattered beyond
just re-running the same commands.

## Frame zero

Frame 1 opens on paper ground with the retinol-bottle silhouette mark faint in
the background (now filled in — amber-glass body, dark cap — after feedback
that the original outline-only mark was hard to spot; see the "Revision
(post-ship, user feedback)" note under Frame 1 in STORYBOARD.md). Frame 2
originally carried the same signature forward via the checked-in glossary's
leaf-icon treatment; it now uses a real product photo instead — see § Re-voice
above.

## Measured timing (from generated TTS, `assets/voice/0N.wav`)

Scene start = previous start + previous VO duration. Scene duration = own VO
duration + 0.5s crossfade tail (final scene: no tail). All values below are
measured (`ffprobe`) from the current Kimberly takes, not estimated —
supersedes the original Marcia-take table this project shipped with. See
§ Re-voice above for why these specific numbers are only valid for the exact
audio files currently in `assets/voice/`.

| # | Frame | VO start | VO duration | Scene duration |
|---|---|---|---|---|
| 1 | 01-hook | 0.000 | 9.500 | 10.000 |
| 2 | 02-power | 9.500 | 10.018 | 10.518 |
| 3 | 03-test-site | 19.518 | 8.376 | 8.876 |
| 4 | 04-night-dose | 27.894 | 9.431 | 9.931 |
| 5 | 05-wait-48 | 37.325 | 12.997 | 13.497 |
| 6 | 06-outro | 50.322 | 10.346 | 10.346 (no tail) |

**Total duration: 60.668s** (the original Marcia take measured 60.682s — the
near-identical total is coincidence; see § Re-voice's pacing-variance note,
since the two Kimberly generations distributed their time very differently
frame-by-frame despite similar totals). Still comfortably inside the
faceless-explainer route's 30–90s sweet spot (hard cap ~3min).

## Second Shorts-optimization pass (post-ship, feedback round 2)

Scene-level timing (start/duration per frame, VO sync) is untouched — every
change here is an in-scene animation, color, or added-element edit. Verified
with `npm run check` (0 errors/warnings, 12/12 contrast) and pixel-measured
snapshots (`hyperframes snapshot`) rather than a visual glance, per this
project's established audit method (see § Shorts safe-zone audit above).

- **Frame 1 — static open + weak STOP beat.** The bottle mark previously
  faded up 10px; it now drops in from off-frame with a physical bounce
  (`y:-200 -> 0`, `ease: bounce.out`, 0.7s) so the opening reads as motion,
  not a still image, on the scroll-past window. Separately, "Stop!" (the
  real word start, 8.96s) now triggers a fast camera-punch on `#root`
  (scale 1 -> 1.07 -> 1, ~0.4s total) layered on top of the existing
  strikethrough + dim + buzzer SFX — confirmed via pixel measurement that
  the bottle's on-screen bbox grows ~6% at the punch's peak (9.02s) and
  recenters on the full 1080x1920 frame, not on the text block, which is
  what makes it read as a camera move rather than a local UI wiggle.
- **Frame 5 — draggy ladder, flat caution copy.** The 0H/24H/48H draw
  window was compressed from a 6.75s crawl to 3.6s (rungs now land at
  1.25/2.75/4.6s instead of 1.25/4.04/7.75s); `split-normal` moved up from
  8.15s to 6.8s to close the dead air that opened up once the ladder
  resolves faster. `split-stop`'s reveal stays hard-pinned to 9.25s (the
  real word "wash," this video's one safety-boundary sync point) —
  unchanged. Separately, "Severe redness, stinging, or raised bumps" inside
  the STOP card is now wrapped in `.split-stop-em` (coral, bold) instead of
  reading in the same ink-grey as every other line of body copy; the coral
  card's border (2px->3px) and background tint (0.08->0.16 alpha) were also
  strengthened. This spends the frame's coral accent more assertively
  rather than introducing a second "warning orange" — the design system's
  one-highlight-color-per-frame budget (see § Design-system reconciliation)
  stays intact.
- **Frame 4 — flat reveals on the two callouts most likely to get missed on
  a small screen.** "PEA-SIZED." (`#dose-label`) and "CLEAN, DRY SKIN"
  (`#rule-1`) now pop in on a `back.out` overshoot (scale 0.82/0.85 -> 1)
  instead of a plain fade+rise, matching the spring already used on
  `#dose-dot`. Font sizes are unchanged here — they were already bumped and
  pixel-validated in the prior round (§ Font-size validation); the request
  offered "larger or pop-in" as alternatives, and animation was the lower-
  risk lever given the sizes already sit close to their safe-zone ceiling.
- **Frame 6 — no visual nudge toward the CTA.** Added a small downward
  chevron (`#outro-arrow-wrap`) between the subline and the disclaimer,
  entering at 8.6s and giving two bounded nudge-down cycles (`yoyo: true,
  repeat: 2` — not an infinite loop, per this project's determinism rule)
  that finish by 10.2s, inside this final (no-tail) scene's 10.346s runtime.
  Colored to match the disclaimer's muted grey rather than the frame's aqua
  accent, which is already spent once on the pill underline. Pixel-measured
  bbox at 59.4s: x 517-562, y 1302-1323 — centered in the safe box (x
  60-918, y 120-1560) with no overlap on neighboring text.
- **SFX at the STOP moment.** The feedback asked for "a sharp sound effect
  ... right at the STOP moment." One already exists — `buzzer.mp3` at 8.96s
  (`index.html`, tied to the real word "Stop!") — so no SFX change was made
  here; the camera-punch above is the actual new addition to that beat.
- **Real b-roll / tactile close-ups — not applied.** The feedback also asked
  for intercut footage of retinol texture or a real person's hands/jawline.
  This project has no real-footage asset in its inventory and is built
  entirely from the checked-in HTML/SVG catalog; sourcing or fabricating
  footage is outside what this pass can responsibly do without a real,
  licensed clip to work from. Flagging this explicitly rather than
  substituting an illustrated stand-in the feedback didn't ask for.

## Skill-compliance audit fixes (2026-08-29)

A `faceless-video-craft` skill review (not tied to the kbeauty-one-percent-line
skill-review goal — a separate request against this project) found and fixed
four issues, then closed the loop with a real render and pixel/audio
verification rather than trusting `npm run check` alone:

1. **Frame zero was blank.** Frame 1's bottle mark didn't start fading in
   until `t=0.1s` from `opacity:0`, so the literal first exported frame was
   empty paper. Fixed in `01-hook.html` — see the Frame 1 revision note above.
2. **Frame 2's `<img>` was missing the mandatory attributes.** No
   `loading`/`decoding`/`width`/`height`, no fallback background on the
   wrapper. Fixed — see the Frame 2 revision note above.
3. **All six `assets/voice/NN.words.json` transcripts were stale**, dated
   ~20 hours before the currently-shipped `.wav` files (all six wavs share
   one mtime from the worktree-recovery rebuild — see § Re-voice's
   "concurrent-session file collision" — but the transcripts were never
   regenerated after). Confirmed via `ffmpeg silencedetect` on Frame 1's
   audio before touching anything: the real "Stop!" burst sits at
   ~8.93-9.15s, matching the code's hardcoded 8.96s trigger, not the stale
   JSON's claimed 5.6s. Regenerated all six with `hyperframes transcribe
   <file> --json` (one at a time, per the shared-sidecar-clobber gotcha
   below § Methodology), confirming every word the code times against
   (`slather`@4.82, `Stop!`@8.96, `wash`@9.27, etc.) matches the fresh
   transcript exactly. The code was never wrong; only the saved reference
   file was. Logged as a general pipeline gotcha in project memory.
4. **No audio ever faded in/out.** All 23 `<audio>` elements in `index.html`
   (6 VO lines, 16 SFX one-shots, BGM) were flat `data-volume` with no
   `data-automation` envelope — hard cuts on every clip edge. Added a fade
   to each (VO: 0.08s in / 0.1s out; short SFX: ~0.01-0.02s in / 0.05-0.1s
   out, sized to not blunt a one-shot's transient; the `tick` texture and
   BGM: longer 0.05s/0.4s in, 0.1s/0.5s out).

   **The skill's own `data-automation` example is stale for this pinned
   `hyperframes@0.8.17`.** The canonical pattern doc shows
   `data-automation='{"volume":[[t,v],...]}'` — this pinned engine rejects
   that shape outright (`Unsupported automation version: undefined`, caught
   by `npm run render`'s correctness gate, *not* by `npm run check`, which
   passed both before and after). Read the actual validator in the installed
   CLI's bundled `dist/cli.js` (search for `Unsupported automation version`)
   to get the real shape: `{"version":1,"lanes":[{"target":"volume","points":
   [{"t":0,"v":0},{"t":0.08,"v":1},...]}]}` — `version` must be the literal
   number `1`, points are `{t,v}` objects, not `[t,v]` tuples, and lanes need
   an explicit `target` (`"volume"` for gain; `"fx.<nodeId>.<param>"` for an
   effect parameter).

   **Second, more dangerous bug: a `data-automation` volume lane REPLACES
   `data-volume` entirely — it does not multiply against it.** The first fix
   attempt held each clip's automation curve at `v:1` during its "full
   volume" plateau, on the assumption that `1` meant "100% of `data-volume`"
   the way it would in a normal fader-times-envelope model. It doesn't: read
   the engine's own gain-resolution code (`dist/cli.js`, the block computing
   `x` from `Tl(r, ...)` right after the automation lookup) — when an
   automation "volume" lane exists for an element, its interpolated value
   *is* the final gain, full stop; `data-volume` is only consulted as a
   fallback when no automation/keyframes exist at all. Net effect: every
   clip that got a `v:1` plateau — BGM (`data-volume="0.12"`) and all 16 SFX
   (`0.25`/`0.35`) — started playing at full source level instead of its
   authored mix level the instant the fade "finished." This shipped as a
   render that passed `npm run check` *and* `npm run render` with zero
   warnings; it was only caught because the user listened to the render and
   said the BGM sounded very loud. Verified by ear-report, not eyeballing:
   `ffmpeg astats` RMS in a VO-silent window (7.2-8.5s, confirmed silent via
   `silencedetect` earlier) measured -24.2dB on the original un-automated
   render vs. **-14.2dB** on the buggy one — a real +10dB the ear caught
   correctly. Fixed by setting each clip's automation plateau to its own
   actual `data-volume` number instead of the placeholder `1` (VO lines were
   accidentally correct throughout, since their `data-volume` already is
   `1`). Re-verified post-fix: the same window now measures -24.3dB, matching
   the pre-automation baseline within noise, while the 0.0-0.1s fade-in
   window still measures a genuinely quieter -43dB — the fade survived, the
   level regression didn't. **Lesson: never assume an automation/envelope
   system multiplies against a base gain — confirm from the engine's own
   gain-resolution code, and always A/B a corrected render's ear-reportable
   levels against the pre-change baseline, not just against "does it still
   ramp."** This exact gotcha is now also logged in the skill itself.

## Thumbnails (2026-08-29)

Built this video's first YouTube thumbnails in `assets/thumbnail/`, following
the extract-grade-finalize convention established on `kbeauty-one-percent-line`
and `seoulhabit-launch` (real frame from the render, light per-video grading
pass, no separate composition authored) — now also written into the
`faceless-video-craft` skill's own "The thumbnail" section.

Three candidates pulled from the corrected render
(`renders/retinol-patch-test_2026-08-29_23-00-57.mp4`) via
`hyperframes snapshot`, each checked against the same frame-zero discipline
as the video itself (fully settled, not mid-crossfade/mid-tween) before
grading:

- **`hook-stop.png`** (t=9.48s) — the hook's payoff: struck-through question
  + "WAIT." on highlighter. Paper ground; graded
  `eq=contrast=1.06:saturation=1.05,unsharp=5:5:0.5` (no vignette — this
  video's light background, same lesson as kbeauty's first grading attempt).
- **`powerful-stakes.png`** (t=16.0s) — Frame 2's real product photo + "=
  POWERFUL" chip. Ink ground, so graded separately rather than reusing the
  paper grade verbatim: `eq=contrast=1.08:saturation=1.08,unsharp=5:5:0.5`.
- **`safety-stop-card.png`** (t=48.0s) — "Wait 48 Hours" headline + ladder +
  the coral STOP card. Paper ground, same grade as `hook-stop`.

Explicitly did NOT pull a candidate from the outro ("You're ready." +
seoulhabit.com, t≈59s) despite it being a clean, settled frame — it's the
video's resolution/payoff, and a thumbnail that shows the ending removes the
reason to click. Kept to candidates that raise a question or a stake instead.

**Grid-size legibility check** (per the skill's new rule — downscaled each
to ~120×213px, roughly Shorts-feed-tile size, before judging):
`safety-stop-card` reads best small — short bold headline, a simple
line-and-dots icon, and a distinct coral color-block all survive
compression. `hook-stop` still reads as "something crossed out + a bold
call-to-action chip" even once the sentence itself blurs. `powerful-stakes`
is the weakest of the three at grid size — a light rectangle with two small
dark shapes on black reads as "a product exists" more than it raises a
question. Set **`safety-stop-card.png`** as `thumbnail-final.png`.

**vidIQ.** `vidiq_score_title` on the existing caption.txt title ("How to
Patch Test Retinol (Beginner's Guide) 🧴") scored 86/100 — kept it rather
than switching to any of `vidiq_generate_titles`' suggestions (85-88), which
scored comparably but leaned hashtag-heavy in a way that doesn't match this
channel's calmer, non-hashtag voice. `vidiq_score_thumbnail` could not be
used — it requires a live YouTube `videoId`/existing upload, and this
project hasn't published yet; noting this as a known pre-publish gap rather
than faking an ID. `vidiq_similar_thumbnails` also has a hard limitation
worth recording: **it only searches long-form video thumbnails, not
Shorts** — so its "competitive check" for this Shorts thumbnail concept
isn't a real read on the actual competitive shelf; the results it returned
(generic long-form skincare product-review thumbnails, unrelated hobby/DIY
videos) confirm it wasn't finding true comparables, not that the concept is
uncrowded. Re-run the thumbnail scoring tools once this video actually has a
`videoId`, rather than trusting this pre-publish pass as final.

All four verified with `npm run check` (clean throughout) plus a real
`npm run render` and fresh `hyperframes snapshot` frames at the changed
beats, followed by the loudness correction above — current render:
`renders/retinol-patch-test_2026-08-29_23-00-57.mp4`. Not in scope for this
pass: Frame 1's hook still doesn't show any on-screen text until ~3s and
doesn't land its "Stop!" payoff until ~9s of the 10s scene, while the VO is
already well into the line by then — a real tension with the skill's
"payoff visible by ~2s" hook guidance, but fixing it well means trimming or
restructuring the VO content itself, not a mechanical timing tweak, so it's
flagged rather than guessed at.
