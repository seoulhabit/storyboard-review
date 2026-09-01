# Storyboard — Peeling Question Open ("A Question We Marked Open" pilot)

25.000s, 1080×1920, 30fps. Silent (no VO). Six scenes, hard cuts throughout
except the loop-adjacent 05→06 boundary (same ground, still cut hard — see
note there). Grounds alternate `--moss` / `--ink-soft` so every real boundary
is a safe hard cut per *Cuts vs crossfades*; scene 6 returns to scene 1's
`--moss` ground so the 25s→0s loop hands back cleanly.

Mean scene length 4.17s — well under the ~9.6s ceiling `REPORT.md` sets, and
every scene's cadence design below spreads real beats across its FULL
duration rather than clustering in the first 2s, per the static-hold gate.

## Scene map

| # | id | start | dur | ground | layout |
|---|---|---|---|---|---|
| 1 | `01-question` | 0.000 | 1.800 | `--moss` | full-bleed frosted panel, peeling sheet |
| 2 | `02-answer` | 1.800 | 3.200 | `--ink-soft` | centered stamp card |
| 3 | `03-reaction` | 5.000 | 5.000 | `--moss` | two-column split |
| 4 | `04-evidence` | 10.000 | 5.000 | `--ink-soft` | asymmetric label + body |
| 5 | `05-boundary` | 15.000 | 5.000 | `--moss` | two-state card pair |
| 6 | `06-open` | 20.000 | 5.000 | `--moss` | centered lockup, matched to scene 1 |

## Scene 1 — `01-question` (0.000–1.800s, ground `--moss`)

**Spatial plan:**
- Full-bleed flex column, `justify-content: flex-end` — the frosted glass panel
  fills the upper ~70% of the canvas, headline sits low in the safe column.
- The panel is one `.glass-panel` flex child; the peeling sheet is a second,
  absolutely-positioned layer *inside* that panel's own stacking context (the
  one sanctioned use of `position:absolute` — a motion layer, not a layout
  relationship).
- Headline is two stacked `.h-line` spans in a flex column beneath the panel,
  not independently positioned.

**Beats:**

