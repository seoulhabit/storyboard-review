# YouTube delivery — the platform layer

Read **before** the beat sheet, not at publish time; everything here is a
beat-sheet input. Platform numbers drift — safe-area percentages and limits are
current-as-written; verify anything load-bearing before a real publish, and
prefer the channel's own measured curve (`channel-baseline.md`) over any
general claim here.

## Formats

| | Long-form | Short |
|---|---|---|
| Canvas | 1920×1080 (16:9) | 1080×1920 (9:16) |
| Length | policy `[S1/S-2]` | ≤ 3:00 platform limit; policy targets 30–58 s |
| State-change cadence | every 8–12 s | every 1.5–3 s |
| End screens / cards | yes | no — one related-video link |
| Chapters | yes (≥ 3, first at 0:00, each ≥ 10 s) | no |
| Thumbnail | generated + scored `[S3/P-3]` | frame 0 |

For a short, set the beat sheet's `canvas` to `{ "w": 1080, "h": 1920 }`; the
generator emits `data-resolution="portrait"`, the matching `#root` dimensions,
and the portrait safe-area insets. Structure scenes as rows, not columns.

For long-form, set `canvas` to `{ "w": 1920, "h": 1080 }`; the generator emits
`data-resolution="landscape"` on `<html>` (not on the root) and the landscape
insets below. **The "rows, not columns" note above is a correction for the
vertical failure mode and does not transfer** — see *Long-form safe areas*.

**The type scale is the same for both.** 1080×1920 and 1920×1080 share a 1080px
short edge, and type size is a fraction of the short edge, so `[S6/A-6]`'s floors
apply unchanged to landscape. Do not scale the scale in either direction: ×0.5625
pushes body copy under the floor, ×1.78 inflates a headline off the frame. Layout
needs an explicit per-canvas variant; type does not.

**Transitions and continuity are format-scoped too, and the cadence row above is
a floor rather than a pass.** A Short cuts on the grid; long-form runs a 2-3
type transition system, a camera path and actors that persist across the cut —
`[S6/A-8]`, `[S6/A-9]`, `[S6/A-10]`. A 340s piece that met this table's 8-12s
cadence everywhere, and passed every other gate, was still reviewed as "a
sequence of separate slides" because all 28 of its boundaries were hard cuts and
65% of its tweens shared one entrance signature. Cadence answers "is anything
happening"; continuity answers "is this one film".

## Long-form safe areas

A 16:9 frame has no action rail and no title strip, so the Shorts numbers are
*semantically* wrong there, not merely miscalibrated. Reserve:

- **Bottom 108 px (10 %)** — player progress bar and controls. Persistent on
  mobile, on-hover on desktop. The only zone binding every frame hard.
- **Top 54 px, left/right 96 px (5 %)** — broadcast action-safe convention.

**The end-screen reserve is scene-scoped, and that is the structural difference
from Shorts.** The Shorts rails bind every frame of the piece; the end-screen
zone binds only the final 5–20 s. Reserving it globally wastes the right third of
every frame in the video. On the final scene alone: ≤ 4 elements inside the inner
80 % (192 px left/right, 108 px top/bottom), video/playlist ≈ 613×343, subscribe
and channel circles ≈ 298 px diameter; keep the **right third (~640 px) and the
lower-right** clear of anything that must be read. Verify in Studio before a real
publish.

**The gate is `catalog/tooling/check-safe-area.py --landscape`**, and it must be
passed that flag. Before 2026-09-02 both QC scripts hard-coded a portrait canvas
with no override, and on a landscape render the bottom-zone slice ran past the
end of a 1080-tall array: numpy returned an empty view and the **hard gate
reported "no findings" and exited 0**, while the right-zone slice measured the
right 52 % of the frame instead of a 96 px margin. Both scripts now probe the
render with `ffprobe` and refuse (exit 2) on a canvas mismatch. A clean gate
result is only evidence if the gate measured the canvas you actually rendered.

**The wide-canvas layout failure inverts.** Vertical fails as a small element
marooned in a tall empty column; landscape fails as a full-width band of text
with no depth behind it. The native 16:9 shapes are two-column (claim left,
evidence right), hero-left/diagram-right, full-bleed plate with a caption rail,
and a genuine three-across row. Hero copy still occupies 60–80 % of *available*
width — but in landscape that should usually mean a grid column, not the whole
1728 px safe width.

