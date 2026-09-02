# Pipeline runbook — story in, MP4 + envelope out

Execute stages in order. Each stage lists: entry condition, calls, artifact,
gate. Rules referenced as `[S2/T-2]` live in `decision-policy.md`. Tool names
are the vidIQ MCP tool names as exposed at the time of writing; if a name has
changed, search the tool list for the closest match and log the substitution.

Working directory for a run: `./outputs/<slug>/` relative to the project, where
`slug` is the seed keyword, kebab-cased, prefixed with the date
(`2026-09-01-niacinamide-barrier`). Use the host's own outputs directory instead
if one exists. **Never assume `/mnt` is there** — it is not, on this host.

**Pin.** Read the hyperframes pin from the project's `package.json` scripts
(`npx --yes hyperframes@X.Y.Z check`) and use that exact version for every CLI
call in the run. This repo has no root `package.json`.

---

## S0 — Baseline (entry: `[S0/B-1]` says refresh)

Calls (owned-channel data; requires vidIQ YouTube authorization —
`vidiq_authorize_with_youtube` if a call returns verification_required):

1. `vidiq_user_channels` → channel id, subs.
2. `vidiq_channel_analytics(channelId, report=top_videos, startDate=−365d, maxResults=200)` → per-video views, avg-view-%, avg duration.
3. `vidiq_channel_analytics(report=shorts_vs_longform_split, −90d)`.
4. `vidiq_channel_analytics(report=traffic_sources, −90d)` → record **every**
   source the tool returns with its own labels, plus `shorts_feed_share`
   (`[S0/B-3]`). A four-slot browse/suggested/search/external schema cannot
   describe a Shorts channel.
5. `vidiq_channel_performance_trends(channelId)` → view-accumulation curve.
   Record the percentiles **the tool actually returns** (`perc30`, `perc70`,
   median) — there is no `p75`. The p30–p70 band is the run's noise floor.
6. Per-video retention. `report=top_videos` returns per-video
   `averageViewPercentage` and `averageViewDuration` — pull it **first**, and do
   not record retention as unavailable until that path has been tried. Then
   `report=audience_retention, filters=video==<id>` for the top 3 and bottom 3
   by avg-view-% → aggregate into a 10-bucket curve; on a small channel this
   call can legitimately return zero rows while top_videos still has the metric.
7. `vidiq_subscriber_insights(channelId)` → best publish windows.
8. `vidiq_voiceover_list_voices` → confirm the baseline voice id still exists.

Artifact: rewrite `references/channel-baseline.md` from the template at its top
(all fields, `populated: true`, date). Ledger: one line per field filled, with
`not available via vidIQ` where a call failed.

Gate: baseline has at least `channel.subs`,
`formats.<fmt>.median_views_per_upload` for the chosen format, and
`retention.avg_view_pct_<fmt>` — otherwise proceed with [default]s and tag the
run `baseline-partial`. Use the real schema key names: a rule that reads a field
the schema does not have fails silently to its default (both of this gate's
original names were wrong, found 2026-09-02 by validating every documented field
reference against the YAML).

## S1 — Story (entry: input received)

1. Normalise the input into the six-section spine (`SKILL.md` §What
   "educational" changes). Pull only from the input material; mark generated
   bridging sentences `[GEN]`.
2. Apply `[S1/S-5]` completeness, `[S1/S-1]` format, `[S1/S-2]` length,
   `[S1/S-3]` presenter, `[S1/S-4]` voice.
3. **`[K-1]` claim inventory.** List every assertion the video will make and
   classify each (nominal / sourced / unsourced / illustration / editorial).
   Unclassifiable defaults to `unsourced`; an identifier nobody read is not a
   source. Apply `[K-2]` and `[K-2a]` — anything hard-prohibited is sourced or
   cut here, before a word of script exists, because cutting it later re-times
   everything downstream of the voiceover.
4. **`[K-2b]` ratio limb.** If unsourced ≥ sourced across Mechanism and Proof,
   the run switches to the disclosure-forward form. Log it now; it changes what
   S4 writes.

Artifact: `01-story-brief.md` — spine sections, format, target length,
presenter, voice, and **§Sourcing: the `[K-1]` table** (on-screen chip | backing |
what it actually supports).

## S2 — Topic gate

