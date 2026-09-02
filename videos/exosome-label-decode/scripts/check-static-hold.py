#!/usr/bin/env python3
"""Scan a rendered MP4 for a static-hold: real content that stops changing for
longer than a short's cadence ceiling, even though it is never blank.

This is the gap check-blank-frames.py cannot close. That script measures
per-frame luma stddev (blankness) — a frozen but fully-populated frame reads
identically to a healthy one on that metric, so a scene that lands all its
beats early and then sits frozen for the rest of its narration sails through
it clean. Confirmed on `videos/peeling-not-progress`'s own sibling channel
project, `videos/glass-skin-5-habits`, 2026-08-30: a CTA/endcard scene
measured several seconds frozen — invisible to check-blank-frames.py and to
`hyperframes check` alike (neither measures frame-to-frame change).

CORRECTED 2026-08-31 (peeling-not-progress): that project's copy of this
script inherited a hardcoded CAPTION_BAND_TOP/BOTTOM (960-1110) from a
different project's caption geometry while itself having no burned-in
captions at all — the crop was cutting a real content strip out of every
scene it scanned. See that project's own copy for the full story if reusing
this file again.

RE-DERIVED 2026-09-02 (this project, exosome-label-decode): this project DOES
burn in captions, in a reserved lane at y 1360-1520, so CAPTION_BAND_EXCLUDE is
True here with THIS project's geometry -- and assert_caption_band_matches_source()
now verifies that against index.html on every run rather than leaving it to a
comment. History of the recurring defect this guards, kept verbatim:

RE-DERIVED 2026-09-01 (peeling-question-open): the PREVIOUS
version of this exact file still carried mugwort-healing-herb's caption-band
crop (`CAPTION_BAND_EXCLUDE = True`, y 215-350) despite this project having
NO burned-in captions at all — the on-screen kinetic type IS the only visual
layer, and the sidecar .srt/.vtt is the caption deliverable (see DELIVERY.md).
This is the exact trap the CORRECTED note above already documents happening
one project earlier, and it recurred anyway: the warning lived in a comment
that got copied along with the bug it was warning about, not enforced by the
tool. Confirmed: with the crop on, this script silently excluded scene 5's
"THE BOUNDARY" kicker (which sits inside y 215-350) from every diff it ran.
CAPTION_BAND_EXCLUDE is OFF below. Re-derive per project — check the actual
index.html for a burned-in caption element before ever setting this True
again; do not copy a sibling project's value.

REGION-AWARE CHECK ADDED 2026-09-01, closing a second, independent gap: the
whole-frame-only PSNR check above can read "clean" while a scene's own HERO
element sits dead for over a second, if unrelated motion elsewhere in the
same frame (a second text block, a caption) keeps the whole-frame PSNR below
the frozen threshold. Confirmed on this project's own 06-open.html: the
glass-panel (this scene's single dominant focal point, per the skill's depth-
roles rule) held zero rendered change for ~1.1s while emptied (last word
faded out, lockup not yet arrived) — invisible to the whole-frame check
because the closing h-line couplet, in a different part of the same frame,
kept animating throughout that exact window. A blankness scanner and the
whole-frame PSNR check above are two different tools that happen to sound
alike (see the skill's own note on this); a hero-region-dead-but-frame-alive
scene is a THIRD case neither one catches.

A naive "any cell frozen for N seconds" grid was tried first and rejected: it
flagged 19 findings across this 25s video, almost all of them a small badge
or pill resting statically in a corner after its own one-time entrance, while
the SCENE as a whole kept satisfying cadence via a Ken Burns zoom elsewhere —
a legitimate resting state, not a defect. The failure that actually matters
is narrower: a region that WAS populated with real content and then goes
essentially EMPTY (not merely static) for longer than the ceiling, scoped to
a single scene so a hard cut between scenes never reads as "content
vanished." Scene boundaries are read from this project's own index.html
(`data-start`/`data-duration` on each `.scene[data-composition-src]`), a
convention this HyperFrames project structure guarantees — this script is
project-specific in that sense, matching check-safe-area.py's own
1080x1920-canvas assumption; re-derive the parsing if reusing this file on a
project with a different root-timeline shape (or on one with no index.html
scene list at all, in which case it falls back to treating the whole render
as one scene).

TWO CONFIRMED FALSE-POSITIVE CLASSES, found by re-verifying this script's own
output against the actual fixed render rather than trusting it — the same
"verify by pixels" discipline this skill demands of an external QC report
applies to this script's own claims too:

1. A textured/gradient plate (not a flat color) can cross the active-content
   threshold without being real UI content — confirmed on this project's own
   scene 1, where a frosted-glass card's embossed watermark produced a false
   content-then-empty read even after tuning.
2. A SECOND, weaker content transition in the same scene/cell can still
   register as "empty" if its own ink footprint is smaller than an earlier
   beat's peak in that same cell. Confirmed on 06-open.html AFTER the fix
   below was applied and verified correct by direct frame extraction (the
   panel's true empty window measured 0.40s post-fix, down from 1.30s
   pre-fix — a real, confirmed improvement): the per-scene baseline is a low
   percentile across the WHOLE scene's samples, so a scene with two different
   content states of different ink magnitude (the word-grid's strong peak,
   then the 습/SeoulHabit lockup's weaker one in the same grid column, since
   the glyph sits mostly right of this column's boundary) can end up with a
   baseline sitting between the two, making the WEAKER state's own arrival
   register as still "empty" relative to ACTIVE_DELTA_PX even though it is
   real, settled content. This script did not self-correct after the retime;
   only extracting and eyeballing the actual frames at t=23.0 and t=23.5
   caught that the flagged window was stale. A per-cell, scene-relative
   dynamic threshold (proportional to that cell's own observed range, not a
   single fixed delta) would likely fix this properly; not implemented here.

The grid itself is still a heuristic, not a scene-aware oracle — a cell
straddling a hero element and its background can still under- or over-report
by a few tenths of a second depending on layout, independent of the two
classes above. Treat a flagged cell as a strong candidate to eyeball at the
given timestamp, not as ground truth on its own — the same advisory posture
as the whole-frame check below, and doubly true given the two confirmed
false-positive classes above.

Method: sample at a fixed low fps, optionally crop out a caption band
(top+bottom strips vstacked back together) when one exists, compute PSNR
between consecutive sampled frames for the whole-frame check. A genuinely
frozen region reads as very high PSNR (identical or near-identical pixels);
real motion — even a slow Ken Burns drift — keeps PSNR well below the cutoff.
The region-aware check instead grids the safe content box, tracks each
cell's own ink-pixel count over time, and flags a cell that drops from
"had real content" to "essentially empty" and stays there past the ceiling,
within one scene's boundaries.

Advisory only (exit 0 always), matching check-blank-frames.py's convention —
a held freeze-frame can be a deliberate choice; this surfaces candidates for
a human to confirm, not a hard gate.
"""
import glob
import re
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import numpy as np
    from PIL import Image
