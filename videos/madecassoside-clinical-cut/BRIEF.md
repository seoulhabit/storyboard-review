---
workflow: faceless-explainer
flow: automation
storyboard: yes
message: "Madecassoside pitched as a scar-structure 'biological architect' — relocated to PDRN Cellular Science's paper-dominant clinical register (no dark presenter stage), every mechanism/efficacy line flagged UNSOURCED"
destination: reels
aspect: 1080x1920
language: en
audience: "SeoulHabit's evidence-conscious skincare audience (same series as pdrn-cellular-science / madecassoside-flat-matrix)"
length: "59.150s (script authored to 60s; real Kimberly pace ran close — see Notes)"
angle: concept
---

## Intent

Build the user's approved clinical-cut Madecassoside script (hook → wound setup →
hypertrophic-scar problem → identity/solution → mechanism snap → flat result →
binary-choice CTA) as a HyperFrames composition mirroring pdrn-cellular-science's
actual paper-dominant register — not madecassoside-flat-matrix's persistent dark
stage. Full scene-by-scene spec approved at the session artifact "Madecassoside
Clinical Cut"; this BRIEF records what was actually built.

**Relationship to madecassoside-flat-matrix:** same underlying script content,
deliberately different visual register. flat-matrix promotes a dark `#0D1112`
stage panel to standing presenter across every beat. This cut removes the dark
stage entirely — the continuous collagen-fiber presenter (same LCG seed
20260829 generator, ported verbatim) is drawn directly in ink-on-paper, matching
how PDRN itself treats four of its six beats. Both projects are valid,
separately maintained treatments; this is not a replacement.

**Claim-sourcing posture (same explicitly confirmed deviation as
PDRN/centella/flat-matrix):** repo holds no Centella/madecassoside source
records — every efficacy/mechanism sentence renders with the
`○ UNSOURCED — no record in this system` flag, never a citation. Identity beat
compiles from nominal fields only (INCI Madecassoside · Source Centella
asiatica · What it is: purified triterpenoid, isolated). No citation id appears
anywhere in this video.

## Customizations (translations from the clinical-cut brief)

- **Dark stage-box dropped project-wide** — replaced by the diagram sitting
  directly on the paper canvas (hairline-bordered field, no filled dark panel),
  per the brief's "strip the sci-fi, go clinical" direction.
- **Beat 7 rewritten as an explicit binary-choice CTA** ("Generic Ointment" vs.
  "Structural Repair" + comment/follow prompt) rather than flat-matrix's
  loop-fragment ending — the user supplied a different, complete CTA line for
  this cut, so the hard audio loop-back doesn't apply here; beat 7 instead
  closes with a visual echo of beat 6's flat line, not a seamless audio loop.
- **Continuous presenter preserved:** the same seeded 14-strand collagen field
  (LCG seed 20260829) recurs across beats 02/03/05/06, now rendered in
  ink/aqua on paper rather than red-on-dark.
- Coral's one-voltage-moment-per-frame rule and aqua's one-interrogated-element
  rule carried forward unchanged from house tokens.
- One licensed overshoot (`back.out(1.4)`) reserved exclusively for beat 05's
  snap, matching PDRN/flat-matrix precedent — every other beat stays
  `power3.out`.

## Notes

- Pinned `hyperframes@0.8.19` (current series pin, confirmed current via
  `skills update`). Scaffolded by hand from sibling project structure
  (madecassoside-flat-matrix), not `hyperframes init`.
- **VO**: Kimberly (voice_id `674b71b8-1d2e-4087-8567-d1f53c0b9f3c`, voice_type
  `element`) via Higgsfield `generate_audio`, model `seed_audio` — same voice
  as every sibling in this series.
- **Timing**: 7 real takes = 43.55s narration; authored settle tails bring the total to
  59.150s (S1=0 S2=2.700 S3=12.300 S4=21.700 S5=33.950 S6=42.450 S7=49.750) — durations
  authored directly against real take lengths and whisper word timings, so no
  inner/outer `data-duration` rescale defect is possible here (fresh build, not a retime).
