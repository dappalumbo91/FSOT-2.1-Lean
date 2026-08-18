# Sibling embodiment ledgers (pulled into the hub)

Same pin **D1D38A**. These folders are **copies of headline results**, not a second engine.

Refresh:

```powershell
python scripts/sync_sibling_embodiment_ledgers.py
```

Machine report: [`sync_report.json`](sync_report.json)

## Genetics — [FSOT-Genetics](https://github.com/dappalumbo91/FSOT-Genetics)

Product freeze **2026-08-13** · `product_vs_alphafold.json`

| Metric | FSOT product | AlphaFold |
|--------|-------------:|----------:|
| Median Cα RMSD (10 proteins) | **0.13 Å** | **0.47 Å** |
| Sub-2 Å | 10/10 | — |
| Bulk / orphan (sequence-only) | 13.57 Å | — |

Product = measured homologs except the eval PDB + residual only when bonds are broken.  
Bulk = F01–F15 from sequence. Do not mix the two.

Files: [`genetics/PRODUCT_FREEZE.md`](genetics/PRODUCT_FREEZE.md)

## Quantum — [FSOT-Quantum](https://github.com/dappalumbo91/FSOT-Quantum)

| Panel | Result |
|-------|--------|
| BH→WH H₀ replay | Planck **0.024%** · SH0ES **1.00%** (2.5% contested band) · global 68.440 |
| Contested sectors | **14/14** |
| Fold-not-Hilbert | **27/27** job families (DJ, BV, Grover, Shor, QAOA, QPE) |
| Observe path | QC dark → QO look → QM measure |

Files: [`quantum/H0_TENSION.md`](quantum/H0_TENSION.md) · [`quantum/STATUS.md`](quantum/STATUS.md)

## Theory map on this hub

[`docs/CONCEPTS.md`](../../docs/CONCEPTS.md) — BH→WH, bubble bleed, \(\kappa_{ij}\), folds, genetics residual.
