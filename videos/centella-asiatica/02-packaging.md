# 02-packaging.md — centella-asiatica

## S2 — Topic gate

- **T-1 seed**: `centella asiatica skincare` (shortest noun phrase naming the
  mechanism/subject).
- **T-2 search demand**: seed itself FAILS (`overall 34.6`, `volume 0` —
  "Very low"). Highest-`overall` related keyword still matching the brief:
  **`centella`** (`overall 67.9`, `volume 67.9`, `competition 32.1`) — PASSES
  both bars (`overall≥50` and `volume≥40 & competition≤60`). **Seed swapped**
  to `centella` (logged).
- **T-3 outliers** (`keyword=centella, contentType=short,
  publishedWithin=sixMonths, minSubscribers=0, maxSubscribers=10000,
  limit=20`): PASS — top result `breakoutScore=29.95` ("Centella Poremizing
  Fresh Ampouls...", Budget Hut Cosmetics) ≥ the 3 default.
- **T-4 title-pattern harvest** — **judgment call, ledgered**: the
  literal top-5-by-`breakoutScore` in the raw result set are keyword noise
  unrelated to centella skincare (a Monica Bellucci clip at 606.97, a gaming
  video at 246.93, etc. — "centella"/"centaur" string collisions, not
  content matches). Harvested shapes from the top-5 **relevant** (actually
  about centella/skincare) results instead: mostly flat product-tag
  captions ("Centella X For Y", hashtag-heavy) and one "X vs Y" comparison
  ("Roundlab vs Skin1004 Centella Tone Brightening Sunscreen"). No
  question-hook or "why X" shape appears among the relevant results in this
  niche on Shorts — informs the title/hook choice below (a direct question
  reads as differentiated against a field of flat product tags), not a gate.

## S3 — Packaging

- **Title candidates** (`vidiq_generate_titles`, `type=short`):

  | Title | Score |
  |---|---|
  | What human studies say about Centella Asiatica #skincare #science | 92 |
  | Centella Asiatica: Does it actually work? #skincare #science | 91 |
  | Is your Cica cream doing anything? #skincarehacks #beauty | 85 |
  | The hidden risk of using Centella Asiatica #skincaretips #dermatology | 85 |
  | Thinking of using Cica? Read this first #skincare #skincaretips | 84 |

  Cross-checked the top candidate with `vidiq_score_title` independently:
  **92**, consistent. Per `baseline.yaml packaging.title_scorer_discriminative:
  false`, the score is read as directional, not decisive — picked the top
  candidate because it also independently reads accurately (an evidence
  check, not an overclaim) and avoids "actually"/hype phrasing.

- **Chosen title**: **"What human studies say about Centella Asiatica"**
  (score 92). Hashtags dropped from the on-platform title field, kept as
  tags below.

- **Thumbnail (P-3)**: Shorts branch — frame 0 **is** the thumbnail (the
  compiled hook scene, `ShHook`, per `H-2`'s frame-zero rule). No separate
  `vidiq_generate_thumbnail`/`vidiq_score_thumbnail` call (long-form only).

- **Description**: "A 45-second evidence check on centella asiatica (cica):
  what the human studies actually tested, the safety data, and who should
  patch test first. Sources in the pinned passport: seoulhabit.com/ingredient/centella-asiatica"

- **Tags**: centella asiatica, cica, gotu kola, k-beauty, korean skincare,
  skincare science, skincare ingredients, evidence-based skincare

- **Chapters**: not applicable — Shorts carry no chapter markers.

## Ledger

vidIQ calls this run: `vidiq_balance` (0 credit) + `vidiq_keyword_research`
+ `vidiq_outliers` (5 credit) + `vidiq_generate_titles` (5 credit) +
`vidiq_score_title` (5 credit) = **4 billed calls, 15 credits**, against the
8-call / 200-credit caps (`PR-3`, `providers.yaml`). `vidiq_balance` before:
355. Balance after: not yet re-checked (will re-check at run close, `H-7`
equivalent for vidIQ).
