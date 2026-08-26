#!/usr/bin/env python3
"""
storyline.py — validate a HyperFrames explainer script.json and trace the
whole pipeline around it: which source record it was compiled from (INPUT),
what each scene actually says and which visual component it uses (the
STORYLINE), which rendered file it produced (OUTPUT), and a sourcing/
content-safety pass over the text.

Usage:
    python3 storyline.py /path/to/scripts/<handle>.json [more scripts ...]

Everything is resolved automatically from the script itself — its own
`sourceRecord` field points at the input, its own `handle` field is matched
against video/out/*.mp4 for the output. Nothing extra to pick.

Checks performed:
  - Structural validation: the same rules video/compositions/lib/build.mjs
    itself enforces (scenes contiguous and starting at 0, known scene/visual
    types, required sub-objects present, durationSeconds matching the last
    scene's own endSeconds). "Valid" here means "build.mjs will actually
    accept this," not a separate, looser opinion.
  - Sourcing audit: every sourceId referenced anywhere in the script
    (scene-level, and inside any visual sub-object — depthOfAction.claim,
    clinicalCalendar rows, conversionPath, pipette, evidenceMeter,
    gradedScale, routineLadder slots) is checked against the source
    record's own "## 13. Source Tracker" section — the same real ledger
    build.mjs's assertion gate resolves against. An id that doesn't resolve
    there is flagged.
  - Content-safety signals: every piece of visible text is scanned for the
    same two marker tiers video/compositions/lib/assertion-gate.mjs uses.
    ABSOLUTE markers ("clinically proven", "100% safe", "guaranteed", ...)
    are always flagged, sourced or not, mirroring that gate's own rule that
    one citation cannot support a categorical claim. This is a heuristic
    signal relevant to platform health-content policy (e.g. YouTube's
    medical-misinformation policy) — it is NOT a compliance determination.
    Only the platform itself can determine actual policy compliance.
  - Output trace: matches video/out/*.mp4 by handle, reports whether a
    render exists and whether its real duration (via ffprobe, if present on
    PATH) matches the script's own durationSeconds.
  - Render checks (pixel-level, only when a render exists): the scroll-stop
    frame (t=0) is checked against a settled frame for the blank/mid-fade
    failure mode; each scene's compiled claim text is OCR-verified against
    what's actually on screen; on-screen text is scanned for leaked internal
    strings (refusal language, harness chrome, template slot leakage); any
    scene carrying a "korean"-role text block gets a pixel-only glyph-
    presence check (see check_korean_glyphs below for why this is NOT OCR-
    based); identity-type scenes are checked for efficacy/evidence language
    that shouldn't appear there regardless of sourcing (identity scenes are
    nominal-only by design — name/INCI/category, never a claim).

Writes one storyline_<handle>.html next to this script and opens it.
Structural validation and sourcing/safety checks need only the standard
library. Render checks additionally need Pillow + numpy (for pixel
analysis) and pytesseract + the tesseract binary with eng/kor language data
(for OCR) — all optional: when any of these aren't installed, the affected
checks report themselves as unavailable instead of failing the whole run.
ffprobe is used if available, skipped with a note if not.
"""

import base64
import html
import io
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import numpy as np
    from PIL import Image
    _HAS_IMAGING = True
except ImportError:
    _HAS_IMAGING = False

try:
    import pytesseract
    _HAS_OCR = True
except ImportError:
    _HAS_OCR = False

VALID_SCENE_TYPES = {"hook", "identity", "claim", "comparison", "enumeration", "sources", "end_card"}
VALID_VISUAL_TYPES = {
    "icon_row", "scale_comparison", "sequence_stack", "chain_diagram", "label_artifact", "none",
    "depth_bands", "evidence_meter", "routine_ladder", "graded_scale", "pipette", "conversion_path",
    "clinical_calendar",
}
REQUIRED_SUBOBJECT_BY_TYPE = {
    "depth_bands": "depthOfAction",
    "evidence_meter": "evidenceMeter",
    "pipette": "pipette",
    "routine_ladder": "routineLadder",
    "graded_scale": "gradedScale",
    "conversion_path": "conversionPath",
    "clinical_calendar": "clinicalCalendar",
}

# Ported verbatim from video/compositions/lib/assertion-gate.mjs so this tool
# flags the same language that gate does — never extended here by guessing
# at synonyms; that list is the one source of truth.
ABSOLUTE_MARKERS = [
    "eliminate any risk", "eliminates any risk", "eliminating any risk",
    "no risk of", "zero risk", "risk-free",
    "completely safe", "totally safe", "perfectly safe", "absolutely safe",
    "100% safe", "entirely safe", "fully biocompatible", "harmless", "non-toxic",
    "cannot cause", "never causes", "no side effects", "guaranteed",
    "clinically proven", "proven to",
    "highly recommended during pregnancy", "non-teratogenic",
    "negligible risk", "zero active irritation",
]
ASSERTION_MARKERS = [
    "proven", "shown to", "demonstrated", "significantly",
    "reduces", "reducing", "improves", "improving", "accelerates", "accelerating",
    "stimulates", "stimulating", "prevents", "preventing", "treats", "treating",
    "heals", "healing", "safe for", "suitable for", "boosts", "boosting",
    "restores", "restoring", "protects against", "inhibits", "inhibiting",
    "promoting",
]

SOURCE_ID_RE = re.compile(r"ING-[a-z0-9-]+-S\d+", re.IGNORECASE)

HANGUL_LO, HANGUL_HI = 0xAC00, 0xD7A3

# Grounded in this repo's own real text, not guessed synonyms: "refusal" /
# "refused" / "test artifact" / "never published" / "proof only" are the
# actual on-screen wording found in video/proof/*/*-refusal-*.png captions
# and _korean-probe-description.md — real harness vocabulary that should
# never reach a video/out/ render. The template/slot entries are generic
# build-time leakage (an interpolation that silently failed).
INTERNAL_STRING_MARKERS = [
    "i cannot", "i can't", "i'm unable", "i am unable", "as an ai",
    "cannot provide", "i apologize", "i'm sorry, but",
    "refusal", "refused", "test artifact", "never published", "proof only",
    "harness", "demo mode", "preview only",
    "{{", "undefined", "nan", "[object object]",
    "todo:", "fixme", "lorem ipsum", "placeholder",
]


def validate(script):
    """Mirrors build.mjs's own validation pass. Returns a list of issue strings."""
    issues = []
    if script.get("aspect") not in ("1080x1920", "1920x1080"):
        issues.append(f'unsupported aspect {script.get("aspect")!r}')
    scenes = script.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        issues.append("scenes[] must be a non-empty array")
        return issues
    if script.get("audio") != "none":
        issues.append(f'audio must be "none" (got {script.get("audio")!r})')

    cursor = 0
    for i, s in enumerate(scenes):
        if s.get("type") not in VALID_SCENE_TYPES:
            issues.append(f'scene {i}: unknown type {s.get("type")!r}')
        if s.get("startSeconds") != cursor:
            issues.append(f'scene {i}: startSeconds {s.get("startSeconds")} != expected {cursor} (scenes must be contiguous)')
        if not (s.get("endSeconds", 0) > s.get("startSeconds", 0)):
            issues.append(f"scene {i}: endSeconds must exceed startSeconds")
        if s.get("type") == "comparison" and len(s.get("comparisonItems") or []) < 2:
            issues.append(f"scene {i}: type \"comparison\" requires 2+ comparisonItems")
        if s.get("type") == "enumeration" and len(s.get("enumerationItems") or []) < 1:
            issues.append(f"scene {i}: type \"enumeration\" requires 1+ enumerationItems")
        if s.get("empty") and not s.get("emptyReason"):
            issues.append(f"scene {i}: empty=true requires a non-empty emptyReason")
        v = s.get("visual")
        if v:
            vt = v.get("type")
            if vt not in VALID_VISUAL_TYPES:
                issues.append(f'scene {i}: unknown visual.type {vt!r}')
            icons = v.get("icons") or []
            if vt != "none" and not icons and not v.get("absentReason"):
                issues.append(f'scene {i}: visual.type {vt!r} with zero icons needs an absentReason')
            if icons and not v.get("derivedFrom"):
                issues.append(f"scene {i}: visual carries icons but no derivedFrom")
            required_sub = REQUIRED_SUBOBJECT_BY_TYPE.get(vt)
            if required_sub and not v.get(required_sub):
                issues.append(f'scene {i}: visual.type {vt!r} requires a "{required_sub}" sub-object')
        cursor = s.get("endSeconds", cursor)

    duration = script.get("durationSeconds")
    if duration is None or abs(cursor - duration) > 1e-9:
        issues.append(f"durationSeconds ({duration}) != last scene's endSeconds ({cursor})")
    return issues


def fmt_time(seconds):
    if seconds is None:
        return "?"
    m, s = divmod(int(round(seconds)), 60)
    return f"{m}:{s:02d}"


def scene_summary(s):
    headline = next((b.get("text") for b in (s.get("textBlocks") or []) if b.get("role") == "headline"), None)
    visual = s.get("visual") or {}
    return {
        "start": s.get("startSeconds"),
        "end": s.get("endSeconds"),
        "type": s.get("type"),
        "headline": headline,
        "visual": visual.get("type", "none"),
        "sources": s.get("sourceIds") or [],
        "empty": bool(s.get("empty")),
        "emptyReason": s.get("emptyReason"),
    }


