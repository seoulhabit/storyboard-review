# hyperframes-engine.md re-verification against 0.8.30

`claude-skills/faceless-video-craft/references/hyperframes-engine.md` states
its own provenance honestly: transcribed from the CLI's shipped docs, pinned
`0.8.17`–`0.8.22`, verified byte-identical by `diff -rq` at the time, with
the instruction *"Re-run that diff when a new pin appears; do not assume
it."* This repo's `hyperframes` now resolves globally at **0.8.30**. Re-run,
this session, before T2 trusts a single line of the transcription.

## Command and result

```
$ diff -rq <0.8.22 cache>/dist/docs      <0.8.30 global>/dist/docs
  (no output — byte-identical)
$ diff -rq <0.8.22 cache>/dist/templates/_shared  <0.8.30 global>/dist/templates/_shared
  (no output — byte-identical)
$ diff -rq <0.8.22 cache>/dist/skills     <0.8.30 global>/dist/skills
  3 files differ (all in dist/skills/*/references/*.md)
```

**`dist/docs/*` and `dist/templates/_shared/*` — the two directories
`hyperframes-engine.md`'s data-attributes/gsap/compositions contract is
transcribed from — are byte-identical, 0.8.22 → 0.8.30.** The engine
contract this WO's compiler is built against (root `data-composition-id`/
`data-width`/`data-height`, `class="clip"` + `data-start`/`data-duration`,
`gsap.timeline({paused:true})` on `window.__timelines[<id>]`, relative
`data-composition-src`, no `Date.now`/`Math.random`/network) holds unchanged
at 0.8.30. `hyperframes-engine.md` can be trusted as-is for T2/T3.

## What did change (not load-bearing for the compiler)

Three `dist/skills/*/references/*.md` files differ — all about `hyperframes
publish` visibility semantics (publish is now **private by default**, with
an explicit `--public` flag and visibility-preserving re-publish behaviour)
and one clarification to `--caption-zone`'s overlap test (now explicitly a
text element's `getBoundingClientRect` overlap with the band, rather than
"content whose center sits inside the band"). Neither touches composition
authoring or the render contract. The `--caption-zone` clarification is
worth carrying into `T4`'s render-QA harness (it changes what counts as a
caption-zone violation), but is irrelevant to T2/T3's compiler work.

## Conclusion

`hyperframes-engine.md` is current at 0.8.30 for every fact `beats_to_composition.py`
and this WO's compiler depend on. No re-transcription needed before T2/T3
proceed.
