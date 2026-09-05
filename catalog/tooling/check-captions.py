#!/usr/bin/env python3
"""Gate the SHIPPED caption sidecars: reading speed, line discipline, spelling.

WHY THE SHIPPED FILE AND NOT THE BUILD. A caption builder prints its own line
counts and floors as it runs, and a builder that is never re-run prints nothing
at all. The .srt/.vtt are what the viewer gets, so they are what this reads.

WHAT IT CATCHES, from two projects that arrived at it independently:

  * READING SPEED. A cue can satisfy every line rule and still be unreadable:
    42 characters held for 1.4s is 30 CPS, roughly double a comfortable rate.
    `videos/collagen-where-did-it-go` found a whole section like this.
  * LINE DISCIPLINE. A cue packer capped on WORD COUNT produces a 55-character
    line the moment the words are long; a word count is not a line length.
    Both projects shipped that bug.
  * TERM SPELLING, case-SENSITIVELY. This is the one most worth having. An
    ASR-derived caption track quietly substitutes its best guess for exactly
    the vocabulary a technical channel depends on -- a company styled lowercase
    comes back capitalised, a molecule comes back as a homophone, a brand comes
    back as a different word entirely. A case-insensitive check passes all
    three. `videos/ectoin-survival-molecule` shipped "Bitop" for "bitop" and
    would have shipped "Abbey" for "Abib".
  * PLACEMENT. Where a project positions cues, every cue must actually carry a
    setting -- one that silently lost its positioning still looks fine in the
    file and lands on a chart in the player.

FIELD CONTRACT
    python3 check-captions.py <project_root> --slug <slug>
        [--captions-dir captions] [--format srt|vtt|both]
        [--max-line-chars 42] [--max-lines 0]        # 0 = off
        [--min-cue-s 1.0]
        [--max-cps-hard 0] [--max-cps-pref 0] [--pref-fraction 0.95]
        [--require-cue-settings] [--top-setting "line:15%,align:center"]
        [--max-nonspeech 0] [--nonspeech-prefix "["]
        [--terms terms.json]
        [--exempt-window LO-HI]                      # repeatable
        [--advisory]

Every threshold defaults to OFF where projects legitimately differ (max-lines,
CPS, non-speech cap) and to the agreed value where they do not (42 chars, 1.0s).
Turn on what your project has a policy about; a gate asserting a policy the
project never set is noise, and noise is how a gate stops being read.

terms.json is `{"required": ["Halomonas elongata", ...],
                "forbidden": ["Bitop", "ectoene", ...]}` -- substring matches
against the concatenated cue text, case-sensitive. `required` is the vocabulary
a human verified by ear; `forbidden` is the recogniser's known guesses at it.

--exempt-window LO-HI drops CPS findings for cues wholly inside a reviewed
window. It exists because a deliberately fast hook is a real editorial choice,
and the alternative -- raising the ceiling for the whole piece -- hides the
cues that are fast by accident.

Exits non-zero on any finding, unless --advisory. Provenance: independently
built as `check-captions.py` in `videos/collagen-where-did-it-go` (CPS, exempt
windows) and `videos/ectoin-survival-molecule` (line/lines caps, term spelling,
cue settings, non-speech cap) during two accessibility passes that could not see
each other's work.
"""
import argparse
import json
import re
import sys
from pathlib import Path


def secs_srt(s):
    h, m, rest = s.split(":")
    sec, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000


def secs_vtt(s):
    h, m, sec = s.split(":")
    return int(h) * 3600 + int(m) * 60 + float(sec)


def parse_cues(path, kind):
    """-> [(start, end, setting, [lines])]. One shape for both formats."""
    blocks, cur = [], []
    for line in path.read_text().splitlines():
        if line.strip() == "":
            if cur:
                blocks.append(cur)
                cur = []
        elif line.strip() != "WEBVTT":
            cur.append(line)
    if cur:
        blocks.append(cur)

    sep = "," if kind == "srt" else "."
    conv = secs_srt if kind == "srt" else secs_vtt
    pat = re.compile(r"([\d:" + re.escape(sep) + r"]+)\s+-->\s+([\d:" + re.escape(sep) + r"]+)(.*)$")
    out = []
    for b in blocks:
        # SRT blocks open with a bare cue number; VTT blocks may carry an id.
        head = 1 if (b and b[0].strip().isdigit() and len(b) > 1) else 0
        m = pat.match(b[head])
        if not m:
            continue
        out.append((conv(m.group(1)), conv(m.group(2)),
                    m.group(3).strip(), b[head + 1:]))
    return out


