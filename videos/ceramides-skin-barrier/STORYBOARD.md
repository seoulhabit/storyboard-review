---
format: 1080x1920
duration: ~40.26s (measured — retimed from the nominal 60s sketch to real Kimberly VO, see BRIEF.md § Revision)

message: "Ceramides make up half your skin's barrier — fix that before layering on more actives."
arc: pattern-interrupt hook -> problem -> mechanism/stakes -> solution -> outro
audience: skincare-curious viewers over-investing in actives while under-investing in barrier health
mode: automation
voice: Higgsfield seed_audio, "Kimberly" (674b71b8-1d2e-4087-8567-d1f53c0b9f3c) — not this pipeline's usual HeyGen voice, see BRIEF.md § Revision
music: lo-fi skincare aesthetic, upbeat electronic synth pad, 110 BPM drum loop, chill ambient — generated (MusicGen), ducked to 0.12 under narration
---

## Video direction — REVISION (supersedes the flat/paper cut below)

Type: cinematic photoreal image-plate short, 1080×1920, one pre-generated
still per scene with continuous Ken Burns motion (see BRIEF.md § Revision for
the full rationale and the explicit departure from this pipeline's flat/paper
convention). Motion grammar: brisk crossfade scene transitions (0.35s,
power2.inOut); continuous constant-speed (`ease:none`) scale/pan on each
plate, one direction per scene, no re-direction mid-scene. Captions: full-
screen center, true word-by-word (registry `caption-kinetic-slam`, adapted to
portrait), opaque scrim band guarantees contrast regardless of the underlying
photo. One signature on-screen text moment (`CERAMIDES` stamp, Scene 4) —
every other beat carries its message through narration + captions only, per
the "spend boldness once" posture rule.

**Caption-band:** full-width scrim, 320px tall, centered on the canvas
vertical midpoint (y ≈ 800–1120px of 1920), `rgba(0,0,0,0.85)` — verified via
`hyperframes check`'s Contrast audit (7/7 WCAG AA) against the brightest scene
(Scene 5's white lab background), not assumed.

**Held/continuous allocation:** Scene 4 (20s, the longest) carries a single
continuous zoom across its full duration rather than multiple held beats —
appropriate here because the "signature moment" (CERAMIDES stamp) lands early
(0.15s in) and holds, while the narration itself carries the two stat beats
(50%, 40%) that the *original* cut gave dedicated static frames to. No
proportional geometry is used for either stat (no bar/fill/wipe) — same
render-discipline guardrail as the original cut, now upheld by omission
(there's no infographic geometry tied to the numbers at all) rather than by a
typography-only rule.

## Scene 1 — Hook

- scene: 01-hook
- voiceover (Kimberly, measured): "Stop using Retinol until you do this one thing. It might be destroying your skin barrier."
- window: 0.00s–5.240s
- transition_in: cut (opens the video)
- src: compositions/frames/01-hook.html
- type: image-plate + Ken Burns
- image: Job `3da6be11-c87b-41c6-890a-a205cd8559c7` (Higgsfield `text2image_soul_v2`) — split-screen frustrated red skin vs. glowing glass skin
- motion: centered zoom 1.00→1.06, no pan (preserves left/right split symmetry)
- sfx: cinematic sub-bass impact hit at 0:00, under "Stop"
- persuasion: pattern-interrupt / warning
- keyMessage: the thing you're doing might be hurting your skin barrier

## Scene 2 — The cost

- scene: 02-serum-counter
- voiceover: shares one continuous VO block with Scene 3 (see below), cut on "…on serums,"
- window: 5.240s–7.760s
- transition_in: crossfade 0.35s + soft air whoosh
- src: compositions/frames/02-serum-counter.html
- image: Job `2bb9c5cc-307f-4be2-9a35-d5ed02fd96fe` (`marketing_studio_image`) — marble bathroom counter overflowing with serum bottles
- motion: zoom 1.00→1.10 with slight upward pan
- keyMessage: you're spending real money on actives

## Scene 3 — The crack

- scene: 03-desert-morph
- voiceover: continues the Scene 2 VO block: "…but if your barrier is cracked, that hydration literally just evaporates."
- window: 7.760s–12.221s
- transition_in: crossfade 0.35s + soft air whoosh (second instance, at the cut)
- src: compositions/frames/03-desert-morph.html
- image: Job `02ae5a3c-693a-4223-a9c6-3b698bd4855b` (`cinematic_studio_2_5`) — macro cracked desert earth morphing into dry skin texture
- motion: zoom 1.00→1.13 with downward pan (desert reads into skin top-to-bottom)
- keyMessage: a cracked barrier wastes whatever you put on top of it

## Scene 4 — Enter Ceramides

- scene: 04-ceramides
- voiceover: "Enter Ceramides. They make up fifty percent of your skin's outer layer, the protective grout holding your skin-cell bricks together. But by age 30, you've lost 40% of them."
- window: 12.221s–23.778s (longest scene)
- transition_in: crossfade 0.35s + bright glass chime, synced to the `CERAMIDES` stamp
- src: compositions/frames/04-ceramides.html
- image: Job `7d4a3b63-50f1-41f6-b683-00ad50766c02` (`nano_banana_2`) — 3D infographic, skin cells held by golden lipid "grout"
- motion: centered continuous zoom 1.00→1.15 across the full 20s
- on-screen text: `CERAMIDES` mono kicker stamp, upper-safe-area, lands at 0.15s and holds
- keyMessage: ceramides are the barrier's structural glue, and most are gone by 30
- Note: carries both stat beats (50%, 40%) via narration + caption only — no proportional geometry tied to either number (see Video Direction above)

## Scene 5 — Putting them back

- scene: 05-sourcing
- voiceover: "To fix the cracks, we have to put them back. Skincare ceramides are usually plant-derived from wheat or rice, or lab-made to match your skin perfectly."
- window: 23.778s–32.338s
- transition_in: crossfade 0.35s
- src: compositions/frames/05-sourcing.html
- image: Job `28581481-65a3-4236-aac6-32036e4ee17a` (`marketing_studio_image`) — glass lab beaker with wheat and rice
- motion: zoom 1.00→1.09 with slight upward pan toward the beaker's contents
- keyMessage: skincare ceramides are plant-derived or lab-made, not human-sourced

## Scene 6 — Outro

- scene: 06-outro
- voiceover: "They lock moisture in and block irritants out. Fix your barrier first. Subscribe for more skincare science!"
- window: 32.338s–40.260s (final scene)
- transition_in: crossfade 0.35s + subtle bell notification, synced to "Subscribe"
- src: compositions/frames/06-outro.html
- image: Job `fb1fb534-9141-4017-a5a7-8e8fe6e4f1a1` (`text2image_soul_v2`) — hand pressing rich cream onto glowing cheek
- motion: zoom 1.00→1.08, gentle downward settle
- keyMessage: fix your barrier first — warm close
- Note: no on-screen CTA graphic — "Subscribe" stays spoken + caption only, consistent with this pipeline's convention that subscribe/follow prompts are platform-native UI, not composition content. No dedicated seoulhabit.com endcard in this cut — the brief's exact 6-scene/60s grid leaves no room for one, and Shorts don't carry custom end-screen elements anyway (platform draws its own related-video UI).

---

## Superseded — original flat/paper cut (pre-revision, still rendered at `renders/video.mp4`)

The original 6-frame kinetic-typography/paper-ink build (Frame 1 "Everyone
talks about Retinol…" hook through Frame 6's seoulhabit.com endcard) is
preserved in `renders/video.mp4` and this file's git-free history. See
BRIEF.md § Revision for why it was superseded rather than deleted.
