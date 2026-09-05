#!/usr/bin/env python3
"""What each camera push cuts off the edge of the frame.

A `.world` camera leg with scale > 1 crops a band off all four sides; an x/y
translate slides that band further. A scene laid out edge to edge therefore
loses real content every time the camera leans in -- on this project that
sliced a trial count to "3", a filter chip to "ep only: independent" and the
citation chip "Nutrients 2023" to "trients 2023", none of which any existing
gate could see. Safe-area only looks at reserved zones, static-hold and
motion-gaps only ask whether pixels changed, and the layout audit models
clipping containers rather than the canvas after a camera transform.

This reads every camera leg out of the built compositions, computes the band it
crops, and extracts the settled frame so a person can see what each push threw
away. It reports no verdict, and that is deliberate.

Two pixel metrics were tried and both failed, which is worth recording so the
third person does not write them again:

  * Detail in the outermost pixels of the PUSHED frame. A sliced word only
    touches the frame edge with its one surviving glyph, so "trients 2023"
    scored the same as a diagram line legitimately crossing the same edge.
  * Percent of on-screen ink inside the band, measured just BEFORE the push.
    Area dominates: a 23-tile grid is most of the ink in the evidence scene, so
    slicing four text chips off its edges scored 0.0% while the sun leaving
    frame in the building scene -- which is the shot working as designed --
    scored 13.2%. It ranked the healthy pushes above the broken ones.

The thing that matters is whether the cut content carried meaning, and that is
a judgement, not a measurement. So: read the strip.

  python3 scripts/check-camera-crop.py . renders/x.mp4 [--sheet]
"""
import json
import os
import re
import subprocess
import sys
import tempfile

CW, CH = 1728.0, 972.0
SETTLE = 0.25       # extra beat after a leg ends, so the frame is at rest


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout


def scenes(root):
    """(id, start, duration) for every scene in the root composition."""
    html = open(os.path.join(root, "index.html")).read()
    out = []
    for m in re.finditer(r"<div([^>]*data-composition-id=\"([^\"]+)\"[^>]*)>", html):
        attrs, cid = m.group(1), m.group(2)
        if cid == "main":
            continue
        st = re.search(r"data-start=\"([0-9.]+)\"", attrs)
        du = re.search(r"data-duration=\"([0-9.]+)\"", attrs)
        if st and du:
            out.append((cid, float(st.group(1)), float(du.group(1))))
    return out


def legs(root, cid, start, dur):
    """Every settled camera state in one scene, as (t, scale, x, y, id, start)."""
    path = os.path.join(root, "compositions", "frames", cid + ".html")
    if not os.path.exists(path):
        return []
    src = open(path).read()
    found = []
    pat = r"tl\.(?:to|fromTo)\(\"#world\",\s*(?:\{[^}]*\}\s*,\s*)?\{([^}]*)\}\s*,\s*([0-9.]+)\s*(?:([-+])\s*([0-9.]+))?\s*\)"
    for m in re.finditer(pat, src):
        body, base, sign, off = m.groups()
        t = float(base)
        if sign:
            t += float(off) * (1 if sign == "+" else -1)
        if "yoyo" in body:
            continue                      # a slam returns to where it started
        num = lambda k, d: float(re.search(k + r":(-?[0-9.]+)", body).group(1)) \
            if re.search(k + r":(-?[0-9.]+)", body) else d
        sc, x, y = num("scale", 1.0), num("x", 0.0), num("y", 0.0)
        if sc <= 1.0 and x == 0.0 and y == 0.0:
            continue                      # a home leg crops nothing
        settled = t + num("duration", 0.5) + SETTLE
        if settled >= dur:
            continue                      # lands under the outgoing wipe
        found.append((start + settled, sc, x, y, cid, start + max(t - 0.15, 0.0)))
    return found


