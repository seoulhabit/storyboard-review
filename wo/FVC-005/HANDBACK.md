# WO-FVC-005 — Handback (T0–T7, full close)

This document originally closed T0–T3 only (S-A ground truth + S-B compiler).
This pass extends it through **T7** — T4 (audio + render harness, plus R-6),
T7 (skill cut to 0.3.0, run out of order), T5 (pilot run, `centella-asiatica`),
and T6 (recurrence) — and is the **T8** deliverable itself: the WO's own §7
close-out. The T0–T3 content below is preserved verbatim except where a later
task resolved something it left open; those spots are marked inline.

**Where things stand at close:** `makemeavideo` is at **0.3.0** on
`origin/master` in `claude-skills` (merged, not a branch); the design system
extraction, R-6 safe-area widening, and the render/compile harness are merged
to `master` in this repo; one real pilot (`centella-asiatica`) ran the full
pipeline end-to-end and its envelope sits in `videos/centella-asiatica/`;
`videos/_queue.yaml` holds 20 queued routes plus that one produced entry, and
`/makemeavideo next` can pop the queue without a human picking the next slug.
Two touchpoints remain genuinely human every run: the story in, the publish
click out (WO §0.1) — nothing done this session moved either of those off a
person.

---

## 1. Attestation table

| Task | Accept check | Command | Output excerpt |
|---|---|---|---|
| T0 | Render machine proven end-to-end | `hyperframes init t0-check --example blank && hyperframes check --json && hyperframes render -q draft -o out.mp4` | `ok: true`, all 0 errors; `18.5 KB · 10.0s video · rendered in 24.6s` |
| T1 | Pre-written criteria, honest verdicts | `cat wo/FVC-005/T1-FINDINGS.md` | F1 **PARTIAL** (rule C-6 fired); F2–F4 **BLOCKED-CONNECTOR** (named, not guessed) |
| T2 | MANIFEST.json re-derives clean | `python3 -c "…sha256 re-check…"` | `63/67 files checked, 0 mismatches` (67 after the vendored GSAP file was added) |
| T2 | Engine contract re-verified at 0.8.30 | `diff -rq <0.8.22 cache>/dist/docs <0.8.30>/dist/docs` | empty — byte-identical |
| T3 | Compiler lints clean | `hyperframes lint 06-render/9x16` | `0 error(s), 0 warning(s)` |
| T3 | Compiler passes the full gate, both canvases | `hyperframes check --samples 40 --at-transitions --json` on 9x16 and 16x9 | `"ok": true` both times, all 5 categories `errorCount: 0` — `wo/FVC-005/t3-verification/check-{9x16,16x9}.json` |
| T3 | Second static gate | `python3 lint_composition.py index.html compositions/frames/*.html` | `0 error(s), 0 warning(s) across 6 file(s)` |
| T3 | Real local render | `hyperframes render -q draft -o out.mp4` + `ffprobe` | `1080x1920, duration=14.600000, codec_name=h264` |
| T3 | Determinism | two independent compiles, `diff -r` | empty |
| T3 | Dual-format timing invariance | `diff` of both canvases' `index.motion.json` | identical `duration` and `assertions` |
| T3 | Repo gates (plan Step 10, D6) — run, not clean at the time | `check-legibility.py`/`check-safe-area.py`, both canvases | Legibility: token floor passes both, render check fails 16:9. Safe-area: **failed both** at T3 time — root-caused to `videos/_system`'s own tokens, **resolved by R-6 at T4** (see below) |
| T4 | R-6 safe-area widening closes T3's finding #20 | recompiled T3's synthetic fixture, re-rendered both canvases, re-ran `check-safe-area.py` | both canvases now `no findings` — `wo/FVC-005/t4-verification/README.md` |
| T4 | Audio + render harness produces a real mixed/loudnormed track and a full check→render→extract→QA pass | `render_local.sh` on the T3 fixture, then a real beat sheet | `mix_audio.py` output passes `qa_render.py`'s `gate_h4_loudness`; `render_local.sh` exits clean end to end — `wo/FVC-005/t4-run-report.md` |
| T7 | Skill rewritten and re-versioned; local engine referenced correctly throughout, no dangling HeyGen Video Agent calls in S4b–S7 | `grep -rn "video_agent\|create_video\b" makemeavideo/{SKILL.md,references/*.md}` post-edit | zero matches outside the now-forbidden tool-fence list itself |
| T7 | `baseline.yaml` carries a resolved `heygen:` block | `python3 -c "…yaml_lite.parse…"` | `voice_id: null, brand_glossary_id: null, cloud_render_credits_cap: 20, spike_findings: {…T1-FINDINGS verbatim…}` |
| T5 | Full pilot run (`new` mode) reaches the envelope, no rule loosened to get there | `/makemeavideo centella-asiatica` from a fresh worktree, S0.0 through S8 | `videos/centella-asiatica/07-publish-envelope.md` written; `09-run-report.md` §Summary posted verbatim as the session's final message |
| T5 | Rendered MP4 passes the compiled pipeline's own gates (H-2, H-4 minus H-3's known false-positive class) | `qa_render.py` on the real render | H-2 pass, H-4.safe-area pass (post-R-6), H-4.loudness pass (-14.0 LUFS / -12.5 dBTP), H-4.duration pass (45.5/45.5s); H-3 fail — visually confirmed false positive (bold typography, no face), documented per T7's H-3 fallback, evidence frames saved |
| T5 | Git LFS carries the real MP4 correctly | `git lfs ls-files` on the commit | `videos/centella-asiatica/06-render/9x16/renders/centella-asiatica-9x16.mp4` listed, LFS pointer confirmed, not a raw blob |
| T6 | `/makemeavideo next` pops the queue and resolves a real request without a human naming the slug | `enqueue_from_site.py` dry run + a `next` invocation against the populated queue | `videos/_queue.yaml` round-trips through `_yaml_lite.py` clean (write then parse-back verified); `queue[0]` (`ceramide`, 8 citations) resolves to a valid `request.yaml`/`story.md` pair |
| T6 | `centella-asiatica` is correctly recognized as already produced, no unrelated pipeline's report files false-match | `enqueue_from_site.py` against the real repo state | `produced[]` backfilled with exactly 1 entry (`centella-asiatica`), the 4 unrelated `09-run-report.md` directories from the older pipeline correctly excluded |
| T8 | This document, plus the WO's own §7 checklist (cost table, T1-FINDINGS, rulings needed, refusals, attestation) | this file | below |

