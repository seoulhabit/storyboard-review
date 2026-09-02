#!/usr/bin/env python3
"""Self-contained controls for check-static-hold.py's region-aware pass.

Run after ANY change to its thresholds or primitives:

    python3 catalog/tooling/test-static-hold-controls.py

Why this exists. On 2026-09-02 the region check was fixed twice in one day, and
after the second fix two real projects both went to zero findings. That is
exactly what a checker looks like when it has been broken into silence, so the
zeroes were worth nothing on their own -- only a control that must still FIRE
made them evidence. This script keeps that control, and its opposite, runnable.

  POSITIVE  a structured block genuinely removed mid-clip  -> MUST be flagged.
            Guards against a fix that quietly blinds the check.

  NEGATIVE  a populated region frozen for the whole clip, beside an animating
            one ("mode 4")                                  -> MUST stay silent.
            This is NOT a bug to fix here: the whole-frame pass stays alive on
            the moving region and the region pass only looks for
            content-then-EMPTY, which never happens. It is a documented coverage
            boundary, and the reason this script asserts silence rather than a
            finding. If someone later implements a frozen-region (byte-identity)
            scan, THIS is the case that must flip from silent to flagged -- and
            this assertion is the one to invert at that point, deliberately.

Both fixtures are built with ffmpeg and need no project assets.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

TOOL = Path(__file__).resolve().parent / "check-static-hold.py"
INDEX = ('<html data-resolution="landscape"><body>\n'
         '<div id="root" data-composition-id="main" data-duration="12"\n'
         '     data-width="1920" data-height="1080">\n'
         '<div class="scene clip" data-composition-id="s1" data-composition-src="f/s1.html"\n'
         '     data-start="0.000" data-duration="12.000"></div>\n'
         '</div></body></html>\n')


def build(kind, out):
    parts, prev = ["color=c=0xF7F5F0:s=1920x1080:d=12:r=30[bg]"], "bg"
    # A persistent headline, so no cell is blank from frame zero in either fixture.
    parts.append(f"[{prev}]drawbox=x=150:y=100:w=700:h=40:color=0x131516:t=fill[h]")
    prev = "h"
    if kind == "positive":
        # Structured block present 2-5s, then GENUINELY removed for 5-12s.
        for i, y in enumerate(range(400, 700, 60)):
            parts.append(f"[{prev}]drawbox=x=150:y={y}:w=600:h=30:color=0x131516:"
                         f"t=fill:enable='between(t,2,5)'[b{i}]")
            prev = f"b{i}"
    else:
        # Left region populated and FROZEN for all 12s...
        for i, y in enumerate(range(300, 640, 60)):
            parts.append(f"[{prev}]drawbox=x=200:y={y}:w=500:h=30:color=0x131516:t=fill[L{i}]")
            prev = f"L{i}"
        # ...beside a right region that moves every second, keeping the frame diff alive.
        for i in range(12):
            parts.append(f"[{prev}]drawbox=x={1150+(i%4)*70}:y={300+(i%3)*90}:w=420:h=200:"
                         f"color=0x59B8AE:t=fill:enable='between(t,{i},{i+1})'[R{i}]")
            prev = f"R{i}"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-filter_complex", ";".join(parts),
                    "-map", f"[{prev}]", "-pix_fmt", "yuv420p", "-t", "12", str(out)],
                   check=True)


def run(kind):
    with tempfile.TemporaryDirectory() as tmp:
        proj = Path(tmp)
        (proj / "renders").mkdir()
        (proj / "index.html").write_text(INDEX)
        mp4 = proj / "renders" / f"{kind}.mp4"
        build(kind, mp4)
        out = subprocess.run([sys.executable, str(TOOL), str(proj), str(mp4), "--landscape"],
                             capture_output=True, text=True, check=False).stdout
    m = re.search(r"(\d+) region-level content-void", out)
    return int(m.group(1)) if m else 0


def main():
    ok = True

    n = run("positive")
    if n >= 1:
        print(f"  PASS  positive control: genuine removal flagged ({n} content-void(s)).")
    else:
        ok = False
        print("  FAIL  positive control: a block that genuinely disappears was NOT flagged.")
        print("        The check has been blinded -- do not trust any 'no findings' result.")

    n = run("negative")
    if n == 0:
        print("  PASS  negative control: frozen-but-populated region stays silent (mode 4,")
        print("        a documented coverage boundary -- see this script's docstring).")
    else:
        ok = False
        print(f"  FAIL  negative control: {n} finding(s) on a region that never goes empty.")
        print("        Either a real improvement worth re-baselining, or a new false")
        print("        positive. Extract frames and decide deliberately before shipping.")

    print("\n  " + ("Both controls behave as expected." if ok else
                    "CONTROLS FAILED -- the checker's results are not evidence right now."))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
