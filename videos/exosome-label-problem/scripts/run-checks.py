#!/usr/bin/env python3
"""Run every post-render check unconditionally and report the aggregate.

The house `postrender` chains its checks with `&&`. That means the first
failing gate silences every check after it: on this project's round-2 render
the safe-area gate failed, so check-cadence never executed, and a reader
skimming the tail of that output would reasonably have concluded cadence was
fine when it had simply never been measured. Each check here runs regardless
of what the previous one returned; only the aggregate decides the exit code,
and only check-safe-area is a hard gate.
"""
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
render = sys.argv[2] if len(sys.argv) > 2 else "renders/exosome-label-problem.mp4"
S = root / "scripts"
SAFE = ["--safe-top","192","--safe-bottom","384","--safe-right","162","--safe-left","72"]

CHECKS = [
    ("blank-frames", [str(S/"check-blank-frames.py"), str(root), render], False),
    ("static-hold",  [str(S/"check-static-hold.py"),  str(root), render], False),
    ("cadence",      [str(S/"check-cadence.py"),      str(root), render], False),
    ("sfx-durations",[str(S/"check-sfx-durations.py"), str(root)],        False),
    ("contrast-px",  [str(S/"check-contrast-pixels.py"), render],         False),
    ("motion-gaps",  [str(S/"check-motion-gaps.py"), render, "--project-root", str(root),
                      "--advisory"],                                       False),
    ("safe-area",    [str(S/"check-safe-area.py"),    str(root), render, *SAFE], True),
]

results = []
for name, cmd, hard in CHECKS:
    print(f"\n{'='*66}\n  {name}{'   [HARD GATE]' if hard else ''}\n{'='*66}")
    r = subprocess.run([sys.executable, *cmd], check=False)
    results.append((name, r.returncode, hard))

print(f"\n{'='*66}\n  SUMMARY\n{'='*66}")
fail_hard = False
for name, code, hard in results:
    tag = "PASS" if code == 0 else ("FAIL" if hard else "findings")
    print(f"  {name:16s} exit={code}  {tag}{'  <- HARD GATE' if hard and code else ''}")
    if hard and code: fail_hard = True
print("\n  Advisory findings are not automatically defects -- confirm each by")
print("  extracting the actual frame before acting on it.")
sys.exit(1 if fail_hard else 0)
