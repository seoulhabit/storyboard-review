# Environment — how-to-repair-skin-barrier

Written by S0.0, first thing, every mode, before any other stage. If a value
can't be determined, write `unknown` — never guess a version or a path.

**Skill version:** 2.1.0
**Surface:** code
**Host:** Darwin / x86_64

**Paths** (see SKILL.md §Paths):
- OUT: `/private/tmp/claude-501/.../scratchpad/t6-run/how-to-repair-skin-barrier/`
  — **overridden for this run.** The §Paths rule resolved to
  `<repo>/videos/how-to-repair-skin-barrier/`, because `/mnt/user-data/outputs/`
  was tested fresh this run and does not exist on this host. The override is
  deliberate: this is a T6 Accept verification against an isolated copy of
  `outputs/2026-09-01-how-to-repair-skin-barrier/`, so that the original run's
  `06-render/` is not overwritten. A production run would use the resolved path.
- CHANNEL: `/Users/sumitchoudhary/Desktop/Story Board/videos/_channel/`
  (`baseline.yaml` present, populated: true, handle SeoulHabit)

**Companions resolved** (see SKILL.md §Companion-skill gates; filled in as
each gate fires during the run, not all at once here):
- frontend-design: `not yet resolved` — S6 entry gate had not fired at S0.0 time
- design-critique: `not yet resolved` — S7 gate had not fired at S0.0 time

**Providers reachable:**
- vidIQ: `ok` — `vidiq_balance` (0-credit call) returned 2316 total
  (1516 renewable of 2000, +800 add-on), renews 2026-10-01
- HyperFrames: `ok + 0.8.26` — on PATH as a global install; FFmpeg/FFprobe 8.1.2
- Higgsfield: `ok` — 2362.25 credits, plan `free`
- Gemini: `no-key` — `GEMINI_API_KEY` unset on this host, so R-1/A-1/V-1 fall
  back to their non-Gemini defaults per their own stated behaviour

**Project skill in play:** `none`
**Budget in force:** `$5.00 per run (providers.yaml budget.per_run_usd), warn at
0.8; 200 vidIQ credits`
**Mode:** `render`