except ImportError:
    print("check-static-hold: needs `python3 -m pip install pillow numpy` — skipping.")
    sys.exit(0)

SAMPLE_FPS = 2                  # whole-frame check: coarse is fine, measured in seconds
REGION_FPS = 4                  # region check: finer, matching check-safe-area.py's own
                                 # reasoning -- a short hole can fall between 2fps samples
CANVAS_W, CANVAS_H = 1080, 1920

# RE-DERIVED 2026-09-02 for exosome-label-decode, from THIS project's own
# index.html -- not inherited. The copy this file was made from carried
# peeling-question-open's values (False, y 215-350), which are wrong here:
# this project DOES burn in captions, in a reserved lane at y 1360-1520
# (`.vo-caption { top: 1360px; height: 160px }`). Leaving the inherited value
# would have let a 27-cue caption track register as constant motion and mask a
# frozen scene underneath it.
#
# assert_caption_band_matches_source() below CHECKS these against index.html at
# every run. That check exists because this exact defect has now recurred three
# times in this file's lineage, twice with a comment in the file explicitly
# warning about it -- a comment demonstrably does not stop it, so this fails
# loud instead.
CAPTION_BAND_EXCLUDE = True
CAPTION_BAND_TOP = 1360
CAPTION_BAND_BOTTOM = 1520
PSNR_FROZEN_DB = 55.0           # above this between consecutive samples reads as "no change"
CADENCE_CEILING_S = 2.5         # shorts target: a state change at least every 1.5-3s

# Region-aware hero check. Matches this project's own tokens.css safe-area
# reserves (--safe-top/bottom/right); safe-left is 0 here (not 72) to match
# check-safe-area.py's own convention of scanning the full non-reserved width.
SAFE_TOP, SAFE_BOTTOM, SAFE_RIGHT, SAFE_LEFT = 192, 384, 162, 0
GRID_ROWS, GRID_COLS = 3, 2
INK_THRESHOLD = 28              # matches check-safe-area.py's own ink threshold
ACTIVE_DELTA_PX = 1200           # a frame counts as "has real content" at/above this many
                                  # ink px ABOVE the cell's own per-scene baseline -- set high
                                  # enough to require an unambiguous content peak (a word/
                                  # lockup landing), not the soft few-hundred-px bump a
                                  # gradient or textured plate (e.g. this project's own
                                  # frosted-glass peel-sheet in scene 1) produces at rest
