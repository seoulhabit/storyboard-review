# Frame — peeling-not-progress

## Canvas

1080×1920, 30fps. Safe areas (the design system's `--short-*` 9:16 lane, read by
**every** scene, not just declared): `--safe-top: 120px` / `--safe-bottom: 360px` /
`--safe-left: 60px` / `--safe-right: 162px`. Scene 1's title stack sits at
`calc(var(--safe-top) + 130px)` — plain `--safe-top` lands inside Shorts' ~192px top UI
zone (a real fix already made twice elsewhere in this repo). Settled frames fill
65–80% of the vertical safe column; no scene is a single centered line in empty canvas.

## Channel audit (reuse basis, not re-derived)

Per `faceless-video-craft`'s "Consistency across a channel's videos," these are copies
of channel sources of truth, verified with `git ls-files` before use — not re-derived:

- Tokens: `videos/seoulhabit-launch/assets/tokens/tokens.css`, verbatim.
- Fonts: `videos/centella-cica-vs-snail-mucin/assets/fonts/*.woff2` (Inter 800, EB
  Garamond 400, JetBrains Mono 500, NotoSansKR-500-subset).
- QA scripts (all three gates): `videos/glass-skin-5-habits/scripts/`.
- `CLAUDE.md` / `AGENTS.md`: byte-identical across all 18 prior projects; copied as-is.
- `hyperframes.json`: copied verbatim, `authoringSkill: faceless-explainer`.
- CLI pinned to `hyperframes@0.8.17`, matching the two newest projects.

**What this project does NOT inherit, deliberately:** the `<hf-audio-group>` VO bus and
its `data-fx-chain` — there is no voiceover. No `SCRIPT.md`, no `assets/voice/`, no
caption sub-composition — the kinetic type is authored directly, not derived from a
transcript.

## Palette

Base five: `--paper: #F7F5F0`, `--ink: #131516`, `--aqua: #59B8AE`,
`--leaf: #6F8F72`, `--coral: #C97A5C`. Hard laws, inherited: exactly one aqua-family
highlight per frame; **coral is the video's single voltage moment, spent once, in
Frame 2's strike** (see § Content corrections for why Frame 4 does *not* also get
coral, despite `retinol-patch-test`'s source scene using it there). No success color —
aqua marks "cited," never "passing."

| Frame | Ground | Notes |
|---|---|---|
| 1 hook | ink | droplet/surface in ink-appropriate tones (paper-colored surface on ink ground) |
| 2 overload | paper | coral spent here |
| 3 truth | ink | signature component (barrier wall) |
| 4 boundary | paper | aqua on the left/NORMAL card only |
| 5 reset | paper | three objects, aqua reserved for chips |
| 6 payoff | ink | matches Frame 1's ground for the loop |

## Type

`--font-display` (EB Garamond) for headline claims, `--font-body` (Inter) for
kickers/labels, `--font-mono` (JetBrains Mono) for citation chips and mono qualifiers.

**Reading type floor: 40px**, not the design system's `--t-floor: 20px`. That token
applies only to decorative/citation micro-type; `glass-skin-5-habits/frame.md` already
rejected a 33px compromise as missing the mobile reading floor. Every headline/body line
in this project is authored at ≥40px.

