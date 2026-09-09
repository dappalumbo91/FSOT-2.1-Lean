# Planetary-cycle connective tanks — why isolated cells kill

*Generated 2026-09-09T19:12:00.017036+00:00 · pin D1D38A*

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

Lean: `cycle_km = 25 * kernel_km` (`FSOT/Formal/ScalarEngineStructure.lean`
`cycle_km_eq_twentyfive_mul_kernel_km`). Law D10.

## Unique loading / volcanic kills

| ID | Place | Cell M≥4.5 | Cycle M≥4.5 | Kp | Verdict | Why |
|----|-------|-----------:|------------:|---:|---------|-----|
| `FCAST-EQ-20260825-02` | 9 km WNW of Pematangsiantar, Indonesia | 0 | 1 (M4.9 @ 776.6 km) | 4.33 | **transferred_poof** | Cell quiet inside 39 km. Cycle orifice R⊕·POOF=978 km had 1 M≥4.5 (max M=4.9 at 776.6 km, 76 km WNW of Bengkulu, Indonesia). Load dumped in the arc/trench tank. |
| `FCAST-EQ-20260825-03` | 31 km NW of Aniso, Peru | 0 | 7 (M4.7 @ 341.1 km) | 4.33 | **transferred_poof** | Cell quiet inside 39 km. Cycle orifice R⊕·POOF=978 km had 7 M≥4.5 (max M=4.7 at 341.1 km, 3 km NW of Yanacancha, Peru). Load dumped in the arc/trench tank. |
| `FCAST-EQ-20260825-04` | 215 km NNE of Lospalos, Timor Leste | 3 | 26 (M5.5 @ 776.3 km) | 4.33 | **playbook_bar** | POOF was in the cell (M≥4.5 n=3) but the issued bar was M≥5. Old-rule kill. Not a missing tank. |
| `FCAST-EQ-20260825-05` | Scotia Sea | 0 | 0 | 4.33 | **already_poofed** | Recent max M=6.2 was the POOF. Window asked for another mainshock after the orifice opened. Omori SUCTION can go quiet. Not a missing 978 km tank and not a kernel retune. |
| `FCAST-EQ-20260825-06` | 56 km NNE of Port-Olry, Vanuatu | 0 | 8 (M5.0 @ 534.3 km) | 4.33 | **transferred_poof** | Cell quiet inside 39 km. Cycle orifice R⊕·POOF=978 km had 8 M≥4.5 (max M=5.0 at 534.3 km, 115 km WNW of Isangel, Vanuatu). Load dumped in the arc/trench tank. |
| `FCAST-EQ-20260825-07` | 33 km SSW of Honchō, Japan | 1 | 13 (M5.6 @ 415.3 km) | 4.33 | **playbook_bar** | POOF was in the cell (M≥4.5 n=1) but the issued bar was M≥5. Old-rule kill. Not a missing tank. |
| `FCAST-EQ-20260825-08` | South Sandwich Islands region | 0 | 4 (M5.1 @ 436.7 km) | 4.33 | **transferred_poof** | Cell quiet inside 39 km. Cycle orifice R⊕·POOF=978 km had 4 M≥4.5 (max M=5.1 at 436.7 km, South Sandwich Islands region). Load dumped in the arc/trench tank. |
| `FCAST-VOLC-20260825-01` | Volcano Islands, Japan region | 0 | 2 (M5.2 @ 90.9 km) | 4.67 | **transferred_poof** | Cell quiet inside 39 km. Cycle orifice R⊕·POOF=978 km had 2 M≥4.5 (max M=5.2 at 90.9 km, Volcano Islands, Japan region). Load dumped in the arc/trench tank. |
| `FCAST-EQ-20260831T2357-01` | 31 km NW of Aniso, Peru | 0 | 3 (M4.7 @ 341.1 km) | 4.67 | **transferred_poof** | Cell quiet inside 39 km. Cycle orifice R⊕·POOF=978 km had 3 M≥4.5 (max M=4.7 at 341.1 km, 3 km NW of Yanacancha, Peru). Load dumped in the arc/trench tank. |
| `FCAST-EQ-20260831T2357-03` | Scotia Sea | 0 | 0 | 4.67 | **already_poofed** | Recent max M=6.2 was the POOF. Window asked for another mainshock after the orifice opened. Omori SUCTION can go quiet. Not a missing 978 km tank and not a kernel retune. |
| `FCAST-EQ-20260831T2357-04` | 215 km NNE of Lospalos, Timor Leste | 0 | 10 (M5.6 @ 770.5 km) | 4.67 | **transferred_poof** | Cell quiet inside 39 km. Cycle orifice R⊕·POOF=978 km had 10 M≥4.5 (max M=5.6 at 770.5 km, 82 km SE of Maba, Indonesia). Load dumped in the arc/trench tank. |
| `FCAST-EQ-20260831T2357-05` | 32 km SSW of Honchō, Japan | 0 | 6 (M5.5 @ 673.4 km) | 4.67 | **transferred_poof** | Cell quiet inside 39 km. Cycle orifice R⊕·POOF=978 km had 6 M≥4.5 (max M=5.5 at 673.4 km, 168 km ESE of Kuril’sk, Russia). Load dumped in the arc/trench tank. |
| `FCAST-EQ-20260831T2357-06` | 145 km N of Caluula, Somalia | 0 | 1 (M5.1 @ 651.5 km) | 4.67 | **transferred_poof** | Cell quiet inside 39 km. Cycle orifice R⊕·POOF=978 km had 1 M≥4.5 (max M=5.1 at 651.5 km, Owen Fracture Zone region). Load dumped in the arc/trench tank. |
| `FCAST-EQ-20260831T2357-07` | 4 km N of Toride, Japan | 0 | 4 (M4.9 @ 589.3 km) | 4.67 | **transferred_poof** | Cell quiet inside 39 km. Cycle orifice R⊕·POOF=978 km had 4 M≥4.5 (max M=4.9 at 589.3 km, 118 km ENE of Kuji, Japan). Load dumped in the arc/trench tank. |
| `FCAST-EQ-20260831T2357-08` | Kermadec Islands, New Zealand | 0 | 5 (M5.4 @ 213.4 km) | 4.67 | **transferred_poof** | Cell quiet inside 39 km. Cycle orifice R⊕·POOF=978 km had 5 M≥4.5 (max M=5.4 at 213.4 km, Kermadec Islands region). Load dumped in the arc/trench tank. |
| `FCAST-EQ-20260901T0032-05` | 32 km SSW of Honchō, Japan | 0 | 5 (M5.5 @ 673.4 km) | 4.67 | **transferred_poof** | Cell quiet inside 39 km. Cycle orifice R⊕·POOF=978 km had 5 M≥4.5 (max M=5.5 at 673.4 km, 168 km ESE of Kuril’sk, Russia). Load dumped in the arc/trench tank. |
| `FCAST-EQ-20260901T0032-08` | Kermadec Islands, New Zealand | 0 | 8 (M5.4 @ 213.4 km) | 4.67 | **transferred_poof** | Cell quiet inside 39 km. Cycle orifice R⊕·POOF=978 km had 8 M≥4.5 (max M=5.4 at 213.4 km, Kermadec Islands region). Load dumped in the arc/trench tank. |

