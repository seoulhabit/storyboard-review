import json

# One source of truth for both caption outputs (faceless-video-craft's own captions
# production order): the burned-in captions and this .srt both read
# scripts/gen/captions_groups.json, itself built from the corrected per-clip
# assets/voice/*.words.json by build_captions.py. Never hand-time this file.

SLUG = "glass-skin-5-habits"
OUT = f"renders/{SLUG}.srt"

with open("scripts/gen/captions_groups.json") as f:
    data = json.load(f)


def ts(seconds):
    ms = round(seconds * 1000)
    h, ms = divmod(ms, 3600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


lines = []
for i, g in enumerate(data["groups"], start=1):
    lines.append(str(i))
    lines.append(f'{ts(g["start"])} --> {ts(g["end"])}')
    lines.append(g["text"])
    lines.append("")

with open(OUT, "w") as f:
    f.write("\n".join(lines).rstrip() + "\n")

print(f"wrote {OUT}, {len(data['groups'])} cues")
