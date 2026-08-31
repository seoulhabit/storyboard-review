# Delivery — peeling-not-progress

First `DELIVERY.md` in this repo — `faceless-video-craft` SKILL.md names the format for
any project past a couple of scenes, but no prior video here had actually written one.

**Updated 2026-08-31** for a skill-update reconciliation pass — `faceless-video-craft`
SKILL.md gained a pre-render gate, raised type floors, a citation-ID ban, and this very
manifest requirement after the render this file originally described. Five real defects
were found and fixed against the updated rules; full account in `frame.md § Post-render
review fixes` round 5 and `STORYBOARD.md`'s matching note.

**Updated again same day** for an external QC report and the round-6 fix it prompted —
a rendered-pixel safe-area bug (three scenes overshot the real bottom/right line by
5-10px despite every scene consuming its `--safe-*` tokens correctly, plus a fourth,
previously undetected transient in Frame 1) and a captions gap the skill's
transcript-predicated caption rule had a blind spot for. Full account in `frame.md
§ Post-render review fixes` round 6. This version replaces the render, adds the
captions deliverable, and updates the verification record and gate below.

## Render

**`renders/peeling-not-progress_FINAL_mastered.mp4`** — the only render kept; every
earlier iteration from this round's fix-and-reverify loop was deleted once superseded,
per house convention.

- 30.1s container duration (900 frames, 30fps — confirmed via `ffprobe -count_frames`;
  video stream copied through unchanged by the loudness pass), 1080×1920, h264 video /
  AAC 192kbps audio.
