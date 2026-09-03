# Policy-change proposals

Findings from runs that had no rule to apply. The learning loop PROPOSES here;
it never edits `decision-policy.md` directly (SKILL.md §1).


---

## 2026-09-03 · run `kbeauty-label-trap` (long-form 16:9, 257.12s)

### P6 — a scene's own `data-duration` must match `index.html`'s transition-extended window, not the beat sheet's nominal duration
**Found:** `[S6/A-8]`'s own transition-overlap formula (`clip data-duration =
duration + d_in + d_out`) is documented for the WRAPPER div in `index.html`,
but nothing in the skill's composition rules says a sub-composition's OWN
`data-duration` (and internal timeline length) must match that extended
value rather than the beat sheet's nominal per-scene duration. Building it
the "obvious" way — sub-comp duration = beat sheet duration — leaves a dead
zone of `d_in + d_out` seconds where the wrapper keeps the clip mounted past
the point its own internal timeline (and rendered background) considers
itself finished. Confirmed: this rendered as **solid black**, not a frozen
last frame, across the tail windows of every scene followed by a non-cut
transition (8 of this project's 14 scenes) — including the video's own true
final ~0.45 seconds, which is how it was first caught. Neither `hyperframes
check` nor `check-safe-area.py`/`check-static-hold.py` flagged it; only a
manual review of the extracted last-frame PNG did.
**Proposed:** state explicitly, next to `[S6/A-8]`'s overlap formula, that a
sub-composition's own registered duration must equal its wrapper's extended
`data-duration`, not the beat sheet's nominal value — and that `check`
should probably assert this equality directly (comparing each
`data-composition-src` file's own root `data-duration` against the value
computed for its wrapper) rather than leaving it to be caught by luck on a
manually-extracted last frame.

### P7 — `check`'s overlap/occlusion detectors are not clip-path-aware
**Found:** `hyperframes check`'s layout pass flagged `content_overlap` and
`text_occluded` warnings for two scenes' text sitting at the same DOM
coordinates during a `clip-path`-driven wipe transition — a real, correctly-
composited transition where only the unmasked half of each element is
actually visible on any given pixel. The warning text ("Two text blocks
overlap and may render unreadable") reads as a real defect until the actual
extracted frame is checked and shows the wipe compositing correctly.
**Proposed:** either have the layout pass account for `clip-path` when
computing effective visible bounds, or state explicitly in the docs that a
`content_overlap`/`text_occluded` warning landing exactly inside a
transition's `[overlap_start, overlap_start+duration]` window should be
visually verified before being treated as a real defect, rather than fixed
by construction (which would mean avoiding text near a wipe boundary
entirely — a worse outcome than the false positive).

### P8 — `amix`'s default `normalize=1` silently drops mixed-audio loudness below the primary track alone
**Found:** mixing VO + a manually-ducked (`volume=0.12`) music bed with
ffmpeg's `amix` filter at its default settings measured **~6 LU quieter**
than the VO's own standalone loudness (-29.75 vs -23.60 LUFS) — `amix`'s
`normalize=1` default auto-attenuates every input to guard against clipping
on sum, which is redundant (and actively harmful) once one input is already
manually gain-staged relative to the other. Not caught until the final
`loudnorm` measurement looked implausibly quiet for content whose loudest
element (VO) peaks at 0dBFS.
**Proposed:** the skill's audio-mixing guidance (or `hyperframes-audio`)
should say explicitly: pass `normalize=0` to `amix` whenever any input has
already been deliberately gain-staged (a ducked music bed, a sound-effect
mixed under narration) — `amix`'s own clipping protection and a
deliberately-set relative level are working against each other otherwise.

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