## Shorts safe areas

The Shorts player overlays UI. Keep anything that must be read out of:
- **Right edge ~15 %** — like/dislike/comment/share rail.
- **Bottom ~20 %** — title, channel, audio attribution.
- **Top ~10 %** — search and camera icons.

Safe zone = centre-left column. Kinetic type drifting into the rail is the most
common Shorts defect and is invisible in a bare-browser preview. Three things
catch it, in increasing order of authority:
- the generated scene draws the zones in `#root.debug-layout` on vertical canvases;
- `scripts/extract_frames.sh` writes `safe-zone-*.png` for the eye;
- **`catalog/tooling/check-safe-area.py` is the gate** — it measures real ink
  inside the reserved zones on transformed, rendered pixels, and exits non-zero.
  A source-level "are the `--safe-*` tokens consumed" audit structurally cannot
  see a `transform: scale()` moving compliant padding past the real line.

Declare the safe tokens *and consume them* — a `--safe-*` token nothing reads is
the defect this pairing exists to prevent.

## The hook

Retention on this channel is decided where the channel's own curve says it is
(baseline `retention.first_drop_s`); with no baseline, assume the first ~3 s of
a short and ~15 s of long-form — but note this number is **unresolved**: v1's
SKILL.md says ~8 s for long-form, this file says ~15 s, and neither is measured
on any real channel. Where the baseline has retention data, it wins and the
ledger records that it was used; where it doesn't, record the figure as an
assumption in the beat sheet rather than inheriting whichever document was read
last. Consequences:
- **Cold open.** No logo, no fade-from-black, no title card. Frame 0 is the
  hook — the strongest visual claim of the piece, already composed.
- The first beat states the payoff or the tension, never the setup.
- In Shorts, engineer the loop: the last frame hands back to the first so a
  replay feels seamless — replays count as retention.

## Chapters map to the beat sheet

Chapters are the spine made public. They come from `[S5/C-1]`, first at 0:00,
each ≥ 10 s, named as payoffs ("Why the label lies"), not sections ("Part 2").
If the beat sheet cannot produce coherent chapters, the beat sheet is wrong —
fix it there.

## The end screen is a scene

The last 8–20 s of long-form carry end-screen elements YouTube draws *on top
of* the composition. The final scene is designed as a frame for them: reserved
negative space where the elements land (right third and lower-right by
convention — verify in Studio), motion calmed, no text in the overlay zones,
and the VO's handoff line ("the next one shows…") timed to it. A video that
ends on its content peak wastes its highest-intent moment.

## What "interactive" can actually be

No true in-player branching exists. The real inventory:
- **End screens + cards** → chained-video branching (two elements → two videos).
- **Chapters + description timestamps** → viewer-seekable structure.
- **Pinned comment + polls** → the feedback channel that scripts the next video.
- **Shorts** → one related-video link; branching happens across shorts.

Design branching as a *graph of videos* with the composition as one node.

## Audio and captions

- The composition is **silent by design**; VO and music are muxed afterward
  (`[S7/R-3]`). The VO's measured duration is the master clock (`[S4/V-2]`).
- **Captions are type.** A large share of Shorts viewing is muted; narration
  text appears as composed, beat-timed typography inside the safe zone, sized to
  the caption floor in `[S6/A-6]` (42–56 px). A claim made only in the voiceover
  is a claim most of this channel's audience never receives: measured, 88.1 % of
  views come from the Shorts feed. Ship `.srt` and `.vtt` alongside the MP4.
- Master to −14 LUFS integrated. **Encode at `TP=-2.5` on the `loudnorm` pass,
  not −1.5**: AAC raises intersample true peak, and a file measured at −1.50
  dBTP on the PCM intermediate has shipped at **+0.5 dBFS**. Re-measure
  `ebur128` on the actual delivered MP4 (`[S7/R-3]`, verbatim rule R6). Louder
  than −14 is simply turned down by the platform.

## Packaging facts the pipeline relies on

- Title ≤ 70 characters with the seed keyword in the first 60 (`[S3/P-1]`).
- Thumbnail overlay text ≤ 3 words and not a repeat of the title (`[S3/P-2]`).
- Description: hook line first (it is the search snippet), chapters, sources,
  pinned-comment question last.
- Tags: seed + ≤ 9 related with `overall ≥ 30` (`[S3/P-4]`).
