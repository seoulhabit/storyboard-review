# Delivery — pilling-vs-peeling (Round 3, 2026-09-01)

Two variants shipped for A/B testing per the creator review's explicit ask.
**Variant A is the primary/default upload** (real macro pilling hook);
variant B is the split-screen teaser hook for a second, separate upload.
YouTube has no native Shorts A/B mechanism — these are two independent
uploads, a quasi-experiment, not a platform-run test; match posting
day/time before comparing retention.

## Renders

**Round 3 retimed `07-fix-peeling` (2.1s → 3.3s, +1.2s) per direct creator
feedback on round 2's render** — "scene 7 feels rushed." Both variants
share scenes 02–08, so both grew by the same 1.2s.

| | File | Duration | Loudness | True peak |
|---|---|---|---|---|
| **Variant A** (primary) | `renders/pilling-vs-peeling.mp4` | 21.1s (633 frames, 30fps), 1080×1920, h264/AAC 192kbps | −14.3 LUFS integrated | −2.0 dBTP |
| **Variant B** | `renders/pilling-vs-peeling_hookB.mp4` | 21.1s, 1080×1920, h264/AAC 192kbps | −14.2 LUFS integrated | −2.1 dBTP |

Both mastered via two-pass `ffmpeg loudnorm` (target `I=-14:TP=-2.5`, the
same target round 2 established, re-applied fresh after this round's
re-render). Video stream copied through unchanged (`-c:v copy`) during
mastering — confirmed via matching MD5 on the isolated video stream,
both variants.

No voiceover (`VO_MODE: silent`, unchanged from round 1). BGM re-cut to
21.1s (was 19.9s) with 200ms declick fades at both ends. Tactile SFX added
for the press/rub beat, both macro→diagram match cuts, the comparison wipe
(forward and return), and each of the three demoed tips; scene 07's 4 cues
and scene 08's 2 cues retimed this round to the new beat schedule (see
BRIEF.md § Round 3 for the exact cascade).

## Captions

Burned-in: none — silent, type-carried piece.

Sidecar, one pair per variant (only the first cue differs):

- **`captions/pilling-vs-peeling.srt`** / **`.vtt`** — 14 cues, variant A.
- **`captions/pilling-vs-peeling_hookB.srt`** / **`.vtt`** — 13 cues, variant B.

