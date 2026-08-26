#!/usr/bin/env python3
"""
storyboard.py — generate a drag-and-drop storyboard HTML page for video clips
and still images.

Usage:
    python3 storyboard.py PATH [PATH ...] [-o output.html]

Each PATH can be a folder (scanned recursively, so items can live in per-item
subfolders) OR an individual video/image file — mix them freely, from anywhere
on disk:

    python3 storyboard.py ~/shoot1 ~/shoot2/clip7.mov "/Volumes/SSD/proof_frames"

For every video it extracts duration (ffprobe) and a thumbnail (ffmpeg, frame
at ~1s). For every image it makes a scaled-down thumbnail from the image
itself and tags it "IMG" (stills have no inherent duration). Writes ONE
self-contained HTML file:

  - each item is a film-strip row: thumbnail, sequence number, filename,
    duration/IMG tag, and an editable note ("what's wrong with this shot")
  - rows are drag-and-drop reorderable
  - order + notes persist in localStorage (keyed by the output file's path),
    so re-running the script keeps your ordering and comments for items that
    still exist; newly found items are appended at the end
  - "Save notes (.json)" downloads a small <board>.notes.json sidecar (order +
    notes + descriptions + prompts + story text + preflight state). Put it
    next to the board's HTML (or pass --notes FILE) and the next run bakes it
    straight into the page instead of relying on that one browser's
    localStorage — the notes survive --combine/--index, a cleared browser
    profile, or opening the board somewhere else. Without a sidecar, nothing
    changes from the localStorage-only behavior above.
  - "Download ffmpeg concat file" exports the current order in concat-demuxer
    format, ready for:
        ffmpeg -f concat -safe 0 -i concat_list.txt -c copy stitched.mp4
    (re-encode instead of -c copy if items differ in codec/resolution, or if
    the sequence mixes images and videos — images get a fixed 3s "duration"
    directive per the concat demuxer's still-image convention)

Requires only ffmpeg/ffprobe on PATH. No server, no database, no dependencies.

Run `python3 storyboard.py --index [DIR]` (default DIR: current folder) to build
an index.html linking every storyboard.py board found there, with title + clip
count — handy once you've generated several boards in the same folder.

Run `python3 storyboard.py --combine [DIR]` to merge every board found in DIR
into ONE page with a tab bar — multiple "stories" (e.g. different component
proof sets), each keeping its own independent drag order, notes, and export,
switchable without leaving the page.
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

VIDEO_EXTS = {".mp4", ".mov", ".m4v", ".mkv", ".webm", ".avi", ".mpg", ".mpeg"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".gif"}
MEDIA_EXTS = VIDEO_EXTS | IMAGE_EXTS
THUMB_WIDTH = 720


def run(cmd, timeout=15):
    """Every ffmpeg/ffprobe call in this file goes through here. Without a
    timeout, one bad file (corrupt, oddly-shaped, or on slow/network
    storage) hangs the ENTIRE scan forever with zero feedback — confirmed
    for real: pointed at ~/Documents (33k files, most not media but some
    are) instead of an actual clips folder, this ran for 2h47m at ~0% CPU
    before being killed by hand. A timed-out call now fails like any other
    ffmpeg error (empty stdout, non-zero returncode) so every existing
    caller's own error handling already covers it — this file just skips
    that one clip instead of hanging on it."""
    try:
        return subprocess.run(cmd, capture_output=True, text=False, timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        print(f"  warning: timed out after {timeout}s running {cmd[0]} on {cmd[-1]} — skipping")
        return subprocess.CompletedProcess(cmd, returncode=-1, stdout=b"", stderr=b"timed out")


def probe_duration(path: Path):
    r = run([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(path),
    ])
    try:
        return float(r.stdout.decode().strip())
    except (ValueError, AttributeError):
        return None


def extract_video_thumb(path: Path, duration):
    # grab the frame at 1s, or the midpoint for clips shorter than ~1.2s
    seek = 1.0
    if duration is not None and duration < 1.2:
        seek = max(duration / 2.0, 0.0)
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tf:
        tmp = Path(tf.name)
    try:
        r = run([
            "ffmpeg", "-y", "-v", "error",
            "-ss", f"{seek:.3f}", "-i", str(path),
            "-frames:v", "1",
            "-vf", f"scale={THUMB_WIDTH}:-2",
            "-q:v", "4",
            str(tmp),
        ])
        if r.returncode != 0 or not tmp.exists() or tmp.stat().st_size == 0:
            # retry from the very first frame (some clips have no frame at 1s)
            r = run([
                "ffmpeg", "-y", "-v", "error",
                "-i", str(path),
                "-frames:v", "1",
                "-vf", f"scale={THUMB_WIDTH}:-2",
                "-q:v", "4",
                str(tmp),
            ])
        if r.returncode == 0 and tmp.exists() and tmp.stat().st_size > 0:
            return "data:image/jpeg;base64," + base64.b64encode(tmp.read_bytes()).decode()
        return None
    finally:
        try:
            tmp.unlink()
        except FileNotFoundError:
            pass


def extract_image_thumb(path: Path):
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tf:
        tmp = Path(tf.name)
    try:
        r = run([
            "ffmpeg", "-y", "-v", "error",
            "-i", str(path),
            "-frames:v", "1",
            "-vf", f"scale={THUMB_WIDTH}:-2:force_original_aspect_ratio=decrease",
            "-q:v", "4",
            str(tmp),
        ])
        if r.returncode == 0 and tmp.exists() and tmp.stat().st_size > 0:
            return "data:image/jpeg;base64," + base64.b64encode(tmp.read_bytes()).decode()
        return None
    finally:
        try:
            tmp.unlink()
        except FileNotFoundError:
            pass


def fmt_duration(seconds):
    if seconds is None:
        return "?"
    m, s = divmod(round(seconds), 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def is_video(p: Path):
    return p.is_file() and p.suffix.lower() in VIDEO_EXTS and not p.name.startswith(".")


def is_image(p: Path):
    return p.is_file() and p.suffix.lower() in IMAGE_EXTS and not p.name.startswith(".")


def is_media(p: Path):
    return p.is_file() and p.suffix.lower() in MEDIA_EXTS and not p.name.startswith(".")


def gather_files(paths):
    """Each path may be a folder (scanned recursively) or a single video/image file."""
    files = []
    for raw in paths:
        root = Path(raw).expanduser().resolve()
        if root.is_dir():
            found = sorted(
                (p for p in root.rglob("*") if is_media(p)),
                key=lambda p: str(p).lower(),
            )
            if not found:
                print(f"  warning: no video/image files in folder {root}")
            files.extend(found)
        elif root.is_file():
            if is_media(root):
                files.append(root)
            else:
                print(f"  warning: not a recognized video/image file, skipping: {root}")
        else:
            sys.exit(f"error: path does not exist: {root}")
    # de-dupe (same file reachable via two args), keep first occurrence
    seen, unique = set(), []
    for f in files:
        key = str(f.resolve())
        if key not in seen:
            seen.add(key)
            unique.append(f)
    return unique


def collect_clips(paths):
    files = gather_files(paths)
    clips = []
    for i, p in enumerate(files, 1):
        print(f"  [{i}/{len(files)}] {p}", flush=True)
        if is_image(p):
            clips.append({
                "id": str(p.resolve()),
                "title": p.name,
                "path": str(p.resolve()),
                "note": "",
                "description": "",
                "prompt": "",
                "dur": "IMG",
                "durSec": 0,
                "isImage": True,
                "thumb": extract_image_thumb(p),
            })
        else:
            dur = probe_duration(p)
            clips.append({
                "id": str(p.resolve()),      # stable key across re-runs: absolute path
                "title": p.name,
                "path": str(p.resolve()),
                "note": "",
                "description": "",
                "prompt": "",
                "dur": fmt_duration(dur),
                "durSec": dur or 0,
                "isImage": False,
                "thumb": extract_video_thumb(p, dur),
            })
    return clips


def load_notes_sidecar(path: Path):
    """Read a <board>.notes.json previously downloaded from a board's own
    "Save notes (.json)" button. Returns None (with a warning printed) if the
    file isn't valid JSON — never raises, since a bad sidecar shouldn't block
    a re-scan."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"  warning: could not read notes file {path}: {e}")
        return None
    if not isinstance(data, dict):
        print(f"  warning: {path} is not a notes-file object, ignoring")
        return None
    return data


def apply_notes_sidecar(clips, sidecar):
    """Merge a notes sidecar's order/notes/descriptions/prompts onto freshly
    scanned clips — same reconciliation the in-page JS does against
    localStorage: sidecar order/annotations win, scan wins for media, new
    items (not in the sidecar) are appended at the end."""
    notes = sidecar.get("notes") or {}
    descriptions = sidecar.get("descriptions") or {}
    prompts = sidecar.get("prompts") or {}
    order = sidecar.get("order") or []

    def annotate(c):
        return {**c, "note": notes.get(c["id"], ""),
                "description": descriptions.get(c["id"], ""),
                "prompt": prompts.get(c["id"], "")}

    by_id = {c["id"]: c for c in clips}
    merged = [annotate(by_id[cid]) for cid in order if cid in by_id]
    seen = set(order)
    merged.extend(annotate(c) for c in clips if c["id"] not in seen)
    return merged


