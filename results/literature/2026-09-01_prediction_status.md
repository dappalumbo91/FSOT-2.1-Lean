# Prediction cross-reference — 2026-09-01

**Predictions frozen in** `predictions/` (pin **D1D38A**). This file is a **result pack**. It does not change any predicted central.

Machine twin: [`2026-09-01_prediction_status.json`](2026-09-01_prediction_status.json)  
Dated scores: [`../dated_forecast_scores/REPORT.md`](../dated_forecast_scores/REPORT.md)

## 1. Dated fluid windows (PRED-064)

Scored against USGS / NDBC / SWPC / CO-OPS. Issued JSON not rewritten.

| Issue | Hold | Kill | Awaiting |
|-------|-----:|-----:|---------:|
| 2026-08-25 | 7 | 7 | 1 (volcanic → 2026-09-08) |
| T012157 | 7 | 3 | 10 (EQ still open until ~01:21Z) |
| T022247 | 7 | 2 | 19 (EQ/hydro until ~02:22Z) |
| 2026-08-31 | 0 | 0 | 26 (EQ/hydro ~2026-09-07) |
| **All** | **21** | **12** | **56** |

### What hit

- **Weather storms (Arctic):** all five first-issue storm cells **hold** (RDDA2, WRXA2, UQXA2, KOZA2, DHXA2).
- **Solar quiet:** Kp_max **1.67** < 5 on all three closed solar windows — **hold**.
- **Tides (window-clipped):** SF/Boston/LA/Key West scored on hours *inside* `valid_to`. The 2.413 m SF spike was **after** the 48 h window (scorer bug, now clipped). Inside-window SF max residual **0.145 m**.
- **Earthquakes:** Ende, Indonesia **M5 at 17.9 km** — **hold** (`FCAST-EQ-20260825-01`).

### What missed (and the refine)

First-issue EQ: **1 hold / 7 kill**. Every cell had `expect_event=True`.

| Cell | Valve at issue | Expect M≥5? | Outcome |
|------|----------------|:-----------:|---------|
| Ende | released | yes | **hold** (M5) |
| Pematangsiantar | steady | yes | kill |
| Aniso, Peru | released | yes | kill |
| Timor Leste | **loading** | yes | kill |
| Scotia Sea | **loading** | yes | kill |
| Vanuatu | steady | yes | kill |
| Honchō, Japan | **loading** | yes | kill |
| South Sandwich | steady | yes | kill |

Loading cells were not empty: **Timor M 4.8 at 3.4 km** (26 Aug) and **Honchō M 4.5 at 28.9 km** (30 Aug). The bar was M≥5 — short 0.2 and 0.5 mag. Released/steady cells had **no M≥4** in-kernel (quiet after the prior 6.x). Full autopsy: [`../dated_forecast_scores/KILL_AUTOPSY.md`](../dated_forecast_scores/KILL_AUTOPSY.md).

Guaranteed M≥5 is too strong. Next issues (after 2026-08-31, which is already frozen):

1. `expect_event` only on `loading_suction` / `post_poof_aftershock` (already in `vendor/fsot_earth_fluid_forecast.py`).
2. Score **elevated rate vs prior half-window**, not a promised M≥5. Loading = SUCTION; a POOF is not owed on a 7-day clock.

Quiet-weather: OLCN6/42058 kills stay on the issued kill_if. New issues skip the 1000–1005 hPa / 12–15 m/s gap.

## 2. Hand PREDs vs live data (no new papers invented)

Literature pack [`2026-08-17_crossref.md`](2026-08-17_crossref.md) still stands. In-repo panels checked 2026-08-31:

| PRED | Lock | Live check | Verdict |
|------|------|------------|---------|
| PRED-001 H0 bridge | 70.75 | CCHP 70.39 / SH0ES~73 / Planck 67.4 | **hold** (between) |
| PRED-002 / 042 S8 | 0.805 | Euclid DR1 12 Nov 2026 | **awaiting** |
| PRED-043 wₐ | −1.018 | DES+DESI not 3σ exclusion | **hold** |
| PRED-004 / 050 g−2 | +2.49e-9 | Fermilab high; lattice split | **partial** |
| PRED-049 m_H | 125.25 GeV | CMS γγ 125.14 (0.088%) | **hold** |
| PRED-048 / 067 GW | ≤0.5% | GWTC panel **0.0085%**; compact-object **0.010%** | **local_green_hold** |
| PRED-052 FRB DM class | 200 pc cm⁻³ | class freeze; 10-row density residual ~66% not stuffed | **hold** class / **not** 0.5% density |
| PRED-054 / 063 climate | ≤0.5% | NCEI/NDBC panels green | **local_green_hold** |
| PRED-056 b-value | 1.0 | literature band 0.90–1.10 | **preregistered** |
| PRED-058 volcano residual | ≤0.5% | GVP panel 0.0235% | **local_green_hold** |
| PRED-059 / 062 solar sectors | classifiers | Kp quiet hold on dated windows | **hold** (quiet sector) |
| PRED-065 tides residual | ≤0.5% | 20-station **0.030%** | **local_green_hold** |
| PRED-066 exo architecture | ≤0.5% | architecture panel green | **local_green_hold** |
| PRED-068 GBIF | ≤0.5% | 240 rec **0.006%** | **local_green_hold** |
| PRED-069 epidemiology | ≤0.5% | 24 rec **0.015%** | **local_green_hold** |
| PRED-070–075 CKM/PMNS/α_s | PDG 0.5% | flavor layer inside tight band | **local_green_hold** |
| PRED-077 siren H0 | 70.024 | no new public siren central | **awaiting** O4/O5 |
| PRED-017 Z119 | viability | no confirmed atom | **awaiting** |
| PRED-064 dated windows | scored | issued + scored; EQ rule too eager | **partial** (process hold; EQ refine) |

**Survey kills this window: 0.** Euclid / Rubin / PDG combo / Z119 still future.

## 3. Direction to refine (not free parameters)

1. **Earthquakes** — rate in the cell vs prior half-window; M≥5 is a class floor for *loading* only, not a promise on every cluster.
2. **Tides** — always clip to `valid_to`; surge only when residual is clearly above POOF (0.145 m inside window vs 0.157 snapshot).
3. **Weather** — do not issue doomed quiet; skip short Great Lakes realtime buffers.
4. **Cryosphere** — still not a mass PRED (classifier 0% stays classifier).

## How to append the next paper

```powershell
python scripts/record_prediction_outcome.py --pred-id PRED-001 --survey "Paper-label" --result hold --measured 70.39 --unit km/s/Mpc --source https://... --notes "one sentence"
```
