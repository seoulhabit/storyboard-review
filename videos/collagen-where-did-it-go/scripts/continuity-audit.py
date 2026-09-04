#!/usr/bin/env python3
"""Audit a HyperFrames project's CONTINUITY -- at SOURCE level, no render needed.

Written 2026-09-02 for pre-render gate item 14, after an external review of
`videos/ectoin-survival-molecule` (340s, 1920x1080, 29 scenes, the channel's
first long-form piece) concluded it "feels like an animated presentation" --
and the audit's decisive finding was that the piece PASSED EVERY GATE THE
SKILL HAD. Cadence clean at the long-form ceiling, median trailing hold 2.1s,
safe-area gate run, contrast passing, and 28/28 hard cuts *because the rule
said so*. Every existing check measures whether something is MOVING. None of
them measures whether the piece is one continuous space or 29 slides.

So this tool does not look at pixels at all. It counts four structural
properties of the SOURCE, which is where "slides" is actually decided:

  1. BOUNDARIES  every scene-to-scene join: cut or transition, and whether the
                 ground (the #root background) changes across it.
  2. SIGNATURES  every real tween's (animated props + EFFECTIVE ease), where
                 "effective" includes the ease inherited from the timeline's
                 own `defaults:{ease}`. A majority of tweens sharing one
                 signature is the template failure, regardless of content.
  3. ACTORS      shapes drawn identically in consecutive scene files -- the
                 same diagram rebuilt rather than carried (H3); and scenes
                 that are already merged multi-phase sub-comps (H3b).
  4. CAMERA      tweens that move a world/stage/frame wrapper rather than an
                 element (H4), plus CSS Ken Burns plate motion counted apart.

WHY SOURCE-LEVEL IS LEGITIMATE HERE, when source-level cadence is not.
Cadence has to be measured on rendered pixels because a source tween can fire
correctly and still be invisible. Variety is the opposite kind of property: it
IS a property of the source. Two tweens with the same props and the same ease
are the same entrance whatever they render to. This tool therefore claims
nothing about how anything looks -- see the verdict line, which says so.

HEURISTICS, NAMED. H3 (rebuilt actors) and H4 (camera) are pattern matches,
not proofs: H3 compares normalised SVG geometry between consecutive files and
will miss a diagram rebuilt with different numbers; H4 matches target
selectors against /(world|zoom|stage|cam|frame)/i and will miss a camera
wrapper called something else. Both are starting points for a look at frames,
not verdicts. The boundary and signature counts are exact.

THE TWEEN SCANNER IS PAREN-BALANCED AND MULTI-LINE ON PURPOSE. Measured on
the calibration project (`videos/ectoin-survival-molecule`, 2026-09-02): 196
real tweens, of which 47 -- 24% -- do not close on the line they open on. A
line-oriented regex is not "mostly right" on that input; it is wrong by
construction, and it fails silently: it returns a smaller, cleaner-looking
population and a share computed over the wrong denominator. The tool prints
that multi-line count on every run, so the claim is re-measured rather than
inherited from this comment.

USAGE
    python3 continuity-audit.py <project_root> [--gate] [--verbose]

Exits 0 by default (advisory, like the other check-*.py here except
check-safe-area.py). With --gate it exits 2 on ONE finding only: a plain
opacity-only crossfade across a ground change, which is the documented
muddy-midpoint defect and the single thing here that is a rule violation
rather than a craft observation.
"""

import re
import sys
from collections import Counter
from pathlib import Path

# --------------------------------------------------------------------------
# Tween vars keys that describe the TWEEN rather than what it animates. Kept
# exactly as the gate spec lists them: anything else at depth 1 counts as an
# animated property, including a callback this list does not name (which will
# show up in a signature and is meant to be visible rather than swallowed).
NON_PROP_KEYS = {"duration", "delay", "ease", "onUpdate", "immediateRender",
                 "overwrite", "stagger"}

MOVE_PROPS = {"x", "y", "xPercent", "yPercent"}
CAMERA_PROPS = {"scale"} | MOVE_PROPS
CAMERA_TARGET_RE = re.compile(r"(world|zoom|stage|cam|frame)", re.IGNORECASE)

# H3: the attributes that make an SVG shape THE SAME SHAPE. Everything else --
# id, fill, stroke colour, opacity -- is styling that a rebuild would vary
# without making it a different actor.
GEOM_ATTRS = ("cx", "cy", "r", "d", "x", "y", "width", "height", "viewBox",
              "stroke-width")
