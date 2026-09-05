#!/usr/bin/env python3
"""Self-contained controls for check-contrast-tokens.py (beside this file).

Run after any change to its ratio arithmetic, its floor selection, its token
resolution, or its expected-FAIL inversion:

    python3 catalog/tooling/test-contrast-tokens-controls.py

  ARITHMETIC       the ratio function against values that do not come from this
                   repo: black on white is 21.00:1 by definition and a colour
                   on itself is 1.00:1 by definition, and #767676 / #949494 on
                   white are WCAG's own published AA and AA-large boundary
                   greys (4.54:1 and 3.03:1). The two definitional anchors alone
                   would not catch a broken gamma curve -- they hold even if the
                   sRGB linearisation is dropped entirely -- so the two greys
                   are what actually pin the curve. Symmetry is checked too:
                   the ratio must not depend on which colour is called fg.

  FLOOR SELECTION  ONE pair at 3.45:1, declared three ways -- "text" (4.5, must
                   fail), "graphic" (3.0, must pass) and a numeric literal.
                   Same colours every time, so the floor is the only variable.

  FLOOR OVERRIDES  the same pair again with --text-floor lowered past it, which
                   must flip it to passing. That proves the CLI flags reach the
                   comparison rather than being parsed and dropped.

  TOKEN RESOLUTION a pair written with token keys and the same pair written
                   with literal #rrggbb must produce the same ratio; and an
                   unknown key must be a FATAL exit, not a silent default. A
                   gate that quietly resolved a typo'd token to black would
                   report a beautiful 21:1 for a pair nobody is actually
                   shipping.

  EXPECTED FAIL    the inversion, in all four combinations: a plain pair that
                   passes (fine) or fails (a finding), and an "expected FAIL"
                   pair that fails (fine, and counted as documented) or PASSES
                   (a finding). That last one is the whole reason the feature
                   exists and is the only case in this directory where a PASS
                   is the failure condition -- a note saying "expected FAIL" is
                   a claim about the palette, and it becomes a lie the moment
                   someone lightens the token. A control that only checked the
                   happy direction would keep passing while the inversion was
                   deleted.

  EXIT CODE        the gate is a HARD gate: every fixture above is driven
                   through its CLI and its exit status asserted, not just its
                   printed text. A gate that prints FAIL and exits 0 protects
                   nothing, and that exact defect has shipped in this directory
                   before (an np.bool_ failing an `is False` identity test).
"""
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

TOOL = Path(__file__).resolve().parent / "check-contrast-tokens.py"

WHITE, BLACK = "#FFFFFF", "#000000"
GREY_AA = "#767676"       # WCAG's published 4.54:1 on white
GREY_AA_LARGE = "#949494"  # WCAG's published 3.03:1 on white
GREY_MID = "#8A8A8A"       # 3.45:1 on white: fails text, passes graphic


