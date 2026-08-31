---
workflow: faceless-explainer
flow: automation
storyboard: yes
message: "Betaine Salicylate delivers BHA-style pore-clearing framed as the gentle alternative to salicylic acid — and this video shows plainly that none of those claims trace to a record in this system"
destination: reels
aspect: 1080x1920
language: en
audience: "SeoulHabit's evidence-conscious skincare audience (same as pdrn-cellular-science / red-ginseng-two-routes)"
length: ~60s target (five beats; real Kimberly narration decides the final cut)
angle: concept
---

## Intent

Adapt a user-supplied 60-second, five-beat script about Betaine Salicylate ("The Gentle
Alternative") into a HyperFrames composition **in the same style as
`videos/pdrn-cellular-science/`** — the user's explicit style reference, delivered render
attached to the request. Everything that project settled carries forward verbatim: house
tokens, uc-card/uc-unsourced components, top-band captions, middle-60% safe zone, dark
glow hook + dark neon CTA with paper claim-cards between, `power3.out` motion grammar,
Kimberly VO via Higgsfield, `--quality high --workers 1` renders, and the full audio QA
chain (transcript verification, adeclick, tail-spike gate, −14 LUFS delivery master).

**Claim-sourcing posture (same explicit posture the requester confirmed for
pdrn-cellular-science):** the complete Betaine Salicylate source registry in this system,
confirmed by repo-wide search, is **zero records** — the only mention anywhere is an INCI
line item ("Betaine Salicylate [0.5%]") inside `videos/kbeauty-one-percent-line/frame.md`,
which is not a study record. Every efficacy/gentleness claim in the script (BHA harshness,
"hydrating amino acid," pore-unclogging parity, "best exfoliant for sensitive skin") is
therefore retained close to as-written **and flagged on-screen with the established
`○ UNSOURCED — no record in this system` marker** — never asserted silently, and no
citation id is invented (no coral citation bracket appears anywhere in this video, since
nothing here has a real record). This repeats the documented deviation from the
`seoulhabit-video-3d` claim-enforcement rule that the PDRN project's BRIEF records as
requester-confirmed; it carries the same unsubstantiated-cosmetic-claim exposure noted
there.

**Audio posture:** full five-beat voiceover (Kimberly via Higgsfield `generate_audio`,
voice_id `674b71b8-1d2e-4087-8567-d1f53c0b9f3c`, voice_type `element`, model
`seed_audio` — the exact voice the user's production notes specify and the PDRN video
shipped with), plus the same BGM bed and SFX vocabulary copied from the sibling projects.
Burned-in word-timed captions in the top band, as shipped in PDRN Round 12.

## Customizations (script → build substitutions, all flagged)

- **"Presenter on camera" beats (2 and 5)** — this is a faceless lane; no presenter
  exists in any shipped video. Beat 2's "pushing away a dropper bottle" becomes an
  illustrative barrier-erosion visual; beat 5's "holding up a product like COSRX BHA"
  becomes a **generic, unbranded** line-drawn product vial labeled only "BETAINE
  SALICYLATE" — no third-party brand name, logo, or trade dress is rendered.
- **Beat 1 split screen** — the script's "angry red skin vs calm glowing skin" is built
  as the lane's established red(irritated)/cyan(calm) abstract split (the same
  damaged/healed color vocabulary PDRN beat 6 shipped), never a figurative face and never
  photographic skin. This is the one frame with a genuine binary state, so the red/teal
  pairing is justified per the PDRN frame.md ruling.
- **Beat 3 puzzle pieces** — the script's literal ask ("two puzzle pieces clicking
  together: Salicylic Acid + Betaine") is this video's one signature motion moment:
  two line-drawn molecule tiles dock with a single `power3.out` snap, aqua marking the
  bond. Boldness spent once, per the governing skill.
- **BGM** — the script asks for "upbeat, trendy lo-fi." No such asset exists in this
  repo; per PDRN precedent (its own SFX list had the same gap) the request is mapped
  onto the existing in-repo bed (`assets/bgm/track.mp3`, the red-ginseng lineage bed)
  rather than sourced fresh, at the same ducked 0.1 volume.
- **SFX** — same vocabulary as PDRN: impact-bass under the hook, whoosh/click-soft on
  card and claim arrivals, sparkle on the beat-4 payoff, chime + whoosh-out on the CTA.

