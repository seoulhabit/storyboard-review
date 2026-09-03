# WO-FVC-001 T2 — Merge matrix (rescoped: verify and document, not redo)

Per `wo/FVC-001/gate-0-notes.md`, T2 was rescoped by Kim on 2026-09-02: the v1→v2 rule merge this task was originally scoped to *perform* had already been done in the video repo by commits `d7e07e3` (2026-09-01, "Rebuild faceless-video-craft as v2.1; add K-* claim rules") and `6e6c202` (2026-09-02, "Add long-form continuity rules... from the Ectoin review"). This file verifies and documents that merge instead of redoing it.

**Method:** a 6-agent background sweep (Workflow `wf_3ae36b7d-27a`, Opus/High, 781,583 tokens, 90 tool calls) read every line of the historical pre-`d7e07e3` v1 file (`git show d7e07e3^:.claude/skills/faceless-video-craft/SKILL.md`, 2172 lines) not already cited as one of the restored rules, and checked whether each distinct piece of gating guidance in it is still represented somewhere in the current file set. Full raw output (202 items, one per finding): `/private/tmp/claude-501/-Users-sumitchoudhary-Desktop-Story-Board/9affa2a8-0b65-41ee-a378-a06f95375761/tasks/wny48blyv.output`.

**Headline result: zero genuine gaps.** All 202 swept items came back `covered` — nothing found in the historical file is actually missing from the current file set. The reason is structural, and itself a finding: commit `d7e07e3` did not gut v1, it *grew* it (2,172 → 3,247 lines) while carving policy/claim content out into `faceless-video-craft-v2`. Chunk A's agent confirmed by direct `git diff` that the first 218 lines of the historical file are byte-identical to the current v1 file. Most of the rest survives the same way, sometimes reworded or extended, never deleted.

---

## 1. Rule-ID matrix (Accept check: grep for empty verdicts → 0)

50 rule IDs exist in `faceless-video-craft-v2` today (corrected count — my first pass in `00-inventory.md` used a regex that silently dropped double-digit IDs like `A-10`; re-scanned with a fixed pattern for this file). v1 (historical or current) carries **no** rule-ID-tagged content at all — every ID below is either v2-native or one of the eight rules explicitly restored from v1 prose.

