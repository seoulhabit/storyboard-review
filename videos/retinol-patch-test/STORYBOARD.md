---
format: faceless-explainer
duration: 60.682s
message: "Patch test retinol behind your ear or jawline before your face — wait 48 hours, and stop at the first sign of a bad reaction."
arc: how-to (hook -> context -> 3 steps -> outro)
audience: skincare beginners who just bought their first retinol
mode: automation
music: calm, warm, aesthetic educational skincare bed, low presence under narration
---

## Video direction

Type: SeoulHabit faceless explainer, 1080x1920, paper/ink alternating grounds.
Motion grammar: crossfade-only scene transitions (0.5s, power2.inOut); no
bounce/elastic easing; no infinite keyframes; shadow-only elevation, never
glow. Rhythm: one clear beat per ~2-3s of narration, staggered chip/label
reveals on `--stagger-line/-node/-step`. Negative list: no success color, no
citation chips (no `ING-*` record for patch-testing exists), Fold & Spark logo
never appears, coral used exactly once across the whole video.

## Frame 1 — Hook

scene: 01-hook
voiceover: "So you just got a brand new retinol, and you want to slather it all over your face immediately? Stop!"
duration: 6.796 (VO 6.296 + 0.5 tail)
transition_in: cut (opens the video)
status: built
src: compositions/frames/01-hook.html
type: kinetic-type
persuasion: pattern-interrupt
beat: hook
blueprint: per-word reveal -> strikethrough slash -> highlighter payoff
focal: "STOP" payoff word
roles: ground=paper, highlight=highlighter (not coral — coral is reserved for Frame 5)
sfx: hook-hit @0.0, buzzer @5.5 (aligned to "Stop!" at 5.619s per assets/voice/01.words.json)
narrativeRole: pattern-interrupt open
keyMessage: don't rush into full-face application
Adapt: user's on-camera "hold serum, hand up to stop" beat becomes kinetic type + a strikethrough slash — the gesture's meaning, not its footage.

Scene 1 (0-6.3s): Faint retinol-bottle silhouette mark on paper ground. Words build one at a time, Inter 800: "SLATHER IT ALL / OVER YOUR FACE?" By ~4.6s the full question is up. At "immediately?" (4.559s) the type holds. At "Stop!" (5.619s) a heavy ink strikethrough slashes across the question and a highlighter "WAIT." pop-in lands beneath it, held to scene end.

## Frame 2 — Retinol is powerful

scene: 02-power
voiceover: "Retinol is the gold standard for anti-aging and breakouts, but it is incredibly strong. Before you risk a damaged skin barrier, you need to patch test. Here's how to do it safely."
duration: 12.647 (VO 12.147 + 0.5 tail)
transition_in: crossfade 0.5s
status: built (rebuilt — see Revision below)
src: compositions/frames/02-power.html
type: icon + card-typography
persuasion: authority + caution
beat: context
blueprint: large stroke icon + headline/category/body card, matching the checked-in glossary card language
focal: the reused Retinol icon + card copy
roles: ground=ink, highlight=aqua (icon + the "= POWERFUL" chip)
sfx: soft-whoosh @0.1 (icon lands), soft-click @5.0 (chip lands)
narrativeRole: raises the stakes before the how-to
keyMessage: retinol is effective but strong enough to need a patch test
Adapt: user's "close-up of product texture on your finger" becomes the checked-in glossary's own Retinol card — same generic leaf-stroke icon, category, and body copy.

Scene 2 (0-12.1s): On ink ground, the checked-in glossary's generic leaf-stroke SVG icon (24x24 viewBox, reused verbatim) scales/fades in large and aqua-colored. Below it: "Retinol" (EB Garamond, paper), "VITAMIN A" category label, a hairline rule, then the checked-in card's own body line ("A gold-standard anti-aging compound that promotes cell turnover.") — all copied from `videos/skincare-glossary-part-4-texture-anti-aging/index.html`'s own tracked Retinol card. Aqua mono chip "= POWERFUL" pops in at ~5.0s, held to scene end.

Revision (post-ship): the original build used `catalog/ingredient-photography/16-retinol.png` as a full-bleed photo hero. That file is not checked into git (`git ls-files` returns 0 matches for the whole `ingredient-photography/` directory), so per a git-provenance audit it was replaced with the checked-in glossary's icon+card treatment above — see `frame.md` § Provenance validation.

