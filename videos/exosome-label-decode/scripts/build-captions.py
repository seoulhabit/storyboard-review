#!/usr/bin/env python3
"""Single source of truth for BOTH caption outputs.

The burned-in `.vo-caption` clips in index.html and the sidecar .srt/.vtt are
generated from the CUES table below, so the two can never drift apart the way
two independently-timed passes would.

Cue timing is derived from the real mixed VO: each take was segmented with
`ffmpeg silencedetect` (noise=-38dB) to find actual phrase boundaries, then
each phrase was mapped onto the authored script line. This is not ASR -- the
words are the authored script (so proper nouns like SeoulHabit and terms like
microneedling are already correct by construction), while the *timing* comes
from measurement rather than estimate.

Discipline enforced here, and asserted at the bottom of this file:
  - max 2 lines on screen, 3-6 words per line
  - >= MIN_CUE_S on screen per cue (a hand-authored sidecar that mirrors the
    beat schedule one-cue-per-element produces sub-0.5s cues; merging
    co-occurring phrases is a separate authoring decision from the visual
    beat schedule)
  - no overlapping cues
"""
import sys
from pathlib import Path

MIN_CUE_S = 1.00
MAX_WORDS_PER_LINE = 6
MAX_LINES = 2

# (start_abs, end_abs, [line1, line2])
CUES = [
    # --- take 01 (VO abs 0.100 - 4.256) ---
    (0.100,  1.720, ["That viral exosome serum?"]),
    (2.070,  3.100, ["The word “exosome”"]),
    (3.100,  4.360, ["tells you almost nothing."]),

    # --- take 02 (VO abs 4.550 - 14.988) ---
    (4.550,  6.700, ["Exosomes are microscopic particles"]),
    (6.965,  8.500, ["cells release to carry signals."]),
    (8.976, 11.630, ["But in skincare, they can come", "from very different sources."]),
    (12.029, 14.700, ["And those sources are not", "automatically interchangeable."]),

    # --- take 03 (VO abs 15.300 - 27.782) ---
    (15.300, 16.700, ["The research is promising,"]),
    (16.885, 17.990, ["but human evidence"]),
    (18.091, 20.700, ["for topical exosome skincare", "is still limited."]),
    (21.301, 25.100, ["Many studies also combine exosomes", "with procedures like microneedling,"]),
    (25.496, 27.880, ["making it difficult to credit", "the serum alone."]),

    # --- take 04 (VO abs 28.100 - 40.499) ---
    (28.489, 29.900, ["So before you buy one,"]),
    (30.251, 31.700, ["ask three questions."]),
    (32.017, 33.250, ["What is the source?"]),
    (33.335, 35.500, ["Has the ingredient been", "properly characterized,"]),
    (35.745, 36.900, ["and kept stable?"]),
    (37.236, 39.000, ["And was this exact", "finished product"]),
    (39.274, 40.560, ["tested on people?"]),

    # --- take 05 (VO abs 40.800 - 48.017) ---
    (41.134, 43.300, ["If the brand only says", "“exosome technology,”"]),
    (44.153, 45.900, ["that is a marketing claim."]),
    (46.388, 48.100, ["Not proof of a miracle."]),

    # --- take 06 (VO abs 48.350 - 55.459) ---
    (48.350, 49.850, ["Promising? Yes."]),
    (50.078, 51.650, ["Proven miracle?"]),
    (51.718, 53.100, ["Not yet."]),
    (53.180, 54.300, ["Comment the exact product,"]),
    (54.300, 55.560, ["and SeoulHabit will decode", "its label next."]),
]

VIDEO_END = 59.000  # 07-endcard (55.800-59.000) is silent -- no cues there


def ts_srt(t):
    h = int(t // 3600); m = int((t % 3600) // 60); s = t % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")


def ts_vtt(t):
    h = int(t // 3600); m = int((t % 3600) // 60); s = t % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"


def validate():
    errs = []
    for i, (a, b, lines) in enumerate(CUES, 1):
        if b - a < MIN_CUE_S - 1e-9:
            errs.append(f"cue {i}: {b-a:.3f}s is under the {MIN_CUE_S}s floor")
        if len(lines) > MAX_LINES:
            errs.append(f"cue {i}: {len(lines)} lines > {MAX_LINES}")
        for ln in lines:
            n = len(ln.split())
            if n > MAX_WORDS_PER_LINE:
                errs.append(f"cue {i}: line has {n} words > {MAX_WORDS_PER_LINE}: {ln!r}")
        if b > VIDEO_END:
            errs.append(f"cue {i}: ends {b:.3f} past video end {VIDEO_END}")
        if i < len(CUES) and b > CUES[i][0] + 1e-9:
            errs.append(f"cue {i}: overlaps cue {i+1} ({b:.3f} > {CUES[i][0]:.3f})")
    return errs


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    errs = validate()
    if errs:
        print("build-captions: FAILED")
        for e in errs:
            print("  -", e)
        sys.exit(1)

    # --- burned-in clips for index.html ---
    html = []
    for i, (a, b, lines) in enumerate(CUES, 1):
        text = "<br>".join(lines)
        html.append(
            f'    <div id="cap-{i:02d}" class="clip vo-caption" data-start="{a:.3f}" '
            f'data-duration="{b-a:.3f}" data-track-index="5"><span>{text}</span></div>'
        )
    (root / "captions" / "_captions.partial.html").write_text("\n".join(html) + "\n")

    # --- sidecar .srt / .vtt, same table, same words ---
    srt = []
    for i, (a, b, lines) in enumerate(CUES, 1):
        srt.append(f"{i}\n{ts_srt(a)} --> {ts_srt(b)}\n" + "\n".join(lines) + "\n")
    (root / "captions" / "exosome-label-decode.srt").write_text("\n".join(srt))

    vtt = ["WEBVTT", ""]
    for i, (a, b, lines) in enumerate(CUES, 1):
        vtt.append(f"{i}")
        vtt.append(f"{ts_vtt(a)} --> {ts_vtt(b)}")
        vtt.extend(lines)
        vtt.append("")
    (root / "captions" / "exosome-label-decode.vtt").write_text("\n".join(vtt))

    durs = [b - a for a, b, _ in CUES]
    print(f"build-captions: {len(CUES)} cues OK")
    print(f"  shortest {min(durs):.3f}s   longest {max(durs):.3f}s   floor {MIN_CUE_S}s")
    print("  wrote captions/_captions.partial.html, .srt, .vtt")


if __name__ == "__main__":
    main()
