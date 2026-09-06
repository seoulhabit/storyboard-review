# T3 — Compiler build — DONE for the standard (non-split) path; end-to-end proven with a real local render
Commits: claude-skills branch `fvc-005/makemeavideo` (compiler); Story Board branch `session/fvc-005` (this status + verification evidence). Back to Sonnet/medium tier per the WO's own flag, T2 being the Opus/High task.

## What shipped

`claude-skills/makemeavideo/scripts/compile_composition.py` (~1,080 lines):
`03-beat-sheet.json` + `videos/_system/` + `04-assets/` → `06-render/<canvas>/`
valid HyperFrames compositions, per the port ledger in the WO plan (~35%
verbatim from `beats_to_composition.py`, ~40% adapted, ~25% new — the
honest split, not "maximum reuse"). Ported verbatim: the utility floor
(`die`/`warn`/`slugify`/`esc`/`f3`), `scene_filename`'s naming contract,
the `(html, assertions)` co-emission discipline, the `WARNINGS` ledger.
New: the D5 timing/split solver, nine component emitters (one per
SeoulHabit scene component), the shared `build_tweens` motion layer, and
the MANIFEST.json drift check run at the start of every compile.

**Proven end-to-end, not just structurally**: a synthetic T1 beat sheet
(`wo/FVC-005/t3-verification/synthetic-t1-fixture.beat-sheet.json`)
compiled to both canvases, passed `hyperframes lint` (0/0), passed full
`hyperframes check --samples 40 --at-transitions --json` on **both**
canvases (`ok: true`, every one of lint/runtime/layout/motion/contrast at
`errorCount: 0` — see `t3-verification/check-{9x16,16x9}.json`), rendered
locally to a real MP4 (1080×1920, exactly 14.600s, 438 frames, h264), and
three extracted frames were visually inspected and sent to the user: frame
0 (the hook, fully dense — the frame-zero rule holds), a rows-scene frame
(correct palette, correct active-row clay, correct DejaVu Serif/Archivo
split), and the end card (서울의 습관 rendering correctly via the
hangul-unicode-range Noto Serif KR attachment — proof the T2 font freeze
actually works at render time, not merely at compile time). Confirmed
dual-format timing invariance (COMPILER.md §7's claim): the two canvases'
`index.motion.json` files are byte-for-byte identical in `duration` and
`assertions`. Confirmed determinism: two independent compiles of the same
input are byte-for-byte identical across every emitted file, and a grep
for `Date.now`/`Math.random`/`setTimeout`/`requestAnimationFrame`/
`repeat:-1` across every generated `.html` file (excluding the vendored,
third-party GSAP library) returns nothing.

## Five real bugs found by actually running the engine, not assumed away

Every one of these was a genuine `hyperframes lint`/`check` finding against
a first-draft compile, diagnosed from the engine's own message, and fixed
before moving on — not discovered later and patched around:

1. **Token scoping.** The extracted `tokens/*.css` declare `:root{...}`
   and a bare `[data-canvas="16x9"]{...}` attribute selector. The proven,
   shipping pattern in `beats_to_composition.py` scopes every custom
   property to `#root{...}` directly, never `:root`. Rescoped at compile
   time (`load_tokens_css`) rather than trusting `:root` to survive
   whatever CSS scoping the engine applies to sub-composition `<style>`
   blocks — untested and unnecessary to test, since the working pattern
   already avoids the question entirely.
2. **Asset path.** Fonts were referenced `../../assets/fonts/...`. `lint`'s
   own `invalid_parent_traversal_in_asset_path` finding named the fix
   directly: compositions are served with the *project root* as base URL,
   so the correct path from a `compositions/frames/*.html` file is the
   same root-relative `assets/fonts/...` as from the root `index.html`,
   never a `../`-prefixed one.
3. **Entrance tween method.** First draft used `gsap.set(el,{opacity:0,y:40})`
   in CSS/JS, then `tl.from(el,{opacity:0,y:40,...})`. Two conflicts: CSS
   `transform:translateY(40px)` alongside a GSAP tween animating `y` is
   `gsap_css_transform_conflict` (GSAP overwrites the whole CSS transform);
   and `tl.from()` animating FROM `{opacity:0}` TO whatever the "current"
   CSS value is — which was ALSO `opacity:0` — is `gsap_from_opacity_noop`,
   a literal 0→0 no-op. Fixed by matching `beats_to_composition.py`'s own
   working "arrive" pattern exactly: CSS declares only `opacity:0` (never a
   `transform:`), `gsap.set()` establishes `{opacity:0,y:40}` outside the
   timeline, and the timeline tween goes `tl.to(el,{opacity:1,y:0,...})` —
   forward, not `.from()`.
4. **Motion sidecar schema.** Invented top-level shape
   (`{keepsMoving:[...], appearsBy:[...], ...}`) was rejected outright:
   `motion_spec_invalid`, "spec must have an assertions array". Read the
   real schema off a shipping project's own `index.motion.json`
   (`videos/collagen-where-did-it-go/`) — one flat `assertions` array,
   each entry carrying its own `kind` — and rewrote `build_sidecar` to
   match it exactly, rather than guessing at a second attempt.
5. **Motion assertion selectors and the "≥2 continuous patterns" rule, in
   real render terms.** A `motion_selector_ambiguous` finding on
   `#mechanism-rows > div` (a class-shaped selector matching all four
   rows) led to adding a distinct `assert_selector` (the group's *last*
   element, matching the real generator's own `#hook-slam-last`-style
   convention) separate from the *animation* selector, which is allowed to
   match many elements. Separately, `motion_frozen` fired on the hook scene
   (0–2.4s, fully static — correct per the frame-zero rule, but a real
   engine violation since the design system's own "≥2 continuous patterns
   per scene" rule is not optional, confirmed by the engine's own 2.0s
   default static-hold ceiling) and again on the ingredient scene (2.4–5.6s,
   whose one-shot entrance completes and then the scene sits static for the
   remainder). Fixed at the render layer, not per-emitter: `render_scene`
   now checks whether an emitter's own markers already include a
   float/sweep/count, and if not, adds a subtle breathing float on the
   whole `#cid-stage` wrapper — plus, for `ShHook` specifically, a "clay
   sweep under the hook word," one of the design system's own named
   idioms, since a wrapper-level float alone would have been a duller
   substitute for a component the design system already has a stated
   pattern for.

## Accept check — what's verified and what isn't

**Verified:**
- `hyperframes lint` on the compiled output: 0 errors, 0 warnings.
- `hyperframes check --samples 40 --at-transitions --json` on both 9x16 and
  16x9: `ok: true`, all five categories `errorCount: 0` — captured verbatim
  in `t3-verification/check-{9x16,16x9}.json`, not summarized from memory.
- A real local `hyperframes render` produced a real MP4, `ffprobe`-confirmed
  at the declared dimensions and duration, and visually inspected (three
  frames, sent to the user) rather than trusted on the render tool's own
  success message alone.
- Determinism: two independent compiles are byte-identical (`diff -r`,
  empty); no disallowed non-deterministic construct in any generated file.
- Dual-format timing invariance: the two canvases' motion sidecars are
  identical except nothing (their `duration` and `assertions` match
  exactly), which is what COMPILER.md §7 predicts and requires.
- The second static gate named in the plan,
  `claude-skills/faceless-video-craft/scripts/lint_composition.py`, run
  against all 6 compiled 9x16 files: `0 error(s), 0 warning(s)`.

**Not verified, and I'm not claiming otherwise:**
- **The D5 split path has not been exercised against a real render.** The
  synthetic fixture's scenes all fit their ceilings; `plan_scene`'s split
  arithmetic is exercised by the fixture's own logic (`plan_scene`,
  `split_beats_by_ceiling`) but has no unit-test file yet, and no compiled,
  checked, rendered proof exists for a scene that actually splits. This is
  named as the next thing to prove, not assumed to work because the
  arithmetic looks right on paper.
