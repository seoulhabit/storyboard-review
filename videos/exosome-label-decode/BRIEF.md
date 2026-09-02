# BRIEF — exosome-label-decode

**Title (working):** What "Exosome" on Your Serum Doesn't Tell You
**Format:** YouTube Short, 9:16, 1080×1920, 30fps
**Audience:** skincare buyers evaluating a trend ingredient at the shelf —
no clinical vocabulary assumed
**Engine:** `hyperframes@0.8.22`
**VO_MODE:** narrated (synthetic) — see § Voice

## Thesis

"Exosome" on a label names a *particle class*, not a formula, a dose, or a
result. The word itself carries no information about source, stability, or
whether the finished product was ever tested on people. Promising ≠ proven.

---

## Voice

Higgsfield `generate_audio`, model `seed_audio`, voice **Kimberly**
(`voice_id 674b71b8-1d2e-4087-8567-d1f53c0b9f3c`, `voice_type element`) —
the channel's established voice, reused verbatim rather than re-chosen.
Confirmed still live via `list_voices` before the build.

HeyGen/`hyperframes tts` sign-in is unavailable from an automation context
(no token in `~/.hyperframes/config.json`); `pdrn-cellular-science/BRIEF.md`
records the same finding and the same Higgsfield fallback. Not re-litigated.

**TTS prompt vs. on-screen text diverge deliberately.** Em-dashes in the
source script were replaced with sentence breaks in the *prompt only*, for
prosody. On-screen copy keeps the authored punctuation.

### BGM bed — how to regenerate it

`assets/bgm/bed-59.0s.wav` is derived, not sourced. The 180s master
(`track-master.mp3`, the channel's most-used bed — the identical blob already
sits in four sibling projects) has **only ~48s of live audio**: it fades from
~48s and is true digital silence past 60s. A naive 0–59s crop would have faded
the last 11s to nothing and handed the replay a dead beat, so the bed is built
by looping the live region:

```bash
ffmpeg -y -i assets/bgm/track-master.mp3 -i assets/bgm/track-master.mp3 \
  -filter_complex "[0:a]atrim=0:46,asetpts=N/SR/TB[a];\
[1:a]atrim=12:27,asetpts=N/SR/TB[b];\
[a][b]acrossfade=d=2:c1=tri:c2=tri[x];\
[x]atrim=0:59.0,asetpts=N/SR/TB,afade=t=in:st=0:d=0.2,afade=t=out:st=58.8:d=0.2[o]" \
  -map "[o]" -ar 48000 -ac 2 assets/bgm/bed-59.0s.wav
```

Kept as **WAV, not mp3** (siblings use mp3 for their derived beds — this is a
deliberate deviation): the bed feeds a `loudnorm` master that re-encodes to
AAC, and an mp3 bed would make that a double lossy encode. The cost is ~10.8MB
in the repo, which is the trade taken. Re-run the command above after any
runtime change, then re-render and re-master.

---

## Duration — reason on record

Script nominal is **48s**. Real Kimberly takes ran **~23% over** script
estimate on `pdrn-cellular-science` (60s scripted → 74.089s actual), so this
is expected to land **~55–62s**. Final runtime is VO-derived and recorded in
`STORYBOARD.md` after measurement, never authored up front.

Past 50s needs a reason (production-loop step 2). The reason:

- The deliverable **is** a three-question decision checklist. Dropping a
  question to reach 45s removes a third of what the viewer came for.
- The channel's own measured baseline finds **no duration→performance
  relationship**: age-normalized median ratio 4.38 (≤50s) vs 3.97 (>50s),
  against a within-cohort spread of 0.67–49.44. It explicitly does not
  license the inverse either.
- Top-quartile-by-performance median duration on this channel is **49.0s**
  (n=4, provisional).

So 28–45s is treated here as a **craft budget, not a threshold**.

---

## Palette — translation record

The brief supplied literal hex values. Channel `tokens.css` wins
(pre-render gate item 6, channel consistency). Every *role* is preserved:

