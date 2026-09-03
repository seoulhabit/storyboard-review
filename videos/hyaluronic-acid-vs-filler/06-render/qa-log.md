# QA log — hyaluronic-acid-vs-filler (v2 revision)

## Gates

| Gate | Result | Measured on |
|---|---|---|
| `hyperframes@0.8.22 check` | **ok: true**, 0 errors across lint / runtime / layout / motion / contrast, 3 accepted warnings | the composition under seek, 40 samples |
| `check-safe-area.py --landscape` | **PASS — no findings, 640 frames sampled** | `06-render/final.mp4` |
| `check-static-hold.py --landscape` | advisory (exit 0); **no findings** — whole-frame pass (320 samples, 10.0s ceiling) and region-aware pass (2×3 grid, 1.0s content-then-empty ceiling) both clean | `final.mp4` |
| `check-cadence.py --longform` | advisory (exit 0); **16.5% whole-video active share**, no scene exceeds the 6.0s quiet ceiling | `final.mp4` |
| `continuity-audit.py` | 12/12 boundaries transitioned · top entrance signature 23.0% · top raw ease 40.0% · 0 rebuilt actors · 14 camera-move tweens · 0 plain-crossfade-across-ground violations | source |
| `ebur128` | **−14.5 LUFS integrated, −2.3 dBTP, LRA 2.0** | `final.mp4`, not the loudnorm intermediate |
| `ffprobe` duration | video **160.000000 s / 4800 frames @ 30 fps** == VO master clock exactly | `final.mp4` |

