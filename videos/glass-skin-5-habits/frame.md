# Frame — glass-skin-5-habits

## Canvas

1080×1920, 30fps, 9:16 (Shorts). Safe area: `--safe-top 120 / --safe-bottom
360 / --safe-left 60 / --safe-right 162` (source tokens.css).

## Channel audit (why this project copies from these two, not the others)

Ten video projects exist on this channel; `faceless-video-craft`'s
"Consistency across a channel's videos" section requires auditing real
inheritance rather than assuming a shared catalog folder implies it. Audit
result, checked file-by-file:

- **Tokens** exist in 2 of 10 projects (`seoulhabit-launch`,
  `kbeauty-one-percent-line`) — this project copies `tokens.css` from
  `seoulhabit-launch` verbatim.
- **The VO bus** (`<hf-audio-group>`) ships in the same 2 of 10 —
  `retinol-patch-test` explicitly declined it, citing a project
  (`red-ginseng-two-routes`) that no longer exists in the repo. This project
  takes the bus.
- **Captions** ship in only `snail-mucin-truth` and
  `snail-mucin-medical-secret`, and only there — a real mechanism
  (`.caption-group`/`.caption-word`, `.is-active`/`.is-spoken`, `gsap.set`
  state, never `tl.call()`), but tokened to an unrelated "Editorial Forest"
  preset (green/cream/Bricolage Grotesque), not this channel's paper/ink/
  aqua. This project reuses the mechanism, re-tokens it to `tokens.css`.
- `caption.txt`, present in 6 of 10 projects, is YouTube description copy,
  not a caption/subtitle file — confirmed by reading it, not assumed from
  the name. This project's own `caption.txt` will be the description only;
  actual captions are `compositions/captions.html` + a real `.srt`.

## Palette

Base five only, from `tokens.css`: `--paper #F7F5F0`, `--ink #131516`,
`--aqua #59B8AE`, `--leaf #6F8F72`, `--coral #C97A5C`, plus `--highlighter
#E0A32B` for the numeral/data-mark moments. **One aqua-family highlight per
frame** (hard law, inherited). **Coral is the single voltage moment for the
whole video** — the ink strikethrough across the ghost "10-STEP" kicker at
the Frame 1 sweep-payoff; every other alert-adjacent beat uses ink-weight
strikethrough or highlighter, never a second coral hit.

Frames alternate paper/ink for hyperframe contrast, same as
`kbeauty-one-percent-line`:

| Frame | Ground |
|---|---|
| 1 hook | paper |
| 2 promise | ink |
| 3 cleanse/hydrate | paper |
| 4 treat/seal | ink |
| 5 protect | paper |
| 6 cta/endcard | paper |

Frame 5→6 is the one same-ground boundary in the sequence; still a hard cut
(house rule — see Motion), not used as license for a crossfade.

## Type

`--font-display` EB Garamond (the "5" numeral, hero moments), `--font-body`
Inter 700/800 (the five habit words — CLEANSE / HYDRATE / TREAT / SEAL /
PROTECT — bold and center-left per the user's own brief), `--font-mono`
JetBrains Mono (SPF/percentage callouts), `--font-kr` Noto Sans KR 500 (습
SeoulHabit lockup, Frame 6 only). Nothing under `--t-floor: 20px`.

## Faceless

Presenter is the macro plate, not typography — a deliberate departure from
this channel's typographic-first house style (`kbeauty-one-percent-line`,
the `skincare-glossary-part-*` series), directly following the user's own
production rule: "without facial expressions to hold retention, your
visuals must be highly tactile." Type still does real work as co-performer:
the persistent habit-word stack, and wall-to-wall captions per the user's
"keep text on screen at all times" rule — but photography carries the frame.

No talking-head footage, no visible faces at any point — every reused and
generated plate is hands-below-wrist or texture-only, matching
`catalog/product-photography/`'s own no-face constraint.

## B-roll / photography (controlled exception, filed per catalog convention)

`catalog/product-photography/README.md` requires "its own filed decision
record" before compositing its stills into a HyperFrames render. This is
that record, and — unlike `kbeauty-one-percent-line`'s Frame 04b, which used
three stills for one 2.5s interlude — photography is this video's **primary
presenter across all six frames**, not a single wordless exception. Full
reuse-vs-generate table, corrections to my own first-pass reading of the
catalog, and provenance: `assets/MANIFEST.md`.

Reused plates are copied project-local into `assets/images/` and
downsampled to ~1400px, not referenced cross-project — matching how fonts
and audio are always project-local in this channel's shipped projects.

