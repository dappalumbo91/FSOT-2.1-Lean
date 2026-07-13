# FSOT Biohub Kaggle v50 — competitive U-Net + FSOT + Living

Competition: [biohub-cell-tracking-during-development](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development)

## Architecture

```
zarr → U-Net FT detect (conf-ranked NMS) → FSOT SequenceTracker linking → submission.csv
         ↑ FSOT-Living adaptive only when proxy < 0.62 (dormant at 0.90)
```

## Competitive defaults (tuned 2026-07-13)

| Parameter | Value | Why |
|-----------|-------|-----|
| `CELLMOT_UNET_WEIGHTS` | **FT biohub** | `cellmot-ft-detector-biohub` |
| `CELLMOT_DET_THRESHOLD` | **0.48** | Best on FSOT pure link sweep |
| `CELLMOT_NMS_UM` | **6.0** | Tighter than 8.0 |
| `FSOT_LINK_MODE` | **`fsot`** | Pure FSOT math linking beats fsot_gate (+0.037) |
| `FSOT_LIVING_PROXY_ACCURACY` | **0.90** | Keeps Living dormant; conf-rank NMS only |
| `FSOT_LIVING_EMERGENCE` | `1` | Adaptive — only activates below 0.62 band |
| `CELLMOT_USE_ILP` | **1** | Global consistency; +0.047 vs no ILP on proxy |
| `CELLMOT_ILP_MAX_EDGES` | **40000** | FSOT graphs ~26k edges/dataset |

## Refinement ladder (train proxy `44b6_0113de3b`)

| Stage | Score | Notes |
|-------|-------|-------|
| v49 peaks + FSOT math | 0.676 | Linking only |
| FT U-Net wrong tuning | 0.505 | det 0.55, NMS 8 |
| FT + det 0.45 + NMS 6 + fsot_gate | 0.857 | ML gate over-filtered |
| det 0.47 + fsot_gate | 0.867 | Gate still drops FSOT edges |
| **FT + det 0.48 + NMS 6 + FSOT pure link** | **0.904** | **Math + ML aligned** |
| All 4 test zarrs submission | 332k rows | Re-run with new defaults |

## FSOT-Living adaptive mode

- `FSOT_LIVING_ADAPTIVE=1`: dormant when `proxy >= 0.62` (math already winning)
- Activates emergence/damping only when accuracy drops below vision organ band
- `FSOT_DET_CONF_RANK=1`: U-Net sigmoid always improves NMS ranking at high proxy

Tune locally: `python tune_v50_params.py --max-frames 50`

Download FT weights locally:

```powershell
python download_ft_weights.py --out D:\Kaggle_Biohub_Data\cellmot
```

## FSOT-Living bridge (`fsot_living_emergence.py`)

Ports [FSOT-Living](https://github.com/dappalumbo91/FSOT-Living) `accuracy_homeo` + closed-set
ranking with **U-Net sigmoid confidences** fused to FSOT scalar. Set `FSOT_LIVING_EMERGENCE=1`
when train-proxy drops below 0.62 to stimulate emergence regions.

## Required Kaggle datasets

1. Competition test mount
2. `aashishnegi23/cellmot-ft-detector-biohub`
3. `thibautgoldsborough/cellmot-baseline-artifacts`

## Upload steps

1. Dataset **`fsot-v50-competitive-bundle`** from this folder
2. Notebook `fsot-biohub-v50.ipynb`
3. Inputs: competition + FT detector + baseline artifacts + bundle
4. GPU T4 x2 recommended
5. Run All → Submit

## Local verification

```powershell
cd vendor\kaggle_biohub_review\v50
pip install -r requirements-v50.txt
python download_ft_weights.py --out D:\Kaggle_Biohub_Data\cellmot
$env:KAGGLE_TEST_DIR = "D:\Kaggle_Biohub_Data\test"
$env:CELLMOT_UNET_WEIGHTS = "D:\Kaggle_Biohub_Data\cellmot\cellmot-ft-detector-biohub\edge_predictor_best.pth"
$env:CELLMOT_DEVICE = "cpu"
python kaggle_main_runner.py
python kaggle_submission_score.py submission_v50.csv --gt-dir D:\Kaggle_Biohub_Data\train
```

Download all four test zarrs: `python download_kaggle_assets.py --out D:\Kaggle_Biohub_Data`

## Fast fallback

`BIOHUB_ENGINE=fsot` + `BIOHUB_DETECTOR=peaks` (~0.67 train proxy, no torch U-Net).