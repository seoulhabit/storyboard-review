#!/usr/bin/env python3
"""Mobile-legibility floor: declared type sizes, and actual rendered pixels at
the scale the video is mostly watched at.

WHY THIS EXISTS. Type that is comfortable in a 1920x1080 editing window is not
the type the audience sees. At a 25% phone-scale preview (480x270), a 32px
source size becomes ~8px on screen -- unreadable for a citation, an axis label,
a filter pill. `videos/collagen-where-did-it-go`'s own review found exactly
that, and raised every referenced type token from 32px to 40-44px; this gate
is what stops it drifting back.

TWO PARTS, TWO INDEPENDENT MECHANISMS, and the second exists because the first
is necessary but NOT sufficient.

PART 1 -- TOKEN FLOOR, from source. Every `--t-*` size declared in the
project's token block must clear --floor-px. Separately, a token may be
declared BELOW the floor and named with --below-floor-token: that says "this
one exists but must never actually be referenced", and Part 1 fails loudly if
it ever is, rather than leaving it as a silent trap for the next scene that
reaches for a token by name without checking whether it is live.

  That list is a FLAG WITH NO DEFAULT ON PURPOSE. It is project vocabulary,
  not a channel constant: `--t-caption` is forbidden in
  collagen-where-did-it-go and referenced 12 times in
  ectoin-survival-molecule, where it is a legitimate 30px caption size. A
  default here would be wrong for one of those two projects whichever way it
  was set.

PART 2 -- RENDERED PIXELS AT PHONE SCALE. A source token being >=40px is
necessary, not sufficient: anti-aliasing, letter-spacing and stroke weight all
affect whether 40px source type is actually legible once rendered and scaled
down. This measures glyph height directly on extracted phone-scale frames (the
same scale a project's own phone.png QC sheet uses for human review), via the
same run-length ink-detection idea check-safe-area.py uses for its edge filter:
a real glyph stroke, not antialiasing noise, spans a run of masked pixels.

FIELD CONTRACT
    python3 check-legibility.py --tokens <path> [--floor-px 40]
                                [--below-floor-token t-floor ...]
                                [--source-glob 'scripts/*.py' ...]
                                [--project-root <dir>]
                                [--render <render.mp4> --probes <probes.json>]
                                [--scene-map <scenes.json>]
                                [--phone-scale 480x270] [--min-glyph-px 5]
                                [--advisory]

--tokens is any file carrying the declarations. If it contains a
`TOKENS = \"\"\"...\"\"\"` block (this channel's `scripts/_preamble.py`
convention) only that block is read; otherwise the whole file is scanned, so a
plain `assets/tokens/tokens.css` works unchanged.

--below-floor-token takes the token name WITHOUT its leading dashes
(`--below-floor-token t-floor`): argparse reads a value starting with `-` as
another flag, so the natural-looking `--below-floor-token --t-floor` fails with
"expected one argument". The `=` form (`--below-floor-token=--t-floor`) also
works; both are normalised to the same name.

--source-glob (repeatable, relative to --project-root) is where the "is this
token referenced" scan looks. Default `scripts/*.py`.

probes.json is a list of probe objects, timed the same two ways
check-contrast-pixels.py uses, and for the same reason -- an absolute second is
correct for exactly one cut, and a probe table pinned to wall-clock silently
samples the wrong scene the first time anything upstream changes length:

    {"cid": "01-hook", "offset": 1.2, "box": [55, 98, 100, 110],
     "bg": 230, "label": "01-hook CREAM chip text", "floor": 5}

    {"t": 5.20, "box": [55, 98, 100, 110], "bg": 230, "label": "...", "floor": 5}

`box` is [x0, y0, x1, y1] in PHONE-SCALE pixels (--phone-scale, default
480x270), not the render's own. `bg` is the background luma at that box.
`floor` is the minimum ink height in phone-scale pixels, defaulting to
--min-glyph-px.

WHY THE DEFAULT FLOOR IS ONLY 5px. Readability research puts a hard floor
around 6-8px cap-height at normal viewing distance, and this measures the WHOLE
line's ink bounding box (ascenders+descenders), which runs taller than
cap-height alone. 5px is already a generous failure margin, not the target.

Covered: every referenced type token meets the floor; a sample of rendered text
is tall enough at phone scale to plausibly read.
NOT covered: font hinting, kerning, or whether wrapped text overlaps. A
project's own phone.png QC sheet is the human corroboration for those.

Exits non-zero on any finding unless --advisory. A missing --render skips Part
2 (reported, not silently); a probe whose frame cannot be extracted is a
finding, not a skip.

Provenance: `videos/collagen-where-did-it-go` (both parts, and the 25%-scale
finding that motivated them); the cid+offset probe schema and the
attribute-order-safe scene-start parser come from
catalog/tooling/check-contrast-pixels.py.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

FLOOR_PX = 40
MIN_GLYPH_PX = 5
PHONE_SCALE = "480x270"


# ---------------------------------------------------------------- Part 1 ---
def token_sizes(text):
    """{token_name: px} from a token block or stylesheet.

    Exposed so a control fixture tests THIS parser rather than re-implementing
    the regex beside it -- a fixture that re-implements the thing it is
    checking cannot detect the bug it claims to.
    """
    m = re.search(r'TOKENS\s*=\s*"""(.*?)"""', text, re.DOTALL)
    block = m.group(1) if m else text
    return {name: int(px) for name, px in re.findall(r"(--t-[a-z-]+):\s*(\d+)px", block)}


def part1(tokens_path, floor_px, below_floor, source_globs, root):
    print(f"PART 1 -- declared type-token floor ({tokens_path})")
    sizes = token_sizes(Path(tokens_path).read_text())
    if not sizes:
        print(f"  !  FAIL  no --t-* sizes found in {tokens_path} -- wrong file, or the "
              f"declaration form changed")
        return 1

    bad = 0
    for name, px in sorted(sizes.items(), key=lambda kv: kv[1]):
        below_floor_by_design = name in below_floor
        ok = (px >= floor_px) or below_floor_by_design
        if not ok:
            bad += 1
        tag = "PASS" if px >= floor_px else (
            "OK (unused by design)" if below_floor_by_design else "FAIL")
        print(f"  {'.' if ok else '!'} {tag:22s}  {name}: {px}px")

    if not below_floor:
        return bad

    files = []
    for g in source_globs:
        # Never scan this gate's own file: it names the forbidden tokens in its
        # own defaults and docstring. Derived from __file__, not a hardcoded
        # literal, so renaming or copying the script cannot silently un-exclude
        # it (the original carried the filename as a string).
        files += [p for p in sorted(root.glob(g)) if p.name != Path(__file__).name]
    if not files:
        print(f"  !  FAIL  --source-glob {source_globs} matched no files under {root}")
        return bad + 1
    src = "\n".join(p.read_text(errors="replace") for p in files)
    for name in below_floor:
        used = f"var({name})" in src
        if used:
            bad += 1
        print(f"  {'!' if used else '.'} {'FAIL' if used else 'PASS'}  "
              f"{name} referenced across {len(files)} source file(s): {used}"
              + (f"  <-- below the {floor_px}px floor and must not ship" if used else ""))
    return bad


# ---------------------------------------------------------------- Part 2 ---
def frame(render, t, scale):
    import io

    import numpy as np
    from PIL import Image
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{t:.3f}",
                        "-i", str(render), "-vf", f"scale={scale.replace('x', ':')}",
                        "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
                       capture_output=True, check=False)
    if not r.stdout:
        return None
    return np.asarray(Image.open(io.BytesIO(r.stdout)).convert("L")).astype(float)


def glyph_height(gray, box, bg_luma, threshold=28, min_run=2):
    """Tallest contiguous vertical run of ink (a real glyph stroke, not a speck
    of antialiasing) inside box, in PHONE-SCALE pixels. box is (x0,y0,x1,y1) at
    the frame's own already-scaled resolution."""
    import numpy as np
    x0, y0, x1, y1 = box
    crop = gray[y0:y1, x0:x1]
    if crop.size == 0:
        return 0
    ink = np.abs(crop - bg_luma) > threshold
    row_has_ink = ink.sum(axis=1) >= min_run   # a row counts only with >=min_run ink px across the box
    if not row_has_ink.any():
        return 0
    rows = np.where(row_has_ink)[0]
    return int(rows.max() - rows.min() + 1)


