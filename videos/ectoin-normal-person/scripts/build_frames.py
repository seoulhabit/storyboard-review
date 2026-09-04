#!/usr/bin/env python3
"""Emit compositions/frames/*.html -- one file per UNIT.

THIS IS THE SOURCE LAYER. compositions/frames/*.html are generated and are
discarded by the next `npm run build`; edit the spec in frames_spec.py, never
the output.

A unit's duration and every phase offset come from scripts/timing.py, which
derives them from measured audio. Nothing here authors a time.

Motion rule for this canvas, inherited and measured: A BEAT MOVES A PANEL OR A
COLUMN, NEVER A WORD. On a 1920-wide frame a headline sits inside a grid cell,
so a text fade changes under 1% of the pixels and reads as nothing. Target
area >= 8% of frame and luma delta >= 80 within <= 0.8s, and pick the colour by
LUMINANCE not hue -- celadon->coral is a 27-luma step and measures as zero.

Ease discipline: there is NO timeline-wide `defaults: {ease}`. That single
inherited default gave the predecessor 65.3% of its tweens one signature while
a grep for `ease:` returned 8 hits and reported variety. Every tween names its
own ease, chosen from what the beat is doing narratively.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _preamble import scene
from timing import walk
from vo_lines import MERGED, TURNS
import frames_spec


# Measured quiet windows from check-cadence on the previous render, converted
# to unit-relative offsets. Each entry fires the lower-third band in the middle
# of a stretch where the VO keeps going and nothing on screen changes.
#
# The text is the line's own point, not a label -- if it cannot say something
# the viewer needs, the scene needs a real content beat instead and the band is
# the wrong answer. Colour alternates so the bands do not read as one signature
# repeated (the entrance-signature failure this build exists to beat).
#
# (at, text, alt) -- `at` is relative to the unit, `alt` picks the second fill
# colour. A unit long enough to need two bands appears in both tables; PASS2 is
# NOT necessarily the later of the pair, which is what broke 03-cell (below).
BAND_BEATS2 = {
    "04-protein": (38.0, "THE REAL BEHAVIOUR IS MESSIER", "alt"),
    "12-bottle":  (18.0, "READ THE LIST - JUDGE THE FORMULA", "alt"),  # re-derived: 12-bottle dropped phases b/c this revision (~53.4s -> ~29s)
}

BAND_BEATS = {
    "04-protein":   (13.7, "PREFERENTIAL EXCLUSION", ""),
    # 04-protein is 53.2s -- the longest unit in the piece -- so one band
    # cannot carry it. BAND_BEATS2 is a second pass at a later offset for the
    # units long enough to need two.

    "05-skin":      ( 5.9, "KERATIN, AND HOW IT HOLDS WATER", "alt"),
    "06-trial104":  ( 4.5, "104 WOMEN - 2% ECTOIN VS THE SAME CREAM", ""),
    "07-preference":( 7.0, "PREFERRED IS NOT MEASURED", "alt"),
    "10-notprove":  (11.7, "LIMITED - AND PARTLY INDUSTRY-FUNDED", ""),
    "11-twelve":    (11.0, "FOUR OF THE TWELVE ARE NOT ABOUT SKIN", "alt"),
    "13-kbeauty":   (11.7, "KOREA PACKAGED IT - BACTERIA BUILT IT", "alt"),
    "14-notnew":    ( 5.6, "NOT THE NEW HYALURONIC ACID", ""),
    "15-whatitis":  ( 4.3, "A SUPPORTING INGREDIENT", "alt"),
    "17-dignity":   (10.2, "WOULD YOU?", ""),
}

SPEAKER = {tid: spk for tid, spk, _ in TURNS}

# Band idioms, keyed to the speaker MEASURED as holding the line the band sits
# under -- derived from timing.walk() below, never hand-assigned. I assigned
# these by reading the band text and was wrong on four of the fifteen.
#
# Why the band should carry a register at all: this piece attributes speakers
# by TYPE only, with no persistent speaker zone, so the band is the one
# recurring chrome element that recurs often enough to say something. SOULHABIT
# settles in WITH the reading direction and passes out the far side; JAY cuts in
# AGAINST it and snaps back the way it came. Fifteen appearances of one stamped
# entrance is the exact failure this build exists to beat, so ease and duration
# rotate within each register as well -- consecutive bands never share a variant.
#
# Every variant is sized against the cadence model BEFORE it ships:
#     per_step = area * dLuma / (dur * 8)
# The model assumes a LINEAR ramp, which is the worst case for a wipe -- every
# ease below is an out-family curve, so each lands at or above its modelled
# number. The band is 11.3% of frame at dLuma 224 (paper/ink) or 149
# (paper/moss), so the slowest variant here (circ.out @0.70s on moss) still
# clears the 1.0 floor by 3.0x. Widening these durations cannot starve a beat.
# Measured on the render regardless -- the model is a model.
BAND_IDIOM = {
    "S": [  # settle: enters left-to-right, decelerating, passes out to the right
        dict(org="0% 50%",   ein="power2.out", din=0.62, tin=0.35, hold=1.95,
             eout="power2.in", dout=0.52, oorg="100% 50%",
             ebin="power2.out", dbin=0.30, etext="power1.out", dbout=0.25),
        dict(org="0% 50%",   ein="circ.out",   din=0.70, tin=0.35, hold=2.10,
             eout="power1.in", dout=0.58, oorg="100% 50%",
             ebin="sine.out",   dbin=0.34, etext="sine.out",   dbout=0.25),
        dict(org="0% 50%",   ein="sine.out",   din=0.66, tin=0.35, hold=1.85,
             eout="power2.in", dout=0.50, oorg="100% 50%",
             ebin="power1.out", dbin=0.28, etext="power1.out", dbout=0.25),
    ],
    "J": [  # interrupt: cuts in right-to-left, snaps back the way it came
        dict(org="100% 50%", ein="expo.out",   din=0.40, tin=0.22, hold=1.55,
             eout="power3.in", dout=0.34, oorg="100% 50%",
             ebin="expo.out",   dbin=0.16, etext="none",       dbout=0.18),
        dict(org="100% 50%", ein="power4.out", din=0.46, tin=0.22, hold=1.70,
             eout="expo.in",   dout=0.38, oorg="100% 50%",
             ebin="power3.out", dbin=0.20, etext="none",       dbout=0.18),
    ],
}


def band_span(v):
    """Real on-screen span of one band, so the clamp uses the variant's own
    length. The old emitter hard-coded 3.0s for every band; the widest variant
    here is 3.25s and would have been cut off by the unit's end."""
    return v["tin"] + v["hold"] + 0.15 + 0.40 + v["dbout"]


