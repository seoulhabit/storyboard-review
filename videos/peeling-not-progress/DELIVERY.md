# Delivery — peeling-not-progress

First `DELIVERY.md` in this repo — `faceless-video-craft` SKILL.md names the format for
any project past a couple of scenes, but no prior video here had actually written one.

**Updated 2026-08-31** for a skill-update reconciliation pass — `faceless-video-craft`
SKILL.md gained a pre-render gate, raised type floors, a citation-ID ban, and this very
manifest requirement after the render this file originally described. Five real defects
were found and fixed against the updated rules; full account in `frame.md § Post-render
review fixes` round 5 and `STORYBOARD.md`'s matching note. This version replaces the
render, the verification record, and adds the gate section below.

## Render

**`renders/peeling-not-progress_FINAL_mastered.mp4`** — the only render kept; every
earlier iteration from this round's fix-and-reverify loop was deleted once superseded,
per house convention.

- 30.016s video (900 frames, 30fps — confirmed via `ffprobe -count_frames`; video
  stream copied through unchanged by the loudness pass), 1080×1920, h264 video / AAC
  192kbps audio.
- Loudness-normalized: two-pass `ffmpeg loudnorm` (measured pass, then a linear
  second pass against the measured values), video stream copied through unchanged.
  Measured **−14.04 LUFS integrated / −1.60 dBTP** (target −14 LUFS / −1.6 dBTP in
  PCM, per this channel's AAC-encode-headroom convention) — confirmed via an
  independent `astats` peak-level check on the final AAC file (−1.06 to −1.32 dB
  per-channel peak, safely under 0 dBFS), not just loudnorm's own report.
- No voiceover in this project (see BRIEF.md's silent-first decision record) — the BGM
  bed (`assets/bgm/track.mp3`, reused from `retinol-patch-test`) plus 7 SFX cues are
  the only audio, unchanged by this round (no scene timing moved).

## Captions

**None — a deliberate departure, not an oversight.** There is no speech in this video,
so there is no transcript to generate a burned-in caption track or a sidecar `.srt`
from. The on-screen kinetic type carries all of the video's language; it is the only
text layer and was authored directly rather than derived from ASR. This departs from
the skill's "produce the `.srt` even for a short once the transcript exists" line,
which is predicated on a transcript existing — see BRIEF.md § Customizations.

## Thumbnail

**`assets/thumbnail/thumbnail-final.png`** — Frame 1's hook payoff (the droplet on its
surface panel, ink ground), lightly graded (`eq=contrast=1.05:saturation=1.08,
unsharp=5:5:0.4`, derived from this video's own palette, not copied from another
project's grade). Chosen over two other real candidates after checking all three at
actual browse-grid scale (120×67, downscaled and inspected at 5× nearest-neighbor to
see exactly what survives): the barrier-wall and "MORE IRRITATION" text-driven
candidates both went illegible at that size, while the droplet's simple, high-contrast
graphic shape read instantly. Rejected candidates kept alongside it, not deleted:
`assets/thumbnail/candidate-barrier-wall-source.png`,
`assets/thumbnail/candidate-more-irritation-source.png`. Unaffected by this round —
Frame 1's droplet plate itself didn't change.

## Chapters / end screen

Not applicable — a 30s Short takes neither chapters nor end-screen elements (YouTube
reserves those for long-form; a Short gets one related-video link instead). The
equivalent mechanism for a Short is the engineered loop: Frame 6 hands back to Frame
1's ink ground at a matched centered hero position (see `STORYBOARD.md`'s arc note;
re-verified after this round's type changes — within 1.5px of Frame 1's droplet-panel
center).

## Pinned comment / description copy

**Description:**
> Visible peeling isn't a scorecard — it's a side effect. A 30-second audit of what
> "more actives, more results" actually gets you, and what your skin is really asking
> for. Sources in the video; full citations below.
>
> — PMID 7544967 (Griffiths et al., *Arch Dermatol* 1995)
> — PMID 21284283 (Draelos et al., *Cutis* 2010)
> — 21 CFR §333.350 (FDA acne-drug labeling)
> — PMID 17121065 (Draelos et al., *Cutis* 2006)
> — FDA-2000-P-0063 (FDA AHA labeling guidance, Jan 2005)

These PMIDs and the docket number are exactly where the skill's new citation rule says
they belong — the on-screen pills now carry only the human-readable `Journal · Year`
form (see the gate item 9 below); this description block is their one place to appear.

**Pinned comment** — this round moved the video's own former closing line here, since
the on-screen close (below) is now a specific action instead of a generic prompt:
> What skincare claim should we audit next? Drop it below.

## Catalog contribution

**`catalog/visual-components/barrier-wall/`** — the barrier-wall diagram (adapted for
Frame 3) harvested as `BarrierWall`, with generalized placeholder content, a paused
seekable clock, and a debug scrubber matching the catalog's existing convention. This
was the mechanism's **third** independent build in this repo (after
`betaine-salicylate-gentle-bha`'s SVG original and `ceramides-barrier-diagnostic`'s
CSS-grid variant) while still absent from the catalog — exactly the repeated-rebuild
failure the catalog lifecycle exists to prevent. Indexed in `catalog/README.md` and
`catalog/index.html`'s browsable gallery. **Updated this round** — the spike carried
Frame 3's pre-fix type sizes and a field contract permitting "your own claim + citation
id"; both corrected so the next video that installs it inherits the new floor and the
human-readable-citation rule instead of this project's original defects.

