#!/usr/bin/env python3
"""Audit SFX <audio> elements against their source file's native duration.

Catches the class of bug found in kbeauty-one-percent-line 2026-08-29: an SFX
clip wired in at its full native length outlasts the visual beat it's meant to
punctuate and bleeds into the next, calmer beat (there: glitch-shatter.mp3,
3.5s of sustained noise-bed texture playing under a ~1.7s visual moment).

Deliberately NOT "declared duration matches native duration" — that flags
nearly every ordinary one-shot hit/pop/click in a project, since short SFX are
supposed to play in full; it's noise, not signal (confirmed by running against
this project's other 21 legitimate SFX). The actual signal is duration itself:
one-shot hits, dings, and clicks that punctuate a kinetic-type beat are almost
always well under LONG_SFX_THRESHOLD_S; anything longer is more likely a
sustained texture/wash that can outlive the moment it was cued for. Flags SFX
past that threshold with no volume-automation fade-out trimming them down.

Portable across HyperFrames video projects: run from a project root (where
index.html and compositions/ live), no project-specific paths hardcoded.

Advisory only (exit 0 always) — a long SFX can be intentional; this surfaces
candidates for a human to confirm, the same way hyperframes check's own
info-level findings do.
"""
import glob
import json
import re
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
TOLERANCE_S = 0.05
LONG_SFX_THRESHOLD_S = 3.0

AUDIO_TAG_RE = re.compile(r"<audio\b[^>]*>", re.IGNORECASE)
ATTR_RE = re.compile(r'(\w[\w-]*)\s*=\s*"([^"]*)"')


def ffprobe_duration(path):
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nk=1:nw=1", str(path)],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        return float(out)
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
        return None


def html_unescape_attr(v):
    return (v.replace("&quot;", '"').replace("&amp;", "&")
             .replace("&lt;", "<").replace("&gt;", ">"))


def parse_audio_tags(html_path):
    text = html_path.read_text(errors="ignore")
    for m in AUDIO_TAG_RE.finditer(text):
        tag = m.group(0)
        attrs = {k: v for k, v in ATTR_RE.findall(tag)}
        yield attrs


def has_fadeout_covering(attrs, declared_duration):
    automation = attrs.get("data-automation")
    if not automation:
        return False
    try:
        data = json.loads(html_unescape_attr(automation))
    except (json.JSONDecodeError, TypeError):
        return False
    for lane in data.get("lanes", []):
        if lane.get("target") != "volume":
            continue
        points = lane.get("points", [])
        if not points:
            continue
        last = points[-1]
        # A real fade-out: last automation point lands at/near the clip's own
        # end with volume ~0, and it isn't the very first point (i.e. there's
        # an actual downward ramp, not just a flat silent clip).
        if last.get("v", 1) <= 0.02 and last.get("t", 0) >= declared_duration - TOLERANCE_S and len(points) > 1:
            return True
    return False


def main():
    html_files = [PROJECT_ROOT / "index.html"] + [
        Path(p) for p in glob.glob(str(PROJECT_ROOT / "compositions" / "**" / "*.html"), recursive=True)
    ]
    html_files = [p for p in html_files if p.exists()]

    findings = []
    checked = 0

    for html_path in html_files:
        for attrs in parse_audio_tags(html_path):
            src = attrs.get("src", "")
            if "/sfx/" not in src and not src.startswith("sfx/"):
                continue
            declared = attrs.get("data-duration")
            if declared is None:
                continue
            declared = float(declared)
            asset_path = PROJECT_ROOT / src
            native = ffprobe_duration(asset_path)
            checked += 1
            if native is None:
                continue
            is_long = native >= LONG_SFX_THRESHOLD_S
            if is_long and not has_fadeout_covering(attrs, declared):
                findings.append({
                    "file": str(html_path.relative_to(PROJECT_ROOT)),
                    "id": attrs.get("id", "?"),
                    "src": src,
                    "data_start": attrs.get("data-start", "?"),
                    "declared_duration": declared,
                    "native_duration": round(native, 3),
                })

    print(f"SFX duration audit — {checked} SFX element(s) checked across {len(html_files)} file(s).")
    if not findings:
        print("  no findings.")
        return 0

    print(f"  {len(findings)} finding(s):")
    for f in findings:
        print(f"  - {f['file']}: #{f['id']} <{f['src']}>")
        print(f"      data-start={f['data_start']}  declared={f['declared_duration']}s"
              f"  native={f['native_duration']}s  (>= {LONG_SFX_THRESHOLD_S}s, no fade-out)")
        print("      Verify this SFX doesn't outlast the visual beat it accompanies —"
              " trim data-duration or add a data-automation fade-out if it does.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