def band_beat(at, txt, alt, v, own, on_ink, note):
    """One band. Both passes go through here -- the old code had two copies and
    they had drifted apart: PASS1 stamped its text at time 0, PASS2 at its own
    offset. In 03-cell PASS2 fires FIRST (17.0s) and PASS1 later (39.7s), so
    seeking to 39.7 replayed both sets in order and the second band showed the
    first one's text. Verified on the shipped render before fixing: the line
    'ECTOIN IS THE ANSWER IT EVOLVED' never appeared in the video.
    Every set now lands just before its own band, so order cannot matter."""
    at = min(at, max(0.0, own - band_span(v)))
    s = max(0.02, at - 0.06)
    # Rebuild the WHOLE class list: className replaces it, so an `alt` set that
    # forgot `on-ink` would silently drop the ink-ground fill colour back to a
    # 75-luma step. No unit currently hits that pairing; this keeps it that way.
    cls = "band" + (" on-ink" if on_ink else "") + (" alt" if alt else "")
    t_ti = at + v["tin"]
    t_to = t_ti + v["hold"]
    t_fo = t_to + 0.15
    t_bo = t_fo + 0.40
    return (
        f"\n    // {note}\n"
        f"    tl.set('#band-t', {{ textContent: {txt!r} }}, {s:.3f});\n"
        f"    tl.set('#band', {{ className: {cls!r} }}, {s:.3f});\n"
        f"    tl.to('#band', {{ opacity: 1, duration: {v['dbin']:.2f},\n"
        f"                      ease: {v['ebin']!r} }}, {at:.3f});\n"
        f"    tl.fromTo('#band-f', {{ scaleX: 0, transformOrigin: {v['org']!r} }},\n"
        f"              {{ scaleX: 1, duration: {v['din']:.2f},\n"
        f"                 ease: {v['ein']!r} }}, {at:.3f});\n"
        f"    tl.to('#band-t', {{ opacity: 1, duration: 0.28,\n"
        f"                       ease: {v['etext']!r} }}, {t_ti:.3f});\n"
        f"    tl.to('#band-t', {{ opacity: 0, duration: 0.25,\n"
        f"                       ease: {v['etext']!r} }}, {t_to:.3f});\n"
        f"    tl.to('#band-f', {{ scaleX: 0, transformOrigin: {v['oorg']!r},\n"
        f"                       duration: {v['dout']:.2f},\n"
        f"                       ease: {v['eout']!r} }}, {t_fo:.3f});\n"
        f"    tl.to('#band', {{ opacity: 0, duration: {v['dbout']:.2f},\n"
        f"                     ease: 'none' }}, {t_bo:.3f});\n")


