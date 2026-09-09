# FSOT Prediction Monitor

*Generated 2026-09-07T23:46:07.767115+00:00 · online=False · pin D1D38A*

Tracks **preregistered** FSOT locks against near/future public data drops. Predicted centrals are frozen; this report only updates **outcome status**.

## Summary

| Metric | Value |
|--------|------:|
| Watches | 29 |
| Prereg PREDs (hand YAML) | 76 |
| **Atlas predictions** | **1445** |
| Atlas domains covered | 472 |
| Multi-tool H₀ locks | 25 |
| Sightline host H₀ | 22 (mean 73.302397) |
| H₀ tool span | 67.383958–75.146282 |
| Non-cosmology domains | 458 |
| Sector portfolios | 9 |
| Residual-hold gate fails | 0 |
| PREDs with future_survey tag | 41 |
| T5 freeze | `TOE-PREREG-20260806` |
| Green gate | 477/477 |
| Report SHA | `9e422c58a67e8f97…` |

Atlas kinds: h0_sightline_host=22, h0_sightline_sector=5, h0_trgb_host=22, h0_trgb_sector=5, multi_tool_h0=25, residual_hold=472, scalar_lock=885, sector_portfolio_hold=9

### Outcomes

| Outcome | Count |
|---------|------:|
| local_green_hold | 17 |
| open_predata | 12 |

## Multi-tool H₀ (bubble bleed)

Full table: `predictions/reports/H0_MULTI_TOOL_PREDICTIONS.md`  
Theory: each measurement system samples a different BH→WH information-flow sector.

| Tool | FSOT H₀ | Literature | Class |
|------|--------:|-----------:|-------|
| planck_cmb_local | **67.383958** | 67.4 | early_universe_cmb |
| tdcosmo_conservative | **67.436763** | 67.4 | strong_lens_time_delay |
| planck_plus_bao_combo | **67.647983** | 67.66 | early_universe_cmb |
| sn_h0_no_local_cal | **67.806398** | 67.8 | snia_early_calibrated |
| act_dr6_cmb | **67.859203** | 67.9 | early_universe_cmb |
| spt3g_cmb | **68.281642** | 68.3 | early_universe_cmb |
| global_cmb_background | **68.440057** | 68.44005682979427 | fsot_global |
| desi_bao_rs_anchored | **68.524545** | 68.52 | bao_intermediate |

### Sightline hosts (sample)

| Host | FSOT H₀ | Sector | Method |
|------|--------:|--------|--------|
| LMC | **70.214931** | `sector_1_local_low` | TRGB_anchor |
| NGC4258 | **70.388608** | `sector_3_fsot_document` | Maser_anchor |
| NGC3021 | **73.470375** | `sector_2_carnegie` | SH0ES_Cepheid |
| NGC3370 | **73.470375** | `sector_2_carnegie` | SH0ES_Cepheid |
| NGC3627 | **73.470375** | `sector_2_carnegie` | SH0ES_Cepheid |
| NGC3982 | **73.470375** | `sector_2_carnegie` | SH0ES_Cepheid |
| UGC9391 | **73.470375** | `sector_2_carnegie` | SH0ES_Cepheid |
| M101 | **73.497059** | `sector_3_fsot_document` | SH0ES_Cepheid |

Full hosts: `predictions/reports/H0_SIGHTLINE_PREDICTIONS.md`

## High-urgency open watches

- `WATCH-Euclid-DR1-S8`
- `WATCH-Rubin-LSST-Y1-structure`
- `WATCH-Local-H0-JWST`
- `WATCH-LVK-GWTC`
- `WATCH-Dated-fluid-forecasts`

## All watches

| ID | Sector | Urgency | Outcome | FSOT lock | Window |
|----|--------|---------|---------|-----------|--------|
| WATCH-Euclid-DR1-S8 | cosmology | high | **open_predata** | `0.805` | 2026-11 to mid-2027 |
| WATCH-Euclid-DR1-wa | cosmology | high | **local_green_hold** | `-1.018` | 2026-11 to 2027 |
| WATCH-Rubin-LSST-Y1-structure | cosmology | high | **open_predata** | `0.805` | 2026-10 to 2027 |
| WATCH-DESI-BAO-H0 | cosmology | high | **local_green_hold** | `70.75` | ongoing 2026-2027 |
| WATCH-Local-H0-JWST | cosmology | high | **open_predata** | `72.1` | rolling 2026-2027 |
| WATCH-CMB-Neff | cosmology | medium | **open_predata** | `3.046` | 2026-2028 |
| WATCH-LVK-GWTC | gravitational_waves | high | **open_predata** | — | 2026-05 done (GWTC-5); more O4 ~Dec 2026; O5 ~late 2026 |
| WATCH-PDG-mH | particle_physics | medium | **local_green_hold** | `125.25` | annual |
| WATCH-muon-g2 | particle_physics | medium | **open_predata** | `2.49e-09` | 2026-2027 literature |
| WATCH-CHIME-FRB | multi_messenger | medium | **local_green_hold** | `200.0` | rolling |
| WATCH-JWST-highz | astrophysics | medium | **local_green_hold** | — | rolling 2026-2027 |
| WATCH-Climate-NCEI | earth_science | low | **local_green_hold** | `0.5` | continuous |
| WATCH-Zebrafish-atlas | biology | medium | **local_green_hold** | `0.358` | rolling |
| WATCH-USGS-ComCat-b | seismology | medium | **local_green_hold** | `1.0` | continuous |
| WATCH-GVP-volcanology | volcanology | medium | **local_green_hold** | `0.5` | continuous |
| WATCH-SWPC-space-weather | space_weather | medium | **local_green_hold** | `0.5` | continuous |
| WATCH-NDBC-fluid-tanks | weather_climate | medium | **local_green_hold** | `0.5` | continuous |
| WATCH-SSE-constitutive | seismology | low | **open_predata** | `1.0` | rolling 2026-2028 |
| WATCH-Dated-fluid-forecasts | earth_system | high | **open_predata** | `1.0` | score after each valid_to (EQ 7d, WX 48h, solar 72h, tide 48h, volc 14d) |
| WATCH-Tides-residual | oceanography | medium | **local_green_hold** | `0.5` | continuous |
| WATCH-Exoplanet-architecture | exoplanets | medium | **local_green_hold** | `0.5` | continuous |
| WATCH-GWTC-chirp-mass | gravitational_waves | medium | **open_predata** | `0.5` | 2026-12 onward |
| WATCH-GBIF-occurrence | ecology | low | **local_green_hold** | `0.5` | continuous |
| WATCH-Epidemiology-class | epidemiology | low | **local_green_hold** | `0.5` | annual / continuous |
| WATCH-CKM-PMNS | particle | medium | **open_predata** | `0.5` | PDG editions |
| WATCH-FRB-same-kernel | transients | medium | **open_predata** | `1.0` | continuous |
| WATCH-GW-siren-mid-sector | gravitational_waves | medium | **open_predata** | `70.024205` | O4 remainder / O5 |
| WATCH-Hydrology-sectors | hydrology | high | **local_green_hold** | `1.0` | score after each 7d hydro valid_to |
| WATCH-Fuel-lab-hold | energy | low | **local_green_hold** | `0.039349` | on demand |

## Schedule

```text
7d
  python scripts/run_prediction_monitor.py
14d
  python scripts/run_prediction_monitor.py --online
```

Related: `predictions/prediction_monitor_registry.yaml` · `docs/PREDATA_RISK.md` · `predictions/toe_prereg_freeze.json` · `docs/INDEPENDENT_REPRODUCTION.md` · `results/INDEX.md` (outcomes, not predictions)