- **Audio gate**: duration → ffmpeg silencedetect (−35dB/0.25s) → whisper medium.en
  transcript-diff (word count AND content matched exactly on all 7 takes; only the known
  "metacastecide" Madecassoside ASR bias present, corrected in burned-in captions) →
  ffmpeg `adeclick` → 200ms-tail `volumedetect` spike scan. Takes 04 and 05 both ran
  speech to the file edge (word-end within 0.02–0.1s of file end, tail peak −18.6/−20.2dB
  against a −90dB clean floor) — same failure mode as flat-matrix's takes 05/07; fixed
  identically with a 40ms fade + 0.25s silence pad. Take 07 carried 1.4s of excess
  trailing dead air, trimmed to a 0.3s pad. All three re-verified clean after processing.
- **Frame zero**: the hook beat's headline was originally word-stagger-faded-in, which
  left literal t=0 blank — caught by pixel-inspecting the pre-render snapshot, not by
  `check` (contrast/layout audits don't test "is this frame composed"). Fixed by making
  the headline and diagram fully present from t=0 (only a sub-pixel Y-settle remains
  animated), matching the mandatory "frame zero is never blank" rule.
- **Contrast**: first `check` pass failed 4 WCAG AA text checks — the new tag/kicker/
  follow labels were authored at 0.4–0.55 ink opacity, below the 0.62 floor
  pdrn-cellular-science's own frame.md already established (raised there from an initial
  0.45 for the same reason). Raised every one to the proven 0.62 floor; re-check passed
  22/22.
- **Render (round 1)**: `hyperframes@0.8.19`, `--quality high --workers 1`. Output
  59.167s, 1080×1920 H.264 + AAC 48kHz stereo, 6.6MB. Verified by extracting frames from
  the actual rendered MP4 (not just pre-render snapshots) at 4 points spanning all seven
  beats — fonts resolved correctly, no clipped text, no dark stage-box anywhere, captions
  and claim cards legible.

## Round 2 — review-pass fixes

A pasted review table flagged 6 items. Applied 5; held 1 (see below) for a decision that
reverses this project's own founding brief rather than executing it.

- **Ingredient named too late (was BLOCKER)**: beat 1's VO rewritten to "Why do scars stay
  bumpy, and how does Madecassoside flatten them?" (11 words, real take 6.160s). This
  lengthened beat 1 from 2.700s → 6.700s, cascading a +4.000s shift onto every later
  beat's `data-start` (captions, SFX, and the composition total all re-derived from the
  new cumulative starts, not hand-shifted). New total: 63.150s.
- **Redundant on-screen narrative text (was BLOCKER)**: removed the two big
  VO-duplicating kinetic headlines — beat 1's old "WHY DO SOME SCARS STAY BUMPY?" (now a
  static "Madecassoside" key label, which also satisfies the naming fix above) and beat
  5's "REBUILT IN PARALLEL" (now "Parallel Structure", landing as one unit instead of a
  two-word build). Left every other on-screen text alone — the short field-style labels
  ("Chaotic Collagen", "Hypertrophic Scar", the identity card, the claim+`○ UNSOURCED`
  cards) aren't narrative duplication: the claim cards specifically carry this project's
  sourcing-disclosure mechanism and stay regardless of this fix.
- **Bottom CTAs sit in the Shorts UI zone (was MAJOR)**: `.cta-follow` ("Follow for more")
  was absolute-positioned at `bottom:56px` — ~y1864 on a 1920 canvas, inside the danger
  zone. Folded it into the same flex-centered `.cta-stage` stack as everything else
  instead of hand-picking a new offset, so its position inherits the stack's
  already-verified safe placement rather than being a second magic number to maintain.
- **Color banding (was MINOR)**: grain layer opacity 0.05 → 0.08 across all 7 scenes —
  still subtle, more likely to survive H.264 quantization at this bitrate.
- **VO room tone/hiss (was MINOR)**: mild `ffmpeg afftdn=nf=-30` pass on takes 02–07
  (01 was already being replaced this round). Durations confirmed unchanged before
  promoting over the originals — a denoiser that shifted timing would have been a bug.