**Two full safe-area re-renders were needed**, both catching real ink in the
reserved zone that `hyperframes check`'s layout pass reported as completely
clean (0 errors) each time — see `00-decision-ledger.md`'s `## re-run`
section for the root-cause diagnosis on each (s05-compare's vertical budget,
then s11-do-not-inject's hold-drift on already-tight content). The layout
pass checks declared containers; it has no notion of the canvas edge or the
reserved safe-area zones, which is exactly why `check-safe-area.py` is the
authoritative gate and not a formality after `check` passes.

**Cadence, in context.** 16.5% of 8fps steps carry a perceptible, localised
change — higher than this project's own 180s cut (15.1%) and the long-form
comparator `ectoin-survival-molecule` (14.0%), consistent with a materially
denser scene count per minute (13 scenes / 160s = one scene every 12.3s,
vs the 180s cut's one every 12.9s) and several newly-added animated elements
(droplet convergence in s08, the loose-to-lattice crossfade in s10).

**Post-code-review re-render.** `/code-review high` on PR #11 surfaced 10
findings, all fixed same-session (see `00-decision-ledger.md`'s
`## re-run — code-review fix pass` section for the full list and root
causes). Two of the ten (C2, C3) changed rendered output: `s05-compare`'s
wipe beat and `s11-do-not-inject`'s slam beat now go through the file's
own `_row_tweens()` helper instead of hand-rolled loops, which is why
cadence moved from the pre-fix render's 18.1% to 16.5% — fewer,
more consistent beats from the house entrance treatment, not a coverage
loss (still above the 180s cut's 15.1%). All gates in the table above are
measured on this post-fix `final.mp4`, not the pre-fix render; safe-area,
static-hold, loudness and duration were unaffected as expected, since none
of the 10 fixes touched claim wording, sourcing, layout dimensions, or
audio — but all three pixel gates were re-run rather than assumed clean.

## `[K-4]` — rendered-claim check, on the extracted frames

| Check | Verdict |
|---|---|
| No internal record id (`ING-*`) anywhere | **PASS** — confirmed across all 13 scene frames |
| No PMID on any frame | **PASS** — chips render `Journal · Year` or `FDA · Dermal Fillers`; PMIDs and DOIs are in the description only |
| On-screen wording hedges at least as far as the VO | **PASS** — verified on extracted frames: `s06-serum-size` at t≈62s reads "Smaller ones **may** travel farther into the upper layers of skin"; `s07-plumping` at t≈75s reads "Hydrated surface cells can **temporarily** make fine lines **appear** softer" — both hedges legible in the on-screen type, not audio-only |
| Nothing hard-prohibited appears | **PASS** — the only on-screen number is `1934` (cited); `DO NOT INJECT YOURSELF` and the risk lines are FDA-verbatim; no *treats/prevents/cures*, no comparative superiority (the "not X" distinctions — "Neither behaves like a filler", the C0 thesis — assert difference, not superiority), no absolute language |
| One citation treatment throughout | **PASS** — the mono pill, unified across all 13 scenes (carried forward from the 180s cut's own `[K-4]` fix) |

**One `[K-4]`-adjacent finding, fixed during S7 rather than shipped:** the
1930s eye+glassware illustration (`s03-origin`) and the clinical vignette
(`s11-do-not-inject`) were both drawn browser-native (inline SVG line art)
rather than generated — no needle enters skin anywhere in either, no
photographic realism, both hold to the "elegant, non-graphic" and "calm,
professional, no frightening stock photography" briefs on inspection of the
extracted frames.

## `design-critique` — frame review

`COMPANION-RESOLVED:design-critique (skill-tool)`. Applied to frames
extracted from the muxed deliverable, both before and after the two
safe-area fix cycles.

### First impression
Frame zero states the thesis in text and shows it in the diagram in the same
instant — "Your hyaluronic-acid serum cannot do what filler does" over the
three-lane molecule lineup, category icons legible, all three lanes composed
at rest. The video's whole argument is visible before a single beat animates.

### What works
- **The backbone does what it's for.** The three-lane diagram opens the
  film, resolves it (s12-badges), and the intervening dives (s05, s06, s10)
  never redraw it — they extend the same actors. `continuity-audit.py`
  confirms this structurally (0 rebuilt-actor pairs); the extracted frames
  confirm it visually.
- **The side-by-side comparison (s05) reads instantly** — "Serum — Surface"
  next to "Filler — Beneath the Skin", each panel's own cross-section making
  the claim the text makes. Lands well before the 1:00 mark the feedback
  asked for.
- **The loose-chains-to-lattice crossfade (s10) is a genuine transform**, not
  a cut — verified on extracted frames either side of the swap beat (t≈107s
  loose, t≈112s settled lattice). Honest about what the engine can actually
  do (opacity/scale, not path morphing) while still reading as a structural
  change.
- **The clinical vignette (s11) does real work in a small space** — capped
  syringe, vial, gloved hand, no needle touching anything, established
  before the full-bleed warning text takes over.
- **The final message holds long enough to be read twice** — "Serum
  hydrates. Filler adds volume. Same name, different jobs." is on screen
  from ≈151.9s to 160.0s, over 8 seconds, well past the requested 3s floor.

### Findings

| Finding | Severity | Action |
|---|---|---|
| s05-compare's original layout put roughly 700px of content into a 560px lane row — no ink was in the reserved zone yet at the design-critique stage, but the margin was already visibly tight on the extracted frame | 🔴 Critical (confirmed by the pixel gate, not just this review) | **Fixed.** Actor 340→260px, title 104→64px, body text to the type floor. |
| s11's hold-drift pushed already-bottom-heavy content further down on one beat | 🟡 Moderate (confirmed by the pixel gate) | **Fixed.** Drift magnitude capped for this scene specifically. |
| The category icons on s01 (bottle/body/syringe) are small enough that at a glance they could be mistaken for decoration rather than the "three categories" the brief asked for | 🟢 Minor | **Accepted.** They sit directly above each molecule actor with consistent teal tinting and read correctly once the lane labels arrive a beat later; the actors themselves already carry the primary identity signal. |
| Lane scenes remain top-heavy (unchanged from the 180s cut's own accepted finding) — the lower third is reserved for foot copy that enters later | 🟢 Minor | **Accepted**, same reasoning as the 180s cut: the space fills as the beats land, not wasted. |

### Accessibility
- Contrast: `check`'s pass measures WCAG AA on rendered pixels — **0
  failures** (down from 2 warnings mid-cycle, both fixed: the kicker/accent
  color on paper measured 2.17:1 against a 3:1 floor for large bold text,
  resolved to the same accessible teal `check` itself suggested).
- Text sizes: hero 64–112px depending on scene, body 40–58px, caption 44px,
  chip 32px — all at or above `[S6/A-6]`'s floors, with 32px the absolute
  floor honored throughout, including the newly-scoped `.cmp-col .body`
  (set to exactly 40px, not below it).

## Warnings left standing, with reasons

- `layout / container_overflow` ×3 — a `hold` drift scales the padded stage
  slightly, so its **box** crosses the canvas edge by a small margin. No
  **ink** does: `check-safe-area.py` on rendered pixels reports 0 findings
  across 640 frames, and that scan — not a bounding-box test — is the
  authority. Same accepted class the 180s cut logged for the same reason.