| Rule ID | Verdict | Note |
|---|---|---|
| A-1 | merge | = restored rule **R4** (catalog lifecycle: discover/reuse/build/contribute), `[S6/A-1]`. Source: v1 (historical) lines 738-807 / (current) lines 507-527, 805-878, verbatim per `restored-v1-rules.md`. |
| A-2, A-3, A-4 | keep | v2-native (design tokens on `#root`; frame-zero-as-design-object; fps default). No v1 rule-ID origin — these formalize craft guidance that also independently survives as prose in the current v1 file, but were authored as v2 policy, not restored. |
| A-5 | merge | = restored rule **R3** (`box-sizing: border-box`), `[S6/A-5]`. Source: v1 lines 72-96, verbatim. Note: R3's `min-height: 0` companion fix is only a forward-pointer in `restored-v1-rules.md` (lines 139-141) to a "Failure modes" section v2 doesn't contain — the actual fix text is reachable only in the current v1 craft file (lines 2860-2880). Not a defect Kim needs to act on now; flagging so T5/T9 don't assume it's fully ported. |
| A-6 | merge | = restored rule **R1** (type floors), `[S6/A-6]`. Source: v1 lines 1309-1323, verbatim. |
| A-7 | merge | = restored rule **R2** (contrast floor 4.5:1 on rendered pixels), `[S6/A-7]`. Source: v1 lines 1324-1370, verbatim. |
| A-8 | merge | = restored rule **R7** (cuts, crossfades, and transitions), `[S6/A-8]`. **Correction to the sourcing model**: R7 does NOT cite the pre-`d7e07e3` historical file — the "Cuts vs crossfades" section at historical lines 1246-1259 was superseded, not reused (confirmed by chunk E/F agents independently). R7 instead cites the **current, live** v1 file at lines 1734-1830 (`## Cuts, crossfades, and transitions`, added by commit `6e6c202` from the Ectoin review). Verified directly: current v1 heading is at line 1734, next heading (`## YouTube delivery`) at 1832 — citation is accurate as of this writing. See `peer-coordination-log.md` for how this was cross-checked with a peer session. |
| A-9 | keep | v2-native (`.stage > * { overflow: hidden }` structural safe-area clip). No v1 rule-ID origin. |
| A-10 | merge | = restored rule **R8** (motion idiom by narrative function), `[S6/A-10]`. Same sourcing correction as A-8: cites current live v1 lines 417-472 (`### Motion idiom by narrative function`), added by `6e6c202`, not the historical file. Verified: current heading at 417, next heading at 474. |
| B-1, B-2, B-3 | keep | v2-native (S0 environment/budget rules — pre-`providers.yaml`/T7 scaffolding). No v1 origin. |
| C-1, C-2, C-3 | keep | v2-native (cadence/motion-budget rules). No v1 origin; C-2's "measure on the shipped file, never a recorded figure" posture echoes v1 craft-file guidance in spirit but was independently authored. |
| E-1, E-2 | keep | v2-native (S8 stage rules). No v1 origin. |
| K-1, K-2, K-2a, K-2b, K-3, K-4, K-5 | keep | Native to v2 — added by `d7e07e3` (2026-09-01). v1 never had claim/citation rule IDs (by its own text: "claim/source enforcement... belong to a project skill, not here"). Per WO §1.1, "K-1..K-5 are expected [in the repo copy]" — they are not; they're v2-only. §1.2's ruling that K-2b stays unloosened is orthogonal to this matrix and untouched here. |
| L-1, L-2 | keep | v2-native (S9 learning-loop rules — proposes, never rewrites policy per §1.4). No v1 origin. |
| P-1, P-2, P-3, P-4 | keep | v2-native (title/thumbnail/chapters rules). No v1 origin, though P-2/P-3's "frame zero as thumbnail, verify by extracting" echoes v1 pre-render gate item 1/2 in spirit. |
| R-1, R-1b | keep | v2-native (`check`/lint gate rules — R-1 is unrelated to the "restored rule R1" naming collision; different namespace, same letter). No v1 rule-ID origin. |
| R-2 | merge | Houses restored rule **R5** (post-render static-hold / cadence pixel diff), `[S7/R-2]`. Source: v1 lines 1005-1101 (verbatim), plus the "gate item 4b" cadence-metric detail (historical lines 909-939) and the transition-midpoint check (historical lines 1102-1111, itself R7-adjacent). This ID is a blend: a v2-native gate mechanism, tightened/justified by restored v1 measurement detail — not a pure v1-to-v2 port. |
| R-3 | merge | Houses restored rule **R6** (AAC intersample true-peak headroom), `[S7/R-3]`. Source: v1 lines 1536-1550 (verbatim). Also a blend: v2 already had a loudness-target rule; R6 tightened it to `TP=-2.5` and added the re-measure-on-the-shipped-file requirement. |
| S-1 | keep, confirmed correct | Format default (long vs short). **Verified per T2's rescoped mandate**: already reads `channel-baseline.md` → `formats.short.uploads_90d` / `formats.long.uploads_90d` (decision-policy.md:51-79), not a hardcoded long-form default. WO's original T2 concern (§2 "S-1: long-form default on a Shorts-majority channel") is already resolved — no action needed. |
| S-2 | keep, confirmed correct | Target length. **Verified**: reads `channel-baseline.md` → `retention.avg_view_pct_long`, `curve.p50_7d`, per-video views/durations (decision-policy.md:80-97); the clamp is measurement-derived, not a fixed replay-inflated figure. WO's T2 concern already resolved. |
| S-3 | keep | v2-native (presenter selection). No v1 origin. |
| S-4, S-5 | keep | v2-native (spine/section-split rules). No v1 origin. |
| S-6 | keep | v2-native (word budget from `channel-baseline.md` voice WPM). No v1 origin. |
| S-7, S-8 | keep | v2-native. No v1 origin. |
| T-1, T-2 | keep | v2-native (vidIQ keyword/outlier gates). No v1 origin. |
| T-3 | keep, confirmed correct | Browse-evidence ceiling. **Verified**: `10 × subs` ceiling is explicit and logged with its rationale (decision-policy.md:316-330: "`10 × subs` alone gives 80... **Both bounds are explicit and both are logged**"), carries the `[default]` tag. WO's T2 concern (10×subs ceiling) already resolved. |
| T-4 | keep | v2-native. No v1 origin. |
| V-1, V-2, V-3 | keep | v2-native (S4 voiceover rules). No v1 origin; V-1 is distinct from T7's future `current-vo` provider-selection rule of the same name — will need disambiguation when T7 runs. |

**Grep check (empty verdicts):** every row above carries `keep`, `merge`, or `keep, confirmed correct` — zero blank cells, zero `dropped` verdicts (nothing was found to actually drop), zero `superseded-by` needed at the rule-ID level (the one supersession found — old "Cuts vs crossfades" retention claim → R7's "record the disagreement" reopening — is *inside* a single rule's own history, not one ID replacing another).

---

