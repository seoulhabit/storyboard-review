# STORYBOARD — exosome-label-problem

Round 2, 2026-09-02. Runtime **67.450s**, 1080×1920, 30fps, narrated (Kimberly).

**Round 2 split the three longest scenes.** Round 1 shipped seven scenes with
03-materials at 13.5s, 05-barrier at 12.8s and 07-verdict at 8.25s carrying
the end card inside it. Each is now two scenes, cut at a **real silence gap
between caption cues** so no cut lands mid-phrase:

| old scene | cut at | why there |
|---|---|---|
| `03-materials` 13.5s | **20.880s** | between cue 7 (ends 20.83, "…fermentation-derived vesicles.") and cue 8 (starts 20.93) |
| `05-barrier` 12.8s | **44.480s** | between cue 15 (ends 44.39, "…to get past the barrier.") and cue 16 (starts 44.57) |
| `07-verdict` 8.25s | **63.120s** | between cue 24 (ends 63.08, "…still developing.") and cue 25 (starts 63.17) |

Each pair shares its ground, so **structure carries the cut** rather than a
colour change: 03a's three-across tile grid against 03b's vertical name
stack; 05a's single full-bleed breached wall against 05b's two-column
intact-wall/skin compare; 07's pure-type verdict against 08's brand lockup
and hero plate. The VO clips are unchanged and span all three cuts —
deliberate, and exactly why the cut points sit in narration silence.

**Cut policy: hard cuts everywhere, no crossfades.**

**This table is derived from `index.html`, not hand-maintained.**

## Scene map

| # | id | start | dur | ground | plate | layout | pill |
|---|---|---|---|---|---|---|---|
| 01 | `01-hook` | 0.000 | 4.000 | paper | ✔ bottle | 2-col grid (annot | plate), bottom-anchored hero | — |
| 02 | `02-what` | 4.000 | 9.050 | ink | — | stacked: term lockup / SVG diagram / turn block | J Extracell Vesicles · 2024 |
| 03 | `03a-materials` | 13.050 | 7.830 | paper | ✔✔✔ triptych | 3-col tile grid, index chip stamped per tile | — |
| 04 | `03b-transfer` | 20.880 | 5.670 | paper | — | vertical name stack, rail down the left gutter | J Nanobiotechnology · 2025 |
| 05 | `04-source` | 26.550 | 9.550 | ink | — | centred branch tree (1 parent → 3 children) | Dermatol Pract Concept · 2026 |
| 06 | `05a-barrier` | 36.100 | 8.380 | paper | — | single full-bleed breached wall | — |
| 07 | `05b-intact` | 44.480 | 4.420 | paper | ✔ skin | 2-col compare (intact wall | skin plate) | Facial Plast Surg Clin N Am · 2026 |
| 08 | `06-questions` | 48.900 | 10.300 | ink | — | vertical gate list, spine rail | Aesthet Surg J Open Forum · 2024 |
| 09 | `07-verdict` | 59.200 | 3.920 | paper | — | pure type — two stacked verdict fields, no plate | Cureus · 2026 |
| 10 | `08-endcard` | 63.120 | 4.330 | paper | ✔ bottle | scene-01 skeleton: 습 brand lockup + hero plate | — |

Sum: 4.000 + 9.050 + 7.830 + 5.670 + 9.550 + 8.380 + 4.420 + 10.300 + 3.920 + 4.330 = **67.450s**
— matches the root `data-duration` (67.450) and the anchor tween (67.450).

Ten scenes averaging **6.75s**, against round 1's seven averaging 9.64s.
Longest is now `06-questions` at 10.300s; the three former outliers are gone.

## The end card

`08-endcard` is a scene in its own right, not a lockup tucked into the
verdict. It carries the channel's **습 mark**, set as TYPE rather than an
image: the glyph is present in this project's own `NotoSansKR-500-subset`
(verified U+C2B5), so it renders crisp at any size and takes `--ink`
directly. The mark sits in a 132px bordered square beside the SeoulHabit
wordmark — the same relationship the channel avatar uses.

The coral watermark variant was **not** used: coral is spent once per video
and this piece spends it on the barrier refusal in 05a/05b.

