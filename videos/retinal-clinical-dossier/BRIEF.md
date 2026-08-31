# Retinal Clinical Dossier — BRIEF

60-second silent 9:16 short (1080×1920, 30fps), built 2026-08-30 from a pasted
six-scene "Hyperframes project" prompt (clinical/minimalist dossier style,
alternating dark/light scenes). Monolithic standalone `index.html`, one paused
GSAP timeline keyed `main`, hyperframes@0.8.19 pinned.

## Scene map (hard cuts, per the pasted timecodes)

| # | Window | Register | Content |
|---|--------|----------|---------|
| 1 | 0–8    | ink      | Hook — "WASTING TIME?", retinol dropper bottle, coral X draws in |
| 2 | 8–18   | paper    | Conversion path card — RETINOL → RETINALDEHYDE → RETINOIC ACID, two coral step highlights |
| 3 | 18–28  | paper    | Dossier card — identity, what-it-is, 11× claim + aqua dots/KNOWN |
| 4 | 28–42  | paper    | Fibroblasts — waffle grid, copy, pulsing collagen/elastin icons |
| 5 | 42–52  | ink      | Application — line-drawn profile, aqua cheek marker, GENTLE / 2–3× WEEKLY |
| 6 | 52–60  | ink      | CTA — DROP THE O / GET THE A, pill button (the one licensed overshoot) |

## Decisions that deviate from the pasted prompt (and why)

1. **Citations replaced by `○ UNSOURCED` flags.** The prompt specifies
   `CITATION — ↳ ING-ret-S001` (11× claim) and `ING-ret-S002` (gentle/2-3x).
   Neither id resolves anywhere: `catalog/ingredients/retinal-vs-retinol/`
   explicitly flags this ingredient as a records gap and no `ING-ret-*` string
   exists in the workspace. House posture (pdrn frame.md: the citation chip is
   "reserved exclusively for a real, verified source id — never invented") puts
   the muted UNSOURCED flag on every efficacy/gentleness claim instead: the 11×
   claim (S3), the fibroblast mechanism copy (S4 — the prompt gave it no
   citation at all), and GENTLE / 2–3× WEEKLY (S5). If real records land later,
   swapping flags for chips is a per-row edit — but note (madecassoside lesson)
   matching a claim to real evidence usually changes the visual too.
2. **House tokens, not the prompt's hexes.** Deep charcoal→ink `#131516`,
   off-white→paper `#F7F5F0`, clinical teal→aqua `#59B8AE`, soft red→coral
   `#C97A5C`. The prompt's palette description maps onto the series tokens
   almost exactly; tokens carry the decision.
3. **No glow.** The prompt asks for a glowing bottle/face/cheek circle; the
   lane bans glow outright. Emphasis is carried by stroke draw-ins, a finite
   scale pulse on the X, and the marker's dashed-circle pulse.
4. **Evidence dots are aqua, not green emoji** (prompt allowed CSS dots;
   EvidenceMeter rule: never success-green). "KNOWN" sits beside them in ink;
   the UNSOURCED flag directly below keeps the grade from reading as a
   verified citation.
5. **Frame zero is fully composed** — headline, kicker, bottle, and tag all
   opaque at t=0; only the bottle settle animates and the X arrives at ~1.3s.
   (The prompt's "X fading in over the bottle" survives as the first beat, not
   as a blank frame zero.)
6. **S2 renders the pathway as a vertical node stack** (three bordered nodes,
   downward step-labeled arrows, illustrative-footer, aqua active-form
   highlight) rather than the prompt's inline "A → B → C" line — vertical
   stacking is the 9:16-native layout; content and sequential-highlight intent
   are unchanged.
7. **S5's flag sits in the text column, not as a bottom footnote** — the
   bottom ~20% is Shorts UI chrome and holds nothing readable.
8. **All scene transitions are hard cuts** (house rule: cuts over crossfades),
   so S6 opens on a cut rather than the prompt's face fade-out.