**SUPERSEDED 2026-08-31 — the 22px chip exception below no longer holds.** This
section originally read: "Citation chips are the sanctioned exception — `--t-chip:
22px` mono, matching every other project's chip treatment; their job is to signal
*sourced*, not to be read at arm's length." Two things changed that reasoning: (1)
`faceless-video-craft` SKILL.md's update set 32px as the absolute floor for anything a
viewer is meant to actually read, with no signal-only carve-out; (2) this project's own
citation pills were converted from raw catalog IDs (`PMID 7544967`) to human-readable
text (`Arch Dermatol · 1995`, see § Sourcing and § Post-render review fixes round 5) —
which makes them something a viewer *is* meant to read, not a decorative mark whose
exact text doesn't matter. Chips now ship at 32px (`--t-chip`, raised in
`assets/tokens/tokens.css`), matching the label floor exactly.

## Faceless

No talking-head footage, no visible faces, no `assets/avatar/` directory — the channel's
standing rule. Every visual in this project is browser-drawn SVG/CSS; there is no
photography to check against the no-faces constraint in the first place.

## Media exception — none needed

Unlike `ceramides-skin-barrier` and `glass-skin-5-habits`, this project files **no**
generative-imagery decision record. Every beat (droplet, fracture, bottles, barrier
wall, evidence cards, three objects, lockup) is SVG/CSS authored in-composition, which
is the `seoulhabit-video-3d` skill's stated default ("Browser-drawn only… No generative
imagery, ever" — quoted at `catalog/ingredients/one-percent-line/README.md:113`), not an
exception to it.

## Motion

`--e-out: cubic-bezier(0.215, 0.61, 0.355, 1)` default ease throughout. No
bounce/elastic/back easing, no infinite keyframes — idle motion (Frame 4's alert-dot
pulse, Frame 5's slow scale) is finite and resolves inside its own scene's duration.
Hard cuts at every ground change (1→2, 2→3, 3→4, 5→6); the sole exception is 4→5
(paper→paper, no ground change), which gets a ≤150ms same-ground fade per
`faceless-video-craft`'s cuts-vs-crossfades rule. Cadence target: a state change every
1.5–3s across each scene's *entire* duration — Frames 3, 4 and 5 (6s each, the longest)
each carry 5–7 internal beats, not 2–3 clustered at the open. Full beat-by-beat timing
is in `STORYBOARD.md`.

## Elevation

**Glow banned outright** — no `box-shadow: 0 0 …` / `drop-shadow(0 0 …)` anywhere,
matching every project on this channel. `--elev-1` hairline seat under chips,
`--elev-2` lift under the evidence cards and the three reset objects.

## Brand anchor

습 SeoulHabit text lockup (Noto Sans KR 500), Frame 6 only, centered — not
bottom-safe like most prior projects, because Frame 6 is this video's loop frame and
needs to match Frame 1's centered hero position for the hand-back to read as seamless.
`catalog/marks/` has no SeoulHabit mark (only PDRN, ginseng, ingredient-generic, and an
unrelated "Fold & Spark" exploration its own README says is *not* tied to SeoulHabit) —
the real lockup is type, copied from
`videos/glass-skin-5-habits/compositions/frames/06-cta-endcard.html`.

## Audio mix

**No VO bus.** No `<hf-audio-group>`, no `data-fx-chain`, no `data-fx-carve` — there is
nothing to duck music under, which is the one place "silent" changes the channel's
usual recipe (see BRIEF.md § Customizations).

- **BGM**: `assets/bgm/track.mp3`, reused verbatim from `videos/retinol-patch-test/`
  (57s source file, `data-duration` capped to the composition's 30s — the same
  cap-don't-trim pattern `centella-cica-vs-snail-mucin` uses on its own 57s bed against
  a 30.28s composition). **Plateau raised well above the channel's usual
  `data-volume="0.12"`**, which is tuned for sitting *under* a voice — here BGM is the
  only sustained audio, and copying 0.12 verbatim would reproduce the channel's own
  documented "BGM sounds like dead silence" defect (measured −48.9dB in a narration gap
  on `seoulhabit-launch` before that project's fix). Actual plateau value set by
  measuring the mastered render's RMS in a window with no SFX active, not chosen by eye
  — recorded in `DELIVERY.md` once rendered.
- **SFX**, all reused from existing channel assets, none newly generated:

  | Cue | Source project | Beat | Trim |
  |---|---|---|---|
  | `droplet-tick.mp3` | `glass-skin-5-habits` | F1 droplet arrival | full (0.31s) |
  | `whoosh-soft-myth-bust-cut.mp3` | `snail-mucin-medical-secret` | F1 crack-draw | full (1.06s) |
  | `sharp-text-stamp-impact-hit.trimmed.mp3` | `ceramides-barrier-diagnostic` | F2 coral strike | full (1.1s, pre-trimmed) |
  | `wall-crumble-crack-collapse.mp3` | `ceramides-barrier-diagnostic` | F3 shard-detach | capped ~2.2s of the 5.39s file — the source project's own scene is 8.6s and plays it near-full; this project's Frame 3 is 6s, so it's capped via `data-duration`, not re-encoded |
  | `click-soft-chip-pair-lands.mp3` | `snail-mucin-medical-secret` | F4 each citation chip | full (0.26s) |
  | `click-soft-3-each-step-arrives.mp3` | `snail-mucin-medical-secret` | F5 each object | full (0.24s) |
  | `chime-on-lockup-landing.mp3` | `ceramides-skin-barrier` | F6 lockup settle | full (1.44s) |

  Considered and rejected: `water-drop-soft-per-droplet-arrival.mp3` (4.11s — longer than
  all of Frame 1) was dropped in favor of `droplet-tick.mp3`, matching the skill's own
  SFX-spotting rule ("a stock SFX that runs longer than its visual beat will audibly
  drone into the next scene").
- Every clip gets an 80ms `data-automation` fade in/out in the **versioned**
  `{"version":1,"lanes":[…]}` shape confirmed correct for `hyperframes@0.8.17` — the flat
  shape is silently accepted by `check` and fails only at `render`. Any automated clip's
  plateau value is written as its real intended level, never `v:1` (a volume lane
  replaces `data-volume`, it doesn't multiply against it).
- Mastered post-render to **−14 LUFS integrated / −1.5 dBTP** via two-pass `ffmpeg
  loudnorm`, video stream copied through unchanged, targeting ≈−1.6 in PCM so the AAC
  encode lands ≤−1 dBTP (the channel's own documented codec-peak gotcha).

## Sourcing

House rule: a citation chip is reserved exclusively for a real, verified source id,
never invented. No `ING-*` record exists for behavioural/regulatory claims like these,
so this project's chips carry **PMIDs and CFR/FDA document identifiers** instead — a new
chip vocabulary for the channel, recorded here for the next non-ingredient project that
needs one.

A dedicated research pass checked every on-screen claim against PubMed and regulatory
text; every URL below was fetched and confirmed live during that pass except where
noted.

| Chip (on-screen) | Backing | What it actually supports |
|---|---|---|
| `PMID 7544967` | Griffiths et al. 1995, *Arch Dermatol* — 48-week double-blind, vehicle-controlled, n=99 | 0.1% and 0.025% tretinoin gave statistically indistinguishable clinical/histologic improvement; 0.1% produced significantly more erythema and scaling — "mechanisms other than irritation dominate tretinoin-induced repair." No DOI exists in PubMed for this record; none is reported. |
| `PMID 21284283` | Draelos et al. 2010, *Cutis* | Dryness/scaling/erythema/burning rise in week 1 of retinoid/BPO therapy, then decrease — "generally mild and improved within 1 to 2 weeks." No DOI in PubMed; none reported. |
| `21 CFR §333.350` | Federal acne-drug labeling (live, `ecfr.gov`) | (c)(4)(ii): burning, itching, peeling and swelling are *labeled, expected* irritation, distinct from a severe/worsening reaction. (c)(1)(ii): "only use one topical acne medication at a time" if irritation occurs — the actual textual basis for Frame 2's claim. |
| `PMID 17121065` | Draelos et al. 2006, *Cutis* — split-face RCT | Barrier-enhancing moisturizer, applied before and during tretinoin therapy, "facilitates the early phase of facial retinization and augments the treatment response." No DOI in PubMed; none reported. |
| `FDA-2000-P-0063` | FDA AHA labeling guidance, Jan 2005 (live, fda.gov) | The source of the AHA "Sunburn Alert" label text; recommended, non-binding guidance for cosmetics, not a binding rule — on-screen copy says "FDA advises," never "required." |

**Two claims required rewording before build, both corrected in the copy deck below
because the brief's original wording said the opposite of the cited regulator:**

1. Original: *"Burning, swelling or pain is not the goal."* — Contradicted by
   §333.350(c)(4)(ii), which lists burning and swelling as expected labeled irritation.
   Corrected to *"Severe burning or swelling? Stop and ask a doctor,"* tracking
   §333.350(c)(3)(ii)'s actual severity-based instruction.
2. Original: *"More actives. More results?"* answered flatly "no." — Contradicted by the
   2024 AAD acne guideline (PMID 38300170, not cited on-screen — used only to check this
   claim, not as a chip), which lists combining topical therapies with multiple
   mechanisms as a good-practice statement for medically directed treatment. Narrowed to
   *"More exfoliants. More results?"* — true only for unsupervised stacking of
   exfoliating actives, which is what the scene's own visuals (retinol, acid, toner
   bottles) depict.

*"Temporary dryness can happen"* needed no correction — already correctly hedged.

**Stated evidentiary limit (not left implicit):** Frame 3's headline — "Peeling is a
side effect — not a scorecard" — is evidenced for **retinoids in photoaging**
specifically (PMID 7544967, and a second dose-comparison, PMID 22538278, not
individually chipped on-screen). No equivalent study was found dissociating peeling
from efficacy for AHA/BHA exfoliants or for acne endpoints, and Griffiths is a
comparison of group means, not a per-patient correlation of an individual's own
peeling against their own outcome. Ships as the video's title claim regardless — it is
the strongest available evidence for the claim as stated — but the limit is recorded
here for a future pass, matching how `ceramides-skin-barrier` and
`betaine-salicylate-gentle-bha` record their own sourcing postures.

**Identifier caveats:** no DOI exists in PubMed for PMIDs 7544967, 21284283, or
17121065 — none is invented or reported. The FDA's 2014 acne-hypersensitivity safety
communication (a natural fit for Frame 4's right card) is 404 on fda.gov as of this
build and archive-only; §333.350 carries that beat's citation instead, since it is live
and states the same severity distinction.

## Copy deck (final, post-sourcing-correction)

| Frame | On-screen | Chip |
|---|---|---|
| 1 | "Your skin is peeling…" → "Does that mean it's working?" | — |
| 2 | "More exfoliants. More results?" → strike → "MORE IRRITATION. NOT MORE PROGRESS." | `21 CFR §333.350` |
| 3 | "Peeling is a side effect — not a scorecard." + "In trials, more irritation didn't mean better results." | `PMID 7544967` |
| 4 | L "Temporary dryness can happen" · R "Severe burning or swelling? Stop and ask a doctor." | `PMID 21284283` · `21 CFR §333.350` |
| 5 | "Start slowly. Follow directions. Protect the barrier." — ONE ACTIVE / MOISTURIZER / DAYTIME SPF | `PMID 17121065` · `FDA-2000-P-0063` |
| 6 | "One claim." / "One boundary." / "SeoulHabit." + "What skincare claim should we audit next?" | — |

## Component reuse

Catalog discovery found **no catalog entry** for a skin-layer diagram, product stack,
droplet animation, two-card comparison, or SeoulHabit mark (see BRIEF.md § Intent). Two
scenes instead adapt proven, uncatalogued mechanisms from prior video projects:

- **Frame 3** adapts `videos/betaine-salicylate-gentle-bha/compositions/frames/02-harsh.html`'s
  brick-wall SVG (`#hd-wall`, `#hd-wash`/`#hd-wash-line`, `#hd-chip-1/2/3`). Reused
  as-is: the wall/course structure, the shard-detach mechanism, the paused-GSAP timeline
  shape. Changed: this scene's wall starts intact and shows the *aftermath* (the wash
  descends and shards fall as the illustration of "what peeling is," not a fresh
  attack), and the headline/claim copy is this project's own, sourced.
