# Planetary-cycle connective tanks — why isolated cells kill

*Generated 2026-09-09T19:01:45.958775+00:00 · pin D1D38A*

Earth is one 25-D compactified fluid. A dated cell is **one slice** of the
crustal orifice. Solar wind, volcanic arcs, trenches, weather basins, and
rivers are **other tanks of the same valve**. Scoring them as siloed
catalogs misses a POOF that dumped next door.

| Scale | Form | km | Job |
|-------|------|---:|-----|
| Cell (issued kill_if) | \(R_\oplus\cdot\mathrm{POOF}/25\) | **39.1** | compactified crustal orifice |
| Planetary cycle | \(R_\oplus\cdot\mathrm{POOF}\) | **977.8** | arc / trench / basin tanks talk |
| Solar | planetary Kp | global | magnetosphere tank (already issued) |

Not a new coefficient. The `/25` is the compactification fold. Taking it
off is looking at the planet as one tank, the same way Materials and Optics
are two looks at \(D=10\).

**Public scoreboard stays the cell kill.** This ledger names the neighbor
POOF. Do not retune kernel km or POOF. Do not rewrite issued JSON.

**Refresh:** `python scripts/diagnose_planetary_cycle_kills.py`

## Unique loading / volcanic kills

| ID | Place | Cell M≥4.5 | Cycle M≥4.5 | Kp | Verdict | Why |
|----|-------|-----------:|------------:|---:|---------|-----|
| `FCAST-EQ-20260825-04` | 215 km NNE of Lospalos, Timor Leste | 3 | 26 (M5.5 @ 776.3 km) | 4.33 | **playbook_bar** | POOF was in the cell (M≥4.5 n=3) but the issued bar was M≥5. Old-rule kill. Not a missing tank. |
| `FCAST-EQ-20260825-05` | Scotia Sea | 0 | 0 | 4.33 | **honest_quiet** | Loading cell, no M≥4.5 inside 978 km, Kp_max=4.33. SUCTION held. Not a kernel retune. |
| `FCAST-EQ-20260825-07` | 33 km SSW of Honchō, Japan | 1 | 13 (M5.6 @ 415.3 km) | 4.33 | **playbook_bar** | POOF was in the cell (M≥4.5 n=1) but the issued bar was M≥5. Old-rule kill. Not a missing tank. |
| `FCAST-VOLC-20260825-01` | Volcano Islands, Japan region | 0 | 2 (M5.2 @ 90.9 km) | 4.67 | **transferred_poof** | Cell quiet inside 39 km. Cycle orifice R⊕·POOF=978 km had 2 M≥4.5 (max M=5.2 at 90.9 km, Volcano Islands, Japan region). Load dumped in the arc/trench tank. |
| `FCAST-EQ-20260831T2357-05` | 32 km SSW of Honchō, Japan | 0 | 6 (M5.5 @ 673.4 km) | 4.67 | **transferred_poof** | Cell quiet inside 39 km. Cycle orifice R⊕·POOF=978 km had 6 M≥4.5 (max M=5.5 at 673.4 km, 168 km ESE of Kuril’sk, Russia). Load dumped in the arc/trench tank. |
| `FCAST-EQ-20260831T2357-08` | Kermadec Islands, New Zealand | 0 | 5 (M5.4 @ 213.4 km) | 4.67 | **transferred_poof** | Cell quiet inside 39 km. Cycle orifice R⊕·POOF=978 km had 5 M≥4.5 (max M=5.4 at 213.4 km, Kermadec Islands region). Load dumped in the arc/trench tank. |
| `FCAST-EQ-20260901T0032-05` | 32 km SSW of Honchō, Japan | 0 | 5 (M5.5 @ 673.4 km) | 4.67 | **transferred_poof** | Cell quiet inside 39 km. Cycle orifice R⊕·POOF=978 km had 5 M≥4.5 (max M=5.5 at 673.4 km, 168 km ESE of Kuril’sk, Russia). Load dumped in the arc/trench tank. |
| `FCAST-EQ-20260901T0032-08` | Kermadec Islands, New Zealand | 0 | 8 (M5.4 @ 213.4 km) | 4.67 | **transferred_poof** | Cell quiet inside 39 km. Cycle orifice R⊕·POOF=978 km had 8 M≥4.5 (max M=5.4 at 213.4 km, Kermadec Islands region). Load dumped in the arc/trench tank. |

Counts: {'playbook_bar': 2, 'honest_quiet': 1, 'transferred_poof': 5}.

## Verdict vocabulary

| Verdict | Meaning | Next issue |
|---------|---------|------------|
| `transferred_poof` | Cell quiet; cycle orifice had M≥4.5 (arc/trench). | Record neighbor tank. Cell kill_if unchanged. |
| `playbook_bar` | POOF was in the cell under M≥4.5; issued bar was M≥5. | Already encoded: loading uses 4.5. |
| `solar_coupled` | Crust quiet; Kp≥5. Solar tank loaded. | Keep solar as a planetary tank on every crustal issue. |
| `honest_quiet` | Loading, no cycle POOF, Kp quiet. SUCTION held. | Not a kernel retune. |

## What this is not

- A fitted 150 km or 1000 km spring to swallow Scotia Sea / Honchō / Kermadec.
- A clock-time hypocenter.
- Flipping a public cell-kill to hold.
- A new \(D_{\mathrm{eff}}\) for 'planetary science of earthquakes'.

Issued EQ/volcanic forecasts now carry `cycle_radius_km` and
`neighbor_kinds` on **new** issues only.

Related: [`WEATHER_MONITORING_APPROACH.md`](WEATHER_MONITORING_APPROACH.md) ·
[`CONCEPTS.md`](CONCEPTS.md) C1/C2/C10 ·
[`../results/dated_forecast_scores/KILL_AUTOPSY.md`](../results/dated_forecast_scores/KILL_AUTOPSY.md)
