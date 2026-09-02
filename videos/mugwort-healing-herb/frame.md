---
version: alpha
name: Mugwort Healing Herb — Frame
description: >
  Canonical SeoulHabit house tokens, paper-dominant register carried over from
  madecassoside-clinical-cut (no dark stage-box anywhere). Portrait only (1080×1920).
unit: the frame — 1080×1920, 9:16 only
principle: one aqua accent per frame · coral is the one voltage moment (beat 04's ✕) ·
  an UNSOURCED flag is never mistaken for a citation · captions from the authoritative
  script, ASR for timing only
colors:
  ink: "#131516"
  paper: "#F7F5F0"
  card: "#FBF9F5"
  aqua: "#59B8AE"
  aqua-text: "#3A7871"       # required whenever aqua colors readable text (3:1 large-text on paper)
  coral: "#C97A5C"
  coral-text: "#9F6149"
  ink-muted: "rgba(19,21,22,0.62)"   # WCAG floor for low-emphasis text — not self-enforcing, apply explicitly
  line: "rgba(19,21,22,0.12)"
typography:
  headline-kinetic: { fontFamily: "Inter", weight: 800, upper: true }
  name-serif: { fontFamily: "EB Garamond", note: "ingredient name + CTA question only" }
  fields-claims: { fontFamily: "Inter", weight: "500-700", note: "≥32px floor, ≥40px for body/claim text" }
---

# Mugwort Healing Herb — Frame

## Round 4 — pixel-verified re-cut (2026-08-31)

A full audit against the round-3 delivery master's actual rendered pixels (not the source,
not `npm run check`, not this doc's own prior claims) found four hard-gate failures that a
clean `check` (0 errors, 33/33 contrast checks) never surfaced: a 33px safe-area overshoot on
the right rail (beats 02/03/04's claim/choice panels were 822px centred at x=129, i.e.
x∈[129,951] — 951 > the 918 rail), ~31.5s of the 57.7s runtime frozen with no measurable pixel
change (worst: beat 04 static for 11.5 of its 12.664s), zero photographic or tactile imagery
anywhere despite two ready-made mugwort plates already sitting in this repo's own shared
catalog, and no `.srt`/thumbnail deliverable. See `videos/mugwort-healing-herb`'s delivery
report (this session) for the full measured breakdown; the fix touched every scene file plus
`index.html`'s audio layer. VO and every `data-start`/`data-duration` in `index.html` were
frozen throughout — nothing here changes the audio timing or re-triggers the re-timing
cascade; every fix below is scene-CSS/JS or the audio automation layer.

- **Safe areas — now actually the tokens, not just documented as them.** Every scene's `#root`
  declares `--safe-top:192px; --safe-bottom:384px; --safe-left:72px; --safe-right:162px;
  --safe-margin:6px` and every scene's content column is sized off them:
  `left:calc(var(--safe-left) + var(--safe-margin))`,
  `width:calc(1080px - var(--safe-left) - var(--safe-right) - var(--safe-margin) * 2)` — i.e.
  the real usable column is x∈[78,912], not the old flush-to-the-line x∈[72,918]. The
  `--safe-margin` guard band exists because content sized to sit *exactly* on the boundary
  line still fails a pixel-level scan: antialiasing, a 1px border, or a box-shadow's blur
  radius reliably bleeds a few px past an exact match (`catalog/tooling/check-safe-area.py`
  caught this directly — a 73px "violation" that was really the citation card's own border
  sitting flush on x=918). Captions top band stays y=240 (round 3's value, unchanged); content
  band moved from the old y∈[384,1440] to each scene's own `top:385-400px` — no single fixed
  content band any more, since beat 02's card and beat 03's diagram+card each needed a
  different top offset once their real rendered height was measured and trimmed to fit.
- **Vertical budget is now measured, not assumed.** Beat 02's card (photo header + kicker +
  name + 3 fields + claim) and beat 03's stack (caption + diagram field + citation card) both
  *looked* bounded by their own source CSS and both overshot the safe-bottom line by
  150-380px on the actual render — confirmed by extracting the frame at the reported
  worst-offense timestamp and visually inspecting it, not by re-deriving the arithmetic a
  second time. Fixed by shrinking (photo aspect 16/9→16/7 in beat 02, diagram field
  640px→480px in beats 03/05, tightened card padding/margins throughout) and re-measuring
  against the real render until `check-safe-area.py` reported clean. A source-level
  budget estimate is not evidence here; only the rendered frame is.
- **Photography, in three of six beats.** `assets/plates/18-mugwort.png` (the catalog's
  `18-mugwort.png`, a real photographed leaf sprig, 2048×2048) is the hero of beat 01 (replacing
  a hand-drawn SVG squiggle) and returns as the loop's landing pad in beat 06 (replacing a
  faint 0.14-opacity SVG ghost), plus a supporting header band in beat 02's clinical-file
  card. `assets/plates/A05-essence-refill.png` (from `catalog/product-photography`, an
  unbranded essence-bottle-and-refill-sachet plate already labeled "에센스 · 100mL") appears in
  beats 04 and 05 for product consistency across the two beats that are actually about the
  same first-layer step. Every plate: `loading="eager" decoding="sync"`, explicit
  `width`/`height` attrs at the source file's real pixel dimensions, an `object-fit:cover`
  container with a `#EFEAE1` fallback background, and its own continuous Ken Burns (never a
  motionless still) — the same fixed-outer-clip / scaled-inner-wrapper pattern used everywhere
  else in this file (see the safe-area note below).
