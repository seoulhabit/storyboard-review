# Gate 0 — WO-FVC-006 answer sheet

Status: **ANSWERED (Kim, 2026-09-07).** All eight slots are closed — three
from the WO-FVC-005 record (G0-1, G0-5, G0-6), five ruled directly by Kim
this session (G0-2, G0-3, G0-4, G0-7, G0-8). **Two of these five rulings
(G0-2, G0-4) deliberately reverse standing decisions in WO-FVC-004 and
WO-FVC-005** — flagged explicitly below per this repo's own convention that
a supersession is recorded, not silently overwritten. T1 may now start;
G0-8's compiler extension is scoped as its own sub-task, **T4.5**, in
`wo/FVC-006/T4.5-compiler-image-ref-scope.md` — see § Sequencing at the end
of this file for what runs when.

---

## Closed from the WO-FVC-005 record — no re-ruling needed

▸ **G0-1 — Palette.** **CLOSED.** `docs/wo/GATE0-FVC-005.md:13` — G0-8
**CONFIRMED (Kim, 2026-09-07)**: ship cream `#F4EDE3` / ink `#26215C` / clay
`#9C3A32` / brass `#C0A265` — the same palette already live in the
`centella-asiatica` pilot render. No Nocturne sheet exists anywhere in this
repo (confirmed again this session — see §7.2 of the WO). If a genuinely new
tint (a blush highlight, an Ink dark variant) is still wanted for this
video specifically, that is a scoped amendment to
`videos/_system/MANIFEST.json`'s `amendments[]` array (the R-6 precedent),
not a fresh palette ruling.

▸ **G0-5 — Fonts.** **CLOSED.** Already shipped, not a default being chosen:
`videos/_system/tokens/typography.css` — `--font-subject: "DejaVu Serif"`
(names, titles, end card), `--font-work: "Archivo"` (labels, captions,
functional text). `serif-split` is correct; "heavy sans 800" should read
Archivo.

▸ **G0-6 — Claude Design source.** **CLOSED.** Confirmed correct project
(`a7945a95-da21-4823-8b16-57c6ffa11558`) *and already extracted*:
2026-09-06, WO-FVC-005 T2, 67 files, sha256-verified in
`videos/_system/MANIFEST.json`, zero mismatches on re-check this session.
T3 becomes *verify the existing extraction*, not re-extract.

---

## Ruled directly by Kim, this session (2026-09-07)

▸ **G0-2 — Imagery lane.** **RULED (Kim, 2026-09-07): full imagery,
generate as needed.** Photographic plates are permitted inside HyperFrames
compositions for this video, generated on demand rather than limited to
reuse.

**This is a deliberate reversal, not an oversight — recorded as such:**

