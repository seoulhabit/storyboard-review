#!/usr/bin/env python3
"""Assemble the single-narrator VO from per-stem takes and emit the master clock.

v3 REWRITE 2026-09-03: the previous version of this script computed
`scale = (TARGET - speech) / sum(weights)` and stretched every inter-stem gap
by one global factor so the total landed on a preset TARGET to the millisecond.
That inverts the master-clock rule: the voiceover's measured duration is
supposed to be the master clock the rest of the pipeline conforms to, not a
number this script conforms the voiceover's PACING to. A gap-scaler makes the
"master clock" partly a fiction -- the speech is real, but a chunk of the
silence between sentences was manufactured backward from a target runtime.

Fixed here: gaps are placed at fixed, natural durations (GAP_TURN / GAP_SECTION
/ GAP_BEFORE_WARNING below) chosen for how they should FEEL, never solved for.
TARGET_BAND is now advisory only -- printed as a tolerance check, and if the
measured total falls outside it the fix is to edit vo-stems.json (cut or add
a stem) and regenerate, exactly like [S4/V-2] already prescribes for the take
itself. This script never adjusts a gap to chase a number.

Why per-stem takes and not one file: [S5/C-1] derives beat start times from a
proportional character offset within a stem. That interpolation cannot cross a
sentence boundary cleanly if stems are concatenated blind, so a stem is still
the smallest safely-proportionable unit even with a single narrator throughout.

Each stem carries ~1.5-2.5s of fixed head/tail padding from the TTS (measured
on this project's own v2 stems: a 4-word line ran 3.58s raw). Concatenating raw
stems would let that padding set the pace, so: trim each stem to its speech,
then place stems with deliberate, fixed gaps.

Emits vo.wav (+ mp3), and vo-timing.json - the master clock [S4/V-2] and the
input [S5/C-1] proportions beats against.
"""
import json, subprocess, sys, os, math

HERE = os.path.dirname(os.path.abspath(__file__))
STEMS = json.load(open(os.path.join(HERE, "vo-stems.json")))
VO = os.path.join(HERE, "vo")

# Advisory only -- see module docstring. Never fed back into gap sizing.
TARGET_BAND = (150.0, 210.0)   # "~2-3 min", the operator's own chosen band

# Gap grammar, in REAL seconds, chosen for feel and never scaled to hit a number.
GAP_SAME_SPEAKER  = 0.45   # unused -- single narrator throughout, kept for the record
GAP_TURN          = 0.55   # a normal beat change within one spine section
GAP_SECTION       = 1.10   # crossing a spine-section boundary -- a bigger breath
GAP_BEFORE_WARNING = 1.45  # the deliberate pause into the FDA passage (stem 20):
                           # "That's worth putting in very large letters." lands,
                           # then a real beat of silence before the register drops.
GAP_AFTER_WARNING  = 1.00  # let the warning's weight sit before recap resumes.

def dur(p):
    o = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                        "-of","csv=p=0",p],capture_output=True,text=True).stdout.strip()
    return float(o)

def trim(src, dst):
    """Strip leading/trailing silence. -45dB peak; keep 60ms of air either side."""
    subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-af",
        "silenceremove=start_periods=1:start_silence=0.06:start_threshold=-45dB:"
        "detection=peak,areverse,"
        "silenceremove=start_periods=1:start_silence=0.06:start_threshold=-45dB:"
        "detection=peak,areverse",
        "-ar","48000","-ac","1",dst],check=True)
    return dur(dst)

def gap_after(rows, i):
    """Fixed real-seconds gap after rows[i], before rows[i+1]. Deterministic,
    never solved for a target -- see module docstring."""
    a, b = rows[i], rows[i + 1]
    if a["id"] == 19 and b["id"] == 20:
        return GAP_BEFORE_WARNING
    if a["id"] == 20 and b["id"] == 21:
        return GAP_AFTER_WARNING
    return GAP_SECTION if b["section"] != a["section"] else GAP_TURN