## Motion

System eases only: `--e-out` entrances, `--e-in` exits, `--e-inout` holds.
`--d-snap 180ms` impact beats (the strikethrough, the finger-tap CTA
micro-interaction), `--d-fast 400ms` / `--d-base 500ms` word reveals,
`--stagger-line 80ms` for the habit-word stack's own list. No bounce/
elastic/back eases, no infinite keyframes — the habit stack's idle motion
(a subtle hold-glow-free pulse on the active word) is a bounded yoyo
(repeat: 2-3) resolving inside its own beat.

**Hard cuts only, no crossfades.** Palette alternates ground scene to scene;
per `faceless-video-craft`'s cuts-vs-crossfades rule, crossfading across a
changing background produces a muddy near-blank transition midpoint. Every
one of this video's six boundaries changes or could be mistaken to change
ground — hard cut at all six.

Within-scene macro plates use seek-safe Ken Burns (scale/translate as a pure
function of scene-local `t`, no CSS `animation`) to give static photography
its "pour"/"melt"/"squeeze" motion read, per the skill's Ken-Burns pattern.

## Elevation

`--elev-2` on the habit-word stack's active card only. **Glow banned**
outright — no `box-shadow: 0 0 …`, matching every other project on this
channel.

## Brand anchor

습 SeoulHabit text lockup (Noto Sans KR 500) appears once, Frame 6, bottom-
safe — not the Fold & Spark mark.

## Audio mix

`<hf-audio-group id="voiceover">` bus carrying the channel's real chain
verbatim (highpass 90Hz → peaking 150Hz +0.8dB → compressor -24dB/4:1 →
peaking 3kHz +2.5dB → peaking 6.5kHz -4dB Q3.5 de-ess → limiter -9dB), copied
from `kbeauty-one-percent-line/index.html`'s `data-fx-chain` — a channel-
level decision per the audit above, not re-derived. 80ms automation fade-in/
out on every VO and SFX clip, versioned `{"version":1,"lanes":[...]}` shape
(the flat-array shape is silently accepted by `check` but rejected at
render — confirmed on `hyperframes@0.8.17`). BGM (`el-bgm`) carries
`data-fx-carve {sources:["voiceover"], strength:0.25}`. ASMR SFX layer (water
splash, jar unscrew, cream swoosh, pump click, droplet tick) — one per lane,
`data-track-index` 20+, `data-volume ≈0.25-0.35`, trimmed to each beat's real
length (not left at native file length) per the skill's SFX-spotting rule.

**Volume-automation trap, confirmed on this CLI version:** a `"volume"`
automation lane *replaces* `data-volume` rather than scaling it. Every clip's
plateau value must be its real intended level (e.g. `v:0.12` for BGM meant to
sit at 0.12), not a normalized `v:1` — verified by re-reading
`faceless-video-craft`'s own documented incident before wiring any fade.

## Content corrections

**Line 1**, user script: "Stop doing a 10-step skincare routine. You're just
destroying your skin barrier." — step count isn't what damages a skin
barrier; over-exfoliation and stacking incompatible actives are the actual
mechanism, and this is an evidence-based channel. User was asked and chose
to soften rather than ship verbatim or add an on-screen qualifier:

> "Stop doing a 10-step skincare routine. Stacking that many actives is how
> barriers get wrecked."

Same word count, same hook energy, defensible. Lines 2-6 ship verbatim.
Video carries the channel's standard "general guidance, not medical advice"
disclaimer (this is routine literacy, not a locked `ING-*` source record for
a single active — same status as `kbeauty-one-percent-line`).

## Design-system reconciliation

Same reconciliation basis as `seoulhabit-launch/frame.md` and
`kbeauty-one-percent-line/frame.md`: `assets/tokens/tokens.css` copied
verbatim from `seoulhabit-launch` (itself reconciled 2026-08-28 against the
live claude.ai design project via DesignSync). No new tokens invented here.

## Verification (real defects found and fixed, not assumed clean)

Full loop per `faceless-video-craft`: `npm run check` (lint/runtime/layout/motion/
contrast), a full render, then frame extraction and direct pixel inspection —
not just a clean manifest. Three real bugs surfaced this way, none of which a
passing `check` or a compressed thumbnail preview would have caught:

