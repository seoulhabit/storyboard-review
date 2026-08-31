---
message: "Visible peeling is an irritation side effect, not a scorecard for whether an active is working."
audience: "skincare-curious viewers stacking actives and reading peeling as proof of progress"
mode: autonomous
format: 1080x1920
duration: 30.000s (AUTHORED — no VO exists to measure from; the brief's own 0/3/8/14/20/26/30 second grid ships as written, per BRIEF.md's silent-first decision record)
arc: pattern interrupt → overload → correction → boundary → reset → brand payoff
music: bed reused verbatim from videos/retinol-patch-test/assets/bgm/track.mp3 (57s file, data-duration capped to fit); no VO to duck under, so no data-fx-carve
---

Six frames, **every boundary a hard cut** — including 4→5 (paper→paper), which an
earlier draft of this doc called out for a 150ms same-ground crossfade that was never
actually implemented in `index.html`; corrected here rather than left inconsistent,
since a hard cut carries no muddy-blend risk on a same-ground boundary anyway (the
house default is hard cuts everywhere per `faceless-video-craft`'s cuts-vs-crossfades
rule). Ground alternates **ink → paper → ink → paper → paper → ink**; Frame 6's ink
hands back to Frame 1's ink at a matched centered hero position — the engineered loop a
short requires. No VO exists, so every beat below is authored directly against the
brief's timing rather than derived from a measured take.

**Recorded reason: no photographic or tactile anchor in any beat.** Every visual is
browser-drawn SVG/CSS (droplet, bottles, barrier wall, evidence cards, three objects,
lockup) — not a fixed-quota shortfall, but this channel's standing rule ("Browser-drawn
only… No generative imagery, ever," `catalog/ingredients/one-percent-line/README.md:113`,
quoted in full in `BRIEF.md § Assets` and `frame.md § Media exception`). Logged here per
`faceless-video-craft` SKILL.md's asset rule 6, which asks for the reason on record in
the beat sheet itself, not only in the brief.

**Post-render fixes (2026-08-31), found by pixel verification, not by the check/lint
pass — see `frame.md § Verification` for the full account:**
1. A real rendering bug: `--p`-driven opacity (a CSS custom property read by
   `opacity: var(--p)`, tweened via GSAP `.to()`) rendered Frame 2's headline fully
   opaque from local t=0 in the actual MP4, even though its entrance tween didn't start
   until local 1.2 — confirmed via frame-exact (`ffprobe`/`-vf select`) extraction, not
   assumed from the timeline code. Frames 1 and 2 both used this pattern for their
   kinetic-type reveals; both converted to plain `opacity`/`transform` tweens (the
   pattern already proven correct everywhere else in this project) rather than patched
   around. See `01-hook.html` and `02-overload.html`'s own comments.
2. The blank-frame scanner flagged near-empty openings at every scene cut except 1→2
   (267ms–1.67s, worst at Frame 4). Fixed by compressing each scene's entrance
   cascade so real content asserts within ~0.5s of the cut, and by adding a continuous
   Ken-Burns push to Frame 4 (matching Frames 3/5) after that compression exposed a
   genuine static-hold tail the scanner then caught on the next render.
3. Two verification methodology notes for future rounds in this project: `ffmpeg -ss`
   placed *before* `-i` is not frame-accurate and produced misleading extractions early
   in this pass (corrected by seeking after `-i`, or by indexed `select=eq(n,N)`
   extraction); and a batched multi-frame `select` + Python contact-sheet labeling
   script produced one genuinely misaligned frame during this same pass — caught by
   re-verifying with single, unbatched `ffmpeg` calls before trusting it. Don't trust
   a diagnostic script's own output more than the direct, boring extraction method.

**Skill-update reconciliation (2026-08-31) — five real defects found against the
updated `faceless-video-craft` SKILL.md, all confirmed by pixel extraction before
fixing. Full account in `frame.md § Post-render review fixes` round 5.**
1. Frame 2's citation chip rendered inside the platform overlay zone — `.stage`'s
   bottom padding was a literal `0` (every other scene used `var(--safe-bottom)`).
   **Correction: the "ticks in bottom-safe" line under Frame 2 below was wrong; it
   didn't.** Fixed.
2. Every citation pill carried its internal PMID/CFR lookup ID instead of a
   human-readable source. Converted to `Journal · Year` form (copy deck below).
3. Type sat below the skill's raised floors (96px hero / 40px body / 32px
   label-and-chip) in 5 of 6 frames — raised throughout.
4. `--safe-right` (the Shorts action-rail reserve) was declared in every frame and
   consumed by none. Switched to asymmetric safe-left/safe-right padding; Frame 2's
   bottle row and Frame 4's two cards re-fit to the resulting 858px column.
