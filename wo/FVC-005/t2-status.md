# T2 — Design-system extraction + compiler design — DONE. Flag "back to Sonnet/medium" at the end of this task, per the WO.
Commits: Story Board branch `session/fvc-005`. No claude-skills changes this task (the compiler itself is T3).

## What shipped

1. **Confirmed which of the two identically-named Claude Design projects
   is the real target**, before extracting anything — `a7945a95-…` matches
   every component name, the palette, the six template ids, and the
   `sh-timeline.js` runtime the WO names; `75132ad8-…` (Aug 28) is a
   different system (Montserrat, icons, scrims). Recorded as a Gate 0
   blocker for Kim to confirm, not silently assumed final.
2. **Extracted `videos/_system/`, 67 files, ~2.4 MB**: 5 token CSS files,
   36 component files (12 components × `.jsx`/`.d.ts`/`.prompt.md`), 6
   template artboards verbatim + 6 derived `T*.json` spines, the retired
   `sh-timeline.orig.js`, 5 frozen font files, and one vendored, pinned
   GSAP 3.14.2 confirmed byte-identical to the copy already vetted in
   `videos/ectoin-normal-person/assets/vendor/`.
3. **`MANIFEST.json` re-verifies clean**: every one of 67 tracked files'
   sha256 was independently re-derived this session and matched, twice
   (once after the initial extraction, once after adding the vendored
   GSAP file). Zero mismatches both times. This is the version anchor the
   source project itself does not provide.
4. **Re-ran `hyperframes-engine.md`'s own prescribed `diff -rq`** against
   the installed 0.8.30, rather than trusting a transcription pinned to
   0.8.17–0.8.22. `dist/docs/*` and `dist/templates/_shared/*` — the two
   directories the engine contract is transcribed from — are
   byte-identical across that whole version range. Three `dist/skills`
   reference files differ (all `publish` visibility wording, one
   `--caption-zone` overlap-detection clarification), neither load-bearing
   for the compiler. Recorded in `ENGINE-DIFF-0.8.30.md`.
5. **Measured eleven engine facts directly from the installed
   `hyperframes@0.8.30` `cli.js`/`*.browser.js`**, not carried from any
   doc, three of them independently re-verified by this session's own
   commands (the base64-audio regex, the `<template>`-wrapping error, the
   `font_family_without_font_face` per-file error). These directly shaped
   `COMPILER.md` §0/§3/§4 rather than being asserted from memory.
6. **`COMPILER.md` written** (249 lines): inputs, the timing rule as
   arithmetic (including the D5 split, worked against a real case —
   `T6.json`'s own steps chapter, 6.0s against a 5.0s cap), the attribute
   vocabulary split by which element the engine vs. the retired IR own,
   asset rules, outputs, a full "predict the tree from a T1 beat sheet"
   walkthrough, and eight named refusal conditions.
7. **`MOTION.md`** documents why `sh-timeline.js` is retired as a runtime
   (two real defects plus one architectural reason — D5's scene splitting
   does not scale to a single-document runtime) and how its five markers
   become the compiler's compile-time IR.
8. **`RETIRED-transitions.md`** preserves `beats_to_composition.py:197-479`
   verbatim rather than deleting it, since `C-6` makes it unreachable but
   not worthless — it carries a real 99-vs-0 measured safe-area comparison.
9. **`TEMPLATES.md`** documents that the six `T*.json` files are derived
   by hand from their artboards, never parsed programmatically (a canvas
   artboard's DOM is a layout accident, not a contract), with a sha256
   drift detector per template.

## Accept check — what's verified and what isn't

**Verified:**
- `videos/_system/COMPILER.md` exists and a second reader (this session,
  cross-checking its own §6 against the actual extracted tree) can predict
  the exact 67-file layout from `EXTRACTION.md` + `MANIFEST.json` alone —
  confirmed by literally running `find videos/_system -type f | sort` and
  matching it against the predicted tree.
- Every sha256 in `MANIFEST.json` was independently re-derived and matched,
  not just generated and trusted.
- The vendored GSAP file is byte-identical (sha256-confirmed) to the copy
  already shipping in `videos/ectoin-normal-person/`.
- The `hyperframes-engine.md` re-verification actually ran `diff -rq`
  against two real, cached CLI installations (0.8.22 and 0.8.30) rather
  than being asserted.
- All six `T*.json` files parse as valid JSON and cross-reference
  component names that exist among the 12 extracted components.

**Not verified, and I'm not claiming otherwise:**
- **The compiler itself does not exist yet.** `COMPILER.md`'s claims about
  what the compiler will refuse, split, and emit are a specification, not
  a tested implementation — `T3` builds and tests it.
- **Whether the derived-stagger arithmetic in `COMPILER.md` §2 actually
  produces motion that reads as intentional**, as opposed to merely
  satisfying the 50%-entrance-by-midpoint inequality. That is a claim to
  measure on a real render, in `T3`/`T4`, not to assert here.
- **The eleven engine facts** are measured against 0.8.30's shipped
  `cli.js` source, which is the best evidence available without an actual
  render exercising each rule — but three of the eleven were spot-checked
  with an independent command this session (base64 regex,
  `standalone_composition_wrapped_in_template`,
  `font_family_without_font_face` presence) and the remaining eight were
  read, not independently triggered. `T3`'s render-and-check steps are
  where all eleven get exercised for real.
- **Whether Kim confirms `a7945a95-…` as the intended project.** This is
  named as a live Gate 0 blocker, not resolved by this session's own
  judgment being treated as final.

## Judgment calls made

- **Froze fonts to root-relative files rather than base64-inlining**,
  reversing the WO's original asset-rule text. Justified in `COMPILER.md`
  §0 and `fonts/SOURCES.md`: the base64 requirement came from the Claude
  Design → HeyGen import path, which `D2` demotes to unused, and inlining
  would duplicate ~2.4 MB across dozens of scene files under the
  sub-composition architecture.
- **Placed the extracted design system at `videos/_system/`**, not the
  WO's literal `video/system/` — the WO's own §0.1 rule ("data and
  one-time picks live in the repo") plus this repo's actual `videos/`
  directory name (not `video/`) settle it; the compiler itself goes in
  `makemeavideo/scripts/` (a mechanism, T3), not in the repo.
- **Did not attempt to programmatically parse the `.dc.html` artboards
  into `T*.json`.** Derived by hand, with a sha256 drift check instead —
  a canvas artboard's DOM has no stable contract to parse.
- **Left the two Noto Serif KR files at their fetched size (~1 MB each)
  rather than re-subsetting them.** Flagged in `fonts/SOURCES.md` as a
  `fonttools`-based step out of this WO's stdlib-preferred scope, not
  silently accepted or silently fixed.

## Not done (correctly out of scope for T2)

The compiler implementation (`T3`), the audio/render harness (`T4`), and
everything past them. `T2`'s own deliverable — a document a reviewer can
predict the output tree from — is complete and self-checked against the
real extracted tree.