def check(cues, a, kind):
    findings, cps_values = [], []
    exempt = [tuple(float(x) for x in w.split("-")) for w in (a.exempt_window or [])]
    for i, (start, end, setting, lines) in enumerate(cues):
        where = f"cue {i+1} ({start:.2f}-{end:.2f}s)"
        dur = end - start
        text = " ".join(lines)
        cps = len(text) / dur if dur > 0 else 999.0
        cps_values.append(cps)

        if dur < a.min_cue_s - 0.005:
            findings.append(f"{where}: {dur:.2f}s, under the {a.min_cue_s:.1f}s floor")
        if a.max_lines and len(lines) > a.max_lines:
            findings.append(f"{where}: {len(lines)} lines (max {a.max_lines}) -- {text!r}")
        for ln in lines:
            if len(ln) > a.max_line_chars:
                findings.append(f"{where}: line is {len(ln)} chars "
                                f"(max {a.max_line_chars}) -- {ln!r}")
        if a.max_cps_hard and cps > a.max_cps_hard:
            if any(lo - 0.05 <= start and end <= hi + 0.05 for lo, hi in exempt):
                print(f"  --exempt-window: {where}, {cps:.1f} CPS, inside a reviewed "
                      f"window -- dropped")
            else:
                findings.append(f"{where}: {cps:.1f} CPS, over the "
                                f"{a.max_cps_hard:.0f} hard ceiling -- {text!r}")
        if a.require_cue_settings and kind == "vtt" and not setting:
            findings.append(f"{where}: no cue setting -- placement is the player's guess")
        if i + 1 < len(cues) and end > cues[i + 1][0] + 0.001:
            findings.append(f"{where}: overlaps cue {i+2} -- ends {end:.3f}s, "
                            f"next starts {cues[i+1][0]:.3f}s")

    body = "\n".join(" ".join(c[3]) for c in cues)
    if a.terms:
        t = json.loads(Path(a.terms).read_text())
        for term in t.get("required", []):
            if term not in body:
                findings.append(f"required term missing or misspelled: {term!r}")
        for term in t.get("forbidden", []):
            if term in body:
                findings.append(f"forbidden spelling present: {term!r}")

    nonspeech = [c for c in cues if c[3] and c[3][0].startswith(a.nonspeech_prefix)]
    if a.max_nonspeech and len(nonspeech) > a.max_nonspeech:
        findings.append(f"{len(nonspeech)} non-speech cues (max {a.max_nonspeech}) -- "
                        f"a decorative transition should not be captioned individually")

    longest = max((len(l) for c in cues for l in c[3]), default=0)
    print(f"  {len(cues)} cues, longest line {longest} chars, "
          f"shortest {min(b - a_ for a_, b, _, _ in cues):.2f}s"
          + (f", worst {max(cps_values):.1f} CPS" if a.max_cps_hard else ""))
    if a.require_cue_settings and kind == "vtt":
        top = sum(1 for c in cues if a.top_setting and c[2] == a.top_setting)
        print(f"  {top} cue(s) carry the top setting; "
              f"{len(nonspeech)} non-speech: {[c[3][0] for c in nonspeech]}")
    if a.max_cps_pref and cps_values:
        frac = sum(1 for c in cps_values if c <= a.max_cps_pref) / len(cps_values)
        print(f"  {frac:.0%} at or under the preferred {a.max_cps_pref:.0f} CPS")
        if frac < a.pref_fraction:
            print(f"  ADVISORY (does not fail): only {frac:.0%} at or under "
                  f"{a.max_cps_pref:.0f} CPS, want >= {a.pref_fraction:.0%}")
    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project_root", nargs="?", default=".")
    ap.add_argument("--slug", required=True)
    ap.add_argument("--captions-dir", default="captions")
    ap.add_argument("--format", choices=("srt", "vtt", "both"), default="both")
    ap.add_argument("--max-line-chars", type=int, default=42)
    ap.add_argument("--max-lines", type=int, default=0)
    ap.add_argument("--min-cue-s", type=float, default=1.0)
    ap.add_argument("--max-cps-hard", type=float, default=0.0)
    ap.add_argument("--max-cps-pref", type=float, default=0.0)
    ap.add_argument("--pref-fraction", type=float, default=0.95)
    ap.add_argument("--require-cue-settings", action="store_true")
    ap.add_argument("--top-setting", default="")
    ap.add_argument("--max-nonspeech", type=int, default=0)
    ap.add_argument("--nonspeech-prefix", default="[")
    ap.add_argument("--terms")
    ap.add_argument("--exempt-window", action="append")
    ap.add_argument("--advisory", action="store_true")
    a = ap.parse_args()

    root = Path(a.project_root).resolve()
    kinds = ["srt", "vtt"] if a.format == "both" else [a.format]
    findings = []
    for kind in kinds:
        p = root / a.captions_dir / f"{a.slug}.{kind}"
        if not p.exists():
            findings.append(f"missing sidecar: {p}")
            continue
        print(f"[captions] {p.name}")
        cues = parse_cues(p, kind)
        if not cues:
            findings.append(f"{p.name}: parsed zero cues -- is it the format it claims?")
            continue
        findings += [f"{p.name}: {f}" for f in check(cues, a, kind)]

    if findings:
        print(f"\n[captions] {len(findings)} finding(s):")
        for f in findings:
            print(f"  - {f}")
        return 0 if a.advisory else 1
    print("[captions] PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
