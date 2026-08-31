# PDRN Cellular Science — VO rewrite (v2, punchy cut)

Rewrite of `user_script.txt`'s six VO blocks for pace and delivery. Frame count,
frame order, on-screen claim text, citations and UNSOURCED flags are **unchanged** —
this pass touches narration only.

**Why it exists:** the shipped build is **80.7s** against a 60s script target
(`renders/…14-19-34.mp4`). Real Kimberly narration is 70.9s of that. Trimming holds
alone can't close a 20s gap; the narration had to come down.

**Generated and installed.** Measured: **VO 54.18s · runtime 60.98s** (−24% / −24%).
Model predicted 54.69s; the six real takes came in 0.5s under it.

---

## The voice model this was written against

Fitted from the six shipped `assets/voice/*.wav` Kimberly renders (RMSE 0.94s):

```
duration ≈ 0.184 × syllables  +  1.60 × sentence-stops
```

**Each full stop costs ~1.6 seconds.** That is the load-bearing finding. Writing in
short punchy sentences — the obvious way to sound fast — is what *lengthens* this
voice. Block 4 proves it: 4 sentences, only 59 syllables, and it ran 17.8s (3.3 syl/s).
Block 5 was 1 sentence, 45 syllables, 8.0s (5.6 syl/s) — the same voice, 70% faster.

So the rewrite gets its energy from **commas and em-dashes, not periods**. Soft breaks
are free; they clause the line for rhythm without buying a pause. Every block below is
1–2 sentences.

---

## The script

Paste-ready for Higgsfield (Kimberly, voice_id `674b71b8-1d2e-4087-8567-…`). Keep the
em-dashes — they are the pacing instrument.

### 01 — Hook · 6.0s VO
> People are applying salmon DNA to their skin — and it isn't a beauty trend, it's medicine.

Frame-zero aligned: "salmon DNA" lands inside the first second, against the glass-skin
orb. No build-up, no setup clause.

### 02 — Identity · 9.96s VO
> It's called PDRN, or polydeoxyribonucleotide, purified DNA fragments from salmon, highly biocompatible with humans, so they won't trigger an allergic response.

**The em-dashes had to go here specifically.** The first take spoke them aloud as "slash"
(see Voice QA). Commas give the same phrasing without the artifact — and the take came in
1.7s shorter.

### 03 — Medical history · 9.3s VO
> Hospitals used it first — it's safe, it triggers rapid cell growth, so it became regenerative medicine for severe burns, skin grafts, and diabetic ulcers.

The "wasn't originally for beauty" idea is dropped from VO because the on-screen FRAME
line already carries it ("This was medicine before it was skincare"). That's the
FRAME/VO division of labour working — not a cut.

### 04 — Mechanism · 12.6s VO
> Here's how it works: your cells carry surface proteins called A2A receptors — locks that control tissue repair. PDRN is the key, and when it turns, inflammation shuts down instantly and blood flow goes up.

Now matches the Round 3 visual, which is a **key and lock**, not a switch. See
Open decisions below.

### 05 — Fibroblasts · 8.0s VO
> It also wakes up your fibroblasts, the cellular factories building brand new collagen, elastin, and hyaluronic acid from the inside out.

**Operator-supplied take**, used verbatim: the generated one mispronounced "fibroblasts".
Note this reverts the word-for-word match with the on-screen CLAIM row that the drafted
line had — the row reads "create new collagen, elastin, and hyaluronic acid", with no
"brand new" and no "from the inside out". Nothing is over-claimed either way; it is a
muted-viewing parity question, not a claim question.

### 06 — CTA · 7.2s VO
> It hacks your cells to repair damage at record speed — so, is salmon DNA worth the hype? Tell me below.

The colon in the first draft ("salmon DNA: worth the hype?") broke generation — see
Generation log. "Worth the hype?" now matches the burned-in neon CTA. The old VO asked a different
question ("Would you try fish DNA for science?") than the screen was showing.
Ending on "salmon DNA" also hands back to the hook's first line, so a Shorts replay
loops cleanly.

---

## Timing

| Frame | VO v2 (actual) | predicted | VO v1 | hold | scene v2 | scene v1 |
|---|---|---|---|---|---|---|
| 1 Hook | 5.55 | 6.01 | 6.90 | 1.0 | 6.55 | 8.18 |
| 2 Identity | 11.68 | 10.97 | 15.82 | 1.0 | 12.68 | 17.80 |
| 3 History | 9.22 | 9.32 | 12.99 | 1.3 | 10.52 | 14.78 |
| 4 Mechanism | 14.01 | 12.57 | 17.78 | 1.0 | 15.01 | 19.63 |
| 5 Fibroblast | 6.51 | 7.85 | 8.00 | 1.0 | 7.51 | 9.26 |
| 6 CTA | 7.22 | 7.97 | 9.41 | 1.5 | 8.72 | 11.08 |
| **Total** | **54.18** | 54.69 | 70.90 | | **60.98** | 80.71 |

Holds are trimmed but not removed. Frames 3 and 6 keep the longest holds (1.3s / 1.5s)
because they are the only two frames carrying a real citation pill — those need read
time under muted viewing. That is deliberate air, not dead air.

These are measured from the installed `assets/voice/*.wav`, not predicted.

## `index.html` timings — applied

