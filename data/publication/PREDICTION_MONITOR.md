# FSOT Prediction Monitor

*Generated 2026-08-06T13:06:59.168415+00:00 · online=False · pin D1D38A*

Tracks **preregistered** FSOT locks against near/future public data drops. Predicted centrals are frozen; this report only updates **outcome status**.

## Summary

| Metric | Value |
|--------|------:|
| Watches | 14 |
| Prereg PREDs (hand YAML) | 48 |
| **Atlas predictions** | **1219** |
| Atlas domains covered | 472 |
| Multi-tool H₀ locks | 25 |
| H₀ FSOT span | 67.383958–75.146282 |
| Residual-hold gate fails | 0 |
| PREDs with future_survey tag | 13 |
| T5 freeze | `TOE-PREREG-20260806` |
| Green gate | 472/472 |
| Report SHA | `1a4fe245853be6b4…` |

Atlas kinds: multi_tool_h0=25, residual_hold=472, scalar_lock=722

### Outcomes

| Outcome | Count |
|---------|------:|
| local_green_hold | 8 |
| open_predata | 6 |

## Multi-tool H₀ (bubble bleed)

Full table: `data/publication/H0_MULTI_TOOL_PREDICTIONS.md`  
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

## High-urgency open watches

- `WATCH-Euclid-DR1-S8`
- `WATCH-Rubin-LSST-Y1-structure`
- `WATCH-Local-H0-JWST`
- `WATCH-LVK-GWTC`

## All watches

| ID | Sector | Urgency | Outcome | FSOT lock | Window |
|----|--------|---------|---------|-----------|--------|
| WATCH-Euclid-DR1-S8 | cosmology | high | **open_predata** | `0.805` | 2026-11 to mid-2027 |
| WATCH-Euclid-DR1-wa | cosmology | high | **local_green_hold** | `-1.018` | 2026-11 to 2027 |
| WATCH-Rubin-LSST-Y1-structure | cosmology | high | **open_predata** | `0.805` | 2026-10 to 2027 |
| WATCH-DESI-BAO-H0 | cosmology | high | **local_green_hold** | `70.75` | ongoing 2026-2027 |
| WATCH-Local-H0-JWST | cosmology | high | **open_predata** | `70.75` | rolling 2026-2027 |
| WATCH-CMB-Neff | cosmology | medium | **open_predata** | `3.046` | 2026-2028 |
| WATCH-LVK-GWTC | gravitational_waves | high | **open_predata** | — | 2026-05 done (GWTC-5); more O4 ~Dec 2026; O5 ~late 2026 |
| WATCH-PDG-mH | particle_physics | medium | **local_green_hold** | `125.25` | annual |
| WATCH-muon-g2 | particle_physics | medium | **open_predata** | `2.49e-09` | 2026-2027 literature |
| WATCH-CHIME-FRB | multi_messenger | medium | **local_green_hold** | `200.0` | rolling |
| WATCH-JWST-highz | astrophysics | medium | **local_green_hold** | — | rolling 2026-2027 |
| WATCH-Climate-NCEI | earth_science | low | **local_green_hold** | `0.5` | continuous |
| WATCH-Zebrafish-atlas | biology | medium | **local_green_hold** | `0.358` | rolling |
| WATCH-Fuel-lab-hold | energy | low | **local_green_hold** | `0.039349` | on demand |

## Schedule

```text
7d
  python scripts/run_prediction_monitor.py
14d
  python scripts/run_prediction_monitor.py --online
```

Related: `data/prediction_monitor_registry.yaml` · `docs/PREDATA_RISK.md` · `data/toe_prereg_freeze.json` · `docs/INDEPENDENT_REPRODUCTION.md`
