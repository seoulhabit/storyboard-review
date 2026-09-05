#!/usr/bin/env python3
"""Burn the positioned captions into a second master (open captions).

The sidecar VTT is the primary deliverable and YouTube displays it reliably.
This exists for the platforms that do not -- an Instagram or TikTok repost of
the same cut, where a selectable track is simply not offered to the viewer.

It burns from the FINISHED master, so it costs one ffmpeg pass rather than a
re-render, and the clean master stays the file every gate runs on. That
separation matters: check-static-hold.py's CAPTION_BAND_EXCLUDE is False for
this project because it ships sidecar captions, and three sibling projects
have inherited that constant wrongly as True. Point a gate at THIS file and
burned-in text will read as content in the caption band.

Placement comes from the same TOP_CUE_SCENES table build_captions.py uses --
one source for "there is something in the lower third here", not two.

  python3 scripts/build_open_captions.py [master.mp4] [out.mp4]
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from build_captions import SLUG

# ASS is the burn-in format because it is the only one libass positions
# reliably per cue. \an8 = top-centre, \an2 = bottom-centre.
FONT = "Inter"
FONT_SIZE = 54          # 1080p; ~5% of frame height, comfortably above the floor
MARGIN_V = 96           # inside title-safe on both edges
STYLE = (f"Style: Caption,{FONT},{FONT_SIZE},&H00F5F7F7,&H00F5F7F7,&H00161513,"
         f"&HC0161513,-1,0,0,0,100,100,0,0,3,0,4,2,96,96,{MARGIN_V},1")


def parse_vtt(text):
    cues, block = [], []
    for line in text.splitlines():
        if line.strip() == "":
            if block:
                cues.append(block)
                block = []
        elif line.strip() != "WEBVTT":
            block.append(line)
    if block:
        cues.append(block)
    out = []
    for b in cues:
        m = re.match(r"([\d:.]+)\s+-->\s+([\d:.]+)(.*)$", b[0])
        if m:
            out.append((m.group(1), m.group(2), m.group(3).strip(), b[1:]))
    return out


def ass_time(t):
    h, m, s = t.split(":")
    return f"{int(h)}:{int(m):02d}:{float(s):05.2f}"


def main():
    src = Path(sys.argv[1] if len(sys.argv) > 1
               else f"renders/{SLUG}_a11y-master.mp4")
    dst = Path(sys.argv[2] if len(sys.argv) > 2
               else f"renders/{SLUG}_open-captions.mp4")
    vtt = ROOT / "captions" / f"{SLUG}.vtt"
    for p in (src, vtt):
        if not p.exists():
            sys.exit(f"FATAL: missing {p}")

    cues = parse_vtt(vtt.read_text())
    lines = [
        "[Script Info]", "ScriptType: v4.00+", "PlayResX: 1920", "PlayResY: 1080",
        "WrapStyle: 2", "ScaledBorderAndShadow: yes", "",
        "[V4+ Styles]",
        "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,"
        "BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,"
        "BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding",
        STYLE, "",
        "[Events]",
        "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text",
    ]
    top = 0
    for a, b, setting, body in cues:
        an = r"{\an8}" if setting.startswith("line:10%") else r"{\an2}"
        top += setting.startswith("line:10%")
        text = r"\N".join(body)
        lines.append(f"Dialogue: 0,{ass_time(a)},{ass_time(b)},Caption,,0,0,0,,{an}{text}")
    ass = ROOT / "captions" / f"{SLUG}.ass"
    ass.write_text("\n".join(lines) + "\n")
    print(f"  {len(cues)} cues -> {ass.relative_to(ROOT)} ({top} placed top)")

    # Video is re-encoded (burning changes pixels); audio is copied untouched,
    # so the mastered loudness of the clean file carries over exactly.
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(src),
           "-vf", f"subtitles={ass.relative_to(ROOT)}",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18",
           "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", str(dst)]
    subprocess.run(cmd, cwd=ROOT, check=True)
    got = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "format=duration,size", "-of", "default=nw=1", str(dst)],
                         capture_output=True, text=True).stdout.strip()
    print(f"  {dst.relative_to(ROOT)}\n  {got}")


if __name__ == "__main__":
    main()