## Notes

- Scaffolded via `hyperframes init --non-interactive --example=blank
  --skill=faceless-explainer`, pinned `hyperframes@0.8.17` (matches all recent
  siblings). `--quality high` added to `npm run render` immediately — the PDRN project's
  static-frame-dedup defect fix, carried forward as standing practice.
- VO blocks are written against the fitted Kimberly voice model recorded in
  `../pdrn-cellular-science/SCRIPT-v2.md` (duration ≈ 0.184×syllables + 1.60×stops):
  energy from commas and em-dashes, 1–2 sentences per block, no colons (a colon broke
  generation there), no `ACRONYM — expansion` dash shape (spoken as "slash" there).
- The PDRN atempo=1.12 speed-up is NOT applied here: it was a PDRN-specific operator
  directive, and this script at natural pace already lands near the 60s target.
- Not committed/pushed as part of this work — built and rendered locally for review.

## Build record — 2026-08-29

- CLI pin bumped 0.8.17 → 0.8.19 by the standing upgrade probe (the fresh 0.8.17 cache
  was also missing `layout-audit.browser.js`, which 0.8.19 resolved); `npm run check`
  verified clean on the new pin: 0 errors, 40/40 contrast, layout clean.
- Five Kimberly takes generated in one `generate_audio_batch` (seed_audio). QA chain:
  silencedetect → head trims (01 −0.42s, 03 −0.42s, 04 −0.80s) → adeclick → tail gates.
  Take 5 arrived with 5.47s of trailing dead air (the PDRN CTA failure shape) but a
  complete transcript — trimmed to 10.0s with a tail fade. Take 3 ran to its buffer end
  still audible — 0.28s tail fade applied (tail peak 927 → 150). Transcript-diffed every
  installed take; all wording verbatim. **Pronunciation note:** Kimberly says betaine as
  "bee-teen" (whisper small.en hears "betene", medium.en "B-teen") — the common
  two-syllable creator pronunciation, not a mangled word; accepted, flagged here for an
  operator listen.
- Final beat map (53.266s): hook 0–7.895 · harsh 7.895–17.391 · identity 17.391–32.371 ·
  power 32.371–41.766 · cta 41.766–53.266. 24 whisper word-timed caption cues, top band.
- Render QA (extracted frames, not manifest): two defects found and fixed by re-render —
  (1) frame 3's puzzle tiles "docked" 166px apart (path geometry never interlocked;
  docked offsets recomputed to ±100 so the nub fills the socket, verified from pixels);
  (2) frame 3's identity card ran into the bottom-20% reserved zone (4,899 ink px below
  y=1536; dock+card compacted — final audit 0 ink below y=1440 at every sampled frame).
  Also strengthened frame-zero wireframes after the first extraction read faint.
- Full-video QA on the final render: no blank/near-uniform frame at 2Hz across 53.3s;
  rendered-audio transcript matches the script end-to-end; right-rail and bottom-zone
  ink audits clean (the ~60px of mid-tone in the rail is the dark stage's rounded-corner
  antialiasing, not text); click hunt clean, the only tail transients being the
  deliberate closing whoosh SFX at 52.4–52.6s.
- Delivery master `renders/betaine-salicylate_DELIVERY_-14LUFS.mp4`: video stream copied
  from the high-quality render, audio +10.7dB into a −1.8dB true-peak limiter, AAC 256k
  48kHz → −13.9 LUFS integrated / −1.6 dBTP post-codec (PDRN's method; its linear-gain
  ceiling applied here too).

## QC round — 2026-08-30 (six mandatory fixes, rebuilt at 49.08s)

Applied per the operator's QC review; full as-built plan in `SCRIPT-QC.md`.
1. Hook rewritten to the mandated phrasing (BHA defined, name at 0:05); frame 1's
   bottom line is now "MEET BETAINE SALICYLATE" (replacing "STOP USING IT.").
2. Pronunciation fixed via phonetic TTS spelling "bee-tane" — transcript-verified in
   both spoken instances. Block 3's first regeneration spoke its em-dash as "slash"
   (the documented PDRN defect); comma take installed clean.
