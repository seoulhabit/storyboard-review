---
format: 1080x1920
duration: 113.84s
message: "Snail mucin has a wild medical origin story, a genuine biological reason it works, and one easy-to-miss application step — not TikTok magic"
arc: story-explainer with process
audience: "TikTok/shorts skincare audience who've seen the snail-mucin trend and want the real story behind it"
mode: autonomous
music: "low cinematic bass swell for the hook, settling into a curious upbeat TikTok-explainer bed, thins under narration"
---

## Video direction — REVISED 2026-08-28: literal script fidelity

**This build replaces an earlier evidence-tuned version** that hedged every
claim and used invented vector graphics throughout. The user's `/goal`
Stop-hook rejected that build for not matching the pasted script and its
literal shot list. This revision follows the script verbatim (see
`SCRIPT.md`) and reconstructs every described shot as a real photographic
image (generated via Higgsfield `soul_2`, stored under `public/`) rather
than invented typographic graphics — the closest a faceless-explainer
pipeline (no footage capture) can get to the literal "macro shot," "B-roll,"
and "cinematic" language in the brief. There is no Claims Inventory and no
citation apparatus in this revision — the script asserts its claims
directly and this build shows it that way.

- **type**: on-screen labels/section titles = Bricolage Grotesque (display) /
  JetBrains Mono (chrome), matching the pipeline's usual type ramp — but the
  frame's visual hero in every scene is now a photographic image, not an
  invented graphic.
- **motion grammar**: `power3` long-tail settles on text overlays; slow Ken
  Burns push/pan on every photographic hero (the substitute for real camera
  movement/B-roll motion within a still image) — never a static crop.
- **rhythm**: no deliberate "held" frames this time — the piece runs at
  TikTok pace throughout, matching the source script's energy.
- **negative list**: no invented vector glyphs standing in for a shot the
  script describes as real (that was the prior build's mismatch); no
  citation chips; no hedging language layered onto the spoken lines.

## Voice change + full retime — 2026-08-29

**Voice switched to Kimberly** (explicit user request); full rationale,
duration/loudness comparison, and decision trail are in `BRIEF.md`'s
"Voice change + full retime" Notes bullet — not duplicated here. New global
frame structure: starts at 0 / 13.52 / 27.84 / 52.96 / 74.0 / 98.64s, total
**113.84s** (was 117.421s).

**Every per-scene timestamp in the Frame sections below predates this
retime** and reflects the *original* HeyGen voice's pacing — kept as the
historical authoring record of the shot design (which beat follows which
clause, why a cut lands where it does), not as current timing. The actual
current timing lives in the composition files themselves
(`compositions/frames/*.html`, `index.html`), each retimed line-by-line
against Kimberly's real per-word transcript. The shot design itself (what
happens, in what order, on which clause) is unchanged by the retime — only
the numbers moved.

