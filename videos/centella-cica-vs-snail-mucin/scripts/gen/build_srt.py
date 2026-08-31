"""Export the sidecar .srt from the SAME corrected caption data the burned-in
captions are built from (scripts/gen/captions_groups.json) -- one source of
truth for both outputs, per faceless-video-craft's captions section, instead
of a second independently-run raw ASR pass on the final mix (which mangled
"Centella" as "santella" the same way the per-line passes did)."""
import json


def fmt(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = round((t - int(t)) * 1000)
    if ms == 1000:
        ms = 0
        s += 1
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


with open("scripts/gen/captions_groups.json") as f:
    data = json.load(f)

lines = []
for i, g in enumerate(data["groups"], start=1):
    lines.append(str(i))
    lines.append(f'{fmt(g["start"])} --> {fmt(g["end"])}')
    lines.append(g["text"])
    lines.append("")

with open("renders/centella-cica-vs-snail-mucin.srt", "w") as f:
    f.write("\n".join(lines))

print(f'wrote renders/centella-cica-vs-snail-mucin.srt ({len(data["groups"])} cues)')