## 2. Refusals on record

| What | Reason | §0.1/§8 rule protected |
|---|---|---|
| Spending HeyGen credits to prove F1's cloud leg | This session's own D2 ruling: zero spend. F1 resolves PARTIAL, its pre-written fail branch (`C-6`, hard cuts only) fires as designed, not as a workaround. | "No auto-retry past a cap; no loosening a rule to pass a gate" |
| Attempting HeyGen MCP OAuth non-interactively for F2–F4 | The system prompt is explicit this session cannot run an interactive OAuth flow. Named `BLOCKED-CONNECTOR`, not guessed or skipped silently. Reconfirmed at T4 and again at T5 — still true both times, not a stale finding carried forward unchecked. | Same |
| Editing the shipped `providers.yaml` with fabricated cost numbers | HeyGen speech/image/enhance costs are unmeasured this pass (connector-blocked). A fabricated number in a budget ledger is worse than a named gap. | — |
| Rewriting the WO's own §0–§7 text to fix found errors | House convention: corrections land as a dated §8 appendix, body text stays a faithful copy of what was drafted. | WO-FVC-004 §8 precedent |
| Touching `faceless-video-craft`'s uncommitted files in claude-skills | They belong to another session's in-flight 2.2.0 work. Verified `git diff --stat` identical before and after this session's own branch creations. | `CLAUDE.md` shared-checkout convention |
| Porting `staysInFrame` assertions into the motion sidecar | The compiler has no per-beat geometric reasoning to back the assertion; a placeholder that asserts something unverified is worse than omitting it. | — |
| Retuning the Haar cascade face detector to stop H-3's false positives on bold typography (T5) | Loosening a detection threshold to pass a gate is exactly the failure mode R-1/R-2/H-5's "no loosening a rule to pass a gate" exists to prevent — a genuinely looser detector would also miss real faces. Resolved instead via T7's own H-3 visual-confirmation fallback, with saved evidence frames, not by moving the goalpost. | "No loosening a rule to pass a gate" |
| Compensating T4's measured +3dB render-stage audio gain with a new hardcoded default in the mixer (T5) | Used the existing `mix_audio.py` CLI flag instead of baking a magic number into the script; the gain is real-hardware-dependent and flagged in the run report as needing re-verification on production render hardware, not treated as solved. | — |
| Backfilling `produced[]` against every `videos/<slug>/09-run-report.md` in the repo (T6) | Four directories from an older, unrelated pipeline share that filename by convention. Scoped the backfill to slugs that are ALSO a currently-published `seoulhabit-learn` route, rather than trusting filename presence alone, to avoid false-matching them into the queue's produced state. | — |
| Using PyYAML in `enqueue_from_site.py` (T6, first draft, corrected before landing) | The skill's own `requirements.txt` and every existing script (`providers.yaml` consumers) are stdlib-only via `_yaml_lite.py`; a new script pulling in a real dependency breaks that convention silently for anyone who doesn't `pip install` it. Rewritten against `_yaml_lite.parse_yaml_subset` plus a narrow hand-written writer instead. | House convention (`requirements.txt` header) |
| Touching the shared `~/Desktop/claude-skills` checkout to fix its stale 0.2.0 drift (see Deploy traps below) | It sits on a branch (`fvc-005/makemeavideo`) with another session's uncommitted work; forcing it onto `origin/master` risks discarding that work. Named as a live, unresolved deploy trap instead of silently "fixed" by force. | `CLAUDE.md` shared-checkout convention |

