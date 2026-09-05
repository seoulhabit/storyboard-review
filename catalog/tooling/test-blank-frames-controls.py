#!/usr/bin/env python3
"""Self-contained controls for check-blank-frames.py (beside this file).

Run after any change to its stddev cutoff, its sampling rate, or its
run-length grouping:

    python3 catalog/tooling/test-blank-frames-controls.py

Every fixture is a synthetic MP4 built here and driven through the gate's own
CLI, so what is tested is the shipping path end to end -- frame extraction,
luma measurement, run grouping and the printed verdict -- not a re-implemented
copy of any of it.

  FIXTURE VALIDITY  before asserting anything about the gate, the fixture's own
                    frames are extracted and measured. A control built on a
                    fixture nobody measured is worthless: the motion-gaps gate
                    in this same directory was made to look broken by a fixture
                    whose block was three times the size its author assumed, and
                    an earlier version of that fixture drew nothing at all. So
                    this asserts the blank frames really do read near zero and
                    the content frames really do read far above the cutoff, and
                    says plainly that a failure here is the FIXTURE's fault.

  DETECTION         a 5-frame (333ms) flat stretch in the middle of a busy
                    timeline MUST be reported, with its start and duration.

  DURATION FLOOR    a 1-frame (67ms) flat stretch in the same render MUST NOT
                    be reported -- below MIN_FLAG_DURATION_S. Both live in the
                    SAME fixture, so a gate that flagged everything and a gate
                    that flagged nothing would each fail one half. A one-sided
                    control cannot tell those two apart.

  CLEAN RENDER      a render with no flat stretch at all MUST report no
                    findings -- the control that catches a gate flagging
                    ordinary content.

  FRAME ZERO        a render that opens flat MUST be reported AND tagged as
                    including frame zero. That tag exists because a blank
                    poster/load frame is its own defect class, and a gate that
                    found the run but lost the tag would still read as passing.

  TRAILING RUN      a render that ENDS flat MUST be reported. The grouping loop
                    closes an open run after the last frame in a separate
                    branch from the one that closes a run mid-timeline, and an
                    unclosed final run is the shape of a defect that silently
                    disappears exactly where a video is most likely to have one.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import numpy as np
    from PIL import Image
except ImportError:
    print("test-blank-frames-controls: needs `python3 -m pip install pillow numpy` -- "
          "skipping (exit 0).")
    sys.exit(0)

TOOL = Path(__file__).resolve().parent / "check-blank-frames.py"

FPS = 15          # the gate's own sample rate; building at it keeps frames 1:1
W, H = 320, 180
BLANK_LUMA = 18   # a flat near-black ground: stddev 0, like a real empty stage


def content_frame(i):
    """A busy frame: high-contrast blocks whose position varies with i, so no
    two content frames are identical and none of them is flat."""
    a = np.full((H, W), BLANK_LUMA, dtype=np.uint8)
    off = (i * 7) % 60
    a[30:90, 20 + off:120 + off] = 240
    a[110:150, 60:280] = 200
    a[20:40, 200:300] = 255
    return a


def blank_frame():
    return np.full((H, W), BLANK_LUMA, dtype=np.uint8)


def build(path, flat_indices, n_frames):
    """Render n_frames to an MP4 at FPS, with the named indices flat.

    -qp 0 (lossless) matters: at an ordinary CRF, x264 smears a hard-edged
    content frame enough to move its stddev, and a control whose fixture drifts
    with the encoder setting is not measuring the gate.
    """
    with tempfile.TemporaryDirectory() as d:
        for i in range(n_frames):
            arr = blank_frame() if i in flat_indices else content_frame(i)
            Image.fromarray(arr).convert("RGB").save(f"{d}/f_{i:05d}.png")
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS),
             "-i", f"{d}/f_%05d.png", "-c:v", "libx264", "-qp", "0",
             "-pix_fmt", "yuv420p", str(path)],
            check=True, capture_output=True)


def measure(path):
    """Extract at the gate's own sample rate and return per-frame stddev."""
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(path),
                        "-vf", f"fps={FPS}", "-q:v", "4", f"{d}/f_%06d.png"],
                       check=True, capture_output=True)
        return [float(np.asarray(Image.open(p).convert("L"), dtype=np.float32).std())
                for p in sorted(Path(d).glob("f_*.png"))]


