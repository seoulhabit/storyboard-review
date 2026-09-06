# T3 — Policy rewrite (`references/policy.md`, `references/youtube-delivery.md`) — DONE
Commit `claude-skills/fvc-004/makemeavideo` branch, `references/policy.md` and `references/youtube-delivery.md`.

## What shipped

`references/policy.md` (768 → 864 lines) and `references/youtube-delivery.md`
(162 → 173 lines) had every retired-engine cross-reference rewritten in place.
Full disposition, one row per finding:

| Where | Was | Now |
|---|---|---|
| Preamble (policy.md:8-13) | "read `check`/`seek`/GSAP/composition as the H-* rule... until T3 strips it" | Rewritten as a completed-state note; T3 is this commit |
| Carried-block HTML comment (policy.md:196) | "stripped in T3" | Rewritten past-tense, names what folded into `H-4` |
| `B-1`, `B-3`, `S-1`, `S-2`, `S-4`, `V-1`, `V-3`, `E-2`, `L-2` reads (8 occurrences) | `<CHANNEL>/baseline.yaml` | `<CHANNEL>/channel.yaml` — see the note below on why `channel.yaml` won |
| `B-3` (traffic schema note) | cited `assets/channel-baseline.template.yaml` | `assets/channel.template.yaml` — that file did not exist under the old name |
| `S-4 · Voice` | `vidiq_voiceover_list_voices`, "write it to baseline" | `heygen.voice_id` from `channel.yaml`, a one-time T2 pick; `BLOCKER-SETUP-PENDING` if unset |
| `K-2`(2) flag mechanism | `catalog/visual-components/unsourced-flag/`; "the `flag` beat role in `scripts/beats_to_composition.py` emits it" | the build spec's style block (`H-1`) instructs the flag treatment directly as a scene note — no generator, no beat role to carry it |
| `K-4` | reads `[S7/R-2]`'s frames; "`hyperframes check` has no notion of a claim"; five checks stated as one undifferentiated list | reads `qa_render.py`'s frame inventory + `H-6` timing; **honest split** — 3 of 5 sub-checks are mechanically measurable (claim→scene map, flag not in accent, no internal id), 2 require reading the words (concurrent flag, hedge/prohibition) and are routed to the `design-critique` gate or the operator, not silently claimed as automated |
| PR-section naming note | cited `R-1` (a rule id not defined anywhere in this file) | deleted wholesale |
| `PR-2 · Voice provider` | `gemini-tts` default / `current-vo` (Higgsfield) fallback, `listening-test pending` | HeyGen is the only provider; no fallback branch (an unreachable HeyGen halts the run, it does not reroute); 2.1.0 providers named once as "superseded, for the reader who remembers them" |
| `PR-3 · Budget` | one $5.00 + 200-credit blended cap, 80%/100% thresholds | two separate caps, HeyGen credits (`H-7`, `per_run_cap`) and vidIQ credits (`vidiq_preproduction_cap`, 200), never summed or converted; `usd_per_credit` is report-only |
| Credit table, S4 row | "voiceover... only when `current-vo` fires per PR-2" | dropped — voiceover is a HeyGen credit spend now, not a vidIQ one; table retitled to say so |
| `V-2 · Voiceover generation` | "whichever provider PR-2 selects"; `vidiq_voiceover_generate` | `create_speech` pre-flight, per-scene, explicitly framed as measuring the master clock, not shipping audio (Video Agent re-synthesises at build time with the same voice) |
| `C-2` cadence check | `scripts/beats_to_composition.py` enforces at generation time; post-render answer is `[S7/R-2]`; cites `[S6/A-8]`,`A-9`,`A-10` (undefined in this file) | enforcement moves to `scripts/validate_beat_sheet.py` at S5 (a script that actually exists); the 2.0s/1.5s hold numbers are now **stated once here** and `H-4` reads them from this rule instead of duplicating them; the "reads like a slide deck" risk is routed to `design-critique`, not to three undefined rule ids |
| **`C-3a` — new** | did not exist in this file | **ported from `faceless-video-craft` 2.2.0** (in-flight, uncommitted, on another session's checkout — see §8.7 below) — brand end-card, every video, every format. Content unchanged from the source; delivery mechanism changed from "mount `catalog/visual-components/seoulhabit-endcard/`" to "describe the scene in the build spec," since a HeyGen render has no local component to reuse |
| `A-2`, `A-3`, `A-4`, `A-6`, `A-7`, `R-2`, `R-3` | seven separate carried rule *bodies*, four of which (`A-6`,`A-7`,`R-2`,`R-3`) deferred their "full text" to `references/restored-v1-rules.md` — **a file not shipped in this skill**, i.e. four live `BLOCKER-SKILL-FILE` conditions sitting inside the rulebook | **retired wholesale**, replaced by a `§A/§R — retired, folded into H-4` banner naming exactly what folded where. `A-2` ("one accent per frame") → `H-1`'s style block. `A-6`/`A-7`/`A-4`/`R-2`/`R-3`'s measured numbers, hero-visual doctrine, frame inventory, hold-limit, catalog-reuse instruction and loudness band → rewritten directly into `H-4` (see below). The seven ids remain valid only as provenance tags on an old ledger line. |
| Stop conditions | 4 tokens listed by name (`BLOCKER-TOOLS` naming the HyperFrames CLI, `BLOCKER-CHECK`/`BLOCKER-PIXEL` retired, `BLOCKER-BUDGET` at "2× the ceiling" — contradicting `H-7` and the rewritten `PR-3`), while **23 tokens are actually referenced across the skill** | full canonical registry, all 23, cross-referenced to the rule that raises each; `BLOCKER-TOOLS` now names HeyGen MCP; `BLOCKER-BUDGET` now matches `PR-3` (halt before crossing, not "2×"); `BLOCKER-ROUTE` kept but flagged as dangling (cites an `S-7` this file never defines, even pre-T3) since an old run's ledger may still cite it |
| `youtube-delivery.md:6` | `<CHANNEL>/baseline.yaml` | `<CHANNEL>/channel.yaml` |
| `youtube-delivery.md:18-27` | "the generator emits `data-resolution=...`, the matching `#root` dimensions" | "the beat sheet's `canvas` is declared; `H-1`'s build spec declares the aspect; `qa_render.py` asserts the delivered file's real dimensions (`H-4`)" |
| `youtube-delivery.md:32-38` | cited `[S6/A-8]`, `[S6/A-9]`, `[S6/A-10]` (undefined) for long-form continuity | rewritten to name `H-1`'s style-block instruction and the `design-critique` gate as where continuity is actually caught |
| `youtube-delivery.md:86-94` | "the generated scene draws the zones in `#root.debug-layout`" as the first of three escalation rungs | that rung deleted (nothing emits DOM); the other two (extract_frames.sh eye-check, check-safe-area.py gate) survive, `check-safe-area.py` now explicitly named as running inside `qa_render.py` / `H-4` |
| `youtube-delivery.md:125` | "elements YouTube draws on top of *the composition*" | "...on top of *the delivered video*" |
| `youtube-delivery.md:139` | "the composition as one node" | "each video as one node" |
| `youtube-delivery.md:143` | **the load-bearing one — this sentence had gone false**: "the composition is silent by design; VO and music are muxed afterward" | HeyGen delivers a muxed MP4 with its own VO and music bed; there is no local mux step; the S4 pre-flight's duration is still the master clock, the delivered runtime is what `H-4` gates |
| `youtube-delivery.md:148` | caption floor cited `[S6/A-6]` (42–56px) as if `qa_render.py` enforced it per role | rewritten: 42–56px is the authoring target the build spec requests; the delivered floor `H-4` can actually gate without a stylesheet is the single absolute 32px floor |
| `youtube-delivery.md:150-153` | a `loudnorm` two-pass mastering recipe (`TP=-2.5`, AAC headroom) with no mux step to run it against | reduced to the measurement doctrine only — target −14 LUFS / ≤ −1 dBTP, measured on the delivered file, because there is nothing to master locally |

## `H-4`, in full, after the fold

`H-4` now states, inline, in the order it must pass: canvas assert (folded
`A-4`) → contrast 4.5:1 + hero-visual reading clause (folded `A-7`) → type
floor, narrowed to a single absolute 32px (folded `A-6`, narrowed — see below)
→ safe-area → static hold at the numbers `C-2` states (folded `R-2`'s
frame-inventory and hold-limit doctrine, its catalog-reuse instruction, and
its "confirm the canvas/scene constants" warning, now aimed at `qa_render.py`'s
own configuration rather than a project's `index.html`) → loudness band and
true-peak, measured on the delivered file only (folded `R-3`, its `loudnorm`
encode step dropped since there is no local mux) → duration.

## The one deliberate narrowing, stated plainly rather than silently implemented

`A-6`'s type floors were **per role** (hero 96–160px, body ≥40px, captions
42–56px, labels 26–32px) because they were measured against a stylesheet that
declared a region's role. A HeyGen render has no stylesheet and
`qa_render.py` cannot attribute a detected text region to a role without one.
`H-4` therefore enforces only the single number A-6 itself called absolute —
**no measurable text region below 32px** — plus an advisory per-scene height
distribution for a human to catch a role reading too small even above that
floor. `youtube-delivery.md`'s caption target (42–56px) survives as an
authoring instruction to the build spec; it is not something the pixel gate
checks per role. This is a real reduction in what is mechanically gated, not
a hidden one — it is stated in both files.

## Two things fixed here that are not in the WO's own T3 acceptance text

1. **The stop-conditions registry was 4 tokens naming things this skill no
   longer has** (the HyperFrames CLI, a "2× the ceiling" budget rule that
   contradicts `H-7`, and two retired `BLOCKER-CHECK`/`BLOCKER-PIXEL` tokens)
   **while 23 tokens are actually raised across the skill.** Rebuilt as the
   canonical registry, cross-referenced to the rule that raises each.
2. **Four rule ids (`A-6`, `A-7`, `R-2`, `R-3`) deferred their full text to
   `references/restored-v1-rules.md`, a file this skill does not ship.**
   Carrying them forward as separate bodies would have created four live
   `BLOCKER-SKILL-FILE` conditions inside the rulebook itself. Folded into
   `H-4` instead, per WO-FVC-004 §8.6.

## §8.7 — the `C-3a` port, and what it means for `faceless-video-craft`

`faceless-video-craft` (`~/Desktop/claude-skills/faceless-video-craft/`) has
five uncommitted files, on another session's working tree, bumping the skill
to an unreleased 2.2.0 and adding rule `C-3a` (a shared brand end-card, every
video, every format). WO-FVC-004 §7 requires that skill frozen and read-only.
This task does **not** touch that working tree — `git status` on
`claude-skills` after this commit shows the same 5 modified files, unchanged,
that existed before this session started. But `C-3a`'s *content* — a brand
sign-off scene, sourced from a real gap (two videos each built one from
scratch, neither using the channel's actual mark) — is engine-independent: it
is a build-spec instruction, not a composition mechanism. Porting it here
credits its origin and prevents it from being lost to the freeze conflict.
See WO-FVC-004 §8.7 for the full account.

## Verified, not assumed

```
$ grep -n -iE 'hyperframes|seek\(|gsap|#root|motion\.json|box-sizing|higgsfield|current-vo|gemini-tts' references/policy.md
12:`check`, `seek`, GSAP, a composition or a motion sidecar now points at the
488:- **Superseded, for the reader who remembers them:** `gemini-tts`, `current-vo`
489:  (Higgsfield `generate_audio`) and `vidiq_voiceover_generate` were the 2.1.0
725:`R-3`) governed a local HyperFrames composition and the `check` CLI's audit of
810:  (`H-0` names the permitted set — the HyperFrames CLI this token used to name
```
All four are this document's own retirement-history prose, not live
cross-references. No other file under `references/` matches.

```
$ python3 -c "... every §H rule has reads/rule/default/ledger ..."
H-0    reads=True rule=True default=True ledger=True
H-1    reads=True rule=True default=True ledger=True
H-2    reads=True rule=True default=True ledger=True
H-3    reads=True rule=True default=True ledger=True
H-4    reads=True rule=True default=True ledger=True
H-5    reads=True rule=True default=True ledger=True
H-6    reads=True rule=True default=True ledger=True
H-7    reads=True rule=True default=True ledger=True
F-2    reads=True rule=True default=True ledger=True
I-1    reads=True rule=True default=True ledger=True
```

**Not verified, and I'm not claiming otherwise:** the acceptance grep was run
against `references/policy.md` and `references/youtube-delivery.md` only, per
this WO's stated scope. `assets/beat-sheet.schema.json` (carried verbatim,
351 lines) still describes GSAP-generated transitions, actor ids and a
composition generator in several field `description`s — it is valid JSON and
unchanged, but its prose is now stale in the same way the policy file's was.
Flagged for T4: `scripts/beats_to_build_spec.py` should read only the
generator-agnostic subset of this schema (`id`, `start`, `duration`,
`section`, `layout`, `beats`) and ignore the GSAP/transition/actor fields
entirely — not fix the schema's prose, which is out of this task's scope.
T3 did not run `tests/run.sh` (no test suite exists yet — that is T4) and did
not verify the `learning-loop.md`/`providers.yaml`/`runbook.md` files beyond
the grep sweep above (they were already clean before this task; SKILL.md
likewise).

## Judgment calls made

- **`channel.yaml` over `baseline.yaml`.** The scaffold's majority usage
  (SKILL.md, every §H rule, the runbook) already said `channel.yaml`; the
  carried block was the minority holdout. `channel.yaml` also matches the new
  file's actual contents — `assets/channel.template.yaml` carries a `heygen:`
  picks block the old `baseline.yaml` shape never had. Renaming the *live*
  repo file (`videos/_channel/baseline.yaml`) is a repo-side change, not part
  of this skill-side task; not done here, tracked in the WO.
- **Fold, not carry, for `A-6`/`A-7`/`R-2`/`R-3`.** Decided in the WO itself
  (§8.6) before this task started; this status file records the resulting
  text, not a new decision.
- **`C-3a` ported with attribution, not silently authored fresh.** The rule's
  content, evidence, and even its exact copy defaults are the other session's
  work; only the delivery mechanism (component-mount → described scene)
  changed.

## Not done (correctly out of scope for T3)

- `references/learning-loop.md`, `references/providers.yaml`,
  `references/runbook.md`, `SKILL.md` — already clean, confirmed by grep,
  not rewritten.
- `assets/beat-sheet.schema.json`'s stale prose — flagged above for T4.
- Renaming the live `videos/_channel/baseline.yaml` file itself, or any other
  repo-side (non-skill) file — that is a Story Board repo change, not a
  `claude-skills` skill change, and is out of this task.
