# Dated fluid-pressure forecasts (this issue)

*Issued 2026-09-01T00:32:44+00:00 · pin D1D38A · kernel **39.1 km** · EQ window **7 d***

Pressure loads (SUCTION). The orifice opens (POOF). Location = catalog pressure cell.
Date = calendar window. Score with `python scripts/score_earth_fluid_forecasts.py`.

USGS events used: **272**. Volcanic-type: **0**. NDBC stations: **837**. SWPC Kp samples: **358**. CO-OPS stations: **8**. NWIS gages: **8**.

Prior frozen issues stay on disk (do not rewrite). This file is the current issue.

| ID | Kind | Where | Window | Call | Valve |
|----|------|-------|--------|------|-------|
| `FCAST-EQ-20260901T0032-01` | earthquake | 31 km NW of Aniso, Peru (-14.6414,-73.5236) r=39.1 km | 2026-09-01 → 2026-09-08 | no M≥5.0 | steady |
| `FCAST-EQ-20260901T0032-02` | earthquake | 29 km NNE of Ruteng, Indonesia (-8.2718,120.5607) r=39.1 km | 2026-09-01 → 2026-09-08 | M≥4.5 count≥1 | loading_suction |
| `FCAST-EQ-20260901T0032-03` | earthquake | Scotia Sea (-60.3515,-47.5217) r=39.1 km | 2026-09-01 → 2026-09-08 | no M≥5.0 | steady |
| `FCAST-EQ-20260901T0032-04` | earthquake | 215 km NNE of Lospalos, Timor Leste (-6.6317,127.4711) r=39.1 km | 2026-09-01 → 2026-09-08 | no M≥5.0 | released |
| `FCAST-EQ-20260901T0032-05` | earthquake | 32 km SSW of Honchō, Japan (41.8646,142.7993) r=39.1 km | 2026-09-01 → 2026-09-08 | M≥4.5 count≥1 | loading_suction |
| `FCAST-EQ-20260901T0032-06` | earthquake | 145 km N of Caluula, Somalia (13.2654,50.5425) r=39.1 km | 2026-09-01 → 2026-09-08 | no M≥5.0 | released |
| `FCAST-EQ-20260901T0032-07` | earthquake | 4 km N of Toride, Japan (35.9375,140.0778) r=39.1 km | 2026-09-01 → 2026-09-08 | no M≥5.0 | steady |
| `FCAST-EQ-20260901T0032-08` | earthquake | Kermadec Islands, New Zealand (-30.1462,-177.8882) r=39.1 km | 2026-09-01 → 2026-09-08 | M≥4.5 count≥1 | loading_suction |
| `FCAST-WX-20260901T0032-01` | weather | NDBC MDXA2 (pacific) (59.438,-146.327) r=50.0 km | 2026-09-01 → 2026-09-03 | storm_sector / pacific | loading_suction |
| `FCAST-WX-20260901T0032-02` | weather | NDBC PPXA2 (arctic) (60.801,-148.357) r=50.0 km | 2026-09-01 → 2026-09-03 | storm_sector / arctic | loading_suction |
| `FCAST-WX-20260901T0032-03` | weather | NDBC 42013 (gulf) (27.173,-82.924) r=50.0 km | 2026-09-01 → 2026-09-03 | storm_sector / gulf | loading_suction |
| `FCAST-WX-20260901T0032-04` | weather | NDBC APRP7 (tropics) (13.444,144.657) r=50.0 km | 2026-09-01 → 2026-09-03 | quiet_sector / tropics | steady |
| `FCAST-WX-20260901T0032-05` | weather | NDBC 62146 (atlantic) (57.2,2.1) r=50.0 km | 2026-09-01 → 2026-09-03 | quiet_sector / atlantic | steady |
| `FCAST-TIDE-20260901T0032-01` | tide | NOAA San Francisco (9414290) (37.8063,-122.4659) r=39.1 km | 2026-09-01 → 2026-09-03 | surge ≥0.1535 m | loading_suction |
| `FCAST-TIDE-20260901T0032-02` | tide | NOAA Los Angeles (9410170) (33.72,-118.2722) r=39.1 km | 2026-09-01 → 2026-09-03 | surge ≥0.1535 m | loading_suction |
| `FCAST-TIDE-20260901T0032-03` | tide | NOAA Galveston (8771341) (29.31,-94.7933) r=39.1 km | 2026-09-01 → 2026-09-03 | surge ≥0.1535 m | loading_suction |
| `FCAST-TIDE-20260901T0032-04` | tide | NOAA Boston (8443970) (42.3534,-71.0534) r=39.1 km | 2026-09-01 → 2026-09-03 | residual <0.1535 m | steady |
| `FCAST-HYDRO-20260901T0032-01` | hydrology | USGS 01646500 Potomac River near Washington DC (38.95,-77.13) r=39.1 km | 2026-09-01 → 2026-09-08 | high_flow | loading_suction |
| `FCAST-HYDRO-20260901T0032-02` | hydrology | USGS 05420500 Cedar River at Cedar Rapids IA (41.97,-91.67) r=39.1 km | 2026-09-01 → 2026-09-08 | quiet_flow | steady |
| `FCAST-HYDRO-20260901T0032-03` | hydrology | USGS 08013000 Brazos River near Houston TX (29.77,-95.59) r=39.1 km | 2026-09-01 → 2026-09-08 | quiet_flow | steady |
| `FCAST-HYDRO-20260901T0032-04` | hydrology | USGS 09402500 Colorado River at Lees Ferry AZ (36.86,-111.59) r=39.1 km | 2026-09-01 → 2026-09-08 | quiet_flow | steady |
| `FCAST-HYDRO-20260901T0032-05` | hydrology | USGS 06803510 Missouri River at Hermann MO (38.71,-91.43) r=39.1 km | 2026-09-01 → 2026-09-08 | quiet_flow | released |
| `FCAST-HYDRO-20260901T0032-06` | hydrology | USGS 14246900 Columbia River at Vancouver WA (45.63,-122.69) r=39.1 km | 2026-09-01 → 2026-09-08 | quiet_flow | steady |
| `FCAST-HYDRO-20260901T0032-07` | hydrology | USGS 023177483 Withlacoochee River at Skipper Bridge GA (30.85,-83.28) r=39.1 km | 2026-09-01 → 2026-09-08 | high_flow | loading_suction |
| `FCAST-HYDRO-20260901T0032-08` | hydrology | USGS 03072655 Monongahela River near Masontown PA (39.84,-79.88) r=39.1 km | 2026-09-01 → 2026-09-08 | quiet_flow | released |

This issue JSON: `predictions/dated_forecasts/2026-09-01_issue.json`
Pointer: `predictions/dated_forecasts/LATEST.json`

Frozen issue files (never rewrite): `2026-08-25T012157_issue.json`, `2026-08-25T022247_issue.json`, `2026-08-25_issue.json`, `2026-08-31_issue.json`, `2026-09-01_issue.json`

These are **not** USGS/NWS watches. They are FSOT valve cells so we can iron out hit/miss.

EQ rule this issue: expect M≥4.5 only on loading/post-POOF; released/steady hold if no M≥5. Scores: `results/dated_forecast_scores/REPORT.md`.

Scores: `results/dated_forecast_scores/REPORT.md` (never rewrite this issue JSON).
