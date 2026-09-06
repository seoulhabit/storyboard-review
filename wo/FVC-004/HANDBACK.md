# WO-FVC-004 — Handback (Gate 0 prep pass)

T1 (repo-side half), T3, T4 complete and committed to `claude-skills` branch
`fvc-004/makemeavideo` (3 commits, `33277a6`..`e153bb1`). T0, T1's HeyGen
half, T2, T5–T9 not started — all gated on the HeyGen MCP connection this
session does not have and on Kim's `approved` plus three required Gate 0
answers. Full task detail in `wo/FVC-004/t1-status.md`, `t3-status.md`,
`t4-status.md`; this file is the WO's own required handback summary (per
WO-FVC-001 §6's format, which WO-FVC-004 does not itself restate but
inherits as house convention), not a replacement for those.

Two things happened outside the numbered tasks that matter as much as any of
them: **the WO's own text did not match the machine in five places**
(§8 of `docs/wo/WO-FVC-004.md` has the full account — no WO-FVC-002/003 exist
anywhere, the scaffold ships as a library skill not a zip, the reconciliation
§0.3 calls open closed since 2026-09-04, `faceless-video-craft` isn't
actually frozen, `makemeavideo` wasn't actually repo-canonical), and **three
real code bugs plus one real policy-text error were found only by running
the new scripts against real project data**, not by reading them (full
account in `t4-status.md`).

---

## 1. Attestation table

Every command below was re-run fresh for this handback, just now.

| Task | Accept check | Command | Output excerpt |
|---|---|---|---|
| T1 | `makemeavideo` resolves from the repo, not the library | `readlink ~/.claude/skills/makemeavideo` | `/Users/sumitchoudhary/Desktop/claude-skills/makemeavideo` |
| T1 | `faceless-video-craft` untouched by this session | `git diff --stat -- faceless-video-craft/` | `5 files changed, 107 insertions(+), 6 deletions(-)` — identical to the diff present before this session's first commit |
| T1 | HeyGen MCP connection | — | **Blocked.** No `heygen` entry in `~/.claude.json`, not in the connector registry, no `heygen`-prefixed tool in this session. Needs an interactive session for OAuth. |
| T3 | No retired-engine cross-references remain in `references/` | `grep -n -iE 'hyperframes\|seek\(\|gsap\|#root\|motion\.json\|box-sizing\|higgsfield\|current-vo\|gemini-tts' references/policy.md references/youtube-delivery.md` | 4 hits, all this session's own retirement-history prose (quoted in full in `t3-status.md`), none live |
| T3 | Every §H rule has reads/rule/default/ledger | scripted check, all 10 rules (`H-0`..`H-7`, `F-2`, `I-1`) | `reads=True rule=True default=True ledger=True` × 10 |
| T4 | Test suite green with dependencies | `bash tests/run.sh` (system python3, no cv2) | `15 passed, 0 failed` (honest `SKIP` on the `qa_render.py` suite, named why) |
| T4 | Test suite green, full dependency set | `PATH=<repo>/.venv/bin:$PATH bash tests/run.sh` | `20 passed, 0 failed` — includes 5 real `qa_render.py` assertions against `ffmpeg`-generated fixtures |
| T4 | `qa_render.py` against a real render, not just fixtures | manual run against `videos/kbeauty-label-trap/06-render/final.mp4` (1920×1080, 257s) | all 9 gates produced real measurements; full envelope in `t4-status.md` |
| T4 | `beats_to_build_spec.py` against real project data | manual run against `outputs/2026-09-01-how-to-repair-skin-barrier/03-beat-sheet.json` + `01-story-brief.md` | 8-scene build spec, all 8 non-`CUT` `[K-1]` claims matched to their scenes |

## 2. Refusals on record

| What | Reason | §1/§2 rule protected |
|---|---|---|
| Running T0 | HeyGen MCP not connected on this machine; cannot complete OAuth non-interactively | §0.2 — T0 must run before any rewrite proceeds past Gate 0 |
| Editing `faceless-video-craft`'s in-flight 2.2.0 diff | Belongs to another session; WO §7 requires it frozen and read-only | §7 (though the freeze itself does not currently hold — see `docs/wo/WO-FVC-004.md` §8.7) |
| Silently loosening `validate_beat_sheet.py`'s section-order rule | The real centella artifact fails it; loosening a carried rule to make a test fixture pass is a policy decision, not a T4 one | house convention (K-2b precedent: "unblocking is a separate fetch-and-read pass, not this task") |
| Removing `makemeavideo`/`faceless-video-craft` from the claude.ai library | Needs the account holder's library settings; not reachable from a coding session | — |
| Answering G0-1, G0-3, G0-6 | Only Kim has the story, the HeyGen plan/credit price, and the brand-token decision | §1 ruling 1 — no creative-preference or missing-input guessing |

## 3. Deploy traps

- **Two-machine parity is entirely unverified.** This session ran on one
  machine. `opencv-python-headless` must be pinned to exactly `4.10.0.84` on
  whichever machine runs `qa_render.py` — the latest release (5.0.0.93 as of
  this session) does not ship the Haar cascade files at all, which would
  make `H-3`, the one non-skippable gate, silently unmeasurable. See
  `requirements.txt`.
- **The claude.ai library still has both skills enabled.** Until
  `TOUCHPOINT-LIBRARY-REMOVAL` (see `t1-status.md`) happens, a session with
  library access will see two `makemeavideo` copies at different
  versions/paths — the exact drift this WO exists to end.
- **The centella artifact used for T0 is ambiguous in the WO's own text**
  (§8.2): "the centella run" could mean `outputs/2026-09-01-how-to-repair-skin-barrier/`
  (45.28s, 8 scenes — the one with a real `03-beat-sheet.json` and
  `01-story-brief.md` §Sourcing) or `videos/centella-tiger-grass/`
  (= `d6DPiORuPO4`, ~72s, no beat sheet in this shape). T0 must record which
  one it actually spiked, in `spike.md`.
- **`validate_beat_sheet.py`'s section-order rule rejects the real T0
  artifact.** Whoever runs T0 will hit `FAIL: sections must be exactly
  [...]` if they run the validator against
  `outputs/2026-09-01-how-to-repair-skin-barrier/03-beat-sheet.json`. This
  is a real, reported, unfixed finding (`t4-status.md`) — decide whether the
  rule needs a short-form exception before assuming the artifact is broken.
- **`H-4.contrast` and `H-4.type-floor` are advisory, not blocking**, in
  `qa_render.py`'s current aggregation — a deliberate, documented scope
  reduction pending validation against a real HeyGen render corpus. Revisit
  once T0 produces real output.
- **HeyGen sign-in has failed before, in this exact repo's history.**
  `wo/FVC-001/gate-0-notes.md:20` records HeyGen/`hyperframes tts` sign-in as
  "unavailable from an automation context" during WO-FVC-001's own Gate 0 —
  which is why the channel's current voice is Higgsfield, not HeyGen. This
  WO bets the *remote MCP's* OAuth succeeds where that *local* sign-in
  failed. Untested either way; T0 should check this before spending credits
  on anything else (`docs/wo/WO-FVC-004.md` §8.5).

## 4. Tier log

| Task | Tier | Notes |
|---|---|---|
| T1 (repo landing) | Sonnet/Med | file copy, symlink, verification — no policy authoring |
| T3 (policy surgery) | Opus/High | per WO §3 T3's own tier assignment |
| T4 (scripts) | Sonnet/Med for CLI plumbing, Opus/High for the qa_render.py gate design and the C-2/H-4 threshold-conflation correction | matches WO §3 T4/T3's mixed tier note |

## 5. Version and hash

```
$ grep version claude-skills/makemeavideo/SKILL.md
  version: "0.2.0"
$ sha256sum claude-skills/makemeavideo/SKILL.md
d824635ba3d6a308f33b49e677701bc2f60c4a6700669175d845475da3cac609
```

## 6. §5 carried

**Unchanged from the WO's own §5 "Does NOT close":** video translation
derivatives, batches/scale, Publish Desk API path, TikTok and 1:1,
HyperFrames-inside-Video-Agent.

**Updated:** the `storyboard-review` reconciliation entry — WO §5 carries it
forward as open; it closed 2026-09-04, before this WO was drafted (§8.3).
`seoulhabit-video-3d` trim — confirmed still open, and confirmed why: no
`videos/seoulhabit-video-3d/` directory exists on disk, only references to
it from other projects' briefs.

**New, found during this pass:**
- Captions are required by `youtube-delivery.md` but no stage produces or
  gates them; `catalog/tooling/check-captions.py` sits unwired. (WO §5,
  added this session.)
- `assets/beat-sheet.schema.json` still describes GSAP-generated
  transitions, actor ids and a composition generator in several field
  descriptions — out of T3's stated scope (policy.md +
  youtube-delivery.md only), flagged for whoever next touches the schema.
- `H-4.contrast`/`H-4.type-floor`'s advisory status (see Deploy traps above)
  needs revisiting once a real HeyGen render corpus exists.
- `validate_beat_sheet.py`'s section-order rule vs. the real T0 artifact
  (see Deploy traps above) — a policy question, not a bug to silently fix.

---

Awaiting: the HeyGen MCP connection (interactive session required), Kim's
`approved` on `docs/wo/WO-FVC-004.md`, and G0-1/G0-3/G0-6 on
`docs/wo/GATE0-FVC-004.md` — all three before T0 can run.
