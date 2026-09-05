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

RE-DERIVED 2026-09-01 (this project, peeling-question-open): the PREVIOUS
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
import math
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
CANVAS_W, CANVAS_H = 1080, 1920   # portrait default; --landscape rebinds these

CAPTION_BAND_EXCLUDE = False    # RE-DERIVED for collagen-where-did-it-go -- the on-screen
                                 # kinetic type IS the content, not a caption overlay on
                                 # top of it. See docstring: re-derive per project, do not
                                 # copy a sibling's value or trust an old comment here.
CAPTION_BAND_TOP = 215
CAPTION_BAND_BOTTOM = 350


def _assert_caption_band_is_this_projects(project_root):
    """Fail loud rather than trust an inherited constant.

    This exact constant has been wrong-by-inheritance FOUR times in this file's
    lineage (peeling-not-progress carried another project's 960-1110;
    peeling-question-open carried mugwort-healing-herb's 215-350; the catalog
    copy still carries a docstring naming peeling-question-double as "this
    project"). Three of those copies already contained a comment warning about
    it. A comment demonstrably does not stop this, so check instead of
    documenting: does a burned-in caption composition actually exist here?
    """
    import re, sys
    idx = Path(project_root) / "index.html"
    html = idx.read_text() if idx.exists() else ""
    frames = sorted((Path(project_root) / "compositions" / "frames").glob("*.html"))
    blob = html + "".join(f.read_text() for f in frames)
    # a real burned-in caption track registers a composition or a class for it
    has_captions = bool(re.search(r'data-composition-id="captions"'
                                  r'|class="[^"]*caption-(group|word|pill)'
                                  r'|compositions/captions\.html', blob))
    if has_captions and not CAPTION_BAND_EXCLUDE:
        print("WARNING: a burned-in caption element exists but "
              "CAPTION_BAND_EXCLUDE is False -- the caption track's own word "
              "changes will mask a frozen scene underneath it.", file=sys.stderr)
    if CAPTION_BAND_EXCLUDE and not has_captions:
        print("FATAL: CAPTION_BAND_EXCLUDE is True but no burned-in caption "
              f"element exists in {project_root}. This constant was inherited "
              "from another project and would silently exclude real content "
              "from every diff. Re-derive it.", file=sys.stderr)
        sys.exit(2)
    return has_captions
PSNR_FROZEN_DB = 55.0           # above this between consecutive samples reads as "no change"
CADENCE_CEILING_S = 2.5         # shorts target: a state change at least every 1.5-3s.
                                 # --landscape raises this to 10.0: the skill's long-form
                                 # cadence budget is 8-12s, and holding a Shorts ceiling
                                 # against a multi-minute piece reports a finding on every
                                 # normal long-form beat. Note this is a CRAFT BUDGET, not
                                 # a measured threshold -- channel-baseline-analysis §7
                                 # lists both cadence numbers as unbacked by channel data.

# Region-aware hero check. Matches this project's own tokens.css safe-area
# reserves (--safe-top/bottom/right); safe-left is 0 here (not 72) to match
# check-safe-area.py's own convention of scanning the full non-reserved width.
SAFE_TOP, SAFE_BOTTOM, SAFE_RIGHT, SAFE_LEFT = 192, 384, 162, 0
GRID_ROWS, GRID_COLS = 3, 2
INK_THRESHOLD = 28              # matches check-safe-area.py's own ink threshold
EDGE_THRESHOLD = 40             # |gradient| above this counts as a structural edge
EDGE_EMPTY_FRACTION = 0.25      # a cell is only "empty" if its edge density has also
                                 # fallen to <=25% of the scene's own 90th-percentile
                                 # peak -- see the alpha-swing note in region_check
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