## 3. Deploy traps

- **`hyperframes` must be invoked bare, never via `npx`.** Unchanged from T0–T3. The tool's own `init` scaffold still writes `npx --yes hyperframes@<pin>` into a fresh project's `package.json`.
- **`videos/_channel/channel.yaml` does not exist — RESOLVED at T7.** The 0.2.0 skill read that nonexistent path in 43 places; the repo has `baseline.yaml`. T7's own rewrite pointed every reference at `baseline.yaml` instead of renaming the repo file, per the AskUserQuestion ruling this session ("Point the skill at baseline.yaml"). Confirmed clean post-rewrite: `grep -rn "channel\.yaml" makemeavideo/{SKILL.md,references/*.md,scripts/*.py}` now returns zero matches. `render_cloud.sh`'s file-resolution order (T7 fix) also checks `baseline.yaml` before `channel.yaml` as a defensive fallback, in case a future project still ships the old name.
- **Two Claude Design projects share the exact name "SeoulHabit Video Design System" — still unresolved, unchanged from T0–T3.** T2 extracted `a7945a95-…` on name-matching alone; if Kim's Gate 0 answer says otherwise, `videos/_system/` needs re-extraction, and `MANIFEST.json`'s sha256 tree (now with the R-6 `amendments[]` entry layered on top) is the only way to tell old from new once that happens.
- **NEW, live, unresolved: the shared `~/Desktop/claude-skills` checkout is stuck on stale content.** `~/.claude/skills/makemeavideo` is a symlink into that checkout. Confirmed this session, moments before writing this document:
  ```
  $ grep -n "version:" ~/Desktop/claude-skills/makemeavideo/SKILL.md
    version: "0.2.0"
  $ cd ~/Desktop/claude-skills && git show origin/master:makemeavideo/SKILL.md | grep -n "version:"
    version: "0.3.0"
  ```
  `origin/master` correctly carries all four merges (T4, T7, T5-fixes, T6:
  `e18f1e5` ← `146563e` T6 ← `e0d3b67` merge-T5-fixes ← `65c0a64` T5-fixes ←
  `5a9f5b0` merge-T7 ← `09877a2` T7 ← `e010f68` merge-T4 ← `40286c7` T4). The
  shared checkout's own working branch (`fvc-005/makemeavideo`) was never
  fast-forwarded and still carries another session's uncommitted files on
  top of the pre-T4 state. **Anyone invoking `/makemeavideo` via the Skill
  tool directly — not from a fresh worktree checked out against
  `origin/master` — gets the stale 0.2.0 rules**: HeyGen Video Agent build
  calls, the nonexistent `channel.yaml` path, none of R-1/R-2/R-6. T5 hit
  this exact trap and worked around it by building a fresh detached-HEAD
  worktree off `origin/master` instead of trusting the Skill tool's loaded
  content. **This needs a human decision** — reconcile or discard the other
  session's uncommitted work in the shared checkout, then fast-forward it —
  not a unilateral fix by this session (see Refusals, above).
