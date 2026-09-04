# Asset specs — snail-mucin-medical-secret-v2

Written before any generation call, per `[S6/A-1]`. Photoreal is used **only** for tactile /
process / application beats (chapters 1, 5, 6, and the chapter-7 callback); chapters 2, 3, 4 and 7's
verdict are browser-drawn so realism cannot masquerade as proof (`CLAIM-LEDGER.md` governs this,
not asset convenience).

## Shared art direction (all photoreal shots)

- **Canvas:** portrait 9:16 master, ≥2160×3840, with a **10% bleed** on every edge so the
  1080×1920 crop has headroom — v1's plates were delivered at exactly 1152×2048 with **zero** crop
  headroom, which forced every punch-in to stay under a ~4% zoom. This time the source is
  generated to leave room.
- **Safe framing:** keep the central 60% clear for the eventual 1080×1920 crop; leave a clean lower
  region for the caption band, which in this project sits at **y 1300–1520 on the final canvas**,
  i.e. roughly the bottom 22–39% of frame — nothing load-bearing there.
- **Register:** editorial documentary realism, not glossy advertising. Natural pores, imperfect
  surfaces, realistic microbubbles, physically plausible reflections, believable depth of field.
- **Palette:** dark forest-green ground with warm amber accents and cream highlights (this
  project's existing tokens: `--green-deep #0f2016`, `--pink #b9835a`, `--cream #fbfaf4`) — but
  shadow detail and natural skin colour must be preserved, never crushed or over-graded.
- **Negative constraints (every shot):** no embedded text, logos, brand labels, watermarks, fake
  charts, fake medical documents; no plastic skin, excessive smoothing, malformed hands, duplicated
  fingers, extra tentacles, distorted shells, impossible liquid geometry, unreadable packaging,
  oversaturation, haloed cutouts, or generic beauty-ad glow.
- **Process:** two candidates per shot, contact-sheeted at phone-frame size before adoption. Clean
  plates without captions; a depth/subject-isolated variant where parallax is planned.

## Shot list

### S1 — Tactile hook (chapter 1, new plate)
100mm macro of translucent secretion-like gel stretching between a glass spatula and lab glass.
Real microbubbles, side-lit amber rim light, deep green-black ground, sharp focal plane on the
strands, no product branding. *Reuse candidate:* v1's `01b-macro-slime-spatula.png` may already
satisfy this — generate one alternative candidate only if the reused plate's crop headroom proves
insufficient for the planned object-tracked push.

### S2 — Medical-history reenactment (chapter 1, new plate)
Archival-style laboratory still, clearly a **reenactment** (never claimed as documentary), period
Spanish-radiotherapy-adjacent props, no identifiable patient, no fabricated record. *Reuse:* v1's
`01a-archival-lab.png` is already grayscale-graded for exactly this use — reuse as-is.

### S3 — Extraction reality (chapter 5, new plate)
Documentary macro of a healthy garden snail on clean mesh in a dim, humid setting. Anatomically
correct shell and two pairs of tentacles, visible natural trail, no distress signalling. **The
narration explicitly states methods vary and welfare is a company claim, not an independent
finding (`CLAIM-LEDGER.md` C12) — the image must not be composed to imply the opposite.** *Reuse:*
v1's `04-snail-mesh.png`.

### S4 — Application (chapter 6, new plate needed)
Close macro of an adult cheek, visible natural pores, thin serum layer patted in by a realistic
hand, soft window light, no retouching, no exaggerated "glass skin" gloss. Two variants: damp-skin
and moisturizer-seal, for the chapter's controlled-progression beat. **No plate in this repo covers
this specifically** — `02-routine-montage.png` is a routine-hands wide shot, not a macro cheek
application; generate new.

### S5 — Closing callback (chapter 7, reuse)
Reframe of S1's macro secretion plate at the opposite framing (wide where chapter 1 was tight) —
the actor-continuity payoff named in the composition design. No new generation.

## Provider and budget

Gemini image (`providers.yaml` §image, `gemini-image` or `gemini-image-lite`) for any generated
plate — Higgsfield is the photographic-plate provider by policy but Gemini is used here because it
is the environment-probed-reachable option this session; log the substitution. Estimated: 1 new
plate (S4, two candidates) ≈ $0.07–0.20 at published per-image rates, well inside the $5.00/run cap.
No plate needed for S1–S3, S5 (all reused) unless review at build time finds the reused crop
headroom insufficient.
