# Verification tooling

Not imagery, not a component — a shared script, catalogued for the same
reason a component is: it was built once for a real project and is worth
finding before the next project rebuilds the same check from scratch.

| Item | File | What it is |
|---|---|---|
| [check-safe-area.py](check-safe-area.py) | `check-safe-area.py` | Scans a rendered MP4 for real content inside YouTube Shorts' reserved UI zones, measured on transformed, rendered pixels — catches a class of defect a source-level "are the `--safe-*` tokens consumed" audit structurally cannot see (a `transform: scale()`/`translate()` between a safe-padded box and the canvas moves ink past a compliant padding value without the source ever being wrong). |
| [check-static-hold.py](check-static-hold.py) | `check-static-hold.py` | Scans a rendered MP4 for a static-hold two different ways: a whole-frame PSNR check (the original, project-portable form already in use across this channel), plus a region-aware check that grids the safe content box and flags a cell that goes from carrying real content to essentially empty and stays there — catching a scene's own HERO element sitting dead while unrelated motion elsewhere in the same frame keeps the whole-frame check clean. Advisory (exits 0), like the other `check-*.py` scripts here except `check-safe-area.py`. |

**Provenance.** Built for `videos/peeling-not-progress`'s round-6 safe-area
fix (2026-08-31) — an external QC report flagged content near the Shorts UI
overlap, and a pixel-level audit found three scenes silently overshooting
the real line via exactly this mechanism (a scene-wide Ken Burns wrapper) and
a fourth via a related one (an entrance transform's own transient). See that
project's `frame.md` "Post-render review fixes" round 6 for the full measured
root cause, and `.claude/skills/faceless-video-craft/SKILL.md`'s
*Verification loop* → "Safe-area intrusion scan" and pre-render gate item 7b
for the rule this script exists to enforce.

**Field contract.** `python3 check-safe-area.py <project_root> [render_path]
--safe-top <px> --safe-bottom <px> --safe-right <px> [--safe-left <px>]` —
zone sizes are CLI flags, not hardcoded, so this is drop-in across projects;
pass the calling project's own real reserved-zone pixel values (its tokens,
or the skill's 192/384/162 defaults if the project has no deviation on
record). Samples the render at 4fps, builds an antialiasing-tolerant ink
mask per frame, and exits non-zero if any sampled frame has real content
inside a reserved zone — a **hard gate**, unlike this repo's other
`check-*.py` scripts, which are advisory (always exit 0). Wire it into a
project's own `package.json` `postrender` script alongside
`check-blank-frames.py` / `check-static-hold.py`.

**Status: validated reference, not yet wired into every project.** Confirmed
working against a real render (`peeling-not-progress`'s round-6 mastered
file, before and after the fix) but copied per-project rather than imported —
matches this repo's existing convention for `check-blank-frames.py` /
`check-static-hold.py`, which are also per-project copies, not a shared
module. Copy this file into a new project's `scripts/` directory and wire it
into `postrender` rather than re-authoring an equivalent script from scratch.

---

## check-static-hold.py

**Provenance.** The whole-frame PSNR half of this script already existed
per-project across the channel (`peeling-not-progress`, `mugwort-healing-
herb`, others) — each copy carrying a `CAPTION_BAND_EXCLUDE` flag and a
caption-band crop hand-derived for ITS OWN project. `peeling-not-progress`'s
own copy documented, in its own docstring, a real defect it had already
caused once: inheriting a sibling project's caption-band crop verbatim,
silently cutting real content out of every diff it ran. That documented
warning did not stop the same defect from recurring one project later
(`peeling-question-open`, 2026-09-01): its copy of this script still carried
`mugwort-healing-herb`'s crop and `True` flag despite `peeling-question-open`
having **no burned-in captions at all** — the crop was masking scene 5's own
"THE BOUNDARY" kicker from every scan. Caught only because an external QC
report's one real (if misdiagnosed) finding prompted a full pixel-level
re-verification, not because this script itself flagged anything wrong with
its own configuration — a comment warning about a trap is not the same as
the tool enforcing against it.

The same verification round found a SECOND, independent gap the whole-frame
check cannot see even with a correct caption-band setting: a scene's own
dominant hero element (a `.glass-panel` in this case) went fully empty for
~1.1s — text had exited, a closing lockup hadn't arrived yet — while a
different on-screen element (a closing headline couplet) kept the whole-
frame PSNR comparison alive throughout. The region-aware half of this script
was added specifically to close that gap: it grids the safe content box and
flags a cell that goes from a real content peak to essentially empty and
stays there past a (tighter) per-region ceiling, scoped to one scene at a
time using the project's own `index.html` scene list so a hard cut between
scenes never misreads as "content vanished."

**Known limitations, confirmed, not hypothetical — two classes.** The
region-aware check's "is there real content in this cell" signal is
spatial-variance-based (pixels differing from a per-cell background
estimate), which can misfire two ways, both confirmed on this same project:

1. A textured or gradient plate that isn't real UI content — scene 1's
   frosted-glass card, whose subtle embossed watermark produced a false
   content-then-empty read even after threshold tuning.
2. A weaker SECOND content transition in the same scene/cell reading as
   still-empty relative to an earlier, stronger beat in that same cell —
   confirmed AFTER fixing the source defect this script was built to catch
   (06-open.html's panel-empty gap): the per-scene baseline sits between the
   word-grid's strong peak and the SeoulHabit lockup's weaker one (in the
   specific column the glyph mostly doesn't reach), so the fix's own arrival
   still read as "empty." Direct frame extraction at the flagged timestamps
   (this skill's own mandated verification method) confirmed the true empty
   window shrank from 1.30s to 0.40s — the fix is real; the tool's own
   continued flag on it is the false positive, not the other way around.

Both are why the check stays advisory (exits 0) and prints a standing
reminder to confirm each candidate against the actual extracted frame, not
trust the cell coordinates alone — including trusting THIS script's own
output, which is exactly the "verify by pixels" discipline the skill asks of
an external QC report applied reflexively to this script's own claims too.
A future improvement worth trying before re-deriving this from scratch: a
per-cell threshold scaled to that cell's own observed ink range (not one
fixed delta shared across every content state in a scene) — not yet
implemented here.

**Field contract.** No CLI flags (unlike `check-safe-area.py`) — the
per-project constants at the top of the file (`CAPTION_BAND_EXCLUDE`,
`SAFE_TOP`/`SAFE_BOTTOM`/`SAFE_RIGHT`/`SAFE_LEFT`, the grid size, all four
threshold constants) are meant to be hand-re-derived per project, matching
this repo's existing per-project-copy convention for this file (see the
`peeling-not-progress` → `mugwort-healing-herb` → `peeling-question-open`
caption-band history above for exactly why copying without re-deriving is
the recurring failure mode this entry exists to break). Reads scene
boundaries from the calling project's own `index.html`
(`data-start`/`data-duration` on each `.scene[data-composition-src]`); falls
back to treating the whole render as one scene if that file or pattern isn't
found. `python3 check-static-hold.py <project_root> [render_path]`.
