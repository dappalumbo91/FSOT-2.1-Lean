# Dated fluid-forecast scores

*Scored rollup 2026-09-17T21:51:32.675673+00:00 · pin D1D38A*

Issued forecast JSON is **not** rewritten. This is `results/` only.
EQ / hydro windows close **2026-09-01**. Volcanic **2026-09-08**.

Refresh: `python scripts/score_earth_fluid_forecasts.py` then this script.

## `2026-08-25_score.json`

hold **7** · kill **8** · awaiting **0**

| ID | Kind | Result | Detail |
|----|------|--------|--------|
| `FCAST-EQ-20260825-01` | earthquake | **hold** |  |
| `FCAST-EQ-20260825-02` | earthquake | **kill** |  |
| `FCAST-EQ-20260825-03` | earthquake | **kill** |  |
| `FCAST-EQ-20260825-04` | earthquake | **kill** |  |
| `FCAST-EQ-20260825-05` | earthquake | **kill** |  |
| `FCAST-EQ-20260825-06` | earthquake | **kill** |  |
| `FCAST-EQ-20260825-07` | earthquake | **kill** |  |
| `FCAST-EQ-20260825-08` | earthquake | **kill** |  |
| `FCAST-WX-20260825-01` | weather | **hold** | buoy RDDA2 expect_storm=True saw_storm=True n=471 |
| `FCAST-WX-20260825-02` | weather | **hold** | buoy WRXA2 expect_storm=True saw_storm=True n=288 |
| `FCAST-WX-20260825-03` | weather | **hold** | buoy UQXA2 expect_storm=True saw_storm=True n=286 |
| `FCAST-WX-20260825-04` | weather | **hold** | buoy KOZA2 expect_storm=True saw_storm=True n=287 |
| `FCAST-WX-20260825-05` | weather | **hold** | buoy DHXA2 expect_storm=True saw_storm=True n=288 |
| `FCAST-SOL-20260825-01` | solar | **hold** | Kp_max=1.0 expect_ge5=False |
| `FCAST-VOLC-20260825-01` | volcanic | **kill** |  |

## `2026-08-25T012157_score.json`

hold **8** · kill **11** · awaiting **1**

| ID | Kind | Result | Detail |
|----|------|--------|--------|
| `FCAST-EQ-20260825T0121-01` | earthquake | **hold** |  |
| `FCAST-EQ-20260825T0121-02` | earthquake | **kill** |  |
| `FCAST-EQ-20260825T0121-03` | earthquake | **kill** |  |
| `FCAST-EQ-20260825T0121-04` | earthquake | **kill** |  |
| `FCAST-EQ-20260825T0121-05` | earthquake | **kill** |  |
| `FCAST-EQ-20260825T0121-06` | earthquake | **kill** |  |
| `FCAST-EQ-20260825T0121-07` | earthquake | **kill** |  |
| `FCAST-EQ-20260825T0121-08` | earthquake | **kill** |  |
| `FCAST-WX-20260825T0121-01` | weather | **hold** | buoy WRXA2 expect_storm=True saw_storm=True n=288 |
| `FCAST-WX-20260825T0121-02` | weather | **hold** | buoy SGXA2 expect_storm=True saw_storm=True n=288 |
| `FCAST-WX-20260825T0121-03` | weather | **kill** | buoy OLCN6 expect_storm=False saw_storm=True n=288 |
| `FCAST-WX-20260825T0121-04` | weather | **awaiting** | no NDBC realtime/stdmet in window for 45144 |
| `FCAST-WX-20260825T0121-05` | weather | **kill** | buoy 42058 expect_storm=False saw_storm=True n=284 |
| `FCAST-WX-20260825T0121-06` | weather | **hold** | buoy BABT2 expect_storm=False saw_storm=True n=474 |
| `FCAST-SOL-20260825T0121-01` | solar | **hold** | Kp_max=1.0 expect_ge5=False |
| `FCAST-VOLC-20260825T0121-01` | volcanic | **kill** |  |
| `FCAST-TIDE-20260825T0121-01` | tide | **kill** | CO-OPS 9414290 expect_surge=True max_resid=0.145 m n=48 |
| `FCAST-TIDE-20260825T0121-02` | tide | **hold** | CO-OPS 8443970 expect_surge=True max_resid=0.248 m n=48 |
| `FCAST-TIDE-20260825T0121-03` | tide | **hold** | CO-OPS 9410170 expect_surge=True max_resid=0.269 m n=48 |
| `FCAST-TIDE-20260825T0121-04` | tide | **hold** | CO-OPS 8724580 expect_surge=False max_resid=0.121 m n=48 |

