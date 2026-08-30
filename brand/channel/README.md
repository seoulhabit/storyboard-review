# SeoulHabitSkin — Channel Branding Assets

Built from `/Users/sumitchoudhary/.claude/plans/role-objective-you-valiant-oasis.md`
(the approved VidIQ research + design plan). Extends the existing SeoulHabit
Video Design System (`videos/seoulhabit-launch/assets/tokens/tokens.css`) onto
the channel page rather than inventing a new identity.

## Deliverables

| Source | Exported PNG | Use |
|---|---|---|
| `avatar-800.html` | `avatar-800.png` (800×800) | Channel profile picture — upload under Customization → Profile → Picture |
| `banner-2560.html` | `banner-2560.png` (2560×1440, 1.08MB) | Channel banner — upload under Customization → Profile → Banner image |
| `watermark-150.html` | `watermark-150.png` (150×150, transparent, 6.7KB) | Video watermark (long-form only — see plan §Asset 4) |
| `ABOUT.md` | — | Ready-to-paste channel description text |

Both PNG deliverables clear YouTube's own stated minimums/limits shown in its
Channel customization page (banner: ≥2048×1152, ≤6MB; picture: ≥98×98, ≤4MB,
PNG/GIF no animation).

**How the PNGs were produced** — pixel-exact, not a scaled browser-pane
screenshot (the Browser pane's `computer` screenshot tool downscales content
larger than the pane, so it isn't fit for a real export at these
resolutions):

```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless=new --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=<W>,<H> \
  --screenshot="$(pwd)/<out>.png" "file://$(pwd)/<source>.html"
# add --default-background-color=00000000 for the transparent watermark
```

Each HTML source has its QA-only debug guide (the avatar's crop-safety circle,
the banner's safe-area outline) gated behind a `?debug=1` URL flag — hidden by
default, so a plain headless capture never bakes debug marks into the export.
Re-run the same command after any edit to `avatar-800.html` / `banner-2560.html`
/ `watermark-150.html` to regenerate the corresponding PNG.

## QA / preview harnesses (kept as working history, not scratch)

| File | What it checks |
|---|---|
| `legibility-test.html` | The 24/32/48px avatar-legibility test from the plan — the new `습` avatar vs. Soko Glam (survived) and Song of Skin / Wishtrend TV (failed) |
| `banner-crop-preview.html` | Mobile (1546×423) / tablet (1855×423) / desktop (2560×423) safe-area crops, rendered via clipped iframes rather than browser scroll (scroll-based capture proved unreliable in this session) |
| `banner-corner-preview.html` | Close-up of the bottom-right corner where the schedule pill sits over the macro plate |
| `watermark-contrast-check.html` | The watermark composited over dark / bright / skin-tone-macro swatches |

## Two real bugs found and fixed during verification

1. **Banner: headline overlapped the macro plate.** Measured via
   `getBoundingClientRect` — the headline's right edge (1860px) extended past
   the plate's original left edge (1660px). Fixed by narrowing the plate to
   the plan's own spec (starts x=1900, giving a 40px gutter) and converting
   the schedule line into an opaque `--mist` pill (the same text-over-photo
   pattern the video frames already use via `Scrim`), since a real photo
   there — not this placeholder gradient — could not otherwise guarantee
   contrast for `--ink-3` text.
2. **Watermark: the coral disc nearly disappeared over skin-tone/product-macro
   footage** — exactly what this channel's real B-roll looks like per
   `videos/seoulhabit-launch/frame.md` (amber-bottle and serum-drop macros).
   Measured contrast: **1.01:1** (invisible) against a skin-tone swatch,
   vs. 5.9:1 against dark footage. Added a solid 4px `--paper` ring (a
   stroke, not a glow — the design system bans `drop-shadow`/`box-shadow`
   specifically, not hairline borders) — re-measured at **3.02:1** against
   skin-tone (clears WCAG AA for graphical objects) and **17.7:1** against
   dark footage.

## Macro-plate photography (added after initial delivery)

The banner originally shipped with a CSS-gradient placeholder standing in for
the plan's macro-photo prompt — real HTML, but no actual image, which meant
no usable file existed for upload. Generated the real plate via
`generate_image` (`marketing_studio_image`, portrait 9:16, 2 variants, 2
credits) using the plan's own prompt; picked the higher-saturation of the two
candidates for a closer match to `--coral`. Saved to
`assets/images/macro-serum-drop.png` (768×1376) and composited into
`banner-2560.html` as a real `<img>` — explicit `width`/`height`,
`loading="eager"`, `decoding="sync"`, `object-fit: cover`, matching this
project's own faceless-video-craft image-plate convention even though this
isn't a video composition. Re-verified the headline/plate gutter and the
schedule pill's contrast against the *real* photo (not the placeholder) —
both held.

## Not done here (per the plan's own scope notes)

- Design-system freshness was not re-verified live (`DesignSync` needs
  `/design-login` in an interactive session) — tokens here match the local
  transcription reconciled 2026-08-28.
