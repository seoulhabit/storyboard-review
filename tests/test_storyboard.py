import json
import re
import shutil
import subprocess

import pytest

import storyboard as sb

# ---- pure helpers -----------------------------------------------------

def test_fmt_duration():
    assert sb.fmt_duration(None) == "?"
    assert sb.fmt_duration(5.4) == "0:05"
    assert sb.fmt_duration(65) == "1:05"
    assert sb.fmt_duration(3661) == "1:01:01"


def test_is_video_image_media(tmp_path):
    vid = tmp_path / "clip.mp4"
    img = tmp_path / "still.png"
    other = tmp_path / "notes.txt"
    hidden = tmp_path / ".hidden.mp4"
    for p in (vid, img, other, hidden):
        p.write_bytes(b"")

    assert sb.is_video(vid) and not sb.is_image(vid)
    assert sb.is_image(img) and not sb.is_video(img)
    assert not sb.is_media(other)
    assert not sb.is_media(hidden)  # dotfiles excluded even with a media extension
    assert sb.is_media(vid) and sb.is_media(img)


def test_gather_files_recurses_dedupes_and_skips_non_media(tmp_path):
    sub = tmp_path / "sub"
    sub.mkdir()
    a = tmp_path / "a.mp4"
    b = sub / "b.jpg"
    junk = tmp_path / "readme.txt"
    for p in (a, b, junk):
        p.write_bytes(b"")

    # same folder passed twice, plus one of its files passed directly — still de-duped
    files = sb.gather_files([str(tmp_path), str(tmp_path), str(a)])
    assert sorted(f.name for f in files) == ["a.mp4", "b.jpg"]


def test_gather_files_missing_path_exits():
    with pytest.raises(SystemExit):
        sb.gather_files(["/no/such/path/at/all"])


# ---- notes sidecar ------------------------------------------------------

def test_load_notes_sidecar_valid(tmp_path):
    p = tmp_path / "board.notes.json"
    p.write_text(json.dumps({"order": ["x"], "notes": {"x": "hi"}}))
    data = sb.load_notes_sidecar(p)
    assert data["notes"]["x"] == "hi"


def test_load_notes_sidecar_bad_json_returns_none(tmp_path):
    p = tmp_path / "board.notes.json"
    p.write_text("{not json")
    assert sb.load_notes_sidecar(p) is None


def test_load_notes_sidecar_non_object_returns_none(tmp_path):
    p = tmp_path / "board.notes.json"
    p.write_text(json.dumps([1, 2, 3]))
    assert sb.load_notes_sidecar(p) is None


def test_apply_notes_sidecar_reorders_annotates_and_appends_new():
    clips = [
        {"id": "1", "title": "one"},
        {"id": "2", "title": "two"},
        {"id": "3", "title": "three"},  # not present in the sidecar's order
    ]
    sidecar = {"order": ["2", "1"], "notes": {"1": "redo this"}, "descriptions": {}, "prompts": {}}
    merged = sb.apply_notes_sidecar(clips, sidecar)
    assert [c["id"] for c in merged] == ["2", "1", "3"]
    assert merged[1]["note"] == "redo this"
    assert merged[2]["note"] == ""  # new item gets blank annotations, not dropped


# ---- html generation / board round-trip ----------------------------------

def make_clip(i, note=""):
    return {"id": f"/clips/{i}.mp4", "title": f"{i}.mp4", "path": f"/clips/{i}.mp4",
            "note": note, "description": "", "prompt": "", "dur": "0:05", "durSec": 5,
            "isImage": False, "thumb": None}


def test_build_html_round_trips_through_parse_board_file(tmp_path):
    clips = [make_clip(1), make_clip(2, note="reshoot")]
    page = sb.build_html("2 sources · /clips", "/out/board.html", clips)
    out = tmp_path / "board.html"
    out.write_text(page, encoding="utf-8")

    parsed = sb.parse_board_file(out)
    assert parsed is not None
    assert len(parsed["clips"]) == 2
    assert parsed["clips"][1]["note"] == "reshoot"


def test_parse_board_file_rejects_unrelated_html(tmp_path):
    p = tmp_path / "page.html"
    p.write_text("<html><body>not a board</body></html>")
    assert sb.parse_board_file(p) is None


def test_slugify():
    assert sb.slugify("Depth of Action v2!") == "depth-of-action-v2"
    assert sb.slugify("") == "story"


def test_gather_boards_and_build_index(tmp_path):
    for i, title in enumerate(["Alpha", "Beta"], 1):
        page = sb.build_html(title, f"/out/{title}.html", [make_clip(i)])
        (tmp_path / f"board{i}.html").write_text(page, encoding="utf-8")

    out = tmp_path / "index.html"
    summary = sb.build_index(tmp_path, out)
    assert out.exists()
    assert sorted(name for _, name, _ in summary) == ["board1.html", "board2.html"]


def test_build_combined_html_dedupes_slugs_for_same_title():
    boards = [
        {"title": "Alpha", "clips": [make_clip(1)], "default_preflight": {}},
        {"title": "Alpha", "clips": [make_clip(2)], "default_preflight": {}},
    ]
    page = sb.build_combined_html(boards, "combo")
    m = re.search(r"const STORIES = (\[.*?\]);", page, re.DOTALL)
    stories = json.loads(m.group(1))
    assert [s["key"] for s in stories] == ["alpha", "alpha-2"]


# ---- real ffmpeg, only when available ------------------------------------

HAS_FFMPEG = shutil.which("ffmpeg") and shutil.which("ffprobe")


@pytest.mark.skipif(not HAS_FFMPEG, reason="ffmpeg/ffprobe not on PATH")
def test_probe_duration_and_thumbnail_against_a_real_clip(tmp_path):
    clip = tmp_path / "tiny.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "lavfi",
         "-i", "testsrc=duration=2:size=64x64:rate=10", str(clip)],
        check=True,
    )
    duration = sb.probe_duration(clip)
    assert duration is not None and 1.5 < duration < 2.5

    thumb = sb.extract_video_thumb(clip, duration)
    assert thumb and thumb.startswith("data:image/jpeg;base64,")
