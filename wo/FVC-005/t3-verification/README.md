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

## D5 split path

`d5-split/` proves the one path this evidence directory's first pass
didn't exercise: a scene whose derived duration exceeds its ceiling. Two
real bugs were found and fixed in the process (the split algorithm not
accounting for the scene's own trailing hold, and split timing not
carrying split content with it) — see `d5-split/README.md` for the full
account, `d5-split/check-9x16.json` for the clean gate result, and the two
extracted frames showing visually distinct, correctly-content-sliced
output.

## The remaining four emitters

`four-emitters/` proves the last gap: `ShCompare`, `ShMyth`, `ShQuote`, and
`ShSteps` — the four of nine scene components no earlier fixture had
exercised. Two more real bugs were found and fixed (a grid-overflow on
`ShCompare` and a motion-freeze gap the earlier D5 fallback fix didn't
fully close for longer one-shot-sweep scenes) — see
`four-emitters/README.md`, `four-emitters/check-9x16.json`, and four
extracted frames confirming visually correct, on-canvas output for all
four.

## A second overflow, in a different emitter, via a different mechanism

`ingredient-overflow/` tests `ShIngredient` deliberately with a genuinely
unbreakable long name (a real 24-character INCI term with no spaces or
hyphens) rather than waiting for the same defect class to surface by
accident. It did: the name div grew to 1895.89px, nearly double the
1080px canvas — the flexbox equivalent of the earlier `ShCompare` grid
bug (`#cid-wrap`'s default `min-width:auto` refusing to shrink below the
unbreakable text's own width). Fixed with `min-width:0` plus
`overflow-wrap:anywhere` (not `break-word`, which does not fix this).
See `ingredient-overflow/README.md` for why those two specific properties
were needed together, `ingredient-overflow/check-9x16.json` for the clean
result, and the extracted frame showing the name correctly breaking
mid-word and staying fully on-canvas. Flags that the remaining seven
emitters have not had the same adversarial-text stress test yet.

## Systematic stress test of the remaining seven emitters

`stress7/` completes the adversarial-text pass across all nine
components: one combined 7-scene fixture stressing `ShHook`, `ShRows`,
`ShSteps`, `ShEvidence`, `ShMyth`, `ShQuote`, and `ShEndcard` at once.
Found and fixed the same overflow defect class in all six non-endcard
emitters (some via `min-width:0`, some also needing `display:block` in
place of an `inline-block` wrapper's shrink-to-fit sizing), plus a far
more serious, universal bug: **every video's closing scene opened with a
~0.17s completely blank flash**, confirmed by exact frame-level pixel
analysis, present in *every* video this compiler could produce until
fixed. See `stress7/README.md` for the full account, including one
`check --at-transitions` finding investigated and ruled a sampling
artifact at hard-cut boundaries rather than a real defect, backed by two
extracted frames proving the actual rendered output is clean.

## D5 split + adversarial content, combined

`d5-adversarial/` tests the intersection of the D5 split path and the
overflow-safety fixes together for the first time -- a scene using the
same real unbreakable 24-character INCI term, split across two
sub-scenes, as both the video's first scene (frame-zero + split +
adversarial, combined) and a mid-video scene (`ShSteps`). A genuinely
informative negative result: no new bugs. Every independently-verified
fix (D5's content slicing, the overflow guards, frame-zero suppression,
the blank-endcard fix) held up in combination. One recurrence of the
already-known `check --at-transitions` artifact at the transition into
the endcard refined the earlier finding: the common factor across both
occurrences (a `ShQuote` scene and now a `ShSteps` split sub-scene, both
transitioning into `ShEndcard`) is that the endcard is the only
component that is both `anchor: true` and chip-less -- not anything
about the outgoing scene or about splitting. See `d5-adversarial/README.md`.

## The endcard-transition artifact's exact mechanism, confirmed

`artifact-mechanism/` closes out the `check --at-transitions` finding
carried as "investigated, ruled a check-tool artifact" since `stress7/`.
Rather than leave it at pattern-matching (clean frames, correlates with
`ShEndcard` as the incoming scene), this reads `hyperframes@0.8.30`'s own
`dist/cli.js` to find the actual sampling mechanism
(`collectTweenBoundaries`/`seekCompositionTimeline`/
`window.__player.renderSeek`), verifies it live against a running instance
of the `stress7` fixture (a real ~33ms, one-frame visibility lag in the
generic scrub-seek path, specific to hard cuts into `ShEndcard`), and then
confirms the actual `hyperframes render` PNG-sequence output at the exact
reported times is completely clean — the frame-capture pipeline does not
share the scrub-seek path's lag. Conclusion: a named, understood
`check --at-transitions` measurement limitation, not a compiler defect. See
`artifact-mechanism/README.md` for the full source citations and the three
decisive rendered frames.

## Repo gates the plan named but this pass had skipped

`repo-gates/` closes a real gap: `check-legibility.py` and `check-safe-area.py`
were in the approved plan's Step 10 (per D6) but never actually run against
T3's output, and never named in `t3-status.md`'s "Not verified" section as a
deliberate deferral either. Running them now: legibility's token-floor half
clears both canvases with zero margin (`--t-chip` lands exactly on the floor,
28px/24px); its render-based half fails 16:9 (4px measured against a 5px
floor, on two independent probes). `check-safe-area.py` fails **both**
canvases — measured precisely on the actual worst-case frames: `ShRows`'
right-aligned values sit 57px inside YouTube Shorts' real reserved UI rail on
9:16, the citation chip sits mostly inside the real reserved bottom zone on
16:9. Root cause, confirmed on pixels rather than inferred: the compiler
correctly implements `videos/_system/tokens/spacing.css`'s own `--safe-x`/
`--safe-bottom` exactly as declared — those declared margins are themselves
narrower than the real platform UI they're meant to clear. A T2
(design-system) finding surfaced by a T3 gate, not a T3 defect, and not a
call this session makes unilaterally. See `repo-gates/README.md`.

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
