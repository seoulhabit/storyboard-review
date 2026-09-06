# D5 split verification

Proves the one path T3's original status file named as unverified: a
scene whose derived duration exceeds its component's ceiling, and the
resulting split.

## What this fixture is

`mechanism-split.beat-sheet.json`: one scene, `ShRows`, `vo_duration_s: 6.0`,
3 beats at offsets `0.0`/`2.0`/`4.0`, 3 rows (`active: 2`). Derived duration
`D_raw = max(6.0 + 0.30, reading_floor(8)) = 6.300s`, against `ShRows`'s
5.0s ceiling (not evidence/compare) — chosen to mirror
`templates/T6.json`'s own reference note about its steps chapter (6.0s
against the same 5.0s cap), which is the exact case `COMPILER.md` names as
"a real, load-bearing case for D5, not hypothetical."

## Two real bugs found by actually running this fixture, both fixed

**Bug 1 — the split algorithm didn't account for the scene's own end.**
First attempt: `compile_composition.py` **died** —
`"scene 'mechanism' group 0: 6.300s still exceeds the 5.0s ceiling after
splitting -- beats too widely spaced to partition further"`. The message
was actively misleading: the three beats span only 4.0s, comfortably under
the 5.0s ceiling — the problem was the scene's *trailing hold* after the
last beat (the difference between the last beat's offset and `D_raw`),
which the original partitioning logic never looked at, since it only
checked each group's own beat-to-beat span. Fixed in
`split_beats_by_ceiling` by passing it `scene_end` (`D_raw`) explicitly and
peeling beats off the back of the final group until what remains actually
fits against that end.

**Bug 2 — splitting timing did nothing to content.** After fixing bug 1,
both compiled sub-scenes rendered the *identical, complete* 3-row list —
confirmed by grepping the compiled HTML, not assumed. `plan_scene` passed
every split group the scene's full, unsliced `slots` dict. Fixed by adding
`split_slots_for_group()`: for components with a natural per-beat list
slot (`ShRows.rows`, `ShSteps.steps` — the only two; everything else
refuses to split rather than guess), each group now renders
`items[lo:hi]` sliced to its own beat-index range, with `ShRows`'s
`active` index relocated to the group's own local index (or `-1` if the
active row landed in a different group).

## Verified, after both fixes

- `hyperframes lint` on the compiled output: `0 errors, 0 warnings`.
- `hyperframes check --samples 40 --at-transitions --json`: `"ok": true`,
  every one of lint/runtime/layout/motion/contrast at `errorCount: 0` —
  `check-9x16.json`, captured verbatim.
- `compile-report.md`: two scenes, `mechanism-1` (0.000–4.000s) and
  `mechanism-2` (4.000–6.300s), both under the ceiling, both traced back
  to parent scene `mechanism`.
- Content split correctly by direct inspection of the compiled HTML:
  `mechanism-1` renders `["Sebum","Down","Barrier","Repaired"]`,
  `mechanism-2` renders `["Pigment","Blocked"]` — exactly rows `[0:2]` and
  `[2:3]`.
- A real local render: exactly 6.300s. `frame-group1.png` (t=3.0s, inside
  the first sub-scene — Sebum/Down and Barrier/Repaired, both in ink, no
  clay, since the active row isn't in this group) and `frame-group2.png`
  (t=5.5s, inside the second — Pigment/Blocked, correctly in clay, the
  relocated active row) were extracted and visually confirmed.

## Reproduce

```
python3 <claude-skills>/makemeavideo/scripts/compile_composition.py \
  mechanism-split.beat-sheet.json /tmp/d5-repro \
  --system videos/_system --format 9x16
cd /tmp/d5-repro/06-render/9x16
hyperframes check --samples 40 --at-transitions --json
hyperframes render -q draft -o out.mp4
```