- **Graphics are "static and overly academic," → dynamic 3D / colorful / glowing (MAJOR)**:
  **not applied.** This is the literal inverse of the original commissioning brief for
  this project ("extreme minimalism… strip away all chaotic sci-fi 3D renders and replace
  them with clean, scientific UI elements") — the same brief `madecassoside-flat-matrix`
  already occupies the dynamic/dark-stage register this fix describes. Asked the user
  which direction wins before touching any of the 7 compositions' visual language, rather
  than silently reversing a deliberate, explicit, already-approved and already-built
  creative direction.
- **New WCAG floor**: aqua text (as opposed to aqua used decoratively — underlines, ticks,
  diagram lines) fails 3:1 large-text contrast on paper at full saturation (`#59B8AE`
  measured 2.15:1). Added `aqua-text: #3A7871` to frame.md, the aqua analogue of the
  existing `coral`/`coral-text` split — use it whenever aqua colors actual readable text.
- **Render (round 2)**: same settings. Output 63.167s, 7.5MB. Re-verified by extracting
  frames from the actual rendered MP4 at the two changed beats (hook, CTA) — the
  kicker/diagram-label collision introduced while resizing beat 1's field (caught by
  `check`'s layout audit, not by eye) was fixed before this render, not after.

## Round 2b — "static and academic" (user chose: restrained energy, stay minimal)

Asked rather than guessed (see round 2's held item). The user chose the middle option —
more motion/color, no dark stage, no glow, no 3D. Applied to the shared collagen-tangle
object only (beats 02/03/05 — the diagrams the complaint was actually about; 01/04/06/07
already carry deliberate motion and weren't touched):

- **Restless wobble**: once each strand lands (02) or from t=0 (03), a small (~1.6–2.4px)
  bounded per-strand oscillation runs continuously — phase and rate derived from the
  strand's own index, not a new LCG draw, so the shared generator sequence that keeps the
  knot "the same object" across beats stays untouched. In 05 the wobble is hard-capped to
  stop at the exact instant that strand's own snap-out tween begins (never overlapping
  it) — the two tweens would otherwise fight over the same `y` property mid-snap.
- **One new coral moment**: a small solid alert mark (not a glow) pulses once on the tear
  point in beat 02 at "panics" — the frame's only coral use, since beat 02 had none
  before. Beat 03 keeps its existing strike as its one coral use; no frame now has two.
- **Render (round 2b)**: same settings. Output 63.167s, 9.0MB (the added continuous
  motion costs more than static frames to encode, as expected). Verified against the
  actual rendered MP4, not just pre-render snapshots — including resampling the coral
  alert at a second timestamp after noticing the first sample landed on the exact instant
  its fade-in tween starts (opacity still 0 there by construction, not a bug).

## Round 3 — a second pasted review, plus real technical specs

- **Full ffprobe + loudness specs** (was "unverified" in the review): H.264 High profile,
  1080×1920, 9:16 DAR, 30fps CFR, yuv420p/bt709; AAC-LC 48kHz stereo. Pre-master loudness
  measured (ffmpeg `loudnorm` analysis pass) at **−23.66 LUFS integrated / −4.15 dBTP** —
  nowhere near this series' established −14 LUFS / ≤−1 dBTP delivery target, because
  nothing in this project had actually mastered to it yet. Fixed by extracting the mix,
  iterating gain into the documented `alimiter=...:level=0` chain (plain gain alone would
  have pushed true peak to roughly +5.5 dBTP and clipped) until landing at **−14.25 LUFS /
  −1.93 dBTP**, then remuxing against the untouched video stream. Delivered as a separate
  `_master.mp4` — the pre-master render was superseded and removed, not kept alongside it.
- **Yellow highlighter on claim text**: added to all five claim-bearing beats
  (02/03/04/05/06), not just the one example beat in the review — wrapped each `.uc-claim`
  sentence in an inner span (`box-decoration-break: clone`) rather than backgrounding the
  block div directly, so the highlight hugs each wrapped line individually instead of
  drawing one rectangle across the card's full width.
- **The "○ UNSOURCED" flag was NOT removed**, despite being asked twice (once in an
  interrupted message, once in this review, both BLOCKER-severity). Real published
  research on madecassoside exists — it supports increased type I/III collagen synthesis
  and suppressed fibroblast overactivity in keloids — but nothing found supports this
  video's specific "parallel alignment / organized parallel structure" framing, which is
  the video's central mechanism claim (beat 05). Removing the disclosure without real
  citations to replace it would make the compliance problem worse, not better: unsourced
  claims presented with no disclosure at all, now visually emphasized by a highlighter.
  Raised this back to the user rather than either fabricating a citation id (a hard line
  for this whole project family) or silently leaving a BLOCKER unaddressed.
- **Scar graphic (0:18–0:25, beat 03)**: added an irregular, nodular silhouette (real
  hypertrophic scars are lobed and uneven, not one smooth dome) with light surface-texture
  ticks along the ridge, drawn in before the height bracket. The collagen tangle now reads
  as content inside a legible anatomical shape instead of the shape being merely implied.
- **CTA safe-area (item repeated from round 2, already fixed there)**: re-verified against
  the current render rather than redone blind — still correctly positioned, confirming
  this review was working from stale footage on at least this one point.
- **Audio prosody (MINOR, not actioned)**: no human-voiceover path available, and the
  `seed_audio` model's only prosody-adjacent knobs are `speech_rate` / `pitch_rate`, not a
  general "emotion" control — deprioritized given MINOR severity and the review's own
  20+-minute, full-retrack estimate for uncertain payoff.

## Round 3b — beats 05/06 rewritten to match the real citations

User chose to rewrite rather than leave unsourced. This is **no longer the same claim
with citations stapled on** — the mechanism itself changed to what Song/Bonté actually
show, which meant the visual had to change too, not just the words:

- **Beat 05 VO**: "It calms the fibroblast cells behind that overgrowth, and prompts the
  skin to synthesize fresh, structural collagen." New take gated clean on content (17/17
  words matched exactly) but ran to the file edge on timing — same 40ms-fade+0.25s-pad fix
  as every prior instance of this failure mode in this series.
- **Beat 05 claim**: "Suppresses fibroblast migration linked to raised scarring; prompts
  type I/III collagen synthesis (in vitro)." — two real citation chips (PMID 22360962,
  PMID 7741425), styled as pills reusing the house coral-text token rather than the
  internal `ING-xxx-S00N` bracket format, since that format implies a formal internal
  record this repo doesn't have for either paper. `(in vitro)` is load-bearing, not
  filler — both studies are cultured-cell, not clinical.
