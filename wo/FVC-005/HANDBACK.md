# WO-FVC-005 — Handback (S-A ground truth + S-B compiler, T0–T3)

This session landed the DRAFT work order, answered or evidenced every Gate 0
slot it could without Kim's plan-page/palette confirmations, and completed
`T0` through `T3` — environment probe, the four-finding spike, the
design-system extraction, and a working compiler proven end-to-end against
a real local render. `T4` (audio + render harness) onward is the next
session boundary, per the WO's own §5 session plan.

Two things happened outside the numbered tasks that matter as much as any
of them: this session found and corrected **seven factual errors in the WO's
own text** before building anything on top of them (§8 of
`docs/wo/WO-FVC-005.md`), and the compiler build surfaced **five real engine
bugs** that a plan built from documentation alone would not have caught —
each found by actually running `hyperframes lint`/`check` against a
first-draft compile, diagnosed from the engine's own error message, and
fixed before moving to the next task.

Every command below was re-run fresh for this handback, just now.

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

## 2. Refusals on record

| What | Reason | §0.1/§8 rule protected |
|---|---|---|
| Spending HeyGen credits to prove F1's cloud leg | This session's own D2 ruling: zero spend. F1 resolves PARTIAL, its pre-written fail branch (`C-6`, hard cuts only) fires as designed, not as a workaround. | "No auto-retry past a cap; no loosening a rule to pass a gate" |
| Attempting HeyGen MCP OAuth non-interactively for F2–F4 | The system prompt is explicit this session cannot run an interactive OAuth flow. Named `BLOCKED-CONNECTOR`, not guessed or skipped silently. | Same |
| Editing the shipped `providers.yaml` with fabricated cost numbers | HeyGen speech/image/enhance costs are unmeasured this pass (connector-blocked). A fabricated number in a budget ledger is worse than a named gap. | — |
| Rewriting the WO's own §0–§7 text to fix the seven found errors | House convention: corrections land as a dated §8 appendix, body text stays a faithful copy of what was drafted. | WO-FVC-004 §8 precedent |
| Touching `faceless-video-craft`'s 5 uncommitted files in claude-skills | They belong to another session's in-flight 2.2.0 work. Verified `git diff --stat` identical before and after this session's own branch creation, twice (once per commit). | `CLAUDE.md` shared-checkout convention |
| Porting `staysInFrame` assertions into the motion sidecar | The current compiler has no per-beat geometric reasoning to back the assertion; a placeholder that asserts something unverified is worse than omitting it. | — |

## 3. Deploy traps

- **`hyperframes` must be invoked bare, never via `npx`.** The WO's own text uses `npx hyperframes` throughout; this repo's convention (and a prior 4.01 GB cache-clear incident) says otherwise. The tool's own `init` scaffold *still* writes `npx --yes hyperframes@<pin>` into a fresh project's `package.json` — confirmed this session — so this trap will keep resurfacing on every freshly-scaffolded project unless corrected by hand.
- **`videos/_channel/channel.yaml` does not exist.** The skill's 0.2.0 pipeline reads that path in 43 places; the repo has `baseline.yaml`. Confirmed by direct `find`, not assumed. Named as Gate 0 slot G0-10 rather than silently resolved — whichever way T7 resolves it (rename the file, or correct the skill's path) must happen on **every machine the skill runs on**, or one machine reads a channel value the other doesn't.
- **Two Claude Design projects share the exact name** "SeoulHabit Video Design System." T2 extracted `a7945a95-…` on the strength of matching every component/palette/template name the WO gives — if Kim's Gate 0 answer says otherwise, `videos/_system/` needs re-extraction from the correct project, and `MANIFEST.json`'s sha256 tree is the only way to tell old from new once that happens.
- **The compiler lives in `claude-skills` (branch `fvc-005/makemeavideo`, not yet merged to `master`), the extracted design system lives in `Story Board` (branch `session/fvc-005`, not yet merged).** Anyone continuing this WO on a second machine needs both branches checked out, or the compiler will `die()` immediately on `check_manifest()` finding no `videos/_system/`.
- **The font freeze duplicates real bytes (~2.4 MB) into every compiled project's `06-render/<canvas>/assets/fonts/`.** This is deliberate (root-relative, not base64, to avoid duplicating that payload across dozens of sub-composition *files* instead) but still means a video repo with many compiled projects accumulates that 2.4 MB once per project per canvas. Not yet a problem at 1 project; worth watching past a handful.
- **Kokoro TTS is not installed** (`pip install kokoro-onnx soundfile`) — needed the moment F2's local-substitute path is actually exercised, not before.

