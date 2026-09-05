# QA log — hyaluronic-acid-vs-filler (v4, retention-review implementation)

Implements the retention/HyperFrames review's copy-ready brief against the
v3 composition (commit `f319ed7`, 120.359s). Proof: `06-render/proof-v4/`.
Does not touch `06-render/final.mp4` (v3, shipped) or `06-render/check.json`
/ `qa-log.md` (both describe the 160s v2 cut per an earlier disclosed note —
still not this version; see below).

## Gates

| Gate | Result | Measured on |
|---|---|---|
| `hyperframes@0.8.28 check --strict --samples 60 --at-transitions --frame-check` | **0 errors, 0 warnings** across lint / runtime / layout / motion (0/1187 samples) / contrast (12/12 AA) | the composition under seek |
| `check-safe-area.py --landscape` | **PASS — no findings, 481 frames sampled** | `06-render/proof-v4/draft.mp4` |
| `check-static-hold.py --landscape` | advisory (exit 0); whole-frame pass **clean** (241 samples, 10.0s ceiling); region-aware pass logs coarse-grid void windows in scenes with a dominant-actor macro layout — spot-checked at 63s/80s/117s, all show genuine legible content elsewhere in frame (see below) | same |
| `check-cadence.py --longform` | **PASS**; **20.9%** whole-video active share (up from v3's own 16.5–19.1%, consistent with the review's motion additions); longest quiet run 5.62s (s08-seals), under the 6.0s ceiling everywhere | same |
| `continuity-audit.py --gate` | **pass** — no plain crossfade across a ground change | source |
| `ffprobe` duration | **120.358s / 120.367s** (audio/video), matches the VO master clock | `draft.mp4` |

**Audio is raw narration muxed in for this proof only** (`vo.mp3` over the
silent render, AAC 48kHz mono, no mastering pass) — measured −26.0 LUFS
integrated, which is the unprocessed voice level, not a mix target. This
session made no audio changes; the project's own two-pass loudnorm mastering
step (voice bus + limiter, documented in `00-decision-ledger.md`) is
unchanged and still needs to run before a publish-ready mux, exactly as it
did before this session.

### `check-static-hold.py`'s region-aware advisory, verified not a real gap

The three longest flagged windows (59.25–68.00s / 8.75s, 77.50–84.00s / 6.50s,
115.50–120.00s / 4.50s) all fall in the CENTER-RIGHT third of its 2×3 grid,
inside scenes using the new macro grammar (actor dominant, positioned right
of center) or the full-bleed endcard. Extracted frames at 63s, 80s, and 117s
inside these exact windows all show genuine, legible, on-design content —
the "void" cell is negative space by design (the actor sits further right;
the endcard lockup sits left-of-center), not a broken or blank moment. The
tool's own note anticipates this ("a smooth gradient/watermark can cross the
active threshold... confirm by extracting the actual frame") and the
whole-frame pass — the less coarse, less position-dependent check — is
clean throughout.

## What changed, and why (see git log on `session/ha-filler-retention` for
the full reasoning on each — summarized here)

**Technical fixes (commit `4b90fd9`)**
- Camera relayering: every scene's `.stage` became a padded, clipping,
  non-moving camera housing; `.cam`/`.cam-in` carry all movement on separate
  transform channels. Fixes the `overlapping_gsap_tweens` lint warning on
  `#s13-badges-stage` and all 13 `container_overflow` layout warnings, at
  their cause rather than with `overwrite: "auto"`.
- s05-size's small-chain group travel reserved inside its own viewBox (was
  clipped ~10px below frame during its own "smaller ones travel farther"
  beat — the one moment the scene exists to make).
- Syringe lane icon's rotated plunger flange moved back inside its viewBox
  (was 2.7px outside for 171 sampled frames).
- `fix_generated_grounds()` made idempotent (it was not: a second run
  duplicated its CSS block on the 4 generated scenes — a live hazard since
  the external generator it post-processes is not vendored in this repo).

**Hook + transitions (commit `8bc150a`)**
- `SERUM ≠ FILLER` now opens the film as a collision/rejection (rush to
  center, sign lands, rejection pushes apart), fully readable at **0.70s**
  (review asked for ≤1.2s) — was landing at ~5.1s in v3.
