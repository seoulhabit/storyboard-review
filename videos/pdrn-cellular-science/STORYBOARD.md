---
format: 1080x1920
duration: 60s
message: "PDRN is a real regenerative-medicine ingredient — this video keeps the original claims and shows plainly which ones trace to a real record and which don't"
arc: hook → identity → history → mechanism → fibroblasts → cta
audience: SeoulHabit's evidence-conscious skincare audience (pdrn / red-ginseng / snail-mucin series)
mode: collaborative
music: none (VO carries the full runtime; light BGM bed under all six beats, ducked well beneath narration)
---

## Video direction

- **Palette** (from `frame.md`, canonical house tokens, never remixed): `paper #F7F5F0` ground / `ink #131516` text throughout. `Coral #C97A5C` is the one scarce "voltage" accent — at most one coral moment per frame (a citation bracket or kicker), never two. `Aqua #59B8AE` marks the one "interrogated/under comparison" element per frame. `Celadon` family (`#4F6B52`/`#6F8F72`/`#93B896`) means "sourced, at every evidence level" — never a success/failing-grade color. The new `UNSOURCED` flag (`ink-faint`, no bracket, never coral/celadon/aqua/red) sits in the citation slot on any beat carrying an unsourced claim. Display type: EB Garamond (FRAME lines, headlines). Body: Inter (CLAIM/ROUTE/STUDY text, kinetic hook type). Chrome/mono/citation: JetBrains Mono.
- **Motion grammar**: `power3.out` long-tail settles everywhere; no bounce/overshoot/elastic. Every frame is VO-paced (all six beats carry real narration, per the explicit audio decision) — reveals are cued to VO phrase boundaries, not a silent beat-paced clock. Frame zero on every ported component (EvidenceMeter, SplitFaceProtocol) stays the dense, fully-built pause state.
- **Framing**: Frame 1 Centered (hook) · Frame 2 Rule-of-thirds (identity card) · Frame 3 Layered-depth (history diagram + claim panel + evidence coda) · Frame 4 Layered-depth (mechanism, deliberate repeat — continuous "cell surface" world, see below) · Frame 5 Centered (fibroblast factory) · Frame 6 Split-screen (SplitFaceProtocol).
- **Deliberate continuity**: Frames 3→4 both work in "just under the skin surface" depth — Frame 3's cell-multiplication visual and Frame 4's A2A-receptor cell-surface zoom share one visual world, traversed continuously across the crossfade, mirroring red-ginseng's Frame 3→4 continuous-camera convention for a paired sequence.
- **Negative list (Frames 2 and 3 only, as originally authored)**: no flash-color strobes, no rotating hero DNA helix, no bass-drop-timed hard color flashes, no glow beyond one bounded `ambient-glow-bloom` moment per beat. **Frames 1, 4, 5, and 6 deliberately break this list** per an explicit Round 2 "high-retention visual" brief — see `BRIEF.md`'s Round 2 section for the exact swap-by-swap mapping and the reasoning. Still true everywhere, unchanged by Round 2: no citation or source id invented beyond the three locked ids (`ING-pdrn-S001/S003/S004`) — every other specific claim in this script gets the `UNSOURCED` flag, never a fabricated id, and no claim panel or marker was touched by the visual pass.

## Frame 1 — The Hook

- scene: [Round 2] A dark glow-lit stage holding a quick cut from a glowing glass-skin orb to a
  glowing lab vial; "SALMON DNA?" survives as a small kinetic caption over the visual.
- voiceover: "People are applying Salmon DNA to their skin, but this isn't just a weird trend—it's actually a medical breakthrough."
- duration: 8s
- transition_in: cut (cold open)
- status: animated
- src: compositions/frames/01-hook.html
- type: hook
- persuasion: Contrast — common assumption (a weird trend) vs. reframe (a medical breakthrough)
- beat: surprise + intrigue
- blueprint: compose, revised (a glowing visual quick-cut is now the hero; caption text is supporting)
- focal: the glass-skin-orb → lab-vial quick cut
- roles: glowing orb/vial = foreground subject · dark stage box = frame · "SALMON DNA?" caption = supporting · small dropper-turned-vial motif folded into the vial cut
- sfx: impact-bass-1, glitch-3

