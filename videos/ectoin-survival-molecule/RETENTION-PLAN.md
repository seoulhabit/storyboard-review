# RETENTION PLAN — ectoin-survival-molecule_retention-master

Session start 17:58 EDT 2026-09-04. Budget: prep to 18:18, shots to 21:18,
assembly to 22:08, sound/captions to 22:28, final export by 22:28, done 22:58.

## Invariants (do not touch)
- VO wavs, words.json, timing.walk(), transitions, captions text, music bed,
  SFX cues, scene ORDER and count (28), 1920x1080 @ 30fps, ~5:38 runtime.
- Originals in renders/ are never overwritten. Output is
  renders/ectoin-survival-molecule_retention-master.mp4 (+ _retention-raw.mp4).

## Plate mechanism
- Generated stills/videos live in assets/plates/ (I##-*.png, V##-*.mp4).
- Video models: Higgsfield minimax_h3 works on this plan (kling/seedance are
  plus-gated). vidIQ generate_video is the second lane (image-to-video with
  startFrameB64). If a shot fails twice -> 2.5D fallback: the still with a
  GSAP Ken Burns / parallax layer stack.
- Plates are FULL-BLEED; text/UI stays inside the safe box. The safe-area gate
  (ink in the 54/108/96/96 margins) is therefore N/A for plate scenes -- it
  assumes a flat page ground. The end-screen reserve on 29-cta is verified
  separately by frame extraction.
- Every conceptual science plate carries a small mono chip
  "CONCEPTUAL VISUALIZATION" (bottom-left, inside safe box).

## Shot list (scene -> plate)
01-hook       V01 salt lake aerial push (0-6s) -> I02 droplet macro push (6-11.7s)
02-osmosis    V02 droplet dive -> V03 bacterium orbit, membrane puckers
03-now        V04 ectoin stabilises (I12 hydration) -> V05 droplet on bottle match-cut
              -> ECTOIN lockup over product still
04-extremolyte I14 hypersaline pond, slow Ken Burns behind the definition
05-halomonas  V06 Halomonas colony (I15)
06-mechanism  V07 osmotic water loss (I11), three-step labels over it
07-question   I12 hydration layer (still, parallax) -> catalog 04-base-skin
08-humectant  split: I16-ish? no -> two stills: glycerin water-cluster vs
              ectoin-at-distance (generate I23/I24) with parallax
09-exclusion  V08 protein hydration layer (I12) for the tidy half; keep the
              existing diagram inversion for the honest half
11-analogy    keep, add slow push on the ring diagram
12-load       I16 barrier calm -> stressor strip -> V10 water escaping (I17)
13-keratin    I16 barrier calm again (stabilised), keep text+cite
14-notforce   keep, dim I02 salt-crust behind "not a force field"
15-framing    keep, add push
16-21         editorial: parallax ground + push; animated data already there
22-whofor     catalog 04-base-skin / 03-flaking (Ken Burns), skin-type cards
23-numbers    V12 bottle turntable I18 front -> I19 back; 7%/2% cards
24-eleven     I19 bottle back still beside the INCI list (carry)
25-formula    catalog C03 flat-lay (16:9) Ken Burns behind the judgement cards
26-kbeauty    V13 serum texture (I20) + V14 toner (I21)
27-resilience V15 sunscreen (I22) -> product stills A01/A03/tube
28-remember   callback montage: I01 -> I03 -> I12 -> I16 -> I04, 1.6s each,
              then the negation cards
29-cta        keep layout (right third + lower-right clear); I19 bottle-back
              still in the left column only