def apply_landscape_profile():
    """Rebind the portrait constants above for a 1920x1080 long-form render.

    Derivations, so a future reader can check rather than trust:
      * canvas 1920x1080; reserved zones top 54 / bottom 108 / left 96 / right 96
        (5% edges, 10% bottom for the player progress bar + controls). There is no
        Shorts action rail in 16:9, so 162px on the right is semantically wrong here.
      * grid transposed 3x2 -> 2x3: a wide frame's cells should be wide, not tall.
      * ACTIVE/EMPTY_DELTA_PX are ABSOLUTE ink-pixel counts, so they scale with cell
        area. Portrait safe box (1080-162) x (1920-192-384) = 918 x 1344 = 1,233,792px
        over 6 cells = 205,632 px/cell, and ACTIVE_DELTA_PX 1200 = 0.583% of a cell.
        Landscape safe box (1920-96-96) x (1080-54-108) = 1728 x 918 = 1,586,304px over
        6 cells = 264,384 px/cell. Holding the same 0.583%: ACTIVE 1542, EMPTY 386.
    """
    global CANVAS_W, CANVAS_H, CADENCE_CEILING_S
    global SAFE_TOP, SAFE_BOTTOM, SAFE_RIGHT, SAFE_LEFT
    global GRID_ROWS, GRID_COLS, ACTIVE_DELTA_PX, EMPTY_DELTA_PX
    CANVAS_W, CANVAS_H = 1920, 1080
    CADENCE_CEILING_S = 10.0
    SAFE_TOP, SAFE_BOTTOM, SAFE_RIGHT, SAFE_LEFT = 54, 108, 96, 96
    GRID_ROWS, GRID_COLS = 2, 3
    ACTIVE_DELTA_PX, EMPTY_DELTA_PX = 1542, 386


