#!/usr/bin/env python3
"""Self-contained controls for check-cadence.py.

Run after ANY change to its thresholds, its sampling, or its scene windowing:

    python3 catalog/tooling/test-cadence-controls.py

Why this exists. check-cadence.py's whole claim to be a different tool from
check-static-hold.py rests on ONE decision: a step counts as a beat only if it
clears a mean |dLuma| floor AND a per-pixel maximum. Drop either half and the
script still runs, still prints a plausible percentage, and is wrong in a
direction nobody notices -- `videos/pilling-vs-peeling`'s round-3 record
credited a scene with "8% active steps" that were two h264 keyframe refreshes
and no animation at all. A percentage is not evidence unless something that
should NOT count reliably does not.

  POSITIVE  a 200x200 high-contrast block jumping every 0.5s for 2s, then
            static for 4s  -> must report a quiet run over the 1.6s shorts
            ceiling AND more than zero active steps. Guards both ways at once:
            a tool tuned so hard that real motion stops registering would pass
            the quiet-run half while failing the active-steps half.

  NEGATIVE  the whole frame stepping +6 luma once a second, nothing moving --
            a codec-refresh look-alike (mean ~5, maxpix < 40) -> must count
            EXACTLY 0 active steps. This is the encoder-artifact rejection the
            docstring is about; it is the assertion that fails first if anyone
            "simplifies" the beat test down to the mean.

  ALIAS     --landscape must behave identically to --longform (both raise the
            quiet ceiling to 6.0s), so the positive fixture's 4s hold stops
            being a finding under either spelling and under neither.

Both fixtures are built with ffmpeg and need no project assets.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

TOOL = Path(__file__).resolve().parent / "check-cadence.py"
W, H, FPS, DUR = 1080, 1920, 30, 6
INDEX = ('<html><body>\n'
         '<div id="root" data-composition-id="main" data-duration="6"\n'
         f'     data-width="{W}" data-height="{H}">\n'
         '<div class="scene clip" data-composition-id="s1" data-composition-src="f/s1.html"\n'
         '     data-start="0.000" data-duration="6.000"></div>\n'
         '</div></body></html>\n')

# Five non-overlapping positions, so every jump changes ~2x the block's area.
POSITIONS = [(140, 400), (740, 400), (140, 1000), (740, 1000), (140, 1500)]


def build(kind, out):
    if kind == "positive":
        parts = [f"color=c=0xF7F5F0:s={W}x{H}:d={DUR}:r={FPS}[bg]"]
        prev = "bg"
        # Jumps at 0.5 / 1.0 / 1.5 / 2.0s; the last position then HOLDS 2-6s.
        spans = [(0, 0.5), (0.5, 1.0), (1.0, 1.5), (1.5, 2.0), (2.0, DUR)]
        for i, ((x, y), (t0, t1)) in enumerate(zip(POSITIONS, spans)):
            parts.append(f"[{prev}]drawbox=x={x}:y={y}:w=200:h=200:color=0x131516:"
                         f"t=fill:enable='between(t,{t0},{t1})'[b{i}]")
            prev = f"b{i}"
    else:
        # Nothing moves. The WHOLE frame steps +6 (RGB) once a second, which is
        # what an h264 keyframe refresh looks like to a frame differ: a big mean
        # with a tiny per-pixel max.
        parts = [f"color=c=0x646464:s={W}x{H}:d={DUR}:r={FPS}[bg]"]
        prev = "bg"
        for i in range(1, DUR):
            g = 0x64 + 6 * i
            hexc = f"0x{g:02X}{g:02X}{g:02X}"
            parts.append(f"[{prev}]drawbox=x=0:y=0:w={W}:h={H}:color={hexc}:"
                         f"t=fill:enable='between(t,{i},{i+1})'[s{i}]")
            prev = f"s{i}"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-filter_complex", ";".join(parts),
                    "-map", f"[{prev}]", "-pix_fmt", "yuv420p", "-crf", "16",
                    "-t", str(DUR), str(out)], check=True)


def measure(out):
    """(active_steps, total_steps, longest_quiet_s, over_ceiling) from the tool's stdout."""
    m = re.search(r"whole video: (\d+)/(\d+) steps", out)
    act, tot = (int(m.group(1)), int(m.group(2))) if m else (None, None)
    row = re.search(r"^\s*1\s+[\d.]+-\s*[\d.]+\s+\d+/\d+\s+\d+%\s+([\d.]+)s(\s+<-- over ceiling)?\s*$",
                    out, re.MULTILINE)
    quiet = float(row.group(1)) if row else None
    over = bool(row and row.group(2))
    return act, tot, quiet, over


