# G0-3b style-core (draft) — editorial B-roll photography

**Status: draft prompt scaffold, zero images generated against it yet.**
Not a catalog entry — `catalog/` holds verified, manifested assets (see
`catalog/product-photography/README.md`'s own verification method); this
is the pre-generation spec, promoted to a real `catalog/*-photography/`
folder with its own `manifest.json` only once beats actually need it and
frames survive `claim_check`/`brand_check`/`face_check`.

Modeled directly on `catalog/product-photography/prompts/style-core.md` —
same three-file structure (`style-core` + per-scene `body` + `negatives`),
same discipline of changing the look once rather than per-scene — but
implementing **G0-3b's ruled palette**, not that folder's paper-white/
celadon/aqua one. The two are deliberately different systems: product-photography
predates G0-3b and is exempt from it as an existing plate (see
`broll-manifest.md` tier 1); anything generated fresh from here on is
new tier-3 generation and G0-3b governs it directly.

This is written now, ahead of T3's beat-level slot list, because the
palette itself isn't gated on beat content — only *which scene bodies* to
write is. Per T3's in-progress `catalog-registry.yaml`
(`editorial_imagery_broll_wrapper` purpose), the wrapper components
(`push-in`, `yt-camera-move`, `device-frame-stage`, `grade-split-reveal`,
`grain-overlay`) carry no content of their own — they wrap whatever plate
this spec eventually produces. So the wrapper choice is T3/T6's job; the
plate's look is T5's, and can be nailed down independently.

## Palette (G0-3b, `wo/FVC-007/GATE0-FVC-007.md`)

- **Pearl-white** — seamless background/primary surface. Not paper-white
  (product-photography's term) and not clinical sterile-white — pearl
  carries a faint warmth product-photography's flatter white doesn't.
- **Soft blush** — bounce/fill light only, not a surface color. Reads as a
  warm pink-toned soft shadow/highlight, never a saturated pink object.
- **Restrained clinical-blue** — rim light or a single small accent detail
  only (per product-photography's own "one accent maximum" discipline,
  carried over here even though G0-3b doesn't say it explicitly — R-13's
  contrast-floor logic and product-photography's precedent both argue for
  capping accent use rather than leaving it open-ended).
- Physically plausible materials, shallow depth of field.
- No lettering, logos, UI, or watermarks baked into the plate — all
  readable information stays in HyperFrames HTML/SVG (R-8).

## Hard exclusions (B-1, carried from product-photography's own pattern)

- **No faces in frame.** A hand may appear only cropped at the wrist or
  forearm — same rule product-photography already enforces, restated here
  since it's B-1's rule, not this folder's invention.
- **No real brand names, logos, wordmarks, or recognizable trade dress.**
  Fictional or unbranded packaging only, same as product-photography.
- **No percentages, durations, efficacy claims, badges, or seals** baked
  into any surface — claim beats never carry B-roll at all (`broll_allowed:
  false` on `claim_vs_evidence` in the registry), but a B-roll plate that
  accidentally renders a stray number or seal is still a liability if it
  ever gets reused off a claim beat later.
- Every generated plate is *content*, not a wrapper — B-1's camera-move
  requirement is the wrapper component's job (`editorial_imagery_broll_wrapper`
  candidates), not something to bake into the image itself as motion blur or
  implied camera movement.

## What this does NOT specify yet

Scene bodies (the per-plate subject matter — what's actually being shown:
a serum droplet, a dermatologist's hands, a texture macro, a lab shot).
Per T5's own manifest, that depends on which beats fall through tiers 1–2
and what they need — T3's caster output. Writing scene bodies against
guessed beat content risks the same waste T0b's programmatic sweep was
built to avoid (generating before knowing what's actually needed). This
file stops at the shared style-core; `scenes.json` (product-photography's
own naming) gets written per-slot once T3/T6 identify them.

## Open question for Gate B / Kim

Product-photography's `style-core.md` bans *all* specular gloss and glow
("no glow, no bloom, no lens flare... explicitly avoid the glossy wet-glass
K-beauty look"). G0-3b's own text doesn't repeat that exclusion, and
"soft blush bounce light" plus "restrained clinical-blue rim" reads as
closer to a lit, dimensional look than product-photography's flat matte
one. Not resolving this by assumption — flagging it as a real difference
between the two specs so whoever reviews this at Gate B can say whether
G0-3b's B-roll is meant to look flatter (matching product-photography, for
visual consistency across the channel's imagery) or is deliberately more
dimensional (per its own "physically plausible materials, shallow depth of
field" language, which reads as allowing real light behavior). Left open
here rather than silently picking one.
