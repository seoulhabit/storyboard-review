# QuestionGate

An ordered checklist of **independent questions a viewer applies in sequence** —
N numbered cards, each activating in turn as its question is asked, with an
optional second sub-beat inside a card when the narration splits that question
into two clauses. Answered cards step back; the live one reads first.

## Why this one, and why now

Harvested from `videos/exosome-label-decode/compositions/frames/04-questions.html`
("What is the source? / Proven to be what it says? / Tested on people — as
sold?" — the three questions to ask before buying an exosome serum).

A discovery pass across every existing `catalog/visual-components/` entry
before that scene was built found **nothing matching this shape**, and one
near-miss worth recording so the next build doesn't repeat the comparison:

| Considered | Why it doesn't fit |
|---|---|
| `FactorConverge` | A **many-to-one** causal diagram — 3 inputs converging on 1 outcome, fixed triangle geometry. These questions converge on nothing; they are independent gates applied in order. |
| `ThresholdList` | A ranked list split by a **cutoff**. There is no ranking here and no cutoff — failing question 2 doesn't reorder anything. |
| `SplitCompare` | A **two-thing** bisector. Three, and they aren't being compared to each other. |
| `TermDefinition` | A single-term hero card, no sequence and no state. |

The distinguishing property is **per-item activation state over time**: the
component's job is to show *which question is being asked right now* while
keeping the others legible as context. None of the entries above carries a
state axis at all.

## Field contract

```js
{
  kicker:   "Before you buy",
  headline: "Ask three questions.",
  gates: [
    { idx: "01", q: "What is the source?",
      subs: ["The label should name the cell."] },
    { idx: "02", q: "Proven to be what it says?",
      subs: ["Characterized — measured, not assumed.",
             "Still stable when it reaches you."] },   // 2 subs = 2 sub-beats
    { idx: "03", q: "Tested on people — as sold?",
      subs: ["This exact finished product.", "Not just the ingredient."] }
  ],
  citation: "Cureus · 2026"        // human-readable only, never an internal id
}
```

**N is not fixed** (unlike `FactorConverge`'s hard 3): the cards are a flex
column of content-sized items, so 2–4 work without geometry changes. Past ~4
the column stops fitting a 9:16 safe box at the type floor — that is a real
limit, not a styling preference.

**1 or 2 subs per gate.** The second sub exists to absorb a narration clause
split; see *The motion* below for why that matters more than it sounds.

## The motion, and why it's shaped this way

- **All gates are COMPOSED at t=0; the stagger rides on the card text**
  (0.25 / 0.75 / 1.25, brightening `idx` + `q` from 0.32 to 1). The viewer sees
  the whole checklist before any of it is answered — that is the promise the
  scene is making, and it has to be legible from frame one. An earlier version
  faded the *cards* in at 0.35/0.62/0.89 instead, which left the cut into this
  scene landing on 13,714 ink px — the headline alone — because the cards carry
  most of the frame's ink. Measured on a render, not inferred; composing them
  took that cut frame to 51,357.
- **Activation is a left bar scaling from the top** (`scaleY` on a 8px celadon
  rule), not a colour wash. State lives in one narrow element so the card's own
  text never changes contrast mid-scene.
- **Answered gates step back via their border only** (`#333` → `#2A2E2F`). No
  success colour: an answered gate must not read as "passed", because the whole
  point is that the viewer, not the video, supplies the answer.
- **Sub-beats absorb clause splits.** This is the non-obvious part. Activation
  times are derived from *measured* sentence boundaries in the narration
  (`ffmpeg silencedetect`), and real narration rarely spaces N questions evenly.
  In the source video, gates 1→2 were 1.3s apart but 2→3 were **3.9s** apart —
  over the 2.5s cadence ceiling, i.e. a visible dead hold. Splitting gates 2
  and 3 into two sub-beats each (one per narration clause) filled that stretch
  with real content instead of decorative motion. Build the sub list from where
  the voice actually breaks, not from an even split.

## Render safety

Paused, seek-safe GSAP; no autoplay, no wall-clock. Every activation bar has its
`t=0` state registered as a real timeline tween (`tl.set(bar, {scaleY: 0}, 0)`),
not a bare `gsap.set()` — each bar is targeted by more than one tween, and the
engine seeks to arbitrary times without passing through 0, so an unregistered
baseline can render at its first tween's "from" value for the whole stretch
before its scheduled beat.

## Layout notes worth inheriting

- Cards are `flex: 0 0 auto` (**content-sized**), with `justify-content:
  space-between` on the column distributing slack. An earlier `flex: 1 1 0`
  forced equal shares; once a caption lane shortened the column, content grew
  taller than its card and spilled out *both* ends under `align-content:
  center` — measured at 74px of overflow above the card's own top edge.
- The scene needs `h1, h2, h3, p { margin: 0 }`, not just a `box-sizing` reset.
  UA default margins scale with font size, so a 42px card question carries ~42px
  of phantom margin; that alone rendered cards at 280–393px against ~194px of
  real content.

## Files

- **`questiongate-spike.html`** — the standalone component, matching this
  catalog's convention: 1080×1920, data-driven from a `DATA` object at the top
  of the script, a paused GSAP timeline scrubbed by one `t`, and a debug
  scrubber behind `?debug=1`. Content is **generalized sample content**, not the
  source video's copy — swapping `DATA` is the whole interface.

## Status

**Validated reference, and wired into a real render.** The mechanism shipped
inside `videos/exosome-label-decode` and was verified post-render there
(safe-area scan clean over 223 frames, static-hold clean whole-frame and
region-aware, cadence 43% active with a 1.88s worst-case hold). The spike here
was then measured in a browser on its own: stage height 1920px with
`getBoundingClientRect()` matching `getComputedStyle()` (no box-sizing defect),
last card bottom at y=1453 and citation right edge at x=382 — both inside the
safe box — and seek-safety confirmed by jumping out of order
(7.2 → 0.5 → 11.2 → 4.0 → 9.0 → 0) with no element bleeding through before its
scheduled beat.

The activation times in the spike are **evenly spaced for demo convenience**.
In a real build they come from measured narration boundaries — see *The motion*
above for why that distinction matters more than it sounds.
