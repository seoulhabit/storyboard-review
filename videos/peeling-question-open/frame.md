# Design spec — peeling-question-open

Pilot of **"A Question We Marked Open,"** a new recurring format for this
channel. Fuller context, sourcing decisions, and the four decisions locked
with the creator before build live in `BRIEF.md`; the beat-by-beat timeline
lives in `STORYBOARD.md`; the delivery manifest and verification summary live
in `DELIVERY.md`. This file is the design system reference and the full
technical account of what broke and how it was fixed.

## Design system

Palette maps onto the channel's canonical design system
(`videos/seoulhabit-launch/assets/tokens/tokens.css`), not a new one:

```
--moss:    #4F6B52   /* evidence ramp, dark -- the brief's "dark SeoulHabit green" */
--leaf:    #6F8F72   /* = --accent-evidence; also EvidenceMeter's "confirmed" fill */
--celadon: #93B896   /* evidence ramp, light */
--ink-soft:#211F1B   /* alternate dark ground */
--paper:   #F7F5F0   --ink: #131516   --mist: #F0EBE1
--coral:   #C97A5C   /* reserved: "a limit or a refusal" -- used ONCE, scene 5, fill only */
```

Contrast measured, not assumed: `--paper` on `--moss` = 5.01–5.42:1 (clears
4.5:1). `--coral` on both `--moss` and `--paper` falls well under the floor —
it is used exclusively as a small filled dot (the STOP indicator in scene 5),
never as text, so the floor doesn't apply.

**Frosted glass primitive** (from `centella-tiger-grass/compositions/frames/02-identity.html`,
proven across 7 shipped renders):

```css
background: rgba(251,249,245,0.16);
backdrop-filter: blur(25px) saturate(1.15);
-webkit-backdrop-filter: blur(25px) saturate(1.15);
border: 1px solid rgba(255,255,255,0.30);
```

Layout constants: 1080×1920, 30fps, safe area 192/384/72/162 (the current
channel standard — `mugwort-healing-herb` and `snail-mucin-recut-34s` are the
only other two projects using it; older projects use the more permissive
120/360). Type floors: hero 96–160px, body 40px min, chips/labels 32px
absolute floor.

## Fonts

Four subset `.woff2` files reused verbatim from `peeling-not-progress`: EB
Garamond 400 (display), Inter 800 (only weight registered — body copy
therefore runs in JetBrains Mono 500 instead of a lighter Inter weight,
matching `peeling-not-progress`'s own `.qualifier` convention), JetBrains
Mono 500 (labels/chips/body), Noto Sans KR 500 (the 습 glyph). The engine's
own Google Fonts auto-injection (confirmed in the `check` log — "Fetched N
font face(s)... Injected deterministic @font-face rules") supplements these;
every element using a non-400/registered weight still declares `font-weight`
explicitly so the compiler's own font-usage scan resolves the correct
variant, rather than relying on a CSS default that happens to not match any
registered face.

## Per-scene design notes

**Scene 1 — `01-question` (moss).** Frosted panel + a translucent peeling film,
built from three counter-effects sharing one timeline position: `clip-path`
reveals the panel texture beneath as the sheet appears to detach, `rotationX`
around the sheet's own bottom edge sells a 3D lift, and a static (never
tweened) `mask-image` gradient fades the sheet's trailing edge to
translucent so the curl reads as thin film, matching
`centella-cica-vs-snail-mucin/04-twist.html`'s proven static-mask technique.
`clip-path` and `rotationX` are both proven GSAP-tweened properties in this
repo's own shipped, rendered projects (`madecassoside-clinical-cut`,
`mugwort-healing-herb`, `snail-mucin-medical-secret`) — not new render-safety
risk. Frame 0 is already mid-peel (not starting flat), so the hook's visual
claim reads instantly on the scroll-stop frame.

**Scene 2 — `02-answer` (ink-soft).** A stamp-impact card: oversized
(`scale:1.35`), slightly rotated, `power2.in` accelerating-in over 0.16s —
the ThresholdList-derived "impact, not reveal" language. Fires at local
t=0.15 (absolute 1.95s), inside the ≤2s hook retention window. A qualifying
sub-line ("Not the way most people mean it.") was added to soften the
otherwise-absolute "NO." — an unqualified flat no is a stronger claim than
scenes 4/5's actual citations support, and it also fills the back half of
this scene honestly rather than with idle motion alone.