```
#el-01-hook / #el-01-voice        data-start="0.000"    scene 6.551    voice 5.551
#el-02-identity / #el-02-voice    data-start="6.551"    scene 12.850   voice 11.677
#el-03-history / #el-03-voice     data-start="19.401"   scene 10.515   voice 9.215
#el-04-mechanism / #el-04-voice   data-start="29.916"   scene 15.007   voice 14.007
#el-05-fibroblast / #el-05-voice  data-start="44.923"   scene 7.506    voice 6.506
#el-06-cta / #el-06-voice         data-start="52.429"   scene 8.724    voice 7.224
#el-bgm                           data-start="0.000"    data-duration="61.153"
```

SFX cues, held at the same proportional position inside each beat:

```
sfx-1a  impact-bass-1   0.000     sfx-3b  whoosh-short  27.369     sfx-6a  chime         57.555
sfx-1b  glitch-3        1.567     sfx-4   click-soft    40.293     sfx-6b  whoosh-short  60.288
sfx-2   whoosh-short    7.802     sfx-5   sparkle       48.564
sfx-3a  click-soft     20.423
```

**Beat 2 carries a 1.173s tail, not 1.0s.** Scaled proportionally, its ambient
fragment-drift tween ends at 12.793s — a 12.677s beat would clip it. Extending the tail
keeps the motion untouched; the alternative was hand-editing one tween out of proportion.
That 0.173s is the whole difference between the 60.980s plan and the 61.153s build.

**Carry the inner-clip fix forward.** BRIEF.md §render QA records a defect where a beat's
root `data-duration` was rescaled but its inner `.clip` durations weren't, so content
vanished mid-beat. Every frame changes duration here, so re-apply that check.

## Shot-sequence retiming — applied

Each frame's internal GSAP timeline was scaled by **its own VO ratio** (the convention the
prior passes used), and every inner `.clip` `data-duration` synced to the beat total:

| Frame | ratio | timeline ends | beat duration |
|---|---|---|---|
| 1 Hook | 0.804143 | 5.113 | 6.551 |
| 2 Identity | 0.738210 | 12.793 | 12.850 |
| 3 History | 0.709556 | 8.822 | 10.515 |
| 4 Mechanism | 0.787795 | 13.463 | 15.007 |
| 5 Fibroblast | 0.813250 | 6.517 | 7.506 |
| 6 CTA | 0.767531 | 7.500 | 8.724 |

Scaled: every `duration:`, every `stagger:`, every position argument (including the
computed `0.431 + idx * 0.215` forms) and `05-fibroblast`'s `starts2` time array. Left
alone: `repeat:`, easing arguments like `back.out(2.4)`, `Math.PI * 2 * 0.5`, `attr:`
targets, and pixel offsets such as `'+=' + (10 + i * 4)` and `var dist = 20 + idx * 3`.

The transform audited every `tl.` call for an unrecognised position argument and reported
none. `.retime-backup-v2/` holds the pre-pass `index.html` and compositions.

---

## Claim safety

Nothing was strengthened. Four things came down in strength, all of them unsourced
superlatives:

| Frame | v1 | v2 | Effect |
|---|---|---|---|
| 1 | "a medical breakthrough" | "medicine" | weaker; matches Frame 3's sourced injected-ulcer trial |
| 3 | "so safe and **brilliant** at triggering" | "it's safe, it triggers" | superlative dropped |
| 5 | "brand new collagen" | "new collagen" | matches the on-screen CLAIM row exactly |
| 5 | "from the inside out" | cut | not on screen; asserted nothing |

Held at parity deliberately: "highly biocompatible" (F2), "severe burns, skin grafts,
and diabetic ulcers" (F3), "instantly" (F4), "hacks your cells… record speed" (F6).

**"Burns, skin grafts, and diabetic ulcers" is not cut,** even though shortening it
would save ~1.5s and drop two unsourced items. Frame 3's UNSOURCED flag reads
"burns & grafts not in this system's records" — that flag is meaningless if the
narration never said burns and grafts. The flag needs its referent.

No citation id was invented. `ING-pdrn-S001` / `S003` / `S004` remain the only three,
in their existing frames.

## Open decisions for the build lane

Two on-screen CLAIM rows now diverge from the VO. CLAIM rows are compiled and governed,
so these are your calls, not mine:

1. **Frame 4** — the CLAIM row still reads "it flips the switch". The visual has been a
   key-and-lock since Round 3 and the VO now matches the visual, which leaves the CLAIM
   row as the only "switch" left in the frame. Swapping it to the key metaphor is a
   metaphor change at identical claim strength on an already-UNSOURCED, already
   `[Authored, illustrative — not a claim]` line — but it is still a CLAIM row edit.
2. **Frame 2** — VO says "allergic response"; the CLAIM row says "allergic immune
   response". Cosmetic, but it is a divergence under muted viewing.

## Notes for generation

- **Say "polydeoxyribonucleotide" once, in Frame 2, isolated between em-dashes.** That
  isolation is the tongue-twister mitigation — it gives the model a clean run-up and
  landing. If it still renders badly, dropping it saves 2.0s and costs nothing on
  screen: the identity card already prints both "PDRN · Polydeoxyribonucleotide" and
  the INCI line.
- Generate the six blocks separately, as the current build does. One render per beat
  keeps the per-frame retiming honest.