The two-card boundary mechanism (adapted for Frame 4, from `retinol-patch-test` +
`snail-mucin-medical-secret`'s `split-tilt-cards.html`) is a second harvest candidate,
noted in `frame.md § Catalog contribution` but not actioned this round.

## Verification record

Full account in `frame.md § Post-render review fixes` and `STORYBOARD.md`'s post-render
notes, across five render-and-reverify rounds (four for the original build, a fifth for
this skill-update reconciliation pass).

**Round 5 summary (2026-08-31):** five defects found against the updated skill, all
confirmed by pixel extraction on the actual render before fixing:
1. Frame 2's citation chip rendered inside the platform overlay zone (a literal `0`
   bottom padding where every other scene used `var(--safe-bottom)`) — fixed.
2. Every citation pill carried an internal PMID/CFR lookup ID — converted to
   `Journal · Year` form throughout.
3. Type sat below the skill's raised floors in 5 of 6 frames — raised (96px hero /
   40px body / 32px label-and-chip) across all six.
4. `--safe-right` was declared and never consumed — all six frames re-fit to
   asymmetric safe-left/safe-right padding and the resulting 858px content column.
5. `scripts/check-static-hold.py` carried a mis-ported caption-band crop from a
   different project — this video has no captions; corrected to scan the full frame.

A first fix attempt for finding 1's class of defect (also present in Frames 3 and 5)
measured **zero effect** on the actual render — the real cause was each scene's own
Ken-Burns zoom displacing bottom-safe content as it scales, not the static layout.
Fixed by reserving zoom-sized static margin instead. Frame 6's lockup needed a
calculated correction after the type raise broke its matched loop position; re-verified
within 1.5px of Frame 1's panel center after the fix.

Final render, fully re-verified (not re-assumed from the edits): all four citation
chips clear the y1560 safe-bottom boundary with 12–80px of real margin; safe-right
honored on all six frames; loop hand-off match within 1.5px; phone-scale downscale
(25%) confirms every headline, label, and pill legible; `check-blank-frames.py`
unchanged (same five 267–533ms scene-opening windows, all pre-existing and judged
acceptable reveal-beat gaps, unrelated to this round); `check-static-hold.py` zero
findings on the full frame (a trustworthy result now, not a blind one); `hyperframes
check` clean throughout (0 errors/warnings, 17/17 contrast checks passing).

## Pre-render gate

Answered per `faceless-video-craft` SKILL.md's binary checklist, against the actual
final render, not the pre-fix draft:

1. **Hook legible from a single silent frame at ~0:01?** Yes — the droplet-on-cracked-
   surface image plus "Does that mean it's working?" reads standalone.
2. **Every important label readable at phone scale?** Yes — confirmed via 25% downscale
   of four representative frames (Frames 2–5) post-fix; all headlines, object labels,
   and citation pills legible. Failed pre-fix (22–26px chips), fixed this round.
3. **One dominant focal point per scene?** Yes — one hero element per frame throughout
   (droplet / headline+bottles / barrier wall / two cards / three objects / lockup).
4. **Motion explains something, not decoration?** Yes — every tween (crack-draw,
   strike-and-resolve, wash-descend/shard-detach, card slide, object stagger,
   glyph-converge) illustrates the beat's own claim; the continuous Ken-Burns pushes
   are the one exception, present specifically to avoid a static-hold flag rather than
   to explain anything, per the skill's own sanctioned use of that pattern.
5. **A real photographic/tactile visual early, or a recorded reason it's absent?**
   Reason recorded — house rule bans generative/photographic imagery on this channel
   entirely (`catalog/ingredients/one-percent-line/README.md:113`); logged in
   `BRIEF.md § Assets`, `frame.md § Media exception`, and (this round) `STORYBOARD.md`'s
   beat sheet itself.
6. **Palette, type, captions, channel mark consistent?** Yes — `assets/tokens/tokens.css`
   palette throughout; no captions exist (recorded departure, see above); 습 SeoulHabit
   lockup in Frame 6 matches the channel mark.
7. **Safe-area tokens actually consumed by every scene?** Yes, as of this round —
   `--safe-right` was declared in all six frames and consumed by none pre-fix; now
   every frame pads asymmetric `--safe-left`/`--safe-right`.
8. **A real sidecar caption file exists?** N/A, recorded departure — no speech, no
   transcript to export one from (see Captions above).
9. **All on-screen citations real and human-readable, with no internal IDs?** Yes, as
   of this round — every PMID/CFR/docket ID converted to `Journal · Year` form; the
   IDs themselves moved to the description (above), never on screen.
10. **No placeholders, unfinished text, or debug-overlay artifacts in frame?** Yes —
    grep-clean across all six composition files (TODO/FIXME/PLACEHOLDER/debug), both
    before and after this round's edits.
11. **Closing beat one specific, lesson-tied action, not a generic subscribe card?**
    Yes, as of this round — Frame 6 now closes on "Peeling? Drop to one active for two
    weeks." (sourced from the video's own cited beats), not the prior generic audit
    prompt, which moved to the pinned comment only.
12. **Does the video still make sense with the sound off?** Yes — every claim, source,
    and instruction is carried by on-screen type; the BGM/SFX are texture, not
    information (this was already true pre-fix and unaffected by this round's changes).
