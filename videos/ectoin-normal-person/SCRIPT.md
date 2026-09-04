# SCRIPT — Ectoin: Explained by SoulHabit, and Then by a Normal Person

Two voices. **SOULHABIT (S)** — calm, credible, occasionally too technical.
**JAY (J)** — curious audience representative who translates the science.

## How to read this file

- **Turn** = one spoken line = one `.wav` = one `<audio>` clip. `t001`–`tNNN`.
- **Scene** = one exchange = one sub-composition file. A scene holds 1–5 turns.
- `VO:` is the **TTS prompt** and may differ from what is on screen. TTS-safe
  rules inherited from the predecessor: **no em-dashes, no colons** — both
  produce odd pauses in this engine.
- `SCREEN:` is what renders. Absent = the scene's visual carries no copy for
  that turn.

### Pronunciation

`ectoin` is written **plain** in every VO prompt. The predecessor tried a
phonetic respelling and it got *worse* ("echetoin"); a plain-spelling retry
fixed it. Do not respell it. Terms that do need checking on the first
audition pass: *Halomonas elongata*, *extremolytes*, *squalane*, *panthenol*.

## Changes — verdict-compression revision (2026-09-03, second revision)

This revision responds to an operator brief with four requirements the prior
(cold-open) revision did not carry: a viewer-facing verdict inside the first
20 seconds, removal of a knowingly false line, a claim ledger (`CLAIMS.md`,
new this revision), and compression to 35–45 turns / roughly 430–500 words —
compressing the mechanism and bottle sections first, per the brief.

**Full turn-by-turn reasoning lives in `scripts/vo_lines.py`'s module
docstring and `00-decision-ledger.md`.** Summary:

1. **`t048` — "None of it passed peer review." — REMOVED.** The prior
   revision retained it by explicit operator decision, VO-only, logged as
   known-bad. It is false (all twelve trials counted for C7 in `CLAIMS.md`
   are peer-reviewed, indexed articles) and it directly contradicted C5 and
   C6, cited approvingly ~30 seconds earlier. This revision's operator
   brief reverses the earlier decision: a knowingly false line does not
   ship for humour or operator preference. See `CLAIMS.md` §Removed.
2. **The verdict now lands inside the first 20 seconds.** Two new turns,
   `t076` and `t077`, follow the "it's a blend" reveal directly: ectoin may
   help dry or stressed skin, the evidence is limited, and it is not a
   miracle or a replacement for treatment. Estimated to complete speaking by
   ~17s at this project's measured per-word pace — see
   `00-decision-ledger.md` for the arithmetic. Real timing supersedes this
   the moment VO exists, as always.
3. **Mechanism (CH2) and bottle sections (CH1, CH5) compressed hardest,**
   per the brief's explicit priority order. CH2 goes from 9 turns/97 words
   to 5 turns/65 words — the largest cut in the script. The "event
   coordinator" gag (`t023`/`t024`) is cut entirely; the celebrity analogy
   (`t019`+`t020`) merges into one turn (`t078`); the hedge that was `t022`
   folds into `t017`'s own sentence instead of standing alone.
4. **A live-verified correction, not a script change:** `CLAIMS.md` finds
   that Bow 2021's dry-condition stress-worsening result (which the *prior*
   revision's changelog claimed "did not surface in PubMed" and cut on that
   basis) **does** surface in the live abstract. That line stays cut here too
   — this is a correction to the historical record, not a reason to restore
   content during a compression pass — but the earlier revision's reasoning
   for cutting it was wrong, and that is now on record.
5. **Result: 58 turns / 595 words → 44 turns / 489 words.** Both the
   35–45-turn band and the ~430–500-word band in the brief are met. See
   `scripts/vo_lines.py`'s docstring for the complete list of what merged,
   what cut, and what stayed verbatim.

### What survives unchanged, by name