PAGE_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Clip Storyboard — __TITLE__</title>
<style>
  :root{
    --bg:#1C1A17; --panel:#252119; --card:#2C2720; --card-edge:#3A342A;
    --amber:#E8A33D; --amber-dim:#8A6528; --teal:#4F9B8E;
    --text:#F0EBE3; --text-muted:#9C948A; --text-faint:#655D51; --danger:#C96A4F;
  }
  *{box-sizing:border-box;}
  body{margin:0;background:radial-gradient(ellipse at top left, rgba(232,163,61,0.05), transparent 55%), var(--bg);
    color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;min-height:100vh;}
  .mono{font-family:"SF Mono","JetBrains Mono",Consolas,"Courier New",monospace;}
  header{padding:28px 32px 20px;border-bottom:1px solid var(--card-edge);display:flex;align-items:flex-end;
    justify-content:space-between;flex-wrap:wrap;gap:16px;}
  .title-block h1{margin:0 0 4px;font-size:22px;font-weight:700;}
  .title-block p{margin:0;color:var(--text-muted);font-size:13px;}
  .tally{text-align:right;font-size:12px;color:var(--text-muted);}
  .tally .num{font-size:26px;color:var(--amber);font-weight:700;display:block;line-height:1.1;}
  .story-text{width:100%;margin:14px 32px 0;max-width:900px;background:transparent;
    border:1px dashed var(--card-edge);border-radius:8px;color:var(--text);
    font-size:14px;line-height:1.5;padding:11px 14px;resize:vertical;min-height:44px;
    font-family:inherit;}
  .story-text:focus{outline:none;border-style:solid;border-color:var(--amber-dim);}
  .story-text::placeholder{color:var(--text-faint);}
  main{padding:24px 32px 60px;margin:0 auto;}
  button{font-family:inherit;cursor:pointer;border:none;border-radius:5px;font-size:13px;padding:9px 16px;
    font-weight:600;transition:transform .08s ease, opacity .12s ease;}
  button:active{transform:scale(0.97);}
  .btn-primary{background:var(--amber);color:#1C1A17;}
  .btn-primary:hover{opacity:0.9;}
  .btn-ghost{background:transparent;color:var(--text-muted);border:1px solid var(--card-edge);}
  .btn-ghost:hover{color:var(--text);border-color:var(--text-faint);}
  .toolbar{display:flex;justify-content:flex-end;gap:8px;margin-bottom:16px;flex-wrap:wrap;}
  .board{display:flex;flex-direction:row;flex-wrap:wrap;align-items:flex-start;gap:16px;}
  .card{display:flex;flex-direction:column;width:260px;flex-shrink:0;background:var(--card);
    border:1px solid var(--card-edge);border-radius:8px;overflow:hidden;
    position:relative;cursor:grab;}
  .card.dragging{opacity:0.35;}
  .card.drag-over{border-color:var(--amber);}
  .sprockets{height:16px;flex-shrink:0;border-bottom:1px solid var(--card-edge);position:relative;}
  .sprockets::before{content:"";position:absolute;inset:0;
    background-image:radial-gradient(circle, var(--bg) 3px, transparent 3.5px);
    background-size:20px 100%;background-position:8px center;}
  .thumb{position:relative;width:100%;aspect-ratio:16/9;flex-shrink:0;background:#000;
    display:flex;align-items:center;justify-content:center;overflow:hidden;
    border-bottom:1px solid var(--card-edge);cursor:zoom-in;}
  .thumb img{width:100%;height:100%;object-fit:cover;display:block;}
  .thumb .noimg{color:var(--text-faint);font-size:10px;text-align:center;padding:4px;}
  .seq{position:absolute;top:6px;left:6px;min-width:20px;height:20px;padding:0 5px;border-radius:10px;
    background:var(--amber);color:#1C1A17;font-size:11px;font-weight:700;
    display:flex;align-items:center;justify-content:center;}
  .dur{position:absolute;bottom:6px;right:6px;background:rgba(0,0,0,.75);color:#fff;
    font-size:10px;padding:2px 6px;border-radius:4px;}
  .card-body{display:flex;flex-direction:column;gap:6px;padding:10px 12px 12px;min-width:0;}
  .card input[type="text"]{background:transparent;border:none;border-bottom:1px solid transparent;
    color:var(--text);font-size:13px;font-weight:600;padding:2px 0;width:100%;}
  .card input[type="text"]:focus{outline:none;border-bottom:1px solid var(--amber-dim);}
  .card .desc, .card .note{background:transparent;border:none;color:var(--text-muted);font-size:12px;
    padding:0;width:100%;font-weight:400;resize:none;font-family:inherit;min-height:32px;line-height:1.35;}
  .card .note{color:var(--amber-dim);border-top:1px dashed var(--card-edge);padding-top:6px;margin-top:2px;}
  .card .desc:focus, .card .note:focus{outline:none;color:var(--text);}
  .card .desc::placeholder, .card .note::placeholder, .card input::placeholder{color:var(--text-faint);}
  .field-label{font-size:9px;text-transform:uppercase;letter-spacing:.04em;color:var(--text-faint);margin:2px 0 -3px;}
  .path{font-size:9px;color:var(--text-faint);word-break:break-all;}
  .toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%) translateY(8px);background:var(--amber);
    color:#1C1A17;padding:10px 18px;border-radius:6px;font-size:13px;font-weight:600;opacity:0;
    pointer-events:none;transition:opacity .2s ease, transform .2s ease;white-space:pre;}
  .toast.show{opacity:1;transform:translateX(-50%) translateY(0);}
  .lightbox{position:fixed;inset:0;background:rgba(10,9,7,.92);z-index:50;
    display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;
    padding:40px;cursor:zoom-out;opacity:0;pointer-events:none;transition:opacity .15s ease;}
  .lightbox.show{opacity:1;pointer-events:auto;}
  .lightbox img{max-width:90vw;max-height:78vh;object-fit:contain;border-radius:6px;
    box-shadow:0 20px 60px rgba(0,0,0,.6);cursor:default;}
  .lightbox .lb-caption{color:var(--text-muted);font-size:13px;text-align:center;max-width:80vw;}
  .lightbox .lb-caption .lb-title{color:var(--text);font-weight:600;margin-right:8px;}
  .lightbox .lb-nav{position:absolute;top:50%;transform:translateY(-50%);background:rgba(44,39,32,.8);
    border:1px solid var(--card-edge);color:var(--text);width:44px;height:44px;border-radius:50%;
    font-size:20px;display:flex;align-items:center;justify-content:center;cursor:pointer;}
  .lightbox .lb-nav:hover{border-color:var(--amber);color:var(--amber);}
  .lightbox .lb-prev{left:24px;}
  .lightbox .lb-next{right:24px;}
  .lightbox .lb-close{position:absolute;top:20px;right:24px;background:transparent;border:none;
    color:var(--text-muted);font-size:26px;cursor:pointer;line-height:1;}
  .lightbox .lb-close:hover{color:var(--text);}
  .preflight{margin-bottom:16px;background:var(--card);border:1px solid var(--card-edge);
    border-radius:10px;overflow:hidden;}
  .pf-header{display:flex;align-items:center;justify-content:space-between;gap:14px;
    padding:13px 18px;cursor:pointer;}
  .pf-header:hover{background:rgba(255,255,255,.02);}
  .pf-header-left{display:flex;align-items:center;gap:10px;}
  .pf-header h3{margin:0;font-size:13.5px;font-weight:700;}
  .pf-caret{color:var(--text-faint);font-size:11px;transition:transform .15s ease;}
  .preflight.open .pf-caret{transform:rotate(90deg);}
  .pf-progress{display:flex;align-items:center;gap:10px;}
  .pf-count{font-size:12px;color:var(--text-muted);font-variant-numeric:tabular-nums;white-space:nowrap;}
  .pf-count b{color:var(--amber);}
  .pf-track{width:70px;height:5px;border-radius:3px;background:var(--bg);overflow:hidden;}
  .pf-fill{height:100%;background:var(--amber);border-radius:3px;width:0%;transition:width .2s ease;}
  .pf-body{display:none;padding:2px 18px 16px;border-top:1px solid var(--card-edge);}
  .preflight.open .pf-body{display:block;}
  .pf-section{padding-top:14px;}
  .pf-section h4{margin:0 0 2px;font-size:12px;font-weight:700;color:var(--amber-dim);
    text-transform:uppercase;letter-spacing:.04em;}
  .pf-section p{margin:0 0 6px;font-size:11.5px;color:var(--text-faint);}
  .pf-item{display:flex;align-items:flex-start;gap:10px;padding:7px 0;border-top:1px solid var(--card-edge);}
  .pf-item:first-of-type{border-top:none;}
  .pf-item input[type="checkbox"]{appearance:none;-webkit-appearance:none;flex-shrink:0;
    margin-top:2px;width:17px;height:17px;border-radius:5px;border:1.5px solid var(--card-edge);
    background:var(--bg);position:relative;cursor:pointer;}
  .pf-item input[type="checkbox"]:checked{background:var(--amber);border-color:var(--amber);}
  .pf-item input[type="checkbox"]:checked::after{content:"";position:absolute;left:4.5px;top:1px;
    width:4.5px;height:8px;border:solid #1C1A17;border-width:0 2px 2px 0;transform:rotate(40deg);}
  .pf-item span{font-size:13px;color:var(--text-muted);line-height:1.4;}
  .pf-item.checked span{color:var(--text-faint);text-decoration:line-through;text-decoration-color:var(--card-edge);}
  @media (prefers-reduced-motion: reduce){*{transition:none !important;}}
</style>
</head>
<body>

<header>
  <div class="title-block">
    <h1>Clip Storyboard</h1>
    <p><span class="mono">__SOURCES__</span> &middot; re-run storyboard.py any time the clips change — order &amp; notes are kept</p>
  </div>
  <div class="tally">
    <span class="num mono" id="clipCount">0</span>
    <span>clips &middot; <span id="totalDur" class="mono">0:00</span> total</span>
  </div>
</header>

<textarea class="story-text" id="storyText" placeholder="Story text — describe what this whole storyboard is about, for context when sharing it for feedback…"></textarea>

<main>
  <div class="preflight" id="preflight">
    <div class="pf-header" onclick="togglePreflight()">
      <div class="pf-header-left">
        <span class="pf-caret">&#9656;</span>
        <h3>Preflight — pre-publish checklist</h3>
      </div>
      <div class="pf-progress">
        <div class="pf-count"><b id="pfDone">0</b>/<span id="pfTotal">0</span></div>
        <div class="pf-track"><div class="pf-fill" id="pfFill"></div></div>
      </div>
    </div>
    <div class="pf-body" id="pfBody"></div>
  </div>

  <div class="toolbar">
    <button class="btn-ghost" onclick="resetBoard()">Reset order, text &amp; notes</button>
    <button class="btn-ghost" onclick="exportText()">Copy sequence as text</button>
    <button class="btn-ghost" onclick="exportNotes()">Save notes (.json)</button>
    <button class="btn-ghost" onclick="exportPacket()">Download review packet (.zip)</button>
    <button class="btn-primary" onclick="exportConcat()">Download ffmpeg concat file</button>
  </div>
  <div class="board" id="board"></div>
</main>

<div class="toast" id="toast"></div>

<div class="lightbox" id="lightbox">
  <button class="lb-close" onclick="closeLightbox()">&times;</button>
  <button class="lb-nav lb-prev" onclick="event.stopPropagation(); navLightbox(-1)">&#8249;</button>
  <img id="lbImg">
  <button class="lb-nav lb-next" onclick="event.stopPropagation(); navLightbox(1)">&#8250;</button>
  <div class="lb-caption"><span class="lb-title" id="lbTitle"></span><span id="lbMeta"></span></div>
</div>

<script>
const SCANNED = __CLIPS_JSON__;
const STORAGE_KEY = "storyboard_order_" + __STORE_KEY__;

let clips = loadOrder();
let dragId = null;

function loadOrder(){
  try{
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "null");
    if(saved && Array.isArray(saved)){
      // Reconcile saved order/notes with freshly scanned data (scan wins for media).
      const byId = Object.fromEntries(SCANNED.map(c => [c.id, c]));
      const merged = saved.filter(s => byId[s.id]).map(s => ({...byId[s.id],
        note: s.note || "", description: s.description || "", prompt: s.prompt || ""}));
      const savedIds = new Set(saved.map(s => s.id));
      SCANNED.forEach(c => { if(!savedIds.has(c.id)) merged.push({...c}); });
      if(merged.length) return merged;
    }
  } catch(e){}
  return SCANNED.map(c => ({...c}));
}