| t | element | property | from → to | dur | ease |
|---|---|---|---|---|---|
| 0.00 | `#panel` | opacity, scale | 1, 1 (resting — composed at t=0) | — | — |
| 0.00 | `#peel-sheet` | clipPath | `inset(0 0 42% 0)` (already mid-peel at frame 0) | — | — |
| 0.00–1.80 | `#peel-sheet` | clipPath | `inset(0 0 42% 0)` → `inset(0 0 68% 0)` | 1.80 | `none` (linear, continuous — the scene's own gap-filler) |
| 0.00–1.80 | `#peel-sheet` | rotationY, transformPerspective | 8deg → 14deg, perspective 900 (curl deepens) | 1.80 | `none` |
| 0.30 | `#h-line-1` ("If it peels,") | opacity, y | 0,10 → 1,0 | 0.35 | `power2.out` |
| 0.85 | `#h-line-2` ("it works?") | opacity, y | 0,10 → 1,0 | 0.35 | `power2.out` |
| 1.10–1.80 | `#peel-sheet` | filter (drop-shadow) | 0 → 6px (lift reads more) | 0.70 | `power1.inOut` |

Frame 0 is composed: the sheet is already visibly mid-peel (not starting flat),
so the hook's visual claim reads instantly on the scroll-stop frame. The
continuous clip-path + rotationY sweep is the scene's cadence gap-filler — real
pixel change across the full 1.8s, not just the text beats.

**Mechanism (peel):** `clip-path: inset()` and `rotationY` are both proven in
shipped, rendered projects in this repo (`madecassoside-clinical-cut`,
`mugwort-healing-herb`, `snail-mucin-medical-secret` — all have real render
output using these exact GSAP-tweened properties), so this is not new
render-safety risk. A static `mask-image: linear-gradient(...)` (not tweened —
matching `centella-cica-vs-snail-mucin`'s proven static-mask pattern) fades the
sheet's trailing edge to translucent, so the curl reads as thin film rather
than an opaque flap.

**SFX:** `glass-clink.mp3` at t=0.05 (very short, under the panel's settle) +
`whoosh-soft-question-to-headline-wipe.mp3` at t=0.30 (under h-line-1).

## Scene 2 — `02-answer` (1.800–5.000s local 0–3.200s, ground `--ink-soft`)

**Spatial plan:**
- Single centered flex column, full canv, `align-items:center; justify-content:center`.
- The stamp card is one flex child (`.stamp-card`), its two text lines
  (`SHORT ANSWER:` / `NO.`) stacked inside it as their own flex column — not
  independently positioned.
- A thin `--leaf` rule beneath the card is a third flex child, not an
  absolutely-positioned decoration.

**Beats (local t, scene starts at global 1.800):**

| t | element | property | from → to | dur | ease |
|---|---|---|---|---|---|
| 0.00 | `#stamp-card` | opacity, scale | 0, 1.35 (baseline — must be `tl.set(...,0)` since hit twice) | — | — |
| 0.15 | `#stamp-card` | opacity, scale, rotation | 0,1.35,-3deg → 1,1,0deg | 0.16 | `power2.in` (accelerating-in = impact, not reveal) |
| 0.15 | *(SFX)* | `paper-stamp-thump-the-myth-stamp-landing.mp3` | — | — | — |
| 0.31–0.55 | `#stamp-card` | scale | 1 → 0.98 → 1 (settle wobble, bounded) | 0.24 | `power1.inOut`, yoyo, repeat:1 |
| 0.60 | `#rule` | scaleX | 0 → 1 | 0.30 | `power2.out` |
| 1.20–3.20 | `#stamp-card` | rotation | 0 → 0.6deg → 0 (idle drift, bounded) | 2.00 | `sine.inOut`, yoyo, repeat:3 |
| 2.40 | `#micro-label` ("a claim, not a scorecard") | opacity | 0 → 0.7 | 0.30 | `power2.out` |

Payoff lands at **global t≈1.95s** (0.15s local) — inside the ≤2s retention
window, which is why scene 1 is trimmed to 1.8s rather than the brief's clean
2.0s. The bounded idle rotation drift from 1.2–3.2s is the gap-filler for this
scene's back half — real, small, resolves inside the scene (never infinite).

**ADDED 2026-09-01 (QC-verification round):** a continuous cadence-floor
zoom (`#zoom`, scale 1→1.02 over the full 3.200s, `ease:"none"`), same
derived-token pattern as scenes 4/5 — this scene's own per-region scan
already measured only a 0.50s hold (under the 1.5s ceiling), so this is
added hardening, not a fix for a measured defect, bringing scene 2 in line
with the rest of the piece rather than leaving it the one scene with no
ambient motion under its beats. No such addition was made to scene 6 — see
that scene's own section for the documented reason.

## Scene 3 — `03-reaction` (5.000–10.000s, ground `--moss`)

**Spatial plan:**
- CSS Grid, two equal columns (`grid-template-columns: 1fr 1fr`), a vertical
  divider as a grid line, not an absolutely-positioned bar.
- Left column: "Peeling is a reaction." Right column: "Not proof of results."
  Each column is its own flex sub-column (icon/word + supporting line).
- `REACTION ≠ RESULT` sits as a full-width grid row beneath both columns,
  centered — the one structurally distinct beat that makes this scene read as
  a split, not a centered stack (this is the "two-column split" layout-variety
  budget item).

**Beats:**

| t | element | property | dur | ease |
|---|---|---|---|---|
| 0.00–5.00 | `#zoom` wrapper | scale 1 → 1.03 | 5.00 | `none` (continuous gap-filler across full scene) |
| 0.20 | `#col-left` | opacity,x: 0,-24 → 1,0 | 0.35 | `power2.out` |
| 0.55 | `#col-right` | opacity,x: 0,24 → 1,0 | 0.35 | `power2.out` |
| 1.40 | `#divider` | scaleY: 0 → 1 | 0.40 | `power2.inOut` |
| 2.30 | `#eq-row` (REACTION ≠ RESULT) | opacity,y: 0,16 → 1,0 | 0.40 | `power2.out` |
| 2.75 | `#neq-symbol` (≠) | scale: 0.7,rotation:-8 → 1,0 | 0.20 | `power2.in` (small stamp-like snap) |
| 3.20–4.60 | `#neq-symbol` | scale 1 → 1.06 → 1 (bounded pulse, resolves) | 1.40 | `sine.inOut`, yoyo, repeat:3 |
| 4.60 | `#col-left`, `#col-right` | opacity: 1 → 0.55 (dim, ≠-row takes focus) | 0.35 | `power2.inOut` |

The zoom wrapper needs `--safe-*-zoomed` derived tokens (max scale 1.03,
origin center) per the mandatory pattern — no hand-tuned `+Npx` allowance.

**SFX:** `click-soft-chip-pair-lands.mp3` at t=0.20 and t=0.55 (each column
lands); a short accent (reuse `glass-clink.mp3`, trimmed via `data-media-start`
if needed) at t=2.75 on the ≠ snap.

## Scene 4 — `04-evidence` (10.000–15.000s, ground `--ink-soft`)

**Spatial plan:**
- Asymmetric: CSS Grid, `grid-template-columns: 320px 1fr` — a fixed-width
  left label column, a flexible right body column. This is the scene budgeted
  as the second structurally-distinct frame (asymmetric, not centered/split).
- Left column: the `EVIDENCE: ESTABLISHED` stamped chip, stacked above the
  citation pill, in its own flex column.
- Right column: the two body lines in their own flex column, `justify-content:center`.

**Beats:**

| t | element | property | dur | ease |
|---|---|---|---|---|
| 0.00–5.00 | `#zoom` wrapper | scale 1 → 1.025 | 5.00 | `none` |
| 0.00 | `#chip-established` | opacity,scale | baseline `tl.set(...,0)` (hit by stamp fromTo below) | — | — |
| 0.20 | `#chip-established` | opacity,scale,rotation: 0,1.3,-3 → 1,1,0 | 0.16 | `power2.in` (stamp) |
| 0.20 | *(SFX)* | `paper-stamp-thump-golden-rule-landing-de.mp3` | — | — |
| 0.75 | `#body-line-1` ("Irritation can happen.") | opacity,y | 0.35 | `power2.out` |
| 1.30 | `#body-line-2` ("More irritation doesn't mean faster results.") | opacity,y | 0.35 | `power2.out` |
| 2.10 | `#citation-pill` (`Arch Dermatol · 1995`) | opacity,y | 0.30 | `power2.out` |
| 2.10 | *(SFX)* | `click-soft-chip-pair-lands.mp3` | — | — |
| 3.00–4.80 | `#leaf-rule` (beneath the chip) | scaleX: 0.9 → 1 → 0.9 (bounded breathe, resolves) | 1.80 | `sine.inOut`, yoyo, repeat:2 |

Chip render: frosted glass base (`--capsule-dark` equivalent on this ground,
i.e. `rgba(247,245,240,0.12)` + `backdrop-filter`), ink-toned mono label,
`--leaf` rule beneath — never a filled green badge, per the evidence-vocabulary
note in BRIEF.md.

## Scene 5 — `05-boundary` (15.000–20.000s, ground `--moss`)

Adapted directly from `videos/peeling-not-progress/compositions/frames/04-boundary.html`'s
verdict-card-pair mechanism (already proven, already on this exact subject) —
mechanism reused, content and palette rebuilt for this project's green ground.

**Spatial plan:**
- Flex column: kicker row, then a flex row of two cards (`NORMAL` / `STOP`)
  with a growing divider between them (same structure as the source scene),
  then a third caveat line beneath for the prescription caveat.
- Cards are flex children of the row, not independently positioned; each
  card's own content is a flex column.

**Beats (adapted timings, `defaults:{ease:"power3.out"}` matching the source):**

| t | element | property | dur |
|---|---|---|---|
| 0.00–5.00 | `#zoom` wrapper | scale 1 → 1.025 | 5.00 (`none`) |
| 0.00 | `#kicker` ("THE BOUNDARY") | opacity | 0.30 |
| 0.15 | `#card-normal` | opacity, x: -24→0 | 0.35 |
| 0.55 | `#chip-normal` | opacity | 0.25 |
| 0.50 | `#card-stop` | opacity, x: 24→0 | 0.35 |
| 0.90 | `#chip-stop` | opacity | 0.25 |
| 1.30 | `#divider` | height: 0%→68% | 0.50, `power2.inOut` |
| 2.20–3.60 | `#stop-dot` | scale 1→1.35→1 (bounded, resolves) | yoyo, repeat:3 |
| 3.80 | `#caveat-line` ("On a prescription? Ask your dermatologist.") | opacity,y | 0.35 |
| 4.10 | `#citation-pill` (`AAD guidance`) | opacity | 0.30 |

The prescription caveat (new content vs. the source scene, required by this
brief's fuller AAD quote) fills what would otherwise be this scene's dead tail
— a real added beat, not decorative padding, addressing the plan's own flagged
risk that a 5s allocation might be generous here.

## Scene 6 — `06-open` (20.000–25.000s, ground `--moss`)

Adapted from `06-payoff.html`'s loop-endpoint pattern: centered across the
*full* canvas (not safe-anchored) so the hard cut back to scene 1 lands on a
matched hero position — measured against scene 1's panel center, not assumed.

**Spatial plan:**
- Full-canvas centered flex column (`justify-content:center`, no safe-top/
  safe-bottom padding — matching the source scene's documented exception,
  re-verified for this project's own frame 1 geometry, not copied blind).
- The "better question" line, the three-chip row (ingredient / strength /
  frequency / combination), the closing couplet, and the 습 SeoulHabit lockup
  are stacked flex children of one column.
- The chip row is its own flex row nested inside the column — not four
  independently positioned chips.

**Beats:**

*Re-derived 2026-09-01 (QC-verification round) directly from the shipped
`06-open.html`, not from memory — this table had drifted from the actual
composition (wrong element IDs, a stale lockup timestamp) well before this
round touched anything; re-sync any other scene's table the same way before
trusting it as a spec rather than history.*

| t | element | property | dur | ease |
|---|---|---|---|---|
| 0.00 | `#state-grid` baseline + `#w-1..4` baseline | `tl.set(...)`, not a bare `gsap.set()` — seek-bleed guard | — | — |
| 0.20 | `#q-lead` ("The better question:") | opacity,y | 0.30 | — |
| 0.60 | `#q-main` ("What changed?") | opacity,scale | 0.34 | `power3.out` |
| 1.05 / 1.35 / 1.65 / 1.95 | `#w-1..4` (ingredient/strength/frequency/combination) | opacity,y in | 0.26 each | — |
| 1.05 | `#q-lead`, `#q-main` | opacity out | 0.28 | — |
| 2.35 / 2.40 / 2.45 / 2.50 | `#w-1..4` | opacity,y out | 0.30 each | `power2.in` |
| 2.85 | `#state-grid` | opacity → 0 (container hide) | 0.01 | — |
| 2.85 | `#h-line-1` ("Not the claim.") | opacity,y | 0.34 | — |
| 3.15 | `.lockup` (습 SeoulHabit) | opacity,scale: 0,0.92→1,1 | 0.34 | `power3.out` |
| 3.15 | *(SFX)* | `glass-clink.mp3`, retimed with the lockup (was 4.05 pre-fix) | — | — |
| 3.30 | `#h-line-2` ("The question.") | opacity,y | 0.34 | — |
| 3.60 | `.hangul` | scale 1→1.06→1 (bounded idle, resolves before cut) | 0.25, yoyo repeat:1 | `sine`-ish (unspecified ease) |

**RETIMED 2026-09-01 (QC-verification round):** the panel sat empty from
local 2.95–4.05 (measured on the render: 1.30s of zero rendered change in
the panel box) between the word-grid's exit and the old lockup arrival at
4.05 — an external QC report misdiagnosed this as the word-grid's own
entrance being too slow (it wasn't: 0.30s apart, already tighter than the
report's 0.5s suggestion). Pulled the lockup to 3.15; the true empty window
measured on the fixed, mastered render is 0.40s (22.8s–23.1s absolute).
Captions cue 21 (`captions/peeling-question-open.srt`/`.vtt`) retimed to
match: 23.150–23.800, was 24.050–24.700.

Gate 11 (closing beat = one specific, lesson-tied action, not a generic
subscribe card) is satisfied by the chip row itself — "what changed" is
actionable audit language, not a subscribe prompt — landing before the brand
lockup, not instead of it.

**Loop:** scene 6's resting frame (from ~t=3.5 onward, `--moss` ground,
centered lockup) must be measured against scene 1's frame 0 (`--moss`
ground, centered panel) for hero-position match before this is called
done — same discipline `06-payoff.html` applied (measured to within 1px
against `01-hook.html`). No Ken Burns zoom was added to this scene despite
this round adding one to scene 2: `06-open.html`'s own spatial-plan comment
documents a deliberate reason — scene 1 never scales its content, so
scene 6 doesn't either, so neither loop endpoint moves its own frame.

Build note: the closing couplet was originally drafted as "Don't follow the
claim." / "Follow the question." — at the required 108px (byte-identical to
scene 1's `.h-line`, needed so the two scenes' `.text-stack` intrinsic heights
match and the panel's `flex:1` sizing lands on the same box), "Don't follow
the claim." wraps to two lines in the 846px-wide safe column, inflating
`.text-stack`'s height and shrinking the panel by 121px on the rendered
frame — confirmed by a pixel-column measurement, not assumed from the source.
Shortened to "Not the claim." / "The question.", which fits one line each at
the same size and preserves the claim-vs-question opposition the beat is
built on.

## Boundary policy

All five scene boundaries are hard cuts. 03→04 and 04→05 change ground
(`--moss`↔`--ink-soft`), so a cut is required, not just preferred. 01→02 and
02→03 likewise change ground. 05→06 is the one same-ground boundary
(`--moss`→`--moss`) where a ≤150ms fade would be technically safe — kept as a
hard cut anyway, consistent with the format's "stamp, don't dissolve" register.

## Audio summary

No VO bus. BGM: `assets/bgm/track.mp3` (57s source) cropped to a flat,
unfaded 25.000s region with ~200ms declick fades at each end — all envelope
shape lives in one `data-automation` lane, matching the `mugwort-healing-herb`
lesson about not compounding a source file's own baked-in tail fade with a
second automation fade. SFX cues listed per-scene above, six files total,
each with its own 60–100ms edge-fade automation.

## Cadence self-check (source-level, to be re-verified against real pixels)

Every scene's beat table above shows entries spread past the 2.5s mark, and
every 5s scene carries a continuous full-span zoom/glow tween as a floor.
This is an authoring-time estimate only — per the skill's own warning, a
source-level beat map is not proof of pixel-level cadence. `check-static-hold.py`
against the real render is the actual gate.