3. **All `○ UNSOURCED` rows and `[Authored, illustrative]` tags removed from the
   render, per explicit QC directive.** These were this lane's deliberate claim-flags,
   not template placeholders — with them gone, the script's efficacy claims
   ("way too harsh," "hydrating," "best exfoliant for sensitive skin") now render
   unmarked. This supersedes the flagged-claims posture recorded above and widens the
   unsubstantiated-cosmetic-claim exposure it described; restoring the flags is a
   one-commit revert if wanted.
4. CTA safe-zone lift: all frame-5 text moved inside the dark stage, 0 ink below
   y=1100 (was: lines at y≈1196–1330) — a ≥15%-of-canvas lift, pixel-verified.
5. Pore diagram upgraded to a high-fidelity gradient vector cross-section (dimensional
   plug + specular, glossy droplets, clear-flow particles). Still browser-drawn SVG —
   no generative imagery entered the pipeline.
6. BGM re-baked to 49.081s and mixed at −25 dB under the VO (data-volume 0.056).
Delivery master `renders/betaine-salicylate_DELIVERY_v2_-14LUFS.mp4`: −14.2 LUFS /
−1.4 dBTP post-AAC (alimiter `level=0` chain). Full-video QA: transcript end-to-end
match, no blank frames, safe-zone audits clean, `npm run check` 0 errors 40/40.

## Retention round — 2026-08-30 (five fixes, rebuilt at 47.02s)

1. **Hook restructured** to the mandated benefit-first line ("If you have sensitive skin
   but want the pore-clearing power of a BHA, meet bee-tane salicylate", 5.99s take,
   transcript-verified); frame zero now shows "BETAINE SALICYLATE / GENTLE PORE-CLEARING"
   immediately, split fields relabeled SENSITIVE SKIN / PORE POWER, no lower-third text.
2. **Puzzle tiles deleted** from frame 3 per QC — the identity beat is now headline +
   identity card only, re-cued to the same take.
