# FSOT predictions

**This folder is the home for all preregistered predictions and monitor artifacts.**

## Start here (human / X)

| Doc | Use |
|-----|-----|
| **[`EXPLAINED.md`](EXPLAINED.md)** | Full explanation through the model (read this first) |
| **[`NEXT_LAYERS.md`](NEXT_LAYERS.md)** | **What to watch now + which prediction layer to expand next** |
| **[`reports/PREDICTION_TIERS.md`](reports/PREDICTION_TIERS.md)** | **Tier A–D split** (contested vs atlas vs scaffold) |
| **[`public/ONE_PAGER.md`](public/ONE_PAGER.md)** | One-screen summary |
| **[`public/X_READY.md`](public/X_READY.md)** | Copy-paste posts + threads for X |
| **[`public/TIERS_FOR_X.md`](public/TIERS_FOR_X.md)** | Short tier blurb for posts |
| **[`public/STORY_HUBBLE_BUBBLE.md`](public/STORY_HUBBLE_BUBBLE.md)** | Narrative: why the sky disagrees with itself |
| `reports/` | Tables generated from the machine ledgers |

### Tiers (honest communication)

| Tier | Lead on X? | Contents |
|------|:----------:|----------|
| **A** Contested / public survey | Yes | H₀ tools+hosts, S₈, wₐ, Euclid/DESI… |
| **B** Empirical atlas | Breadth only | Residual + scalar holds (~1400) |
| **C** Lab / engineering | Support | Fuel, materials, climate, … |
| **D** Scaffold / speculation | Label only | Cold-fusion scaffolds, Z-islands, transporter… |

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
python scripts/build_catalog_prediction_layer.py
python scripts/build_higgs_prediction_layer.py
python scripts/build_prediction_tiers.py
python scripts/run_prediction_monitor.py
```

Higgs next phase (tighten without changing global 0.5%): [`HIGGS_TIGHTEN_PLAN.md`](HIGGS_TIGHTEN_PLAN.md)

MPCORB classical metrics (arcsec RMS / U / Kepler — dual scoreboard with FSOT %):

```powershell
python scripts/build_mpcorb_classical_metrics.py
```

## Related docs

- `docs/PREDICTION_MONITOR.md`
- `docs/PREDICTION_MONITORING_POLICY.md`
- `docs/PREDATA_RISK.md`
- `docs/FSOT_EXPLAINED_LAYMAN.md`