def main():
    stems = STEMS["stems"]

    # Stale-asset guard: the exact set of stems the manifest names, no more,
    # no less. A v2->v3 rewrite left 12 orphaned v1 wavs on disk uncaught last
    # time (09-run-report.md claimed they were replaced; they weren't) --
    # this assertion is what would have caught it.
    wanted = {f"s{s['id']:02d}.wav" for s in stems}
    present = {f for f in os.listdir(VO) if f.endswith(".wav")}
    missing = wanted - present
    orphans = present - wanted
    if missing:
        sys.exit("MISSING STEMS: %s" % sorted(missing))
    if orphans:
        sys.exit("ORPHANED STEMS on disk, not named in vo-stems.json: %s "
                  "-- delete them or add them to the script." % sorted(orphans))

    os.makedirs(f"{VO}/trimmed", exist_ok=True)
    rows, speech = [], 0.0
    for s in stems:
        raw = f"{VO}/s{s['id']:02d}.wav"
        tr  = f"{VO}/trimmed/s{s['id']:02d}.wav"
        d_raw, d_tr = dur(raw), trim(raw, tr)
        rows.append({**s, "raw_s": round(d_raw,3), "trim_s": round(d_tr,3),
                     "trimmed_pad_s": round(d_raw-d_tr,3)})
        speech += d_tr

    gaps = [gap_after(rows, i) for i in range(len(rows) - 1)]

    t, timeline = 0.0, []
    for i, r in enumerate(rows):
        timeline.append({"id": r["id"], "v": r["v"], "voice": STEMS["voices"][r["v"]]["character"],
                         "section": r["section"], "start": round(t,3),
                         "dur": r["trim_s"], "end": round(t+r["trim_s"],3),
                         "chars": len(r["text"]), "text": r["text"],
                         **({"plate": r["plate"]} if "plate" in r else {})})
        t += r["trim_s"]
        if i < len(gaps): t += gaps[i]
    total = t

    # concat with silence padding
    parts = []
    for i, r in enumerate(rows):
        parts.append(f"{VO}/trimmed/s{r['id']:02d}.wav")
        if i < len(gaps):
            sp = f"{VO}/trimmed/gap{i:02d}.wav"
            subprocess.run(["ffmpeg","-v","error","-y","-f","lavfi","-i",
                "anullsrc=r=48000:cl=mono","-t",f"{gaps[i]:.4f}",sp],check=True)
            parts.append(sp)
    lst = f"{VO}/trimmed/concat.txt"
    with open(lst,"w") as fh:
        for p in parts: fh.write("file '%s'\n" % os.path.abspath(p))
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",lst,
                    "-ar","48000","-ac","1",f"{HERE}/vo.wav"],check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-i",f"{HERE}/vo.wav","-b:a","192k",
                    f"{HERE}/vo.mp3"],check=True)
    measured = dur(f"{HERE}/vo.wav")

    out = {"speech_s": round(speech,3),
           "gap_total_s": round(sum(gaps),3),
           "gap_turn_s": GAP_TURN, "gap_section_s": GAP_SECTION,
           "gap_before_warning_s": GAP_BEFORE_WARNING, "gap_after_warning_s": GAP_AFTER_WARNING,
           "computed_total_s": round(total,3), "measured_total_s": round(measured,3),
           "target_band_s": list(TARGET_BAND),
           "stems": timeline}
    json.dump(out, open(f"{HERE}/vo-timing.json","w"), indent=2)

    print("stems              : %d" % len(rows))
    print("trimmed padding    : %.2fs removed across all stems"
          % sum(r["trimmed_pad_s"] for r in rows))
    print("speech             : %.3fs" % speech)
    print("gaps               : %.3fs total (fixed: turn %.2fs / section %.2fs / "
          "pre-warning %.2fs / post-warning %.2fs)"
          % (sum(gaps), GAP_TURN, GAP_SECTION, GAP_BEFORE_WARNING, GAP_AFTER_WARNING))
    print("computed total     : %.3fs" % total)
    print("MEASURED vo.wav    : %.3fs   <-- THE MASTER CLOCK, not solved for" % measured)
    lo, hi = TARGET_BAND
    print("advisory band %.0f-%.0fs : %s (informational only -- if OUT, edit "
          "vo-stems.json and regenerate; this script will not stretch a gap to fix it)"
          % (lo, hi, "IN BAND" if lo <= measured <= hi else "OUT OF BAND"))

if __name__ == "__main__":
    main()