- **The compiler and design system are now both merged to their respective `master`s** — this trap from T0–T3 ("two unmerged branches, needs both checked out") is resolved. The one live cross-repo trap is the drift above, not a missing merge.
- **The font freeze duplicates ~2.4 MB into every compiled project's `06-render/<canvas>/assets/fonts/`.** Unchanged, still just a thing to watch past a handful of projects — `centella-asiatica` is the first real one to carry it; not a problem yet at n=1.
- **Kokoro TTS still not installed** (`pip install kokoro-onnx soundfile`) — confirmed a second time at T5: no matching `onnxruntime` wheel for Python 3.9/x86_64 in this environment. T5 used `mix_audio.py --allow-placeholder-vo` per policy's rewritten PR-2/V-2 rather than forcing an install or spending HeyGen credits. Whoever runs this on a machine with a compatible wheel gets real VO fidelity; this one still gets the named substitute.
- **The render-stage audio gain (~+3dB, T4's own measurement) is real-hardware-dependent and unverified on a second machine.** T5 compensated it via `mix_audio.py`'s existing gain flag for this pilot's own render, but the number itself is not yet confirmed stable across hardware — flag anyone re-running this pipeline on different render hardware to re-measure before trusting the same offset.
- **Nine of `seoulhabit-learn`'s 21 published passports carry zero citations and zero findings** (WO §8.9). T6 did not filter these out of the queue — they're enqueued and sorted to the back, on purpose, so the evidence-rich routes get produced first and the zero-evidence ones surface `K-2b`'s halt when their turn comes, rather than being silently skipped.

## 4. Tier log

| Task | Tier | Notes |
|---|---|---|
| Landing the WO + Gate 0 sheet | Sonnet/medium | |
| T0 (environment) | Sonnet/medium | |
| T1 (spike) | Sonnet/medium | |
| T2 (design-system extraction + compiler design) | **Opus/High** | Per the WO's own flag — its one Opus/High task |
| T3 (compiler build) | Sonnet/medium | Flagged back down at T2's end, per the WO's own instruction |
| T4 (audio + render harness, R-6) | Sonnet/medium | |
| T7 (skill cut, out of order) | Sonnet/medium | Documentation/rewrite task, no new engine design |
| T5 (pilot run) | Sonnet/medium | Largest single task by wall-clock this WO has run, but mechanically a run of an already-designed pipeline, not new design |
| T6 (recurrence) | Sonnet/medium | |
| T8 (this handback) | Sonnet/medium | |

## 5. Version and hash

```
$ cd ~/Desktop/claude-skills && git show origin/master:makemeavideo/SKILL.md | grep -n 'version:' | head -1
  version: "0.3.0"
```
Bumped at T7, per `docs/wo/WO-FVC-005.md` §8.1's own correction target. **Note the standing trap above**: this is `origin/master`'s content, not what the shared `~/Desktop/claude-skills` checkout currently shows on disk (still `0.2.0`, uncommitted-work-blocked from fast-forwarding).

```
$ python3 -c "import json; m=json.load(open('videos/_system/MANIFEST.json')); print(m['file_count'], sum(f['bytes'] for f in m['files'].values()))"
67 2526063
```
`file_count` unchanged at 67 since T2 (no files added or removed — R-6 only
edited one file's contents); `total_bytes` moved from `2525499` to
`2526063` (+564 bytes) — entirely from `tokens/spacing.css` growing under
R-6's amendment. `MANIFEST.json` now carries an `amendments[]` array with
one entry recording R-6 (the ruling, the exact before/after values, and
why); re-derives clean against every file's own sha256, `check_manifest()`
confirmed passing on every T4/T5/T6/T7 compile that touched the design
system.

## 6. §5/§6 carried

**Unchanged from the WO's own §6 "Does NOT close":** the Sunny/Higgsfield
lane, Publish Desk automation, the Nocturne-vs-video palette question (still
open — Gate 0 G0-8), HeyGen Video Agent as an engine (now formally
superseded for S4b–S7 by R-1/R-2, but the WO's own §6 scope line is
unchanged), localisation, `faceless-video-craft` 2.1.0 archive.

**Resolved this pass, closed out of §6 rather than carried further:**
- **`videos/_channel/channel.yaml` vs. `baseline.yaml`** — resolved at T7 (see Deploy traps). No longer an open question.
- **The design-system safe-area tokens failing both canvases (T3 finding, carried at T0–T3 close)** — resolved by R-6 at T4. Both canvases verified clean post-fix.
- **`makemeavideo`'s modes colliding with `validate_request.py`'s front door** (T0–T3 carried finding: `build`/`package`/`readout` couldn't pass validation) — resolved incidentally by T7's rewrite; the front-door table in `SKILL.md` and `validate_request.py`'s accepted modes now agree (confirmed via the T7 status file's own verification, not re-checked fresh in this pass — worth a spot-check if the discrepancy resurfaces).

**Still open, carried forward:**
- Nine of `seoulhabit-learn`'s 21 published passports carry zero citations and zero findings. Now concretely queued (T6), sorted to the back — a pilot or queue-pop landing on one still fails `K-2b` on the website's own content, not a compiler defect. This will surface as a real halt once the queue works through the evidence-rich entries.
- WO-FVC-004 §7's unshipped **1.0.0** retarget (with `faceless-video-craft` archived) is still open; unrelated to this WO's own work.
- The D5 split path and all nine component emitters remain proven only against the T3 synthetic fixtures and the one T5 real pilot — a second and third real production run would be the next real stress test, not another synthetic one.
- **NEW: the shared `~/Desktop/claude-skills` checkout drift** (Deploy traps, above) — the most consequential open item from this pass. Left unresolved deliberately; needs a human call on the other session's uncommitted work before it can be fast-forwarded.
- **NEW: the render-stage +3dB audio gain** (T4 measurement, T5 compensation) — verified on one machine only. Needs re-measurement on whatever hardware eventually runs this in production before the compensation value is trusted past this pilot.
- **NEW: H-3's Haar-cascade false-positive class on bold typography** — confirmed again on `centella-asiatica`'s real frames (T5), now two independent confirmations (T3's synthetic fixtures, T5's real pilot). Resolved procedurally (T7's visual-confirmation fallback), not by fixing the detector. A future pass replacing the detector itself, if anyone wants tighter automation here, would need to preserve the same false-positive-on-bold-type behavior class to avoid missing real faces.
- **NEW: `policy.md`'s S-4/S4b text still carries a residual inconsistency** flagged during T7's own rewrite but not corrected in that pass (out of T7's stated scope at the time) — worth a follow-up correction pass to `policy.md`'s S-4 rule text specifically, not urgent enough to have blocked T7's merge.

---

## 7. Cost table

No paid API spend occurred in T4, T7, T6, or T8 — all four were local
engineering/documentation tasks (compiler, skill text, queue tooling,
handback) with zero credit-bearing calls. T5 (the pilot) is the only task
this WO has run that spent real, metered credits:

| Task | Provider | Spend | Notes |
|---|---|---|---|
| T1 (prior) | HeyGen | $0 | D2 ruling: zero spend, F1 resolves PARTIAL instead |
| T5 | vidIQ | 355 → 335 credits (**20 spent**) | `vidiq_keyword_research`, `vidiq_outliers`, `vidiq_generate_titles`, `vidiq_score_title`, `vidiq_score_thumbnail` — real calls, S2/S3 topic-gate and packaging stages |
| T5 | HeyGen | $0 | Connector unauthorized (BLOCKED-CONNECTOR, reconfirmed); VO shipped via `mix_audio.py --allow-placeholder-vo` instead, named plainly in the run report, not billed |
| T5 | Local render (compute only) | $0 (no cloud render credits spent) | R-1: local by default; `baseline.yaml`'s `cloud_render_credits_cap: 20` [default] was never touched — the pilot never needed the cloud fallback |
| T0–T4, T6–T8 | — | $0 | No API/credit calls in any of these tasks |

**Running total against `PR-3`'s cap:** 20 vidIQ credits spent this WO,
against whatever ceiling Kim's own G0-4 answer sets (still not confirmed —
see Rulings needed, below). No HeyGen spend has occurred at any point in
this WO, T0 through T8.

## 8. T1-FINDINGS.md — pass/fail, reprinted

Unchanged since T1; reprinted here per the WO's own §7 checklist so it's
visible without a second file open.

| # | Finding | Verdict |
|---|---|---|
| F1 | Local render parity | **PARTIAL** — local clean; cloud leg not run (D2). Consequence: rule `C-6`, hard cuts only, applied. |
| F2 | VO cost + fidelity | **BLOCKED-CONNECTOR** — local substitute (`hyperframes tts`/Kokoro) available once installed; does not answer the cost half. Reconfirmed blocked at T4 and T5. |
| F3 | Image generation reach | **BLOCKED-CONNECTOR** — likely moot regardless, given the design system's own no-imagery rule. |
| F4 | Enhance retrievability | **BLOCKED-CONNECTOR** — no local substitute exists. |

Acceptance, per the WO's own bar ("all four findings written with their
evidence; Finding 1 = PASS; spend ≤ G0-4"): **not met as literally stated**
— F1 is PARTIAL, not PASS, and F2–F4 are blocked, not found. This has not
changed at any point from T1 through T8: every later task that touched a
connector-dependent path (T4's Kokoro check, T5's VO pre-flight) reconfirmed
the same blockage rather than finding a way around it.

## 9. Rulings needed from Kim

Three lines each, as the WO's own convention asks.

**G0-1 — which Claude Design project.**
Two projects share the exact name "SeoulHabit Video Design System."
T2 extracted `a7945a95-…` on name/component/palette match alone.
If wrong, `videos/_system/` needs re-extraction; `MANIFEST.json`'s sha256 tree is the only way to tell old from new after that.

**G0-4 — the $/credit half, still open.**
T5 spent 20 real vidIQ credits against no confirmed cap.
`baseline.yaml`'s `cloud_render_credits_cap: 20` is this session's own default, never confirmed by Kim.
A second pilot or the queue's next several pops will spend more against the same unconfirmed ceiling.

**G0-8 — the Nocturne-vs-video palette question.**
Still entirely open since T0–T3; no task since has touched it.
`videos/_system`'s extracted palette has shipped in every render since T2 regardless.
If Nocturne's palette should govern instead, every compiled video to date (including the real `centella-asiatica` pilot) would need a re-render, not just a token edit.

**The shared `~/Desktop/claude-skills` checkout drift (new, this pass).**
`~/.claude/skills/makemeavideo` still resolves to stale 0.2.0 content, four merges behind `origin/master`.
The checkout's branch carries another session's uncommitted work this session declined to discard unilaterally.
Whoever owns that other session's work needs to either land or discard it so the checkout can fast-forward — until then, anyone invoking `/makemeavideo` directly (not via a fresh worktree) gets stale rules.

**HeyGen MCP connector authorization (carried since T1).**
F2–F4 have been BLOCKED-CONNECTOR at every checkpoint from T1 through T5, never once answerable non-interactively.
No workaround exists that doesn't either spend money without authorization or trust an unverified substitute permanently.
An interactive session running the OAuth flow once is the only way this WO's own F2–F4 findings ever move past PARTIAL/BLOCKED.

---

Awaiting: Kim's confirmation of G0-1, the $/credit half of G0-4, the palette
confirmation at G0-8, a decision on the shared-checkout drift, and the
HeyGen MCP connector authorization for F2–F4 — all named above and in
`docs/wo/GATE0-FVC-005.md`. None of T4 through T8's work depended on
guessing any of them: R-6 was itself a confirmed ruling (this session,
AskUserQuestion), and every other open question was either worked around
with a named, reported substitute or left genuinely open rather than
resolved by assumption.

**This closes T8 and, with it, everything this WO asked for through T7.**
The pipeline runs local-first end to end, has produced one real video, and
can recur on its own queue. What's left is not engineering — it's the five
rulings above, each of which only Kim can make.
