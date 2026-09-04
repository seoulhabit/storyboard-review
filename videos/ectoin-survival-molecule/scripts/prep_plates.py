#!/usr/bin/env python3
"""Prepare assets/plates/*.jpg|mp4 from assets/plates/raw/ + the catalog.

Every plate is normalised to 1920x1080; videos to 30fps, silent, H.264 CRF 18,
and PADDED (last frame cloned) to at least `target` seconds so a
`<video class="clip" data-duration=...>` never runs out under its scene.
`speed` < 1 slows the clip (minterpolate for smooth motion), > 1 speeds it up.

    python3 scripts/prep_plates.py            # everything whose raw exists
    python3 scripts/prep_plates.py V03 I02    # by prefix
"""
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "assets" / "plates" / "raw"
OUT = ROOT / "assets" / "plates"
CAT = ROOT.parent.parent / "catalog"

# (out_name, raw_source, target_seconds, speed)
VIDEOS = [
    ("V01-saltlake.mp4",  RAW / "V01-saltlake.mp4",  6.4,  0.85),
    ("V02-dive.mp4",      RAW / "V02-dive.mp4",      3.8,  1.60),
    ("V03-orbit.mp4",     RAW / "V03-orbit.mp4",     6.4,  1.20),
    ("V05-bottle.mp4",    RAW / "V05-bottle.mp4",    7.8,  0.80),
    ("V06-colony.mp4",    RAW / "V06-colony.mp4",    11.4, 0.80),
    ("V07-osmosis.mp4",   RAW / "V07-osmosis.mp4",   10.0, 0.85),
    ("V08-hydration.mp4", RAW / "V08-hydration.mp4", 11.2, 0.80),
    ("V10-escape.mp4",    RAW / "V10-escape.mp4",    7.8,  0.85),
    ("V11-stabilise.mp4", RAW / "V11-stabilise.mp4", 17.6, 0.60),
    ("V12-turn.mp4",      RAW / "V12-turn.mp4",      9.6,  1.00),
    ("V13-serum.mp4",     RAW / "V13-serum.mp4",     5.6,  1.00),
    ("V14-toner.mp4",     RAW / "V14-toner.mp4",     5.4,  1.00),
    ("V15-sunscreen.mp4", RAW / "V15-sunscreen.mp4", 8.2,  0.70),
]
STILLS = [
    ("I01-saltlake.jpg", RAW / "I01-saltlake.png"), ("I02-droplet.jpg", RAW / "I02-droplet.png"),
    ("I03-bacterium.jpg", RAW / "I03-bacterium.png"), ("I04-bottle-droplet.jpg", RAW / "I04-bottle-droplet.png"),
    ("I11-shrivel.jpg", RAW / "I11-shrivel.png"), ("I12-hydration.jpg", RAW / "I12-hydration.png"),
    ("I13-droplet-bottle.jpg", RAW / "I13-droplet-bottle.png"), ("I14-pinkpond.jpg", RAW / "I14-pinkpond.png"),
    ("I15-colony.jpg", RAW / "I15-colony.png"), ("I16-barrier-calm.jpg", RAW / "I16-barrier-calm.png"),
    ("I17-barrier-stressed.jpg", RAW / "I17-barrier-stressed.png"), ("I18-bottle-front.jpg", RAW / "I18-bottle-front.png"),
    ("I19-bottle-back.jpg", RAW / "I19-bottle-back.png"), ("I20-serum.jpg", RAW / "I20-serum.png"),
    ("I21-toner.jpg", RAW / "I21-toner.png"), ("I22-sunscreen.jpg", RAW / "I22-sunscreen.png"),
    ("I23-glycerin.jpg", RAW / "I23-glycerin.png"), ("I24-membrane.jpg", RAW / "I24-membrane.png"),
    ("I25-suntube.jpg", RAW / "I25-suntube.png"), ("I26-recovered.jpg", RAW / "I26-recovered.png"),
    # catalog reuse (verified, unbranded)
    ("C-baseskin.jpg", CAT / "skin-macro-photography" / "04-base-skin.png"),
    ("C-flaking.jpg",  CAT / "skin-macro-photography" / "03-flaking-skin.png"),
    ("C-layering.jpg", CAT / "skin-macro-photography" / "02-layering-hand.png"),
    ("C-flatlay.jpg",  CAT / "product-photography" / "assets" / "C03-01.png"),
    ("C-shelf.jpg",    CAT / "product-photography" / "assets" / "C01-01.png"),
    ("C-serum.jpg",    CAT / "product-photography" / "assets" / "A01-01.png"),
    ("C-tonerpad.jpg", CAT / "product-photography" / "assets" / "A03-01.png"),
]
SCALE = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080"


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                 "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())


def video(out, src, target, speed):
    d = dur(src) / speed
    pad = max(0.0, target - d + 0.2)
    vf = [SCALE]
    if abs(speed - 1.0) > 1e-3:
        vf.append(f"setpts=PTS/{speed}")
    if speed < 0.999:
        vf.append("minterpolate=fps=30:mi_mode=blend")
    else:
        vf.append("fps=30")
    vf.append(f"tpad=stop_mode=clone:stop_duration={pad:.3f}")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-an", "-vf", ",".join(vf),
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-movflags", "+faststart", str(OUT / out)], check=True)
    print(f"  {out:22s} {dur(OUT / out):6.2f}s  (raw {dur(src):.2f}s x{speed} -> target {target})")


def still(out, src):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-vf", SCALE, "-q:v", "2",
                    str(OUT / out)], check=True)
    print(f"  {out}")


def main():
    only = [a for a in sys.argv[1:]]
    def want(name):
        return not only or any(name.startswith(o) for o in only)
    for out, src, target, speed in VIDEOS:
        if want(out) and src.exists():
            video(out, src, target, speed)
    for out, src in STILLS:
        if want(out) and src.exists():
            still(out, src)
    return 0


if __name__ == "__main__":
    sys.exit(main())