The Jargon Alarm's three-beat arc (fire on `t018` in `04-protein`; reach,
no fire, in `05-skin`; retire on `t057` — "You may deactivate the Jargon
Alarm now"), the flat "No." force-field denial (`t029`–`t031`), the
`Promising?/Yes./Miracle?/No.` slam (`t039`–`t042`), the extremolyte gloss
(`t016`, marked do-not-cut in both revisions), the dignity-ship joke
(now one merged JAY turn, `t081`, rather than four), and the "supporting
actor, not superhero" close (`t064`).

## Changes from the submitted draft (prior revision, carried forward as history)

1. **Hook reordered.** The payoff is now turn 1. The draft's opening targeting
   line ("If your skin feels dry, sensitive or irritated…") is **deleted** —
   §6 already opened with the same sentence, so this fixed the hook and
   removed a repetition in one edit.
2. **§4's unverified claim cut** — believed at the time not to surface in
   PubMed. **This revision's live check found it does surface** — see
   §Changes above, point 4. Not restored; the correction is on record.
3. ~~**"None of it passed peer review" retained by operator decision.**~~
   **Reversed this revision — see §Changes above, point 1. Removed.**
4. **"Extremolytes" glossed** (`t016`). It was the one technical term JAY
   never translated.

---

## CH1 — Turn the bottle around, then the verdict, then the origin

### U01 · the reveal
- t071 **S** VO: This bottle says eleven percent. Does that mean eleven percent ectoin?
  SCREEN: `11%` swells on the front label
- t072 **S** VO: No. It's a blend.
  SCREEN: the label turns (scaleX through zero); INCI list wipes in on the back; illustrative-label tag

