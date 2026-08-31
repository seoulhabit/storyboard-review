import json

CLIP_STARTS = {
    "01": 0.000, "02": 5.260, "03": 10.200, "04": 14.980, "05": 20.640,
}
CLIP_DURATIONS = {  # measured VO duration, used to clamp a clip's last word
    "01": 4.960, "02": 4.640, "03": 4.480, "04": 5.360, "05": 7.040,
}
TOTAL_DURATION = 28.680

# Whisper mis-transcribed "Centella" every time it wasn't the very last word of
# a clean sentence (scintella / sentella / Suntella) -- exactly the proper-noun
# correction pass faceless-video-craft's captions section calls for. Timing
# comes from the ASR (real, measured); only the displayed TEXT is corrected
# here, matching SCRIPT.md verbatim.
TEXT_CORRECTIONS = {
    "01": {0: "Snail", 3: "Centella?"},
    "02": {},
    "03": {5: "Centella", 6: "Asiatica"},
    "04": {0: "Spoiler:", 1: "K-beauty's", 2: "Cica", 5: "Centella"},
    "05": {0: "So:", 1: "Snail", 3: "glow.", 4: "Centella"},
}

# indices (0-based) of the ingredient-identity words within each clip's own word
# list -- reuses the caption-skin mechanism's underline emphasis verbatim
# (videos/snail-mucin-truth/.hyperframes/caption-skin.html via glass-skin-5-habits'
# port), re-flagging ingredient names instead of habit words -- same swap-the-array
# contract the catalog documents for this component, not a new mechanism.
INGREDIENT_WORD_INDEX = {
    "01": [0, 1, 3],   # Snail, mucin, Centella?
    "02": [0, 1],      # Snail, mucin
    "03": [5, 6],      # Centella, Asiatica
    "04": [2, 5],      # Cica, Centella
    "05": [1, 4],      # Snail, Centella
}

all_words = []
for clip in ["01", "02", "03", "04", "05"]:
    with open(f"assets/voice/{clip}.words.json") as f:
        words = json.load(f)
    offset = CLIP_STARTS[clip]
    corrections = TEXT_CORRECTIONS.get(clip, {})
    ingredient_idx = set(INGREDIENT_WORD_INDEX.get(clip, []))
    for i, w in enumerate(words):
        all_words.append({
            "text": corrections.get(i, w["text"]),
            "start": round(w["start"] + offset, 3),
            "end": round(min(w["end"], CLIP_DURATIONS[clip]) + offset, 3),
            "clip": clip,
            "habit": i in ingredient_idx,
        })

# Group into caption phrases: never cross a clip (scene) boundary, cap at 4 words,
# and break early on a >0.35s gap (a natural pause).
groups = []
cur = []
for i, w in enumerate(all_words):
    if cur:
        prev = cur[-1]
        gap = w["start"] - prev["end"]
        crosses_clip = w["clip"] != prev["clip"]
        if crosses_clip or len(cur) >= 4 or gap > 0.35:
            groups.append(cur)
            cur = []
    cur.append(w)
if cur:
    groups.append(cur)

GROUPS = []
for gi, gwords in enumerate(groups):
    GROUPS.append({
        "id": f"caption-group-{gi}",
        "start": gwords[0]["start"],
        "end": gwords[-1]["end"],
        "text": " ".join(w["text"] for w in gwords),
        "words": [
            {"id": f"caption-word-{gi}-{wi}", "text": w["text"], "start": w["start"], "end": w["end"], "habit": w["habit"]}
            for wi, w in enumerate(gwords)
        ],
    })

with open("scripts/gen/captions_groups.json", "w") as f:
    json.dump({"groups": GROUPS, "duration": TOTAL_DURATION}, f, indent=2)

print(f"{len(GROUPS)} caption groups from {len(all_words)} words")
for g in GROUPS:
    print(f'  {g["start"]:>6.2f}-{g["end"]:>6.2f}  "{g["text"]}"')
