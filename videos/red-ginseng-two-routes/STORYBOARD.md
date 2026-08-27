---
format: 1080x1920
duration: 40s
message: "Oral and topical red ginseng aren't interchangeable — each route is backed by a different study, for a different result"
arc: concept-explainer
audience: SeoulHabit's evidence-conscious skincare audience (pdrn / snail-mucin / am-pm series)
mode: collaborative
music: quiet clinical tension, minimal pulse, no percussion swell, thins out under Scene 3-4 voxel renders
---

## Video direction

- **Palette system** (from `frame.md`, never invented): paper `#F7F5F0` ground / ink `#131516` text throughout. Coral `#C97A5C` is the ONE scarce "voltage" accent — at most one coral moment per frame (a citation bracket, a kicker mark), never two. Aqua `#59B8AE` is reserved for the "interrogated / under comparison" mark (Frame 5's accent, per the original brief). Celadon family (`#4F6B52`/`#6F8F72`/`#93B896`) is reserved for "confirmed, at every level" reads — this project's own no-success-color law: celadon never means "winning," it means "sourced." Absence markers ("Not reached") stay neutral ink at reduced opacity, never red/danger. Display type: EB Garamond (headlines, the two VO clauses, the end-card title). Body: Inter. Chrome/mono/citation: JetBrains Mono, matching `frame.md`'s `kicker`/`mono-label`/`code` roles.
- **Motion grammar + reveal model**: `power3` long-tail settles everywhere; no bounce/overshoot. Frame 1 is the only frame with real narration — its reveals are cued to the two VO clauses. Every other frame is silent and paces its reveals to the beat instead, following the same anti-front-load discipline: nothing dumped at t=0, each card/element arrives on its own beat across the frame's full duration. Holds use subtle jitter only — no breathing, no back-half pan/push.
- **Rhythm / held-frame allocation**: Frame 2 (Identity) and Frame 6 (End Card) are the deliberate breather beats — calm, one restrained move, then a still hold. Frames 3–4 (the two routes) and 5 (the comparison) carry the video's density and motion; they build continuously rather than holding early.
- **Framing variety**: Frame 1 Centered · Frame 2 Rule-of-thirds · Frame 3 Layered-depth · Frame 4 Layered-depth (deliberate repeat — see below) · Frame 5 Split-screen · Frame 6 Centered (non-adjacent repeat of Frame 1, fine — both are calm bookends).
- **Deliberate exception**: Frames 3→4 intentionally repeat the Layered-depth framing and share one continuous camera logic (Frame 3 opens deep in the dermis; Frame 4 rises from that same depth to the surface) — this is story-design's "consistent stage" continuity rule for a paired sequence overriding the general "never the same framing twice in a row" guidance, not an oversight.
- **Negative list**: no stock bokeh / purple-blue "AI" gradient cliché; no interface mocks (nothing here is a real UI); no heavy/hard drop-shadows — only `frame.md`'s own defined soft card shadow (hairline + one soft warm shadow, never a heavy drop/glow/gradient); no slideshow front-loading; no screensaver (independently-floating elements with no hierarchy); no citation or number invented beyond the four locked ids (`ING-ginseng-S001/S002/S005/S006`) and the two study headline numbers already in the approved script — the two voxel-render frames' own on-screen "8 WEEKS" / illustrative labels stay visually subordinate to the real CITATION chip, never a second source of truth.

## Frame 1 — The Hook

- scene: Slow, dramatic pan over dried red ginseng roots; minimal type, no diagram, no meter yet.
- voiceover: "The strongest ginseng study never touched skin. It was swallowed."
- duration: 5.094s
- transition_in: cut
- status: animated
- src: compositions/frames/01-hook.html
- type: hook
- persuasion: Contrast — common-belief vs. reality (a skincare study is assumed to test skin; the strongest one here didn't)
- beat: surprise + intrigue
- blueprint: compose (no Hook blueprint fits a slow invented-field pan under VO; composed from the motion vocabulary)
- focal: the two VO clauses (kinetic type is the true hero — no diagram yet, per the outline's own "keep it minimal")
- roles: VO-clause type = foreground subject · amber root-vein linework = background (dim ~40%, invented — not photography, this is a faceless explainer) · "[Authored, marked not-a-claim]" tag = supporting
- sfx: glitch-3

narrativeRole: Opens the cognitive gap the whole video resolves — implies a route distinction exists and matters, before naming what it is.
keyMessage: The best-evidenced result for this ingredient isn't a topical one.
On-screen: small caption "[Authored, marked not-a-claim]" — this line is voice/tone framing, not a cited claim; keep it visually subordinate to the VO.

Shot sequence (Centered framing; VO-paced — this is the one frame with real narration):
Scene 1 (0.0–0.6s): solid ink-dark ground; fine amber root-vein linework begins tracing in via SVG self-draw (`svg-path-draw`) — full-bleed background, dim ~40%, evoking dried root structure without any literal photography (invented visual, per faceless-explainer rules).
Scene 2 (0.6–2.6s): as the VO speaks "The strongest ginseng study never touched skin," it enters via per-word staggered reveal (`dynamic-content-sequencing`) on a `power3` settle, warm-white on dark, lower-third — root linework keeps tracing beneath at low opacity.
Scene 3 (2.6–3.0s): held beat matching the VO's pause — nothing new enters, linework settles.
Scene 4 (3.0–4.4s): "It was swallowed." arrives via per-word staggered reveal on its own line beneath the first — flat, quiet delivery, no emphasis pop (the reversal is in the reveal's plainness, not a flourish).
Scene 5 (4.4–5.0s): the "[Authored, marked not-a-claim]" tag fades in small and low-opacity, lower-third within the caption keep-out; both clauses hold still — subtle jitter (`sine-wave-loop`, low amplitude) only.

## Frame 2 — Identity

- scene: Botanical dossier reveal — raw-ingredient breakdown, like a scientific spec sheet.
- voiceover:
- duration: 5s
- transition_in: crossfade
- status: animated
- src: compositions/frames/02-identity.html
- type: product_intro
- persuasion: Frame-then-fill (state the botanical identity's shape, then populate it)
- beat: clarity + orientation
- blueprint: titlecard-reveal (Reproduce — a calm breather beat, one restrained move, then a still hold)
- focal: the "인삼 · Panax ginseng" headline
- roles: headline = foreground subject · INCI / Botanical lines = supporting · hairline card border = supporting frame
- sfx: click-soft

narrativeRole: Names the one root both routes share, so Frames 3-4 clearly read as two paths from the same subject rather than two unrelated claims.
keyMessage: One root — Panax ginseng — studied two different ways.
On-screen text (verbatim, dossier-card layout):
- 인삼 · Panax ginseng
- INCI: PANAX GINSENG ROOT EXTRACT
- Botanical: Steamed or dried roots
Silent frame by design — no VO line was supplied for this beat; let the dossier card carry it at a calm, held pace rather than inventing narration.

Shot sequence (Rule-of-thirds framing — card anchored lower-middle band, generous negative space above; beat-paced, silent):
Scene 1 (0.0–1.4s): the card's hairline border draws on (`svg-path-draw`) around empty space, centered horizontally in the lower-middle band.
Scene 2 (1.4–3.0s): "인삼 · Panax ginseng" enters via per-word staggered reveal (`dynamic-content-sequencing`), centered within the card on a `power3` settle.
Scene 3 (3.0–4.2s): the INCI line reveals, then the Botanical line one beat after (sequential, not simultaneous) — both center-aligned beneath the headline.
Scene 4 (4.2–5.0s): held read — dossier complete, centered, still; at most subtle jitter (`sine-wave-loop`, low amplitude).

## Frame 3 — Route One: Oral

- scene: Dermal Matrix voxel render — camera opens deep in the dark dermis, looking up at the epidermis far above; a collapsed collagen/elastin web tightens to vibrant amber as bloodstream-delivered extract particles attach. Route/study/citation cards reveal in sequence, not at once.
- voiceover:
- duration: 12s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/03-route-oral.html
- type: feature_showcase
- persuasion: Evidence (citation/source) + Contrast ("surface" and "upper skin" explicitly tagged Not Reached)
- beat: comprehension + conviction
- blueprint: camera-journey (sub-shape B, cursorless flight — Adapt: structure fits [a motivated cinematic dive landing on a payoff], content is this frame's own dermal-matrix world rather than a product surface; keeps the signature move — the continuous dive that lands on a dramatic reveal)
- focal: the collagen/elastin web's amber "REBUILD" transformation
- roles: voxel dermis diagram = foreground subject (fills 40-60% of frame) · capillary + amber-particle field = supporting · FRAME/CLAIM/ROUTE/STUDY/Note/CITATION cards = supporting (reveal in sequence, one per beat)
- sfx: impact-bass-1

narrativeRole: Shows the first route in full: what it is, what it claims, what actually backs the claim, and — expressed as the diagram itself — what it does NOT reach.
keyMessage: Oral ginseng works from inside the dermis; it never touches the skin surface at all.
Key visual — "The Dermal Matrix" (illustrative/conceptual, not a literal claim): voxel-grid 3D render. Pulsing red capillaries release glowing amber particles (the extract) that attach to broken collagen/elastin strands, which tighten and glow vibrant amber — a "REBUILD" transformation, distinct from Frame 4's blue surface glow. Small glowing "BLOODSTREAM" / "SYSTEMIC" labels, a tiny heart/vessel icon, UI scan-line framing. Deep-dermis establishing shot for the pair — Frame 4 rises from here to the surface (continuous world, traversed deep-first to match this script's scene order, reversing the asset brief's literal surface-then-plunge note).
On-screen text (verbatim, reveal as discrete beats synced to the camera move — do not show all six at once):
- FRAME: This route never crosses the surface.
- CLAIM: Restores structural spring and bounce to sagging skin, locks in hydration, and stops chronic peeling and dryness.
- ROUTE: Oral — Systemic (750 mg daily capsules)
- STUDY: 78 randomized individuals, double-blind, placebo-controlled, 24 weeks.
- Note: Results build gradually over a 6-month period and require strict daily compliance.
- CITATION: ⌞ ING-ginseng-S002 ⌟
Diagram tags: "Surface" and "Upper skin" both marked "Not reached."
Silent frame by design — the outline gives a directional "Voiceover Focus: the slow, structural build from within" note, not literal words; honoring VO_MODE=verbatim means not inventing spoken lines to fill that direction. Use it to pace the reveal (slow, deliberate) instead.

Shot sequence (Layered-depth framing, 3 depth layers; beat-paced, silent — "slow, structural build" sets the pacing):
Scene 1 (0.0–1.5s): open deep in the dark dermis (the dive's establishing beat) — collapsed collagen/elastin web visible as a fragile dark line-web in the foreground, capillaries pulse faint red in the mid-ground, epidermis a distant pale band far above.
Scene 2 (1.5–3.2s): "FRAME: This route never crosses the surface." reveals via per-word staggered reveal, upper band, as the camera continues one slow push deeper — no back-half re-push once landed.
Scene 3 (3.2–5.0s): amber light particles release from the capillaries and travel toward the broken web (the dive's mid-flight beat); "CLAIM: …" reveals beneath the FRAME line.
Scene 4 (5.0–7.0s): particles attach — the web tightens and blooms vibrant amber (`ambient-glow-bloom`, the signature move's dramatic landing); "ROUTE:" card reveals, then "STUDY:" one beat after.
Scene 5 (7.0–9.5s): "Note:" reveals; "Surface" / "Upper skin" tags fade in at the top of frame reading "Not reached" — muted ink at reduced opacity, an absence marker, never red/danger or celadon.
Scene 6 (9.5–11.0s): "CITATION — ⌞ ING-ginseng-S002 ⌟" lands last in JetBrains Mono, the coral bracket accent (this frame's one voltage moment).
Scene 7 (11.0–12.0s): held read — full amber transformation + all cards visible, camera settles to a stop; subtle jitter (`sine-wave-loop`, low amplitude) only, no continuing push.

## Frame 4 — Route Two: Topical

- scene: Epidermal Scan voxel render — camera rises from Frame 3's dermis back to the surface; an amber serum droplet impacts from above and blue light smooths glowing wrinkle lines, confined to the uppermost strata only. Route/study/citation cards reveal in sequence, not at once.
- voiceover:
- duration: 10s
- transition_in: crossfade
- status: animated
- src: compositions/frames/04-route-topical.html
- type: feature_showcase
- persuasion: Evidence (citation/source) + Contrast (mirrors Frame 3 — this time the surface IS reached, the dermis is not the target)
- beat: comprehension + momentum
- blueprint: camera-journey (sub-shape B, cursorless flight — Adapt: continues Frame 3's world, traveling the opposite direction [rising to the surface] and landing on the "SMOOTH" payoff instead of "REBUILD"; keeps the signature move)
- focal: the blue-light wrinkle-smoothing moment
- roles: voxel epidermis diagram = foreground subject (fills 40-60% of frame) · serum droplet + blue-glow field = supporting · FRAME/CLAIM/ROUTE/STUDY/Note/CITATION cards = supporting (reveal in sequence, one per beat)
- sfx: whoosh-short, sparkle

narrativeRole: Shows the second route in full, on the same visual stage as Frame 3, so the viewer directly contrasts what each route reaches.
keyMessage: Topical ginseng acts fast, but only at the surface it can physically touch.
Key visual — "The Epidermal Scan" (illustrative/conceptual, not a literal claim): semi-transparent voxel-grid cross-section of skin, cool blue + amber/red + glowing white. An amber serum droplet impacts the surface from above; blue glow radiates only in the uppermost strata (Stratum Corneum and just below) while the deep dermis stays dark — the visual inverse of Frame 3's deep-only glow. Glowing jagged "wrinkle" lines visibly smooth as the blue light pulses over them (a "SMOOTH" graphic). Small timer icon + glowing "8 WEEKS" near the smoothed-wrinkle graphic — explicitly illustrative time-to-effect, not a restated citation (the real, sourced duration is in the STUDY line below). Steady illustrative tilt/zoom, gentle depth of field. Continuous camera logic with Frame 3 (see Frame 3's narrative note on traversal order).
On-screen text (verbatim, reveal as discrete beats synced to the camera move — do not show all six at once):
- FRAME: This route starts at the surface.
- CLAIM: Significantly reduces wrinkle depth, smooths out eye area crow's feet, and plumps facial skin.
- ROUTE: Topical (1.0% to 5.0% enzyme-modified or steamed extract)
- STUDY: 23 healthy subjects with visible wrinkles, 8 weeks.
- Note: Wrinkle reduction is highly dependent on the bioavailable rare ginsenosides; standard white extracts may require 12–24 weeks for comparable results.
- CITATION: ⌞ ING-ginseng-S001 · S005 · S006 ⌟
Silent frame by design — outline gives "Voiceover Focus: the targeted, surface-level correction" as direction, not literal words; same verbatim-mode handling as Frame 3.

Shot sequence (Layered-depth framing — deliberate repeat of Frame 3, see Video direction; beat-paced, silent — "targeted, surface-level" sets a faster pace than Frame 3):
Scene 1 (0.0–1.2s): camera continues rising from Frame 3's dermis (matched direction/velocity across the crossfade cut) breaking into the upper strata — voxel layers become visible, the deep dermis dims below and stays visibly dark.
Scene 2 (1.2–2.6s): the amber serum droplet impacts the surface from above (`motion-blur-streak` on its fast arrival); "FRAME: This route starts at the surface." reveals.
Scene 3 (2.6–4.4s): blue light radiates outward from the impact point, confined to the uppermost strata only (`ambient-glow-bloom`, capped hard at the strata boundary — the contrast beat against Frame 3's deep-only glow); "CLAIM: …" reveals.
Scene 4 (4.4–6.2s): the glowing jagged wrinkle lines visibly smooth as the blue pulse crosses them (`svg-path-draw` reversing/softening the jagged path — the signature payoff); "ROUTE:" card reveals, then "STUDY:" one beat after.
Scene 5 (6.2–8.2s): "Note:" reveals; "Surface — reached" / "Dermis — not the target" tags fade in, aqua-tinted this time (surface genuinely is reached here, mirroring but inverting Frame 3's neutral "not reached" tags).
Scene 6 (8.2–9.2s): "CITATION — ⌞ ING-ginseng-S001 · S005 · S006 ⌟" lands in JetBrains Mono, the coral bracket accent.
Scene 7 (9.2–10.0s): held read — smoothed wrinkle + all cards visible, settles still; subtle jitter only.

## Frame 5 — The Comparison

- scene: Both route markers land on one block; an aqua accent highlights the element under scrutiny; EvidenceMeter lockup (claim + source chips + meter) weighs Oral against Topical side by side.
- voiceover:
- duration: 5s
- transition_in: cut
- status: animated
- src: compositions/frames/05-comparison.html
- type: social_proof
- persuasion: Contrast — comparison of two options
- beat: recognition + clarity
- blueprint: comparison-split (Adapt, cross-role from Key_Feature — nothing in social_proof's own menu pairs two items side by side; keeps the signature move: mirrored 3D book-open tilts from opposite wings, holding side-by-side at equal weight)
- focal: the Oral vs. Topical pairing
- roles: two comparison columns = foreground subject (co-equal weight) · EvidenceMeter lockup = supporting · "Same root. Different journeys." headline = supporting (sets up the pair)
- sfx: click-soft, chime

narrativeRole: States the thesis explicitly by placing both routes' evidence side by side — this is where "same root, different journeys" crystallizes, later than the usual beat-2 landing because the compare/contrast structure earns that line by first showing both routes in full (Frames 3-4).
keyMessage: Same root. Two different, non-interchangeable evidence bases.
On-screen text (verbatim):
- FRAME: Same root. Different journeys.
- Oral: 78 people, 24 weeks.
- Topical: 23 people, 8 weeks.
- CITATION: ⌞ S002 · S001 ⌟
Silent frame by design — no VO given; let the side-by-side numbers and the EvidenceMeter do the talking.

Shot sequence (Split-screen framing — new framing for this frame; beat-paced, silent):
Scene 1 (0.0–1.0s): "Same root." enters center in ink, held type; "Different journeys." follows immediately in aqua (the interrogated-element accent) — per-word staggered reveal.
Scene 2 (1.0–2.6s): the Oral column enters from the left wing with a mirrored 3D book-open tilt (`split-tilt-cards`, the signature move), settling with "78 people / 24 weeks."
Scene 3 (2.6–4.0s): the Topical column enters from the right wing with the opposing tilt, settling with "23 people / 8 weeks" — both columns now held side-by-side at equal weight.
Scene 4 (4.0–4.6s): the EvidenceMeter lockup blooms in beneath (`ambient-glow-bloom`), aqua accent on the interrogated element per the brief's claim+chips+meter concept.
Scene 5 (4.6–5.0s): "CITATION — ⌞ S002 · S001 ⌟" lands last in JetBrains Mono; brief held read into the cut.

## Frame 6 — End Card

- scene: Calm, information-dense hold — brand lockup, title, sourcing line. No new claims, no motion flourish.
- voiceover:
- duration: 3s
- transition_in: crossfade
- status: animated
- src: compositions/frames/06-endcard.html
- type: branding
- persuasion: Distillation (compress the whole piece to one credibility line)
- beat: resolve + trust
- blueprint: titlecard-reveal (Reproduce — calm landing beat, exactly one restrained move, then a still hold)
- focal: the SeoulHabit brand lockup
- roles: brand lockup (mark + title + tagline) = foreground subject · paper ground = background
- sfx: chime

narrativeRole: Closes on credibility rather than a new claim — the payoff of "here's what was actually tested," not a sales ask.
keyMessage: Every claim in this video traces to a real source.
On-screen text (verbatim):
- 습 SeoulHabit
- Red Ginseng: What the Studies Actually Tested
- Sources on every claim.
Silent frame by design — no VO given; the stillness itself is the tone (frame.md's "restraint" law applies hardest here).

Shot sequence (Centered framing — non-adjacent repeat of Frame 1, both calm bookends; beat-paced, silent):
Scene 1 (0.0–1.2s): the full lockup (습 SeoulHabit mark, title, tagline) enters together as ONE restrained move — a slide-up crossfade, centered.
Scene 2 (1.2–3.0s): held, still — no further motion; at most subtle jitter (`sine-wave-loop`, low amplitude). The calm hold IS the close.