1. **Habit-badge glyph never updated on a mid-file state transition.** A row
   that transitions active→done via `tl.set(el,{attr:{"data-state":"done"}})`
   correctly re-styled (white badge, full-opacity text) but kept its baked-in
   digit instead of showing a checkmark — the checkmark glyph was only ever
   written into the static HTML for rows *authored* as done from t=0, never
   updated for a row that became done mid-timeline. Found via `hyperframes
   snapshot --at 25.0` and pixel-sampling the badge region, not from the
   `check` output (which reported 0 errors). Fixed by putting both glyphs in
   the DOM always and letting the same `data-state` attribute the JS already
   sets choose which one paints via CSS — no JS text update needed, so this
   class of bug can't recur.
2. **Frame 2's own frame-zero was a blank dark box.** The numeral's solid
   backing capsule was visible immediately but the "5" itself faded in over
   0.2s — ffmpeg-extracting the exact hard-cut frame at t=6.785 (not a
   compressed contact-sheet thumbnail, which hid it) showed an empty dark
   square. This is the same "frame zero is a design object" rule violated at
   a *mid-video* hard cut, not just the video's cold open — every scene's own
   local t=0 needs the same discipline. Fixed by composing the numeral
   immediately and keeping only the bounded pulse as its motion.
3. **A 3.5s flat stretch in Frame 4's TREAT beat** — caught by a static-hold
   check (sample ~0.5s, diff consecutive frames, flag >2-3s with no
   measurable change) that neither of this project's two inherited QA
   scripts covers. Fixed with a mid-beat content chip ("JUST ONE ACTIVE")
   timed to the VO's own clause, not decorative filler added just to move
   pixels.

**Layout checker's overlap findings — investigated, not blindly suppressed.**
`npm run check`'s layout pass initially failed on `content_overlap` between
every frame's `.habit-word`/`.habit-badge` spans and the *same* spans in
adjacent sub-composition files — because the persistent stack sits at the
identical absolute position by design (it must, to read as one continuous
UI element across hard cuts) and the checker's geometric pass doesn't fully
model cross-file temporal occlusion. Verified with direct snapshots at the
exact reported window (t=20.0, t=25.0) showing clean, non-overlapping
rendering before marking the leaf text spans `data-layout-allow-overlap` —
confirmed via the CLI's own bundled source
(`layout-audit.browser.js:hasAllowOverlapFlag`) that the flag must sit on
the exact leaf element, not an ancestor `.habit-row`/`.habit-stack`, which
is where the first two (ineffective) attempts placed it.

**Audio.** `ffmpeg astats` on a VO-free window (40.6-41.4s, BGM-only) read
-40.6dB RMS against a VO-present window's -34.6dB RMS — BGM sits
meaningfully under narration as authored (`data-volume="0.12"`), confirming
the automation-replaces-volume trap this file's own § Audio mix section
warns about did not bite here (the plateau value was written as the real
level, not `v:1`).

**Loudness mastering.** Two-pass `ffmpeg loudnorm` (I=-14 LUFS, TP=-1.5dBTP)
on the render: measured input -23.91 LUFS / -5.87dBTP → output -14.50 LUFS /
-1.50dBTP, video stream copied through unchanged.
`renders/glass-skin-5-habits_FINAL_mastered.mp4` is the publish-ready file
(re-mastered 2026-08-30 from the QC fix pass's render — see below; supersedes
the original `..._16-35-50_mastered.mp4`).

**Captions.** Word-level transcript generated per-clip from the *actual
generated VO* via `hyperframes transcribe` (not estimated) — text matched
the scripted lines exactly (15/15/13/17/11/14 words, until line 06 was
re-recorded 2026-08-30 — see below). 28 caption groups built from real
timestamps, offset into the root composition's global timeline;
`renders/glass-skin-5-habits.srt` exported from the same corrected source
via `scripts/gen/build_srt.py` (new, added in the QC fix pass — previously
hand-exported, now the same source-of-truth pipeline as the burned-in
captions). Burned-in captions reuse the channel's one real caption mechanism
(`snail-mucin-truth`), re-tokened — see § Channel audit.

**Static-hold, frame-zero (all six scenes' own t=0, not just the video's
cold open), and loop check.** ~~All re-verified clean on the final
render.~~ **Correction, 2026-08-30:** this claim was wrong for one scene, and
wrong in a way the tooling available at the time could not have caught.
Frame 6 (the CTA/endcard) held ~5.0s of genuinely frozen imagery (local
~2.06-7.5s, PSNR ~70dB between 0.5s samples excluding the caption band) — a
real static-hold violation, not the intentional loop-hold tail this section
originally attributed it to. `check-blank-frames.py` measures per-frame luma
*stddev* (blankness); a frozen-but-populated frame is invisible to it by
construction — it cannot distinguish "nothing changed" from "nothing is
there." Found by a QC pass that sampled the actual render at a fixed interval
and diffed consecutive frames, per `faceless-video-craft`'s own verification
loop — which this project's own tooling should have been doing already and
wasn't. Fixed with five new content beats plus continuous Ken Burns filling
the frame's full local duration (previously stopped at 1.2s); re-verified
zero static-hold findings on the fixed render via the new
`scripts/check-static-hold.py` (below). The remaining ~0.9s hold at Frame 6's
very end, after all beats resolve, *is* the intentional loop-hold tail and is
well under the cadence ceiling.

