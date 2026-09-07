# Gate 0 — WO-FVC-006 answer sheet

Status: **PARTIALLY ANSWERED FROM THE RECORD.** Three of the WO's own six
Gate 0 slots were already ruled by Kim under WO-FVC-005, dated the same day
this WO was drafted (`docs/wo/GATE0-FVC-005.md`) — this sheet closes those
from citation rather than re-asking. Four items remain genuinely open: two
required (G0-2, G0-3), one promoted from a silent default (G0-4), and two
new ones this review surfaced (G0-7 scale, G0-8 pipeline). See
`docs/wo/WO-FVC-006-credibility-gap-remake.md` §7 for full corrections and
citations; `wo/FVC-006/ASSET-INVENTORY.md` for the evidence behind G0-2/G0-4.

---

## Closed from the record — no re-ruling needed

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

## Still open — required

▸ **G0-3 — Source file.** Confirmed present at
`~/Downloads/The_Credibility_Gap__When_Cosmetics_Borrow_Medical_Halos.mp4`
(53 MB), not yet copied into the repo. **Three additional facts to rule on
alongside the copy, found by `ffprobe`/`ffmpeg ebur128` this session:**
  - Source is **1280×720**, not 1080p — output spec is 1920×1080, so any
    reused source footage is a 1.5× upscale. Rule: acceptable, or source
    footage excluded from the final cut entirely?
  - Source is **already clipping** at +1.0 dBFS true peak (LUFS-I −16.6).
    T9's ≤ −1.0 dBTP target needs ~2 dB reduction plus clip repair, not
    normalization alone — noted so T9 isn't surprised by it.
  - Source audio is a **single mono stream** — no channel-based narration/
    music separation is possible, and no source-separation model is
    installed. If a music bed is embedded, T1 can report only "present,
    inseparable," not isolate it.
  - Duration confirmed correct: 410.83s / ~6:51.

▸ **G0-2 — Imagery lane.** **Genuinely open, and larger in scope than the
WO's own framing.** This is not only a founder-note decision — it is
enforced by a merged compiler (`videos/_system/COMPILER.md:195`: *"the
compiler refuses an `image_ref` field it does not recognise"*) and by
per-asset metadata (`catalog/manifest.json`: every record's
`approved_surfaces` array *"excludes HyperFrames compositions… no
generative imagery"*). The one filed precedent for an exception is
`catalog/ingredients/one-percent-line/README.md:113` (a single scrim-tinted
product photo, explicit in-session creator authorization) — cite that as
the bar for what "yes" looks like.

  **Presented alongside real evidence, not blind:** `wo/FVC-006/ASSET-INVENTORY.md`
  finds ~336 existing reusable images plus 21 built visual-mechanism
  components already covering the *mechanism* side of scene systems 2–4
  (a labelled skin cross-section, a claim-vs-evidence bisector, an
  N-way "shares a name, not the evidence" component that is close to this
  video's actual thesis). Net-new generation looks most needed for scene
  system 1 and ingredient-specific beats, not for 85–95% of the visual load
  as the WO originally estimated. Rule on:
  1. Photographic plates inside HyperFrames compositions — yes / no / reuse-only
     (existing catalog + video plates, no new generation)?
  2. If yes in any form — does the design system's `readme.md`, the
     compiler's `image_ref` handling, and every affected
     `approved_surfaces` record in `catalog/manifest.json` get amended for
     this video only, or as a standing lane change? (§5 of the WO already
     scopes this video-only unless ruled broader — confirm that scoping
     survives contact with the actual mechanism, which is repo-wide
     metadata, not a per-video flag.)

▸ **G0-4 — Image provider.** **Promoted from `[default]` (proceeds
unattended) to REQUIRED.** Higgsfield is retired out of lane by two standing
WOs: `docs/wo/WO-FVC-005.md:52` — *"Not in the lane: … Higgsfield for
anything faceless"* — and `docs/wo/WO-FVC-004.md:32/123`, which retires
"Higgsfield as image role" and marks the `providers.yaml` Higgsfield rows
`retired: 2026-09-05`. Re-entering a retired provider must not happen on a
default nobody actively confirms. Note for context, not as an argument
either way: the existing `catalog/skin-macro-photography/` stills already
used Higgsfield `nano_banana_pro` under a prior, separately-authorized run
— so the model itself has in-repo precedent even though the provider is
currently out of the pipeline's lane.

---

## New gates surfaced by this review

▸ **G0-7 — Scale.** The compiled pipeline has exactly one real end-to-end
pilot: `centella-asiatica`, 45.5s, 9x16 only, 12 shipped components, zero
imagery. This WO proposes 410.8s (9×), 16:9 (previously only a synthetic
test fixture), 30–40 photographic plates, and one net-new component,
simultaneously. **Recommendation: prove one T6 chapter (~70–100s, matching
`T6.json`'s `chapters_min: 4` at ~411s/4) at 16:9 end-to-end before
committing to all 4–6 chapters** — folded into the existing GATE C pilot in
place of the WO's 30–45s opening pilot, not as an added gate. This surfaces
any 16:9-specific or long-form-specific defect while only one chapter's
work is at stake, not all six.

▸ **G0-8 — Pipeline choice.** WO-006's header selects the HyperFrames
`general-video` companion flow (hand-authored `STORYBOARD.md`, hand-built
composition modules). WO-FVC-005 merged a different pipeline: a beat-sheet
compiler reading `03-beat-sheet.json` against `videos/_system/`, emitting
hash-checked sub-compositions with a `compile-report.md` ledger. They are
incompatible on five specific points (component naming, duration ceilings,
font inlining, the imagery refusal, and the missing `_ds_manifest.json` —
full detail in the WO's own §7.4). **This gate is largely downstream of
G0-2**: if imagery stays out of lane, the compiled pipeline is very likely
the right choice and gets this WO's compiler-conflict corrections for free;
if imagery is allowed in, the compiler needs new capability first (an
`image_ref` handler) and the hand-authored `general-video` flow becomes the
only path available today. Rule on: compile through the WO-005 pipeline, or
hand-author via `general-video`?

---

## Kickoff line for Code (corrected)

> Read `docs/wo/WO-FVC-006-credibility-gap-remake.md` §0–§6 for the original
> plan and §7 for corrections, then this file (`wo/FVC-006/GATE0-FVC-006.md`)
> for the current Gate 0 state. Rule on G0-2, G0-3, G0-4, G0-7, and G0-8
> before T1 starts; G0-1, G0-5, and G0-6 are closed and need no further
> input unless you want to change them.
