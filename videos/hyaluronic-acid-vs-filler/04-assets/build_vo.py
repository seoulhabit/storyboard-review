#!/usr/bin/env python3
"""Assemble the single-narrator VO from per-stem takes and emit the master clock.

v3 RETENTION CUT (2026-09-04): rewritten from v1/v2's stretch-to-TARGET model.

v1 (two-hander) and v2 (single narrator, still stretch-fit) both computed one
global `scale` so `speech + sum(gaps) == TARGET` exactly (TARGET was 180.0,
then 160.0). Two problems with that model, found on this project's own repeat
runs and fixed here rather than carried forward:

  1. `scale` had NO GUARD. If a rewrite's speech ever exceeded TARGET, `scale`
     went negative and stems would have been placed with NEGATIVE gaps --
     silently overlapping audio -- with no error anywhere in the pipeline.
  2. It inverts the brief for this cut: "let the measured VO duration drive
     the final timeline; do not stretch it back to" a fixed number. A fixed
     TARGET is precisely the thing not to have.

So v3 uses ABSOLUTE gaps in seconds, chosen once from what v1/v2 realized
naturally (turn gap 0.47-0.52s, section gap 0.84-0.93s measured), not derived
from any target. The total falls out of speech + gaps; nothing stretches to
meet it. `TARGET_BAND` below is purely a post-hoc report against the brief's
120-135s ask -- informational only, never fed back into gap sizing.

Per-stem takes remain the unit (not one continuous take) because v1/v2 already
proved the value: any single line can be re-recorded without touching the
rest, and this is a single narrator now so [S5/C-1]'s old cross-voice
character-offset constraint no longer applies -- stems are split by sentence
group for editability, not because a voice change forces it.

Each stem carries ~1.5-2.5s of fixed head/tail padding from the TTS. Trim each
stem to its speech, then place stems with deliberate absolute gaps.

Emits vo.wav (+ mp3), and vo-timing.json - the master clock [S4/V-2] and the
input [S5/C-1] proportions beats against.
"""
import json, subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
STEMS = json.load(open(os.path.join(HERE, "vo-stems.json")))
VO = os.path.join(HERE, "vo")

# Absolute gaps in seconds -- fixed, not solved for. Values taken from what
# v1's 180s stretch-fit and v2's 160s stretch-fit each realized on their own
# (gap_turn_s 0.469/0.516, gap_section_s 0.844/0.928), rounded to a natural
# reading rhythm rather than re-derived from a target.
GAP_STEM    = 0.50   # base gap between consecutive stems, same section
GAP_SECTION = 1.10   # crossing a spine-section boundary -- a breath, not a beat

# Informational only (brief: 120-135s). Never used to size a gap.
TARGET_BAND = (120.0, 135.0)

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

def main():
    stems = STEMS["stems"]
    missing = [s["id"] for s in stems if not os.path.exists(f"{VO}/s{s['id']:02d}.wav")]
    if missing:
        sys.exit("MISSING STEMS: %s" % missing)

    os.makedirs(f"{VO}/trimmed", exist_ok=True)
    rows, speech = [], 0.0
    for s in stems:
        raw = f"{VO}/s{s['id']:02d}.wav"
        tr  = f"{VO}/trimmed/s{s['id']:02d}.wav"
        d_raw, d_tr = dur(raw), trim(raw, tr)
        rows.append({**s, "raw_s": round(d_raw,3), "trim_s": round(d_tr,3),
                     "trimmed_pad_s": round(d_raw-d_tr,3)})
        speech += d_tr

    # Absolute gaps -- fixed per adjacency, never solved for a target.
    gaps = []
    for i in range(1, len(rows)):
        gaps.append(GAP_SECTION if rows[i]["section"] != rows[i-1]["section"] else GAP_STEM)

    # Guard the model actually needs now that gaps are no longer scaled from
    # a stretch factor: every gap must still be a real, positive silence.
    # (Trivially true for fixed constants, but this is the check that v1/v2's
    # `scale` skipped, and skipping it is exactly how two stems could have
    # ended up silently overlapping.)
    assert all(g > 0 for g in gaps), "computed a non-positive gap: %r" % gaps

    t, timeline = 0.0, []
    for i, r in enumerate(rows):
        timeline.append({"id": r["id"], "v": r["v"], "voice": STEMS["voices"][r["v"]]["character"],
                         "section": r["section"], "start": round(t,3),
                         "dur": r["trim_s"], "end": round(t+r["trim_s"],3),
                         "chars": len(r["text"]), "text": r["text"]})
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

    out = {"gap_stem_s": GAP_STEM, "gap_section_s": GAP_SECTION,
           "speech_s": round(speech,3), "gap_total_s": round(sum(gaps),3),
           "computed_total_s": round(total,3), "measured_total_s": round(measured,3),
           "target_band_s": list(TARGET_BAND),
           "stems": timeline}
    json.dump(out, open(f"{HERE}/vo-timing.json","w"), indent=2)

    print("stems              : %d" % len(rows))
    print("trimmed padding    : %.2fs removed across all stems"
          % sum(r["trimmed_pad_s"] for r in rows))
    print("speech             : %.3fs" % speech)
    print("gaps               : %.3fs total (stem %.2fs / section %.2fs, both fixed)"
          % (sum(gaps), GAP_STEM, GAP_SECTION))
    print("computed total     : %.3fs" % total)
    print("MEASURED vo.wav    : %.3fs   <-- THE MASTER CLOCK, drives the beat sheet" % measured)
    lo, hi = TARGET_BAND
    print("brief's band %.0f-%.0fs : %s (informational -- nothing stretches to it)"
          % (lo, hi, "IN BAND" if lo <= measured <= hi else "OUT OF BAND, script needs a look"))

if __name__ == "__main__":
    main()