### 2026-08-30 QC fix pass

A 6-item external QC review (1 blocker, 4 major, 1 minor) came in against the
originally shipped render. All six were verified against the actual render
and source before fixing, per this skill's "verify by pixels, never by
manifest" rule — none were taken on the report's word alone.

1. **Captions in the Shorts UI overlay zone (BLOCKER).** Caption band was at
   `top:1360px`, inside the platform's bottom ~20% reserved zone (channel
   handle, description, audio-track pill). Moved to `top:960px` (960-1110px,
   the frame's middle third) — `scripts/gen/build_captions_html.py`. This
   forced a reflow of every scene whose own content collided with the new
   band: Frame 2's numeral badge (660→400px), Frames 4/5's info chips
   (900→780px, after their own box fix below), and Frame 6's entire vertical
   stack (split above/below the band instead of running through it).
2. **VO tail cutoff.** The original take's very last sample was mid-word —
   confirmed via `ffmpeg silencedetect`, no trailing silence existed at all,
   so a fade would have had nothing to fade into. Re-recorded via the
   project's own TTS pipeline (Higgsfield `seed_audio`, same voice) with real
   trailing room; the new take's "barrier." completes naturally (5.72-6.04s
   local) with genuine decay after it. Extended 0.5s past that natural end
   into an engineered 10-frame (0.333s @30fps) fade-out — `data-duration`
   6.500→6.630, automation lane rewritten with an exponential-shaped
   multi-point ramp rather than the original flat 80ms line — `index.html`.
   Re-transcribed (`hyperframes transcribe`); `assets/voice/06.words.json`,
   caption groups 23-27, and the `.srt` all re-derived from this take.
3. **Frame 6 static-hold** — see the correction above. Fixed in
   `scripts/gen/build_frames.py`'s Frame 6 section: continuous Ken Burns
   across the scene's full duration, plus five beats each landing on a real
   VO clause (habit-stack pop on "Five habits," brand-mark entrance on
   "because," bounded product-band drift on "tomorrow," a "NEXT: BARRIER
   REPAIR" next-video chip on "damaged" — the burned-in form of the VO's own
   closing line, not an invented claim).
4. **Frame 4's "JUST ONE ACTIVE" chip, root cause.** Not a colour problem —
   `.treat-chip` inherited `.clip`'s `inset:0` and only overrode `top`/`left`,
   so with no explicit `width` the inherited `right:0` stretched it to a
   ~1020px slab with text pinned to its top-left corner. That slab is what
   read as "low contrast": text against its own capsule was fine, text
   against the *hero plate* behind an invisible oversized box was not. Fixed
   the box (`bottom/right:auto; width:max-content`) and applied the report's
   asks on top: white text, 600 weight, 40px (up from 22px).
5. **Frame 5's "TWO FINGERS · SPF 50" chip.** Same root cause as #4
   (`.spf-chip`, identical missing-width bug). Same fix; 40px to match Frame
   4's chip as one component (not the report's literal 150%, which lands at
   33px and still misses the mobile reading floor).
6. **Frame 1 hook plate, six-fingered hand.** Confirmed on inspection —
   `assets/images/hook-clutter.png`, on screen 0.0-4.6s. Regenerated via the
   project's own image pipeline (`nano_banana_pro`, 9:16, matching
   `hook-swept.png`'s ground and lighting per `assets/MANIFEST.md`); four
   candidates generated, each inspected at full resolution before picking one
   — no stock footage substitution (this composition is images-only, and the
   plate is a deliberate before/after pair with `hook-swept.png`).

**Detection gap closed.** `scripts/check-static-hold.py` (new) samples the
render at 2fps, crops out the caption band (otherwise its own word changes
mask every frozen scene beneath it — precisely why the Frame 6 freeze passed
review once already), and flags any run of consecutive-frame PSNR above a
frozen threshold longer than the shorts cadence ceiling. Wired into
`package.json`'s `postrender` alongside the existing blank-frame scan.
Re-verified on the fixed render: zero findings.