EMPTY_DELTA_PX = 300               # a frame counts as "essentially empty" at/below this many
                                  # ink px above the baseline
BASELINE_PERCENTILE = 20          # per-cell, per-scene baseline: low-percentile ink count,
                                   # not a flat 0 -- a rounded-corner panel/card border
                                   # contributes a constant few-hundred-px "floor" that is
                                   # structural, not content, and differs per cell/scene.
                                   # Confirmed necessary on this project's own 06-open.html:
                                   # the glass-panel's own translucent fill/border produced
                                   # a ~450-870px floor even with zero text on screen, which
                                   # silently defeated a flat EMPTY_INK_PX threshold below
                                   # that floor -- the truly-empty window never registered as
                                   # empty because it never dropped below a threshold the
                                   # panel's own structure already exceeded at rest.
REGION_CADENCE_CEILING_S = 1.0  # tighter than the whole-frame ceiling -- a hero region
                                 # going fully empty is a sharper failure than a frame-wide
                                 # hold, so it gets a tighter allowance


def assert_caption_band_matches_source(project_root):
    """Fail loud if the configured caption band does not match index.html.

    Guards both directions:
      - EXCLUDE=True  but no burned-in caption element exists  -> a real content
        strip is being silently cut out of every diff.
      - EXCLUDE=False but a caption composition DOES exist      -> the caption
        track's own word changes mask a frozen scene underneath.
    """
    idx = project_root / "index.html"
    if not idx.exists():
        return
    src = idx.read_text()
    has_caption_el = 'class="clip vo-caption"' in src or "vo-caption" in src

    if CAPTION_BAND_EXCLUDE and not has_caption_el:
        sys.exit("check-static-hold: CAPTION_BAND_EXCLUDE is True but index.html has no "
                 "burned-in caption element. Re-derive these constants for THIS project.")
    if not CAPTION_BAND_EXCLUDE and has_caption_el:
        sys.exit("check-static-hold: index.html HAS a burned-in caption layer but "
                 "CAPTION_BAND_EXCLUDE is False -- its repainting would mask a frozen "
                 "scene. Re-derive these constants for THIS project.")

    if CAPTION_BAND_EXCLUDE:
        m_top = re.search(r"\.vo-caption\s*\{[^}]*top:\s*(\d+)px", src, re.DOTALL)
        m_h = re.search(r"\.vo-caption\s*\{[^}]*height:\s*(\d+)px", src, re.DOTALL)
        if m_top and m_h:
            top = int(m_top.group(1))
            bottom = top + int(m_h.group(1))
            if top < CAPTION_BAND_TOP or bottom > CAPTION_BAND_BOTTOM:
                sys.exit(f"check-static-hold: index.html renders its caption band at "
                         f"y {top}-{bottom}, which is not covered by the configured "
                         f"crop y {CAPTION_BAND_TOP}-{CAPTION_BAND_BOTTOM}. Re-derive.")
            print(f"  caption band verified against index.html: y {top}-{bottom} "
                  f"(crop {CAPTION_BAND_TOP}-{CAPTION_BAND_BOTTOM})")
        else:
            sys.exit("check-static-hold: could not read .vo-caption top/height from "
                     "index.html to verify the crop. Refusing to trust the constants.")


def most_recent_render(project_root):
    candidates = glob.glob(str(project_root / "renders" / "*.mp4"))
    if not candidates:
        return None
    return Path(max(candidates, key=lambda p: Path(p).stat().st_mtime))


def scene_boundaries(project_root):
    """Read (start, end) tuples from index.html's root-timeline scene list.
    Falls back to a single (0, inf) scene if index.html is missing or has no
    recognizable scene markup — see docstring."""
    index_path = project_root / "index.html"
    if not index_path.exists():
        return None
    text = index_path.read_text(errors="replace")
    pattern = re.compile(
        r'class="[^"]*\bscene\b[^"]*"[^>]*data-composition-src="[^"]+"[^>]*?\s+data-start="([\d.]+)"\s+data-duration="([\d.]+)"'
    )
    scenes = [(float(a), float(a) + float(b)) for a, b in pattern.findall(text)]
    return scenes or None