SHAPE_TAGS = ("circle", "rect", "path", "ellipse", "polygon", "g")

KEN_BURNS_RE = re.compile(
    r"transform\s*:\s*scale\(\s*calc\(\s*1\s*\+\s*var\(\s*--progress", re.IGNORECASE)


# ---------------------------------------------------------------- JS scanning
def _skip_string(text, i):
    """Index just past the string literal that starts at i."""
    quote = text[i]
    i += 1
    while i < len(text):
        c = text[i]
        if c == "\\":
            i += 2
            continue
        if c == quote:
            return i + 1
        i += 1
    return i


def _skip_trivia(text, i):
    """Index past whitespace and comments starting at i (may be a no-op)."""
    n = len(text)
    while i < n:
        if text[i].isspace():
            i += 1
        elif text.startswith("//", i):
            j = text.find("\n", i)
            i = n if j < 0 else j + 1
        elif text.startswith("/*", i):
            j = text.find("*/", i)
            i = n if j < 0 else j + 2
        else:
            break
    return i


def balanced_args(text, open_idx):
    """Split the parenthesised argument list starting at text[open_idx] == '('.

    Returns (args, end_idx) with args as raw source strings. Brace/bracket/paren
    depth, string literals and comments are all tracked, which is the whole
    point: a GSAP call routinely spans several lines and contains nested object
    literals, arrays, arithmetic and quoted selectors.
    """
    assert text[open_idx] == "("
    i = open_idx + 1
    depth = 0
    args, start = [], i
    n = len(text)
    while i < n:
        c = text[i]
        if c in "\"'`":
            i = _skip_string(text, i)
            continue
        if text.startswith("//", i) or text.startswith("/*", i):
            i = _skip_trivia(text, i)
            continue
        if c in "([{":
            depth += 1
        elif c in ")]}":
            if c == ")" and depth == 0:
                args.append(text[start:i])
                return args, i + 1
            depth -= 1
        elif c == "," and depth == 0:
            args.append(text[start:i])
            start = i + 1
        i += 1
    args.append(text[start:])
    return args, n


def object_entries(text):
    """Depth-1 (key, value_source) pairs of a JS object literal.

    `text` should start at the literal's '{'. Nested objects, arrays, quoted
    keys and template strings are all handled; nothing inside a nested value is
    reported as a key.
    """
    text = text.strip()
    if not text.startswith("{"):
        return []
    entries = []
    i, n, depth = 0, len(text), 0
    expect_key = False
    while i < n:
        c = text[i]
        if c in "\"'`":
            j = _skip_string(text, i)
            if depth == 1 and expect_key:
                key = text[i + 1:j - 1]
                k = _skip_trivia(text, j)
                if k < n and text[k] == ":":
                    val, i = _read_value(text, k + 1)
                    entries.append((key, val))
                    expect_key = False
                    continue
            i = j
            continue
        if text.startswith("//", i) or text.startswith("/*", i):
            i = _skip_trivia(text, i)
            continue
        if c in "([{":
            depth += 1
            if c == "{" and depth == 1:
                expect_key = True
            i += 1
            continue
        if c in ")]}":
            depth -= 1
            i += 1
            if depth == 0:
                break
            continue
        if depth == 1:
            if c == ",":
                expect_key = True
                i += 1
                continue
            if expect_key and not c.isspace():
                m = re.match(r"[A-Za-z_$][\w$\-]*", text[i:])
                if m:
                    key = m.group(0)
                    k = _skip_trivia(text, i + len(key))
                    if k < n and text[k] == ":":
                        val, i = _read_value(text, k + 1)
                        entries.append((key, val))
                        expect_key = False
                        continue
                expect_key = False
        i += 1
    return entries


def _read_value(text, i):
    """Value source from i to the next depth-0 comma or the closing brace."""
    n, depth, start = len(text), 0, i
    while i < n:
        c = text[i]
        if c in "\"'`":
            i = _skip_string(text, i)
            continue
        if text.startswith("//", i) or text.startswith("/*", i):
            i = _skip_trivia(text, i)
            continue
        if c in "([{":
            depth += 1
        elif c in ")]}":
            if depth == 0:
                return text[start:i].strip(), i
            depth -= 1
        elif c == "," and depth == 0:
            return text[start:i].strip(), i
        i += 1
    return text[start:].strip(), n