Crust counts: {'transferred_poof': 13, 'playbook_bar': 2, 'already_poofed': 2}.

## Remaining other-tank kills (weather / tide / hydro)

| ID | Place | Verdict | Why |
|----|-------|---------|-----|
| `FCAST-WX-20260825T0121-03` | NDBC OLCN6 (atlantic) | **transferred_weather** | Quiet-cell kill while the same issue's storm tanks held: WRXA2, SGXA2. Load dumped in the loaded basin. Gap-zone quiet should not issue. |
| `FCAST-WX-20260825T0121-05` | NDBC 42058 (tropics) | **transferred_weather** | Quiet-cell kill while the same issue's storm tanks held: WRXA2, SGXA2. Load dumped in the loaded basin. Gap-zone quiet should not issue. |
| `FCAST-TIDE-20260825T0121-01` | NOAA San Francisco (9414290) | **issue_bar** | Surge issue bar is POOF·(1+POOF). Snapshot below issue bar. Not a POOF retune. |
| `FCAST-WX-20260825T0222-03` | NDBC OLCN6 (atlantic) | **transferred_weather** | Quiet-cell kill while the same issue's storm tanks held: UQXA2. Load dumped in the loaded basin. Gap-zone quiet should not issue. |
| `FCAST-WX-20260825T0222-05` | NDBC 42058 (tropics) | **transferred_weather** | Quiet-cell kill while the same issue's storm tanks held: UQXA2. Load dumped in the loaded basin. Gap-zone quiet should not issue. |
| `FCAST-HYDRO-20260825T0222-01` | USGS 01646500 Potomac River near Washington DC | **fluid_loaded** | Issued quiet; window mean rose. Honest quiet miss on the river tank. |
| `FCAST-HYDRO-20260825T0222-05` | USGS 06803510 Missouri River at Hermann MO | **wrong_gage** | 06803510 is Little Salt Creek, not Missouri at Hermann (06934500). Wrong object. |
| `FCAST-HYDRO-20260825T0222-08` | USGS 03072655 Monongahela River near Masontown PA | **fluid_released** | Loading at issue; window mean dropped. SUCTION completed in the river tank. |
| `FCAST-WX-20260831T2357-05` | NDBC 44078 (atlantic) | **transferred_weather** | Quiet-cell kill while the same issue's storm tanks held: MDXA2, PPXA2. Load dumped in the loaded basin. Gap-zone quiet should not issue. |
| `FCAST-HYDRO-20260831T2357-01` | USGS 01646500 Potomac River near Washington DC | **fluid_released** | Loading at issue; window mean dropped. SUCTION completed in the river tank. |
| `FCAST-TIDE-20260901T0032-04` | NOAA Boston (8443970) | **honest_quiet_load** | Harmonic cell loaded in-window. Honest quiet miss, not a POOF retune. |
| `FCAST-HYDRO-20260901T0032-01` | USGS 01646500 Potomac River near Washington DC | **fluid_released** | Loading at issue; window mean dropped. SUCTION completed in the river tank. |

