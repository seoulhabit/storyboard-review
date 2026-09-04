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

---

## From `snail-mucin-medical-secret` v2.1 retrofit (2026-09-03, render mode)

### P6 — `[S6/A-8]` states the target state but not the retiming procedure
Converting a crossfade boundary to a cut is not just deleting the tween: the
clip windows overlap by the transition duration, so the scenes must also be made
**contiguous**, and the safe pre-check is each scene's **last GSAP cue against
its shortened window**. Neither is written down. On this run the five boundaries
needed `data-duration` retimed (14.02→13.52 etc., each landing on its own VO
length) and every scene's last cue verified first.
**Proposed:** add both as a sub-clause of A-8.

### P7 — `[S7/R-2]` assumes there is room to move content out of the reserved zones
"Fix the scene(s) named above" understates the work when the reserved zone is
already occupied by design. Here the caption band could not slide up until
**six** lower-third elements across five scenes were shifted first — a coupled
relayout, not a per-scene fix.
**Proposed:** name the coupling, and say that the caption band's position is a
project-wide constraint the scenes must be laid out around, not an overlay.

### P8 — `[S6/A-6]` does not say which box component type resolves against
A `cqw`/`cqh` font size inside a registry component resolves against its
**mount**, not the canvas. `grid-card-assemble` in a 756×750 mount resolved to
16.5px/19.5px and `split-tilt-cards` in a 756×740 mount to 15.9px/16.6px, while
every scene file passed the same audit cleanly. Worse, this run's own safe-area
narrowing (900→756px) pushed those component sizes **further under** the floor —
a rule fix that silently regressed another rule.
**Proposed:** A-6 must require resolving component type per mount, and flag that
changing a mount's width is a type-floor change.

### P9 — a component may overwrite the custom properties it documents as inputs
`grid-card-assemble` computes `--gca-font` / `--gca-body-font` at runtime and
`setProperty`s them onto its own `#root`, so a host-level override in the mount's
inline style does nothing. The first fix attempt here looked correct in source,
passed `check`, and changed nothing on screen; it was caught only on the extracted
frame, on the second pass.
**Proposed:** a line in A-6 or `hyperframes-engine.md` — a component-level style
override is verified on pixels, never assumed from source.

### P10 — `hyperframes snapshot` does not apply a mount's `data-variable-values`
`snapshot --at` rendered `grid-card-assemble` with its **default** items and
layout rather than the mount's, so it cannot stand in for a render when verifying
anything variable-driven. It is still useful for static layout and contrast.
**Proposed:** note the limitation wherever the runbook suggests a cheap
verification path. Observed on 0.8.17, not root-caused.

### P11 — a copied QC script's caption-band constant is load-bearing and ships wrong
`catalog/tooling/check-static-hold.py` ships `CAPTION_BAND_EXCLUDE = False` with
the comment *"this project has NO burned-in captions"* — inherited from a
different project. This project does have them, and with the band included the
constantly-changing karaoke captions keep the whole-frame diff alive and **mask a
frozen hero region**. Re-deriving it (band 1300–1520) is what surfaced two of the
three static holds. The script's own docstring already warns about this class of
bug; the shipped default still contradicts it.
**Proposed:** make the band a CLI argument with no default, so it cannot be
inherited silently.
