---
message: "Korean glass skin isn't 10 products — it's 5 habits: Cleanse, Hydrate, Treat, Seal, Protect."
audience: "Skincare-curious viewers overwhelmed by K-beauty's reputation for long routines"
mode: autonomous
format: 1080x1920
duration: 41.526s (measured, see below)
---

Six frames, fixed script (user-supplied, one line corrected for accuracy —
see `frame.md` § Content corrections), fully faceless — macro plate is the
presenter, not typography (a deliberate departure from this channel's usual
typographic-first house style; see `frame.md` § Faceless). All six scenes
hard-cut (no crossfades) — palette alternates paper/ink frame to frame, and
`faceless-video-craft` flags crossfading across a ground change as producing
a muddy near-blank transition midpoint (kbeauty-one-percent-line's own
review round 1 hit exactly this bug; see that project's `index.html`
comment). **Timing below is FINAL, re-derived from measured
`assets/voice/*.wav` durations** (assets/MANIFEST.md § Voice) after
generation — not the pre-generation word-count estimates this section
originally held. Total runtime 41.526s: 39.026s of VO plus five 0.3s
inter-scene holds and a 1.0s loop-hold tail on Frame 6. Design source:
`frame.md`.

## Frame 1 — hook

- status: animated
- src: compositions/frames/01-hook.html
- type: hook
- start: 0.000
- duration (scene clip): 7.285s (VO 6.485s + 0.3s hold, +0.5s tail overlap into Frame 2)
- ground: paper
- beat: Top-down cluttered counter plate (generated), 10+ bottles filling
  frame. Two hands enter and firmly slide most of them out of frame — hard
  cut to the same counter swept clear (generated, second plate) at the VO's
  "barrier" beat, landing the payoff inside the 2s retention window. The one
  coral voltage moment: an ink strikethrough slams across a ghost "10-STEP"
  kicker as the sweep lands. VO (corrected): "Stop doing a 10-step skincare
  routine. Stacking that many actives is how barriers get wrecked." SFX:
  hook-hit, buzzer (crossed out), soft glass-clink as bottles slide.

## Frame 2 — promise

- status: animated
- src: compositions/frames/02-promise.html
- type: branding
- start: 6.785
- duration (scene clip): 6.191s (VO 5.391s + 0.3s hold, +0.5s tail overlap into Frame 3)
- ground: ink
- beat: Reused plate `C02-01.png` (hand dispensing serum, cropped at wrist)
  full-bleed, slow Ken-Burns push. "5" numeral snaps in aqua, oversized,
  center-left — first appearance of the habit-count motif the CTA frame
  closes on. VO: "Korean glass skin doesn't come from hoarding products. It
  comes from these 5 simple habits." SFX: soft whoosh, chime.

## Frame 3 — habits 1 & 2 (Cleanse / Hydrate)

- status: animated
- src: compositions/frames/03-cleanse-hydrate.html
- type: concept
- start: 12.476
- duration (scene clip): 7.800s (VO 7.000s + 0.3s hold, +0.5s tail overlap into Frame 4)
- ground: paper
- beat: Two-beat split within one scene, hard cut at the VO's "Two:" — left
  beat: reused plate `B03-01.png` (balm block melting into a celadon-tinted
  puddle) for Cleanse; right beat: generated toner-pour-into-cupped-palm
  plate for Hydrate. Habit-word stack (RoutineLadder mechanism, re-skinned —
  see `frame.md` § Component reuse) advances CLEANSE → HYDRATE center-left,
  synced to the cut. VO: "One: Cleanse. Melt the SPF off. Two: Hydrate.
  Press toner into damp skin." SFX: jar-unscrew, water-pour/splash.

## Frame 4 — habits 3 & 4 (Treat / Seal)

