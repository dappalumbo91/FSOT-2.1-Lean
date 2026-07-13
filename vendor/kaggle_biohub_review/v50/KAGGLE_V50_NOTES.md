# FSOT Biohub Kaggle v50 — competitive U-Net + FSOT + Living

Competition: [biohub-cell-tracking-during-development](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development)

## Architecture

```
zarr → U-Net FT detect (conf-ranked) → FSOT fsot_gate linking → submission.csv
         ↑ optional FSOT-Living emergence when proxy accuracy drops
```

## Competitive defaults (tuned 2026-07-13)

| Parameter | Value | Why |
|-----------|-------|-----|
| `CELLMOT_UNET_WEIGHTS` | **FT biohub** | `cellmot-ft-detector-biohub` |
| `CELLMOT_DET_THRESHOLD` | **0.45** | Recall/recall balance (0.55 → 0.50 score) |
| `CELLMOT_NMS_UM` | **6.0** | Tighter than 8.0; 0.857 train proxy |
| `FSOT_LINK_MODE` | `fsot_gate` | FSOT scalar + ML edge fusion |
| `FSOT_LIVING_EMERGENCE` | `0` | Enable for deficit tuning experiments |

## Local benchmark (`44b6_0113de3b`, CPU, train proxy)

| Config | Score |
|--------|-------|
| v49 peaks + FSOT | 0.6764 |
| FT + det 0.55 + NMS 8 | 0.505 |
| **FT + det 0.45 + NMS 6 + fsot_gate** | **0.8570** |
| FT + det 0.45 + NMS 6 + Living | 0.8422 |

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