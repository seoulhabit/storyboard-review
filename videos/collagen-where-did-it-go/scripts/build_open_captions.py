#!/usr/bin/env python3
"""Burn the shipped SRT into a second, open-caption master.

    python3 scripts/build_open_captions.py .

WHY THIS EXISTS AS ITS OWN SCRIPT, NOT AN FFMPEG ONE-LINER. This machine's
ffmpeg is built without libass and without freetype (confirmed: `ffmpeg
-filters` lists neither `subtitles` nor `drawtext`), so there is no native
burn-in path -- `-vf subtitles=...` and `-vf drawtext=...` are both
unavailable. This renders each UNIQUE cue's text once as a PNG via PIL
(which does its own font rasterising and needs neither), then composites
each cue onto the clean master with ffmpeg's `overlay` filter, time-gated to
that cue's own span. Compositing PNGs is not a workaround for the missing
filters; it is the same operation `subtitles` would have done, just with the
rasterising step moved to PIL instead of libass.

POSITION. The caption band sits inside the 220-260px reserve
check-caption-overlay.py already simulates (CAPTION_BAND_PX below matches
its own CAPTION_BOTTOM_PX) -- this is the one render where that band is
actually FILLED, by design, so nothing essential may already be sitting in
it. check-caption-overlay.py's own advisory findings on the CLEAN master are
exactly what would collide with this burn-in; review them before publishing
this variant.

THIS IS THE THIRD, FALLBACK DELIVERABLE (see PUBLISH.md): the clean master
plus its sidecar SRT/VTT remains the primary artefact. A viewer can turn a
sidecar track off, resize it, or read it with a screen reader; none of that
is true of an open-caption burn-in. Build this only for a destination that
cannot carry the sidecar track through.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
SLUG = "collagen-where-did-it-go"
SRC = ROOT / "renders" / f"{SLUG}_final.mp4"
OUT = ROOT / "renders" / f"{SLUG}_open-captions.mp4"
SRT = ROOT / "captions" / f"{SLUG}.srt"

CANVAS_W, CANVAS_H = 1920, 1080
CAPTION_BAND_PX = 240          # matches check-caption-overlay.py's own CAPTION_BOTTOM_PX
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_SIZE = 52
LINE_GAP = 14
PAD_X = 60


def ts(s):
    h, m, rest = s.split(":")
    sec, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000


def parse_srt(path):
    raw = path.read_text().strip()
    cues = []
    for block in re.split(r"\n\s*\n", raw):
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue
        a, b = lines[1].split(" --> ")
        cues.append((ts(a), ts(b), lines[2:]))
    return cues


def render_cue_png(lines, out_path):
    from PIL import Image, ImageDraw, ImageFont
    font = ImageFont.truetype(FONT, FONT_SIZE)
    im = Image.new("RGBA", (CANVAS_W, CAPTION_BAND_PX), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    # measure each line, stack bottom-up so a 1-line cue sits low in the band
    # and a 2-line cue grows upward from the same baseline -- matching how a
    # player's own caption track behaves rather than always centring in the
    # full band regardless of line count.
    sizes = [d.textbbox((0, 0), ln, font=font) for ln in lines]
    heights = [b[3] - b[1] for b in sizes]
    total_h = sum(heights) + LINE_GAP * (len(lines) - 1)
    y = CAPTION_BAND_PX - 28 - total_h  # 28px breathing room above the true frame edge

    for ln, (bbox, h) in zip(lines, zip(sizes, heights)):
        w = bbox[2] - bbox[0]
        x = (CANVAS_W - w) // 2
        # a solid backing band, not a per-glyph outline: readable over any
        # ground the clean master ever puts behind it, ink or paper alike.
        d.rectangle([x - PAD_X // 2, y - 6, x + w + PAD_X // 2, y + h + 10],
                    fill=(10, 10, 10, 210))
        d.text((x, y), ln, font=font, fill=(255, 255, 255, 255))
        y += h + LINE_GAP
    im.save(out_path)


def main():
    if not SRC.exists():
        print(f"build_open_captions: {SRC.relative_to(ROOT)} not found -- run npm run render/master first.")
        return 1
    if not SRT.exists():
        print(f"build_open_captions: {SRT.relative_to(ROOT)} not found -- run npm run build first.")
        return 1

    cues = parse_srt(SRT)
    print(f"  {len(cues)} cues -> rendering unique caption images")

    work = ROOT / "renders" / "_captions_tmp"
    work.mkdir(exist_ok=True)
    for f in work.glob("*.png"):
        f.unlink()

    inputs, filters, labels = [], [], []
    prev = "0:v"
    for i, (a, b, lines) in enumerate(cues):
        png = work / f"cue-{i:03d}.png"
        render_cue_png(lines, png)
        inputs += ["-i", str(png)]
        out_label = f"v{i+1}"
        filters.append(
            f"[{prev}][{i+1}:v]overlay=0:{CANVAS_H - CAPTION_BAND_PX}:"
            f"enable='between(t,{a:.3f},{b:.3f})'[{out_label}]"
        )
        prev = out_label
        labels.append(out_label)

    filter_complex = ";".join(filters)
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(SRC), *inputs,
           "-filter_complex", filter_complex, "-map", f"[{prev}]", "-map", "0:a",
           "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
           "-c:a", "copy", str(OUT)]
    print(f"  compositing {len(cues)} time-gated overlays onto the clean master...")
    r = subprocess.run(cmd, capture_output=True, text=True)
    for f in work.glob("*.png"):
        f.unlink()
    work.rmdir()

    if r.returncode != 0:
        print(r.stderr[-3000:])
        return 1
    size_mb = OUT.stat().st_size / 1e6
    print(f"  wrote {OUT.relative_to(ROOT)} ({size_mb:.1f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
