# faceless-video-craft skill-audit run — REPORT

Run date: 2026-08-31. Nothing published. No `vidiq_update_video`, no metadata writes, no
uploads. Every draft below is unapproved and needs your sign-off before it goes anywhere.

---

## 1. Target

**Every default in the brief was void before the run started**, and that itself is the
first finding: the channel (`UCzqEGQ9uAU43AgyxGtLT7MA`, connected as `hello@seoulhabit.com`)
has **zero public long-form uploads** — all 8 public videos are Shorts. The 21-day exclusion
window, applied literally, leaves exactly one video: the channel's own best performer. Both
defaults were confirmed void by direct query, not assumed, and the target was re-picked
against the actual data with the user's sign-off (see the plan file's Phase 1 for the full
elimination).

**Target: `LPqIuEYOx3s`** — "Everything you need to know about Snail Mucin 🐌🧴" — 1:54,
100 views. Source: [videos/snail-mucin-medical-secret/](videos/snail-mucin-medical-secret).

**Controls:** `2NGeQYjsR7Y` (mugwort/centella, 0:56, 1,036 views, published **1h55m before**
the target the same day) and `D4e2xnNQm1M` (the channel's all-time best, 1,186 views).

**The condemning number: 10.4×**, age-matched, same-day, no confound. And it inverts the
obvious story: at t+2h the target had **14** views to the winner's **4** — the loser was
sampled *more*, not less. Between t+2.8h and t+3.7h the winner went 4→174 views (VPH 179)
while the target sat flat at 14 for four straight hours (VPH 0). Both got shown to viewers;
only one held them.

**Failure type: retention, not impressions/CTR.** `vidiq_score_title` scored the *losing*
video's actual title **94** — higher than the 10.4× winner's own title (**90**), and higher
than all three of this rebuild's honest new title drafts (83–87, §3 below). Packaging was
never the problem here; a scorer that says otherwise on this exact video is worth flagging on
its own (§4).

Supporting evidence from the settled cohort (27 videos with real `averageViewPercentage`
data via `vidiq_channel_analytics`, not estimated): 19–22s videos median AVP **~78%**;
34s–1:27 videos median **~32%**. The target's own AVP is **not available via vidIQ** —
YouTube Analytics carries a ~2-day reporting lag and `audience_retention` returned zero rows
for a video published 2 days before this run.

---

## 2. Diagnosis

Every finding checked against both controls; anything also true of them is demoted out of
this table (see "Demoted" below). Full evidence trail is in the plan file.

| Finding | Evidence | Skill rule | Sev |
|---|---|---|---|
| Payoff lands ~13.5s in a 2s-window format | Transcript: 13.5s of 1960s-Spain setup before "SNAIL MUCIN" appears on screen | *The hook* — payoff visible by ~2s | Critical |
| Runtime 113.84s = 2.5× the skill's ceiling, no reason recorded | Root `data-duration="113.84"`; STORYBOARD.md records a voice-retime rationale, not a duration one | Prod. loop 2 — 28–45s default, record exceptions past 50s | Critical |
| Scene length ~2× the winner's at equal scene count | Target mean 19.4s/scene vs winner's 9.6s/scene, both 6 scenes | *Formats* — cadence "for the entire scene" | Critical |
| 60.5% of runtime inside a >3s cadence gap | Corrected beat-map measurement (see §4's regex note): max gap/scene 3.55/5.56/7.10/6.26/4.77/5.07s → 68.85s of 113.84s | *Formats* + static-hold | High |
| Caption band drawn entirely inside the reserved bottom-20% UI zone | `captions.html`: band spans y 1600–1920 on a 1920 canvas; reserved zone starts at y 1536 | *9:16-native* — bottom ~20% | High |
| Generic subscribe close, no engineered loop | Final frame = "WOULD YOU TRY IT?" + "SUBSCRIBE!"; frame zero shares no colour/position with it | *The hook* — lesson-tied close + loop | High |
| Six type declarations below the 32px floor | 24px/26px/28px labels across 3 files | *9:16-native* type floor (**new in this revision**) | Med |
| `[NOT IN SKILL]` on-screen "04 / 06" progress counter in a Short | `04-snail-spa.html:292` | — | Med |

**Withdrawn during verification** (the skill's own "a QC report is a claim, not a diagnosis"
rule, applied to my own tooling): an initial regex measured false 16.3s/14.6s frozen-scene
gaps because it only matched single-line `tl.to(...)` calls — this project's real scenes use
multi-line `fromTo` and helper-function calls (`ytCameraMove(tl, sel, AT, {...})`). Corrected
extraction (handling both shapes) found the real maxima above. Also withdrawn: an apparent
"HUMECTANT TEST | 000" on-screen placeholder — that was `vidiq_watch_shortform_content`'s own
OCR error; the source file reads "HUMECTANT TEST" only.

**Demoted (true of the 10.4× winner too, so not findings):** zero `--safe-*` token usage in
any of 7 files (0 in both controls as well); no `.srt`/`.vtt` sidecar (absent in all three
videos compared); thumbnail scored 35 with 3 unlabeled candidates and no final choice (**the
winner has no thumbnail directory at all**, and Shorts carry no thumbnail-click decision).
Real pre-render-gate failures, but none of them explain the gap.

---

## 3. What I rebuilt

New project, nothing existing touched: [videos/snail-mucin-recut-34s/](videos/snail-mucin-recut-34s).

**Open in this order:**

1. [STORYBOARD.md](videos/snail-mucin-recut-34s/STORYBOARD.md) — beat sheet, catalog
   discovery, asset manifest, what was rejected and why.
2. [index.html](videos/snail-mucin-recut-34s/index.html) — root timeline, 6 scenes + captions,
   34.0s.
3. [compositions/frames/01-mistake.html](videos/snail-mucin-recut-34s/compositions/frames/01-mistake.html)
   through `06-loop.html`, in order.
4. [compositions/captions.html](videos/snail-mucin-recut-34s/compositions/captions.html).
5. [renders/snail-mucin-recut-34s_master.mp4](videos/snail-mucin-recut-34s/renders/snail-mucin-recut-34s_master.mp4)
   — the one render in the folder; the pre-fix render was deleted, not left for you to guess
   which one to trust.

**Scope, per your call:** full 30–40s re-cut, not the brief's "first 15s" default — the
diagnosed failure is structural (scene length, total runtime), and trimming the opening of a
114s short doesn't fix a 114s short.

**What changed and why, tied to the findings table:**

- **Payoff moved to frame zero.** The mistake ("You're doing this wrong" / damp-skin plate)
  opens the video; the 1960s origin story moves to a compressed 6s credibility beat *after*
  the value, per *The hook*'s "every beat past value delivery earns its place."
- **Scene count held at 6, total runtime cut 113.84s → 34.0s.** Max scene length 8.0s
  (target findings #2/#3).
- **Cadence measured from source, not estimated**, after finding and fixing my own
  measurement bug (see §4): every scene holds ≥1 state change every ≤2.5s internally, no gap
  over 3s anywhere in the 34s render. **Correction (§7): this claim was itself false.** A
  source-level beat map counts authored tween positions, not pixel change — a
  `tl.to(el, {opacity: 0.85})` registers as a beat while moving 0.00 pixels. A post-render
  pixel diff (caption layer cropped out, the check *Verification loop* specifies) found four
  of six scenes frozen for 2.0–7.5s at a time. Fixed and re-verified in §7; do not trust this
  bullet as evidence the original render's cadence was sound.
- **Caption band rebuilt from the actual safe-bottom token** (384px = 20% of 1920) instead of
  a hardcoded offset: new band sits at y 1168–1488, clearing the reserved zone (≥1536) by
  48px. Directly fixes finding #5.
- **Closing beat is one lesson-tied action** ("Mist first. Then apply."), not a subscribe
  card, and the last frame reuses Scene 01's exact plate, crop, and hero position — confirmed
  by frame extraction (§5), not assumed.
- **Reused the catalog's `split-compare` mechanism** for the dry-vs-misted-sponge reversal
  (Scene 02) — the source video's own content already *was* this comparison, just never built
  as one. `term-definition` was checked against the 3-card ingredient scene and **rejected**
  (its own choreography assumes a slower per-term glossary sweep than an 8s/3-card burst can
  give it) — recorded in STORYBOARD.md as a real component-check outcome, not silently
  skipped.
- **Type floor enforced**: nothing below 32px; hero copy 84–116px; captions 46px.
- **No progress counter.** Dropped; it encoded nothing a Shorts viewer needed.
- **Built silent-first**, audio slots wired and marked reused-vs-new-take per line in
  `index.html`'s HTML comments — the new beat order doesn't match the existing VO's take
  order, and the skill is explicit that a fade cannot fix a clip that was never
  recorded/timed for this cut.
- **Zero new plates generated.** Every image is reused from the source project's own `public/`
  folder — the catalog and the source project together already covered every beat.

**Real defects the process itself caught and fixed, worth stating plainly rather than
folding into a clean summary:**

- The first render shipped with **three genuine layout overlaps** — Scene 01's headline
  wrapped to 3 lines instead of 2 (didn't fit the safe width at 116px), and Scene 02's
  reversal labels ("PANICS"/"ABSORBS") and its "IT'S A MOISTURE MAGNET" headline both
  collided with the caption band and with each other respectively. **`npx hyperframes check`
  reported 0 layout issues on that build.** These were found only by extracting frames and
  looking — exactly the discipline *Verification loop* insists on and exactly the gap the
  skill warns a passing manifest can't close. Fixed, re-rendered, re-extracted, re-confirmed
  by pixels a second time (frames attached to this session).

**Packaging drafts (drafts only, nothing publishes):**

| Title option | `vidiq_score_title` |
|---|---|
| "You're Using Snail Mucin Wrong (Here's the Fix)" | 87 |
| "Snail Mucin Dries Out Your Skin If You Skip This" | 86 |
| "The Snail Mucin Mistake Everyone Makes #skincare" | 83 |

Notable and worth not burying: **all three honest rewrites score below the failing video's
own title (94)** and below the 10.4× winner's (90). On this one video, the title scorer's
output doesn't track the actual outcome at all — see §4.

- **Thumbnail direction** (not built — the source render's frame-zero plate is thumbnail-
  ready on its own, per *The thumbnail*'s "extract, grade, finalize" path): the damp-skin
  macro plate with "YOU'RE DOING THIS WRONG." burned in, matching the video's actual frame
  zero exactly — no separate authored composition needed. The winning control shipped no
  thumbnail at all, which is itself the more relevant channel precedent to note here.
- **Chapters: not applicable.** Skill's own Formats table — Shorts carry no chapters.
- **End screen: not applicable.** Shorts get one related-video link; the engineered loop in
  Scene 06 is the format's actual equivalent mechanism.
- **Pinned comment draft:** "The mistake: applying to bone-dry skin. Mist first, then pat it
  in — that's the whole fix. What's your damp-skin routine?" (Captions are burned in for
  everyone regardless of settings, so the comment doesn't need a CC callout — the sidecar
  `renders/snail-mucin-recut-34s.srt` is for YouTube's own caption-track upload field, not a
  detail worth surfacing to viewers.)

---

## 4. Skill audit

This is the part that was actually asked for. Not a compliment pass — several of these are
real problems in the revised `SKILL.md`, found by pushing one real video through it.

### Rules that fired and changed the output

- **The 32px absolute type floor** (revision-only — the pre-revision skill had no floor below
  "reading/body text: 40px minimum") directly killed six real labels in the source project
  and set a hard minimum for every new label in the rebuild. Without this rule, 24–28px
  labels would have passed uncommented.
- **"The closing beat is one specific, lesson-tied action... never a generic
  subscribe/like card"** (revision-only) is the rule that produced Scene 06's "Mist first.
  Then apply." instead of a subscribe card, and the rule that made the engineered loop
  (matching frame zero) a requirement rather than a nice-to-have.
- **"An external QC report is a claim, not a diagnosis — verify its fix against the actual
  pixels"** (revision-only) is the rule that caught my own two false cadence findings
  (§2) *and* the three real overlap defects the automated `check` gate missed (below). It
  earned its place twice in one run.
- **Pre-render gate + Verification loop as a combined checklist** (revision-only structure)
  is what forced frame extraction at all, rather than trusting `npx hyperframes check`'s
  "0 issues" result. Without it, this rebuild would have shipped with three overlapping
  text blocks.

### Rules that never fired on this real video — candidates for cutting or demoting

- **Audio-mastering LUFS targets, `data-fx-carve` ducking, SFX hash-comparison** — none of
  this applied because the rebuild is silent-first by necessity (new beat order, no matching
  take). A large fraction of *Audio is a first-class composition layer* simply never
  activates on a project at this stage of production. Not wrong, just untested here — worth
  noting as coverage, not a defect.
- **The catalog-contribution step (production-loop 12)** never fired either: nothing built in
  this rebuild was novel enough to harvest back (the SplitCompare adaptation is a use of an
  existing entry, not a new one). A real, honest "no contribution this time" outcome, which
  the skill's own wording anticipates ("not everything qualifies") — so this isn't a gap, but
  it's worth naming since the audit asked for what didn't fire.

### Ambiguous, self-contradictory, or guess-inducing

- **The skill declares itself "deliberately domain-neutral"** (top of file) and then
  hardcodes this one channel's own measurements into what read as general rules: "14 of this
  channel's 23 shipped shorts already run past 50s," "only 6 of 24 shipped projects reference
  `--safe-*` tokens," "real scenes across 14 of this channel's 24 shipped projects already run
  type as small as 18-33px." These are real, useful evidence for *this* channel, but they sit
  inside sections written as universal craft rules, with no signal to a reader on a different
  channel that the *numbers* are local evidence and the *rules* are general. A reader who
  takes the file at its word could reasonably conclude the skill has silently absorbed one
  project's constraints exactly as its own opening paragraph warns against doing.
- **The skill's own canonical sub-composition example is stale against the pinned engine
  version it tells you to trust.** *Canonical patterns → A sub-composition (one scene, one
  file)* shows `<html><body><div id="root" class="clip">` with `document.importNode`. Every
  real shipped composition on `hyperframes@0.8.17` (checked across 4+ projects, not just the
  target) instead uses a top-level `<template data-composition-id="..." data-duration="...">`
  wrapper with no `importNode` call at all — the runtime handles mounting internally. Worse:
  the skill's canonical CSS (`.clip { position: absolute; inset: 0; ... }` applied to the
  scene root) **fails `npx hyperframes check` outright** on this version
  (`subcomposition_root_styled_by_class`, an ERROR, not a warning) — because the render scopes
  sub-composition CSS as `[data-composition-id="X"] <selector>`, and a rule keyed on the
  root's own class becomes a non-matching descendant selector. Following the skill's own
  canonical example literally, on the exact version it tells you to verify against, produces
  a failing gate. The skill's blanket disclaimer ("verify against the shipped docs... this
  file's shape may drift") technically covers this, but a worked example that fails the
  gate it tells you to run is a stronger and more specific problem than a generic
  drift-happens disclaimer communicates.

### `[NOT IN SKILL]` — what a real video needed that the skill couldn't say

1. **No guidance that `vidiq_score_title`/`vidiq_score_thumbnail` can disagree with actual
   outcome, and by how much.** This run hit that directly: the failing video's title scored
   94 (higher than the 10.4× winner's 90, and higher than every honest rewrite this session
   produced). The skill's *YouTube delivery* section treats these scorers as reliable
   competitive-research inputs with no caveat about a scorer/outcome mismatch this large. A
   reader following the skill as written would have no reason to distrust a 94.
2. **No method for actually measuring cadence from timeline source**, only from rendered
   pixels. *Verification loop*'s static-hold check operates on extracted frames — correct,
   but expensive, and it doesn't help *during* authoring, before a render exists. This session
   needed a source-level beat-gap measurement to build the diagnosis and to verify the rebuild
   pre-render, and had to invent one — which then had a real bug (matched only single-line
   `tl.to()` calls, silently under-counting beats authored as multi-line `fromTo()` or via
   helper functions like `ytCameraMove()`). A method this easy to get wrong quietly, with no
   guidance in the skill at all, is exactly the kind of gap that produces false findings in
   review work built on top of this skill.
3. **The title/thumbnail section is written entirely for a long-form click decision** and
   never says the packaging lever is different for a Short (no thumbnail-click moment exists
   in the Shorts feed at all — confirmed directly by this run's own winning control, which
   shipped with no thumbnail whatsoever and still won by 10.4×). A reader building a Short
   would reasonably over-invest in thumbnail iteration based on this section's wording.
4. **Nothing about on-screen progress/chapter counters ("04 / 06") inside a Short**, despite
   the skill explicitly banning Shorts chapters at the platform level (*Formats* table). A
   composition can still render an on-screen counter that implies chapter-like structure the
   format doesn't support — the skill has no rule against this specific, confirmed-shipped
   pattern.
5. **No worked convention for how a burned-in caption band and a scene's own bottom-anchored
   hero copy are supposed to coexist without colliding.** *9:16-native composition* gives safe-
   area percentages and *The captions* gives a band position, but nothing tells an author that
   reserving `--safe-bottom` alone is insufficient once a caption band also claims real
   vertical space above it — this rebuild discovered that the hard way (three real overlaps,
   confirmed by frame extraction, that a clean `check` run did not catch) and had to invent a
   `--content-bottom-limit` token that accounts for both zones together.

**Proposed edits (diffs against the installed `SKILL.md`, not applied):**

```diff
--- a/SKILL.md (### Consistency across a channel's videos section)
+++ b/SKILL.md
@@
+**A number cited as evidence for a rule is not the same as the rule itself.** Where this
+file cites one channel's own measurements ("14 of 23 shipped shorts run past 50s," "only 6
+of 24 projects reference --safe-* tokens"), that number is *evidence this constraint is
+worth enforcing*, not a fact about every channel a reader of this file might be working on.
+State the general rule first, then mark channel-specific evidence as an example, not as the
+rule's own scope.
```

```diff
--- a/SKILL.md (### Canonical patterns section)
+++ b/SKILL.md
@@
-Prefer sub-compositions once a project has more than ~4-5 scenes...
+Prefer sub-compositions once a project has more than ~4-5 scenes...
+
+**Confirm the sub-composition root shape against a real project on your pinned CLI version
+before copying the snippet below.** Confirmed divergence: hyperframes@0.8.17's own shipped
+projects use a top-level `<template data-composition-id="..." data-duration="...">` wrapper
+with no `document.importNode` call, and `npx hyperframes check` treats styling the scene
+root by its `.clip` class as an ERROR (`subcomposition_root_styled_by_class`) on that
+version — the exact opposite of what the snippet below shows. Run `npx hyperframes check`
+on your first scaffolded file before writing five more from the same template.
```

```diff
--- a/SKILL.md (### The thumbnail section, opening line)
+++ b/SKILL.md
@@
-The thumbnail is a deliverable, not a by-product of rendering...
+**For a Short, there is no thumbnail-click moment in the feed at all — the safe area,
+cadence, and hook sections below carry the actual retention lever.** Treat thumbnail
+production for a Short as a lower-priority packaging asset (still worth one good candidate
+for search/browse surfaces), not the primary lever this section describes for long-form.
+
+The thumbnail is a deliverable, not a by-product of rendering...
```

```diff
--- a/SKILL.md (### Verification loop, after Static-hold detection)
+++ b/SKILL.md
@@
+**Source-level cadence measurement, not just post-render.** Extracting every GSAP tween
+position from a scene's own `<script>` block is the fast way to check cadence before a
+render exists — but a naive regex over `tl.to(...)` calls will silently under-count any
+beat authored as a multi-line `fromTo()` call or via a named helper function
+(`ytCameraMove(tl, target, at, {...})`, `ytDefocusPulse(...)`). Match the position argument
+across the full call, not line-by-line, and include helper-function call sites explicitly —
+an under-counted beat map reports a false gap where none exists, or worse, misses a real one.
```

```diff
--- a/SKILL.md (### 9:16-native composition, Safe areas bullet)
+++ b/SKILL.md
@@
-Approximate reserved zones (verify against a current device):
+A burned-in caption band claims its own vertical space **in addition to** the safe-bottom UI
+zone below it, not carved out of it. Define a combined `--content-bottom-limit` (canvas
+height minus safe-bottom minus caption-band-height minus a clearance gap) and anchor every
+scene's own bottom-positioned content to that token, not to `--safe-bottom` alone — a scene
+that only clears the UI zone can still collide with the caption band sitting above it.
+
+Approximate reserved zones (verify against a current device):
```

---

## 5. Audio update (post-report)

Real VO recorded and mixed after this report was first written — the rebuild is no longer
silent-first. Voice: **Kimberly** (`674b71b8-1d2e-4087-8567-d1f53c0b9f3c`), the same voice
already used elsewhere on this channel (`kbeauty-one-percent-line`, `seoulhabit-launch`) —
reused for channel-voice consistency via `media-use`'s TTS path, not picked fresh. All 6
lines fit their scene windows with real headroom (no retiming needed). Raw takes measured
-17.8 to -20.8 LUFS; two-pass `ffmpeg loudnorm` (measure -> apply, linear) brought every
clip to the -16.6 to -17.0 LUFS band this exact voice already established on this channel.
BGM reuses the source video's own bed at its own `data-volume=0.12`, cropped to 34.0s with
head/tail fades baked in — no `data-fx-carve` ducking, matching the real, confirmed
convention the source project itself ships (no `hf-audio-group`/carve anywhere in its
`index.html`). Final export mastered to **-14.1 LUFS / -0.9 dBTP** via a second two-pass
`loudnorm` on the rendered MP4 (video stream copied through unchanged), per the skill's
own post-render mastering rule — the raw render measured -13.9 LUFS / **-0.4 dBTP**, hotter
than the -1.5 dBTP publish target, so this pass was not optional. Verified by direct
measurement (`ffprobe`/`ffmpeg loudnorm`), not by the render's own success line, and by
re-extracting frames from the mastered file to confirm the visual build is untouched.

One real engine-mechanics finding surfaced doing this: **hyperframes@0.8.17's own
`data-automation` volume-lane validator requires the exact shape
`{version:1,lanes:[{target:"volume",points:[{t,v}]}]}`** — confirmed by reading the
installed CLI's own bundled `dist/cli.js` validator directly (not assumed from
`faceless-video-craft`'s own documentation of this, which was itself independently
confirmed correct here) before writing any automation markup, per the skill's instruction to
verify engine mechanics against shipped code before a real render.

## 6. What I'd need to do next

Ranked by what actually moves the number, with time estimates:

1. **Re-pull `vidiq_channel_analytics report=audience_retention filters=video==LPqIuEYOx3s`
   in ~2 days** (5 min, then wait) — once YouTube's reporting lag clears, this either confirms
   or refutes the inferred retention diagnosis against a real drop-off curve instead of the
   proxy evidence (VPH collapse + cohort duration curve) this report used.
2. **A/B the two titles that actually beat the field** — this run's 87-score draft against
   the channel's next few uploads, given finding #1 in §4 (the scorer's output didn't track
   this video's real outcome at all).
3. **Sidecar `.srt` — done.** `renders/snail-mucin-recut-34s.srt`, 10 cues, exported from
   real per-clip word-level transcription (`npx hyperframes transcribe`), not retyped from
   the script. One real ASR error hand-corrected ("Missed" -> "Mist", scene 06). One real
   process bug caught and fixed along the way: transcribing all 6 clips as a single 32s
   composite let Whisper collapse a genuine ~3s cross-scene silence gap into one word's
   reported duration — redone per-clip, then offset by each clip's real `data-start`, which
   avoids that failure mode entirely. Verified against the actual mastered render's audio
   (`ffmpeg volumedetect` at every cue start), not the pre-mix clips.
4. **If the July-batch videos with a measured 7.48% AVP (`mwBUi4tfqQA`) exist anywhere
   outside this repo, pull them in** (~10 min once located) — that number is the hardest
   retention failure on the channel and has no source here to diagnose against.

---

## 7. QC verification (post-report) — three of four findings were fabricated, the real defect was elsewhere

An external QC pass graded this cut "fix-then-ship": one BLOCKER (captions in the bottom
15% safe zone), two MAJORs (a "QOO" typo, 8s of dead air), one MINOR (slow caption fade-in).
Per *Verification loop*'s own rule — "an external QC report is a claim, not a diagnosis" —
every finding was reproduced against the actual rendered pixels/audio before touching
anything.

| # | QC claim | Verdict | Evidence |
|---|---|---|---|
| 1 | "QOO" typo at 0:26 | **False** | Source reads `GOO`; native-resolution frame crop at t=28.5 confirms "THAT SAME GOO IS NOW" on screen. Grain in the archival plate under the G's bowl is what reads as a Q to an OCR pass. Also mistimed — the line isn't on screen at 0:26 at all. |
| 2 | **BLOCKER** — captions inside bottom 15% | **False** | Caption band sits at y 1168–1488 on a 1920-tall canvas; bottom 15% starts at y 1632. Row-measured on 4 extracted frames, clearing the reserved zone by ≥48px. Applying the report's prescribed fix (shift up 350–400px) would have driven captions into Scene 02's verdict row and Scene 05's headline. |
| 3 | 8s dead air 0:15–0:23 | **Mostly false** | VO is present 16.15–21.03s at −13 to −20dB RMS — no 8s hole. Two real ~3.2s narration-free spans exist (12.9–16.2s, 21.0–24.2s) carrying BGM at −26 to −35dB, kept deliberately as breathing room rather than filled with new VO. |
| 4 | Ingredient sub-text fades too slowly | **False** | Cards fade in 0.35s and hold fully opaque 1.65s — already past the 1.5s floor the report asked for. |

**What the report missed entirely, and what actually needed fixing:**

- **D1 — four of six scenes were frozen.** The static-hold check (4fps extraction, caption
  layer cropped out per *Verification loop*) found 0.00 mean pixel-diff runs of 2.0–2.5s in
  Scenes 02, 03, and 06 — Scene 03 was static for 7.5 of its 8 seconds. Root cause:
  `yt-camera-move` was installed and used in exactly one of six scenes (05). Fixed by wiring
  the same helper into Scenes 02, 03, 04, and 06 (opposed pushes on the Scene 02 split,
  continuous plate motion under Scene 03's list and Scene 04's cards, a reversed creep in
  Scene 06 that still lands on Scene 01's frame-zero geometry for the loop). Scene 03 also
  got per-step dwell-fill bars so the gaps between list items carry real motion, not just
  the background. Re-verified post-render: **no run ≥1.0s anywhere in the video.**
- **D2 — the loop point was simultaneously silent and frozen.** The BGM's tail fade dropped
  to −78dB by 32.5s and true silence by 34.0s, coinciding with Scene 06's frozen final 2.75s.
  Re-cut a 34s at-level bed (self-crossfaded loop from the source project's `track.loop.mp3`
  chorus section) with 200ms in/out declick fades instead of a 4.5s fade-to-silence.
  Re-verified: −35dB at 33.75s (was −78dB).
- **D3 — Scene 02's actual claim line measured 1.44:1 contrast**, pink text directly on a
  light plate (WCAG AA floor is 3:1). Gave it an opaque ink pill. Re-measured: 16.16:1.
- **D4 — Scene 06's caption pill repeated its hero copy verbatim** ("Mist first. Then
  apply." twice on screen at once). The caption stayed the literal VO transcript (accuracy
  wins per *The captions*); the decorative hero line was reworded to "Damp skin. Every
  time." — same lesson, not the same sentence.

Also renamed the project directory from `snail-mucin-recut-34s_master.mp4/` (a render
filename applied to a folder) to `snail-mucin-recut-34s/`.

**Re-render.** `npx hyperframes check`: 0 errors (three benign `GSAP target not found`
warnings traced to the pasted-per-scene `gsap.set()` firing before each scene's own
mounting completes — cosmetic; the actual seeked `tl.to()` motion these warnings sit next to
renders correctly, confirmed by the pixel diff above). Full re-render, then two-pass
`ffmpeg loudnorm`: raw render measured −13.93 LUFS / −0.58 dBTP; mastered file measured
**−14.09 LUFS / −1.35 dBTP** against the −14 LUFS / −1.5 dBTP target. Loop-match diff between
first and last frame: 3.16 (baseline before this pass: 3.03 — unchanged within noise).

**Delivery manifest for this pass:**

- **Render:** `videos/snail-mucin-recut-34s/renders/snail-mucin-recut-34s_master.mp4` —
  34.0s (34.1s incl. trailing audio tail), 1080×1920, loudness-normalized to −14.09 LUFS /
  −1.35 dBTP. This is the only render in the folder — the pre-fix version was deleted, not
  left for ambiguity.
- **Captions:** burned in (unchanged mechanism); sidecar
  `videos/snail-mucin-recut-34s/renders/snail-mucin-recut-34s.srt` (unchanged — the fixed
  scenes didn't touch VO timing, so no cue re-derivation was needed; Scene 06's cue still
  matches the unchanged VO/caption text).
- **Thumbnail:**
  `videos/snail-mucin-recut-34s/thumbnails/snail-mucin-recut-34s_final.png` — extracted from
  the mastered render, graded (contrast/saturation/sharpen), confirmed legible at grid scale
  (120x213 downscale check). Extracted from frame index 6 (~0.2s in), not literal frame 0 —
  see the frame-zero finding immediately below for why.
- **Skill updated:** `.claude/skills/faceless-video-craft/SKILL.md` — see below.

## 8. Skill updates applied

1. **Pre-render gate gained a cadence item** — the static-hold check existed only in prose
   inside *Verification loop* and was never one of the 12 binary gate items that actually
   get run before calling a render final. This is the single biggest reason D1 shipped.
2. **The source-level cadence measurement this report itself proposed adding to the skill
   (§4 of the original report) was rewritten before adoption** — as originally worded it
   would have institutionalized exactly the blind spot that let D1 pass: a tween is not a
   pixel change, and this render is now the cited case.
3. **The loop rule now covers audio, not just the visual last frame** — D2 sat in a real
   gap between *The hook*'s loop guidance (visual-only) and *Audio is a first-class
   composition layer* (never states the mix must be live at the last frame).
4. **The QC-report-verification rule now names fabricated findings as their own failure
   class**, distinct from the misdiagnosis case it already covered, with a cheap disproof
   per claim type (native-res crop for a text claim, row measurement for a safe-area claim,
   RMS-vs-time for an audio claim) — three of four findings in this exact report were
   fabricated, not misdiagnosed.
5. **A contrast floor was added to the 9:16 type section** — the type floors were all size;
   nothing checked contrast, which is how a 1.44:1 headline (D3) passed both a human review
   and the engine's own automated contrast checker (13/13 "pass" on the original render).

## 9. New finding, flagged rather than fixed here — frame-zero/cut-boundary capture lag

Extracting by exact frame index (not timestamp) while sourcing the thumbnail surfaced a
defect outside this pass's approved scope: the literal first exported frame (index 0,
t=0.000s) of the whole video is missing Scene 01's headline entirely, even though the source
markup (`01-mistake.html`'s `.mistake-head`) has no opacity animation and should render
immediately — the text only appears starting at frame index ~3 (t≈0.1s). Separately, at the
Scene 01→02 cut (frame index 60, t=2.000s exactly), the extracted frame shows Scene 02's
split-compare divider and labels already well into their entrance while Scene 01's caption
pill is still fully visible, well past when its own script schedules it to have faded out.
Both point at the render/capture pipeline (frame index not mapping cleanly to nominal
timeline position at scene boundaries), not at a bug in this video's own composition code.
Not investigated further here — flagged as a separate task
(`task_c3e11056`, "Investigate HyperFrames frame-zero/cut-boundary capture lag") since
root-causing it would mean checking other projects across the channel and possibly the
engine's own internals, well past what this QC-fix pass was scoped for. Worked around for
this video's own thumbnail (sourced from a later, fully-composed frame instead of literal
frame 0) rather than blocked on it.