## Frame 3 — Step 1: choose a test site

scene: 03-test-site
voiceover: "Because retinol speeds up cell turnover, test it right behind your ear or along your jawline — the spots that behave most like the skin on your face."
duration: 9.120 (VO 8.620 + 0.5 tail)
transition_in: crossfade 0.5s
status: built (redesigned — see Revision below)
src: compositions/frames/03-test-site.html
type: svg-diagram + legend
persuasion: procedural clarity
beat: step 1
focal: front-view head+shoulders bust silhouette, two numbered test-site markers, matching legend chips
roles: ground=paper, highlight=aqua (both markers + their legend numbers)
sfx: soft-click @2.5 (marker 1 / BEHIND EAR lands), soft-click @5.0 (marker 2 / JAWLINE lands)
narrativeRole: names the two safe test sites
keyMessage: behind the ear and along the jawline are the two test sites
Adapt: user's "zoom in on you pointing to your jawline" becomes a clean vector bust diagram, in the abstract-clinical-geometry language of `catalog/visual-components/split-face-protocol/splitfaceprotocol-spike.html` (smooth continuous arcs, no attempted facial detail) rather than a fussy anatomical profile.

Scene 3 (0-8.6s): Mono kicker "STEP 1 · PICK A TEST SITE" fades in at open. A faint dashed ring plus an ink-line front-view head+shoulders bust (with a small ear) draw in via `stroke-dashoffset` over ~1.1s. Two numbered aqua markers pop onto the bust in sequence — ① behind the ear at 2.5s, ② on the jawline at 5.0s — each landing alongside a matching numbered legend chip ("① BEHIND EAR" / "② JAWLINE") below the diagram. Tagline "Same turnover, lower stakes" fades in at 6.5s, held to scene end.

Revision (post-ship): the original build used a hand-drawn side-profile head (nose/lips detail) with floating leader-line labels — user feedback called the result "awful." Replaced with the front-view bust + numbered-legend pattern above, which also fixed a real CSS bug: `.legend-zone` inherited an unset `bottom: 0` from the shared `.clip` base class, stretching the legend chips into tall vertical stadiums instead of horizontal pills. Fix: any zone that positions via `top` must also set `bottom: auto` to cancel that inheritance — the same latent pattern exists elsewhere in this project (harmless where children lack borders/backgrounds) but is a checklist item for any new zone in this design system.

## Frame 4 — Step 2: the dose

scene: 04-night-dose
voiceover: "At night, apply a tiny, pea-sized amount to clean, dry skin. Rub it in gently, and then leave it alone. No other serums or moisturizers on top."
duration: 10.662 (VO 10.162 + 0.5 tail)
transition_in: crossfade 0.5s
status: built
src: compositions/frames/04-night-dose.html
type: display-text + rule-list
persuasion: precise instruction
beat: step 2
blueprint: night motif (ported celestial-arc moon/PM lockup) + dose scale + staggered rule chips
focal: pea-sized aqua dot on a mono ruler
roles: ground=ink, highlight=aqua (the dose dot only)
sfx: pop @3.0 (pea dot lands), soft-click @5.0/6.0/7.0 (three rule chips)
narrativeRole: the one instruction viewers must not skim past
keyMessage: pea-sized amount, clean dry skin, nothing layered on top
Adapt: user's "applying a tiny, pea-sized amount... at night" becomes a dose-scale graphic under the catalog's real day-to-night arc (`catalog/visual-components/celestial-arc/celestial-arc-spike.html` — same arc path, same overlapping-circle crescent-moon technique, ported deterministic and glow-free since the source runs on CSS `infinite` keyframes and a blurred box-shadow, neither allowed here).

Scene 4 (0-10.2s): The catalog's day-to-night arc — a dim static sun (day already done) and a bright crescent moon + stars (now) on a dashed arc — draws in top-third, "NIGHT ROUTINE" label beneath. Center: mono ruler graphic with a single aqua dot sized like a pea, label "PEA-SIZED. THAT'S IT." lands at 3.0s. Three rule chips stagger in below starting 5.0s: "CLEAN, DRY SKIN" / "RUB IN GENTLY" / "NOTHING ON TOP" — the third chip carries an ink strikethrough over small serum + moisturizer glyphs.