- **Frame 4** adapts `videos/retinol-patch-test/compositions/frames/05-wait-48.html`'s
  `.split-normal`/`.split-stop` two-column layout and entrance timing. Changed: coral is
  dropped from the "stop" card (border/background revert to ink/rule-weight) since
  coral is already spent in Frame 2 — an explicit mechanism-not-skin adaptation per the
  skill's component-check step, not an oversight.
- **Frame 5**'s three object glyphs (`droplet`, `flask-conical`, `sun`) are copied from
  `catalog/visual-components/routine-ladder/`'s sanctioned Lucide vocabulary — 24×24
  viewBox, constant 3-unit stroke, "geometry is copied, not drawn."
- **Frame 6**'s lockup pattern is copied from
  `videos/glass-skin-5-habits/compositions/frames/06-cta-endcard.html`.

## Catalog contribution (planned, pending render)

The barrier-wall mechanism is now independently built a **third** time in this repo
(`betaine-salicylate-gentle-bha` SVG original, `ceramides-barrier-diagnostic`'s CSS-grid
variant, and this project's adaptation) while still absent from
`catalog/visual-components/` — exactly the repeated-rebuild failure the catalog
lifecycle exists to stop. After render and verification, harvest it as `BarrierWall`
with generalized sample content (not this video's real claim copy) and a paused,
seekable clock, sourced from the betaine-salicylate original since it's the cleanest
pure-SVG implementation. The two-card boundary mechanism
(`retinol-patch-test` + `snail-mucin-medical-secret`'s `split-tilt-cards.html`) is a
second harvest candidate, not yet actioned.

## Post-render review fixes

Four render-and-verify rounds. `npm run check` was clean from the first render
onward (0 errors, 0 warnings throughout) — every finding below came from pixel
verification the check/lint pass has no way to catch, matching this skill's own
"verify by pixels, never by manifest" rule.

**Round 1 — `check-blank-frames.py` (advisory, exit 0 always).** First render flagged
four near-blank scene-openings (533ms–1.67s, worst at Frame 4's 14.0–15.67s) —
entrance cascades that started with only a small kicker line visible for over a
second before the scene's real content arrived. Fixed by compressing each scene's
entrance timing so real canvas coverage arrives within roughly 0.5s of the cut.

**Round 2 — `check-static-hold.py`.** The Frame 4 compression from round 1 moved its
last authored beat (the alert-dot pulse) earlier, which exposed a genuine 2.5s frozen
tail (17.5–20.0s) the *first* render's check hadn't caught, because a slower pulse had
been silently covering for the same gap. Fixed with a continuous Ken-Burns push on
Frame 4 (`.frame-zoom`, scale 1→1.025 across the full 6s), matching the technique
already in place on Frames 3 and 5.

**Round 3 — a real rendering bug, not a timing tweak.** With rounds 1–2's fixes in,
the blank-frame scanner still flagged Frame 2's opening as near-blank — worth
independent pixel confirmation before accepting it as "a beat gap" (its own advisory
framing invites exactly that check). Frame-exact extraction
(`ffmpeg -vf "select=eq(n\,90)"`, bypassing `-ss`'s non-frame-accurate seeking, which
itself produced a misleading early read of this same boundary) showed `#headline-q`
rendering **fully opaque from Frame 2's literal first frame**, even though its GSAP
tween (`'--p':1`, driven by `opacity: var(--p)`) wasn't authored to start until local
1.2s. This was a genuine defect in the rendered MP4, not a misread — bottle-1/2/3's
plain-`opacity` tweens on the same frame animated correctly on schedule, isolating the
bug to the CSS-custom-property-driven pattern specifically. Frame 1 used the identical
`--p` pattern for its own kinetic-type reveal and was converted alongside Frame 2,
even though it hadn't been independently proven broken — the same mechanism, unproven
safe, wasn't worth trusting a second time. Both files now use plain `opacity` +
`transform: translateY()` tweens, the pattern already proven correct in Frames 3–6
and in Frame 2's own bottles. Root cause not fully diagnosed (plausibly a GSAP
auto-"from"-detection quirk specific to custom properties in this render pipeline,
distinct from the project's own documented `data-automation` custom-property gotcha)
— not chased further once the reliable alternative was in hand and verified.

**Round 4 — re-verifying the fix, and a false alarm in my own tooling.** A batched,
multi-frame `ffmpeg select` + Python contact-sheet script built to re-check the fix
showed Frame 2's *first* frame already fully resolved ("MORE IRRITATION...", 3
bottles, the citation chip) — which would have meant the fix hadn't worked, or had
somehow made things worse. Before acting on that, the same frame was re-pulled with a
single, unbatched `ffmpeg` call: genuinely blank, 10KB PNG (consistent with a truly
empty canvas), confirming the batched script had mislabeled its own grid, not that the
render was broken. The direct method was trusted over the diagnostic script's output,
and the fix was confirmed correct: `#headline-q` invisible at local 0, visible only
from local ~1.2s onward, exactly as authored (`n90`/`n105`/`n135`/`n195` inspected
individually). Frame 2's true remaining blank-frame window (267–400ms, the bottle
cascade alone, before the fix had been masking it) was then tightened the same way as
round 1's other four scenes.

Final render: `check-blank-frames.py` reports five windows, all 267–533ms (down from
one as high as 1.67s); `check-static-hold.py` reports zero findings. See
`DELIVERY.md` for the mastered file and its measured loudness.

**Round 5 (2026-08-31) — skill-update reconciliation, before that "zero findings" was
trustworthy.** `faceless-video-craft` SKILL.md gained a pre-render gate, raised type
floors, a citation-ID ban, and a delivery-manifest requirement after this project's
first render. Re-checked against it and found five real defects, all confirmed against
actual pixels before fixing, not assumed from the CSS:

1. **Frame 2's citation chip rendered inside the platform overlay zone.** `.stage`'s
   padding-bottom was a literal `0` (every other scene used `var(--safe-bottom)`) —
   confirmed by indexed frame extraction: the chip sat at y≈1700–1743, 140–180px past
   the y1560 safe-bottom boundary. `STORYBOARD.md`'s "ticks in bottom-safe" line was
   wrong. Fixed.
2. **Every citation pill carried the internal PMID/CFR lookup ID**, not a
   human-readable source — the skill's new rule reserves the on-screen pill for
   `Journal · Year`; the ID belongs in the description only. Converted using the
   mappings already recorded in § Sourcing above (no new research needed).
3. **Type sat below the skill's raised floors in 5 of 6 frames** — heroes were
   52–72px against a new 96px floor, chips/labels 22–26px against a new 32px floor.
   Raised across all six frames; this also superseded this file's own § Type note
   about a deliberate 22px chip exception, which no longer applies once pills carry
   real reading text instead of a decorative signal-only ID.
4. **`--safe-right` (162px, the Shorts action-rail reserve) was declared in every
   frame and consumed by none** — all six padded symmetric `--safe-left` on both
   sides. Switched to asymmetric `--safe-left`/`--safe-right` padding throughout,
   which also meant re-fitting Frame 2's bottle row and Frame 4's two cards to the
   narrower 858px column (both previously sized for the old 960px symmetric column).
5. **The static-hold scanner (`scripts/check-static-hold.py`) was a mis-ported
   copy** carrying another project's caption-band crop geometry (y960–1110) and
   docstring — this project has no captions, so the crop was cutting Frame 3's
   shard-detach animation out of every comparison. Its "zero findings" in this file's
   own Round 1–4 account above was therefore not established by anything that could
   have caught a real freeze in that band. Corrected to sample the full frame; still
   zero findings, now on real evidence.

**A wrong first fix, caught by re-measuring rather than trusting the edit.** The
initial fix for finding 1's class of defect (also found independently in Frames 3 and
5, both landing their citation chip within a few px of y1560 with zero margin) tried
shrinking each scene's `headline-zone`/top-padding. Re-extracting the actual render
showed **zero change** in the chip's rendered position. Root cause, found by comparing
an early-scene frame (low zoom) against the scene's own last frame (max zoom) for the
same element: `diagram-zone`/`objects-row`'s `flex:1` absorbs any change to the space
above it exactly, so the *unscaled* layout was already correct — the real cause was
each scene's own continuous Ken-Burns `#zoom` transform (present precisely to avoid a
static-hold flag) displacing content below its transform-origin further down as scale
grows through the scene. Fixed by reserving extra static margin below
`var(--safe-bottom)` (+45px on Frame 3, +35px on Frame 5), sized from the scene's own
max scale and origin, so the flex-absorbed layout starts far enough above the boundary
to survive the zoom. Frame 6's lockup also needed a measured correction: raising its
type grew the scene's text stack enough to shift the centered group's lockup line 52px
above Frame 1's droplet-panel center, breaking the loop hand-off's matched hero
position (`STORYBOARD.md`'s arc note) — corrected with a calculated `margin-top`
(shifting a centered flex child down by d needs 2d of margin, since the group
recenters and absorbs half); re-measured after the fix at within 1.5px of Frame 1's
panel center.

Re-verified end to end on the corrected render: all four citation chips clear
y1560 with 12–80px of real margin: safe-right honored on all six frames (right edge
within a few px of x918 everywhere, matching antialiasing noise); loop hand-off
lockup-to-panel match within 1.5px; phone-scale downscale (25%) confirms every
headline, label, and pill legible; `check-blank-frames.py` unchanged (same five
267–533ms scene-opening windows, unrelated to this pass); `check-static-hold.py`
zero findings on the full frame. See `DELIVERY.md`'s pre-render gate for the full
12-item record.

**Round 6 (2026-08-31) — external QC report, and the checker this project didn't
have.** A QC report on the round-5 render returned "fix-then-ship": one BLOCKER
(the outro instruction blocked by the Shorts UI, "move above y1530"), two MAJORs
(the outro's ~4s static hold; Frame 3's citation "too low," move up 15-20%), and two
MINORs (Frame 4's right card into the action rail; no captions for this VO-less
video). Per this skill's own rule ("an external QC report is a claim, not a
diagnosis"), every finding was reproduced against the actual render before touching
anything, by extracting frames at 2fps/4fps and measuring ink extents directly:

| # | Report | Measured | Verdict |
|---|---|---|---|
| 1 | BLOCKER: outro text at extreme bottom edge, move above y1530 | Prompt bottom = y1420 — 116px clear of the line, already past the report's own target | **False** |
| 2 | MAJOR: ~4s static outro, trim to 1s | Longest static run at the end = 1.25s (28.75-30.0s); under the skill's 2-3s ceiling | **False on duration** |
| 3 | MAJOR: citation too low, move up 15-20% (288-384px) | Real. Frame 3 ink reached y1546 — 10px past the real line, not 288-384px | **Real, misquantified ~30x** |
| 4 | MINOR: right card into the action rail, shift 100-150px | Real. Frame 4 ink reached x923 — 5px past the line, not 100-150px | **Real, misquantified ~25x** |
| 5 | MINOR: no captions, no VO | Correct premise: zero speech, 100% of the language on-screen | **Real** |

A third violation the report missed entirely: **Frame 5** reached y1543 (7px past)
from the identical cause. Applying the report's literal fixes would have broken
working things — item 1's ~384px shift would have pushed Frame 6's outro out of the
loop-matched hero position this file's own round-5 note describes; item 4's
100-150px shift would have thrown the two-card row far off its centered layout.

**Root cause — one bug, three scenes, and it's the mechanism round 5's own fix
already named without generalizing.** Round 5's "wrong first fix" note above already
diagnosed that a scene's continuous Ken-Burns `#zoom` transform displaces content
below its transform-origin further down as scale grows — and fixed it there with a
hand-computed `+45px`/`+35px` allowance on Frames 3/5. That allowance was correct
against the boundary in effect when it was measured (`--safe-bottom: 360px`, 18.75%
— itself under the skill's stated 20%) and silently wrong once corrected: raising
`--safe-bottom` to the real 384px (20%) without re-deriving the allowance left both
scenes still 7-10px short of the new line. The math, confirmed against measured
pixels:

| Scene | origin | max scale | unscaled box edge | → after scale | measured overshoot |
|---|---|---|---|---|---|
| `03-truth` | y768 | 1.045 | y1515 | y1548.8 | y1546 |
| `05-reset` | y864 | 1.030 | y1525 | y1544.8 | y1543 |
| `04-boundary` | x540 | 1.025 | x918 | x927.5 | x923 |

`padding` constrains the layout box; a `transform: scale()` applied outside that box
(the Ken Burns wrapper, mandatory for every scene per the anti-static-hold rule) maps
the padded edge outward by the same factor — every one of the six scenes declared and
consumed every `--safe-*` token (gate item 7 as it read before this round), and the
pixels still overshot, because token-consumption is a source-code question and this
defect only exists once the render is measured.

**A fourth, previously undetected violation — caught only because the new checker
samples the whole render at 4fps, not just settle frames.** After fixing the three
scenes above and building `scripts/check-safe-area.py` (see below), a first run of
that script against the *fixed* render still failed, flagging Frame 1 — a scene
neither the QC report nor any prior round's spot-checks had named. Frame-exact
inspection found `#line-2` ("Does that mean it's working?") transiently overshooting
the bottom line by ~10px during its own entrance, between local t=1.85s and ~2.0s,
before easing back to a compliant resting position (y1531, a real but thin 5px
margin) by t≈2.17s. Cause: `.line`'s base state carried `transform:
translateY(18px)`, and the entrance tween's `power2.out` ease spends most of its
first ~150ms still close to that full offset while opacity is still low — exactly
the kind of transient a 1-2fps spot-check (what every prior round, and the external
report, effectively used) reliably lands outside of. Fixed by removing the
`translateY` from both `.line`'s entrance/exit (opacity-only cross-fade now,
matching the pattern already proven correct everywhere else in this project per
round 3's own note) — the settled position is unchanged, the transient is gone.

**A regression caught by re-measuring the fix, not by assuming it was safe.** A
first attempt also trimmed Frame 1's `.stage` `gap` (56→32px) for extra headroom.
Re-measuring the surface-panel's own center after that change showed it had moved
~12px (772→784), because the panel and the text-stack are both centered as one flex
group — reducing the gap doesn't just shrink space between them, it shifts the whole
group. That broke the round-5-era loop hand-off `06-payoff.html`'s own `.lockup`
`margin-top` is hand-tuned against (Frame 1's panel center is the target Frame 6's
lockup matches for the hard-cut loop). Reverted — the `translateY` removal alone was
sufficient and didn't touch panel position at all. Re-verified: 771.5 vs 770.5,
within 1px.

**Fix: replace the hand-tuned allowance with a derived safe box.** `--safe-bottom`
raised 360→384px (the real 20%); `--safe-top` deliberately kept at 120px (6.25%,
not the skill's 192px) with the reason recorded — Shorts' top chrome is minimal and
every scene's headline already starts at y134-164, so the full reserve would push
four headlines down 60px for no real UI there. Added `--zoom-max`/`--zoom-origin-x`/
`--zoom-origin-y` (per-scene, matching each scene's own `fromTo('#zoom', ...)` call)
and `--safe-bottom-zoomed`/`--safe-right-zoomed`, which invert the scale-then-measure
math above so the *padded* edge lands on the real line *after* the scene's own max
scale — a function of the scene's actual zoom, not a constant that silently drifts
the next time either the token or the scale changes. Frames 3/4/5 (the zoomed
scenes) now consume the `-zoomed` tokens in `.stage`'s padding; Frame 3's diagram SVG
and Frame 4's two cards were re-fit to the ~15-20px narrower resulting column (Frame
5's objects-row already had slack and needed no re-fit). Frame 2 (no scene zoom)
switched to the same `-zoomed` spelling at neutral `--zoom-max: 1` defaults purely
for consistency — identical resulting values, one spelling project-wide. Frames 1/6
keep their deliberate full-canvas centering (no vertical safe padding) unchanged,
per the loop-match reasoning above.

**The durable fix: `scripts/check-safe-area.py`, a hard gate.** Modeled on the
existing `check-static-hold.py`'s CLI shape, sampling the render at 4fps and flagging
any frame with real ink (antialiasing-tolerant) inside a reserved zone — the check
this project never had, and the only pre-render gate item (7) with no corresponding
entry in the Verification loop before this round. Unlike the blank-frame/static-hold
scripts, this one is a **hard gate** (non-zero exit), wired into `postrender`
alongside them. Harvested into `catalog/tooling/` as the first verification-tooling
entry — see `catalog/README.md`.

**Captions.** `DELIVERY.md`'s prior "no captions — deliberate" note was a correct
read of the skill's transcript-predicated caption workflow (no VO, nothing to run
ASR on) but an incomplete read of the actual requirement — 100% of this video's
language is on-screen kinetic type, and a captions/screen-reader user got nothing
without a sidecar. Hand-authored `captions/peeling-not-progress.srt` and `.vtt`
directly from `STORYBOARD.md`'s copy deck and `index.html`'s scene timings (no ASR
involved or needed, since the text and its exact timing were already authored
artifacts) — 21 SDH-style cues, every citation included, bracketed cues for the two
narratively meaningful SFX (`[wall crumbles]`, `[chime]`); routine UI clicks
omitted. Every cue verified to land inside the scene whose text it transcribes.

**Re-verified end to end on the corrected, re-mastered render** (independent 4fps
ink-extent scan, not just the new script's own output): zero frames with ink in any
reserved zone across all six scenes (previously 3-10px over on Frames 3/4/5, plus the
newly found Frame 1 transient). Real per-scene margins: Frame 1 y1531 (5px) / x917
(1px, by design — the safe column's own full width, confirmed not new), Frame 3
y1530 (6px), Frame 4 x912 (6px), Frame 5 y1531 (5px), Frames 2/6 comfortably clear
(84px/116px). Frame 1↔6 loop hero-position match: 771.5 vs 770.5 (within 1px,
unchanged from round 5). `check-static-hold.py`: zero findings, unchanged.
`check-blank-frames.py`: same five 200-533ms scene-opening windows as round 5,
unrelated to this pass. Phone-scale (25%) downscale confirms Frame 1/3/4's affected
text still legible. Re-mastered: two-pass `ffmpeg loudnorm`, −14.04 LUFS integrated /
−1.60 dBTP (matching round 5's figures — the audio layer wasn't touched), independent
`astats` peak check −1.20 dB, safely under 0 dBFS. See `DELIVERY.md` for the full
manifest.
