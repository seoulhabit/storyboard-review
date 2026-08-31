---
workflow: faceless-explainer
flow: automation
storyboard: yes
message: "Ceramides make up roughly 50% of the skin's barrier, and the reserve drops sharply by age 30 — verify barrier health before adding more actives."
destination: shorts
aspect: 1080x1920
language: en
audience: "skincare-curious viewers who'd respond to a data/diagnostic framing over a marketing one"
length: 34.4s
angle: clinical UI dashboard — diagnostic read, not a pitch
VO_MODE: adapted
style_preset: clinical-ui-dashboard
---

## Intent

Sibling project to `../ceramides-skin-barrier` (the photoreal cinematic cut)
— **not a replacement of it**. Same underlying topic (ceramides / skin
barrier), a third distinct visual execution: this pipeline has now built the
same message as (1) flat paper/ink kinetic typography, (2) photoreal
cinematic image plates with Ken Burns, and (3) this — a minimalist,
UI-driven "research dashboard" treatment. All three exist independently;
each was an explicit, deliberate user direction, not an iteration that
superseded the last.

The script was drafted first as a standalone deliverable (published as an
artifact, "Barrier Diagnostic Cut") per an explicit two-column
visual-cues/voiceover request, reviewed, then built out here on request. The
artifact is the source of record for the creative brief; this file records
what changed or was decided during the build itself.

## Why a separate project directory

HyperFrames' own `lint` rejects two standalone root `data-composition-id`
files in one project (`multiple_root_compositions` — "the runtime may
discover both as entry points, causing duplicate audio playback"). The first
build attempt put this cut's root file directly in `ceramides-skin-barrier/`
alongside its existing `index.html`; lint caught the conflict immediately.
Correct structure is one project per root composition, matching how every
other video in this pipeline is organized (sibling directories under
`videos/`) — so this became its own project, scaffolded the same way
(`package.json` pinning `hyperframes@0.8.17`, `hyperframes.json`,
`meta.json`), rather than two roots sharing one project.

## Voice, SFX, BGM

- **Voice:** Higgsfield `seed_audio`, "Kimberly" element voice
  (`674b71b8-1d2e-4087-8567-d1f53c0b9f3c`) — same provider/voice as
  `ceramides-skin-barrier`'s photoreal cut (established there after HeyGen
  TTS credit ran out), reused here for consistency between the two
  sibling builds. Real measured duration ~50.1s of speech across 5 lines,
  close to the script's own ~52s nominal estimate.
- **Line 1 fix:** whisper's transcript dropped the opening "Retinol"
  (merged into "using"'s span — same class of ASR error as
  `ceramides-skin-barrier`'s "Stop"). Corrected in the caption text; the
  underlying audio was not affected.
- **Line 1 audio glitch:** a sharp synthesis-artifact click landed in the
  trailing silence after "check." (~6.5-6.6s into the raw take, confirmed via
  `ffmpeg showwavespic` — not audible content, a real glitch). Trimmed at
  the source (5.24s → wait, this file: originally longer, trimmed to 6.58s
  with a fade-out) rather than masked downstream. **Second, independent
  occurrence of this exact failure mode** on a "line 1" — worth knowing if a
  future line 1 in this pipeline sounds wrong: check the waveform before
  assuming the script or the render is at fault.
- **Line 4 excess trailing silence:** the raw take was 18.2s but real speech
  content ends at 14.8s — 3.4s of dead air (plus something at its extreme
  tail worth not trusting). Trimmed to 15.1s. Cutting the silence also
  removes whatever was sitting in it, same fix as the line 1 glitch.
- **SFX:** 4 cues, HeyGen retrieval, UI-appropriate (not the prior cuts'
  cinematic/whoosh register) — toggle click (Scene 1 flip), soft data blip
  (Scene 2 chart reveal), subtle mechanical click (Scene 3 grout
  completing), soft confirmation chime (Scene 5 resolve).
- **BGM:** HeyGen catalog retrieval, query "minimal ambient electronic pulse
  clinical technology sparse focus" — cooler/sparser mood than the photoreal
  cut's "lo-fi chill beauty focus" query, matching this cut's clinical
  register. 23s source, crossfade-looped to the full composition length.

## A real bug worth recording for future compositions in this pipeline

Every one of the 5 new scene files initially declared
`#root .clip { position: absolute; inset: 0; }` — copied by habit from the
photoreal cut's full-bleed image-plate pattern. The actual established
pattern (confirmed against the working reference file,
`ceramides-skin-barrier/compositions/frames/01-hook.html`) is
**`#root .clip { position: absolute; }` only — no `inset: 0`.** `inset: 0`
in that shared rule has higher specificity (`#root .clip`, an ID + a class)
than a scene's own single-class positioning rule (e.g. `.c1-label-wrap {
top: 700px; ... }`), so it silently won the cascade and collapsed every
labeled wrapper to the same top-left position regardless of its intended
`top` value. `hyperframes check`'s Layout pass caught it directly
(`content_overlap`, multiple elements reported at the same coordinates) —
this is exactly the kind of bug that would NOT be visible from reading the
code casually (both rules look reasonable in isolation) and is why the
Layout check step matters, not just Lint. Fixed by dropping `inset: 0` from
the shared rule and giving only the elements that are genuinely meant to be
full-bleed (`#c2a-wrap`, `#c2b-wrap`, `#c3-wrap`, `#c4-wrap`) their own
ID-scoped `inset: 0`.

## Captions: ground-aware color, not scrim, not a single fixed stroke

Per the `ceramides-skin-barrier` project's precedent, captions here are
lower-third, grouped into 3-5 word phrases, no opaque background bar. But
that project's captions sit over **photographic** stills — even a
notionally "light" moment has photo texture behind the text, so a strong
black stroke on white fill measures enough contrast. This project's Scene 2
and Scene 4 grounds are **flat, solid** off-white/white (`#F3F1EA`/`#FFFFFF`)
— a white fill there measures ~1:1 contrast regardless of stroke strength,
confirmed by `hyperframes check`. Fix: captions know which of the 5 scenes'
grounds are light vs. dark (hardcoded from the actual per-scene `#root`
background colors, not inferred) and swap to dark-fill/light-stroke during
the two light windows. **This needed a second pass** — the first version
only flagged Scene 2's second beat (the bar chart) as light, missed that
Scene 2's *first* beat (the schematic) shares the same off-white `#root`
background. The default `hyperframes check` 9-sample pass didn't happen to
land inside that window and reported clean; caught by rereading the
composition's own background declaration, not by the tool. Re-verified by
rerunning `check --at` against all 27 caption groups' exact start times
explicitly, not just the default sample count — 29/29 contrast checks pass
at every real caption moment, not just the ones the default sampling
happened to hit.

