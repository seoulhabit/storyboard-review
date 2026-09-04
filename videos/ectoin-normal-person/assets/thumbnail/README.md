# Thumbnail

**Shipped file: `final.png`** (1280x720). Source: `cand-a.html`, captured via
Playwright chromium at the exact 1280x720 viewport (no device scale factor),
matching the renderer's own approach of a real headless-Chrome capture rather
than a scaled screenshot.

**Rebuilt this revision (2026-09-03).** The prior candidate hard-coded the
retired hook line ("Invented by bacteria trying not to die"), which no longer
opens the video. Recomposed around the new hook: the bottle prop (the same
one that opens and bookends the video) large on the right, "Does 11% mean 11%
ectoin?" as the headline, "TURN IT AROUND" as the payoff chip. Same tokens,
same type roles as before — only the words and the visual anchor changed.

**Authored, not extracted.** Frame 0 of the actual render (the bottle close-up)
reads fine at full size but is a single centred object with a lot of empty
canvas around it, which wastes the crop that actually gets browsed at
120x67. This composition splits the frame between the headline (left) and
the bottle (right) so both survive the downscale.

**Grid-size proof:** `grid-check.png` is `final.png` at 120x67, the size a
thumbnail is actually browsed at; `grid-check-magnified.png` is that same
downscale blown back up with nearest-neighbour so the degradation is visible
without squinting.

**Contrast, measured (`scripts/contrast.py` method):**

    16.81:1  headline #F7F5F0 on ink #131516
     7.76:1  eyebrow  #59B8AE on ink #131516
     8.24:1  chip     #131516 text on #E0A32B
    16.81:1  bottle "11%" #131516 on paper #F7F5F0
     6.69:1  bottle nm2/illustrative-label #5A5650 on paper #F7F5F0

**No grade was ported.** Built on the project's own tokens, not graded toward
another piece's look.

**Not done:** `vidiq_score_thumbnail` / `vidiq_similar_thumbnails` were not
run this revision — S3 (packaging) was skipped per the revision's mode
(subject/seed unchanged; only the thumbnail needed rebuilding since its hook
line was retired). Score title and thumbnail together before publish.
