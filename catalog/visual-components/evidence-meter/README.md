# EvidenceMeter

"Component 3/5" in the day's in-page numbering. A precision readout for one
ingredient claim's evidence grade — not a loading bar. See
[../../README.md](../../README.md) for the shared design rules (no success
color, deterministic `t`-driven clock, locked to its claim/source) that this
component follows.

- **`evidencemeter-spike.html`** — "Lockup + Design Modes." The primary,
  flat 2D take: hero claim → instrument → source footnote, four confidence
  levels (open/inferred/qualified/known), five color-mode explorations
  (A–E), and a separate "design mode" for present/absent study attributes
  instead of a confidence score. Start here — this is the fullest spec.
- **`evidencemeter-3d-spike.html`** — "Volumetric Monolith." The same
  component re-imagined in Three.js as a 3D object instead of a flat panel.
  Same series slot as the file above — a stylistic alternative, not a
  different component.

Both cite real ingredient source IDs (`ING-GINSENG-S002`, `ING-PDRN-S004`,
etc.) pulled from the actual source tracker, not placeholder text.
