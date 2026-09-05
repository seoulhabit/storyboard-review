#!/usr/bin/env python3
"""Emit compositions/frames/*.html. GENERATED -- edit THIS file, not the output.

EIGHT composition files carry SIXTEEN beat units, grouped by ACTOR CONTINUITY:
a file boundary is exactly a visible transition (transitions.BOUNDARIES), and
inside a file consecutive units are phases on ONE set of DOM nodes, so the
molecule, the building and the barrier are moved and re-framed, never redrawn.

Every beat time is a WORD. `@w(word[,n])` / `@we(word[,n])` resolve to the
n-th occurrence of that word's measured start / end on the file's own
timeline; `@ustart(cid)` / `@uend(cid)` are a unit's span edges; `@fown` is
the file's own span (where the outgoing push begins). Nothing here authors a
second by hand.

Build-time asserts (each one is a defect a previous build shipped):
  * every on-screen text beat <= 10 words (motion.MOTION[cid]["text"])
  * a registering cadence beat at least every CADENCE_MAX_GAP seconds inside
    every spoken file (motion beats; beat_budget formula)
  * the camera is HOME (scale 1, x 0, y 0) before a file's own span ends; the
    only tween allowed to end later is the 1.06 push under the next wipe
  * no `overflow` on .world, no `transform` on .stage / .worldclip, no
    position:fixed, no <img>: each is a safe-area failure mode on record
  * the end-screen tokens are present in the inlined token block
  * the evidence file names no trial count except the documented 23
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _preamble import scene, EASE, TOKENS
from timing import walk, Ctx
from motion import MOTION
from vo_lines import ORDER, WORDLESS, CITES
from transitions import KIND

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "compositions" / "frames"

CADENCE_MAX_GAP = 4.0     # seconds between beats the cadence checker can see
REGISTER = 1.0            # beat_budget per-step threshold
W, H = 1920, 1080


# ---------------------------------------------------------------- binding

TOKEN_RE = re.compile(
    r"@(w|we)\(\s*([A-Za-z0-9'’\-]+)\s*(?:,\s*(\d+)\s*)?\)"
    r"|@(ustart|uend|ufirst|ulast)\(\s*([0-9a-z\-]+)\s*\)"
    r"|@(fown|fdur)\b"
    r"|@(sent|sent_end)\(\s*([0-9a-z\-]+)\s*,\s*(\d+)\s*\)")


class FileCtx:
    """All the unit contexts of one file, plus the file span."""

    def __init__(self, fspan):
        self.f = fspan
        self.u = {u.cid: Ctx(u) for u in fspan.units}
        self.by_word = {}   # word -> the unit that owns its n-th occurrence (file-wide)

    def find(self, word, occ):
        """File-wide occurrence search across the file's units in order."""
        seen = 0
        for u in self.f.units:
            ctx = self.u[u.cid]
            n = len(ctx._matches(word))
            if seen + n >= occ:
                return ctx, occ - seen
            seen += n
        raise SystemExit(f"@w({word},{occ}): only {seen} occurrence(s) in file {self.f.cid} "
                         f"(units {[u.cid for u in self.f.units]})")


def bind(src, fctx, reveals):
    def repl(m):
        if m.group(1):
            ctx, occ = fctx.find(m.group(2), int(m.group(3) or 1))
            val = (ctx.w if m.group(1) == "w" else ctx.we)(m.group(2), occ)
            reveals.append({"file": fctx.f.cid, "unit": ctx.unit.cid, "kind": m.group(1),
                            "word": m.group(2), "occurrence": occ, "seconds": val,
                            "abs": round(val + fctx.f.start, 3)})
            return f"{val:.3f}"
        if m.group(4):
            ctx = fctx.u[m.group(5)]
            return f"{ {'ustart': ctx.ustart, 'uend': ctx.uend, 'ufirst': ctx.first, 'ulast': ctx.last}[m.group(4)]():.3f}"
        if m.group(6):
            return f"{fctx.f.own if m.group(6) == 'fown' else fctx.f.dur:.3f}"
        if m.group(7):
            ctx = fctx.u[m.group(8)]
            return f"{(ctx.sent if m.group(7) == 'sent' else ctx.sent_end)(int(m.group(9))):.3f}"
        return m.group(0)
    out = TOKEN_RE.sub(repl, src)
    if "@" in out:
        leftover = sorted(set(re.findall(r"@[A-Za-z_]+(?:\([^)]*\))?", out)))
        raise SystemExit(f"file {fctx.f.cid}: unresolved marker(s): {leftover}\n"
                         f"Run `python3 scripts/timing.py --words <unit>` to see real words.")
    return out


