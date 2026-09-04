#!/usr/bin/env python3
"""WCAG contrast for the speaker palette. Measured, not eyeballed.

Attribution is carried by TYPE ALONE in this project (no speaker rails), so
every speaker colour has to clear 4.5:1 against the ACTUAL ground it sits on.
A token that passes on paper can fail on ink and vice versa -- that is exactly
the per-ground trap the predecessor hit with --ink-2 (4.89:1 on paper, 3.44:1
on ink) and the reason the token set carries -dark variants.
"""
def lin(c):
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

def lum(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return 0.2126*lin(r) + 0.7152*lin(g) + 0.0722*lin(b)

def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

PAPER, INK, INK_SOFT = "#F7F5F0", "#131516", "#211F1B"
CORAL, CORAL_DEEP     = "#C97A5C", "#A85A3C"
AQUA, MOSS            = "#59B8AE", "#4F6B52"

CASES = [
    ("SOULHABIT on paper",   INK,        PAPER),
    ("SOULHABIT on ink",     PAPER,      INK),
    ("JAY coral on ink",     CORAL,      INK),
    ("JAY coral on paper",   CORAL,      PAPER),      # expected FAIL
    ("JAY coral-deep/paper", CORAL_DEEP, PAPER),      # the fix
    ("JAY coral-deep on ink", CORAL_DEEP, INK),       # expected FAIL
    ("JAY coral on ink-soft", CORAL,     INK_SOFT),
    ("ink text on aqua wash", INK,       AQUA),
    ("paper text on moss",    PAPER,     MOSS),
]

if __name__ == "__main__":
    bad = 0
    for name, fg, bg in CASES:
        r = ratio(fg, bg)
        ok = "PASS" if r >= 4.5 else "FAIL"
        if r < 4.5:
            bad += 1
        print(f"  {ok}  {r:5.2f}:1  {name:24s} {fg} on {bg}")
    # Scope the summary to what actually ran. A line that states a count the
    # run did not produce is how a checker ships a false all-clear.
    exp = sum(1 for n, _, _ in CASES if "coral on paper" in n or "coral-deep on ink" in n)
    print(f"\n  {bad} of {len(CASES)} below 4.5:1; {exp} of those are EXPECTED "
          f"fails that exist to document why each coral is ground-scoped.")
    print("  Covered: foreground token vs a FLAT ground.")
    print("  NOT covered: text over a photo, a gradient, or a blend-mode layer --")
    print("               those must be sampled from rendered pixels, not tokens.")
