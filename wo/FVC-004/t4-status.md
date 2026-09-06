# T4 — Runbook + scripts + front door — DONE (scripts + tests); front door (one command, sub-commands) not built this session
Commit `claude-skills/fvc-004/makemeavideo` branch, `scripts/qa_render.py`, `scripts/beats_to_build_spec.py`, `scripts/provider_call.py`, `scripts/_yaml_lite.py`, `requirements.txt`, `assets/environment.template.md`, `tests/`, `references/runbook.md` (two fixes).

## What shipped

Three scripts the WO's own §7 table marked "not written": `qa_render.py`,
`beats_to_build_spec.py`, `provider_call.py` (`validate_request.py` already
shipped in 0.1.0). Plus a shared parser module neither the WO nor the 0.1.0
scaffold names (`_yaml_lite.py`), a dependency manifest, the environment
probe template, and a real test suite — 20/20 green with `qa_render.py`'s
dependencies installed, 15/15 (with an honest `SKIP`) without them.

**Every claim below is backed by a command actually run this session, not
a description of intended behavior** — see the "Verified, not assumed"
section at the end for the transcript.

### `scripts/qa_render.py` (new, ~870 lines)

Gates a delivered MP4 against `H-2`..`H-4`, produces `K-4`'s mechanical
claim-to-frame checks, writes one `qa.json` envelope. Reuses, rather than
re-derives, four `catalog/tooling/` scripts:

