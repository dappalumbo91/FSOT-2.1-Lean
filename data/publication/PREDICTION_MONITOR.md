# FSOT Prediction Monitor

*Generated 2026-08-06T12:59:40.068574+00:00 · online=True · pin D1D38A*

Tracks **preregistered** FSOT locks against near/future public data drops. Predicted centrals are frozen; this report only updates **outcome status**.

## Summary

| Metric | Value |
|--------|------:|
| Watches | 14 |
| Prereg PREDs | 48 |
| PREDs with future_survey tag | 13 |
| Prereg domains | 27 |
| T5 freeze | `TOE-PREREG-20260806` |
| Green gate | 472/472 |
| Report SHA | `e1633804ad823847…` |

### Outcomes

| Outcome | Count |
|---------|------:|
| data_available | 1 |
| local_green_hold | 8 |
| open_predata | 3 |
| source_reachable_awaiting_release | 2 |

## High-urgency open watches

- `WATCH-Euclid-DR1-S8`
- `WATCH-Rubin-LSST-Y1-structure`
- `WATCH-Local-H0-JWST`
- `WATCH-LVK-GWTC`

## All watches

| ID | Sector | Urgency | Outcome | FSOT lock | Window |
|----|--------|---------|---------|-----------|--------|
| WATCH-Euclid-DR1-S8 | cosmology | high | **source_reachable_awaiting_release** | `0.805` | 2026-11 to mid-2027 |
| WATCH-Euclid-DR1-wa | cosmology | high | **local_green_hold** | `-1.018` | 2026-11 to 2027 |
| WATCH-Rubin-LSST-Y1-structure | cosmology | high | **source_reachable_awaiting_release** | `0.805` | 2026-10 to 2027 |
| WATCH-DESI-BAO-H0 | cosmology | high | **local_green_hold** | `70.75` | ongoing 2026-2027 |
| WATCH-Local-H0-JWST | cosmology | high | **open_predata** | `70.75` | rolling 2026-2027 |
| WATCH-CMB-Neff | cosmology | medium | **open_predata** | `3.046` | 2026-2028 |
| WATCH-LVK-GWTC | gravitational_waves | high | **data_available** | — | 2026-05 done (GWTC-5); more O4 ~Dec 2026; O5 ~late 2026 |
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