- status: animated
- src: compositions/frames/04-treat-seal.html
- type: concept
- start: 19.776
- duration (scene clip): 9.400s (VO 8.600s + 0.3s hold, +0.5s tail overlap into Frame 5)
- ground: ink
- beat: Two-beat split, hard cut at "Four:" — left beat: reused plate
  `B01-01.png` (single suspended droplet over a glass dish) for Treat,
  chosen deliberately because the single drop visually carries "just *one*
  active serum"; right beat: reused plate `B02-01.png` (thick cream swirl)
  for Seal. Habit stack advances TREAT → SEAL. VO: "Three: Treat. Pick just
  one active serum. Four: Seal. Lock it all in with a barrier cream." SFX:
  droplet-tick, cream-swoosh.

## Frame 5 — habit 5 (Protect)

- status: animated
- src: compositions/frames/05-protect.html
- type: concept
- start: 28.676
- duration (scene clip): 5.850s (VO 5.050s + 0.3s hold, +0.5s tail overlap into Frame 6)
- ground: paper
- beat: Generated plate — two fingers, two thick SPF lines squeezed down
  their length, close macro crop. Habit stack advances to PROTECT, all five
  words now visible in the completed stack (the scene's one deliberately
  denser beat — five words on screen at once, matching the "keep text on
  screen at all times" rule at its peak). VO: "And Five: Protect. Two
  fingers of SPF 50, every single morning." SFX: pump-click, soft-squeeze.

## Frame 6 — CTA / endcard

- status: animated
- src: compositions/frames/06-cta-endcard.html
- type: cta
- start: 34.026
- duration (scene clip): 7.500s (VO re-recorded 2026-08-30, real word end 6.04s
  + a 0.59s engineered tail/fade to 6.630s, + remaining loop-hold to the
  frame's own end — see QC fix pass below; unchanged from the original 7.500s
  since the fix didn't need to extend the frame, only fill it)
- ground: paper
- beat: Reused plate `C01-01.png` (six-product shelf), cropped to 5 of 6
  products, placed as a full-width horizontal band — the video's one
  structurally different layout (per faceless-video-craft's layout-variety
  rule) and the frame that makes "just 5 products" literally true. Full
  habit stack holds beneath it, with a landing pop staggered across all five
  rows on "Five habits." A finger-tap micro-interaction lands on the real
  "subscribe" word. 습 SeoulHabit lockup arrives on "because." A "NEXT:
  BARRIER REPAIR" chip — the frame's one aqua accent, and the burned-in form
  of the VO's own closing promise — lands on "damaged" and clears before the
  loop-hold settle. Continuous Ken Burns runs the product band across the
  scene's *entire* duration (previously stopped at 1.2s, leaving ~5s frozen
  past it — see QC fix pass below). Final held frame (product band + clear
  counter, same paper ground as Frame 1's payoff) is the deliberate loop
  target back to Frame 1's cold open. VO: "That's it. 5 habits. Hit
  subscribe because tomorrow we're fixing your damaged skin barrier." SFX:
  chime-triple.

### 2026-08-30 QC fix pass (post-ship)

A 6-item QC review flagged: captions inside the Shorts UI overlay zone
(blocker), an abrupt VO cutoff, ~5s of frozen imagery in this frame, two
under-boxed chips (Frames 4/5) misread as low-contrast/too-small, and a
six-fingered hand in the Frame 1 hook plate. All six confirmed real against
the actual render; two (the Frame 4/5 chips) turned out to share one root
cause — a CSS `inset:0` box bug, not a colour/size defect — and the Frame 6
freeze was measured precisely (5.0s, local ~2.06-7.5s) rather than assumed.
Fixes: caption band moved −400px (960-1110px, mid-frame) with every scene's
own content reflowed to clear it; the two chips got real shrink-to-fit boxes
(the colour/size asks were applied on top, not instead of); this frame
gained five new beats filling the freeze plus continuous Ken Burns; VO line
06 was re-recorded with real trailing room and a genuine 10-frame fade
(the original take had no trailing silence at all — the "fade" had nothing
to fade); the hook plate was regenerated. See `frame.md` § Verification for
the fixed render's measurements, and `scripts/check-static-hold.py` (new)
for the checker that would have caught the freeze the first time.
