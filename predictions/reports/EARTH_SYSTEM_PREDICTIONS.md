# Earth-system predictions (weather, seismic, volcanic, solar)

*Generated 2026-09-08T00:37:18.739034+00:00 · pin D1D38A*

Cosmology already has a 25-tool H₀ layer. This is the **same grammar** for
Earth: structure + neighborhood bubble, not one number. Dated *windows*
exist (PRED-064); clock-time hypocenters do not.

**Refresh:** `python scripts/build_earth_system_prediction_layer.py`

## What we will not claim

- A clock-time and single hypocenter for the next large earthquake or VEI≥4 eruption.
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
| `PRED-065` | NOAA_Coastal_Tides | 0.5 pooled_median_error_pct_ceiling | noaa_coastal_tides_benchmark exceeds 0.5% on CO-OPS refresh | A beat of NOAA harmonic tables at every minute. |
| `PRED-066` | Exoplanet_System_Architecture | 0.5 pooled_median_error_pct_ceiling | Exoplanet_System_Architecture pooled median exceeds 0.5% on NASA archive refresh | The discovery date of the next transiting Earth analog. |
| `PRED-067` | Compact_Object_Binary_Events | 0.5 pooled_median_error_pct_ceiling | compact_object_binary_events chirp-mass class exceeds 0.5% on GWTC refresh | The GPS time of the next compact-binary merger. |
| `PRED-068` | GBIF_Species_Occurrence | 0.5 pooled_median_error_pct_ceiling | gbif_species_occurrence_benchmark exceeds 0.5% on dump refresh | The date a named species arrives in a new county. |
| `PRED-069` | Epidemiology_Panel | 0.5 pooled_median_error_pct_ceiling | epidemiology_panel_benchmark exceeds 0.5% on World Bank / WHO refresh | The start date of the next named outbreak in a named city. |
| `PRED-078` | Hydrology | 1.0 two_sector_classifier | high-flow and quiet NWIS classes collapse to one residual sector, or issued hydro windows never scored | Street-level inundation maps. A 0.5% central on one gage's next-hour stage. |
| `PRED-080` | Grace_Cryosphere | 0.5 pooled_median_error_pct_ceiling | grace_cryosphere |delta| scalar median exceeds 0.5% on GravIS refresh | The calendar day the next ice shelf calves. |
| `PRED-081` | Agriculture_Agroecology | 0.5 pooled_median_error_pct_ceiling | agriculture_agroecology_gap_fill pooled median exceeds 0.5% on GBIF / World Bank refresh | County bushels next Tuesday. A USDA yield-number pick after harvest. |
| `PRED-082` | Gaia_Astrometry_Panel_Deep | 0.5 pooled_median_error_pct_ceiling | Gaia astrometry / CAT-GAIA-DR3 pooled median exceeds 0.5% on DR4 / DR3 reprocess | A new H0 from one star. |
| `PRED-083` | Paleoclimate_Panel | 0.5 pooled_median_error_pct_ceiling | paleoclimate_panel pooled median exceeds 0.5% on ice-core / paleo class refresh | A named-year drought date. |

Hand PREDs live in `predictions/preregistered_predictions_manifest.yaml`.
Score outcomes in `results/` — do not rewrite these centrals.

Scientist question map: [`SCIENTIST_OPEN_QUESTIONS.md`](SCIENTIST_OPEN_QUESTIONS.md).
