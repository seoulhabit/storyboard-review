# Delivery — peeling-question-open

Pilot of a new recurring format, **"A Question We Marked Open"**. This is a
different treatment of a topic `videos/peeling-not-progress/` already shipped
(30.1s, ink/paper/aqua palette) — that project is untouched by this build; this
one exists to prove out the format itself (question → stamped short answer →
reaction/result split → evidence label → boundary → better question) so it can
be reused with different content, not to replace the earlier video.

## Render

**`renders/peeling-question-open_FINAL_mastered.mp4`** — the only render kept;
every earlier iteration from the fix-and-reverify loop was deleted once
superseded, matching house convention.

- **750 video frames at 30fps = 25.000s of picture** (confirmed via
  `ffprobe -count_frames`; video stream copied through unchanged by the
  loudness pass), 1080×1920, h264 video / AAC 192kbps audio. The container's
  reported 25.1s duration is a known `ffmpeg loudnorm` audio-padding artifact,
  not a picture-length change.
- Loudness-normalized: two-pass `ffmpeg loudnorm` (measured pass, then a
  second pass against the measured values), video stream copied through
  unchanged. Measured **−14.1 LUFS integrated / −1.5 dBTP** against a target
  of −14 LUFS / −1.5 dBTP. Raw pre-master render measured −22.3 LUFS
  integrated, confirming the render itself does not apply loudness
  normalization (per house convention, this is always a separate step).
- No voiceover (silent-first, matching `peeling-not-progress`'s own
  precedent — see BRIEF.md). BGM bed (`assets/bgm/track.mp3`, reused from
  `peeling-not-progress`) plus 12 SFX cues are the only audio.
- **Loop-aware BGM envelope**, a deliberate departure from the usual
  declick-to-true-silence convention: both ends land on a low floor (0.15)
  rather than 0, because a hard fade-to-silence-then-restart creates an
  audible dead spot exactly at the seam every replay. Confirmed on the actual
  mastered file via `ffmpeg astats` RMS: start window (0–0.6s) measures
  **−8.9 dB RMS**, end window (24.4–25.0s) measures **−24.5 dB RMS** — both
  real, audible signal, neither true digital silence.

## Captions

**`captions/peeling-question-open.srt` and `.vtt`** — 21 cues, hand-authored
directly from `STORYBOARD.md`'s copy deck and each scene's actual GSAP timeline
positions, not from ASR (there is no speech — the on-screen text and its exact
timing were already authored artifacts). Citation pills each get their own
cue; the SFX-carried chime on the closing lockup is bracketed; routine UI
clicks are omitted. Decorative category labels (REACTION / RESULT) are not
captioned redundantly alongside their own sentence — only the sentence itself
is captioned, per the skill's rule against a caption repeating a decorative
label's exact phrase with no new meaning.

No separate burned-in caption track: the on-screen kinetic type *is* the
caption layer for this silent short (matching `peeling-not-progress`'s
approach) — the sidecar files are the caption deliverable.

## Thumbnail

