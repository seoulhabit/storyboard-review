# T6 — Recurrence — DONE

Commits: claude-skills branch `wo-fvc-005-t6` off `origin/master` (`e0d3b67`,
the merged T5 fixes); Story Board branch `session/wo-fvc-005-t6` (the
populated `videos/_queue.yaml` + this status).

## What shipped

- **`makemeavideo/scripts/enqueue_from_site.py`** (new): diffs the site
  repo's published `content/ingredients/*.json` routes against
  `videos/_queue.yaml`'s own `queue[]`+`produced[]` (not against a second
  git SHA — see the script's own docstring for why a route-level diff on
  raw commit ranges would be the wrong mechanism), and appends the
  difference. Zero-evidence routes (WO sec 8.9's own nine) are enqueued,
  not dropped — sorted to the back so `/makemeavideo next` reaches the
  strongest passports first — and each entry records its own
  citations/findings count so the coming K-2b halts are visible before
  they're spent on.
- **`SKILL.md`/`policy.md`/`runbook.md`**: `/makemeavideo next` added to
  the front door, resolving `queue[0]` into an ordinary `request.yaml`/
  `story.md` pair before S0.0's own `validate_request.py` step, then
  running exactly as a hand-authored `new` run would. `BLOCKER-QUEUE-EMPTY`
  added alongside the other stop conditions.
- **`videos/_queue.yaml`**, populated for real: 20 queued (evidence-rich
  first: `ceramide` 8 citations down to the nine zero-evidence routes at
  the back), 1 produced (`centella-asiatica`, T5's pilot).

## Two real bugs found while proving this, not assumed clean

1. **`centella-asiatica` came back as "new" on the very first real run.**
   Nothing populates `produced[]` retroactively, and T5's own pilot
   predates this script entirely. Fixed by also checking
   `videos/<slug>/09-run-report.md` for any slug that's ALSO a currently-
   published route (scoped that way on purpose: this repo has other
   `videos/<slug>/09-run-report.md` directories from an older, unrelated
   pipeline — `hyaluronic-acid-vs-filler`, `snail-mucin-medical-secret` —
   sharing the same report filename by convention but never sourced from a
   seoulhabit-learn route; none of their slugs collide with a real
   ingredient handle, confirmed by checking, but backfilling every
   `09-run-report.md` in the repo into this queue's own `produced[]`
   would have been noise this file's readers have no reason to see).
2. **`_yaml_lite.py`'s own reader requires an INDENTED list under a key,
   not flush-left** — real YAML allows both, but `_parse_block()` only
   descends into a list when the line after `key:` is indented strictly
   more than the key itself. A flush-left first draft
   (`queue:\n- slug: x`) round-tripped as `queue: None`. Found by actually
   testing the round-trip (write, then read back with the same parser
   `/makemeavideo next` will use), not assumed from the docstring's own
   description. Fixed in `dump_queue_yaml()`'s own indentation, matching
   `providers.yaml`'s existing convention (`roles.tts_preflight:` at
   indent 2, its `- id: ...` items at indent 4) — `_yaml_lite.py` itself
   was not touched, since the fix belongs in the one writer producing
   this shape, not in a parser other scripts already depend on.

## Judgment call: stdlib-only, not PyYAML

`requirements.txt`'s own header states every script but `qa_render.py` is
stdlib-only "by deliberate policy." `enqueue_from_site.py`'s first draft
imported `yaml` (PyYAML) since it needs to both read AND write YAML, and
`_yaml_lite.py` only reads. Rewritten to use `_yaml_lite.parse_yaml_subset`
for reading and a small, narrow `dump_queue_yaml()` for writing — scoped
to exactly this file's own shape (a block list of flat mappings), not a
general YAML dumper, matching `_yaml_lite.py`'s own stated philosophy
("not a general YAML parser — verify against a new file's actual shape").

## Accept check

**Done-when, per the WO's own bar**: "the queue is populated from the
current live routes and the pilot's readout is scheduled." Both true —
`videos/_queue.yaml` has 20 real entries from the current live
`seoulhabit-learn` routes (verified idempotent: a second run finds 0 new),
and T5's own `08-readout-schedule.md` already scheduled the pilot's 48h/7d
readout.

**Not done, named rather than silently skipped**: `next` mode's own
request.yaml/story.md-writing step (runbook.md's own new "Next" section)
is documented but not exercised end-to-end this session — actually running
`/makemeavideo next` on the real queue is a production run in its own
right (the next real pilot), not something to spend inside a
recurrence-infrastructure task. Template auto-detection beyond a uniform
T1 default (WO sec 4.4's T2-T6 routing) is not attempted — named as a
limitation in the script's own docstring, not guessed at from weak
signals.
