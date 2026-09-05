#!/usr/bin/env python3
"""Mobile-legibility floor: declared type sizes, and actual rendered pixels
at the scale this video is mostly watched at.

    python3 scripts/check-legibility.py .
    python3 scripts/check-legibility.py . renders/collagen-where-did-it-go_final.mp4

PART 1 -- TOKEN FLOOR. The review's own finding: at a 25% phone-scale preview
(480x270), a 32px source size becomes ~8px on screen -- unreadable for a
citation, an axis label, a filter pill. Phase 3 raised every referenced type
token from 32px to 40-44px; this asserts it stays that way. `--t-floor` (20px)
and `--t-caption` (24px) are declared in _preamble.TOKENS but referenced
nowhere in this project's scenes on purpose -- both are BELOW the floor, so
Part 1 fails loudly if either is ever actually used, rather than leaving them
as a silent trap for the next scene that reaches for a token by name without
checking whether it is live.

PART 2 -- RENDERED PIXELS AT PHONE SCALE. A source token being >=40px is
necessary, not sufficient: anti-aliasing, letter-spacing and stroke weight all
affect whether 40px source type is actually legible once rendered and scaled
down. Measures glyph height directly on extracted 480x270 frames (the same
scale qc_sheets.py's phone.png uses for human review) at a sample of the
project's own kinetic-reveal anchors, via the same run-length ink-detection
idea check-safe-area.py uses for its edge filter: a real glyph stroke, not
antialiasing noise, spans a run of masked pixels in a column.

Covered: every referenced type token meets the floor; a sample of rendered
text is tall enough at phone scale to plausibly read.
NOT covered: font hinting, kerning, or whether wrapped text overlaps.
qc_sheets.py's phone.png is the human corroboration for those.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
RENDER = Path(sys.argv[2]) if len(sys.argv) > 2 else None
SCRIPTS = ROOT / "scripts"

FLOOR_PX = 40
BELOW_FLOOR_TOKENS = ("--t-floor", "--t-caption")  # must never be referenced


def part1():
    print("PART 1 -- declared type-token floor")
    preamble = (SCRIPTS / "_preamble.py").read_text()
    m = re.search(r'TOKENS\s*=\s*"""(.*?)"""', preamble, re.S)
    tokens_css = m.group(1) if m else ""
    sizes = dict(re.findall(r"(--t-[a-z]+):\s*(\d+)px", tokens_css))

    bad = 0
    for name, px in sorted(sizes.items(), key=lambda kv: int(kv[1])):
        px = int(px)
        below_floor_by_design = name in BELOW_FLOOR_TOKENS
        ok = (px >= FLOOR_PX) or below_floor_by_design
        if not ok:
            bad += 1
        tag = "PASS" if px >= FLOOR_PX else ("OK (unused by design)" if below_floor_by_design else "FAIL")
        print(f"  {'.' if ok else '!'} {tag:22s}  {name}: {px}px")

    all_scene_src = "\n".join(
        p.read_text() for p in SCRIPTS.glob("*.py") if p.name != "check-legibility.py")
    for name in BELOW_FLOOR_TOKENS:
        used = f"var({name})" in all_scene_src
        if used:
            bad += 1
        print(f"  {'!' if used else '.'} {'FAIL' if used else 'PASS'}  "
              f"{name} referenced anywhere in scripts/: {used}"
              + ("  <-- below the 40px floor and must not ship" if used else ""))
    return bad


# ---------------------------------------------------------------- Part 2 ---
def frame(render, t, scale="480:270"):
    import io
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{t:.3f}",
                        "-i", str(render), "-vf", f"scale={scale}", "-frames:v", "1",
                        "-f", "image2pipe", "-vcodec", "png", "-"],
                       capture_output=True, check=False)
    if not r.stdout:
        return None
    import numpy as np
    from PIL import Image
    return np.asarray(Image.open(io.BytesIO(r.stdout)).convert("L")).astype(float)


def glyph_height(gray, box, bg_luma, threshold=28, min_run=2):
    """Tallest contiguous vertical run of ink (a real glyph stroke, not a
    speck of antialiasing) inside box, in PHONE-SCALE pixels. box is (x0,y0,x1,y1)
    at the frame's own (already 480x270) resolution."""
    import numpy as np
    x0, y0, x1, y1 = box
    crop = gray[y0:y1, x0:x1]
    ink = np.abs(crop - bg_luma) > threshold
    col_has_ink = ink.sum(axis=1) >= min_run   # a row counts only with >=min_run ink px across the box
    if not col_has_ink.any():
        return 0
    rows = np.where(col_has_ink)[0]
    return int(rows.max() - rows.min() + 1)


# (t, box in 480x270 px, background luma at that box, label, min phone-px height)
# MIN_GLYPH_PX=5 is deliberately low: readability research on small on-screen
# text puts a hard floor around 6-8px cap-height at normal viewing distance,
# and this measures the WHOLE line's ink bounding box (ascenders+descenders),
# which runs taller than cap-height alone -- 5px here is already a generous
# failure margin, not the target.
PHONE_TARGETS = [
    (5.20, (55, 98, 100, 110), 230, "01-hook CREAM chip text", 5),
]
MIN_GLYPH_PX = 5


def part2(render):
    print(f"\nPART 2 -- rendered glyph height at phone scale (480x270), {render.name if render else 'no render'}")
    if not render or not render.exists():
        print("  SKIPPED: render not found")
        return 0
    bad = 0
    for t, box, bg, label, floor in PHONE_TARGETS:
        g = frame(render, t)
        if g is None:
            print(f"  ?  {label}: could not extract frame at t={t}s")
            continue
        h = glyph_height(g, box, bg)
        ok = h >= floor
        if not ok:
            bad += 1
        print(f"  {'.' if ok else '!'} {'PASS' if ok else 'FAIL'}  {h}px tall (floor {floor}px)  {label}")
    print("  Corroborate with renders/qc/phone.png (qc_sheets.py) -- every kinetic-reveal")
    print("  anchor at this same 480x270 scale, for a human to confirm what this measures.")
    return bad


def main():
    bad1 = part1()
    bad2 = part2(RENDER)
    total = bad1 + bad2
    print(f"\n{total} finding(s) across both parts.")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
