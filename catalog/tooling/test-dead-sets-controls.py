#!/usr/bin/env python3
"""Self-contained controls for check-dead-sets.py.

Run after ANY change to how it resolves which set is in force at a reveal:

    python3 catalog/tooling/test-dead-sets-controls.py

Why this exists. The gate's whole claim is that it catches a `tl.set()` whose
value never reaches the screen. The FIRST implementation of this check looked
for sets declared out of time order, ran against the real defect in
`videos/ectoin-normal-person/compositions/frames/03-cell.html`, and printed a
clean `0 shadowed set(s)` -- because the two sets there ARE in ascending order
(t=0 then t=16.95). The bug is the gap between a set and its use, not the order
of the sets. A scanner that reports zero is worth nothing until something that
SHOULD trip it reliably does.

  POSITIVE   the real 03-cell shape: sets at t=0 and t=16.95 on one element,
             reveals at 17.35 and 40.05. Both reveals resolve to the t=16.95
             value, so the t=0 line is authored and never seen -> must report
             EXACTLY 1 dead set, and name the t=0 one.

  ORDERING   two sets in DESCENDING declaration order, each in force at its own
             reveal -> must report 0. This is the assertion that fails first if
             anyone reduces the check back to an order comparison. It is the
             exact fixture the broken first version passed and the real bug
             failed, so it guards the implementation that actually shipped
             a repeated caption to a rendered video.

  ADJACENT   the fix's shape: each set stamped 0.06s before its own reveal ->
             must report 0. Guards against a check so eager that correct code
             cannot satisfy it.

  SPARSE     one set, three reveals -> must report 0. An element legitimately
             stamped once and shown repeatedly is not a finding; fewer than two
             sets can never be dead.

Fixtures are plain strings -- this gate reads source, so it needs no render, no
project assets and no ffmpeg.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

TOOL = Path(__file__).resolve().parent / "check-dead-sets.py"


def frame(body):
    return ("<html><body><div id=\"root\"><template>\n<script>\n"
            "const tl = gsap.timeline({ paused: true });\n" + body +
            "\n</script>\n</template></div></body></html>\n")


def band(text, t_set, t_reveal):
    return (f"    tl.set('#band-t', {{ textContent: {text!r} }}, {t_set:.3f});\n"
            f"    tl.to('#band', {{ opacity: 1, duration: 0.30,\n"
            f"                      ease: 'power2.out' }}, {t_reveal - 0.35:.3f});\n"
            f"    tl.to('#band-t', {{ opacity: 1, duration: 0.28,\n"
            f"                       ease: 'none' }}, {t_reveal:.3f});\n"
            f"    tl.to('#band-t', {{ opacity: 0, duration: 0.25,\n"
            f"                       ease: 'none' }}, {t_reveal + 1.85:.3f});\n")


CASES = {
    # the real defect: both sets declared early, second one wins both reveals
    "positive": (band("ECTOIN IS THE ANSWER IT EVOLVED", 0.0, 40.05)
                 + band("WATER LEAVES - PROTEINS DESTABILISE", 16.95, 17.35), 1),
    # descending declaration order, but each value IS on screen at its reveal
    "ordering": (band("SECOND LINE", 39.64, 40.05)
                 + band("FIRST LINE", 16.94, 17.35), 0),
    # the fix: every set lands just before its own use
    "adjacent": (band("FIRST LINE", 16.94, 17.35)
                 + band("SECOND LINE", 39.64, 40.05), 0),
    # one set, reused three times -- never a finding
    "sparse": ("    tl.set('#band-t', { textContent: 'ONE LINE' }, 0.000);\n"
               + "".join(f"    tl.to('#band-t', {{ opacity: 1, duration: 0.28,\n"
                         f"                       ease: 'none' }}, {t:.3f});\n"
                         for t in (5.0, 20.0, 35.0)), 0),
}


def run(name, body, want):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / f"{name}.html"
        p.write_text(frame(body))
        r = subprocess.run([sys.executable, str(TOOL), str(p)],
                           capture_output=True, text=True,
                           check=False)  # exits 1 on a finding, which `positive` wants
        got = int(r.stdout.strip().split("\n")[-1].split()[0])
        ok = got == want
        detail = ""
        if name == "positive" and ok:
            # must name the t=0 set, not merely count one
            ok = "@0.00" in r.stdout and "ECTOIN" in r.stdout
            detail = "" if ok else "   counted 1 but did not name the t=0 set"
        print(f"  {'PASS' if ok else 'FAIL'}  {name:9s} "
              f"expected {want} dead, got {got}{detail}")
        if not ok and r.stdout.strip():
            for line in r.stdout.strip().split("\n"):
                print(f"          | {line}")
        return ok


if __name__ == "__main__":
    print(f"check-dead-sets.py controls  ({TOOL})")
    results = [run(n, b, w) for n, (b, w) in CASES.items()]
    print(f"\n{sum(results)}/{len(results)} controls pass")
    sys.exit(0 if all(results) else 1)
