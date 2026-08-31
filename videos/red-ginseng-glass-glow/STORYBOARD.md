# red-ginseng-glass-glow — storyboard

1080×1920 · 30fps · total 50.782s · six beats timed to gated Kimberly take lengths.
Plates: Higgsfield cinematic_studio_2_5, 2k, warm-amber grade tail on all prompts.

| # | id | start | dur | VO take (dur) | plate | motion | overlay |
|---|---|---|---|---|---|---|---|
| 1 | 01-hook | 0.000 | 6.482 | 01.wav (5.482) | split face/root | KB zoom-in 1.03→1.085 | "Red Ginseng" lockup + 홍삼 kicker (opaque from t=0 — frame zero) |
| 2 | 02-problem | 6.482 | 6.957 | 02.wav (6.157) | face + barrier cells | KB zoom-out 1.09→1.03 | "Wrinkles, without the retinol toll" tag |
| 3 | 03-heritage | 13.439 | 7.205 | 03.wav (6.405) | apothecary→lab morph | pan across morph at 1.16 | "Centuries of use → Modern lab" |
| 4 | 04-mechanism | 20.644 | 10.523 | 04.wav (8.923) | golden cells vs particles | KB zoom-in 1.0→1.07 | GINSENOSIDES chip: in vitro ROS ↓, PMID 38465216 (reveal @1.9s) |
| 5 | 05-result | 31.167 | 10.730 | 05.wav (8.930, +0.5s pause @2.0) | glass-skin macro cheek | KB zoom-out 1.06→1.0 | ○ UNSOURCED flag (circulation) @3.6s + oral-RCT chip PMID 20041778 @4.6s |
| 6 | 06-cta | 41.897 | 8.885 | 06.wav (6.385) | dropper + serum drop | KB zoom-in 1.0→1.055 | CTA card + aqua subscribe pill @4.2s; end state holds for loop handback |

Captions: 25 cues, track 5, top band y=196, script-authoritative text × whisper word
timing (beat-5 "glass-skin" merged to match script tokenization).
Audio: VO track 10; BGM track-pulse @0.1 track 11; SFX tracks 20–27 (whoosh on scene
turns 2/4/6, click on 3/5, chime on both chip reveals + subscribe pill).

## Spatial plan (per scene)
- Full-bleed plate layer (sanctioned absolute stack), `object-fit:cover`, bg fallback #1A1512, KB overscan marked `data-layout-allow-overflow`.
- Grain overlay (SVG fractal noise, 0.07 multiply) on every scene for cross-plate cohesion.
- One flex-positioned ink card (#16181A, white text) in the safe zone: left x=72, bottom band ~y1360–1440; index pill right-aligned but inside x<918 … right:180px keeps it clear of the Shorts rail.
- One aqua-family accent max per frame: hook underline / chip left-border / subscribe pill border. Beats 2–3 carry none.

## VO gate record (2026-08-30)
- Take 01: first take said "roots"; retake clean. 02/03/05 (+11b) had the seed_audio
  run-to-edge tail defect (tail-200ms peaks −16.8…−22.2 dB) → 40ms fade + 0.25s pad.
- "ginsenosides": garbled differently across 3 takes (real TTS articulation failure per
  series rule) in both "…compounds called ginsenosides" and "…ginsenoside compounds"
  forms. Fixed with phonetic TTS-prompt respelling "jinsenosides" — two independent takes
  then transcribed identically ("ginsenocytes" = ASR bias, consistent), tails clean.
  Captions print the correct spelling from the authoritative script.
- Take 05: 0.5s silence inserted at 2.00s (word boundary after "magic?") per the brief's
  micro-pause note; word timings recomputed by re-transcribing the processed file.
- All installed takes: adeclick applied; final tail-200ms floors −84…−91 dB.