function saveOrder(){
  const toSave = clips.map(c => ({id: c.id, note: c.note, description: c.description, prompt: c.prompt}));
  localStorage.setItem(STORAGE_KEY, JSON.stringify(toSave));
}

const DEFAULT_STORY_TEXT = __DEFAULT_STORY_TEXT__;
const STORY_TEXT_KEY = STORAGE_KEY + "::storytext";
document.getElementById('storyText').value = localStorage.getItem(STORY_TEXT_KEY) || DEFAULT_STORY_TEXT;
document.getElementById('storyText').addEventListener('input', e => {
  localStorage.setItem(STORY_TEXT_KEY, e.target.value);
});

const PREFLIGHT_DATA = [
  { key: "hook", title: "Hook", desc: "The first three seconds decide whether anyone stays.", items: [
    "States the single claim or question in the first 3 seconds, before any logo or intro",
    "First frame is fully composed the instant it loads — no fade-up from blank",
    "Cut the weakest 5 seconds; every second left in earns its place",
  ]},
  { key: "format", title: "Format & safe zones", desc: "Vertical, and clear of the platform's own UI.", items: [
    "Exported at 1080×1920 (9:16) — not cropped or letterboxed from a wider master",
    "Burned-in text sits clear of the bottom-left caption/sound UI and the right-edge button rail",
    "Checked real device crop risk at the very top and bottom of frame, not just the raw canvas",
  ]},
  { key: "claims", title: "Claims & sourcing", desc: "Nothing on screen that can't be backed up.", items: [
    "Every on-screen claim carries a source chip or citation a viewer could actually verify",
    "No claim states a result beyond what the cited study's own duration supports",
    "Unsourced or refused claims render nothing — no placeholder text, no “coming soon”",
  ]},
  { key: "captions", title: "Captions & legibility", desc: "Most of this gets watched on mute.", items: [
    "Captions are burned in — sound is a bonus, not a requirement",
    "Watched the export at actual phone width, not just the desktop preview size",
    "Korean/English text renders with no missing glyphs or fallback-font boxes",
  ]},
  { key: "loop", title: "Loop & pacing", desc: "How it ends is part of how it starts.", items: [
    "If it's meant to loop, the last frame rhymes with the first — no jump-cut at the seam",
    "Runtime matches the idea; nothing padded just to hit a round number",
  ]},
  { key: "metadata", title: "Title, description & cover", desc: "What gets someone to click before they've seen a frame.", items: [
    "Title states the specific claim or question, not a vague category label",
    "Description includes real sources or links, not only hashtags",
    "Cover frame (if used) is legible at true small size, not just full-screen preview",
  ]},
  { key: "final", title: "Final pass", desc: "One last look, the way a viewer will actually see it.", items: [
    "Watched the whole thing once with sound off",
    "Watched the whole thing once with sound on, on a phone",
    "Confirmed the file about to upload is the current export, not an old one",
  ]},
];

const DEFAULT_PREFLIGHT = __DEFAULT_PREFLIGHT__;
const PREFLIGHT_KEY = STORAGE_KEY + "::preflight";
const PREFLIGHT_OPEN_KEY = STORAGE_KEY + "::preflight_open";

function loadPreflight(){
  try {
    const saved = JSON.parse(localStorage.getItem(PREFLIGHT_KEY));
    if (saved) return saved;
  } catch(e){}
  return {...DEFAULT_PREFLIGHT};
}
let preflightChecked = loadPreflight();

function pfItemId(sectionKey, i){ return sectionKey + "-" + i; }

function renderPreflight(){
  const body = document.getElementById('pfBody');
  body.innerHTML = "";
  let total = 0;
  PREFLIGHT_DATA.forEach(section => {
    const sec = document.createElement('div');
    sec.className = 'pf-section';
    const h4 = document.createElement('h4'); h4.textContent = section.title;
    const p = document.createElement('p'); p.textContent = section.desc;
    sec.appendChild(h4); sec.appendChild(p);
    section.items.forEach((text, i) => {
      total++;
      const id = pfItemId(section.key, i);
      const item = document.createElement('div');
      item.className = 'pf-item' + (preflightChecked[id] ? ' checked' : '');
      const cb = document.createElement('input');
      cb.type = 'checkbox';
      cb.checked = !!preflightChecked[id];
      cb.addEventListener('change', () => {
        preflightChecked[id] = cb.checked;
        item.classList.toggle('checked', cb.checked);
        localStorage.setItem(PREFLIGHT_KEY, JSON.stringify(preflightChecked));
        updatePreflightProgress();
      });
      const span = document.createElement('span'); span.textContent = text;
      item.appendChild(cb); item.appendChild(span);
      sec.appendChild(item);
    });
    body.appendChild(sec);
  });
  document.getElementById('pfTotal').textContent = total;
  updatePreflightProgress();
}

function updatePreflightProgress(){
  const total = PREFLIGHT_DATA.reduce((n, s) => n + s.items.length, 0);
  const done = Object.values(preflightChecked).filter(Boolean).length;
  document.getElementById('pfDone').textContent = done;
  document.getElementById('pfFill').style.width = (total ? Math.round(done / total * 100) : 0) + '%';
}

function togglePreflight(){
  const el = document.getElementById('preflight');
  const open = el.classList.toggle('open');
  localStorage.setItem(PREFLIGHT_OPEN_KEY, open ? '1' : '0');
}

if (localStorage.getItem(PREFLIGHT_OPEN_KEY) === '1') {
  document.getElementById('preflight').classList.add('open');
}
renderPreflight();

function updateField(id, field, value){
  const clip = clips.find(c => c.id === id);
  if(clip){ clip[field] = value; saveOrder(); }
}

function render(){
  const board = document.getElementById('board');
  board.innerHTML = "";
  document.getElementById('clipCount').textContent = clips.length;
  const totalSec = clips.reduce((s,c) => s + (c.durSec || 0), 0);
  const m = Math.floor(totalSec/60), s = Math.round(totalSec%60).toString().padStart(2,'0');
  document.getElementById('totalDur').textContent = `${m}:${s}`;

  clips.forEach((clip, i) => {
    const card = document.createElement('div');
    card.className = 'card';
    card.draggable = true;
    card.dataset.id = clip.id;
    card.innerHTML = `
      <div class="sprockets"></div>
      <div class="thumb">
        ${clip.thumb ? `<img>` : `<span class="noimg">no thumb</span>`}
        <div class="seq mono">${String(i+1).padStart(2,'0')}</div>
        <div class="dur mono">${clip.dur || '?'}</div>
      </div>
      <div class="card-body">
        <input type="text" class="fname" readonly>
        <div class="field-label">What's in this shot</div>
        <textarea class="desc" placeholder="describe what the image/clip shows"></textarea>
        <div class="field-label">Generation prompt</div>
        <textarea class="prompt" placeholder="text used to generate this image, if known"></textarea>
        <div class="field-label">Feedback</div>
        <textarea class="note" placeholder="what's wrong with this clip / story note"></textarea>
        <span class="path"></span>
      </div>`;
    if(clip.thumb) card.querySelector('.thumb img').src = clip.thumb;
    const thumb = card.querySelector('.thumb');
    // native drag-and-drop suppresses the click event after an actual drag, so this
    // only fires on a plain click (used to reorder cards, this listener opens the zoom view)
    thumb.addEventListener('click', () => { if(clip.thumb) openLightbox(clip.id); });
    const fname = card.querySelector('.fname');
    fname.value = clip.title;
    fname.title = clip.path;
    card.querySelector('.path').textContent = clip.path;
    const desc = card.querySelector('.desc');
    desc.value = clip.description || "";
    desc.addEventListener('input', e => updateField(clip.id, 'description', e.target.value));
    desc.addEventListener('mousedown', e => e.stopPropagation());
    desc.addEventListener('dragstart', e => { e.preventDefault(); e.stopPropagation(); });
    const promptField = card.querySelector('.prompt');
    promptField.value = clip.prompt || "";
    promptField.addEventListener('input', e => updateField(clip.id, 'prompt', e.target.value));
    promptField.addEventListener('mousedown', e => e.stopPropagation());
    promptField.addEventListener('dragstart', e => { e.preventDefault(); e.stopPropagation(); });
    const note = card.querySelector('.note');
    note.value = clip.note || "";
    note.addEventListener('input', e => updateField(clip.id, 'note', e.target.value));
    note.addEventListener('mousedown', e => e.stopPropagation());
    note.addEventListener('dragstart', e => { e.preventDefault(); e.stopPropagation(); });
    card.addEventListener('dragstart', () => { dragId = clip.id; card.classList.add('dragging'); });
    card.addEventListener('dragend', () => card.classList.remove('dragging'));
    card.addEventListener('dragover', (e) => { e.preventDefault(); card.classList.add('drag-over'); });
    card.addEventListener('dragleave', () => card.classList.remove('drag-over'));
    card.addEventListener('drop', (e) => { e.preventDefault(); card.classList.remove('drag-over'); reorder(dragId, clip.id); });
    board.appendChild(card);
  });
}

function reorder(fromId, toId){
  if(fromId === toId) return;
  const fromIdx = clips.findIndex(c => c.id === fromId);
  const toIdx = clips.findIndex(c => c.id === toId);
  if(fromIdx === -1 || toIdx === -1) return;
  const [moved] = clips.splice(fromIdx, 1);
  clips.splice(toIdx, 0, moved);
  saveOrder();
  render();
}

let lbId = null;

function openLightbox(id){
  lbId = id;
  renderLightbox();
  document.getElementById('lightbox').classList.add('show');
}

function closeLightbox(){
  document.getElementById('lightbox').classList.remove('show');
  lbId = null;
}

function navLightbox(delta){
  const withThumbs = clips.filter(c => c.thumb);
  if(!withThumbs.length) return;
  const idx = withThumbs.findIndex(c => c.id === lbId);
  const next = withThumbs[(idx + delta + withThumbs.length) % withThumbs.length];
  lbId = next.id;
  renderLightbox();
}