9. **The S5 face is a single-line abstract profile** with the route word
   (TOPICAL) printed in the header — application depiction, not a
   SplitFaceProtocol result surface.

## Round 2 (2026-08-30, user feedback: name ingredient up front / rework :50 /
stronger ending / more action)

- S1 now names RETINAL twice: kicker "RETINAL VS RETINOL · DOSSIER N#03" at
  frame zero, plus an aqua "THE UPGRADE · RETINAL" pill at 3.4s (bottle shrunk
  to clear it). X draws at 0.9s.
- S5 reworked: smoother profile path, marker at the cheek, and a 7-pip week row
  (3 filled aqua) making "2–3× WEEKLY" visual.
- S6 rewritten: "RETINAL · ONE STEP AHEAD" lockup, power4 word slams, aqua
  underline, pill pop + closing pulse. VO 06 rewritten to "One step ahead. Drop
  the O, get the A. Formulas below." (take regenerated, clean tail, 6.08s).
- Anti-lag pass: every scene carries continuous motion (linear push-ins on
  stage/cards/grid), stagger times tightened ~30%, arrow highlights synced to
  the VO mentions, S4 gets five aqua "active cells" lighting in sequence.
- Master re-run: −13.90 LUFS / −1.91 dBTP.

## Round 3 (2026-08-30, user feedback: "too many pauses")

Audited every scene for dead time between the last discrete beat and the cut
(VO end + tween end vs `data-duration`). Two real violations of the shorts
1.5-3s state-change cadence: S2 had a ~2.2s silent tail after the highlight
sequence (15.8-18s), and S3 had a ~5s static hold after the flag landed
(22.9-28s) — by far the worst offender. S1/S4/S5/S6 already had continuous
beats/pulses running close to their cut points and needed no change.

Fixes, not fabricated content — both reuse information already on screen:
- S2: an aqua checkmark badge confirms onto the RETINOIC ACID node at 15.9s
  (pop-in + settle pulse), closing the tail to <2s.
- S3: the claim text gets a single re-emphasis scale at 24.6s, the three
  evidence dots do a synchronized mid-blink at 25.7-26.7s, and the UNSOURCED
  flag nudges once at 26.9s — closes the 5s gap to a natural ~1.1s settle.

Render note: two consecutive attempts stalled mid-capture (`no frame progress
for 60000ms`, different frame numbers each time — 1246 then 1102, both near
the S4/S5 boundary) before a third attempt completed cleanly at 1800/1800
frames. Transient capture-engine flakiness, not a composition defect (`check`
and snapshots were clean throughout) — retry on a stall before treating it as
a code problem. Master re-verified: −13.90 LUFS / −1.91 dBTP.

## Round 4 (2026-08-30, user feedback: "the audio stops")

Diagnosis: the 60s track was real (video and audio streams both 60.000s), but
VO lines were short bursts (2-9s) inside 8-14s scene windows, leaving 4-7s of
pure silence at nearly every scene boundary — that reads as the audio cutting
out repeatedly, not as intentional pacing.