## `2026-08-25T022247_score.json`

hold **13** · kill **13** · awaiting **2**

| ID | Kind | Result | Detail |
|----|------|--------|--------|
| `FCAST-EQ-20260825T0222-01` | earthquake | **hold** |  |
| `FCAST-EQ-20260825T0222-02` | earthquake | **kill** |  |
| `FCAST-EQ-20260825T0222-03` | earthquake | **kill** |  |
| `FCAST-EQ-20260825T0222-04` | earthquake | **kill** |  |
| `FCAST-EQ-20260825T0222-05` | earthquake | **kill** |  |
| `FCAST-EQ-20260825T0222-06` | earthquake | **kill** |  |
| `FCAST-EQ-20260825T0222-07` | earthquake | **kill** |  |
| `FCAST-EQ-20260825T0222-08` | earthquake | **kill** |  |
| `FCAST-WX-20260825T0222-01` | weather | **hold** | buoy UQXA2 expect_storm=True saw_storm=True n=286 |
| `FCAST-WX-20260825T0222-02` | weather | **awaiting** | no NDBC realtime/stdmet in window for 46208 |
| `FCAST-WX-20260825T0222-03` | weather | **kill** | buoy OLCN6 expect_storm=False saw_storm=True n=288 |
| `FCAST-WX-20260825T0222-04` | weather | **awaiting** | no NDBC realtime/stdmet in window for 45145 |
| `FCAST-WX-20260825T0222-05` | weather | **kill** | buoy 42058 expect_storm=False saw_storm=True n=284 |
| `FCAST-WX-20260825T0222-06` | weather | **hold** | buoy EPTT2 expect_storm=False saw_storm=True n=478 |
| `FCAST-SOL-20260825T0222-01` | solar | **hold** | Kp_max=1.0 expect_ge5=False |
| `FCAST-VOLC-20260825T0222-01` | volcanic | **kill** |  |
| `FCAST-TIDE-20260825T0222-01` | tide | **hold** | CO-OPS 8443970 expect_surge=True max_resid=0.248 m n=48 |
| `FCAST-TIDE-20260825T0222-02` | tide | **hold** | CO-OPS 9410170 expect_surge=True max_resid=0.269 m n=48 |
| `FCAST-TIDE-20260825T0222-03` | tide | **hold** | CO-OPS 9414290 expect_surge=False max_resid=0.145 m n=48 |
| `FCAST-TIDE-20260825T0222-04` | tide | **hold** | CO-OPS 8724580 expect_surge=False max_resid=0.121 m n=48 |
| `FCAST-HYDRO-20260825T0222-01` | hydrology | **kill** | NWIS 01646500 expect_high=False mean=3464.93 cfs |
| `FCAST-HYDRO-20260825T0222-02` | hydrology | **hold** | NWIS 05420500 expect_high=False mean=11135.77 cfs |
| `FCAST-HYDRO-20260825T0222-03` | hydrology | **hold** | NWIS 08013000 expect_high=False mean=31.83 cfs |
| `FCAST-HYDRO-20260825T0222-04` | hydrology | **hold** | NWIS 09402500 expect_high=False mean=7773.18 cfs |
| `FCAST-HYDRO-20260825T0222-05` | hydrology | **kill** | NWIS 06803510 expect_high=True mean=4.19 cfs |
| `FCAST-HYDRO-20260825T0222-06` | hydrology | **hold** | NWIS 14246900 expect_high=False mean=219745.49 cfs |
| `FCAST-HYDRO-20260825T0222-07` | hydrology | **hold** | NWIS 023177483 expect_high=False mean=276.71 cfs |
| `FCAST-HYDRO-20260825T0222-08` | hydrology | **kill** | NWIS 03072655 expect_high=True mean=3052.06 cfs |

## `2026-08-31_score.json`

hold **17** · kill **9** · awaiting **0**