TWEEN_RE = re.compile(r"\btl\.(fromTo|from|to)\s*\(")
STRAY_GSAP_RE = re.compile(r"\bgsap\.(fromTo|from|to)\s*\(")
DEFAULTS_EASE_RE = re.compile(
    r"defaults\s*:\s*\{[^{}]*?ease\s*:\s*[\"'`]([^\"'`]+)[\"'`]", re.DOTALL)


def scan_tweens(text, default_ease=None):
    """Every real tl.to/from/fromTo in `text`, paren-balanced and multi-line.

    Skips `tl.to({}, ...)` full-span anchors (they animate nothing; every scene
    has one) and never sees `tl.set` (an instant state, not a tween).
    Returns dicts: target (raw source), props (set), ease (effective), pos.
    """
    out = []
    for m in TWEEN_RE.finditer(text):
        kind = m.group(1)
        args, end = balanced_args(text, m.end() - 1)
        if not args:
            continue
        target = args[0].strip()
        if re.sub(r"\s+", "", target) == "{}":
            continue                      # full-span anchor, not a tween
        vars_idx = 2 if kind == "fromTo" else 1
        if len(args) <= vars_idx:
            continue
        entries = object_entries(args[vars_idx])
        keys = [k for k, _ in entries]
        props = {k for k in keys if k not in NON_PROP_KEYS}
        ease = None
        for k, v in entries:
            if k == "ease":
                ease = v.strip().strip("\"'`")
        pos = None
        if len(args) > vars_idx + 1:
            try:
                pos = float(args[vars_idx + 1].strip())
            except ValueError:
                pos = None
        out.append({"kind": kind, "target": target, "props": props,
                    "ease": ease or default_ease, "explicit_ease": ease is not None,
                    "pos": pos, "line": text.count("\n", 0, m.start()) + 1,
                    "multiline": "\n" in text[m.start():end]})
    return out


# ----------------------------------------------------------------- HTML bits
def parse_scenes(index_text):
    """(id, comp_id, src, start, duration) per .scene clip, attribute-order-independent.

    Same approach as check-static-hold.py's scene_boundaries(): match the TAG,
    then pull each attribute out of it separately. A single ordered regex is
    the bug that silently returned zero scenes on `pilling-vs-peeling`.
    """
    tag_re = re.compile(r"<div\b[^>]*\bclass=\"[^\"]*\bscene\b[^\"]*\"[^>]*>")
    def attr(tag, name):
        esc = re.escape(name)
        m = re.search(rf'\b{esc}="([^"]*)"', tag)
        return m.group(1) if m else None
    scenes = []
    for tag in tag_re.findall(index_text):
        src = attr(tag, "data-composition-src")
        start, dur = attr(tag, "data-start"), attr(tag, "data-duration")
        if not (src and start and dur):
            continue
        scenes.append({
            "id": attr(tag, "id") or "",
            "comp_id": attr(tag, "data-composition-id") or "",
            "src": src, "start": float(start), "duration": float(dur),
            "end": float(start) + float(dur),
        })
    scenes.sort(key=lambda s: s["start"])
    return scenes


ROOT_BG_RE = re.compile(r"#root\s*\{([^}]*)\}", re.DOTALL)
BG_DECL_RE = re.compile(r"\bbackground(?:-color)?\s*:\s*([^;}]+)")
VAR_USE_RE = re.compile(r"var\(\s*(--[\w-]+)")


def ground_of(text):
    """(raw, resolved) ground colour from the LAST `#root {...background...}` block.

    A scene file has several `#root` blocks -- one carrying the design tokens,
    one carrying layout, and the ground on the last. Taking the first gets a
    block with no background at all; taking any block that merely mentions
    `background` gets a token declaration. Last-with-a-background is the one
    that wins in CSS, which is the only definition that is not a guess.
    """
    blocks = [b for b in ROOT_BG_RE.findall(text) if BG_DECL_RE.search(b)]
    if not blocks:
        return (None, None)
    raw = BG_DECL_RE.search(blocks[-1]).group(1).strip()
    resolved = raw
    seen = set()
    while True:
        m = VAR_USE_RE.search(resolved)
        if not m or m.group(1) in seen:
            break
        seen.add(m.group(1))
        esc = re.escape(m.group(1))
        d = re.search(rf"{esc}\s*:\s*([^;}}\n]+)", text)
        if not d:
            break
        resolved = d.group(1).strip()
    return (raw, resolved.lower())


