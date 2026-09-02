---
name: faceless-video-craft
description: "Data-gated, zero-decision production line for faceless educational YouTube video built as code: story in, rendered MP4 plus publish envelope out, every fork resolved by a written rule and measured channel data (vidIQ) rather than a question to the operator. Covers HTML/CSS/JS compositions rendered deterministically through HyperFrames (HeyGen), motion design, image-plate animation, kinetic typography, voiceover-locked timing, title/thumbnail scoring, retention structure, chapters, end screens, Shorts safe areas, and the post-publish learning loop. Use for any video with no presenter on camera: explainers, lessons, motion graphics, 'make a video about X', 'turn this script into a video', 'animate this image', 'why did this video underperform', or any vidIQ topic/title/thumbnail decision. Trigger even for plain frontend work, since ordinary web animation renders frozen in a seeking headless browser. Also on HyperFrames, window.__timelines, hyperframes check, Remotion, Ken Burns, beat sheet, 9:16 short, vidIQ, or /produce."
---

# Faceless video craft — v2 (data-gated production line)

This skill turns a **story** (topic, script, research note, or lesson) into a
**rendered MP4 plus a publish envelope** with no operator decisions in between.
Two things stay human: the story that goes in, and the final publish click
(metadata writes to YouTube require explicit consent). Everything between is a
rule, a default, or a measured number — and every rule that fired is written to
a **Decision Ledger** so the run is auditable and the rules can be recalibrated.

It is domain-neutral about *subject matter*. Brand palettes, component rosters
and a project's own truth rules belong to a **project skill**; if one is in play
its content constraints win, this skill still governs craft and process. Never
carry one project's constraints into another project's work.

**Claim sourcing is the exception, and it is not delegated.** `decision-policy.md`
§Claims (`K-*`) is a **floor** that applies whether or not a project skill exists.
A project skill may be stricter; it may not be looser, and its absence is not
license to skip. v1 said this in prose and left the rule unwritten, which is how a
health-claims run reached a halt with nothing to apply.

## Read order

1. This file — operating contract, mandatory rules, the pipeline at a glance.
2. `references/decision-policy.md` — **the rulebook.** Every fork in the
   pipeline, the data it reads, the threshold, the default when data is
   missing. Read before any run; this is what "no decisions" means.
3. `references/pipeline-runbook.md` — the stage-by-stage execution order with
   exact tool calls, credit costs, artifacts and gate checks.
4. `references/hyperframes-engine.md` — **the shipped engine contract**,
   transcribed from the pinned CLI's own docs with the source file named beside
   every line. Read before writing any markup.
   Its §Claims (`K-*`) is the floor for what may be asserted on screen; read it
   before writing a single claim sentence.
5. `references/restored-v1-rules.md` — six rules carried over from v1
   **verbatim**, each with the confirmed defect it was written for. Referenced
   from the policy by id; read when a rule needs its reasoning, not just its
   threshold.
6. `references/youtube-delivery.md` — formats, safe areas, hook, chapters, end
   screen, captions, audio. Read before the beat sheet is written.
7. `references/learning-loop.md` — post-publish readout and how measured
   results rewrite `references/channel-baseline.md`.
8. `references/channel-baseline.md` — the channel's own measured numbers. If
   it reads "not yet populated", stage 0 of the runbook populates it.

Check the directory before assuming a reference exists. If one is missing, this
file plus `decision-policy.md` are enough to run; never stall on a missing file.

**Read the pinned version's own shipped docs before writing markup.** They ship
inside the CLI package (`dist/docs/`, `dist/skills/`, `dist/templates/`) and
`npx hyperframes docs <topic>` prints them with no network. `hyperframes-engine.md`
is a transcription of them, not a substitute: if a pattern is not in the pinned
version's shipped docs, it is not in this skill. Read the copy for the pin the
project's own `package.json` scripts name, never `@latest`.

Locate the `frontend-design` skill rather than assuming a path — it may sit under
a plugin marketplace, the session skill cache, or `/mnt/skills/public/`. If it is
absent, proceed. Compositions are frontend and inherit its taste rules.

## Operating contract

**Inputs accepted** (any one is enough to start):
- a topic ("how niacinamide works"), a question, a research note, a script,
  a lesson outline, or a URL/document to teach from.
- optional overrides, all with defaults: format (long/short), target length,
  presenter type, voice, language, project skill to apply.

