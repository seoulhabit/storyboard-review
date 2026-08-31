# Verification tooling

Not imagery, not a component — a shared script, catalogued for the same
reason a component is: it was built once for a real project and is worth
finding before the next project rebuilds the same check from scratch.

| Item | File | What it is |
|---|---|---|
| [check-safe-area.py](check-safe-area.py) | `check-safe-area.py` | Scans a rendered MP4 for real content inside YouTube Shorts' reserved UI zones, measured on transformed, rendered pixels — catches a class of defect a source-level "are the `--safe-*` tokens consumed" audit structurally cannot see (a `transform: scale()`/`translate()` between a safe-padded box and the canvas moves ink past a compliant padding value without the source ever being wrong). |

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