def run_gate(render):
    r = subprocess.run([sys.executable, str(TOOL), str(render.parent.parent), str(render)],
                       capture_output=True, text=True, check=False)
    spans = [(float(a), float(b)) for a, b in
             re.findall(r"t=([0-9.]+)s to t=([0-9.]+)s", r.stdout)]
    return r.stdout, spans


def project(tmp, name):
    """The gate takes <project_root> <render>; give it a plausible one."""
    p = Path(tmp) / name / "renders"
    p.mkdir(parents=True)
    return p / "test.mp4"


def main():
    if not TOOL.exists():
        print(f"test-blank-frames-controls: {TOOL.name} not found beside this fixture -- "
              f"skipping (exit 0).")
        return 0
    import importlib.util
    spec = importlib.util.spec_from_file_location("check_blank_frames", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    ok = True

    with tempfile.TemporaryDirectory() as tmp:
        # 30 frames @ 15fps = 2.0s. Frames 7-11 flat (5 frames, 333ms -> must
        # flag); frame 26 flat alone (67ms -> must not).
        main_render = project(tmp, "main")
        build(main_render, set(range(7, 12)) | {26}, 30)

        print("\n  FIXTURE VALIDITY -- the fixture's own frames, measured before "
              "anything is asserted:")
        sd = measure(main_render)
        flat = [sd[i] for i in list(range(7, 12)) + [26] if i < len(sd)]
        busy = [sd[i] for i in range(len(sd)) if i not in set(range(7, 12)) | {26}]
        good = (len(sd) == 30 and max(flat) < 6.0 and min(busy) > 25.0
                and max(flat) < mod.STDDEV_CUTOFF < min(busy))
        ok &= good
        print(f"    {len(sd)} frames sampled   flat: max stddev {max(flat):.2f}   "
              f"busy: min stddev {min(busy):.2f}   cutoff {mod.STDDEV_CUTOFF}")
        print("    PASS" if good else
              "    FAIL <-- THE FIXTURE is wrong, not the gate: its frames are not in "
              "the regime it claims")

        print("\n  DETECTION + DURATION FLOOR -- a 333ms flat run and a 67ms one, same render:")
        out, spans = run_gate(main_render)
        # the 333ms run covers frames 7-11: starts 7/15=0.467s, ends 12/15=0.800s
        found_long = any(abs(a - 7 / FPS) < 0.02 and abs(b - 12 / FPS) < 0.02 for a, b in spans)
        found_short = any(abs(a - 26 / FPS) < 0.02 for a, b in spans)
        good = found_long and not found_short and len(spans) == 1
        ok &= good
        print(f"    reported spans: {[(round(a, 3), round(b, 3)) for a, b in spans]}")
        print(f"    333ms run reported: {found_long} (must be True)   67ms run reported: "
              f"{found_short} (must be False)")
        print(f"    {'PASS' if good else 'FAIL <-- detection or the MIN_FLAG_DURATION_S floor is broken'}")

        print("\n  CLEAN RENDER -- no flat stretch anywhere:")
        clean = project(tmp, "clean")
        build(clean, set(), 30)
        out, spans = run_gate(clean)
        good = not spans and "no findings" in out
        ok &= good
        print(f"    reported spans: {spans} (must be empty)   "
              f"{'PASS' if good else 'FAIL <-- ordinary content is being flagged as blank'}")

        print("\n  FRAME ZERO -- a render that opens flat must be reported AND tagged:")
        zero = project(tmp, "zero")
        build(zero, {0, 1, 2, 3}, 30)
        out, spans = run_gate(zero)
        starts_at_zero = any(a <= 0.01 for a, b in spans)
        tagged = "includes frame zero" in out
        good = starts_at_zero and tagged
        ok &= good
        print(f"    span starts at 0.00s: {starts_at_zero}   poster-frame tag present: {tagged}   "
              f"{'PASS' if good else 'FAIL <-- the frame-zero case is lost or untagged'}")

        print("\n  TRAILING RUN -- a render that ENDS flat must still be reported:")
        tail = project(tmp, "tail")
        build(tail, set(range(24, 30)), 30)
        out, spans = run_gate(tail)
        good = any(abs(a - 24 / FPS) < 0.02 for a, b in spans)
        ok &= good
        print(f"    reported spans: {[(round(a, 3), round(b, 3)) for a, b in spans]}   "
              f"{'PASS' if good else 'FAIL <-- a run left open at the last frame is being dropped'}")

    print("\n  All controls behave as expected.\n" if ok else
          "\n  A CONTROL FAILED -- do not trust this gate until it is resolved.\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
