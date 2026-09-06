# T4 — Audio and render harness — DONE, plus R-6 (safe-area widened, T3 finding #20 closed)

Commits: claude-skills branch `wo-fvc-005-t4` off `fvc-005/makemeavideo`
(the audio/render harness + `compile_composition.py`'s R-6 constants);
Story Board branch `session/wo-fvc-005-t4` (R-6 tokens + this status +
verification evidence).

## R-6 (ruling, confirmed by Kim this session): widen safe-area to 15%/10%

Closes T3 finding #20 (`t3-status.md`, `t3-verification/repo-gates/README.md`):
`check-safe-area.py` failed BOTH canvases against the design system's
extracted safe-margin tokens (9:16 right rail 10% vs. the platform's real
15%; 16:9 bottom zone 8% vs. the platform's real 10%).

Changed, minimally, to the two specific values the gate actually measured
as too narrow — nothing else:
- `videos/_system/tokens/spacing.css`: `:root` (9:16) `--safe-x: 10% -> 15%`;
  `[data-canvas="16x9"]` `--safe-bottom: 8% -> 10%`.
- `videos/_system/MANIFEST.json`: re-hashed `tokens/spacing.css`, plus a new
  `amendments[]` entry recording the ruling, the exact change, and why —
  the manifest carries no version string (it IS the version anchor, sec
  8.6(a)), so a hand-edited token file must re-hash or `compile_composition.py`'s
  own drift check (`check_manifest()`) dies on it, as designed.
- `compile_composition.py`'s `FORMATS` dict: the two mirrored Python
  literals (`safe_x` for 9:16, `safe_bottom` for 16:9) updated to match —
  these are informational only (only `w`/`h` are read from `FORMATS` at
  runtime; actual layout is driven by the loaded token CSS), but the
  file's own header comment requires them kept in sync by hand.

**Verified, not assumed**: recompiled the T3 synthetic-t1-fixture, rendered
both canvases, re-ran `check-safe-area.py` exactly as T3's own repro block
specifies. Both canvases now report `no findings` — see
`t4-verification/README.md`.

## T4 — audio + render harness

Shipped in `claude-skills/makemeavideo/scripts/`:

- **`mix_audio.py`** — places each scene's VO at that scene's own beat
  start (the same cumulative timeline `compile_composition.py`'s
  `derive_duration()` computes — imported, not re-derived), lays a music
  bed underneath, normalises to H-4's band (-14 LUFS ±2, true peak ≤ -1
  dBTP) via ffmpeg's `loudnorm`, and writes one `audio.wav` plus a
  `*.mix-report.json`. A scene with no `vo_file` is a hard stop unless
  `--allow-placeholder-vo` substitutes a slate tone — named as a
  substitute in the report, never presented as real narration (T1-FINDINGS'
  own discipline for F2's local substitute). `--patch-beat-sheet` wires
  the beat sheet's `audio.src` so T3's existing `compile_composition.py`
  (unmodified) picks the file up automatically — no duplicate asset-copy
  logic added.
- **`render_local.sh <slug> <format>`** — check -> render -> extract
  frames -> `qa_render.py`, against an already-compiled
  `$MMAV_PROJECT_ROOT/<slug>/06-render/<format>/` (default
  `MMAV_PROJECT_ROOT=videos`, override-able for a scratch run). Reuses
  `extract_frames.sh` (`basic` mode) and `qa_render.py` verbatim per the
  WO's own reuse instruction (sec 8.7) rather than re-authoring the QA
  layer.
- **`render_cloud.sh <slug>`** — the only path that can ever request a
  HeyGen cloud render. Checks R-1's gate (`request.yaml render: cloud` AND
  the channel's credit cap, per sec 8.3's correction to a credit-denominated
  cap, not a free-tier render count) and refuses loudly if either is
  unmet. Even on a passed gate it does not call HeyGen itself — this
  environment has no authorized connector (T1-FINDINGS F2-F4,
  BLOCKED-CONNECTOR) and a cloud render spends real, capped, non-refundable
  credits, which this WO's own "no auto-retry past a cap" discipline treats
  with the same care as an irreversible spend. It prints the gate result
  and the next manual step instead.
- **`_qa_adapter.py`** (new, small, internal helper — same `_`-prefixed
  convention as `_yaml_lite.py`) — anywhere `qa_render.py`/`extract_frames.sh`
  need `scene.start`/`scene.duration` (the OLD faceless-video-craft
  schema), this replays `compile_composition.py`'s own `derive_duration()`
  over the beat sheet's scenes in order to produce a QA-facing annotated
  copy. Needed because T3's compiler computes timing internally and never
  writes it back onto the beat sheet — a real, pre-existing schema gap
  between T2/T3's compiler and WO-FVC-004's QA tooling (T3 status named
  the mirror-image of this gap: "neither of the two real beat sheets in
  this repo can be compiled yet").

## Two real bugs found while proving the harness against a real render, fixed before reporting anything clean

1. **`mix_audio.py` measured its own mix wrong.** Its loudness check matched
   the FIRST `I: <n> LUFS` line in ffmpeg's ebur128 stderr — a running,
   unconverged reading printed every ~100ms during the scan (an early one
   read -70 LUFS against a file that actually measured -14.0 LUFS
   overall). Fixed to scope the regex to the final `Summary:` block first,
   matching `qa_render.py`'s own `gate_h4_loudness` exactly, so the two
   never disagree on method.
2. **`_qa_adapter.py` passed a stale duration through.** The beat sheet's
   own top-level `vo_duration_s` (12.0s, the raw per-scene narration sum)
   was left untouched by a `setdefault` that never fires when the field is
   already present. `qa_render.py`'s `H-4.duration` gate reads that field
   as the video's total intended length; in the new schema it is only the
   narration sum, and the compiler's own timing rule (tail padding /
   reading floor) always makes the real render longer (14.6s here). Fixed
   to always overwrite it with the derived total.

## One real, external finding — not a defect in either new script

The mixed `audio.wav` measured -14.0 LUFS / -8.0 dBTP on disk. The SAME
file, after `hyperframes render`'s Chrome audio-capture + AAC mux,
measured -11.0 LUFS in the delivered MP4 — confirmed NOT an AAC-encoding
artifact (encoding the identical WAV to AAC with plain `ffmpeg` measures
-14.0 LUFS, unchanged). HyperFrames' own render pipeline adds roughly
+3dB somewhere between the `<audio>` element and the muxed output.
Compensated for this verification run via `mix_audio.py --target-lufs
-17` (delivered result then measured -14.0 LUFS / -10.9 dBTP, inside
H-4's band) — named here as a render-engine characteristic worth its own
investigation, not baked into the script as a silent default. A real
production run should re-measure this on its own render machine before
trusting -14 as the right pre-mux number.

## Accept check

**Verified**: `hyperframes check` on the compiled 9:16 output (`ok: true`);
a real local `hyperframes render` with `hasAudio: true`; `qa_render.py`
against the delivered MP4 with `H-2`, `H-4.canvas`, `H-4.safe-area`,
`H-4.static-hold`, `H-4.loudness`, `H-4.duration` all `pass`, and the two
advisory gates (`H-4.contrast`, `H-4.type-floor`) also `pass`. Full
envelope: `t4-verification/qa-9x16.json`.

**Not met, named rather than rounded up**: `H-3` (faceless) reports `fail`
— but the flagged frame (`t4-verification/h3-false-positive/`) is pure
typography with no imagery at all; the two "face" boxes sit on bold
headline glyphs, a documented weakness of the Haar-cascade detector
`qa_render.py` uses (WO-FVC-004 T4), not a real face and not a defect this
WO's T4 introduced. Retuning that detector is out of T4's own scope
(audio + render harness) and is not attempted here — reported for whoever
owns `qa_render.py` next, per this WO's "no loosening a rule to pass a
gate" rule: the finding stays visible rather than being patched around.

**Not done, correctly out of scope for T4**: the `<hf-audio-group>`/
`data-fx-chain`/`data-fx-carve`/`data-automation` ducking/automation
mixing graph (`videos/collagen-where-did-it-go/scripts/build_index.py`) —
T4's own bullet (VO at beat starts, one bed under, loudness band,
true-peak, one `audio.wav`) is covered literally; the fuller per-scene
automation engine is not. 16:9 was not run through the full
`render_local.sh` pipeline this pass (R-6 was independently verified on
both canvases separately; the audio/render harness itself was proven on
9:16 only, since the mechanism — `derive_duration`, the `<audio>` wiring,
`qa_render.py`'s gates — is canvas-independent). Real VO (`create_speech`
or local Kokoro) remains blocked exactly as T1-FINDINGS F2 describes;
`kokoro-onnx` could not be installed in this environment either (no
matching `onnxruntime` wheel for this machine's Python 3.9/x86_64) —
named, not silently worked around; `opencv-python-headless==4.10.0.84`
(H-3's own detector) installed cleanly and is now available.

## Judgment calls made

- **Compensated the measured +3dB render-stage loudness gain via
  `--target-lufs`, an existing CLI flag, rather than hard-coding it as
  `mix_audio.py`'s new default.** The gate itself (H-4's -14±2 LUFS
  delivered band) was not touched or loosened; only this run's own pre-mux
  target was tuned to hit it, given a real, reproducible characteristic of
  the render pipeline the audio must go through. A permanent default
  change needs more than one measurement to justify.
- **Did not retune or replace `qa_render.py`'s H-3 face detector** after
  finding its false positive, even though doing so would have made this
  status read "all green." The detector is WO-FVC-004 scope; changing it
  to pass THIS gate would be exactly the "loosen a rule to pass it"
  pattern this WO's own sec 0.1 forbids.
- **Did not attempt kokoro-onnx a second way** (e.g., a different Python,
  a venv) after the pip resolution failed — the local-TTS substitute is
  optional per T1-FINDINGS, and forcing a working install by changing the
  machine's Python environment is a bigger, riskier action than a T4
  audio-harness task warrants.
