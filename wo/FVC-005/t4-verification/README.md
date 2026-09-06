# T4 verification evidence — R-6 (safe-area) + audio/render harness

## R-6 — safe-area widened to 15%/10%

`videos/_system/tokens/spacing.css` changed (`9:16 --safe-x 10%->15%`,
`16:9 --safe-bottom 8%->10%`), `MANIFEST.json` re-hashed, and
`compile_composition.py`'s mirrored `FORMATS` constants updated to match
(claude-skills, same commit series). Re-ran T3's own repro exactly
(`t3-verification/repo-gates/README.md`'s reproduce block) against the
recompiled synthetic-t1-fixture:

```
9x16:  check-safe-area.py --canvas-w 1080 --canvas-h 1920
       reserved zones: top<192  bottom>=1536  right>=918
       no findings (58 frames sampled) — was FAIL (57px inside the rail) before R-6.
16x9:  check-safe-area.py --landscape
       reserved zones: top<54  bottom>=972  right>=1824  left<96
       no findings (58 frames sampled) — was FAIL (22/29px inside the zone) before R-6.
```

`repo-gates/r6-9x16.mp4` and `repo-gates/r6-16x9.mp4` are the two renders
this was measured against.

## T4 — audio + render harness

Scripts (claude-skills `makemeavideo/scripts/`): `mix_audio.py`,
`render_local.sh`, `render_cloud.sh`, `_qa_adapter.py`. Proven against the
same synthetic-t1-fixture beat sheet, 9:16 canvas, in a scratch project
directory (`MMAV_PROJECT_ROOT` override — never touched `videos/` for
this).

**Pipeline run**: `mix_audio.py` (5 scenes, slate-tone VO substitutes +
pink-noise placeholder bed, `--patch-beat-sheet`) -> `compile_composition.py`
(audio wired via the existing T3 `<audio>` contract) -> `render_local.sh`
(check -> render -> extract -> qa_render).

**Two real bugs found and fixed while proving this, not assumed clean:**

1. `mix_audio.py`'s own loudness measurement matched the FIRST `I: <n>
   LUFS` line in ffmpeg's ebur128 output (an unconverged reading during the
   scan, e.g. -70 LUFS at t=0.1s) instead of the final `Summary:` block —
   fixed to scope the regex to `Summary:` first, exactly like
   `qa_render.py`'s own `gate_h4_loudness` already does.
2. `_qa_adapter.py` passed the beat sheet's own top-level `vo_duration_s`
   (12.0s, the raw narration sum) through unchanged into the QA-facing
   copy. `qa_render.py`'s `H-4.duration` gate and `index_supplied_frames()`
   both read that field as the video's total intended length (true in the
   OLD schema); in T2/T3's schema it is only the narration sum, and
   COMPILER.md's own timing rule (`vo_duration_s + 0.3s tail` or the
   reading floor, whichever is larger) always makes the real compiled
   video longer (14.6s here). Fixed by having the adapter always overwrite
   `vo_duration_s` with the derived total.

**One real, external finding, not a bug in either script**: the source
`audio.wav` measured -14.0 LUFS / -8.0 dBTP on disk, but the SAME file
measured -11.0 LUFS after going through `hyperframes render`'s Chrome
audio-capture + AAC mux (confirmed NOT an artifact of AAC encoding itself:
encoding the same WAV to AAC with plain `ffmpeg` measures -14.0 LUFS
unchanged). HyperFrames' own render pipeline adds roughly +3dB somewhere
between the `<audio>` element and the muxed track. Compensated for this
run by mixing to a -17 LUFS pre-mux target (`mix_audio.py --target-lufs
-17`); the delivered file then measured -14.0 LUFS / -10.9 dBTP, inside
H-4's band. This is named as a render-engine characteristic to investigate
before it becomes a permanent default, not baked into `mix_audio.py` as a
silent compensation constant.

**Final qa_render.py verdict** (`qa-9x16.json`): `H-2` pass, `H-4.canvas`
pass, `H-4.safe-area` pass, `H-4.static-hold` pass, `H-4.loudness` pass,
`H-4.duration` pass, `H-4.contrast`/`H-4.type-floor` pass (advisory).
**`H-3` (faceless) fails** — but on inspection
(`h3-false-positive/frame-t11.0s-evidence-scene.png`) the flagged frame is
pure typography (a "2.8%" stat and citation text, no imagery at all,
consistent with the design system's own no-photography rule, T1-FINDINGS
F3). The two "face" boxes land squarely on the bold `"Matched hydro..."`
headline glyphs — a Haar-cascade false positive on high-contrast text, a
known weakness of that detector family, not a real face. This is a
pre-existing `qa_render.py` (WO-FVC-004 T4) limitation surfaced by
actually running the harness end-to-end against real typographic content,
not a defect introduced by T4's own scripts, and not something T4 retunes
(no loosening a gate to pass it — the finding is named here for whoever
owns `qa_render.py`'s detector next).

`check-9x16.json` (`hyperframes check`, `ok: true`) and `mix-report.json`
(the audio mix's own measured numbers) are included for the full chain of
evidence.