## 4. Tier log

| Task | Tier | Notes |
|---|---|---|
| Landing the WO + Gate 0 sheet | Sonnet/medium | |
| T0 (environment) | Sonnet/medium | |
| T1 (spike) | Sonnet/medium | |
| T2 (design-system extraction + compiler design) | **Opus/High** | Per the WO's own flag — this is its one Opus/High task |
| T3 (compiler build) | Sonnet/medium | Flagged back down at T2's end, per the WO's own instruction |

## 5. Version and hash

```
$ grep -n 'version' ~/Desktop/claude-skills/makemeavideo/SKILL.md | head -1
  version: "0.2.0"
```
Not bumped this session — `T7` (skill cut) is out of scope for S-A/S-B. `docs/wo/WO-FVC-005.md` §8.1 records the correction (target is 0.3.0, not the WO's stated 0.2.0) for `T7` to apply.

```
$ python3 -c "import hashlib,json; m=json.load(open('videos/_system/MANIFEST.json')); print(m['file_count'], m['total_bytes'])"
67 2523417
```
This is the design system's own version anchor (no version string exists in the source project — see `EXTRACTION.md`).

## 6. §5/§6 carried

**Unchanged from the WO's own §6 "Does NOT close":** the Sunny/Higgsfield lane, Publish Desk automation, the Nocturne-vs-video palette question (still open — Gate 0 G0-8), MFS gate 13 / evidence-completion on the website, HeyGen Video Agent as an engine, localisation, `faceless-video-craft` 2.1.0 archive.

**Updated:** MFS is no longer an unresolved name — `docs/wo/WO-FVC-005.md` §8.4 identifies it as `seoulhabit-learn`, the site repo this WO's R-3 already depends on.

**New, found during this pass — carried to §6 of the WO, not fixed here:**
- Nine of `seoulhabit-learn`'s 21 published passports carry zero citations and zero findings. A pilot or queue entry landing on one fails `K-2b` on the *website's* content — a finding to report, never a rule to loosen.
- WO-FVC-004 §7's unshipped **1.0.0** retarget (with `faceless-video-craft` archived) is still open; that skill is now at an unreleased **2.2.0 with five uncommitted files**, not "frozen at 2.1.0" as its own changelog claims.
- Three of `makemeavideo`'s five documented modes (`build`/`package`/`readout`) cannot pass `validate_request.py`'s front door, which accepts only `new`/`improve`. `T7`'s own instruction to re-run the pilot in `build` mode collides with this directly.
- The D5 split path and four of the nine component emitters (`ShCompare`/`ShMyth`/`ShQuote`/`ShSteps`) are implemented but not yet exercised against a real render.
- Neither of the two real beat sheets already in this repo can compile without a schema migration (they predate `component`/`slots`).

---

Awaiting: Kim's confirmation of G0-1 (which Claude Design project), the
$/credit half of G0-4, the palette confirmation at G0-8, the two new slots
G0-9/G0-10, and the HeyGen MCP connector authorization for F2–F4 — all
named in `docs/wo/GATE0-FVC-005.md`. None of this session's work depended
on guessing any of them, so `T4` can start once any subset clears; it does
not need all five at once.