**Outputs, always, in `./outputs/<slug>/`** relative to the project (or the
host's own outputs directory if one exists — never assume `/mnt` is there):

| File | What it is |
|---|---|
| `00-decision-ledger.md` | Every rule that fired, the data it read, the value chosen. |
| `01-story-brief.md` | Learning objective, misconception, mechanism, proof, application — **plus §Sourcing, the `[K-1]` claim table**, which no claim may skip. |
| `02-packaging.md` | Title (with vidIQ score), thumbnail concept + file, description, tags, chapters. |
| `03-beat-sheet.json` | Timed beats, locked to the voiceover's measured duration. |
| `04-assets/` | Manifest + every plate, font, VO, music file, resolved to absolute paths. |
| `05-composition/` | `index.html`, `compositions/frames/*.html`, `index.motion.json`, `hyperframes.json` — generated from the beat sheet, `check`-clean, debug class off. |
| `06-render/` | MP4, muxed audio, the `check --json` envelope, extracted check frames, pixel QA log. |
| `07-publish-envelope.md` | Paste-ready title/description/tags/chapters/pinned comment, end-screen map. |
| `08-readout-schedule.md` | When to run the learning loop and what to compare. |

**Human touchpoints: exactly two.** The story in; the publish click out. The
pipeline never asks "which do you prefer" — it applies the rule, logs it, and
moves. If a needed input is truly absent and the policy has no default, the
run **halts with a named blocker** (see runbook §Stop conditions) — it does not
ask an open question and it does not invent the value.

**Data rules:**
- Every quantitative decision reads live data through the vidIQ tools listed in
  the runbook. No invented numbers. If a metric is not retrievable, write
  `not available via vidIQ` in the ledger and use the policy's default.
- Channel-relative before absolute. "Good" is defined against
  `channel-baseline.md` (the channel's own curve), not against raw counts.
- One measurement per fork, then move on. Do not re-query to shop for a nicer
  number; a re-score is allowed only where the policy names an iteration cap.
- Budget: a run spends at most the credit budget in the policy (default 200
  vidIQ credits pre-production, plus render/VO costs). Log spend per stage.

## Mandatory render rules

Operator rules, not preferences. They override convenience in every case.

1. **Time is seeked, not played — through a paused GSAP timeline.** The
   renderer opens the page headless and jumps to each frame. The engine drives
   `gsap.timeline({ paused: true })` registered on
   `window.__timelines[<composition-id>]`, one per composition. **There is no
   `seek(t)` entry point** — a hand-written `window.seek` is never called, and a
   composition built on one renders as a single flat colour for its whole
   duration (measured: mean |Δ| = 0.00 across five frames). Banned inside a
   composition: `requestAnimationFrame`, `Date.now`, `Math.random`,
   `performance.now`, `setTimeout`, `setInterval`, self-running CSS `animation`,
   autoplaying `<video>`/`<audio>`, network fetches, and any timeline not
   registered paused. **`npx hyperframes check` is the gate** (`[S7/R-1]`); its
   errors gate the run and its `sweep_static` refuses to pass a frozen render.
2. **Images: eager, sized, fitted, fallback-backed.** Never `loading="lazy"`.
   Always `loading="eager"` + `decoding="sync"`, explicit `width`/`height`
   attributes, explicit `object-fit`, and a background colour on the parent.
   **Project-relative paths** (`assets/plates/01.png`) — the bundler resolves
   them via `hyperframes.json` `paths.assets`. No `file://`, no `/mnt`.
3. **Layout math is Grid/Flex.** `position:absolute` only for full-bleed scene
   stacking and individual motion layers floating over the grid. Structural
   columns are never absolute.
4. **Verify by pixels, never by manifest.** Extract frame 0, each scene's
   settle frame, and the last frame (`scripts/extract_frames.sh`) and look at
   them. Fonts are the classic silent failure.
5. **Frame zero is the hook and the thumbnail candidate.** Never blank, never
   mid-fade, never a lone title on empty canvas.
6. **Assets exist before the composition does.** Asset strategy (browser-drawn,
   generated plates, licensed stock, mix) is decided by policy rule A-1 before
   any markup; a composition cannot invent a missing image.
7. **The composition is silent by design.** Voiceover and music are muxed
   onto the rendered MP4 afterward; the beat sheet carries the audio timing so
   both lanes agree. The VO's *measured* duration is the master clock.
8. **Ship with `debug-layout` off.** The class belongs on `#root`, never on
   `<body>` — a sub-composition's renderable surface *is* `#root`. Confirmed by
   inspecting frame 0.
9. **`box-sizing: border-box` first, every composition** (`[S6/A-5]`). A project
   missing it passes `check` completely clean and still ships a stage laying out
   576px taller than declared.
10. **Type floors and a 4.5:1 contrast floor on rendered pixels** (`[S6/A-6]`,
   `[S6/A-7]`). `check`'s Contrast pass enforces the text half; the hero-visual
   half has no automated check anywhere and is read off the extracted frame.
11. **Every claim is classified before the script is written, and an unsourced
   claim is attributed and flagged or it is cut** (`[K-1]`, `[K-2]`, `[K-2a]`).
   No tool checks this — `check` has no notion of a claim — so `[K-4]` reads it
   off the extracted frames. An unsourced **safety** claim, an unsourced
   **number**, and *treats / prevents / cures* never render at all, flag or no
   flag.

## The pipeline at a glance

```
S0 Baseline ──► S1 Story ──► S2 Topic gate ──► S3 Packaging ──► S4 Script+VO
     │             │              │                 │                │
 channel curve  brief from    keyword/outlier    title+thumb      script → VO →
 retention,     input, one    evidence ≥ policy  scored, iterate  measured
 traffic mix    presenter     or reframe topic   ≤ cap, best wins duration = clock
                                                                    │
S9 Readout ◄── S8 Envelope ◄── S7 Render QA ◄── S6 Composition ◄── S5 Beat sheet
 48h / 7d      title/desc/     check → render →  GENERATED from     beats from VO
 vs baseline;  chapters/       frames → pixel    the beat sheet;    timestamps;
 rewrite       end screen      checks → mux      spatial plan →     hook + chapters
 baseline      map             → ebur128         motion pass        + end-scene
```

Each stage has an entry condition, a fixed set of tool calls, an artifact, and
an automatic gate. Gates either **pass**, **auto-fix within a cap**, or **halt
with a named blocker**. None of them ask.

Model-tier protocol: S0–S4 and S8–S9 are data pulls and CRUD — run them on the
cheaper tier. S5–S7 (structure, spatial reasoning, pixel QA judgement) are where
the stronger tier earns its cost. Flag the switch at the S4→S5 and S7→S8
transitions, not every turn.

## What "educational" changes

An explainer has a spine, and the spine is what the beat sheet is built on:

1. **Hook** — the payoff or the tension, stated as a claim, in frame 0.
2. **Misconception** — what the viewer currently believes and why it's wrong.
3. **Mechanism** — how it actually works, one moving diagram, one idea per beat.
4. **Proof** — the evidence, shown not narrated (a number, a comparison, a source).
5. **Application** — what to do differently, concrete, in the viewer's context.
6. **Recap + handoff** — three-beat summary, then the end-screen scene.

`decision-policy.md` §S fixes the time split across these by format and length.
A story brief that cannot fill all six is not ready; the S1 gate reframes it,
it does not ask.

## Posture: what keeps faceless from reading as generic

The default of this category — AI voice, stock B-roll, centred sans type, slow
zoom, ambient pad — is what to design against. The levers that differentiate:
one grade and grain across every plate; motion that encodes meaning (depth =
sequence, size = magnitude, position = time); type as the performer when there
is no face; **an entrance idiom chosen per beat rather than one ease for the
whole video** `[S6/A-10]`; **hard cuts on a timing grid for a Short, a 2-3 type
transition system for long-form, and never a plain crossfade across a ground
change** `[S6/A-8]`; **continuity across the cut — a camera path and actors
that persist rather than being redrawn** `[S6/A-9]`; one signature component
per video; silence as a choice with captions carrying content.

## Companion skills and tools

| Skill / tool | Role in the pipeline |
|---|---|
| `frontend-design` | Taste and token discipline; read before S6. |
| vidIQ MCP (`vidiq_*`) | The data layer. Exact calls per stage in the runbook. |
| HyperFrames CLI / MCP | Render engine. Verify API against the installed version. |
| Higgsfield MCP | Plate generation when policy A-1 selects generated imagery. |
| `/hyperframes-animation` | The implementation library: 48 atomic rules, 22 blueprints, the transition catalog and its machine registry. `[S6/A-8]`/`[S6/A-10]` name its rules exactly; do not invent equivalents. |
| `/hyperframes-keyframes` | Punch-in, reframe, Ken Burns on a non-timed wrapper; routes match-cut and whip pan back to `-animation`. |
| `design:design-critique` | Optional review pass on extracted frames, not code. |
| `marketing:draft-content` | Description/pinned-comment copy if a house voice exists. |
| `web-artifacts-builder` | Preview harnesses only — never render compositions. |

## Failure modes this version is built to prevent

- Asking the operator to choose a title, a hook, a length, a presenter, a
  colour, a voice, or a scene layout. All of these have a rule.
- Starting the composition before the voiceover exists, then re-timing everything.
- Treating a title or thumbnail as final without a score, or re-scoring
  endlessly to chase a number.
- Diagnosing a "bad video" without first classifying CTR-failure vs
  retention-failure against the channel's own curve.
- Rendering an efficacy claim the project cannot source, on the strength of a
  badge doing all the disclosure work alone.
- Building against recalled HyperFrames attribute names, or against a second
  gate that disagrees with the engine's own.
- Applying the Short's cuts-only default to a long-form piece, so all N
  boundaries are hard cuts and the result reads as a slide deck even though
  every cadence, safe-area and contrast gate passed `[S6/A-8]`.
- Letting a timeline's `defaults: { ease }` be the real entrance signature of a
  whole video, then counting explicit occurrences of that ease and concluding
  the motion is varied `[S6/A-10]`.
- Splitting scene files by narration sentence, so the same diagram is redrawn
  in consecutive scenes instead of one sub-comp rearranging its actors
  `[S6/A-9]`.
- Reading `check`'s `motion.enabled: false` as "motion verification was turned
  off". There is no flag: it means no `*.motion.json` was written `[S7/R-1b]`.
- Any `[NOT IN SKILL]` finding from a run that is not written back to the
  policy or the baseline within the same session (see `learning-loop.md`).
