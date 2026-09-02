---
workflow: faceless-explainer
flow: automation
storyboard: no
message: "Mugwort is a thousand-year Korean herb whose star molecule, eupatilin, has real preclinical anti-inflammatory evidence — this video shows what is sourced and flags what is not"
destination: shorts
aspect: 1080x1920
language: en
audience: "SeoulHabit's evidence-conscious skincare audience (same as pdrn-cellular-science / madecassoside-clinical-cut)"
length: ~60s target; final runtime set by real Kimberly take lengths
angle: concept
---

## Intent

Build the next SeoulHabit ingredient short from the approved 6-beat Mugwort (Artemisia
Princeps) script (this session, 2026-08-30), following `madecassoside-clinical-cut` as the
structural template — paper-dominant register, no dark stage-box, canonical house tokens,
`.uc-card` + `.uc-citation-pill` components, top-band captions, Kimberly VO.

**Claim-sourcing posture:** verified via NCBI E-utilities before scripting.
- Beat 3 (mechanism) VO is hedged to "lab and animal studies" and traces to two real records:
  - **PMID 29353040** — eupatilin, a PPARα activator, improved atopic-dermatitis-like symptoms
    in an oxazolone mouse model; suppressed IgE and inflammatory cytokines (TNFα, IFN-γ,
    IL-1β, IL-4, TSLP); increased barrier proteins filaggrin and loricrin. *Mouse model.*
  - **PMID 28899779** — eupatilin suppressed TNFα-induced MMP-2/-9 and NF-κB / MAPK-AP-1
    signaling in HaCaT human keratinocytes via PPARα. *In vitro.*
  Neither is a human clinical trial; the VO and claim panel must not read as one. Citation
  pills carry `PMID 29353040` / `PMID 28899779` adjacent to the mechanism claim.
- Beat 2's compound list (camphor, 1,8-cineole, eupatilin as the studied flavone of Artemisia
  species) is nominal/compositional identity, not an efficacy claim.
- Beat 4 (protocol — raw herb / DIY steam irritates vs fermented essence on damp skin) and
  Beat 5 ("floods reactive skin ... before anything else touches it") are authored usage
  guidance with no record in this system → on-screen `○ UNSOURCED — no record in this system`
  flag, per series convention. Never a fabricated citation id.

**Audio posture:** Kimberly VO (Higgsfield `generate_audio`, model `seed_audio`, voice_type
`element`, voice_id `674b71b8-1d2e-4087-8567-d1f53c0b9f3c`). Full gate on every take:
duration → silence floor → transcript-diff (medium.en) → adeclick → tail-spike scan
(run-to-edge defect expected on ~1-2 of 7 takes; remedy = 40ms fade-out + 0.25s pad).
"Eupatilin" is a TTS-rare word — transcript-diff it across takes; garbled-differently means
articulation failure → phonetic respelling in the TTS prompt only (captions keep the real
spelling, ASR used only for timing).

## Notes

- Scaffolded 2026-08-30 via `hyperframes@latest init --resolution=portrait
  --skill=faceless-explainer --example blank`, resolved and pinned to `hyperframes@0.8.20`
  (sibling projects climb monotonically: 0.8.17 → 0.8.19 → this).
- `npm run render` carries `--quality high --workers 1` from day one (static-frame-dedup
  defect + determinism, per pdrn-cellular-science round 3).
- BGM `track-pulse.wav` + SFX (click-soft / whoosh-short / chime) copied verbatim from
  `../madecassoside-clinical-cut/assets/` (itself from red-ginseng-two-routes) — the studio's
  established lean palette.
- Beat starts computed programmatically from real take durations; captions come from the
  authoritative script paired positionally with ASR word timings.

### Image asset manifest (added round 4 — this section did not exist before; catalog
discovery was skipped at scaffold time, and two ready-made mugwort plates sat undiscovered in
this repo's own shared catalog for four rounds)

