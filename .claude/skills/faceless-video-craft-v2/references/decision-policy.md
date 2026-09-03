# Decision policy — the rulebook

Every fork in the pipeline is listed here with four fields: **reads** (the data
it consumes), **rule** (how the value is chosen), **default** (what happens when
the data is missing), and **ledger** (the line written to
`00-decision-ledger.md`). If a fork is not in this file, it is not a decision
the pipeline may make silently — add it here first, with a rule, then run.

Numbers marked **[baseline]** are read from `channel-baseline.md` when it is
populated. Numbers marked **[default]** are starting values for a channel with
no history; they are replaced by measured ones after the first readouts. Do not
treat a default as a fact about YouTube — treat it as the pipeline's opening
position until the channel's own data overrides it.

Six rules carried over from v1 are reproduced **verbatim** in
`references/restored-v1-rules.md` and referenced below by their policy id. Each
has a confirmed shipped defect behind it; the wording is not paraphrased,
because a filed-down rule stops catching what it was written for.

Ledger line format, one per rule fired:

```
[S2/T-2] topic gate → PASS | seed "niacinamide barrier repair" overall=61 (≥50) | vidiq_keyword_research
```

---

## S0 — Baseline

**B-1 · Do we have a channel baseline?**
- reads: `channel-baseline.md`
- rule: if `populated: false` or older than 30 days → run S0 fully (runbook §S0) before anything else. Otherwise skip S0.
- default: none needed.
- ledger: `[S0/B-1] baseline fresh (updated YYYY-MM-DD) → skip` or `→ refresh`.

**B-2 · Which channel?**
- reads: `vidiq_user_channels`
- rule: if exactly one authorized channel → use it. If several → use the one named in the project skill or the run input; else **HALT: BLOCKER-CHANNEL**.
- ledger: channel id + handle.

**B-3 · Traffic schema must be able to describe this channel**
- reads: `vidiq_channel_analytics(report=traffic_sources)`
- rule: the baseline's traffic block records **every** returned source type, including the Shorts feed. A four-slot `browse / suggested / search / external` schema cannot represent a Shorts channel — on this channel the Shorts feed alone is 88.1 % of views and has no slot in that schema. Record whatever the tool returns, with its own labels, plus a `shorts_feed_share` field.
- default: `not available via vidIQ` per missing source.
- ledger: source shares as returned, and which schema slots were empty.

---

## S1 — Story

**S-1 · Format (long 16:9 vs short 9:16)**
- reads: run input; `channel-baseline.md` → `formats.short.uploads_90d` and `formats.long.uploads_90d`, then the story brief's shape
- rule (in order):
  1. Run input names a format → use it.
  2. **The baseline's dominant format by `formats.<fmt>.uploads_90d`, when one format holds ≥ 60 % of `corpus.uploads_total`** → use it. What the channel actually publishes outranks what one brief looks like; a channel that is 46 of 48 Shorts does not want a long-form default because a single brief happened to fill six sections.
  3. Brief has ≥ 4 of the 6 spine sections with distinct content → **long**.
  4. Brief is a single claim + single mechanism → **short**.
  5. Tie → whichever format's median views/upload is higher in baseline.
