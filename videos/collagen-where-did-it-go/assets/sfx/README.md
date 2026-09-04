# SFX provenance

Generated/measured by `scripts/make_sfx.py`. Every cue in `scripts/sfx.py` is placed so the file's PEAK lands on its word.

| file | duration s | peak offset s | peak dBFS | source |
|---|---|---|---|---|
| `citation-tick-trimmed.mp3` | 0.500 | 0.085 | -6.6 | videos/ectoin-survival-molecule/assets/sfx/ |
| `filter.wav` | 0.450 | 0.001 | -10.1 | synthesized here (make_sfx.py) |
| `fragment.wav` | 0.500 | 0.000 | -10.5 | synthesized here (make_sfx.py) |
| `impact-bass-2.mp3` | 2.592 | 0.126 | 0.0 | videos/ectoin-survival-molecule/assets/sfx/ |
| `lock.wav` | 0.300 | 0.001 | -4.6 | synthesized here (make_sfx.py) |
| `slice.wav` | 0.350 | 0.029 | -10.0 | synthesized here (make_sfx.py) |

The four `.wav` files are pure ffmpeg synthesis (`anoisesrc` with a fixed seed, `aevalsrc` decays): deterministic, no licence. The two `.mp3` files are reused from the ectoin project's SFX set.