ATTR_RE = re.compile(r'([\w:.-]+)\s*=\s*"([^"]*)"')


def shape_signatures(text):
    """Normalised geometry of every SVG shape in the file (H3).

    Drops id / fill / stroke / opacity -- a rebuild varies styling freely --
    and keeps only geometry. A shape with NO geometry attribute at all (a bare
    `<g>`) is dropped: it would match every other bare `<g>` in the project and
    turn this heuristic into noise.
    """
    sigs = set()
    alt = "|".join(SHAPE_TAGS)
    for m in re.finditer(rf"<({alt})\b([^>]*)>", text):
        tag, attrs = m.group(1), dict(ATTR_RE.findall(m.group(2)))
        geom = tuple(f"{k}={attrs[k].strip()}" for k in GEOM_ATTRS if k in attrs)
        if geom:
            sigs.add((tag,) + geom)
    return sigs


def phase_count(text):
    """H3b: a merged multi-phase sub-comp declares its phases as divs."""
    return len(re.findall(r'<div\b[^>]*\bclass="[^"]*\bphase\b[^"]*"', text))


def root_script(text):
    """The root composition's own <script> bodies (where transitions get stamped)."""
    return "\n".join(re.findall(r"<script\b[^>]*>(.*?)</script>", text, re.DOTALL))


# ------------------------------------------------------------------ analysis
def classify(props):
    if props and props <= {"opacity"}:
        return "crossfade"
    if props & MOVE_PROPS:
        return "push"
    if "scale" in props:
        return "zoom"
    if "filter" in props:
        return "blur"
    return "transition"


def audit(project_root):
    root = Path(project_root).resolve()
    index_path = root / "index.html"
    if not index_path.exists():
        print(f"continuity-audit: no index.html under {root} - nothing to audit.")
        return None
    index_text = index_path.read_text(errors="replace")
    scenes = parse_scenes(index_text)
    if not scenes:
        print(f"continuity-audit: {index_path} declares no "
              f".scene[data-composition-src] clips - nothing to audit.")
        return None

    # --- per scene: ground, tweens, shapes, phases
    for s in scenes:
        p = root / s["src"]
        s["exists"] = p.exists()
        text = p.read_text(errors="replace") if s["exists"] else ""
        s["ground_raw"], s["ground"] = ground_of(text)
        eases = DEFAULTS_EASE_RE.findall(text)
        s["default_ease"] = eases[0] if eases else None
        s["tweens"] = scan_tweens(text, s["default_ease"])
        s["shapes"] = shape_signatures(text)
        s["phases"] = phase_count(text)
        s["ken_burns"] = bool(KEN_BURNS_RE.search(text))
        s["stray_gsap"] = len(STRAY_GSAP_RE.findall(text))

    # --- root-timeline tweens, mapped to the boundary they sit at
    root_tweens = [t for t in scan_tweens(root_script(index_text))
                   if "#scene-" in t["target"] or any(
                       s["id"] and "#" + s["id"] in t["target"] for s in scenes)]
    by_boundary = {}
    for t in root_tweens:
        hits = [i for i, s in enumerate(scenes)
                if (s["id"] and "#" + s["id"] in t["target"])
                or (s["comp_id"] and "#scene-" + s["comp_id"] in t["target"])]
        if not hits:
            continue
        j = hits[0]
        cands = [b for b in (j - 1, j) if 0 <= b < len(scenes) - 1]
        if not cands:
            continue
        if t["pos"] is not None and len(cands) > 1:
            b = min(cands, key=lambda b: abs(scenes[b + 1]["start"] - t["pos"]))
        else:
            b = cands[-1] if j == 0 else cands[0]
        by_boundary.setdefault(b, []).append(t)

    # --- boundaries
    boundaries = []
    for i in range(len(scenes) - 1):
        a, b = scenes[i], scenes[i + 1]
        overlap = a["end"] - b["start"]
        tws = by_boundary.get(i, [])
        props = set().union(*[t["props"] for t in tws]) if tws else set()
        if tws:
            kind = classify(props)
        elif overlap > 1e-3:
            kind = "overlap?"
        else:
            kind = "cut"
        ground_change = (a["ground"] is not None and b["ground"] is not None
                         and a["ground"] != b["ground"])
        violation = (kind == "crossfade" and ground_change)
        boundaries.append({
            "i": i, "a": a, "b": b, "t": b["start"], "overlap": max(overlap, 0.0),
            "kind": kind, "props": props, "ground_change": ground_change,
            "violation": violation, "tweens": tws,
        })

    # --- signatures over every real scene tween
    all_tweens = [t for s in scenes for t in s["tweens"]]
    sig = Counter((tuple(sorted(t["props"])), t["ease"] or "(none)") for t in all_tweens)
    ease_share = Counter(t["ease"] or "(none)" for t in all_tweens)
    fade_slide = sum(1 for t in all_tweens
                     if "opacity" in t["props"] and t["props"] & MOVE_PROPS)

    # --- actors
    pairs = []
    for i in range(len(scenes) - 1):
        shared = scenes[i]["shapes"] & scenes[i + 1]["shapes"]
        if shared:
            pairs.append((i, shared))
    merged = [s for s in scenes if s["phases"] >= 2]

    # --- camera
    cams = [(s, t) for s in scenes for t in s["tweens"]
            if CAMERA_TARGET_RE.search(t["target"]) and (t["props"] & CAMERA_PROPS)]
    ken = [s for s in scenes if s["ken_burns"]]

    return {"root": root, "scenes": scenes, "boundaries": boundaries,
            "tweens": all_tweens, "sig": sig, "ease_share": ease_share,
            "fade_slide": fade_slide, "pairs": pairs, "merged": merged,
            "cams": cams, "ken": ken, "root_tweens": root_tweens}