**The loop lives here.** 08 reuses scene 01's skeleton — same flex column,
same padding, same 400×765 plate panel bottom-aligned right — and runs its
Ken Burns in reverse (1.080→1.0), so the final frame sits at exactly scene
01's frame-zero scale on the same paper ground.

## Voiceover placement

Scene durations are derived from measured take durations, never authored up
front. Takes were trimmed to a uniform 0.08s lead / 0.35s tail (see
`assets/voice/takes.json`).

| take | file | abs start | dur | spans |
|---|---|---|---|---|
| 01 | `assets/voice/01.wav` | 0.000 | 3.210 | `01-hook` |
| 02 | `assets/voice/02.wav` | 4.120 | 8.710 | `02-what` |
| 03 | `assets/voice/03.wav` | 13.170 | 13.190 | `03a + 03b` |
| 04 | `assets/voice/04.wav` | 26.670 | 9.270 | `04-source` |
| 05 | `assets/voice/05.wav` | 36.220 | 12.490 | `05a + 05b` |
| 06 | `assets/voice/06.wav` | 49.020 | 9.990 | `06-questions` |
| 07 | `assets/voice/07.wav` | 59.350 | 7.530 | `07 + 08` |

VO total **64.390s** of speech across 67.450s of runtime.
**27 SFX cues**, re-spotted after each split — deleting or retiming a beat
orphans its cue, so every cue was re-checked against a beat that still fires.

## Per-scene notes

**01-hook** — Frame zero is the poster: the bottle is at rest and `EXOSOME` is already set. **The payoff lands at t=1.35** — inside the ~2s retention window.

**02-what** — The cell and the term name are both composed at t=0 (a blank-frame scan measured 267ms of near-blank after the cut when the name faded in at 0.15). Seven vesicles bud off staggered 0.33s apart, then scatter outward at 5.20 as the turn lands.

**03a-materials** — **First half of the split.** Each material lands as THREE beats — plate, name block, stamped index chip — instead of one, which is what the extra room bought. Tiles carry a 4px ink border and elevation: cream plates on a cream ground changed only ~13 luma per pixel and barely registered as events.

**03b-transfer** — **Second half.** A vertical name stack, deliberately not 03a's grid. The celadon rail draws DOWN the gutter joining the three names (the proposition), then at 1.75 the bar strikes and the rail dims to 0.20 (the withdrawal).

**04-source** — The added taxonomy beat. Scaled up in round 2: at 34px chips and 62px rails the tree occupied barely a third of the safe column and its whole build-out registered as ~1% of steps carrying visible change — the 9:16 under-fill defect, where a correct mechanism reads as 'small fonts'.

**05a-barrier** — **First half of the split**, and where coral is spent. The wall was enlarged 540→780px for the same under-fill reason. Three coral channels drive through the courses, then three brick fragments detach and fall: BarrierWall's own shard mechanism, adapted.

**05b-intact** — **Second half**, and the reversal. The cut lands on a wall that is suddenly WHOLE again beside real skin — which is why the intact wall is composed at t=0 rather than fading in.

**06-questions** — A spine rail draws downward and each gate opens as it passes. Answered gates step back to 0.42 as the next opens — QuestionGate's activation-state property — then all three return at 7.10.

**07-verdict** — **Pure type, no plate** — the one late scene with no imagery, so the cut into 08's brand lockup and hero plate reads as a change of register. Two verdict fields land in sequence, one clause each, then emphasis shifts from the promising half to the developing half.

**08-endcard** — **The end card and the loop.** The 습 mark arrives with a scale pop rather than sitting there as wallpaper, then the headline, rule and CTA. Closes on one specific action, not a subscribe card.

## Audio

- **VO bus** `<hf-audio-group id="voiceover">` carrying the channel's chain verbatim.
- **BGM** re-cut to exactly the runtime from two copies of the source's
  full-body section (27–61.5s) crossfaded at the seam; the source's own quiet
  intro and outro would have left both loop boundaries ~24dB down. Tail fade
  is **150ms**, not 500ms — a 500ms fade measured the final 0.3s at −37dB
  against −16.5dB at the head, handing the replay a dead beat.
- **Automation plateaus carry each clip's real level**, never a bare 1.0: a
  volume lane REPLACES `data-volume` rather than scaling it.