- Reverses `videos/_system/COMPILER.md:195`'s stated design-system rule
  (*"the design system forbids imagery by rule… the compiler refuses an
  `image_ref` field it does not recognise"*) — see G0-8 below for how this
  gets built rather than worked around.
- Reverses the `approved_surfaces` exclusion on every record in
  `catalog/manifest.json` (*"approved_surfaces excludes HyperFrames
  compositions: that lane is browser-drawn only… no generative imagery"*)
  — those records need updating for any asset this video actually uses, not
  globally, unless Kim later rules this broader than one video.
- **Scope: this video only**, per the WO's own §5 ("does not close… as a
  *standing* rule (G0-2 covers this video only unless Kim rules broader)").
  The design-system `readme.md` rule and the compiler's default behavior
  for every *other* project remain "no imagery" unless a separate ruling
  says otherwise.

**Asset-inventory context, not a constraint on this ruling:**
`wo/FVC-006/ASSET-INVENTORY.md` found ~336 existing reusable images and 21
visual-mechanism components already covering much of scene systems 2–4's
*mechanism* need. That does not change this ruling — full generation is
approved — but T7's actual plate count should still check the inventory
first per the WO's own §1 rule 7 ("Check before generating") before spending
a credit on something that already exists.

▸ **G0-4 — Image provider.** **RULED (Kim, 2026-09-07): re-authorize
Higgsfield `nano_banana_pro`.**

**This directly reverses two standing rulings, recorded here rather than
silently:**

- `docs/wo/WO-FVC-005.md:52` — *"Not in the lane: … Higgsfield for anything
  faceless."*
- `docs/wo/WO-FVC-004.md:32` — retires "Higgsfield as image role" from the
  pipeline; `:123` marks the `providers.yaml` Higgsfield rows `retired:
  2026-09-05 (WO-FVC-004)`.

  **Correction (2026-09-07, found scoping T4.5):** the above assumed a
  dormant Higgsfield row could be un-retired. Checked directly —
  `makemeavideo/references/providers.yaml` has **no Higgsfield row left to
  amend**; WO-FVC-004 removed it outright, leaving only a header comment
  (`line 7`: *"Higgsfield … closed by supersession, WO-FVC-004"*).
  Re-authorizing means **adding a new row** under the existing `roles:
  image:` block (which already has the schema to copy — `heygen-image`,
  currently `tool: null`, "moot… no-op for the current design system"),
  not restoring a flag on an old one. Scoped as part of T4.5 — see
  `wo/FVC-006/T4.5-compiler-image-ref-scope.md` §2.6.

  Spend cap carries forward from the WO's own G0-4 default: 16:9, count 3
  per plate, hard cap 40 plates / 120 generations, stop and report at cap
  — unchanged, since only the provider was in question, not the budget.

▸ **G0-8 — Pipeline choice.** **RULED (Kim, 2026-09-07): extend the
WO-005 compiler with `image_ref` support, rather than choosing between the
compiled pipeline and hand-authoring, or working around the gap.**

This is the correct pairing with G0-2: it means this video gets the
compiler's hash-checking, duration-ceiling enforcement, and
`compile-report.md` ledger *and* its photographic plates, instead of
trading one for the other. It also means the capability is built once, in
`videos/_system/` and the compiler script (not in this WO's own video
directory), so the next video that wants imagery inherits it rather than
re-deriving the same workaround.

**Scoped as its own sub-task, T4.5, inserted before T5** —
`wo/FVC-006/T4.5-compiler-image-ref-scope.md`. Full detail there, including
exact file:line grounding in the real `compile_composition.py` (the
`#root` background line it attaches to, the `copy_assets()` audio-staging
pattern it mirrors, why `ShScene` — not four separate components — is the
right level for the new slot, and the corrected G0-4 provider-row finding
above). Summary:
1. `videos/_system/COMPILER.md` §4's "Images: none" rule gets a real
   `image_ref` spec — asset path resolution (root-relative, mirroring the
   existing audio-staging convention), which components accept it (likely
   only scene systems 1–2, not 3–4), and safe-area interaction with
   `check-safe-area.py`.
2. `catalog/manifest.json` (and any `catalog-v2` equivalent) records this
   video actually references get their `approved_surfaces` array amended —
   but that's T7's job, per-asset, when plates are actually chosen, not
   part of T4.5 itself.
3. `providers.yaml` gets a new Higgsfield row (see the G0-4 correction
   above), not an amended one.
4. This is compiler and design-system work — it belongs in
   `videos/_system/` and the compiler script in the separate `claude-skills`
   repo (per `COMPILER.md`'s own provenance discipline), reviewed and
   merged on its own before T5, not folded silently into this video's own
   composition files.

**Sequencing implication:** T0–T4 (environment, transcript, claims, brief,
beat map) do not depend on this and can proceed now. T4.5 must land before
T5 (style frames) — see § Sequencing below.

▸ **G0-3 — Source footage.** **RULED (Kim, 2026-09-07): exclude source
footage entirely.** The source MP4 is used only for its narration audio
(extracted, cleaned, and repaired per T9's existing scope). No frames from
the 720p source are reused as footage or b-roll anywhere in the composition.

This sidesteps both source-file problems found this session without
needing a separate ruling on each:
- The 1280×720-vs-1920×1080 upscale question is moot — no source frames
  ship.
- The true-peak clipping (+1.0 dBFS) and mono-stream/no-separation findings
  still apply to the narration audio itself and remain T1/T9's concern —
  **this ruling does not close those**, it only settles that no *visual*
  footage comes from the source.

File-copy mechanics remain as originally scoped: copy to `assets/source/`
before T1, per G0-3's original text.

▸ **G0-7 — Scale.** **Already ruled this session** (via the plan-approval
questions, before this Gate 0 sheet existed): **prove one T6 chapter
(~70–100s) at 16:9 end-to-end before committing to all 4–6 chapters.**
Recorded here for completeness — no new decision needed. Folds into the
existing GATE C pilot in place of the WO's original 30–45s opening pilot.

---

## Sequencing — what's unblocked now vs. still gated

**Unblocked, can start immediately, no dependency on T4.5:** T0
(environment + asset inventory — already run once this session, re-runnable
per-task), T1 (audio extraction + transcript — G0-3 confirms audio-only use
of the source), T2 (claim register), T3 (brief + design-spec — verification
only, already extracted), T4 (beat map skeleton).

**T4.5 — Compiler `image_ref` extension.** Fully scoped in
`wo/FVC-006/T4.5-compiler-image-ref-scope.md`: exact code sites in
`compile_composition.py` (the audio-staging pattern it mirrors, the `#root`
background line it attaches to), the `ShScene`-level design recommendation,
the corrected `providers.yaml` finding (a new row, not an amended one), and
acceptance criteria mirroring T3's own bar. Runs across two repos —
`storyboard-review` (`COMPILER.md`) and `claude-skills`
(`compile_composition.py`, `providers.yaml`).

**Blocked on T4.5 landing:** T5 (style frames) is the first task that
actually needs `image_ref` to exist. T6/T7 inherit the same dependency.
**Ownership RULED (Kim, 2026-09-07):** T4.5 stays a WO-FVC-006 sub-task,
not a separate WO — direct precedent in WO-FVC-005 itself (compiler
infrastructure built in `claude-skills` and the first video pilot run,
both under one WO number). Full reasoning in T4.5 §6. Doesn't block T0–T4
from starting now either way.

---

## Kickoff line for Code (corrected, Gate 0 fully closed)

> Read `docs/wo/WO-FVC-006-credibility-gap-remake.md` §0–§6 for the original
> plan, §7 for corrections, then this file (`wo/FVC-006/GATE0-FVC-006.md`)
> for the Gate 0 rulings — all eight slots are closed as of 2026-09-07. T0–T4
> can start now. T5 needs `wo/FVC-006/T4.5-compiler-image-ref-scope.md`
> executed first — it runs as this WO's own T4.5, in a `claude-skills`
> branch/PR cross-referenced from this one, not a separate WO.
