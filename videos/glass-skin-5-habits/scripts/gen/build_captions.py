import json

CLIP_STARTS = {
    "01": 0.000, "02": 6.785, "03": 12.476, "04": 19.776, "05": 28.676, "06": 34.026,
}
CLIP_DURATIONS = {  # measured VO duration, used to clamp a clip's last word
    "01": 6.485, "02": 5.391, "03": 7.000, "04": 8.600, "05": 5.050, "06": 6.630,
}
TOTAL_DURATION = 41.526

# indices (0-based) of the habit words within each clip's own word list -- for the
# secondary underline emphasis in captions (the PRIMARY highlight is the habit-word
# stack; this is reinforcement, not a duplicate mechanism).
HABIT_WORD_INDEX = {
    "03": [1, 7],   # cleanse., hydrate.
    "04": [1, 8],   # treat., seal.
    "05": [2],      # protect
}

all_words = []
for clip in ["01", "02", "03", "04", "05", "06"]:
    with open(f"assets/voice/{clip}.words.json") as f:
        words = json.load(f)
    offset = CLIP_STARTS[clip]
    habit_idx = set(HABIT_WORD_INDEX.get(clip, []))
    for i, w in enumerate(words):
        all_words.append({
            "text": w["text"],
            "start": round(w["start"] + offset, 3),
            "end": round(min(w["end"], CLIP_DURATIONS[clip]) + offset, 3),
            "clip": clip,
            "habit": i in habit_idx,
        })

# Group into caption phrases: never cross a clip (scene) boundary, cap at 4 words,
# and break early on a >0.35s gap (a natural pause) -- same grouping intent as the
# ported mechanism's own scene-aware groups, re-derived here since this project's
# transcript comes from `hyperframes transcribe` per-clip, not a bundled captions.mjs.
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