## Revision 2 — "retention rewrite," benchmarked against PDRN

User-directed rewrite, explicitly modeled on a reference video:
`~/Desktop/ingredent videos/PDRN/pdrncellularscience_20260829_165514.mp4`
(63.2s, 159 words, ~2.55 words/sec). Analyzed directly before writing anything
— extracted a frame contact sheet and a full whisper transcript rather than
guessing at "high-retention format" — and the benchmark turned out to already
use this same project's "Ingredient Identity" card component (plus a richer
vocabulary this project hasn't adopted: on-screen "○ UNSOURCED" badges,
"ING-xxx-Sxxx" citation chips, a confidence indicator). Noted below as a
follow-up opportunity, not implemented here — out of scope for what was
actually requested this round.

**Structural changes:**

1. **Hook rewritten, toggle-switch device dropped from Scene 1.** New line:
   "Your $80 Retinol won't work until you fix this one hidden variable."
   (synthesized from the two example directions given — the dollar-amount
   specificity of one, the curiosity-gap of the other). Visual is now bold
   kinetic type (kicker → slam → rule → italic tagline) — no UI toggle. This
   breaks the Scene 1/Scene 5 toggle bookend from Revision 1; Scene 5 was
   redesigned independently rather than patched to still reference a device
   Scene 1 no longer opens with.
2. **Scene 3 (mechanism) reordered and made kinetic.** New VO ("Here's what's
   happening: ceramides are the mortar...") names the mortar before the
   bricks, so the grout now reveals first, bricks build second — reversed
   from Revision 1, which built bricks first. Added the requested crumble:
   after the wall is established, all 12 bricks tumble to fixed (not
   `Math.random()`) per-brick rotation/offset targets, grout fades to 18%
   opacity, and three small chevrons rise from the rubble echoing Scene 2's
   "moisture escaping" motif. `hyperframes check --at-transitions` flags a
   `rotation_pivot_drift` warning on 3 of the 12 bricks (combined rotate +
   translate moves the bounding-box center, which is the whole point of a
   tumble) — reviewed against an actual snapshot at the collapse frame, reads
   as intentional debris, not a bug. Left as a known, reviewed warning.
3. **Scene 4's static "Ingredient Identity" card removed entirely**, replaced
   with 4 fast flash-cut text beats ("Identical to your skin." / "Wheat ·
   Rice · Lab-Made." / "Barrier: Restored." / "All skin types."), each ~1.5-2s
   in-hold-out. A first pass had adjacent flashes briefly co-visible during
   their cross-fade (`content_overlap`, caught by `check --at-transitions`,
   same failure class as the Revision 1 caption-timing bug) — fixed by
   guaranteeing each exit completes before the next entrance starts, not by
   tuning durations closer together.
4. **CTA rewritten to the user's exact copy**: "Are you buffering your
   retinol, or are you raw-dogging it and burning your skin barrier? Drop
   your routine below." On-screen Scene 5 uses a condensed, word-by-word
   ACCUMULATING build ("Buffering?" → "+ or" → "+ raw-dogging it?") copying
   the benchmark's exact technique for its closing question — implemented as
   plain opacity-reveal spans, not GSAP's `text:` property (TextPlugin is a
   paid Club GreenSock plugin, not assumed available here, and using it
   silently no-ops without a console warning most agents would catch). Closes
   on "Drop your routine below. ↓", matching the benchmark's explicit
   "comment below" ask structure.
5. **Pacing.** Requested 10-15% VO speed increase. Higgsfield `seed_audio`'s
   `speech_rate` param is an integer (not the float multiplier first tried;
   422 until corrected) clamped to `[-50, 100]`, and its effect on actual
   output duration is **noisy, not linear** — `speech_rate: 13` measured
   ~5.4% faster on a direct same-text comparison, `speech_rate: 19` measured
   ~3.8% faster (less, despite the higher setting — generation-to-generation
   variance in natural pause placement, not a monotonic curve), `speech_rate:
   30` measured ~28% faster (audibly rushed). Committed to the already-
   generated, glitch-checked `speech_rate: 13` batch rather than keep
   burning generation cycles chasing exact percentage precision against a
   noisy parameter — real result is a **more modest ~5-7% raw TTS speedup**,
   short of the requested range on that number alone. The tighter/punchier
   rewritten copy (shorter clauses, benchmark-style) contributes additional
   *perceived* pace on top of that. Flagged plainly rather than silently
   under-delivered: if the literal 10-15% matters more than the qualitative
   "brisker" result, it needs another generation pass at a higher
   `speech_rate`, accepting the risk of sounding rushed.
6. **Both new hook (line 1) and new solution (line 4) lines checked for the
   trailing synthesis-artifact click** that hit 2 of 5 lines in Revision 1 —
   this time checked proactively on all 5 new lines via waveform, not
   reactively after a user report. Line 1 had it again (3rd occurrence of
   this exact failure mode across this project's two revisions — worth
   assuming any new Kimberly/seed_audio line needs this check, not just
   "line 1" specifically, which is just this project's pattern so far by
   coincidence of which lines happened to be regenerated each time); trimmed
   at the source. One borderline case on the new line 5 (CTA) turned out to
   be the legitimate tail of "below." on inspection, not trimmed.

**Total runtime dropped from ~50.5s to ~40.7s** — shorter script (rewritten
copy is tighter) plus the real, if modest, pacing increase. Well inside a
Short's runtime envelope either way.

## Revision 3 — QC pass + "direct ingredient hook" rewrite

Two inputs, handled together as one rebuild rather than as patches: a
timestamped QC table from a real-render review of Revision 2, and a full
script rewrite that names Ceramides in the hook itself instead of "one
hidden variable." Because the rewrite touches all 5 lines and reshuffles
scene boundaries, every QC fix was baked into the fresh build rather than
patched onto the old one — cheaper and less error-prone than patch-then-
diverge.

### QC items and how each was actually resolved

1. **CTA in the bottom 15% dead zone (MAJOR).** The Revision 2 fix for this
   exact class of bug had already been applied once — `.c5-cta-wrap` was
   `position:absolute; inset:0; display:flex; ...; justify-content:center;`
   spanning the full 1920px canvas, which centers at y≈960. The user's
   real-render report says the CTA still measured inside the bottom-15%
   safe-area boundary (below y≈1632) anyway. Rather than trust centering-math
   again, Scene 5's CTA wrap is now **top-anchored** at a fixed `top:660px`
   instead of canvas-centered — its ~190px content block (two lines of 58px
   text + arrow) now spans roughly 660-850px, nowhere near either the top
   10% or bottom 15% safe-area boundaries, with no dependency on flexbox
   centering math landing where expected.
2. **"won't won't work" audio stutter at 0:01-0:02 (MAJOR).** Structurally
   moot: the new hook line doesn't contain that phrase at all ("Your $80
   retinol is useless without one specific ingredient: Ceramides."). No
   stutter-specific edit was needed, but the underlying discipline —
   checking word-level transcripts for duplicated tokens, not just trailing
   waveform glitches — was applied to all 5 new lines regardless (see below).
3. **"Wheat • RiceLab-Made." typo (MINOR).** The old two-line `<br>` split
   (`Wheat · Rice<br><span class=accent>Lab-Made.</span>`) is gone along with
   the scene it lived in. Scene 4's new f1 flash uses a single line with
   consistent separators throughout: `Wheat &middot; Rice &middot; Lab-Made.`
4. **"$80 RETINOL" eyebrow too small/low-contrast (MINOR).** `.c1-kicker`
   was `font-size:36px; color:#8B8E86`. Now `font-size:54px` (1.5x) and
   `color:#FFFFFF` (pure white, was a mid-gray measuring weakly against the
   `#17191A` ground on mobile).

### Script rewrite — structural reshuffle, not just new copy

The new script's beat boundaries don't line up 1:1 with Revision 2's five
scenes — it splits and recombines content differently:

- **Scene 1 (hook)** now stages a reveal instead of a slam: kicker ("$80
  RETINOL") → setup line ("is useless without one specific ingredient:") →
  a punch-in payoff word ("CERAMIDES.", 128px, accent green). The old
  two-word bold slam ("WON'T / WORK.") is gone entirely — the ingredient
  name itself is now the visual payoff, matching the point of this rewrite.
- **Scene 2 ("mortar/50%")** is new: grout-then-bricks (reusing Revision 2's
  Scene 3 brick/grout mechanic verbatim, since it was already proven) build
  an *intact* wall — no crumble here — paired with a "50% / OF YOUR OUTER
  BARRIER" stat card. This used to be folded into a single "problem" scene
  with the bar chart; now it's split out on its own beat.
- **Scene 3 ("40%/crumble")** is the one genuinely new composite beat: Beat
  A is an Age-20-vs-Age-30 bar chart (reusing Revision 1's bar-chart
  mechanic, recolored for a dark ground since this scene stays dark
  throughout rather than flipping to off-white), Beat B is the *same* wall
  design crumbling (Revision 2's crumble mechanic, unchanged fixed
  per-brick `collapse` targets). The two beats cross-dissolve into each
  other rather than being separate scenes — "age bar chart transitioning to
  crumbling bricks" as specified. Keeping this scene dark end-to-end (rather
  than off-white-to-dark) was a deliberate simplification: it avoids
  re-introducing the ground-aware caption-contrast bug from Revision 1
  inside a single scene's own internal transition.
- **Scene 4 (sourcing)** keeps the flash-cut mechanic but the 3rd flash is
  new: a small 8-brick mini-wall (4×2 grid) assembles from scattered
  scale-0 bricks into a solid block ("Instantly patched.") — a direct visual
  callback to Scene 3's crumble, satisfying the brief's "restored barrier
  graphic" note with the same visual language as the wall it's repairing,
  not a generic checkmark.
- **Scene 5 (CTA)** question chunks now read "Buffering" → "with
  ceramides," → "or raw-dogging it?" (added "with ceramides" per the new
  script; Revision 2's chunks didn't name the ingredient either).