def psnr(a, b):
    mse = np.mean((a.astype(np.float64) - b.astype(np.float64)) ** 2)
    if mse <= 1e-9:
        return 99.0
    return 10.0 * np.log10((255.0 ** 2) / mse)


def whole_frame_check(render_path):
    if CAPTION_BAND_EXCLUDE:
        print(f"Static-hold scan (whole frame) — {render_path.name}, sampling every "
              f"{1000/SAMPLE_FPS:.0f}ms, caption band ({CAPTION_BAND_TOP}-{CAPTION_BAND_BOTTOM}px) excluded.")
        top_h = CAPTION_BAND_TOP
        bot_h = CANVAS_H - CAPTION_BAND_BOTTOM
        filt = (
            f"[0:v]fps={SAMPLE_FPS},crop={CANVAS_W}:{top_h}:0:0[top];"
            f"[0:v]fps={SAMPLE_FPS},crop={CANVAS_W}:{bot_h}:0:{CAPTION_BAND_BOTTOM}[bot];"
            f"[top][bot]vstack=inputs=2[out]"
        )
    else:
        print(f"Static-hold scan (whole frame) — {render_path.name}, sampling every "
              f"{1000/SAMPLE_FPS:.0f}ms, full frame (no caption band to exclude).")
        filt = f"[0:v]fps={SAMPLE_FPS}[out]"

    with tempfile.TemporaryDirectory() as tmp:
        proc = subprocess.run(
            ["ffmpeg", "-y", "-i", str(render_path), "-filter_complex", filt,
             "-map", "[out]", "-q:v", "4", f"{tmp}/f_%06d.png"],
            capture_output=True, check=False,
        )
        frame_paths = sorted(glob.glob(f"{tmp}/f_*.png"))
        if not frame_paths:
            print("  could not extract frames — skipping.")
            print(proc.stderr.decode(errors="replace")[-800:])
            return []

        arrays = [np.asarray(Image.open(p).convert("L"), dtype=np.uint8) for p in frame_paths]

    findings = []
    run_start = None
    for i in range(1, len(arrays)):
        t = i / SAMPLE_FPS
        p = psnr(arrays[i - 1], arrays[i])
        if p > PSNR_FROZEN_DB:
            if run_start is None:
                run_start = t - (1.0 / SAMPLE_FPS)
        else:
            if run_start is not None:
                duration = t - run_start
                if duration >= CADENCE_CEILING_S:
                    findings.append((run_start, t, duration))
                run_start = None
    if run_start is not None:
        t_end = (len(arrays) - 1) / SAMPLE_FPS
        duration = t_end - run_start
        if duration >= CADENCE_CEILING_S:
            findings.append((run_start, t_end, duration))

    if not findings:
        print(f"  no findings ({len(arrays)} frames sampled, {CADENCE_CEILING_S}s ceiling).")
    else:
        print(f"  {len(findings)} static-hold(s) found, over the {CADENCE_CEILING_S}s cadence ceiling:")
        for start, end, duration in findings:
            print(f"  - t={start:.2f}s to t={end:.2f}s  ({duration:.2f}s frozen, imagery excluding captions)")
    return findings