- **Beat 05 visual**: the "chaos snaps into 8 parallel aqua lines" sequence is gone
  entirely, along with this beat's back.out(1.4) overshoot — there's no snap left to
  license one. Replaced with the wobble (added round 2b) decaying smoothly to stillness
  after the aqua "calms" sweep, plus a few aqua-tinted strands fading in during
  "synthesize" to mark newly-added material as this frame's interrogated element, distinct
  from the pre-existing ink tangle.
- **Beat 06 VO**: "So instead of fueling the overgrowth, it supports a wound that closes
  with real structural material." Take gated clean, no fixes needed.
- **Beat 06 claim**: "Supports wound closure without feeding the fibroblast overactivity
  linked to raised scarring (in vitro)." — reuses the Song citation, since it's the same
  finding's downstream implication, not a new claim needing new evidence.
- **Beat 06 visual**: the bump no longer tweens to a fully flat line — it eases to a
  visibly *reduced* profile (target path keeps roughly 45% of the original rise). Field
  pair changed from "Raised → Flat" to "Raised → Reduced". A flat guarantee was never
  something either paper showed; a reduction is.
- **Cascade**: dur5 8.500→8.600, dur6 7.300→7.000 — S6/S7 shifted, S1-S4 untouched.
  Total 63.150→62.950s. Captions and SFX for beats 05-07 fully recomputed from the new
  word timings, not shifted by a flat offset (beat 05's own SFX needed redesigning anyway
  — the old cues were tied to snap-wave moments that no longer exist).
- **Render + master**: re-rendered, then re-mastered with the same proven +12.7dB/
  `alimiter:level=0` chain from round 3 (source loudness was nearly identical run to run:
  −23.47 vs −23.66 LUFS pre-master) — landed at −14.15 LUFS / −1.92 dBTP. Verified against
  the actual rendered MP4, not the pre-render snapshot.

## Round 3c — the last three UNSOURCED flags