# ---- generic tree walkers: gather source ids / text snippets from anywhere
# in a scene, including nested visual sub-objects, without hand-enumerating
# every field name from the schema. New sub-object shapes are picked up
# automatically as long as they follow the existing *SourceId / sourceIds /
# text / "reasonable expectation" / notes{} naming this schema already uses.

# Fields that end in "SourceId" but name a CLAIM id for internal bookkeeping
# rather than a citation meant to resolve in the record's own Source Tracker
# — e.g. clinicalCalendar.longestStudyDurationSourceId exists purely for
# this tool's/build.mjs's own console report and is never rendered on
# screen (see script.schema.json's own field description). Included here
# would be a false positive: it correctly never resolves against Section
# 13, but not because anything is wrong.
NOT_A_CITATION_FIELDS = {"longestStudyDurationSourceId"}


def collect_source_ids(node, out):
    if isinstance(node, dict):
        for k, v in node.items():
            if k in NOT_A_CITATION_FIELDS:
                continue
            if k == "sourceIds" and isinstance(v, list):
                for item in v:
                    if isinstance(item, str):
                        out.update(p.strip() for p in item.split("·"))
            elif k.lower().endswith("sourceid") and isinstance(v, str):
                out.update(p.strip() for p in v.split("·"))
            else:
                collect_source_ids(v, out)
    elif isinstance(node, list):
        for item in node:
            collect_source_ids(item, out)


def collect_texts(node, out):
    if isinstance(node, dict):
        for k, v in node.items():
            if k in ("text", "reasonable expectation") and isinstance(v, str) and v.strip():
                out.append(v)
            elif k == "notes" and isinstance(v, dict):
                out.extend(t for t in v.values() if isinstance(t, str) and t.strip())
            else:
                collect_texts(v, out)
    elif isinstance(node, list):
        for item in node:
            collect_texts(item, out)


def scan_markers(texts):
    absolute_hits, qualified_hits = [], []
    for t in texts:
        low = t.lower()
        for m in ABSOLUTE_MARKERS:
            if m in low:
                absolute_hits.append((m, t))
        for m in ASSERTION_MARKERS:
            if m in low:
                qualified_hits.append((m, t))
    return absolute_hits, qualified_hits


def has_no_source_record(value):
    return not value or str(value).strip().lower().startswith("none")


def section13_ids(record_path: Path):
    text = record_path.read_text(encoding="utf-8", errors="ignore")
    section13 = text.split("\n## 13.")
    if len(section13) < 2:
        return None  # no such section — different doc shape, not "empty"
    body = section13[1].split("\n## 14.")[0]
    return set(m.upper() for m in SOURCE_ID_RE.findall(body))


def find_repo_root(script_path: Path):
    # script lives at <repo_root>/video/scripts/<handle>.json
    parts = script_path.parts
    if "video" in parts and "scripts" in parts:
        vi = len(parts) - 1 - parts[::-1].index("video")
        return Path(*parts[:vi])
    return None


def extract_thumb(video_path: Path, at_seconds: float, width: int = 200):
    """Same technique as storyboard.py's own extract_video_thumb: one frame,
    scaled, embedded as a data URI so the report stays one self-contained
    file — nothing to keep alongside it or lose track of."""
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tf:
        tmp = Path(tf.name)
    try:
        r = subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-ss", f"{max(at_seconds, 0):.3f}", "-i", str(video_path),
             "-frames:v", "1", "-vf", f"scale={width}:-2", "-q:v", "4", str(tmp)],
            capture_output=True, timeout=15,
        )
        if r.returncode == 0 and tmp.exists() and tmp.stat().st_size > 0:
            return "data:image/jpeg;base64," + base64.b64encode(tmp.read_bytes()).decode()
        return None
    except Exception:
        return None
    finally:
        try:
            tmp.unlink()
        except FileNotFoundError:
            pass


def probe_duration(path: Path):
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
            capture_output=True, text=True, timeout=10,
        )
        return float(r.stdout.strip())
    except Exception:
        return None


def resolve_input(script, repo_root):
    raw = script.get("sourceRecord")
    if has_no_source_record(raw):
        return {"declared": raw, "path": None, "exists": False, "no_record_by_design": True, "source_ids": None}
    if repo_root is None:
        return {"declared": raw, "path": None, "exists": False, "no_record_by_design": False, "source_ids": None}
    record_path = (repo_root / raw).resolve()
    if not record_path.is_file():
        return {"declared": raw, "path": record_path, "exists": False, "no_record_by_design": False, "source_ids": None}
    ids = section13_ids(record_path)
    return {"declared": raw, "path": record_path, "exists": True, "no_record_by_design": False, "source_ids": ids}


def embed_scaled_image(path: Path, width: int = 200):
    """Same technique as extract_thumb, for a static PNG/JPG instead of a
    video frame — ffmpeg re-encodes either one, so one helper covers both."""
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tf:
        tmp = Path(tf.name)
    try:
        r = subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", str(path), "-frames:v", "1",
             "-vf", f"scale={width}:-2", "-q:v", "5", str(tmp)],
            capture_output=True, timeout=15,
        )
        if r.returncode == 0 and tmp.exists() and tmp.stat().st_size > 0:
            return "data:image/jpeg;base64," + base64.b64encode(tmp.read_bytes()).decode()
        return None
    except Exception:
        return None
    finally:
        try:
            tmp.unlink()
        except FileNotFoundError:
            pass


# Fallback thumbnail source for a scene whose OWN script has no video/out/
# render yet (not built this cycle, e.g. ginseng/retinal-vs-retinol — or
# built through a component's own standalone build-proof.mjs, which never
# produces a scripts/*.json this tool can even see, e.g. pipette-v5-proof.mp4
# existing with no _pipette-v5-proof.json anywhere). video/proof/<name>/ still
# holds real, committed evidence of what that VISUAL COMPONENT looks like,
# even when this particular script was never rendered — falling back to it
# beats a blank box. Deliberately excludes routine_ladder: its only proof/
# folder ("routineladder") is the NOT-YET-WIRED v3 candidate, not what the
# live six-rung component renders — showing it here would silently repeat
# the exact live/retired confusion already found and labeled once in the
# Story Board app's own folder picker (see design/component-registry.md and
# scripts/regen-proof-frames.mjs's own manifest, cross-checked 2026-08-25).
LIVE_COMPONENT_PROOF_FOLDERS = {
    "depth_bands": "depthofaction-v2",
    "clinical_calendar": "clinicalcalendar",
    "conversion_path": "conversionpath",
    "pipette": "pipette",
    "evidence_meter": "meters-v3",
    "graded_scale": "meters-v3",
}


def find_component_reference_frame(visual_raw, repo_root):
    if repo_root is None:
        return None
    vtype = visual_raw.get("type")
    if vtype == "label_artifact":
        folder = "brandmark" if "brand-glyph" in (visual_raw.get("icons") or []) else "routeicon"
    else:
        folder = LIVE_COMPONENT_PROOF_FOLDERS.get(vtype)
    if not folder:
        return None
    proof_dir = repo_root / "video" / "proof" / folder
    if not proof_dir.is_dir():
        return None
    candidates = sorted(proof_dir.glob("*.png"))
    for p in candidates:
        low = p.name.lower()
        if "refusal" not in low and "empty" not in low:
            return p
    return candidates[0] if candidates else None


def resolve_output(script, repo_root):
    handle = script.get("handle")
    if not handle or repo_root is None:
        return []
    out_dir = repo_root / "video" / "out"
    if not out_dir.is_dir():
        return []
    matches = sorted(out_dir.glob(f"*{handle}*.mp4"))
    results = []
    for m in matches:
        dur = probe_duration(m)
        results.append({
            "path": m,
            "size_bytes": m.stat().st_size,
            "duration": dur,
        })
    return results


# ---- pixel-level render checks: everything below inspects the ACTUAL
# rendered frame, never the script's declared intent, since that's the
# whole point (a script can declare correct text and still render it
# wrong). Degrades gracefully — every function here returns
# {"available": False} rather than raising when Pillow/numpy/tesseract
# aren't installed, so the rest of the tool keeps working either way.

_ocr_broken = False


def pil_to_data_uri(img, fmt="PNG"):
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    mime = "image/png" if fmt.upper() == "PNG" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(buf.getvalue()).decode()


def extract_full_frame(video_path: Path, at_seconds: float, width: int = 900):
    """Same technique as extract_thumb, but PNG (not JPEG) and wide enough
    to actually resolve individual glyph strokes — the 200px display
    thumbnail is too small to tell a dropped glyph from a rendering
    artifact. Returns a PIL Image (pixels loaded into memory) or None."""
    if not _HAS_IMAGING:
        return None
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tf:
        tmp = Path(tf.name)
    try:
        r = subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-ss", f"{max(at_seconds, 0):.3f}", "-i", str(video_path),
             "-frames:v", "1", "-vf", f"scale={width}:-2", str(tmp)],
            capture_output=True, timeout=15,
        )
        if r.returncode == 0 and tmp.exists() and tmp.stat().st_size > 0:
            return Image.open(tmp).convert("RGB")
        return None
    except Exception:
        return None
    finally:
        try:
            tmp.unlink()
        except FileNotFoundError:
            pass


def ocr_text(img, lang="eng"):
    """Wraps pytesseract; returns None (never raises) the moment OCR proves
    unavailable — missing module or missing tesseract binary look the same
    from here — and stays None for the rest of this run so a broken install
    doesn't cost a subprocess attempt per scene."""
    global _ocr_broken
    if not _HAS_OCR or _ocr_broken:
        return None
    try:
        return pytesseract.image_to_string(img, lang=lang)
    except Exception:
        _ocr_broken = True
        return None


