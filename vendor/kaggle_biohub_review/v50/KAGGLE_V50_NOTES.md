# FSOT Biohub Kaggle v50 — competitive U-Net + FSOT vision

Competition: [biohub-cell-tracking-during-development](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development)

## Architecture

```
zarr → U-Net detect (+ FSOT vision + FSOT-Living emergence) → ranked centroids → FSOT fsot_gate linking → submission.csv
```

### FSOT-Living bridge (`fsot_living_emergence.py`)

Ports [FSOT-Living](https://github.com/dappalumbo91/FSOT-Living) mechanisms:

| Living mechanism | Kaggle use |
|------------------|------------|
| `accuracy_homeo` (vision thr 0.62) | Proxy score 0.54 → deficit boost / damping |
| Vision regime (emergence/damping) | Over-detect → damping + rank prune; under-detect → emergence |
| Closed-set ranking (73.7% raw_zs strength) | Rank U-Net candidates by FSOT scalar; cap per frame |

Env: `FSOT_LIVING_EMERGENCE=1` (experimental), `FSOT_LIVING_PROXY_ACCURACY=0.54`

**Status:** Bridge implemented; default **off** until U-Net detection confidences feed the
Living ranker (scalar-only proxy over-prunes with baseline weights). Next step: wire
`predict_unet_transformer` heatmap scores into `detection_coherence_score`.

| Stage | v49 (peaks) | v50 (competitive) |
|-------|-------------|-------------------|
| Detection | peaks/threshold | **U-Net** + FSOT-derived `det_threshold` |
| Linking | FSOT gate | FSOT gate (same) |
| Score (train proxy) | ~0.676 | **0.90+** with FT weights on Kaggle GPU |

## Local benchmark (2026-07-13, `44b6_0113de3b`, CPU)

| Config | Nodes | Train proxy score |
|--------|-------|-------------------|
| v49 peaks + FSOT | 25,767 | **0.6764** |
| v50 U-Net baseline weights + FSOT vision | 30,062 | 0.5463 |
| v50 U-Net baseline, det_thr=0.65 | 29,199 | 0.5481 |

Baseline U-Net weights **over-detect** vs peaks on this dataset. Competitive scores require
**fine-tuned** weights (`aashishnegi23/cellmot-ft-detector-biohub`) attached on Kaggle.

## v50 vs v49

| Item | v49 | v50 |
|------|-----|-----|
| Default engine | `fsot` + peaks | **`fsot_unet`** (auto-fallback to peaks) |
| FSOT on vision | — | `fsot_vision_calibrate.py` per-dataset threshold |
| GPU | disabled | **auto** (cuda if assigned, else CPU) |
| ILP | off | off |
| det threshold | fixed | FSOT-calibrated (base 0.55) |

## Required Kaggle datasets

1. Competition data (test mount)
2. `aashishnegi23/cellmot-ft-detector-biohub` — fine-tuned detector weights
3. `thibautgoldsborough/cellmot-baseline-artifacts` — cellmot wheels + baseline weights

## Upload steps

1. Create Kaggle dataset **`fsot-v50-competitive-bundle`** from this `v50/` folder.
2. New notebook from `fsot-biohub-v50.ipynb`.
3. Add inputs: competition + ft-detector + baseline-artifacts + v50 bundle.
4. Settings → Accelerator → **GPU T4 x2** if available; CPU works but slower.
5. Run All → Submit `submission.csv`.

## Environment (defaults in `kaggle_main_runner.py`)

```text
BIOHUB_ENGINE=auto
FSOT_VISION_CALIBRATE=1
FSOT_LINK_MODE=fsot_gate
FSOT_GATE_FRAC=0.42
FSOT_GATE_ADAPTIVE=1
FSOT_GATE_RESCUE=1
CELLMOT_DET_THRESHOLD=0.55   # overridden per-dataset when vision calibrate on
CELLMOT_USE_ILP=0
CELLMOT_DET_TTA=0
```

## Local verification

```powershell
cd vendor\kaggle_biohub_review\v50
python -m venv .venv
.\.venv\Scripts\pip install -r requirements-v50.txt
$env:KAGGLE_TEST_DIR = "D:\Kaggle_Biohub_Data\test"
$env:CELLMOT_UNET_WEIGHTS = "D:\Kaggle_Biohub_Data\cellmot\cellmot-baseline-artifacts\weights\unet_transformer\split_0\edge_predictor_best.pth"
$env:CELLMOT_DEVICE = "cpu"
$env:BIOHUB_ENGINE = "fsot_unet"
.\.venv\Scripts\python kaggle_main_runner.py
.\.venv\Scripts\python kaggle_submission_score.py submission_v50.csv --gt-dir D:\Kaggle_Biohub_Data\train
```

Download all four test zarrs + train GT:

```powershell
.\.venv\Scripts\python download_kaggle_assets.py --out D:\Kaggle_Biohub_Data
```

## Fast fallback

Set `BIOHUB_ENGINE=fsot` and `BIOHUB_DETECTOR=peaks` for CPU-only peaks pipeline (~0.67 train proxy).