# Publish envelope — paste-ready

> Chapters below are **regenerated from `STORYBOARD.md`** on every build, which
> parses the real `data-start` values. Re-paste them after the final build; a
> chapter list is the one deliverable nothing in the render pipeline validates.

## Title

**You Bought Collagen. Where Did It Actually Go?**

Alternates, if the primary underperforms:
- Collagen Cream, Collagen Powder, and What the 2025 Evidence Actually Says
- Your Skin Is a Building. Collagen Is the Scaffolding.

> Note: this channel's title scorer is recorded as **not discriminative** on its
> own videos (it ranked a failing title above every rewrite, 3 videos / 3 runs),
> so a score is worth logging and not worth obeying. These are chosen on the
> curiosity gap the script itself opens, not on a number.

## Thumbnail

**Upload:** `assets/thumbnail/thumbnail-final.png` — 1280×720, 185 KB, RGB with no alpha channel.

The climax frame at 101.60s: **THE EFFECT / STOPS / SHOWING UP** in 132px black
caps on the paper flood, against the ink ground, with `NOT SIGNIFICANT` and the
meter beside it and the `Am J Med · 2025` chip bottom-right.

**It answers the title rather than repeating it.** The title asks where the
collagen went; the thumbnail states what the evidence found. The two sit side by
side in every surface, so a thumbnail that restates the question spends its one
frame on something the viewer has already read — that rule picked this frame over
four alternatives, all of which are kept in `assets/thumbnail/` with the
reasoning in its README.

**Chosen at 120×67, not at full size.** At 256×144 four of the five candidates
still read. At the size a thumbnail is actually browsed at, only this one does —
everything else collapses into colour blocks. `feed-check-contact.png` and
`grid-check-contact.png` are the two contact sheets the call was made on.

**Do not re-cut the frame by hand.** The timestamp is pinned inside a 0.8s window
(101.15–101.95): before 101.10 the word "UP" is still grey mid-transition, and
from 101.95 the word "works?" fades in underneath. Regenerate with
`python3 scripts/make-thumbnail.py`, which writes `thumbnail-final.png` from the
`WINNER` constant so the uploaded file cannot drift from the decision.

**A/B alternate, if it underperforms:** `candidate-c-rejected-1280.png` — the
REJECTED stamp over the coral barrier. It is the only other candidate that holds
a readable word at feed scale, though both size numbers are lost there.

## Description

```
Collagen is the structure holding your skin up. So what happens to the collagen
you buy — the cream, and the powder?

Short version: the cream is too big a molecule to get in, your stomach doesn't do
facial delivery, and when a 2025 review kept only the independent, higher-quality
trials, the benefit stopped showing up.

This is not "collagen is a scam." It's a question of how it reaches you, and what
the evidence survives.

0:00 Where does it actually go?
0:14 Your skin is a building
0:38 Why the cream can't get in
0:56 Your stomach doesn't do facial delivery
1:17 The evidence plot twist
1:49 What actually protects it

SOURCES
• Fisher GJ, Voorhees JJ. J Investig Dermatol Symp Proc. 1998;3(1):61-8. PMID 9732061
• Bos JD, Meinardi MMHM. The 500 Dalton rule. Exp Dermatol. 2000;9(3):165-9.
  doi:10.1034/j.1600-0625.2000.009003165.x
• Pu S-Y et al. Nutrients. 2023;15(9):2080. doi:10.3390/nu15092080
• Myung S-K, Park Y. Am J Med. 2025;138(9):1264-1277. doi:10.1016/j.amjmed.2025.04.034
• Morita A. J Dermatol Sci. 2007;48(3):169-75. doi:10.1016/j.jdermsci.2007.06.015
• Kafi R et al. Arch Dermatol. 2007;143(5):606-12. doi:10.1001/archderm.143.5.606

Educational content, not medical advice. Talk to a dermatologist about your own skin.

SeoulHabit — evidence, not hype.
```

## Pinned comment

```
The line that surprised me most while making this: the 2025 review (Myung & Park,
Am J Med) DID find collagen supplements improved hydration, elasticity and
wrinkles across all 23 trials. The effect only disappeared once you separated the
industry-funded and lower-quality studies from the rest.

That's not the same as "it doesn't work." It's "we don't have clean evidence that
it does." Which is a genuinely different, and more annoying, answer.

One thing the video shows but doesn't say out loud: the paper reports the
subgroup RESULTS, not how many trials fell in each subgroup. The tiles you see
drop out are a pattern, not a count — which is why they carry a label saying so.

What would you want us to run this same treatment on next?
```

## End screen

The closing scene (`16-end`) holds for 5.0s with the right third (640px) and the
lower-right (200px) kept clear by the `--endscreen-right` / `--endscreen-bottom`
tokens, and its only motion is a single slow settle — so the overlay elements
land on a clear, calm frame. `scripts/check-endscreen.py` measures that on the
rendered pixels rather than trusting the tokens.

The `curtain` transition into it wipes LEFT, revealing the empty right third
first: the reserve is clear before the card has finished arriving.

- **Next video:** the strongest related piece in the catalog is
  `videos/retinal-clinical-dossier` — the hierarchy's fourth row names retinoids,
  so the handoff is content-led rather than arbitrary.
- **Subscribe element:** lower-left of the reserved band.
