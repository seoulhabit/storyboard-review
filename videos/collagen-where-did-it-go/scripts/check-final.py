#!/usr/bin/env python3
"""The delivery gate: everything the brief promises, measured on the file that
ships and on the sources that produced it. Exit 1 on any failed row.

    python3 scripts/check-final.py . renders/collagen-where-did-it-go_final.mp4

Every row here is a promise a viewer or the operator can check, so every row is
measured on the DELIVERED artefact rather than on an intermediate:
loudness is decoded back out of the MP4 (a PCM measurement is not what YouTube
normalises), the first word is checked against real audio energy as well as
against the manifest, and the "one narrator" claim is tested by grepping the
generated files for the second speaker this rebuild removed.

Prints a Markdown table for DELIVERY.md.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
sys.path.insert(0, str(ROOT / "scripts"))
from timing import walk                                # noqa: E402

DUR_MIN, DUR_MAX = 120.0, 150.0
FIRST_WORD_MAX = 0.30
LUFS_TARGET, LUFS_TOL, TP_MAX = -14.0, 1.0, -1.0
CUES_MIN, CUES_MAX, CUE_MIN_S = 30, 90, 1.0
SECOND_VOICE = re.compile(r"\bjay\b|soulhabit|dylan|b847bc29", re.I)
GENERATED = ["index.html", "SCRIPT.md", "STORYBOARD.md",
             "captions/collagen-where-did-it-go.srt", "captions/collagen-where-did-it-go.vtt"]


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True)


def probe(path, entries, stream=None):
    cmd = ["ffprobe", "-v", "error"]
    if stream:
        cmd += ["-select_streams", stream]
    cmd += ["-show_entries", entries, "-of", "default=nw=1:nk=1", str(path)]
    return sh(*cmd).stdout.split()


def loudness(path):
    err = sh("ffmpeg", "-nostdin", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-").stderr
    tail = err[err.rindex("Summary:"):] if "Summary:" in err else err
    i = re.search(r"I:\s*(-?[\d.]+)\s*LUFS", tail)
    tp = re.search(r"Peak:\s*(-?[\d.]+)\s*dBFS", tail)
    return (float(i.group(1)) if i else None, float(tp.group(1)) if tp else None)


def band_rms(path, start, dur):
    r = sh("ffmpeg", "-nostdin", "-v", "info", "-ss", f"{start:.3f}", "-t", f"{dur:.3f}",
           "-i", str(path), "-af", "highpass=f=200,lowpass=f=4000,volumedetect", "-f", "null", "-")
    m = re.search(r"mean_volume:\s*(-?[\d.]+|-inf) dB", r.stderr)
    if not m:
        raise SystemExit("check-final: volumedetect produced no mean_volume -- refusing to pass unmeasured")
    return float("-inf") if m.group(1) == "-inf" else float(m.group(1))


def srt_cues(path):
    if not path.exists():
        return []
    out, block = [], []
    for line in path.read_text().splitlines():
        if line.strip() == "":
            if block:
                out.append(block); block = []
        else:
            block.append(line)
    if block:
        out.append(block)
    cues = []
    for b in out:
        m = re.search(r"(\d\d):(\d\d):(\d\d),(\d+)\s*-->\s*(\d\d):(\d\d):(\d\d),(\d+)", "\n".join(b))
        if m:
            g = [int(x) for x in m.groups()]
            cues.append((g[0]*3600+g[1]*60+g[2]+g[3]/1000, g[4]*3600+g[5]*60+g[6]+g[7]/1000))
    return cues


def main():
    render = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    if render and not render.is_absolute():
        render = ROOT / render
    if not render or not render.exists():
        raise SystemExit("usage: check-final.py <project-root> <final.mp4>")
    units, files, total, manifest = walk()
    rows, bad = [], []

    def row(name, got, ok, want):
        rows.append((name, got, "PASS" if ok else "FAIL", want))
        if not ok:
            bad.append(f"{name}: {got} (want {want})")

    dur = float(probe(render, "format=duration")[0])
    row("duration", f"{dur:.3f}s ({int(dur//60)}:{dur%60:05.2f})",
        DUR_MIN <= dur <= DUR_MAX, f"{DUR_MIN:.0f}-{DUR_MAX:.0f}s")
    row("matches root data-duration", f"{abs(dur - total):.3f}s off", abs(dur - total) <= 0.15, "<= 0.15s")

    w, h, fps = probe(render, "stream=width,height,r_frame_rate", "v:0")[:3]
    row("video stream", f"{w}x{h} @ {fps}", (w, h, fps) == ("1920", "1080", "30/1"), "1920x1080 @ 30/1")

    fw = manifest["words"][0]["start"]
    row("first word (manifest)", f"{fw:.3f}s", fw <= FIRST_WORD_MAX, f"<= {FIRST_WORD_MAX}s")
    early, settled = band_rms(render, 0.05, 0.40), band_rms(render, 1.0, 1.0)
    row("speech energy in the first 0.45s", f"{early:.1f} dB vs {settled:.1f} dB at 1-2s",
        early > settled - 12.0, "within 12 dB of the narrated level")

    i, tp = loudness(render)
    row("integrated loudness", f"{i} LUFS", i is not None and abs(i - LUFS_TARGET) <= LUFS_TOL,
        f"{LUFS_TARGET} +/- {LUFS_TOL} LUFS")
    row("true peak", f"{tp} dBTP", tp is not None and tp < TP_MAX, f"< {TP_MAX} dBTP")

    index = (ROOT / "index.html").read_text()
    row("audio groups", str(index.count("<hf-audio-group")), index.count("<hf-audio-group") == 1, "exactly 1")
    nvo = len(re.findall(r'<audio[^>]*src="assets/voice/', index))
    row("narration clips", str(nvo), nvo == 1, "exactly 1 (one master take)")
    row("group membership", str(index.count('data-audio-group="voiceover"')),
        index.count('data-audio-group="voiceover"') == 1, "exactly 1")

    hits = []
    for rel in GENERATED:
        p = ROOT / rel
        if p.exists():
            hits += [f"{rel}:{m.group(0)}" for m in SECOND_VOICE.finditer(p.read_text())]
    for p in sorted((ROOT / "compositions" / "frames").glob("*.html")):
        hits += [f"{p.name}:{m.group(0)}" for m in SECOND_VOICE.finditer(p.read_text())]
    row("second speaker removed", f"{len(hits)} hit(s)" + (f" {hits[:3]}" if hits else ""),
        not hits, "0 (BRIEF/DELIVERY may name Jay; generated files may not)")

    fake = [rel for rel in GENERATED + ["index.motion.json"]
            if (ROOT / rel).exists() and "FAKE" in (ROOT / rel).read_text()]
    fake += [p.name for p in (ROOT / "compositions" / "frames").glob("*.html") if "FAKE" in p.read_text()]
    row("no FAKE manifest banner", f"{len(fake)} file(s) {fake[:3]}", not fake and manifest.get("source") != "fake",
        "0, and manifest source != fake")

    hf = index.count("data-hf-id") + sum(p.read_text().count("data-hf-id")
                                         for p in (ROOT / "compositions" / "frames").glob("*.html"))
    row("generated files clean", f"{hf} data-hf-id", hf == 0, "0 (preview server did not rewrite them)")

    cues = srt_cues(ROOT / "captions" / "collagen-where-did-it-go.srt")
    vtt = (ROOT / "captions" / "collagen-where-did-it-go.vtt")
    nvtt = len(re.findall(r"-->", vtt.read_text())) if vtt.exists() else -1
    row("caption cues", f"{len(cues)} srt / {nvtt} vtt", CUES_MIN <= len(cues) <= CUES_MAX and len(cues) == nvtt,
        f"{CUES_MIN}-{CUES_MAX}, srt == vtt")
    short = [c for c in cues if c[1] - c[0] < CUE_MIN_S - 0.01]
    over = [1 for a, b in zip(cues, cues[1:]) if a[1] > b[0] + 0.001]
    row("cue hygiene", f"{len(short)} under {CUE_MIN_S}s, {len(over)} overlapping, "
        f"first {cues[0][0]:.2f}s, last ends {cues[-1][1]:.2f}s" if cues else "no cues",
        bool(cues) and not short and not over and cues[0][0] <= FIRST_WORD_MAX and cues[-1][1] <= dur + 0.5,
        "none short, none overlapping, first <= 0.30s, last within the render")

    blocks = manifest.get("blocks") or []
    # stats_master is measured on the cut master, AFTER the per-block level and
    # brightness match; `stats` describes the raw takes, i.e. what was corrected.
    stats = [b for b in blocks if isinstance(b, dict) and b.get("stats_master")]
    for b in stats:
        b = b.setdefault("stats", b["stats_master"])
    stats = [{"name": b["name"], "stats": b["stats_master"]} for b in stats]
    if len(stats) >= 2:
        # EVERY adjacent pair. With four blocks there are three seams, and the one
        # that separates is not necessarily the first.
        worst, detail = 0.0, []
        for i in range(len(stats) - 1):
            a, b = stats[i]["stats"], stats[i + 1]["stats"]
            dl = abs((a.get("lufs") or 0) - (b.get("lufs") or 0))
            ca, cb = a.get("centroid") or 0, b.get("centroid") or 0
            dc = abs(ca - cb) / max(1.0, ca)
            detail.append(f"{stats[i]['name']}->{stats[i+1]['name']} {dl:.2f}LU/{dc*100:.0f}%")
            worst = max(worst, dl / 2.0, dc / 0.12)
        row("block seam continuity", "; ".join(detail), worst <= 1.0,
            "every seam <= 2.0 LU and <= 12% centroid")
    else:
        rows.append(("block seam continuity", f"{len(blocks)} block(s), no stats recorded", "n/a", "gen_vo verify"))

    print(f"\n| check | measured | result | expected |\n|---|---|---|---|")
    for n, got, res, want in rows:
        print(f"| {n} | {got} | **{res}** | {want} |")
    if bad:
        print(f"\n  {len(bad)} FAILED row(s):")
        for x in bad:
            print(f"    - {x}")
        return 1
    print("\n  Result: the delivered file meets every acceptance row.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
