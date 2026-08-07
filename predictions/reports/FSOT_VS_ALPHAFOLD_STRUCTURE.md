# FSOT vs AlphaFold — structure head-to-head

*Generated 2026-08-07T00:37:01.681589+00:00*

## Mission

FSOT sequence-only structure prediction vs AlphaFold, scored on experimental PDB Cα RMSD

- Engine: `fsot_structure_engine_v1` · **free parameters: 0**
- Metric: Cα RMSD (Å) after Kabsch alignment to experimental PDB (lower is better)
- Hardware: Designed to run on HP Omen-class desktop, storage-capped cache

## Scoreboard

| Side | Median Cα RMSD (Å) | Wins |
|------|-------------------:|-----:|
| **FSOT** | **16.48006804477105** | **1** |
| AlphaFold | 0.43535089145183603 | 7 |
| Ties | — | 0 |

Paired proteins: **8** · FSOT win rate: **0.125**

## Per protein

| UniProt | Name | PDB | FSOT RMSD Å | AF RMSD Å | Winner |
|---------|------|-----|------------:|----------:|:------:|
| P69905 | Hemoglobin alpha | 1A3N | 19.130 | 0.2697832925375286 | AlphaFold |
| P68871 | Hemoglobin beta | 1A3N | 16.480 | 0.5196952732909565 | AlphaFold |
| P00918 | Carbonic anhydrase II | 1CA2 | 23.959 | 0.3617948214686656 | AlphaFold |
| P00441 | SOD1 | 2C9V | 18.005 | 0.28634210236027413 | AlphaFold |
| P61626 | Lysozyme human | 1LZ1 | 14.579 | 0.43535089145183603 | AlphaFold |
| P61823 | RNase A | 7RSA | 15.794 | 0.3314052297214222 | AlphaFold |
| P0CG47 | Ubiquitin | 1UBQ | 13.083 | 1.6959974037473304 | AlphaFold |
| P01308 | Insulin | 4INS | 5.758 | 6.619892197937176 | FSOT |

## How to run

```powershell
python scripts/run_fsot_vs_alphafold_structure.py --max-proteins 8 --rounds 90
```

## Next

- Increase refine rounds / multi-start from secondary string variants
- Add side-chain packing after Cα (still seed-only)
- Expand benchmark set (CASP-style hard targets)
- Distogram assembly F15 full matrix for n>200