### U01 · the verdict — NEW this revision, inside the first ~20s
- t076 **S** VO: Ectoin itself may genuinely help dry or stressed skin feel more comfortable.
  SCREEN: `MAY HELP` — dry/stressed skin, plain statement, no citation pill (this is the video's own framing, not a single sourced claim)
- t077 **S** VO: But the evidence is limited, and it is not a miracle or a replacement for treatment.
  SCREEN: `LIMITED EVIDENCE` / `NOT A MIRACLE` / `NOT A REPLACEMENT FOR TREATMENT` — three short claims, same panel-strike idiom `10-notprove` uses later, establishing the visual grammar early rather than introducing it cold at CH4

### U02 · before skincare found it
- t073 **S** VO: Before skincare marketing found it, ectoin belonged to a bacterium in extremely salty water.
  SCREEN: crystal field assembles on dark water; `Halomonas elongata`
- t002 **J** VO: Bacteria invented skincare?
- t003 **S** VO: Not intentionally.
- t074 **S** VO: The salt pulls water out of the cell, turning it into a microscopic raisin. Ectoin helps keep the machinery stable.
  SCREEN: cell deforms, `RAISIN`, ectoin appears inside and the cell recovers
- t075 **S** VO: Skincare borrowed the molecule. Marketing borrowed the drama.
  SCREEN: `SKINCARE BORROWED THE MOLECULE` transforms into `MARKETING BORROWED THE DRAMA`

## CH2 — Give the protein some space (compressed hardest: 9 turns/97w → 5 turns/65w)

### S07 · extremolytes
- t016 **S** VO: Ectoin belongs to a group of protective molecules sometimes called extremolytes.
  SCREEN: term card — `EXTREMOLYTE` / *noun* / `a molecule that keeps a cell stable in conditions that should destroy it`
  **NOTE:** do not cut this gloss. It is the one technical term JAY never translates, by design — the definition card does the translating instead.

### S08 · preferential exclusion, hedged in the same breath — JARGON ALARM 2 (fire)
- t017 **S** VO: Its effects involve how water arranges around proteins. Scientists call part of it preferential exclusion, though the real picture is messier.
  SCREEN: `PREFERENTIAL EXCLUSION` · cite `Phys Chem Chem Phys · 2018` · the hedge ("messier") types in smaller, second line — carries what was t022's standalone hedge, folded in rather than given its own turn
- t018 **J** VO: Even the alarm wants you to stop.

### S09 · the celebrity — MERGED this revision (was t019 + t020, two turns)
- t078 **S** VO: Picture a protein as a celebrity with security. Ectoin may help that water stay organised without touching the protein directly.
  SCREEN: protein + shell actor, label `PROTEIN`, ring rearranges through the sentence rather than cutting

### S10 · personal space
- t021 **J** VO: So ectoin gives proteins personal space.
  SCREEN: `PREFERENTIAL EXCLUSION` **transforms into** `GIVE THE PROTEIN SOME SPACE`

**Cut this revision: the "event coordinator" gag (`t023`/`t024`).** Two
turns, one joke, no new information — the celebrity analogy already lands
the idea and `t021` already lands the punchline. Cutting the follow-on gag
was the single largest per-beat saving in the compression pass.

## CH3 — What this means for skin

### S12 · lab research
- t025 **S** VO: Laboratory research suggests ectoin may help stabilise structures and change how keratin in the outer skin layer interacts with water.
  SCREEN: `KERATIN` + water — *(JAY's hand enters frame toward the alarm — the "reach, no fire" beat)*

### S13 · dry or stressed skin
- t026 **S** VO: It may help dry or stressed skin cope more comfortably.

**Cut this revision: the "translating yourself" exchange (`t027`/`t028`).**
A character beat, not a claim or a gag load-bearing elsewhere; cut for
length in the skin section per the brief's compression order.

### S14 · no force field
- t029 **J** VO: Does ectoin create an invisible protective force field around my face?
  SCREEN: `FORCE FIELD?`
- t030 **S** VO: No. Not at all.
  SCREEN: `FORCE FIELD?` → struck through — **VO padded, SCREEN stays plain
  "No."** The prior revision's `DELIVERY.md` documents the bare "No." take as
  pure silence (this engine needs more than one syllable to decay into) and
  names this exact fix as an accepted option.
- t031 **J** VO: Finally, a skincare ingredient with realistic boundaries.

### S15 · support, not armour
- t032 **S** VO: Think of ectoin as support for the skin barrier, not body armour.
  SCREEN: `SUPPORT` / not `ARMOUR`

## CH4 — Does it work on people?

### S16 · the 104
- t033 **S** VO: In one study, 104 women compared a cream containing 2 percent ectoin with the same cream without it.
  SCREEN: count-up `104` · 104-dot cohort grid · cite `Skin Pharmacol Physiol · 2007`
- t034 **S** VO: The women preferred the ectoin version.
  SCREEN: `PREFERRED`

### S17 · preference is not proof
- t035 **J** VO: So it worked?
- t036 **S** VO: They liked it better. That is real, but not the same as a machine proving their skin changed.
  SCREEN: `LIKED IT BETTER` ≠ `MEASURED CHANGE`

**Cut this revision: `t037` ("Preference, not Cinderella").** The joke was
extra to the point `t036` already makes; kept `t035`→`t036` as a real Q&A
rather than gutting the exchange to a single unanswered line.

### S18 · the eczema trial
- t038 **S** VO: Another study followed 65 people with mild to moderate eczema. Over four weeks the ectoin cream matched the comparison and was well tolerated.
  SCREEN: `65` · `4 WEEKS` · two bars level · cite `Skin Pharmacol Physiol · 2013`

### S19 · promising, not a miracle
- t039 **J** VO: Promising?
- t040 **S** VO: Yes.
- t041 **J** VO: Miracle?
- t042 **S** VO: No.

### S20 · what it does not prove — MERGED this revision (was t043 + t044)
- t079 **S** VO: It does not prove ectoin cures eczema or replaces treatment. The evidence is limited, and some research comes from companies that sell it.
  SCREEN: two claims struck — `CURES ECZEMA` `REPLACES TREATMENT` (dropped "reverses ageing" as a third struck claim — ectoin was never claimed to address ageing in this script, so striking it read as a straw man) — then `bitop AG` / `Kao Corporation` shown as plain author-affiliation content, never a pill (see `CLAIMS.md` C4, C6 — the industry connection is now verified stronger than the prior brief recorded)

### S21 · twelve
- t046 **S** VO: A PubMed search found twelve clinical trials.
  SCREEN: `12` count-up · 12 tiles · cite `PubMed · 2026`
- t047 **J** VO: Twelve? My group chat has produced more research on whether someone should text their ex.

**Cut this revision: `t045` ("How limited?") and `t048` ("None of it passed
peer review.").** `t045` was a cheap bridging question `t046` doesn't need to
be prompted into; `t046` now follows `t079` directly. `t048` is **removed
outright** — see §Changes above, point 1, and `CLAIMS.md` §Removed. This is
the one change in this revision that is not a length cut: it is a
correction of a knowingly false line.

## CH5 — How to read the bottle

### S22 · who it is for — MERGED this revision (was t049 + t050)
- t080 **S** VO: Ectoin suits dry, sensitive or irritated skin, and pairs with panthenol, glycerin, squalane and ceramides.
  SCREEN: four states, four pills — same visual payload as the two-turn version, now landing on one clip

**S23/S24 retired (prior revision).** t051-t054 ("So I buy the bottle with
the largest percentage?" / "No. Turn the bottle around." / the blend
explanation / "a group project where ectoin only completed one slide.") were
cut when that reveal moved to open the video at U01. The bottle here is the
SAME one from the open, already turned.

### S25 · read the list
- t055 **S** VO: Exactly. Check the actual percentage when it is disclosed, read the ingredient list and judge the complete formula.
  SCREEN: INCI list, ectoin's real position
- t056 **J** VO: One fashionable ingredient cannot rescue a badly built product.
- t057 **S** VO: You may deactivate the Jargon Alarm now.
  SCREEN: alarm powers down — the running gag closes (JARGON ALARM retire)

### S26 · did K-beauty invent it — MERGED this revision (was t058 + t059)
- t082 **S** VO: K-beauty did not invent ectoin. Bacteria developed the survival strategy. Korean formulators pair it with barrier ingredients in light textures.
  SCREEN: `K-BEAUTY` struck, `BACTERIA` stands
- t060 **J** VO: So bacteria invented it, and Korea gave it better packaging.

**Cut this revision: `t061` ("Aggressively simplified, but acceptable.").**
Extra beat after the joke already lands on `t060`; cut for length.

## CH6 — The honest verdict

### S27 · not the new hyaluronic acid
- t062 **S** VO: Ectoin is not the new hyaluronic acid, not a miracle, and the evidence does not support dramatic promises.
  SCREEN: `NOT A MIRACLE`

### S28 · what it is
- t063 **S** VO: It is a genuinely interesting supporting ingredient that may help dry or stressed skin.
  SCREEN: `A GENUINELY INTERESTING SUPPORTING INGREDIENT` — **wrap in an element, never a bare text node under the wash**
- t064 **J** VO: Supporting actor, not superhero.

### S29 · the action
- t065 **S** VO: Exactly. Look for the actual percentage, then judge the whole formula.
  SCREEN: the closing action, lesson-tied — `FIND THE REAL PERCENTAGE` / `THEN JUDGE THE WHOLE FORMULA`

### S30 · the dignity ship — MERGED this revision (was t066 + t067 + t068 + t069, four turns)
- t081 **J** VO: And would I put a bacteria-made survival molecule on my face? I already bought snail mucus. The dignity ship sailed years ago.
  SCREEN: none — the joke carries itself

**Compression note:** the prior four-turn version had SOULHABIT bounce the
question back ("Would you?") before JAY answered it. That interjection is
cut here — the joke and its rhythm survive as one JAY turn, but the specific
S/J volley does not. Logged as a deliberate trade for length, not an
oversight.

### S31 · end screen
- t070 **J** VO: What questionable skincare ingredient are we investigating next?
  SCREEN: end-screen scene. Right third and lower-right kept clear for YouTube's
  own overlays. Motion calmed. Camera returns to the CH1 framing — the piece
  bookends.
