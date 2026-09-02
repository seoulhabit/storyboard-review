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
a short and ~15 s of long-form. Consequences:
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
