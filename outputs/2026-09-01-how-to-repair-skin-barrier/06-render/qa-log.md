# Render QA log

| Gate | Result |
|---|---|
| `[S7/R-1]` `check --json --snapshots` | **ok: true** — lint 0/0, runtime 0/0, layout 0/0, motion 0/0, contrast 0/0. **0 fix cycles.** |
| `[S7/R-1b]` motion sidecar | 44 assertions, 0 errors |
| `[S7/R-2]` safe-area (hard gate) | **PASS** — 181 frames, no ink in reserved zones |
| `[S7/R-2]` static-hold whole-frame | no findings, 91 frames, 2.5 s ceiling |
| `[S7/R-2]` static-hold region-aware | 6 content-voids → **verified false positive** by extraction (centred column, empty by design) |
| `[S7/R-2]` frame zero | composed — the **complete** hook question. A first re-cut split it across two scenes and shipped "IS YOUR SKIN" alone; caught by extraction, not by `check` (which passed 0/0 on it). Fixed. |
| `[S7/R-2]` last frame | application scene; same ground as frame zero (#101314) |
| `[S7/R-2]` Unicode | 병풀 renders correctly, no tofu — Noto Sans KR loaded beside Inter |
| `[S7/R-3]` integrated | **−15.1 LUFS** (target −14; see the ledger's R-3 `[NOT IN SKILL]`) |
| `[S7/R-3]` true peak, shipped file | **−2.2 dBFS** — under −1.0. Headroom rule holds. |
| `[S7/R-3]` duration | video 45.300 s vs VO 45.280 s → Δ 0.020 s, inside ±0.1 s |
| **`[K-4]` rendered-claim check** | **PASS** — 2 unsourced claims flagged concurrently (muted, never accent); 1 **sourced** claim carrying `PMID 35328954` as an accent-toned citation chip from its scene's first frame, visually distinct from the flag; no internal record ids; on-screen hedging ≥ VO at every checked timestamp |

Tool defect found and fixed during this run: `extract_frames.sh` read
`format=duration` (the audio stream on a muxed file) and silently wrote no last
frame. See the ledger.
