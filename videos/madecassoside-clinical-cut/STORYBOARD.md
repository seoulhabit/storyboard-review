# Madecassoside Clinical Cut — Storyboard (as built, round 3b)

**Delivery master**: `renders/*_master.mp4` — −14.15 LUFS integrated / −1.92 dBTP (target
−14 LUFS / ≤−1 dBTP), mastered via `volume` + `alimiter=...:level=0` against the raw mix
(measured pre-master at −23.47 LUFS / −4.15 dBTP — nothing had hit the target before round
3). H.264 High 1080×1920 30fps + AAC-LC 48kHz stereo.

**Claim treatment**: every `.uc-claim` sentence is wrapped in a yellow-highlighter span
(per-line, via `box-decoration-break: clone`). Beats 02/03/04/07's claims keep the
`○ UNSOURCED` flag underneath — this repo holds no records for those specific sentences.
Beats 05/06 carry **real, verified citations** instead (Song et al. 2012, *Burns*, PMID
22360962; Bonté et al. 1995, *Ann Pharm Fr*, PMID 7741425) — see BRIEF.md "Round 3b" for
why the claims themselves had to change to match what those papers actually show, not
just gain a citation stapled onto the original wording.

Total 62.950s · 1080×1920 · 30fps · 7 beats, all hard cuts. VO = Kimberly. No dark
presenter stage anywhere in this cut (see frame.md) — every beat sits on the paper canvas.

| # | Start | Dur | Beat | VO (as recorded) | Field state | On-screen claim | Status |
|---|-------|-----|------|------------------|-------------|-----------------|--------|
| 01 | 0.000 | 6.700 | Hook | Why do scars stay bumpy, and how does Madecassoside flatten them? | "Madecassoside" key label (present from frame zero, aqua underline) over a small raised/flat diagram; no VO-duplicate headline | — (question, ingredient named in-shot) | clean |
| 02 | 6.700 | 9.600 | Setup | When your skin tears, or you pop a pimple, your body panics. It rapidly dumps chaotic, unorganized collagen to plug the hole. | Surface tears open; 14 seeded ink strands pour in, tangle unevenly, restless wobble once landed; one aqua tick marks the wound margin; one coral alert pulses on "panics" | Wound repair dumps unorganized collagen to close the gap. | ○ UNSOURCED |
| 03 | 16.300 | 9.400 | Problem | This tangled mess creates a raised, hypertrophic scar. Generic healing ointments just lock in moisture, but they don't fix the structure. | Irregular nodular scar silhouette draws in (real hypertrophic scars are lobed, not one smooth dome) with surface-texture ticks; knot (same object, wobble continuing) inside it; unruled bracket; 3 generic jars; occlusion film; coral strike on "don't" | Occlusives hold surface moisture; they do not reorganize collagen structure. | ○ UNSOURCED |
| 04 | 25.700 | 12.250 | Solution | Enter Madecassoside. This isolated, highly purified molecule doesn't just soothe the skin. It acts as a biological architect. | Paper identity uc-card (nominal fields only, resolves instantly) → hairline field, aqua blueprint over dimmed tangle; FRAME line "Not a barrier. A blueprint." | Positioned as a structural, not just soothing, ingredient. | ○ UNSOURCED (card fields nominal) |
| 05 | 37.950 | 8.600 | Mechanism | It calms the fibroblast cells behind that overgrowth, and prompts the skin to synthesize fresh, structural collagen. | Aqua "calms" sweep; the restless wobble decays smoothly to stillness (no snap, no overshoot — nothing here is forced into alignment); a few aqua-tinted strands fade in on "synthesize", marking newly-added material; key label "Collagen Synthesis" | Suppresses fibroblast migration linked to raised scarring; prompts type I/III collagen synthesis (in vitro). | **Song et al. 2012 (PMID 22360962) · Bonté et al. 1995 (PMID 7741425)** |
| 06 | 46.550 | 7.000 | Result | So instead of fueling the overgrowth, it supports a wound that closes with real structural material. | Bump eases to a visibly *reduced* (not flattened) profile, aqua-tinted with the beat's one bloom; new-synthesis marks settled beneath it; field pair RAISED → REDUCED | Supports wound closure without feeding the fibroblast overactivity linked to raised scarring (in vitro). | **Song et al. 2012 (PMID 22360962)** |
| 07 | 53.550 | 9.400 | CTA | So, are you still relying on generic ointments, or is it time to upgrade your skin repair? Let me know your thoughts below and follow for more! | Two-column choice card (Generic Ointment / Structural Repair) present together; coral underline on "upgrade"; prompt chip + follow tag (in-flow with the stage stack, clear of the Shorts UI zone); beat-6 line ghosts in behind | — (binary choice, not a sourced claim) | clean |

SFX map (absolute, lean 3-sound palette — click-soft / whoosh-short / chime only):
whoosh @6.70 (setup cut) · click @7.57 (tear) · click @16.30 (problem cut) ·
click @24.38 (strike) · chime @25.70 (card) · whoosh @34.65 (phase-B cut) ·
click @37.95 (mechanism cut) · chime @42.99 (new-synthesis strands) ·
click @46.55 (result cut) · chime @50.15 (bloom) · whoosh @53.55 (CTA cut) ·
click @57.39 (underline) · chime @59.49 (prompt).
BGM: track-pulse.wav @0.1 vol, `data-duration="62.160"` (the file's own length).

**Audio gate (run on every take before installation):** duration (ffprobe) →
silencedetect (ffmpeg, −35dB/0.25s) → transcript-diff (whisper medium.en, word count AND
content matched exactly against script on every take recorded across all rounds) →
adeclick → tail-spike scan (200ms-tail `volumedetect`). The "ran speech to the file edge"
failure (word-end within ~0.1s of file end, tail peak well above the ~−90dB clean floor)
has recurred on 3 separate takes across this project's rounds (04/05 in round 1, 05 again
in round 3b) — same fix every time: 40ms fade-out + 0.25s silence pad. Takes 02–07 also
carry a mild `afftdn=nf=-30` de-noise pass from round 3.
