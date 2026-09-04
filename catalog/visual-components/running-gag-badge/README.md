# RunningGagBadge — a recurring on-screen object with an arc

A small badge that **fires, is reached for, and is finally retired** across a
whole piece. It is not a notification chip: the point is that it appears more
than once and that its last appearance *closes* something the first one opened.

- **Duration** 4.0s in the spike (all four states shown in sequence). In a real
  piece the states are minutes apart.
- **Control** clock — a paused GSAP timeline scrubbed by a single `t`.
- **Scrubber** `debug` — append `?debug=1`.
- **Status** spike, extracted from a real render
  (`videos/ectoin-normal-person`, where it is the JARGON ALARM: fires in
  `03-cell` and `04-protein`, is reached-for-but-not-fired in `05-skin`, and is
  powered down in `12-bottle` on the line "you may deactivate the Jargon Alarm
  now").

## Why this exists

*Spend boldness once.* A piece is allowed one component that is louder than
everything around it, and a badge that recurs with a beginning, middle and end
is a cheaper way to get one than a signature scene — it costs a corner of the
frame, not a beat.

The reason it is worth cataloguing rather than re-inventing is the **retirement
state**, which is the half people skip. A gag that just stops appearing was
never a gag; it was a repeated element. The fourth state below is the whole
value of the component.

## The four states

| State | What it does | Where it goes in a piece |
|---|---|---|
| `fire` | hard scale-in on `back.out(3)`, then a **bounded** pulse | the first time the thing it mocks happens |
| `fire` (again) | identical, so it reads as the same object | the second time, which is what makes it a gag |
| `reach` | drifts in at 0.75 opacity and retreats **without firing** | the near-miss; someone self-corrects in time |
| `retire` | tweens to grey, dims, its dot shrinks | the callback that closes it |

## Data contract

```js
var DATA = { label: "JARGON ALARM", at: [1.0, 2.0], reachAt: 2.7, retireAt: 3.3 };
```

Swap `label`; everything else is timing. The badge itself is markup, not data.

## Two things that are load-bearing

**The pulse is finite.** `yoyo: true, repeat: 3` — a real count, never
`repeat: -1`. An infinite repeat is wall-clock behaviour wearing a tween's
clothes: it will not seek, so it renders as a frozen frame at whatever phase
the engine happened to sample.

**Retirement is a TWEENED COLOUR, not a class toggle.** The first version of
this used `onStart` to add a `.dead` class. Seek does not fire callbacks — the
engine jumps to arbitrary times — so the badge rendered in whatever state the
last executed callback left it. Every visual state has to be a pure function of
timeline position. This is the single most common way a component that previews
correctly renders wrong.

## Positioning

Pin it to the corner **opposite the copy**. In the source piece it was
top-right, which in every unit that used it was the text column, and `check`
reported an 11-sample `content_overlap` error against a spoken line. Top-left,
over the diagram column, has empty corners by construction.
