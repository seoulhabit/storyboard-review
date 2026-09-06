# The `content_overlap`/`text_occluded` artifact at endcard transitions — mechanism, confirmed

Every prior round that touched a chip-less `ShEndcard` scene (`stress7`,
`d5-adversarial`) hit the same `check --at-transitions` finding: a
`content_overlap`/`text_occluded` warning on the outgoing scene's text,
timestamped exactly at the hard-cut boundary into `cta`. Both rounds already
concluded — correctly — that this was a check-tool artifact, not a real
defect, on the strength of clean extracted frames at and around the
boundary. What was missing was *why* the check tool reports it at all. This
round reads the installed engine's own source (`hyperframes@0.8.30`) to find
the exact mechanism, then verifies that mechanism against a live page rather
than trusting the reading.

## 1. Where `--at-transitions`'s sample times come from (source read)

In `dist/cli.js`, `runLayoutAudit()`'s `--at-transitions` branch calls:

```js
const boundaries = await collectTweenBoundaries(page);
const transitions = buildTransitionSampleTimes({ duration, boundaries, cap: opts.maxTransitionSamples });
```

`collectTweenBoundaries(page)` runs in-browser and does exactly this (full
text, deminified names aside):

```js
const toTimelineTime = (root, anim, localTime) => {
  let time = localTime, node = anim;
  while (node && node !== root) {
    time = callOr(node.startTime, node, 0) + time / (callOr(node.timeScale, node, 1) || 1);
    node = node.parent;
  }
  return time;
};
const tweenBoundaries = (root, tween) => {
  if (typeof tween.duration !== "function") return [];
  return [toTimelineTime(root, tween, 0), toTimelineTime(root, tween, tween.duration())]
    .filter(Number.isFinite);
};
const timelineBoundaries = (timeline) =>
  (timeline.getChildren?.(true, true, false) ?? []).flatMap((tween) => tweenBoundaries(timeline, tween));
return Object.values(window.__timelines ?? {}).flatMap(timelineBoundaries);
```

For every **top-level** entry in `window.__timelines` (this compiler
registers one per scene — `hook`, `rows`, …, `cta` — plus the root `main`),
it walks that timeline's own tween tree and reports each tween's start/end
**relative to that timeline's own root**. This is the correct, intended
design for collecting every scene's own internal animation boundaries in
absolute terms once GSAP has nested/positioned them — the boundary values it
collects legitimately include each scene's own mount instant.

`buildLayoutSampleTimes`'s **base grid** (`--samples 40` on this fixture's
25.8s duration) does *not* land near 23.4 — the nearest grid points are
22.898 and 23.543, both real evenly-spaced samples about 0.6s apart. So the
finding at exactly `23.4` / `23.432` is a **transition-boundary sample**,
not a base-grid coincidence.

## 2. Confirming the seek mechanism (source read)

Every sample — base grid or transition — is captured by
`collectLayoutIssues()`, which calls `seekCompositionTimeline(page, time, …)`
before every `__hyperframesLayoutAudit` probe. That function's seek cascade,
read from `cli.js`:

```js
const renderSeek = getProperty(player, "renderSeek");   // window.__player.renderSeek — tried first
const playerSeek  = getProperty(player, "seek");
const bridgeSeek  = getProperty(hf, "seek");             // window.__hf.seek
// falls back to raw window.__timelines[key].seek(t) only if nothing above exists
```

`window.__player.renderSeek` is a general-purpose scrub API — the same one
the interactive Studio preview uses for scrubbing/editing — not a
frame-capture-specific code path.

## 3. What `renderSeek` actually does at the boundary (live verification)

Rather than trust the reading, this was checked against a live, fully
mounted page. `hyperframes preview` was started on the exact `stress7`
fixture (`06-render/9x16`), confirming `window.__timelines` really does
carry one key per scene (`hook, rows, steps, evidence, myth, quote, cta`,
plus `main`) once mounted, and `window.__player.renderSeek` is present with
the same shape `seekCompositionTimeline` expects.

Binary-searching `renderSeek(t)` around the `quote → cta` boundary
(`quote` ends and `cta` starts at `t=23.400`, from the compile report):

| t | `quote` clip `visibility` | `cta` clip `visibility` |
|---|---|---|
| 23.399 | visible | hidden |
| **23.400** | **visible** | **visible** |
| 23.410 – 23.432 | visible | visible |
| 23.435 | **hidden** | visible |

