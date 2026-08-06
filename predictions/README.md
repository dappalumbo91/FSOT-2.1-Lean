# FSOT predictions

**This folder is the home for all preregistered predictions and monitor artifacts.**

## Start here (human / X)

| Doc | Use |
|-----|-----|
| **[`EXPLAINED.md`](EXPLAINED.md)** | Full explanation through the model (read this first) |
| **[`public/ONE_PAGER.md`](public/ONE_PAGER.md)** | One-screen summary |
| **[`public/X_READY.md`](public/X_READY.md)** | Copy-paste posts + threads for X |
| **[`public/STORY_HUBBLE_BUBBLE.md`](public/STORY_HUBBLE_BUBBLE.md)** | Narrative: why the sky disagrees with itself |
| `reports/` | Tables generated from the machine ledgers |

## Machine ledgers

| Path | Role |
|------|------|
| `preregistered_predictions_manifest.yaml` | Hand-curated PRED-001… locks |
| `prediction_monitor_registry.yaml` | Survey watches + kill criteria |
| `sector_h0_seed.json` | Multi-tool H₀ density seeds (BH→WH bubble) |
| `h0_multi_tool_predictions.json` | Per-instrument H₀ predictions |
| `h0_sightline_predictions.json` | SH0ES per-host sightline H₀ |
| `cchp_trgb_sightline_predictions.json` | Carnegie TRGB per-host H₀ |
| `domain_prediction_atlas.json` | Full multi-sector atlas (~1400+ PREDs) |
| `nearest_data_drop_ranking.json` | Closest survey drop priority |
| `prediction_monitor_report.json` | Last monitor run |
| `toe_prereg_freeze.json` | Label B T5 SHA freeze bundle |
| `contested_future_observation_ledger.json` | Contested future differentiators |
| `external_data_pointers.json` | Paths to bulk data on external drive |
| `reports/` | Human-readable markdown tables |

## Policy

- **Git commit SHA** = preregistration clock (see `docs/PREDICTION_MONITORING_POLICY.md`).
- **Do not freeze development** while waiting for survey drops — log outcomes when data lands.
- **Large catalogs** (CCHP hosts, open-science dumps) live on `G:/FSOT-PublicData/…`, not on C:.

## Rebuild

```powershell
python scripts/build_h0_multi_tool_predictions.py
python scripts/build_h0_sightline_predictions.py
python scripts/build_cchp_trgb_sightline_predictions.py
python scripts/build_domain_prediction_atlas.py
python scripts/rank_nearest_data_drops.py
python scripts/run_prediction_monitor.py
```

## Related docs

- `docs/PREDICTION_MONITOR.md`
- `docs/PREDICTION_MONITORING_POLICY.md`
- `docs/PREDATA_RISK.md`
- `docs/FSOT_EXPLAINED_LAYMAN.md`