3. **UI collisions**: captions dropped y196→y390 (below the top Shorts overlays; every
   frame's own text re-laid to start below ~y540); frame-5 CTA text lifted again — all
   text ends by ~y880 (46%), pixel-audited. Mid-round defect caught by frame extraction:
   the dropped caption pill covered the CTA vial; resolved by removing the vial glyph and
   backing the neon type with the glow bloom (type as the performer).
4. **Continuous motion**: every beat now carries a slow linear digital zoom (stages
   1.00→1.08 center-origin; paper cards 1.00→1.06 top-origin so growth moves away from
   the caption band). Verified as live motion by frame-differencing post-settle frames.
   Render size 3.5→11.4MB (zooms defeat static-frame dedup, expected).
5. **Tail trimmed**: beat 5 cut to 10.0s — the video ends 0.24s after the last spoken
   word (47.020s total, was 49.081 with a 2s frozen hold).
Delivery master `renders/betaine-salicylate_DELIVERY_v3_-14LUFS.mp4`: −14.0 LUFS /
−1.6 dBTP post-AAC. `npm run check` clean (32/32 contrast); rendered-audio transcript
matches end-to-end (whisper-of-the-mix wrote "built-in" loosely on one pass; the block-4
stem is byte-unchanged from its verified take, so per the PDRN envelope rule the word is
present).

## QC round 3 — 2026-08-30 (six fixes, rebuilt at 49.39s)

1. **Captions removed entirely** (MAJOR, "distracting narrative text") — all 20 burned-in
   caption clips deleted from the root. Pixel-verified: 0 dark-pill pixels in the old
   caption band on paper frames. NOTE: this reverses the Round-12-style caption
   convention added two rounds ago at QC direction; muted-viewing content is now carried
   by on-screen frame text only.
2. **CTA lift (BLOCKER)** — the whole frame-5 text stack raised ~264px (captions gone
   freed the band): comment/subscribe line now tops at y≈552; zero content below y=1000.
3. **Hook rerecorded** to the mandated beginner line ("Do you have sensitive skin but
   want the pore clearing power of something stronger? Strong ingredients like BHA can
   be way too harsh.", 8.36s installed take, transcript-verified). Known echo accepted:
   the mandated line ends "way too harsh" and beat 2's standing VO opens with the same
   phrase — flagged here rather than silently rewriting the non-mandated block. The VO
   no longer names the ingredient; the frame-zero hero text still does.
4. **Molecular snap restored** to frame 3 (MAJOR): a benzene-ring salicylic-acid glyph
   and a tri-lobe betaine glyph travel and physically snap together on spoken
   "attached", aqua flash + bond at the junction. (This re-adds motion where round 2's
   QC had ordered the puzzle tiles deleted — the two directives conflict; the newest
   governs, implemented as molecular icons rather than the old pills.)
5. **Audio chain** (MINOR): every VO stem reprocessed adeclick → noise gate (−35dB
   threshold, 2:1) → light compression (2:1 @ −18dB, +3dB makeup); transcripts
   re-verified post-chain; 03's tail re-faded after makeup gain raised it (peak 214→5);
   final mix normalized −14.1 LUFS / −1.6 dBTP post-AAC.
6. **F4 pacing** (MINOR): droplet descent, rings, plug lift, and clear-flow particles
   all sped up 1.5×.
Contrast defect caught by `npm run check` mid-round: the glow bloom moved behind the
neon text dropped it below 3:1 — bloom dimmed/repositioned; final 27/27 contrast.
Delivery master `renders/betaine-salicylate_DELIVERY_v4_-14LUFS.mp4`.

## Polish round — 2026-08-30 (operator feedback, rebuilt at 47.99s)

1. **"way too harsh" echo removed**: beat 2 rerecorded as "It's famous for clearing
   pores, but gentle, it is not — you don't have to destroy your skin barrier just to
   get rid of breakouts." (7.09s take, transcript-verified; the phrase now occurs exactly
   once in the video, in the mandated hook line). On-screen claim re-lettered to match
   ("Famous for clearing pores — but gentle, it is not."); wash/chips re-cued.
2. **Clipped "alternative" fixed**: root cause was the 03 stem's tail fade at 9.5s
   starting mid-word (and being applied twice across rounds — fade, then chain+refade).
   Stem rebuilt from the raw take: chain → 0.3s pad → fade at 9.80s, after the word's
   energy (verified by envelope: full level through 27.9s abs, natural decay). Element
   duration synced to 10.140s.
3. **0:40 CTA rebalanced**: stage compacted to fit its content (520px), name enlarged
   to 3.6cqw Inter 800 with a hairline divider beneath, neon up to 5.0cqw, check/follow
   respaced — no more dead cavern below the text.
4. **Ingredient name bigger everywhere**: F1 hero 4.6→5.6cqw, F3 headline 5.6→6.6cqw
   EB Garamond, F5 name 2.2→3.6cqw.
Delivery master `renders/betaine-salicylate_DELIVERY_v5_-14LUFS.mp4`. Check clean
(27/27 contrast); rendered transcript verbatim end-to-end.

## Full-bleed round — 2026-08-30 (four QC fixes, rebuilt at 47.55s)

1. **BLOCKER — framing**: all five frames redesigned full-bleed. The boxed dark stages
   and white cards are gone; backgrounds run to the screen edges (dark radial on frames
   1/5, paper on 2/3/4) and internal graphics render at full canvas width (+50-80% vs
   the boxed cut: hook split-field 1080w, barrier wall and pore cross-section at 1.54x,
   molecules at 1.31x with larger glyph labels, hook hero stacked at 8.0cqw).
2. **Labels**: INGREDIENT IDENTITY / INCI / STRUCTURE / CLASS (and all kickers/diagram
   labels) now #333333 at 3.2-3.4cqw (+~45-50%), values 4.2cqw semibold.
3. **CTA**: "Comment if you found it — and subscribe for more." doubled to 5.1cqw and
   bold (700); still ends ~y1030, clear of the Shorts UI.
4. **VO halting pause at 0:23**: the 0.65s dead-air gap after "betaine," in block 3
   spliced out (atrim+acrossfade, verbatim take kept; internal silences now all
   ≤0.36s). Rendered-mix word gap measured 0.0s. Beat map re-timed (F3 audio 9.700s,
   total 47.552s).
Contrast 27/27; layout clean; rendered transcript verbatim end-to-end. Delivery master
`renders/betaine-salicylate_DELIVERY_v6_-14LUFS.mp4`.
NOTE: a QC report for the centella-tiger-grass video arrived mid-session (its block-06
"morning and night" truncation is real — both installed and pre-declick stems end
mid-decay); a replacement take was generated at Higgsfield but not yet installed when
the operator redirected to this project. That fix remains open in centella's court.

## Rework round — 2026-08-30 (four QC fixes, rebuilt at 46.99s)

1. **BLOCKER — bottom text**: verified real by pixel audit before acting (F3's claim
   reached y1573/82% at beat end; F2/F4 ~74-75%). All three paper frames compacted and
   lifted; F3's zoom eased 1.06→1.05. Re-audit at each beat's end: F2 64% · F3 72% ·
   F4 67% · F5 52% — everything clear of the Shorts overlay band.
2. **MAJOR — water-drop SFX**: sparkle.mp3 gain cut 0.35→0.12 (−9.3dB). Verified in the
   rendered mix: the sparkle window's RMS now sits at/below the adjacent VO-only level.
3. **MINOR — "a gentle" stumble**: block 2 regenerated with the sentence restructured
   to force a clean attack ("It's famous for clearing pores. But gentle? It is not. ...").
   medium.en transcript on stem AND rendered mix both read "but gentle it is not";
   the 0.68s post-"not." pause capped to ~0.35s by splice. On-screen claim re-lettered
   to match ("but gentle? It is not."). New take 6.530s; beat map re-timed (46.988s).
4. **MINOR — hook pacing**: intro field animation retimed ~1.5x (red flood 0.45s, both
   fields fully staged by ~2.1s); hero name/benefit remain composed at frame zero.
Delivery specs (the reviewer's "could not verify" list): 1080×1920 · H.264 yuv420p ·
30fps · bt709 · AAC 256k 48kHz stereo · −14.1 LUFS integrated / −1.6 dBTP post-codec.
Delivery master `renders/betaine-salicylate_DELIVERY_v7_-14LUFS.mp4`.

## Fix-then-ship round — 2026-08-30 (five fixes, rebuilt at 46.99s)

1. **F1 labels (BLOCKER)**: split-field graphics + SENSITIVE SKIN / PORE POWER labels
   lifted ~380-480px (svg top 660→470, h 900→680; hero compacted to make room).
   Measured: frame-1 content now ends y992 (52%), was ~1520 with graphics.
2. **F4 claim (BLOCKER)**: nudged up (diagram 330→310, claim 970→920) — measured 64% at
   beat end. (Pre-fix measurement was already 67%, above the claimed bottom-20% zone;
   lifted anyway per directive.)
3. **F5 CTA (BLOCKER)**: stack shifted down/tightened so the comment/subscribe line
   centers on the frame's vertical middle (line at y888-1042, center ≈965 vs frame 960).
   (Pre-fix it ended at 52% — "very bottom" refuted by pixels — centered per directive.)
4. **Identity fields (MAJOR)**: INCI/Structure/Class labels 3.2→4.8cqw and values
   4.0→6.0cqw (both +50%); the "Ingredient identity" kicker dropped and the Structure
   value tightened to "Salicylic acid + betaine" to hold the safe band; line-by-line
   stagger already present. F3 lowest text 72% at beat end.
5. **Audio (MINOR)**: all five stems de-essed (ffmpeg deesser i=0.32, high-band),
   transcripts re-verified verbatim; ambient bed raised 0.056→0.12 — measured at
   −25.1 LUFS in the VO-free window of the master (the requested ~−25 LUFS).
Reviewer's could-not-verify list (measured): 1080×1920 · H.264 yuv420p · 30fps · bt709 ·
AAC 256k 48kHz · −14.2 LUFS / −1.6 dBTP post-codec.
Delivery master `renders/betaine-salicylate_DELIVERY_v8_-14LUFS.mp4`.

## Thumbnails — 2026-08-30

Browser-drawn HTML thumbnails per the PDRN precedent (`thumbnail/thumb-1080x1920.html`,
`thumb-1280.html`, screenshotted via headless Chrome, exported JPG q2). Design: dark
stage + grain, celadon ingredient pill, "THE GENTLE BHA?" 900-weight hook with coral
underline, struck-through red "RED · PEELING · BURN", the glowing molecule-pair
signature art (bond node fixed after v1 read as a prohibition sign), neon "GLOW, NO
BURN." payoff. Copied to `ingredent videos/Betaine Salicylate/` as thumb1080x1920.jpg
and thumb1280x720.jpg.
