# Betaine Salicylate — VO script (Kimberly / Higgsfield)

Five blocks, written against the fitted Kimberly voice model from
`../pdrn-cellular-science/SCRIPT-v2.md`:

```
duration ≈ 0.184 × syllables + 1.60 × sentence-stops
```

Energy comes from commas and em-dashes, not periods (each full stop costs ~1.6s). No
colons (a colon silently broke generation on the PDRN CTA). No `ACRONYM — expansion`
dash shape (spoken aloud as "slash" there). Wording stays as close to `user_script.txt`
as those constraints allow; nothing is strengthened.

Voice: Kimberly, voice_id `674b71b8-1d2e-4087-8567-d1f53c0b9f3c`, voice_type `element`,
model `seed_audio` — generate the five blocks separately, one render per beat.

### 01 — Hook · predicted ~8.0s
> If you want to clear blackheads without irritation, but traditional salicylic acid leaves your skin red and peeling — stop using it.

(35 syllables, 1 stop. The script's "..." pause becomes the em-dash — a free soft break.)

### 02 — Too harsh · predicted ~8.2s
> BHA is famous for clearing pores, but it can be way too harsh — you don't have to destroy your skin barrier just to get rid of breakouts.

(36 syllables, 1 stop. The two sentences merge on an em-dash.)

### 03 — Identity · predicted ~12.4s
> Meet your new best friend, betaine salicylate. It's literally salicylic acid attached to a hydrating amino acid called betaine — the ultimate gentle alternative.

(50 syllables, 2 stops. The colon after "best friend" becomes a comma. "Betaine
salicylate" gets a clean run-up and a full-stop landing — the PDRN "polydeoxyribonucleotide"
tongue-twister mitigation. Transcript-QA this word specifically; "fibroblasts" was
mispronounced there.)

### 04 — Gentle power · predicted ~8.8s
> That means all the blackhead-busting, pore-unclogging power of a BHA, but with built-in hydration — hands-down the best exfoliant for sensitive skin.

(39 syllables, 1 stop.)

### 05 — CTA · predicted ~11.4s
> You get the glow, without the burn. Have you checked your ingredient list for this yet? Let me know in the comments, and subscribe for more skincare secrets.

(36 syllables, 3 stops — the stops are deliberate here: the CTA needs its three distinct
moves to land separately. "lists" → "list" is the one word-level change.)

**Predicted total ≈ 48.8s VO.** With settle holds (1.0 / 1.0 / 1.3 / 1.0 / 1.5s) the cut
plans to ~54.6s — inside the 60s target with air, so no atempo speed-up is applied
(that was a PDRN-specific operator directive).

## Claim parity vs user_script.txt

Nothing strengthened. Two things came down or moved:

| Block | user script | VO | Effect |
|---|---|---|---|
| 3 | "This is the ultimate Salicylic acid alternative." (own sentence) | "— the ultimate gentle alternative." (clause) | same strength, one fewer stop |
| 5 | "ingredient lists" | "ingredient list" | cosmetic |

Held at parity deliberately: "way too harsh," "destroy your skin barrier," "hydrating
amino acid," "hands-down the best exfoliant for sensitive skin" — each is flagged
UNSOURCED on screen, and the flag needs its referent spoken (the PDRN "burns & grafts"
rule).

## Audio QA gates (standing, from the PDRN rounds)

duration → silence → **transcript diff** → install. Then: trim leading silence only
(validate trims on the trimmed file, never trust whisper's first-word timestamps),
adeclick every take, scan the final 100ms of each processed file for post-decay spikes,
and click-hunt the last second without the quiet-neighborhood filter. Delivery master
normalizes to −14 LUFS / ≤−1 dBTP post-AAC.