- default: baseline empty → **short**. (v2 defaulted to long. Reversed: the pipeline is aimed at Shorts-first channels, and a short that should have been long is a cheaper mistake than the reverse.)
- ledger: format + which branch fired + the uploads_90d share that drove branch 2.
- **first-of-kind override (branch 1 against a ≥ 60 % dominant format).** Branch 1
  already wins on an explicit operator format; what this note adds is what that
  costs when the chosen format has **no prior art on the channel or in the repo**.
  Do not treat it as an ordinary branch-1 pass:
  1. Ledger it as an override, naming the share it overrode (e.g. "long, operator
     override; branch 2 would have selected short on 46/48 = 95.8 % Shorts").
  2. Every `curve.*` and `retention.*` figure in the baseline was built from the
     *other* format. Ranking this run against them is a category error — mark any
     such comparison `[UNDERPOWERED]` or omit it, and say which in the ledger.
  3. Format-specific gates must be re-pointed, not inherited. Safe-area zones,
     cadence ceilings and QC canvas constants are all per-format; a portrait-
     calibrated gate run against a landscape render is confirmed to report a
     **silent clean pass** (see `youtube-delivery.md` §Long-form safe areas).
  4. `[S3/P-3]` changes behaviour: long-form generates and scores a thumbnail,
     where Shorts use frame 0. Do not carry the Shorts branch across.
  5. Prefer proving the format on a short vertical slice before committing a full
     runtime of voiceover and scenes. A first-of-kind format is a pipeline
     hypothesis, not just a longer version of the same run.

**S-2 · Target length** — per format, and never on a replay-inflated metric
- reads: format; `channel-baseline.md` → `retention.avg_view_pct_long`, `curve.p50_7d`, per-video views and durations

- rule, **long**: target = median duration of the channel's top-quartile videos
  **by avg-view-%** [baseline], clamped 4:00–12:00. [default] 6:30.

- rule, **short**: target = median duration of the channel's top-quartile videos
  **by `views ÷ curve.p50_7d`** [baseline] — *not* by avg-view-%. Clamped 30–58 s.
  [default] 45 s.
  avg-view-% counts replays: 6 of 34 shorts on this channel exceed 100 %, one at
  603.86 %, so a shorter video scores higher mechanically and the override
  ratchets target length down on every readout. Measured on this channel the
  avg-view-% quartile median is **19 s** — below this rule's own clamp floor.

- rule, **both**: if the measured value falls outside the clamp, log
  `baseline-below-clamp` (or `-above-clamp`) with the measured number and use
  **the clamp bound**. A measurement that would defeat its own rule is recorded,
  not obeyed.

- **The clamp is a target for new work, not a diagnostic for existing work.** A
  published video whose length sits outside the clamp is not thereby a finding.
  Measured counter-example: the 2026-09-01 target is 72 s (outside 30–58) and
  its control `cGbokt_B_vE` is 116 s (further outside) and outperforms it 10×.
  Duration has no discriminative power on this channel and may not be cited as
  a cause in an S9 diagnosis.

- ledger: seconds, source, clamp status, and whether `baseline-below-clamp` fired.

**S-3 · Presenter (what carries attention)**
- reads: brief content type
- rule: mechanism-heavy (process, pathway, how-it-works) → **moving diagram**; comparison/number-heavy → **data object**; vocabulary/definition → **kinetic type**; physical/product subject with usable plates → **photographic plate**. One presenter per video, no switching.
- default: kinetic type.
- ledger: presenter + trigger.

**S-4 · Voice**
- reads: project skill voice setting; `channel-baseline.md` → `voice.id`
- rule: project skill voice → baseline voice → first English voice returned by `vidiq_voiceover_list_voices` whose name contains "neutral"/"narrator", else the first returned. Once chosen for a channel, write it to baseline and never rotate.
- ledger: voice id.

**S-5 · Spine completeness gate**
- reads: brief
- rule: all six spine sections must have ≥ 1 sentence of distinct content. If a section is empty, generate it from the input material; if it cannot be grounded in the input, mark `[UNGROUNDED]` and reduce the video to a **short** on the sections that are grounded (re-fires S-1 branch 4). Never fabricate proof.
- ledger: sections grounded / generated / dropped.

---

## Claims — `K-*`

A cross-stage family: it fires at S1, constrains S4, gates S6, and is checked on
pixels at S7. It carries its own letter rather than a per-stage one so `grep K-`
finds all of it at once.

**This is a floor, not a delegation.** `SKILL.md` says truth rules belong to a
project skill. A project skill may be **stricter** than `K-*`; it may not be
looser, and its absence is not license to skip. v1 stated this in prose and left
the rule unwritten; v2 deleted the prose; the 2026-09-01 dry run halted here
(`BLOCKER-CLAIM`) because there was nothing to apply. This is that rule.

### K-1 · Claim inventory — before the script, not after

- reads: the six-section spine from `[S1/S-5]`; the project's own `frame.md`
  §Sourcing if it has one; `catalog/ingredients/`
- rule: list **every assertion the video will make**, one row each, and classify
  it. Write the table into `01-story-brief.md` §Sourcing, in the shape
  `videos/peeling-not-progress/frame.md` already uses — **on-screen chip |
  backing | what it actually supports**. No claim enters S4 unclassified.

| Class | What it is |
|---|---|
| **nominal** | Identity or definition, asserting no effect — name, Korean name, category, origin, constituent chemistry. |
| **sourced** | An efficacy, mechanism, safety or protocol claim carrying a real externally-verifiable identifier **the author has actually read**: PMID, DOI, CFR / regulation code, or `Journal · Year`. |
| **unsourced** | The same kind of claim, with no such identifier. |
| **illustration** | A drawn diagram of an unmeasured process. |
| **editorial** | Hook framing, legend, opinion, second-person address — asserts no outcome. |

- **An identifier you have not read is not a source.** The exemplar is
  `videos/peeling-not-progress`: a dedicated pass fetched and confirmed every
  citation URL live, and **two claims required rewording before build "because
  the brief's original wording said the opposite of the cited regulator."** That
  is what sourcing is for. A chip attached to an unread paper is decoration, and
  its claim is `unsourced`.
- **`ING-*` and other internal catalog keys are not sources and never render.**
  A real record behind them still has to produce a human-readable chip.
- default: unclassifiable → **`unsourced`**. Never `sourced` by assumption.
- ledger: counts per class, plus the sourced : unsourced ratio across Mechanism
  and Proof.

### K-2 · What may render, by class — the gate

| Class | May render as |
|---|---|
| **nominal** | Plainly. No flag, no chip. |
| **sourced** | Plainly, with a human-readable citation chip (`PMID 7544967`, `21 CFR §333.350`, `Arch Dermatol · 1995`). Never the internal id. |
| **unsourced** | Only under all three conditions below. |
| **illustration** | With `[Authored, illustrative — not a claim]`, and it may not borrow chart grammar — no axes, gridlines, or plotted points implying a measurement that does not exist. |
| **editorial** | Plainly, subject to the absolute-language prohibition below. |

An **unsourced** claim may render only if **all three** hold:

1. **Attributed, not asserted.** The sentence names it as someone else's claim —
   "is *described as*", "is *said to*", "*is claimed to*" — never as fact. This
   binds the on-screen type, not just the voiceover (see `K-3`).
2. **Flagged, concurrently.** An UNSOURCED flag is on screen *while* the claim
   is, not before or after. Muted ink, **never the accent colour**, never
   citation typography — a flag that borrows the accent reads as a citation.
   Component: `catalog/visual-components/unsourced-flag/`; the `flag` beat role
   in `scripts/beats_to_composition.py` emits it.
3. **Not in the hard-prohibited set.**

### K-2a · Hard prohibitions — no flag rescues these

These do not render, sourced-or-not-flagged. If the claim cannot be moved to
**sourced**, it is **cut**, and the spine section is rebuilt from what remains —
which re-fires `[S1/S-5]`, whose `[UNGROUNDED]` path then applies.

- **Unsourced safety claims** — scaled to risk, not to keyword. What is safe to
  put on a body; dosing or frequency **of an active** (acid, retinoid,
  prescription, anything with a warning label); "safe for" a condition,
  pregnancy or an age group; "won't irritate"; contraindications; or starting or
  stopping treatment for a diagnosed condition. A low-risk usage instruction for
  a non-active ("apply the moisturiser daily") is **not** this bullet — but it is
  still an unsourced claim under `K-2` and still needs attribution and a flag.
  The test is harm from getting it wrong, not whether the sentence contains a
  frequency. (Calibrated against the 2026-09-01 dry run, whose "Start cica,
  daily, on damp skin" the first draft of this rule would have cut outright.)
- **Treats / prevents / cures a named medical condition.** Regardless of flag.
- **An unsourced quantity.** A percentage, a count of days, an "n× more". This is
  the standing "no invented numbers" rule applied to the rendered frame; a number
  on screen reads as measurement whatever sits beside it.
- **Comparative superiority** over a named alternative ("better than retinol").
- **Absolute language** — *guaranteed, instantly, proven, always, useless,
  clinically proven, doctor-approved*. Restated here as a claim class because v1
  found it shipping in a hook line where no citation pill was attached and it
  still read as one.

### K-2b · The ratio limb — when everything is unsourced

- reads: `K-1`'s counts for the Mechanism and Proof sections
- rule: if **unsourced ≥ sourced** in those two sections, the video **may not
  present as an explainer of how the thing works**. It takes the
  **disclosure-forward** form instead: the absence of sourcing is stated in the
  narration, not only badged — the video's subject becomes what is claimed *and*
  what could actually be verified. Log `disclosure-forward`.
- **Why a limb and not just a flag.** A rule that only says "flag it" produces a
  video where every substantive sentence carries a badge, and a badge on
  everything is wallpaper. Measured case: `videos/centella-tiger-grass` had
  **zero** sourced claims and four flagged unsourced efficacy claims, and its
  Round 5 pass deleted the flags while keeping the claims — the disclosure layer
  was the first thing to go precisely because it was doing all the work alone.
- worked example: the 2026-09-01 dry run
  (`outputs/2026-09-01-how-to-repair-skin-barrier/`), whose narration says "No
  source record exists in this system for any of that, so it is flagged here,
  not cited." That is the sanctioned shape.
- ledger: `disclosure-forward` fired or not, with the two counts.

### K-3 · Claim language in script and captions

- reads: the K-1 table; `[S4/V-1]`
- rule: the attribution verb from `K-2`(1) appears in **both** the voiceover and
  the on-screen type. **The on-screen wording must hedge at least as far as the
  voiceover does** — a caption that drops the hedge is the defect, because
  88.1 % of this channel's views come from the muted-first Shorts feed, so the
  on-screen sentence is the claim most viewers actually receive.
- Plain language: the claim sentence must be actionable by the project's own
  stated `audience:` without clinical vocabulary. A citation chip beside an
  already-plain sentence is the sanctioned pattern; a claim sentence written in
  clinical shorthand is not (v1, *What must never reach a rendered frame*).
- ledger: attribution verb used, and any claim reworded to satisfy this.

### K-4 · The rendered-claim check — on pixels, at S7

- reads: the extracted frames from `[S7/R-2]`; the K-1 table
- rule: the classification has to survive to the pixels. `hyperframes check` has
  no notion of a claim and cannot do any of this — it is a reading gate, like the
  hero-visual clause in `[S6/A-7]`. On the frames, confirm:
  - every frame carrying an unsourced claim shows its flag, **concurrently**;
  - the flag is not in the accent colour and is not set in citation typography;
  - no internal record id (`ING-*` or equivalent) appears anywhere;
  - the on-screen wording hedges at least as far as the VO at that timestamp;
  - no hard-prohibited claim appears.
- Any failure is a `BLOCKER-CLAIM`, not a warning. Cap: 2 fix cycles.
- ledger: frames checked, per-claim verdict.

### K-5 · The envelope carries the sourcing posture

- rule: `07-publish-envelope.md` states, in the description and in the pinned
  comment, which claims are unsourced. A disclosure that exists only inside the
  video is not a disclosure to anyone reading the page. Where `disclosure-forward`
  fired, the description says so in its first three lines.
- Nothing here changes `[S8/E-1]`: the envelope is a draft until the operator
  clicks.

---

**S-7 · `faceless-explainer` route interview — pre-answered**

The shipped `/faceless-explainer` route (`skills/hyperframes/references/routes/
faceless-explainer.md`) asks four things. v2.1 runs the route; it does not run
the interview. Each field is resolved from data already in hand:

| Route field | Resolved from | Rule |
|---|---|---|
| **angle** | story brief shape | Six-section spine with a named wrong belief → `concept`. Ordered steps the viewer performs → `how-to`. ≥ 3 parallel items → `listicle`. A single case followed through time → `narrative`. Tie → `concept`. |
| **length** | `[S1/S-2]` | The already-resolved target seconds. The route's 30–90 s sweet spot is advice, not a gate; `[S1/S-2]`'s clamp wins and the divergence is logged. |
| **destination** | `[S1/S-1]` | short → 9:16 (Shorts/TikTok). long → 16:9 (YouTube). 1:1 is never selected by this pipeline; the channel has no feed placement that uses it. |
| **`VO_MODE`** | run input | Only asked when a script was pasted. Script supplied verbatim in the run input → `use it verbatim`. Script generated by `[S4/V-1]` → `restructure per scene`. |

- default: the table is total — every branch resolves. If the route asks
  something not in this table, that is a `[NOT IN SKILL]` line and a **HALT:
  BLOCKER-ROUTE**, not an improvised answer.
- ledger: `[S1/S-7] route faceless-explainer → angle=concept | length=45s | destination=9:16 | VO_MODE=n/a (no pasted script)`.

**S-8 · Route pitch round**
- reads: the route's `pitch-round` requirement (`message` + `angle`).
- rule: the pitch round exists so five tellings of one topic are recognised as
  five different videos. Generate the five, then select by `[S2/T-4]`'s
  `title_shapes[]` — the telling whose shape matches the highest-`breakoutScore`
  shape from the channel's own outlier set wins. No operator vote.
- default: if T-4 returned no shapes, keep the angle from `[S1/S-7]`.
- ledger: five messages, the shape each maps to, winner and its breakoutScore.

---

## S2 — Topic gate

**T-1 · Seed keyword**
- reads: brief hook + mechanism
- rule: seed = the shortest noun phrase a viewer would type that names the mechanism (2–5 words, no brand names unless the brand is the subject).
- ledger: seed.

**T-2 · Search demand**
- reads: `vidiq_keyword_research(mode=research, keyword=seed, country=US)`
- rule: PASS if `overall ≥ 50` **or** (`volume ≥ 40` and `competition ≤ 60`). Else take the highest-`overall` related keyword whose meaning still matches the brief; if that passes → adopt it as seed (log the swap). If none passes → T-3 decides.
- default: if the tool is unavailable → mark `not available via vidIQ`, PASS provisionally, flag in ledger.
- ledger: seed, volume, competition, overall, PASS/SWAP.

**T-3 · Browse evidence (outliers)**
- reads: `vidiq_outliers(keyword=seed, contentType=<format>, publishedWithin=sixMonths, minSubscribers=0, maxSubscribers=max(10 × channel subs, 10_000), limit=20)`
- rule: PASS if ≥ 1 result with `breakoutScore ≥ 3` [default].
  **Both bounds are explicit and both are logged.** `10 × subs` alone gives 80
  on an 8-subscriber channel, and an outlier search capped at 80-subscriber
  channels returns nothing usable; the `10_000` floor is what makes the search
  answer a question. `minSubscribers = 0` is stated rather than omitted so the
  ledger records that small channels were *not* excluded.
  If T-2 failed and T-3 passes → topic proceeds on browse evidence. If both fail
  → **reframe**: rewrite the hook as the question form with highest volume from
  `vidiq_keyword_research(mode=questions, keyword=seed)`, re-run T-2 once. If
  still failing → proceed but tag the video `experiment` in the ledger and cap
  the credit budget at 50 % for S3.
- ledger: both subscriber bounds as sent, top 3 outliers (title, breakoutScore, subs), verdict.

**T-4 · Title-pattern harvest** (informs S3 and S-8, no gate)
- reads: the T-3 result set
- rule: extract the title *shape* of the top 5 by breakoutScore (question / number / contrast / "why X" / "X vs Y"). Store as `title_shapes[]`. Do not copy titles.
- ledger: shapes list.

---

## S3 — Packaging

**P-1 · Title**
- reads: `title_shapes[]`, seed, `vidiq_score_title`
- rule: generate 5 candidates, each using a different shape from T-4, each
  containing the seed keyword within the first 60 characters, ≤ 70 characters.
  Score all five **once**. Selection is by T-4 shape rank; the score is logged,
  not obeyed. **Cap: 1 round, 5 scoring calls.**
- **Why the scorer does not decide.** On this channel `vidiq_score_title` has no
  demonstrated discriminative power: it scored the *failing* 2026-09-01 target
  **95**, above all three diagnosis-driven rewrites (93 / 90 / 87), and the
  2026-08-31 run found the same inversion on a different video (failing title
  94, rewrites 83–87). Two runs, two videos — which is `[S9/L-2]`'s own
  "contradicted twice in a row" bar. The old rule's ~10 calls (~50 credits) buys
  a number that points the wrong way; 5 calls buys the same information for half
  the credits and is kept only as a logged signal for L-2 to keep watching.
- default: no T-4 shapes → pick the candidate whose first 40 characters carry
  the mechanism, not the category.
- ledger: all candidates with scores, the shape each used, winner, why it won,
  and whether the highest-scoring candidate was the winner (an inversion is
  itself evidence for L-2).

**P-2 · Thumbnail concept**
- reads: presenter (S-3), winner title, `vidiq_similar_thumbnails(description=<concept>, limit=20)` for saturation
- rule: concept = frame-zero composition + ≤ 3 words of overlay text that are **not** in the title. If similar-thumbnail search returns ≥ 10 near-identical concepts in the last six months → pick the second concept variant (swap the visual metaphor, keep the words).
- ledger: concept, saturation count.

**P-3 · Thumbnail generation + score**
- reads: `vidiq_generate_thumbnail(title, userQuery=<concept>, orientation)`, then `vidiq_score_thumbnail`
- rule: generate 1, score. If `< 70` [default], `vidiq_refine_thumbnail` once with the scorer's top improvement, re-score, keep the better. **Cap: 1 refine.** Long-form only; **Shorts use frame 0 as the thumbnail** (no generation, no score) — which is why `[S6/A-3]` treats frame zero as a composed design object.
- ledger: scores, which version shipped.

**P-4 · Description, tags, chapters**
- reads: brief, seed, T-2 related keywords
- rule: description = hook sentence + 2-line summary + chapter timestamps (from S5) + source list from the brief + pinned-comment question. Tags = seed + up to 9 related keywords with `overall ≥ 30`. Chapters come from the beat sheet (see S5 C-1), never written by hand here.
- ledger: tag count, related keywords used.

---

## S4 — Script and voiceover

**V-1 · Script length from target length**
- reads: S-2 target seconds; `channel-baseline.md` → `voice.words_per_minute` [default 150]
- rule: word budget = target_seconds × wpm / 60, ±10 %. Allocate by spine split (S-6). Write the script to the budget. Captions = the script, sentence-chunked, ≤ 42 characters per line, ≤ 2 lines per beat.
- ledger: word budget, actual words.

**S-6 · Spine time split**
- rule [default], as % of runtime:

| Section | Long | Short |
|---|---|---|
| Hook | 0–8 % (max 20 s) | 0–10 % (max 3 s) |
| Misconception | 8–18 % | 10–25 % |
| Mechanism | 18–55 % | 25–65 % |
| Proof | 55–75 % | 65–85 % |
| Application | 75–90 % | 85–100 % |
| Recap + end scene | 90–100 % (end scene ≥ 8 s, ≤ 20 s) | — (last beat loops to frame 0) |

- [baseline] override: if the channel's aggregated retention curve shows a median drop-off deeper than 30 % at any section boundary, shorten the section *before* that boundary by 20 % and lengthen Mechanism.
- ledger: split used, baseline override yes/no.

**V-2 · Voiceover generation**
- reads: script, S-4 voice, `vidiq_voiceover_generate`
- rule: generate once. The returned **duration is the master clock**. If duration is outside target ±15 % → edit the script (cut or add to the Mechanism section only), regenerate once. **Cap: 2 generations.**
- ledger: duration, character count, generations used.

**V-3 · Music**
- reads: presenter; `channel-baseline.md` → `music.track_url` if a house track exists; `catalog/` before either
- rule: an already-sourced bed in the repo catalog or the channel's own library → use it ([S6/A-1] applies to audio, not only imagery). Else house track. Else `vidiq_generate_music("instrumental, <mood by presenter>, no vocals, steady tempo", durationSeconds = VO duration + 5)` once. Mood map: diagram → "minimal electronic, focused"; data object → "soft percussive, precise"; kinetic type → "rhythmic, driving, sparse"; photographic → "warm ambient, slow". Music ducks to 0.25 under VO, fade 400 ms.
- default: no music if generation fails; log it.
- ledger: source, whether it was reused or generated, duration.

---

## S5 — Beat sheet

**C-1 · Beats from the voiceover**
- reads: VO duration; script sentence boundaries; S-6 split
- rule: one beat per sentence cluster that expresses one visual state; beat start times = proportional character offset × VO duration (or word timestamps if the VO tool returns them). Hook beat starts at 0.00 s. Chapters = section starts from S-6, rounded to the nearest beat, first at 0:00, each ≥ 10 s (long only), named as payoffs not sections.
- ledger: beat count, chapter list.

**C-2 · State-change cadence check**
- reads: beats; `youtube-delivery.md` cadence targets
- rule: long: a visible state change every 8–12 s; short: every 1.5–3 s. A scene
  whose beats leave a still window longer than the cap (long 2.0 s, short 1.5 s
  as enforced) is split into sub-beats — never padded with a crossfade.
  **`scripts/beats_to_composition.py` enforces this at generation time and exits
  non-zero**, so the defect never reaches a render. It is still only an
  authoring-time aid: the post-render pixel answer is `[S7/R-2]`.
- **cadence is a floor, not a pass.** Long-form additionally satisfies
  `[S6/A-8]`, `[S6/A-9]` and `[S6/A-10]`: a piece can clear this rule on every
  scene and still read as a slide deck, because a state-change count cannot see
  that every scene has the same enter-wash-hold shape, the same entrance
  signature and no continuity across its cuts. Confirmed:
  `videos/ectoin-survival-molecule` passed this rule — and every other gate —
  and was reviewed as separate slides. Measure the share on the shipped file,
  never from a figure the project already recorded: that project's
  `DELIVERY.md` says 14.8%, written eleven minutes after the render, and the
  shipped MP4 measures **12.7%** under the project's own unmodified script.
- ledger: max gap before/after, and whether the generator rejected a scene.

**C-3 · End-screen scene (long only)**
- rule: last beat is an end-screen frame: reserved overlay zones clear, motion calmed, next-video handoff line in VO. Duration from S-6.
- ledger: end scene duration.

---

## S6 — Composition

**A-1 · Asset and mechanism strategy — check the catalog first**
- reads: `catalog/` (this repo's shared catalog: `catalog/README.md`,
  `catalog/index.html`); presenter; project skill's generated-imagery
  permission; `04-assets/manifest.json`
- rule: **discover, reuse, build, contribute** — the full rule is R4 in
  `references/restored-v1-rules.md`, verbatim. Its three operative points:
  discovery does not stop at `CLAUDE.md` (check for a conventional
  `catalog/` sibling directory); the catalog is checked for **mechanisms**,
  not only imagery — a scene's structure is as reusable as a plate; and a
  genuinely new reusable mechanism is **harvested back** before the run ends.
  Then: diagram / data object / kinetic type → browser-drawn (SVG/CSS/canvas).
  Photographic → project-supplied plates, else catalog plates, else generated
  imagery if the project skill permits, else `vidiq_generate_broll` with
  attribution in the manifest. If none are obtainable → re-fire S-3 with
  presenter = kinetic type (log the fallback).
- **Written for:** the same term/definition card independently rebuilt five
  times across five videos; the BarrierWall mechanism reused for the first time
  on its fourth appearance only because a dedicated review found it.
- ledger: what was searched, what was reused (with its catalog path), what was
  built new, and what was harvested back at the end of the run.

**A-2 · Palette and type tokens**
- reads: project skill tokens; else `frontend-design` guidance
- rule: project tokens win. Otherwise: one dark neutral background, one accent, one text colour, one display face + one text face, all declared as CSS variables in `:root` (or on `#root` for a sub-composition). **Exactly one accent per frame.**
- ledger: tokens used.

**A-3 · Spatial plan, and frame zero**
- rule: three bullets per scene naming the Grid/Flex strategy before markup (see `hyperframes-engine.md`). Not optional, not skipped for "simple" scenes. **Frame zero is a design object** — the scroll-stop and, for a Short, the thumbnail itself ([S3/P-3]). Never blank, never mid-fade, never a lone title on empty canvas. Verify it by extracting it, not by reading the source.
- ledger: scene count with plans; frame-zero verdict.

**A-4 · fps and canvas**
- rule: 30 fps unless the presenter is a data object with fast counters (60 fps). Canvas 1920×1080 or 1080×1920 by S-1.
- ledger: fps.

**A-5 · `box-sizing: border-box`** — restored, verbatim as R3
- rule: `*, *::before, *::after { box-sizing: border-box; }` as the **first rule
  in every composition's `<style>` block**, root and every sub-composition. Full
  text: `references/restored-v1-rules.md` §R3.
- **Written for:** a `.stage { height: 1920px; padding: 192px … 384px … }`
  laying out at an actual **2496px**, silently pushing citation chips and a CTA
  past the real canvas edge. Invisible from source — it shows only as a
  discrepancy between `getComputedStyle(el).height` and
  `el.getBoundingClientRect().height` on a compiled render. A project missing
  the reset **passes `npx hyperframes check` completely clean** and still ships
  the defect; `check` surfaces it only as info-level
  `container_overflow` / `canvas_overflow` findings, which do not gate.
- enforcement: `scripts/beats_to_composition.py` emits it in both the root and
  every scene. If a composition is hand-written, this rule is on the author.
- ledger: confirmed present in root + N sub-compositions.

**A-6 · Type floors** — restored, verbatim as R1
- rule: hero/headline **96–160 px** at 1080 width; reading/body **40 px**
  minimum; burned-in captions **42–56 px**; labels and secondary chrome
  **26–32 px**, and **32 px is the absolute floor for anything a viewer is meant
  to actually read** — smaller than that is decoration, not content. Full text
  and the reasoning for keeping these above looser outside guidance:
  `references/restored-v1-rules.md` §R1.
- **Written for:** six sub-floor type declarations shipped in the 2026-08-31
  target; type as small as 18–33 px running in 14 of 24 shipped projects.
- ledger: smallest declared size per scene, and its role.

**A-7 · Contrast floor 4.5:1, on rendered pixels** — restored, verbatim as R2
- rule: **4.5:1 for any text meant to be read, measured against the actual
  pixels behind it, not the design token alone.** Text over a photo or variable
  plate gets an opaque backing (a pill, a scrim) rather than a colour choice
  trusted to stay legible. A colour token's documented scope is a constraint:
  a secondary-ink token validated on paper can fail outright on ink. Contrast
  applies to the **hero visual**, not only to text — a hook illustration at
  1.05:1 against its own ground reads as an empty frame. Full text:
  `references/restored-v1-rules.md` §R2.
- **now enforced by the tool, and the rule points at it:**
  `npx hyperframes check`'s Contrast pass measures WCAG AA **on rendered
  pixels**, sampled at 5 grid points per sample time; failures are gating errors
  carrying the sampled fg/bg colours, measured vs required ratio, and a
  suggested compliant colour in the same palette direction. Thresholds 4.5:1
  normal, 3:1 large (24 px+, or 19 px+ bold). Do not re-derive contrast prose
  here; read the finding and apply `suggestedColor`.
- **the residual the tool does not cover:** `check` audits *text*. The
  hero-visual clause above has no automated check anywhere — a decorative panel
  at 1.05:1 against its ground is passed by every contrast checker because none
  evaluates it. That one stays a reading rule, checked on the extracted frame.
- ledger: `check` contrast pass N/N, plus the hero-visual verdict per scene.

**A-8 · Transition system, format-scoped**
- reads: `format`; each scene's `bg` and `section`; `03-beat-sheet.json`
- rule: **short — every boundary is a `cut`. Long — a transition SYSTEM: 2-3
  types for the whole video, one primary carrying ~60-70% of boundaries plus
  1-2 accents, never a different transition per scene.** The derivation the
  generator applies when a scene names none: `wipe-left 0.45` inside a
  section, `wipe-up 0.60` at a section start — the boundary where a viewer
  decides to leave, so the strongest transition serves the re-hook instead of
  decorating it.
- **A wipe, not a push, and this corrects an earlier version of this rule.**
  A clip-path wipe reveals the incoming scene at its own resting position; a
  push *translates* whole scenes, which drags their content through the
  reserved safe-area zones. Confirmed by rendering both on the same 29-scene
  1920×1080 piece: the push failed the hard safe-area gate `[S7/R-2]` on **99
  frames** — real text, up to 6.2% edge density inside the top band — against
  a hard-cut baseline that passed all 1361; the wipe measured **0**. Both
  render correctly and both pass `check`, so nothing before the safe-area
  scan distinguishes them. Ground-blending and safe-area transit are
  independent axes: `push-slide` is clean on the first and dirty on the
  second. A wipe only clips, so it cannot place content anywhere a settled
  frame does not already have it — which holds only while the settled frames
  are themselves compliant, and is unsafe over a **raster** (the
  `drawElement` capture bug), so check for `<img>` inside the wiped region
  before choosing it.
- **Expect `[S7/R-1]` to report a wipe boundary as `content_overlap` /
  `text_occluded`, and do not restructure the composition to satisfy it.**
  `check`'s layout pass tests bounding-box geometry and does not model
  `clip-path`, so a clipped incoming wrapper still presents a full-canvas
  opaque box over the outgoing scene's text. The rendered frames show both
  scenes with a clean seam. The trap is that severity is persistence-aware, so
  the verdict tracks **sampling density rather than the composition**:
  measured on one generated 3-scene proof, cuts gave 0 layout errors at any
  `--samples` while wipes gave 1 at 9, 3 at 20 and 3 at 60 — and a 340s piece
  with 28 wipes gave 0 errors / 26 info at `--samples 40`, because a 0.45s
  window is rarely sampled twice when samples sit 8.5s apart. So a run can
  pass on a long piece and halt on a short one for the same technique. This is
  the one place `[S7/R-1]`'s "errors gate the run" needs a named exception:
  confirm the boundary on an extracted frame, ledger the finding with this
  reason, and continue. A plain `crossfade` where the two scenes' grounds differ is a
  **generation error**, not a warning: both layers sit near 50% opacity over an
  unrelated canvas colour and the midpoint frame is muddy. `blur-crossfade` is
  the sanctioned soft option across a ground change — the blur masks the clash
  — but its midpoint still blends two grounds, so `[S7/R-2]` extracts that
  frame rather than trusting the registry's note — in opacity terms
  `blur-crossfade` blends *exactly* as hard as a plain `crossfade` (both ease
  `power2.inOut`, so both wrappers sit at 0.500 at the midpoint and the
  outgoing ground still shows through at ~25%); the 10px blur on both layers is
  the entire difference, and it masks the clash rather than removing it.
  `push-slide` and `squeeze` are the only two that genuinely cannot blend: they
  animate `x`/`y` and `scaleX` with opacity pinned at 1 on both wrappers, so no
  frame ever composites two grounds. `zoom-through` does cross-fade, but its
  asymmetric pair (`power3.in` out, `power3.out` in) leaves both wrappers at
  0.875 at the midpoint, so the outgoing ground shows ~11% and the raw canvas
  ~2% — mild rather than muddy, and still worth the extracted frame. Exit
  animations are never emitted:
  the outgoing scene is fully composed when the transition starts, and the
  transition IS the exit. The overlap window is DERIVED by
  `scripts/beats_to_composition.py` from the scene's `transition.duration` —
  outgoing `data-duration` extended, incoming `data-start` pulled earlier,
  track index ping-ponged, the two-wrapper tween stamped on the root timeline —
  so the beat sheet's own scene times stay contiguous and no overlap is ever
  hand-typed. Registry cap 2.0s; typical 0.3-0.6s. Full text:
  `references/restored-v1-rules.md` §R7.
- **Written for:** `videos/ectoin-survival-molecule` — 28 of 28 boundaries hard
  cut, by correct application of v1's Shorts-derived rule, on a 340s long-form
  piece. It passed every gate this policy had, including `[S5/C-2]` at 12.7%
  active steps on the shipped render (above one shipped 9:16 comparator at
  11.7%, under the other at 23.1%), and was reviewed as "a sequence of
  separate slides". 11 of those 28 boundaries did not even change ground.
- **the disagreement, recorded rather than resolved:** v1 says hard cuts
  outperform crossfades on retention; `hyperframes-animation`'s
  `transitions/overview.md` says "Every composition uses transitions. No
  exceptions." Neither is measured on this channel, and this channel's only
  long-form piece marks every retention comparison `[UNDERPOWERED]` per
  `[S1/S-1]`'s first-of-kind override. Treat the choice as a craft budget:
  authorable, never citable as the cause of a result.
- ledger: transition types used and the count per type, ground-change
  boundaries, and which midpoints `[S7/R-2]` extracted.

**A-9 · Continuity: camera path and actor map (long only)**
- reads: `sections`; each beat's `actor`; each scene's `handoff`
- rule: **cadence is a floor, not a pass — continuity is what a long-form piece
  is judged on.** Two artifacts, both authored at `[S5]` and both cheap. A
  **camera path** maps the information hierarchy to zoom levels so consecutive
  scenes read as framings of one space rather than unrelated slides (salt
  crystal into the bacterium into the protein's hydration layer; a product's
  front label into its ingredient list, then back out to the verdict). An
  **actor map** names which on-screen actors persist across which beats. An
  actor appearing in two consecutive scenes as separately-drawn markup is the
  defect: those scenes are ONE sub-composition with internal phase divs and one
  timeline (hyperframes-core `references/composition-patterns.md` §"C.
  Multi-scene merge"), the actors REARRANGED rather than redrawn, and the file
  is marked `handoff: "hand-authored"` so the generator emits its clip, its
  transition and its assertions but not its markup. **Split scene files by
  actor continuity, not by narration sentence.** Camera legs are hand-authored
  on that merged sub-comp: `viewport-change` for the base virtual camera,
  `coordinate-target-zoom` to dive on an off-centre element (measure the
  target — a journey amplifies centring error on every leg),
  `multi-phase-camera` for a phased move plus the micro-drift that keeps a hold
  alive. A camera move is exactly the transform-between-padded-box-and-canvas
  case `[S6/A-3]` and the safe-area gate exist for: clip the stage's child
  (`.stage > * { overflow: hidden }`) so no transient renders past the line.
  `motion-blur-streak` only on a fast leg, resolving sharp at the landing —
  there is no render-level motion blur in this engine.
- **Written for:** the same render. `09-exclusion.html` and `10-messier.html`
  draw byte-identical protein and water-shell geometry (`viewBox 0 0 620 620`,
  r 190/112, stroke-width 46) with a duplicated ring-builder loop, because the
  files were split by sentence. `hyperframes.json` declared a
  `compositions/components` directory that was never created, and the catalog
  held no molecule actor to reuse — so the merge was a missed *creation*, which
  is what `[S6/A-1]`'s contribute half exists for.
- ledger: the camera path, the actor list, which scenes merged, and the camera
  leg count.

**A-10 · Entrance idiom per beat; no single ease default**
- reads: each beat's `idiom`, and its optional `easing` override
- rule: **the fade-and-rise is one idiom among six, not the house style.** Each
  beat declares an `idiom` chosen from what the narration is doing at that
  moment: `arrive` (opacity plus travel — the old default), `slam`
  (`kinetic-beat-slam`, a word landing on a spoken beat), `wipe` (a clip-path
  reveal, a mechanism drawing itself), `count` (`counting-dynamic-scale`, a
  number counting to its value as it is spoken), `swap`
  (`scale-swap-transition`, a myth transforming into its correction rather than
  being replaced by it), `hold` (bounded camera drift on the stage — a
  deliberate hold kept alive by the camera, never a breathing loop stamped on a
  text card). The generator emits an explicit ease per idiom and **declares no
  timeline-level `defaults: { ease }`**, because an inherited default is
  invisible to any grep for the ease name and is how a project ships one
  signature without anyone counting it. Signature = animated property set plus
  *effective* ease. A top signature over 50% of a run's real tweens is ledgered
  as a template-failure warning. Full text:
  `references/restored-v1-rules.md` §R8.
- **Written for:** the same render. All 29 scene timelines declared
  `defaults: { ease: "power3.out" }`; only 8 tweens named it and 128 of 196
  real tweens carried it — 65%, with 69 of 122 opacity tweens also moving x/y.
  Counting explicit occurrences alone reports 8 and misses the finding
  entirely.
- **this one is a legitimate source-level check**, unlike source-level cadence
  (`[S5/C-2]`, which measures authored beats rather than pixels): entrance
  variety IS a property of the source, so counting it in the markup answers the
  actual question. `catalog/tooling/continuity-audit.py` does the counting.
- ledger: the top three signatures with their shares, and the fade-and-slide
  share.

---

## S7 — Render QA

**R-1 · The gate is the engine's own `check`**
- reads: `npx hyperframes check --json --snapshots` from the project directory
- rule: **errors gate the run. Warnings are logged, not gated.** Pass `--strict`
  only when the project's own `package.json` already runs strict — the pipeline
  does not raise a project's bar behind its back.
  `check` runs the linter first and skips the browser entirely when lint reports
  errors, so a lint error is fixed before anything else is believed. Errors are
  fixed automatically where the fix is mechanical (`loading="eager"`,
  `object-fit`, a missing `id`, a `suggestedColor` swap); non-mechanical errors
  are re-authored. **Cap: 3 fix cycles**, then **HALT: BLOCKER-CHECK** with the
  `--json` envelope and the finding that would not clear.
- **v2's `scripts/lint_composition.py` is deleted, not fixed.** It was inverted
  against the shipped engine: it PASSED a composition that rendered frozen
  (mean |Δ| = 0.00 across five frames) and FAILED the working one, on three
  counts each false here — `window.seek` is not this engine's entry point, a
  project-relative image path resolves correctly, and a named Google Fonts link
  is the supported path because the compiler injects deterministic `@font-face`
  at render time. A second gate that disagrees with the engine is worse than no
  second gate.
- read `skills/hyperframes-cli/references/lint-validate-inspect.md` for finding
  semantics — in particular that severity is persistence-aware (a single-sample
  transient demotes to info) and that a composition showing zero geometry change
  across every sample fails with **`sweep_static`** rather than passing.
- ledger: `ok`, per-pass error/warning counts, fix cycles used, and every
  warning left standing with a one-line reason.

**R-1b · Motion intent is declared, not assumed**
- reads: `03-beat-sheet.json`
- rule: every run writes a `*.motion.json` sidecar next to the composition, from
  the beat sheet, so `check` verifies entrances, order, in-frame and liveness
  against the same seeked timeline the renderer uses. `check` discovers it
  automatically — no flag. Assertions available:
  `appearsBy` / `before` / `staysInFrame` / `keepsMoving`; findings are errors
  by default, and a selector matching nothing fails loudly as
  `motion_selector_missing` rather than silently passing.
  `scripts/beats_to_composition.py` emits the sidecar in the same pass that
  emits the markup, so a selector cannot exist in one and not the other.
- **one root-scoped `keepsMoving` (`withinSelector: "#root"`), with
  `maxStaticSec` set from the format's own cadence cap** rather than the
  engine's 2s default, which is a Shorts number. **Not one per scene**:
  measured on `hyperframes@0.8.22`, the static-window scan runs across the
  whole root duration and is never bounded to the window in which a scene's
  clip is live, so a per-scene `withinSelector` reports that scene's own
  off-screen time as frozen and fails by construction on any tiling
  composition (a 3-scene 9s proof produced three `motion_frozen` errors, each
  one exactly a clip's off-screen span). Relatedly, **the sidecar lives at the
  project root and nowhere else** — one written beside a sub-composition in
  `compositions/frames/` is silently ignored, confirmed by planting an
  impossible assertion there and still getting `ok: true`.
  And **assertions name the copy element, never its container**: an assertion
  on a wrapper passes while the text inside it is overpainted or was never
  wrapped in an element at all. Confirmed:
  `videos/ectoin-survival-molecule`'s payoff line
  (`compositions/frames/28-remember.html:167`) renders blank because it is a
  bare text node under an animated wash — an `appearsBy` naming that copy
  element would have failed at check time as `motion_appears_late`, or as
  `motion_selector_missing` if the element does not exist to be named.
- **Why this rule exists:** it is the closest automated proxy for "render the
  MP4 and watch it", and it catches the render-vs-preview class layout sampling
  cannot — an entrance the seek lands past, a broken stagger, a frozen shot.
- ledger: assertion count, motion pass result.

**R-2 · Post-render pixel gate, on the muxed deliverable** — restored, verbatim as R5
- reads: `bash scripts/extract_frames.sh 06-render/final.mp4 06-render/frames/`;
  `catalog/tooling/check-static-hold.py`; `catalog/tooling/check-safe-area.py`;
  `catalog/tooling/check-cadence.py` (the perceptibility metric: 8fps,
  mean |dLuma| >= 1.0 AND a localised per-pixel max, so a codec refresh cannot
  read as a beat); `catalog/tooling/continuity-audit.py` (source-structural,
  long-form, `[S6/A-8]`-`[S6/A-10]`). The transition-midpoint frame below
  covers `blur-crossfade` boundaries specifically.
- rule: **a source-level cadence measurement is an authoring-time aid, never a
  substitute for the post-render pixel diff.** `[S5/C-2]` measures authored
  beats; an authored beat is not the same thing as a pixel changing. Full text
  and the two confirmed failure modes: `references/restored-v1-rules.md` §R5.
  Check frames: frame zero (composed, not mid-fade), the last frame (for a
  Short, hands back toward the first if a loop was promised), and every
  scene-to-scene transition **midpoint**, not just before and after.
- **Written for:** four of six scenes frozen 2.0–7.5 s on a project that passed
  `check` with 0 errors.
- **what the tool now covers:** `check`'s `sweep_static` refuses to pass a 3 s+
  composition showing zero geometry change across every sample, and `keepsMoving`
  (R-1b) catches a static window over `maxStaticSec`. Treat these the same way
  as contrast: keep the rule, point it at the tool.
- **what the tool does not cover, and why this rule survives it:** `check`
  audits the *composition under seek*. The artifact that ships is the **muxed
  MP4**, after render and the audio pass. And `sweep_static` is a whole-frame
  test — it cannot see a scene's own hero region sitting dead while a different,
  legitimate element elsewhere in the same frame keeps the whole-frame diff
  alive. That is what `catalog/tooling/check-static-hold.py`'s region-aware half
  is for. Reuse it ([S6/A-1]); do not rebuild it here.
- **before trusting any copied checker's "0 findings"**, confirm its
  `CAPTION_BAND_EXCLUDE` / crop constants against *this* project's own
  `index.html` — a burned-in caption band inherited from a sibling project
  silently excludes real content from every diff. Recurred three times in this
  lineage; a comment describing the bug does not prevent it.
- **Cap: 2 re-renders per scene**, then **HALT: BLOCKER-PIXEL** with the frame.
- ledger: frames inspected, each verdict, which catalog scripts ran and their
  exit codes, and the constants they were confirmed against.

**R-3 · Audio master, with AAC headroom** — restored, verbatim as R6
- rule: master to ~**−14 LUFS integrated** as a post-render step. **Encode with
  headroom for the lossy stage: target `TP=-2.5` on the `loudnorm` pass, not
  `-1.5`,** so the post-encode file still lands under −1.0 dBTP. Then
  **re-measure `ebur128` on the actual shipped file** before calling mastering
  done. Full text: `references/restored-v1-rules.md` §R6.
- **Written for:** a two-pass `loudnorm` that correctly hit −1.50 dBTP on its
  PCM output; the shipped MP4's AAC encode had pushed true peak to **+0.5 dBFS**.
  A measurement against the intermediate is not evidence about the deliverable.

```bash
ffmpeg -i raw.mp4 -i vo.mp3 -i music.wav -filter_complex \
  "[2:a]volume=0.25[m];[1:a][m]amix=inputs=2:duration=first[a];\
   [a]loudnorm=I=-14:TP=-2.5:LRA=11[out]" \
  -map 0:v -map "[out]" -c:v copy -c:a aac 06-render/final.mp4
# then, on the SHIPPED file, not the intermediate:
ffmpeg -i 06-render/final.mp4 -af ebur128=peak=true -f null -
```

- also verify with `ffprobe` that video duration == VO duration ± 0.1 s.
- ledger: integrated LUFS and true peak **measured on `final.mp4`**, not on the
  loudnorm intermediate.

---

## S8 — Publish envelope

**E-1 · Everything is a draft until the click.** `vidiq_update_video` and any metadata write are never called by the pipeline. The envelope is pasted or applied only after the operator confirms in chat. This is the second and last human touchpoint.

**E-2 · Schedule**
- reads: `channel-baseline.md` → `best_publish_windows[]` from `vidiq_subscriber_insights`
- rule: propose the next window in the envelope; do not set it.

---

## S9 — Readout (see `learning-loop.md`)

**L-1 · Classify before diagnosing.** At 48 h and 7 d, classify on impressions-CTR
vs channel median and avg-view-% vs channel median **before** any finding is
written. The full table, including the distribution-failure row, is in
`learning-loop.md`. The short form:

| Condition | Class | Where the fix lives |
|---|---|---|
| CTR < median **and** avg-view-% ≥ median | **CTR-failure** | S3 packaging |
| CTR ≥ median **and** avg-view-% < median | **Retention-failure** | S5/S6 structure |
| both below | **Both** — packaging first | S3 then S5 |
| both at/above | **Working** — record the positive signal | none |
| **CTR unavailable **and** avg-view-% ≥ median **and** views ≪ curve** | **Distribution failure** — the video was never served, not rejected | **S2 topic/seed, then the first-frame feed signal — not packaging, not structure** |

**L-2 · Rule recalibration.** Any [default] that a readout contradicts twice in a row is replaced by the measured value in `channel-baseline.md`, with the date and the two video ids as evidence.

---

## Credit budget (vidIQ), per video [default]

| Stage | Calls | Approx. credits |
|---|---|---|
| S0 (once / 30 d) | user_channels, channel_analytics ×3–4, performance_trends, subscriber_insights | ~25–30 |
| S2 | keyword_research ×1–2, outliers ×1 | 10–15 |
| S3 | score_title ×5, similar_thumbnails ×1, generate_thumbnail ×1, refine ×≤1, score_thumbnail ×2 | ~45–70 |
| S4 | voiceover (14 / 1 000 chars, ×≤2), music ×1 (25) | 40–70 |
| S9 | video_stats, channel_analytics(audience_retention) ×1 each readout | ~10 |

Ceiling **200 credits pre-production**; if a stage would exceed it, the stage
uses its cap-reduced path (no refine, no music) and logs `budget-reduced`.
P-1's reduction from ~10 title scores to 5 is a rule change (see P-1), not a
budget cut — the credits it frees are not reallocated to more scoring.

## Working directory

`./outputs/<slug>/` relative to the project, where `slug` is the seed keyword,
kebab-cased, date-prefixed (`2026-09-01-niacinamide-barrier`). If the host
provides its own outputs directory, use that. **Never assume `/mnt` exists** —
it does not on this host, and v2 wrote every artifact to a path that is not
there.

## Stop conditions (halt, don't ask)

- BLOCKER-TOOLS: a required vidIQ tool or the HyperFrames CLI is not callable.
- BLOCKER-CHANNEL: more than one authorized channel and none named.
- BLOCKER-INPUT: the story input cannot ground a single hook + mechanism.
- BLOCKER-ROUTE: the route asks for a field `[S1/S-7]` does not resolve.
- BLOCKER-CLAIM: a hard-prohibited claim (`[K-2a]`) cannot be sourced and cannot
  be cut without leaving the video with nothing to say; or `[K-4]`'s caps are
  exhausted. The resume fact is a source identifier, or permission to cut.
- BLOCKER-CHECK / BLOCKER-PIXEL: caps exhausted (above).
- BLOCKER-BUDGET: the run would exceed 2× the ceiling.

A halt reports the blocker, what was completed, and the single fact needed to
resume. It never presents a menu.
