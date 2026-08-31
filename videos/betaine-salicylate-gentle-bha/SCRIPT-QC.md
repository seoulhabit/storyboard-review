# Betaine Salicylate — QC-round script & editing plan (v2, built)

Applies the six mandatory QC fixes. This is the as-built document: every timing below
is measured from the installed takes and verified in the rendered MP4.

## Global Editing Rules

1. **Hook**: BHA defined in the first 3 seconds and the ingredient introduced by 0:05.
   VO phrasing per QC: "Love Beta Hydroxy Acid (BHA), but hate the peeling? Meet
   Betaine Salicylate." Frame zero is fully composed (scroll-stop) — no fade-in.
2. **TTS pronunciation**: the AI voiceover pronounces the ingredient **"bee-tane
   suh-lis-uh-late"**. Implementation: TTS prompts spell it "bee-tane salicylate"
   (Kimberly already renders salicylate as suh-LIS-uh-late); verified by transcript on
   both spoken instances. On-screen text always spells it "Betaine Salicylate".
3. **Placeholders**: all template/flag text — every "○ UNSOURCED — no record in this
   system" row and every "[Authored, illustrative — not a claim]" tag — is **removed
   from the render**. (Note: these were deliberate claim-flags, not template debris;
   removal is logged in BRIEF.md as an explicit QC decision, and the claims they
   flagged now render unmarked.)
4. **Safe zones**: all bottom-screen text shifted up ≥15% of canvas height — the CTA's
   lines now live inside the dark stage and **every readable pixel ends by y≈1032
   (54% of frame)**, verified 0 ink below y=1100 on the CTA beat. Bottom 20% carries
   nothing anywhere; captions hold the top band (y196–330); right ~15% rail kept clear.
5. **Graphics**: the 0:30 pore-unclogging section upgraded from flat wireframe to a
   high-fidelity vector cross-section — gradient-shaded dermis block, dimensional
   plug with specular highlight, glossy gradient droplets, aqua clear-flow particles.
   (Browser-drawn SVG; this render pipeline is deterministic-vector, not generative 3D.)
6. **Audio mix**: royalty-free lo-fi bed under the full runtime at **−25 dB relative
   to the VO** (data-volume 0.056), baked to length with a 0.8s tail fade — no dead
   air. Master normalized to −14.2 LUFS / −1.4 dBTP.

Runtime: **49.1s** (50s target). 1080×1920 · 30fps · five beats.

## Two-column script (as built)

| Time | VISUALS | AUDIO (Kimberly VO + cues) |
|---|---|---|
| 0:00–0:07.5 | **Hook — dark stage split.** Frame zero composed: "LOVE BHA, HATE THE PEELING?" white kinetic type over a bisected field. Left half floods irritated red with drifting flake chips on "hate the peeling" (3.8s); right half blooms calm cyan on the name (5.0s); "MEET BETAINE SALICYLATE" lands at 5.05s. Caption pill defines "Beta Hydroxy Acid (BHA)". | VO: "Love Beta Hydroxy Acid, BHA, but hate the peeling? Meet bee-tane salicylate." · impact-bass at 0:00 · soft click on the name land · lo-fi bed enters at −25 dB |
| 0:07.5–0:17 | **The problem — paper card.** Barrier brick wall assembles; coral acid wash descends on "way too harsh" (10.5s); top course erodes, chips drift off. Claim lines land on "destroy your skin barrier". No flag rows. | VO: "BHA is famous for clearing pores, but it can be way too harsh — you don't have to destroy your skin barrier just to get rid of breakouts." · whoosh on card · click on claim |
| 0:17–0:28 | **Identity — the signature dock.** Two puzzle tiles ("SALICYLIC ACID" + "BETAINE") snap together on spoken "attached" (19.6s), aqua bond ring on the joint, lockup re-labels "BETAINE SALICYLATE". Identity card beneath: INCI / Structure / Class fields, then the claim line. | VO: "It's literally salicylic acid attached to a hydrating amino acid called bee-tane, the ultimate gentle salicylic acid alternative." · click on the dock snap · whoosh on card |
| 0:28–0:37.5 | **Gentle power — high-fidelity cross-section.** Gradient dermis block; the dimensional plug lifts out on "pore-unclogging" (30.1s); channel floods with aqua clear-flow and rising particles; glossy droplets descend and absorb on "built-in hydration" (32.5s) with radiating rings; claim lines on "hands-down the best exfoliant". | VO: "That means all the blackhead-busting, pore-unclogging power of a BHA, but with built-in hydration — hands-down the best exfoliant for sensitive skin." · click on plug lift · sparkle on droplets |
| 0:37.5–0:49 | **CTA — dark stage, everything above 54%.** Vial line-draws, takes cyan glow + "BETAINE SALICYLATE" label on "the glow" (39s); neon "GLOW, / WITHOUT THE BURN."; "— CHECK YOUR INGREDIENT LIST" (41.9s) and "Comment if you found it — and subscribe for more." (44.8s), all inside the stage; calm glow-breathe close. | VO: "You get the glow, without the burn. Have you checked your ingredient list for this yet? Let me know in the comments, and subscribe for more skincare secrets." · chime on glow · whoosh out at 48.2s |

## Voice QA log (this round)

- Block 1 first take: clean; "bee-tane" transcribes as *betaine* — pronunciation fix
  confirmed. Head −0.44s trim, tail dead air trimmed to 6.55s.
- Block 3 first take: **em-dash spoken aloud as "slash"** (the documented PDRN failure
  shape) — regenerated with a comma; second take transcript-clean, head −0.46s trim,
  tail faded (peak 62). Installed at 9.84s.
- Blocks 2, 4, 5: unchanged installed takes from the first build.
- Rendered-MP4 transcript matches the full script end-to-end.
