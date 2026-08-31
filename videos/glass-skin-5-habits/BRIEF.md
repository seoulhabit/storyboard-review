---
workflow: faceless-explainer
flow: automation
storyboard: yes
message: "Korean glass skin isn't 10 products — it's 5 habits done right: Cleanse, Hydrate, Treat, Seal, Protect."
destination: shorts
aspect: 1080x1920
language: en
audience: "Skincare-curious viewers overwhelmed by K-beauty's reputation for long routines — general beauty/skincare YouTube Shorts audience"
length: 35s
angle: how-to
VO_MODE: verbatim-with-one-correction
---

## Intent

A ~35s tactile, macro-photography-led Short teaching the 5-step "glass skin"
routine (Cleanse / Hydrate / Treat / Seal / Protect), built from a
user-supplied 6-beat A/V script. Presenter is the macro plate (product
texture, hands, drops) rather than typography — a deliberate departure from
this channel's typographic-first videos, driven by the user's own brief
("without facial expressions to hold retention, your visuals must be highly
tactile"). Type still carries real weight: a persistent center-left habit
stack (RoutineLadder mechanism, re-skinned) plus wall-to-wall karaoke
captions, per the user's "keep text on screen at all times" rule.

## Assets

- SeoulHabit Video Design System — `assets/tokens/tokens.css` (copied
  verbatim from `videos/seoulhabit-launch/assets/tokens/tokens.css`),
  `assets/fonts/NotoSansKR-500-subset.woff2`.
- `videos/seoulhabit-launch/` + `videos/kbeauty-one-percent-line/` — the
  channel's real reference pair for tokens, the `<hf-audio-group>` voiceover
  bus, and root-composition structure (see `frame.md` § Channel audit for
  why these two and not the others).
- `videos/snail-mucin-truth/.hyperframes/caption-skin.html` — the channel's
  only real burned-in caption mechanism, reused and re-tokened to
  SeoulHabit's paper/ink/aqua (its shipped tokens are an unrelated preset —
  see `frame.md`).
- `catalog/visual-components/routine-ladder/` — focus-advance mechanism
  adapted for the habit-word stack (skin dropped; five-step subset of its
  six rungs — see `frame.md` § Component reuse).
- `catalog/product-photography/assets/` — five reused plates
  (B01/B02/B03/C01/C02); see `frame.md` § B-roll / asset manifest for the
  verified reuse-vs-generate table (two initial catalog-table assumptions
  were corrected by actually opening the files).
- Voiceover: 6 narration lines via Higgsfield, voice "Kimberly"
  (`674b71b8-1d2e-4087-8567-d1f53c0b9f3c`, `voice_type: element`) — the same
  voice `kbeauty-one-percent-line` and `retinol-patch-test` use —
  `assets/voice/{01..06}.wav`.
- SFX: ASMR layer (water, jar unscrew, cream swoosh, pump click, droplet) —
  `assets/sfx/`.
- BGM: one calm, warm instrumental bed — `assets/bgm/track.mp3`.

## Customizations

**Duration**: user chose VO-driven timing over a hard 30s grid — script
kept verbatim (except the one correction below), landing ~34-36s. Still
comfortably inside the Shorts 3:00 limit.

**One VO correction**: line 1's "You're just destroying your skin barrier"
is a blanket claim this evidence-based channel can't ship — step count
isn't what damages a barrier; stacking actives and over-exfoliating are.
User chose to soften it: "Stacking that many actives is how barriers get
wrecked." Same length, same hook energy. See `frame.md` § Content
corrections.

**Macro plates**: user chose a hybrid sourcing strategy — reuse verified
catalog stills where they genuinely match (5 of 9 needed plates), generate
only the real gaps (4 plates: cluttered counter, swept-clear counter, toner
pour, two-finger SPF lines). See `frame.md` § B-roll for the full table,
including two corrections to my own first-pass reading of the catalog.

## Notes

Photography is this video's primary presenter, not an interlude exception
like `kbeauty-one-percent-line` Frame 04b — filed as a larger-scope
controlled exception to the channel's normally browser-drawn house style,
per `catalog/product-photography/README.md`'s "needs its own filed decision
record first" requirement. General-guidance disclaimer ships per channel
convention (general routine literacy, not a locked `ING-*` source record for
a single active).
