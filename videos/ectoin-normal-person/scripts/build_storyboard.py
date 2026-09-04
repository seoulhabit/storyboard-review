#!/usr/bin/env python3
"""Regenerate STORYBOARD.md by PARSING index.html and the scene files.

Never hand-edit the timing table. A storyboard whose numbers were typed by hand
stops being a spec the moment one real timing changes, and this project's timings
are derived from measured voiceover, so they change on every retake.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = {  # unit id -> chapter title (payoff-named, never "Part 2")
    "01-bottle": "Turn the bottle around",
    "04-protein": "Give the protein some space",
    "05-skin": "What this actually means for skin",
    "06-trial104": "Does it work on people?",
    "12-bottle": "How to read the bottle",
    "14-notnew": "The honest verdict",
}


def mmss(t):
    return f"{int(t//60)}:{t%60:05.2f}"


def main():
    html = (ROOT / "index.html").read_text()
    root_dur = float(re.search(r'id="root"[^>]*data-duration="([\d.]+)"', html).group(1))
    scenes = []
    for tag in re.findall(r"<div[^>]*\bclass=\"[^\"]*\bscene\b[^\"]*\"[^>]*>", html):
        cid = re.search(r'data-composition-id="([^"]+)"', tag).group(1)
        st = float(re.search(r'data-start="([\d.]+)"', tag).group(1))
        du = float(re.search(r'data-duration="([\d.]+)"', tag).group(1))
        f = ROOT / "compositions" / "frames" / f"{cid}.html"
        beats = len(re.findall(r"\btl\.(?:to|fromTo|set)\(", f.read_text())) if f.exists() else 0
        scenes.append((cid, st, du, beats))

    L = ["# STORYBOARD — Ectoin: the survival molecule", "",
         "**GENERATED — do not hand-edit.** `python3 scripts/build_storyboard.py`",
         "re-derives this from `index.html` and the scene files, so it cannot drift",
         "from what actually renders.", "",
         f"**Canvas** 1920x1080 landscape · **fps** 30 · "
         f"**duration** {mmss(root_dur)} ({root_dur:.3f}s) · **scenes** {len(scenes)}", "",
         "## Chapters", "",
         "Paste-ready for the description. First at 0:00, each >= 10s.", "", "```"]
    for cid, st, _, _ in scenes:
        if cid in CHAPTERS:
            L.append(f"{int(st//60)}:{int(st%60):02d} {CHAPTERS[cid]}")
    L += ["```", "", "## Scene table", "",
          "`beats` counts authored timeline calls. It is an AUTHORING aid only —",
          "an authored tween is not a rendered pixel change, and this project measured",
          "that gap directly. `scripts/check-cadence.py` on the render is the answer.", "",
          "| # | scene | start | dur | beats | beats/s |", "|---|---|---|---|---|---|"]
    for i, (cid, st, du, b) in enumerate(scenes, 1):
        L.append(f"| {i:02d} | `{cid}` | {mmss(st)} | {du:.2f}s | {b} | {b/du:.2f} |")
    tot = sum(b for _, _, _, b in scenes)
    L += ["", f"**{tot} authored beats across {root_dur:.1f}s "
              f"({tot/root_dur:.2f}/s average).**", ""]
    (ROOT / "STORYBOARD.md").write_text("\n".join(L))
    print(f"  STORYBOARD.md: {len(scenes)} scenes, {tot} beats, {mmss(root_dur)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
