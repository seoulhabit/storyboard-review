#!/usr/bin/env python3
"""Verify every verbatim citation in references/restored-v1-rules.md.

    python3 scripts/check_restored_citations.py [--fix]

That file reproduces sections of v1's SKILL.md **verbatim** and cites each by
line range. Both halves have to move together: any edit to v1 above a cited
span shifts it, nothing errors, and the file then claims a range that no longer
holds what it reproduces. Only a checker catches it.

WHY THIS EXISTS, AND WHY IT COVERS ALL EIGHT. The first guard written for this
handled R7 and R8 -- the two sections added the day it was written -- and
asserted byte-identity on exactly those. It printed `identical=True` twice and
said nothing about R1-R6, five of which were drifted at the time, several by
more than 1,500 lines. It was not wrong about what it checked; it was silent
about what it did not, which reads the same from outside. A partial guard that
reports success is worse than no guard, because the success is quoted.

TWO FAILURE MODES, AND ONLY ONE IS SAFE TO AUTO-FIX:

  POINTER DRIFT  the body still exists in v1 as one contiguous block, just at
                 different line numbers. The citation is stale; the content is
                 fine. `--fix` renumbers it.

  FRAGMENTED     new prose was inserted INSIDE the cited span, so the stored
                 body matches no contiguous range in v1 any more. Renumbering
                 cannot repair this and would silently mint a false citation.
                 Re-extraction is a content decision -- how much of the new
                 material belongs to this rule -- so this is reported and left
                 alone.

CITATION CONVENTION, which differs per rule and is inferred, not assumed: when
the cited range begins on a MARKDOWN HEADING the reproduced body omits that
heading, because the R-section's own title stands in for it (R4, R7, R8). When
it begins mid-prose the body covers the whole range (R1, R2, R3, R5, R6). Both
are accepted; a body is a match under either reading.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V1 = ROOT.parent / "faceless-video-craft" / "SKILL.md"
RULES = ROOT / "references" / "restored-v1-rules.md"
HEADING = re.compile(r"^#{1,6} ")


def spans(v1_lines, a, b):
    """The cited range read both ways: with and without a leading heading."""
    whole = "\n".join(v1_lines[a - 1:b]).strip("\n")
    if a - 1 < len(v1_lines) and HEADING.match(v1_lines[a - 1]):
        return {"whole": whole, "no-heading": "\n".join(v1_lines[a:b]).strip("\n")}
    return {"whole": whole}


def main() -> int:
    fix = "--fix" in sys.argv
    with open(V1, encoding="utf-8") as fh:
        v1 = fh.read().split("\n")
    with open(RULES, encoding="utf-8") as fh:
        text = fh.read()
    joined = "\n".join(v1)

    drift, frag, ok = [], [], 0
    for part in re.split(r"\n(?=## R\d+ · )", text):
        m = re.match(r"## (R\d+) · ", part)
        if not m:
            continue
        rid = m.group(1)
        cite = re.search(r"(\*\*Source:\*\* `[^`]+` lines )(\d+)-(\d+)", part)
        if not cite:
            print(f"  MISSING  {rid}: no line citation")
            frag.append(rid)
            continue
        a, b = int(cite.group(2)), int(cite.group(3))
        rest = part[cite.end():]
        rest = rest.split("\n", 1)[1] if "\n" in rest else ""
        body = re.sub(r"\n+---\s*$", "", rest.strip("\n")).strip("\n")

        if body in spans(v1, a, b).values():
            print(f"  OK       {rid}: lines {a}-{b}")
            ok += 1
            continue

        # where does this body actually live now?
        idx = joined.find(body)
        if idx < 0:
            print(f"  FRAGMENT {rid}: cites {a}-{b}; body matches no contiguous range "
                  f"in v1 — prose was inserted mid-span. Re-extract by hand.")
            frag.append(rid)
            continue
        start = joined.count("\n", 0, idx) + 1
        end = start + len(body.split("\n")) - 1
        # A heading-led rule's body omits its heading, so the body starts one or
        # more lines BELOW the line the citation names. Walk back over blanks to
        # find it rather than assuming a fixed offset -- assuming one line put
        # R4's renumbered start two lines late in the control fixture, which is
        # how this was caught.
        j = start - 1
        while j >= 1 and v1[j - 1].strip() == "":
            j -= 1
        if j >= 1 and HEADING.match(v1[j - 1]):
            start = j
        print(f"  DRIFT    {rid}: cites {a}-{b}, actually {start}-{end}"
              f"{' — renumbering' if fix else ''}")
        drift.append((rid, cite.group(1), a, b, start, end))

    if fix and drift:
        for _rid, prefix, a, b, start, end in drift:
            old = f"{prefix}{a}-{b}"
            assert text.count(old) == 1, f"{_rid}: anchor not unique"
            text = text.replace(old, f"{prefix}{start}-{end}", 1)
        with open(RULES, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"\n  renumbered {len(drift)} citation(s); re-run to confirm")
        return 1

    total = ok + len(drift) + len(frag)
    print(f"\n  {ok}/{total} citations byte-identical to the v1 range they cite.")
    if drift:
        print(f"  {len(drift)} pointer drift — re-run with --fix to renumber.")
    if frag:
        print(f"  {len(frag)} fragmented ({', '.join(frag)}) — needs re-extraction, "
              f"which is a content decision and is NOT automated.")
    if not drift and not frag:
        print("  Checked: every R-section's Source: range. Not checked: whether the "
              "reproduced text is still the RIGHT excerpt for the rule.")
    return 0 if not drift and not frag else 1


if __name__ == "__main__":
    sys.exit(main())
