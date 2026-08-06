# MPCORB baseline epoch run (~30–60 min)

Training-style **epochs**: each wave expands the queue, fetches a batch of raw MPC observations, runs **model-correct FSOT residual verify** on every stored object, then scores a limited Horizons O–C batch. Soft wall-clock stop. **No automatic git push.**

## Why epochs

Same idea as LLM training:

| LLM | This pipeline |
|-----|----------------|
| Epoch / step | Expand + fetch + verify + O–C |
| Checkpoint | `pipeline_state.json`, `epoch_log.jsonl`, `epoch_status.json` |
| Loss gate | FSOT residual ≤ 0.5% per object (halt if fail) |
| Rate limits | `--sleep`, `--fetch-per-epoch`, `--oc-per-epoch` |
| Full train later | Raise `--max-minutes` / `--epochs` after baseline is clean |

## Default baseline (~45–50 min)

```powershell
python scripts/run_mpcorb_epoch_baseline.py
```

Defaults:

| Knob | Value | Role |
|------|------:|------|
| `--epochs` | 4 | Max waves |
| `--max-minutes` | 50 | Soft stop |
| `--fetch-per-epoch` | 60 | MPC downloads / wave |
| `--oc-per-epoch` | 25 | New Horizons scores / wave |
| `--queue-add-per-epoch` | 80 | New objects via **sequential** catalog walk |
| `--sleep` | 0.55 s | API cushion |

**Expansion mode:** sequential walk of MPCORB (resume `catalog_walk_line`), not stratified cell caps. Stratified cells max out around `n_cells × per_cell` (~175 at per_cell=25); sequential can enqueue the full eligible numbered set (~100k at min_obs≥15) and eventually the whole catalog.

Shorter smoke:

```powershell
python scripts/run_mpcorb_epoch_baseline.py --max-minutes 20 --epochs 2 --fetch-per-epoch 40 --oc-per-epoch 15
```

Graceful stop while running:

```powershell
# create stop file on external store
New-Item -ItemType File -Force "G:\FSOT-PublicData\anomaly_observables\mpcorb_raw_observations\STOP_EPOCHS"
```

## Watch progress

```powershell
Get-Content "G:\FSOT-PublicData\anomaly_observables\mpcorb_raw_observations\epoch_status.json"
# or repo mirror:
Get-Content data\mpcorb_epoch_status.json
```

Final report:

- `G:/…/epoch_baseline_report.json`
- `data/mpcorb_epoch_baseline_report.json`

## After baseline

1. Check `all_pass` on FSOT verify and scan O–C medians / failures.
2. Fix any interface / rate-limit issues.
3. **Then** ask to commit/push.
4. Full run example (when ready):

```powershell
python scripts/run_mpcorb_epoch_baseline.py --max-minutes 720 --epochs 40 --fetch-per-epoch 80 --oc-per-epoch 30 --sleep 0.55
```

## Model reminder

FSOT residual is **dimensional interface** residual law — not `Δn × calendar years`. Standard O–C arcsec is the classical clock layer only.
