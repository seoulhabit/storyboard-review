# T5 — Validators and lint hardening — DONE

Commit `70ade98` pushed to `github.com/seoulhabit/claude-skills`. Built via three parallel background agents (Workflow `wf_04a459e8-bcb`, ~483K tokens, 115 tool calls), each writing one script plus its own fixtures and required to actually run its script against them before reporting back — then independently re-verified by me before committing (see below), not taken on trust.

## Attestation — `tests/run.sh`, run myself after extending it

The agents delivered `validate_beat_sheet.py`, `lint_composition.py`, and a hardened `extract_frames.sh` — the `extract_frames.sh` agent had also already written a `tests/run.sh`, but it only covered its own script. I extended it to also exercise `validate_beat_sheet.py`'s and `lint_composition.py`'s fixtures (the Accept criterion wants one unified runner across all three validators), then ran the whole thing myself:

```
== validate_beat_sheet.py ==
PASS: pass.json passes (exit 0)
PASS: fail_overlap.json rejected (exit 1), finding names 'overlap'
PASS: fail_canvas.json rejected (exit 1), finding names 'canvas'
PASS: fail_chapters_on_short.json rejected (exit 1), finding names 'chapters'

== lint_composition.py ==
PASS: clean.html lints clean (exit 0)
PASS: fail_banned_raf.html rejected (exit 1), finding names 'requestAnimationFrame'
PASS: fail_lazy_image.html rejected (exit 1), finding names 'decoding'

== extract_frames.sh ==
[7 cases, all PASS — variance flag, no false positive on real motion, legacy
invocation, scenes mode end-to-end, unsafe-id rejection, malformed-JSON
rejection, DUR-fallback WARN]

==========================================
  15 passed, 0 failed
==========================================
EXIT CODE: 0
```

**Independent spot-check beyond the agents' own claims** (the highest-stakes one, since a previous version of `lint_composition.py` was deleted for exactly this failure mode): ran the new linter against the actual shipped `assets/composition-skeleton.html` and `scene-skeleton.html` myself — `0 error(s), 0 warning(s)` — and confirmed the `clean.html` fixture genuinely contains a relative image path (`assets/plates/hero.png`) and a Google Fonts `<link>`, neither flagged. Also read the scene-id sanitization regex in `extract_frames.sh` directly (`^[A-Za-z0-9_-]+$`, properly anchored both ends) rather than trusting the agent's description of it.

## What each script does, briefly

- **`validate_beat_sheet.py`** — 8 checks per the WO spec, sourced from the actual schema and decision-policy.md rules (A-4 canvas, C-1 chapters, C-3 end-scene, the S-6 spine-split table), not guessed. Collects every finding before exiting 1.
- **`lint_composition.py`** — full rebuild, not a resurrection. Verified not to repeat the three false checks that got the old one deleted (documented at decision-policy.md's R-1 note): `window.seek`, project-relative image paths, named Google Fonts links. Implements the WO's requested checks (per-image findings, `decoding="sync"`, remote URLs, fallback backgrounds, self-running-animation detection with comments/strings properly masked out — not naive regex) plus three checks `hyperframes check` genuinely doesn't cover: a `*.motion.json` sidecar silently ignored when placed beside a non-root file, an inherited `defaults:{ease}` hiding real ease usage from a grep, and a best-effort `keepsMoving` root-scoping check (honestly scoped to the one JSON vocabulary the generator actually emits, not claimed as general).
- **`extract_frames.sh`** — three real hardening items, each verified against actual generated media rather than assumed: scene-id sanitization before any path gets constructed (a new `scenes` mode extracting per-scene settle and transition-midpoint frames); a real bug found and fixed in the old duration-fallback logic (its own ffprobe result was piped to `/dev/null` and never used — confirmed on a real `.mkv` fixture lacking video-stream duration fields); and the mean-brightness-only "near-uniform" heuristic replaced with an actual variance estimate, after measuring on generated frames that the WO's suggested `YRMS²−YAVG²` metric isn't exposed by this machine's ffmpeg build and that the alternative `YHIGH−YLOW` metric false-negatives on realistic sparse-content frames.

## Judgment call

Extended `tests/run.sh` beyond what any single agent produced, since the Accept criterion needs one runner covering all three validators and the agents correctly avoided touching each other's files. No other changes to the agents' work were needed.