- Back up `assets/voice/*.wav` the way the Kimberly swap did
  (`_pre-kimberly-backup/`) before overwriting.
- No graphic-content exposure: this lane is browser-drawn SVG/CSS/canvas only, no
  generative imagery, and Frame 6 uses SplitFaceProtocol's geometric periorbital
  diagram — never a figurative face. There is no photoreal ulcer, burn, or fish
  anywhere in the build to filter on.

---

## Generation log — 2026-08-29

Six blocks via Higgsfield `generate_audio_batch`, model `seed_audio`, Kimberly
(`674b71b8-1d2e-4087-8567-d1f53c0b9f3c`, `voice_type: element`) — same voice and model as v1.

**Block 6 failed silently on the first take.** The line ended `salmon DNA: worth the hype?`
and the take ran 12.80s: speech stopped at 7.06s, then 5.69s of digital silence (−89 dB) and
a 0.05s click at the tail. It read as "just a long take" on duration alone — the tell was
that only 0.66s remained for the last eight syllables, which is not speakable. The colon is
the likely cause. Regenerated as `— so, is salmon DNA worth the hype?` (7.22s, clean) and as
`. So, is salmon DNA worth the hype?` (7.84s, 0.56s trailing silence); the em-dash take won
on both counts.

**Note the detection trap:** `ffmpeg -v error … silencedetect` prints nothing, because
silencedetect logs at INFO. A silence check run that way returns clean on a file that is
5.7s of dead air. Use `-hide_banner -nostats` instead.

**Leading silence trimmed** (dead air at a cut is exactly what this rewrite is removing):
block 1 −0.40s (had 0.457s), block 3 −0.39s (had 0.448s), block 4 −0.25s (had 0.302s).
Blocks 2, 5 and the regenerated 6 had none. All internal pauses left alone — they are
phrasing. No trailing silence in any installed take.

All six installed at 24000 Hz / stereo / pcm_s16le, matching v1. Previous Kimberly takes
backed up to `assets/voice/_v1-kimberly-backup/`; the older Kokoro set remains in
`_pre-kimberly-backup/`. Raw untrimmed downloads kept in `assets/voice/_v2-staging/`.

---

## Render QA — `renders/pdrn-cellular-science_2026-08-29_15-18-58.mp4`

`hyperframes@0.8.17 render --quality high --workers 1` (single worker, per the lane's
determinism rule). **61.2s · 1835 frames · 1080×1920 · 5.7 MB.** `npm run check` passed
first time: 0 lint, 0 runtime, 0 layout, 0 motion, 23/23 contrast.

Verified from extracted frames, not the manifest.

**The inner-clip defect did not recur.** A luma-variance scan at 2 Hz across all 61.2s
found no blank or near-uniform frame in the middle or at the end of any beat — which is
where content-vanishing-mid-beat would appear. Every beat's settle frame is dense and
fully built; all three citation pills (`ING-pdrn-S003`, `S001`, `S004`) and all four
UNSOURCED flags render legibly; no missing glyphs.

The only near-empty runs are at beat *openings*, before content arrives — and they are
pre-existing pacing that this pass **shortened**:

| | v1 render | v2 render |
|---|---|---|
| beat 2 opening | 2.5s | 2.0s |
| beat 3 opening | 2.0s | 1.5s |
| beat 4 opening | 2.5s | 2.0s |

Structural safety check: masking every decimal in both versions, the diff between the
pre-pass and post-pass compositions is **0 lines** across all six files — the transform
changed only numeric values. No `requestAnimationFrame` / `Date.now` / `performance.now` /
`Math.random` anywhere.

Audio: all six VO blocks detected at their declared starts (0.000 / 6.551 / 19.401 /
29.916 / 44.923 / 52.429, each within +0.05–0.35s — first-phoneme attack). Audio track
61.15s against 61.17s of video.

### Defect found — frame zero is blank

