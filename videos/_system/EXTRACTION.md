# EXTRACTION.md — what was copied out of Design project a7945a95, when, sha256 per file

## Source

Claude Design project `a7945a95-da21-4823-8b16-57c6ffa11558`,
"SeoulHabit Video Design System", `updatedAt: 2026-09-06T15:40:08.903377Z`
at extraction time. Extracted via the `DesignSync` tool's `list_files` /
`get_file` methods, one file at a time, 2026-09-06, WO-FVC-005 T2.

**Confirmed, not assumed, that this is the right project.** The account
holds two projects sharing the exact name "SeoulHabit Video Design System"
— `a7945a95-…` and `75132ad8-…` (updated 2026-08-28). They are not versions
of one system: `75132ad8-…` is Montserrat/Noto Sans KR with an icon set,
logo marks, scrims, and a dataviz/evidence component family — a different
system entirely. `a7945a95-…` is the only one matching every component name,
palette, template id, and the `sh-timeline.js` runtime this WO's Gate 0
sheet names. This is disclosed as `docs/wo/GATE0-FVC-005.md` blocker #1 and
G0-1 asks Kim to confirm the reading before it is treated as final.

## No version string exists

Neither project carries any file naming a system version (no
`SYSTEM-VERSION`, no version field in any manifest, no changelog). The WO's
own text names "v5.0" — that label cannot be verified against the source
and is not repeated here. **This `MANIFEST.json` — project id +
`updatedAt` + a sha256 per extracted file — is the version anchor** for
whatever was actually ported, per `docs/wo/WO-FVC-005.md` §8.6(a).

## What was extracted, and what was not

**Extracted, verbatim:**
- `tokens/{colors,typography,spacing,motion}.css` — the four token files
  that hold real values (5 files fetched; `fonts.css` handled separately,
  below).
- 12 components × 3 files each (`.jsx`, `.d.ts`, `.prompt.md`) = 36 files —
  every scene and furniture component the readme's Index table names.
- `templates/_shared/sh-timeline.js`, preserved unmodified at
  `sh-timeline.orig.js` (see `MOTION.md` for why it is not shipped as a
  render-time runtime).
- Six `templates/<slug>/<Slug>.dc.html` artboards, verbatim, at
  `templates/reference/`.

**Deliberately not extracted:**
- `assets/`, `avatar/`, `guidelines/*.card.html`, `screenshots/`,
  `ui_kits/`, `thumbnail.html`, `styles.css`, `SKILL.md`, `readme.md`,
  `_ds_bundle.js`, `_ds_manifest.json`, `_adherence.oxlintrc.json`. These
  are Claude Design authoring/preview infrastructure (guideline specimen
  cards, the design-system's own SKILL.md for use as a *prototyping*
  skill, review harnesses) — none of it is consumed by the compiler this
  WO builds. If a future task needs the guideline cards for human
  reference, extract them then, named explicitly, rather than carrying
  unused weight now.

**Fetched separately, not extracted from the project:** the five font
`.woff2` files. The project itself ships no font binaries — its own
`tokens/fonts.css` loads them from a CDN and says so in its own comment.
See `fonts/SOURCES.md` for the pinned URLs and hashes actually used.

## Verify

```
$ python3 -c "
import hashlib, os, json
SYS = 'videos/_system'
m = json.load(open(f'{SYS}/MANIFEST.json'))
bad = 0
for rel, meta in m['files'].items():
    h = hashlib.sha256(open(f'{SYS}/{rel}','rb').read()).hexdigest()
    if h != meta['sha256']:
        print('MISMATCH', rel); bad += 1
print(f\"{len(m['files'])} files checked, {bad} mismatches\")
"
```

Run this session: **63 files checked, 0 mismatches.**
