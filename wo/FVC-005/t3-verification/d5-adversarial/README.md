# D5 split + adversarial content, combined

Tests the intersection of two previously-separately-verified features:
the D5 duration-split path (`t3-verification/d5-split/`) and the
overflow-safety fixes found by adversarial-text testing (`ingredient-
overflow/`, `four-emitters/`, `stress7/`). Neither had been proven
*together* — a scene could split correctly with short content, and long
content could render correctly without splitting, but nothing confirmed
that a split sub-scene's *sliced* content still gets the overflow
protection, or that split scenes interact correctly with the frame-zero/
compose-immediately machinery.

## The fixture

Three scenes: `ShRows` (the video's first scene — also exercises
frame-zero + split + adversarial content together), `ShSteps`, and a
closing `ShEndcard`. Both `ShRows` and `ShSteps` use the identical setup
already proven to force a D5 split (`vo_duration_s: 6.0`, three beats at
offsets 0.0/2.0/4.0, derived duration 6.3s against each component's 5.0s
ceiling), but this time with the same genuinely unbreakable 24-character
INCI term (`"Polymethylsilsesquioxane"`) used throughout the earlier
adversarial-text passes, placed in slots that land in *different* split
groups (confirmed with the timing solver directly before compiling: the
long term for both components lands in split group 1, the short terms in
group 2).

## No new bugs found — this is a genuine, informative negative result

Every fix already made independently held up under the combination:

- The D5 split correctly sliced the adversarial rows/steps content per
  group (`compile-report.md` shows `mechanism-1`/`mechanism-2` and
  `steps-1`/`steps-2`, matching the pre-computed split exactly).
- The overflow-safety fixes (`min-width:0` / `overflow-wrap:anywhere`)
  applied identically regardless of whether the slot content reached the
  emitter directly or via `split_slots_for_group`'s slicing — expected,
  since the fix lives in the emitter functions themselves, which have no
  way to distinguish a pre-sliced call from a direct one, but worth
  confirming rather than assuming.
- The frame-zero rule and the D5 split composed correctly together: the
  video's first scene (`mechanism`, split into two) correctly suppressed
  entrance only on its first compiled sub-scene (`mechanism-1`, the
  overall frame zero), while `mechanism-2` — not frame zero, but chip-
  bearing — used its normal entrance.
- The blank-endcard fix held after a *split* scene precedes the endcard,
  not just a normal one: `hyperframes check --at-transitions` returned
  `"ok": true`, and frame-by-frame extraction around the `steps-2-> cta`
  boundary shows no blank frame (range stayed 242-246 throughout,
  compared to the pixel-uniform range-of-1 that would indicate a true
  blank hold — see `d5-split/README.md`'s original finding for what that
  actually looks like).

## One recurrence of the known check-tool artifact — and a refinement

`content_overlap`/`text_occluded` findings appeared again, exactly at
`time: 12.6` — the `steps-2 -> cta` boundary, the only transition in this
composition landing on the endcard. As before: a frame extracted well
inside `steps-2` (t=11.5, `frame-steps2-mid-scene.png`) is clean, and the
actual rendered boundary frame (frame 378 of 432, `frame-boundary-378.png`)
shows the endcard alone, correct, with no trace of the outgoing scene.
None of the three purely-internal split boundaries in this same
composition (`mechanism-1->mechanism-2` at t=4.0, `mechanism-2->steps-1`
at t=6.3, `steps-1->steps-2` at t=10.3) showed any finding at all.

This adds a real data point that refines the earlier conclusion. The
first occurrence (`stress7/`) was an outgoing `ShQuote` scene into
`ShEndcard`; this one is an outgoing `ShSteps` *split sub-scene* into the
same `ShEndcard`. The common factor across both is not the outgoing
scene's component, and not whether it was split — it is that **the
incoming scene is always `ShEndcard`, the only component in every
template that is both `anchor: true` and structurally chip-less**.
`anchor` scenes get an explicit `opacity:1` set on their own `#root` in
CSS (`render_scene`'s `stage_visibility`), unlike every other scene,
which relies purely on the parent mount's `data-start`/`data-duration`
visibility toggle with no CSS override on its own root. This is recorded
as a refinement of the finding in `stress7/README.md`, not a new,
separate bug: still no evidence of any actual defect in rendered pixels,
now confirmed identically across two structurally different transitions
into the same kind of scene.

## Verified

- `hyperframes lint`: `0 errors, 0 warnings` across all 6 files.
- `hyperframes check --samples 40 --at-transitions --json`: `"ok":
  true`. The only findings are the known artifact above, investigated
  and accounted for exactly as before.
- The second static gate, `lint_composition.py`: `0 error(s), 0
  warning(s) across 6 file(s)`.
- Determinism: two independent compiles, `diff -r`, empty.
- A real local render: exactly 14.400s, matching the compiled total.
  Frame-by-frame extraction around the `steps-2 -> cta` boundary
  confirms no blank frame.
- **No regression** on any of the five prior fixtures (`synthetic-t1`,
  the original D5 split, the four-emitter fixture, the `ShIngredient`
  overflow fixture, and the seven-emitter stress test), all re-checked
  after this pass (no compiler code changed this round — this was a
  pure verification pass, and it passed).

## Reproduce

```
python3 <claude-skills>/makemeavideo/scripts/compile_composition.py \
  d5-adversarial.beat-sheet.json /tmp/d5adv-repro \
  --system videos/_system --format 9x16
cd /tmp/d5adv-repro/06-render/9x16
hyperframes check --samples 40 --at-transitions --json
hyperframes render -q draft -o out.mp4
```