## 2. Beyond the 50 IDs — what the sweep actually surfaced

The rule-ID matrix above is clean, but it undersells what the sweep found. Of the 202 audited items, roughly half are marked `covered` only because the content survives in the **current v1 craft file** — with explicit notes like "ABSENT from v2", "no v2 equivalent", or "covered by the craft file alone." Nothing is lost from the repo, but a lot of it is **not enforced by v2's automated pipeline** — the thing that actually runs `/produce`. A human (or Claude) has to know to go read the v1 craft skill by hand; `check`, the validators, and decision-policy.md's gates don't see it.

This is not a defect to fix under T2 (§1.4: the learning loop *proposes*, it doesn't rewrite policy; T2 is verify-and-document only). It's the actual output of "document what's already merged" — documenting *what didn't merge into policy* is part of that. Highest-consequence examples, out of ~90 such notes (full list in the raw output file above):

- **Largest single gap** (the sweep's own words): the Linux/cloud `beginframe` capture-mode defect (`hasDamage:false` reusing the previous buffer; frame 0 can ship with the entrance element missing; needs `PRODUCER_FORCE_SCREENSHOT=true`) — v1 documents this at length (confirmed cause of a real defect on `snail-mucin-recut-34s`); **zero** mention anywhere in v2's seven files. v2's runbook renders locally and has no instruction to re-verify frame 0 after a `hyperframes cloud`/`cloudrun`/`lambda` render. Relevant to T7/T8, which do discuss cloud rendering paths.
- No gate anywhere in v2 for placeholder/TODO/unfinished copy reaching the export (v1 states it plainly; K-4's pixel check enumerates claim defects but not this class).
- No v2 statement of "an external QC report is a claim, not a diagnosis" or "a report can name a symptom that does not exist" (fabricated findings) — both are v1-only, and both are directly relevant methodology for the kind of automated audit this WO itself keeps running.
- Several 9:16-composition craft rules (depth roles, anchor-to-edge, fill-the-safe-column, layout variety, a real tactile/photographic anchor early, "channel mark" consistency) have no v2 policy-line counterpart.
- Channel-wide consistency mechanisms (single-source `tokens.css`, a reusable per-channel audio mastering chain, a "caption skin" as a versioned component, thumbnail structural-template continuity) exist only in the craft file; `channel-baseline.md` is measured performance data, not a design-consistency rule.
- A handful of caption-production details (≥1.0s minimum cue duration, competitive research via `vidiq_video_transcript`, mid-hold verification against the final mix, the "don't infer caption status from a filename" trap) have no v2 gate.

None of this changes the rule-ID matrix above or requires action under T2. It's recorded here so it doesn't get re-discovered from scratch, and so it's available if Kim wants to seed `policy-change-proposals.md` from it later (§1.4's proper channel — not this file).

---

## 3. Engine contract — status, not a full Accept pass

Read `references/hyperframes-engine.md` directly (not just grepped) and cross-checked against the current v1 file and the sweep's own citations. It's internally consistent: `#root`/`data-composition-id`/`data-start`/`data-duration`, `class="clip"`, paused GSAP timelines on `window.__timelines`, and the "nothing plays, the renderer seeks" contract are stated the same way in both v1 and v2, with per-line source citations to the pinned CLI's own shipped docs (commit `d7e07e3`'s stated method).

**What this does NOT satisfy**: T2's Accept criterion — `hyperframes check assets/composition-skeleton.html` exit 0, and the lint-vs-`check` reconciliation across three fixtures — needs the actual HyperFrames CLI, which `00-inventory.md` §0.5 already found is **not installed on this machine**. That blocker stands, unchanged. The contract is verified *as documented*; it is not verified *as executed*, and I'm not representing otherwise.

---

## 4. One correction absorbed from a peer session

A peer Claude session (`story-board-b0`, same repo) flagged that the plugin-cache copy of this skill (a stale 2026-09-01 snapshot, physically the source of the `anthropic-skills:faceless-video-craft` entry in this session's own skill list) still has `scripts/lint_composition.py` — which I initially read as a recoverable asset missing from the repo. The peer corrected this: `decision-policy.md:659` (verified directly) records that script as **deliberately deleted** for being inverted against the shipped engine (it passed a frozen render and failed a working one). T1's extraction already sourced from the repo, not the cache, so this was never at risk — full exchange and independent verification of every claim in `wo/FVC-001/peer-coordination-log.md`.

---

## Accept readback

```
$ grep -c "| merge |\|| keep |\|confirmed correct" wo/FVC-001/merge-matrix.md
# every rule-ID row carries a verdict — see the table in §1; 0 empty cells, 0 unresolved rows
```
