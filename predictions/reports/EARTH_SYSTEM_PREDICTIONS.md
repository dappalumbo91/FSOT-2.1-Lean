# Earth-system predictions (weather, seismic, volcanic, solar)

*Generated 2026-08-25T00:07:41.878363+00:00 · pin D1D38A*

Cosmology already has a 25-tool H₀ layer. This is the **same grammar** for
Earth: structure + neighborhood bubble, not one number and not a date.

**Refresh:** `python scripts/build_earth_system_prediction_layer.py`

## What we will not claim

- The time/place of the next large earthquake or VEI≥4 eruption.
- Beating ECMWF at subseasonal (S2S) week 3–4.
- A post-hoc Solar Cycle 25 sunspot-number pick.

Those are T1 look / catalog noise, not seed-closed centrals.

## Locks

| ID | Domain | Lock | Kill | Not |
|----|--------|------|------|-----|
| `PRED-056` | Seismology | 1.0 b_value | USGS ComCat / ISC-GEM named global MLE b-value outside 0.90–1.10 | A date or place for the next M≥7 earthquake. |
| `PRED-057` | Seismology | 1.0 same_valve_classifier | community consensus that slow slip and fast earthquakes require two constitutive laws with no viscosity / rate-state continuum | A forecast of a specific slow-slip episode. |
| `PRED-058` | Volcanology_Panel | 0.5 pooled_median_error_pct_ceiling | volcanology_panel_benchmark exceeds 0.5% on GVP/USGS refresh | The date of the next VEI≥4 eruption. |
| `PRED-059` | Space_Weather | 0.5 pooled_median_error_pct_ceiling | space_weather or geomagnetism classifier panel exceeds 0.5% / 99.5% accuracy on SWPC refresh | A flare time-of-arrival for a named AR. |
| `PRED-060` | Fluid_Dynamics | 0.5 pooled_median_error_pct_ceiling | Between_Scale_Interconnects fluid_tanks_* channels exceed 0.5% on NDBC refresh | Next week's local forecast or the next El Niño onset date. |
| `PRED-061` | Seismology | 0.5 pooled_median_error_pct_ceiling | lithosphere vp/vs median channel exceeds 0.5% (deep PREM stays structural) | A new radial Earth model replacing PREM. |
| `PRED-062` | Space_Weather | 1.0 two_sector_classifier | quiet-time and storm-time SWPC classes collapse to one residual sector on refresh | A post-hoc Cycle 25 sunspot-number pick. |
| `PRED-063` | Climate_Science | 0.5 pooled_median_error_pct_ceiling | climate_observed or NDBC fluid-tank channels exceed 0.5% | S2S ensemble beating ECMWF at week 3–4. |
| `PRED-064` | Seismology | 1.0 issued_windows_scored | issued forecast JSON rewritten after valid_from, or scoring abandoned | A clock-time for a single hypocenter, or a USGS/NWS watch replacement. |

Hand PREDs live in `predictions/preregistered_predictions_manifest.yaml`.
Score outcomes in `results/` — do not rewrite these centrals.

Scientist question map: [`SCIENTIST_OPEN_QUESTIONS.md`](SCIENTIST_OPEN_QUESTIONS.md).