**Scene 3 — `03-reaction` (moss).** Horizontal split (REACTION field / seam /
RESULT field) — deliberately horizontal rather than vertical, so it doesn't
read as a re-skin of the catalog's `SplitCompare` component (a vertical
bisector). The RESULT field's own argument is rendered visually, not just
stated: five tick marks accumulate in the REACTION field, then dim, while an
empty dashed outline (the "void") draws into the RESULT field — the reaction
side visibly generates evidence of itself while the result side stays
literally empty. This 1.0s stroke-draw is also the scene's real content beat
for a duration budget that would otherwise be padded.

**Scene 4 — `04-evidence` (ink-soft).** Asymmetric: a fixed content column
plus a narrow vertical `writing-mode: vertical-rl` rail reading "EVIDENCE" —
the second structurally-distinct frame this project's layout-variety budget
requires (full-bleed/centered scenes 1/2/6, split scene 3, asymmetric+rail
scene 4, card-pair scene 5). The evidence badge reuses scene 2's stamp
language at a smaller scale — a visual echo, not a second payoff, paired
deliberately with a quieter/shorter SFX file. The dose-response row (1×/2×/3×
chips over three bars filled to the *same* height) renders the claim "more
irritation doesn't mean faster results" as an image, not just a sentence —
the beat most likely to be screenshotted, and this project's answer to a
duration allocation that the copy alone doesn't fill honestly.

