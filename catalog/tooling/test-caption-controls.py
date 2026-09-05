#!/usr/bin/env python3
"""Self-contained controls for check-captions.py.

Run after any change to its parsing, its thresholds or its term matching:

    python3 catalog/tooling/test-caption-controls.py

Every control builds a throwaway project tree in a temp dir and drives the gate
through its CLI -- not by importing it -- so an exit code that stops matching
the printed verdict is itself caught. That failure is not hypothetical: a
sibling gate in this repo printed FAIL on four probes and exited 0 for two
render cycles, because a numpy bool failed an `is False` identity test.

Each control is a PAIR: a fixture the gate must reject, and one it must accept.
A gate that has been accidentally silenced passes the second and fails the
first, which a one-sided test cannot tell from a gate that works.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

TOOL = Path(__file__).resolve().parent / "check-captions.py"
SLUG = "control"


def srt(cues):
    """cues: [(start, end, [lines])] -> SRT text."""
    def ts(t):
        h, r = divmod(t, 3600)
        m, s = divmod(r, 60)
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{round((s % 1) * 1000):03d}"
    return "\n".join(f"{i+1}\n{ts(a)} --> {ts(b)}\n" + "\n".join(ls) + "\n"
                     for i, (a, b, ls) in enumerate(cues))


def vtt(cues):
    """cues: [(start, end, setting, [lines])] -> WebVTT text."""
    def ts(t):
        h, r = divmod(t, 3600)
        m, s = divmod(r, 60)
        return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"
    out = ["WEBVTT", ""]
    for a, b, setting, ls in cues:
        out.append(f"{ts(a)} --> {ts(b)}" + (f" {setting}" if setting else ""))
        out += ls + [""]
    return "\n".join(out)


def run(tmp, text, kind, *flags):
    root = Path(tmp)
    (root / "captions").mkdir(parents=True, exist_ok=True)
    (root / "captions" / f"{SLUG}.{kind}").write_text(text)
    r = subprocess.run([sys.executable, str(TOOL), str(root), "--slug", SLUG,
                        "--format", kind, *flags],
                       capture_output=True, text=True, check=False)
    return r.returncode, r.stdout


def control(name, expect_fail, text, kind, *flags, terms=None):
    with tempfile.TemporaryDirectory() as tmp:
        if terms is not None:
            p = Path(tmp) / "terms.json"
            p.write_text(json.dumps(terms))
            flags = (*flags, "--terms", str(p))
        code, out = run(tmp, text, kind, *flags)
    rejected = code != 0
    ok = rejected == expect_fail
    want = "reject" if expect_fail else "accept"
    print(f"  {'PASS' if ok else 'FAIL'}  must {want:6s}  {name}"
          + ("" if ok else f"   <-- exit {code}"))
    if not ok:
        print("".join(f"        {l}\n" for l in out.strip().splitlines()[-4:]))
    return ok


def main():
    ok = True
    long_line = "x" * 50
    print("\n  LINE LENGTH (cap 42)")
    ok &= control("a 50-char line", True,
                  srt([(0.0, 4.0, [long_line])]), "srt")
    ok &= control("a 40-char line", False,
                  srt([(0.0, 4.0, ["x" * 40])]), "srt")

    print("\n  MINIMUM DURATION (floor 1.0s)")
    ok &= control("a 0.4s cue", True, srt([(0.0, 0.4, ["short"])]), "srt")
    ok &= control("a 1.2s cue", False, srt([(0.0, 1.2, ["short"])]), "srt")

    print("\n  READING SPEED (hard ceiling 20 CPS)")
    fast = srt([(0.0, 1.0, ["thirty characters of caption ab"])])
    ok &= control("31 chars in 1.0s = 31 CPS", True, fast, "srt", "--max-cps-hard", "20")
    ok &= control("the same cue inside --exempt-window", False, fast, "srt",
                  "--max-cps-hard", "20", "--exempt-window", "0.00-1.05")
    ok &= control("31 chars in 3.0s = 10 CPS", False,
                  srt([(0.0, 3.0, ["thirty characters of caption ab"])]), "srt",
                  "--max-cps-hard", "20")

    print("\n  OVERLAP")
    ok &= control("cue 1 outlasts cue 2's start", True,
                  srt([(0.0, 3.0, ["one"]), (2.0, 5.0, ["two"])]), "srt")

    print("\n  LINE COUNT (cap 2, off by default)")
    three = srt([(0.0, 4.0, ["one", "two", "three"])])
    ok &= control("three lines with --max-lines 2", True, three, "srt", "--max-lines", "2")
    ok &= control("three lines with the cap off", False, three, "srt")

    print("\n  TERM SPELLING (case-sensitive -- the whole point)")
    body = srt([(0.0, 4.0, ["Research from Bitop and Merck."])])
    ok &= control("'Bitop' present when 'bitop' is required", True, body, "srt",
                  terms={"required": ["bitop"], "forbidden": []})
    ok &= control("'Bitop' present when it is forbidden", True, body, "srt",
                  terms={"required": [], "forbidden": ["Bitop"]})
    ok &= control("'Merck' present and required", False, body, "srt",
                  terms={"required": ["Merck"], "forbidden": ["Merk"]})

    print("\n  CUE PLACEMENT (VTT only)")
    ok &= control("a cue with no setting", True,
                  vtt([(0.0, 4.0, "", ["placed nowhere"])]), "vtt",
                  "--require-cue-settings")
    ok &= control("a cue carrying a setting", False,
                  vtt([(0.0, 4.0, "line:15%,align:center", ["placed"])]), "vtt",
                  "--require-cue-settings")

    print("\n  NON-SPEECH CAP")
    noisy = srt([(0.0, 2.0, ["[chime]"]), (2.5, 4.5, ["[whoosh]"]),
                 (5.0, 7.0, ["[thud]"]), (7.5, 9.5, ["[chime]"])])
    ok &= control("four non-speech cues with a cap of 3", True, noisy, "srt",
                  "--max-nonspeech", "3")
    ok &= control("the same four with the cap off", False, noisy, "srt")

    print("\n  MISSING FILE")
    with tempfile.TemporaryDirectory() as tmp:
        code, _ = subprocess.run(
            [sys.executable, str(TOOL), tmp, "--slug", "nope", "--format", "srt"],
            capture_output=True, text=True, check=False).returncode, None
    good = code != 0
    ok &= good
    print(f"  {'PASS' if good else 'FAIL'}  must reject  an absent sidecar")

    print("\n  All controls behave as expected.\n" if ok else
          "\n  A CONTROL FAILED -- do not trust this gate until it is resolved.\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
