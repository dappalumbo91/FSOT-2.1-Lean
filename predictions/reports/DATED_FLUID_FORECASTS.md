# Dated fluid-pressure forecasts (this issue)

*Issued 2026-09-09T18:54:26+00:00 · pin D1D38A · kernel **39.1 km** · EQ window **7 d***

Pressure loads (SUCTION). The orifice opens (POOF). Location = catalog pressure cell.
Date = calendar window. Score with `python scripts/score_earth_fluid_forecasts.py`.

USGS events used: **236**. Volcanic-type: **0**. NDBC stations: **891**. SWPC Kp samples: **358**. CO-OPS stations: **8**. NWIS gages: **8**.

Prior frozen issues stay on disk (do not rewrite). This file is the current issue.

| ID | Kind | Where | Window | Call | Valve |
|----|------|-------|--------|------|-------|
| `FCAST-EQ-20260909T1854-01` | earthquake | 84 km SSW of Nikolski, Alaska (52.2074,-169.3692) r=39.1 km | 2026-09-09 → 2026-09-16 | no M≥5.0 | released |
| `FCAST-EQ-20260909T1854-02` | earthquake | South Sandwich Islands region (-56.2002,-27.9015) r=39.1 km | 2026-09-09 → 2026-09-16 | no M≥5.0 | released |
| `FCAST-EQ-20260909T1854-03` | earthquake | 145 km N of Caluula, Somalia (13.2654,50.5425) r=39.1 km | 2026-09-09 → 2026-09-16 | no M≥5.0 | steady |
| `FCAST-EQ-20260909T1854-04` | earthquake | 96 km ESE of Isangel, Vanuatu (-19.8039,170.0929) r=39.1 km | 2026-09-09 → 2026-09-16 | no M≥5.0 | steady |
| `FCAST-EQ-20260909T1854-05` | earthquake | Kermadec Islands, New Zealand (-30.1462,-177.8882) r=39.1 km | 2026-09-09 → 2026-09-16 | no M≥5.0 | steady |
| `FCAST-EQ-20260909T1854-06` | earthquake | southern East Pacific Rise (-34.9815,-109.0259) r=39.1 km | 2026-09-09 → 2026-09-16 | no M≥5.0 | steady |
| `FCAST-EQ-20260909T1854-07` | earthquake | 93 km SE of Kirakira, Solomon Islands (-11.0595,162.519) r=39.1 km | 2026-09-09 → 2026-09-16 | no M≥5.0 | released |
| `FCAST-EQ-20260909T1854-08` | earthquake | 71 km WSW of Puerto Madero, Mexico (14.3122,-93.0746) r=39.1 km | 2026-09-09 → 2026-09-16 | no M≥5.0 | released |
| `FCAST-WX-20260909T1854-01` | weather | NDBC 62442 (atlantic) (49.0,-16.5) r=50.0 km | 2026-09-09 → 2026-09-11 | storm_sector / atlantic | loading_suction |
| `FCAST-WX-20260909T1854-02` | weather | NDBC 46070 (pacific) (55.048,175.246) r=50.0 km | 2026-09-09 → 2026-09-11 | storm_sector / pacific | loading_suction |
| `FCAST-WX-20260909T1854-03` | weather | NDBC 64046 (arctic) (60.483,-4.167) r=50.0 km | 2026-09-09 → 2026-09-11 | quiet_sector / arctic | steady |
| `FCAST-WX-20260909T1854-04` | weather | NDBC 51002 (tropics) (17.07,-157.755) r=50.0 km | 2026-09-09 → 2026-09-11 | quiet_sector / tropics | steady |
| `FCAST-WX-20260909T1854-05` | weather | NDBC PTIT2 (gulf) (26.061,-97.215) r=50.0 km | 2026-09-09 → 2026-09-11 | quiet_sector / gulf | steady |
| `FCAST-SOL-20260909T1854-01` | solar | Earth magnetosphere (planetary Kp) (0.0,0.0) r=6371.0 km | 2026-09-09 → 2026-09-12 | Kp stays <5 | steady |
| `FCAST-TIDE-20260909T1854-01` | tide | NOAA San Francisco (9414290) (37.8063,-122.4659) r=39.1 km | 2026-09-09 → 2026-09-11 | surge ≥0.1535 m | loading_suction |
| `FCAST-TIDE-20260909T1854-02` | tide | NOAA Boston (8443970) (42.3534,-71.0534) r=39.1 km | 2026-09-09 → 2026-09-11 | surge ≥0.1535 m | loading_suction |
| `FCAST-TIDE-20260909T1854-03` | tide | NOAA Los Angeles (9410170) (33.72,-118.2722) r=39.1 km | 2026-09-09 → 2026-09-11 | surge ≥0.1535 m | loading_suction |
| `FCAST-TIDE-20260909T1854-04` | tide | NOAA Key West (8724580) (24.5508,-81.8081) r=39.1 km | 2026-09-09 → 2026-09-11 | residual <0.1535 m | steady |
| `FCAST-HYDRO-20260909T1854-01` | hydrology | USGS 01646500 Potomac River near Washington DC (38.95,-77.13) r=39.1 km | 2026-09-09 → 2026-09-16 | quiet_flow | released |
| `FCAST-HYDRO-20260909T1854-02` | hydrology | USGS 05464500 Cedar River at Cedar Rapids IA (41.97,-91.67) r=39.1 km | 2026-09-09 → 2026-09-16 | quiet_flow | released |
| `FCAST-HYDRO-20260909T1854-03` | hydrology | USGS 08114000 Brazos River at Richmond TX (29.58,-95.76) r=39.1 km | 2026-09-09 → 2026-09-16 | high_flow | loading_suction |
| `FCAST-HYDRO-20260909T1854-04` | hydrology | USGS 09380000 Colorado River at Lees Ferry AZ (36.86,-111.59) r=39.1 km | 2026-09-09 → 2026-09-16 | quiet_flow | steady |
| `FCAST-HYDRO-20260909T1854-05` | hydrology | USGS 06934500 Missouri River at Hermann MO (38.71,-91.43) r=39.1 km | 2026-09-09 → 2026-09-16 | quiet_flow | released |
| `FCAST-HYDRO-20260909T1854-06` | hydrology | USGS 14144700 Columbia River at Vancouver WA (45.62,-122.67) r=39.1 km | 2026-09-09 → 2026-09-16 | quiet_flow | released |
| `FCAST-HYDRO-20260909T1854-07` | hydrology | USGS 023177483 Withlacoochee River at Skipper Bridge GA (30.85,-83.28) r=39.1 km | 2026-09-09 → 2026-09-16 | quiet_flow | steady |
| `FCAST-HYDRO-20260909T1854-08` | hydrology | USGS 03072655 Monongahela River near Masontown PA (39.84,-79.88) r=39.1 km | 2026-09-09 → 2026-09-16 | high_flow | loading_suction |

This issue JSON: `predictions/dated_forecasts/2026-09-09_issue.json`
Pointer: `predictions/dated_forecasts/LATEST.json`

Frozen issue files (never rewrite): `2026-08-25T012157_issue.json`, `2026-08-25T022247_issue.json`, `2026-08-25_issue.json`, `2026-08-31_issue.json`, `2026-09-01_issue.json`, `2026-09-09_issue.json`

These are **not** USGS/NWS watches. They are FSOT valve cells so we can iron out hit/miss.

Scores: `results/dated_forecast_scores/REPORT.md` (never rewrite this issue JSON).