`t=0` is an empty cream rectangle: grain texture and nothing else. This is the scroll-stop
frame and the thumbnail candidate, and it breaks both governing rules —
`seoulhabit-video-3d` ("Frame zero is the final built frame holding the dense
pause-and-study state… never blank") and the craft skill's "frame zero is a design object…
never a lone title on empty canvas."

**Pre-existing, not introduced here.** STORYBOARD.md Frame 1 Scene 1 authors it as
"matte paper ground with fine grain, as VO begins — unchanged," and this pass only
shortened it (1.2s → 0.965s). It is the highest-leverage remaining defect in the video.

Fix is small: pull Frame 1's Scene 2 reveals to position 0 so the stage box, the glowing
vial and the "SALMON DNA?" caption are already composed at `t=0`, and let the VO's first
line land over an image that is already there. Not done here — it edits the authored hook
sequence the storyboard deliberately marks unchanged, across several rounds of your own
iteration, so it is your call.

### Burned-in text now diverging from VO

Visible in the render, all on Frame 1 and Frame 4:

1. **Frame 1 sub-line reads "—it's actually a medical breakthrough"** while Kimberly now
   says "it isn't a beauty trend, it's medicine." The screen is carrying the *stronger*
   unsourced claim of the two. Per STORYBOARD this line is authored hook copy, not a
   compiled CLAIM row and marker-free — so unlike the Frame 4 row it can be changed without
   touching a governed claim.
2. **Frame 4 CLAIM row still reads "it flips the switch"** while the VO says "PDRN is the
   key, and when it turns" and the visual is a key and lock. The row is now the only
   "switch" left in the frame.
3. Frame 2 CLAIM says "allergic immune response"; VO says "allergic response". Cosmetic.

Frames 3, 5 and 6 read clean against the new VO — Frame 5 is word-for-word.

---

## Voice QA — the check that duration and silence miss

Two of the six generated takes were wrong in ways that **duration and silence analysis
cannot see**. Both takes were the right length, had no dead air, and passed every
structural check. The words were wrong.

| Block | Defect | Evidence |
|---|---|---|
| 02 | em-dashes spoken aloud as **"slash"** — *"It's called P-D-R-N slash polydeoxyribonucleotide slash purified DNA fragments…"* | 0.48s and 0.16s of real audio at exactly the two dash positions |
| 05 | **"fibroblasts" mispronounced** — transcribes as "fibrostrats" | operator caught it on listening; confirmed against a correct take |

**Standing method: transcribe every take and diff it against the intended line.** The
correct sequence is duration → silence → *transcript* → install. Skipping the transcript
step is what let both of these reach a render.

Block 2's fix was to drop the em-dashes for commas. The construction that triggers it is
`ACRONYM — expansion` — seed_audio appears to read it as an abbreviation pattern. Blocks 1,
3, 4 and 6 all use em-dashes and transcribed clean, so em-dashes remain the pacing
instrument everywhere else; only the acronym-expansion shape needs commas. The comma take
also came in 1.7s shorter.

Block 5 uses the operator-supplied take verbatim, converted from 44.1 kHz mono MP3 to the
project's 24 kHz stereo `pcm_s16le`. Superseded takes are in `assets/voice/_v2-superseded/`.

## Render QA — `renders/pdrn-cellular-science_2026-08-29_15-35-28.mp4`

**60.8s · 1080×1920 · 6.0 MB.** `npm run check`: 0 lint, 0 runtime, 0 layout, 0 motion,
21/21 contrast.

End-to-end transcript of the **rendered audio track** matches the intended script on all
six blocks — no "slash", "fibroblasts" and "polydeoxyribonucleotide" both correct. This is
now the acceptance gate for audio, alongside frame extraction for video.

Frame scan: no blank or near-uniform frame mid-beat or end-beat anywhere in the 60.8s. All
six settle frames dense and fully built; all three citation pills and all four UNSOURCED
flags legible. Near-empty runs remain only at beat openings — beat 2's dropped to 1.5s
(from 2.0s), beats 3 and 4 unchanged at 1.5s and 2.0s, and beat 5 gained a 0.5s opening
from its 1.23× stretch.

Final beat map:

```
1 Hook        0.000 – 6.551    VO 5.551
2 Identity    6.551 – 17.511   VO 9.960
3 History    17.511 – 28.026   VO 9.215
4 Mechanism  28.026 – 43.033   VO 14.007
5 Fibroblast 43.033 – 52.033   VO 8.000
6 CTA        52.033 – 60.757   VO 7.224
```

**Still open, unchanged:** frame zero is blank, and Frame 1's sub-line ("—it's actually a
medical breakthrough") and Frame 4's CLAIM row ("it flips the switch") still diverge from
the VO. See the sections above.

---

## Feedback round — 2026-08-29 (audio pop, citation holds, dynamic hook, safe zones, color cues, CTA rewrite)

Applied against the operator's review-notes list. `.retime-backup-v3/` holds the pre-pass state.

### Audio
- **The 0:17 pop**: all six VO tracks now run through ffmpeg's `adeclick` (autoregressive
  declicker — the "AI de-clicker" ask, minus the marketing). Durations byte-stable.
- **Found in passing**: block 5 (the operator-supplied clip) ended mid-waveform at 15.6%
  full scale — a hard truncation that popped at ~0:51. Fixed with a 60ms tail fade.
  Pre-declick originals in `assets/voice/_pre-declick/`.

### CTA rewrite (block 6 regenerated)
> It hacks your cells to repair damage at record speed. So, would you inject fish DNA into
> your face, or is this skincare trend a step too far?

9.220s installed take, transcript-verified word-for-word. Neon CTA re-lettered to match:
"INJECT FISH DNA?" / "OR TOO FAR?", two stacked lines, per-word reveals riding the VO's own
word timings. **Honesty note**: the question says *inject* while the on-screen S004 label
still reads "Periorbital · Topical · N=32" — kept intact deliberately; the diagram never
claims the injectable route, the question merely asks about it.

### Citation holds
- Frame 3: beat extended 10.515 → 12.015s; the S003 pairing and the S001 coda now hold
  ~4.7s and ~4.0s respectively.
- Frame 6: instead of stretching the beat, the citation was **moved earlier** (lands 2.9s
  into the beat, straight after the split resolves) — the S004 pill's read window is now
  ~8.6s, up from ~3.7s.

### Dynamic hook (frame 1 rebuilt)
Frame zero is now fully composed — caption + dark stage + glowing salmon + near-empty
vial — which also closes the blank-frame-zero defect from the last QA. The opening beat is
the extraction itself: five DNA-fragment glyphs stream from the salmon into the vial while
its liquid rises (SVG attr tweens), the salmon dims as the extract concentrates, and the
vial takes the glow. Sub-line re-lettered to match the VO: "—it isn't a trend. It's
medicine." (the old "medical breakthrough" line was the stronger unsourced claim; the
"beauty" variant was cut after the pixel audit showed its last word crossing x=918 into
the button rail).