def hangul_count(text):
    return sum(1 for ch in (text or "") if HANGUL_LO <= ord(ch) <= HANGUL_HI)


def check_internal_strings(text):
    """Scans OCR'd on-screen text for leaked harness/refusal/template
    chrome. See INTERNAL_STRING_MARKERS's own comment for where each phrase
    is grounded in this repo's real proof-harness vocabulary."""
    if not text:
        return []
    low = text.lower()
    return [m for m in INTERNAL_STRING_MARKERS if m in low]


def _significant_words(text):
    return [w for w in re.findall(r"[a-zA-Z0-9']+", text.lower()) if len(w) > 2]


def check_claim_on_screen(expected_text, ocr_raw):
    """Fuzzy word-overlap, not exact string match or a raw similarity ratio
    on the full strings — OCR preserves word boundaries far better than
    exact characters (confirmed directly: "First: what it is." came back as
    "First: what itis." — one dropped space, otherwise perfect), and a
    substring compiled claim inside a longer OCR'd frame would score low on
    whole-string similarity even when every word is actually present."""
    if not expected_text:
        return {"skipped": True, "reason": "no headline text to check"}
    if hangul_count(expected_text) > 0:
        return {"skipped": True, "reason": "contains Korean text — see the glyph check instead (OCR tested unreliable on this pipeline's mixed Korean/Latin headings, confirmed across every page-segmentation mode; not attempted here rather than silently guessing)"}
    if ocr_raw is None:
        return {"skipped": True, "reason": "OCR unavailable (pytesseract/tesseract not installed)"}
    expected_words = _significant_words(expected_text)
    if not expected_words:
        return {"skipped": True, "reason": "no significant words to check"}
    ocr_words = _significant_words(ocr_raw)
    ocr_word_set = set(ocr_words)
    found = 0
    for w in expected_words:
        if w in ocr_word_set:
            found += 1
        elif len(w) >= 4 and any(w in tok for tok in ocr_words):
            # OCR occasionally merges two adjacent on-screen words with no
            # space between them — confirmed for real, not hypothetical:
            # this pipeline's own "Same route, over time." rendered
            # correctly on screen but OCR'd as "...overtime.", which an
            # exact-token match would wrongly score as two missing words.
            # A substring hit against a single OCR token still counts.
            found += 1
    ratio = found / len(expected_words)
    return {"skipped": False, "ratio": ratio, "match": ratio >= 0.7, "ocr_text": ocr_raw.strip()}


def _ink_mask(gray_arr, bg, thresh=28):
    return np.abs(gray_arr.astype(int) - bg) > thresh


def _line_bands(mask, min_frac=0.01, min_gap=4):
    """Row-wise ink projection: segments a frame into text-line bands
    without needing to know where any text block sits on screen."""
    h, w = mask.shape
    row_ink = mask.sum(axis=1)
    is_text_row = row_ink > (w * min_frac)
    bands, start, gap = [], None, 0
    for y, is_text in enumerate(is_text_row):
        if is_text:
            start, gap = (start if start is not None else y), 0
        elif start is not None:
            gap += 1
            if gap > min_gap:
                bands.append((start, y - gap))
                start, gap = None, 0
    if start is not None:
        bands.append((start, h - 1))
    return bands


def _col_blobs(mask, y0, y1, min_gap=2):
    """Column-wise ink projection within one line band: segments that line
    into individual glyph blobs."""
    band = mask[y0:y1 + 1, :]
    is_ink = band.sum(axis=0) > 0
    blobs, start, gap = [], None, 0
    for x, v in enumerate(is_ink):
        if v:
            start, gap = (start if start is not None else x), 0
        elif start is not None:
            gap += 1
            if gap > min_gap:
                blobs.append((start, x - gap))
                start, gap = None, 0
    if start is not None:
        blobs.append((start, len(is_ink) - 1))
    return blobs


def check_korean_glyphs(img, expected_text):
    """Pixel-only glyph-presence check — deliberately NOT OCR, and NOT a
    font-manifest lookup (a font can declare Hangul coverage and still fall
    back silently at runtime; a manifest check would miss exactly that).
    Tesseract was tried first: tested directly against this pipeline's own
    real "PDRN · 피디알엔" render across every page-segmentation mode and
    consistently misread it as Latin-lookalike garbage, so it isn't used
    here at all rather than shipping an unreliable check that looks
    sophisticated.

    Instead: segment the frame into text-line bands by row-wise ink
    projection, then within each band count "squarish" ink blobs — Hangul
    syllable blocks are drawn to fit a square em, unlike variable-width
    Latin letters, so a real glyph count falls out of shape alone with no
    need to recognize WHAT each character is. Picks whichever band's
    square-blob count comes closest to the source text's own Hangul syllable
    count. Verified before shipping: exact match against a real render, and
    a synthetic single-glyph dropout (one syllable blanked out, simulating
    the real missing-디-in-피디알엔 failure class) correctly came back short
    by 1 in the matching band."""
    if not _HAS_IMAGING:
        return {"available": False}
    expected = hangul_count(expected_text)
    if expected == 0:
        return {"available": False}
    arr = np.array(img.convert("L"))
    bg = int(np.median(arr))
    mask = _ink_mask(arr, bg)
    best = None
    for (y0, y1) in _line_bands(mask):
        blobs = _col_blobs(mask, y0, y1)
        h = y1 - y0
        square = [b for b in blobs if h > 6 and 0.6 <= (b[1] - b[0]) / h <= 1.5]
        count = len(square)
        dist = abs(count - expected)
        if best is None:
            best = (y0, y1, count)
            continue
        best_dist = abs(best[2] - expected)
        # On a tied distance, prefer the candidate at or above the expected
        # count over one below it. Found for real on a short (2-syllable)
        # Hangul string: the actual line ("Ginseng · 인삼") picked up one
        # extra square-ish blob from the capital "G" (3 found vs. 2
        # expected, distance 1) and tied with an unrelated line that
        # happened to have exactly 1 blob (also distance 1) — first-found
        # tiebreaking kept the wrong line and reported a false "short by 1"
        # on a render that was actually correct. A stray extra blob from a
        # nearby Latin letter is far more likely than an unrelated line
        # coincidentally landing exactly one glyph short, so ties resolve
        # toward the read that doesn't imply a dropped glyph.
        if dist < best_dist or (dist == best_dist and count >= expected > best[2]):
            best = (y0, y1, count)
    if best is None:
        return {"available": True, "expected": expected, "found": 0, "status": "no_line_found", "band_uri": None}
    y0, y1, found = best
    status = "match" if found == expected else ("short" if found < expected else "extra")
    pad = 6
    crop = img.crop((0, max(0, y0 - pad), img.width, min(img.height, y1 + pad)))
    crop = crop.resize((crop.width * 2, crop.height * 2))
    return {"available": True, "expected": expected, "found": found, "status": status, "band_uri": pil_to_data_uri(crop)}


def check_frame_zero(video_path):
    """The scroll-stop frame (t=0, what a Shorts viewer sees before playback
    starts) should be the dense final built state, not blank or mid-fade —
    checked here by comparing pixel-density (grayscale stdev) against a
    settled frame a beat later, not by trusting that t=0 "should" already be
    composed. Confirmed on real content this matters: pdrn-short.mp4's own
    t=0 is genuinely blank, its own hook scene hasn't entrance-animated in
    yet at the very first frame."""
    if not _HAS_IMAGING:
        return {"available": False}
    f0 = extract_full_frame(video_path, 0.0, width=540)
    settled = extract_full_frame(video_path, 0.6, width=540)
    if f0 is None or settled is None:
        return {"available": False}
    d0 = float(np.array(f0.convert("L")).std())
    d1 = float(np.array(settled.convert("L")).std())
    sparse = d1 > 0 and d0 < d1 * 0.35
    return {
        "available": True, "frame0_density": d0, "settled_density": d1,
        "status": "sparse" if sparse else "ok",
        "frame0_uri": pil_to_data_uri(f0, "JPEG"), "settled_uri": pil_to_data_uri(settled, "JPEG"),
    }


def run_acceptance_harness(repo_root: Path, handle: str):
    """Shells out to the video repo's OWN render gate
    (video/scripts/acceptance-harness.mjs, rules A-I: internal strings,
    legibility floor, Korean glyphs, frame zero, caption collision,
    start-of-scene flash, badge-alpha override, safe-area placement)
    instead of reimplementing any of it here. Two reasons: those rules are
    actively maintained against real content (the 27px legibility floor was
    only finalized 2026-08-25), and a second, hand-rolled copy in this tool
    would just be one more place for the two to quietly disagree. Evidence
    mode is used for probe/demo scripts (leading-underscore handle, same
    convention Story Board.applescript already keys off of) since rule A's
    strict reading is specifically wrong for their intentional "Refusal —"
    fixture text. Degrades gracefully like every other check here: no repo
    root, no built composition, or no `node` on PATH all report as
    unavailable rather than raising."""
    if repo_root is None:
        return {"available": False, "reason": "could not resolve the video repo root"}
    video_dir = repo_root / "video"
    comp_dir = video_dir / "compositions" / handle
    if not (comp_dir / "index.html").is_file():
        return {"available": False, "reason": f"no built composition at {comp_dir}"}
    cmd = ["node", "scripts/acceptance-harness.mjs", str(comp_dir)]
    if handle.startswith("_"):
        cmd.append("--evidence")
    try:
        r = subprocess.run(cmd, cwd=str(video_dir), capture_output=True, text=True, timeout=120)
    except FileNotFoundError:
        return {"available": False, "reason": "node not found on PATH"}
    except subprocess.TimeoutExpired:
        return {"available": False, "reason": "timed out after 120s (browser launch/render taking too long)"}
    out = r.stdout or ""
    findings = []
    for line in out.splitlines():
        m = re.match(r"^\s+\[([^\]]+)\]\s+(.+?)\s+—\s+(.*)$", line)
        if m:
            findings.append({"rule": m.group(1), "where": m.group(2), "detail": m.group(3)})
    summary_line = next((ln.strip() for ln in out.splitlines() if ln.strip()[:1] in ("✓", "✗")), "")
    summary = summary_line[1:].strip() if summary_line else ""
    return {
        "available": True, "passed": r.returncode == 0, "summary": summary,
        "findings": findings, "raw": (out + (r.stderr or "")).strip(),
    }


