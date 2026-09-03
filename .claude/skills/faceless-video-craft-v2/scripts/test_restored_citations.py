#!/usr/bin/env python3
"""Controls for check_restored_citations.py.

    python3 scripts/test_restored_citations.py

Run after ANY change to that checker's parsing, its citation convention, or its
renumbering. It works on throwaway copies and never touches the real skills.

Why this exists. The guard this replaces covered two of eight citations and
printed `identical=True`, which read as an all-clear while five of the other six
were drifted. So the property under test is not "does it pass on a good tree" --
it is "does it FAIL on each way the coupling actually breaks", and there are two
of those, with different correct responses:

  CLEAN       an untouched copy                        -> 8/8, exit 0.

  DRIFT       lines inserted ABOVE every cited span. Every citation is stale by
              the same offset, every body is still contiguous  -> all 8 reported,
              each new range exactly the old one plus the offset, and --fix
              renumbers to a clean re-run. The per-rule offset check is the
              point: an earlier version got heading-led rules (R4/R7/R8) wrong
              by two lines while looking correct in aggregate, because it
              assumed a fixed one-line heading gap instead of walking back over
              blanks. Aggregate counts hid it; per-rule arithmetic caught it.

  FRAGMENT    prose inserted INSIDE a cited span, so that body matches no
              contiguous range any more  -> reported as FRAGMENT, and NOT
              renumbered. Renumbering a fragmented body would mint a citation
              that points at text the file does not reproduce, which is the one
              outcome worse than the drift it was trying to fix.
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILLS = HERE.parent.parent


def stage(tmp):
    """A throwaway copy of just the three files the checker touches."""
    (tmp / "faceless-video-craft").mkdir(parents=True)
    (tmp / "faceless-video-craft-v2" / "references").mkdir(parents=True)
    (tmp / "faceless-video-craft-v2" / "scripts").mkdir(parents=True)
    shutil.copy(SKILLS / "faceless-video-craft" / "SKILL.md",
                tmp / "faceless-video-craft" / "SKILL.md")
    shutil.copy(SKILLS / "faceless-video-craft-v2" / "references" / "restored-v1-rules.md",
                tmp / "faceless-video-craft-v2" / "references" / "restored-v1-rules.md")
    shutil.copy(HERE / "check_restored_citations.py",
                tmp / "faceless-video-craft-v2" / "scripts" / "check_restored_citations.py")
    return (tmp / "faceless-video-craft-v2" / "scripts" / "check_restored_citations.py",
            tmp / "faceless-video-craft" / "SKILL.md")


def run(checker, *args):
    p = subprocess.run([sys.executable, str(checker), *args],
                       capture_output=True, text=True, check=False)
    return p.stdout, p.returncode


def insert(path, at, lines):
    with open(path, encoding="utf-8") as fh:
        ls = fh.read().split("\n")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(ls[:at] + lines + ls[at:]))


def main() -> int:
    ok = True
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        checker, v1 = stage(tmp)

        print("\n  CLEAN — untouched copy (must pass):")
        out, rc = run(checker)
        good = "8/8" in out and rc == 0
        ok &= good
        print(f"    {out.strip().splitlines()[-2].strip()}  exit={rc}   "
              f"{'PASS' if good else 'FAIL <-- the checker cannot even confirm a good tree'}")

        print("\n  DRIFT — 5 lines inserted above every span (must flag all 8, each +5):")
        before = dict(re.findall(r"OK       (R\d+): lines (\d+)-\d+", out))
        insert(v1, 6, [""] * 5)
        out, rc = run(checker)
        found = dict(re.findall(r"DRIFT    (R\d+): cites \d+-\d+, actually (\d+)-\d+", out))
        offsets = {r: int(found[r]) - int(before[r]) for r in before if r in found}
        good = len(found) == 8 and set(offsets.values()) == {5}
        ok &= good
        print(f"    {len(found)}/8 flagged, offsets {sorted(set(offsets.values()))}   "
              f"{'PASS' if good else f'FAIL <-- uneven offsets {offsets}'}")

        out, rc = run(checker, "--fix")
        out, rc = run(checker)
        good = "8/8" in out and rc == 0
        ok &= good
        print(f"    --fix then re-run: {'clean' if good else 'STILL DIRTY'}  exit={rc}   "
              f"{'PASS' if good else 'FAIL'}")

        print("\n  FRAGMENT — prose inserted INSIDE R5's span (must NOT renumber it):")
        insert(v1, 1300, ["", "**Inserted mid-span.**", ""])
        out, rc = run(checker)
        good = "FRAGMENT" in out and "R5" in out and rc != 0
        ok &= good
        print(f"    R5 reported as FRAGMENT: {'yes' if good else 'no'}  exit={rc}   "
              f"{'PASS' if good else 'FAIL <-- a fragmented body must never be auto-renumbered'}")

        out, _ = run(checker, "--fix")
        still = "FRAGMENT" in run(checker)[0]
        ok &= still
        print(f"    --fix left it fragmented rather than minting a false citation: "
              f"{'yes' if still else 'NO'}   {'PASS' if still else 'FAIL'}")

    print("\n  All controls behave as expected.\n" if ok else
          "\n  A CONTROL FAILED — do not trust this checker until it is resolved.\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