| Brief | Channel token | Role |
|---|---|---|
| `#F4F0E8` warm ivory | `--paper #F7F5F0` | ground |
| `#171717` near-black | `--ink #131516` | primary text |
| `#B8F5CE` clinical green | `--celadon #93B896` / `--leaf #6F8F72` | evidence, vesicles |
| `#FF645F` warning coral | `--coral #C97A5C` | limitation / refusal |

Coral's documented channel role is *"a limitation or a refusal"* — which is
precisely what `EVIDENCE: LIMITED` and `MARKETING CLAIM ≠ PROOF` need. The
mapping is a role match, not a compromise.

The brief's `#B8F5CE` measures ~1.3:1 on ivory and `#FF645F` ~3.1:1 — both
below this channel's 4.5:1 floor for read text. `--celadon`/`--coral` are
used as **fills and marks behind ink text**, never as text colour on paper.

---

## Imagery decision record

Following `pilling-vs-peeling/BRIEF.md` § Round 2 § Imagery decision record.

- **Why:** the piece needs a real tactile/product anchor early (asset-protocol
  rule 6). The subject is a retail serum bottle; there is something concrete
  to show, so an all-illustrated open would be the weaker call.
- **What:** `catalog/product-photography/assets/A01-01.png` — frosted glass
  dropper bottle, `세럼 · 30mL`, 1536×2752, 9:16. **Reused, not generated.**
- **Precedent:** `videos/pilling-vs-peeling` ships four photographic plates
  inside real HyperFrames compositions (`01-hook-a.html`, `04-flaking.html`,
  `05-test.html`, `08-close.html`). The product-photography README's older
  "not HyperFrames assets" note predates that precedent.
- **Scope:** unbranded, no faces, no claims on any rendered surface. The
  label carries a category word and a volume only — it asserts nothing, which
  is what lets it sit next to a sourced claim without implying one.
- **Grade:** ground-keyed to `--paper`. Only pixels with `luma > 235` and
  `chroma < 6` are shifted; the subject is **bit-identical** to the catalog
  original (verified: max abs per-channel delta 0.0 across the bottle).
  A first attempt using a per-channel *gamma* solved against the near-white
  ground was discarded — near 1.0 all gammas converge, so a ~6/255 ground
  shift demanded exponents (R 0.56 / B 1.26) that turned the silver cap
  brass (`134,134,136` → `176,161,117`) and raised mean chroma 2.57 → 12.23.
  Recorded because the failure was invisible when sampling the ground alone.

---

## Sources

Every on-screen citation pill reads `Journal · Year` only. No PMID, no DOI,
no internal key on any frame. Full list with DOIs → `DELIVERY.md`.

| # | Claim carried | Pill | DOI |
|---|---|---|---|
| S1 | Exosome source varies (MSC, immune cell, platelet) and confers distinct molecular signatures — sources are not interchangeable | `Aesthet Surg J · 2026` | `10.1093/asj/sjaf259` |
| S2 | 17 human studies 2020–25; delivery via topical, microneedling, fractional CO₂ laser or injection; small samples, short follow-up, non-randomized single-arm designs | `J Drugs Dermatol · 2026` | `10.36849/jdd.9610` |
| S3 | 19 human studies, most non-randomized; heterogeneity and lack of follow-up; rigorous RCTs still required | `Cureus · 2026` | `10.7759/cureus.104182` |

**Scope guard, load-bearing.** All three reviews span **injected and
in-office** exosome use alongside topical. This video is about a **retail
serum**. That gap is not glossed — it is the entire point of beat 4's third
question ("was this *exact finished product* tested on people?"). No frame
claims a topical serum inherits evidence generated by an injected or
microneedled protocol.

**Plain-language check (gate 9b).** No claim sentence requires clinical
vocabulary. "Extracellular vesicle" never appears as the claim; "particles
cells release to carry signals" does. "Characterized" is glossed on screen as
"proven to be what it says." Citation pills stay terse because they are
provenance, not instruction.

---

## Beat sheet

Presenter: **hero plate + condensed type**, held across all seven scenes
(scene 7, the brand end card, was added after the first render — see DELIVERY).
Grounds alternate paper/ink → **hard cuts everywhere**; a crossfade across a
ground change produces a muddy midpoint and is structurally unsafe here.

