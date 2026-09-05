#!/usr/bin/env python3
"""Build the visual review set into renders/qc/ so a human (or the agent) looks
at real pixels rather than at a gate's summary line.

    python3 scripts/qc_sheets.py . renders/<final>.mp4

  sheet-early/mid/late.png  thirds of the runtime, 24 frames each
  phone.png                 every kinetic-anchor moment at 25% -- the scale at
                            which this is actually watched, and the only pass
                            that has ever caught a .worldclip crop
  seams.png                 the seam midpoints check-seams.py wrote

Phone-scale is a separate sheet on purpose: a 480px-wide contact tile is small
enough to hide a legibility failure that a 25% downscale of the full frame
shows immediately.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
QC = ROOT / "renders" / "qc"
ANCHORS = ["replace", "powder", "go", "trials", "remove", "building", "structure",
           "cut", "sunscreen", "daltons", "door", "film", "breaks", "decides",
           "keep", "three", "effect", "up", "protein", "protect"]


def sh(*a):
    return subprocess.run([str(x) for x in a], capture_output=True, text=True)


def tile(frames, out, cols, scale):
    if not frames:
        return None
    lst = QC / "_list.txt"
    lst.write_text("".join(f"file '{f}'\n" for f in frames))
    rows = (len(frames) + cols - 1) // cols
    r = sh("ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-r", "1", "-i", lst,
           "-filter_complex", f"scale={scale}:-1,tile={cols}x{rows}:padding=6:color=#7a756c",
           "-frames:v", "1", out)
    lst.unlink(missing_ok=True)
    return out if r.returncode == 0 else None


def grab(render, t, path, scale=None):
    vf = ["-vf", f"scale={scale}"] if scale else []
    sh("ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", render, "-frames:v", "1", *vf, path)
    return path if Path(path).exists() else None


def main():
    render = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    if render and not render.is_absolute():
        render = ROOT / render
    if not render or not render.exists():
        raise SystemExit("usage: qc_sheets.py <project-root> <final.mp4>")
    QC.mkdir(parents=True, exist_ok=True)
    dur = float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration",
                   "-of", "default=nk=1:nw=1", render).stdout.strip())
    made = []

    tmp = QC / "_f"
    tmp.mkdir(exist_ok=True)
    for name, (a, b) in {"early": (0, dur / 3), "mid": (dur / 3, 2 * dur / 3),
                         "late": (2 * dur / 3, dur)}.items():
        step = (b - a) / 24
        frames = [f for i in range(24)
                  if (f := grab(render, a + i * step + step / 2, str(tmp / f"{name}-{i:02d}.png")))]
        out = tile(frames, str(QC / f"sheet-{name}.png"), 6, 420)
        if out:
            made.append(out)
        print(f"  sheet-{name}.png  {len(frames)} frames  {a:.1f}-{b:.1f}s")

    # phone scale, on the moments the piece is actually built around
    rv = ROOT / "index.reveals.json"
    times = [0.05, dur - 2.0]
    if rv.exists():
        seen = set()
        for r in json.loads(rv.read_text()):
            if r["word"].lower().strip(".,?!") in ANCHORS and r["word"] not in seen:
                seen.add(r["word"]); times.append(r["abs"] + 0.45)
    times = sorted(t for t in times if 0 <= t < dur)[:24]
    frames = [f for i, t in enumerate(times)
              if (f := grab(render, t, str(tmp / f"phone-{i:02d}.png"), scale="480:270"))]
    out = tile(frames, str(QC / "phone.png"), 4, 480)
    if out:
        made.append(out)
    print(f"  phone.png        {len(frames)} frames at 25% (480x270)")

    seams = sorted((QC / "seams").glob("*-mid.png"))
    if seams:
        out = tile([str(p) for p in seams], str(QC / "seams.png"), 4, 460)
        if out:
            made.append(out)
        print(f"  seams.png        {len(seams)} transition midpoints")
    else:
        print("  seams.png        skipped -- run check-seams.py --render first")

    for f in tmp.glob("*.png"):
        f.unlink()
    tmp.rmdir()
    print(f"\n  {len(made)} sheet(s) in {QC.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
