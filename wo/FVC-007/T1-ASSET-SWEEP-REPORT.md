# T1 — Asset sweep and voiceover extraction

Deliverables:

- [`docs/wo/007/asset-inventory.md`](../../docs/wo/007/asset-inventory.md) —
  the per-plate table T1's own text asks for.
- [`videos/kbeauty-one-percent-line-v2/vo/source-vo.wav`](../../videos/kbeauty-one-percent-line-v2/vo/source-vo.wav)
  — the fixed-variable voiceover track, assembled and hashed (below).

Run in its own worktree (`session/fvc-007-t1`), branched from master at
`2361302` (after T3's merge). Held from merging per instruction, same as T5.

---

## 1. Asset sweep — method and scope

T1's own text scopes this to "every already-rendered plate from the
centella and PDRN runs." Read literally: every `videos/*` project whose
slug contains `centella` or `pdrn`, plus `madecassoside-*` (Centella
asiatica's active compound — same ingredient family, same likely plate
reuse). Eight projects swept:

`centella-asiatica`, `centella-barrier-recut-15s`, `centella-cica-vs-snail-mucin`,
`centella-tiger-grass`, `madecassoside-clinical-cut`, `madecassoside-flat-matrix`,
`pdrn-cellular-science`, `pdrn-left-the-clinic`.

Five of the eight (`centella-asiatica`, both `madecassoside-*`, both
`pdrn-*`) turned out to hold **audio only** — voice/BGM/SFX/font assets,
zero images or B-roll video. Confirmed by directory listing, not assumed
from the project name. The real find is concentrated in three projects:
`centella-barrier-recut-15s`, `centella-cica-vs-snail-mucin`, and
`centella-tiger-grass`.

**This sweep does not duplicate `catalog/` (T5's own territory).** Two
plates in `centella-barrier-recut-15s` turned out to be literal duplicates
of already-catalogued files (`02-centella-asiatica.png`,
`03-flaking-skin.png` — see `catalog/ingredient-photography/` and
`catalog/skin-macro-photography/`) and are recorded as such, not
double-counted as new inventory.

### The real find: `centella-cica-vs-snail-mucin/assets/images/`

Six stills, five of them genuinely new and B-1-clean: `f1-palette.png`,
`f2-string-start.png`, `f3-dropper-start.png` (all native 1536×2752, 9:16 —
same dimensions as `catalog/product-photography`'s set, worth noting since
it suggests the same generation pipeline), `twist-centella-leaf.png`
(1400×1400 square, centella leaf on white), and `twist-cream-swirl.png`
(781×1400, whipped cream texture, near-9:16). All five verified by direct
visual inspection (not by filename guess): no faces, no real brands, no
baked-in claim text. `cta-snail-pour.png` (1400×1400, dropper into a dish)
is the sixth — same clearance, square aspect.

The project's own thumbnail files (`assets/thumbnail/*.png`) were checked
and excluded on sight: they carry baked-in headline copy ("SNAIL MUCIN OR
CENTELLA? If your skin is red and angry, stop guessing.") — thumbnails, not
B-roll, and disqualified under B-1 regardless of the clean photography
underneath the text.

### `centella-tiger-grass/assets/plates/` — real footage, not generated

14 MP4s, all native 720×1280 (9:16) or 1440×2560 (9:16 at 2K). Sampled
frames from `broll-1.mp4`, `tiger.mp4`, and `under-1.mp4` confirm this is
**real nature/wildlife footage** — dew-covered leaves, and an actual tiger
rolling in vegetation (the project's own pun: "tiger grass" is Centella
asiatica's common name) — not generated imagery. Content clears B-1 (no
human face; an animal is not a face for B-1's purposes; no brand, no
claim), but:

**Flag, not a ruling — provenance/licence is unconfirmed.** No README,
manifest, or licence note exists anywhere in `centella-tiger-grass/`.
Footage of this quality (an actual tiger) is very unlikely to be first-party
shot or generated — it reads as licensed stock. Unlike the Higgsfield
catalog plates (T5's tier 1/3, provably first-party and free), this cannot
be marked "$0, no licence" without confirming it. **Recommend: do not cast
this footage onto a beat until its licence is confirmed** — reusing
unlicensed stock in a finished video is exactly the liability B-1's own
tier-4 attribution language is written to prevent, even though this
particular footage didn't arrive through that tier.

---

## 2. Frame extraction from `cGbokt_B_vE` (T1 item 2)

Extracted 9 frames — one per scene — directly from the actual rendered MP4
(`kbeauty-one-percent-line_2026-08-29_21-40-00.mp4`, probed at 115.60s),
sampled ~1s into each scene per `STORYBOARD.md`'s own frame-start table (past
the 0.5s cross-fade each scene runs into the next). Every frame was viewed,
not inferred from the HTML source — matching this WO's own repeated
precedent (T0-GATE-A-REPORT, T2's contrast checks) of verifying from
rendered pixels rather than declared intent.

**Result: 0 of 9 usable as raw B-roll.** T1's own text predicted "most will
be typographic and unusable" — this composition is more typographic than
that framing allows for: every sampled frame is either pure type-on-color
(hook, promise, the-trick, hanbang-rapidfire) or a design-system card with
claim/label text baked directly into the same pixels as any photography it
carries (hook's bottle + "80% GINSENG?" headline; 04b's ginseng root +
caption + progress dots; teardown's INCI list card; the endcard's recap
card). None of that is a defect — these are exactly the `claim_vs_evidence`
beats B-1 already requires to be design-system-only (`broll_allowed: false`
in T3's registry) — but it does mean tier 2 contributes **zero** plates to
the sourcing pool, not "few."

One overlap worth naming: 04b's ginseng root photo is the same source image
already sitting clean (no card chrome) at
`videos/kbeauty-one-percent-line/assets/images/ingredient-ginseng.png`
(already in T5's own inventory). Extracting the composited frame doesn't
add anything tier 1 didn't already have.

Tier 2 is therefore exhausted, per G0-4's own instruction to exhaust it "at
no cost before falling through" — the cost here was nine frame extractions
and nine visual checks, and the finding is that this tier is empty for this
pilot, not merely thin.

---

## 3. Voiceover extraction and assembly (T1 items 3–4)

Per the WO's own 2026-09-07 correction: the source project is
`videos/kbeauty-one-percent-line/` itself (already 9:16, 1080×1920), and
its per-scene voiceover already exists on disk as 8 WAV/MP3 pairs at
`assets/voice/{01..08}.{wav,raw.mp3}` — using these, re-placed at the
composition's own timeline offsets, instead of extracting the published
YouTube mix (which would bake in BGM/SFX and violate R-10's single-variable
premise). No YouTube extraction was performed.

### Offsets and durations (from `STORYBOARD.md`'s own frame table, cross-checked)

| Scene | VO file | Start offset | Measured duration (ffprobe) | Matches STORYBOARD? |
|---|---|---|---|---|
| 01 hook | `01.wav` | 0.00s | 7.20s | Yes |
| 02 promise | `02.wav` | 8.20s | 7.28s | Yes |
| 03 extract-loophole | `03.wav` | 16.48s | 13.76s | Yes |
| 04 one-percent-line | `04.wav` | 31.24s | 11.60s | Yes |
| 04b ingredient-showcase | — (no VO; visual-only insert) | — | — | — |
| 05 the-trick | `05.wav` | 46.34s | 19.04s | Yes |
| 06 teardown | `06.wav` | 66.38s | 17.52s | Yes |
| 07 hanbang-rapidfire | `07.wav` | 84.90s | 19.84s | Yes (this is the corrected take — see STORYBOARD's 2026-08-29 entry on the "inky"→"I-N-C-I" respell; file mtime, Aug 29 07:23, postdates the other seven, confirming the corrected file is what's on disk) |
| 08 cta-endcard | `08.wav` | 105.74s | 6.80s | Yes |

All 8 measured durations matched `STORYBOARD.md`'s documented values
exactly — no drift between the doc and the files on disk.

### Assembly

Built with `ffmpeg`: each of the 8 WAVs delayed to its start offset
(`adelay`), mixed without gain normalization (`amix=normalize=0`, since
the clips barely overlap and normalizing by input count would quietly
attenuate the actual dialogue), then padded/trimmed to the rendered MP4's
own probed total length.

**Total duration used: 115.60s — the actual probed render duration, not
`STORYBOARD.md`'s rounded 115.54s figure.** The doc's number is a
hand-maintained approximation; the render itself is the authority T6 needs
to match, so the assembled track's length is set from that, not from the
prose.

```
ffmpeg -i 01.wav -i 02.wav -i 03.wav -i 04.wav -i 05.wav -i 06.wav -i 07.wav -i 08.wav \
  -filter_complex "
    [0]adelay=0|0[a0];       [1]adelay=8200|8200[a1];
    [2]adelay=16480|16480[a2]; [3]adelay=31240|31240[a3];
    [4]adelay=46340|46340[a4]; [5]adelay=66380|66380[a5];
    [6]adelay=84900|84900[a6]; [7]adelay=105740|105740[a7];
    [a0][a1][a2][a3][a4][a5][a6][a7]amix=inputs=8:duration=longest:dropout_transition=0:normalize=0,apad[out]
  " -map "[out]" -t 115.60 -ar 48000 -ac 1 source-vo.wav
```

### Result and ledger entry

| Field | Value |
|---|---|
| Path | `videos/kbeauty-one-percent-line-v2/vo/source-vo.wav` |
| Duration (probed) | 115.600000s |
| Sample rate / channels / codec | 48000 Hz / mono / pcm_s16le |
| SHA-256 | `ea4dc2823f21cf6601302725d23794564e73272c65c9e456b1d6092b17ce78a9` |
| Source | `videos/kbeauty-one-percent-line/assets/voice/{01..08}.wav`, unmodified except for silence-padding at their own timeline offsets — no re-synthesis, no re-levelling beyond what `amix` does structurally |
| Built | 2026-09-07, this session |

**Per T1's own instruction, this file is the fixed variable of the whole
experiment.** It is not to be regenerated, re-synthesized, or re-levelled
beyond a true-peak pass (not yet run — flagged for whoever takes this into
T6, since a true-peak pass changes gain, not content, and is explicitly
permitted). T6's rebuilt composition must match this file's 115.60s
duration to within 100ms — this duration supersedes `STORYBOARD.md`'s
115.54s figure as the actual target, since it's measured from the real
render rather than hand-maintained prose.

---

## 4. What this hands to T5 / T6

- Five clean, native-or-near-9:16 B-1 stills added to the sourcing pool
  T5 already built (`f1-palette.png`, `f2-string-start.png`,
  `f3-dropper-start.png`, `twist-cream-swirl.png`, plus the square
  `twist-centella-leaf.png` and `cta-snail-pour.png` pending a reframe
  decision) — all tier 1, all $0, all already committed to the repo.
- A real 720×1280/1440×2560 wildlife/nature footage pool
  (`centella-tiger-grass`) that clears B-1's content bar but carries an
  **unresolved licence flag** — not to be cast onto a beat until that's
  confirmed.
- Confirmation that tier 2 (extracted `cGbokt_B_vE` frames) is empty, not
  thin — T5/T6 should not expect to find anything there.
- `source-vo.wav`, hashed and ledgered, ready for T6's build without
  needing to re-derive it.

Not done here, and not this task's job: deriving `03-beat-sheet.json` from
`STORYBOARD.md` + the SRT (T6's own scope, per REVIEW.md P2) — this sweep
found the frame-start table but did not turn it into a machine-readable
beat sheet, since that's a T6 casting input, not an asset-inventory
question.
