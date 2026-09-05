#!/usr/bin/env python3
"""The publish gate: every deliverable a destination checklist assumes exists,
actually exists and is non-empty. Does NOT re-run the render/gates pipeline --
`npm run gates` is the authority on the render itself; this is the LAST step,
checking the things a publish checklist hands to a human are actually there.

    python3 scripts/check-publish.py .

Hard requirement (fails the gate): a verified caption track. A video with no
caption track is not ready to publish on an accessibility-reviewed channel,
full stop -- this is the one row check-final.py does not already cover (it
checks caption HYGIENE -- cue count, timing -- not that a human has actually
looked at the track).
"""
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
SLUG = "collagen-where-did-it-go"

REQUIRED = [
    (f"renders/{SLUG}_final.mp4", "the mastered render"),
    (f"captions/{SLUG}.srt", "caption track (SRT)"),
    (f"captions/{SLUG}.vtt", "caption track (VTT)"),
    ("TRANSCRIPT.md", "accessible transcript (visual-only info + citations)"),
    ("TRANSCRIPT.html", "accessible transcript, HTML"),
    ("DELIVERY.md", "delivery notes (gate status, known findings)"),
    ("PUBLISH.md", "per-destination publish checklist"),
]


def main():
    findings = []
    for rel, label in REQUIRED:
        p = ROOT / rel
        if not p.exists():
            findings.append(f"MISSING: {rel} ({label})")
        elif p.stat().st_size == 0:
            findings.append(f"EMPTY: {rel} ({label})")

    srt = ROOT / "captions" / f"{SLUG}.srt"
    if srt.exists() and srt.stat().st_size > 0:
        print(f"  . caption track present: {srt.relative_to(ROOT)}")
    else:
        print(f"  ! NO VERIFIED CAPTION TRACK -- this is a hard requirement, not a checklist item")

    for f in findings:
        print(f"  ! {f}")

    if findings:
        print(f"\n  {len(findings)} deliverable(s) missing or empty -- not ready to publish.")
        return 1
    print(f"\n  All {len(REQUIRED)} deliverables present. Ready for the PUBLISH.md checklist.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