narrativeRole: Opens the cognitive gap the video resolves — names the strange-sounding fact before explaining it.
keyMessage: This isn't a gimmick — treat it as a real, if surprising, ingredient.
On-screen: "SALMON DNA?" (small kinetic caption, per-word reveal, over the glow visual) — a hook headline, not a claim; no marker needed.

Shot sequence (Centered framing; VO-paced) — [Round 2 revision, replacing the plain-text opening]:
Scene 1 (0.0–1.2s): matte paper ground with fine grain, as VO begins — unchanged.
Scene 2 (1.2–2.3s): a dark stage box blooms in; a glowing, dewy "glass skin" orb (radial-gradient sphere with a soft aqua bloom) scales in behind it; "SALMON DNA?" reveals per-word as a small caption above, timed to VO's "applying Salmon DNA to their skin."
Scene 3 (3.3–3.55s): a quick cut — the orb drops out and a sleek, glowing modern lab vial cuts in, timed to VO's "isn't just a weird trend."
Scene 4 (5.6–7.2s): "—it's actually a medical breakthrough" lands as before, coral underline draws on once (this frame's one voltage moment) — unchanged from the original cut.
Scene 5 (7.2–8.0s): held read, subtle jitter only, settling into the cut.

## Frame 2 — What PDRN Is

- scene: Identity dossier card — nominal fields only (name, source, what it physically is), plus the biocompatibility claim, flagged.
- voiceover: "It's called PDRN, or Polydeoxyribonucleotide. It's extracted and highly purified from salmon because these specific DNA fragments are highly biocompatible with humans—meaning they won't trigger an allergic immune response."
- duration: 10s
- transition_in: cut
- status: animated
- src: compositions/frames/02-identity.html
- type: product_intro
- persuasion: Frame-then-fill (name it, then say what it is)
- beat: clarity + orientation
- blueprint: titlecard-reveal, adapted (a calm identity beat, then one flagged claim)
- focal: the "PDRN" identity card
- roles: identity card = foreground subject · DNA-fragment field = background, illustrative · biocompatibility claim row = supporting
- sfx: none distinct (scanner-sweep/forcefield-hum cues from the original script have no matching asset in this repo; approximated with a soft whoosh under the card's arrival instead of a fresh sourced SFX)

narrativeRole: Establishes what PDRN literally is before any claim is made about it — nominal identity first, per this lane's identity-scene convention.
keyMessage: PDRN is a real, named, sourced material — and one specific safety claim about it has no record behind it.
On-screen text:
- Identity card (nominal fields only, no marker needed): "PDRN · Polydeoxyribonucleotide" / "INCI: Polydeoxyribonucleotide (Salmon)" / "Source: Salmon (Oncorhynchus keta) DNA fragments" / "Extraction: Purified"
- CLAIM row: "Highly biocompatible with humans — won't trigger an allergic immune response." → `○ UNSOURCED — no record in this system`

Shot sequence (Rule-of-thirds framing — card anchored lower-middle, generous negative space above; VO-paced):
Scene 1 (0.0–1.0s): background field of short DNA fragments (double-helix segments a few base-pairs long, matte flat-shaded, no rotation) drifts in slowly at low opacity behind where the card will land.
Scene 2 (1.0–2.6s): the identity card's hairline border draws on, centered in the lower-middle band, as VO says "It's called PDRN, or Polydeoxyribonucleotide."
Scene 3 (2.6–5.0s): the four nominal fields reveal in sequence (name → INCI → source → extraction), timed to "extracted and highly purified from salmon."
Scene 4 (5.0–8.2s): as VO reaches "highly biocompatible with humans—meaning they won't trigger an allergic immune response," the CLAIM row reveals beneath the identity card, and the `○ UNSOURCED` flag lands last, in the citation slot — no bracket, muted ink.
Scene 5 (8.2–10.0s): held read, DNA fragments continue their slow ambient drift (bounded, settles), into the cut.

## Frame 3 — The Medical History

- scene: Cell-multiplication field behind a FRAME/CLAIM/ROUTE/STUDY/Note/CITATION panel for the regenerative-medicine claim (mixed sourcing), closing with a compact "well-established" EvidenceMeter coda for `ING-pdrn-S001`.
- voiceover: "Because it is so safe and brilliant at triggering rapid cell growth, it wasn't originally for beauty. It was developed for hospitals as a regenerative medicine to heal severe burns, skin grafts, and diabetic ulcers."
- duration: 10s
- transition_in: crossfade
- status: animated
- src: compositions/frames/03-history.html
- type: feature_showcase
- persuasion: Evidence (partial citation) + transparency (explicit flag on the rest)
- beat: comprehension + credibility
- blueprint: claim-beat (FRAME → CLAIM → ROUTE → STUDY → Note → CITATION/UNSOURCED, ported structurally from red-ginseng's `03-route-oral.html`)
- focal: the claim panel's CITATION + UNSOURCED pairing
- roles: cell-multiplication field = background, illustrative · claim panel = foreground subject · EvidenceMeter coda = supporting, closing beat
- sfx: none distinct (heartbeat-monitor-beep has no matching asset; approximated with a soft click-in on the panel's arrival) → whoosh-short (into the coda)

narrativeRole: Grounds "regenerative medicine" in what's actually real (an injected-route trial on diabetic foot ulcers) while being explicit that "burns" and "skin grafts" aren't in this system's records — then closes on the one claim that's genuinely strong.
keyMessage: Real medical-use history exists for PDRN, but it's narrower and more specific than "burns, grafts, and ulcers" as a blanket claim.
On-screen text:
- FRAME (asserts nothing): "This was medicine before it was skincare."
- CLAIM: "So safe and effective at triggering rapid cell growth that it was developed for hospitals as a regenerative medicine — to heal severe burns, skin grafts, and diabetic ulcers."
- ROUTE: "Injected — clinical/hospital setting"
- STUDY: "Placebo-controlled, randomized human trial — diabetic foot ulcers"
- Note: "This route and population is not facial skin, and does not cover burns or skin grafts specifically."
- CITATION — ⌞ ING-pdrn-S003 ⌟ (scoped to the diabetic-ulcer portion) **directly above** `○ UNSOURCED — burns & grafts not in this system's records`
- Coda card (EvidenceMeter lockup): "Reduces visible transepidermal water loss" · 4 of 4 checkpoints lit · CITATION — ⌞ ING-pdrn-S001 ⌟ · label "KNOWN"

Shot sequence (Layered-depth framing; VO-paced):
Scene 1 (0.0–1.0s): cell-multiplication field (flat matte circles dividing/duplicating, celadon-tinted, no red/danger color) establishes behind the panel position.
Scene 2 (1.0–2.4s): panel's hairline border draws on; FRAME line reveals ("This was medicine before it was skincare") as VO says "Because it is so safe and brilliant at triggering rapid cell growth."
Scene 3 (2.4–4.4s): CLAIM row reveals as VO continues "...it wasn't originally for beauty. It was developed for hospitals as a regenerative medicine..."
Scene 4 (4.4–6.6s): ROUTE, then STUDY reveal in sequence as VO finishes "...to heal severe burns, skin grafts, and diabetic ulcers."
Scene 5 (6.6–7.6s): Note reveals; CITATION (⌞ ING-pdrn-S003 ⌟, coral bracket) lands directly above the `○ UNSOURCED` flag — this frame's one voltage moment.
Scene 6 (7.6–9.4s): panel recedes slightly (opacity down, not removed) as the compact EvidenceMeter coda blooms in beneath — four checkpoint nodes lock in celadon in sequence, `CITATION — ⌞ ING-pdrn-S001 ⌟` lands last.
Scene 7 (9.4–10.0s): held read into the crossfade.

## Frame 4 — How It Works (A2A Receptors)

- scene: [Round 3] Zoom into a flat cell-surface world, now a light hairline-bordered card (not
  the Round 2 dark glowing box): a receptor (stem + binding pocket) line-draws on, then a key
  travels down and turns with one precise, ungloved snap, opening a gate at the receptor's base —
  replacing Round 2's switch metaphor with a literal key-and-lock one, ported from a separate
  demo exploration but recolored into this project's own paper/ink/aqua tokens rather than the
  demo's own separate palette. Background still shifts warm to cool at the resolution moment.
- voiceover: "Here is how it works. Your cells have surface proteins called A2A receptors. Think of them as master control switches for tissue repair. When PDRN binds to them, it flips the switch—instantly shutting down inflammation and boosting blood flow."
- duration: 14s
- transition_in: crossfade
- status: animated
- src: compositions/frames/04-mechanism.html
- type: feature_showcase
- persuasion: Explanation (mechanism narrative) — explicitly not evidence, since none exists
- beat: comprehension
- blueprint: camera-journey, adapted (continues Frame 3's "just under the surface" world, arriving at one cell's surface)
- focal: the key turning and the gate opening in response
- roles: cell-surface field = foreground subject (fills 40–60% of frame) · key + receptor = supporting, explicitly illustrative · claim panel = supporting
- sfx: none distinct (microscopic-zoom has no matching asset) → click-soft (the turn moment)

narrativeRole: Explains the mechanism the script wants to tell, honestly bounded as an authored illustration rather than a cited fact, since no source anywhere in this system backs this specific claim.
keyMessage: This is how PDRN is described as working — not yet something this system can verify.
On-screen text:
- small subordinate tag, top of frame: "[Authored, illustrative — not a claim]"
- Kinetic label (general biology, no marker needed): "A2A receptors"
- CLAIM: "When PDRN binds to A2A receptors, it flips the switch — instantly shutting down inflammation and boosting blood flow." (script wording kept verbatim per the original claim-sourcing posture, even though the visual metaphor is now a key, not a switch)
- `○ UNSOURCED — no record in this system` (no CITATION anywhere in this frame — nothing here traces to a record)

Shot sequence (Layered-depth framing, continuous world with Frame 3; VO-paced) — [Round 3 revision, replacing Round 2's glowing switch with a key/receptor, in this project's own light-card tokens rather than the switch's dark glow]:
Scene 1 (0.0–1.8s): camera continues the push from Frame 3's cell field, arriving at one cell's surface (now a light, hairline-bordered card) as VO says "Here is how it works."
Scene 2 (1.8–3.2s): the receptor (stem + binding pocket) line-draws on; "A2A receptors" label and the `[Authored, illustrative — not a claim]` tag fade in; the gate reveals closed at the stem's base.
Scene 3 (4.6–8.8s): a key fades in and travels slowly, deliberately down toward the pocket — an explainer's pace, not a jump-scare's.
Scene 4 (8.8–9.4s): THE TURN — one precise `power3.out` snap, no overshoot, pivoting at the key's own tip exactly as a real key turns in a lock.
Scene 5 (9.2–9.9s): the gate opens in direct response; the pocket takes this frame's one aqua accent; background shifts warm→cool alongside it.
Scene 6 (14.6–16.4s): CLAIM row reveals at the base of frame as VO finishes "...instantly shutting down inflammation and boosting blood flow"; `○ UNSOURCED` flag lands directly beneath it.
Scene 7 (16.4–18.0s): held read into the crossfade.

## Frame 5 — Fibroblasts

- scene: [Round 2] A bouncy, dimensional "collagen matrix" — plump woven fiber bars that fly in
  from scattered positions and snap into place — replacing the flat factory line-drawing; closes
  on the flagged claim as before.
- voiceover: "This also wakes up your fibroblasts—the cellular factories responsible for creating brand new collagen, elastin, and hyaluronic acid from the inside out."
- duration: 10s
- transition_in: cut
- status: animated
- src: compositions/frames/05-fibroblast.html
- type: feature_showcase
- persuasion: Explanation, explicitly not evidence
- beat: momentum
- blueprint: compose (a single illustrative motif, one claim, one flag)
- focal: the collagen matrix snapping into place
- roles: collagen matrix = foreground subject, illustrative · three output glyphs (collagen/elastin/HA) = supporting · claim row = supporting
- sfx: none distinct (fast-mechanical-clicking has no matching asset) → sparkle (as the three glyphs land)

narrativeRole: Carries the video's second unsupported mechanism claim, keeping the same honest-flag treatment as Frame 4 rather than a different or softer marker.
keyMessage: This is the claimed downstream effect — also not yet backed by a record in this system.
On-screen text:
- small subordinate tag: "[Authored, illustrative — not a claim]"
- Kinetic label: "FIBROBLASTS"
- CLAIM: "Wakes up fibroblasts — the cellular factories that create new collagen, elastin, and hyaluronic acid."
- `○ UNSOURCED — no record in this system`

Shot sequence (Centered framing; VO-paced) — [Round 2 revision, replacing the factory + flying-particle mechanic]:
Scene 1 (0.2–1.55s): ten plump, glossy fiber bars fly in from scattered positions and snap into a woven lattice with a bouncy overshoot, settling with one residual jiggle — timed to VO's "wakes up your fibroblasts."
Scene 2 (1.6–4.0s): "FIBROBLASTS" kinetic label reveals above the matrix; the `[Authored, illustrative — not a claim]` tag fades in small, subordinate.
Scene 3 (4.0–7.4s): three small glyphs (collagen / elastin / hyaluronic acid, each a distinct simple flat icon) fade and rise in sequence beneath the matrix, timed to "creating brand new collagen, elastin, and hyaluronic acid."
Scene 4 (7.4–9.0s): CLAIM row reveals at the base of frame as VO finishes "...from the inside out"; `○ UNSOURCED` flag lands directly beneath.
Scene 5 (9.0–10.0s): held read into the hard cut.

## Frame 6 — Closing / CTA

- scene: [Round 2] SplitFaceProtocol's real periorbital diagram, restyled as a literal damaged
  (glowing red) vs. healed (glowing cyan) split screen — DAMAGED/HEALED labeled — with the
  sourcing chip and scope label kept intact, and a glowing neon CTA baked into the same dark panel.
- voiceover: "It essentially hacks your cells to repair damaged tissue at record speed. Would you try fish DNA for science? Let me know below!"
- duration: 8s
- transition_in: n/a (final frame)
- status: animated
- src: compositions/frames/06-cta.html
- type: social_proof
- persuasion: Distillation + direct engagement CTA
- beat: resolve + engagement
- blueprint: comparison-split, reused (SplitFaceProtocol's control-arm/active-arm, ported verbatim, recolored)
- focal: the damaged-red vs. healed-cyan split
- roles: SplitFaceProtocol diagram = foreground subject · "WORTH THE HYPE?" neon kinetic type = supporting, closing · citation = supporting
- sfx: pop, whoosh-short (swoosh out)

narrativeRole: Closes on the one visual in the video that's both real and already built in this system, rather than the script's generic invented "damaged grid" — then hands off to the CTA.
keyMessage: What's actually shown and sourced here is a periorbital (eye-area) topical trial — narrower than "record-speed tissue repair," and that's the honest note to end on before the CTA. The DAMAGED/HEALED relabeling makes the same real diagram punchier without claiming more than the N=32 periorbital trial covers.
On-screen text:
- Diagram label: "Periorbital · Topical · N=32" (kept, unchanged — the honest scope disclosure)
- Per-arm labels (new): "DAMAGED" / "HEALED"
- CITATION — ⌞ ING-pdrn-S004 ⌟ (real; kept exactly as before)
- Kinetic CTA (changed): "WORTH THE HYPE?" in glowing neon-cyan type (no marker — pure engagement prompt, not a claim)
- Recap line (unchanged, echoes Frames 4–5, already flagged there — no new marker needed): "hacks your cells... record speed" rendered small, italic EB Garamond, clearly subordinate to the CTA

Shot sequence (Split-screen framing; VO-paced) — [Round 2 revision, replacing the celadon fill + plain CTA text]:
Scene 1 (0.0–1.6s): SplitFaceProtocol's cranial bounds + bisector draw in (control-arm left, active-arm right) as VO says "It essentially hacks your cells to repair damaged tissue at record speed" — recap line unchanged.
Scene 2 (1.6–3.2s): both periorbital zones fade in as neutral wireframe (identical, pre-treatment) — the bilateral-symmetry beat, unchanged.
Scene 3 (3.2–4.6s): the split resolves — control floods angry glowing red ("DAMAGED"), active floods glowing cyan ("HEALED"), simultaneously; box border lights cyan; "Periorbital · Topical · N=32" label reveals.
Scene 4 (4.6–5.6s): `CITATION — ⌞ ING-pdrn-S004 ⌟` lands in coral, unchanged — still this frame's one real, sourced moment.
Scene 5 (5.6–7.2s): "WORTH THE HYPE?" lands in glowing neon-cyan kinetic type, per-word reveal, baked into the bottom of the same dark panel, timed to "Would you try fish DNA for science?"
Scene 6 (7.2–8.0s): held read, settled, on "Let me know below!" — a final ambient glow-breathe on both zones, then the calm hold is the close.
