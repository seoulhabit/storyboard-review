#!/usr/bin/env python3
"""Self-contained controls for check-sfx-durations.py (beside this file).

Run after any change to its threshold, its tag parsing, or its fade-out test:

    python3 catalog/tooling/test-sfx-durations-controls.py

Each fixture is a synthetic project -- an index.html plus real audio files of
known length, written to a temp dir and driven through the gate's own CLI, so
the ffprobe path and the HTML parse are both exercised for real rather than
stubbed.

  THRESHOLD       a 4s SFX with no fade MUST flag; a 1s SFX MUST NOT. Both in
                  the same project, so a gate that flagged everything and a
                  gate that flagged nothing each fail one half.

  FADE-OUT        the same 4s SFX with a real volume ramp to zero at its end
                  MUST NOT flag. That is the gate's whole escape hatch: a long
                  sustained texture is fine if it is faded, and a gate that
                  ignored the automation would flag every legitimately-faded
                  wash in a project.

  FADE-OUT, EACH  the fade test is three conditions ANDed -- the last point
  CONDITION       lands at ~zero volume, at ~the clip's end, and is not the
                  only point. Each is checked with the other two satisfied, so
                  dropping any ONE of them fails a control. A single happy-path
                  fixture cannot tell which condition is live and would keep
                  passing with two of the three deleted.

  SRC FILTER      an <audio> that is long but is NOT under an sfx/ path (a
                  music bed, a voice track) MUST be ignored -- the gate is
                  scoped to SFX, and a bed is long by definition.

  ATTRIBUTE ORDER the same long SFX tag written with data-hf-id injected FIRST
                  -- which is exactly what this repo's preview server does to
                  every tag it serves -- MUST still flag. CLAUDE.md records a
                  parser in this repo that silently stopped matching for this
                  reason, and "found nothing" looks identical to "nothing is
                  wrong". This is the control that would catch it here.
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

TOOL = Path(__file__).resolve().parent / "check-sfx-durations.py"


def tone(path, seconds):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi",
                    "-i", f"sine=frequency=440:d={seconds}", "-ar", "44100",
                    "-ac", "1", str(path)], check=True, capture_output=True)


def automation(points):
    lane = {"lanes": [{"target": "volume", "points": points}]}
    return json.dumps(lane).replace('"', "&quot;")


def audio_tag(el_id, src, duration, auto=None, hf_id_first=False):
    attrs = f'id="{el_id}" src="{src}" data-start="0" data-duration="{duration}"'
    if auto:
        attrs += f' data-automation="{auto}"'
    if hf_id_first:
        attrs = f'data-hf-id="hf-9zq1" {attrs}'
    return f"<audio {attrs}></audio>"


def project(tmp, name, tags, assets):
    """assets: {relative path: seconds}."""
    root = Path(tmp) / name
    (root / "sfx").mkdir(parents=True)
    for rel, secs in assets.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        tone(p, secs)
    (root / "index.html").write_text(
        "<html><body>\n" + "\n".join(tags) + "\n</body></html>")
    return root


def run_gate(root):
    r = subprocess.run([sys.executable, str(TOOL), str(root)],
                       capture_output=True, text=True, check=False)
    flagged = set(re.findall(r"#([\w-]+) <", r.stdout))
    return r.stdout, flagged


def check(label, flagged, must, must_not, extra=""):
    good = must <= flagged and not (must_not & flagged)
    print(f"    flagged: {sorted(flagged) or '(none)'}   must flag: {sorted(must) or '(none)'}"
          f"   must not: {sorted(must_not) or '(none)'}")
    print(f"    {'PASS' if good else 'FAIL <-- ' + label}{extra}")
    return good


def main():
    if not TOOL.exists():
        print(f"test-sfx-durations-controls: {TOOL.name} not found beside this fixture -- "
              f"skipping (exit 0).")
        return 0
    import importlib.util
    spec = importlib.util.spec_from_file_location("check_sfx_durations", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    ok = True
    thr = mod.LONG_SFX_THRESHOLD_S
    long_s, short_s = thr + 1.0, 1.0

    with tempfile.TemporaryDirectory() as tmp:
        print(f"\n  THRESHOLD -- a {long_s}s SFX and a {short_s}s one, no fade on either "
              f"(threshold {thr}s):")
        root = project(tmp, "threshold", [
            audio_tag("sfx-long", "sfx/wash.wav", long_s),
            audio_tag("sfx-short", "sfx/tick.wav", short_s),
        ], {"sfx/wash.wav": long_s, "sfx/tick.wav": short_s})
        _, flagged = run_gate(root)
        ok &= check("the duration threshold is broken", flagged, {"sfx-long"}, {"sfx-short"})

        print(f"\n  FADE-OUT -- the same {long_s}s SFX with a real ramp to zero at its end:")
        root = project(tmp, "faded", [
            audio_tag("sfx-faded", "sfx/wash.wav", long_s,
                      auto=automation([{"t": 0.0, "v": 1.0}, {"t": long_s, "v": 0.0}])),
        ], {"sfx/wash.wav": long_s})
        _, flagged = run_gate(root)
        ok &= check("a properly faded long SFX is still being flagged", flagged,
                    set(), {"sfx-faded"})

        print("\n  FADE-OUT, EACH CONDITION -- three near-misses, each satisfying the "
              "other two:")
        root = project(tmp, "nearmiss", [
            # ramps down but only to 0.5 -- not silent at the end
            audio_tag("nm-not-silent", "sfx/wash.wav", long_s,
                      auto=automation([{"t": 0.0, "v": 1.0}, {"t": long_s, "v": 0.5}])),
            # reaches zero, but a full second before the clip ends
            audio_tag("nm-early", "sfx/wash.wav", long_s,
                      auto=automation([{"t": 0.0, "v": 1.0}, {"t": long_s - 1.0, "v": 0.0}])),
            # a single point at zero: a flat silent clip, not a ramp
            audio_tag("nm-single", "sfx/wash.wav", long_s,
                      auto=automation([{"t": long_s, "v": 0.0}])),
        ], {"sfx/wash.wav": long_s})
        _, flagged = run_gate(root)
        ok &= check("a near-miss automation is being accepted as a fade-out -- one of the "
                    "three conditions is no longer live", flagged,
                    {"nm-not-silent", "nm-early", "nm-single"}, set())

        print("\n  SRC FILTER -- a long music bed outside sfx/ must be ignored:")
        root = project(tmp, "srcfilter", [
            audio_tag("bed", "music/bed.wav", long_s),
            audio_tag("sfx-long", "sfx/wash.wav", long_s),
        ], {"music/bed.wav": long_s, "sfx/wash.wav": long_s})
        _, flagged = run_gate(root)
        ok &= check("the sfx/ src filter is broken", flagged, {"sfx-long"}, {"bed"})

        print("\n  ATTRIBUTE ORDER -- the same tag with data-hf-id injected first, as the "
              "preview server writes it:")
        root = project(tmp, "hfid", [
            audio_tag("sfx-injected", "sfx/wash.wav", long_s, hf_id_first=True),
        ], {"sfx/wash.wav": long_s})
        out, flagged = run_gate(root)
        good = "sfx-injected" in flagged and "0 SFX element(s) checked" not in out
        ok &= good
        verdict = ("PASS" if good else
                   "FAIL <-- the parser is anchored to attribute order and has stopped "
                   "seeing injected tags")
        print(f"    flagged: {sorted(flagged) or '(none)'}   {verdict}")

    print("\n  All controls behave as expected.\n" if ok else
          "\n  A CONTROL FAILED -- do not trust this gate until it is resolved.\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