def find_invisible_scene_sourcing(scenes_raw):
    """compositions/lib/artifacts.mjs's own caption/transcript generator only
    emits a visible citation line when scene.type === "claim" (verified
    directly at that file's own line 108, with the other Claude session
    working this same repo). comparison/enumeration scenes cite through
    their own per-item sourceIds instead — a separate, still-real path, so
    they're excluded here, not silently missed. Any OTHER scene type
    (hook/identity/end_card/sources) carrying scene-level sourceIds would be
    sourced in the data but never rendered — true of no real script today,
    but the schema and validate-manifest.mjs both allow it structurally, so
    a future script could add one and nothing else would catch it."""
    findings = []
    for i, s in enumerate(scenes_raw):
        if s.get("type") in ("claim", "comparison", "enumeration"):
            continue
        if s.get("sourceIds"):
            findings.append({"scene_index": i, "type": s.get("type"), "source_ids": s["sourceIds"]})
    return findings


def load_feedback_sidecar(path: Path):
    """Read a storyline_<handle>.feedback.json previously downloaded from
    this report's own "Save feedback (.json)" button — same idea as
    storyboard.py's own load_notes_sidecar. Never raises; a missing or
    malformed sidecar shouldn't block a normal run."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"  warning: could not read feedback file {path}: {e}")
        return {}
    scenes = data.get("scenes") if isinstance(data, dict) else None
    if not isinstance(scenes, dict):
        print(f"  warning: {path} is not a feedback-file object, ignoring")
        return {}
    return scenes


def check_identity_scene_language(scenes_raw):
    """Identity scenes are nominal-only by design — name, INCI, category,
    the one mechanism-grounded sentence (see STORYBOARD.md's own Frame 2
    notes). Even a SOURCED efficacy/evidence-grade/gentleness claim there is
    wrong, because identity is supposed to say what something IS, never what
    it does — that's what "claim" scenes are for. Scoped to just each
    identity scene's own text (not the whole script), since the exact same
    phrase inside a "claim" scene is precisely the content those scenes
    exist to carry."""
    findings = []
    for i, s in enumerate(scenes_raw):
        if s.get("type") != "identity":
            continue
        texts = []
        collect_texts(s, texts)
        abs_hits, qual_hits = scan_markers(texts)
        for marker, text in abs_hits:
            findings.append({"scene_index": i, "tier": "absolute", "marker": marker, "text": text})
        for marker, text in qual_hits:
            findings.append({"scene_index": i, "tier": "assertive", "marker": marker, "text": text})
    return findings


def build_audit(script, repo_root):
    script_ids = set()
    collect_source_ids(script.get("scenes", []), script_ids)

    texts = []
    collect_texts(script.get("scenes", []), texts)
    absolute_hits, qualified_hits = scan_markers(texts)

    input_info = resolve_input(script, repo_root)
    unresolved = None
    if input_info["source_ids"] is not None:
        # Case-insensitive: the record's own table and the script's own
        # authored ids both use "ING-<handle>-S0NN" by convention, but
        # nothing guarantees identical casing between the two, so compare
        # normalized while keeping each side's own original casing for
        # display (a real bug here once compared ING-PDRN-S001 against
        # ING-pdrn-S001 and silently flagged every real id as unresolved).
        resolved_upper = {s.upper() for s in input_info["source_ids"]}
        unresolved = sorted(s for s in script_ids if s.upper() not in resolved_upper)

    output_info = resolve_output(script, repo_root)
    invisible_sourcing = find_invisible_scene_sourcing(script.get("scenes", []))
    identity_language = check_identity_scene_language(script.get("scenes", []))

    return {
        "script_ids": sorted(script_ids),
        "unresolved_ids": unresolved,
        "absolute_hits": absolute_hits,
        "qualified_hits": qualified_hits,
        "input": input_info,
        "output": output_info,
        "invisible_sourcing": invisible_sourcing,
        "identity_language": identity_language,
    }


PAGE_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Storyline — __TITLE__</title>
<style>
  :root{
    --bg:#1C1A17; --card:#2C2720; --card-edge:#3A342A;
    --amber:#E8A33D; --amber-dim:#8A6528; --teal:#4F9B8E;
    --text:#F0EBE3; --text-muted:#9C948A; --text-faint:#9A8E7C; --danger:#C96A4F;
  }
  *{box-sizing:border-box;}
  body{margin:0;background:radial-gradient(ellipse at top left, rgba(232,163,61,0.05), transparent 55%), var(--bg);
    color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;min-height:100vh;}
  .mono{font-family:"SF Mono","JetBrains Mono",Consolas,"Courier New",monospace;}
  header{padding:28px 32px 20px;border-bottom:1px solid var(--card-edge);}
  header h1{margin:0 0 4px;font-size:22px;font-weight:700;}
  header p{margin:0;color:var(--text-muted);font-size:13px;}
  .meta{display:flex;gap:18px;flex-wrap:wrap;margin-top:14px;font-size:12px;color:var(--text-muted);}
  .meta b{color:var(--text);}
  main{padding:24px 32px 60px;max-width:760px;margin:0 auto;}
  h2.section{font-size:13px;text-transform:uppercase;letter-spacing:.06em;color:var(--text-faint);
    margin:36px 0 12px;padding-top:20px;border-top:1px solid var(--card-edge);scroll-margin-top:20px;}
  h2.section:first-of-type{margin-top:0;padding-top:0;border-top:none;}
  .status{display:flex;align-items:center;gap:10px;padding:14px 18px;border-radius:10px;margin-bottom:16px;font-weight:600;font-size:14px;}
  .status.ok{background:rgba(79,155,142,0.15);border:1px solid var(--teal);color:var(--teal);}
  .status.bad{background:rgba(201,106,79,0.15);border:1px solid var(--danger);color:var(--danger);}
  .status.warn{background:rgba(232,163,61,0.15);border:1px solid var(--amber);color:var(--amber);}
  .issues{list-style:none;margin:0 0 16px;padding:0;display:flex;flex-direction:column;gap:6px;}
  .issues li{background:var(--card);border:1px solid var(--danger);border-left:3px solid var(--danger);
    border-radius:6px;padding:8px 12px;font-size:12.5px;color:var(--text);}
  .card{background:var(--card);border:1px solid var(--card-edge);border-radius:8px;padding:14px 16px;margin-bottom:10px;font-size:13px;}
  .card .path{font-size:11.5px;color:var(--text-faint);word-break:break-all;}
  /* Image and text stay side by side (row), just at a much bigger image
     size than the original 96px postage stamp — 240px is closer to
     mobile-screen scale and actually reviewable, while still leaving room
     for the text column beside it. align-self:flex-start keeps the image
     from stretching to match the (usually taller) text column's height. */
  .scene{display:flex;gap:16px;padding:18px 0;border-top:1px solid var(--card-edge);}
  .scene:first-of-type{border-top:none;}
  .scene-thumb{flex-shrink:0;align-self:flex-start;width:240px;border-radius:10px;display:block;
    background:#000;aspect-ratio:9/16;object-fit:contain;}
  .scene-thumb-wrap{flex-shrink:0;align-self:flex-start;width:240px;}
  .scene-thumb-wrap .scene-thumb{width:100%;}
  .thumb-caption{font-size:10px;color:var(--text-faint);text-align:center;margin-top:5px;line-height:1.3;}
  .scene-thumb.placeholder{flex-shrink:0;align-self:flex-start;width:240px;aspect-ratio:9/16;display:flex;
    align-items:center;justify-content:center;text-align:center;font-size:11px;color:var(--text-faint);
    border:1px dashed var(--card-edge);padding:6px;}
  .scene-time{flex-shrink:0;width:60px;font-size:12px;color:var(--text-faint);padding-top:2px;}
  .scene-body{flex:1;min-width:0;}
  .feedback-label{font-size:10px;text-transform:uppercase;letter-spacing:.06em;color:var(--text-faint);margin:12px 0 6px;}
  .feedback-row{display:flex;gap:10px;align-items:flex-start;}
  .feedback-imgname{flex-shrink:0;width:110px;padding-top:11px;font-size:10.5px;color:var(--text-faint);word-break:break-word;}
  .feedback-note{flex:1;min-width:0;box-sizing:border-box;padding:10px 12px;border-radius:8px;resize:vertical;min-height:52px;
    background:rgba(232,163,61,0.06);border:1px solid var(--card-edge);color:var(--text);
    font-family:inherit;font-size:12.5px;line-height:1.4;}
  .feedback-note:focus{outline:none;border-color:var(--amber-dim);}
  .feedback-note::placeholder{color:var(--text-faint);}
  .header-actions{margin-top:14px;}
  .btn{font-size:12px;font-weight:600;padding:8px 16px;border-radius:8px;border:1px solid var(--amber-dim);
    background:rgba(232,163,61,0.12);color:var(--amber);cursor:pointer;font-family:inherit;}
  .btn:hover{background:rgba(232,163,61,0.2);border-color:var(--amber);}
  .toast{position:fixed;left:50%;bottom:28px;transform:translateX(-50%) translateY(20px);background:var(--card);
    border:1px solid var(--amber-dim);color:var(--text);padding:10px 18px;border-radius:8px;font-size:12.5px;
    opacity:0;pointer-events:none;transition:opacity .2s,transform .2s;white-space:pre-line;text-align:center;
    max-width:80%;z-index:50;}
  .toast.show{opacity:1;transform:translateX(-50%) translateY(0);}
  .review-player{display:block;margin:0 auto;width:360px;max-width:100%;max-height:70vh;
    border-radius:12px;background:#000;border:1px solid var(--card-edge);}
  .source-data{margin-top:10px;background:rgba(232,163,61,0.07);border:1px solid var(--amber-dim);
    border-radius:6px;padding:10px 12px;}
  .source-data-label{font-size:10px;text-transform:uppercase;letter-spacing:.06em;color:var(--amber);
    font-weight:700;margin-bottom:6px;}
  .derived-from{margin:0 0 8px;font-size:12.5px;color:var(--text);line-height:1.4;}
  .derived-from:last-child{margin-bottom:0;}
  .raw-data{margin:0;font-size:11px;line-height:1.5;color:var(--text-muted);white-space:pre-wrap;word-break:break-word;}
  .scene-tags{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:6px;}
  .tag{font-size:10.5px;font-weight:700;text-transform:uppercase;letter-spacing:.04em;padding:3px 9px;border-radius:999px;}
  .tag.type{background:var(--card-edge);color:var(--text-muted);}
  .tag.visual{background:rgba(232,163,61,0.18);color:var(--amber);}
  .tag.visual.none{background:transparent;color:var(--text-faint);border:1px solid var(--card-edge);}
  .tag.empty{background:rgba(201,106,79,0.18);color:var(--danger);}
  .headline{font-size:15px;font-weight:600;margin:0 0 6px;}
  .headline.faint{color:var(--text-faint);font-weight:400;font-style:italic;}
  .sources{display:flex;gap:6px;flex-wrap:wrap;}
  .source-chip{font-size:10.5px;font-family:"SF Mono","JetBrains Mono",Consolas,monospace;
    color:var(--teal);border:1px solid var(--teal);border-radius:5px;padding:1px 7px;}
  .source-chip.bad{color:var(--danger);border-color:var(--danger);}
  .source-chip.small{font-size:9.5px;padding:0 5px;}
  .no-sources{font-size:11.5px;color:var(--text-faint);}
  .compare-row{display:flex;gap:10px;margin:8px 0;}
  .compare-col{flex:1;min-width:0;background:var(--card);border:1px solid var(--card-edge);border-radius:6px;padding:10px 12px;}
  .compare-label{font-size:10px;text-transform:uppercase;letter-spacing:.06em;color:var(--teal);font-weight:700;margin-bottom:4px;}
  .compare-text{font-size:12.5px;margin:0 0 6px;line-height:1.4;}
  .enum-list{display:flex;flex-direction:column;gap:8px;margin:8px 0;}
  .enum-row{display:flex;gap:10px;align-items:flex-start;}
  .enum-index{flex-shrink:0;color:var(--teal);font-size:12px;padding-top:1px;}
  .marker-hit{background:var(--card);border-left:3px solid var(--danger);border-radius:6px;padding:8px 12px;margin-bottom:6px;font-size:12.5px;}
  .marker-hit.qualified{border-left-color:var(--amber);}
  .marker-hit b{font-family:"SF Mono",monospace;}
  .caveat{font-size:11.5px;color:var(--text-faint);margin-top:8px;font-style:italic;}
  .raw-data-toggle{margin-top:10px;}
  .raw-data-toggle summary{cursor:pointer;font-size:10.5px;text-transform:uppercase;letter-spacing:.06em;
    color:var(--amber-dim);font-weight:700;}
  .raw-data-toggle summary:hover{color:var(--amber);}
  .raw-data-toggle[open] summary{margin-bottom:8px;}
  .raw-data-toggle .raw-data{margin-top:0;}
  nav.section-nav{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px;}
  nav.section-nav a{font-size:11.5px;text-decoration:none;color:var(--text-muted);
    border:1px solid var(--card-edge);border-radius:999px;padding:5px 12px;transition:border-color .12s,color .12s;}
  nav.section-nav a:hover{border-color:var(--amber);color:var(--amber);}
  .check-row{border-radius:6px;padding:8px 12px;margin-bottom:8px;font-size:12.5px;background:var(--card);
    border-left:3px solid var(--card-edge);}
  .check-row.bad{border-left-color:var(--danger);}
  .evidence-row{display:flex;gap:14px;flex-wrap:wrap;margin:10px 0;}
  .evidence-img{max-width:100%;border-radius:6px;border:1px solid var(--card-edge);display:block;}
</style>
</head>
<body>
<header>
  <h1>__TITLE__</h1>
  <p class="mono">__SOURCE_PATH__</p>
  <div class="meta">
    <span><b>handle</b> __HANDLE__</span>
    <span><b>aspect</b> __ASPECT__</span>
    <span><b>duration</b> __DURATION__s</span>
    <span><b>scenes</b> __SCENE_COUNT__</span>
  </div>
  <nav class="section-nav">
    <a href="#validation">Validation</a>
    <a href="#input">Input</a>
    <a href="#storyline">Storyline</a>
    <a href="#output">Output</a>
    <a href="#render-checks">Render checks</a>
    <a href="#sourcing">Sourcing</a>
    <a href="#safety">Safety</a>
    <a href="#review">Review</a>
  </nav>
  <div class="header-actions">
    <button class="btn" onclick="exportFeedback()">Save feedback (.json)</button>
  </div>
</header>
<div class="toast" id="toast"></div>
<main>
  <h2 class="section" id="validation">Structural validation</h2>
  __STATUS_HTML__

  <h2 class="section" id="input">Input</h2>
  __INPUT_HTML__

  <h2 class="section" id="storyline">Storyline</h2>
  __SCENES_HTML__

  <h2 class="section" id="output">Output</h2>
  __OUTPUT_HTML__

  <h2 class="section" id="render-checks">Render checks</h2>
  __RENDER_CHECKS_HTML__

  <h2 class="section" id="sourcing">Sourcing audit</h2>
  __SOURCING_HTML__

  <h2 class="section" id="safety">Content-safety signals</h2>
  __SAFETY_HTML__

  <h2 class="section" id="review">Review the video</h2>
  __VIDEO_PLAYER_HTML__
</main>
<script>
  // Mirrors storyboard.py's own notes pattern: localStorage for immediate,
  // zero-effort persistence across reloads of this exact file, plus a
  // downloadable JSON sidecar for anything that needs to survive a
  // regeneration (or getting shared/moved) — storyline.py auto-loads
  // storyline_<handle>.feedback.json back in next to this report if it
  // finds one, no flag needed.
  const STORE_KEY = __STORE_KEY__;
  const STORYLINE_TITLE = __STORYLINE_TITLE__;
  const FEEDBACK_STORAGE_KEY = "storyline_feedback_" + STORE_KEY;
  const BAKED_FEEDBACK = __BAKED_FEEDBACK__;

  // localStorage throws (SecurityError) for plain file:// pages in some
  // browsers (Chrome restricts it there; confirmed directly, not assumed) —
  // isolated behind try/catch so that failure can never break the rest of
  // this script. Losing cross-reload persistence is a minor degradation;
  // an uncaught exception here would have silently broken typing AND the
  // Save button both, since every line after it would never have run.
  function readStoredFeedback() {
    try {
      const raw = localStorage.getItem(FEEDBACK_STORAGE_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch (e) {
      return null;
    }
  }
  function writeStoredFeedback(data) {
    try {
      localStorage.setItem(FEEDBACK_STORAGE_KEY, JSON.stringify(data));
    } catch (e) {
      // no durable persistence across reloads here, but in-memory state and
      // the Save-feedback download below still work fine this page load
    }
  }

  let sceneFeedback = readStoredFeedback() || BAKED_FEEDBACK;

  document.querySelectorAll(".feedback-note").forEach((ta) => {
    const idx = ta.dataset.sceneIndex;
    if (sceneFeedback[idx] !== undefined) ta.value = sceneFeedback[idx];
    ta.addEventListener("input", (e) => {
      sceneFeedback[idx] = e.target.value;
      writeStoredFeedback(sceneFeedback);
    });
  });

  function showToast(msg) {
    const t = document.getElementById("toast");
    t.textContent = msg;
    t.classList.add("show");
    setTimeout(() => t.classList.remove("show"), 3200);
  }

  function exportFeedback() {
    const name = "storyline_" + STORE_KEY + ".feedback.json";
    const payload = { handle: STORE_KEY, title: STORYLINE_TITLE, scenes: sceneFeedback, savedAt: new Date().toISOString() };
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = name;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 5000);
    showToast(`Downloaded ${name}\nKeep it next to this report — re-running storyline.py picks it up automatically.`);
  }
</script>
</body>
</html>
"""


