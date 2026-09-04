#!/usr/bin/env python3
"""Download, TRIM, pad and QC the VO takes.

Generation happens through the Higgsfield MCP tool (a Python script cannot call
it) and writes assets/voice/_takes.json as {turn_id: {"url": ...}}. This turns
that into the per-turn WAVs that scripts/timing.py measures.

WHY THE TRIM STEP EXISTS. Measured on the real takes: this engine returns
large and wildly variable LEADING silence -- 0.40s on t001, 1.61s on t067,
1.97s on t061. Scene timing is derived from these durations, so shipping them
untrimmed would put a second of dead air in front of most of the 70 turns and
inflate the runtime by roughly a minute of nothing. `videos/exosome-label-decode`
records a `lead_trimmed` field per take for exactly this reason.

FAIL LOUD, NEVER OPEN. The first version of this file returned 0.0 when
silencedetect emitted no closing event, which made every one of the 70 takes
report "ends mid-word" -- a gate that flags everything is a gate nobody reads.
It now distinguishes three states explicitly: a fully silent take (the TTS
returned nothing -- t030 came back 1.88s of digital silence at -60dB), a take
that ends mid-word, and a healthy one.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOICE = ROOT / "assets" / "voice"
TAKES = VOICE / "_takes.json"
TAIL = 0.250        # uniform trailing silence on every take
LEAD_KEEP = 0.040   # keep a hair of lead so the fade-in has something to open on
NOISE = "-45dB"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vo_lines import TURNS, TEXT, SPEAKER

TERMS = ["ectoin", "Halomonas", "elongata", "extremolyte", "squalane",
         "panthenol", "glycerin", "ceramide", "PubMed", "eczema"]


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True)


def dur(p):
    o = sh("ffprobe", "-v", "error", "-show_entries", "format=duration",
           "-of", "csv=p=0", str(p)).stdout.strip()
    return float(o) if o else 0.0


def silences(p, noise=NOISE):
    """[(start, end_or_None)] -- end is None when silence runs to EOF."""
    r = sh("ffmpeg", "-v", "info", "-i", str(p), "-af",
           f"silencedetect=noise={noise}:d=0.04", "-f", "null", "-")
    out, cur = [], None
    for line in r.stderr.splitlines():
        m = re.search(r"silence_start:\s*([\d.]+)", line)
        if m:
            cur = float(m.group(1))
            continue
        m = re.search(r"silence_end:\s*([\d.]+)", line)
        if m and cur is not None:
            out.append((cur, float(m.group(1))))
            cur = None
    if cur is not None:
        out.append((cur, None))       # ran to EOF -- real trailing silence
    return out


def eof_level(p, window=0.12):
    """Mean volume of the final `window` seconds, in dB.

    THIS is the measurement that answers "does the take end mid-word?", and it
    replaces a silencedetect-event proxy that reported 69 of 70 takes as cut.
    Measured on the real takes, the two populations are unambiguous: a clean
    ending reads -91 dB (digital silence) while a truncated one reads -19 to
    -29 dB, often LOUDER than the file's own average. There is no middle
    cluster, so a single threshold separates them cleanly.
    """
    r = sh("ffmpeg", "-sseof", f"-{window}", "-i", str(p), "-af",
           "volumedetect", "-f", "null", "-")
    m = re.search(r"mean_volume:\s*(-?[\d.]+) dB", r.stderr)
    return float(m.group(1)) if m else 0.0


LIVE_AT_EOF_DB = -45.0   # above this, the last word is still sounding


def analyse(p):
    """(lead, eof_db, is_silent). Explicit about which of the three it is."""
    total = dur(p)
    sil = silences(p)
    is_silent = any(s <= 0.01 and (e is None or e >= total - 0.01)
                    for s, e in sil)
    lead = 0.0
    if sil and sil[0][0] <= 0.01 and sil[0][1] is not None:
        lead = sil[0][1]
    return lead, eof_level(p), is_silent


def main():
    report_only = "--report-only" in sys.argv
    if not TAKES.exists():
        raise SystemExit(f"missing {TAKES}")
    takes = json.loads(TAKES.read_text())
    missing = [t for t, _, _ in TURNS if t not in takes]
    if missing:
        raise SystemExit(f"{len(missing)} turns have no take: {missing[:8]}")

    rows, dead, midword, slow, trims = [], [], [], [], []
    for tid, spk, text in TURNS:
        raw, out = VOICE / f"_raw_{tid}.wav", VOICE / f"{tid}.wav"
        if not report_only:
            if not raw.exists():
                sh("curl", "-sS", "-o", str(raw), takes[tid]["url"])
            lead, eof_db, is_silent = analyse(raw)
            if is_silent:
                dead.append(tid)
                continue                      # do NOT emit a silent take
            if eof_db > LIVE_AT_EOF_DB:
                midword.append((tid, eof_db))
            cut = max(0.0, lead - LEAD_KEEP)
            trims.append((tid, cut))
            pad = TAIL
            sh("ffmpeg", "-v", "error", "-y", "-ss", f"{cut:.3f}", "-i", str(raw),
               "-af", f"apad=pad_dur={pad:.3f}", "-ac", "1", "-ar", "24000",
               str(out))
        if out.exists():
            L = dur(out)
            speech = max(0.01, L - TAIL)
            rows.append((tid, spk, L, len(text.split()) / (speech / 60), text))

    total = sum(r[2] for r in rows)
    print(f"{len(rows)}/{len(TURNS)} takes  {total:.2f}s speech "
          f"({int(total//60)}:{total%60:05.2f}) before scene gaps")
    for spk, name in (("S", "SOULHABIT"), ("J", "JAY")):
        sel = [r for r in rows if r[1] == spk]
        if sel:
            med = sorted(r[3] for r in sel)[len(sel) // 2]
            print(f"  {name:10s} {len(sel):3d} takes  {sum(r[2] for r in sel):7.2f}s"
                  f"  median {med:.0f} wpm")
    if trims:
        tot = sum(c for _, c in trims)
        worst = max(trims, key=lambda x: x[1])
        print(f"  lead trimmed from {sum(1 for _,c in trims if c>0.05)} takes, "
              f"{tot:.1f}s total, worst {worst[0]} at {worst[1]:.2f}s")

    for tid, spk, L, wpm, _ in rows:
        if not (110 <= wpm <= 230):
            slow.append((tid, wpm))

    print("\nterm check -- listen to these; the engine garbles them and garbles")
    print("them DIFFERENTLY per take:")
    for term in TERMS:
        hits = [r[0] for r in rows if term.lower() in r[4].lower()]
        if hits:
            print(f"  {term:12s} {len(hits):2d}  {' '.join(hits[:9])}"
                  f"{' ...' if len(hits) > 9 else ''}")

    bad = 0
    if dead:
        bad += 1
        print(f"\nDEAD -- the engine returned pure silence, REGENERATE: {dead}")
    if midword:
        bad += 1
        print(f"\n{len(midword)} take(s) end mid-word (regenerate, a longer fade "
              f"only mutes a live word faster):")
        for tid, db in midword[:12]:
            print(f"  {tid}  still at {db:.1f} dB at EOF")
    if slow:
        print(f"\n{len(slow)} take(s) outside 110-230 wpm (short lines read slow "
              f"by nature; check only if one sounds wrong):")
        print("  " + "  ".join(f"{t}:{w:.0f}" for t, w in slow[:14]))

    print("\nCovered: pure-silence takes, leading/trailing silence, speaking rate,")
    print("         and which takes carry which domain term.")
    print("NOT covered: whether a term is PRONOUNCED correctly, and whether a")
    print("         reading is well-acted. Both need a human listen.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