function renderLightbox(){
  const clip = clips.find(c => c.id === lbId);
  if(!clip) return;
  const i = clips.findIndex(c => c.id === lbId);
  document.getElementById('lbImg').src = clip.thumb;
  document.getElementById('lbTitle').textContent = `${String(i+1).padStart(2,'0')}. ${clip.title}`;
  document.getElementById('lbMeta').textContent = clip.dur ? `  ·  ${clip.dur}` : '';
}

document.getElementById('lightbox').addEventListener('click', (e) => {
  if(e.target.id === 'lightbox') closeLightbox();
});
document.addEventListener('keydown', (e) => {
  if(!document.getElementById('lightbox').classList.contains('show')) return;
  if(e.key === 'Escape') closeLightbox();
  else if(e.key === 'ArrowLeft') navLightbox(-1);
  else if(e.key === 'ArrowRight') navLightbox(1);
});

function showToast(msg){
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2600);
}

function sequenceText(){
  return clips.map((c,i) => `${i+1}. ${c.title}${c.dur ? '  ['+c.dur+']' : ''}${c.note ? '  — '+c.note : ''}`).join('\n');
}

function exportText(){
  const text = sequenceText();
  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(text)
      .then(() => showToast("Copied sequence to clipboard"))
      .catch(() => window.prompt("Copy the sequence:", text));
  } else {
    window.prompt("Copy the sequence:", text);
  }
}

const IMAGE_DURATION_SEC = 3;

function exportConcat(){
  const esc = p => p.replace(/'/g, "'\\''");
  const rows = [];
  clips.forEach((c, i) => {
    rows.push(`file '${esc(c.path)}'`);
    if (c.isImage) rows.push(`duration ${IMAGE_DURATION_SEC}`);
  });
  // ffmpeg's concat demuxer ignores the last entry's "duration" line, so if the
  // sequence ends on a still image, repeat its file line per the documented workaround.
  if (clips.length && clips[clips.length - 1].isImage) {
    rows.push(`file '${esc(clips[clips.length - 1].path)}'`);
  }
  const hasImages = clips.some(c => c.isImage);
  const lines = rows.join('\n') + '\n';
  const blob = new Blob([lines], {type: "text/plain"});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = "concat_list.txt";
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 5000);
  const cmd = hasImages
    ? "ffmpeg -f concat -safe 0 -i concat_list.txt -vsync vfr -pix_fmt yuv420p out.mp4  (re-encode required — sequence mixes stills and video)"
    : "ffmpeg -f concat -safe 0 -i concat_list.txt -c copy out.mp4";
  showToast("Downloaded concat_list.txt \n Run: " + cmd);
}

function slugifyJs(text){
  return (text || "storyboard").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "") || "storyboard";
}

function buildManifest(title, storyText){
  const lines = [`# ${title}`];
  if (storyText && storyText.trim()) { lines.push(""); lines.push(storyText.trim()); }
  lines.push("");
  clips.forEach((c, i) => {
    const n = String(i + 1).padStart(2, "0");
    lines.push(`## ${n}. ${c.title}`);
    lines.push(`Duration: ${c.dur || "?"}`);
    if (c.description) { lines.push(""); lines.push(`**What's in this shot:** ${c.description}`); }
    if (c.prompt) { lines.push(""); lines.push(`**Generation prompt:** ${c.prompt}`); }
    if (c.note) { lines.push(""); lines.push(`**Feedback:** ${c.note}`); }
    lines.push("");
  });
  return lines.join("\n");
}

function dataUriToBytes(dataUri){
  const binary = atob(dataUri.split(",")[1]);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
  return bytes;
}

let _crc32Table = null;
function crc32(bytes){
  if (!_crc32Table) {
    _crc32Table = new Uint32Array(256);
    for (let n = 0; n < 256; n++) {
      let c = n;
      for (let k = 0; k < 8; k++) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
      _crc32Table[n] = c >>> 0;
    }
  }
  let crc = 0xFFFFFFFF;
  for (let i = 0; i < bytes.length; i++) crc = (crc >>> 8) ^ _crc32Table[(crc ^ bytes[i]) & 0xFF];
  return (crc ^ 0xFFFFFFFF) >>> 0;
}

// Minimal ZIP writer (STORE method, no compression — images are already compressed).
function makeZip(files){
  const encoder = new TextEncoder();
  const localParts = [], centralParts = [];
  let offset = 0;
  const dosTime = 0, dosDate = 0x21;

  files.forEach(f => {
    const nameBytes = encoder.encode(f.name);
    const data = f.data;
    const crc = crc32(data);
    const size = data.length;

    const lh = new Uint8Array(30 + nameBytes.length);
    const lv = new DataView(lh.buffer);
    lv.setUint32(0, 0x04034b50, true);
    lv.setUint16(4, 20, true);
    lv.setUint16(6, 0, true);
    lv.setUint16(8, 0, true);
    lv.setUint16(10, dosTime, true);
    lv.setUint16(12, dosDate, true);
    lv.setUint32(14, crc, true);
    lv.setUint32(18, size, true);
    lv.setUint32(22, size, true);
    lv.setUint16(26, nameBytes.length, true);
    lv.setUint16(28, 0, true);
    lh.set(nameBytes, 30);
    localParts.push(lh, data);

    const ch = new Uint8Array(46 + nameBytes.length);
    const cv = new DataView(ch.buffer);
    cv.setUint32(0, 0x02014b50, true);
    cv.setUint16(4, 20, true);
    cv.setUint16(6, 20, true);
    cv.setUint16(8, 0, true);
    cv.setUint16(10, 0, true);
    cv.setUint16(12, dosTime, true);
    cv.setUint16(14, dosDate, true);
    cv.setUint32(16, crc, true);
    cv.setUint32(20, size, true);
    cv.setUint32(24, size, true);
    cv.setUint16(28, nameBytes.length, true);
    cv.setUint32(42, offset, true);
    ch.set(nameBytes, 46);
    centralParts.push(ch);

    offset += lh.length + data.length;
  });

  const centralSize = centralParts.reduce((s, p) => s + p.length, 0);
  const end = new Uint8Array(22);
  const ev = new DataView(end.buffer);
  ev.setUint32(0, 0x06054b50, true);
  ev.setUint16(8, files.length, true);
  ev.setUint16(10, files.length, true);
  ev.setUint32(12, centralSize, true);
  ev.setUint32(16, offset, true);

  return new Blob([...localParts, ...centralParts, end], {type: "application/zip"});
}

function exportPacket(){
  const title = document.title;
  const storyText = document.getElementById('storyText').value;
  const files = [{name: "manifest.md", data: new TextEncoder().encode(buildManifest(title, storyText))}];
  clips.forEach((c, i) => {
    if (!c.thumb) return;
    const n = String(i + 1).padStart(2, "0");
    const base = slugifyJs(c.title.replace(/\.[^.]+$/, ""));
    files.push({name: `${n}-${base}.jpg`, data: dataUriToBytes(c.thumb)});
  });
  const blob = makeZip(files);
  const name = slugifyJs(title) + "_review_packet.zip";
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = name;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 5000);
  showToast(`Downloaded ${name} \n Drag it into Google Drive for Gemini review`);
}

function notesFileName(){
  const outPath = __STORE_KEY__;
  const base = outPath.split('/').pop().replace(/\.html?$/i, "");
  return base + ".notes.json";
}

function exportNotes(){
  const payload = {
    order: clips.map(c => c.id),
    notes: Object.fromEntries(clips.map(c => [c.id, c.note || ""])),
    descriptions: Object.fromEntries(clips.map(c => [c.id, c.description || ""])),
    prompts: Object.fromEntries(clips.map(c => [c.id, c.prompt || ""])),
    storyText: document.getElementById('storyText').value,
    preflight: preflightChecked,
  };
  const name = notesFileName();
  const blob = new Blob([JSON.stringify(payload, null, 2)], {type: "application/json"});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = name;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 5000);
  showToast(`Downloaded ${name} \n Keep it next to this board (or pass --notes) so re-running storyboard.py keeps these notes even if this browser's storage is ever cleared`);
}

function resetBoard(){
  if(confirm("Clear saved order, descriptions, notes, story text, and the preflight checklist for this storyboard?")){
    localStorage.removeItem(STORAGE_KEY);
    localStorage.removeItem(STORY_TEXT_KEY);
    localStorage.removeItem(PREFLIGHT_KEY);
    document.getElementById('storyText').value = "";
    preflightChecked = {...DEFAULT_PREFLIGHT};
    renderPreflight();
    clips = SCANNED.map(c => ({...c}));
    render();
  }
}

render();
</script>
</body>
</html>
"""


def build_html(sources_label: str, store_key: str, clips, default_preflight=None, default_story_text=None):
    page = PAGE_TEMPLATE
    page = page.replace("__TITLE__", html.escape(sources_label))
    page = page.replace("__SOURCES__", html.escape(sources_label))
    page = page.replace("__CLIPS_JSON__", json.dumps(clips))
    page = page.replace("__STORE_KEY__", json.dumps(store_key))
    page = page.replace("__DEFAULT_PREFLIGHT__", json.dumps(default_preflight or {}))
    page = page.replace("__DEFAULT_STORY_TEXT__", json.dumps(default_story_text or ""))
    return page


INDEX_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Storyboards — __DIR_NAME__</title>
<style>
  :root{
    --bg:#1C1A17; --card:#2C2720; --card-edge:#3A342A;
    --amber:#E8A33D; --amber-dim:#8A6528;
    --text:#F0EBE3; --text-muted:#9C948A; --text-faint:#655D51;
  }
  *{box-sizing:border-box;}
  body{margin:0;background:radial-gradient(ellipse at top left, rgba(232,163,61,0.05), transparent 55%), var(--bg);
    color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;min-height:100vh;}
  .mono{font-family:"SF Mono","JetBrains Mono",Consolas,"Courier New",monospace;}
  header{padding:28px 32px 20px;border-bottom:1px solid var(--card-edge);}
  header h1{margin:0 0 4px;font-size:22px;font-weight:700;}
  header p{margin:0;color:var(--text-muted);font-size:13px;}
  main{padding:24px 32px 60px;max-width:900px;margin:0 auto;}
  .grid{display:flex;flex-direction:column;gap:10px;}
  a.board{display:flex;align-items:center;justify-content:space-between;gap:16px;
    background:var(--card);border:1px solid var(--card-edge);border-radius:10px;
    padding:16px 18px;text-decoration:none;color:var(--text);transition:border-color .1s ease;}
  a.board:hover{border-color:var(--amber);}
  .board-title{font-size:15px;font-weight:600;}
  .board-file{font-size:11px;color:var(--text-faint);margin-top:3px;word-break:break-all;}
  .board-count{flex-shrink:0;text-align:center;background:var(--bg);border:1px solid var(--card-edge);
    border-radius:8px;padding:8px 14px;}
  .board-count .num{display:block;font-size:18px;font-weight:700;color:var(--amber);}
  .board-count .lbl{font-size:10px;color:var(--text-muted);text-transform:uppercase;letter-spacing:.04em;}
  .empty{color:var(--text-muted);padding:40px 0;text-align:center;}
</style>
</head>
<body>
<header>
  <h1>Storyboards</h1>
  <p><span class="mono">__DIR_PATH__</span> &middot; re-run <code>storyboard.py --index</code> any time boards are added or removed</p>
</header>
<main>
  <div class="grid">__BOARD_ROWS__</div>
</main>
</body>
</html>
"""