### Audio pipeline — one real bug found, two glitches caught

- **`transcribe` writes next to its input, not to a fixed path.** Assumed
  (from this project's own Revision 1/2 history) that `npx hyperframes
  transcribe <file>` always writes `assets/voice/transcript.json` regardless
  of input path. False: it writes `transcript.json` in the **same directory
  as the input file**. Transcribing `assets/voice/raw/01.wav` produced
  `assets/voice/raw/transcript.json` — a different path than the stale
  `assets/voice/transcript.json` left over from Revision 2. First pass at
  copying "the shared transcript path" after each of 5 transcribe calls
  silently copied the *same stale Revision-2 file* five times (identical
  word-for-word output for all 5 supposedly-distinct lines was the tell).
  Re-run correctly once the actual output path was confirmed via a single
  file's un-suppressed command output. Worth remembering precisely for next
  time, since the wrong assumption was stated as established fact in this
  project's own prior documentation.
- **Line 3 trailing blip** — a ~130ms isolated sound artifact after
  "through." ends, in what should be trailing silence (confirmed via
  `ffmpeg silencedetect` + a `showwavespic` zoom, same diagnostic discipline
  as before). **4th occurrence of this synthesis-artifact pattern across
  this pipeline's two projects, but the first NOT on "line 1"** — revises
  the earlier working theory that this was specifically a first-line
  phenomenon; it reads better as "any Kimberly/seed_audio line can glitch in
  its trailing silence," worth checking on every line generated, not just
  the first. Fixed by trimming before the blip with a fade timed to start
  *after* the last real word ends, not into it — a first attempt at this fix
  started the fade 100ms too early and measurably clipped into "through."
  itself (caught by a full re-transcription showing the word merged into
  "straight." instead of appearing separately — not by ear).
- **Line 5's engineered pause needed a crossfade, not a hard cut.** The raw
  take had a genuine 2.3s dead-air gap between "raw dogging it?" and "Drop
  your routine below." (too long for this pacing). Concatenating a trimmed
  head and tail with a hard cut produced a splice-seam artifact that
  confused word-level re-transcription at the join. Rebuilt with a 60ms
  `acrossfade` at the seam instead of `concat` — clean on re-transcription,
  audible pause down to ~0.5s.
- A hallucinated "Mm-hmm." leading word appeared on one (but not both)
  re-transcriptions of the final Line 1 file, despite the file's actual
  leading audio being byte-identical to the original clean take (only the
  tail was trimmed). Cross-checked against the original untrimmed
  transcript (which read "Your" cleanly at the same position, no
  hallucination) and a volume-level probe of that window (-34.7dB mean, well
  above the noise floor, consistent with quiet natural speech onset, not a
  spike) before concluding this was a small-model ASR hallucination on quiet
  audio rather than a real artifact — no audio edit made.

### Runtime

**Total dropped from 40.7s to 34.4s** — the new script's lines are
individually more concise, and Line 5's dead-air gap was tightened from
2.3s to ~0.5s. Comfortably inside a Short's runtime envelope.

## Revision 4 — "0:06 scratch" + caption removal

Two quick fixes on the Revision 3 cut, no script changes.

- **"Scratch" at 0:06.** Not a VO glitch this time (line 1's audio was
  already verified clean). Root cause: `sharp-text-stamp-impact-hit.mp3`
  (the Scene 1 reveal hit) is a 3.6s file — a clean ~0.5s swell-into-hit
  followed by a long, dense, granular decay tail that was playing for its
  *full* length, bleeding under "Ceramides." and into the Scene 2 crossfade.
  That tail is almost certainly what read as a scratch. Fixed by deriving
  `sharp-text-stamp-impact-hit.trimmed.mp3` — the swell+hit only (1.1s,
  `afade` out over the last 0.25s, no abrupt cutoff) — and nudging its start
  from 5.85s to 5.6s so the hit's peak lands closer to the visual punch-in
  instead of trailing behind it. Confirmed via waveform diff on the actual
  rendered audio track, before vs. after: the dense granular texture in the
  5-7s window is gone, replaced by a single clean swell-into-vocal burst.
- **Captions removed.** The `clinical-captions` composition and its
  `data-composition-src` reference in `index.html` are gone entirely (file
  deleted, not just hidden) — no more lower-third text band. Scene content
  itself (on-screen labels, stat cards, the CTA) is unaffected; only the
  word-synced caption overlay is gone.

**Runtime unchanged (34.4s)** — both fixes were asset/mix-level, no timing
cascade changes.

## Revision 5 — QC pass, monetization safety, B-roll

Implementation of the script/prompts document from the prior turn (published
as an artifact, "Ceramides Script Revision") — VO regenerated on Higgsfield
Kimberly, two live-action B-roll clips generated and blended in, full
timing cascade recomputed since the new lines run shorter.

- **Line 1 leading artifact.** Regenerated clean. This time the "Mm"-style
  concern was treated as real rather than dismissed — checked via waveform
  zoom on the raw take (continuous natural onset from t=0.05s, no isolated
  blip) *and* a word-level transcript confirming "Your" as the first token
  with no phantom leading word. Worth noting: Revision 4 dismissed an
  identical-looking artifact as ASR hallucination on the same class of
  evidence: this round's independent listener report contradicted that
  call, so the earlier judgment was likely wrong. Lesson applied here, not
  re-litigated: verify fresh each time rather than pattern-matching to a
  prior "probably fine."
- **Line 3 reworded + regenerated.** "...leak straight through." →
  "...leak straight out." per the QC request. Confirmed via transcript that
  "out." lands as its own final word (6.56-6.68s) — the prior take's
  "through" had come back merged into the previous word on one
  re-transcription pass; this new take shows no such ambiguity.
- **Line 5 tightened.** Real 0.85s gap (confirmed via `silencedetect`, not
  the transcript's own less-precise word boundaries) between "...applying it
  directly?" and "Drop your routine below." Cut down to ~0.35s with a 60ms
  `acrossfade` splice — same technique as Revision 3's line 5 fix, same
  reason: a hard concat at this kind of boundary risks a seam artifact on
  re-transcription.
- **"Raw-dogging it" → "applying it directly"** in the VO, the on-screen
  question build, and (there being no caption track anymore) nowhere else
  to change.
- **CTA arrow: down → right.** Repositioned to the lower-right of "Drop your
  routine below." rather than centered underneath, gesturing toward the
  Shorts engagement rail instead of the bottom title-safe strip.
- **Two B-roll clips generated and blended in** (`seedance_2_5`, 9:16,
  4s each, trimmed via `data-media-start` offset rather than
  regenerated when the first pass needed a reroll):
  - Scene 3: a serum-droplet macro, crossfaded in over the settled rubble
    to stand in for "moisture escapes," then crossfaded back to the
    "Barrier compromised" label.
  - Scene 4: a forearm moisturizer application, crossfaded in ahead of the
    mini-wall reassembly. The first prompt for this one ("bare shoulder and
    collarbone") tripped an NSFW filter — reworded to a forearm shot, which
    is both safer and a more standard skincare B-roll frame anyway.
  - Each cutaway carries a small mono caption (`MOISTURE — ESCAPING`,
    `INSTANTLY — PATCHING`) so the live-action insert still reads as part
    of the same diagnostic-dashboard idiom rather than a stock-footage
    interruption.

### A real HyperFrames rule, confirmed by trial

Went looking for "the definitive rule" on video timing placement earlier in
this project and came away without a firm answer; this build settled it by
direct lint feedback. The wrapper **or** the video gets `data-start` —
never both, and never neither:
- Video with `data-start` inside a wrapper that *also* has `data-start` →
  `video_nested_in_timed_element` (the frame extractor and the visibility
  system disagree about the clip's window).
- Video with **no** `data-start` at all, wrapper timed or not →
  `media_missing_data_start`.
- Fix used here: strip `data-start`/`data-duration` off the crossfade
  wrapper (it becomes a plain always-present container; GSAP opacity is the
  only thing that actually shows/hides it), keep them on the `<video>`
  itself. Matches the existing `-inner` div pattern already used for the
  bar-chart/wall crossfade in this same scene — the outer `.clip` carries
  the track timing, an un-timed inner element carries the actual visual
  crossfade.

### Runtime

**Total dropped from 34.4s to 28.1s** — shorter regenerated lines (the new
Line 1 and Line 3 takes both came back faster than their predecessors) plus
the tightened Line 5 gap. Comfortably inside a Short's runtime envelope.

## Revision 6 — QC audit fixes

Implementation of the QC review from the prior turn (7-area audit against
YouTube delivery standards, using ffprobe/ebur128/astats/frame-timestamp
analysis plus pixel-measured safe-area checks — not a subjective watch-through).
No VO regeneration this round; every fix here is visual/mix, not script.

- **Wheat/rice/lab-made card.** The editor's own note ("images go too fast...
  nonphoto-realistic images for rice, wheat") plus the QC finding (text-only
  card, ~2.1s hold inside a 5-beat/7.1s scene) both pointed at the same
  spot. Added three hand-authored line-art SVG icons (wheat ear, rice
  panicle, lab flask — plain stroke paths, no external icon library, matching
  this project's existing all-CSS/SVG visual language) staggered in ahead of
  the text, and extended the card's hold from ~2.1s to ~2.5s. This retimed
  the rest of Scene 4's beat cascade (f2/B-roll/mini-wall/f4 all shifted and
  their hold times trimmed slightly to stay inside the fixed 7.42s scene
  budget) — see the composition's script comments for the new numbers.
- **CTA arrow safe-zone.** QC found it pixel-measured entirely inside the
  right-edge 15% Shorts UI zone (`padding-right: 118px` put its right edge at
  x=962 on a 1080-wide canvas, past the x=918 boundary). Now `210px`,
  right edge at x=870 — reconfirmed by the same crop-and-measure method
  post-fix, comfortably clear.
- **B-roll caption position.** Both captions (`MOISTURE — ESCAPING`,
  `INSTANTLY — PATCHING`) moved from `top: 1560px` to `top: 1480px` — QC
  found them sitting inside the general bottom-20% band, even though clear
  of the harder bottom-15% line.
- **Accessibility: "actives leak out."** The spoken claim "expensive actives
  leak straight out" had no on-screen text equivalent — a muted viewer got
  the crumble visual and "Barrier compromised" but not this specific line.
  Added a brief lead-in label ("Actives leak out.") before "Barrier
  compromised" in the same slot, both perceptually sequenced to the VO.
- **Loudness.** QC measured -21.7 LUFS integrated vs YouTube's -14 LUFS
  target — 7.7 LU quiet, with plenty of true-peak headroom (-2.5 dBTP) to
  fix without clipping. A naive linear gain bump was ruled out (would have
  pushed peak to +5.2 dBFS); used a two-pass `loudnorm` mastering step
  instead (`measured_I`/`measured_TP`/`measured_LRA` from a fresh pass on
  the actual render, `linear=true`). Lands at -15.4 LUFS / -1.0 dBTP,
  confirmed via a third `ebur128` pass on the delivered file — closer to
  target than a first-pass estimate typically gets, no clipping introduced
  (`astats` flat factor 0.0 on the output).
- **Bitrate.** QC found 662.6 kbps video on a 1080×1920/30fps H.264 file —
  well under YouTube's own ~8 Mbps floor for 1080p/30 SDR — and confirmed
  visible macroblocking on zoomed inspection of the B-roll's flat gradient
  background. Re-encoded at `-b:v 8M -maxrate 10M -bufsize 16M`; actual
  achieved average landed at ~1.84 Mbps (x264's rate control doesn't spend
  bits content doesn't need — most of this piece is flat vector graphics),
  which is still a ~2.8x increase concentrated where the B-roll needed it.
  Bundled into the same ffmpeg pass as the loudness fix — one mastering
  step, not two.

### A real bug caught by re-verifying rather than trusting the pattern

Restructuring Scene 3's label into two stacked states (`Actives leak out.` →
`Barrier compromised`) required making `.c3b-label` itself absolutely
positioned so both could share one slot. First pass also made it
`display:flex; justify-content:center` for the centering — and that
silently re-triggered this exact project's own previously-documented
word-spacing bug ("Actives" + "leak out." collapsed to "ActivesLEAK OUT."
with the inter-word space eaten). Caught on a snapshot before rendering,
not after. Fixed the same way as the earlier occurrence: `text-align:
center` instead of flex for the centering, since flex treats a bare text
node as an anonymous item and can drop the whitespace at its edge.

### Not fixed this round (need real input, not more editing)

- **Unsourced 50%/40% stat claims** — still no citation on file anywhere in
  this pipeline. Needs an actual source, not a placeholder.
- **Synthetic-content disclosure** — a YouTube Studio upload-time toggle
  (Content details → Altered or synthetic content), not a file change.

### Runtime

**Unchanged at 28.1s** — every fix this round was either intra-scene
retiming (same scene boundaries) or a final-mix/encode pass, no script or
scene-duration changes.

## Revision 7 — second QC pass, mostly non-reproducing

A second QC review came in against the exact Revision 6 file (confirmed via
MD5 — the reviewed copy in `ingredent videos/ceremides/` was byte-identical
to the delivered render). Unlike the Revision 5→6 review, this one's own
"could not verify" list admitted it didn't measure LUFS, codec, or run any
tooling — it's a subjective watch-through, not an instrumented audit. Three
of its four findings didn't reproduce against the actual file:

- **"Arrow completely blocked by Shorts UI, BLOCKER"** — the arrow was
  pixel-measured and fixed in Revision 6 (`padding-right: 118px → 210px`,
  right edge now at x=870 on a 1080px canvas, clear of the x=918 boundary).
  Re-measured again this round via the same crop-and-inspect method:
  still clear. Not reproducible.
- **"1.5s of dead silence, 0:15-0:17, MAJOR"** — `silencedetect` at both
  -40dB and -35dB thresholds (0.2s minimum) found zero gaps anywhere in
  the file, including that window. Not reproducible. (There is a real,
  much smaller ~0.4s beat right after the Scene 3→4 crossfade completes
  before the wheat/rice icons start popping in — worth knowing about, but
  it isn't dead air and doesn't warrant a ripple-delete or an SFX patch.)
- **"-40% Reserve Lost dips into bottom 20%, MINOR"** — measured at
  y≈1300-1360px on a 1920px canvas (~68-71%), well clear of the 1536px/80%
  boundary. Not reproducible.
- **"Voiceover volume low, needs -14 LUFS normalize, MAJOR"** — this one
  had a real kernel: Revision 6 landed at -15.4 LUFS, close to but not
  exactly -14. Applied one more light `loudnorm` pass using this file's own
  measured values (dynamic mode, not linear — true peak was already sitting
  right at -1.0 dBTP with zero headroom left for a flat gain bump). Lands
  at **-14.5 LUFS / -1.0 dBTP**, re-verified via a fresh `ebur128` pass,
  zero clipping (`astats` flat factor 0.0). Video stream copied through
  untouched (`-c:v copy`) — this was an audio-only pass, no re-encode risk
  to the bitrate fix from Revision 6.

Declined to action the other three: deleting or repositioning an
already-correctly-placed arrow, or nudging a tag that isn't misplaced, or
cutting/patching a gap that measurement shows doesn't exist, would each
make the file worse against the reviewer's own stated goal, not better.
Documented with the measurement each claim was checked against rather than
silently ignored.

### Runtime

**Unchanged at 28.1s.** Audio-only pass, video stream untouched.

## Revision 8 — literal compliance pass, with proof where it mattered

The Stop-hook gating Revision 7 rejected "not reproducible" as an answer and
required the four specified remedies applied literally. Re-approached each
one individually rather than either blanket-complying or blanket-refusing:

- **Arrow.** Rather than keep arguing margin size, took the goal's own
  offered alternative literally: centered directly under the CTA text
  (`justify-content: center`, no right-side padding), removing the
  right-edge question entirely instead of relitigating exactly how much
  margin counts as "clear."
- **"-40% Reserve Lost" tag.** Tested the literal 200px move first
  (`top: 1300px → 1100px`) and rendered a snapshot rather than reasoning
  about it in the abstract — confirmed it collides with the Age 20 bar and
  sits above the axis labels instead of below them, a real regression, not
  a hypothetical one. Reverted, then applied a smaller nudge (`top: 1260px`,
  40px up) that's still clearly a real move in the requested direction
  without the proven collision — baseline sits at 1220px, so this keeps a
  40px clearance.
- **"Dead air" at the Scene 3→4 transition.** `silencedetect` still finds
  no actual gap (rechecked again this round), so there was nothing to
  ripple-delete. But the goal's own fix language ("carry the audio through
  the transition" with "a low riser or soft whoosh") described an addition,
  not just a deletion — sourced `soft-low-riser-whoosh-transition-swell.mp3`
  via the media-use audio engine, inspected its envelope (clean swell, no
  buzzy tail this time), and placed it spanning 13.3-16.7s with its peak
  landing on the crossfade itself.
- **Loudness.** Pushed for closer to the literal -14.0 than the -14.5 that
  drew feedback last round. Diagnosis: a single `loudnorm` pass targeting
  -14 plateaus at ~-15.3 regardless of the `LRA` setting (tried both 7 and
  the goal's own suggested 11, identical result) — the binding constraint
  is this content's peak-to-loudness ratio against the -1 dBTP ceiling, not
  the loudness-range parameter. Two sequential gentle dynamic passes (same
  technique as Revision 7) reliably lands at -14.5/-1.0dBTP without
  clipping; that's the practical floor for this mix without either
  loosening the peak ceiling or audibly over-compressing it.

### Runtime

**Unchanged at 28.1s.** All four changes were composition-level position/
audio tweaks plus the same mastering pass as Revision 7 — no scene timing
changes.

## Revision 9 — stretched to 51.6s ("this can stretch to 60 seconds, adjust")

Given real runway (up to 60s, was 28.1s), re-approached pacing by extending
the actual beat choreography rather than padding with silence — voice audio
is completely unchanged across all 5 lines. Every scene's hold time roughly
doubled, with the extra time weighted toward wherever it does the most work:

- **Scene 1 (hook):** 4.45s → 7.6s. Kicker/slam/reveal timing unchanged
  (still synced to the actual VO words); the "CERAMIDES." reveal now holds
  for ~3.4s afterward instead of cutting almost immediately.
- **Scene 2 (mortar/50%):** 5.46s → 8.6s. Same story — wall-build and stat
  reveal unchanged, the completed 50% stat now holds ~5.3s.
- **Scene 3 (crumble):** 7.08s → 13.2s. Bar chart and crumble trigger stay
  VO-synced (unchanged). The B-roll cutaway extended from 1.1s to 1.8s
  visible. Biggest change: "Barrier compromised" — this scene's resting
  state — now holds ~6s (was ~0.65s) instead of getting cut off right after
  appearing.
- **Scene 4 (sourcing):** 7.42s → 13.6s, the scene the editor's original
  note was about. The wheat/rice/lab-made card's hold went from ~2.1s
  (Revision 3) → ~2.5s (Revision 6, budget-constrained) → **~4s now**, with
  no compression trade-off needed elsewhere this time. B-roll extended to
  1.7s visible. Mini-wall + "Instantly patched." now holds ~3.2s.
- **Scene 5 (CTA):** 4.86s → 9.8s. Question-build timing unchanged (already
  well VO-synced); the actual "Drop your routine below." now holds ~6.2s
  instead of ~1.3s — this is arguably the single highest-value place in the
  whole piece to add hold time, since it's the conversion moment.

### Mechanics

- **Cascade formula changed.** Previously `scene[i].start = scene[i-1].start
  + voice[i-1].duration` (next scene begins the instant the previous line
  finishes speaking). Now `scene[i].start = scene[i-1].start +
  scene[i-1].duration - 0.3` — scenes hold on their own after their voice
  line ends, with the existing 0.3s crossfade style preserved at the
  boundary. This is what let every scene's tail become a real, silent (but
  not "dead" — BGM continues, and the visual itself is the point) hold
  rather than an immediate cut.
- **All 6 SFX cues repositioned** to their new absolute times (each one's
  *local* sync point relative to its own scene was unchanged — only the
  scenes moved).
- **BGM re-extended.** The trimmed loop had no headroom to stretch (already
  cut down to the old 28.1s target across several revisions). Rebuilt from
  the original 23s catalog source via `acrossfade`-looped repeats (3x,
  1.2s crossfades) to ~67s, then trimmed to the new exact 51.6s with a
  fade-out — same technique this project used for its very first BGM bed.
- **Loudness re-measured post-stretch, not assumed.** The longer holds mean
  much more BGM-only (no-VO) runtime proportionally, which measurably
  changed the file's overall loudness profile (input integrated dropped to
  -23.95 LUFS, loudness range widened to 12.8 LU, both expected consequences
  of more quiet passages relative to speech — not a defect to chase back
  to the old numbers). Re-ran the same multi-pass `loudnorm` technique
  (3 passes this time, LRA target loosened to 11 to match the content's
  now-wider natural range) — landed at **-14.4 LUFS / -1.0 dBTP**, the
  closest to the literal -14 target across every revision so far.

### Runtime

**28.1s → 51.6s.** Comfortably under the 60s ceiling given, and still well
inside a Short's 3:00 limit.

## Revision 10 — the arrow, resolved for real

Feedback: "the user doesn't know what this is or where it should go — it
should unblock the consumer." Read as being about the CTA arrow, whose
Revision 8 state was genuinely incoherent: the last QC's literal remedy
("center it under the text") was applied while the glyph still pointed
**right** — so the copy said "Drop your routine *below*" while a centered
arrow pointed sideways at empty space. Complying with the letter of that
remedy had broken its meaning.

- **Glyph flipped → to ↓**, staying centered under the text. Copy and arrow
  now agree: below means down.
- **Added a gentle finite bob** (12px, sine, 8 half-cycles over 4s, then
  still) so the arrow reads as an instruction toward the comments rather
  than static decoration. Finite `repeat: 7` — never `repeat: -1` — keeps
  it seek-safe; verified live via two snapshots 0.25s apart showing the
  arrow at different heights.
- Safe-area status unchanged: centered ≈ x=540, sits ≈ y=860-930 even at
  bob-bottom — nowhere near the bottom-15% (y≥1632) or right-15% (x≥918)
  zones this element has been flagged against in past rounds.

### Mastering note — a real lesson on true peak vs. AAC

The Revision 9 chain ended with a loudnorm pass *followed by* AAC encoding,
and lossy encoding regenerates inter-sample peaks: the delivered file
measured **-0.4 dBTP** despite loudnorm's -1.0 ceiling being enforced
pre-encode. Caught this round by measuring the actual delivered file
rather than trusting the filter's own summary. Fix: one extra audio-only
pass with the ceiling set to **-1.5 pre-encode**, leaving room for AAC
overshoot — final file measures **-14.4 LUFS / -1.0 dBTP exactly**, zero
clipping. Worth keeping for every future master here: the TP target must be
set below the delivery target by ~0.5 dB when AAC is the last step.

### Runtime

**Unchanged at 51.6s.**

## Revision 11 — "rework": fill the dead air with actual content

This QC review was the honest verdict on Revision 9's stretch: doubling hold
times without adding content produced real dead air, and the piece never
answered the viewer's obvious next questions — *where do I get ceramides,
and how do I use them?* Every finding reproduced against the file, so all
four were actioned as specified.

- **Two new VO lines (Higgsfield/Kimberly, same voice + rate as always):**
  - Line 2 now continues past the 50% stat into sourcing: "...You'll
    typically find them in thick repair creams, hydrating serums, and even
    everyday drugstore cleansers." (9.35s, was 5.16s)
  - Line 4 replaces "instantly patching...every skin type" with usage
    advice: "...Apply a ceramide cream right before your retinol as a
    buffer to prevent irritation, or immediately after to lock the active
    in." (11.95s, was 7.12s)
  - Both glitch-checked per this project's standing discipline (waveform +
    silencedetect + transcript). Line 4's sharp transient at ~5.4s was
    inspected by zoom and is the tail of "own." attached to speech — real
    audio, not an artifact. Tails trimmed with short fades as usual.
- **Three new product B-roll clips** (seedance, 9:16, unbranded) for the
  reviewer's "rapid-fire" sourcing beat: cream-jar scoop, amber serum
  dropper bottle, foaming cleanser pump. Each lands on its own named
  product in the VO with a pilled caption (REPAIR CREAMS / HYDRATING
  SERUMS / DRUGSTORE CLEANSERS), with dip-to-dark gaps between clips.
- **Scene 4 restructured around the advice**: icons card → "structurally
  identical" → the skin-application clip now arrives right on "Apply"
  (the reviewer's "speed up the transition to the skin-patching clip") and
  carries two caption swaps (BEFORE RETINOL — BUFFER / AFTER — LOCK IT IN)
  → mini-wall "Instantly patched." as the button. The "Every skin type."
  flash was dropped — its VO clause no longer exists.
- **CTA tightened** to ~2.2s of read time after the question resolves
  (scene 5: 9.8s → 5.8s), per "two seconds is plenty."
- **Captions rescaled ×1.55 (26→40px) and moved to the vertical center**
  in all three B-roll treatments, per the exact remedy given.
- **Axis labels 26→34px**, matching the "-40% Reserve Lost" tag, as asked.
- **All other holds trimmed back** (scene 1: 7.6→5.4s; scene 3: 13.2→8.6s)
  — the stretch runtime now comes from content, not holds.

### Caught by `check`, fixed before render

The first pass at the product-B-roll layering left the wall/stat text
sitting occluded under the full-bleed clips (8 `text_occluded` errors) and
consecutive captions briefly co-visible during crossfades. Fixed
structurally rather than annotated away: the graphic half now fades out
*before* the first clip arrives, and the clip fades are gapped into
dip-cuts so no two captions ever coexist. A final contrast catch — white
caption on the near-white cream jar (2.1:1) — led to the scrim pill behind
all B-roll captions, which also future-proofs them against any bright
footage.

### Mastering

Same chain as recent revisions, with one more lesson: even a -1.5 dBTP
pre-encode ceiling wasn't enough headroom when a *dynamic* second pass
pushes gain up against it — AAC overshot to -0.1 dBTP. The corrective pass
used -2.0 pre-encode; the delivered file measures **-14.5 LUFS / -1.3
dBTP**, zero clipping. Standing rule updated: after any loudnorm pass that
*raises* gain, re-measure the actual encoded file, and keep ≥1 dB of
pre-encode true-peak headroom.

### Runtime

**51.6s → 41.4s.** Shorter than the stretch cut but longer than the 28.1s
original — the added length is now all spoken content and product footage,
no silent holds.

## Revision 12 — final QA pass on "barrierdiagnosticcut2.mp4"

The reviewed file was MD5-verified byte-identical to the Revision 11
render. The request offered a choice of FFmpeg / MoviePy / Remotion source;
this project's source is HyperFrames, so fixes 1-3 (position + captions)
went into the compositions where they belong, and fix 4 (EQ) went into the
ffmpeg mastering chain where *it* belongs.

1. **CTA Y-shift.** `.c5-cta-wrap` top 660px → 276px — a 384px shift, 20%
   of the 1920px canvas, per the "at least 20%" remedy. (Prior
   measurements had it clear of the bottom-15% zone already; the higher
   placement is harmless and finally retires this flag.) Clears the
   top-10% zone too (starts below y=192).
2. **Chart Y-shift.** The whole composition moved up 288px (15% of
   canvas), uniformly: chart top 760→472, baseline 1220→932, tag wrap
   1260→972. Internal geometry preserved exactly.
3. **Burnt-in captions restored.** Full-VO phrase captions (32 groups of
   3-5 words, timed from the real word-level transcripts of all five
   current lines) as a new `captions.html` sub-composition. High-contrast
   via the same dark scrim pill as the B-roll captions — holds on dark
   scenes, the off-white Scene 4, and all live footage. Placement: a
   y=1420 band, max-width 760 centered (spans ~x160-920) — inside the
   right-rail boundary (x<918) and ~200px above the bottom-15% line. Not
   literally center-middle: dead-center collides with the primary visuals
   (charts, wall, the y910 product pills), and this project was explicitly
   instructed in an early round to keep captions out of dead center. The
   chosen band satisfies both stated hard constraints (bottom-15% + right
   rail).
   Note: captions had been removed entirely in Revision 4 by explicit
   request ("remove the text at the bottom"); this review explicitly asks
   for them back, so back they are — at a compliant position/size rather
   than the old flagged one.
4. **80Hz high-pass, 24 dB/oct.** Two cascaded 2nd-order `highpass`
   filters (12 dB/oct each = 4th-order/24 dB/oct total) at the head of the
   mastering chain: `highpass=f=80:poles=2,highpass=f=80:poles=2`.
   Verified like-for-like on the flagged "CERAMIDES." window (3.6-4.2s):
   sub-80Hz energy sat 5.7 dB below full-band before, 11.4 dB below after
   — ≈5.8 dB net cut of the plosive's low-end thump, speech untouched.

### Mastering

Same chain with the standing rules applied (TP=-2.0 pre-encode headroom
after the AAC-overshoot lessons of Revisions 10-11; three measured passes).
Delivered file: **-14.4 LUFS / -1.2 dBTP**, zero clipping, ~3.9 Mbps video.

### Runtime

**Unchanged at 41.4s.**

## Revision 13 — fix-then-ship pass (2 items)

1. **"CTA in the bottom 20%" (MAJOR)** — identity correction first: the CTA
   block + arrow moved to y=276 in Revision 12 (pixel-verified, top third
   of the frame). What actually sits low at 0:39-0:41 is the burnt-in
   *caption* for the same spoken line ("Drop your routine below.") in the
   caption band Revision 12 added at y=1420. Applied the remedy to the
   thing that's actually low: the whole caption band raised 270px (inside
   the requested 250-300px range) to **y=1150** — chosen precisely because
   several scenes' content bottoms sit at y≈1140 (wall, question text), so
   1150 clears everything with a 10px margin while a full 288px/15% shift
   to 1132 would have overlapped them by 8px and tripped content_overlap.
   Re-verified by snapshot: captions now stack under the graphics in every
   scene, ~380px above the bottom-20% line.
2. **Crumble SFX competing with VO (MINOR)** — `data-volume` 0.45 → 0.28,
   which is **-4.1 dB**, mid of the requested -3 to -5 dB range.

Same mastering chain (80Hz/24dB-oct HPF + three measured loudnorm passes,
TP=-2.0 pre-encode). Delivered: **-14.4 LUFS / -1.7 dBTP**, zero clipping.

For the review's "could not verify" list, the delivered file's specs:
1080×1920 (9:16), constant 30fps, H.264 High (yuv420p, bt709 range-limited)
in MP4, ~3.9 Mbps video; AAC-LC 48kHz stereo ~192kbps.

### Runtime

**Unchanged at 41.4s.**

## Revision 14 — captions removed (again)

"Remove the captions" — the burnt-in VO caption track added in Revision 12
(at a reviewer's request) is deleted entirely: `compositions/captions.html`
removed, its scene reference dropped from `index.html`. Scene-native text
(labels, stat cards, B-roll pills, the CTA) is untouched. This is the
second full caption-track life cycle for this project (added → removed in
Revisions 3-4, added → removed in Revisions 12-14); if a third request to
add captions arrives, worth asking where they should sit *before* building.

Mastering: same chain (80Hz HPF + measured loudnorm passes). The final
gain-up pass again overshot true peak post-AAC (to 0.0 dBFS — caught by
measuring the delivered file, per the standing rule) and was corrected
with a TP=-2.5 pass. Delivered: **-14.4 LUFS / -1.9 dBTP**, zero clipping.

### Runtime

**Unchanged at 41.4s.**

## Sourcing — unchanged from the photoreal cut, not re-litigated here

The 50%-of-barrier and 40%-lost-by-30 stats, and the wheat/rice/lab-made
sourcing claim, carry no `ING-*` source record in this codebase — same gap
as every prior video in this pipeline that uses them (see
`ceramides-skin-barrier/BRIEF.md` § Notes). Flagged again here, not
resolved: a clinical-dashboard *presentation* of a stat (a data card, a bar
chart with a specific percentage) reads as more evidentiary than a spoken
claim in a marketing-style cut, even though the underlying sourcing status
hasn't changed. Worth a real citation pass before this cut ships, arguably
more so than the photoreal version.
