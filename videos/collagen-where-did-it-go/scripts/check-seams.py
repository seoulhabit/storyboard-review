#!/usr/bin/env python3
"""Every transition seam, from the SOURCE and from a finished render.

    python3 scripts/check-seams.py . --source
    python3 scripts/check-seams.py . --render renders/<file>.mp4

--source is cheap and needs no render. It asserts the three things the seam
grammar promises and nothing downstream re-checks:

  * the incoming unit's first word lands at seam + d - j (transitions.KIND),
    within 20ms. gen_vo.py `cut` INSERTS that silence; timing.walk() asserts
    the manifest agrees; this asserts the SEAM TABLE build_index.py wrote
    agrees too, so a hand-edited index.seams.json cannot pass unnoticed.
  * the master really is quiet across each seam window -- measured on
    assets/voice/master.wav, not assumed from the edit list.
  * every iris centre is inside the safe box. An iris that opens off the safe
    line reveals the incoming file from a point the viewer cannot see, and no
    pixel gate can tell you why the transition read as a cut.

--render adds what only decoded pixels can answer: at each seam midpoint BOTH
files must be visible. A wipe whose midpoint matches either neighbour is a cut
or a stall wearing a wipe's timing, and the layout auditor -- which does not
model clip-path -- will never say so.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else ".").resolve()
sys.path.insert(0, str(ROOT / "scripts"))
from timing import walk, LEAD_KEEP, MASTER            # noqa: E402
from transitions import KIND                          # noqa: E402

W, H = 1920, 1080
SAFE = (96, 54, 1920 - 96, 1080 - 108)     # left, top, right, bottom
GRAMMAR_TOL = 0.02
SEAM_QUIET_DBFS = -40.0        # what counts as a pause inside the seam window
SEAM_QUIET_MIN_S = 0.10        # how much of the window has to be that quiet
MID_PSNR_MAX = 30.0            # above this the midpoint IS one of its neighbours
MID_STDDEV_MIN = 12.0          # below this the midpoint is blank
EXPECT_KINDS = {"iris": 4, "invert": 2, "curtain": 1}


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True)


def quiet_span(path, start, dur):
    """The longest continuous quiet stretch inside a seam window, in seconds.

    A seam window is NOT all silence and was never meant to be: it is the
    outgoing word's tail, then inserted digital silence, then the incoming
    word's lead-in. Averaging the whole window therefore measures the words on
    either side of the pause and reports every healthy seam as a failure --
    which is exactly what it did, on four of seven. What the viewer needs is a
    real pause somewhere in there, so that is what gets measured."""
    r = sh("ffmpeg", "-nostdin", "-v", "info", "-ss", f"{start:.3f}", "-t", f"{dur:.3f}",
           "-i", str(path), "-af", f"silencedetect=noise={SEAM_QUIET_DBFS}dB:d=0.03",
           "-f", "null", "-")
    spans, cur = [], None
    for line in r.stderr.splitlines():
        m = re.search(r"silence_start:\s*(-?[\d.]+)", line)
        if m:
            cur = float(m.group(1)); continue
        m = re.search(r"silence_end:\s*([\d.]+)", line)
        if m and cur is not None:
            spans.append(float(m.group(1)) - cur); cur = None
    if cur is not None:
        spans.append(max(0.0, start + dur - cur))
    return max(spans) if spans else 0.0


def frame(render, t):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(render),
                        "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                       capture_output=True)
    if len(r.stdout) < W * H:
        return None
    return np.frombuffer(r.stdout[:W * H], dtype=np.uint8).reshape(H, W).astype(np.int16)


def psnr(a, b):
    mse = float(np.mean((a - b) ** 2))
    return 99.0 if mse <= 1e-9 else 10.0 * np.log10(255.0 ** 2 / mse)


def load_seams():
    p = ROOT / "index.seams.json"
    if not p.exists():
        raise SystemExit("index.seams.json missing -- run scripts/build_index.py")
    return json.loads(p.read_text())


def check_source(seams, files):
    """`seams` keys are composition FILE cids; a file's first/last unit carries
    the words the grammar is asserted against (timing.FILE_NAMES renames one)."""
    bad = []
    by_cid = {f.cid: f for f in files}
    kinds = {}
    print("  seam grammar (first word = seam + d - j) and measured seam quiet:")
    for s in seams:
        kinds[s["kind"]] = kinds.get(s["kind"], 0) + 1
        d, seam_after, j, gap = KIND[s["kind"]]
        u = by_cid[s["into"]].units[0]
        quiet = "-"
        if u.first_word_abs is not None:
            want = s["seam"] + d - j
            got = u.first_word_abs
            if abs(got - want) > GRAMMAR_TOL:
                bad.append(f"{s['from']} -> {s['into']}: first word {got:.3f}s, grammar wants "
                           f"{want:.3f}s ({s['kind']}: seam {s['seam']:.3f} + d {d} - j {j})")
            prev_end = by_cid[s["from"]].units[-1].last_word_abs
            win = max(0.05, got - LEAD_KEEP - prev_end)
            if MASTER.exists():
                q = quiet_span(MASTER, prev_end, win)
                quiet = f"{q:5.2f}s quiet"
                if q < SEAM_QUIET_MIN_S:
                    bad.append(f"{s['from']} -> {s['into']}: seam window {prev_end:.2f}-"
                               f"{prev_end + win:.2f}s has only {q:.2f}s below "
                               f"{SEAM_QUIET_DBFS} dBFS (want >= {SEAM_QUIET_MIN_S}s) -- "
                               f"no audible pause at the transition")
        if s["kind"] == "iris":
            x, y = s["iris_at"] or (None, None)
            if x is None:
                bad.append(f"{s['into']}: iris boundary with no centre")
            elif not (SAFE[0] <= x <= SAFE[2] and SAFE[1] <= y <= SAFE[3]):
                bad.append(f"{s['into']}: iris centre ({x:.0f},{y:.0f}) outside the safe box {SAFE}")
        print(f"    {s['from']:14s} -> {s['into']:14s} {s['kind']:8s} seam {s['seam']:8.3f}  "
              f"gap {gap:.2f}s  quiet {quiet}")
    for k, n in EXPECT_KINDS.items():
        if kinds.get(k, 0) != n:
            bad.append(f"transition grammar: {kinds.get(k, 0)}x {k}, expected {n}x")
    if len(seams) != sum(EXPECT_KINDS.values()):
        bad.append(f"{len(seams)} seams, expected {sum(EXPECT_KINDS.values())}")
    return bad


def check_render(seams, render):
    out = ROOT / "renders" / "qc" / "seams"
    out.mkdir(parents=True, exist_ok=True)
    bad = []
    print(f"\n  seam midpoints on {render.name} (both files must be visible):")
    for s in seams:
        d = s["d"]
        ts = {"out": s["seam"] - 0.05, "mid": s["seam"] + d / 2, "in": s["seam"] + d + 0.05}
        fr = {}
        for name, t in ts.items():
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(render),
                            "-frames:v", "1", str(out / f"{s['from']}__{s['into']}-{name}.png")],
                           capture_output=True)
            fr[name] = frame(render, t)
        if any(v is None for v in fr.values()):
            bad.append(f"{s['into']}: could not decode a seam frame"); continue
        p_out, p_in = psnr(fr["mid"], fr["out"]), psnr(fr["mid"], fr["in"])
        sd = float(fr["mid"].std())
        flag = ""
        if p_out > MID_PSNR_MAX or p_in > MID_PSNR_MAX:
            flag = "  <-- midpoint matches a neighbour: a cut or a stall, not a wipe"
            bad.append(f"{s['from']} -> {s['into']}: midpoint PSNR out {p_out:.1f} / in {p_in:.1f} dB "
                       f"(both must be under {MID_PSNR_MAX})")
        if sd < MID_STDDEV_MIN:
            flag = "  <-- midpoint is near-blank"
            bad.append(f"{s['from']} -> {s['into']}: midpoint luma stddev {sd:.1f} < {MID_STDDEV_MIN}")
        print(f"    {s['from']:14s} -> {s['into']:14s} mid {ts['mid']:7.3f}s  "
              f"PSNR out {p_out:5.1f} in {p_in:5.1f} dB  stddev {sd:5.1f}{flag}")
    print(f"  frames written to {out.relative_to(ROOT)}/")
    return bad


def main():
    argv = sys.argv[1:]
    render = None
    if "--render" in argv:
        render = Path(argv[argv.index("--render") + 1])
        if not render.is_absolute():
            render = ROOT / render
    units, files, total, manifest = walk()
    seams = load_seams()
    bad = []
    if "--source" in argv or render is None:
        bad += check_source(seams, files)
    if render is not None:
        if not render.exists():
            raise SystemExit(f"render not found: {render}")
        bad += check_render(seams, render)
    if manifest.get("source") == "fake":
        print("\n  [VO MANIFEST: FAKE -- seam quiet is synthetic silence by construction]")
    if bad:
        print(f"\n  {len(bad)} finding(s):")
        for b in bad:
            print(f"    - {b}")
        return 1
    print("\n  Result: every seam matches the grammar and is visibly a wipe." if render
          else "\n  Result: every seam matches the grammar.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
