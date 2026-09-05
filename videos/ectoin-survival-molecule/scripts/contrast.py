#!/usr/bin/env python3
"""WCAG contrast for this project's token pairs. Measured, not eyeballed.

PORTED from videos/ectoin-normal-person/scripts/contrast.py after the retention
master shipped 19-limits, 21-verdict and 24-eleven at ~1.3:1 -- paper-white type
rendering BLACK because a wrapper's trailing `#root { color:inherit }` outranked
each scene's own root colour. That defect is a rendered-pixel one and this file
could not have caught it (see the closing note); what this file does catch is
the other half, a token pair that never clears 4.5:1 on the ground it lands on.

Companion: scripts/check-contrast-pixels.py, which measures the render.
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
MIST, CORAL, AQUA, MOSS = "#F0EBE1", "#C97A5C", "#59B8AE", "#4F6B52"
INK_2, INK_2_DARK, INK_3, INK_3_DARK = "#666666", "#8E9293", "#9C978D", "#7C8082"

# Every pair the frame builders actually bind, on the ground it actually lands
# on. The four marked EXPECTED are documentation, not aspiration: they record
# why a token is ground-scoped, and each one has a note saying what replaced it.
CASES = [
    ("paper on ink",              PAPER,      INK,      True),
    ("paper on ink-soft",         PAPER,      INK_SOFT, True),
    ("paper on moss wash",        PAPER,      MOSS,     True),
    ("ink on aqua",               INK,        AQUA,     True),
    ("ink on paper",              INK,        PAPER,    True),
    (".p-body ink-2 on paper",    INK_2,      PAPER,    True),
    (".p-body ink-2 on mist",     INK_2,      MIST,     True),
    (".kicker.on-ink 2-dark/ink", INK_2_DARK, INK,      True),
    (".kicker.on-ink 2-dark/soft",INK_2_DARK, INK_SOFT, True),
    (".inci 2-dark on ink",       INK_2_DARK, INK,      True),
    ("coral on ink-soft",         CORAL,      INK_SOFT, True),
    # EXPECTED failures, kept as the record of why each is ground-scoped:
    ("ink-3-dark on ink-soft",    INK_3_DARK, INK_SOFT, False),  # -> ink-2-dark
    ("ink-3 on paper",            INK_3,      PAPER,    False),  # graphics only
    ("coral on moss wash",        CORAL,      MOSS,     False),  # -> paper + a word
    ("paper on coral",            PAPER,      CORAL,    False),  # large text only
]

if __name__ == "__main__":
    unexpected = []
    for name, fg, bg, want in CASES:
        r = ratio(fg, bg)
        ok = r >= 4.5
        mark = "PASS" if ok else "FAIL"
        note = "" if ok == want else "   <-- UNEXPECTED"
        if ok != want:
            unexpected.append((name, r, want))
        print(f"  {mark}  {r:5.2f}:1  {name:28s} {fg} on {bg}{note}")
    exp = sum(1 for *_x, want in CASES if not want)
    print(f"\n  {len(CASES)} pairs, {exp} of them EXPECTED failures that exist to "
          f"document why a token is ground-scoped.")
    print("  Covered: foreground token vs a FLAT ground.")
    print("  NOT covered: text over a photo, a gradient, a blend-mode layer, or")
    print("               text whose colour is overridden at RENDER time --")
    print("               those must be sampled from rendered pixels")
    print("               (scripts/check-contrast-pixels.py).")
    if unexpected:
        print(f"\n  {len(unexpected)} pair(s) did not behave as recorded:")
        for name, r, want in unexpected:
            print(f"    {name}: {r:.2f}:1, expected {'PASS' if want else 'FAIL'}")
        raise SystemExit(1)