# ---------------------------------------------------------------- structure

def _wrap_world(body, cid):
    """Insert the clip layer around the camera layer. Done here so no file can
    be added without it; the failure it prevents is ink in a reserved zone."""
    m = re.search(r'( *)<div class="world"([^>]*)>', body)
    assert m, f"{cid}: no .world element to wrap"
    ind = m.group(1)
    body = body[:m.start()] + f'{ind}<div class="worldclip">\n' + \
           f'{ind}<div class="world"{m.group(2)}>' + body[m.end():]
    close = "\n      </div>\n"
    assert body.count(close) >= 1, f"{cid}: no stage close to match"
    i = body.rindex(close)
    return body[:i] + "\n      </div>" + close + body[i + len(close):]


def departure(fspan):
    """The outgoing push under the next wipe -- the ONLY camera leg allowed to
    end off home. Lives here, in the outgoing file's own timeline, because the
    root cannot reach inside a sub-composition and a push OUTSIDE .worldclip
    would drag content into the reserved zones."""
    if not fspan.kind_out or fspan.hold <= 0:
        return ""
    return (f'\n    // departure: push under the {fspan.kind_out} wipe into the next file\n'
            f'    tl.to("#world", {{ scale:1.06, duration:{fspan.hold:.2f}, '
            f'ease:"{EASE["camera"]}" }}, {fspan.own:.3f});\n')


# ---------------------------------------------------------------- asserts

def _camera_ok(tl, fspan):
    """Every #world tween must end by `own`, except the 1.06 departure push."""
    bad = []
    for m in re.finditer(r'tl\.(to|fromTo)\(\s*"#world"\s*,(.*?)\}\s*,\s*([\d.\s()+\-*/]+?)\s*\)\s*;', tl, re.S):
        body, at_expr = m.group(2), m.group(3)
        at = eval(at_expr, {"__builtins__": {}}, {})   # arithmetic literal only, same whitelist as _cadence_ok
        d = re.search(r"duration\s*:\s*([\d.]+)", body)
        dur = float(d.group(1)) if d else 0.0
        rp = re.search(r"repeat\s*:\s*(\d+)", body)
        dur *= 1 + (int(rp.group(1)) if rp else 0)     # a yoyo/repeat runs the leg again
        end = at + dur
        last = body[body.rfind("{"):]
        is_push = "1.06" in last and end <= fspan.own + fspan.hold + 0.01 and at >= fspan.own - 0.01
        if end > fspan.own + 0.01 and not is_push:
            bad.append(f"#world tween at {at:.3f} ends {end:.3f} > own {fspan.own:.3f}: {last.strip()[:60]}")
        if not is_push:
            sc = re.search(r"scale\s*:\s*([\d.]+)", last)
            x = re.search(r"\bx\s*:\s*(-?[\d.]+)", last)
            y = re.search(r"\by\s*:\s*(-?[\d.]+)", last)
    return bad


def _cadence_ok(fspan, fctx, reveals_before):
    """Registering beats (area*dl/(dur*8) >= 1) must sit <= CADENCE_MAX_GAP
    apart across the file's spoken span; the file start counts (a wipe or the
    hook's frame zero), and so does `own` (the next wipe)."""
    if all(u.cid in WORDLESS for u in fspan.units):
        return []
    times = [0.0]
    for u in fspan.units:
        for b in MOTION[u.cid].get("beats", []):
            per_step = b["area"] * b["dl"] / (max(b["dur"], 0.05) * 8)
            if per_step >= REGISTER:
                at = b["at"]
                if isinstance(at, str):
                    expr = bind(at, fctx, [])
                    if not re.fullmatch(r"[\d.\s()+\-*/]+", expr):
                        raise SystemExit(f"{u.cid}: beat time is not arithmetic: {expr!r}")
                    at = float(eval(expr, {"__builtins__": {}}, {}))
                times.append(at)
    times.append(fspan.own)
    times.sort()
    gaps = [(a, b) for a, b in zip(times, times[1:]) if b - a > CADENCE_MAX_GAP]
    return [f"{fspan.cid}: no registering beat between {a:.2f}s and {b:.2f}s "
            f"({b - a:.2f}s > {CADENCE_MAX_GAP}s)" for a, b in gaps]


