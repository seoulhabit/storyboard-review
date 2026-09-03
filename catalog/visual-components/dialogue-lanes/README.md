# DialogueLanes — two-speaker dialogue, faceless

A conversation between two named speakers, rendered without avatars, portraits
or any depiction of a person. Speaker identity is carried by **which lane the
card lands in**, plus a colour, a weight and a distinct entrance — nothing else.

- **Duration** 12.0s in the spike (6 turns). Real length is the sum of the VO
  takes; the component is duration-agnostic.
- **Control** clock — a paused GSAP timeline scrubbed by a single `t`.
- **Scrubber** `debug` — append `?debug=1`.
- **Status** wired into a real render pipeline
  (`videos/collagen-where-did-it-go`, 41 turns across 5 scenes).

## Why this exists

A two-character dialogue had no treatment anywhere in this repo — no character
sheet, no speaker-attribution component, no prior video with named speakers, and
one standing VO voice. The channel is faceless *by rule*, so the obvious answers
(a portrait, an avatar chip) were all out. What was needed was a way to make two
speakers legible from typography alone.

Extracted rather than left in one video's folder because the same repo has
already independently rebuilt one card component **five** times for want of
exactly this step.

## Field contract

```js
LINES = [
  { who: "a" | "b",     // which lane
    name: "SoulHabit",  // lane label, uppercase mono
    text: "…",          // may contain <em> for the word the beat turns on
    at:   4.20 }        // seconds; normally derived from the VO take, not typed
]
```

Swap the array. Nothing else is content-specific.

## The three things that make it work

**1. A lane is a PANEL, not a line of type.** On a 1920-wide frame a headline
sits inside a grid cell, so animating text changes ~0.7% of the pixels — below
what a frame-difference cadence check can see, and close to what a viewer can.
The source project measured 5.8% active steps with word-scale motion against
11.7–23.1% on shipped 9:16 work. Cards move 15–30% of the frame instead.

**2. The stack is TRANSLATED, never reflowed.** The first version collapsed each
spent card's `height`/`marginTop`/`padding` to make room; `check` rejected it 31
times as `gsap_non_transform_motion` — layout properties snap to integer device
pixels, so an ease-out tail stutters under a seek-by-frame capture. The stack is
one `y` transform on a fixed viewport, and the positions are **measured** from
the laid-out DOM (`offsetTop`/`offsetHeight`), never hand-derived: card heights
depend on copy length and on the webfont, so any constant would be wrong the
first time a line is reworded.

**3. The two speakers get DIFFERENT entrances.** Lane A arrives (`power2.out`,
x −70); lane B slams (`back.out(1.7)`, x +70, scale 0.9→1). This is the whole
reason not to set a timeline-level `defaults: {ease}` — one inherited ease put
65% of a sibling project's 196 tweens on a single signature while a grep for an
explicit `ease:` found only 8, and the continuity audit reads that as one house
template.

## Contrast, measured not assumed

| pair | ratio |
|---|---|
| `--ink` on `--mist` (lane A card) | 15.42:1 |
| `--ink-2-mist #626262` on `--mist` (lane A name) | 5.13:1 |
| `--ink` on coral tint `#F6E7E0` (lane B card) | 15.20:1 |
| `#8A4A30` on `#F6E7E0` (lane B name) | 5.62:1 |

Two traps worth carrying:

- `--ink-2 #6B6B6B` on `--mist` measures **4.49:1** — under the floor. A token
  scoped to `--paper` does not transfer to `--mist`; re-measure per ground.
- Lane B is a **tint**, not `--coral`. Not for contrast (`--ink` on full coral is
  5.60:1 and passes) but for accent discipline: a speaker who talks twenty times
  in full-saturation accent makes that accent the colour of the whole video.

## On an ink ground

Both lanes need an inverted variant; see `dialoguelanes-spike.html`'s
`.on-ink` block. `--ink-3-dark` on `--ink-soft` measures **4.13:1** and fails —
use `#93989A` (5.64:1).

## Captions

If the piece has no burned-in caption track, prefix the sidecar cue with the
speaker name **only on a change of speaker**. With two voices and no on-screen
track a captions user otherwise cannot tell who is talking, which is usually
most of the joke; prefixing every cue is noise.
