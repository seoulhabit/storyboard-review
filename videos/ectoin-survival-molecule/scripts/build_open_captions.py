#!/usr/bin/env python3
"""Burn the positioned captions into a second master (open captions).

The sidecar VTT is the primary deliverable and YouTube displays it reliably.
This exists for the platforms that do not -- an Instagram or TikTok repost of
the same cut, where a selectable track is simply not offered to the viewer.

WHY IT RASTERISES INSTEAD OF USING `subtitles=`. This machine's ffmpeg is a
homebrew build configured without `--enable-libass` and without
`--enable-libfreetype`, so BOTH the `subtitles`/`ass` filters and `drawtext`
are absent -- `ffmpeg -filters | grep subtitles` returns nothing. Rather than
make the deliverable depend on a differently-configured ffmpeg, each cue is
rendered to a full-frame RGBA plate with Pillow (already a dependency of
check-contrast-pixels.py) and composited with `overlay`, which this build does
have. The .ass file is still written next to the sidecars, so a machine with
libass can burn it in one pass if that is ever easier.

It burns from the FINISHED master, so it costs one encode rather than a
re-render, and the clean master stays the file every gate runs on. That
separation matters: check-static-hold.py's CAPTION_BAND_EXCLUDE is False for
this project because it ships sidecar captions, and three sibling projects have
inherited that constant wrongly as True. Point a gate at THIS file and
burned-in text will read as content in the caption band.

Placement comes from the same TOP_CUE_SCENES table build_captions.py uses --
one source for "there is something in the lower third here", not two.

  python3 scripts/build_open_captions.py [master.mp4] [out.mp4]
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from build_captions import SLUG, VTT_TOP

W, H = 1920, 1080
FONT_TTF = ROOT / "assets" / "fonts" / "ttf" / "Inter-800.ttf"
FONT_SIZE = 52
LINE_GAP = 14
PAD_X, PAD_Y = 34, 22
RADIUS = 14
SAFE_BOTTOM = 96                 # inside title-safe
# Top plates clear the kicker band as well as the safe line: several scenes
# set a 36px mono label just under --safe-top, and a caption at 96 sat on it.
SAFE_TOP = 162                   # matches build_captions.VTT_TOP (line:15%)
INK = (19, 21, 22, 232)          # --ink at ~91%: 15.1:1 against the type
PAPER = (247, 245, 240, 255)     # --paper


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
            out.append((secs(m.group(1)), secs(m.group(2)),
                        m.group(3).strip(), b[1:]))
    return out


def secs(t):
    h, m, s = t.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def ass_time(t):
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def write_ass(cues, path):
    """Kept for a machine whose ffmpeg has libass; not used by the burn below."""
    style = (f"Style: Caption,Inter ExtraBold,{FONT_SIZE},&H00F0F5F7,&H00F0F5F7,"
             f"&H00161513,&H1A161513,-1,0,0,0,100,100,0,0,3,10,0,2,96,96,{SAFE_BOTTOM},1")
    lines = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}",
             "WrapStyle: 2", "ScaledBorderAndShadow: yes", "", "[V4+ Styles]",
             "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,"
             "BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,"
             "BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding",
             style, "", "[Events]",
             "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text"]
    for a, b, setting, body in cues:
        an = r"{\an8}" if setting == VTT_TOP else r"{\an2}"
        lines.append(f"Dialogue: 0,{ass_time(a)},{ass_time(b)},Caption,,0,0,0,,"
                     f"{an}" + r"\N".join(body))
    path.write_text("\n".join(lines) + "\n")


def plate(body, top, font, out):
    """One full-frame RGBA plate: the cue, centred, on its own ink card."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    widths, height = [], 0
    for line in body:
        box = d.textbbox((0, 0), line, font=font)
        widths.append(box[2] - box[0])
        height = box[3] - box[1]
    bw = max(widths) + 2 * PAD_X
    bh = len(body) * height + (len(body) - 1) * LINE_GAP + 2 * PAD_Y
    x0 = (W - bw) // 2
    y0 = SAFE_TOP if top else H - SAFE_BOTTOM - bh
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], RADIUS, fill=INK)
    y = y0 + PAD_Y
    for i, line in enumerate(body):
        box = d.textbbox((0, 0), line, font=font)
        d.text(((W - (box[2] - box[0])) // 2 - box[0], y - box[1]), line,
               font=font, fill=PAPER)
        y += height + LINE_GAP
    img.save(out)


def main():
    src = Path(sys.argv[1] if len(sys.argv) > 1
               else f"renders/{SLUG}_a11y-master.mp4")
    dst = Path(sys.argv[2] if len(sys.argv) > 2
               else f"renders/{SLUG}_open-captions.mp4")
    vtt = ROOT / "captions" / f"{SLUG}.vtt"
    for p in (src, vtt, FONT_TTF):
        if not p.exists():
            sys.exit(f"FATAL: missing {p}")

    cues = parse_vtt(vtt.read_text())
    write_ass(cues, ROOT / "captions" / f"{SLUG}.ass")
    font = ImageFont.truetype(str(FONT_TTF), FONT_SIZE)

    tmp = Path(tempfile.mkdtemp(prefix="oc-plates-"))
    try:
        inputs, graph, prev = [], [], "[0:v]"
        for i, (a, b, setting, body) in enumerate(cues):
            png = tmp / f"cue-{i:04d}.png"
            plate(body, setting == VTT_TOP, font, png)
            inputs += ["-i", str(png)]
            lbl = f"[v{i}]"
            graph.append(f"{prev}[{i + 1}:v]overlay=0:0:"
                         f"enable='between(t,{a:.3f},{b:.3f})'{lbl}")
            prev = lbl
        top = sum(1 for c in cues if c[2] == VTT_TOP)
        print(f"  {len(cues)} cue plates ({top} placed top) -> {tmp}")

        cmd = (["ffmpeg", "-y", "-v", "error", "-i", str(src)] + inputs +
               ["-filter_complex", ";".join(graph), "-map", prev, "-map", "0:a",
                "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart",
                str(dst)])
        subprocess.run(cmd, cwd=ROOT, check=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    facts = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                            "format=duration,size", "-of", "default=nw=1", str(dst)],
                           capture_output=True, text=True).stdout.strip()
    print(f"  {dst}\n  {facts}")


if __name__ == "__main__":
    main()
