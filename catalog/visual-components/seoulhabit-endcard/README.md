# SeoulHabitEndCard

The channel's brand sign-off scene: the actual `습` mark (not just the
wordmark), "SeoulHabit," a tagline, a rule, and a CTA — appended as the final
scene of every video. This is the first shared, reusable version of that
scene; before this entry it didn't exist anywhere in the repo.

## Why this one, and why now

`faceless-video-craft`'s own rulebook (`decision-policy.md`) had a
**C-3 · End-screen scene** rule, but it only covers YouTube's native
end-screen *overlay reserve* (long-form only: clear the corner zones, calm
the motion, hand off to the next video in VO) — nothing about an in-video
brand moment, and nothing for Shorts, which is 16 of this channel's 17
public uploads (`videos/_channel/baseline.yaml`). Two videos independently
built a sign-off scene anyway, because the beat clearly wanted one:

- `videos/collagen-where-did-it-go/compositions/frames/16-end.html` — kicker
  "SeoulHabit," headline "Evidence, not hype.", a coral rule, sub "Sources
  in the description."
- `videos/snail-mucin-medical-secret-v2/compositions/frames/07-endcard.html`
  — the same kicker and headline verbatim, sub "Follow for more." Its own
  commit message says it plainly: *"No shared end-card component exists
  anywhere in the repo; followed the one proven pattern
  (collagen-where-did-it-go's 16-end.html) rather than inventing one."*

Both are wordmark-only — neither uses the actual brand mark. The channel
does have one: the `습` glyph, built for the channel avatar and watermark in
`brand/channel/` (`avatar-800.html`, `watermark-150.html`). This entry is
the merge of the two: the proven wordmark/tagline/rule pattern, plus the
mark that was sitting unused one directory over. See the new
**`C-3a`** rule in `decision-policy.md` (added alongside this component) —
this is what a run reaches for now instead of building a third one-off.

## Field contract

```js
{
  wordmark: "SeoulHabit",    // Latin only -- never set the glyph itself as running text
  tagline: "Evidence, not hype.",   // the line both prior one-offs converged on independently;
                                    // swap per-project only with a reason, not by default
  cta: "Follow for more.",  // swappable -- "Sources in the description." is the confirmed
                             // alternate (collagen's own CTA) when the video's own C-3 overlay
                             // reserve doesn't already carry a source callout
  duration: 4.5             // seconds; long-form can extend the hold -- see "Canvas" below
}
```

## The mark, and the contrast decision behind it

The disc is `--mist` fill with a 3px `--ink` hairline ring (a stroke, never
a glow — `box-shadow`/`drop-shadow` stay banned per this system's own
convention) and the `습` glyph in `--ink`, at the same proportions as
`avatar-800.html` (glyph ≈ 58% of the disc's diameter, optically
centered — Hangul syllable blocks sit high in the em box, hence the small
`translateY` nudge). This is the **avatar's** ink-on-light treatment, not
the **watermark's** coral-disc-on-paper-glyph one — deliberately: measured
by the same WCAG luminance formula `brand/channel/README.md` uses,
`--coral` text/glyph on `--paper` is **3.0:1** (clears WCAG's 3:1 large-text
floor, not this skill's own stricter "4.5:1 contrast floor on rendered
pixels" rule), while `--ink` on `--mist` is nowhere near that edge. The
watermark's coral disc earns its color from sitting on top of *footage*
elsewhere in the channel's assets — irrelevant here, since this end card's
disc sits on the flat `--paper` canvas, not B-roll.

The same math is why the wordmark and CTA below the mark use `--ink-2`
(4.89:1 against `--paper`), not `--coral` — measured, not assumed;
`--coral` at 3.0:1 in that role is what `snail-mucin-medical-secret-v2`'s
own shipped end card actually uses for its kicker and sub-line, which is
likely under this skill's own floor (not fixed here — that's a shipped,
published video, out of scope for this catalog entry). `--coral` stays
reserved for the rule, a graphical divider the text-contrast rule doesn't
reach.

## Canvas

Built at `1080×1920` with the channel's own safe-area tokens
(`videos/seoulhabit-launch/assets/tokens/tokens.css`:
`--safe-top:120px; --safe-bottom:360px; --safe-left:60px; --safe-right:162px`),
because 16 of this channel's 17 public videos are Shorts at that canvas
(`videos/_channel/baseline.yaml`). For a `1920×1080` long-form video, drop
in that project's own safe-area tokens the way
`collagen-where-did-it-go/16-end.html` already scopes its own
(`--safe-top:54px; --safe-bottom:108px; --safe-left:96px; --safe-right:96px`)
— nothing here is Shorts-specific except the two canvas/safe-area constants
and the default 4.5s hold, which C-3a's own long-form guidance extends.

## Fonts

Latin (`EB Garamond`, `Inter`, `JetBrains Mono`) loads from Google Fonts CDN
in this spike, matching this catalog's other entries (`routine-ladder`,
`term-definition`) — flagged there as a render-time network dependency the
real pipeline still carries, not fixed here either. A production composition
should self-host all three instead (matching what
`collagen-where-did-it-go/16-end.html` actually ships), per this skill's own
render-determinism rule against network fetches.

Korean is self-hosted: `assets/NotoSansKR-500-subset.woff2`, copied from
`brand/channel/assets/fonts/NotoSansKR-500-subset.woff2`
(`sha1 c39aa0a2791275eebfa158d2a9025236c3da7b6d`). Worth flagging, the same
way `routine-ladder`'s README already flags its own copy of this exact
question: `routine-ladder`'s README identifies this **same hash** as "the
OLDER copy under `videos/red-ginseng-two-routes/`," distinct from the
remote design system's current file (`sha1 8afa880c...`) that
`routine-ladder` itself uses instead. So `brand/channel/`'s own font copy —
and therefore this entry's — is the older subset, not the current one. Not
re-fetched here; noted so it isn't mistaken for a verified match later.

## Verification

Rendered headless (`--headless=new --window-size=1080,1920`) at the settled
hold (`t=4.5`) and reviewed on the actual exported PNG, not the source —
mark, wordmark, headline, rule and CTA all land inside the safe box with no
overlap, the glyph renders as a real character (not a missing-glyph box),
and both text colors hold their measured ratios against the real rendered
pixels. Not yet run through `hyperframes check` — this is a catalog spike
(see Status), not a project-wired composition; a project that adopts this
still owes it its own `check` pass and post-render pixel QA per this
skill's own mandatory rules.

## Status

**SPIKE — not wired to `build.mjs`.** A validated visual reference, matching
this catalog's existing convention: a project adopting it pastes the mark
+ wordmark + tagline + rule + CTA markup and its timeline into its own final
scene, supplies its own `wordmark`/`tagline`/`cta`/`duration`, and registers
the timeline on `window.__timelines[<its own scene id>]` per the engine's
real contract (this spike exposes `window.__seoulHabitEndcardTimeline` and
`window.renderFrame` for standalone preview only, the same convention
`routine-ladder`'s spike uses).