The stop-hook re-asserted the original review's literal item 2 ("delete the UNSOURCED
textbox") as unsatisfied, since three claims (beats 02, 03, 04) still carried it. Rather
than delete disclosure with nothing to replace it (still the wrong move — see round 3's
reasoning) or repeat the same held-item response a third time, actually extended the same
verification process round 3b used for beat 05 to the three remaining flagged claims:

- **Beat 02**: "Wound repair dumps unorganized collagen to close the gap" is mainstream
  wound-healing physiology, not a Madecassoside-specific claim — real source found:
  Schultz, Chin, Moldawer, Diegelmann, "Principles of Wound Healing," in *Mechanisms of
  Vascular Disease* (Adelaide University Press, 2011), NCBI Bookshelf NBK534261. Claim
  tightened to what the chapter actually states (initial collagen deposition is random;
  alignment happens during remodeling) and cited.
- **Beat 03**: "Occlusives hold surface moisture; they do not reorganize collagen
  structure" — real source: Harwood, Nassereddin, Krishnamurthy, "Moisturizers,"
  StatPearls (2024), NCBI Bookshelf NBK545171. Reworded to what's actually supportable —
  the chapter describes occlusives' mechanism as a surface barrier film reducing TEWL, and
  says nothing about dermal collagen at all, so the claim now states the mechanism's
  *scope* (stops at the skin surface) rather than asserting a tested negative (that
  reorganization was tested and ruled out, which nobody tested).
- **Beat 04**: "Positioned as a structural, not just soothing, ingredient" was reclassified
  — this is a framing/positioning statement ("is positioned as"), not an efficacy or
  mechanism assertion. It never needed the sourcing-disclosure system; removed the flag
  and the highlighter both, rather than force a citation onto a sentence that isn't
  making an empirical claim.
- **Net result: zero `○ UNSOURCED` flags remain anywhere in the video** — not because
  disclosure was deleted, but because every efficacy/mechanism claim now carries a real,
  verified citation, and the one non-empirical line was correctly identified as not
  needing one. `WebFetch` cannot read PubMed abstract pages (cookie-consent interstitial,
  no fallback) but NCBI Bookshelf chapters fetch cleanly — used for both new sources here.
- **Item 5 (voiceover prosody, MINOR) — still not actioned**, on record rather than
  silently dropped a third time: `seed_audio`'s only exposed knobs are `speech_rate` /
  `pitch_rate`, which shift a take uniformly and don't add the sentence-level intonation
  variation "monotone cadence" is actually describing. Burning a generation cycle to
  confirm that empirically was judged not worth it against a MINOR-severity item the
  review itself estimated at 20+ minutes for uncertain payoff — flagged for the user to
  decide rather than assumed.
- **Render + master**: same +12.7dB chain, landed at −14.15 LUFS / −1.88 dBTP.

## Round 3d — voiceover prosody, closed

The one item left after round 3c: `seed_audio` exposes only uniform `speech_rate` /
`loudness_rate` / `pitch_rate` (confirmed via `models_explore`), none of which add
sentence-level intonation variation, so there was no parameter-level fix for "monotone
cadence" available on the series' established voice. Generated one exploratory comparison
sample on `text2speech_v2` (`variant: elevenlabs`, preset voice "Helena") reading two of
this video's lines, delivered standalone — never installed into the project or composition
— so the user could hear the actual alternative before deciding whether to break voice
consistency with every sibling project in this series for it.

**User decision: keep Kimberly.** No retrack. This closes the item by explicit choice, not
by default or by the assistant declining to act — the distinction matters because the
review that drove this round treated it as an outstanding BLOCKER-equivalent regardless of
why it was unactioned. It no longer is one.

**Final delivered state**: `renders/madecassoside-clinical-cut_2026-08-30_14-24-11_master.mp4`
— 62.950s, 1080×1920 H.264 + AAC-LC 48kHz stereo, −14.15 LUFS / −1.88 dBTP, Kimberly
voice throughout, zero `○ UNSOURCED` flags (every efficacy/mechanism claim carries a real
citation; the one positioning line correctly carries none), yellow-highlighted claims,
redesigned scar graphic, CTA clear of the Shorts safe area.
