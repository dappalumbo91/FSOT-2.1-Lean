# FSOT vs AlphaFold — structure head-to-head

> **Stale snapshot (2026-08-07).** This file is the **sequence-only bulk / orphan** path (~15 Å median).  
> Current **product** freeze (same-data homologs, 2026-08-13) lives in [FSOT-Genetics](https://github.com/dappalumbo91/FSOT-Genetics): median **0.13 Å** vs AlphaFold **0.47 Å** on 10 proteins.  
> Hub copy: [`../../results/siblings/genetics/PRODUCT_FREEZE.md`](../../results/siblings/genetics/PRODUCT_FREEZE.md).  
> Do not quote this 15 Å table as the Genetics product.

*Generated 2026-08-07T01:24:11.218913+00:00*

## Mission

FSOT sequence-only **bulk** structure prediction vs AlphaFold, scored on experimental PDB Cα RMSD

- Engine: `fsot_protein_F01_F15_fast_v7` · **free parameters: 0**
- Metric: Cα RMSD (Å) after Kabsch alignment to experimental PDB (lower is better)
- Hardware: HP Omen-class desktop; formula path (MDS+sparse), storage-capped cache
- FSOT median fold time: **163.40660001151264 ms**/chain · wall **12.218831300007878 s** (incl. downloads)

## Scoreboard

| Side | Median Cα RMSD (Å) | Wins |
|------|-------------------:|-----:|
| **FSOT** | **15.629035217133008** | **1** |
| AlphaFold | 0.43535089145183603 | 7 |
| Ties | — | 0 |

Paired proteins: **8** · FSOT win rate: **0.125**

## Per protein

| UniProt | Name | PDB | FSOT RMSD Å | AF RMSD Å | predict_ms | Winner |
|---------|------|-----|------------:|----------:|-----------:|:------:|
| P69905 | Hemoglobin alpha | 1A3N | 13.653 | 0.2697832925375286 | 151 | AlphaFold |
| P68871 | Hemoglobin beta | 1A3N | 15.629 | 0.5196952732909565 | 155 | AlphaFold |
| P00918 | Carbonic anhydrase II | 1CA2 | 26.025 | 0.3617948214686656 | 417 | AlphaFold |
| P00441 | SOD1 | 2C9V | 23.178 | 0.28634210236027413 | 172 | AlphaFold |
| P61626 | Lysozyme human | 1LZ1 | 15.223 | 0.43535089145183603 | 158 | AlphaFold |
| P61823 | RNase A | 7RSA | 18.710 | 0.3314052297214222 | 163 | AlphaFold |
| P0CG47 | Ubiquitin | 1UBQ | 14.723 | 1.6959974037473304 | 334 | AlphaFold |
| P01308 | Insulin | 4INS | 5.830 | 6.619892197937176 | 98 | FSOT |

## How to run

```powershell
python scripts/run_fsot_vs_alphafold_structure.py --max-proteins 8 --rounds 24 --sleep 0.2
```

## Next

- Accuracy: improve F15→D map / contact caps until RMSD competitive with AF
- Keep formula path seconds-scale (no O(n²) free-param grind)
- Optional Zig CLI for distogram parity + speed
- Expand benchmark set only after median RMSD moves
