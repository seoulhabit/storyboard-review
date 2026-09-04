#!/usr/bin/env python3
"""Size a beat BEFORE authoring it, not after rendering.

check-cadence.py scores a step as a beat when
    mean|dLuma| over the whole 1920x1080 frame >= 1.0   AND   maxpix >= 40
so a beat's contribution is approximately

    per_step = (frame_area_fraction * luma_delta) / (duration_s * 8fps)

Two ways to get this wrong, both of which happened on this project and each
cost a full 15-minute render:

  1. Sizing by eye. A chip that clearly "appears" to a viewer can be 2% of the
     frame and move 9 luma, which is 0.06 per step -- nothing.
  2. Picking the colour by hue. --mist on --paper reads as a real card and is a
     9-luma step. --coral on --paper looks dramatic and is 106. Only luma counts.
"""
W, H = 1920, 1080


def lin(c):
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luma8(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    # check-cadence reads ffmpeg's gray plane: BT.601 luma, not linear.
    return 0.299 * r + 0.587 * g + 0.114 * b


TOK = {"paper": "#F7F5F0", "ink": "#131516", "ink-soft": "#211F1B",
       "mist": "#F0EBE1", "aqua": "#59B8AE", "moss": "#4F6B52",
       "coral": "#C97A5C", "coral-deep": "#A85A3C", "highlighter": "#E0A32B",
       "celadon": "#93B896", "ink-3": "#9C978D", "rule": "#E3E3E3"}


def beat(w_px, h_px, frm, to, dur, n=1):
    """per-step mean|dLuma| for n elements of w x h going frm -> to over dur."""
    area = (w_px * h_px * n) / (W * H)
    d = abs(luma8(TOK.get(frm, frm)) - luma8(TOK.get(to, to)))
    return area * d / (dur * 8), area * 100, d


if __name__ == "__main__":
    print(f"{'beat':46s} {'area%':>6s} {'dLuma':>6s} {'per-step':>9s}  verdict")
    print("-" * 82)
    cases = [
        ("4 chips 380x64 mist->paper (WHAT I SHIPPED)", 380, 64, "paper", "mist", 0.34, 1),
        ("4 chips 380x64 paper->ink (fix)",             380, 64, "paper", "ink",  0.34, 1),
        ("blend bar 800x74 -> ink",                     800, 74, "mist",  "ink",  0.55, 1),
        ("full panel 840x300 mist->moss",               840, 300, "mist", "moss", 0.60, 1),
        ("full-column wash 840x900 paper->ink",         840, 900, "paper","ink",  0.70, 1),
        ("6 ring rects 26x26 coral->highlighter",        26, 26, "coral","highlighter", 0.80, 6),
        ("22 strands 540x7 leaf->ink",                  540,  7, "#6F8F72", "ink", 0.80, 22),
        ("half-frame flood 960x1080 paper->ink",        960,1080, "paper","ink",  0.60, 1),
    ]
    for name, w, h, a, b, d, n in cases:
        ps, area, dl = beat(w, h, a, b, d, n)
        print(f"{name:46s} {area:6.1f} {dl:6.0f} {ps:9.2f}  "
              f"{'CLEARS' if ps >= 1.0 else 'invisible'}")
