# Policy-change proposals

Findings from runs that had no rule to apply. The learning loop PROPOSES here;
it never edits `decision-policy.md` directly (SKILL.md §1).


---

## 2026-09-03 · run `hyaluronic-acid-vs-filler` (long-form 16:9, 180.000s)

### P1 — `[S1/S-3]` / `[S1/S-4]` have no rule for a multi-character script
**Found:** the supplied story was a two-hander (SoulHabit + Jay). `[S1/S-3]` says
"one presenter per video, no switching"; `[S1/S-4]` says a channel voice, "once
chosen, never rotate"; `[S4/V-2]`'s two-generation cap assumes a single VO.
Nothing covers a second *character*.

**Applied this run:** Kimberly stayed the narrator and was NOT rotated; a second
voice (Grady, preset) was added for the foil, and the baseline records both under
a new `voice.cast` map. 25 per-turn stems, one generation each.

**Proposed rule (`S-4b`, cast):** a script with more than one named speaker
declares a `cast` map in the baseline. The channel voice is bound to the narrator
role and never rotates; additional roles take voices from a stated fallback
ordering and are appended to `voice.cast`, never overwriting `voice.id`. The
generation cap becomes per-turn, not per-video, because a two-hander's clock is
the assembled timeline rather than one file.

**Also worth writing down:** a speaker turn is the smallest unit `[S5/C-1]` can
proportion beats across — its character-offset interpolation cannot cross a voice
change. That is a real constraint on stem granularity and it is not stated
anywhere.

### P2 — three defects in `scripts/beats_to_composition.py`
All three make an authoring-time check pass while the rendered composition is
static, which is the exact class of failure `[S7/R-2]` warns about ("an authored
beat is not the same thing as a pixel changing") — except here it is inside the
generator, not downstream of it. Each was caught by `hyperframes check`'s motion
pass and worked around in this project's own builders.

1. **An offset-0 beat is counted for cadence but emitted with no tween.** The
   generator composes the first beat at frame zero (correct — frame zero must not
   be mid-fade) and emits neither a `gsap.set` nor a tween for it. But its
   `[S5/C-2]` check still counts that beat as covering `[0, dur]`. Measured on
   `s02-cousins`: authored gap 1.9s, actual rendered gap 3.6s.
   *Fix:* treat an offset-0 first beat's coverage as a point, not an interval.

2. **Consecutive `hold` beats emit identical targets.** Every hold emits
   `{x: 6, y: -4, scale: 1.01}` (alternating sign only in some paths), so after
   the first, the element is tweened to where it already is — zero movement.
   `check` measured an 8.43s frozen window on a scene with three such holds.
   *Fix:* cycle distinct drift targets per hold.

3. **A `wipe` beat emits a `clipPath`-only tween, which the motion pass cannot
   see.** `clipPath` changes what is painted, not the bounding-box geometry
   `keepsMoving` samples. A run of consecutive wipes therefore reads as frozen —
   9.03s on `s12-do-not-inject`, whose tail is three wipes and nothing else.
   *Fix:* pair every clipPath reveal with a short travel on the same element.
   This is more motion, not a metric dodge: a reveal whose only moving part is
   the clip edge is genuinely low-motion on a 1920-wide frame.

### P3 — the generator paints ink text on a dark ground
`beats_to_composition.py` sets `--ink: #131516` on `#root` and then paints
`#root` with the scene's own `bg`. On any dark-ground scene that is **1:1
contrast — invisible copy**, confirmed by `check`'s contrast pass on
`#s04-named-b0` and `-b2`. It affects every dark generated scene, and a project
that never uses a dark ground would never see it.
**Proposed:** the generator should flip `--ink`/`--muted` when the scene `bg`
is dark, the way a hand-authored scene must.

### P4 — `id_requires_css_escape` is a warning but is load-bearing
The generator derives every element id from the scene id. A beat sheet with
scene ids like `01-lineup` produces `#01-lineup-b0`, and
`querySelectorAll('#01-lineup-b0')` **throws a SyntaxError** — so every GSAP
tween in every scene fails and the render freezes. `check` reports this at
**warning** severity (89 of them here), so it does not gate.
**Proposed:** either the generator sanitises scene ids to start with a letter, or
`[S5]` requires it of the beat sheet. A warning that silently freezes the whole
render is mis-severed.

### P5 — `maxStaticSec` for long-form is ambiguous in the skill's own documents
`[S7/R-1b]` says to set the sidecar's `keepsMoving.maxStaticSec` "from the
format's own cadence cap rather than the engine's 2s default, which is a Shorts
number". But `CADENCE_CAP["long"]` in the generator is *also* 2.0, so the
generator emits the very number R-1b calls a Shorts number, while
`catalog/tooling/check-cadence.py` raises its long-form quiet ceiling to **6.0**
and `youtube-delivery.md` sets long-form cadence at 8-12s.
**Proposed:** name one long-form number and use it in all three places. This run
used 6.0, matching `check-cadence.py --longform`, and left the post-render pixel
gate strict.

## Filed 2026-09-04, hyaluronic-acid-vs-filler v3 revision

### P6 — a hand-authored scene must independently replicate the generator's own wrapper-padding math, and nothing says so
`beats_to_composition.py`'s `render_scene()` extends a GENERATED scene's root
wrapper by `d_in + d_out` (its incoming + outgoing transition overlap) and
shifts every beat offset by `+d_in`, so the sub-composition's own internal
timeline lines up with the padded wrapper window. This is documented for
generated scenes. **Nothing documents that a hand-authored scene needs the
identical treatment**, and the engine's own runtime keys a sub-composition's
visibility off its OWN declared duration, not the wrapper's. Confirmed on a
real render: 15 of 15 hand-authored scenes in this project shipped a hard,
silent BLANK FRAME for their own trailing `d_in+d_out` seconds (0.35-1.10s
each) — `hyperframes check`'s layout pass reported 0 errors throughout,
because it has no notion of "does this sub-composition go invisible before
its wrapper's window closes." Confirmed via both the actual rendered MP4
and `hyperframes snapshot` on the live composition (ruling out a
render-capture artifact) — a real timeline defect, not a capture quirk.

**Proposed:** either (a) `beats_to_composition.py` computes and writes each
hand-authored scene's own `d_in`/`d_out` into the beat sheet itself (a
`_transition_geometry` block, machine-derivable, so a hand-authored builder
can read it rather than re-deriving `resolve_transitions()`'s logic), or (b)
this reference file states explicitly, next to the existing `d_in`/`d_out`
documentation: "a hand-authored scene must apply this same padding+shift
itself, or its own tail goes blank for `d_in+d_out` seconds — confirmed on
a real render, not a theoretical risk." This run's fix (in
`videos/hyaluronic-acid-vs-filler/build_actors.py`): compute `D_IN`/`D_OUT`
once per scene from the beat sheet's own declared `transition` field, pad
every declared duration, and shift every `tl.to`/`tl.fromTo` position via one
regex pass over the already-built tween strings (never `gsap.set`, which is
immediate and outside the timeline) — centralized in `scene_shell()` rather
than threaded through every builder.