**Scene 5 — `05-boundary` (moss).** Directly adapted from
`peeling-not-progress/compositions/frames/04-boundary.html`'s two-card
verdict-pair mechanism — already proven, already on this exact subject.
Content and palette rebuilt for the green ground; the STOP dot uses coral
(this project's one and only use of that accent, matching its semantic role
as "a limit or a refusal") with a paper ring for definition, the same fix
`brand/channel/README.md` records for a coral watermark disappearing over a
similar mid-value ground. The prescription caveat ("On a prescription? Ask
your dermatologist.") is new content the source scene didn't need — required
by this brief's fuller AAD quote, and it fills what would otherwise be the
scene's dead tail with a real beat rather than decorative padding.

**Scene 6 — `06-open` (moss, matches scene 1's ground for the loop).** Adapted
from `06-payoff.html`'s loop-endpoint pattern: the `.stage`/`.glass-panel`
shell is byte-identical to scene 1's (see *Loop geometry* below for why this
had to be verified, not assumed). Three content states layer inside the
panel — the lead question, a four-word grid (ingredient/strength/frequency/
combination), then the 습 SeoulHabit lockup — each an absolutely-positioned
child of the panel's own stacking context, the same "layered motion planes"
idiom scene 1 uses for its texture/peel-sheet pair. The word grid is the
beat that satisfies the "closing action, not a generic subscribe card" gate:
it names the actual audit checklist, landing before the brand lockup, not
instead of it.

## Post-render review fixes (round 1)

Three real defects, found by extracting and eyeballing actual rendered
frames — `npx hyperframes check` passed cleanly at every point and caught
none of them, consistent with this repo's documented history of `check`
reporting 0 issues on genuinely broken renders.

### 1. Void-box reveal rendered fully drawn from frame zero (scene 3)

**Symptom.** The empty "result" outline (`#result-void`, meant to stay hidden
via `stroke-dasharray`/`stroke-dashoffset` until a 1.00s reveal at local
t=2.45s) rendered as an essentially-complete outline from the scene's very
first frame, static for the entire scene.

**Root cause.** The initial `stroke-dasharray`/`stroke-dashoffset` state was
set via a bare `gsap.set(voidRect, {...})` call *outside* the GSAP timeline.
This is the same failure class the skill documents for an element hit by
multiple `fromTo()` calls at different positions ("a bare `gsap.set()` call
outside the timeline does not fix this... it's not part of what the timeline
itself evaluates on a seek") — generalized here to a single `.to()` reveal
whose *starting* state depended entirely on that out-of-band call. A `.to()`
tween (unlike `fromTo()`) never explicitly sets a "from" value, so before its
own start time the property is governed by whatever was set outside the
timeline — which this render pipeline does not reliably honor under an
arbitrary seek.

**Fix, two parts.**
1. Moved the dasharray/dashoffset initialization to `tl.set(voidRect, {...}, 0)`
   — inside the timeline, at position 0.
2. Separately switched the shape from an SVG `<rect rx="14">` to an
   equivalent `<path>` with an explicit rounded-rect `d` string, matching
   `peeling-not-progress/01-hook.html`'s proven `getTotalLength()` pattern,
   which uses `<path>` elements exclusively — a `<rect>`'s `getTotalLength()`
   support was a secondary suspect not fully ruled out, and `<path>` is the
   established-safe choice in this exact codebase regardless.

**Verification.** A 9-frame composite spanning the full scene (t=5.0 through
9.9, local 0.0 through 4.9) confirms: hidden through local t=2.00, a small
dash appears at local 2.00–2.30, progressively lengthens through local
2.50–2.80, and is fully drawn and stable from local 3.20 onward — matching
the authored 2.45→3.45 reveal window within the 0.5s sampling grid used for
the composite.

**Consequence for scene 1.** `#peel-sheet` in `01-question.html` shares the
exact same risk shape (bare `gsap.set()` initial state, then two further
`.to()` calls) and happened to be rendering correctly on inspection — but
rather than leave a latent risk once the mechanism was understood, its
baseline was defensively moved into `tl.set(..., 0)` too.

### 2. A decorative rule rendered ~90% drawn from frame zero (scene 4)

**Symptom.** `.badge-rule` (a thin leaf-green rule meant to grow in beneath
the `EVIDENCE: ESTABLISHED` badge, entrance tween at local t=0.42) appeared
almost fully drawn at the scene's very first frame — before the badge itself
had even stamped in.

**Root cause.** `.badge-rule`'s CSS default was `transform: scaleX(0.9)`
instead of `scaleX(0)` — a copy-paste residue from drafting, not an
intentional resting state.

**Fix.** Corrected the CSS default to `scaleX(0)`, and additionally
registered `tl.set('#badge-rule', { scaleX: 0 }, 0)` inside the timeline,
since this element is hit by two tweens (the entrance at 0.42 and a later
breathing pulse at 3.20) — the same defensive discipline applied after
defect #1.

**Verification.** Re-extracted t=10.000 (scene 4's local t=0.00): only the
always-visible dose-track backgrounds are present; the badge, its text, and
the rule are all correctly absent until their own entrance beats.

### 3. The loop's hero panel didn't geometrically match scene 1 (scene 6)

**Symptom.** A pixel-column measurement of the panel's bottom edge (the
loop's actual acceptance criterion, not an eyeballed comparison) showed
scene 6's panel ending well past scene 1's frame-0 panel — first measured at
a 38px mismatch, then, after an initial fix, a 121px mismatch.

**Root cause, in two layers.**
1. Scene 6's `.h-line` originally used a different font-size/line-height
   (96px/1.16) than scene 1's (108px/1.12). Since `.text-stack` has no fixed
   height and `.glass-panel` is `flex:1` in the same `.stage` column, any
   difference in the text-stack's intrinsic height changes how much space
   the panel auto-expands into.
2. Making the font-size byte-identical *still* left a 121px mismatch,
   because the closing couplet's first line — "Don't follow the claim." at
   108px — wraps to two physical lines inside the 846px-wide safe column,
   inflating `.text-stack`'s real rendered height well beyond what the
   matching CSS alone would suggest.

**Fix.** Matched `.h-line`'s font-size/line-height exactly to scene 1's
(fixing layer 1), then shortened the closing couplet to "Not the claim." /
"The question." — short enough to fit one line each at the same size, while
preserving the claim-vs-question opposition the beat is built on (fixing
layer 2).

**Verification.** A naive whole-column pixel scan initially reported a
*further* mismatch after the font-size fix (scene 6 appearing *taller* than
scene 1) — this was a measurement artifact, not a real regression: scanning
a full column can't distinguish "panel pixel" from "couplet-text pixel"
landing at the same x-coordinate once the panel and the text below it are
both non-background-colored. The fix was to measure only the *first
contiguous* non-background run per column, starting from the known safe-top
y-position — isolating the panel from any content beneath it. Under that
corrected method, scene 1 frame 0 and scene 6's resting frame both measure
panel top=192, bottom=1201, at every tested x-column (120, 300, 500, 800) —
an exact pixel match, not an approximate one.

## Verification loop, full account

See `DELIVERY.md`'s *Verification record* for the QC script results and the
blank-frame advisory findings (four, all legitimate reveal-beat gaps,
confirmed by direct frame inspection). This file's account above covers the
three defects that required a source-code fix; nothing else did.

This render was produced with `PRODUCER_FORCE_SCREENSHOT=true`. The render
log for the very first spike (single-scene, before this env var was set)
reported `"captureMode":"beginframe"` on this macOS machine — contradicting
a direct read of `hyperframes@0.8.20`'s own bundled `dist/cli.js`, whose
capture-mode selection logic gates `beginframe` to
`headlessShell && process.platform === "linux"`. Not fully root-caused (this
machine reports Darwin per its own environment info), but the escape hatch
reliably forces the `screenshot` capture path, and every fix above was
verified against a `screenshot`-mode render, not a `beginframe`-mode one.
Re-verify the active capture mode on any future render of this project via
the render log's own `captureMode` field, rather than assuming the platform
alone determines it.