def load_tool():
    spec = importlib.util.spec_from_file_location("check_contrast_tokens", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_gate(tmp, doc, *flags):
    p = Path(tmp) / "pairs.json"
    p.write_text(json.dumps(doc))
    r = subprocess.run([sys.executable, str(TOOL), str(p), *flags],
                       capture_output=True, text=True, check=False)
    return r.returncode, r.stdout + r.stderr


def pair(label, fg, bg, floor=None, note=None):
    d = {"label": label, "fg": fg, "bg": bg}
    if floor is not None:
        d["floor"] = floor
    if note is not None:
        d["note"] = note
    return d


def main():
    if not TOOL.exists():
        print(f"test-contrast-tokens-controls: {TOOL.name} not found beside this fixture -- "
              f"skipping (exit 0).")
        return 0
    mod = load_tool()
    ok = True

    print("\n  ARITHMETIC -- against WCAG's own numbers, not this repo's:")
    cases = [(BLACK, WHITE, 21.00, "black on white (definitional maximum)"),
             (WHITE, WHITE, 1.00, "white on white (definitional minimum)"),
             (GREY_AA, WHITE, 4.54, "WCAG's published AA boundary grey"),
             (GREY_AA_LARGE, WHITE, 3.03, "WCAG's published AA-large boundary grey")]
    for fg, bg, want, why in cases:
        got = mod.ratio(fg, bg)
        good = abs(got - want) < 0.01
        ok &= good
        print(f"    {fg} on {bg}: {got:6.3f}:1  expected {want:5.2f}  {why}   "
              f"{'PASS' if good else 'FAIL <-- the ratio arithmetic is wrong'}")
    sym = abs(mod.ratio(GREY_AA, WHITE) - mod.ratio(WHITE, GREY_AA)) < 1e-9
    ok &= sym
    print(f"    symmetric in fg/bg: {sym}   "
          f"{'PASS' if sym else 'FAIL <-- the ratio depends on argument order'}")

    with tempfile.TemporaryDirectory() as tmp:
        tokens = {"paper": WHITE, "mid": GREY_MID, "ink": BLACK}

        print("\n  FLOOR SELECTION -- one 3.45:1 pair declared three ways, colours held fixed:")
        rc, out = run_gate(tmp, {"tokens": tokens, "pairs": [
            pair("mid on paper as text", "mid", "paper"),                    # 4.5 -> FAIL
            pair("mid on paper as graphic", "mid", "paper", floor="graphic"),  # 3.0 -> PASS
            pair("mid on paper at 3.4", "mid", "paper", floor=3.4),          # 3.4 -> PASS
        ]})
        lines = [ln for ln in out.splitlines() if ":1 (floor" in ln]
        verdicts = [ln.strip().split()[0] for ln in lines]
        good = verdicts == ["FAIL", "PASS", "PASS"] and rc == 1
        ok &= good
        print(f"    verdicts: {verdicts} (expected ['FAIL', 'PASS', 'PASS'])   exit {rc} (must be 1)")
        print(f"    {'PASS' if good else 'FAIL <-- floor selection is not reading the per-pair floor'}")

        print("\n  FLOOR OVERRIDES -- the same failing pair with --text-floor lowered under it:")
        doc = {"tokens": tokens, "pairs": [pair("mid on paper as text", "mid", "paper")]}
        rc_default, _ = run_gate(tmp, doc)
        rc_lowered, out = run_gate(tmp, doc, "--text-floor", "3.0")
        good = rc_default == 1 and rc_lowered == 0
        ok &= good
        print(f"    default floor -> exit {rc_default} (must be 1)   --text-floor 3.0 -> exit "
              f"{rc_lowered} (must be 0)   "
              f"{'PASS' if good else 'FAIL <-- the CLI floor flags are parsed but not used'}")

        print("\n  TOKEN RESOLUTION -- keys and literals must agree; an unknown key must be fatal:")
        rc, out = run_gate(tmp, {"tokens": tokens, "pairs": [
            pair("by key", "mid", "paper", floor="graphic"),
            pair("by literal", GREY_MID, WHITE, floor="graphic"),
        ]})
        ratios = [ln.split(":1")[0].strip().split()[-1] for ln in out.splitlines()
                  if ":1 (floor" in ln]
        agree = len(ratios) == 2 and ratios[0] == ratios[1] and rc == 0
        ok &= agree
        print(f"    ratios: {ratios} (must be identical)   "
              f"{'PASS' if agree else 'FAIL <-- key and literal resolve differently'}")

        rc, out = run_gate(tmp, {"tokens": tokens, "pairs": [
            pair("typo", "mdi", "paper"),
        ]})
        fatal = rc != 0 and "FATAL" in out
        ok &= fatal
        print(f"    unknown key -> exit {rc}, FATAL in output: {'FATAL' in out}   "
              f"{'PASS' if fatal else 'FAIL <-- an unresolvable token is being silently defaulted'}")

        print("\n  EXPECTED FAIL -- the inversion, all four combinations:")
        # Each in its own run so one pair's finding cannot mask another's.
        combos = [
            ("plain pair that passes", pair("ink on paper", "ink", "paper"), 0),
            ("plain pair that fails", pair("mid on paper", "mid", "paper"), 1),
            ("expected-FAIL pair that fails", pair(
                "mid on paper", "mid", "paper",
                note="expected FAIL -- superseded, must not ship"), 0),
            ("expected-FAIL pair that now PASSES", pair(
                "ink on paper", "ink", "paper",
                note="expected FAIL -- superseded, must not ship"), 1),
        ]
        for label, p, want_rc in combos:
            rc, out = run_gate(tmp, {"tokens": tokens, "pairs": [p]})
            good = rc == want_rc
            ok &= good
            note = "  <-- a PASS is the failure here" if label.endswith("PASSES") else ""
            print(f"    {label:38s} exit {rc} (must be {want_rc})   "
                  f"{'PASS' if good else 'FAIL <-- the expected-FAIL inversion is broken'}{note}")

        rc, out = run_gate(tmp, {"tokens": tokens, "pairs": [
            pair("mid on paper", "mid", "paper", note="expected FAIL -- superseded"),
        ]})
        counted = "1 deliberate documented failure" in out
        ok &= counted
        print(f"    documented failures counted separately from findings: {counted}   "
              f"{'PASS' if counted else 'FAIL <-- expected failures are not being reported as such'}")

    print("\n  All controls behave as expected.\n" if ok else
          "\n  A CONTROL FAILED -- do not trust this gate until it is resolved.\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