- Loudness-normalized: two-pass `ffmpeg loudnorm` (measured pass, then a linear
  second pass against the measured values), video stream copied through unchanged.
  Measured **−14.04 LUFS integrated / −1.60 dBTP** (target −14 LUFS / −1.6 dBTP in
  PCM, per this channel's AAC-encode-headroom convention) — confirmed via an
  independent `astats` peak-level check on the final AAC file (peak −1.20 dB, safely
  under 0 dBFS), not just loudnorm's own report. Matches round 5's figures — the
  audio layer itself wasn't touched this round.
- No voiceover in this project (see BRIEF.md's silent-first decision record) — the BGM
  bed (`assets/bgm/track.mp3`, reused from `retinol-patch-test`) plus 7 SFX cues are
  the only audio, unchanged by this round (no scene timing moved).
- **Round-6 fix**, re-rendered and re-mastered: a rendered-pixel safe-area bug across
  Frames 1/3/4/5 (fixed) and a captions gap (fixed, see below) — see `frame.md
  § Post-render review fixes` round 6 for the full measured account.

## Captions

**`captions/peeling-not-progress.srt` and `captions/peeling-not-progress.vtt`** —
21 SDH-style cues, hand-authored directly from `STORYBOARD.md`'s copy deck and
`index.html`'s scene timings, not from ASR (there is no speech to transcribe — see
BRIEF.md's silent-first decision record — and the on-screen text plus its exact
timing were already authored artifacts, so no transcript step was needed). Every
citation pill's text is included as its own cue; the two narratively meaningful SFX
(`[wall crumbles]`, `[chime]`) are bracketed; routine UI clicks are omitted per SDH
convention. Every cue verified to land inside the scene whose text it transcribes.

This corrects a round-5 gap: the prior "None — deliberate" note above was a correct
read of the skill's transcript-predicated caption workflow (no VO exists, so ASR
doesn't apply) but an incomplete read of the actual requirement — 100% of this
video's language is on-screen type, and a captions/screen-reader user got nothing
without a sidecar. See `frame.md § Post-render review fixes` round 6 and the
`faceless-video-craft` SKILL.md update it prompted (*The captions* now names this
case explicitly).

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
`assets/thumbnail/candidate-more-irritation-source.png`. Unaffected by round 5 —
Frame 1's droplet plate itself didn't change.

**Re-confirmed for round 6, not just assumed carried-forward.** The shipped
thumbnail is a frame from before any text is on screen at all (the panel and
droplet only — no `.text-stack` content yet), and round 6's Frame 1 changes were
both text-layer-only: removing `translateY` from `#line-1`/`#line-2`'s entrance
(the panel and droplet markup/position are untouched), and a `.stage` `gap`
experiment that was tried, found to shift the panel, and reverted back to its
original value (see `frame.md` round 6's loop-match regression note) — so the
panel ends this round in the exact same position it started in. Opened the actual
file and visually confirmed: still the pale panel + droplet + finite ripple dots,
no text, pixel-unaffected.

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
form (see gate item 9a below); this description block is their one place to appear.

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
notes, across six render-and-reverify rounds (four for the original build, a fifth for
the prior skill-update reconciliation pass, a sixth for this round's external QC report
and the checker it exposed the need for).

**Round 6 summary (2026-08-31):** an external QC report's five findings were each
reproduced against the actual render before acting (per this skill's "a QC report is a
claim, not a diagnosis" rule) — two (the BLOCKER outro-position claim, the MAJOR
outro-duration claim) didn't reproduce at all; two (Frame 3's citation, Frame 4's
right card) were real but misquantified by 25-30x versus the report's own numbers; one
(no captions) was real. A fourth safe-area violation the report never named (Frame 5)
was found by direct measurement, and a fifth (a ~150ms entrance transient in Frame 1)
was found only after building `scripts/check-safe-area.py` and running it against the
render at 4fps — finer than any prior round's spot-checks. Root cause for all four real
safe-area violations: a Ken-Burns `transform: scale()` (or, for Frame 1, an entrance
`transform: translateY()`) sitting between a correctly-padded box and the canvas, which
none of the six scenes' source-level `--safe-*` consumption could catch. Fixed by
deriving each zoomed scene's padded edge from its own scale/origin instead of a
hand-tuned constant (see `frame.md`'s full math), and by removing Frame 1's entrance
transform outright. A first fix attempt (trimming Frame 1's `.stage` gap for extra
margin) was reverted after re-measuring showed it shifted the panel's center 12px and
broke the round-5 loop hand-off — the `translateY` removal alone was sufficient and
left the panel position untouched.

Re-verified end to end on the corrected, re-mastered render (an independent 4fps
ink-extent scan, not just the new script's own "no findings"): zero frames with ink in
any reserved zone across all six scenes; real margins of 5-6px on the three previously
-failing scenes (Frame 1 y1531, Frame 3 y1530, Frame 4 x912, Frame 5 y1531); loop
hand-off match within 1px (771.5 vs 770.5, tighter than round 5's 1.5px); phone-scale
(25%) legibility confirmed on all affected frames; `check-static-hold.py` and
`check-blank-frames.py` both unchanged from round 5.

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
   palette throughout; captions now exist as of round 6 (see above); 습 SeoulHabit
   lockup in Frame 6 matches the channel mark.
7. **Safe-area tokens actually consumed by every scene, AND no rendered pixel inside
   a reserved zone?** Yes to both, as of round 6 — consumption alone (7a) was already
   true as of round 5, but three scenes still shipped ink 5-10px past the real line
   because a Ken-Burns transform sat between the padded box and the canvas; a fourth
   (Frame 1) overshot via its own entrance transform. Fixed this round by deriving
   the padded edge from each scene's own scale/origin and by removing Frame 1's
   entrance transform; confirmed on rendered pixels (7b), not just source, via
   `scripts/check-safe-area.py` and an independent re-measurement — see the
   Verification record above.
8. **A real sidecar caption file exists?** Yes, as of round 6 —
   `captions/peeling-not-progress.srt` and `.vtt`, hand-authored from the storyboard
   and scene timings (no VO to transcribe, so no ASR step, but a sidecar exists all
   the same — see Captions above).
9a. **All on-screen citations real and human-readable, with no internal IDs?**
    Yes, as of round 5 — every PMID/CFR/docket ID converted to `Journal · Year`
    form; the IDs themselves moved to the description (above), never on screen.
9b. **Does every on-screen claim/instruction stand on its own in plain language,
    independent of the citation next to it?** Yes, checked directly against the
    full current copy deck — every claim/instruction ("Severe burning or
    swelling? Stop and ask a doctor.", "In trials, more irritation didn't mean
    better results.", "Start slowly. Follow directions. Protect the barrier.")
    is plain English on its own; the citation pills (`Arch Dermatol · 1995`,
    `21 CFR 333.350`, `Cutis · 2006`, `FDA guidance · 2005`) do pure provenance
    work beside already-understandable sentences, never carrying meaning the
    viewer needs to decode. New gate item this round — see `faceless-video-craft`
    SKILL.md's "untranslated clinical/technical register" entry; this project
    is the worked passing example cited there.
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
