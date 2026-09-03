#!/usr/bin/env python3
"""Assemble the two-voice VO from per-turn stems and emit the master clock.

Why per-turn stems and not one file: [S5/C-1] derives beat start times from a
proportional character offset within a stem. That interpolation cannot cross a
voice change, so a speaker turn is the smallest safely-proportionable unit.

Each stem carries ~1.5-2.5s of fixed head/tail padding from the TTS (measured:
a 4-word Grady line is 3.58s). Concatenating raw stems would let that padding
set the pace. So: trim each stem to its speech, then place turns with DELIBERATE
gaps sized to land the whole thing on the target.

Emits vo.wav (+ mp3), and vo-timing.json - the master clock [S4/V-2] and the
input [S5/C-1] proportions beats against.
"""
import json, subprocess, sys, os, math

HERE = os.path.dirname(os.path.abspath(__file__))
STEMS = json.load(open(os.path.join(HERE, "vo-stems.json")))
VO = os.path.join(HERE, "vo")
TARGET = 160.0
# Gap grammar: a reply to a question lands faster than a new statement.
GAP_SAME_SPEAKER = 0.45   # never used - consecutive turns always change speaker
GAP_TURN         = 1.00   # base inter-speaker beat, scaled below to hit TARGET
GAP_SECTION      = 1.80   # crossing a spine-section boundary

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

    # gap weights, then one global scale so the total lands exactly on TARGET
    weights = []
    for i in range(1, len(rows)):
        weights.append(GAP_SECTION if rows[i]["section"] != rows[i-1]["section"] else GAP_TURN)
    scale = (TARGET - speech) / sum(weights) if sum(weights) else 0.0
    gaps = [w*scale for w in weights]

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

    out = {"target_s": TARGET, "speech_s": round(speech,3),
           "gap_total_s": round(sum(gaps),3), "gap_scale": round(scale,4),
           "gap_turn_s": round(GAP_TURN*scale,3), "gap_section_s": round(GAP_SECTION*scale,3),
           "computed_total_s": round(total,3), "measured_total_s": round(measured,3),
           "stems": timeline}
    json.dump(out, open(f"{HERE}/vo-timing.json","w"), indent=2)

    print("stems              : %d" % len(rows))
    print("trimmed padding    : %.2fs removed across all stems"
          % sum(r["trimmed_pad_s"] for r in rows))
    print("speech             : %.3fs" % speech)
    print("gaps               : %.3fs total (turn %.2fs / section %.2fs)"
          % (sum(gaps), GAP_TURN*scale, GAP_SECTION*scale))
    print("computed total     : %.3fs" % total)
    print("MEASURED vo.wav    : %.3fs   <-- THE MASTER CLOCK" % measured)
    print("target %.0fs +/-15%% : %.1f - %.1f  ->  %s"
          % (TARGET, TARGET*.85, TARGET*1.15,
             "IN TOLERANCE" if TARGET*.85 <= measured <= TARGET*1.15 else "OUT"))

if __name__ == "__main__":
    main()
