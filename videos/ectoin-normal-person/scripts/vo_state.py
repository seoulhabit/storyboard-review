#!/usr/bin/env python3
"""Track which turns have a submitted job and which still need one.

The TTS backend rate-limits hard (429 on ~2/3 of a 12-item batch), so
generation is inherently many small retries. This keeps that bookkeeping out
of the conversation: /tmp/vo/jobs.json maps turn_id -> job_id, and
/tmp/vo/urls.json maps turn_id -> result_url once terminal.

  python3 scripts/vo_state.py            # what is missing
  python3 scripts/vo_state.py --next 6   # emit the next N requests as JSON
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from vo_lines import TURNS

JOBS = Path("/tmp/vo/jobs.json")
URLS = Path("/tmp/vo/urls.json")
VOICE = {"S": ("element", "674b71b8-1d2e-4087-8567-d1f53c0b9f3c"),
         "J": ("preset",  "a3ce02fe-4d3e-55bc-b4d4-a4801b9acdb4")}


def load(p):
    return json.loads(p.read_text()) if p.exists() else {}


def main():
    jobs, urls = load(JOBS), load(URLS)
    todo = [(t, s, x) for t, s, x in TURNS if t not in jobs and t not in urls]

    if "--next" in sys.argv:
        n = int(sys.argv[sys.argv.index("--next") + 1])
        reqs = [{"index": int(t[1:]),
                 "params": {"model": "seed_audio", "prompt": x,
                            "voice_type": VOICE[s][0], "voice_id": VOICE[s][1]}}
                for t, s, x in todo[:n]]
        print(json.dumps(reqs))
        return 0

    print(f"turns {len(TURNS)}  submitted {len(jobs)}  done {len(urls)}  "
          f"todo {len(todo)}")
    if todo:
        print("  next:", " ".join(t for t, _, _ in todo[:12]))
    if jobs:
        print("  awaiting:", " ".join(sorted(jobs)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
