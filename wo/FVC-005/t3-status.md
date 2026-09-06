# T3 — Compiler build — DONE, all nine scene emitters adversarially stress-tested and the D5 split path proven; a serious universal defect (blank endcard flash) found and fixed
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

## Seventeen real bugs found, plus one confirmed clean combination, one confirmed check-tool limitation, and one real design-system finding surfaced by a repo gate the plan named but this pass had skipped

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

6. **The split algorithm never accounted for the scene's own end.**
   Given the exact case `COMPILER.md` had already named as load-bearing
   (`ShRows`, three beats at offsets 0.0/2.0/4.0, derived duration 6.3s
   against a 5.0s ceiling), the first D5 implementation **died** —
   `"6.300s still exceeds the 5.0s ceiling after splitting -- beats too
   widely spaced to partition further"` — a genuinely misleading message,
   since the three beats span only 4.0s. The real problem was the scene's
   trailing hold *after* the last beat, which `split_beats_by_ceiling`
   never looked at: it only checked each group's own beat-to-beat span,
   never the group's true effective duration once a scene's actual end is
   considered. Fixed by passing the function `scene_end` (`D_raw`)
   explicitly and peeling beats off the back of the final group until what
   remains fits against it.
7. **Splitting timing did nothing to content.** After fixing bug 6, both
   compiled halves of the same fixture rendered the *identical, complete*
   3-row list — found by grepping the actual compiled HTML, not assumed.
   `plan_scene` passed every split group the scene's full, unsliced
   `slots`. Fixed by adding `split_slots_for_group()`: only components with
   a natural per-beat list slot (`ShRows.rows`, `ShSteps.steps` — the only
   two) can split content automatically, slicing `items[lo:hi]` to each
   group's own beat-index range and relocating `ShRows`'s `active` index to
   the containing group's local index (or `-1` if it landed elsewhere).
   Every other component refuses to split rather than guess at a division
   with no defined meaning.

8. **`ShCompare`'s two-column grid let a wide header overflow the canvas.**
   `check` found a real `canvas_overflow` warning: `"THD ascorbate"`
   extending 94.6px past the right edge, held across the scene's full
   visible window (16 occurrences). Root cause: `grid-template-columns:1fr
   1fr` still respects each grid child's default `min-width:auto`,
   refusing to shrink below the unwrapped text's own width — a standard
   CSS grid trap, and one the source JSX has too (this is not a porting
   error, it's a real defect the design system's own component would hit
   on a real render). Fixed by adding `min-width:0` and
   `overflow-wrap:break-word` to every grid child.
