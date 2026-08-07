# Genetics diversity pack (storage-capped)

*Generated 2026-08-07T00:25:27.765629+00:00*

## Paradigm

Same residual law as astronomy packs. Not secular sky drift. Not a claim to replace AlphaFold coordinate generation.

Guide: [`GENETICS_PIVOT_GUIDE.md`](GENETICS_PIVOT_GUIDE.md)

## Storage

- **0.022 MB** / budget 50.0 MB
- Path: `G:/FSOT-PublicData/anomaly_observables/genetics_diversity_pack`

## FSOT residual

- Records: **131**
- Pooled median: **0.0153110614693258%**
- Over 0.5% gate: **0**
- all_pass: **True**

| Cell | n | median residual % |
|------|--:|------------------:|
| disease_relevant | 35 | 0.015311061469323869 |
| housekeeping | 32 | 0.015311061469327033 |
| longevity_adjacent | 35 | 0.01531106146932526 |
| metabolic | 29 | 0.015311061469327945 |

### By property

| Property | median residual % |
|----------|------------------:|
| af_fractionPlddtConfident_pct | 0.015311061469322446 |
| af_fractionPlddtLow_pct | 0.015311061469327165 |
| af_fractionPlddtVeryHigh_pct | 0.015311061469324302 |
| af_fractionPlddtVeryLow_pct | 0.015311061469325486 |
| af_globalMetricValue | 0.015311061469322162 |
| mol_weight_da | 0.015311061469323105 |
| sequence_length | 0.022236250385201096 |

## Claims

- **Yes:** FSOT residual-matches UniProt sequence/mass and AlphaFold DB confidence metrics at Biology/Biochemistry interfaces with zero free parameters.
- **No:** We did not re-derive atomic coordinates or run wet-lab sequencing on this PC.

```powershell
python scripts/run_genetics_diversity_pack.py --budget-mb 50
```
