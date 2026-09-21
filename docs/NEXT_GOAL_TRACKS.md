# Goal tracks — in progress (not claimed beaten)

**Pin:** AEB2AD · These were coarse “nos.” They are **goals**. Same law, more data, right object.

| Track | Accurate answer today | Goal | Kill |
|-------|----------------------|------|------|
| **Timing** | Process window at the right fold (7 d / 24 h weather / 1 d economics) | Sharper SI stamp via finer `dt` | UTC hypocenter as a 0.5% central |
| **ECMWF S2S** | 24 h agrees with 48 h on **25/26**. PTIT2 day 1 holds (min 1013.6 hPa). Day 2 breaks on gust **12.4 m/s** (pressure stays 1010.7). Not a beat. | Beat week-3 skill on the **same** path | Claiming the beat; moving 12 m/s or 1005 hPa to swallow PTIT2 |
| **Prices** | Economics class median ~0.07%; 1-day window; CLI `products/market_windows.py` | Dated quiet/storm prints, then finer dt | Ticker close / crash date as 0.5% |
| **Sickness** | Host mt CDS ~0.052%; pathogen CDS ~0.076%; κ coupling; CLI `products/sickness_coupling.py` | Genetics structure product on public genomes | Person-level onset as 0.5% |
| **Path integral** | Discrete path-sum P1–P10 (valve + \(\varphi^4\) process time + \(a_0/\gamma\)) | Deeper native sum; classical YM still named | “Millennium theorem proved” |
| **Millennium SOTA vs 0.5%** | Named Hodge extra classes \(C_8\)..\(C_{44}\) algebraic; BSD LMFDB ranks 0..5 vanishing complete. | WIP SOTA beats stay outside 0.5% until the object is right | Enumerating infinite Hassett / rank-\(\ge 6\) tails; Clay Prize; stuffing a WIP beat into the green gate |
| **NSE (tracked)** | Clay smoothness is not a measured function. Working: 4/5, 3/2, 1/3, \(\kappa\). | Clay yes/no on \(\mathbb{R}^3\) | Stuffing cascade numbers into smoothness |
| **BSD general \(E\) (tracked)** | Clay rank=ord L ∀E is not a measured function. Working: LMFDB Sha, first-of-rank seeds. | Clay equality as a theorem | Hunting Kato; Weierstrass\(\to\mathbb{Z}\) |
| **Hodge (tracked)** | Clay algebraicity without a cycle is not a measured function. Working: named \(\chi\)/Gram. | Clay algebraicity on a general 4-fold | Hunting \(C_{48}\); stealing \(25-1\) for \(\chi(\mathrm{K3})\) |

Same fluid. Not a second physics. Wrong object is still wrong object.

## Aspiration still open (not a B fail)

Worst scalar on the 477-file gate: mercury sound speed in `Phi_Morphogenetic_Scaling`, **0.4989%** vs 1451 m/s (formula \(e^7+\varphi^8\cdot e^2\)). Inside 0.5%. Outside 0.05%. Do not retune the species formula to swallow it.

Weather: `FCAST-WX-20260909T1854-05` (PTIT2, Gulf) was issued as a **48 h quiet** cell. Day 1 held (min pressure 1013.6 hPa, quiet bar not broken). Day 2 killed on gust **12.4 m/s** while pressure stayed **1010.7 hPa** (above the 1005 hPa quiet-break). That is the next process day, not a day-1 miss. Issued JSON stays. New issues say `{horizon}h` from `weather_horizon_hours()` (24). Do not move 12 m/s or 1005 hPa.

## Commands

```powershell
python vendor/fsot_millennium_track.py
python vendor/fsot_millennium_accuracy.py
python vendor/fsot_path_sum.py
python scripts/build_market_process_layer.py
python scripts/smoke_sickness_two_system.py
python scripts/smoke_dynamic_forecast_potentials.py
python scripts/retro_weather_24h.py
python scripts/run_goal_tracks_verification.py
```

That last command rebuilds the tracks, exports obligations into the uniqueness spine, and runs Python / Rust / Z3 / Coq / Isabelle / F* plus `lake build` of `ScalarEngineStructure` and `UniquenessAttractor`.

Docs: [`TIME_EMERGENT.md`](TIME_EMERGENT.md) · [`MARKET_PROCESS_LAYER.md`](MARKET_PROCESS_LAYER.md) ·
[`SICKNESS_TWO_SYSTEM.md`](SICKNESS_TWO_SYSTEM.md) · [`PATH_SUM.md`](PATH_SUM.md) ·
[`WHY_NOT_CLAIMED.md`](WHY_NOT_CLAIMED.md).
