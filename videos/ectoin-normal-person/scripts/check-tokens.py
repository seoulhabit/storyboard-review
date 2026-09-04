#!/usr/bin/env python3
"""Guard the inlined token block against its source of truth.

Tokens are INLINED into every scene rather than linked -- a <link> to
assets/tokens/tokens.css is confirmed not to resolve custom properties through
this render pipeline. That is safe only because the inlining is GENERATED from
one constant. This check is what keeps it honest.

The failure it exists to catch is SILENT: an inlined block that omits a token a
scene actually uses makes the calc() invalid, so CSS drops the whole
declaration -- no error, no lint finding, just wrong geometry. It cost the
predecessor 41 frames of end-screen intrusion, and the one-command diagnosis
(`grep -c endscreen` -> 3 in tokens.css, 0 in the inlined block) is invisible
from reading either file alone.

Run before every build.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import _preamble as P

# Tokens that MUST be inlined even though few scenes read them. Each of these
# is consumed inside a calc(), which is what makes an omission silent.
REQUIRED = ["--endscreen-right", "--endscreen-bottom", "--safe-top",
            "--safe-bottom", "--safe-left", "--safe-right", "--safe-margin",
            "--coral", "--coral-deep"]


def main():
    css = (ROOT / "assets" / "tokens" / "tokens.css").read_text()
    inlined = set(re.findall(r"(--[a-z0-9-]+)\s*:", P.TOKENS))
    source = set(re.findall(r"(--[a-z0-9-]+)\s*:", css))

    bad = 0
    drift = sorted(inlined - source)
    if drift:
        bad += 1
        print(f"FAIL  {len(drift)} token(s) inlined but absent from tokens.css: {drift}")
        print("      tokens.css is the source of truth; add them there or drop them.")

    absent = [t for t in REQUIRED if t not in inlined]
    if absent:
        bad += 1
        print(f"FAIL  required token(s) missing from the inlined block: {absent}")
        print("      These are read inside calc(). An omission fails SILENTLY.")

    # Any token a scene file references must be inlined. Scene files are
    # generated, so this catches a css string that reached for a token the
    # preamble does not carry.
    frames = sorted((ROOT / "compositions" / "frames").glob("*.html"))
    for f in frames:
        used = set(re.findall(r"var\((--[a-z0-9-]+)", f.read_text()))
        gap = sorted(used - inlined)
        if gap:
            bad += 1
            print(f"FAIL  {f.name} uses token(s) the inlined block lacks: {gap}")

    print(f"\n  inlined {len(inlined)}  |  tokens.css {len(source)}  |  "
          f"{len(frames)} scene file(s) scanned")
    print("  Covered: inlined-vs-source drift, required calc() tokens, per-scene use.")
    print("  NOT covered: whether a token's VALUE is right for its ground --")
    print("               that is scripts/contrast.py, and it needs the ground.")
    if bad == 0:
        print("\n  No token drift.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