| Asset | Source | Reused / new | Used in |
|---|---|---|---|
| `assets/plates/18-mugwort.png` | `catalog/ingredient-photography/18-mugwort.png` (2048×2048, Higgsfield-generated, part of the 20-item ingredient-photography set) | Reused verbatim | Beats 01 (hero), 02 (card header band), 06 (loop landing pad) |
| `assets/plates/A05-essence-refill.png` | `catalog/product-photography/assets/A05-01.png` ("Paperboard refill sachet + glass vessel", labeled 에센스·100mL — an unbranded essence bottle, already the right subject for this video's protocol beats) | Reused verbatim | Beats 04, 05 (product consistency across the two first-layer beats) |

No new plate was generated this round — both candidates already existed and matched the
beats' actual content once the catalog was actually checked. See `frame.md`'s Round 4 section
for placement/treatment detail and `assets/thumbnail/` for the derived thumbnail (extract +
grade from the render, not a separate generation).
- Delivery: master to −14 LUFS / ≤−1 dBTP (two-pass ffmpeg `loudnorm`), verify with
  `loudnorm=print_format=json`, frame-extract QA (frame zero composed at t=0, no debug class,
  safe zones respected — round 4: captions y=240 band, `--safe-*` tokens per scene
  [top:192 bottom:384 left:72 right:162, +6px guard margin], verified against rendered pixels
  via `scripts/check-safe-area.py`, not inferred from source), then copy the delivery master
  to `/Users/korswedie/Desktop/ingredent videos/Mugwort/` once this round is approved.

## Round 2 — pasted review pass (2026-08-30)

Verdict "fix-then-ship", five items. Actions, after verifying each premise:

1. **Duration (BLOCKER as stated)** — premise partially outdated: YouTube raised the Shorts
   limit to 3:00 in Oct 2024, so 73.9s would NOT have been rejected. Tightened anyway per the
   explicit <0:59:15 directive: internal VO silences >0.30s compressed to 0.22s (saved 7.9s),
   takes sped 5% via atempo (pitch-preserved — keeps the Kimberly identity), CTA's final
   sentence cut, inter-beat gaps 0.15s. New total **57.671s**. Takes re-transcribed after
   processing; captions/cues/SFX recomputed programmatically from the new word timings.
2. **"Eupatiliin" typo (MAJOR)** — **premise false, no change made.** Verified by repo grep
   (9 occurrences, all "Eupatilin", zero "Eupatiliin") AND by pixel-zoom on the rendered
   frames at the cited timestamps. Not "fixed" silently, since there was nothing to fix.
3. **Lethargic hook (MAJOR)** — sprig now unfurls (each lobe rotates open from a folded-but-
   visible state, staggered through the first sentence, plus a stem width pulse). Deliberately
   NOT a blank-then-write-on: frame zero stays fully composed per this series' documented
   frame-zero rule; the unfurl delivers the requested live energy without blanking the
   scroll-stop frame. Audio gaps closed by item 1's silence compression.
4. **Bloated CTA (MINOR)** — final line ("Mugwort has been waiting…") deleted; beat ends
   ~0.6s after "breakdown." on the composed CTA frame (the shorts loop landing pad) rather
   than a literal cut-to-black, which would break the loop rhyme with frame zero.
5. **Gradient banding (MINOR)** — grain/dither layer strengthened 0.08 → 0.12 opacity in all
   six frames (the composition's existing monochromatic turbulence noise, i.e. dither at
   source rather than a post filter).

Could-not-verify specs are answered with ffprobe/loudnorm measurements in PUBLISH.md.

## Round 3 — pasted review pass (2026-08-30)

Verdict "fix-then-ship", four items. Actions, after verifying each premise against the actual
project files and rendered output (not just the review's description):

1. **End-of-file cutoff mid-word "Mug-" (stated BLOCKER)** — **premise false against every file
   currently on disk, no change made.** `assets/voice/06.words.json` (the CTA take, last beat)
   contains no instance of "Mugwort" at all — round 2 already re-recorded this take to end at
   "...ingredient breakdown." Verified empirically: `silencedetect`/`astats` on the delivery
   master's last 3s shows a clean decay to digital silence (matching the documented, deliberate
   0.5s post-VO pad), not an abrupt cut. The delivered copy in `ingredent videos/Mugwort/` is
   byte-identical (md5) to `renders/mugwort-healing-herb_delivery.mp4`. Only the very first,
   pre-round-2 render (`_2026-08-30_16-05-04.mp4`, 73.9s — the untightened cut that still had
   the now-deleted final CTA sentence) could contain anything like this, and it doesn't match
   the reviewed timestamp/file-length ("0:57", "very end of the file"). Most likely explanation:
   a stale file was reviewed. Re-rendered anyway as part of this round; the fresh render's tail
   matches the existing clean pattern exactly.
2. **`○ UNSOURCED — no record in this system` called a "template placeholder error" (stated
   MAJOR)** — **premise false, no change made.** This is the documented, brief-mandated
   disclosure flag for beats 4/5 (protocol and absorption framings are authored usage guidance
   with no repo record) — see "Claim-sourcing posture" above and frame.md's citation rule.
   Deleting it would silently reintroduce an unsourced claim with zero disclosure, which is
   worse than the status quo, and would reverse an explicit, repeatedly-confirmed series
   convention (never a fabricated citation id). Same pattern as prior rounds on this series;
   holding per established precedent rather than re-asking.
3. **Burned-in captions in the top ~10% of frame, risking Shorts UI overlap (stated MAJOR)** —
   partial, bounded fix. Moved caption top band from y=196 to y=240 (+44px more top clearance)
   in `index.html`; frame.md's safe-area note updated to match. Did **not** apply the literally
   requested 10–15% (≈192–288px) shift, because that lands at y≈388–484 — inside this project's
   own documented content band (y∈[384,1440]) — trading a hypothetical top-UI overlap for a
   guaranteed content collision. y=196 has shipped clean across 5 prior series videos with no
   prior complaint; treating this as a bounded precaution on this video rather than an overhaul
   of the series-wide convention.
4. **Disclaimer tag `[Authored, illustrative — not a claim]` small/low-contrast (stated MINOR)**
   — applied as requested. `.mx-tag`/`.lz-tag` font-size 1.5cqw → 1.8cqw (+20%), color
   `rgba(19,21,22,0.62)` (the series' own documented WCAG-floor token) → `#555555` in
   `03-mechanism.html` and `05-layer.html`. The prior color already cleared 4.5:1 (≈4.96:1
   computed) so this wasn't a strict AA failure, but the darker/larger tag is a real legibility
   win at mobile size with no downside — `npm run check` still shows 33/33 contrast checks
   passing after the change.

Re-rendered and re-mastered (video unchanged frame-for-frame except items 3/4's CSS; audio
unchanged). New delivery: 57.70s, −13.81 LUFS / −1.91 dBTP. See PUBLISH.md.

**Addendum (same round, after hook re-fire):** the hold on items 1/2 above got pushback for not
literally matching the review's directives. Re-examined both rather than complying by default:

- Item 2 revisited: never actually looked at how `○ UNSOURCED` *renders*, only confirmed its
  content was intentional. It turned out to be bare unstyled text (no card/border/fill) sitting
  under the styled comparison cards in beats 4/5 — genuinely plausible to misread as leftover
  template output, distinct from the citation pills in beat 3 which clearly read as designed UI.
  Gave it a proper pill/badge treatment (ink-toned border + subtle fill, `border-radius:999px`,
  same visual language as `.uc-cite` but deliberately not coral, per frame.md's "never mistaken
  for a citation" rule) in both `04-protocol.html` and `05-layer.html`. This resolves the fair
  part of the complaint (looks unfinished) without touching the part that would be wrong to
  concede (deleting a truth-discipline-mandated disclosure). Verified by frame extraction at
  both beats — fits comfortably within the content width, no overflow.
- Item 1 revisited: re-confirmed the clean tail against the newly re-rendered file (same
  silencedetect signature as before). Tried to close the one remaining gap — a stale published
  link (`npm run publish` creates a public shareable URL) being what was actually reviewed — but
  publish requires interactive confirmation and creates new public content, which needs the
  user's explicit go-ahead rather than being run speculatively. Did not complete it; asked the
  user instead. No further local evidence exists for this item; holding without more information
  on which file/link was actually watched.

Re-rendered/re-mastered again after the pill styling change: 57.70s, −13.80 LUFS / −1.91 dBTP.