| ID | Kind | Result | Detail |
|----|------|--------|--------|
| `FCAST-EQ-20260831T2357-01` | earthquake | **kill** |  |
| `FCAST-EQ-20260831T2357-02` | earthquake | **hold** |  |
| `FCAST-EQ-20260831T2357-03` | earthquake | **kill** |  |
| `FCAST-EQ-20260831T2357-04` | earthquake | **kill** |  |
| `FCAST-EQ-20260831T2357-05` | earthquake | **kill** |  |
| `FCAST-EQ-20260831T2357-06` | earthquake | **kill** |  |
| `FCAST-EQ-20260831T2357-07` | earthquake | **kill** |  |
| `FCAST-EQ-20260831T2357-08` | earthquake | **kill** |  |
| `FCAST-WX-20260831T2357-01` | weather | **hold** | buoy MDXA2 expect_storm=True saw_storm=True n=288 |
| `FCAST-WX-20260831T2357-02` | weather | **hold** | buoy PPXA2 expect_storm=True saw_storm=True n=288 |
| `FCAST-WX-20260831T2357-03` | weather | **hold** | buoy APRP7 expect_storm=False saw_storm=True n=480 |
| `FCAST-WX-20260831T2357-04` | weather | **hold** | buoy BZST2 expect_storm=False saw_storm=True n=480 |
| `FCAST-WX-20260831T2357-05` | weather | **kill** | buoy 44078 expect_storm=False saw_storm=True n=288 |
| `FCAST-SOL-20260831T2357-01` | solar | **hold** | Kp_max=2.333 expect_ge5=False |
| `FCAST-TIDE-20260831T2357-01` | tide | **hold** | CO-OPS 9414290 expect_surge=True max_resid=0.17 m n=48 |
| `FCAST-TIDE-20260831T2357-02` | tide | **hold** | CO-OPS 8443970 expect_surge=True max_resid=0.266 m n=48 |
| `FCAST-TIDE-20260831T2357-03` | tide | **hold** | CO-OPS 9410170 expect_surge=True max_resid=0.254 m n=48 |
| `FCAST-TIDE-20260831T2357-04` | tide | **hold** | CO-OPS 8771341 expect_surge=True max_resid=0.292 m n=48 |
| `FCAST-HYDRO-20260831T2357-01` | hydrology | **kill** | NWIS 01646500 expect_high=True mean=2287.79 cfs |
| `FCAST-HYDRO-20260831T2357-02` | hydrology | **hold** | NWIS 05420500 expect_high=False mean=10941.4 cfs |
| `FCAST-HYDRO-20260831T2357-03` | hydrology | **hold** | NWIS 08013000 expect_high=False mean=30.86 cfs |
| `FCAST-HYDRO-20260831T2357-04` | hydrology | **hold** | NWIS 09402500 expect_high=False mean=7742.96 cfs |
| `FCAST-HYDRO-20260831T2357-05` | hydrology | **hold** | NWIS 06803510 expect_high=False mean=3.09 cfs |
| `FCAST-HYDRO-20260831T2357-06` | hydrology | **hold** | NWIS 14246900 expect_high=False mean=197983.42 cfs |
| `FCAST-HYDRO-20260831T2357-07` | hydrology | **hold** | NWIS 023177483 expect_high=True mean=282.54 cfs |
| `FCAST-HYDRO-20260831T2357-08` | hydrology | **hold** | NWIS 03072655 expect_high=False mean=3783.93 cfs |

## `2026-09-01_score.json`

hold **20** · kill **4** · awaiting **1**