`quote`'s `.clip` stays `visibility: visible` for **~33ms past its own
`data-duration` end** — one frame at 30fps — while `cta`'s `.clip` becomes
visible exactly on schedule at `t=23.400`. For that ~33ms window, both
scenes' content is simultaneously in the accessibility/layout tree at full
opacity — which is precisely what `--at-transitions` samples and precisely
why it reports overlap at `23.4` and `23.432` (`firstSeen`/`lastSeen` in the
original JSON, 32ms apart — consistent with exactly one dropped frame's
width).

The same probe at the two other hard cuts in the same composition
(`hook → rows` at `3.300`, `rows → steps` at `8.100`) shows **zero overlap
window** — the outgoing clip goes hidden on the exact same tick the
incoming clip goes visible, no lag at either boundary. So this is not a
generic per-cut rounding bug in the engine; it reproduces specifically
where the incoming scene is `cta` (`ShEndcard`, chip-less, `anchor: true`),
consistent with every prior round's finding.

**Caveat carried forward explicitly**: the Studio preview is documented
(`CLAUDE.md`, "the preview server rewrites your files while it runs") to run
a different, live-editing-oriented code path than the plain compiled
project — its own attribute rewriting (`data-hf-id`, `data-duration` →
`data-hf-authored-duration`) is visible in this same test. `renderSeek`
existing and behaving this way in the *Studio's* runtime instance does not
by itself prove `check`'s own bundled-and-served instance behaves
identically. That gap is closed in the next section, not assumed away.

## 4. What actually ends up in the rendered video (ground truth)

`hyperframes render . -q draft -f 30 --format png-sequence` was run on the
same fixture, producing all 774 frames of the 25.8s video individually as
PNGs — the actual pixel-capture pipeline `render`/`check` bundle and drive,
distinct from the Studio's interactive scrub path.

- Frame 703 (`t = 23.400`, exactly the reported artifact time).
- Frame 704 (`t = 23.433`, matching the reported `lastSeen: 23.432`).

Both frames — `frame-703-t23.400-reported-artifact-time.png` and
`frame-704-t23.433-reported-lastSeen-time.png` in this directory — show the
`cta` endcard alone (서울의 습관 / SEOULHABIT / the citation line), with
**no visible trace whatsoever** of the quote scene's
"Polymethylsilsesquioxane is simply inert." text: no ghosting, no
overlapping glyphs, nothing. `frame-702-t23.367-last-quote-frame.png` (the
last frame that is genuinely still `quote`'s own) is included for
before/at/after continuity.

## Conclusion

The mechanism is now fully accounted for, not just worked around:

1. `--at-transitions` legitimately samples each scene's own mount instant
   as a transition boundary (`collectTweenBoundaries`, confirmed from
   source).
2. The generic scrub-seek path (`window.__player.renderSeek`, also used by
   the interactive Studio) has a real, reproducible ~1-frame lag in
   `.clip[data-composition-id]` visibility teardown, specific to
   transitions where the incoming scene is `ShEndcard` — verified live
   against a fully mounted page, not inferred.
3. The actual frame-capture rendering pipeline (`hyperframes render`'s
   PNG-sequence output) does **not** carry this lag: the exact reported
   times, checked as real rendered pixels, are clean.

**This is a `hyperframes check --at-transitions` measurement limitation**,
not a compiler defect and not a shipped-video defect: the check tool's
layout audit and the render pipeline's frame capture use different seek
mechanisms, and only the former exhibits the lag. No compiler change
follows from this — the composition is provably correct in the artifact
that is actually delivered. This is recorded as a known, understood,
named limitation of the check tool at hard-cut-into-chip-less-scene
boundaries, worth reporting upstream, not worth working around by changing
correct compiler output.

## Reproduce

```bash
# 1. Confirm the finding still reproduces
cd t3-verification/stress7 && hyperframes check --samples 40 --at-transitions --json | \
  python3 -c "import json,sys; d=json.load(sys.stdin); print([f for f in d['layout']['findings'] if f['code'] in ('content_overlap','text_occluded')])"

# 2. Confirm the live renderSeek lag (Studio preview, one scene pair)
hyperframes preview <fixture>/06-render/9x16 --port=3911 --background --no-open
# open http://localhost:3911/api/projects/9x16/preview?__hf_shader_capture_scale=1&__hf_shader_loading=player
# in a browser and binary-search window.__player.renderSeek(t) around the
# reported time, reading getComputedStyle(clip).visibility

# 3. Confirm the real render is clean at the exact reported time(s)
hyperframes render <fixture>/06-render/9x16 -q draft -f 30 --format png-sequence -o frames-png
# open frames-png/frame_NNNNNN.png where NNNNNN = round(reported_time*fps)+1
```