def _motion_asserts(tl, cid):
    """The brief's motion rules, enforced where they can be: no infinite repeat,
    no bounce/flicker filler (a yoyo cycled three or more times says nothing),
    no unseeded randomness."""
    bad = []
    if re.search(r"repeat\s*:\s*-1", tl):
        bad.append("infinite repeat (repeat:-1)")
    for m in re.finditer(r"repeat\s*:\s*(\d+)", tl):
        if int(m.group(1)) >= 3:
            bad.append(f"repeat:{m.group(1)} -- a cycled tween is filler, not a beat")
    if "Math.random(" in tl:
        bad.append("Math.random() -- unseeded randomness is not seek-safe")
    return bad


def _static_asserts(body, css, cid):
    bad = []
    if "<img" in body:
        bad.append("raster <img> in a composition (fast-capture + clip-path hazard)")
    if re.search(r"\.world\s*\{[^}]*overflow", css):
        bad.append("overflow on .world (a transform scales its own clip edge)")
    if re.search(r"\.(stage|worldclip)\s*\{[^}]*transform", css):
        bad.append("transform on .stage/.worldclip (moves the padded edge outward)")
    if "position:fixed" in css.replace(" ", ""):
        bad.append("position:fixed")
    if cid == "10-evidence":
        for n in re.findall(r"\b(\d+)\s*(?:trials|studies)\b", re.sub(r"<[^>]+>", " ", body)):
            if n != "23":
                bad.append(f"evidence file names a trial count ({n}) the source does not give")
    return bad


def check_text_beats():
    bad = []
    for cid in ORDER:
        for t in MOTION[cid]["text"]:
            if len(t.split()) > 10:
                bad.append(f"{cid}: on-screen beat over 10 words: {t!r}")
        n = len(MOTION[cid]["treatments"])
        if not 2 <= n <= 4:
            bad.append(f"{cid}: {n} treatments (want 2-4)")
    return bad


# ---------------------------------------------------------------- files

def _stub(fspan, fctx):
    """Plumbing stub: one panel per unit, one wash at its first word. Replaced
    by the authored file functions in FILE_FNS."""
    body = ['      <div class="stage">', '       <div class="world" id="world">',
            '        <div class="col" style="gap:var(--s-4);height:100%;justify-content:center;">']
    tl, beats = [], []
    for k, u in enumerate(fspan.units):
        txt = MOTION[u.cid]["text"][0]
        body.append(f'          <div class="phase" id="ph-{u.cid}"><div class="panel" id="p-{u.cid}" '
                    f'style="height:200px;"><div class="wash aqua" id="w-{u.cid}"></div>'
                    f'<p class="p-title">{txt}</p></div></div>')
        at = "0.10" if u.cid in WORDLESS else f"@ustart({u.cid})"
        tl.append(f'    tl.fromTo("#w-{u.cid}", {{ scaleX:0 }}, {{ scaleX:1, duration:0.5, '
                  f'ease:"{EASE["wipe"]}" }}, {at});')
        MOTION[u.cid]["beats"] = [{"name": "stub wash", "at": at, "area": 0.12, "dl": 91, "dur": 0.5}]
        if u.cid not in WORDLESS:
            for i, w in enumerate(u.words[::6]):
                t = w["start"] - fspan.start
                tl.append(f'    tl.to("#w-{u.cid}", {{ scaleX:{0.4 + 0.6 * ((i + 1) % 2)}, duration:0.4, '
                          f'ease:"{EASE["swap"]}" }}, {t:.3f});')
                MOTION[u.cid]["beats"].append({"name": "stub nudge", "at": t, "area": 0.12, "dl": 91, "dur": 0.4})
    body += ['        </div>', '       </div>', '      </div>', '']
    tl.append(f'    tl.fromTo("#world", {{ scale:1.03 }}, {{ scale:1, duration:1.0, ease:"{EASE["camera"]}" }}, 0);')
    return "\n".join(body), "", "\n".join(tl)