All verdicts: {'transferred_poof': 13, 'playbook_bar': 2, 'already_poofed': 2, 'transferred_weather': 5, 'issue_bar': 1, 'fluid_loaded': 1, 'wrong_gage': 1, 'fluid_released': 3, 'honest_quiet_load': 1}.

## Verdict vocabulary

| Verdict | Meaning | Next issue |
|---------|---------|------------|
| `transferred_poof` | Cell quiet; cycle orifice had M≥4.5 (arc/trench). | Record neighbor tank. Cell kill_if unchanged. |
| `already_poofed` | Recent M≥5.5 *was* the POOF. Window asked for a second mainshock. | `valve_state` checks big event first; post-POOF is quiet hold. |
| `playbook_bar` | POOF was in the cell under M≥4.5; issued bar was M≥5. | Already encoded: loading uses 4.5. |
| `solar_coupled` | Crust quiet; Kp≥5. Solar tank loaded. | Keep solar as a planetary tank on every crustal issue. |
| `honest_quiet` | Loading, no cycle POOF, no recent M≥5.5, Kp quiet. SUCTION held. | Not a kernel retune. |
| `transferred_weather` | Quiet buoy kill; storm tanks on the same issue held. | Skip gap-zone quiet. |
| `wrong_gage` | Hydro ID is a different river. | 06934500 Hermann. |
| `fluid_released` | River loaded at issue; window mean dropped. | SUCTION completed. |

Scotia Sea: n_recent=2, max M=6.2. That 6.2 already opened the orifice. Labeling it `loading_suction` because rate-up ran *before* the big-event check was the remaining miss. Next issues: recent M≥5.5 → `post_poof_aftershock`, expect_event false (Omori may go quiet).

## What this is not

- A fitted 150 km or 1000 km spring to swallow Scotia Sea.
- A clock-time hypocenter.
- Flipping a public cell-kill to hold.
- A new \(D_{\mathrm{eff}}\) for 'planetary science of earthquakes'.

Issued EQ/volcanic forecasts now carry `cycle_radius_km` and
`neighbor_kinds` on **new** issues only.

Related: [`WEATHER_MONITORING_APPROACH.md`](WEATHER_MONITORING_APPROACH.md) ·
[`CONCEPTS.md`](CONCEPTS.md) C1/C2/C10 ·
[`../results/dated_forecast_scores/KILL_AUTOPSY.md`](../results/dated_forecast_scores/KILL_AUTOPSY.md)