9. **The continuous-motion fallback trusted one-shot markers it shouldn't
   have.** `ShQuote`'s 3.2s scene tripped `motion_frozen` — the fallback
   (from this WO's earlier D5 session) treated `sweep`/`count` as
   equally sufficient to `float`, but both are one-shot: they play once
   and stop, saying nothing about whether motion continues for the rest
   of an arbitrarily long scene. The bug had been latent since it was
   written — it happened to pass on `ShHook`'s shorter 2.4s scene by
   coincidence of duration, not because the check was actually correct.
   Fixed by trusting only `float` (which spans the full scene duration by
   construction) to suppress the fallback.

10. **`ShIngredient` had the same defect class as `ShCompare`'s grid
   overflow, through flexbox instead of grid.** Tested deliberately with
   a real, unbreakable 24-character INCI term
   (`"Polymethylsilsesquioxane"`) rather than waiting for it to surface
   by accident. `#cid-name` grew to **1895.89px — nearly double the
   1080px canvas** — because `text-wrap:balance` only balances line
   lengths once wrapping already happens, and `#cid-wrap`'s default
   flex-item `min-width:auto` refused to shrink below that unbreakable
   text's own min-content width. Fixed with `min-width:0` on the flex
   column plus `overflow-wrap:anywhere` (not the legacy `break-word`,
   which does not change an element's min-content contribution the way
   `anywhere` does — that distinction is the reason `min-width:0` alone
   would not have been enough) on every text child.
11–16. **The same overflow defect class, confirmed in all six of the
   remaining emitters** (`ShHook`, `ShRows`, `ShSteps`, `ShEvidence`,
   `ShMyth`, `ShQuote`) by one combined adversarial-text fixture stressing
   all seven not-yet-tested emitters at once. `ShHook` and `ShMyth` had an
   additional structural variant: an `inline-block` wrapper whose
   shrink-to-fit sizing makes `max-width:100%` on its own child circular,
   fixed by switching to `display:block`. Every other case was the same
   missing `min-width:0`/`overflow-wrap:anywhere` pair already found
   twice. `ShEndcard`'s `cta` was fixed defensively too (didn't fail this
   specific fixture's content, but had the identical structural gap).
   Full account, including why each one is structurally the same class of
   bug: `wo/FVC-005/t3-verification/stress7/README.md`.
17. **Far more serious: every compiled video's closing scene opened with
   a ~0.17s completely blank flash — confirmed on every single video this
   compiler could ever produce, not a rare case.** Root cause: `ShEndcard`'s
   three elements all use the standard delayed entrance, which is fine
   everywhere else because every other scene also has a citation chip
   rendering immediately and bridging the gap — confirmed by direct
   inspection that all six of the design system's own templates give the
   closing scene, and *only* the closing scene, no chip. Found by exact
   frame-by-frame pixel-variance analysis (frames 702–706 of 774,
   perfectly uniform, zero variance), not by trusting the `check` tool's
   summary alone. Fixed by extending the compiler's existing
   compose-immediately rule (previously applied only to the video's
   overall first scene) to any scene with no chip to bridge the entrance
   gap. One residual `check --at-transitions` finding
   (`content_overlap`/`text_occluded` on the quote scene, exactly at the
   hard-cut instant) was investigated with real extracted frames — both a
   mid-scene frame and the actual boundary frame are clean — and is
   recorded as a check-tool sampling artifact at hard-cut boundaries, not
   a defect, per `wo/FVC-005/t3-verification/stress7/README.md`.
18. **No new bug — a genuine, informative negative result, and a
   refinement of finding 17's artifact.** Tested the D5 split path and
   the adversarial-text overflow fixes together for the first time (a
   `ShRows` scene as the video's own frame zero, and a `ShSteps` scene
   mid-video, both split, both loaded with the same unbreakable INCI
   term). Every independently-verified fix held up in combination: split
   content slicing carried the overflow guards correctly, frame-zero
   suppression applied only to the first compiled sub-scene of a split
   first scene, and the blank-endcard fix held after a split scene
   precedes the endcard. The known artifact from finding 17 recurred —
   this time on a `ShSteps` split sub-scene transitioning into the
   endcard, not a `ShQuote` scene — which sharpens the diagnosis: the
   common factor across both occurrences is that the *incoming* scene is
   always `ShEndcard`, the only component that is both `anchor: true`
   (getting an explicit `opacity:1` on its own `#root`) and structurally
   chip-less, not anything about the outgoing scene or about splitting.
   See `wo/FVC-005/t3-verification/d5-adversarial/README.md`.
19. **Not a bug — the recurring endcard-transition artifact's exact
   mechanism, confirmed against the installed engine's own source rather
   than left as an inferred pattern.** Read `hyperframes@0.8.30`'s
   `dist/cli.js` directly: `check --at-transitions` samples layout via
   `window.__player.renderSeek()`, a generic scrub-seek API also used by
   the interactive Studio preview, not the frame-capture pipeline. Live
   binary-search against a running instance of the `stress7` fixture
   confirmed that API leaves the outgoing scene's `.clip` visible for
   exactly one extra frame (~33ms) past its own `data-duration` end when
   the *incoming* scene is `ShEndcard` — reproducing the finding — while
   the other five hard cuts in the same composition show zero lag. A real
   `hyperframes render` PNG-sequence at 30fps, inspected frame-by-frame at
   the exact reported times (`23.400`, `23.432`), is completely clean:
   the frame-capture pipeline does not share the scrub-seek path's lag.
   Conclusion: this is a `check --at-transitions` measurement limitation
   specific to hard cuts into chip-less/`anchor:true` scenes, not a
   compiler defect and not present in any actually rendered frame. No
   code change follows. Full source citations, the live-page verification,
   and the decisive rendered frames are in
   `wo/FVC-005/t3-verification/artifact-mechanism/README.md`.
20. **A real gap in the plan's own Step 10 ("Repo gates"), found and closed
   by re-reading the plan against what had actually shipped — and a real,
   consequential finding once it was run.** `check-legibility.py` and
   `check-safe-area.py` were named in the approved plan (per D6) but never
   run against the compiled output, and not named in this file's own "Not
   verified" section as a deliberate deferral either — a silent omission,
   not a declined check. Running them now: the token-floor half of
   legibility passes both canvases (`--t-chip` lands exactly on the floor
   in both, 28px/24px, no margin); the render-based half **fails 16:9**
   (`--t-chip` measures 4px glyph height at phone scale against a 5px
   floor, confirmed on two independent probes) while 9:16 passes with zero
   margin (exactly 5px). `check-safe-area.py` **fails both canvases** —
   measured precisely on the actual worst-case frames, not accepted from
   the JSON: `ShRows`' right-aligned values sit 57px inside YouTube
   Shorts' real reserved UI rail on 9:16, and the citation chip sits mostly
   inside the real reserved bottom zone on 16:9. Root cause, confirmed on
   pixels: **the compiler is not at fault** — it correctly implements
   `videos/_system/tokens/spacing.css`'s own `--safe-x: 10%` /
   `--safe-bottom: 8%` exactly as declared. Those declared margins
   themselves are narrower than the real platform UI they're meant to
   clear (15%/10% respectively). This is a T2 (design-system) finding
   surfaced by a T3 gate, not a T3 defect, and not something to patch
   unilaterally inside the compiler — see
   `wo/FVC-005/t3-verification/repo-gates/README.md` for the full
   measurements and the tradeoff either fix requires.

## Accept check — what's verified and what isn't

**Verified:**
- The plan's Step 10 repo gates (`check-legibility.py`, `check-safe-area.py`)
  are now run against real compiled+rendered output on both canvases — see
  finding 20 and `t3-verification/repo-gates/`. "Run" here does not mean
  "clean": legibility passes both canvases' declared floor and 9:16's render
  check, fails 16:9's render check; safe-area fails both canvases, root-
  caused to T2's own safe-margin token values, not to the compiler.
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
- ~~The D5 split path has not been exercised against a real render.~~
  **Now verified** — see the two new bugs (6, 7) below and
  `wo/FVC-005/t3-verification/d5-split/`.
- ~~`ShCompare`, `ShMyth`, `ShQuote`, `ShSteps` have not been exercised
  through a real compile.~~ **Now verified, all nine of nine emitters** —
  see bugs 8–9 below and `wo/FVC-005/t3-verification/four-emitters/`.
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