| # | Scene | Ground | Intent (one line) | Mechanism |
|---|---|---|---|---|
| 1 | `01-hook` | paper | The word on the bottle is not the evidence | full-bleed plate + Ken Burns; `EXOSOME?` set at t=0, payoff ≤2s |
| 2 | `02-what` | ink | It's a delivery particle — and its *source* varies | SVG vesicle-release diagram + `TermDefinition` lockup · S1 |
| 3 | `03-evidence` | paper | Human evidence is real but thin, and often confounded | `EvidenceMeter`, 2 of 4 nodes · S2 |
| 4 | `04-questions` | ink | Three questions to ask before buying | **new `QuestionGate`** · S3 |
| 5 | `05-claim` | paper | "Exosome technology" is a claim, not a result | `SplitCompare`, tint floods the claim side only |
| 6 | `06-close` | paper | One specific action | lockup + CTA + 습 mark |
| 7 | `07-endcard` | paper | Channel sign-off | 습 mark + wordmark + CTA; matches scene 1 ground/hero for the loop |

**Hook.** Frame zero is composed, not mid-fade — plate at rest, `EXOSOME?`
already set. The payoff ("tells you almost nothing") lands by ~2s, inside
the retention window; the question is not left hanging for the setup.

**Loop.** Scene 6 returns to scene 1's ground and hero position so a replay
hands back cleanly. The BGM bed is re-cut to true runtime with ~200ms
declick fades at both ends — a stock tail fade authored for a longer bed
would leave the last seconds near-silent and hand the replay a dead beat.

**Closing beat** is one specific, lesson-tied action ("comment the exact
product and we'll decode its label"), not a generic subscribe card.

---

## Component check

Cross-checked against the catalog inventory read at discovery, not a fresh
search. Reused/adapted vs. built new:

| Scene | Catalog entry | Verdict |
|---|---|---|
| 2 | `TermDefinition` | **adapt** — lockup structure (name / category / definition / rule) for the text half. Single entry, no cycling; the array-cycling half of its contract is unused. |
| 3 | `EvidenceMeter` | **adapt** — 4 checkpoint nodes, staggered hollow→solid snap at 0.12s, claim + citation footnote. Skin re-derived; mechanism kept. |
| 5 | `SplitCompare` | **adapt** — bisector, two independently-targetable fields, tint floods the interrogated side only, no success colour. |
| 4 | — | **build new → `QuestionGate`** |

**`FactorConverge` rejected, deliberately.** It was the near-miss for scene 4
and is a many-to-one causal diagram (3 inputs converging on 1 outcome, fixed
triangle geometry). Scene 4's three questions are **independent sequential
gates** a viewer applies in order — no convergence, no shared outcome node.
`ThresholdList` (ranked list split by a cutoff) and `SplitCompare`
(two-thing bisector) don't fit either. Forcing any of them would be a
category error, so scene 4 is built new and harvested back per step 12.

**Reused imagery:** 1 plate (above). **Newly generated imagery:** none.

---

## Type & legibility

Channel floors, from `assets/tokens/tokens.css`: hero 96px, figure 60px,
frame 50px, body 40px (reading floor), label/chip 32px (absolute floor for
anything meant to be read). Nothing below 32px carries content.

Contrast is verified per **ground**, against actual rendered pixels — not
tokens. `--ink-2` on paper, `--ink-2-dark` on ink. (A prior project recorded
"16/16 passed" while reusing a paper-scoped token on an ink ground at
3.44:1; the token's documented scope is a constraint, not a comment.)

---

## Safe areas

`--safe-top 192` / `--safe-bottom 384` / `--safe-right 162` / `--safe-left 72`,
`--safe-margin 6`. Every scene consumes the tokens; no scene hardcodes an
offset. Any scene with a Ken Burns scale uses the **derived**
`--safe-*-zoomed` values (already in `tokens.css`, including the top/left
inversion for an off-centre origin) rather than a hand-tuned `+Npx`
allowance, which goes stale the moment the token or the scene's scale changes.

Verified against the render, not the source — a source-level audit
structurally cannot see a transform-induced overshoot.
