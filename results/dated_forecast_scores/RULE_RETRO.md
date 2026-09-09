# Playbook retrospective — 12 frozen kills under the refined rule

*Generated 2026-09-01T00:42:40.613794+00:00 · pin D1D38A*

Issued JSON is **still frozen**. Public scoreboard of those files stays
**12 kills**. This is not a restuff. It asks whether the
playbook encoded after the autopsy would have issued a different call.

POOF = 0.1535 m · score bar = POOF · issue bar = POOF·(1+POOF) = **0.1770 m**.

Converted to hold **6** · still kill **1** · would not issue **5**.

## Earthquakes

| ID | Place | Valve | New call | Converted | Why |
|----|-------|-------|----------|-----------|-----|
| `FCAST-EQ-20260825-02` | 9 km WNW of Pematangsiantar, Indonesia | **steady** | M≥5.0 expect=False | **hold** | released/steady → quiet hold (kill only if M≥5 shows); n_M5=0 |
| `FCAST-EQ-20260825-03` | 31 km NW of Aniso, Peru | **released** | M≥5.0 expect=False | **hold** | released/steady → quiet hold (kill only if M≥5 shows); n_M5=0 |
| `FCAST-EQ-20260825-04` | 215 km NNE of Lospalos, Timor Leste | **loading_suction** | M≥4.5 expect=True | **hold** | loading → expect M≥4.5; kernel had 4.8 |
| `FCAST-EQ-20260825-05` | Scotia Sea | **loading_suction** | M≥4.5 expect=True | **kill** | loading → expect M≥4.5; no M≥4.5 in kernel |
| `FCAST-EQ-20260825-06` | 56 km NNE of Port-Olry, Vanuatu | **steady** | M≥5.0 expect=False | **hold** | released/steady → quiet hold (kill only if M≥5 shows); n_M5=0 |
| `FCAST-EQ-20260825-07` | 33 km SSW of Honchō, Japan | **loading_suction** | M≥4.5 expect=True | **hold** | loading → expect M≥4.5; kernel had 4.5 |
| `FCAST-EQ-20260825-08` | South Sandwich Islands region | **steady** | M≥5.0 expect=False | **hold** | released/steady → quiet hold (kill only if M≥5 shows); n_M5=0 |

## Weather quiet

| ID | Buoy | At issue | Converted | Why |
|----|------|----------|-----------|-----|
| `FCAST-WX-20260825T0121-03` | NDBC OLCN6 (atlantic) | 1004.4 hPa / 9.3 m/s | **would_not_issue** | gap-zone quiet (pres=1004.4 hPa, gst=9.3 m/s); new issuer skips 1000–1010 / 8–15 |
| `FCAST-WX-20260825T0121-05` | NDBC 42058 (tropics) | 1010.4 hPa / 12.0 m/s | **would_not_issue** | gap-zone quiet (pres=1010.4 hPa, gst=12.0 m/s); new issuer skips 1000–1010 / 8–15 |
| `FCAST-WX-20260825T0222-03` | NDBC OLCN6 (atlantic) | 1004.7 hPa / 13.9 m/s | **would_not_issue** | gap-zone quiet (pres=1004.7 hPa, gst=13.9 m/s); new issuer skips 1000–1010 / 8–15 |
| `FCAST-WX-20260825T0222-05` | NDBC 42058 (tropics) | 1011.2 hPa / 11.0 m/s | **would_not_issue** | gap-zone quiet (pres=1011.2 hPa, gst=11.0 m/s); new issuer skips 1000–1010 / 8–15 |

## Tide

| ID | Station | Snapshot | Window max | Converted | Why |
|----|---------|---------:|-----------:|-----------|-----|
| `FCAST-TIDE-20260825T0121-01` | NOAA San Francisco (9414290) | 0.157 m | 0.145 m | **would_not_issue** | snapshot 0.157 m < issue bar POOF·(1+POOF)=0.177 m (score bar still POOF=0.153 m) |

## What still kills

- `FCAST-EQ-20260825-05` (Scotia Sea): loading → expect M≥4.5; no M≥4.5 in kernel

Scotia Sea is the remaining EQ miss: a loading cell with no M≥4.5 inside 39 km. Ocean catalog is sparse; do not retune kernel km or ρ to swallow it. Next issues keep the same kernel; a loading ocean cell that stays quiet is an honest kill.

## What we will not do

- Rewrite issued JSON.
- Change the public hold/kill counts on frozen files.
- Retune ρ, POOF, or kernel km to swallow Scotia Sea.

Refresh: `python scripts/retro_dated_forecast_rule.py`

Related: [`KILL_AUTOPSY.md`](KILL_AUTOPSY.md) · [`../../docs/WEATHER_MONITORING_APPROACH.md`](../../docs/WEATHER_MONITORING_APPROACH.md)