### P7 — `hyperframes snapshot` does not correctly composite the outgoing scene during an active transition
Extracting a frame at a timestamp inside a live cross-scene transition
window via `hyperframes snapshot` returned a fully blank frame; extracting
the SAME timestamp from the actual rendered MP4 showed the correct,
expected mid-wipe composite (both scenes' content visible, split cleanly
along the reveal boundary). Cost real time this run chasing what looked
like a second composition bug before the render itself proved it wasn't one.
**Proposed:** state this limitation directly wherever `snapshot` is
recommended for verification — a transition-midpoint frame must be pulled
from the rendered file, never from `snapshot`, when the two disagree.

### P8 — `check-safe-area.py` cannot evaluate a full-bleed photographic plate
Its ground-detection method clusters the outer-border-ring luma and flags
anything elsewhere in a reserved zone that doesn't match — correct for a
flat diagram background, meaningless for a full-bleed photo, where every
pixel is legitimate image content with no single "ground" to cluster
against. Confirmed by reading the tool's own detection code, then by direct
pixel inspection of every frame it flagged on a real project's four photo
plates (261 flagged frames, 0 of which showed any actual text/graphic
encroachment — all photo surface). This is the same class of failure the
tool's own docstring already documents once (portrait-canvas-on-landscape):
a gate is only evidence if it was built to evaluate the thing it's looking at.
**Proposed:** `check-safe-area.py` gains either a `--allow-photo-bleed` flag
or an automatic exemption for any scene whose beat-sheet entry carries a
`plate` field, since that field already signals "this scene is a full-bleed
photographic background by design."

### P9 — VO assembly must never scale gaps to hit a preset runtime
Found on THIS project's OWN prior revision: `build_vo.py` computed
`scale = (TARGET - speech) / sum(weights)` and stretched every inter-stem
silence by one factor to land the total on a preset number to the
millisecond. The skill's own master-clock rule says the voiceover's
MEASURED duration governs everything downstream — a gap-scaler quietly
inverts that for the silence, even when the speech itself is untouched.
**Proposed:** state explicitly in the VO-assembly reference that gaps are
fixed, chosen-for-feel real-second values, never solved for a target; a
target band is advisory-only, printed as a tolerance check, and an
out-of-band result is fixed by editing the SCRIPT (cut or add a stem), never
by adjusting gap math.

### P10 — the runbook mux recipe is missing `-movflags +faststart`
Confirmed absent from this project's own two prior shipped deliverables
(`moov` after `mdat` in both) via direct atom-offset inspection.
**Proposed:** add it to the canonical mux command in the runbook.

### P11 — a voice-bus chain should be the DEFAULT for a TTS source, not a discovered fix
This project's raw VO has now measured a ~25-26 dB loudness/peak crest
factor on two separate revisions with two different scripts (-24.3 LUFS /
+0.05 dBFS, then -25.9 LUFS / -0.0 dBFS) — the plain `amix`+`loudnorm`
runbook recipe under-shoots target loudness by several LU on a source shaped
like this, confirmed both times. A voice-bus chain (highpass ~85Hz →
compressor ~-26dB 4:1 makeup ~11 → limiter ~0.60) before the mix fixes it
both times.
**Proposed:** promote the voice-bus chain into the default mux recipe for
any TTS-sourced voiceover, rather than leaving it to be independently
rediscovered per project. Measure the raw VO's LUFS/peak before mixing;
if the crest factor exceeds roughly 15dB, the voice bus is not optional.