# -------------------------------------------------------------------- report
def report(a, verbose=False):
    scenes, bounds, tweens = a["scenes"], a["boundaries"], a["tweens"]
    n = len(tweens)
    print(f"Continuity audit - {a['root'].name}")
    print(f"  {len(scenes)} scenes, {scenes[-1]['end']:.3f}s authored span, "
          f"{len(bounds)} boundaries.")
    missing = [s for s in scenes if not s["exists"]]
    if missing:
        print(f"  WARNING: {len(missing)} scene file(s) named in index.html do not "
              f"exist: {', '.join(s['src'] for s in missing[:4])}")

    # boundaries -----------------------------------------------------------
    print("\n  BOUNDARIES")
    print(f"    {'#':>3}  {'at':>9}  {'from -> to':<34} {'ground':<18} type")
    for b in bounds:
        g = f"{b['a']['ground'] or '?'} -> {b['b']['ground'] or '?'}"
        mark = " *" if b["ground_change"] else "  "
        note = "  <-- CROSSFADE ACROSS A GROUND CHANGE" if b["violation"] else ""
        pair = f"{b['a']['comp_id'] or b['a']['id']} -> {b['b']['comp_id'] or b['b']['id']}"
        print(f"    {b['i']+1:>3}  {b['t']:>9.3f}  {pair:<34} {g:<18}{mark}{b['kind']}{note}")
    kinds = Counter(b["kind"] for b in bounds)
    gc = [b for b in bounds if b["ground_change"]]
    viol = [b for b in bounds if b["violation"]]
    print("\n    types: " + ", ".join(f"{k} {v}" for k, v in kinds.most_common()))
    print(f"    transitions: {sum(v for k, v in kinds.items() if k != 'cut')} of "
          f"{len(bounds)}   hard cuts: {kinds.get('cut', 0)}")
    print(f"    ground changes (*): {len(gc)} of {len(bounds)}"
          f"   -- {sum(1 for b in gc if b['kind'] == 'cut')} of them are hard cuts,"
          f" {len(bounds) - len(gc)} same-ground boundaries could carry one")
    print(f"    plain-crossfade-across-ground violations: {len(viol)}")

    # signatures -----------------------------------------------------------
    print("\n  ENTRANCE SIGNATURES")
    ml = sum(1 for t in tweens if t["multiline"])
    print(f"    {n} real tweens across {len(scenes)} scene files "
          f"({ml} of them span more than one line - a line regex would have "
          f"missed {100*ml/max(n,1):.0f}% of the population).")
    print("    top signatures (animated props + effective ease):")
    for (props, ease), c in a["sig"].most_common(3):
        label = "{" + ",".join(props) + "}" if props else "{}"
        print(f"      {c:>4}  {100*c/max(n,1):>5.1f}%  {label} + {ease}")
    print("    effective ease shares (explicit OR inherited from defaults:{ease}):")
    for ease, c in a["ease_share"].most_common(3):
        exp = sum(1 for t in tweens if (t["ease"] or "(none)") == ease and t["explicit_ease"])
        print(f"      {c:>4}  {100*c/max(n,1):>5.1f}%  {ease}"
              f"   ({exp} explicit, {c-exp} inherited)")
    defaults = Counter(s["default_ease"] for s in scenes if s["default_ease"])
    print(f"    timelines declaring defaults:{{ease}}: {sum(defaults.values())} of "
          f"{len(scenes)}" + (f"   ({', '.join(f'{k} x{v}' for k, v in defaults.most_common())})"
                              if defaults else ""))
    print(f"    fade-and-slide (opacity + x|y in one tween): {a['fade_slide']} "
          f"({100*a['fade_slide']/max(n,1):.1f}%)")
    stray = sum(s["stray_gsap"] for s in scenes)
    if stray:
        print(f"    NOTE: {stray} gsap.to/from/fromTo call(s) outside the timeline were "
              f"seen and NOT counted -- they are also not seek-safe.")

    # actors ---------------------------------------------------------------
    print("\n  ACTORS")
    print(f"    rebuilt-actor pairs (H3, consecutive files sharing normalised "
          f"geometry): {len(a['pairs'])}")
    for i, shared in a["pairs"]:
        ex = sorted(shared)[:2]
        pretty = "; ".join(s[0] + "(" + ",".join(s[1:]) + ")" for s in ex)
        print(f"      {scenes[i]['comp_id']} -> {scenes[i+1]['comp_id']}: "
              f"{len(shared)} shape(s)  e.g. {pretty}")
        if verbose:
            for s in sorted(shared)[2:]:
                print(f"          {s[0]}(" + ",".join(s[1:]) + ")")
    print(f"    merged multi-phase scenes (H3b, >=2 .phase divs): "
          f"{len(a['merged'])} of {len(scenes)}"
          + (f"   ({', '.join(s['comp_id'] for s in a['merged'])})" if a["merged"] else ""))

    # camera ---------------------------------------------------------------
    print("\n  CAMERA")
    print(f"    camera-move tweens (H4, target ~ /(world|zoom|stage|cam|frame)/i "
          f"with scale/x/y): {len(a['cams'])}")
    for s, t in a["cams"][:12]:
        print(f"      {s['comp_id']}:{t['line']}  {t['target']}  "
              f"{{{','.join(sorted(t['props']))}}} {t['ease']}")
    print(f"    CSS Ken Burns plate motion (counted SEPARATELY - it moves a plate "
          f"inside a\n      frame, not the frame): {len(a['ken'])} scene(s)"
          + (f"   ({', '.join(s['comp_id'] for s in a['ken'][:8])})" if a["ken"] else ""))

    # verdict --------------------------------------------------------------
    print("\n  VERDICT (gate item 14 - four source-structural counts)")
    top = a["sig"].most_common(1)
    top_share = 100 * top[0][1] / max(n, 1) if top else 0.0
    top_ease = a["ease_share"].most_common(1)
    ease_top = 100 * top_ease[0][1] / max(n, 1) if top_ease else 0.0
    print(f"    boundaries carried by a transition : "
          f"{sum(1 for b in bounds if b['kind'] != 'cut')}/{len(bounds)}")
    print(f"    top entrance signature share       : {top_share:.1f}%   "
          f"(top effective ease alone: {ease_top:.1f}%)")
    print(f"    rebuilt-actor pairs / merged scenes: {len(a['pairs'])} / {len(a['merged'])}")
    print(f"    camera moves                       : {len(a['cams'])}")
    print("\n    These are SOURCE-STRUCTURAL COUNTS, NOT PIXELS. Nothing here says how")
    print("    the piece looks, and a clean row is not a clean render. H3 (rebuilt")
    print("    actors) and H4 (camera) are heuristics -- verify each on extracted")
    print("    frames before acting on it. The one hard rule is the crossfade-across-")
    print("    a-ground-change violation above; everything else is a craft reading.")
    return len(viol)


def main():
    argv = [a for a in sys.argv[1:] if not a.startswith("--")]
    gate = "--gate" in sys.argv
    verbose = "--verbose" in sys.argv
    a = audit(argv[0] if argv else ".")
    if a is None:
        return 0
    violations = report(a, verbose)
    if gate and violations:
        print(f"\n  --gate: FAIL ({violations} plain crossfade(s) across a ground "
              f"change).")
        return 2
    if gate:
        print("\n  --gate: pass (no plain crossfade across a ground change). This gates "
              "\n  that ONE rule and nothing else above it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
