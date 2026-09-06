# SOURCES.md — frozen font provenance

Fetched 2026-09-06, from the exact pinned URLs `tokens/fonts.css` named in
the extracted Claude Design project (the project itself ships no font
binaries — see `EXTRACTION.md` / `MANIFEST.json`). Pinned to a specific
Fontsource package version (`@5`), never `@latest` — an unpinned URL is an
expiring/moving target, which the WO's asset rules forbid regardless of
whether the bytes happen to be base64-inlined or root-relative.

| File | Source URL | sha256 | Bytes |
|---|---|---|---|
| `dejavu-serif-400.woff2` | `https://cdn.jsdelivr.net/npm/@fontsource/dejavu-serif@5/files/dejavu-serif-latin-400-normal.woff2` | `8dbcad0d5f9f95d4ca21080e87dc83fc7c728106c1536769f346c397e8a26bf` | 143,920 |
| `dejavu-serif-700.woff2` | `https://cdn.jsdelivr.net/npm/@fontsource/dejavu-serif@5/files/dejavu-serif-latin-700-normal.woff2` | `190f2c82c7e1f252ba7da6bba2f6ed56e5f8d1357814f7c04d8e26759ab99ef` | 130,464 |
| `archivo-variable.woff2` | `https://cdn.jsdelivr.net/npm/@fontsource-variable/archivo@5/files/archivo-latin-wght-normal.woff2` | `8f704806dbedeaaeca334b11ec348bc3ac3a439d6431544b3afb54f534ee496` | 34,928 |
| `noto-serif-kr-700.woff2` | `https://cdn.jsdelivr.net/npm/@fontsource/noto-serif-kr@5/files/noto-serif-kr-korean-700-normal.woff2` | `504d6af6abb882acd912d47bafa383c4512a6c8c33635e4e8fb37111d931094` | 1,033,556 |
| `noto-serif-kr-400.woff2` | `https://cdn.jsdelivr.net/npm/@fontsource/noto-serif-kr@5/files/noto-serif-kr-korean-400-normal.woff2` | `c9a1e3ac69994d680883b53b1fd83d520733b704792522a932bfaa276117de4` | 971,428 |

Re-verify with:

```
$ shasum -a 256 videos/_system/fonts/*.woff2
```

## Why root-relative, not base64-inlined, by default

This WO's original spec called for base64-inlined fonts (the Claude Design
→ HeyGen import contract needs it, since that path has no filesystem to
reference). This WO's `D2` ruling demotes that import path to unused —
render is local by default (`R-1`) — and this session measured directly
against the installed `hyperframes@0.8.30` lint that `composition_file_too_large`
counts lines **after stripping `<style>` blocks**, so inlining costs nothing
against that particular gate either way. The reason to freeze-and-reference
instead is architectural, not gate-driven: this WO's compiler emits one
`<template>` sub-composition per scene (see `COMPILER.md`), and a beat sheet
with ~50 scenes (kbeauty-scale, 257s at the 5s ceiling under D5's split
rule) would duplicate ~2.3 MB of base64 font payload up to 50 times if
inlined per file. Referencing the same five files from
`videos/<slug>/06-render/<canvas>/assets/fonts/` keeps one copy on disk
regardless of scene count, exactly the pattern already shipping clean in
`videos/kbeauty-label-trap/04-assets/fonts/` and
`videos/ectoin-normal-person/scripts/_preamble.py`.

`--inline-fonts` remains available as a compiler flag for the rare case of
a genuinely single-file deliverable (e.g. handing one HTML file to someone
outside this pipeline).

## Noto Serif KR file size, flagged

The two Noto Serif KR files are far larger (971 KB / 1.03 MB) than the
Latin faces (35–144 KB) despite `tokens/fonts.css`'s comment describing
them as attached "under a hangul-only `unicode-range`". The `unicode-range`
CSS property controls which code points *trigger* a browser's download of
this file — it does not necessarily mean Fontsource pre-subsets the file's
internal glyph table to only those code points. This is exactly the file
Fontsource publishes under the `korean` subset name; it was not
re-subsetted further in this pass. If Korean-glyph-only trimming is wanted
to shrink this, that is a `fonttools`-based build step out of this WO's
scope (stdlib-only was preferred for the compiler itself) — flagged here
rather than silently accepted or silently fixed.