- **A transform must never live on the same element as its own `overflow:hidden` clip
  boundary.** Every Ken Burns/camera-pull in every scene follows one pattern: a FIXED,
  unscaled outer container carries `overflow:hidden` and the safe-column sizing; a plain,
  unstyled inner `-zoom` wrapper (100%×100% of the outer) carries the actual `scale` tween.
  Getting this backwards — scaling the *same* box that also defines the safe clip boundary —
  is exactly the mechanism this file's own `9:16-native composition` safe-areas note warns
  about (a Ken Burns transform mapping a compliant padded edge outward by the scale factor).
  Caught mid-build here too: an early draft scaled `.mx-field` directly (bordered,
  `overflow:hidden`, 846px wide) at 1.04× centred scale, which would have bulged ~17px past
  *both* the left and right safe rails despite the box's own unscaled width being exactly
  correct. Fixed before it ever reached a render by introducing `.mx-field-zoom` (and the
  equivalent `-zoom` wrapper in every other scene) as the only thing GSAP ever touches.
- **Cadence — motion runs the scene's whole duration, not just its opening beats.** Beat 02's
  three fields now stagger across the take's full length instead of landing as one block at
  t=0; beat 02's photo, beat 03's diagram field, beat 05's diagram field and essence plate all
  carry a continuous slow zoom for their entire on-screen duration (previously capped partway
  through, leaving the back half of each scene motionless). Beat 04 needed two passes: scaling
  only the small essence-bottle plate (150×200px) measured as under 2% of the frame and didn't
  register as real cadence on a pixel diff; the actual fix scales `.pr-choice-inner` — the
  *whole* two-column panel's content, behind the same fixed-outer/scaled-inner safe pattern —
  which does. `scripts/check-static-hold.py` (copied in from `peeling-not-progress`, its
  caption-band constants re-derived for *this* project's own `.vo-caption` geometry — see that
  script's own docstring for why copying a sibling's constants verbatim is exactly how this
  class of bug happens) reports 0 findings against the delivery master at a 2.5s ceiling.
- **Accent discipline restored in beat 03.** The claim card's yellow `.uc-hl` highlighter
  (never in this file's color table) is retired; the frame's one accent stays aqua (the
  settle-dot), matching this doc's own stated principle above.
- **Type raised to this doc's own floor.** Every size below 32px (illustrative tags, kickers,
  labels — 11 of the 17 distinct sizes in the round-3 cut) is now ≥3.0cqw (32.4px at 1080
  canvas width); body/field/claim text is 4.0cqw (43.2px, clearing the 40px floor); hero name
  is 11cqw (~119px, within the 96-160px hero floor, up from 8.2cqw/88.5px); burned-in captions
  are 46px (up from 40px).
- Diagram fields hairline-bordered directly on paper; `[Authored, illustrative — not a
  claim]` tag bottom-left on every illustrative state (unchanged from round 3).
- Mugwort plate (beats 01/06): same photographic crop and Ken Burns treatment in both frames —
  the CTA fades it back in as the loop's landing pad, replacing the prior hand-authored SVG
  sprig ghost.
- Citations (beat 03 only): `.uc-cite` pills, Jung et al. 2018 · PMID 29353040 and
  Jung et al. 2017 · PMID 28899779, with explicit scope line "Mouse model · human skin
  cells in vitro — not a human clinical trial". Beats 04/05 carry
  `○ UNSOURCED — no record in this system` instead — the protocol and absorption
  framings are authored guidance. Unchanged from round 3.1's badge styling.
- Motion: `power3.out` settles on discrete beats; continuous camera-pull tweens use `power1.inOut`
  or, where a scene's tail measured as low-motion on `power1.inOut`'s own ease-out (beat 03),
  `ease:'none'` for a constant per-frame rate instead. No overshoot anywhere (nothing in this
  video snaps into a structure, so nothing earns back.out). Alarm-ray jitter in beat 03 decays
  via deterministic timeline onUpdate — never rAF.
- Frame zero = beat 01 fully composed (plate, name, underline, payoff badge, kicker, tag all
  opaque at t=0; only sub-pixel settles and the continuous Ken Burns move). Verified against
  the actual rendered frame 0, not inferred from the source — this render's capture log
  reported `captureMode:"beginframe"` even on this macOS host (contrary to this skill's
  documented Linux-only trigger for that mode), so frame 0 and every scene-boundary frame were
  pulled and inspected directly; none showed the documented stale-buffer/missing-entrance
  defect.
- **Payoff moved into the hook.** Beat 01 now carries a concrete preview badge ("One studied
  compound: Eupatilin") opaque from t=0, not just an ingredient name — the retention window no
  longer spends its whole budget on setup before beat 03's actual mechanism payoff at ~18s.
- **CTA carries the video's real lesson, not just the VO's engagement ask.** A new on-screen
  strapline ("Fermented essence · first layer · damp skin") sits in the closing card alongside
  the emoji-comment prompt the VO actually asks for — the closing beat stays lesson-tied
  without touching the frozen VO.
- Beat grid — **unchanged from round 2's tightened cut, still authoritative**: S1=0.000
  S2=9.861 S3=18.403 S4=30.074 S5=42.738 S6=51.272, total 57.671s. (The prior version of this
  doc still recorded the pre-round-2 grid — S1=0.000 S2=11.400 S3=21.700 S4=36.500 S5=51.600
  S6=63.600, total 73.900s — two rounds after it stopped matching `index.html`. Re-derive this
  line from `index.html` directly after any future timing change; don't hand-edit an estimate.)
