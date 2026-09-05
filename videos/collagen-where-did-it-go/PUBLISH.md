# Publish envelope — paste-ready

> Chapters below are **regenerated from `STORYBOARD.md`** on every build, which
> parses the real `data-start` values. Re-paste them after the final build; a
> chapter list is the one deliverable nothing in the render pipeline validates.

Run `python3 scripts/check-publish.py .` before working through this envelope
-- it verifies every deliverable this file assumes exists (the render, both
caption formats, the accessible transcript, this file itself) actually does,
and hard-fails if there is no verified caption track. It does not re-verify
the render itself; `npm run gates` is the authority on that.

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

**Accessibility addition (this session):** also link the accessible transcript
(`TRANSCRIPT.md` / a hosted copy of `TRANSCRIPT.html`) in the description for
viewers using a screen reader or reading rather than watching — it carries the
visual-only facts (the size and trial-count comparisons, the ranked-
recommendation order) a caption track alone does not. The description already
carries the trial-tag caveat implicitly via "the tiles you see drop out are a
pattern, not a count" in the pinned comment below; consider pulling that line
up into the description itself so it is visible without opening comments.

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

---

## Accessibility & destination checklist (this session's addition)

### Before publishing anywhere: the channel-fit caveat

**This channel's own baseline (`videos/_channel/baseline.yaml`,
`baseline-notes.md`) has no public long-form video at all** -- of 48 uploads,
46 are Shorts and the only 2 long-form pieces are both private with no
distribution signal. 88.1% of all channel views come from the Shorts feed.
This project is a 1920x1080 landscape, 2:23 long-form video: a format this
specific channel has never actually published publicly. That is not a defect
in this video -- the accessibility review this delivery is built around
applies regardless of format -- but it means there is no channel-specific
data to predict how a long-form upload performs here, and publishing it is a
genuine first, not a repeat of a proven pattern. Worth the operator's own
call before scheduling a publish, not something this checklist can decide.

### YouTube (long-form) -- the fit this video was built for

The only destination this video's own 16:9 landscape aspect ratio and 2:23
runtime suit without a re-edit.

- [ ] Upload `renders/collagen-where-did-it-go_final.mp4`.
- [ ] Upload `captions/collagen-where-did-it-go.srt` as a caption track (not
      "auto-generated" -- a real track, reviewed this session for reading
      speed and hygiene). Set the track language and confirm it is set as
      the DEFAULT track, not merely available.
- [ ] After upload, turn captions ON in the actual player and screenshot one
      frame from each third of the video (early/mid/late) to confirm the
      platform's own caption rendering does not collide with on-screen text
      -- `scripts/check-caption-overlay.py`'s 240px simulated band is a
      pre-upload estimate, not a substitute for looking at the real player.
      This step needs the channel account and cannot be automated here.
- [ ] Description and pinned comment above, plus the transcript link noted
      under Description.

### Shorts / TikTok / Instagram Reels -- not this render

This video is landscape 16:9 at 2:23. None of the vertical-first platforms
are a fit without a genuine re-edit (a vertical reframe, and very likely a
much shorter cut) -- pushing this exact file to a vertical placement would
letterbox or crop content out of the safe area this review spent real effort
getting right. Not attempted as part of this delivery; flag to the operator
as a possible SEPARATE project if a Shorts-native cut of this material is
wanted, given the channel's own baseline shows that is where its actual
audience is.

### Open-caption variant

If a destination or repost context cannot guarantee the sidecar caption
track survives (a platform that strips SRT/VTT on repost, a downstream
embed), `renders/collagen-where-did-it-go_open-captions.mp4` has captions
burned into the frame, in the reserved caption band
`scripts/check-caption-overlay.py` verifies. This is a fallback for exactly
that failure mode, not a replacement for the sidecar track: a real caption
track can be turned off, resized, or read by a screen reader in ways a
burned-in one cannot. It also has known, reviewed overlaps with a small
number of on-screen callouts (`check-caption-overlay.py`'s own advisory
findings on the clean master predict exactly where) -- built and kept as a
working fallback, not polished to be collision-free, since the sidecar
track above is the primary deliverable.