### Safe zones (stricter than Round 4)
Content band moved from y∈[288,1440] to the **middle 60%** (y∈[384,1536)): stages and
cards in frames 1, 4, 5, 6 shifted to top:384. Cards narrowed (888 → 822/840) so no text
crosses x=918 (right ~15% rail). Frame 2's card already sat at 494; frame 3's card kept
top:322 because its stacked rows need the height — its *text* still clears both reserved
edges. Bottom 20% (y≥1536) carries nothing in any frame.

### Scientific color cues
- **Frame 4**: inflamed-red radial wash now sits behind the receptor from frame zero and
  cuts to a cool blue-aqua wash exactly on VO "instantly shutting down inflammation"
  (10.85s; word lands 10.89s). The key's travel was stretched to arrive at "when it
  turns" (10.14–10.84s) — the turn used to fire 2.8s before the word. The red/cool pairing
  deliberately reuses beat 6's damaged/healed vocabulary.
- **Frame 5**: on "from the inside out" (6.63–7.84s) the matrix pulses, two rings radiate
  outward from its center, and the three output glyphs push outward and up-scale. Bounded,
  settles.

### Timeline
```
1 Hook        0.000 –  6.551   VO 5.551
2 Identity    6.551 – 17.511   VO 9.960
3 History    17.511 – 29.526   VO 9.215   (+1.5s citation hold)
4 Mechanism  29.526 – 44.533   VO 14.007
5 Fibroblast 44.533 – 53.533   VO 8.000
6 CTA        53.533 – 65.033   VO 9.220   (rewritten, citation window ~8.6s)
```

### Publish envelope
Title, description, hashtags, and the three seeded comments live in `PUBLISH.md`.
YouTube pins only one comment — pin #1, post #2/#3 unpinned from the channel account.

### QA findings on the first feedback-round render (15-59-30), fixed before final
- **Safe-zone pixel audit**: bottom 20% carried zero ink on every key frame; the right
  15% was clean everywhere except the hook sub-line, whose "…medicine." crossed x=918.
  Shortened the line rather than shrinking the type.
- **Color cue too faint**: the inflamed/calm washes read as a tint at render, not the
  requested sharp state change — alphas raised (inflamed 0.55→0.9 overall, calm target
  0.6→0.9, gradient stops up ~50%).
- **Click hunt, whole 65s**: one isolated-transient candidate at 3.389s — the /t/
  stop-release in "isn't", legitimate speech. The 0:17 boundary is clean after adeclick;
  block 5's truncation pop at ~0:51 is gone (tail fade).
- Rendered-audio transcript matches the intended script word-for-word, including the new
  polarizing CTA.

---

## Round 5 — 2026-08-29 (glitch removal, "mouthful" aside, subscribe CTA)

### Audio cleanup
The "scratch/glitch" was the **deliberate `glitch-3.mp3` tech-glitch SFX** at 1.57s — a
holdover from the original script's "Bass drop → Tech glitch" cue that reads as a defect
against the clean VO. Removed from the timeline (element deleted, not muted); the hook's
hard cut now stands alone over the impact-bass. A fresh full-file click hunt on the
rendered audio is part of this round's QA gate.

### "Whew, that was a mouthful!"
Block 2 regenerated in full rather than spliced, so Kimberly delivers the aside in one
natural read:

> It's called PDRN, or polydeoxyribonucleotide. **Whew, that was a mouthful!** Purified DNA
> fragments from salmon, highly biocompatible with humans, so they won't trigger an
> allergic response.

Installed take 12.60s (was 9.96s). Frame 2's timeline was re-set against the installed
take's own transcript rather than proportionally stretched: the name lands on the spoken
"PDRN" (0.93s), the card **deliberately holds during the aside** (4.36–5.5s) with only the
small round badge landing — a quiet clinical wink, nothing that undercuts the identity
beat — then the three nominal fields ride "Purified DNA fragments from salmon" and the
CLAIM row lands on "highly biocompatible."

**Trim near-miss worth recording:** whisper timed the untrimmed take's head words into a
region silencedetect called dead (0–1.96s). The 1.90s trim was validated by re-transcribing
the *installed* file — head intact, so silencedetect was right and whisper's head snap was
wrong. Same lesson as the CTA trim in the last round: never trust whisper's first word's
timestamps; verify trims on the trimmed file.

