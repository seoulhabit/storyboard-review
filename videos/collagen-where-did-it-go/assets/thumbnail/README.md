# Thumbnail

**Shipped:** `thumbnail-final.png` (1280×720, a copy of `candidate-b-rejected-1280.png`).

Extract-grade-finalize, the house path: the composition already puts a hero
object and a single strong word in one frame, so no separate asset was authored.

| Candidate | Frame | Why it was tested |
|---|---|---|
| `a-cold-open` | t=2.60s | The title question, literally — the oversized molecule at a door too small for it. |
| `b-rejected` | t=52.35s | The strongest single claim: REJECTED, with both size numbers. **Chosen.** |
| `c-four-left` | t=126.95s | The evidence payoff on the inverted ground, 23 → 4. |

**Why B.** Judged at 256×144 and again at 120×67, not at full size.

- **A** is legible — its headline is the largest type in the video — but it
  *repeats the title*, which sits next to the thumbnail in every surface where
  the thumbnail appears, and it does it in flat warm ivory with no colour to
  hold a feed. A thumbnail that restates the title spends its one frame saying
  something the viewer has already read.
- **C** is the best beat in the video and the worst thumbnail: on the ink ground
  the numeral and the tile field both fall below legibility at grid size.
- **B** carries one legible word (REJECTED) plus the only high-contrast colour
  pair in the piece — the teal ~500 block against the coral ~300,000 block. That
  is a story at a glance without any text needing to be read, which is what the
  scale actually allows.

**Caption-free by construction** — this project burns in no caption track at
all, so no candidate could contain one.

**Grade.** Re-derived for this video's own palette, deliberately light:
`eq=contrast=1.06:saturation=1.10` plus a small unsharp. **No vignette** — the
ground is flat warm ivory by design and a prior video's vignette-and-curve chain
reads as a muddy cast on it. Scene 04's ink ground would take a different grade
again, which is one more reason not to ship C.

Regenerate with `python3 scripts/make-thumbnail.py`.
