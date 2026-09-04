---
workflow: faceless-explainer
flow: automation
storyboard: yes
message: "A specific snail secretion has real, narrow clinical evidence behind it — but that does not make every snail-mucin product on the shelf a miracle, and TikTok skipped the parts that would tell you which is which."
destination: shorts
aspect: 1080x1920
language: en
audience: "skincare-curious social viewers who've seen snail mucin trend but don't know the science"
length: 75s
angle: concept
style_preset: editorial-forest
CLAIM_LEDGER: required
VO_MODE: not-verbatim
---

## Intent

Rebuild `videos/snail-mucin-medical-secret` (113.84s, shipped 2026-08-29) as a **new sibling
project**, not an edit in place — the original render and its source stay untouched for a clean
before/after comparison. See `videos/snail-mucin-medical-secret/00-decision-ledger.md` and
`09-run-report.md` for the render-mode pass that fixed that project's safe-area / type / contrast /
transition / audio defects on 2026-09-03; this is a separate, story-level rebuild, not a
continuation of that pass.

This rebuild is a direct response to an engagement review (2026-09-03) whose measurements were
independently verified before acting on them: practical payoff at 74.0s (65% of runtime), 27.84s of
hook+setup before any substance, near-zero shot-level visual change with global karaoke captions
doing all the visible motion. The review's own numbers are recorded in
`BEFORE-AFTER-EVAL.md` §Baseline.

## §Revision note — why `VO_MODE: verbatim` is gone

v1's `BRIEF.md` (§Customizations) locked `VO_MODE: verbatim` after a `/goal` Stop-hook rejected an
earlier, evidence-tuned build for not matching the user's exact pasted script. That decision
deleted the citation apparatus wholesale and shipped six `[K-2a]`-hard-prohibited claims
("miraculous cure," "instantly heal," "massive doses," "Allantoin to heal wounds," "Zero harm,
zero stress," an unsourced humectant-harm mechanism) with zero citation identifiers anywhere in
the project.

**The current user request explicitly reverses that decision** — the whole point of this rebuild
is scientific responsibility over the original wording. `VO_MODE` is therefore **not** set to
verbatim; the script in `SCRIPT.md` is a rewrite built from `CLAIM-LEDGER.md`'s allowed wording,
not a retiming of the user's original pasted paragraph. This is a considered reversal of a prior
project decision under new, explicit instruction — not a silent override.

## §Sourcing

See `CLAIM-LEDGER.md` — the `[K-1]` claim table, written before this script, with four sources
actually read (not just cited): a 1999 controlled radiodermatitis trial, two small randomized
trials of one branded extract (2013, 2020), and a 2024 lab comparison of four commercial products
by extraction method. `[K-2b]`'s ratio check does not fire disclosure-forward — sourced claims
outnumber unsourced in both the Mechanism and Proof sections, because the sourcing pass found real
evidence to report rather than an evidence vacuum.

## §Customizations

- **Photoreal generated imagery** for tactile/process/application beats only (chapters 1, 5, 6, and
  the chapter-7 callback) — per explicit user direction, same departure from the faceless-explainer
  "invented graphics only" default that v1 used. Mechanism and evidence chapters (3, 4) stay
  browser-drawn so realism cannot masquerade as proof — this is new for v2; v1 used photoreal
  imagery under its evidence beats too, and that is part of what made an unsourced claim read as
  documented.
- Reuse `style_preset: editorial-forest` for on-screen type, extending the same design system as
  v1 and the wider SeoulHabitSkin channel.
- Voice unchanged: Kimberly, `voice_id: 674b71b8-1d2e-4087-8567-d1f53c0b9f3c`. A new script means a
  full VO regeneration and retime regardless of voice choice.
- **Engine pin: `hyperframes@0.8.27`**, not v1's `0.8.17`. This is new work, not a reproduction, so
  there is no reproducibility contract to preserve. Verified via
  `hyperframes upgrade --project . --check` on the v1 project: "would bump project scripts
  0.8.17 → 0.8.27." v1 stays pinned at 0.8.17, untouched.
- `length` follows the script's own measured VO duration (measured from TTS, not estimated),
  targeting 75s ± the format's own chapter-boundary rounding.

## §Reused assets

Plates copied from `videos/snail-mucin-medical-secret/public/` (all 1152×2048, exactly 9:16, zero
crop headroom — `object-fit: cover` at 1080×1920 consumes the entire source):
`01a-archival-lab.png`, `01b-macro-slime-spatula.png`, `04-snail-mesh.png`,
`02-routine-montage.png`. BGM track (`assets/bgm/track.loop.mp3`, `track.mp3`) and the project's
three fonts copied unchanged. New photoreal plates needed: see `ASSET-SPECS.md`.

## §Format-specific ordering (new — not in v1)

The six-section spine in `faceless-video-craft` SKILL.md (Hook → Misconception → Mechanism →
Proof → Application → Recap) puts Application 5th of 6, which is exactly why v1's payoff landed at
65% of runtime. This rebuild reorders for a Short: **Hook → Immediate Answer → Mechanism → Proof →
Extraction Reality → Application → Verdict** — the useful truth by 0:12, mechanism and proof in the
middle third, application still gets its own full chapter rather than being compressed into the
outro. This reordering is logged as a proposed skill change, not invented ad hoc — see
`SKILL-IMPROVEMENT-PROPOSAL.md` item 2.