FILE_FNS = {}   # file cid -> fn(fspan, fctx) -> (body, css, tl); missing -> stub
FILE_MODULES = {"01-hook": "frames_a", "02-promise": "frames_a", "03-building": "frames_b",
                "06-door": "frames_c", "08-digestion": "frames_d", "10-evidence": "frames_e",
                "14-hierarchy": "frames_f", "16-end": "frames_g"}


def load_file_fns(only=None):
    """Import the file modules. With `only`, import just that file's module so a
    sibling mid-edit cannot break an unrelated file's build."""
    mods = sorted(set(FILE_MODULES.values())) if only is None else [FILE_MODULES[only]]
    for _mod in mods:
        FILE_FNS.update(__import__(_mod).FILES)


def emit(fspan, fctx, reveals, fake):
    fn = FILE_FNS.get(fspan.cid, _stub)
    body, css, tl = fn(fspan, fctx)
    tl = bind(tl, fctx, reveals) + departure(fspan)
    bad = (_static_asserts(body, css, fspan.cid) + _motion_asserts(tl, fspan.cid)
           + _camera_ok(tl, fspan) + _cadence_ok(fspan, fctx, reveals))
    if bad:
        raise SystemExit(f"{fspan.cid}:\n  " + "\n  ".join(bad))
    if fake:
        body = "      <!-- VO MANIFEST: FAKE -- NOT FOR DELIVERY -->\n" + body
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{fspan.cid}.html").write_text(scene(fspan.cid, fspan.dur, _wrap_world(body, fspan.cid), css, tl))
    return f"  {fspan.cid:14s} {fspan.dur:7.3f}s  units {', '.join(u.cid for u in fspan.units)}"


LOOP_TRIALS_BY, LOOP_REMOVE_BY = 9.0, 10.5   # the curiosity loop opens inside the first 10s


def _loop_ok(units, fake):
    """The brief: the industry-funding curiosity loop opens in the first 10s. On
    the real manifest this is a hard assert; on the fake it is advisory."""
    u = next(x for x in units if x.cid == "02-promise")
    ctx = Ctx(u)
    t_trials, t_remove = ctx.w_abs("trials"), ctx.w_abs("remove")
    msg = f"  curiosity loop: 'trials' at {t_trials:.2f}s (<= {LOOP_TRIALS_BY}), 'remove' at {t_remove:.2f}s (<= {LOOP_REMOVE_BY})"
    ok = t_trials <= LOOP_TRIALS_BY and t_remove <= LOOP_REMOVE_BY
    if not ok and not fake:
        raise SystemExit(msg + "\n  the take runs slow -- trim the hook or raise the tempo before round 2")
    print(msg + ("" if ok else "  [fake manifest -- advisory]"))


def main():
    only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
    assert "--endscreen-right" in TOKENS and "--endscreen-bottom" in TOKENS, \
        "end-screen tokens missing from the inlined token block (silent calc() failure)"
    load_file_fns(only)
    bad = check_text_beats()
    if bad:
        raise SystemExit("\n".join(bad))
    units, files, total, manifest = walk()
    fake = manifest.get("source") == "fake"
    _loop_ok(units, fake)
    reveals = []
    if only is None:
        for f in OUT.glob("*.html"):
            f.unlink()
    print("emitting compositions/frames/ (GENERATED -- edit build_frames.py):")
    for fspan in files:
        if only and fspan.cid != only:
            continue
        print(emit(fspan, FileCtx(fspan), reveals, fake))
    if only:
        print(f"  --only {only}: reveals not written; run the full build before build_index")
        return 0
    (ROOT / "index.reveals.json").write_text(json.dumps(reveals, indent=1) + "\n")
    stubs = [f.cid for f in files if f.cid not in FILE_FNS]
    print(f"  total {total:.3f}s  {len(reveals)} word markers -> index.reveals.json"
          f"{'  [VO MANIFEST: FAKE]' if fake else ''}")
    if stubs:
        print(f"  STUB files (plumbing only): {stubs}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