1. `[S2/T-1]` seed.
2. `vidiq_keyword_research(mode=research, keyword=seed, country=US)` → `[S2/T-2]`.
3. `vidiq_outliers(keyword=seed, contentType=long|short, publishedWithin=sixMonths, maxSubscribers=10×subs, limit=20, sort=breakoutScore)` → `[S2/T-3]`, `[S2/T-4]`.
4. If reframe needed: `vidiq_keyword_research(mode=questions, keyword=seed, limit=10)`.

Artifact: `02-packaging.md` §Topic — seed, metrics, verdict, `title_shapes[]`.
Gate: PASS / PASS-on-browse / experiment. Never a halt (topic weakness is a
budget signal, not a stop).

## S3 — Packaging

1. Five titles per `[S3/P-1]`; `vidiq_score_title` each; second round if needed.
2. `[S3/P-2]` concept; `vidiq_similar_thumbnails(description=concept, publishedWithin=sixMonths, limit=20)`.
3. Long-form: `vidiq_generate_thumbnail(title=winner, userQuery=concept, orientation=landscape)` → poll `vidiq_job_poll` → `vidiq_score_thumbnail` → `[S3/P-3]`. Save the image to `04-assets/thumbnail.png` (download the imageUrl; do not leave a signed URL as the only copy).
4. `[S3/P-4]` description skeleton and tags (chapters filled in S5).

Artifact: `02-packaging.md` complete except chapters.
Gate: a title and (long) a thumbnail exist with recorded scores.

## S4 — Script and voiceover

1. `[S4/V-1]` word budget; write the script section by section per `[S4/S-6]`,
   under `[K-3]`: an unsourced claim carries its attribution verb in the VO **and**
   in the on-screen type, and the on-screen wording hedges at least as far as the
   voiceover — the muted viewer reads the type, not the voice.
2. `vidiq_voiceover_generate(script, voiceId, output=url_only)` → poll → duration. Apply `[S4/V-2]`. Download the MP3 to `04-assets/vo.mp3`.
3. `[S4/V-3]` music → `04-assets/music.wav` (or house track path).
4. Captions file: `04-assets/captions.json` — `[ {text, charStart, charEnd} ]` per caption chunk.

Artifact: `04-assets/script.md`, `vo.mp3`, `music.*`, `captions.json`,
`manifest.json` (every file, source, licence, absolute path).
Gate: VO duration within target ±15 % (after ≤ 2 generations).

## S5 — Beat sheet (switch to Opus/High here)

1. Read `youtube-delivery.md` first — hook, cadence, safe areas, end scene are
   beat-sheet inputs.
2. `[S5/C-1]` beats from VO timing; `[S5/C-2]` cadence; `[S5/C-3]` end scene.
3. Write `03-beat-sheet.json` against `assets/beat-sheet.schema.json`.
4. Fill chapters into `02-packaging.md`.

Artifact: `03-beat-sheet.json`. Gate: schema-valid; scenes tile the timeline
with no gap or overlap; beat 0 starts at 0.00; scenes total the VO duration
±0.15 s; no still window above the cadence cap. **All of these are enforced by
`scripts/beats_to_composition.py`, which exits non-zero and names the scene** —
so the gate is the generator refusing to emit, not a reading pass.

## S6 — Composition

1. Read `hyperframes-engine.md` and the pinned version's shipped docs.
2. `[S6/A-1]` **check `catalog/` first** — for mechanisms as much as imagery —
   then generate/collect plates into `04-assets/plates/`; update the manifest.
3. `[S6/A-2]` tokens; `[S6/A-3]` spatial plan + frame zero (written into
   `05-composition/spatial-plan.md`); `[S6/A-4]` fps; `[S6/A-5]` border-box;
   `[S6/A-6]` type floors; `[S6/A-7]` contrast.
4. **Generate, do not hand-write:**

   ```bash
   python3 scripts/beats_to_composition.py 03-beat-sheet.json 05-composition/
   ```

   This emits `index.html`, `compositions/frames/NN-<id>.html` and
   `index.motion.json` from the beat sheet, with the `#root` attributes, the
   `.clip` timing, and the paused timelines registered on `window.__timelines`.
   Timing is never hand-typed into the HTML — edit the beat sheet and re-run.
   `assets/composition-skeleton.html` and `assets/scene-skeleton.html` document
   the emitted shape for the rare root the generator does not cover.
5. Layout check with `debug-layout` on `#root` → `check --snapshots` → fix →
   remove the class → confirm on frame 0.