def run(proj, mp4, *flags):
    return subprocess.run([sys.executable, str(TOOL), str(proj), str(mp4), *flags],
                          capture_output=True, text=True, check=False).stdout


def main():
    ok = True
    with tempfile.TemporaryDirectory() as tmp:
        proj = Path(tmp)
        (proj / "renders").mkdir()
        (proj / "index.html").write_text(INDEX)

        pos = proj / "renders" / "positive.mp4"
        neg = proj / "renders" / "negative.mp4"
        build("positive", pos)
        build("negative", neg)

        p_out = run(proj, pos)
        p_act, p_tot, p_quiet, p_over = measure(p_out)
        print(f"  positive fixture: {p_act}/{p_tot} active steps, longest quiet run "
              f"{p_quiet}s, over-ceiling flag={p_over}")
        if p_quiet is not None and p_quiet > 1.6 and p_over:
            print("  PASS  positive control (a): the 4s hold clears the 1.6s shorts ceiling.")
        else:
            ok = False
            print("  FAIL  positive control (a): a 4s dead hold was NOT reported over the "
                  "1.6s ceiling.")
            print("        The quiet-run measurement or the scene windowing is broken.")
        if p_act and p_act > 0:
            print(f"  PASS  positive control (b): real motion still registers ({p_act} beats).")
        else:
            ok = False
            print("  FAIL  positive control (b): a 200x200 block jumping every 0.5s scored "
                  "0 beats.")
            print("        The thresholds are now blind to real motion; no percentage this "
                  "tool\n        prints is evidence of anything.")

        n_out = run(proj, neg)
        n_act, n_tot, n_quiet, _ = measure(n_out)
        print(f"\n  negative fixture: {n_act}/{n_tot} active steps, longest quiet run "
              f"{n_quiet}s")
        if n_act == 0:
            print("  PASS  negative control: whole-frame luma steps counted as 0 beats")
            print("        (mean clears the floor, maxpix does not -- the encoder-artifact")
            print("        rejection is intact).")
        else:
            ok = False
            print(f"  FAIL  negative control: {n_act} beat(s) counted on a clip where "
                  "nothing moves.")
            print("        A mean-only test would do exactly this. Restore the maxpix half")
            print("        before trusting any active-step share this tool has ever printed.")

        lf = run(proj, pos, "--longform")
        ls = run(proj, pos, "--landscape")
        _, _, lf_q, lf_over = measure(lf)
        _, _, ls_q, ls_over = measure(ls)
        print(f"\n  alias: --longform over-ceiling={lf_over}, --landscape "
              f"over-ceiling={ls_over}, quiet {lf_q}s / {ls_q}s")
        if lf == ls and not lf_over and "6.0s quiet ceiling" in lf:
            print("  PASS  alias control: --landscape == --longform, both at the 6.0s ceiling")
            print("        (the same 4s hold is a finding at 1.6s and not at 6.0s).")
        else:
            ok = False
            print("  FAIL  alias control: --landscape and --longform do not agree, or the")
            print("        long-form ceiling did not rebind to 6.0s.")

    print("\n  " + ("All controls behave as expected." if ok else
                    "CONTROLS FAILED -- check-cadence.py's output is not evidence right now."))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
