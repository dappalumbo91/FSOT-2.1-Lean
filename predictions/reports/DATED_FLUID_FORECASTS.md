# Dated fluid-pressure forecasts (this issue)

*Issued 2026-08-25T00:06:39+00:00 · pin D1D38A · kernel **39.1 km** · EQ window **7 d***

Pressure loads (SUCTION). The orifice opens (POOF). Location = catalog pressure cell.
Date = calendar window. Score with `python scripts/score_earth_fluid_forecasts.py`.

USGS events used: **299**. NDBC stations: **895**. SWPC Kp samples: **357**.

| ID | Kind | Where | Window | Call | Valve |
|----|------|-------|--------|------|-------|
| `FCAST-EQ-20260825-01` | earthquake | 68 km NNW of Ende, Indonesia (-8.3097,121.3583) r=39.1 km | 2026-08-25 → 2026-09-01 | M≥5.0 count≥1 | released |
| `FCAST-EQ-20260825-02` | earthquake | 9 km WNW of Pematangsiantar, Indonesia (2.9863,98.9853) r=39.1 km | 2026-08-25 → 2026-09-01 | M≥5.0 count≥1 | steady |
| `FCAST-EQ-20260825-03` | earthquake | 31 km NW of Aniso, Peru (-14.6414,-73.5236) r=39.1 km | 2026-08-25 → 2026-09-01 | M≥5.0 count≥1 | released |
| `FCAST-EQ-20260825-04` | earthquake | 215 km NNE of Lospalos, Timor Leste (-6.6323,127.4636) r=39.1 km | 2026-08-25 → 2026-09-01 | M≥5.0 count≥1 | loading_suction |
| `FCAST-EQ-20260825-05` | earthquake | Scotia Sea (-60.3515,-47.5217) r=39.1 km | 2026-08-25 → 2026-09-01 | M≥5.0 count≥1 | loading_suction |
| `FCAST-EQ-20260825-06` | earthquake | 56 km NNE of Port-Olry, Vanuatu (-14.5474,167.1934) r=39.1 km | 2026-08-25 → 2026-09-01 | M≥5.0 count≥1 | steady |
| `FCAST-EQ-20260825-07` | earthquake | 33 km SSW of Honchō, Japan (41.8344,142.8255) r=39.1 km | 2026-08-25 → 2026-09-01 | M≥5.0 count≥1 | loading_suction |
| `FCAST-EQ-20260825-08` | earthquake | South Sandwich Islands region (-60.2445,-28.9899) r=39.1 km | 2026-08-25 → 2026-09-01 | M≥5.0 count≥1 | steady |
| `FCAST-WX-20260825-01` | weather | NDBC RDDA2 (67.575,-164.067) r=50.0 km | 2026-08-25 → 2026-08-27 | storm_sector | loading_suction |
| `FCAST-WX-20260825-02` | weather | NDBC WRXA2 (70.636,-160.034) r=50.0 km | 2026-08-25 → 2026-08-27 | storm_sector | loading_suction |
| `FCAST-WX-20260825-03` | weather | NDBC UQXA2 (71.315,-156.722) r=50.0 km | 2026-08-25 → 2026-08-27 | storm_sector | loading_suction |
| `FCAST-WX-20260825-04` | weather | NDBC KOZA2 (66.901,-162.589) r=50.0 km | 2026-08-25 → 2026-08-27 | storm_sector | loading_suction |
| `FCAST-WX-20260825-05` | weather | NDBC DHXA2 (70.222,-148.419) r=50.0 km | 2026-08-25 → 2026-08-27 | storm_sector | loading_suction |
| `FCAST-SOL-20260825-01` | solar | Earth magnetosphere (planetary Kp) (0.0,0.0) r=6371.0 km | 2026-08-25 → 2026-08-28 | Kp stays <5 | steady |
| `FCAST-VOLC-20260825-01` | volcanic | Volcano Islands, Japan region (23.4461,142.7868) r=39.1 km | 2026-08-25 → 2026-09-08 | volcanic_or_explosion_in_window | loading_suction |

Frozen JSON: `predictions/dated_forecasts/LATEST.json`

These are **not** USGS/NWS watches. They are FSOT valve cells so we can iron out hit/miss.
