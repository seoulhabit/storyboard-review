# frame.md — Hyaluronic Acid · Clinical Redesign (v3)

**Design source: the shipped PDRN reference** — the rendered file
`pdrncellularscience_20260829_162744.mp4` and its in-repo source
(`videos/pdrn-cellular-science/`, especially `frame.md`,
`compositions/frames/01-hook.html`, `02-identity.html`, `06-cta.html`). The
user's directive is to mirror that video's premium/clinical/authoritative
aesthetic exactly. Where this file conflicts with older HA-project
conventions (v1/v2's warm illustrated-presenter build), THIS file wins. The
v1 presenter kit (hand/face/props) is retired — no hand, no face, no sponge,
no padlock icon. Every visual is stark geometry, typography, and schematic
line-art.

Tokens below are transcribed from the PDRN build's own source. **Hardcode
these hex/rgba values directly in each frame** (the PDRN frames do exactly
that); do not `@import` tokens.css in new frames, and NEVER load styles via a
sibling `<link rel="stylesheet">` (documented silent failure — BRIEF Notes).

## Canvas & safe area

1080×1920, 30fps. Content lives in y ∈ [288, 1440] (PDRN's 15%-top /
25%-bottom convention). **No caption track in this video** (PDRN parity —
narration + composed type carry everything), so the old caption keep-out is
replaced by that content window. `1cqw = 10.8px` when sizing type in px
(PDRN sizes in cqw with `container-type:size` on `#root`).

## Palette

Ground & ink:
- `paper #F7F5F0` — page ground. Paper frames use the PDRN radial ground:
  `radial-gradient(1100px 820px at 50% 32%, #FBF9F5 0%, #F7F5F0 55%, #EFEAE1 100%)`
  plus the grain overlay (below).
- `ink #131516` — text on paper, AND the dark-panel fill itself.
- `card #FBF9F5` — light card fill; border `1px solid rgba(19,21,22,0.12)`;
  radius 28px; shadow `0 1px 3px rgba(19,21,22,0.08), 0 4px 16px rgba(19,21,22,0.04)`.
- `dim rgba(19,21,22,0.62)` — kickers, labels, secondary text on paper (AA-checked).
- hairline `rgba(19,21,22,0.10–0.12)`.

Accents (discipline unchanged from house rules):
- `aqua #59B8AE` — ONE interrogated element per frame. Neon-bright variant on
  dark panels: `#6FE0D3` with layered glow (recipe below).
- `coral #C97A5C` decorative / `coral-text #9F6149` (citation-bracket text —
  darkened for AA on paper). At most one coral moment per frame.
- `celadon #6F8F72` (family `#4F6B52`/`#93B896`) — "sourced" tint only
  (citation-pill border/fill), never success/win.
- `red #E05252` — dark-panel negative marker ONLY (the struck marketing
  figures; PDRN's "DAMAGED" register). Never on paper.

On dark panels: primary text `#F7F5F0`, secondary `rgba(247,245,240,0.62)`.

## Typography (PDRN scale, verbatim)

- Headline / FRAME lines: **EB Garamond** — headline 5.0–5.6cqw; FRAME lines
  italic 3.2cqw, `rgba(19,21,22,0.75)`, centered above panels.
- Body / claims / kinetic: **Inter** — claim rows 3.3cqw w600 lh1.45; field
  values 2.8cqw w500; kinetic/neon 4.4cqw w700–800 UPPERCASE tracking -0.01em.
- Chrome / kickers / data: **JetBrains Mono** — kickers 1.46–2.4cqw w500–700
  UPPERCASE tracking 0.06–0.16em in `dim` (on dark: paper at 0.62).
- All three are pre-bundled — reference by family name, no @font-face, no
  Google Fonts links needed.

## Surface kit (clone these exactly)

**Grain overlay** (paper frames, full-bleed, opacity ~0.05, its own layer):
`background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' seed='7' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")`

**Dark stage panel**: `#131516`, radius 40px, centered. Hook size 640×760;
data/protocol panels ~680×980–1150. Content inside gets the glow register —
this is the ONE place glow is permitted (mirroring the shipped reference; the
flat-lane no-glow rule stays in force on paper).

**Neon type** (dark panels): Inter 800 uppercase, color `#6FE0D3`,
`text-shadow: 0 0 8px rgba(111,224,211,0.9), 0 0 24px rgba(89,184,174,0.65), 0 0 64px rgba(89,184,174,0.4)`.

**Glow pill** (dark panels): 999px radius, dark fill `rgba(247,245,240,0.06)`,
2px border in the accent, `box-shadow: 0 0 14px <accent@0.55>, inset 0 0 10px <accent@0.25>`;
label above in Inter 700 paper.

**Identity card** (Frame 2 — the 0:13 format, cloned from
`02-identity.html`): card `left:96 top:494 width:822`, `#FBF9F5`, r28,
padding 56/64. Kicker "INGREDIENT IDENTITY" (Inter 700 2.4cqw dim, ls
0.06em). Name row: EB Garamond 5.6cqw — `HA <span 0.6em rgba(19,21,22,0.5)>· Hyaluronic acid</span>`.
Round badge chip top-right (84px circle, `rgba(19,21,22,0.04)` fill, hairline
border) holding a small ink-gray glyph at 0.5 opacity — for HA a three-hexagon
polymer chain, not a fish. Field rows (`padding:20px 0`, hairline bottom
border, label Inter 700 2.3cqw dim uppercase / value Inter 500 2.8cqw ink):
1. `INCI` → `Sodium Hyaluronate`
2. `MOLECULAR WEIGHT` → `~10 kDa – 2 MDa · grade-dependent`
3. `SOURCE` → `Microbial fermentation (Streptococcus strains)`
Claim block (margin-top 28): Inter 600 3.3cqw —
`Water-binding humectant — capacity set by molecular weight.` then the
CITATION pill (below). This card's claim is genuinely sourced — bracket pill,
NOT an UNSOURCED flag.

**Citation pill** (the boxed clinical citation, used on every sourced claim):
inline pill, radius 999px, padding 14px 28px, fill `rgba(111,143,114,0.10)`,
border `1.5px solid rgba(111,143,114,0.45)`. Text: `CITATION — ` Inter 700
ink + `⌞ ING-hyaluronic-acid-S00N ⌟` JetBrains Mono 500 in `coral-text
#9F6149`. Only the three real ids ever appear: S001 / S002 / S003. On dark
panels the pill sits BELOW the panel on paper (PDRN F6 pattern).

**UNSOURCED flag** (if ever needed): `○ UNSOURCED — <reason>` Inter 600 in
`dim`; hollow circle prefix, never a bracket, never coral/celadon/aqua/red.

**Illustrative tag** (over every mechanism schematic):
`[Authored, illustrative — not a claim]` Inter 600 ~2.2cqw `rgba(19,21,22,0.55)`.

**Ambient molecule field** (paper frames' background layer): 4–6 small HA
polymer glyphs — chains of 2–3 line-drawn hexagons with short link strokes —
scattered per PDRN's fragment field (`02-identity.html`), strokes
`rgba(19,21,22,0.14–0.18)` with exactly one aqua-tinted glyph
(`rgba(89,184,174,0.24–0.35)`, optionally inside a dashed circle). Bounded
slow sine drift (`y: '+=' + (10 + i*4)` over the beat), never rotation loops.

**Light schematic card** (Frames 4–5): the `card` surface holding an inner
wash panel (soft irregular radial tints, `rgba(89,184,174,0.10)` /
`rgba(111,143,114,0.08)` blobs on `#FBF9F5`, grain on top at 0.04) with
textbook line-art: strokes 2–2.5px ink at 0.75–0.9 alpha, geometric shapes
only, JetBrains Mono uppercase labels with thin leader lines. This mirrors
the reference's receptor diagram (ref-45s): minimal, diagrammatic, zero
cartoon.

## Motion

`power3.out` settles everywhere; `power2.inOut` 0.5s crossfades between
frames (cut into F1, F2; cut into F6). VO-paced reveals — each element lands
on its spoken cue; no front-loading, no lazy breathing, no back-half camera
pans. Bounded ambient drift only. **Frame zero of Frame 1 must be dense**
(caption + dark stage + glow visual already composed at t=0 — the shipped
PDRN's one recorded defect was a blank frame zero; do not inherit it). Frame
6's final held state is the video's frame-zero-quality close: fully resolved,
still.

## Sound

Kimberly VO (see SCRIPT.md) on track 10 at volume 1. BGM
`assets/bgm/track-pulse.wav` (63.15s, from the PDRN build) on track 11 at
**volume 0.1**, looped by the assembler if the cut runs longer. SFX from the
PDRN set only: `impact-bass-1, glitch-3, whoosh-short, click-soft, sparkle,
chime` at 0.3–0.35.

## Endcard & compliance

No 습 SeoulHabit endcard (PDRN parity — the video closes on the dark protocol
panel's held frame). Below the final panel, on paper: the citation pill, then
`Tell me below — and follow for more.` (Inter 500, dim), then one small
JetBrains Mono line at `rgba(19,21,22,0.5)`, ~1.8cqw:
`General skincare education — not sourced claims, not medical advice.`
(the house disclaimer, kept deliberately even though the PDRN cut omitted it
— logged in BRIEF Notes).