All cues re-derived from round 2's own scene timings and copy deck, hand-
authored (no ASR — there's no voiceover to transcribe). Every cue is ≥1.0s
(round 1 shipped 10 of 29 cues under 0.5s, shortest 0.15s — each on-screen
element's entrance had become its own cue; round 2 merges co-occurring
copy into one cue per beat instead). Round 3 shifted every cue at or after
the old 17.9s mark by +1.2s in all four files, matching scene 07's own
retime — cue text unchanged, only timing.

## Thumbnail

**`assets/thumbnail/thumbnail-final.png`** — extracted from variant A at
t=1.6s (the hook's payoff: real macro pilling residue + "Those white flakes
may not be your skin."), light grade (contrast 1.08×, saturation 1.05×),
confirmed legible at 68×120 grid scale
(`assets/thumbnail/candidate-hookA-grid-check-5x.png`). Replaces round 1's
thumbnail, whose hero panel measured 1.05:1 contrast against its own ground
and was effectively invisible at grid scale.

## Imagery

Four generated macro plates in `assets/plates/` — see BRIEF.md § Round 2 §
Imagery decision record for the full Why/Precedent/Scope filing. Summary:
`01-pilling-macro.png` (hook), `02-layering-hand.png` (product residue),
`03-flaking-skin.png` (peeling), `04-base-skin.png` (the bare/layered
comparison base, both sides of the wipe are this one plate — the "layered"
state is a browser-drawn overlay, not a second generation). Generated via
Higgsfield `nano_banana_pro`, one consistent grade applied across the set.

## Full source list (for the video description)

- Lua BL, Ruan L, Lyu Y, Liu S. *Understanding the causes of skincare
  product pilling.* Skin Res Technol. 2024 Aug;30(8):e13828. PMID 39092468.
  DOI: https://doi.org/10.1111/srt.13828
- 21 CFR § 333.350(c)(4)(ii) — FDA topical acne drug product labeling,
  local irritation (burning, itching, peeling, swelling):
  https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-333/subpart-D/section-333.350
- Draelos ZD. *Hydration and skin barrier function.* Cutis. 2006.
- FDA AHA labeling guidance, Jan 2005 (FDA-2000-P-0063).

## Title

**Pilling vs. Peeling — Which One Is It?** (unchanged)

## Description (draft)

Pilling and peeling can look similar — but they call for very different
fixes. Bare skin flaking points to peeling; crumbs that only show up after
layering point to pilling — a clue, not a diagnosis. If peeling is painful,
severe, blistering, or persistent, speak with a dermatologist. Educational,
not diagnostic.

Sources: Lua et al., *Skin Res Technol* 2024 (DOI: 10.1111/srt.13828) · 21
CFR § 333.350

## Pinned comment (draft)

What are you seeing — crumbs after layering, or flakes on bare skin? Tell
me below.

## End-screen / next-video target

Not applicable — standalone Short. Related viewing:
`videos/pilling-not-dead-skin` and `videos/peeling-not-progress` cover
their half of this differential in more depth.

## Catalog contribution

**`FactorConverge`** (scene 03's 3-node convergence diagram, renumbered
from round 1's scene 04 — same component, same catalog entry) —
`catalog/visual-components/factor-converge/`, unchanged this round.

## What shipped this round that a future round should reuse

- The macro→diagram match-cut technique (scene 02, scene 04): a real plate
  zooms briefly, then hard-cuts to a diagram at the exact same box
  position/size. Worth a catalog entry if a third video uses the same move.
- The wipe-comparison mechanism (scene 05): a fixed-px wipe-mask holding a
  second copy of the same base image plus a drawn overlay, revealing then
  partially retreating to a genuine side-by-side. Also a catalog-worthy
  mechanism — not harvested this round for time, flagged here instead.
- The `box-sizing: border-box` + `min-height: 0` defect and fix (see
  `frame.md` § Verification § 2) — proposed as a `faceless-video-craft`
  SKILL.md addition this round; check whether it landed before assuming a
  future project needs to rediscover it.

## Verification record

See `frame.md` § Verification for the full account. Summary:

| Check | Result |
|---|---|
| `npx hyperframes check` | 0 errors, 1 pre-existing warning unrelated to this round (see `frame.md` § Verification — Round 3 § 1), 6 benign info findings |
| Render pipeline | Caught a real gap: plain `npm run render` writes a timestamped file, not `renders/pilling-vs-peeling.mp4` — the postrender scripts hardcode that filename, so the first postrender pass after this round's render validated the *stale* round-2 file. Caught by checking `ffprobe` duration before trusting the result; fixed by promoting the new render and re-running. See `frame.md` § Verification — Round 3 § 2. |
| `check-blank-frames.py` | 0 findings, 317 frames sampled (on the correct, promoted file) |
| `check-static-hold.py` (whole-frame) | 0 findings, 42 samples |
| `check-static-hold.py` (region-aware) | Still falls back to whole-render mode — round 2's open item, not addressed this round |
| `check-safe-area.py` (hard gate) | 0 findings, both variants (84 samples each) |
| `check-sfx-durations.py` | 0 findings, 23/23 checked |
| Audio mastering | −14.3/−2.0 dBTP (A), −14.2/−2.1 dBTP (B), video MD5-confirmed unchanged, loop-seam RMS −16.2 dB (live, not silent) |
| Visual spot-check, scene 07 | 6 frames extracted across the new timeline, beat schedule confirmed landing where authored (see `frame.md` § Verification — Round 3 § 7) |
| Thumbnail | Unaffected by this round (t=1.6s sits in scene 01, untouched) |