**`assets/thumbnail/thumbnail-final.png`** — extracted from the real render
at the scene-2 stamp's resolved state (~2.2s, after the impact settles),
graded `eq=contrast=1.05:saturation=1.08, unsharp=5:5:0.4` (same filter chain
as `peeling-not-progress`'s own finalized thumbnail, re-applied to this
video's own green/ink palette rather than copied verbatim).

Two candidates were tested at true grid scale (120×213px, matching a mobile
scroll-grid thumbnail) before choosing: the scene-1 peel-hook frame rendered
as an unlabeled, textless gradient blob at grid size — no legible information,
easily mistaken for a loading placeholder. The stamped "SHORT ANSWER: NO."
card stayed fully legible at the same scale and is inherently curiosity-driving
(it answers a question the viewer hasn't heard yet). Kept both source
candidates plus grid-check proofs in `assets/thumbnail/` per the file
convention — nothing deleted, the rejected one labeled for what it tested.

## Full source list (for the video description)

- Griffiths CE, Kang S, Ellis CN, et al. "Two concentrations of topical
  tretinoin (Retin-A) cause similar improvement of photoaging but different
  degrees of irritation." *Archives of Dermatology*, 1995. PMID 7544967.
  48-week double-blind trial, n=99. Shown on screen as `Arch Dermatol · 1995`.
- American Academy of Dermatology. "How to maximize results from anti-aging
  skin care products." Fetched and read directly for this build (not
  carried over from the predecessor without a check):
  https://www.aad.org/public/everyday-care/skin-care-secrets/anti-aging/maximize-anti-aging-products
  — verified live to carry both the stop-instruction ("Stop using a product
  that stings, burns, or tingles...") and the prescription caveat ("If you
  are using a product prescribed by your dermatologist, ask if this should
  be happening before you stop using it."), both represented on screen in
  scene 5. Shown on screen as `AAD guidance`.

## Title

**Peeling Is Not Proof Your Skincare Works**

## Pinned comment (draft)

> Peeling isn't the scorecard. What changed — ingredient, strength, frequency,
> or combination — is the better question. What's a claim you'd want us to
> audit next?

## Verification record

`npx hyperframes check` passed cleanly at every stage but caught none of the
three real defects found below — consistent with `REPORT.md`'s own recorded
history of `check` reporting 0 issues on genuinely broken renders. All three
were found by extracting and eyeballing real frames, exactly as the skill
requires, not by trusting a passing lint.

1. **Void-box reveal rendered fully drawn from frame zero** (scene 3,
   `03-reaction.html`). The empty "result" outline was meant to stay hidden
   until a 1.00s stroke-draw reveal at local t=2.45s; instead it rendered
   solid across the whole scene. Root cause: the SVG element's
   `stroke-dasharray`/`stroke-dashoffset` initial state was set via a bare
   `gsap.set()` call outside the GSAP timeline, which does not reliably
   survive a hard seek in this render pipeline — the exact failure class the
   skill documents for elements hit by multiple `fromTo()` calls, generalized
   here to a single `.to()` reveal whose *starting* state depended on an
   out-of-band set. Fixed by moving the initialization to `tl.set(..., 0)`
   inside the timeline, and separately switching the shape from an SVG
   `<rect>` to an equivalent `<path>` (matching the predecessor's own proven
   `getTotalLength()` pattern, which uses `<path>` elements exclusively).
   Confirmed fixed via a 9-frame composite spanning the full scene: hidden
   through t=7.00, progressively drawing 7.30–7.80, fully complete by 8.20
   and stable afterward — matching the authored timeline exactly.
2. **A decorative rule rendered ~90% drawn from frame zero** (scene 4,
   `04-evidence.html`). `.badge-rule`'s CSS default was `scaleX(0.9)` instead
   of `scaleX(0)` — likely a copy-paste residue — so the rule appeared before
   the badge it was meant to decorate had even stamped in. Fixed the CSS
   default and additionally registered a `tl.set(..., 0)` baseline, since this
   element is hit by two tweens (entrance + a later breathing pulse) at
   different positions.
3. **The loop's hero panel didn't match scene 1's geometry** — measured, not
   assumed. Scene 6's `.text-stack` originally used a smaller font-size
   (96px/1.16) than scene 1's (108px/1.12); since `.glass-panel` is `flex:1`
   in the same `.stage` column, this shrank scene 6's panel by ~38px versus
   scene 1's. Matching the font-size exactly *still* left a 121px mismatch —
   traced to the closing couplet's first line ("Don't follow the claim.")
   wrapping to two lines at 108px in the safe column, which inflated
   `.text-stack`'s real height further. Fixed by shortening the copy to "Not
   the claim." / "The question." (fits one line each, preserves the
   claim-vs-question opposition). Confirmed by a pixel-column measurement of
   the panel's own first contiguous non-background run (not a blind
   whole-column scan, which was initially contaminated by the couplet text
   itself): scene 1 frame 0 and scene 6's resting frame now both measure
   panel top=192, bottom=1201 at every tested x-column.

All four QC scripts (`check-safe-area.py`, `check-static-hold.py`,
`check-blank-frames.py`, `check-sfx-durations.py`) run clean against the final
render. `check-safe-area.py` (hard gate): 0 findings across 100 sampled
frames. `check-static-hold.py`: 0 findings across 50 sampled frames — no scene
holds frozen more than 2.5s. `check-blank-frames.py` (advisory): 4 near-blank
windows flagged, all at scene-boundary opening beats (the deliberate "beat
before the beat" pattern already established and gate-passing in
`peeling-not-progress`'s own `01-hook.html`); each verified by direct frame
inspection to be legitimate, well-composed content, not a defect — confirmed
false-positive on this tool's luma-variance metric, which cannot see sparse
serif type against a large flat ground. `check-sfx-durations.py`: 0 findings.

Every scene boundary, frame zero, and the loop's resting frame were extracted
and eyeballed directly, not inferred from source. Contrast: 20/20 checks pass
WCAG AA per `npx hyperframes check`; coral (this project's one "limit"
accent) is used only as a small filled dot, never as text, after confirming
it falls under the 4.5:1 floor on every ground color in this palette.

## Known gaps / not done here

- **No paper-tear SFX** exists anywhere in this repo, and none was generated
  for this build — the peel beat runs on the existing glass-clink and whoosh
  cues instead. Flagged in the approved plan; not fabricated as a placeholder.
- **`backdrop-filter` frosted glass** is proven in this repo
  (`centella-tiger-grass`, 7 shipped renders) and is confirmed working here
  too via direct pixel inspection, but it remains a GPU-dependent,
  environment-scoped effect — re-verify on any future non-macOS render
  target before trusting it blind.
- This render used `PRODUCER_FORCE_SCREENSHOT=true` to force the `screenshot`
  capture path. On this machine, `beginframe` mode was observed active by
  default even on macOS (contradicting the plain reading of `hyperframes@0.8.20`'s
  own bundled capture-mode selection logic, which should gate `beginframe` to
  Linux only) — not fully root-caused, but the escape hatch reliably produces
  a consistent, verifiable render, and every fix in this delivery was
  confirmed against a `screenshot`-mode render. Re-verify capture mode on any
  future render of this project rather than assuming the default is safe.