| `H-*` clause | Mechanism |
|---|---|
| `H-4` canvas | `ffprobe`, asserted before any other gate runs |
| `H-4` safe-area | **shelled out** to `check-safe-area.py` — already MP4-native, a hard gate, nothing to patch |
| `H-4` static-hold | **imported in-process** (`importlib.util.spec_from_file_location`, the same hyphenated-filename technique `check-cadence.py` already uses on this file) — `scene_boundaries()` is monkeypatched to read the beat sheet, since there is no `index.html` on a HeyGen render, and `apply_landscape_profile()` is called for long-form so `CANVAS_W/H` and the safe-zone constants change together, not independently |
| `H-4` contrast / type floor | **new**: `textish_regions()`, a Sobel-gradient + morphology + connected-components heuristic, then `check-contrast-pixels.py`'s own audited Otsu-split/WCAG math reused verbatim on each detected box |
| `H-4` loudness | `ffmpeg -af ebur128=peak=true`, the `Summary:` block parsed (not the per-frame lines, which also match `I:`/`Peak:` and would return a running value, not the final one) |
| `H-3` faceless | **new**: `opencv-python-headless`, two Haar cascades (frontal + profile — a faceless gate that only catches frontal faces isn't one), plus a dense 2fps re-sample of the whole file, because `extract_frames.sh`'s frame0/settle/transition-mid/last inventory can miss a face appearing mid-scene |
| `K-4` (mechanical third only) | claim id → scene → frame map; the concurrent-flag/hedge/prohibition checks are `requires-reading`, routed to the `design-critique` gate, per policy.md's own honest split |

Every gate reports `pass` / `fail` / `unmeasurable` — never a silent pass
when nothing was actually measured, which several of the underlying
`catalog/tooling/` scripts do by default (`check-blank-frames.py` and
`check-static-hold.py`'s whole-render checks are advisory-exit-0 always; a
missing numpy/PIL makes `check-safe-area.py` exit 0 too). `qa_render.py`
converts these into real verdicts by reading the actual output, not the
exit code.

### `scripts/beats_to_build_spec.py` (new, ~250 lines)

Beat sheet + `01-story-brief.md` §Sourcing + `channel.yaml` → `05-build-spec.md`.
Documents its own interpretation in its docstring, since no real HeyGen
build spec exists yet to check against (T0 hasn't run): scene VISUAL = the
scene's beats' `intent` fields (the schema itself calls `intent` "a visual
state, not a sentence" — the closest thing to a visual cue a beat carries);
scene VO = the beats' `text` fields, since `[S4/V-1]` already treats
captions as "the script, sentence-chunked"; `[K-1 #n]` markers are attached
to a scene by substring-matching the claim table's "On-screen" column
against that scene's joined text, and an unmatched claim id is reported on
stderr, never silently dropped. `C-3a`'s brand end-card is always appended.

### `scripts/provider_call.py` (new, ~200 lines) and `scripts/_yaml_lite.py` (new, ~140 lines)

`provider_call.py` ports 2.1.0's ledger-line shape and adds `heygen` /
`vidiq` / `gemini` / `log` subcommands, each pricing against `providers.yaml`
and appending one line to `cost-log.jsonl`. It does not itself call any MCP
tool — an agent session does that; this script is the bookkeeping the agent
hands its numbers to.

`_yaml_lite.py` is a small local module (not a package dependency) holding
the minimal YAML-subset parser both scripts need, extracted after writing it
inline once and finding three real bugs in it (see below) — duplicating a
parser with those bugs into a second script would have shipped them twice.

### `requirements.txt` (new) and `assets/environment.template.md` (rewritten)

`qa_render.py` is this skill's one script that is not stdlib-only, because
it measures pixels — documented as a deliberate exception, not a quiet
departure from the convention. `environment.template.md` gained a "QA
capability probe" section (detector + `catalog/tooling/` resolution) and the
version/drift-check block the 0.1.0 file was missing.

### `references/runbook.md` — two fixes found by running it, not reading it

1. **S0.0** gained the QA capability probe (detector + tooling-dir
   resolution), so a HeyGen session is never built only to discover at S7
   that the gate can't run.
2. **S7 step 2 was factually wrong.** It named one call —
   `extract_frames.sh scenes <mp4> <beat-sheet> <out>` — as producing "frame
   0, per-scene settle frames, last frame." Running it against a real
   fixture showed `scenes` mode only ever writes `scene-<id>-settle.png` /
   `scene-<id>-transition-mid.png`; frame 0 and the last frame come from
   `basic` mode only. `qa_render.py`'s `H-2` gate needs `frame-000-hook.png`
   and would have reported `unmeasurable` on every real run under the old
   instruction. Fixed to call both modes; also added the `--brief`/`--timing`
   arguments `qa_render.py` actually needs (the runbook previously gave it
   three positional args and assigned it K-4 duty with no way to reach the
   claim table or the H-6 timing).

### `tests/run.sh` + fixtures (new)

House pattern (`mktemp -d` + trap, pass/fail tally, assertions on finding
*text* not just exit code), fixture media generated by `ffmpeg` at test
time rather than committed, per this repo's own convention
(`faceless-video-craft/tests/fixtures/extract_frames/generate.sh`).

- `validate_request` — pass + 3 failure fixtures (bad slug, bad video_id,
  bad format).
- `validate_beat_sheet` — a hand-built, fully compliant 6-section long-form
  fixture (`pass.json`) plus `fail_overlap`, `fail_canvas`,
  `fail_chapters_on_short`, and a new `fail_cadence` fixture exercising the
  cadence rule added to `validate_beat_sheet.py` this session (see below).
- `beats_to_build_spec` — a golden-file comparison plus a `BLOCKER-TOKENS`
  negative control.
- `provider_call` — one assertion per subcommand, including the budget-cap
  warning path.
- `qa_render` — `generate.sh` builds four MP4s via `ffmpeg` lavfi sources
  (`clean`, `static`, `blank`, `loud`); each is asserted against the *one*
  gate it was built to exercise (see "What this suite does NOT cover" below
  for why not "everything passes on `clean`").

## Three real bugs this session's testing found and fixed — none would have surfaced from reading the code

1. **`Path | None` union-type syntax needs Python 3.10+; this environment's
   `python3` is 3.9.4.** `qa_render.py` crashed on its own `--help` on the
   first run. Fixed with `from __future__ import annotations`.
2. **`beats_to_build_spec.py`'s `BLOCKER-TOKENS` check was dead code.** An
   earlier version computed `colors = tokens.get("colors") or
   TEMPLATE_DEFAULT_TOKENS["colors"]` *before* the blocker check, so an
   empty `channel.yaml` never actually reached the check — it silently got
   a script-invented neutral default instead, contradicting `H-1`'s own
   rule ("a colour is a one-time channel pick, not a per-run guess").
   Caught by testing against a `channel.yaml` with empty tokens.
3. **The minimal YAML parser's naive comment-stripper truncated hex
   colours.** `colors: ["#0B1F3A", ...]` was read as `["` because
   `line.split("#", 1)[0]` treats any `#` as a comment start, including one
   inside a quoted string. Found because the generated build spec's STYLE
   line printed garbage instead of three hex codes. Fixed with a
   quote-aware `strip_comment()`. Two more parser gaps found in the same
   pass: flow-style lists (`["a", "b"]`) and block-style lists of mappings
   (`providers.yaml`'s `roles.<role>` shape) were not handled at all —
   added both, then verified the parser against the **real**
   `channel.template.yaml` and `providers.yaml`, not just synthetic test
   input.

## One real design correction this session's testing found

**`policy.md`'s T3 text conflated two different thresholds that happen to
share a similar shape.** `C-2`'s authoring-time beat-gap cap (long 2.0s /
short 1.5s, checked on the *beat sheet* before a render exists) is not the
same number as `catalog/tooling/check-static-hold.py`'s own post-render
whole-frame cadence ceiling (2.5s portrait / 10.0s landscape, via
`apply_landscape_profile()`, calibrated against real renders to avoid false
positives on legitimate slow holds). An earlier draft of `H-4` and `C-2`'s
text said the two numbers were the same value stated once; they are not.
Caught only by actually running `check-static-hold.py` in-process and
reading its module-level `CADENCE_CEILING_S`. **`policy.md`'s H-4 and C-2
text now state this correctly** — `H-4.static-hold` reports the tool's own
`cadence_ceiling_s` in its `measured` block rather than a hardcoded number,
and `C-2`'s docstring in `validate_beat_sheet.py` explains the distinction
so a future reader doesn't re-conflate them.

## A real finding about the WO's own reference artifact, reported not fixed

`outputs/2026-09-01-how-to-repair-skin-barrier/03-beat-sheet.json` — the
exact file WO-FVC-004 §0.2/T0 step 3 points the spike at — **fails
`validate_beat_sheet.py`'s carried section-order rule.** That rule (carried
verbatim from `faceless-video-craft` 2.1.0, not touched by T3 or T4) requires
all six spine sections (`hook, misconception, mechanism, proof, application,
recap`) in that exact order; this real, previously-shipped short-form video
has four (`hook, misconception, mechanism, application`) — plausible under
`S-5`'s own "reduce to a short on the grounded sections" rule, but not what
the validator, as written, accepts. **Not silently loosened.** This is a
policy-affecting question (does the section-order rule need a short-form
exception, or was this artifact built before the rule existed) and belongs
with whoever runs T0, not patched here as a side effect of writing a test
fixture.

## Judgment calls made

- **`H-4.contrast` and `H-4.type-floor` are advisory in `qa_render.py`'s own
  verdict aggregation**, not blocking, despite `policy.md`'s `H-4` listing
  them as "all must pass." Reasoning: `textish_regions()` has no composition
  source to consult, and testing it against a real project render
  (`videos/kbeauty-label-trap/06-render/final.mp4`) measured a very high
  false-positive rate even after tightening the filter (108 → 98 "text"
  regions on a 20s clip, most of them full-width design panels, not text
  lines) — no HeyGen render corpus exists yet to calibrate against (T0
  hasn't run). Both gates still measure and report every finding loudly;
  they just don't gate the overall pass/fail verdict until validated. This
  is stated in the script's own comments and in `qa_render.py`'s docstring,
  not silently done. **This is a scope reduction from `policy.md`'s literal
  text and should be revisited once T0 produces real HeyGen renders to
  calibrate against** — it may turn out the heuristic needs more tuning, or
  that these two clauses stay advisory permanently and a human
  (`design-critique`) is the real gate for them.
- **`opencv-python-headless==4.10.0.84`, pinned exactly**, not "any recent
  version." The latest release as of this session (5.0.0.93) does not ship
  the Haar cascade XML files in the wheel at all — `cv2.data.haarcascades`
  resolves to an empty directory. A naive `pip install opencv-python-headless`
  would make `H-3`, the one non-skippable gate, silently unmeasurable. This
  is why `requirements.txt` pins the version and the S0.0 probe checks for
  the cascade files specifically, not just that `cv2` imports.
- **Cadence enforcement (`C-2`) landed in `validate_beat_sheet.py`, not a
  new script.** `policy.md`'s T3 text names this script as the enforcement
  point (replacing the retired `beats_to_composition.py`); it already runs
  at S5 before the build spec is generated, already validates other
  timing rules, and adding a ninth check there keeps the property `C-2`
  cares about (the defect never reaches a render) without inventing a new
  gate.

## Not done (correctly out of scope for T4, or blocked)

- **The front door itself** — `SKILL.md` already specifies `/makemeavideo`
  with sub-commands (`improve`/`build`/`package`/`readout`) as a design, but
  no slash-command wiring was built this session; that is a claude.ai / CLI
  registration step, not a skill-file change, and the WO's own §6 Gate 1
  criterion ("slash list on both machines") needs the second machine this
  session doesn't have.
- **`evals/`** — the WO's T9 scope, gated on the 1.0.0 release, itself gated
  on T0.
- Anything requiring the HeyGen MCP connection — T0, T1's HeyGen probe, T5–T8.

## Verified, not assumed

```
$ bash tests/run.sh                     (system python3, no cv2)
== 15 passed, 0 failed ==
  SKIP: numpy/Pillow/cv2 not all importable in this interpreter

$ PATH=<repo>/.venv/bin:$PATH bash tests/run.sh   (venv python, has numpy+Pillow+cv2 4.10.0.84)
== 20 passed, 0 failed ==
  pass: blank.mp4 fails H-2 (frame zero blank)
  pass: static.mp4 fails H-4.static-hold
  pass: loud.mp4 fails H-4.loudness (true peak)
  pass: clean.mp4 passes H-4.canvas (correctly-dimensioned fixture)
  pass: clean.mp4 passes H-4.duration (correct target)
```

`qa_render.py` was also run against a real, previously-shipped project
render (`videos/kbeauty-label-trap/06-render/final.mp4`, 1920×1080, 257s) —
not just synthetic fixtures — with a hand-built beat sheet standing in for
the real one (that project predates this skill and has no `03-beat-sheet.json`
in this shape). All nine gates produced real, inspectable measurements;
this is where the contrast/type-floor false-positive rate and the H-3 face
count (19 detections, plausibly some real photography in a k-beauty video,
not necessarily all false positives — not adjudicated here) were measured.

`beats_to_build_spec.py` was run against the real
`outputs/2026-09-01-how-to-repair-skin-barrier/` artifacts (the actual
`03-beat-sheet.json` and `01-story-brief.md`, not fixtures) and produced a
real 8-scene build spec with all 8 non-CUT `[K-1]` claims correctly matched
to their scenes.

**Not verified, and I'm not claiming otherwise:** no real HeyGen MCP
connection exists on this machine, so nothing here has been exercised
against an actual HeyGen-delivered MP4 — every fixture and every real-render
test used pre-existing HyperFrames-era renders or synthetic media.
`qa_render.py`'s face/contrast/type-floor heuristics are therefore unvalidated
against the artifact they will actually have to gate; T0 is where that
validation happens. The front door's sub-command dispatch was not built or
tested. Two-machine parity (WO ruling 9) is unverified — this session ran on
one machine only.