5. `scripts/check-static-hold.py` carried a mis-ported caption-band crop from a
   different, captioned project — this video has no captions, so the crop was
   cutting Frame 3's shard-detach animation out of the check. Corrected to the full
   frame; still zero findings, now on real evidence.

A first fix attempt (shrinking Frame 3/5's top-side spacing) measured **zero effect**
on the actual render — the real cause was each scene's own continuous Ken-Burns zoom
pushing bottom-safe content down as it scales through the scene, not the static
layout. Fixed by reserving extra static margin sized to each scene's own zoom
displacement. Frame 6's lockup also needed a measured `margin-top` correction after
the type raise shifted it 52px off Frame 1's matched loop position; re-verified within
1.5px after the fix. All five defects re-verified against the corrected final render,
not re-assumed from the edits.

## Frame 1 — hook

- status: shipped
- src: compositions/frames/01-hook.html
- type: hook
- start: 0.000
- duration (scene clip, authored): 3.000s
- ground: ink
- beat: Cold open, payoff visible immediately (frame-zero discipline — the droplet is
  already settled on the surface at t=0, not fading in). 0.0–0.9s: glossy droplet at
  rest on a smooth surface, finite ripple rings, "Your skin is peeling…" fades in at
  0.1s. 0.9–1.8s: SVG crack paths draw outward from center (`stroke-dashoffset`,
  seek-safe) as the surface dries; droplet fades into the cracked surface. 1.8–3.0s:
  fracture completes, first line exits, "Does that mean it's working?" resolves —
  the pattern-interrupt payoff, landing inside the shorts retention window.
  SFX: `droplet-tick` at the droplet's arrival, `whoosh-soft-myth-bust-cut` under the
  crack-draw.

## Frame 2 — overload

- status: shipped
- src: compositions/frames/02-overload.html
- type: concept
- start: 3.000
- duration (scene clip, authored): 5.000s
- ground: paper
- beat: 3.0–4.2s: three bottle silhouettes stack in, staggered, each trailing a small
  INCI-style label chip that overlaps the previous one — deliberate visual noise, not a
  layout bug. 4.2–5.0s: "More exfoliants. More results?" settles over the stack.
  5.0–5.6s: two more ingredient-name tags (RETINOL, AHA/BHA) fan in, clutter peaks.
  5.6–6.2s: **the video's one coral moment** — a coral strike line scales across the
  headline. 6.2–8.0s: strike resolves into "MORE IRRITATION. NOT MORE PROGRESS.", the
  `FDA · 21 CFR 333.350` chip ticks in bottom-safe. SFX: `sharp-text-stamp-impact-hit.trimmed`
  on the strike, a soft click on the final chip.
- review fix: coral is spent here, not in Frame 4 — see BRIEF.md § Assets for why (house
  rule: one coral moment per video; this is the brief.s own explicit ask, and 3–8s is
  the higher-retention slot).
- correction (2026-08-31): this chip did NOT actually land bottom-safe as this beat
  originally claimed -- .stage.s bottom padding was a literal 0, and pixel extraction
  found the chip at y~1700-1743, inside the platform overlay zone. Fixed (see
  frame.md § Post-render review fixes round 5); text also changed from the internal
  21 CFR §333.350 ID to the human-readable FDA · 21 CFR 333.350 form.

## Frame 3 — truth

- status: shipped
- src: compositions/frames/03-truth.html
- type: concept
- start: 8.000
- duration (scene clip, authored): 6.000s
- ground: ink
- beat: **Signature component** — adapted from `betaine-salicylate-gentle-bha`'s
  `02-harsh.html` brick-wall mechanism (see BRIEF.md § Assets). 8.0–8.8s: a clean
  three-course brick wall assembles (staggered fade/scale, no acid wash yet — this
  video's wall starts intact, betaine's starts already-clean and gets attacked; here
  the *attack already happened offscreen* and this scene shows the aftermath, so the
  wash/shard-detachment beat below reads as "what peeling actually is," not a fresh
  assault). 8.8–10.0s: "Peeling is a side effect — not a scorecard." resolves, two-line
  reveal. 10.0–11.2s: the adapted wash-descends-then-shards-detach beat — top course
  dims, three shards drift and rotate away. 11.2–12.2s: mono qualifier fades in below
  the headline: "In trials, more irritation didn't mean better results." 12.2–13.0s:
  `Arch Dermatol · 1995` chip ticks in bottom-safe (was the internal PMID 7544967 ID). 13.0–14.0s: brief hold before the hard cut.
  SFX: `wall-crumble-crack-collapse` (data-duration capped to ~2.2s, timed to the
  shard-detach beat only — the 5.39s source file is longer than this scene needs, see
  `frame.md § Audio mix`).

## Frame 4 — boundary

- status: shipped
- src: compositions/frames/04-boundary.html
- type: concept
- start: 14.000
- duration (scene clip, authored): 6.000s
- ground: paper
- beat: Adapted from `retinol-patch-test`'s `05-wait-48.html` two-column mechanism (see
  BRIEF.md § Assets) — **skin, not the coral skin**: this scene carries its boundary on
  rule-weight and ink, since coral was already spent in Frame 2. 14.0–14.4s: kicker
  "WHERE'S THE LINE?" fades in top-safe. 14.4–15.2s: left card slides/fades in —
  "NORMAL" (aqua kicker) / "Temporary dryness can happen." 15.2–15.6s: `Cutis · 2010` (was PMID 21284283)
  chip ticks onto the left card. 15.6–16.4s: right card slides in from the opposite
  side — "STOP" (ink-weight, no coral) / "Severe burning or swelling? Stop and ask a
  doctor." 16.4–16.8s: `FDA · 21 CFR 333.350` chip ticks onto the right card (was 21 CFR §333.350 ID). 16.8–17.6s: a
  vertical divider rule draws between the two cards, literalizing "the boundary."
  17.6–20.0s: a bounded (2-cycle, finite) pulse on the right card's alert dot keeps the
  tail from reading as a static hold. SFX: `click-soft-chip-pair-lands` on each chip.