def build_report(script_path: Path, script: dict, feedback: dict = None) -> str:
    feedback = feedback or {}
    handle = script.get("handle") or script_path.stem
    issues = validate(script)
    scenes = [scene_summary(s) for s in script.get("scenes", [])]
    repo_root = find_repo_root(script_path)
    audit = build_audit(script, repo_root)

    # --- structural validation ---
    if issues:
        issues_html = "<ul class=\"issues\">" + "".join(f"<li>{html.escape(i)}</li>" for i in issues) + "</ul>"
        status_html = f'<div class="status bad">✗ {len(issues)} issue(s) — build.mjs would refuse to render this</div>{issues_html}'
    else:
        status_html = '<div class="status ok">✓ Valid — every rule build.mjs itself checks passes</div>'

    # --- input ---
    inp = audit["input"]
    if inp["no_record_by_design"]:
        input_html = f'<div class="card">No source record by design (declared: <span class="mono">{html.escape(str(inp["declared"]))}</span>) — a reusability/probe fixture, not real content.</div>'
    elif not inp["path"]:
        input_html = f'<div class="card" style="border-color:var(--danger)">Declared source record <span class="mono">{html.escape(str(inp["declared"]))}</span> could not be resolved.</div>'
    elif not inp["exists"]:
        input_html = f'<div class="card" style="border-color:var(--danger)">Declared source record does not exist on disk:<br><span class="path mono">{html.escape(str(inp["path"]))}</span></div>'
    else:
        id_count = len(inp["source_ids"]) if inp["source_ids"] is not None else 0
        input_html = f'<div class="card">Source record found, {id_count} source id(s) in its own Section 13 ledger:<br><span class="path mono">{html.escape(str(inp["path"]))}</span></div>'

    # --- storyline (thumbnail + source data per scene) ---
    # Pick whichever resolved output's real duration actually matches this
    # script — multiple files can match the handle substring (a "-proof"
    # render alongside the real one) and thumbnails from the wrong one would
    # show the wrong cut entirely.
    output_video = None
    if audit["output"]:
        exact = [o for o in audit["output"] if o["duration"] is not None and abs(o["duration"] - script.get("durationSeconds", -1)) < 0.6]
        output_video = (exact[0] if exact else audit["output"][0])["path"]

    rows = []
    render_check_cards = []
    render_check_counts = {"scenes_checked": 0, "korean_run": 0, "korean_bad": 0, "leak_hits": 0, "claim_checked": 0, "claim_bad": 0}
    for i, (raw_scene, sc) in enumerate(zip(script.get("scenes", []), scenes)):
        time_range = f'{fmt_time(sc["start"])}–{fmt_time(sc["end"])}'
        tags = f'<span class="tag type">{html.escape(sc["type"] or "?")}</span>'
        if sc["empty"]:
            tags += f'<span class="tag empty">empty — {html.escape(sc["emptyReason"] or "no reason given")}</span>'
        visual_class = "visual none" if sc["visual"] == "none" else "visual"
        tags += f'<span class="tag {visual_class}">{html.escape(sc["visual"])}</span>'

        if sc["headline"]:
            headline_html = f'<p class="headline">{html.escape(sc["headline"])}</p>'
        else:
            headline_html = '<p class="headline faint">(no headline text block)</p>'

        # comparisonItems/enumerationItems carry the REAL content for these
        # two scene types — the scene's own headline is just a framing line
        # (e.g. "The two forms don't take the same path to work."); the
        # actual compared claims, and their own per-item sourceIds (which
        # the schema allows to differ from the scene-level ones), live one
        # level deeper. Missing this meant half of retinal-vs-retinol's own
        # scenes rendered with no visible content at all.
        comparison_items = raw_scene.get("comparisonItems")
        enumeration_items = raw_scene.get("enumerationItems")
        items_html = ""

        def _item_text(item):
            return " ".join(b.get("text", "") for b in (item.get("textBlocks") or []) if b.get("text"))

        def _item_sources_html(item):
            srcs = item.get("sourceIds") or []
            if srcs:
                return "".join(f'<span class="source-chip small">{html.escape(s)}</span>' for s in srcs)
            return '<span class="no-sources">no sourceIds</span>'

        if comparison_items:
            cols = "".join(
                f'<div class="compare-col"><div class="compare-label">{html.escape(item.get("label") or "?")}</div>'
                f'<p class="compare-text">{html.escape(_item_text(item))}</p>{_item_sources_html(item)}</div>'
                for item in comparison_items
            )
            items_html = f'<div class="compare-row">{cols}</div>'
        elif enumeration_items:
            rows_ = "".join(
                f'<div class="enum-row"><span class="enum-index mono">{html.escape(str(item.get("index", "?")))}</span>'
                f'<div><p class="compare-text">{html.escape(_item_text(item))}</p>{_item_sources_html(item)}</div></div>'
                for item in enumeration_items
            )
            items_html = f'<div class="enum-list">{rows_}</div>'

        if items_html:
            # Per-item source chips above already cover sourcing precisely;
            # the generic scene-level chip row would just repeat the same
            # ids redundantly (this schema duplicates them at both levels).
            sources_html = ""
        elif sc["sources"]:
            sources_html = '<div class="sources">' + "".join(
                f'<span class="source-chip">{html.escape(s)}</span>' for s in sc["sources"]
            ) + "</div>"
        else:
            sources_html = '<span class="no-sources">no sourceIds</span>'

        # The actual answer to "what generated this image": the schema's own
        # derivedFrom description, plus the raw sub-object (depthOfAction,
        # clinicalCalendar, etc.) driving that visual.type — not just which
        # source ids it cites, but the structured fields those ids attach to.
        visual_raw = raw_scene.get("visual") or {}
        derived_from = visual_raw.get("derivedFrom")
        sub_key = REQUIRED_SUBOBJECT_BY_TYPE.get(visual_raw.get("type"))
        sub_data = visual_raw.get(sub_key) if sub_key else None
        source_data_html = ""
        if derived_from or sub_data:
            inner = []
            if derived_from:
                inner.append(f'<p class="derived-from">{html.escape(derived_from)}</p>')
            if sub_data:
                # Collapsed by default: an unbounded array (e.g. a 4-row
                # ClinicalCalendar timeline) was outweighing the thumbnail
                # and headline next to it — the image is the primary read,
                # this is reference detail one click away, not the headline.
                inner.append(
                    '<details class="raw-data-toggle"><summary>Raw data</summary>'
                    f'<pre class="raw-data mono">{html.escape(json.dumps(sub_data, indent=2, ensure_ascii=False))}</pre>'
                    '</details>'
                )
            source_data_html = f'<div class="source-data"><div class="source-data-label">Source data for this image</div>{"".join(inner)}</div>'

        thumb_html = None
        if output_video:
            at = min(sc["start"] + (sc["end"] - sc["start"]) * 0.78, max(sc["end"] - 0.05, sc["start"]))
            data_uri = extract_thumb(output_video, at, width=680)
            if data_uri:
                thumb_html = f'<img class="scene-thumb" src="{data_uri}" alt="scene {fmt_time(sc["start"])}">'
        if not thumb_html:
            ref_frame = find_component_reference_frame(visual_raw, repo_root)
            if ref_frame:
                ref_uri = embed_scaled_image(ref_frame, width=680)
                if ref_uri:
                    thumb_html = (
                        f'<div class="scene-thumb-wrap"><img class="scene-thumb" src="{ref_uri}" alt="component reference">'
                        '<div class="thumb-caption">component reference, not this exact scene</div></div>'
                    )
        if not thumb_html:
            thumb_html = '<div class="scene-thumb placeholder">no render to grab a frame from</div>'

        # --- pixel-level render checks for this scene (only when a render
        # exists) — reuses the exact same sampled instant as the thumbnail
        # above so "what you see" and "what got checked" are the same frame.
        if output_video and _HAS_IMAGING:
            render_check_counts["scenes_checked"] += 1
            full_frame = extract_full_frame(output_video, at)
            scene_findings = []
            if full_frame is not None:
                korean_block = next((b for b in (raw_scene.get("textBlocks") or []) if b.get("role") == "korean"), None)
                if korean_block:
                    render_check_counts["korean_run"] += 1
                    # Native resolution, not the shared 900px-wide full_frame —
                    # confirmed scale-sensitive for real: the same real syllable
                    # count (3/3, correct) misdetected as short/extra at 900,
                    # 1100, even 1300px width on a 1920-wide landscape source,
                    # only stabilizing correctly at 1500px+. A fixed extraction
                    # width loses proportionally more resolution on a wider
                    # source frame, and this check specifically needs enough
                    # pixels to resolve individual glyph blobs — native
                    # resolution sidesteps the whole scale-dependence rather
                    # than chasing a "safe" fixed width per aspect ratio.
                    native_width = None
                    try:
                        native_width = int(str(script.get("aspect", "")).lower().split("x")[0])
                    except (ValueError, IndexError):
                        pass
                    korean_frame = extract_full_frame(output_video, at, width=native_width) if native_width else full_frame
                    kc = check_korean_glyphs(korean_frame or full_frame, korean_block["text"])
                    if kc.get("available") and kc["status"] != "match":
                        render_check_counts["korean_bad"] += 1
                        scene_findings.append(
                            f'<div class="check-row bad">✗ Korean glyph check: found {kc["found"]} of {kc["expected"]} expected syllables in "{html.escape(korean_block["text"])}"'
                            + (f'<br><img class="evidence-img" src="{kc["band_uri"]}" alt="detected line, 2x scale"><div class="thumb-caption">detected line, 2x scale — the actual pixels checked</div>' if kc.get("band_uri") else "")
                            + '</div>'
                        )
                ocr_raw = ocr_text(full_frame, lang="eng")
                leaks = check_internal_strings(ocr_raw or "")
                if leaks:
                    render_check_counts["leak_hits"] += len(leaks)
                    scene_findings.append(f'<div class="check-row bad">✗ Internal string leak on screen: {", ".join(html.escape(m) for m in leaks)}</div>')
                if sc["type"] in ("comparison", "enumeration"):
                    # Confirmed directly in build.mjs: renderComparison() and
                    # renderEnumeration() never reference scene.textBlocks at
                    # all — only comparisonItems/enumerationItems render. The
                    # scene-level "headline" this check would otherwise test
                    # is never actually drawn on screen for these two types,
                    # so checking it produced a real false "mismatch" here
                    # (caught on retinal-vs-retinol.json: the OCR'd frame had
                    # the real on-screen text, correctly, just never the
                    # headline this check was comparing against).
                    claim_check = {"skipped": True, "reason": "comparison/enumeration scenes render their items' own text, not the scene-level headline"}
                else:
                    claim_check = check_claim_on_screen(sc["headline"], ocr_raw)
                if not claim_check.get("skipped"):
                    render_check_counts["claim_checked"] += 1
                    if not claim_check["match"]:
                        render_check_counts["claim_bad"] += 1
                        scene_findings.append(
                            f'<div class="check-row bad">✗ On-screen text doesn\'t match the compiled claim (word overlap {claim_check["ratio"]:.0%})'
                            f'<br><span class="mono" style="font-size:11px">OCR read: "{html.escape(claim_check["ocr_text"][:200])}"</span></div>'
                        )
            if scene_findings:
                render_check_cards.append(
                    f'<div class="card" style="border-color:var(--danger)"><b>Scene {fmt_time(sc["start"])}–{fmt_time(sc["end"])}</b> — "{html.escape(sc["headline"] or "")}"'
                    + "".join(scene_findings) + '</div>'
                )

        saved_note = html.escape(feedback.get(str(i), ""))
        image_name = f"{handle}_scene{i}"
        rows.append(f"""
  <div class="scene">
    {thumb_html}
    <div class="scene-body">
      <div class="scene-time mono">{time_range}</div>
      <div class="scene-tags">{tags}</div>
      {headline_html}
      {items_html}
      {sources_html}
      {source_data_html}
      <p class="feedback-label">Feedback on this scene</p>
      <div class="feedback-row">
        <div class="feedback-imgname mono">{html.escape(image_name)}</div>
        <textarea class="feedback-note" data-scene-index="{i}" placeholder="what's wrong, what to check, anything for the next pass…">{saved_note}</textarea>
      </div>
    </div>
  </div>""")
    scenes_html = "\n".join(rows)

    # --- render checks (pixel-level: frame zero, identity-scene language,
    # then whatever per-scene findings the main loop above collected) ---
    render_parts = []
    id_lang = audit["identity_language"]
    if id_lang:
        rows_ = "".join(
            f'<li>scene {f["scene_index"]} (identity) — "{html.escape(f["marker"])}" in: {html.escape(f["text"])}</li>'
            for f in id_lang
        )
        render_parts.append(f'<div class="status bad">✗ {len(id_lang)} identity-scene line(s) use efficacy/evidence language — identity scenes are nominal-only by design, regardless of sourcing</div><ul class="issues">{rows_}</ul>')
    else:
        render_parts.append('<p class="caveat">✓ No identity scene uses efficacy/evidence/gentleness language (identity scenes are checked as nominal-only — name, INCI, category — never a claim).</p>')

    if not output_video:
        render_parts.append('<div class="card">No render to check pixel-level — see Output above.</div>')
    elif not _HAS_IMAGING:
        render_parts.append('<div class="card" style="border-color:var(--danger)">Pixel-level checks unavailable: Pillow/numpy not installed.</div>')
    else:
        fz = check_frame_zero(output_video)
        if fz.get("available"):
            if fz["status"] == "sparse":
                render_parts.append(
                    f'<div class="status bad">✗ Frame zero (the scroll-stop frame) looks blank or mid-fade — density {fz["frame0_density"]:.1f} vs {fz["settled_density"]:.1f} settled</div>'
                    f'<div class="evidence-row"><div><img class="evidence-img" src="{fz["frame0_uri"]}"><div class="thumb-caption">t=0.0s — scroll-stop frame</div></div>'
                    f'<div><img class="evidence-img" src="{fz["settled_uri"]}"><div class="thumb-caption">t=0.6s — settled, for comparison</div></div></div>'
                )
            else:
                render_parts.append(f'<p class="caveat">✓ Frame zero is the dense, settled state (density {fz["frame0_density"]:.1f} vs {fz["settled_density"]:.1f} at t=0.6s) — not blank or mid-fade.</p>')
        else:
            render_parts.append('<p class="caveat">Frame-zero check unavailable (frame extraction failed).</p>')

        if not _HAS_OCR:
            render_parts.append('<p class="caveat">Internal-string and on-screen-claim checks unavailable: pytesseract/tesseract not installed — Korean glyph check above still ran (it doesn\'t use OCR).</p>')

        c = render_check_counts
        summary_bits = [f'{c["scenes_checked"]} scene(s) checked against the actual rendered frame']
        if c["korean_run"]:
            summary_bits.append(f'{c["korean_run"]} Korean-text scene(s) glyph-checked, {c["korean_bad"]} short/extra')
        if c["claim_checked"]:
            summary_bits.append(f'{c["claim_checked"]} claim(s) verified on-screen, {c["claim_bad"]} mismatched')
        if c["leak_hits"]:
            summary_bits.append(f'{c["leak_hits"]} internal-string leak hit(s)')
        status_class = "bad" if (render_check_cards) else "ok"
        status_glyph = "✗" if render_check_cards else "✓"
        render_parts.append(f'<div class="status {status_class}" style="margin-top:14px">{status_glyph} {"; ".join(summary_bits)}</div>')
        if render_check_cards:
            render_parts.extend(render_check_cards)

    render_parts.append(
        '<p class="caveat">Claim-on-screen and internal-string checks are OCR-based (tesseract) and skip any line containing '
        'Korean text — tested directly against this pipeline\'s own renders and found unreliable on short mixed Korean/Latin '
        'headings. The Korean glyph check above is pixel-only for exactly that reason (see check_korean_glyphs in this tool\'s '
        'own source for how). All of these are heuristic signals meant to catch what a founder would otherwise have to find '
        'by eye, frame by frame — not a guarantee nothing is wrong.</p>'
    )

    # --- pipeline acceptance harness (rules A-I) — the real render gate,
    # run for real against the built composition rather than reimplemented.
    # This is what catches things like "the font is too small" (rule I)
    # that none of the checks above ever asked about.
    harness = run_acceptance_harness(repo_root, handle)
    if not harness["available"]:
        render_parts.append(
            f'<p class="caveat">Pipeline acceptance checks (rules A–I — legibility floor, badge alpha, '
            f'caption collision, safe-area, start-of-scene flash, frame zero, Korean glyphs, internal strings) '
            f'unavailable: {html.escape(harness["reason"])}.</p>'
        )
    elif harness["passed"]:
        render_parts.append(f'<div class="status ok" style="margin-top:14px">✓ Pipeline acceptance checks (rules A–I) — {html.escape(harness["summary"])}</div>')
    else:
        rows_h = "".join(
            f'<div class="check-row bad">✗ [{html.escape(f["rule"])}] {html.escape(f["where"])} — {html.escape(f["detail"])}</div>'
            for f in harness["findings"]
        )
        render_parts.append(
            f'<div class="status bad" style="margin-top:14px">✗ Pipeline acceptance checks (rules A–I) — {html.escape(harness["summary"])}</div>{rows_h}'
        )
    if harness.get("raw"):
        render_parts.append(
            '<details class="raw-data-toggle"><summary>Raw acceptance-harness.mjs output</summary>'
            f'<pre class="raw-data mono">{html.escape(harness["raw"])}</pre></details>'
        )

    render_checks_html = "\n".join(render_parts)

    # --- output ---
    outs = audit["output"]
    if not outs:
        output_html = '<div class="card" style="border-color:var(--danger)">No rendered file found under video/out/ matching this handle. Nothing has been rendered yet, or it was rendered under a different name.</div>'
    else:
        parts = []
        for o in outs:
            size_mb = o["size_bytes"] / (1024 * 1024)
            if o["duration"] is None:
                dur_html = "duration unknown (ffprobe unavailable or failed)"
                match_html = ""
            else:
                matches = abs(o["duration"] - script.get("durationSeconds", -1)) < 0.6
                dur_html = f'{o["duration"]:.1f}s'
                match_html = (
                    ' <span style="color:var(--teal)">— matches script duration</span>' if matches
                    else f' <span style="color:var(--danger)">— does NOT match script duration ({script.get("durationSeconds")}s)</span>'
                )
            parts.append(
                f'<div class="card">{html.escape(o["path"].name)} — {size_mb:.1f} MB, {dur_html}{match_html}'
                f'<br><span class="path mono">{html.escape(str(o["path"]))}</span></div>'
            )
        output_html = "\n".join(parts)

    # --- review (the actual playable video) ---
    # Tried a plain file:// reference first (the video lives in a totally
    # different directory tree than this report) — confirmed it throws
    # "Not allowed to load local resource" rather than assuming that was
    # just a preview-tool quirk, since Chrome genuinely restricts file://
    # pages from loading resources outside their own directory. Embedding
    # as a data URI, same as every thumbnail elsewhere in this report,
    # works regardless of browser or where the two files sit relative to
    # each other.
    if output_video:
        mime = {".mp4": "video/mp4", ".mov": "video/quicktime", ".webm": "video/webm"}.get(output_video.suffix.lower(), "application/octet-stream")
        video_uri = f"data:{mime};base64," + base64.b64encode(output_video.read_bytes()).decode()
        video_player_html = (
            f'<video class="review-player" controls preload="metadata" src="{video_uri}"></video>'
            f'<p class="caveat">{html.escape(output_video.name)}</p>'
        )
    else:
        video_player_html = '<div class="card">No render to review yet — see Output above.</div>'

    # --- sourcing audit ---
    if inp["source_ids"] is None:
        sourcing_html = '<div class="card">No source-record ledger to check against (see Input above) — sourcing audit skipped.</div>'
    elif not audit["script_ids"]:
        sourcing_html = '<div class="card">This script cites no source ids anywhere.</div>'
    elif not audit["unresolved_ids"]:
        chips = "".join(f'<span class="source-chip">{html.escape(s)}</span>' for s in audit["script_ids"])
        sourcing_html = f'<div class="status ok">✓ All {len(audit["script_ids"])} cited source id(s) resolve in the record\'s own Section 13</div><div class="sources">{chips}</div>'
    else:
        chips = "".join(
            f'<span class="source-chip{" bad" if s in audit["unresolved_ids"] else ""}">{html.escape(s)}</span>'
            for s in audit["script_ids"]
        )
        sourcing_html = (
            f'<div class="status bad">✗ {len(audit["unresolved_ids"])} of {len(audit["script_ids"])} cited source id(s) do NOT resolve in the record\'s own Section 13</div>'
            f'<div class="sources">{chips}</div>'
        )

    # Confirmed directly against compositions/lib/artifacts.mjs (with the
    # other Claude session working this same repo): its own transcript
    # generator only emits a visible citation for scene.type === "claim".
    # A hook/identity/end_card/sources scene carrying sourceIds would be
    # sourced in the data but invisible in the actual output — not a
    # sourcing failure exactly, but worth surfacing since nothing else
    # catches it (comparison/enumeration excluded: they cite through their
    # own per-item sourceIds, a separate, still-real path).
    invis = audit["invisible_sourcing"]
    if invis:
        rows = "".join(
            f'<li>scene {f["scene_index"]} (type "{html.escape(f["type"])}") carries {", ".join(html.escape(s) for s in f["source_ids"])} — '
            'won\'t render as a visible citation (artifacts.mjs only emits one for type "claim")</li>'
            for f in invis
        )
        sourcing_html += f'<div class="status warn" style="margin-top:10px">⚠ {len(invis)} scene(s) with sourceIds that will never render</div><ul class="issues">{rows}</ul>'
    else:
        sourcing_html += '<p class="caveat" style="margin-top:10px">✓ No non-claim scene silently carries an invisible source id (checked against compositions/lib/artifacts.mjs\'s own claim-only citation gate).</p>'

    # --- content-safety signals ---
    abs_hits, qual_hits = audit["absolute_hits"], audit["qualified_hits"]
    safety_parts = []
    if abs_hits:
        safety_parts.append(f'<div class="status bad">✗ {len(abs_hits)} absolute-claim phrase(s) found — these refuse regardless of sourcing in the real pipeline</div>')
        for marker, text in abs_hits:
            safety_parts.append(f'<div class="marker-hit"><b>"{html.escape(marker)}"</b> in: {html.escape(text)}</div>')
    else:
        safety_parts.append('<div class="status ok">✓ No absolute-claim language found</div>')
    if qual_hits:
        safety_parts.append(f'<p style="font-size:12.5px;color:var(--text-muted);margin:14px 0 6px">{len(qual_hits)} assertive phrase(s) found — fine when a source id resolves nearby, flagged here for a quick look:</p>')
        for marker, text in qual_hits:
            safety_parts.append(f'<div class="marker-hit qualified"><b>"{html.escape(marker)}"</b> in: {html.escape(text)}</div>')
    safety_parts.append(
        '<p class="caveat">Heuristic signal only, ported from this project\'s own assertion-gate marker lists — '
        'relevant to platform health-content policy (e.g. YouTube\'s medical-misinformation policy) but not a '
        'compliance determination. Only the platform itself can determine actual policy compliance.</p>'
    )
    safety_html = "\n".join(safety_parts)

    page = PAGE_TEMPLATE
    page = page.replace("__TITLE__", html.escape(script.get("title") or script_path.stem))
    page = page.replace("__SOURCE_PATH__", html.escape(str(script_path)))
    page = page.replace("__HANDLE__", html.escape(script.get("handle") or "?"))
    page = page.replace("__ASPECT__", html.escape(script.get("aspect") or "?"))
    page = page.replace("__DURATION__", html.escape(str(script.get("durationSeconds", "?"))))
    page = page.replace("__SCENE_COUNT__", str(len(scenes)))
    page = page.replace("__STORE_KEY__", json.dumps(handle))
    page = page.replace("__STORYLINE_TITLE__", json.dumps(script.get("title") or handle))
    page = page.replace("__BAKED_FEEDBACK__", json.dumps(feedback))
    page = page.replace("__STATUS_HTML__", status_html)
    page = page.replace("__INPUT_HTML__", input_html)
    page = page.replace("__SCENES_HTML__", scenes_html)
    page = page.replace("__OUTPUT_HTML__", output_html)
    page = page.replace("__RENDER_CHECKS_HTML__", render_checks_html)
    page = page.replace("__SOURCING_HTML__", sourcing_html)
    page = page.replace("__SAFETY_HTML__", safety_html)
    page = page.replace("__VIDEO_PLAYER_HTML__", video_player_html)
    return page


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: python3 storyline.py /path/to/scripts/<handle>.json [more scripts ...]")

    out_dir = Path(__file__).resolve().parent
    for raw in sys.argv[1:]:
        script_path = Path(raw).expanduser().resolve()
        try:
            script = json.loads(script_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            print(f"error: could not read/parse {script_path}: {e}")
            continue

        issues = validate(script)
        handle = script.get("handle") or script_path.stem
        print(f"\n{script_path.name} — {'VALID' if not issues else f'{len(issues)} issue(s)'}")
        for i in issues:
            print(f"  ✗ {i}")
        for i, sc in enumerate(scene_summary(s) for s in script.get("scenes", [])):
            marker = " [EMPTY]" if sc["empty"] else ""
            print(f'  {i}. {fmt_time(sc["start"])}-{fmt_time(sc["end"])}  {sc["type"]:<11} visual={sc["visual"]:<16} "{sc["headline"] or ""}"{marker}')

        repo_root = find_repo_root(script_path)
        audit = build_audit(script, repo_root)
        if audit["unresolved_ids"]:
            print(f'  ✗ sourcing: {len(audit["unresolved_ids"])} unresolved id(s): {", ".join(audit["unresolved_ids"])}')
        elif audit["input"]["source_ids"] is not None:
            print(f'  ✓ sourcing: all {len(audit["script_ids"])} cited id(s) resolve')
        if audit["invisible_sourcing"]:
            for f in audit["invisible_sourcing"]:
                print(f'  ⚠ scene {f["scene_index"]} (type "{f["type"]}") has sourceIds that will never render: {", ".join(f["source_ids"])}')
        if audit["absolute_hits"]:
            print(f'  ✗ content-safety: {len(audit["absolute_hits"])} absolute-claim phrase(s) found')
        if audit["identity_language"]:
            for f in audit["identity_language"]:
                print(f'  ✗ scene {f["scene_index"]} (identity): "{f["marker"]}" language — identity scenes are nominal-only')
        if not audit["output"]:
            print("  ✗ output: no rendered file found under video/out/")
        else:
            for o in audit["output"]:
                print(f'  output: {o["path"].name} — {o["duration"]}s' if o["duration"] else f'  output: {o["path"].name}')
            if not (_HAS_IMAGING and _HAS_OCR):
                missing = ", ".join(n for n, ok in (("Pillow/numpy", _HAS_IMAGING), ("pytesseract", _HAS_OCR)) if not ok)
                print(f"  (pixel-level render checks partially unavailable: {missing} not installed — see the HTML report for what did run)")

        out_path = out_dir / f"storyline_{handle}.html"
        feedback_path = out_dir / f"storyline_{handle}.feedback.json"
        feedback = {}
        if feedback_path.is_file():
            feedback = load_feedback_sidecar(feedback_path)
            if feedback:
                print(f"  Applied saved feedback from {feedback_path.name}")

        out_path.write_text(build_report(script_path, script, feedback), encoding="utf-8")
        print(f"  Wrote {out_path} — see its Render checks section for frame-zero, glyph, and on-screen claim verification")
        subprocess.run(["open", str(out_path)])


if __name__ == "__main__":
    main()
