# FSOT results (outcomes, not predictions)

**This folder is the measured-outcome ledger.**  
**Predictions stay frozen in [`../predictions/`](../predictions/).**

| Folder | Role |
|--------|------|
| `predictions/` | Timestamped / SHA-locked **forecasts**. Do not rewrite centrals after data lands. |
| `results/` | **What came out later.** Literature, APIs, survey drops, panel refreshes. |

Authority pin: **D1D38A** · zero free parameters · prereg clock = git commit SHA.

## Layout

| Path | Role |
|------|------|
| [`INDEX.md`](INDEX.md) | Human scoreboard (latest literature + monitor) |
| [`outcomes/prediction_outcome_log.jsonl`](outcomes/prediction_outcome_log.jsonl) | Append-only machine log |
| [`literature/`](literature/) | Dated cross-reference packs (`YYYY-MM-DD_*.json` + `.md`) |
| [`monitor/`](monitor/) | Latest prediction-monitor snapshot (written by the runner) |
| [`verification/`](verification/) | Lightweight health / green-gate snapshots from this session |
| [`dated_forecast_scores/`](dated_forecast_scores/) | Hit/miss on issued Earth-fluid windows ([`dated_forecast_scores/REPORT.md`](dated_forecast_scores/REPORT.md)) |

## Policy

1. A prediction is registered when it is committed to `predictions/` (SHA + `registered_at`).
2. When a paper, catalog, or API lands, **append** an outcome here. Do not edit the historical prediction file’s central.
3. Verdicts: `hold` · `partial` · `awaiting` · `theory_rebase` · `kill`.
4. `kill` fires only when a registered `kill_if` / discriminant is actually violated.
5. Local green-gate holds (`477/477` ≤ 0.5% pooled median) live in `data/benchmark_margin_audit.json` and are **mirrored**, not replaced, here.

## Commands

```powershell
# Record one literature / survey outcome (does not touch predictions/)
python scripts/record_prediction_outcome.py --help

# Refresh monitor; writes predictions/ AND results/monitor/
python scripts/run_prediction_monitor.py
python scripts/run_prediction_monitor.py --online

# Score issued dated windows (does not rewrite predictions/)
python scripts/score_earth_fluid_forecasts.py
python scripts/build_dated_forecast_score_report.py

# Empirical green gate (all domain panels)
python scripts/audit_all_benchmark_margins.py
```

Related: [`../docs/PREDICTION_MONITORING_POLICY.md`](../docs/PREDICTION_MONITORING_POLICY.md)
