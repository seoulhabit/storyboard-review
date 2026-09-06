# T3 verification evidence

Why these live here and not in the live output directory: the compile
target was a scratch fixture outside the repo (`/private/tmp/.../t1-fixture`),
so its full output tree (including the ~2.4 MB of copied fonts and the
vendored GSAP file, already tracked once at `videos/_system/`, plus the
634 KB rendered MP4) is not checked in here. What's committed is the
deterministic, textual evidence a reviewer needs to re-verify the claim
without re-running anything:

- `synthetic-t1-fixture.beat-sheet.json` — the exact input. Five scenes
  matching `templates/T1.json`'s sequence (`hook -> ShHook`,
  `define -> ShIngredient`, `mechanism -> ShRows`, `evidence -> ShEvidence`,
  `cta -> ShEndcard`), none exceeding the D5 ceiling (this fixture does not
  exercise the split path — that is a separate, still-open test named in
  `t3-status.md`'s "Not verified" section).
- `compile-report-9x16.md` / `-16x9.md` — the compiler's own accounting:
  5 scenes, tiled with no gaps, 14.600s total, identical component
  sequence and timing in both canvases (COMPILER.md §7's claim).
- `check-9x16.json` / `check-16x9.json` — the full `hyperframes check
  --samples 40 --at-transitions --json` result for each canvas, captured
  verbatim (not summarized): `"ok": true`, every one of
  lint/runtime/layout/motion/contrast at `errorCount: 0`.

## Reproduce from scratch

```
python3 <claude-skills>/makemeavideo/scripts/compile_composition.py \
  synthetic-t1-fixture.beat-sheet.json /tmp/t3-repro \
  --system videos/_system --format both
cd /tmp/t3-repro/06-render/9x16 && hyperframes check --samples 40 --at-transitions --json
cd /tmp/t3-repro/06-render/16x9 && hyperframes check --samples 40 --at-transitions --json
hyperframes render -q draft -o out.mp4   # from either canvas dir
```

A local render was additionally produced and visually inspected this
session (not committed — reproducible, and binary): 1080×1920, exactly
14.600s, 438 frames, h264, 634 KB. Three frames were extracted and sent to
the user directly: frame 0 (the hook, fully dense, no blank start), a frame
well into the rows scene (all four rows visible, the active row correctly
in clay, brass hairline connectors, DejaVu Serif right-hand terms), and the
end card (the Korean 서울의 습관 wordmark rendering correctly via the
hangul-unicode-range Noto Serif KR attachment — proof the font-freeze from
T2 actually works at render time, not just at compile time).