**Frame 3 ingredient cards redesigned same day (legibility fix, user-flagged):**
the three `grid-card-assemble` mounts were stacked at 210px tall each so all
three stayed visible as a growing checklist — confirmed via a live
`getComputedStyle` probe that this rendered ingredient text at 7.2px/6px
(label/body), unreadable, since the component sizes text as a percentage of
its own mount height. Redesigned to swap-in-place: all three now share one
750px-tall region and appear one at a time (cards 1-2 exit via the
component's own `exit:"fade"`, card 3 holds), which resolves to a
width-capped ~23px/~20px — see the inline comment in
`compositions/frames/03-chemistry.html` for the full before/after math. This
changes the frame's visual metaphor from an accumulating list to a cycling
spotlight; the VO-cue timing each card lands on is unchanged.

## Frame 1 — Hook: The Bizarre History

- scene: A vintage black-and-white 1960s lab-footage still, then a hard cut to a hyper-crisp macro photo of clear slime being pulled apart by a metal spatula.
- voiceover: "In the 1960s, a Spanish doctor trying to heal severe radiation burns stumbled onto a bizarre, miraculous cure. Fast forward to today, and that exact same goo is the beauty industry's biggest, weirdest obsession."
- duration: 15.125s
- transition_in: cut
- status: animated
- src: compositions/frames/01-hook.html
- type: hook
- persuasion: Historical revelation + counterintuitive claim
- beat: surprise + intrigue
- blueprint: kinetic-type-beats (Hook-escalation, Adapt)
- focal: Scene 1 the real B&W archival lab photo (`public/01a-archival-lab.png`); Scenes 2-4 the real macro slime/spatula photo (`public/01b-macro-slime-spatula.png`)
- roles: archival photo = foreground subject, full-bleed (Scene 1) · macro slime photo = foreground subject, full-bleed (Scenes 2-4) · VO captions/lead-in text = supporting overlay
- sfx: vintage-film-projector-click (Scene 1 open, under the "1960s · Spain" label pop; retriggers at the 2.40s snap-cut as a film-reel-skip accent), bass-drop-cinematic (Scene 1→2 hard cut), squish-stretch-asmr (over the macro slime hold), sparkle (payoff word)

narrativeRole: Opens on the real, strange 1960s origin story before the hard cut to the visceral macro slime shot that IS the video's hook image.
keyMessage: Snail mucin's TikTok fame traces back to a specific, bizarre medical origin story.

Adapt: keep kinetic-type-beats' hard-cut escalation signature, but the "beats" are real photographs full-bleed under text overlays rather than invented type cards — this frame is photo-led, not type-led.

Scene 1 (0.0–5.4s): `public/01a-archival-lab.png` fills the frame full-bleed (a subtle grayscale/high-contrast filter + light grain overlay reinforces "vintage footage"), dimmed ~35% under a mono "1960s · SPAIN" label. As the VO says "In the 1960s, a Spanish doctor trying to heal severe radiation burns" (0.10–5.20s), a caption line per-word-reveals lower-third (clear of the caption band). A fast whip-blur snap-cut at 2.40–2.64s (same photo, punched in and reframed — no second angle exists for this beat) breaks the hold into two sub-3s visual beats, so the 1960s-to-modern transition reads as rapid cuts rather than one long static hold; text/label overlays sit outside the punched layer and stay crisp through it.

Scene 2 (5.4–8.7s): hard cut — `public/01b-macro-slime-spatula.png` fills the frame full-bleed, slow Ken Burns push-in begins (runs through Scene 4). On "stumbled onto a bizarre, miraculous cure" (5.64–8.52s), the phrase per-word-reveals over the image, upper-third.

Scene 3 (8.7–10.3s): Ken Burns push continues; on "Fast forward to today," (8.96–10.14s), the line clears and the next reveals beneath it.

Scene 4 (10.3–15.125s): on "and that exact same goo is the beauty industry's biggest, weirdest obsession" (10.46–14.86s), the payoff word "OBSESSION" spring-pops (power3, capped back.out(1.4)) dead-center over the image on a translucent dark scrim for legibility, landing exactly on the word (14.28–14.86s); holds, Ken Burns push settling to a stop, through the frame's real end at 15.125s.

## Frame 2 — Intro: The Yuck Factor

- scene: A fast montage feel built from a real skincare-routine photo (hands patting product), then the "SNAIL SECRETION FILTRATE" ingredient-label callout as on-screen type.
- voiceover: "Welcome to the weird world of Snail Mucin. Today, we're stripping away the TikTok hype and diving into the actual, microscopic science of what this slime does to your face — and the huge mistake you're probably making when you use it."
- duration: 13.845s
- transition_in: crossfade
- status: animated
- src: compositions/frames/02-intro.html
- type: product_intro
- persuasion: Frame-then-fill + signposting
- beat: orientation + anticipation
- blueprint: kinetic-type-beats (Product_Intro namedrop, Reproduce)
- focal: the real skincare-routine photo (`public/02-routine-montage.png`) as full-bleed backdrop; "SNAIL MUCIN" title lockup and "SNAIL SECRETION FILTRATE" label callout as the foreground type
- roles: routine photo = background, full-bleed, dimmed ~40% · "SNAIL MUCIN" title = foreground subject · "THE YUCK FACTOR" mono kicker = supporting · "SNAIL SECRETION FILTRATE" label callout = supporting, arriving late
- sfx: click-soft (title lands), whoosh-soft (label callout arrives)

narrativeRole: Names the video's honest angle — cutting through TikTok hype — using the real routine photo as atmosphere behind the title.
keyMessage: This video strips away the hype and explains the actual science of snail mucin, including the mistake most people make.

Reproduce: kinetic-type-beats' Product_Intro namedrop shape, now photo-backed — the routine photo plays continuously beneath the type beats instead of a flat color field.

Scene 1 (0.0–2.7s): `public/02-routine-montage.png` fills the frame full-bleed, dimmed ~40%, slow Ken Burns drift. On "Welcome to the weird world of Snail Mucin" (0.26–2.52s), a mono "THE YUCK FACTOR" kicker per-word-reveals, and "SNAIL MUCIN" title spring-pops center, Bricolage Grotesque 500, cream on the dimmed photo.

Scene 2 (2.7–5.5s): on "Today, we're stripping away the TikTok hype" (2.90–5.38s), the title settles smaller upper-third, making room below it.

Scene 3 (5.5–10.7s): on "and diving into the actual, microscopic science of what this slime does to your face —" (5.68–10.56s), a JetBrains Mono label callout "SNAIL SECRETION FILTRATE" wipes in lower-third — the ingredient-label beat from the brief, rendered as clean type since a photoreal label can't reliably show real legible text.

Scene 4 (10.7–13.845s): on "and the huge mistake you're probably making when you use it" (10.84–13.60s), a small "COMING UP: THE MISTAKE" mono tag lands beneath the label callout; holds to the frame's real end at 13.845s.

## Frame 3 — The Mad Science of Slime

- scene: High-contrast dark background with a real macro droplet photo; glowing type tracks the chemical breakdown — Glycolic Acid, Allantoin, Hyaluronic Acid.
- voiceover: "This isn't just water and goo. Snails secrete this specific mucin to instantly heal their own bodies when they get cut sliding over sharp rocks. It is naturally loaded with Glycolic Acid to eat away dead skin, Allantoin to heal wounds, and massive doses of Hyaluronic Acid. It's basically an anti-aging, barrier-repairing super-serum — perfectly engineered by nature."
- duration: 25.496s
- transition_in: crossfade
- status: animated
- src: compositions/frames/03-chemistry.html
- type: feature_showcase
- persuasion: Concretization + escalating enumeration
- beat: fascination + awe
- blueprint: grid-card-assemble (Benefits vertical-list, BUILD, Reproduce)
- focal: the real macro droplet photo (`public/03-macro-droplet.png`) as full-bleed dark backdrop; three glowing ingredient callouts as the foreground type list
- roles: droplet photo = background, full-bleed, dimmed ~50% · ingredient list (GLYCOLIC ACID / ALLANTOIN / HYALURONIC ACID) = foreground subject · closing payoff line = foreground subject
- sfx: click-soft ×3 (each ingredient lands), sparkle (final payoff line)

narrativeRole: Delivers the "mad science" chemistry beat exactly as scripted — real ingredients, escalating to the "perfectly engineered by nature" payoff.
keyMessage: Snail mucin is naturally loaded with Glycolic Acid, Allantoin, and Hyaluronic Acid — an anti-aging, barrier-repairing super-serum.

Reproduce: grid-card-assemble's vertical BUILD list, photo-backed — the droplet image sits beneath the whole sequence instead of a flat dark color field.

Scene 1 (0.0–2.2s): `public/03-macro-droplet.png` fills the frame full-bleed, dimmed ~50%, slow Ken Burns push begins (runs the whole frame). On "This isn't just water and goo." (0.18–2.02s), a glowing mono lead-in line per-word-reveals upper-third.

Scene 2 (2.2–9.2s): on "Snails secrete this specific mucin to instantly heal their own bodies when they get cut sliding over sharp rocks." (2.52–9.02s), an empty three-slot list region establishes in the top ~83% (caption-band clear), and a small glowing "PROTECT + REPAIR" tag settles beneath the lead-in line.

Scene 3 (9.2–14.0s): on "It is naturally loaded with Glycolic Acid to eat away dead skin," (9.42–13.86s), item 1 spring-pops into the list, glowing shell-accent text: "GLYCOLIC ACID" + "eats away dead skin."

Scene 4 (14.0–16.1s): on "Allantoin to heal wounds," (14.26–15.92s), item 2 assembles beneath: "ALLANTOIN" + "heals wounds."

Scene 5 (16.1–19.0s): on "and massive doses of Hyaluronic Acid." (16.32–18.84s), item 3 assembles, emphasized larger than items 1-2 (the "massive doses" escalation): "HYALURONIC ACID" + "massive doses."

Scene 6 (19.0–25.496s): on "It's basically an anti-aging, barrier-repairing super-serum — perfectly engineered by nature." (19.28–25.28s), the list clears (velocity-matched cut) to a single glowing payoff line — "PERFECTLY ENGINEERED BY NATURE" — dead-center, landing on "perfectly engineered by nature" (23.58–25.28s) and holding through the frame's real end at 25.496s.

## Frame 4 — The Snail Spa

- scene: Cinematic, dark, moody B-roll of a real snail gliding across a mesh net.
- voiceover: "And if you're picturing a snail torture chamber, stop. The modern extraction process is basically a luxury spa for mollusks. They naturally prefer the dark, so they are placed in quiet, dark rooms to roam freely over mesh nets. The mucin they leave behind is collected, purified, and bottled. Zero harm, zero stress."
- duration: 23.171s
- transition_in: crossfade
- status: animated
- src: compositions/frames/04-snail-spa.html
- type: feature_showcase
- persuasion: Myth-busting reassurance
- beat: relief + reassurance
- blueprint: titlecard-reveal (Adapt)
- focal: the real cinematic snail-on-mesh photo (`public/04-snail-mesh.png`) as full-bleed hero
- roles: snail-on-mesh photo = foreground subject, full-bleed · "LUXURY SPA FOR MOLLUSKS" headline = supporting overlay · "ZERO HARM, ZERO STRESS" closing line = supporting overlay, landing last
- sfx: record-scratch (on the "TORTURE CHAMBER?" pop, 2.40s — resets attention on the myth callout itself), whoosh-soft (myth-bust cut), click-soft (closing line lands), click-soft (CRUELTY-FREE tag lands, 21.2s)

narrativeRole: Directly answers and dismisses the "torture chamber" worry using the real moody B-roll photo as proof-of-mood.
keyMessage: Snail mucin is collected in a quiet, dark, spa-like setting — zero harm, zero stress.

Adapt: titlecard-reveal's one-restrained-move-then-hold signature, photo-backed — the "card" IS the full-bleed B-roll photo with a slow Ken Burns drift instead of a flat color card.

Scene 1 (0.0–3.9s): a brief dark scrim with mono "TORTURE CHAMBER?" per-word-reveals center, small scale, on "And if you're picturing a snail torture chamber, stop." (0.18–3.58s).

Scene 2 (3.9–9.1s): hard cut — `public/04-snail-mesh.png` fills the frame full-bleed, slow Ken Burns drift begins (runs the rest of the frame). "LUXURY SPA FOR MOLLUSKS" headline settles upper-third via one restrained wipe, on "The modern extraction process is basically a luxury spa for mollusks." (4.38–8.82s).

Scene 3 (9.1–15.9s): on "They naturally prefer the dark, so they are placed in quiet, dark rooms to roam freely over mesh nets." (9.30–15.60s), a small supporting caption line reveals lower-third, clear of the caption band; Ken Burns drift continues over the snail photo.

Scene 4 (15.9–20.4s): on "The mucin they leave behind is collected, purified, and bottled." (16.20–20.16s), a second supporting caption line reveals beneath the first, replacing it.

Scene 5 (20.4–23.171s): on "Zero harm, zero stress." (20.86–22.86s), "ZERO HARM, ZERO STRESS" lands as the closing headline, spring-pop settle, holding through the frame's real end at 23.171s. A small "CRUELTY-FREE" chip spring-pops in beneath it at 21.2s — on-screen only, added per reviewer feedback; the spoken line stays exactly as scripted (verbatim VO), since "cruelty-free" is a more specific claim (normally about animal testing, not sourcing) than "zero harm, zero stress" itself asserts.

## Frame 5 — The Sponge Metaphor (How to Not Ruin Your Skin)

- scene: A literal side-by-side visual test — a bone-dry sponge with serum sitting inert on the left, a misted sponge absorbing serum on the right.
- voiceover: "But here is why people claim snail mucin \"dried out\" their skin. It's a master humectant — a moisture magnet. If you put it on a bone-dry face, it panics and pulls hydration out of the deep layers of your skin. You have to apply it to a damp face. Mist, pat the slime in — never rub — and immediately trap it with a moisturizer."
- duration: 21.603s
- transition_in: push-slide UP
- status: animated
- src: compositions/frames/05-sponge-rule.html
- type: feature_showcase
- persuasion: Before/after demonstration + signposting
- beat: focus + mastery
- blueprint: comparison-split (Adapt)
- focal: the real dry-sponge photo (`public/05a-dry-sponge.png`) left / real misted-sponge photo (`public/05b-wet-sponge.png`) right, the literal side-by-side test from the brief
- roles: dry-sponge photo = foreground subject, left half · misted-sponge photo = foreground subject, right half · "MOISTURE MAGNET" headline = supporting overlay · step captions (mist / pat / seal) = supporting, arriving late
- sfx: whoosh-soft (split reveal), click-soft ×3 (mist / pat / seal captions land)

narrativeRole: Delivers the practical payoff exactly as scripted — a literal before/after sponge test proving the humectant mechanism, then the fix.
keyMessage: Snail mucin needs damp skin — mist first, pat it in, then seal with a moisturizer, or the humectant effect works against you.

Adapt: comparison-split's mirrored book-open two-item signature, cast with the brief's literal dry-vs-misted sponge photos instead of abstract cards.

Scene 1 (0.0–4.7s): "THE MISTAKE" mono setup line on a dark scrim, on "But here is why people claim snail mucin \"dried out\" their skin." (0.12–4.44s).

Scene 2 (4.7–7.8s): "MOISTURE MAGNET" headline spring-pops centered, on "It's a master humectant — a moisture magnet." (4.92–7.50s).

Scene 3 (7.8–10.3s): the headline clears; `public/05a-dry-sponge.png` and `public/05b-wet-sponge.png` book-open in from opposite sides with mirrored 3D tilts, settling side-by-side (left = dry, right = misted) — the split-screen visual test named in the brief. On "If you put it on a bone-dry face," (7.92–9.70s), a small caption reveals beneath the dry (left) side.

Scene 4 (10.3–14.0s): on "it panics and pulls hydration out of the deep layers of your skin." (10.10–13.80s), the dry-sponge (left) side pulses/dims slightly to sell "panics," the caption beneath it updating.

Scene 5 (14.0–16.4s): on "You have to apply it to a damp face." (14.28–16.20s), the misted (right) side brightens/scales slightly to draw the eye; a caption reveals beneath it.

Scene 6 (16.4–19.3s): on "Mist, pat the slime in — never rub —" (16.64–19.06s), the two photos clear (velocity-matched cut) to a compact 2-step caption stack — "MIST" then "PAT — NEVER RUB" — landing one per clause over a plain dark ground.

Scene 7 (19.3–21.603s): on "and immediately trap it with a moisturizer." (19.14–21.38s), step 3 — "SEAL IT IN" — lands the same way; all three steps hold together, settled through the frame's real end at 21.603s.

## Frame 6 — Outro

- scene: A glowing cheekbone catching the light in a dark room, with "Would you try it?" and "Subscribe!" text overlays.
- voiceover: "From healing radiation burns to unlocking flawless glass skin... nature is wild. So, are you brave enough to try it, or is the yuck-factor too high? Let the debate begin in the comments. Subscribe for more skincare science, and I'll see you in the next one."
- duration: 18.181s
- transition_in: crossfade
- status: animated
- src: compositions/frames/06-outro.html
- type: cta
- persuasion: Callback (return to the hook's history) + direct challenge
- beat: resolve + invitation
- blueprint: titlecard-reveal (CTA end-card, Adapt)
- asset_candidates: public/06-cheekbone-glow.png — the real glowing-cheekbone beauty photo specified as the outro shot in the brief
- focal: the real glowing-cheekbone photo (`public/06-cheekbone-glow.png`), full-bleed
- roles: cheekbone photo = foreground subject, full-bleed · "WOULD YOU TRY IT?" text overlay = supporting · "SUBSCRIBE!" text overlay = supporting, landing last
- sfx: whoosh-soft (photo reveal), sparkle (subscribe text lands)

narrativeRole: Closes on the exact callback and CTA the script asks for — the origin-to-glass-skin journey, then a direct challenge and subscribe ask.
keyMessage: Snail mucin's journey from radiation burns to glass skin is wild — try it, or don't, but subscribe either way.

Adapt: titlecard-reveal's single-restrained-reveal-then-hold signature; the "card" is the real cheekbone photo, and BOTH text overlays named in the brief ("Would you try it?" and "Subscribe!") land explicitly, in that order.

Scene 1 (0.0–4.5s): `public/06-cheekbone-glow.png` fades in full-bleed and scales slightly (~95%→100%, smooth ease-out), slow Ken Burns push running through the rest of the frame. On "From healing radiation burns to unlocking flawless glass skin..." (0.14–4.18s), a caption line per-word-reveals lower-third.

Scene 2 (4.5–6.4s): on "nature is wild." (4.94–6.12s), the caption swaps to this short emphasis line, same position.

Scene 3 (6.4–9.3s): on "So, are you brave enough to try it," (6.84–8.98s), "WOULD YOU TRY IT?" text overlay spring-pops in upper-third over the photo.

Scene 4 (9.3–11.4s): on "or is the yuck-factor too high?" (9.42–11.08s), the question overlay settles/completes with a small emphasis pulse on "yuck-factor."

Scene 5 (11.4–13.7s): on "Let the debate begin in the comments." (11.66–13.42s), a small supporting caption reveals beneath the question, clear of the caption band.

Scene 6 (13.7–18.181s): on "Subscribe for more skincare science, and I'll see you in the next one." (13.84–18.02s), "SUBSCRIBE!" text overlay spring-pops in, larger, dead-center-lower; everything holds — photo, both text overlays — settled through the frame's real end at 18.181s. This is the video's true exit; no further transition follows.
