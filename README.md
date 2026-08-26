# storyboard-review

Generate a drag-and-drop HTML storyboard for reviewing and reordering video
clips and still images — no server, no database, no Python dependencies.

Point it at one or more folders (scanned recursively) or individual
video/image files, and it writes a single self-contained HTML page:

- each item is a film-strip row — thumbnail, sequence number, filename,
  duration/`IMG` tag, and an editable note ("what's wrong with this shot")
- rows are drag-and-drop reorderable
- order + notes persist in the browser's `localStorage`, so re-running the
  script keeps your ordering and comments for items that still exist
- "Save notes (.json)" downloads a small sidecar file (order + notes +
  descriptions + prompts + story text). Put it next to the board's HTML and
  the next run bakes it straight into the page, so notes survive a cleared
  browser profile or opening the board somewhere else
- "Download ffmpeg concat file" exports the current order in
  concat-demuxer format, ready for
  `ffmpeg -f concat -safe 0 -i concat_list.txt -c copy stitched.mp4`

## Requirements

- Python 3.9+
- `ffmpeg` and `ffprobe` on `PATH` (used to extract clip durations and
  thumbnails)

No pip dependencies are required for the core tool.

## Install

```bash
pipx install .
```

or, for local development:

```bash
pip install -e .
```

Both give you a `storyboard` command. You can also run it directly with
`python3 storyboard.py` without installing anything.

## Usage

```bash
# One folder
storyboard ~/shoot1 -o review.html

# Mix folders and individual files, from anywhere on disk
storyboard ~/shoot1 ~/shoot2/clip7.mov "/Volumes/SSD/proof_frames"

# Build an index.html linking every board found in a directory
storyboard --index [DIR]

# Merge multiple boards into one page with a tab bar, each keeping its own
# independent order/notes/export
storyboard --combine [DIR]
```

Run `storyboard --help` for the full option list.

## Development

```bash
pip install -e ".[dev]"
pre-commit install   # one-time: runs ruff + mypy on every commit
ruff check .
mypy
pytest -q
```

The test suite covers the pure logic (scanning, sidecar merging, HTML/board
round-tripping) without needing `ffmpeg`. One additional test exercises real
thumbnail/duration extraction and is skipped automatically if `ffmpeg`/
`ffprobe` aren't on `PATH`. The clip objects passed between functions are
typed as a `Clip` TypedDict and checked with `mypy`. CI
([.github/workflows/ci.yml](.github/workflows/ci.yml)) runs lint, type
checking, and tests across macOS, Linux, and Windows on Python 3.9 and 3.12.

`storyline.py` isn't part of this package yet, so it's deliberately left out
of the lint/type-check/pre-commit scope above.

## License

MIT — see [LICENSE](LICENSE).