BOARD_ROW_TEMPLATE = """    <a class="board" href="__HREF__">
      <div>
        <div class="board-title">__TITLE__</div>
        <div class="board-file mono">__FILE__</div>
      </div>
      <div class="board-count"><span class="num mono">__COUNT__</span><span class="lbl">clips</span></div>
    </a>"""


COMBINE_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Storyboard — __TITLE__</title>
<style>
  :root{
    --bg:#1C1A17; --panel:#252119; --card:#2C2720; --card-edge:#3A342A;
    --amber:#E8A33D; --amber-dim:#8A6528; --teal:#4F9B8E;
    --text:#F0EBE3; --text-muted:#9C948A; --text-faint:#655D51; --danger:#C96A4F;
  }
  *{box-sizing:border-box;}
  body{margin:0;background:radial-gradient(ellipse at top left, rgba(232,163,61,0.05), transparent 55%), var(--bg);
    color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;min-height:100vh;}
  .mono{font-family:"SF Mono","JetBrains Mono",Consolas,"Courier New",monospace;}
  header{padding:28px 32px 20px;border-bottom:1px solid var(--card-edge);display:flex;align-items:flex-end;
    justify-content:space-between;flex-wrap:wrap;gap:16px;}
  .title-block h1{margin:0 0 4px;font-size:22px;font-weight:700;}
  .title-block p{margin:0;color:var(--text-muted);font-size:13px;}
  .tally{text-align:right;font-size:12px;color:var(--text-muted);}
  .tally .num{font-size:26px;color:var(--amber);font-weight:700;display:block;line-height:1.1;}
  .tabs{display:flex;gap:6px;padding:14px 32px 0;flex-wrap:wrap;border-bottom:1px solid var(--card-edge);}
  .tab{background:transparent;border:1px solid transparent;border-bottom:none;color:var(--text-muted);
    font-family:inherit;font-size:13px;font-weight:600;padding:9px 16px;border-radius:8px 8px 0 0;
    cursor:pointer;margin-bottom:-1px;}
  .tab:hover{color:var(--text);}
  .tab.active{color:var(--text);background:var(--card);border-color:var(--card-edge);}
  .tab .tab-count{color:var(--text-faint);font-weight:400;margin-left:5px;}
  .tab.active .tab-count{color:var(--amber-dim);}
  .story-text{width:100%;margin:14px 32px 0;max-width:900px;background:transparent;
    border:1px dashed var(--card-edge);border-radius:8px;color:var(--text);
    font-size:14px;line-height:1.5;padding:11px 14px;resize:vertical;min-height:44px;
    font-family:inherit;}
  .story-text:focus{outline:none;border-style:solid;border-color:var(--amber-dim);}
  .story-text::placeholder{color:var(--text-faint);}
  main{padding:24px 32px 60px;margin:0 auto;}
  button{font-family:inherit;cursor:pointer;border:none;border-radius:5px;font-size:13px;padding:9px 16px;
    font-weight:600;transition:transform .08s ease, opacity .12s ease;}
  button:active{transform:scale(0.97);}
  .btn-primary{background:var(--amber);color:#1C1A17;}
  .btn-primary:hover{opacity:0.9;}
  .btn-ghost{background:transparent;color:var(--text-muted);border:1px solid var(--card-edge);}
  .btn-ghost:hover{color:var(--text);border-color:var(--text-faint);}
  .toolbar{display:flex;justify-content:flex-end;gap:8px;margin-bottom:16px;flex-wrap:wrap;}
  .board{display:flex;flex-direction:row;flex-wrap:wrap;align-items:flex-start;gap:16px;}
  .card{display:flex;flex-direction:column;width:260px;flex-shrink:0;background:var(--card);
    border:1px solid var(--card-edge);border-radius:8px;overflow:hidden;
    position:relative;cursor:grab;}
  .card.dragging{opacity:0.35;}
  .card.drag-over{border-color:var(--amber);}
  .sprockets{height:16px;flex-shrink:0;border-bottom:1px solid var(--card-edge);position:relative;}
  .sprockets::before{content:"";position:absolute;inset:0;
    background-image:radial-gradient(circle, var(--bg) 3px, transparent 3.5px);
    background-size:20px 100%;background-position:8px center;}
  .thumb{position:relative;width:100%;aspect-ratio:16/9;flex-shrink:0;background:#000;
    display:flex;align-items:center;justify-content:center;overflow:hidden;
    border-bottom:1px solid var(--card-edge);cursor:zoom-in;}
  .thumb img{width:100%;height:100%;object-fit:cover;display:block;}
  .thumb .noimg{color:var(--text-faint);font-size:10px;text-align:center;padding:4px;}
  .seq{position:absolute;top:6px;left:6px;min-width:20px;height:20px;padding:0 5px;border-radius:10px;
    background:var(--amber);color:#1C1A17;font-size:11px;font-weight:700;
    display:flex;align-items:center;justify-content:center;}
  .dur{position:absolute;bottom:6px;right:6px;background:rgba(0,0,0,.75);color:#fff;
    font-size:10px;padding:2px 6px;border-radius:4px;}
  .card-body{display:flex;flex-direction:column;gap:6px;padding:10px 12px 12px;min-width:0;}
  .card input[type="text"]{background:transparent;border:none;border-bottom:1px solid transparent;
    color:var(--text);font-size:13px;font-weight:600;padding:2px 0;width:100%;}
  .card input[type="text"]:focus{outline:none;border-bottom:1px solid var(--amber-dim);}
  .card .desc, .card .note{background:transparent;border:none;color:var(--text-muted);font-size:12px;
    padding:0;width:100%;font-weight:400;resize:none;font-family:inherit;min-height:32px;line-height:1.35;}
  .card .note{color:var(--amber-dim);border-top:1px dashed var(--card-edge);padding-top:6px;margin-top:2px;}
  .card .desc:focus, .card .note:focus{outline:none;color:var(--text);}
  .card .desc::placeholder, .card .note::placeholder, .card input::placeholder{color:var(--text-faint);}
  .field-label{font-size:9px;text-transform:uppercase;letter-spacing:.04em;color:var(--text-faint);margin:2px 0 -3px;}
  .path{font-size:9px;color:var(--text-faint);word-break:break-all;}
  .toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%) translateY(8px);background:var(--amber);
    color:#1C1A17;padding:10px 18px;border-radius:6px;font-size:13px;font-weight:600;opacity:0;
    pointer-events:none;transition:opacity .2s ease, transform .2s ease;white-space:pre;}
  .toast.show{opacity:1;transform:translateX(-50%) translateY(0);}
  .lightbox{position:fixed;inset:0;background:rgba(10,9,7,.92);z-index:50;
    display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;
    padding:40px;cursor:zoom-out;opacity:0;pointer-events:none;transition:opacity .15s ease;}
  .lightbox.show{opacity:1;pointer-events:auto;}
  .lightbox img{max-width:90vw;max-height:78vh;object-fit:contain;border-radius:6px;
    box-shadow:0 20px 60px rgba(0,0,0,.6);cursor:default;}
  .lightbox .lb-caption{color:var(--text-muted);font-size:13px;text-align:center;max-width:80vw;}
  .lightbox .lb-caption .lb-title{color:var(--text);font-weight:600;margin-right:8px;}
  .lightbox .lb-nav{position:absolute;top:50%;transform:translateY(-50%);background:rgba(44,39,32,.8);
    border:1px solid var(--card-edge);color:var(--text);width:44px;height:44px;border-radius:50%;
    font-size:20px;display:flex;align-items:center;justify-content:center;cursor:pointer;}
  .lightbox .lb-nav:hover{border-color:var(--amber);color:var(--amber);}
  .lightbox .lb-prev{left:24px;}
  .lightbox .lb-next{right:24px;}
  .lightbox .lb-close{position:absolute;top:20px;right:24px;background:transparent;border:none;
    color:var(--text-muted);font-size:26px;cursor:pointer;line-height:1;}
  .lightbox .lb-close:hover{color:var(--text);}
  .preflight{margin-bottom:16px;background:var(--card);border:1px solid var(--card-edge);
    border-radius:10px;overflow:hidden;}
  .pf-header{display:flex;align-items:center;justify-content:space-between;gap:14px;
    padding:13px 18px;cursor:pointer;}
  .pf-header:hover{background:rgba(255,255,255,.02);}
  .pf-header-left{display:flex;align-items:center;gap:10px;}
  .pf-header h3{margin:0;font-size:13.5px;font-weight:700;}
  .pf-caret{color:var(--text-faint);font-size:11px;transition:transform .15s ease;}
  .preflight.open .pf-caret{transform:rotate(90deg);}
  .pf-progress{display:flex;align-items:center;gap:10px;}
  .pf-count{font-size:12px;color:var(--text-muted);font-variant-numeric:tabular-nums;white-space:nowrap;}
  .pf-count b{color:var(--amber);}
  .pf-track{width:70px;height:5px;border-radius:3px;background:var(--bg);overflow:hidden;}
  .pf-fill{height:100%;background:var(--amber);border-radius:3px;width:0%;transition:width .2s ease;}
  .pf-body{display:none;padding:2px 18px 16px;border-top:1px solid var(--card-edge);}
  .preflight.open .pf-body{display:block;}
  .pf-section{padding-top:14px;}
  .pf-section h4{margin:0 0 2px;font-size:12px;font-weight:700;color:var(--amber-dim);
    text-transform:uppercase;letter-spacing:.04em;}
  .pf-section p{margin:0 0 6px;font-size:11.5px;color:var(--text-faint);}
  .pf-item{display:flex;align-items:flex-start;gap:10px;padding:7px 0;border-top:1px solid var(--card-edge);}
  .pf-item:first-of-type{border-top:none;}
  .pf-item input[type="checkbox"]{appearance:none;-webkit-appearance:none;flex-shrink:0;
    margin-top:2px;width:17px;height:17px;border-radius:5px;border:1.5px solid var(--card-edge);
    background:var(--bg);position:relative;cursor:pointer;}
  .pf-item input[type="checkbox"]:checked{background:var(--amber);border-color:var(--amber);}
  .pf-item input[type="checkbox"]:checked::after{content:"";position:absolute;left:4.5px;top:1px;
    width:4.5px;height:8px;border:solid #1C1A17;border-width:0 2px 2px 0;transform:rotate(40deg);}
  .pf-item span{font-size:13px;color:var(--text-muted);line-height:1.4;}
  .pf-item.checked span{color:var(--text-faint);text-decoration:line-through;text-decoration-color:var(--card-edge);}
  @media (prefers-reduced-motion: reduce){*{transition:none !important;}}
</style>
</head>
<body>

<header>
  <div class="title-block">
    <h1 id="storyTitle">Clip Storyboard</h1>
    <p><span class="mono" id="storySource"></span> &middot; each story keeps its own order &amp; notes</p>
  </div>
  <div class="tally">
    <span class="num mono" id="clipCount">0</span>
    <span>clips &middot; <span id="totalDur" class="mono">0:00</span> total</span>
  </div>
</header>

<nav class="tabs" id="tabs"></nav>

<textarea class="story-text" id="storyText" placeholder="Story text — describe what this story is about, for context when sharing it for feedback…"></textarea>

<main>
  <div class="preflight" id="preflight">
    <div class="pf-header" onclick="togglePreflight()">
      <div class="pf-header-left">
        <span class="pf-caret">&#9656;</span>
        <h3>Preflight — pre-publish checklist</h3>
      </div>
      <div class="pf-progress">
        <div class="pf-count"><b id="pfDone">0</b>/<span id="pfTotal">0</span></div>
        <div class="pf-track"><div class="pf-fill" id="pfFill"></div></div>
      </div>
    </div>
    <div class="pf-body" id="pfBody"></div>
  </div>

  <div class="toolbar">
    <button class="btn-ghost" onclick="resetBoard()">Reset this story's order, text &amp; notes</button>
    <button class="btn-ghost" onclick="exportText()">Copy sequence as text</button>
    <button class="btn-ghost" onclick="exportNotes()">Save notes (.json)</button>
    <button class="btn-ghost" onclick="exportPacket()">Download review packet (.zip)</button>
    <button class="btn-primary" onclick="exportConcat()">Download ffmpeg concat file</button>
  </div>
  <div class="board" id="board"></div>
</main>

<div class="toast" id="toast"></div>

<div class="lightbox" id="lightbox">
  <button class="lb-close" onclick="closeLightbox()">&times;</button>
  <button class="lb-nav lb-prev" onclick="event.stopPropagation(); navLightbox(-1)">&#8249;</button>
  <img id="lbImg">
  <button class="lb-nav lb-next" onclick="event.stopPropagation(); navLightbox(1)">&#8250;</button>
  <div class="lb-caption"><span class="lb-title" id="lbTitle"></span><span id="lbMeta"></span></div>
</div>

<script>
const STORIES = __STORIES_JSON__;
const COMBO_KEY = "storyboard_combined_active_" + __COMBO_KEY__;

let activeIndex = (() => {
  const saved = parseInt(localStorage.getItem(COMBO_KEY), 10);
  return (saved >= 0 && saved < STORIES.length) ? saved : 0;
})();
let clips = [];
let dragId = null;

function storageKeyFor(i){ return "storyboard_combined_story_" + STORIES[i].key; }

function loadOrder(i){
  const SCANNED = STORIES[i].clips;
  try{
    const saved = JSON.parse(localStorage.getItem(storageKeyFor(i)) || "null");
    if(saved && Array.isArray(saved)){
      // Reconcile saved order/notes with this story's scanned data (scan wins for media).
      const byId = Object.fromEntries(SCANNED.map(c => [c.id, c]));
      const merged = saved.filter(s => byId[s.id]).map(s => ({...byId[s.id],
        note: s.note || "", description: s.description || "", prompt: s.prompt || ""}));
      const savedIds = new Set(saved.map(s => s.id));
      SCANNED.forEach(c => { if(!savedIds.has(c.id)) merged.push({...c}); });
      if(merged.length) return merged;
    }
  } catch(e){}
  return SCANNED.map(c => ({...c}));
}

function saveOrder(){
  const toSave = clips.map(c => ({id: c.id, note: c.note, description: c.description, prompt: c.prompt}));
  localStorage.setItem(storageKeyFor(activeIndex), JSON.stringify(toSave));
}

function storyTextKeyFor(i){ return storageKeyFor(i) + "::storytext"; }

function loadStoryText(i){
  document.getElementById('storyText').value = localStorage.getItem(storyTextKeyFor(i)) || "";
}

document.getElementById('storyText').addEventListener('input', e => {
  localStorage.setItem(storyTextKeyFor(activeIndex), e.target.value);
});

const PREFLIGHT_DATA = [
  { key: "hook", title: "Hook", desc: "The first three seconds decide whether anyone stays.", items: [
    "States the single claim or question in the first 3 seconds, before any logo or intro",
    "First frame is fully composed the instant it loads — no fade-up from blank",
    "Cut the weakest 5 seconds; every second left in earns its place",
  ]},
  { key: "format", title: "Format & safe zones", desc: "Vertical, and clear of the platform's own UI.", items: [
    "Exported at 1080×1920 (9:16) — not cropped or letterboxed from a wider master",
    "Burned-in text sits clear of the bottom-left caption/sound UI and the right-edge button rail",
    "Checked real device crop risk at the very top and bottom of frame, not just the raw canvas",
  ]},
  { key: "claims", title: "Claims & sourcing", desc: "Nothing on screen that can't be backed up.", items: [
    "Every on-screen claim carries a source chip or citation a viewer could actually verify",
    "No claim states a result beyond what the cited study's own duration supports",
    "Unsourced or refused claims render nothing — no placeholder text, no “coming soon”",
  ]},
  { key: "captions", title: "Captions & legibility", desc: "Most of this gets watched on mute.", items: [
    "Captions are burned in — sound is a bonus, not a requirement",
    "Watched the export at actual phone width, not just the desktop preview size",
    "Korean/English text renders with no missing glyphs or fallback-font boxes",
  ]},
  { key: "loop", title: "Loop & pacing", desc: "How it ends is part of how it starts.", items: [
    "If it's meant to loop, the last frame rhymes with the first — no jump-cut at the seam",
    "Runtime matches the idea; nothing padded just to hit a round number",
  ]},
  { key: "metadata", title: "Title, description & cover", desc: "What gets someone to click before they've seen a frame.", items: [
    "Title states the specific claim or question, not a vague category label",
    "Description includes real sources or links, not only hashtags",
    "Cover frame (if used) is legible at true small size, not just full-screen preview",
  ]},
  { key: "final", title: "Final pass", desc: "One last look, the way a viewer will actually see it.", items: [
    "Watched the whole thing once with sound off",
    "Watched the whole thing once with sound on, on a phone",
    "Confirmed the file about to upload is the current export, not an old one",
  ]},
];

function preflightKeyFor(i){ return storageKeyFor(i) + "::preflight"; }
function preflightOpenKeyFor(i){ return storageKeyFor(i) + "::preflight_open"; }

function loadPreflight(i){
  try {
    const saved = JSON.parse(localStorage.getItem(preflightKeyFor(i)));
    if (saved) return saved;
  } catch(e){}
  return {...(STORIES[i].defaultPreflight || {})};
}
let preflightChecked = {};

function pfItemId(sectionKey, i){ return sectionKey + "-" + i; }

function renderPreflight(){
  preflightChecked = loadPreflight(activeIndex);
  const body = document.getElementById('pfBody');
  body.innerHTML = "";
  let total = 0;
  PREFLIGHT_DATA.forEach(section => {
    const sec = document.createElement('div');
    sec.className = 'pf-section';
    const h4 = document.createElement('h4'); h4.textContent = section.title;
    const p = document.createElement('p'); p.textContent = section.desc;
    sec.appendChild(h4); sec.appendChild(p);
    section.items.forEach((text, i) => {
      total++;
      const id = pfItemId(section.key, i);
      const item = document.createElement('div');
      item.className = 'pf-item' + (preflightChecked[id] ? ' checked' : '');
      const cb = document.createElement('input');
      cb.type = 'checkbox';
      cb.checked = !!preflightChecked[id];
      cb.addEventListener('change', () => {
        preflightChecked[id] = cb.checked;
        item.classList.toggle('checked', cb.checked);
        localStorage.setItem(preflightKeyFor(activeIndex), JSON.stringify(preflightChecked));
        updatePreflightProgress();
      });
      const span = document.createElement('span'); span.textContent = text;
      item.appendChild(cb); item.appendChild(span);
      sec.appendChild(item);
    });
    body.appendChild(sec);
  });
  document.getElementById('pfTotal').textContent = total;
  updatePreflightProgress();
}

function updatePreflightProgress(){
  const total = PREFLIGHT_DATA.reduce((n, s) => n + s.items.length, 0);
  const done = Object.values(preflightChecked).filter(Boolean).length;
  document.getElementById('pfDone').textContent = done;
  document.getElementById('pfFill').style.width = (total ? Math.round(done / total * 100) : 0) + '%';
}

function togglePreflight(){
  const el = document.getElementById('preflight');
  const open = el.classList.toggle('open');
  localStorage.setItem(preflightOpenKeyFor(activeIndex), open ? '1' : '0');
}

function updateField(id, field, value){
  const clip = clips.find(c => c.id === id);
  if(clip){ clip[field] = value; saveOrder(); }
}

function renderTabs(){
  const tabs = document.getElementById('tabs');
  tabs.innerHTML = "";
  STORIES.forEach((story, i) => {
    const btn = document.createElement('button');
    btn.className = 'tab' + (i === activeIndex ? ' active' : '');
    btn.innerHTML = `${escapeHtml(story.title)}<span class="tab-count mono">${story.clips.length}</span>`;
    btn.addEventListener('click', () => switchStory(i));
    tabs.appendChild(btn);
  });
}

function escapeHtml(s){
  const d = document.createElement('div');
  d.textContent = s;
  return d.innerHTML;
}

function switchStory(i){
  if(i === activeIndex) return;
  activeIndex = i;
  localStorage.setItem(COMBO_KEY, String(i));
  clips = loadOrder(activeIndex);
  document.getElementById('storyTitle').textContent = STORIES[activeIndex].title;
  loadStoryText(activeIndex);
  document.getElementById('preflight').classList.toggle('open',
    localStorage.getItem(preflightOpenKeyFor(activeIndex)) === '1');
  renderPreflight();
  renderTabs();
  render();
}

function render(){
  const board = document.getElementById('board');
  board.innerHTML = "";
  document.getElementById('clipCount').textContent = clips.length;
  const totalSec = clips.reduce((s,c) => s + (c.durSec || 0), 0);
  const m = Math.floor(totalSec/60), s = Math.round(totalSec%60).toString().padStart(2,'0');
  document.getElementById('totalDur').textContent = `${m}:${s}`;
  document.getElementById('storySource').textContent = clips.length ? clips[0].path.replace(/\/[^/]*$/, '') : '';

  clips.forEach((clip, i) => {
    const card = document.createElement('div');
    card.className = 'card';
    card.draggable = true;
    card.dataset.id = clip.id;
    card.innerHTML = `
      <div class="sprockets"></div>
      <div class="thumb">
        ${clip.thumb ? `<img>` : `<span class="noimg">no thumb</span>`}
        <div class="seq mono">${String(i+1).padStart(2,'0')}</div>
        <div class="dur mono">${clip.dur || '?'}</div>
      </div>
      <div class="card-body">
        <input type="text" class="fname" readonly>
        <div class="field-label">What's in this shot</div>
        <textarea class="desc" placeholder="describe what the image/clip shows"></textarea>
        <div class="field-label">Generation prompt</div>
        <textarea class="prompt" placeholder="text used to generate this image, if known"></textarea>
        <div class="field-label">Feedback</div>
        <textarea class="note" placeholder="what's wrong with this clip / story note"></textarea>
        <span class="path"></span>
      </div>`;
    if(clip.thumb) card.querySelector('.thumb img').src = clip.thumb;
    const thumb = card.querySelector('.thumb');
    thumb.addEventListener('click', () => { if(clip.thumb) openLightbox(clip.id); });
    const fname = card.querySelector('.fname');
    fname.value = clip.title;
    fname.title = clip.path;
    card.querySelector('.path').textContent = clip.path;
    const desc = card.querySelector('.desc');
    desc.value = clip.description || "";
    desc.addEventListener('input', e => updateField(clip.id, 'description', e.target.value));
    desc.addEventListener('mousedown', e => e.stopPropagation());
    desc.addEventListener('dragstart', e => { e.preventDefault(); e.stopPropagation(); });
    const promptField = card.querySelector('.prompt');
    promptField.value = clip.prompt || "";
    promptField.addEventListener('input', e => updateField(clip.id, 'prompt', e.target.value));
    promptField.addEventListener('mousedown', e => e.stopPropagation());
    promptField.addEventListener('dragstart', e => { e.preventDefault(); e.stopPropagation(); });
    const note = card.querySelector('.note');
    note.value = clip.note || "";
    note.addEventListener('input', e => updateField(clip.id, 'note', e.target.value));
    note.addEventListener('mousedown', e => e.stopPropagation());
    note.addEventListener('dragstart', e => { e.preventDefault(); e.stopPropagation(); });
    card.addEventListener('dragstart', () => { dragId = clip.id; card.classList.add('dragging'); });
    card.addEventListener('dragend', () => card.classList.remove('dragging'));
    card.addEventListener('dragover', (e) => { e.preventDefault(); card.classList.add('drag-over'); });
    card.addEventListener('dragleave', () => card.classList.remove('drag-over'));
    card.addEventListener('drop', (e) => { e.preventDefault(); card.classList.remove('drag-over'); reorder(dragId, clip.id); });
    board.appendChild(card);
  });
}

function reorder(fromId, toId){
  if(fromId === toId) return;
  const fromIdx = clips.findIndex(c => c.id === fromId);
  const toIdx = clips.findIndex(c => c.id === toId);
  if(fromIdx === -1 || toIdx === -1) return;
  const [moved] = clips.splice(fromIdx, 1);
  clips.splice(toIdx, 0, moved);
  saveOrder();
  render();
}

let lbId = null;

function openLightbox(id){
  lbId = id;
  renderLightbox();
  document.getElementById('lightbox').classList.add('show');
}

function closeLightbox(){
  document.getElementById('lightbox').classList.remove('show');
  lbId = null;
}

function navLightbox(delta){
  const withThumbs = clips.filter(c => c.thumb);
  if(!withThumbs.length) return;
  const idx = withThumbs.findIndex(c => c.id === lbId);
  const next = withThumbs[(idx + delta + withThumbs.length) % withThumbs.length];
  lbId = next.id;
  renderLightbox();
}

function renderLightbox(){
  const clip = clips.find(c => c.id === lbId);
  if(!clip) return;
  const i = clips.findIndex(c => c.id === lbId);
  document.getElementById('lbImg').src = clip.thumb;
  document.getElementById('lbTitle').textContent = `${String(i+1).padStart(2,'0')}. ${clip.title}`;
  document.getElementById('lbMeta').textContent = clip.dur ? `  ·  ${clip.dur}` : '';
}

document.getElementById('lightbox').addEventListener('click', (e) => {
  if(e.target.id === 'lightbox') closeLightbox();
});
document.addEventListener('keydown', (e) => {
  if(!document.getElementById('lightbox').classList.contains('show')) return;
  if(e.key === 'Escape') closeLightbox();
  else if(e.key === 'ArrowLeft') navLightbox(-1);
  else if(e.key === 'ArrowRight') navLightbox(1);
});

function showToast(msg){
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2600);
}