- Replaced all 13 identical clip-path wipes with a semantic plan: 2 hard
  cuts (misconception break, safety interrupt), 1 camera-dive hero
  (s04→s05), 1 hand-authored liquid-lens hero (s07→s08, binding→sealing —
  no registry type does this; recorded as a catalog miss), rest short wipes
  ≤0.6s.
- s08's panel no longer re-enters on its own scene start — it's the
  molecule s07 ended on, exposed already in place by the liquid-lens reveal
  rather than sliding in from empty.

**Scene grammar + micro-motion (commit `6adc568`)**
- Full-frame skin cross-sections (s05/s06) instead of a 560px card beside
  the copy; a hand-authored `skin_layers()` ground (EPIDERMIS/DERMIS),
  composed once under the chains.
- s09-crosslink rebuilt as a real depth-scatter-assemble: shallow 3D field
  (`transformPerspective`, `rotationY/X`, soft blur), all 42 lattice nodes
  scatter from index-derived positions to their grid slot (~1.05s), cross-
  links draw only once every node has landed, then the actor racks flat and
  sharp on the citation beat.
- Word-level emphasis (`loose`/`locked`/`binds`/`seals`/`cross-linked`/
  `volume`/`surface`/`temporarily`): a bounded color+glow bloom, tweened up
  and back to baseline — no ongoing wobble.
- Three hand-authored clinical pictograms (tissue/vessel, eye, neurological
  signal) drawing in one at a time under the risk line — checked
  `catalog/visual-components/` first; no clinical icon set exists there.
- Endcard lockup splits into two spans with two different entrances (push +
  back.out) plus one bounded `ambient-glow-bloom`, instead of one shared
  fade.
- The warning slam ("DO NOT INJECT YOURSELF") moved 0.04s earlier in the
  beat sheet so it is *landing*, not just starting, at its own spoken onset.

**Two authoring bugs, caught by the checker, not by eye:**
- `_emphasize()`'s first version did a substring replace across each row's
  *whole* markup string, including its own `id="{sid}-b{i}"` — any emphasis
  word that was a substring of its own scene slug (`binds`, `seals`)
  spliced a `<span>` into the id itself, breaking every row in that scene.
  Fixed by restricting the search to the element's text node with a real
  word-boundary match.
- s09's first node-scatter draft (±110/±108px) blew past the actor's own
  480×560 viewBox by up to 122px on a sampled frame; shrunk to fit the
  lattice's own 40px pad.