def scene_starts(scene_map, project_root):
    if scene_map:
        return {k: float(v) for k, v in json.loads(Path(scene_map).read_text()).items()}
    if not project_root:
        return {}
    html = Path(project_root) / "index.html"
    if not html.exists():
        return {}
    # Match on the ATTRIBUTES, never on their order: this repo's preview server
    # injects data-hf-id as the first attribute on every tag, and a pattern
    # anchored to the tag's opening bytes silently stops matching.
    return {cid: float(t) for cid, t in re.findall(
        r'data-composition-id="([^"]+)"[^>]*?data-start="([0-9.]+)"', html.read_text())}


def part2(render, probes_path, starts, scale, min_glyph_px):
    label = render.name if render else "no --render"
    print(f"\nPART 2 -- rendered glyph height at phone scale ({scale}), {label}")
    if not render:
        print("  SKIPPED: no --render given")
        return 0
    if not render.exists():
        print(f"  !  FAIL  render not found: {render}")
        return 1
    if not probes_path:
        print("  SKIPPED: no --probes given")
        return 0
    probes = json.loads(Path(probes_path).read_text())
    if not probes:
        print(f"  !  FAIL  {probes_path} declares no probes")
        return 1

    bad = 0
    for p in probes:
        if "t" in p:
            t = float(p["t"])
        else:
            cid = p["cid"]
            if cid not in starts:
                sys.exit(f"FATAL: probe names scene {cid!r}, which is not in the scene "
                         f"map. Pass --scene-map or --project-root.")
            t = starts[cid] + float(p.get("offset", 0.0))
        floor = int(p.get("floor", min_glyph_px))
        g = frame(render, t, scale)
        if g is None:
            # A frame that will not extract is a finding, not a skip: a probe
            # timed past the end of the render is exactly the failure mode a
            # re-time introduces, and reporting it as "?" and moving on is how
            # a gate stops protecting anything.
            bad += 1
            print(f"  !  FAIL  could not extract a frame at t={t:.2f}s  {p['label']}")
            continue
        h = glyph_height(g, p["box"], p["bg"])
        ok = h >= floor
        if not ok:
            bad += 1
        print(f"  {'.' if ok else '!'} {'PASS' if ok else 'FAIL'}  {h}px tall "
              f"(floor {floor}px)  t={t:7.2f}s  {p['label']}")
    print("  Corroborate with the project's own phone.png QC sheet -- every kinetic-reveal")
    print("  anchor at this same scale, for a human to confirm what this measures.")
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tokens", required=True)
    ap.add_argument("--floor-px", type=int, default=FLOOR_PX)
    ap.add_argument("--below-floor-token", action="append", default=[],
                    metavar="t-name",
                    help="declared below the floor and forbidden from being referenced; "
                         "give the name without its leading dashes")
    ap.add_argument("--source-glob", action="append", default=[],
                    help="where to scan for token references (default scripts/*.py)")
    ap.add_argument("--project-root", default=".")
    ap.add_argument("--render")
    ap.add_argument("--probes")
    ap.add_argument("--scene-map")
    ap.add_argument("--phone-scale", default=PHONE_SCALE)
    ap.add_argument("--min-glyph-px", type=int, default=MIN_GLYPH_PX)
    ap.add_argument("--advisory", action="store_true")
    a = ap.parse_args()

    root = Path(a.project_root).resolve()
    below = ["--" + n.lstrip("-") for n in a.below_floor_token]
    bad1 = part1(a.tokens, a.floor_px, below,
                 a.source_glob or ["scripts/*.py"], root)
    bad2 = part2(Path(a.render) if a.render else None, a.probes,
                 scene_starts(a.scene_map, a.project_root), a.phone_scale, a.min_glyph_px)

    total = bad1 + bad2
    print(f"\n{total} finding(s) across both parts.")
    if total and a.advisory:
        print("  Advisory: exits 0 regardless.")
    return 1 if (total and not a.advisory) else 0


if __name__ == "__main__":
    sys.exit(main())