| ID | Kind | Result | Detail |
|----|------|--------|--------|
| `FCAST-EQ-20260901T0032-01` | earthquake | **hold** |  |
| `FCAST-EQ-20260901T0032-02` | earthquake | **hold** |  |
| `FCAST-EQ-20260901T0032-03` | earthquake | **hold** |  |
| `FCAST-EQ-20260901T0032-04` | earthquake | **hold** |  |
| `FCAST-EQ-20260901T0032-05` | earthquake | **kill** |  |
| `FCAST-EQ-20260901T0032-06` | earthquake | **hold** |  |
| `FCAST-EQ-20260901T0032-07` | earthquake | **hold** |  |
| `FCAST-EQ-20260901T0032-08` | earthquake | **kill** |  |
| `FCAST-WX-20260901T0032-01` | weather | **hold** | buoy MDXA2 expect_storm=True saw_storm=True n=288 |
| `FCAST-WX-20260901T0032-02` | weather | **hold** | buoy PPXA2 expect_storm=True saw_storm=True n=288 |
| `FCAST-WX-20260901T0032-03` | weather | **hold** | buoy 42013 expect_storm=True saw_storm=True n=95 |
| `FCAST-WX-20260901T0032-04` | weather | **hold** | buoy APRP7 expect_storm=False saw_storm=True n=480 |
| `FCAST-WX-20260901T0032-05` | weather | **awaiting** | no NDBC realtime/stdmet in window for 62146 |
| `FCAST-TIDE-20260901T0032-01` | tide | **hold** | CO-OPS 9414290 expect_surge=True max_resid=0.17 m n=48 |
| `FCAST-TIDE-20260901T0032-02` | tide | **hold** | CO-OPS 9410170 expect_surge=True max_resid=0.254 m n=48 |
| `FCAST-TIDE-20260901T0032-03` | tide | **hold** | CO-OPS 8771341 expect_surge=True max_resid=0.292 m n=48 |
| `FCAST-TIDE-20260901T0032-04` | tide | **kill** | CO-OPS 8443970 expect_surge=False max_resid=0.266 m n=48 |
| `FCAST-HYDRO-20260901T0032-01` | hydrology | **kill** | NWIS 01646500 expect_high=True mean=2162.86 cfs |
| `FCAST-HYDRO-20260901T0032-02` | hydrology | **hold** | NWIS 05420500 expect_high=False mean=10200.0 cfs |
| `FCAST-HYDRO-20260901T0032-03` | hydrology | **hold** | NWIS 08013000 expect_high=False mean=30.46 cfs |
| `FCAST-HYDRO-20260901T0032-04` | hydrology | **hold** | NWIS 09402500 expect_high=False mean=7699.26 cfs |
| `FCAST-HYDRO-20260901T0032-05` | hydrology | **hold** | NWIS 06803510 expect_high=False mean=3.02 cfs |
| `FCAST-HYDRO-20260901T0032-06` | hydrology | **hold** | NWIS 14246900 expect_high=False mean=197894.59 cfs |
| `FCAST-HYDRO-20260901T0032-07` | hydrology | **hold** | NWIS 023177483 expect_high=True mean=329.46 cfs |
| `FCAST-HYDRO-20260901T0032-08` | hydrology | **hold** | NWIS 03072655 expect_high=False mean=4244.13 cfs |

## `2026-09-09_score.json`

hold **20** · kill **4** · awaiting **2**