function sequenceText(){
  return clips.map((c,i) => `${i+1}. ${c.title}${c.dur ? '  ['+c.dur+']' : ''}${c.note ? '  — '+c.note : ''}`).join('\n');
}

function exportText(){
  const text = sequenceText();
  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(text)
      .then(() => showToast("Copied sequence to clipboard"))
      .catch(() => window.prompt("Copy the sequence:", text));
  } else {
    window.prompt("Copy the sequence:", text);
  }
}

const IMAGE_DURATION_SEC = 3;

function exportConcat(){
  const esc = p => p.replace(/'/g, "'\\''");
  const rows = [];
  clips.forEach((c, i) => {
    rows.push(`file '${esc(c.path)}'`);
    if (c.isImage) rows.push(`duration ${IMAGE_DURATION_SEC}`);
  });
  if (clips.length && clips[clips.length - 1].isImage) {
    rows.push(`file '${esc(clips[clips.length - 1].path)}'`);
  }
  const hasImages = clips.some(c => c.isImage);
  const lines = rows.join('\n') + '\n';
  const blob = new Blob([lines], {type: "text/plain"});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `concat_list_${STORIES[activeIndex].key}.txt`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 5000);
  const cmd = hasImages
    ? `ffmpeg -f concat -safe 0 -i ${a.download} -vsync vfr -pix_fmt yuv420p out.mp4  (re-encode required — sequence mixes stills and video)`
    : `ffmpeg -f concat -safe 0 -i ${a.download} -c copy out.mp4`;
  showToast(`Downloaded ${a.download} \n Run: ` + cmd);
}