### Subscribe CTA
New Kimberly line appended as its own timeline element (`assets/voice/07-follow.wav`,
2.93s, transcript-verified), starting 9.55s into beat 6 — a natural 0.33s beat after
"...a step too far?". Matching on-screen line ("Let me know your thoughts below and follow
for more!") lands beneath the citation pill at the same moment, Inter 600 at 2.8cqw, muted
ink — subordinate to the citation, inside the safe band.

### Timeline (69.87s)
```
1 Hook        0.000 –  6.551   VO 5.551
2 Identity    6.551 – 20.151   VO 12.600  (mouthful aside)
3 History    20.151 – 32.166   VO 9.215
4 Mechanism  32.166 – 47.173   VO 14.007
5 Fibroblast 47.173 – 56.173   VO 8.000
6 CTA        56.173 – 69.873   VO 9.220 + follow 2.930 @ 65.723
```

### Round-5 render QA — `renders/pdrn-cellular-science_2026-08-29_16-27-44.mp4`
**69.9s · 1080×1920 · 6.6 MB.** `npm run check`: clean, 30/30 contrast.

- **Click hunt: zero isolated transients in the full 69.9s** — with the glitch SFX gone,
  even the previous /t/-release candidate no longer trips the detector's thresholds.
- Rendered-audio transcript carries the aside and the follow CTA. One transcription
  quirk, verified harmless: whisper drops "Whew," when transcribing the full mix (BGM
  under a breathy interjection) — the 50ms-resolution energy envelope of the render at
  that spot matches the installed 02.wav sample-for-sample, so the word is present;
  whisper simply merged it. Envelope comparison is the tiebreaker when a transcript of
  the *mix* disagrees with a transcript of the *stem*.
- Frame checks: card holds correctly through the aside (name + eyebrow only, badge lands
  at its end); full identity card + CLAIM + UNSOURCED by 8.95s into the beat; follow line
  renders beneath the citation pill and the safe-zone audit on that frame is 0-ink in
  both reserved zones.

---

## Round 6 — 2026-08-29 (pacing, keyword frames, neon key, pulsing bed, VO speed-up)

`.retime-backup-v4/` holds the pre-pass state. New total **63.15s** (was 69.87s).

### VO speed-up + micro-pause removal
Every block (and the follow line) reprocessed: `silenceremove` caps internal pauses >0.40s
at 0.26s, then `atempo=1.12` (+12%, mid of the requested 10–15%), then `adeclick`. Wording
verified by transcript on all seven processed files. **Because pause removal is non-uniform,
every word-synced cue was re-set from fresh transcripts of the processed takes** — not
proportionally scaled; the analytic silence-map disagreed with silenceremove's actual cuts
by ~0.2s/block, so transcripts are the only trustworthy map.

New VO durations: 4.97 / 11.26 / 8.24 / 12.32 / 7.16 / 8.20 (+2.61 follow).

### Line-by-line text (0:07 → beat 2)
The CLAIM row now reveals in two lines ("Highly biocompatible with humans —" then "won't
trigger an allergic immune response."), then the UNSOURCED flag — three tracked reveals
where there was one lump. The nominal fields already revealed line-by-line.

### Clinical frame simplified (beat 3) — with one wording substitution
The authored FRAME line is promoted out of the card into hero kinetic type — "MEDICINE,"
/ "BEFORE SKINCARE." line-by-line — and the panel compacts beneath it (rows at 2.4cqw,
still above the 2.3cqw legibility floor). **The requested keyword "Hospital Proven" was
not used**: as a standalone rendered surface it would assert efficacy without a source id
— the S003 record covers one injected diabetic-foot-ulcer trial, and burns/grafts are
explicitly flagged UNSOURCED in this very frame — so the punchy layer uses the authored
FRAME line, which asserts nothing. Every governed row (CLAIM, ROUTE, STUDY, Note, both
markers, the S001 coda) remains rendered, verbatim.

### Neon key (beat 4)
The key is now neon cyan (#00E5D1) with a two-stage glow, stroke bumped to 3.2 — the same
cyan vocabulary as beat 6's "healed" state, under this frame's existing Round-2 glow
exception. Receptor, membrane, and gate stay ink; the pocket still takes aqua at the flip.

### The "0:17 scratch"
No isolated transient exists at 0:17 in the previous cut — the largest jumps there are
plosive-scale, inside "biocompatible with humans" (the deliberate glitch SFX was already
removed last round). The full reprocessing chain (adeclick again, plus the new takes) is
the corrective anyway; this round's QA re-runs the whole-file click hunt.

### Pulsing bed
`assets/bgm/track-pulse.wav` — the original bed with a subtle 0.85Hz tremolo (depth 0.10)
and a volume ramp from 0.55× to 1.05× that plateaus 12s before the end, so the final hook
and CTA ride the peak; 0.8s tail fade. Baked with ffmpeg rather than mixed live so the
render stays deterministic; timeline `data-volume` unchanged at 0.1.

### New SFX cues (existing asset vocabulary, no new assets)
click-soft on the beat-3 hero keyword and the beat-5 grid snap; whoosh-short on the beat-4
inflammation flip and the beat-6 neon CTA reveal. Existing cues re-anchored: click at the
key turn, sparkle at the output glyphs, chime at the S004 citation, whoosh out at the end.

### Timeline (63.15s)
```
1 Hook        0.000 –  5.970
2 Identity    5.970 – 18.231
3 History    18.231 – 28.831
4 Mechanism  28.831 – 42.150
5 Fibroblast 42.150 – 50.650
6 CTA        50.650 – 63.150   (follow VO at 59.18)
```

### Round-6 render QA — `renders/pdrn-cellular-science_2026-08-29_16-46-31.mp4`
**63.15s · 6.3 MB.** `npm run check` clean, 31/31 contrast. Rendered-audio transcript
matches the script word-for-word at the new tempo ("Whew" included this time — the faster
read gives whisper a cleaner segment boundary). Click hunt: clean across the full 63.15s.
Frame checks: hero keywords render alone before the panel arrives; the panel with all
governed rows + both citations + coda verified at settle; neon key clearly visible against
both the inflamed and calm washes; claim reveals line-by-line in beat 2; follow line
present at the close. Near-empty runs are beat-boundary openings only, all ≤1.5s — the
tightest of any cut.

---

## Round 7 — the 0:17 scratch, finally found and killed

The operator flagged ~0:17 in three successive cuts; every whole-file click hunt reported
clean. The defect was real: **a 9652-RMS spike in the final 25-50ms of the processed
02.wav** — a `silenceremove` edge artifact sitting after the word "response." had decayed
to near-silence, landing at 17.2s on the timeline.

Two detector blind spots let it survive:
1. The click hunt requires a *quiet neighborhood* (±15ms RMS < 900) around a jump — the
   spike's own energy disqualified its window. An artifact loud enough is invisible to a
   detector that assumes artifacts are quiet.
2. The tail checks sampled the last 5ms — the spike sat 25-50ms before EOF with clean
   samples after it.

**Diagnosis method that worked:** per-stem decomposition (mix vs VO stem vs BGM bed) with
a 100ms RMS + first-difference (HF-emphasis) profile over the flagged window — the burst
appeared identically in mix and VO stem, clearing BGM and SFX in one step. Then a 25ms
tail envelope made it unmistakable.

**Fix:** 02.wav truncated to 11.190s ahead of the spike with a 60ms fade (tail peak now
98); a tail-artifact scan across all seven processed blocks found no other instance;
`el-02-voice` duration synced. Beat timings unchanged — the 71ms lands in the settle hold.

**Standing addition to the audio gate:** after any `silenceremove`/`atempo` processing,
scan the final 100ms of each output for post-decay spikes (quiet→loud→quiet tail shape),
and run the click hunt *without* the quiet-neighborhood filter on the last second of
every block.

---

## Round 8 — SFX layering + seamless loop close (61.00s)

### SFX (0:18–0:40)
Four new subtle UI clicks (existing `click-soft` asset, 0.22–0.25 vol): hero line 2
(19.73), the CITATION+UNSOURCED landing (24.28), the mechanism card arrival (28.95), and
the mechanism CLAIM row (39.83). The key's lock click moved to **exactly 38.000** per the
directive — mid-snap of the turn, reading as the lock engaging. The flip whoosh at 38.38
stays.

### Loop close (replaces the follow CTA)
- Removed: the follow VO and its on-screen line (frame 6 element + tween deleted).
- Added: `assets/voice/08-loop.wav` — Kimberly, "And that's why…", trailing delivery,
  0.98s, at 59.25 (0.4s after "…a step too far?"). The generated take carried 1.8s of dead
  head air; trimmed, de-clicked, tail-faded, and passed the post-decay tail-spike gate.
- Beat 6 shortened to 10.35s; total runtime **61.000s**. The wrap: "…and that's why—" →
  (loop) → "People are applying salmon DNA to their skin", question → answer.
- **BGM re-baked for the seam**: the momentum ramp now returns to its opening level
  (0.55×) over the final 0.8s instead of fading to zero, so the bed's level matches
  across the loop point. The closing whoosh sits at 60.28, bridging into the opening
  impact-bass on replay.
- The neon question holds as the final frame; frame zero's composed salmon/vial stage is
  the visual re-entry.

---

## Round 9 — CTA restored, loop kept (63.78s)

The follow CTA returns — VO (`07-follow.wav`, the existing processed take, at 59.20) and
the on-screen line beneath the citation (revealing at 59.35). The loop close stays as the
**final** element so the seam still wraps: the ending now runs

> …or is this skincare trend a step too far? Let me know your thoughts below and follow
> for more. And that's why— → (loop) → People are applying salmon DNA…

`08-loop.wav` moved to 62.15 as its own timeline element; beat 6 is 13.13s; total
**63.780s**. BGM re-baked at the new length with the same loop-matched seam level
(returns to 0.55× over the final 0.8s); closing whoosh at 63.06.

### Round-9 render QA — `renders/pdrn-cellular-science_2026-08-29_17-32-24.mp4`
**63.8s.** Ending transcribes "…a step too far? Let me know your thoughts below, and
follow for more. And that's why…" — CTA restored, loop line last. Burst scan clean. First
render of this round had the follow line's last glyphs grazing 12px into the right rail
(9 ink hits at x918-930); type stepped 2.8→2.55cqw and the re-render audits 0/0 in both
reserved zones.

---

## Round 10 — loop line removed (62.66s)

`08-loop.wav` element deleted; the video now ends conventionally on the CTA:
"…a step too far? Let me know your thoughts below and follow for more." Beat 6 tightened
to 12.01s (0.85s settle after the CTA); total **62.660s**. The seamless-loop mechanism
from round 8 is retired with it, so the BGM was re-baked with a normal 0.8s tail fade in
place of the loop-matched seam level; closing whoosh at 61.94.

Render `…17-43-20.mp4`: ending transcript verified, burst scan clean across 62.66s.

---

## Round 11 — external QA report triage (62.2s delivery master)

Four findings measured against the actual file before acting. Two were real, two refuted
with pixels; the "could not verify" delivery-spec list was measured and one real failure
(loudness) fixed.

| # | Claim | Verdict | Evidence / action |
|---|---|---|---|
| 1 | Citations/CTA "deep in the bottom 20%" (0:21–0:51) | **Refuted** | Ink audit at 6 frames across the window: 0 pixels below y=1536 AND 0 below the 1080×1350 safe line (y=1635). The referenced "Below ~50% humidity…" text does not exist in this project (grep: no match) — likely another video's review. |
| 2 | Continuous hiss under the VO | **Real — root-caused narrower** | Stems measured: blocks 1–4,6 floor −83…−94 dBFS (clean); **block 5 = −58.2 dBFS** (operator-supplied lossy MP3 source) and follow line −74.9. `afftdn=nf=-25` applied to those two stems only: −68.8 / −91.8 dBFS. Blocks already at −85+ left untouched — denoising clean stems risks artifacts for nothing. |
| 3 | Disclaimer covered by Shorts UI | **Refuted / adopted alternative** | No disclaimer exists on-screen anywhere (grep: no match). Their own fallback adopted: "General skincare education — not medical advice…" added to the PUBLISH.md description draft. |
| 4 | Hook static for 5s | **Partly real** | The hook is an animated extraction from 0.28s (was 0.40) and frame zero is composed — not static. But the settle hold was halved (1.0→0.5s), so the Ingredient Identity card now lands at **5.47s**. It cannot land at 0:03 while the hook line is spoken — that would cut narration, which is an operator call. |

**Delivery specs measured and locked** (`renders/pdrn-cellular-science_DELIVERY_-14LUFS.mp4`):
1080×1920 · H.264/yuv420p · 30fps CFR (r=avg) · bt709 (space/primaries/transfer) · AAC
48kHz stereo. Loudness was the one real failure: **−21.2 LUFS** → normalized to
**−14.2 LUFS integrated / −1.4 dBTP** via two-pass linear loudnorm, video stream copied.
Two loudness passes were needed beyond the first: AAC codec overshoot regenerates ~0.3dB
above the encoded peak, so hitting ≤−1 dBTP post-codec requires targeting ≈−1.6 in PCM.

Timeline: hook trimmed −0.5s; everything after beat 1 shifted uniformly (word-sync
preserved by construction — beat-internal cues untouched). The lock click still rides the
key turn, now at 37.5s absolute. Total **62.16s** (delivery file 62.28 with AAC padding).
Render QA: full-script transcript verified, burst scan clean, beat-5 mix floor now
−30.3 dBFS (that's the deliberate BGM bed, not noise).

---

## Round 12 — second external QA report: safe areas, marker legibility, captions, disclaimer (62.16s)

Four findings, all verified against `…17-43-20.mp4` pixels before acting; all four real
(unlike the round-11 report, which was half phantom). Timestamps below in the reviewer's
62.66s frame of reference; the fixes land on the round-11 timeline (−0.5s hook trim).

| # | Finding | Action |
|---|---|---|
| 1 | **MAJOR** — follow CTA line at ~y1508 (78.5%), under the Shorts title/description overlay | `06-cta` stage lifted 384→300 and compacted (diagram 860→810, margins trimmed); citation pill now settles ~y1320, follow line ~y1390 — both above the y=1440 (75%) line. Round 9's "0-ink" audit only enforced the bottom-15% zone; the reviewer's threshold is stricter and is now met. |
| 2 | UNSOURCED / CITATION markers small + low-contrast | All `.uc-unsourced` 2.6→**3.4cqw** (28→37px) and rgba-ink 0.62→**0.85**; all `.uc-citation-pill` 2.6/2.8→**3.4cqw**. Not the full +50%/40pt the report asked: at 3.9cqw the beat-3 card (every governed row + coda, non-removable per round-6 ruling) breaks the y=1440 floor. 3.4cqw + darkened ink was the max that keeps every governed row rendered and safe-area-clean; the 40px accessibility bar is carried by the captions instead. Beat-3 hero/card lifted + compacted to absorb the growth (hero 6.4→6.0cqw, card top 580→492). |
| 3 | No burned-in captions | 33 caption cues added at root (`index.html`, track 5): whisper word-timed per stem (same processed takes), one phrase per clip, framework-toggled (no tweens). Ink pill / paper text, Inter 800 40px, top band y196–330 — the only strip clear of scene content in all six beats; the reviewer's y65% suggestion would sit captions on the claim cards and cover governed rows. Frame zero carries no caption (first cue at 0.07s). |
| 4 | Medical-claim compliance risk (burns/grafts/ulcers VO) | On-screen disclaimer "Illustrative purposes only. Consult a dermatologist." added to `03-history` at y1452, revealing with the panel (3.9s in — the claim window) and holding to beat end. Complements the "not medical advice" line already in the PUBLISH.md description. |

Render `…18-12-47.mp4` (62.16s): `npm run check` clean (0 errors, 33/33 contrast).
Frame QA at 0 / 1 / 8 / 14.5 / 24.5 / 26.5 / 40.5 / 55 / 60 / 61.8s: captions legible and
clear of the right rail, markers read at arm's length, disclaimer present through the
claim window, CTA close fully inside y<1440, frame zero unchanged and caption-free.

Delivery master re-cut: `renders/pdrn-cellular-science_DELIVERY_v2_-14LUFS.mp4` —
**−14.35 LUFS integrated / −1.56 dBTP post-AAC** (gain +9.8dB into a true-peak limiter at
−1.8dB; pure linear gain caps out at −15.1 against the TP ceiling). Video stream copied
from the render; AAC 256k 48kHz.