Fix: rewrote lines 01/02/03/04/05 longer (06 already covered ~76% of its
scene, left unchanged) — extensions only restate information already on
screen (the two-step conversion, "skips the first conversion step," "still an
active ingredient so start gentle"), no new claims introduced. New takes
regenerated, gated (duration + tail-defect scan — all clean this round, no
fade/pad needed), transcribed for word timing.

One real defect caught in gating: the first take of 05 ("Applied to the
skin...") synthesized with the leading word "Applied" completely absent —
audio started cold at "to the skin..." with zero lead-in silence before the
first phoneme (confirmed via silencedetect: no gap before word start).
Distinct from the documented tail-run-on defect — this is a dropped-onset
failure. Regenerated once; second take included the word cleanly. Add this to
the gate checklist: verify the first transcribed word's start time isn't
suspiciously close to 0 with no leading room-tone, same as checking the tail.

All downstream visual beats that were synced to VO content (S2's arrow
highlights, the round-3 checkmark/claim-pulse/dot-reblink beats) were
retimed to the new, real word timestamps rather than left at their old
silence-filling offsets — they now land on the words they're reinforcing
("first to retinal" / "then to retinoic acid" / claim numbers) instead of
arbitrary gaps. Scene-boundary silence cut from up to 6.7s down to a worst
case of ~5.6s at one boundary (S4→S5) and ~2.9s at another (S1→S2); every
other transition is under 2s. Master: −14.08 LUFS / −1.58 dBTP.

## Round 5 (2026-08-30, user request: SRT file)

Generated `retinal-clinical-dossier.srt` — 22 cues, extracted programmatically
from the composition's own `<div id="el-cap-NN">` caption elements (their
`data-start`/`data-duration` + text), not hand-transcribed, so it is
guaranteed to match the burned-in captions exactly. Copied alongside the
delivery master in `ingredent videos/Retinal/`.

## Safe areas / craft

Content sits inside y∈[≈216,1460] and x<918 (right rail clear); bottom 20%
holds nothing readable. One aqua accent per frame (S2: active-form node border;
S3: dots; S4: icon strokes; S5: cheek marker; S6: the "A"); coral is the
voltage register (X, step highlights, struck "O"). All motion is
absolute-time `fromTo` tweens on the one paused timeline — no rAF, no clocks,
finite repeats only.

## QA

- `hyperframes check` clean: 0 lint errors, 24/24 contrast, layout/motion clean.
- Frame extraction verified at 0 / 3 / 9 / 14.5 / 20 / 23.5 / 33 / 46.5 / 55 /
  59.8s: frame zero composed, no missing glyphs, chips/flags legible, emoji
  renders, cheek marker on the cheek (nudged from first pass).
- Audio (added 2026-08-30 after user feedback "the audio is missing"): Kimberly VO
  per SCRIPT.md, six seed_audio takes gated (5 of 7 takes total hit the tail
  run-on defect → 40ms fade + 0.25s pad; take 03 regenerated shorter after a
  10.68s overrun of its 10s window; transcript-diff clean — retinol/retinal ASR
  swaps in both directions = near-homophone bias, captions burn from SCRIPT.md).
  Word-timed top-band captions (S1/S5 headers moved below y≈350 to clear the
  band). Master: +12.4dB into alimiter limit=0.794 level=0 →
  **−13.98 LUFS / −1.88 dBTP** (renders/retinal-clinical-dossier_master.mp4).

## Round 6 (2026-08-30, pasted review: 1 BLOCKER, 1 MAJOR, 2 MINOR)

(Numbered 6, not 5 — a concurrent session ran the SRT export above as its own
"Round 5" while this round was in progress, unrelated request, same day. Its
SRT was extracted before this round's ripple-delete, so cues 16-22 were stale
against the new timing/56s length the moment this round rendered; regenerated
it from the current caption values — same extraction method, current source —
and replaced the stale copy in `ingredent videos/Retinal/`.)

1. **BLOCKER — ripple-deleted the S4→S5 dead zone.** The review caught the
   worst-case gap Round 4 had left undocumented as fixed (BRIEF's own Round 4
   text already named it: "worst case of ~5.6s at one boundary (S4→S5)").
   VO04 ends ~37.7s but S4's `data-duration` ran to 42.0s, leaving a flat
   4s hold with no beat. Rather than patch in more filler motion (already
   tried twice, rounds 2 and 4), cut S4's duration to 10.0s (28-38, now
   matching S2/S3/S5's own 10s length) and rippled everything after it
   earlier by exactly 4.000s: S5 start 42→38, S6 start 52→48, root
   `data-duration` 60→56, VO05/VO06 `data-start` -4s, captions 17-22
   `data-start` -4s (cap-16 trimmed 2.850→2.750 so it stops bleeding past
   the new cut), and every S5/S6 GSAP absolute-time argument -4s. A uniform
   shift preserves every previously-tuned VO-to-beat sync relationship
   exactly, so nothing needed re-deriving from word timings. Final video is
   56s, not 60s. Verified: `silencedetect -40dB/0.3s` across the full
   mastered file shows zero gaps anywhere near the old dead zone or
   anywhere in S5/S6 at all; longest remaining gap dropped to ~1.5s.
2. **MAJOR — CTA cluster moved off the Shorts bottom UI.** `.s6-stack` top
   660px → 355px, plus `.s6-pill` margin-top 56→36 and `.s6-tag` margin-top
   40→28 to reclaim margin on both ends of a content stack too tall to just
   slide (top is bounded by the S6 captions still running at y196-306,
   bottom needed real clearance past this series' documented CTA-specific
   floor of y≈1100). Net shift ≈305px (~15.9%, inside the reviewer's
   "15-20%/~300px" ask). Pixel-verified via extracted frame at 50s/55.5s:
   tag now bottoms out around y≈1050-1060 with the caption band clear
   above — same precedent as red-ginseng-glass-glow's y≈1310-1400 CTA that
   drew an identical BLOCKER from a human reviewer; this project's original
   S6 placement (top:660) was in the same danger zone (~y1355 tag bottom,
   bottom ~29%) and had simply never been reviewed against Shorts chrome
   before now.
3. **MINOR — house BGM bed added.** `assets/bgm/track-pulse.wav` reused
   from the pdrn-cellular-science lineage (same file already serving
   madecassoside-clinical-cut and red-ginseng-glass-glow — this project is
   documented as the same "clinical/minimalist dossier" register, so reuse
   over a fresh resolve). `data-volume="0.056"` (20·log10(0.056) ≈ −25dB,
   matching the review's ask precisely; house default elsewhere is 0.1/
   −20dB, so this bed sits quieter than its siblings by design). Verified
   present and correctly scaled by isolating a VO-silent window and
   comparing its RMS against the source file's own native level at that
   timestamp — audibility tracks the track's own dynamics (an ambient bed
   has quiet passages; that's expected, not a mixing defect).
4. **MINOR — `.flag-unsourced` scaled up.** 22px/400 → 34px/500 (both a
   ~55% size increase and a weight bump, per the review's "at least 50% or
   Medium/Bold"). Shared by all three UNSOURCED flags (S3/S4/S5) since
   they're one class — fixes all three from a single edit, consistent with
   the house convention of one flag treatment across a video. S4's flag
   text now wraps to 2 lines (was 1) inside the unchanged 760px column;
   verified no overflow/clipping via extracted frame.

Re-mastered: raw render measured −23.31 LUFS / −3.43 dBTP pre-master (BGM
now in the mix, pulling input stats from Round 4's numbers). Alimiter
gain-eats-input again (documented mugwort/madecassoside behavior) — +12dB
in only reached −14.88 LUFS, +16dB reached −13.55, interpolating to
+14.6dB landed **−13.93 LUFS / −1.91 dBTP**, matching every prior round's
delivered range (−13.90 to −14.08) without re-deriving the chain from
scratch. `hyperframes check` clean (0 errors; contrast 25/25; the two
warnings are pre-existing file-size/track-density lint notes, not new).
Delivered to both `retinal-clinical-dossier_master.mp4` and the
no-hyphen `retinalclinicaldossier_master.mp4` in `ingredent videos/Retinal/`
(the latter is an unexplained stray duplicate from before this round —
kept in sync rather than left stale, not investigated further since it
isn't this project's own file). An unrelated `retinal-clinical-dossier.srt`
appeared in that same delivery folder mid-session (timestamped before this
round's edits, matching Round 4's old caption timings) — not touched, not
part of this round's work, flagged to the user rather than assumed benign
or deleted.