| ID | Kind | Result | Detail |
|----|------|--------|--------|
| `FCAST-EQ-20260909T1854-01` | earthquake | **hold** |  |
| `FCAST-EQ-20260909T1854-02` | earthquake | **hold** |  |
| `FCAST-EQ-20260909T1854-03` | earthquake | **hold** |  |
| `FCAST-EQ-20260909T1854-04` | earthquake | **kill** |  |
| `FCAST-EQ-20260909T1854-05` | earthquake | **hold** |  |
| `FCAST-EQ-20260909T1854-06` | earthquake | **kill** |  |
| `FCAST-EQ-20260909T1854-07` | earthquake | **hold** |  |
| `FCAST-EQ-20260909T1854-08` | earthquake | **hold** |  |
| `FCAST-WX-20260909T1854-01` | weather | **awaiting** | no NDBC realtime/stdmet in window for 62442 |
| `FCAST-WX-20260909T1854-02` | weather | **hold** | buoy 46070 expect_storm=True saw_storm=True n=227 |
| `FCAST-WX-20260909T1854-03` | weather | **awaiting** | no NDBC realtime/stdmet in window for 64046 |
| `FCAST-WX-20260909T1854-04` | weather | **hold** | buoy 51002 expect_storm=False saw_storm=True n=235 |
| `FCAST-WX-20260909T1854-05` | weather | **kill** | buoy PTIT2 expect_storm=False saw_storm=True n=480 |
| `FCAST-SOL-20260909T1854-01` | solar | **hold** | Kp_max=3.0 expect_ge5=False |
| `FCAST-TIDE-20260909T1854-01` | tide | **hold** | CO-OPS 9414290 expect_surge=True max_resid=0.29 m n=48 |
| `FCAST-TIDE-20260909T1854-02` | tide | **hold** | CO-OPS 8443970 expect_surge=True max_resid=0.247 m n=47 |
| `FCAST-TIDE-20260909T1854-03` | tide | **hold** | CO-OPS 9410170 expect_surge=True max_resid=0.323 m n=48 |
| `FCAST-TIDE-20260909T1854-04` | tide | **kill** | CO-OPS 8724580 expect_surge=False max_resid=0.179 m n=48 |
| `FCAST-HYDRO-20260909T1854-01` | hydrology | **hold** | NWIS 01646500 expect_high=False mean=1799.05 cfs |
| `FCAST-HYDRO-20260909T1854-02` | hydrology | **hold** | NWIS 05464500 expect_high=False mean=2845.76 cfs |
| `FCAST-HYDRO-20260909T1854-03` | hydrology | **hold** | NWIS 08114000 expect_high=True mean=754.04 cfs |
| `FCAST-HYDRO-20260909T1854-04` | hydrology | **hold** | NWIS 09380000 expect_high=False mean=7889.87 cfs |
| `FCAST-HYDRO-20260909T1854-05` | hydrology | **hold** | NWIS 06934500 expect_high=False mean=43707.59 cfs |
| `FCAST-HYDRO-20260909T1854-06` | hydrology | **hold** | NWIS 14144700 expect_high=False mean=85271.4 cfs |
| `FCAST-HYDRO-20260909T1854-07` | hydrology | **hold** | NWIS 023177483 expect_high=False mean=230.21 cfs |
| `FCAST-HYDRO-20260909T1854-08` | hydrology | **hold** | NWIS 03072655 expect_high=True mean=6791.39 cfs |

## Totals (all issues)

hold **85** · kill **49** · awaiting **6**

Tide hours are clipped to `valid_from`–`valid_to` (not the whole end calendar day).
Quiet-weather kills use the issued kill_if (pres<1005 or gust≥12). Do not rewrite issues.
New issues skip the 1000–1005 hPa / 12–15 m/s gap (doomed quiet) and skip lake `other` buoys.
Hydro IDs on **new** issues use the 2026-09-07 NWIS map (`06934500` Missouri at Hermann). Issued JSON keeps the old IDs.

## Remaining awaiting (missing catalogs, not a retune)

These cells closed but the public archive was empty in-window. Do not rewrite the issue. Do not invent a residual.

| ID | Catalog | Why still awaiting |
|----|---------|--------------------|
| `FCAST-WX-20260825T0121-04` | weather | no NDBC realtime/stdmet in window for 45144 |
| `FCAST-WX-20260825T0222-02` | weather | no NDBC realtime/stdmet in window for 46208 |
| `FCAST-WX-20260825T0222-04` | weather | no NDBC realtime/stdmet in window for 45145 |
| `FCAST-WX-20260901T0032-05` | weather | no NDBC realtime/stdmet in window for 62146 |
| `FCAST-WX-20260909T1854-01` | weather | no NDBC realtime/stdmet in window for 62442 |
| `FCAST-WX-20260909T1854-03` | weather | no NDBC realtime/stdmet in window for 64046 |

## 2026-09-01 playbook — honest loading misses (not a kernel retune)

The 09-01 issue already used `expect_event` only on loading/post-POOF. Two ocean loading cells stayed quiet inside 39 km. Same grammar as Scotia Sea.

| ID | Place | Valve | Result |
|----|-------|-------|--------|
| `FCAST-EQ-20260901T0032-05` | 32 km SSW of Honchō, Japan | loading · M≥4.5 | **kill** (no M≥4.5 in kernel) |
| `FCAST-EQ-20260901T0032-08` | Kermadec Islands, New Zealand | loading · M≥4.5 | **kill** (no M≥4.5 in kernel) |
| `FCAST-HYDRO-20260901T0032-01` | Potomac `01646500` (correct ID) | loading | **kill** (window mean dropped) |

Do not retune kernel km, POOF, or ρ to swallow ocean-catalog sparse cells.