**Two real, previously-undiscovered engine-interaction bugs, found only
because a render was actually taken and its frames extracted (commits
`42c5724`, `7240cf7`):**
- Every hand-authored scene (10 of 14 — everything `scene_shell()` writes)
  went fully blank for ~0.3–0.6s at each of its own transitions. Root cause
  traced into `hyperframe-runtime.js`: the runtime hides an element once any
  `[data-start]` ancestor's own declared window is exceeded, and
  `scene_shell()` never extended a hand-authored scene's *internal*
  duration to cover its transition overlaps the way the external
  generator's `render_scene()` already does for the 4 generated scenes.
  Confirmed present in the **unmodified v3 baseline** before writing a fix
  (s05→s06 at 42.7–42.9s) — this matches a limitation the v3 run report
  itself disclosed and deferred ("9 brief ~1–1.25s near-empty windows...
  flagged as a rough edge for a possible follow-up pass, not fixed in this
  round"). `fix_transition_hold()` now copies each hand-authored scene's
  outer-wrapper duration (already correctly resolved by the generator)
  onto its own internal duration and anchor tween.
- Fixing that exposed a second, real bug: s05 and s06 share the identical
  reused actor at the identical screen position by design. Once s05 stopped
  going blank mid-wipe, its EPIDERMIS/DERMIS labels and headline sat
  pixel-for-pixel under s06's own — 7 real `content_overlap`/`text_occluded`
  findings. Fixed by adding s05→s06 to the same real-opacity-fade treatment
  s03→s04 and s12→s13 already needed for an unrelated reason.
- Fixing *that* exposed a third: with s04 now correctly visible through its
  own exit, the s04→s05 zoom-through hero's registry-default 2.5× outgoing
  scale — always latent, warned about by the generator's own validator, but
  never visible before because s04 used to disappear before reaching this
  point — pushed content up to 1384px into the reserved zones on a real
  render. Reduced to 1.15×; the review's own acceptance line ("no scene
  needs more than one hero motion") does not ask for a bigger push than
  that to read as a dive.

## Explicitly deferred

**Sound design (review §4)** is not implemented. The v3 proof carries a
mono narration stream and no in-project music/SFX tracks, confirmed
unchanged. Building a music bed, 5–7 SFX cues, and a ducked mix under the
warning beat is a separate media-sourcing task (the `media-use` skill's
territory), not a composition-authoring change, and was out of scope for
this pass. Flagging rather than silently skipping it, per the review's own
framing.

**"One continuous molecular journey" (review's item #2)** is implemented as
continuity of *camera and transition language* across scenes 4–9 (the dive,
the reused actors, the liquid-lens hand-off), not as a literal multi-scene
merge — the brief's own implementation note says to preserve every scene ID
unless an edit is explicitly approved, which a merge would violate.

## Acceptance criteria, checked against this render

- `SERUM ≠ FILLER` fully readable by 1.2s — **0.70s**. ✅
- Three identities readable by 10.2s — **10.095s** (unchanged from v3, not
  touched this pass; still ahead of the ask). ✅
- No more than two hero transitions — **exactly 2** (camera-dive, liquid-lens). ✅
- At least four distinct frame grammars — **≥6**: three-lane hero, full-frame
  skin cross-section, macro molecular world, shallow-3D lattice, editorial
  lab plate, full-bleed warning. ✅
- On-screen text is a conclusion, not narration duplication — unchanged
  from v3 (not in this pass's scope; v3 already read this way per its own
  design-critique pass). Not re-audited line-by-line this round.
- HyperFrames strict check: **0 errors, 0 warnings**. ✅
- No blank/near-empty transition window on extracted frames — **fixed**
  (see `fix_transition_hold()` above); this was the one acceptance line the
  v3 baseline explicitly failed and disclosed.
- Final audio 48kHz stereo, ~−14 LUFS, ≤−1 dBTP — **not evaluated this
  pass**; deferred with sound design, since no audio was touched.

## Verification commands run against this proof

```bash
cd videos/hyaluronic-acid-vs-filler/05-composition
hyperframes lint
hyperframes check --strict --snapshots --samples 60 --at-transitions --frame-check
hyperframes keyframes . --selector "#s05-size-panel" --shot .hyperframes/size-strip.png --layout strip --from 31.295 --to 43.080
hyperframes keyframes . --selector "#s07-binds-panel" --shot .hyperframes/binds-strip.png --layout strip --from 51.207 --to 59.832
hyperframes keyframes . --selector "#s09-crosslink-actor" --shot .hyperframes/crosslink-strip.png --layout strip --from 67.653 --to 78.044
hyperframes snapshot --at 0,1.2,5.8,10.1,21.8,31.3,43.0,51.2,59.8,67.7,78.0,84.1,90.5,103.2,115.9,120.3
python3 ../../../catalog/tooling/check-safe-area.py . ../06-render/proof-v4/draft.mp4 --landscape
python3 ../../../catalog/tooling/check-static-hold.py . ../06-render/proof-v4/draft.mp4 --landscape
python3 ../../../catalog/tooling/check-cadence.py . ../06-render/proof-v4/draft.mp4 --longform
python3 ../../../catalog/tooling/continuity-audit.py . --gate
```

## Next steps for a publish-ready render

1. Sound design pass (deferred above) — music bed + SFX + ducked mix.
2. Full-quality render (`hyperframes render --quality high --workers 1`),
   not this draft-quality proof.
3. Run the project's own `postrender` chain (`package.json`) on that
   high-quality output, including the existing loudnorm mastering step this
   session did not touch.
4. Re-run all four pixel gates above on the final mastered file, not this
   proof (draft quality + raw narration mux).