def render_dimensions(render_path):
    """(width, height) of the render via ffprobe, or None if it cannot be determined."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", str(render_path)],
            capture_output=True, check=False, timeout=30,
        ).stdout.decode(errors="replace").strip()
        w, h = out.split("x")[:2]
        return int(w), int(h)
    except Exception:  # noqa: BLE001 - any ffprobe/parse failure means "canvas unknown"
        return None


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

    # Attribute-ORDER-INDEPENDENT. The previous single regex required the literal order
    # src -> data-start -> data-duration, so it silently found nothing on the canonical
    # markup this repo actually ships -- `videos/pilling-vs-peeling/index.html` writes
    # data-start/data-duration BEFORE data-composition-src, and the region check quietly
    # degraded to "whole render as one scene", the exact mode whose own warning text says
    # cross-cut false positives are possible. Matching the tag first and pulling each
    # attribute out of it separately removes the ordering assumption entirely.
    tag_re = re.compile(r"<div\b[^>]*\bclass=\"[^\"]*\bscene\b[^\"]*\"[^>]*>")
    src_re = re.compile(r'data-composition-src="[^"]+"')
    start_re = re.compile(r'data-start="([\d.]+)"')
    dur_re = re.compile(r'data-duration="([\d.]+)"')

    scenes = []
    for tag in tag_re.findall(text):
        if not src_re.search(tag):
            continue
        m_start, m_dur = start_re.search(tag), dur_re.search(tag)
        if not (m_start and m_dur):
            continue
        start, dur = float(m_start.group(1)), float(m_dur.group(1))
        scenes.append((start, start + dur))
    return sorted(scenes) or None


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
            # Alongside it, an EDGE-DENSITY count. Ink alone is the wrong primitive
            # for an element whose ALPHA is animated: a card at background
            # rgba(...,0.06) sits below INK_THRESHOLD and the same card at 0.18
            # sits above it, so a legitimate highlight-then-release cycle makes the
            # whole card's area enter and leave the ink mask while the element is
            # fully present the entire time. Measured on a synthetic card:
            #
            #   a=0.06 (rest)        ink  26,576   edges 6,116
            #   a=0.18 (highlighted) ink 111,044   edges 6,116     <- 4.2x ink swing
            #   genuinely removed    ink       0   edges     0
            #
            # Borders and glyph strokes survive an alpha change, so edge density
            # barely moves; only real removal collapses BOTH. Requiring both to be
            # low for "empty" survives every dim/highlight/focus-pull cycle, which
            # a single ink threshold (or any hysteresis on one) cannot.
            ink_counts, edge_counts = [], []
            for a in arrays:
                cell = a[ry0:ry1, rx0:rx1]
                vals, counts = np.unique(cell, return_counts=True)
                bg = vals[counts.argmax()]
                ink_counts.append(int((np.abs(cell - bg) > INK_THRESHOLD).sum()))
                f = cell.astype(np.int16)
                gy = np.abs(np.diff(f, axis=0))[:, :-1]
                gx = np.abs(np.diff(f, axis=1))[:-1, :]
                edge_counts.append(int(((gx + gy) > EDGE_THRESHOLD).sum()))

            for scene_start, scene_end in scenes:
                # ceil, NOT int, on BOTH bounds -- half-open [start, end) frame
                # semantics, so a window contains only frames whose timestamp
                # actually falls inside the scene.
                #
                # int() truncates, which opened each window one sample EARLY
                # whenever a scene start did not land exactly on the 1/REGION_FPS
                # grid. That leading frame still shows the PREVIOUS scene, so it
                # flipped had_content True and the next scene's legitimately-empty
                # cell then read as "content, then empty" -- a false positive
                # manufactured at almost every hard cut. Measured across this
                # repo: 711 of 936 data-start values (76%) are off the 4fps grid,
                # so this fired on roughly three boundaries in four. Confirmed on
                # videos/pilling-vs-peeling scene 06 (starts 13.200s): int() gave
                # i0=52 = t=13.00s, which is still scene 05 and carried 27.1% ink.
                i0 = max(1, math.ceil(scene_start * REGION_FPS))
                i1 = min(n, math.ceil(scene_end * REGION_FPS))
                if i1 <= i0:
                    continue
                # Baseline excludes the window's own first/last sample -- a
                # scene-boundary frame (a hard cut into/out of a differently
                # composed neighbor scene) is a one-frame outlier, not a
                # representative "at rest" reading for THIS scene.
                raw_window = ink_counts[i0 - 1:i1] if i0 >= 1 else ink_counts[0:i1]
                window = raw_window[1:-1] if len(raw_window) > 2 else raw_window
                baseline = float(np.percentile(window, BASELINE_PERCENTILE))
                raw_e = edge_counts[i0 - 1:i1] if i0 >= 1 else edge_counts[0:i1]
                e_win = raw_e[1:-1] if len(raw_e) > 2 else raw_e
                e_peak = float(np.percentile(e_win, 90))

                had_content = False
                empty_start = None
                for i in range(i0, i1):
                    t = i / REGION_FPS
                    delta = ink_counts[i] - baseline
                    if delta >= ACTIVE_DELTA_PX:
                        had_content = True
                        if empty_start is not None:
                            empty_start = None
                    elif had_content and delta <= EMPTY_DELTA_PX and \
                            edge_counts[i] <= e_peak * EDGE_EMPTY_FRACTION:
                        # BOTH signals must collapse. Ink alone flags a card that
                        # merely dimmed; structure (borders, glyph strokes) persists
                        # unless the content actually left.
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


def _flags(argv):
    """--ceiling <s>, --exempt-last, --exempt-window <start>-<end> (repeatable)
    and --gate, stripped from argv.

    These were passed by package.json and SILENTLY IGNORED: the old filter kept
    only the profile flag, so `--ceiling` landed in argv[0] and became the
    project root while the ceiling stayed at its profile default. A gate that
    is handed a stricter number and quietly uses a looser one is worse than no
    gate, because its PASS line names the number it was given.

    --exempt-window is --exempt-last generalised: a named, reviewed window is
    a design decision (Animation item 11 in this project's review: "allows
    intentional comprehension holds and rejects only unmotivated dead time"),
    not evidence the checker should keep re-discovering. Unlike --exempt-last
    it is NOT open-ended -- pass the exact window a finding actually measured,
    so a genuine regression that grows past it still gates."""
    out, ceiling, exempt_last, gate, exempt_windows = [], None, False, False, []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--ceiling":
            ceiling = float(argv[i + 1]); i += 2; continue
        if a == "--exempt-last":
            exempt_last = True; i += 1; continue
        if a == "--exempt-window":
            lo, hi = argv[i + 1].split("-")
            exempt_windows.append((float(lo), float(hi))); i += 2; continue
        if a == "--gate":
            gate = True; i += 1; continue
        out.append(a); i += 1
    return out, ceiling, exempt_last, gate, exempt_windows


def main():
    global CADENCE_CEILING_S
    argv = [a for a in sys.argv[1:] if a != "--landscape"]
    if "--landscape" in sys.argv:
        apply_landscape_profile()
    argv, ceiling, exempt_last, gate, exempt_windows = _flags(argv)
    if ceiling is not None:
        CADENCE_CEILING_S = ceiling   # AFTER apply_landscape_profile(), which resets it

    project_root = Path(argv[0] if len(argv) > 0 else ".").resolve()
    _assert_caption_band_is_this_projects(project_root)
    render_path = argv[1] if len(argv) > 1 else None
    render_path = Path(render_path) if render_path else most_recent_render(project_root)

    if not render_path or not render_path.exists():
        print("check-static-hold: no render found under renders/*.mp4 — skipping.")
        return 0

    # Loud canvas assert. This check is advisory (exits 0) by convention, but a canvas
    # mismatch is not an advisory condition: every crop and cell index below is computed
    # against CANVAS_W/CANVAS_H, so a mismatch silently measures the wrong regions --
    # the same class of defect check-safe-area.py's own docstring records in detail.
    real = render_dimensions(render_path)
    if real and real != (CANVAS_W, CANVAS_H):
        print(f"check-static-hold: CANVAS MISMATCH — {render_path.name} is "
              f"{real[0]}x{real[1]} but the constants are set for {CANVAS_W}x{CANVAS_H}.")
        print("  Refusing to run: crop rects and grid cells would address the wrong "
              "regions, reporting findings that are not real and missing ones that are.")
        print("  Fix: pass --landscape for a 1920x1080 render, or re-derive the "
              "constants for this canvas (see apply_landscape_profile's docstring).")
        return 2

    whole_findings = whole_frame_check(render_path)
    if exempt_last and whole_findings:
        # the wordless end card is a deliberate calm hold, not a stall
        scenes = scene_boundaries(project_root)
        if scenes:
            last_start = scenes[-1][0]   # scene_boundaries yields (start, end)
            dropped = [f for f in whole_findings if f[0] >= last_start - 0.01]
            whole_findings = [f for f in whole_findings if f[0] < last_start - 0.01]
            if dropped:
                print(f"  --exempt-last: {len(dropped)} finding(s) inside the closing "
                      f"scene (from {last_start:.2f}s) treated as the authored end-card hold")
    if exempt_windows and whole_findings:
        def _covered(f):
            t0, t1 = f[0], f[1]
            return any(lo - 0.05 <= t0 and t1 <= hi + 0.05 for lo, hi in exempt_windows)
        dropped = [f for f in whole_findings if _covered(f)]
        whole_findings = [f for f in whole_findings if not _covered(f)]
        if dropped:
            for lo, hi in exempt_windows:
                print(f"  --exempt-window {lo:.2f}-{hi:.2f}s: reviewed, intentional hold")
            print(f"  {len(dropped)} finding(s) fell fully inside a reviewed window and were dropped")
    region_findings = region_check(render_path, project_root)

    # Scope the summary to what was actually TESTED. "Overall: clean" reads as a
    # verdict on the render, and it is not: a region that is frozen while still
    # CARRYING content is invisible to both passes -- the whole-frame diff stays
    # alive on any other moving element, and the region pass only looks for
    # content-then-EMPTY, which never happens. Confirmed on a synthetic with a
    # populated left region frozen for all 12s beside an animating right region:
    # both passes reported no findings and the old line printed "Overall: clean".
    # An honest scope line is what stops that shipping under a clean banner.
    print("\n  Covered: near-blank frames, frozen whole frames, and regions that "
          "carry content\n  and then go empty.")
    print("  NOT covered: a region that stays FROZEN while still carrying content. "
          "Neither\n  pass can see it -- verify a suspect scene by extracting its "
          "own frames and\n  diffing them, not by trusting this summary.")
    if not whole_findings and not region_findings:
        print("\n  Result: no findings in the two checks above.")
    else:
        print("\n  Verify each: does this scene need a beat, or is it a deliberate hold?")
    # --gate fails on WHOLE-FRAME findings only. The region pass has two
    # documented false-positive classes in this project (the end-screen reserve
    # is REQUIRED to be clear, and 06-door's negative space), so gating on it
    # would fail the build for the design working.
    return 1 if (whole_findings and gate) else 0


if __name__ == "__main__":
    sys.exit(main())
