# FSOT Biohub Kaggle v49 — CPU-only

Competition: [biohub-cell-tracking-during-development](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development)

**Runtime constraint:** competition workers are CPU-only. v49 forces `CELLMOT_DEVICE=cpu` and defaults to `BIOHUB_ENGINE=fsot` + `BIOHUB_DETECTOR=peaks` (no torch/cuda required).

## v49 vs v48

| Item | v48 | v49 |
|------|-----|-----|
| Accelerator | GPU T4/P100 | **None (CPU)** |
| Default engine | `fsot_unet` | `fsot` + peaks |
| CUDA | enabled | `CUDA_VISIBLE_DEVICES=""` |
| ILP | off | off |
| Validation | `KAGGLE_SUBMISSION_FAST_VALIDATE=0` | same |

## Bundle contents (`vendor/kaggle_biohub_review/v49/`)

- `kaggle_main_runner_cpu.py` — entry point
- `fsot_original_competition.py`, `fsot_core.py`, `fsot_cellular_bridge.py`
- `biohub_competitive.py`, `biohub_unet_engine.py` (write_submission_csv + optional CPU U-Net)
- `validate_kaggle_submission.py`, `csv_to_geffs.py`
- `fsot-biohub-v49-cpu.ipynb` — Kaggle notebook

## Upload steps

1. Create Kaggle dataset **`fsot-v49-cpu-bundle`** from this `v49/` folder (or attach repo files).
2. New notebook from `fsot-biohub-v49-cpu.ipynb`.
3. Add competition data + `fsot-v49-cpu-bundle` as inputs.
4. Settings → Accelerator → **None**.
5. Run All → Submit `submission.csv`.

## Optional CPU U-Net

If weights dataset is attached, set `BIOHUB_ENGINE=fsot_unet` — still runs on CPU (slower).

## Local smoke test

```powershell
cd vendor\kaggle_biohub_review\v49
python -m venv .venv
.\.venv\Scripts\pip install -r requirements-cpu-smoke.txt
python make_smoke_zarr.py --out D:\Kaggle_Biohub_Data\test
$env:KAGGLE_TEST_DIR = "D:\Kaggle_Biohub_Data\test"
.\.venv\Scripts\python kaggle_main_runner_cpu.py
```

Runner validates schema inline (no torch). Local Windows verification (2026-07-13):

```text
44b6_0113de3b  frames=100  nodes=25767  edges=25535  rows=51302
csv_to_geffs: OK
train proxy score: 0.6764 (adj_edge_jaccard=0.6764)
```

**Local data layout** (`D:\Kaggle_Biohub_Data`):

| Path | Source |
|------|--------|
| `test/` | `python download_kaggle_assets.py` or competition mount |
| `train/` | train `.geff` + `.zarr` for `44b6_0113de3b` (scoring) |
| `cellmot/cellmot-baseline-artifacts/wheels/` | Kaggle dataset (Linux wheels for notebook) |

Windows local deps: `pip install -r requirements-cpu-smoke.txt` plus optional `torch` (CPU) for `--score`.

## Grading alignment

- Schema: `id,dataset,row_type,node_id,t,z,y,x,source_id,target_id`
- `validate_kaggle_submission.py` mirrors `csv_to_geffs` + node_id 1..N rules
- Competition score: per-dataset graph edge Jaccard vs ground truth (train proxy locally)