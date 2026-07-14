# FSOT Biohub Kaggle v48

Competition: [biohub-cell-tracking-during-development](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development)

Base notebook: `damianpalumbo/fsot-biohub-v47-fastsubmit`

## v48 fixes (vs v47)

| Issue in v47 | v48 change |
|--------------|------------|
| `CUDA_VISIBLE_DEVICES=""` forced CPU | Remove that line; enable **GPU** in notebook Settings |
| `CELLMOT_USE_ILP=1` caused 12h timeouts | `CELLMOT_USE_ILP=0` |
| `CELLMOT_DET_THRESHOLD=0.99` killed recall | `0.55` |
| Model reloaded per dataset | `_ENGINE_CACHE` in `biohub_unet_engine.py` |
| Fast validate skipped official loader | `KAGGLE_SUBMISSION_FAST_VALIDATE=0` |

## Upload steps

1. Duplicate v47 notebook on Kaggle → name `fsot-biohub-v48-predictive`.
2. Settings → Accelerator → **GPU T4 x2** (or P100).
3. Replace embedded `biohub_unet_engine.py` / main runner with files in this folder.
4. Delete cell 1 lines that set `CUDA_VISIBLE_DEVICES=""`.
5. Run All → Submit.

## Fast fallback (if GPU queue is long)

Set `BIOHUB_ENGINE=fsot` and `BIOHUB_DETECTOR=peaks` for pure FSOT scalar linking (lower score, finishes fast).