Revision (post-ship): the original build hand-drew its own simple moon + 3 dots instead of actually reusing celestial-arc's geometry — same issue as Frame 3. Replaced with the source's real arc path (`M 70 150 Q 500 -30 930 150`, same 1000x200 viewBox) and its own sun/moon positions, ported deterministically. First attempt at the crescent used a hand-tuned two-arc SVG path that silently failed to render (verified via `hyperframes snapshot`, not the Studio preview — see Notes); replaced with an SVG mask (a circle cut by an offset circle), which is a more faithful port of the source's own inset-box-shadow "subtract an offset shape" technique anyway.

## Frame 5 — Step 3: wait 48 hours

scene: 05-wait-48
voiceover: "Retinol reactions can be delayed, so wait 48 hours. A little dryness is normal — but if you see severe redness, stinging, or raised bumps, wash it off. Your skin needs a gentler formula."
duration: 13.404 (VO 12.904 + 0.5 tail)
transition_in: crossfade 0.5s
status: built
src: compositions/frames/05-wait-48.html
type: timeline-ladder
persuasion: safety boundary
beat: step 3 (the video's one coral moment)
blueprint: display headline + 0h->24h->48h vertical ladder + normal-vs-stop split
focal: the coral "STOP" symptom block
roles: ground=paper, highlight=coral (the ONLY coral use in the whole video)
sfx: tick @0.3 (ticking-clock texture under the ladder build, ~7.8s), alert-ping @10.5 (truncated to ~1.3s, on the coral reveal)
narrativeRole: the video's safety boundary and its single voltage moment
keyMessage: wait 48 hours; stop and use a gentler formula on severe reactions
Adapt: user's "checking the spot" + "Wait 48 Hours" on-screen text becomes a vertical timeline ladder (numbered-stack pattern from `videos/snail-mucin-medical-secret/compositions/frames/05-sponge-rule.html`), retimed 0h -> 24h -> 48h.

Scene 5 (0-12.9s): Display text-on-screen "Wait 48 Hours" (EB Garamond) lands at open. Vertical ladder draws down through three rungs — 0H / 24H / 48H — with a progress stroke, paced to land 48H at ~9.0s. At 48H the frame splits into two mono columns: "NORMAL — slight dryness" (ink/`--ink-3`, left) and, on the right, the coral block: "STOP — severe redness, stinging, raised bumps -> wash it off" (coral rule line + coral mono header, `--d-snap` snap-in). Held to scene end.

## Frame 6 — Outro

scene: 06-outro
voiceover: "If your skin looks normal, you're ready to start using it slowly. Check out the description, or head to seoulhabit dot com for our full guide on layering retinol."
duration: 10.553 (VO 10.553, no tail — final frame)
transition_in: crossfade 0.5s
status: built
src: compositions/frames/06-outro.html
type: endcard
persuasion: warm CTA
beat: outro
blueprint: 습 SeoulHabit lockup + CTA pill + cursor-tap beat + disclaimer
focal: "seoulhabit.com" pill
roles: ground=paper, highlight=aqua (underline accent only — coral already spent)
sfx: chime @1.0 (lockup lands)
narrativeRole: close and CTA
keyMessage: seoulhabit.com for the full retinol layering guide
Adapt: user's "smiling, pointing down/to the side" + "seoulhabit.com" on-screen text becomes the standard SeoulHabit endcard pattern (`videos/seoulhabit-launch/compositions/frames/06-cta.html`).

Scene 6 (0-10.5s): 습 SeoulHabit Noto Sans KR text lockup fades/lifts in at open (chime @1.0s). "seoulhabit.com" pill — ink-on-paper with an aqua underline accent — lands at ~3.0s with a cursor-tap beat at ~4.5s. Sub-line "full retinol layering guide" fades in at ~5.5s. Disclaimer microcopy ("General patch-testing guide — not sourced claims, not medical advice"), mono `--ink-3`, sits above the 360px safe-bottom line, visible from ~7.0s. Held to scene end — final frame, no outgoing crossfade.