- **`ShCompare`, `ShMyth`, `ShQuote`, `ShSteps` have not been exercised
  through a real compile.** The synthetic fixture only uses `ShHook`,
  `ShIngredient`, `ShRows`, `ShEvidence`, `ShEndcard` (T1's own sequence).
  The other four emitters were written to the same pattern and pass a
  Python syntax check, but have not been proven against `hyperframes
  check` the way these five have.
- **Neither of the two real beat sheets in this repo
  (`videos/kbeauty-label-trap/03-beat-sheet.json`,
  `videos/hyaluronic-acid-vs-filler/03-beat-sheet.json`) can be compiled
  yet.** Both predate this WO's `component`/`slots` fields and use
  free-form `layout` values (`three-lane`, `hero-left`, `split-compare`)
  that map onto no SeoulHabit component. This was flagged as a known
  conflict in the plan before any code was written; it is restated here as
  still true, not newly discovered.
- **T4's audio graph is not implemented.** `04-assets` audio is copied and
  referenced as a plain `<audio>` element if present; the `hf-audio-group`/
  `data-fx-chain`/`data-fx-carve`/`data-automation` mixing graph from
  `videos/collagen-where-did-it-go/scripts/build_index.py` is explicitly
  T4 scope and was not ported here.
- **The `staysInFrame` assertion kind is not emitted at all**, unlike the
  real generator's own sidecar. This is a real simplification, not an
  oversight I'm hiding: applying it correctly needs per-beat geometric
  reasoning the current compiler doesn't do, and adding a placeholder
  assertion that doesn't mean anything would be worse than omitting it.
- **Whether the "add a stage-level float when nothing else provides
  motion" fallback reads as intentional rather than filler** is a design
  judgment call, not something `hyperframes check`'s numeric gates can
  confirm. It passes every automated check; whether it looks *right* is
  for whoever reviews the actual frames.

## Judgment calls made

- **Rescoped tokens from `:root` to `#root` without first trying `:root`
  against a real render.** Justified because the working, three-projects-
  shipping precedent already avoids `:root` entirely — reproducing a
  pattern already proven to work when the two candidates are otherwise
  identical is the smaller risk than testing an unproven one first.
- **Added a synthetic continuous-motion fallback at the render layer**
  rather than hand-authoring a float/sweep for every one of the twelve
  components. This keeps individual emitters describing content, not
  motion-gate compliance, and is stated explicitly in the code's own
  comment as a compiler responsibility, not a per-component afterthought.
- **Did not attempt to port `staysInFrame`** rather than emit a
  best-effort version that might assert something untrue.

## Not done (correctly out of scope for T3, named for T4)

The D5 split path proven against a real render; the four unexercised
emitters proven the same way; a beat-sheet schema migration (or adapter)
so the two real repo beat sheets can compile; the audio mixing graph;
The other four gaps named above (D5 split proof, four unexercised
emitters, beat-sheet schema migration, audio mixing graph) remain open for
T4/a follow-on pass.