## Frame 5 — reset

- status: shipped
- src: compositions/frames/05-reset.html
- type: concept
- start: 20.000
- duration (scene clip, authored): 6.000s
- ground: paper
- beat: 20.0–20.6s: kicker "THE RESET" + "Start slowly. Follow directions. Protect the
  barrier." resolve as one wrapped block (not three separately staggered lines — keeps
  the safe column's remaining height for the three objects, which need to fill 65–80%
  of it, not the text). 20.6–21.4s: object 1 scales/fades in — `droplet` glyph (Lucide
  geometry via `catalog/visual-components/routine-ladder/`'s sanctioned icon set),
  "ONE ACTIVE" — a deliberate callback to Frame 1's droplet motif. 21.4–22.2s: object 2
  — `flask-conical` glyph, "MOISTURIZER." 22.2–23.0s: object 3 — `sun` glyph, "DAYTIME
  SPF." 23.0–23.6s: `Cutis · 2006` chip ticks in near objects 1–2 (was PMID 17121065). 23.6–24.2s:
  `FDA guidance · 2005` chip ticks in near object 3 (was FDA-2000-P-0063) — on-screen copy reads "FDA advises,"
  never "required" (the AHA sunburn alert is recommended labeling in a non-binding
  guidance document, not a binding rule — see BRIEF.md § Notes). 24.2–26.0s: a slow,
  continuous, seek-safe scale (1.0→1.03) across the full scene covers the tail so
  nothing sits frozen. SFX: `click-soft-3-each-step-arrives`, one hit per object.

## Frame 6 — payoff

- status: shipped
- src: compositions/frames/06-payoff.html
- type: cta
- start: 26.000
- duration (scene clip, authored): 4.000s
- ground: ink
- beat: Hard cut to ink. 26.0–26.3s: the three object glyphs from Frame 5 reappear in
  miniature, converging toward center. 26.3–26.7s: they resolve behind the 습 SeoulHabit
  lockup (`videos/glass-skin-5-habits/compositions/frames/06-cta-endcard.html`'s
  lockup pattern, self-hosted `NotoSansKR-500-subset.woff2`), which settles centered —
  matched to Frame 1's centered droplet position for the loop hand-off. 26.7–27.3s:
  "One claim." fades in. 27.3–27.9s: "One boundary." 27.9–28.5s: "SeoulHabit." settles
  as the brand line. 28.5–29.3s: the closing-action line fades in — "Peeling? Drop to
  one active for two weeks." (was the generic "What skincare claim should we audit
  next?" prompt, moved 2026-08-31 to the pinned comment only — see DELIVERY.md and
  frame.md § Post-render review fixes round 5; the replacement is one specific,
  lesson-tied action sourced from this video's own beats: 21 CFR 333.350(c)(1)(ii)'s
  one-active-at-a-time instruction + PMID 21284283's 1-2 week improvement window).
  29.3–30.0s: final hold, ink ground, centered lockup — the
  frame that hands back to Frame 1's t=0. SFX: `chime-on-lockup-landing` on the lockup
  settle.