6. Motion pass: easing, stagger, camera. One idea at a time. For motion
   vocabulary use `/hyperframes-animation`; for camera moves and Ken Burns,
   `/hyperframes-keyframes`; for how footage and plates are treated,
   `/media-use` and its `references/media-treatments.md`. Do not improvise
   equivalents.

Artifact: `05-composition/{index.html, compositions/frames/*.html,
index.motion.json, hyperframes.json}`, `spatial-plan.md`.
Gate: `[S7/R-1]` `check` passes before render is attempted.

## S7 — Render QA

1. **The gate** — `[S7/R-1]`, from inside `05-composition/`:

   ```bash
   npx --yes hyperframes@<pin> check --json --snapshots
   ```

   Errors gate; warnings are logged. `--strict` only if the project already
   runs strict. Cap 3 fix cycles → **HALT: BLOCKER-CHECK**. Save the envelope to
   `06-render/check.json`. The motion sidecar (`[S7/R-1b]`) is picked up
   automatically — no flag.
2. Render → `06-render/raw.mp4`:

   ```bash
   npx --yes hyperframes@<pin> render --quality high --workers 1 -o 06-render/raw.mp4
   ```

   Use `--docker` when byte-identical output across hosts is required.
3. Mux and master `[S7/R-3]` — note `TP=-2.5`, not `-1.5`, to leave AAC
   intersample headroom:

   ```bash
   ffmpeg -i 06-render/raw.mp4 -i 04-assets/vo.mp3 -i 04-assets/music.wav \
     -filter_complex "[2:a]volume=0.25[m];[1:a][m]amix=inputs=2:duration=first[a];\
                      [a]loudnorm=I=-14:TP=-2.5:LRA=11[out]" \
     -map 0:v -map "[out]" -c:v copy -c:a aac 06-render/final.mp4
   ffmpeg -i 06-render/final.mp4 -af ebur128=peak=true -f null -   # measure the SHIPPED file
   ```

4. **Post-render pixel gate `[S7/R-2]`, on the muxed deliverable:**

   ```bash
   bash scripts/extract_frames.sh 06-render/final.mp4 06-render/frames/
   python3 catalog/tooling/check-static-hold.py <project> 06-render/final.mp4
   python3 catalog/tooling/check-safe-area.py  <project> 06-render/final.mp4 \
     --safe-top 192 --safe-bottom 384 --safe-right 162 --safe-left 72
   ```

   Confirm each script's crop constants against *this* project's own
   `index.html` before trusting a "0 findings" — an inherited caption band
   silently excludes real content. Look at every frame.
5. **`[K-4]` rendered-claim check**, on the same frames: every unsourced claim
   shows its flag concurrently; the flag is not the accent colour and not
   citation typography; no internal record id anywhere; the on-screen wording
   hedges at least as far as the VO at that timestamp; nothing hard-prohibited
   appears. `check` cannot see any of this. Failure is `BLOCKER-CLAIM`, cap 2.
6. `ffprobe` duration check (video == VO ±0.1 s); write `06-render/qa-log.md`.

Artifact: `06-render/{final.mp4, check.json, frames/, qa-log.md}`.
Gate: `check` clean, pixel, duration, and true peak measured on `final.mp4`.
(Switch back to the cheaper tier after this stage.)

## S8 — Publish envelope

Write `07-publish-envelope.md`: title, description (with chapters and sources),
tags, pinned comment, end-screen element map (which zone → which video/
playlist), proposed schedule window `[S8/E-2]`, and the thumbnail path.
`[K-5]`: the description and pinned comment state which claims are unsourced —
a disclosure that exists only inside the video is not a disclosure to anyone
reading the page.
**No write calls.** Present the envelope; the publish action is Kim's.

## S9 — Readout schedule

Write `08-readout-schedule.md` with the two dates (48 h, 7 d after publish) and
the exact calls (`learning-loop.md`). When a readout is run, it appends to the
ledger and may rewrite `channel-baseline.md` per `[S9/L-2]`.

---

## Stop conditions

See `decision-policy.md` §Stop conditions. A halt message has three lines:
the blocker name, what is already in the output folder, and the one fact that
resumes the run. Nothing else.

## Re-running a stage

Stages are idempotent on their inputs. To re-run S6 after a beat-sheet edit,
delete `05-composition/` and start at S6; the ledger keeps the earlier lines
and appends new ones under a `## re-run` header.
