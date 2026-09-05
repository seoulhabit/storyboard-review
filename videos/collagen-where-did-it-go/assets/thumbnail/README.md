# Thumbnail

**Shipped:** `thumbnail-final.png` (1280×720), written by
`scripts/make-thumbnail.py` from `candidate-d-effect-stops-1280.png`.

Extract-grade-finalize, the house path: the composition already puts a hero
object and a single strong statement in one frame, so no separate asset was
authored.

Re-chosen for the **2:14.90 single-narrator cut**. The previous winner was a
frame at t=2.60s of the 3:09 two-voice cut, on a cold open this build does not
have.

| Candidate | Frame | What it argues |
|---|---|---|
| `a-not-replace` | 4.60s | The contradiction: cream and powder beside a molecule that does NOT replace. |
| `b-uv-cuts` | 29.00s | The cause, in the only black-on-yellow block in the piece. |
| `c-rejected` | 47.80s | The refusal — REJECTED over a coral barrier, both size numbers. |
| `d-effect-stops` | 101.60s | The verdict, in the largest type in the video. **Chosen.** |
| `e-protect` | 128.60s | The payoff: the ranked list under "Protect the building first." |

## Why D

**Judged at 120×67, which is the size a thumbnail is actually browsed at**, and
cross-checked at 256×144. Both contact sheets are in this folder.

At 256×144, four of the five still read. At 120×67 only one does. That is the
whole decision, and it is why the feed-scale sheet exists:

- **D is the only candidate whose text survives 120×67.** Three lines of 132px
  black caps on a paper flood, against the ink ground — the highest-contrast
  pairing in the piece, and the largest type in the video. Everything else
  collapses into colour blocks.
- **C** (the previous cut's winner) holds its shape — REJECTED is still legible
  as a word, and the coral barrier is a strong block — but both size numbers are
  gone, so the frame argues "rejected" without saying what was rejected.
- **B** keeps its yellow-and-black colour story, but the claim inside the black
  card turns to mush, and a card you can see but not read is worse than no card.
- **A** and **E** lose their text entirely. E additionally spends its frame on a
  four-item list, which is four things to read at a size that permits one.

**It answers the title instead of repeating it.** The title is *"You Bought
Collagen. Where Did It Actually Go?"*, which sits next to the thumbnail
everywhere the thumbnail appears. A frame restating the question spends itself on
something the viewer has already read; D states the finding the question leads
to. Every candidate here was chosen on that rule.

**On the ink ground.** The previous README rejected its own dark-ground
candidate because "the numeral and the tile field both fall below legibility at
grid size". That reasoning was about a numeral and a 23-tile field, not about a
white flood — inverted, a dark ground is what makes D the *most* legible frame
in the set rather than the least.

## The timestamp is pinned inside a 0.8s window

101.60s is not a round number by accident. The window is **101.15–101.95**:

- before **101.10** the kinetic word "UP" is still grey, mid-transition, and a
  half-set word reads as a rendering fault in a still;
- from **101.95** the word "works?" fades in underneath the headline.

Both bounds were measured off the render, not eyeballed. Outside that window the
frame carries a visible defect — the first attempt at this shipped a grey "UP"
before the luma was checked.

## Grade

Unchanged and deliberately light: `eq=contrast=1.06:saturation=1.10` plus a
small unsharp. **No vignette** — a prior video's vignette-and-curve chain reads
as a muddy cast on this palette. D sits on the ink ground rather than the ivory
one, and the same light grade holds there; the flood is already near-white and a
heavier hand clips it.

**Caption-free by construction** — this project burns in no caption track, so no
candidate could contain one.

Regenerate with `python3 scripts/make-thumbnail.py`. It writes
`thumbnail-final.png` itself from the `WINNER` constant, so the shipped file
cannot drift from the decision recorded here.