def region_check(render_path, project_root):
    scenes = scene_boundaries(project_root)
    if scenes:
        print(f"\nStatic-hold scan (region-aware) — {render_path.name}, sampling every "
              f"{1000/REGION_FPS:.0f}ms, {GRID_ROWS}x{GRID_COLS} grid over the safe content box, "
              f"content-then-empty detection, {len(scenes)} scene(s) from index.html.")
    else:
        print(f"\nStatic-hold scan (region-aware) — {render_path.name}, sampling every "
              f"{1000/REGION_FPS:.0f}ms, {GRID_ROWS}x{GRID_COLS} grid over the safe content box, "
              f"content-then-empty detection. No index.html scene list found — treating the "
              f"whole render as one scene (cross-cut false positives are possible).")

    with tempfile.TemporaryDirectory() as tmp:
        proc = subprocess.run(
            ["ffmpeg", "-y", "-i", str(render_path), "-vf", f"fps={REGION_FPS}",
             "-q:v", "4", f"{tmp}/f_%06d.png"],
            capture_output=True, check=False,
        )
        frame_paths = sorted(glob.glob(f"{tmp}/f_*.png"))
        if not frame_paths:
            print("  could not extract frames — skipping.")
            print(proc.stderr.decode(errors="replace")[-800:])
            return []
        y0, y1 = SAFE_TOP, CANVAS_H - SAFE_BOTTOM
        x0, x1 = SAFE_LEFT, CANVAS_W - SAFE_RIGHT
        arrays = [
            np.asarray(Image.open(p).convert("L"), dtype=np.int16)[y0:y1, x0:x1]
            for p in frame_paths
        ]

    n = len(arrays)
    if not scenes:
        scenes = [(0.0, n / REGION_FPS)]

    h, w = arrays[0].shape
    row_h, col_w = h // GRID_ROWS, w // GRID_COLS
    findings = []
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            ry0, ry1 = r * row_h, h if r == GRID_ROWS - 1 else (r + 1) * row_h
            rx0, rx1 = c * col_w, w if c == GRID_COLS - 1 else (c + 1) * col_w
            cell_abs = (y0 + ry0, y0 + ry1, x0 + rx0, x0 + rx1)

            # Per-frame ink-pixel count for this cell, against a per-frame
            # local background (modal luma) so a slow Ken Burns brightness
            # drift doesn't get misread as "content."
            ink_counts = []
            for a in arrays:
                cell = a[ry0:ry1, rx0:rx1]
                vals, counts = np.unique(cell, return_counts=True)
                bg = vals[counts.argmax()]
                ink_counts.append(int((np.abs(cell - bg) > INK_THRESHOLD).sum()))

            for scene_start, scene_end in scenes:
                i0 = max(1, int(scene_start * REGION_FPS))
                i1 = min(n, int(scene_end * REGION_FPS) + 1)
                if i1 <= i0:
                    continue
                # Baseline excludes the window's own first/last sample -- a
                # scene-boundary frame (a hard cut into/out of a differently
                # composed neighbor scene) is a one-frame outlier, not a
                # representative "at rest" reading for THIS scene.
                raw_window = ink_counts[i0 - 1:i1] if i0 >= 1 else ink_counts[0:i1]
                window = raw_window[1:-1] if len(raw_window) > 2 else raw_window
                baseline = float(np.percentile(window, BASELINE_PERCENTILE))

                had_content = False
                empty_start = None
                for i in range(i0, i1):
                    t = i / REGION_FPS
                    delta = ink_counts[i] - baseline
                    if delta >= ACTIVE_DELTA_PX:
                        had_content = True
                        if empty_start is not None:
                            empty_start = None
                    elif had_content and delta <= EMPTY_DELTA_PX:
                        if empty_start is None:
                            empty_start = t - (1.0 / REGION_FPS)
                    # ambiguous zone (between EMPTY_DELTA_PX and ACTIVE_DELTA_PX):
                    # neither resets nor extends a run, avoids flapping on noise
                if empty_start is not None:
                    t_end = (i1 - 1) / REGION_FPS
                    duration = t_end - empty_start
                    if duration >= REGION_CADENCE_CEILING_S:
                        findings.append((empty_start, t_end, duration, cell_abs))

    if not findings:
        print(f"  no findings (content-then-empty, {REGION_CADENCE_CEILING_S}s ceiling).")
    else:
        print(f"  {len(findings)} region-level content-void(s) found:")
        for start, end, duration, (ay0, ay1, ax0, ax1) in findings:
            print(f"  - t={start:.2f}s to t={end:.2f}s  ({duration:.2f}s empty after carrying content) "
                  f"in cell y={ay0}-{ay1} x={ax0}-{ax1}")
        print("  Note: a textured or gradient plate (not a flat color) can still read as a\n"
              "  false content-void here -- the ink signal is spatial-variance-based and a\n"
              "  smooth gradient/watermark can cross the active threshold without being\n"
              "  real UI content. Confirm each by extracting the actual frame, not by\n"
              "  trusting the cell coordinates alone.")
    return findings


def main():
    project_root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    # Verify the caption-band constants against THIS project's index.html before
    # trusting any result from them (see the constants block for why).
    assert_caption_band_matches_source(project_root)
    render_path = sys.argv[2] if len(sys.argv) > 2 else None
    render_path = Path(render_path) if render_path else most_recent_render(project_root)

    if not render_path or not render_path.exists():
        print("check-static-hold: no render found under renders/*.mp4 — skipping.")
        return 0

    whole_findings = whole_frame_check(render_path)
    region_findings = region_check(render_path, project_root)

    if not whole_findings and not region_findings:
        print("\n  Overall: clean (whole-frame and region-aware checks both clean).")
    else:
        print("\n  Verify each: does this scene need a beat, or is it a deliberate hold?")
    return 0


if __name__ == "__main__":
    sys.exit(main())