function slugifyJs(text){
  return (text || "storyboard").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "") || "storyboard";
}

function buildManifest(title, storyText){
  const lines = [`# ${title}`];
  if (storyText && storyText.trim()) { lines.push(""); lines.push(storyText.trim()); }
  lines.push("");
  clips.forEach((c, i) => {
    const n = String(i + 1).padStart(2, "0");
    lines.push(`## ${n}. ${c.title}`);
    lines.push(`Duration: ${c.dur || "?"}`);
    if (c.description) { lines.push(""); lines.push(`**What's in this shot:** ${c.description}`); }
    if (c.prompt) { lines.push(""); lines.push(`**Generation prompt:** ${c.prompt}`); }
    if (c.note) { lines.push(""); lines.push(`**Feedback:** ${c.note}`); }
    lines.push("");
  });
  return lines.join("\n");
}

function dataUriToBytes(dataUri){
  const binary = atob(dataUri.split(",")[1]);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
  return bytes;
}

let _crc32Table = null;
function crc32(bytes){
  if (!_crc32Table) {
    _crc32Table = new Uint32Array(256);
    for (let n = 0; n < 256; n++) {
      let c = n;
      for (let k = 0; k < 8; k++) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
      _crc32Table[n] = c >>> 0;
    }
  }
  let crc = 0xFFFFFFFF;
  for (let i = 0; i < bytes.length; i++) crc = (crc >>> 8) ^ _crc32Table[(crc ^ bytes[i]) & 0xFF];
  return (crc ^ 0xFFFFFFFF) >>> 0;
}

// Minimal ZIP writer (STORE method, no compression — images are already compressed).
function makeZip(files){
  const encoder = new TextEncoder();
  const localParts = [], centralParts = [];
  let offset = 0;
  const dosTime = 0, dosDate = 0x21;

  files.forEach(f => {
    const nameBytes = encoder.encode(f.name);
    const data = f.data;
    const crc = crc32(data);
    const size = data.length;

    const lh = new Uint8Array(30 + nameBytes.length);
    const lv = new DataView(lh.buffer);
    lv.setUint32(0, 0x04034b50, true);
    lv.setUint16(4, 20, true);
    lv.setUint16(6, 0, true);
    lv.setUint16(8, 0, true);
    lv.setUint16(10, dosTime, true);
    lv.setUint16(12, dosDate, true);
    lv.setUint32(14, crc, true);
    lv.setUint32(18, size, true);
    lv.setUint32(22, size, true);
    lv.setUint16(26, nameBytes.length, true);
    lv.setUint16(28, 0, true);
    lh.set(nameBytes, 30);
    localParts.push(lh, data);

    const ch = new Uint8Array(46 + nameBytes.length);
    const cv = new DataView(ch.buffer);
    cv.setUint32(0, 0x02014b50, true);
    cv.setUint16(4, 20, true);
    cv.setUint16(6, 20, true);
    cv.setUint16(8, 0, true);
    cv.setUint16(10, 0, true);
    cv.setUint16(12, dosTime, true);
    cv.setUint16(14, dosDate, true);
    cv.setUint32(16, crc, true);
    cv.setUint32(20, size, true);
    cv.setUint32(24, size, true);
    cv.setUint16(28, nameBytes.length, true);
    cv.setUint32(42, offset, true);
    ch.set(nameBytes, 46);
    centralParts.push(ch);

    offset += lh.length + data.length;
  });

  const centralSize = centralParts.reduce((s, p) => s + p.length, 0);
  const end = new Uint8Array(22);
  const ev = new DataView(end.buffer);
  ev.setUint32(0, 0x06054b50, true);
  ev.setUint16(8, files.length, true);
  ev.setUint16(10, files.length, true);
  ev.setUint32(12, centralSize, true);
  ev.setUint32(16, offset, true);

  return new Blob([...localParts, ...centralParts, end], {type: "application/zip"});
}

