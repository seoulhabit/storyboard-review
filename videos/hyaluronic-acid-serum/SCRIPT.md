# SCRIPT — hyaluronic-acid-serum · v4 (retention cut)

**Voice:** Kimberly (Higgsfield) — model `seed_audio`, `voice_type: element`,
`voice_id 674b71b8-1d2e-4087-8567-d1f53c0b9f3c` — the same voice, model, and
generation route as `videos/pdrn-cellular-science` (its SCRIPT-v2.md documents
the protocol this file follows).
**Voice direction:** calm, sophisticated, distinctly clinical — a specialist
correcting the record, never selling.

**Pacing model (fitted on Kimberly's own takes, PDRN SCRIPT-v2.md):**
`duration ≈ 0.184 × syllables + 1.60 × sentence-stops`. Full stops are
expensive (~1.6s each); energy comes from commas and em-dashes, not periods.
Every block below is 1–2 sentences. Known generation hazards, inherited from
the PDRN log: **no colons in any line** (a colon silently killed a take),
isolate tongue-twisters between commas ("hyaluronate"), and expect ~0.3–0.5s
of leading silence to trim on some takes.

This supersedes the v1 Marcia/HeyGen script (the tutorial cut). The v1 six-beat
factual skeleton — myth correction (S001), decline (S002), damp-skin rule
(S003) — carries over; the register, order of emphasis, and close are new.

---

> **v4 retention rewrite** (producer pass): conversational register, zero
> dalton figures / cell-biology nouns in VO, spoken CTA in the close, hook
> names the ingredient + benefit in the first breath. Measured installs:
> 4.770 / 6.142 / 11.805 / 8.541 / 6.408 / 9.420 = **47.09s VO · 51.7s cut**.

## Block 1 — Hook (Frame 1) · installed 4.77s

    Hyaluronic acid — your skin's biggest drink of water, and the number on the bottle is a myth.

## Block 2 — Identity (Frame 2) · installed 6.14s

    The label says sodium hyaluronate — same molecule, a sugar that grabs water and refuses to let go.

## Block 3 — The myth (Frame 3) · installed 11.81s

    Here's the myth — brands say it holds a thousand times its weight in water, some say six thousand, but measured in a lab it's ten to a hundred, depending on the size of the chain.

## Block 4 — Why you care (Frame 4) · installed 8.54s

    And here's why you care — your skin makes its own, it's what keeps it plump, and after your twenties you lose about six percent every decade.

## Block 5 — The catch (Frame 5) · installed 6.41s

    But here's the catch — this stuff pulls water from wherever it can, so on dry skin, in dry air, it can pull it out of you.

## Block 6 — Protocol + CTA (Frame 6) · installed 9.42s

    The fix is simple — damp skin, serum, then moisturizer to lock it in. If this myth surprised you, tell me in the comments — and hit follow for the next ingredient.

## Claim-safety audit

| Line | Assertion | Record |
|---|---|---|
| B1 | "the number on the bottle is a myth" | ING-hyaluronic-acid-S001 |
| B2 | identity + humectant framing (claim row on screen carries the citation) | ING-hyaluronic-acid-S001 |
| B3 | 1,000×/6,000× unsupported; measured 10–100×, chain-size dependent | ING-hyaluronic-acid-S001 |
| B4 | endogenous HA, plumpness role, ≈6%/decade decline | ING-hyaluronic-acid-S002 |
| B5 | humectant draws from the wetter side — incl. the skin, when air is dry | ING-hyaluronic-acid-S003 |
| B6 | damp + seal protocol | ING-hyaluronic-acid-S003 |

The v3 clinical blocks are preserved in git-less history via
`assets/voice/_v3-staging/` and the render `renders/hyaluronic-acid-serum-v3.mp4`.