def crop_band(sc, x, y):
    """World pixels lost off each side: left, right, top, bottom."""
    vw, vh = CW / sc, CH / sc
    mx, my = (CW - vw) / 2.0, (CH - vh) / 2.0
    return mx + x, mx - x, my + y, my - y


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    sheet = "--sheet" in sys.argv
    root = args[0] if args else "."
    mp4 = args[1] if len(args) > 1 else None
    if not mp4 or not os.path.exists(mp4):
        print("usage: check-camera-crop.py <root> <render.mp4> [--sheet]")
        return 2

    try:
        from PIL import Image
    except ImportError:
        print("Pillow is not available; cannot measure frames.")
        return 2

    all_legs = []
    for cid, st, du in scenes(root):
        all_legs += legs(root, cid, st, du)
    all_legs.sort()
    if not all_legs:
        print("no camera pushes found.")
        return 0

    tmp = tempfile.mkdtemp(prefix="camcrop-")
    rows, shots = [], []
    for i, (t, sc, x, y, cid, _before) in enumerate(all_legs):
        png = os.path.join(tmp, "p%02d.png" % i)
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", "%.3f" % t,
                        "-i", mp4, "-frames:v", "1", "-y", png],
                       capture_output=True)
        if not os.path.exists(png):
            continue
        shots.append(png)
        rows.append((t, cid, sc, crop_band(sc, x, y)))

    w = max(len(r[1]) for r in rows)
    print("  %-7s %-*s %-6s %s" % ("time", w, "scene", "scale",
                                   "world px cut off  left/right/top/bottom"))
    for t, cid, sc, (l, r, tp, bt) in rows:
        print("  %7.2f %-*s %5.2f  %14.0f %6.0f %6.0f %6.0f"
              % (t, w, cid, sc, max(l, 0), max(r, 0), max(tp, 0), max(bt, 0)))

    print("\n  %d camera push(es). No verdict: see the header for why two pixel"
          % len(rows))
    print("  metrics were tried and both ranked healthy pushes above broken ones.")
    print("  Look at the strip and ask, of anything at an edge: was that meant")
    print("  to leave the frame, or did it get sliced?")

    if sheet and shots:
        qc = os.path.join(root, "renders", "qc")
        os.makedirs(qc, exist_ok=True)
        dest = os.path.join(qc, "pushes.png")
        # delete first: a stale strip left on disk is indistinguishable from a
        # fresh one, and reporting "wrote it" because the path exists is how a
        # broken filter graph goes unnoticed for a whole render cycle.
        if os.path.exists(dest):
            os.remove(dest)

        per = 5
        cw = 560
        with Image.open(shots[0]) as im:
            ch = int(round(im.height * cw / im.width))
        tw, th = cw + 6, ch + 6
        rows_n = (len(shots) + per - 1) // per

        ins = []
        for sh_ in shots:
            ins += ["-i", sh_]

        filt = "".join("[%d:v]scale=%d:%d,pad=iw+6:ih+6:3:3:red[s%d];"
                       % (i, cw, ch, i) for i in range(len(shots)))
        rowids = []
        for a in range(rows_n):
            grp = [g for g in range(a * per, (a + 1) * per) if g < len(shots)]
            filt += "".join("[s%d]" % g for g in grp)
            filt += "hstack=%d[h%d];" % (len(grp), a)
            if len(grp) < per:
                # widen the short row rather than feed vstack a mismatch
                filt += "[h%d]pad=%d:%d:0:0:black[r%d];" % (a, per * tw, th, a)
            else:
                filt += "[h%d]null[r%d];" % (a, a)
            rowids.append("r%d" % a)
        if rows_n > 1:
            filt += "".join("[%s]" % r for r in rowids) + "vstack=%d[out]" % rows_n
            last = "[out]"
        else:
            filt = filt.rstrip(";")
            last = "[%s]" % rowids[0]

        r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error"] + ins +
                           ["-filter_complex", filt, "-map", last,
                            "-frames:v", "1", "-y", dest], capture_output=True, text=True)
        if os.path.exists(dest):
            print("  strip: renders/qc/pushes.png (%d frames)" % len(shots))
        else:
            print("  strip FAILED: %s" % (r.stderr.strip().splitlines() or ["?"])[-1])
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