function exportPacket(){
  const title = STORIES[activeIndex].title;
  const storyText = document.getElementById('storyText').value;
  const files = [{name: "manifest.md", data: new TextEncoder().encode(buildManifest(title, storyText))}];
  clips.forEach((c, i) => {
    if (!c.thumb) return;
    const n = String(i + 1).padStart(2, "0");
    const base = slugifyJs(c.title.replace(/\.[^.]+$/, ""));
    files.push({name: `${n}-${base}.jpg`, data: dataUriToBytes(c.thumb)});
  });
  const blob = makeZip(files);
  const name = slugifyJs(title) + "_review_packet.zip";
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = name;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 5000);
  showToast(`Downloaded ${name} \n Drag it into Google Drive for Gemini review`);
}

function exportNotes(){
  const payload = {
    order: clips.map(c => c.id),
    notes: Object.fromEntries(clips.map(c => [c.id, c.note || ""])),
    descriptions: Object.fromEntries(clips.map(c => [c.id, c.description || ""])),
    prompts: Object.fromEntries(clips.map(c => [c.id, c.prompt || ""])),
    storyText: document.getElementById('storyText').value,
    preflight: preflightChecked,
  };
  const name = STORIES[activeIndex].key + ".notes.json";
  const blob = new Blob([JSON.stringify(payload, null, 2)], {type: "application/json"});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = name;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 5000);
  showToast(`Downloaded ${name} \n This combined view doesn't feed notes back into the individual board yet — annotate ${STORIES[activeIndex].title}'s own board (and pass --notes there) to keep them past a re-scan`);
}

function resetBoard(){
  if(confirm(`Clear saved order, descriptions, notes, story text, and the preflight checklist for "${STORIES[activeIndex].title}"? (Other stories are unaffected.)`)){
    localStorage.removeItem(storageKeyFor(activeIndex));
    localStorage.removeItem(storyTextKeyFor(activeIndex));
    localStorage.removeItem(preflightKeyFor(activeIndex));
    document.getElementById('storyText').value = "";
    renderPreflight();
    clips = STORIES[activeIndex].clips.map(c => ({...c}));
    render();
  }
}

document.getElementById('storyTitle').textContent = STORIES[activeIndex].title;
clips = loadOrder(activeIndex);
loadStoryText(activeIndex);
if (localStorage.getItem(preflightOpenKeyFor(activeIndex)) === '1') {
  document.getElementById('preflight').classList.add('open');
}
renderPreflight();
renderTabs();
render();
</script>
</body>
</html>
"""


def parse_board_file(f: Path):
    """Pull title + clips out of one storyboard.py-generated HTML file.
    Reflects order/notes as last saved by build_html, NOT any live unsaved
    edits sitting only in an open browser tab's localStorage. Returns None
    if f isn't a storyboard.py board."""
    if not f.is_file():
        return None
    text = f.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"const SCANNED = (\[.*?\]);\s*\n\s*const STORAGE_KEY", text, re.DOTALL)
    if not m:
        return None
    try:
        clips = json.loads(m.group(1))
    except json.JSONDecodeError:
        return None
    title_m = re.search(r"<title>(.*?)</title>", text)
    title = html.unescape(title_m.group(1)) if title_m else f.stem
    title = re.sub(r"^Clip Storyboard\s*—\s*", "", title)
    default_preflight = {}
    pf_m = re.search(r"const DEFAULT_PREFLIGHT = (\{.*?\});", text)
    if pf_m:
        try:
            default_preflight = json.loads(pf_m.group(1))
        except json.JSONDecodeError:
            pass
    return {"title": title, "name": f.name, "clips": clips, "default_preflight": default_preflight}


def gather_boards(paths, exclude: Path | None = None):
    """Each path may be a folder (every *.html board directly inside it) or
    a specific board HTML file; mix freely. De-dupes, skips non-boards."""
    boards, seen = [], set()
    for raw in paths:
        p = Path(raw).expanduser().resolve()
        candidates = sorted(p.glob("*.html")) if p.is_dir() else [p]
        for f in candidates:
            if exclude is not None and f.resolve() == exclude.resolve():
                continue
            key = str(f.resolve())
            if key in seen:
                continue
            board = parse_board_file(f)
            if board:
                seen.add(key)
                boards.append(board)
    return boards


def build_index(directory: Path, out_path: Path):
    boards = gather_boards([directory], exclude=out_path)

    if not boards:
        rows_html = '<p class="empty">No storyboard.py boards found in this folder yet.</p>'
    else:
        rows_html = "\n".join(
            BOARD_ROW_TEMPLATE
            .replace("__HREF__", html.escape(b["name"]))
            .replace("__TITLE__", html.escape(b["title"]))
            .replace("__FILE__", html.escape(b["name"]))
            .replace("__COUNT__", str(len(b["clips"])))
            for b in boards
        )

    page = INDEX_TEMPLATE
    page = page.replace("__DIR_NAME__", html.escape(directory.name or str(directory)))
    page = page.replace("__DIR_PATH__", html.escape(str(directory)))
    page = page.replace("__BOARD_ROWS__", rows_html)
    out_path.write_text(page, encoding="utf-8")
    return [(b["title"], b["name"], len(b["clips"])) for b in boards]


def slugify(text):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s or "story"


def build_combined_html(boards, combo_key):
    seen = {}
    stories = []
    for b in boards:
        title = Path(b["title"]).name if b["title"].startswith("/") else b["title"]
        base = slugify(title)
        n = seen.get(base, 0)
        seen[base] = n + 1
        key = base if n == 0 else f"{base}-{n + 1}"
        stories.append({"title": title, "key": key, "clips": b["clips"],
                         "defaultPreflight": b.get("default_preflight", {})})

    page = COMBINE_TEMPLATE
    page = page.replace("__STORIES_JSON__", json.dumps(stories))
    page = page.replace("__COMBO_KEY__", json.dumps(combo_key))
    page = page.replace("__TITLE__", html.escape(f"{len(stories)} stories"))
    return page


def main():
    ap = argparse.ArgumentParser(
        description="Generate a storyboard HTML page from folders and/or individual video/image files.")
    ap.add_argument("paths", nargs="*", metavar="PATH",
                    help="folder (scanned recursively) or a single video/image file; mix freely")
    ap.add_argument("-o", "--output",
                    help="output HTML path (default: storyboard.html in the first folder given, "
                         "or next to the first file)")
    ap.add_argument("--notes", metavar="FILE",
                    help="load a <board>.notes.json previously saved from this board's own "
                         "'Save notes (.json)' button, and bake its order/descriptions/notes/"
                         "prompts/preflight/story-text into this run instead of leaving them to "
                         "the browser's localStorage. Auto-detected next to the output path "
                         "(<output-stem>.notes.json) when this flag is omitted.")
    ap.add_argument("--index", metavar="DIR", nargs="?", const=".",
                    help="instead of scanning for clips, build an index.html linking every "
                         "storyboard.py board found in DIR (default: current directory)")
    ap.add_argument("--combine", action="store_true",
                    help="merge multiple storyboard.py boards into ONE page with a tab bar — "
                         "each becomes an independent 'story' with its own order/notes/export. "
                         "Pass specific board HTML files as PATH to combine exactly those; "
                         "with no PATH, every board directly inside the current directory "
                         "is combined")
    args = ap.parse_args()

    if args.index is not None:
        directory = Path(args.index).expanduser().resolve()
        if not directory.is_dir():
            sys.exit(f"error: not a folder: {directory}")
        out = Path(args.output).expanduser().resolve() if args.output else directory / "index.html"
        boards = build_index(directory, out)
        print(f"Found {len(boards)} board(s):")
        for title, name, count in boards:
            print(f"  {name}  ({count} clips)  — {title}")
        print(f"\nWrote {out}")
        print(f"Open it:  open '{out}'")
        return

    if args.combine:
        targets = args.paths if args.paths else ["."]
        out = Path(args.output).expanduser().resolve() if args.output else Path.cwd() / "storyboard_combined.html"
        boards = gather_boards(targets, exclude=out)
        if not boards:
            sys.exit("No storyboard.py boards found among the given path(s).")
        out.write_text(build_combined_html(boards, str(out)), encoding="utf-8")
        print(f"Combined {len(boards)} stor{'y' if len(boards) == 1 else 'ies'}:")
        for b in boards:
            print(f"  {b['title']}  ({len(b['clips'])} clips)")
        print(f"\nWrote {out}")
        print(f"Open it:  open '{out}'")
        return

    if not args.paths:
        ap.error("PATH is required unless --index or --combine is given")

    for tool in ("ffprobe", "ffmpeg"):
        try:
            subprocess.run([tool, "-version"], capture_output=True, check=False)
        except FileNotFoundError:
            sys.exit(f"error: {tool} not found on PATH")

    print(f"Scanning {len(args.paths)} path(s) …")
    clips = collect_clips(args.paths)
    if not clips:
        sys.exit("No video/image files found (looked for: " + ", ".join(sorted(MEDIA_EXTS)) + ")")

    first = Path(args.paths[0]).expanduser().resolve()
    if args.output:
        out = Path(args.output).expanduser().resolve()
    else:
        out = (first if first.is_dir() else first.parent) / "storyboard.html"

    if args.notes:
        sidecar_path = Path(args.notes).expanduser().resolve()
        if not sidecar_path.is_file():
            sys.exit(f"error: --notes file not found: {sidecar_path}")
    else:
        sidecar_path = out.parent / (out.stem + ".notes.json")

    default_preflight = None
    default_story_text = None
    if sidecar_path.is_file():
        sidecar = load_notes_sidecar(sidecar_path)
        if sidecar:
            clips = apply_notes_sidecar(clips, sidecar)
            default_preflight = sidecar.get("preflight") or None
            default_story_text = sidecar.get("storyText") or None
            print(f"Applied saved notes from {sidecar_path.name}")

    print(f"\nSequence ({len(clips)} clips, in the order found — this is the board's starting order):")
    for i, c in enumerate(clips, 1):
        note = "  ·  has note" if c.get("note") else ""
        print(f"  {i:>2}. {c['title']}  [{c['dur']}]{note}")

    label = str(first) if len(args.paths) == 1 else f"{len(args.paths)} sources · {first}, …"
    out.write_text(build_html(label, str(out), clips, default_preflight=default_preflight,
                               default_story_text=default_story_text), encoding="utf-8")
    print(f"\nWrote {out}  ({len(clips)} clips)")
    print(f"Open it:  open '{out}'")


if __name__ == "__main__":
    main()