def band_register(at, own, turns, start):
    """Which speaker holds the line this band sits under, from measured turn
    times. Falls back to the nearest preceding turn when a band lands in the
    gap between two."""
    abs_t = start + at
    for tid, tstart, tlen in turns:
        if tstart <= abs_t < tstart + tlen:
            return SPEAKER.get(tid, "S")
    prev = [tid for tid, tstart, _ in turns if tstart <= abs_t]
    return SPEAKER.get(prev[-1], "S") if prev else "S"


def main():
    units, total = walk()
    out = ROOT / "compositions" / "frames"
    out.mkdir(parents=True, exist_ok=True)

    rot = {"S": 0, "J": 0}          # rotate variants in playback order
    log = []
    written = []
    for cid, start, own, phases, turns in units:
        spec = frames_spec.SPECS.get(cid)
        if spec is None:
            raise SystemExit(f"no spec for unit {cid} -- add it to frames_spec.py")
        ctx = frames_spec.Ctx(cid=cid, dur=own, phases=phases, turns=turns,
                              merged=cid in MERGED)
        css, body, tl = spec(ctx)
        on_ink = 'class="band on-ink"' in body

        # Both quiet-window passes, emitted in the order they PLAY so the
        # variant rotation is the order a viewer actually sees.
        beats = []
        if cid in BAND_BEATS:
            beats.append((BAND_BEATS[cid], "Measured quiet window: the band carries this stretch."))
        if cid in BAND_BEATS2:
            beats.append((BAND_BEATS2[cid], "Second measured quiet window in a long unit."))
        beats.sort(key=lambda b: b[0][0])

        for (at, txt, alt), note in beats:
            reg = band_register(at, own, turns, start)
            v = BAND_IDIOM[reg][rot[reg] % len(BAND_IDIOM[reg])]
            rot[reg] += 1
            tl += band_beat(at, txt, alt, v, own, on_ink, note)
            clamped = min(at, max(0.0, own - band_span(v)))
            log.append((cid, at, clamped, reg, v["ein"], v["din"],
                        "alt" if alt else "-", on_ink))

        # A slow full-span camera drift under every unit. See BRIEF.md: camera
        # is this piece's PRIMARY continuity mechanism, because attribution is
        # type-only and no actor crosses a cut by default. Amplitude is small
        # (1.5-2% over the unit's whole length) so it never competes with a
        # content beat; its job is to keep the frame alive through a long
        # spoken hold the way a held shot does, not to substitute for a beat.
        # Units with an authored leg get this UNDER it, not instead of it.
        tl = (tl + f"\n    tl.fromTo('#drift', {{ scale: 1, y: 0 }},\n"
                   f"              {{ scale: 1.018, y: -7, duration: {own:.3f},\n"
                   f"                 ease: 'sine.inOut' }}, 0);\n")
        (out / f"{cid}.html").write_text(scene(cid, own, body, css, tl))
        written.append((cid, own, len(phases)))

    print(f"{len(written)} scene files, total {total:.3f}s "
          f"({int(total//60)}:{total%60:05.2f})")
    nm = sum(1 for c, _, _ in written if c in MERGED)
    print(f"  merged units: {nm}  "
          f"(internal phase beats: {sum(p-1 for c,_,p in written if c in MERGED)})")

    print(f"\n  bands: {len(log)}  "
          f"(S {sum(1 for r in log if r[3]=='S')} / J {sum(1 for r in log if r[3]=='J')})")
    print(f"  {'unit':14s} {'at':>6s} {'clamp':>6s} {'reg':>3s} {'entry ease':>12s} "
          f"{'dur':>5s} {'fill':>4s} {'per-step':>9s}")
    for cid, at, cl, reg, ein, din, alt, oi in log:
        # cadence model: area * dLuma / (dur*8); linear ramp = worst case.
        d = 149.0 if alt == "alt" else 224.0
        ps = 0.113 * d / (din * 8)
        flag = "" if ps >= 1.0 else "   <-- BELOW FLOOR"
        note = "" if abs(cl - at) < 1e-6 else "  (clamped)"
        print(f"  {cid:14s} {at:6.1f} {cl:6.1f} {reg:>3s} {ein:>12s} "
              f"{din:5.2f} {alt:>4s} {ps:9.2f}{flag}{note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
